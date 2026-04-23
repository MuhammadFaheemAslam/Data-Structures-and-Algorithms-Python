"""
sentinel-search.py – Sentinel Linear Search

A classic micro-optimization of linear search. It doesn't change the
algorithm's Big-O (still O(n) time, O(1) space) — it just removes one
comparison from the inner loop.

---------------------------------------------------
The Idea:

Normal linear search has TWO comparisons per iteration:

    while i < n:                          # 1: bounds check
        if arr[i] == target:              # 2: equality check
            return i
        i += 1

The bounds check `i < n` is run every iteration, but it's only true on
the very last iteration. It's pure overhead.

Sentinel search eliminates the bounds check by GUARANTEEING that the
loop will always terminate via the equality check — by appending
`target` itself as a sentinel at the end of the array. Now the loop:

    while arr[i] != target:               # only ONE check
        i += 1

If the real target exists, the loop exits at its real position. If
not, the loop exits at the sentinel's position (i == n). One comparison
removed; same algorithm.

---------------------------------------------------
Does It Matter in Python?

No — in Python, the constant-factor gain is invisible and often
reversed by the cost of the append/pop.

The technique matters in LOW-LEVEL LANGUAGES (C, assembly) where
the compiler can keep the sentinel loop entirely in a couple of
registers. In Python, built-in methods like `list.index()` already do
this dance in C, so writing it yourself buys you nothing.

We implement it here because it's CULTURALLY IMPORTANT — it's a classic
CS idea that appears in every algorithms textbook, and you should be
able to recognize and explain it.

---------------------------------------------------
Variants Shown:

    1. sentinel_search             — append sentinel, scan, pop it back
    2. sentinel_search_non_mutating — wrap in try/finally so the array
                                       restores even if an exception fires
    3. Comparison with regular linear_search — to verify identical output

Run this file to see each variant's output.
"""

# =========================================================================
# 1. Sentinel Search — Modifies the Input Temporarily
# =========================================================================

def sentinel_search(arr, target):
    """
    Sentinel linear search.

    Time:  O(n)
    Space: O(1)

    Returns the index of the first occurrence of `target`, or -1 if
    not present. Restores `arr` to its original state before returning.
    """
    if not arr:
        return -1

    n = len(arr)
    last = arr[-1]                                # remember original tail
    arr[-1] = target                              # plant sentinel

    i = 0
    while arr[i] != target:                       # ONE comparison per step
        i += 1

    arr[-1] = last                                # restore

    # If we landed at the last index, it's a true match only if the
    # original tail WAS the target.
    if i < n - 1:
        return i
    return n - 1 if last == target else -1


# =========================================================================
# 2. Non-Mutating Version — Safe Under Exceptions
# =========================================================================

def sentinel_search_safe(arr, target):
    """
    Like sentinel_search, but restores the array even if something
    raises inside the loop. A good pattern any time you mutate an
    input you don't own.

    Time:  O(n)
    Space: O(1)
    """
    if not arr:
        return -1

    n = len(arr)
    last = arr[-1]

    try:
        arr[-1] = target
        i = 0
        while arr[i] != target:
            i += 1

        if i < n - 1:
            return i
        return n - 1 if last == target else -1
    finally:
        arr[-1] = last                            # always restore


# =========================================================================
# 3. Pure (Non-Destructive) Version via Copy
# =========================================================================

def sentinel_search_pure(arr, target):
    """
    Build a copy with the sentinel appended. Doesn't mutate the input.

    Time:  O(n) — but with a constant-factor overhead for the copy
    Space: O(n)

    Included to show how you'd actually ship a sentinel search in code
    where mutation is unacceptable. In practice, use `list.index()`.
    """
    if not arr:
        return -1

    work = arr + [target]                         # sentinel appended
    i = 0
    while work[i] != target:
        i += 1

    return i if i < len(arr) else -1


# =========================================================================
# 4. The Built-In Equivalent (What You'd Actually Use)
# =========================================================================

def idiomatic_search(arr, target):
    """
    The right answer in real Python code: use the built-in. list.index
    is implemented in C and is a sentinel-search-style linear scan.

    Returns -1 on miss (unlike list.index, which raises ValueError).
    """
    try:
        return arr.index(target)
    except ValueError:
        return -1


# =========================================================================
# Demonstration
# =========================================================================

if __name__ == "__main__":
    arr = [3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5]

    print(f"arr = {arr}")
    print()
    print("Three implementations of the same linear search:")
    print(f"   sentinel_search(arr, 4)        = {sentinel_search(arr, 4)}")
    print(f"   sentinel_search_safe(arr, 4)   = {sentinel_search_safe(arr, 4)}")
    print(f"   sentinel_search_pure(arr, 4)   = {sentinel_search_pure(arr, 4)}")
    print(f"   idiomatic_search(arr, 4)       = {idiomatic_search(arr, 4)}")
    print()

    # Extensive test cases — verify every variant agrees
    test_cases = [
        # (arr, target, expected_index)
        ([3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5], 4,   2),
        ([3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5], 5,   4),          # first of many 5s
        ([3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5], 99,  -1),          # not found
        ([3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5], 5,   4),          # same again
        ([], 1, -1),                                           # empty array
        ([7], 7, 0),                                           # single match
        ([7], 8, -1),                                          # single non-match
        ([1, 2, 3, 4, 5], 5, 4),                               # tail match (touches sentinel slot)
        ([5, 5, 5], 5, 0),                                     # all equal
        ([1, 2, 3, 4, 5], 1, 0),                               # head match
    ]

    for i, (data, tgt, expected) in enumerate(test_cases):
        # copy the array for each variant — sentinel_search mutates
        for fn_name, fn in [
            ("sentinel_search",        sentinel_search),
            ("sentinel_search_safe",   sentinel_search_safe),
            ("sentinel_search_pure",   sentinel_search_pure),
            ("idiomatic_search",       idiomatic_search),
        ]:
            arr_copy = list(data)
            got = fn(arr_copy, tgt)
            assert got == expected, (
                f"Test {i+1} ({fn_name}) failed on {data}, target={tgt}: "
                f"expected {expected}, got {got}"
            )
            # mutating variants must restore
            if fn_name in ("sentinel_search", "sentinel_search_safe"):
                assert arr_copy == data, (
                    f"Test {i+1} ({fn_name}): input was not restored"
                )
        print(f"Test {i+1} passed: arr len={len(data)}, target={tgt} -> {expected}")

    print("\nAll tests passed!")

    # ---------------------------------------------------------------
    # Should You Use Sentinel Search in Real Code?
    #
    #   In Python: NO.
    #   - list.index() is already a C-level linear scan.
    #   - The bookkeeping to plant/remove the sentinel costs more
    #     than the one comparison it saves.
    #
    #   In C: yes, but it's usually done by the compiler already.
    #   Modern C compilers recognize the bounded-loop + constant-comparison
    #   pattern and apply similar optimizations automatically.
    #
    #   Why Teach It Anyway?
    #   - It's culturally important — every algorithms textbook shows it.
    #   - It's a clean example of "trade a small mutation for a loop
    #     simplification" — a pattern you'll see in low-level systems code.
    #   - It makes the bounds check visible, which helps with reasoning
    #     about cache effects and branch prediction.
    # ---------------------------------------------------------------
