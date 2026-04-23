"""
Problem: Parentheses — Three Classic Variants

Difficulty: Easy → Medium

---------------------------------------------------
Covered in this file:

    1. is_valid_parentheses(s)          — match (), [], {} (LC #20)
    2. longest_valid_parentheses(s)     — longest valid () substring (LC #32)
    3. generate_parentheses(n)          — all valid ()()() strings of n pairs (LC #22)

The first two use a **stack**. The third uses **backtracking**. Together
they're the three shapes every parenthesis-related interview question
boils down to.

This is the first preview of stacks in this phase. We'll use them
extensively in **04-Stack/**.
"""


# =========================================================================
# 1. Valid Parentheses (LC #20) — The Canonical Stack Problem
# =========================================================================

def is_valid_parentheses(s):
    """
    True iff the brackets in `s` are properly matched and nested.

        "()"      → True
        "()[]{}"  → True
        "(]"      → False
        "([)]"    → False   (improper nesting)
        "{[]}"    → True

    Algorithm: walk the string, push opens, match closes against top.

        - OPEN bracket? → push on stack
        - CLOSE bracket? → stack top MUST be the matching open, else fail.

    At the end, stack must be empty.

    Time:  O(n)
    Space: O(n)  — stack up to size n/2 on pathological input "((((..."
    """
    pairs = {")": "(", "]": "[", "}": "{"}         # close → open
    stack = []

    for ch in s:
        if ch in "([{":
            stack.append(ch)
        elif ch in ")]}":
            if not stack or stack[-1] != pairs[ch]:
                return False
            stack.pop()
        # characters that aren't brackets are ignored; remove this `else`
        # if the problem says only bracket characters may appear.

    return not stack


# =========================================================================
# 2. Longest Valid Parentheses (LC #32)
# =========================================================================

def longest_valid_parentheses(s):
    """
    Return the LENGTH of the longest substring of `s` that is valid
    parentheses (using only '(' and ')').

        "(()"       → 2   (the inner "()")
        ")()())"    → 4   ("()()")
        ""          → 0
        "()(())"    → 6   (the whole string)

    Time:  O(n)
    Space: O(n)

    Technique: stack of INDICES. Initialize with a "base" of -1 so
    that the first valid pair has a correct length calculation.

        - '(' → push index.
        - ')' → pop. If stack is now empty, push the current index as
          the new base. Else, length of current valid run is
          i - stack[-1].
    """
    stack = [-1]                                    # base index
    best = 0

    for i, ch in enumerate(s):
        if ch == "(":
            stack.append(i)
        else:                                        # ch == ')'
            stack.pop()
            if not stack:
                stack.append(i)                      # new base
            else:
                best = max(best, i - stack[-1])

    return best


# =========================================================================
# 3. Generate Valid Parentheses (LC #22) — Backtracking
# =========================================================================

def generate_parentheses(n):
    """
    Return all distinct strings of n pairs of balanced parentheses.

        n=0 → [""]
        n=1 → ["()"]
        n=2 → ["(())", "()()"]
        n=3 → ["((()))", "(()())", "(())()", "()(())", "()()()"]

    Technique: BACKTRACKING. Maintain counts of open and close.
        - You may add '(' if we've used fewer than n opens so far.
        - You may add ')' if closes < opens (can't close what isn't open).

    Time:   O(4^n / sqrt(n)) — the Catalan-number count of valid strings.
    Space:  O(n) recursion stack + O(output size) for the result.
    """
    result = []
    path = []

    def backtrack(open_count, close_count):
        if len(path) == 2 * n:
            result.append("".join(path))
            return

        if open_count < n:
            path.append("(")
            backtrack(open_count + 1, close_count)
            path.pop()                               # un-choose

        if close_count < open_count:
            path.append(")")
            backtrack(open_count, close_count + 1)
            path.pop()

    backtrack(0, 0)
    return result


# =========================================================================
# Bonus: Minimum Add to Make Parentheses Valid (LC #921)
# =========================================================================

def min_add_to_make_valid(s):
    """
    Return the minimum number of '(' or ')' insertions needed to make
    `s` a valid parentheses string.

        "()"     → 0
        "())"    → 1
        "((("    → 3
        "()))(("  → 4

    Technique: one pass with two counters.
        - For each ')' that can't be matched (close > open so far),
          increment `need_open`.
        - At the end, leftover opens need matching closes: `need_close`.
        - Answer: need_open + need_close.

    Time:  O(n)
    Space: O(1)
    """
    open_needed = close_needed = 0

    for ch in s:
        if ch == "(":
            close_needed += 1                         # expect a future ')'
        else:                                         # ch == ')'
            if close_needed > 0:
                close_needed -= 1                     # match with a previous '('
            else:
                open_needed += 1                      # unmatched ')' needs a '(' before it

    return open_needed + close_needed


# =========================================================================
# Test the Functions
# =========================================================================

if __name__ == "__main__":
    # 1. is_valid_parentheses
    print("1. is_valid_parentheses (LC #20):")
    valid_cases = [
        ("()",           True),
        ("()[]{}",       True),
        ("(]",           False),
        ("([)]",         False),
        ("{[]}",         True),
        ("",             True),                       # empty is valid
        ("(",            False),
        (")",            False),
        ("((",           False),
        ("(((())))",     True),
        ("(()",          False),
        ("()()()",       True),
    ]
    for s, expected in valid_cases:
        got = is_valid_parentheses(s)
        assert got == expected, f"is_valid({s!r}): {got} != {expected}"
        print(f"   is_valid_parentheses({s!r:12}) = {got}")
    print()

    # 2. longest_valid_parentheses
    print("2. longest_valid_parentheses (LC #32):")
    long_cases = [
        ("(()",         2),
        (")()())",      4),
        ("",            0),
        ("()(())",      6),
        ("()()",        4),
        ("(()()",       4),
        ("((()",        2),
        ("()(()",       2),
        (")",           0),
        ("(",           0),
    ]
    for s, expected in long_cases:
        got = longest_valid_parentheses(s)
        assert got == expected, f"longest({s!r}): {got} != {expected}"
        print(f"   longest_valid_parentheses({s!r:15}) = {got}")
    print()

    # 3. generate_parentheses
    print("3. generate_parentheses (LC #22):")
    gen_cases = [
        (0, [""]),
        (1, ["()"]),
        (2, ["(())", "()()"]),
        (3, ["((()))", "(()())", "(())()", "()(())", "()()()"]),
    ]
    for n, expected in gen_cases:
        got = generate_parentheses(n)
        assert sorted(got) == sorted(expected), f"generate({n}): {got}"
        print(f"   generate_parentheses({n}) = {got}")

    # Catalan count check: C_n = #generate_parentheses(n)
    # C_0 = 1, C_1 = 1, C_2 = 2, C_3 = 5, C_4 = 14, C_5 = 42
    catalan = [1, 1, 2, 5, 14, 42]
    for n in range(len(catalan)):
        assert len(generate_parentheses(n)) == catalan[n]
    print(f"   Catalan check: #(n=0..5) = {[len(generate_parentheses(n)) for n in range(6)]}")
    print()

    # Bonus: min_add_to_make_valid
    print("4. min_add_to_make_valid (LC #921):")
    min_cases = [
        ("()",       0),
        ("())",      1),
        ("(((",      3),
        ("()))((",   4),
        ("",         0),
        ("(()",      1),
        ("))((",     4),
    ]
    for s, expected in min_cases:
        got = min_add_to_make_valid(s)
        assert got == expected, f"min_add({s!r}): {got} != {expected}"
        print(f"   min_add({s!r:10}) = {got}")

    # Stress test
    import random
    random.seed(42)

    # For is_valid vs a brute-force matcher
    for _ in range(300):
        n = random.randint(0, 20)
        s = "".join(random.choice("()[]{}") for _ in range(n))

        # brute-force: repeatedly strip innermost "()" / "[]" / "{}" until stable
        def brute_valid(s):
            while True:
                before = s
                s = s.replace("()", "").replace("[]", "").replace("{}", "")
                if s == before:
                    return s == ""

        got = is_valid_parentheses(s)
        expected = brute_valid(s)
        assert got == expected, f"stress: {s!r}: {got} != {expected}"

    print("\nStress test: 300 random bracket strings — stack matches brute-force")

    print("\nAll tests passed!")
