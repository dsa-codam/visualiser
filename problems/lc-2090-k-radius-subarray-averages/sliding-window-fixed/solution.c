#include <stdlib.h>  // @hide

int* getAverages(int* nums, int numsSize, int k, int* returnSize) {
    int n = numsSize;  // @a:init
    int* avgs = malloc(n * sizeof(int));  // the caller frees it
    for (int i = 0; i < n; i++) {
        avgs[i] = -1;  // -1 stays wherever there is no full window
    }
    *returnSize = n;
    int size = 2 * k + 1;  // window length: k numbers, the centre, k numbers
    if (size > n) {  // the window does not fit: every answer is -1  // @a:fits
        return avgs;
    }
    long long total = 0;  // sum of the window; up to 10^10, so long long  // @a:total
    for (int right = 0; right < size; right++) {  // build the first window nums[0..size-1]  // @a:build-loop
        total += nums[right];  // @a:build
    }
    int center = k;  // the first window [0, size-1] is centred at index k  // @a:first
    avgs[center] = total / size;  // integer division; nums are non-negative, so truncation is what LeetCode expects, and the average is at most 10^5, so it fits in int
    int left = 0;  // left edge of the window
    for (int right = size; right < n; right++) {  // slide: one number in, one out  // @a:loop
        total += nums[right];  // new number enters on the right  // @a:add
        total -= nums[left];  // oldest number leaves on the left  // @a:drop
        left++;
        center = left + k;  // the middle of the new window  // @a:write
        avgs[center] = total / size;
    }
    return avgs;  // @a:return
}
