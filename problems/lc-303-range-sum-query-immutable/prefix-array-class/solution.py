from typing import List  # @hide


class NumArray:
    def __init__(self, nums: List[int]):
        n = len(nums)  # @a:init
        self.pre = [0] * (n + 1)  # pre[k] = nums[0] + ... + nums[k - 1]; pre[0] = 0  # @a:init
        # @trace-begin
        self._nums = nums[:]
        self._built = 1
        self._answers = []
        T.step("init", "build", f"Constructor: pre gets n + 1 = {n + 1} slots. pre[0] = 0 is the sum of no numbers. "
               "All the work happens here, once.", **self._snap(None, None, None, {0: "new"}))
        # @trace-end
        for i in range(n):  # build the prefix array once  # @a:build
            T.op()  # @trace
            self.pre[i + 1] = self.pre[i] + nums[i]  # @a:build
            # @trace-begin
            self._built = i + 2
            T.step("build", "build", f"pre[{i + 1}] = pre[{i}] + nums[{i}] = {self.pre[i]} + ({nums[i]}) = {self.pre[i + 1]}.",
                   **self._snap(i, None, None, {i + 1: "new"}))
            # @trace-end

    # @trace-begin
    def _snap(self, i, left, right, pre_roles=None, ans=None):
        return dict(
            state={"nums": self._nums, "pre": self.pre[:], "built": self._built, "i": i, "left": left, "right": right,
                   "answers": self._answers[:], "pre_roles": pre_roles or {}},
            roles={i: "current"} if i is not None else {},
            vars=[
                {"label": "left", "value": "—" if left is None else left, "role": "back"},
                {"label": "right", "value": "—" if right is None else right, "role": "front"},
                {"label": "answer", "value": "—" if ans is None else ans, "flash": ans is not None},
            ],
        )
    # @trace-end

    def sumRange(self, left: int, right: int) -> int:
        T.op()  # @trace
        # @trace-begin
        ans = self.pre[right + 1] - self.pre[left]
        self._answers.append(ans)
        T.step("query", "query", f"sumRange({left}, {right}) = pre[{right + 1}] − pre[{left}] = {self.pre[right + 1]} − ({self.pre[left]}) = {ans}. "
               "One subtraction, whatever the length of the range.",
               **self._snap(None, left, right, {right + 1: "current", left: "current"}, ans))
        # @trace-end
        return self.pre[right + 1] - self.pre[left]  # sum of nums[left..right]  # @a:query
