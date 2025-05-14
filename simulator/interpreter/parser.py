from simulator.interpreter.associativity import Assoc, get_binary_op_assoc
from simulator.interpreter.expr import Expr, BinaryExpr, LiteralExpr, VariableExpr
from simulator.interpreter.diagnostic import Diagnostic
from simulator.interpreter.precedence import PrecLevel, get_binary_op_precedence
from simulator.interpreter.scanner import Scanner
from simulator.interpreter.stmt import ExpressionStmt, Stmt, VariableStmt
from simulator.interpreter.token import Token, TokenType

from typing import override

class ParseError():
    """Base class for exceptions raised by the parser."""
    msg: str
    line: int
    col: int
    text: str

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

    @override
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
    diagnostics: list[Diagnostic]

    def __init__(self, source: str, diagnostics: list[Diagnostic]):
        self.source = source
        self.scanner = Scanner(source)
        self.diagnostics = diagnostics
        self.current = Token(TokenType.EOF, "", None, 0, 0)
        self._advance()

    def parse(self) -> list[Stmt]:
        """
        Parses the source string into an AST that takes the form of a list of
        statements.
        """

        statements: list[Stmt] = []

        while not self._is_at_end():
            stmt = self._statement()
            statements.append(stmt)

        return statements

    def _statement(self) -> Stmt:
        match self._peek().token:
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
        var_type = self._advance()
        identifier = self._consume(
            TokenType.IDENTIFIER, "Expect identifier in variable declaration."
        )
        initializer = None

        # if left square bracket, this is an array
        if self._match(TokenType.LEFT_BRACKET):
            _number = self._consume(
                TokenType.NUMBER, "Expect number constant in array declaration."
            )
            self._consume(
                TokenType.RIGHT_BRACKET, "Expect closing ']' in array declaration."
            )
            # don't know what to do with this yet

        # if equals, we are initializing the variable
        if self._match(TokenType.EQUAL):
            initializer = self._expression()

        self._consume(TokenType.SEMICOLON, "Expect ';' after declaration.")

        return VariableStmt(var_type, identifier, initializer)

    def _expression_statement(self) -> ExpressionStmt:
        expr = self._expression()
        self._consume(TokenType.SEMICOLON, "Expect ';' after expression.")
        stmt = ExpressionStmt(expr)
        return stmt

    def _expression(self, min_prec: PrecLevel = PrecLevel.MINIMAL) -> Expr:
        match self._peek():
            case Token(token=TokenType.IDENTIFIER) as name:
                self._advance()
                return VariableExpr(name)
            case Token(token=TokenType.INT_LITERAL) as num:
                self._advance()
                return LiteralExpr(num)
            case _:
                return self._parse_binary_expr(min_prec)

    def _parse_binary_expr(self, min_prec: PrecLevel) -> Expr:
        # precedence climbing algorithm from https://eli.thegreenplace.net/2012/08/02/parsing-expressions-by-precedence-climbing
        lhs = self._parse_atom()
        curr_token_prec = get_binary_op_precedence(self._peek().token)

        while self._peek().is_binary() and curr_token_prec >= min_prec:
            op = self.current
            assoc = get_binary_op_assoc(op.token)
            next_min_prec = min_prec + 1 if assoc is Assoc.LEFT else min_prec

            self._advance()
            rhs = self._expression(next_min_prec)
            lhs = BinaryExpr(lhs, op, rhs)

        return lhs

    def _parse_atom(self) -> Expr:
        match self._peek():
            case Token(token=TokenType.LEFT_PAREN):
                self._advance()
                expr = self._expression(PrecLevel.MINIMAL)
                self._consume(TokenType.RIGHT_PAREN, "Unmatched '('")
                return expr
            case Token(token=TokenType.INT_LITERAL | TokenType.FLOAT_LITERAL) as token:
                self._advance()
                return LiteralExpr(token)
            case Token(token=TokenType.IDENTIFIER) as token:
                self._advance()
                return VariableExpr(token)
            case unexpected_token:
                self._advance()
                self._error(
                    unexpected_token, "Expected number or expression inside parens."
                )
                return LiteralExpr(unexpected_token)

    def _consume(self, token_type: TokenType, message: str) -> Token:
        if not self._check(token_type):

            diag = Diagnostic(message, self.current.line, self.current.column,
                        len(self.current.lexeme) + self.current.column)
            self.diagnostics.append(diag)

        return self._advance()

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
        # return it        
        
        diag = Diagnostic(message, token.line, token.column, token.column +
            len(token.lexeme))
        self.diagnostics.append(diag)
