"""
Problem 01: Rotate an Array

Difficulty: Medium (LeetCode #189)

---------------------------------------------------
Problem Statement:

Given an array `nums` and a non-negative integer `k`, rotate the
array to the RIGHT by `k` steps.

    [1, 2, 3, 4, 5, 6, 7], k=3  →  [5, 6, 7, 1, 2, 3, 4]

Follow-ups:
    - Can you do it in O(1) extra space?
    - Can you do it in O(n) time AND O(1) space?

Both "yes". The three-reverse trick is the classic answer.

---------------------------------------------------
The Three Approaches:

    1. Slicing                — O(n) time, O(n) space.  Pythonic, not in place.
    2. Rotate one step × k    — O(n·k) time.            Slow for large k.
    3. Three-reverse trick    — O(n) time, O(1) space.  THE answer.

We show all three. The first is the quick production answer. The second
is the "naïve in-place" attempt to watch fail. The third is the classic.

---------------------------------------------------
The Three-Reverse Trick:

To rotate right by k:

    1. Reverse the ENTIRE array.
    2. Reverse the FIRST k elements.
    3. Reverse the LAST n - k elements.

Example: [1, 2, 3, 4, 5, 6, 7], k = 3

    Start:                      [1, 2, 3, 4, 5, 6, 7]
    Reverse whole:              [7, 6, 5, 4, 3, 2, 1]
    Reverse first k=3:          [5, 6, 7, 4, 3, 2, 1]
    Reverse last n-k=4:         [5, 6, 7, 1, 2, 3, 4]  ← done

Each reverse is O(n) and in place. Total: O(n) time, O(1) space.

---------------------------------------------------
Don't Forget: `k = k % n`

If k > n, rotating by k is the same as rotating by k % n (going
around the cycle multiple times is wasteful). Handle this at the
top of every implementation or you'll run into out-of-range errors.

---------------------------------------------------
"""

# =========================================================================
# Approach 1: Slicing — Pythonic, Not In Place
# =========================================================================

def rotate_slicing(nums, k):
    """
    The idiomatic Python one-liner.

    Time:  O(n)
    Space: O(n) — creates new list
    In place: technically mutates via slice assignment, but allocates
    a new list internally.
    """
    if not nums:
        return nums
    n = len(nums)
    k = k % n
    nums[:] = nums[-k:] + nums[:-k] if k else nums[:]
    return nums


# =========================================================================
# Approach 2: Naïve — Rotate One at a Time × k
# =========================================================================

def rotate_naive(nums, k):
    """
    Rotate right by ONE step, k times. Each step is O(n).

    Time:  O(n · k)
    Space: O(1)

    Works but slow for large k. For k = n/2 on a million-element array,
    this is 500 billion ops — unusable.
    """
    if not nums:
        return nums
    n = len(nums)
    k = k % n

    for _ in range(k):
        last = nums[-1]
        # shift everything right by 1
        for i in range(n - 1, 0, -1):
            nums[i] = nums[i - 1]
        nums[0] = last

    return nums


# =========================================================================
# Approach 3: Three-Reverse Trick — O(n), O(1), In Place
# =========================================================================

def rotate(nums, k):
    """
    Rotate in place using three reverses.

    Time:  O(n)
    Space: O(1)
    """
    n = len(nums)
    if n == 0:
        return nums
    k = k % n

    # Reverse whole array
    _reverse(nums, 0, n - 1)
    # Reverse first k
    _reverse(nums, 0, k - 1)
    # Reverse last n - k
    _reverse(nums, k, n - 1)

    return nums


def _reverse(arr, left, right):
    """Reverse arr[left..right] (INCLUSIVE) in place. O(right - left + 1)."""
    while left < right:
        arr[left], arr[right] = arr[right], arr[left]
        left += 1
        right -= 1


# =========================================================================
# Approach 4: Cyclic Replacements — O(n), O(1), One Pass
# =========================================================================

def rotate_cyclic(nums, k):
    """
    Each element jumps directly to its final position, following cycles.

    Time:  O(n) — each element is touched exactly once
    Space: O(1)

    This is the mathematically elegant version. Works by following
    number-theoretic cycles through the rotation.

    Gotcha: the number of cycles equals gcd(n, k). If gcd > 1, you
    can't traverse all elements with one loop — you need one loop
    per cycle. That's the `count < n` condition.
    """
    n = len(nums)
    if n == 0:
        return nums
    k = k % n
    count = 0

    start = 0
    while count < n:
        current = start
        prev = nums[start]
        while True:
            next_idx = (current + k) % n
            nums[next_idx], prev = prev, nums[next_idx]
            current = next_idx
            count += 1
            if current == start:
                break
        start += 1                                 # move to the next cycle

    return nums


# =========================================================================
# Rotate LEFT — Just a Relabeling
# =========================================================================

def rotate_left(nums, k):
    """
    Rotate LEFT by k. Equivalent to rotating RIGHT by n - k.
    """
    n = len(nums)
    if n == 0:
        return nums
    return rotate(nums, n - (k % n))


# =========================================================================
# Test the Functions
# =========================================================================

if __name__ == "__main__":
    # Canonical example
    nums = [1, 2, 3, 4, 5, 6, 7]
    k = 3
    expected = [5, 6, 7, 1, 2, 3, 4]
    print(f"nums = {nums}, k = {k}")
    print(f"   slicing:          {rotate_slicing(nums[:], k)}")
    print(f"   naive:            {rotate_naive(nums[:], k)}")
    print(f"   three-reverse:    {rotate(nums[:], k)}")
    print(f"   cyclic:           {rotate_cyclic(nums[:], k)}")
    print()

    # Test cases — (nums, k, expected)
    test_cases = [
        ([1, 2, 3, 4, 5, 6, 7],     3,  [5, 6, 7, 1, 2, 3, 4]),
        ([-1, -100, 3, 99],         2,  [3, 99, -1, -100]),
        ([1, 2],                    1,  [2, 1]),
        ([1, 2],                    3,  [2, 1]),           # k > n
        ([1, 2, 3],                 0,  [1, 2, 3]),
        ([1],                       5,  [1]),
        ([],                        3,  []),
        ([1, 2, 3, 4, 5, 6],        6,  [1, 2, 3, 4, 5, 6]),  # k == n
        ([1, 2, 3, 4],              2,  [3, 4, 1, 2]),
    ]

    for i, (nums, k, expected) in enumerate(test_cases):
        for fn in (rotate_slicing, rotate_naive, rotate, rotate_cyclic):
            got = fn(nums[:], k)
            assert got == expected, (
                f"Test {i+1} ({fn.__name__}) failed on {nums} k={k}: "
                f"expected {expected}, got {got}"
            )
        print(f"Test {i+1} passed: nums={nums}, k={k} -> {expected}")

    # rotate_left
    print()
    print("Rotate LEFT:")
    left_cases = [
        ([1, 2, 3, 4, 5], 2, [3, 4, 5, 1, 2]),
        ([1, 2, 3, 4, 5], 0, [1, 2, 3, 4, 5]),
        ([1, 2, 3],       5, [3, 1, 2]),
    ]
    for nums, k, expected in left_cases:
        got = rotate_left(nums[:], k)
        assert got == expected, f"rotate_left({nums}, {k}): expected {expected}, got {got}"
        print(f"   rotate_left({nums}, {k}) = {got}")

    # Stress test
    import random
    random.seed(42)
    for _ in range(300):
        n = random.randint(0, 30)
        data = [random.randint(-100, 100) for _ in range(n)]
        k = random.randint(0, 50)
        results = [fn(data[:], k) for fn in (rotate_slicing, rotate_naive, rotate, rotate_cyclic)]
        for r in results[1:]:
            assert r == results[0], f"disagreement on {data} k={k}: {results}"

    print("\nStress test: 300 random inputs — all four approaches agree")

    print("\nAll tests passed!")
