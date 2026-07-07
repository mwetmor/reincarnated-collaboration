# Finding — 2026-07-07 — gamora Step-3 REDUX (lived-channel instrument fix + calibration + stratified re-pilot)

**Reviewer:** jack-ryan
**Severity:** PASS-WITH-FOLLOWUPS (one INFO taxonomy-label defect; the F3 STOP + F2 re-lock + F4-probe are correctly-escalated design decisions, not review blocks)
**Target:** tag `gamora/v-batch2-step3-lived-channel-repilot-1` = HEAD `6468b57`
**Developer:** gamora (simulation seam)
**Principles applied:** Review #1 (math-before-code), #2 (smoke-gate), #3 (cross-seam impact), #4 (decisions-log as truth), #5 (severity). Disciplines #1, #1.1, #2, #3, #11, #12, #24. Fit-direction law. one-pilot-policy contract. ADR-002 (doc-fix tier), ADR-004 (MIGRATION).

---

## What I found

Certification-path instrument change. I verified every load-bearing claim against source and independently re-ran the calibration sweep beat (45.7 s) and the regression suite. The dead mob-damage channel is genuinely repaired at BOTH builders; the coercion finding, the F4-by-inheritance claim, the 7-wheel kit-invariance, the F2 lock, the TTK-DPS-bound mechanism, and the F3 STOP all reproduce and hold under scrutiny. The re-pilot report matches its submission tables byte-for-byte on the load-bearing numbers. One cosmetic taxonomy-label defect (F2 over-band saturation mislabeled `wr_under_band`); it touches no cert, verdict, or the F-b read. No bar/band moved, kit chassis FROZEN, no MIGRATION (correctly — the mob-dict `skills` list is an in-memory `run_spatial_fight` input, not a persisted field). Tag → HEAD confirmed. pilot_policy stamp matches the decisions-log string.

## Verification log (independent)

**(1) Channel fix (A)+(C) + coercion — CONFIRMED at source.**
- `_build_standard_mob_dicts` (`gauntlet_four_family_metrology_driver.py:203`) and `_build_smoke_four_family._mob` (`_build_smoke_four_family.py:54-59`) both source `skills` from `emit_skills_for_threat_tier`. Verified.
- **F4-by-inheritance claim SOUND.** `spatial_engine.py:3269` `_spawn_template_dict = mob_dicts[-1]` — the reinforcement template is literally the last dict from the fixed builder. Reinforcements clone the fixed dict, not a separately-built damage-less one. The claim that the same fix repairs F4 fodder holds by construction. Confirmed the same `_has_spawner` path covers both F4 continuous-spawn and F3 timed add-waves.
- **Coercion finding (Disc #11) REAL and load-bearing.** `spatial_resolver_adapter.py:118`: `float(skill_dict.get("damage_multiplier", 1.0) or 1.0)`. A computed `dm=0.0` (what `mob_damage_scale=0.0` produces via `_mob_skills_for_tier`) is falsy → coerced to 1.0. So scale 0.0 aliases the NATIVE dm, not off. The sweep grid uses strictly-positive scales (`[0.02..1.0]`) and treats the dead dict as the true-off witness — correct. This retro-validates the earlier "0.0 readings" caution: any prior "scale 0.0 = off" reading would have been mis-stated; gamora caught it before it contaminated the calibration.

**(2) Calibration + wheel — CONFIRMED, independently reproduced.**
- Re-ran `gamora_step3_lived_calibration_sweep --beat`: F2 lock `mob_damage_scale=0.03` (IN_BAND, pop wheel-avg WR **0.8809**), steep cliff reproduced (0.025→0.976, 0.03→0.881, 0.035→0.31). Lock is sound: 0.03 is the band member closest to the 0.90 midpoint.
- **Wheel kit-invariance CONFIRMED.** `gamora_step3_lived_calibration_sweep_...:58-63`: element = `ROTATING_ELEMENTS[w]` for every kit; per-element seed = `base_seed ^ (w * 0x9E3779B1)` — the wheel perturbation carries no kit identity. The schedule is a pure function of `(family, wheel_index)`. Cert = pooled wheel average; worst-element recorded as `worst_element` diagnostic, not gated. Matches Matt's Ruling B exactly.

**(3) TTK-DPS-bound finding — DISCRIMINATION SOUND, conclusion CORRECT.** See determination below.

**(4) F3 #24 STOP — the crux.** See determination below. Boss-defang arithmetic verified empirically: `_mob_skills_for_tier('boss', 0.03, 'fire')` → dm **0.15** (5.0×0.03); swarm → 0.0255. The monolithic-scalar coupling is real.

**(5) F-b retirement.** See determination below.

**(6) Calibration-precision note (§12.3):** CONFIRMED a precision refinement, not a bar/kit change. The beat-lock 0.03 gives the full-40-kit-pop F2 **mean** WR 0.945 — inside [0.85,0.95] on the certification statistic (the mean/wheel-average) but riding the ceiling edge with median saturated at 1.0. The recommended ~0.032–0.035 re-lock moves the sweep's operating point within the same steep cliff, touching no bar and no kit constant. It SHOULD fold into the F3 third-knob re-run (do the full-pop re-lock and the boss-decouple in one calibration pass, not two — the F2 swarm chip and the new boss knob are then co-locked on the full population under one seed stream).

**(7) Scope/regression — CONFIRMED.** `test_cycle13_wave5_gauntlet_sim` 50/50 (re-run). Channel-fix + build smokes referenced PASS (commit `7164e40` records them). Docstring WARN resolved: the three stale pre-flip spans in `gauntlet_sim.py` now narrate post-R4-flip behavior (verified in the diff — "R4 flip FIRED 2026-07-07"). No bar/band moved; chassis constants FROZEN; no MIGRATION (sim-internal in-memory input + new sidecar JSON). pilot_policy stamp `pilot_policy=scripted-rotation-v1` matches the decisions-log entry `8607840`.

## INFO — miss-taxonomy label defect (non-blocking, cosmetic)

`gauntlet_lived_channel_repilot_driver.py::_miss_taxonomy` (`:84-86`) reads WR via `disp.get("wr", disp.get("win_rate"))`. For `kpm_band` families (F1/F2), `_bar_disposition` (`:281-292`) writes NEITHER `"wr"` nor `"win_rate"` into the disposition — only `wr_in_band`. So `wr` resolves to `None`, the `side` ternary falls through to `"under"`, and F2's WR=1.0 (which is ABOVE the 0.95 ceiling → over-band saturation) is mislabeled `wr_under_band`. The report's F2 martial `wr_side` count (32) and the caster F2 `wr_under_band` are directionally inverted. **This changes NO verdict** — `passes_bar` is computed independently and correctly (F2 fails because WR ∉ band, which is true either way), and the F-b parity read keys off WR medians (not the taxonomy label), so it is unaffected. It is a reporting-clarity defect only. Fix: in `_bar_disposition`'s `kpm_band` branch, write `disp["wr"] = wr` so the taxonomy can read the side; or read `kit_result` WR directly in `_miss_taxonomy`.

---

# Determinations for Matt (the three escalation inputs)

## (4) F3 #24 STOP — determination

**(a) The STOP was CORRECT.** The dispatch #24 clause is explicit: read F3 WR LAST as an output; if it misses [0.60,0.80] after (1)+(2), that is a finding → STOP, do NOT add a third knob. F3 WR is stuck at 1.0 at every boss HP 6k→9.6M. gamora stopped, added no third knob, and flagged. Textbook Discipline #24 compliance. The alternative — quietly adding a boss knob to force F3 into band — would have been tuning the instrument to a target reading, the exact anti-pattern #24 exists to prevent.

**(b) A tier-independent `boss_damage_scale` IS the clean, minimal resolution; there is no two-knob path.** I verified the mechanism at source: `mob_damage_scale` is a single multiplicative scalar applied to the emitter's per-tier `damage_multiplier` in `_mob_skills_for_tier` (`:223-225`), so it multiplies boss (5.0) and swarm (0.85) together. The two authorized knobs are (a) this monolithic damage scalar and (b) boss HP. Boss HP moves TTK but cannot move WR (a boss that deals 0.15-dm damage never kills the kit regardless of how long it lives — verified: `boss_final_hp=0` at every HP, WR 1.0 throughout). So the two-knob surface has a structural degeneracy for F3: F2 competency demands a LOW scalar (0.03); an F3 boss that threatens the kit demands a HIGH boss multiplier. One scalar cannot satisfy both. No re-parameterization of the existing two knobs escapes this — it is a rank-deficiency, not a search-failure. The decoupled `boss_damage_scale` (applied only to boss/mini-boss tier in the builder) is the minimum-rank addition that makes the F3 WR controllable. gamora's read ("structurally insufficient") is correct.

**(c) A per-tier boss scale STAYS INSIDE the fit-direction law.** The law is: tune ROOMS to BARS, never BARS to KITS. `boss_damage_scale` is a room-side instrument knob (mob lethality), exactly like `mob_damage_scale` and `boss_hp` which the dispatch already unfroze. It does not move a bar (F3 WR ∈ [0.60,0.80] stays fixed), does not touch a kit chassis constant, and does not fit a bar to a kit. It gives the F3 room a lethality lever the monolithic scalar structurally denied it. This is repairing the instrument's degrees of freedom to MATCH the bar, which is the correct direction. Recommend Matt authorize it — as a NEW calibration knob it is a scope decision above seam authority, correctly escalated (ADR-002).

**Recommended sequencing:** fold (c) with the §12.3 full-pop F2 re-lock into ONE calibration pass — co-lock the swarm `mob_damage_scale` (~0.032–0.035, full-pop) and the new boss `boss_damage_scale` (to land F3 WR ∈ [0.60,0.80]) under a single seed stream. Doing them separately risks the F2 lock drifting the F3 read.

## (5) F-b retirement robustness — determination

**LEGITIMATE. F3 exclusion does NOT undercut the F-b conclusion.** F-b's question is narrow: is there a SYSTEMATIC caster-vs-martial WR asymmetry beyond the 2-cell caster sample? The parity check (`_fb_parity_read:301`) flags divergence at `|WR_median_martial − WR_median_caster| > 0.35` per family. F1/F2/F4 all show martial and caster WR medians at 1.0 (delta 0) — no asymmetry. F3 is excluded not to hide a divergence but because the two-knob calibration cannot produce a MEANINGFUL WR there (both classes saturate at 1.0 for the SAME reason — the defanged boss — so F3 would show delta 0 too, i.e. it would only re-confirm parity, never refute it). Excluding a cell that can only agree does not weaken a parity conclusion. The F1/F2/F4 evidence is sufficient: three families, both classes, no asymmetry.

**The caveat does NOT threaten the retirement, but bounds it honestly.** The caster margins (F1 WR 1.0 +0.05; F4 exit 1.0 +0.20) are re-confirmed at the F2-locked lenient scale 0.03; at native scale 1.0 the caster dies 5/5 on F4. So the margins are scale-conditional. BUT F-b asks about caster-vs-martial PARITY, not absolute caster survivability. At the calibrated scale both classes are measured on the same instrument and show no asymmetry. A per-family higher mob-damage would lower BOTH classes' margins (it is a room lethality knob, class-agnostic) — it does not asymmetrically favor martial over caster. So the caveat is a note on absolute margin fragility (relevant to the future F4-specific lethality knob), not a parity confound. The parity conclusion is robust to it. **F-b confirm-unneeded criterion is MET; retirement to git is legitimate — Matt rules.** One honest bound to carry forward: parity is confirmed on 3 families at one calibrated scale with a 2-cell caster sample; if a future per-family lethality knob lands, re-read caster margins then (not a re-open of F-b, a margin re-confirm).

## (3) TTK-DPS-bound finding — determination

**DISCRIMINATION SOUND; CONCLUSION CORRECT.** The four hypotheses were pre-registered in the math note BEFORE the lived sweep (committed `865bc41`, Disc #1) with an explicit discriminating measurement for each — falsifiable, not post-hoc. I checked the discrimination logic:
- **H2 (timeout-censoring) REJECTED** correctly: `timeout_rate=0.00` at every HP; TTK 9.7–18 s sits far below the 240 s window, so there is no high-tail being censored out of the won-mean. Sound.
- **H3 (heal-race) REJECTED** correctly: `_boss_has_regen()` inspects the boss `combatant_state` for regen fields and returns False; `boss_final_hp=0` at every HP (boss always dies). No unkillable threshold. Sound — verified the discriminator reads the actual entity, not an assumption.
- **H4 (DPS-cap) REJECTED** correctly: `damage_to_boss` scales linearly to 9.6M with near-zero overkill; if a per-hit/tick cap existed, TTK would grow linearly with HP (it does, weakly) — but the ABSENCE of a cap is shown by the linear damage accumulation with no plateau. Sound.
- **H1-refined CONFIRMED:** TTK is monotone-non-decreasing in HP (I re-ran: `monotone=True`) but dominated by a fixed ~11–13 s engage/ramp floor; the martial kit's ~90k effective DPS means boss HP only registers on TTK at millions (15 s floor reached at ~9.6M HP). This is the residual after H2/H3/H4 are eliminated, and the linear-damage + monotone-TTK signature is consistent with it. Sound.

**The conclusion (TTK is DPS-bound, NOT a dead-channel artifact; saturation persists) is CORRECT.** The prior worry was that the TTK saturation seen on the dead channel might be a channel artifact that would dissolve once mobs retaliated. It did not dissolve — it reproduces on the lived channel. The mechanism is a DPS-vs-HP-scale mismatch: the kit kills too fast for boss HP to be the binding term on TTK, and boss damage (defanged to 0.15) never threatens the kit, so WR stays pinned at 1.0. This is exactly why the F3 STOP (4) is a structural finding and not a calibration miss: the boss cannot threaten via HP (WR-inert) and cannot threaten via the monolithic damage scalar (F2-locked low) — it needs the decoupled boss-damage knob. The TTK finding and the F3 STOP are the same rank-deficiency seen from two angles, and both reads are correct.

---

## Rationale

Review #1 (math-before-code): the hypothesis set + #24 isolation plan were committed pre-tuning (`865bc41`) — verified. Review #2 (smoke-gate): channel-fix smoke proves the repair with a dead-dict regression witness. Review #4 (decisions-log as truth): pilot_policy stamp read from the canonical string, not invented. Discipline #24: the STOP is the discipline operating correctly, not a failure. Discipline #11: coercion + F4-clone + damage-path all read from source, not asserted. Fit-direction: no bar moved; the proposed boss knob tunes the room to the bar. The one INFO defect is a reporting-label inversion with zero cert/verdict impact.

## Action
- [ ] Developer (gamora, INFO — within-seam, no re-tag required): write `disp["wr"] = wr` in `_bar_disposition`'s `kpm_band` branch (or read WR directly in `_miss_taxonomy`) so F2/F1 over-band saturation labels as `wr_over_band`. Cosmetic; fold into the F3 third-knob re-run commit.
- [ ] Matt (ESCALATE — authorize): the tier-independent `boss_damage_scale` third knob for F3 (my determination: clean, minimal, fit-direction-compliant — see (4)).
- [ ] Matt (ESCALATE — rule): F-b retirement to git (my determination: legitimate, robust to the F3 exclusion and the caster-margin caveat — see (5)).
- [ ] Matt (ESCALATE — rule): whether the F4-martial pilot-attribution probe fires (dispatch-gated; not a review item).
- [ ] Matt/knight-rider (sequencing note): fold the §12.3 full-pop F2 re-lock (~0.032–0.035) INTO the F3 third-knob re-run — co-lock swarm + boss knobs on the full population under one seed stream, not two passes.

## References
- Submission: `agentic_orchestration/qa/pending/2026-07-07-gamora-step3-lived-channel-repilot-gate2.md`
- Dispatch: `agentic_orchestration/dispatches/2026-07-07-gamora-step3-instrument-fix-lived-channel-repilot.md`
- Math note: `reincarnated-engine/src/reincarnated/simulation/math/step3-lived-channel-calibration-repilot-2026-07-07.md`
- Sweep: `reincarnated-engine/src/reincarnated/simulation/scripts/gamora_step3_lived_calibration_sweep_2026_07_07.py`
- Re-pilot driver: `reincarnated-engine/src/reincarnated/simulation/gauntlet_lived_channel_repilot_driver.py`
- Report: `reincarnated-engine/src/reincarnated/output/gauntlet_lived_channel_repilot/lived_channel_repilot_report.json`
- Builders verified: `gauntlet_four_family_metrology_driver.py:161-226`; `spatial_gauntlet/_build_smoke_four_family.py:47-65`
- Coercion: `spatial_gauntlet/spatial_resolver_adapter.py:118`; F4 clone: `spatial_gauntlet/spatial_engine.py:3269`; emitter shapes: `generation/typed_monster_skills.py:57,68-87`
- Predecessor Gate-2 (diagnosis confirm): `qa/findings/2026-07-07-gamora-step3-mob-lethality-calibration-r4-flip-gate2.md`
- decisions-log pilot_policy stamp: entry `8607840`
