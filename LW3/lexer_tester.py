import re
from lexer import Lexer


def run_lexer():
    print("Enter ChemOrg DSL code (press Enter twice to run, type 'exit' to quit):")

    while True:
        lines = []
        while True:
            user_input = input(">>> ").strip()
            if user_input == "exit":
                return
            if user_input == "":  # If user presses Enter twice, process input
                break
            lines.append(user_input)

        full_input = " ".join(lines)  # Combine lines into one string
        lexer = Lexer(full_input)
        tokens = lexer.tokenize()
        print_tokens(tokens)


def print_tokens(tokens):
    print("\nTokenized Output:")
    for token in tokens:
        print(f"{token['type']}: {token['value']}")
    print("\n")


if __name__ == "__main__":
    run_lexer()
