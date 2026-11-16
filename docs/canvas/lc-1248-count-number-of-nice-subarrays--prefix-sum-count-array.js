/* Generated from problems/lc-1248-count-number-of-nice-subarrays/prefix-sum-count-array/canvas.js */
VIZ.canvas.register("lc-1248-count-number-of-nice-subarrays/prefix-sum-count-array", /* LC 1248 · prefix count of odd numbers + counting array.
   Reads step.state = { nums, cnt, i, odd, k, nice, look, cnt_roles } and step.roles = { pos: "current" } for nums.
   nums row: the window band covers the prefix nums[0..i]. cnt row: index = number of odd values,
   cnt_roles marks the slot looked up (current) or just increased (new).
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
    const h2 = host("cnt <small>(cnt[p] = prefixes with p odd numbers)</small>");
    ctx.row1 = new VIZ.ArrayRow(h1, a.nums, { roles: ["front"] });
    ctx.row2 = new VIZ.ArrayRow(h2, new Array(a.nums.length + 1).fill(0), { roles: [] });
  },

  render(step, ctx) {
    const s = step.state;
    const cls1 = {};
    for (const [pos, role] of Object.entries(step.roles || {})) cls1[pos] = role;
    const cls2 = {};
    for (const [pos, role] of Object.entries(s.cnt_roles || {})) cls2[pos] = role;
    ctx.row1.update({
      arr: s.nums,
      cls: cls1,
      bands: s.i === null ? [] : [{ kind: "window", from: 0, to: s.i, label: `odd = ${s.odd}` }],
      pointers: [{ role: "front", label: "i", at: s.i }],
    });
    ctx.row2.update({
      arr: s.cnt,
      cls: cls2,
      bands: s.look === null ? [] : [{ kind: "window", from: s.look, to: s.look, label: `cnt[${s.look}] = ${s.cnt[s.look]}` }],
      pointers: [],
    });
  },
}));
