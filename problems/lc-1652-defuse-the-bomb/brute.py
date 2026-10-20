def brute(code, k):
    n = len(code)
    result = [0] * n
    for i in range(n):  # every position gets its own sum
        total = 0
        for step in range(1, abs(k) + 1):  # the |k| numbers after i (k > 0) or before i (k < 0)
            T.op()  # @trace
            if k > 0:
                total += code[(i + step) % n]
            else:
                total += code[(i - step) % n]
        result[i] = total
    return result
