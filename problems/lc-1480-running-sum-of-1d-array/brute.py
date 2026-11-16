def brute(nums):
    result = []
    for i in range(len(nums)):  # every end index i
        T.op()  # @trace
        total = 0  # sum of nums[0..i], computed again from the start
        for j in range(i + 1):
            T.op()  # @trace
            total += nums[j]
        result.append(total)
    return result
