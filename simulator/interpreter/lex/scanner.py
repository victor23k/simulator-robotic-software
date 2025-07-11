from simulator.interpreter.diagnostic import Diagnostic
from simulator.interpreter.lex.token import Token, TokenType

keywords = {
    "break": TokenType.BREAK,
    "case": TokenType.CASE,
    "continue": TokenType.CONTINUE,
    "do": TokenType.DO,
    "else": TokenType.ELSE,
    "for": TokenType.FOR,
    "goto": TokenType.GOTO,
    "if": TokenType.IF,
    "return": TokenType.RETURN,
    "switch": TokenType.SWITCH,
    "while": TokenType.WHILE,
}

types = {
    "bool": TokenType.BOOL,
    "boolean": TokenType.BOOLEAN,
    "byte": TokenType.BYTE,
    "char": TokenType.CHAR,
    "double": TokenType.DOUBLE,
    "float": TokenType.FLOAT,
    "int": TokenType.INT,
    "long": TokenType.LONG,
    "short": TokenType.SHORT,
    "size_t": TokenType.SIZE_T,
    "word": TokenType.WORD,
}


def is_bin(c: str) -> bool:
    """Checks if a character is a valid hexadecimal binary character"""

    return 48 <= ord(c) <= 49


def is_hex(c: str) -> bool:
    """Checks if a character is a valid hexadecimal ASCII character"""

    codepoint = ord(c)
    return (
        (48 <= codepoint <= 57) or (97 <= codepoint <= 102) or (65 <= codepoint <= 70)
    )


def is_decimal(c: str) -> bool:
    """
    Checks if a character is an ASCII decimal.

    str.isdecimal() is not valid for this scanner because it returns True for
    unicode decimal characters.
    """

    codepoint = ord(c)
    return 48 <= codepoint <= 57


def is_octal(c: str) -> bool:
    """
    Checks if a character is a valid octal ASCII character.
    """

    return 48 <= ord(c) <= 55


class Scanner:
    """
    Iterator that produces tokens from source program.
    """

    source: str
    start: int
    current: int
    line: int
    column: int
    tokens: list[Token]
    diagnostics: list[Diagnostic]
    source_consumed: bool

    def __init__(self, source: str):
        self.source = source
        self.start = 0
        self.current = 0
        self.line = 1
        self.column = 1
        self.tokens = []
        self.diagnostics = []
        self.source_consumed = False

    def __iter__(self):
        return self

    def __next__(self) -> Token:
        if self.source_consumed:
            raise StopIteration

        if self._is_at_end():
            self.source_consumed = True
            return self._produce_empty_token(TokenType.EOF)

        self._skip_whitespace()

        next_token = self._produce_empty_token(TokenType.EOF)

        match self._advance():
            case "(":
                next_token = self._produce_empty_token(TokenType.LEFT_PAREN)
            case ")":
                next_token = self._produce_empty_token(TokenType.RIGHT_PAREN)
            case "[":
                next_token = self._produce_empty_token(TokenType.LEFT_BRACKET)
            case "]":
                next_token = self._produce_empty_token(TokenType.RIGHT_BRACKET)
            case "{":
                next_token = self._produce_empty_token(TokenType.LEFT_BRACE)
            case "}":
                next_token = self._produce_empty_token(TokenType.RIGHT_BRACE)
            case ".":
                next_token = self._produce_empty_token(TokenType.DOT)
            case ";":
                next_token = self._produce_empty_token(TokenType.SEMICOLON)
            case "=":
                if self._peek() == "=":
                    self._advance()
                    next_token = self._produce_empty_token(TokenType.EQUAL_EQUAL)
                else:
                    next_token = self._produce_empty_token(TokenType.EQUAL)
            case "+":
                match self._peek():
                    case "+":
                        self._advance()
                        next_token = self._produce_empty_token(TokenType.INCREMENT)
                    case "=":
                        self._advance()
                        next_token = self._produce_empty_token(TokenType.PLUS_EQUAL)
                    case _:
                        next_token = self._produce_empty_token(TokenType.PLUS)
            case "-":
                match self._peek():
                    case "-":
                        self._advance()
                        next_token = self._produce_empty_token(TokenType.DECREMENT)
                    case "=":
                        self._advance()
                        next_token = self._produce_empty_token(TokenType.MINUS_EQUAL)
                    case _:
                        next_token = self._produce_empty_token(TokenType.MINUS)
            case "*":
                if self._peek() == "=":
                    self._advance()
                    next_token = self._produce_empty_token(TokenType.STAR_EQUAL)
                else:
                    next_token = self._produce_empty_token(TokenType.STAR)
            case "/":
                if self._peek() == "=":
                    self._advance()
                    next_token = self._produce_empty_token(TokenType.SLASH_EQUAL)
                else:
                    next_token = self._produce_empty_token(TokenType.SLASH)
            case "%":
                if self._peek() == "=":
                    self._advance()
                    next_token = self._produce_empty_token(TokenType.PERCENTAGE_EQUAL)
                else:
                    next_token = self._produce_empty_token(TokenType.PERCENTAGE)
            case "!":
                if self._peek() == "=":
                    self._advance()
                    next_token = self._produce_empty_token(TokenType.NOT_EQUAL)
                else:
                    next_token = self._produce_empty_token(TokenType.LOGICAL_NOT)
            case "0":
                match self._peek():
                    case "b":
                        self._advance()
                        next_token = self._binary()
                    case "x":
                        self._advance()
                        next_token = self._hex()
                    case char:
                        if is_octal(char):
                            self._advance()
                            next_token = self._octal()
                        else:
                            # can be 0 or float with leading 0.
                            next_token = self._number()
            case "\x00":
                pass
            case char:
                if is_decimal(char):
                    next_token = self._number()
                elif char.isalpha():
                    next_token = self._identifier()
                else:
                    diag = Diagnostic(
                        message=f"Unexpected character: {char}",
                        line=self.line,
                        col_start=self.column - (self.current - self.start),
                        col_end=self.column,
                    )
                    self.diagnostics.append(diag)
                    pass

        self.start = self.current
        return next_token

    def _is_at_end(self) -> bool:
        return self.current >= len(self.source)

    def _number(self) -> Token:
        while is_decimal(self._peek()):
            self._advance()

        # scientific notation
        if self._peek() == "e" or self._peek() == "E":
            self._advance()
            if self._peek() == "-":
                self._advance()

            while is_decimal(self._peek()):
                self._advance()

            number = float(self.source[self.start : self.current])
            token_type = TokenType.FLOAT_LITERAL

        # float scientific notation
        elif self._peek() == "." and self._peek_next().isdigit():
            self._advance()
            while self._peek().isdigit():
                self._advance()

            if self._peek() == "e" or self._peek() == "E":
                self._advance()
                if self._peek() == "-":
                    self._advance()

                while is_decimal(self._peek()):
                    self._advance()

            number = float(self.source[self.start : self.current])
            token_type = TokenType.FLOAT_LITERAL
        # regular integer
        else:
            number = int(self.source[self.start : self.current])
            token_type = TokenType.INT_LITERAL

        return self._produce_token(token_type, number)

    def _binary(self) -> Token:
        if is_bin(self._peek()):
            self._advance()
        else:
            # eat characters until whitespace
            while not self._peek().isspace():
                self._advance()

            diag = Diagnostic(
                message="Expected 0 or 1 in binary constant",
                line=self.line,
                col_start=self.column - (self.current - self.start),
                col_end=self.column,
            )
            self.diagnostics.append(diag)
            return self._produce_empty_token(TokenType.ERROR)

        while is_bin(self._peek()):
            self._advance()

        number = int(self.source[self.start : self.current], 2)

        return self._produce_token(TokenType.INT_LITERAL, number)

    def _hex(self) -> Token:
        if is_hex(self._peek()):
            self._advance()
        else:
            # panic mode until whitespace
            while not self._peek().isspace():
                self._advance()

            diag = Diagnostic(
                message="Expected 0-9, A-F or a-f in hex constant",
                line=self.line,
                col_start=self.start,
                col_end=self.current,
            )
            self.diagnostics.append(diag)
            return self._produce_empty_token(TokenType.ERROR)

        while is_hex(self._peek()):
            self._advance()

        number = int(self.source[self.start : self.current], 16)
        return self._produce_token(TokenType.INT_LITERAL, number)

    def _octal(self) -> Token:
        while is_octal(self._peek()):
            self._advance()

        number = int(self.source[self.start : self.current], 8)
        return self._produce_token(TokenType.INT_LITERAL, number)

    def _identifier(self) -> Token:
        while self._peek().isalnum() or self._peek == "_":
            self._advance()

        identifier = self.source[self.start : self.current]

        if identifier == "unsigned":
            self._skip_whitespace()
            second_word_start = self.current
            while self._peek().isalnum():
                self._advance()

            second_word = self.source[second_word_start : self.current]
            match second_word:
                case "char":
                    return self._produce_token(
                        TokenType.UNSIGNED_CHAR,
                        self.source[self.start:self.current]
                    )
                case "int":
                    return self._produce_token(
                        TokenType.UNSIGNED_INT,
                        self.source[self.start:self.current]
                    )
                case "long":
                    return self._produce_token(
                        TokenType.UNSIGNED_LONG,
                        self.source[self.start:self.current]
                    )
                case _:
                    diag = Diagnostic(
                        message="Only the following types allow an 'unsigned'" +
                            "modifier: 'char', 'int', and 'long'",
                        line=self.line,
                        col_start=self.column - (self.current - self.start),
                        col_end=self.column,
                    )
                    self.diagnostics.append(diag)
                    return self._produce_empty_token(TokenType.ERROR)
        else:
            token_type = keywords.get(
                            identifier,
                            types.get(identifier, TokenType.IDENTIFIER))

            return self._produce_token(token_type, identifier)

    def _advance(self) -> str:
        if self._is_at_end():
            return "\0"
        self.current += 1
        self.column += 1
        return self.source[self.current - 1]

    def _match(self, expected: str) -> bool:
        if self._is_at_end():
            return False
        if self.source[self.current] != expected:
            return False

        self.current += 1
        return True

    def _peek(self) -> str:
        if self._is_at_end():
            return "\0"
        return self.source[self.current]

    def _peek_next(self) -> str:
        if self.current + 1 >= len(self.source):
            return "\0"
        return self.source[self.current + 1]

    def _skip_whitespace(self):
        peek_chr = self._peek()
        if peek_chr == "\n" or peek_chr == "\r":
            self.line += 1
            self._advance()
            self.column = 0
        elif peek_chr == "\r" and self._peek_next() == "\n":
            self.line += 1
            self._advance()
            self._advance()
            self.column = 0

        while self._peek().isspace():
            self._advance()

        self.start = self.current

    def _produce_empty_token(self, token_type: TokenType) -> Token:
        return self._produce_token(token_type, None)

    def _produce_token(self, token_type: TokenType, literal: object) -> Token:
        text = self.source[self.start : self.current]
        return Token(token_type, text, literal, self.line, self.column)
