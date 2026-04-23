"""
Problem: Tower of Hanoi

Difficulty: Medium (classic)

---------------------------------------------------
Problem Statement:

You have 3 pegs (source, auxiliary, destination) and n disks of
different sizes, all stacked on the source peg with the largest at
the bottom and the smallest on top.

Goal: move all n disks from source to destination, subject to:
    1. Only ONE disk can be moved at a time.
    2. Each move takes a disk from the top of one peg and places
       it on another peg.
    3. A larger disk can NEVER be placed on top of a smaller one.

Print the sequence of moves.

---------------------------------------------------
Why Tower of Hanoi Is the Canonical Recursion Demo:

It's the purest illustration of "reduce to a smaller instance of
the same problem." The recursive structure is so clean that the
solution is almost a pseudo-code comment:

    hanoi(n, src, aux, dst):
        if n == 0: return
        hanoi(n - 1, src, dst, aux)        # move top n-1 to aux
        move(src, dst)                     # move disk n to destination
        hanoi(n - 1, aux, src, dst)        # move top n-1 from aux to dst

Three steps. Total moves: **2^n - 1** — the theoretical minimum.

---------------------------------------------------
The Recurrence:

    T(n) = 2 · T(n - 1) + 1                (two recursive calls + one move)

Solving:

    T(n) = 2T(n-1) + 1
         = 2(2T(n-2) + 1) + 1
         = 4T(n-2) + 2 + 1
         = ...
         = 2^n · T(0) + (2^(n-1) + 2^(n-2) + ... + 1)
         = 0 + (2^n - 1)
         = 2^n - 1

So the minimum-move count grows exponentially in n. For n = 64
(the original legend's count), that's 18 quintillion moves — enough
to take monks more than the age of the universe at one move per second.

---------------------------------------------------
Complexity:

    Time:  O(2^n)   — MUST do exponential work; output itself is exponential
    Space: O(n)     — recursion depth

This is an INTRINSICALLY exponential problem. Memoization can't
help because there's no redundancy — every move is distinct.
"""


# =========================================================================
# Classic Recursive Solution
# =========================================================================

def hanoi(n, source="A", auxiliary="B", destination="C", moves=None):
    """
    Solve Tower of Hanoi with n disks.

    Returns a list of (disk_number, from_peg, to_peg) tuples, one per
    move in order.

    Time:  O(2^n)
    Space: O(n) recursion + O(2^n) output
    """
    if moves is None:
        moves = []

    if n <= 0:
        return moves

    # Step 1: move top n-1 disks from source to auxiliary (using destination as spare)
    hanoi(n - 1, source, destination, auxiliary, moves)

    # Step 2: move disk n from source to destination
    moves.append((n, source, destination))

    # Step 3: move top n-1 disks from auxiliary to destination (using source as spare)
    hanoi(n - 1, auxiliary, source, destination, moves)

    return moves


# =========================================================================
# Count Moves (Closed Form)
# =========================================================================

def hanoi_move_count(n):
    """
    Return the number of moves required for n disks.

    The closed-form answer is 2^n - 1.
    """
    return 2 ** n - 1


# =========================================================================
# Pretty-Print the Moves
# =========================================================================

def print_hanoi(n, source="A", auxiliary="B", destination="C"):
    """Print the moves for n disks."""
    moves = hanoi(n, source, auxiliary, destination)
    for disk, frm, to in moves:
        print(f"   Move disk {disk} from {frm} to {to}")
    return moves


# =========================================================================
# Iterative Solution via Explicit Stack (Simulating the Recursion)
# =========================================================================

def hanoi_iterative(n, source="A", auxiliary="B", destination="C"):
    """
    Iterative Tower of Hanoi — the recursion simulated with an explicit
    stack of frames.

    Each "frame" on the stack represents a pending call:
        (n, source, auxiliary, destination, phase)
    where `phase` tracks which of the three steps we're about to do:
        0 → enqueue left subcall, then pop it
        1 → emit the big-disk move and enqueue right subcall
        2 → done

    Time:  O(2^n)
    Space: O(n) explicit stack (same as the recursive version's call stack)

    This version produces the SAME moves as the recursive one — no
    number-theoretic tricks, just iterative simulation.
    """
    moves = []
    # Each frame: [n, src, aux, dst, phase]
    stack = [[n, source, auxiliary, destination, 0]]

    while stack:
        frame = stack[-1]
        cur_n, src, aux, dst, phase = frame

        if cur_n == 0:
            stack.pop()
            continue

        if phase == 0:
            # Phase 0: recurse on hanoi(n - 1, src, dst, aux)
            frame[4] = 1                           # advance phase for this frame
            stack.append([cur_n - 1, src, dst, aux, 0])
        elif phase == 1:
            # Phase 1: emit the big-disk move; prepare the right subcall
            moves.append((cur_n, src, dst))
            frame[4] = 2
            stack.append([cur_n - 1, aux, src, dst, 0])
        else:
            # Phase 2: both subcalls done
            stack.pop()

    return moves


# =========================================================================
# Test
# =========================================================================

if __name__ == "__main__":
    # Print solution for small n
    print("Tower of Hanoi with 3 disks (should take 2^3 - 1 = 7 moves):")
    moves = print_hanoi(3)
    assert len(moves) == 7
    print()

    # Verify move counts for n = 0..10
    for n in range(11):
        moves = hanoi(n)
        expected = hanoi_move_count(n)
        assert len(moves) == expected
        print(f"   n = {n:2}:  {expected} moves")
    print()

    # Verify the moves are LEGAL — simulate and check invariants
    def simulate(n, moves, source="A", auxiliary="B", destination="C"):
        pegs = {source: list(range(n, 0, -1)),
                auxiliary: [], destination: []}
        for disk, frm, to in moves:
            # The disk must be on top of `frm`
            assert pegs[frm][-1] == disk, f"disk {disk} not on top of {frm}"
            # Moving onto `to`: the top disk there (if any) must be larger
            if pegs[to]:
                assert pegs[to][-1] > disk, f"can't put {disk} on {pegs[to][-1]}"
            pegs[frm].pop()
            pegs[to].append(disk)
        # Must end with all disks on destination
        assert pegs[destination] == list(range(n, 0, -1))
        return True

    for n in range(1, 10):
        moves = hanoi(n)
        simulate(n, moves)
    print("   All moves are LEGAL (simulated and verified) for n = 1..9")
    print()

    # Iterative solution matches recursive (by move count and final state)
    for n in range(1, 8):
        rec_moves = hanoi(n)
        iter_moves = hanoi_iterative(n)
        assert len(rec_moves) == len(iter_moves) == 2 ** n - 1
        simulate(n, iter_moves)
    print("   Iterative solution validates for n = 1..7")

    # Closed-form move count
    for n in range(20):
        assert hanoi_move_count(n) == 2 ** n - 1
    print("   Move count = 2^n - 1 confirmed for n = 0..19")

    print("\nAll tests passed!")

    # ---------------------------------------------------------------
    # The Legend (And the Math):
    #
    #   The Tower of Brahma legend has priests moving 64 disks
    #   between three pillars, one disk per second, ending the
    #   universe when they finish.
    #
    #   2^64 - 1 seconds = 1.84 × 10^19 seconds
    #                    ≈ 585 billion years
    #                    ≈ 40× the current age of the universe
    #
    # They've got a while.
    # ---------------------------------------------------------------
