# net-doctor — "Calm Field Guide" design system (v2)

**Project:** [net-doctor](https://github.com/Kabelo-Theko/net-doctor) · **v2 redesign, July 2026**
*(v1's CRT/oscilloscope theme was retired after review: novelty theming,
mono-everything and scanline texture read as AI-generated. v2 designs the
product, not a costume.)*

## The concept

At 2am with a store offline, the tool's job is to be **the calmest thing in the
room**. v2 is a field guide with a steady hand: warm obsidian canvas, bone ink,
one aqua pulse that marks exactly what's alive — the active step, the primary
action, the lamp. The diagnostic reads as a soft numbered timeline; the
conclusion arrives as a quiet, aqua-ringed readout. A warm bone light theme
covers bright rooms.

### Design DNA

| | |
|---|---|
| **Essence** | A steady hand for the worst hour of the shift. Method made calm. |
| **One-liner** | "Linear's design team hired to rebuild a paper troubleshooting flowchart." |
| **Canvas** | Warm obsidian `#131110` with bone ink `#F3EFE9` (field, default) · warm bone `#F5F1E8` (light). Warm neutrals, never sci-fi green-black. |
| **Accent** | Aqua pulse `#3ECFBB` (field) / deep aqua `#0F7A6D` (bone) — active step ring, primary actions, the breathing brand lamp. Pass/fail stay semantic green/red as tinted chips and solid trigger buttons. |
| **Type cast** | Clash Display 600 (headlines, flow titles — confident 2026 grotesk, Fontshare) · General Sans (text, Fontshare) · Red Hat Mono (commands and IDs only) |
| **Shape** | Soft 10–26px radii, pill controls, segmented pill switches — tactile, not bezelled |
| **Signature** | The **layer-path capsule** (LINK · IP · GATEWAY · DNS · APP as a segmented pill) and the timeline whose active step sits in a lifted card with an aqua halo ring |
| **Motion** | Settled: one rise per view, active-step halo static, lamp breathes at 3.2s (ambient), lock dot blinks ×2 then holds |
| **Rejection list** | No CRT/scanlines/graticule, no phosphor green, no mono body text, no hard 3px radii, no channel-hardware metaphors, no glow beyond the halo ring |

### The 2026 bar it was rebuilt against
Warm canvas · Clash Display scale moment (hero clamp 2.2–3.9rem vs 15px body)
· left-rail app shell (the suite's only sidebar) · pill/segmented controls ·
ONE accent ≤5% of screen · 12%-alpha semantic chips · spring hovers ·
Fontshare voice.

## Functional parity (zero loss — engine untouched)

The v1 script ships intact (only theme names renamed screen→field,
manual→bone): all five flows, OS-aware commands, environment hints, multi-user
precheck + banner, field-mode dual panes, AI explain / router / escalation-note
with reasoning receipts and no-key fallbacks, escalation-card text contract,
printable incident record (print CSS contract unchanged), URL deep links
(`os, env, field, store, symptom`), resolve-notes cross-link, verdict
announcements, focus management.

## Files
`tokens.css` · `tailwind.config.js` · `components.md` · `accessibility.md` ·
`motion.md` · `grid.md` · `icons/scope-icons.svg` (8 round-stroke icons).

## Reaching every state
| State | How |
|---|---|
| Home / input select | Load the app — five symptom cards with aqua number chips |
| Multi-user banner | Toggle "Yes, several" |
| Timeline mid-flow | Pick a symptom; answer pass and fail |
| Diagnosis readout | Reach any conclusion (aqua ring, lock dot ×2) |
| Field-mode panes | Setup → Field mode → Dual pane |
| AI loading / fallback | Explain or Route offline |
| Escalation card / empty | Second rail item, after / before a diagnosis |
| Bone (light) theme | Theme in the rail foot; persists |
| Deep link | `?symptom=pos&store=Gateway&os=mac&env=pos&field=1` |
