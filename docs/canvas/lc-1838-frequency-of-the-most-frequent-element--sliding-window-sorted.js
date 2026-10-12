/* Generated from problems/lc-1838-frequency-of-the-most-frequent-element/sliding-window-sorted/canvas.js */
VIZ.canvas.register("lc-1838-frequency-of-the-most-frequent-element/sliding-window-sorted", /* LC 1838 · sort + sliding window.
   Reads step.state = { arr, ids, left, right, window, total, cost, k, longest, bestWindow, tags }
   and step.roles = { pos: "current" | "conflict" | "removed" }.
   The first step shows nums before sorting; ids make the cells slide into sorted order.
   Draws only with VIZ.ArrayRow — no colours or sizes here. */
({
  build(ctx) {
    ctx.row = new VIZ.ArrayRow(ctx.canvas, ctx.example.args.nums, { roles: ["back", "front"], bar: true });
  },

  render(step, ctx) {
    const s = step.state, roles = step.roles, right = s.right;
    const cls = {};
    s.arr.forEach((v, i) => {
      const c = [], role = roles[i];
      if (role === "removed") c.push("removed");
      else if (right !== null && i < s.left) c.push("out");
      if (step.phase === "return" && s.bestWindow && i >= s.bestWindow[0] && i <= s.bestWindow[1]) c.push("best");
      if (role === "current") c.push("current");
      if (role === "conflict") c.push("conflict");
      cls[i] = c.join(" ");
    });
    const w = s.window;
    const costText = s.cost === null ? `total ${s.total}` : `cost ${s.cost} ${s.cost > s.k ? ">" : "≤"} k = ${s.k}`;
    ctx.row.update({
      arr: s.arr,
      ids: s.ids,
      cls,
      tags: s.tags,
      bands: w ? [{ kind: "window", from: w[0], to: w[1], label: `window [${w[0]}, ${w[1]}] · ${costText}` }] : [],
      pointers: [
        { role: "back", label: "left", at: right === null ? null : s.left },
        { role: "front", label: "right", at: right },
      ],
      bar: s.bestWindow
        ? { from: s.bestWindow[0], to: s.bestWindow[1], label: `best window [${s.bestWindow[0]}, ${s.bestWindow[1]}] · longest ${s.longest}` }
        : null,
    });
  },
}));
