"""
radix-sort.py – Radix Sort (LSD, with Stable Counting Sort as Inner Loop)

A non-comparison sort that works DIGIT BY DIGIT. For integers with
`d` digits (in some base), radix sort runs in:

    Time:   **O(d · (n + k))** where k = base (typically 10 or 256)
    Space:  O(n + k)

When the keys have a BOUNDED number of digits (e.g., 32-bit ints have
at most 10 decimal digits), radix sort is **O(n)** — asymptotically
faster than comparison sorts.

---------------------------------------------------
The Two Flavours:

### LSD Radix Sort (Least-Significant Digit First)

Sort by the ones digit, then the tens digit, then the hundreds digit, …
Each pass uses a STABLE sort (counting sort) so that earlier passes'
order is preserved within equal-digit groups.

After d passes, the numbers are fully sorted.

This is the standard version and the one we implement.

### MSD Radix Sort (Most-Significant Digit First)

Sort by the highest digit first, RECURSIVELY bucketing equal-MSD
groups. Used for variable-length strings and parallel implementations.
We don't implement MSD here; it's a different beast.

---------------------------------------------------
Why Counting Sort Must Be Stable:

Radix sort's correctness depends on each digit-level sort being
STABLE. If the sort by ones-digit isn't stable, then after the sort
by tens-digit, the ones-digit order within each tens group is
scrambled — and the algorithm silently produces wrong answers.

This is the reason we built stable counting sort in the sibling module.

---------------------------------------------------
The Algorithm:

    def radix_sort(arr):
        max_val = max(arr)
        exp = 1                          # current digit place (1, 10, 100, ...)
        while max_val // exp > 0:
            arr = counting_sort_by_digit(arr, exp)
            exp *= 10

    def counting_sort_by_digit(arr, exp):
        # stable counting sort keyed by (x // exp) % 10

---------------------------------------------------
Example:

    arr = [170, 45, 75, 90, 802, 24, 2, 66]

    Sort by ones:   [170, 90, 802, 2, 24, 45, 75, 66]
    Sort by tens:   [802, 2, 24, 45, 66, 170, 75, 90]
    Sort by hunds:  [2, 24, 45, 66, 75, 90, 170, 802]      ✓

---------------------------------------------------
"""

# =========================================================================
# LSD Radix Sort (Base 10)
# =========================================================================

def radix_sort(arr):
    """
    Sort an array of NON-NEGATIVE integers using LSD radix sort.

    Time:   O(d · (n + k)) where d = number of digits, k = 10
    Space:  O(n + k)
    Stable: Yes

    Handles only non-negative integers. For negatives, see
    `radix_sort_signed`.
    """
    if not arr:
        return arr

    if min(arr) < 0:
        raise ValueError("radix_sort requires non-negative integers; "
                         "use radix_sort_signed() for arrays with negatives")

    max_val = max(arr)
    exp = 1                                       # current digit place: 1, 10, 100, ...

    while max_val // exp > 0:
        arr = _counting_sort_by_digit(arr, exp)
        exp *= 10

    return arr


def _counting_sort_by_digit(arr, exp):
    """
    Stable counting sort keyed by the digit (x // exp) % 10.

    This is exactly stable counting sort, but with a custom key
    (the digit at position `exp`).

    Time:   O(n + 10) = O(n)
    """
    n = len(arr)
    output = [0] * n
    counts = [0] * 10

    # Step 1: count occurrences of each digit
    for x in arr:
        digit = (x // exp) % 10
        counts[digit] += 1

    # Step 2: prefix sum — counts[i] = number of elements with digit ≤ i
    for i in range(1, 10):
        counts[i] += counts[i - 1]

    # Step 3: backward walk for stability
    for x in reversed(arr):
        digit = (x // exp) % 10
        counts[digit] -= 1
        output[counts[digit]] = x

    return output


# =========================================================================
# Handling Negative Integers
# =========================================================================

def radix_sort_signed(arr):
    """
    Radix sort that handles negative integers by splitting, sorting
    each part, and recombining.

    Alternative approach: offset all values by `-min(arr)` to make
    them non-negative, then sort, then subtract back. That's simpler
    but inflates k when values span a huge range.

    This split-and-recombine version is cleaner for mixed-sign inputs
    with modest negatives.

    Time:   O(d · (n + k))
    Space:  O(n)
    """
    if not arr:
        return arr

    negatives = [-x for x in arr if x < 0]        # make positive for sorting
    positives = [x for x in arr if x >= 0]

    # Sort each half
    if negatives:
        negatives = radix_sort(negatives)
        # reverse and negate back (negatives should come first, most negative first)
        negatives = [-x for x in reversed(negatives)]

    if positives:
        positives = radix_sort(positives)

    return negatives + positives


# =========================================================================
# Base-Configurable Radix Sort (For Strings / Byte Arrays)
# =========================================================================

def radix_sort_base(arr, base=10):
    """
    Radix sort in an arbitrary base. Base 256 is standard for sorting
    strings byte-by-byte; base 2 for bitwise radix sort.

    Time:   O(d · (n + base))
    Space:  O(n + base)

    Higher base = fewer digits = fewer passes, but larger counts array
    per pass. Sweet spot depends on n and the key size.
    """
    if not arr:
        return arr

    max_val = max(arr)
    exp = 1

    while max_val // exp > 0:
        arr = _counting_sort_by_digit_base(arr, exp, base)
        exp *= base

    return arr


def _counting_sort_by_digit_base(arr, exp, base):
    n = len(arr)
    output = [0] * n
    counts = [0] * base

    for x in arr:
        digit = (x // exp) % base
        counts[digit] += 1

    for i in range(1, base):
        counts[i] += counts[i - 1]

    for x in reversed(arr):
        digit = (x // exp) % base
        counts[digit] -= 1
        output[counts[digit]] = x

    return output


# =========================================================================
# Test the Functions
# =========================================================================

if __name__ == "__main__":
    arr = [170, 45, 75, 90, 802, 24, 2, 66]
    print(f"Input:  {arr}")
    sorted_arr = radix_sort(arr[:])
    print(f"Sorted: {sorted_arr}")
    print()

    # Test cases — (arr, expected)
    test_cases = [
        ([170, 45, 75, 90, 802, 24, 2, 66], [2, 24, 45, 66, 75, 90, 170, 802]),
        ([],                                [],),
        ([5],                               [5],),
        ([1, 2, 3, 4, 5],                   [1, 2, 3, 4, 5]),
        ([5, 4, 3, 2, 1],                   [1, 2, 3, 4, 5]),
        ([0, 0, 0, 0],                      [0, 0, 0, 0]),
        ([1000, 100, 10, 1],                [1, 10, 100, 1000]),
        ([999, 1, 50],                      [1, 50, 999]),
        ([3, 30, 300, 3000, 30000],          [3, 30, 300, 3000, 30000]),
    ]

    for i, (data, expected) in enumerate(test_cases):
        # Handle Python's one-tuple quirk (empty list test)
        if isinstance(expected, list):
            exp = expected
        else:
            exp = list(expected)
        got = radix_sort(data[:])
        assert got == exp, f"Test {i+1} failed on {data}: expected {exp}, got {got}"
        print(f"Test {i+1} passed: {data} -> {got}")

    # Signed version
    print()
    print("radix_sort_signed (handles negatives):")
    signed_cases = [
        [-3, -1, -4, -1, -5, 9, 2, 6, 5, 3, 5],
        [-5, -4, -3, -2, -1],
        [-1],
        [0, -1, 0, -2, 0],
        [100, -100, 50, -50],
    ]
    for data in signed_cases:
        expected = sorted(data)
        got = radix_sort_signed(data[:])
        assert got == expected, f"{data}: expected {expected}, got {got}"
        print(f"   {data} -> {got}")

    # Different bases
    print()
    print("radix_sort_base (various bases):")
    for base in [2, 10, 16, 256]:
        arr = [170, 45, 75, 90, 802, 24, 2, 66]
        got = radix_sort_base(arr[:], base=base)
        expected = sorted(arr)
        assert got == expected, f"base={base}: expected {expected}, got {got}"
        print(f"   base={base:>3}:  {got}")

    # Stress test
    import random
    random.seed(42)
    for _ in range(200):
        n = random.randint(0, 100)
        data = [random.randint(0, 10**6) for _ in range(n)]
        assert radix_sort(data[:]) == sorted(data)

    for _ in range(100):
        n = random.randint(0, 100)
        data = [random.randint(-1000, 1000) for _ in range(n)]
        assert radix_sort_signed(data[:]) == sorted(data)

    print("\nStress test: 200 non-neg + 100 signed random inputs — all matched sorted()")

    # Performance demo — radix sort on a large input with small keys
    import time
    n = 200_000

    # Small-key case: 6-digit integers, 200k of them
    random.seed(0)
    data = [random.randint(0, 10**6 - 1) for _ in range(n)]

    t0 = time.time()
    radix_sort(data[:])
    t_radix = time.time() - t0

    t0 = time.time()
    sorted(data)
    t_py = time.time() - t0

    print()
    print(f"Timing on n={n}, 6-digit integers:")
    print(f"   radix_sort:     {t_radix:.3f}s  (O(d·n) = O(6·n))")
    print(f"   Python sorted:  {t_py:.3f}s     (Timsort in C — very fast constants)")
    print("   (Python's sorted() typically wins in real Python due to C-level speed.)")

    print("\nAll tests passed!")

    # ---------------------------------------------------------------
    # Radix Sort's Niche in Practice:
    #
    #   Pure-Python radix sort is slower than Python's C-level
    #   sorted(). The theoretical O(n) vs O(n log n) doesn't matter
    #   when the constant factor difference is 30-50x.
    #
    # Where radix sort dominates:
    #   - **C/C++ implementations** sorting large arrays of fixed-
    #     width integers or short strings.
    #   - **Hardware radix sort** in GPUs / FPGAs — amenable to
    #     massive parallelism.
    #   - **Database indexing** of integer keys.
    #   - **Specialized domains**: genomics (DNA sequences = base-4),
    #     networking (IP address sorting = 4 bytes, base-256).
    # ---------------------------------------------------------------
