# Responsive grid & layout — net-doctor "Bench Oscilloscope"

## Breakpoints
| Width | Changes |
|---|---|
| ≤ 560px | H1 compresses; cheat table scrolls horizontally; AI inputs release min-width; channel row wraps to its own line (order 3) |
| ≤ 620px | Field-mode dual panes stack |
| 940px | `--bench-max` — instrument face never stretches wider |

Checked at 360 / 768 / 1280.

## Column structure
Single-column instrument face (a scope is one screen):
```
┌ front panel (sticky) ─ brand · CH1 CH2 CH3 · setup · theme ┐
├ setup drawer (when open): OS | Environment | Field mode    ┤
│ signal path strip (LINK → IP → GW → DNS → APP)             │
│ H1 + lede + setup context line                             │
│ CH1: precheck → AI analyzer → AI router → input select     │
│  └ in flow: [scope screen: graticule + trace + readout]    │
│ CH2: escalation printout                                   │
│ CH3: layer list + cheat table                              │
│ footer                                                      │
└──────────────────────────────────────────────────────────────┘
```

## Reflow rules
- **Trace**: fixed 34px gutter for pulse nodes; measurement text max 64ch;
  commands wrap as inline blocks.
- **AI rows**: input flexes (min 200px), model + button wrap beneath on narrow.
- **Symptom buttons**: full-width rows at all sizes (tap targets first).
- **Conclusion actions**: wrap freely; primary first in source order.
- **Cheat table**: block-scrolls inside its bezel below 560px.
- **Setup drawer**: groups wrap with 32px gaps.

## Type fluidity
H1 `clamp(1.6 → 2.6rem)` mono; readouts fixed; body 15px. Explanations capped
at 62–66ch.

## Rhythm
4px grid (93% audited). Bezel interiors 16/20px; graticule cell 28px (7×4 —
on-grid); section padding 40–64px.
