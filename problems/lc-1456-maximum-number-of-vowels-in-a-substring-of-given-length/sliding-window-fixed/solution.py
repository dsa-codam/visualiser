def is_vowel(c):  # five comparisons: constant time
    return c == 'a' or c == 'e' or c == 'i' or c == 'o' or c == 'u'


class Solution:
    def maxVowels(self, s: str, k: int) -> int:
        vowels = 0  # number of vowels in the window  # @a:init
        left = 0  # left edge of the window
        # @trace-begin
        best_win = None
        most = None

        def snap(right, window, roles=None, flash=False):
            return dict(
                state={"arr": list(s), "k": k, "left": left, "right": right, "window": window, "vowels": vowels,
                       "most": most, "bestWindow": best_win},
                roles=roles or {},
                vars=[
                    {"label": "left", "value": left, "role": "back"},
                    {"label": "right", "value": "—" if right is None else right, "role": "front"},
                    {"label": "vowels", "value": vowels},
                    {"label": "most", "value": "—" if most is None else most, "flash": flash},
                ],
            )

        def kind(c):
            return "a vowel" if is_vowel(c) else "not a vowel"

        T.step("init", "init", f"vowels = 0, left = 0. We look at every window of k = {k} letters "
               "and count the vowels in it.", **snap(None, None))
        # @trace-end
        for right in range(k):  # build the first window s[0..k-1]  # @a:build-loop
            # @trace-begin
            T.step("build-loop", "build", f"The first for loop fills the first window: right = {right}." if right == 0 else
                   f"Next round of the first for loop: right = {right} < k = {k}.",
                   **snap(right, [0, right - 1] if right > 0 else None))
            # @trace-end
            if is_vowel(s[right]):  # @a:build
                vowels += 1
            # @trace-begin
            T.op()
            T.step("build", "build", f"s[{right}] = '{s[right]}' is {kind(s[right])}, so vowels = {vowels}.",
                   **snap(right, [0, right], {right: "current"}))
            # @trace-end
        most = vowels  # the first full window is the best so far  # @a:first
        # @trace-begin
        best_win = [0, k - 1]
        T.step("first", "update", f"The first window [0, {k - 1}] is full, so most = vowels = {most}.",
               **snap(None, [0, k - 1], flash=True))
        # @trace-end
        for right in range(k, len(s)):  # slide: one letter in, one out  # @a:loop
            T.step("loop", "next", f"Next round of the second for loop: right moves to index {right}. The window slides one step to the right.", **snap(right, [left, right - 1]))  # @trace
            if is_vowel(s[right]):  # new letter enters on the right  # @a:add
                vowels += 1
            # @trace-begin
            T.op()
            T.step("add", "add", f"s[{right}] = '{s[right]}' enters. It is {kind(s[right])}, so vowels = {vowels}. "
                   f"The window now has k + 1 = {k + 1} letters, one too many.",
                   **snap(right, [left, right], {right: "current"}))
            # @trace-end
            if is_vowel(s[left]):  # oldest letter leaves on the left  # @a:drop
                vowels -= 1
            left += 1
            # @trace-begin
            T.op()
            T.step("drop", "drop", f"s[{left - 1}] = '{s[left - 1]}' leaves. It is {kind(s[left - 1])}, so vowels = {vowels}. "
                   f"left moves to {left}, and the window [{left}, {right}] has k = {k} letters again.",
                   **snap(right, [left, right], {left - 1: "removed"}))
            old = most
            # @trace-end
            most = max(most, vowels)  # keep the largest vowel count  # @a:update
            # @trace-begin
            if most > old:
                best_win = [left, right]
                T.step("update", "update", f"vowels = {vowels} > old most {old}, so most = {most}. "
                       f"Window [{left}, {right}] has the most vowels so far.", **snap(right, [left, right], flash=True))
            else:
                T.step("update", "compare", f"vowels = {vowels} is not more than most = {most}. most stays.",
                       **snap(right, [left, right]))
            # @trace-end
        # @trace-begin
        T.step("return", "return", f"Return most = {most}, the vowels in window [{best_win[0]}, {best_win[1]}]. "
               "Every window of length k was checked once, so no window has more vowels.", **snap(None, None))
        # @trace-end
        return most  # @a:return
