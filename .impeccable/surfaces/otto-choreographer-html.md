---
version: 1
slug: "otto-choreographer-html"
primary_target: "otto-choreographer.html"
related_targets: []
---

# Surface: otto-choreographer.html

Mode: Operate. Single-file offline web tool, desktop-first, 390px must still work.

## Direction contract

**THESIS** — This is a departure table you compose on: every frame is a scheduled departure numbered on a raked rack of slides lying on a lit goldenrod bed. The category's floating dark cards with one neon accent are refused; so is the control-panel costume.

**OWN-WORLD** — Goldenrod stock carries the working ground and the left slide; carbon slabs hold the two dark areas; bible ivory is the reversed surface and the one opaque pane. One type size in a condensed grotesque; rank comes only from weight, case, reversal and rule. Code chips in bottle green and vermilion; vermilion marks the armed frame, bottle green the confirmed connection. Everything else is carbon ink on goldenrod or ivory on carbon.

**STORY** — The visitor reads six axes at a glance, sees the whole sequence as a position on a graduated ruler, and knows which frame is live because exactly one slide is reversed. They drag, watch the robot, and send.

**FIRST VIEWPORT** — Full-bleed goldenrod bed with a wide outer margin. A carbon title band spans the top: product name in goldenrod at the left, connection controls at the right. Three slides sit on the bed: goldenrod stock at the left holding the six axes and the twelve presets; a carbon stage in the centre with a graduation ruler under it; a carbon rack at the right where frame tickets rake down a tick rail, with the sequence JSON printed as a code strip below it.

**FORM** — 1971 pocket timetable read as a raked rack of tinted glass slides on a lit goldenrod bed; third on the ordered list, taken over the assigned stitch chart; seed: 33c54be83220ccc4

**FINISH** — unreviewed and undocumented is unfinished; this build ends with the finish review, the verdict, DESIGN.md, and every shipping raster carrying its provenance.

## Constraints carried in

- Static check locks: exactly two inline `<script>`, no external script src, no fetch/XHR, no viewport zoom lock, and a fixed set of JS substrings (view defaults, assembly coordinates, side mapping, licence metadata). Do not touch them.
- Tests forbid: `.model-note` inside `#robotStage`; the strings 点击追加 / 拖动… in `#view3dControls`; any clear confirmation dialog. `#connStatus` text stays 未连接 / 已连接 / 错误.
- Every element id used by the app JS stays; class names consumed by JS (`servo`, `right`, `preset-grid`, `frame`, `active`, `playing`, `osc-servo`, `show`) stay.
- Offline: no webfont download. The condensed voice comes from a system stack led by Arial Narrow, with CJK falling back to the platform sans.

## Unresolved

- Whether the mobile layout keeps the bed margin or lets slabs go edge to edge.
