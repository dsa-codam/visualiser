/* Generated from problems/lc-1413-minimum-value-to-get-positive-step-by-step-sum/prefix-sum-running/canvas.js */
VIZ.canvas.register("lc-1413-minimum-value-to-get-positive-step-by-step-sum/prefix-sum-running", /* LC 1413 · running prefix sum + lowest point.
   Reads step.state = { nums, i, total, lowest, start_value } and step.roles = { pos: "current" }.
   The window band covers nums[0..i], the numbers inside total.
   Draws only with VIZ.ArrayRow — no colours or sizes here. */
({
  build(ctx) {
    ctx.canvas.innerHTML = "<h3>nums</h3>";
    const d = VIZ.el("div");
    ctx.canvas.append(d);
    ctx.row = new VIZ.ArrayRow(d, ctx.example.args.nums, { roles: ["front"] });
  },

  render(step, ctx) {
    const s = step.state;
    const cls = {};
    for (const [pos, role] of Object.entries(step.roles || {})) cls[pos] = role;
    ctx.row.update({
      arr: s.nums,
      cls,
      bands: s.i === null ? [] : [{ kind: "window", from: 0, to: s.i, label: `total = ${s.total} · lowest = ${s.lowest}` }],
      pointers: [{ role: "front", label: "i", at: s.i }],
    });
  },
}));
