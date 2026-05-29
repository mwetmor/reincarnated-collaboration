# Concern #3 Caller-Graph Audit + P3a Viability Check

**Date:** 2026-05-29
**Author:** gamora (engine simulation seam owner)
**Authority:** Matt 2026-05-29 in-session — Concern #3 resolution authorization § 3.1 (audit scope) + § 3.2 (pre-ratified KR routing matrix)
**Dispatch:** `agentic_orchestration/dispatches/2026-05-29-gamora-cycle-14-a2-1-resumption-2-step-1-concern-3-caller-graph-audit.md`
**Pattern:** Pattern A-deep audit-only (read-only; no code-touch)
**Engine HEAD:** `98e1825`

---

## 1. VERDICT

**Concern #3 caller-graph audit complete; routing recommendation per § 3.2 matrix: Case A (single consumer of `mean_encounters_passed_per_kit`) + Case D (P3a method viable); KR action: P3c (preferred) — architectural fix at source; fallback P3a if P3c blocks.**

---

## 2. Caller-Graph Table

All occurrences of `mean_encounters_passed_per_kit` in engine Python source (`grep -rn` across `src/`, including tests):

| # | File | Line | Role | Context |
|---|---|---|---|---|
| P | `simulation/gauntlet_sim.py:646` | Field declaration | `GauntletQualityReport.mean_encounters_passed_per_kit: float = 0.0` | Dataclass field; the data structure |
| P | `simulation/gauntlet_sim.py:690` | `to_dict()` serialization | `"mean_encounters_passed_per_kit": round(self.mean_encounters_passed_per_kit, 2)` | JSON output; telemetry only |
| P | `simulation/gauntlet_sim.py:1074` | **ASSIGNMENT (producer)** | `quality_report.mean_encounters_passed_per_kit = statistics.mean(all_enc_pass_counts)` | Iterates ALL 4 `COHORT_ARCHETYPES` regardless of cohorts run |
| C | `simulation/phase7_bridge.py:368` | **READ (consumer)** | `enc_passed = round(quality_report.mean_encounters_passed_per_kit)` | Only consumer reading this value for gate logic |
| I | `simulation/phase7_bridge.py:355` | Comment (informational) | Explains proxy intent (incorrect: states 1 kit × 1 cohort = exact value — this is the bug) | No code execution |
| I | `simulation/phase7_bridge.py:361` | Comment (informational) | Repeats incorrect framing | No code execution |
| I | `simulation/phase7_bridge.py:367` | Comment (informational) | Repeats incorrect framing | No code execution |
| I | `simulation/MIGRATION.md:2578` | Documentation | Example value `14.25` in migration record | Not executable |
| I | `simulation/MIGRATION.md:2833` | Documentation | Field name in schema-change record | Not executable |

**Legend:** P = producer-site; C = consumer-site; I = informational (comment, doc, JSON output)

**Consumer count: 1.** `phase7_bridge.py:368` is the sole live Python consumer. No test files consume this field.

---

## 3. Per-Caller Semantic-Equivalence Assessment

### The single consumer: `phase7_bridge.py:368` in `_run_gauntlet_for_kit()`

| Dimension | Finding |
|---|---|
| **Cohorts populated** | 1 of 4 — `cohorts=[gauntlet_archetype]` at `phase7_bridge.py:340` (by Phase 7 design: each kit evaluated against its single assigned cohort) |
| **Divisor-4 dependency** | NO — Phase 7 does NOT depend on divisor=4 semantics. The correct value it needs is the count of encounters passed for the ONE cohort it ran. The current divisor=4 is the bug: it dilutes the actual count by 4, making the maximum possible `mean_encounters_passed_per_kit` = 18/4 = 4.5 when running 1 cohort of 18 encounters. Phase 7's threshold check `pass_rate = enc_passed / 18` then yields max `4.5/18 = 0.25`, far below `P7_GAUNTLET_PASS_FLOOR = 0.70`. |
| **Divisor=actual-count equivalence** | YES — if `gauntlet_sim.py:1072` iterated only over cohorts actually run (1 cohort in Phase 7's case), `mean_encounters_passed_per_kit` would equal the raw encounter-pass count for that cohort, which is exactly what Phase 7 needs: `enc_passed / 18 = gauntlet_pass_rate`. |
| **Caller intent** | Phase 7 bridge wants `encounters_passed` for the specific cohort it ran, to compute `pass_rate = passes / total_encounters`. Comments at lines 355-367 state this intent but incorrectly assert the divisor=4 aggregation is equivalent for 1 kit × 1 cohort — this is the documented misunderstanding. |

### Other `run_gauntlet_sim` callers (do NOT consume `mean_encounters_passed_per_kit`)

Two additional callers of `run_gauntlet_sim` also pass partial cohort sets:

| Caller | File:Line | Cohorts passed | Reads `mean_encounters_passed_per_kit`? | Assessment |
|---|---|---|---|---|
| `_run_gauntlet_t4_context()` | `unified_calibration_loop.py:739` | Single cohort (`[cohort_normalized]` per kit, line 695) | **NO** — returns `gauntlet_sim_pass, quality_report`; caller at line 2753 discards quality_report (`_, _gauntlet_result`); extracts KPM from JSON output file | **Not a Concern #3 consumer; Disc #40 secondary observation** |
| `w5r2_gauntlet_sim_integration()` | `season_generation_pipeline.py:1193` | Single cohort (`[cohort_normalized]` per kit, lines 876 + 902 + 928) | **NO** — reads `quality_report.total_kits_validated`, `.kits_season_emit`, `.total_fights_run` only; derives per-kit pass from canonical JSON (line 1223+) | **Not a Concern #3 consumer; Disc #40 secondary observation** |

These callers are architecturally affected by the same cohort-divisor bug in `mean_encounters_passed_per_kit` computation — that field is silently wrong in their outputs too — but they do not read it, so they are not operationally impacted by Concern #3. They are Disc #40 secondary observations (see Section 7).

---

## 4. P3a Method-Signature Viability Check

**Candidate replacement at `phase7_bridge.py:368`:**
```python
# P3a candidate: replace
enc_passed = round(quality_report.mean_encounters_passed_per_kit)
# with:
enc_passed = kit_results[0].encounters_passed(gauntlet_archetype)
```

**Method existence check — `GauntletKitResult.encounters_passed(cohort: str) -> int`:**

Found at `gauntlet_sim.py:482-484`:
```python
def encounters_passed(self, cohort: str) -> int:
    """Count of encounters where in_band=True for a given cohort (all encounter types)."""
    return sum(1 for r in self.cohort_results.get(cohort, []) if r.in_band)
```

| Check | Result |
|---|---|
| Method exists on `GauntletKitResult`? | **YES** — `gauntlet_sim.py:482` |
| Accepts archetype/cohort string parameter? | **YES** — `cohort: str` positional parameter |
| Return type compatible (int or float)? | **YES** — returns `int` (count of passing encounters); `round()` wrapper at call site is harmless but unnecessary |
| Semantics correct for Phase 7's use? | **YES** — `cohort_results.get(cohort, [])` returns only results for the cohort that was actually run; `in_band=True` count = encounters the kit passed for that cohort |
| `kit_results` accessible at call site? | **YES** — at `phase7_bridge.py:351`, `kit_results = quality_report`; HOWEVER this is a semantic misassignment: `run_gauntlet_sim()` returns `(bool, GauntletQualityReport)`, so `quality_report` IS the `GauntletQualityReport`, not a list of `GauntletKitResult`. The `GauntletQualityReport` does not expose a `kit_results` list as a public field. |

**P3a VIABLE — but requires access path clarification.** The method `encounters_passed(cohort)` exists with the right signature and return type. However, P3a as specified (`kit_results[0].encounters_passed(gauntlet_archetype)`) requires accessing the `GauntletKitResult` list, which is not directly exposed on `GauntletQualityReport`. The P3a fix would need one of:
- (a) Add `kit_results` as a field on `GauntletQualityReport` (populated by `gauntlet_sim.py:w5g2` before returning) — minimal change, correct
- (b) Access via the local `kit_results` list built inside `w5g2_gauntlet_quality_report()` and pass it through — requires signature change
- (c) P3c at source avoids this indirection entirely

P3a viability verdict: **viable** (Case D), but the simplest P3a implementation is slightly more involved than a one-line change — it requires exposing `kit_results` on `GauntletQualityReport` OR restructuring the return path. P3c (fix at source in the `mean_encounters_passed_per_kit` assignment) is cleaner.

---

## 5. Disposition Mapping to § 3.2 Matrix

| Dimension | Finding | Matrix column |
|---|---|---|
| Caller graph | **Single consumer** (`phase7_bridge.py:368` only) | "Single (only Phase 7)" |
| P3a method viability | **Viable** (method exists; access path requires one additional field exposure) | "viable" |

**Matrix row match:** Single caller (only Phase 7) + P3a viable → **KR action: P3c (preferred); fallback P3a if P3c blocks.**

**Case classification:** Case A (single consumer) + Case D (P3a viable). NOT Case C + Case E combined. No surface-to-Matt required.

**Rationale for P3c preference:**
1. No other consumer depends on divisor=4 semantics — changing to `len(p7_cohorts_actually_run)` at source is semantically transparent for all callers
2. `unified_calibration_loop.py` and `season_generation_pipeline.py` also pass partial cohorts; while they don't read `mean_encounters_passed_per_kit` today, the field is computed incorrectly for them too — P3c corrects the field universally
3. P3a requires exposing an additional field on `GauntletQualityReport` to access `kit_results[0]` — adds API surface. P3c is a smaller, cleaner change at the assignment line
4. Leaves no footgun for future callers

---

## 6. Disc #42a Q1-Q6 Self-Audit

| Q | Question | Verdict |
|---|---|---|
| Q1 | Load-bearing framing assumption: "caller-graph audit + method-signature viability check is sufficient to determine routing between P3a and P3c" | CONFIRMED — the audit IS the determination. No additional information needed. Single consumer empirically confirmed. |
| Q2 | Refutation evidence in scope? | YES — the grep output + per-file quality_report field access analysis directly refutes or confirms "P3c is universally safe" assumption. Confirmed safe: no other consumer of the field. |
| Q3 | Refutable cheaply? | YES — completed within ~20min wall-clock; read-only; no code-touch |
| Q4 | Measurement context match? | YES — the audit measured what callers actually require (field access pattern + divisor dependency), not a proxy |
| Q5 | Calibration scope match? | YES — scope was callers of `mean_encounters_passed_per_kit` in engine `src/`; impact scope of P3c fix is exactly the producer at `gauntlet_sim.py:1074`. Match is exact. Secondary observation: two other partial-cohort callers of `run_gauntlet_sim` are not impacted operationally but benefit from P3c correction |
| Q6 | Semantic stability of "caller graph" + "P3a viability"? | YES — "caller graph" = all Python sites reading `GauntletQualityReport.mean_encounters_passed_per_kit` (enumerated: 1 site); "P3a viability" = does `GauntletKitResult.encounters_passed(cohort)` exist + right signature (confirmed: line 482) |

All 6 Q verdicts: PASS. No framing refutation triggered.

---

## 7. Secondary Observations (Disc #40 + Disc #11 — INFO class; not fixed in this dispatch)

### Disc #40 — Scaffold-pattern observations

**Secondary Obs 1 (Disc #40):** `unified_calibration_loop.py` at `_run_gauntlet_t4_context()` (line 739) passes single-cohort configs to `run_gauntlet_sim()` and the returned `_gauntlet_result` is discarded (`_` at line 2753). The `mean_encounters_passed_per_kit` field in that quality_report is computed incorrectly (cohort-divisor bug) but never read. This is a latent correctness gap: if a future caller of `_run_gauntlet_t4_context()` reads `mean_encounters_passed_per_kit`, it would silently receive a 4x-diluted value. P3c fixes this universally. INFO-class; do not fix in this audit dispatch.

**Secondary Obs 2 (Disc #40):** `season_generation_pipeline.py:w5r2_gauntlet_sim_integration()` passes single-cohort configs (each kit's `primary_cohort` only, lines 876/902/928) and similarly does not read `mean_encounters_passed_per_kit`. Same latent gap. P3c fixes. INFO-class.

**Secondary Obs 3 (Disc #40):** The comment block at `phase7_bridge.py:355-367` (lines 355, 361, 367) actively misframes the bug as a known-correct behavior. The comments state "for 1 kit, 1 cohort = exact value" — this is factually wrong (the divisor is 4 regardless of cohorts run). These comments will require correction as part of the downstream P3a or P3c fix dispatch. INFO-class; not touched in audit.

### Disc #11 — Hygiene observations

**Hygiene Obs 1 (Disc #11):** `gauntlet_sim.py:1068` comment reads: "Mean encounters passed per kit (across all cohorts, per kit)". After P3c, this comment will need updating to reflect "across cohorts actually run" semantics. The docstring currently implies all-cohort iteration is correct/intended, which it was for the full-cohort caller (season_generation_pipeline) but is wrong when partial cohorts are passed. INFO-class.

**Hygiene Obs 2 (Disc #11):** `GauntletQualityReport` does not expose the `kit_results` list (list of `GauntletKitResult`) as a public field. The comment at `phase7_bridge.py:351` sets `kit_results = quality_report` (the report object, not a list of kit results), which is a confusing local alias. If P3a were chosen, this naming confusion would need resolution. P3c avoids this. INFO-class.

---

## 8. Cross-References

| Artifact | Role |
|---|---|
| `agentic_orchestration/dispatches/2026-05-29-gamora-cycle-14-a2-1-resumption-2-step-1-concern-3-caller-graph-audit.md` | This dispatch (audit scope + brief format) |
| `agentic_orchestration/gandalf/notes/2026-05-29-concern-3-resolution-authorization-and-pre-ratification.md` | Authoritative Concern #3 resolution authorization + § 3.2 routing matrix |
| `agentic_orchestration/gandalf/notes/2026-05-29-phase-a2-cascade-resumption-2-fire-prompt.md` | KR cascade-drive through Cycle 14 end |
| Collab commit `1a8f12c` | KR Matt-surface — Concern #3 technical specification + P3a/P3b/P3c candidates |
| `simulation/gauntlet_sim.py:482-484` | `GauntletKitResult.encounters_passed(cohort)` — P3a method (viable) |
| `simulation/gauntlet_sim.py:646` + `:1068-1076` | `GauntletQualityReport.mean_encounters_passed_per_kit` producer — P3c fix site |
| `simulation/phase7_bridge.py:340` + `:368` | Concern #3 consumer site — partial-cohort call + incorrect extraction |
| `canonical/story/phase-7-2-layer-joint-gate-spec-2026-05-27.md` | Phase 7 gate semantics LOCKED (P3a/P3c preserve; P3b REJECTED) |
| `simulation/unified_calibration_loop.py:695` + `:3657` | Secondary Disc #40 obs — partial-cohort callers that do NOT read the field |
| `generation/season_generation_pipeline.py:876` + `:902` + `:928` | Secondary Disc #40 obs — partial-cohort callers that do NOT read the field |

---

## 9. Sign-Off

**Audit complete.** No surface-to-KR conditions triggered (not Case C + Case E combined; no unexpected patterns; all 6 Disc #42a Q verdicts PASS; no Disc #48 R48.5 RAM pressure).

**KR routing recommendation:** Case A + Case D → P3c preferred (upstream fix at `gauntlet_sim.py:1068-1076`; divide by `len(cohorts_actually_run)` not `len(COHORT_ARCHETYPES)`); fallback P3a if P3c blocks.

**gamora** | 2026-05-29
