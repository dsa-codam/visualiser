from typing import List  # @hide


class Solution:
    def runningSum(self, nums: List[int]) -> List[int]:
        n = len(nums)  # @a:init
        result = [0] * n  # result[i] = nums[0] + nums[1] + ... + nums[i]  # @a:init
        # @trace-begin
        written = 0  # slots of result written so far (the rest show as empty)

        def show(v):
            return "[" + ", ".join(map(str, v)) + "]"

        def snap(i, band=None, label="", r1=None, r2=None, flash=False):
            return dict(
                state={"nums": nums[:], "result": result[:], "i": i, "written": written,
                       "band": band, "label": label, "r1": r1 or {}, "r2": r2 or {}},
                vars=[
                    {"label": "i", "value": "—" if i is None else i, "role": "front"},
                    {"label": "nums[i]", "value": "—" if i is None else nums[i]},
                    {"label": "result[i - 1]", "value": "—" if i is None or i == 0 else result[i - 1]},
                    {"label": "result[i]", "value": "—" if i is None or i >= written else result[i], "flash": flash},
                    {"label": "result", "value": show(result[:written]) if written < n else show(result)},
                ],
            )

        T.step("init", "init", f"n = {n}. result has {n} empty slots. result[i] will hold the sum nums[0] + … + nums[i].", **snap(None))
        # @trace-end
        result[0] = nums[0]  # the first running sum is just the first number  # @a:first
        # @trace-begin
        written = 1
        T.step("first", "first", f"result[0] = nums[0] = {nums[0]}. Nothing comes before index 0, so the first sum is the first number.",
               **snap(0, [0, 0], f"result[0] = nums[0] = {nums[0]}", {0: "current"}, {0: "new"}, flash=True))
        # @trace-end
        for i in range(1, n):  # every next index  # @a:add
            T.op()  # @trace
            result[i] = result[i - 1] + nums[i]  # previous sum + one new number  # @a:add
            # @trace-begin
            written = i + 1
            T.step("add", "add", f"i = {i}: result[{i}] = result[{i - 1}] + nums[{i}] = {result[i - 1]} + {nums[i]} = {result[i]}. "
                   f"result[{i - 1}] already holds the sum of nums[0..{i - 1}], so one addition is enough.",
                   **snap(i, [i - 1, i], f"result[{i}] = {result[i - 1]} + {nums[i]} = {result[i]}", {i: "current"}, {i: "new"}, flash=True))
            # @trace-end
        # @trace-begin
        T.step("return", "return", f"Return result = {show(result)}. Each slot was found with one addition from the slot before it, "
               f"the for loop runs {n - 1} times; the brute force needs {n + n * (n + 1) // 2} iterations.", **snap(None))
        # @trace-end
        return result  # @a:return
