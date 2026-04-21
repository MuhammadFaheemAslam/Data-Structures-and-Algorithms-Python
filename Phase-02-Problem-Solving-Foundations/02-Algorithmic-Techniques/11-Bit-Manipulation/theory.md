# Bit Manipulation — Theory

## Introduction

**Bit Manipulation** is not really a technique — it's a *vocabulary*.
A small set of operators and idioms that together let you work with
integers as compact containers of bits, not as numeric values.

Where hashing says "replace a search with a lookup", bit manipulation
says:

> *"Treat this number as 32 (or 64) parallel yes/no questions. Answer
> all of them at once with a single machine instruction."*

When it applies, bit manipulation is absurdly fast — every operation
is a single CPU op. The catch is that it applies to a specific kind
of problem: ones where the state is naturally a **small set of binary
flags**, often representing "is element k included in this subset?"
or "is property k present in this number?"

Key use cases:
- **Subset enumeration** — every integer 0..2^n−1 is a bitmask encoding
  a subset.
- **Parity** — XOR is the "sum mod 2" operator and cancels pairs.
- **Set operations on small universes** — union, intersection,
  difference on sets of at most ~30 elements.
- **Power-of-two checks**, **popcount**, bit hacks.

The entire toolkit fits on one page, and every operator has a mental
picture — when you see `n & (n-1)` you should immediately think
"clear the lowest set bit", not parse it character by character.

---

## The Six Core Operators

| Operator | Name     | Effect on each bit position                     |
|----------|----------|-------------------------------------------------|
| `&`      | AND      | 1 iff both bits are 1                           |
| `\|`     | OR       | 1 iff either bit is 1                           |
| `^`      | XOR      | 1 iff the bits differ                           |
| `~`      | NOT      | flip every bit                                  |
| `<<`     | shift left  | append zeros on the right (multiply by 2^k)   |
| `>>`     | shift right | drop bits from the right (floor-divide by 2^k)|

That's it. Six operators, each O(1). Everything else is *patterns*
built from them.

---

## Single-Bit Operations (Memorize These)

For a given integer `n` and bit position `k` (0-indexed, LSB is 0):

```python
# Check:    is bit k of n set?
(n >> k) & 1                  # returns 0 or 1
n & (1 << k)                  # returns 0 or a nonzero value

# Set:      turn bit k on
n | (1 << k)

# Clear:    turn bit k off
n & ~(1 << k)

# Toggle:   flip bit k
n ^ (1 << k)
```

These four operations, used together, cover 90% of bit-manipulation
problems. Learn them as a unit.

---

## Useful Idioms

These are the "you should recognize these without thinking" patterns:

### Clear the lowest set bit
```python
n & (n - 1)
```
Subtracting 1 flips the lowest set bit to 0 and all bits below it to 1.
ANDing with `n` keeps only the bits above — i.e., drops the lowest 1.

Used in: popcount, power-of-two check, Brian Kernighan's algorithm.

### Isolate the lowest set bit
```python
n & -n
```
In two's complement, `-n == ~n + 1`. ANDing with `n` keeps exactly the
lowest set bit. This is the "lowest 1" as a value, not a position.

Used in: Fenwick trees, finding first set bit.

### Is n a power of two?
```python
n > 0 and (n & (n - 1)) == 0
```
A power of two has exactly one bit set; dropping it leaves zero.

### Count set bits (popcount)
```python
count = 0
while n:
    n &= n - 1            # clear the lowest set bit
    count += 1
```
Brian Kernighan's algorithm — O(# of set bits) rather than O(bit length).

In Python 3.10+ this is built in: `n.bit_count()`. For older Pythons,
`bin(n).count("1")` is the canonical one-liner.

### Toggle case of an ASCII letter
```python
ch = chr(ord(ch) ^ 32)    # 'a' <-> 'A', 'b' <-> 'B', ...
```
Bit 5 differs between ASCII upper and lower case.

### Swap two ints without a temp
```python
a, b = a ^ b, a ^ b ^ (a ^ b) = a ^ b, a  # but tuple swap is simpler in Python
```
An old-school party trick. Python's `a, b = b, a` is cleaner.

---

## XOR — The Magical Operator

XOR is the operator that punches above its weight. Key properties:

```
a ^ a = 0                 # self-inverse — CANCELS pairs
a ^ 0 = a                 # identity
a ^ b = b ^ a             # commutative
a ^ (b ^ c) = (a ^ b) ^ c # associative
```

Because XOR cancels pairs and doesn't care about order, it's the right
tool when:

- **Every element except one appears an even number of times.** XOR
  everything; pairs cancel; survivor is the answer. (See Single Number,
  LC #136 — one of the prettiest algorithms in the canon.)
- **You need prefix XOR for range queries.** Just like prefix sum, but
  with XOR. `prefix[j+1] ^ prefix[i]` is the XOR of `arr[i..j]`.
- **Finding the missing number in 0..n.** XOR all numbers and all
  indices; the missing one survives.

---

## Bitmasks for Sets

The single most important application of bit manipulation in algorithms:

> *An integer's bits encode a subset of a universe of up to ~30 elements.*

Given a universe `U = {0, 1, ..., n-1}`, a subset `S ⊆ U` maps to an
integer `mask` where:

```
bit k of mask is set  <->  element k is in S
```

With this encoding, **set operations become bitwise operations**:

| Set operation      | Bitmask equivalent |
|--------------------|---------------------|
| `A ∪ B`            | `A \| B`            |
| `A ∩ B`            | `A & B`             |
| `A \ B` (difference)| `A & ~B`           |
| `A △ B` (symmetric diff)| `A ^ B`        |
| `k ∈ A`            | `(A >> k) & 1`      |
| empty set          | `0`                 |
| full universe      | `(1 << n) - 1`      |

This makes bitmask DP extremely fast — the state is a single int, and
transitions are O(1).

### Enumerating All Subsets

```python
for mask in range(1 << n):    # 0, 1, 2, ..., 2^n - 1
    ...
```

Each iteration's mask encodes one of the 2^n subsets.

### Iterating Over Set Bits

```python
mask = 0b10110101
while mask:
    low = mask & -mask            # the lowest set bit (as a value)
    mask ^= low                   # clear it
    k = low.bit_length() - 1       # position of that bit
    ...
```

### Enumerating Sub-Masks of a Mask

A specific trick for bitmask DP — iterate over all non-empty subsets of
a given mask:

```python
sub = mask
while sub:
    ...            # sub is a non-empty subset of mask
    sub = (sub - 1) & mask
```

For a mask with k set bits, this iterates over all 2^k subsets in O(2^k)
time. Crucial for problems like "partition into subsets" DP.

---

## When to Reach for Bit Manipulation

Strong signals:

1. **Subsets of small sets (n ≤ ~30).** Any "for each subset" enumeration
   is better done via bitmasks than via itertools.
2. **Parity / "appears twice except once"** problems. XOR is king.
3. **Set operations on small universes.** Union / intersection / etc.
   become single bitwise ops.
4. **Bitmask DP** — when the state naturally includes "which items have
   been selected".
5. **Low-level operations** — single/double/toggle bit, popcount,
   isolate lowest set, clear lowest set, etc.

Weak signals:

6. **Hashing alternatives** — sometimes a small bitmask is a better hash
   key than a tuple or frozenset.
7. **Symmetry problems** (toggle, complement).

---

## When NOT to Use Bit Manipulation

- **n > ~30.** 2^n is too big to iterate over or fit in an int's bits.
- **The elements you're "selecting" aren't numbered** (strings, objects).
  Bitmasks work on integer indices.
- **Python-level performance is fine.** The assembly-level speed of bit
  ops is less visible in Python than in C++. In Python, clarity often
  beats cleverness.
- **You want to impress, not communicate.** Clever bit hacks can make
  code unreadable. The `n & (n-1)` popcount trick is idiomatic; a
  20-line sequence of shifts masquerading as a bitwise lookup table
  usually isn't.

---

## Python-Specific Notes

1. **Python ints are arbitrary-precision.** You don't need to worry
   about overflow, but that means `~n` returns `-(n+1)` rather than a
   fixed-width complement. For fixed-width behaviour, AND with a mask:
   `(~n) & 0xFFFFFFFF`.

2. **Negative numbers use an infinite-precision two's complement.**
   Right-shifting a negative number is arithmetic (fills with 1s).
   Usually fine; occasionally surprising.

3. **Built-in helpers:**
   - `bin(n)` — string representation.
   - `n.bit_length()` — number of bits to represent n (0 for n=0).
   - `n.bit_count()` (Python 3.10+) — popcount.

4. **`int.from_bytes` / `int.to_bytes`** — for converting bit patterns
   to and from byte strings, useful for bit-level I/O.

---

## Bit Manipulation vs Related Techniques

| Technique              | Use when…                                       |
|------------------------|--------------------------------------------------|
| **Bit Manipulation**   | Set operations on small universes, parity, popcount |
| **Bitmask DP**         | DP state includes "which items selected"        |
| **Hashing**            | General-purpose lookup; alphabet/universe too big |
| **Backtracking**       | Subset/permutation enumeration when structure matters |
| **Monotonic Stack**    | Completely unrelated — different shape entirely |

Bitmask DP is a sub-application of bit manipulation and was touched on
in Phase-02 / 01 / 04-Dynamic-Programming's patterns file. This module
covers the more elementary uses.

---

## Complexity

Every bit-manipulation primitive is **O(1)** — a single CPU
instruction. Algorithms built from them have complexity determined by
the *iteration*, not the ops:

- Enumerating all subsets of n elements: **O(2^n)**.
- Popcount via Kernighan: **O(popcount)** (often much less than O(bit length)).
- Set union / intersection on n-element universe: **O(1)** (fits in one int).

The factor-of-constant speedup over dict/set is real but often
imperceptible in Python. The algorithmic use — "bitmask as subset
representation" — is where bit manipulation wins big.

---

## Pitfalls

- **Operator precedence.** `a & b == c` parses as `a & (b == c)` in
  Python (because `==` binds tighter than `&`). Parenthesize:
  `(a & b) == c`.
- **`1 << k` vs `k << 1`.** The first shifts 1 by k (`2^k`); the second
  shifts k by 1 (`2k`). Mix them up once, fix the bug, never again.
- **Confusing `&` with `and`.** `and` is short-circuit boolean; `&` is
  bitwise on ints. `3 and 5` is 5; `3 & 5` is 1.
- **Off-by-one on full mask.** Full universe of size n is `(1 << n) - 1`,
  not `1 << n`.
- **Using `~` as logical NOT.** `~0` is `-1`, not `1`. For boolean flip,
  use `not`.
- **Signed shift surprises.** `-5 >> 1 == -3` (rounds toward negative
  infinity). Usually fine; occasionally surprising.

---

## Key Takeaways

1. **Six operators, four single-bit operations, a handful of idioms.**
   That's the whole vocabulary.
2. **XOR cancels pairs.** That single property solves a half-dozen
   classic problems.
3. **Bitmasks represent subsets of small universes.** Set operations
   become single bitwise ops.
4. **`n & (n-1)` and `n & -n`** are the two most important idioms —
   "clear lowest set bit" and "isolate lowest set bit".
5. **Enumeration via `for mask in range(1 << n)`** is the fastest way
   to iterate over all subsets when n ≤ ~25.

For concrete bit-op references, see [`bit-operations.py`](bit-operations.py).
For worked problems that showcase XOR magic, bitmask enumeration, and
power-of-two detection, see [`problems/`](problems/).
