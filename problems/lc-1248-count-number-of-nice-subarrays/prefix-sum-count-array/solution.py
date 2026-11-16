from typing import List  # @hide


class Solution:
    def numberOfSubarrays(self, nums: List[int], k: int) -> int:
        n = len(nums)  # @a:init
        cnt = [0] * (n + 1)  # cnt[p] = how many prefixes so far have exactly p odd numbers  # @a:init
        cnt[0] = 1  # the empty prefix (before nums[0]) has 0 odd numbers  # @a:init
        odd = 0  # odd numbers in nums[0..i]  # @a:init
        nice = 0  # nice subarrays found so far  # @a:init
        # @trace-begin
        look = None  # index odd - k looked up in this step

        def snap(i, cnt_roles=None, roles=None, flash=None):
            return dict(
                state={"nums": nums[:], "cnt": cnt[:], "i": i, "odd": odd, "k": k, "nice": nice,
                       "look": look, "cnt_roles": cnt_roles or {}},
                roles=roles or {},
                vars=[
                    {"label": "i", "value": "—" if i is None else i, "role": "front"},
                    {"label": "odd", "value": odd, "flash": flash == "odd"},
                    {"label": "odd − k", "value": "—" if look is None else look},
                    {"label": "nice", "value": nice, "flash": flash == "nice"},
                ],
            )

        T.step("init", "init", f"cnt has n + 1 = {n + 1} slots, one for each possible number of odd values in a prefix. "
               "cnt[0] = 1: the empty prefix, before nums[0], has 0 odd numbers.", **snap(None, {0: "new"}))
        # @trace-end
        for i in range(n):  # @a:add
            T.op()  # @trace
            odd += nums[i] % 2  # 1 if nums[i] is odd, 0 if even  # @a:add
            # @trace-begin
            kind = "odd" if nums[i] % 2 else "even"
            look = odd - k if odd >= k else None
            # @trace-end
            if odd >= k:  # @a:add
                nice += cnt[odd - k]  # each earlier prefix with odd - k odd numbers starts a nice subarray ending at i  # @a:add
            # @trace-begin
            if look is not None:
                msg = (f"i = {i}: nums[{i}] = {nums[i]} is {kind}, odd = {odd}. A subarray ending at i is nice if the prefix before it "
                       f"has odd − k = {odd} − {k} = {look} odd numbers. cnt[{look}] = {cnt[look]}, so nice = {nice - cnt[look]} + {cnt[look]} = {nice}.")
                T.step("add", "add", msg, **snap(i, {look: "current"}, {i: "current"}, "nice"))
            else:
                T.step("add", "add", f"i = {i}: nums[{i}] = {nums[i]} is {kind}, odd = {odd} < k = {k}: "
                       "no subarray ending here can have k odd numbers yet.", **snap(i, None, {i: "current"}, "odd"))
            # @trace-end
            cnt[odd] += 1  # remember this prefix for later ends  # @a:store
            # @trace-begin
            T.step("store", "store", f"The prefix nums[0..{i}] has {odd} odd numbers: cnt[{odd}] = {cnt[odd]}.",
                   **snap(i, {odd: "new"}, {i: "current"}))
            look = None
            # @trace-end
        # @trace-begin
        T.step("return", "return", f"Return nice = {nice}. Each nice subarray is counted once, at its last index, "
               "by the prefix that ends just before it.", **snap(None))
        # @trace-end
        return nice  # @a:return
