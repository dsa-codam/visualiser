/* LC 724 · total + running left sum.
   Reads step.state = { nums, i, phase: "total" | "scan" | "done", total, left, right }
   and step.roles = { pos: "current" | "best" }.
   First pass: the window band covers nums[0..i] (the numbers in total).
   Second pass: the window band covers the left side nums[0..i − 1]; the label also shows right.
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
    let bands = [];
    if (s.phase === "total" && s.i !== null) {
      bands = [{ kind: "window", from: 0, to: s.i, label: `total = ${s.total}` }];
    } else if (s.phase === "scan" && s.i !== null) {
      const sides = `left = ${s.left} · right = ${s.right === null ? "—" : s.right}`;
      // after "left += nums[i]" the left side already includes i
      const to = step.anchor === "move" ? s.i : s.i - 1;
      bands = to >= 0 ? [{ kind: "window", from: 0, to, label: sides }] : [];
    }
    ctx.row.update({ arr: s.nums, cls, bands, pointers: [{ role: "front", label: "i", at: s.i }] });
  },
})
