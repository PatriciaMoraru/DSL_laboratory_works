import graphviz

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

