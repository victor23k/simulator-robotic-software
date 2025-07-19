from abc import ABC, abstractmethod


class Arduino(ABC):
    """
    Functions to interact with an Arduino sketch program.
    """

    @abstractmethod
    def compile(self):
        """
        Compiles the Arduino sketch and returns the final representation.

        In this project compilation can mean transpilation, error checking or real
        compilation to a binary.
        """

        pass

    @abstractmethod
    def check(self) -> bool | None:
        """
        Checks errors on the Arduino sketch
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
