# Dispatch — legolas Mode A — DISCOVERY: Source Scouting for Weapon-Library-Import Hive-Mind

**Date:** 2026-05-22
**Author:** knight-rider (hive-mind orchestrator)
**For:** legolas (Mode A analytical research)
**Pattern:** B (long task; fan-out across many web sources)
**Status:** FIRING (Wave 1)
**Mission:** `agentic_orchestration/weapon-library-import-hive-mind-mission-2026-05-22.md`
**State:** `agentic_orchestration/weapon-library-import-hive-mind-state.md`

---

## Required reading

1. Mission doc (above)
2. `agentic_orchestration/logs/2026-05-22-evening-robots-verification.md` — existing robots-verified source dispositions
3. `agentic_orchestration/legolas/research/weapon-library-import-2026-05-22/findings-summary.md` — original 14-library inventory
4. This dispatch in full

---

## Task

Search the public web (search engines, GitHub, GitLab, Codeberg, blogs, forums, museum collection portals, gaming community wikis, mod databases, academic data repositories, social media) for **every viable source of weapon data** (text descriptions, structured metadata, reference images, 3D models) across all genres named in the mission doc § 2.1.

Return a **CSV** of source candidates with per-row:
- `source_name` (human-readable)
- `url` (canonical URL — root domain or API endpoint)
- `category` (one of: `historical-museum`, `historical-academic`, `fantasy-rpg-canonical`, `fantasy-rpg-community`, `sci-fi-canonical`, `sci-fi-community`, `modern-military`, `game-data-mmo`, `game-data-arpg`, `game-data-soulslike`, `game-data-monster-hunter-like`, `game-data-fps`, `game-data-other`, `modding-database`, `community-editorial`, `3d-model-library`, `image-library`, `bibliographic`, `etymology-linguistics`, `other`)
- `genres` (semicolon-separated subset of mission § 2.1 domains)
- `est_capacity` (rough estimate of weapon-entry count addressable: e.g., `<100`, `100-1K`, `1K-5K`, `5K-20K`, `20K-100K`, `>100K`)
- `access_method` (one of: `bulk-dump`, `rest-api`, `graphql-api`, `sparql`, `https-crawl`, `git-clone`, `static-download`, `web-scrape`, `other`)
- `license_likely` (best guess: `CC0`, `CC-BY`, `CC-BY-SA`, `OGL`, `public-domain`, `proprietary-but-redistributable`, `proprietary`, `unknown`)
- `robots_status` (one of: `GREEN`, `GREEN-with-caution`, `AMBER`, `RED`, `unverified`) — best-effort per `robots.txt` lookup
- `claude_agent_explicit` (one of: `allowed`, `blocked`, `unlisted`, `unknown`)
- `crawl_delay_seconds` (integer or `none`)
- `priority_for_floor` (1-5; 1=must-have, 5=long-tail) — your judgment based on est_capacity × access_method ease × license_fit
- `notes` (free-text: gotchas, sub-paths, ToS link, API key requirement, etc.)

Output: `agentic_orchestration/legolas/research/weapon-library-import-2026-05-22/discovery-wave1.csv`

Also produce: `agentic_orchestration/legolas/research/weapon-library-import-2026-05-22/discovery-wave1-summary.md` — narrative rollup: top-priority sources, surprising findings, dead-end paths investigated, recommended next-wave fire order.

---

## Specific sources to investigate (seed list from Matt + prior research)

Investigate these explicitly and include in the CSV:

| Source | Notes from Matt / context |
|---|---|
| `https://github.com/nick-aschenbach/dnd-data` | D&D 5e data repo; CC license expected; small but high-quality |
| `https://www.osrsbox.com/projects/osrsbox-db/` + their GitHub org | OSRS weapons database; explicitly redistributed; structured JSON |
| `https://myarmoury.com/` | Historical-armoury community editorial site; geometry + cross-sections per Matt's note ("very promising") |
| Swordis Global Weapon Index | Need to find canonical URL; geometry-rich per Matt's note |
| Wikidata Q728 (weapon) subclass tree | Already in Track A1; confirm SPARQL approach |
| Wikipedia Category:Weapons + subcategories (all subcats: by region, by era, by type) | Already in Track A1 |
| Wikimedia Commons Category:Weapons | Already in Track A1 / image enrichment |
| Smithsonian Open Access (api.data.gov) | Already in Track A2 (BLOCKED on API key) |
| Met Museum API at `metmuseum.org/api` | Site crawl was RED; API path needs separate robots check |
| Royal Armouries | Already in Track A3 |
| Sketchfab CC0+CC-BY weapon tag | Already in Track B (3D models) |
| Kenney.nl asset packs | Already in Track B |
| Open Game Art weapons category | Already in Track B |

### Categories to systematically scout (open-ended)

For each category, name as many specific viable sources as you can find:

1. **D&D ecosystem:** SRD, OGL-derived sites, dndbeyond (paid; OGL portion?), dnd5eapi.co, open5e.com, 5e.tools, Pathfinder Archives of Nethys, Starfinder SRD, OGL-licensed third-party publisher sites
2. **MMO data:** WoWHead (and the open data export?), GW2 API, FFXIV public data (Garland Tools, XIVAPI), ESO data sources, Final Fantasy wiki etc. — but check robots; many are RED
3. **ARPG / soulslike:** PoE GGG-official API, Diablo III/IV community data, Elden Ring open community DB, Dark Souls / Bloodborne community catalogues
4. **Monster Hunter / Capcom titles:** MHWiki alternatives, kiranico (check robots)
5. **JRPG:** Final Fantasy weapon catalogues, Dragon Quest, Persona, Tales-of series
6. **Indie game weapon dumps:** Terraria wiki, Stardew Valley, Vampire Survivors, Hades, etc. (check robots)
7. **Modding databases:** Nexus Mods (API?), Mod DB, Steam Workshop, GameBanana — check ToS + robots
8. **Historical/academic:** university museum collections (Harvard Semitic Museum, Penn Museum, Pitt Rivers Oxford, British Museum API, Louvre, Hermitage, regional national museums); Metropolitan museums in many countries; Europeana
9. **Firearms-specific:** IAMD, gun catalogue databases (check ethical floor), military museum collections (Imperial War Museum, US Army museums), NRA museum
10. **Mythological / legendary:** Theoi.com (Greek), regional mythology databases, Encyclopedia Mythica, folklore catalogues, regional epic poetry databases (Mahabharata, Ramayana weapon catalogues)
11. **Sci-fi canonical:** Star Wars: Wookieepedia (Fandom, AMBER), Memory Alpha (Star Trek, Fandom AMBER), Warhammer 40K Lexicanum (independent wiki — check robots), Halopedia, Mass Effect wiki, Cyberpunk wiki
12. **Tabletop wargames:** Warhammer Age of Sigmar, Warmachine, Infinity, etc. weapon profiles
13. **3D model libraries beyond Sketchfab/Kenney/OGA:** TurboSquid (commercial), CGTrader (mixed), Free3D, Quaternius, ambientcg, Poly Haven, mixamo
14. **GitHub/GitLab data repos:** search GitHub for `weapon-data`, `rpg-data`, `dnd-data`, `mmo-weapons`, `<game-name>-data` etc. Compile every active repo with ≥10 stars OR ≥1 commit in last 2 years
15. **Etymology / linguistic:** Wiktionary weapon-name entries; etymology databases (etymonline); regional language weapon-vocabulary catalogues
16. **Archaeology / typology:** Oakeshott sword typology references; Petersen Viking sword typology; lithic projectile databases; bronze age weapon catalogues
17. **HEMA / martial arts:** historical European martial arts references; Asian martial arts weapon catalogues; specialized weapon-tradition databases

### Scout discipline

- Do NOT fetch URLs from RED sources after confirming RED (waste of bandwidth)
- For each AMBER source, attempt one alt-path verification (e.g., MediaWiki api.php direct for Fandom; check if the API surface is open even if site crawl is blocked)
- For each source named in the CSV, ATTEMPT robots.txt fetch and capture the result in `robots_status`
- Use the Wikimedia-etiquette User-Agent (`reincarnated-engine/0.1 (research; mhwetmore@gmail.com)`) for all probe fetches
- Honor any explicit Crawl-delay you encounter in robots.txt during probing — even probes
- Cite your sources for est_capacity guesses (e.g., "Wikidata SPARQL count returns ~15K", "GitHub repo README claims 25K items", "Wikipedia category subtree count via PetScan tool")

---

## Discipline #19 compliance

- Mode A is research-time work, NOT long-running background crawl. Most of your work is read-only WebFetch + WebSearch with bursts of analysis. Should complete in <2 hours of agent runtime.
- If any sub-investigation requires a long-running probe (e.g., enumerating GitHub repos via paginated API), structure that as: author probe script → fire `nohup python probe.py > log 2>&1 &` → return PID + log path to knight-rider; knight-rider polls on-demand
- Final deliverable is the CSV + summary doc, NOT a babysit handoff

---

## Discipline #20 compliance

- Every URL you actually fetch (not just name in the CSV) goes through robots.txt verification first
- If you encounter a source you didn't anticipate that explicitly Disallows ClaudeBot, log it in the CSV with `robots_status=RED` and `claude_agent_explicit=blocked` and DO NOT crawl further
- The CSV is the deliverable — including AMBER and RED sources, since the dispositions themselves are valuable cross-reference

---

## Acceptance criteria

| # | Criterion |
|---|---|
| 1 | CSV at canonical path with ≥150 source rows (the floor — likely you'll find 300-500+) |
| 2 | All 17 categories above have ≥3 sources represented in the CSV |
| 3 | Each row has all columns populated (no NULL except where genuinely unknown) |
| 4 | All 3 Matt-named sources explicitly investigated and CSV'd (nick-aschenbach/dnd-data, osrsbox-db, MyArmoury) + Swordis Global Weapon Index found and CSV'd |
| 5 | Summary doc with: top 30 sources by `priority_for_floor`; top 10 surprises (high-yield finds Matt likely didn't know); top 5 dead-end paths investigated with reasons; recommended Wave-2 fire order |
| 6 | ≥40% of CSV rows are robots-verified (`robots_status` ≠ `unverified`) |
| 7 | Total estimated yield (sum of est_capacity midpoints across GREEN + GREEN-with-caution rows) reported in summary — provides realistic check vs 100K floor |
| 8 | No ClaudeBot UA used in any probe; research-agent UA only |

---

## Out of scope

- Authoring crawl scripts for newly discovered sources (that's the per-track Wave-2 dispatches knight-rider will spawn)
- Negotiating with site owners for elevated access
- Paying for any service
- Crawling RED sources to confirm they're really RED (one robots.txt fetch is enough)

---

## Cross-references

- Mission: `agentic_orchestration/weapon-library-import-hive-mind-mission-2026-05-22.md`
- State: `agentic_orchestration/weapon-library-import-hive-mind-state.md`
- Existing robots verification: `agentic_orchestration/logs/2026-05-22-evening-robots-verification.md`
- Prior library enumeration: `agentic_orchestration/legolas/research/weapon-library-import-2026-05-22/library-enumeration.md`

---

**Signed:** knight-rider (hive-mind orchestrator; Wave-1 fire 2026-05-22)
