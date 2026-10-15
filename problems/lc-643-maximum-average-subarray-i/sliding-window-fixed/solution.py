from typing import List  # @hide


class Solution:
    def findMaxAverage(self, nums: List[int], k: int) -> float:
        total = 0  # sum of the window  # @a:init
        left = 0  # left edge of the window
        # @trace-begin
        best_win = None
        largest = None

        def snap(right, window, roles=None, flash=False):
            return dict(
                state={"arr": nums[:], "k": k, "left": left, "right": right, "window": window, "total": total,
                       "largest": largest, "bestWindow": best_win},
                roles=roles or {},
                vars=[
                    {"label": "left", "value": left, "role": "back"},
                    {"label": "right", "value": "—" if right is None else right, "role": "front"},
                    {"label": "total", "value": total},
                    {"label": "largest", "value": "—" if largest is None else largest, "flash": flash},
                ],
            )

        T.step("init", "init", f"total = 0, left = 0. Every window has exactly k = {k} elements, "
               "so the largest average belongs to the window with the largest sum.", **snap(None, None))
        # @trace-end
        for right in range(k):  # build the first window nums[0..k-1]  # @a:build-loop
            # @trace-begin
            T.step("build-loop", "build", f"The first for loop fills the first window: right = {right}." if right == 0 else
                   f"Next round of the first for loop: right = {right} < k = {k}.",
                   **snap(right, [0, right - 1] if right > 0 else None))
            # @trace-end
            total += nums[right]  # @a:build
            # @trace-begin
            T.op()
            T.step("build", "build", f"Add nums[{right}] = {nums[right]}, total = {total}.",
                   **snap(right, [0, right], {right: "current"}))
            # @trace-end
        largest = total  # the first full window is the best so far  # @a:first
        # @trace-begin
        best_win = [0, k - 1]
        T.step("first", "update", f"The first window [0, {k - 1}] is full, so largest = total = {largest}. "
               "Do not start largest at 0: every sum can be negative.", **snap(None, [0, k - 1], flash=True))
        # @trace-end
        for right in range(k, len(nums)):  # slide: one element in, one out  # @a:loop
            T.step("loop", "next", f"Next round of the second for loop: right moves to index {right}. The window slides one step to the right.", **snap(right, [left, right - 1]))  # @trace
            total += nums[right]  # new element enters on the right  # @a:add
            # @trace-begin
            T.op()
            T.step("add", "add", f"Add nums[{right}] = {nums[right]}, total = {total}. "
                   f"The window now has k + 1 = {k + 1} elements, one too many.",
                   **snap(right, [left, right], {right: "current"}))
            # @trace-end
            total -= nums[left]  # oldest element leaves on the left  # @a:drop
            left += 1
            # @trace-begin
            T.op()
            T.step("drop", "drop", f"Drop nums[{left - 1}] = {nums[left - 1]}, total = {total}, left moves to {left}. "
                   f"The window [{left}, {right}] has k = {k} elements again.",
                   **snap(right, [left, right], {left - 1: "removed"}))
            old = largest
            # @trace-end
            largest = max(largest, total)  # keep the largest window sum  # @a:update
            # @trace-begin
            if largest > old:
                best_win = [left, right]
                T.step("update", "update", f"total = {total} > old largest {old}, so largest = {largest}. "
                       f"Window [{left}, {right}] is the best so far.", **snap(right, [left, right], flash=True))
            else:
                T.step("update", "compare", f"total = {total} is not more than largest = {largest}. largest stays.",
                       **snap(right, [left, right]))
            # @trace-end
        # @trace-begin
        T.step("return", "return", f"Return largest / k = {largest} / {k} = {largest / k:.5f}, the average of window "
               f"[{best_win[0]}, {best_win[1]}]. Every window of length k was checked once, and each one has the same length, "
               "so the largest sum gives the largest average.", **snap(None, None))
        # @trace-end
        return largest / k  # divide only once, at the end  # @a:return
