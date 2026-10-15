double findMaxAverage(int* nums, int numsSize, int k) {
    int total = 0;  // sum of the window  // @a:init
    int left = 0;  // left edge of the window
    for (int right = 0; right < k; right++) {  // build the first window nums[0..k-1]  // @a:build-loop
        total += nums[right];  // @a:build
    }
    int largest = total;  // the first full window is the best so far  // @a:first
    for (int right = k; right < numsSize; right++) {  // slide: one element in, one out  // @a:loop
        total += nums[right];  // new element enters on the right  // @a:add
        total -= nums[left];  // oldest element leaves on the left  // @a:drop
        left++;
        if (total > largest) {  // keep the largest window sum  // @a:update
            largest = total;
        }
    }
    return (double)largest / k;  // divide only once, at the end  // @a:return
}
