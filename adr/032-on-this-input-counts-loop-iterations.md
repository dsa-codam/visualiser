# 032 — "On this input" counts loop iterations

Status: accepted · 2026-11-16

## Context
ADR 013 put the line "On this input: brute force needs X …, this approach needs Y" on every page. What counts as one operation was chosen per problem (opsUnit), and each page placed T.op() for its own unit: minute checks, pair sums, comparisons, additions. Some pages counted two operations in one loop run, others skipped work outside a loop. Numbers could not be compared across pages, and they did not follow how Big O counts work. While we built LC 1480, the word "steps" also clashed with the "Step 4 / 6" counter of the animation.

## Options we discussed
- **A** — keep one unit per page (opsUnit)
- **B** — "steps" everywhere
- **C** — "additions" everywhere
- **D** — "iterations" everywhere: how many times loop bodies run

## Decision
D. This replaces the "chosen per problem" part of ADR 013.
- One T.op() per run of a loop body, in brute.py and in solution.py. With nested loops, every run of every loop counts, outer and inner. A loop in a helper function that the solution calls counts too.
- A loop of fixed size that does not grow with n (for example the 26 letters in LC 424) is not counted: it is O(1) in Big O.
- A comprehension in code shown to readers is a loop: T.op(len(...))  # @trace on the next line.
- Library calls (sort, slicing, comparing two lists) are not counted.
- opsUnit defaults to "iterations". Pages do not set it. All pages move to it now, while the project is small.
- The line reads: "On this input (size = <length of the longest array or string argument>): brute force needs X iterations, this approach needs Y." "iteration" in the singular when the number is 1. We say "size", not "n", because some problems have their own parameter named n (LC 88).
- When this approach needs as many iterations as brute force or more (small inputs, where the pattern's setup is not paid back yet), the line adds: "Small inputs hide the gain; it grows with input size."

## Why
- Big O counts how many times loop bodies run, not what happens inside them. The counter now teaches the same thing.
- One unit makes pages comparable and removes a choice from every new page.

## Trade-offs
- A heavy loop body and a light one count the same.
- Work hidden in library calls is not counted.
- Work inside fixed-size loops is not visible in the counter.

Depends on: 013 · Affects: 013
Revisit when: a page needs to count work that has no loop, such as recursion or a library call that matters for the lesson.
