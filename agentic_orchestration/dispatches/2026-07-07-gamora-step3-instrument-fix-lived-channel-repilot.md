# Dispatch — 2026-07-07 — gamora — Step 3 (redux): dead-channel instrument fix + lived-channel calibration + stratified re-pilot

**From:** knight-rider
**To:** gamora (simulation seam — `spatial_gauntlet/`, `gauntlet_sim.py`, metrology driver)
**Approved by:** Matt 2026-07-07 (instrument-fix ruling: A + C authorized; B ruled; TTK-anomaly pre-registration required — verbatim below)
**Estimated effort:** multi-day (channel fix + pre-registered calibration sweep + stratified lived-channel re-pilot; analysis-heavy)
**Acceptance:** the dead mob-damage channel is repaired at BOTH instrument builders (mobs deal real damage), the pre-registered two-lever calibration executes on the LIVED channel bringing F2/F3 WR + F3 boss-TTK into their genre-anchored bands, a stratified caster+martial re-pilot runs against the FIXED bars with miss-taxonomy-split reporting, the caster-PASS *margins* are re-confirmed on the lived channel, the F-b parity closing read is delivered, and the lever-(b) TTK-saturation anomaly gets its pre-registered mechanism check post-fix.

## Context — what happened and what this fixes

Your Step-3 probe (`08972d0`) STOP-and-flagged correctly: the mob-damage channel is **structurally dead** — both instrument builders (`_build_standard_mob_dicts` + the Lane-1 build smoke) hand-roll damage-less mob dicts (`effect_category` string, no `effects` list), so `resolve_skill` accumulates zero `"damage"` effects → 0.0 dmg/hit at dm=1× and 32×; `MOB_DAMAGE_SCALE` inert. jack-ryan Gate-2 (`38b5a30`) **CONFIRMED the diagnosis at the mechanism** (a live-`damage`-effect dict yields 1522.9 dmg/hit scaling linearly) and **ENDORSED your proposed fix** (source from `emit_skills_for_threat_tier`, `spatial_engine.py:3122`).

**§7-survival (jack-ryan's determination — binding context):** the bars survive WHOLE (genre-anchored, fit-direction). All KPM dispositions survive. The **caster-PASS reframe survives as a VERDICT** (both caster passes gated on a KPM component + one-sided floors WR/exit=1.0 satisfy regardless of mob damage — a lived channel can only LOWER them, never manufacture a pass). **BUT the WR=1.0 / exit=1.0 MARGINS on those passes are dead-channel-inflated + unmeasured → the margins (not the verdicts) MUST be re-confirmed post-fix.** The one re-attributed signal: F2/F3 WR=1.0 saturation was a dead-channel artifact, not "rooms too easy" — re-read on the lived instrument.

## Matt's instrument-fix ruling (VERBATIM — binding)

> **Authorize A and C.** **B:** deterministic within-kit rotation across the full 7-element wheel — every kit faces the identical seeded element schedule; certification judged on the wheel average; worst-element recorded as a diagnostic flag, not a gate. **Pre-register the lever-(b) TTK-saturation anomaly for a mechanism check post-fix.**

Unpacked:
- **(A) — authorized:** source BOTH mob-dict builders from `emit_skills_for_threat_tier` (`spatial_engine.py:3122`), then sweep the mob-damage scalar (lever a).
- **(C) — authorized:** check whether the F4 continuous-spawn fodder path shares the dead-effect defect (your probe covered F2/F3 only); repair it if present. Ties to the F4 caster-margin re-confirm.
- **(B) — RULED (signature_element policy):** the emitter rejects `physical`; mobs must deal one of the 7 rotating elements. Ruling: **deterministic within-kit rotation across the full 7-element wheel — every kit faces the IDENTICAL seeded element schedule** (no kit gets a systematically easier/harder element draw). **Certification is judged on the WHEEL AVERAGE.** **Worst-element is RECORDED as a diagnostic flag, NOT a gate** (same shape as the ceiling=overpowered-flag semantics: a signal routed to review, not an auto-fail).
- **TTK-saturation anomaly pre-registration:** your probe found lever (b) boss HP moved TTK only 9.5→13.4s at 400k and never reached the 15s floor nor moved WR off 1.0. That saturation is anomalous (HP rising should raise TTK ~linearly). **Pre-register a mechanism check to run post-fix** — is it a heal/regen race, a resolver cap, a timeout artifact, or a genuine DPS-vs-HP ceiling? Document the hypothesis set BEFORE the lived-channel sweep so the check is falsifiable.

## Required reading before starting
- Your Step-3 math note `simulation/math/step3-mob-lethality-calibration-2026-07-07.md` (§5 the three ruling-asks — now ruled) + probe `simulation/scripts/gamora_step3_calibration_probe_2026_07_07.py` + `simulation/output/step3_calibration/step3_probe.json`.
- jack-ryan Gate-2 finding `qa/findings/2026-07-07-gamora-step3-mob-lethality-calibration-r4-flip-gate2.md` (diagnosis confirmation + §7-survival determination + fix concerns B/C).
- `emit_skills_for_threat_tier` at `spatial_engine.py:3122` (the canonical mob-skill source you are wiring the builders to — swarm dm 0.85, boss dm 5.0, magnitude 1000; note the `physical` rejection for the B wheel).
- `canonical/reap-die-rise-engine/gauntlet-run-beat-families-spec.md` §3 (bars/bands — FIXED inputs), §5 (headroom law), §6 (bar-derivation — bars do NOT move).
- `simulation/math/gauntlet-four-family-metrology-2026-07-07.md` §7 (jack-ryan's re-run — what you re-read on the lived channel) + §8 (miss-taxonomy semantics).
- Run-state `batch2-run-state-2026-07-06.md` — gamora Step-3 RESULT + jack-ryan Gate-2 blocks + the seventh-entry composition finding (stratification reference population).

## Math-before-code (Discipline #1 + #24 — document BEFORE any tuning)
Pre-register in a math note, committed before the calibration sweep:
- **The channel fix:** exactly which two builders change, how each sources from `emit_skills_for_threat_tier`, and a smoke proving mobs now deal real damage (dm=1× yields non-zero dmg/hit; confirm linear grip 1×→N×).
- **The 7-element wheel schedule (Ruling B):** the deterministic seeded element schedule EVERY kit faces (identical across kits); how certification aggregates to the wheel average; how worst-element is recorded as a diagnostic flag (not a gate). Confirm the schedule is kit-invariant (the whole point — no elemental-draw bias between kits).
- **#24 single-parameter sweep isolation (jack-ryan's endorsed protocol — now RELAYABLE, use it):** (1) fix mob-damage on **F2 first** (the clean single-knob family) → lock the scalar on F2 WR ∈ 0.85–0.95; (2) carry the locked scalar into **F3, sweep boss HP ALONE** against F3 TTK ∈ 15–90s → lock boss HP on TTK; (3) **read F3 WR LAST, as an OUTPUT — do NOT tune to it.** If F3 WR misses 0.60–0.80 after (1)+(2), that is a *finding* → STOP and flag to knight-rider; do NOT add a third knob.
- **Lever-(b) TTK-saturation mechanism check (Matt pre-registration):** the falsifiable hypothesis set + the measurement that discriminates them, registered BEFORE the lived-channel sweep.
- **Stratified reference population:** template strata for BOTH caster + martial paths per the seventh-entry composition finding (NOT a curated subset).
- **Miss-taxonomy report schema:** under-floor / over-ceiling / WR-side; floor = hard cert line; ceiling = overpowered-flag → balance-review (not fail).
- **Resource-bounds (Disc #1.1):** the lived-channel re-pilot's peak concurrent entities + run cost (mobs now deal damage → fights resolve differently; re-project).

## Cross-seam contract change? (Principle 6 gate)
- **Channel fix + mob calibration:** sim-internal; no cross-seam field change expected. If the fix touches any persisted field, MIGRATION.md + round-trip.
- **`pilot_policy` version stamp (Matt directive — cross-cutting):** Matt ruled all derived bands/certs are stamped with the `pilot_policy` version. **jack-ryan canonicalizes the version string in decisions-log (parallel task).** Your obligation: **stamp the certification output** (`family_certification_pass` result / the re-pilot report) with that `pilot_policy` version so a cert is traceable to the policy it was measured under. Read the version string jack-ryan registers; if it isn't landed when you reach the stamp, flag to knight-rider (don't invent one).
- **F4 telemetry:** star-lord's v2.20 consume already landed (`7d999db`) — `escape_reached` / `continuous_spawned_total` persist; no in-memory gap for the lived-channel re-pilot.

## Scope
- [ ] **Math-before-code note first** (all bullets above), committed before tuning. Includes the #24 isolation plan, the 7-element wheel schedule, the TTK-anomaly hypothesis set.
- [ ] **(A) Channel fix:** source BOTH mob-dict builders from `emit_skills_for_threat_tier`; smoke proves mobs deal real damage with linear scalar grip.
- [ ] **(C) F4-fodder defect check:** confirm/repair the continuous-spawn fodder damage channel.
- [ ] **(B) 7-element wheel:** deterministic kit-invariant seeded element schedule; cert on wheel average; worst-element = diagnostic flag.
- [ ] **Lever (a):** sweep mob-damage scalar → F2 WR ∈ 0.85–0.95 (lock on F2), carry to F3.
- [ ] **Lever (b):** sweep F3 boss HP ALONE → boss TTK ∈ 15–90s; **run the pre-registered TTK-saturation mechanism check.**
- [ ] **F3 WR read LAST as output** (do not tune to it; miss ⇒ finding ⇒ STOP-and-flag).
- [ ] **Stratified caster+martial re-pilot** on the lived channel vs the FIXED bars, template-stratified both paths.
- [ ] **Miss-taxonomy-split report** (under-floor / over-ceiling / WR-side; ceiling=overpowered-flag→review).
- [ ] **Re-confirm caster-PASS margins** on the lived channel (the WR/exit=1.0 margins were dead-channel-inflated — verdicts stand per jack-ryan, margins get real numbers).
- [ ] **F4-martial KPM: MEASURE + REPORT only** (still Rider-2 kit-side deferred). **NEW GATE (Matt):** any kit-side design response to F4-martial is gated on a **pilot-attribution probe** post-re-pilot (is the below-floor KPM a pilot-policy/mob-behavior artifact or a genuine kit defect?) — do NOT fire that probe or any kit response in this dispatch; note the gate.
- [ ] **F-b closing read:** explicit statement of whether caster/martial parity holds on the lived, calibrated instrument beyond the 2-cell caster sample (F-b confirm-unneeded criterion).
- [ ] **`pilot_policy` version stamp** on the cert output / re-pilot report (use jack-ryan's canonicalized version string).
- [ ] **Docstring doc-fix (jack-ryan Gate-2 WARN, pre-approved doc-only under ADR-002):** correct the three stale pre-flip narration spans at `gauntlet_sim.py:781-783`, `:833-835`, `:897-898` to match live post-R4-flip behavior (Disc-#12 framing hygiene).
- [ ] AGENT_STATE.md updated; MIGRATION.md if any boundary touched.
- [ ] Tag: `gamora/v-batch2-step3-lived-channel-repilot-1`.
- [ ] **Submit tagged commit to `agentic_orchestration/qa/pending/` for jack-ryan Gate-2** (mob-constant calibration + channel fix = certification-path instrument change).

## Out of scope (FROZEN / deferred)
- **NO kit-side chassis constant changes** (BASE_PHYSICAL/SPELL_DAMAGE_L50 + kin, the 2.3384× fossil) — Matt rules after the lived-channel re-pilot numbers land.
- **NO bar or band moves** (fit-direction — bars are fixed inputs; the instrument fix does NOT license moving a bar).
- **NO F4-martial fix / NO martial AOE-cleave work** — kit-side, gated on the pilot-attribution probe, NOT in this dispatch.
- **NO F-b sizing / NO F-fork adjudication** — F-b held confirm-unneeded; this re-pilot is its closing CRITERION. Matt rules after numbers land.
- **NO Leg C** — HELD until the re-pilot returns and Matt rules on its numbers.
- **NO pilot-policy / AI-layer work** (utility scorer, flocking, BT) — that's the ratified one-pilot-policy contract's future spec-work, un-parks when the Godot combat layer scopes; the scripted rotation is adequate here.

## References
- Matt instrument-fix ruling 2026-07-07 (A/C authorized, B 7-element wheel, TTK-anomaly pre-reg — verbatim above)
- gamora Step-3 STOP-flag (`08972d0`); jack-ryan Gate-2 (`38b5a30`, finding above); star-lord F4 telemetry (`7d999db`)
- Spec `gauntlet-run-beat-families-spec.md`; metrology note `gauntlet-four-family-metrology-2026-07-07.md`
- Disciplines #1 (design-before-code), #1.1 (resource-bounds), #11 (attribution), #12 (semantic-shift), #24 (single-parameter sweep isolation — jack-ryan's F2-first/boss-HP-on-TTK/WR-as-readout protocol); fit-direction law; one-pilot-policy contract (ratified canon 2026-07-07)
- Run-state `batch2-run-state-2026-07-06.md`
