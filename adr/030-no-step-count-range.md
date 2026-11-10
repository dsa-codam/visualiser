# 030 — No step-count range; warn only on long inputs

Status: accepted · 2026-11-10

## Context
ADR 012 set "aim for 15–40 steps" on main examples, and build.py warned outside that range. We set the numbers before we used them. While we reworked LC 424, the grouped steps of ADR 029 made LeetCode Example 1 ("ABAB", k = 2) 10 steps long, and build.py warned about it. The range has no real basis: the number of steps depends on the problem and on how steps are grouped, not on whether the example is good. A LeetCode example is also never changed, so a warning about it cannot lead to an action.

## Options we discussed
- **A** — keep the 15–40 range and its warning
- **B** — drop the step-count range; warn only when a main input is long, and never for LeetCode examples

## Decision
B. This replaces only the step-count part of ADR 012. The limit of 10 elements on main examples and the hard limit of 20 elements stay.
- build.py does not check the number of steps.
- build.py warns "example input is long, check if a shorter one works" when a main example has more than 10 elements.
- No warning for LeetCode examples. An example with "expected" comes from the statement (schemas.md), so build.py uses that field to recognise it.

## Why
- A warning should lead to an action. For a LeetCode example there is none.
- The input length is what matters on a phone (ADR 009, ADR 012); the step count follows from it.

## Trade-offs
- A very long animation is no longer reported. We rely on review and on the 10-element limit.
- An example of our own that has "expected" by mistake also gets no warning.

Depends on: 012, 029 · Affects: 012
Revisit when: club members say an animation is too long or too short to follow.
