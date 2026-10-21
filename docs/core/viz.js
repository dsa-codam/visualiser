/* =====================================================================
   viz.js — shared engine for every visualisation page.
   - Components: ArrayRow, vars, countMap, kvMap, stack, queue, legend
   - Page shell: VIZ.mount(PAGE) builds the whole page from data
   - Canvas plug-ins: VIZ.canvas.register(id, { build, render })
   A page never re-implements anything in this file. If a page needs
   something new, add it here (after the user approves it) and show it
   in gallery.html.
   ===================================================================== */
(function () {
  "use strict";
  const VIZ = (window.VIZ = window.VIZ || {});
  VIZ.schemaVersion = 1;

  // ---------- small helpers ----------
  const esc = (s) => String(s).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;");
  const el = (tag, cls, html) => {
    const e = document.createElement(tag);
    if (cls) e.className = cls;
    if (html !== undefined) e.innerHTML = html;
    return e;
  };
  const cssNum = (name, fallback) => {
    const v = parseFloat(getComputedStyle(document.documentElement).getPropertyValue(name));
    return Number.isFinite(v) ? v : fallback;
  };
  VIZ.esc = esc;
  VIZ.el = el;

  // =====================================================================
  // ArrayRow — one row of array cells with indices, pointers, bands,
  // a swap arc and an optional "best" bar underneath.
  // Cells are keyed by identity (ids) so a swap slides the cells.
  // =====================================================================
  const ROLE_ROW = { back: 0, front: 1, mid: 2 };

  class ArrayRow {
    /**
     * @param host     element to draw into (its width decides the cell size)
     * @param values   initial values (length n, 0..20)
     * @param opts     { roles: ["back","front"], bar: true|false, measure: true|false, minWidth }
     *                 measure: reserve a lane for update({ measure }) on every step, so rows never jump
     */
    constructor(host, values, opts = {}) {
      this.host = host;
      this.values = values.slice();
      this.roles = opts.roles || ["back", "front"];
      this.hasBar = !!opts.bar;
      this.hasMeasure = !!opts.measure;
      this.build();
    }

    build() {
      const n = Math.max(1, this.values.length);
      const pmin = cssNum("--cell-pitch-min", 30), pmax = cssNum("--cell-pitch-max", 60);
      const avail = Math.max(120, this.host.clientWidth - 34);
      const pitch = Math.max(pmin, Math.min(pmax, Math.floor(avail / n)));
      const size = pitch - 6;
      this.pitch = pitch;
      this.size = size;
      // top to bottom: band labels · measure lane (optional) · swap arc · indices · cells · pointers · best bar
      const lane = this.hasMeasure ? cssNum("--measure-lane", 44) : 0;
      const idxTop = 20 + lane;
      const cellTop = 40 + lane;
      const ptrTop = cellTop + size + 6;
      const rows = this.roles.length;
      const barTop = ptrTop + rows * 26 + 8;
      this.geo = { cellTop, idxTop, ptrTop, barTop, laneTop: 16 };

      const track = el("div", "ar-track");
      track.style.width = n * pitch + "px";
      track.style.height = (this.hasBar ? barTop + 28 : ptrTop + rows * 26) + "px";
      track.style.fontSize = Math.max(13, Math.min(18, size * 0.38)) + "px";
      track.classList.toggle("small", pitch < 44);
      this.track = track;

      this.bandEls = {};
      for (const kind of ["best", "gap", "window"]) {
        // band2 is the second piece of a band that wraps around the end (circular arrays)
        const [b, b2] = [0, 1].map(() => {
          const e = el("div", "ar-band " + kind);
          e.style.top = cellTop - 5 + "px";
          e.style.height = size + 10 + "px";
          e.style.opacity = 0;
          return e;
        });
        const l = el("div", "ar-blabel " + kind);
        l.style.opacity = 0;
        track.append(b, b2, l);
        this.bandEls[kind] = { band: b, band2: b2, label: l };
      }
      this.arc = el("div", "ar-arc", "<span></span>");
      this.arc.style.top = 4 + lane + "px";
      this.arc.style.opacity = 0;
      track.append(this.arc);

      for (let i = 0; i < this.values.length; i++) {
        const ix = el("div", "ar-idx", String(i));
        ix.style.left = i * pitch + "px";
        ix.style.width = pitch + "px";
        ix.style.top = idxTop + "px";
        track.append(ix);
      }
      this.cells = this.values.map((v, id) => {
        const c = el("div", "ar-cell", esc(v));
        c.style.width = size + "px";
        c.style.height = size + "px";
        c.style.top = cellTop + "px";
        c.style.transform = `translateX(${id * pitch + 3}px)`;
        track.append(c);
        return c;
      });
      if (this.hasMeasure) {
        this.measureEl = el("div", "ar-measure");
        track.append(this.measureEl);
      }
      this.ptrEls = {};
      this.roles.forEach((role, row) => {
        const p = el("div", "ar-ptr " + role);
        p.style.width = pitch + "px";
        p.style.top = ptrTop + row * 26 + "px";
        p.style.opacity = 0;
        track.append(p);
        this.ptrEls[role] = p;
      });
      if (this.hasBar) {
        this.bar = el("div", "ar-bar");
        this.bar.style.top = barTop + "px";
        this.bar.style.opacity = 0;
        this.barLbl = el("div", "ar-barlbl");
        this.barLbl.style.top = barTop + 8 + "px";
        this.barLbl.style.opacity = 0;
        track.append(this.bar, this.barLbl);
      }
      this.host.innerHTML = "";
      this.host.append(track);
    }

    /**
     * @param s {
     *   arr:      current values by position
     *   ids:      identity at each position (optional; default = position)
     *   cls:      { pos: "current conflict ..." } extra classes per position
     *   tags:     { pos: ">k" } small red badge per position
     *   bands:    [{ kind: "window"|"best"|"gap", from, to, label, wrap }]  (to is inclusive)
     *             wrap: true and from > to → circular band, drawn as [from, n-1] and [0, to];
     *             without wrap, a band with to < from is empty and hidden
     *   arc:      { from, to, label } | null
     *   pointers: [{ role: "back"|"front"|"mid", label, at, dim }]
     *   bar:      { from, to, label } | null
     *   measure:  { from, to, origin: "center"|"start"|"end", at, role: "back"|"front"|"mid", labels: [..], text } | null
     *             needs { measure: true } in the constructor. "center": two arrows from the middle of cell at
     *             to the outer edges of from and to (an arrow is left out when it has no length);
     *             "start" / "end": one arrow across the range, pointing right / left.
     *             text: a string, or (origin "center" only) { left, center, right }: center exactly under
     *             cell at, left right-aligned to it, right left-aligned to it.
     * }
     */
    update(s) {
      const p = this.pitch;
      const arr = s.arr;
      const ids = s.ids || arr.map((_, i) => i);
      const cls = s.cls || {};
      const tags = s.tags || {};
      ids.forEach((id, pos) => {
        const c = this.cells[id];
        if (!c) return;
        c.style.transform = `translateX(${pos * p + 3}px)`;
        c.className = "ar-cell" + (cls[pos] ? " " + cls[pos] : "");
        c.innerHTML = esc(arr[pos]) + (tags[pos] ? `<span class="tag">${esc(tags[pos])}</span>` : "");
      });
      // bands
      const used = new Set();
      const place = (band, from, to, cut) => {
        band.style.left = from * p + "px";
        band.style.width = (to - from + 1) * p + "px";
        band.style.opacity = 1;
        band.classList.toggle("cut-end", cut === "end");
        band.classList.toggle("cut-start", cut === "start");
      };
      for (const b of s.bands || []) {
        const e = this.bandEls[b.kind];
        const wraps = b.wrap && b.to < b.from;
        if (!e || (b.to < b.from && !wraps)) continue;
        used.add(b.kind);
        let lFrom = b.from, lTo = b.to;
        if (wraps) {
          const last = arr.length - 1;
          place(e.band, b.from, last, "end");
          place(e.band2, 0, b.to, "start");
          // the label goes on the longer piece (the first one on a tie)
          if (b.to + 1 > last - b.from + 1) lFrom = 0;
          else lTo = last;
        } else {
          place(e.band, b.from, b.to, null);
          e.band2.style.opacity = 0;
        }
        e.label.textContent = b.label || "";
        e.label.style.left = ((lFrom + lTo + 1) * p) / 2 + "px";
        e.label.style.opacity = b.label ? 1 : 0;
      }
      for (const k of Object.keys(this.bandEls)) {
        if (!used.has(k)) {
          this.bandEls[k].band.style.opacity = 0;
          this.bandEls[k].band2.style.opacity = 0;
          this.bandEls[k].label.style.opacity = 0;
        }
      }
      // arc
      if (s.arc && s.arc.to > s.arc.from) {
        this.arc.style.left = (s.arc.from + 0.5) * p + "px";
        this.arc.style.width = (s.arc.to - s.arc.from) * p + "px";
        this.arc.querySelector("span").textContent = s.arc.label || "";
        this.arc.style.opacity = 1;
      } else this.arc.style.opacity = 0;
      // pointers
      const seen = new Set();
      for (const ptr of s.pointers || []) {
        const e = this.ptrEls[ptr.role];
        if (!e) continue;
        seen.add(ptr.role);
        const at = Math.max(0, Math.min(arr.length - 1, ptr.at == null ? 0 : ptr.at));
        e.innerHTML = "▲<br>" + esc(ptr.label);
        e.style.left = at * p + "px";
        e.style.opacity = ptr.at == null ? 0 : ptr.dim ? 0.35 : 1;
      }
      for (const r of Object.keys(this.ptrEls)) if (!seen.has(r)) this.ptrEls[r].style.opacity = 0;
      // measure
      if (this.hasMeasure) this.drawMeasure(s.measure || null);
      else if (s.measure) console.error("ArrayRow: update({ measure }) needs { measure: true } in the constructor");
      // bar
      if (this.hasBar) {
        if (s.bar) {
          this.bar.style.left = s.bar.from * p + 5 + "px";
          this.bar.style.width = (s.bar.to - s.bar.from + 1) * p - 10 + "px";
          this.bar.style.opacity = 1;
          this.barLbl.style.left = s.bar.from * p + 5 + "px";
          this.barLbl.textContent = s.bar.label || "";
          this.barLbl.style.opacity = 1;
        } else {
          this.bar.style.opacity = 0;
          this.barLbl.style.opacity = 0;
        }
      }
    }
  }
  /** Measure annotation: arrows over a cell range, a label per arrow, one text line under them. */
  ArrayRow.prototype.drawMeasure = function (m) {
    const box = this.measureEl;
    box.replaceChildren();
    box.className = "ar-measure";
    if (!m) return;
    const n = this.values.length;
    const split = m.text != null && typeof m.text === "object";
    const bad = !(Number.isInteger(m.from) && Number.isInteger(m.to)) || m.from > m.to || m.from < 0 || m.to >= n ||
      !["center", "start", "end"].includes(m.origin) ||
      (m.origin === "center" && !(Number.isInteger(m.at) && m.at >= m.from && m.at <= m.to)) ||
      (split && m.origin !== "center");
    if (bad) {
      console.error("ArrayRow measure: invalid input, nothing drawn", { from: m.from, to: m.to, origin: m.origin, at: m.at, n, text: m.text });
      return;
    }
    const p = this.pitch, top = this.geo.laneTop;
    const left = m.from * p + 3, right = m.to * p + 3 + this.size;  // outer edges of the range
    const labels = m.labels || [];
    if (m.role) box.classList.add(m.role);
    // all labels and text are set with textContent (never innerHTML), so no escaping is needed
    const str = (v) => (v == null ? "" : String(v));
    const span = (cls, text) => {
      const e = el("span", cls);
      e.textContent = text;
      return e;
    };
    const part = (cls, x, text) => {
      const e = el("div", cls);
      if (text != null) e.textContent = text;
      e.style.left = x + "px";
      e.style.top = top + "px";
      box.append(e);
      return e;
    };
    const arrow = (from, to, dir, label) => {
      const a = part("ar-measure-arrow " + dir, from);
      a.style.width = to - from + "px";
      if (label) part("ar-measure-label", (from + to) / 2, label);
    };
    let mid;
    if (m.origin === "center") {
      mid = m.at * p + p / 2;
      if (m.at > m.from) arrow(left, mid, "to-left", labels[0]);
      if (m.at < m.to) arrow(mid, right, "to-right", labels[1]);
      if (m.at > m.from || m.at < m.to) part("ar-measure-dot", mid);
    } else {
      mid = (left + right) / 2;
      arrow(left, right, m.origin === "start" ? "to-right" : "to-left", labels[0]);
    }
    if (split) {
      // { left, center, right }: center sits exactly under cell at; left ends just before it, right starts just after.
      // left and right hang off the edges of center, so their widths never move it.
      const e = part("ar-measure-text split", mid);
      const c = el("span", "center");
      // DOM order left · center · right, so the line reads in order for screen readers and copy-paste
      c.append(span("left", str(m.text.left)), str(m.text.center), span("right", str(m.text.right)));
      e.append(c);
    } else if (m.text) part("ar-measure-text", mid, str(m.text));
  };

  VIZ.ArrayRow = ArrayRow;

  // =====================================================================
  // Aux components
  // =====================================================================

  /** vars: [{ label, value, role?: "back"|"front"|"mid", flash?: bool }] */
  VIZ.vars = function (host, vars, flash) {
    host.innerHTML = "";
    const dl = el("dl", "vars");
    for (const v of vars) {
      const dt = el("dt", v.role || "", esc(v.label));
      const span = el("span", "", esc(v.value == null ? "—" : v.value));
      if (flash && v.flash) span.classList.add("flash");
      const dd = el("dd");
      dd.append(span);
      dl.append(dt, dd);
    }
    host.append(dl);
  };

  /** countMap: rows [{ key, count }], limit = max allowed count */
  VIZ.countMap = function (host, rows, limit, title) {
    host.innerHTML = title ? `<h3>${title}</h3>` : "";
    for (const r of rows) {
      let slots = "";
      const cap = Math.max(limit + 1, r.count);
      for (let i = 1; i <= cap; i++)
        slots += `<span class="cm-slot${i > limit ? " extra" : ""}${i <= r.count ? " on" : ""}"></span>`;
      const over = r.count > limit;
      host.insertAdjacentHTML(
        "beforeend",
        `<div class="cm-row${over ? " over" : ""}"><span class="cm-key mono">${esc(r.key)}</span>` +
          `<span class="cm-slots">${slots}</span><span class="cm-num mono">${r.count}${over ? " &gt; " + limit : ""}</span></div>`
      );
    }
  };

  /** kvMap: rows [{ key, value, mark?: "hit"|"new" }] */
  VIZ.kvMap = function (host, rows, title) {
    host.innerHTML = (title ? `<h3>${title}</h3>` : "") +
      `<table class="kv">${rows.map((r) => `<tr class="${r.mark || ""}"><td class="mono">${esc(r.key)}</td><td class="mono">${esc(r.value)}</td></tr>`).join("")}</table>`;
  };

  /** stack: items bottom→top [{ value, mark?: "new"|"gone" }] */
  VIZ.stack = function (host, items, title) {
    host.innerHTML = (title ? `<h3>${title}</h3>` : "") + `<div class="sq-lbl">top</div>`;
    const s = el("div", "stk");
    items.forEach((it, i) => s.append(el("div", (i === items.length - 1 ? "top " : "") + (it.mark || ""), esc(it.value))));
    host.append(s);
    host.insertAdjacentHTML("beforeend", `<div class="sq-lbl">bottom</div>`);
  };

  /** queue: items front→back [{ value, mark?: "new"|"gone" }] */
  VIZ.queue = function (host, items, title) {
    host.innerHTML = (title ? `<h3>${title}</h3>` : "") + `<div class="sq-lbl">front → back</div>`;
    const q = el("div", "que");
    items.forEach((it) => q.append(el("div", it.mark || "", esc(it.value))));
    host.append(q);
  };

  /** legend: [{ swatch, text, label? }] — swatch names are listed in design-system.md */
  VIZ.legend = function (host, items) {
    host.innerHTML = "";
    for (const it of items) {
      const d = el("div");
      let sw;
      if (it.swatch.startsWith("ptr-")) sw = el("span", "sw ptr " + it.swatch.slice(4), "▲");
      else sw = el("span", "sw " + it.swatch, it.label ? esc(it.label) : "");
      d.append(sw, document.createTextNode(it.text));
      host.append(d);
    }
  };

  /** code block: lines [{ src, comment }]. Line numbers come from CSS (.ln::before), so they are never copied. */
  VIZ.codeBlock = function (lines) {
    const pre = el("pre", "code");
    pre.innerHTML = lines
      .map((l, i) => `<span class="ln" data-n="${i + 1}">${esc(l.src)}${l.comment ? (l.src.trim() ? "  " : "") + '<span class="c">' + esc(l.comment) + "</span>" : ""}</span>`)
      .join("");
    return pre;
  };

  /** the text of a code block as shown, without line numbers */
  VIZ.codeText = (pre) => Array.from(pre.querySelectorAll(".ln"), (l) => l.textContent).join("\n") + "\n";

  /** copy a code block to the clipboard; the button shows "Copied" for a moment */
  VIZ.copyCode = function (pre, btn) {
    const text = VIZ.codeText(pre);
    const done = (ok) => {
      btn.textContent = ok ? "Copied" : "Copy failed";
      clearTimeout(btn._t);
      btn._t = setTimeout(() => (btn.textContent = "Copy"), 1500);
    };
    const fallback = () => {
      const ta = el("textarea");
      ta.value = text;
      ta.setAttribute("readonly", "");
      ta.style.position = "fixed";
      ta.style.opacity = 0;
      document.body.append(ta);
      ta.select();
      let ok = false;
      try { ok = document.execCommand("copy"); } catch (e) { ok = false; }
      ta.remove();
      done(ok);
    };
    if (navigator.clipboard && window.isSecureContext) navigator.clipboard.writeText(text).then(() => done(true), fallback);
    else fallback();
  };

  // =====================================================================
  // Canvas plug-in registry
  // =====================================================================
  const canvases = {};
  VIZ.canvas = {
    register(id, impl) { canvases[id] = impl; },
    get(id) { return canvases[id]; },
  };

  // =====================================================================
  // Page shell
  // =====================================================================
  const LANG_LABEL = { python: "Python3", cpp: "C++17", c: "C" };
  const LANG_ORDER = ["python", "cpp", "c"];
  // Play / Pause icons. U+FE0E asks for the text form, so Mac and iOS do not draw colour emoji.
  const PLAY = "\u25B6\uFE0E", PAUSE = "\u23F8\uFE0E";

  // Rule-of-thumb table: n → what complexity still fits in ~1 second.
  const CHEATSHEET = [
    { max: 10, fits: "O(n!)", ex: "all permutations" },
    { max: 20, fits: "O(2ⁿ)", ex: "all subsets, backtracking" },
    { max: 500, fits: "O(n³)", ex: "three nested loops" },
    { max: 5000, fits: "O(n²)", ex: "two nested loops, brute force on pairs" },
    { max: 1e6, fits: "O(n log n) or O(n)", ex: "sorting, two pointers, sliding window, hash map" },
    { max: Infinity, fits: "O(log n) or O(1)", ex: "binary search, maths" },
  ];

  function fmtN(n) {
    if (n === Infinity) return "more";
    if (n >= 1000 && Math.log10(n) % 1 === 0) return "10" + String(Math.log10(n)).split("").map((d) => "⁰¹²³⁴⁵⁶⁷⁸⁹"[d]).join("");
    return n.toLocaleString("en-GB");
  }

  VIZ.mount = function (PAGE, root) {
    root = root || document.getElementById("app");
    const P = PAGE.problem, S = PAGE.site || {};
    const st = { a: 0, e: 0, cur: 0, timer: null, lang: "python" };

    // ---------- layout (ADR 017) ----------
    // left column = animation, code under it; right column = variables, controls, caption.
    // Controls sit above the caption so the Next button never moves when a caption is longer.
    const SRC = P.source || {};
    const srcShort = SRC.short || { LeetCode: "LC", NeetCode: "NC" }[SRC.site] || "";
    const label = SRC.id ? `${srcShort} ${SRC.id} · ` : "";

    // ---------- static skeleton ----------
    const parts = {
      canvas: `<div class="panel vz-canvas" id="vz-canvas"></div>`,
      aux: `<div class="vz-aux" id="vz-aux"><div class="panel" id="vz-vars"></div></div>`,
      caption: `<div class="panel vz-caption" aria-live="polite">
        <div><span class="phase" id="vz-phase"></span><span class="vz-cap" id="vz-cap"></span></div>
        <div class="vz-inv" id="vz-inv"></div></div>`,
      controls: `<div class="vz-controls">
        <div class="vz-buttons"><button id="vz-start" aria-keyshortcuts="Home">Start</button>
        <button class="vz-icon" id="vz-prev" aria-label="Previous step" aria-keyshortcuts="ArrowLeft">‹</button>
        <button class="vz-icon vz-main" id="vz-play" aria-label="Play" aria-keyshortcuts="Space">${PLAY}</button>
        <button class="vz-icon" id="vz-next" aria-label="Next step" aria-keyshortcuts="ArrowRight">›</button>
        <button id="vz-end" aria-keyshortcuts="End">End</button></div>
        <div class="vz-speedrow"><label>Speed <input id="vz-speed" type="range" min="1" max="10" value="5"></label>
        <span class="vz-counter" id="vz-counter"></span></div></div>`,
      code: `<details class="panel" id="vz-code"><summary>Show code</summary><div class="vz-codebar"><div class="vz-tabs" id="vz-tabs" role="tablist" aria-label="Language"></div><button type="button" class="vz-copy" id="vz-copy" title="Copy this code without line numbers">Copy</button></div><div id="vz-code-body"></div></details>`,
    };
    const body = `<div class="vz-stage"><div class="vz-col">${parts.canvas}${parts.code}</div>
           <div class="vz-col">${parts.aux}${parts.controls}${parts.caption}</div></div>`;
    root.innerHTML = `
      <a class="vz-back" href="index.html">← Main page</a>
      <header class="vz-header"><h1>${esc(label)}${esc(P.title)}</h1>
        <span class="pill ${esc(P.difficulty.toLowerCase())}">${esc(P.difficulty)}</span>
        ${SRC.url ? `<a class="ext" href="${esc(SRC.url)}" target="_blank" rel="noopener">Open on ${esc(SRC.site || "the source site")} ↗</a>` : ""}</header>
      <div class="vz-meta" id="vz-meta"></div>
      <div class="vz-approaches" id="vz-approaches" role="tablist" aria-label="Approaches"></div>
      <details class="panel" id="vz-compare" hidden><summary>Compare approaches</summary><div class="vz-table-wrap" id="vz-compare-body"></div></details>
      <details class="panel" id="vz-constraints"><summary>Constraints — what they tell you</summary><div id="vz-constraints-body"></div></details>
      <details class="panel" id="vz-card"><summary>Why this pattern?</summary><div id="vz-card-body"></div></details>
      <div class="vz-examples" id="vz-examples" role="group" aria-label="Example input"></div>
      ${body}`;
    const $ = (id) => document.getElementById(id);

    // ---------- constraints (problem level) ----------
    (function constraints() {
      const rows = (P.constraints || [])
        .map((c) => `<tr><td class="mono">${esc(c.text)}</td><td>${esc(c.meaning)}</td><td>${esc(c.impact)}</td></tr>`)
        .join("");
      let hit = -1;
      if (P.nMax) hit = CHEATSHEET.findIndex((r) => P.nMax <= r.max);
      const sheet = CHEATSHEET.map((r, i) => {
        const prev = i === 0 ? null : CHEATSHEET[i - 1].max;
        const range = prev === null ? `n ≤ ${fmtN(r.max)}` : r.max === Infinity ? `n > ${fmtN(prev)}` : `n ≤ ${fmtN(r.max)}`;
        return `<tr class="${i === hit ? "hit" : ""}"><td class="mono">${range}</td><td class="mono">${r.fits}</td><td>${r.ex}</td></tr>`;
      }).join("");
      $("vz-constraints-body").innerHTML =
        `<div class="vz-table-wrap"><table class="vz-table"><thead><tr><th>Constraint</th><th>What it means</th><th>What it changes</th></tr></thead><tbody>${rows}</tbody></table></div>` +
        `<p class="vz-sub"><b>Rule of thumb:</b> about 10⁸ simple operations run in one second. Find the row for n to see which complexity is fast enough.` +
        (hit >= 0 ? ` Here n can be up to ${fmtN(P.nMax)}.` : "") + `</p>` +
        `<div class="vz-table-wrap"><table class="vz-table"><thead><tr><th>n</th><th>Fast enough</th><th>Typical approach</th></tr></thead><tbody>${sheet}</tbody></table></div>`;
    })();

    // ---------- approach tabs ----------
    const approaches = PAGE.approaches;
    if (approaches.length > 1) {
      $("vz-approaches").innerHTML = approaches
        .map((a, i) => `<button role="tab" data-a="${i}" aria-selected="false">${esc(a.name)}</button>`)
        .join("");
      $("vz-compare").hidden = false;
      $("vz-compare-body").innerHTML =
        `<table class="vz-table"><thead><tr><th>Approach</th><th>Time</th><th>Space</th><th>When to choose it</th></tr></thead><tbody>` +
        approaches.map((a) => `<tr><td><a href="#${esc(a.id)}">${esc(a.name)}</a></td><td class="mono">${esc(a.time)}</td><td class="mono">${esc(a.space)}</td><td>${esc(a.whenToUse || "")}</td></tr>`).join("") +
        `</tbody></table>`;
      $("vz-approaches").addEventListener("click", (e) => {
        const b = e.target.closest("[data-a]");
        if (b) selectApproach(+b.dataset.a, true);
      });
    } else $("vz-approaches").remove();

    // ---------- per-approach parts ----------
    let canvasImpl = null, ctx = null;

    function selectApproach(i, push) {
      stop();
      st.a = i;
      const A = approaches[i];
      if (push !== false && approaches.length > 1) history.replaceState(null, "", "#" + A.id);
      document.querySelectorAll("#vz-approaches [data-a]").forEach((b) => b.setAttribute("aria-selected", +b.dataset.a === i));
      const bigO = S.bigO ? ` <a class="ext" href="${esc(S.bigO)}" target="_blank" rel="noopener">Big-O ↗</a>` : "";
      const guideUrl = (S.patternGuides || {})[A.pattern] || S.notionPatterns;
      const guide = guideUrl ? ` <a class="ext" href="${esc(guideUrl)}" target="_blank" rel="noopener">Pattern guide ↗</a>` : "";
      $("vz-meta").innerHTML =
        `<span class="badge">${esc(A.pattern)}</span>` +
        (A.ds || []).map((d) => `<span class="badge ds">${esc(d)}</span>`).join("") +
        `<span class="cx">${esc(A.time)} time · ${esc(A.space)} space</span>${bigO}${guide}`;
      const C = A.card || {};
      const bf = P.bruteForce || {};
      $("vz-card-body").innerHTML =
        `<ul>` +
        (C.signals ? `<li><b>Signals:</b> ${esc(C.signals)}</li>` : "") +
        (bf.summary ? `<li><b>Brute force:</b> ${esc(bf.summary)}</li>` : "") +
        (C.pattern ? `<li><b>Pattern:</b> ${esc(C.pattern)}</li>` : "") +
        (C.coreIdea ? `<li><b>Core idea:</b> ${esc(C.coreIdea)}</li>` : "") +
        `<li id="vz-ops"></li></ul>` +
        (bf.code ? `<details><summary>Brute force code (Python3)</summary><div id="vz-bf-code"></div></details>` : "");
      if (bf.code) $("vz-bf-code").append(VIZ.codeBlock(bf.code));
      // approach.legend is kept in the data but not shown for now (ADR 023)
      buildCode(A);
      // examples
      const ex = A.examples;
      const mains = ex.map((x, j) => [x, j]).filter(([x]) => x.kind !== "edge");
      const edges = ex.map((x, j) => [x, j]).filter(([x]) => x.kind === "edge");
      const btn = ([x, j]) => `<button data-ex="${j}" aria-pressed="false" title="${esc(x.inputText)}">${esc(x.label)}</button>`;
      $("vz-examples").innerHTML =
        `<span class="lbl">Examples:</span>${mains.map(btn).join("")}` +
        (edges.length ? `<span class="sep"></span><span class="lbl">Edge cases:</span>${edges.map(btn).join("")}` : "");
      canvasImpl = VIZ.canvas.get(A.canvas);
      if (!canvasImpl) throw new Error("Canvas not registered: " + A.canvas);
      selectExample(0);
    }

    function buildCode(A) {
      const langs = LANG_ORDER.filter((l) => A.code[l]);
      if (!langs.includes(st.lang)) st.lang = langs[0];
      const acc = new Set(A.accepted || []);
      $("vz-tabs").innerHTML = langs
        .map((l) => `<button role="tab" data-lang="${l}" aria-selected="${l === st.lang}">${LANG_LABEL[l]}${acc.has(l) ? '<span class="acc" title="Accepted">✓</span>' : ""}</button>`)
        .join("");
      const body = $("vz-code-body");
      body.innerHTML = "";
      for (const l of langs) {
        const pre = VIZ.codeBlock(A.code[l].lines);
        pre.dataset.lang = l;
        pre.hidden = l !== st.lang;
        body.append(pre);
      }
      const notes = [];
      if (acc.size) notes.push("✓ = accepted on " + (SRC.site || "the judge") + " in that language.");
      if (!A.code.c && A.noC) notes.push("No C version: " + A.noC);
      if (notes.length) body.insertAdjacentHTML("beforeend", `<p class="note">${notes.map(esc).join(" ")}</p>`);
    }

    $("vz-copy").addEventListener("click", (e) => {
      const pre = document.querySelector(`#vz-code-body pre[data-lang="${st.lang}"]`);
      if (pre) VIZ.copyCode(pre, e.currentTarget);
    });

    $("vz-tabs").addEventListener("click", (e) => {
      const b = e.target.closest("[data-lang]");
      if (!b) return;
      st.lang = b.dataset.lang;
      document.querySelectorAll("#vz-tabs [data-lang]").forEach((x) => x.setAttribute("aria-selected", x.dataset.lang === st.lang));
      document.querySelectorAll("#vz-code-body pre").forEach((p) => (p.hidden = p.dataset.lang !== st.lang));
      highlightCode();
    });

    function selectExample(j) {
      stop();
      st.e = j;
      st.cur = 0;
      document.querySelectorAll("#vz-examples [data-ex]").forEach((b) => b.setAttribute("aria-pressed", +b.dataset.ex === j));
      buildCanvas();
      render(false);
    }

    function buildCanvas() {
      const A = approaches[st.a], X = A.examples[st.e];
      const aux = $("vz-aux");
      aux.querySelectorAll(".extra").forEach((n) => n.remove());
      ctx = { canvas: $("vz-canvas"), aux, approach: A, example: X, problem: P, extraPanel() {
        const p = el("div", "panel extra");
        aux.append(p);
        return p;
      } };
      canvasImpl.build(ctx);
      const ops = X.ops || {};
      const unit = P.bruteForce && P.bruteForce.opsUnit ? P.bruteForce.opsUnit : "operations";
      $("vz-ops").innerHTML = ops.brute != null
        ? `<b>On this input:</b> brute force needs ${ops.brute} ${esc(unit)}, this approach needs ${ops.approach}.`
        : "";
    }

    function highlightCode() {
      const A = approaches[st.a], s = A.examples[st.e].steps[st.cur];
      for (const pre of document.querySelectorAll("#vz-code-body pre")) {
        const line = (A.code[pre.dataset.lang].anchors || {})[s.anchor];
        let on = null;
        pre.querySelectorAll(".ln").forEach((l) => {
          const hit = +l.dataset.n === line;
          l.classList.toggle("on", hit);
          if (hit) on = l;
        });
        if (on && !pre.hidden && pre.scrollHeight > pre.clientHeight) {
          const top = on.offsetTop - pre.offsetTop, h = pre.clientHeight;
          if (top < pre.scrollTop || top > pre.scrollTop + h - 40) pre.scrollTop = Math.max(0, top - h / 3);
        }
      }
    }

    function render(flash) {
      const A = approaches[st.a], X = A.examples[st.e], steps = X.steps, s = steps[st.cur];
      canvasImpl.render(s, ctx, flash);
      VIZ.vars($("vz-vars"), s.vars || [], flash);
      $("vz-phase").textContent = (A.phases && A.phases[s.phase]) || s.phase;
      $("vz-cap").textContent = s.caption;
      const inv = s.invariant || A.invariant;
      $("vz-inv").textContent = inv ? "Invariant: " + inv : "";
      $("vz-counter").textContent = `Step ${st.cur + 1} / ${steps.length}`;
      $("vz-start").disabled = st.cur === 0;
      $("vz-prev").disabled = st.cur === 0;
      $("vz-next").disabled = st.cur === steps.length - 1;
      $("vz-end").disabled = st.cur === steps.length - 1;
      highlightCode();
    }

    const nSteps = () => approaches[st.a].examples[st.e].steps.length;
    function go(i, flash) { st.cur = Math.max(0, Math.min(nSteps() - 1, i)); render(flash); }
    function delay() { return 2200 - $("vz-speed").value * 200; }
    function setPlay(icon, label) { const b = $("vz-play"); b.textContent = icon; b.setAttribute("aria-label", label); }
    function stop() { clearTimeout(st.timer); st.timer = null; setPlay(PLAY, "Play"); }
    function tick() {
      if (st.cur >= nSteps() - 1) return stop();
      go(st.cur + 1, true);
      st.timer = setTimeout(tick, delay());
    }
    function toggle() {
      if (st.timer) return stop();
      if (st.cur >= nSteps() - 1) go(0);
      setPlay(PAUSE, "Pause");
      st.timer = setTimeout(tick, Math.min(400, delay()));
    }

    $("vz-start").onclick = () => { stop(); go(0); };
    $("vz-prev").onclick = () => { stop(); go(st.cur - 1); };
    $("vz-next").onclick = () => { stop(); go(st.cur + 1, true); };
    $("vz-end").onclick = () => { stop(); go(nSteps() - 1); };
    $("vz-play").onclick = toggle;
    $("vz-examples").addEventListener("click", (e) => {
      const b = e.target.closest("[data-ex]");
      if (b) selectExample(+b.dataset.ex);
    });
    root.addEventListener("click", (e) => { if (e.target.closest("button")) e.target.closest("button").blur(); });
    document.addEventListener("keydown", (e) => {
      if (e.metaKey || e.ctrlKey || e.altKey) return;  // key combinations belong to the browser and the OS
      if (e.target.tagName === "INPUT" || e.target.tagName === "TEXTAREA" || e.target.tagName === "SELECT") return;
      if (e.key === "ArrowRight") { stop(); go(st.cur + 1, true); }
      else if (e.key === "ArrowLeft") { stop(); go(st.cur - 1); }
      else if (e.key === " ") { e.preventDefault(); toggle(); }
      else if (e.key === "Home") { stop(); go(0); }
      else if (e.key === "End") { stop(); go(nSteps() - 1); }
    });
    let rt;
    window.addEventListener("resize", () => {
      clearTimeout(rt);
      rt = setTimeout(() => { buildCanvas(); render(false); }, 120);
    });
    window.addEventListener("hashchange", () => {
      const i = approaches.findIndex((a) => "#" + a.id === location.hash);
      if (i >= 0 && i !== st.a) selectApproach(i, false);
    });

    const start = Math.max(0, approaches.findIndex((a) => "#" + a.id === location.hash));
    selectApproach(start, false);

    // test hook for the smoke test in build.py
    VIZ._page = { st, go, selectApproach, selectExample, nSteps };
  };
})();
