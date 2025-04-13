from cnf_form import Grammar

def main():
    non_terminals = {"S", "A", "B", "C", "D"}
    terminals = {"a", "b"}
    start_symbol = "S"
    productions = {
        "S": ["aB", "bA", "A"],
        "A": ["B", "Sa", "bBA", "b"],
        "B": ["b", "bS", "aD", ""],
        "D": ["AA"],
        "C": ["Ba"]
    }

    grammar = Grammar(non_terminals, terminals, start_symbol, productions)

    grammar.print_grammar("Initial Grammar")
    grammar.eliminate_epsilon()
    grammar.print_grammar("After Eliminating ε-productions")
    grammar.eliminate_unit_productions()
    grammar.print_grammar("After Eliminating Unit Productions")
    grammar.eliminate_inaccessible_symbols()
    grammar.print_grammar("After Eliminating Inaccessible Symbols")
    grammar.eliminate_non_productive_symbols()
    grammar.print_grammar("After Eliminating Non-Productive Symbols")
    grammar.to_cnf()
    grammar.print_grammar("Final Grammar in CNF")

if __name__ == "__main__":
    main()
