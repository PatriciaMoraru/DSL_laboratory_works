import itertools

def expand_pattern(pattern, max_reps=5, debug=False):
    def tokenize(pat):
        tokens = []
        i = 0
        while i < len(pat):
            if pat[i] == '(':
                j = i + 1
                depth = 1
                while j < len(pat) and depth:
                    if pat[j] == '(':
                        depth += 1
                    elif pat[j] == ')':
                        depth -= 1
                    j += 1
                tokens.append(pat[i:j])
                i = j
            elif pat[i] in '*+':
                tokens.append(pat[i])
                i += 1
            elif pat[i] == '^':
                j = i + 1
                while j < len(pat) and pat[j].isdigit():
                    j += 1
                tokens.append(pat[i:j])
                i = j
            elif pat[i].isdigit():
                num = ""
                while i < len(pat) and pat[i].isdigit():
                    num += pat[i]
                    i += 1
                for digit in num:
                    tokens.append(digit)
            else:
                tokens.append(pat[i])
                i += 1
        return tokens

    def interpret_token(token):
        if debug: print(f"Interpreting token: {token}")
        if token.startswith('('):
            return token[1:-1].split('|')
        elif token in ['*', '+']:
            return token
        elif token.startswith('^'):
            return token
        else:
            return [token]

    def generate_combinations(tokens):
        stack = [[]]
        i = 0
        while i < len(tokens):
            tok = tokens[i]
            interpreted = interpret_token(tok)
            next_token = tokens[i + 1] if i + 1 < len(tokens) else None
            op = None

            if next_token in ['*', '+'] or (next_token and next_token.startswith('^')):
                op = next_token
                i += 1

            new_stack = []
            for entry in stack:
                if isinstance(interpreted, list):
                    if op == '*':
                        new_stack.append(entry)
                        for r in range(1, max_reps + 1):
                            for combo in itertools.product(interpreted, repeat=r):
                                new_stack.append(entry + list(combo))
                    elif op == '+':
                        for r in range(1, max_reps + 1):
                            for combo in itertools.product(interpreted, repeat=r):
                                new_stack.append(entry + list(combo))
                    elif op and op.startswith('^'):
                        count = int(op[1:])
                        for combo in itertools.product(interpreted, repeat=count):
                            new_stack.append(entry + list(combo))
                    else:
                        for val in interpreted:
                            new_stack.append(entry + [val])
                else:
                    raise ValueError(f"Unexpected token: {interpreted}")
            stack = new_stack
            i += 1
        return [''.join(s) for s in stack]

    tokens = tokenize(pattern)
    if debug: print(f"Tokenized: {tokens}")
    return generate_combinations(tokens)

# Bonus: Processing steps
def show_processing_steps(pattern):
    print(f"\n--- Processing Steps for: {pattern} ---")
    step = 1
    i = 0
    while i < len(pattern):
        if pattern[i] == '(':
            j = i + 1
            depth = 1
            while j < len(pattern) and depth:
                if pattern[j] == '(':
                    depth += 1
                elif pattern[j] == ')':
                    depth -= 1
                j += 1
            group = pattern[i+1:j-1].split('|')
            print(f"[Step {step}] Found group: {pattern[i:j]} → will choose one of: {group}")
            i = j
        elif pattern[i] in '*+':
            if pattern[i] == '*':
                print(f"[Step {step}] Found repetition: '*' → applies to previous element 0–5 times")
            else:
                print(f"[Step {step}] Found repetition: '+' → applies to previous element 1–5 times")
            i += 1
        elif pattern[i] == '^':
            j = i + 1
            while j < len(pattern) and pattern[j].isdigit():
                j += 1
            count = pattern[i+1:j]
            print(f"[Step {step}] Found exact repetition: '^{count}' → applies to previous element exactly {count} times")
            i = j
        elif pattern[i].isdigit():
            print(f"[Step {step}] Found literal digit: '{pattern[i]}'")
            i += 1
        else:
            print(f"[Step {step}] Found character: '{pattern[i]}'")
            i += 1
        step += 1

def save_combinations_to_file(patterns, filename="combinations_output.txt"):
    with open(filename, "w") as f:
        for pat in patterns:
            f.write(f"Pattern: {pat}\n")
            results = expand_pattern(pat, debug=False)
            f.write(f"Generated {len(results)} combinations.\n")
            for item in results:
                f.write(f"{item}\n")
            f.write("\n" + "="*40 + "\n\n")
    print(f"\nAll combinations saved to '{filename}'")


def main():
    # Regex from Variant 4
    patterns = [
        "(S|T)(U|V)W*Y+24",
        "L(M|N)D^3P*Q(2|3)",
        "R*S(T|U|V)W(X|Y|Z)^2"
    ]

    print("=== Generating Combinations ===")
    for pat in patterns:
        print(f"\nPattern: {pat}")
        results = expand_pattern(pat, debug=False)
        print(f"Generated {len(results)} combinations. Sample:")
        print("\n".join(results[:5]), "...\n")

    print("=== Bonus: Processing Steps ===")
    for pat in patterns:
        show_processing_steps(pat)

    save_combinations_to_file(patterns)

if __name__ == "__main__":
    main()
