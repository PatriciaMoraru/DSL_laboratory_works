import graphviz

def visualize_fa(fa, filename="finite_automaton"):
    """Generates a graphical visualization of the finite automaton using Graphviz."""
    dot = graphviz.Digraph(format='png')
    dot.attr(rankdir='LR', size='10')

    # Add states
    for state in fa.Q:
        if state in fa.F:
            dot.node(str(state), shape="doublecircle", color="green")  # Final states
        else:
            dot.node(str(state), shape="circle")

    # Add start state arrow
    dot.node("start", shape="none", width="0")
    dot.edge("start", str(fa.q0))

    # Add transitions
    for (state, symbol), next_states in fa.Delta.items():
        for next_state in next_states:
            dot.edge(str(state), str(next_state), label=symbol)

    dot.render(filename, view=True)
    print(f"Finite Automaton graph saved as {filename}.png")
