"""
Problem: Stock Span

Difficulty: Medium (GeeksforGeeks classic; LeetCode #901 is the online-streaming variant)

---------------------------------------------------
Problem Statement:

Given an array `prices` representing daily stock prices, return an
array `span` where `span[i]` is the number of consecutive days up
to and including day i on which the price was LESS THAN OR EQUAL
to `prices[i]`.

    prices = [100, 80, 60, 70, 60, 75, 85]
    spans  = [1,   1,  1,  2,  1,  4,  6]

Why 4 at day 5 (price 75)? Because the 4 most recent days (70, 60,
75 — wait, let me re-derive) have prices ≤ 75. Actually:

    day 5 is price 75. Walking back:
        day 5: 75 ≤ 75  ✓  count 1
        day 4: 60 ≤ 75  ✓  count 2
        day 3: 70 ≤ 75  ✓  count 3
        day 2: 60 ≤ 75  ✓  count 4
        day 1: 80 > 75  ✗  stop

    span = 4.

---------------------------------------------------
Why This Is a Monotonic-Stack Problem:

The stock span is effectively "how far back is the PREVIOUS GREATER
element?" (or the start of the array, if none).

    span[i] = i - (index of the last day j < i with prices[j] > prices[i])

If no such day, `span[i] = i + 1` (all days counted).

We can find "previous greater element" for every index in O(n) total
using a monotonic (decreasing) stack — covered in depth in Phase-02 /
02 / 09-Monotonic-Stack.

---------------------------------------------------
The Two Approaches:

    1. Brute force              O(n²)  — scan backward for each day
    2. Monotonic stack          O(n)   — canonical next/previous-greater pattern

The stack approach reuses work: once a price on the stack is surpassed,
we pop it — we'll never need it again (any future day with higher
price than the popper will also surpass the popped day by transitivity).

---------------------------------------------------
"""


# =========================================================================
# Solution 1: Brute Force — O(n²)
# =========================================================================

def stock_span_brute_force(prices):
    """
    For each day, scan backward until a greater price is found.

    Time:  O(n²)
    Space: O(1) beyond output
    """
    n = len(prices)
    span = [1] * n                                # each day at least counts itself
    for i in range(1, n):
        j = i - 1
        while j >= 0 and prices[j] <= prices[i]:
            j -= 1
        span[i] = i - j
    return span


# =========================================================================
# Solution 2: Monotonic Stack — O(n)
# =========================================================================

def stock_span(prices):
    """
    Compute the stock span for each day in O(n) using a monotonic stack.

    The stack holds (price, span) pairs — or equivalently, INDICES of
    days whose price hasn't yet been surpassed.

    Invariant: the stack's price values are strictly DECREASING from
    bottom to top. When a new price comes in that exceeds the top,
    pop — the popped day is "absorbed" into the current day's span.

    Time:  O(n)   amortized — each day is pushed once and popped at most once
    Space: O(n)
    """
    n = len(prices)
    span = [0] * n
    stack = []                                    # (price, span) pairs

    for i, price in enumerate(prices):
        absorbed_span = 1                         # the current day itself
        while stack and stack[-1][0] <= price:
            absorbed_span += stack.pop()[1]
        stack.append((price, absorbed_span))
        span[i] = absorbed_span

    return span


# =========================================================================
# Solution 3: Streaming / Online (LeetCode #901)
# =========================================================================

class StockSpanner:
    """
    LeetCode #901 "Online Stock Span".

    Same algorithm, but exposed as a streaming API: one `next(price)`
    call per day returns the span for that day, without batch
    precomputation.

    Total across all calls: O(n) amortized.
    """

    def __init__(self):
        self._stack = []                          # (price, span) pairs

    def next(self, price):
        span = 1
        while self._stack and self._stack[-1][0] <= price:
            span += self._stack.pop()[1]
        self._stack.append((price, span))
        return span


# =========================================================================
# Test the Solutions
# =========================================================================

if __name__ == "__main__":
    # Canonical example
    prices = [100, 80, 60, 70, 60, 75, 85]
    expected = [1, 1, 1, 2, 1, 4, 6]
    print(f"prices   = {prices}")
    print(f"expected = {expected}")
    print(f"   stock_span_brute_force:  {stock_span_brute_force(prices)}")
    print(f"   stock_span (monotonic):  {stock_span(prices)}")

    # Streaming API
    spanner = StockSpanner()
    streaming_spans = [spanner.next(p) for p in prices]
    print(f"   StockSpanner (streaming): {streaming_spans}")

    assert stock_span_brute_force(prices) == expected
    assert stock_span(prices) == expected
    assert streaming_spans == expected
    print()

    # More test cases
    test_cases = [
        ([100, 80, 60, 70, 60, 75, 85],   [1, 1, 1, 2, 1, 4, 6]),
        ([10, 4, 5, 90, 120, 80],         [1, 1, 2, 4, 5, 1]),
        ([1],                              [1]),
        ([],                               []),
        ([1, 2, 3, 4, 5],                  [1, 2, 3, 4, 5]),         # all rising → accumulating spans
        ([5, 4, 3, 2, 1],                  [1, 1, 1, 1, 1]),         # all falling
        ([5, 5, 5, 5, 5],                  [1, 2, 3, 4, 5]),         # all equal
    ]

    for prices, expected in test_cases:
        assert stock_span(prices) == expected
        assert stock_span_brute_force(prices) == expected

        spanner = StockSpanner()
        assert [spanner.next(p) for p in prices] == expected

        print(f"prices={prices} → spans={expected}")

    # Stress test — monotonic stack vs brute force
    import random
    random.seed(42)
    for _ in range(200):
        n = random.randint(0, 50)
        prices = [random.randint(1, 200) for _ in range(n)]
        assert stock_span(prices) == stock_span_brute_force(prices)

    print("\nStress test: 200 random price arrays — both approaches agree")

    # Timing — monotonic stack should crush brute force at scale
    import time
    n = 10_000
    random.seed(0)
    big = [random.randint(1, 100_000) for _ in range(n)]

    t0 = time.time()
    stock_span(big)
    t_stack = time.time() - t0

    t0 = time.time()
    stock_span_brute_force(big)
    t_brute = time.time() - t0

    print(f"\nTiming on n={n}:")
    print(f"   monotonic stack:  {t_stack:.4f}s")
    print(f"   brute force:      {t_brute:.4f}s")
    print(f"   speedup:          {t_brute / max(t_stack, 1e-6):.0f}×")

    print("\nAll tests passed!")

    # ---------------------------------------------------------------
    # The Monotonic-Stack Family of Problems:
    #
    #   Stock span is one of the cleanest instances of the broader
    #   "next-greater / previous-greater" pattern. Sister problems:
    #
    #     - Next Greater Element (LC #496, #503)
    #     - Daily Temperatures (LC #739)
    #     - Largest Rectangle in Histogram (LC #84)
    #     - Trapping Rain Water (LC #42, two-pointer variant too)
    #
    # All use a monotonic stack to do "for each element, find the
    # nearest greater/smaller element in O(1) amortized." Covered
    # in depth in Phase-02 / 02 / 09-Monotonic-Stack.
    # ---------------------------------------------------------------
