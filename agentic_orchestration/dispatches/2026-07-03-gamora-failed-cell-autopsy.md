# Dispatch — 2026-07-03 — gamora — W3 failed-cell autopsy (11 cells, no re-fight)

**From:** knight-rider
**To:** gamora (lead) · jack-ryan (review leg — DEV-MODE, on gamora's output)
**Approved by:** Matt, 2026-07-03 (this session — "FAILED-CELL AUTOPSY, ruling-independent, fire now")
**Estimated effort:** 2-4h (forensic read + classification + write-up), then jack-ryan review beat
**Acceptance:** the 11 failed cells are each classified by failure mode (kit-design / calibration / structural) with per-cell evidence cited from the canonical JSON; findings appended to the summoner decision file; jack-ryan review passes. **Zero fights simulated.**

## Context

The W3 batch-1 emission produced 700 survivors from 7 of 18 BC cells. **All 11 non-surviving cells** are: 5 INT + 5 WIS caster cells (a systematic caster wipeout) + 1 melee-DEX cell (`melee_high_flat_dex`). gandalf's addendum to the summoner decision file established that this is materially wider than "summoner emission" — a proxy-live batch-2 re-fire is now the candidate recovery vehicle for THREE absences (summoners, casters, role-varied kits), and **Matt's Option-1-vs-2 summoner ruling gates on this autopsy's failure-mode classification.** If caster failure is *structural* (needs the proxy gen-path or a resource-economy fix), batch-2 fires with a target; if *calibration*, batch-2 without the autopsy fires blind.

This is a **read-only forensic over existing on-disk fight data. NO re-fight.** Matt was explicit; a prior session's "no re-fight" recovery claim shipped without an existing code path and cost 1.5h of accidental re-simulation (see W3 emission dispatch completion record + engineering-disciplines candidate entry). Do not repeat that. If you conclude the data cannot answer a sub-question without new fights, **halt-loud and report it** — do not silently simulate.

## Canonical source — VERIFIED by knight-rider (premise is real, not assumed)

**File:** `reincarnated-engine/src/reincarnated/simulation/output/cycle-13-gauntlet-sim-results-2026-05-27.json` (93MB — this is the W3 canonical the emission driver's `--recover-from-canonical` reads; NOT the T4-suite look-alikes with other timestamps, which share the format but are the same content).

KR pre-verified the following so you don't burn time on discovery:

- **`kit_results`** (2,200 rows) carries **cell-level `season_emit`** — the survivor signal. season_emit=True ⇒ surviving cell; =False ⇒ failed cell. This cleanly separates the 7 survivors from the 11 failures.
- **`encounter_results`** (125,400 rows) carries the **per-encounter forensic mechanism**: `tier_1_outcome` (ACCEPT/REJECT), `tier_1_kpm`, `tier_1_elevated`, `tier_2_kpm`, `tier_2_survival_rate`, `in_band`, `sg_overall` (BLOCK/…), `bypassed_ceiling_artifact`, `gauntlet_pass`, `encounters_passed`/`encounters_total`. Cell identity is embedded in `encounter_id` (e.g. `endgame_bc_melee_high_flat_int_none`) and `legendary_id`.
- **All 18 cells are present**, including every INT/WIS failed cell. The 11 failed cells' fight data is fully on disk.

**Note the analysis unit:** this canonical JSON is cohort/T4-keyed (`cohort` ∈ {DPS-min-maxer, Balanced, Defensive, Hybrid}, `t4_config_key`), mapped to BC cells via `encounter_id`. The autopsy is therefore a **cell-level** forensic ("why did this cell reject"), which is exactly what Matt asked for. Per-candidate 1:1 identity with the 1,800 W3-generated kits is NOT needed and NOT present — don't chase it.

## A starting observation (KR-measured; a lead, NOT a pre-judged verdict)

The tier-1 REJECT counts across failed cells are **bimodal**, which is likely your primary failure-mode axis:

- **High-reject cells** (tier_1_outcome=REJECT ≈ 5,100–6,300 of ~6,600 encounters): `melee_high_flat_dex`, `ranged_low_spiky_int`, `ranged_medium_variable_int_none`, `ranged_medium_variable_int_light`, `ranged_low_spiky_wis` (partial ~3,436), `ranged_medium_variable_wis`. These fail *at tier-1* — throughput/damage rejection.
- **Low-reject-but-still-failed cells** (REJECT ≈ 0–3, yet season_emit=False everywhere): `melee_high_flat_int`, `melee_high_variable_wis`, `melee_medium_variable_wis`, `mid_low_spiky_int`, `mid_medium_variable_wis`. These *pass* tier-1 damage but fail a **downstream gate** — check `in_band`, `tier_2_survival_rate`, `sg_overall`.

Two distinct mechanisms hide behind one "FAIL" label. Your classification should resolve which, per cell. (Cross-reference W2's caster-alone WR 0.000 evidence and doc-48 INT/WIS→mana economy.)

## Classification taxonomy (Matt's three modes — define your boundaries, then apply)

For each of the 11 cells, assign ONE primary mode (secondary allowed if evidenced):

- **kit-design** — the composed kit is coherent but its design (skill mix, resource model, geometry) is mismatched to the encounter; fixable by re-composing within existing generation capability.
- **calibration** — the kit design is sound but a tuning constant (damage coefficient, mana economy, band thresholds, DDA) puts it out of band; fixable by a number, no new gen-path.
- **structural** — the failure is a missing generation capability (e.g., caster viability depends on proxy/summon composition that does not exist; the mana economy has no functioning loop). Not fixable without new engine work; this is the mode that would make batch-2 fire blind absent the fix.

**Discipline #23 framing-audit** applies at the taxonomy boundary: state, per cell, the *cheapest refuting test* for your assigned mode (#19.1) — what in the JSON would flip the verdict. **Discipline #1 (math-before-code):** this is analysis-only, but the classification IS a load-bearing claim Matt rules on; cite file:field:value for each verdict, no assertion without evidence.

## Cross-seam contract change? (Principle 6 gate)

**No.** This dispatch reads existing JSON and writes a findings section to a markdown decision file. No telemetry schema, fight_log, loadout, or export packet is added/modified/renamed.
**Round-trip: not applicable — no cross-seam contract change in this dispatch.**

## Scope
- [ ] Read the canonical JSON; confirm the 11 failed cells + 7 survivors match season_emit (sanity check vs this dispatch's inventory).
- [ ] For each of the 11 failed cells: classify failure mode (kit-design / calibration / structural) with cited evidence (tier_1_outcome distribution, kpm, in_band, tier_2_survival_rate, sg_overall).
- [ ] Resolve the bimodal split: which cells fail at tier-1 (throughput) vs downstream (band/survival/sg).
- [ ] Per-cell: name the cheapest refuting test (#19.1) for the assigned mode.
- [ ] Explicit answer to the load-bearing question: **is the caster wipeout (10 INT/WIS cells) predominantly structural (⇒ batch-2 needs a gen-path/economy fix) or calibration (⇒ a proxy-live re-fire may recover them)?** This is what Matt's ruling turns on.
- [ ] Append findings to `canonical/matt_decision_needed/2026-07-03-w3-summoner-emission-structural-gap.md` as a new dated section (do not edit gandalf's addendum; append below it).
- [ ] AGENT_STATE.md updated (simulation seam).
- [ ] jack-ryan DEV-MODE review of the classification (the review leg below).
- [ ] No tag required (analysis artifact, no code change) — if you write a throwaway analysis script, keep it under `simulation/notes/` and do not tag it as production.

## Acceptance criteria
- [ ] 11 cells classified, evidence-cited, bimodal split resolved.
- [ ] Caster-wipeout structural-vs-calibration question answered explicitly for Matt's ruling.
- [ ] Findings appended to the decision file.
- [ ] jack-ryan review passes (or returns findings for gamora to resolve).
- [ ] Zero fights simulated — assert this explicitly in the write-up.
- [ ] Round-trip: not applicable — no cross-seam contract change.

## Review leg (jack-ryan, DEV-MODE)

After gamora appends findings, jack-ryan reviews the **classification method and evidence**, not just the conclusions: (a) is each cell's mode assignment supported by the cited fields, (b) is the bimodal split correctly attributed, (c) does the structural-vs-calibration caster verdict survive its own cheapest-refuting-test, (d) any framing-audit (#23) miss (e.g., reading a field that isn't a live varying coordinate — the F2 role_orientation-phantom lesson from the glyph pre-run). jack-ryan may BLOCK the finding from informing Matt's ruling if the evidence doesn't hold; that's the gate.

## Out of scope (explicit non-goals)
- **Any re-fight / re-simulation.** Read on-disk data only. Halt-loud if a question needs new fights.
- Proposing or building the summoner/caster gen-path — that's the Option-1 dispatch, downstream of Matt's ruling.
- Re-opening the summoner Option-1-vs-2 question — the autopsy INFORMS it, doesn't decide it (Matt's call).
- Touching the survivor bundle, the roster shortlist, or the flavor pass (separate carve-outs).
- Curve-fitting a recovery recommendation — classify the failure; recommendation is Matt's + the follow-on dispatch's.

## Open questions for gamora to resolve
- Does the `Defensive` cohort's 0-pass-everywhere (metadata `gauntlet_pass_by_cohort.Defensive=0`) confound the caster read, or is it orthogonal? Document.
- Is `mid_medium_variable_wis` (REJECT=0, yet failed) a pure band/survival failure? If so it's the cleanest "calibration not structural" candidate — or the cleanest counter-evidence. Call it.
- The `ranged_medium_variable_int_light` cell (the one proxy-`light` INT cell): does its failure mode differ from the `_none` INT cells? This is the closest on-disk signal to whether proxy-density changes caster viability — directly bears on Option 1.

## References
- Decision file (append target): `canonical/matt_decision_needed/2026-07-03-w3-summoner-emission-structural-gap.md` (+ gandalf addendum lines 54-69)
- glyph pre-run findings (caster wipeout evidence, F2 phantom-axis lesson): `agentic_orchestration/gandalf/notes/2026-07-03-glyph-s5-pre-run-findings.md`
- W3 emission dispatch (canonical-JSON recovery mechanism, the 1.5h re-fight lesson): `dispatches/2026-07-03-rocket-star-lord-w3-emission-run.md` §Phase-B completion record
- shortlist prep (survivor cell inventory): `agentic_orchestration/w3-batch1-curation-shortlist-prep-2026-07-03.md`
- Disciplines #1 (math-before-code), #19.1 (cheapest-refuting-test-per-claim), #23 (framing-audit) — `~/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md`
- Canonical JSON: `src/reincarnated/simulation/output/cycle-13-gauntlet-sim-results-2026-05-27.json` (kit_results.season_emit + encounter_results forensics; 18 cells)
</content>
