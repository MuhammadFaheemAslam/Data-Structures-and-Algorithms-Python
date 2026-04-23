"""
string-builder.py – Efficient String Concatenation in Python

The single most important string performance lesson in Python:

    ❌ NEVER use `+=` on a string in a loop.
    ✅ Accumulate into a list, then call `"".join(...)`.

This file demonstrates the difference with measured timings on large
inputs. For 100_000 appends, the naive `+=` approach can take several
seconds; the idiomatic `.join()` approach takes milliseconds.

---------------------------------------------------
The Four Builder Patterns:

    1. BAD:   `result += s` in a loop                    → O(n²)
    2. OK:    `"".join(list_of_strings)`                 → O(n)
    3. OK:    `io.StringIO` with `.write()` + `.getvalue()` → O(n)
    4. OK:    `list.append(s)` then `"".join(list)`      → O(n)

(2), (3), (4) are all linear. Pick whichever fits your style.

---------------------------------------------------
Why `+=` Is Quadratic:

Each `result += s` operation:
    1. Allocates a new string of size len(result) + len(s).
    2. Copies the ENTIRE current `result` into the new buffer.
    3. Copies `s` after it.

Over n appends of average length k:
    1st:  copy 0 + k     = k
    2nd:  copy k + k     = 2k
    3rd:  copy 2k + k    = 3k
    ...
    nth:  copy (n-1)k + k = nk

Total: k + 2k + 3k + ... + nk = k · n(n+1)/2 = O(n² · k)

---------------------------------------------------
Minor Caveat — CPython's "Interned String Optimization":

Starting in CPython 2.4, the `+=` pattern has a special optimization:
if the current string has a reference count of 1 (nobody else uses
it), CPython will resize it IN PLACE instead of allocating a new one.
When the optimization kicks in, `+=` becomes amortized O(1).

BUT:
    - The optimization is CPython-specific. PyPy, Jython, and IronPython
      don't do it. Relying on it makes your code non-portable.
    - It breaks in subtle ways if the string is assigned to multiple
      variables, passed to a function, or otherwise referenced elsewhere.
    - `.join()` is clearer and always O(n). Just use it.

Never rely on the interned-string trick. Use `.join()`.
"""

import io
import time


# =========================================================================
# The Four Patterns
# =========================================================================

def build_via_plus_equals(parts):
    """
    ❌ ANTIPATTERN: += in a loop.

    Time:  O(n²) in general (O(n) if CPython's interned-string opt kicks in)
    Space: O(n²) in allocations if the optimization misses
    """
    result = ""
    for s in parts:
        result += s
    return result


def build_via_join(parts):
    """
    ✅ The idiomatic answer.

    Time:  O(total length)
    Space: O(total length) — one allocation
    """
    return "".join(parts)


def build_via_stringio(parts):
    """
    ✅ StringIO — Python's "string builder."

    Time:  O(total length)
    Space: O(total length)

    Useful when:
        - You're generating output from many sources.
        - You want a file-like interface (so you can pass it to
          functions that `write` to it).
        - You need intermediate flushes (rare for strings).

    Slightly more overhead than join() for simple cases.
    """
    buf = io.StringIO()
    for s in parts:
        buf.write(s)
    return buf.getvalue()


def build_via_list_then_join(parts):
    """
    ✅ Alternative to join: accumulate into a list, then join once.

    Time:  O(total length)
    Space: O(total length)

    Useful when:
        - The string pieces are generated CONDITIONALLY — you can
          `if x: chunks.append(...)` and only include what you need.
        - You're building up from many different sources.
    """
    chunks = []
    for s in parts:
        chunks.append(s)
    return "".join(chunks)


# =========================================================================
# Timing Demonstration
# =========================================================================

def run_timings(n, avg_len):
    """
    Build a string of n pieces, each ~avg_len characters long.
    Time each of the four patterns.
    """
    # Generate test input
    parts = ["x" * avg_len for _ in range(n)]

    print(f"\nTiming with n={n} pieces, avg_len={avg_len}:")

    # 1. Plus-equals
    t0 = time.time()
    r1 = build_via_plus_equals(parts)
    t_pe = time.time() - t0

    # 2. Join
    t0 = time.time()
    r2 = build_via_join(parts)
    t_join = time.time() - t0

    # 3. StringIO
    t0 = time.time()
    r3 = build_via_stringio(parts)
    t_sio = time.time() - t0

    # 4. List + join
    t0 = time.time()
    r4 = build_via_list_then_join(parts)
    t_list = time.time() - t0

    # All four should produce identical output
    assert r1 == r2 == r3 == r4

    print(f"   +=         : {t_pe:.4f}s")
    print(f"   join       : {t_join:.4f}s")
    print(f"   StringIO   : {t_sio:.4f}s")
    print(f"   list+join  : {t_list:.4f}s")

    # Warn if += is dramatically slower than join — that's the teaching moment
    if t_pe > t_join * 10:
        print(f"\n   += is {t_pe / t_join:.0f}× slower than join!  (quadratic trap)")
    else:
        print(f"\n   += performance: {t_pe / t_join:.1f}× join")
        print("   (CPython's interned-string optimization is helping; "
              "don't rely on it — other interpreters may not optimize.)")


# =========================================================================
# Practical Examples
# =========================================================================

def example_conditional_build():
    """
    Pattern: building a query string from optional pieces.

    Using list + join makes this cleaner than messing with += and
    trailing separators.
    """
    def build_query(name=None, age=None, city=None):
        parts = []
        if name is not None:
            parts.append(f"name={name}")
        if age is not None:
            parts.append(f"age={age}")
        if city is not None:
            parts.append(f"city={city}")
        return "&".join(parts)                    # idiomatic

    assert build_query(name="alice") == "name=alice"
    assert build_query(name="alice", age=30) == "name=alice&age=30"
    assert build_query(age=30, city="nyc") == "age=30&city=nyc"
    assert build_query() == ""

    print("\nexample_conditional_build: passed")


def example_streaming_build():
    """
    Pattern: converting binary data to hex via streaming.

    StringIO or list+join both work. Here we use list+join.
    """
    data = bytes([0x48, 0x65, 0x6c, 0x6c, 0x6f])  # "Hello" in ASCII

    chunks = []
    for byte in data:
        chunks.append(f"{byte:02X}")
    hex_string = " ".join(chunks)

    assert hex_string == "48 65 6C 6C 6F"
    print("example_streaming_build: passed")


def example_csv_row():
    """
    Building a CSV row — classic join use case.
    """
    row = ["alice", "30", "NYC", "engineer"]
    csv_line = ",".join(row)
    assert csv_line == "alice,30,NYC,engineer"
    print("example_csv_row: passed")


# =========================================================================
# Run the Demonstration
# =========================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("The Four String-Builder Patterns — Timing Comparison")
    print("=" * 60)

    # Small n: difference may be invisible
    run_timings(1_000, 20)

    # Medium n: differences start to show
    run_timings(10_000, 20)

    # Large n: the `+=` version is now visibly slower (if the
    # optimization isn't kicking in, dramatically so)
    run_timings(50_000, 20)

    print()
    print("=" * 60)
    print("Practical Examples")
    print("=" * 60)
    example_conditional_build()
    example_streaming_build()
    example_csv_row()

    print("\nAll tests passed!")

    # ---------------------------------------------------------------
    # Production Rule of Thumb:
    #
    #   Collect strings into a LIST. Join at the end with "".join().
    #
    #   Do this even if your "loop" is only 10 iterations. It's:
    #     - Always O(n), regardless of implementation quirks
    #     - Clearer than += (you're explicitly accumulating)
    #     - Zero cost vs += when the list is small
    #
    # This single habit prevents the #1 string-performance bug in
    # real-world Python code.
    # ---------------------------------------------------------------
