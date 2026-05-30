# Pi-Infrastructure Rollout — Per-Agent-Per-Seam Directions + KR Orchestrator/Consultant Roles

> **STATUS:** CURRENT (operational; load-bearing for Pi Phase 1 rollout) — per-seam dispatch directions for the Pi-middleware infrastructure rollout. Composes with canonical commitment doc + exhaustive HTML implementation plan.
>
> **Authority:** Matt 2026-05-30 verbatim — "explicit directions needed per-agent-per-seam and instructions for knight-rider as orchestrator (and also as implementations consultant/manager)."

**Date:** 2026-05-30
**Author:** gandalf (story-and-design steward)
**Companion docs:**
- `canonical/story/2026-05-30-pi-middleware-mac-to-pc-architecture.md` — canonical commitment record
- `pi-infrastructure-transition.md` — Matt's design intent doc
- `2026-05-30-physical-infrastructure-implementation-plan.html` — exhaustive HTML implementation plan
- `~/Games/reincarnated-engine/output/` — current engine output destination (will route to Pi Phase 1)

---

## 0. TL;DR

| Role | Pi-rollout assignment |
|---|---|
| **knight-rider** | Dual role: orchestrator (dispatch routing, seam coordination, cycle integration) + implementations consultant/manager (advice for Matt + son, blocker surfacing, dependency tracking, hardware procurement timing) |
| **star-lord** | Engine emit-pipeline output_dir configurability (Phase 1) + Pi PostgreSQL connection for telemetry (Phase 2 + 3) |
| **rocket** | Phase 2 generation output_dir configurability (Phase 1) + engine-output schema versioning enforcement |
| **gamora** | Simulation telemetry destination (Phase 1: local; Phase 2: optional Pi PostgreSQL emit) |
| **drax** | Loadout app CONTINUES Vercel; deploy bundled planning HTML suite (3 docs) to a `/planning` route; Phase 2: Unreal-side HTTP client (VaRest plugin) — PC seam handoff documented |
| **galadriel** | Visual artifact destinations (Meshy URLs + CV outputs) route to Pi shared folder Phase 1+ |
| **elrond** | PostgreSQL host on Pi continues per D1; schema-extension dispatches name Pi explicitly; backup discipline ownership |
| **legolas** | Research artifacts CONTINUE git collab repo; no Pi routing change needed |
| **jack-ryan** | Gate-1/Gate-2 review criteria extended to cover Pi-routing dispatches; backup-discipline-from-day-1 enforcement |
| **gandalf** | Canonical doc maintenance; design escalation on architectural questions during rollout |

---

## 1. Knight-rider — orchestrator + implementations consultant/manager

### 1.1 Orchestrator role (existing KR seam — extended scope)

**Routine orchestration responsibilities for Pi infrastructure rollout:**

1. **Phase 1 dispatch sequencing** — sequence the work-items in the HTML implementation plan § 5 (Phase 1 Samba) so seam-owners can act on them coherently. Likely ordering:
   - (a) Matt + son physical setup work (Samba install + smb.conf + user accounts + share creation)
   - (b) Mac-side Samba mount work (testing connection)
   - (c) star-lord output_dir config (read from env var or settings.json)
   - (d) rocket Phase 2 output_dir config (same pattern)
   - (e) Integration test (engine run → file appears on Pi mount → Mac reads back)
   - (f) Backup discipline implementation (rsync script + cron + test restore)

2. **Cross-seam coordination** — when Phase 2 HTTP API fires (PC-gated), coordinate:
   - star-lord (FastAPI service authoring)
   - drax (Unreal-side HTTP client integration)
   - elrond (PostgreSQL query endpoints)
   - jack-ryan (Gate-2 review of HTTP API surface)

3. **Cycle integration** — Pi rollout work composes with Cycle 14 v1.2 + Cycle 15+ work. KR ensures Pi infrastructure tasks land in cycle dispatch queues without disrupting in-flight engine work.

4. **State file maintenance** — append Pi-rollout state to `cycle-14-hive-mind-state.md` (or successor) so cross-session continuity preserves rollout context.

5. **Discipline composition** — apply Disc #41 substrate-led (this is real infrastructure not designer-imposed) + Disc #19 background processes (rsync scripts, FastAPI uvicorn) + Disc #21 no-sleep-recommendations + Disc #22 timezone-agnosticism (rollout is workstream-relative, not time-of-day-relative).

### 1.2 Implementations consultant/manager role (NEW — per Matt 2026-05-30 expansion)

**Per Matt 2026-05-30 verbatim — KR additionally serves Matt + son as implementations consultant/manager.** This is a new responsibility class for KR; not a routine seam expansion. KR is not the implementation owner (Matt + son are); KR is the advisor.

**Concrete responsibilities:**

1. **Practical implementation advice for Matt + son** — when they hit unfamiliar territory (e.g., "do I configure static IP at router level or Pi level?"), KR consumes the HTML implementation plan + canonical docs + responds with pragmatic recommendation grounded in the documentation. KR does NOT execute infrastructure work directly (ADR-006 read-only-by-default external systems); KR advises.

2. **Blocker surfacing** — when Matt + son hit a blocker (e.g., "Samba auth failing from macOS"), KR helps debug at the conceptual level + surfaces canonical-doc references + escalates to other agents if the blocker is in another seam's expertise (e.g., elrond on PostgreSQL).

3. **Dependency tracking** — KR maintains a running checklist of "what depends on what" for the rollout: e.g., "Pi Phase 2 HTTP API requires Pi Phase 1 closed AND PC online AND Unreal installed." When Matt asks "what's blocking what?", KR answers definitively.

4. **Hardware procurement timing recommendations** — when Matt is ready to procure PC or USB SSD, KR consumes the HTML implementation plan § 11 (PC procurement) or § 7 (SSD migration) + provides procurement-window recommendation grounded in current rollout state.

5. **Process refinement during execution** — if rollout reveals that the HTML implementation plan has gaps OR that a step is harder than anticipated, KR surfaces the refinement need to gandalf for plan update. Gandalf authors; KR consumes the updated plan; the loop continues.

6. **Risk surfacing** — when KR observes a deviation from the risk register (canonical doc § 8), KR surfaces to Matt with the mitigation recommendation.

**What KR does NOT do as implementations consultant:**
- Does NOT ssh into Pi to install/configure (per ADR-006 — Matt's seam)
- Does NOT make architectural decisions unilaterally (gandalf design steward seam)
- Does NOT decide hardware budget (Matt's seam)
- Does NOT replace gandalf as design escalation path (KR escalates to gandalf when design question surfaces)

### 1.3 KR's first-action items for Pi rollout

1. **Read** canonical commitment doc + this doc + HTML implementation plan in full
2. **Author** initial dispatch sequence for Phase 1 covering items 1.1.1 (a)-(f) above
3. **Coordinate** with drax on bundled HTML deploy (3 docs to Vercel `/planning` route)
4. **Track** Matt + son's Phase 1 execution session; surface blockers as they appear
5. **Update** `cycle-14-hive-mind-state.md` with Pi rollout state appendix

---

## 2. Star-lord — engine emit-pipeline output_dir configurability

### 2.1 Phase 1 scope (immediate)

**Goal:** make star-lord's emit pipeline output destination configurable so engine outputs can route to Pi shared folder (via macOS mount point) when Pi Phase 1 lands.

**Concrete work:**

1. **Output dir as env var or settings.json field.** Currently `cycle14_wave5_emitter.py` (and other emitters) likely have hardcoded output paths or path resolution via `staging_root`. Refactor to read from:
   - Env var `REINCARNATED_ENGINE_OUTPUT_DIR` (e.g., `/Volumes/data/shared/engine-output/`)
   - Fallback to current default (local `output/` directory)
   - Per-season subdir under output dir (e.g., `/Volumes/data/shared/engine-output/cycle-14-wave-5-season-003/`)

2. **Atomic file write pattern** (per canonical risk register R5). Write to `<filename>.tmp` then `os.rename()`. The rename is atomic from reader perspective. Document the pattern in `MIGRATION.md` under star-lord §v1.70 candidate.

3. **Schema versioning field** — verify every emitted JSON includes `manifest_version` (already present per current wave-close). Pi-routed artifacts inherit the version automatically.

4. **Logging extension** — log destination path explicitly so Pi-routed vs local-routed is visible in star-lord output logs.

5. **Backward compat** — local output continues by default. Pi routing opt-in via env var. No regression for non-Pi workflows.

**Acceptance:**
- Engine run with `REINCARNATED_ENGINE_OUTPUT_DIR=/tmp/pi-test/` writes outputs to `/tmp/pi-test/`
- Engine run without env var writes to existing default location
- Atomic write pattern verified by intentional reader interleave test
- Tag candidate: `star-lord/v1.70-pi-phase1-output-routing-1`

### 2.2 Phase 2 scope (PC-gated)

**Goal:** stand up FastAPI HTTP service on Pi exposing endpoints for Unreal dynamic queries.

**Concrete work:**

1. **FastAPI service author** — Pi-side Python service. Endpoints:
   - `GET /character/{character_id}` — full character JSON
   - `GET /season/{season_id}/characters` — all characters in season
   - `GET /season/{season_id}/manifest` — season manifest
   - `GET /character/{character_id}/skills` — skill tree for character
   - `GET /character/{character_id}/gear` — gear loadout for character

2. **PostgreSQL connection** — Pi-resident PostgreSQL (per D1) accessed via psycopg2 or asyncpg. Read-only role for HTTP service.

3. **systemd service** — service runs as `reincarnated-api.service`. Auto-start on Pi boot. Logs to journald.

4. **Authentication** — LAN-only; no internet exposure. Optional: API token in header (lightweight; not OAuth).

5. **Versioning** — endpoint paths include version prefix (e.g., `/v1/character/...`) for forward compatibility.

**Acceptance:**
- Pi `curl http://pi.local:8000/v1/character/<id>` returns JSON within reasonable latency
- Unreal HTTP client (VaRest plugin per drax § 4.2) successfully fetches character data
- systemd service survives Pi reboot
- Tag candidate: `star-lord/v1.71-pi-phase2-http-api-1`

### 2.3 Disciplines composition for star-lord Pi work

- **Disc #41 substrate-led:** Pi routing is not designer-imposed taxonomy; it's real infrastructure. No discipline tension.
- **Disc #42a framing-audit:** apply at dispatch consumption — verify Pi mount point exists + writable before engine run
- **Disc #19 background processes:** FastAPI uvicorn runs as systemd service; standard pattern
- **Disc #45 vocabulary lock:** use canonical infrastructure vocabulary (Samba, FastAPI, PostgreSQL) — these are industry-standard terms, no project-specific renaming

---

## 3. Rocket — generation seam output destination + schema versioning

### 3.1 Phase 1 scope (immediate)

**Goal:** mirror star-lord's output_dir configurability for Phase 2 kit generation outputs.

**Concrete work:**

1. **Output dir config** — `phase2_kit_candidates.json` + `phase4_archive_insertion.json` + other generation artifacts respect `REINCARNATED_ENGINE_OUTPUT_DIR` env var.

2. **Schema versioning** — verify schema_version field on every generation artifact JSON. Increment on schema changes per existing MIGRATION.md pattern.

3. **Cross-seam contract preserved** — star-lord + rocket share the same output_dir env var. No new contract.

**Acceptance:**
- Phase 2 generation writes to Pi shared folder when env var set
- Schema versioning consistent with star-lord emission
- No regression for local-only workflows

### 3.2 Phase 2 scope (PC-gated)

If FastAPI service queries Phase 2 kit candidates, rocket's emission may need PostgreSQL backing (elrond coordination). Defer until PC + Unreal integration scoped.

---

## 4. Gamora — simulation telemetry destination

### 4.1 Phase 1 scope (immediate)

**Current state:** simulation telemetry currently emits to `telemetry.db` per season directory + various JSON artifacts.

**Pi rollout consideration:** telemetry is write-heavy, query-frequent. Two viable paths:

| Option | Description | Recommendation |
|---|---|---|
| **A. Telemetry stays local SQLite** | No change; telemetry.db on Mac local filesystem | Acceptable Phase 1; preserves current pattern |
| **B. Telemetry to Pi PostgreSQL** | gamora writes telemetry rows to Pi PostgreSQL via psycopg2 | RECOMMENDED Phase 1 if elrond schema-extension ready; better cross-machine queryability for Phase 2 |

**Phase 1 acceptance (Option A path):**
- No telemetry routing change; gamora continues current pattern
- Documentation of Phase 2 migration path captured in MIGRATION.md

**Phase 1 acceptance (Option B path):**
- Telemetry schema extended on Pi PostgreSQL (elrond coordination)
- gamora simulation writes telemetry rows to Pi PostgreSQL
- Backward compat: local telemetry.db option preserved via config flag

### 4.2 Phase 2 scope (PC-gated)

Unreal-side telemetry visualization (if scoped) queries Pi PostgreSQL via HTTP API. Endpoint: `GET /v1/telemetry?season_id=...&filter=...`. Coordinate with drax + star-lord.

---

## 5. Drax — loadout app continues Vercel + bundled HTML planning suite + Phase 2 Unreal HTTP

### 5.1 Phase 1 scope (immediate — HIGH PRIORITY)

**Goal:** deploy the bundled HTML planning suite to Vercel under `/planning` route (or similar). Three HTML docs:

1. **`2026-05-30-physical-infrastructure-implementation-plan.html`** (primary) — the exhaustive implementation plan for Matt + son
2. **`2026-05-29-community-substrate-axis-expansion-and-t4-capstone-design-implications.html`** (bundled — engine analysis substrate)
3. **`2026-05-30-engine-state-season-003-flow-diagram.html`** (bundled — state-of-engine current data)

**Concrete work:**

1. **Copy 3 HTML docs to loadout repo** at `public/planning/` or similar
2. **Add Vite route** — `/planning` (index of 3 docs), `/planning/implementation-plan`, `/planning/engine-analysis`, `/planning/state-of-engine`
3. **Index page** — `/planning/index.html` (or React component) lists the 3 docs with brief descriptions
4. **Cross-link** between the 3 docs (each doc's nav can reference the others)
5. **Push to Vercel** — preview verification then production

**Acceptance:**
- `https://reincarnated-loadout.vercel.app/planning/implementation-plan` loads the HTML doc
- All 3 docs accessible from `/planning` index
- Internal links work
- No regression on existing loadout app routes

### 5.2 Phase 2 scope (PC-gated)

**Goal:** wire up Unreal-side HTTP client to consume Pi FastAPI endpoints.

**Concrete work:**

1. **VaRest plugin install** (Unreal Marketplace; free) — HTTP client for Blueprint/C++
2. **Endpoint integration** — Unreal Blueprint or C++ class consumes Pi FastAPI per star-lord § 2.2 spec
3. **Schema version check** — before parse, validate schema_version field against expected version; error gracefully if mismatch
4. **Caching consideration** — frequently-queried character data cached in Unreal client; invalidation triggered by manifest version change

**This is PC-side work and depends on PC procurement + Unreal install.** Drax's authority extends into Unreal once PC seam comes online.

### 5.3 Disciplines composition for drax Pi work

- **Disc #11 empirical inspection:** verify Pi share is mounted on Mac before assuming Pi-routed content is available
- **Disc #45 vocabulary lock:** use canonical infrastructure vocabulary on Vercel-deployed surfaces
- **D7 AI-tell line:** any LLM-generated content for the Vercel planning surfaces follows templated-substrate-narrow-blanks pattern (this implementation plan is gandalf-authored, not LLM-runtime)

---

## 6. Galadriel — visual artifact destinations route to Pi

### 6.1 Phase 1 scope (when triggered)

**Current state:** galadriel visual artifacts (Meshy URLs, CV pipeline outputs, capture-pipeline screenshots) currently live in collaboration repo or galadriel's local working directories.

**Pi rollout consideration:** when visual artifacts need PC/Unreal consumption (e.g., § 12 hero+gear Meshy → Unreal pipeline), route to Pi shared folder for PC pickup.

**Concrete work:**

1. **Output dir config** — galadriel's artifact emissions respect `REINCARNATED_VISUAL_OUTPUT_DIR` env var (or share `REINCARNATED_ENGINE_OUTPUT_DIR` if scope permits)
2. **Asset naming convention** — include character_id + iteration counter + timestamp per canonical doc § 1.4 file naming guidance
3. **Meshy URL refs** — small JSON files (just URL + metadata) on Pi share; PC's Unreal fetches actual glTF from Meshy URL or cached glTF on Pi

**Acceptance:**
- Visual artifacts written to Pi share with substrate-honest naming
- Meshy URLs queryable by PC from Pi
- § 12 hero+gear flow has clear handoff path from drax (image extraction) → Matt (Meshy load) → galadriel (URL routing to Pi) → drax (Unreal consumption)

### 6.2 Phase 2 scope (PC-gated)

Unreal-side asset import pipeline consumes Meshy URLs from Pi. Coordinate with drax + star-lord.

---

## 7. Elrond — PostgreSQL on Pi continues per D1; backup ownership

### 7.1 Phase 1 scope (immediate)

**Current state:** PostgreSQL on Pi already established per D1 ratification 2026-05-25.

**Concrete work:**

1. **Schema-extension dispatches name Pi explicitly** — when elrond extends a substrate schema (e.g., research.db tables), the dispatch names Pi PostgreSQL as the host
2. **pg_dump backup script** — Pi-side cron that runs `pg_dump` nightly to `/home/matt/data/postgresql-backup/` (or equivalent)
3. **Weekly rsync to Mac** — pg_dump artifacts included in weekly rsync to Mac per canonical doc § 6 backup discipline
4. **Backup test rehearsal** — once Phase 1 closes, verify backup restores via test on a separate database (`reincarnated_test`)

**Acceptance:**
- pg_dump runs nightly without errors
- Backup files present on Pi `/home/matt/data/postgresql-backup/`
- Weekly rsync includes backup files
- Test restore succeeds (data verifiable post-restore)

### 7.2 Phase 2 scope (PC-gated)

If gamora telemetry routes to Pi PostgreSQL per § 4.1 Option B path, elrond owns the telemetry schema extension. Coordinate with gamora + star-lord HTTP API.

### 7.3 Disciplines composition for elrond Pi work

- **Disc #11 empirical inspection:** verify pg_dump runs succeed by inspecting log files weekly
- **Disc #41 substrate-led:** PostgreSQL is industry-standard infrastructure; no taxonomy concern
- **Disc #46 DB anti-materialization:** Pi PostgreSQL queries should stream where possible; don't materialize large result sets in HTTP API responses

---

## 8. Legolas — research artifacts CONTINUE git collab repo

### 8.1 Phase 1 scope (no change)

Legolas research artifacts (markdown findings, mechanisms.csv, statistical analysis docs) are multi-agent-consumed and git-versioned. **No Pi routing needed; no change to legolas workflow.**

Research artifacts live at `agentic_orchestration/research/` — accessible to all agents via git checkout. Future-Matt + future-agents read git history; Pi is for Mac↔PC content artifact handoff, not for design/research artifacts.

### 8.2 If research artifacts ever need PC/Unreal consumption

(Not anticipated for current scope.) Would route through Pi shared folder like other PC-bound artifacts. Defer until empirical trigger.

---

## 9. Jack-ryan — Gate-1/Gate-2 review criteria extended

### 9.1 Phase 1 scope (immediate)

**Goal:** extend Gate-1/Gate-2 review criteria to cover Pi-routing dispatches without inventing new gate categories.

**Concrete work:**

1. **Gate-1 framing-audit (Disc #42a) for Pi-routing dispatches** — verify the Pi routing assumption holds (mount point exists, share writable, network reachable) before dispatch fires
2. **Gate-2 backward-compat check** — verify Pi-routing changes preserve local-only workflows (env var fallback works)
3. **Backup discipline enforcement** — Gate-2 of any Phase 1 closure verifies backup script + cron + test restore landed. **Day-1 backup is non-negotiable per canonical doc § 8 R1.**
4. **Schema versioning enforcement** — Gate-2 verifies emit-pipeline changes include schema_version updates

**Acceptance:**
- Gate-2 dispatches for Pi-routing work include backup-verification line item
- No Phase 1 closure dispatches PASS without backup discipline verified
- Schema version field present on every emitted JSON

### 9.2 Disciplines composition for jack-ryan Pi work

- **Disc #42a framing-audit Q1-Q6** applied at every Pi-routing dispatch consumption
- **Disc #19 background processes** verified for any service that runs as systemd
- **Disc #11 empirical inspection** verified at gate consumption (file presence, service status)

---

## 10. Gandalf — canonical doc maintenance + design escalation

### 10.1 Phase 1 scope (continuous)

**Concrete work:**

1. **Canonical doc maintenance** — update `canonical/story/2026-05-30-pi-middleware-mac-to-pc-architecture.md` if architectural amendments surface during rollout (e.g., if Phase 1 reveals augmentation framing needs refinement)
2. **HTML implementation plan refinement** — if Matt + son hit a hurdle the plan didn't anticipate, gandalf authors the plan update
3. **Design escalation path** — when KR (as consultant) surfaces a design question, gandalf provides the design-side adjudication
4. **Per-agent direction doc update** — this very doc receives amendments as seam-owner directives crystallize during execution

### 10.2 Pattern-B engagement opportunities

If Matt wants a sustained design conversation on infrastructure architecture (e.g., "should we reconsider augmentation vs replacement?"), gandalf engages as Pattern-B per OP § 2.

### 10.3 Disciplines composition for gandalf Pi work

- **Disc #21 no-sleep-recommendations** preserved (Pi rollout doesn't change this discipline)
- **Disc #22 timezone-agnosticism** preserved (Pi rollout is workstream-relative, not time-of-day-relative)
- **Disc #41 substrate-led** preserved (canonical commitments grounded in infrastructure reality)
- **Disc #42a framing-audit** applied to architectural amendments during rollout

---

## 11. KR's first dispatch sequence (recommended)

**For KR to fire immediately upon consumption of this doc:**

| # | Owner | Work-item | Gate |
|---|---|---|---|
| 1 | drax | Deploy bundled HTML planning suite to Vercel `/planning` | jack-ryan Gate-2 verify deploy success |
| 2 | Matt + son | Phase 1 physical setup per HTML implementation plan § 5 | KR consultant role active; surface blockers |
| 3 | star-lord | Engine emit output_dir config extension | jack-ryan Gate-2; backward compat verified |
| 4 | rocket | Generation output_dir config extension | jack-ryan Gate-2; backward compat verified |
| 5 | Matt + son + KR | Phase 1 integration test (engine run → file on Pi → Mac reads back) | KR verifies acceptance criteria |
| 6 | Matt + son + elrond | Backup script + cron + first test restore | jack-ryan Gate-2 enforces backup discipline |
| 7 | KR | Phase 1 closure summary + state file append | gandalf reviews; doc updates if needed |

**Phase 2 sequence (PC-gated):** fires when PC procured + online + Unreal installed.

---

## 12. Open items (carry forward)

1. PC procurement timing — concurrent with Phase 1 (recommended) OR sequential (acceptable)
2. Static IP vs .local mDNS — recommend .local first; upgrade if flaky
3. Backup target — Mac local rsync recommended; cloud add-on Phase 4
4. Telemetry routing path (gamora Option A vs B) — defer to gamora's call during dispatch consumption
5. systemd service config specifics — captured in HTML implementation plan § 6 Phase 2 detail

---

## 13. Sign-off

**Authored:** gandalf (story-and-design steward) per Matt 2026-05-30 verbatim — "explicit directions needed per-agent-per-seam and instructions for knight-rider as orchestrator (and also as implementations consultant/manager)."

**For:** the operational per-agent dispatch directions for the Pi-middleware infrastructure rollout. KR consumes this doc to author Phase 1 dispatch sequence. Each seam-owner consumes the relevant section as their pre-fire substrate. Matt + son consume the HTML implementation plan + this doc as the master execution reference.

**Companion deliverables:**
- Canonical commitment: `canonical/story/2026-05-30-pi-middleware-mac-to-pc-architecture.md`
- Exhaustive HTML implementation plan: `agentic_orchestration/gandalf/notes/2026-05-30-physical-infrastructure-implementation-plan.html` (for drax Vercel deploy)
- 2 bundled HTML docs (engine analysis substrate + state-of-engine flow): both at `agentic_orchestration/gandalf/notes/` (for drax Vercel co-deploy)
