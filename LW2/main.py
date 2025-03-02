from finite_automaton import FiniteAutomaton, print_fa
import grammar as gr
import visualization as vs

# Define Grammar (Variant 20)
V_n = {"S", "A", "B", "C"}
V_t = {"a", "b", "c", "d"}
P = {
    "S": ["dA"],
    "A": ["d", "aB"],
    "B": ["bC"],
    "C": ["cA", "aS"]
}
S = "S"
grammar = gr.Grammar(V_n, V_t, P, S)

# Convert Grammar to FA
grammar_fa = grammar.to_finite_automaton()
print("\nGrammar converted to Finite Automaton:")
print_fa(grammar_fa)
vs.visualize_fa(grammar_fa, "grammar_to_fa")


# Define Finite Automaton (Variant 20)
Q = {"q0", "q1", "q2", "q3"}
Sigma = {"a", "b", "c"}
Delta = {
    ("q0", "a"): {"q0", "q1"},
    ("q1", "b"): {"q2"},
    ("q2", "a"): {"q2"},
    ("q2", "c"): {"q3"},
    ("q3", "c"): {"q3"},
}
q0 = "q0"
F = {"q3"}

finite_automaton = FiniteAutomaton(Q, Sigma, Delta, q0, F)

# Print and visualize FA
print("\nOriginal Finite Automaton:")
print_fa(finite_automaton)
vs.visualize_fa(finite_automaton, "finite_automaton")


# Convert FA to Regular Grammar
converted_grammar = finite_automaton.convert_fa_to_rg()

print("\nFinite Automaton converted to Regular Grammar:")
print(f"VN (Non-terminals): {converted_grammar.V_n}")
print(f"VT (Terminals): {converted_grammar.V_t}")
print(f"Start Symbol: {converted_grammar.S}")
print("Production Rules:")
for lhs, rhs in converted_grammar.P.items():
    print(f"  {lhs} → {' | '.join(rhs)}")


print("\nConverted DFA:")
print_fa(dfa)
vs.visualize_fa(dfa, "converted_dfa")

