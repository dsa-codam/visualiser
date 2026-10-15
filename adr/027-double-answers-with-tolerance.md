# 027 — "double" answers, compared within 10⁻⁵

Status: accepted · 2026-10-15

## Context
LC 643 Maximum Average Subarray I returns a double. The statement says: "Any answer with a calculation error less than 10⁻⁵ will be accepted." build.py supported only void, int, long, bool and int[] returns, and compared answers as exact text.

## Options we discussed
- **A** — a new return type `"double"`: the drivers print 10 decimal places, and build.py accepts an answer when |got − brute| < 10⁻⁵
- **B** — exact comparison of the printed text, rounded to a fixed number of decimals

## Decision
Option A. `signature.returns = "double"` is supported in Python, C++ and C. One helper, `same_answer()`, does every comparison (statement examples, clean Python, traced Python, C++ and C). For all other return types it still compares exactly.

## Why
- It copies LeetCode's own rule, so every answer LeetCode accepts also passes here.
- Option B can fail on a correct answer when two values round to different sides of the last decimal.
- Other problems with averages or ratios will reuse it.

## Trade-offs
- An answer that is wrong by less than 10⁻⁵ passes. LeetCode accepts it too.
- The tolerance is fixed. A problem with a different tolerance needs a new field.

Depends on: 003, 004 · Affects: 025
Revisit when: a problem states a tolerance other than 10⁻⁵, or returns double[].
