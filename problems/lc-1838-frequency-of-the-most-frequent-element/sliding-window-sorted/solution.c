#include <stdlib.h>  // @hide

static int compare_ints(const void* a, const void* b) {  // for qsort: ascending order
    int x = *(const int*)a, y = *(const int*)b;
    return (x > y) - (x < y);
}

int maxFrequency(int* nums, int numsSize, int k) {
    qsort(nums, numsSize, sizeof(int), compare_ints);  // the cheapest values to raise sit just before nums[right]  // @a:sort
    int left = 0;  // left edge of the window  // @a:init
    long long total = 0;  // sum of nums[left..right]; can reach 10^10
    int longest = 0;  // largest valid window so far
    for (int right = 0; right < numsSize; right++) {  // right edge: nums[right] is the target value  // @a:loop
        total += nums[right];  // add nums[right] to the window  // @a:expand
        long long cost = (long long)nums[right] * (right - left + 1) - total;  // increments to raise the whole window to nums[right]
        while (cost > k) {  // too many increments: shrink from the left  // @a:while
            total -= nums[left];  // drop nums[left] from the window  // @a:shrink
            left++;
            cost = (long long)nums[right] * (right - left + 1) - total;
        }
        int length = right - left + 1;  // valid window: all can become nums[right]  // @a:length
        if (length > longest) {  // @a:update
            longest = length;
        }
    }
    return longest;  // @a:return
}
