def brute(nums, k):
    n = len(nums)
    smallest = None
    for i in range(n):  # nums[i] as the lowest score of the group
        for j in range(n):  # nums[j] as the highest score of the group
            if nums[j] < nums[i]:
                continue
            count = 0  # scores between nums[i] and nums[j]
            for x in nums:
                T.op()  # @trace
                if nums[i] <= x <= nums[j]:
                    count += 1
            if count >= k:  # k of them can form a group with this lowest and highest
                diff = nums[j] - nums[i]
                if smallest is None or diff < smallest:
                    smallest = diff
    return smallest
