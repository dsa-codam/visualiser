#include <stdlib.h>  // @hide

int numberOfSubarrays(int* nums, int numsSize, int k) {
    int n = numsSize;  // @a:init
    int* cnt = calloc(n + 1, sizeof(int));  // cnt[p] = how many prefixes so far have exactly p odd numbers  // @a:init
    cnt[0] = 1;  // the empty prefix (before nums[0]) has 0 odd numbers  // @a:init
    int odd = 0;  // odd numbers in nums[0..i]  // @a:init
    int nice = 0;  // nice subarrays found so far (at most n(n + 1) / 2 ~ 1.25 * 10^9: fits in int)  // @a:init
    for (int i = 0; i < n; i++) {  // @a:add
        odd += nums[i] % 2;  // 1 if nums[i] is odd, 0 if even  // @a:add
        if (odd >= k) {  // @a:add
            nice += cnt[odd - k];  // each earlier prefix with odd - k odd numbers starts a nice subarray ending at i  // @a:add
        }
        cnt[odd]++;  // remember this prefix for later ends  // @a:store
    }
    free(cnt);  // @a:return
    return nice;  // @a:return
}
