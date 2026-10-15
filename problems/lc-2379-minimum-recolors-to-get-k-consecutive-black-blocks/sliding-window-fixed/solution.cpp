#include <algorithm>  // @hide
#include <string>  // @hide
using namespace std;  // @hide

class Solution {
public:
    int minimumRecolors(string blocks, int k) {
        int whites = 0;  // number of 'W' in the window = recolors it needs  // @a:init
        int left = 0;  // left edge of the window
        for (int right = 0; right < k; right++) {  // build the first window blocks[0..k-1]  // @a:build-loop
            if (blocks[right] == 'W') {  // @a:build
                whites++;
            }
        }
        int fewest = whites;  // the first full window is the best so far  // @a:first
        for (int right = k; right < (int)blocks.size(); right++) {  // slide: one block in, one out  // @a:loop
            if (blocks[right] == 'W') {  // new block enters on the right  // @a:add
                whites++;
            }
            if (blocks[left] == 'W') {  // oldest block leaves on the left  // @a:drop
                whites--;
            }
            left++;
            fewest = min(fewest, whites);  // keep the smallest number of recolors  // @a:update
        }
        return fewest;  // @a:return
    }
};
