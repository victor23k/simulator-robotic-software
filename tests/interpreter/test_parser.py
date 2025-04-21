import unittest
from simulator.interpreter.parser import Parser
from simulator.interpreter.token import Token, TokenType
from simulator.interpreter.expr import BinaryExpr, LiteralExpr


class TestParser(unittest.TestCase):
    def test_parses_complex_arithmetic_expression(self):
        parser = Parser("1 * (5 - 4 % (10 - 3)) / 10")
        [expr] = parser.parse()
        match expr:
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


if __name__ == "__main__":
    unittest.main()
