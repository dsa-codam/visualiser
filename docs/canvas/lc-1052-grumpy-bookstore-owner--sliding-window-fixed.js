/* Generated from problems/lc-1052-grumpy-bookstore-owner/sliding-window-fixed/canvas.js */
VIZ.canvas.register("lc-1052-grumpy-bookstore-owner/sliding-window-fixed", /* LC 1052 · fixed-size sliding window over two arrays of the same length.
   Reads step.state = { customers, grumpy, minutes, i, scanned, left, right, window, satisfied, extra, max_extra, bestWindow }
   and step.roles = { pos: "current" | "removed" }.
   customers row: calm minutes already counted in satisfied get a ✓ (done); window, pointers and best bar.
   On the last step only the best window is green, so the two greens do not mix.
   grumpy row: the same window band, so a reader sees which 0s and 1s are inside it.
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
    const h1 = host("customers <small>(✓ = calm minute, counted in satisfied)</small>");
    const h2 = host("grumpy <small>(1 = grumpy: only the technique makes these customers happy)</small>");
    ctx.row1 = new VIZ.ArrayRow(h1, a.customers, { roles: ["back", "front"], bar: true });
    ctx.row2 = new VIZ.ArrayRow(h2, a.grumpy, { roles: [] });
  },

  render(step, ctx) {
    const s = step.state, roles = step.roles, right = s.right;
    const done = step.phase === "return";
    const inBest = (i) => done && s.bestWindow && i >= s.bestWindow[0] && i <= s.bestWindow[1];
    const cls1 = {}, cls2 = {};
    s.customers.forEach((v, i) => {
      const c = [], role = roles[i];
      if (role === "removed") c.push("removed");
      else if (right !== null && s.left !== null && i < s.left) c.push("out");
      if (inBest(i)) c.push("best");
      else if (!done && s.grumpy[i] === 0 && i < s.scanned) c.push("done");
      if (role === "current") c.push("current");
      cls1[i] = c.join(" ");
      cls2[i] = role === "current" ? "current" : inBest(i) ? "best" : "";
    });
    const w = s.window;
    ctx.row1.update({
      arr: s.customers,
      cls: cls1,
      bands: w ? [{ kind: "window", from: w[0], to: w[1], label: `window [${w[0]}, ${w[1]}] · extra ${s.extra}` }] : [],
      pointers: [
        { role: "back", label: "left", at: right === null ? null : s.left },
        { role: "front", label: "right", at: right },
      ],
      bar: s.bestWindow
        ? { from: s.bestWindow[0], to: s.bestWindow[1], label: `best window [${s.bestWindow[0]}, ${s.bestWindow[1]}] · max_extra ${s.max_extra}` }
        : null,
    });
    ctx.row2.update({
      arr: s.grumpy,
      cls: cls2,
      bands: w ? [{ kind: "window", from: w[0], to: w[1], label: "" }] : [],
    });
  },
}));
