def brute(nums, threshold):
    longest = 0
    for l in range(len(nums)):  # every start
        T.op()  # @trace
        if nums[l] % 2 != 0 or nums[l] > threshold:  # a subarray must start with an even value <= threshold
            continue
        r = l
        while r + 1 < len(nums):
            T.op()  # @trace
            if nums[r + 1] > threshold:  # too big: the subarray ends at r
                break
            if nums[r + 1] % 2 == nums[r] % 2:  # same parity: the subarray ends at r
                break
            r += 1
        longest = max(longest, r - l + 1)  # nums[l..r] is valid
    return longest
