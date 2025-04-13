from ast_nodes import *
from token_type import TokenType

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.position = 0

    def peek(self):
        return self.tokens[self.position] if self.position < len(self.tokens) else None

    def advance(self):
        current = self.peek()
        self.position += 1
        return current

    def expect(self, token_type, value=None):
        token = self.peek()
        if not token or token["type"] != token_type or (value is not None and token["value"] != value):
            raise SyntaxError(f"Expected {token_type} {value}, got {token}")
        return self.advance()

    def match(self, token_type, value=None):
        token = self.peek()
        if token and token["type"] == token_type and (value is None or token["value"] == value):
            return self.advance()
        return None

    def parse(self):
        return Program(self.parse_statement_list())

    def parse_statement_list(self):
        statements = []
        while self.peek() and self.peek()["type"] in {TokenType.KEYWORD, TokenType.IDENTIFIER, TokenType.FUNCTION}:
            statements.append(self.parse_statement())
        return statements

    def parse_statement(self):
        token = self.peek()
        if token["type"] == TokenType.KEYWORD and token["value"] == "let":
            node = self.parse_assignment()
        elif token["type"] == TokenType.IDENTIFIER:
            node = self.parse_assignment()
        elif token["type"] == TokenType.KEYWORD and token["value"] == "if":
            return self.parse_if_statement()
        elif token["type"] == TokenType.FUNCTION:
            node = self.parse_function_call()
        else:
            raise SyntaxError(f"Unexpected statement token: {token}")

        self.expect(TokenType.EXPRESSION_END)
        return node

    def parse_assignment(self):
        if self.match(TokenType.KEYWORD, "let"):
            ident = self.expect(TokenType.IDENTIFIER)
            if self.match(TokenType.OPERATOR, "="):
                expr = self.parse_expression()
                return LetStatement(Identifier(ident["value"]), expr)
            return LetStatement(Identifier(ident["value"]), None)
        else:
            ident = self.expect(TokenType.IDENTIFIER)
            self.expect(TokenType.OPERATOR, "=")
            expr = self.parse_expression()
            return LetStatement(Identifier(ident["value"]), expr)

    def parse_expression(self):
        return self.parse_comparison()

    def parse_comparison(self):
        left = self.parse_additive()
        while self.peek() and self.peek()["type"] == TokenType.OPERATOR and self.peek()["value"] in {"<", "<=", ">", ">=", "==", "!="}:
            op = self.advance()["value"]
            right = self.parse_additive()
            left = BinaryOperation(left, op, right)
        return left

    def parse_additive(self):
        left = self.parse_primary()
        while self.peek() and self.peek()["type"] == TokenType.OPERATOR and self.peek()["value"] == "+":
            op = self.advance()["value"]
            right = self.parse_primary()
            left = BinaryOperation(left, op, right)
        return left

    def parse_primary(self):
        token = self.peek()
        if token["type"] == TokenType.STRING:
            return Literal(self.advance()["value"])
        elif token["type"] == TokenType.NUMBER:
            return Literal(self.advance()["value"])
        elif token["type"] == TokenType.IDENTIFIER:
            return Identifier(self.advance()["value"])
        elif token["type"] == TokenType.FUNCTION:
            return self.parse_function_call()
        elif token["type"] == TokenType.PUNCTUATION and token["value"] == "(":
            self.advance()
            expr = self.parse_expression()
            self.expect(TokenType.PUNCTUATION, ")")
            return expr
        else:
            raise SyntaxError(f"Unexpected token in expression: {token}")

    def parse_function_call(self):
        func_name = self.advance()["value"]
        self.expect(TokenType.PUNCTUATION, "(")

        args = []
        while not self.match(TokenType.PUNCTUATION, ")"):
            args.append(self.parse_expression())
            if not self.match(TokenType.PUNCTUATION, ","):
                self.expect(TokenType.PUNCTUATION, ")")
                break

        return FunctionCall(func_name, args)

    def parse_if_statement(self):
        self.expect(TokenType.KEYWORD, "if")
        self.expect(TokenType.PUNCTUATION, "(")
        condition = self.parse_expression()
        self.expect(TokenType.PUNCTUATION, ")")
        self.expect(TokenType.BLOCK, "{")
        true_branch = self.parse_statement_list()
        self.expect(TokenType.BLOCK, "}")

        elif_branches = []
        while self.match(TokenType.KEYWORD, "elif"):
            self.expect(TokenType.PUNCTUATION, "(")
            elif_cond = self.parse_expression()
            self.expect(TokenType.PUNCTUATION, ")")
            self.expect(TokenType.BLOCK, "{")
            elif_body = self.parse_statement_list()
            self.expect(TokenType.BLOCK, "}")
            elif_branches.append((elif_cond, elif_body))

        else_branch = None
        if self.match(TokenType.KEYWORD, "else"):
            self.expect(TokenType.BLOCK, "{")
            else_branch = self.parse_statement_list()
            self.expect(TokenType.BLOCK, "}")

        return IfStatement(condition, true_branch, elif_branches, else_branch)
