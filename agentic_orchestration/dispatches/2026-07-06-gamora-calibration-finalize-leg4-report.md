# Dispatch — 2026-07-06 — gamora — calibration-note finalize + Leg-4 report (ONE unit)

**From:** knight-rider
**To:** gamora
**Approved by:** Matt 2026-07-06 (C2 chassis ruling + merged fire-order, relayed via gandalf `gandalf/notes/2026-07-06-kr-relay-av2-chassis-ruling-fire-order.md`)
**Estimated effort:** ~2–3h
**Acceptance:** calibration note finalized on the Gate-2-verified baseline; plain-caster band gap quantified; Leg-4 report written; both INFO flags folded; one batch-2 spec line captured. **Analysis + report ONLY — no re-emit, no re-fight, no band re-tune.**

## Context — the C2 ruling you are calibrating against

Matt ruled the caster chassis-band fork **C2: TWO CHASSIS BANDS, keyed on the existing proxy-share knob** (validated 0.250000 exact at W3 — no new mechanism):
- **Plain-caster band** (proxy share ~0): carries a **solo single-target floor — must clear open_arena AND chokepoint solo** ("a mage kills what it points at" / D2 Sorceress law). The current **0.0 KPM on both shells is a chassis gap-to-close, not a design position.**
- **Summoner band** (proxy share ≥ 0.25 knob): **solo timeout ACCEPTABLE; proxy DPS mandatory** (already ruled 2026-07-02).
- **The numeric placement of the plain-caster floor is an OUTPUT of your calibration note** — nobody picks it in advance.

Your calibration note (`simulation/notes/proxy-magnitude-calibration-math-2026-07-06.md`) already cleared Gate-1 (RATIFY-WITH-CONDITIONS, both critics). Its open slot — the solo-caster baseline — now exists on disk and was **independently re-verified by jack-ryan at Gate-2 to 4 decimals** (not fabricated).

## Required reading before starting
- `agentic_orchestration/gandalf/notes/2026-07-06-kr-relay-av2-chassis-ruling-fire-order.md` — the C2 ruling + this fire-order (authoritative).
- `agentic_orchestration/variation-pilot-run-state-2026-07-06.md` — full pilot chain, triage outcome, baseline, Gate-1 conditions.
- Your own `simulation/notes/proxy-magnitude-calibration-math-2026-07-06.md` — the note you are finalizing.
- `reincarnated-engine/src/reincarnated/output/variation_pilot_measurement_report.json` — the Gate-2-verified baseline (the input for your open slot).
- `agentic_orchestration/qa/pending/2026-07-06-pilot-measurement-report-gate2.md` — jack-ryan's Gate-2 finding + the two INFO flags.
- The calibration Gate-1 disposition + its 6 binding conditions (in the run-state note).

## Scope (all analysis/report — NO production code)
- [ ] **1. Finalize the calibration note** — anchor on the Gate-2-verified `tier_2_kpm` per shell × cohort. Fill the open baseline slot with real numbers.
- [ ] **2. Quantify the plain-caster band gap** — the distance from the current chassis to open_arena/chokepoint solo-clear. **This is the number that places the C2 plain-caster floor.** (It is an output, not a pick.)
- [ ] **3. Fold INFO flag 2** — confirm the min=max clamp semantics behind `magic_pack` KPM=600.0 before treating it as real DPS; until confirmed, report it as a **≥-ceiling**. `elite_pack` 426.9 (genuine spread) is the pack-overperformance **signal of record**.
- [ ] **4. Fold INFO flag 1** — `caster_proxy` baseline is legitimately empty (int_light collapsed into shared buckets). The note **anchors on the plain-caster baseline only** and says so explicitly; **summoner-band calibration defers to batch-2 measured data.**
- [ ] **5. Write the Leg-4 report** (the pre-registered attribution verdict, now unsealed):
  - Mechanism thesis **CONFIRMED**: 40/81 season_emit; chain-variants 15/15 eligible-encounters-passed; G4 knob at z≈−1.0 (in-range at 4/25).
  - The **chassis finding**: plain-caster times out solo on single-target/corridor (KPM 0.0), over-clears on packs — the empirical basis for C2.
  - The **triage lineage**: KR's join hypothesis DISCONFIRMED via the published contract; the coupling was the whole defect; fix = `measurement_report_writer.py` / MIGRATION §v2.10; Gate-2 PASS-WITH-FOLLOWUPS.
  - **Attribution discipline (Rider 2):** any proxy-dominant read = "solo-baseline, summons inert by design" — NEVER summoner viability.
- [ ] **6. One batch-2 spec line — per-cohort bucket keys** — proxy cohorts (int_light etc.) must never collapse into shared legendary-id buckets again. Capture it for the batch-2 gauntlet spec (cheap at spec time, expensive to discover twice). This is a NOTE for gandalf's batch-2 spec, not a code change here.
- [ ] AGENT_STATE.md updated at session end.
- [ ] Auto-commit (authorized cycle work). No tag needed (no production code). Do NOT push.

## Cross-seam contract change? (Principle 6 gate)
**NO — no cross-seam contract change in this dispatch.** Analysis + report only; no schema, fixture, or emit-shape touched. The batch-2 per-cohort-bucket-key item is a spec NOTE handed to gandalf, not a change made here.

## Out of scope (explicit non-goals)
- **NO re-emit, NO re-fight, NO band re-tune.** Under C2 the plain-caster band re-tune becomes **batch-2 config**, and the re-emit/re-fight IS batch-2 itself — one batch, one fire, after the gen-path chain closes. Do not fire standalone compute.
- The summoner-band proxy magnitudes — defer to batch-2 measured data (INFO flag 1). Do not invent them from the empty caster_proxy slot.
- Any production code. This unit is analysis + report.

## Open questions for you to resolve (document your answers)
- The magic_pack clamp semantics (INFO flag 2) — confirm from the source sim whether 600.0 is a real ceiling or a min=max artifact; report accordingly.
- Where the plain-caster floor lands numerically once the gap is quantified (the C2 output).

## References
- gandalf relay `2026-07-06-kr-relay-av2-chassis-ruling-fire-order.md`; run-state `variation-pilot-run-state-2026-07-06.md`
- Gate-1 disposition (calibration note) + Gate-2 finding (measurement-report fix)
- decisions-log: C2 registration batches with the 2026-07-06 ruling set on jack-ryan's next pass (not this unit's concern)

---

## Completion record

**Completed:** 2026-07-06 (gamora SESSION 49). ANALYSIS + REPORT ONLY — ZERO fights, ZERO re-emit,
ZERO re-fight, ZERO band re-tune, ZERO production code (edits confined to `simulation/notes/`). No tag.
No push (Matt-gated). MIGRATION: N/A.

**Two artifacts delivered (one unit):**
1. `reincarnated-engine/src/reincarnated/simulation/notes/proxy-magnitude-calibration-math-2026-07-06.md`
   — FINALIZED. §2 open baseline slot FILLED from the Gate-2-verified
   `output/variation_pilot_measurement_report.json` (jack-ryan re-verified to 4 decimals). Both INFO
   flags folded (§2.1 plain-caster-only / caster_proxy defers to batch-2; §2.2 magic_pack 600.0 =
   `≥`-ceiling artifact). Plain-caster band gap QUANTIFIED (§2.3).
2. `reincarnated-engine/src/reincarnated/simulation/notes/leg4-attribution-report-2026-07-06.md` — NEW.
   The unsealed pre-registered attribution verdict.

**Acceptance items, all met:**
- [x] Calibration note finalized on the Gate-2-verified baseline.
- [x] Plain-caster band gap quantified → **C2 floor placed at bar_lo: 9.90 KPM (open_arena) / 11.65 KPM
  (chokepoint)**. Current chassis 0.0 on both → gap == floor (full timeout-to-floor jump). Output of
  the measurement, not a pick.
- [x] INFO flag 2 folded — **magic_pack 600.0 verdict: metric-domain ARTIFACT** (1/tick-floor =
  kills/(0.1s/60) when a pack clears sub-tick; `t4_sim_cycling.py:108-113,273-277,720`; engine already
  routes sub-`T_min` clears on COMPLETION via `CLEAR_SHELL_DOMAIN_TMIN_S=1.0`), NOT a min=max clamp,
  NOT real DPS → reported as `≥`-ceiling. elite_pack 426.9 (genuine spread 163.6–450.0) = pack-
  overperformance signal of record.
- [x] INFO flag 1 folded — caster_proxy legitimately empty (int_light bucket-collapse); note anchors on
  PLAIN-caster baseline only; summoner-band DEFERS to batch-2.
- [x] Leg-4 report written — mechanism CONFIRMED (40/81 emit; chain-variants 15/15
  eligible-encounters-passed; G4 knob z≈−1.0 in-range at 4/25) + chassis finding + triage lineage
  (KR join hypothesis DISCONFIRMED via published contract; coupling was the whole defect; fix =
  star-lord `measurement_report_writer.py` / MIGRATION §v2.10; Gate-2 PASS-WITH-FOLLOWUPS) +
  attribution discipline (Rider 2: proxy-dominant = solo-baseline, summons inert; NEVER summoner
  viability).
- [x] One batch-2 spec line captured (per-cohort bucket keys) — handed to gandalf's batch-2 spec
  (report §6), not made here.
- [x] AGENT_STATE.md updated (SESSION 49).
- [x] Auto-commit (authorized cycle work); no tag; no push.

**Returns to KR:** pilot chain CLOSED → gandalf authors the batch-2 build spec (consumes the C2 floor
placement + per-cohort-bucket-key spec line). Light jack-ryan read (analysis+report, no production code).
