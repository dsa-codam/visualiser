/* LC 2760 · sliding window that restarts at a break.
   Reads step.state = { arr, left, right, window, threshold, longest, bestWindow, tags }
   and step.roles = { pos: "current" | "conflict" | "dup" }.
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
      if (right !== null && i < s.left && !role) c.push("out");
      if (step.phase === "return" && s.bestWindow && i >= s.bestWindow[0] && i <= s.bestWindow[1]) c.push("best");
      if (role) c.push(role);
      cls[i] = c.join(" ");
    });
    const w = s.window;
    ctx.row.update({
      arr: s.arr,
      cls,
      tags: s.tags,
      bands: w ? [{ kind: "window", from: w[0], to: w[1], label: `window [${w[0]}, ${w[1]}] · length ${w[1] - w[0] + 1}` }] : [],
      pointers: [
        { role: "back", label: "left", at: right === null || s.left >= s.arr.length ? null : s.left },
        { role: "front", label: "right", at: right },
      ],
      bar: s.bestWindow
        ? { from: s.bestWindow[0], to: s.bestWindow[1], label: `best window [${s.bestWindow[0]}, ${s.bestWindow[1]}] · longest ${s.longest}` }
        : null,
    });
  },
})
