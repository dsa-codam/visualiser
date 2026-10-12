def brute(nums):
    squares = [x * x for x in nums]  # square every value
    for i in range(1, len(squares)):  # insertion sort on the squares
        value = squares[i]
        k = i - 1
        while k >= 0:
            T.op()  # @trace
            if squares[k] <= value:  # found where value belongs
                break
            squares[k + 1] = squares[k]  # shift the bigger value right
            k -= 1
        squares[k + 1] = value
    return squares
