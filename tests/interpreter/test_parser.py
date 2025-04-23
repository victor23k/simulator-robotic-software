import unittest
from simulator.interpreter.parser import Parser
from simulator.interpreter.token import Token, TokenType
from simulator.interpreter.expr import BinaryExpr, LiteralExpr
from simulator.interpreter.stmt import Stmt, VariableStmt


class TestParser(unittest.TestCase):
    def test_parses_complex_arithmetic_expression(self):
        parser = Parser("1 * (5 - 4 % (10 - 3)) / 10;")
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
        parser = Parser("int num;")
        statements = parser.parse()
        self.assertIsInstance(statements[0], VariableStmt)
        self.assertEqual(statements[0].var_type.token, TokenType.INT)
        self.assertEqual(statements[0].name.literal, "num")
        self.assertIsNone(statements[0].initializer)

    def test_parses_declaration_with_initialization(self):
        parser = Parser("int num = 4;")
        statements = parser.parse()
        self.assertIsInstance(statements[0], VariableStmt)
        self.assertEqual(statements[0].var_type.token, TokenType.INT)
        self.assertEqual(statements[0].name.literal, "num")
        self.assertIsInstance(statements[0].initializer, LiteralExpr)
        self.assertEqual(statements[0].initializer.value, 4)


if __name__ == "__main__":
    unittest.main()
