/* Generated from problems/lc-3427-sum-of-variable-length-subarrays/prefix-sum-array/canvas.js */
VIZ.canvas.register("lc-3427-sum-of-variable-length-subarrays/prefix-sum-array", /* LC 3427 · prefix array with a leading 0.
   Reads step.state = { nums, pre, built, i, phase, start, subarray_sum, total, pre_roles }
   and step.roles = { pos: "current" } for nums. pre slots ≥ built are not written yet (dashed).
   Query steps: the window band covers nums[start..i] and pre[start..i + 1] (the two ends are the cells used).
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
    const h2 = host("pre <small>(pre[k] = sum of the first k numbers)</small>");
    ctx.row1 = new VIZ.ArrayRow(h1, a.nums, { roles: ["back", "front"] });
    ctx.row2 = new VIZ.ArrayRow(h2, new Array(a.nums.length + 1).fill(0), { roles: [] });
  },

  render(step, ctx) {
    const s = step.state;
    const q = s.phase === "query" && s.i !== null;
    const cls1 = {};
    for (const [pos, role] of Object.entries(step.roles || {})) cls1[pos] = role;
    const cls2 = {};
    s.pre.forEach((v, pos) => { if (pos >= s.built) cls2[pos] = "zero"; });
    for (const [pos, role] of Object.entries(s.pre_roles || {})) cls2[pos] = role;
    ctx.row1.update({
      arr: s.nums,
      cls: cls1,
      bands: q ? [{ kind: "window", from: s.start, to: s.i, label: `sum = ${s.subarray_sum}` }] : [],
      pointers: [
        { role: "back", label: "start", at: q ? s.start : null },
        { role: "front", label: "i", at: s.i },
      ],
    });
    ctx.row2.update({
      arr: s.pre,
      cls: cls2,
      bands: q ? [{ kind: "window", from: s.start, to: s.i + 1, label: `pre[${s.i + 1}] − pre[${s.start}]` }] : [],
      pointers: [],
    });
  },
}));
