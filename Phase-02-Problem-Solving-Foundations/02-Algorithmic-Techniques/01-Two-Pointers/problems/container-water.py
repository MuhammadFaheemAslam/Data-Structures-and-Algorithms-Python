"""
Problem: Container With Most Water

Technique: Two Pointers (converging, with a non-obvious invariant)
Difficulty: Medium (LeetCode #11)

---------------------------------------------------
Problem Statement:

Given `n` non-negative integers `heights[0..n-1]`, where each represents
the height of a vertical line drawn at position i, find two lines that
together with the x-axis form a container holding the most water.

The area of a container formed by lines at positions (i, j) is:

    area(i, j) = min(heights[i], heights[j]) * (j - i)

Return the maximum area achievable.

---------------------------------------------------
The Two-Pointer Lens:

Brute force is O(n^2) — check every pair of lines. Two pointers gets
us to O(n) by exploiting a less obvious invariant than usual:

    Start with the pair (left=0, right=n-1) — maximum possible WIDTH.

    At each step, move the pointer pointing at the SHORTER line.

    Why? Because area = min(h[L], h[R]) * (R - L). If we moved the
    taller pointer inward, width decreases, and min(h[L], h[R]) can
    only stay the same or get WORSE (since it's bounded by the shorter,
    which we didn't change). So there's no hope of improving.

    If instead we move the shorter pointer, width decreases by 1 but
    min(h[L], h[R]) could INCREASE — the new line might be taller.
    That's the only branch where improvement is possible.

Each step eliminates one line from ever being part of the optimal pair
(the shorter one, because any pair involving it and some closer line
can only be smaller), so total work is O(n).

The invariant is harder to see than Two Sum's because we're maximizing
rather than matching a target. But the logic is the same: **each move
rules something out**, so the scan is linear.

Time Complexity:  O(n)
Space Complexity: O(1)

---------------------------------------------------
Example:

    heights = [1, 8, 6, 2, 5, 4, 8, 3, 7]
    Output:  49           # lines at indices 1 (height 8) and 8 (height 7)
                          # area = min(8, 7) * (8 - 1) = 7 * 7 = 49

---------------------------------------------------
"""

# -------------------------------------------------
# The Two-Pointer Solution
# -------------------------------------------------

def max_area(heights):
    """
    Two-pointer O(n) solution to Container With Most Water.

    Time Complexity:  O(n)
    Space Complexity: O(1)
    """
    left, right = 0, len(heights) - 1
    best = 0

    while left < right:
        h = min(heights[left], heights[right])
        area = h * (right - left)
        if area > best:
            best = area

        # always move the pointer at the SHORTER line — the invariant
        # from the docstring
        if heights[left] < heights[right]:
            left += 1
        else:
            right -= 1

    return best


# -------------------------------------------------
# Brute Force for Verification
# -------------------------------------------------

def max_area_brute_force(heights):
    """
    Check every pair — O(n^2). For verifying the two-pointer version.
    """
    n = len(heights)
    best = 0
    for i in range(n):
        for j in range(i + 1, n):
            area = min(heights[i], heights[j]) * (j - i)
            if area > best:
                best = area
    return best


# -------------------------------------------------
# Test the Functions
# -------------------------------------------------

if __name__ == "__main__":
    heights = [1, 8, 6, 2, 5, 4, 8, 3, 7]
    print(f"heights = {heights}")
    print(f"max_area:             {max_area(heights)}")
    print(f"max_area_brute_force: {max_area_brute_force(heights)}")
    print()

    # Test cases — (heights, expected)
    test_cases = [
        ([1, 8, 6, 2, 5, 4, 8, 3, 7],  49),
        ([1, 1],                        1),
        ([4, 3, 2, 1, 4],              16),      # two outer 4s
        ([1, 2, 1],                     2),
        ([0, 0, 0],                     0),
        ([],                            0),
        ([5],                           0),      # only one line → no container
        ([1, 2, 4, 3],                  4),
        ([2, 3, 4, 5, 18, 17, 6],      17),
    ]

    for i, (data, expected) in enumerate(test_cases):
        for fn in (max_area, max_area_brute_force):
            got = fn(data)
            assert got == expected, (
                f"Test {i+1} ({fn.__name__}) failed on {data}: "
                f"expected {expected}, got {got}"
            )
        print(f"Test {i+1} passed: {data} -> {expected}")

    print("\nAll tests passed!")

    # ---------------------------------------------------------------
    # The Lesson:
    #
    #   This problem is chosen because its two-pointer invariant is
    #   subtle. "Move the shorter" looks arbitrary at first — it's
    #   clearly the right choice once you write down what happens in
    #   each branch:
    #
    #     Move taller:   width ↓,    height upper-bounded  → area never improves
    #     Move shorter:  width ↓ 1,  height CAN increase   → possible win
    #
    #   Two-pointer problems are won and lost on identifying such
    #   invariants. When in doubt, literally write down what can and
    #   cannot change under each possible move — the right move is
    #   usually the only one where improvement is possible.
    # ---------------------------------------------------------------
