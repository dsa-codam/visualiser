/* Generated from problems/lc-2483-minimum-penalty-for-a-shop/prefix-sum-running-penalty/canvas.js */
VIZ.canvas.register("lc-2483-minimum-penalty-for-a-shop/prefix-sum-running-penalty", /* LC 2483 · running penalty.
   Reads step.state = { arr, j, close, penalty, best, best_hour, tags } and step.roles = { pos: "current" }.
   close = the closing hour of this step: the window band covers the open hours [0, close − 1].
   The best band covers the open hours of best_hour. tags = hours that add 1 to the penalty
   (drawn as conflict cells with a "+1" badge). Draws only with VIZ.ArrayRow — no colours or sizes here. */
({
  build(ctx) {
    ctx.canvas.innerHTML = "<h3>customers <small>(band = open hours)</small></h3>";
    const d = VIZ.el("div");
    ctx.canvas.append(d);
    ctx.row = new VIZ.ArrayRow(d, ctx.example.args.customers.split(""), { roles: ["front"] });
  },

  render(step, ctx) {
    const s = step.state;
    const cls = {};
    for (const pos of Object.keys(s.tags)) cls[pos] = "conflict";
    for (const [pos, role] of Object.entries(step.roles || {})) cls[pos] = role;
    const bands = [];
    if (s.close !== null && s.close > 0) {
      bands.push({ kind: "window", from: 0, to: s.close - 1, label: `close at ${s.close} · penalty ${s.penalty}` });
    }
    if (s.best_hour !== null && s.best_hour > 0) {
      bands.push({ kind: "best", from: 0, to: s.best_hour - 1, label: `best: close at ${s.best_hour}` });
    }
    ctx.row.update({ arr: s.arr, cls, tags: s.tags, bands, pointers: [{ role: "front", label: "j", at: s.j }] });
  },
}));
