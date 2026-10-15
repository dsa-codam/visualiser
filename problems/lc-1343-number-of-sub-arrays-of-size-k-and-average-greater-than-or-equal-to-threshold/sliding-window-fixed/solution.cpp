#include <vector>  // @hide
using namespace std;  // @hide

class Solution {
public:
    int numOfSubarrays(vector<int>& arr, int k, int threshold) {
        int min_sum = threshold * k;  // average >= threshold  <=>  sum >= threshold * k  // @a:init
        int total = 0;  // sum of the window
        int left = 0;  // left edge of the window
        int count = 0;  // windows with average >= threshold
        for (int right = 0; right < k; right++) {  // build the first window arr[0..k-1]  // @a:build-loop
            total += arr[right];  // @a:build
        }
        if (total >= min_sum) {  // check the first full window  // @a:check-first
            count++;
        }
        for (int right = k; right < (int)arr.size(); right++) {  // slide: one element in, one out  // @a:loop
            total += arr[right];  // new element enters on the right  // @a:add
            total -= arr[left];  // oldest element leaves on the left  // @a:drop
            left++;
            if (total >= min_sum) {  // @a:check
                count++;
            }
        }
        return count;  // @a:return
    }
};
