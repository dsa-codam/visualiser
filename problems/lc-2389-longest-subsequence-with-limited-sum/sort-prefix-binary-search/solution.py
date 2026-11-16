from typing import List  # @hide


class Solution:
    def answerQueries(self, nums: List[int], queries: List[int]) -> List[int]:
        n = len(nums)  # @a:sort
        nums.sort()  # the smallest numbers first: the best subsequence takes them  # @a:sort
        pre = [0] * (n + 1)  # pre[c] = sum of the c smallest numbers; pre[0] = 0  # @a:sort
        # @trace-begin
        built = 1
        answer = [0] * len(queries)
        answered = 0
        lo = mid = hi = count = j = None

        def snap(i, phase, pre_roles=None, flash=None):
            return dict(
                state={"nums": nums[:], "pre": pre[:], "built": built, "queries": queries[:], "answer": answer[:],
                       "answered": answered, "i": i, "j": j, "lo": lo, "mid": mid, "hi": hi, "phase": phase,
                       "pre_roles": pre_roles or {}},
                roles={i: "current"} if i is not None else {},
                vars=[
                    {"label": "j", "value": "—" if j is None else j, "role": "front"},
                    {"label": "queries[j]", "value": "—" if j is None else queries[j]},
                    {"label": "lo", "value": "—" if lo is None else lo, "role": "back"},
                    {"label": "mid", "value": "—" if mid is None else mid, "role": "mid"},
                    {"label": "hi", "value": "—" if hi is None else hi, "role": "front"},
                    {"label": "count", "value": "—" if count is None else count, "flash": flash == "count"},
                ],
            )

        T.step("sort", "sort", f"nums sorted: {nums}. A subsequence can use any numbers, and to fit as many as possible "
               "under a limit we take the smallest ones. pre[0] = 0: zero numbers, sum 0.", **snap(None, "build", {0: "new"}))
        # @trace-end
        for i in range(n):  # build the prefix array  # @a:build
            T.op()  # @trace
            pre[i + 1] = pre[i] + nums[i]  # @a:build
            # @trace-begin
            built = i + 2
            T.step("build", "build", f"pre[{i + 1}] = pre[{i}] + nums[{i}] = {pre[i]} + {nums[i]} = {pre[i + 1]}: "
                   f"the {i + 1} smallest numbers sum to {pre[i + 1]}.", **snap(i, "build", {i + 1: "new"}))
            # @trace-end
        answer = [0] * len(queries)  # @a:answer
        for j in range(len(queries)):  # one binary search per query  # @a:query
            T.op()  # @trace
            lo = 1  # try counts from 1 to n  # @a:query
            hi = n  # @a:query
            count = 0  # largest count that fits so far  # @a:query
            # @trace-begin
            mid = None
            T.step("query", "query", f"Query j = {j}: limit queries[{j}] = {queries[j]}. Find the largest count with "
                   f"pre[count] ≤ {queries[j]}. pre only grows, so binary search on counts lo = 1 .. hi = {n}.",
                   **snap(None, "query", None, "count"))
            # @trace-end
            while lo <= hi:  # @a:mid
                T.op()  # @trace
                mid = lo + (hi - lo) // 2  # @a:mid
                if pre[mid] <= queries[j]:  # the mid smallest numbers fit  # @a:mid
                    count = mid  # @a:fit
                    lo = mid + 1  # try more numbers  # @a:fit
                    # @trace-begin
                    T.step("fit", "fit", f"mid = {mid}: pre[{mid}] = {pre[mid]} ≤ {queries[j]}, so {mid} numbers fit. "
                           f"count = {mid}; try more: lo = {lo}." + (" lo > hi, so the while loop stops." if lo > hi else ""),
                           **snap(None, "query", {mid: "current"}, "count"))
                    # @trace-end
                else:  # @a:mid
                    hi = mid - 1  # too much: try fewer numbers  # @a:nofit
                    # @trace-begin
                    T.step("nofit", "nofit", f"mid = {mid}: pre[{mid}] = {pre[mid]} > {queries[j]}, so {mid} numbers are too many. "
                           f"Try fewer: hi = {hi}." + (" lo > hi, so the while loop stops." if lo > hi else ""),
                           **snap(None, "query", {mid: "conflict"}))
                    # @trace-end
            answer[j] = count  # @a:store
            # @trace-begin
            answered = j + 1
            lo = mid = hi = None
            T.step("store", "store", f"answer[{j}] = {count}: the {count} smallest numbers sum to {pre[count]} ≤ {queries[j]}.",
                   **snap(None, "query", {count: "best"}))
            # @trace-end
        # @trace-begin
        j = None
        count = None
        T.step("return", "return", f"Return {answer}. pre was built once; each query took one binary search over it.",
               **snap(None, "done"))
        # @trace-end
        return answer  # @a:return
