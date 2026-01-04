from abc import ABC, abstractmethod

from simulator.interpreter.debugger.adb import Debugger


class Arduino(ABC):
    """
    Functions to interact with an Arduino sketch program.
    """
    
    valid: bool

    @abstractmethod
    def compile(self, console, board) -> bool:
        """
        Compiles the Arduino sketch to the executable intermediate
        representation and sets up the standard library. Returns if the
        compilation completed successfully.

        In this project compilation can mean transpilation, creating the AST or
        real compilation to a binary.
        """

        pass

    @abstractmethod
    def check(self) -> bool | None:
        """
        Once the Arduino sketch is compiled, returns if the sketch compiled
        without errors. 
        """

        pass

    @abstractmethod
    def setup(self):
        """
        Executes the Arduino sketch `setup()` function.
        """

        pass

    @abstractmethod
    def loop(self):
        """
        Executes the Arduino sketch `loop()` function.
        """

        pass

    @abstractmethod
    def debug(self, loop_callback) -> Debugger: 
        """
        Creates a Debugger ready for execution controlled by the user.
        """

        pass

    def run(self):
        """
        Run Arduino sketch.
        """
        
        self.setup()
        self.loop()
