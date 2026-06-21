# mini_boss caster-wipe — DESIGN-HALF ruling ("what is mini_boss FOR")

**Type:** gandalf design-half ruling on the held `mini_boss` column, ahead of a Matt ratification halt.
**Date:** 2026-06-20
**Author:** gandalf (story-and-design steward)
**Requested by:** knight-rider (instrument-validity workstream; design-half of the boss-gate refit).
**Standing instruction (Matt):** this is "gandalf + Matt (do NOT resolve in-session by KR)." I author the ruling; the final "what is mini_boss FOR" call + held-column disposition is Matt's at the halt that follows. I do NOT authorize the fix.

**Read first / composes with:**
- engine half (DECISIVE): gamora `reincarnated-engine/.../math/miniboss-caster-wipe-diagnosis-2026-06-20.md` + data `cycle-14-wave-5-season-001/miniboss-caster-diagnosis-clean-boss-rerun-2026-06-20.json`
- my prior cliff ruling: `gandalf/notes/2026-06-20-boss-gate-inverted-disposition-design-fit-ruling.md`
- doctrine spine §5/§5a: `gandalf/notes/2026-06-19-encounter-measurement-doctrine-spine.md`

**Verdict in one line:** the engine diagnosis CONFIRMS my prior flag — the caster mini_boss cliff is a **stale-calibration DEFECT, same class as the four instrument-validity targets**, not honest texture. The 150s soft_timeout is a dead-absolute-constant left over from a ~3s/KPM~60 DPS regime; against the composed instrument's 125–175s caster kills it functions as a guillotine, not a pacing tool. The held `mini_boss` column does NOT bank as-is. It converts to a confirmed defect requiring a config re-scale + re-measure before banking. **But the "what is mini_boss FOR" identity call is Matt's** — and the fix's exact target depends on which identity he ratifies. I give him a ruled recommendation and the one decision he must make.

---

## RULINGS (1–4)

### 1. What is `mini_boss` FOR? — RULED: "a smaller boss," NOT a burst-window enrage check.

I rule the design intent is **"a smaller boss" — a single-target fight every viable build should be able to clear given a reasonable window** — NOT a solo-DPS-race / enrage gate. Three reasons, in order of weight:

- **The catalog never declared a burst identity that the rest of the system honors.** The `sequence_intent` string says "soft timeout enforces burst-execution pacing," but that is a leftover annotation from the W-α7+ Phase 3c calibration, not a ratified design pillar. No canonical doc, no §5/§5a doctrine, no progression-skeleton beat establishes mini_boss as an enrage check. An enrage check is a deliberate, loud design statement (think Diablo III's Greater Rift guardian timer, or a raid DPS-check phase) — it is never a quiet soft_timeout constant inherited from a tuning pass. If we did not *decide* it was an enrage check, it is not one.

- **The class-fantasy outcome is upside-down, which is the tell.** Under a true burst-window identity, the burst casters (int/wis) are exactly who SHOULD clear it and the slow grind-DPS melee (STR) is who should struggle. The instrument produces the inverse: STR clears flat (1.000), int/wis wipe flat (0.000). A "burst gate" that only the non-burst archetype passes is not a burst gate — it is a broken constant masquerading as one. Naming a defect "intended identity" because it happens to produce a 0.000 does not make it identity (this is the §5/§5a anti-pattern: do not ratify an artifact as texture just because the gate that produced it is wired soundly).

- **It coheres with the rest of the encounter ladder.** `boss_with_adds` runs the full 240s with no soft cut — it is "the boss." If `mini_boss` is "a *smaller* boss," the player's reasonable expectation is that it is EASIER or equal, clearable by the same builds that clear the full boss. A mini-boss that is mechanically HARDER than the full boss for two of four attribute archetypes violates the most basic naming-contract a player reads off the word "mini." (Diablo's champion/unique mobs are *smaller* threats than act bosses; nobody ships a "mini" that out-walls the real one.)

**This is the call I am handing Matt to ratify.** If Matt instead rules that mini_boss IS intended as a burst-window enrage check, my ruling on (2)/(3) changes — see the fork in (3). But absent an explicit Matt decision to MAKE it an enrage check, the default-correct reading is "smaller boss," and the timeout is a defect.

### 2. HONEST TEXTURE or DEFECT? — DEFECT. Both sub-findings adjudicated against the workstream's own discipline.

**(a) The 150s soft_timeout — YES, this is the SAME class as the four instrument-validity defects.** This is the load-bearing adjudication. The whole instrument-validity workstream exists to find **dead-absolute-constants whose meaning has drifted out from under them** — predicate values calibrated to a regime that no longer obtains (the KPM band, the 600@0.3s timing floor, the over-performance ceiling, the boss KPM gate). The 150s soft_timeout is textbook member of that class:

- It was set in W-α7+ Phase 3c to a calibration that explicitly assumed "mini_boss fight ~3.0s at Balanced-cohort DPS → KPM ~60." That is a regime where kills happen in *seconds*.
- The composed instrument's caster kills happen in **125–175s** — two orders of magnitude slower than the calibration assumed.
- A timer set to allow a 3s kill, applied to a 160s kill, is not measuring "did you burst fast enough." It is measuring nothing the designer intended — it is a stale constant that no longer means what it meant when it was set. **That is the exact failure signature this workstream was chartered to kill.** Banking it as "intended" would be the instrument lying again, on the same axis, one shell over.

**(b) mini_boss HP rolling ABOVE the full boss — CONFIG INVERSION, not coherent design.** mini_boss HP rolls 190–290k (mid 240k, upper 290k); boss rolls 210–252k (mid 231k, upper 252k). The "mini" boss's MID exceeds the boss's MID and its UPPER exceeds the boss's UPPER. mini_boss armor is lower, so HP is unambiguously the wall. This HP was raised in W-α7+ Phase 3c "for T4 peak achievability" — a generation-side reach for a tier target that incidentally pushed the mini above the full boss. There is no design world where "mini" should carry more HP than "boss." It is an inversion produced by a tuning pass optimizing one axis (T4 achievability) without checking the cross-shell coherence axis. **Coherent design would floor mini_boss HP at or below boss HP by construction; the current config does not, and that is a config inversion, not texture.**

The two findings compound: equal-or-higher HP to remove, in 62% of the time. The casters are a hair-to-far short of a kill the timer won't let them finish. That is not difficulty — that is two stale constants multiplying.

### 3. Disposition of the held `mini_boss` column — DOES NOT BANK as-is. Convert to confirmed defect → re-scale + re-measure → THEN bank. (Matt ratifies first.)

The held column does **not** bank as honest texture. The engine diagnosis converts my prior candidate-defect flag into a **confirmed stale-calibration defect.** Disposition: HOLD remains, escalated to "confirmed defect requiring fix + re-measure before bank."

**The fix (FLAGGED — needs Matt's design ratification first; I do NOT authorize it):**

- **Owner:** gamora (simulation/scenario config — soft_timeout and HP ceiling both live in the scenario/stat-profile layer she diagnosed: `spatial_engine.py:1684-1696`, `endgame_mob_stat_profile.py` / `endgame_encounter_catalog.py` HP-factor range).
- **Recompose-first scope (Discipline #-aligned):** do NOT hand-tune to make the casters pass. Re-scale the two stale constants to their *coherent* values, then RE-MEASURE the full caster×shell grid on the composed instrument and read whatever disposition falls out — bank that, defect-free:
  1. **soft_timeout:** raise to match the composed-instrument kill-window the constant was meant to bound. Candidate: align mini_boss to the same 240s as boss_with_adds (simplest coherent value — "smaller boss, same window"), OR set a soft_timeout meaningfully above the measured caster TTK ceiling (~176s wis) if a *modest* pacing pressure is still wanted. Matt's identity call (finding 1) picks which.
  2. **HP ceiling:** floor mini_boss HP at or below boss HP. Candidate: cap the HP-factor upper at boss's (≤12.60 → ≤252k) so "mini" is never larger than "boss." If T4-achievability still needs the headroom, solve it on a non-inverting axis (boss HP too, or a tier-scalar), not by making the mini exceed the boss.
- **Empirical criterion that closes the defect:** re-measured caster×shell grid where the caster mini_boss disposition is a *defensible graded outcome* (or a clean pass) explainable WITHOUT reference to a stale timer — i.e., the cross-shell story is coherent (casters clear or gradiently struggle on mini_boss the way they do on boss_with_adds; STR is no longer the *only* archetype that clears mini_boss). The flag closes when the inversion is gone, not when the casters merely pass.

**THE FORK MATT OWNS (this is the one decision the fix's target depends on):**

- **If Matt rules "smaller boss" (my recommended default):** re-scale BOTH constants → mini_boss becomes a coherent single-target fight ≤ the full boss → re-measure → bank. Soft_timeout likely → 240s (or removed); HP capped at ≤ boss.
- **If Matt rules "intended burst-window enrage check":** then the casters failing 150s is *honest by design* — BUT two reconciliations become MANDATORY before banking, per gamora's framing (C): (i) the HP inversion is STILL a defect even under this identity (a burst check should not also carry more HP than the full boss — fix HP regardless); and (ii) we must explicitly reconcile + ratify "the same casters that clear the 240s full boss cannot burst the 150s mini in time, and that is the intended skill expression" as a LOUD, documented design pillar — not a quiet pooled number. An enrage check is a deliberate statement; if Matt wants one, it must be designed as one (telegraphed timer, player-legible, and the HP fixed so the *only* lever is speed, not a hidden HP wall).

**Either fork requires the HP inversion fixed.** Only the soft_timeout value forks on Matt's identity call.

### 4. Phase-6 / cross-cutting implications.

- **STR-via-raw-throughput banked result — UNAFFECTED, and this defect actually firms it up.** gamora's diagnosis shows STR is *shell-insensitive*: its composed rage economy (~48k DPS) kills in ~15s, never approaching either timeout. STR clears mini_boss for the same reason it clears boss_with_adds — raw throughput, not a timer-gaming trick. So the STR banked result does NOT depend on the mini_boss config at all; re-scaling soft_timeout/HP will not move STR. (Mild upside: once the casters' mini_boss numbers are de-contaminated, the §5a "STR ships boss shells" reading is fully trustworthy rather than half-trustworthy — closes the empirical criterion I put on the §5a falsification amendment in my prior ruling.)

- **Post-workstream absolute-magnitude-constant sweep — ADD the 150s soft_timeout AND the mini_boss HP-factor range to that sweep's target list.** This defect is the clearest evidence yet that the planned absolute-magnitude-constant sweep is correctly scoped: the soft_timeout is a magnitude constant that drifted exactly like the KPM band did. Both stale constants surfaced here should be explicit line-items in that sweep so the same drift is caught system-wide, not just patched on this one shell. The pattern — "a tuning pass (W-α7+ Phase 3c) set a constant for a local target (T4 achievability) and silently broke a cross-shell coherence invariant" — is the generalizable lesson; the sweep should look for *other* Phase-3c-era constants with the same provenance.

- **Doctrine spine §5a:** my prior amendment gated "STR ships boss shells" final-trustworthiness on the mini_boss cliff being diagnosed. It is now diagnosed (defect, not contamination of STR). Once the re-measure lands, the §5a amendment stamps final. No new doctrine needed; this ruling is the diagnosis the criterion asked for.

---

## The single crisp recommendation for KR → Matt halt

> **The engine half is in and it confirms the flag: the caster mini_boss wipe is a stale-calibration DEFECT, not honest texture — it is the same class as the four instrument-validity targets.** Casters are NEVER killed on mini_boss (a_dead=0, 100% timeouts); they kill the full boss in 125–175s but a leftover **150s soft_timeout** — set in W-α7+ Phase 3c for a ~3s/KPM~60 regime two orders of magnitude faster than today's caster kills — guillotines them, against a "mini" boss whose **HP rolls ABOVE the full boss** (mid 240k vs 231k, upper 290k vs 252k). Two stale constants multiplying: more HP to remove, in 62% of the time. STR clears both because its ~48k DPS kills in 15s, timer-insensitive — which is exactly why a "burst gate" only the non-burst class passes is a broken constant, not an identity.
>
> **gandalf's design ruling: mini_boss is "a smaller boss" (clearable by viable builds given a reasonable window), NOT a burst-window enrage check.** Under that intent, the held `mini_boss` column does NOT bank as-is — it converts to a confirmed defect: **re-scale soft_timeout (→ 240s / align to boss) + floor mini_boss HP at ≤ boss HP, then re-measure the caster×shell grid and bank whatever coherent disposition falls out.** Owner gamora, recompose-first (do NOT hand-tune to a pass), criterion = the inversion is gone (STR no longer the only archetype clearing mini_boss).
>
> **The ONE decision that is yours, Matt:** ratify the identity. If "smaller boss" (recommended) → fix both constants, re-measure, bank. If you instead want mini_boss to BE a burst-window enrage check → say so explicitly and we design it as a loud, player-legible timer — but the HP inversion gets fixed either way, and "casters can't burst the 150s mini but can kill the 240s full boss" becomes a documented design pillar, not a quiet pooled number. **The fix is NOT authorized until you make this call.**

---

**Signed:** gandalf, 2026-06-20. The instrument stopped lying about STR; it had started lying about casters on one shell, exactly as the cliff predicted. The engine half names the two stale constants. A "mini" boss harder than the boss, gated by a timer set for a fight 50× faster than the one being run — that is two dead constants, not a design. Fix the constants, re-measure, bank it honest. The identity call is yours.
