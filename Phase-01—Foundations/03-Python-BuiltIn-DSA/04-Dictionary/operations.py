"""
operations.py – Python Dictionary Operations with Complexity Analysis

This script demonstrates common Python dict operations.
Each section includes detailed comments about:
- What the operation does
- Time complexity (Big O)
- Space complexity
- Important notes (hashability, order, views, edge cases)

Run the script to see the output and follow along with the explanations.
"""

def main():
    # -------------------- Creating Dictionaries --------------------
    # Operation: Creating a dict using literals or the dict() constructor.
    # Time complexity: O(k) where k = number of initial entries.
    #   - Each key is hashed and placed into the hash table.
    # Space complexity: O(k) for the underlying hash table.
    #   - The table is pre-allocated larger than k to keep the load factor low.
    #
    # IMPORTANT pitfall:
    #   {}     -> an empty DICT (not a set!)
    #   set()  -> an empty set
    print("1. Creating Dictionaries")
    empty = {}
    scores = {"alice": 90, "bob": 85, "carol": 78}
    from_kwargs = dict(alice=90, bob=85)                    # keys must be valid identifiers
    from_pairs = dict([("a", 1), ("b", 2)])                 # iterable of 2-tuples
    zipped = dict(zip(["x", "y", "z"], [10, 20, 30]))       # parallel iterables
    comp = {x: x * x for x in range(5)}                     # dict comprehension
    print(f"   empty:       {empty}")
    print(f"   scores:      {scores}")
    print(f"   from_kwargs: {from_kwargs}")
    print(f"   from_pairs:  {from_pairs}")
    print(f"   zipped:      {zipped}")
    print(f"   {{x: x*x}}:     {comp}")
    print()

    # -------------------- Key Hashability --------------------
    # Dict keys must be HASHABLE. Immutable types (int, str, tuple of
    # hashables, frozenset) work. Mutable types (list, dict, set) don't.
    # VALUES can be anything — no restriction.
    print("2. Key Hashability")
    ok = {1: "int", "hi": "str", (3, 4): "tuple", frozenset({5, 6}): "fset"}
    print(f"   ok: {ok}")
    try:
        bad = {[1, 2]: "list as key"}
    except TypeError as e:
        print(f"   {{[1, 2]: ...}} raised TypeError: {e}")
    print()

    # -------------------- Accessing Values --------------------
    # Operation: d[k]
    # Time complexity: O(1) average.
    # Raises KeyError if k is absent.
    #
    # Operation: d.get(k) / d.get(k, default)
    # Time complexity: O(1) average.
    # Returns None (or the supplied default) if k is absent.
    #
    # Operation: d.setdefault(k, default)
    # Time complexity: O(1) average.
    # Returns existing value if k is present, else inserts default
    # AND returns it. Handy for lazy initialization.
    print("3. Accessing Values")
    d = {"a": 1, "b": 2}
    print(f"   d['a']           = {d['a']}")
    try:
        _ = d["missing"]
    except KeyError as e:
        print(f"   d['missing']     raised KeyError: {e}")
    print(f"   d.get('missing') = {d.get('missing')}")
    print(f"   d.get('x', 0)    = {d.get('x', 0)}")

    lazy = {}
    lazy.setdefault("list", []).append("first")
    lazy.setdefault("list", []).append("second")            # key already exists, default ignored
    print(f"   after setdefault twice: {lazy}")
    print()

    # -------------------- Adding / Updating Entries --------------------
    # Operation: d[k] = v
    # Time complexity: O(1) average. Amortized O(1) if a resize is needed.
    # Assigning an existing key OVERWRITES the old value.
    #
    # Operation: d.update(other)
    # Time complexity: O(k) where k = len(other).
    # Accepts a dict, an iterable of pairs, or keyword arguments.
    print("4. Adding and Updating")
    d = {"a": 1}
    d["b"] = 2                                              # insert
    d["a"] = 99                                             # overwrite
    print(f"   after insert/overwrite: {d}")
    d.update({"c": 3, "d": 4})                              # merge another dict
    d.update(e=5, f=6)                                      # keyword form
    print(f"   after update():         {d}")
    print()

    # -------------------- Removing Entries --------------------
    # Operation: del d[k]
    # Time complexity: O(1) average.
    # Raises KeyError if k is absent.
    #
    # Operation: d.pop(k) / d.pop(k, default)
    # Time complexity: O(1) average.
    # Removes and returns the value. With a default, won't raise on missing.
    #
    # Operation: d.popitem()
    # Time complexity: O(1).
    # Removes and returns the LAST-INSERTED (key, value) pair.
    # (Before Python 3.7, order was arbitrary.)
    #
    # Operation: d.clear()
    # Time complexity: O(n).
    print("5. Removing Entries")
    d = {"a": 1, "b": 2, "c": 3, "d": 4}
    del d["b"]
    print(f"   after del d['b']:     {d}")
    val = d.pop("a")
    print(f"   pop('a') -> {val}, d = {d}")
    val = d.pop("missing", -1)
    print(f"   pop('missing', -1) -> {val}, d = {d}")
    last = d.popitem()
    print(f"   popitem() -> {last}, d = {d}   (removed last-inserted)")
    d.clear()
    print(f"   after clear():        {d}")
    print()

    # -------------------- Membership --------------------
    # Operation: k in d
    # Time complexity: O(1) average.
    # IMPORTANT: `in` checks KEYS, not values. To check values, use
    # `v in d.values()` which is O(n).
    print("6. Membership")
    d = {"a": 1, "b": 2, "c": 3}
    print(f"   'a' in d           -> {'a' in d}")
    print(f"   1   in d           -> {1 in d}           (False – 1 is a value, not a key)")
    print(f"   1   in d.values()  -> {1 in d.values()}   (O(n) – linear scan of values)")
    print()

    # -------------------- Iteration --------------------
    # Iterating a dict yields its KEYS (in insertion order, Python 3.7+).
    # Time complexity: O(n)
    #
    # d.keys()   -> view of keys
    # d.values() -> view of values
    # d.items()  -> view of (key, value) pairs
    #
    # Views are LIVE – they reflect changes to the dict.
    # Views are cheap – O(1) to create; they don't copy data.
    print("7. Iteration")
    d = {"a": 1, "b": 2, "c": 3}
    print(f"   iterating d (keys):       {[k for k in d]}")
    print(f"   d.keys():                 {list(d.keys())}")
    print(f"   d.values():               {list(d.values())}")
    print(f"   d.items():                {list(d.items())}")

    # Proof that views are live
    keys_view = d.keys()
    d["z"] = 99
    print(f"   keys_view after adding z: {list(keys_view)}")
    print()

    # -------------------- Views Are Set-Like --------------------
    # `d.keys()` and `d.items()` (where values are hashable) support
    # set-algebra operators: &, |, -, ^.
    # Useful for comparing two dicts' key sets directly.
    print("8. Dict Views as Set Algebra")
    d1 = {"a": 1, "b": 2, "c": 3}
    d2 = {"b": 20, "c": 30, "d": 40}
    print(f"   d1.keys() & d2.keys() = {d1.keys() & d2.keys()}   (shared keys)")
    print(f"   d1.keys() - d2.keys() = {d1.keys() - d2.keys()}   (only in d1)")
    print(f"   d1.keys() | d2.keys() = {d1.keys() | d2.keys()}   (all keys)")
    print()

    # -------------------- Merging --------------------
    # Python 3.9+ provides the | and |= operators for dicts.
    # On key collisions, the RIGHT-hand side wins.
    #   a | b   -> new dict
    #   a |= b  -> update a in place (same as a.update(b))
    print("9. Merging")
    defaults = {"debug": False, "port": 8080, "host": "localhost"}
    override = {"port": 9000, "debug": True}
    merged = defaults | override                            # new dict
    print(f"   defaults:            {defaults}")
    print(f"   override:            {override}")
    print(f"   defaults | override: {merged}   (right-hand side wins)")
    print()

    # -------------------- The Counting Idiom --------------------
    # Building a histogram with a plain dict.
    # Time complexity: O(n)
    # Space complexity: O(k) where k = number of distinct items.
    #
    # `collections.Counter` does this in one line and is usually preferred,
    # but the manual pattern is worth knowing by heart.
    print("10. Counting Idiom")
    words = ["apple", "banana", "apple", "cherry", "banana", "apple"]
    counts = {}
    for w in words:
        counts[w] = counts.get(w, 0) + 1
    print(f"   words:  {words}")
    print(f"   counts: {counts}")
    print()

    # -------------------- The Grouping Idiom --------------------
    # Classic use of setdefault(): build a dict of lists keyed by a category.
    # Time complexity: O(n)
    # Space complexity: O(n)
    #
    # `collections.defaultdict(list)` simplifies this further.
    print("11. Grouping Idiom")
    items = [
        ("fruit", "apple"),
        ("veg",   "carrot"),
        ("fruit", "pear"),
        ("veg",   "broccoli"),
        ("fruit", "banana"),
    ]
    groups = {}
    for category, item in items:
        groups.setdefault(category, []).append(item)
    print(f"   groups: {groups}")
    print()

    # -------------------- Dict Comprehensions --------------------
    # Concise way to build or transform a dict.
    # Time complexity: O(n)
    # Space complexity: O(n)
    print("12. Dict Comprehensions")
    squares = {x: x * x for x in range(6)}
    print(f"   squares: {squares}")

    # Invert a dict (swap keys and values) – beware: values must be unique
    original = {"a": 1, "b": 2, "c": 3}
    inverted = {v: k for k, v in original.items()}
    print(f"   inverted: {inverted}")
    print()

    # -------------------- Length and Other Utilities --------------------
    # Operation: len(d)    – O(1)
    # Operation: max/min/sum on d  -> operates on KEYS by default
    # Operation: max(d.values())   -> operates on values, O(n)
    print("13. Length and Utilities")
    scores = {"alice": 90, "bob": 85, "carol": 78, "dan": 92}
    print(f"   scores:            {scores}")
    print(f"   len(scores):       {len(scores)}")
    print(f"   max(scores):       {max(scores)}           (max KEY)")
    print(f"   max(scores.values()): {max(scores.values())}           (max value)")

    # Find the key with the max value – very common interview pattern
    top_name = max(scores, key=scores.get)
    print(f"   max(scores, key=scores.get) -> {top_name!r}   (key with largest value)")
    print()

    # -------------------- Performance Note: Dict vs List of Pairs --------------------
    # A list of (key, value) pairs forces O(n) scans to find anything.
    # A dict turns those scans into O(1) lookups — usually the right call.
    print("14. Performance Note: dict vs list-of-pairs")
    as_pairs = [("alice", 90), ("bob", 85), ("carol", 78)]
    as_dict  = dict(as_pairs)

    # Find bob's score
    from_list = next((score for name, score in as_pairs if name == "bob"), None)  # O(n)
    from_dict = as_dict.get("bob")                                                # O(1) avg

    print(f"   list lookup -> {from_list}")
    print(f"   dict lookup -> {from_dict}   (dramatically faster at scale)")


if __name__ == "__main__":
    main()
