# Dispatch — 2026-07-07 — gamora — Step 3 completion: F3 tier-independent boss_damage_scale + full-pop F2 re-lock + genre-sane boss HP

**From:** knight-rider
**To:** gamora (simulation seam — `spatial_gauntlet/`, `gauntlet_sim.py`, metrology + re-pilot drivers)
**Approved by:** Matt 2026-07-07 (ruling on the four Step-3 decision points — verbatim below)
**Estimated effort:** medium–multi-day (one new tier-scoped knob + F2 re-lock + genre-sane boss-HP + re-pilot under one seed stream; analysis-moderate — the channel is already live, this closes the F3 STOP)
**Acceptance:** the F3 (and mini-boss) certification lands in-band via a **tier-independent `boss_damage_scale` scoped to boss/mini-boss tiers ONLY**, F2's `mob_damage_scale` is re-locked on the full stratified population, F3 boss HP is set at a **genre-sane ratio** (NOT swept to force TTK), the full four-family re-pilot re-runs under ONE seed stream, and dispositions follow Rider-3 semantics (floor = hard line; ceiling / over-band = overpowered flag → balance review, NOT auto-fail).

## Context — closing the second #24 STOP

Your lived-channel re-pilot (`6468b57`, Gate-2 PASS-WITH-FOLLOWUPS `9ecccff`) fixed the dead channel and locked F2, but F3 hit a second #24 STOP: the **monolithic `mob_damage_scale` couples boss (dm 5.0) and swarm (dm 0.85)**, so the F2-lock 0.03 defangs the F3 boss (→0.15) and F3 WR pins at 1.0 across boss HP 150k→9.6M. jack-ryan's Gate-2 determination: this is a **rank-deficiency — one scalar cannot serve both a low-competency F2 swarm chip AND a threatening F3 boss; there is no two-knob path.** The tier-independent `boss_damage_scale` is the clean, minimal resolution and stays inside fit-direction (a room knob, not a bar/kit move). Also confirmed: the TTK saturation is a **real DPS-vs-HP mismatch (DPS-bound, ~11–13s engage floor + ~90k kit DPS), NOT a dead-channel artifact.**

## Matt's ruling (VERBATIM — binding)

> **Authorize (1) — boss_damage_scale, boss/mini-boss tier only.** Retire (2) — F-b to git with the parity statement; jack-ryan logs the arc. On (3): register as chassis-evidence #1 for the loot-campaign rebalance alongside the F2-cliff defense finding; boss HP set at genre-sane ratio; the TTK overpowered flag stands population-wide; nothing unfreezes. Accept (4) with the fold, and confirm F2 WR-over-band disposes as flag-pass per Rider 3, not fail.

**What this dispatch executes (1) + (4). (2) and (3) are jack-ryan's decisions-log lane — NOT your scope here** (F-b retirement + chassis-evidence-#1 registration are being routed in parallel).

Unpacked for your scope:
- **(1) `boss_damage_scale` — tier-scoped to boss + mini-boss ONLY.** Introduce a tier-independent boss/mini-boss damage scalar decoupled from the swarm `mob_damage_scale`. It applies to the **boss and mini-boss tiers only** — trash/swarm/champion tiers keep the F2-locked `mob_damage_scale`. Tune `boss_damage_scale` so **F3 WR ∈ [0.60, 0.80]** on the stratified population.
- **Boss HP at a GENRE-SANE RATIO (Matt (3) — binding on your scope):** do **NOT** sweep boss HP to force TTK into the 15–90s band (the 9.6M figure is absurd and rejected). Size F3 boss HP at a **genre-sane ratio** (document the ratio basis — e.g., boss HP relative to trash HP / to expected kit DPS per ARPG-genre norm). **The resulting TTK-under-15s is a STANDING overpowered flag, population-wide — recorded, routed to balance review, NOT auto-fail, NOT a reason to inflate HP.** Nothing kit-side unfreezes.
- **(4) F2 full-pop re-lock + fold:** re-lock F2 `mob_damage_scale` on the **full 40-kit stratified population** (§12.3 flagged ~0.032–0.035 vs the beat-locked 0.03 which sits at the band-ceiling edge). Fold this INTO this re-run under **one seed stream** (jack-ryan's sequencing note).
- **F2 WR-over-band disposition (Matt (4) — confirmed):** if F2's full-pop mean WR lands at/over the band ceiling after best-effort re-lock, it disposes as a **flag-pass per Rider 3 (overpowered flag → balance review), NOT a certification fail.** Encode this disposition; do not auto-fail F2 on an over-band WR.

## Required reading before starting
- Your lived-channel math note `simulation/math/step3-lived-channel-calibration-repilot-2026-07-07.md` (§12.3 the F2 re-lock note; the F3 STOP analysis; the TTK mechanism finding) + re-pilot driver `simulation/gauntlet_lived_channel_repilot_driver.py` + report `simulation/output/gauntlet_lived_channel_repilot/lived_channel_repilot_report.json`.
- jack-ryan Gate-2 finding `qa/findings/2026-07-07-gamora-step3-lived-channel-repilot-gate2.md` (the rank-deficiency determination + the cosmetic miss-taxonomy INFO defect to fix).
- The mob-skill emitter `spatial_engine.py:3122` `emit_skills_for_threat_tier` (tier params — boss dm 5.0, swarm dm 0.85) — where the tier-scoped scalar attaches.
- `spatial_resolver_adapter.py:118` (the `or 1.0` coercion — keep the strictly-positive-scale discipline; a tier scalar of 0.0 would alias to native, so guard it).
- `canonical/reap-die-rise-engine/gauntlet-run-beat-families-spec.md` §3 (F3 bars/bands — FIXED), §5 (headroom law); metrology note §8 (Rider-3 miss-taxonomy semantics: floor=hard, ceiling=overpowered-flag→review).
- Run-state `batch2-run-state-2026-07-06.md` — gamora Step-3 REDUX RESULT block + Matt's 4-decision ruling.

## Math-before-code (Discipline #1 + #24 — document BEFORE tuning)
- **The tier-scoped knob:** how `boss_damage_scale` attaches to boss + mini-boss tiers ONLY (and provably does NOT touch trash/swarm/champion — no leakage into the F2 lock); the strictly-positive guard (0.0 would alias native via the `or 1.0` coercion).
- **#24 isolation (now cleanly separable):** F2 swarm scale and F3 boss scale are now ORTHOGONAL knobs — document that decoupling resolves the rank-deficiency, and the sweep order (re-lock F2 on full pop first, then sweep `boss_damage_scale` for F3 WR ∈ [0.60,0.80], boss HP fixed at the genre-sane ratio). Confirm no residual coupling.
- **Genre-sane boss-HP ratio:** state the ratio + its basis; register the resulting TTK + the standing population-wide overpowered flag (do NOT tune HP to the TTK band).
- **Rider-3 disposition schema:** floor = hard cert line; ceiling / over-band = overpowered flag → balance review (F2 WR-over-band = flag-pass, NOT fail); the F3 TTK-under-15s = standing overpowered flag.
- **Resource-bounds (Disc #1.1):** re-pilot peak entities + run cost.

## Cross-seam contract change? (Principle 6 gate)
- Tier-scoped mob-damage knob + F2 re-lock + boss HP: **sim-internal room-side constants; no cross-seam field change expected.** If any persisted field changes, MIGRATION.md + round-trip.
- Cert output continues to carry `pilot_policy=scripted-rotation-v1` (jack-ryan `8607840`).

## Scope
- [ ] **Math-before-code note first** (all bullets above), committed before tuning.
- [ ] **(1) tier-independent `boss_damage_scale`** scoped to boss + mini-boss ONLY; tune F3 WR ∈ [0.60, 0.80] on the stratified population; prove no leakage into swarm/trash/champion (F2 lock unaffected).
- [ ] **(4) F2 full-pop re-lock** of `mob_damage_scale` (~0.032–0.035 candidate); folded into this re-run under ONE seed stream.
- [ ] **Genre-sane F3 boss HP** (document ratio); TTK-under-15s recorded as a STANDING population-wide overpowered flag (NOT HP-inflated, NOT auto-fail); nothing kit-side unfreezes.
- [ ] **Full four-family re-pilot** re-run under one seed stream; stratified caster+martial; certification dispositions per Rider 3.
- [ ] **F2 WR-over-band = flag-pass per Rider 3** (encode; do not auto-fail).
- [ ] **Caster-margin re-confirm** on the new F2 scale + on F3 now that the boss threatens (F3 was excluded as STOP last run — casters now get real F3 numbers).
- [ ] **Cosmetic INFO fix (jack-ryan):** `_miss_taxonomy` mislabels over-band saturation as `wr_under_band` for kpm_band families (disp dict lacks a `wr` key) — correct the label.
- [ ] AGENT_STATE.md updated; MIGRATION.md only if a boundary is touched.
- [ ] Tag: `gamora/v-batch2-step3-f3-boss-scale-1`.
- [ ] **Submit tagged commit to `agentic_orchestration/qa/pending/` for jack-ryan Gate-2** (new certification-path knob + re-lock).

## Out of scope (FROZEN / deferred)
- **NO kit-side chassis constant changes** — Matt: "nothing unfreezes." The TTK-DPS mismatch is chassis-evidence #1 for the FUTURE loot-campaign rebalance (jack-ryan registers it), NOT a now-fix. Do not touch BASE_PHYSICAL/SPELL_DAMAGE_L50 or kin.
- **NO bar or band moves** (fit-direction — F3 bars fixed; you tune the room knob to the bar).
- **NO boss-HP inflation to force the TTK band** (genre-sane ratio + standing flag instead).
- **NO F-b work** — F-b retires to git via jack-ryan's decisions-log (parallel); do not re-open it.
- **NO F4-martial fix** — kit-side, gated on the pilot-attribution probe, deferred.
- **NO Leg C** — HELD until this completes + Matt rules.
- **NO new tier scalar beyond boss/mini-boss** — trash/swarm/champion stay on the F2-locked `mob_damage_scale`.

## References
- Matt 4-decision ruling 2026-07-07 (verbatim above)
- gamora lived-channel re-pilot (`6468b57`); jack-ryan Gate-2 (`9ecccff`, finding above); decisions-log canon (`8607840`)
- Spec `gauntlet-run-beat-families-spec.md`; metrology note; Disciplines #1, #1.1, #11, #12, #24; fit-direction law; Rider-3 miss-taxonomy semantics
- Run-state `batch2-run-state-2026-07-06.md`
