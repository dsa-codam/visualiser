#include <stdlib.h>  // @hide

static int ascending(const void* a, const void* b) {  // compare function for qsort
    int x = *(const int*)a, y = *(const int*)b;
    return (x > y) - (x < y);
}

int* answerQueries(int* nums, int numsSize, int* queries, int queriesSize, int* returnSize) {
    int n = numsSize;  // @a:sort
    qsort(nums, n, sizeof(int), ascending);  // the smallest numbers first: the best subsequence takes them  // @a:sort
    int* pre = calloc(n + 1, sizeof(int));  // pre[c] = sum of the c smallest numbers; max 1000 * 10^6 = 10^9: fits in int  // @a:sort
    for (int i = 0; i < n; i++) {  // build the prefix array  // @a:build
        pre[i + 1] = pre[i] + nums[i];  // @a:build
    }
    int* answer = calloc(queriesSize, sizeof(int));  // the caller frees it  // @a:answer
    for (int j = 0; j < queriesSize; j++) {  // one binary search per query  // @a:query
        int lo = 1;  // try counts from 1 to n  // @a:query
        int hi = n;  // @a:query
        int count = 0;  // largest count that fits so far  // @a:query
        while (lo <= hi) {  // @a:mid
            int mid = lo + (hi - lo) / 2;  // @a:mid
            if (pre[mid] <= queries[j]) {  // the mid smallest numbers fit  // @a:mid
                count = mid;  // @a:fit
                lo = mid + 1;  // try more numbers  // @a:fit
            } else {  // @a:mid
                hi = mid - 1;  // too much: try fewer numbers  // @a:nofit
            }
        }
        answer[j] = count;  // @a:store
    }
    free(pre);  // @a:return
    *returnSize = queriesSize;  // @a:return
    return answer;  // @a:return
}
