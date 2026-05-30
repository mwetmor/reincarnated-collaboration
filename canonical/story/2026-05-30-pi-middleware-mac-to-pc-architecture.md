# Pi-Middleware Mac↔PC Architecture — Canonical Commitment

> **STATUS:** CURRENT (load-bearing as of 2026-05-30) — architectural commitment for the Reincarnated three-machine development infrastructure. Mac retains content-engine + agent orchestration + design work; PC takes Unreal Engine 5 development (procurement gated); Pi 5 serves as always-on connective tissue (Samba file share + FastAPI HTTP API + PostgreSQL host).
>
> **Composes with:** prior Pi recognition record (Matt 2026-05-25 D1 ratified Pi-Postgres for engine-internal); D4 amendment hosted-Postgres for loadout conditional; D9 LLM cache deferred; execution previously deferred to "right moment." This doc captures that the right moment has arrived (2026-05-30 Epic Games Launcher uninstall + transition to PC for Unreal Engine).

**Date:** 2026-05-30
**Author:** gandalf (story-and-design steward)
**Authority:** Matt 2026-05-30 verbatim — "let's make this canonical" following review of `pi-infrastructure-transition.md` design intent doc + Epic Games Launcher uninstall transition decision
**Companion docs:**
- `pi-infrastructure-transition.md` (root of collab repo) — design intent doc Matt authored 2026-05-30 capturing the Pi-as-connective-tissue decision
- `agentic_orchestration/gandalf/notes/2026-05-30-pi-infrastructure-rollout-per-agent-per-seam-directions.md` — per-agent dispatch instructions + KR orchestrator role
- `agentic_orchestration/gandalf/notes/2026-05-30-physical-infrastructure-implementation-plan.html` — exhaustive implementation plan for Matt + son as physical spec consultants/managers
- `agentic_orchestration/gandalf/notes/2026-05-29-community-substrate-axis-expansion-and-t4-capstone-design-implications.html` — engine analysis bundled with implementation plan
- `agentic_orchestration/gandalf/notes/2026-05-30-engine-state-season-003-flow-diagram.html` — state-of-engine bundled with implementation plan
- `canonical/00-ground-state.md` (will register new CURRENT entry on commit)
- `canonical/38-downstream-delivery-strategy-2026-05-23.md` § D1 — Unreal Engine + PC-first decision (composes; PC-procurement now sequenced)

---

## 0. TL;DR

Three-machine development infrastructure committed:

| Machine | Role | Status |
|---|---|---|
| **Mac (8GB)** | Content engine (Python) + agent orchestration + design work + JSON output generation | EXISTING (current dev machine) |
| **Pi 5 (8GB / 128GB SD)** | Always-on middleware — Samba file share + FastAPI HTTP API + PostgreSQL host | EXISTING (PostgreSQL already running per D1) |
| **PC (specs TBD)** | Unreal Engine 5 development + runtime integration + character creation system | PROCUREMENT GATED — see § 5 |

**Architectural commitment:** Pi is **augmentation, not replacement**. Git+Vercel flow continues for code + canonical docs + loadout app data + design artifacts. Pi handles the new Mac↔PC seam: engine-output artifacts destined for Unreal consumption + persistent PostgreSQL queries + (Phase 2) HTTP API for dynamic queries.

**Phasing:** Phase 1 Samba file share immediate priority (~4-8h focused session); Phase 2 HTTP API triggered by PC + Unreal readiness; Phase 3 SSD migration triggered by SD card capacity/wear thresholds.

**Physical implementation team:** Matt + son (per Matt 2026-05-30 verbatim assignment) — physical spec implementations consultants/managers per the bundled HTML implementation plan.

---

## 1. Architectural commitment

### 1.1 Three-machine separation of concerns

The Reincarnated project has outgrown single-machine development:

- **Content engine** (Python + agent orchestration + design): Mac's strengths — high developer productivity, mature toolchain, agent CLI affordances, Git velocity
- **Game engine development** (Unreal Engine 5): PC's strengths — Windows-native UE5 tooling, RTX-class GPU support for Lumen/Nanite/Niagara, ample RAM for engine work
- **Always-on connective tissue** (file share + DB + future HTTP API): Pi's strengths — low power, always-on, headless, network-resident

Each machine plays to its strengths; the Pi makes the seam between Mac and PC asynchronous and decoupled.

### 1.2 The augmentation-not-replacement principle

The existing data flow (Mac → git → Vercel for loadout app + canonical docs) **continues unchanged**. The Pi adds a parallel data path for content destined for Unreal consumption:

| Content type | Path | Rationale |
|---|---|---|
| Canonical docs + design artifacts + code | Git (collab + engine + loadout repos) | Versioned, distributed, multi-agent friendly; works |
| Loadout app data (class JSONs, manifests) | Git → Vercel | Works; users access via Vercel SPA; no Pi involvement |
| Engine-output artifacts for Unreal consumption | Mac → Pi shared folder (Samba) → PC reads | NEW — Pi's primary role for Phase 1 |
| § 12 hero+gear Meshy artifacts | Mac → Pi shared folder → PC reads (Phase 2) | NEW — composes naturally with Phase 2 Unreal integration |
| PostgreSQL engine-internal data | Pi (already) | D1 ratified 2026-05-25; continues |
| Telemetry from gamora sim | Pi PostgreSQL | Queryable, structured; better than file-based for analytics |
| Research artifacts (legolas) | Git collaboration repo | Markdown + structured data; multi-agent consumption |

The principle: **content takes the route that matches its consumption pattern.** No central Pi monopoly on the project's data.

### 1.3 Three Pi functions (locked)

Per `pi-infrastructure-transition.md` § "The Pi's Specific Role":

**Function 1 — File Sharing (Phase 1):** Samba shared folder at `/home/matt/data/shared` (explicit path; not default `/srv/samba/`). Both Mac and PC mount. Bidirectional file operations.

**Function 2 — HTTP API (Phase 2):** FastAPI service exposing endpoints for dynamic queries from Unreal. Backed by PostgreSQL. Systemd service for auto-start. Triggered by PC + Unreal being live.

**Function 3 — PostgreSQL Host (Already Established):** Continues hosting project's PostgreSQL instance per D1 ratification.

### 1.4 Storage strategy (locked)

- **Initial:** SD card (128GB). Acceptable for weeks. **Backup discipline from day 1 is non-negotiable.**
- **Migration:** USB 3 SSD ($50-100, 500GB-1TB). Triggered by SD card 70-80% full OR write-wear concerns OR 6 months elapsed OR any read/write errors in system logs.
- **Critical:** Use explicit data directories (`/home/matt/data/postgresql`, `/home/matt/data/shared`) from the start. Migration becomes "mount SSD at `/data`, copy, update mount point, restart services."

---

## 2. Composition with existing canon

### 2.1 Composes with prior Pi recognition record (Matt 2026-05-25)

Per `MEMORY.md` → `project_engine_state_findings.md`-adjacent entries:
- D1 RATIFIED: Pi-Postgres for engine-internal (executed)
- D4 amendment: hosted-Postgres for loadout (conditional — defer; loadout-on-Vercel continues)
- D9 DEFERRED: LLM cache (G12 NOT TRIGGERED — defer indefinitely)
- Execution gate: "Matt's right moment"

The right moment is now. This doc operationalizes the deferred execution.

### 2.2 Composes with doc 38 D1 (Unreal Engine + PC-first launch)

Doc 38 D1 commits Unreal Engine 5 + PC/console-first launch + mobile port at +6 months. The Mac cannot run Unreal Engine practically (8GB RAM + install corruption issues per Matt 2026-05-30 transition doc § "Architectural Decision"). PC procurement becomes a doc-38-D1 dependency.

This doc sequences the procurement: Phase 1 + Phase 2 of Pi infrastructure can proceed before PC arrives; Phase 2 HTTP API + PC-side Unreal integration are PC-gated.

### 2.3 Composes with cascade-r4 § 12 hero animation flow

The drax hero+gear extraction → Matt → Meshy → animation URL → drax wire-up workflow has an awkward "URL handoff" step. Once Phase 1 Samba lands: artifacts (or URL refs + cached glTF) can land on Pi shared folder. PC's Unreal in Phase 2 consumes directly. The Pi removes the manual handoff friction.

### 2.4 Composes with Variant C engine-as-general-serial-content-product

Per `canonical/37-engine-and-game-two-products.md` + `canonical/story/engine-as-general-serial-content-product-2026-05-22.md`, the engine produces serial content; the game consumes it. The Pi is the substrate layer that **physically separates production from consumption** — making Variant C's two-product architecture materially deployable across machine boundaries.

---

## 3. Implementation team — Matt + son as physical spec consultants/managers

Per Matt 2026-05-30 verbatim assignment, the physical spec implementations consultants/managers for this infrastructure are **Matt and his son**. The collaborative dynamic between them (per `MEMORY.md` user_role: "collaborates with 11yo son on gameplay concepts and art") extends naturally to physical infrastructure: hands-on hardware assembly, network configuration, Samba debugging, PC procurement decisions.

This is **physical execution territory** — agents (gandalf included) provide written direction, documentation, verification of committed config files, and post-execution review. Actual `apt install`, `smb.conf` authoring, network cable routing, USB drive mounting, PC component selection are Matt + son's seam per ADR-006 external-systems read-only-by-default rule.

The bundled HTML implementation plan (`2026-05-30-physical-infrastructure-implementation-plan.html`) is the load-bearing artifact for their work — exhaustive scope, every hurdle anticipated, every command + config specified, every failure mode + recovery procedure documented.

---

## 4. Knight-rider role expansion

Per Matt 2026-05-30 verbatim assignment, knight-rider takes a **dual role** for this infrastructure rollout:

- **Orchestrator:** routine dispatch sequencing, cross-seam coordination, cycle integration (existing KR seam)
- **Implementations consultant/manager:** practical implementation advice for Matt + son, blocker surfacing, dependency tracking, hardware procurement timing recommendations, process refinement during execution

Per-seam direction lives in `agentic_orchestration/gandalf/notes/2026-05-30-pi-infrastructure-rollout-per-agent-per-seam-directions.md`. KR consumes that doc as orchestration spec.

---

## 5. PC procurement sequencing

PC procurement is **gated separately** but explicitly tracked here:

| Decision | Status |
|---|---|
| **Procure now (parallel with Pi Phase 1)** | RECOMMENDED — Pi Phase 1 has value independent of PC; PC arrival accelerates Pi Phase 2 readiness |
| **Defer PC until Pi Phase 1 closes** | Acceptable; Pi can be tested with Mac-as-sole-client |
| **PC spec floor** | UE5 minimum: 16GB RAM (32GB recommended), 1TB NVMe SSD, RTX 3060+ GPU, modern CPU, DX12 |
| **PC spec target for Reincarnated specifically** | 32GB+ RAM (Lumen + Nanite + Niagara are RAM-hungry), 1TB NVMe SSD, RTX 4070+ GPU, modern CPU |
| **Decision authority** | Matt (hardware budget); HTML implementation plan § 11 captures full discussion |

---

## 6. Phasing commitment

### Phase 1 — Samba file sharing (immediate priority)
- ~4-8h focused execution session
- Mac mounts Pi share; engine-output dir routed
- Backup discipline from day 1 (weekly rsync to Mac local disk minimum)
- Acceptance: engine writes JSON → file appears on Pi → another machine (or Mac itself initially) reads identical content within seconds

### Phase 2 — HTTP API for Unreal (PC-gated)
- ~8-16h execution
- FastAPI + PostgreSQL queries
- Triggered by PC online + Unreal Engine installed + initial integration test scoped
- Acceptance: Unreal makes HTTP request → Pi responds with structured JSON within reasonable latency

### Phase 3 — SSD migration (capacity/wear-triggered)
- ~2-4h execution
- Mount external USB 3 SSD at `/data`
- Move PostgreSQL data + shared folder contents
- Triggered by SD card thresholds OR 6 months elapsed OR I/O errors

### Phase 4 (future) — Backup hardening
- Beyond Day-1 weekly rsync: offsite backup, retention strategy, disaster recovery rehearsal
- Triggered by infrastructure maturity (~3-6 months post Phase 1)

---

## 7. Matt elections — LOCKED 2026-05-30

Per Matt 2026-05-30 verbatim "lock the 5 elections" following gandalf recommendations, all five open elections close at recommended values:

| # | Election | LOCKED decision |
|---|---|---|
| 1 | **Augmentation framing** | ✅ **LOCKED — AUGMENTATION confirmed.** Pi handles Mac↔PC engine-output flow; git+Vercel continues for canonical docs + loadout app + design artifacts. Per § 1.2 table. |
| 2 | **Phase 1 timing** | ✅ **LOCKED — FIRE NOW.** Phase 1 Samba file sharing executes immediately without waiting for PC procurement. Phase 1 has independent value (test infrastructure, build backup discipline, prepare data directory structure). |
| 3 | **Backup target** | ✅ **LOCKED — Mac local rsync as Day-1 minimum.** Weekly rsync of Pi `/home/matt/data` + pg_dump to Mac local disk per HTML implementation plan § 7. Cloud add-on deferred to Phase 4. |
| 4 | **Network resolution** | ✅ **LOCKED — .local mDNS first.** Pi addressable as `reincarnated-pi.local` from Mac (built-in mDNS) and PC (Apple Bonjour Print Services for Windows fallback). Upgrade to static IP via router DHCP reservation only if `.local` proves flaky in practice. |
| 5 | **PC procurement timing** | ✅ **LOCKED — CONCURRENT with Phase 1.** PC procurement fires in parallel with Pi Phase 1 execution. Pi Phase 1 doesn't require PC to validate (Mac alone proves the file share infrastructure). PC arrival accelerates Phase 2 HTTP API readiness when ready. |

**Composition with rollout sequencing:** All 5 elections compose without internal conflict. KR's first-dispatch sequence per per-agent-per-seam doc § 11 operates under these locked decisions; no Matt re-election needed for Phase 1 work-items.

**Amendment authority:** future amendments to these elections require explicit Matt verbatim directive + gandalf canonical doc update. Locked elections are load-bearing for subsequent dispatch authoring.

---

## 8. Risk register

| # | Risk | Mitigation |
|---|---|---|
| R1 | SD card failure → data loss | Day-1 weekly rsync backup to Mac local; non-optional |
| R2 | Samba auth issues across macOS + Windows + Pi | HTML implementation plan § 5 documents canonical SMB3 + smbpasswd workflow |
| R3 | Network unreliability (Pi WiFi flaky) | Wired ethernet recommended over WiFi; HTML plan documents both |
| R4 | Schema mismatch (engine emits new fields; Unreal reader crashes) | Schema version field per emit; Unreal reader checks before parse |
| R5 | Partial file reads (Unreal reads mid-write JSON) | Atomic write pattern (write to `.tmp`, then rename) |
| R6 | PostgreSQL data corruption | Backup; pg_dump nightly to Pi local + weekly rsync to Mac |
| R7 | Pi power loss (network outage) | UPS option for production; manual recovery for dev cycle |
| R8 | PC procurement delays Phase 2 | Phase 1 valuable independent of PC; Phase 2 is PC-gated by design |
| R9 | Static IP setup complexity (DHCP reservation vs Pi-side static) | .local first; static IP upgrade documented in HTML plan |
| R10 | macOS .DS_Store noise in Pi share | smb.conf `veto files` directive documented in HTML plan |

---

## 9. Sign-off

**Authored:** gandalf (story-and-design steward) per Matt 2026-05-30 verbatim "let's make this canonical" following review of `pi-infrastructure-transition.md`.

**For:** the architectural commitment of the Pi-middleware three-machine infrastructure for Reincarnated development. Augmentation-not-replacement principle locked. Phase 1 Samba file sharing immediate priority. Phase 2 HTTP API PC-gated. PC procurement sequenced. Matt + son named as physical spec implementations consultants/managers. Knight-rider expanded to dual orchestrator + implementations-consultant role for this infrastructure rollout.

**Companion artifacts:** MD per-agent direction doc + exhaustive HTML implementation plan + 2 bundled engine analysis HTML docs (community substrate axis expansion + state-of-engine season-003 flow diagram) for drax Vercel deployment as planning suite.

---

**Signed:** gandalf (story-and-design steward)
**For:** Matt's commitment of Pi-middleware Mac↔PC architecture as canonical infrastructure pattern for the Reincarnated project's three-machine development workflow.
