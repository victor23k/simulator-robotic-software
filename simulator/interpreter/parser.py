import sys
from simulator.interpreter.scanner import Scanner
from simulator.interpreter.token import Token, TokenType
from simulator.interpreter.expr import Expr, BinaryExpr, LiteralExpr
from simulator.interpreter.precedence import PrecLevel, get_binary_op_precedence
from simulator.interpreter.associativity import Assoc, get_binary_op_assoc
from simulator.interpreter.stmt import ExpressionStmt, Stmt, VariableStmt


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
        Parses the source string into an AST that takes the form of a list of
        statements.
        """

        statements = []

        while not self._is_at_end():
            statements.append(self._statement())

        return statements

    def _statement(self) -> Stmt:
        next_token = self._advance()
        match next_token.token:
            # var type, must be a declaration
            case (
                TokenType.BOOL
                | TokenType.BOOLEAN
                | TokenType.BYTE
                | TokenType.CHAR
                | TokenType.DOUBLE
                | TokenType.FLOAT
                | TokenType.INT
                | TokenType.LONG
                | TokenType.SHORT
                | TokenType.SIZE_T
                | TokenType.UNSIGNED_INT
                | TokenType.WORD
                | TokenType.UNSIGNED_CHAR
                | TokenType.UNSIGNED_LONG
            ):
                return self._declaration()
            case _:
                return self._expression_statement()

    def _declaration(self) -> VariableStmt:
        var_type = self.previous
        identifier = self._consume(
            TokenType.IDENTIFIER, "Expect identifier in variable declaration."
        )
        initializer = None

        # if left square bracket, this is an array
        if self._check(TokenType.LEFT_BRACKET):
            self._advance()
            _number = self._check(
                TokenType.NUMBER, "Expect number constant in array declaration."
            )
            self._check(
                TokenType.RIGHT_BRACKET, "Expect closing ']' in array declaration."
            )
            # don't know what to do with this yet

        # if equals, we are initializing the variable
        if self._check(TokenType.EQUAL):
            self._advance()
            initializer = self._expression()

        self._consume(TokenType.SEMICOLON, "Expect ';' after declaration.")
        return VariableStmt(var_type, identifier, initializer)

    def _expression_statement(self) -> ExpressionStmt:
        expr = self._expression()
        self._consume(TokenType.SEMICOLON, "Expect ';' after expression.")
        stmt = ExpressionStmt(expr)
        return stmt

    def _expression(self):
        return self._parse_binary_expr(PrecLevel.MINIMAL)

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
        raise ParseError(message, self.current.line, self.current.column, self.source)

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
        return self.previous

    def _error(self, token: Token, message: str):
        # This should generate a Diagnostic, report it to the interpreter and
        # return an exception to be raised
        print(message, file=sys.stderr)
