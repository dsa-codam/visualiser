def brute(nums):
    total = 0
    for i in range(len(nums)):  # every end index i
        T.op()  # @trace
        start = max(0, i - nums[i])
        for j in range(start, i + 1):  # add nums[start..i] from scratch
            T.op()  # @trace
            total += nums[j]
    return total
