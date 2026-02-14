# 📘 Time Complexity

---

# 📌 What is Time Complexity?

Time Complexity measures **how the running time of an algorithm grows as the input size increases**.

It does **NOT** measure time in seconds.

Instead, it measures:

> How the number of operations grows relative to input size (n).

---

# ❓ Why Measuring Time in Seconds is Wrong

Many beginners think:

> "Let me run the program and check how many seconds it takes."

That approach is incorrect because:

### 1️⃣ Different Computers → Different Speeds

* A high-end machine runs faster
* A slower machine runs slower

Same code → different execution time.

---

### 2️⃣ Background Processes Affect Time

Your system might be:

* Running Chrome
* Downloading files
* Running other apps

This changes execution time.

---

### 3️⃣ Input Size Changes Everything

If an algorithm takes:

* 0.01 seconds for 100 elements
* It might take 10 seconds for 1,000,000 elements

Time in seconds does not explain scalability.

---

# ✅ Machine-Independent Analysis

Instead of measuring seconds, we count:

* Number of operations
* Number of steps

This makes analysis:

* Independent of hardware
* Independent of programming language
* Independent of system speed

This method is called **asymptotic analysis**.

---

# 📌 What is Input Size (n)?

In most problems:

* **n = number of elements in input**

Examples:

* Array of size 10 → n = 10
* String length 50 → n = 50
* Graph with 100 nodes → n = 100

We analyze how the algorithm behaves when **n becomes very large**.

---

# 📌 Common Time Complexities

Let’s understand the most important ones.

---

# 🔹 O(1) — Constant Time

Execution time does NOT change with input size.

Example:

```python
arr = [10, 20, 30, 40]
print(arr[0])
```

No matter how big the array is, accessing an index takes constant time.

So this is:

> O(1)

---

# 🔹 O(n) — Linear Time

Time increases linearly with input size.

Example:

```python
for i in range(n):
    print(i)
```

---

## 🔍 Step-by-Step Explanation

Let’s assume:

```
n = 5
```

The loop runs:

```
i = 0
i = 1
i = 2
i = 3
i = 4
```

It runs 5 times.

If:

```
n = 100
```

The loop runs 100 times.

If:

```
n = 1,000,000
```

The loop runs 1,000,000 times.

So the number of operations is directly proportional to n.

That means:

> T(n) = n

So complexity = **O(n)**

---

# 🔹 O(n²) — Quadratic Time

Occurs when we use nested loops.

Example:

```python
for i in range(n):
    for j in range(n):
        print(i, j)
```

---

## 🔍 Step-by-Step Explanation

If:

```
n = 3
```

Outer loop runs 3 times.

For each outer iteration, inner loop runs 3 times.

Total executions:

```
3 × 3 = 9
```

If:

```
n = 100
```

Total operations:

```
100 × 100 = 10,000
```

So:

> T(n) = n × n = n²

That’s why it’s **O(n²)**.

Quadratic growth increases very fast.

---

# 🔹 O(log n) — Logarithmic Time

Occurs when we divide the problem in half repeatedly.

Example: Binary Search

Each step cuts the search space in half.

If n = 1,000,000:

We divide:

1,000,000
500,000
250,000
125,000
...

After about 20 steps, we reach 1 element.

So instead of checking 1 million elements, we check about 20.

That is:

> O(log n)

Very efficient.

---

# 🔹 O(2ⁿ) — Exponential Time

Usually appears in recursion problems like naive Fibonacci.

Example:

```python
def fib(n):
    if n <= 1:
        return n
    return fib(n-1) + fib(n-2)
```

This function recomputes values many times.

If:

```
n = 5 → small
n = 40 → extremely slow
```

Because number of calls grows exponentially.

That is:

> O(2ⁿ)

Very inefficient for large inputs.

---

# 📊 Growth Comparison

As n increases:

* O(1) → Constant Time
* O(log n) → Logaritmic Time
* O(n) → Linear Time
* O(n log n) → Linearithmic Time
* O(n²) → Quadratic Time
* O(2ⁿ) → Exponential Time
* O(2ⁿ) → Factorial Time

| Complexity | Growth Rate          | Example                   |
| ---------- | -------------------- | ------------------------- |
| O(1)       | Flat             | Array access              |
| O(log n)   | Very slow growth     | Binary search             |
| O(n)       | Moderate growth      | Linear iteration          |
| O(n log n) | Moderate-fast growth | Merge Sort, Heap Sort     |
| O(n²)      | Fast growth          | Bubble Sort, Nested loops |
| O(n³)      | Very fast growth     | Triple loops              |
| O(2ⁿ)      | Explosive growth     | Recursive DFS, Fibonacci  |
| O(n!)      | Extremely explosive  | Brute-force permutations  |

---

Understanding this growth behavior is the key to writing efficient algorithms.

---

# 📌 Important Rule in Big O

We ignore:

* Constants
* Lower-order terms

Example:

```
T(n) = 5n + 10
```

In Big O:

```
O(n)
```

Because for large n, constants don’t matter.

---

# 🧠 Why Time Complexity Matters

Without analyzing complexity:

* Your code may work for small inputs
* But fail for large inputs
* Or timeout in interviews
* Or crash production systems

Good engineers always think:

> "How will this scale?"

---

# 🏁 Final Thoughts

Time Complexity is about:

* Measuring growth
* Analyzing scalability
* Writing efficient solutions

It trains you to think beyond:

> "Does this work?"

And instead ask:

> "Is this optimal?"

