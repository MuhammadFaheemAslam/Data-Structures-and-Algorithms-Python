"""
operations.py – Python Set Operations with Complexity Analysis

This script demonstrates common Python set operations.
Each section includes detailed comments about:
- What the operation does
- Time complexity (Big O)
- Space complexity
- Important notes (hashability, order, algebra, edge cases)

Run the script to see the output and follow along with the explanations.
"""

def main():
    # -------------------- Creating Sets --------------------
    # Operation: Creating a set using literals or the set() constructor.
    # Time complexity: O(k) where k = number of initial elements.
    #   - Each element is hashed and placed into the hash table.
    # Space complexity: O(k) for the underlying hash table.
    #   - The table is pre-allocated larger than k to keep the load factor low.
    #
    # IMPORTANT pitfall:
    #   {}      -> an empty DICT, not a set
    #   set()   -> an empty set
    print("1. Creating Sets")
    empty_set = set()                      # correct way to create an empty set
    numbers = {1, 2, 3, 4, 5}
    from_list = set([1, 2, 2, 3, 3, 3])    # duplicates are dropped automatically
    from_string = set("hello")             # {'h', 'e', 'l', 'o'} – unordered
    comp = {x * x for x in range(5)}       # set comprehension
    print(f"   empty_set:   {empty_set}")
    print(f"   numbers:     {numbers}")
    print(f"   from_list:   {from_list}  (duplicates dropped)")
    print(f"   from_string: {from_string}")
    print(f"   comp {{x*x}}:  {comp}")
    print()

    # -------------------- Hashability Requirement --------------------
    # Sets only accept HASHABLE elements. Mutable containers like list,
    # dict, and set itself are not hashable and will raise TypeError.
    # Tuples OF hashables and frozenset ARE hashable.
    print("2. Hashability Requirement")
    ok = {1, "hi", (3, 4), frozenset({5, 6})}
    print(f"   ok: {ok}")
    try:
        bad = {[1, 2]}                     # list is unhashable
    except TypeError as e:
        print(f"   {{[1, 2]}} raised TypeError: {e}")
    print()

    # -------------------- Adding Elements --------------------
    # Operation: add(x)
    # Time complexity: O(1) average – hash + slot write.
    #                   Amortized O(1) when resize is triggered.
    # Space complexity: O(1) amortized.
    #
    # Operation: update(iterable)
    # Time complexity: O(k) where k = len(iterable).
    print("3. Adding Elements")
    s = {1, 2, 3}
    s.add(4)
    print(f"   after add(4):           {s}")
    s.add(2)                               # already present – no effect
    print(f"   after add(2) (dup):     {s}")
    s.update([5, 6, 7])
    print(f"   after update([5,6,7]):  {s}")
    print()

    # -------------------- Removing Elements --------------------
    # Operation: remove(x)
    # Time complexity: O(1) average.
    # Raises KeyError if x is absent.
    #
    # Operation: discard(x)
    # Time complexity: O(1) average.
    # Silently does nothing if x is absent – prefer this when you're
    # not sure whether the element exists.
    #
    # Operation: pop()
    # Time complexity: O(1) average.
    # Removes and returns an ARBITRARY element (not "the first" –
    # sets have no order).
    #
    # Operation: clear()
    # Time complexity: O(n) – frees all internal slots.
    print("4. Removing Elements")
    s = {10, 20, 30, 40}
    s.remove(20)
    print(f"   after remove(20):     {s}")
    s.discard(99)                          # not present – no error
    print(f"   after discard(99):    {s}  (99 wasn't there, no crash)")
    try:
        s.remove(99)                       # raises KeyError
    except KeyError as e:
        print(f"   remove(99) raised KeyError: {e}")
    popped = s.pop()
    print(f"   pop() returned {popped}, set now {s}")
    s.clear()
    print(f"   after clear():        {s}")
    print()

    # -------------------- Membership Testing (The Superpower) --------------------
    # Operation: x in s
    # Time complexity: O(1) average – one hash + slot compare.
    # Space complexity: O(1).
    #
    # Contrast with `x in list`, which is O(n). For membership-heavy
    # workloads, converting a list to a set is almost always worth it.
    print("5. Membership Testing")
    big_set = set(range(1_000_000))
    print(f"   500_000 in big_set? {500_000 in big_set}   (O(1) average)")
    print(f"   9_999_999 in big_set? {9_999_999 in big_set}")
    print()

    # -------------------- Set Algebra: Union --------------------
    # Operation: a | b   or   a.union(b)
    # Returns a NEW set containing every element that appears in
    # either a, b, or both.
    # Time complexity: O(len(a) + len(b))
    # Space complexity: O(len(a) + len(b))
    #
    # Note: the `|` operator requires BOTH sides to be sets.
    # The .union() method accepts any iterable.
    print("6. Union (|)")
    a = {1, 2, 3, 4}
    b = {3, 4, 5, 6}
    print(f"   a = {a}")
    print(f"   b = {b}")
    print(f"   a | b          = {a | b}")
    print(f"   a.union([7,8]) = {a.union([7, 8])}  (method accepts any iterable)")
    print()

    # -------------------- Set Algebra: Intersection --------------------
    # Operation: a & b   or   a.intersection(b)
    # Returns a NEW set of elements that appear in BOTH.
    # Time complexity: O(min(len(a), len(b)))
    #   - Python iterates the smaller set and looks up each in the larger.
    # Space complexity: O(min(len(a), len(b)))
    print("7. Intersection (&)")
    print(f"   a & b = {a & b}   (common to both)")
    print()

    # -------------------- Set Algebra: Difference --------------------
    # Operation: a - b   or   a.difference(b)
    # Returns a NEW set of elements in a that are NOT in b.
    # Time complexity: O(len(a))
    # Space complexity: O(len(a))
    print("8. Difference (-)")
    print(f"   a - b = {a - b}   (in a but not in b)")
    print(f"   b - a = {b - a}   (in b but not in a)")
    print()

    # -------------------- Set Algebra: Symmetric Difference --------------------
    # Operation: a ^ b   or   a.symmetric_difference(b)
    # Returns a NEW set of elements in EXACTLY ONE of the two sets.
    # Time complexity: O(len(a) + len(b))
    # Space complexity: O(len(a) + len(b))
    print("9. Symmetric Difference (^)")
    print(f"   a ^ b = {a ^ b}   (in exactly one)")
    print()

    # -------------------- Subset / Superset / Disjoint --------------------
    # Operation: a <= b   or   a.issubset(b)
    # True if every element of a is also in b.
    # Time complexity: O(len(a))
    #
    # Operation: a >= b   or   a.issuperset(b)
    # True if a contains every element of b.
    # Time complexity: O(len(b))
    #
    # Operation: a.isdisjoint(b)
    # True if a and b share NO elements.
    # Time complexity: O(min(len(a), len(b)))
    print("10. Subset / Superset / Disjoint")
    small = {3, 4}
    print(f"   small = {small}, a = {a}")
    print(f"   small <= a            -> {small <= a}   (subset?)")
    print(f"   a >= small            -> {a >= small}   (superset?)")
    print(f"   a.isdisjoint({{100,200}}) -> {a.isdisjoint({100, 200})}")
    print()

    # -------------------- In-place Update Variants --------------------
    # Every binary set operator has an in-place form that mutates `a`.
    # These avoid allocating a new set when you don't need the old one.
    #
    #   a |= b    a.update(b)                 – union in place
    #   a &= b    a.intersection_update(b)    – intersection in place
    #   a -= b    a.difference_update(b)      – difference in place
    #   a ^= b    a.symmetric_difference_update(b)
    print("11. In-place Updates")
    x = {1, 2, 3}
    x |= {3, 4, 5}
    print(f"   x |= {{3,4,5}} -> {x}")
    x -= {1}
    print(f"   x -= {{1}}     -> {x}")
    print()

    # -------------------- Deduplication Idiom --------------------
    # The classic use case: drop duplicates from a list.
    # Time complexity: O(n)
    # Space complexity: O(n)
    # Downside: order is NOT preserved.
    # If you need order preserved, see the tuple problem 03 pattern
    # (walk the list with a `seen` set).
    print("12. Deduplication Idiom")
    raw = [1, 2, 2, 3, 3, 3, 4, 1, 5]
    unique = list(set(raw))
    print(f"   raw:    {raw}")
    print(f"   unique: {unique}   (order NOT guaranteed)")
    print()

    # -------------------- Iteration --------------------
    # Sets are iterable, but iteration order is IMPLEMENTATION DEFINED.
    # Never rely on it. If you need an ordered view, sort during iteration.
    # Time complexity: O(n)
    print("13. Iteration")
    s = {30, 10, 20, 40}
    print(f"   set:            {s}")
    print(f"   for v in s:     {[v for v in s]}   (order not guaranteed)")
    print(f"   sorted(s):      {sorted(s)}       (returns a list, deterministic)")
    print()

    # -------------------- frozenset: The Hashable Set --------------------
    # A frozenset is an IMMUTABLE set. Because it is immutable, it is
    # hashable — so it can be an element of another set, or a dict key.
    # All the read operations (union, intersection, membership, …) work.
    # Write operations (add, remove, update, …) do NOT exist.
    print("14. frozenset")
    fs = frozenset([1, 2, 3])
    print(f"   fs = {fs}")
    print(f"   2 in fs: {2 in fs}")
    nested = {frozenset({1, 2}), frozenset({3, 4})}   # set of frozensets
    print(f"   set of frozensets: {nested}")
    try:
        fs.add(4)                          # no such method
    except AttributeError as e:
        print(f"   fs.add(4) raised AttributeError: {e}")
    print()

    # -------------------- Length and Other Utilities --------------------
    # Operation: len()
    # Time complexity: O(1) – size stored as an attribute.
    #
    # Operation: max(), min(), sum()
    # Time complexity: O(n) – must scan all elements.
    print("15. Length and Utilities")
    nums = {3, 1, 4, 1, 5, 9, 2, 6}        # {1, 2, 3, 4, 5, 6, 9}
    print(f"   nums:      {nums}")
    print(f"   len(nums): {len(nums)}")
    print(f"   max(nums): {max(nums)}")
    print(f"   min(nums): {min(nums)}")
    print(f"   sum(nums): {sum(nums)}")
    print()

    # -------------------- Performance: List vs Set Membership --------------------
    # Converting to a set once, then doing many `in` checks, turns an
    # O(n * m) search into O(n + m). This is one of the most common
    # performance wins in Python code.
    print("16. Performance Note")
    needles = [17, 42, 999, 500_000, 1_000_001]
    haystack_list = list(range(1_000_000))
    haystack_set  = set(haystack_list)

    found_list = [n for n in needles if n in haystack_list]   # O(m * n)
    found_set  = [n for n in needles if n in haystack_set]    # O(m)
    print(f"   found via list scan: {found_list}")
    print(f"   found via set  scan: {found_set}   (dramatically faster)")


if __name__ == "__main__":
    main()
