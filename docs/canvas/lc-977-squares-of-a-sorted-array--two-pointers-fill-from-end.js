/* Generated from problems/lc-977-squares-of-a-sorted-array/two-pointers-fill-from-end/canvas.js */
VIZ.canvas.register("lc-977-squares-of-a-sorted-array/two-pointers-fill-from-end", /* LC 977 · two pointers, filling the result from the end.
   Reads step.state = { nums, result, left, right, write, placed, r1, r2 }:
   result slots >= placed are final; r1 / r2 = { pos: "current" | "new" } per row.
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
    const h2 = host("result <small>(squares, filled from the back)</small>");
    ctx.row1 = new VIZ.ArrayRow(h1, a.nums, { roles: ["back", "front"] });
    ctx.row2 = new VIZ.ArrayRow(h2, a.nums.map(() => 0), { roles: ["back"] });
  },

  render(step, ctx) {
    const s = step.state, n = s.nums.length;
    const finished = step.phase === "return" || step.phase === "stop";
    const cls1 = {}, cls2 = {};
    s.nums.forEach((v, pos) => {
      const c = [];
      if (pos < s.left || pos > s.right) c.push("out");
      if (s.r1[pos]) c.push(s.r1[pos]);
      cls1[pos] = c.join(" ");
    });
    s.result.forEach((v, pos) => {
      const c = [pos >= s.placed ? "done" : "zero"];
      if (s.r2[pos]) c.push(s.r2[pos]);
      cls2[pos] = c.join(" ");
    });
    const bands1 = s.left <= s.right ? [{ kind: "window", from: s.left, to: s.right, label: "waiting" }] : [];
    const bands2 = s.placed <= n - 1 ? [{ kind: "best", from: s.placed, to: n - 1, label: "placed" }] : [];
    ctx.row1.update({
      arr: s.nums,
      cls: cls1,
      bands: bands1,
      pointers: [
        { role: "back", label: "left", at: finished ? null : s.left },
        { role: "front", label: "right", at: finished ? null : s.right },
      ],
    });
    ctx.row2.update({
      arr: s.result,
      cls: cls2,
      bands: bands2,
      pointers: [{ role: "back", label: "write", at: finished || s.write < 0 ? null : s.write }],
    });
  },
}));
