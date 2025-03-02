# Report nr.2: Finite Automata

### Course: Formal Languages & Finite Automata
### Author: PATRICIA MORARU, FAF-233

----

# Theory

Finite automata (FA) are abstract mathematical models used to recognize patterns and define computational processes. They are widely applied in text processing, lexical analysis, and control systems. 

A **finite automaton (FA)** consists of:

1. **States**: Finite set of states **Q** (e.g., \{q₀, q₁, q₂, q₃\})
2. **Alphabet**: A finite set of input symbols **Σ** (e.g., \{a, b, c, d\})
3. **Transition function δ**: Defines state transitions based on input symbols.
4. **Start state q₀**: The initial state.
5. **Final states F**: States where the FA accepts a string.

In this work, we implemented various operations related to finite automata, including classifying a grammar based on the Chomsky hierarchy, converting a finite automaton to a regular grammar, checking if an FA is deterministic, and converting an NDFA into a DFA. Additionally, we visualized the automaton using external tools to validate correctness.


---

# Objectives

* Classify a given grammar based on the Chomsky hierarchy.
* Convert a finite automaton to a regular grammar.
* Determine whether the given finite automaton is deterministic (DFA) or non-deterministic (NDFA).
* Implement a function to convert an NDFA to a DFA using the subset construction method.
* Generate a visual representation of the finite automaton.


# Implementation Description

## **1. Grammar Classification**

A function was implemented in the `Grammar` class to classify a given grammar based on the Chomsky hierarchy. It determines whether the grammar is **regular (Type 3), context-free (Type 2), context-sensitive (Type 1), or unrestricted (Type 0)** based on the structure of the production rules.

```python
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
```
## **2. Converting FA to Regular Grammar**
A function was added in `FiniteAutomaton` to convert a finite automaton to a regular grammar. The transitions in the FA were transformed into production rules in the grammar.

```python
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
```

## **3. Checking if FA is Deterministic**
A function was implemented to check if the FA is deterministic by ensuring that each state-symbol pair has only one transition and that no epsilon (ε) transitions exist.

```python
    def is_deterministic(self):
        """Checks if the finite automaton is deterministic (DFA) or non-deterministic (NDFA)."""
        for (state, symbol), next_states in self.Delta.items():
            if len(next_states) > 1:
                return False  # more than one transition for the same state-symbol pair -> NDFA
            if symbol == "ε":
                return False  # the presence of ε-transition -> NDFA
        return True
```
## **4. Converting NDFA to DFA**
The subset construction method was used to convert an NDFA to a DFA. A new set of states was generated based on subsets of existing NDFA states.

```python
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
```
## **5. Graphical Representation**
Graphviz is used to create a visual representation of the FA, making it easier to understand.

```python
def visualize_fa(fa, filename="finite_automaton"):
    """Generates a graphical visualization of the finite automaton using Graphviz."""
    dot = graphviz.Digraph(format='png')
    dot.attr(rankdir='LR', size='10')

    def format_state(state):
        """Converts states (including frozensets) into readable names."""
        if isinstance(state, frozenset):
            return "_".join(sorted(state))
        return str(state)

    # adding the states
    for state in fa.Q:
        clean_state = format_state(state)
        if state in fa.F:
            dot.node(clean_state, shape="doublecircle", color="green")  # for final states
        else:
            dot.node(clean_state, shape="circle")

    # start state arrow
    dot.node("start", shape="none", width="0")
    dot.edge("start", format_state(fa.q0))

    # transitions
    for (state, symbol), next_states in fa.Delta.items():
        clean_state = format_state(state)
        for next_state in next_states:
            clean_next_state = format_state(next_state)
            dot.edge(clean_state, clean_next_state, label=symbol)

    dot.render(filename, view=True)
    print(f"Finite Automaton graph saved as {filename}.png")
```

# Conclusions

This laboratory work successfully demonstrated the connection between **regular grammars and finite automata**, providing a structured approach to **formal language processing**. 

Through **conversion between finite automata and regular grammars**, we explored the **deterministic and non-deterministic nature of automata** and implemented methods to **convert an NDFA into a DFA** using the **subset construction algorithm**.

Additionally, **graphical representations** of the automata provided a clearer understanding of **state transitions and language acceptance**, confirming the correctness of the transformations.

Python was chosen due to its **efficiency in handling automata operations**, **flexibility in working with sets and dictionaries**, and the availability of **graph visualization libraries** like **Graphviz** for automaton representation.

---

## Achievements:

- **Implemented a `Grammar` class** to represent a **right-linear grammar**.
- **Developed a method** to classify the grammar based on the **Chomsky hierarchy**.
- **Generated valid strings** from the language using **random derivations**.
- **Implemented FA to Regular Grammar conversion**, ensuring correct transition mapping.
- **Created an NDFA to DFA conversion function** using the **subset construction method**.
- **Implemented a check for FA determinism** to distinguish between **DFA and NDFA**.
- **Designed a visualization system** using **Graphviz** to represent FA and DFA structures.
- **Validated string acceptance** to determine whether a given input belongs to the language.

## Results:
### Output from console
```bash
Grammar Classification:
Type 3: Regular Grammar

Grammar converted to Finite Automaton:

Finite Automaton Representation

States (Q): {'q0', 'q2', 'q3', 'q1'}
Alphabet (Σ): {'c', 'a', 'b', 'd'}
Initial State (q0): q0
Final States (F): {'q1'}

Transitions (Delta):
('q0', 'd') -> {'q1'}
('q1', 'd') -> {'qf'}
('q1', 'a') -> {'q2'}
('q2', 'b') -> {'q3'}
('q3', 'c') -> {'q1'}
('q3', 'a') -> {'q0'}

FA Transformation Completed!


Original Finite Automaton:

Finite Automaton Representation

States (Q): {'q0', 'q2', 'q3', 'q1'}
Alphabet (Σ): {'c', 'a', 'b'}
Initial State (q0): q0
Final States (F): {'q3'}

Transitions (Delta):
('q0', 'a') -> {'q0', 'q1'}
('q1', 'b') -> {'q2'}
('q2', 'a') -> {'q2'}
('q2', 'c') -> {'q3'}
('q3', 'c') -> {'q3'}

FA Transformation Completed!


Finite Automaton converted to Regular Grammar:
VN (Non-terminals): {'q0', 'q2', 'q3', 'q1'}
VT (Terminals): {'c', 'a', 'b'}
Start Symbol: q0
Production Rules:
  q0 → aq0 | aq1
  q2 → aq2 | cq3
  q3 → cq3 | ε
  q1 → bq2

FA Deterministic Check:
Non-Deterministic

Converted DFA:

Finite Automaton Representation

States (Q): {'q0', 'q3', 'q0_q1', 'q2'}
Alphabet (Σ): {'c', 'a', 'b'}
Initial State (q0): q0
Final States (F): {'q3'}

Transitions (Delta):
('q0', 'a') -> {'q0_q1'}
('q0_q1', 'a') -> {'q0_q1'}
('q0_q1', 'b') -> {'q2'}
('q2', 'c') -> {'q3'}
('q2', 'a') -> {'q2'}
('q3', 'c') -> {'q3'}

FA Transformation Completed!

Finite Automaton graph saved as finite_automaton.png
Finite Automaton graph saved as converted_dfa.png
```

## Visualization
### NDFA Visualization

The original **Non-Deterministic Finite Automaton (NDFA)**:

![NDFA Visualization](finite_automaton.png)


---
### DFA Visualization

Here is the **converted DFA**:

![Converted DFA](converted_dfa.png)

## Manual Conversion

<img src="images/manual_1.jpg" alt="Manual Conversion" width="500">
<img src="images/manual_2.jpg" alt="Manual Conversion" width="500">
