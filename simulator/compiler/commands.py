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
    spec = importlib.util.spec_from_file_location('temp.script_arduino', 'temp/script_arduino.py')
    module = importlib.util.module_from_spec(spec)
    sys.modules['temp.script_arduino'] = module
    spec.loader.exec_module(module)


class Command:

    def __init__(self, controller):
        self.controller = controller
        self.ready = False

    def execute(self):
        """
        Executes a command object
        """
        pass

    def reboot(self):
        self.ready = False

    def prepare_exec(self):
        standard.board = self.controller.robot_layer.robot.board
        standard.state = state.State()
        serial.cons = self.controller.console
        self.ready = True


class Compile(Command):
    """
    Transpiles the Arduino sketch to python code in a temp python script. 
    """

    def __init__(self, controller):
        super().__init__(controller)
        self.ast = None

    def execute(self):
        try:
            warns, errors, self.ast = transpiler.transpile(self.controller.get_code())
            if len(errors) > 0:
                self.print_errors(errors)
                return False
            elif len(warns) > 0:
                self.print_warnings(warns)
                return True
            return True
        except Exception as e:
            print(f'la excepción es {e}')
            traceback.print_exc()
            logger.error(
                console.Error("Error de compilación", 0, 0, "El sketch no se ha podido compilar correctamente").to_string())

    def compile(self, code):
        try:
            warns, errors, ast = transpiler.transpile(code)
            if len(errors) > 0:
                self.print_errors(errors)
                return None
            elif len(warns) > 0:
                self.print_warnings(warns)
                return ast
            return ast
        except Exception as e:
            print(f'la excepción es {e}')
            traceback.print_exc()
            self.controller.console.write_error(
                console.Error("Error de compilación", 0, 0, "El sketch no se ha podido compilar correctamente"))

    def print_warnings(self, warnings):
        for warning in warnings:
            logger.warning(warning.to_string())

    def print_errors(self, errors):
        for error in errors:
            logger.error(error.to_string())


class Setup(Command):
    """
    Loads the sketch module from the temp python script and executes the setup
    function.
    """

    def __init__(self, controller):
        super().__init__(controller)

    def execute(self):
        global module
        if not self.ready:
            self.prepare_exec()
            _import_module()
        curr_time_ns = time.time_ns()
        if (
                not standard.state.exec_time_us > curr_time_ns / 1000
                and not standard.state.exec_time_ms > curr_time_ns / 1000000
        ):
            try:
                module.setup()
            except Exception:
                self.controller.console.write_error(
                    console.Error("Error de ejecución", 0, 0, "El sketch no se ha podido ejecutar correctamente"))
        return True


class Loop(Command):

    def __init__(self, controller):
        super().__init__(controller)

    def execute(self):
        global module
        if not self.ready:
            self.prepare_exec()
        curr_time_ns = time.time_ns()
        if (
                not standard.state.exec_time_us > curr_time_ns / 1000
                and not standard.state.exec_time_ms > curr_time_ns / 1000000
                and not standard.state.exited and self.controller.executing
        ):
            try:
                module.loop()
            except Exception:
                self.controller.console.write_error(
                    console.Error("Error de ejecución", 0, 0, "El sketch no se ha podido ejecutar correctamente"))
                self.controller.executing = False

class ArduinoCompiler(Arduino):

    def __init__(self, controller, code):
        self.compile_command = Compile(controller)
        self.setup_command = Setup(controller)
        self.loop_command = Loop(controller)
        self.code = code


    @override
    def compile(self):
        self.compile_command.compile(self.code)

    @override
    def check(self) -> bool | None:
        return self.compile_command.execute()

    @override
    def setup(self):
        self.setup_command.execute()

    @override
    def loop(self):
        self.loop_command.execute()
