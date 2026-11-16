from typing import List  # @hide


class Solution:
    def minStartValue(self, nums: List[int]) -> int:
        total = 0  # running sum: nums[0] + ... + nums[i]  # @a:init
        lowest = 0  # lowest running sum so far; 0 = before any number  # @a:init
        # @trace-begin
        start_value = None

        def snap(i, roles=None, flash=None):
            return dict(
                state={"nums": nums[:], "i": i, "total": total, "lowest": lowest, "start_value": start_value},
                roles=roles or {},
                vars=[
                    {"label": "i", "value": "—" if i is None else i, "role": "front"},
                    {"label": "nums[i]", "value": "—" if i is None else nums[i]},
                    {"label": "total", "value": total, "flash": flash == "total"},
                    {"label": "lowest", "value": lowest, "flash": flash == "lowest"},
                    {"label": "start_value", "value": "—" if start_value is None else start_value, "flash": flash == "start"},
                ],
            )

        T.step("init", "init", "total = 0 and lowest = 0. total will be the step-by-step sum without startValue. "
               "lowest starts at 0: before any number, the sum is just startValue.", **snap(None))
        # @trace-end
        for i in range(len(nums)):  # @a:add
            T.op()  # @trace
            total += nums[i]  # add one more number  # @a:add
            # @trace-begin
            old = lowest
            # @trace-end
            if total < lowest:  # a new lowest point  # @a:add
                lowest = total  # @a:add
            # @trace-begin
            if lowest < old:
                tail = f"That is lower than {old}, so lowest = {lowest}."
            else:
                tail = f"Not lower than lowest = {lowest}, so lowest stays."
            T.step("add", "add", f"i = {i}: total = {total - nums[i]} + ({nums[i]}) = {total}. {tail}",
                   **snap(i, {i: "current"}, "lowest" if lowest < old else "total"))
            # @trace-end
        start_value = 1 - lowest  # startValue + lowest must be at least 1  # @a:return
        # @trace-begin
        T.step("return", "return", f"The lowest step-by-step sum is startValue + lowest = startValue + ({lowest}). "
               f"It must be at least 1, so start_value = 1 − ({lowest}) = {start_value}. "
               "Every other sum is higher than the lowest one, so they are all at least 1 too.", **snap(None, None, "start"))
        # @trace-end
        return start_value  # @a:return
