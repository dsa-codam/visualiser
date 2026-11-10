/* Generated from problems/lc-424-longest-repeating-character-replacement/sliding-window-count-array/canvas.js */
VIZ.canvas.register("lc-424-longest-repeating-character-replacement/sliding-window-count-array", /* LC 424 · sliding window + counting array.
   Reads step.state = { arr, k, left, right, window, bad, replace, rows, length, topLetter, topCount,
   changes, longest, bestWindow } and step.roles = { pos: "current" | "removed" }.
   A bad window (changes > k) gets the red band; its red cells are the letters to change (replace).
   Draws only with VIZ.ArrayRow and VIZ.kvMap — no colours or sizes here. */
({
  build(ctx) {
    ctx.row = new VIZ.ArrayRow(ctx.canvas, ctx.example.args.s.split(""), { roles: ["back", "front"], bar: true });
    ctx.mapPanel = ctx.extraPanel();
  },

  render(step, ctx) {
    const s = step.state, roles = step.roles, left = s.left, right = s.right;
    const cls = {};
    s.arr.forEach((v, i) => {
      const c = [], role = roles[i];
      if (role === "removed") c.push("removed");
      else if (right !== null && i < left) c.push("out");
      if (step.phase === "return" && s.bestWindow && i >= s.bestWindow[0] && i <= s.bestWindow[1]) c.push("best");
      if (role === "current") c.push("current");
      if (s.replace.includes(i)) c.push("conflict");
      cls[i] = c.join(" ");
    });
    const w = s.window;
    // every step with a window comes after the four values are computed, so the label is always the full check
    const label = w
      ? `window [${w[0]}, ${w[1]}] · length ${s.length} · top ${s.topLetter}×${s.topCount} · changes ${s.length} − ${s.topCount} = ${s.changes}` +
        (s.bad ? ` > k = ${s.k} ✗` : ` ≤ k = ${s.k}`)
      : "";
    ctx.row.update({
      arr: s.arr,
      cls,
      bands: w ? [{ kind: "window", bad: s.bad, from: w[0], to: w[1], label }] : [],
      pointers: [
        { role: "back", label: "left", at: right === null ? null : left },
        { role: "front", label: "right", at: right },
      ],
      bar: s.bestWindow
        ? { from: s.bestWindow[0], to: s.bestWindow[1], label: `best window [${s.bestWindow[0]}, ${s.bestWindow[1]}] · longest ${s.longest}` }
        : null,
    });
    VIZ.kvMap(ctx.mapPanel, s.rows, `count <small>(letter → times in window, k = ${s.k})</small>`);
  },
}));
