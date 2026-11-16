#include <vector>  // @hide
#include <algorithm>  // @hide
using namespace std;  // @hide

class Solution {
public:
    int subarraySum(vector<int>& nums) {
        int n = nums.size();  // @a:init
        vector<int> pre(n + 1, 0);  // pre[i] = nums[0] + ... + nums[i - 1]; pre[0] = 0 (max 100 * 1000 = 10^5)  // @a:init
        for (int i = 0; i < n; i++) {  // build the prefix array  // @a:build
            pre[i + 1] = pre[i] + nums[i];  // @a:build
        }
        int total = 0;  // at most 100 * 10^5 = 10^7: fits in int  // @a:total0
        for (int i = 0; i < n; i++) {  // one subarray for every index i  // @a:query
            int start = max(0, i - nums[i]);  // the subarray is nums[start..i]  // @a:query
            int subarray_sum = pre[i + 1] - pre[start];  // sum of nums[start..i]  // @a:query
            total += subarray_sum;  // @a:query
        }
        return total;  // @a:return
    }
};
