def brute(nums, queries):
    answer = []
    for left, right in queries:  # every query from scratch
        T.op()  # @trace
        special = True
        for i in range(left + 1, right + 1):  # every pair (i - 1, i) inside the range
            T.op()  # @trace
            if nums[i] % 2 == nums[i - 1] % 2:  # same parity: not special
                special = False
                break
        answer.append(special)
    return answer
