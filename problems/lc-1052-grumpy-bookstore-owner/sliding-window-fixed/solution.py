from typing import List  # @hide


class Solution:
    def maxSatisfied(self, customers: List[int], grumpy: List[int], minutes: int) -> int:
        # @trace-begin
        i = left = extra = max_extra = None
        scanned = 0  # how many minutes the first loop has looked at
        best_win = None

        def dash(x):
            return "—" if x is None else x

        def snap(right, window, roles=None, flash=False):
            return dict(
                state={"customers": customers[:], "grumpy": grumpy[:], "minutes": minutes, "i": i, "scanned": scanned,
                       "left": left, "right": right, "window": window, "satisfied": satisfied, "extra": extra,
                       "max_extra": max_extra, "bestWindow": best_win},
                roles=roles or {},
                vars=[
                    {"label": "minutes", "value": minutes},
                    {"label": "i", "value": dash(i)},
                    {"label": "satisfied", "value": satisfied},
                    {"label": "left", "value": dash(left), "role": "back"},
                    {"label": "right", "value": dash(right), "role": "front"},
                    {"label": "extra", "value": dash(extra)},
                    {"label": "max_extra", "value": dash(max_extra), "flash": flash},
                ],
            )
        # @trace-end
        n = len(customers)  # @a:init
        satisfied = 0  # customers of calm minutes: happy without the technique
        T.step("init", "init", f"satisfied = 0. First count the customers who are happy anyway: the ones in minutes where grumpy[i] = 0.", **snap(None, None))  # @trace
        for i in range(n):  # @a:base-loop
            T.step("base-loop", "base", "The first for loop starts: i = 0." if i == 0 else f"Next round of the first for loop: i = {i}.", **snap(None, None, {i: "current"}))  # @trace
            if grumpy[i] == 0:  # the owner is calm, so these customers are happy  # @a:base
                satisfied += customers[i]
            # @trace-begin
            T.op()
            scanned = i + 1
            if grumpy[i] == 0:
                T.step("base", "base", f"grumpy[{i}] = 0: the owner is calm. Add customers[{i}] = {customers[i]}, satisfied = {satisfied}.", **snap(None, None, {i: "current"}))
            else:
                T.step("base", "base", f"grumpy[{i}] = 1: the owner is grumpy, so customers[{i}] = {customers[i]} is not added. Only the technique can win these customers back.", **snap(None, None, {i: "current"}))
            # @trace-end
        # @trace-begin
        i = None
        T.step("base-loop", "base", f"The first loop ends: satisfied = {satisfied}. Now find the {minutes} minutes in a row whose grumpy customers are worth the most.", **snap(None, None))
        # @trace-end
        extra = 0  # grumpy-minute customers in the window: the technique wins them back  # @a:extra
        T.step("extra", "build", f"extra = 0. The window has minutes = {minutes} cells. extra counts customers[j] only where grumpy[j] = 1.", **snap(None, None))  # @trace
        for right in range(minutes):  # build the first window [0, minutes - 1]  # @a:build-loop
            T.step("build-loop", "build", f"The second for loop fills the first window: right = {right}." if right == 0 else f"Next round of the second for loop: right = {right} < minutes = {minutes}.", **snap(right, [0, right - 1] if right > 0 else None))  # @trace
            if grumpy[right] == 1:  # @a:build
                extra += customers[right]
            # @trace-begin
            T.op()
            if grumpy[right] == 1:
                T.step("build", "build", f"grumpy[{right}] = 1: add customers[{right}] = {customers[right]}, extra = {extra}.", **snap(right, [0, right], {right: "current"}))
            else:
                T.step("build", "build", f"grumpy[{right}] = 0: these customers are already in satisfied, so extra does not change ({extra}).", **snap(right, [0, right], {right: "current"}))
            # @trace-end
        max_extra = extra  # the first full window is the best so far  # @a:first
        left = 0  # left edge of the window
        # @trace-begin
        best_win = [0, minutes - 1]
        T.step("first", "update", f"The first window [0, {minutes - 1}] is full, so max_extra = extra = {max_extra}. left = 0.", **snap(None, [0, minutes - 1], flash=True))
        # @trace-end
        for right in range(minutes, n):  # slide: one minute in, one out  # @a:loop
            T.step("loop", "next", f"Next round of the third for loop: right moves to minute {right}. The window slides one step to the right.", **snap(right, [left, right - 1]))  # @trace
            if grumpy[right] == 1:  # new minute enters on the right  # @a:add
                extra += customers[right]
            # @trace-begin
            T.op()
            if grumpy[right] == 1:
                T.step("add", "add", f"grumpy[{right}] = 1: add customers[{right}] = {customers[right]}, extra = {extra}.", **snap(right, [left, right], {right: "current"}))
            else:
                T.step("add", "add", f"grumpy[{right}] = 0: minute {right} is calm, extra does not change ({extra}).", **snap(right, [left, right], {right: "current"}))
            # @trace-end
            if grumpy[left] == 1:  # oldest minute leaves on the left  # @a:drop
                extra -= customers[left]
            left += 1
            # @trace-begin
            T.op()
            j = left - 1
            if grumpy[j] == 1:
                T.step("drop", "drop", f"grumpy[{j}] = 1: drop customers[{j}] = {customers[j]}, extra = {extra}. left moves to {left}; the window [{left}, {right}] has {minutes} minutes again.", **snap(right, [left, right], {j: "removed"}))
            else:
                T.step("drop", "drop", f"grumpy[{j}] = 0: minute {j} was never in extra, so extra stays {extra}. left moves to {left}; the window [{left}, {right}] has {minutes} minutes again.", **snap(right, [left, right], {j: "removed"}))
            old = max_extra
            # @trace-end
            max_extra = max(max_extra, extra)  # keep the window that wins back the most  # @a:update
            # @trace-begin
            if max_extra > old:
                best_win = [left, right]
                T.step("update", "update", f"extra = {extra} > old max_extra {old}, so max_extra = {max_extra}. Window [{left}, {right}] is the best so far.", **snap(right, [left, right], flash=True))
            else:
                T.step("update", "compare", f"extra = {extra} is not more than max_extra = {max_extra}. max_extra stays.", **snap(right, [left, right]))
            # @trace-end
        # @trace-begin
        T.step("return", "return", f"Return satisfied + max_extra = {satisfied} + {max_extra} = {satisfied + max_extra}: use the technique in minutes [{best_win[0]}, {best_win[1]}]. "
               "Calm minutes are counted once in satisfied, and every window of minutes in a row was checked once.", **snap(None, None))
        # @trace-end
        return satisfied + max_extra  # @a:return
