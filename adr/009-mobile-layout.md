# 009 — Pages work on phones

Status: accepted · 2026-10-06

## Context
The first LC 283 page adapted to small screens; the LC 2958 page did not. The project is also a portfolio piece and may be opened on a phone during an interview or a club session.

## Decision
Every page works at 375px wide with no sideways page scroll. Panels stack; array cells shrink; a long array scrolls inside its own panel. The smoke test checks this on every build.

Below 900px every panel takes the full width of the page (`align-items: stretch` in the one-column layout), and array cells are sized from that width. Band labels and the best-bar label stay inside their card: ArrayRow moves a label sideways only as far as needed, and wraps it only if it is wider than the card.

Note (2026-10-24): before this, panels on phones shrank to their content. Cells then stayed at about their smallest size (24px) whatever the screen width, and labels near the right end went past the card, so the card scrolled sideways (found on LC 3, 643, 1456, 1695, 1838, 1984, 2379, 2760 and 2958). Pages with a title above the array were already full width. A card with a long array (9 or 10 cells at the smallest cell size) was wider than the page column; now it keeps the column width and the array scrolls inside it, as this decision says.

## Trade-offs
- Some layout code for small screens in core.
- A label that was moved is not exactly over its band. It still overlaps the band, and the text names the window.
- A wrapped label makes the row taller on that step, so the row (for a band label) or the rows under it (for a bar label) move down. This only happens when a label is wider than the whole card; no page does this today.

Depends on: 002 · Affects: 012, 017
Revisit when: —
