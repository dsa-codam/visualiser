/* LC 2090 · fixed-size sliding window, answer written at the window's centre.
   Reads step.state = { arr, avgs, k, left, right, window, total, center, written, newAt }
   and step.roles = { pos: "current" | "removed" } for the nums row.
   Draws only with VIZ.ArrayRow — no colours or sizes here. */
({
  build(ctx) {
    const a = ctx.example.args;
    ctx.canvas.innerHTML = "";
    const host = (title) => {
      ctx.canvas.insertAdjacentHTML("beforeend", `<h3>${title}</h3>`);
      const d = VIZ.el("div");
      ctx.canvas.append(d);
      return d;
    };
    const h1 = host("nums");
    const h2 = host("avgs <small>(avgs[center] = window average)</small>");
    ctx.row1 = new VIZ.ArrayRow(h1, a.nums, { roles: ["back", "front"] });
    ctx.row2 = new VIZ.ArrayRow(h2, a.nums.map(() => -1), { roles: [] });
  },

  render(step, ctx) {
    const s = step.state, roles = step.roles, right = s.right;
    const done = step.phase === "return";
    const cls1 = {}, cls2 = {};
    s.arr.forEach((v, i) => {
      const role = roles[i];
      if (role) cls1[i] = role;
      else if (right !== null && i < s.left) cls1[i] = "out";
    });
    s.avgs.forEach((v, i) => {
      if (done) cls2[i] = "best";
      else if (i === s.newAt) cls2[i] = "new";
      else if (!s.written.includes(i)) cls2[i] = "zero";
    });
    const w = s.window;
    ctx.row1.update({
      arr: s.arr,
      cls: cls1,
      bands: w ? [{ kind: "window", from: w[0], to: w[1], label: `window [${w[0]}, ${w[1]}] · total ${s.total}` }] : [],
      pointers: [
        { role: "back", label: "left", at: right === null ? null : s.left },
        { role: "front", label: "right", at: right },
      ],
    });
    ctx.row2.update({ arr: s.avgs, cls: cls2, pointers: [] });
  },
})
