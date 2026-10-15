def brute(arr, k, threshold):
    count = 0
    for i in range(len(arr) - k + 1):  # every possible start of a window
        total = 0
        for j in range(i, i + k):  # add up the window from scratch
            T.op()  # @trace
            total += arr[j]
        if total / k >= threshold:  # the average, as the statement defines it
            count += 1
    return count
