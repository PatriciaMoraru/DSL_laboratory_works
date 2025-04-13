from abc import ABC, abstractmethod

class ASTNode(ABC):
    @abstractmethod
    def __repr__(self):
        pass

    def pretty(self, indent=0):
        return "  " * indent + repr(self)


class Program(ASTNode):
    def __init__(self, statements):
        self.statements = statements  # list of ASTNode

    def __repr__(self):
        return f"Program({self.statements})"

    def pretty(self, indent=0):
        out = "  " * indent + "Program([\n"
        for stmt in self.statements:
            out += stmt.pretty(indent + 1) + ",\n"
        out += "  " * indent + "])"
        return out


class LetStatement(ASTNode):
    def __init__(self, identifier, expression):
        self.identifier = identifier
        self.expression = expression

    def __repr__(self):
        return f"Let({self.identifier} = {self.expression})"

    def pretty(self, indent=0):
        return "  " * indent + f"Let({self.identifier.pretty()} = {self.expression.pretty() if self.expression else 'None'})"


class FunctionCall(ASTNode):
    def __init__(self, name, arguments):
        self.name = name
        self.arguments = arguments  # list of expressions

    def __repr__(self):
        return f"Call({self.name}({', '.join(map(str, self.arguments))}))"

    def pretty(self, indent=0):
        args = ", ".join(arg.pretty() for arg in self.arguments)
        return "  " * indent + f"Call({self.name}({args}))"


class IfStatement(ASTNode):
    def __init__(self, condition, true_branch, elif_branches=None, else_branch=None):
        self.condition = condition
        self.true_branch = true_branch
        self.elif_branches = elif_branches or []
        self.else_branch = else_branch

    def __repr__(self):
        elif_repr = "".join([f" elif ({cond}) {{ {stmts} }}" for cond, stmts in self.elif_branches])
        else_repr = f" else {{ {self.else_branch} }}" if self.else_branch else ""
        return f"If({self.condition}) {{ {self.true_branch} }}{elif_repr}{else_repr}"

    def pretty(self, indent=0):
        out = "  " * indent + f"If({self.condition.pretty()}) {{\n"
        for stmt in self.true_branch:
            out += stmt.pretty(indent + 1) + "\n"
        out += "  " * indent + "}"
        for cond, stmts in self.elif_branches:
            out += f"\n{'  ' * indent}elseif ({cond.pretty()}) {{\n"
            for stmt in stmts:
                out += stmt.pretty(indent + 1) + "\n"
            out += "  " * indent + "}"
        if self.else_branch:
            out += f"\n{'  ' * indent}else {{\n"
            for stmt in self.else_branch:
                out += stmt.pretty(indent + 1) + "\n"
            out += "  " * indent + "}"
        return out


class BinaryOperation(ASTNode):
    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right

    def __repr__(self):
        return f"({self.left} {self.operator} {self.right})"

    def pretty(self, indent=0):
        return "  " * indent + f"({self.left.pretty()} {self.operator} {self.right.pretty()})"


class Literal(ASTNode):
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f"Literal({self.value})"

    def pretty(self, indent=0):
        return "  " * indent + f"Literal({self.value})"


class Identifier(ASTNode):
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f"Identifier({self.name})"

    def pretty(self, indent=0):
        return "  " * indent + f"Identifier({self.name})"
