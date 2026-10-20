def brute(nums, k):
    n = len(nums)
    avgs = [-1] * n
    for i in range(n):  # every possible centre
        if i - k < 0 or i + k >= n:  # fewer than k numbers on one side: stays -1
            continue
        total = 0
        for j in range(i - k, i + k + 1):  # add up the window from scratch
            T.op()  # @trace
            total += nums[j]
        avgs[i] = total // (2 * k + 1)
    return avgs
