def brute(s):
    longest = 0
    for i in range(len(s)):  # every start
        seen = [False] * 128  # characters in s[i..j]
        j = i
        while j < len(s):
            T.op()  # @trace
            if seen[ord(s[j])]:  # repeat: no longer substring starts at i
                break
            seen[ord(s[j])] = True
            j += 1
        longest = max(longest, j - i)  # s[i..j-1] is unique
    return longest
