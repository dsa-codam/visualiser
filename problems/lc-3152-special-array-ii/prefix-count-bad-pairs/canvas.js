/* LC 3152 · prefix count of bad pairs.
   Reads step.state = { nums, pre, built, queries (strings "[a,b]"), answer (strings), i, j, left, right, phase, band, pre_roles }
   and step.roles = { pos: "current" } for nums. band = { from, to, bad, label } on nums: a pair while pre is built,
   the query range later; bad: true draws it red. Draws only with VIZ.ArrayRow — no colours or sizes here. */
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
    const h2 = host("pre <small>(pre[i] = bad pairs inside nums[0..i])</small>");
    const h3 = host("queries → answer");
    ctx.row1 = new VIZ.ArrayRow(h1, a.nums, { roles: ["back", "front"] });
    ctx.row2 = new VIZ.ArrayRow(h2, a.nums.map(() => 0), { roles: [] });
    ctx.qhost = h3;
  },

  render(step, ctx) {
    const s = step.state;
    const cls1 = {};
    for (const [pos, role] of Object.entries(step.roles || {})) cls1[pos] = role;
    const cls2 = {};
    s.pre.forEach((v, pos) => { if (pos >= s.built) cls2[pos] = "zero"; });
    for (const [pos, role] of Object.entries(s.pre_roles || {})) cls2[pos] = role;
    const b = s.band;
    ctx.row1.update({
      arr: s.nums,
      cls: cls1,
      bands: b ? [{ kind: "window", from: b.from, to: b.to, bad: b.bad, label: b.label }] : [],
      pointers: [
        { role: "back", label: "left", at: s.left },
        { role: "front", label: "right", at: s.right },
      ],
    });
    ctx.row2.update({ arr: s.pre, cls: cls2, pointers: [] });
    // queries and their answers as one row of "[a,b] → true" cells
    const cells = s.queries.map((q, k) => (k < s.answer.length ? `${q} ${s.answer[k] === "true" ? "✓" : "✗"}` : q));
    const key = cells.length;
    if (!ctx.row3 || ctx.row3Len !== key) {
      ctx.qhost.innerHTML = "";
      ctx.row3 = new VIZ.ArrayRow(ctx.qhost, cells, { roles: [] });
      ctx.row3Len = key;
    }
    const cls3 = {};
    cells.forEach((c, k) => {
      if (k < s.answer.length) cls3[k] = s.answer[k] === "true" ? "best" : "conflict";
      else cls3[k] = "zero";
    });
    if (s.phase === "query" && s.answer.length) cls3[s.answer.length - 1] += " current";
    ctx.row3.update({ arr: cells, cls: cls3, pointers: [] });
  },
})
