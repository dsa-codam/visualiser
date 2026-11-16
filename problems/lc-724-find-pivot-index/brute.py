def brute(nums):
    n = len(nums)
    for i in range(n):  # try every index as the pivot
        T.op()  # @trace
        left = 0
        right = 0
        for j in range(n):  # add every other number to its side
            T.op()  # @trace
            if j < i:
                left += nums[j]
            elif j > i:
                right += nums[j]
        if left == right:
            return i  # the leftmost pivot
    return -1
