from typing import List  # @hide


class Solution:
    def numOfSubarrays(self, arr: List[int], k: int, threshold: int) -> int:
        min_sum = threshold * k  # average >= threshold  <=>  sum >= threshold * k  # @a:init
        total = 0  # sum of the window
        left = 0  # left edge of the window
        count = 0  # windows with average >= threshold
        # @trace-begin
        def snap(right, window, roles=None, passed=False, flash=False):
            return dict(
                state={"arr": arr[:], "k": k, "left": left, "right": right, "window": window, "total": total,
                       "min_sum": min_sum, "count": count, "passed": passed},
                roles=roles or {},
                vars=[
                    {"label": "left", "value": left, "role": "back"},
                    {"label": "right", "value": "—" if right is None else right, "role": "front"},
                    {"label": "total", "value": total},
                    {"label": "min_sum", "value": min_sum},
                    {"label": "count", "value": count, "flash": flash},
                ],
            )

        def check(anchor, right, w):
            if total >= min_sum:
                T.step(anchor, "count", f"total = {total} ≥ min_sum = {min_sum}, so the average {total}/{k} is at least "
                       f"{threshold}. count = {count}.", **snap(right, w, passed=True, flash=True))
            else:
                T.step(anchor, "skip", f"total = {total} < min_sum = {min_sum}, so the average {total}/{k} is below "
                       f"{threshold}. count stays {count}.", **snap(right, w))

        T.step("init", "init", f"min_sum = threshold × k = {threshold} × {k} = {min_sum}. A window's average is ≥ {threshold} "
               f"exactly when its sum is ≥ {min_sum}, so we never need to divide.", **snap(None, None))
        # @trace-end
        for right in range(k):  # build the first window arr[0..k-1]  # @a:build-loop
            # @trace-begin
            T.step("build-loop", "build", f"The first for loop fills the first window: right = {right}." if right == 0 else
                   f"Next round of the first for loop: right = {right} < k = {k}.",
                   **snap(right, [0, right - 1] if right > 0 else None))
            # @trace-end
            total += arr[right]  # @a:build
            # @trace-begin
            T.op()
            T.step("build", "build", f"Add arr[{right}] = {arr[right]}, total = {total}.",
                   **snap(right, [0, right], {right: "current"}))
            # @trace-end
        if total >= min_sum:  # check the first full window  # @a:check-first
            count += 1
        check("check-first", None, [0, k - 1])  # @trace
        for right in range(k, len(arr)):  # slide: one element in, one out  # @a:loop
            T.step("loop", "next", f"Next round of the second for loop: right moves to index {right}. The window slides one step to the right.", **snap(right, [left, right - 1]))  # @trace
            total += arr[right]  # new element enters on the right  # @a:add
            # @trace-begin
            T.op()
            T.step("add", "add", f"Add arr[{right}] = {arr[right]}, total = {total}. "
                   f"The window now has k + 1 = {k + 1} elements, one too many.",
                   **snap(right, [left, right], {right: "current"}))
            # @trace-end
            total -= arr[left]  # oldest element leaves on the left  # @a:drop
            left += 1
            # @trace-begin
            T.op()
            T.step("drop", "drop", f"Drop arr[{left - 1}] = {arr[left - 1]}, total = {total}, left moves to {left}. "
                   f"The window [{left}, {right}] has k = {k} elements again.",
                   **snap(right, [left, right], {left - 1: "removed"}))
            # @trace-end
            if total >= min_sum:  # @a:check
                count += 1
            check("check", right, [left, right])  # @trace
        # @trace-begin
        T.step("return", "return", f"Return count = {count}. Every window of length k was checked once, with the same test "
               f"total ≥ min_sum, which is the same as average ≥ threshold.", **snap(None, None))
        # @trace-end
        return count  # @a:return
