from typing import List  # @hide


class Solution:
    def subarraySum(self, nums: List[int]) -> int:
        n = len(nums)  # @a:init
        pre = [0] * (n + 1)  # pre[i] = nums[0] + ... + nums[i - 1]; pre[0] = 0  # @a:init
        # @trace-begin
        total = None
        start = None
        subarray_sum = None
        built = 1  # slots of pre written so far

        def snap(i, phase, pre_roles=None, roles=None, flash=None):
            return dict(
                state={"nums": nums[:], "pre": pre[:], "built": built, "i": i, "phase": phase, "start": start,
                       "subarray_sum": subarray_sum, "total": total, "pre_roles": pre_roles or {}},
                roles=roles or {},
                vars=[
                    {"label": "i", "value": "—" if i is None else i, "role": "front"},
                    {"label": "start", "value": "—" if start is None else start, "role": "back"},
                    {"label": "subarray_sum", "value": "—" if subarray_sum is None else subarray_sum, "flash": flash == "sub"},
                    {"label": "total", "value": "—" if total is None else total, "flash": flash == "total"},
                ],
            )

        T.step("init", "init", f"pre has n + 1 = {n + 1} slots. pre[0] = 0 is the sum of no numbers, "
               "so every subarray sum can be one subtraction, even one that starts at index 0.", **snap(None, "build", {0: "new"}))
        # @trace-end
        for i in range(n):  # build the prefix array  # @a:build
            T.op()  # @trace
            pre[i + 1] = pre[i] + nums[i]  # @a:build
            # @trace-begin
            built = i + 2
            T.step("build", "build", f"pre[{i + 1}] = pre[{i}] + nums[{i}] = {pre[i]} + {nums[i]} = {pre[i + 1]}.",
                   **snap(i, "build", {i + 1: "new"}, {i: "current"}))
            # @trace-end
        total = 0  # @a:total0
        # @trace-begin
        T.step("total0", "total0", "pre is ready. Now each subarray sum costs one subtraction. total = 0.", **snap(None, "query"))
        # @trace-end
        for i in range(n):  # one subarray for every index i  # @a:query
            T.op()  # @trace
            start = max(0, i - nums[i])  # the subarray is nums[start..i]  # @a:query
            subarray_sum = pre[i + 1] - pre[start]  # sum of nums[start..i]  # @a:query
            total += subarray_sum  # @a:query
            # @trace-begin
            T.step("query", "query", f"i = {i}: start = max(0, {i} − {nums[i]}) = {start}. "
                   f"Sum of nums[{start}..{i}] = pre[{i + 1}] − pre[{start}] = {pre[i + 1]} − {pre[start]} = {subarray_sum}. "
                   f"total = {total - subarray_sum} + {subarray_sum} = {total}.",
                   **snap(i, "query", {i + 1: "current", start: "current"}, {i: "current"}, "total"))
            # @trace-end
        # @trace-begin
        start = None
        subarray_sum = None
        T.step("return", "return", f"Return total = {total}. Every subarray sum came from two cells of pre, "
               "so the second loop is O(n).", **snap(None, "done"))
        # @trace-end
        return total  # @a:return
