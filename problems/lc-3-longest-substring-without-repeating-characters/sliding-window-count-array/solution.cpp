#include <algorithm>  // @hide
#include <string>  // @hide
#include <vector>  // @hide
using namespace std;  // @hide

class Solution {
public:
    int lengthOfLongestSubstring(string s) {
        vector<int> count(128, 0);  // character code -> times it is in the window (s is ASCII)  // @a:init
        int left = 0;  // left edge of the window
        int longest = 0;  // longest unique window so far
        for (int right = 0; right < (int)s.size(); right++) {  // right edge, moves every step  // @a:loop
            count[(unsigned char)s[right]]++;  // add s[right] to the window  // @a:expand
            while (count[(unsigned char)s[right]] > 1) {  // only s[right] can be a repeat  // @a:while
                count[(unsigned char)s[left]]--;  // drop s[left] from the window  // @a:shrink
                left++;
            }
            int length = right - left + 1;  // unique window: its length  // @a:length
            longest = max(longest, length);  // @a:update
        }
        return longest;  // @a:return
    }
};
