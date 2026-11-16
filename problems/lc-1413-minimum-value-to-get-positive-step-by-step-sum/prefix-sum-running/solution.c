int minStartValue(int* nums, int numsSize) {
    int total = 0;  // running sum: nums[0] + ... + nums[i] (|total| <= 100 * 100 = 10^4: fits in int)  // @a:init
    int lowest = 0;  // lowest running sum so far; 0 = before any number  // @a:init
    for (int i = 0; i < numsSize; i++) {  // @a:add
        total += nums[i];  // add one more number  // @a:add
        if (total < lowest) {  // a new lowest point  // @a:add
            lowest = total;  // @a:add
        }
    }
    int start_value = 1 - lowest;  // startValue + lowest must be at least 1  // @a:return
    return start_value;  // @a:return
}
