# Report nr.4: Regular expressions

### Course: Formal Languages & Finite Automata
### Author: PATRICIA MORARU, FAF-233

----

# Theory

In this laboratory, we explored how regular expressions can be interpreted programmatically to generate valid combinations of characters. Regular expressions define patterns used to match or generate strings based on repetition, grouping, and alternatives. These expressions are often used in text processing, lexical analysis, and syntax validation.

Key symbols include:
- `(A|B)` – denotes a choice between symbols A or B.
- `*` – zero or more repetitions of the previous element.
- `+` – one or more repetitions.
- `^n` – exact number of repetitions.
- Literal symbols (e.g., `Q`, `2`, `4`) are taken as-is.

# Objectives

- Interpret simplified regular expressions dynamically.
- Generate all valid combinations based on these patterns.
- Respect repetition limits (max 5) for undefined repetition symbols (`*`, `+`).
- Describe the sequence of how each part of the expression is processed.

# Implementation Description

The goal of this implementation is to interpret and generate valid combinations of symbols that match a simplified version of regular expressions. These patterns include grouping, repetition operators, and literal characters. The approach is modular, meaning the process is split into three clear stages: tokenization, interpretation, and combination generation.

The main function expand_pattern() handles the full process of parsing and generating strings from a pattern.
1. **Tokenize** it: break the expression into characters, groups, and repetition operators.
2. **Interpret** each token: identify what it represents and how it should be expanded.
3. **Generate** all valid combinations respecting limits.

## 1. Tokenization

The first step in processing a regular expression is to tokenize it — that is, to break it down into meaningful parts (called tokens). This function scans the input string one character at a time and classifies symbols such as:

- **Groups like (A|B)** — These are kept as one token so they can be interpreted as sets of choices later.

- **Repetition operators** *, **+**, and **^n** — These are kept as separate tokens and will later be applied to the element before them.

- **Literal digits like "24"** — When these aren't part of a repetition (**^24**), they're treated as two separate character tokens: **'2'** and **'4'**.

- **Other characters** — Simple characters such as **W**, **Y**, **Q** are treated as individual tokens.

This step simplifies the logic that comes later by organizing the input into manageable chunks.
```python
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
```

## 2. Token Interpretation

This helper function **interprets the meaning** of each token from the tokenizer:

- If the token is a **group**, like `(x|y|z)`, it is split into a list of choices: `['x', 'y', 'z']`.

- If it's a **repetition operator** (`*`, `+`, or `^n`), it's returned as-is.

- If it's a **simple character**, it is wrapped in a list to unify the data structure used in the next steps.

This step ensures that we have a consistent and clear understanding of what each token is meant to do when we start generating combinations.

``` python
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
```


## 3. Combination Generation
This function is the core of the pattern expansion process. It maintains a list called `stack` that holds **partially built string combinations**. The logic proceeds token-by-token and builds up all valid combinations step by step.

Key logic:

- If a **repetition operator** (`*`, `+`, `^n`) is detected **after** a token, the function uses that to determine **how many times to repeat** the previous character or group.

- `itertools.product()` is used to generate **all permutations** of repeated elements.

- The function handles:
  - `*` as 0–5 repetitions
  - `+` as 1–5 repetitions
  - `^n` as **exactly n** repetitions

- If no repetition is specified, the token is just added once to each existing string in the `stack`.

By the end of this loop, `stack` contains all the valid generated strings.
```python
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
```

## 4. Bonus Task
This function addresses the **bonus requirement** from the lab:

> "Write a function that will show the sequence of processing the regular expression — what you do first, second, and so on."

Rather than simply generating output, this function essentially thinks aloud. It acts like a guided interpreter, taking the original regular expression pattern and walking through it step-by-step, explaining in natural language what each component means, in which order it is encountered, and how it will be processed.

In other words, this function doesn’t compute the final results — it tells a story of the parsing process, allowing the reader (or evaluator) to understand how the program logically makes sense of the expression.

This is especially useful for:

1. Debugging complex patterns. 
2. Learning purposes, so students can visualize the structure of a regular expression. 
3. Proving that the implementation is dynamic, not hardcoded. 
4. Documenting behavior when generating combinations.
``` python
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
```

## Results
The following examples demonstrate that the patterns are dynamically interpreted and expanded correctly:

**Pattern 1: (S|T)(U|V)W*Y+24**
```bash
Generated 120 combinations. Sample:
SUY24
SUYY24
SUYYY24
SUYYYY24
SUYYYYY24 ...
```

**Pattern: L(M|N)D^3P*Q(2|3)**
```bash
Generated 24 combinations. Sample:
LMDDDQ2
LMDDDQ3
LMDDDPQ2
LMDDDPQ3
LMDDDPPQ2 ...
```

**Pattern: R*S(T|U|V)W(X|Y|Z)^2**
```bash
Generated 162 combinations. Sample:
STWXX
STWXY
STWXZ
STWYX
STWYY ...
```
---
**Bonus: Processing Steps**

```bash
=== Bonus: Processing Steps ===

--- Processing Steps for: (S|T)(U|V)W*Y+24 ---
[Step 1] Found group: (S|T) → will choose one of: ['S', 'T']
[Step 2] Found group: (U|V) → will choose one of: ['U', 'V']
[Step 3] Found character: 'W'
[Step 4] Found repetition: '*' → applies to previous element 0–5 times
[Step 5] Found character: 'Y'
[Step 6] Found repetition: '+' → applies to previous element 1–5 times
[Step 7] Found literal digit: '2'
[Step 8] Found literal digit: '4'

--- Processing Steps for: L(M|N)D^3P*Q(2|3) ---
[Step 1] Found character: 'L'
[Step 2] Found group: (M|N) → will choose one of: ['M', 'N']
[Step 3] Found character: 'D'
[Step 4] Found exact repetition: '^3' → applies to previous element exactly 3 times
[Step 5] Found character: 'P'
[Step 6] Found repetition: '*' → applies to previous element 0–5 times
[Step 7] Found character: 'Q'
[Step 8] Found group: (2|3) → will choose one of: ['2', '3']

--- Processing Steps for: R*S(T|U|V)W(X|Y|Z)^2 ---
[Step 1] Found character: 'R'
[Step 2] Found repetition: '*' → applies to previous element 0–5 times
[Step 3] Found character: 'S'
[Step 4] Found group: (T|U|V) → will choose one of: ['T', 'U', 'V']
[Step 5] Found character: 'W'
[Step 6] Found group: (X|Y|Z) → will choose one of: ['X', 'Y', 'Z']
[Step 7] Found exact repetition: '^2' → applies to previous element exactly 2 times
```


# Conclusion
This laboratory assignment challenged us to not only understand regular expressions, but also to build a working engine that can parse, interpret, and expand them dynamically. The implementation avoids hardcoding and instead generalizes the parsing logic, making it reusable and extendable for various kinds of simplified regex patterns.

We successfully achieved the following:
1. Dynamically parsed expressions containing groups, character literals, and repetition operators. 
2. Respected repetition limits (* as **0–5**, **+** as **1–5**, **^n** as **exact**). 
3. Generated all valid combinations for each expression, validating correctness against provided examples. 
4. Wrote an enhanced bonus function that explains the logic in sequence, providing transparency and interpretability.

The most valuable part of this lab was learning how to simulate the behavior of a regex engine, breaking a complex abstract syntax into meaningful units, and then combining them to produce real output. This exercise not only deepened our understanding of regular languages and automata, but also reinforced the principles of clean parsing, modular code, and step-by-step logic construction.

In conclusion, this lab has provided a strong foundation in regex-based computation and helped bridge theoretical knowledge with practical implementation — fulfilling all required and bonus objectives with clarity and structure.

