"""
Problem: Task Scheduler

Difficulty: Medium (LeetCode #621)

---------------------------------------------------
Problem Statement:

You have a list of tasks represented by CHARACTERS (task types).
Each unit of time the CPU either runs a task or IDLES. Between two
runs of the SAME task type, there must be a COOLDOWN of at least `n`
time units. Return the minimum number of time units to finish all
tasks.

Example:
    tasks = ["A","A","A","B","B","B"], n = 2
    One schedule: A B idle A B idle A B    → 8 time units
    (Between consecutive A's there are 2 other slots; same for B.)

---------------------------------------------------
Approach 1 — Simulation With A Max-Heap + Cooldown Queue:

Build counts of each task type. The strategy is to always RUN the task
with the highest remaining count that's not on cooldown. Tasks that
JUST RAN go on a cooldown timer; they become available again after
`n` ticks.

    max_heap: task counts (largest first) of available tasks
    cooldown: FIFO of (count, ready_time)

At each tick:
    if heap non-empty: pop max, decrement, schedule for return
    else: idle
    move entries from cooldown whose ready_time has come back to heap

O(T log k) where T is total ticks and k is number of distinct tasks.

---------------------------------------------------
Approach 2 — Greedy Formula (the "AHA" solution):

Let `m = max task count` and `c = number of tasks tied at count m`.
The minimum time is:

    max(len(tasks), (m - 1) * (n + 1) + c)

Intuition: the most-frequent tasks dominate the schedule. You have
(m - 1) full "frames" of length (n + 1), plus one final frame holding
`c` tasks. If the total task count exceeds that, the extra tasks fill
idle slots, giving just `len(tasks)`.

O(T) overall, O(26) space. This is the "you should know if asked
this in an interview" solution, but the simulation is more general
(handles more variants).

---------------------------------------------------
Complexity summary:

    Simulation:  O(T log k).
    Formula:     O(T).
"""

from collections import Counter, deque
import heapq


# -------- Solution 1: Simulation --------

def schedule_sim(tasks, n):
    """
    Simulate tick-by-tick: max-heap of available task counts,
    FIFO cooldown queue of (remaining_count, ready_time).

    Time:  O(T log k), Space: O(k).
    """
    counts = Counter(tasks)
    heap = [-c for c in counts.values()]           # max-heap via negation
    heapq.heapify(heap)
    cooldown = deque()                             # (remaining_count, ready_time)
    time = 0

    while heap or cooldown:
        time += 1

        if heap:
            c = -heapq.heappop(heap) - 1           # run this task; decrement count
            if c > 0:
                cooldown.append((c, time + n))
        # else: idle

        # Release any tasks whose cooldown expired
        if cooldown and cooldown[0][1] == time:
            c, _ = cooldown.popleft()
            heapq.heappush(heap, -c)

    return time


# -------- Solution 2: Closed-form formula --------

def schedule_formula(tasks, n):
    """
    Max total time = max(len(tasks), (max_count - 1) * (n + 1) + ties_at_max).

    Time:  O(T).
    """
    if not tasks:
        return 0
    counts = Counter(tasks)
    m = max(counts.values())
    c = sum(1 for v in counts.values() if v == m)
    return max(len(tasks), (m - 1) * (n + 1) + c)


# =========================================================================
# Test
# =========================================================================

if __name__ == "__main__":
    # LC #621 examples
    cases = [
        (["A", "A", "A", "B", "B", "B"], 2, 8),
        (["A", "A", "A", "B", "B", "B"], 0, 6),                    # no cooldown
        (["A", "A", "A", "A", "A", "A", "B", "C", "D", "E", "F", "G"], 2, 16),
        (["A"], 0, 1),
        (["A"], 5, 1),
        ([], 10, 0),
        (["A", "B", "C", "D"], 3, 4),                              # no repeats — no idle
        (["A", "A", "A"], 2, 7),                                   # A _ _ A _ _ A
    ]

    for tasks, n, expected in cases:
        sim_res = schedule_sim(tasks, n)
        form_res = schedule_formula(tasks, n)
        assert sim_res == expected, f"sim({tasks}, {n}) = {sim_res}, want {expected}"
        assert form_res == expected, f"formula({tasks}, {n}) = {form_res}, want {expected}"

    # Stress: simulation and formula agree on random inputs
    import random
    random.seed(42)
    for _ in range(500):
        m = random.randint(0, 100)
        tasks = [chr(ord('A') + random.randint(0, 5)) for _ in range(m)]
        n = random.randint(0, 10)
        assert schedule_sim(tasks, n) == schedule_formula(tasks, n), (
            f"mismatch: tasks={tasks}, n={n}"
        )

    print("All tests passed!")

    # ---------------------------------------------------------------
    # Which Solution To Present In An Interview:
    #
    #   The simulation is ~15 lines and OBVIOUSLY correct once you
    #   describe it; an interviewer will accept it readily.
    #
    #   The formula is 5 lines and demonstrates deeper insight — but
    #   if you can't explain WHY it works, don't lead with it. Start
    #   with simulation; then, if asked to optimize, derive the
    #   formula as a follow-up.
    #
    #   Both run in under a millisecond on LC's test inputs. The
    #   formula is asymptotically faster for huge inputs, but the
    #   "real" interview advantage is clarity of reasoning.
    # ---------------------------------------------------------------
