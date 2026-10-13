from typing import List  # @hide


class Solution:
    def longestAlternatingSubarray(self, nums: List[int], threshold: int) -> int:
        left = 0  # left edge of the window; left > right means there is no window  # @a:init
        longest = 0  # longest valid window so far
        # @trace-begin
        best_win = None

        def parity(v):
            return "even" if v % 2 == 0 else "odd"

        def snap(right, window, roles=None, tags=None, length=None, flash=False):
            return dict(
                state={"arr": nums[:], "left": left, "right": right, "window": window, "threshold": threshold,
                       "longest": longest, "bestWindow": best_win, "tags": tags or {}},
                roles=roles or {},
                vars=[
                    {"label": "threshold", "value": threshold},
                    {"label": "left", "value": left, "role": "back"},
                    {"label": "right", "value": "—" if right is None else right, "role": "front"},
                    {"label": "nums[right]", "value": "—" if right is None else nums[right]},
                    {"label": "nums[right] % 2", "value": "—" if right is None else nums[right] % 2},
                    {"label": "length", "value": "—" if length is None else length},
                    {"label": "longest", "value": longest, "flash": flash},
                ],
            )

        T.step("init", "init", f"left = 0, longest = 0. A valid window starts with an even value, alternates even / odd, and has no value above threshold = {threshold}.", **snap(None, None))
        # @trace-end
        for right in range(len(nums)):  # right edge, moves every step  # @a:loop
            # @trace-begin
            T.op()
            T.step("loop", "next", (f"Next round of the for loop: right moves to index {right}." if right else "The for loop starts: right = 0.")
                   + ("" if left < right else " There is no window before it."),
                   **snap(right, [left, right - 1] if left < right else None))
            empty_before = left == right
            v, p = nums[right], parity(nums[right])
            # @trace-end
            if nums[right] > threshold:  # no valid window can contain nums[right]  # @a:over
                left = right + 1  # @a:reset
                T.step("reset", "reset", f"nums[right] = {v} > threshold = {threshold}, so no valid window can contain it. left = right + 1 = {left}: there is no window now.", **snap(right, None, {right: "conflict"}, {right: f">{threshold}"}))  # @trace
            elif left == right or nums[right] % 2 == nums[right - 1] % 2:  # the window cannot grow to right  # @a:restart
                # @trace-begin
                if empty_before:
                    why = "There is no window before right, so nums[right] can only start a new one."
                    before = {}
                else:
                    why = f"nums[right - 1] = {nums[right - 1]} and nums[right] = {v} are both {p}, so the window cannot grow to right."
                    before = {right - 1: "dup"}
                # @trace-end
                if nums[right] % 2 == 0:
                    left = right  # an even value starts a new window  # @a:start
                    T.step("start", "restart", f"{why} nums[right] = {v} is even and ≤ threshold, so a new window starts here: left = right = {left}.", **snap(right, [left, right], {**before, right: "current"}))  # @trace
                else:
                    left = right + 1  # an odd value cannot start a window  # @a:skip
                    T.step("skip", "skip", f"{why} nums[right] = {v} is odd, and a window must start with an even value. left = right + 1 = {left}: there is no window now.", **snap(right, None, {**before, right: "conflict"}, {right: "odd"}))  # @trace
            else:  # @trace
                T.step("restart", "expand", f"nums[right - 1] = {nums[right - 1]} is {parity(nums[right - 1])} and nums[right] = {v} is {p}: the parity alternates and {v} ≤ threshold, so the window grows to [{left}, {right}].", **snap(right, [left, right], {right: "current"}))  # @trace
            if left <= right:  # there is a window [left, right]
                length = right - left + 1  # @a:length
                old = longest  # @trace
                longest = max(longest, length)  # @a:update
                # @trace-begin
                if longest > old:
                    best_win = [left, right]
                    T.step("update", "update", f"Window [{left}, {right}] has length = {length} > old longest {old}, so longest = {longest}.",
                           **snap(right, [left, right], length=length, flash=True))
                else:
                    T.step("update", "compare", f"Window [{left}, {right}] has length = {length}, not more than longest = {longest}. longest stays.",
                           **snap(right, [left, right], length=length))
                # @trace-end
        # @trace-begin
        if best_win is None:
            T.step("return", "return", "Return longest = 0: no element is an even value ≤ threshold, so no valid window ever started.", **snap(None, None))
        else:
            T.step("return", "return", f"Return longest = {longest}: the window [{best_win[0]}, {best_win[1]}]. A rule can only break between two neighbours "
                   "or at one element, so no valid window crosses a break. The window restarted at every break and was checked at every right, so no longer window was missed.",
                   **snap(None, None))
        # @trace-end
        return longest  # @a:return
