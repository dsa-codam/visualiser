class Solution:
    def minimumRecolors(self, blocks: str, k: int) -> int:
        whites = 0  # number of 'W' in the window = recolors it needs  # @a:init
        left = 0  # left edge of the window
        # @trace-begin
        best_win = None
        fewest = None

        def snap(right, window, roles=None, flash=False):
            return dict(
                state={"arr": list(blocks), "k": k, "left": left, "right": right, "window": window, "whites": whites,
                       "fewest": fewest, "bestWindow": best_win},
                roles=roles or {},
                vars=[
                    {"label": "left", "value": left, "role": "back"},
                    {"label": "right", "value": "—" if right is None else right, "role": "front"},
                    {"label": "whites", "value": whites},
                    {"label": "fewest", "value": "—" if fewest is None else fewest, "flash": flash},
                ],
            )

        T.step("init", "init", f"whites = 0, left = 0. To make a window of k = {k} blocks all black, "
               "each 'W' in it needs one recolor, so we count the 'W' in the window.", **snap(None, None))
        # @trace-end
        for right in range(k):  # build the first window blocks[0..k-1]  # @a:build-loop
            # @trace-begin
            T.step("build-loop", "build", f"The first for loop fills the first window: right = {right}." if right == 0 else
                   f"Next round of the first for loop: right = {right} < k = {k}.",
                   **snap(right, [0, right - 1] if right > 0 else None))
            # @trace-end
            if blocks[right] == 'W':  # @a:build
                whites += 1
            # @trace-begin
            T.op()
            T.step("build", "build", f"blocks[{right}] = '{blocks[right]}': " +
                   (f"a white block enters, whites = {whites}." if blocks[right] == 'W' else f"already black, whites stays {whites}."),
                   **snap(right, [0, right], {right: "current"}))
            # @trace-end
        fewest = whites  # the first full window is the best so far  # @a:first
        # @trace-begin
        best_win = [0, k - 1]
        T.step("first", "update", f"The first window [0, {k - 1}] is full, so fewest = whites = {fewest}.",
               **snap(None, [0, k - 1], flash=True))
        # @trace-end
        for right in range(k, len(blocks)):  # slide: one block in, one out  # @a:loop
            T.step("loop", "next", f"Next round of the second for loop: right moves to index {right}. The window slides one step to the right.", **snap(right, [left, right - 1]))  # @trace
            if blocks[right] == 'W':  # new block enters on the right  # @a:add
                whites += 1
            # @trace-begin
            T.op()
            T.step("add", "add", f"blocks[{right}] = '{blocks[right]}' enters: " +
                   (f"it is white, so whites = {whites}." if blocks[right] == 'W' else f"it is black, so whites stays {whites}."),
                   **snap(right, [left, right], {right: "current"}))
            # @trace-end
            if blocks[left] == 'W':  # oldest block leaves on the left  # @a:drop
                whites -= 1
            left += 1
            # @trace-begin
            T.op()
            T.step("drop", "drop", f"blocks[{left - 1}] = '{blocks[left - 1]}' leaves: " +
                   (f"it was white, so whites = {whites}." if blocks[left - 1] == 'W' else f"it was black, so whites stays {whites}.") +
                   f" left moves to {left}, and the window [{left}, {right}] has k = {k} blocks again.",
                   **snap(right, [left, right], {left - 1: "removed"}))
            old = fewest
            # @trace-end
            fewest = min(fewest, whites)  # keep the smallest number of recolors  # @a:update
            # @trace-begin
            if fewest < old:
                best_win = [left, right]
                T.step("update", "update", f"whites = {whites} < old fewest {old}, so fewest = {fewest}. "
                       f"Window [{left}, {right}] needs the fewest recolors so far.", **snap(right, [left, right], flash=True))
            else:
                T.step("update", "compare", f"whites = {whites} is not less than fewest = {fewest}. fewest stays.",
                       **snap(right, [left, right]))
            # @trace-end
        # @trace-begin
        T.step("return", "return", f"Return fewest = {fewest}: recolor the {fewest} white block(s) in window "
               f"[{best_win[0]}, {best_win[1]}]. Every window of length k was checked once, so no window needs fewer recolors.",
               **snap(None, None))
        # @trace-end
        return fewest  # @a:return
