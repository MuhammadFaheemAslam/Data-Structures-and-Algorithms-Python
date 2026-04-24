"""
Matrix Chain Multiplication — The Textbook Interval-DP Problem

Given a chain of matrices A1, A2, ..., An where matrix Ai has
dimensions `dims[i-1] x dims[i]`, find the PARENTHESIZATION that
minimizes the total number of SCALAR MULTIPLICATIONS required to
compute their product.

Input is given as `dims` — a list of `n+1` numbers describing the
sequence of dimensions. For example, `dims = [10, 30, 5, 60]` means
3 matrices of sizes 10×30, 30×5, 5×60.

Multiplying an a×b matrix by a b×c matrix costs `a*b*c` scalar
multiplications.

---------------------------------------------------
Why Parenthesization Matters:

Matrix multiplication is ASSOCIATIVE — `A(BC) = (AB)C` — but the
COST is NOT.

Example:  A(10×30) · B(30×5) · C(5×60)

    ((AB)C):  AB needs 10·30·5 = 1500. ABc needs 10·5·60 = 3000. Total 4500.
    (A(BC)):  BC needs 30·5·60 = 9000. A(BC) needs 10·30·60 = 18000. Total 27000.

So the order chosen affects the total by a factor of 6×. This
problem asks for the minimum.

---------------------------------------------------
The Interval DP:

    dp[l][r] = min scalar mults to compute the product A_l · ... · A_r

For every split point k in [l..r-1]:

    dp[l][r] = min over k of (
        dp[l][k] + dp[k+1][r] + dims[l-1] * dims[k] * dims[r]
    )

    The "multiply result of left · result of right" costs
    dims[l-1] * dims[k] * dims[r], where:
        left piece has shape (dims[l-1], dims[k])
        right piece has shape (dims[k], dims[r])

Base case: dp[i][i] = 0 (a single matrix is already computed).

Time O(n³), Space O(n²).

---------------------------------------------------
Historical / Practical Note:

This was one of the ORIGINAL interval-DP problems studied in the
1970s. The algorithmic technique has wider use (see palindrome
partitioning, burst balloons, etc.). Modern numerical libraries
actually compile matrix-chain expressions optimally at runtime —
e.g. NumPy's `np.linalg.multi_dot`.
"""


def matrix_chain_min_mults(dims):
    """
    Return the minimum number of scalar multiplications for a chain of
    n = len(dims) - 1 matrices with dimensions given by `dims`.

    Time: O(n³), Space: O(n²).
    """
    n = len(dims) - 1                                       # number of matrices
    if n <= 1:
        return 0                                            # 0 or 1 matrix — nothing to multiply

    # dp[i][j] = min mults to compute the product of matrices i..j (1-indexed)
    # For ergonomics, we index from 1 to n inclusive.
    INF = float("inf")
    dp = [[0] * (n + 2) for _ in range(n + 2)]

    # Fill by chain length
    for length in range(2, n + 1):
        for i in range(1, n - length + 2):
            j = i + length - 1
            dp[i][j] = INF
            for k in range(i, j):
                cost = dp[i][k] + dp[k + 1][j] + dims[i - 1] * dims[k] * dims[j]
                if cost < dp[i][j]:
                    dp[i][j] = cost

    return dp[1][n]


# -------- Reconstruction: which split is optimal at each stage? --------

def matrix_chain_parenthesization(dims):
    """
    Return (min_mults, parenthesized_string) — a human-readable description
    of the optimal grouping, e.g. "((A1*A2)*A3)".

    Time: O(n³), Space: O(n²).
    """
    n = len(dims) - 1
    if n == 0:
        return (0, "")
    if n == 1:
        return (0, "A1")

    INF = float("inf")
    dp = [[0] * (n + 2) for _ in range(n + 2)]
    best_split = [[0] * (n + 2) for _ in range(n + 2)]

    for length in range(2, n + 1):
        for i in range(1, n - length + 2):
            j = i + length - 1
            dp[i][j] = INF
            for k in range(i, j):
                cost = dp[i][k] + dp[k + 1][j] + dims[i - 1] * dims[k] * dims[j]
                if cost < dp[i][j]:
                    dp[i][j] = cost
                    best_split[i][j] = k

    def build(i, j):
        if i == j:
            return f"A{i}"
        k = best_split[i][j]
        return "(" + build(i, k) + "*" + build(k + 1, j) + ")"

    return (dp[1][n], build(1, n))


# =========================================================================
# Test
# =========================================================================

if __name__ == "__main__":
    # Classic CLRS example
    # Matrices: 30×35, 35×15, 15×5, 5×10, 10×20, 20×25
    # Min cost = 15125
    assert matrix_chain_min_mults([30, 35, 15, 5, 10, 20, 25]) == 15125

    # Small examples
    assert matrix_chain_min_mults([10, 30, 5, 60]) == 4500
    assert matrix_chain_min_mults([40, 20, 30, 10, 30]) == 26000

    # Edge cases
    assert matrix_chain_min_mults([]) == 0                               # no matrices
    assert matrix_chain_min_mults([10]) == 0                             # still no matrices
    assert matrix_chain_min_mults([10, 20]) == 0                         # 1 matrix
    assert matrix_chain_min_mults([10, 20, 30]) == 6000                  # 2 matrices: 10*20*30 = 6000

    # Reconstruction matches
    cost, paren = matrix_chain_parenthesization([10, 30, 5, 60])
    assert cost == 4500
    assert paren == "((A1*A2)*A3)"

    cost, paren = matrix_chain_parenthesization([30, 35, 15, 5, 10, 20, 25])
    assert cost == 15125
    # The optimal split is "(A1(A2A3))((A4A5)A6)" — verify it's SOMETHING sensible
    assert paren.count("A") == 6
    assert paren.count("(") == paren.count(")")

    # Brute force: enumerate all parenthesizations (Catalan-many)
    def brute(dims):
        n = len(dims) - 1
        if n <= 1:
            return 0
        from functools import cache
        @cache
        def rec(i, j):
            if i == j:
                return 0
            best = float("inf")
            for k in range(i, j):
                best = min(best, rec(i, k) + rec(k + 1, j) + dims[i - 1] * dims[k] * dims[j])
            return best
        return rec(1, n)

    import random
    random.seed(42)
    for _ in range(50):
        n = random.randint(0, 8)
        dims = [random.randint(1, 20) for _ in range(n + 1)]
        assert matrix_chain_min_mults(dims) == brute(dims)

    print("All tests passed!")
