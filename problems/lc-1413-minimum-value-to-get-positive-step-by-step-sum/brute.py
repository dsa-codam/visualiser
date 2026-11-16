def brute(nums):
    start_value = 1  # the smallest positive candidate
    while True:  # try 1, 2, 3, ... until one works
        T.op()  # @trace
        total = start_value  # step-by-step sum, starting from start_value
        ok = True
        for x in nums:  # add the numbers one by one
            T.op()  # @trace
            total += x
            if total < 1:  # dropped below 1: this start_value is too small
                ok = False
                break
        if ok:
            return start_value
        start_value += 1
