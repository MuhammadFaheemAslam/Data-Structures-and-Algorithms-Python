# 03 Time Complexity

Welcome to a deep dive into **Time Complexity**! In this file, we'll explore what time complexity really means, why measuring seconds is misleading, and how to analyse the efficiency of your code using Big O notation. By the end, you'll be able to look at any algorithm and estimate how its runtime grows with input size.

---

## 📌 What is Time Complexity?

Time complexity measures **how the running time of an algorithm increases as the size of the input grows**.

It does **not** measure actual seconds or milliseconds. Instead, it counts the **number of operations** (or steps) an algorithm performs relative to the input size (usually denoted as `n`).

This allows us to compare algorithms independently of the computer’s speed, programming language, or background processes.

---

## ❓ Why Measuring Time in Seconds is Wrong

Beginners often think: *"I'll just run the program and see how many seconds it takes."*  
That approach fails for several reasons:

1. **Different computers → different speeds**  
   A high‑end machine runs faster than an old laptop, so the same code will give different timings.

2. **Background processes affect time**  
   If your system is busy downloading files or running other apps, execution time will vary.

3. **Input size changes everything**  
   An algorithm might take 0.01 seconds for 100 elements, but 10 seconds for 1,000,000 elements.  
   A single time measurement doesn’t tell you how it scales.

**Solution:** Count operations. This method is called **asymptotic analysis** – it’s independent of hardware and language.

---

## 🔢 What is Input Size (n)?

In most problems, **n** represents the size of the input. For example:

- An array of 10 numbers → `n = 10`
- A string of length 50 → `n = 50`
- A graph with 100 nodes → `n = 100`

We analyse how the number of operations grows as `n` becomes very large.

---

## 🧮 Detailed Explanations of Common Time Complexities

Let’s explore each important complexity class with step‑by‑step breakdowns, just like the O(n) example you liked.

---

### 🔹 O(1) – Constant Time

**Execution time does NOT change with input size.**  
The algorithm always performs the same number of operations, no matter how big `n` is.

**Example: Accessing an array element by index**
```python
arr = [10, 20, 30, 40]
print(arr[0])   # always one operation
```

#### 🔍 Step‑by‑Step Explanation

- The operation `arr[0]` directly fetches the element at index 0.
- It doesn’t matter if the array has 5 elements or 5 million elements – the time to access a specific index is the same.
- There is **no loop**, no dependence on `n`.

If we count operations:

- For `n = 5` → 1 operation
- For `n = 1000` → 1 operation
- For `n = 1,000,000` → 1 operation

So the number of operations is always constant.  
That means:

> T(n) = 1

Thus, complexity = **O(1)**.

---

### 🔹 O(log n) – Logarithmic Time

The algorithm reduces the problem size by a constant factor at each step.  
Common in divide‑and‑conquer approaches (e.g., binary search).

**Example: Binary search in a sorted array**
```python
def binary_search(arr, target):
    left, right = 0, len(arr) - 1
    while left <= right:
        mid = (left + right) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return -1
```

#### 🔍 Step‑by‑Step Explanation

Let’s trace through an example.

Assume we have a sorted array of size `n = 16` and we are searching for a target.  
At each step, we compare the middle element and then eliminate **half** of the remaining elements.

- **Step 1:** We look at the middle of 16 elements → 1 comparison. Remaining 8 elements.
- **Step 2:** Middle of 8 → 1 more comparison. Remaining 4.
- **Step 3:** Middle of 4 → 1 more. Remaining 2.
- **Step 4:** Middle of 2 → 1 more. Remaining 1.
- **Step 5:** Last element → 1 more. Done.

Total comparisons = 5.

Notice that 2⁵ = 32, which is slightly more than 16. In fact, for an array of size `n`, the maximum number of comparisons is about `log₂(n)`.

If `n = 16`, log₂(16) = 4, but we did 5 comparisons in the worst case (because of the loop condition). In Big O, we ignore such small differences.

Now generalise:

- `n = 16` → about 4–5 steps
- `n = 1024` → about 10 steps (2¹⁰ = 1024)
- `n = 1,000,000` → about 20 steps (2²⁰ ≈ 1 million)

So the number of operations grows very slowly.  
That means:

> T(n) ≈ log₂(n)

Thus, complexity = **O(log n)**.

---

### 🔹 O(n) – Linear Time

Runtime grows proportionally to the input size.  
A single loop that processes each element once is O(n).

**Example: Finding the maximum value**
```python
def find_max(arr):
    max_val = arr[0]
    for num in arr:
        if num > max_val:
            max_val = num
    return max_val
```

#### 🔍 Step‑by‑Step Explanation

Let’s assume the array has `n` elements.

- We initialise `max_val` with the first element (1 operation, but constant, so we ignore it for large n).
- Then the loop runs once for each element.

If `n = 5`, the loop runs 5 times (for indices 0 to 4).  
If `n = 100`, it runs 100 times.  
If `n = 1,000,000`, it runs 1,000,000 times.

The number of iterations is exactly `n`. Inside each iteration we do a constant amount of work (a comparison and maybe an assignment).

So the total number of operations is directly proportional to `n`.  
That means:

> T(n) = n

Thus, complexity = **O(n)**.

---

### 🔹 O(n log n) – Linearithmic Time

Slightly worse than linear, but still efficient for large datasets.  
Appears in optimal sorting algorithms like merge sort, heapsort.

**Example: Merge sort (simplified)**
```python
def merge_sort(arr):
    if len(arr) <= 1:
        return arr
    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    return merge(left, right)
```

#### 🔍 Step‑by‑Step Explanation

Merge sort divides the array into halves recursively until each subarray has one element. Then it merges them back together in sorted order.

- **Division:** How many times can we split an array of size `n` in half?  
  That’s `log₂(n)` levels.  
  For example, `n = 8` → split into 4, then 2, then 1 → 3 levels (log₂8 = 3).

- **Merging:** At each level, we merge all subarrays. Merging two sorted arrays of total size `k` takes O(k) operations.  
  Across one entire level, the total size of all merges is `n` (because every element is processed exactly once per level).

So we have `log n` levels, each doing O(n) work.  
Total work = `n * log n`.

Let’s verify with small `n`:

- `n = 8` → log₂8 = 3 levels → operations ≈ 8 × 3 = 24
- `n = 16` → 4 levels → 64 operations
- `n = 1024` → 10 levels → 10,240 operations

The growth is slightly more than linear but much less than quadratic.

Thus, complexity = **O(n log n)**.

---

### 🔹 O(n²) – Quadratic Time

Often comes from nested loops where each loop runs about `n` times.  
These algorithms become very slow for large inputs.

**Example: Printing all pairs**
```python
def print_pairs(arr):
    for i in range(len(arr)):
        for j in range(len(arr)):
            print(arr[i], arr[j])
```

#### 🔍 Step‑by‑Step Explanation

Assume `n = len(arr)`.

- The outer loop runs `n` times (once for each `i`).
- For each outer iteration, the inner loop also runs `n` times (once for each `j`).

So total iterations = `n × n = n²`.

If `n = 3`, outer runs 3 times, inner runs 3 times each → 9 prints.  
If `n = 10`, outer runs 10, inner runs 10 each → 100 prints.  
If `n = 100`, we get 10,000 prints.

The number of operations grows with the square of `n`.  
That means:

> T(n) = n²

Thus, complexity = **O(n²)**.

---

### 🔹 O(2ⁿ) – Exponential Time

Runtime doubles with each additional input element.  
Common in naive recursive algorithms that solve a problem of size `n` by solving two problems of size `n-1`.

**Example: Naive Fibonacci**
```python
def fib(n):
    if n <= 1:
        return n
    return fib(n - 1) + fib(n - 2)
```

#### 🔍 Step‑by‑Step Explanation

Let’s trace the recursion for `fib(5)`:

```
fib(5)
├── fib(4)
│   ├── fib(3)
│   │   ├── fib(2)
│   │   │   ├── fib(1)
│   │   │   └── fib(0)
│   │   └── fib(1)
│   └── fib(2)
│       ├── fib(1)
│       └── fib(0)
└── fib(3)
    ├── fib(2)
    │   ├── fib(1)
    │   └── fib(0)
    └── fib(1)
```

Count the calls:

- `fib(5)` calls `fib(4)` and `fib(3)` (2 calls)
- `fib(4)` calls `fib(3)` and `fib(2)` (2 more)
- and so on.

The recursion tree grows rapidly. In fact, for `fib(n)`, the number of calls is roughly `2ⁿ` (specifically, it’s about 1.618ⁿ, but we round to 2ⁿ for Big O).

If `n = 5`, we have about 15 calls.  
If `n = 10`, calls jump to about 177.  
If `n = 20`, calls exceed 20,000.  
If `n = 50`, the number of calls is astronomical (over 2⁵⁰ ≈ 1.1 × 10¹⁵).

Thus, the growth is explosive.  
That means:

> T(n) ≈ 2ⁿ

So complexity = **O(2ⁿ)**.

---

### 🔹 O(n!) – Factorial Time

Even worse than exponential. Appears in algorithms that generate all permutations of a set.

**Example: Generating all permutations of a string**
```python
def permutations(s):
    if len(s) == 1:
        return [s]
    perms = []
    for i, char in enumerate(s):
        for perm in permutations(s[:i] + s[i+1:]):
            perms.append(char + perm)
    return perms
```

#### 🔍 Step‑by‑Step Explanation

For a string of length `n`, the number of permutations is `n!` (n factorial).  
That means:

- `n = 3` → 3! = 6 permutations
- `n = 4` → 4! = 24 permutations
- `n = 5` → 5! = 120 permutations
- `n = 10` → 10! = 3,628,800 permutations
- `n = 20` → 20! ≈ 2.43 × 10¹⁸ – unimaginable.

The algorithm must generate each permutation, so the number of operations is at least proportional to `n!`.  
Thus, complexity = **O(n!)**.

---

## 📊 Growth Comparison Table

| Complexity | Name              | Growth Rate                     | Example                     |
|------------|-------------------|---------------------------------|-----------------------------|
| O(1)       | Constant          | Flat                            | Array access                |
| O(log n)   | Logarithmic       | Very slow increase              | Binary search               |
| O(n)       | Linear            | Increases steadily with n       | Linear search               |
| O(n log n) | Linearithmic      | Slightly faster than linear     | Merge sort, heap sort       |
| O(n²)      | Quadratic         | Increases rapidly               | Nested loops, bubble sort   |
| O(2ⁿ)      | Exponential       | Explodes – doubles with each n  | Naive Fibonacci             |
| O(n!)      | Factorial         | Extremely explosive             | Generating all permutations |

As `n` grows, the differences become huge. For `n = 100`:

- O(1) = 1 operation
- O(log n) ≈ 7 operations
- O(n) = 100 operations
- O(n log n) ≈ 664 operations
- O(n²) = 10,000 operations
- O(2ⁿ) ≈ 1.27 × 10³⁰ operations – impossible!

---

## 📝 Best, Average, and Worst Case

Time complexity is usually expressed for the **worst case**, but we can also consider:

- **Best case**: minimum time for any input of size `n`.
- **Average case**: expected time over all possible inputs.
- **Worst case**: maximum time.

**Example: Linear search in an unsorted array**
```python
def linear_search(arr, target):
    for i, val in enumerate(arr):
        if val == target:
            return i
    return -1
```
- Best case: O(1) – the target is the first element.
- Worst case: O(n) – the target is last or not present.
- Average case: O(n) – on average, we check half the elements.

When we say “an algorithm is O(n)”, we usually mean the worst‑case complexity.

---

## 🧠 Rules of Big O Analysis

1. **Drop constants**  
   If an algorithm does `5n` operations, we write O(n), not O(5n). Constant factors don’t matter for large n.

2. **Keep only the dominant term**  
   If the operation count is `n² + 3n + 100`, we write O(n²). For large n, the lower‑order terms become insignificant.

**Example:**
```python
def example(arr):
    total = 0                     # O(1)
    for x in arr:                 # O(n)
        total += x
    for i in range(len(arr)):     # O(n²)
        for j in range(len(arr)):
            print(i, j)
    return total
```
Total = O(1) + O(n) + O(n²) = **O(n²)**.

---

## ❓ Why Time Complexity Matters

- **Scalability**: Your code might work for small inputs but fail with large data (e.g., time out in contests or production).
- **Algorithm choice**: Time complexity helps you pick the right algorithm for the job.
- **Interview essential**: Almost every technical interview asks you to analyse the efficiency of your solution.
- **Professional mindset**: Good engineers always think: *“How will this scale?”*

---

## 🏁 Final Thoughts

Time complexity is not about exact running times – it’s about **growth rates**.  
It trains you to think beyond “does it work?” and ask **“is it optimal?”**

Now that you understand the theory, you’re ready to analyse any algorithm you write. In the next file, we’ll look at **Space Complexity** – the other side of the efficiency coin.

Happy coding!