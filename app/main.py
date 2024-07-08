import sys


def tokenize(file_contents):
    line = 0

    for c in file_contents:
        match c:
            case "(":
                print("LEFT_PAREN ( null")
            case ")":
                print("RIGHT_PAREN ) null")
            case "}":
                print("RIGHT_BRACE } null")
            case "{":
                print("LEFT_BRACE { null")
            case "*":
                print("STAR * null")
            case ".":
                print("DOT . null")
            case ",":
                print("COMMA , null")
            case "+":
                print("PLUS + null")
            case "-":
                print("MINUS - null")
            case ";":
                print("SEMICOLON ; null")
            case "\n":
                line += 1
            case _:
                print("[line "+str(line)+"] Error: Unexpected character: " + c)
                exit(65)
    print("EOF  null")


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

    tokenize(file_contents)


if __name__ == "__main__":
    main()
