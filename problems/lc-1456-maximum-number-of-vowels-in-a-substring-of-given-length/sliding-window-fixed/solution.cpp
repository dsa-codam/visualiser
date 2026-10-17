#include <algorithm>  // @hide
#include <string>  // @hide
using namespace std;  // @hide

static bool is_vowel(char c) {  // five comparisons: constant time
    return c == 'a' || c == 'e' || c == 'i' || c == 'o' || c == 'u';
}

class Solution {
public:
    int maxVowels(string s, int k) {
        int vowels = 0;  // number of vowels in the window  // @a:init
        int left = 0;  // left edge of the window
        for (int right = 0; right < k; right++) {  // build the first window s[0..k-1]  // @a:build-loop
            if (is_vowel(s[right])) {  // @a:build
                vowels++;
            }
        }
        int most = vowels;  // the first full window is the best so far  // @a:first
        for (int right = k; right < (int)s.size(); right++) {  // slide: one letter in, one out  // @a:loop
            if (is_vowel(s[right])) {  // new letter enters on the right  // @a:add
                vowels++;
            }
            if (is_vowel(s[left])) {  // oldest letter leaves on the left  // @a:drop
                vowels--;
            }
            left++;
            most = max(most, vowels);  // keep the largest vowel count  // @a:update
        }
        return most;  // @a:return
    }
};
