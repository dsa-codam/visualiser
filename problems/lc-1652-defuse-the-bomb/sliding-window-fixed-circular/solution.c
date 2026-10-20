#include <stdlib.h>  // @hide

int* decrypt(int* code, int codeSize, int k, int* returnSize) {
    int n = codeSize;  // @a:init
    int* result = calloc(n, sizeof(int));  // all zeros: this is already the answer when k == 0; the caller frees it
    *returnSize = n;
    if (k == 0) {  // @a:zero
        return result;
    }
    int left, right;
    if (k > 0) {  // the window of code[0] is the next k numbers  // @a:start
        left = 1;
        right = k;
    } else {  // the window of code[0] is the previous -k numbers
        left = n + k;
        right = n - 1;
    }
    int total = 0;  // sum of the numbers in the window  // @a:total
    for (int j = left; j <= right; j++) {  // build the first window code[left..right]  // @a:build-loop
        total += code[j];  // @a:build
    }
    result[0] = total;  // the first window belongs to code[0]  // @a:first
    for (int i = 1; i < n; i++) {  // slide the window one step for each next i  // @a:loop
        right = (right + 1) % n;  // after n - 1 comes 0  // @a:add
        total += code[right];  // new number enters on the right
        total -= code[left];  // oldest number leaves on the left  // @a:drop
        left = (left + 1) % n;
        result[i] = total;  // this window belongs to code[i]  // @a:write
    }
    return result;  // @a:return
}
