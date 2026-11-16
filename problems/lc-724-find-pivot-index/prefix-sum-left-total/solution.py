from typing import List  # @hide


class Solution:
    def pivotIndex(self, nums: List[int]) -> int:
        total = 0  # sum of the whole array  # @a:init
        # @trace-begin
        left = None
        right = None

        def snap(i, phase, roles=None, flash=None):
            return dict(
                state={"nums": nums[:], "i": i, "phase": phase, "total": total, "left": left, "right": right},
                roles=roles or {},
                vars=[
                    {"label": "i", "value": "—" if i is None else i, "role": "front"},
                    {"label": "total", "value": total, "flash": flash == "total"},
                    {"label": "left", "value": "—" if left is None else left, "flash": flash == "left"},
                    {"label": "right", "value": "—" if right is None else right, "flash": flash == "right"},
                ],
            )

        T.step("init", "init", "First pass: add up the whole array into total. "
               "Then every right sum can be found from total, without adding again.", **snap(None, "total"))
        # @trace-end
        for i in range(len(nums)):  # first pass  # @a:total
            T.op()  # @trace
            total += nums[i]  # @a:total
            # @trace-begin
            T.step("total", "total", f"i = {i}: total = {total - nums[i]} + ({nums[i]}) = {total}.",
                   **snap(i, "total", {i: "current"}, "total"))
            # @trace-end
        left = 0  # sum of nums[0..i-1]; nothing to the left of index 0  # @a:left0
        # @trace-begin
        T.step("left0", "left0", f"total = {total}. Second pass: left = 0, because nothing is to the left of index 0.",
               **snap(None, "scan", None, "left"))
        # @trace-end
        for i in range(len(nums)):  # second pass: try each index  # @a:check
            T.op()  # @trace
            right = total - left - nums[i]  # everything except the left side and nums[i]  # @a:check
            if left == right:  # @a:check
                # @trace-begin
                T.step("check", "found", f"i = {i}: right = total − left − nums[i] = {total} − {left} − ({nums[i]}) = {right}. "
                       f"left = right = {left}, so {i} is a pivot.", **snap(i, "scan", {i: "best"}, "right"))
                T.step("return", "return", f"Return {i}. We check indexes from left to right, so this is the leftmost pivot.",
                       **snap(i, "done", {i: "best"}))
                # @trace-end
                return i  # @a:return
            # @trace-begin
            T.step("check", "check", f"i = {i}: right = total − left − nums[i] = {total} − {left} − ({nums[i]}) = {right}. "
                   f"left = {left} ≠ {right}, so {i} is not a pivot.", **snap(i, "scan", {i: "current"}, "right"))
            # @trace-end
            left += nums[i]  # nums[i] moves to the left side for the next index  # @a:move
            # @trace-begin
            T.step("move", "move", f"nums[{i}] = {nums[i]} joins the left side: left = {left - nums[i]} + ({nums[i]}) = {left}.",
                   **snap(i, "scan", {i: "current"}, "left"))
            # @trace-end
        # @trace-begin
        T.step("none", "return", f"No index has left = right, so return −1.", **snap(None, "done"))
        # @trace-end
        return -1  # @a:none
