# Accessibility sheet — net-doctor "Bench Oscilloscope"

Target WCAG 2.2 AA. Implemented in `docs/index.html`.

## Measured contrast (WCAG 2.x)

### Screen theme (CRT)
| Pair | Ratio | Verdict |
|---|---|---|
| text-max #EAF5EC / base #0B110D | 15.5:1 | AAA |
| text-primary #D2E2D5 / base | 14.2:1 | AAA |
| text-secondary #96AB9B / panel #131B15 | 7.19:1 | AAA |
| text-secondary / screen #0D1710 | 7.49:1 | AAA |
| text-tertiary #7E937F / base (base only) | 5.79:1 | AA+ |
| phosphor #5BEB9E / screen | 12.05:1 | AAA |
| phosphor / inset (commands) | 12.89:1 | AAA |
| phos-ink #04140B / solid phosphor | 12.45:1 | AAA |
| fail #FF7A66 / screen | 7.17:1 | AAA |
| fail-ink #230703 / solid fail | 7.46:1 | AAA |
| cursor #F5C86B / base | 12.14:1 | AAA |

### Service-manual theme (paper)
| Pair | Ratio | Verdict |
|---|---|---|
| text-primary #28312A / base #F4F3EC | 12.1:1 | AAA |
| text-secondary #525F53 / panel | 6.5:1 | AA+ |
| schematic green #156B3F / base | 5.89:1 | AA |
| green ink #F2FBF4 / solid green | 6.2:1 | AA+ |
| fail #A5352A / base | 6.01:1 | AA+ |
| cursor #7A5A00 / base | 5.74:1 | AA |
| green / inset commands | 5.38:1 | AA |

Notes: the scanline overlay (3.5% effective) and graticule sit behind panels,
never behind body text at meaningful density; command lines render on the
clean inset. Glow budget ≤ 0.14 alpha, phosphor elements only.

## Focus indicators
Two-layer `:focus-visible` ring (2px canvas + 2px phosphor) on channels, setup
switches, symptom buttons, pass/fail triggers, AI inputs/selects, textareas,
action buttons, footer links.

## Keyboard navigation order
1. Skip link → `#main`
2. Front panel: brand → CH1/CH2/CH3 → Setup (aria-expanded drawer) → theme
3. Setup drawer: OS → Environment → Field mode (grouped, labelled)
4. Diagnose home: scope toggle → AI analyzer (input → model → Explain) → AI router → symptom buttons CH1–CH5
5. In-flow: Back → pass/fail triggers → (conclusion) resolution textarea → actions
6. Enter submits both AI inputs

View changes move focus to `#main`; every verdict is announced.

## ARIA strategy
| Surface | Treatment |
|---|---|
| Channels | `aria-current="page"`; LEDs decorative |
| Setup | Trigger `aria-expanded` + `aria-controls`; switch groups `role="group"` with labels |
| Verdicts | Announced via `.sr-only` `role="status"` live region ("Check passed. Next check ready." / "…Diagnosis locked.") — the trace is visual reinforcement, not the only channel |
| Signal-path strip | Single `aria-label` ("Signal path: link, IP, gateway, DNS, application") |
| AI fields | `.sr-only` labels; buttons get `aria-busy` + spinner while fetching |
| Trace nodes | Pass/fail encoded three ways: node color, `signal clean / signal lost` text verdict, and position in history |
| Print record | Unchanged semantics; visibility-based print CSS |
| Icons | All `aria-hidden`; theme toggle has dynamic `aria-label` |

## Color independence
Pass/fail always paired with text verdicts; the active probe is amber *and*
labelled by the answer buttons; multi-user severity is a worded banner;
environment hints are labelled blocks. The lock lamp blink is decorative
(2 iterations, holds) — the "Diagnosis locked" text carries the meaning.

## Motion
One rise per view; lock lamp 2 blinks then static; busy spinner only during
fetches. Full `prefers-reduced-motion` collapse (animations + transitions to
0.01ms, single iteration). Scanlines are static (no flicker, ever).

## Targets & zoom
Buttons ≥ 40px tall; channel buttons ≥ 36px; setup switches ≥ 32px with 4px
gaps (grouped controls). Fluid to 360px; zoom never disabled.
