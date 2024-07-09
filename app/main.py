import sys
from enum import Enum


class Scanner:
    """
    Scanner class scans the line and extracts tokens.
    """
    def __init__(self, source):
        self.tokens = []
        self.pointer = 0
        self.start = 0
        self.line = 1
        self.source = source
        self.error_code = 0

    def is_at_end(self):
        """Checks if the line is at the end of the file."""
        return self.pointer == len(self.source)

    def advance(self):
        character = self.source[self.pointer]
        self.pointer += 1
        return character

    def next_char(self, character):
        """ Returns True if the next character is the expected 'character' param """
        if self.is_at_end():
            return False
        if self.source[self.pointer] != character:
            return False

        self.pointer += 1
        return True

    def peek(self):
        if not self.is_at_end():
            return self.source[self.pointer]
        return '\0'

    def peek_next(self) -> str:
        if self.pointer + 1 >= len(self.source):
            return "\0"
        return self.source[self.pointer + 1]

    def scan_token(self):
        """Scans the line and extracts tokens."""
        c = self.advance()
        match c:
            case '\n':
                self.line += 1
            case '(':
                self.add_token(TokenType.LEFT_PAREN)
            case ')':
                self.add_token(TokenType.RIGHT_PAREN)
            case '{':
                self.add_token(TokenType.LEFT_BRACE)
            case '}':
                self.add_token(TokenType.RIGHT_BRACE)
            case ',':
                self.add_token(TokenType.COMMA)
            case '.':
                self.add_token(TokenType.DOT)
            case '-':
                self.add_token(TokenType.MINUS)
            case '+':
                self.add_token(TokenType.PLUS)
            case ';':
                self.add_token(TokenType.SEMICOLON)
            case '*':
                self.add_token(TokenType.STAR)
            case '!':
                self.add_token(TokenType.BANG_EQUAL if self.next_char('=') else TokenType.BANG)
            case '=':
                self.add_token(TokenType.EQUAL_EQUAL if self.next_char('=') else TokenType.EQUAL)
            case '<':
                self.add_token(TokenType.LESS_EQUAL if self.next_char('=') else TokenType.LESS)
            case '>':
                self.add_token(TokenType.GREATER_EQUAL if self.next_char('=') else TokenType.GREATER)
            case '/':
                if self.next_char('/'):
                    while self.peek() != '\n' and not self.is_at_end():
                        self.advance()
                else:
                    self.add_token(TokenType.SLASH)
            case ' ':
                return
            case '\t':
                return
            case '\r':
                return
            case '"':
                self.string()
            case _:
                if self.is_digit(c):
                    self.number()
                else:
                    self.error_code = 65
                    print(f'[line {self.line}] Error: Unexpected character: {c}', file=sys.stderr)

    @staticmethod
    def is_digit(char: str) -> bool:
        return "0" <= char <= "9"

    def number(self) -> None:
        while self.is_digit(self.peek()):
            self.advance()

        if self.peek() == "." and self.is_digit(self.peek_next()):
            self.advance()

        while self.is_digit(self.peek()):
            self.advance()

        self.add_token(TokenType.NUMBER, float(self.source[self.start: self.pointer]))

    def string(self):
        """Parse for string literal"""
        while self.peek() != '"' and not self.is_at_end():
            self.advance()
        if not self.is_at_end():
            self.advance()
            self.add_token(TokenType.STRING, self.source[self.start + 1:self.pointer - 1])

    def scan_tokens(self):
        """Scanning loop controller"""
        while not self.is_at_end():
            self.start = self.pointer
            self.scan_token()

        self.tokens.append(Token(TokenType.EOF, "", None, self.line))
        return None

    def add_token(self, token_type: Enum, literal=None):
        """ Adds a new token to the tokens list."""
        # self.pointer should always be bigger than self.start
        text = self.source[self.start:self.pointer]
        self.tokens.append(Token(token_type, text, literal, self.line))


class Token:
    """
    Token class, contains all information of the token to return to the scanner.
    """

    def __init__(self, token_type: Enum, lexeme, literal, line):
        self.type = token_type
        self.lexeme = lexeme
        self.literal = literal
        self.line = line

    def __str__(self):
        if self.literal is None:
            literal = "null"
        else:
            literal = self.literal
        return f"{self.type.value} {self.lexeme} {literal}"


class TokenType(Enum):
    # Single-character tokens
    LEFT_PAREN = "LEFT_PAREN"
    RIGHT_PAREN = "RIGHT_PAREN"
    LEFT_BRACE = "LEFT_BRACE"
    RIGHT_BRACE = "RIGHT_BRACE"
    COMMA = "COMMA"
    DOT = "DOT"
    PLUS = "PLUS"
    MINUS = "MINUS"
    STAR = "STAR"
    SEMICOLON = "SEMICOLON"
    SLASH = "SLASH"

    # One or two character tokens
    BANG = "BANG"
    BANG_EQUAL = "BANG_EQUAL"
    EQUAL = "EQUAL"
    EQUAL_EQUAL = "EQUAL_EQUAL"
    GREATER = "GREATER"
    GREATER_EQUAL = "GREATER_EQUAL"
    LESS = "LESS"
    LESS_EQUAL = "LESS_EQUAL"

    # Keywords
    AND = "AND"
    OR = "OR"
    CLASS = "CLASS"
    ELSE = "ELSE"
    WHILE = "WHILE"
    VAR = "VAR"
    FALSE = "FALSE"
    TRUE = "TRUE"
    THIS = "THIS"
    RETURN = "RETURN"
    PRINT = "PRINT"
    IF = "IF"
    NIL = "NIL"
    FUN = "FUN"
    SUPER = "SUPER"

    # Multi-character tokens
    STRING = "STRING"
    NUMBER = "NUMBER"

    # EOF
    EOF = "EOF"


def main():
    if len(sys.argv) < 3:
        print("Usage: ./your_program.sh tokenize <filename>", file=sys.stderr)
        exit(1)

    command = sys.argv[1]
    filename = sys.argv[2]

    if command != "tokenize":
        print(f"Unknown command: {command}", file=sys.stderr)
        exit(1)

    with open(filename) as file:
        file_contents = file.read()

    scanner = Scanner(file_contents)
    scanner.scan_tokens()
    print(*scanner.tokens, sep="\n")

    exit(scanner.error_code)


if __name__ == "__main__":
    main()
