import unittest

from simulator.interpreter.environment import Value
from simulator.interpreter.interpreter import Interpreter
from simulator.interpreter.sema.types import ArduinoBuiltinType

def run(code: str) -> Interpreter:
    interpreter = Interpreter(code)
    interpreter.compile(None, None)
    interpreter.run_test()

    return interpreter

class TestAstInterpreter(unittest.TestCase):
    def test_interprets_simple_arithmetic(self):
        code = "float a = 5 - 4 / 2;"
        interpreter = run(code)

        a_value = interpreter.environment.get("a", 0)

        assert isinstance(a_value, Value)
        self.assertEqual(a_value.value, 3.0)
        self.assertEqual(a_value.value_type, ArduinoBuiltinType.FLOAT)


    def test_interprets_complex_arithmetic(self):
        code = "float a = 1 * (5 - 24 % (10 - 3)) / 10;"
        interpreter = run(code)

        a_value = interpreter.environment.get("a", 0)

        assert isinstance(a_value, Value)
        should_be = 1 * (5 - 24 % (10 - 3)) / 10
        self.assertEqual(a_value.value, should_be)
        self.assertEqual(a_value.value_type, ArduinoBuiltinType.FLOAT)

    def test_interprets_assignment_and_usage(self):
        code = "int a = 2;\nint b;\nb = a + 3;"
        interpreter = run(code)

        b_value = interpreter.environment.get("b", 0)

        assert isinstance(b_value, Value)
        self.assertEqual(b_value.value, 5)
        self.assertEqual(b_value.value_type, ArduinoBuiltinType.INT)

    def test_interprets_binary_op_plus(self):
        code = "int a = 4 + 2;"
        interpreter = run(code)

        a_value = interpreter.environment.get("a", 0)

        assert isinstance(a_value, Value)
        self.assertEqual(a_value.value, 6)
        self.assertEqual(a_value.value_type, ArduinoBuiltinType.INT)

    def test_interprets_binary_op_plus_float_coerce_var(self):
        code = "float a = 4 + 2;"
        interpreter = run(code)

        val = interpreter.environment.get("a", 0)

        assert isinstance(val, Value)
        self.assertEqual(val.value, 6.0)
        self.assertEqual(val.value_type, ArduinoBuiltinType.FLOAT)

    def test_interprets_binary_op_plus_float_coerce(self):
        code = "float a = 4.0 + 2;"
        interpreter = run(code)

        val = interpreter.environment.get("a", 0)

        assert isinstance(val, Value)
        self.assertEqual(val.value, 6.0)
        self.assertEqual(val.value_type, ArduinoBuiltinType.FLOAT)

    def test_interprets_binary_op_plus_float(self):
        code = "float a = 4.0 + 2.0;"
        interpreter = run(code)

        val = interpreter.environment.get("a", 0)

        assert isinstance(val, Value)
        self.assertEqual(val.value, 6.0)
        self.assertEqual(val.value_type, ArduinoBuiltinType.FLOAT)

    def test_interprets_comparisons(self):
        code = "bool a = 5 == 6;\nbool b = 5 != 6;"
        interpreter = run(code)

        a_value = interpreter.environment.get("a", 0)

        assert isinstance(a_value, Value)
        self.assertEqual(a_value.value, False)
        self.assertEqual(a_value.value_type, ArduinoBuiltinType.BOOL)

        b_value = interpreter.environment.get("b", 0)

        assert isinstance(b_value, Value)
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


    def test_interprets_if_statement(self):
        code = """int a = 7;
int b = 0;
if (a > b) {
    b = 3;
} else {
    b = b + 5;
}"""

        interpreter = run(code)

        val_b = interpreter.environment.get("b", 0)

        assert isinstance(val_b, Value)
        self.assertEqual(val_b.value, 3)


    def test_interprets_if_else_if_statement(self):
        code = """int a = 4;
int b = 8;
int c = 5;
int res = 0;

if (a > b && a > c) {
    res = a;
} else if (b > c) {
    res = b;
} else {
    res = c;
}"""

        interpreter = run(code)

        val_res = interpreter.environment.get("res", 0)

        assert isinstance(val_res, Value)
        self.assertEqual(val_res.value, 8)

    def test_interprets_switch_case_statement(self):
        code = """int classify(int x) {
  switch (x) {
    case 1:
      return 10;
      break;
    case 2:
      return 20;
      break;
    default:
      return 0;
      break;
  }
}

int result_ten = classify(1);
int result_twenty = classify(2);
int result_default = classify(5);"""

        interpreter = run(code)

        val_res10 = interpreter.environment.get("result_ten", 0)
        val_res20 = interpreter.environment.get("result_twenty", 0)
        val_resdef = interpreter.environment.get("result_default", 0)

        assert isinstance(val_res10, Value)
        self.assertEqual(val_res10.value, 10)
        assert isinstance(val_res20, Value)
        self.assertEqual(val_res20.value, 20)
        assert isinstance(val_resdef, Value)
        self.assertEqual(val_resdef.value, 0)


    def test_interprets_decrement_and_increment_postfix(self):
        code = """int x = 5;
int y = 5;
int a = x++; int b = y--;"""

        interpreter = run(code)

        val_x = interpreter.environment.get("x", 0)
        val_y = interpreter.environment.get("y", 0)
        val_a = interpreter.environment.get("a", 0)
        val_b = interpreter.environment.get("b", 0)

        assert isinstance(val_x, Value)
        self.assertEqual(val_x.value, 6)
        assert isinstance(val_y, Value)
        self.assertEqual(val_y.value, 4)

        assert isinstance(val_a, Value)
        self.assertEqual(val_a.value, 5)
        assert isinstance(val_b, Value)
        self.assertEqual(val_b.value, 5)

    def test_interprets_decrement_and_increment_prefix(self):
        code = """int x = 5;
int y = 5;
int a = ++x; int b = --y;"""

        interpreter = run(code)

        val_x = interpreter.environment.get("x", 0)
        val_y = interpreter.environment.get("y", 0)
        val_a = interpreter.environment.get("a", 0)
        val_b = interpreter.environment.get("b", 0)

        assert isinstance(val_x, Value)
        self.assertEqual(val_x.value, 6)
        assert isinstance(val_y, Value)
        self.assertEqual(val_y.value, 4)

        assert isinstance(val_a, Value)
        self.assertEqual(val_a.value, 6)
        assert isinstance(val_b, Value)
        self.assertEqual(val_b.value, 4)


    def test_interprets_compound_arithmetic_assignment(self):
        code = """int x = 5;
x += 15 * 10;
int y = 20;
y -= 10;
int z = 20;
z /= 10;
int a = 20;
a %= 15;
int b = 10;
b *= 3;
"""

        interpreter = run(code)

        val_x = interpreter.environment.get("x", 0)
        val_y = interpreter.environment.get("y", 0)
        val_z = interpreter.environment.get("z", 0)
        val_a = interpreter.environment.get("a", 0)
        val_b = interpreter.environment.get("b", 0)

        assert isinstance(val_x, Value)
        self.assertEqual(val_x.value, 155)
        assert isinstance(val_y, Value)
        self.assertEqual(val_y.value, 10)
        assert isinstance(val_z, Value)
        self.assertEqual(val_z.value, 2)
        assert isinstance(val_a, Value)
        self.assertEqual(val_a.value, 5)
        assert isinstance(val_b, Value)
        self.assertEqual(val_b.value, 30)

if __name__ == "__main__":
    unittest.main()
