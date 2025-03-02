import grammar as gr
import visualization as vs
class FiniteAutomaton:
    def __init__(self, Q, Sigma, Delta, q0, F):
        """ The Constructor of the class. """
        self.Q = Q
        self.Sigma = Sigma
        self.Delta = Delta
        self.q0 = q0
        self.F = F

    def convert_fa_to_rg(self):
        """ Converts a Finite Automaton (FA) to a Regular Grammar (RG) """
        V_n = self.Q  # V_n non-terminals are the FA states
        V_t = self.Sigma  # V_t terminals are the FA alphabet
        P = {}  # the roduction rules
        S = self.q0  # start symbol is the FA's start state

        # initializing the production rules
        for state in self.Q:
            P[state] = []

        # converting transitions to production rules
        # (state, input) -> next_state; turns into
        # state -> input next_state
        for (state, symbol), next_states in self.Delta.items():
            for next_state in next_states:
                P[state].append(symbol + next_state)  # ex of regular grammar rule: A -> aB

        # adding ε-transition if a final state can terminate
        for final_state in self.F:
            P[final_state].append("ε")

        return gr.Grammar(V_n, V_t, P, S)

    def is_deterministic(self):
        """Checks if the finite automaton is deterministic (DFA) or non-deterministic (NDFA)."""
        for (state, symbol), next_states in self.Delta.items():
            if len(next_states) > 1:
                return False  # more than one transition for the same state-symbol pair -> NDFA
            if symbol == "ε":
                return False  # the presence of ε-transition -> NDFA
        return True

    def string_belong_to_language(self, str_input, visualize=False):
        state_current = {self.q0}
        steps = []

        for k in str_input:
            next_state = set()
            for state in state_current:
                if (state, k) in self.Delta:
                    next_state.update(self.Delta[(state, k)])

            steps.append((state_current, k, next_state))  # Save for visualization

            if not next_state:
                return False

            state_current = next_state

        accepted = any(state in self.F for state in state_current)
        return accepted

    def convert_ndfa_to_dfa(self, visualize=False):
        """ Converts an NDFA to a DFA using the subset construction method. """
        new_states = {frozenset([self.q0])}  # start state as a set
        new_delta = {}  # DFA transition table
        new_final_states = set()
        unprocessed_states = [frozenset([self.q0])]
        steps = []  # storing steps for visualization

        state_name_map = {frozenset([self.q0]): "q0"}  # assigning readable names (like "q0_q1")

        def format_state(state_set):
            """ Converts a frozenset into a readable string. """
            return "_".join(sorted(state_set))

        while unprocessed_states:
            current_set = unprocessed_states.pop()
            formatted_current = format_state(current_set)  # format DFA state properly

            for symbol in self.Sigma:
                next_set = set()
                for state in current_set:
                    if (state, symbol) in self.Delta:
                        next_set.update(self.Delta[(state, symbol)])

                if next_set:
                    next_set = frozenset(next_set)
                    formatted_next = format_state(next_set)

                    if next_set not in state_name_map:
                        state_name_map[next_set] = formatted_next
                        new_states.add(next_set)
                        unprocessed_states.append(next_set)

                    new_delta[(formatted_current, symbol)] = {formatted_next}
                    steps.append((formatted_current, symbol, formatted_next))

        for state_set in new_states:
            if any(s in self.F for s in state_set):
                new_final_states.add(state_name_map[state_set])

        if visualize:
            vs.visualize_dfa_conversion(steps)

        return FiniteAutomaton(set(state_name_map.values()), self.Sigma, new_delta, "q0", new_final_states)


def print_fa(fa, formatted=False):
    """Prints the finite automaton in a readable format."""
    print("\nFinite Automaton Representation\n")

    print(f"States (Q): {set(fa.Q)}")
    print(f"Alphabet (Σ): {set(fa.Sigma)}")
    print(f"Initial State (q0): {fa.q0}")
    print(f"Final States (F): {set(fa.F)}\n")

    print("Transitions (Delta):")
    for (state, symbol), next_states in fa.Delta.items():
        # converts frozensets to strings for cleaner output
        state = ", ".join(sorted(state)) if isinstance(state, frozenset) else state
        next_states = {", ".join(sorted(ns)) if isinstance(ns, frozenset) else ns for ns in next_states}

        if formatted:
            print(f"('{state}', '{symbol}') -> {next_states}")
        else:
            for next_state in next_states:
                print(f"  {state} -- {symbol} --> {next_state}")

    print("\nFA Transformation Completed!\n")


