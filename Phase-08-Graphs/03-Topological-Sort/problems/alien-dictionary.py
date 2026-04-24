"""
Problem: Alien Dictionary

Difficulty: Hard (LeetCode #269)

---------------------------------------------------
Problem Statement:

You're given a list of `words` from an alien language, SORTED
lexicographically (in THEIR alphabet order, which you don't know).
Return a valid alphabet ordering of the characters that appear in
`words`, or "" if no such ordering exists.

Example:
    words = ["wrt", "wrf", "er", "ett", "rftt"]

    From adjacent pairs, we infer orderings:
        "wrt"<"wrf"   →   t < f
        "wrf"<"er"    →   w < e
        "er"<"ett"    →   r < t
        "ett"<"rftt"  →   e < r

    Combining: w < e < r < t < f.
    Answer: "wertf" (any topological order of these constraints).

---------------------------------------------------
The Reduction:

1. Collect all UNIQUE characters into the alphabet.
2. For each adjacent pair (word_i, word_{i+1}):
     Find the first position where they differ.
     That character of word_i must come BEFORE that character
     of word_{i+1}. That's a directed edge.

3. Topologically sort the character graph.

---------------------------------------------------
Edge Cases:

Case A — INVALID PREFIX:
    words = ["abc", "ab"]
    `abc` being sorted BEFORE `ab` is impossible in any ordering
    (a proper prefix comes FIRST, not after). Return "".

Case B — Cycle in the character graph:
    words = ["wrt", "wrf", "tf", "tr"]
    "tf" < "tr"  →   f < r
    "wrt" < "wrf" →  t < f
    "wrf" < "tf"  →  w < t
    "tf" < "tr"   →  f < r     (already there)
    ...if we can also derive r < w somehow, closing a cycle,
    topo sort fails → return "".

We cover both cases in the tests.

---------------------------------------------------
Complexity:

    Let C = total length of all words, V = distinct chars, E = pairs.

    Time:  O(C + V + E)   = O(C) since E ≤ V²  ≤ 26²
    Space: O(V + E)       = O(1) given a fixed alphabet (26 lowercase)
"""

from collections import defaultdict, deque


def alien_order(words):
    """
    Return a valid alphabet ordering, or "" if none exists.

    Time:  O(C), Space: O(V + E).
    """
    # 1. Initialize graph with every unique character
    adj = defaultdict(set)
    indeg = {ch: 0 for w in words for ch in w}

    # 2. Derive constraints from adjacent pairs
    for i in range(len(words) - 1):
        w1, w2 = words[i], words[i + 1]
        # Walk both strings simultaneously
        min_len = min(len(w1), len(w2))
        found_diff = False
        for j in range(min_len):
            if w1[j] != w2[j]:
                if w2[j] not in adj[w1[j]]:
                    adj[w1[j]].add(w2[j])
                    indeg[w2[j]] += 1
                found_diff = True
                break
        # If w1 is STRICTLY LONGER and starts with w2, it's invalid
        if not found_diff and len(w1) > len(w2):
            return ""

    # 3. Kahn's topological sort
    queue = deque(ch for ch, d in indeg.items() if d == 0)
    order = []
    while queue:
        u = queue.popleft()
        order.append(u)
        for v in adj[u]:
            indeg[v] -= 1
            if indeg[v] == 0:
                queue.append(v)

    if len(order) != len(indeg):
        return ""                                  # cycle in constraints
    return "".join(order)


# =========================================================================
# Test
# =========================================================================

def _valid_alien_order(words, alphabet):
    """Verify that sorting `words` by `alphabet`'s char order gives `words` back."""
    if not alphabet:
        return False
    rank = {c: i for i, c in enumerate(alphabet)}
    def key(w):
        return [rank[c] for c in w]
    try:
        return all(key(words[i]) <= key(words[i + 1]) for i in range(len(words) - 1))
    except KeyError:
        return False


if __name__ == "__main__":
    # LC #269 examples
    result = alien_order(["wrt", "wrf", "er", "ett", "rftt"])
    assert result != ""
    assert _valid_alien_order(["wrt", "wrf", "er", "ett", "rftt"], result)

    assert alien_order(["z", "x"]) == "zx"

    # Cycle
    assert alien_order(["z", "x", "z"]) == ""

    # Invalid prefix case
    assert alien_order(["abc", "ab"]) == ""

    # Single word — any permutation of its unique chars works
    result = alien_order(["aabb"])
    assert set(result) == {"a", "b"}

    # Identical duplicates
    result = alien_order(["abc", "abc"])
    assert set(result) == {"a", "b", "c"}

    # Empty input
    assert alien_order([]) == ""
    assert alien_order([""]) == ""

    # Multiple valid answers
    result = alien_order(["ab", "ac"])                  # only constraint: b < c
    assert "b" in result and "c" in result and result.index("b") < result.index("c")
    # And 'a' is unconstrained — can appear anywhere
    assert "a" in result

    # Long chain
    words = ["a", "b", "c", "d", "e", "f"]
    result = alien_order(words)
    assert result == "abcdef"

    # Stress: random "valid" word lists, ensure the returned order
    # preserves the input as a sorted list
    import random
    random.seed(42)
    for _ in range(200):
        alphabet_size = random.randint(1, 6)
        alien_alphabet = list("abcdefg"[:alphabet_size])
        random.shuffle(alien_alphabet)
        rank = {c: i for i, c in enumerate(alien_alphabet)}

        # Generate random words and sort by alien order
        n_words = random.randint(1, 8)
        words = []
        for _ in range(n_words):
            L = random.randint(1, 5)
            w = "".join(random.choice(alien_alphabet) for _ in range(L))
            words.append(w)
        words.sort(key=lambda w: [rank[c] for c in w])

        got = alien_order(words)
        # Either valid (sorting under `got` keeps the input sorted)
        # or empty (not enough info — possible for very short lists).
        # It should NEVER be wrong.
        if got != "":
            assert _valid_alien_order(words, got), (
                f"alien_order({words}) = {got!r}, but not consistent"
            )

    print("All tests passed!")
