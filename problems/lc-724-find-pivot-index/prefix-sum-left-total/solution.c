int pivotIndex(int* nums, int numsSize) {
    int total = 0;  // sum of the whole array (|total| <= 10^4 * 1000 = 10^7: fits in int)  // @a:init
    for (int i = 0; i < numsSize; i++) {  // first pass  // @a:total
        total += nums[i];  // @a:total
    }
    int left = 0;  // sum of nums[0..i-1]; nothing to the left of index 0  // @a:left0
    for (int i = 0; i < numsSize; i++) {  // second pass: try each index  // @a:check
        int right = total - left - nums[i];  // everything except the left side and nums[i]  // @a:check
        if (left == right) {  // @a:check
            return i;  // @a:return
        }
        left += nums[i];  // nums[i] moves to the left side for the next index  // @a:move
    }
    return -1;  // @a:none
}
