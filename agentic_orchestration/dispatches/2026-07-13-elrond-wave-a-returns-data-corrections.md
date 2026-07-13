# Dispatch — 2026-07-13 — elrond — Wave-A returns-adjudication data corrections + mint-dossier backfill

> **⛔ SUPERSEDED — EXECUTED-VIA-GANDALF-PROMPT (do NOT launch a second elrond session).**
> Matt already launched elrond under gandalf's running prompt, which is a **SUPERSET** of this dispatch:
> - **Fold 1** (= this dispatch): the 4 returns-corrections below.
> - **Fold 2** (NOT in this dispatch): key the 9 mint dossiers into `canon_engine_key` so they plot on the atlas.
> Launching a second elrond = two concurrent writers on `corpus.db` = the 2026-07-11 double-writer anti-pattern the Gate-1 note warned against. This dispatch is retained for lineage; its scope is subsumed by the live gandalf-prompted session. **KR launches only rocket + gamora for the Wave-A slices; elrond is already live.**

**From:** knight-rider
**To:** elrond (data steward — `research/curated/corpus.db` + curation seam)
**Approved by:** Matt — corrections fall out of the Wave-A returns adjudication (gandalf, ruled 2026-07-13 in the Wave-A KR-handoff). These are corpus-DB corrections within elrond's stewarded seam (not external/production systems), so they execute under the standing data-steward mandate; KR routes.
**Pattern:** B (discrete but multi-item DB curation; own session memory)
**Estimated effort:** ~half a day
**Folds in cleanly** — independent of the rocket/gamora Wave-A engine slices; no ordering dependency.

## Context

The Wave-A returns adjudication surfaced four data corrections to the curated corpus DB (`research/curated/corpus.db`, stood up under Q24 2026-07-12). Three are game-attribution / dedup / canon-flag fixes; one is a mint-dossier metadata backfill. None re-opens a closed Wave-A fork — these are pure data hygiene against the ratified corpus.

## Required reading before starting

- Wave-A KR-handoff (the returns adjudication block): `agentic_orchestration/gandalf/design-inputs/wave-a-KR-handoff-2026-07-13.md` § "Data-correction routing"
- Wave-A rulings (the enrichment-kit list — confirms `le-ring-of-shields` corrected from `poe1-*`): `agentic_orchestration/gandalf/design-inputs/wave-a-summon-proxy-RULINGS-2026-07-13.md`
- Your Q24 ingest brief: `agentic_orchestration/gandalf/briefs/2026-07-12-elrond-corpus-ingest-brief.md` (the DB you're correcting)
- ADR-004 (MIGRATION) / ADR-006 (read-only-by-default — these writes are to YOUR stewarded corpus DB, in-scope; NOT production telemetry)

## Scope (the four corrections)

- [ ] **1. Game-attribution fix:** `poe1-ring-of-shields` → `le-ring-of-shields` (Last Epoch, not PoE1). 2-source confirmed in the adjudication. Re-key the row + any lineage/join references; preserve provenance (git audit trail per Law 2 — do not silently drop the old key without a lineage note).
- [ ] **2. CotA vs IK-HotA — ruled DISTINCT, no dedup:** `d3-call-of-the-ancients` (Call of the Ancients) and `ik-hota` (Immortal King Hammer of the Ancients) are separate kits. Confirm both rows stand as distinct; **do NOT merge/dedup.** If a dedup candidate flag exists on either, clear it with the ruling citation.
- [ ] **3. `d2-sacrifice` negative-canon flag:** set `negative=1` (KEEP). Joins the existing 37-entry negative-canon family; **excluded from the S6 population.** Confirm the negative-canon exclusion is honored by whatever view feeds S6.
- [ ] **4. Mint-dossier backfill:** ingest the 9 mint dossiers' `era_year` / `patch` + URL backfill (2026-07-13 dossiers). Fill the metadata columns; do not alter kit identity.

## Cross-seam contract change? (Principle 6 gate — KR completed at authoring time)

**Assess and state explicitly.** If any of these changes a column/key on a table that star-lord's engine-side telemetry boundary reads (ADR-004 boundary), write a MIGRATION note and state the round-trip disposition. If all four are self-contained corpus-DB curation with no consumer beyond elrond-stewarded views + the S6 population filter, state `Round-trip: not applicable because <reason>` and note which view feeds S6 so the negative-canon exclusion (#3) is verified end-to-end.

## Acceptance criteria

- [ ] `le-ring-of-shields` re-keyed; old `poe1-*` key carries a provenance/lineage note (not silently dropped).
- [ ] CotA / IK-HotA confirmed distinct; no dedup fired.
- [ ] `d2-sacrifice` `negative=1`; S6-feeding view confirmed to exclude it (verify, don't assume).
- [ ] 9 mint dossiers' `era_year`/`patch`/URL backfilled.
- [ ] Round-trip disposition stated (MIGRATION note if any star-lord-boundary column changed; not-applicable justification otherwise).
- [ ] Auto-commit; **NO push** (Matt-gated per ADR-006).

## Out of scope

- Re-opening any closed Wave-A fork (these are data corrections, not design).
- Any change to the roster-atlas / lineage tables beyond the four items above.
- Applying any migration to production telemetry (star-lord seam; Matt-gated).

## Completion record
_(append: each correction's before/after; the S6-feeding view name + negative-canon exclusion verification; round-trip disposition; any MIGRATION note path; tag)_
