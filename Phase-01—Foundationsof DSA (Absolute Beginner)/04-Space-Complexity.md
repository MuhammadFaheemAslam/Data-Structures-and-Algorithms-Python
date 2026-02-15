# 📘 Space Complexity

---

# 📌 What is Space Complexity?

Space Complexity measures **how the memory usage of an algorithm grows as the input size increases**.

It does **NOT** measure memory in MB or GB directly.

Instead, it counts:

> How much extra memory (variables, data structures, function calls) the algorithm needs relative to input size (n).

---

# ❓ Why Measuring Memory in MB/GB is Wrong

Beginners often think:

> "Let me check how much RAM my program uses."

This is misleading because:

### 1️⃣ Different Systems → Different RAM Usage

* A program may use more memory on one system than another.
* OS memory management, garbage collection, and runtime differences affect memory.

---

### 2️⃣ Input Size Matters Most

Memory usage depends on:

* How many elements your algorithm stores
* How recursive calls are stacked
* Temporary data structures created

Example:

* Array of size 1,000 → memory usage is small
* Array of size 1,000,000 → memory usage grows significantly

---

# ✅ Machine-Independent Analysis

Instead of measuring MB:

* Count memory required in terms of input size **n**
* Count **variables, data structures, recursion stack space**

This is **space complexity analysis**.

---

# 📌 Components of Space Complexity

1. **Fixed Part**
   Memory that does **not depend on input size**:

   * Constants, fixed variables, program instructions

2. **Variable Part**
   Memory that **depends on input size**:

   * Arrays, lists, hash tables
   * Recursive call stack
   * Temporary data structures created during execution

---

# 📌 Common Space Complexities

---

# 🔹 O(1) — Constant Space

Memory does **not grow** with input size.

Example:

```python
def add_two_numbers(a, b):
    return a + b
```

* Only two variables `a` and `b`
* No extra memory proportional to input size

So space complexity = **O(1)**

---

# 🔹 O(n) — Linear Space

Memory grows linearly with input size.

Example:

```python
def create_list(n):
    arr = []
    for i in range(n):
        arr.append(i)
    return arr
```

* For `n` elements, we store `n` numbers → O(n) space

---

# 🔹 O(n²) — Quadratic Space

Memory grows proportional to **square of input size**.

Example:

```python
def create_matrix(n):
    matrix = []
    for i in range(n):
        row = []
        for j in range(n):
            row.append(i*j)
        matrix.append(row)
    return matrix
```

* n × n elements → **O(n²)** space

---

# 🔹 Recursive Call Stack

Recursion consumes memory on the **call stack**.

Example: Factorial

```python
def factorial(n):
    if n == 0:
        return 1
    return n * factorial(n-1)
```

* Stack depth = n → **O(n) space**
* Iterative factorial → **O(1) space**

---

# 🔹 O(log n) — Logarithmic Space

Occurs when recursion divides input in half.

Example: Binary Search (recursive)

```python
def binary_search(arr, target, low, high):
    if low > high:
        return -1
    mid = (low + high)//2
    if arr[mid] == target:
        return mid
    elif arr[mid] < target:
        return binary_search(arr, target, mid+1, high)
    else:
        return binary_search(arr, target, low, mid-1)
```

* Each recursive call reduces the search space by half
* Stack depth ≈ log n → **O(log n) space**

---

# 📊 Space Complexity Growth Comparison

| Complexity | Growth Rate          | Example                                    |
| ---------- | -------------------- | ------------------------------------------ |
| O(1)       | Flat                 | Fixed variables                            |
| O(log n)   | Very slow growth     | Recursive binary search                    |
| O(n)       | Moderate growth      | Storing array of n elements                |
| O(n log n) | Moderate-fast growth | Recursive merge sort (stack + temp arrays) |
| O(n²)      | Fast growth          | 2D matrices                                |
| O(2ⁿ)      | Explosive growth     | Recursive subsets / Fibonacci              |
| O(n!)      | Extremely explosive  | Brute-force permutations                   |

---

# 🧠 Why Space Complexity Matters

Ignoring memory usage can cause:

* Program crashes (OutOfMemory)
* Slow performance due to swapping
* Inefficient solutions for large inputs

Good engineers always ask:

> "How much memory will this algorithm need for large input?"

---

# 🏁 Final Thoughts

Space Complexity is about:

* Tracking memory usage
* Choosing memory-efficient algorithms
* Writing scalable solutions

It trains you to balance:

> "Fast enough?" vs "Memory efficient enough?"


