#include <algorithm>  // @hide
#include <vector>  // @hide
using namespace std;  // @hide

class Solution {
public:
    int minimumDifference(vector<int>& nums, int k) {
        sort(nums.begin(), nums.end());  // close scores are now neighbours  // @a:sort
        int left = 0;  // left edge of the window  // @a:init
        int smallest = nums[nums.size() - 1] - nums[0];  // the widest gap: no k scores differ by more
        for (int right = k - 1; right < (int)nums.size(); right++) {  // right edge: nums[left..right] has k scores  // @a:loop
            int diff = nums[right] - nums[left];  // sorted, so this is the highest minus the lowest of the window  // @a:diff
            smallest = min(smallest, diff);  // keep the smallest difference  // @a:update
            left++;  // the next window starts one step to the right  // @a:slide
        }
        return smallest;  // @a:return
    }
};
