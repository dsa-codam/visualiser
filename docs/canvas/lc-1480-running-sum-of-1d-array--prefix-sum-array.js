/* Generated from problems/lc-1480-running-sum-of-1d-array/prefix-sum-array/canvas.js */
VIZ.canvas.register("lc-1480-running-sum-of-1d-array/prefix-sum-array", /* LC 1480 · prefix sum into a new result array.
   Reads step.state = { nums, result, i, written, band, label, r1, r2 }:
   result slots < written are filled; band = [i - 1, i] (the two slots in the formula);
   r1 / r2 = { pos: "current" | "new" } for the nums row and the result row.
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
    const h2 = host("result <small>(result[i] = nums[0] + … + nums[i])</small>");
    ctx.row1 = new VIZ.ArrayRow(h1, a.nums, { roles: ["front"] });
    ctx.row2 = new VIZ.ArrayRow(h2, a.nums.map(() => 0), { roles: ["front"] });
  },

  render(step, ctx) {
    const s = step.state;
    const done = step.phase === "return";
    const cls1 = {}, cls2 = {};
    s.nums.forEach((v, pos) => {
      cls1[pos] = s.r1[pos] || "";
    });
    s.result.forEach((v, pos) => {
      const c = [pos < s.written ? "" : "zero"];
      if (done) c.push("best");
      if (s.r2[pos]) c.push(s.r2[pos]);
      cls2[pos] = c.join(" ").trim();
    });
    const pointer = [{ role: "front", label: "i", at: s.i }];
    ctx.row1.update({ arr: s.nums, cls: cls1, pointers: pointer });
    ctx.row2.update({
      arr: s.result,
      cls: cls2,
      bands: s.band ? [{ kind: "window", from: s.band[0], to: s.band[1], label: s.label }] : [],
      pointers: pointer,
    });
  },
}));
