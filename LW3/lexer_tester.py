import re
from lexer import Lexer
from colorama import Fore, Style


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
        token_type = token["type"]
        value = token["value"]

        if token_type == "KEYWORD_TOKEN":
            color = Fore.BLUE
        elif token_type == "FUNCTION_TOKEN":
            color = Fore.CYAN
        elif token_type == "IDENTIFIER_TOKEN":
            color = Fore.GREEN
        elif token_type == "NUMBER_TOKEN":
            color = Fore.YELLOW
        elif token_type == "STRING_TOKEN":
            color = Fore.MAGENTA
        elif token_type == "OPERATOR_TOKEN":
            color = Fore.RED
        elif token_type in {"PUNCTUATION_TOKEN", "BLOCK_TOKEN", "EXP"}:
            color = Fore.WHITE
        else:
            color = Fore.RESET

        print(f"{color}{token_type}: {value}{Style.RESET_ALL}")

    print("\n")


if __name__ == "__main__":
    run_lexer()
