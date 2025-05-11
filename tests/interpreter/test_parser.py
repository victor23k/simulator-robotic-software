import unittest
from typing import cast

from simulator.interpreter.parser import Parser
from simulator.interpreter.token import Token, TokenType
from simulator.interpreter.expr import BinaryExpr, LiteralExpr
from simulator.interpreter.stmt import VariableStmt


class TestParser(unittest.TestCase):
    def test_parses_complex_arithmetic_expression(self):
        parser = Parser("1 * (5 - 4 % (10 - 3)) / 10;", [])
        statements = parser.parse()
        match statements[0].expr:
            case BinaryExpr(
                op=Token(token=TokenType.STAR),
                lhs=LiteralExpr(value=1),
                rhs=BinaryExpr(
                    op=Token(token=TokenType.SLASH),
                    lhs=BinaryExpr(
                        op=Token(token=TokenType.MINUS),
                        lhs=LiteralExpr(value=5),
                        rhs=BinaryExpr(
                            op=Token(token=TokenType.PERCENTAGE),
                            lhs=LiteralExpr(value=4),
                            rhs=BinaryExpr(
                                op=Token(token=TokenType.MINUS),
                                lhs=LiteralExpr(value=10),
                                rhs=LiteralExpr(value=3),
                            ),
                        ),
                    ),
                    rhs=LiteralExpr(value=10),
                ),
            ):
                self.assertTrue(True)
            case _:
                self.assertTrue(False)

    def test_parses_declaration(self):
        parser = Parser("int num;", [])
        statements = parser.parse()
        self.assertIsInstance(statements[0], VariableStmt)
        var_stmt = cast(VariableStmt, statements[0])
        self.assertEqual(var_stmt.var_type.token, TokenType.INT)
        self.assertEqual(var_stmt.name.literal, "num")
        self.assertIsNone(var_stmt.initializer)

    def test_parses_declaration_with_initialization(self):
        parser = Parser("int num = 4;", [])
        statements = parser.parse()
        self.assertIsInstance(statements[0], VariableStmt)
        var_stmt = cast(VariableStmt, statements[0])
        self.assertEqual(var_stmt.var_type.token, TokenType.INT)
        self.assertEqual(var_stmt.name.literal, "num")
        self.assertIsInstance(var_stmt.initializer, LiteralExpr)
        self.assertEqual(cast(LiteralExpr, var_stmt.initializer).value.literal, 4)

    def test_parses_assignment_and_expression(self):
        parser = Parser("int a = 2;\nint b = a + 3;", [])


if __name__ == "__main__":
    unittest.main()
