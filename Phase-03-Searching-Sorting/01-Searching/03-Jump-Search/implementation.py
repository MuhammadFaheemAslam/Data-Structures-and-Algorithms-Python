"""
implementation.py – Jump Search

An O(√n) search algorithm on sorted arrays. Positioned BETWEEN linear
search (O(n)) and binary search (O(log n)) — slower than binary search
in theory, but historically useful on media where "jumping ahead" is
cheap but "seeking backward" is expensive (think: magnetic tape).

---------------------------------------------------
The Algorithm:

    1. Pick a block size `step = floor(sqrt(n))`.
    2. JUMP forward `step` indices at a time until we either
       overshoot the target or hit the end of the array.
    3. Within the last block (between the previous jump and the
       current position), LINEAR-SEARCH for the target.

    lo = 0
    step = int(sqrt(n))
    # find the block that might contain target
    while lo < n and arr[min(lo + step, n) - 1] < target:
        lo += step
    # linear-search inside that block
    for i in range(lo, min(lo + step, n)):
        if arr[i] == target:
            return i
    return -1

Jumping is O(n / step); linear within a block is O(step). Total work
is O(n/step + step), minimized at step = √n, giving O(√n).

---------------------------------------------------
Is Jump Search Useful in Python?

Honestly — not really, for in-memory arrays. Binary search is strictly
better at O(log n). Jump search's reason to exist is:

    - When seeks are much slower than sequential reads (tapes, some
      disk layouts, some compressed streams).
    - When comparisons are cheap but skipping forward is expensive.
    - As a pedagogical stepping stone between linear and binary search.

In modern memory hierarchies with random access, binary search wins.
Keep this algorithm in your vocabulary for the interview where it
comes up, and for the rare low-level system where tape-like access
dominates.

---------------------------------------------------
Example:

    arr = [1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23]  (n=12, step=3)
    jump_search(arr, 15)
        block 0 (i=0):  arr[2] = 5  < 15 → jump
        block 1 (i=3):  arr[5] = 11 < 15 → jump
        block 2 (i=6):  arr[8] = 17 ≥ 15 → stop, linear-search arr[6..8]
        found at i=7
"""

import math


# =========================================================================
# Jump Search
# =========================================================================

def jump_search(arr, target):
    """
    Return the index of `target` in sorted `arr`, or -1 if not present.

    Time Complexity:  O(√n)
    Space Complexity: O(1)
    """
    n = len(arr)
    if n == 0:
        return -1

    step = max(1, int(math.sqrt(n)))
    lo = 0

    # 1) Find the block that might contain target.
    while lo < n and arr[min(lo + step, n) - 1] < target:
        lo += step

    # 2) Linear-search within the candidate block.
    for i in range(lo, min(lo + step, n)):
        if arr[i] == target:
            return i

    return -1


# =========================================================================
# Variant: Jump Search with Custom Block Size
# =========================================================================

def jump_search_custom_step(arr, target, step):
    """
    Jump search with a user-specified block size. Useful for:
      - Analyzing how step size affects runtime (step = n^α for α ∈ (0, 1)).
      - Scenarios where seek cost / read cost ratio is known.

    Total cost scales as O(n/step + step); step = √n is the minimizer.
    """
    n = len(arr)
    if n == 0 or step <= 0:
        return -1

    lo = 0
    while lo < n and arr[min(lo + step, n) - 1] < target:
        lo += step

    for i in range(lo, min(lo + step, n)):
        if arr[i] == target:
            return i

    return -1


# =========================================================================
# Test the Functions
# =========================================================================

if __name__ == "__main__":
    arr = [1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23]

    print(f"arr = {arr}")
    print(f"sqrt(n) step = {int(math.sqrt(len(arr)))}")
    print()
    for target in [1, 15, 23, 4, 24, 13, 0]:
        got = jump_search(arr, target)
        print(f"   jump_search(arr, {target:2}) = {got}")
    print()

    # Test cases — (arr, target, expected)
    test_cases = [
        ([1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23], 15,  7),
        ([1, 3, 5, 7, 9],                             5,   2),
        ([1, 3, 5, 7, 9],                             1,   0),
        ([1, 3, 5, 7, 9],                             9,   4),
        ([1, 3, 5, 7, 9],                             4,  -1),
        ([1, 3, 5, 7, 9],                             0,  -1),
        ([1, 3, 5, 7, 9],                             10, -1),
        ([],                                          5,  -1),
        ([42],                                        42,  0),
        ([42],                                        10, -1),
        ([1, 1, 1, 1, 1],                             1,   0),   # first match
    ]

    for i, (data, tgt, expected) in enumerate(test_cases):
        got = jump_search(data, tgt)
        # For "first match" semantics on equals, verify we found SOME valid index
        if expected == -1:
            assert got == -1, f"Test {i+1}: expected -1, got {got}"
        else:
            assert 0 <= got < len(data) and data[got] == tgt, (
                f"Test {i+1}: returned {got} not valid for {data}, target={tgt}"
            )
        print(f"Test {i+1} passed: target={tgt} -> {got}")

    # Stress test — compare against Python's index()
    import random
    random.seed(42)
    for _ in range(200):
        n = random.randint(0, 100)
        arr = sorted(random.sample(range(-200, 200), n))
        target = random.randint(-250, 250)

        got = jump_search(arr, target)
        expected = arr.index(target) if target in arr else -1

        if target in arr:
            # multiple occurrences — either algorithm can return any valid index
            assert got >= 0 and arr[got] == target
        else:
            assert got == -1

    print("\nStress test: 200 random sorted arrays matched linear scan")
    print("\nAll tests passed!")
