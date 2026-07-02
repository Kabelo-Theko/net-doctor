# net-doctor — "Bench Oscilloscope" design system

**Project:** [net-doctor](https://github.com/Kabelo-Theko/net-doctor) · **Redesign:** complete UI/UX overhaul, July 2026

## The concept

net-doctor already thinks like an instrument — probe one layer at a time, stop
at the first broken one. The redesign makes it **look like the instrument it
is**: a bench oscilloscope. The diagnostic runs on a phosphor CRT screen with a
faint graticule; each completed check is a pulse on the trace (clean green =
passed, dropped red = failed); the conclusion is a **DIAGNOSIS LOCKED** readout
with a 2-blink trigger lamp. Views are channels on the front panel
(CH1 Diagnose · CH2 Escalation card · CH3 Reference), and OS / environment /
field-mode live in a Setup drawer of instrument switches.

A light **service-manual** theme (paper + schematic green) covers printed-page
tastes and bright rooms.

### Design DNA

| | |
|---|---|
| **Essence** | A network fault, on a scope. Method made visible. |
| **One-liner** | "A Tektronix bench scope hired to walk first-line through a fault." |
| **Archetype** | Engineer/Sage 70 (the method is the product) / Caregiver 30 (it holds your hand at 2am) |
| **Canvas** | CRT black-green `#0B110D` with a phosphor screen panel `#0D1710` (chosen for the instrument persona) · paper service-manual theme |
| **Accent** | Phosphor green `#5BEB9E` (trace, pass, locks) · fail trace `#FF7A66` · amber cursor `#F5C86B` for the active probe + AI labels |
| **Type cast** | Azeret Mono 600/700 (readouts, headings, commands) · Schibsted Grotesk (explanations) — a mono-led instrument voice, no serif anywhere |
| **Shape** | 3–10px radii, bezel panels with inner edges, square LEDs; graticule = 28px grid lines; scanline texture at 3.5% on the screen only |
| **Motion** | Trace-like: one rise per view on a probe bezier; the lock lamp blinks exactly twice; the only loop is the busy spinner |
| **Signature** | The graticule screen + spine-as-trace with pulse nodes and `signal clean / signal lost` verdicts; channel-button nav with LEDs |
| **Rejection list** | No blue/indigo tech gradients, no glassmorphism, no rounded consumer pills, no serif, no Inter, no glow beyond the phosphor budget (≤ .14 alpha), no emoji |

### Why this fits these users

A first-line tech mid-fault needs *sequence*, not choice. The trace makes
progress physical — you can see how deep into the stack you are, which checks
were clean, exactly where the signal was lost. Commands render for the tech's
actual OS; field mode splits every check into manager-speak and tech-speak
panes; the escalation card is the instrument printout second line actually
wants.

### How it differs from the siblings

Only project with: green-black CRT canvas, phosphor/graticule language,
mono-led type, channel-button nav, scanline texture. (ticket-triage: indigo
dispatch strips · onboard-kit: cream welcome kit · slo-watch: salmon broadsheet
· requirements-forge: cyanotype blueprint · incident-retro: archival dossier ·
resolve-notes: riso zine · portfolio: kinetic editorial.)

## Functional parity (zero loss)

All five flows (verbatim from `flows.py` mirror) · OS-aware commands ·
environment hints · multi-user precheck + major-incident banner · field-mode
dual panes · AI explain / router / escalation-note with reasoning receipts and
no-key fallbacks · resolution textarea → printable incident record (print
contract unchanged) · escalation card text format unchanged · deep-link URL
params (`os`, `env`, `field`, `store`, `symptom`) · resolve-notes cross-link.

New: channel nav with `aria-current` + LEDs, Setup drawer (was a popover),
CRT/manual themes persisted, live-region announcements after every verdict,
labelled AI inputs, skip link, focus management, custom instrument icon set.

## Files

`tokens.css` (both themes) · `tailwind.config.js` · `components.md` ·
`accessibility.md` · `motion.md` · `grid.md` · `icons/scope-icons.svg`
(7 symbols — 24px grid, 1.7 squared stroke).

## Reaching every state

| State | How |
|---|---|
| Input select (home) | Load the app |
| Multi-user banner | Toggle "Yes, several" in the precheck |
| Trace mid-flow | Pick CH1 symptom, answer a few checks — pass and fail both |
| Diagnosis locked | Follow any branch to its conclusion (lamp blinks twice) |
| Field mode dual panes | Setup → Field mode → Dual pane (best on the POS flow) |
| AI loading / fallback | Explain or Route without the backend |
| Escalation card / empty | CH2 after / before a diagnosis |
| Incident record print | Conclusion → Print incident record |
| Service-manual theme | Book icon, top right; persists |
| Deep link | `?symptom=pos&store=Gateway&os=mac&env=pos&field=1` |
