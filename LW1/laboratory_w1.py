import random

class Grammar:
    def __init__(self, V_n, V_t, P, S):
        self.V_n = V_n  # non-terminal symbols
        self.V_t = V_t  # terminal symbols
        self.P = P  # the production rules for transformation
        self.S = S  # the start symbol

    def generate_strings(self, num_strings=5, max_conv=10):
        gen_str = []

        while len(gen_str) < num_strings:
            new_string = self.S
            steps = 0

            while any(symbol in self.V_n for symbol in new_string) and steps < max_conv:
                for i, symbol in enumerate(new_string):
                    if symbol in self.V_n:
                        replacements = self.P[symbol]
                        corresponding_replacement = random.choice(replacements)

                        # replaces non-terminal symbol at the first occurrence in the string
                        new_string = new_string[:i] + corresponding_replacement + new_string[i + 1:]
                        steps += 1
                        break

            if any(symbol in self.V_n for symbol in new_string):
                continue  # for skiping incomplete strings such as 'dabcabcabcA' since i set a limit of 10 conversions

            gen_str.append(new_string)

        return gen_str

    def to_finite_automaton(self):
        Q = set()  # the sttates
        Sigma = self.V_t  # input symbols
        Delta = {}  # the transition functions (delta)
        F = set()  # the final states
        state_mapping = {}  # the mapping of non-terminals to FA states

        # for better precaution let's ensure from the beginning that `S` is always `q0`
        state_mapping[self.S] = "q0"
        Q.add("q0")

        # assign states to non-terminals except the 'S'
        state_index = 1
        for vn in sorted(self.V_n):
            if vn == self.S:  # skiping S since we already assigned q0
                continue
            state_mapping[vn] = f"q{state_index}"
            Q.add(state_mapping[vn])
            state_index += 1

        q0 = state_mapping[self.S]

        # now we need to define the transitions(delta) and determine the final states
        for vn, prods in self.P.items():
            current_state = state_mapping[vn]

            for prod in prods:
                first_symbol = prod[0]  # first character in production

                if first_symbol in self.V_t:
                    if len(prod) == 1:
                        next_state = "qf"  # it's a final state
                    else:
                        next_non_terminal = prod[1:]
                        next_state = state_mapping.get(next_non_terminal, "qf")

                    if (current_state, first_symbol) not in Delta:
                        Delta[(current_state, first_symbol)] = set()
                    Delta[(current_state, first_symbol)].add(next_state)

        # finding the final states (non-terminals producing only terminals)
        for vn, prods in self.P.items():
            for prod in prods:
                if all(symbol in self.V_t for symbol in prod):  # if the production contains only terminals
                    F.add(state_mapping[vn])

        print("\nTransitions (Delta):")
        for key, value in Delta.items():
            print(f"  {key} → {value}")

        print("Final States:", F)

        return FiniteAutomaton(Q, Sigma, Delta, q0, F)


class FiniteAutomaton:
    def __init__(self, Q, Sigma, Delta, q0, F):
        self.Q = Q
        self.Sigma = Sigma
        self.Delta = Delta
        self.q0 = q0
        self.F = F

    def string_belong_to_language(self, str_input):
        state_current = {self.q0}  # tracking also for the case of multiple states like in NFA

        for k in str_input:
            next_state = set()
            for state in state_current:
                if (state, k) in self.Delta:
                    next_state.update(self.Delta[(state, k)])

            if not next_state:
                return False

            state_current = next_state

        # checking if any final state is reached, including 'qf'
        return any(state in self.F or state == 'qf' for state in state_current)

def grammar_var20():
    V_n = {"S", "A", "B", "C"}
    V_t = {"a", "b", "c", "d"}
    P = {
        "S": ["dA"],
        "A": ["d", "aB"],
        "B": ["bC"],
        "C": ["cA", "aS"]
    }
    S = "S"

    return Grammar(V_n, V_t, P, S)

class Main:
    @staticmethod
    def run():
        # use the predefined grammar in the function grammar_var20
        grammar = grammar_var20()

        # generate valid strings from the grammar
        generated_str = grammar.generate_strings()
        print("The 5 Generated Strings from Grammar:", generated_str)

        # convert Grammar to Finite Automaton
        finite_automaton = grammar.to_finite_automaton()

        # test if FA accepts generated strings
        print("\nTesting FA with generated strings:")
        for test in generated_str:
            is_valid = finite_automaton.string_belong_to_language(test)
            print(f"Does the FA accept '{test}'? {is_valid}")

        # additional tests
        custom_str = ["dd", "dabadabacd", "dabcd", "abc"]
        print("\nTesting FA with custom strings:")
        for test in custom_str:
            is_valid = finite_automaton.string_belong_to_language(test)
            print(f"Does the FA accept '{test}'? {is_valid}")

if __name__ == "__main__":
    Main.run()

