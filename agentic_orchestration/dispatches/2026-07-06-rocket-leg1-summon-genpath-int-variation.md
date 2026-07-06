# Dispatch — 2026-07-06 — rocket — Leg 1: summon gen-path + INT-composition fix + within-cell variation axes

**From:** knight-rider
**To:** rocket
**Approved by:** Matt (VARIATION PILOT dispatch, 2026-07-06 — Option 1 ruled on the summoner-emission structural gap; Leg 0 cleared HALT=NO)
**Estimated effort:** multi-hour build; math-note-first with a hard Gate-1 stop before any code
**Acceptance:** the three sub-builds below land behind a Gate-1-ratified math note, smoke-tested, with an ADR-004 MIGRATION for the new `proxies` emission contract; both pilot cells can then be sampled with mechanical variation.

## Context

Matt ruled **Option 1** on `canonical/matt_decision_needed/2026-07-03-w3-summoner-emission-structural-gap.md`: build the missing summon-skill generation path, then re-fire summoner emission as a registered **batch 2**. This dispatch is that build. Batch-1 sampled 100/cell varying only element pair + weapon skin + names — geometry, chains, role split, T4 capstone, resource, and gear were all cell-locked. **Batch-2 samples must differ in MECHANICS, not just palette** — so this build also lands the within-cell variation axes. Summoners are a caster-subset per G4 (no separate summoner cell); the G4 knob is already verified at the knob layer (share 0.250000, W4) and must now be wired through to real emitted content.

**Leg 0 finding (HALT=NO, session-scale):** the 4 zero-composed INT cells die **upstream of the composer**, in the subspace-generator + substrate-binding path — a *different* code path than the summon gap. So this is two independent in-seam fixes bundled. Root causes and the B1 fix scope are in the Leg-0 note (required reading).

## Required reading before starting

- Leg-0 root-cause note: `reincarnated-engine/src/reincarnated/generation/notes/w3-int-cell-zero-composition-rootcause-2026-07-06.md` (engine `2980182`)
- The decision file (autopsy + jack-ryan verdict + gamora's corrected cohort-(B) decomposition): `canonical/matt_decision_needed/2026-07-03-w3-summoner-emission-structural-gap.md`
- rocket's own W3 finding note: `generation/notes/w3-ungate-refutation-fired-2026-07-03.md`
- The composer blockers: `bc_target_composer.py:97,318,380-384,756-757`; bridge `proxy_vocabulary_bridge.py:295-311`
- Engineering disciplines #1 (math-before-code), #1.2 (math-note code-citation), #2/#2.1 (smoke-test + resource-scaling), #12 (semantic shift): `~/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md`
- ADR-004 (MIGRATION.md cross-seam handoff): `agentic_orchestration/GOVERNANCE.md`

## Math-before-code (MANDATORY — Gate-1 stop)

Author a math note covering ALL THREE sub-builds BEFORE writing production code, then **STOP for Gate-1**. Knight-rider convenes the critique pair — **jack-ryan (DESIGN-MODE) + gandalf** — to review the math note. **No code until the math note is ratified.** The role-split template SET in particular must be ratified at Gate-1 (see (c)).

The math note must specify:

- **(a) Summon-skill composition path.** How the 3 verified blockers are resolved: the Phase-4d stub (`bc_target_composer.py:756-757`, currently a no-op assuming `proxy_bin=="solo"`); the multi-spawn geometry that currently maps to `multi_projectile`/`chain`/`fork` (`:380-384`) vs a real summon taxonomy; and the missing summon discriminator on `PoolMechanic`. Then: how the **existing W0 G4 knob** (share verified 0.250000 at the knob layer) is wired through so knob-selected samples emit trees carrying **real summon skills + ≥1 proxy-focused T4** in the η offer table. Define the new cross-seam `proxies` emission contract (the field(s) exported per kit; currently every kit gets `[]` per `proxy_vocabulary_bridge.py:298-299`).
- **(b) INT-composition fix (B1 per Leg 0).** The ~15–25 LOC across `bc_target_subspace_generator.py` + `bc_target_cell_sampler.py` (+ the `option_beta` attribute-only match in `bc_target_substrate_engine.py:306-313`) that makes the 4 INT cells compose real candidates. Leg 0 flagged this as borderline math-note-worthy (caster-emission-share delta) — a short note per Disc #1 suffices. **B2 (a genuine INT substrate seed) is explicitly OUT OF SCOPE — that's a separate elrond cross-seam enrichment; do NOT lash it here.**
- **(c) Within-cell variation axes** (generation/ seam; apply to BOTH pilot cells):
  - **Per-sample T4 draw:** idx-salt the `+500` capstone seed; uniform over the catalog-eligible set of the 26 (`t4_catalog_v2.py`). No new curation layer at pilot.
  - **Per-sample role-split templates:** a config surface replacing the `_CHAIN_ROLE` hard-code at `per_skill_emitter.py:364-368`. Design **≥3 templates**, each preserving **≥1 attack chain + ≥1 utility slot**. **Gate-1 ratifies this set.**
  - **Element pair:** stays per-sample as-is (already varies).
  - **Geometry jitter within band:** OPTIONAL — your math-note call; justify include/exclude.

## Cross-seam contract change? (Principle 6 gate — knight-rider completes this at authoring time)

**YES** — this dispatch adds a new `proxies` emission contract on the exported kit (rocket → star-lord/downstream boundary; currently `[]` population-wide). Therefore Acceptance MUST include the round-trip clause, and an **ADR-004 MIGRATION.md is required** documenting the `proxies` field shape and its consumer boundary.

## Scope
- [ ] Math note covering (a)+(b)+(c), authored FIRST, then Gate-1 stop (jack-ryan DESIGN-MODE + gandalf ratify; role-split template set ratified)
- [ ] (a) Summon-skill composition path: Phase-4d population, multi-spawn→summon taxonomy, `PoolMechanic` summon discriminator, bridge derivation; G4 knob wired through to emitted trees (real summon skills + ≥1 proxy-focused T4 in offer table)
- [ ] (b) INT-composition fix (B1): the 4 INT cells compose real candidates
- [ ] (c) Variation axes: per-sample T4 draw (idx-salted +500), ≥3 role-split templates (config surface), element per-sample, geometry-jitter decision documented
- [ ] Smoke-test passes (no full regen; resource-scaling rehearsal per Disc #2.1 if the sampler path scales)
- [ ] MIGRATION.md for the `proxies` cross-seam contract (ADR-004)
- [ ] Round-trip smoke per Principle 6 (below)
- [ ] AGENT_STATE.md updated at session end
- [ ] Tag: `rocket/v-pilot-leg1-summon-int-variation-<n>` (seam-prefixed; Matt approves any prefix-drop)

## Acceptance criteria
- [ ] With the G4 knob at 0.25 on a caster stem, knob-selected samples emit trees carrying **≥1 real summon skill AND ≥1 proxy-focused T4** in the offer table (key-present + non-NULL) — not hollow `[]` proxy bins
- [ ] The 4 INT cells (`ranged_medium_variable_int_none` [Cell 12], `ranged_low_spiky_int_none`, `mid_low_spiky_int_none`, `ranged_medium_variable_int_light`) compose ≥1 real candidate each on a smoke sample
- [ ] Within a single cell's smoke sample: **distinct t4_id count > 1 AND distinct role-split templates > 1**
- [ ] Round-trip smoke: production-path sample emits the new `proxies` field, consumed at the export boundary, field-presence + non-NULL checked for knob-selected kits — OR a documented not-applicable reason (there is a cross-seam change, so this is expected to apply)

## Out of scope (explicit non-goals)
- Literal weapon-rooted composition (weapon-as-identity-surface — L2+; do NOT lash to this build)
- B2 genuine INT substrate seed (separate elrond cross-seam enrichment)
- Batch-2 full-spectrum fire (gates on Leg 4 + Matt's go)
- Band re-tuning before pilot evidence (no clear-shell band touches)
- E4 ECHO ally-attack channel (sequences WITH batch-2; solo summoners sim fine per the 2 curated re-certs)
- Running the pilot itself (Leg 3 — star-lord driver + gamora shells, detached process; NOT this dispatch)

## Open questions for the agent to resolve (document in the math note)
- Geometry-jitter-within-band: include or exclude, with justification
- The exact `proxies` field shape (list of proxy-skill refs? proxy taxonomy tags?) and its offer-table linkage
- Whether the summon discriminator lives on `PoolMechanic` or a parallel structure, and the migration implication

## References
- Master dispatch: Matt's VARIATION PILOT (2026-07-06), rulings 1–3 + Legs 0–4
- Leg-0 note (engine `2980182`); decision file (collab `c37de6d` after gamora's corrections)
- Composer blockers `bc_target_composer.py:97,318,380-384,756-757`; bridge `proxy_vocabulary_bridge.py:295-311`; role hard-code `per_skill_emitter.py:364-368`; capstone seed `+500`; T4 catalog `t4_catalog_v2.py`
- ADR-004 (MIGRATION); Disciplines #1, #1.2, #2, #2.1, #12

---

## Gate-1 disposition (knight-rider, 2026-07-06)

**Math note reviewed:** `generation/notes/leg1-summon-genpath-int-variation-math-2026-07-06.md` (engine `f23d353`).
**Critique pair (parallel, DESIGN-MODE):** jack-ryan (technical) + gandalf (thematic/experiential).
**Combined disposition: RATIFY-WITH-CONDITIONS. No BLOCK from either.**

**Load-bearing finding — the divergence HOLDS:** rocket's "(a) is a wire-in, not a build" is verified empirically (jack-ryan, Disc #11). The parked emitter+bridge path is real (`skill_schema.py:181-203`; `bc_target_player_class.py:415` auto-calls `build_proxies_surface`; bridge `proxy_vocabulary_bridge.py:281` discriminates on the emitted `Skill`, NOT `PoolMechanic`). The composer Phase-4d stub (`bc_target_composer.py:756-757`) is genuinely off the emission path and stays untouched. The prior Gate-2 + decision-file "path does not exist" were scoped to the *composer* path only; the parked *emitter* path was uncovered. Legitimate finding — Option-1 cost basis dropped to a one-wire hook. gandalf: the `demo_summoner_kits` reuse is a values-template (proxy shapes), not curated-identity passthrough — struck §5.2 honored, no hollow-kit/decoration-pet failure.

**Conditions (folded into the code-build brief):**
- **C1 [gandalf, block-on-ratification]:** add a 5th role-split template `warden_leaning` (chain_C = pet-command verbs) so the summoner subset gets mechanical, not bolted-on, identity. Preserve chain_A pure-primary_attack invariant.
- **C2 [gandalf, info]:** warden_leaning chain_C + appended summon skill must read as one identity; document in note.
- **A1 [jack-ryan]:** pilot-beat/smoke asserts on `to_dict()["proxies"]` with ≥1 valid `proxy_type` on a knob-selected sample — not "summon skill present." Closes hollow-kit risk empirically.
- **A2 [jack-ryan] + F1 [gandalf]:** ADR-004 MIGRATION for `proxies` population change ([]→populated; shape stable; no PoolMechanic migration); include gamora + drax consumer notes; roster-fill trigger reads SURVIVAL (tier_2 gate pass), not mere emission.
- **A3 [jack-ryan, warn]:** rng-draw over `% len(TEMPLATES)` for role-split coverage.
- **A4 [jack-ryan]:** T4 seed-collision guard for cells > 499 samples (pilot N=100 safe).

**Ratified as-is:** geometry-jitter exclusion (both, Disc #12/#25); G4 at 0.25 emitted share (gandalf); INT B1 fall-through (jack-ryan — Cells 12/16 hit the skip; 13/14 route via `_apply_section_4_routing:257-267`).

**Code build fired** post-disposition with all conditions inline.

---

## Completion record (rocket, 2026-07-06)

**Status: DONE. All (a)/(b)/(c) + all 7 conditions landed. Smoke ALL GREEN. Tag `rocket/v-pilot-leg1-summon-int-variation-1` (pushed, engine `0eb6e06`).**

**What landed:**
- **(a) summon gen-path (WIRE-IN):** `SkillEmissionConfig.proxy_density` (`per_skill_emitter.py`) threaded from `enc.bc_proxy_density` (`season_generation_pipeline.py:~1036`). `_make_summon_skill` appends ONE summon skill on `light/heavy` draws → `build_proxies_surface` emits non-empty `proxies`. `proxy_geometry="projectile"` → `autonomous_caster` (spectral-ally caster summon; magnitudes None → gamora). Composer untouched. `KitCandidate.to_character_dict()` now emits the `proxies` key (was absent — the season pipeline emits KitCandidate, not PlayerClassV2; this closes A1 end-to-end).
- **(b) INT B1:** `bc_target_subspace_generator.py` — non-locked BLOCKED option_beta INT cells fall through to `_bind_and_build` Step-5 last-resort instead of returning None. Cells 13/14 handled via their existing locked routing (`_apply_section_4_routing`). B2 = elrond, out of scope.
- **(c) variation:** per-sample T4 (`enc_seed+500+sample_idx`, A4-guarded ≤499); 5 role-split templates rng-drawn (A5); element per-sample as-is; geometry-jitter excluded.

**5-template SET final form:** `balanced_striker` (T0 baseline) · `control_leaning` · `dual_offense` · `support_specialist` · `warden_leaning` (C1 — chain_C = rally-the-construct/mend-the-construct verbs). Import-time assert enforces chain_A-all-primary_attack in EVERY template → §1c signature-ailment emission invariant. C2: summon (autonomous_caster spectral ally) + warden chain_C = ONE identity (documented math note §4.2a; drax renders together).

**Smoke results (`generation/notes/leg1_summon_int_variation_smoke_2026_07_06.py`, ALL GREEN, 0.75s, no LLM/no regen/no fights):**
- **A1 proxies round-trip:** `to_character_dict()["proxies"]` carries a valid `autonomous_caster` proxy_type (light→count 1, heavy→count 2); solo→`proxies==[]`. Proven at BOTH emitter+bridge AND KitCandidate production boundary.
- **A3 distinct checks:** distinct role-split templates = **5**, distinct t4_ids = **12** over 30 samples (both > 1, margin).
- **B1:** all 4 INT cells (12/13/14/16) compose a real candidate; forced-BLOCKED 12/16 fall through (`b1_fallthrough=True`, not None).
- Regression: 195 PASS across proxy/subspace/emitter suites; `test_bc_target_subspace_generator` 27 PASS. Two pre-existing failures (confirmed on stash-baseline, NOT mine): d6 grouping-vocab-doc missing; `test_w3_emission_driver` hardcoded-300/400-split vs N=1 smoke.

**MIGRATION path (ADR-004):** `generation/MIGRATION.md` [2026-07-06] entry — `proxies` POPULATION change (`[]`→populated for knob-selected summoners; SHAPE stable; NO PoolMechanic migration) + `KitCandidate.to_character_dict()` now emits the contract. gamora note (first production population; calibrate scaffold magnitudes; F1 clear-shell gate); star-lord note (PlayerClassV2 path no-action; KitCandidate key now present); drax note (render summon+warden as one identity). **F1: roster-fill/G4-share accounting reads SURVIVAL (tier_2 clear-shell pass), NOT emission.**

**Tag:** `rocket/v-pilot-leg1-summon-int-variation-1` (engine `0eb6e06`, pushed to origin/main + tag).

**READY FOR LEG 3.** The gen-path emits real summoners at the G4 ~25% share + varied kits (T4 + role-split + element). Leg 3 (pilot run: star-lord driver + gamora shells, detached) can fire. gamora owns the F1 clear-shell survival gate for correct G4-share accounting (emission ≠ shippable).

**Nothing needs re-Gate.** All conditions were folded pre-build; the two consequential design amendments (5th template, KitCandidate proxies wire) were mandated by the ratified conditions (C1, A1) — no new design surface introduced.
