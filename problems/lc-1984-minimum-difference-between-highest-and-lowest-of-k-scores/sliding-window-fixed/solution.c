#include <stdlib.h>  // @hide

static int compare_ints(const void* a, const void* b) {  // for qsort: ascending order
    int x = *(const int*)a, y = *(const int*)b;
    return (x > y) - (x < y);
}

int minimumDifference(int* nums, int numsSize, int k) {
    qsort(nums, numsSize, sizeof(int), compare_ints);  // close scores are now neighbours  // @a:sort
    int left = 0;  // left edge of the window  // @a:init
    int smallest = nums[numsSize - 1] - nums[0];  // the widest gap: no k scores differ by more
    for (int right = k - 1; right < numsSize; right++) {  // right edge: nums[left..right] has k scores  // @a:loop
        int diff = nums[right] - nums[left];  // sorted, so this is the highest minus the lowest of the window  // @a:diff
        if (diff < smallest) {  // keep the smallest difference  // @a:update
            smallest = diff;
        }
        left++;  // the next window starts one step to the right  // @a:slide
    }
    return smallest;  // @a:return
}
