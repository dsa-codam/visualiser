from typing import List  # @hide


class Solution:
    def decrypt(self, code: List[int], k: int) -> List[int]:
        n = len(code)  # @a:init
        result = [0] * n  # all zeros: this is already the answer when k == 0
        # @trace-begin
        left = right = total = None
        i = j = None
        written = 0

        def snap(window=None, roles=None, new=None, flash=False):
            return dict(
                state={"code": list(code), "result": list(result), "k": k, "left": left, "right": right,
                       "window": window, "total": total, "written": written, "newAt": new},
                roles=roles or {},
                vars=[
                    {"label": "k", "value": k},
                    {"label": "left", "value": "—" if left is None else left, "role": "back"},
                    {"label": "right", "value": "—" if right is None else right, "role": "front"},
                    {"label": "j", "value": "—" if j is None else j},
                    {"label": "total", "value": "—" if total is None else total, "flash": flash},
                    {"label": "i", "value": "—" if i is None else i},
                ],
            )

        def win():
            return [left, right]

        T.step("init", "init", f"n = {n}. result starts as {n} zeros. Each result[i] will get the sum of a window "
               f"of |k| = {abs(k)} numbers next to code[i].", **snap())
        # @trace-end
        if k == 0:  # @a:zero
            T.step("zero", "return", "k == 0, so every number is replaced with 0. Return result, which is all zeros.", **snap())  # @trace
            return result
        T.step("zero", "init", f"k = {k} is not 0, so we need windows of |k| = {abs(k)} numbers.", **snap())  # @trace
        if k > 0:  # the window of code[0] is the next k numbers  # @a:start
            left = 1
            right = k
        else:  # the window of code[0] is the previous -k numbers
            left = n + k
            right = n - 1
        # @trace-begin
        side = "after" if k > 0 else "before"
        T.step("start", "init", f"k {'> 0' if k > 0 else '< 0'}: the window of code[0] is the {abs(k)} numbers {side} it, "
               f"so left = {left} and right = {right}. Inside [0, n − 1], so no wrap yet.", **snap())
        # @trace-end
        total = 0  # sum of the numbers in the window  # @a:total
        T.step("total", "init", "total = 0. We add the numbers of the first window one by one.", **snap())  # @trace
        for j in range(left, right + 1):  # build the first window code[left..right]  # @a:build-loop
            # @trace-begin
            T.step("build-loop", "build", f"The first for loop adds the first window: j = {j}." if j == left else
                   f"Next round of the first for loop: j = {j} ≤ right = {right}.",
                   **snap([left, j - 1] if j > left else None))
            # @trace-end
            total += code[j]  # @a:build
            # @trace-begin
            T.op()
            T.step("build", "build", f"code[{j}] = {code[j]} is added, so total = {total}.",
                   **snap([left, j], {j: "current"}))
            # @trace-end
        # @trace-begin
        j = None
        # @trace-end
        result[0] = total  # the first window belongs to code[0]  # @a:first
        # @trace-begin
        written = 1
        T.step("first", "write", f"The first window [{left}, {right}] is full: result[0] = total = {total}.",
               **snap(win(), new=0, flash=True))
        # @trace-end
        for i in range(1, n):  # slide the window one step for each next i  # @a:loop
            T.step("loop", "next", f"Next round of the second for loop: i = {i}. The window moves one step to the right.", **snap(win()))  # @trace
            right = (right + 1) % n  # after n - 1 comes 0  # @a:add
            total += code[right]  # new number enters on the right
            # @trace-begin
            T.op()
            wrap = " (it wraps from n − 1 to 0)" if right == 0 else ""
            T.step("add", "add", f"right = {right}{wrap}. code[{right}] = {code[right]} enters, so total = {total}. "
                   f"The window now has |k| + 1 = {abs(k) + 1} numbers, one too many.",
                   **snap(win(), {right: "current"}))
            # @trace-end
            total -= code[left]  # oldest number leaves on the left  # @a:drop
            left = (left + 1) % n
            # @trace-begin
            gone = (left - 1) % n
            wrap = " (it wraps from n − 1 to 0)" if left == 0 else ""
            T.op()
            T.step("drop", "drop", f"code[{gone}] = {code[gone]} leaves, so total = {total}. left = {left}{wrap}, "
                   f"and the window has |k| = {abs(k)} numbers again.", **snap(win(), {gone: "removed"}))
            # @trace-end
            result[i] = total  # this window belongs to code[i]  # @a:write
            # @trace-begin
            written = i + 1
            T.step("write", "write", f"result[{i}] = total = {total}.", **snap(win(), new=i, flash=True))
            # @trace-end
        # @trace-begin
        i = None
        T.step("return", "return", f"Return result = {result}. Each window was made from the one before it by adding one "
               "number and removing one, so every sum is correct and each number is touched only a few times.", **snap())
        # @trace-end
        return result  # @a:return
