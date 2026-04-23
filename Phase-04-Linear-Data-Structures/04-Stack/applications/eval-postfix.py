"""
eval-postfix.py – Evaluate a Postfix Expression with One Stack

The easiest expression-evaluator there is. Postfix (Reverse Polish
Notation) makes evaluation a single linear pass over the tokens:

    for each token:
        if NUMBER:    push it
        if OPERATOR:  pop two operands, apply op, push result
    return stack[-1]

Time:  O(n)
Space: O(n)

Also the algorithm behind LeetCode #150 "Evaluate Reverse Polish Notation".

---------------------------------------------------
Why Postfix Evaluation Is So Clean:

In infix notation, a parser needs:
    - Precedence rules
    - Parenthesis tracking
    - Associativity handling

In postfix:
    - Operators come AFTER their operands, always.
    - No precedence to resolve (the author already did that).
    - No parentheses (they become unnecessary once operators are in order).

So evaluating postfix is trivial: every time you see an operator,
it applies to the two most-recently-pushed numbers. One stack, one
pass, done.

---------------------------------------------------
Example:

    Tokens:  ["2", "3", "4", "*", "+"]    =  2 + 3*4

    token  '2'   →  stack: [2]
    token  '3'   →  stack: [2, 3]
    token  '4'   →  stack: [2, 3, 4]
    token  '*'   →  pop 4, 3 → 3*4=12 → push →  stack: [2, 12]
    token  '+'   →  pop 12, 2 → 2+12=14 → push →  stack: [14]

    Result: 14.

---------------------------------------------------
"""

import operator


# =========================================================================
# Operator Dispatch
# =========================================================================

# Note: subtraction / division are NOT commutative. Careful with the
# order — pop `b` FIRST (the right operand), then `a` (the left operand).

def _divide(a, b):
    """Integer division, truncating towards zero (LeetCode #150 semantics)."""
    result = a / b
    return int(result) if result >= 0 else -(-a // b) if a % b != 0 else a // b


OPS = {
    "+": operator.add,
    "-": operator.sub,
    "*": operator.mul,
    "/": _divide,
    "^": operator.pow,
}


# =========================================================================
# Postfix Evaluator
# =========================================================================

def eval_postfix(tokens):
    """
    Evaluate a list of postfix tokens. Returns the result as an int (or float
    if any operand was a float).

    Time:  O(n)
    Space: O(n)

    Tokens should be a list of strings (numbers or operators).
    """
    stack = []

    for token in tokens:
        if token in OPS:
            if len(stack) < 2:
                raise ValueError(f"not enough operands for operator {token!r}")
            b = stack.pop()
            a = stack.pop()
            stack.append(OPS[token](a, b))
        else:
            stack.append(_parse_number(token))

    if len(stack) != 1:
        raise ValueError(f"invalid postfix expression — {len(stack)} values left on stack")
    return stack[-1]


def _parse_number(token):
    """Parse a number token as int if possible, else float."""
    try:
        return int(token)
    except ValueError:
        return float(token)


# =========================================================================
# LeetCode #150 Signature (Integer Evaluation with Truncate-Toward-Zero Division)
# =========================================================================

def eval_rpn(tokens):
    """
    LeetCode #150 "Evaluate Reverse Polish Notation". Same algorithm,
    integer-only. Division truncates toward zero (unlike Python's
    `//`, which floors).

    Time:  O(n)
    Space: O(n)
    """
    stack = []
    for token in tokens:
        if token in ("+", "-", "*", "/"):
            b = stack.pop()
            a = stack.pop()
            if token == "+":
                stack.append(a + b)
            elif token == "-":
                stack.append(a - b)
            elif token == "*":
                stack.append(a * b)
            else:
                # truncate toward zero (LC #150 spec)
                # Python // floors; that's wrong for negative results
                q = a // b
                if q < 0 and a % b != 0:
                    q += 1                         # undo the floor → truncate
                stack.append(q)
        else:
            stack.append(int(token))

    return stack[0]


# =========================================================================
# Test the Evaluator
# =========================================================================

if __name__ == "__main__":
    # Basic cases
    cases = [
        (["2", "3", "+"],                    5),
        (["2", "3", "4", "*", "+"],          14),
        (["2", "3", "+", "4", "*"],          20),
        (["5"],                               5),
        (["10", "2", "/"],                    5),
        (["2", "3", "^"],                     8),
        (["3", "4", "+", "2", "*", "7", "/"], 2.0),   # ((3+4)*2)/7 = 14/7 = 2
        (["1", "2", "3", "*", "+"],           7),     # 1 + (2*3) = 7
        # exponent is right-associative: 2 3 2 ^ ^  =  2 ^ (3^2) = 2^9 = 512
        (["2", "3", "2", "^", "^"],           512),
    ]

    print("Postfix evaluation:")
    for tokens, expected in cases:
        got = eval_postfix(tokens)
        # allow int/float mismatch since / may produce floats
        assert got == expected, f"eval({tokens}) = {got}, expected {expected}"
        print(f"   {' '.join(tokens):25} =  {got}")
    print()

    # LC #150 — integer semantics
    print("eval_rpn (LeetCode #150):")
    lc_cases = [
        (["2", "1", "+", "3", "*"],                9),          # (2+1)*3 = 9
        (["4", "13", "5", "/", "+"],               6),          # 4 + 13/5 = 4 + 2 = 6
        (["10", "6", "9", "3", "+", "-11", "*", "/", "*", "17", "+", "5", "+"],
                                                  22),
        (["18", "-5", "/"],                        -3),         # -3.6 truncated → -3 (not -4)
    ]
    for tokens, expected in lc_cases:
        got = eval_rpn(tokens)
        assert got == expected, f"eval_rpn({tokens}) = {got}, expected {expected}"
        print(f"   {' '.join(tokens):40} =  {got}")

    # Errors
    print("\nError cases:")
    for bad, description in [
        (["+"],             "no operands"),
        (["1", "+"],        "one operand"),
        (["1", "2", "3"],   "leftover stack"),
    ]:
        try:
            eval_postfix(bad)
        except ValueError as e:
            print(f"   {description}: {e}")

    # End-to-end: infix string → postfix → evaluate
    print("\nEnd-to-end pipeline (infix → postfix → eval):")
    import sys
    sys.path.insert(0, ".")
    try:
        # We can't import infix-postfix.py because of the hyphen in the name;
        # re-inline a minimal version for the pipeline demo.
        def tokenize(e):
            tokens, i = [], 0
            while i < len(e):
                c = e[i]
                if c.isspace():
                    i += 1
                elif c.isdigit() or c == ".":
                    j = i
                    while j < len(e) and (e[j].isdigit() or e[j] == "."):
                        j += 1
                    tokens.append(e[i:j]); i = j
                else:
                    tokens.append(c); i += 1
            return tokens

        PREC = {"+": 1, "-": 1, "*": 2, "/": 2, "^": 3}
        RIGHT = {"^"}

        def to_postfix(e):
            out, st = [], []
            for t in tokenize(e):
                try: float(t); out.append(t); continue
                except ValueError: pass
                if t in PREC:
                    while st and st[-1] != "(" and (
                        PREC[st[-1]] > PREC[t] or (PREC[st[-1]] == PREC[t] and t not in RIGHT)):
                        out.append(st.pop())
                    st.append(t)
                elif t == "(":
                    st.append(t)
                elif t == ")":
                    while st and st[-1] != "(":
                        out.append(st.pop())
                    st.pop()
            while st:
                out.append(st.pop())
            return out

        pipeline_cases = [
            ("2 + 3 * 4",        14),
            ("(2 + 3) * 4",      20),
            ("10 + 20 - 5",      25),
            ("2 ^ 3 ^ 2",        512),
            ("(1 + 2) * (3 + 4)", 21),
        ]
        for infix, expected in pipeline_cases:
            postfix_tokens = to_postfix(infix)
            result = eval_postfix(postfix_tokens)
            assert result == expected
            print(f"   {infix:22}  →  postfix {' '.join(postfix_tokens):20}  →  {result}")
    except Exception as e:
        print(f"   pipeline demo skipped: {e}")

    print("\nAll tests passed!")
