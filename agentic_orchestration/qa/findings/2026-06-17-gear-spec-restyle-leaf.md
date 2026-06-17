# Finding — 2026-06-17 — gear-spec §7.2 restyle-leaf (Wave B2)

**Reviewer:** jack-ryan
**Severity:** INFO (PASS-WITH-INFO)
**Target:** commit `5f85014`, tag `rocket/v-gear-spec-restyle-leaf-1` (not pushed)
**Developer:** rocket (generation seam)
**Principles applied:** Review Principle #1 (math-before-code), #2 (smoke-gate), #3 (cross-seam impact), #5 (severity matters); Disciplines #1, #2, #8; ADR-004 (cross-seam MIGRATION)

## What I found
The build conforms to the §7.6 StyleProfile ruling on all three rules and is grounded in real elrond substrate. I independently ran the smoke harness against the regenerated `synty_catalogue.db` (08:24 mtime) — it PASSES end to end: modular pack 101 derives `per_region` with 5 region entries + present `whole_tint`; whole_atlas pack 31 (0 region masks) derives `whole_tint` with empty regions; accent system enumerates exactly 17 verified sockets and binds to a real `assets.member_path` (`back_accent` row); invented-socket `All_99_Bogus` is rejected with ValueError; the 5-zone channel-test classifies each corner to its own zone and a (0.5,0.5,0.5) midpoint to None; emission deltas are 0.10/0.15/0.20/0.30 (monotone-accelerating). I verified the DB schema directly: every field the module consumes is real (`textures.texture_role`, `textures.channel_region_map`, `packs.structural_class`, `packs.recolor_scheme`, `assets.is_accent`, `assets.member_path`, `assets.slot`) — no invented fields. The `structural_class='modular'` filter yields exactly 1 pack (101), matching elrond's MIGRATION line-120 consumer-caveat verbatim. The module has zero engine/sibling imports (pure leaf), and nothing in the tree imports it yet (additive; no contract surprise to existing consumers). The spec note precedes and is cited by the code (Discipline #1), and the ε=0.25 channel-test math is sound: the 5 RGB-corner keys have minimum pairwise distance 1.0 (e.g. CYAN↔BLUE), so a quarter-distance band admits compression noise without ever confusing two corners.

## Rationale
- **Discipline #1 (math-before-code):** spec note §2.2/§2.3/§2.4 authored first; code cites the note in module docstring and per-function. ε=0.25 derivation is correct (min corner separation 1.0; 0.25 < 0.5 half-distance → no double-membership). PASS.
- **Discipline #2 (smoke-test):** harness exercises BOTH fill-densities against the REAL regenerated DB read-only; passes on independent run (EXIT=0). PASS.
- **Schema fidelity (Discipline #8):** all consumed columns exist; 5-zone scheme matches DB `channel_region_map` byte-for-byte; `structural_class='modular'` caveat honored. PASS.
- **Ruling conformance:** rule 1 (mode mesh-derived via `derive_mode`, not generator-chosen) — held; rule 2 (`whole_tint` always present) — structurally guaranteed (required non-Optional pydantic field; both return paths populate it); rule 3 (provisional labels, additive-nullable) — held, labels flagged provisional. PASS.
- **Cross-seam (ADR-004):** MIGRATION names drax §7.5 + star-lord §7.3 with concrete consumption seams (`classify_zone` mirror for drax adapter; `build_palette(region_tints=, region_finishes=)` fill seam for star-lord). Pure-downstream/generate-forward invariant holds. PASS.

## INFO notes (non-blocking; for the record)
1. **Socket-count nuance is documented, not hidden.** Dispatch/MIGRATION colloquially say "12 named accent sockets"; the rig truth is 13 `All_NN` (incl. `All_12_Extra` spare) + 4 cape = 17. rocket built to the verified 17-socket superset and rejects anything outside it — superset-safe, no socket invented. The reconciliation is explicit in spec note §1.3. No action; flagging so drax/star-lord readers aren't surprised by "17" when the dispatch said "12."
2. **DB `is_accent` taxonomy (10 slot-classes) is a SUBSET of the rig socket set, by design.** rocket correctly treats galadriel's rig extraction as the authoritative socket truth and the DB `is_accent` slots as the part→socket binding hint. Worth a one-line note to star-lord §7.3 so the LLM-fill keys accents off rig sockets, not the DB slot vocabulary.
3. **Provisional zone labels (metal vs leather) remain an open galadriel render-pass dependency.** Correctly scoped as a known gap, not a schema contradiction (5-zone COUNT is decision-grade). drax §7.5 must not hard-bind label semantics until the render pass locks them.

## Action
- [x] Developer: no rework required. Build is sound; tag stands.
- [ ] knight-rider (carry-forward): when drax §7.5 + star-lord §7.3 dispatches fire, surface INFO #1 (17 vs "12" sockets) and INFO #2 (rig-socket authority over DB slot taxonomy) in their dispatch context.

## Escalation
None. No BLOCK, no decisions-log conflict, no locked-decision contradiction, no Matt/gandalf decision needed. PASS-WITH-INFO is within ADR-002 within-seam tier (additive module, no cross-seam schema break to existing consumers).

## References
- `/Users/admin/Games/reincarnated-engine/src/reincarnated/generation/gear_style_profile.py`
- `/Users/admin/Games/reincarnated-engine/src/reincarnated/generation/notes/2026-06-17-gear-spec-restyle-leaf-spec-note.md`
- `/Users/admin/Games/reincarnated-engine/src/reincarnated/generation/notes/smoke_gear_style_profile_2026_06_17.py`
- `/Users/admin/Games/reincarnated-engine/src/reincarnated/generation/MIGRATION.md` (2026-06-17 entry)
- `/Users/admin/Games/reincarnated-engine/src/reincarnated/generation/AGENT_STATE.md` (2026-06-17 checkpoint)
- `/Users/admin/Games/reincarnated-collaboration/canonical/story/styleprofile-output-shape-ruling-2026-06-17.md` (§7.6 ruling)
- `/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/research/curated/MIGRATION.md` (elrond v1.11 consumer-caveat, line 120)
- `/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/research/curated/synty_catalogue.db` (substrate, schema v1.0)
