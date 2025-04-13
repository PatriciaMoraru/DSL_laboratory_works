from itertools import product
class Grammar:
    def __init__(self, non_terminals, terminals, start_symbol, productions):
        self.non_terminals = non_terminals
        self.terminals = terminals
        self.start_symbol = start_symbol
        self.productions = productions

    def print_grammar(self, title):
        print(f"\n--- {title} ---\n")

        if self.start_symbol in self.productions:
            rules = self.productions[self.start_symbol]
            if rules:
                right = " | ".join(rules)
                print(f"{self.start_symbol} → {right}")

        for nt in sorted(self.productions):
            if nt == self.start_symbol:
                continue
            rules = self.productions[nt]
            if rules:
                right = " | ".join(rules)
                print(f"{nt} → {right}")
        print()

    def eliminate_epsilon(self):
        nullable = set()
        for nt, rules in self.productions.items():
            for rule in rules:
                if rule == "":
                    nullable.add(nt)

        updated = {}
        for nt in self.productions:
            new_rules = set()
            for rule in self.productions[nt]:
                if rule == "":
                    continue
                new_rules.add(rule)
                combos = self._generate_nullable_variations(rule, nullable)
                for alt in combos:
                    if alt != rule and alt != "":
                        new_rules.add(alt)
            updated[nt] = list(new_rules)

        self.productions = updated

    def eliminate_unit_productions(self):
        updated = {nt: set() for nt in self.non_terminals}
        for nt in self.productions:
            updated[nt].update(self.productions[nt])

        for nt in self.non_terminals:
            unit_stack = [nt]
            visited = set()
            while unit_stack:
                current = unit_stack.pop()
                if current in visited:
                    continue
                visited.add(current)
                for rule in self.productions.get(current, []):
                    if rule in self.non_terminals:
                        unit_stack.append(rule)
                    else:
                        updated[nt].add(rule)

        self.productions = {nt: list(rules - self.non_terminals) for nt, rules in updated.items()}

    def eliminate_inaccessible_symbols(self):
        reachable = set()
        to_visit = [self.start_symbol]

        while to_visit:
            current = to_visit.pop()
            if current in reachable:
                continue
            reachable.add(current)
            for rule in self.productions.get(current, []):
                for symbol in rule:
                    if symbol in self.non_terminals and symbol not in reachable:
                        to_visit.append(symbol)

        self.non_terminals = self.non_terminals.intersection(reachable)
        self.productions = {nt: rules for nt, rules in self.productions.items() if nt in reachable}

    def eliminate_non_productive_symbols(self):
        productive = set()

        changed = True
        while changed:
            changed = False
            for nt in self.non_terminals:
                for rule in self.productions.get(nt, []):
                    if all(ch in self.terminals or ch in productive for ch in rule):
                        if nt not in productive:
                            productive.add(nt)
                            changed = True

        self.non_terminals = self.non_terminals.intersection(productive)
        self.productions = {
            nt: [rule for rule in rules if all(ch in self.terminals or ch in productive for ch in rule)]
            for nt, rules in self.productions.items()
            if nt in productive
        }

    def to_cnf(self):
        new_productions = {}
        terminal_map = {}
        counter = 1

        for nt in self.productions:
            new_rules = []
            for rule in self.productions[nt]:
                if len(rule) > 1:
                    symbols = []
                    for ch in rule:
                        if ch in self.terminals:
                            if ch not in terminal_map:
                                new_nt = f"X_{counter}"
                                counter += 1
                                terminal_map[ch] = new_nt
                            symbols.append(terminal_map[ch])
                        else:
                            symbols.append(ch)
                    new_rules.append(symbols)
                else:
                    new_rules.append([rule])
            new_productions[nt] = new_rules

        for t, x in terminal_map.items():
            new_productions[x] = [[t]]
            self.non_terminals.add(x)

        updated = {}
        new_counter = counter
        binary_map = {}

        for nt in new_productions:
            updated[nt] = []
            for rule in new_productions[nt]:
                if len(rule) <= 2:
                    updated[nt].append("".join(rule))
                else:
                    symbols = rule
                    left = symbols[0]
                    for i in range(1, len(symbols) - 1):
                        pair = symbols[i] + symbols[i + 1]
                        if pair in binary_map:
                            new_nt = binary_map[pair]
                        else:
                            new_nt = f"X_{new_counter}"
                            new_counter += 1
                            binary_map[pair] = new_nt
                            updated[new_nt] = [pair]
                        symbols[i + 1] = new_nt
                    updated[nt].append(left + symbols[-1])

        self.productions = updated

    def _generate_nullable_variations(self, rule, nullable):
        indices = [i for i, ch in enumerate(rule) if ch in nullable]
        variations = set()

        for mask in product([0, 1], repeat=len(indices)):
            temp = list(rule)
            for i, keep in zip(indices, mask):
                if not keep:
                    temp[i] = ""
            alt = "".join(temp)
            variations.add(alt)

        return variations

