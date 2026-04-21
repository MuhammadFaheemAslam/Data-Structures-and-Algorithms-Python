"""
Problem: Largest Rectangle in Histogram

Technique: Monotonic Stack — the hardest classical monotonic-stack problem
Difficulty: Hard (LeetCode #84)

---------------------------------------------------
Problem Statement:

Given an array of non-negative integers `heights`, where `heights[i]`
is the height of the bar at position `i` in a histogram, find the
largest rectangle that can be formed within the histogram.

(Each bar has width 1. The rectangle must have its base on the
x-axis and fit entirely between/under the bars.)

---------------------------------------------------
The Monotonic-Stack Lens:

Brute force (per bar):
    For each bar i, expand outward — find the first bar to the LEFT
    that is STRICTLY SHORTER than heights[i], and likewise to the
    RIGHT. The largest rectangle ANCHORED at height heights[i] has
    width = right - left - 1, so area = heights[i] * (right - left - 1).
    Take the max over all i.

Computing "first shorter to the left" and "first shorter to the right"
for each bar is a textbook monotonic-stack pair — each in O(n).
After those precomputations, the answer is a simple max over O(n)
candidates.

We'll show two variants:

    1. Two-pass version (prev-smaller + next-smaller arrays).
       Clean, pedagogical, O(n) time.

    2. Single-pass version (one stack, sentinel 0 appended).
       More compact; same complexity; favoured in interviews.

---------------------------------------------------
The Single-Pass Trick:

As we walk the array left-to-right, maintain a stack of indices whose
heights are INCREASING. When a new bar is shorter than the stack's
top, we've just found a "next smaller to the right" for the top.
After popping the top:
    - The NEW top is the "previous smaller to the left" for the popped index.
    - The current position is the "next smaller to the right".
    - So the rectangle ending at the popped index has:
          height = heights[popped]
          width  = (current_i - 1) - (new_top) = current_i - new_top - 1

Append a sentinel 0 at the end to flush the stack.

Time Complexity:  O(n)
Space Complexity: O(n)

---------------------------------------------------
Example:

    heights = [2, 1, 5, 6, 2, 3]

    The largest rectangle has area 10 — bars at indices 2 and 3 (heights
    5 and 6), limited to the minimum height (5) across those two bars:
    width = 2, height = 5 → area = 10.

---------------------------------------------------
"""

# -------------------------------------------------
# Approach 1: Two-Pass Monotonic Stacks (Pedagogical)
# -------------------------------------------------

def largest_rectangle_two_pass(heights):
    """
    Compute prev-smaller and next-smaller arrays, then the answer.

    Time Complexity:  O(n)
    Space Complexity: O(n)
    """
    n = len(heights)
    if n == 0:
        return 0

    # prev_smaller[i] = index of the nearest bar to the LEFT shorter than heights[i], or -1
    prev_smaller = [-1] * n
    stack = []
    for i in range(n):
        while stack and heights[stack[-1]] >= heights[i]:
            stack.pop()
        prev_smaller[i] = stack[-1] if stack else -1
        stack.append(i)

    # next_smaller[i] = index of the nearest bar to the RIGHT shorter than heights[i], or n
    next_smaller = [n] * n
    stack = []
    for i in range(n - 1, -1, -1):
        while stack and heights[stack[-1]] >= heights[i]:
            stack.pop()
        next_smaller[i] = stack[-1] if stack else n
        stack.append(i)

    # for each bar, compute the rectangle anchored at heights[i]
    best = 0
    for i in range(n):
        width = next_smaller[i] - prev_smaller[i] - 1
        area = heights[i] * width
        if area > best:
            best = area

    return best


# -------------------------------------------------
# Approach 2: Single-Pass with Sentinel (Interview-Standard)
# -------------------------------------------------

def largest_rectangle(heights):
    """
    One-pass monotonic stack with a trailing 0 sentinel to flush
    everything out at the end.

    Time Complexity:  O(n)
    Space Complexity: O(n)

    The single-pass version is more compact and arguably more elegant;
    it's what most interview solutions ship. The two-pass version
    (Approach 1) is better for TEACHING the idea.
    """
    stack = []                                    # holds indices; heights INCREASING
    best = 0

    # iterate with a sentinel height of 0 at the end to flush the stack
    for i, h in enumerate(heights + [0]):
        while stack and heights[stack[-1]] > h:
            top = stack.pop()
            # width bounded on the right by i (the current, smaller bar)
            # and on the left by the NEW stack top (nearest smaller to left)
            # or by -1 if the stack is empty (all bars so far were taller)
            left_bound = stack[-1] if stack else -1
            width = i - left_bound - 1
            area = heights[top] * width
            if area > best:
                best = area
        stack.append(i)

    return best


# -------------------------------------------------
# Approach 3: Brute Force — O(n²)
# -------------------------------------------------

def largest_rectangle_brute_force(heights):
    """
    For each bar, expand outward to find the widest rectangle of at
    least that height.

    Time Complexity:  O(n²)
    Space Complexity: O(1)

    Used only for validation on small inputs.
    """
    n = len(heights)
    best = 0
    for i in range(n):
        # expand left while bars >= heights[i]
        left = i
        while left > 0 and heights[left - 1] >= heights[i]:
            left -= 1
        # expand right while bars >= heights[i]
        right = i
        while right < n - 1 and heights[right + 1] >= heights[i]:
            right += 1
        area = heights[i] * (right - left + 1)
        if area > best:
            best = area
    return best


# -------------------------------------------------
# Test the Functions
# -------------------------------------------------

if __name__ == "__main__":
    heights = [2, 1, 5, 6, 2, 3]

    print(f"heights = {heights}")
    print(f"largest_rectangle             (one-pass)   = {largest_rectangle(heights)}")
    print(f"largest_rectangle_two_pass                = {largest_rectangle_two_pass(heights)}")
    print(f"largest_rectangle_brute_force             = {largest_rectangle_brute_force(heights)}")
    print()

    # Test cases — (heights, expected)
    test_cases = [
        ([2, 1, 5, 6, 2, 3],        10),          # canonical example
        ([2, 4],                    4),           # smaller of the two is the limiter
        ([],                        0),
        ([1],                       1),
        ([0, 0, 0],                 0),
        ([5, 5, 5, 5],              20),          # uniform — full rectangle
        ([1, 2, 3, 4, 5],           9),           # 3×3 anchored at heights[2..4]
        ([5, 4, 3, 2, 1],           9),           # mirror of above
        ([2, 1, 2],                 3),           # limited by the 1 in the middle
        ([6, 7, 5, 2, 4, 5, 9, 3],  16),          # [4, 5, 9, 3] → no; [5, 9]=18? nope, let's compute... we'll trust brute force
    ]

    for i, (data, expected) in enumerate(test_cases):
        got_1 = largest_rectangle(data)
        got_2 = largest_rectangle_two_pass(data)
        got_bf = largest_rectangle_brute_force(data)

        assert got_1 == expected, f"Test {i+1} (one-pass): expected {expected}, got {got_1}"
        assert got_2 == expected, f"Test {i+1} (two-pass): expected {expected}, got {got_2}"
        assert got_bf == expected, f"Test {i+1} (brute):   expected {expected}, got {got_bf}"
        print(f"Test {i+1} passed: {data} -> {expected}")

    # Stress test against brute force
    import random
    random.seed(7)
    for _ in range(200):
        n = random.randint(0, 20)
        data = [random.randint(0, 10) for _ in range(n)]
        bf = largest_rectangle_brute_force(data)
        ms = largest_rectangle(data)
        assert bf == ms, f"stress: {data} → brute {bf}, stack {ms}"
    print("\nStress test: 200 random histograms matched brute force")

    print("\nAll tests passed!")

    # ---------------------------------------------------------------
    # Why This Is the Hardest Classical Monotonic-Stack Problem:
    #
    #   1. You have to identify the right SUB-QUESTION:
    #         "for each bar, what's the widest rectangle of at least
    #          this height anchored here?"
    #      That reduces to prev-smaller + next-smaller.
    #
    #   2. The SENTINEL trick (append a 0) is non-obvious and
    #      easy to get wrong under pressure.
    #
    #   3. The invariants are subtle: the stack holds INCREASING bars,
    #      and popping happens when the NEW bar is shorter. When you
    #      pop, you know two things at once — "next smaller to the
    #      right" is the CURRENT index, "previous smaller to the left"
    #      is the NEW stack top.
    #
    # If you can explain the single-pass version fluently, you've
    # mastered monotonic stacks. Maximal Rectangle (LC #85) and
    # Trapping Rain Water (LC #42) are both direct extensions.
    # ---------------------------------------------------------------
