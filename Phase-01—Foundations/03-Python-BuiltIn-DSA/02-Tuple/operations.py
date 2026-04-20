"""
operations.py – Python Tuple Operations with Complexity Analysis

This script demonstrates common Python tuple operations.
Each section includes detailed comments about:
- What the operation does
- Time complexity (Big O)
- Space complexity
- Important notes (e.g., immutability, hashability, edge cases)

Run the script to see the output and follow along with the explanations.
"""

def main():
    # -------------------- Creating Tuples --------------------
    # Operation: Creating a tuple using literals.
    # Time complexity: O(k) where k = number of initial elements.
    #   - Each element reference is placed into the fixed‑size array.
    # Space complexity: O(k) for the underlying array of pointers.
    #   - Unlike lists, tuples do NOT over‑allocate; size is fixed at creation.
    #
    # Note: For a single‑element tuple, the trailing comma is required.
    #   (42)   -> this is just the int 42 in parentheses
    #   (42,)  -> this is a 1‑element tuple
    print("1. Creating Tuples")
    empty_tuple = ()
    single = (42,)                          # trailing comma is required!
    numbers = (1, 2, 3, 4, 5)
    mixed = (1, "hello", 3.14, (6, 7))      # tuples can hold mixed types
    packed = 1, 2, 3                        # parentheses optional – the comma makes the tuple
    from_iter = tuple([10, 20, 30])         # build from any iterable
    print(f"   empty_tuple: {empty_tuple}")
    print(f"   single: {single}")
    print(f"   numbers: {numbers}")
    print(f"   mixed: {mixed}")
    print(f"   packed: {packed}")
    print(f"   from_iter: {from_iter}")
    print()

    # -------------------- Accessing Elements --------------------
    # Operation: Indexing (tup[i])
    # Time complexity: O(1) – direct pointer arithmetic on the underlying array.
    # Space complexity: O(1).
    #
    # Operation: Slicing (tup[i:j])
    # Time complexity: O(k) where k = j - i. Creates a new tuple.
    # Space complexity: O(k) for the new tuple.
    print("2. Accessing Elements")
    print(f"   numbers[0] = {numbers[0]}")           # first element
    print(f"   numbers[-1] = {numbers[-1]}")         # last element (negative index)
    print(f"   numbers[1:3] = {numbers[1:3]}")       # slice from index 1 to 2
    print(f"   numbers[::-1] = {numbers[::-1]}")     # reversed copy (new tuple)
    print()

    # -------------------- Immutability --------------------
    # Tuples CANNOT be modified after creation.
    # There is no append, insert, remove, pop, sort, or reverse method.
    # Attempting to assign to an index raises TypeError.
    #
    # However, if a tuple contains a MUTABLE element (like a list),
    # that inner object can still be mutated — the tuple slot (pointer) is
    # unchanged, but the object it points to can change internally.
    print("3. Immutability")
    try:
        numbers[0] = 99                             # will raise TypeError
    except TypeError as e:
        print(f"   numbers[0] = 99 raised TypeError: {e}")

    nested = (1, 2, [3, 4])
    print(f"   before mutating inner list: {nested}")
    nested[2].append(5)                             # allowed – mutates the inner list
    print(f"   after nested[2].append(5):  {nested}")
    print()

    # -------------------- Concatenation and Repetition --------------------
    # Operation: Concatenation (t1 + t2)
    # Time complexity: O(n + m) where n, m are the input sizes.
    #   - Creates a NEW tuple; inputs are untouched (immutability).
    # Space complexity: O(n + m) for the new tuple.
    #
    # Operation: Repetition (tup * k)
    # Time complexity: O(n · k) – copies n references k times.
    # Space complexity: O(n · k) for the new tuple.
    print("4. Concatenation and Repetition")
    a = (1, 2, 3)
    b = (4, 5)
    print(f"   a + b = {a + b}")
    print(f"   a * 3 = {a * 3}")
    print()

    # -------------------- Searching and Counting --------------------
    # Operation: index(x)
    # Time complexity: O(n) – linear scan until value found.
    # Space complexity: O(1).
    # Raises ValueError if x is not present.
    #
    # Operation: count(x)
    # Time complexity: O(n) – scans the entire tuple.
    # Space complexity: O(1).
    #
    # Operation: membership (x in tup)
    # Time complexity: O(n) – linear scan.
    # Space complexity: O(1).
    print("5. Searching and Counting")
    sample = (1, 2, 3, 2, 4, 2)
    print(f"   sample = {sample}")
    print(f"   index of first 2: {sample.index(2)}")
    print(f"   count of 2: {sample.count(2)}")
    print(f"   is 5 in sample? {5 in sample}")
    print()

    # -------------------- Unpacking --------------------
    # Tuple unpacking assigns each element to a target variable in one step.
    # Time complexity: O(n) – one assignment per element.
    # Space complexity: O(1) beyond the existing references.
    #
    # The starred form (*rest) collects the remaining elements into a list.
    print("6. Unpacking")
    point = (3, 4)
    x, y = point
    print(f"   point = {point} -> x={x}, y={y}")

    record = ("alice", 30, "engineer")
    name, age, role = record
    print(f"   name={name}, age={age}, role={role}")

    head, *middle, tail = (1, 2, 3, 4, 5)
    print(f"   head={head}, middle={middle}, tail={tail}")

    # Swapping without a temp variable (Pythonic idiom)
    p, q = 1, 2
    p, q = q, p
    print(f"   after swap: p={p}, q={q}")
    print()

    # -------------------- Returning Multiple Values --------------------
    # A function that returns "multiple values" actually returns a tuple.
    # The caller can then unpack it directly.
    print("7. Returning Multiple Values")

    def min_max(xs):
        return min(xs), max(xs)                     # returns a tuple (implicit parentheses)

    lo, hi = min_max([3, 1, 4, 1, 5, 9, 2, 6])
    print(f"   min={lo}, max={hi}")
    print()

    # -------------------- Tuples as Dict Keys / Set Members --------------------
    # Because tuples are immutable AND hashable (when their elements are),
    # they can be used as dictionary keys or added to sets.
    # This is one of the most important practical differences from lists.
    print("8. Tuples as Dict Keys and Set Members")
    locations = {
        (40.7128, -74.0060): "New York",
        (34.0522, -118.2437): "Los Angeles",
    }
    print(f"   locations[(40.7128, -74.0060)] = {locations[(40.7128, -74.0060)]}")

    seen_pairs = {(1, 2), (3, 4), (1, 2)}           # duplicates removed
    print(f"   set of pairs: {seen_pairs}")

    # A tuple containing a list is NOT hashable
    try:
        hash((1, [2, 3]))
    except TypeError as e:
        print(f"   hash((1, [2, 3])) raised TypeError: {e}")
    print()

    # -------------------- Sorting (returns a LIST) --------------------
    # Tuples have no .sort() method. Use the built-in sorted(),
    # which returns a NEW list. Convert back with tuple() if needed.
    # Time complexity: O(n log n) (Timsort).
    # Space complexity: O(n) for the new list/tuple.
    print("9. Sorting")
    unsorted = (5, 2, 8, 1, 9)
    sorted_list = sorted(unsorted)                  # returns a list
    sorted_tuple = tuple(sorted(unsorted))          # convert back to tuple
    print(f"   unsorted:     {unsorted}")
    print(f"   sorted() ->   {sorted_list}   (list)")
    print(f"   tuple(sorted) {sorted_tuple}   (tuple)")
    print()

    # -------------------- Iteration --------------------
    # Tuples are iterable just like lists.
    # Time complexity: O(n) to visit each element.
    # Space complexity: O(1) beyond the iterator.
    #
    # Note: there is no such thing as a "tuple comprehension" — the
    # expression (x for x in ...) creates a GENERATOR, not a tuple.
    # To build a tuple from a comprehension, wrap it with tuple(...).
    print("10. Iteration")
    for value in record:
        print(f"   value: {value}")

    squares = tuple(x * x for x in range(5))        # generator -> tuple
    print(f"   squares of 0..4: {squares}")
    print()

    # -------------------- Nested Tuples --------------------
    # Tuples can contain other tuples, forming immutable matrices / records of records.
    # Indexing into nested tuples is O(1) per level.
    print("11. Nested Tuples (Matrix)")
    matrix = (
        (1, 2, 3),
        (4, 5, 6),
        (7, 8, 9),
    )
    for row in matrix:
        print(f"      {row}")
    print(f"   matrix[1][2] = {matrix[1][2]}")
    print()

    # -------------------- Length and Other Utilities --------------------
    # Operation: len()
    # Time complexity: O(1) – length is stored as an attribute.
    # Space complexity: O(1).
    #
    # Operation: max(), min(), sum()
    # Time complexity: O(n) – must scan all elements.
    # Space complexity: O(1).
    print("12. Length and Utilities")
    nums = (3, 1, 4, 1, 5, 9, 2, 6)
    print(f"   len(nums) = {len(nums)}")
    print(f"   max(nums) = {max(nums)}")
    print(f"   min(nums) = {min(nums)}")
    print(f"   sum(nums) = {sum(nums)}")
    print()

    # -------------------- Conversion Between Tuple and List --------------------
    # tuple(list)  -> O(n), creates a new tuple
    # list(tuple)  -> O(n), creates a new list
    # Useful pattern: convert to list, mutate, convert back to tuple.
    print("13. Converting Between Tuple and List")
    as_list = list(numbers)
    as_list.append(6)                                # list is mutable
    back_to_tuple = tuple(as_list)
    print(f"   numbers (tuple): {numbers}")
    print(f"   list(numbers):   {as_list}")
    print(f"   tuple(as_list):  {back_to_tuple}")
    print()

    # -------------------- Performance Note: Tuples vs Lists --------------------
    # Tuples are generally:
    #   - Faster to construct (no over‑allocation, CPython reuses small tuples)
    #   - Slightly smaller in memory (no spare capacity)
    #   - Hashable (usable as dict keys / set members)
    # Prefer tuples for FIXED, HETEROGENEOUS records.
    # Prefer lists for GROWING / HOMOGENEOUS sequences.
    print("14. Performance Note")
    print("   Use a tuple for fixed records (e.g., coordinates, DB rows).")
    print("   Use a list when you need to add, remove, or reorder items.")


if __name__ == "__main__":
    main()
