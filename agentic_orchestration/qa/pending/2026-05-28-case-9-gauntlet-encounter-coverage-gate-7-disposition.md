# Gate-7 Disposition — Case 9 Gauntlet Encounter Coverage
## Architectural Decision — 2026-05-28

**Reviewer:** jack-ryan
**Severity:** BLOCK (architectural — Matt Pattern-B required per Discipline #47)
**Type:** Architectural disposition (Gate-7 — post W-α3 Phase 2 / W-α4 compound_pass=False)
**Developer:** gamora
**Target:** post-W-α3 Phase 2 calibrated engine state; W-α4 harness run documented at MIGRATION.md § v1.43
**Principles applied:** Review Principles #1 (descriptive before prescriptive), #3 (schema validation at boundaries), #5 (escalation routing)
**Disciplines applied:** #11 (empirical inspection), #39 (Mode A/B scaffold-drift taxonomy), #44 (framing-refusal), #47 (balance changes affecting doc 50 § 4 5 targets require Matt design-call)

---

## 1. Gamora Forensic Diagnosis — PASS (with one clarification)

**Verdict: PASS.** The forensic diagnosis is accurate and structurally grounded. One scope clarification added.

### 1.1 Source verification

`GAUNTLET_ELIGIBLE_ENCOUNTER_TYPES_C14V1` is a `frozenset` defined at `gauntlet_sim.py` lines 131-135 with a module-load assertion at lines 180-182 that the set has exactly 2 members:

```python
GAUNTLET_ELIGIBLE_ENCOUNTER_TYPES_C14V1: frozenset[str] = frozenset({
    "boss_with_adds",  # 3 encounters: str_01, int_02, wis_02
    "mini_boss",       # 1 encounter:  wis_03
})
assert len(GAUNTLET_ELIGIBLE_ENCOUNTER_TYPES_C14V1) == 2, ...
```

The `tier_2_kpm` field (gauntlet_sim.py line 246) is only populated for encounters where the kit passes the T1 cohort-band check. The eligible-encounter logic at lines 319-352 explicitly filters to `GAUNTLET_ELIGIBLE_ENCOUNTER_TYPES_C14V1`, meaning T2 evaluation is structurally restricted to boss_with_adds + mini_boss.

**Bypassed encounter types confirmed:** open_arena, chokepoint_corridor, magic_pack, elite_pack — all 4 produce `tier_2_kpm=0.0` structurally (not from calibration state).

**Comment on gauntlet line 17 (bypass annotation):** the bypass list reads "BYPASSED (Cycle 14 v1): swarm + magic_pack + elite_pack" — this groups open_arena + chokepoint_corridor as "swarm." The BVV harness treats them as 2 distinct encounter types (BOUNDED_VIABILITY_ENCOUNTER_TYPES at bounded_viability_validation.py lines 76-83). The 4 bypassed encounter types at the harness layer are the 4 listed in gamora's forensic. Nomenclature consistent; no discrepancy.

### 1.2 Root cause confirmation: NOT a calibration artifact

Three alternative root causes are excluded:

**Scale_factor miscalibration:** excluded. W-α3 math note § 5.1 shows calibration converged at scale_factor=0.664063 (2.44% delta from reference target 75 KPM). T1 PASS at ratio=1.31× confirms the calibration objective was achieved. `tier_2_kpm=0.0` on 4 bypassed encounter types is independent of calibration state — it occurs because those encounter types are structurally outside the single Balanced band (71-79 KPM) regardless of scale factor.

**BVV harness bug residue:** excluded. Math note § 11.5 documents two bugs fixed (kit ID mismatch + S1_ prefix) during W-α3 Phase 2 work. These bugs are patched at bounded_viability_validation.py `_bvv_kit_legendary_id()` (lines 1167-1181). The W-α4 harness run producing T2/T4 FAIL was executed post-fix.

**Doc 50 § 4 target misalignment:** excluded. BVV harness target definitions match doc 50 § 4 verbatim per Amendment 1 + Amendment 2 (harness dispatch). Target 2 criterion (zero_count = 0 across 108 cells) and Target 4 criterion (per-kit specialization peaks) are correctly implemented. The 88-cell zero count is the correct measurement output given the current gauntlet architecture.

### 1.3 Clarification: Cycle 15 Option A nomenclature

Gamora's citation of "Cycle 15 Option A per-encounter-type bands" refers to the `ENCOUNTER_COHORT_KPM_BAND[enc_type][cohort]` infrastructure described in MIGRATION.md lines 558-628 and forward-linked from gauntlet_sim.py line 583. This is NOT the Gate-5 D2 Option 6 metric replacement (which was retroactively RETRACTED by Matt at Gate-6 per decisions-log "Cycle 15 D2 Option 6 RETRACTION" entry 2026-05-28). It is a new Cycle 15 commit that has never been scoped. It was first named as a planned future design at the SC7-F1 Gate-3 ratification (D2 RATIFIED: "Cycle 15 Phase 2 = Option A per-encounter-type KPM bands" at hive-mind state § SC7-F1 Gate-3). That D2 Cycle 15 naming survives the Gate-6 reversal — the reversal retracted D2 Option 6 metric replacement, not D2 per-encounter-type bands. The Cycle 15 per-encounter-type band architecture is a coherent scope item not yet defined.

---

## 2. Root Cause Chain (Description Only)

The BVV harness (W-α4, bounded_viability_validation.py) was specified at doc 50 § 4 to measure all 6 encounter types × 18 kits = 108 cells. At the time of doc 50 authoring and W-α4-gamora implementation, the harness was specified against a future architecture (Cycle 15 per-encounter-type bands) that does not exist yet.

The current gauntlet (gauntlet_sim.py) implements a Cycle 14 v1 stratified floor design: only boss_with_adds + mini_boss are eligible for T2 in-band evaluation. The other 4 encounter types produce `tier_2_kpm=0.0` by architectural design.

The W-α4 harness reads `tier_2_kpm` across all 6 encounter types. This produces 88 structural zero cells (18 kits × 4 bypassed types = 72 + 14 mini_boss misses at calibrated DPS = 86 structural zeros, with rounding producing the 88 observed).

T4 derives from T2: Target 4 requires `cohort_median_KPM > 0` to compute a ratio. With 4 bypassed encounter types producing cohort_median_KPM=0.0, ratios are undefined → no specialization peaks possible → 18/18 kits fail.

The arithmetic KPM gap for bypassed encounter types is structural and scale-invariant (W-α3 math note § 11.2): swarm encounters (800 HP) vs boss (77k HP) → KPM ratio ~100×. No single-band KPM architecture can cover both. Per-encounter-type bands are the architectural solution.

---

## 3. Options Analysis

### 3.1 Framing: what is actually being decided

The decision is: what constitutes "Path α close" for Cycle 14 v1?

Path α was ratified to achieve the bounded-viability-with-specialization directive (doc 50 § 4). The compound_pass criterion was set as: all 5 targets simultaneously PASS. T2/T4 as currently specified require per-encounter-type KPM bands that are a Cycle 15 scope item. The question is whether to defer that scope into Cycle 15, pull it forward, or find a Cycle 14 partial path.

### 3.2 Option A — Modify Path α close criterion to T1 + T3 + T5 PASS

**Mechanics:** Matt amends doc 50 § 4.6 compound_pass requirement to T1+T3+T5 as the Cycle 14 v1 close criterion. T2 and T4 are deferred to Cycle 15 per-encounter-type bands.

**What is achieved:** T1 (DPS variance ≤1.5× = 1.31× PASS) directly addresses the root-cause divergence (365× cross-path ratio at elite_pack). T3 is structural PASS (ceiling removed). T5 floor check is PASS (0 floor violations). The primary disease — STR/DEX producing 0.0 KPM on boss encounters — IS fixed by W-α1 + W-α3.

**What is deferred:** T2 (zero_count = 0 across 108 cells) and T4 (per-kit specialization peaks) cannot be measured until per-encounter-type bands exist. These represent the "every kit has somewhere to be excellent" and "no kit is locked out of any encounter type" properties. They are the specialization and bounded-viability properties — not just measurement formality.

**Scope impact:** 0d. Path α close possible within hours of Option A ratification.

**Close criterion tag accuracy:** the doc 50 § 0 tag is `v1-cycle-14-bounded-viability-substrate-led`. Under Option A, the tag name is architecturally inaccurate. The design directive explicitly requires bounded viability (T2: no zero encounter-type cells) and specialization (T4: designed peaks per kit) — both of which are deferred. Option A ships T1 (base DPS parity) as "bounded-viability-with-specialization." This is a material naming mismatch. Tag should be amended to reflect partial closure if Option A is taken. Suggested: `v1-cycle-14-cross-path-dps-parity-substrate-led` (accurately describes what is delivered without overclaiming the full directive).

**Discipline #39 classification:** Option A acknowledges Case 9 as Mode A hidden drift without resolving it within Cycle 14. The scaffold (`GAUNTLET_ELIGIBLE_ENCOUNTER_TYPES_C14V1` narrowing) is left open; T2/T4 carry forward as Cycle 15 items without the 3-element Mode B annotation (scaffold declaration + named resolution party + named resolution gate).

**Assessment:** T1 PASS is the root-cause-fix proof. The 365× problem is resolved. However, the bounded-viability-with-specialization directive's constitutive properties 1 and 2 (bounded viability floor + specialization peaks) remain unmeasured. Option A delivers the infrastructure required for the directive but not verification that the directive is satisfied.

### 3.3 Option B — Pull Cycle 15 Option A per-encounter-type bands into Cycle 14 v1

**Mechanics:** Implement `ENCOUNTER_COHORT_KPM_BAND[enc_type][cohort]` for all 6 encounter types in Cycle 14. Requires Discipline #1 math note (HP analysis per encounter type + band derivation), new calibration pass per encounter type at each cohort × damage_scaling_path, and expanding `GAUNTLET_ELIGIBLE_ENCOUNTER_TYPES_C14V1` to all 6 types.

**What is achieved:** compound_pass=True as originally specified. All 5 targets simultaneously PASS. Cycle 14 v1 tag accurately reflects `bounded-viability-with-specialization`. The design directive is verified, not just the root cause fixed.

**Scope impact:** ~2-4d. Math note authoring (~0.5d), calibration sweep across 6 encounter types × 4 cohorts (~1-2d), BVV harness re-run (~0.5d), Gate-2 (~0.25d). Within Matt 6-week re-evaluation budget (Path α elapsed ~2hr as cited in framing).

**Architecture:** structurally coherent. The HP-profile differences between encounter types (swarm ~800 HP vs boss ~77k HP) demand per-encounter-type bands — this is not a workaround, it is the correct architecture (confirmed by MIGRATION.md line 628: "when Cycle 15 Option A lands: retire GAUNTLET_ELIGIBLE_ENCOUNTER_TYPES_C14V1"). Option B resolves Case 9 in Cycle 14 rather than deferring it.

**Discipline #39 classification:** Option B = Mode B resolution within Cycle 14. Case 9 closed with the 3-element annotation pattern.

**Tag accuracy:** `v1-cycle-14-bounded-viability-substrate-led` accurately describes what is delivered.

**Assessment:** Option B is architecturally complete. It verifies the directive rather than assuming it. Primary tradeoff: ~2-4d scope expansion.

### 3.4 Option C — Expand GAUNTLET_ELIGIBLE_ENCOUNTER_TYPES_C14V1 to all 6 without per-type bands

**Mechanics:** Expand the eligibility constant to all 6 encounter types, using the single Balanced band (71-79 KPM) for all encounter types.

**Architectural coherence assessment:** NOT coherent. The KPM values for the 4 bypassed encounter types are 6-100× outside the single Balanced band at W-α3 calibrated DPS. Expanding eligibility without per-type bands means all 6 encounter types are evaluated against a 71-79 KPM band. All 18 kits will fail T2 on all 4 previously-bypassed types (swarm: 600 KPM >> 79; magic_pack: 600 KPM >> 79; elite_pack: ~472 KPM >> 79). `tier_2_kpm=0.0` is produced by the in-band check failing — the same structural zeros appear but with the eligibility constant expanded. T2/T4 still FAIL. Option C does not resolve the architectural gap; it just moves it.

**Assessment:** ELIMINATED. Option C produces identical compound_pass=False result while consuming implementation effort and widening the assertion violations.

### 3.5 Option D — Separate validation harness for all-encounter-type coverage

**Mechanics:** Keep gauntlet_sim.py unchanged (GAUNTLET_ELIGIBLE_ENCOUNTER_TYPES_C14V1 = 2 types). Add a separate "encounter coverage harness" that runs gauntlet sim in a reporting-only mode across all 6 encounter types, reading `tier_1_kpm` (raw signal) instead of `tier_2_kpm`, and computing a separate set of coverage metrics. Harness produces a "coverage report" artifact but does not contribute to compound_pass.

**What it provides:** visibility into per-kit signal across all 6 encounter types. Shows qualitative encounter-type coverage without requiring per-type band calibration. Could surface the T4-equivalent information (which kits are relatively stronger on which encounter types) even without pass/fail.

**What it does NOT provide:** T2/T4 PASS. compound_pass remains False. Matt still needs to make Option A or B decision for Path α close criterion.

**T4 analysis:** math note § 11.3 explicitly addresses this. Using `tier_1_kpm` for bypassed types, open_arena tier_1_kpm = 600.0 for ALL kits equally → per-kit/cohort-median ratio ≈ 1.0 for all → still no peaks in [1.5, 2.0] band. T4 would still fail even with full tier_1 signal from bypassed types.

**Assessment:** Option D is a visibility instrument, not a resolution. It could be a useful Cycle 14 close artifact (characterizing encounter-type coverage qualitatively) but it does not change the compound_pass decision. Option D could be combined with Option A as a "document what we're deferring" artifact, but it cannot replace Option A or B.

### 3.6 Option E — Partial Option B: per-type bands for elite_pack only

**Mechanics:** Pull only the elite_pack per-type band calibration into Cycle 14 (elite_pack KPM at W-α3 calibrated DPS is ~472, closest to boss/mini_boss tier). Swarm encounter types remain bypassed. 3 bypassed types remain (open_arena, chokepoint_corridor, magic_pack), 1 moved to eligible.

**Scope:** ~1-2d (narrower math note + calibration sweep × 1 encounter type).

**Assessment:** Does not resolve T2/T4 FAIL. With 3 bypassed types remaining, 18 kits × 3 encounter types = 54 additional zero cells. compound_pass still False. The partial improvement does not move the compound_pass needle unless ALL 6 types are in-band at their respective natural KPM scales. Option E saves ~1-2d scope vs Option B but produces the same compound_pass=False result. Not recommended as a standalone option; could be Phase 1 of a staged Option B if scope is a constraint.

---

## 4. Recommendation

**OPTION B — Pull Cycle 15 Option A per-encounter-type bands into Cycle 14 v1.**

**Rationale (one sentence per Discipline #47 routing requirement):**

The bounded-viability-with-specialization directive's constitutive properties 1 and 2 (bounded viability floor = T2; specialization peaks = T4) are the design intent of Path α, not measurement formality — shipping a "bounded-viability-with-specialization" tag without verifying bounded viability or specialization is architecturally dishonest and creates a false RATIFICATION record against doc 50.

**Supporting rationale:**

1. **T1 PASS is necessary but not sufficient.** T1 PASS (ratio=1.31×) confirms the root-cause fix (cross-path DPS parity). It does not confirm that the directive's other two properties (bounded viability + specialization) are satisfied post-refactor. The engine may satisfy them — or may not. Without T2/T4 measurement, this is unknown.

2. **The per-encounter-type band architecture is not novel scope — it was already ratified as D2 Cycle 15 at SC7-F1 Gate-3.** Pulling it forward accelerates the already-committed work by one cycle. Option B is a timeline pull-forward, not a scope extension.

3. **Q10 quality > timeline is still operative.** Matt ratified "extend timeline as needed for Wave 0.5 and all waves" at Cycle 14 entry. Path α is ~2hr elapsed. ~2-4d scope expansion is within the 6-week re-evaluation budget by a significant margin.

4. **Option A requires a tag name amendment regardless.** The doc 50 § 0 tag `v1-cycle-14-bounded-viability-substrate-led` cannot accurately describe Option A closure. Amending the tag name to reflect partial closure creates a decisions-log entry, a doc 50 amendment, and a separate canonical record of the deferral. The overhead of Option A's documentation burden approaches the overhead of Option B's scope.

5. **Discipline #39 Mode B resolution pattern.** Eight prior scaffold-drift cases resolved within the cycle via empirical sub-agent execution. Option B continues this pattern for Case 9. Option A breaks it by leaving a Mode A drift open with no Mode B annotation.

---

## 5. Path α Close Trajectory Per Option

### Option A (recommended against)
- Matt Pattern-B ratification: same session (this disposition)
- Doc 50 § 4.6 amendment + tag name amendment: ~0.5d (gandalf)
- Decisions-log entry for T2/T4 deferral: ~0.25d (jack-ryan)
- Bundle Gate-2 + Wave 5 RE-FIRE: ~3-5d (per existing trajectory)
- **v1 tag: ~3-5d from ratification**

### Option B (recommended)
- Matt Pattern-B ratification: same session (this disposition)
- Per-encounter-type bands math note (Discipline #1): ~0.5d (gamora)
- Calibration sweep × 6 encounter types × 4 cohorts: ~1-2d (gamora)
- BVV harness re-run (compound_pass=True expected): ~0.5d (gamora)
- Bundle Gate-2 + Wave 5 RE-FIRE: ~3-5d (per existing trajectory)
- **v1 tag: ~5-8d from ratification** (within 6-week budget)

---

## 6. Cycle 14 v1 Tag Semantics Per Option

### Under Option A
Tag `v1-cycle-14-bounded-viability-substrate-led` is **inaccurate** as written.

- "bounded-viability" in the tag name refers to the design directive from doc 50. The directive has 3 constitutive properties. Under Option A, only the base-DPS-parity property is verified (T1). The bounded-viability floor property (T2) and specialization property (T4) are explicitly deferred.
- **Recommended amended tag:** `v1-cycle-14-cross-path-dps-parity-substrate-led` — accurately names what is delivered.
- This is not a cosmetic concern. Tags appear in decisions-log entries, MIGRATION.md, and future Cycle 15 entry docs. An overstatement at the tag level propagates into downstream framing.
- Alternatively: retain the tag name and add explicit "T2/T4-deferred" annotation in the tag's decisions-log entry, clearly distinguishing which properties of the directive are and are not verified. This approach preserves tag-name continuity but requires explicit deferral record.

### Under Option B
Tag `v1-cycle-14-bounded-viability-substrate-led` is **accurate**.

- All 5 doc 50 § 4 targets PASS via compound_pass=True.
- The bounded-viability floor (T2), specialization (T4), DPS parity (T1), no ceiling saturation (T3), and floor violation (T5) are all verified.
- No tag amendment needed.

---

## 7. Discipline #47 Enforcement Check

**Routing confirmed: Gate-7 → Matt Pattern-B.**

Discipline #47 states: balance changes affecting any of doc 50 § 4 5 targets require explicit Matt design-call ratification.

Case 9 directly affects:
- **T2:** 88 structural zero cells in current harness run; resolution (Option B) changes the architecture that produces these zeros
- **T4:** 18/18 kits with no_peaks, derived from T2; same resolution path
- **T5:** conditionally — T5 is currently PASS (floor_violation_count=0); this is because `is_floor_violation` is only set when `cohort_median_kpm > 0` (bounded_viability_validation.py lines 844-849). The 88 zero cells fall under T2 (is_zero=True), not T5. T5's PASS is structurally correct under the current harness.

The Option A vs Option B decision modifies Path α close criterion (doc 50 § 4.6) or expands the gauntlet eligibility architecture — both require Matt design-call per:
- ADR-002 tiered approval: cross-seam architectural decisions require Matt escalation
- Discipline #47 (per hive-mind state § "CASE 9 SCAFFOLD-DRIFT" routing)
- Review Principle #5: BLOCK-tagged findings escalate to Matt
- Doc 50 § 4.6 is a locked canonical decision (canonical lock as of W-α4-gandalf `fe0b4a7`)

**This disposition is a BLOCK routing to Matt Pattern-B. Gamora cannot proceed to modify Path α close criterion or expand gauntlet eligibility architecture without Matt ratification.**

---

## 8. Summary Table

| Item | Finding |
|---|---|
| Gamora forensic diagnosis | **PASS** — 2 of 6 encounter types in GAUNTLET_ELIGIBLE_ENCOUNTER_TYPES_C14V1 confirmed; structural T2/T4 zeros confirmed; not calibration artifact |
| Alternative root causes eliminated | scale_factor miscalibration: EXCLUDED; harness bug residue: EXCLUDED; doc 50 misalignment: EXCLUDED |
| "Cycle 15 Option A" nomenclature | per-encounter-type KPM bands; Gate-3 D2 ratified item; DISTINCT from retracted Option 6 metric replacement |
| Option C architectural coherence | INCOHERENT — expands eligibility without bands; same compound_pass=False result |
| Option D utility | VISIBILITY instrument only; T4 still fails on tier_1_kpm due to ratio ≈ 1.0 uniformity across kits |
| Option E standalone utility | INSUFFICIENT — 3 bypassed types remain; compound_pass still False |
| Recommendation | **Option B** — per-encounter-type bands in Cycle 14 v1 |
| Recommendation rationale | Directive constitutive properties 1+2 must be verified, not assumed; ~2-4d within 6-week budget; Mode B resolution preserves Discipline #39 pattern |
| v1 tag under Option A | INACCURATE — amend to `v1-cycle-14-cross-path-dps-parity-substrate-led` or add explicit T2/T4-deferred annotation |
| v1 tag under Option B | ACCURATE — no amendment needed |
| Discipline #47 routing | CONFIRMED — Gate-7 → Matt Pattern-B; neither option executable without Matt ratification |
| Path α close trajectory under Option B | ~5-8d from Matt ratification |

---

## 9. Action Items

- [ ] **Matt:** Ratify Option A or Option B (or surface additional option). Primary question: is T1 PASS + T3/T5 structural PASS sufficient to close Path α within Cycle 14 v1, or does the bounded-viability-with-specialization directive require T2/T4 measurement before tagging?
- [ ] **Matt (if Option A):** Confirm amended tag name (`v1-cycle-14-cross-path-dps-parity-substrate-led` or deferral-annotation approach).
- [ ] **Matt (if Option A):** Authorize doc 50 § 4.6 amendment (gandalf seam write; ~0.5d).
- [ ] **Gamora (if Option B, post-ratification):** Author per-encounter-type KPM bands math note (Discipline #1 required before code changes); expand GAUNTLET_ELIGIBLE_ENCOUNTER_TYPES_C14V1 to 6 types; re-run BVV harness.
- [ ] **Jack-ryan (if Option B, post-gamora):** Gate-2 review of per-encounter-type bands implementation.

---

## 10. References

- `~/Games/reincarnated-engine/src/reincarnated/simulation/gauntlet_sim.py` lines 131-135, 180-182 — GAUNTLET_ELIGIBLE_ENCOUNTER_TYPES_C14V1 source + assertion
- `~/Games/reincarnated-engine/src/reincarnated/simulation/gauntlet_sim.py` lines 246, 319-352 — tier_2_kpm field + eligible-encounter counting logic
- `~/Games/reincarnated-engine/src/reincarnated/simulation/bounded_viability_validation.py` lines 76-83, 104-107 — BOUNDED_VIABILITY_ENCOUNTER_TYPES; 6-type assertion
- `~/Games/reincarnated-engine/src/reincarnated/simulation/bounded_viability_validation.py` lines 844-849 — floor violation logic (T5 vs T2 demarcation)
- `~/Games/reincarnated-engine/src/reincarnated/simulation/math/w-alpha-3-unified-calibration-pass-2026-05-28.md` § 5 (Phase 2 locked calibration; scale=0.664063; T1 ratio=1.31×) + § 11 (W-α4 harness result + gap analysis)
- `~/Games/reincarnated-engine/src/reincarnated/simulation/MIGRATION.md` § v1.43 (Phase 2 COMPLETE + T2/T4 FAIL documented + Matt decision required flag)
- `~/Games/reincarnated-collaboration/canonical/50-bounded-viability-with-specialization-design-directive-2026-05-28.md` § 4 (5 operationalized targets) + § 4.6 (compound criterion)
- `~/Games/reincarnated-collaboration/agentic_orchestration/cycle-14-hive-mind-state.md` § "W-α3 PHASE 2 COMPLETE 2026-05-28" + § "CASE 9 SCAFFOLD-DRIFT"
- `~/Games/reincarnated-engine/design/decisions/decisions-log.md` — Path α RATIFICATION entry + Cycle 15 D2 Option 6 RETRACTION entry (confirms Cycle 15 Option A per-encounter-type bands is NOT the same as retracted metric replacement)
