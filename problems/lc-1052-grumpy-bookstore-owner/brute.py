def brute(customers, grumpy, minutes):
    n = len(customers)
    most = 0
    for start in range(n - minutes + 1):  # the technique covers minutes start .. start + minutes - 1
        total = 0
        for i in range(n):  # add up the whole day from scratch
            T.op()  # @trace
            calm = grumpy[i] == 0 or start <= i < start + minutes
            if calm:
                total += customers[i]
        most = max(most, total)
    return most
