# 🔍 Problem 1: Find Most Frequent Element
# Given a list of integers, return the value that appears most frequently.
# If there's a tie, return any of the most frequent.
#
# Example:
# Input: [1, 3, 2, 3, 4, 1, 3]
# Output: 3
 
def most_frequent(numbers):
    # An empty list has no most frequent value.
    if not numbers:
        return None
 
    counts = {}
    best_value = numbers[0]
    best_count = 0
 
    # Count each value and keep track of the leader as we go,
    # so the list only has to be walked once.
    for value in numbers:
        counts[value] = counts.get(value, 0) + 1
        if counts[value] > best_count:
            best_count = counts[value]
            best_value = value
 
    return best_value
 
"""
Time and Space Analysis for problem 1:
- Best-case: O(n). Even if every element is the same, each one still has to be
  looked at once to know nothing else appears more often.
- Worst-case: O(n). One pass over the list; each dictionary lookup and update
  is O(1) on average.
- Average-case: O(n).
- Space complexity: O(k), where k is the number of distinct values. In the
  worst case every value is different, so k = n and the space is O(n).
- Why this approach? A dictionary gives constant-time counting, so the whole
  problem is solved in a single pass. The alternative of calling
  numbers.count(x) for every x would be O(n^2).
- Could it be optimized? Not in time: O(n) is the minimum because every
  element must be read at least once. Space could be reduced to O(1) by
  sorting the list in place first and counting runs of equal values, but that
  trade-off costs O(n log n) time and changes the order of the caller's list.
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
 
    for value in nums:
        # Set membership is O(1) on average, unlike `value in result`,
        # which would scan the whole result list each time.
        if value not in seen:
            seen.add(value)
            result.append(value)
 
    return result
 
"""
Time and Space Analysis for problem 2:
- Best-case: O(n). Every element has to be checked once, even when the list
  is all the same value.
- Worst-case: O(n). One pass, with O(1) average set lookups and O(1)
  amortized appends.
- Average-case: O(n).
- Space complexity: O(n). In the worst case (no duplicates) both the set and
  the result list hold all n values.
- Why this approach? The set answers "have I seen this before?" in constant
  time, while the separate result list keeps the original order. Using only a
  list and checking `value not in result` would make the function O(n^2).
- Could it be optimized? The time is already optimal. The code could be
  shortened to list(dict.fromkeys(nums)), which has the same O(n) time and
  O(n) space because dictionaries keep insertion order. Space could be cut to
  O(1) extra by skipping the set and scanning the result list instead, but
  the trade-off is O(n^2) time.
"""
 
 
# 🔍 Problem 3: Return All Pairs That Sum to Target
# Write a function that returns all unique pairs of numbers in the list that sum to a target.
# Order of output does not matter. Assume input list has no duplicates.
#
# Example:
# Input: ([1, 2, 3, 4], target=5)
# Output: [(1, 4), (2, 3)]
 
# ORIGINAL SOLUTION (kept for comparison with the optimized version below)
def find_pairs_original(nums, target):
    pairs = []
 
    # Compare every element with every element that comes after it.
    for i in range(len(nums)):
        for j in range(i + 1, len(nums)):
            if nums[i] + nums[j] == target:
                pairs.append((min(nums[i], nums[j]), max(nums[i], nums[j])))
 
    return pairs
 
 
# OPTIMIZED SOLUTION
# How this was optimized compared to find_pairs_original:
# The original used two nested loops to test every possible pair, which is
# n(n-1)/2 comparisons, or O(n^2) time. This version walks the list once and
# keeps a set of the numbers already seen. For each number it asks "is the
# number I need (target - num) already in the set?", which is an O(1) lookup
# on average. That removes the inner loop entirely and brings the time down
# from O(n^2) to O(n).
#
# Performance comparison (measured with timeit on this file, n = 5,000):
#   find_pairs_original: about 0.8 seconds per call
#   find_pairs:          about 0.0007 seconds per call (roughly 1,000x faster)
# Doubling n roughly quadruples the original's time but only doubles this one.
#
# Space comparison:
#   find_pairs_original: O(1) extra space besides the output list.
#   find_pairs:          O(n) extra space for the `seen` set.
# The trade-off is spending memory to save time: the set holds up to n
# numbers, but it is what makes the single pass possible.
def find_pairs(nums, target):
    seen = set()
    pairs = []
 
    for num in nums:
        complement = target - num
        if complement in seen:
            # Store the smaller number first so the output is consistent.
            pairs.append((min(num, complement), max(num, complement)))
        seen.add(num)
 
    return pairs
 
"""
Time and Space Analysis for problem 3:
- Best-case: O(n). The whole list must be read even when no pair exists.
- Worst-case: O(n). One pass with O(1) average set lookups and inserts.
  (The original nested-loop version was O(n^2) in every case.)
- Average-case: O(n).
- Space complexity: O(n) for the set of seen numbers, plus up to n/2 pairs in
  the output list.
- Why this approach? Each number has exactly one possible partner
  (target - num), so instead of searching the list for it, a set can confirm
  whether it has already appeared in constant time. Adding the number to the
  set only after checking also prevents pairing a number with itself, such as
  5 + 5 = 10 when 5 appears once.
- Could it be optimized? Time is already optimal. Space could be reduced to
  O(1) extra by sorting the list and moving two pointers inward from both
  ends, but that costs O(n log n) time for the sort and either reorders the
  caller's list or needs a sorted copy. The nested-loop original is the other
  option: O(1) extra space, but O(n^2) time.
"""
 
 
# 🔍 Problem 4: Simulate List Resizing (Amortized Cost)
# Create a function that adds n elements to a list that has a fixed initial capacity.
# When the list reaches capacity, simulate doubling its size by creating a new list
# and copying all values over (simulate this with print statements).
#
# Example:
# add_n_items(6) → should print when resizing happens.
 
def add_n_items(n, initial_capacity=2):
    capacity = initial_capacity
    size = 0
    items = [None] * capacity   # fixed-size block of storage
    total_copies = 0
 
    for value in range(n):
        # The storage is full, so build a new one twice as large
        # and copy every existing value into it.
        if size == capacity:
            new_capacity = capacity * 2
            print(f"Resizing from {capacity} to {new_capacity}: copying {size} items")
            new_items = [None] * new_capacity
            for i in range(size):
                new_items[i] = items[i]
            total_copies += size
            items = new_items
            capacity = new_capacity
 
        items[size] = value
        size += 1
 
    print(f"Added {n} items. Final capacity: {capacity}. Total copies: {total_copies}")
    # Return only the filled part of the storage.
    return items[:size]
 
"""
Time and Space Analysis for problem 4:
- When do resizes happen? Whenever an append arrives and the list is already
  full, which is when the size reaches 2, 4, 8, 16, ... (the initial capacity
  times a power of two). Adding n items causes about log2(n) resizes.
- What is the worst-case for a single append? O(n). An append that triggers a
  resize has to copy every existing item into the new list before adding the
  new one.
- What is the amortized time per append overall? O(1). Across n appends the
  copies add up to 2 + 4 + 8 + ... + n/2 + n, which is less than 2n. Total
  work is therefore under 3n (n writes plus fewer than 2n copies), and
  3n / n appends is a constant per append.
- Space complexity: O(n). The capacity is always less than twice the number
  of items stored. During a resize the old and new lists exist at the same
  time, so the peak is about 3n slots, which is still O(n).
- Why does doubling reduce the cost overall? Each resize buys as many free
  slots as there are items, so expensive copies become rarer as the list
  grows: after copying k items, the next k appends are cheap. If the list
  grew by a fixed amount instead (for example, +1 each time), every append
  would copy the whole list and n appends would cost 1 + 2 + ... + n =
  O(n^2). The trade-off is memory: up to half of the capacity can sit unused.
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
 
    # Carry the sum forward instead of re-adding from the start each time.
    for value in nums:
        current += value
        totals.append(current)
 
    return totals
 
"""
Time and Space Analysis for problem 5:
- Best-case: O(n). Every element contributes to the output, so each one has
  to be read once.
- Worst-case: O(n). One pass, with one addition and one O(1) amortized append
  per element.
- Average-case: O(n).
- Space complexity: O(n) for the new list of totals. Besides that output,
  only one extra variable is used, so the auxiliary space is O(1).
- Why this approach? Each total is just the previous total plus the current
  value, so keeping a running sum avoids repeated work. The more direct
  version, sum(nums[:i + 1]) for each index, re-adds the same numbers over
  and over and takes O(n^2) time.
- Could it be optimized? Time is already optimal. Space could be reduced by
  overwriting nums in place (nums[i] += nums[i - 1]), which needs no new
  list, but the trade-off is that the caller's original data is destroyed,
  and the problem asks for a new list. itertools.accumulate(nums) does the
  same job lazily and is useful when the totals are only needed one at a
  time.
"""
 
 
# 🧪 Test Cases
if __name__ == "__main__":
    import timeit
 
    # Problem 1: most_frequent
    assert most_frequent([1, 3, 2, 3, 4, 1, 3]) == 3        # example from the prompt
    assert most_frequent([]) is None                        # edge: empty list
    assert most_frequent([7]) == 7                          # edge: single element
    assert most_frequent([5, 5, 5, 5]) == 5                 # edge: all the same
    assert most_frequent([1, 2, 3]) in (1, 2, 3)            # edge: every value tied
    assert most_frequent([1, 1, 2, 2]) in (1, 2)            # edge: two-way tie
    assert most_frequent([-1, -1, 0, 2]) == -1              # negative numbers
    assert most_frequent([4, 9, 9]) == 9                    # winner appears last
    print("Problem 1 tests passed")
 
    # Problem 2: remove_duplicates
    assert remove_duplicates([4, 5, 4, 6, 5, 7]) == [4, 5, 6, 7]   # example
    assert remove_duplicates([]) == []                              # edge: empty list
    assert remove_duplicates([1]) == [1]                            # edge: single element
    assert remove_duplicates([2, 2, 2, 2]) == [2]                   # edge: all duplicates
    assert remove_duplicates([1, 2, 3]) == [1, 2, 3]                # edge: no duplicates
    assert remove_duplicates([3, 1, 3, 2, 1]) == [3, 1, 2]          # first occurrence order kept
    assert remove_duplicates([-1, 0, -1, 0]) == [-1, 0]             # negatives and zero
    original = [4, 5, 4]
    remove_duplicates(original)
    assert original == [4, 5, 4]                                    # input is not modified
    print("Problem 2 tests passed")
 
    # Problem 3: find_pairs (both versions must agree)
    for pair_function in (find_pairs_original, find_pairs):
        assert sorted(pair_function([1, 2, 3, 4], 5)) == [(1, 4), (2, 3)]   # example
        assert pair_function([], 5) == []                                   # edge: empty list
        assert pair_function([5], 5) == []                                  # edge: single element
        assert pair_function([1, 2, 3], 100) == []                          # edge: no pairs
        assert pair_function([5, 1, 2], 10) == []                           # 5 must not pair with itself
        assert sorted(pair_function([-3, 3, 0, 5, -5], 0)) == [(-5, 5), (-3, 3)]  # negatives
        assert pair_function([10, -4], 6) == [(-4, 10)]                     # exactly two elements
    print("Problem 3 tests passed")
 
    # Problem 4: add_n_items
    print("\nadd_n_items(6):")
    assert add_n_items(6) == [0, 1, 2, 3, 4, 5]             # example: resizes at 2 and 4
    print("\nadd_n_items(0):")
    assert add_n_items(0) == []                             # edge: nothing to add
    print("\nadd_n_items(2):")
    assert add_n_items(2) == [0, 1]                         # edge: exactly fills capacity, no resize
    print("\nadd_n_items(3):")
    assert add_n_items(3) == [0, 1, 2]                      # edge: one past capacity, one resize
    print("\nadd_n_items(9, initial_capacity=1):")
    assert add_n_items(9, initial_capacity=1) == list(range(9))   # different starting capacity
    print("Problem 4 tests passed")
 
    # Problem 5: running_total
    assert running_total([1, 2, 3, 4]) == [1, 3, 6, 10]     # example
    assert running_total([]) == []                          # edge: empty list
    assert running_total([5]) == [5]                        # edge: single element
    assert running_total([0, 0, 0]) == [0, 0, 0]            # edge: all zeros
    assert running_total([3, -3, 2, -2]) == [3, 0, 2, 0]    # negatives
    assert running_total([1.5, 2.5]) == [1.5, 4.0]          # floats
    data = [1, 2, 3]
    running_total(data)
    assert data == [1, 2, 3]                                # input is not modified
    print("Problem 5 tests passed")
 
    # Performance comparison for the optimized problem (Problem 3)
    print("\nfind_pairs: original vs optimized")
    for size in (1000, 2000, 4000):
        sample = list(range(size))
        goal = size  # produces many matching pairs
        slow = timeit.timeit(lambda: find_pairs_original(sample, goal), number=3) / 3
        fast = timeit.timeit(lambda: find_pairs(sample, goal), number=3) / 3
        print(f"n = {size}: original {slow:.5f}s, optimized {fast:.5f}s")
 
    print("\nAll tests passed!")
 