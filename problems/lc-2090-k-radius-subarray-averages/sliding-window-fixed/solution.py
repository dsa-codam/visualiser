from typing import List  # @hide


class Solution:
    def getAverages(self, nums: List[int], k: int) -> List[int]:
        n = len(nums)  # @a:init
        avgs = [-1] * n  # -1 stays wherever there is no full window
        size = 2 * k + 1  # window length: k numbers, the centre, k numbers
        # @trace-begin
        total = None
        left = 0
        center = None
        written = []

        def snap(right, window, roles=None, new=None, flash=False):
            return dict(
                state={"arr": list(nums), "avgs": list(avgs), "k": k, "left": left, "right": right,
                       "window": window, "total": total, "center": center, "written": list(written), "newAt": new},
                roles=roles or {},
                vars=[
                    {"label": "k", "value": k},
                    {"label": "size", "value": size},
                    {"label": "left", "value": left, "role": "back"},
                    {"label": "right", "value": "—" if right is None else right, "role": "front"},
                    {"label": "total", "value": "—" if total is None else total},
                    {"label": "center", "value": "—" if center is None else center, "flash": flash},
                ],
            )

        T.step("init", "init", f"n = {n}. avgs starts as {n} times -1. Each window has size = 2·k + 1 = {size} "
               f"numbers: k = {k} on each side of its centre.", **snap(None, None))
        # @trace-end
        if size > n:  # the window does not fit: every answer is -1  # @a:fits
            T.step("fits", "return", f"size = {size} > n = {n}: no index has {k} numbers on both sides. Return avgs, all -1.", **snap(None, None))  # @trace
            return avgs
        T.step("fits", "init", f"size = {size} ≤ n = {n}, so at least one full window fits.", **snap(None, None))  # @trace
        total = 0  # sum of the window; up to 10^10, so long long in C and C++  # @a:total
        left = 0  # left edge of the window
        T.step("total", "init", "total = 0, left = 0. We add the first window nums[0..size − 1] one by one.", **snap(None, None))  # @trace
        for right in range(size):  # build the first window nums[0..size-1]  # @a:build-loop
            # @trace-begin
            T.step("build-loop", "build", f"The first for loop fills the first window: right = {right}." if right == 0 else
                   f"Next round of the first for loop: right = {right} < size = {size}.",
                   **snap(right, [0, right - 1] if right > 0 else None))
            # @trace-end
            total += nums[right]  # @a:build
            # @trace-begin
            T.op()
            T.step("build", "build", f"nums[{right}] = {nums[right]} is added, so total = {total}.",
                   **snap(right, [0, right], {right: "current"}))
            # @trace-end
        avgs[k] = total // size  # the first window is centred at index k  # @a:first
        # @trace-begin
        written.append(k)
        T.step("first", "write", f"The first window [0, {size - 1}] is full. Its centre is index k = {k}: "
               f"avgs[{k}] = total // size = {total} // {size} = {avgs[k]}.", **snap(None, [0, size - 1], new=k))
        # @trace-end
        for right in range(size, n):  # slide: one number in, one out  # @a:loop
            T.step("loop", "next", f"Next round of the second for loop: right moves to index {right}. The window slides one step to the right.", **snap(right, [left, right - 1]))  # @trace
            total += nums[right]  # new number enters on the right  # @a:add
            # @trace-begin
            T.op()
            T.step("add", "add", f"nums[{right}] = {nums[right]} enters, so total = {total}. "
                   f"The window now has size + 1 = {size + 1} numbers, one too many.",
                   **snap(right, [left, right], {right: "current"}))
            # @trace-end
            total -= nums[left]  # oldest number leaves on the left  # @a:drop
            left += 1
            # @trace-begin
            T.op()
            T.step("drop", "drop", f"nums[{left - 1}] = {nums[left - 1]} leaves, so total = {total}. "
                   f"left moves to {left}, and the window [{left}, {right}] has size = {size} numbers again.",
                   **snap(right, [left, right], {left - 1: "removed"}))
            # @trace-end
            center = left + k  # the middle of the window  # @a:write
            avgs[center] = total // size
            # @trace-begin
            written.append(center)
            T.step("write", "write", f"center = left + k = {center}: avgs[{center}] = total // size = "
                   f"{total} // {size} = {avgs[center]}.", **snap(right, [left, right], new=center, flash=True))
            center = None
            # @trace-end
        # @trace-begin
        T.step("return", "return", f"Return avgs = {avgs}. The first k and the last k indices have no full window, "
               "so they keep -1. Every other window was made from the one before it by adding one number and "
               "removing one, so each total is correct.", **snap(None, None))
        # @trace-end
        return avgs  # @a:return
