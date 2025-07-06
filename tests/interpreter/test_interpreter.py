import unittest

from simulator.interpreter.diagnostic import Diagnostic
from simulator.interpreter.interpreter import Interpreter
from simulator.interpreter.parse.parser import Parser
from simulator.interpreter.sema.resolver import Resolver
from simulator.interpreter.sema.types import ArduinoBuiltinType

def run(code: str) -> Interpreter:
    parser = Parser(code, [])
    statements = parser.parse()
    interpreter = Interpreter([])
    resolver = Resolver([])
    resolver.resolve(statements)
    interpreter.run(statements)

    return interpreter

class TestInterpreter(unittest.TestCase):
    def test_interprets_simple_arithmetic(self):
        code = "float a = 5 - 4 / 2;"
        interpreter = run(code)

        a_value = interpreter.environment.get("a", 0)

        assert a_value is not None
        self.assertEqual(a_value.value, 3.0)
        self.assertEqual(a_value.value_type, ArduinoBuiltinType.FLOAT)


    def test_interprets_complex_arithmetic(self):
        code = "float a = 1 * (5 - 24 % (10 - 3)) / 10;"
        interpreter = run(code)

        a_value = interpreter.environment.get("a", 0)

        assert a_value is not None
        should_be = 1 * (5 - 24 % (10 - 3)) / 10
        self.assertEqual(a_value.value, should_be)
        self.assertEqual(a_value.value_type, ArduinoBuiltinType.FLOAT)

    def test_interprets_assignment_and_usage(self):
        code = "int a = 2;\nint b;\nb = a + 3;"
        interpreter = run(code)

        b_value = interpreter.environment.get("b", 0)

        assert b_value is not None
        self.assertEqual(b_value.value, 5)
        self.assertEqual(b_value.value_type, ArduinoBuiltinType.INT)

    def test_interprets_binary_op_plus(self):
        code = "int a = 4 + 2;"
        interpreter = run(code)

        a_value = interpreter.environment.get("a", 0)

        assert a_value is not None
        self.assertEqual(a_value.value, 6)
        self.assertEqual(a_value.value_type, ArduinoBuiltinType.INT)

    def test_interprets_binary_op_plus_float_coerce_var(self):
        code = "float a = 4 + 2;"
        interpreter = run(code)

        val = interpreter.environment.get("a", 0)

        assert val is not None
        self.assertEqual(val.value, 6.0)
        self.assertEqual(val.value_type, ArduinoBuiltinType.FLOAT)

    def test_interprets_binary_op_plus_float_coerce(self):
        code = "float a = 4.0 + 2;"
        interpreter = run(code)

        val = interpreter.environment.get("a", 0)

        assert val is not None
        self.assertEqual(val.value, 6.0)
        self.assertEqual(val.value_type, ArduinoBuiltinType.FLOAT)

    def test_interprets_binary_op_plus_float(self):
        code = "float a = 4.0 + 2.0;"
        interpreter = run(code)

        val = interpreter.environment.get("a", 0)

        assert val is not None
        self.assertEqual(val.value, 6.0)
        self.assertEqual(val.value_type, ArduinoBuiltinType.FLOAT)

    def test_interprets_comparisons(self):
        code = "bool a = 5 == 6;\nbool b = 5 != 6;"
        interpreter = run(code)

        a_value = interpreter.environment.get("a", 0)

        assert a_value is not None
        self.assertEqual(a_value.value, False)
        self.assertEqual(a_value.value_type, ArduinoBuiltinType.BOOL)

        b_value = interpreter.environment.get("b", 0)

        assert b_value is not None
        self.assertEqual(b_value.value, True)
        self.assertEqual(b_value.value_type, ArduinoBuiltinType.BOOL)

    def test_interprets_nested_blocks(self):
        code = """int a = 7;
int b = 0;
int c = 0;
{
    a = 3;
    b = a + 1;
    {
        c = b + 5;
    }
}"""

        interpreter = run(code)

        val_a = interpreter.environment.get("a", 0)
        val_b = interpreter.environment.get("b", 0)
        val_c = interpreter.environment.get("c", 0)

        assert val_a is not None
        self.assertEqual(val_a.value, 3)
        assert val_b is not None
        self.assertEqual(val_b.value, 4)
        assert val_c is not None
        self.assertEqual(val_c.value, 9)


if __name__ == "__main__":
    unittest.main()
