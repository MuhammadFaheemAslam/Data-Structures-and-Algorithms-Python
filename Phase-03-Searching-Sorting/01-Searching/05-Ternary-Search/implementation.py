"""
implementation.py – Ternary Search

Ternary search has two distinct uses that are often confused:

    1. **On sorted arrays** — divide into THREE parts instead of two.
       Runs in O(log₃ n) iterations, each making TWO comparisons.
       Total comparisons: 2 · log₃(n) ≈ 1.26 · log₂(n). Slightly
       WORSE than binary search. Historically interesting but not
       useful in practice.

    2. **On UNIMODAL functions** — find the maximum (or minimum) of
       a function that strictly increases then strictly decreases
       (or vice versa). O(log n) iterations. This IS the useful
       version — it's the standard tool for optimizing continuous
       unimodal functions and for problems like:

         - Find the peak of a ski slope.
         - Find the day a stock price peaks.
         - Optimize a physical parameter with a single sweet spot.

This file implements both. The unimodal-function version is the one
worth knowing by heart.

---------------------------------------------------
The Unimodal Version (The Useful One):

A function f is UNIMODAL on [lo, hi] if there is exactly ONE maximum
(or minimum) inside — everything to its left is strictly increasing,
everything to its right is strictly decreasing (for a max peak).

    f:    ... < ... < ... < PEAK > ... > ... > ...

To find the peak:

    mid1 = lo + (hi - lo) / 3
    mid2 = hi - (hi - lo) / 3

    if f(mid1) < f(mid2):
        the peak is in (mid1, hi]        → lo = mid1 + 1
    else:
        the peak is in [lo, mid2)        → hi = mid2 - 1

Why? If f(mid1) < f(mid2), the peak cannot be in [lo, mid1] — f is
increasing at mid1, so it's still climbing. It must be in (mid1, hi].

Each iteration shrinks the range by a factor of 2/3. After k iterations
the range has length n · (2/3)^k, so O(log n) — base 3/2 — iterations
suffice.

---------------------------------------------------
Use Cases for Ternary Search:

- **Convex / concave function optimization** without derivatives
  (continuous or discrete).
- **Game theory:** finding the optimal value in a unimodal payoff
  function.
- **Geometric optimization:** closest point in time / distance with
  a single turning point.
- **LeetCode-style problems:** Find the Peak Element (LC #162 — but
  binary search works too), Sqrt (LC #69 — binary works better).

---------------------------------------------------
Example (Unimodal):

    f(x) = -(x - 5)²         — peaks at x = 5
    ternary_search_max(f, 0, 10) → approximately 5

    arr = [1, 3, 5, 7, 6, 4, 2]    — peak at index 3
    ternary_search_unimodal_array(arr) → 3
"""

# =========================================================================
# 1. Ternary Search on a Sorted Array
# =========================================================================

def ternary_search_sorted(arr, target):
    """
    Classic ternary search on a sorted array.

    Time Complexity:  O(log₃ n) iterations, each with 2 comparisons.
                      Slightly worse than binary search by a constant factor.
    Space Complexity: O(1)

    Returns the index of `target`, or -1 if not present. Included for
    completeness; prefer binary search in practice.
    """
    lo, hi = 0, len(arr) - 1

    while lo <= hi:
        # divide into three parts at two split points
        mid1 = lo + (hi - lo) // 3
        mid2 = hi - (hi - lo) // 3

        if arr[mid1] == target:
            return mid1
        if arr[mid2] == target:
            return mid2

        if target < arr[mid1]:
            hi = mid1 - 1                         # target is in the left third
        elif target > arr[mid2]:
            lo = mid2 + 1                         # target is in the right third
        else:
            lo = mid1 + 1                         # target is in the middle third
            hi = mid2 - 1

    return -1


# =========================================================================
# 2. Ternary Search on an Integer-Domain Unimodal Array
# =========================================================================

def ternary_search_unimodal_array(arr):
    """
    Find the index of the peak value in a unimodal (increases then
    decreases) integer array.

    Time Complexity:  O(log n)
    Space Complexity: O(1)

    Assumes arr is strictly increasing then strictly decreasing,
    with at least one element.
    """
    if not arr:
        return -1

    lo, hi = 0, len(arr) - 1
    while lo < hi:
        mid1 = lo + (hi - lo) // 3
        mid2 = hi - (hi - lo) // 3

        if arr[mid1] < arr[mid2]:
            lo = mid1 + 1                         # peak is in (mid1, hi]
        else:
            hi = mid2 - 1                         # peak is in [lo, mid2)

    return lo


# =========================================================================
# 3. Ternary Search on a Continuous Unimodal Function
# =========================================================================

def ternary_search_max(f, lo, hi, eps=1e-9):
    """
    Find the argmax of a unimodal function f(x) on the interval [lo, hi].

    f must strictly increase, then strictly decrease, with a single peak
    inside [lo, hi].

    Time Complexity:  O(log((hi - lo) / eps))
    Space Complexity: O(1)

    Each iteration shrinks the bracket by a factor of 2/3. We stop
    when the bracket is narrower than `eps`.
    """
    while hi - lo > eps:
        mid1 = lo + (hi - lo) / 3
        mid2 = hi - (hi - lo) / 3

        if f(mid1) < f(mid2):
            lo = mid1
        else:
            hi = mid2

    return (lo + hi) / 2


def ternary_search_min(f, lo, hi, eps=1e-9):
    """
    Find the argmin of a unimodal (decreases then increases) function.

    Same algorithm, comparison flipped.
    """
    while hi - lo > eps:
        mid1 = lo + (hi - lo) / 3
        mid2 = hi - (hi - lo) / 3

        if f(mid1) > f(mid2):
            lo = mid1
        else:
            hi = mid2

    return (lo + hi) / 2


# =========================================================================
# Test the Functions
# =========================================================================

if __name__ == "__main__":
    # 1. Sorted-array ternary search
    print("Ternary Search on a Sorted Array:")
    arr = [1, 3, 5, 7, 9, 11, 13, 15, 17, 19]
    for target in [1, 9, 19, 4, 20, 13]:
        got = ternary_search_sorted(arr, target)
        print(f"   ternary_search_sorted(arr, {target:2}) = {got}")
    print()

    # 2. Unimodal array (peak finding)
    print("Ternary Search on a Unimodal Array:")
    unimodal_cases = [
        ([1, 3, 5, 7, 6, 4, 2],      3),          # peak at index 3 (value 7)
        ([1, 2, 3, 4, 5],            4),          # strictly increasing — peak at end
        ([5, 4, 3, 2, 1],            0),          # strictly decreasing — peak at start
        ([1, 3, 2],                  1),          # simple 3-element peak
        ([42],                       0),          # single element
    ]
    for arr, expected in unimodal_cases:
        got = ternary_search_unimodal_array(arr)
        assert got == expected, f"{arr}: expected {expected}, got {got}"
        print(f"   ternary_search_unimodal_array({arr}) = {got} (value {arr[got]})")
    print()

    # 3. Continuous unimodal function
    print("Ternary Search on a Continuous Function:")
    # f(x) = -(x - 5)² has a maximum at x = 5
    f = lambda x: -(x - 5) ** 2
    got = ternary_search_max(f, 0, 10)
    print(f"   argmax of f(x) = -(x - 5)² on [0, 10] = {got:.6f}   (expected ~5.0)")
    assert abs(got - 5.0) < 1e-6

    # g(x) = (x - 3)² has a minimum at x = 3
    g = lambda x: (x - 3) ** 2
    got = ternary_search_min(g, 0, 10)
    print(f"   argmin of g(x) = (x - 3)² on [0, 10] = {got:.6f}   (expected ~3.0)")
    assert abs(got - 3.0) < 1e-6

    # 4. Sorted-array tests — verify against binary search semantics
    test_cases = [
        ([1, 3, 5, 7, 9, 11, 13, 15, 17, 19],  9,   4),
        ([1, 3, 5, 7, 9, 11, 13, 15, 17, 19],  1,   0),
        ([1, 3, 5, 7, 9, 11, 13, 15, 17, 19],  19,  9),
        ([1, 3, 5, 7, 9, 11, 13, 15, 17, 19],  4,   -1),
        ([],                                   5,   -1),
        ([42],                                 42,  0),
        ([42],                                 5,   -1),
    ]

    for i, (data, tgt, expected) in enumerate(test_cases):
        got = ternary_search_sorted(data, tgt)
        assert got == expected, (
            f"Test {i+1}: target={tgt}: expected {expected}, got {got}"
        )
        print(f"Test {i+1} passed: sorted target={tgt} -> {got}")

    # Stress test — unimodal array peaks
    import random
    random.seed(3)
    for _ in range(300):
        n = random.randint(1, 30)
        peak = random.randint(0, n - 1)
        left = sorted(random.sample(range(-100, 100), peak))
        right = sorted(random.sample(range(-100, 100), n - 1 - peak), reverse=True)
        top = max((left[-1] if left else -1000),
                  (right[0] if right else -1000)) + 1
        arr = left + [top] + right

        got = ternary_search_unimodal_array(arr)
        expected = arr.index(max(arr))
        assert got == expected, f"stress: {arr}, expected {expected}, got {got}"

    print("\nStress test: 300 random unimodal arrays — peaks found correctly")
    print("\nAll tests passed!")
