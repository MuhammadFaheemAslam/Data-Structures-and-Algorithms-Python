"""
Problem: Palindrome — Four Variants

Difficulty: Easy → Medium

---------------------------------------------------
Covered in this file:

    1. is_palindrome_basic(s)          — exact match, raw string
    2. is_palindrome_normalized(s)     — ignore case and non-alphanumerics (LC #125)
    3. valid_palindrome_with_one_deletion(s)  — allow at most one char deletion (LC #680)
    4. longest_palindrome_length(s)    — longest palindromic substring length

All of these reduce to the same two-pointer-swap pattern from
Phase-04 / 01-Array / problems / easy / 02-reverse.py.

---------------------------------------------------
The Two-Pointer Skeleton (Memorize This):

    left, right = 0, len(s) - 1
    while left < right:
        if s[left] != s[right]:
            return False
        left += 1
        right -= 1
    return True

Time:  O(n)
Space: O(1)

Every palindrome problem is this loop plus some bookkeeping.
"""


# =========================================================================
# 1. Basic Palindrome Check — Exact String
# =========================================================================

def is_palindrome_basic(s):
    """
    True iff `s` reads the same forward and backward, exactly as given.

    Time:  O(n)
    Space: O(1)

        is_palindrome_basic("racecar")  → True
        is_palindrome_basic("hello")    → False
        is_palindrome_basic("ABBA")     → True   (uppercase treated literally)
        is_palindrome_basic("Abba")     → False  (case matters)
    """
    left, right = 0, len(s) - 1
    while left < right:
        if s[left] != s[right]:
            return False
        left += 1
        right -= 1
    return True


# =========================================================================
# 2. Normalized Palindrome (LC #125) — Ignore Case + Non-Alphanumeric
# =========================================================================

def is_palindrome_normalized(s):
    """
    True iff `s` is a palindrome after:
        - removing all non-alphanumeric characters, AND
        - converting to lowercase.

    "A man, a plan, a canal: Panama"  → True
    "race a car"                      → False
    ""                                → True (empty string is trivially a palindrome)

    Time:  O(n)
    Space: O(1)  — two-pointer walk with in-place character filtering
    """
    left, right = 0, len(s) - 1

    while left < right:
        # skip non-alphanumeric chars from the left
        while left < right and not s[left].isalnum():
            left += 1
        # skip from the right
        while left < right and not s[right].isalnum():
            right -= 1

        if s[left].lower() != s[right].lower():
            return False

        left += 1
        right -= 1

    return True


# =========================================================================
# 3. Valid Palindrome with ONE Deletion Allowed (LC #680)
# =========================================================================

def valid_palindrome_with_one_deletion(s):
    """
    True iff `s` CAN be made a palindrome by deleting AT MOST one character.

    "aba"   → True  (already)
    "abca"  → True  (delete 'b' or 'c' → "aba" or "aca")
    "abc"   → False

    Time:  O(n)
    Space: O(1)

    Standard two-pointer walk. On the first mismatch, we have two options:
        a) delete s[left]  — check if s[left+1 .. right] is a palindrome
        b) delete s[right] — check if s[left .. right-1] is a palindrome
    If either is a palindrome, return True.
    """
    def is_palindrome_range(lo, hi):
        while lo < hi:
            if s[lo] != s[hi]:
                return False
            lo += 1
            hi -= 1
        return True

    left, right = 0, len(s) - 1
    while left < right:
        if s[left] != s[right]:
            # try deleting one of them
            return is_palindrome_range(left + 1, right) or is_palindrome_range(left, right - 1)
        left += 1
        right -= 1

    return True


# =========================================================================
# 4. Longest Palindromic Substring — Length Only (Quick Variant)
# =========================================================================

def longest_palindrome_length(s):
    """
    Return the LENGTH of the longest palindromic substring in `s`.

    (For the substring itself, use `longest_palindrome_substring` below.)

    "babad"  → 3 ("bab" or "aba")
    "cbbd"   → 2 ("bb")

    Algorithm: **EXPAND AROUND CENTERS.** For each position in the string,
    expand outward treating that position as the CENTER of a potential
    odd-length palindrome. Then do the same between each pair of adjacent
    positions for even-length palindromes.

    Total work: 2n - 1 centers × O(n) expansion = O(n²).

    Time:  O(n²)
    Space: O(1)  — no new allocations; just pointer walks

    An O(n) algorithm (Manacher's) exists but is overkill for most problems.
    """
    if not s:
        return 0

    def expand(left, right):
        """Return the length of the palindrome centered at (left, right)."""
        while left >= 0 and right < len(s) and s[left] == s[right]:
            left -= 1
            right += 1
        return right - left - 1                 # length after walking one step too far

    best = 1
    for i in range(len(s)):
        best = max(best, expand(i, i))           # odd-length center (single char)
        best = max(best, expand(i, i + 1))       # even-length center (between chars)

    return best


def longest_palindrome_substring(s):
    """
    Return the longest palindromic substring itself (not just its length).

    Same expand-around-centers algorithm, but track the best START and END.

    Time:  O(n²)
    Space: O(1)
    """
    if not s:
        return ""

    def expand(left, right):
        while left >= 0 and right < len(s) and s[left] == s[right]:
            left -= 1
            right += 1
        return left + 1, right - 1              # inclusive bounds AFTER mismatch

    best_start = best_end = 0
    for i in range(len(s)):
        for (lo, hi) in (expand(i, i), expand(i, i + 1)):
            if hi - lo > best_end - best_start:
                best_start, best_end = lo, hi

    return s[best_start:best_end + 1]


# =========================================================================
# Test the Functions
# =========================================================================

if __name__ == "__main__":
    # 1. Basic
    print("1. is_palindrome_basic:")
    basic_cases = [
        ("racecar", True),
        ("hello",   False),
        ("",        True),                       # empty trivially
        ("a",       True),                       # single char
        ("abba",    True),
        ("abcba",   True),
        ("ABBA",    True),
        ("Abba",    False),                      # case matters
    ]
    for s, expected in basic_cases:
        got = is_palindrome_basic(s)
        assert got == expected, f"basic({s!r}): {got} != {expected}"
        print(f"   is_palindrome_basic({s!r:15}) = {got}")
    print()

    # 2. Normalized
    print("2. is_palindrome_normalized (LC #125):")
    norm_cases = [
        ("A man, a plan, a canal: Panama", True),
        ("race a car",                      False),
        ("",                                True),
        (" ",                               True),
        ("0P",                              False),     # '0' != 'p' after lowering
        ("a.",                              True),      # non-alnum is skipped
        ("No 'x' in Nixon",                 True),
    ]
    for s, expected in norm_cases:
        got = is_palindrome_normalized(s)
        assert got == expected, f"normalized({s!r}): {got} != {expected}"
        print(f"   normalized({s!r:35}) = {got}")
    print()

    # 3. One deletion
    print("3. valid_palindrome_with_one_deletion (LC #680):")
    delete_cases = [
        ("aba",        True),                     # already palindrome
        ("abca",       True),                     # delete 'b' or 'c'
        ("abc",        False),
        ("",           True),
        ("a",          True),
        ("deeee",      True),                     # delete 'd' → "eeee"
        ("abcdeca",    False),                    # needs 2 deletions
        ("ebcbbececabbacecbbcbe", True),
    ]
    for s, expected in delete_cases:
        got = valid_palindrome_with_one_deletion(s)
        assert got == expected, f"one_deletion({s!r}): {got} != {expected}"
        print(f"   one_deletion({s!r:30}) = {got}")
    print()

    # 4. Longest palindromic substring
    print("4. longest_palindrome_length and longest_palindrome_substring:")
    long_cases = [
        ("babad",  3, ("bab", "aba")),
        ("cbbd",   2, ("bb",)),
        ("",       0, ("",)),
        ("a",      1, ("a",)),
        ("ac",     1, ("a", "c")),
        ("aaaa",   4, ("aaaa",)),
        ("forgeeksskeegfor", 10, ("geeksskeeg",)),
    ]
    for s, expected_len, valid_subs in long_cases:
        length = longest_palindrome_length(s)
        substring = longest_palindrome_substring(s)
        assert length == expected_len, f"length({s!r}): {length} != {expected_len}"
        assert substring in valid_subs, f"substring({s!r}): {substring} not in {valid_subs}"
        print(f"   s={s!r:25}  length={length}  substring={substring!r}")
    print()

    # Stress test
    import random
    random.seed(42)
    for _ in range(200):
        length = random.randint(0, 30)
        s = "".join(random.choice("abc") for _ in range(length))

        # Sanity: basic palindrome check == exact reverse match
        assert is_palindrome_basic(s) == (s == s[::-1])

    print("Stress test: 200 random strings — basic check matches reverse comparison")

    print("\nAll tests passed!")
