import unittest
from simulator.interpreter.scanner import Scanner 
from simulator.interpreter.token import TokenType 

class TestScanner(unittest.TestCase):

    def test_tokenizes_left_paren(self):
        scanner = Scanner("(")
        token = next(scanner)
        self.assertIs(token.token, TokenType.LEFT_PAREN)

    def test_scans_integer(self):
        scanner = Scanner("123456")
        token = next(scanner)
        self.assertIs(token.token, TokenType.NUMBER)

    def test_scans_simple_arithmetic(self):
        scanner = Scanner("1 * 2 + 3")
        tokens = [token.token for token in scanner]
        test_tokens = [TokenType.NUMBER, TokenType.STAR, TokenType.NUMBER,
                       TokenType.PLUS, TokenType.NUMBER, TokenType.EOF]
        self.assertEqual(tokens, test_tokens)

    def test_scans_arithmetic_with_parens(self):
        scanner = Scanner("(1 * 2) + 3")
        tokens = [token.token for token in scanner]
        test_tokens = [TokenType.LEFT_PAREN, TokenType.NUMBER, TokenType.STAR,
                       TokenType.NUMBER, TokenType.RIGHT_PAREN,
                       TokenType.PLUS, TokenType.NUMBER, TokenType.EOF]
        self.assertEqual(tokens, test_tokens)

    def test_scans_integer_numbers(self):
        scanner = Scanner("55 + 45")
        literals = [token.literal for token in scanner]
        self.assertEqual(literals[0], 55)
        self.assertEqual(literals[2], 45)

    def test_scans_float_numbers(self):
        scanner = Scanner("5.5 + 4.5")
        literals = [token.literal for token in scanner]
        self.assertEqual(literals[0], 5.5)
        self.assertEqual(literals[2], 4.5)

if __name__ == '__main__':
    unittest.main()
