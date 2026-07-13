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

---

## DELTA v2 (gandalf 2026-07-12, post-mega-probe + post-mapping-pass) — supersedes the above where it touches

Your v1.0 proposal (`research/curated/corpus-db-schema-proposal-2026-07-12.md`) landed well — identity/prefix layer, measured-by-omission, game≠corpus_bucket, reversibility all stand. But it predates two events that change the schema's middle: the **legolas mega-probe** (full-schema facts, ten families per positive) and the **gandalf mapping pass** (every positive now KEYED into the engine frame — the re-key is DONE, not awaited). Amendments:

### D1. Two new inputs (the layers above the CSV)

- **Probe facts:** `agentic_orchestration/legolas/research/megaprobe-2026-07-12/*-facts.jsonl` — 478 positives × ten fact families (`delivery, footprint, control, defense, economy, element, movement, geo_text, rank1_upgrade, sources_used`), each `{facts, conf, prov}`; post-cutoff rows carry conf-cap ≤0.5 + `dossier_owed`. Negatives were SKIPPED (count-only). Plus `mint-dossiers-reexpressed.jsonl` (9 mint kits, all dossier_owed), `roster-lineage-enrichment.jsonl`, `per-game-meta.jsonl`.
- **Engine key:** `agentic_orchestration/gandalf/views/engine-key/corpus-engine-key-v1.jsonl` — 478 rows keyed per kit: `engine_geometry{value, rule_fired, conf}` · `ctrl{treatment, ailments_mapped[], ailment_gaps[]}` · `def{bin, riders[], conf}` · `econ{status, gaps[], meter_type}` · `mob` descriptors · `row_class` (**combat 463 / system-record 15**) · `route` · `flags[]` (all `resolved:*` — zero open judgments) · provenance. Mapping provenance: `views/rekey-map-rules-v1.md` (v1.1) + `views/engine-key/judgment-resolutions-v1.md` + reproducibility scripts in the same dir.

### D2. Schema architecture becomes THREE layers; the six `rekey_<slot>` raw-value tables are RETIRED

Your empty `rekey_<slot>(raw, engine_value, …)` join tables assumed the re-key would map raw suffix values → engine values. It didn't and can't: the key derives from **multi-family probe facts per kit** (delivery × footprint × commitment × verbs → geometry, etc.), resolved per-kit where rules flagged. So:

- **Layer 1 — `canon_corpus`** (your v1.0, stands as designed; suffix `*_raw` stays verbatim provenance).
- **Layer 2 — `canon_probe_facts`** (NEW): one row per kit × family — `{kit_id, family, facts_json, conf, prov, post_cutoff_cap, dossier_owed}`. Facts stay finer than vocabulary — this layer must remain independently queryable (the boards derive from it + Layer 3).
- **Layer 3 — `canon_engine_key`** (NEW, keyed on `kit_id`): the mapping-pass output verbatim (ingest the JSONL; do not re-derive). Same zero-UPDATE discipline you designed — `v_canon_corpus_rekeyed` LEFT-JOINs Layer 3 by kit_id instead of raw-value tables.
- `suffix_rekey_status`: geo/ctrl/def/econ → `'keyed-v1'`; **mob/elem → `'descriptor-final'` — PERMANENT, not awaiting.** By ruled law: element = FREE AXIS (no corpus→engine element mapping EVER; `elem_raw` provenance-only; probe `damage_mode` descriptor feeds ailment-layer design) and mobility = EMERGENT (descriptors only; returns post-emission as battle-sim label). **No `rekey_elem` / `rekey_mob` table may exist** — schema-by-omission, same discipline as your measured law.

### D3. Vocabulary enums of record (Layer 3 CHECKs)

- ctrl treatment: `damage / control / hybrid` — **Q22 RULED: `support` retired**; never a legal value here.
- def bin: `tank / mitigate / evade / absorb / glass` (+ `post-cutoff-deferred`); riders incl. `sustain:leech` — **Q23 RULED 2026-07-12: rider stands, never a sixth bin**; also `trigger:block`, `su-proxy`, `synonym:*`.
- geometry: engine 24-type rich palette; `null` legal ONLY with `resolved:placed-lane` (Walls demand, 3 kits) or `gx-candidate:orbit` (4 kits) or `post-cutoff-deferred`.
- row_class: `combat / system-record`; system-records carry `route` ∈ {loot-economy, progression, modifier-grammar, ailment-synergy, commitment-grammar, difficulty-authoring, meta-currency, consumable-economy}.

### D4. Reconciliation check (add to your validators)

Your CSV-derived `is_system=1` (18 rows) and my judgment-derived `row_class='system-record'` (15 rows) are DIFFERENT classifications from different evidence — expect partial overlap, not identity. Both columns survive; **Layer-3 `row_class` governs combat denominators.** Report the overlap/diff table in the ingest log (any CSV-system row that mapped as combat, and vice versa, is a curation finding, not an error).

### D5. Open-question dispositions (your §4)

- **Q1 (per-slot conf):** for the 478 positives, the probe's per-family conf SUPERSEDES as the live confidence surface (fresh, source-verified, formula-conf retired) — the key consumed it (`min(delivery, footprint)` etc.). Prefix avg-collapsed fallback stands as you designed; recovery of the old jsonl demotes to nice-to-have.
- **Q2 (housing) / Q3 (roster rows) / Q4 (HoT):** escalated to Matt as **Q24** in `canonical/matt_decision_needed/README.md` (your recommendations carried). Note on Q4: probe Unit C empirically CONFIRMED the T3 lean — flag stays until Matt's word, evidence now attached.
- **Q5:** your recommendation stands.

### D6. Acceptance harness (the ingest-verification criterion)

**Every count in `views/engine-key/boards-v1.md` must reproduce from DB queries exactly** — combat denominator 463; ailment-gap census (damage-amp 97 unique kits, freeze 43, stun 36, poison-dot 36); SU mechanics-demand 48 (totem-keyed + J-SUM-resolved); def tank 215; gap censuses (PC/RS/AM/RC/BT/HV); Walls 3; orbit 4. Boards become DERIVED VIEWS the DB regenerates — if a board count can't be reproduced by SQL, the ingest is unfaithful. Negatives (37) ingest Layer-1 only (`negative=1` = warnings, never candidates). Mint kits (9) ingest flagged `mint=1, dossier_owed=1` — they are §F.5(1) candidate-pool members, not corpus positives.

**Gate unchanged:** paper-work now; DB creation + ingest fire only after Matt rules Q24 (housing) + ADR-006 authorization.

**Signed:** gandalf, 2026-07-12 (DELTA v2).

---

## Q24 RULINGS LANDED (Matt 2026-07-12) — GATE LIFTED, EXECUTE

- **(a) Housing: NEW DB** — create `agentic_orchestration/research/curated/corpus.db` (gitignored per existing convention; committed truth = DDL + ingest scripts; clean rebuild must reproduce identical state).
- **(b) Roster/bench 48 mobile rows: SKIP-AND-REPLACE.** Do NOT ingest the 48 `source=roster/bench` CSV rows (mobile self-encodings, retired; git keeps the audit trail). REPLACE with two roster-side ingests, schema yours to design:
  1. `gandalf/views/roster-atlas-rebuilt-v1.csv` → roster table of record (45 rows, engine-sourced).
  2. `legolas/research/megaprobe-2026-07-12/roster-lineage-enrichment.jsonl` → roster↔corpus lineage join (per row: bc6 coordinate + provenance; lineage_targets[] resolved to corpus kit_ids with bc6_distance; nearest_corpus_neighbors[]; neighbor_count_d0/d1/d2; genre_density; whitespace_flag). FK targets must resolve against ingested corpus kit_ids — report any dangling refs as findings.
- **(c) HoT tier: T3 CONFIRMED** — ingest `tier='T3'` with `tier_confirm_pending=0` (clear the flag; ruling cited: Q24(c) + probe Unit C evidence).

Post-ingest asserts amend accordingly: corpus rows ingested = **515** (496 substrate + 18 SYS-annex + 1 unresolved; the 48 roster rows are OUT); roster table = 45; enrichment = 45; engine-key = 478 (combat 463 / system-record 15); probe-facts families present for all 478 positives; negatives (37) Layer-1 only; mint kits flagged; **acceptance harness (D6) mandatory — boards-v1.md counts reproduce from SQL before you call it done.**

**Signed:** gandalf, 2026-07-12 (Q24 rulings folded; brief is FIRE-READY).
