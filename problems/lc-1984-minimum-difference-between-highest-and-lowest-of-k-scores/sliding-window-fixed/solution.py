from typing import List  # @hide


class Solution:
    def minimumDifference(self, nums: List[int], k: int) -> int:
        # @trace-begin
        ids = sorted(range(len(nums)), key=lambda i: nums[i])  # where each cell goes when sorted (stable)
        best_win = None
        left = smallest = diff = None

        def show(v):
            return "[" + ", ".join(map(str, v)) + "]"

        def dash(x):
            return "—" if x is None else x

        def snap(right, window, roles=None, flash=False, sorted_=True):
            return dict(
                state={"arr": nums[:], "ids": ids if sorted_ else list(range(len(nums))), "k": k,
                       "left": left, "right": right, "window": window, "diff": diff,
                       "smallest": smallest, "bestWindow": best_win},
                roles=roles or {},
                vars=[
                    {"label": "k", "value": k},
                    {"label": "left", "value": dash(left), "role": "back"},
                    {"label": "right", "value": dash(right), "role": "front"},
                    {"label": "nums[left]", "value": "—" if right is None or left > right else nums[left]},
                    {"label": "nums[right]", "value": "—" if right is None else nums[right]},
                    {"label": "diff", "value": dash(diff)},
                    {"label": "smallest", "value": dash(smallest), "flash": flash},
                ],
            )

        T.step("sort", "init", f"nums = {show(nums)}, k = {k}. We may pick any k scores, so their order in nums does not matter. "
               "After sorting, scores that are close in value sit next to each other.", **snap(None, None, sorted_=False))
        # @trace-end
        nums.sort()  # close scores are now neighbours  # @a:sort
        # @trace-begin
        T.step("sort", "init", f"After sorting: nums = {show(nums)}. The best group of k scores is now always k neighbours, "
               f"so we only check windows of exactly k = {k} cells.", **snap(None, None))
        # @trace-end
        left = 0  # left edge of the window  # @a:init
        smallest = nums[len(nums) - 1] - nums[0]  # the widest gap: no k scores differ by more
        # @trace-begin
        T.step("init", "init", f"left = 0. smallest = nums[{len(nums) - 1}] − nums[0] = {nums[-1]} − {nums[0]} = {smallest}: "
               "the highest minus the lowest of all scores, so no group can have a bigger difference.", **snap(None, None))
        # @trace-end
        for right in range(k - 1, len(nums)):  # right edge: nums[left..right] has k scores  # @a:loop
            # @trace-begin
            diff = None
            T.step("loop", "next", f"The for loop starts: right = k − 1 = {right}, so the first window is [{left}, {right}]." if right == k - 1 else
                   f"Next round of the for loop: right moves to index {right}. The window is [{left}, {right}].",
                   **snap(right, [left, right]))
            # @trace-end
            diff = nums[right] - nums[left]  # sorted, so this is the highest minus the lowest of the window  # @a:diff
            # @trace-begin
            T.op()
            T.step("diff", "diff", f"diff = nums[{right}] − nums[{left}] = {nums[right]} − {nums[left]} = {diff}. "
                   "nums is sorted, so nums[right] is the highest and nums[left] the lowest score in the window.",
                   **snap(right, [left, right], {left: "current", right: "current"}))
            old = smallest
            # @trace-end
            smallest = min(smallest, diff)  # keep the smallest difference  # @a:update
            # @trace-begin
            if smallest < old:
                best_win = [left, right]
                T.step("update", "update", f"diff = {diff} < old smallest {old}, so smallest = {smallest}. "
                       f"Window [{left}, {right}] is the best so far.", **snap(right, [left, right], flash=True))
            elif best_win is None:
                best_win = [left, right]
                T.step("update", "update", f"diff = {diff} = smallest: this window is as wide as all scores together, "
                       f"so smallest stays {smallest}. Window [{left}, {right}] is the best so far.", **snap(right, [left, right]))
            else:
                T.step("update", "compare", f"diff = {diff} is not less than smallest = {smallest}. smallest stays.",
                       **snap(right, [left, right]))
            # @trace-end
            left += 1  # the next window starts one step to the right  # @a:slide
            # @trace-begin
            last = right == len(nums) - 1
            T.step("slide", "slide", f"left moves to {left}. nums[{left - 1}] = {nums[left - 1]} leaves the window." +
                   (f" right = {right} is the last index, so the for loop ends." if last else
                    f" Next, right moves to {right + 1} and the window has k = {k} scores again."),
                   **snap(right, [left, right] if left <= right else None, {left - 1: "removed"}))
            # @trace-end
        # @trace-begin
        diff = None
        T.step("return", "return", f"Return smallest = {smallest}, the difference of window [{best_win[0]}, {best_win[1]}]: "
               f"{nums[best_win[1]]} − {nums[best_win[0]]}. In a sorted array the closest group of k scores is always k neighbours, "
               "and every window of k neighbours was checked once.", **snap(None, None))
        # @trace-end
        return smallest  # @a:return
