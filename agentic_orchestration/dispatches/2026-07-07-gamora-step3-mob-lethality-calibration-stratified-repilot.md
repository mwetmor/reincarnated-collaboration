# Dispatch — 2026-07-07 — gamora — Step 3: mob-lethality calibration + stratified caster+martial re-pilot (+ R4 ship-gate flip)

**From:** knight-rider
**To:** gamora (simulation seam — `spatial_gauntlet/`, `gauntlet_sim.py`)
**Approved by:** Matt 2026-07-07 (GO on reshaped Step 3, three riders + two precisions, folded verbatim below)
**Estimated effort:** multi-day (pre-registered calibration sweep + stratified re-pilot + one-line R4 flip; analysis-heavy)
**Acceptance:** F2/F3 win-rates and F3 boss-TTK brought into their genre-anchored bands via the PRE-REGISTERED mob-lethality knobs (rooms must be able to kill functional kits), a stratified caster+martial re-pilot run against the four-family bars with miss-taxonomy-split reporting, the R4 ship-gate flip wired, and a clear empirical read on whether caster/martial parity holds beyond the 2-cell caster sample (F-b's closing criterion).

## Context — what this is and what changed

The Q11 four-family instrument is built (Lane 1, `8d45f95`, Gate-2 PASS) and bars are derived (Lane 3, `e1f12b8`). jack-ryan's re-run on the NEW instrument (native HP, no dead 300k/500k wall) reframed the caster HALT: **casters PASS the cells they ran (F1 2/2, F4 2/2)** — the original ~10× shortfall was substantially a dead-wall + saturation-cap ARTIFACT, not a caster damage defect. The remaining misses (F2/F3 WR saturate at 1.0 = rooms too EASY; F3 TTK ~6s below the 15–90s rail; F4 martial-KPM below floor) are **mob-lethality calibration signals + one kit finding — NOT caster-vs-martial asymmetry.**

Matt ruled **GO on reshaped Step 3**: mob-lethality calibration + stratified caster+martial re-pilot against the new bars. **F-b (caster-damage-premium) is HELD as confirm-unneeded — this re-pilot is its closing criterion. If caster/martial parity holds beyond the 2-cell caster sample, F-b retires to git.**

## Matt's riders (VERBATIM — binding)

**Rider 1 — Pre-registered calibration, split by knob.** Two levers, two targets, **registered in your math-before-code note BEFORE any tuning**:
- **(a) mob damage UP** until **F2 WR lands in 0.85–0.95** AND **F3 WR lands in 0.60–0.80** — rooms must be able to kill functional kits.
- **(b) F3 boss HP sized** until **boss TTK lands in the 15–90s rail** (metrology's 6000 was a PLACEHOLDER, not a finding).
- **Reference population = the stratified pilot population** (BOTH paths — caster + martial — template-stratified per the seventh-entry composition finding), NEVER a curated subset.
- **Bands and bars do NOT move — fit-direction law, one layer down.** You tune the rooms to the bars; you never tune the bars to the kits.

**Rider 2 — F4-martial stays OUT of the room-calibration bucket.** jack-ryan's note calls it the KIT finding — keep it that way. It gets **MEASURED** in the stratified re-pilot (expect it to widen if any mob HP rises), then disposition is **kit-side** (martial AOE/cleave expression) — NOT a bar move, NOT a room move, and **NOT fired inside Step 3.** Report the F4-martial KPM number; do not act on it here.

**Rider 3 — Miss-taxonomy split + ceiling semantics.** Re-pilot reporting **splits misses into: under-floor / over-ceiling / WR-side.** **Floor = hard certification line. Ceiling = OVERPOWERED flag routed to balance review, NOT auto-fail** (matches F3's overpowered-flag semantics + doc-50 bounded-viability). (jack-ryan registers these semantics alongside the bars — parallel task; use them in your report format.)

## Matt's precisions (VERBATIM — binding)

**Precision 1 — Freeze boundary (READ CAREFULLY — the freeze SPLITS here):**
- **KIT-SIDE chassis constants remain FROZEN:** `BASE_PHYSICAL_DAMAGE_L50` / `BASE_SPELL_DAMAGE_L50` and kin — the 2.3384× fossil moves ONLY on Matt's ruling after re-pilot numbers land. Do NOT touch these.
- **ROOM-SIDE mob constants are explicitly UNFROZEN** for the pre-registered calibration above: mob damage scalars, boss HP, `MOB_HP_DIFFICULTY_MULTIPLIER`-class knobs. **This unfreeze IS the point of Step 3.** Your Lane-1 "constants frozen" guardrail now reads as **kit-side only** from here forward.

**Precision 2 — the R4 ship-gate flip fires with this go** (scoped item below).

## Required reading before starting
- `canonical/reap-die-rise-engine/gauntlet-run-beat-families-spec.md` §3 (per-family bars + bands), §5 (headroom law + judging), §6 (bar-derivation — bars are FIXED inputs to you now).
- `simulation/math/gauntlet-four-family-metrology-2026-07-07.md` §7 (jack-ryan's re-run results you are calibrating against — the WR saturation + TTK placeholder + F4-martial number).
- `simulation/math/gauntlet-four-family-instrument-build-2026-07-07.md` (your own Lane-1 build note — populations, HP mapping, the mob-constant knobs).
- `agentic_orchestration/batch2-run-state-2026-07-06.md` — Lane-3 RESULT block + the seventh-entry composition finding (stratification reference population).
- `output/gauntlet_four_family_metrology/metrology_report.json` (the re-run data).
- `gauntlet_sim.py:771` (`family_certification_pass()`) + `:812` (`gauntlet_pass()` — still reads the legacy ≥9-of-18 W-α6 floor) — the R4 flip sites.

## Math-before-code (Discipline #1 + #24 — document BEFORE tuning)
- **Pre-register the two-lever calibration** (Rider 1): the exact knobs, their current values, the target metric each drives, and the sweep procedure. **Discipline #24 (single-parameter sweep isolation) is a HOTSPOT here:** lever (a) mob damage and lever (b) F3 boss HP BOTH touch F3 (damage→WR, HP→TTK, and HP has a secondary WR effect). **Document how you isolate them** — sweep order, hold-one-fix-one, and how you attribute F3 WR vs TTK movement to the right knob. **If the F3 two-knob coupling cannot be cleanly isolated, STOP and flag to knight-rider** (jack-ryan is doing a parallel methodology check on this exact point — your math-note is the checkpoint; align with any concern relayed before you tune).
- **Stratified reference population** (Rider 1): define the template strata (both caster + martial paths) per the seventh-entry composition finding. NOT a curated subset.
- **Miss-taxonomy report schema** (Rider 3): under-floor / over-ceiling / WR-side, with ceiling=overpowered-flag (not fail).
- Resource-bounds (Disc #1.1): the stratified re-pilot's peak concurrent entities + run cost.

## Cross-seam contract change? (Principle 6 gate)
- **Mob-constant calibration:** sim-internal; no cross-seam field change expected.
- **R4 flip:** changes the certification-contract behavior of `gauntlet_pass()` — a semantic shift (Disc #12). Document in MIGRATION.md; jack-ryan registers the contract shift in decisions-log (already flagged).
- **F4 telemetry:** `escape_reached` / `continuous_spawned_total` / `mobs_killed` range — star-lord is being dispatched IN PARALLEL to wire the consume side (MIGRATION v1.84). Coordinate via MIGRATION v1.84; if the re-pilot needs F4 telemetry persisted and star-lord's consume hasn't landed, flag it (don't block — run in-memory if needed and note the gap).

## Scope
- [ ] **Math-before-code note first** (all bullets above), committed before any tuning. Includes the #24 sweep-isolation plan.
- [ ] **Lever (a) — mob damage calibration:** tune mob damage scalars UP until F2 WR ∈ 0.85–0.95 AND F3 WR ∈ 0.60–0.80, measured on the stratified reference population.
- [ ] **Lever (b) — F3 boss HP calibration:** size boss HP until F3 boss TTK ∈ 15–90s (replace the 6000 placeholder).
- [ ] **Stratified caster+martial re-pilot:** run all four families against the fixed bars, template-stratified both paths.
- [ ] **Miss-taxonomy-split report** (Rider 3): under-floor / over-ceiling / WR-side; ceiling=overpowered-flag→balance-review, floor=hard line.
- [ ] **F4-martial KPM: MEASURE and REPORT only** (Rider 2) — do NOT act on it; note whether it widened under any mob-HP rise; disposition is kit-side, deferred.
- [ ] **F-b closing read:** explicit statement of whether caster/martial parity holds beyond the 2-cell caster sample (F-b confirm-unneeded criterion).
- [ ] **R4 ship-gate flip (Precision 2):** wire `gauntlet_pass()` (`:812`) to `family_certification_pass()` (`:771`) — certification = pass all four families, retiring the legacy ≥9-of-18 floor. MIGRATION.md + Disc-#12 note.
- [ ] AGENT_STATE.md updated.
- [ ] Tag: `gamora/v-batch2-step3-mob-lethality-calibration-1`.
- [ ] **Submit tagged commit to `agentic_orchestration/qa/pending/` for jack-ryan Gate-2** (mob-constant changes + R4 flip = certification-path code).

## Out of scope (FROZEN / deferred)
- **NO kit-side chassis constant changes** (BASE_PHYSICAL/SPELL_DAMAGE_L50 + kin, the 2.3384× fossil) — Matt-ruled after re-pilot numbers land.
- **NO bar or band moves** (fit-direction — bars are fixed inputs).
- **NO F4-martial fix / NO martial AOE-cleave work** (Rider 2 — kit-side, deferred, not in Step 3).
- **NO F-b sizing / NO F-fork adjudication** — F-b is held confirm-unneeded; this re-pilot is its closing CRITERION, not its execution. Matt rules after numbers land.
- **NO Leg C** — stays HELD until the re-pilot returns and Matt rules on its numbers.

## References
- Matt GO ruling 2026-07-07 (riders 1–3, precisions 1–2, verbatim above)
- Spec `gauntlet-run-beat-families-spec.md`; metrology `e1f12b8`; build `8d45f95`
- Disciplines #1 (design-before-code), #1.1 (resource-bounds), #11 (attribution), #12 (semantic-shift — R4 contract), #24 (single-parameter sweep isolation — F3 two-knob hotspot); fit-direction law
- Run-state `batch2-run-state-2026-07-06.md`
