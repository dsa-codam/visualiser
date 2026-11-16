from typing import List  # @hide


class Solution:
    def isArraySpecial(self, nums: List[int], queries: List[List[int]]) -> List[bool]:
        n = len(nums)  # @a:init
        pre = [0] * n  # pre[i] = bad pairs (same parity) inside nums[0..i]  # @a:init
        # @trace-begin
        built = 1
        answer = []
        j = left = right = bad = None

        def snap(i, phase, pre_roles=None, roles=None, band=None, flash=None):
            return dict(
                state={"nums": nums[:], "pre": pre[:], "built": built, "queries": [f"[{a},{b}]" for a, b in queries],
                       "answer": ["true" if x else "false" for x in answer], "i": i, "j": j, "left": left, "right": right,
                       "phase": phase, "band": band, "pre_roles": pre_roles or {}},
                roles=roles or {},
                vars=[
                    {"label": "j", "value": "—" if j is None else j, "role": "front"},
                    {"label": "left", "value": "—" if left is None else left, "role": "back"},
                    {"label": "right", "value": "—" if right is None else right, "role": "front"},
                    {"label": "bad", "value": "—" if bad is None else bad, "flash": flash == "bad"},
                ],
            )

        T.step("init", "init", "pre[0] = 0: one number alone has no pairs. A pair (i − 1, i) is bad when both numbers "
               "are even or both are odd.", **snap(None, "build", {0: "new"}))
        # @trace-end
        for i in range(1, n):  # pair (i - 1, i)  # @a:build
            T.op()  # @trace
            pre[i] = pre[i - 1]  # @a:build
            if nums[i] % 2 == nums[i - 1] % 2:  # same parity: a bad pair  # @a:build
                pre[i] += 1  # @a:build
            # @trace-begin
            built = i + 1
            same = nums[i] % 2 == nums[i - 1] % 2
            word = "odd" if nums[i] % 2 else "even"
            T.step("build", "build", f"Pair ({i - 1}, {i}): {nums[i - 1]} and {nums[i]} are " +
                   (f"both {word}, a bad pair: pre[{i}] = {pre[i - 1]} + 1 = {pre[i]}." if same
                    else f"different parity, fine: pre[{i}] = pre[{i - 1}] = {pre[i]}."),
                   **snap(i, "build", {i: "new"}, {i - 1: "current", i: "current"},
                          {"from": i - 1, "to": i, "bad": same, "label": "same parity ✗" if same else "different ✓"}))
            # @trace-end
        answer = []  # @a:answer
        for j in range(len(queries)):  # @a:query
            T.op()  # @trace
            left = queries[j][0]  # @a:query
            right = queries[j][1]  # @a:query
            bad = pre[right] - pre[left]  # bad pairs with both numbers inside nums[left..right]  # @a:query
            answer.append(bad == 0)  # special = no bad pair  # @a:query
            # @trace-begin
            T.step("query", "query", f"Query j = {j}: [{left}, {right}]. bad = pre[{right}] − pre[{left}] = {pre[right]} − {pre[left]} = {bad}. "
                   + ("No bad pair inside, so answer[j] = true." if bad == 0 else f"{bad} bad pair{'s' if bad > 1 else ''} inside, so answer[j] = false."),
                   **snap(None, "query", {left: "current", right: "current"}, None,
                          {"from": left, "to": right, "bad": bad > 0, "label": f"bad = {bad}"}, "bad"))
            # @trace-end
        # @trace-begin
        j = left = right = bad = None
        T.step("return", "return", "pre[i] counts the bad pairs up to index i. pre[left] holds the pairs that end at or before left, "
               "so pre[right] − pre[left] counts exactly the pairs inside the range: each query is O(1).", **snap(None, "done"))
        # @trace-end
        return answer  # @a:return
