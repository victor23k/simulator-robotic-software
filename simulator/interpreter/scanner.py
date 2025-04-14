from simulator.interpreter.token import Token, TokenType

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


class Scanner:
    """
    Iterator that produces tokens from source program.
    """

    source: str
    start: int
    current: int
    line: int
    tokens: [Token]

    def __init__(self, source: str):
        self.source = source
        self.start = 0
        self.current = 0
        self.line = 1
        self.tokens = []
        self.source_consumed = False

    def __iter__(self):
        return self

    def __next__(self):
        if self.source_consumed:
            raise StopIteration

        if self._is_at_end():
            self.source_consumed = True
            return self._produce_empty_token(TokenType.EOF)

        self._skip_whitespace()

        match self._advance():
            case "(":
                next_token = self._produce_empty_token(TokenType.LEFT_PAREN)
            case ")":
                next_token = self._produce_empty_token(TokenType.RIGHT_PAREN)
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
            case x:
                if x.isdigit():
                    next_token = self._number()
                elif x.isalpha():
                    next_token = self._identifier()
                else:
                    # error: unexpected character
                    pass

        self.start = self.current
        return next_token

    def _is_at_end(self) -> bool:
        return self.current >= len(self.source)

    def _number(self) -> Token:
        while self._peek().isdigit():
            self._advance()
        if self._peek() == "." and self._peek_next().isdigit():
            self._advance()
            while self._peek().isdigit():
                self._advance()
            number = float(self.source[self.start:self.current])
        else:
            number = int(self.source[self.start : self.current])

        return self._produce_token(TokenType.NUMBER, number)

    def _identifier(self) -> Token:
        while self._peek().isalnum() or self._peek == "_":
            self._advance()

        identifier = self.source[self.start : self.current]

        return self._produce_token(keywords.get(identifier, TokenType.IDENTIFIER))

    def _advance(self) -> str:
        if self._is_at_end():
            return False
        self.current += 1
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
        while self._peek().isspace():
            self._advance()
        self.start = self.current

    def _produce_empty_token(self, token_type: TokenType) -> Token:
        return self._produce_token(token_type, None)

    def _produce_token(self, token_type: TokenType, literal: object) -> Token:
        text = self.source[self.start : self.current]
        return Token(token_type, text, literal, self.line)
