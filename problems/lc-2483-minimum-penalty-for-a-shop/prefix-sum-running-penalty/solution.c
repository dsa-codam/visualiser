int bestClosingTime(char* customers) {
    int penalty = 0;  // penalty if the shop closes at hour 0: every 'Y' is missed  // @a:init
    for (int i = 0; customers[i] != '\0'; i++) {  // first pass: count the 'Y'  // @a:count
        if (customers[i] == 'Y') {  // @a:count
            penalty++;  // @a:count
        }
    }
    int best = penalty;  // lowest penalty so far  // @a:start
    int best_hour = 0;  // the earliest hour with that penalty  // @a:start
    for (int j = 0; customers[j] != '\0'; j++) {  // hour j becomes an open hour: now the shop closes at j + 1  // @a:move
        if (customers[j] == 'Y') {  // @a:move
            penalty--;  // these customers are served now  // @a:move
        } else {  // @a:move
            penalty++;  // open, but nobody comes  // @a:move
        }
        if (penalty < best) {  // strictly lower, so ties keep the earlier hour  // @a:update
            best = penalty;  // @a:update
            best_hour = j + 1;  // @a:update
        }
    }
    return best_hour;  // @a:return
}
