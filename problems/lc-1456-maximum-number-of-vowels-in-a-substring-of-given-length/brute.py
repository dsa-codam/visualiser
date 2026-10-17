def brute(s, k):
    most = 0
    for i in range(len(s) - k + 1):  # every possible start of a window
        vowels = 0
        for j in range(i, i + k):  # count the vowels in the window from scratch
            T.op()  # @trace
            if s[j] in "aeiou":
                vowels += 1
        most = max(most, vowels)
    return most
