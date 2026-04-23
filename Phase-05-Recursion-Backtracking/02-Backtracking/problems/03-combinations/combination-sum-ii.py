"""
Problem: Combination Sum II (No Reuse, Duplicates in Input)

Difficulty: Medium (LeetCode #40)

---------------------------------------------------
Problem Statement:

Given `candidates` (which may contain duplicates) and a target,
find all UNIQUE combinations summing to `target` where each number
is used AT MOST ONCE.

    candidates = [10, 1, 2, 7, 6, 1, 5],  target = 8
    output = [[1, 1, 6], [1, 2, 5], [1, 7], [2, 6]]

Note: two `1`s in the input lets us use `[1, 1, 6]`, but we don't
output [1_a, 7] and [1_b, 7] as separate solutions — that's the
duplicate problem.

---------------------------------------------------
Compared to Combination Sum I:

    Combination Sum I:   candidates DISTINCT,    REUSE allowed  → `i` (not i+1)
    Combination Sum II:  candidates WITH DUPS,  NO reuse       → `i + 1`, + dup-skip

The duplicate-skip is the same `i > start and candidates[i] == candidates[i-1]`
idiom from Subsets II.

---------------------------------------------------
The Template:

    candidates = sorted(candidates)

    def backtrack(start, remaining):
        if remaining == 0:
            result.append(path[:])
            return

        for i in range(start, len(candidates)):
            if candidates[i] > remaining: break        # pruning

            if i > start and candidates[i] == candidates[i-1]:
                continue                              # dup-skip AT THIS LEVEL

            path.append(candidates[i])
            backtrack(i + 1, remaining - candidates[i])  # i + 1: no reuse
            path.pop()

---------------------------------------------------
"""


def combination_sum_ii(candidates, target):
    """
    Find all unique combinations summing to `target`, each element
    used at most once.

    Time:  O(2^N)
    Space: O(N) stack + O(output)
    """
    candidates = sorted(candidates)               # sort + enable dup-skip and pruning
    result = []
    path = []

    def backtrack(start, remaining):
        if remaining == 0:
            result.append(path[:])
            return

        for i in range(start, len(candidates)):
            c = candidates[i]

            if c > remaining:
                break                              # pruning: sorted, so rest is larger

            # DUPLICATE-SKIP: if this is not the first choice at this level
            # and it equals the previous, skip.
            if i > start and candidates[i] == candidates[i - 1]:
                continue

            path.append(c)
            backtrack(i + 1, remaining - c)        # i + 1 — NO REUSE
            path.pop()

    backtrack(0, target)
    return result


# =========================================================================
# Test
# =========================================================================

def _normalize(combos):
    return sorted([sorted(c) for c in combos])


if __name__ == "__main__":
    cases = [
        ([10, 1, 2, 7, 6, 1, 5],     8,
            [[1, 1, 6], [1, 2, 5], [1, 7], [2, 6]]),
        ([2, 5, 2, 1, 2],            5,
            [[1, 2, 2], [5]]),
        ([1, 1, 1, 1],               2,
            [[1, 1]]),
        ([1],                         1,   [[1]]),
        ([1],                         2,   []),
        ([2, 3, 6, 7],                7,   [[7]]),   # distinct → no reuse → just 7 alone
    ]

    for cands, target, expected in cases:
        got = combination_sum_ii(cands, target)
        assert _normalize(got) == _normalize(expected), (
            f"{cands} t={target}: got {got}, expected {expected}"
        )
        print(f"   combination_sum_ii({cands}, t={target}) = {_normalize(got)}")

    # Stress test — brute force via bitmask for small n
    import random
    random.seed(42)
    for _ in range(50):
        cands = [random.randint(1, 8) for _ in range(random.randint(0, 8))]
        target = random.randint(1, 25)

        # Brute: every subset (bitmask), keep those summing to target, dedupe
        brute = set()
        n = len(cands)
        for mask in range(1 << n):
            subset = tuple(sorted(cands[i] for i in range(n) if mask & (1 << i)))
            if sum(subset) == target:
                brute.add(subset)

        got = set(tuple(c) for c in _normalize(combination_sum_ii(cands, target)))
        assert got == brute, f"mismatch on {cands}, t={target}"

    print("\nStress test: 50 random inputs — matches brute force")

    print("\nAll tests passed!")

    # ---------------------------------------------------------------
    # Summary of the Three "Combination Sum" Variants:
    #
    #     Variant     Duplicates   Reuse  Technique
    #     ────────   ────────────  ─────  ─────────────────
    #     I          distinct      YES    start at i (not i+1)
    #     II         possible dup  NO     start at i+1, dup-skip
    #     III        distinct      NO     fixed count k, start at i+1
    #
    # Same template, three parameter sets. Once the template is in
    # memory, any variant is a small adjustment.
    # ---------------------------------------------------------------
