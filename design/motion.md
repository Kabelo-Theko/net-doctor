# Motion spec — net-doctor "Bench Oscilloscope"

Temperament: **trace-like**. An instrument settles; it does not bounce.

## Tokens
```css
--motion-micro: 110ms; --motion-small: 190ms;
--motion-large: 280ms; --motion-page: 380ms;
--ease-standard: cubic-bezier(.2, 0, 0, 1);
--ease-trace:    cubic-bezier(.3, .7, .1, 1);  /* probe settle */
```

## Choreography
| Interaction | Trigger | Animation | Spec | Communicates |
|---|---|---|---|---|
| View rise | channel change / render | fade + 8px rise | 380ms trace, one per view | page context |
| Node append | pass/fail answered | new active block rises | 380ms trace | the probe advancing |
| Lock lamp | conclusion reached | LED opacity blink **×2, then holds** | 1s standard | diagnosis latched — never an infinite alarm |
| Trigger press | active | translateY(1px) | 110ms | tactile |
| Busy states | AI fetch | spinner + `aria-busy` + label swap ("Analysing…", "Routing…", "Writing…") | until resolve — the only loop |
| Setup drawer | Setup click | display toggle (no slide — a switch, not a curtain) | instant |
| Theme swap | toggle | background transition | 280ms standard |

Rejected on purpose: staggered list entrances (checks arrive one at a time by
nature), glow pulses (glow budget is static, ≤ .14), scanline flicker
(nauseating, banned), count-ups.

## Reduced motion
Global collapse (0.01ms, single iteration). The lock lamp holds lit; verdicts
are text; nothing rides on motion alone.
