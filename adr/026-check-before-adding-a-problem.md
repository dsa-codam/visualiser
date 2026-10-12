# 026 — Check before adding a problem

Status: accepted · 2026-10-12

## Context
Nothing stopped Claude from building a problem that is already in problems/. If the user gave the same problem again, Claude could rewrite the existing page or add a second folder for it. Keeping a separate list of done problems by hand would get out of date.

## Options we discussed
- **A** — keep a separate list of done problems
- **B** — only a rule in the skill: look in problems/ before starting
- **C** — a rule in the skill that runs a script, plus a check in build.py

## Decision
C. problems/ stays the only list.
- `python3 build.py --check <id>` prints the problem and its approaches, or "not found". It builds nothing. Without an id it lists every problem.
- Workflow A starts with this check. If the problem is there, Claude stops and asks: new approach, change one, or nothing.
- build.py fails if two folders have the same source (site + id, or url when there is no id), or if two approaches in one problem have the same name.
- The same pattern twice in one problem is allowed (ADR 022 makes "Two pointers" broad), so it is only a warning in the skill, not a build error.

## Why
- The script gives the same answer every time and does not depend on how a folder was named.
- The check in build.py also runs in CI, so it catches the same mistake in pull requests from other people.
- Reading one short output is cheaper than listing folders and opening JSON files.

## Trade-offs
- A problem from another site with a different id (for example the same task on NeetCode) is not seen as a duplicate. This is fine: finding the same task across sites was never a goal. People search by the number they know. If we add other sources, we link the pages to each other instead.

Depends on: 006, 016, 019 · Affects: 022
Revisit when: problems from a second source are added.
