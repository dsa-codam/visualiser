#include <stdlib.h>  // @hide

typedef struct {
    int* pre;  // pre[k] = nums[0] + ... + nums[k - 1]; |pre[k]| <= 10^4 * 10^5 = 10^9: fits in int
} NumArray;

NumArray* numArrayCreate(int* nums, int numsSize) {
    int n = numsSize;  // @a:init
    NumArray* obj = malloc(sizeof(NumArray));  // @a:init
    obj->pre = calloc(n + 1, sizeof(int));  // pre[0] = 0  // @a:init
    for (int i = 0; i < n; i++) {  // build the prefix array once  // @a:build
        obj->pre[i + 1] = obj->pre[i] + nums[i];  // @a:build
    }
    return obj;
}

int numArraySumRange(NumArray* obj, int left, int right) {
    return obj->pre[right + 1] - obj->pre[left];  // sum of nums[left..right]  // @a:query
}

void numArrayFree(NumArray* obj) {
    free(obj->pre);
    free(obj);
}
