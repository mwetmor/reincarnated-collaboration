# Finding — 2026-07-08 — batched Gate-2: gamora Leg-i completion-build + rocket E1 geometry axis

**Reviewer:** jack-ryan (DEV-MODE, Gate-2, BLOCK authority)
**Severity:** INFO (both commits PASS)
**Target:** `a63aae2` (gamora completion-build) + `bfc94eb` (rocket E1 geometry axis)
**Developer:** gamora (simulation seam) + rocket (generation seam)
**Principles applied:** 1 (math-before-code), 2 (smoke-gate) + #2-FF, 3 (cross-seam / ADR-004), 4 (decisions-log truth), 6 (cross-seam round-trip)
**Disciplines cited:** #1, #2, #3, #10, #11, #12

Batched because both feed the same first content-bearing per-axis certification run under the Matt-ratified full-run pivot (decisions-log `a50db87`). No content-bearing pilot fires until this Gate-2 clears; gating both together per the pivot precondition.

---

## VERDICT

| Commit | Verdict |
|---|---|
| `a63aae2` gamora Leg-i completion-build | **PASS** |
| `bfc94eb` rocket E1 geometry axis | **PASS** |

Neither is a Principle-6 cross-seam contract change; both are within-seam. Both reproduced their claimed smoke evidence live in this session. No BLOCK, no ESCALATE. Two INFO notes recorded below for the record (neither blocking).

---

## COMMIT 1 — gamora `a63aae2` — PASS

### What I found
The two SESSION-59 halt gaps are genuinely closed. Gap 1 (gear threaded leaf-only): `measured_gear_stats` is now threaded end-to-end — `w5g1_gauntlet_execution` composes per-cohort `certification_gear(cohort, _build_cohort_combatant_stats(cohort))` inside the cohort loop and forwards it into both `w4g1_tier_1_sweep` (t4_sim_cycling.py:1373) and `w4g2_tier_2_full_sim` (:1454), each of which forwards to the leaf `_run_spatial_w4g_batch` (:1244, param at :1181), which forwards to `run_spatial_fight(measured_gear_stats=...)`. I traced the full chain first-hand; it is unbroken. Gap 2 (no cell-grain two-arm driver): `leg_i_cell_grain_two_arm_driver.py` exists, is population-agnostic (`_resolve_population` precedence: explicit dict > `regen:<seed>` spec > seed), runs one representative kit per cell, arm S then arm G SEQUENTIALLY at the SAME `cell_seed_base`, on the UNAMENDED four-family judge (`md._bar_disposition` + `DERIVED_BARS`), and machine-HALTs (exit 2) if arm G == arm S everywhere. I ran `--smoke` live: `arm_g_differs=True`, exit 0, plumbing took.

### Rationale
- **Principle 1 / Discipline #1:** satisfied. Math-before-code cited to `certification-gear-v0-composition-2026-07-08.md §6 step 2` (the build spec); this commit is the un-done half of an already-authored math note, not fresh un-mathed work.
- **Principle 2 / #2-FF:** satisfied. The verdict-rendering instrument is real: the instrument-validity check computes `max_abs_kpm_delta` across all (cell×family) and renders PLUMBING-TOOK vs HALT-LOUD with a nonzero machine exit code. This is exactly the instrument whose ABSENCE caused the SESSION-59 fraudulent zero-delta failure class (same class as the Matt-killed 1800-run). It now discriminates.
- **Discipline #3:** satisfied and verified in code. `run()` runs `_run_arm_on_cell(ARM_STRIPPED, ...)` then `_run_arm_on_cell(ARM_GEARED, ...)` at the same `cell_seed_base` (:276-277); per-family seed = `cell_seed_base + FAMILIES.index(fam)*100`, identical for both arms. No parallel same-seed regen.
- **Principle 3 / ADR-004:** no cross-seam surface touched. `arm` and `measured_gear_stats` both DEFAULT to legacy-preserving values (`arm="S"`, `gear=None`) — every existing caller is byte-identical. No star-lord export/telemetry schema, no output packet shape change. No MIGRATION.md required; correctly claimed NONE.
- **Discipline #12:** the semantic-shift note is correctly framed and NOT buried — arm G is now a live geared MEASUREMENT distinct from stripped arm S, but the certification-baseline MOVE (stripped → geared) is explicitly deferred to the succession clause / content re-fire, NOT moved here. F4-honesty preserved (gear carries no exit-window stat; arm G does not rescue an F4 exit fail).

### On the Disc #12 negative-delta-at-tiny-n finding — CORRECTLY CHARACTERIZED
gamora's framed observation (AGENT_STATE.md:25) states the F2/F4 negative KPM deltas under gear at n_fights=2/WR=0 are a KPM-instrument property at tiny n with partial-clears (gear shifts elapsed and kills-at-timeout in either direction), NOT a bug and NOT a content verdict, and that the smoke tests THREAD-VALIDITY (arm G ≠ arm S) not magnitude. **I independently reproduced this.** My live `--smoke` sliced different cells than gamora's reported run (mine: `melee_high_flat_dex`, `melee_high_flat_int`; `max_abs_kpm_delta=17.770` vs gamora's reported 12.941 — expected, different representative kits) and showed the same signature: multiple negative deltas (F1 -17.77, F2 -17.66/-2.272, F4 -8.72/-6.629) accompanied by `open_arena WR=0.000` floor warnings. This is the correct reading — at WR=0 with 2 fights, KPM is dominated by kills-at-timeout noise, and gear perturbing elapsed/kill-count in either direction is expected. It is a small-n instrument artifact, NOT a masked regression. The magnitude is explicitly reserved for the content-bearing per-axis run at full n_fights with re-fit bands. Characterization stands.

---

## COMMIT 2 — rocket `bfc94eb` — PASS

### What I found
The emitter's once-per-kit 3-shape collapse (`_BC_AMPLITUDE_TO_GEOMETRY`, applied once at the old :585, written into all 12 slots) is replaced by a per-skill kernel-driven `assign_skill_geometry(role, tier, damage_scaling_type)` called inside the emission loop (:684), with the result written per-slot (:742). The old kit-level assignment line is fully removed; only two `geometry_type` references remain and both are correct. I ran the round-trip smoke live: it reproduced the captured output byte-for-byte (distinct/kit 12/11/11/12, min 11 ≥ floor N=6; every emitted value resolves via `rich_type_translation`, zero `heuristic_fallback`; zero movement verbs; tracks-kernel PASS on all slots; B11 mechanics fire — chain_lightning 2.533×, multi_projectile 2.6×, fork 2.2×, ricochet_bounce 2.533×, leap_strike 1.3×, ring 1.2×), exit 0.

### Rationale
- **Principle 1 / Discipline #1:** satisfied. Math note `geometry-axis-e1-2026-07-08.md` lands in the SAME commit and is genuinely upstream of the code — it answers the design question (assignment basis = skill KERNEL (role, tier, delivery), justified in §1; subset proof in §2; floor N=6 derived from kernel decomposition in §4, not arbitrary; balance-spine preservation in §5). Both Gate-1 amendments are folded: §2 enumerates the closed excluded-movement-verb set; §4 justifies floor N and the distribution-shape (tracks-kernel) check.
- **Principle 2 / #2-FF:** satisfied and strong. The smoke proves the FULL round-trip (emitted geometry → `_RICH_TO_SPATIAL` → 6-type spatial class → B11 multiplier fires > 1.0), not merely that richer strings were written. The tracks-kernel check re-derives `g(kernel)` per slot and asserts equality with the emitted value — this defeats a bare distinct-count fig leaf. Pre-fire one-command baseline (`len(set(_BC_AMPLITUDE_TO_GEOMETRY.values())) == 3`) present and asserted.
- **Principle 3 / Principle 6 / ADR-004:** no cross-seam contract change. I independently verified emitted-set ⊆ the 24 `_RICH_TO_SPATIAL` keys (every value resolved via `rich_type_translation`, none via heuristic) AND emitted-set ∩ excluded-movement-verbs = ∅ (zero movement verbs across all four kits). No new sim key is emitted; the sim vocabulary (F1 RATIFIED LIVE 2026-06-17) and B11 mechanics already exist. Correctly claims NONE / no MIGRATION.md. This is a pure emitter widening within the accepted contract.
- **Discipline #10 (attribution / isolability):** E1 is isolable. The change writes exactly ONE field per skill (`geometry`); it writes no damage magnitude, no tier coefficient, no energy/cooldown/cast value. E2 (economy scalars) / E3 (hybrid) / E4 (timing) and C3 band re-fit are explicitly out of scope. The effective-throughput shift is the SIM applying B11 multipliers to the widened geometry — an axis EFFECT, not a co-mingled second change.
- **Discipline #12:** the semantic shift (effective per-skill throughput shifts because B11 mechanics now fire on the generated population instead of being dead code behind a 3-shape collapse) is named explicitly in §5, and the downstream consequence (C3 band re-fit gates-on E1) is correctly routed downstream, not silently absorbed.

---

## INFO notes (for the record — non-blocking)

- **INFO-1 (rocket, side-finding confirmed correct):** rocket's side-finding is accurate and material. Pre-E1, two of the three collapse values (`small_aoe`, `large_aoe`) were NEVER valid `_RICH_TO_SPATIAL` keys, so the old collapse silently degraded to F1 Path-3 geometry-blindness for ~2/3 of the amplitude space. This means the pre-E1 declared baseline was measuring a geometry-blind population more than the "3 shapes" framing implied — relevant to C3 band re-fit, which should be understood as re-fitting off a largely point/Path-3 baseline, not a clean 3-shape one. Recorded so the C3 owner reads the re-fit delta correctly. No action on rocket.
- **INFO-2 (gamora, forward-watch):** the driver's default representative cohort for arm G at cell grain is `Balanced` (single cohort) unless `--all-cohorts-arm-g` is passed. The dispatch's "four cohort tilts" deliverable is served by the `all_cohorts_arm_g` path, which the `--smoke` does NOT exercise. Confirm the content-bearing per-axis run invokes the four-cohort path (or `w5g1` arm="G", which composes per-cohort inside its own loop) so the per-cohort delta map the C3 re-fit wants is actually produced. Not a defect in this build — the capability is present and correct — a run-config watch-item for the content fire. Route to KR / gamora at fire-time.

---

## Action
- [x] jack-ryan: both commits Gate-2 PASS. Content-bearing per-axis certification run precondition (this batched Gate-2) is CLEARED.
- [ ] KR / gamora (run-config, non-blocking): at the content-bearing fire, ensure the four-cohort arm-G path is exercised so the per-cohort delta map is produced for C3 re-fit (INFO-2).
- [ ] C3 re-fit owner (awareness, non-blocking): read the re-fit delta as measured off a largely point/Path-3 pre-E1 baseline, per INFO-1.
- [ ] No Matt escalation required (no BLOCK, no locked-decision conflict, no cross-seam schema change).

## References
- `src/reincarnated/simulation/leg_i_cell_grain_two_arm_driver.py` (new; reviewed + ran `--smoke` live)
- `src/reincarnated/simulation/gauntlet_sim.py` (`w5g1_gauntlet_execution` + `arm` param + per-cohort gear compose)
- `src/reincarnated/simulation/t4_sim_cycling.py` (`w4g1`:1304/1373, `w4g2`:1402/1454, leaf `_run_spatial_w4g_batch`:1181/1244)
- `src/reincarnated/simulation/combatant.py` (`certification_gear`:491, `CERTIFICATION_GEAR_INSTRUMENT_ID`:488)
- `src/reincarnated/simulation/math/certification-gear-v0-composition-2026-07-08.md` (§6 step 2 build spec)
- `src/reincarnated/simulation/AGENT_STATE.md:24-25` (Disc #12 negative-delta framing)
- `src/reincarnated/generation/per_skill_emitter.py` (`assign_skill_geometry`; emitter widening; `_EXCLUDED_MOVEMENT_VERB_GEOMETRIES`)
- `src/reincarnated/generation/math/geometry-axis-e1-2026-07-08.md` (math note; both Gate-1 amendments folded)
- `scripts/rocket_geometry_axis_e1_smoke_2026_07_08.py` + `src/reincarnated/generation/math/geometry-axis-e1-smoke-output-2026-07-08.txt` (reproduced live)
- `agentic_orchestration/dispatches/2026-07-08-rocket-geometry-axis-E1.md` (Gate-1 PASS-WITH-AMENDMENTS)
- Authority: `agentic_orchestration/gandalf/notes/2026-07-08-full-run-pivot-four-rulings.md`; decisions-log `a50db87`
