# Dispatch — 2026-07-07 — jack-ryan — four-family gauntlet metrology pass (Lane 3)

**From:** knight-rider
**To:** jack-ryan (analyst / metrology — the bar-derivation half of the instrument)
**Approved by:** Matt 2026-07-07 (Q11 RATIFIED — this is the §6 metrology pass inside the ratified structure)
**Estimated effort:** multi-day (bar derivation + saturation guards + re-run martial distribution + caster cells on the new instrument + decisions-log registration)
**Acceptance:** numeric certification bars derived on the NEW four-family instrument per the genre bands, saturation-guarded, with the martial distribution + caster cells re-run on the built instrument; the Q11 ratification + the two governing laws registered in decisions-log. **Bars remain provisional-hypotheses-pending-playtest — genre-anchoring upgrades provenance, only the Godot descent-floor playtest validates feel.**

## ⛔ GATE — DO NOT START UNTIL LANE 1 LANDS
This pass **fires when gamora's Lane-1 rooms exist** (spec §8 step 3: "after the rooms exist"). Precondition: `gamora/v-batch2-gauntlet-four-family-instrument-1` tagged AND its Gate-2 passed (you are also the Gate-2 reviewer for that commit — Gate-2 PASS is the natural trigger to begin this pass). If you pick this up and the four family arenas are not yet buildable, STOP and report BLOCKED to knight-rider. **If Lane 2 (drax perf spike) has changed the §3 populations via spec amendment, derive against the amended populations** (population changes re-derive bars).

## Context — why bars are being re-derived, and the law that governs them

The old 9.90/11.65 martial bars are dead: they exceeded the 8-mob supply cap of the shells they were judged on (Step-1 finding). Bars must be re-derived on the new instrument — **never carry a bar across instruments** (the 9.90-on-8-mobs lesson). The governing law is fit-direction: **the genre bands are the EXTERNAL reference standard; the kit population is the SUBJECT under measurement, never the calibration source.** A kit that fails a genre-anchored bar gets fixed; the bar moves only if genre evidence says the bar misread canon.

## Required reading before starting
- `canonical/reap-die-rise-engine/gauntlet-run-beat-families-spec.md` — **§6 (your six-point bar-derivation protocol — the authoritative spec for this pass)**, §3 (the genre bands per family: F1 KPM 30–60 WR>95% · F2 KPM 20–40 WR 85–95% · F3 success-rate + TTK 15–90s WR 60–80% · F4 KPM 60–150 + progress + exit WR 80–90%+), §5 (headroom law: no KPM shell caps below ~2× its bar; F3 success-judged, exempt), §1 (why re-base — the saturation defect).
- `agentic_orchestration/legolas/findings/2026-07-07-arpg-genre-canon-encounter-metrology.md` — **the external reference standard** (32 sources, per-row confidence). The bands in §3 derive from this; you cite it as the exterior reference.
- `agentic_orchestration/gandalf/notes/2026-07-07-kr-relay-q11-fire-order.md` §2 Lane 3 — your scoped item list + the two laws to register.
- gamora's Lane-1 build output: the four arena configs + gamora's design/math note + compute-cost estimate (read when Lane 1 lands).
- Step-1 driver + finding: `simulation/martial_bar_rederivation_driver.py`, `simulation/notes/caster-bar-rederivation-2026-07-07.md`, `simulation/math/caster-bar-rederivation-instrument-match-2026-07-07.md` (the instrument-matched-derivation discipline you carry forward; the saturation lesson).
- The 30–50 TMPM anchor (2026-05-17, re-validated 2026-07-07) — the scale bridge into our economy (spec §6.1).

## The §6 six-point protocol (execute as specced)
1. Genre bands (§3, legolas file) are the exterior reference; the 30–50 TMPM anchor is the scale bridge into our economy.
2. **Bars derive on the NEW instrument only** — never carry a bar across instruments (instrument-matched derivation per the Step-1 driver's discipline).
3. **Saturation guard at derivation time:** reject any derived bar within 2× of the shell's supply ceiling (headroom law §5). Register the guard, don't just apply it.
4. Balanced cohort first (per the §2-S.1 reduction); cohort expansion after.
5. All bars remain **provisional hypotheses pending playtest** — stamp them so.
6. **Numeric bars are NOT pre-set** — you set them here, on the built instrument, against the genre bands.

## Scope
- [ ] Derive numeric bars per family (F1/F2 = KPM floor+ceiling per genre §3; F3 = **success-rate + TTK rails, NOT KPM** — KPM stays a wide sanity rail only; F4 = KPM + forward-progress + exit-within-window).
- [ ] Register saturation guards (§5 headroom law): assert no KPM-judged shell caps below ~2× its bar; reject any bar within 2× of the shell's supply ceiling at derivation time.
- [ ] Re-run the martial distribution on the new instrument (the Step-1 martials, now on genre-populated rooms with headroom).
- [ ] Re-run the caster cells on the new instrument.
- [ ] If Lane 2's spike landed and changed §3 populations, derive against the amended populations.
- [ ] **Decisions-log registration:** the Q11 ratification + the two laws (fit-direction, one-spatial-contract) per the standing batch pattern. (You own decisions-log.)
- [ ] Note file with the derived bars, provisional-hypothesis stamp, and the saturation-guard record.
- [ ] Report the derived bars + re-run distributions to knight-rider (feeds the resumed Step 3 stratified re-pilot).

## Out of scope
- **NO instrument construction** — gamora built the rooms (Lane 1). You derive bars ON them.
- **NO re-pilot / F-b sizing** — that is the RESUMED Step 3/4 (knight-rider orchestrates after your bars land). You produce the bars + re-run distributions; the F-fork adjudication and constant changes stay FROZEN until then + Matt's ruling.
- **NO fitting bars to make kits pass** (fit-direction law) — bars answer to the genre; kits get measured.
- **NO re-derivation on the old 8-mob shells** — dead instrument; new instrument only.

## References
- Spec `gauntlet-run-beat-families-spec.md` §3/§5/§6 (RATIFIED 2026-07-07); fire order Lane 3
- legolas genre metrology (external reference standard) `legolas/findings/2026-07-07-arpg-genre-canon-encounter-metrology.md`
- `gauntlet-metrics-as-provisional-hypotheses-recognition` (bars provisional pending playtest)
- Disciplines #1 (design-before-code), #11 (attribution), #18.1 (substrate-voting-binding), #23 (framing-audit at metrology hotspot); Principle: fit-direction law
- Run-state `batch2-run-state-2026-07-06.md`
