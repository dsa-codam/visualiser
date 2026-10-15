def brute(blocks, k):
    fewest = k  # a window never needs more than k recolors
    for i in range(len(blocks) - k + 1):  # every possible start of a window
        whites = 0
        for j in range(i, i + k):  # count the 'W' in the window from scratch
            T.op()  # @trace
            if blocks[j] == 'W':
                whites += 1
        fewest = min(fewest, whites)  # each 'W' needs one recolor
    return fewest
