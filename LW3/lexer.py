import re

class Lexer:
    def __init__(self, input_text):
        self.input = input_text
        self.position = 0
        self.tokens = []

    def is_at_end(self):
        return self.position >= len(self.input)

    def peek(self):
        return self.input[self.position] if not self.is_at_end() else None

    def peek_ahead(self, n=1):
        return self.input[self.position + n] if self.position + n < len(self.input) else None

    def advance(self):
        self.position += 1
        return self.input[self.position - 1]

    def tokenize(self):
        while not self.is_at_end():
            self.skip_whitespace()
            if self.is_at_end():
                break

            ch = self.peek()

            if self.is_alpha(ch):
                self.tokenize_identifier_or_keyword()
            elif self.is_digit(ch):
                self.tokenize_number()
            elif ch == '"':
                self.tokenize_string()
            else:
                self.tokenize_symbol()

        return self.tokens

    def skip_whitespace(self):
        while not self.is_at_end() and self.peek().isspace():
            self.advance()

    def is_alpha(self, ch):
        return re.match(r'[a-zA-Z]', ch) is not None

    def is_digit(self, ch):
        return re.match(r'[0-9]', ch) is not None

    def is_alphanumeric(self, ch):
        return re.match(r'[a-zA-Z0-9]', ch) is not None

    def tokenize_identifier_or_keyword(self):
        start = self.position
        while not self.is_at_end() and self.is_alphanumeric(self.peek()):
            self.advance()
        text = self.input[start:self.position]

        keywords = {"let", "if", "elif", "else"}

        # Function names in the ChemOrg DSL
        functions = {
            "resolve", "possible", "getOxidixngs", "getReducings", "show",
            "getMolecWeight", "getVolume", "getV", "isAcid", "isBase"
        }

        if text in keywords:
            self.tokens.append({"type": "KEYWORD_TOKEN", "value": text})
        elif text in functions:
            self.tokens.append({"type": "FUNCTION_TOKEN", "value": text})
        else:
            self.tokens.append({"type": "IDENTIFIER_TOKEN", "value": text})

    def tokenize_number(self):
        start = self.position
        while not self.is_at_end() and self.is_digit(self.peek()):
            self.advance()
        text = self.input[start:self.position]
        self.tokens.append({"type": "NUMBER_TOKEN", "value": text})

    def tokenize_string(self):
        self.advance()  # Skip opening "
        start = self.position
        value = ""

        while not self.is_at_end() and self.peek() != '"':
            if self.peek() == '\n':  # If a newline appears, stop parsing
                print(f"Error: Unterminated string at position {start}: \"{value}\"")
                self.tokens.append({"type": "ERROR", "value": "Unterminated string"})
                return  # Stop processing this token but continue lexing

            if self.peek() == '\\':  # Handle escape sequences
                self.advance()
            value += self.advance()

        if self.is_at_end():  # If we reach the end and still no closing "
            print(f"Error: Unterminated string at position {start}: \"{value}\"")
            self.tokens.append({"type": "ERROR", "value": "Unterminated string"})
            return  # Stop processing this token but continue lexing

        self.advance()  # Skip closing "

        # Split chemical formulas properly
        parts = re.split(r'(\s*[\+\-\*/]\s*)', value)  # Keep operators separate

        for part in parts:
            part = part.strip()  # Remove unnecessary spaces
            if part in {"+", "-", "*", "/"}:
                self.tokens.append({"type": "OPERATOR_TOKEN", "value": part})
            elif part:  # Avoid empty strings
                self.tokens.append({"type": "STRING_TOKEN", "value": part})

    def tokenize_symbol(self):
        ch = self.advance()
        if ch in {">", "<", "=", "!"} and self.peek() == "=":
            op = ch + self.advance()
            self.tokens.append({"type": "OPERATOR_TOKEN", "value": op})
            return

        symbol_map = {
            "+": "OPERATOR_TOKEN",
            ">": "OPERATOR_TOKEN",
            "<": "OPERATOR_TOKEN",
            "=": "OPERATOR_TOKEN",
            "(": "PUNCTUATION_TOKEN",
            ")": "PUNCTUATION_TOKEN",
            "{": "BLOCK_TOKEN",
            "}": "BLOCK_TOKEN",
            ",": "PUNCTUATION_TOKEN",
            ";": "EXP"
        }

        if ch in symbol_map:
            self.tokens.append({"type": symbol_map[ch], "value": ch})
        else:
            raise ValueError(f"Unexpected character: {ch}")
