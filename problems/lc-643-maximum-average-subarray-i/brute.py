def brute(nums, k):
    largest = None
    for i in range(len(nums) - k + 1):  # every possible start of a window
        total = 0
        for j in range(i, i + k):  # add up the window from scratch
            T.op()  # @trace
            total += nums[j]
        if largest is None or total > largest:
            largest = total
    return largest / k  # same length k for all windows: largest sum = largest average
