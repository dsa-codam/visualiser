/* Generated from problems/lc-1652-defuse-the-bomb/sliding-window-fixed-circular/canvas.js */
VIZ.canvas.register("lc-1652-defuse-the-bomb/sliding-window-fixed-circular", /* LC 1652 · fixed-size sliding window on a circular array.
   Reads step.state = { code, result, k, left, right, window, total, written, newAt }
   and step.roles = { pos: "current" | "removed" } for the code row.
   window = [from, to]; from > to means the window wraps around the end.
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
    const h1 = host("code <small>(circular: after the last index comes 0)</small>");
    const h2 = host("result <small>(result[i] = sum of the window of code[i])</small>");
    ctx.row1 = new VIZ.ArrayRow(h1, a.code, { roles: ["back", "front"] });
    ctx.row2 = new VIZ.ArrayRow(h2, a.code.map(() => 0), { roles: [] });
  },

  render(step, ctx) {
    const s = step.state, roles = step.roles;
    const done = step.phase === "return";
    const cls1 = {}, cls2 = {};
    s.code.forEach((v, pos) => { if (roles[pos]) cls1[pos] = roles[pos]; });
    s.result.forEach((v, pos) => {
      if (done) cls2[pos] = "best";
      else if (pos === s.newAt) cls2[pos] = "new";
      else if (pos >= s.written) cls2[pos] = "zero";
    });
    const w = s.window;
    ctx.row1.update({
      arr: s.code,
      cls: cls1,
      bands: w ? [{ kind: "window", from: w[0], to: w[1], wrap: true, label: `window [${w[0]}, ${w[1]}] · total ${s.total}` }] : [],
      pointers: [
        { role: "back", label: "left", at: done ? null : s.left },
        { role: "front", label: "right", at: done ? null : s.right },
      ],
    });
    ctx.row2.update({ arr: s.result, cls: cls2, pointers: [] });
  },
}));
