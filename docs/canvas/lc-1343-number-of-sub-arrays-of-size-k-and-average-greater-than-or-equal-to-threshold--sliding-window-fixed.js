/* Generated from problems/lc-1343-number-of-sub-arrays-of-size-k-and-average-greater-than-or-equal-to-threshold/sliding-window-fixed/canvas.js */
VIZ.canvas.register("lc-1343-number-of-sub-arrays-of-size-k-and-average-greater-than-or-equal-to-threshold/sliding-window-fixed", /* LC 1343 · fixed-size sliding window.
   Reads step.state = { arr, k, left, right, window, total, min_sum, count, passed }
   and step.roles = { pos: "current" | "removed" }.
   A window that passes the test is drawn with the "best" band.
   Draws only with VIZ.ArrayRow — no colours or sizes here. */
({
  build(ctx) {
    ctx.row = new VIZ.ArrayRow(ctx.canvas, ctx.example.args.arr, { roles: ["back", "front"] });
  },

  render(step, ctx) {
    const s = step.state, roles = step.roles, left = s.left, right = s.right;
    const cls = {};
    s.arr.forEach((v, i) => {
      const c = [], role = roles[i];
      if (role === "removed") c.push("removed");
      else if (right !== null && i < left) c.push("out");
      if (role === "current") c.push("current");
      cls[i] = c.join(" ");
    });
    const w = s.window;
    const bands = [];
    if (w && s.passed) bands.push({ kind: "best", from: w[0], to: w[1], label: `total ${s.total} ≥ ${s.min_sum} · counted` });
    else if (w) bands.push({ kind: "window", from: w[0], to: w[1], label: `window [${w[0]}, ${w[1]}] · total ${s.total}` });
    ctx.row.update({
      arr: s.arr,
      cls,
      bands,
      pointers: [
        { role: "back", label: "left", at: right === null ? null : left },
        { role: "front", label: "right", at: right },
      ],
    });
  },
}));
