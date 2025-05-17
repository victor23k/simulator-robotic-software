import unittest
from simulator.interpreter.interpreter import Interpreter
from simulator.interpreter.parser import Parser
from simulator.interpreter.resolver import Resolver


class TestInterpreter(unittest.TestCase):
    def test_interprets_simple_arithmetic(self):
        diags = []
        parser = Parser("5 - 4 / 2;", diags)
        statements = parser.parse()
        interpreter = Interpreter(statements, diags)
        a = interpreter.run()

        self.assertEqual(a, 3.0)


    def test_interprets_complex_arithmetic(self):
        diags = []
        parser = Parser("1 * (5 - 24 % (10 - 3)) / 10;", diags)
        statements = parser.parse()
        interpreter = Interpreter(statements, diags)
        a = interpreter.run()

        should_be = 1 * (5 - 24 % (10 - 3)) / 10
        self.assertEqual(a, should_be)

    def test_interprets_assignment_and_usage(self):
        diags = []
        parser = Parser("int a = 2;\nint b;\nb = a + 3;", diags)
        statements = parser.parse()
        interpreter = Interpreter(statements, diags)
        resolver = Resolver(interpreter)
        resolver.resolve(statements)
        interpreter.run()

        print(diags)


if __name__ == "__main__":
    unittest.main()
