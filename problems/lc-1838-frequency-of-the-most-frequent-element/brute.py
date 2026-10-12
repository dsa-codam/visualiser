def brute(nums, k):
    nums = sorted(nums)  # the target of a group is its largest value
    longest = 0
    for right in range(len(nums)):  # nums[right] is the target value
        cost = 0  # increments needed so far
        left = right
        while left >= 0:
            T.op()  # @trace
            cost += nums[right] - nums[left]  # raise nums[left] up to nums[right]
            if cost > k:  # over budget: no longer group with this target
                break
            left -= 1
        longest = max(longest, right - left)  # nums[left+1..right] all fit
    return longest
