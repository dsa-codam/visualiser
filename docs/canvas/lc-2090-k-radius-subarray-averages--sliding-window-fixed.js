/* Generated from problems/lc-2090-k-radius-subarray-averages/sliding-window-fixed/canvas.js */
VIZ.canvas.register("lc-2090-k-radius-subarray-averages/sliding-window-fixed", /* LC 2090 · fixed-size sliding window, answer written at the window's centre.
   Reads step.state = { arr, avgs, k, left, right, window, total, center, written, newAt }
   and step.roles = { pos: "current" | "removed" } for the nums row.
   On the first full window (anchor "first") a measure annotation shows the radius:
   k + 1 + k = 2k + 1. Draws only with VIZ.ArrayRow — no colours or sizes here. */
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
    const h2 = host("avgs <small>(avgs[center] = total / (2k + 1), whole part only)</small>");
    ctx.row1 = new VIZ.ArrayRow(h1, a.nums, { roles: ["back", "front", "mid"], measure: true });
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
        { role: "mid", label: "center", at: done ? null : s.center },
      ],
      measure: step.anchor === "first"
        ? { from: w[0], to: w[1], origin: "center", at: s.center, role: "mid",
            labels: [`k = ${s.k}`, `k = ${s.k}`], text: { left: `${s.k} +`, center: "1", right: `+ ${s.k} = ${2 * s.k + 1}` } }
        : null,
    });
    ctx.row2.update({ arr: s.avgs, cls: cls2, pointers: [] });
  },
}));
