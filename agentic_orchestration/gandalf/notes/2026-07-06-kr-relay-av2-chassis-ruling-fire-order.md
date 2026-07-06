# KR relay — AV2 pilot chain: chassis ruling C2 + gamora close-out fire-order

> **From:** gandalf (Pattern-B session with Matt) → **knight-rider (AV2 session).** Matt-ruled 2026-07-06; this note is paste-ready fire-order. Pattern precedent: `2026-07-02-kr-relay-two-lane-fire-order.md`.
> **Context you already hold:** Gate-2 PASS-WITH-FOLLOWUPS on the measurement-report fix (`c97263e`); baseline trustworthy; two INFO flags; your (a)/(b) fork + Leg-4-report-first alternative.

---

## 1. THE RULING (Matt, 2026-07-06) — C2: TWO CHASSIS BANDS, keyed on proxy share

Matt ruled the caster chassis-band fork **C2** (*"I agree on all points"* against the three-option table; C1 one-band and C3 summons-everywhere both REJECTED):

- **Plain-caster band** (proxy share ~0): carries a **solo single-target floor — must clear open_arena AND chokepoint solo.** A mage kills what it points at (D2 Sorceress law). The current 0.0 KPM on both shells is a chassis gap-to-close, not a design position.
- **Summoner band** (proxy share at/above the validated 0.25 knob): **solo timeout ACCEPTABLE; proxy DPS mandatory.** This half was already ruled 2026-07-02 (*"we are expecting summon-kits to time out or die to boss if not for their proxy's DPS"*) — C2 confirms it and adds the missing plain-caster floor beside it.
- The band discriminator is the **existing proxy-share composition knob** (validated 0.250000 exact at W3) — no new mechanism.
- **Numeric placement of the plain-caster floor = an OUTPUT of gamora's calibration note** (§2 item 2), not a number anyone picks in advance.

## 2. FIRE NOW — one gamora dispatch: calibration note + Leg-4 report, ONE unit

Matt ruled your (a) and the report-first alternative **merge**: same evidence, same author, one dispatch. Scope:

1. **Finalize the calibration note** anchored on the Gate-2-verified baseline (tier_2_kpm per shell×cohort).
2. **Quantify the plain-caster band gap** — the distance from the current chassis to open_arena/chokepoint solo-clear. This is the number that places the C2 floor.
3. **Fold INFO flag 2:** confirm the min=max clamp semantics behind magic_pack 600.0 before treating it as real DPS; until confirmed, report it as a ≥-ceiling. elite_pack 426.9 (genuine spread) is the pack-overperformance signal of record.
4. **Fold INFO flag 1:** caster_proxy baseline legitimately empty (int_light collapsed into shared buckets) — the note anchors on the **plain-caster baseline only** and says so; summoner-band calibration defers to batch-2 measured data.
5. **Write the Leg-4 report** (the pre-registered attribution verdict, now unsealed): mechanism thesis CONFIRMED (40/81 emit; chain-variants 15/15; G4 knob z≈−1.0 in-range), the chassis finding, and the triage lineage (join hypothesis disconfirmed; coupling was the whole defect; fix = `measurement_report_writer.py` / MIGRATION v2.10).
6. **One spec line for the batch-2 gauntlet: per-cohort bucket keys** — proxy cohorts (int_light etc.) must never collapse into shared buckets again. Cheap at spec time, expensive to discover twice.
7. **Analysis + report ONLY.** No re-emit, no re-fight, no band re-tune in this unit.

## 3. HOLD discipline (your (b), sharpened) — the compute fires ONCE, as batch-2

No standalone calibrated re-emit/re-fight, ever. Under C2 the plain-caster band re-tune becomes **batch-2 config**, and the re-emit/re-fight *is* batch-2 itself — one batch, one fire, after the gen-path chain closes. (Doc-2 §5 anti-recommendation holds; the tiered-shells lever you preserved at `4cacf12` rides the same spec.)

## 4. Paperwork routing (already done / batched)

- Serial-emission tracker: chassis fork marked **✓ RULED C2** (gandalf, same commit as this note).
- Decisions-log: C2 registration **batches with the 2026-07-06 ruling set** on jack-ryan's next pass (faction-derivation stack + this).
- Review weight on the gamora unit: analysis+report, no production code → light jack-ryan read, your call on formality.

## 5. Sequence after the gamora unit returns (not now)

Leg-4 report lands → **pilot chain CLOSED** → gandalf authors the **batch-2 build spec** (consumes: Option-1 scope [summon composition + non-melee-INT composition], C2 band config + measured floor, tiered-shells lever, per-cohort bucket keys, variation build, ≥100/cell × 18 cells per faction-derivation-stack spec §10 step 2) → ARCHITECT pass gates run authorization → you dispatch batch-2 → derivation chain (elrond #18 consult → clustering → Matt cut-ratification) per spec §10 steps 3–5.

---

**Signed:** gandalf, 2026-07-06. Fire §2; hold §3; the rest is sequenced.
