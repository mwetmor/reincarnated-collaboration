# VDM-1 D-5 Backfill Summary — capstone_alterations + item_alterations
**Date:** 2026-07-18
**Mode:** B (catalogue backfill)
**Source:** poedb.tw (primary); fallback poedb WebSearch for 404 item pages
**Crawl approach:** skill-batched (not kit-batched) — fetched per core skill, fanned results to kits sharing that skill

---

## Coverage delta

### family: capstone_alterations
Target: 58 abstained kits
Filled: 55
Still silent: 3

Still-silent kits (capstone_alterations):
- poe1-sweep — poedb page contains no transfig/alt-quality/threshold data
- poe1-icicle-mines — transfig names listed (Icicle Mine of Fanning, Icicle Mine of Sabotage); no mechanic diff text extracted
- poe1-seismic-trap — Seismic Trap of Swells listed; no mechanic diff text extracted

Partial-confidence kits (capstone_alterations, filled but anchor_quote=null on some entries):
- poe1-edc (Essence Drain) — transfig names listed; no mechanic diff text
- poe1-lightning-conduit — Lightning Conduit of the Heavens listed; no mechanic diff text
- poe1-soulrend — Soulrend of Reaping/Spiral listed; no mechanic diff text
- poe1-storm-brand — Storm Brand of Indecision listed; no mechanic diff text
- poe1-tornado-shot — Tornado Shot of Cloudburst listed; no mechanic diff text
- poe1-vaal-blade-vortex — filled with Vaal vs base mechanic differences; no dedicated endgame alt-quality

### family: item_alterations
Target: 36 abstained kits (overlap with capstone list)
Filled: 30
Still silent: 6

Still-silent kits (item_alterations):
- poe1-edc — poedb silent on key-unique item lines for Essence Drain
- poe1-icicle-mines — poedb silent on item-altering lines
- poe1-lightning-conduit — poedb silent on skill-altering item lines
- poe1-seismic-trap — poedb silent beyond variant name
- poe1-soulrend — poedb silent on item-altering lines
- poe1-storm-brand — poedb silent beyond Storm Brand of Indecision name

---

## ERRATA-14 and ERRATA-15 anchors

**ERRATA-14 (Tectonic Slam introduced 3.2.0):** FOUND
- Source: https://poedb.tw/us/Tectonic_Slam
- Verbatim: "Added a new Strength Skill Gem - Tectonic Slam in patch 3.2.0 (Bestiary league)"
- Captured in dossier kit poe1-tectonic-slam, family capstone_alterations, errata field

**ERRATA-15 (Toxic Rain introduced 3.4.0):** FOUND
- Source: https://poedb.tw/us/Toxic_Rain
- Verbatim: "Added a new Dexterity Skill Gem - Toxic Rain in version 3.4.0"
- Captured in dossier kit poe1-toxic-rain, family capstone_alterations, errata field

Both citations in backfill-capstone-items-citations.jsonl.

---

## Access anomalies / red flags

- poedb.tw direct item pages for Mjolner, Death's Oath (primary path), The Poet's Pen, Writhing Jar returned HTTP 404 — poedb URL scheme for unique items differs from skill gem pages. Mjolner trigger text sourced via WebSearch result snippet (poedb.tw/unique.php?n=Mjölner); Poet's Pen sourced via The_Poets_Pen (no apostrophe) which succeeded; Death's Oath sourced via Death_Aura skill page (item trigger line confirmed there); Writhing Jar worm text sourced from WebSearch result snippet.
- NO fabrication: where poedb page was silent or 404 and no fallback found, kit remains abstained or partial with explicit notes.
- Elrond fill-only guard: all rows carry abstained=0 only where anchor evidence was retrieved. Partial entries carry conf="partial-poedb" with notes field. Still-silent entries carry abstained=1.

---

## Output files

- `backfill-capstone-items-dossier.jsonl` — 94 rows (58 capstone + 36 item families; some kits appear in both families)
- `backfill-capstone-items-citations.jsonl` — 66 citation rows (per poedb page fetched)
- `backfill-capstone-items-summary.md` — this file

---

## STEWARD AUDIT + REPAIR ADDENDUM (gandalf, 2026-07-18)

**Verdict: ACCEPTED after mechanical schema repair.** Content quality good (ERRATA-14/15 anchors verbatim-recovered; 86/94 rows filled); two schema deviations repaired steward-side (b07 line-2 precedent — deterministic repairs, no judgment substitution):

1. **Abstained rows (8):** carried `payload_json: {}` + `conf: "still-silent"` → repaired to strictly-null per NO-FABRICATION LAW. File-truth abstained set: capstone ×1 (sweep) · item ×7 (edc, icicle-mines, lightning-conduit, seismic-trap, soulrend, storm-brand, sweep). Reason (from agent return): poedb renders variant names only / no item-alteration text for these — structural page limit, not crawl failure. *(Self-report said 3 capstone + 6 item still-silent — file truth 1+7; D-2c advisory-histogram law vindicated again.)*
2. **conf-as-provenance-tag (86 non-abstained rows):** string tiers → deterministic float map, originals in git (`136c7140`): `verified-poedb`→**0.9** (×78, direct page verbatim) · `verified-poedb-search`→**0.75** (×1, mjolner — WebSearch snippet recovery, one hop weaker) · `partial-poedb`→**0.5** (×7, variant names captured but zero mechanic-diff text: edc, icicle-mines, lightning-conduit, seismic-trap, soulrend, storm-brand, tornado-shot — all capstone_alterations).
3. **Self-report vs file truth on partials:** agent named VBV partial; file truth has VBV at 0.9 and icicle-mines/seismic-trap at 0.5.

**Ingest-7 law (elrond):** FILL-ONLY merge — insert/replace `kit_dossier` rows ONLY where the existing stage-1 row is abstained (or absent); NEVER overwrite a non-abstained stage-1 row (stage-1 guide-tier fills are primary; this sweep is enrichment). Expected fill ceiling: ≤57 capstone + ≤29 item rows flip abstained→filled (poe1-incinerate item row exists here but stage-1 may already carry it — elrond's merge counts are file truth). 404-pattern note for future poedb item work: item pages do NOT follow `/us/<Name>` gem scheme (mjolner/deaths-oath/poets-pen/writhing-jar 404'd; underscore-only URL worked for poets-pen).

**Brief-amendment candidate (basin templates, non-retro):** dossier `conf` is NUMERIC 0.0-1.0; provenance vocabulary belongs in the summary, never the conf column.
