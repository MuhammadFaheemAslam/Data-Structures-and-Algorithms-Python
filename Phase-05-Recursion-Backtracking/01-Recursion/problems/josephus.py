"""
Problem: Josephus Problem

Difficulty: Medium (classic)

---------------------------------------------------
Problem Statement:

n people stand in a circle, numbered 0 to n-1. Starting from person
0, we count k people around the circle and eliminate the kth. Then
we continue counting k from the next person and eliminate again,
and so on, until only one person remains.

Return the 0-based position of the LAST SURVIVOR.

    Example: n = 5, k = 2
        Eliminate in order: 1, 3, 0, 4  → survivor = 2.
    Example: n = 7, k = 3
        Eliminate in order: 2, 5, 1, 6, 4, 0  → survivor = 3.

---------------------------------------------------
The Recurrence — One of the Cleanest in Recursion:

Let J(n, k) = the 0-based survivor's position in a circle of n.

    J(1, k) = 0            (only one person, so they survive)
    J(n, k) = (J(n-1, k) + k) mod n       for n > 1

Why? After the first elimination, we effectively have a SMALLER
version of the same problem with n-1 people, but the "starting
position" has shifted by k. Add k modulo n to translate positions
between the two problems.

This recurrence gives O(n) time, O(n) stack (or O(1) iterative).

---------------------------------------------------
Three Implementations:

    1. Simulation with a circular linked list   O(n · k), O(n) space
    2. Recursive formula                        O(n) time, O(n) stack
    3. Iterative formula                        O(n) time, O(1) space  ← ship this

Covered in Phase 04 / 03-Linked-List / 03-Circular-LL from the
data-structure side; here we explore the RECURSIVE MATH.

---------------------------------------------------
Historical Note:

Flavius Josephus (1st-century Roman historian) described being
trapped in a cave with 40 fellow rebels, who voted to die rather
than surrender. They agreed to kill each other in a circle,
counting to three. Josephus (a clever mathematician) figured out
WHICH POSITION WOULD SURVIVE and placed himself there — saving
himself and one other man.

This is the Josephus Problem with n = 40, k = 3. Survivor positions:
let's compute below.
"""


# =========================================================================
# 1. Simulation (Using a Python list as a circular array)
# =========================================================================

def josephus_simulate(n, k):
    """
    Directly simulate the process by maintaining a list of survivors.

    Time:  O(n · k)   — each elimination shifts a list of size n
    Space: O(n)

    Uses `list.pop(idx)` which is O(n); with a circular linked list
    we'd get O(n · k) but faster constants. See Phase 04 / 03 /
    03-Circular-LL / implementation.py for the circular-linked-list
    version.
    """
    if n <= 0 or k <= 0:
        raise ValueError("n and k must be positive")

    people = list(range(n))
    idx = 0
    while len(people) > 1:
        # advance k-1 steps from current `idx`, wrapping around
        idx = (idx + k - 1) % len(people)
        people.pop(idx)                            # O(n) — could be avoided with a linked list
    return people[0]


# =========================================================================
# 2. Recursive Formula — O(n) Time, O(n) Stack
# =========================================================================

def josephus_recursive(n, k):
    """
    Apply the recurrence:
        J(1, k) = 0
        J(n, k) = (J(n - 1, k) + k) mod n

    Time:  O(n)
    Space: O(n) stack

    Dramatically faster than simulation for large n — no list
    manipulations, just one arithmetic step per level.
    """
    if n <= 0 or k <= 0:
        raise ValueError("n and k must be positive")

    if n == 1:
        return 0
    return (josephus_recursive(n - 1, k) + k) % n


# =========================================================================
# 3. Iterative Formula — O(n) Time, O(1) Space (Production Choice)
# =========================================================================

def josephus_iterative(n, k):
    """
    Same recurrence, iterative.

    Time:  O(n)
    Space: O(1)

    Equivalent to josephus_recursive but without the stack frames.
    For n up to 10^6 or more, this is the right version.
    """
    if n <= 0 or k <= 0:
        raise ValueError("n and k must be positive")

    survivor = 0                                  # J(1, k) = 0
    for size in range(2, n + 1):
        survivor = (survivor + k) % size
    return survivor


# =========================================================================
# 4. 1-Indexed Variant (The Version in Most Textbooks)
# =========================================================================

def josephus_1_indexed(n, k):
    """
    Return the 1-indexed position of the survivor.

    Some sources use 1-indexing (as in the original Josephus legend
    with people numbered 1..n). Just add 1 to the 0-indexed result.
    """
    return josephus_iterative(n, k) + 1


# =========================================================================
# Test
# =========================================================================

if __name__ == "__main__":
    # Small-n correctness cross-check
    small_cases = [
        (1,  2,   0),
        (2,  2,   0),
        (5,  2,   2),              # classic result
        (7,  3,   3),
        (10, 2,   4),
        (10, 3,   3),
        (1,  1,   0),              # trivial
        (6,  5,   0),
    ]
    for n, k, expected in small_cases:
        a = josephus_simulate(n, k)
        b = josephus_recursive(n, k)
        c = josephus_iterative(n, k)
        assert a == b == c == expected, f"n={n}, k={k}: {a}/{b}/{c} != {expected}"
        print(f"   josephus(n={n}, k={k}) = {expected}")
    print()

    # The Josephus legend (n=40 according to one version)
    survivor = josephus_iterative(40, 3)
    print(f"Josephus (n=40, k=3):  survivor at 0-indexed position {survivor}")
    print(f"                        1-indexed position {survivor + 1}")
    print()

    # Large-n — iterative has no problems where the recursive hits the depth limit
    import sys
    sys.setrecursionlimit(10_000)

    big_n = 5_000
    a = josephus_iterative(big_n, 7)
    b = josephus_recursive(big_n, 7)
    assert a == b
    print(f"josephus(n={big_n}, k=7) = {a}  (iterative = recursive)")

    # n > recursion_limit → iterative still works; recursive would crash
    sys.setrecursionlimit(1000)
    really_big = 10_000
    result = josephus_iterative(really_big, 2)
    print(f"josephus(n={really_big}, k=2) = {result}  (iterative only)")

    # Stress test: simulation vs formula on smaller inputs
    import random
    random.seed(42)
    for _ in range(200):
        n = random.randint(1, 50)
        k = random.randint(1, 20)
        assert josephus_simulate(n, k) == josephus_iterative(n, k)

    print("\nStress test: 200 random (n, k) — simulation matches formula")

    print("\nAll tests passed!")

    # ---------------------------------------------------------------
    # The Three Implementations Summary:
    #
    #                            time          space         note
    #   simulation               O(n · k)      O(n)          intuitive; slow for large n
    #   recursive formula        O(n)          O(n) stack    clean; may hit recursion limit
    #   iterative formula        O(n)          O(1)          ← ship this
    #
    # Josephus is one of the best "recursion → iteration" conversions:
    # the recurrence is a single-line arithmetic step, so unrolling
    # it into a loop is trivial and strictly better.
    # ---------------------------------------------------------------
