import sys
from typing import override

from simulator.interpreter.ast.stmt import Stmt
from simulator.interpreter.diagnostic import Diagnostic
from simulator.interpreter.ast_interpreter import AstInterpreter
from simulator.interpreter.parse.parser import Parser
from simulator.interpreter.sema.resolver import Resolver
from simulator.arduino import Arduino


class Interpreter(Arduino):
    """
    Arduino sketch interpreter.
    """

    code: str
    parser: Parser
    diagnostics: list[Diagnostic]
    resolver: Resolver
    interpreter: AstInterpreter
    statements: list[Stmt]

    def __init__(self, code: str):
        self.code = code
        self.diagnostics = []
        self.parser = Parser(code, self.diagnostics)
        self.resolver = Resolver(self.diagnostics)
        self.interpreter = AstInterpreter(self.diagnostics)

    @override
    def compile(self):
        statements = self.parser.parse()
        self.resolver.resolve(statements)

        self.statements = statements

    @override
    def check(self) -> bool | None:
        return self._check_program()

    @override
    def setup(self):
        raise NotImplementedError()

    @override
    def loop(self):
        raise NotImplementedError()

    @override
    def run(self):
        """
        Interprets the loaded Arduino sketch.

        If there are any errors before execution, prints them to standard error
        output and exits.
        """

        if len(self.diagnostics) == 0:
            self.interpreter.run(self.statements)
        else:
            print(self.diagnostics, file=sys.stderr)

    def _check_program(self) -> bool:
        """
        Checks the loaded Arduino sketch for errors and returns a boolean
        indicating if the program is correct.

        If there are any errors, prints them to standard error output.
        """

        statements = self.parser.parse()
        self.resolver.resolve(statements)

        return len(self.diagnostics) == 0

    def print_diagnostics(self):
        print(self.diagnostics, file=sys.stderr)
