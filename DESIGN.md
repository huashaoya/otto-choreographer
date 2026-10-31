---
name: Otto 在线编舞台
description: 六轴双足机器人的动作编排台，单文件离线运行；界面是一张 1971 年的口袋时刻表——青石板印的边栏，中间一页奶油纸站着机器人，金菊装订边把整本箍起来。
colors:
  slate: "#2B3A40"
  slate-2: "#3B484C"
  ivory: "#E9E0CA"
  bed: "#C49031"
  bed-lip: "#A87722"
  silk: "#CFC4A8"
  silk-dim: "#B4A98D"
  ink: "#1C1913"
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
  edge: "6px"
  gap: "0"
  row: "3px"
  inline: "8px"
components:
  page-chrome:
    backgroundColor: "{colors.slate}"
    textColor: "{colors.ivory}"
    rounded: "{rounded.none}"
    padding: "0 12px"
  page-stage:
    backgroundColor: "{colors.ivory}"
    textColor: "{colors.ink}"
    rounded: "{rounded.none}"
    padding: "10px"
  page-binding:
    backgroundColor: "{colors.bed}"
    textColor: "{colors.ink-soft}"
    rounded: "{rounded.none}"
    padding: "0 12px"
  frame-row:
    backgroundColor: "{colors.slate-2}"
    textColor: "{colors.ivory}"
    rounded: "{rounded.none}"
    padding: "5px 8px 5px 0"
  frame-row-active:
    backgroundColor: "{colors.ivory}"
    textColor: "{colors.ink}"
  button:
    backgroundColor: "transparent"
    textColor: "{colors.ivory}"
    rounded: "{rounded.none}"
    padding: "6px 12px"
  button-hover:
    backgroundColor: "{colors.ivory}"
    textColor: "{colors.ink}"
  button-primary:
    backgroundColor: "{colors.bed}"
    textColor: "{colors.ink}"
    rounded: "{rounded.none}"
    padding: "6px 12px"
  input-field:
    backgroundColor: "{colors.slate-2}"
    textColor: "{colors.ivory}"
    rounded: "{rounded.none}"
    height: "26px"
  json-box:
    backgroundColor: "transparent"
    textColor: "{colors.bed}"
    rounded: "{rounded.none}"
    padding: "8px 9px"
---

# Otto 在线编舞台 — Design System

## Overview

The product is a single-file, offline choreography desk for a six-servo biped. One person tunes a pose beside the robot and sequences those poses into a show. The interface is not a console and not a dashboard: it is a **1971 pocket timetable printed in two darknesses** — slate chrome for the margins, a deeper plate for the stage — bound in goldenrod.

Three surfaces, and they never trade places:

- **Slate `#2B3A40`** — the printed chrome. The header strip, the left column (axes and pose library), the right column (frame table, meter, JSON), and the status bar at the foot. It is where all the small type lives.
- **Window `#1E2A32`** — the stage. One step darker than the chrome, so the centre reads as a plate recessed into the page rather than printed on it. The robot stands there, and that is all that stands there. `#3B484C` lifts a frame row off the chrome; nothing lifts the window.
- **Goldenrod `#C49031`** — the binding. A 16px edge on all four sides, 9px mullions between the three panes, and the 20px imprint band along the bottom. About 6%, and it never becomes a working surface.

Ivory is no longer a surface at page scale. `#E9E0CA` is ink — the type on both dark tones, the reversed selected row, the primary action's fill, the modal and the tooltip. There is no paper anywhere in the page, and that is the point: a white robot on cream was 1.0× separation and looked weightless; on the window it is 2.7× and reads as an object.

The system is deliberately narrow: one type size, one radius, no gradients as surface treatment, no shadows as depth cues, no icon set. Rank comes from weight, case, reversal and rule. Colour does a job or it is not used.

## Colors

Six jobs, no seventh:

- **Slate `#2B3A40`** — the printed chrome, front to back. Header, both columns and the status bar are the same tone, separated only by hairlines, so the interface reads as one printed sheet. `#3B484C` lifts a frame row or a field off that block.
- **Window `#1E2A32`** — the stage plate, one step darker than the chrome so the centre reads as recessed. It is the only place the model is ever watched, and the only place a shadow falls.
- **Ivory `#E9E0CA`** — ink, not a surface. All primary type on slate and on the window, the reversed selected row, the primary button's fill, the modal, the tooltip. The reference measures `#F2EAD6` (L* 92.8); the shipped ivory is one step down at L* 89.3 — a recorded deviation, ΔL* 3.5, ΔE ≈ 2.5, invisible as a colour and real as a glare reduction when it last sat under a 710px panel.
- **Goldenrod `#C49031`** — the binding: the 16px page edge, the 9px mullions, the imprint band, the primary button's fill. It is not a surface, and it appears in no row or field. Its lip `#A87722` is the only edge tone it uses.
- **Vermilion `#C4442B`** — states that move or destroy: the playing row's fill (`#8F2A12`), the ruler cursor, the current frame's rail tick, the danger hover, the warning line. Its ink variants exist so the hue can pass contrast on both substances: `#EE8A6A` on slate, `#5E1A0B` on ivory and on gold.
- **Bottle green `#23503F`** — the confirmed connection, as the dot. On slate it holds 5.6:1, so the status word beside it stays ivory and the dot carries the whole signal.

Ink on the page is `#1C1913` at 14.62:1 and `#3A2C08` at 11.35:1. On slate, primary is `#E9E0CA` at 9.6:1 and secondary is `#B4A98D` at 6.2:1. On the binding, text is `#3A2C08` at 4.9:1. All are solid values — alpha over a saturated ground fails AA at any comfortable lightness.

## Typography

One size for the whole interface: **13px**, rising to **15px** below 600px because a 13px tool on a phone is a 13px tool held at arm's length. There is no display size, no headline size, no caption size.

Rank is carried four ways only:

1. **Weight** — 400 for values and prose, 700 for names, panel heads and the active view.
2. **Case and tracking** — `.16em`–`.2em` uppercase for panel heads and the product name; `0` tracking for Chinese labels.
3. **Reversal** — the selected frame row is an ivory page inside the slate block; nothing else in the row moves.
4. **Rule** — a 1px border is a section head; no head has a background.

Latin and numerals set in **Archivo Narrow**, embedded in the page as a base64 woff2 (latin subset, weights 400 and 700, SIL OFL 1.1) — the file must run with no network, so the font is part of the document. The fallback stack behind it is Roboto Condensed / Arial Narrow / Arial, but on a machine without Arial Narrow that stack silently becomes Arial: 10×“M” at 13px measures 108.30px in Arial against 88.80px in the embedded face. The embedded copy is the type, not a preference. Chinese falls through to the platform sans. Numerals are always tabular so angle columns align without being boxed.

Machine output is the one exception: the sequence JSON sets in **Cascadia Mono / Consolas at 11.5px**, and inline angle tokens inside frame rows use the mono stack at 13px. A code strip is a different substance from a label, and both worlds know it.

## Layout

Three dark panes held by goldenrod: a 16px edge all round and 9px mullions between them, so the columns are `300px | 1fr | 380px` at 1440 (`316 / 1035` in reference pixels, measured). The panes are two darknesses — slate, window, slate — and the gold, not a hairline, is what separates them. Inside a pane, hairlines divide rows.

Vertical order in each pane is fixed and each pane closes with its own status line: left — head, six axes, head, sixteen poses in two columns, `中立 90° / 限位 0–180°`; centre — stage, page caption, view row, play row (the playhead is the play row's last cell, not a separate strip); right — head, frame table, meter, timing fields, frame toolbar, head, code strip, `OTTO-SEQ v1 · 离线可编 / UTF-8 · N FRAMES`. Under all three, the goldenrod imprint band.

A servo row is two lines, as in the printed original: name and key chip, the range description inline beside them, the value flush right, then the ticked rule underneath. Nothing is stacked into a third line.

Below 1100px the three columns become one stack with the stage first (`order: -1`), because the robot is what you look at while dragging a slider. Below 700px the stage's right-hand caption drops out and the two footer bands wrap instead of colliding. Below 600px every control goes to a 42px minimum touch height.

## Elevation & Depth

There is no elevation. Nothing floats, nothing casts a drop shadow, no row lifts on hover.

Depth is three things only: the binding behind everything, the slate chrome printed on it, and the window sunk one tone below the chrome. There is no fourth plane, and nothing is ever raised above any of them — the selected frame row is the one exception, reversed to ivory so it reads as cut back down through the chrome. The only soft shading in the interface is light: the 3D stage casts a real contact shadow from its key light (`ShadowMaterial`, opacity .55) into the window, and that shadow is the one shadow the design owns. The rig is now tuned for darkness — key 2.7, hemisphere 2.0 (cool floor), fill 1.1, rim 2.2, white shell `#e8edf1` with clearcoat .16 — so the shell reads at L* 90 against a window at L* 16, a 2.7× separation. On paper the same shell sat at L* 90 against L* 89: a 1.0× separation, which is why it looked weightless.

**Focus is two-tone, never one colour.** `outline: 2px solid var(--ivory)` with `outline-offset: 1px` plus `box-shadow: 0 0 0 4px var(--slate)`. A single-colour ring cannot survive two substances: an ivory ring alone disappears on the page, a slate halo alone disappears on slate. Nothing in the file may set `outline: none` without replacing it.

## Shapes

Radius is zero everywhere. Buttons, inputs, rows, the modal, the toast: square corners, 1px borders. The only curve in the system is the connection dot.

The one recurring form is the **printed row**: a 1px hairline under every row, fixed columns, and a head that names them once. In the left column that is a `20px` index plus content; in the right it is `30px` index, `40px` type, `1fr` parameters, actions flush right. Rows are never cards — no border box, no fill, no gap between them.

Scales are drawn, not implied: the slider track is a 1px rule crossed by ticks every 15°; the ruler under the stage is a rule with major ticks every 50px and minors every 10px. These are the only repeating gradients in the file and they encode measurement. Both were kept against the mock's bare rules: a six-axis desk that hides its graduations is an instrument that lies.

## Components

- **Printed chrome** (header, left column, right column, status bar): slate field, ivory ink, hairlines in `rgba(242,234,214,.15)`, no border boxes anywhere.
- **Window** (stage): the `#1E2A32` plate, edge to edge inside the pane, with the two captions in ivory at its top corners and the projection line in silk beneath it. The robot, its shadow and the faint floor grid — nothing else. No card, no dock, no panel floating over the model.
- **Section head**: uppercase 700, `.16em` tracking, 3px padding, one hairline beneath, and a right-aligned micro tag in secondary silk (`R1–R6 · 0–180`, `P01–P16`).
- **Servo row**: two lines. Line one is the name in 700 plus an outlined mono key chip (`LL`, ivory hairline on transparent — never a filled chip, which would compete with reversal), the range description inline in secondary silk, the value flush right in 700. Line two is the ticked 1px rule with a 3px ivory bar thumb. The six axes run `lh rh ll rl lf rf` — hands first, then legs, then feet: the hands are what a pose reads by, and the feet are what it stands on.
- **Pose cell**: a printed table cell in a two-column grid, not a button — no border box, no fill, no radius; name in 700 on one line, its number (`P01`–`P16`) centred against the right edge, and the servo description carried by the cell's `title`/`aria-label` rather than printed. Sixteen cells of two-line descriptions were the densest wall in the interface; the name is what you pick by, the description is what you confirm by hovering.
- **Frame table head**: one hairline-thick row, `帧 / 类型 / 参数 · v / d`, in secondary silk. It is what makes the rack a timetable instead of a stack.
- **Frame row**: slate-2 row on the slate block — mono index (`F1`), type label (`姿态` ivory, `振荡` goldenrod), one line of mono angle pairs with the timing after it. Active reverses the whole row to the page; playing fills it with `#8F2A12`. Row actions do not live in the row: at 380px they cost a third of the width.
- **Frame toolbar**: `当前帧 ↑ ↓ 编辑 删除` under the timing fields, acting on the selected frame and disabled when there is none. Row actions moved here when the rack narrowed to 380px.
- **Timing fields**: `耗时 / 延迟` on one row under the meter — short labels, because the sequence delay above them already says which number is the show's and these two belong to the selected frame.
- **Tick rail**: a 16px column left of the frame table, one 2px tick per frame, the current frame's tick at 4px in vermilion. It is an index of the whole sequence, not a proportional minimap.
- **Window captions**: `预览 · 正面` and `真机标定 90° · 6 DOF · 正交投影` in ivory at the window's top corners; `正视 1:1 · 网格 60px · 舵机限位 0–180°` in silk under it. They are printed on the plate at 11.4:1, not chrome floating over it.
- **Playhead cell**: the last cell of the play row, `1 / 4` in mono ink, divided from 停止预览 by the same 1px rule as the buttons. The reference has no separate ruler strip, and neither does this build.
- **Pane foot**: a 22px line closing each pane, in mono secondary silk behind a hairline — `中立 90° / 限位 0–180°` under the poses, `OTTO-SEQ v1 · 离线可编 / UTF-8 · N FRAMES` under the code strip.
- **Imprint band**: the 20px goldenrod band across the whole page, `1971 · POCKET TIMETABLE No.04` in ink. The Chinese half of that imprint (`口袋时刻表斜架`) was cut at the owner's request — it named the world instead of the tool.
- **Buttons**: transparent with an ivory border; hover fills a 12% ivory. Primary is the inverse — ivory fill, ink text — because on a dark plate the emphasis is the light one. Destructive hover is `#A83318`, never bare vermilion, so ivory text holds contrast.
- **JSON strip**: the slate block with a hairline outline, goldenrod mono, no syntax colouring.
- **Two Darknesses**: slate `#2B3A40` for the chrome, window `#1E2A32` for the stage, and no third dark tone. They are never swapped, and a paper surface never appears at page scale.
- **Hover note**: one `?` button at the end of the timeline head row — 22px square, 1px ivory hairline, the same outline as every other button — opens a single 276px ivory card with a 1px ink border, square corners and no shadow, hanging 7px under it and joined to the button by an 8px connector line. The card carries both definitions as two rows divided by a hairline (姿态帧, then 振荡帧); the variable names (`v`, `d`, `c`, `p`) set in mono vermilion so they match the tokens in the frame rows. Shown on hover, on keyboard focus (`:focus-within` plus `aria-describedby`), and — because a phone has no hover — pinned open by clicking the button (Esc or a click outside dismisses it), never as the browser's own tooltip — a native tip would be rounded, shadowed and in the system font.
- **Scrollbar**: drawn, never the system's. A 12px lane with a 1px hairline down its inner edge and a 4px square ivory thumb (4px transparent border inside `background-clip: content-box`, so the visible bar is narrower than its hit area). No buttons, no arrows, no rounded caps. Hover brightens to `.62`, drag fills it with the binding gold. Chromium ignores `::-webkit-scrollbar*` as soon as `scrollbar-width` or `scrollbar-color` is declared, so those standard properties are deliberately absent from the file.

## Do's and Don'ts

**Do**

- Keep the binding visible on all four sides; the page must read as bound, not as a full-bleed screen.
- Keep the chrome continuous: header, both columns and the status bar are one slate tone separated by hairlines.
- Keep the window empty. The dark plate is the composition; filling it with cards, docks, paper or labels destroys the only calm surface left.
- Spend rank on weight, case, reversal and rule before reaching for a size.
- Give every colour a job: binding, chrome, window, ink, lifted row, armed, confirmed. If a new colour cannot name its job, it is decoration.
- Draw scales when a number has a range — sliders and the ruler both carry ticks.
- Print the row number in the margin (R1–R6, P01–P16) when a section header promises a count.
- Order the axes by how a pose is read — hands, legs, feet — not by the firmware's pin order.
- Mark a state with a filled row, a reversed cell, or a drawn rule — not with a stripe down one side.

**Don't**

- Don't sample a palette by eye. Every tone in this file came from a pixel measurement of the reference (`#2B3A40`, `#E9E0CA`, `#C49031`); the third (`#1E2A32`) came from measuring the complaint — 37% of the screen at L* 86 against chrome at L* 29. A "better contrast" substitution is how the first two attempts turned the ground inside out.
- Don't give the stage a paper mat, and don't give the chrome a paper panel. Ivory is ink; the moment it becomes a surface the page turns back into a light box.
- Don't add a second type size for hierarchy.
- Don't round a corner, lift a row, or add a blurred shadow.
- Don't put vermilion behind body text; it is an edge and a label colour.
- Don't let the frame table become floating cards — the hairlines and the shared column grid are what make it a table.
- Don't use a gradient as surface decoration; the only gradients are the two tick scales.
- Don't reintroduce an icon set: labels are the icons.
- Don't tint a whole axis to signal left or right. The name and the key chip already say which side it is.
- Don't let an instrument lie: the playhead prints the real total at rest, the ruler cursor sits at `activeFrame / (n−1)`, and each rail tick is drawn by its own row so it cannot drift from its index.
