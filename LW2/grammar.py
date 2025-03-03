import random
import finite_automaton

class Grammar:
    def __init__(self, V_n, V_t, P, S):
        """ The Constructor of the class. """
        self.V_n = V_n  # non-terminal symbols
        self.V_t = V_t  # terminal symbols
        self.P = P  # the production rules for transformation
        self.S = S  # the start symbol

    def generate_strings(self, num_strings=5, max_conv=10):
        """ Generates a number of strings based on the given Grammar. """
        gen_str = [] # initializing an empty list where we will store the generated words

        while len(gen_str) < num_strings:
            new_string = self.S  # we start with the initial symbol of the grammar
            steps = 0

            # this loop will continue until there are no non-terminal symbols left
            while any(symbol in self.V_n for symbol in new_string) and steps < max_conv:
                # scans the new_string for V_n, collects their position and their symbols
                possible_replacements = [(i, symbol) for i, symbol in enumerate(new_string) if symbol in self.P]

                if not possible_replacements:
                    break

                # if there are multiple production rules for a single symbol we pick one randomly
                i, symbol = random.choice(possible_replacements)
                new_string = new_string[:i] + random.choice(self.P[symbol]) + new_string[i + 1:]
                steps += 1

            #if we get to the established lenght of the word and it still contains V_n we discrd it
            if any(symbol in self.V_n for symbol in new_string):
                continue

            gen_str.append(new_string)
        return gen_str

    def classify_grammar(self):
        """ Classifies the grammar based on Chomsky hierarchy. """
        # this will be our classification flags
        type3_regular = True
        type2_context_free = True
        type1_context_sensitive = True

        # checking for empty productions in the right-hand side
        contains_empty_string= any("ε" in rhs_list for rhs_list in self.P.values())

        # checking if the start symbol can derive into empty since for some types of gr this is allowed only if S doesnt appera on the rhs of other rule
        start_symbol_derives_into_empty = "ε" in self.P.get(self.S, [])

        # now we check if S appears in any rhs
        start_symbol_appears_rhs = any(self.S in rhs for rhs_list in self.P.values() for rhs in rhs_list)

        # now we will loop through every production rule
        for lhs, rhs_list in self.P.items():
            # from start we check how many symbols are on the lhs to exclude type2 and 3
            if len(lhs) > 1:
                type2_context_free = False  # type 2 requires single non-terminal LHS
                type3_regular = False  # regular grammars also require single non-terminal LHS
            for rhs in rhs_list:
                # rhs must be at least as long as lhs
                if len(rhs) < len(lhs):
                    type1_context_sensitive = False  # type 1 must have non-shrinking rules
                if any(sym in self.V_n for sym in rhs):  # doing checks for regular grammar
                    if not (rhs[0] in self.V_t and (len(rhs) == 1 or rhs[1] in self.V_n)):
                        type3_regular = False  # type 3 must follow strict left/right linearity

        if type3_regular:
            if contains_empty_string:
                if start_symbol_derives_into_empty and not start_symbol_appears_rhs:
                    return "Type 3: Regular Grammar"  # regular grammar allows ε only if start symbol isn't used elsewhere
            else:
                return "Type 3: Regular Grammar"
        elif type2_context_free:
            if contains_empty_string and not start_symbol_appears_rhs:
                return "Type 2: Context-Free Grammar"  # CFG allows ε under constraints
            return "Type 2: Context-Free Grammar"
        elif type1_context_sensitive:
            return "Type 1: Context-Sensitive Grammar"
        else:
            return "Type 0: Unrestricted Grammar"

    def to_finite_automaton(self):
        """ Converts Grammar to Finite Automaton. """
        Q = set()  # set of the states
        Sigma = self.V_t  # the input symbols (the terminals)
        Delta = {}  # the transition function (production rules)
        F = set()  # the final states
        state_mapping = {} # maps grammar non-terminals to FA states

        # we need to ensure S is always q0
        state_mapping[self.S] = "q0"
        Q.add("q0")

        # assigning states to non-terminals
        state_index = 1
        for vn in sorted(self.V_n):
            if vn == self.S:
                continue # skipping S since it was already assigned
            state_mapping[vn] = f"q{state_index}"
            Q.add(state_mapping[vn])
            state_index += 1

        # track non-terminals that appear in RHS of productions to determine the final states later
        #if a V_n never appears on the right the its FA state is final
        appearing_non_terminals = set()
        for productions in self.P.values():
            for prod in productions:
                for symbol in prod:
                    if symbol in self.V_n:
                        appearing_non_terminals.add(symbol)

        # defining the transitions
        for vn, prods in self.P.items():
            current_state = state_mapping[vn]
            for prod in prods:
                first_symbol = prod[0]

                # determine next state
                if len(prod) == 1 and first_symbol in self.V_t:
                    next_state = "qf"  # if only a terminal remains, then transition to final state
                else:
                    next_non_terminal = prod[1:]  # get next part
                    next_state = state_mapping.get(next_non_terminal, "qf")

                # creating the transitions and storing them
                if (current_state, first_symbol) not in Delta:
                    Delta[(current_state, first_symbol)] = set()
                Delta[(current_state, first_symbol)].add(next_state)

        # determining the final states
        for vn, prods in self.P.items():
            for prod in prods:
                # If a production directly leads to a terminal (A → d), its FA state is final
                if len(prod) == 1 and prod in self.V_t:
                    F.add(state_mapping[vn])

        # ensuring there's at least one final state, but don't adding 'qf' unnecessarily
        if not F:
            F.add(state_mapping[self.S])  # default to start state only if no other finals exist

        return finite_automaton.FiniteAutomaton(Q, Sigma, Delta, "q0", F)