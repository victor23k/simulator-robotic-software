import logging
from typing import override

from simulator.interpreter.ast.stmt import Function, Stmt
from simulator.interpreter.diagnostic import Diagnostic
from simulator.interpreter.environment import Environment
from simulator.interpreter.parse.parser import Parser
from simulator.interpreter.sema.resolver import Resolver
from simulator.arduino import Arduino

import simulator.libraries.standard as standard
import simulator.libraries.serial as serial
import simulator.robot_components.robot_state as state

logger = logging.getLogger("SketchLogger")


class Interpreter(Arduino):
    """
    Arduino sketch interpreter.
    """

    code: str
    parser: Parser
    diagnostics: list[Diagnostic]
    resolver: Resolver
    statements: list[Stmt]
    environment: Environment
    globals: Environment
    valid: bool

    def __init__(self, code: str):
        self.code = code
        self.diagnostics = []
        self.parser = Parser(code, self.diagnostics)
        self.resolver = Resolver(self.diagnostics)
        self.globals = Environment(None)
        self.environment = self.globals
        self.statements = []
        self.valid = False

    @override
    def compile(self, console, board):
        standard.board = board
        standard.state = state.State()
        serial.cons = console

        statements = self.parser.parse()
        self.resolver.resolve(statements)

        self.statements = statements
        self._log_diagnostics()

        self.valid = len(self.diagnostics) == 0  # change to only errors
        return len(self.diagnostics) == 0

    @override
    def check(self) -> bool | None:
        return self.valid

    @override
    def setup(self):
        for statement in self.statements:
            statement.execute(self.environment)

        setup_fn = self.environment.get("setup", 0)
        assert isinstance(setup_fn, Function)

        setup_fn.call([])

    @override
    def loop(self):
        loop_fn = self.environment.get("loop", 0)
        assert isinstance(loop_fn, Function)

        while True:
            loop_fn.call([])

    @override
    def run(self):
        """
        Interprets the loaded Arduino sketch.

        If there are any errors before execution, prints them to standard error
        output and exits.
        """

        if len(self.diagnostics) == 0:
            self.setup()
            self.loop()
        else:
            self._log_diagnostics()

    def run_test(self):
        """
        Interprets the Arduino sketch for a test run.

        This does not require `setup` and `loop` functions.
        """

        for statement in self.statements:
            statement.execute(self.environment)

        setup_fn = self.environment.get("setup", 0)
        loop_fn = self.environment.get("loop", 0)

        if isinstance(setup_fn, Function) and isinstance(loop_fn, Function):
            setup_fn.call([])
            while True:
                loop_fn.call([])

    def _check_program(self) -> bool:
        """
        Checks the loaded Arduino sketch for errors and returns a boolean
        indicating if the program is correct.

        If there are any errors, prints them to standard error output.
        """

        statements = self.parser.parse()
        self.resolver.resolve(statements)
        self._log_diagnostics()

        return len(self.diagnostics) == 0

    def _log_diagnostics(self):
        for diag in self.diagnostics:
            logger.error(diag)
