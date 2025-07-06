import sys

from simulator.interpreter.diagnostic import Diagnostic
from simulator.interpreter.interpreter import Interpreter
from simulator.interpreter.parse.parser import Parser
from simulator.interpreter.sema.resolver import Resolver

class Arduino:
    """
    Arduino sketch interpreter.
    """

    code: str
    parser: Parser
    diagnostics: list[Diagnostic]
    resolver: Resolver
    interpreter: Interpreter

    def __init__(self, code: str):
        self.code = code
        self.diagnostics = []
        self.parser = Parser(code, self.diagnostics)
        self.resolver = Resolver(self.diagnostics)
        self.interpreter = Interpreter(self.diagnostics)

    def run(self):
        """
        Interprets the loaded Arduino sketch. 

        If there are any errors before execution, prints them to standard error
        output and exits.
        """

        statements = self.parser.parse()
        self.resolver.resolve(statements)

        if len(self.diagnostics) == 0:
            self.interpreter.run(statements)
        else:
            print(self.diagnostics, file=sys.stderr)
        

    def check_program(self) -> bool:
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


