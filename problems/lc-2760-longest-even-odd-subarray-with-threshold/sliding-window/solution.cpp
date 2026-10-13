#include <algorithm>  // @hide
#include <vector>  // @hide
using namespace std;  // @hide

class Solution {
public:
    int longestAlternatingSubarray(vector<int>& nums, int threshold) {
        int left = 0;  // left edge of the window; left > right means there is no window  // @a:init
        int longest = 0;  // longest valid window so far
        for (int right = 0; right < (int)nums.size(); right++) {  // right edge, moves every step  // @a:loop
            if (nums[right] > threshold) {  // no valid window can contain nums[right]  // @a:over
                left = right + 1;  // @a:reset
            } else if (left == right || nums[right] % 2 == nums[right - 1] % 2) {  // the window cannot grow to right  // @a:restart
                if (nums[right] % 2 == 0) {
                    left = right;  // an even value starts a new window  // @a:start
                } else {
                    left = right + 1;  // an odd value cannot start a window  // @a:skip
                }
            }
            if (left <= right) {  // there is a window [left, right]
                int length = right - left + 1;  // @a:length
                longest = max(longest, length);  // @a:update
            }
        }
        return longest;  // @a:return
    }
};
