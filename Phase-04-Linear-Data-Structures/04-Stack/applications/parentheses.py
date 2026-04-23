"""
parentheses.py – Bracket Matching with a Stack

The archetypal stack problem. Covered in 02-String/problems/parentheses.py
from a STRING lens; here we give it the STACK lens, which is the same
algorithm but told from the data-structure side.

Three variants in this file:

    1. is_balanced(s)                — match (), [], {} (LC #20)
    2. longest_valid_parentheses(s)  — longest valid () substring (LC #32)
    3. minimum_removals_to_balance(s) — fewest chars to remove (LC #1249)

---------------------------------------------------
The Core Algorithm:

    stack = []
    pairs = {")": "(", "]": "[", "}": "{"}

    for ch in s:
        if ch in "([{":
            stack.push(ch)
        elif ch in ")]}":
            if not stack or stack.top() != pairs[ch]:
                return False
            stack.pop()

    return stack.is_empty()

Three-line idea:
    - OPEN brackets: push.
    - CLOSE brackets: MUST match the top, else fail.
    - At the end, the stack MUST be empty.

Time:  O(n)
Space: O(n) — the stack can grow to n/2 on "((((((..." inputs.

---------------------------------------------------
"""


# =========================================================================
# 1. Is Balanced (LC #20)
# =========================================================================

def is_balanced(s):
    """
    True iff `s` is a balanced bracket string over '()[]{}'.

    Time:  O(n)
    Space: O(n)
    """
    pairs = {")": "(", "]": "[", "}": "{"}
    stack = []

    for ch in s:
        if ch in "([{":
            stack.append(ch)
        elif ch in ")]}":
            if not stack or stack[-1] != pairs[ch]:
                return False
            stack.pop()
        # non-bracket characters are ignored; change this to `else: return False`
        # if the input is guaranteed to contain only brackets

    return not stack


# =========================================================================
# 2. Longest Valid Parentheses (LC #32)
# =========================================================================

def longest_valid_parentheses(s):
    """
    Return the LENGTH of the longest substring of `s` that is a valid
    '(' / ')' string.

    Technique: STACK OF INDICES. Initialize with a "base" of -1 so
    the first valid close has a correct length.

    Rules:
        - '(' → push its index.
        - ')' → pop. If the stack is now empty, push the current index
                      as the new "base". Else, the current valid run
                      has length (i - stack[-1]).

    Time:  O(n)
    Space: O(n)
    """
    stack = [-1]                                  # base index
    best = 0

    for i, ch in enumerate(s):
        if ch == "(":
            stack.append(i)
        else:                                      # ch == ')'
            stack.pop()
            if not stack:
                stack.append(i)                    # new base: this ')' has no matching '('
            else:
                best = max(best, i - stack[-1])

    return best


# =========================================================================
# 3. Minimum Removals to Make Parentheses Balanced (LC #1249)
# =========================================================================

def min_removals_to_balance(s):
    """
    Return the minimum number of '(' or ')' characters to remove so
    that the remaining string is balanced.

    (Non-bracket characters in `s` are left alone and don't count.)

    Time:  O(n)
    Space: O(n)

    Technique: scan left-to-right, pushing indices of unmatched '(' and
    ')'. Anything that REMAINS on the stack at the end is unmatched —
    return its count.
    """
    stack = []
    for i, ch in enumerate(s):
        if ch == "(":
            stack.append(i)
        elif ch == ")":
            if stack and s[stack[-1]] == "(":
                stack.pop()                        # matched
            else:
                stack.append(i)                    # unmatched ')'

    return len(stack)


# =========================================================================
# Bonus — Remove Outermost Parentheses (LC #1021)
# =========================================================================

def remove_outer_parentheses(s):
    """
    Decompose `s` into "primitive" balanced substrings (each one is
    the smallest balanced non-empty substring that stands alone), and
    remove each primitive's outermost parentheses.

        "(()())(())"   → "()()" + "()"   =  "()()()"
        "(()())(())(()(()))"   → "()()" + "()" + "()(())"   = "()()()()(())"

    Technique: maintain a counter of "depth" (open - close). When
    depth is 0, we're at a primitive's boundary.

    Time:  O(n)
    Space: O(n) for the output
    """
    result = []
    depth = 0

    for ch in s:
        if ch == "(":
            if depth > 0:                          # skip the outermost '('
                result.append(ch)
            depth += 1
        else:                                      # ch == ')'
            depth -= 1
            if depth > 0:                          # skip the outermost ')'
                result.append(ch)

    return "".join(result)


# =========================================================================
# Test the Functions
# =========================================================================

if __name__ == "__main__":
    # 1. is_balanced
    print("1. is_balanced (LC #20):")
    cases = [
        ("()",           True),
        ("()[]{}",       True),
        ("(]",           False),
        ("([)]",         False),
        ("{[]}",         True),
        ("",             True),
        ("(",            False),
        (")",            False),
        ("((",           False),
        ("(((())))",     True),
        ("(()",          False),
        ("()()()",       True),
    ]
    for s, expected in cases:
        got = is_balanced(s)
        assert got == expected
        print(f"   is_balanced({s!r:12}) = {got}")
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
    ]
    for s, expected in long_cases:
        got = longest_valid_parentheses(s)
        assert got == expected
        print(f"   longest_valid_parentheses({s!r:10}) = {got}")
    print()

    # 3. min_removals_to_balance
    print("3. min_removals_to_balance (LC #1249):")
    min_cases = [
        ("lee(t(c)o)de)",      1),                 # remove one ')'
        ("a)b(c)d",            1),
        ("))((",                4),
        ("(a(b(c)d)",           1),
        ("",                    0),
        ("()()",                0),
        ("((()))",              0),
    ]
    for s, expected in min_cases:
        got = min_removals_to_balance(s)
        assert got == expected
        print(f"   min_removals({s!r:20}) = {got}")
    print()

    # 4. remove_outer_parentheses
    print("4. remove_outer_parentheses (LC #1021):")
    outer_cases = [
        ("(()())(())",          "()()()"),
        ("(()())(())(()(()))",  "()()()()(())"),
        ("()()",                ""),
        ("()",                  ""),
        ("",                    ""),
    ]
    for s, expected in outer_cases:
        got = remove_outer_parentheses(s)
        assert got == expected
        print(f"   remove_outer({s!r:25}) = {got!r}")

    # Stress test — is_balanced against a "strip pairs until stable" reference
    import random
    random.seed(42)

    def brute_balanced(s):
        while True:
            before = s
            s = s.replace("()", "").replace("[]", "").replace("{}", "")
            if s == before:
                return s == ""

    for _ in range(300):
        length = random.randint(0, 20)
        s = "".join(random.choice("()[]{}") for _ in range(length))
        assert is_balanced(s) == brute_balanced(s)

    print("\nStress test: 300 random strings — is_balanced matches brute force")
    print("\nAll tests passed!")
