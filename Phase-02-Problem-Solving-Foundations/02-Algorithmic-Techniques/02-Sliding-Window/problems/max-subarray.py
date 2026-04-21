"""
Problem: Maximum Sum Subarray of Size K

Technique: Sliding Window (FIXED size)
Difficulty: Easy

---------------------------------------------------
Problem Statement:

Given an array of integers `arr` and a positive integer `k`, find the
contiguous subarray of length exactly `k` with the maximum sum and
return that sum.

(Note: this is different from the Maximum Subarray problem in Phase-02
/ 01 / 01-Brute-Force / problems / max-subarray.py, which allows ANY
length. THAT problem is solved with Kadane's DP. THIS one is the
canonical fixed-sliding-window problem.)

---------------------------------------------------
The Sliding-Window Lens:

Brute force: for each starting index, sum k elements → O(n * k).

Sliding window: notice that going from window [i, i+k-1] to [i+1, i+k],
we REMOVE arr[i] and ADD arr[i+k]. That's a net O(1) update to the
running sum. Total work: O(n).

The same-direction two-pointer structure is obvious here:
    - left  = window start
    - right = window end
    - both advance by exactly 1 per step (fixed size)

---------------------------------------------------
Example:

    arr = [2, 1, 5, 1, 3, 2], k = 3
    -> 9   # best window is [5, 1, 3]

---------------------------------------------------
"""

# -------------------------------------------------
# The Sliding-Window Solution — O(n)
# -------------------------------------------------

def max_sum_subarray_size_k(arr, k):
    """
    Return the maximum sum over all contiguous subarrays of length `k`.

    Time Complexity:  O(n)
    Space Complexity: O(1)

    Returns None if len(arr) < k (no valid window exists).
    """
    if len(arr) < k or k <= 0:
        return None

    # 1. prime: compute sum of the first window
    window_sum = sum(arr[:k])
    best = window_sum

    # 2. slide: O(1) per step — add new right, remove old left
    for i in range(k, len(arr)):
        window_sum += arr[i] - arr[i - k]
        if window_sum > best:
            best = window_sum

    return best


# -------------------------------------------------
# Brute Force for Verification — O(n * k)
# -------------------------------------------------

def max_sum_subarray_size_k_brute_force(arr, k):
    """
    Re-sum every window from scratch. Used only to validate the sliding
    version.
    """
    if len(arr) < k or k <= 0:
        return None

    best = float("-inf")
    for i in range(len(arr) - k + 1):
        s = sum(arr[i:i + k])
        if s > best:
            best = s

    return best


# -------------------------------------------------
# Test the Functions
# -------------------------------------------------

if __name__ == "__main__":
    arr = [2, 1, 5, 1, 3, 2]
    k = 3

    print(f"arr = {arr}, k = {k}")
    print(f"max_sum_subarray_size_k:              {max_sum_subarray_size_k(arr, k)}")
    print(f"max_sum_subarray_size_k_brute_force:  {max_sum_subarray_size_k_brute_force(arr, k)}")
    print()

    # Test cases — (arr, k, expected)
    test_cases = [
        ([2, 1, 5, 1, 3, 2],           3,    9),     # [5, 1, 3]
        ([2, 3, 4, 1, 5],              2,    7),     # [3, 4]
        ([5, 7, 1, 3, 4, 2, 1],        4,    16),    # [5, 7, 1, 3]? = 16; or [7,1,3,4]=15 → 16
        ([-1, -2, -3, -4],             2,   -3),     # [-1, -2] = -3, best of all-negative
        ([10, 20, -30, 40, 50],        3,    60),    # [40, 50, -30]=60? no: [-30,40,50]=60
        ([1],                          1,    1),
        ([1, 2],                       3,    None),  # k > len
        ([5, 5, 5, 5, 5],              2,    10),    # all same
        ([100, 200, 300, 400],         4,    1000),  # k == n
    ]

    for i, (data, kk, expected) in enumerate(test_cases):
        for fn in (max_sum_subarray_size_k, max_sum_subarray_size_k_brute_force):
            got = fn(data, kk)
            assert got == expected, (
                f"Test {i+1} ({fn.__name__}) failed on {data} k={kk}: "
                f"expected {expected}, got {got}"
            )
        print(f"Test {i+1} passed: arr={data}, k={kk} -> {expected}")

    print("\nAll tests passed!")

    # ---------------------------------------------------------------
    # Why This Is the Canonical Fixed-Window Problem:
    #
    #   It's the cleanest possible showcase:
    #     - Window state is a single int (running sum).
    #     - Update is literally `+= arr[new] - arr[old]`.
    #     - No dicts, no deques, no edge cases.
    #
    #   Every other fixed-window problem adds complexity on top of
    #   this skeleton: tracking a max via a monotonic deque, counting
    #   distinct elements via a dict, etc. Learn this pattern by heart
    #   and the rest is just "what's my window state?"
    # ---------------------------------------------------------------
