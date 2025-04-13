from lexer import Lexer
from token_type import TokenType
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

        full_input = " ".join(lines)
        lexer = Lexer(full_input)
        tokens = lexer.tokenize()
        print_tokens(tokens)

def print_tokens(tokens):
    print("\nTokenized Output:")

    for token in tokens:
        token_type = token["type"]
        value = token["value"]

        if token_type == TokenType.KEYWORD:
            color = Fore.BLUE
        elif token_type == TokenType.FUNCTION:
            color = Fore.CYAN
        elif token_type == TokenType.IDENTIFIER:
            color = Fore.GREEN
        elif token_type == TokenType.NUMBER:
            color = Fore.YELLOW
        elif token_type == TokenType.STRING:
            color = Fore.MAGENTA
        elif token_type == TokenType.OPERATOR:
            color = Fore.RED
        elif token_type in {TokenType.PUNCTUATION, TokenType.BLOCK, TokenType.EXPRESSION_END}:
            color = Fore.WHITE
        elif token_type == TokenType.ERROR:
            color = Fore.LIGHTRED_EX
        else:
            color = Fore.RESET

        print(f"{color}{token_type.name}: {value}{Style.RESET_ALL}")

    print("\n")

if __name__ == "__main__":
    run_lexer()