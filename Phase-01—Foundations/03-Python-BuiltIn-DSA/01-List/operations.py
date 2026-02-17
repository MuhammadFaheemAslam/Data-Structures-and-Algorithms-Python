"""
operations.py – Python List Operations with Complexity Analysis

This script demonstrates common Python list operations.
Each section includes detailed comments about:
- What the operation does
- Time complexity (Big O)
- Space complexity
- Important notes (e.g., amortized behavior, edge cases)

Run the script to see the output and follow along with the explanations.
"""

def main():
    # -------------------- Creating Lists --------------------
    # Operation: Creating a list using literals.
    # Time complexity: O(k) where k = number of initial elements.
    #   - Each element is assigned to the new list.
    # Space complexity: O(k) for the underlying array of pointers.
    #   - The list stores references to objects; the objects themselves are allocated elsewhere.
    print("1. Creating Lists")
    empty_list = []
    numbers = [1, 2, 3, 4, 5]
    mixed = [1, "hello", 3.14, [6, 7]]  # list can hold mixed types
    print(f"   empty_list: {empty_list}")
    print(f"   numbers: {numbers}")
    print(f"   mixed: {mixed}")
    print()

    # -------------------- Accessing Elements --------------------
    # Operation: Indexing (lst[i])
    # Time complexity: O(1) – direct pointer arithmetic on the underlying array.
    # Space complexity: O(1) – no extra memory.
    #
    # Operation: Slicing (lst[i:j])
    # Time complexity: O(k) where k = j - i (if step=1). Creates a new list.
    # Space complexity: O(k) for the new list.
    print("2. Accessing Elements")
    print(f"   numbers[0] = {numbers[0]}")           # first element
    print(f"   numbers[-1] = {numbers[-1]}")         # last element (negative index)
    print(f"   numbers[1:3] = {numbers[1:3]}")       # slice from index 1 to 2 (exclusive 3)
    print()

    # -------------------- Modifying Elements --------------------
    # Operation: Single assignment (lst[i] = x)
    # Time complexity: O(1) – direct index update.
    # Space complexity: O(1).
    #
    # Operation: Slice assignment (lst[i:j] = iterable)
    # Time complexity: O(n + m) where n = len(lst), m = len(iterable).
    #   - May shift elements after the slice.
    # Space complexity: O(1) – in‑place (list may resize if slice length != iterable length).
    print("3. Modifying Elements")
    numbers[0] = 10
    print(f"   after numbers[0] = 10 -> {numbers}")
    numbers[1:3] = [20, 30]  # replace slice (indices 1 and 2) with [20,30]
    print(f"   after numbers[1:3] = [20, 30] -> {numbers}")
    print()

    # -------------------- Appending and Extending --------------------
    # Operation: append(x)
    # Time complexity: Amortized O(1). Worst‑case O(n) when resizing, but rare.
    #   - Appends element at the end; may trigger dynamic resize.
    # Space complexity: Amortized O(1) – occasionally O(n) during resize.
    #
    # Operation: extend(iterable)
    # Time complexity: O(k) where k = len(iterable). May cause resizes.
    # Space complexity: O(k) for the new elements (list capacity may increase).
    print("4. Appending and Extending")
    numbers.append(6)
    print(f"   after append(6) -> {numbers}")
    numbers.extend([7, 8, 9])
    print(f"   after extend([7,8,9]) -> {numbers}")
    print()

    # -------------------- Inserting --------------------
    # Operation: insert(i, x)
    # Time complexity: O(n) because all elements from index i onward are shifted right.
    # Space complexity: O(1) – works in place (may resize if full).
    print("5. Inserting")
    numbers.insert(2, 99)  # insert 99 at index 2
    print(f"   after insert(2, 99) -> {numbers}")
    print()

    # -------------------- Removing Elements --------------------
    # Operation: remove(x)
    # Time complexity: O(n) – linear search + shift of subsequent elements.
    # Space complexity: O(1).
    #
    # Operation: pop() – remove last element
    # Time complexity: O(1) – no shifting needed.
    # Space complexity: O(1).
    #
    # Operation: pop(i) – remove element at index i
    # Time complexity: O(n) – shifts elements left after removal.
    # Space complexity: O(1).
    #
    # Operation: del lst[i] – same as pop(i) but no return.
    # Time complexity: O(n).
    # Space complexity: O(1).
    print("6. Removing Elements")
    numbers.remove(99)  # remove first occurrence of 99
    print(f"   after remove(99) -> {numbers}")
    popped = numbers.pop()  # pop last element
    print(f"   popped last element: {popped} -> numbers now {numbers}")
    popped_at = numbers.pop(2)  # pop element at index 2
    print(f"   popped element at index 2: {popped_at} -> numbers now {numbers}")
    del numbers[0]  # delete first element
    print(f"   after del numbers[0] -> {numbers}")
    print()

    # -------------------- Searching and Counting --------------------
    # Operation: index(x)
    # Time complexity: O(n) – linear scan until value found.
    # Space complexity: O(1).
    #
    # Operation: count(x)
    # Time complexity: O(n) – scans entire list.
    # Space complexity: O(1).
    #
    # Operation: membership (x in lst)
    # Time complexity: O(n) – linear scan.
    # Space complexity: O(1).
    print("7. Searching and Counting")
    numbers = [1, 2, 3, 2, 4, 2]
    print(f"   numbers = {numbers}")
    print(f"   index of first 2: {numbers.index(2)}")
    print(f"   count of 2: {numbers.count(2)}")
    print(f"   is 5 in numbers? {5 in numbers}")
    print()

    # -------------------- Sorting and Reversing --------------------
    # Operation: sort()
    # Time complexity: O(n log n) average/worst case (Timsort).
    # Space complexity: O(n) worst case (Timsort uses temporary memory).
    #
    # Operation: reverse()
    # Time complexity: O(n) – swaps elements in place.
    # Space complexity: O(1).
    #
    # Operation: sorted() – returns a new sorted list.
    # Time complexity: O(n log n).
    # Space complexity: O(n) for the new list.
    print("8. Sorting and Reversing")
    unsorted = [5, 2, 8, 1, 9]
    print(f"   unsorted: {unsorted}")
    unsorted.sort()
    print(f"   after sort(): {unsorted}")
    unsorted.reverse()
    print(f"   after reverse(): {unsorted}")
    original = [3, 1, 4]
    new_sorted = sorted(original)
    print(f"   original: {original}, sorted(original): {new_sorted}")
    print()

    # -------------------- Copying --------------------
    # Operation: copy() or [:].
    # Both create a shallow copy (references are copied, not the objects themselves).
    # Time complexity: O(n) – copies all references.
    # Space complexity: O(n) for the new list.
    print("9. Copying")
    original = [1, 2, 3]
    copy1 = original.copy()
    copy2 = original[:]
    print(f"   original: {original}")
    print(f"   copy1 (copy()): {copy1}")
    print(f"   copy2 ([:]): {copy2}")
    original.append(4)
    print(f"   after original.append(4): original = {original}")
    print(f"   copy1 still: {copy1} (independent)")
    print()

    # -------------------- List Comprehensions --------------------
    # List comprehensions provide a concise way to create lists.
    # Time complexity: O(k) where k is the number of elements generated.
    # Space complexity: O(k) for the new list.
    print("10. List Comprehensions")
    squares = [x**2 for x in range(5)]
    print(f"   squares of 0..4: {squares}")
    evens = [x for x in range(10) if x % 2 == 0]
    print(f"   even numbers 0..9: {evens}")
    print()

    # -------------------- Nested Lists --------------------
    # Lists can contain other lists, forming matrices or jagged arrays.
    # Indexing into nested lists is O(1) per level.
    print("11. Nested Lists (Matrix)")
    matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    print("   matrix:")
    for row in matrix:
        print(f"      {row}")
    element = matrix[1][2]  # second row, third column
    print(f"   matrix[1][2] = {element}")
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
    print(f"   len(numbers) = {len(numbers)}")
    print(f"   max(numbers) = {max(numbers)}")
    print(f"   min(numbers) = {min(numbers)}")
    print(f"   sum(numbers) = {sum(numbers)}")
    print()

    # -------------------- Performance Tip: Building Lists Efficiently --------------------
    # Pre‑allocating a list of known size avoids multiple resizes during appends.
    # Create list with [0] * n (or any placeholder) then assign.
    # Time complexity: O(n) to create and fill.
    # Space complexity: O(n) for the final list.
    print("13. Performance Tip: Pre‑allocate if size known")
    n = 5
    arr = [0] * n                # allocate once
    for i in range(n):
        arr[i] = i * 2
    print(f"   built list of size {n}: {arr}")
    print()


if __name__ == "__main__":
    main()