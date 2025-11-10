from simulator.interpreter.parse.associativity import Assoc, get_binary_op_assoc
from simulator.interpreter.ast.expr import (
    AssignExpr,
    CallExpr,
    Expr,
    BinaryExpr,
    LiteralExpr,
    UnaryExpr,
    VariableExpr,
)
from simulator.interpreter.diagnostic import Diagnostic
from simulator.interpreter.parse.precedence import PrecLevel, get_binary_op_precedence
from simulator.interpreter.lex.scanner import Scanner
from simulator.interpreter.ast.stmt import (
    BlockStmt,
    BreakStmt,
    ContinueStmt,
    ExpressionStmt,
    ForStmt,
    FunctionStmt,
    ReturnStmt,
    IfStmt,
    Stmt,
    SwitchStmt,
    CaseStmt,
    DefaultStmt,
    VariableStmt,
    WhileStmt,
)
from simulator.interpreter.lex.token import Token, TokenType

from typing import override

class ParseException(Exception):
    pass

class ParseError:
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


var_ttype = [
    TokenType.BOOL,
    TokenType.BOOLEAN,
    TokenType.BYTE,
    TokenType.CHAR,
    TokenType.DOUBLE,
    TokenType.FLOAT,
    TokenType.INT,
    TokenType.LONG,
    TokenType.SHORT,
    TokenType.SIZE_T,
    TokenType.UNSIGNED_INT,
    TokenType.VOID,
    TokenType.WORD,
    TokenType.UNSIGNED_CHAR,
    TokenType.UNSIGNED_LONG,
]


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
            stmt = self._declaration()
            if stmt is not None:
                statements.append(stmt)

        return statements

    def _declaration(self) -> Stmt | None:
        try:
            if self._match(*var_ttype):
                return self._variable_declaration()
            else:
                return self._statement()
        except ParseException:
            self._synchronize()
            return None

    def _variable_declaration(self) -> VariableStmt | FunctionStmt:
        ttype, identifier = self._declaration_start()

        if self._match(TokenType.EQUAL):
            initializer = self._expression()
            self._consume(TokenType.SEMICOLON, "Expect ';' after declaration.")
            return VariableStmt(ttype, identifier, initializer, ttype=None)

        elif self._match(TokenType.LEFT_PAREN):
            return self._function_declaration(ttype, identifier)

        else:
            self._consume(TokenType.SEMICOLON, "Expect ';' after declaration.")
            return VariableStmt(ttype, identifier, initializer=None, ttype=None)


    def _statement(self) -> Stmt:
        match self._peek().token:
            case TokenType.LEFT_BRACE:
                self._advance()  # LEFT_BRACE
                return self._block()
            case TokenType.RETURN:
                return self._return_stmt()
            case TokenType.BREAK:
                return self._break_stmt()
            case TokenType.CONTINUE:
                return self._continue_stmt()
            case TokenType.SWITCH:
                return self._switch_stmt()
            case TokenType.IF:
                return self._if_stmt()
            case TokenType.WHILE:
                return self._while_stmt()
            case TokenType.FOR:
                return self._for_stmt()
            case _:
                return self._expression_statement()

    def _return_stmt(self):
        self._advance()  # RETURN
        expr = self._expression()
        self._consume(TokenType.SEMICOLON, "Expect ';' after return expression.")
        return ReturnStmt(expr, ttype=None)

    def _break_stmt(self):
        brk = self._advance()  # BREAK
        self._consume(TokenType.SEMICOLON, "Expect ';' after 'break'.")
        return BreakStmt(brk)

    def _continue_stmt(self):
        cont = self._advance()  # CONTINUE
        self._consume(TokenType.SEMICOLON, "Expect ';' after 'continue'.")
        return ContinueStmt(cont)


    def _if_stmt(self):
        self._advance()  # IF

        self._consume(TokenType.LEFT_PAREN, "Expect '(' after if statement.")
        condition = self._expression()
        self._consume(TokenType.RIGHT_PAREN, "Expect ')' after if condition.")

        then_branch = self._statement()

        else_branch = None
        if self._match(TokenType.ELSE):
            else_branch = self._statement()

        return IfStmt(condition, then_branch, else_branch)

    def _switch_stmt(self) -> SwitchStmt:
        self._advance()  # SWITCH

        self._consume(TokenType.LEFT_PAREN, "Expect '(' after switch statement.")
        var = self._parse_atom()
        if not (isinstance(var, LiteralExpr) or isinstance(var, VariableExpr)):
            raise self._error(self.previous, "Var to evaluate in switch statement must be a literal or variable.")
        self._consume(TokenType.RIGHT_PAREN, "Expect ')' after switch var.")

        self._consume(TokenType.LEFT_BRACE, "Expect '{' after switch.")
        cases: list[CaseStmt] = []

        while self._match(TokenType.CASE):
            cases.append(self._case_stmt())

        default = None
        if self._match(TokenType.DEFAULT):
            self._consume(TokenType.COLON, "Expect ':' after default.")
            stmts: list[Stmt] = []
            while self._peek().token is not TokenType.RIGHT_BRACE:
                stmts.append(self._statement())

            default = DefaultStmt(stmts)

        self._consume(TokenType.RIGHT_BRACE, "Expect '}' to end switch.")
        return SwitchStmt(var, cases, default)

    def _case_stmt(self) -> CaseStmt:
        label = self._parse_atom()
        if not (isinstance(label, LiteralExpr) or isinstance(label, VariableExpr)):
            raise self._error(self.previous, "Label to evaluate in case statement must be a literal or variable.")
        self._consume(TokenType.COLON, "Expect ':' after case label.")

        stmts: list[Stmt] = []
        while self._peek().token not in [TokenType.CASE, TokenType.DEFAULT,
                              TokenType.RIGHT_BRACE]:
            stmts.append(self._statement())

        return CaseStmt(label, stmts)

    def _block(self) -> BlockStmt:
        stmts: list[Stmt] = []

        while (not self._check(TokenType.RIGHT_BRACE)) or self._is_at_end():
            stmt = self._declaration()
            if stmt is not None:
                stmts.append(stmt)

        self._consume(TokenType.RIGHT_BRACE, "Expect '}' to close a block.")

        return BlockStmt(stmts)

    def _while_stmt(self) -> WhileStmt:
        self._advance() # WHILE

        self._consume(TokenType.LEFT_PAREN, "Expect '(' after while.")
        condition = self._expression()
        self._consume(TokenType.RIGHT_PAREN, "Expect ')' to close while condition.")

        statement = self._statement()
        return WhileStmt(condition, statement)

    def _for_stmt(self) -> ForStmt:
        self._advance() # FOR

        self._consume(TokenType.LEFT_PAREN, "Expect '(' after for.")

        if self._check(TokenType.SEMICOLON):
            self._advance()
            init_expr = None
        else:
            if self._match(*var_ttype):
                init_expr = self._variable_declaration()
                if not isinstance(init_expr, VariableStmt):
                    raise self._error(self.previous, "For loop init must be a expression or a variable declaration")
            else:
                init_expr = self._expression()
                self._consume(TokenType.SEMICOLON, "Expect ';' after 'for' init expression")

        if self._check(TokenType.SEMICOLON):
            self._advance()
            condition = None
        else:
            condition = self._expression()
            self._consume(TokenType.SEMICOLON, "Expect ';' after 'for' condition")

        if self._check(TokenType.RIGHT_PAREN):
            self._advance()
            loop_expr = None
        else:
            loop_expr = self._expression()
            self._consume(TokenType.RIGHT_PAREN, "Expect ')' after 'for' loop expression")

        statement = self._statement()
        return ForStmt(init_expr, condition, loop_expr, statement)

    def _declaration_start(self):
        var_type = self.previous

        # if left square bracket, this is an array
        if self._match(TokenType.LEFT_BRACKET):
            _number = self._consume(
                TokenType.NUMBER, "Expect number constant in array declaration."
            )
            self._consume(
                TokenType.RIGHT_BRACKET, "Expect closing ']' in array declaration."
            )

        identifier = self._consume(
            TokenType.IDENTIFIER, "Expect identifier in variable declaration."
        )

        return var_type, identifier

    def _function_declaration(self, fn_type: Token, identifier: Token) -> FunctionStmt:
        self._advance()  # LEFT_PAREN
        params = self._parameters()

        self._consume(TokenType.LEFT_BRACE, "Expect '{' before function body.")
        body: list[Stmt] = []

        while not self._check(TokenType.RIGHT_BRACE) and not self._is_at_end():
            stmt = self._declaration()
            if stmt is not None:
                body.append(stmt)

        self._consume(TokenType.RIGHT_BRACE, "Expect '}' to close function body.")

        return FunctionStmt(identifier, params, body, fn_type, ttype=None)

    def _parameters(self) -> list[VariableStmt]:
        params: list[VariableStmt] = []

        if not self._check(TokenType.RIGHT_PAREN):
            var_type, identifier = self._declaration_start()
            param = VariableStmt(var_type, identifier, None, None)
            params.append(param)

        while not self._check(TokenType.RIGHT_PAREN) and self._match(TokenType.COMMA):
            if len(params) > 255:
                self._error(self._peek(), "Can't have more than 255 parameters.")

            if self._match(*var_ttype):
                var_type, identifier = self._declaration_start()
                param = VariableStmt(var_type, identifier, None, None)
                params.append(param)
            else:
                self._error(self._peek(), "Function parameter must have valid type")

        self._consume(TokenType.RIGHT_PAREN, "Expect ')' after parameters.")

        return params

    def _expression_statement(self) -> ExpressionStmt:
        expr = self._expression()
        self._consume(TokenType.SEMICOLON, "Expect ';' after expression.")
        stmt = ExpressionStmt(expr)
        return stmt

    def _expression(self, min_prec: PrecLevel = PrecLevel.MINIMAL) -> Expr:
        if self._match(TokenType.DECREMENT, TokenType.INCREMENT):
            return self._unary_expr()

        return self._parse_binary_expr(min_prec)

    def _unary_expr(self) -> UnaryExpr:
        op = self.previous
        
        self._consume(TokenType.IDENTIFIER, 
                      "Expect identifier after prefix expression")

        var = VariableExpr(self.previous)
        return UnaryExpr(op, True, var)


    def _parse_binary_expr(self, min_prec: PrecLevel) -> Expr:
        # precedence climbing algorithm from https://eli.thegreenplace.net/2012/08/02/parsing-expressions-by-precedence-climbing
        lhs = self._parse_atom()

        while True:
            curr_token = self._peek()

            if (not curr_token.is_binary() or
                get_binary_op_precedence(curr_token.token) < min_prec):
                return lhs

            prec = get_binary_op_precedence(curr_token.token)
            assoc = get_binary_op_assoc(curr_token.token)
            if assoc is Assoc.LEFT:
                next_min_prec = prec + 1
            else:
                next_min_prec = prec

            self._advance()
            rhs = self._expression(next_min_prec)
            if curr_token.token in [
                TokenType.EQUAL,
                TokenType.PLUS_EQUAL,
                TokenType.MINUS_EQUAL,
                TokenType.STAR_EQUAL,
                TokenType.SLASH_EQUAL,
                TokenType.PERCENTAGE_EQUAL,
                TokenType.AND_EQUAL,
                TokenType.OR_EQUAL,
                TokenType.XOR_EQUAL,
            ]:
                if isinstance(lhs, VariableExpr):
                    lhs = AssignExpr(lhs, curr_token, rhs)
                else:
                    # lhs = AssignExpr(Token(TokenType.ERROR, "", None, op.line,
                    # op.column), rhs)
                    self._error(lhs, "Invalid l-value for assignment expression")
            else:
                lhs = BinaryExpr(lhs, curr_token, rhs)

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
            case Token(token=TokenType.IDENTIFIER) as identifier:
                self._advance()

                if self._match(TokenType.LEFT_PAREN):
                    return self._call_expr(identifier)
                elif self._match(TokenType.DECREMENT, TokenType.INCREMENT):
                    return UnaryExpr(self.previous, False,
                                     VariableExpr(identifier))
                else:
                    return VariableExpr(identifier)
            case unexpected_token:
                self._advance()
                self._error(
                    unexpected_token, "Expected number or expression inside parens."
                )
                return LiteralExpr(unexpected_token)

    def _call_expr(self, identifier: Token):
        fn_name = VariableExpr(identifier)

        arguments: list[Expr] = []

        if not self._check(TokenType.RIGHT_PAREN):
            arg = self._expression()
            arguments.append(arg)

        while not self._check(TokenType.RIGHT_PAREN) and self._match(TokenType.COMMA):
            if len(arguments) > 255:
                self._error(self._peek(), "Can't have more than 255 arguments.")

            arg = self._expression()
            arguments.append(arg)

        self._consume(TokenType.RIGHT_PAREN, "Expect ')' after function arguments.")

        return CallExpr(fn_name, arguments)

    def _consume(self, token_type: TokenType, message: str) -> Token:
        if not self._check(token_type):
            raise self._error(self._peek(), message)

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
        diag = Diagnostic(
            message, token.line, token.column, token.column + len(token.lexeme)
        )
        self.diagnostics.append(diag)
        return ParseException()

    def _synchronize(self):
        self._advance()

        while not self._is_at_end():
            if self.previous.token is TokenType.SEMICOLON:
                return

            if self._peek().token in [
                TokenType.SWITCH,
                TokenType.CHAR,
                TokenType.FOR,
                TokenType.WHILE,
                TokenType.IF,
                TokenType.RETURN,
                TokenType.DO,
            ]:
                return

            self._advance()
