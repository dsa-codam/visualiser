# 029 — Steps grouped by meaning; one step can highlight several lines

Status: accepted · 2026-11-10

## Context
While we reworked LC 424 (Longest Repeating Character Replacement), the page had a step for each code line, as the rule in SKILL.md asked: a step on the `for` line at the start of every round, a step on the `while` line before its body, and separate steps for "add" and "check". On the `for` step the right pointer already sat outside the window, and the window label switched between a short form ("window [0, 1]") and the full check. These steps carried no meaning for a learner. The engine could not help: build.py stored one line per anchor and stopped when an anchor was used twice, and viz.js highlighted exactly one line.

## Options we discussed
- **A** — keep one step per line and the step on every loop header
- **B** — group lines into steps by meaning; one step highlights all lines of its group

## Decision
B.
- A step is one action a learner can name: "add s[right]", "drop s[left]", "update best". It highlights every line that belongs to that action.
- A `for` / `while` line gets its own step only when the line itself decides something (`while lo <= hi` in binary search). Otherwise it belongs to the group that starts the round: the `for` line goes with "add s[right]", the `while` line with "drop s[left]".
- No step shows a pointer outside the range it marks.
- The same `@a:<name>` may mark several lines. build.py stores each anchor as a list of line numbers. viz.js highlights all of them and scrolls the code box to the first one. A single number is still read correctly.
- The groups are the same in Python, C++ and C (ADR 028).
- Pages built before this ADR keep their one-line steps. The rule applies to new pages and to pages we change.

## Why
- Every step changes something the learner can see: the window grows, shrinks, or the best value changes.
- Labels stay in one format, because every step comes after the values they show are computed.
- Fewer steps for the same input: LC 424 Example 2 goes from 38 to 20 steps.

## Trade-offs
- A learner does not see the loop header on its own step, so "the loop starts again" is said in the caption, not shown by a separate highlight.
- Pages built before this ADR use the old style until we touch them, so the site mixes both styles for a while.
- A highlighted group of several lines says less about which line does what; the code comments must carry that.

Depends on: 017, 028 · Affects: —
Revisit when: club members say they lose track of where a loop starts, or a page needs a step inside a group (e.g. a line-by-line debug view).
