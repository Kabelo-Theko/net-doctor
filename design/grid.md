# Responsive grid & layout — net-doctor v2 "Calm Field Guide"

## Breakpoints
| Width | Changes |
|---|---|
| ≤ 560px | Cheat table scrolls; AI inputs release min-width; active card un-indents; timeline gutter tightens |
| ≤ 620px | Field-mode panes stack |
| ≤ 880px | **Rail → sticky top bar** (blurred), labels collapse to icons, channels scroll horizontally |
| 880px+ | 216px rail · content column (max 880px + gutters) |

Checked at 360 / 768 / 1280.

## Structure
```
┌ rail 216px ┬ content ───────────────────────────────┐
│ ● net-doctor │ [setup band when open]               │
│ GUIDE        │ (LINK·IP·GATEWAY·DNS·APP) capsule    │
│ ● Diagnose   │ Clash H1 · lede · context line       │
│ ○ Escalation │ precheck → AI boxes → symptom cards  │
│ ○ Reference  │   └ flow: timeline + active card     │
│ ──────────── │        → diagnosis readout           │
│ ⚙ Setup      │ footer                                │
│ ◐ Theme      │                                       │
└──────────────┴───────────────────────────────────────┘
```

## Reflow
Timeline: 40px gutter, dots at −47px; active card indents −20px on desktop,
flush on mobile. Symptom cards full-width always. Setup groups wrap at 32px
gaps. Escalation printout is fluid mono.

## Rhythm
4px grid (88% audited). Cards 20px interior; content sections 32–64px; hero
32px below capsule. Radii: 10 (rail items) / 14 (chips) / 20 (cards) /
26 (readout) / pill (controls).
