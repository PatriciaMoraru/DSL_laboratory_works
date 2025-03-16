# Report nr.3: Lexer - Chemistry DSL

### Course: Formal Languages & Finite Automata
### Author: PATRICIA MORARU, FAF-233

----

# Theory
Lexical analysis, or lexing, is the process of converting a sequence of characters into tokens. A lexer (also called a tokenizer or scanner) is responsible for recognizing patterns in text and classifying different components such as keywords, identifiers, numbers, operators, and punctuation.

In this work, a lexer for the ChemOrg DSL was implemented. ChemOrg DSL is a domain-specific language used for chemical computations. The lexer takes a string of ChemOrg DSL code as input and processes it to generate a structured list of tokens that can later be used in parsing or interpretation.

The lexer follows a deterministic approach, scanning through the text character by character and grouping them based on language rules. This implementation supports:

- **Keywords**: `let`, `if`, `elif`, `else`
- **Functions specific to ChemOrg DSL**: `resolve`, `getVolume`, `isAcid`, etc.
- **Identifiers**: Any variable or user-defined name.
- **Numbers**: Integers and floating-point values.
- **Strings**: Enclosed within double quotes.
- **Operators & Symbols**: `+`, `-`, `*`, `/`, `=`, `()`, `{}`, etc.

# Objectives
1. Understand how a lexer processes an input stream into tokens.
2. Implement a custom lexer to recognize ChemOrg DSL-specific tokens.
3. Test the lexer by running ChemOrg DSL expressions and analyzing the tokenized output.

# Implementation Description

The implementation consists of a `Lexer` class that reads an input string and processes it into tokens. The lexer operates through the following steps:

## 1. Initialization and Input Handling

The `Lexer` class starts by initializing three attributes:

- `self.input`: Stores the input string.
- `self.position`: Tracks the current character index.
- `self.tokens`: A list where identified tokens are stored.

```python
import re

class Lexer:
    def __init__(self, input_text):
        self.input = input_text
        self.position = 0
        self.tokens = []
```

## 2. Tokenization Process

The lexer loops through the input string, character by character, and determines the type of token being processed. Whitespace is skipped, and based on the current character, an appropriate function is called:

- **Alphabetic characters** → Processed as **keywords, functions, or identifiers**.
- **Numbers** → Processed as **numeric tokens**.
- **Quotes (`"`)** → Processed as **string tokens**.
- **Operators or symbols** → Processed as **punctuation or special tokens**.

```python
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
```

## 3. Identifying Keywords, Functions, and Identifiers

When a word is encountered, the lexer needs to determine whether it is a:

- **Keyword** (e.g., `let`, `if`, `else`)
- **Function** (e.g., `getVolume`, `resolve`)
- **Identifier** (a variable name)

The lexer checks predefined sets of **keywords** and **functions**.  
If a match is found, the token is labeled accordingly. Otherwise, it is categorized as an **identifier**.

```python
def tokenize_identifier_or_keyword(self):
    start = self.position
    while not self.is_at_end() and self.is_alphanumeric(self.peek()):
        self.advance()
    text = self.input[start:self.position]

    keywords = {"let", "if", "elif", "else"}
    functions = {
        "resolve", "possible", "getOxidixngs", "getReducings",
        "show", "getMolecWeight", "getVolume", "getV", "isAcid", "isBase"
    }

    if text in keywords:
        self.tokens.append({"type": "KEYWORD_TOKEN", "value": text})
    elif text in functions:
        self.tokens.append({"type": "FUNCTION_TOKEN", "value": text})
    else:
        self.tokens.append({"type": "IDENTIFIER_TOKEN", "value": text})
```

## 4. Processing Numbers

Numbers in ChemOrg DSL can be **integers** (e.g., `42`, `100`) or **floating-point numbers** (e.g., `3.14`, `0.5`).  
The lexer must correctly identify numbers, ensuring that floating-point values are **not mistakenly split into separate tokens**.

#### **How Number Tokenization Works:**
- When the lexer encounters a **digit (0-9)**, it assumes the beginning of a numeric token.
- It continues scanning until a **non-numeric character** is found.
- If a **decimal point (`.`)** is encountered, the lexer ensures that it appears **only once** in the number.
- The extracted sequence is then stored as a **NUMBER_TOKEN**.

The following function processes both **integers** and **floating-point numbers**, ensuring correct handling of decimal values:

```python
def tokenize_number(self):
    start = self.position
    has_dot = False  
    
    while not self.is_at_end() and (self.is_digit(self.peek()) or (self.peek() == '.' and not has_dot)):
        if self.peek() == '.':
            has_dot = True  
        self.advance()

    text = self.input[start:self.position]
    self.tokens.append({"type": "NUMBER_TOKEN", "value": text})
```

## 5. Handling Strings and Errors

Strings in ChemOrg DSL are enclosed within **double quotes (`" "`)**.  
A string token may contain **letters, numbers, spaces, and special characters**.

#### **How String Tokenization Works:**
- The lexer **skips the opening quote (`"`)**.
- Characters are collected **until another quote (`"`) is found**.
- If the lexer **reaches the end of the input without finding a closing quote**, it generates an **error token**.
- **Escape sequences** (e.g., `\"`) are handled by skipping the escape character (`\`).

```python
def tokenize_string(self):
    self.advance()  
    start = self.position
    value = ""

    while not self.is_at_end() and self.peek() != '"':
        if self.peek() == '\n':  
            print(f"Error: Unterminated string at position {start}: \"{value}\"")
            self.tokens.append({"type": "ERROR", "value": "Unterminated string"})
            return

        if self.peek() == '\\': 
            self.advance()
        value += self.advance()

    if self.is_at_end():  
        print(f"Error: Unterminated string at position {start}: \"{value}\"")
        self.tokens.append({"type": "ERROR", "value": "Unterminated string"})
        return

    self.advance() 
    self.tokens.append({"type": "STRING_TOKEN", "value": value})
```

## 6. Recognizing Symbols and Operators

Operators and symbols are fundamental elements of ChemOrg DSL, allowing **mathematical operations**, **comparisons**, and **structural definitions**.  
The lexer needs to differentiate **operators (`+`, `-`, `=`, `>`, `<`)** and **punctuation (`()`, `{}`, `;`)** to correctly tokenize the input.

#### **How Symbol and Operator Tokenization Works:**
1. The lexer reads a **single character** and determines if it belongs to:
   - **Arithmetic operators**: `+`, `-`, `*`, `/`
   - **Comparison operators**: `>`, `<`, `=`, `!=`
   - **Grouping symbols**: `(`, `)`, `{`, `}`
   - **Separators**: `,`, `;`
2. If a **multi-character operator** (e.g., `>=`, `<=`, `!=`) is detected, the lexer **reads ahead** to form the full operator.
3. If the character **is not recognized**, an error is raised.

The following function processes symbols and operators, ensuring correct token classification:

```python
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
```

## 7. Testing the Lexer

To ensure that the lexer correctly identifies and processes tokens, an **interactive testing script (`lexer_tester.py`)** was implemented.  
This script allows users to **input ChemOrg DSL code**, process it through the lexer, and view the resulting tokens.

#### **How the Testing Script Works:**
1. The script **prompts the user** to enter ChemOrg DSL code.
2. The user **types multiple lines of input**, pressing **Enter twice** to process the input.
3. The script **sends the input to the lexer** for tokenization.
4. The **resulting tokens** are displayed in a readable format.
5. The user can **type 'exit'** to terminate the testing session.

The following function provides an **interactive lexer testing environment**:

```python
from lexer import Lexer

def run_lexer():
    print("Enter ChemOrg DSL code (press Enter twice to run, type 'exit' to quit):")

    while True:
        lines = []
        while True:
            user_input = input(">>> ").strip()
            if user_input == "exit":
                return
            if user_input == "":
                break
            lines.append(user_input)

        full_input = " ".join(lines)
        lexer = Lexer(full_input)
        tokens = lexer.tokenize()
        print_tokens(tokens)
```

## Conclusions

- The lexer successfully extracts **meaningful tokens** from ChemOrg DSL code.
- It handles **keywords, functions, numbers, strings, and operators** effectively.
- **Error handling** for unterminated strings was implemented to prevent parsing issues.
- The **interactive tester** allows quick validation of lexical analysis, making debugging easier.
