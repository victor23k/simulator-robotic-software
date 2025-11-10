import unittest

from simulator.interpreter.lex.scanner import Scanner
from simulator.interpreter.lex.token import TokenType


class TestScanner(unittest.TestCase):
    def test_tokenizes_left_paren(self):
        scanner = Scanner("(")
        token = next(scanner)
        self.assertIs(token.token, TokenType.LEFT_PAREN)

    def test_scans_integer(self):
        scanner = Scanner("123456")
        token = next(scanner)
        self.assertIs(token.token, TokenType.INT_LITERAL)

    def test_scans_simple_arithmetic(self):
        scanner = Scanner("1 * 2 + 3")
        tokens = [token.token for token in scanner]
        test_tokens = [
            TokenType.INT_LITERAL,
            TokenType.STAR,
            TokenType.INT_LITERAL,
            TokenType.PLUS,
            TokenType.INT_LITERAL,
            TokenType.EOF,
        ]
        self.assertEqual(tokens, test_tokens)

    def test_scans_arithmetic_with_parens(self):
        scanner = Scanner("(1 * 2) + 3")
        tokens = [token.token for token in scanner]
        test_tokens = [
            TokenType.LEFT_PAREN,
            TokenType.INT_LITERAL,
            TokenType.STAR,
            TokenType.INT_LITERAL,
            TokenType.RIGHT_PAREN,
            TokenType.PLUS,
            TokenType.INT_LITERAL,
            TokenType.EOF,
        ]
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

    def test_scans_edge_float_numbers(self):
        scanner = Scanner("0.5 + 0 + 1.5")
        literals = [token.literal for token in scanner]
        self.assertEqual(literals[0], 0.5)
        self.assertEqual(literals[2], 0)
        self.assertEqual(literals[4], 1.5)

    def test_scans_upper_hex_constants(self):
        scanner = Scanner("0xB2B + 0xC1")
        tokens = [token for token in scanner]
        self.assertEqual(tokens[0].literal, int("0xB2B", 16))
        self.assertEqual(tokens[2].literal, int("0xC1", 16))
        self.assertEqual(tokens[0].token, TokenType.INT_LITERAL)
        self.assertEqual(tokens[2].token, TokenType.INT_LITERAL)

    def test_scans_lower_hex_constants(self):
        scanner = Scanner("0xb2b + 0xc1")
        tokens = [token for token in scanner]
        self.assertEqual(tokens[0].literal, int("0xb2b", 16))
        self.assertEqual(tokens[2].literal, int("0xc1", 16))
        self.assertEqual(tokens[0].token, TokenType.INT_LITERAL)
        self.assertEqual(tokens[2].token, TokenType.INT_LITERAL)

    def test_scans_octal_constants(self):
        scanner = Scanner("0173 + 032")
        tokens = [token for token in scanner]
        self.assertEqual(tokens[0].literal, int("0173", 8))
        self.assertEqual(tokens[2].literal, int("032", 8))
        self.assertEqual(tokens[0].token, TokenType.INT_LITERAL)
        self.assertEqual(tokens[2].token, TokenType.INT_LITERAL)

    def test_scans_binary_constants(self):
        scanner = Scanner("0b101 + 0b1100")
        tokens = [token for token in scanner]
        self.assertEqual(tokens[0].literal, 5)
        self.assertEqual(tokens[2].literal, 12)
        self.assertEqual(tokens[0].token, TokenType.INT_LITERAL)
        self.assertEqual(tokens[2].token, TokenType.INT_LITERAL)

    def test_scans_positive_scientific_notation_upper_float(self):
        scanner = Scanner("2.34E5")
        token = next(scanner)
        self.assertEqual(token.literal, 234000)

    def test_scans_positive_scientific_notation_lower_float(self):
        scanner = Scanner("5.344e5")
        token = next(scanner)
        self.assertEqual(token.literal, 534400)

    def test_scans_positive_scientific_notation_upper(self):
        scanner = Scanner("2E7")
        token = next(scanner)
        self.assertEqual(token.literal, 20000000)

    def test_scans_positive_scientific_notation_lower(self):
        scanner = Scanner("5e5")
        token = next(scanner)
        self.assertEqual(token.literal, 500000)

    def test_scans_negative_scientific_notation_upper(self):
        scanner = Scanner("67E-3")
        token = next(scanner)
        self.assertEqual(token.literal, 0.067)

    def test_scans_negative_scientific_notation_lower(self):
        scanner = Scanner("67e-3")
        token = next(scanner)
        self.assertEqual(token.literal, 0.067)

    def test_scans_negative_scientific_notation_lower_float(self):
        scanner = Scanner("4.7e-3")
        token = next(scanner)
        self.assertEqual(token.literal, 0.0047)

    def test_scans_negative_scientific_notation_upper_float(self):
        scanner = Scanner("4.7E-3")
        token = next(scanner)
        self.assertEqual(token.literal, 0.0047)

    def test_adds_diagnostic_for_malformed_binary_constant(self):
        scanner = Scanner("1 + 0b * 2")
        [token for token in scanner]
        self.assertNotEqual(scanner.diagnostics, [])

    def test_adds_diagnostic_for_malformed_hex_constant(self):
        scanner = Scanner("1 + 0xZ89 * 2")
        [token for token in scanner]
        self.assertNotEqual(scanner.diagnostics, [])

    def test_scans_simple_declaration(self):
        scanner = Scanner("int num;")
        self.assertIs(TokenType.INT, next(scanner).token)
        ident = next(scanner)
        self.assertIs(TokenType.IDENTIFIER, ident.token)
        self.assertEqual("num", ident.literal)
        self.assertIs(TokenType.SEMICOLON, next(scanner).token)

    def test_scans_declaration_with_assignment(self):
        scanner = Scanner("int a = 2;")
        self.assertIs(TokenType.INT, next(scanner).token)
        ident = next(scanner)
        self.assertIs(TokenType.IDENTIFIER, ident.token)
        self.assertEqual("a", ident.literal)
        self.assertIs(TokenType.EQUAL, next(scanner).token)
        num = next(scanner)
        self.assertIs(TokenType.INT_LITERAL, num.token)
        self.assertIs(2, num.literal)

    def test_scans_assignment_and_usage(self):
        scanner = Scanner("int a = 2;\na;")
        tokens = [token for token in scanner]
        # pprint(tokens)


if __name__ == "__main__":
    unittest.main()
