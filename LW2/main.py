from finite_automaton import FiniteAutomaton, print_fa
from grammar import Grammar
import visualization as vs

class Main:
    def __init__(self):
        self.run()

    def run(self):

        # 1. Define Variant 20 Grammar
        V_n = {"S", "A", "B", "C"}
        V_t = {"a", "b", "c", "d"}
        P = {
            "S": ["dA"],
            "A": ["d", "aB"],
            "B": ["bC"],
            "C": ["cA", "aS"]
        }
        S = "S"
        grammar = Grammar(V_n, V_t, P, S)

        # 2. Classify Grammar
        print("\nGrammar Classification:")
        print(grammar.classify_grammar())

        # 3. Convert Grammar to Finite Automaton
        grammar_fa = grammar.to_finite_automaton()
        print("\nGrammar converted to Finite Automaton:")
        print_fa(grammar_fa, formatted=True)

        # 4. Define Variant 20 Finite Automaton
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

        # 5. Print FA Details
        print("\nOriginal Finite Automaton:")
        print_fa(finite_automaton, formatted=True)

        # 6. Convert FA to Regular Grammar
        converted_grammar = finite_automaton.convert_fa_to_rg()
        print("\nFinite Automaton converted to Regular Grammar:")
        print(f"VN (Non-terminals): {converted_grammar.V_n}")
        print(f"VT (Terminals): {converted_grammar.V_t}")
        print(f"Start Symbol: {converted_grammar.S}")
        print("Production Rules:")
        for lhs, rhs in converted_grammar.P.items():
            print(f"  {lhs} → {' | '.join(rhs)}")

        # 7. Check if FA is Deterministic
        print("\nFA Deterministic Check:")
        print("✅ Deterministic" if finite_automaton.is_deterministic() else "Non-Deterministic")

        # 8. Convert NDFA to DFA
        dfa = finite_automaton.convert_ndfa_to_dfa()
        print("\nConverted DFA:")
        print_fa(dfa, formatted=True)

        # 9. Generate Visualizations
        vs.visualize_fa(finite_automaton, "finite_automaton")
        vs.visualize_fa(dfa, "converted_dfa")

if __name__ == "__main__":
    Main()
