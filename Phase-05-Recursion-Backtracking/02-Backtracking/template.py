"""
template.py – The Universal Backtracking Skeleton

Every backtracking problem is this four-line loop with different
definitions of choices, feasibility, and solution. Memorize the
pattern once; reuse it across subsets, permutations, combinations,
constraint-satisfaction, grid paths, and graph colouring.

---------------------------------------------------
The Skeleton:

    def backtrack(state, path):
        if is_solution(state):
            record(path)
            return

        for choice in candidates(state):
            if not feasible(choice, state):
                continue                        # PRUNE

            apply(choice, state, path)           # CHOOSE
            backtrack(state, path)               # EXPLORE
            revert(choice, state, path)          # UN-CHOOSE

Five blanks to fill for ANY backtracking problem:

    1. is_solution — when is `state` a complete answer?
    2. candidates  — what choices are available from here?
    3. feasible    — is this choice valid right now?
    4. apply/revert — how do we record / undo a choice?
    5. record      — what to emit/count on a solution

---------------------------------------------------
Demo: Generate All Subsets of [1, 2, 3] via the Template

This file uses the classic "enumerate all subsets" problem as the
running example, because it's the simplest case where every blank
is non-trivial:

    state       = index of the next element to decide on
    path        = the subset being built
    is_solution = state == len(nums)
    candidates  = ["exclude", "include"]
    feasible    = always True (no constraints)
    apply       = if "include", path.append(nums[state])
    revert      = if "include", path.pop()
    record      = results.append(path[:])

Run the file to see the full generation in action.
"""


# =========================================================================
# The Universal Skeleton, Applied to Subsets
# =========================================================================

def subsets(nums):
    """
    Generate all 2^n subsets of `nums` via the canonical backtracking
    template.

    Time:  O(n · 2^n)
    Space: O(n) stack + O(n · 2^n) output
    """
    results = []
    path = []

    def backtrack(index):
        # 1. IS SOLUTION? (we've decided about every element)
        if index == len(nums):
            results.append(path[:])                # RECORD (snapshot!)
            return

        # 2. CANDIDATES: two options at each step — exclude or include
        # We encode this by making two recursive calls.

        # Option A: EXCLUDE nums[index]
        #   (no apply/revert needed; path is unchanged)
        backtrack(index + 1)

        # Option B: INCLUDE nums[index]
        path.append(nums[index])                   # CHOOSE
        backtrack(index + 1)                       # EXPLORE
        path.pop()                                 # UN-CHOOSE

    backtrack(0)
    return results


# =========================================================================
# Alternative Phrasing — Explicit "For Each Choice" Loop
# =========================================================================

def subsets_explicit_loop(nums):
    """
    Same problem, but with an explicit `for choice in candidates` loop.

    Makes the universal template more visible — every backtracking
    problem looks like this.
    """
    results = []
    path = []

    def backtrack(start):
        # Record the current subset as a solution — EVERY prefix is a
        # valid subset, so we record at every node.
        results.append(path[:])

        # CANDIDATES: choose any index from `start` onward to add to the subset
        for i in range(start, len(nums)):
            # FEASIBLE: always, for subsets (no constraints).

            # CHOOSE
            path.append(nums[i])

            # EXPLORE — subsequent choices must come AFTER `i` to avoid
            # duplicates (we're enumerating subsets, not permutations)
            backtrack(i + 1)

            # UN-CHOOSE
            path.pop()

    backtrack(0)
    return results


# =========================================================================
# Decision-Tree Demo (for Teaching)
# =========================================================================

def subsets_with_trace(nums):
    """
    Same algorithm, but prints the decision tree as it's explored.
    Great for understanding exactly what "choose → explore → un-choose"
    looks like at runtime.
    """
    results = []
    path = []
    depth = 0

    def indent():
        return "  " * depth

    def backtrack(index):
        nonlocal depth
        if index == len(nums):
            print(f"{indent()}✓ solution: {path}")
            results.append(path[:])
            return

        item = nums[index]

        # Exclude
        print(f"{indent()}[index={index}] exclude {item}")
        depth += 1
        backtrack(index + 1)
        depth -= 1

        # Include
        print(f"{indent()}[index={index}] include {item}")
        path.append(item)
        depth += 1
        backtrack(index + 1)
        depth -= 1
        path.pop()

    backtrack(0)
    return results


# =========================================================================
# Test the Template
# =========================================================================

if __name__ == "__main__":
    # The two subset implementations should produce the same subsets
    # (possibly in different orders)
    nums = [1, 2, 3]

    a = subsets(nums)
    b = subsets_explicit_loop(nums)

    norm = lambda x: sorted(sorted(s) for s in x)
    assert norm(a) == norm(b)
    print(f"subsets({nums}):")
    for s in a:
        print(f"   {s}")
    print(f"\ncount: {len(a)}  (expected 2^{len(nums)} = {2 ** len(nums)})")
    assert len(a) == 2 ** len(nums)
    print()

    # Larger n
    for n in [0, 1, 4, 6]:
        nums = list(range(n))
        out = subsets(nums)
        assert len(out) == 2 ** n, f"subsets({nums}): got {len(out)}, expected {2 ** n}"
        print(f"   subsets(len={n}): {len(out)} subsets")
    print()

    # Decision tree visualization — for a small input
    print("=" * 60)
    print("Decision-tree trace for subsets([A, B]):")
    print("=" * 60)
    subsets_with_trace(["A", "B"])

    print("\nAll tests passed!")

    # ---------------------------------------------------------------
    # Recognizing the Template in the Wild:
    #
    #   Once you've seen it here, you'll see it EVERYWHERE:
    #
    #     - Subsets / permutations / combinations  (problems/01, 02, 03)
    #     - N-Queens, Sudoku                        (problems/04, 05)
    #     - Word Search, maze solving               (problems/06)
    #     - Hamiltonian path, graph colouring        (problems/07)
    #
    #   The template never changes. What changes is:
    #
    #     - What `state` represents (index, grid, current node).
    #     - What counts as a solution (complete subset, legal placement).
    #     - What the candidates are (next items, adjacent cells, neighbours).
    #     - What feasibility means (bounds, uniqueness, no attacks).
    #
    #   Fill those four blanks; the rest is the same four lines.
    # ---------------------------------------------------------------
