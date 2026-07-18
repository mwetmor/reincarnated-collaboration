# BASIN-5 CRAWL INGEST — MANIFEST (steward → elrond)

**Author:** gandalf (steward) · 2026-07-18 · **For:** elrond (single-writer)
**Op:** the LAST crawl ingest of the VDM-1 run (basin-5 verify/dossier/citations).

---

## Scope

Ingest the basin-5 CRAWL stage into `corpus.db`. **Greenfield 123 kits (c01–c13)** + **le-bomb REPLACE (1 kit)**. NO new `canon_corpus` kit rows — every kit already exists in `canon_corpus`; the crawl adds `verify_ledger` + `kit_dossier` + `kit_citations` rows to existing kits (plus the le-bomb re-key + DELETE-INSERT). Assign the next sequential MIGRATION number. Back up `corpus.db` first (timestamped). Commit **pathspec-only** (script + MIGRATION + errata log; `corpus.db` is gitignored-local). Do NOT push — steward pushes at the boundary.

## Source files (all committed, `agentic_orchestration/research/vdm1/stage1/basin5/`)

- **Greenfield:** `batch-c01..c13-{verify,citations,dossier}.jsonl` — 13 waves, 123 kits → **verify 378 / dossier 738 / citations 254**.
- **REPLACE:** `batch-lebomb-{verify,citations,dossier}.jsonl` — 1 kit → verify 4 / dossier 6 / citations 6.
- **Pre-ingest guard:** assert every file `kit_id` resolves to an existing `canon_corpus` row. Steward already verified roster-complete + zero-phantoms per game (tq 21 · chr 16 · ud 12 · tl2 11 · tli 9 · tl1 2 · vs 23 · hot 17 · hades1 7 · mcd 5) — re-assert as a hard guard before writing.

---

## TIER 1 — LOAD-BEARING (gating)

### 1a. Greenfield ingest
INSERT c01–c13 → `verify_ledger` (verify), `kit_dossier` (dossier), `kit_citations` (citations). Schema per basin-2/3/4 pattern.

### 1b. N1 — c01 CHECK-violation normalization (HARD BLOCKER — ingest fails without this)
`c01` tq-a: all **17 abstained dossier rows** carry `payload_json={"abstain_reason":"…"}` instead of `null` → violates `CHECK(abstained=0 OR payload_json IS NULL)`. Normalize at ingest: **SET `payload_json=NULL`** on those 17 rows (lift `abstain_reason` text into a notes field, or drop it). `c02–c13` are all clean (strict null-payload on abstained rows) — isolated to c01's crawler.

### 1c. N2 — c05 placeholder citation
`c05` `ud-snowstorm-frost` carries an all-null placeholder citation (url/cite_class/rank_class all null, `quarantined=0`). Set `quarantined=1` or drop the row. (Ties to the ud-snowstorm-frost-fully-unattested erratum, §2a.)

### 1d. le-bomb REPLACE + RE-KEY
- **DELETE** the existing basin-2 `le-bomb-lance-falconer` rows: 3 `verify_ledger` + 6 `kit_dossier` (all abstained/null from basin-2) + any basin-2 le-bomb `kit_citations`.
- **INSERT** the re-crawl: 4 verify + 6 dossier + 6 citations (from `batch-lebomb-*.jsonl`).
- **RE-KEY `canon_corpus`** — **`kit_id` `le-bomb-lance-falconer` STAYS as opaque PK (do NOT churn the PK)**; correct the DISPLAY fields only:
  - `folk_name` → **"Explosive Ballista Falconer"**
  - `core_skills` → **["Explosive Trap","Ballista","Falconry","Dive Bomb"]**
  - `era_raw` → **"1.0 launch (Feb 27 2024); attested through Season 4 (1.4-omens, 2026)"**
  - `mech_note` → drop the false "Bomb Lance / thrown-explosive" identity (real identity: Rogue→Falconer; Explosive Trap [0-mana] procs explosive Ballista turrets + Dive Bomb burst + Falcon companion)
  - `elem_raw` → **leave for the mapper** (dossier prose carries cold [Apogee of Frozen Light] + fire [Explosive Trap "inflicting fire damage"]; NAME-ONLY adjudication happens at map stage — shape-not-number law, do NOT pre-assert)
- **Note for the mapper (record in MIGRATION):** the 6 re-crawl dossier rows carry `{"note":"IDENTITY_MISMATCH…"}` wrappers whose prose holds the REAL mechanical facts (rotation/geometry/uniques/variants) — legal (abstained=0 + dict payload), mappable after this re-key. `IDENTITY_MISMATCH` is now RESOLVED by the re-key; the wrappers are historical.

---

## TIER 2 — HYGIENE (non-gating; apply in same pass — mapping reads the DOSSIER not `elem_raw`, shape-not-number law)

### 2a. elem_raw / mech_note corrections (existing `canon_corpus` rows)
| kit | correction |
|---|---|
| prismatic-embermage (tl2) | elem_raw `fire` → `fire/ice/lightning` (tri-element) |
| hailstorm-embermage (tl2) | elem_raw `cold` → `ice` (+ ice/electric vuln-debuff, dossier carries) |
| ud-toxic-flame | "poison+fire dual" → **poison-only** |
| tq-liche-king | "player transform" → **summoned-pet** |
| ud-lightning-vortex | "ranged cast" → **melee** (swings weapon) |
| tq-distortion | "control-centric" → **physical+vitality damage** |
| chr-bloodbinder | "HP self-sacrifice" → **mana-stacking** |
| tq-squall | lightning (probe-inference) → **element-silent** (no lightning damage-type in anchor) |
| chr-turret-drone | "Holy Lance Turrets" = skill-name → **element-silent** |
| hot-warlock | elem_raw "dark/arcane" → **not-attested** (summoner/magic → no-engine-family, silent) |
| hot-cleric-radiant | "magic" → **no-engine-family** (silent) |
| hot-spirit-warrior | "magic" → **no-engine-family** (silent); also = cross-class ability, not a class |
| ud-snowstorm-frost | **fully-unattested** (ties to N2) |

### 2b. era / identity / scope corrections
- **vs-out-of-bounds-freeze:** era → arcana Patch 0.6.1 (May 2022); scope → 14 weapons (not 3)
- **vs-queen-sigma:** era → Patch 0.11.0 (Aug 2022); base predates DLC label
- **vs-big-trouser + vs-fuwalafuwaloo:** DLC → base game
- **vs-vlad-dracula:** starting weapon → Wine Glass (DB generic)
- **hot-sage:** era → added Feb-2024, active in 1.0-2024 (widen the over-narrow window)
- **hades1-guan-yu:** lifesteal is on **Spin Attack** (corpus said Special)
- **hades1-beowulf:** bloodstones never lodge / fire alongside bull rush; Igneus-Eden wrong-weapon correction

---

## TIER 3 — PROMOTION
Promote verified facts to `verified-v1.1` per the basin-2/3 pattern (N kits × 10 facts). Report the promotion census (kits promoted × facts).

---

## STEWARD GATE (on return — steward runs, advisory NEVER trusted)
D-2c INGEST battery (readonly): DB≡files row-level match on all 124 kits · N1 applied (0 CHECK violations) · N2 quarantined · le-bomb REPLACE clean (old basin-2 rows gone, 16 new rows in, re-key landed on all 4 display fields) · TIER-2 errata applied · promotion census correct · citations quarantine correct. Steward recounts from committed files + DB; grades/counts governed by file-truth.

---

**Signed:** gandalf (steward) · basin-5 crawl INGEST manifest · greenfield 123 + REPLACE 1 + N1/N2 + 13 elem/mech errata + 7 era/identity errata + promotion.
