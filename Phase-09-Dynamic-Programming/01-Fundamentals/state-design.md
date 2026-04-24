# State Design — The Art Of DP

Pick the wrong state and no amount of cleverness with transitions
will save you. Pick the right state and the rest is mechanical.

This is the single hardest skill in DP, and the only one that
doesn't transfer cleanly from theory — it comes from solving many
problems and noticing which state variables keep showing up.

---

## What IS the state?

The **state** is the set of arguments your recursive function takes.
Equivalently, the index into your `dp` array. A state must be
**sufficient**: given the state, the answer is fully determined,
independent of how you arrived at that state.

A memoization rule of thumb:

> *If you add `@cache` and the function would return wrong answers
>  due to hidden side effects or missing arguments, your state is
>  incomplete.*

---

## Example: House Robber

Given an array of house values, rob a SUBSET where no two robbed
houses are adjacent. Maximize the sum.

**Wrong state**: `dp[i]` = max rob starting FROM house i onward.
(This *works*, it's just backward-indexed and confusing.)

**Right state**: `dp[i]` = max rob from houses `0..i` inclusive.

**Transition**: at house i, you either rob it (value + dp[i-2]) or
skip it (dp[i-1]):

    dp[i] = max(dp[i-1], houses[i] + dp[i-2])

**Insight**: the state only needs `i` because "what you did before
i-1" doesn't affect what you can do from i onward — the
non-adjacency constraint bounds its horizon to 1 step.

---

## Example: House Robber II — when state needs to grow

Same, but houses are in a CIRCLE (first and last are adjacent now).

**The naive fix doesn't work**: `dp[i]` isn't enough; whether you
robbed house 0 changes what's legal for house n-1.

**Add dimension** to state: `dp[i][robbed_first]` where
`robbed_first ∈ {0, 1}`.

**But simpler**: split into two problems, each without the circle:
- Rob in range [0, n-2] (can't touch last).
- Rob in range [1, n-1] (can't touch first).
Take the max. That's effectively removing one half of the wrap-around
constraint.

This is "decomposition vs. extra state" — often there's a cleaner
problem reformulation than adding a dimension.

---

## Example: Stock Trading (state machine)

LC #309 — Best Time to Buy/Sell Stock with Cooldown. You own at
most one share, can buy/sell many times, but after a sell must wait
one day before buying.

Candidate state: just `dp[i]` = max profit through day i.
**Insufficient** — a profit at day i depends on whether you HOLD a
share, are IN COOLDOWN, or are FREE to buy.

Right state: `dp[i][machine_state]` where `machine_state ∈ {hold,
free, cooldown}`. Three values. Transitions encode the state-machine
rules.

    dp[i][hold]     = max(dp[i-1][hold], dp[i-1][free] - price[i])
    dp[i][free]     = max(dp[i-1][free], dp[i-1][cooldown])
    dp[i][cooldown] = dp[i-1][hold] + price[i]

This "add a dimension for the mode you're in" idea generalizes to
LC #188 (at most k transactions), LC #714 (transaction fee), etc.

---

## Tricks for state design

### 1. "What's enough for the next step?"

Ask: if I handed you just the state, could you decide what to do
next with no other info? If NO, your state is missing something.

### 2. "What changes when I advance one step?"

Often the state is: (position, side-effect-state, capacity-left,
direction-or-mode). Advance = increment position; update side-effect
state based on the decision.

### 3. "What's the output axis?"

If the problem asks "the kth SMALLEST" or "count WAYS", the state
might need to include k or a count. "Number of ways with exactly
k errors" needs (position, errors-so-far) — two dimensions.

### 4. "Am I looking BACK or FORWARD?"

Both work. Looking back (dp[i] from dp[i-1]) is more common.
Looking forward (dp[i] requires future values) requires reverse
iteration. Pick whichever makes the base case cleaner.

### 5. "Interval DP: (l, r), not (i)"

If the problem involves "where do I split", the natural state is a
RANGE `dp[l][r]`, not an index. Matrix-chain, burst balloons,
optimal BST, palindrome partitioning all have state (l, r).

---

## Things that are NOT state

- **Constants**: anything fixed across the whole problem shouldn't be
  in the state. (The input array, a target sum, etc.) They're
  closure variables.
- **Redundant info**: if variable B is derivable from variable A, keep
  only A. ("Position + how many evens so far" is fine; "position +
  how many evens + how many odds" is redundant because `odds = i -
  evens`.)
- **Global counters** that would grow unboundedly: "distinct words
  seen" isn't a state variable because its domain is too big.
  Reformulate.

---

## How to know your state is right

Three signs:

1. **Base cases are simple**: usually dp[0] (or the empty prefix /
   smallest sub-interval) is trivially 0, 1, True, or equal to the
   input value.
2. **Transition formula fits on one line**: if you need multiple
   branches and careful bookkeeping, you're probably missing state.
3. **The memo hit-rate is non-trivial**: if every cached call is a
   miss (no repeat work), DP isn't saving you anything and the
   problem might not be DP at all.

---

## Common state patterns by problem family

| Pattern                        | State                       | Example problems            |
|--------------------------------|-----------------------------|-----------------------------|
| Linear walk                    | `dp[i]`                     | fib, climb, rob, LIS        |
| 2D grid / two-string alignment | `dp[i][j]`                  | paths, LCS, edit dist       |
| Interval / split               | `dp[l][r]`                  | matrix chain, balloons      |
| Knapsack (item + capacity)     | `dp[i][w]`                  | 0/1 knapsack, subset sum    |
| State machine                  | `dp[i][mode]`               | stock-trading family        |
| Bitmask over items             | `dp[mask][i]`               | TSP, assignment             |
| Tree DP                        | `dp[node][mode]`            | rob-iii, tree diameter      |
| Counting + constraints         | `dp[i][count]`              | distinct subsequences       |

If you recognize one of these patterns in a new problem, you're
80% done. The remaining 20% is figuring out the exact transition.
