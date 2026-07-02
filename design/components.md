# Component library — net-doctor v2 "Calm Field Guide"

Semantic tokens only. Type: Clash Display (headlines) · General Sans (text) ·
Red Hat Mono (commands/IDs only).

## App shell — left rail (the suite's only sidebar)
216px sticky rail: brand (breathing aqua lamp + Clash wordmark) · GUIDE label ·
three items with LED dots · rail foot (Setup, Theme).
Item states: default / hover (aqua-subtle wash) / `aria-current` (surface fill
+ aqua ring + lit LED) / focus-visible.
≤ 880px: the rail becomes a blurred sticky top bar; labels collapse to icons.

## Setup band
Toggled by the rail's Setup (`aria-expanded`); a soft card of **segmented pill
switches** (OS / Environment / Field mode): default / hover / on (solid aqua +
dark ink) / focus-visible.

## Masthead
**Layer-path capsule** (signature): LINK · IP · GATEWAY · DNS · APP as a
segmented pill, first segment lit. Clash Display H1 with aqua emphasis word →
lede → mono context line (setup summary).

## Symptom cards
Full-width rounded cards: aqua number chip (44px, 14px radius) + Clash title +
supporting line. Hover: raise −1px, aqua border; press .99.

## The timeline (flow)
Soft vertical line with 14px dot nodes:
- done-pass: solid green dot, row at 78% opacity, "looks healthy" chip
- done-fail: solid red dot, "not right" chip
- **active: lifted surface card with an aqua halo ring around its dot** —
  check text, command pill (mono, » prefix, on inset), interpretation,
  Pass (solid green pill) / Fail (solid red pill) triggers.

## Diagnosis readout
26px-radius surface card with aqua border + deep shadow: "DIAGNOSIS LOCKED"
(dot blinks ×2) → Clash cause → FIX (green heading) → environment note (amber
heading) → WHEN TO ESCALATE → resolution textarea → actions (escalation card ·
AI note · resolution note → resolve-notes · print record · start over).

## Field-mode panes
Inset panes: FOR THE STORE MANAGER (green role label) / FOR THE TECHNICIAN
(amber role label, mono command voice). 2-up, stack < 620px.

## AI boxes
Soft cards: labelled rows (spark = explain, probe = router), borderless inset
inputs, pill selects, primary aqua actions; layer chips as aqua-subtle pills;
mono reasoning receipts; designed no-key notes.

## Escalation card
Mono printout in a soft card (text contract unchanged) + copy/back; designed
empty state.

## Reference
Layer list card (Clash layer keys) + three-OS command table (mono command ink),
horizontal scroll ≤ 560px.

## Buttons
Pills: primary aqua / pass green / fail red / ghost outline; six states each
(hover lift, spring press, `aria-busy` spinner).

## Iconography
`icons/scope-icons.svg` — 8 symbols (probe, alert, book, sun, spark, copy,
check, dial), 24px grid, **1.8 round stroke**. LEDs and dots are CSS
primitives.
