from enum import Enum, auto


class TokenType(Enum):
    # Keywords
    KEYWORD = auto()

    # Functions specific to ChemOrg DSL
    FUNCTION = auto()

    # Identifiers (variable names)
    IDENTIFIER = auto()

    # Literals
    NUMBER = auto()
    STRING = auto()

    # Operators
    OPERATOR = auto()

    # Punctuation
    PUNCTUATION = auto()
    BLOCK = auto()
    EXPRESSION_END = auto()

    # Error handling
    ERROR = auto()
