from __future__ import annotations

import logging
from types import ModuleType
from typing import TYPE_CHECKING, override
from inspect import signature

if TYPE_CHECKING:
    from simulator.interpreter.ast.stmt import Stmt

from simulator.arduino import Arduino
from simulator.interpreter.diagnostic import Diagnostic
from simulator.interpreter.environment import Environment, Value
from simulator.interpreter.parse.parser import Parser
from simulator.interpreter.preprocessor import Preprocessor
from simulator.interpreter.sema.resolver import Resolver
from simulator.interpreter.sema.types import ArduinoObjType, str_to_arduino_type
from simulator.interpreter.runtime.classes import ArduinoClass, ArduinoInstance
from simulator.interpreter.runtime.functions import Function, LibFn

from simulator.libraries.libs import LibraryManager
import simulator.libraries.standard as standard
import simulator.libraries.serial as serial
import simulator.robot_components.robot_state as state

sketch_logger = logging.getLogger("SketchLogger")
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)


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

        logging.debug("Execute top level")
        for statement in self.statements:
            statement.execute(self.environment)

        setup_fn = self.environment.get("setup", 0)
        assert isinstance(setup_fn, Value)
        assert isinstance(setup_fn.value, Function)

        logging.debug("Execute setup()")
        setup_fn.value.call([], setup_fn.value_type)

    @override
    def loop(self):
        loop_fn = self.environment.get("loop", 0)
        assert isinstance(loop_fn, Value)
        assert isinstance(loop_fn.value, Function)

        logging.debug("Execute loop()")
        loop_fn.value.call([], loop_fn.value_type)

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
            sketch_logger.error(diag)

    def _setup_libraries(self, parser: Parser, resolver: Resolver):
        self._setup_standard_library_functions(resolver)

        library_modules = self.libraryManager.get_available_libs()
        for library_module in library_modules:
            if library_module.get_name() == "Serial":
                self._setup_singleton(library_module, resolver)
            else:
                self._setup_library_class(library_module, parser, resolver)

    def _setup_standard_library_functions(self, resolver: Resolver):
        for fn_name, fn in standard.get_methods().items():
            fn_return_type = str_to_arduino_type(fn[0])
            arity = self._compute_fn_arity(fn[2])
            resolver.define_library_fn(fn_name, fn_return_type)
            self.environment.define(
                fn_name, Value(fn_return_type, LibFn(standard, fn[1], arity))
            )

    def _setup_singleton(self, library_class: ModuleType, resolver: Resolver):
        lib_methods: dict[str, Value] = dict()
        for fn_name, fn in library_class.get_methods().items():
            fn_return_type = str_to_arduino_type(fn[0])
            arity = self._compute_fn_arity(fn[2])
            lib_methods[fn_name] = Value(
                fn_return_type, LibFn(library_class, fn[1], arity)
            )

        lib_classname = library_class.get_name()
        lib_class = getattr(library_class, lib_classname)
        init_method = getattr(lib_class, "__init__")
        lib_init_params = signature(init_method).parameters
        parameters = list(
            filter(lambda p: p not in ["self", "args", "kwargs"], lib_init_params)
        )
        lib_class = ArduinoClass(lib_class, lib_classname, lib_methods, parameters)
        lib_classtype = ArduinoObjType(lib_classname)

        lib_singleton = lib_class.call([], lib_classtype)
        resolver.define_library_fn(lib_classname, lib_classtype)
        self.environment.define(lib_classname, Value(lib_classtype, lib_singleton))

    def _setup_library_class(
        self, library_class: ModuleType, parser: Parser, resolver: Resolver
    ):
        lib_methods: dict[str, Value] = dict()
        for fn_name, fn in library_class.get_methods().items():
            fn_return_type = str_to_arduino_type(fn[0])
            arity = self._compute_fn_arity(fn[2])
            lib_methods[fn_name] = Value(
                fn_return_type, LibFn(library_class, fn[1], arity)
            )

        lib_classname = library_class.get_name()
        lib_class = getattr(library_class, lib_classname)
        init_method = getattr(lib_class, "__init__")
        lib_init_params = signature(init_method).parameters
        parameters = list(
            filter(lambda p: p not in ["self", "args", "kwargs"], lib_init_params)
        )

        constructor_fn_name = f"__{lib_classname}_constructor"
        if constructor_fn_name in lib_methods:
            constructor = lib_methods.pop(constructor_fn_name).value
        else:
            constructor = None

        lib_class = ArduinoClass(
            lib_class, lib_classname, lib_methods, parameters, constructor
        )
        lib_classtype = ArduinoObjType(lib_classname)
        resolver.define_library_fn(lib_classname, lib_classtype)
        self.environment.define(lib_classname, Value(lib_classtype, lib_class))
        parser.add_type_name(lib_classname)

    def _compute_fn_arity(self, parameters: list[str]) -> int | range:
        max_arity = len(parameters)
        optional_parameters = len(
            list(
                filter(lambda param: param[:1] == "(" and param[-1:] == ")", parameters)
            )
        )

        return range(max_arity - optional_parameters, max_arity + 1)
