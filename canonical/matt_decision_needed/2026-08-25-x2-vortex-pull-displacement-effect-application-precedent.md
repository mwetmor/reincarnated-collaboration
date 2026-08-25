# X-2 — building `vortex_pull` displacement would set the sim's first effect-application law. Ruled DECLINED at phase level; Matt owns the reopen.

**Filed:** 2026-08-25 (knight-rider). **Occasioned by:** gamora's X-2 Part-2 survey return (`dispatches/2026-08-24-gamora-x1-x2-spatial-vocabulary-routings.md`), consumed while sequencing Step-2 tranche 3.

**This is not a request for a build authorization.** The build was declined at my level and the row was minted around the gap. This row exists because *the reason for declining is a design precedent Matt owns*, and a decision made silently at phase level is exactly the shape the orientation rule was written to catch.

---

## The situation in four lines

- Spec § 6.2 / charter make **RT-6 law**: `vortex_pull` is **NOT scored on VFX alone** — its readability criterion requires **enemy displacement**.
- gamora surveyed the sim and returned: displacement machinery **already exists** (`spatial_engine.py:2378-2443`, the Wave-D fear flee-AI). `on_vortex_pull` **is a phantom** — the hook is named but fires nowhere. The one genuine gap is a **world-anchored attractor**.
- Her verdict was explicit: **"WIRING, not capability."** The build is *cheap*.
- I declined it anyway.

## Why cheap was not the criterion

gamora's own return names the consequence better than I can paraphrase it:

> *displacement would be the first control effect in the sim to actually apply, setting the effect-application law ahead of the decode B-2 refused to guess* (`MD-B2-2`).

So the sequencing question is: **does a VFX-scoring criterion get to set the simulation's first effect-application law?**

Under `CLAUDE.md`'s orientation rule — **engine > game > phase** — no. The effect-application law is *engine* (architectural integrity). The `vortex_pull` readability score is *phase* (an operational unit of the Step-2 wave). Letting the phase need mint the engine law inverts the ordering, and it does so at the worst possible site: whatever wiring lands first becomes the precedent every later control effect is read against, established not by a decode but by whichever row happened to need a number.

**B-2 declined to guess this.** Building it as a side effect of a VFX tranche would be guessing it, with less deliberation than B-2 applied when it refused.

## What I did instead

`vortex_pull` mints in tranche 3A (R-8) with its displacement criterion recorded **`UNEVALUABLE — never PASS`**, per the **#80 cl. 2(a)** shape: where the criterion's object is absent, the criterion cannot go red, so it must not be allowed to go green either. The row's VFX is minted and scored on everything RT-6 does *not* reserve. The gap is recorded in the row, not hidden by it.

This is the conservative disposition: it costs one unevaluable criterion on one row, and it costs nothing that cannot be recovered by scoring that criterion later once the law exists.

## What Matt actually owns here

Three things, in descending urgency. **None blocks tranche 3.**

1. **Is the decline correct?** If you want `vortex_pull` fully scored inside Step-2, say so and X-2 fires — but then the effect-application law is being set by this wave, deliberately, and that should be on the record as a choice rather than as a side effect.
2. **When does `MD-B2-2` get decoded?** X-2 is now the *second* consumer waiting on it. The queue behind that decode is growing, and the pressure to shortcut it grows with the queue. That pressure is the thing to watch, not any individual row.
3. **The phantom itself.** `on_vortex_pull` is a named hook that fires nowhere. That is a live misleading surface in the sim regardless of how 1 and 2 resolve — a reader encountering it reasonably concludes the effect is wired. Cheapest fix is a comment or a raise; it needs no decision, only a routing, and it is routed to gamora with the rest of her named opens.

## Empirical criterion that gates re-engagement

**Not time.** The `MD-B2-2` decode landing, or Matt's explicit ruling that the Step-2 wave may set the effect-application law. Either one unblocks X-2's build; neither is expected inside this wave.

## Cross-references

- Survey of record: `dispatches/2026-08-24-gamora-x1-x2-spatial-vocabulary-routings.md` (Part-2 completion record)
- Row as minted: `dispatches/2026-08-25-drax-s2c-mint-tranche-3a.md` § R-8
- Spec: `gandalf/notes/2026-08-24-vfx-archetype-binding-spec-DRAFT.md` § 3.1.19; RT-6 at § 6.2
- Sibling finding on X-1 (the same survey's Part 1, which I *did* discharge): the `circle`-for-annulus approximation, carried into R-7 `orbit` as an authoring instruction rather than a blocker.
