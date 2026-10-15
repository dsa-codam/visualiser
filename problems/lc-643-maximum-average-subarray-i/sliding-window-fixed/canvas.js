/* LC 643 · fixed-size sliding window.
   Reads step.state = { arr, k, left, right, window, total, largest, bestWindow }
   and step.roles = { pos: "current" | "removed" }.
   Draws only with VIZ.ArrayRow — no colours or sizes here. */
({
  build(ctx) {
    ctx.row = new VIZ.ArrayRow(ctx.canvas, ctx.example.args.nums, { roles: ["back", "front"], bar: true });
  },

  render(step, ctx) {
    const s = step.state, roles = step.roles, left = s.left, right = s.right;
    const cls = {};
    s.arr.forEach((v, i) => {
      const c = [], role = roles[i];
      if (role === "removed") c.push("removed");
      else if (right !== null && i < left) c.push("out");
      if (step.phase === "return" && s.bestWindow && i >= s.bestWindow[0] && i <= s.bestWindow[1]) c.push("best");
      if (role === "current") c.push("current");
      cls[i] = c.join(" ");
    });
    const w = s.window;
    ctx.row.update({
      arr: s.arr,
      cls,
      bands: w ? [{ kind: "window", from: w[0], to: w[1], label: `window [${w[0]}, ${w[1]}] · total ${s.total}` }] : [],
      pointers: [
        { role: "back", label: "left", at: right === null ? null : left },
        { role: "front", label: "right", at: right },
      ],
      bar: s.bestWindow
        ? { from: s.bestWindow[0], to: s.bestWindow[1], label: `best window [${s.bestWindow[0]}, ${s.bestWindow[1]}] · largest ${s.largest}` }
        : null,
    });
  },
})
