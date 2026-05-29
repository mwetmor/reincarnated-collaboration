# DISPATCH — Gamora Cycle 14 A2-1-FIX: phase7_bridge.py Cross-Seam Import Repair (Phase A2 Dispatch 1-FIX)

**Authored:** 2026-05-29 (Mode A Phase A2 unattended cascade A2-1-FIX; routes rocket A2-1 INTERIM FAIL → gamora seam-owner fix → rocket A2-1 re-fire)
**Author:** knight-rider (Cycle 14 Mode A hive-mind orchestrator)
**Recipient:** gamora (simulation seam; owns `src/reincarnated/simulation/phase7_bridge.py`)
**Pattern:** Pattern A-light (2-line absolute-import fix + verification + auto-commit + tag + return); optional secondary Phase 3 quality-vector anomaly investigation per § 2
**Expected effort:** ~10-20 min (fix + verification + commit + optional secondary investigation; secondary may defer)
**Status:** PENDING — fires on receipt
**Authority:** Matt 2026-05-28 Phase A2 cascade authorization composes with hive-mind decision-routing (Matt 2026-05-23 verbatim — seam-owner decides in-scope work; KR routes; Matt last-resort escalation); R48.4 single-seam (rocket sub-agent returned; gamora is the only sub-agent firing)

---

## 0. CONTEXT (read first — 3 min)

### 0.1 Rocket A2-1 INTERIM FAIL surface (verified by KR per Disc #42a meta-observation 5)

Rocket fired Wave 5 season_001 PRODUCTION cascade (dispatch `2026-05-29-rocket-cycle-14-wave-5-season-001-production-fire.md`) and surfaced INTERIM FAIL: 0/18 kits emit at Phase 7 (vs ≥12/18 D9 threshold).

Pipeline result summary:
- Phase 2 — 18 kits generated (earth × 4, wind × 4, fire × 5, water × 5) ✅
- Phase 3 — **13/18 WR-bracket PASS** at gauntlet sim layer; 37,360 fights (validates Path α architecture at THIS layer) ✅
- Phase 4 — 18/18 ACCEPTED to kit_archive ✅
- Phase 5 — $0.00 LLM cost; 3 placeholder clusters (faction_visibility=invisible; cohesion judge LLM NOT exercised because Phase 7 0 KPM short-circuited)
- Phase 7 — **0/18 shipped_worthy** ❌ BLOCKED by `simulation/phase7_bridge.py` import bug

**Disc #11 grep `synthetic_mode`:** ZERO functional code (PASS).
**LLM cost:** $0.00 (well within $50 soft cap; no budget concern).

### 0.2 KR verification of the bug (Disc #42a meta-observation 5 — verify artifact against attestation)

KR read `src/reincarnated/simulation/phase7_bridge.py` lines 195-220 and confirms rocket's diagnosis:

```python
# Lines 195-197 actual content:
        try:
            from .ability_schema import AbilityEffect, AbilityTiming
            from .skill_schema import Skill
```

The relative imports `.ability_schema` + `.skill_schema` resolve to `reincarnated.simulation.ability_schema` + `reincarnated.simulation.skill_schema` — neither file exists in the simulation seam. Both modules live in `reincarnated.generation/`:

```
$ ls reincarnated/generation/ability_schema.py reincarnated/generation/skill_schema.py
# both present
$ ls reincarnated/simulation/ability_schema.py reincarnated/simulation/skill_schema.py
# both MISSING (ls error code 1)
```

The `try/except ImportError` block at lines 195+ catches the ImportError silently and returns an empty skills list. With no skills, `Phase7SyntheticKit` runs auto-attack only → 0 KPM in-band → 0 season_emit across all 18 kits.

Code comment at lines 191-193 already acknowledges the construction is copied from generation seam:
```
"Same skill construction as season_generation_pipeline._SyntheticPlayerClass
(code-citation: season_generation_pipeline.py:910-934)."
```

The imports were left as relative without correcting for the cross-seam path — a latent bug masked by smoke mode (`use_mock_gauntlet=True` bypasses `_build_synthetic_skills` entirely; PRE-Path-α 3/18 emit was hitting the same bug in a different configuration).

### 0.3 Why this is a BUG FIX (NOT a Path α architectural failure)

**Path α architecture is empirically validated at the Phase 3 gauntlet sim layer:** 13/18 WR-bracket PASS exceeds the conceptual ≥12/18 D9 threshold at that layer (per rocket attestation; KR routes A2-1 re-fire to confirm Phase 7 acceptance reproduces this signal post-fix).

**Disc #42a Q6 semantic-stability vigilance for re-fire:** Phase 3 13/18 ≠ Phase 7 ≥12/18 acceptance. These are different measurement layers. Phase 7 acceptance ALSO gates on cohesion judge LLM verdicts (dispatch § 1.4 permits up to 6 LLM exclusions). 13/18 at Phase 3 → expected post-fix Phase 7 emit between 7/18 (worst case: 6 LLM exclusions) and 13/18 (best case: 0 LLM exclusions). Path α is FULLY validated only when Phase 7 emits ≥12/18 with real LLM cohesion judge exercised.

A2-1-FIX (this dispatch) repairs the bug. Rocket A2-1 re-fire empirically validates Path α at the Phase 7 acceptance layer.

---

## 1. THE TASK (PRIMARY — required)

### 1.1 The fix

Edit `~/Games/reincarnated-engine/src/reincarnated/simulation/phase7_bridge.py` lines 196-197.

**Change FROM:**
```python
            from .ability_schema import AbilityEffect, AbilityTiming
            from .skill_schema import Skill
```

**Change TO (absolute imports):**
```python
            from reincarnated.generation.ability_schema import AbilityEffect, AbilityTiming
            from reincarnated.generation.skill_schema import Skill
```

Zero logic change. Pure import path correction.

### 1.2 Verification (REQUIRED before commit)

Verify the fix works:

1. **Static import verification:** `python -c "from reincarnated.simulation.phase7_bridge import Phase7SyntheticKit"` should resolve without ImportError
2. **Skill construction smoke:** instantiate `Phase7SyntheticKit` with a known `kit_id` + `element` + `bc_cell_id` triple; assert `kit.skills` is non-empty (list length 1; primary_attack skill present)
3. **Optional fuller verification:** run any existing test that exercises `phase7_bridge.py` (e.g., `pytest -k phase7_bridge`); if no such test exists, the smoke instantiation in (2) suffices
4. **Disc #11 regression check:** `grep -rn "synthetic_mode" src/reincarnated/simulation/ --include="*.py"` returns ZERO functional code (verify the fix doesn't reintroduce synthetic_mode flag)

### 1.3 MIGRATION.md scope

This is an intra-engine bug fix touching `simulation/` only. No cross-seam contract change (no fixture key add/rename/remove; no inter-seam dict shape change). MIGRATION.md NOT required per ADR-004 — but a brief `simulation/MIGRATION.md` entry noting the import-path correction + behavior change ("phase7 synthetic kits now build proper primary_attack skill; pre-fix behavior was empty skills list silently") is good hygiene per Discipline #11 + #12 attribution clarity.

### 1.4 Commit + tag

Per CLAUDE.md addendum 2026-05-25 auto-commit work-products of authorized cascade work:

- Engine commit message convention: `gamora: A2-1-FIX phase7_bridge cross-seam absolute-imports — restores skill construction (Phase A2 A2-1-FIX)`
- Engine tag convention: `gamora/v2.12-a2-1-fix-phase7-bridge-imports-1` (or your seam convention)
- Collab commit: append completion record to this dispatch file

DO NOT push — KR fires push AFTER A2-2 Gate-2 PASS per per-workstream pattern Matt-locked (A2-1 re-fire + A2-2 critique-pair still pending).

### 1.5 Report format (Completion record append)

Append a `## Completion record` section to this dispatch with:

1. **VERDICT** — single line: "A2-1-FIX phase7_bridge cross-seam imports → absolute; verification PASS; bug fix complete; A2-1 re-fire unblocked"
2. **Engine commit hash + tag**
3. **Verification results** — static import + skill construction smoke + (optional) test outcome
4. **Disc #11 grep result** — `synthetic_mode` ZERO functional code confirmed
5. **MIGRATION.md location** (if added)
6. **Secondary Phase 3 quality-vector investigation** — per § 2 below (DEFERRED or BUNDLED)
7. **Any anomalies surfaced** during fix verification

---

## 2. THE TASK (SECONDARY — optional; gamora's call to bundle or defer)

### 2.1 Phase 3 quality-vector anomaly (rocket A2-1 surfaced as non-blocking)

Rocket's A2-1 pipeline run produced 18 WARNs at Phase 3 quality-vector derivation: "no encounter_results found." All 18 kits got neutral 0.5 quality vectors as a result. The orchestrator's `_derive_quality_vector()` could not find `encounter_results` in the Phase 3 gauntlet JSON.

This is a gamora-seam concern — Phase 3 gauntlet JSON shape is owned by `gauntlet_sim.py`. The orchestrator's `_derive_quality_vector()` consumer expects an `encounter_results` field that the gauntlet JSON doesn't appear to emit (or emits under a different name).

### 2.2 Gamora's call

**Option B-1 — BUNDLE in this dispatch:** if quick diagnostic shows the issue is a small field-rename / field-not-emitted bug fixable in <30 min, gamora addresses it in the same engine commit OR a sibling commit in the same tag-group, and attests in this completion record.

**Option B-2 — DEFER to separate dispatch:** if diagnostic shows the issue requires more substantive investigation (e.g., `_derive_quality_vector()` semantics need design review with rocket or KR), gamora notes the deferral in this completion record, and KR routes a separate dispatch post-A2-1 re-fire close.

**Non-blocking for A2-1:** quality vectors all-neutral-0.5 doesn't BLOCK Phase 7 acceptance — it produces unhelpful uniform clustering at Phase 5, but Phase 7 emit count is independent of quality vector content. Rocket's A2-1 re-fire can proceed without this fix; A2-1 may still emit ≥12/18 with degraded quality-vector signal (or may not, depending on cohesion judge LLM behavior on uniform-vector input).

**Recommended disposition:** quick diagnostic (~10 min) at the start of this dispatch; bundle if trivial, defer otherwise. Gamora's call.

---

## 3. CROSS-SEAM CONTRACT CHANGE? (Principle 6)

**No** — this dispatch is an intra-engine bug fix touching `simulation/phase7_bridge.py` only. No additive/renamed/removed fields on cross-seam fixtures.

**Round-trip clause:** A2-1 re-fire (post-fix) IS the cross-seam round-trip exercising rocket → gamora → star-lord → phase 7 acceptance. Inherent to the cascade.

---

## 4. QUALITY CRITERION (KR OP § 3.11)

**Game-quality goal this dispatch serves:** unblocks the empirical validation of Path α v1 architecture at the Phase 7 acceptance layer (post-LLM cohesion judge exercised) by repairing the import bug that prevented Phase 7 synthetic kit skill construction. Engine > Game > Phase orientation: engine architectural integrity preserved (Path α validated at Phase 3 confirmed by 13/18 WR-bracket PASS); this fix removes the bug masking Phase 7's measurement of the architectural signal.

**Refutation conditions:**
- This dispatch contradicts canonical anchor X — refute via gauntlet_sim + phase7_bridge are both gamora seam; no canonical contradiction
- Alternative execution Y serves the named quality goal better — refute via Disc #42a Q1: smallest-surface fix (2-line import); no smaller alternative
- Acceptance criteria can pass without advancing the quality goal — refute via verification step 1.2 (skill construction smoke); criteria-passes-only-if-bug-actually-fixed
- Dispatch framing pre-commits to a decision Matt has not ratified — NO; routing to gamora is in-scope per hive-mind decision-routing
- Dispatch introduces a pre-authored taxonomy without justification (#41 candidate) — N/A
- Dispatch introduces a scaffold value not flagged as pending-decision (#40) — N/A

If any refutation condition triggers, SURFACE TO KR before fix.

---

## 5. OUT OF SCOPE

- ❌ Any Path α architectural change (Path α is validated at Phase 3 layer; this is a downstream-layer bug fix)
- ❌ Any change to skill construction logic (only import path corrected)
- ❌ Cycle 16+ BC axis expansion impl
- ❌ Two-layer T4 architectural amendment
- ❌ Re-firing the full season production pipeline (rocket's seam; KR routes rocket A2-1 re-fire after this dispatch closes)
- ❌ Jack-ryan Gate-2 review (Phase A2-2 scope after rocket A2-1 re-fire closes)
- ❌ Matt v1 tag ratification (Phase A2-7)
- ❌ Pushing to remote (per-workstream push pattern fires AFTER A2-2 Gate-2 PASS)
- ❌ Parallel sub-agent fan-out under R48.4 (rocket released; only gamora running)

---

## 6. RISKS + COMPLICATIONS

- **Verification gap:** if no test exercises `phase7_bridge.py`, gamora's smoke instantiation in § 1.2 step 2 IS the verification; no fallback. Make sure the smoke construction actually exercises the import (i.e., calls `Phase7SyntheticKit.__init__` such that `_build_synthetic_skills` fires).
- **Circular-import risk:** the comment at line 193 references "module-load circular dependencies" as the reason imports were deferred. The absolute-import correction may re-expose the original circular-import concern. If so: 
  - Diagnose the circular-import chain
  - Determine if the deferred-import-with-absolute-path pattern still resolves at runtime (i.e., still deferred inside the function body — only the path changes)
  - If runtime resolution works, proceed with absolute imports
  - If circular-import re-emerges, SURFACE TO KR for design call (this becomes a routing-design discussion, not just a bug fix)
- **Disc #42a Q4 measurement-context for re-fire:** rocket's claim "Phase 3 13/18 = Path α validated" is partially overcommitted. Phase 7 acceptance also gates on cohesion judge LLM exclusions. The re-fire's Phase 7 emit result is the FULL validation; Phase 3 is a useful proxy but not the full signal. (This is forward-looking for rocket; gamora's responsibility ends at A2-1-FIX completion.)
- **Secondary anomaly bundling:** Phase 3 quality-vector all-neutral-0.5 is non-blocking but routes more deeply if the gauntlet JSON shape needs design change. Use the Option B-1 vs B-2 disposition framework at § 2 to decide.

---

## 7. URGENCY + SEQUENCING

**Fires after A2-1 INTERIM FAIL surface; precedes A2-1 re-fire.**

Single-seam sequencing per R48.4 preserved (rocket released; gamora is the only sub-agent).

On A2-1-FIX completion → KR fires rocket A2-1 re-fire (re-attempt of season_001 production cascade) under R48.4 single-seam.

On rocket A2-1 re-fire PASS → KR fires A2-2 (jack-ryan + gandalf critique-pair Gate-2 Pattern E autonomous-ratification).

---

## 8. SURFACING-TO-KR PROTOCOL

Surface back to KR via completion record on this dispatch when:

- ✅ Fix lands + verification PASS + commit + tag — normal close (KR fires rocket A2-1 re-fire)
- ⚠️ Circular-import re-emerges blocking absolute-import path — SURFACE for design call
- ⚠️ Verification step 1.2 (skill construction smoke) FAILS post-fix — SURFACE with diagnosis
- ⚠️ Disc #11 grep returns `synthetic_mode` functional code — SURFACE (regression)
- ⚠️ Disc #48 R48.5 mid-fix RAM pressure (< 500 MB available) — pause + SURFACE
- ⚠️ Phase 3 quality-vector anomaly diagnosis reveals load-bearing design concern — SURFACE with options
- 🚨 Substantial unexpected failure mode not covered above — SURFACE

Per Matt 2026-05-23 hive-mind decision-routing: gamora decides in-scope simulation-seam work; KR routes; Matt last-resort escalation.

---

## 9. REFERENCES

- `agentic_orchestration/dispatches/2026-05-29-rocket-cycle-14-wave-5-season-001-production-fire.md` — A2-1 dispatch + rocket interim FAIL completion record
- `agentic_orchestration/cycle-14-path-alpha-v1-closure-record-2026-05-28.md` — Path α v1 engine readiness gate (validated at gauntlet sim layer)
- `agentic_orchestration/cycle-14-hive-mind-state.md` — Cycle 14 hive-mind state file (Wave 5 row FIRING)
- `agentic_orchestration/gandalf/pushback/2026-05-28-framing-audit-three-instance-case.md` — Disc #42a architectural argument (operational at dispatch consumption + completion attestation)
- `~/Games/reincarnated-engine/src/reincarnated/simulation/phase7_bridge.py` — file to fix (lines 196-197)
- `~/Games/reincarnated-engine/src/reincarnated/generation/ability_schema.py` + `skill_schema.py` — correct module location
- `~/Games/reincarnated-engine/src/reincarnated/generation/season_generation_pipeline.py:910-934` — original code-citation reference (per phase7_bridge.py line 192)
- `~/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md` — Discipline #11 + #12 + #21 + #22 + #42a + #48 active

---

**KR signature:** authored per hive-mind decision-routing (Matt 2026-05-23 verbatim — seam-owner decides; collaboration resolves; Matt last-resort) + R48.4 single-seam (rocket released; gamora firing alone) + Disc #42a meta-observation 5 self-vigilance (artifact verified against rocket attestation) + auto-commit per CLAUDE.md addendum.

This dispatch is the cheapest surface-able-by-collaboration repair of A2-1 INTERIM FAIL. 2-line absolute-import fix; verification; commit; tag; hand back to KR for rocket A2-1 re-fire under R48.4.

A2-1-FIX PASS → rocket A2-1 re-fire → expected Phase 7 emit reproducing Phase 3 13/18 signal with cohesion judge LLM exclusions applied → A2-2 Gate-2 Pattern E autonomous-ratification → cascade continues toward Cycle 14 v1 MVP D9 close.
