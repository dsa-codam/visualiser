#include <vector>  // @hide
using namespace std;  // @hide

class NumArray {
    vector<int> pre;  // pre[k] = nums[0] + ... + nums[k - 1]; |pre[k]| <= 10^4 * 10^5 = 10^9: fits in int

public:
    NumArray(vector<int>& nums) {
        int n = nums.size();  // @a:init
        pre.assign(n + 1, 0);  // pre[0] = 0  // @a:init
        for (int i = 0; i < n; i++) {  // build the prefix array once  // @a:build
            pre[i + 1] = pre[i] + nums[i];  // @a:build
        }
    }

    int sumRange(int left, int right) {
        return pre[right + 1] - pre[left];  // sum of nums[left..right]  // @a:query
    }
};
