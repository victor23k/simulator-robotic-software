import unittest
from simulator.interpreter.diagnostic import Diagnostic
from simulator.interpreter.interpreter import Interpreter
from simulator.interpreter.parser import Parser
from simulator.interpreter.resolver import Resolver
from simulator.interpreter.types import ArduinoBuiltinType

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

    def test_interprets_binary_op_plus(self):
        code = "int a = 4 + 2;"
        diags: list[Diagnostic] = []
        parser = Parser(code, diags)
        statements = parser.parse()
        interpreter = Interpreter(statements, diags)
        resolver = Resolver(interpreter)
        resolver.resolve(statements)
        interpreter.run()
        a_value = interpreter.environment.get("a", 0)

        assert a_value is not None
        self.assertEqual(a_value.value, 6)
        self.assertEqual(a_value.value_type, ArduinoBuiltinType.INT)

    def test_interprets_binary_op_plus_float(self):
        code = """
        float a = 4 + 2;
        float b = 4.0 + 2;
        float c = 4.0 + 2.0;
        """
        diags: list[Diagnostic] = []
        parser = Parser(code, diags)
        statements = parser.parse()
        interpreter = Interpreter(statements, diags)
        resolver = Resolver(interpreter)
        resolver.resolve(statements)
        interpreter.run()

        for varname in ["a", "b", "c"]:
            val = interpreter.environment.get(varname, 0)

            assert val is not None
            self.assertEqual(val.value, 6.0)
            self.assertEqual(val.value_type, ArduinoBuiltinType.FLOAT)

    def test_interprets_comparisons(self):
        code = """
        bool a = 5 == 6;
        bool b = 5 != 6;
        """

        diags: list[Diagnostic] = []
        parser = Parser(code, diags)
        statements = parser.parse()
        interpreter = Interpreter(statements, diags)
        resolver = Resolver(interpreter)
        resolver.resolve(statements)
        interpreter.run()

        a_value = interpreter.environment.get("a", 0)

        assert a_value is not None
        self.assertEqual(a_value.value, False)
        self.assertEqual(a_value.value_type, ArduinoBuiltinType.BOOL)

        b_value = interpreter.environment.get("b", 0)

        assert b_value is not None
        self.assertEqual(b_value.value, True)
        self.assertEqual(b_value.value_type, ArduinoBuiltinType.BOOL)


if __name__ == "__main__":
    unittest.main()
