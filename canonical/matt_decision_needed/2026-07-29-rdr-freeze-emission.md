# Should RDR content generation emit `freeze`? (WR1 wave, M-7 leg 3)

**Filed:** 2026-07-29, gandalf (RUN-CONDUCTOR, run WR1-2026-07-28) — the one UNCONDITIONAL Matt HALT out of the M-4..M-9 spec set (`gandalf/design-inputs/2026-07-29-wr1-m4to9-specs.md` §M-7).

**The question:** RDR's freeze-shatter operators are woken but corpus-dormant — nothing in generation emits `freeze`, and the execute operator fires 0 times. GD's freeze (the fidelity source for the wave) is pure CC — **no shatter**. So there is NO fidelity warrant in either direction: whether RDR content should emit freeze, and whether a shatter burst (~20% max HP) should exist at all, is a pure RDR balance/design call — your territory, not the wave's.

**Options:**
- **(a) Stay dormant** (default; zero work) — freeze remains woken-but-unfed; revisit at content-design time.
- **(b) Emit freeze as CC-only** — matches the GD-fidelity freeze the wave models; shatter stays dead.
- **(c) Emit freeze with RDR shatter** — the 20%-max-HP burst goes live; a real balance surface opens.

**What does NOT wait on this:** M-7 legs 1–2 build regardless; predicate P-5 (ratified) guarantees shatter-count = 0 in every post-wave battery, so the baton cannot be contaminated whichever way you rule.
