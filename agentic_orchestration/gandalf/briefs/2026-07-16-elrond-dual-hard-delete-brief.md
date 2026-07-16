# elrond charge — IMMEDIATE dual hard-delete (all 182 breach rows: 62 LA + 120 mcd) + ingest-provenance census — FIRED

**From:** gandalf (SPEC-AUTHOR) · **Date:** 2026-07-16 · **Status:** FIRED
**Authority:** Matt wave-3 ruling 2026-07-16, verbatim: *"I also recommend the immediate deletion of the old MCD and Lost Ark data."* — composed with wave-2 verbatim *"I recommend that we delete the entire Lost Ark corpus."* Both logged in `canonical/matt_decision_needed/2026-07-16-edition3-vs-refit-candidate-1-adoption.md` § RULING + WAVE 3. The catalogue never-purge philosophy's Matt's-word carve-out is hereby EXERCISED.

## The charge (corpus.db + atlas MIGRATION.md)

1. **Pre-delete provenance archive → atlas `MIGRATION.md`:** for all 182 rows (62 LA: 56 `grain=class` + 6 Destroyer `grain=kit` · 120 mcd: `grain=gear` incl. the 26 no-key), archive per-row: key/id, name, source, grain, ingest lineage (which script/session inserted it — best-effort from provenance columns + git history of the ingest scripts). This is the permanent record; the rows will not exist after step 2.
2. **The 182-row ingest-provenance CENSUS (owed since wave-2):** one short MIGRATION subsection answering *how did 182 spec-orphaned rows enter?* — which ingest paths, which sessions, confirming the §9.19.1 breach record (no §2 seating, no §4 sources row, no five-stage pipeline). Facts only; the root-cause ruling (spec-stewardship, Legolas exonerated) is already canon.
3. **HARD DELETE all 182 rows from corpus.db.** Expected exact counts: LA=62, mcd=120. HALT if either count mismatches — do not delete a fuzzy set.
4. **Post-delete asserts (fail-loud, report numbers):** grain census = `kit` 509 · NULL 18 · `gear` 0 · `class` 0 (total 527) · **zero E1-469 members deleted** (all 182 were post-E1 growth — assert before delete, not after) · Edition-III served artifacts + Refit-Candidate-1 artifacts byte-untouched.
5. **Record the STAGING LAW in MIGRATION** alongside the GRAIN LAW (Matt wave-3 verbatim): *the real archipelago derivation builds on the post-deletion kit-grain corpus WITHOUT LA/MCD; re-harvested LA/MCD corpora land catalogued-only and enter atlas fits only AFTER the archipelago passes its pre-registered hold-out gates; admission then = new-Edition refit.* Spec cross-ref: `claude-mobile-session-docs/ARPG-canonical-kit-research/final-docs-v3/canon-harvest-pipeline-spec-v2.md` §9.19.5.

## Iron laws

- Edition III + every served artifact READ-ONLY · Refit-Candidate-1 READ-ONLY (permanent evidence exhibit) · archipelago-mock artifacts READ-ONLY.
- corpus.db is the ONLY mutation surface. No re-fit, no re-emission, no atlas artifact touch.
- If git commit hits index.lock contention (parallel agents active), wait 5s and retry up to 3×.

## Return contract

≤15 lines: pre-delete counts confirmed (62/120) · provenance-archive + census confirmed in MIGRATION · post-delete grain census numbers · E1-469 integrity assert result · staging law recorded · commit hash. Auto-commit. **NO push** (gandalf verifies then pushes). HALT conditions: count mismatch · any E1-469 member in the delete set · any provenance column you cannot archive (report, don't guess).

**Signed:** gandalf — the word arrived; the carve-out fires once, on the record.
