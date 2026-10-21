# Design system — meaning

Status: extracted from the first prototype pages (LC 283 Move Zeroes, LC 2958), October 2026.

This file says what each design element **means**. The values (hex codes, pixels, timings) live only in `core/tokens.css`. The live preview of everything is `docs/gallery.html` (source `core/gallery.html`).

Adding or changing anything here follows workflow C in SKILL.md: propose → user approves → update tokens.css / viz.css / viz.js → gallery.html → this file.

## 1. Colour roles
One colour = one meaning, on every page. A colour is never reused for something else.

| Token | Meaning | Used for |
|---|---|---|
| --role-back | Trailing pointer | left, slow, lo |
| --role-front | Leading pointer | right, fast, hi |
| --role-mid | Computed position | mid (proposal, not used on a page yet) |
| --role-current | Examined now | the element the code is looking at in this step; at most one per step |
| --role-swap | Swap | two elements changing places; drawn with the "swap" arc |
| --role-conflict | Rule broken | the element that breaks the rule, and its "!" / ">k" badge |
| --role-best | Answer | best so far, element in its final place, the result |
| --role-new | Just added | pushed, inserted, enqueued (proposal) |
| --role-gone | Dropped | left the window for good, discarded half |
| --zero | Empty value | values the problem treats as "nothing", such as 0 in Move Zeroes |
| --slot-fill | Count | one occurrence in a count map |
| --band-window | Active range | sliding window, binary-search range |
| --band-best | Answer range | placed zone, best window |
| --band-gap | Waiting range | a range that only holds "empty" values |

Surface tokens: --bg (page), --panel (cards), --ink (text), --muted (secondary text), --line (borders), --code-bg, --code-hl (highlighted code line), --badge-ink (text on a filled badge).

## 2. Never colour alone
Every meaning also has a non-colour signal:
- pointers: a text label under ▲
- conflict: a red badge with text ("!", ">k")
- dropped / out: strike-through and lower opacity
- zero: dashed border
- done: a ✓ in the corner (hidden when cells are very small)
- duplicates of an over-limit value: dashed red border
- measure annotation: arrows with text labels and a text line ("k = 3", "3 + 1 + 3 = 7")

## 3. Pointer names (ADR 011)
left / right — towards each other, and sliding window edges · slow / fast — same direction, linked lists · lo / mid / hi — binary search · p1 / p2 / write — merging two arrays (ADR 021: write is --role-back, p1 and p2 are --role-front). The trailing pointer is always --role-back, the leading one --role-front. Code variable names match the labels.

## 3a. Measure annotation (ArrayRow { measure: true })
Arrows over a range of cells that show a length or a radius, with a label on each arrow and one optional text line under them. It sits in its own lane between the band label and the indices; the lane is kept on every step, so rows do not jump. Colour comes from a pointer role (back / front / mid), usually the role of the pointer the arrows start from. Origin "center": two arrows from the middle of a cell out to the range edges (an arrow with no length is left out). Origin "start" / "end": one arrow across the range. The text line is a string; for origin "center" it can also be { left, center, right }: center sits exactly under the origin cell (also when k = 0 and no dot is drawn), left ends just before it, right starts just after it (e.g. "3 +" · "1" · "+ 3 = 7"). An object with origin "start" / "end" is invalid. Invalid input is reported with console.error and nothing is drawn.

## 4. Cell states (CSS classes on .ar-cell)
`current`, `swap`, `conflict` (+ tag), `dup`, `done`, `best`, `new`, `zero`, `removed`, `out`. Several can combine (e.g. `zero swap`).

## 5. Legend swatch names (approach.json → "legend")
Problem pages do not show the legend for now (ADR 023). Keep writing it for every approach.

`ptr-back`, `ptr-front`, `ptr-mid`, `current`, `swap`, `conflict`, `dup`, `done`, `best`, `new`, `zero`, `removed`, `out`, `band-window`, `band-best`, `band-gap`, `bar`, `slot`, `slot-over`. List only the ones used on that page, with a label tied to the problem ("left: left edge of the window").

## 6. Size limits (ADR 012)
- Preset "main" example limits are in SKILL.md, workflow A step 4. Reason: about 9–10 cells fit a 375px phone screen.
- Renderer: up to 20 elements. Cells shrink from 60px to 30px pitch; below that the canvas scrolls sideways inside its panel, never the page.

## 7. Typography and layout
- UI font: system-ui stack. Values, indices and code: monospace stack.
- Page max width 1080px. From 900px: animation and code on the left, variables, controls and caption on the right (ADR 017). Below 900px everything stacks.
- Indices sit above the cells; pointers below.
- No horizontal page scroll at 375px (checked by the smoke test).

## 8. Motion
- Cell moves (swaps): --t-move. Colour changes: --t-colour. New best value: flash for --t-flash.
- prefers-reduced-motion turns all of them off; autoplay still works.
- No decorative animation. Every movement shows a state change.

## 9. Themes
Light and dark follow the system setting. Pages also accept `data-theme="light|dark"` on `<html>` (used by the gallery's theme buttons).
