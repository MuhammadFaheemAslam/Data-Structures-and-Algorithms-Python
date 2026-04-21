"""
Problem 01: Word Frequency Count

Difficulty: Easy

---------------------------------------------------
Problem Statement:

Given a sentence (or a list of words), return a dictionary that maps
each word to how many times it appears.

Bonus: also return the MOST FREQUENT word.

This problem highlights the #1 everyday use of dicts: counting.
You'll meet this pattern under many different names — histogram,
frequency map, bag-of-words — but the core technique is always the same.

---------------------------------------------------
Example:

Input:
    "the quick brown fox jumps over the lazy dog the"

Output:
    {'the': 3, 'quick': 1, 'brown': 1, 'fox': 1,
     'jumps': 1, 'over': 1, 'lazy': 1, 'dog': 1}

    most frequent = 'the'

---------------------------------------------------
"""

# -------------------------------------------------
# Approach 1: Manual Loop with .get() (Interview Friendly)
# -------------------------------------------------

def word_count_get(sentence):
    """
    Walk the words, incrementing each count with .get(word, 0) + 1.

    Time Complexity: O(n)   where n = number of words
    Space Complexity: O(k)  where k = number of DISTINCT words

    This is the "show me you understand dicts" version – no imports,
    no tricks, works on any Python.
    """
    counts = {}
    for word in sentence.split():
        counts[word] = counts.get(word, 0) + 1
    return counts


# -------------------------------------------------
# Approach 2: setdefault() (Same Idea, Slightly Different Shape)
# -------------------------------------------------

def word_count_setdefault(sentence):
    """
    setdefault(key, 0) returns the existing value or inserts 0 and returns it.
    Slightly clunkier than .get() for counting, but handy when the default
    is a mutable container (list, set).

    Time Complexity: O(n)
    Space Complexity: O(k)
    """
    counts = {}
    for word in sentence.split():
        counts[word] = counts.setdefault(word, 0) + 1
    return counts


# -------------------------------------------------
# Approach 3: collections.Counter (One-Liner)
# -------------------------------------------------

def word_count_counter(sentence):
    """
    The standard-library tool for exactly this problem.

    Time Complexity: O(n)
    Space Complexity: O(k)

    Counter is a dict subclass; it IS a dict, with extra helpers like
    .most_common() that returns the top-N pairs by count.
    """
    from collections import Counter
    return dict(Counter(sentence.split()))


# -------------------------------------------------
# Most Frequent Word
# -------------------------------------------------

def most_frequent(counts):
    """
    Return the key with the largest value.

    Time Complexity: O(k) where k = number of distinct keys.
    Space Complexity: O(1).

    max(counts, key=counts.get) is the idiomatic pattern: `max` iterates
    over the dict's KEYS and calls counts.get(key) to get the comparison
    value. Ties are broken by first-seen (insertion order).
    """
    if not counts:
        return None
    return max(counts, key=counts.get)


# -------------------------------------------------
# Test the Functions
# -------------------------------------------------

if __name__ == "__main__":
    sentence = "the quick brown fox jumps over the lazy dog the"

    print(f"Input: {sentence!r}")
    print()
    print(f"word_count_get:         {word_count_get(sentence)}")
    print(f"word_count_setdefault:  {word_count_setdefault(sentence)}")
    print(f"word_count_counter:     {word_count_counter(sentence)}")
    print()

    counts = word_count_get(sentence)
    print(f"most frequent word: {most_frequent(counts)!r}")
    print()

    # Test cases – (sentence, expected_counts, expected_most_frequent)
    test_cases = [
        (
            "a b a c a b",
            {"a": 3, "b": 2, "c": 1},
            "a",
        ),
        (
            "hello",
            {"hello": 1},
            "hello",
        ),
        (
            "",
            {},
            None,
        ),
        (
            "one two three",
            {"one": 1, "two": 1, "three": 1},
            "one",                         # all tied; first-seen wins
        ),
    ]

    for i, (data, expected_counts, expected_top) in enumerate(test_cases):
        got_counts = word_count_get(data)
        got_top = most_frequent(got_counts)
        assert got_counts == expected_counts, (
            f"Test {i+1} counts failed: expected {expected_counts}, got {got_counts}"
        )
        assert got_top == expected_top, (
            f"Test {i+1} most_frequent failed: expected {expected_top}, got {got_top}"
        )
        print(f"Test {i+1} passed: counts={got_counts}, top={got_top!r}")

    print("\nAll tests passed!")
