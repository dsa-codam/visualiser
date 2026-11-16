def brute(nums, queries):
    nums = sorted(nums)  # the smallest numbers first
    answer = []
    for q in queries:  # every query from scratch
        T.op()  # @trace
        total = 0
        count = 0
        for x in nums:  # take the smallest numbers while they fit
            T.op()  # @trace
            if total + x > q:
                break
            total += x
            count += 1
        answer.append(count)
    return answer
