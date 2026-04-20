# 🤝 Contributing Guide

Thank you for your interest in contributing to **Master Python DSA**! This project is a learning resource, so every improvement — from fixing a typo to adding a new problem — helps someone learn better.

This guide explains **how to contribute**, **what we accept**, and **the standards** we follow.

---

## 📚 Table of Contents

- [Ways to Contribute](#-ways-to-contribute)
- [Before You Start](#-before-you-start)
- [Project Structure](#-project-structure)
- [Contribution Workflow](#-contribution-workflow)
- [Coding Standards](#-coding-standards)
- [Documentation Standards](#-documentation-standards)
- [Adding a New Problem](#-adding-a-new-problem)
- [Adding a New Topic / Phase](#-adding-a-new-topic--phase)
- [Commit Message Convention](#-commit-message-convention)
- [Pull Request Checklist](#-pull-request-checklist)
- [Code of Conduct](#-code-of-conduct)

---

## 🌟 Ways to Contribute

You can contribute in many ways:

| Contribution Type | Examples |
|-------------------|----------|
| 📝 **Documentation** | Fix typos, improve explanations, clarify examples |
| 🧩 **New Problems** | Add coding problems with solutions and explanations |
| 💡 **New Solutions** | Add alternative approaches to existing problems |
| 🐛 **Bug Fixes** | Fix incorrect complexity analysis, broken code, wrong outputs |
| 📘 **New Topics** | Add missing chapters (e.g., Linked Lists, Trees, Graphs) |
| 🎨 **Visuals** | Add diagrams, flowcharts, or animated illustrations |
| 🧪 **Tests** | Add unit tests for existing implementations |

---

## ✅ Before You Start

1. **Check existing issues and PRs** — your idea may already be in progress.
2. **Open an issue first** for large changes (new topics, structural changes). This avoids duplicate work.
3. **Small fixes** (typos, formatting) — feel free to submit a PR directly.
4. **Read this guide fully** before your first contribution.

---

## 📂 Project Structure

### Top-Level Layout

```text
Data-Structures-and-Algorithms-Python/
│
├── README.md                                # Project overview & quick start
├── ROADMAP.md                               # 13-phase learning journey
├── CONTRIBUTING.md                          # Pointer to this guide
├── LICENSE                                  # MIT License
├── .gitignore                               # Python / OS / IDE ignores
├── requirements.txt                         # Optional dev dependencies
│
├── Phase-01-Foundations/                    # DSA basics, complexity, built-ins
├── Phase-02-Problem-Solving-Foundations/    # Paradigms & techniques
├── Phase-03-Searching-Sorting/              # Search & sort algorithms
├── Phase-04-Linear-Data-Structures/         # Array, String, LL, Stack, Queue
├── Phase-05-Recursion-Backtracking/         # Recursion & backtracking
├── Phase-06-Hashing/                        # HashMap, HashSet, frequency
├── Phase-07-Trees-Heaps/                    # Trees, BST, AVL, Heap, Trie
├── Phase-08-Graphs/                         # Graph algorithms
├── Phase-09-Dynamic-Programming/            # 1D/2D DP, Knapsack, LCS, LIS
├── Phase-10-String-Algorithms/              # KMP, Z-algo, Manacher, Suffix
├── Phase-11-Advanced-Data-Structures/       # Segment Tree, Fenwick, Sparse
├── Phase-12-Greedy-Math/                    # Greedy, number theory, combinatorics
├── Phase-13-Competitive-Level/              # HLD, Network Flow, Convex Hull
│
├── resources/                               # Cheatsheets, templates, interview prep
├── projects/                                # Beginner → advanced DSA projects
├── scripts/                                 # Automation & test runners
├── tests/                                   # Unit tests
└── docs/                                    # Contributing, style guide, FAQ
```

### Inside Each Phase

Every phase has a `README.md` and one or more numbered topic folders:

```text
Phase-XX-Topic-Name/
├── README.md                # Phase overview & learning goals
├── 01-First-Topic/
├── 02-Second-Topic/
└── 03-Third-Topic/
```

### Inside Each Topic

Most topics follow this consistent pattern:

```text
<topic-name>/
├── theory.md                # Concept explanation (what/why/how)
├── operations.py            # Hands-on code examples
├── time-complexity.md       # Big O analysis for every operation
└── problems/
    ├── easy/
    │   ├── 01-problem-name.py
    │   ├── 02-problem-name.py
    │   └── solutions.md     # Step-by-step explanations
    ├── medium/
    │   ├── 01-problem-name.py
    │   └── solutions.md
    └── hard/
        ├── 01-problem-name.py
        └── solutions.md
```

> **Note:** Some algorithm-focused folders (e.g., sorting, searching) replace `theory.md` + `operations.py` with implementation files like `merge-sort.py`, `quick-sort.py`. Use the pattern that best fits the topic — but keep `problems/` with the `easy/medium/hard/` tiers wherever practice problems exist.

### Supporting Folders

| Folder        | Purpose                                                              |
|---------------|----------------------------------------------------------------------|
| `resources/`  | Cheatsheets, reusable templates, interview prep, book notes, videos  |
| `projects/`   | End-to-end applications (beginner / intermediate / advanced)         |
| `scripts/`    | Automation: `setup.sh`, `test-runner.py`, `generate-stats.py`        |
| `tests/`      | Unit tests for algorithms and data structures                        |
| `docs/`       | Contributing guide, style guide, FAQ                                 |

---

## 🔁 Contribution Workflow

### 1. Fork the repository

Click the **Fork** button at the top right of the repo on GitHub.

### 2. Clone your fork

```bash
git clone https://github.com/<your-username>/Data-Structures-and-Algorithms-Python.git
cd Data-Structures-and-Algorithms-Python
```

### 3. Create a feature branch

```bash
git checkout -b feat/add-linked-list-topic
```

**Branch naming:**
- `feat/<short-description>` — new features or content
- `fix/<short-description>` — bug fixes
- `docs/<short-description>` — documentation-only changes
- `refactor/<short-description>` — code restructuring

### 4. Make your changes

Follow the [Coding Standards](#-coding-standards) and [Documentation Standards](#-documentation-standards) below.

### 5. Test your code

```bash
python3 path/to/your-file.py
```

Make sure:
- The script runs without errors.
- Output matches the expected examples.
- All assertions / tests pass.

### 6. Commit your changes

See [Commit Message Convention](#-commit-message-convention).

### 7. Push and open a Pull Request

```bash
git push origin feat/add-linked-list-topic
```

Then open a PR against `main` from the GitHub UI. Fill out the PR template completely.

---

## 🐍 Coding Standards

### Language & Version
- **Python 3.11+**
- Use **standard library only** unless the topic specifically requires a third-party package.

### Style
- Follow **[PEP 8](https://peps.python.org/pep-0008/)**.
- Use **4 spaces** for indentation (no tabs).
- Keep lines under **100 characters** where possible.
- Use **`snake_case`** for variables and functions.
- Use **`PascalCase`** for classes.

### Required Structure for Each Python File

Every solution file must include:

```python
"""
Problem XX: <Problem Title>

Difficulty: Easy | Medium | Hard

---------------------------------------------------
Problem Statement:

<Clear description of the problem>

---------------------------------------------------
Example:

Input:
    <example input>

Output:
    <example output>

---------------------------------------------------
"""


def solution_function(arr):
    """
    Short description of the approach.

    Time Complexity: O(...)
    Space Complexity: O(...)
    """
    # Implementation
    pass


if __name__ == "__main__":
    # Test cases
    test_cases = [
        (input1, expected1),
        (input2, expected2),
    ]

    for i, (inp, expected) in enumerate(test_cases):
        result = solution_function(inp)
        assert result == expected, f"Test {i+1} failed: expected {expected}, got {result}"
        print(f"Test {i+1} passed: {inp} -> {result}")

    print("\nAll tests passed!")
```

### Required Rules

- ✅ **Always include time and space complexity** in docstrings.
- ✅ **Always include at least one test case** (using `assert` or printed output).
- ✅ **Handle edge cases**: empty input, single element, duplicates, negatives.
- ✅ **Provide at least two approaches** when educational (e.g., brute-force + optimal).
- ❌ **Never commit** unused imports, commented-out code, or debug `print` statements.

---

## 📝 Documentation Standards

### Markdown Files

- Use **GitHub-flavored Markdown**.
- Start each file with a clear `# Title`.
- Use **consistent heading levels** (don't skip from `##` to `####`).
- Use **fenced code blocks** with language tags: ` ```python `, ` ```bash `, ` ```text `.
- Use **tables** for comparisons and complexity summaries.
- Use **emojis sparingly** but consistently with the existing style.

### Explanation Quality

- Write for **beginners** — avoid jargon without defining it.
- Use **analogies** to connect abstract ideas to real-world examples.
- Include **step-by-step traces** for non-trivial algorithms.
- Show **both correct and incorrect** approaches when instructive.
- Always add a **complexity analysis** section.

### File Naming

Use **kebab-case** (lowercase, hyphen-separated):

- ✅ `time-complexity.md`
- ✅ `01-two-sum.py`
- ❌ `Time_Complexity.md`
- ❌ `01_TwoSum.py`

---

## 🧩 Adding a New Problem

1. **Choose the correct folder and difficulty tier**
   Every topic has three tiers: `easy/`, `medium/`, `hard/`.
   Example: a list-based **easy** problem →
   `Phase-01-Foundations/03-Python-BuiltIn-DSA/01-List/problems/easy/`

2. **Name the file** using the pattern `NN-problem-name.py`:
   - `NN` = two-digit number (next in sequence within that difficulty tier)
   - `problem-name` = kebab-case summary
   - Example: `03-find-duplicates.py`

3. **Follow the Python file template** from the [Coding Standards](#-coding-standards).

4. **Update `solutions.md`** in the **same difficulty folder** (e.g., `easy/solutions.md`) with:
   - Problem recap
   - Approach explanation (step-by-step)
   - Why each approach works
   - Complexity discussion
   - Related practice questions

5. **Run your file** and confirm all tests pass:
   ```bash
   python3 Phase-01-Foundations/03-Python-BuiltIn-DSA/01-List/problems/easy/03-find-duplicates.py
   ```

### Difficulty Tier Guidelines

| Tier | Characteristics | Typical Complexity |
|------|-----------------|--------------------|
| **easy** | Single data structure, straightforward logic, 5–15 lines of core code | O(n) or O(n log n) |
| **medium** | Combined techniques, optimization required, tricky edge cases | O(n) with clever use of hashing/pointers |
| **hard** | Multiple approaches to compare, advanced patterns, non-obvious insight | Often O(n log n) optimal, sometimes requires DP |

---

## 📘 Adding a New Topic / Phase

Adding a whole new topic (e.g., "Linked Lists") is a bigger contribution. Please **open an issue first** to discuss scope.

### For a New Topic (within an existing phase)

Create the folder with the standard pattern:

```text
<new-topic>/
├── theory.md
├── operations.py
├── time-complexity.md
└── problems/
    ├── easy/
    │   ├── 01-first-problem.py
    │   └── solutions.md
    ├── medium/
    └── hard/
```

**Also update:**
- The **parent phase's `README.md`** to list the new topic.
- **[ROADMAP.md](../ROADMAP.md)** if the topic represents a significant milestone.

### For a New Phase

Creating a new phase is rare — most additions fit within the existing 13 phases. Before starting, confirm with the maintainer via an issue.

If approved, the folder structure is:

```text
Phase-XX-Phase-Name/
├── README.md                # Phase overview: what you'll learn, prerequisites
├── 01-First-Topic/          # (Topic folders as above)
├── 02-Second-Topic/
└── ...
```

**Also update:**
- The **root [README.md](../README.md)** — add the phase to the structure tree and Quick Navigation.
- **[ROADMAP.md](../ROADMAP.md)** — add the phase row with status and description.
- Any preceding phase's "what's next" reference, if it links forward.

---

## 📮 Commit Message Convention

Follow a simple, readable format:

```text
<type>: <short imperative summary>

<optional longer explanation>
```

### Types

| Type       | Purpose                                      |
|------------|----------------------------------------------|
| `feat`     | New content or feature                       |
| `fix`      | Bug fix / correction                         |
| `docs`     | Documentation-only changes                   |
| `refactor` | Restructure without changing behavior        |
| `style`    | Formatting, whitespace, naming               |
| `test`     | Adding or updating tests                     |
| `chore`    | Housekeeping (gitignore, configs)            |

### Examples

```text
feat: add merge sort implementation with step-by-step trace
fix: correct space complexity in rotate.py brute-force approach
docs: clarify O(log n) explanation in time-complexity.md
refactor: rename Phase-01—Foundations → Phase-01-Foundations
```

### Rules
- Use **imperative mood**: "add", "fix", "remove" (not "added", "fixed").
- Keep the summary **≤ 70 characters**.
- Use the body (wrapped at ~72 chars) for **why**, not **what**.

---

## ✅ Pull Request Checklist

Before submitting, ensure your PR meets all of these:

- [ ] The branch is up to date with `main`.
- [ ] Code follows [PEP 8](https://peps.python.org/pep-0008/).
- [ ] Every Python file includes **time and space complexity** in docstrings.
- [ ] Every Python file has **at least one test case** that passes.
- [ ] File and folder names use **kebab-case**.
- [ ] Markdown renders correctly (preview on GitHub).
- [ ] No unused imports, commented-out code, or stray `print` debug lines.
- [ ] Commit messages follow the [convention](#-commit-message-convention).
- [ ] The PR description clearly explains **what** and **why**.
- [ ] Linked to a related issue (if one exists).

---

## 📜 Code of Conduct

This project follows a simple rule: **be kind, be helpful, be patient.**

- Respect all contributors, regardless of experience level.
- Give constructive feedback — focus on the code, not the person.
- Assume good intent.
- English is preferred for discussions so everyone can participate.

Harassment, discrimination, or disrespectful behavior will not be tolerated.

---

## 🙋 Need Help?

- Open a **[GitHub Issue](../../issues)** for questions, ideas, or bug reports.
- Check existing discussions before posting a new one.
- Tag your issue appropriately (`bug`, `enhancement`, `question`, `good first issue`).

---

## 🎉 Thank You!

Every contribution makes this resource better for thousands of learners around the world. Whether you fix a typo or add a whole new topic — **you're helping someone crack their first coding interview, or understand DSA for the first time.**

That matters. Thank you. 🚀
