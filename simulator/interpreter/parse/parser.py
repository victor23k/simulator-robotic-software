from simulator.interpreter.parse.associativity import Assoc, get_binary_op_assoc
from simulator.interpreter.ast.expr import (
    ArrayInitExpr,
    ArrayRefExpr,
    AssignExpr,
    CallExpr,
    GetExpr,
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
    ArrayDeclStmt,
    BlockStmt,
    BreakStmt,
    ContinueStmt,
    DeclarationListStmt,
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
    DoWhileStmt,
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
    type_names: set[str]

    def __init__(self, source: str, diagnostics: list[Diagnostic]):
        self.source = source
        self.scanner = Scanner(source)
        self.diagnostics = diagnostics
        self.current = Token(TokenType.EOF, "", None, 0, 0)
        self.type_names = set()
        self._advance()

    def parse(self) -> list[Stmt]:
        """
        Parses the source string into an AST that takes the form of a list of
        statements.
        """

        sketch_items: list[Stmt] = []

        while not self._is_at_end():
            item = self._sketch_item()
            if item is not None:
                sketch_items.append(item)

        return sketch_items

    def add_type_name(self, type_name: str):
        """
        Adds a type name to differentiate between regular identifiers and user
        defined type identifiers.

        In our Arduino implementation these can only come from classes.
        """
        self.type_names.add(type_name)

    def _sketch_item(self) -> Stmt | None:
        try:
            if (
                self._check(
                    *var_ttype, TokenType.CONST, TokenType.VOLATILE, TokenType.STATIC
                )
                or self._is_type_name_identifier()
            ):
                return self._declaration(self._advance())
            else:
                return self._statement()
        except ParseException:
            self._synchronize()
            return None

    def _declaration(self, first_spec=None) -> Stmt | None:
        specifiers = []
        if first_spec is not None:
            specifiers.append(first_spec)

        specifiers.extend(self._decl_specifiers())

        return self._declarator_list(specifiers)

    def _decl_specifiers(self) -> list[Token]:
        specifiers: list[Token] = []
        while (
            self._check(
                *var_ttype, TokenType.CONST, TokenType.VOLATILE, TokenType.STATIC
            )
            or self._is_type_name_identifier()
        ):
            tok = self._advance()
            if not self._check(TokenType.VOLATILE, TokenType.STATIC):
                specifiers.append(tok)

        return specifiers

    def _is_type_name_identifier(self):
        return (
            self._check(TokenType.IDENTIFIER) and self._peek().lexeme in self.type_names
        )

    def _declarator_list(self, specifiers) -> Stmt:
        declarator_list = [self._declarator(specifiers)]

        while self._match(TokenType.COMMA):
            declarator_list.append(self._declarator(specifiers))

        if len(declarator_list) == 1:
            if not isinstance(declarator_list[0], FunctionStmt):
                self._consume(TokenType.SEMICOLON, "Expect ';' after declaration.")
            return declarator_list[0]

        self._consume(TokenType.SEMICOLON, "Expect ';' after declaration list.")
        return DeclarationListStmt(declarator_list)

    def _declarator(self, specifiers) -> VariableStmt | FunctionStmt | ArrayDeclStmt:
        # if self._match(TokenType.STAR):
        #     pointer = self._pointer()

        ident = self._consume(TokenType.IDENTIFIER, "Expect identifier")

        if self._match(TokenType.LEFT_PAREN):
            return self._function_declaration(specifiers, ident)
        else:
            return self._variable_declarator(specifiers, ident)

    def _variable_declarator(self, specifiers, ident) -> ArrayDeclStmt | VariableStmt:
        initializer = None

        if not self._check(TokenType.LEFT_BRACKET):
            if self._match(TokenType.EQUAL):
                initializer = self._initializer()
            return VariableStmt(specifiers, ident, initializer)

        dimensions: list[Expr | None] = []
        needs_initializer = False

        while self._match(TokenType.LEFT_BRACKET):
            if self._match(TokenType.RIGHT_BRACKET):
                needs_initializer = True
                dimensions.append(None)
            else:
                dimensions.append(self._expression())
                self._consume(TokenType.RIGHT_BRACKET, "Expect ']' to close array.")

        if self._match(TokenType.EQUAL):
            initializer = self._initializer()
        elif needs_initializer:
            self._error(ident, "Array declaration without size needs an initializer")

        return ArrayDeclStmt(specifiers, dimensions, ident, initializer)

    def _initializer(self) -> Expr:
        if self._match(TokenType.LEFT_BRACE):
            init_list: list[Expr] = []
            init_list.append(self._initializer())

            while self._match(TokenType.COMMA) and not self._check(
                TokenType.RIGHT_BRACE
            ):
                init_list.append(self._initializer())

            self._consume(
                TokenType.RIGHT_BRACE, "Expect '}' to close initializer list."
            )

            return ArrayInitExpr(init_list)
        elif self._check(TokenType.STRING_LITERAL):
            string = self._advance()
            init_list = [LiteralExpr(c) for c in string.literal]
            return ArrayInitExpr(init_list)

        return self._expression()

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
            case TokenType.DO:
                return self._do_while_stmt()
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
            raise self._error(
                self.previous,
                "Var to evaluate in switch statement must be a literal or variable.",
            )
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
            raise self._error(
                self.previous,
                "Label to evaluate in case statement must be a literal or variable.",
            )
        self._consume(TokenType.COLON, "Expect ':' after case label.")

        stmts: list[Stmt] = []
        while self._peek().token not in [
            TokenType.CASE,
            TokenType.DEFAULT,
            TokenType.RIGHT_BRACE,
        ]:
            stmts.append(self._statement())

        return CaseStmt(label, stmts)

    def _block(self) -> BlockStmt:
        stmts: list[Stmt] = []

        while (not self._check(TokenType.RIGHT_BRACE)) or self._is_at_end():
            stmt = self._sketch_item()
            if stmt is not None:
                stmts.append(stmt)

        self._consume(TokenType.RIGHT_BRACE, "Expect '}' to close a block.")

        return BlockStmt(stmts)

    def _while_stmt(self) -> WhileStmt:
        self._advance()  # WHILE

        self._consume(TokenType.LEFT_PAREN, "Expect '(' after while.")
        condition = self._expression()
        self._consume(TokenType.RIGHT_PAREN, "Expect ')' to close while condition.")

        statement = self._statement()
        return WhileStmt(condition, statement)

    def _do_while_stmt(self) -> DoWhileStmt:
        self._advance()  # DO

        statement = self._statement()
        self._consume(TokenType.WHILE, "Expect 'while' after do-while statement.")
        self._consume(TokenType.LEFT_PAREN, "Expect '(' after 'while'.")
        condition = self._expression()
        self._consume(TokenType.RIGHT_PAREN, "Expect ')' to close do-while condition.")
        self._consume(TokenType.SEMICOLON, "Expect ';' after do-while condition.")

        return DoWhileStmt(statement, condition)

    def _for_stmt(self) -> ForStmt:
        self._advance()  # FOR

        self._consume(TokenType.LEFT_PAREN, "Expect '(' after for.")

        if self._check(TokenType.SEMICOLON):
            self._advance()
            init_expr = None
        else:
            if self._match(
                *var_ttype, TokenType.CONST, TokenType.VOLATILE, TokenType.STATIC
            ):
                init_expr = self._simple_declaration(self.previous)
                self._consume(
                    TokenType.SEMICOLON, "Expect ';' after 'for' init declaration"
                )
            else:
                init_expr = self._expression()
                self._consume(
                    TokenType.SEMICOLON, "Expect ';' after 'for' init expression"
                )

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
            self._consume(
                TokenType.RIGHT_PAREN, "Expect ')' after 'for' loop expression"
            )

        statement = self._statement()
        return ForStmt(init_expr, condition, loop_expr, statement)

    def _function_declaration(
        self, fn_specifiers: list[Token], identifier: Token
    ) -> FunctionStmt:
        params = self._parameters()

        self._consume(TokenType.LEFT_BRACE, "Expect '{' before function body.")
        body: list[Stmt] = []

        while not self._check(TokenType.RIGHT_BRACE) and not self._is_at_end():
            stmt = self._sketch_item()
            if stmt is not None:
                body.append(stmt)

        self._consume(TokenType.RIGHT_BRACE, "Expect '}' to close function body.")

        return FunctionStmt(identifier, params, body, fn_specifiers)

    def _parameters(self) -> list[VariableStmt]:
        params: list[VariableStmt] = []

        if not self._check(TokenType.RIGHT_PAREN):
            param = self._simple_declaration()
            params.append(param)

        while not self._check(TokenType.RIGHT_PAREN) and self._match(TokenType.COMMA):
            if len(params) > 255:
                self._error(self._peek(), "Can't have more than 255 parameters.")

            param = self._simple_declaration()
            params.append(param)

        self._consume(TokenType.RIGHT_PAREN, "Expect ')' after parameters.")

        return params

    def _simple_declaration(self, first_spec=None) -> VariableStmt:
        specifiers = []
        if first_spec is not None:
            specifiers.append(first_spec)

        specifiers.extend(self._decl_specifiers())

        decl = self._declarator(specifiers)
        if isinstance(decl, FunctionStmt):
            raise self._error(
                decl.name, "Cannot use a function declaration in a simple declaration."
            )

        return decl

    def _expression_statement(self) -> ExpressionStmt:
        expr = self._expression()
        self._consume(TokenType.SEMICOLON, "Expect ';' after expression.")
        stmt = ExpressionStmt(expr)
        return stmt

    def _expression(self, min_prec: PrecLevel = PrecLevel.MINIMAL) -> Expr:
        if self._match(
            TokenType.DECREMENT,
            TokenType.INCREMENT,
            TokenType.LOGICAL_NOT,
            TokenType.BITWISE_NOT,
        ):
            return self._unary_expr()

        return self._parse_binary_expr(min_prec)

    def _unary_expr(self) -> UnaryExpr:
        op = self.previous

        self._consume(TokenType.IDENTIFIER, "Expect identifier after prefix expression")

        var = VariableExpr(self.previous)
        return UnaryExpr(op, True, var)

    def _parse_binary_expr(self, min_prec: PrecLevel) -> Expr:
        # precedence climbing algorithm from https://eli.thegreenplace.net/2012/08/02/parsing-expressions-by-precedence-climbing
        lhs = self._parse_atom()

        while True:
            curr_token = self._peek()

            if (
                not curr_token.is_binary()
                or get_binary_op_precedence(curr_token.token) < min_prec
            ):
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
                if isinstance(lhs, VariableExpr) or isinstance(lhs, ArrayRefExpr):
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
            case _:
                return self._postfix_expr()

    def _postfix_expr(self) -> Expr:
        primary = self._primary_expr()

        if self._check(TokenType.LEFT_PAREN, TokenType.DOT):
            return self._call_expr(primary)
        elif self._match(TokenType.DECREMENT, TokenType.INCREMENT):
            return UnaryExpr(self.previous, False, primary)
        elif self._match(TokenType.LEFT_BRACKET):
            return self._array_ref_expr(primary)
        else:
            return primary

    def _array_ref_expr(self, primary: Expr):
        expr = self._expression()
        self._consume(TokenType.RIGHT_BRACKET, "Expect ']' to close array reference.")
        if self._match(TokenType.LEFT_BRACKET):
            arrexpr = self._array_ref_expr(ArrayRefExpr(primary, expr))
            return arrexpr

        return ArrayRefExpr(primary, expr)

    def _primary_expr(self):
        match self._advance():
            case Token(token=TokenType.LEFT_PAREN):
                expr = self._expression(PrecLevel.MINIMAL)
                self._consume(TokenType.RIGHT_PAREN, "Unmatched '('")
                return expr
            case (
                Token(
                    token=TokenType.INT_LITERAL
                    | TokenType.FLOAT_LITERAL
                    | TokenType.CHAR_LITERAL
                    | TokenType.STRING_LITERAL
                ) as token
            ):
                return LiteralExpr(token)
            case Token(token=TokenType.IDENTIFIER) as ident:
                return VariableExpr(ident)
            case unexpected_token:
                raise self._error(
                    unexpected_token, "Expected number or expression inside parens."
                )

    def _call_expr(self, expr: Expr):
        while True:
            if self._match(TokenType.LEFT_PAREN):
                expr = self._finish_call_expr(expr)
            elif self._match(TokenType.DOT):
                name = self._consume(TokenType.IDENTIFIER, "Expect method after '.'.")
                expr = GetExpr(expr, name)
            else:
                break

        return expr

    def _finish_call_expr(self, callee: Expr) -> CallExpr:
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

        return CallExpr(callee, arguments)

    def _get_expr(self, obj: Expr):
        name = self._consume(
            TokenType.IDENTIFIER, "Expect method or attribute name after '.'."
        )

        return GetExpr(obj, name)

    def _consume(self, token_type: TokenType, message: str) -> Token:
        if not self._check(token_type):
            raise self._error(self._peek(), message)

        return self._advance()

    def _match(self, *token_types: TokenType) -> bool:
        if self._check(*token_types):
            self._advance()
            return True

        return False

    def _check(self, *token_types: TokenType) -> bool:
        return self._peek().token in token_types

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
