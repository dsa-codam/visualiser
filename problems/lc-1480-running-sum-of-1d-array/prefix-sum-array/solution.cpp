#include <vector>  // @hide
using namespace std;  // @hide

class Solution {
public:
    vector<int> runningSum(vector<int>& nums) {
        int n = nums.size();  // @a:init
        vector<int> result(n);  // result[i] = nums[0] + nums[1] + ... + nums[i]  // @a:init
        result[0] = nums[0];  // the first running sum is just the first number  // @a:first
        for (int i = 1; i < n; i++) {  // every next index  // @a:add
            result[i] = result[i - 1] + nums[i];  // previous sum + one new number (|sum| <= 10^9: fits in int)  // @a:add
        }
        return result;  // @a:return
    }
};
