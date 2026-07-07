# Gate-2 submission — 2026-07-07 — gamora Step-3 REDUX: lived-channel instrument fix + calibration + stratified re-pilot

**To:** jack-ryan (Gate-2, BLOCK authority)
**From:** gamora (simulation seam)
**Engine tag:** `gamora/v-batch2-step3-lived-channel-repilot-1` (HEAD `6468b57`; push HELD — Matt-gated)
**Dispatch:** `dispatches/2026-07-07-gamora-step3-instrument-fix-lived-channel-repilot.md` (Matt instrument-fix ruling A+C authorized, B ruled, TTK-anomaly pre-reg)
**Why Gate-2:** certification-path instrument change (mob-constant calibration + channel fix) per the dispatch.

## What landed (5 commits on `main`)
- `865bc41` — math-before-code note (Disc #1+#24), committed BEFORE any tuning.
- `7164e40` — (A)+(C) channel fix: both builders source `emit_skills_for_threat_tier`; F4 fodder fixed by inheritance; build-smoke + gauntlet_sim docstring doc-fixes; channel-fix smoke.
- `ff8f851` — (B) 7-element wheel + lever(a) F2-lock + lever(b) TTK-anomaly discriminated + F3 STOP-flag (calibration sweep).
- `01439fe` — full stratified re-pilot (40 martial + 2 caster × 7-wheel), miss-taxonomy, caster margins, F-b close.
- `6468b57` — AGENT_STATE checkpoint.

## Diagnosis-to-fix chain (your `38b5a30` endorsed the fix path)
- **(A) Channel fix — DONE.** `_build_standard_mob_dicts` (metrology) + `_build_smoke_four_family._mob` now source the mob `skills` list from `emit_skills_for_threat_tier` (the source `spatial_engine.py:3122` names). Mobs carry a live `"damage"` effect; the typed death channel resolves real damage. Channel-fix smoke proves: live effect per tier; dead dict = 0 kills; lived channel kills with a typed element; dmg/hit positive + monotone (133/531/1851/7506 @ scale 0.05/0.2/1.0/4.0).
- **COERCION FINDING (Disc #11, load-bearing for the sweep):** `mob_damage_scale=0.0` is NOT "off" — `_resolver_skill_from_dict` coerces `dm 0.0 -> 1.0` (`or 1.0`, `spatial_resolver_adapter.py:120`). Sweep grid uses strictly-positive scales; the DEAD dict is the true off witness.
- **(C) F4 fodder — RESOLVED BY INSPECTION.** Continuous-spawn reinforcements clone `mob_dicts[-1]` (`spatial_engine.py:3269`) → the same fix repairs F4 fodder; NO separate F4 code change. Verified live in the smoke + re-pilot (F4 caster escapes 5/5 at scale 0.03, dies 5/5 at native scale 1.0 — fodder is genuinely live).
- **(B) 7-element wheel — kit-invariant.** element@wheel-index `w` = `ROTATING_ELEMENTS[w]` for EVERY kit (only the per-fight seed varies as `base^w`); cert = wheel average; worst-element = diagnostic flag. Verified kit-invariant.

## #24 sweep-isolation result (F2-first / boss-HP-on-TTK / F3-WR-as-readout)
- **Lever (a) F2-LOCKED: mob_damage_scale = 0.03** (F2 wheel-avg WR 0.881 beat / 0.945 full-pop mean, in [0.85,0.95]). Steep cliff (0.025→0.98, 0.03→0.88, 0.035→0.31).
- **Lever (b): boss HP moves TTK** (9.7s @ 6k → 18s @ 9.6M), reaches 15s floor only at ~9.6M HP.
- **F3 WR read LAST: stuck at 1.0 at every boss HP → #24 STOP-AND-FLAG fired.** The monolithic `mob_damage_scale`, locked at 0.03 for F2, defangs the F3 boss (dm 5.0→0.15), so the boss never threatens the kit → WR 1.0; boss HP moves TTK but never WR. Landing F3 WR ∈ [0.60,0.80] needs a THIRD knob (tier-independent `boss_damage_scale`). **Per the dispatch STOP clause: NO third knob added; flagged to knight-rider.** Recommended shape in math note §11.4.

## TTK-saturation mechanism check (Matt pre-registration — falsifiable, all discriminated)
- **H2 timeout-censoring REJECTED** (timeout_rate=0; TTK 9.7–18s << 240s window).
- **H3 heal/regen-race REJECTED** (no boss regen term; boss_final_hp=0 at every HP).
- **H4 resolver DPS-cap REJECTED** (damage_to_boss scales linearly to 9.6M, near-zero overkill).
- **H1-refined CONFIRMED:** TTK dominated by a fixed ~11–13s engage/ramp floor; the martial kit's effective DPS (~90k+) is the binding term, not boss HP. **The saturation was NOT a dead-channel artifact — it persists on the lived channel; it is a DPS-vs-HP-scale mismatch.**

## Full re-pilot (40 martial + 2 caster × 7-wheel × 14 fights, 114s, `pilot_policy=scripted-rotation-v1`)
| Family | Martial pass/n | Caster pass/n | Miss-taxonomy (martial u/oc/wr) |
|---|---|---|---|
| F1 | 25/40 (KPM 45.3, reproduces §7) | 2/2 | 15 / 15 / 0 |
| F2 | 8/40 (mean WR 0.945) | 0/2 | 0 / 20 / 32 |
| F3 | 0/40 (STOP) | 0/2 (STOP) | 40 / 40 |
| F4 | 5/40 (KPM 23.7 < 60 floor) | 2/2 | 35 / 10 / 0 |

- **Caster-PASS MARGINS re-confirmed on the lived channel (verdicts stand per your §7):** F1 both casters WR 1.0 (margin +0.05 above 0.95); F4 both exit 1.0 (+0.20 above 0.80). Caveat: measured at F2-locked scale 0.03 (native 1.0 → caster dies 5/5 on F4); a per-family higher mob-damage could still lower them.
- **F4-martial KPM: MEASURE ONLY** = 23.7 med < 60 floor. Kit response GATED on the pilot-attribution probe (Matt) — NOT fired.
- **F-b closing read: PARITY HOLDS** on F1/F2/F4 → F-b confirm-unneeded criterion MET; F-b retires to git (Matt rules).

## Doc-fix (your Gate-2 WARN, ADR-002 pre-approved)
Three stale pre-flip docstring spans in `gauntlet_sim.py` (`:781-783`, `:833-835`, `:897-898`) corrected to live post-R4-flip behavior.

## Guard / provenance
- **NO kit-side chassis constants touched** (BASE_PHYSICAL/SPELL_DAMAGE_L50, 2.3384× fossil FROZEN). **NO bar/band moved** (fit-direction).
- Room-side mob-damage scalar + boss HP knobs UNFROZEN & used per authorization.
- Sim-internal; reports are new sidecar JSON (`step3-lived-calibration-sweep-v1`, `step3-lived-channel-repilot-v1`) — NO cross-seam persisted field → NO MIGRATION entry (math note §9).
- **pilot_policy stamp:** re-pilot report stamped `pilot_policy=scripted-rotation-v1` (read from your decisions-log entry `8607840`).
- **Regression:** `test_cycle13_wave5_gauntlet_sim` 50/50; build-smoke + channel-fix smoke PASS.

## Asks for Gate-2 + escalation
1. **Verify the channel fix** (both builders + F4-fodder-by-inheritance) and the 7-wheel kit-invariance.
2. **Adjudicate the F3 #24 STOP:** is the third-knob (`boss_damage_scale`) the right resolution, or is there a two-knob path I missed? (My read: the monolithic scalar is structurally insufficient; F3 needs boss/swarm decoupling.)
3. **Escalate to Matt (post-numbers rulings the dispatch defers):** F-b retirement (parity holds), the F3 third-knob authorization, the F2 full-pop re-lock (~0.032–0.035), and whether the F4-martial pilot-attribution probe fires.
