"""
template.py – Backtracking Reference Template

This file demonstrates the SHAPE of a backtracking algorithm in two
canonical forms:

    1. Generate all subsets     — no constraints, pure enumeration.
    2. Combination Sum          — constrained enumeration with pruning.

Every backtracking algorithm you'll ever write follows the same
three-step recipe:

    (1) CHOOSE       — make a decision, append to the running path.
    (2) EXPLORE      — recurse with the updated state.
    (3) UN-CHOOSE    — undo the decision before trying the next.

The pattern is five lines long; the art is in picking the right
candidate choices and the right pruning.

Run this file to see each template's output.
"""

# =========================================================================
# Generic Backtracking Skeleton
# =========================================================================
#
# def backtrack(path, state):
#     if is_complete(path, state):
#         result.append(path[:])           # SNAPSHOT — never share `path`
#         return
#
#     for choice in candidate_choices(state):
#         if feasible(choice, state):
#             path.append(choice)          # CHOOSE
#             apply(choice, state)         # (optional state update)
#             backtrack(path, state)       # EXPLORE
#             unapply(choice, state)       # (optional state revert)
#             path.pop()                   # UN-CHOOSE


# =========================================================================
# Template 1: All Subsets
# Search space: 2^n subsets of the input array.
# Constraints: NONE — this is the simplest backtracking possible.
# Complexity: O(n * 2^n) — 2^n subsets, each of length up to n to copy.
# =========================================================================

def subsets(nums):
    """
    Return every subset of `nums`, in a list-of-lists.

    The decision tree is binary: at each position, either INCLUDE
    the current element in the subset, or SKIP it. Every leaf of that
    tree is a distinct subset.

    Time Complexity:  O(n * 2^n)
    Space Complexity: O(n)  for the recursion stack
                      +  O(n * 2^n) for the output

    No pruning is possible here because every leaf is a valid subset —
    there are no invalid states to cut off.
    """
    result = []
    path = []

    def backtrack(start):
        # every prefix of the decision tree is itself a valid subset
        result.append(path[:])                  # snapshot!

        for i in range(start, len(nums)):
            path.append(nums[i])                # CHOOSE
            backtrack(i + 1)                    # EXPLORE — advance past i
            path.pop()                          # UN-CHOOSE

    backtrack(0)
    return result


# =========================================================================
# Template 2: Combination Sum
# Search space: all multisets of candidates summing to target.
# Constraints: sum must equal target; each number can be reused.
# Complexity: O(N^(T/M)) where N = len(candidates), T = target, M = min(candidates).
#             Pruning brings it WELL below this bound on realistic inputs.
# =========================================================================

def combination_sum(candidates, target):
    """
    Return every UNIQUE combination of `candidates` summing to `target`.
    Each number may be used an unlimited number of times.

    This is a perfect demonstration of PRUNING in action:

        - When the running sum exceeds `target` → prune (can't come back).
        - When the running sum hits `target` → record, prune (can't add more).
        - When no more candidates are available → prune (dead end).

    Sorting `candidates` lets us prune entire branches the moment a
    candidate exceeds the remaining target.

    Time Complexity:  worst case exponential; fast in practice
    Space Complexity: O(target / min(candidates)) recursion depth
    """
    result = []
    path = []
    candidates = sorted(candidates)             # enable "exceeded" pruning

    def backtrack(start, remaining):
        if remaining == 0:
            result.append(path[:])              # CHOOSE completed a valid path
            return

        for i in range(start, len(candidates)):
            c = candidates[i]
            if c > remaining:                   # PRUNE — sorted, rest are bigger
                break

            path.append(c)                      # CHOOSE
            backtrack(i, remaining - c)         # EXPLORE — reuse allowed (pass `i`, not i+1)
            path.pop()                          # UN-CHOOSE

    backtrack(0, target)
    return result


# =========================================================================
# Template 3: Grid Path Search
# Search space: all paths from a start cell to a target cell in a grid.
# Constraints: stay in bounds, don't revisit cells.
# Complexity: O(4^(R*C)) worst case without pruning.
# =========================================================================

def count_paths(grid, start, target):
    """
    Count all simple paths from `start` to `target` in a grid, where
    you can move up/down/left/right and cannot revisit cells.

    Demonstrates MUTATING state during exploration:
        - Temporarily mark the current cell as visited (e.g., set to None).
        - Recurse.
        - Restore the cell on the way back up.

    This is the pattern behind Word Search, Number of Islands
    (with connectivity tracking), and rat-in-a-maze problems.

    Time Complexity:  O(4^(R*C)) worst case; usually much less with
                      feasibility pruning on blocked cells
    Space Complexity: O(R * C) for the recursion stack in the worst case
    """
    R, C = len(grid), len(grid[0])
    count = 0

    def in_bounds(r, c):
        return 0 <= r < R and 0 <= c < C

    def backtrack(r, c):
        nonlocal count
        if (r, c) == target:
            count += 1
            return

        # mark visited by replacing with a sentinel we can restore
        saved = grid[r][c]
        grid[r][c] = None                       # CHOOSE (mark visited)

        for dr, dc in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            nr, nc = r + dr, c + dc
            if in_bounds(nr, nc) and grid[nr][nc] is not None:
                backtrack(nr, nc)               # EXPLORE

        grid[r][c] = saved                      # UN-CHOOSE (restore)

    sr, sc = start
    backtrack(sr, sc)
    return count


# =========================================================================
# Demonstration
# =========================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("Template 1 — All Subsets")
    print("=" * 60)
    for nums in [[1, 2, 3], [4, 5]]:
        sets = subsets(nums)
        print(f"   subsets({nums}) = {sets}")
        print(f"   count = {len(sets)}  (expected 2^{len(nums)} = {2 ** len(nums)})")
    print()

    print("=" * 60)
    print("Template 2 — Combination Sum")
    print("=" * 60)
    for cands, tgt in [([2, 3, 6, 7], 7), ([2, 3, 5], 8), ([1], 3)]:
        combos = combination_sum(cands, tgt)
        print(f"   combination_sum({cands}, {tgt}) = {combos}")
    print()

    print("=" * 60)
    print("Template 3 — Grid Path Count")
    print("=" * 60)
    grid = [
        [1, 1, 1],
        [1, 1, 1],
        [1, 1, 1],
    ]
    count = count_paths(grid, (0, 0), (2, 2))
    print(f"   3×3 grid, count paths from (0,0) to (2,2) = {count}")
