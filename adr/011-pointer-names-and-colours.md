# 011 — Pointer names follow the pattern; colours follow the role

Status: accepted · 2026-10-06

## Context
The prototype pages used names from each problem (write / read, l / r). That made the same idea look different on different pages. We considered start / end for pointers moving towards each other, but chose the names readers meet on LeetCode and in interviews.

## Decision
| Pattern | Names |
|---|---|
| Two pointers towards each other | left / right |
| Sliding window | left / right |
| Same direction, linked list | slow / fast |
| Binary search | lo / mid / hi |
| Fixed window with the answer at its middle | left / right / center |

center is the middle of a fixed window (e.g. LC 2090: center = left + k), coloured --role-mid.

The trailing pointer is always blue (--role-back), the leading one orange (--role-front), mid is --role-mid. Code variables use the same names as the labels.

## Trade-offs
- Two pointers and sliding window share left / right; the picture (window band or not) tells them apart.
- Move Zeroes code now says slow / fast instead of write / read.

Note (2026-10-21): the list was extended with center for LC 2090 K Radius Subarray Averages.

Depends on: 002 · Affects: —
Revisit when: club members are confused by the shared left / right names.
