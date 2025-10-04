import logging
import traceback
import importlib.util
import sys
import time
from typing import override
import output.console as console
import compiler.transpiler as transpiler
import libraries.standard as standard
import libraries.serial as serial
import robot_components.robot_state as state
from simulator.arduino import Arduino

module = None
logger = logging.getLogger("SketchLogger")


def _import_module():
    global module
    spec = importlib.util.spec_from_file_location(
        "temp.script_arduino", "temp/script_arduino.py"
    )
    module = importlib.util.module_from_spec(spec)
    sys.modules["temp.script_arduino"] = module
    spec.loader.exec_module(module)


class ArduinoCompiler(Arduino):
    def __init__(self, code):
        self.code = code
        self.valid = False

    @override
    def compile(self, console, board) -> bool:
        """
        Transpiles the Arduino sketch to python code in a temp python script.
        """

        try:
            standard.board = board
            standard.state = state.State()
            serial.cons = console

            warns, errors, self.ast = transpiler.transpile(self.code)
            self.print_errors(errors)
            self.print_warnings(warns)

            if len(errors) == 0:
                self.valid = True
                return True
            return False
        except Exception as e:
            print(f"la excepción es {e}")
            traceback.print_exc()
            logger.error(
                console.Error(
                    "Error de compilación",
                    0,
                    0,
                    "El sketch no se ha podido compilar correctamente",
                ).to_string()
            )
            return False

    @override
    def check(self) -> bool | None:
        return self.valid

    @override
    def setup(self):
        """
        Loads the sketch module from the temp python script and executes the setup
        function.
        """

        global module
        _import_module()
        curr_time_ns = time.time_ns()
        if (
            not standard.state.exec_time_us > curr_time_ns / 1000
            and not standard.state.exec_time_ms > curr_time_ns / 1000000
        ):
            try:
                module.setup()
            except Exception:
                logger.error(
                    console.Error(
                        "Error de ejecución",
                        0,
                        0,
                        "El sketch no se ha podido ejecutar correctamente",
                    )
                )

    @override
    def loop(self):
        global module
        curr_time_ns = time.time_ns()
        if (
            not standard.state.exec_time_us > curr_time_ns / 1000
            and not standard.state.exec_time_ms > curr_time_ns / 1000000
            and not standard.state.exited
        ):
            try:
                module.loop()
            except Exception:
                logger.error(
                    console.Error(
                        "Error de ejecución",
                        0,
                        0,
                        "El sketch no se ha podido ejecutar correctamente",
                    )
                )

    def print_warnings(self, warnings):
        for warning in warnings:
            logger.warning(warning.to_string())

    def print_errors(self, errors):
        for error in errors:
            logger.error(error.to_string())
