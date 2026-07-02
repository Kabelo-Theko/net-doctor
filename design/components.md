# Component library — net-doctor "Bench Oscilloscope"

Semantic tokens only (`tokens.css`). Type: readouts/data = Azeret Mono,
explanations = Schibsted Grotesk.

## Front panel (navigation)
Sticky bezel bar: brand lamp + wordmark · **channel buttons** CH1/CH2/CH3
(square LED + mono caps label) · Setup · theme toggle.
Channel states: default (inset bg, dim LED) / hover / `aria-current` (phosphor
text + border, lit LED with glow) / focus-visible.

## Setup drawer
Full-width bezel drawer (replaces the old popover — reachable, not hover-lost):
three labelled switch groups (OS · Environment · Field mode). Switch states:
default / hover / **on** (solid phosphor + dark ink) / focus-visible.

## Buttons
Mono-labelled rects (3px radius):
| Variant | Use |
|---|---|
| `.btn-pass` | phosphor solid — "Passed / looks healthy" |
| `.btn-fail` | fail solid — "Failed / not right" |
| `.btn-primary` | phosphor solid — card/primary actions |
| `.btn-ghost` | outline — secondary actions |
All six states: default / hover / focus-visible / active (1px press) /
disabled (.55) / busy (`aria-busy` + spinner + label swap).

## Signature components

### Scope screen (`.scopescreen`)
The flow container: screen-green panel, 28px **graticule** grid, static
scanline overlay (3.5%), inner edge + shadow. Everything diagnostic happens
inside it.

### The trace (`.spine` + `.node`)
Vertical phosphor baseline; each check is a square pulse node:
- **done-pass** — solid phosphor node + `SIGNAL CLEAN` verdict chip
- **done-fail** — solid fail node + `SIGNAL LOST` chip
- **active** — amber-ringed hollow node + measurement block: check text,
  OS-aware command (`» prefix`, phosphor on inset), interpretation, triggers.

### Diagnosis readout (`.conclusion`)
Phosphor-bordered panel with contained glow: `◾ DIAGNOSIS LOCKED` label (lamp
blinks ×2, holds) → cause (mono 700) → FIX (phosphor heading) → environment
hint (amber heading, env-specific) → WHEN TO ESCALATE → resolution textarea →
actions (escalation card · AI note · resolution note → resolve-notes ·
print record · start over).

### Field-mode dual panes
`FOR THE STORE MANAGER` (phosphor top rule) / `FOR THE TECHNICIAN` (amber top
rule, command voice). Grid 2-up, stacks < 620px.

## AI analyzer boxes
Amber-labelled bezel panels: error explainer (input + model + Explain) and
flow router (description + Route → plan + layer chip + "Start:" button).
Every response carries a mono **reasoning receipt**; every failure has a
designed no-key note that points back to the rule-based path.

## Symptom picker ("input select")
CH-numbered buttons: mono channel square + title + description. Hover =
phosphor border; the number is the affordance (an input jack, not a bullet).

## Escalation card
Mono `pre` printout on inset (text contract unchanged), copy + back actions;
designed empty state when no diagnosis is on the screen.

## Reference
Layer list (1·Link → 5·App) as a bezel list with phosphor layer keys;
three-OS command cheat table (mono phosphor `code`), horizontal scroll on
small screens.

## Incident record (print)
Unchanged print contract: visibility-swap CSS, signature lines, checks table.

## Iconography
`icons/scope-icons.svg` — 7 symbols (probe-trace, alert, book, crt, spark,
copy, check). 24px grid · 1.7px squared stroke — an instrument etch; LEDs and
channel squares are CSS primitives, not icons.
