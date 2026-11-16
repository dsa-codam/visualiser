/* LC 2389 · sort + prefix array + binary search.
   Reads step.state = { nums, pre, built, queries, answer, answered, i, j, lo, mid, hi, phase, pre_roles }
   and step.roles = { pos: "current" } for nums (while pre is built).
   Rows: nums (sorted), pre (lo / mid / hi and the lo..hi band), queries (j), answer (written slots).
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
    const h1 = host("nums <small>(sorted)</small>");
    const h2 = host("pre <small>(pre[c] = sum of the c smallest numbers)</small>");
    const h3 = host("queries");
    const h4 = host("answer");
    ctx.row1 = new VIZ.ArrayRow(h1, a.nums, { roles: ["front"] });
    ctx.row2 = new VIZ.ArrayRow(h2, new Array(a.nums.length + 1).fill(0), { roles: ["back", "front", "mid"] });
    ctx.row3 = new VIZ.ArrayRow(h3, a.queries, { roles: ["front"] });
    ctx.row4 = new VIZ.ArrayRow(h4, a.queries.map(() => 0), { roles: [] });
  },

  render(step, ctx) {
    const s = step.state;
    const done = s.phase === "done";
    const cls1 = {};
    for (const [pos, role] of Object.entries(step.roles || {})) cls1[pos] = role;
    const cls2 = {};
    s.pre.forEach((v, pos) => { if (pos >= s.built) cls2[pos] = "zero"; });
    for (const [pos, role] of Object.entries(s.pre_roles || {})) cls2[pos] = role;
    const searching = s.lo !== null && s.hi !== null && s.lo <= s.hi;
    ctx.row1.update({ arr: s.nums, cls: cls1, pointers: [{ role: "front", label: "i", at: s.i }] });
    ctx.row2.update({
      arr: s.pre,
      cls: cls2,
      bands: searching ? [{ kind: "window", from: s.lo, to: s.hi, label: `counts ${s.lo}..${s.hi}` }] : [],
      pointers: [
        { role: "back", label: "lo", at: s.lo !== null && s.lo <= s.pre.length - 1 ? s.lo : null },
        { role: "front", label: "hi", at: s.hi !== null && s.hi >= 0 ? s.hi : null },
        { role: "mid", label: "mid", at: s.mid },
      ],
    });
    ctx.row3.update({ arr: s.queries, cls: s.j !== null ? { [s.j]: "current" } : {}, pointers: [{ role: "front", label: "j", at: s.j }] });
    const cls4 = {};
    s.answer.forEach((v, pos) => { cls4[pos] = done ? "best" : pos < s.answered ? "" : "zero"; });
    ctx.row4.update({ arr: s.answer, cls: cls4, pointers: [] });
  },
})
