import sys
from enum import Enum


class Scanner:
    """
    Scanner class scans the line and extracts tokens.
    """

    def __init__(self, source):
        self.error = False
        self.tokens = []
        self.source = source

    def advance(self, current):
        if current + 1 < len(self.source):
            return self.source[current + 1]
        else:
            return None

    def scan(self):
        # Scan the line and add found tokens to the tokens list
        pointer = 0
        line = 1
        while pointer < len(self.source):
            char = self.source[pointer]
            match char:
                case '\n':
                    line += 1
                case "(":
                    self.tokens.append(Token(TokenType.LEFT_PAREN, self.get_token(pointer), "null", line))
                case ")":
                    self.tokens.append(Token(TokenType.RIGHT_PAREN, self.get_token(pointer), "null", line))
                case "}":
                    self.tokens.append(Token(TokenType.RIGHT_BRACE, self.get_token(pointer), "null", line))
                case "{":
                    self.tokens.append(Token(TokenType.LEFT_BRACE, self.get_token(pointer), "null", line))
                case "*":
                    self.tokens.append(Token(TokenType.STAR, self.get_token(pointer), "null", line))
                case ".":
                    self.tokens.append(Token(TokenType.DOT, self.get_token(pointer), "null", line))
                case ",":
                    self.tokens.append(Token(TokenType.COMMA, self.get_token(pointer), "null", line))
                case "+":
                    self.tokens.append(Token(TokenType.PLUS, self.get_token(pointer), "null", line))
                case "-":
                    self.tokens.append(Token(TokenType.MINUS, self.get_token(pointer), "null", line))
                case ";":
                    self.tokens.append(Token(TokenType.SEMICOLON, self.get_token(pointer), "null", line))
                case "=":
                    if self.advance(pointer) == '=':
                        self.tokens.append(Token(TokenType.EQUAL_EQUAL, self.get_token_multi(pointer, 1), "null", line))
                        pointer += 1
                    else:
                        self.tokens.append(Token(TokenType.EQUAL, self.get_token(pointer), "null", line))
                case _:
                    print(f'[line {line}] Error: Unexpected character: {char}', file=sys.stderr)
                    self.error = True
            pointer += 1
        self.tokens.append(Token(TokenType.EOF, "", "null", line))

    def get_token(self, index):
        return self.get_token_multi(index, 0)

    def get_token_multi(self, index_start, span):
        return self.source[index_start: (index_start + 1) + span]


class Token:
    """
    Token class, contains all information of the token to return to the scanner.
    """

    def __init__(self, token_type, lexeme, literal, line):
        self.type = token_type
        self.lexeme = lexeme
        self.literal = literal
        self.line = line

    def __str__(self):
        return f"{self.type.value} {self.lexeme} {self.literal}"


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
    scanner.scan()
    print(*scanner.tokens, sep="\n")

    if scanner.error:
        exit(65)
    else:
        exit(0)


if __name__ == "__main__":
    main()
