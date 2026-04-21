"""
Problem: Corporate Flight Bookings (Range Updates)

Technique: Difference Array
Difficulty: Medium (LeetCode #1109)

---------------------------------------------------
Problem Statement:

There are `n` flights numbered from 1 to n. You are given an array
`bookings` where `bookings[i] = [first, last, seats]` means the booking
reserved `seats` seats on every flight from `first` to `last` inclusive.

Return an array `answer` of length `n`, where `answer[i]` is the total
number of seats reserved for flight `i+1`.

---------------------------------------------------
The Difference-Array Lens:

Brute force — apply each booking by looping over [first, last]:

    for first, last, seats in bookings:
        for i in range(first - 1, last):
            answer[i] += seats

Cost: O(B · n) where B = len(bookings). For B = n = 20_000 (LeetCode's
limit) that's 4×10^8 operations — borderline TLE.

Difference array turns each booking into an O(1) pair of writes:

    diff[first - 1]      += seats
    diff[last]           -= seats         # "last+1" in 0-indexed, which is just `last` when first/last are 1-indexed

At the end, `answer` is the prefix sum of `diff`. Total cost: O(B + n).

---------------------------------------------------
Indexing Note:

The problem is 1-indexed: flights are 1..n, booking ranges are [first, last].

We'll store `diff` in 0-indexed form (length n + 1 so we can safely
write `diff[last]` as the exclusive end).

    1-indexed booking [first, last]
        → 0-indexed range [first - 1, last - 1] inclusive
        → diff updates:
              diff[first - 1] += seats
              diff[last]      -= seats         # = diff[(last - 1) + 1]

This is the single off-by-one that causes bugs in this problem. Always
redraw the index conversion.

---------------------------------------------------
Example:

    bookings = [[1, 2, 10], [2, 3, 20], [2, 5, 25]],  n = 5

    Booking 1: seats 10 on flights 1, 2
    Booking 2: seats 20 on flights 2, 3
    Booking 3: seats 25 on flights 2, 3, 4, 5

    answer = [10, 55, 45, 25, 25]

    (Flight 1: 10.  Flight 2: 10+20+25 = 55.  Flight 3: 20+25 = 45.
     Flights 4, 5: 25 each.)

---------------------------------------------------
"""

# -------------------------------------------------
# The Difference-Array Solution — O(B + n)
# -------------------------------------------------

def corporate_flight_bookings(bookings, n):
    """
    Return total seats booked per flight using difference array.

    Time Complexity:  O(B + n)
    Space Complexity: O(n)
    """
    diff = [0] * (n + 1)

    for first, last, seats in bookings:
        diff[first - 1] += seats                  # convert to 0-indexed start
        diff[last]      -= seats                  # one past 0-indexed end = `last`

    # reconstruct via prefix sum
    answer = [0] * n
    running = 0
    for i in range(n):
        running += diff[i]
        answer[i] = running
    return answer


# -------------------------------------------------
# Brute Force for Verification — O(B · n)
# -------------------------------------------------

def corporate_flight_bookings_brute_force(bookings, n):
    """
    Apply each booking by looping over its range.

    Time Complexity:  O(B · n)
    Space Complexity: O(n)
    """
    answer = [0] * n
    for first, last, seats in bookings:
        for i in range(first - 1, last):
            answer[i] += seats
    return answer


# -------------------------------------------------
# Test the Functions
# -------------------------------------------------

if __name__ == "__main__":
    # Classic example from the problem statement
    bookings = [[1, 2, 10], [2, 3, 20], [2, 5, 25]]
    n = 5

    got = corporate_flight_bookings(bookings, n)
    exp = [10, 55, 45, 25, 25]
    print(f"   bookings = {bookings}")
    print(f"   n        = {n}")
    print(f"   expected = {exp}")
    print(f"   got      = {got}")
    assert got == exp
    print()

    # Test cases — (bookings, n, expected)
    test_cases = [
        ([[1, 2, 10], [2, 3, 20], [2, 5, 25]],    5,   [10, 55, 45, 25, 25]),
        ([[1, 2, 10], [2, 2, 15]],                2,   [10, 25]),
        ([[1, 1, 5]],                             1,   [5]),
        ([],                                      3,   [0, 0, 0]),
        ([[1, 3, 100]],                           3,   [100, 100, 100]),
        # overlapping + non-overlapping mix
        ([[1, 2, 5], [4, 5, 7]],                  5,   [5, 5, 0, 7, 7]),
        # same range added twice
        ([[2, 4, 3], [2, 4, 2]],                  5,   [0, 5, 5, 5, 0]),
    ]

    for i, (b, nn, expected) in enumerate(test_cases):
        got = corporate_flight_bookings(b, nn)
        assert got == expected, (
            f"Test {i+1}: expected {expected}, got {got}"
        )
        bf = corporate_flight_bookings_brute_force(b, nn)
        assert got == bf, (
            f"Test {i+1}: diff-array ({got}) disagrees with brute force ({bf})"
        )
        print(f"Test {i+1} passed: bookings={b}, n={nn} -> {expected}")

    # Stress test — larger random inputs
    import random
    random.seed(42)
    n = 200
    B = 500
    random_bookings = []
    for _ in range(B):
        first = random.randint(1, n)
        last = random.randint(first, n)
        seats = random.randint(1, 100)
        random_bookings.append([first, last, seats])

    fast = corporate_flight_bookings(random_bookings, n)
    brute = corporate_flight_bookings_brute_force(random_bookings, n)
    assert fast == brute
    print(f"\nStress test: n={n}, B={B} random bookings matched brute force")

    print("\nAll tests passed!")

    # ---------------------------------------------------------------
    # The Speedup:
    #
    #   Naive brute force:   O(B * n)
    #   Difference array:    O(B + n)
    #
    #   For B = n = 20_000:
    #       naive:           4 * 10^8 operations   → seconds in Python (TLE risk)
    #       diff array:      4 * 10^4 operations   → milliseconds
    #
    # A 10_000× speedup from two array writes per booking. That's the
    # power of picking the right representation: you're doing the same
    # arithmetic, just in a form that compresses.
    # ---------------------------------------------------------------
