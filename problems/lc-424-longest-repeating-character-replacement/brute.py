def brute(s, k):
    longest = 0
    for i in range(len(s)):  # every start
        count = [0] * 26  # letter -> times in s[i..j]
        top = 0  # highest count of one letter in s[i..j]
        for j in range(i, len(s)):
            T.op()  # @trace
            count[ord(s[j]) - ord('A')] += 1
            top = max(top, count[ord(s[j]) - ord('A')])
            if (j - i + 1) - top <= k:  # change every letter except the top one
                longest = max(longest, j - i + 1)
    return longest
