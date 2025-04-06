import unittest
from simulator.interpreter.scanner import Scanner 
from simulator.interpreter.token import TokenType 

class TestScanner(unittest.TestCase):

    def test_tokenizes_left_paren(self):
        scanner = Scanner("(")
        scanner.next_token()
        token = scanner.tokens[-1]
        self.assertIs(token.token, TokenType.LEFT_PAREN)

    def test_scans_integer(self):
        scanner = Scanner("123456")
        scanner.next_token()
        token = scanner.tokens[-1]
        self.assertIs(token.token, TokenType.INT)


if __name__ == '__main__':
    unittest.main()
