from typing import List  # @hide


class Solution:
    def sortedSquares(self, nums: List[int]) -> List[int]:
        # @trace-begin
        def show(v):
            return "[" + ", ".join(map(str, v)) + "]"

        def snap(left, right, write, placed, left_square=None, right_square=None, r1=None, r2=None, flash=False):
            return dict(
                state={"nums": nums[:], "result": result[:], "left": left, "right": right, "write": write,
                       "placed": placed, "r1": r1 or {}, "r2": r2 or {}},
                vars=[
                    {"label": "left", "value": left, "role": "back"},
                    {"label": "right", "value": right, "role": "front"},
                    {"label": "write", "value": write, "role": "back"},
                    {"label": "left_square", "value": "—" if left_square is None else left_square},
                    {"label": "right_square", "value": "—" if right_square is None else right_square},
                    {"label": "result", "value": show(result), "flash": flash},
                ],
            )
        rounds = 0
        # @trace-end
        n = len(nums)  # @a:init
        result = [0] * n  # the squares go here, from the back
        left = 0  # most negative value
        right = n - 1  # most positive value
        write = n - 1  # next slot to fill: the largest square goes last
        T.step("init", "init", f"left = 0 and right = {right}: the two ends of nums. The largest square is always at one of the ends. write = {write}: result is filled from the back, largest first.", **snap(left, right, write, n))  # @trace
        while left <= right:  # @a:loop
            T.op()  # @trace
            # @trace-begin
            rounds += 1
            left_word = "one value is" if left == right else f"{right - left + 1} values are"
            T.step("loop", "next", (f"while left <= right: {left} <= {right}, so the loop runs. {left_word.capitalize()} not placed yet." if rounds == 1
                                    else f"Next round: left = {left} <= right = {right}, so {left_word} still waiting."), **snap(left, right, write, write + 1))
            # @trace-end
            left_square = nums[left] * nums[left]  # @a:squares
            right_square = nums[right] * nums[right]
            if left_square > right_square:  # the left end has the larger square  # @a:compare
                # @trace-begin
                T.step("compare", "compare", f"left_square = {nums[left]}² = {left_square} > right_square = {nums[right]}² = {right_square}. {left_square} is the largest square left, so it goes into slot write = {write}.",
                       **snap(left, right, write, write + 1, left_square, right_square, {left: "current"}))
                # @trace-end
                result[write] = left_square  # @a:takeLeft
                T.step("takeLeft", "take", f"result[{write}] = {left_square}. Slot {write} is final. left moves right: nums[{left}] is used.", **snap(left, right, write, write, left_square, right_square, r2={write: "new"}, flash=True))  # @trace
                left += 1
            else:
                # @trace-begin
                if left == right:
                    cap = f"left = right = {left}: one value left. left_square = right_square = {right_square}, so take it from the right."
                elif left_square == right_square:
                    cap = f"left_square = right_square = {right_square}: the squares are equal, so either end works. The code takes the right one."
                else:
                    cap = f"left_square = {nums[left]}² = {left_square} <= right_square = {nums[right]}² = {right_square}. {right_square} is the largest square left, so it goes into slot write = {write}."
                T.step("compare", "compare", cap, **snap(left, right, write, write + 1, left_square, right_square, {right: "current"}))
                # @trace-end
                result[write] = right_square  # @a:takeRight
                T.step("takeRight", "take", f"result[{write}] = {right_square}. Slot {write} is final. right moves left: nums[{right}] is used.", **snap(left, right, write, write, left_square, right_square, r2={write: "new"}, flash=True))  # @trace
                right -= 1
            write -= 1  # @a:advance
        T.step("loop", "stop", f"left = {left} > right = {right}: every value of nums is used, so the while loop stops.", **snap(left, right, write, 0))  # @trace
        T.step("done", "return", f"Done: result = {show(result)}. Each slot from the back got the largest square left, and that square is always at one end of nums, so the result is sorted. One pass: O(n).", **snap(left, right, write, 0))  # @trace
        return result  # @a:done
