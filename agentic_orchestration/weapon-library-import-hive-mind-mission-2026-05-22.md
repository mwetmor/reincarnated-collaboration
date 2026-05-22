# Weapon-Library-Import Hive-Mind Mission — 2026-05-22

**Author:** knight-rider (orchestrator)
**Authority:** Matt 2026-05-22 explicit greenlight; defaults pre-authorized for scoping/sizing/crawling/inserting/committing/pushing
**Status:** ACTIVE — hive-mind firing
**Companion docs:**
- `agentic_orchestration/weapon-library-import-hive-mind-state.md` — live state file (single source of truth)
- `agentic_orchestration/weapon-library-import-orchestration-plan-2026-05-22.md` — gandalf's design substrate (this hive-mind operationalizes one slice of that plan)
- `agentic_orchestration/legolas/research/weapon-library-import-2026-05-22/schema.sql` v1.1.0 — schema

---

## 1. Mission

Populate the loadout SQLite DB at `/Users/admin/Games/reincarnated-loadout/data/telemetry.db` with as many unique weapon entries as can be ethically gathered from publicly accessible sources across all genres (historical, fantasy, sci-fi, modern, mythological, regional/cultural, game-specific), with reference images linked.

**Floor target:** 100,000 unique weapon entries.
**Ceiling target:** 200,000 unique weapon entries.
**Acceptable terminus:** source-exhaustion confirmed by DISCOVERY scout BEFORE floor reached (i.e., the addressable universe of GREEN/GREEN-with-CAUTION sources cannot yield 100K) — at which point we ship what we have with explicit ceiling note.

---

## 2. Scope

### 2.1 In-scope

| Domain | Examples |
|---|---|
| Historical real-world weapons | Bronze Age → modern; all regions; all martial traditions |
| Fantasy weapons | D&D, Tolkien, Warhammer Fantasy, Elder Scrolls, generic fantasy |
| Sci-fi weapons | Star Wars, Star Trek, Warhammer 40K, Halo, Mass Effect, Cyberpunk, generic sci-fi |
| Modern military / firearms | Real-world military, civilian, historical firearms |
| Ancient / mythological | Excalibur, Mjölnir, Gáe Bulg, regional mythological weapons (worldwide) |
| Regional / cultural | Japanese, Chinese, Indian, Middle Eastern, African, Indigenous American, Polynesian, etc. |
| Game-specific catalogues | PoE, OSRS, D&D 5e, Pathfinder, Elden Ring, Dark Souls, Monster Hunter, WoW, FF, Diablo, etc. |

### 2.2 Out-of-scope

| Domain | Reason |
|---|---|
| NSFW / explicit-sexual weapon representations | Editorial floor |
| Joke / parody weapons that are NOT meaningfully unique | Judgment call; "rubber chicken" counts if it appears in a real game; not Internet jokes |
| Real-world WMDs, IEDs, modern terrorist weapon constructions | Editorial floor + legal risk |
| Sources that explicitly Disallow ClaudeBot or anthropic-ai (Discipline #20 RED) | Per `agentic_orchestration/logs/2026-05-22-evening-robots-verification.md` |

---

## 3. Schema commitment

The schema (`schema.sql` v1.1.0) handles the 200K scale natively. SQLite WAL mode is enabled at first writer-connection. Each track writes with `INSERT OR IGNORE` against the canonical merge key (TBD per-source; default: `(source_library, source_id)`). Compound indices already exist on the hot-path query columns. No schema migration needed for scale; if a column gap surfaces, it gets logged in the state file and ratified via Matt-routed amendment.

**Image-storage policy:** URL-only by default per gandalf's commit `7b98231`. Download is a phased-escalation trigger, not a per-import action. `knowledge_entry_reference_images` table records `image_url`, `license_class`, `width_px`, `height_px`, `image_source`; the actual bytes stay remote until a downstream consumer pulls them.

**License-tier policy:** record what we found (all 12 license tiers in `licenses` reference table). Inclusion has NO license filter — we index everything we can ethically access. Commercial-usability is a derived flag (`v_weapons_cc0` view, etc.), not an inclusion filter.

---

## 4. Track inventory

| Track | Owner | Source | Status | Expected yield |
|---|---|---|---|---|
| **A1** | legolas | Wikipedia + Wikidata + Commons (via dumps + SPARQL) | READY | 30K-80K weapon Q-items + reference images |
| **A2** | legolas | Smithsonian Open Access (api.data.gov) | BLOCKED — Matt API key | 3K-10K |
| **A3** | legolas | Royal Armouries (HTTPS crawl with 20s delay) | READY | 1K-5K |
| **B** | legolas | Sketchfab + Kenney + OGA (3D model libraries) | READY | 2K-5K 3D-model attachments (secondary substrate) |
| **G** (NEW) | legolas | GitHub-hosted weapon-data repos (nick-aschenbach/dnd-data, osrsbox-db, all others scout finds) | READY | 2K-10K |
| **E** (NEW) | legolas | Editorial / community sites with geometry+cross-section detail (MyArmoury, Swordis, all others scout finds) | ROBOTS-PENDING | 500-3K (high-quality long-tail) |
| **DISCOVERY** (NEW) | legolas Mode A | Web/social/blog/GitHub search for every viable source | FIRING | N/A — produces source candidates for next-wave tracks |

**Next-wave tracks** spawn from DISCOVERY output. Each new candidate passes:
1. Robots verification (Claude-agent Disallow check + Crawl-delay extraction)
2. License-fit check (any license OK for indexing; commercial-usability derived)
3. Schema-fit check (can normalize to `weapon_knowledge_entries` row)

Sources passing all three become new tracks (e.g., `Track H — Wikidata Lexeme weapon-name etymologies`, `Track I — Wikimedia structured data on Commons`, etc.). I authorize new tracks under default authority unless: (a) significant new dependency (e.g., paid API), (b) significant new schema requirement, (c) source raises ethical/legal flag.

---

## 5. Operational protocol

### 5.1 Discipline #19 compliance (MANDATORY)

- All long-running crawls execute as OS-level processes (`nohup python <script> > <log> 2>&1 &` or `Bash(run_in_background=true)`)
- No sub-agent is in the monitoring chain. Status is on-demand via `sqlite3` one-shot queries against the DB or via reading JSON summary artifacts
- Cross-session continuity is file-based: hive-mind state file + per-track JSON summary artifacts on completion
- Sub-agents fire scripts and return immediately with `(script_path, PID, log_path, expected_wall_time, JSON_summary_path)`

### 5.2 Discipline #20 compliance (PROPOSED, observed as if ratified)

- Every new candidate source passes robots.txt verification BEFORE any fetch
- User-Agent in HTTP calls is `reincarnated-engine/0.1 (research; mhwetmore@gmail.com)` for sources that expect a research-agent UA per their etiquette docs (e.g., Wikimedia, GitHub API)
- For sources that explicitly call out Claude-agent allowance, we use `ClaudeBot/1.0 (research; ...)` — exception requires explicit GREEN signal in robots, not absence of block
- Crawl-delay directives are honored as the minimum interval; we add a 1.5× safety margin
- If a source rate-limits (429) we back off exponentially; sustained 429 → mark AMBER → defer to next wave

### 5.3 Discipline #1 (math-before-code)

- Each track's sub-agent authors a brief math note BEFORE writing the crawl script
- Math note covers: expected yield, runtime estimate, rate-limit budget, failure-mode coverage
- Math note lands at `agentic_orchestration/legolas/research/weapon-library-import-2026-05-22/track-<X>-math-note.md`
- Math notes do NOT require jack-ryan Gate-1 for tracks under default authority (scale + scope are pre-authorized); jack-ryan Gate-1 fires only if a track requires Matt-routed amendment

### 5.4 Write contention

SQLite WAL mode is the per-DB-connection write strategy. Multiple concurrent writers serialize naturally; transaction batches of 50-200 rows keep lock duration small. If contention becomes the bottleneck, fallback architecture is per-track JSONL staging files + periodic consolidator import. Default: direct WAL writes.

### 5.5 Commit cadence

Knight-rider commits the hive-mind state file + new dispatches at natural milestones (per wave fired, per significant count threshold crossed, per new track authorized). Commit messages follow the `docs(knight-rider): ...` convention. Pushes happen at each commit unless Matt directs otherwise.

---

## 6. Success criteria

| # | Criterion | How measured |
|---|---|---|
| C1 | ≥100,000 unique entries in `weapon_knowledge_entries` (the floor) | `SELECT COUNT(*) FROM weapon_knowledge_entries;` |
| C2 | ≤200,000 entries OR all known GREEN sources exhausted | DISCOVERY scout final report |
| C3 | ≥70% of entries have ≥1 reference image URL | `SELECT COUNT(DISTINCT knowledge_entry_id) ...` |
| C4 | License metadata captured for ≥95% of reference images | NULL-rate on `license_class` |
| C5 | Source diversity: ≥10 distinct `source_library` values represented | `SELECT COUNT(DISTINCT source_library) FROM weapon_knowledge_entries;` |
| C6 | Per-source ingest summaries committed as JSON artifacts | `ls agentic_orchestration/legolas/research/weapon-library-import-2026-05-22/summaries/` |
| C7 | Genre coverage validated by spot-check: ≥1 entry from each of {historical, fantasy, sci-fi, modern-firearm, mythological, regional-non-European, game-PoE/OSRS/D&D} | Manual spot-check by Matt at wind-down |

---

## 7. Wind-down conditions

The hive-mind exits ACTIVE state and enters CLOSED state under any of:

| Condition | Action |
|---|---|
| C1 reached AND new-source yield rate < 100 entries/hour for 4 consecutive hours | Auto-wind-down; final summary doc authored; tag fired |
| C2 source-exhaustion confirmed by DISCOVERY scout before C1 | Wind-down with explicit ceiling note; Matt-briefing on what was/wasn't achievable |
| Matt explicit "stop" instruction | Immediate wind-down; preserve all in-flight state for resume-later if desired |
| Resource exhaustion (disk > 80% full; sustained network failures) | Graceful pause; Matt-briefing |
| Schema gap requiring structural amendment | Pause new track fires; flag in state file; resume after gandalf+rocket disposition |

Tag intent on clean wind-down: `v1.0-weapon-library-import-shipped` (Matt-promoted; seam-prefixed during run: `knight-rider/v0.x-weapon-library-import-<wave-n>`).

---

## 8. Authority

| Decision class | Authority | Examples |
|---|---|---|
| Default authority (knight-rider, no sign-off) | Scoping wave size, sizing target sub-ranges, robots verification dispositioning, schema-fit normalization choices, commit timing, push timing | Adding a new GREEN source from DISCOVERY output as a new track |
| Matt-routed amendment | Schema change requiring migration; paid API authorization (Smithsonian key, future Meshy partner-tier); ethical-floor edge cases; Discipline #20 ratification | E.g., commercial use of CC-BY-SA assets; AMBER-source GREEN reclassification |
| Critique-pair escalation (jack-ryan + gandalf) | Cross-seam interface contract changes; decisions-log entries | If schema or pipeline shape changes meaningfully |

---

## 9. Cross-references

### 9.1 Already-authored dispatches (fired in this hive-mind)
- `dispatches/2026-05-22-legolas-track-A-wikipedia-wikidata-commons-dump-consumption.md`
- `dispatches/2026-05-22-legolas-track-A-museum-smithsonian-royal-armouries.md` (A3 portion only; A2 blocked)
- `dispatches/2026-05-22-legolas-track-B-3d-model-imports-sketchfab-kenney-oga.md`

### 9.2 NEW dispatches authored in this hive-mind
- `dispatches/2026-05-22-legolas-DISCOVERY-source-scouting.md`
- `dispatches/2026-05-22-legolas-track-G-github-data-repos.md`
- `dispatches/2026-05-22-legolas-track-E-editorial-content-myarmoury-swordis.md`

### 9.3 Pre-existing references
- `agentic_orchestration/weapon-library-import-orchestration-plan-2026-05-22.md` (gandalf design substrate)
- `agentic_orchestration/legolas/research/weapon-library-import-2026-05-22/schema.sql` v1.1.0
- `agentic_orchestration/logs/2026-05-22-evening-robots-verification.md`
- `~/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md` § 19 (RATIFIED) + § 20 (PROPOSED)

---

**Signed:** knight-rider (hive-mind orchestrator; 2026-05-22 first-wave fire)
