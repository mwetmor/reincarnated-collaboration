# Finding — 2026-06-15 — b6-deletion Prerequisite A — Gate-1 (adversarial-pool construction)

**Reviewer:** jack-ryan
**Mode:** DESIGN-MODE (Gate-1, peer collaborator with rocket)
**Severity:** WARN (CLEAR-WITH-AMENDMENTS)
**Target:** commit `c2ba6c4`, tag `rocket/v1.3-b6-deletion-prereq-A-math-note` (engine repo)
**Developer:** rocket
**Principles applied:** #1 (math-before-code), #3 (cross-seam impact), #5 (severity), Review-Principle smoke-gate; Disciplines #1/#1.2, #2/#2.1, #11
**Verdict:** **CLEAR-WITH-AMENDMENTS** — one BLOCK-class amendment must be folded into the gate script before the run; everything else clears.

## What I found

I verified rocket's three load-bearing claims at source, not on assertion.

**Crux 1 — palette-driven / weapon-attribute-INVARIANT: CONFIRMED.** `_build_subpalette` (`weapon_envelope_composer.py:140-189`) only multiplies weights on geometry subsets; it never deletes a key, so the full palette dict is always returned. `_draw_geometry_distinct_first` draws `min(kit_size, len(geos))` distinct without replacement (`:218`). `PHYSICAL_GEOMETRY_PALETTE` is exactly 11 entries (`:49-61`); `RANGED_PHYSICAL_UNLOCK` adds 3 → 14 (`:66-70`). Therefore `geometry_only_distinct = min(kit_size, 11)` for melee and `min(kit_size, 14)` for ranged, regardless of weapon attributes. **rocket's honest reframe holds: an attribute-thin pool cannot move the floor, and L-A (pinning the headroom-1 melee corner as the central case) is the correct true stressor.** I find no path by which attribute/pool composition moves `geometry_only_distinct` — the only path that could is a grammar override re-merging a forced geometry, which is exactly what the tripwire is for (Crux 3).

**Crux 2 — headroom-1 caveat handled honestly: CONFIRMED.** § 4.4 surfaces the exactly-10/zero-slack melee property and routes both non-falsifying refinements (palette 11→≥13 expansion; or accept floor-exact) to gandalf rather than designing the stress away. The PASS is pinned to b6's protected corner, not the friendly median. This is the load-bearing honesty the dispatch's honest-fail clause demands.

**Crux 3 — honest-fail tripwire LIVE in the harness: PARTIAL — this is the amendment.** The tripwire mechanism (`step3_fired = len(set(drawn)) < 10`, `:239`; cross-envelope `assert :186-188`) is live in the composer. But the **PASS gate in `gate_4_1` keys on the GLOBAL median** (`central_geometry_only_ge_10`, computed at `:209-210, :222`, gated at `:269, :272`). The harness already computes `worst_cell_median` (`:220, :256`) and `min_geo_only` (`:211`) but **neither is wired into the PASS verdict.** This is the same median-masks-a-minority-collapse class of concern I verified on the Phase-2 tripwire.

It bites HERE specifically: the physical (STR/DEX) encounter set in `endgame_encounter_catalog.py` mixes `bc_range` melee, mid, AND ranged cells (e.g. `endgame_bc_ranged_low_spiky_str_none:169`, `endgame_bc_ranged_high_flat_dex_none:381`, `endgame_bc_mid_high_flat_dex_none:463`). Under the natural `_RANGE_TO_PROFILE` map (`:62`) those resolve to the 14-geometry palette → distinct 13-14. rocket's L-A § 3.1 says it will "ALSO run a melee-forced variant" on DEX/ranged cells. If both the melee-forced (11-palette → 10) AND the natural ranged (14-palette → 13-14) kits land in the same pooled distribution, the global median sits at 11-13 — and a single melee-corner cell collapsing to 9 would hide under a passing median. The adversarial run's whole point is to make the headroom-1 corner the central case; a global-median tripwire silently un-does that pinning the moment a 14-palette cell is also present.

## Rationale

Review-Principle smoke-gate + Discipline #11 (empirical inspection over assumption): a gate's PASS condition must be evaluated on the protected corner, not a pooled aggregate that can dilute it. The construction's hostility is real (Crux 1+2), but the **gate that reads it** must fire honest-fail on the worst headroom-1 melee subset, or the rigor rocket built into the pool leaks out at the verdict line. This is a within-seam gate-script change (no schema, no field) — Principle-6 confirmed NO (Crux 4 below), so it is the developer's to fold and remains my approval authority per ADR-002 (within-seam, test/harness-only).

**Crux 4 — run scope: CONFIRMED CLEAR.** Smoke-scale, LLM-free, deterministic, ~256 kits, 2-3 min (§ 5). "Multi-day" is workstream effort, not regen size. Right tool for a structural geometry-count question (Discipline #2.1). Principle-6: no new field, no MIGRATION — the adversarial selector is a read-only query/in-memory-fixture extension over columns that already exist (`proxy_geometry_class`, `proxy_range_class`, `proxy_tempo_class`, `element_affinity_modifiers_json`). Confirmed at `:71-104` (query) and § 6. No cross-seam emission change.

## Action

- [ ] **rocket (AMENDMENT — fold before run):** The honest-fail PASS gate must evaluate `geometry_only_distinct >= 10` on the **headroom-1 melee subset's worst-cell median (and report `min_geo_only`)**, NOT the pooled global median across the melee+ranged adversarial set. Concretely: either (a) wire `worst_cell_median >= 10` (and `min_geo_only >= 10` for the meets-floor invariant) into the PASS condition alongside `all_in_band`, partitioning the melee-forced (11-palette) cells from the ranged (14-palette) cells so the 11-palette subset is graded on its own worst cell; or (b) run the adversarial set as melee-forced-ONLY on every cell (DEX/ranged included, per L-A § 3.1) so median == worst by construction and the global-median tripwire becomes sound. Either is acceptable; (a) is the more honest report because it preserves the ranged diagnostic alongside the pinned-melee verdict. Document which in the gate script header.
- [ ] **rocket:** Surface `min_geo_only` and `worst_cell_median` in the run artifact's headline (not just nested diagnostics) so the headroom-1 corner is the first number Gate-2 reads.
- [ ] **jack-ryan (Gate-2, post-run):** Verify the amended tripwire actually fires on the worst melee cell and that step3_fired distinguishes "kit_size > palette (structural, expected under L-C)" from "floor unmet from native palette (the falsification sense)" per § 3.4.

No escalation to Matt required: this is a within-seam harness amendment to a gate I authored the amendment-2 requirement for; clears under ADR-002.

## Clearance

**rocket is CLEAR-TO-RUN once the worst-cell/min tripwire amendment is folded.** The pool construction itself (L-A primary + L-B/L-C/L-D composed levers) is sound and genuinely hostile — I see no missing hostility lever. The only gap is at the verdict line, not in the pool. Do NOT run on the global-median PASS gate as currently wired; it would risk a trivially-friendly pass if any 14-palette cell dilutes the median.

## References

- `~/Games/reincarnated-engine/src/reincarnated/generation/notes/2026-06-15-b6-deletion-prereq-A-adversarial-pool-math-note.md`
- `~/Games/reincarnated-engine/src/reincarnated/generation/weapon_envelope_composer.py` (`:49-61` palette, `:140-189` subpalette weighting, `:192-240` distinct-first draw, `:186-188` cross-envelope assert, `:239` step3_fired tripwire)
- `~/Games/reincarnated-engine/scripts/weapon_as_identity_phase2_gate_2026_06_15.py` (`:62` range map, `:71-104` query, `:209-222` median gate, `:220/:256` worst_cell_median, `:269-272` PASS verdict)
- `~/Games/reincarnated-engine/src/reincarnated/generation/endgame_encounter_catalog.py` (`:169, :381, :463` mixed-range physical cells)
- `~/Games/reincarnated-engine/design/decisions/decisions-log.md` (no locked entry in conflict; b6 Decision 2 governed by recognition doc, gate is its validation prereq)
