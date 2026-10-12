from typing import List  # @hide


class Solution:
    def maxFrequency(self, nums: List[int], k: int) -> int:
        # @trace-begin
        ids = sorted(range(len(nums)), key=lambda i: nums[i])  # where each cell goes when sorted (stable)
        best_win = None

        def show(v):
            return "[" + ", ".join(map(str, v)) + "]"

        def snap(right, window, total, cost=None, length=None, roles=None, tags=None, flash=False, sorted_=True, before_init=False):
            dash = lambda x: "—" if before_init else x
            return dict(
                state={"arr": nums[:], "ids": ids if sorted_ else list(range(len(nums))), "left": left, "right": right,
                       "window": window, "total": total, "cost": cost, "k": k, "longest": longest,
                       "bestWindow": best_win, "tags": tags or {}},
                roles=roles or {},
                vars=[
                    {"label": "k", "value": k},
                    {"label": "left", "value": dash(left), "role": "back"},
                    {"label": "right", "value": "—" if right is None else right, "role": "front"},
                    {"label": "nums[right]", "value": "—" if right is None else nums[right]},
                    {"label": "total", "value": dash(total)},
                    {"label": "cost", "value": "—" if cost is None else cost},
                    {"label": "length", "value": "—" if length is None else length},
                    {"label": "longest", "value": dash(longest), "flash": flash},
                ],
            )

        left, longest = 0, 0
        T.step("sort", "init", f"nums = {show(nums)}, k = {k}. Values can only go up, so a group of equal values is built by raising smaller values to the largest one. Sorting puts the cheapest values to raise next to each other.", **snap(None, None, 0, sorted_=False, before_init=True))
        # @trace-end
        nums.sort()  # the cheapest values to raise sit just before nums[right]  # @a:sort
        T.step("sort", "init", f"After sorting: nums = {show(nums)}. For each right, the window nums[left..right] will all be raised to nums[right].", **snap(None, None, 0, before_init=True))  # @trace
        left = 0  # left edge of the window  # @a:init
        total = 0  # sum of nums[left..right]
        longest = 0  # largest valid window so far
        T.step("init", "init", "left = 0, total = 0, longest = 0. Rule: cost = nums[right] × length − total, the increments the window needs, must stay ≤ k.", **snap(None, None, total))  # @trace
        for right in range(len(nums)):  # right edge: nums[right] is the target value  # @a:loop
            T.step("loop", "next", f"Next round of the for loop: right moves to index {right}." if right else "The for loop starts: right = 0.", **snap(right, [left, right - 1] if right > left else None, total))  # @trace
            total += nums[right]  # add nums[right] to the window  # @a:expand
            cost = nums[right] * (right - left + 1) - total  # increments to raise the whole window to nums[right]
            T.op()  # @trace
            # @trace-begin
            v, ln = nums[right], right - left + 1
            if cost > k:
                T.step("expand", "expand", f"Add nums[{right}] = {v}, total = {total}. cost = {v} × {ln} − {total} = {cost} > k = {k}: the window needs too many increments.",
                       **snap(right, [left, right], total, cost, roles={right: "conflict"}, tags={right: ">k"}))
            else:
                T.step("expand", "expand", f"Add nums[{right}] = {v}, total = {total}. cost = {v} × {ln} − {total} = {cost} ≤ k = {k}: every value in the window can be raised to {v}.",
                       **snap(right, [left, right], total, cost, roles={right: "current"}))
            # @trace-end
            while cost > k:  # too many increments: shrink from the left  # @a:while
                T.step("while", "check", f"while cost = {cost} > k = {k}: the loop runs. Drop the smallest value, nums[left] = {nums[left]}: it needs the most increments.", **snap(right, [left, right], total, cost, roles={right: "conflict"}, tags={right: ">k"}))  # @trace
                total -= nums[left]  # drop nums[left] from the window  # @a:shrink
                left += 1
                cost = nums[right] * (right - left + 1) - total
                # @trace-begin
                T.op()
                d, ln = nums[left - 1], right - left + 1
                if cost > k:
                    T.step("shrink", "shrink", f"Drop {d}, total = {total}, left moves to {left}. cost = {nums[right]} × {ln} − {total} = {cost}, still > k = {k}.",
                           **snap(right, [left, right], total, cost, roles={left - 1: "removed", right: "conflict"}, tags={right: ">k"}))
                else:
                    T.step("shrink", "shrink", f"Drop {d}, total = {total}, left moves to {left}. cost = {nums[right]} × {ln} − {total} = {cost} ≤ k = {k}, so the while loop stops.",
                           **snap(right, [left, right], total, cost, roles={left - 1: "removed"}))
                # @trace-end
            length = right - left + 1  # valid window: all can become nums[right]  # @a:length
            old = longest  # @trace
            longest = max(longest, length)  # @a:update
            # @trace-begin
            if longest > old:
                best_win = [left, right]
                T.step("update", "update", f"Window [{left}, {right}] has length = {length} > old longest {old}, so longest = {longest}." + (f" {length} values can all become {nums[right]}." if length > 1 else ""),
                       **snap(right, [left, right], total, cost, length, flash=True))
            else:
                T.step("update", "compare", f"Window [{left}, {right}] has length = {length}, not more than longest = {longest}. longest stays.",
                       **snap(right, [left, right], total, cost, length))
            # @trace-end
        # @trace-begin
        T.step("return", "return", f"Return longest = {longest}: the values in [{best_win[0]}, {best_win[1]}] can all be raised to {nums[best_win[1]]} with at most k = {k} increments. "
               "Every right was tried as the target, and left only moved when the cost went over k, so no longer window was missed.",
               **snap(None, None, total))
        # @trace-end
        return longest  # @a:return
