import tkinter as tk
from lexer import Lexer
from chem_parser import Parser
from token_type import TokenType
from tkinter import scrolledtext, Toplevel, Label
from ast_nodes import *
import tkinter.font as tkFont
import graphviz
from PIL import Image, ImageTk
import os
import uuid

def run_parser():
    code = text_input.get("1.0", tk.END).strip()
    output.configure(state='normal')
    output.delete("1.0", tk.END)

    lexer = Lexer(code)
    try:
        tokens = lexer.tokenize()
        output.insert(tk.END, "Tokens:\n", 'header')
        for t in tokens:
            tag = t['type'].name.lower()
            output.insert(tk.END, f"{t['type'].name}: {t['value']}\n", tag)
    except Exception as e:
        output.insert(tk.END, f"Lexer Error: {e}\n", 'error')
        output.configure(state='disabled')
        return

    try:
        parser = Parser(tokens)
        global last_ast
        last_ast = parser.parse()
        output.insert(tk.END, "\nParsed AST:\n", 'header')
        output.insert(tk.END, last_ast.pretty(), 'ast')
    except Exception as e:
        output.insert(tk.END, f"\nParser Error: {e}\n", 'error')

    output.configure(state='disabled')

def visualize_ast():
    if last_ast is None:
        return

    dot = graphviz.Digraph(graph_attr={"rankdir": "TB"})

    def add_node(node):
        node_id = str(uuid.uuid4())

        if isinstance(node, Program):
            label = "Program"
            dot.node(node_id, label, shape="box", style="filled", fillcolor="#D0F0C0")
            for stmt in node.statements:
                child_id = add_node(stmt)
                dot.edge(node_id, child_id)

        elif isinstance(node, LetStatement):
            label = f"Let: {node.identifier.name}"
            dot.node(node_id, label, shape="box", style="filled", fillcolor="#AEDFF7")
            if node.expression:
                expr_id = add_node(node.expression)
                dot.edge(node_id, expr_id, label="= expr")

        elif isinstance(node, FunctionCall):
            label = f"Function: {node.name}"
            dot.node(node_id, label, shape="box", style="filled", fillcolor="#FFE4B5")
            for i, arg in enumerate(node.arguments):
                arg_id = add_node(arg)
                dot.edge(node_id, arg_id, label=f"arg[{i}]")

        elif isinstance(node, IfStatement):
            label = "If"
            dot.node(node_id, label, shape="box", style="filled", fillcolor="#FCD5CE")
            cond_id = add_node(node.condition)
            dot.edge(node_id, cond_id, label="condition")

            if node.true_branch:
                block_id = str(uuid.uuid4())
                dot.node(block_id, "if-body", shape="plaintext")
                dot.edge(node_id, block_id)
                for stmt in node.true_branch:
                    stmt_id = add_node(stmt)
                    dot.edge(block_id, stmt_id)

            for elif_cond, elif_body in node.elif_branches:
                ec_id = add_node(elif_cond)
                dot.edge(node_id, ec_id, label="elif-cond")
                elif_block_id = str(uuid.uuid4())
                dot.node(elif_block_id, "elif-body", shape="plaintext")
                dot.edge(node_id, elif_block_id)
                for stmt in elif_body:
                    eb_id = add_node(stmt)
                    dot.edge(elif_block_id, eb_id)

            if node.else_branch:
                else_block_id = str(uuid.uuid4())
                dot.node(else_block_id, "else-body", shape="plaintext")
                dot.edge(node_id, else_block_id)
                for stmt in node.else_branch:
                    else_id = add_node(stmt)
                    dot.edge(else_block_id, else_id)

        elif isinstance(node, BinaryOperation):
            label = f"Operator: {node.operator}"
            dot.node(node_id, label, shape="ellipse", style="filled", fillcolor="#FFFACD")
            left_id = add_node(node.left)
            right_id = add_node(node.right)
            dot.edge(node_id, left_id, label="left")
            dot.edge(node_id, right_id, label="right")

        elif isinstance(node, Literal):
            label = f"Literal: {node.value}"
            dot.node(node_id, label, shape="ellipse", style="filled", fillcolor="#E0BBE4")

        elif isinstance(node, Identifier):
            label = f"Identifier: {node.name}"
            dot.node(node_id, label, shape="ellipse", style="filled", fillcolor="#B5EAD7")

        return node_id

    add_node(last_ast)
    dot_path = "ast.png"
    dot.render("ast", format='png', cleanup=True)

    img = Image.open(dot_path)
    popup = Toplevel(app)
    popup.title("AST Visualization")
    img = ImageTk.PhotoImage(img)
    label = Label(popup, image=img)
    label.image = img  # Keep a reference!
    label.pack()

def setup_tags(widget):
    widget.tag_config('header', foreground='black', font=('Courier', 10, 'bold'))
    widget.tag_config('keyword', foreground='blue')
    widget.tag_config('function', foreground='cyan')
    widget.tag_config('identifier', foreground='green')
    widget.tag_config('number', foreground='orange')
    widget.tag_config('string', foreground='magenta')
    widget.tag_config('operator', foreground='red')
    widget.tag_config('punctuation', foreground='gray')
    widget.tag_config('block', foreground='darkgray')
    widget.tag_config('expression_end', foreground='gray')
    widget.tag_config('error', foreground='red', font=('Courier', 10, 'bold'))
    widget.tag_config('ast', foreground='black')

last_ast = None

app = tk.Tk()
app.title("ChemOrg DSL Parser")

text_input = tk.Text(app, height=10, width=90, font=("Courier", 10))
text_input.pack(padx=10, pady=5)

parse_button = tk.Button(app, text="Parse", command=run_parser)
parse_button.pack(pady=5)

visualize_button = tk.Button(app, text="Visualize AST", command=visualize_ast)
visualize_button.pack(pady=5)

output = scrolledtext.ScrolledText(app, height=25, width=90, font=("Courier", 10), bg="#f5f5f5")
output.pack(padx=10, pady=5)
setup_tags(output)
output.configure(state='disabled')

app.mainloop()
