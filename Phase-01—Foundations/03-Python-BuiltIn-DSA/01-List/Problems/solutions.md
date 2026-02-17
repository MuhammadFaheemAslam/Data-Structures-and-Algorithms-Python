# 🧠 Solutions Explanation – Easy Problems (List)

This file explains the logic behind each easy problem step-by-step.

---

# ✅ Problem 01 – Find Maximum and Minimum

## 🔹 Problem Recap

Given a list of numbers, return:
- Maximum value
- Minimum value

Example:
[3, 5, 1, 9, 2]

Output:
Maximum = 9
Minimum = 1

---

## 🔹 Approach 1 – Built-in Functions

Python provides:

- max(list)
- min(list)

These functions scan the entire list once.

Time Complexity: O(n)  
Because Python checks every element.

---

## 🔹 Approach 2 – Manual Traversal (Important for Interviews)

### Step-by-step logic:

1. Assume first element is both max and min.
2. Start checking from second element.
3. Compare each number:
   - If greater → update max
   - If smaller → update min
4. Return both values.

Why start from second element?

Because we already assumed the first element as initial max & min.

---

## 🔹 Why This Problem Is Important

This problem teaches:

- Iteration
- Comparison logic
- Handling edge cases
- Time complexity basics

It is one of the most asked beginner interview questions.

---

# ✅ Problem 02 – Rotate a List

## 🔹 Problem Recap

Rotate a list by k positions.

Example:
[1, 2, 3, 4, 5]
k = 2

Left Rotation:
[3, 4, 5, 1, 2]

Right Rotation:
[4, 5, 1, 2, 3]

---

# 🔹 Understanding Rotation Visually

Original:
1  2  3  4  5

Left Rotate by 2:
Move first 2 elements to the end

[1, 2] + [3, 4, 5]
↓
[3, 4, 5] + [1, 2]

---

# 🔹 Why k % n ?

If list size = 5

Rotate by 7 positions:
7 % 5 = 2

Rotating 7 times is same as rotating 2 times.

This prevents unnecessary rotations.

---

# 🔹 Approach 1 – Slicing (Recommended)

Left Rotation:
arr[k:] + arr[:k]

Right Rotation:
arr[-k:] + arr[:-k]

Time Complexity: O(n)  
Space Complexity: O(n)

---

# 🔹 Approach 2 – Brute Force

Rotate one step at a time.

If k = 3:
Repeat 3 times:
- Remove first element
- Add it to end

Time Complexity: O(n × k)

Not recommended for large k.

---

# 🔥 Key Interview Takeaway

Always compare approaches.

Better:
O(n)

Avoid:
O(n × k)

---

# 🎯 Practice Questions

1. Rotate list without using slicing.
2. Rotate list in-place.
3. Rotate negative numbers.
4. Rotate 2D list (matrix).

