"""
Problem: Palindrome Check via Deque

Difficulty: Easy

---------------------------------------------------
Problem Statement:

Given a string (or array), determine whether it reads the same
forward and backward — using a DEQUE.

Covered in this file:

    1. is_palindrome_deque(s)                   — basic check
    2. is_palindrome_normalized(s)              — ignore case + non-alphanumeric
    3. PalindromeDeque (class)                  — streaming: push/pop and ask "is the current content a palindrome?"

---------------------------------------------------
Why a Deque?

We already solved palindrome checks with two pointers in
02-String/problems/palindrome.py. The **two-pointer walk IS a deque
operation in disguise**:

    while left < right:
        l, r = s[left], s[right]      ↔   l, r = d.popleft(), d.pop()
        if l != r: return False
        left += 1; right -= 1

The deque framing makes explicit what the two-pointer approach
encodes implicitly: we're repeatedly TAKING THE FIRST AND LAST
characters and comparing them.

The deque framing ALSO generalizes nicely to streaming cases —
where characters arrive one at a time and you want to maintain a
"current string, with a palindrome-check primitive." See
`PalindromeDeque` below.

---------------------------------------------------
Complexity:

    Time:  O(n)
    Space: O(n) for the deque

---------------------------------------------------
"""

from collections import deque


# =========================================================================
# 1. Basic Palindrome Check via Deque
# =========================================================================

def is_palindrome_deque(s):
    """
    True iff `s` (string or list) reads the same in both directions.

    Time:  O(n)
    Space: O(n)
    """
    d = deque(s)
    while len(d) > 1:
        if d.popleft() != d.pop():
            return False
    return True


# =========================================================================
# 2. Normalized Palindrome (ignore case, skip non-alphanumeric)
# =========================================================================

def is_palindrome_normalized(s):
    """
    True iff `s` is a palindrome after removing non-alphanumeric
    characters and lowercasing. Matches LC #125.

    Time:  O(n)
    Space: O(n)
    """
    # Filter and lowercase as we go
    d = deque(c.lower() for c in s if c.isalnum())
    while len(d) > 1:
        if d.popleft() != d.pop():
            return False
    return True


# =========================================================================
# 3. Streaming PalindromeDeque
# =========================================================================

class PalindromeDeque:
    """
    A deque that also answers "is the current sequence a palindrome?"
    in O(n) per query.

    You can push/pop from either end as the string evolves. Useful
    for:
        - Interactive builders ("is it STILL a palindrome after this
          character?" queries).
        - Puzzles / IOCCC-style problems.

    Implementation note: each is_palindrome() query is O(n). To do
    better (O(1) query), you'd need a more clever structure like a
    rolling hash (not covered here).
    """

    def __init__(self, iterable=None):
        self._d = deque(iterable) if iterable is not None else deque()

    def append(self, ch):
        """Add to the back. O(1)."""
        self._d.append(ch)

    def appendleft(self, ch):
        """Add to the front. O(1)."""
        self._d.appendleft(ch)

    def pop(self):
        """Remove and return back. O(1)."""
        return self._d.pop()

    def popleft(self):
        """Remove and return front. O(1)."""
        return self._d.popleft()

    def is_palindrome(self):
        """
        True iff the current contents are a palindrome. O(n).

        We don't want to destroy the deque, so we iterate over a
        COPY — or equivalently, do two-pointer iteration without
        popping.
        """
        data = list(self._d)
        left, right = 0, len(data) - 1
        while left < right:
            if data[left] != data[right]:
                return False
            left += 1
            right -= 1
        return True

    def __len__(self):
        return len(self._d)

    def __repr__(self):
        return f"PalindromeDeque({list(self._d)})"


# =========================================================================
# Test the Functions
# =========================================================================

if __name__ == "__main__":
    # 1. Basic palindrome check
    print("1. is_palindrome_deque:")
    basic_cases = [
        ("racecar", True),
        ("hello",   False),
        ("",        True),
        ("a",       True),
        ("ab",      False),
        ("aa",      True),
        ("abba",    True),
        ("abcba",   True),
        ("abcde",   False),
        ([1, 2, 3, 2, 1], True),                   # works on lists too
        ([1, 2, 3],        False),
    ]
    for s, expected in basic_cases:
        got = is_palindrome_deque(s)
        assert got == expected
        print(f"   {s!r:20}  →  {got}")
    print()

    # 2. Normalized (LC #125 semantics)
    print("2. is_palindrome_normalized (LC #125):")
    norm_cases = [
        ("A man, a plan, a canal: Panama",  True),
        ("race a car",                       False),
        ("",                                 True),
        (".,",                               True),        # all non-alnum → empty → True
        ("No 'x' in Nixon",                  True),
        ("0P",                               False),       # '0' != 'p'
    ]
    for s, expected in norm_cases:
        got = is_palindrome_normalized(s)
        assert got == expected
        print(f"   {s!r:35}  →  {got}")
    print()

    # 3. PalindromeDeque — streaming
    print("3. PalindromeDeque (streaming):")
    pd = PalindromeDeque()
    assert pd.is_palindrome()                    # empty is a palindrome

    for ch, still_pal in [("a", True), ("b", False), ("a", True)]:
        pd.append(ch)
        assert pd.is_palindrome() is still_pal
        print(f"   append({ch!r})   → {pd}    palindrome? {pd.is_palindrome()}")

    # Pop from the back: "aba" → "ab"  (not a palindrome)
    popped = pd.pop()
    assert popped == "a"
    assert pd.is_palindrome() is False
    print(f"   pop → {popped!r}   → {pd}    palindrome? {pd.is_palindrome()}")

    # Back to empty
    pd.pop()
    pd.pop()
    assert pd.is_palindrome() is True

    # Build "racecar" via appendleft (fun because we're going backward)
    pd = PalindromeDeque()
    for ch in "racecar":
        pd.append(ch)
    assert pd.is_palindrome()
    print(f"\n   built 'racecar' via append only: palindrome? {pd.is_palindrome()}")

    # Build "racecar" via appendleft (prepending each char gives reversed string)
    pd = PalindromeDeque()
    for ch in "racecar":
        pd.appendleft(ch)
    # Still "racecar" because racecar == reverse(racecar)
    assert pd.is_palindrome()
    assert list(pd._d) == list(reversed("racecar"))
    print(f"   built 'racecar' via appendleft only: palindrome? {pd.is_palindrome()}")
    print()

    # Stress test — compare against the string-reverse reference
    import random
    random.seed(42)
    for _ in range(300):
        length = random.randint(0, 30)
        s = "".join(random.choice("ab") for _ in range(length))
        assert is_palindrome_deque(s) == (s == s[::-1])

    print("Stress test: 300 random strings — deque approach matches reverse comparison")

    print("\nAll tests passed!")

    # ---------------------------------------------------------------
    # Deque vs Two Pointers — Same Algorithm, Different Code Style:
    #
    #   The two-pointer palindrome walk IS a deque algorithm:
    #
    #     # two-pointer:
    #     while left < right:
    #         if s[left] != s[right]: return False
    #         left += 1; right -= 1
    #
    #     # deque:
    #     while len(d) > 1:
    #         if d.popleft() != d.pop(): return False
    #
    #   The deque framing makes the "take from both ends" intent
    #   explicit. When you need to also MUTATE the sequence during
    #   the check (add/remove characters mid-stream), the deque
    #   version is the natural data structure.
    # ---------------------------------------------------------------
