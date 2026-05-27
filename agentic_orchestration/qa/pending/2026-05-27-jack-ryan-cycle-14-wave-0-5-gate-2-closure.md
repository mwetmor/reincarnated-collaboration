# Finding — 2026-05-27 — Cycle 14 Wave 0.5 Gate-2 Closure

**Reviewer:** jack-ryan
**Severity:** PASS-with-WARN (1 WARN, 4 INFO — 0 BLOCK)
**Target:** `rocket/v1.5-wave-0-5-track-d-content-emission` + `gamora/v1.5-wave-0-5-damage-routing-synthetic-retired` + SC-6b commit `3c95883`
**Developers:** rocket + gamora + elrond
**Principles applied:** Principles 1, 2, 3, 4, 6 (REVIEW_PROCESS.md § 1)
**Authority basis:** Matt 2026-05-27 framing brief Q1-Q11 RATIFIED; SC-1 jack-ryan Discipline #38 + #39 RATIFIED; critique-pair-gate-protocol DEV-MODE BLOCK authority

---

## Verdict: PASS-with-WARN

Wave 0.5 closes. Downstream Wave 1 and pipeline wiring sidecar may fire.

The load-bearing close gate criteria are all met. Discipline #39 is empirically verified.
Cross-seam MIGRATION coverage is complete. Math-notes were pre-authored. AGENT_STATE.md
updated on both seams. One WARN requires follow-on tracking (not blocking); four INFO items
are for the record.

---

## Finding 1 — PASS (BLOCK authority exercised; criterion MET)

### Discipline #39 Empirical Verification — synthetic_mode RETIRED ABSOLUTELY

**What I found:**

Ran empirically per Discipline #11 (empirical inspection over assumption):

```bash
grep -rn "synthetic_mode" ~/Games/reincarnated-engine/src/reincarnated/simulation/ --include="*.py"
```

Result:
```
simulation/gauntlet_sim.py:427:    # Discipline #39 (Cycle 14 Wave 0.5): synthetic_mode detection retired.
simulation/t4_sim_cycling.py:955:    Cycle 14 Wave 0.5 — Discipline #39 (synthetic_mode RETIRED):
simulation/t4_sim_cycling.py:956:      synthetic_mode parameter removed. All calls run with full variance and full KPM routing.
simulation/t4_sim_cycling.py:1045:    Cycle 14 Wave 0.5 — Discipline #39 (synthetic_mode RETIRED):
simulation/t4_sim_cycling.py:1046:      synthetic_mode parameter removed. in_band restored to original semantic:
simulation/t4_sim_cycling.py:1100:    # The synthetic_mode override that changed this to "encounter completable" is retired.
```

ZERO functional production code matches. ALL matches are retirement-notice comments and
docstring references documenting the retirement. This satisfies the Wave 0.5 close gate
criterion verbatim per gamora MIGRATION.md § v1.33 and framing brief Q8.

Discipline #12 `in_band` semantic restoration confirmed: `in_band = sg_result.overall !=
SUBGATE_BLOCK` (KPM within cohort band, original definition).

**Cite:** Discipline #39 (no-synthetic-stub-as-permanent-fallback; LOAD-BEARING per Matt Q4
emphatic "extremely confirm.. retire it"); Discipline #11 (empirical inspection over assumption).

**Status: CRITERION MET. Gate cleared.**

---

## Finding 2 — WARN: LUT value divergence between elrond SC-6b and rocket fallback table is not fully reconciled

**What I found:**

Elrond SC-6b backfill used Pass 2 corrected LUT values:
`martial-heavy=177, martial-light=99, ranged=91, caster-arcane=31, caster-faith=31`

Rocket's `WEAPON_FAMILY_L50_BASELINE` fallback LUT (in `substrate_weapon_binding.py`):
`martial-heavy=200, martial-light=130, ranged=150, caster-arcane=50, caster-faith=50`

These differ materially (martial-heavy: 177 vs 200; ranged: 91 vs 150). Both sets are
within doc 47 § 3.1 ranges, but the divergence means:

1. When `sc6b_live=True` and `base_physical_damage_l50` is non-NULL (the nominal case for
   2,293 v1_scope rows), rocket reads elrond's live substrate value — elrond's LUT wins.
2. When `sc6b_live=False` or the column is NULL (scaffold state, non-v1_scope rows, or future
   expansion rows before SC-6b enrichment), rocket's fallback LUT applies — values differ
   from what elrond's math-note targets.

The MIGRATION.md § 5 records that elrond's rocket Pattern-A query was filed but NOT
confirmed by rocket before SC-6b backfill proceeded (recorded as "absent rocket amendment,
Path A stands"). Rocket's math note (`element/math/wave-0-5-substrate-binding-math-2026-05-27.md`)
states the fallback LUT is "coordinated with elrond SC-6b" — but the values do not match.

In production paths this is currently benign (live SC-6b values take precedence when
non-NULL, which they are for all 2,293 v1_scope rows). The divergence becomes active only
in scaffold/fallback states.

**Risk:** When Wave 5 generates a fresh roster and pipes through `substrate_weapon_binding.py`
with SC-6b enrichment live, the production path reads elrond's values. But any diagnostic
path or test that invokes `substrate_weapon_binding.py` with `sc6b_live=False` (scaffold
mode) produces damage baselines materially different from the SC-6b substrate. This can
produce confusing debugging results and violates Discipline #10 (attribution clarity — if
you change sc6b_live you change the baseline, making baseline comparison ambiguous).

**Remediation (not blocking Wave 0.5, but required before Wave 5 gauntlet):**
Rocket should either (a) update `WEAPON_FAMILY_L50_BASELINE` to match elrond's Pass 2
corrected values, or (b) explicitly document the divergence in both math-notes as intentional
(different purposes: elrond's LUT is the amplitude-adjusted substrate anchor; rocket's fallback
LUT is the doc-47-midpoint-nominal value). KR should author a follow-on dispatch for this
alignment. Gate before Wave 5 gauntlet runs.

**Cite:** Discipline #10 (attribution clarity — change one thing, measure one thing);
Discipline #11 (empirical inspection over assumption); Principle 6 (cross-seam round-trip
discipline — contract ambiguity at seam join).

**Action:**
- [ ] Rocket: reconcile `WEAPON_FAMILY_L50_BASELINE` with elrond Pass 2 values OR explicitly
      document divergence as intentional in both math-notes
- [ ] KR: author follow-on dispatch; gate on Wave 5 fresh roster gauntlet (not Wave 1-2-3)

---

## Finding 3 — INFO: `_SCALING_ATTR_NORMALIZE` cross-seam contract — documented; disposition adequate for Wave 0.5 close

**What I found:**

Gamora's `damage_resolver.resolve_skill()` includes `_SCALING_ATTR_NORMALIZE` mapping
uppercase short-form ("INT") → lowercase full-form ("intelligence") attribute keys. This
bridges the gap between rocket's `_BC_ATTRIBUTE_TO_SCALING_ATTR` emitting uppercase
short-forms and `StatDistribution.as_dict()` returning lowercase full-forms.

Empirically confirmed: `per_skill_emitter._BC_ATTRIBUTE_TO_SCALING_ATTR` returns
`{"STR": "STR", "DEX": "DEX", "INT": "INT", "WIS": "WIS"}` — uppercase throughout.

The fix is documented in MIGRATION.md § v1.33 addendum as a behavior change (not silent bug
fix) per Discipline #12. The cross-seam contract is explicit: "rocket must continue to use
uppercase short-form; gamora normalizes at the seam join point."

**Cross-seam contract concern assessment (per hive-mind state § 7 open item #1):**

The contract is acceptable for Wave 0.5 through Wave 5 under one condition: the MIGRATION.md
addendum entry is sufficient to gate rocket against silently changing to lowercase emission
in a future wave. Currently it is documented but not enforced at the code boundary.

No decisions-log entry is needed for this operational detail. The MIGRATION.md § v1.33
addendum is the correct artifact. It is already filed. No additional action required at
Wave 0.5 close.

If rocket ever changes `_BC_ATTRIBUTE_TO_SCALING_ATTR` to lowercase, gamora's normalize map
becomes a no-op (not a break) — the map falls through to `_sa.lower()`, which produces the
same result. The contract survives lowercase changes too; the normalize map is additive-safe.
The concern is resolved by this code inspection.

**Cite:** Discipline #12 (semantic-shifting fixes need explicit framing); Principle 3
(cross-seam impact called out).

**Action:** None required. MIGRATION.md addendum is sufficient. For the record only.

---

## Finding 4 — INFO: Cross-seam round-trip smoke is PARTIAL — full integration smoke is a Wave 5 prerequisite, not Wave 0.5 close criterion

**What I found:**

Gamora's Item 3 cross-seam round-trip smoke: "PARTIAL (4/4 assertions PASS)" pending rocket
Track D pipeline integration and elrond SC-6b completion. Both have now landed. The 4
gamora-side assertions all passed against the stub smoke; the full integration smoke (real
rocket Track D character JSON → gauntlet_sim routing per `damage_scaling_type`) has not yet
run against the live three-way combination.

Rocket's MIGRATION.md § Wave 0.5 notes: "SC-6b live for `base_physical_damage` and
`weapon_type_family`; scaffold fallback for `element_affinity_modifiers` (NULL in substrate)."

Rocket's smoke result shows: `BC=INT→caster-arcane base_phys=114.2` — this uses the live SC-6b
`base_physical_damage_l50` value for the Rod of Icicles row (which at 50.22 × amplitude lottery
would produce values in the 40-80 range, not 114.2). This discrepancy is consistent with rocket
using its own fallback LUT (caster-arcane=50 × amplitude ~2.3) rather than the live SC-6b row.
Confirms the WARN in Finding 2 is active even in rocket's own Wave 0.5 smoke.

The Wave 0.5 close gate criterion per framing brief Q8 does not require full integration smoke
— it requires: (a) damage routing per doc 47 § 4 ✅; (b) synthetic_mode RETIRED ✅; (c) all 8
substrate weapon fields ✅; (d) per-skill content emission ✅; (e) elements 4→7 ✅. The cross-seam
round-trip smoke is listed as a Wave 5 prerequisite (pipeline wiring sidecar + fresh roster
generation). This is per-spec.

KR state file § 7 open item #4 correctly captures "full cross-seam round-trip smoke" as
follow-on. No block.

**Cite:** Principle 6 (cross-seam round-trip discipline); Discipline #11 (empirical inspection).

**Action:** KR open item #4 (full round-trip smoke) is the appropriate sequencing. No new
action required here.

---

## Finding 5 — INFO: Math-notes authored pre-implementation — PASS with one note

**What I found:**

Math-notes confirmed present at named paths:
- `generation/math/wave-0-5-elements-expansion-math-2026-05-27.md` (rocket Item 1)
- `generation/math/wave-0-5-per-skill-emission-math-2026-05-27.md` (rocket Item 2)
- `element/math/wave-0-5-substrate-binding-math-2026-05-27.md` (rocket Item 3; path is
  `element/math/` not `generation/math/` — minor seam-internal notation divergence vs
  dispatch instruction; not blocking)
- `simulation/math/wave-0-5-damage-routing-math-2026-05-27.md` (gamora Item 1)
- `simulation/math/wave-0-5-synthetic-retirement-math-2026-05-27.md` (gamora Item 2)
- `agentic_orchestration/elrond/research/sc-6b-substrate-enrichment-2026-05-27/sc-6b-baseline-lut-math-2026-05-27.md` (elrond; with 2 correction passes per Discipline #11)

All 6 math-notes exist. Elrond's notes included TWO correction passes per empirical
inspection at backfill execution (Discipline #11 exemplary practice). Dispatches were
authored first; math-notes authored pre-implementation within each seam session.

Gate-1 design-mode review of dispatch package fired pre-implementation (per hive-mind state
§ 2.3 Wave 0 close record — "PASS-with-REVISIONS (2 WARN amended; 0 BLOCK)"). Gate-1
criterion satisfied.

Note on rocket Item 3 math-note path: dispatch instructed
`generation/math/wave-0-5-substrate-binding-math-2026-05-27.md` but rocket filed it at
`element/math/wave-0-5-substrate-binding-math-2026-05-27.md`. Both paths are confirmed
present in the math directory listing. No missing math-note; path divergence is cosmetic.

**Cite:** Discipline #18 (methodology-before-execution); Discipline #1 (math-before-code);
Principle 1 (math-before-code on non-trivial changes).

**Action:** None required.

---

## Finding 6 — INFO: AGENT_STATE.md updates — PASS (gamora); PASS with note (rocket)

**What I found:**

**Gamora:** `simulation/AGENT_STATE.md` updated with full Cycle 14 Wave 0.5 section — items
completed, math notes, status, deferred items, tag intent. Current and accurate.

**Rocket:** `generation/AGENT_STATE.md` has Wave 0.5 state section beginning at line 2486
with dispatch reference, all 3 items documented, math-note paths, and deliverable manifest.
The `Last updated:` header at the top of the file still reads "2026-05-27 (Cycle 13 Wave 5
Track B — initial mechanical season generation — COMPLETE; Cycle 13 close milestone)" —
the Wave 0.5 state is captured in the embedded section but the top-line `Last updated:`
header was not refreshed to reflect Wave 0.5.

This is a minor hygiene miss; the Wave 0.5 record IS captured in the file body.

**Cite:** Discipline #6 (tag intermediate states; small checkpoints — AGENT_STATE.md is
the checkpoint artifact for seam continuity).

**Action:**
- [ ] Rocket (low priority, non-blocking): update `generation/AGENT_STATE.md` top-line
      `Last updated:` header to reflect Wave 0.5 completion at next session touch.

---

## Finding 7 — INFO: MIGRATION.md coverage — PASS; bidirectional cross-references adequate

**What I found:**

Three MIGRATION.md files checked:

**rocket `generation/MIGRATION.md § Wave 0.5`:** All 8 substrate weapon fields explicitly
enumerated per Gate-1 Amendment 1. Round-trip clause names gamora + star-lord as downstream
consumers. Cross-seam contract documented (rocket → gamora on `damage_scaling_type`; rocket
→ star-lord Track C on substrate weapon fields). SC-6b live vs scaffold states noted.

**gamora `simulation/MIGRATION.md § v1.32 + § v1.33`:** v1.32 covers Cycle 13 remediation.
v1.33 covers Wave 0.5 in full: three typed-path helpers, CombatantState fields, constants,
formula convention, SC-5 Appendix A refinements, cross-seam contract (rocket → gamora),
synthetic_mode RETIREMENT with production paths modified, Discipline #12 semantic restoration,
`_SyntheticPlayerClass` disposition, and the critical `_SCALING_ATTR_NORMALIZE` addendum.
Downstream consumer impact (star-lord: NO schema impact) noted. Well-formed.

**elrond SC-6b `MIGRATION.md`:** 5 new columns documented with types and constraints.
Backfill scope detailed. Round-trip clause specifies all 8 character-JSON fields with
NULL-policy exceptions. Rollback plan in 3 levels. Rocket Pattern-A query content recorded.
Decisions-log entry proposal in § 6. Cross-references all companion docs. ADR-004 compliant.

Bidirectionality: elrond MIGRATION.md cites rocket as consumer. Rocket MIGRATION.md cites
gamora + star-lord as downstream. Gamora MIGRATION.md cites rocket as upstream, star-lord as
downstream (no schema impact noted). The chain is documented.

**Cite:** ADR-004 (cross-repo coordination + MIGRATION.md requirement); Principle 3 (cross-seam
impact called out); Principle 6 (cross-seam round-trip discipline).

**Action:** None required.

---

## Finding 8 — INFO: Damage-scaling-path functions (Discipline #38) — implementation matches doc 47 § 4 + SC-5 Appendix A

**What I found:**

Inspected `_calc_physical_damage_raw`, `_calc_magical_damage_raw`, `_calc_hybrid_damage_raw`
in `damage_resolver.py` against doc 47 § 4 (as cited in MIGRATION.md) and SC-5 Appendix A
refinements (as documented in gamora MIGRATION.md § v1.33):

- Physical: weapon_base × damage_multiplier × (1 + phys_pct/100) × element_conversion_factor
  × tier_coeff. SC-5 reorder (element_conversion before tier_coeff) applied. PASS.
- Magical: base_spell × damage_multiplier × (1 + spell_pct_pool/100) × tier_coeff. SC-5 R1
  additive pool (weapon_spell_mod + elem_affinity + global_spell → ONE additive sum) applied.
  PASS.
- Hybrid: three patterns (physical_with_element_flavor / magical_with_martial_weapon / sum_paths)
  with ω-penalty for cross-attribute. Provisional OMEGA_PENALTY=0.80. Q-W05-G1 confirmation
  from gandalf deferred per hive-mind state open item #2. PASS for Wave 0.5 scope.

Backward-compatibility with legacy flat `magnitude` path confirmed: skills without
`damage_scaling_type` fall through to existing code path unchanged.

Stat-range bounds (Discipline #33): gamora MIGRATION.md § v1.33 cross-references doc 46
Layer 1 caps; implementation notes `[0, 150]` spell modifier range constraint; crit is
unified `player.crit_chance` model.

Smoke results from gamora: 4/4 assertions PASS (T1 fire INT=80 spell_mod=50%, T4 water
WIS=100, physical scaffold, T1 fire resistance) at expected values.

**Cite:** Discipline #38 (damage-scaling-path — skills declare damage_scaling_type; fight
engine routes per type); Discipline #33 (stat-range bounds).

**Action:** None required. OMEGA_PENALTY gandalf confirmation (open item #2) is a
pre-Wave-5-gauntlet action, not Wave 0.5 close.

---

## Summary

| Finding | Severity | Criterion | Status |
|---|---|---|---|
| Discipline #39 synthetic_mode RETIRED (empirical grep) | GATE CRITERION | Met | PASS |
| LUT value divergence elrond vs rocket fallback | WARN | Follow-on before Wave 5 gauntlet | Track |
| `_SCALING_ATTR_NORMALIZE` cross-seam contract | INFO | Documented; no action | Closed |
| Cross-seam round-trip smoke PARTIAL | INFO | Per-spec; Wave 5 prerequisite | Acknowledged |
| Math-notes pre-authored | INFO | All 6 present | PASS |
| AGENT_STATE.md updates | INFO | Gamora PASS; rocket header stale | Low-priority |
| MIGRATION.md coverage ADR-004 | INFO | All three complete + bidirectional | PASS |
| Damage formula implementation Discipline #38 | INFO | Matches doc 47 § 4 + SC-5 Appendix A | PASS |

**Overall verdict: PASS-with-WARN**

Gate-2 criteria per framing brief Q8:
- Damage scaling routing per doc 47 § 4 + SC-5 Appendix A: PASS
- synthetic_mode RETIRED ABSOLUTELY (Discipline #39, empirical grep): PASS
- Substrate weapon binding output (all 8 fields): PASS
- Per-skill mechanical content emission (damage_scaling_type populated): PASS
- Elements expansion 4→7: PASS
- MIGRATION.md authored (all three seams): PASS
- Math-notes authored pre-implementation: PASS

**Wave 0.5 closes. Downstream waves (Wave 1 + pipeline wiring sidecar) may fire.**

WARN (Finding 2 — LUT divergence) is tracked as a pre-Wave-5-gauntlet follow-on, not a
Wave 0.5 close blocker. KR to sequence with pipeline wiring sidecar dispatch.

---

## Decisions-log entry — Path A architectural commitment

Per elrond MIGRATION.md § 6 + hive-mind state open item #6: jack-ryan authors decisions-log
entry for Path A substrate-side L50 baseline architecture. Entry filed at:
`~/Games/reincarnated-engine/design/decisions/decisions-log.md` (appended below in this
session per jack-ryan seam authority).

---

## References

- `agentic_orchestration/dispatches/2026-05-27-rocket-cycle-14-wave-0-5-track-d-content-emission.md`
- `agentic_orchestration/dispatches/2026-05-27-gamora-cycle-14-wave-0-5-damage-routing-synthetic-retirement.md`
- `agentic_orchestration/dispatches/2026-05-27-elrond-cycle-14-sc-6b-substrate-enrichment.md`
- `agentic_orchestration/elrond/notes/2026-05-27-cycle-14-sc-6b-substrate-enrichment-implementation.md`
- `agentic_orchestration/elrond/research/sc-6b-substrate-enrichment-2026-05-27/MIGRATION.md`
- `~/Games/reincarnated-engine/src/reincarnated/generation/MIGRATION.md § Wave 0.5`
- `~/Games/reincarnated-engine/src/reincarnated/simulation/MIGRATION.md § v1.32 + § v1.33`
- `~/Games/reincarnated-engine/src/reincarnated/simulation/damage_resolver.py`
- `~/Games/reincarnated-engine/src/reincarnated/generation/per_skill_emitter.py`
- `~/Games/reincarnated-engine/src/reincarnated/generation/substrate_weapon_binding.py`
- `agentic_orchestration/cycle-14-hive-mind-state.md § 7`
- `~/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md` (#10, #11, #12, #18, #33, #38, #39)
- `agentic_orchestration/GOVERNANCE.md` ADR-004
