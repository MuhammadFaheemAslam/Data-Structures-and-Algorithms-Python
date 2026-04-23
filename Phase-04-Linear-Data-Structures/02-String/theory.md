# String — Theory

## Introduction

In Python, a **string is a specialized, immutable array of Unicode
characters**. From a data-structure point of view, there's one giant
thing to understand up front:

> ***Strings are immutable.*** Every operation that "modifies" a
> string actually creates a NEW string.

This single fact drives 90% of the performance and idiom differences
between strings and lists. You can do everything you'd do with a list
of characters — but with different costs, different APIs, and a few
specific traps.

---

## What's a String, Really?

### In Most Languages

A string is a sequence of bytes or characters, laid out contiguously
in memory. In C it's literally `char*`. In Java and C#, strings are
objects wrapping a `char[]` array. In Rust, `String` is a heap-allocated
`Vec<u8>` of UTF-8 bytes.

### In Python

Python strings are **arrays of Unicode code points** (not bytes).
Starting with Python 3.3 (PEP 393), they use a flexible internal
representation:

- ASCII strings → 1 byte per character.
- BMP strings (Unicode ≤ U+FFFF) → 2 bytes per character.
- Non-BMP strings (emoji, rare scripts) → 4 bytes per character.

You mostly don't care — `len(s)` gives character count, `s[i]` gives
a character, and everything "just works." But it's worth knowing that
`s[i]` is **always O(1)** in Python (unlike, say, Rust's `chars().nth(i)`
which is O(n) because it walks UTF-8 bytes).

### Bytes vs String

- `str`: a sequence of Unicode characters.
- `bytes`: a sequence of raw 8-bit values.

They're different types; you convert between them with `.encode()` /
`.decode()`. In this module we focus on `str`.

---

## Immutability — The Big Thing

```python
s = "hello"
s[0] = "H"                      # TypeError: 'str' object doesn't support item assignment
```

To "change" a character, you build a new string:

```python
s = "H" + s[1:]                 # "Hello"
```

Every operation that looks like it mutates actually allocates:

| Operation              | Result                                      |
|------------------------|---------------------------------------------|
| `s + "x"`              | New string (O(n))                           |
| `s.replace(a, b)`      | New string (O(n))                           |
| `s.upper()`            | New string (O(n))                           |
| `s[::-1]`              | New string (O(n))                           |
| `s.strip()`            | New string (O(n))                           |

This is mostly a non-issue — until you find yourself doing it in a
loop. See **string-builder.py** for the classic concatenation trap.

---

## Time Complexity (The Table to Memorize)

Let n = len(s), m = len(other).

| Operation                         | Complexity              |
|-----------------------------------|-------------------------|
| Index `s[i]`                      | O(1)                    |
| Length `len(s)`                   | O(1)                    |
| Slice `s[i:j]`                    | O(k) where k = j − i    |
| Concatenation `s + t`             | **O(n + m)**            |
| Repetition `s * k`                | O(n · k)                |
| Equality `s == t`                 | O(min(n, m))            |
| Membership `sub in s`             | O(n · m) worst case     |
| `s.find(sub)` / `s.index(sub)`    | O(n · m) worst case     |
| `s.count(sub)`                    | O(n · m)                |
| `s.startswith(prefix)`            | O(len(prefix))          |
| `s.endswith(suffix)`              | O(len(suffix))          |
| `s.lower()` / `s.upper()`         | O(n)                    |
| `s.strip()`, `s.lstrip()`, `s.rstrip()` | O(n)              |
| `s.replace(a, b)`                 | O(n · len(a))           |
| `s.split(delim)`                  | O(n)                    |
| `"".join(list_of_strings)`        | O(total length)         |
| `s[::-1]` (reverse)               | O(n)                    |

**Two points worth calling out:**

1. **`sub in s` is O(n · m) worst case**, not O(n). Python uses a
   Boyer-Moore-like algorithm that's usually fast, but the worst
   case is the naive-match bound. For pattern matching, this is
   plenty fast in practice — don't reach for KMP unless you're
   doing thousands of searches.

2. **Concatenation is O(n + m).** Python allocates a new string of
   length `n + m` and copies both in. This is the basis of the
   "concat in a loop is O(n²)" antipattern.

---

## The Concatenation Trap

The single most important string-performance lesson in Python:

### ❌ Antipattern — Quadratic

```python
result = ""
for s in list_of_strings:
    result += s              # each + copies the full `result` — O(n²) total
```

For a list of n strings each of length k, this is O(n² · k) work.
On 100,000 strings, this can take *minutes* when it should take
milliseconds.

### ✅ Correct — Linear

```python
result = "".join(list_of_strings)      # O(total length)
```

`str.join` knows the total length up front, allocates once, and
copies each source string exactly once. O(n · k) total.

The rule of thumb: **never use `+=` on a string in a loop.** Collect
into a list first, then `"".join()`. See `string-builder.py` for a
timing demo that makes the difference concrete.

---

## Common Patterns (That We'll See in Problems)

### 1. Two-Pointer Palindrome Check

```python
left, right = 0, len(s) - 1
while left < right:
    if s[left] != s[right]: return False
    left += 1; right -= 1
return True
```

O(n) time, O(1) space. Variants add case-insensitivity, skip non-alphanumeric
characters, or allow at-most-k differences.

### 2. Anagram via Multiset Comparison

```python
from collections import Counter
return Counter(s) == Counter(t)
```

Two strings are anagrams iff their character counts match. For
fixed alphabets (lowercase a–z), an array-of-26 is even faster.

### 3. Parenthesis Matching via Stack

```python
stack = []
pairs = {")": "(", "]": "[", "}": "{"}
for ch in s:
    if ch in "([{":
        stack.append(ch)
    else:
        if not stack or stack[-1] != pairs[ch]:
            return False
        stack.pop()
return not stack
```

O(n) time, O(n) space. Any "balanced bracket" problem reduces to this.

### 4. Sliding Window on Characters

Covered in Phase-02 / 02 / 02-Sliding-Window. "Longest substring
without repeating characters", "minimum window substring", and
similar are pure sliding-window plus a character counter.

### 5. Frequency Counting

Covered in Phase-02 / 02 / 08-Frequency-Counting. Valid Anagram,
First Unique Character, Find All Anagrams in a String — all are
character-count comparisons.

---

## String-Specific Python Details

### Slicing

```python
s = "hello"
s[1:4]        # "ell"
s[::-1]       # "olleh"
s[::2]        # "hlo" — every 2nd character
s[-3:]        # "llo" — last 3
```

All slicing creates a NEW string — O(k) where k = slice length.

### Iteration

```python
for ch in s: ...                          # iterates characters
for i, ch in enumerate(s): ...             # with indices
```

Each `ch` is a one-character string (no `char` type).

### Membership

```python
"ell" in "hello"                           # True — substring match
"x" in "hello"                             # False
```

Substring match, not character match (though the two are the same
for length-1 substrings).

### Comparison

```python
"apple" < "banana"                         # True — lexicographic
"Apple" < "apple"                          # True — uppercase < lowercase (ASCII 65 < 97)
```

Strings compare lexicographically by Unicode code point. Beware:
"Z" < "a" in ASCII but "Z" > "a" in case-insensitive sort.

### Formatting (f-strings)

```python
name = "alice"
age = 30
f"{name} is {age}"                         # "alice is 30"
f"{age:05d}"                               # "00030"
f"{3.14159:.2f}"                           # "3.14"
```

f-strings (Python 3.6+) are the preferred formatting approach.
Fast, readable, arbitrary expressions.

---

## When to Reach for a List Instead

Because strings are immutable, some problems are much easier if you
convert to a list first:

```python
chars = list(s)                            # O(n) — now mutable
chars[0] = "H"                             # O(1)
result = "".join(chars)                    # O(n)
```

Use when you need:
- **In-place character swaps** (e.g., reverse, rotate, sort).
- **Many "mutations"** in a loop.
- **Shuffling or partitioning**.

Net cost: two O(n) conversions for the ability to do O(1) per edit.
Beats O(n) per edit if you're doing more than a handful.

---

## A Quick Word on Unicode

Strings are code points, not bytes. That matters in a few places:

- `len("é")` is 1 (one code point), but `len("é".encode("utf-8"))` is 2 (two bytes).
- Some characters are COMBINING characters: `"é"` could be one code point
  (U+00E9) or two code points (e + combining acute U+0301). Normalize
  with `unicodedata.normalize("NFC", s)` if this matters.
- Emoji with modifiers ("👨‍🦳" = "man" + ZWJ + "white hair") span multiple
  code points. `len("👨‍🦳")` returns 3 even though it renders as one glyph.
  Use the `grapheme` library if you need to count "perceived characters."

For most algorithmic work (ASCII, simple Unicode), none of this
matters. It bites you when you process real-world human text.

---

## Key Takeaways

1. **Strings are immutable.** Every "modification" creates a new string.
2. **Index and length are O(1).** Python stores width-per-char, so no walking.
3. **Never use `+=` in a loop.** Collect into a list, then `"".join()`.
   This is the #1 string-performance bug in real Python code.
4. **For in-place edits, convert to `list(s)` first.** Two O(n)
   conversions beat doing O(n) on every edit.
5. **Membership / search is O(n · m) worst case** — use `in`
   liberally for readability; reach for specialized algorithms
   (KMP, Rabin-Karp) only when you're doing many searches against
   the same text.
6. **Two pointers, sliding window, frequency counting, and stack-
   based matching** are the four techniques that solve most string
   problems. Covered in depth in Phase 02.

For Python's string methods with their Big-O, see
[`string-methods.py`](string-methods.py). For efficient string
building, see [`string-builder.py`](string-builder.py). For
practice problems, see [`problems/`](problems/).
