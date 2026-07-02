# Motion spec — net-doctor v2 "Calm Field Guide"

Temperament: **settled**. The tool breathes slowly; it never flickers.

## Tokens
```css
--motion-micro: 130ms; --motion-small: 210ms;
--motion-large: 300ms; --motion-page: 400ms;
--ease-standard:  cubic-bezier(.2, 0, 0, 1);
--ease-spring:    cubic-bezier(.34, 1.26, .5, 1);
--ease-emphasized: cubic-bezier(.05, .7, .1, 1);
```

## Choreography (complete)
| Interaction | Animation | Spec | Communicates |
|---|---|---|---|
| View rise | fade + 10px | 400ms emphasized, one per view | context change |
| Step advance | new active card rises | 400ms emphasized | the probe moving down a layer |
| Card hover | −1px lift | 130ms spring | tactile |
| Button press | scale .97 | 130ms spring | press |
| Lock dot | blink ×2, hold | 1s ×2 | diagnosis latched — never an alarm loop |
| Brand lamp | opacity breathe | 3.2s loop (ambient status; collapses under reduced motion) | the guide is on |
| Busy AI | spinner + `aria-busy` + label swap | until resolve | honest progress |
| Theme swap | background transition | 300ms | place change |

Rejected: scanline/CRT effects, staggered lists, glow pulses, count-ups.

## Reduced motion
Global collapse (0.01ms, single iteration). Halo ring and verdicts are static
encodings; nothing rides on motion.
