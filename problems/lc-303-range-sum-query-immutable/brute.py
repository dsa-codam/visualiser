class NumArray:
    def __init__(self, nums):
        self.nums = nums  # keep the numbers, nothing else

    def sumRange(self, left, right):
        T.op()  # @trace
        total = 0
        for i in range(left, right + 1):  # add the range from scratch on every call
            T.op()  # @trace
            total += self.nums[i]
        return total
