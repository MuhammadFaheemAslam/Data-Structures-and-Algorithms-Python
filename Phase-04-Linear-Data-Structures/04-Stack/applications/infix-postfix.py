"""
infix-postfix.py – Infix → Postfix Conversion (Shunting-Yard Algorithm)

Dijkstra's classic algorithm for converting standard math notation
("2 + 3 * 4") into postfix / Reverse Polish Notation ("2 3 4 * +"),
which can then be evaluated without parentheses using just a stack.

---------------------------------------------------
Why Postfix?

Evaluating INFIX expressions requires operator-precedence rules,
parenthesis handling, and (sometimes) right-associativity. A program
has to know that in "2 + 3 * 4":

    - '*' binds tighter than '+'
    - So the answer is 2 + (3 * 4) = 14, not (2 + 3) * 4 = 20.

POSTFIX removes all ambiguity. The operator always comes AFTER its
two operands. There's exactly one way to parse, no precedence to
remember:

    "2 3 + 4 *"   →  (2+3) * 4  = 20
    "2 3 4 * +"   →  2 + (3*4)  = 14

Postfix evaluators are much simpler (see eval-postfix.py).

---------------------------------------------------
The Shunting-Yard Algorithm (Dijkstra, 1961):

Two data structures:
    - OUTPUT QUEUE (we'll use a list)
    - OPERATOR STACK

For each token in the INFIX expression:

    if token is a NUMBER:
        append to output
    if token is an OPERATOR op1:
        while operator stack is non-empty AND its top op2 has
              HIGHER OR EQUAL precedence than op1, AND op1 is
              left-associative (or HIGHER precedence for right-assoc):
            pop op2 from stack, append to output
        push op1 onto the stack
    if token is '(':
        push '('
    if token is ')':
        pop operators to output until '(' is on top
        discard the '('

After all tokens: pop remaining operators onto output.

---------------------------------------------------
Precedence and Associativity (Standard Math Rules):

    Operator | Precedence | Associativity
    +, -     | 1          | Left
    *, /     | 2          | Left
    ^ (pow)  | 3          | RIGHT — 2^3^2 means 2^(3^2) = 2^9

---------------------------------------------------
Example:

    Infix:    2 + 3 * 4
    Tokens:   ['2', '+', '3', '*', '4']

    Step-by-step:
        '2'   → output: [2]                        stack: []
        '+'   → output: [2]                        stack: [+]
        '3'   → output: [2, 3]                     stack: [+]
        '*'   → '*' has higher prec than '+', so don't pop.
                output: [2, 3]                     stack: [+, *]
        '4'   → output: [2, 3, 4]                  stack: [+, *]
        end   → pop all: output: [2, 3, 4, *, +]  stack: []

    Postfix: "2 3 4 * +"

---------------------------------------------------
"""


# =========================================================================
# Precedence Table
# =========================================================================

PRECEDENCE = {
    "+": 1, "-": 1,
    "*": 2, "/": 2,
    "^": 3,                                        # exponent, right-associative
}

RIGHT_ASSOC = {"^"}


# =========================================================================
# Tokenizer — A Simple One for Single-Digit Numbers + Operators
# =========================================================================

def tokenize(expression):
    """
    Split an infix string into tokens (numbers, operators, parentheses).

    Supports:
        - multi-digit integers (via isdigit runs)
        - decimals (e.g., "3.14")
        - whitespace (ignored)
        - operators: +, -, *, /, ^, (, )

    Does NOT support:
        - unary minus
        - functions like sin() / sqrt()
        - variable names

    Time: O(n)
    """
    tokens = []
    i = 0
    n = len(expression)

    while i < n:
        c = expression[i]

        if c.isspace():
            i += 1
            continue

        if c.isdigit() or c == ".":
            # consume a number
            j = i
            while j < n and (expression[j].isdigit() or expression[j] == "."):
                j += 1
            tokens.append(expression[i:j])
            i = j
            continue

        if c in "+-*/^()":
            tokens.append(c)
            i += 1
            continue

        raise ValueError(f"unexpected character: {c!r} at position {i}")

    return tokens


# =========================================================================
# Infix → Postfix (Shunting-Yard)
# =========================================================================

def infix_to_postfix(expression):
    """
    Convert an infix expression string to a list of postfix tokens.

    Time:  O(n)
    Space: O(n)
    """
    output = []
    stack = []

    for token in tokenize(expression):
        if _is_number(token):
            output.append(token)

        elif token in PRECEDENCE:                 # an operator
            while stack and stack[-1] != "(" and (
                PRECEDENCE[stack[-1]] > PRECEDENCE[token]
                or (PRECEDENCE[stack[-1]] == PRECEDENCE[token]
                    and token not in RIGHT_ASSOC)
            ):
                output.append(stack.pop())
            stack.append(token)

        elif token == "(":
            stack.append(token)

        elif token == ")":
            while stack and stack[-1] != "(":
                output.append(stack.pop())
            if not stack:
                raise ValueError("mismatched ')' in expression")
            stack.pop()                            # discard the matching '('

        else:
            raise ValueError(f"unexpected token: {token!r}")

    # pop any remaining operators
    while stack:
        top = stack.pop()
        if top == "(":
            raise ValueError("mismatched '(' in expression")
        output.append(top)

    return output


# =========================================================================
# Helpers
# =========================================================================

def _is_number(token):
    try:
        float(token)
        return True
    except ValueError:
        return False


# =========================================================================
# Test the Functions
# =========================================================================

if __name__ == "__main__":
    # Simple cases
    cases = [
        ("2 + 3",                   ["2", "3", "+"]),
        ("2 + 3 * 4",               ["2", "3", "4", "*", "+"]),
        ("(2 + 3) * 4",             ["2", "3", "+", "4", "*"]),
        ("2 * 3 + 4 * 5",           ["2", "3", "*", "4", "5", "*", "+"]),
        ("2 * (3 + 4) * 5",         ["2", "3", "4", "+", "*", "5", "*"]),
        ("2 ^ 3 ^ 2",               ["2", "3", "2", "^", "^"]),       # right-associative
        ("(1 + 2) * (3 - 4)",       ["1", "2", "+", "3", "4", "-", "*"]),
        ("10",                       ["10"]),
        ("3.14",                     ["3.14"]),
    ]

    print("Infix → Postfix conversions:")
    for infix, expected in cases:
        got = infix_to_postfix(infix)
        assert got == expected, (
            f"infix_to_postfix({infix!r}) = {got}, expected {expected}"
        )
        print(f"   {infix:25} →  {' '.join(got)}")

    # Errors
    print("\nError cases:")
    for bad in [")(", "(1 + 2"]:                   # mismatched parens
        try:
            infix_to_postfix(bad)
        except ValueError as e:
            print(f"   {bad!r} raised: {e}")

    # End-to-end: tokenize → infix_to_postfix → evaluate
    # (evaluation lives in eval-postfix.py; here we just convert)
    print("\nAll tests passed!")

    # ---------------------------------------------------------------
    # The Full Pipeline:
    #
    #   infix string  →  tokenize  →  infix_to_postfix  →  eval_postfix  →  number
    #
    # That's how a calculator works. Each step is a simple stack
    # operation; combined, they handle arbitrary nested expressions
    # with operator precedence, parentheses, and associativity.
    # ---------------------------------------------------------------
