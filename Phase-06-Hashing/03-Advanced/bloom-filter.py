"""
bloom-filter.py — Probabilistic Set Membership

A BLOOM FILTER answers "have I seen this before?" using dramatically
less memory than a HashSet — at the cost of occasional FALSE POSITIVES
(it may say "yes" when the answer is actually "no"). It NEVER gives
false negatives.

---------------------------------------------------
When You'd Use One:

    - A browser's "malicious URL" database (Google Safe Browsing):
      fast local check; only phone home to the server on a HIT.
    - A CDN cache: "is this page possibly cached anywhere?"
    - Database query planners: "could this key exist in this SSTable?"
      Used in Cassandra, LevelDB, RocksDB to skip disk reads.
    - Duplicate-submission checks on high-traffic services.

The pattern is the same in every case:
    1. Cheap check: "is it possibly in the set?"
    2. If the Bloom says NO → definitely not, skip the expensive lookup.
    3. If it says YES → do the expensive lookup (DB, disk, network).

You get the fast-path optimization without having to store the full set.

---------------------------------------------------
How It Works:

State: a BIT ARRAY of size `m`, initially all zeros.
Hashes: `k` independent hash functions, each mapping any element to
        a position in 0..m-1.

add(x):
    for each of the k hash functions:
        set bits[h_i(x)] = 1

contains(x):
    return True iff bits[h_i(x)] == 1 for EVERY i
    (any zero → definitely not present)

That's the entire algorithm. If contains(x) returns True, the element
is PROBABLY present — but it could be a coincidence that all k bits
happen to be set by unrelated adds.

---------------------------------------------------
Sizing & False Positive Rate:

For a bit array of size m, k hash functions, and n inserted elements,
the false-positive rate is approximately:

    p ≈ (1 - e^(-k*n/m))^k

Given a desired rate p and expected n, optimal settings are:

    m = -n * ln(p) / (ln 2)^2
    k = (m / n) * ln 2

For n = 1,000,000 and p = 1%:
    m ≈ 9,585,058 bits ≈ 1.2 MB
    k ≈ 7 hash functions

Compared to a HashSet storing 1M 10-character strings (~16 MB with
overhead), Bloom's 1.2 MB for 1% FP rate is a 10× memory win.

---------------------------------------------------
Caveats:

    • No delete: clearing bits would break other elements that rely
      on the same bits. Workarounds exist (Counting Bloom Filter —
      uses small counters instead of bits).
    • No iteration: you can't list what you've added.
    • Fixed capacity: once n exceeds your sizing, the FP rate blows up.
    • Tuning matters: too few hashes → more FPs; too many → all bits
      end up set, also more FPs.

---------------------------------------------------
Getting k Independent Hashes From Two:

A classical trick (Kirsch & Mitzenmacher, 2006): for k > 2 hash
functions, you don't need k independent hashes — two are enough.
Generate hash i as:

    h_i(x) = (h1(x) + i * h2(x)) mod m

This is how most production Bloom filters are built. We use it below.
"""

import math


class BloomFilter:
    """
    Bloom filter with tunable capacity and target false-positive rate.

    Example:
        bf = BloomFilter(capacity=1_000_000, fp_rate=0.01)
        bf.add("alice@example.com")
        "alice@example.com" in bf   # True (definite)
        "other@example.com" in bf   # usually False; <1% False positive
    """

    def __init__(self, capacity, fp_rate=0.01):
        """
        Configure for `capacity` expected items at ~`fp_rate` false-positive rate.
        """
        if capacity <= 0 or not (0 < fp_rate < 1):
            raise ValueError("capacity must be > 0 and 0 < fp_rate < 1")

        self.capacity = capacity
        self.fp_rate = fp_rate
        self.m = BloomFilter._optimal_m(capacity, fp_rate)          # bit array size
        self.k = BloomFilter._optimal_k(self.m, capacity)           # # hashes
        self._bits = bytearray((self.m + 7) // 8)
        self._count = 0                            # actual # of add() calls

    # ------------------------------------------------------------------
    # Sizing formulas
    # ------------------------------------------------------------------

    @staticmethod
    def _optimal_m(n, p):
        """m = -n ln p / (ln 2)^2"""
        return max(1, int(math.ceil(-n * math.log(p) / (math.log(2) ** 2))))

    @staticmethod
    def _optimal_k(m, n):
        """k = (m / n) * ln 2, rounded to nearest int (at least 1)."""
        return max(1, int(round((m / n) * math.log(2))))

    # ------------------------------------------------------------------
    # Hashing — double-hashing trick
    # ------------------------------------------------------------------

    def _hashes(self, x):
        """
        Produce k hash positions in [0, m) using only two base hashes.

        Kirsch & Mitzenmacher: h_i = (h1 + i * h2) mod m behaves like
        k independent hashes for practical purposes.
        """
        # Use Python's hash() for h1; fnv-style for h2 (independent-ish).
        h1 = hash(x)
        h2 = hash((x, "bloom-salt"))               # different input → different hash

        for i in range(self.k):
            yield (h1 + i * h2) % self.m

    # ------------------------------------------------------------------
    # Core operations
    # ------------------------------------------------------------------

    def add(self, x):
        """Mark `x` as possibly present. Always succeeds."""
        for pos in self._hashes(x):
            self._bits[pos >> 3] |= (1 << (pos & 7))
        self._count += 1

    def __contains__(self, x):
        """
        True iff every bit for x's k hashes is set.

        False → definitely not present.
        True  → probably present (may be a false positive).
        """
        for pos in self._hashes(x):
            if not (self._bits[pos >> 3] & (1 << (pos & 7))):
                return False
        return True

    # ------------------------------------------------------------------
    # Stats / introspection
    # ------------------------------------------------------------------

    def __len__(self):
        """Number of add() calls (NOT distinct elements — the filter can't tell)."""
        return self._count

    def current_fp_rate(self):
        """
        Empirical FP rate given how many bits are currently set.

        If fraction `f` of bits are set, the per-element FP rate is f^k.
        """
        bits_set = sum(bin(b).count("1") for b in self._bits)
        f = bits_set / self.m
        return f ** self.k

    def info(self):
        return {
            "capacity":       self.capacity,
            "fp_rate_target": self.fp_rate,
            "m_bits":         self.m,
            "k_hashes":       self.k,
            "m_bytes":        len(self._bits),
            "count":          self._count,
            "fp_rate_now":    self.current_fp_rate(),
        }


# =========================================================================
# Test
# =========================================================================

if __name__ == "__main__":
    # Basic correctness
    bf = BloomFilter(capacity=1000, fp_rate=0.01)
    print(f"Configured: {bf.info()}")

    # NO FALSE NEGATIVES (the defining property)
    inserted = [f"item-{i}" for i in range(1000)]
    for x in inserted:
        bf.add(x)
    for x in inserted:
        assert x in bf, f"false negative for {x}"

    # Measure false-positive rate on unseen items
    unseen = [f"unseen-{i}" for i in range(10_000)]
    false_positives = sum(1 for x in unseen if x in bf)
    empirical_fp = false_positives / len(unseen)

    print(f"\nInserted 1000 items into a filter sized for capacity 1000.")
    print(f"   configured target FP rate: {bf.fp_rate}")
    print(f"   empirical FP rate on 10000 unseen items: {empirical_fp:.4f}")
    print(f"   current estimated FP rate: {bf.current_fp_rate():.4f}")

    # Should be in the ballpark of the target; allow generous slack
    assert empirical_fp < 0.05, "FP rate uncomfortably high for target 0.01"

    # Edge case: tiny filter
    tiny = BloomFilter(capacity=10, fp_rate=0.1)
    for i in range(10):
        tiny.add(i)
    for i in range(10):
        assert i in tiny

    # Unhashable — should raise
    try:
        bf.add([1, 2, 3])
    except TypeError:
        pass
    else:
        raise AssertionError("expected TypeError on unhashable")

    # Overloading: if you insert WAY more than capacity, FP rate degrades
    overloaded = BloomFilter(capacity=100, fp_rate=0.01)
    for i in range(5000):                          # 50× overload
        overloaded.add(f"overload-{i}")
    # Most bits should now be set — FP rate ~ 1.0
    assert overloaded.current_fp_rate() > 0.5, (
        f"overloaded filter should be saturated, got {overloaded.current_fp_rate():.3f}"
    )

    print("\nOverloaded filter (50× capacity):")
    print(f"   current FP rate: {overloaded.current_fp_rate():.4f}   "
          f"(≈1.0 means 'filter is saturated')")

    print("\nAll tests passed!")

    # ---------------------------------------------------------------
    # Real-World Sizing Quick-Reference:
    #
    #   Target FP rate    bits per element
    #   ---------------   ----------------
    #        10%                4.8
    #         1%                9.6
    #       0.1%               14.4
    #      0.01%               19.2
    #
    # Every 10× reduction in FP rate costs ~5 more bits per element.
    # For most production uses, 1% (9.6 bits/elem ≈ 1.2 bytes) is the
    # sweet spot: orders of magnitude smaller than a HashSet, with a
    # FP rate low enough that the cache-miss penalty is negligible.
    # ---------------------------------------------------------------
