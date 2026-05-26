# Gate-2 QA Submission — Phase 5 T4 Narration (Fix 1)

**Date:** 2026-05-26
**Author:** rocket
**QA target:** jack-ryan
**Gate level:** Gate-2 (implementation validation)
**Companion:** drax Fix 2 (WeaponSlot reconciliation) runs in parallel; Gate-2 fires once BOTH land

**Authority:** Matt 2026-05-26 via KR routing; gandalf amendment commit 3a3992b ratified

---

## Scope

Fix 1 of Phase 5 regen review fast-follow. Implements gandalf's Phase 5 spec amendment:
form-level T4 keystone narration LLM pass that fills the NULL/empty prose fields in
`spirit_guide_narration_metadata` across all 35 forms.

**Parent Gate-2:** `agentic_orchestration/qa/pending/` (parent Phase 5 skill-node naming —
Gate-2 PASS-with-WARN issued 2026-05-25). This Gate-2 is ADDITIVE — validates amendment
§ 7 criteria in addition to confirming parent § 6 criteria still PASS.

---

## What was implemented

**New file:** `~/Games/reincarnated-engine/src/reincarnated/generation/phase5_t4_narration.py`

- T4 narration LLM call per form (1 call × 35 forms post full-regen)
- 2-dimension cohesion-judge: kit_identity (0.60) + thematic_rationale_fit (0.40)
- Path A static-template fallback when LLM FAIL (per-strategy; ~5-6 distinct strings)
- Per-form telemetry: cohesion_score + breakdown + attempt# + cache_hit + is_fallback
- Calibration parameters per amendment § 4: T4_TEMPERATURE=0.75, T4_MAX_TOKENS=300,
  T4_COHESION_PASS_THRESHOLD=0.75, T4_MAX_ATTEMPTS=3

**Modified:** `~/Games/reincarnated-engine/src/reincarnated/generation/phase5_skill_naming.py`

- `apply_phase5_skill_naming()` return type changed: **2-tuple → 3-tuple**
  `(dicts, Phase5RunStats, Phase5T4RunStats | None)`
- New param `run_t4_narration: bool = True` — T4 narration fires AFTER skill-node naming
- Callers updated: generation run script + resmoke script

**Bug fix:** `~/Games/reincarnated-engine/src/reincarnated/generation/t4_wireup.py` line ~1047

- Old: `narration["manifestation"] = alteration_output.manifestation` (unconditional overwrite)
- New: `if narration.get("manifestation") is None: narration["manifestation"] = alteration_output.manifestation`
- Prevents clobbering LLM prose with tier-label enum when AlterationOutput wiring is fixed

**MIGRATION.md addendum:** `~/Games/reincarnated-engine/src/reincarnated/generation/MIGRATION.md`
entry `[2026-05-26] Phase 5 T4 Keystone Narration — Amendment (Fix 1)` — schema disambiguation
table, caller breaking-change note, deferred gap note.

---

## Smoke results (3-form LLM smoke; pre-Gate-2)

Forms: Rampart Knight (physical/european/DEFENSIVE_CONVERSION), Blade of Empires
(physical/middle_eastern/DEFENSIVE_CONVERSION), Menuki Bladedancer (physical/east_asian/TRADE_OFF)

| Metric | Result | Target |
|---|---|---|
| First-attempt PASS rate | 100% (3/3) | ≥ 70% |
| Re-roll rate | 0% | ≤ 15% |
| Final FAIL rate (Path A) | 0% | ≤ 5% |
| Label uniqueness | 100% | ≥ 90% |
| Cost / 3 forms | $0.0127 (~$0.15 / full run) | < G12 guard |

Sample narration quality (Rampart Knight — DEFENSIVE_CONVERSION):
- `alteration_type`: "Wrath Turned Rampart"
- `manifestation`: "The rage that would drive lesser warriors forward folds inward instead — armor plates resonate with a low, iron hum, and each wound that should stagger you hardens the steel, the pain transmuting into something dense and immovable."
- `thematic_rationale`: "The knight's fury was never meant to burn outward alone; the oldest castle walls were built from the same stubborn refusal to yield that now makes your body the fortification."
- `cohesion_score`: 0.84 (PASS)
- `tier_label preserved`: None (existing export state; AlterationOutput gap deferred)

---

## Acceptance criteria checklist (amendment § 7)

For jack-ryan to validate against full 35-form regen output (fires after Gate-2 PASS on
this + drax Fix 2):

- [ ] T4 narration LLM pass fires for ALL forms (35/35)
- [ ] `spirit_guide_narration_metadata["manifestation"]` non-None and non-empty across all 35 forms
- [ ] `spirit_guide_narration_metadata["thematic_rationale"]` non-empty across all 35 forms
- [ ] `spirit_guide_narration_metadata["alteration_type"]` narrated label (not enum) across all 35 forms
- [ ] `t4_alteration_output["thematic_rationale"]` non-empty across all 35 forms (top-level mirror)
- [ ] `t4_alteration_output["manifestation"]` (top-level) tier label semantics preserved (None or "T4_active"/"rank2_passive"/"rank3_passive" — NOT prose; should remain None until AlterationOutput wiring fixed)
- [ ] T4 narration cohesion-judge fires per form; `phase5_t4_narration_cohesion_score` in t4_alteration_output
- [ ] First-attempt PASS rate ≥ 70%
- [ ] Re-roll rate ≤ 15%
- [ ] Final FAIL rate (Path A fallback) ≤ 5% per run
- [ ] `alteration_type` label uniqueness ≥ 90% across 35 forms
- [ ] `apply_phase5_skill_naming()` 3-tuple return — callers handle correctly (verify no AttributeError on old 2-tuple unpack in scripts)
- [ ] t4_wireup.py overwrite guard present at emit_cross_seam_fields (line ~1047-1051)
- [ ] MIGRATION.md addendum authored with schema disambiguation table
- [ ] Cost-per-run delta reported in metadata.json (`phase5_t4_narration_stats`)

## Known gaps (pre-Gate-2 disclosure)

1. **AlterationOutput threading gap** — `t4_alteration_output["manifestation"]` (top-level tier label)
   remains None because AlterationOutput object is stored as plain dict and not reconstructed.
   Deferred to Cycle 13 v1.1+. t4_wireup.py overwrite guard protects prose slot.
   This is an existing gap predating this amendment; amendment does not introduce it.

2. **Full regen not fired in this dispatch** — KR controls regen fire-time per Gate-2 chain.
   Smoke validates implementation; full 35-form regen fires post-Gate-2 PASS.

3. **drax T4AlterationPanel narrated label display** — optional follow-on (§ 8.2) not in scope.
   The manifestation prose lands via thematic_rationale fallback chain regardless.

---

**Spec refs:**
- `canonical/story/phase-5-t4-narration-amendment-2026-05-26.md` (gandalf; commit 3a3992b) — PRIMARY
- `canonical/story/phase-5-cohesion-judge-calibration-spec-2026-05-25.md` § 7 (parent spec)

**Implementation files:**
- `~/Games/reincarnated-engine/src/reincarnated/generation/phase5_t4_narration.py` (new)
- `~/Games/reincarnated-engine/src/reincarnated/generation/phase5_skill_naming.py` (modified)
- `~/Games/reincarnated-engine/src/reincarnated/generation/t4_wireup.py` (bug fix)
- `~/Games/reincarnated-engine/src/reincarnated/generation/MIGRATION.md` (addendum)
- `~/Games/reincarnated-engine/scripts/v2_narrow_phase_5_generation_run_2026_05_25.py` (updated)
- `~/Games/reincarnated-engine/scripts/v2_narrow_phase_5_targeted_resmoke_2026_05_25.py` (updated)
