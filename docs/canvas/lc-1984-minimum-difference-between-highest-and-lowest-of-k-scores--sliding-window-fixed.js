/* Generated from problems/lc-1984-minimum-difference-between-highest-and-lowest-of-k-scores/sliding-window-fixed/canvas.js */
VIZ.canvas.register("lc-1984-minimum-difference-between-highest-and-lowest-of-k-scores/sliding-window-fixed", /* LC 1984 · sort + fixed-size sliding window.
   Reads step.state = { arr, ids, k, left, right, window, diff, smallest, bestWindow }
   and step.roles = { pos: "current" | "removed" }.
   The first step shows nums before sorting; ids make the cells slide into sorted order.
   On a slide step the band has k − 1 cells, so its label leaves out diff (that was the old window's).
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
      cls[i] = c.join(" ");
    });
    const w = s.window;
    const label = w ? `window [${w[0]}, ${w[1]}]` + (s.diff === null || step.phase === "slide" ? "" : ` · diff ${s.diff}`) : "";
    ctx.row.update({
      arr: s.arr,
      ids: s.ids,
      cls,
      bands: w ? [{ kind: "window", from: w[0], to: w[1], label }] : [],
      pointers: [
        { role: "back", label: "left", at: right === null ? null : s.left },
        { role: "front", label: "right", at: right },
      ],
      bar: s.bestWindow
        ? { from: s.bestWindow[0], to: s.bestWindow[1], label: `best window [${s.bestWindow[0]}, ${s.bestWindow[1]}] · smallest ${s.smallest}` }
        : null,
    });
  },
}));
