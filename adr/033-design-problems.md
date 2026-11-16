# 033 — Design problems (classes) in LeetCode's format

Status: accepted · 2026-11-16

## Context
LC 303 Range Sum Query – Immutable asks for a class (NumArray) with a constructor and a method that is called many times. build.py only knew problems with one function. More class problems will come with stacks, queues and caches.

## Options we discussed
- **A** — rewrite such a problem as one function (nums, queries) → answers
- **B** — support classes in LeetCode's own format: a list of calls and a list of arguments
- **B without C** — the same, but only Python and C++, because C may be dropped soon

## Decision
B, with C. The signature has "design": true, the class name, a C prefix, the constructor and the methods. Examples use LeetCode's { calls, args } form and its output with null for the constructor. C follows LeetCode's form (struct + Create / method / Free).

## Why
- The code on the page is exactly what LeetCode accepts, so it can be submitted and get a ✓.
- One format for every class problem; the work is done once in build.py.
- The C part is generated, not written by hand, so keeping it costs little.

## Trade-offs
- build.py has a second driver for classes; the C part goes away if C is dropped.
- Long call lists make long animations; pages pick short examples.

Depends on: 003, 005 · Affects: —
Revisit when: a class problem needs a state that is not an array (a linked list, a tree), so the page needs a new way to show it.
