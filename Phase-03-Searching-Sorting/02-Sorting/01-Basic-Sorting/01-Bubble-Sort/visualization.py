"""
visualization.py – Bubble Sort with Pass-by-Pass Visualization

Run bubble sort while PRINTING the array after every pass (and
optionally after every swap). Useful for:

    - Teaching: seeing the largest-bubbles-first pattern.
    - Debugging: catching off-by-one errors in the loop bounds.
    - Intuition: confirming that bubble sort's "sorted tail" grows
      by one element per pass.

This file is the "watch it run" version of bubble sort. It's not
meant for performance — it prints, so it's O(n² · length-of-printout).

---------------------------------------------------
Run this file directly to see the visualization on a small example.
"""


# =========================================================================
# Pass-by-Pass Visualization
# =========================================================================

def bubble_sort_show_passes(arr):
    """
    Sort `arr` in place, printing it after each outer-loop iteration.

    The SORTED TAIL — the final `i + 1` elements after iteration i —
    is highlighted with brackets `[ ]`.
    """
    n = len(arr)
    print(f"   Pass 0 (start):    {arr}")

    for i in range(n - 1):
        swapped = False
        for j in range(n - 1 - i):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped = True

        _print_pass(arr, i + 1, n)

        if not swapped:
            print(f"   → early exit after pass {i + 1} (no swaps made)")
            break

    return arr


def _print_pass(arr, pass_num, n):
    """Print the array, highlighting the sorted tail."""
    unsorted_len = n - pass_num
    unsorted_part = str(arr[:unsorted_len])[:-1]   # drop trailing "]"
    sorted_part = arr[unsorted_len:]
    sorted_str = ", ".join(str(x) for x in sorted_part)
    if sorted_part:
        display = f"{unsorted_part}, [{sorted_str}]]"
    else:
        display = str(arr)
    print(f"   Pass {pass_num}:            {display}")


# =========================================================================
# Step-by-Step Visualization (Every Swap)
# =========================================================================

def bubble_sort_show_swaps(arr, pause=False):
    """
    Sort `arr` printing the array after EACH SWAP. Produces a lot of
    output on large inputs — keep n ≤ ~10 for legibility.

    If `pause` is True, wait for Enter after each swap (interactive mode).
    """
    n = len(arr)
    swap_count = 0
    print(f"   Initial:  {arr}")

    for i in range(n - 1):
        for j in range(n - 1 - i):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swap_count += 1
                # indicate what just happened by showing the two swapped positions
                marker = [" "] * n
                marker[j] = "^"
                marker[j + 1] = "^"
                print(f"   Swap {swap_count:<3}: {arr}")
                print(f"             {' '.join(marker)}")
                if pause:
                    input("   [Enter to continue] ")

    print(f"\n   Final sorted: {arr}  (total swaps: {swap_count})")
    return arr, swap_count


# =========================================================================
# ASCII Bar Chart Rendering
# =========================================================================

def bubble_sort_bars(arr, width=40):
    """
    Render each pass as a simple ASCII bar chart — useful for seeing
    the "heavy elements sink" motion visually.

    The tallest bar is at most `width` characters wide.
    """
    if not arr:
        print("   (empty array)")
        return arr

    mx = max(arr)
    if mx <= 0:
        mx = 1

    def render():
        print()
        for x in arr:
            bars = "█" * int(width * x / mx)
            print(f"   {x:>4} | {bars}")
        print()

    n = len(arr)
    print(f"   === Pass 0 (initial) ===")
    render()

    for i in range(n - 1):
        swapped = False
        for j in range(n - 1 - i):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped = True
        print(f"   === Pass {i + 1} ===")
        render()
        if not swapped:
            break

    return arr


# =========================================================================
# Demonstration
# =========================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("Pass-by-Pass Visualization")
    print("=" * 60)
    bubble_sort_show_passes([5, 2, 9, 1, 5, 6])
    print()

    print("=" * 60)
    print("Step-by-Step (Every Swap)")
    print("=" * 60)
    bubble_sort_show_swaps([3, 1, 4, 1, 5])
    print()

    print("=" * 60)
    print("ASCII Bar Chart")
    print("=" * 60)
    bubble_sort_bars([5, 2, 8, 1, 6, 3])
    print()

    print("=" * 60)
    print("Already-Sorted Input (Classic Early Exit Demo)")
    print("=" * 60)
    bubble_sort_show_passes([1, 2, 3, 4, 5])

    # Basic correctness check
    for data in [[3, 1, 4, 1, 5, 9, 2, 6], [], [1], [5, 4, 3, 2, 1]]:
        expected = sorted(data)
        got = bubble_sort_show_passes(list(data))
        assert got == expected, f"Visualization failed on {data}"

    print("\nCorrectness check on a few inputs: all sorted correctly.")
