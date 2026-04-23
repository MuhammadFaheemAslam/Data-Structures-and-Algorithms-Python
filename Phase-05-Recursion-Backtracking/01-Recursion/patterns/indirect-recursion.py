"""
indirect-recursion.py – Indirect / Mutual Recursion

**Indirect recursion** (also called **mutual recursion**) happens when
function A calls function B, and B calls A — so A ends up calling
itself by going through B. Neither function is directly self-calling,
but together they form a recursive pair.

    def A(n):
        if base_case: return ...
        return B(n - 1)        # A calls B

    def B(n):
        if base_case: return ...
        return A(n - 1)        # B calls A — so A calls itself via B

---------------------------------------------------
Why Use Mutual Recursion?

Most problems solvable by mutual recursion can also be solved by a
single direct-recursive function with a `mode` parameter. Mutual
recursion is a stylistic choice, useful when:

    - Two processes toggle between distinct states (even/odd,
      sender/receiver, minimax's max/min layers).
    - A GRAMMAR naturally has mutually-defined non-terminals
      (e.g., `expression` calls `term` calls `expression`).
    - Finite-state machines with two or more states.

For linear toggling problems, direct recursion with a flag is usually
cleaner. This file demonstrates a few classic cases to make the
concept concrete.

---------------------------------------------------
Correctness: Simultaneous Induction

To prove a mutually-recursive pair correct:

    Base case:  both A and B are correct on the smallest input.
    Inductive step:
        Assume both A and B are correct on all smaller inputs.
        Then:
            A(n) is correct because it calls B on a smaller input.
            B(n) is correct because it calls A on a smaller input.

Same structure as direct-recursion induction, but on TWO functions
at once.
"""


# =========================================================================
# 1. is_even / is_odd — The Classic Textbook Example
# =========================================================================

def is_even(n):
    """
    True iff `n` is even, defined mutually-recursively with is_odd.

    Base: 0 is even.
    Recursive: n is even iff (n - 1) is odd.
    """
    if n < 0:
        n = -n
    if n == 0:
        return True
    return is_odd(n - 1)


def is_odd(n):
    """True iff `n` is odd."""
    if n < 0:
        n = -n
    if n == 0:
        return False
    return is_even(n - 1)


# Note: in Python, `n % 2 == 0` is vastly better. This is pedagogy,
# not production code.


# =========================================================================
# 2. Hofstadter's Female / Male Sequences
# =========================================================================

def hofstadter_F(n):
    """
    Hofstadter's "Female" sequence:
        F(0) = 1
        F(n) = n - M(F(n - 1))       for n > 0

    Mutually recursive with M.
    """
    if n == 0:
        return 1
    return n - hofstadter_M(hofstadter_F(n - 1))


def hofstadter_M(n):
    """
    Hofstadter's "Male" sequence:
        M(0) = 0
        M(n) = n - F(M(n - 1))       for n > 0

    Mutually recursive with F.
    """
    if n == 0:
        return 0
    return n - hofstadter_F(hofstadter_M(n - 1))


# Known starting values (OEIS A005378 / A005379):
HOFSTADTER_F_FIRST_20 = [1, 1, 2, 2, 3, 3, 4, 5, 5, 6, 6, 7, 8, 8, 9, 9, 10, 11, 11, 12]
HOFSTADTER_M_FIRST_20 = [0, 0, 1, 2, 2, 3, 4, 4, 5, 6, 6, 7, 7, 8, 9, 9, 10, 11, 11, 12]


# =========================================================================
# 3. Grammar-Based Expression Parser (Mutual Recursion by Design)
# =========================================================================
#
# Arithmetic expressions are defined mutually:
#
#     expression = term (('+' | '-') term)*
#     term       = factor (('*' | '/') factor)*
#     factor     = number | '(' expression ')'
#
# Note that `factor` can call `expression` (inside parens), and
# `expression` calls `term` which calls `factor`. Mutual recursion
# matches the grammar directly — you can hardly write a parser any
# other way.
#
# We implement a small calculator to demonstrate.

class Parser:
    """
    Recursive-descent parser. `parse_expression`, `parse_term`,
    `parse_factor` are mutually recursive, mirroring the grammar.
    """

    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def _peek(self):
        return self.tokens[self.pos] if self.pos < len(self.tokens) else None

    def _consume(self):
        tok = self.tokens[self.pos]
        self.pos += 1
        return tok

    def parse_expression(self):
        """expression = term (('+' | '-') term)*"""
        value = self.parse_term()
        while self._peek() in ("+", "-"):
            op = self._consume()
            right = self.parse_term()
            value = value + right if op == "+" else value - right
        return value

    def parse_term(self):
        """term = factor (('*' | '/') factor)*"""
        value = self.parse_factor()
        while self._peek() in ("*", "/"):
            op = self._consume()
            right = self.parse_factor()
            value = value * right if op == "*" else value / right
        return value

    def parse_factor(self):
        """factor = number | '(' expression ')'"""
        tok = self._consume()
        if tok == "(":
            value = self.parse_expression()       # mutual recursion
            assert self._consume() == ")", "missing ')'"
            return value
        return float(tok)


def evaluate(expression_string):
    """Parse and evaluate an arithmetic expression like '2 + 3 * (4 - 1)'."""
    tokens = _tokenize(expression_string)
    return Parser(tokens).parse_expression()


def _tokenize(s):
    """Split into tokens: numbers, operators, parens."""
    tokens = []
    i = 0
    while i < len(s):
        c = s[i]
        if c.isspace():
            i += 1
        elif c.isdigit() or c == ".":
            j = i
            while j < len(s) and (s[j].isdigit() or s[j] == "."):
                j += 1
            tokens.append(s[i:j])
            i = j
        elif c in "+-*/()":
            tokens.append(c)
            i += 1
        else:
            raise ValueError(f"bad character: {c!r}")
    return tokens


# =========================================================================
# Test the Functions
# =========================================================================

if __name__ == "__main__":
    # 1. is_even / is_odd
    print("1. is_even / is_odd (mutual recursion):")
    for n in [0, 1, 2, 10, 15, 100]:
        even = is_even(n)
        assert even == (n % 2 == 0)
        print(f"   is_even({n:4}) = {even}")
    print()

    # 2. Hofstadter F / M
    print("2. Hofstadter's F and M sequences:")
    for n in range(20):
        f = hofstadter_F(n)
        m = hofstadter_M(n)
        assert f == HOFSTADTER_F_FIRST_20[n]
        assert m == HOFSTADTER_M_FIRST_20[n]
        print(f"   F({n:2}) = {f:2},  M({n:2}) = {m:2}")
    print()

    # 3. Parser
    print("3. Recursive-descent parser (mutually recursive grammar):")
    cases = [
        ("2 + 3",                5),
        ("2 + 3 * 4",            14),
        ("(2 + 3) * 4",          20),
        ("(1 + 2) * (3 + 4)",    21),
        ("10 / 2",               5),
        ("3",                    3),
        ("((1 + 2) + (3 + 4))",  10),
    ]
    for expr, expected in cases:
        got = evaluate(expr)
        assert got == expected, f"{expr}: got {got}, expected {expected}"
        print(f"   evaluate({expr!r:25}) = {got}")

    print("\nAll tests passed!")

    # ---------------------------------------------------------------
    # When to Reach for Mutual Recursion:
    #
    #   - You're implementing a grammar (recursive-descent parsers).
    #   - You're modeling a 2-state machine (alternating strategies).
    #   - Minimax-style games (max level calls min, min calls max).
    #
    # When NOT to:
    #
    #   - "Just two states" → direct recursion with a flag parameter is cleaner.
    #   - "Toggling" → use modular arithmetic (n % 2) or a loop.
    #
    # The grammar case (example 3) is the only one where mutual recursion
    # is CLEARER than the alternatives. Learn it there; the rest is pedagogy.
    # ---------------------------------------------------------------
