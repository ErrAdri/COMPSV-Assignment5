# 🔍 Problem 1: Find Most Frequent Element
# Given a list of integers, return the value that appears most frequently.
# If there's a tie, return any of the most frequent.
#
# Example:
# Input: [1, 3, 2, 3, 4, 1, 3]
# Output: 3

def most_frequent(numbers):
    if not numbers:
        return None

    counts = {}
    best_value = numbers[0]
    best_count = 0

    for num in numbers:
        counts[num] = counts.get(num, 0) + 1
        if counts[num] > best_count:
            best_count = counts[num]
            best_value = num

    return best_value

"""
Time and Space Analysis for problem 1:
- Best-case: O(n). Every element must be visited at least once, because any
  unseen element could change the answer. Even if all values are identical,
  we still traverse the whole list.
- Worst-case: O(n). One pass over the list; each dictionary lookup/update is
  O(1) on average.
- Average-case: O(n). Same single pass with O(1) average hash operations.
- Space complexity: O(k), where k is the number of distinct values
  (O(n) in the worst case when every value is unique).
- Why this approach? A hash map (dict) gives O(1) average insert and lookup,
  so counting is linear. Tracking the current best while counting avoids a
  second pass over the dictionary.
- Could it be optimized? Not asymptotically: O(n) time is a lower bound.
  collections.Counter(numbers).most_common(1) is shorter but has the same
  complexity. If the list is already sorted, the mode can be found in O(1)
  extra space by counting consecutive runs. The Boyer-Moore voting algorithm
  uses O(1) space but only works when one value is a strict majority (> n/2).
"""


# 🔍 Problem 2: Remove Duplicates While Preserving Order
# Write a function that returns a list with duplicates removed but preserves order.
#
# Example:
# Input: [4, 5, 4, 6, 5, 7]
# Output: [4, 5, 6, 7]

def remove_duplicates(nums):
    seen = set()
    result = []

    for num in nums:
        if num not in seen:
            seen.add(num)
            result.append(num)

    return result

"""
Time and Space Analysis for problem 2:
- Best-case: O(n). Even if every value is the same, each element still has to
  be checked once against the set.
- Worst-case: O(n). One pass; set membership checks and inserts are O(1) on
  average, and list appends are amortized O(1).
- Average-case: O(n).
- Space complexity: O(n). In the worst case (all values unique) both the
  `seen` set and the `result` list hold n items.
- Why this approach? The set answers "have I seen this before?" in O(1), and
  the separate result list keeps the original order. A naive version that
  checks `if num not in result` scans a list each time and is O(n^2).
- Could it be optimized? Not below O(n) time. A one-liner with the same
  complexity is list(dict.fromkeys(nums)), since dicts keep insertion order
  in Python 3.7+. Sorting first would save no time (O(n log n)) and would
  destroy the original order.
"""


# 🔍 Problem 3: Return All Pairs That Sum to Target
# Write a function that returns all unique pairs of numbers in the list that sum to a target.
# Order of output does not matter. Assume input list has no duplicates.
#
# Example:
# Input: ([1, 2, 3, 4], target=5)
# Output: [(1, 4), (2, 3)]

def find_pairs(nums, target):
    seen = set()
    pairs = []

    for num in nums:
        complement = target - num
        if complement in seen:
            # Store each pair smallest-first so the output is consistent.
            pairs.append((min(num, complement), max(num, complement)))
        seen.add(num)

    return pairs

"""
Time and Space Analysis for problem 3:
- Best-case: O(n). Every number must be examined once to know whether it
  belongs to a pair, even if no pairs exist.
- Worst-case: O(n). One pass; each set lookup and insert is O(1) on average.
- Average-case: O(n).
- Space complexity: O(n) for the `seen` set, plus O(p) for the output, where
  p is the number of pairs (at most n/2, since the input has no duplicates).
- Why this approach? For each number we only need to know whether its
  complement (target - num) appeared earlier, and a set answers that in O(1).
  Because a number is only compared with numbers *before* it, each pair is
  found exactly once, so no duplicate pairs appear. The brute-force version
  with two nested loops checks every pair and is O(n^2).
- Could it be optimized? O(n) time is already optimal. If memory is tight,
  sort the list and use two pointers (one at each end): O(n log n) time but
  O(1) extra space besides the output. If the input could contain duplicates,
  storing pairs in a set of tuples would keep them unique.
"""


# 🔍 Problem 4: Simulate List Resizing (Amortized Cost)
# Create a function that adds n elements to a list that has a fixed initial capacity.
# When the list reaches capacity, simulate doubling its size by creating a new list
# and copying all values over (simulate this with print statements).
#
# Example:
# add_n_items(6) → should print when resizing happens.

def add_n_items(n, initial_capacity=1):
    capacity = initial_capacity
    storage = [None] * capacity   # the fixed-size "underlying array"
    size = 0
    total_copies = 0

    for i in range(n):
        if size == capacity:
            new_capacity = capacity * 2
            print(f"Resizing: capacity {capacity} -> {new_capacity}, "
                  f"copying {size} items")
            new_storage = [None] * new_capacity
            for j in range(size):          # copy every existing item over
                new_storage[j] = storage[j]
            total_copies += size
            storage = new_storage
            capacity = new_capacity

        storage[size] = i
        size += 1
        print(f"Added item {i} (size={size}, capacity={capacity})")

    print(f"Done: {n} appends, {total_copies} copies in total, "
          f"final capacity {capacity}")
    return storage[:size]

"""
Time and Space Analysis for problem 4:
- When do resizes happen? Whenever size == capacity at the moment of an
  append. Starting from capacity 1, that is when inserting the 2nd, 3rd,
  5th, 9th, 17th, ... item, i.e. when size reaches a power of 2
  (1, 2, 4, 8, 16, ...). Only about log2(n) resizes happen for n appends.
- What is the worst-case for a single append? O(n). An append that triggers
  a resize must allocate a new array and copy all n current items.
- What is the amortized time per append overall? O(1). The copies across
  all resizes add up to 1 + 2 + 4 + ... + n/2 < n. So n appends cost at most
  n writes + under n copies = under 2n operations in total, which is O(1)
  per append on average over the whole sequence.
- Space complexity: O(n). The capacity is never more than 2n, so at most
  about half the slots are unused. During a resize the old and new arrays
  exist at the same time, briefly using about 3x the current size.
- Why does doubling reduce the cost overall? Each resize doubles capacity,
  so expensive copies get exponentially rarer: after copying k items, the
  next k appends are free of copying. That "pays back" the copy cost. If we
  instead grew by a fixed amount (e.g. +10 slots), resizes would happen
  every 10 appends and the total copying would be about n^2 / 20, making
  each append O(n) amortized. Python's real list uses this same idea with a
  growth factor of about 1.125x plus a constant, which still gives
  amortized O(1) appends while wasting less memory.
"""


# 🔍 Problem 5: Compute Running Totals
# Write a function that takes a list of numbers and returns a new list
# where each element is the sum of all elements up to that index.
#
# Example:
# Input: [1, 2, 3, 4]
# Output: [1, 3, 6, 10]
# Because: [1, 1+2, 1+2+3, 1+2+3+4]

def running_total(nums):
    totals = []
    current = 0

    for num in nums:
        current += num
        totals.append(current)

    return totals

"""
Time and Space Analysis for problem 5:
- Best-case: O(n). Every position needs its own output value, so all n
  elements must be visited.
- Worst-case: O(n). One pass; each step is one addition and one amortized
  O(1) append.
- Average-case: O(n).
- Space complexity: O(n) for the new output list; only O(1) extra besides
  that (the `current` variable).
- Why this approach? Each running total equals the previous total plus the
  current number, so we reuse the last sum instead of re-adding everything
  from the start. The naive version, sum(nums[:i + 1]) for every i, does
  1 + 2 + ... + n additions and is O(n^2).
- Could it be optimized? Time is already optimal. itertools.accumulate(nums)
  does the same thing in C and is faster in practice. If the original list
  is no longer needed, the totals can be written in place to avoid
  allocating a second list (O(1) extra space).
"""


# ✅ Test cases
if __name__ == "__main__":
    # Problem 1: most_frequent
    assert most_frequent([1, 3, 2, 3, 4, 1, 3]) == 3        # example
    assert most_frequent([7]) == 7                           # single item
    assert most_frequent([5, 5, 5, 5]) == 5                  # all identical
    assert most_frequent([1, 2, 2, 1]) in (1, 2)             # tie: either ok
    assert most_frequent([-1, -1, 0, 2]) == -1               # negatives
    assert most_frequent([]) is None                         # empty list
    print("Problem 1 tests passed")

    # Problem 2: remove_duplicates
    assert remove_duplicates([4, 5, 4, 6, 5, 7]) == [4, 5, 6, 7]  # example
    assert remove_duplicates([]) == []                             # empty
    assert remove_duplicates([1, 1, 1]) == [1]                     # all same
    assert remove_duplicates([3, 2, 1]) == [3, 2, 1]               # no dups
    assert remove_duplicates([2, 1, 2, 3, 1]) == [2, 1, 3]         # order kept
    print("Problem 2 tests passed")

    # Problem 3: find_pairs (order does not matter, so compare sorted)
    assert sorted(find_pairs([1, 2, 3, 4], 5)) == [(1, 4), (2, 3)]  # example
    assert find_pairs([1, 2, 3], 100) == []                          # no pairs
    assert find_pairs([], 5) == []                                   # empty
    assert sorted(find_pairs([-2, 0, 2, 4], 2)) == [(-2, 4), (0, 2)] # negatives
    assert find_pairs([5], 10) == []          # a number can't pair with itself
    assert sorted(find_pairs([0, 1, 5, 6, 10], 11)) == [(1, 10), (5, 6)]
    print("Problem 3 tests passed")

    # Problem 4: add_n_items (prints each append and each resize)
    print("\nadd_n_items(6):")
    assert add_n_items(6) == [0, 1, 2, 3, 4, 5]
    print("\nadd_n_items(0):")
    assert add_n_items(0) == []
    print("\nadd_n_items(5, initial_capacity=2):")
    assert add_n_items(5, initial_capacity=2) == [0, 1, 2, 3, 4]
    print("Problem 4 tests passed\n")

    # Problem 5: running_total
    assert running_total([1, 2, 3, 4]) == [1, 3, 6, 10]      # example
    assert running_total([]) == []                           # empty
    assert running_total([5]) == [5]                         # single item
    assert running_total([3, -1, -2, 4]) == [3, 2, 0, 4]     # negatives
    assert running_total([0, 0, 0]) == [0, 0, 0]             # zeros
    print("Problem 5 tests passed")

    print("\nAll tests passed!")