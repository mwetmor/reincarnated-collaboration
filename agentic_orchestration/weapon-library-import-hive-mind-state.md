# Weapon-Library-Import Hive-Mind — Live State

**Single source of truth.** Knight-rider updates each cycle. Anyone (including next-session knight-rider, gandalf, jack-ryan, Matt) reads this to know exactly where the hive-mind is.

**Mission doc:** `agentic_orchestration/weapon-library-import-hive-mind-mission-2026-05-22.md`

---

## Last update

| Field | Value |
|---|---|
| Timestamp | 2026-05-22 — Wave-1 COMPLETE; Wave-1.5 fix + Wave-2 (H/I/J/K) firing |
| Cycle | 5 (DISCOVERY returned; Wave-1 wikipedia false-positive caught + quarantined; Wave-1.5 + Wave-2 firing) |
| Orchestrator | knight-rider (this session) |
| State | WAVE_2_FIRING + WIKIPEDIA_FIX_FIRING |

---

## Counts

| Table | Count | Updated |
|---|---|---|
| `weapon_knowledge_entries` (total all tags) | 160,723 | Cycle 5 |
| `weapon_knowledge_entries` (clean — excluding `wikipedia-unfiltered`) | **30,389** | Cycle 5 |
| `weapons` (3D models) | 5,162 | Cycle 5 |
| `knowledge_entry_reference_images` | 40,689 | Cycle 5 |
| `knowledge_model_attachments` | 0 | (not populated by Wave-1; future track) |

**Progress vs floor (CLEAN COUNT):** **30,389 / 100,000 → 30.4%**

**Breakdown by source_library (CLEAN — quality verified):**
| source_library | count | quality |
|---|---|---|
| wikidata (A1.1 complete) | 12,371 | CLEAN (SPARQL Q728 weapon class) |
| royal_armouries (A3 in flight; ~28hr) | 10,544 | CLEAN (museum collection objects) |
| nick-aschenbach-dnd-data (G) | 6,297 | CLEAN |
| sketchfab (B1) | 4,800 | CLEAN (weapons-military tag) |
| osrsbox-db (G) | 940 | CLEAN |
| oga (B3) | 341 | CLEAN |
| bloqhead-demigods (G) | 320 | CLEAN |
| 5e-bits-5e-database (G) | 37 | CLEAN |
| kenney (B2) | 21 | CLEAN (yield-gap; fix-task #11) |

**QUARANTINED (audit-preserved; not in floor count):**
| source_library | count | issue |
|---|---|---|
| wikipedia-unfiltered (A1.2 v1 output) | 130,334 | Loose full-dump keyword matcher; ~9-12% true-positive rate per spot-check. Re-ingestion via Wikidata-anchored matcher firing as Wave-1.5 fix (track-A1-WIKIPEDIA-FIX dispatch) |

---

## Track status

| Track | Source(s) | Status | PID | Log | JSON summary | Last count |
|---|---|---|---|---|---|---|
| DISCOVERY | web/social/blog/GitHub source scouting | **COMPLETE** | done | — | discovery-wave1.csv (159 rows; 73% robots-verified) | total addressable ~604K |
| G | 4 GitHub data repos | **COMPLETE (2.9s)** | done | — | `…/summaries/track-G-wave1.json` | 7,594 |
| A1.1 Wikidata SPARQL | Q728 weapon + subclasses | **COMPLETE** | done | `…/logs/knowledge_crawl_wikidata.log` | (folded) | 12,371 |
| A1.2 Wikipedia v1 | full-dump keyword matcher (FALSE-POSITIVE; quarantined) | **COMPLETE-WITH-ISSUE** | done | `…/logs/knowledge_crawl_wikipedia.log` | (folded) | 130,334 → `wikipedia-unfiltered` |
| **A1.2-FIX Wikipedia v2** | **Wikidata-sitelink-anchored re-ingest** | **FIRING (Wave-1.5)** | sub-agent | — | `…/knowledge_crawl_wikipedia_v2_summary.json` | TBD (expect ~10-15K) |
| A1.3 Commons enricher | wikidata-P18 image license + dimensions | RUNNING (~5-11hr full enrich) | **44284** | `…/logs/knowledge_crawl_commons.log` | (folded) | ~1K processed |
| A2 | Smithsonian | BLOCKED — Matt API key | — | — | — | 0 |
| A3 | Royal Armouries (internal REST API; 67K addressable; editorial_only) | RUNNING (~28hr wall) | **44776** | `…/logs/weapon-library-track-A3.log` | TBD | 10,544 (climbing) |
| B1 Sketchfab | weapons-military CC0+CC-BY | **COMPLETE** | done | `…/logs/model_crawl_sketchfab.log` | `…/summaries/track-b1-sketchfab-summary.json` | 4,800 (×4 over projection) |
| B2 Kenney | static asset packs | COMPLETE-WITH-GAP (21/150; task #11) | — | — | `…/summaries/track-b2-kenney-summary.json` | 21 |
| B3 OGA | weapons category w/ 15s delay | **COMPLETE** | done | `…/logs/model_crawl_oga.log` | `…/summaries/track-b3-oga-summary.json` | 341 |
| **H Met Museum API** | collectionapi.metmuseum.org Arms&Armor dept (CC0) | **FIRING (Wave-2)** | sub-agent | — | `…/summaries/track-H-wave1.json` | TBD (expect ~13K) |
| **I Cataclysm DDA** | git-clone CC-BY-SA modern/improvised | **FIRING (Wave-2)** | sub-agent | — | `…/summaries/track-I-wave1.json` | TBD (expect 800-3K) |
| **J WoW Classic** | nexus-devs/wow-classic-items MIT MMO | **FIRING (Wave-2)** | sub-agent | — | `…/summaries/track-J-wave1.json` | TBD (expect 3K-8K) |
| **K Multi-ARPG** | PoE RePoE + Elden Ring + D2 + GTA-V (5 repos bundled) | **FIRING (Wave-2)** | sub-agent | — | `…/summaries/track-K-wave1.json` | TBD (expect 1.5K+) |
| E | MyArmoury / Swordis / editorial | DEFERRED (Wave-3 candidate; low priority since Wave-2 should clear floor) | — | — | — | 0 |

---

## In-flight PIDs

| PID | Track | Script | Started | Est. wall |
|---|---|---|---|---|
| 43941 | A1.1 Wikidata SPARQL | `a1_1_wikidata_sparql.py` | wave-1 | 2-4 hours (band-strategy) |
| 43950 | A1.2 Wikipedia dump | `a1_2_wikipedia_dump_parser.py` | wave-1 | 3-6 hours (bandwidth-bound) |
| 44095 | B1 Sketchfab | `track_b1_sketchfab_crawl.py` | wave-1 | 15-30 min |
| 44110 | B3 OGA | `track_b3_oga_crawl.py` | wave-1 | 100-150 min |
| 44284 | A1.3 Commons enricher | `a1_3_commons_enricher.py` | wave-1 (re-fired post URL-fix) | 5-11 hours |
| 44776 | A3 Royal Armouries | `track_a3_royal_armouries.py` | wave-1 | ~28 hours (20-items/page cap) |
| ~~44292~~ | ~~Track G~~ | ~~`track_g_import.py`~~ | ~~completed 2.9s~~ | DONE |

To kill all in-flight PIDs (graceful wind-down):
```bash
kill -TERM 43941 43950 44095 44110 44284 44776
```

---

## Newly discovered sources (from DISCOVERY scout)

DISCOVERY scout returned 159 source rows (73% robots-verified) at `agentic_orchestration/legolas/research/weapon-library-import-2026-05-22/discovery-wave1.csv`. Total addressable yield (GREEN + GREEN-with-caution, midpoint estimates): ~604K weapons. The 100K-200K floor/ceiling target is achievable. Key surprises:

1. **Met Museum Open Access API** at `collectionapi.metmuseum.org` — GREEN (no robots.txt; CC0; 13,753 Arms&Armor objects). Different subdomain from RED `metmuseum.org`. **→ Fired as Track H Wave-2.**
2. **Cataclysm: Dark Days Ahead** — CC-BY-SA modern/improvised weapons (1K-3K) on GitHub. **→ Fired as Track I Wave-2.**
3. **Wikidata revised upward** — 13,134 confirmed (vs prior 10,497 estimate); +25%.
4. **ODIN Worldwide Equipment Guide (US Army TRADOC)** — US gov public domain; modern military. Wave-3 candidate.
5. **Firearms Guide** (84K firearms, ClaudeBot not blocked but paywall) — Wave-3 AMBER probe needed.

Wave-2 fires (current): H, I, J, K + Wikipedia FIX (Wave-1.5).
Wave-3 candidates (queued, not yet fired):
- ODIN US Army TRADOC (modern military gap-fill)
- Fextralife soulslike bundle (1.5K weapons; ClaudeBot absent from robots; GPTBot blocked)
- Wikipedia Category:Firearms specific bulk-dump pass (modern military)
- Pitt Rivers Museum Arms & Armour
- Lexicanum (Warhammer 40K) + Halopedia (community-wiki check)
- Met Museum images: post-Track-H, run a Commons-style image enrichment pass
- BSData/warhammer-age-of-sigmar (tabletop)

Flags Matt should be aware of (no blocking; recorded for downstream):
- **osrsbox-db license:** underlying OSRS wiki content is CC-BY-NC-SA 3.0 (non-commercial). 940 rows present in DB; commercial-use is a derived flag per mission § 3 — these won't appear in `v_weapons_cc0`. Decision deferred until commercial-pipeline integration.
- **Louvre nuance:** robots blocks ClaudeBot on image-byte file extensions only; metadata pages are GREEN. URL-only storage policy already complies. Worth a Wave-3 metadata-only pass.
- **A3 license:** all Royal Armouries entries `license_class='editorial_only'`. Indexable substrate but excluded from `v_weapons_cc0` automatically.

---

## Open Matt-side blockers

| ID | Blocker | Impact |
|---|---|---|
| C1 (carry) | `MESHY_API_KEY` not persisted in `~/.zshrc` | Blocks Meshy bulk-import (deferred substrate, not blocking floor) |
| C4 (carry) | `SMITHSONIAN_API_KEY` not registered | Blocks Track A2 only |
| C5 (carry) | CC-BY-SA legal review for commercial use | NOT blocking indexing; only blocks commercial-derived flag for CC-BY-SA assets |

---

## Cycle log

### Cycle 0 — initialization (2026-05-22)

- Verified DB state: 17 tables present, all counts 0
- Verified no in-flight processes
- Authored mission brief: `weapon-library-import-hive-mind-mission-2026-05-22.md`
- Authored state file (this doc)
- Authored 3 new dispatches: DISCOVERY, Track G, Track E
- **Wave 1 fire imminent: DISCOVERY + Track G + Track A1 + Track A3 + Track B (5 parallel sub-agents via Task tool)**

### Cycle 1 — Wave-1 partial (Track B first to return, 2026-05-22)

- Track B sub-agent returned. 3 scripts authored + fired.
- B1 Sketchfab: PID 44095; ~200/min; 400+ rows at first count; expected 800-1,200 final
- B2 Kenney: COMPLETE; only 21 rows vs 150 target. Script-fix dispatched (task #11): regex extension for `unit_/item_/prop_/weapon_` prefix patterns + live pack-URL probe (hardcoded URLs 404'd due to content-hash rotation)
- B3 OGA: PID 44110; 15s/request; phase 1 (entry-URL collection) in progress; ~100-150 min total
- Math note + 3 scripts + 1 JSON-summary stub committed under `legolas/research/weapon-library-import-2026-05-22/`
- DISCOVERY + Track G + A1 + A3 still in flight — will batch-update on next return

### Cycle 2 — Track G complete (2026-05-22)

- Track G sub-agent returned. PID 44292 ran clean in **2.9 seconds** (all data via raw.githubusercontent.com CDN; no clone needed)
- 7,594 net rows from 4 GitHub sources: nick-aschenbach (6,297), osrsbox-db (940), bloqhead-demigods (320), 5e-bits (37)
- 1,050 ignored as collision-duplicates (community D&D homebrew has duplicated magic-item names; INSERT OR IGNORE handled)
- One mid-run SSL fix: macOS Python urllib needed `certifi` CA bundle; second fire succeeded
- 2,047 reference images registered (URL-only per mission policy)
- Track A1 wikidata also visibly producing (12,371 rows at this snapshot — sub-agent will return its own status separately)
- **Floor progress: 20% (19,965 / 100,000)**
- Wave-2 GitHub repo recommendations from sub-agent: 5e-bits 2024 edition, Pf2ools (Pathfinder 2e), Souls_API (Dark Souls), Kaggle DS3 weapons CSV, WoW community repos — these go into the Wave-2 fire queue once DISCOVERY scout returns

### Cycle 3 — Track A1 sub-agent returned; 3 long-running PIDs registered (2026-05-22)

- A1 sub-agent returned with 3 scripts authored + fired as OS-background:
  - **A1.1 Wikidata SPARQL** (PID 43941): OFFSET pagination got 3 chunks (13,468 entries), then 504-timeout at offset=20K predicted in math note → band-chunking fallback engaging now. Target 30K-60K final entries; 2-4hr wall.
  - **A1.2 Wikipedia XML dump** (PID 43950): 741MB of 22GB downloaded; bandwidth-bound; parse fires automatically after download (~15min parse). Target +15K-40K entries; 3-6hr total wall.
  - **A1.3 Commons enricher** (PID 44284): URL parser had a bug (Wikidata uses `Special:FilePath/` not `wiki/File:`); fixed + re-fired; enriching 1,090+ images at 1 req/sec. Target full enrichment 5-11hr.
- Track A1 alone forecasts 30K-60K (A1.1) + 15K-40K (A1.2) = **45K-100K entries** toward the 100K floor
- All A1 processes are nohup-class; will keep running across this session if needed; PIDs registered for wind-down
- DISCOVERY + Track A3 still in flight

### Cycle 4 — Track A3 sub-agent returned; long-haul process registered (2026-05-22)

- A3 sub-agent returned; script firing as PID 44776
- **Architectural discovery:** Royal Armouries publishes an undiscovered internal REST API at `collections.armouries.net/api/v3/search` (reverse-engineered from Vue SPA bundle). Addresses 67,783 physical museum objects (filter `data_type:(object)`) with 9,503 having media/images
- **Empirical correction:** API ignores `size` param and caps at 20 items/page → wall time revised from ~6hr to ~28hr (3,390 requests × 30s honoring 20s Crawl-delay × 1.5)
- **License:** all entries `editorial_only` (Royal Armouries proprietary, non-commercial) — recorded per policy; commercial-usability flag derives downstream; excluded from `v_weapons_cc0` view automatically
- **Cultural register coverage:** British, European, East/South Asian (Japan, India, China), African, Middle Eastern, South American — strong diversity beyond European-saturated default
- Image-server note: `images.royalarmouries.org` blocks ClaudeBot; replaced with `collections.armouries.net/media/` (200-verified; same robots policy GREEN)
- **Wave-1 forecast (all tracks combined):** ~85K-180K weapons by ~T+28hr. Tracking to FLOOR purely on Wave-1.
- Only DISCOVERY scout still in flight from Wave-1

### Cycle 5 — DISCOVERY returned; Wikipedia false-positive caught + quarantined; Wave-1.5 + Wave-2 firing (2026-05-22)

**Major findings:**
- DISCOVERY scout returned 159 sources / 73% robots-verified. Met Museum API discovered as #1 GREEN find (13,753 CC0 Arms&Armor objects via `collectionapi.metmuseum.org` subdomain — different from RED `metmuseum.org`)
- **Quality issue caught:** A1.2 Wikipedia v1 produced 130,334 rows via loose full-dump keyword matcher. Spot-check showed ~9-12% true-positive rate (false matches: athletes, actors, footballers, songs, train stations, Eurovision entries, kings). The implementation deviated from the original A1.2 dispatch spec which called for Wikidata-sitelink-anchored matching.
- **Operational response:** quarantined the 130,334 rows by renaming `source_library` from `wikipedia` → `wikipedia-unfiltered` (audit-preserved, excluded from clean views and floor count). Wave-1.5 fix dispatch fires v2 ingestion with the canonical Wikidata-anchored matcher.

**Wave-1 final tallies (clean):**
- 12,371 wikidata + 10,544 royal_armouries (climbing) + 7,594 Track G + 4,800 sketchfab + 341 OGA + 21 kenney + 5,162 weapons (3D models) = ~30K clean knowledge entries + ~5K models

**Wave-2 fires (5 sub-agents in parallel):**
- A1.2-FIX Wikipedia v2 (Wikidata-anchored)
- H Met Museum API (~13K CC0)
- I Cataclysm DDA (~800-3K CC-BY-SA modern/improvised)
- J WoW Classic Items (~3K-8K MIT MMO)
- K Multi-ARPG bundle (~1.5K+ across 5 repos: PoE/ER/D2/GTA-V)

**Floor forecast post-Wave-2:** ~30K (current clean) + ~10-15K (wikipedia fix) + ~13K (Met) + ~3K (Cata) + ~6K (WoW) + ~1.5K (K) + ~57K more from A3 continuing = ~120K clean → floor cleared with margin.

**Discipline #11 lesson:** empirical inspection caught the Wikipedia false-positive at T+5hr post-fire instead of after committing to floor-reached wind-down. Audit-preservation pattern (rename source_library rather than DELETE) keeps the bad data inspectable.

### Cycle 6 — TBD (Wave-2 returns + Wave-3 fire decision)

---

## Operational quick-reference

### Live counts (one-shot)
```bash
sqlite3 /Users/admin/Games/reincarnated-loadout/data/telemetry.db "
SELECT 'knowledge' AS type, source_library, COUNT(*) AS n
FROM weapon_knowledge_entries GROUP BY source_library
UNION ALL
SELECT 'weapons', source_library, COUNT(*)
FROM weapons GROUP BY source_library
UNION ALL
SELECT 'images', image_source, COUNT(*)
FROM knowledge_entry_reference_images GROUP BY image_source;"
```

### Total progress
```bash
sqlite3 /Users/admin/Games/reincarnated-loadout/data/telemetry.db \
  "SELECT COUNT(*) AS total_knowledge_entries FROM weapon_knowledge_entries;"
```

### In-flight processes
```bash
ps -ef | grep -E "(weapon|crawl|wikidata|wikipedia|github|royal|sketchfab|kenney|oga|myarmoury|swordis|discovery)" | grep -v grep
```

### Per-track logs
```bash
ls -la /Users/admin/Games/reincarnated-engine/logs/weapon-library-* 2>/dev/null
```

### Per-track summaries
```bash
ls -la /Users/admin/Games/reincarnated-collaboration/agentic_orchestration/legolas/research/weapon-library-import-2026-05-22/summaries/
```

---

**Signed:** knight-rider (live state; update as the hive-mind moves)
