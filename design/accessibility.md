# Accessibility sheet — net-doctor v2 "Calm Field Guide"

Target WCAG 2.2 AA. Implemented in `docs/index.html`.

## Measured contrast (WCAG 2.x)

### Field theme (warm dark, default)
| Pair | Ratio | Verdict |
|---|---|---|
| bone #F3EFE9 / obsidian #131110 | 16.4:1 | AAA |
| text-secondary #B5AC9F / surface #1C1917 | 7.8:1 | AAA |
| text-tertiary #9A9184 / base | 5.6:1 | AA+ |
| aqua #3ECFBB / base | 9.73:1 | AAA |
| on-accent #062A24 / aqua | 7.95:1 | AAA |
| aqua-text #8AE0D2 / base | 12.26:1 | AAA |
| command ink #8AE0D2 / inset #0D0B0A | 12.79:1 | AAA |
| pass #5BC98A / base · ink #0A2C1A on pass | 9.12 / 7.32:1 | AAA |
| fail #F08A7B / base · ink #2B0B06 on fail | 7.73 / 7.48:1 | AAA |
| amber #E8C87D / base | 11.65:1 | AAA |

### Bone theme (light)
| Pair | Ratio | Verdict |
|---|---|---|
| ink #26211B / bone #F5F1E8 | 14.2:1 | AAA |
| text-secondary #5E564A / surface | 6.98:1 | AA+ |
| deep aqua #0F7A6D / bone (labels/large) | 4.63:1 | AA |
| on-accent #F2FBF9 / deep aqua | 4.95:1 | AA |
| command ink #0A5A50 / inset #EBE5D8 | 6.46:1 | AA+ |
| pass #20713F · fail #AC3A2B / bone | 5.33 / 5.49:1 | AA |

## Focus, keyboard, ARIA
- Two-layer focus ring (canvas + aqua) everywhere, including rail items and
  segmented switches.
- Rail order: skip link → brand → Diagnose → Escalation card → Reference →
  Setup (`aria-expanded`/`aria-controls`) → Theme. Then content in DOM order.
- View changes move focus to `#main`; every pass/fail verdict is announced via
  the `.sr-only` live region ("Check passed. Next check ready." / "Diagnosis
  locked.").
- Verdicts triple-encoded: node color + `SIGNAL CLEAN`/`SIGNAL LOST`-class text
  chips ("looks healthy"/"not right" wording preserved from engine) + position.
- Layer-path capsule: single `role="img"` label ("The layered method: link,
  then IP…"); segments decorative.
- AI inputs labelled (`.sr-only`); buttons `aria-busy` with spinner + label
  swap while fetching.
- Setup switch groups are labelled `role="group"` sets of real buttons.
- Print record semantics unchanged.

## Motion
One rise per view · active-step halo is static · lamp breathes 3.2s (ambient
brand status; collapses under reduced motion) · lock dot blinks exactly twice
· spinner only while fetching. Global reduced-motion collapse.

## Targets & zoom
Rail items ≥ 44px; trigger buttons ≥ 44px; segmented switches ≥ 36px. Fluid to
360px (rail becomes a top bar ≤ 880px); zoom never disabled.
