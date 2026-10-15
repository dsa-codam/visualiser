# 028 — Same steps in every language, no hidden work

Status: accepted · 2026-10-15

## Context
While we added the fixed-size sliding window problems (LC 643, LC 1343, LC 2379), the question came up how close the Python, C++ and C solutions must be to each other and to the animation. Idiomatic Python often hides the steps of a pattern: `blocks[i:i+k].count('W')` or `sum(nums[i:i+k])` looks like one line, but it walks the whole window again. A reader then sees a highlighted line that does more work than the step describes, and the real complexity is O(n·k), not O(n).

## Options we discussed
- **A** — all three languages follow the same steps as the animation, using only index access and simple variables
- **B** — idiomatic code in each language (slicing, `.count()`, `sum()`, `substr`), even when it hides steps

## Decision
Option A, for every problem and every language:
- solution.py, solution.cpp and solution.c follow the same sequence of steps as the animation. Every step maps to the same anchored lines in each language.
- Strings are treated as arrays of characters, as in C.
- Allowed: index access and simple variables (counters, indices, running min/max). Idiomatic syntax that does not hide a step is fine: for / range, len(), min(), max(), a tuple swap.
- Not allowed: anything that hides a step of the pattern or changes the complexity: slicing, `.count()`, `sum()` over a window, `sorted()` inside a loop, `substr` / `strncmp` / `std::count` inside a loop.
- For example, a window counter is updated step by step: +1 for the element that enters, −1 for the element that leaves.
- One approach = one data structure, the same in every language and the same as the animation. A count array is an array in Python, C++ and C. A hash map is dict / defaultdict in Python and std::unordered_map in C++ (not std::map, which is a tree), and there is no C version. If a problem can be solved with both, they are two approaches with two tabs (ADR 006).
- The rule applies to the clean solution. Lines marked @trace may use anything (copies of the state, slices in captions).

## Why
- The highlighted line always does exactly what the caption says, in every language.
- The code shows the real complexity. A beginner cannot copy a hidden O(n·k) solution and think it is O(n).
- The three languages can be compared line by line, which also makes the C version easy to write.
- It keeps the JavaScript port from ADR 005 simple.

## Trade-offs
- The Python code is longer than the shortest idiomatic solution. People who know Python may find it less "pythonic".
- build.py does not check this rule. It is kept by review only.

Depends on: 004, 005, 006 · Affects: —
Revisit when: club members ask for idiomatic versions on several pages, or a pattern cannot be shown without a library call.
