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

    def is_at_end(self) -> bool:
        return self.current >= len(self.source)

    def next_token(self):
        match self.__advance():
            case "(":
                self.__add_empty_token(TokenType.LEFT_PAREN)
            case ")":
                self.__add_empty_token(TokenType.RIGHT_PAREN)
            case "{":
                self.__add_empty_token(TokenType.LEFT_BRACE)
            case "}":
                self.__add_empty_token(TokenType.RIGHT_BRACE)
            case "[":
                self.__add_empty_token(TokenType.RIGHT_BRACKET)
            case "]":
                self.__add_empty_token(TokenType.RIGHT_BRACKET)
            case ",":
                self.__add_empty_token(TokenType.COMMA)
            case ".":
                self.__add_empty_token(TokenType.DOT)
            case ";":
                self.__add_empty_token(TokenType.SEMICOLON)
            case ":":
                self.__add_empty_token(TokenType.COLON)
            case x:
                if x.is_digit():
                    self.__number()
                elif self.__is_alpha(x):
                    self.__identifier()
                else:
                    # error: unexpected character
                    pass


    def __advance(self) -> str:
        self.current += 1
        return self.source[self.current - 1]

    def __match(self, expected: str) -> bool:
        if self.is_at_end():
            return False
        if self.source[self.current] != expected:
            return False

        self.current += 1
        return True

    def __peek(self) -> str:
        if self.is_at_end():
            return "\0"
        return self.source[self.current]

    def __peek_next(self) -> str:
        if self.current + 1 >= len(self.source):
            return "\0"
        return self.source[self.current + 1]

    def __add_empty_token(self, token_type: TokenType):
        self.__add_token(token_type, None)

    def __add_token(self, token_type: TokenType, literal: object):
        text = self.source[self.start : self.current]
        self.tokens.append(Token(token_type, text, literal, self.line))
