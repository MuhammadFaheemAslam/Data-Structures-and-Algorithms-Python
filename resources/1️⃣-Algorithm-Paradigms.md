# 1️⃣ Algorithm Paradigms - Core Thinking Models

*Your mental framework for approaching any coding problem*

---

## 🎯 What Are Algorithm Paradigms?

Algorithm paradigms are fundamental approaches or mental models for solving problems. Think of them as "problem-solving strategies" or "thinking frameworks" that guide how you structure your solution. Just as a carpenter has different tools for different jobs, a programmer has different paradigms for different types of problems.

---

## 📋 The 7 Essential Paradigms

### 1. 🔨 **Brute Force**
*"Try all possibilities"*

#### 🤔 **Mental Model**
When you're stuck, start here. Generate every possible solution and check each one until you find the correct answer. It's like trying every key on a keychain to open a door.

#### 🎯 **When to Use**
- Problem size is small (n ≤ 10-15 for exponential, n ≤ 1000 for O(n²))
- As a baseline solution before optimization
- When no better approach exists
- To verify correctness of optimized solutions

#### 🧠 **Recognition Patterns**
- "Find all possible combinations..."
- "Check every pair..."
- "Generate all subsets..."
- "Try all possibilities..."

#### 💻 **Template**
```python
def brute_force_solution(data):
    # Generate all possibilities
    for possibility in generate_all_possibilities(data):
        # Check if it's valid
        if is_valid(possibility):
            return possibility
    return None

# Example: Two Sum - Find all pairs
def two_sum_brute_force(nums, target):
    n = len(nums)
    for i in range(n):
        for j in range(i + 1, n):
            if nums[i] + nums[j] == target:
                return [i, j]
    return []
```

#### ⚖️ **Complexity**
- **Time:** Usually exponential or polynomial (O(n!), O(2ⁿ), O(n²))
- **Space:** Usually O(1) or O(n)

#### 📊 **Pros & Cons**
| ✅ Pros | ❌ Cons |
|--------|--------|
| Always works | Extremely slow for large inputs |
| Simple to implement | Often impractical |
| No special cases | Wastes computational resources |
| Great for small inputs | May time out in interviews |

#### 🎯 **Classic Problems**
- Two Sum (naive approach)
- String matching (naive)
- Generating all permutations
- Traveling Salesman (naive)

---

### 2. ✂️ **Divide & Conquer**
*"Break into smaller pieces, solve each, combine results"*

#### 🤔 **Mental Model**
Like solving a giant puzzle by breaking it into smaller sections, solving each section, then putting them together. If a problem is too big to solve directly, split it until it's manageable.

#### 🎯 **When to Use**
- Problem can be divided into independent subproblems
- Results can be combined efficiently
- Recursive structure is natural
- Looking for O(n log n) solutions

#### 🧠 **Recognition Patterns**
- "Divide the array into halves..."
- "Recursively solve left and right..."
- "Merge sorted lists..."
- "Find in rotated array..."

#### 💻 **Template**
```python
def divide_and_conquer(problem):
    # Base case: if problem is small enough
    if is_trivial(problem):
        return solve_directly(problem)
    
    # 1. DIVIDE: Break into smaller subproblems
    subproblems = split_into_smaller_parts(problem)
    
    # 2. CONQUER: Solve each subproblem recursively
    subresults = []
    for subproblem in subproblems:
        subresult = divide_and_conquer(subproblem)
        subresults.append(subresult)
    
    # 3. COMBINE: Merge results
    return combine_results(subresults)

# Example: Merge Sort
def merge_sort(arr):
    # Base case
    if len(arr) <= 1:
        return arr
    
    # 1. DIVIDE
    mid = len(arr) // 2
    left = arr[:mid]
    right = arr[mid:]
    
    # 2. CONQUER
    left = merge_sort(left)
    right = merge_sort(right)
    
    # 3. COMBINE
    return merge(left, right)

def merge(left, right):
    result = []
    i = j = 0
    
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    
    result.extend(left[i:])
    result.extend(right[j:])
    return result
```

#### ⚖️ **Complexity**
- **Time:** Usually O(n log n) or O(n)
- **Space:** Usually O(log n) to O(n) due to recursion

#### 📊 **Pros & Cons**
| ✅ Pros | ❌ Cons |
|--------|--------|
| Highly efficient for large data | Recursion overhead |
| Naturally parallelizable | May use extra memory |
| Often leads to O(n log n) solutions | Not always intuitive |
| Great for sorted data problems | Stack overflow risk |

#### 🎯 **Classic Problems**
- Merge Sort, Quick Sort
- Binary Search
- Maximum subarray sum (Kadane's variant)
- Closest pair of points
- Strassen's matrix multiplication

---

### 3. 💰 **Greedy**
*"Make the best choice right now, hope it leads to optimal solution"*

#### 🤔 **Mental Model**
Like choosing the largest piece of cake first, hoping that making the best choice at each step leads to the best overall outcome. No regrets, no looking back!

#### 🎯 **When to Use**
- Local optimum leads to global optimum
- Problem has optimal substructure
- Need efficient, often O(n) or O(n log n) solutions
- Decision problems with clear "best" at each step

#### 🧠 **Recognition Patterns**
- "Minimum number of coins..."
- "Maximum profit..."
- "Schedule as many as possible..."
- "Always pick the largest/smallest..."

#### 💻 **Template**
```python
def greedy_solution(items):
    # Sort if needed (common in greedy)
    items = sort_by_criteria(items)
    
    result = []
    remaining_capacity = initial_capacity
    
    for item in items:
        # At each step, make the locally optimal choice
        if can_take(item, remaining_capacity):
            result.append(item)
            remaining_capacity -= item.cost
            
        if solution_complete(result):
            break
    
    return result

# Example: Coin Change (minimum coins)
def coin_change_greedy(coins, amount):
    # Greedy works for standard currencies (USD, EUR)
    coins.sort(reverse=True)  # Sort descending
    count = 0
    
    for coin in coins:
        if amount == 0:
            break
        # Take as many of this coin as possible
        num_coins = amount // coin
        count += num_coins
        amount -= num_coins * coin
    
    return count if amount == 0 else -1
```

#### ⚖️ **Complexity**
- **Time:** Usually O(n log n) due to sorting, or O(n)
- **Space:** Usually O(1)

#### 📊 **Pros & Cons**
| ✅ Pros | ❌ Cons |
|--------|--------|
| Very fast and efficient | Doesn't always give optimal solution |
| Simple to implement | Requires proof of correctness |
| Intuitive approach | Can't handle complex constraints |
| Great for optimization | No way to correct wrong choices |

#### 🎯 **Classic Problems**
- Activity Selection
- Huffman Coding
- Dijkstra's Algorithm
- Fractional Knapsack
- Job Sequencing with Deadlines

---

### 4. 📊 **Dynamic Programming**
*"Remember past results to avoid recomputation"*

#### 🤔 **Mental Model**
Like solving a complex math problem by building from simple cases upward, writing down each result so you never have to calculate it again. "Those who cannot remember the past are condemned to repeat it."

#### 🎯 **When to Use**
- Overlapping subproblems (same subproblem appears multiple times)
- Optimal substructure (optimal solution contains optimal subsolutions)
- Need to optimize (min/max) or count
- Decision problems with multiple choices

#### 🧠 **Recognition Patterns**
- "Find maximum/minimum way to..."
- "Count number of ways to..."
- "Longest/shortest sequence..."
- "Knapsack/backpack problems"
- "Edit distance"
- "Subset sum"

#### 💻 **Templates**

**Top-Down (Memoization):**
```python
def dp_top_down(problem):
    memo = {}  # Cache results
    
    def solve(state):
        # Check if already solved
        if state in memo:
            return memo[state]
        
        # Base case
        if is_base_case(state):
            return base_value
        
        # Recursive case with memoization
        result = combine(
            solve(next_state1),
            solve(next_state2)
        )
        
        # Store before returning
        memo[state] = result
        return result
    
    return solve(initial_state)

# Example: Fibonacci with memoization
def fib(n):
    memo = {0: 0, 1: 1}
    
    def solve(k):
        if k in memo:
            return memo[k]
        
        memo[k] = solve(k-1) + solve(k-2)
        return memo[k]
    
    return solve(n)
```

**Bottom-Up (Tabulation):**
```python
def dp_bottom_up(problem_size):
    # Create DP table
    dp = [[0] * (size + 1) for _ in range(problem_size + 1)]
    
    # Fill base cases
    initialize_base_cases(dp)
    
    # Fill table in order
    for i in range(1, problem_size + 1):
        for j in range(1, capacity + 1):
            # Transition: use previously computed values
            dp[i][j] = max(
                dp[i-1][j],  # Skip current
                dp[i-1][j-w[i]] + v[i] if j >= w[i] else 0  # Take current
            )
    
    return dp[problem_size][capacity]

# Example: 0/1 Knapsack
def knapsack(weights, values, capacity):
    n = len(weights)
    dp = [[0] * (capacity + 1) for _ in range(n + 1)]
    
    for i in range(1, n + 1):
        for w in range(1, capacity + 1):
            if weights[i-1] <= w:
                dp[i][w] = max(
                    values[i-1] + dp[i-1][w - weights[i-1]],
                    dp[i-1][w]
                )
            else:
                dp[i][w] = dp[i-1][w]
    
    return dp[n][capacity]
```

#### ⚖️ **Complexity**
- **Time:** Usually polynomial (O(n²), O(n×m))
- **Space:** Usually O(n) to O(n²)

#### 📊 **Pros & Cons**
| ✅ Pros | ❌ Cons |
|--------|--------|
| Optimal solution guaranteed | Can be hard to identify pattern |
| Avoids recomputation | May use significant memory |
| Handles complex constraints | Complex to debug |
| Great for optimization | State definition is crucial |

#### 🎯 **Classic Problems**
- 0/1 Knapsack
- Longest Common Subsequence
- Longest Increasing Subsequence
- Matrix Chain Multiplication
- Edit Distance
- Coin Change (minimum coins)

---

### 5. 🔙 **Backtracking**
*"Explore all paths, backtrack when stuck"*

#### 🤔 **Mental Model**
Like solving a maze: try a path, if it leads to a dead end, go back to the last junction and try another path. Explore systematically, retreat when necessary.

#### 🎯 **When to Use**
- Need to find ALL solutions
- Need to find ONE valid solution under constraints
- Decision problems with multiple choices
- Constraint satisfaction problems
- When brute force is too slow but you need completeness

#### 🧠 **Recognition Patterns**
- "Find all possible arrangements..."
- "Generate all permutations/combinations..."
- "Solve this puzzle (Sudoku, N-Queens)..."
- "Check if path exists..."
- "Print all paths..."

#### 💻 **Template**
```python
def backtracking_solution(problem):
    result = []
    
    def backtrack(current_solution, choices_left):
        # If current solution is complete
        if is_complete(current_solution):
            result.append(current_solution.copy())
            return
        
        # Try all possible choices
        for choice in get_next_choices(choices_left):
            # Prune invalid paths early
            if is_valid_choice(current_solution, choice):
                # 1. MAKE CHOICE
                current_solution.append(choice)
                
                # 2. EXPLORE FURTHER
                backtrack(current_solution, choices_left - {choice})
                
                # 3. UNDO CHOICE (BACKTRACK)
                current_solution.pop()
    
    backtrack([], initial_choices)
    return result

# Example: Generate all permutations
def permutations(nums):
    result = []
    
    def backtrack(current, remaining):
        # Base case: permutation complete
        if not remaining:
            result.append(current.copy())
            return
        
        # Try each remaining number
        for i in range(len(remaining)):
            # Make choice
            current.append(remaining[i])
            
            # Explore with remaining numbers
            backtrack(current, remaining[:i] + remaining[i+1:])
            
            # Undo choice
            current.pop()
    
    backtrack([], nums)
    return result

# Example: N-Queens
def solve_n_queens(n):
    result = []
    
    def is_safe(board, row, col):
        # Check column
        for i in range(row):
            if board[i] == col:
                return False
        
        # Check diagonals
        for i in range(row):
            if abs(board[i] - col) == abs(i - row):
                return False
        
        return True
    
    def backtrack(board, row):
        if row == n:
            # Found a valid configuration
            result.append(board.copy())
            return
        
        for col in range(n):
            if is_safe(board, row, col):
                board[row] = col  # Place queen
                backtrack(board, row + 1)
                # No need to explicitly undo since we overwrite
    
    backtrack([-1] * n, 0)
    return result
```

#### ⚖️ **Complexity**
- **Time:** Usually exponential (O(2ⁿ), O(n!))
- **Space:** Usually O(n) for recursion stack

#### 📊 **Pros & Cons**
| ✅ Pros | ❌ Cons |
|--------|--------|
| Finds ALL solutions | Exponential time |
| Systematic exploration | Can be slow without pruning |
| Handles constraints well | Complex to implement |
| Great for puzzles | Stack overflow for large n |

#### 🎯 **Classic Problems**
- N-Queens
- Sudoku Solver
- Generate all subsets/permutations
- Combination Sum
- Word Search
- Rat in a Maze

---

### 6. 🔄 **Recursion**
*"Function calls itself on smaller instances"*

#### 🤔 **Mental Model**
Like Russian dolls: each doll contains a smaller copy of itself. Solve a big problem by solving a slightly smaller version of the same problem, until you reach a tiny problem you can solve directly.

#### 🎯 **When to Use**
- Problem can be defined in terms of itself
- Tree/Graph traversal
- Divide & Conquer problems
- Backtracking problems
- Problems with recursive data structures (trees, linked lists)

#### 🧠 **Recognition Patterns**
- "Define function in terms of itself..."
- "Tree traversal..."
- "Compute factorial/fibonacci..."
- "List all files in directories..."
- "Parse nested structures..."

#### 💻 **Template**
```python
def recursive_solution(problem):
    # 1. BASE CASE: Smallest instance, solved directly
    if is_base_case(problem):
        return base_value
    
    # 2. RECURSIVE CASE: Reduce to smaller instance
    smaller_problem = reduce_problem(problem)
    subresult = recursive_solution(smaller_problem)
    
    # 3. COMBINE: Use subresult to build result
    return combine(problem, subresult)

# Example: Tree traversal
def traverse_tree(node):
    # Base case
    if node is None:
        return
    
    # Process current node
    print(node.value)
    
    # Recursive cases (smaller instances)
    traverse_tree(node.left)
    traverse_tree(node.right)

# Example: Factorial
def factorial(n):
    # Base case
    if n <= 1:
        return 1
    
    # Recursive case
    return n * factorial(n - 1)

# Example: Directory listing
def list_files(directory):
    files = []
    
    for item in os.listdir(directory):
        path = os.path.join(directory, item)
        
        if os.path.isfile(path):
            files.append(path)  # Base case
        else:
            # Recursive case: list subdirectory
            files.extend(list_files(path))
    
    return files
```

#### ⚖️ **Complexity**
- **Time:** Varies (O(n), O(2ⁿ), etc.)
- **Space:** O(depth of recursion) for stack

#### 📊 **Pros & Cons**
| ✅ Pros | ❌ Cons |
|--------|--------|
| Elegant and clean code | Stack overflow risk |
| Natural for certain problems | Function call overhead |
| Easy to prove correctness | Can be hard to debug |
| Great for tree/graph problems | May be less efficient |

#### 🎯 **Classic Problems**
- Factorial
- Fibonacci
- Tree traversals
- Tower of Hanoi
- Binary search (recursive)
- Directory traversal

---

### 7. 🌿 **Branch & Bound**
*"Smart backtracking with pruning"*

#### 🤔 **Mental Model**
Like planning a road trip: you have a map and you know the straight-line distance to your destination. If a road is already longer than the best route you've found, don't bother exploring it. Prune early, explore promising paths first.

#### 🎯 **When to Use**
- Optimization problems (find BEST solution)
- Need to avoid exploring all possibilities
- Can calculate bounds/estimates
- Problems where early pruning saves time
- When backtracking is too slow

#### 🧠 **Recognition Patterns**
- "Find the shortest/cheapest way..."
- "Minimize cost/maximize profit..."
- "Traveling salesman problem"
- "Job scheduling optimization"
- "Find optimal solution quickly"

#### 💻 **Template**
```python
def branch_and_bound(problem):
    best_solution = None
    best_cost = float('inf')
    
    def bound(current_solution):
        """Calculate optimistic estimate (lower bound for minimization)"""
        # This is problem-specific
        # Must be <= actual cost of any complete solution
        return optimistic_estimate(current_solution)
    
    def branch(current_solution, remaining_items):
        nonlocal best_solution, best_cost
        
        # Calculate bound for current path
        current_cost = calculate_cost(current_solution)
        optimistic_cost = current_cost + bound(current_solution)
        
        # PRUNE: if can't beat best solution, stop exploring
        if optimistic_cost >= best_cost:
            return
        
        # If solution is complete
        if is_complete(current_solution):
            if current_cost < best_cost:
                best_cost = current_cost
                best_solution = current_solution.copy()
            return
        
        # Try each possible next choice
        for choice in get_next_choices(remaining_items):
            # Make choice
            current_solution.append(choice)
            
            # Explore further
            branch(current_solution, remaining_items - {choice})
            
            # Backtrack
            current_solution.pop()
    
    branch([], initial_items)
    return best_solution, best_cost

# Example: Traveling Salesman (simplified)
def tsp_branch_bound(distances, cities):
    n = len(cities)
    best_path = None
    best_cost = float('inf')
    
    def bound(path):
        # Simple bound: sum of minimum edges from remaining cities
        remaining = set(cities) - set(path)
        if not remaining:
            # Add return to start
            return distances[path[-1]][path[0]]
        
        bound_sum = 0
        for city in remaining:
            # Add minimum edge from this city
            min_edge = min(distances[city][c] for c in remaining | {path[0]})
            bound_sum += min_edge
        return bound_sum
    
    def branch(path, remaining, current_cost):
        nonlocal best_path, best_cost
        
        # Prune if can't beat best
        if current_cost + bound(path) >= best_cost:
            return
        
        if not remaining:
            # Complete tour by returning to start
            total = current_cost + distances[path[-1]][path[0]]
            if total < best_cost:
                best_cost = total
                best_path = path + [path[0]]
            return
        
        # Try each remaining city
        for city in sorted(remaining, 
                          key=lambda x: distances[path[-1]][x]):
            branch(path + [city], 
                  remaining - {city}, 
                  current_cost + distances[path[-1]][city])
    
    for start in cities:
        branch([start], set(cities) - {start}, 0)
    
    return best_path, best_cost
```

#### ⚖️ **Complexity**
- **Time:** Better than brute force but still exponential worst-case
- **Space:** O(n) for recursion

#### 📊 **Pros & Cons**
| ✅ Pros | ❌ Cons |
|--------|--------|
| Finds optimal solution | Complex to implement |
| Prunes bad paths early | Bound calculation tricky |
| Better than backtracking | Still exponential worst-case |
| Great for optimization | Problem-specific tuning |

#### 🎯 **Classic Problems**
- Traveling Salesman
- Job Shop Scheduling
- 0/1 Knapsack (optimization)
- Assignment Problem
- Graph Coloring

---

## 🎨 Paradigm Selection Guide

### Quick Reference Card

| If you see... | Try... |
|--------------|--------|
| "Find all possible..." | Backtracking |
| "Find the best way..." | DP or Greedy |
| "Count number of ways..." | DP |
| "Divide into halves..." | Divide & Conquer |
| "Always pick the largest/smallest..." | Greedy |
| "Solve this puzzle..." | Backtracking |
| "Tree/Graph traversal..." | Recursion |
| "Optimize with constraints..." | Branch & Bound |
| "Small input size..." | Brute Force |

### Problem Characteristics Matrix

| Paradigm | Best For | Key Feature | Typical Complexity |
|----------|----------|-------------|-------------------|
| Brute Force | Small inputs, verification | Exhaustive search | O(n!) to O(n²) |
| Divide & Conquer | Independent subproblems | Split + combine | O(n log n) |
| Greedy | Local optimum = global | Make choice + move on | O(n log n) |
| DP | Overlapping subproblems | Memoization | O(n²) to O(n³) |
| Backtracking | Constraint satisfaction | Explore + backtrack | Exponential |
| Recursion | Self-similar structure | Function calls itself | Varies |
| Branch & Bound | Optimization with pruning | Bounding function | Exponential+ |

---

## 💡 Pro Tips

### 1. **Start with Brute Force**
Always begin with a brute force solution. It helps you understand the problem and gives you something to optimize.

### 2. **Look for Patterns**
- **Overlapping subproblems?** → DP
- **Independent subproblems?** → Divide & Conquer
- **Local decisions optimal?** → Greedy
- **All solutions needed?** → Backtracking

### 3. **Optimization Progression**
```
Brute Force → Backtracking → DP/Greedy → Branch & Bound
(Slowest)    (Better)      (Fast)       (Optimal+Fast)
```

### 4. **Common Pitfalls**
- Using greedy when DP is needed
- Using recursion without base case
- Not pruning in backtracking
- Wrong DP state definition
- Bound too loose in branch & bound

### 5. **Interview Strategy**
1. Start with brute force (shows you understand problem)
2. Identify the paradigm (shows you recognize patterns)
3. Optimize step by step (shows progression)
4. Implement cleanly (shows coding ability)

---

## 📚 Practice Problems by Paradigm

### 🔨 Brute Force
- Two Sum
- String matching
- Generate all subarrays
- Palindrome checking

### ✂️ Divide & Conquer
- Merge Sort
- Quick Sort
- Binary Search
- Maximum subarray

### 💰 Greedy
- Activity Selection
- Coin Change (standard)
- Huffman Coding
- Fractional Knapsack

### 📊 Dynamic Programming
- 0/1 Knapsack
- Longest Common Subsequence
- Edit Distance
- Matrix Chain Multiplication

### 🔙 Backtracking
- N-Queens
- Sudoku Solver
- Permutations
- Subsets
- Combination Sum

### 🔄 Recursion
- Tree traversals
- Factorial
- Fibonacci
- Tower of Hanoi

### 🌿 Branch & Bound
- Traveling Salesman
- Job Scheduling
- 0/1 Knapsack (optimization)
- Graph Coloring

---

## 🎓 Summary

| Paradigm | Mental Model | When to Use |
|----------|--------------|-------------|
| **Brute Force** | Try everything | Small inputs, starting point |
| **Divide & Conquer** | Split + solve + combine | Independent subproblems |
| **Greedy** | Best local choice | Local optimum works |
| **Dynamic Programming** | Remember past | Overlapping subproblems |
| **Backtracking** | Explore + backtrack | Need all solutions |
| **Recursion** | Function calls itself | Self-similar structure |
| **Branch & Bound** | Prune bad paths | Optimization with bounds |

---

*Remember: The right paradigm transforms a impossible problem into an elegant solution. Master these seven, and you'll have a framework for tackling any coding challenge!* 🚀
```

This comprehensive file provides:
1. Clear explanations of each paradigm
2. Mental models for understanding
3. When to use each approach
4. Code templates
5. Complexity analysis
6. Pros and cons
7. Classic problems
8. Selection guides

You can now push this to GitHub! Let me know when you're ready for the next file (2️⃣-Algorithmic-Techniques-Cheatsheet.md).