def brute(nums, k):
    nice = 0
    for i in range(len(nums)):  # every start of a subarray
        T.op()  # @trace
        odd = 0
        for j in range(i, len(nums)):  # every end, counting odd numbers on the way
            T.op()  # @trace
            odd += nums[j] % 2
            if odd == k:
                nice += 1
    return nice
