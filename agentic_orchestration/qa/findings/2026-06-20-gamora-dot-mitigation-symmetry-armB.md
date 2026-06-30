# Finding — 2026-06-20 — gamora DoT/mitigation-symmetry F1/F2/F4 + Arm B run

**Reviewer:** jack-ryan
**Severity:** PASS-WITH-INFO
**Target:** engine `e537b29` (HEAD, unpushed, ahead 5) + collab `7099e49` (HEAD, unpushed)
**Developer:** gamora
**Principles applied:** P1 (math-before-code), P2 (smoke-gate), P3 (cross-seam impact), P4 (decisions-log/bands as truth), P5 (severity); Disciplines #1, #2.1, #3, #11, #12, #24

## Verdict: PASS-WITH-INFO

F1/F2/F4 are faithfully implemented recompose-first; the Arm B run is JSON-verified across every gate the dispatch named; the math note's conclusions match the data and do NOT overreach. No BLOCK. Three INFO items recorded for the downstream band-refit step. One of them (INFO-1) is the load-bearing one the dispatch's checklist item 2 asked me to surface explicitly.

## What I found (descriptive)

**Mechanism correctness (checklist 1) — CLEAN.**
- F2 (`damage_resolver.py`): `_SCALING_ATTR_NORMALIZE` promoted module-level; `_try_apply_ailment` now threads `skill=` and computes `eff_attr` from `skill.scaling_attribute` via the same normalize table the direct path uses (`:314`). Fallback to the old int-or-wis read is gated on `if not eff_attr` — so a caster (scaling_attribute already INT/WIS) reads the identical value and **cannot regress**. gandalf's design-correctness condition (route via the SKILL's scaling attr, not the kit's max attribute) is honored — it reads `getattr(skill, "scaling_attribute")`, not a kit-level max.
- F1 (`spatial_engine.py`): reuses `effect_resolver.tick_effects` (NOT re-derived — `effect_resolver.py` is unmodified in the commit, confirmed), re-syncs scratch HP to live HP before ticking, subtracts only the returned float from authoritative `e.hp`, with a kill-check identical to the direct-hit path. Faithful float-bridge.
- F4 (`t4_sim_cycling.py`): `elemental_resistances={e: mob_armor/(mob_armor+ARMOR_MITIGATION_K)}` over the 7-substrate `ROTATING_ELEMENTS`, gated by `mitigation_symmetric` (default True). The symmetry proof holds — max tier r=92.7% < the 0.95 clamp (`math_model.py:127`), so elemental eats exactly what physical eats at every tier.
- RECOMPOSE-FIRST verified literally: `ARMOR_MITIGATION_K=3000.0` unchanged (`math_model.py:34`; math_model NOT in commit), `0.003` tick coefficient unchanged (`damage_resolver.py:1017`), `mob_armor` values untouched. No magnitude or armor re-tune this pass.

**Production SHIP-GATE regression (checklist 2) — NO regression to the GATE LOGIC; one declared-but-load-bearing consequence (INFO-1 below).** Band constant (`gauntlet_sim.py` `ENCOUNTER_COHORT_KPM_BAND`), floor, gauntlet_pass, tier_1 routing all untouched — `gauntlet_sim.py` is NOT in the commit. `metadata.production_gate_modified=False` is literally true.

**Semantic-shift declarations (checklist 3) — PRESENT, both.** DoT-live (F1) and resist-live (F4) declared on combat-output fields, in the commit message, the math note §10, and `metadata.semantic_shift_declarations`. Adequate per Discipline #12.

**Band-refit dependency (checklist 4) — RECORDED, not dropped.** `metadata.band_refit_required_downstream=True`; math note §10; commit message. Gate-trust explicitly suspended pending refit.

**Seed-stride fix (checklist 5) — VERIFIED.** Adopted production `*10_000`/`*1_000`/`+enc_idx` layout; `DOT_MIT_SEED_BASE=820000` (`metadata.seed_base=820000`), disjoint from `[700000,766703]` and `[619000,684303]`. Discipline #3 honored.

**V-gates (checklist 6) — JSON-CONFIRMED, not txt-only.** `v1_integrity_all_pass=True` (harness assertion `:315-325` fails loud on `n_fights != expected_n`); `v4_integrity_all_pass=True`; Fold-A `paired_seed=true`, int pooled −2.894 / wis −4.7466, both `drops=true`. Arm-isolation: A→B toggles only F4 (F1/F2 inert, 0/66 DoT source).

**The two gamora-flagged items — both check out.**
- §5.1 authoritative-comparison: correctly designated. The INTERNAL paired-seed Fold-A (`fold_a_caster_drop_check`) is the load-bearing read; the external `arm_b_to_arm_a_deltas` table is labeled corroborative-only with the WIS +24% smoke-noise example cited. No load-bearing claim rests on the cross-namespace external table.
- §4.4 DEX-also-drops: reasoning is sound. DEX A→B (external table: open_arena −7.24%, and the note's elite −72.8%/boss −93.1% from the cohort-composition read) follows from DEX routing ~83% elemental — F4 mitigates by skill ELEMENT (`damage_resolver.py:478`, the real lookup line), not attribute label. STR external A→B confirmed near-zero in the JSON (open_arena −0.34%, boss 0.0%, mini_boss 0.0%). Expected, not a harness fault.

**Headline conclusion vs data — MATCHES, no overreach.** The math note revises the original hypothesis correctly: STR does NOT move A→B (JSON: −0.3% to 0.0%), so the "armor-confound under-credits STR" hypothesis is NOT supported; the confound was caster OVER-credit (Q2: 76–94% free elite/boss KPM). gandalf's pre-registered FALSIFIER (rail 3: STR physical cells ~static A→B) is SATISFIED, not tripped — STR's near-zero move is the predicted result, not a quarantine trigger. STR residual gap stays real-allocation, awaiting deferred Arm C.

## INFO items (downstream band-refit owns these; none block the push)

**INFO-1 (the load-bearing one — checklist item 2 answer).** `gauntlet_sim.py:1032` calls `w4g2_tier_2_full_sim(...)` WITHOUT passing `mitigation_symmetric`, so the production gauntlet now inherits the new default `True`. **F4 symmetric mitigation is therefore LIVE in the production SHIP-GATE evaluation path, not merely in the measurement harness.** The production gauntlet now computes tier_2 KPM under symmetric mitigation and scores it against the UNTOUCHED (now-stale) bands. This is INTENDED (dispatch §10: "production DEFAULT once committed must be F1+F2+F4 ALL ON") and DECLARED (band-refit dependency, gate-trust suspended). It is correctly classified as a declared intermediate state — NOT a defect. Recording it explicitly so the band-refit step knows the gate is already running symmetric-mitigation KPMs against pre-symmetry bands, and so no one reads a production gauntlet_pass result as trustworthy until refit. Discipline #12 boundary is the right frame; this is the operational consequence of it.

**INFO-2 (anchor-citation drift, Discipline #11).** Math note §4.1/§4.3 and the F4 diff comment cite the DEFENDER elemental-resist lookup at `damage_resolver.py:470`; the actual line is `:478` (`res = defender.elemental_resistances.get(element, 0.0)`). The `:312` direct-path citation also reads `:314` on current disk. Cosmetic — the mechanism cited is correct and the lines are within the same function; flag for correction at the Arm C re-fire math note so future anchor-walks land clean.

**INFO-3 (Arm C deferral provenance — for the record).** Arm C is structurally null for this population (0/66 DoT source; STR's designed bleed absent from generation = rocket-seam bug, Matt-confirmed). gandalf pre-reg `df1023b` binds to the deferred re-fire. The F1/F2 fixes ship inert-but-correct now; their first live measurement waits on the rocket generation fix. No action this pass — noted so the deferred Arm C is not silently forgotten.

## Rationale

PASS-WITH-INFO, not BLOCK: every acceptance criterion in the dispatch §8 is met and JSON-verified; recompose-first is honored literally (constants unchanged, reused modules unmodified); both semantic-shift boundaries and the band-refit dependency are declared per Discipline #12; the math note's conclusions track the data without overclaiming (the headline revision is correctly reasoned and matches gandalf's pre-registered rails). INFO-1 is a real production-path consequence but it is intended-and-declared, which is precisely the "declared intermediate state" the dispatch authorized — so it is recorded, not blocked. No principle is violated.

## Action

- [ ] Developer (gamora): no required rework. At the Arm C re-fire math note, correct the `:470`→`:478` and `:312`→`:314` anchor citations (INFO-2).
- [ ] Downstream band-refit (gamora sim + jack-ryan Gate-2): treat the production gauntlet as running symmetric-mitigation KPMs against stale bands (INFO-1) — gate-trust SUSPENDED until refit; do NOT read a production gauntlet_pass as trustworthy in the interim.
- [ ] Matt: push authorization for `e537b29` + `7099e49` is yours — the commits are trustworthy to push and to build on per this Gate-2. Separately, the Q3 result (boss survive+kill = 0.000 for ALL FOUR attributes under symmetric ~90–93% mitigation) is the data input to your boss armor-nerf decision; that is a downstream, data-driven call, NOT this run.

## References
- Engine commit `e537b29`: `damage_resolver.py` (F2, `:1017` coeff, `:478` lookup), `spatial_gauntlet/spatial_engine.py` (F1), `t4_sim_cycling.py` (F4, `ROTATING_ELEMENTS`, `mitigation_symmetric` default True), `math/dot-ailment-mitigation-symmetry-run-2026-06-20.md`, `dot_mitigation_symmetry_armb_harness_2026_06_20.py` (V1 assert `:315-325`)
- Unmodified (recompose-first verification): `foundation/math_model.py` (`ARMOR_MITIGATION_K=3000.0` `:34`, 0.95 clamp `:127`), `effect_resolver.py`, `spatial_resolver_adapter.py`, `gauntlet_sim.py` (bands/floor/gate)
- Production inheritance locus: `gauntlet_sim.py:1032`
- Artifact: `agentic_orchestration/cycle-14-wave-5-season-001/dot-mitigation-symmetry-armB-2026-06-20.{json,txt}`
- Dispatch: `agentic_orchestration/dispatches/2026-06-20-gamora-dot-ailment-mitigation-symmetry-run.md`
- Pre-registration: `agentic_orchestration/gandalf/notes/2026-06-20-dot-mitigation-symmetry-3arm-pre-registered-interpretation.md` (`df1023b`)
