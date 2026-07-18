# VDM-1 Stage 0 — Census Reconciliation

**Date:** 2026-07-18
**Author:** legolas (Mode A, Stage 0b — local work only)
**DB authority:** `agentic_orchestration/research/curated/corpus.db` (elrond single-writer; read-only here)
**JSONL source root:** `claude-mobile-session-docs/ARPG-canonical-kit-research/`
**Total DB rows:** 585 · DB game codes enumerated: chronicon, d2, d3, d4, di, gd, hades1, hades2, hot, la, le, mcd, poe1, poe2, tl1, tl2, tli, tq, tq2, undecember, vs

---

## Method

Per-basin diff: kit_ids extracted from per-game JSONL files vs kit_ids in `canon_corpus` per DB game code. Combined-JSONL basins (Hades = hades1+hades2 in one file; Torchlight = tl1+tl2+tli in one file; TQ = tq+tq2 in one file) are compared against the union of their DB sub-codes. The DB is authority; JSONL is the mobile-harvest input. Direction of diff is named explicitly: IN-JSONL-NOT-DB (JSONL excess) and IN-DB-NOT-JSONL (DB additions post-harvest).

---

## Per-Basin Tables

### chronicon
| Metric | Count |
|---|---|
| JSONL records | 17 |
| DB records (game=chronicon) | 17 |
| Exact ID match | 17 |
| IN-JSONL-NOT-DB | 0 |
| IN-DB-NOT-JSONL | 0 |

**CLEAN.**

---

### d2 (Diablo II / D2R)
| Metric | Count |
|---|---|
| JSONL records | 58 |
| DB records (game=d2) | 60 |
| Exact ID match | 58 |
| IN-JSONL-NOT-DB | 0 |
| IN-DB-NOT-JSONL | 2 |

**IN-DB-NOT-JSONL:**
- `d2-sacrifice` (Sacrifice Paladin)
- `d2-teleport-sorc` (Teleport Sorceress)

**Note:** Both are late additions to the DB post-mobile-harvest. No id-mismatch suspects identified; all 58 shared IDs match exactly.

---

### d3 (Diablo III)
| Metric | Count |
|---|---|
| JSONL records | 46 |
| DB records (game=d3) | 49 |
| Exact ID match | 46 |
| IN-JSONL-NOT-DB | 0 |
| IN-DB-NOT-JSONL | 3 |

**IN-DB-NOT-JSONL:**
- `d3-call-of-the-ancients` (Call of the Ancients Barbarian)
- `d3-dashing-strike-monk` (Dashing Strike Monk)
- `d3-wizard-black-hole` (Wizard — Black Hole)

**Note:** Three DB-only records; no JSONL excess; no id-mismatch suspects.

---

### d4 (Diablo IV)
| Metric | Count |
|---|---|
| JSONL records | 45 |
| DB records (game=d4) | 46 |
| Exact ID match | 45 |
| IN-JSONL-NOT-DB | 0 |
| IN-DB-NOT-JSONL | 1 |

**IN-DB-NOT-JSONL:**
- `d4-spiritborn-vortex` (Spiritborn — Vortex)

---

### di (Diablo Immortal)
| Metric | Count |
|---|---|
| JSONL records | 23 |
| DB records (game=di) | 24 |
| Exact ID match | 23 |
| IN-JSONL-NOT-DB | 0 |
| IN-DB-NOT-JSONL | 1 |

**IN-DB-NOT-JSONL:**
- `di-cyclone-strike-monk-base` (DI Monk — Cyclone Strike base)

---

### gd (Grim Dawn)
| Metric | Count |
|---|---|
| JSONL records | 41 |
| DB records (game=gd) | 41 |
| Exact ID match | 41 |
| IN-JSONL-NOT-DB | 0 |
| IN-DB-NOT-JSONL | 0 |

**CLEAN.**

---

### hades (hades1 + hades2 combined JSONL vs hades1+hades2 DB)
| Metric | Count |
|---|---|
| JSONL records | 13 (8 hades1 + 5 hades2) |
| DB records (hades1=8, hades2=5) | 13 |
| Exact ID match | 13 |
| IN-JSONL-NOT-DB | 0 |
| IN-DB-NOT-JSONL | 0 |

**CLEAN.**

---

### hot (Halls of Torment)
| Metric | Count |
|---|---|
| JSONL records | 19 |
| DB records (game=hot) | 19 |
| Exact ID match | 19 |
| IN-JSONL-NOT-DB | 0 |
| IN-DB-NOT-JSONL | 0 |

**CLEAN.**

---

### la (Lost Ark)
| Metric | Count |
|---|---|
| JSONL records | 53 |
| DB records (game=la) | 53 |
| Exact ID match | 53 |
| IN-JSONL-NOT-DB | 0 |
| IN-DB-NOT-JSONL | 0 |

**CLEAN.**

---

### le (Last Epoch)
| Metric | Count |
|---|---|
| JSONL records | 35 |
| DB records (game=le) | 35 |
| Exact ID match | 35 |
| IN-JSONL-NOT-DB | 0 |
| IN-DB-NOT-JSONL | 0 |

**CLEAN.**

---

### mcd (Marvel Contest of Champions / MCD)
| Metric | Count |
|---|---|
| JSONL records | 5 |
| DB records (game=mcd) | 5 |
| Exact ID match | 5 |
| IN-JSONL-NOT-DB | 0 |
| IN-DB-NOT-JSONL | 0 |

**CLEAN.**

---

### poe1 (Path of Exile 1) — PRIMARY BASIN FOR VDM-1
| Metric | Count |
|---|---|
| JSONL records | 91 |
| DB records (game=poe1) | 94 |
| Exact ID match | 91 |
| IN-JSONL-NOT-DB | 0 |
| IN-DB-NOT-JSONL | 3 |

**IN-DB-NOT-JSONL:**
- `poe1-blood-magic-kit` (Blood Magic Life-as-Resource) — system/mechanic record; has source_urls in DB; negative=0; mobile_blocking_mechanics=NULL
- `poe1-totem-hierophant` (Totem Hierophant) — has source_urls in DB; negative=0; mobile_blocking_mechanics=NULL (blank)
- `poe1-vaal-blade-vortex` (Vaal Blade Vortex) — has source_urls in DB; negative=0; mobile_blocking_mechanics=NULL

**Note:** This exactly accounts for the VERIFY-1 memo's "91 records" count vs DB's 94. The three DB-only records were added to the DB after the mobile harvest pass. All three have zero mobile_blocking_mechanics. Search specs must be authored for all three (DB is authority for the crawl).

---

### poe2 (Path of Exile 2)
| Metric | Count |
|---|---|
| JSONL records | 38 |
| DB records (game=poe2) | 38 |
| Exact ID match | 38 |
| IN-JSONL-NOT-DB | 0 |
| IN-DB-NOT-JSONL | 0 |

**CLEAN.**

---

### tq+tq2 (Titan Quest + Titan Quest 2 — single JSONL)
| Metric | Count |
|---|---|
| JSONL records | 26 (21 tq + 5 tq2) |
| DB records (tq=21, tq2=5) | 26 |
| Exact ID match | 26 |
| IN-JSONL-NOT-DB | 0 |
| IN-DB-NOT-JSONL | 0 |

**CLEAN.**

---

### tl / tl1+tl2+tli (Torchlight — single JSONL)
| Metric | Count |
|---|---|
| JSONL records | 22 (2 tl1 + 11 tl2 + 9 tli) |
| DB records (tl1=2, tl2=11, tli=9) | 22 |
| Exact ID match | 22 |
| IN-JSONL-NOT-DB | 0 |
| IN-DB-NOT-JSONL | 0 |

**CLEAN.**

---

### undecember
| Metric | Count |
|---|---|
| JSONL records | 17 |
| DB records (game=undecember) | 17 |
| Exact ID match | 17 |
| IN-JSONL-NOT-DB | 0 |
| IN-DB-NOT-JSONL | 0 |

**CLEAN.** Note: JSONL uses prefix `ud-*`; DB uses `ud-*` consistently — no prefix drift.

---

### vs (Vampire Survivors)
| Metric | Count |
|---|---|
| JSONL records | 24 |
| DB records (game=vs) | 24 |
| Exact ID match | 24 |
| IN-JSONL-NOT-DB | 0 |
| IN-DB-NOT-JSONL | 0 |

**CLEAN.**

---

## Summary Table

| Basin | JSONL | DB | IN-JSONL-NOT-DB | IN-DB-NOT-JSONL |
|---|---|---|---|---|
| chronicon | 17 | 17 | 0 | 0 |
| d2 | 58 | 60 | 0 | 2 |
| d3 | 46 | 49 | 0 | 3 |
| d4 | 45 | 46 | 0 | 1 |
| di | 23 | 24 | 0 | 1 |
| gd | 41 | 41 | 0 | 0 |
| hades (h1+h2) | 13 | 13 | 0 | 0 |
| hot | 19 | 19 | 0 | 0 |
| la | 53 | 53 | 0 | 0 |
| le | 35 | 35 | 0 | 0 |
| mcd | 5 | 5 | 0 | 0 |
| **poe1** | **91** | **94** | **0** | **3** |
| poe2 | 38 | 38 | 0 | 0 |
| tq+tq2 | 26 | 26 | 0 | 0 |
| tl+tl2+tli | 22 | 22 | 0 | 0 |
| undecember | 17 | 17 | 0 | 0 |
| vs | 24 | 24 | 0 | 0 |
| **TOTAL** | **523** | **533** | **0** | **10** |

**Worst basin by raw gap count: d3 (3 DB-only), tied with poe1 (3 DB-only).** No JSONL-excess anywhere — the DB is a strict superset of the mobile harvest. No id-mismatch suspects found: all shared IDs are byte-exact matches.

---

## Id-Mismatch Suspects

**None identified.** Every kit present in both JSONL and DB has identical kit_id strings. No folk_name-same/id-different pairs detected in the compared population.

---

## Resolution note

These discrepancies are NOT resolved here. They are named for elrond's ingestion fix lane (the 10 DB-only records need their core_skills, aliases, and eras backfilled from authoritative sources — they currently have no JSONL counterpart). The three poe1 DB-only records require search specs authored directly from DB fields + general knowledge (see poe1-search-specs.jsonl).
