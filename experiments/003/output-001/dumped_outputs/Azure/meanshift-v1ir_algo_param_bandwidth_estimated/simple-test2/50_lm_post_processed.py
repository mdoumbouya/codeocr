def twoSum(nums, target):
    for i in range(len(nums)):
        for p in range(i, len(nums)):
            if (nums[i] + nums[p] == target):
                return [i, p]
