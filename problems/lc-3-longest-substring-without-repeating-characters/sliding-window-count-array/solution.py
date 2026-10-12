class Solution:
    def lengthOfLongestSubstring(self, s: str) -> int:
        count = [0] * 128  # character code -> times it is in the window (s is ASCII)  # @a:init
        left = 0  # left edge of the window
        longest = 0  # longest unique window so far
        # @trace-begin
        order = list(dict.fromkeys(s))  # map rows in order of first appearance
        best_win = None

        def show(ch):
            return f"'{ch}'"

        def snap(right, window, roles=None, dup=None, length=None, flash=False):
            return dict(
                state={"arr": list(s), "left": left, "right": right, "window": window,
                       "rows": [{"key": show(c), "count": count[ord(c)]} for c in order],
                       "dup": dup, "longest": longest, "bestWindow": best_win},
                roles=roles or {},
                vars=[
                    {"label": "left", "value": left, "role": "back"},
                    {"label": "right", "value": "—" if right is None else right, "role": "front"},
                    {"label": "s[right]", "value": "—" if right is None else show(s[right])},
                    {"label": "length", "value": "—" if length is None else length},
                    {"label": "longest", "value": longest, "flash": flash},
                ],
            )

        T.step("init", "init", "count is all zeros, left = 0, longest = 0. Rule: no character may appear twice in the window.", **snap(None, None))
        # @trace-end
        for right in range(len(s)):  # right edge, moves every step  # @a:loop
            T.step("loop", "next", f"Next round of the for loop: right moves to index {right}." if right else "The for loop starts: right = 0.", **snap(right, [left, right - 1] if right > left else None))  # @trace
            count[ord(s[right])] += 1  # add s[right] to the window  # @a:expand
            T.op()  # @trace
            # @trace-begin
            c = show(s[right])
            if count[ord(s[right])] > 1:
                T.step("expand", "expand", f"right = {right}: add {c}. count[{c}] is now 2, so {c} appears twice and the window is no longer unique.",
                       **snap(right, [left, right], {right: "conflict"}, dup=s[right]))
            else:
                T.step("expand", "expand", f"right = {right}: add {c}. count[{c}] = 1, so the window [{left}, {right}] is still unique.",
                       **snap(right, [left, right], {right: "current"}))
            # @trace-end
            while count[ord(s[right])] > 1:  # only s[right] can be a repeat  # @a:while
                T.step("while", "check", f"while count[{show(s[right])}] = 2 > 1: the loop runs, so the window shrinks from the left until the old {show(s[right])} is gone.", **snap(right, [left, right], dup=s[right]))  # @trace
                count[ord(s[left])] -= 1  # drop s[left] from the window  # @a:shrink
                left += 1
                # @trace-begin
                T.op()
                d, c = show(s[left - 1]), show(s[right])
                if count[ord(s[right])] > 1:
                    T.step("shrink", "shrink", f"Drop s[{left - 1}] = {d}, left moves to {left}. It is not the old {c}, so {c} still appears twice.",
                           **snap(right, [left, right], {left - 1: "removed"}, dup=s[right]))
                else:
                    T.step("shrink", "shrink", f"Drop s[{left - 1}] = {d}, left moves to {left}. That was the old {c}, so the window [{left}, {right}] is unique again and the while loop stops.",
                           **snap(right, [left, right], {left - 1: "removed"}))
                # @trace-end
            length = right - left + 1  # unique window: its length  # @a:length
            old = longest  # @trace
            longest = max(longest, length)  # @a:update
            # @trace-begin
            if longest > old:
                best_win = [left, right]
                T.step("update", "update", f"Window [{left}, {right}] = \"{s[left:right + 1]}\" has length = {length} > old longest {old}, so longest = {longest}.",
                       **snap(right, [left, right], length=length, flash=True))
            else:
                T.step("update", "compare", f"Window [{left}, {right}] = \"{s[left:right + 1]}\" has length = {length}, not more than longest = {longest}. longest stays.",
                       **snap(right, [left, right], length=length))
            # @trace-end
        # @trace-begin
        if best_win is None:
            T.step("return", "return", "s is empty, so the for loop never ran. Return longest = 0.", **snap(None, None))
        else:
            T.step("return", "return", f"Return longest = {longest}: the substring \"{s[best_win[0]:best_win[1] + 1]}\". Every unique window was checked "
                   "at its right end, and left only moved right when a repeat forced it, so no longer unique window was missed.",
                   **snap(None, None))
        # @trace-end
        return longest  # @a:return
