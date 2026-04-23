"""
Problem: Combination Sum III (Fixed Count, Digits 1-9)

Difficulty: Medium (LeetCode #216)

---------------------------------------------------
Problem Statement:

Find all combinations of `k` different numbers from 1 to 9 that sum
to `n`. Each number may be used AT MOST ONCE.

    k = 3, n = 7   →  [[1, 2, 4]]
    k = 3, n = 9   →  [[1, 2, 6], [1, 3, 5], [2, 3, 4]]
    k = 4, n = 1   →  []                 (impossible — smallest 4 digits sum to 10)

---------------------------------------------------
Compared to the Other Combination-Sum Variants:

    Variant     Input universe       Count   Reuse  Sum target
    ──────      ──────────────       ─────   ─────  ──────────
    I           `candidates` distinct  any    YES    target
    II          `candidates` with dup  any    NO     target
    III         1..9 (fixed)           EXACTLY k NO  n

The "fixed count k" is the new twist. The size of the answer is
bounded (at most C(9, k) combinations), so this is often faster
than I or II in practice.

---------------------------------------------------
The Template:

    def backtrack(start, remaining):
        if len(path) == k and remaining == 0:
            result.append(path[:])
            return

        if len(path) == k:          ← PRUNE: can't add more if we've hit k
            return
        if remaining < 0:           ← PRUNE: overshot the sum
            return

        for d in range(start, 10):
            path.append(d)
            backtrack(d + 1, remaining - d)   # d+1 — NO REUSE
            path.pop()

Two extra pruning opportunities:
    - If remaining < next_smallest_possible_sum (sum of k - len(path)
      smallest digits ≥ start), bail.
    - If remaining > next_largest_possible_sum, also bail.
"""


def combination_sum_iii(k, n):
    """
    Find all combinations of exactly `k` distinct digits from 1..9
    that sum to `n`.

    Time:  O(C(9, k))   — at most 9-choose-k combinations
    Space: O(k) stack
    """
    # Basic sanity: the smallest sum of k distinct digits from 1..9
    # is 1+2+...+k = k*(k+1)/2. The largest is 9+8+...+(10-k).
    min_sum = k * (k + 1) // 2
    max_sum = k * (19 - k) // 2
    if n < min_sum or n > max_sum:
        return []

    result = []
    path = []

    def backtrack(start, remaining):
        if len(path) == k:
            if remaining == 0:
                result.append(path[:])
            return

        # Need `k - len(path)` more digits from [start..9] summing to `remaining`
        needed = k - len(path)

        # PRUNE: if the smallest `needed` digits ≥ start can't sum to remaining, fail
        # smallest = start + (start+1) + ... + (start + needed - 1)
        smallest_sum = sum(range(start, start + needed))
        if smallest_sum > remaining:
            return

        # PRUNE: if the largest `needed` digits ≤ 9 can't reach remaining, fail
        largest_sum = sum(range(10 - needed, 10))
        if largest_sum < remaining:
            return

        for d in range(start, 10):
            if d > remaining:
                break                              # sorted — no need to try bigger

            path.append(d)
            backtrack(d + 1, remaining - d)
            path.pop()

    backtrack(1, n)
    return result


# =========================================================================
# Test
# =========================================================================

def _normalize(combos):
    return sorted([sorted(c) for c in combos])


if __name__ == "__main__":
    cases = [
        (3, 7,   [[1, 2, 4]]),
        (3, 9,   [[1, 2, 6], [1, 3, 5], [2, 3, 4]]),
        (4, 1,   []),                              # too small
        (3, 15,  [[1, 5, 9], [1, 6, 8], [2, 4, 9], [2, 5, 8], [2, 6, 7], [3, 4, 8], [3, 5, 7], [4, 5, 6]]),
        (9, 45,  [[1, 2, 3, 4, 5, 6, 7, 8, 9]]),   # the one way to sum to the max using all 9
        (1, 5,   [[5]]),
        (1, 10,  []),                              # 10 not a digit
        (2, 18,  []),                              # max 2-digit-distinct sum is 17 (8+9)
        (2, 17,  [[8, 9]]),
    ]

    for k, n, expected in cases:
        got = combination_sum_iii(k, n)
        assert _normalize(got) == _normalize(expected), f"k={k}, n={n}: {got}"
        print(f"   combination_sum_iii(k={k}, n={n}) = {_normalize(got)}")

    # Stress test — compare against itertools.combinations brute force
    from itertools import combinations

    for k in range(1, 10):
        for n in range(1, 50):
            brute = [list(c) for c in combinations(range(1, 10), k) if sum(c) == n]
            got = combination_sum_iii(k, n)
            assert _normalize(brute) == _normalize(got), f"mismatch k={k}, n={n}"

    print("\nStress test: all (k, n) for k∈[1,9], n∈[1,49] — matches brute force")

    print("\nAll tests passed!")

    # ---------------------------------------------------------------
    # The Three Combination-Sum Problems — Final Summary:
    #
    #     I   (LC #39):    distinct candidates, REUSE allowed
    #                      template: for i, recurse with `i` (not i+1)
    #
    #     II  (LC #40):    candidates with duplicates, NO reuse
    #                      template: for i, recurse with i+1, dup-skip
    #
    #     III (LC #216):   digits 1..9, fixed count `k`, NO reuse
    #                      template: for d, recurse with d+1, track len(path)
    #
    # All three use the same universal template with different:
    #   - Candidate pool
    #   - Reuse / no-reuse (→ start=i vs i+1)
    #   - Termination condition (sum target, fixed count, both)
    #   - Dup-handling strategy (none, dup-skip, inherent from 1..9)
    #
    # Master the template; the three variants become mechanical
    # parameter substitutions.
    # ---------------------------------------------------------------
