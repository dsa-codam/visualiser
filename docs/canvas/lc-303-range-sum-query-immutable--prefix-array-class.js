/* Generated from problems/lc-303-range-sum-query-immutable/prefix-array-class/canvas.js */
VIZ.canvas.register("lc-303-range-sum-query-immutable/prefix-array-class", /* LC 303 · prefix array built in the constructor (design problem, ADR 033).
   Reads step.state = { nums, pre, built, i, left, right, answers, pre_roles } and step.roles for nums.
   A side panel lists the calls of this example (ctx.example.args.calls / args) with the answers so far.
   Draws only with VIZ helpers — no colours or sizes here. */
({
  build(ctx) {
    const a = ctx.example.args;
    const nums = a.args[0][0];
    ctx.canvas.innerHTML = "";
    const host = (title) => {
      ctx.canvas.insertAdjacentHTML("beforeend", `<h3>${title}</h3>`);
      const d = VIZ.el("div");
      ctx.canvas.append(d);
      return d;
    };
    const h1 = host("nums");
    const h2 = host("pre <small>(pre[k] = sum of the first k numbers)</small>");
    ctx.row1 = new VIZ.ArrayRow(h1, nums, { roles: ["back", "front"] });
    ctx.row2 = new VIZ.ArrayRow(h2, new Array(nums.length + 1).fill(0), { roles: [] });
    ctx.calls = ctx.extraPanel();
  },

  render(step, ctx) {
    const s = step.state;
    const q = s.left !== null;
    const cls1 = {};
    for (const [pos, role] of Object.entries(step.roles || {})) cls1[pos] = role;
    const cls2 = {};
    s.pre.forEach((v, pos) => { if (pos >= s.built) cls2[pos] = "zero"; });
    for (const [pos, role] of Object.entries(s.pre_roles || {})) cls2[pos] = role;
    ctx.row1.update({
      arr: s.nums,
      cls: cls1,
      bands: q ? [{ kind: "window", from: s.left, to: s.right, label: `sum = ${s.answers[s.answers.length - 1]}` }] : [],
      pointers: [
        { role: "back", label: "left", at: s.left },
        { role: "front", label: "right", at: s.right },
      ],
    });
    ctx.row2.update({
      arr: s.pre,
      cls: cls2,
      bands: q ? [{ kind: "window", from: s.left, to: s.right + 1, label: `pre[${s.right + 1}] − pre[${s.left}]` }] : [],
      pointers: [],
    });
    const a = ctx.example.args;
    const rows = a.calls.slice(1).map((name, k) => ({
      key: `${name}(${a.args[k + 1].join(", ")})`,
      value: k < s.answers.length ? String(s.answers[k]) : "—",
      mark: q && k === s.answers.length - 1 ? "hit" : "",
    }));
    VIZ.kvMap(ctx.calls, rows, "calls");
  },
}));
