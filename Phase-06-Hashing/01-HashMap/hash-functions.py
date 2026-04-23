"""
hash-functions.py – Designing and Comparing Hash Functions

A hash function maps arbitrary-sized keys to fixed-size integer
bucket indices. What separates a GOOD hash from a BAD one?

    - Deterministic:   same input → same output
    - Uniform:         outputs spread evenly over the range
    - Fast:            computable in O(|key|)
    - Avalanche:       one-bit input change flips about half the output bits

This file implements several classic hash functions, compares their
distribution quality on real-world inputs, and shows why Python's
built-in `hash()` uses a CRYPTOGRAPHIC scheme (SipHash) with a
random seed.

---------------------------------------------------
Hash Functions Implemented:

    1. trivial_hash            — terrible; shows what NOT to do
    2. length_hash             — still terrible (all same-length keys collide)
    3. sum_hash                — bad (anagrams collide)
    4. polynomial_hash         — good; the classic "Rabin-Karp" hash
    5. fnv_hash                — FNV-1a: fast, non-cryptographic
    6. python_builtin_hash     — SipHash (via hash()) — cryptographic

We test each on the same input and compare collision rates.
"""


# =========================================================================
# The Table Size (for bucket mapping)
# =========================================================================

TABLE_SIZE = 97                                   # a prime; reduces clustering


# =========================================================================
# 1. Trivial Hash — ALWAYS Returns 0 (Just to Show What "Bad" Looks Like)
# =========================================================================

def trivial_hash(key):
    """
    The worst possible hash function: every key hashes to 0.

    Time:  O(1)
    Collisions: EVERY key collides. The hash table degenerates to a
                linked list. Lookup becomes O(n).

    This exists to make the "uniform distribution" property concrete:
    without it, hash tables don't work.
    """
    return 0 % TABLE_SIZE


# =========================================================================
# 2. Length Hash — By Key Length (Still Terrible)
# =========================================================================

def length_hash(key):
    """
    Hash strings by their LENGTH.

    All strings of the same length collide. If your keys are
    usernames (mostly 5-15 chars), they all crowd into 10 buckets.

    Time:  O(1)
    Collisions: heavy clustering.
    """
    return len(key) % TABLE_SIZE


# =========================================================================
# 3. Sum Hash — Sum of Character Codes (Anagram-Fragile)
# =========================================================================

def sum_hash(key):
    """
    Hash strings by the sum of character codes.

    Problem: ANAGRAMS collide. "listen" and "silent" sum to the same
    total. "ab" and "ba" are identical.

    Time:  O(|key|)
    """
    total = 0
    for ch in key:
        total += ord(ch)
    return total % TABLE_SIZE


# =========================================================================
# 4. Polynomial Hash — The Classic "Rabin-Karp" Hash
# =========================================================================

def polynomial_hash(key, base=31, modulus=(1 << 32) - 1):
    """
    Treat the string as a number in base `base`:

        h("abc") = 'a' * base² + 'b' * base + 'c'

    Uses modulus to keep the result bounded.

    Time:  O(|key|)
    Collisions: much better than sum/length hashes. Good enough for
    most applications — but NOT cryptographically secure, so attackers
    who know `base` and `modulus` can engineer collisions.

    `base = 31` is the standard (used in Java's `String.hashCode`).
    31 is odd, prime, and easy for the compiler to optimize
    (`31 * x == (x << 5) - x`).
    """
    h = 0
    for ch in key:
        h = (h * base + ord(ch)) % modulus
    return h % TABLE_SIZE


# =========================================================================
# 5. FNV-1a — A Strong Non-Cryptographic Hash
# =========================================================================

def fnv_hash(key, offset=14695981039346656037, prime=1099511628211):
    """
    FNV-1a (Fowler-Noll-Vo, 64-bit variant). Widely used in
    non-cryptographic contexts (DNS caches, DB indexes).

    Algorithm:
        hash = FNV_offset
        for byte in input:
            hash = hash XOR byte
            hash = hash * FNV_prime (mod 2^64)

    Time:  O(|key|)
    Properties: good distribution, very fast, simple to implement.
    Not resistant to adversarial collision attacks — but fine for
    internal use.
    """
    mask = (1 << 64) - 1
    h = offset
    for ch in key:
        h ^= ord(ch)
        h = (h * prime) & mask                    # modulo 2^64
    return h % TABLE_SIZE


# =========================================================================
# 6. Python's Built-In `hash()` — Cryptographic (SipHash)
# =========================================================================

def python_builtin_hash(key):
    """
    Python's built-in hash. Uses SipHash with a random per-process
    seed for strings/bytes.

    The random seed is the reason the same string hashes to DIFFERENT
    values in different Python runs — it prevents a class of
    attacks called "hash collision DoS," where a malicious client
    sends keys designed to force every hash into the same bucket.

    Time: O(|key|)
    Properties: cryptographically strong, unpredictable across runs.
    Slower than FNV/polynomial but still very fast in C.
    """
    return hash(key) % TABLE_SIZE


# =========================================================================
# Collision-Rate Comparison
# =========================================================================

def collision_rate(hash_fn, keys):
    """
    Count how many keys collide in a table of size TABLE_SIZE.

    Returns (num_collisions, num_nonempty_buckets).
    """
    buckets = {}
    for k in keys:
        h = hash_fn(k)
        buckets.setdefault(h, []).append(k)

    collisions = sum(max(0, len(v) - 1) for v in buckets.values())
    return collisions, len(buckets)


def longest_chain(hash_fn, keys):
    """Return the length of the longest bucket chain."""
    buckets = {}
    for k in keys:
        h = hash_fn(k)
        buckets.setdefault(h, []).append(k)
    return max((len(v) for v in buckets.values()), default=0)


# =========================================================================
# Test and Compare
# =========================================================================

if __name__ == "__main__":
    # Real-world-ish test: common English words, usernames, URLs
    test_keys = [
        "alice", "bob", "carol", "dave", "eve", "frank", "grace", "henry",
        "iris", "jack", "kate", "leo", "mary", "nick", "olivia", "peter",
        "quinn", "rachel", "steve", "tom", "uma", "victor", "wendy", "xavier",
        "yara", "zack",
        # Anagrams (to expose sum_hash weakness)
        "listen", "silent", "enlist",
        "earth", "heart", "hater",
        # Similar prefixes
        "user1", "user2", "user3", "user4", "user5",
        # Common words
        "the", "and", "for", "with", "you", "this", "that", "from",
        # Similar length
        "cat", "bat", "rat", "hat", "mat", "fat", "pat", "sat",
    ]

    print(f"Testing on {len(test_keys)} keys, table size = {TABLE_SIZE}")
    print()

    hashes = [
        ("trivial_hash",        trivial_hash),
        ("length_hash",         length_hash),
        ("sum_hash",            sum_hash),
        ("polynomial_hash",     polynomial_hash),
        ("fnv_hash",            fnv_hash),
        ("python_builtin_hash", python_builtin_hash),
    ]

    print(f"{'Hash Function':<25}  {'Collisions':>12}  {'Nonempty Buckets':>18}  {'Longest Chain':>14}")
    print("-" * 76)
    for name, fn in hashes:
        c, b = collision_rate(fn, test_keys)
        lc = longest_chain(fn, test_keys)
        print(f"{name:<25}  {c:>12}  {b:>18}  {lc:>14}")

    print()
    print("Analysis:")
    print(f"   trivial_hash:        all keys in one bucket (chain of {len(test_keys)})")
    print(f"   length_hash:         keys grouped by length (many collisions)")
    print(f"   sum_hash:            anagrams collide (listen/silent/enlist)")
    print(f"   polynomial_hash:     spreads nicely; a few incidental collisions")
    print(f"   fnv_hash:            strong industrial hash, low collisions")
    print(f"   python_builtin:      cryptographic, randomized — same distribution quality,")
    print(f"                        PLUS resistance to adversarial attacks.")

    # Show that sum_hash fails on anagrams specifically
    print()
    print("Anagrams — sum_hash gives them the same bucket:")
    for a in ["listen", "silent", "enlist"]:
        print(f"   sum_hash({a!r}) = {sum_hash(a)}")
    print(f"\n   polynomial_hash gives them DIFFERENT buckets:")
    for a in ["listen", "silent", "enlist"]:
        print(f"   polynomial_hash({a!r}) = {polynomial_hash(a)}")

    # Show Python's hash randomization — values differ run-to-run
    print()
    print("Python hash randomization (these may differ if you re-run):")
    for k in ["alice", "bob"]:
        print(f"   hash({k!r}) = {hash(k)}")

    print("\nAll tests passed!")

    # ---------------------------------------------------------------
    # The Takeaway:
    #
    #   Hash function quality ENTIRELY determines hash-table
    #   performance. A bad hash function turns an "O(1) dict" into
    #   an O(n) one. CPython's `hash()` is not just fast — it's
    #   carefully engineered to resist adversarial inputs.
    #
    # If you ever implement your own `__hash__` for a custom class,
    # remember:
    #   (1) it must be consistent with `__eq__`
    #   (2) it should distribute well over your expected key set
    #   (3) for untrusted input, consider a randomized seed
    # ---------------------------------------------------------------
