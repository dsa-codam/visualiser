#include <stdlib.h>  // @hide

int* runningSum(int* nums, int numsSize, int* returnSize) {
    int n = numsSize;  // @a:init
    int* result = malloc(n * sizeof(int));  // result[i] = nums[0] + nums[1] + ... + nums[i]; the caller frees it  // @a:init
    result[0] = nums[0];  // the first running sum is just the first number  // @a:first
    for (int i = 1; i < n; i++) {  // every next index  // @a:add
        result[i] = result[i - 1] + nums[i];  // previous sum + one new number (|sum| <= 10^9: fits in int)  // @a:add
    }
    *returnSize = n;  // @a:return
    return result;  // @a:return
}
