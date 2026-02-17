"""
02 - Amortized Analysis (Beginner-Friendly)

🔹 Topic: Amortized Analysis

Amortized Analysis helps us understand the "average cost" of operations in a sequence,
even if some operations are occasionally expensive.

Think of it like this:
- Most operations are cheap (fast)
- Occasionally, one operation is expensive (slow)
- Amortized analysis tells us: "On average, each operation is still cheap!"

We'll see this with examples:
1️⃣ Dynamic array append (Python list)
2️⃣ Stack with multipush
3️⃣ Binary counter increment
"""

# -------------------------------------------------------------
# Example 1: Dynamic Array (Python list)
# -------------------------------------------------------------
print("Example 1: Dynamic Array Append\n")

# Python lists are dynamic arrays:
# - Appending is usually O(1) — very fast
# - Sometimes, the array resizes (copies all elements to a bigger array) → O(n)
# - Amortized analysis averages this out → still O(1) per append on average

dynamic_list = []

for i in range(1, 11):
    dynamic_list.append(i)
    print(f"Append {i}: Current List = {dynamic_list}")

print("""
Even though resizing may happen occasionally, each append is O(1) on average.
This is the essence of amortized analysis.
""")

# Visualizing how list resizes occasionally
print("Visualizing list resizing (capacity doubling):")

capacity = 1
elements = 0
while elements < 16:
    elements += 1
    if elements > capacity:
        print(f"Resize needed! Old Capacity: {capacity} → New Capacity: {capacity*2}")
        capacity *= 2
    else:
        print(f"Append {elements} (No resize)")

print("\nNotice: Most appends are fast, only a few cause resizing.")


# -------------------------------------------------------------
# Example 2: Stack with Multipush
# -------------------------------------------------------------
print("\nExample 2: Stack Multipush\n")

class Stack:
    def __init__(self):
        self.stack = []

    def push(self, val):
        self.stack.append(val)  # O(1)

    def multipush(self, vals):
        """
        Push multiple values at once.
        Each push is O(1), so total cost = O(k) for k elements
        Amortized cost per element = O(1)
        """
        for val in vals:
            self.push(val)
            print(f"Pushed {val}: {self.stack}")

# Using the stack
s = Stack()
s.multipush([10, 20, 30, 40, 50])

print("""
Even if we push multiple items at once, each push is O(1) on average.
This shows amortized cost is useful when doing batch operations.
""")


# -------------------------------------------------------------
# Example 3: Binary Counter Increment (Classic Interview Example)
# -------------------------------------------------------------
print("\nExample 3: Binary Counter Increment\n")

"""
Imagine a binary counter: 0b000, 0b001, 0b010, etc.
- Incrementing flips some bits.
- Sometimes flipping many bits at once looks expensive.
- But over many increments, average cost per increment = O(1) amortized.
"""

counter = [0, 0, 0]  # 3-bit counter, least significant bit first

def increment(counter):
    """
    Increment binary counter
    """
    i = 0
    while i < len(counter):
        if counter[i] == 0:
            counter[i] = 1
            break
        else:
            counter[i] = 0
            i += 1
    print(counter)

print("Binary counter increments:")
for _ in range(8):
    increment(counter)

print("""
Notice: Sometimes multiple bits flip (expensive), but average cost per increment
over many operations is still O(1). That's amortized analysis in action.
""")
