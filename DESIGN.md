---
name: Otto 在线编舞台
description: 六轴双足机器人的动作编排台，单文件离线运行；界面是一张摊在金菊硬封上的奶油纸口袋时刻表，帧是表里的行。
colors:
  bed: "#C8912C"
  bed-lip: "#A9751F"
  carbon: "#1C1913"
  carbon-2: "#26221A"
  slate: "#2C3A40"
  ivory: "#F2EAD6"
  silk: "#CFC4A8"
  silk-dim: "#B4A98D"
  ink-soft: "#3A2C08"
  vermilion: "#C4442B"
  vermilion-ink: "#EE8A6A"
  vermilion-deep: "#5E1A0B"
  bottle: "#23503F"
typography:
  ui:
    fontFamily: "Archivo Narrow, Roboto Condensed, Arial Narrow, Helvetica Neue, Arial, sans-serif"
    fontSize: "13px"
    fontWeight: 400
    lineHeight: 1.45
    letterSpacing: "0em"
  ui-mobile:
    fontFamily: "Archivo Narrow, Roboto Condensed, Arial Narrow, Helvetica Neue, Arial, sans-serif"
    fontSize: "15px"
    fontWeight: 400
    lineHeight: 1.45
  data:
    fontFamily: "Cascadia Mono, Consolas, ui-monospace, monospace"
    fontSize: "11.5px"
    fontWeight: 400
    lineHeight: 1.55
    letterSpacing: "0.02em"
  data-inline:
    fontFamily: "Cascadia Mono, Consolas, ui-monospace, monospace"
    fontSize: "13px"
    fontWeight: 400
    lineHeight: 1.45
    letterSpacing: "0.02em"
rounded:
  none: "0"
  dot: "50%"
spacing:
  bed: "8px"
  gap: "0"
  section: "6px"
  row: "4px"
  inline: "8px"
components:
  button:
    backgroundColor: "transparent"
    textColor: "{colors.carbon}"
    rounded: "{rounded.none}"
    padding: "6px 12px"
  button-hover:
    backgroundColor: "{colors.carbon}"
    textColor: "{colors.bed}"
  button-primary:
    backgroundColor: "{colors.carbon}"
    textColor: "{colors.bed}"
    rounded: "{rounded.none}"
    padding: "6px 12px"
  panel-stock:
    backgroundColor: "{colors.ivory}"
    textColor: "{colors.carbon}"
    rounded: "{rounded.none}"
    padding: "0 12px"
  panel-stage:
    backgroundColor: "{colors.ivory}"
    textColor: "{colors.carbon}"
    rounded: "{rounded.none}"
    padding: "0 12px"
  frame-row:
    backgroundColor: "transparent"
    textColor: "{colors.ivory}"
    rounded: "{rounded.none}"
    padding: "5px 8px 5px 0"
  frame-row-active:
    backgroundColor: "{colors.ivory}"
    textColor: "{colors.carbon}"
  json-box:
    backgroundColor: "{colors.carbon-2}"
    textColor: "{colors.bed}"
    rounded: "{rounded.none}"
    padding: "8px 9px"
  input-field:
    backgroundColor: "{colors.ivory}"
    textColor: "{colors.carbon}"
    rounded: "{rounded.none}"
    height: "26px"
---

# Otto 在线编舞台 — Design System

## Overview

The product is a single-file, offline choreography desk for a six-servo biped. One person tunes a pose beside the robot and sequences those poses into a show. The interface is not a console and not a dashboard: it is a **1971 pocket timetable printed on a cream sheet and glued into a goldenrod hard cover**. The cover is the frame you hold, the sheet is the page you fill in, the right column is the one block that was printed in dark ink.

The sheet is continuous: the six axes and the pose library on the left, the robot standing on the same paper in the centre, divided only by hairlines. Two substances only, paper and printed ink, bound by a goldenrod edge. The system is deliberately narrow: one type size, one radius, no gradients as surface treatment, no shadows as depth cues, no icon set. Rank comes from weight, case, reversal and rule. Colour does a job or it is not used.

## Colors

Six jobs, no seventh:

- **Goldenrod `#C8912C`** — the cover, and only the cover: the 8px page edge, the header strip, the two footer lines. It never becomes a working surface. Its lip `#A9751F` is the only edge tone the cover uses.
- **Bible ivory `#F2EAD6`** — the sheet. It is both the panel ground and the stage ground, so the robot stands on the same paper the sliders are printed on. It is the dominant surface and carries roughly half the interface.
- **Carbon `#1C1913`** — the printed block: the right column only (frame table, meter, code strip). `#26221A` is the second carbon used inside that column's inputs.
- **Slate `#2C3A40`** — retired as a surface. It survives only as a mid-tone in the 3D environment map, never as a fill.
- **Vermilion `#C4442B`** — the armed state, and only states that move or destroy: the playing row's fill, the ruler cursor, the current frame's rail tick, the danger hover, the warning line. Its ink variants exist so the hue can pass contrast on both grounds: `#EE8A6A` on carbon, `#5E1A0B` on ivory and on the cover.
- **Bottle green `#23503F`** — the confirmed connection only, as the dot. At 3.29:1 on the cover it clears the 3:1 bar for UI graphics but not the text bar, so the status word beside it stays carbon.

Ink on the sheet is `#1C1913` at 14.62:1 and `#3A2C08` at 11.35:1. On carbon, primary is `#F2EAD6` and secondary is `#B4A98D`. On the cover, primary is carbon at 6.30:1 and secondary is `#3A2C08` at 4.89:1; both solid values, never alpha, because alpha over a saturated ground fails AA at any comfortable lightness.

## Typography

One size for the whole interface: **13px**, rising to **15px** below 600px because a 13px tool on a phone is a 13px tool held at arm's length. There is no display size, no headline size, no caption size.

Rank is carried four ways only:

1. **Weight** — 400 for values and prose, 700 for names, panel heads and the active view.
2. **Case and tracking** — `.16em`–`.2em` uppercase for panel heads and the product name; `0` tracking for Chinese labels.
3. **Reversal** — the selected frame is an ivory sheet inside the dark printed block; nothing else in the row moves.
4. **Rule** — a 1px border is a section head; no head has a background.

Latin and numerals set in **Archivo Narrow**, embedded in the page as a base64 woff2 (latin subset, weights 400 and 700, SIL OFL 1.1) — the file must run with no network, so the font is part of the document. The fallback stack behind it is Roboto Condensed / Arial Narrow / Arial, but on a machine without Arial Narrow that stack silently becomes Arial: 10×“M” at 13px measures 108.30px in Arial against 88.80px in the embedded face. The embedded copy is the type, not a preference. Chinese falls through to the platform sans. Numerals are always tabular (`font-variant-numeric: tabular-nums`) so angle columns align without being boxed.

Machine output is the one exception: the sequence JSON sets in **Cascadia Mono / Consolas at 11.5px**, and inline angle tokens inside frame rows use the mono stack at 13px. A code strip is a different substance from a label, and both worlds know it.

## Layout

A fixed three-column grid on the sheet: `302px | 1fr | 500px`, no gutters, divided by 1px hairlines. The sheet itself is inset 8px inside the goldenrod cover, so the cover is always visible as an edge on all four sides — the page must read as held, not as a full-bleed screen.

Vertical order in each column is fixed: a section head, then content. Above the sheet sits the cover's header strip (44px) and below it the two footer lines (20px + 16px), so the frame of the page is never the viewport edge.

The left column never scrolls as a whole — the six axes are fixed and the sixteen-pose library sits under them in two columns, tight enough to show all sixteen at 900px. The centre is `1fr / auto / auto / auto / auto`: stage, ruler, page caption, view row, play row. The right column is `auto / 0-1 / auto / auto / 1`: head, frame table, meter, head, code strip.

Below 1100px the three columns become one stack with the stage first (`order: -1`), because the robot is what you look at while dragging a slider; the hairline dividers turn into the bottom edge of each block. Below 700px the stage's right-hand caption drops out and the two footer lines wrap instead of colliding. Below 600px every control goes to a 42px minimum touch height.

## Elevation & Depth

There is no elevation. Nothing floats, nothing casts a drop shadow, no row lifts on hover.

Depth is a bound book, expressed only by **binding order**: cover, sheet, printed block. The cover is `body`'s own goldenrod with an 8px gap; the sheet is `main` with a 1px hairline; the printed block is the right column with no border at all, because ink does not need an edge. The selected frame is a reversed sheet cut into the printed block. The only soft shading in the interface is light, not layering: the 3D stage casts a real contact shadow from the key light (`ShadowMaterial`, opacity .17) onto the page, and that shadow is the one shadow the design owns. The former light-pool radials are gone with the dark stage.

**Focus is two-tone, never one colour.** `outline: 2px solid var(--ivory)` with `outline-offset: 1px` plus `box-shadow: 0 0 0 4px var(--carbon)`. A single-colour ring cannot survive three grounds: vermilion measures 1.79:1 on goldenrod, and an ivory ring alone disappears on an ivory card. The ivory ring holds 14.62:1 on carbon and the carbon halo holds 11.35:1 on the sheet, so at least one component is always readable on either substance. Nothing in the file may set `outline: none` without replacing it.

## Shapes

Radius is zero everywhere. Buttons, inputs, rows, the modal, the toast: square corners, 1px borders. The only curve in the system is the connection dot.

The one recurring form is the **timetable row**: a 1px hairline under every row, four fixed columns (`30px` index, `40px` type, `1fr` parameters, actions flush right), and a header row that names them once. Rows are not cards — they have no border box, no fill and no gap, so the column reads as one printed table with a tick rail down its left edge. The retired rake (an 8px sheared ticket on every frame) survives only as history: a table has no left edge to shear.

Scales are drawn, not implied: the slider track is a 1px rule crossed by ticks every 15°; the ruler under the stage is a rule with major ticks every 50px and minors every 10px. These are the only repeating gradients in the file and they encode measurement. Both were kept from the previous world deliberately — the reference mock draws its sliders as bare rules, but a six-axis desk that hides its graduations is an instrument that lies.

## Components

- **Sheet panel** (left and stage): ivory ground, carbon ink, no border of its own — a 1px hairline on its right edge is the only division, and hairline rules separate rows inside.
- **Printed block** (right): carbon ground, ivory ink, no border; it is the one dark column on the page and it runs full height.
- **Cover strip** (header): goldenrod ground, carbon ink, 44px, 1px darker hairline beneath, connection controls at the right in outlined carbon.
- **Cover foot** (two lines under the sheet): mono, `#3A2C08` and 62% carbon, one line of live state (`中立 90° · 舵机限位 0–180°` / the Home pose) and one imprint line (`1971 · POCKET TIMETABLE No.04 · 口袋时刻表斜架`).
- **Section head**: uppercase 700, `.16em` tracking, 4px padding, one hairline beneath, and a right-aligned micro tag in secondary ink (`R1–R6 · 0–180`, `P01–P16`).
- **Servo row**: name in 700 + a reversed mono key chip (`LL`), value right-aligned 700, a ticked 1px track with a 3px bar thumb, and the range description under it in secondary ink. Right-side servos are no longer tinted — the key chip already carries the side, and vermilion there read as an alarm.
- **Pose cell**: a printed table cell in a two-column grid, not a button — no border box, no fill, no radius; name in 700, its number (`P01`–`P16`) set in the cell's top-right corner, description in secondary ink beneath.
- **Frame row**: a table row — mono index (`F1`), type label (`姿态` / `振荡` in goldenrod), one line of mono angle pairs with the timing on the next, and `↑ ↓ 编辑 删除` flush right behind hairlines. Active reverses the whole row to an ivory sheet; playing fills it with `#8F2A12`.
- **Table head**: one hairline-thick row above the frames, `帧 / 类型 / 参数 · v / d`, in secondary silk. It is what makes the rack a timetable instead of a stack.
- **Tick rail**: a 16px column left of the frame table, one 2px tick per frame, the current frame's tick at 4px in vermilion. It is an index of the whole sequence, not a proportional minimap.
- **Page captions**: `预览 · 正面` and `真机标定 90° · 6 DOF · 正交投影` sit inside the stage's top corners; `正视 1:1 · 网格 60px · 舵机限位 0–180°` sits under the viewport. They are printed on the page, not chrome over it.
- **Ruler**: 26px strip under the stage carrying the playhead chip (`1 / 4`) in carbon on goldenrod, with ticks that belong to the paper now rather than to a dark panel.
- **Buttons**: transparent with a current-colour border; hover fills with the inverse. Primary is carbon fill with goldenrod text. Destructive hover is `#A83318`, never bare vermilion, so ivory text holds contrast.
- **JSON strip**: `#26221A` ground inside the printed block, goldenrod mono, 1px hairline, no syntax colouring.

## Do's and Don'ts

**Do**

- Keep the cover visible around the sheet; the page must read as bound, not as a full-bleed screen.
- Spend rank on weight, case, reversal and rule before reaching for a size.
- Give every colour a job: cover, sheet, printed ink, reversal, armed, confirmed. If a new colour cannot name its job, it is decoration.
- Draw scales when a number has a range — sliders and the ruler both carry ticks.
- Use a solid ink value rather than an alpha tint when text sits on the cover, and keep text off the cover entirely where a spreadsheet of values is involved.
- Keep the six axes visible while the pose library scrolls.
- Print the row number in the margin (R1–R6, P01–P16) when a section header promises a count.
- Mark a state with a filled row, a reversed sheet, or a drawn rule — not with a stripe down one side.

**Don't**

- Don't add a second type size for hierarchy.
- Don't round a corner, lift a row, or add a shadow.
- Don't put vermilion behind body text; it is an edge and a label colour.
- Don't let the frame table become floating cards — the hairlines and the shared column grid are what make it a table.
- Don't use a gradient as surface decoration; the only gradients left are the two tick scales.
- Don't reintroduce an icon set: labels are the icons.
- Don't decorate a row edge with an accent stripe; state belongs in the row's fill.
- Don't let an instrument lie: the playhead prints the real total at rest, the ruler cursor sits at `activeFrame / (n−1)`, and each rail tick is drawn by its own row so it cannot drift from its index.
- Don't turn the stage back into a dark box. The robot is white; on cream it is held by a cast shadow and a faint 280-unit grid, not by contrast against carbon.
