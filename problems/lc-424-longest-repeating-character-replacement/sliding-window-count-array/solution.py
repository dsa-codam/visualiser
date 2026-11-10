def idx(letter):  # position of a letter in count: 'A' -> 0, ..., 'Z' -> 25 (letter - 'A' in C)
    return ord(letter) - ord('A')


def find_top(count):  # returns the most common letter in the window ('A' to 'Z'): one pass over the 26 letters
    top = 'A'  # most common letter so far
    for letter in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
        if count[idx(letter)] > count[idx(top)]:  # strict '>': on a tie the first letter in alphabetical order stays
            top = letter
    return top


class Solution:
    def characterReplacement(self, s: str, k: int) -> int:
        count = [0] * 26  # letter -> times it is in the window (s is 'A' to 'Z')  # @a:init
        left = 0  # left edge of the window  # @a:init
        longest = 0  # longest good window so far  # @a:init
        # @trace-begin
        letters = sorted(set(s))  # count rows, in alphabetical order (the order find_top uses)
        best_win = None
        length = top_letter = top_count = changes = None  # declared inside the for loop in C and C++

        def cnt(ch):
            return count[idx(ch)]

        def check_text():
            tied = [c for c in letters if cnt(c) == top_count]
            tie = f" Tie {' = '.join(tied)} → {top_letter} chosen: find_top keeps the first letter in alphabetical order." if len(tied) > 1 else ""
            return (f"length = {length}, top letter '{top_letter}' is there {top_count} times, "
                    f"so changes = {length} − {top_count} = {changes}.{tie}")

        def snap(right, roles=None, flash=False):
            window = None if right is None else [left, right]
            bad = window is not None and changes > k
            return dict(
                state={"arr": list(s), "k": k, "left": left, "right": right, "window": window,
                       "bad": bad, "replace": [i for i in range(left, right + 1) if s[i] != top_letter] if bad else [],
                       "rows": [{"key": c, "value": cnt(c)} for c in letters],
                       "length": length, "topLetter": top_letter, "topCount": top_count, "changes": changes,
                       "longest": longest, "bestWindow": best_win},
                roles=roles or {},
                vars=[
                    {"label": "left", "value": left, "role": "back"},
                    {"label": "right", "value": "—" if right is None else right, "role": "front"},
                    {"label": "s[right]", "value": "—" if right is None else f"'{s[right]}'"},
                    {"label": "length", "value": "—" if length is None else length},
                    {"label": "top_letter", "value": "—" if top_letter is None else f"'{top_letter}'"},
                    {"label": "top_count", "value": "—" if top_count is None else top_count},
                    {"label": "changes", "value": "—" if changes is None else changes},
                    {"label": "k", "value": k},
                    {"label": "longest", "value": longest, "flash": flash},
                ],
            )

        T.step("init", "init", f"count is all zeros, left = 0, longest = 0. A window is good if it needs at most k = {k} changes: "
               "changes = length − (count of its most common letter).", **snap(None))
        # @trace-end
        for right in range(len(s)):  # right edge, moves every step  # @a:add
            count[idx(s[right])] += 1  # add s[right] to the window  # @a:add
            length = right - left + 1  # letters in the window [left, right]  # @a:add
            top_letter = find_top(count)  # most common letter in the window  # @a:add
            top_count = count[idx(top_letter)]  # how often top_letter is in the window  # @a:add
            changes = length - top_count  # letters to change so that all are top_letter  # @a:add
            # @trace-begin
            T.op()
            head = (f"The for loop starts: right = 0, add '{s[right]}'." if right == 0
                    else f"Next round: right moves to {right}, add '{s[right]}'.") + f" Recompute: {check_text()}"
            if changes > k:
                T.step("add", "expand", f"{head} That is > k = {k}: the red cells are the {changes} letters to change. "
                       "Too many, so the while loop will run.", **snap(right, {right: "current"}))
            else:
                T.step("add", "expand", f"{head} That is ≤ k = {k}, so the window is good and the while loop does not run.",
                       **snap(right, {right: "current"}))
            # @trace-end
            while changes > k:  # bad window: more letters to change than k  # @a:drop
                count[idx(s[left])] -= 1  # drop s[left] from the window  # @a:drop
                left += 1  # shrink from the left  # @a:drop
                length = right - left + 1  # length of the smaller window  # @a:drop
                top_letter = find_top(count)  # most common letter in the smaller window  # @a:drop
                top_count = count[idx(top_letter)]  # its count in the smaller window  # @a:drop
                changes = length - top_count  # letters to change in the smaller window  # @a:drop
                # @trace-begin
                T.op()
                head = f"while changes > k: drop s[{left - 1}] = '{s[left - 1]}', left moves to {left}. Recompute: {check_text()}"
                if changes > k:
                    T.step("drop", "shrink", f"{head} Still > k = {k}, so the loop runs again.", **snap(right, {left - 1: "removed"}))
                else:
                    T.step("drop", "shrink", f"{head} Now ≤ k = {k}, so the while loop stops.", **snap(right, {left - 1: "removed"}))
                # @trace-end
            old = longest  # @trace
            longest = max(longest, length)  # the window is good here: keep the longest  # @a:update
            # @trace-begin
            if longest > old:
                best_win = [left, right]
                T.step("update", "update", f"Window [{left}, {right}] = \"{s[left:right + 1]}\" is good and has length = {length} > old longest {old}, so longest = {longest}.",
                       **snap(right, flash=True))
            else:
                T.step("update", "compare", f"Window [{left}, {right}] = \"{s[left:right + 1]}\" is good, but length = {length} is not more than longest = {longest}. longest stays.",
                       **snap(right))
            # @trace-end
        # @trace-begin
        length = top_letter = top_count = changes = None  # out of scope after the loop, as in C++
        b0, b1 = best_win
        T.step("return", "return", f"Return longest = {longest}: the window [{b0}, {b1}] = \"{s[b0:b1 + 1]}\" becomes one letter with at most k = {k} changes. "
               "Adding a letter never lowers changes, so a bad window stays bad when right moves: left never has to go back, "
               "and after the while loop each window is the longest good one that ends at right.", **snap(None))
        # @trace-end
        return longest  # @a:return
