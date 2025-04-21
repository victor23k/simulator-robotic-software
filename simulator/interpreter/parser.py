import sys
from simulator.interpreter.scanner import Scanner
from simulator.interpreter.token import Token, TokenType
from simulator.interpreter.expr import Expr, BinaryExpr, LiteralExpr
from simulator.interpreter.precedence import PrecLevel, get_binary_op_precedence
from simulator.interpreter.associativity import Assoc, get_binary_op_assoc


class ParseError(Exception):
    """Base class for exceptions raised by the parser."""

    def __init__(self, msg: str, line: int, col: int, text: str):
        self.msg = msg
        self.line = line
        self.col = col
        self.text = text

    # This formatting could be fancier, including the source line and signaling
    # the error part. This is a example from the rust docs:

    # error[E0000]: main error message
    #   --> file.rs:LL:CC
    #    |
    # LL | <code>
    #    | -^^^^- secondary label
    #    |  |
    #    |  primary label
    #    |
    #    = note: note without a `Span`, created with `.note`

    def __str__(self):
        return f"""{self.__class__.__name__}: {self.msg}.
                Ocurred at pos ({self.line}, {self.col}) in:
                {self.text}"""


class Parser:
    """
    This class has a main function to parse Arduino source code into an Abstract
    Syntax Tree (AST).

    Hybrid parser:

    - Recursive descent
    - Pratt parser for expressions
    """

    source: str
    scanner: Scanner
    current: Token
    previous: Token

    def __init__(self, source: str):
        self.source = source
        self.scanner = Scanner(source)
        self.current = None
        self.previous = None
        self._advance()

    def parse(self) -> [Expr]:
        """
        Parses the source string into an AST.
        """

        expr = self._parse_binary_expr(PrecLevel.MINIMAL)
        return [expr]

    def _parse_binary_expr(self, min_prec: PrecLevel) -> Expr:
        # precedence climbing algorithm from https://eli.thegreenplace.net/2012/08/02/parsing-expressions-by-precedence-climbing
        lhs = self._parse_atom()
        curr_token_prec = get_binary_op_precedence(self._peek().token)

        while self._peek().is_binary() and curr_token_prec >= min_prec:
            op = self.current
            assoc = get_binary_op_assoc(op)
            next_min_prec = min_prec + 1 if assoc is Assoc.LEFT else min_prec

            self._advance()
            rhs = self._parse_binary_expr(next_min_prec)
            lhs = BinaryExpr(lhs, op, rhs)

        return lhs

    def _parse_atom(self) -> Expr:
        match self._peek():
            case Token(token=TokenType.LEFT_PAREN):
                self._advance()
                expr = self._parse_binary_expr(PrecLevel.MINIMAL)
                self._consume(TokenType.RIGHT_PAREN, "Unmatched '('")
                return expr
            case Token(token=TokenType.NUMBER):
                self._advance()
                return LiteralExpr(self.previous.literal)
            case Token(token=tt) if tt in [TokenType.STAR]:
                self._advance()
                self._error(
                    self.previous, "Expected number or expression inside parens."
                )

    def _consume(self, token_type: TokenType, message: str) -> Token:
        if self._check(token_type):
            return self._advance()
        raise ParseError(message)

    def _match(self, *token_types: TokenType) -> bool:
        for token_type in token_types:
            if self._check(token_type):
                self._advance()
                return True

        return False

    def _check(self, token_type: TokenType) -> bool:
        return self._peek().token == token_type

    def _is_at_end(self) -> bool:
        return self._peek().token == TokenType.EOF

    def _peek(self) -> Token:
        return self.current

    def _advance(self):
        self.previous = self.current
        self.current = next(self.scanner)

    def _error(self, token: Token, message: str):
        # This should generate a Diagnostic, report it to the interpreter and
        # return an exception to be raised
        print(message, file=sys.stderr)
