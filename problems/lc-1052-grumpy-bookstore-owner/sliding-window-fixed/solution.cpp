#include <algorithm>  // @hide
#include <vector>  // @hide
using namespace std;  // @hide

class Solution {
public:
    int maxSatisfied(vector<int>& customers, vector<int>& grumpy, int minutes) {
        int n = customers.size();  // @a:init
        int satisfied = 0;  // customers of calm minutes: happy without the technique
        for (int i = 0; i < n; i++) {  // @a:base-loop
            if (grumpy[i] == 0) {  // the owner is calm, so these customers are happy  // @a:base
                satisfied += customers[i];
            }
        }
        int extra = 0;  // grumpy-minute customers in the window: the technique wins them back  // @a:extra
        for (int right = 0; right < minutes; right++) {  // build the first window [0, minutes - 1]  // @a:build-loop
            if (grumpy[right] == 1) {  // @a:build
                extra += customers[right];
            }
        }
        int max_extra = extra;  // the first full window is the best so far  // @a:first
        int left = 0;  // left edge of the window
        for (int right = minutes; right < n; right++) {  // slide: one minute in, one out  // @a:loop
            if (grumpy[right] == 1) {  // new minute enters on the right  // @a:add
                extra += customers[right];
            }
            if (grumpy[left] == 1) {  // oldest minute leaves on the left  // @a:drop
                extra -= customers[left];
            }
            left++;
            max_extra = max(max_extra, extra);  // keep the window that wins back the most  // @a:update
        }
        return satisfied + max_extra;  // @a:return
    }
};
