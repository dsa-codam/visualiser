#include <stdlib.h>  // @hide

int* sortedSquares(int* nums, int numsSize, int* returnSize) {
    int n = numsSize;  // @a:init
    int* result = malloc(n * sizeof(int));  // the caller frees it; filled from the back
    int left = 0;  // most negative value
    int right = n - 1;  // most positive value
    int write = n - 1;  // next slot to fill: the largest square goes last
    while (left <= right) {  // @a:loop
        int left_square = nums[left] * nums[left];  // at most 10^8: fits in int  // @a:squares
        int right_square = nums[right] * nums[right];
        if (left_square > right_square) {  // the left end has the larger square  // @a:compare
            result[write] = left_square;  // @a:takeLeft
            left++;
        } else {
            result[write] = right_square;  // @a:takeRight
            right--;
        }
        write--;  // @a:advance
    }
    *returnSize = n;
    return result;  // @a:done
}
