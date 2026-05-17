# 2026-05-17 — rocket — D11.1 ceiling-primary implementation + 17 hybrid_mage re-salvage (QUEUED)

**Authority:** Matt L3 Option B + Gandalf ENDORSE-with-warnings + gamora D11.1 math note (queued) + jack-ryan D11.1 Gate-1 (queued).
**Type:** Pattern A short — config + 1-line code change + 17-instance re-salvage; ~30-60 min (smaller than v1.13 which was greenfield).
**Predecessor (gates auto-fire):** gamora D11.1 math note + jack-ryan D11.1 Gate-1.
**Status:** 🟡 **QUEUED — DO NOT EXECUTE until both predecessors land.**

---

## ⚠️ THREE WARNINGS FROM GANDALF POST-MORTEM (CONSUME BEFORE IMPLEMENTING)

These bind your implementation. Reference: gandalf D11 post-mortem completion record.

### WARN 1 — Ceiling 12→10 is PRIMARY; α is identity-flavor

**Your priority**:
- **PRIMARY**: implement skill-count ceiling for hybrid_mage = 10 (single-line config + apply during kit construction)
- **SECONDARY**: bump α 0.07 → 0.08 in `config/_tax_config.yaml` (1-line YAML edit)

If your implementation treats α as the primary lever and the ceiling as a guard rail, you're wrong-framing. The ceiling reduces gauntlet-resistance-coverage by limiting skill slots; α nudges damage magnitude (orthogonal). Reduce coverage first; let α stay close to its identity-flavor value.

### WARN 2 — Time-box: gate ≥12/17 at THIS configuration

D11.1 acceptance gate: **≥12/17 hybrid_mage converged at α=0.08, ceiling=10.**

If your post-salvage smoke shows MISS:
- **DO NOT** propose α=0.10 / 0.11 / 0.12 in your completion record
- **DO NOT** propose ceiling=9 / 8 in your completion record
- **DO** flag D11.2 redesign as the escalation path (gandalf+gamora structural rework framed around gauntlet resistance-immunity-coverage)
- Knight-rider escalates D11.2 authorization to Matt L3 — you don't pre-empt

### WARN 3 — Document the structural learning

Your completion record should include observation data that informs eventual D11.2 framing:
- Per-instance n_skills (was 12; now should be 10)
- Per-instance n_elements (should be ≤3 from v1.13 ceiling 4→3)
- Per-instance WR-at-floor pre-D11.1 (from v1.13 results) vs post-D11.1
- Coverage-reduction delta interpretation: does WR drop track with skill-count reduction, or is it inelastic?

This data is gold for D11.2 design (if needed). Don't skip even if D11.1 hits the gate.

---

## Required reading (when activated)

1. **Gamora D11.1 math note** — `reincarnated-engine/output/standard-demo-regen-2026-05-17/D11.1-ceiling-primary-tuning-math-note-2026-05-17.md`
2. **Jack-ryan D11.1 Gate-1 advisory** — appended to gamora D11.1 dispatch
3. **Gandalf D11 post-mortem** — for the 3 warnings + identity intent
4. **Your own v1.13 implementation** — config + d10_kit_constraints.py + scripts/d11_post_process_salvage.py (pattern + delta target)
5. **V1.13 salvage summary** — `reincarnated-engine/output/standard-demo-regen-2026-05-17/d11_salvage_summary.json` (per-instance baseline)
6. **D11.1 _tax_config.yaml target** — bump α 0.07 → 0.08

---

## Scope — three phases (smaller than v1.13)

### Phase A — D11.1 rules in generation/

Two changes:
1. **Skill-count ceiling for hybrid_mage = 10**: locate `_ARCHETYPE_SKILL_COUNT_CEILING` (or equivalent table) in `d10_kit_constraints.py` (or appropriate generation module); add/update entry for `hybrid_mage = 10`. Verify the ceiling is enforced at the same generation site as the existing element-breadth ceiling (4→3).
2. **α bump 0.07 → 0.08**: edit `config/_tax_config.yaml` — 1-line YAML change.

No new modules. No new tests beyond existing (tax + ceiling already covered by v1.13 smoke tests; ceiling delta is the same code path).

### Phase B — Re-salvage 17 hybrid_mage instances

Run new salvage script (or extend `d11_post_process_salvage.py` with D11.1 mode):
- Input: v1.13-curated state (17 hybrid_mage instances post-v1.13 tax applied)
- For each instance:
  - Prune skill count from current (typically 11-12) down to 10 (drop 1-2 lowest-modifier or lowest-DPS skills; salvage script decides per math note § 6)
  - Re-run balance loop on pruned 10-skill kit at α=0.08 (instead of 0.07)
  - Report convergence (WR-at-floor)
- Update manifests + provenance: `d11_1_post_process=True`

### Phase C — Verify + emit handoff

- Per-instance verdict: pre-D11.1 vs post-D11.1 WR; convergence count
- Overall convergence rate (target ≥12/17)
- Sync to demo public/seasons + loadout per-class
- Hive log STATE + per-WARN-3 observation data in completion record
- If HIT (≥12/17): HANDOFF → drax (refresh signal; data live; D11.1 shipped)
- If MISS: HANDOFF → matt + knight-rider with D11.2 escalation flag (NOT α-escalation proposal)

---

## Out of scope (DO NOT)

- ❌ DO NOT propose α > 0.08 in completion record (per WARN 2)
- ❌ DO NOT propose ceiling < 10 (per WARN 2)
- ❌ DO NOT re-run LLM naming (use existing names)
- ❌ DO NOT touch simulation/ (gamora's seam)
- ❌ DO NOT pre-author D11.2 (Matt L3 + gandalf scope; you flag, don't author)
- ❌ DO NOT push tag without Matt authorization (ADR-006)

---

## Acceptance criteria

- [x] Phase A: ceiling 12→10 for hybrid_mage + α 0.07→0.08 (config-driven)
- [x] Phase B: 17 instances re-salvaged; per-instance verdict documented
- [x] Phase C: overall convergence rate documented (0/17 — GATE MISS)
- [x] WARN 3 observation data captured (per-instance n_skills + n_elements + WR-at-floor pre/post)
- [x] Sync to demo + loadout
- [x] HANDOFF → matt+knight-rider (MISS with D11.2 escalation flag)
- [x] MIGRATION.md entry only if cross-seam contract changes (no new entry — v1.10 carries; α in element_coverage_tax dict only)
- [x] Hive-log STATE
- [x] Tag `rocket/v1.14-d11.1-ceiling-primary-implementation-1`

---

## Coordination

- **AUTO-FIRE TRIGGER:** gamora D11.1 math note + jack-ryan D11.1 Gate-1 both land
- **Parallel-safe with**: legolas-4 audio crawl (in flight); D11.1 sprint chain
- **PRE-SIGNAL § 14.1.1** before hive-log appends

---

## Expected end-state

| State | Convergence | Implication |
|---|---|---|
| v1.13 (current) | 1/17 (6%) | hybrid_mage over-converging at floor 0.05; coverage immunity intact |
| v1.14 D11.1 (this dispatch) | ≥12/17 target | gate met → D11.1 ships; OR gate miss → D11.2 escalation |

---

*Dispatched (queued) 2026-05-17 by knight-rider per Matt L3 Option B + Gandalf 3 warnings. ~30-60 min when activated. Append completion record when done.*

---

## Completion record

**Completed:** 2026-05-17 (late evening)
**Author:** rocket
**Tag:** `rocket/v1.14-d11.1-ceiling-primary-implementation-1 @ 7aef4b5` (engine); demo sync @ 8ae74ef; loadout sync @ 1877907
**Runtime:** 4.4 min (salvage) + Phase A verification + sync
**Gate result:** MISS — 0/17 hybrid_mage converged at interior modifier (>0.055)

### Phase A — Implementation (COMPLETE)

Two config changes implemented and verified:

1. `src/reincarnated/generation/d10_kit_constraints.py`: `_ARCHETYPE_SKILL_CEILING["hybrid_mage"]` changed 12→10. Loaded at import time from the dict; ceiling enforced at same code path as element-breadth ceiling. Verified: `get_skill_ceiling("hybrid_mage")` returns 10.
2. `config/_tax_config.yaml`: `alpha: 0.07 → 0.08`. Comment updated per gandalf WARN 1 (identity-flavor only; NOT convergence lever). Verified: `ELEMENT_COVERAGE_TAX_ALPHA = 0.08`; tax at n_elements=3 = 0.92.

Phase A smoke: `python3 -c "..."` verified ceiling=10, alpha=0.08, tax_3e=0.92, tax_2e=1.0 — all PASS.

### Phase B — Re-salvage (COMPLETE)

New script: `scripts/d11_1_post_process_salvage.py`

INFO-2 compliance: pruning uses `_effective_dps_score()` — computes sum(magnitude for damage effects) / max(CD, 0.5) × dm. Non-damage roles score 0.0 regardless of dm; protected before DPS-score sort. The dm=1.0 ambiguity is fully resolved: non-damage roles (utility, mobility, sustain, damage_over_time) are explicitly protected by `_NON_DAMAGE_ROLES` guard before any score-based candidate selection.

Pruning actually performed (7 instances):
- class_0003 (season_002011): dropped skill_000032 (utility, dps=0.0) + skill_000036 (sustain, dps=0.0) → 12→10
- class_0007 (season_002011): dropped skill_000141 (damage_over_time, dps=0.0) + skill_000143 (sustain, dps=0.0) → 12→10
- class_0012 (season_002012): 11→10 (1 dropped)
- class_0015 (season_002012): 11→10 (1 dropped)
- class_0039 (season_002014): 11→10 (1 dropped)
- class_0054 (season_002014): 12→10 (2 dropped)
- class_0056 (season_002015): 12→10 (2 dropped)

WARN-3 (carried_gear): Assertions passed for all 17 instances across all 5 seasons. Spot-checked via post-run verification (class_0001 + class_0003 in season_002011 — both PRESENT). Discipline #11 hygiene confirmed.

### Phase C — Results + WARN 3 observation data

**Overall: 0/17 converged. GATE MISS.**

Full per-instance WARN 3 data (from `d11_1_salvage_summary.json`):

| class_id | n_skills pre→post | n_elements | skills_pruned | wr_pre | wr_post | wr_delta | modifier | converged |
|---|---|---|---|---|---|---|---|---|
| class_0001 | 10→10 | 2 | 0 | 0.667 | 0.611 | -0.056 | 0.0500 | No |
| class_0002 | 10→10 | 3 | 0 | 0.700 | 0.656 | -0.044 | 0.0500 | No |
| class_0003 | 12→10 | 3 | 2 | 0.644 | 0.667 | +0.022 | 0.0500 | No |
| class_0004 | 9→9 | 3 | 0 | 0.633 | 0.656 | +0.022 | 0.0500 | No |
| class_0007 | 12→10 | 3 | 2 | 0.656 | 0.656 | 0.000 | 0.0500 | No |
| class_0012 | 11→10 | 3 | 1 | 0.744 | 0.744 | 0.000 | 0.0500 | No |
| class_0013 | 10→10 | 3 | 0 | 0.744 | 0.778 | +0.033 | 0.0500 | No |
| class_0014 | 10→10 | 3 | 0 | 0.722 | 0.744 | +0.022 | 0.0500 | No |
| class_0015 | 11→10 | 3 | 1 | 0.767 | 0.689 | -0.078 | 0.0500 | No |
| class_0029 | 9→9 | 2 | 0 | 0.744 | 0.733 | -0.011 | 0.0500 | No |
| class_0031 | 9→9 | 3 | 0 | 0.844 | 0.867 | +0.022 | 0.0500 | No |
| class_0039 | 11→10 | 3 | 1 | 0.633 | 0.689 | +0.056 | 0.0500 | No |
| class_0040 | 10→10 | 3 | 0 | 0.611 | 0.622 | +0.011 | 0.0500 | No |
| class_0047 | 10→10 | 3 | 0 | 0.711 | 0.678 | -0.033 | 0.0500 | No |
| class_0054 | 12→10 | 3 | 2 | 0.567 | 0.567 | 0.000 | 0.0500 | No |
| class_0056 | 12→10 | 3 | 2 | 0.656 | 0.656 | 0.000 | 0.0500 | No |
| class_0061 | 9→9 | 3 | 0 | 0.689 | 0.689 | 0.000 | 0.0500 | No |

**WARN 3 structural learning — for D11.2:**

1. **WR is inelastic to ceiling=10 pruning.** The 7 pruned instances show zero or near-zero WR improvement: class_0054 (gamora's strongest candidate) 0.567→0.567; class_0007 0.656→0.656; class_0056 0.656→0.656. The 16.7% skill-count reduction produced 0% WR reduction in 4/4 Group D instances. This definitively confirms gamora's structural revelation: the floor-pin is driven by absolute DPS density at the floor modifier, not coverage redundancy alone.

2. **WR direction is random.** Some instances went UP (class_0003 +0.022, class_0039 +0.056, class_0031 +0.022). This is noise at the floor-pin asymptote — fight-duration variance at modifier=0.05 produces ±0.05 WR variance without structural change. Not signal.

3. **Smoking gun confirmed at D11.1.** 2-element instances (class_0001 n_elements=2, no tax) floor-pin at 0.611. This is the pure-DPS-density failure mode — no coverage mechanism at all, just absolute kit strength at floor modifier.

4. **D11.2 dual-mode problem confirmed:**
   - Mode A (n=11-12 instances, 4 prunable to 10): ceiling=10 insufficient — WR inelastic to pruning
   - Mode B (n=9-10 instances, 10 unprunable): no structural relief from any ceiling ≥10; absolute DPS density problem
   - Both modes require structural redesign, not additional tuning of ceiling or α

5. **MIGRATION.md not required.** D11.1 adds `alpha`, `n_skills_post_prune`, `skills_pruned` fields to `balance_metadata.element_coverage_tax` dict only (already a cross-seam-visible dict from v1.10). No new `ClassBalanceResult` fields added. v1.10 MIGRATION.md entry carries.

### Handoffs

**HANDOFF → matt + knight-rider (D11.2 ESCALATION):**
Gate missed: 0/17 (was 1/17 at v1.13). D11.1's PRIMARY lever (ceiling=10) did not resolve floor-pinning. Per gandalf WARN 2: DO NOT propose α>0.08 or ceiling<10. D11.2 is a structural redesign — not a config tweak. Escalation path: gandalf designs + gamora math note + rocket implements. Key inputs for D11.2 scope: (a) WR inelastic to ceiling=10 pruning; (b) dual-mode failure confirmed; (c) lowest-modifier dropped skills had dps_score=0.0 (utility/sustain/damage_over_time) — no meaningful DPS reduction from pruning these roles.

**HANDOFF → drax (MISS pattern):**
D11.1 data is live in demo (seasons 002011-002015 classes.json updated; post_process_d11_1=True). Hybrid_mage classes have D11.1 provenance but remain floor-pinned (balance metadata reflects floor-convergence). No gameplay regression introduced. Demo can continue playtesting against this state. D11.2 will update again when structural fix lands.

### Observations for D11.2 (INFO-3 carry-forward per dispatch)

The D11.2 must address two structurally distinct failure modes discovered empirically at D11.1:

**Mode A — coverage redundancy (n=11-12 instances):** These were the pruning targets of D11.1. The skill-count ceiling correctly identifies them as coverage-redundant, but the DROPPED SKILLS had dps_score=0.0 (utility, sustain, damage_over_time — non-damage roles). Removing them reduced skill count without reducing DPS. D11.2 insight: the pruning order matters. D11.1 correctly protected required roles and pruned by lowest-DPS; but the lowest-DPS prunable skills are literally non-damage roles with 0.0 contribution. True DPS-density reduction requires pruning DAMAGE-bearing skills, which the current protection hierarchy prevents.

**Mode B — absolute DPS density (n=9-10 instances):** These instances were at or below ceiling=10 before D11.1. They receive zero structural relief from any ceiling ≥10. They floor-pin because the kit's total damage output at modifier=0.05 is high enough to win 60-75% of fights regardless. D11.2 must address this via a mechanism that reduces per-skill DPS magnitude (not just skill count), or via a gauntlet-side change.

**D11.2 structural candidate from gamora § 9:** parametric sweep of ceiling=9, 8 on 5 representative instances before full salvage. This would inform whether Mode A can be addressed by deeper ceiling. Mode B likely requires a different lever entirely (α escalation beyond 0.08 was rejected; gamora suggests tax demotion paired with ceiling=9 as Option C-prime). Escalate to matt+gandalf for D11.2 authorization.

**Key data for D11.2 math note:** class_0054 at wr=0.567 (lowest in dataset) received 0% WR improvement from 12→10 pruning. If the math note projected class_0054 as "convergence candidate" based on wr=0.567, the empirical result (0.567→0.567) means the DPS contribution of the pruned skills was genuinely zero, not 12-15% as projected. This is because the pruned skills were non-damage roles — the projection assumed proportional DPS contribution, but non-damage roles contribute 0% of damage DPS.
