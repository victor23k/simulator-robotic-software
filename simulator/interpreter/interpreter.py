import logging
from typing import override

from simulator.interpreter.ast.stmt import ArduinoClass, Function, Stmt, LibFn
from simulator.interpreter.diagnostic import Diagnostic
from simulator.interpreter.environment import Environment, Value
from simulator.interpreter.parse.parser import Parser
from simulator.interpreter.preprocessor import Preprocessor
from simulator.interpreter.sema.resolver import Resolver
from simulator.arduino import Arduino

from simulator.interpreter.sema.types import ArduinoObjType, str_to_arduino_type
from simulator.libraries.libs import LibraryManager
import simulator.libraries.string as string
import simulator.libraries.servo as servo
import simulator.libraries.standard as standard
import simulator.libraries.serial as serial
import simulator.robot_components.robot_state as state

logger = logging.getLogger("SketchLogger")


class Interpreter(Arduino):
    """
    Arduino sketch interpreter.
    """

    code: str
    diagnostics: list[Diagnostic]
    statements: list[Stmt]
    environment: Environment
    libraryManager: LibraryManager
    globals: Environment
    valid: bool

    def __init__(self, code: str):
        self.code = code
        self.diagnostics = []
        self.globals = Environment(None)
        self.environment = self.globals
        self.statements = []
        self.libraryManager = LibraryManager()
        self.valid = False

    @override
    def compile(self, console, board):
        standard.board = board
        standard.state = state.State()
        serial.cons = console

        preprocessor = Preprocessor(self.code)
        self.code = preprocessor.process(self.libraryManager)

        parser = Parser(self.code, self.diagnostics)
        resolver = Resolver(self.diagnostics)
        self._setup_libraries(parser, resolver)
        self.statements = parser.parse()

        resolver.resolve(self.statements)

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

    def _log_diagnostics(self):
        for diag in self.diagnostics:
            logger.error(diag)

    def _setup_libraries(self, parser: Parser, resolver: Resolver):
        for fn_name, fn in standard.get_methods().items():
            fn_return_type = str_to_arduino_type(fn[0])
            resolver.define_library_fn(fn_name, fn_return_type)
            self.environment.define(
                fn_name, Value(fn_return_type, LibFn(standard, fn[1], len(fn[2])))
            )

        string_methods: dict[str, Value] = dict()
        for fn_name, fn in string.get_methods().items():
            fn_return_type = str_to_arduino_type(fn[0])
            string_methods[fn_name] = Value(
                fn_return_type, LibFn(string, fn[1], len(fn[2]))
            )

        string_classname = string.get_name()
        string_class = ArduinoClass(
            string.String, string_classname, string_methods, ["val"]
        )
        string_classtype = ArduinoObjType(string_classname)
        resolver.define_library_fn(string_classname, string_classtype)
        self.environment.define(string_classname, Value(string_classtype, string_class))
        parser.add_type_name(string_classname)

        servo_methods: dict[str, Value] = dict()
        for fn_name, fn in servo.get_methods().items():
            servo_methods[fn_name] = LibFn(servo, fn[1], len(fn[2]))

        servo_classname = servo.get_name()
        servo_class = ArduinoClass(servo.Servo, servo_classname, servo_methods, [])
        resolver.define_library_fn(
            servo_classname, ArduinoObjType(servo_classname)
        )
        self.environment.define(servo_classname, servo_class)
        parser.add_type_name(servo_classname)
