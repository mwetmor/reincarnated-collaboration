# Corpus FOLD 1+2 Log — 2026-07-13

**Author:** elrond
**Date:** 2026-07-13
**Authority:** gandalf returns-adjudication (`agentic_orchestration/gandalf/notes/2026-07-13-returns-adjudication-elrond-s1-legolas-mint.md`)
**Source of record:** legolas 9-mint-dossier series, commit `aaa519d6` (`agentic_orchestration/legolas/findings/mint-dossiers-paste-ready-2026-07-13/`)
**Script:** `agentic_orchestration/research/scripts/corpus_fold12_2026_07_13.py`
**DB:** `agentic_orchestration/research/curated/corpus.db` (gitignored, schema_meta 2.1 → 2.2)
**MIGRATION entry:** v2.2

---

## 0. One-line intent

Two folds carried in ONE idempotent pass. **FOLD 1** applies gandalf-ratified data corrections; **FOLD 2** keys the 9 mint kits into `canon_engine_key` so they become plottable on the V1.2 atlas plane (before this pass, all 9 had zero Layer-3 rows → invisible). Every geometry/movement value traces to dossier mechanical text — **curation from source of record, never invention.** Corpus row-count unchanged (524); the canon combat denominator (463, `mint=0`) is preserved.

## 1. D6 rebuild sequence (now three committed scripts)

```
python3 agentic_orchestration/research/scripts/corpus_ingest_2026_07_12.py        # base three-layer ingest
python3 agentic_orchestration/research/scripts/corpus_completion_s1_2026_07_13.py  # S1 completion (idempotent)
python3 agentic_orchestration/research/scripts/corpus_fold12_2026_07_13.py         # this fold (idempotent)
```

All deterministic. Clean rebuild from scratch verified: base → S1 → fold12 passes all 12 gates. The fold is idempotent (`ADD COLUMN` pragma-guarded; UPDATEs pure; engine_key inserts `INSERT OR REPLACE` scoped to the 9 mint kit_ids). corpus.db stays gitignored; the three scripts + the two logs + the MIGRATION entries are the committed truth.

## 2. FOLD 1 — data corrections

### 1a — `poe1-ring-of-shields` → `le-ring-of-shields`
Game-attribution error, 2-source confirmed (lastepoch.fandom.com + lastepochtools.com): Ring of Shields is a **Last Epoch Sentinel → Forge Guard summon skill, NOT a PoE1 skill.**
- `kit_id` corrected `poe1-ring-of-shields` → `le-ring-of-shields`; `game` poe1 → le.
- Cascaded across canon_corpus / canon_probe_facts (0 rows) / canon_engine_key (keyed as le in FOLD 2).
- **era_year corrected 2013 → 2024.** The rename moved `game` to `le`, but era_year retained the stale poe1 game-level (2013). Corrected to the le game-level (2024) — which also matches the dossier's skill-debut year. This is a consistency correction (era_year must track the kit's game), not the semantic override discussed in §4.
- **Consequence (per gandalf ruling):** the poe1 totem-hole now rests solely on `poe1-totem-hierophant`; LE proxy/summon coverage strengthens (Falconer + Shift Bladedancer + Ring of Shields).

### 1b — CotA vs IK-HotA: RULED DISTINCT, no dedup
Both `d3-call-of-the-ancients` and `d3-ik-hota` verified present (script asserts cota=1, hota=1). CotA = summon-3-ancients (proxy economy, Wave-A relevant); IK-HotA = melee slam. Shared Immortal King set is **not** a dedup trigger — different skill, delivery, and plane address. No action beyond verification.

### 1c — `d2-sacrifice` negative-canon
`negative=1` set. Joins the negative-canon family (37 → 38). Founding self-cost melee archetype; never meta-viable; GX-06 evidential value. **KEEP, not delete** — excluded from S6 certification population, present in the catalogue as a historical-exhibit.

### 1d — 9-dossier ingest
Two new columns on `canon_corpus`: `skill_debut_year` (INTEGER), `source_urls` (TEXT, JSON array). Per-kit backfill:

| # | kit_id | stabilization_patch | skill_debut_year | source_urls |
|---|---|---|---|---|
| 01 | poe1-totem-hierophant | 2.3.0 | 2016 | 4 |
| 02 | d3-call-of-the-ancients | 2.6.1 | 2017 | 3 |
| 03 | le-ring-of-shields | 1.0 | 2024 | 4 |
| 04 | poe1-blood-magic-kit | 2.0.0 | 2015 | 3 |
| 05 | d2-teleport-sorc | 1.10 | 2003 | 4 |
| 06 | d3-dashing-strike-monk | 2.4.2 | 2016 | 2 |
| 07 | le-shift-bladedancer | 1.0 | 2024 | 3 |
| 08 | poe1-vaal-blade-vortex | **NULL** | 2016 | 4 |
| 09 | d2-sacrifice | **NULL** | 2001 | 4 |

- `stabilization_patch` **7/9** filled; VBV + Sacrifice honest-NULL (introduction patch unconfirmed at source — PoE-wiki 403 for VBV; D2 v1.00 launch skill ambiguous for Sacrifice).
- `dossier_owed` cleared 9/9 (dossier debt discharged).
- Patch tokens stored **bare** (`2.6.1`, not `v2.6.1`) — see §4.

## 3. FOLD 2 — plane-keying (9 canon_engine_key rows)

Each geometry value traced to the dossier's mechanical description (`geo_descriptor` + `mob_descriptor` recorded in each row's `provenance_json`).

### Keyed cleanly as combat-kit (7)

| kit_id | geometry_value | mob_policy | plane cell | dossier trace |
|---|---|---|---|---|
| poe1-totem-hierophant | `totem` | full-move | FREE-MOVE×SUMMON | "at-target totem placement; totems persist" |
| d3-call-of-the-ancients | `totem` | full-move | FREE-MOVE×SUMMON | "at-target summon; 3 ancestors roam a large zone" |
| le-ring-of-shields | NULL + `gx-candidate:orbit` | full-move | ORBITAL\* | "shields form a rotating ring, follows player" |
| d3-dashing-strike-monk | `dash_attack` | full-move | FREE-MOVE×MELEE | "player body as projectile, carves a lane" |
| le-shift-bladedancer | `dash_attack` | full-move | FREE-MOVE×MELEE | "self-origin lane dash; blade trails persist" |
| poe1-vaal-blade-vortex | NULL + `gx-candidate:orbit` | full-move | ORBITAL\* | "self-origin homing-vortex cloud; semi-proxy orbit" |
| d2-sacrifice | `melee_strike` | walk | WALK×MELEE (neg=1) | "at-target single-hit melee strike; single-target" |

`mob_skill_is_movement=1` set for the two dash kits + teleport-sorc (movement IS the delivery); 0 elsewhere.

### Off-plane by design — system-record (2)

| kit_id | route | why unplottable |
|---|---|---|
| poe1-blood-magic-kit | `resource-economy` | NOT a delivery skill — life-as-resource keystone/economy grammar (per gandalf ruling). No geometry to force. |
| d2-teleport-sorc | `mobility-grammar` | NOT a damage-delivery skill — movement identity; Teleport IS the verb, damage comes from other skills (per gandalf ruling). |

These are `row_class='system-record'` with geometry NULL — an **explicit non-combat classification** (mirrors the 15 existing system-records like di-essence-transfer / hades2-omega-magick), not an unprocessed hole. The renderer filters `row_class='combat-kit'`, so they correctly do not plot.

\* **Orbit kits (le-ring-of-shields, poe1-vaal-blade-vortex):** keyed legally per the DDL law ("geometry NULL legal ONLY with resolved:placed-lane / gx-candidate:orbit / post-cutoff-deferred"). They render **UNMAPPED** until gandalf adds them to the renderer's `UNMAPPED_COL` hardcode → `"ORBITAL"` (see §5).

## 4. Steward decisions surfaced (flagged to gandalf for ratification)

1. **era_year NOT overridden with dossier skill-debut years.** FOLD 1d's header names "era_year," but its parenthetical notes P5 already filled era_year corpus-wide as per-GAME release year. The dossiers carry a per-SKILL debut year that differs (CotA 2017 vs d3-2012; Sacrifice 2001 vs d2-2000; totem-hierophant 2016 vs poe1-2013; blood-magic 2015; teleport-sorc 2003). Writing those into `era_year` would mix two semantics in one column and corrupt temporal ordering for 9 rows while 515 stay game-level. **Decision:** keep `era_year` at P5 game-level (consistent column semantics); capture the dossier signal in the new `skill_debut_year` column. Both signals preserved. The le-ring-of-shields 2013→2024 change is a separate correction (era_year must track the post-rename `game=le` level), not this override. Precedent: Finding-4 spirit (prefer the specific canonical signal) is honored — the specific signal is captured, just in a semantically-correct column.
2. **patch tokens stored bare** (no leading `v`). The renderer's `build_public_label()` prepends `v` (`f" (v{patch})"`); a stored `v2.6.1` renders `vv2.6.1`. Bare storage (`2.6.1`) matches the render convention and yields `(v2.6.1)`.

## 5. Render-spec FLAGS to gandalf (follow-ups; NOT elrond's to change)

- **Orbital mint kits need `UNMAPPED_COL` entries.** Add `le-ring-of-shields` + `poe1-vaal-blade-vortex` → `"ORBITAL"` in `render_v1_2_stratified.py` `UNMAPPED_COL`, mirroring `poe1-poison-bv`. Until then they render UNMAPPED (delivery=None). The data is correct; only the render override is missing.
- **d2-sacrifice dual state.** It is now the first kit that is BOTH `negative=1` AND combat-keyed. It plots as an on-plane mint ★ dot (WALK×MELEE) and also appears in the negative-overlay annotation. The data is correct (its melee delivery IS determinable AND it is negative-canon). **Render precedence** — exclude negatives from the combat JOIN, or accept the dual representation as an intentional negative-exhibit-with-geometry — is gandalf's call.

## 6. Verification (all 12 gates passed; clean-rebuild-from-scratch confirmed)

| Gate | Result |
|---|---|
| corpus rows unchanged | 524 ✓ |
| engine_key 478 → 487 (+9) | 487 ✓ |
| combat-kit 463 → 470 (+7) | 470 ✓ |
| system-record 15 → 17 (+2) | 17 ✓ |
| **CANON combat (mint=0) preserved** | **463 ✓** |
| negative 37 → 38 (+1) | 38 ✓ |
| all 9 mint kits keyed | 9 ✓ |
| ring OLD id gone | 0 ✓ |
| ring NEW game=le | le ✓ |
| dossier_owed cleared | 0 ✓ |
| cone Path-2 BEAM untouched | 5 ✓ |
| cone Path-2 PROJECTILE untouched | 6 ✓ |

**V1.2 render reproduces** (`render_v1_2_stratified.py`, exit 0; 470 combat / 38 negative / 45 roster; 515 dots). 5 non-orbit combat mint kits place on-plane as ★; 2 orbit UNMAPPED (expected, §5); 2 system-records correctly absent.

## 7. Reversibility

corpus.db is gitignored. Clean rebuild = base ingest + S1 completion + this fold, all from committed inputs (v3 CSV + engine-key/probe/roster/lineage JSONL + per-game-meta.jsonl + the 9 committed dossiers + URL manifest). Raw columns untouched; all new columns/rows derived at fold time. Output is byte-identical SQLite state (verified via full three-script rebuild-from-scratch).
