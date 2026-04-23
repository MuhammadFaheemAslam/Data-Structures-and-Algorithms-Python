"""
string-methods.py – Python String Methods with Big-O Annotations

A runnable reference to the most commonly-used string methods, with
their complexity and practical notes. Run this file to see each
method in action.

Organized into seven categories:

    1. Inspection and testing
    2. Case manipulation
    3. Trimming and padding
    4. Searching
    5. Splitting and joining
    6. Replacing and translating
    7. Iteration / slicing patterns

This is the CHEAT SHEET version of what Python gives you for free.
Use it as a lookup while solving problems.
"""

# =========================================================================
# 1. Inspection and Testing — All O(n)
# =========================================================================

def demo_inspection():
    print("=" * 60)
    print("1. Inspection and Testing")
    print("=" * 60)
    s = "Hello, World! 42"

    print(f"   s = {s!r}")
    print(f"   len(s)              = {len(s)}")                    # O(1)
    print(f"   s.isalpha()         = {s.isalpha()}")                 # O(n) — all letters?
    print(f"   s.isdigit()         = {s.isdigit()}")                 # all digits?
    print(f"   s.isalnum()         = {s.isalnum()}")                 # letters OR digits
    print(f"   s.isspace()         = {s.isspace()}")                 # all whitespace
    print(f"   s.isupper()         = {s.isupper()}")                 # all uppercase letters are uppercase
    print(f"   s.islower()         = {s.islower()}")
    print(f"   s.istitle()         = {s.istitle()}")                 # Title Case?
    print(f"   'abc'.isalpha()     = {'abc'.isalpha()}")
    print(f"   '123'.isdigit()     = {'123'.isdigit()}")
    print()


# =========================================================================
# 2. Case Manipulation — All O(n), All Return New Strings
# =========================================================================

def demo_case():
    print("=" * 60)
    print("2. Case Manipulation")
    print("=" * 60)
    s = "Hello, World!"
    print(f"   s = {s!r}")
    print(f"   s.upper()           = {s.upper()!r}")
    print(f"   s.lower()           = {s.lower()!r}")
    print(f"   s.title()           = {s.title()!r}")
    print(f"   s.capitalize()      = {s.capitalize()!r}")
    print(f"   s.swapcase()        = {s.swapcase()!r}")
    print(f"   s.casefold()        = {'WEISS'.casefold()!r}"
          f"   (stronger than lower() for Unicode)")
    print()


# =========================================================================
# 3. Trimming and Padding
# =========================================================================

def demo_trim_pad():
    print("=" * 60)
    print("3. Trimming and Padding")
    print("=" * 60)
    s = "   hello   "
    print(f"   s = {s!r}")
    print(f"   s.strip()           = {s.strip()!r}")                # O(n)
    print(f"   s.lstrip()          = {s.lstrip()!r}")
    print(f"   s.rstrip()          = {s.rstrip()!r}")
    print(f"   'xxhelloxx'.strip('x') = {'xxhelloxx'.strip('x')!r}")

    t = "hi"
    print(f"\n   t = {t!r}")
    print(f"   t.ljust(10, '.')    = {t.ljust(10, '.')!r}")          # O(width)
    print(f"   t.rjust(10, '.')    = {t.rjust(10, '.')!r}")
    print(f"   t.center(10, '.')   = {t.center(10, '.')!r}")
    print(f"   t.zfill(5)          = {t.zfill(5)!r}                (pad with zeros)")
    print()


# =========================================================================
# 4. Searching — O(n · m) Worst Case, Fast in Practice
# =========================================================================

def demo_search():
    print("=" * 60)
    print("4. Searching")
    print("=" * 60)
    s = "The quick brown fox jumps over the lazy dog"
    print(f"   s = {s!r}")

    # Membership (substring)
    print(f"   'fox' in s             = {'fox' in s}")              # O(n · m)
    print(f"   'cat' in s             = {'cat' in s}")

    # find returns -1 if not found; index raises ValueError
    print(f"   s.find('fox')          = {s.find('fox')}")            # O(n · m)
    print(f"   s.find('cat')          = {s.find('cat')}")            # -1

    # count — always scans the whole string
    print(f"   s.count('o')           = {s.count('o')}")            # O(n · m)
    print(f"   s.count('the', 0, len(s)) with startswith-style range = "
          f"{s.lower().count('the')}")

    # Prefix / suffix
    print(f"   s.startswith('The')    = {s.startswith('The')}")     # O(len(prefix))
    print(f"   s.endswith('dog')      = {s.endswith('dog')}")
    print(f"   s.startswith(('The', 'A'))  = {s.startswith(('The', 'A'))}   "
          "(tuple of candidates)")
    print()


# =========================================================================
# 5. Splitting and Joining — O(n) in Total Length
# =========================================================================

def demo_split_join():
    print("=" * 60)
    print("5. Splitting and Joining")
    print("=" * 60)
    csv = "alice,bob,charlie,dan"
    print(f"   csv = {csv!r}")
    print(f"   csv.split(',')      = {csv.split(',')}")             # O(n)
    print(f"   csv.split(',', 2)   = {csv.split(',', 2)}")            # at most 2 splits
    print(f"   csv.rsplit(',', 1)  = {csv.rsplit(',', 1)}")           # from the right

    text = "line one\nline two\nline three"
    print(f"\n   text.splitlines()   = {text.splitlines()}")          # handles \n, \r, \r\n

    parts = ["alice", "bob", "charlie"]
    print(f"\n   parts = {parts}")
    print(f"   ', '.join(parts)    = {', '.join(parts)!r}")         # O(total length)
    print(f"   ''.join(['a', 'b']) = {''.join(['a', 'b'])!r}       (no separator)")

    # partition returns (before, sep, after)
    print(f"\n   'key=value'.partition('=') = {'key=value'.partition('=')}")
    print()


# =========================================================================
# 6. Replacing and Translating
# =========================================================================

def demo_replace():
    print("=" * 60)
    print("6. Replacing and Translating")
    print("=" * 60)
    s = "the cat and the dog"
    print(f"   s = {s!r}")
    print(f"   s.replace('the', 'a')       = {s.replace('the', 'a')!r}")   # O(n · len(old))
    print(f"   s.replace('the', 'a', 1)    = {s.replace('the', 'a', 1)!r}     (only first)")

    # translate with str.maketrans — O(n), handles multiple mappings at once
    tr = str.maketrans("aeiou", "AEIOU")
    print(f"\n   str.maketrans('aeiou', 'AEIOU') + translate:")
    print(f"   'hello world'.translate(tr) = {'hello world'.translate(tr)!r}")

    # delete characters via translate
    del_digits = str.maketrans("", "", "0123456789")
    print(f"\n   remove all digits:")
    print(f"   'abc123def'.translate(del_digits) = {'abc123def'.translate(del_digits)!r}")
    print()


# =========================================================================
# 7. Iteration / Slicing Patterns — Review
# =========================================================================

def demo_iteration():
    print("=" * 60)
    print("7. Iteration / Slicing")
    print("=" * 60)
    s = "abcdef"

    print(f"   s = {s!r}")
    print(f"   s[0]        = {s[0]!r}        (first)")
    print(f"   s[-1]       = {s[-1]!r}        (last)")
    print(f"   s[1:4]      = {s[1:4]!r}       (slice)")
    print(f"   s[::-1]     = {s[::-1]!r}      (reverse)")
    print(f"   s[::2]      = {s[::2]!r}       (every 2nd)")

    # character-by-character iteration
    print(f"\n   for c in s: print(c, end=',') → ", end="")
    for c in s:
        print(c, end=",")
    print()

    # With indices
    print(f"\n   for i, c in enumerate(s): print(f'{{i}}:{{c}}', end=' ') → ", end="")
    for i, c in enumerate(s):
        print(f"{i}:{c}", end=" ")
    print("\n")


# =========================================================================
# Bonus: String Multiplication, f-strings, ord / chr
# =========================================================================

def demo_bonus():
    print("=" * 60)
    print("Bonus")
    print("=" * 60)
    # Multiplication
    print(f"   '-' * 20            = {'-' * 20!r}")
    print(f"   'abc' * 3           = {'abc' * 3!r}")

    # f-strings
    name = "alice"
    score = 0.95
    print(f"\n   f'{{name}} — {{score:.1%}}' → {name} — {score:.1%}")
    print(f"   f'{{42:05d}}'       → {42:05d}")
    print(f"   f'{{3.14159:.3f}}' → {3.14159:.3f}")
    print(f"   f'{{42:>10}}'      → '{42:>10}'")                     # right-align width 10

    # ord / chr
    print(f"\n   ord('a')           = {ord('a')}")
    print(f"   chr(65)            = {chr(65)!r}")
    print(f"   chr(ord('a') + 2)  = {chr(ord('a') + 2)!r}")
    print()


# =========================================================================
# Demonstration
# =========================================================================

if __name__ == "__main__":
    demo_inspection()
    demo_case()
    demo_trim_pad()
    demo_search()
    demo_split_join()
    demo_replace()
    demo_iteration()
    demo_bonus()

    # Sanity-check assertions
    assert len("hello") == 5
    assert "hello".upper() == "HELLO"
    assert "  hi  ".strip() == "hi"
    assert "abc".find("b") == 1
    assert "a,b,c".split(",") == ["a", "b", "c"]
    assert "".join(["a", "b"]) == "ab"
    assert "hello".replace("l", "L") == "heLLo"
    assert "hello"[::-1] == "olleh"
    assert ord("a") == 97
    assert chr(65) == "A"

    print("All checks passed!")
