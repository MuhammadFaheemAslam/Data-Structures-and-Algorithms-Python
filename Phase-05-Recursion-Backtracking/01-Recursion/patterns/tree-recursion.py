"""
tree-recursion.py – Tree Recursion (Multiple Recursive Calls Per Step)

A function is **tree-recursive** if it makes MORE THAN ONE recursive
call per invocation:

    def tree_recursive(n):
        if base_case(n):
            return base_value
        return combine(
            tree_recursive(reduce_a(n)),
            tree_recursive(reduce_b(n))
        )

The recursion tree BRANCHES at every level — hence the name.

---------------------------------------------------
Time Complexity: Usually Exponential

With a branching factor of `b` and depth `d`, the tree has roughly
**b^d** nodes. So binary tree recursion (b=2) on an input of size n
(d ≈ n) gives **O(2^n)** calls.

That's why naive Fibonacci is O(φ^n) ≈ O(1.618^n): each call spawns
two more, unbounded.

The cure is usually **memoization / DP** (Phase 02 / 01 / 04) — when
subproblems overlap, we cache each one's result. The exponential
tree collapses to a polynomial table.

---------------------------------------------------
When Tree Recursion Is the Right Tool:

    - Divide & conquer (merge sort, quicksort, closest-pair)
    - Enumeration of subsets, permutations, combinations
    - Backtracking search (N-Queens, Sudoku)
    - Tree and graph traversal
    - Expression evaluation on recursive structures (JSON, ASTs)

For problems that DON'T benefit from tree recursion (overlapping
subproblems, linear accumulation), prefer a single recursive call
or iteration.

This file shows five canonical tree-recursive problems — two that
are inefficient without memoization, and three that are correct
applications.
"""


# =========================================================================
# 1. Fibonacci (Naive Tree Recursion) — THE Pathological Example
# =========================================================================

def fib_naive(n):
    """
    Naive tree-recursive Fibonacci.

    Time:  O(φ^n) ≈ O(1.618^n)   — exponential!
    Space: O(n) stack depth

    fib(30) takes ~2.7 million calls. fib(40) takes ~300 million.
    DON'T USE THIS beyond n ≈ 30.

    Fix: memoize (see Phase 02 / 01 / 04-Dynamic-Programming).
    """
    if n < 2:
        return n
    return fib_naive(n - 1) + fib_naive(n - 2)


def fib_memoized(n, memo=None):
    """
    Memoized Fibonacci — the tree collapses to a chain via caching.

    Time:  O(n)
    Space: O(n) for the memo + O(n) stack
    """
    if memo is None:
        memo = {}
    if n in memo:
        return memo[n]
    if n < 2:
        return n
    memo[n] = fib_memoized(n - 1, memo) + fib_memoized(n - 2, memo)
    return memo[n]


# =========================================================================
# 2. Generate All Subsets — Correct Use of Tree Recursion
# =========================================================================

def all_subsets(arr):
    """
    Generate all 2^n subsets of `arr` via tree recursion.

    At each index, we make TWO recursive calls: one where arr[i] is
    INCLUDED in the subset, one where it's EXCLUDED.

    Time:  O(n · 2^n)   — 2^n subsets, each taking O(n) to construct
    Space: O(n) stack + O(n · 2^n) output

    This is a PROPER use of tree recursion: the output is inherently
    exponential, so the runtime has to be too. Memoization wouldn't help
    because there are no overlapping subproblems.

    Compared to the bitmask approach (Phase 02 / 02 / 11-Bit-Manipulation),
    tree recursion is often clearer and easier to extend with pruning.
    """
    result = []

    def backtrack(index, current):
        if index == len(arr):
            result.append(list(current))
            return

        # Branch 1: EXCLUDE arr[index]
        backtrack(index + 1, current)

        # Branch 2: INCLUDE arr[index]
        current.append(arr[index])
        backtrack(index + 1, current)
        current.pop()                             # backtrack

    backtrack(0, [])
    return result


# =========================================================================
# 3. Count Paths in a Grid (Top-Left to Bottom-Right, Down/Right Moves)
# =========================================================================

def count_paths(m, n):
    """
    Count the number of paths from (0, 0) to (m-1, n-1) in an m × n
    grid, moving only right or down.

    Time:  O(2^(m+n)) — exponential without memoization
    Space: O(m + n) stack

    Without memoization: tree recursion explores every possible path.

    With memoization (classic DP): O(m · n) time.
    """
    if m == 1 or n == 1:
        return 1
    return count_paths(m - 1, n) + count_paths(m, n - 1)


def count_paths_memoized(m, n, memo=None):
    """Memoized version — O(m · n) time."""
    if memo is None:
        memo = {}
    if (m, n) in memo:
        return memo[(m, n)]
    if m == 1 or n == 1:
        return 1
    memo[(m, n)] = count_paths_memoized(m - 1, n, memo) + count_paths_memoized(m, n - 1, memo)
    return memo[(m, n)]


# =========================================================================
# 4. Max Element in a List via Divide & Conquer (Tree Recursion Done Right)
# =========================================================================

def max_element(lst):
    """
    Find the maximum via binary-split divide & conquer.

    T(n) = 2T(n/2) + O(1)   →   O(n)

    Tree-recursive but NOT exponential — subproblems don't overlap
    (each half is disjoint), so we get the balanced-tree geometry:
    O(n) total work across O(log n) levels.

    A linear scan is simpler and faster in practice. This is
    educational — showing that tree recursion can be linear when the
    subproblems DIVIDE the input rather than overlapping.
    """
    if len(lst) == 1:
        return lst[0]
    mid = len(lst) // 2
    return max(max_element(lst[:mid]), max_element(lst[mid:]))


# =========================================================================
# 5. Tower of Hanoi — 2^n Moves, No Redundancy
# =========================================================================

def count_hanoi_moves(n):
    """
    Count the minimum number of moves to solve Tower of Hanoi with
    n disks.

    Recurrence: T(n) = 2·T(n-1) + 1     (move n-1, move big disk, move n-1 again)
    Closed form: 2^n - 1
    Time:  O(2^n)

    Tree recursion here is GENUINELY exponential — the number of
    MOVES is exponential by the problem's structure, not by
    redundancy. Memoization wouldn't help because there are no
    overlapping subproblems.

    Compare to fib_naive: both are O(2^n), but fib can be fixed to
    O(n) (with memoization) because its subproblems overlap.
    Hanoi cannot; the output itself is 2^n - 1 moves.
    """
    if n == 0:
        return 0
    return 2 * count_hanoi_moves(n - 1) + 1


# =========================================================================
# Test the Functions
# =========================================================================

if __name__ == "__main__":
    # 1. Fibonacci
    for n in [0, 1, 5, 10, 15]:
        assert fib_naive(n) == fib_memoized(n)
    print(f"Fibonacci matches for n ≤ 15")

    # Demonstrate the exponential cost
    import time
    t0 = time.time()
    fib_naive(30)
    t_naive = time.time() - t0

    t0 = time.time()
    fib_memoized(30)
    t_memo = time.time() - t0

    print(f"\nfib(30):")
    print(f"   naive:     {t_naive:.4f}s   (~2.7 million calls)")
    print(f"   memoized:  {t_memo:.6f}s   (31 unique calls)")
    print()

    # 2. Subsets
    for arr in [[], [1], [1, 2], [1, 2, 3]]:
        subsets = all_subsets(arr)
        assert len(subsets) == 2 ** len(arr)
        print(f"   all_subsets({arr}): {len(subsets)} subsets")
    print()

    # 3. Paths
    for m, n in [(1, 1), (2, 2), (3, 3), (3, 7)]:
        a = count_paths(m, n)
        b = count_paths_memoized(m, n)
        assert a == b
        print(f"   count_paths({m}, {n}) = {a}")
    print()

    # Timing: memoized wins big at m, n ≥ 10
    t0 = time.time()
    count_paths(10, 10)
    t_naive = time.time() - t0

    t0 = time.time()
    count_paths_memoized(10, 10)
    t_memo = time.time() - t0

    print(f"count_paths(10, 10):")
    print(f"   naive:     {t_naive:.4f}s")
    print(f"   memoized:  {t_memo:.6f}s")
    print()

    # 4. Max element (D&C)
    import random
    random.seed(42)
    for _ in range(50):
        lst = [random.randint(-100, 100) for _ in range(random.randint(1, 30))]
        assert max_element(lst) == max(lst)
    print("max_element via D&C matches max() on 50 random lists")
    print()

    # 5. Hanoi count — closed form validation
    for n in range(10):
        assert count_hanoi_moves(n) == 2 ** n - 1
    print(f"Tower of Hanoi: moves(n) = 2^n - 1 confirmed for n = 0..9")

    print("\nAll tests passed!")

    # ---------------------------------------------------------------
    # Two Types of "Exponential":
    #
    #   1. REDUNDANT exponential — overlapping subproblems recomputed.
    #      Fix with memoization. Example: fib_naive → fib_memoized,
    #      O(2^n) → O(n).
    #
    #   2. INTRINSIC exponential — the OUTPUT is exponential in size,
    #      so the runtime has to be too. Example: all_subsets.
    #      Memoization can't help.
    #
    # Always ask: "could memoization help here?" If subproblems
    # overlap, yes. If every recursive call has a unique argument,
    # no — the exponential is inherent.
    # ---------------------------------------------------------------
