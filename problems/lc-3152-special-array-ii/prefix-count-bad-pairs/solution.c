#include <stdbool.h>  // @hide
#include <stdlib.h>  // @hide

bool* isArraySpecial(int* nums, int numsSize, int** queries, int queriesSize, int* queriesColSize, int* returnSize) {
    (void)queriesColSize;  // every query has 2 numbers, so this is not needed
    int n = numsSize;  // @a:init
    int* pre = calloc(n, sizeof(int));  // pre[i] = bad pairs (same parity) inside nums[0..i]  // @a:init
    for (int i = 1; i < n; i++) {  // pair (i - 1, i)  // @a:build
        pre[i] = pre[i - 1];  // @a:build
        if (nums[i] % 2 == nums[i - 1] % 2) {  // same parity: a bad pair  // @a:build
            pre[i]++;  // @a:build
        }
    }
    bool* answer = malloc(queriesSize * sizeof(bool));  // the caller frees it  // @a:answer
    for (int j = 0; j < queriesSize; j++) {  // @a:query
        int left = queries[j][0];  // @a:query
        int right = queries[j][1];  // @a:query
        int bad = pre[right] - pre[left];  // bad pairs with both numbers inside nums[left..right]  // @a:query
        answer[j] = (bad == 0);  // special = no bad pair  // @a:query
    }
    free(pre);  // @a:return
    *returnSize = queriesSize;  // @a:return
    return answer;  // @a:return
}
