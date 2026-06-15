# Finding — 2026-06-15 — rocket weapon-as-identity Phase-2 (envelope composer)

**Reviewer:** jack-ryan
**Severity:** PASS-WITH-AMENDMENTS (one WARN, two INFO; no BLOCK)
**Target:** commit `137ed25`, tag `rocket/v1.3-weapon-as-identity-phase-2` (engine repo, NOT pushed)
**Developer:** rocket
**Principles applied:** 1 (math-before-code), 2 (smoke-gate), 5 (severity matters), 6 (cross-seam round-trip), honest-fail clause
**Disciplines cited:** #1 / #1.2 (code-cited math), #2.1 (resource-scaling), #8 (schema validation at boundaries)

## Verdict

**PASS-WITH-AMENDMENTS.** The PASS is REAL, not force-passed. The honest-fail tripwire is live (proven to engage). All four Gate-1 amendments are honored in code at source. gandalf Q2 reach-order honored. No regression of Phase-1. Out-of-scope respected. This CLEARS the recognition record's kit_size headline gate (§4.1: 10-13 band reached off the weapon-gated geometry sub-palette with the sparse mechanic-pool path disabled). One WARN and two INFO are recorded below — none blocking; all are gate-quality / future-design notes, not falsifications.

## What I found (descriptive)

I re-ran the gate harness myself (`python3 scripts/weapon_as_identity_phase2_gate_2026_06_15.py`): exit 0, reproducible, OVERALL ALL PASS, §4.1 HEADLINE VERDICT PASS. I independently AST-parsed `weapon_envelope_composer.py` (not trusting the gate's self-report) and confirmed zero executable references to any mechanic-pool symbol — the module imports ONLY `ability_grammar`, `skill_composition`, `skill_schema`. I traced the `_draw_geometry_distinct_first` draw logic to determine whether the worst-cell floor of 11 is genuine native geometry or a prop. I diffed the commit (5 files: 3 new + 2 amended; additive-only confirmed) and confirmed `balance_loop.py` / b6 / composed_kit / class_generator / per_skill_emitter are untouched. Targeted pytest: 24 passed, 0 failures, 5786 deselected.

## Amendment-by-amendment verification (at source)

**Amendment 1 — pool-count reconciliation: HONORED.** math-note §8.2 carries the code-time re-snapshot: ACTIVE 8/6/4/2 (rage/focus/combo/stamina), no `is_primary` flag in live YAML (so the dispatch's PRIMARY 4/4/2 is a doc-comment subset, not a queryable partition), starvation holds under BOTH readings (every pool < 10). Canonical physical-row count corrected to **1,855 of 2,405 selectable** (the math-note's earlier 463 was the `cleave` proxy_geometry_class subset mis-cited as the total — explicitly corrected). Element-affinity 33/1,855 = 1.78% ≤1.8% invariant holds. Verified at `notes/...phase-2-math-note.md:463-484`.

**Amendment 2 — geometry-only-distinct reported SEPARATELY and IS the floor test: HONORED, and the tripwire is LIVE.** The gate's `meets_floor` keys on `result.geometry_only_distinct >= 10` (script:196), NOT on `triple_distinct`. The two counts are emitted as separate JSON blocks (gate output `geometry_only_distinct` vs `triple_distinct`). I verified the tripwire is not dead code: I fed `_draw_geometry_distinct_first` a forced 7-geometry palette and it returned distinct=7 with `step3_fired=True` — i.e. **if the palette were genuinely starved below 10, the harness WOULD report geometry-only-distinct < 10 and route HONEST_FAIL**. The honest-fail clause is enforced (script:271-276 sets VERDICT=HONEST_FAIL and `honest_fail_routing` to gandalf when central geometry-only < 10).

**Amendment 3 — flaming-greatsword non-leak fixture: HONORED as a real code assertion.** `gate_4_3_flaming_greatsword` (script:280-331) is an executable fixture, not prose. `{"fire":25}` weapon → asserts `damage_scaling_type==["physical"]`, `scaling_attribute==["strength"]`, `canonical_element==["fire"]` (flavor applied), and `no_cross_envelope_geometry` (0 caster geometries). All four assertions PASS in the artifact. The non-leak is structurally guaranteed: STEP-4 pins `damage_scaling_type="physical"` BEFORE STEP-5 writes only `canonical_element` (composer:344-356), and the L1 derivation reads neither field.

**Amendment 4 — `PHYSICAL_GEOMETRY_PALETTE` + proxy→sub-palette mapping cited NET-NEW: HONORED.** math-note §8.1 explicitly states "This does NOT exist today" with citation that `geometry_derivation.py:370 _physical_geometry()` is keyed on `(role, effects, cooldown)` NOT `proxy_geometry_class`. The palette + mapping live in the new `weapon_envelope_composer.py` (composer:42-111) with the NET-NEW framing in the module docstring. No `src/reincarnated/canonical/` write (correct — this is generation-internal content logic, not engine-canonical reference data; rocket's call, within seam).

## gandalf Q2 verification (reach-order + never-cross + frequency signal)

**HONORED.** (a) Step-3 NEVER crosses envelope: `_build_subpalette` carries a runtime `assert not (set(weights) & CASTER_ENVELOPE_GEOMETRIES)` (composer:186-188) and the palette-invariant gate confirms 0 overlap. A greatsword's weights never contain `aura`/`beam_channel`/`totem` — the fill-draw in Phase-3 redraws from the SAME weighted physical palette only (composer:227-234). (b) Step-3 reported as a frequency signal: 0 floor-rescue reaches (`kits_with_step3_fired=0`), 23 total fill-draws across 64 kits (mean 0.36/kit) — labeled LOW pool-growth signal for elrond. Correct.

## Honest-fail integrity — the central probe (is the PASS propped?)

**The PASS is REAL. It is not propped by role/tier rescue.** I determined the exact mechanism: `geometry_only_distinct == min(kit_size, palette_size)` deterministically. The melee palette is 11 native geometries; kit_size is 10-13; so geometry-only-distinct lands at 10 or 11 — and crucially, `triple_distinct == geometry_only_distinct` at the floor in every weapon class I tested (single/cleave/AoE/multi-hit/scatter/cone × melee/ranged). Role and tier add NOTHING at the floor; the floor is met purely by the native physical geometry palette having ≥10 entries. That IS the gandalf-ratified design claim (the weapon gates a sub-palette; richness lives in the gated vocab, mirroring the caster path's 26-geometry mana spread). The worst-cell median of 11 is genuine native geometry, not a prop. rocket's report of "worst cell = exactly 10" is the per-KIT minimum (a kit_size=10 kit yields exactly 10 distinct), which is honest and correct — the per-CELL median is 11.

## Rationale (cites)

- The honest-fail clause (dispatch) requires geometry-only-distinct to be the falsification tripwire measured independently of role/tier. Verified live: tripwire engages on a starved palette (forced-7 probe). Satisfies Principle 2 (smoke-gate) + the dispatch's honest-fail discipline.
- Principle 6 (cross-seam round-trip) NO verdict holds at source: the composer reuses `grammar.generate(forced_geometry=...) + composer.compose()` and post-overrides only EXISTING Skill fields (`damage_scaling_type`, `scaling_attribute`, `canonical_element`). No field added/renamed/removed; no MIGRATION.md required. Discipline #8 (schema validation at boundary) satisfied.
- Out-of-scope respected per ADR-004 cross-seam discipline: additive-only diff, b6/G4/G5/G7/G8 intact, balance_loop.py not in commit, no L1 literal-root refactor, no L2 hard-wire.

## WARN / INFO (non-blocking)

**WARN — the math-note's predicted MARGINAL corner (§2.4) no longer exists in code, and the honest-fail tripwire therefore cannot fire under the current 11-entry palette.** The math-note predicted an 8-10 MARGINAL yield for "single melee-light weapon × single-target cell." The shipped code uses WEIGHTS-not-gates (the full palette stays reachable), so even the narrowest weapon draws min(kit_size, 11) ≥ 10 distinct geometries. This is a legitimate gandalf-ratified reframe (§8 addendum) and the RIGHT design — but it means the tripwire can only engage if the physical palette itself shrinks below 10. Today it cannot. The tripwire is real but currently un-triggerable by any in-scope weapon. Recommendation: when the palette or its per-weapon reachability is ever narrowed (e.g. a future hard-gate on coherence), re-confirm the tripwire's live range. No action required now.

**INFO — `worst_cell_median` and the §4.1 "worst cell = exactly 10" framing differ in denominator.** The gate reports per-cell MEDIAN (=11); rocket's narrative "worst = mid-DEX = exactly 10" describes a per-kit minimum. Both are true and both are in the artifact; the narrative could read as a per-cell median of 10, which it is not. Naming nit only.

**INFO — `_role_for_geometry` mobility branch (composer:245) is dead for two of three mobility geometries.** The guard `geometry in _MOBILITY_GEOMETRIES and geometry == "defensive_dash"` means only `defensive_dash` ever returns "mobility"; `dash_attack`/`leap_strike` fall through to AOE/primary. Harmless (role spread still clears the triple), but the `_MOBILITY_GEOMETRIES` frozenset is wider than the code that consumes it. rocket's call whether to tighten.

## Action

- [x] jack-ryan: APPROVE Phase-2 commit `137ed25` for tagging at intermediate-tag scope (PASS-WITH-AMENDMENTS; the amendments are non-blocking notes).
- [ ] rocket (optional, non-blocking): consider the two INFO items (per-cell-median framing in narrative; `_role_for_geometry` mobility-branch tightening) at next touch. Neither gates this commit.
- [ ] knight-rider / Matt: this clears the recognition record's kit_size headline gate. Milestone tagging (dropping the `rocket/` seam prefix) remains Matt-gated per ADR-002. Push remains Matt-gated.

## References

- `/Users/admin/Games/reincarnated-engine/src/reincarnated/generation/weapon_envelope_composer.py`
- `/Users/admin/Games/reincarnated-engine/scripts/weapon_as_identity_phase2_gate_2026_06_15.py`
- `/Users/admin/Games/reincarnated-engine/output/weapon-as-identity-phase2-gate-20260615.json`
- `/Users/admin/Games/reincarnated-engine/src/reincarnated/generation/notes/2026-06-15-weapon-as-identity-phase-2-math-note.md` (§8 code-time addendum)
- commit `137ed25` (engine repo); tag `rocket/v1.3-weapon-as-identity-phase-2`
