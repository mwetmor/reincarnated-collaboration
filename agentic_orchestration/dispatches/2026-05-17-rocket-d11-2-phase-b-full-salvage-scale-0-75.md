# 2026-05-17 — rocket — D11.2 Phase B: full 17-instance salvage at scale_factor=0.75

**Authority:** Phase A PHASE_B_AUTHORIZED verdict — smoke 5/5 PASS at scale=0.75 (gentlest sweep option). Gandalf advisory + jack-ryan Gate-1 + gamora math note all upstream.
**Type:** Pattern B — full salvage + sliding-gate convergence check; ~1-2 hours.
**Predecessor (just shipped):** rocket Phase A — tag `rocket/v1.15-d11-2-phase-a-lever-b-plus-smoke-1`; decision file at `reincarnated-engine/output/d11_2_smoke_decision.json`.
**Status:** 🟢 **ACTIVE — fire immediately. Auto-fire per gandalf handoff (no Matt escalation needed; PHASE_B_AUTHORIZED is the happy path).**

---

## Why this matters

Phase A smoke landed at the BEST possible outcome — first sweep point (scale=0.75, 25% DPS reduction) passed 5/5 representative instances including class_0031 worst-outlier. Identity preservation maximized; composite B+D not needed. This is the durable correction to the D11 cycle: empirical calibration via Discipline #17 outperformed math projection in our favor.

Phase B applies this scale across the remaining 12 hybrid_mage instances (5 already proven in smoke) and validates the sliding gate at full population scale. If gate clears → **CONVERGENCE LOCKED**; engine end-to-end healthy; ready for fresh new-season regen per Matt's stated goal ("develop a completely new LLM generated season once we feel those issues are resolved and converge many classes from it").

---

## Required reading

1. **Phase A completion record** — `agentic_orchestration/dispatches/2026-05-17-rocket-d11-2-phase-a-lever-b-impl-plus-smoke-runner.md` § completion (your verdict + delivered code paths)
2. **Phase A decision file** — `reincarnated-engine/output/d11_2_smoke_decision.json` (selected_scale=0.75, composite_d_active=false)
3. **D11.1 salvage pattern** — `reincarnated-engine/scripts/d11_1_post_process_salvage.py` (your reference for Phase B salvage script structure)
4. **Gamora math note** — `reincarnated-engine/src/reincarnated/simulation/math/d11-2-lever-b-and-smoke-gate.md` § 1 (Lever B algorithm; idempotency restore rule)
5. **Gandalf advisory** — `canonical/story/d11-2-structural-redesign-advisory-2026-05-17.md` § 7.4 (Phase B sliding gate spec; RETIRE clause if gate fails)
6. **balance_loop.py** — your kit-finalization + salvage entry point; lines 427-432 composite-D pattern (default False here)
7. **MIGRATION.md** — `reincarnated-engine/src/reincarnated/simulation/MIGRATION.md` v1.11 (append Phase B results in same entry)

---

## Scope — Phase B: 6 deliverables

### Deliverable 1 — Phase B salvage script

New script at `reincarnated-engine/scripts/d11_2_phase_b_full_salvage.py` (or your naming preference). Mirrors `d11_1_post_process_salvage.py` pattern, but:
- Iterates all 17 hybrid_mage instances across seasons 002011-015 (verify count + season distribution from staged seasons)
- For each instance: idempotency restore (divide out previous scale if balance_metadata has hybrid_mage_dps_scale_factor); then apply `_apply_dps_density_scale(skills, 0.75)` at kit finalization
- Re-run balance loop on each instance to get post-scale convergence verdict
- Persist updated balance_metadata (flat hybrid_mage_dps_scale_factor=0.75 + nested hybrid_mage_lever_b dict per jack-ryan condition 2)
- composite_d_active stays False (Phase A did not select composite)
- Logs per-instance: pre-modifier, post-modifier, pre-WR, post-WR, interior-vs-floor flag

### Deliverable 2 — Sliding gate evaluation

After re-salvage of all 17 instances, evaluate Phase B sliding gate per gandalf § 7.4:
- **Primary gate:** ≥10/17 instances converge at interior modifier (`final_modifier > 0.055` per existing floor-pin definition)
- **Fallback gate (not applicable here — we're at scale=0.75 not 0.55):** ≥12/17 at scale=0.55
- For scale=0.75: only the **primary gate ≥10/17** applies

If ≥10/17 pass: **PHASE_B_PASSED** → CONVERGENCE LOCKED.
If <10/17 pass: **PHASE_B_FAILED** → escalate to Matt with retire-vs-third-attempt decision.

### Deliverable 3 — Decision file output

Write structured decision at `reincarnated-engine/output/d11_2_phase_b_decision.json`:

```json
{
  "timestamp": "2026-05-17T...",
  "phase": "B",
  "scale_factor_applied": 0.75,
  "composite_d_active": false,
  "instances": [
    {
      "season_id": "002011",
      "class_id": "class_NNNN",
      "modifier_pre": <float>,
      "modifier_post": <float>,
      "wr_pre": <float>,
      "wr_post": <float>,
      "interior": <bool>
    }
    // 17 entries
  ],
  "interior_count": <int>,
  "gate_target": 10,
  "verdict": "PHASE_B_PASSED" | "PHASE_B_FAILED",
  "escalation_recommendation": null | "RETIRE_HYBRID_MAGE" | "THIRD_ATTEMPT"
}
```

### Deliverable 4 — Demo + loadout sync (post-pass only)

If PHASE_B_PASSED:
- Sync engine output → `reincarnated-demo/public/seasons/season_002011-015/classes.json` (rocket already has v1.13.2 / v1.14-d11.1-demo-sync pattern; mirror it)
- Sync engine output → `reincarnated-loadout/data/season_002011-015/classes/<id>.json` per-class files (rocket has v1.14-d11.1-loadout-sync pattern; mirror it)
- Verify drax-loadout per-class files updated; flag staleness gone

If PHASE_B_FAILED: do not sync; await Matt decision.

### Deliverable 5 — MIGRATION.md v1.11 amendment

Append Phase B results to existing v1.11 entry (per jack-ryan R11(b) deferral clause structure). Capture:
- Scale_factor applied: 0.75
- Composite_d_active: false
- Interior_count: <X>/17
- Phase B verdict
- Cross-seam impact (demo + loadout sync state if passed)

### Deliverable 6 — INFO callouts surfaced

Per jack-ryan Phase A INFO items:
- `consecrate` inclusion in `_is_damage_bearing` predicate — verify this works correctly for any hybrid_mage instance with consecrate skill in kit; log if anomalous
- ValueError guard for `previous_scale ≤ 0.0` in idempotency restore — confirm this hardening is in place from Phase A
- Mid-WR/mid-count instance cluster (0.65-0.73 WR / 5-6 damage-skill count) — note any prediction uncertainty in completion record if Phase B convergence rate in this band differs from non-cluster bands

---

## Acceptance criteria

- [ ] Phase B salvage script authored at named path
- [ ] All 17 hybrid_mage instances re-salvaged at scale=0.75 (idempotency restore + scale apply)
- [ ] Per-instance log captures pre/post modifier + WR + interior flag
- [ ] Phase B decision file written
- [ ] Sliding gate evaluated; verdict written (PHASE_B_PASSED or PHASE_B_FAILED)
- [ ] If passed: demo + loadout sync completed; staleness verified gone
- [ ] If failed: escalation file written; no sync; surface to Matt
- [ ] MIGRATION.md v1.11 amended with Phase B results
- [ ] `pytest` clean on simulation + generation seams
- [ ] PRE-SIGNAL § 14.1.1 before hive-log append (drax v1.16.1 hotfix in flight in parallel)
- [ ] AGENT_STATE STATE entry
- [ ] Tag `rocket/v1.16-d11-2-phase-b-full-salvage-1`

---

## Out of scope (DO NOT)

- ❌ DO NOT regen any seasons (Phase B is salvage-only; no LLM calls)
- ❌ DO NOT change scale_factor from 0.75 (Phase A selected; locked for Phase B)
- ❌ DO NOT activate composite_d (Phase A did not select; stays false)
- ❌ DO NOT touch engine logic beyond salvage application (no balance_loop changes)
- ❌ DO NOT pre-empt new-season regen (separate dispatch; gated on Phase B + Matt authorization)
- ❌ DO NOT touch drax seam (v1.16.1 hotfix in flight; parallel-safe)
- ❌ DO NOT escalate to Matt mid-execution unless verdict is PHASE_B_FAILED
- ❌ DO NOT push tag (ADR-006)

---

## Coordination

- **Predecessor:** rocket Phase A (just shipped; PHASE_B_AUTHORIZED at scale=0.75)
- **Parallel-safe with:** drax v1.16.1 hotfix (in flight; demo seam — different repo, no conflicts)
- **Triggers downstream (on PHASE_B_PASSED):** new-season regen authorization to Matt; star-lord telemetry column #119 follow-on; gear_pool size bump #118 follow-on
- **Triggers downstream (on PHASE_B_FAILED):** ESCALATE-TO-MATT with structured retire-vs-third-attempt data
- **PRE-SIGNAL § 14.1.1** before hive-log appends

---

## Why this completes the D11 cycle

After Phase B passes:
- Hybrid_mage joins all other archetypes at acceptable convergence rates
- D10 substrate-coherent generation + D11.2 Lever B fully landed
- Engine end-to-end healthy across all 7 substrates + all archetypes
- Ready for fresh new-season regen per Matt's stated goal: "develop a completely new LLM generated season once we feel those issues are resolved and converge many classes from it"
- D11.2 cycle becomes the canonical case study for Discipline #17 (empirical-calibration smoke gate before full-regen)

---

*Dispatched 2026-05-17 by knight-rider per Phase A handoff + gandalf authorized auto-fire path. ~1-2h Phase B. Append completion record + verdict + decision file path when done.*

---

## Completion record

**Completed:** 2026-05-17
**Agent:** rocket
**Tag:** `rocket/v1.16-d11-2-phase-b-full-salvage-1`
**Verdict:** PHASE_B_FAILED — 0/17 instances at interior modifier (gate: ≥10/17)
**Runtime:** 301.3s (5.0 min)

### Deliverables shipped

1. `scripts/d11_2_phase_b_full_salvage.py` — Phase B salvage script (idempotency restore + Lever B apply + sliding gate + escalation path + INFO callouts)
2. 17 classes.json + manifests updated with Phase B provenance across seasons 002011-015 (scale_factor=0.75, post_process_d11_2_phase_b=True, schema_version=v1.10)
3. `output/d11_2_phase_b_decision.json` — Phase B decision file (verdict + per-instance pre/post + diagnostic)
4. Demo + loadout sync: NOT executed (gate failed; dispatch rule)
5. MIGRATION.md v1.11 amended with Phase B results + gear-catalog mismatch finding
6. INFO callouts resolved:
   - consecrate in _is_damage_bearing: verified correct; no instance had consecrate skills (no holy-substrate hybrid_mage in 002011-015)
   - ValueError guard for previous_scale≤0: enforced in _restore_pre_lever_b(); not triggered
   - Mid-WR/mid-count cluster: 4 instances flagged (class_0003, class_0004, class_0015, class_0047); all floor-pinned — cluster uncertainty confirmed (prediction uncertainty is real, not a specific failure mode here)

### Phase B per-instance results

| Season | Class | mod_pre | mod_post | wr_pre | wr_post | interior |
|---|---|---|---|---|---|---|
| 002011 | class_0001 | 0.050 | 0.050 | 0.611 | 0.622 | False |
| 002011 | class_0002 | 0.050 | 0.050 | 0.656 | 0.678 | False |
| 002011 | class_0003 | 0.050 | 0.050 | 0.667 | 0.644 | False |
| 002011 | class_0004 | 0.050 | 0.050 | 0.656 | 0.633 | False |
| 002011 | class_0007 | 0.050 | 0.050 | 0.656 | 0.600 | False |
| 002012 | class_0012 | 0.050 | 0.050 | 0.744 | 0.711 | False |
| 002012 | class_0013 | 0.050 | 0.050 | 0.778 | 0.767 | False |
| 002012 | class_0014 | 0.050 | 0.050 | 0.744 | 0.733 | False |
| 002012 | class_0015 | 0.050 | 0.050 | 0.689 | 0.656 | False |
| 002013 | class_0029 | 0.050 | 0.050 | 0.733 | 0.756 | False |
| 002013 | class_0031 | 0.050 | 0.050 | 0.867 | 0.844 | False |
| 002014 | class_0039 | 0.050 | 0.050 | 0.689 | 0.633 | False |
| 002014 | class_0040 | 0.050 | 0.050 | 0.622 | 0.622 | False |
| 002014 | class_0047 | 0.050 | 0.050 | 0.678 | 0.611 | False |
| 002014 | class_0054 | 0.050 | 0.050 | 0.567 | 0.589 | False |
| 002015 | class_0056 | 0.050 | 0.050 | 0.656 | 0.656 | False |
| 002015 | class_0061 | 0.050 | 0.050 | 0.689 | 0.622 | False |

### Critical finding — smoke/Phase B environment mismatch

Phase A smoke ran WITHOUT gear_catalog (no Monte Carlo gear sampling). Phase B runs WITH gear_catalog (matching D11.1 environment — 19 base_items, 20 effect_pool per season). Gear buffs hybrid_mage effective fight performance, requiring a deeper DPS reduction than 25% to achieve interior convergence.

Cross-check on smoke instances:

| Instance | Smoke WR (no gear) | Phase B WR (with gear) | Smoke modifier | Phase B modifier |
|---|---|---|---|---|
| class_0007 | 0.500 | 0.600 | 0.173 | 0.050 |
| class_0054 | 0.411 | 0.589 | 0.073 | 0.050 |
| class_0031 | 0.500 | 0.844 | 0.297 | 0.050 |

Phase A smoke 5/5 PASS was a false positive. Phase B 0/17 is the authoritative full-environment result.

### pytest

339 passed (test_balance_loop + test_combat_simulator + test_resistance_matrix + test_gate3b_ms_consumption). All assertions clean.

### Decision file

`reincarnated-engine/output/d11_2_phase_b_decision.json`

### Triggers

**ESCALATE TO MATT.** Options in decision file:
- OPTION_A: Re-run smoke with gear_catalog to recalibrate magnitude (deeper scale or composite needed)
- OPTION_B: Composite B+D (scale=0.65 + 5% HP penalty) re-tested with gear_catalog
- OPTION_C: RETIRE_HYBRID_MAGE from canonical-7 for current season set; fresh regen excludes it (Matt's stated goal: "develop a completely new LLM generated season once we feel those issues are resolved")
- OPTION_D: Structural D12+ redesign (hybrid_mage kit composition)
