#include <vector>  // @hide
#include <algorithm>  // @hide
using namespace std;  // @hide

class Solution {
public:
    vector<int> answerQueries(vector<int>& nums, vector<int>& queries) {
        int n = nums.size();  // @a:sort
        sort(nums.begin(), nums.end());  // the smallest numbers first: the best subsequence takes them  // @a:sort
        vector<int> pre(n + 1, 0);  // pre[c] = sum of the c smallest numbers; max 1000 * 10^6 = 10^9: fits in int  // @a:sort
        for (int i = 0; i < n; i++) {  // build the prefix array  // @a:build
            pre[i + 1] = pre[i] + nums[i];  // @a:build
        }
        vector<int> answer(queries.size(), 0);  // @a:answer
        for (int j = 0; j < (int)queries.size(); j++) {  // one binary search per query  // @a:query
            int lo = 1;  // try counts from 1 to n  // @a:query
            int hi = n;  // @a:query
            int count = 0;  // largest count that fits so far  // @a:query
            while (lo <= hi) {  // @a:mid
                int mid = lo + (hi - lo) / 2;  // @a:mid
                if (pre[mid] <= queries[j]) {  // the mid smallest numbers fit  // @a:mid
                    count = mid;  // @a:fit
                    lo = mid + 1;  // try more numbers  // @a:fit
                } else {  // @a:mid
                    hi = mid - 1;  // too much: try fewer numbers  // @a:nofit
                }
            }
            answer[j] = count;  // @a:store
        }
        return answer;  // @a:return
    }
};
