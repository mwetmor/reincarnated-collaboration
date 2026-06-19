# SESSION CLOSE — VFX register-test (Gap #8) → V1 juiced-Binbun in the current war_hall

**Author:** gandalf (design steward). **Date:** 2026-06-19. **Type:** session-close handoff / resume-point.
**Thread:** the buy-vs-build VFX question — does the Binbun CC0 backbone + the in-engine juice lever reach the genre-register floor, or must we build a Hovl harvest pipeline? — carried from the register-test tripod through to V1-in-the-actual-game.
**Discipline note:** deferred items below are gated by **empirical criteria** (re-score / re-render evidence), NOT time-passage. Resume each when its named evidence-gate is the next thing to produce.

---

## WHAT LANDED (this session)

1. **VFX register-test spec authored + §8 window-hygiene discipline** — `notes/2026-06-18-vfx-register-test-spec-binbun-emission.md` (commits `e8bad05`, `b9d438c`). The one experiment that collapses the buy-vs-build tree: V0 (stock Binbun) / V1 (the juice lever: `blend_add` + `emission 2.0` + 32-billboard ember) / V2 (Brackeys flipbook harvest-proxy). §8 = every visual/VFX test self-closes its render window (Matt directive after closing 10+ orphans).
2. **The tripod ran to a verdict** — drax build (`4b707bb`) + galadriel Wave-2 scorecard (`7401031`) + harness hygiene patch w/ 120s watchdog (`e71e989`). Verdict: **MARGINAL** — `notes/2026-06-18-vfx-register-test-verdict-binbun-backbone.md` (`681ac2a`). Backbone register-VIABLE; juice lever proven on the energy axes (bloom **above T3** 3.47, motion **+26.2**); the two shortfalls (hue, depth) are in-engine-fixable / confounded, NOT a harvest mandate. **Recommendation: defer the harvest, run a cheap in-engine V1.1.**
3. **V1 put into the ACTUAL game (the live ask)** — corrected a stale mis-target (the first integration hit the Jun-15 boss arena; Matt: *"these are very old rooms/clips"*) → retargeted to the **current** war_hall (`Zone3_elite_pack` in `arena_descent.tscn`). drax shipped `harness_logs/spellfx_v1_warhall.mp4` + a 6-beat frame-strip; new harnesses committed (NOT pushed — Matt-gated); **parity PASS** (35/35), **Gate B held**, §8 hygiene clean. Caught a latent bug: the boss harness's `fire_trail` instantiated as the wrong type → the earlier boss clip's trail never rendered.
4. **In-context adjudication: PASS** — `notes/2026-06-19-v1-warhall-incontext-adjudication.md` (`<this session>`). V1 reads as a premium **directed** fireball (the backwards-routing bug drax fixed mid-run); legible charge→…→fade arc; premium read **in the chamber that helps it least** (war_hall = brightest/coolest in the descent). The one cost — the white-hot impact core — is register-predicted, in-engine-fixable (hue-lock), and chamber-amplified. **Confirms the defer-harvest call with real-geometry evidence.**

## PENDING DECISION (Matt ratifies — not evidence-gated, just your call)

**The V1 rollout.** My recommendation is **(A)**: greenlight V1 as the hero-cast fire substrate + apply the hue-lock fix + roll it into the remaining summon placeholders (`render_arena_room.gd` still runs the old `SummonGlow`+`SummonFireColumn`). Alternatives on the table: **(B)** judge once more in a dark chamber before rollout; **(C)** hue-lock first, re-render, then decide. The decision is the gate on everything below.

## DEFERRED — each with its EMPIRICAL re-engagement criterion

- **Hue-lock fix + re-render** (fires if rollout = A or C). *Criterion to resume-and-close:* a re-score showing the achromatic-blown fraction dropped / hue recovers **≥ T2** while bloom (**≥ T3**) and motion (**+26**) hold. That evidence — not elapsed time — is what confirms the fix.
- **Dark-chamber showcase render** (oubliette / cathedral). Worth doing as the *showcase* frame regardless of A/B/C. *Criterion:* does the same V1 bloom read against dark-fantasy mood — i.e. is the war_hall result the FLOOR (likely) or the ceiling of V1's quality.
- **The V1.1 round from the MARGINAL verdict — now SHRUNK.** Directionality is no longer untested (the war_hall render proved the directed projectile), so the remaining fixes are **hue-lock + 3–4 composed depth layers + a re-windowed depth metric** (galadriel O2/O4). *Criterion (the big win):* if V1.1 clears **T2 on depth + hue**, the harvest is **unnecessary** and the Binbun backbone is **confirmed register-sufficient for the full 400-combo catalogue** — no pipeline to build. Only if depth stays capped after proper layering + a re-windowed metric does a hero-slot-only Hovl harvest get scoped, with depth named + quantified.
- **The scene-scoring rubric dive (O1–O5)** — `notes/2026-06-18-scene-scoring-rubric-opportunity-memo.md`. Tee'd up, fires on your steer. **O1 (the genre-register calibration ladder) IS the measuring stick the quality spike needs** — build the stick, then climb. First artifact is a no-new-code exemplar-battery calibration (score real PoE/D2/D4/LE frames through the existing instruments to set the tier-marks). This session's white-core finding is exactly the kind of "GREEN-locked but below the genre bar" gap the ladder is built to position.

## RESUME POINTERS

- **Watch the video:** `reincarnated-godot/harness_logs/spellfx_v1_warhall.mp4` (+ the six `spellfx_v1_warhall_0N_*.png` beats). LOCAL / git-ignored (Synty + Binbun derivative IP).
- **Godot code is committed, NOT pushed** (Matt-gated). The V1 war_hall harnesses: `scripts/shoot_spellfx_v1_warhall.gd` / `_seq.gd` + scenes + `run_spellfx_v1.sh`.
- **Stale, non-blocking:** the uncommitted `boss_v1summon_*` files (wrong room) — leave as a reference for the verdict's V1.1 boss-context, or delete; low-stakes cleanup, no decision needed to proceed.
- **The two governing artifacts:** the MARGINAL verdict (`2026-06-18-...-verdict-binbun-backbone.md`) + this in-context adjudication (`2026-06-19-...-v1-warhall-incontext-adjudication.md`). Together they hold the full buy/build evidence chain.

---

**Signed:** gandalf, 2026-06-19. The VFX buy-vs-build question is now answered on two independent legs — the register test (MARGINAL, defer-harvest) and V1 in real descent geometry (PASS in context, the one cost is a cheap in-engine knob). The backbone holds; the harvest stays deferred. The live gate is your rollout call (A/B/C); everything downstream is evidence-gated, not time-gated.
