# ELROND BRIEF — corpus ingest under the engine-frame schema (draft now · execute after Matt's housing ruling)

> **PASTE INTO EXACTLY ONE SESSION** (fresh elrond session). Authored by gandalf 2026-07-12 under Matt's usage-offload directive; knight-rider sequences if this collides with other elrond work.
>
> **Gate:** schema design + MIGRATION proposal are ungated paper-work — do them now. **Actual DB ingest fires only after Matt's corpus-housing D-ruling** (still open) and standard authorization (ADR-006).

## Mission

Design the catalogue-DB representation of the mobile ARPG canon corpus under the **engine-frame schema of record**: `agentic_orchestration/gandalf/views/corpus-rekey-spec-v1.md` — read §1–§3 first; the §2 fate table IS the schema authority.

## Inputs

- `claude-mobile-session-docs/ARPG-canonical-kit-research/final-docs-v3/rdr-kit-atlas-v3.csv` — 563 rows; **canon rows are the substrate of record**; the 35 roster + 13 bench mobile rows are provenance-only lineage (Matt throw-out ruling 2026-07-12), ingest them flagged as such or skip
- `agentic_orchestration/gandalf/views/roster-atlas-rebuilt-v1.csv` — the roster of record (45 rows, rebuilt from engine sources)
- `final-docs-v3/rdr-kit-atlas-generator.py` — the mobile code vocabularies (needed to decode raw suffix values)
- `final-docs-v3/canon-harvest-pipeline-spec-v2.md` — harvest provenance rules

## Schema shape (per the fate table)

- **Prefix = typed engine-lattice columns:** attr/range/tempo/amp/proxy/commitment as enums + **per-slot confidence** ({value, confidence}) + provenance tag `mobile-harvest-v3`. Commitment enum: instant / wind-up / channel.
- **Suffix = raw descriptor columns** (`mob_raw`, `geo_raw`, `ctrl_raw`, `def_raw`, `econ_raw`, `elem_raw`) flagged `awaiting-rekey` — do NOT invent mappings; six design sessions will supply the mapping tables later (design your schema so mapping tables can join in without rewriting rows).
- **Identity columns:** game · tier · era strings · negative flag · lineage · gx · folk_name · original atlas_key (preserved verbatim as provenance).
- **HoT ruling:** Halls of Torment is its OWN game (Matt 2026-07-12); tier lean T3 (gandalf lean — flag for Matt confirm at ingest).
- **Measured-vs-projected law in schema:** corpus rows can NEVER carry measured/fingerprint values; measured columns exist only for gauntlet-run kits.
- Raw harvest artifacts immutable; game identity + all curation assigned in DB.

## Deliverables

1. Schema proposal + `MIGRATION.md` entry per ADR-004 conventions (your seam's format)
2. Staged ingest plan (dry-run counts, row-level validation, rollback)
3. Open-questions list for Matt/KR (housing location, HoT tier confirm, roster-provenance rows in-or-out)

Auto-commit the proposal docs per CLAUDE.md discipline (no push; no production-DB writes). Final message: ≤200-word summary + paths.
