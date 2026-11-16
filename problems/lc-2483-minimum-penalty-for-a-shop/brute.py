def brute(customers):
    n = len(customers)
    best_hour = 0
    best = n + 1  # more than any possible penalty
    for j in range(n + 1):  # try every closing hour
        T.op()  # @trace
        penalty = 0
        for i in range(n):  # count the penalty from scratch
            T.op()  # @trace
            if i < j and customers[i] == 'N':  # open, nobody comes
                penalty += 1
            elif i >= j and customers[i] == 'Y':  # closed, customers come
                penalty += 1
        if penalty < best:  # strictly lower: keep the earliest hour
            best = penalty
            best_hour = j
    return best_hour
