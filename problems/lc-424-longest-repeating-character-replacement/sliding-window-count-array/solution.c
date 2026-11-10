static char find_top(const int count[26]) {  // returns the most common letter in the window ('A' to 'Z'): one pass over the 26 letters
    int top = 0;  // index of the most common letter so far
    for (int i = 0; i < 26; i++) {
        if (count[i] > count[top]) {  // strict '>': on a tie the first letter in alphabetical order stays
            top = i;
        }
    }
    return 'A' + top;
}

int characterReplacement(char* s, int k) {
    int count[26] = {0};  // letter -> times it is in the window (s is 'A' to 'Z')  // @a:init
    int left = 0;  // left edge of the window  // @a:init
    int longest = 0;  // longest good window so far  // @a:init
    for (int right = 0; s[right] != '\0'; right++) {  // right edge, moves every step  // @a:add
        count[s[right] - 'A']++;  // add s[right] to the window  // @a:add
        int length = right - left + 1;  // letters in the window [left, right]
        char top_letter = find_top(count);  // most common letter in the window
        int top_count = count[top_letter - 'A'];  // how often top_letter is in the window
        int changes = length - top_count;  // letters to change so that all are top_letter
        while (changes > k) {  // bad window: more letters to change than k  // @a:drop
            count[s[left] - 'A']--;  // drop s[left] from the window  // @a:drop
            left++;  // shrink from the left  // @a:drop
            length = right - left + 1;  // length of the smaller window
            top_letter = find_top(count);  // most common letter in the smaller window
            top_count = count[top_letter - 'A'];  // its count in the smaller window
            changes = length - top_count;  // letters to change in the smaller window
        }
        if (length > longest) {  // the window is good here: keep the longest  // @a:update
            longest = length;  // @a:update
        }  // @a:update
    }
    return longest;  // @a:return
}
