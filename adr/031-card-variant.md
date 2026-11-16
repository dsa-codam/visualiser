# 031 — card.variant: the form of the pattern

Status: accepted · 2026-11-16

## Context
While we built LC 1480 Running Sum of 1d Array, the "Why this pattern?" card needed one more line: this page uses an inclusive prefix sum, not the version with a leading 0 (sentinel) that range-sum problems use. The card had only signals, pattern and core idea, and viz.js showed only those fields. Other patterns have the same question: a sliding window can be fixed-size or variable-size, two pointers can move towards each other or in the same direction.

## Options we discussed
- **A** — put the form into the core idea text
- **B** — an optional field card.variant, shown as its own "Variant:" line after "Core idea"

## Decision
B.
- card.variant names the sub-type of the pattern that this solution uses, for example "inclusive prefix sum", "exclusive prefix sum with sentinel", "fixed-size window", "variable-size window", "opposite-direction pointers", and says in one or two sentences why this form fits.
- Fill it when the pattern has more than one form. Leave it out when it has only one.
- It is free text for now, not a fixed list.
- Existing pages are not backfilled in one go. A page gets card.variant the next time it is edited.

## Why
- The form decides details a learner copies: the array length (n or n + 1), the loop bounds, the formula.
- A separate line is easy to find and compare across pages; inside the core idea it gets lost.

## Trade-offs
- Free text: two pages can name the same form in different words until we fix a list.
- For a while some pages have the line and others do not.

Depends on: 018, 022 · Affects: —
Revisit when: about five pages use card.variant, so we can see which names repeat and decide on a fixed list.
