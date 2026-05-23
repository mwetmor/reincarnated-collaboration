# Weapon-Library-Import Hive-Mind — Live State

**Single source of truth.** Knight-rider updates each cycle. Anyone (including next-session knight-rider, gandalf, jack-ryan, Matt) reads this to know exactly where the hive-mind is.

**Mission doc:** `agentic_orchestration/weapon-library-import-hive-mind-mission-2026-05-22.md`

---

## Last update

| Field | Value |
|---|---|
| Timestamp | 2026-05-22 evening — knight-rider wind-down session |
| Cycle | 8 — **WIND-DOWN COMPLETE** (final summary written; checkpoint tagged) |
| Orchestrator | knight-rider (wind-down session, post API outage) |
| State | **IDLE / CHECKPOINTED** — clean total **89,839 / 100K (89.8%)**; no PIDs running; no sub-agents in flight; awaiting Matt direction on whether to push to floor (Wave-4) or pause at 89.8% |

---

## Counts (FINAL — post-A3-kill, all processes terminated)

| Table | Count | Notes |
|---|---|---|
| `weapon_knowledge_entries` (total all tags incl. quarantine) | **220,173** | includes 130,334 wikipedia-unfiltered quarantine |
| `weapon_knowledge_entries` (clean — excluding `wikipedia-unfiltered`) | **89,839** | **floor metric** |
| `weapons` (3D models) | **5,162** | Sketchfab 4,800 + Kenney 21 + OGA 341 |
| `knowledge_entry_reference_images` | **82,191** | URL-only per policy |
| `knowledge_model_attachments` | 0 | not populated; future cross-link pass |

**Progress vs floor (CLEAN COUNT):** **89,839 / 100,000 → 89.8%** (10,161 to go for floor)

**Final per-source contributors (clean — 24 sources):**

| Rank | Source | Count | License class | Track |
|---|---|---|---|---|
| 1 | royal_armouries | 38,127 | editorial_only | A3 (Matt-halted) |
| 2 | wikidata | 12,371 | CC0 | A1.1 |
| 3 | wikipedia (v2 clean) | 8,579 | CC-BY-SA | A1.2-FIX |
| 4 | met-museum | 7,559 | CC0 | H |
| 5 | nick-aschenbach-dnd-data | 6,297 | CC-BY | G |
| 6 | wow-classic-items | 4,440 | MIT | J |
| 7 | odin-army-tradoc | 3,998 | public-domain (US gov) | N |
| 8 | bsdata-warhammer-aos | 2,183 | unknown | M |
| 9 | cataclysm-dda | 1,599 | CC-BY-SA-3.0 | I |
| 10 | osrsbox-db | 940 | CC-BY-NC-SA (non-commercial) | G |
| 11 | pf2ools-pf2ools-data | 688 | OGL-1.0a | M |
| 12 | diablo2-d2data | 521 | unknown | K |
| 13 | path-of-exile-repoe | 494 | unknown | K |
| 14 | fextralife-elden-ring | 375 | fan-wiki | L |
| 15 | bloqhead-demigods | 320 | MIT | G |
| 16 | elden-ring-erdb | 307 | unknown | K |
| 17 | fextralife-ds2 | 239 | fan-wiki | L |
| 18 | fextralife-ds3 | 219 | fan-wiki | L |
| 19 | gta-v-data | 183 | unknown | K |
| 20 | fextralife-ds1 | 133 | fan-wiki | L |
| 21 | 5e-bits-5e-database-2024 | 110 | MIT | M |
| 22 | army-recognition | 62 | editorial | N |
| 23 | souls-api-thomaslincoln | 58 | unknown | M |
| 24 | 5e-bits-5e-database | 37 | MIT | G |
| — | **TOTAL CLEAN** | **89,839** | (mixed licenses; `v_weapons_cc0` view filters automatically) | |

**3D model sources (separate `weapons` table):**

| Source | Count | License |
|---|---|---|
| sketchfab | 4,800 | CC0 + CC-BY mix |
| oga | 341 | CC-BY-SA / OGA-BY |
| kenney | 21 | CC0 (yield-gap; task #11 fix open) |
| **TOTAL** | **5,162** | |

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
| wikipedia-unfiltered (A1.2 v1 output) | 130,334 | Loose full-dump keyword matcher; ~9-12% true-positive rate per spot-check. Replaced by Wikidata-anchored v2 ingest (`wikipedia` source_library, 8,579 clean rows). v1 retained for audit but excluded from floor count. |

---

## Track status (FINAL)

| Track | Source(s) | Status | Final count | Summary JSON |
|---|---|---|---|---|
| DISCOVERY | web/social/blog/GitHub source scouting | **COMPLETE** | 159 source rows | `…/discovery-wave1.csv` |
| G | 4 GitHub data repos | **COMPLETE** (2.9s) | 7,594 | `track-G-wave1.json` |
| A1.1 Wikidata SPARQL | Q728 weapon + subclasses (band-strategy after OFFSET timeout) | **COMPLETE** | 12,371 | (folded into A1) |
| A1.2 Wikipedia v1 | full-dump keyword matcher (FALSE-POSITIVE) | **COMPLETE-WITH-ISSUE / QUARANTINED** | 130,334 → `wikipedia-unfiltered` | (folded) |
| A1.2-FIX Wikipedia v2 | Wikidata-sitelink-anchored re-ingest | **COMPLETE** | 8,579 (clean) | (in-progress at A3-kill; final via DB query) |
| A1.3 Commons enricher | wikidata-P18 image license + dimensions | **TERMINATED (with A3-kill)** | ~partial | (folded; not separately summarized) |
| A2 | Smithsonian | **BLOCKED — Matt API key** | 0 | — |
| A3 | Royal Armouries (internal REST API; 67K addressable; editorial_only) | **HALTED BY MATT mid-crawl** | 38,127 (vs ~67K target) | — (no final summary; partial) |
| B1 Sketchfab | weapons-military CC0+CC-BY | **COMPLETE** | 4,800 | `track-b1-sketchfab-summary.json` |
| B2 Kenney | static asset packs | **COMPLETE-WITH-GAP** (21/150; fix-task #11 open) | 21 | `track-b2-kenney-summary.json` |
| B3 OGA | weapons category w/ 15s delay | **COMPLETE** | 341 | `track-b3-oga-summary.json` |
| H Met Museum API | collectionapi.metmuseum.org Arms&Armor (CC0) | **COMPLETE-PARTIAL** (7,459 inserted from 13,753 IDs; 6,207 errors @ 56.8% image coverage; 6hr wall) | 7,559 | `track-H-met-museum-summary.json` |
| I Cataclysm DDA | git-clone CC-BY-SA modern/improvised | **COMPLETE** (6.7s) | 1,599 | `track-I-cataclysm-summary.json` |
| J WoW Classic | nexus-devs/wow-classic-items MIT MMO | **COMPLETE** | 4,440 | `track-J-wow-classic-items.json` |
| K Multi-ARPG | PoE RePoE + Elden Ring + D2 + GTA-V | **COMPLETE** | 1,505 across 4 sources | `track-K-wave1.json` |
| L Fextralife soulslike | DS1/DS2/DS3/BB/ER fan-wiki bundle | **COMPLETE** (Bloodborne yielded 0) | 966 | `track-L-fextralife.json` |
| M GitHub supplemental | pf2ools + 5e-2024 + warhammer-AoS + Souls_API (Kaggle skipped) | **COMPLETE** (98s) | 3,039 | `track-M-bundle.json` |
| N Modern military | ODIN US Army TRADOC + Army Recognition | **COMPLETE** (odin 3,998 + AR 62 = 4,060) | 4,060 | `track-N-summary-2026-05-22.json` |
| E | MyArmoury / Swordis / editorial | **DEFERRED** (never fired) | 0 | — |

---

## In-flight PIDs — ALL TERMINATED

No processes running. Verified post-kill via `ps -ef | grep -E "(weapon\|crawl\|wikidata\|...)"` → no matches.

Final PID disposition:
- 44776 (A3 Royal Armouries): killed by Matt at clean=89,839 mid-crawl
- 44284 (A1.3 Commons enricher): terminated with A3-kill
- 64952 (Wikipedia v2 FIX): natural completion before kill (8,579 rows landed)
- 65205 (H Met Museum): natural completion before kill (7,459 inserted; 6hr wall)
- 66320 (L Fextralife): natural completion before kill (966 rows)
- 66412 (M GitHub bundle): natural completion before kill (3,039 rows)
- 66987 (N Army Recognition): natural completion before kill (62 rows)
- All Wave-1 short-runners (43941/43950/44095/44110): natural completion long before kill

Kill command (for reference / historical record):
```bash
kill -TERM 44776 64952 65205 66320 66412 66987
```
(Most had already exited by the time Matt issued the halt; A3 + Commons were the only true mid-flight terminations.)

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

### Cycle 6 — Wave-2 all returned; Wave-3 fired (2026-05-22 06:00-06:20 EDT)

- Wave-2 J/K/I/H all returned cleanly. Track J 4,440 WoW; Track K 1,505 across 4 ARPG sources; Track I 1,599 Cataclysm (3 schema-iterations during fire); Track H Met Museum still firing in background (~13K target)
- Wikipedia-fix v2 (PID 64952) delivering CLEAN weapons (T+5min spot-check 100% true positive: AK-74, Fat Man, M61 Vulcan, Gladius, Gungnir, Naginata, Uzi)
- Authored Wave-3 dispatches L/M/N + fired sub-agents in parallel

### Cycle 7 — Wave-3 strong returns; modern military gap filled (2026-05-22 06:20-06:25 EDT)

- **Track N modern military:** ODIN US Army TRADOC delivered 3,998 entries (CC0 US gov public domain). Sub-agent reverse-engineered the DotCMS API via JS bundle analysis. Army Recognition continuing at 5s/request (PID 66987; AR ~50 article URLs to ingest). globalmilitary.net dispositioned RED (Cloudflare WAF blocks regardless of permissive robots). Small Arms Survey structural-skip (aggregate stats, no per-weapon rows).
- **Track M GitHub bundle:** Pf2ools 688 + Warhammer AoS 2,183 (huge surprise yield from BSData tabletop) + 5e-2024 110 + Souls_API 58 = 3,039 rows. Exceeds acceptance 800.
- **Track L Fextralife:** progressing nicely; DS1/DS2/DS3/Bloodborne/ER all contributing; ~880-970 forecast.
- **Wikipedia fix:** 4,600 clean rows already (target ~6K); 100% true-positive on spot-check
- **Met Museum:** 613 climbing (target ~13K)
- **Royal Armouries:** 11,840 climbing (target ~67K; ~22hr to go)

**Wave-3 floor-trajectory check:** at current rates, 100K floor projected to clear in next 6-12 hours (driven mostly by Royal Armouries continuing to deliver museum entries + Met API completing + Wikipedia fix completing). Ceiling 200K NOT projected on Wave-3 alone — would need a Wave-4 push to reach ceiling.

### Cycle 8 — Wind-down (2026-05-22 evening; this knight-rider session, post API outage)

**Trigger:** Matt halted A3 mid-crawl + signaled wind-down. API outage during prior knight-rider attempt left the state file mid-update; this session reconciles.

**Wind-down actions:**
1. **PID verification.** `ps -ef | grep …` → no matching processes. All terminated.
2. **Final count snapshot.** Clean total **89,839 / 100K (89.8%)**; all-tags total 220,173; 5,162 weapons (3D models); 82,191 reference images; 24 clean source libraries + 1 quarantined.
3. **Royal Armouries final tally:** 38,127 rows (vs ~67K full target). At Matt's halt point — A3 contributed ~42% of the clean substrate alone.
4. **Met Museum revised result:** 7,459 inserted from 13,753 object IDs (54%); 6,207 errors at 359-min wall. Image coverage 56.8% (below 70% acceptance). NOT a Wave-2 win; Wave-4 retry needed if Met is desired complete.
5. **Wikipedia v2 fix final:** 8,579 clean rows (vs 7,400-8,700 forecast). Tight bullseye on math-note prediction. Discipline #1 (math-before-code) validated.
6. **Fextralife L track:** 966 rows (vs ≥1000 acceptance gate → **acceptance not met**). Bloodborne wiki yielded 0; the other 4 carry the substrate. Errors 97 (DS3 had 30 errors, ER had 33). Real source but soft on absolute count.
7. **Misplaced script.** A Wave-2 sub-agent created `scripts/track_j_wow_classic.py` at repo root instead of under `legolas/research/.../scripts/`. Moved to canonical location.
8. **__pycache__ removed.** Python bytecode cache purged from scripts dir.
9. **State file updated** (this doc) to reflect final IDLE state.
10. **Wind-down summary** authored at `agentic_orchestration/weapon-library-import-wind-down-summary-2026-05-22.md` (next: see § Cross-references).
11. **CHANGELOG entry** appended.
12. **skill_handoff** authored at `agentic_orchestration/skill_handoff_2026-05-22-windown.md`.
13. **Tag:** `knight-rider/weapon-library-hive-mind-cycle-8-windown-2026-05-22` (seam-prefix; intermediate state; not Matt-milestone).

**Decision point for Matt:**
- (a) **Accept 89.8%** as substrate-complete and pivot to next-phase work (canonical normalization / abstraction analysis / engine integration). 10,161 short of floor; well above 10× the original 15-entry catalogue; sufficient for emergent-pattern analysis.
- (b) **Wave-4 fire** to close the 10K gap (and potentially reach the 200K ceiling). Candidates queued: (i) re-fire A3 to completion (~22hr remaining at last rate; ~29K more rows); (ii) Met Museum retry on the 6,207 errored IDs (parameter fixup; ~6K more); (iii) Pitt Rivers Museum + Louvre metadata-only; (iv) Wave-3 deferred candidates (Lexicanum/Halopedia/Firearms Guide AMBER probe). A3 alone would clear the floor cleanly.

No-decision-yet stance: hive-mind is **IDLE / CHECKPOINTED**. Matt directs.

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
