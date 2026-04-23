# Insertion Sort — Analysis

## The Algorithm in One Paragraph

Insertion sort builds the final sorted array ONE element at a time.
For each new element, it walks back through the already-sorted prefix,
shifting each larger element right to make room, and inserts the new
element at its correct position. It's how most people naturally sort
a hand of playing cards.

---

## Complexity

| Dimension                          | Insertion Sort |
|------------------------------------|----------------|
| Best case (sorted input)           | **O(n)**       |
| Average case                       | O(n²)          |
| Worst case (reverse sorted)        | O(n²)          |
| Space                              | O(1)           |
| Stable                             | **Yes**        |
| Adaptive                           | **Yes**        |
| Online                             | **Yes** — can sort data as it arrives |

Insertion sort is the **best of the O(n²) sorts** on every metric except
swap count:

- **Adaptive:** O(n) on already-sorted input, O(n·k) on arrays with
  k inversions (distance between actual position and sorted position).
- **Stable:** equal elements retain their input order.
- **Online:** when a new element arrives, insert it into the sorted
  prefix in O(n). No need to re-sort from scratch.

These properties make insertion sort the **base case inside Timsort**
— Python's built-in sorting algorithm uses insertion sort on any run
of ≤ 32 elements.

---

## Why It's Adaptive

Each outer-loop iteration shifts until it finds the key's correct
position. On already-sorted input, the key is always already in place,
so the inner `while` runs zero times. The total cost is O(n) — one
loop over the array doing a constant amount of work per element.

More precisely, the number of shift operations equals the number of
**inversions** in the input — pairs `(i, j)` with `i < j` but
`arr[i] > arr[j]`:

- Sorted array:    0 inversions → O(n)
- Reverse sorted:  n(n-1)/2 inversions → O(n²)
- Random input:    ~n²/4 inversions → O(n²)

---

## Why It's Used in Production (Timsort's Inner Loop)

Python's `list.sort()` is Timsort, a hybrid of merge sort and insertion
sort. It breaks the input into "runs" — already-sorted (or
reverse-sorted) subsequences — and merges them. For runs **shorter
than `MIN_RUN` (usually 32)**, Timsort calls insertion sort to
finish them.

Why? Three reasons insertion sort wins at small n:

1. **Cache friendliness.** Insertion sort only touches adjacent
   memory positions — every access is likely a cache hit.
2. **No recursion overhead.** Merge sort's recursive calls have
   fixed per-call costs (stack frames, function prologue/epilogue)
   that dominate at small n.
3. **Adaptive.** Small runs are often nearly-sorted already (because
   Timsort's run-finding step has already extracted ordered pieces
   from the input). Insertion sort exploits that.

So insertion sort is not just pedagogical — it's **actively used
every time you call `sorted()` in Python**.

---

## Counting Operations

For an array of `n` elements with `I` inversions:

| Quantity              | Best   | Average       | Worst   |
|-----------------------|--------|---------------|---------|
| Comparisons           | n − 1  | ~n²/4         | n(n-1)/2|
| Shifts                | 0      | ~n²/4         | n(n-1)/2|
| Total work            | O(n)   | O(n + I)      | O(n²)   |

The "O(n + I)" bound is the classic adaptive result. If the input is
nearly sorted (I is small), insertion sort is nearly O(n).

---

## Binary Insertion Sort — A Small Tweak

Using binary search to find the insertion point drops the comparisons
to O(log n) per element — total **O(n log n) comparisons**. But the
shifts are still O(n²).

| Variant              | Comparisons  | Shifts    | Useful when           |
|----------------------|--------------|-----------|------------------------|
| Insertion Sort       | O(n²)        | O(n²)     | Standard version       |
| Binary Insertion     | **O(n log n)** | O(n²)   | Comparisons expensive  |

Binary insertion sort shines when comparisons are MUCH more expensive
than assignments — e.g., sorting records with complex custom `__lt__`
methods, or string comparisons with long common prefixes.

See `binary-insertion.py` for the implementation.

---

## Insertion Sort vs Bubble vs Selection

| Property           | Bubble     | Selection | Insertion    |
|--------------------|------------|-----------|--------------|
| Best case          | O(n) w/ opt| O(n²)     | **O(n)**     |
| Average            | O(n²)      | O(n²)     | O(n²)        |
| Worst              | O(n²)      | O(n²)     | O(n²)        |
| Stable             | Yes        | No        | Yes          |
| Adaptive           | With opt   | No        | **Yes**      |
| Comparisons (avg)  | ~n²/2      | n(n-1)/2  | **~n²/4**    |
| Swaps/moves (avg)  | ~n²/4      | **n − 1** | ~n²/4 moves  |
| In place           | Yes        | Yes       | Yes          |
| Online             | No         | No        | **Yes**      |

Insertion sort **wins on adaptivity, stability, online-ness, and
average-case comparisons.** Selection sort wins only on swap count.
Bubble sort wins on… nothing practical, really.

If you must pick an O(n²) sort, pick insertion sort — except when
swap cost dominates, in which case pick selection sort.

---

## Pitfalls

- **Using `>=` instead of `>`:** breaks stability.
- **Off-by-one on the while loop:** `j >= 0` is the guard against
  walking off the left end.
- **Shifting instead of swapping:** use the shift-based version
  (`arr[j + 1] = arr[j]`); the swap-based version does twice the
  memory writes for the same result.
- **Over-applying to large n:** insertion sort is O(n²). Past n ≈ 50
  it's dramatically slower than Timsort. Know when to switch.

---

## Shell Sort — An Interesting Descendant

Shell sort is insertion sort at MULTIPLE GAPS. Starting with a large
gap (e.g., n/2), do insertion sort on the elements `gap` apart. Then
shrink the gap (n/4, n/8, ...) and repeat. The final gap-1 pass is
ordinary insertion sort, by which time the array is already "almost
sorted" → O(n) in that last pass.

Complexity depends on the gap sequence — Sedgewick's gives O(n^(4/3)),
Pratt's gives O(n·log² n). Still not O(n log n), but a massive
improvement over plain insertion sort.

Shell sort is occasionally used in embedded systems where Timsort's
memory footprint is too large. Rare in modern software.

---

## Key Takeaways

1. **Insertion sort is O(n²) worst, O(n) best — adaptive.**
2. **Stable, in-place, online.** Best O(n²) sort on every axis except
   swap count (selection wins there).
3. **Used in production** as Timsort's base case for small subarrays.
   Not purely pedagogical.
4. **Best for:**
   - Tiny arrays (n ≤ 16)
   - Nearly-sorted arrays
   - Online / streaming input
5. **Switch to O(n log n) sorts past n ≈ 50.**
