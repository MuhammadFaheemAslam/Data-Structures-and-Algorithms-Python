"""
Problem: Find the Duplicate Number

Difficulty: Medium (LeetCode #287)

---------------------------------------------------
Problem Statement:

Given an array `nums` containing n + 1 integers where each integer
is in the range [1, n] (INCLUSIVE), there is exactly ONE duplicated
number. Find it.

Constraints:
    - Must NOT modify the array.
    - Must use only O(1) extra space.
    - Must use less than O(n²) time.

---------------------------------------------------
Why This Is a Floyd's Problem in Disguise:

The array `nums` can be interpreted as a FUNCTION:

    f(i) = nums[i]

Start at index 0. Repeatedly apply f (i.e., `i = nums[i]`). This
generates a sequence of indices. Key observation:

    - Since values are in [1, n], f(i) for any i is in [1, n] — an
      index of the array.
    - Starting at index 0 (which is NOT in the range [1, n]), the
      sequence `0 → f(0) → f(f(0)) → ...` can never return to 0.
    - The sequence must eventually REPEAT (there are only n+1 possible
      values, so by pigeonhole).
    - The repetition means there's a CYCLE in this function graph.
    - The ENTRY of the cycle is the duplicated number.

So the problem reduces to "find the start of the cycle" in a functional
graph — which is exactly Floyd's algorithm, applied to the implicit
"linked list" defined by f(i) = nums[i].

---------------------------------------------------
The Algorithm:

Phase 1 (find the meeting point inside the cycle):

    slow = nums[0]
    fast = nums[0]
    while True:
        slow = nums[slow]
        fast = nums[nums[fast]]
        if slow == fast:
            break

Phase 2 (find the entry = the duplicate):

    slow = nums[0]                    # reset to start
    while slow != fast:
        slow = nums[slow]
        fast = nums[fast]
    return slow

---------------------------------------------------
Time:  O(n)
Space: O(1)

---------------------------------------------------
Why the Entry IS the Duplicate:

The function f(i) = nums[i] maps n+1 indices into a range of n
values. By pigeonhole, TWO distinct indices i and j have f(i) = f(j)
= some value v. That means v has MULTIPLE predecessors in the
function graph, which is exactly how cycles form.

The cycle ENTRY is the first index that's reached from MULTIPLE
paths. Starting from index 0, the path enters the cycle at some
"merge point" — and that merge point is the duplicated value.

---------------------------------------------------
"""


# =========================================================================
# Solution 1: Floyd's — O(n) Time, O(1) Space
# =========================================================================

def find_duplicate(nums):
    """
    Find the single duplicate in a list of n+1 integers in [1, n].

    Time:  O(n)
    Space: O(1)
    """
    # Phase 1: detect the cycle
    slow = fast = nums[0]
    while True:
        slow = nums[slow]
        fast = nums[nums[fast]]
        if slow == fast:
            break

    # Phase 2: find the entrance (= duplicate)
    slow = nums[0]
    while slow != fast:
        slow = nums[slow]
        fast = nums[fast]
    return slow


# =========================================================================
# Solution 2: Hash Set — O(n) Time, O(n) Space (Fails the O(1)-Space Constraint)
# =========================================================================

def find_duplicate_hashset(nums):
    """
    Obvious approach — use a hash set. Violates the O(1) space constraint
    but useful for validation.
    """
    seen = set()
    for x in nums:
        if x in seen:
            return x
        seen.add(x)
    return -1                                     # unreachable under the problem's invariants


# =========================================================================
# Solution 3: Sort and Find Adjacent Duplicate — Modifies the Array
# =========================================================================

def find_duplicate_sort(nums):
    """
    Sort and scan for adjacent duplicates. O(n log n) time, O(1) space
    (if you sort IN PLACE). But this MUTATES the array — violates the
    problem's no-modification constraint. Included for comparison only.
    """
    sorted_nums = sorted(nums)
    for i in range(1, len(sorted_nums)):
        if sorted_nums[i] == sorted_nums[i - 1]:
            return sorted_nums[i]
    return -1


# =========================================================================
# Solution 4: Binary Search on the Answer — O(n log n) Time, O(1) Space
# =========================================================================

def find_duplicate_binary_search(nums):
    """
    Binary-search the VALUE RANGE [1, n]. For a candidate value `mid`,
    count how many elements in nums are ≤ mid. If that count > mid,
    the duplicate is in [1, mid]; else in [mid+1, n].

    Time:  O(n log n)
    Space: O(1)

    Slower than Floyd's but also O(1) space; useful variant to know.
    """
    lo, hi = 1, len(nums) - 1                     # values are in [1, n]
    while lo < hi:
        mid = (lo + hi) // 2
        count = sum(1 for x in nums if x <= mid)
        if count > mid:
            hi = mid                              # duplicate is in [lo, mid]
        else:
            lo = mid + 1                          # duplicate is in [mid+1, hi]
    return lo


# =========================================================================
# Test the Functions
# =========================================================================

if __name__ == "__main__":
    # LC #287 examples
    cases = [
        ([1, 3, 4, 2, 2],             2),
        ([3, 1, 3, 4, 2],             3),
        ([1, 1],                      1),
        ([1, 1, 2],                   1),
        ([2, 2, 2, 2, 2],             2),         # all duplicates of 2
        ([1, 4, 4, 2, 4],             4),
        ([3, 3, 3, 3, 3, 3, 3],       3),
    ]

    for nums, expected in cases:
        for fn in (find_duplicate, find_duplicate_hashset,
                   find_duplicate_sort, find_duplicate_binary_search):
            # sort / binary_search mutate their inputs? no — sort copies, binary just counts
            got = fn(nums[:])
            assert got == expected, f"{fn.__name__}({nums}): {got} != {expected}"
        print(f"find_duplicate({nums}) = {expected}")

    # Stress test
    import random
    random.seed(42)
    for _ in range(200):
        n = random.randint(1, 50)
        values = list(range(1, n + 1))            # {1, 2, …, n}
        duplicate = random.choice(values)
        nums = values + [duplicate]
        random.shuffle(nums)

        for fn in (find_duplicate, find_duplicate_hashset,
                   find_duplicate_sort, find_duplicate_binary_search):
            assert fn(nums[:]) == duplicate

    print("\nStress test: 200 random inputs — all four approaches agree")

    print("\nAll tests passed!")

    # ---------------------------------------------------------------
    # Why This Problem Is a Classic:
    #
    #   It's the clearest example of "Floyd's algorithm on a NON-LINKED-LIST
    #   input." By treating nums as a function graph, we get the full
    #   cycle-detection + entry-point machinery for free.
    #
    # Related problems using this same "array as function graph" trick:
    #
    #   - Happy Number (LC #202) — next(n) = sum of squares of digits
    #   - Find the Duplicate Number (this problem)
    #   - Circular Array Loop (LC #457)
    #
    # In all three, Floyd's tortoise-and-hare is the key insight.
    # ---------------------------------------------------------------
