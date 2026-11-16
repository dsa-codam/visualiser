#include <vector>  // @hide
using namespace std;  // @hide

class Solution {
public:
    vector<bool> isArraySpecial(vector<int>& nums, vector<vector<int>>& queries) {
        int n = nums.size();  // @a:init
        vector<int> pre(n, 0);  // pre[i] = bad pairs (same parity) inside nums[0..i]  // @a:init
        for (int i = 1; i < n; i++) {  // pair (i - 1, i)  // @a:build
            pre[i] = pre[i - 1];  // @a:build
            if (nums[i] % 2 == nums[i - 1] % 2) {  // same parity: a bad pair  // @a:build
                pre[i]++;  // @a:build
            }
        }
        vector<bool> answer;  // @a:answer
        for (int j = 0; j < (int)queries.size(); j++) {  // @a:query
            int left = queries[j][0];  // @a:query
            int right = queries[j][1];  // @a:query
            int bad = pre[right] - pre[left];  // bad pairs with both numbers inside nums[left..right]  // @a:query
            answer.push_back(bad == 0);  // special = no bad pair  // @a:query
        }
        return answer;  // @a:return
    }
};
