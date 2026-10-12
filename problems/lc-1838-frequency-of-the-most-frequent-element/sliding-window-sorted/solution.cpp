#include <algorithm>  // @hide
#include <vector>  // @hide
using namespace std;  // @hide

class Solution {
public:
    int maxFrequency(vector<int>& nums, int k) {
        sort(nums.begin(), nums.end());  // the cheapest values to raise sit just before nums[right]  // @a:sort
        int left = 0;  // left edge of the window  // @a:init
        long long total = 0;  // sum of nums[left..right]; can reach 10^10
        int longest = 0;  // largest valid window so far
        for (int right = 0; right < (int)nums.size(); right++) {  // right edge: nums[right] is the target value  // @a:loop
            total += nums[right];  // add nums[right] to the window  // @a:expand
            long long cost = (long long)nums[right] * (right - left + 1) - total;  // increments to raise the whole window to nums[right]
            while (cost > k) {  // too many increments: shrink from the left  // @a:while
                total -= nums[left];  // drop nums[left] from the window  // @a:shrink
                left++;
                cost = (long long)nums[right] * (right - left + 1) - total;
            }
            int length = right - left + 1;  // valid window: all can become nums[right]  // @a:length
            longest = max(longest, length);  // @a:update
        }
        return longest;  // @a:return
    }
};
