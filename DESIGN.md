---
name: Otto 在线编舞台
description: 六轴双足机器人的动作编排台，单文件离线运行；界面是摊在灯台上的口袋时刻表，帧是斜置的票根。
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
  bed: "12px"
  gap: "12px"
  section: "6px"
  row: "4px"
  inline: "8px"
components:
  button:
    backgroundColor: "transparent"
    textColor: "{colors.silk}"
    rounded: "{rounded.none}"
    padding: "6px 12px"
  button-hover:
    backgroundColor: "{colors.ivory}"
    textColor: "{colors.carbon}"
  button-primary:
    backgroundColor: "{colors.bed}"
    textColor: "{colors.carbon}"
    rounded: "{rounded.none}"
    padding: "6px 12px"
  panel-stock:
    backgroundColor: "{colors.bed}"
    textColor: "{colors.carbon}"
    rounded: "{rounded.none}"
    padding: "0 12px"
  panel-slab:
    backgroundColor: "{colors.carbon}"
    textColor: "{colors.ivory}"
    rounded: "{rounded.none}"
    padding: "0 12px"
  frame-card:
    backgroundColor: "{colors.slate}"
    textColor: "{colors.ivory}"
    rounded: "{rounded.none}"
    padding: "5px 9px 6px"
  frame-card-active:
    backgroundColor: "{colors.ivory}"
    textColor: "{colors.carbon}"
  json-box:
    backgroundColor: "{colors.carbon-2}"
    textColor: "{colors.bed}"
    rounded: "{rounded.none}"
    padding: "8px 9px"
  input-field:
    backgroundColor: "{colors.carbon-2}"
    textColor: "{colors.ivory}"
    rounded: "{rounded.none}"
    height: "26px"
---

# Otto 在线编舞台 — Design System

## Overview

The product is a single-file, offline choreography desk for a six-servo biped. One person tunes a pose beside the robot and sequences those poses into a show. The interface is not a console and not a dashboard: it is a **1971 pocket timetable read as a raked rack of tinted glass slides lying on a lit goldenrod bed**. The bed is the field, the slides are the work, and the drop of a slide into the rack is how a frame joins the show.

Three surfaces sit on the bed and never merge into one another: goldenrod stock on the left (the six axes and the pose library), a carbon stage in the centre (the robot under a lamp), a carbon rack on the right (the frames, the meter, the JSON code strip).

The system is deliberately narrow. One type size, one radius, no gradients as surface treatment, no shadows as depth cues, no icon set. Rank comes from weight, case, reversal and rule. Colour does a job or it is not used.

## Colors

Six jobs, no seventh:

- **Goldenrod `#C8912C`** — the lit bed. It is the page ground, the left panel's stock, the active frame's accent chip, the cursor of the ruler. It carries roughly half the visible surface. Its lip `#A9751F` is the only edge tone the bed uses.
- **Carbon `#1C1913`** — the stage and the rack. Absolute ground for everything the robot is watched on, so the white model reads as lit matter rather than a white card. `#26221A` is the second carbon used only inside inputs and the code strip.
- **Slate `#2C3A40`** — the unselected frame slide. A tinted glass tone, one step off carbon, only ever the body of a frame card.
- **Bible ivory `#F2EAD6`** — the reversed surface. The selected frame, the modal sheet, the hovered neutral button. Ivory is what "this one is live" looks like without a colour.
- **Vermilion `#C4442B`** — the armed state. The osc ticket label, the playing frame's ticket, the danger hover, the warning line. Never a background for body text. Its two ink variants exist so the same hue can pass contrast on both grounds: `#EE8A6A` on carbon, `#5E1A0B` on goldenrod.
- **Bottle green `#23503F`** — the confirmed connection only. One dot, nothing else.

Ink on goldenrod is `#1C1913` for primary text and `#3A2C08` for secondary; both are solid values, never alpha, because alpha over a saturated ground fails AA at any comfortable lightness. On carbon, primary is `#F2EAD6` and secondary is `#B4A98D`.

## Typography

One size for the whole interface: **13px**, rising to **15px** below 600px because a 13px tool on a phone is a 13px tool held at arm's length. There is no display size, no headline size, no caption size.

Rank is carried four ways only:

1. **Weight** — 400 for values and prose, 700 for names, panel heads and the active view.
2. **Case and tracking** — `.16em`–`.2em` uppercase for panel heads and the product name; `0` tracking for Chinese labels.
3. **Reversal** — the selected frame is ivory on carbon; nothing else in the row moves.
4. **Rule** — a 1px border is a section head; no head has a background.

Latin and numerals set in **Archivo Narrow**, embedded in the page as a base64 woff2 (latin subset, weights 400 and 700, SIL OFL 1.1) — the file must run with no network, so the font is part of the document. The fallback stack behind it is Roboto Condensed / Arial Narrow / Arial, but on a machine without Arial Narrow that stack silently becomes Arial: 10×“M” at 13px measures 108.30px in Arial against 88.80px in the embedded face. The embedded copy is the type, not a preference. Chinese falls through to the platform sans. Numerals are always tabular (`font-variant-numeric: tabular-nums`) so angle columns align without being boxed.

Machine output is the one exception: the sequence JSON sets in **Cascadia Mono / Consolas at 11.5px**, and inline angle tokens inside frame cards use the mono stack at 13px. A code strip is a different substance from a label, and both worlds know it.

## Layout

A fixed three-column grid on the bed: `302px | 1fr | 440px`, 12px gutters, 12px bed margin all round. The columns are slides, so they never touch the viewport edge — the goldenrod bed must be visible as a field around them, not merely as a fill behind them.

Vertical order in each column is fixed: a section head, then content. The left column never scrolls as a whole — the six axes are fixed and the twelve-pose library scrolls under them with a visible thin scrollbar. The centre is `1fr / auto / auto / auto`: stage, ruler, view row, play row. The right column is `auto / 0-1 / auto / auto / 1`: head, frame rack, meter, head, code strip.

Below 1100px the three columns become one stack with the stage first (`order: -1`), because the robot is what you look at while dragging a slider. Below 600px the bed margin drops to 8px and every control goes to a 42px minimum touch height.

## Elevation & Depth

There is no elevation. Nothing floats, nothing has a drop shadow, no card lifts on hover.

Depth is a stack of physical sheets and is expressed only by **which sheet is on top**: the bed is behind everything; a panel is a sheet on the bed marked by a 1px lip and a 2px hard offset in the lip colour (`box-shadow: 0 2px 0 var(--bed-lip)`); the selected frame is a reversed sheet inside its column. The stage carries a single soft radial pool of warm light behind the model — that is light, not elevation. The same lamp falls on the bed: `main` carries a 115%×88% radial that lifts the goldenrod from #C8912C to #D19B33 at 26% — a 4% value change that makes the paper read as lit rather than painted. These two radials are the only soft gradients in the interface.

**Focus is two-tone, never one colour.** `outline: 2px solid var(--ivory)` with `outline-offset: 1px` plus `box-shadow: 0 0 0 4px var(--carbon)`. A single-colour ring cannot survive three grounds: vermilion measures 1.79:1 on goldenrod, and an ivory ring alone disappears on an ivory card. The carbon halo holds 6.30:1 on the bed and the ivory ring holds 14.62:1 on carbon, so at least one component is always readable. Nothing in the file may set `outline: none` without replacing it.

## Shapes

Radius is zero everywhere. Buttons, inputs, cards, panels, the modal, the toast: square corners, 1px borders. The only curve in the system is the connection dot.

The one recurring form is the **rake**: every frame card opens with a ticket whose right edge is sheared 8px (`clip-path: polygon(0 0, 100% 0, calc(100% - 8px) 100%, 0 100%)`). Tickets align on a common axis, so the rack reads as a stack of slides slid in from the left. The shear is the same 8px at every card height and is never applied to text.

Scales are drawn, not implied: the slider track is a 1px rule crossed by ticks every 15°; the ruler under the stage is a rule with major ticks every 50px and minors every 10px. These are the only repeating gradients in the file and they encode measurement.

## Components

- **Stock panel** (left): goldenrod field, carbon ink, `1px solid var(--bed-lip)` edge, hairline rules between rows, no inner boxes.
- **Slab panel** (right/stage): carbon field, ivory ink, black hairline edge.
- **Section head**: uppercase 700, `.16em` tracking, 6px padding, one hairline beneath, and a right-aligned micro tag in secondary ink (`R1–R6 · 0–180`, `P01–P12`).
- **Servo row**: name in 700 + a reversed mono key chip (`LL`), value right-aligned 700 (vermilion-deep for the right-side servos), a ticked 1px track with a 3px bar thumb, and the range description under it in secondary ink.
- **Pose cell**: a printed table cell, not a button — no border, no fill, no radius; name in 700 over its description in secondary ink; the whole cell is the target.
- **Frame card**: slate body, no left border, ticket on the left (mono `#3`, type label beneath), one line of mono angle pairs, then a meta line with `↑ ↓ 编辑 删除` flush right. Active inverts the whole card to ivory; playing adds a 3px vermilion edge.
- **Tick rail**: a 16px column left of the rack, one 2px tick per frame, the current frame's tick at 4px in vermilion. It is an index of the whole sequence, not a proportional minimap.
- **Ruler**: 26px strip under the stage carrying the playhead chip (`3 / 4`) in carbon on goldenrod.
- **Buttons**: transparent with a current-colour border; hover fills with the inverse. Primary is goldenrod fill with carbon text. Destructive hover is `#A83318`, never bare vermilion, so ivory text holds contrast.
- **JSON strip**: `#26221A` ground, goldenrod mono, 1px hairline, no syntax colouring.

## Do's and Don'ts

**Do**

- Keep the bed visible around every panel; the field is the world.
- Spend rank on weight, case, reversal and rule before reaching for a size.
- Give every colour a job: bed, ground, glass, reversal, armed, confirmed. If a new colour cannot name its job, it is decoration.
- Draw scales when a number has a range — sliders and the ruler both carry ticks.
- Use a solid ink value rather than an alpha tint when text sits on goldenrod.
- Keep the six axes visible while the pose library scrolls.
- Print the row number in the margin (R1–R6, P01–P16) when a section header promises a count.
- Mark a state with a filled ticket, a reversed sheet, or a drawn rule — not with a stripe down one side.

**Don't**

- Don't add a second type size for hierarchy.
- Don't round a corner, lift a card, or add a shadow.
- Don't put vermilion behind body text; it is an edge and a label colour.
- Don't let the frame rack become floating cards — the ticket shear and the shared axis are what make it a rack.
- Don't use a gradient as surface decoration; the only gradients are the light pool behind the model and the tick scales.
- Don't reintroduce an icon set: labels are the icons.
- Don't decorate a card edge with an accent stripe; state belongs in the ticket's fill.
- Don't let an instrument lie: the playhead prints the real total at rest, the ruler cursor sits at `activeFrame / (n−1)`, and each rail tick is drawn by its own card so it cannot drift from its ticket.
