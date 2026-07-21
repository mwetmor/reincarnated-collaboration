# Glance per-kit "single source of truth" page — build spec

> **STATUS:** SPEC · MATT-APPROVED 2026-07-20 (sample shape approved) · routes to **elrond** (join generator) + **drax** (glance render). Author: gandalf. Seed artifacts: `2026-07-20-glance-per-kit-sample.py` + `.json` (this folder).

## Purpose

A per-kit detail page on **glance** showing the **joined single source of truth** for one kit — every associated row across `corpus.db`, on one URL. This is the human-readable drill-down of the D-11 `kit_master` one-representation consolidation.

## Architecture (mirrors the existing `/atlas` route — do NOT deviate)

Glance's founding law: **derived, never authored; no DB / no server / no LLM in the live truth path.** `/atlas` already surfaces DB-derived content the compliant way: a **build-time generator reads `corpus.db` → emits a static asset → committed/staged → served statically.** The DB is read at *generate-time only*, never queried from the browser.

The per-kit page is the **same pattern, one more surface**:

```
corpus.db  ──(build-time generator, elrond)──►  public/kits/index.json + public/kits/<kit_id>.json
                                                          │
                                          (static assets, git-provenance stamped)
                                                          ▼
                              glance SPA route /kits (index) + /kit/:id (detail)  ──(drax)──►  rendered
```

## The interface contract — FROZEN

**The approved sample JSON (`2026-07-20-glance-per-kit-sample.json`) is the frozen interface contract.** Elrond emits *exactly* this shape at scale; drax renders *exactly* this shape. Any field change requires a re-sync between both owners before it lands. The 10 sections per kit:

| section | source table | notes |
|---|---|---|
| `spine` | `kit_master` VIEW | 25-field header: folk_name, game, tier, grade, terminal_state, eras, elements/ailments attested (as arrays), verify tallies |
| `mapping` | `kit_mapping` | grade + parsed `mapping_json` (skills[], coords, T4 doors) |
| `mints_anchored[]` | `mint_ledger` | mints this kit forced (may be `[]` — render empty, not error) |
| `dockets[]` | `mechanic_gap_docket` | gaps citing this kit as evidence |
| `atlas_group` | `atlas_gateA_labels_*` | plane group + rationale (may be `null`) |
| `lineage_enrichment` | `roster_lineage_enrichment` | `null` for corpus kits not yet placed in `roster_atlas` — expected, render empty |
| `citations[]` | `kit_citations` | every source row incl. `quarantined` flag; render quarantined visually distinct |
| `verify_ledger[]` | `verify_ledger` | per-claim CONFIRMED/CONTRADICTED/UNSUPPORTED + anchor_quote |
| `dossier{}` | `kit_dossier` | grouped by 6 families; parsed payloads; `abstained` rows render as "source silent" |
| `_row_counts` | (computed) | density summary for the index/badges |

## Elrond deliverable (corpus → JSON generator)

1. Productionize the seed script (`2026-07-20-glance-per-kit-sample.py`) to emit **all 574 kits**: one `index.json` (kit_id, folk_name, game, tier, grade, `_row_counts` for the browse/filter list) + one `<kit_id>.json` per kit (full object).
2. Build-time, deterministic, read-only. **No LLM, no network, no judgment** — pure projection (respects glance's truth-path law).
3. Emit a **git-provenance stamp** (corpus.db commit/hash + generate date) alongside, same as `/atlas`'s `plane-provenance.json`.
4. Size budget: sample is ~11 KB/kit → ~6 MB total. Per-kit files lazy-loaded; index stays small. If any kit is pathologically large, note it — don't silently truncate.
5. **Honest rendering of gaps is a feature, not a bug.** Empty `mints_anchored`, `null lineage`, `abstained` dossier rows, empty `elements_attested` — all pass through as-is. This page is *also a diagnostic* for the mechanical-sparseness gap (see companion recognition note); do not paper over sparse kits.

## Drax deliverable (glance render routes)

1. Add `/kits` (browsable/filterable index off `index.json` — filter by game/tier/grade; show `_row_counts` density) + `/kit/:id` (full detail render of `<kit_id>.json`).
2. Match the existing `/atlas` static-asset staging pattern (`stage-assets.mjs` → `public/`). Do NOT introduce a live DB call, a server, or an API — static assets only.
3. Render every section; **empty/null sections render gracefully** (the unlinked/unplaced states are common and meaningful, not errors).
4. Quarantined citations + abstained dossier rows render **visually flagged** (they're recorded-but-not-authoritative).

## Constraints (both)

- **No push / no deploy without Matt's explicit go.** Build, self-review, report back what you built for Matt's review. (Push is Matt-authorized per team discipline.)
- Coordinate on the **frozen JSON shape** as the interface; it's the contract that lets you work in parallel.
- Report back: elrond → generator + sample full-corpus output stats; drax → route + a local screenshot/description of the rendered page.

## Sequencing note (not part of this build)

This page is **diagnostic**: rendering per-kit truth makes the *mechanical-axis sparseness* (many kits thin on mechanics) and the *T4/capstone extraction confusion* visible per kit. That motivates a **separate VDM-2 substrate-schema track** (companion note: `2026-07-20-mechanical-axis-sparseness-and-t4-ontology-recognition.md`). Render first (diagnostic); schema-complete second. Do not bundle the schema work into this build.
