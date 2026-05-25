# Infrastructure: Raspberry Pi 5 + Postgres + (potential) closed-loop player-telemetry pipeline

> **STATUS:** RECOGNITION RECORD 2026-05-25 — architectural commitments DEFERRED per gandalf OP § 3.4 recognition-validate-commit discipline. Decisions enumerated in § 7 are gated on the empirical-evidence criteria in § 8.
>
> **Authored:** 2026-05-25
> **Author:** gandalf (story-and-design steward; Pattern-B sustained dialogue with Matt 2026-05-25)
> **Pattern:** recognition record — captures substantive infrastructure recognition; identifies decision-gates; routes operational specifics to seam owners; does NOT pre-commit to architecture
> **Scope:** infrastructure (operationally star-lord + elrond + drax territory). Gandalf authors the design-level recognition + framing-audit; operational specifics route to seam owners before any execution fires.

---

## 0. Origin

Matt 2026-05-25 surfaced two threads in a single Pattern-B dialogue:

1. **Hardware on hand:** unused Raspberry Pi 5 (Cana Kit starter, 128GB SD, 8GB RAM, case + heatsink + fan)
2. **Operational pain:** recurring SQLite write-contention failures when 2+ Claude API agents concurrently write LLM responses to telemetry DB on Mac mini M2 8GB

Matt's proposed framing: Pi as Postgres host (solves SQLite contention); Pi + Docker + CI/CD across Pi/Mac/GitHub; Pi as autonomous-pipeline runner; Pi + closed-loop player-telemetry pipeline from PC playtests.

This doc captures the substantive recognition + frames the decisions before commitment.

---

## 1. The current pain — accurately diagnosed

### 1.1 SQLite multi-writer contention (acute)

SQLite uses database-level write locking. When concurrent writers (multiple Claude API agents writing LLM responses to telemetry DB) hit simultaneously:
- One writer wins the lock
- Others block, timeout, or fail outright depending on busy-timeout configuration
- WAL mode (`PRAGMA journal_mode=WAL`) buys breathing room (concurrent reads-during-writes) but does NOT solve concurrent writes

**This is architectural, not configuration.** SQLite is by design a single-writer database. Multi-writer workloads (which the team's hive-mind cycles have become) are outside SQLite's design envelope.

### 1.2 Mac mini M2 8GB RAM ceiling (subacute)

8GB RAM is the project's compute floor. Active dev sessions (Claude Code + multiple Agent sub-processes + Python engine work + browser + IDE) routinely approach the ceiling. Kernel panics + OOM kills are recurring. The compute pressure is **real and ongoing**, not theoretical.

### 1.3 What's NOT the problem

- Disk space (telemetry DB is modest)
- Network (LAN is fine)
- Engine performance per se (the engine is fast enough; it's the data-layer + agent-orchestration overhead that bites)
- Python/library compatibility (mature stack)

**Diagnosis routing:** star-lord owns telemetry DB + LLM-call write surface. He should quantify (a) write-contention failure rate over last 2 weeks of cycles and (b) Mac-RAM pressure correlation with failures. **Before any infrastructure commitment fires, this measurement should land.**

---

## 2. Tier 1 — Pi as dedicated Postgres host

### 2.1 Architectural fit

Postgres solves the multi-writer contention via MVCC (multi-version concurrency control). Concurrent writers are first-class; no global write lock. **This is the architecturally correct answer** for multi-agent workloads.

Pi 5 + Postgres 16 is a mature combination. Ubuntu Server 24.04 ARM64 + apt-installed Postgres works without exotic configuration. 8GB RAM is adequate for Postgres + the project's current query volume.

### 2.2 The critical caveat — disk I/O

**Do NOT run Postgres data on the SD card.** Two reasons:

1. **Write-wear failure** — SD cards have limited write cycles (~100k-1M per cell); a busy Postgres data volume burns through endurance in months. SD card dies → DB dies → catastrophic data loss.
2. **I/O throughput** — SD random-write IOPS are ~100-500. Postgres wants 5k-50k IOPS for healthy operation.

**Fix:** Pi 5 supports NVMe via PCIe. Buy official Raspberry Pi M.2 HAT+ (~$15) + small NVMe SSD (256GB-1TB, $30-80). Total additional cost: $50-100. Put `/var/lib/postgresql` on NVMe. Without this step, Tier 1 is fragile.

### 2.3 Backup discipline — also non-negotiable

DB becomes single source of truth for engine state. Mandatory:
- Nightly `pg_dump` to Mac mini local volume
- Weekly `pg_dump` to off-Mac storage (B2/S3/external drive)
- **Test the restore at least once.** Untested backups are theater.

### 2.4 DB unification approach

**One Postgres instance, multiple logical databases** (NOT one giant merged schema):

```
pi5-postgres:
├── reincarnated_telemetry   (engine-internal; star-lord)
├── reincarnated_loadout     (player-facing analytics; star-lord via D9; drax UI consumes)
└── reincarnated_catalogue   (catalogue substrate; elrond — Phase 2 candidate, not Day 1)
```

Logical separation preserved; operational consolidation gained (one backup target, one upgrade cadence, one connection pool to tune).

### 2.5 Migration approach

Migration effort depends heavily on whether engine code uses **SQLAlchemy** (dialect swap + connection string + minor schema-isolation quirks) or **raw sqlite3** calls (more rewriting). **Star-lord must diagnose before commitment.**

Recommended pattern: **dual-write transition** (read-from-both, write-to-both, then cut over) rather than Big Bang. Avoids freeze-window risk.

### 2.6 Hosted-Postgres alternative

If operational appetite is low, **hosted Postgres** (Supabase free tier; Neon free tier; Railway) provides the multi-writer benefit without the hardware-ownership tax. Trade-offs:

| Dimension | Pi-Postgres | Hosted Postgres |
|---|---|---|
| Cost | One-time $50-100 hardware; $0 ongoing | $0 on free tier; $10-25/mo when limits exceeded |
| Operational ownership | Real ops work forever (backups, OS updates, monitoring) | Vendor handles ops |
| Network latency | LAN ~1ms | Internet ~20-100ms |
| Vercel reachability | Hard problem (see § 5) | Trivial |
| Vendor risk | None | Real (free-tier limits, vendor pivots) |
| Privacy | Local-only | Data leaves machine |
| Pi remains useful for | Tier 2/1.5/closed-loop | Tier 2/1.5/closed-loop |

**Honest take:** if Pi-Postgres becomes operational drudgery, hosted-Postgres is the escape hatch. Knowing this in advance lowers the commitment cost.

---

## 3. Tier 2 — Pi as autonomous pipeline runner

### 3.1 Use case

Pi runs engine cycles unattended — substrate refresh, balance-loop iterations, telemetry aggregation, scheduled re-generation passes. Cron + Python scripts + Postgres DB.

### 3.2 Why interesting

Decouples engine throughput from agent session availability. Removes Matt + Claude agents from the routine-execution loop for cycles that don't need design judgment.

### 3.3 Why caveats matter

- **Pi compute is not unlimited** — Postgres + autonomous jobs + query-serving competing for CPU. Bottleneck just moved from Mac mini to Pi.
- **What's truly autonomous?** Balance loops with locked acceptance criteria → fine. LLM-generation cycles → questionable (cost control, drift, need human eyes). Substrate refreshes → fine if criteria tight.
- **Observability cost.** Silent failures are worse than no autonomy. Need: structured logs, failure alerts, dashboards. Operational maturity that doesn't exist today.

### 3.4 Recommended start

ONE narrow autonomous workload with tight acceptance criteria — probably the engine's batch-balance-runner once v1 balance loop stabilizes. Add more after that one demonstrates 2 weeks of reliable unattended operation.

---

## 4. Tier 3 — Closed-loop player-telemetry pipeline (Matt's expanded framing)

### 4.1 Matt's framing (verbatim, 2026-05-25)

> *"this may help to centralize play-testing data from my PC once we pass the JSON packet + LLM/model/rig/animation pipeline there, so that we can set up something like test data telemetry back to the raspberry pi and start actioning it on the mac in real time."*

> *"I am probably getting way ahead of myself. And if I did get that data, I don't even know what decisions I might make with it. The engine will be slow to respond to updates unless I split off the battle sim as a containerized product as well which can be tweaked and pass out altered combat specs as JSON."*

### 4.2 The architectural shape

Three-node closed loop:

```
PC (play surface)                    Pi (data plane)              Mac (design surface)
─────────────────                    ─────────────                ────────────────────
Demo runtime                         Postgres                     Engine
  ↓ player actions                     ↓ telemetry sink              ↓ reads telemetry
JSON packet ──────────────────────→  insert ──────────────────→   pattern analysis
LLM/model/rig                                                       ↓ balance adjust
  pipeline                           Containerized                generate JSON
  ↑                                  battle sim                     spec delta
JSON spec delta ←──────────────────  serves                  ←──── push
  ↑ reload                           tweaked specs
Resume play with new specs           Dashboard
                                     (Matt observes loop)
```

### 4.3 What this would unlock — if it landed

- **Real player-data balance loop** — currently the engine balances against MOCK seasons; closing the loop on REAL playtest data is a meaningful capability jump
- **Live iteration** — Matt's son plays; data flows; Matt tweaks; new specs deploy; son keeps playing with updated balance. Game-design feedback loop measured in minutes, not days.
- **Containerized battle sim as fast-iteration product** — the sim can be re-deployed without redeploying the entire engine; this IS the Docker/CI-CD use case that's worth the operational overhead

### 4.4 Framing-audit — what load-bearing assumptions does this depend on?

Per gandalf OP § 4.1 framing-audit checklist (Pattern A-deep three-question protocol):

**Q1 — What load-bearing assumptions does this depend on?**

| Assumption | Status |
|---|---|
| A demo runtime that produces player telemetry exists | **FALSE** — current `reincarnated-demo` (Pixi.js, browser) does not emit player-action telemetry. Needs instrumentation. |
| The JSON packet + LLM/model/rig/animation pipeline to PC exists | **FALSE** — this pipeline is part of the architecture-validation spike (per ground-state.md § 5; PARTIAL with Sidecar A pulled forward in Cycle 10). Not landed. |
| Telemetry sink + schema designed | **FALSE** — telemetry DB currently captures engine-side data only; player-side schema doesn't exist |
| Battle sim is separable from engine main process | **PARTIALLY TRUE** — sim is in-process today but architecturally clean enough to extract. Real work to containerize. |
| Containerized sim can be tweaked + re-deployed live | **FALSE** — would require API surface design for spec ingestion + hot-reload mechanism |
| Matt knows what decisions to make from the telemetry | **FALSE per Matt's own admission** ("if I did get that data, I don't even know what decisions I might make with it") |
| Player population exists to generate enough telemetry to act on | **PARTIALLY TRUE** — Matt's son is N=1; not enough sample size for statistical balance decisions, but enough for qualitative tuning |

**Q2 — What evidence currently in hand could refute these assumptions?**

The N=1 player population is empirically refuting "enough data to act on" preemptively. Matt's self-flag ("don't even know what decisions I might make") refutes "the analysis loop is ready to consume this data."

**Q3 — Should the framing be refined rather than executed as-framed?**

**YES.** Matt's "probably getting way ahead of myself" is the correct read. The closed-loop pipeline is a multi-phase build where each phase unlocks the next; trying to build all phases simultaneously fights the substrate-led discipline. Better to:

1. Land the prerequisites in order
2. Validate each phase produces useful signal BEFORE building the next
3. Let the empirical signal-quality at each phase decide whether the next phase is worth firing

### 4.5 Sequenced build (if pursued)

| Phase | Prerequisite | Output | Empirical gate to next phase |
|---|---|---|---|
| **A — Telemetry sink** | Pi-Postgres (Tier 1) landed | Schema for `player_action_events` + ingestion endpoint on Pi | Sink can ingest + persist a fake event stream |
| **B — Demo instrumentation** | A landed; demo1 architecture-validation spike complete | Demo emits player-action telemetry (positions, abilities used, deaths, completions) | Real son playtest generates ≥1 hour of useful telemetry |
| **C — Analysis layer** | B landed; ≥10 hours telemetry accumulated | Dashboard on Pi showing key metrics (per-ability usage, encounter difficulty heatmap, completion-vs-death rate by build) | Matt can identify ≥1 concrete balance question he wants answered |
| **D — Containerized battle sim** | C landed AND Matt has a balance question worth iterating fast on | Sim runs in container; API ingests spec; hot-reload supported | Sim responds to a tweak in <30 sec; spec delta deployable to PC in <5 min |
| **E — Closed-loop iteration** | D landed | Full loop active for live-tuning sessions | Measured iteration cadence (game-design questions resolved per hour) |

**Each phase is gated on the prior phase producing useful signal.** Phase A is the only one that needs to land soon (and only IF Tier 1 lands). Phases B-E are progressive unlocks.

### 4.6 What this does NOT mean

- It does NOT mean Docker CI/CD is now urgent. Phase D is the trigger; Phases A-C don't need it.
- It does NOT mean every infrastructure decision blocks on this pipeline. Tier 1 (Postgres host) is worth doing for its own sake (SQLite contention) regardless of whether Phases B-E ever land.
- It does NOT mean Matt should build the demo PC pipeline ahead of the engine. The architecture-validation spike is the prerequisite; it should land first.

---

## 5. Tier 4 — Other Pi uses Matt didn't enumerate

| Item | Recommendation strength | Rationale |
|---|---|---|
| **Tailscale (or similar VPN) across Mac + Pi + you-traveling** | STRONG | Free; ~5 min setup; makes Pi accessible from anywhere securely; PREREQUISITE for Vercel reachability problem (§ 6.1) |
| **MCP server hosting on Pi** | MEDIUM | Offloads MCP processes from stretched Mac; useful once we know which MCPs we actually need; don't preemptively build |
| **LLM response cache (Postgres-backed)** | STRONG IF cache-hit rate is meaningful | Save $$ on repeated LLM calls; star-lord should measure cache-hit potential before committing |
| **Dashboard / monitoring web server** | MEDIUM | Replaces "what's the engine doing right now?" friction with a URL; modest authoring effort; high value once built |
| **Asset pipeline offload (Meshy / CV)** | WEAK | Pi GPU not meaningfully better than Mac M2's for CV; skip unless specific bottleneck surfaces |
| **Off-Mac backup target for repos** | LIGHT | Trivial cron + `git bundle`; small marginal value alongside GitHub remote |

---

## 6. Critical risks

### 6.1 Vercel + Pi-Postgres reachability

Vercel functions (loadout app) need to reach Pi-hosted loadout DB. Options:
- **Tailscale-with-Vercel** — works; needs setup; Vercel functions auth into Tailnet
- **Public Pi endpoint + IP allowlist + auth** — possible; security surface to maintain
- **Keep loadout DB on hosted Postgres** (Supabase/Neon) and consolidate ONLY engine-internal DBs on Pi — pragmatic compromise

**Decision routing:** drax + star-lord must scope this BEFORE Tier 1 fires. The Vercel reachability constraint may push loadout DB to hosted-Postgres regardless of Tier 1 outcome.

### 6.2 Single point of failure

Pi becomes critical infrastructure. NVMe failure / power-supply failure / SD card failure kills the data layer. Backups mitigate but don't eliminate. Question: is Mac mini your fallback DB host if Pi dies? Or do you accept 24-48 hr recovery window?

### 6.3 Postgres-on-ARM gotchas

Mature but not zero. Extensions like `pgvector` (potential future use for substrate vector search) need ARM-compatible builds. Most do; verify per-extension.

### 6.4 Migration coordination

Moving SQLite → Postgres during active development requires either a freeze-window OR dual-write transition. **Star-lord must own this design.** Big Bang migration during a hive-mind cycle would be reckless.

### 6.5 Operational appetite

The Pi-Postgres + NVMe + Tailscale + backup stack is real ops work that demands sporadic attention forever after. Worth it for SQLite-contention win + future autonomous-pipeline future, but eyes-open. Matt's operational appetite is the load-bearing variable — only Matt can assess.

---

## 7. Decisions enumerated (DEFERRED per § 8 empirical gates)

> **AMENDED 2026-05-25 (post-Matt-log-back + clarification dialogue):** D1, D4, D9 status updated. D4 framing clarified per Matt 2026-05-25 dialogue exposing prior framing imprecision (telemetry.db vs hypothetical loadout app DB conflation). See § 7.1 amendment note below + § 7.2 framing-imprecision capture.

| # | Decision | Status | Gating criterion (§ 8) |
|---|---|---|---|
| D1 | Tier 1 — Pi-Postgres host (NVMe HAT mandatory) vs hosted-Postgres vs status-quo | **RATIFIED 2026-05-25 — Pi-Postgres for engine-internal DBs (telemetry + catalogue) at Matt "right moment"; status-quo continues until then with PRAGMA busy_timeout mitigation (P2.5)** | G1 ✓ TRIGGERED both branches |
| D2 | Tier 1 timing — fire in window between Cycle 10 close and Algorithm § 8 implementation, OR defer to post-§-8 | **DEFERRED to Matt "right moment"** (Matt P2a verbatim 2026-05-25) — execution NOT in Cycle 11 scope | G1 ✓ + Matt scheduling |
| D3 | Catalogue DB unification (Phase 2 with telemetry, or separate later) | DEFERRED | G3 |
| D4 | Loadout DB location — **(amended) hypothetical loadout app DB, distinct from telemetry.db** | **AMENDED to DEFERRED CONDITIONAL**: hosted-Postgres recommended ONLY IF a concrete YES-scenario (per § 7.2 below) surfaces in roadmap; for v1.0 + foreseeable use cases, loadout stays static-JSON-bundled and no loadout app DB is needed. Pi-Postgres handles telemetry.db (engine-internal). | G4 + YES-scenario surfacing (new sub-gate) |
| D5 | Tier 2 — Pi as autonomous pipeline runner | DEFERRED | G5 |
| D6 | Tier 3 Phase A — telemetry sink build | DEFERRED | D1 + G6 |
| D7 | Tier 3 Phases B-E — demo instrumentation + analysis + containerized sim + closed-loop | DEFERRED | Sequential; D6 → G7 → G8 → G9 → G10 |
| D8 | Tier 4 — Tailscale (rec STRONG; near-free; can fire independently) | **DEFERRED to Matt 15-min window** (Matt P2a authorized; not in Cycle 11) | G11 (Matt schedule) |
| D9 | Tier 4 — LLM response cache | **DEFERRED — G12 NOT TRIGGERED 2026-05-25** (0.13% repeat rate vs 20% threshold; structural cross-season zero collisions) | G12 ✓ NOT TRIGGERED; re-measure if LLM architecture shifts |
| D10 | Tier 4 — Dashboard / monitoring | DEFERRED | G13 |

### 7.1 Amendment note — D1 / D4 / D9 status update (2026-05-25)

Per Matt 2026-05-25 log-back dialogue + 7-decision capture at `agentic_orchestration/matt-log-back-decisions-2026-05-25.md`:

- **D1 RATIFIED** as Pi-Postgres for engine-internal DBs (telemetry + catalogue) — empirically forced by G1 TRIGGERED on both branches (per-day 11.1% SQLite contention exceeds 5% threshold + 4 kernel panics 2026-05-23 from RAM pressure). Execution timing DEFERRED to Matt "right moment"; status-quo continues with PRAGMA busy_timeout mitigation (P2.5).
- **D4 AMENDED to DEFERRED CONDITIONAL** — see § 7.2 below for full framing-imprecision capture + revised reasoning.
- **D9 status confirmed DEFERRED** — G12 NOT TRIGGERED empirically (0.13% repeat rate vs 20% threshold).
- **D8 status confirmed DEFERRED to Matt 15-min window** — Tailscale install authorized per Matt P2a; can fire independently of D1 execution timing.

### 7.2 D4 framing-imprecision capture (Matt 2026-05-25 surface)

**The conflation that surfaced:** original framing treated "loadout DB" as a single concept. Matt's clarifying question 2026-05-25 ("what is the reason we need the cloud hosted DB for the loadout btw?") exposed that two distinct databases were being conflated:

| DB | Where it lives | Who writes | Who reads | Why it exists | Actual D1 / D4 mapping |
|---|---|---|---|---|---|
| **`telemetry.db`** | `~/Games/reincarnated-loadout/data/telemetry.db` | ENGINE (generation runs, LLM-call logging, balance-loop) | star-lord analysis | Engine-internal telemetry; happens to live in loadout repo path historically | **D1 territory** (engine-internal; Pi-Postgres) |
| **Hypothetical loadout app DB** | Would be server-side, Vercel-reachable | Loadout app (writes) + maybe engine push | Loadout app (reads) | Player-facing live state; does NOT exist yet | **D4 territory** (loadout-facing; hosted IF needed) |

**The original framing** treated D4 as "if Pi-Postgres path → need Tailscale-to-Vercel for loadout" or "if hosted-Postgres path → done." But this assumes the loadout NEEDS a live DB at all — which it currently doesn't (v1.0 is static-JSON-bundled per drax memo § 2.3 + § 2.7).

**The amended framing** treats D4 as a CONDITIONAL decision: hosted-Postgres is needed ONLY IF a concrete YES-scenario surfaces requiring server-side loadout state. Until then, loadout stays static-JSON-bundled and D4 is moot.

**YES-scenarios that would trigger D4 commitment:**

| Scenario | DB needed? | Likelihood at current roadmap shape |
|---|---|---|
| Player-saved loadouts / sharing / comments | YES | LOW — conflicts with established "solo game" design direction |
| Authenticated user accounts + multi-device sync | YES | LOW — out of scope per solo-game framing |
| Earth Self persistence server-side (gacha form library) | YES | DEFERRED far-future per Earth meta-layer scope |
| `/the-work` analytics suite with live aggregation across many seasons | MAYBE | MEDIUM — bundled JSON may suffice depending on aggregation scope |
| Real-time engine→loadout data refresh without rebuild | YES | LOW — deploy-cadence problem isn't acute |

**NO-scenarios (current + foreseeable v1):**

| Scenario | DB needed? |
|---|---|
| Solo player browsing class / build / form data | NO — static JSON suffices |
| Read-only T4 post-mortem display | NO — published comparison data; no writes |
| Static class roster + skill tree display | NO — engine bundles at build |

**Revised D4 recommendation:** stay static-JSON-bundled for loadout indefinitely. Re-engage D4 only when a concrete YES-scenario actually lands in the roadmap. **Do NOT pre-build hosted-Postgres for loadout.**

**Operational simplification this unlocks:**
- ONE database system (Pi-Postgres for engine-internal) instead of two (Pi-Postgres + hosted-Postgres)
- ZERO Vercel reachability problem to solve (because loadout doesn't need a DB)
- ZERO vendor risk / data-leaves-machine concern
- Loadout deploy cadence stays simple (JSON rebuild → Vercel preview/production)

**Implication for Matt's P2a verbatim** (*"We will find the right moment and then build the new raspberry pi server and postgres DB later on to solve. We can get the hosted version later on for the loadout also."*): the second sentence is now CONDITIONAL — hosted-Postgres for loadout fires only if a YES-scenario surfaces. Matt's P2a decision is still good; the framing for the loadout half is just clarified as "if-when-needed" rather than "planned."

---

## 8. Empirical-evidence gating criteria

Per gandalf OP § 3.4 recognition-validate-commit discipline. Each gate is a SPECIFIC EMPIRICAL CRITERION (not time-passage). Decisions are committed when gates resolve.

| Gate | Criterion | Owner | Trigger window |
|---|---|---|---|
| **G1** | star-lord quantifies SQLite write-contention failure rate over last 2 weeks + Mac M2 RAM pressure correlation. If failure rate >5% of cycle ops OR RAM-pressure causally implicated in ≥1 kernel panic → Tier 1 commit triggered. | star-lord | Within Cycle 10 close window |
| **G2** | Cycle 10 closes cleanly; no active cycle blocking infrastructure swap | knight-rider state-file | At Cycle 10 final-tag |
| **G3** | elrond reviews catalogue DB query patterns + schema; assesses whether unification adds value vs operational complexity | elrond | Post-G1 |
| **G4** | drax + star-lord scope Vercel reachability constraint; produces yes/no on Tailscale-to-Vercel viability | drax + star-lord | Pre-Tier-1 fire |
| **G5** | Engine v1 balance loop demonstrates 2 weeks of stable operation under current Mac-mini orchestration; ONE well-bounded workload identified as autonomous-candidate | gamora + jack-ryan | Post-Algorithm § 8 implementation |
| **G6** | Tier 1 landed AND stable for 2 weeks; player-action telemetry schema designed | star-lord | Post-Tier-1 stability |
| **G7** | Demo1 architecture-validation spike completes (current `reincarnated-demo` instrumentable OR Demo1+ exists); ≥1 hour of real son playtest telemetry captured | drax + star-lord | Post-G6 + post-architecture-validation |
| **G8** | Matt can articulate ≥1 concrete balance question worth answering from telemetry | Matt | Post-G7; substrate-led discipline applies — empirical signal-quality at G7 informs G8 |
| **G9** | Containerized sim achieves <30 sec response time to spec tweak + <5 min spec deployment to PC | rocket + gamora + star-lord | Post-G8 |
| **G10** | Closed loop demonstrates measurable game-design iteration cadence (≥1 question resolved per hour of live-tuning session) | Matt + gamora | Post-G9 |
| **G11** | Matt has 15 min spare; Tier 4 Tailscale fires (low cost, can land independently of any other gate) | Matt | Any time |
| **G12** | star-lord measures LLM-call repeat-rate over last 2 weeks; if ≥20% of calls have cacheable identical inputs → cache build triggered | star-lord | Post-G1 |
| **G13** | Tier 1 landed; Matt identifies ≥3 questions he'd answer via dashboard | Matt + gandalf | Post-G1 |

---

## 9. Recommended near-term sequence

**This is a recommendation, not a commitment.** Each step is gated on its prior step + the relevant § 8 gate resolving.

### Step 1 (immediate, no infrastructure work)
**Star-lord measures G1 and G12** — quantify SQLite write-contention failure rate + LLM call repeat rate. This is data-gathering, not engineering. Outputs are dispatches/reports, not infrastructure. **Knight-rider can dispatch this within Cycle 10 close window or Cycle 11 open.**

### Step 2 (parallel, low cost)
**Matt fires G11** — install Tailscale on Mac + Pi (~15 min). Pi remains otherwise idle. Nothing else commits.

### Step 3 (gated on G1)
If G1 resolves to "Tier 1 commit triggered":
- **drax + star-lord resolve G4** (Vercel reachability)
- **Matt decides D1** (Pi-Postgres vs hosted-Postgres vs status-quo) informed by G1 + G4
- **Matt decides D4** (loadout DB location) informed by G4

### Step 4 (gated on D1 = Pi-Postgres committed)
- Buy NVMe HAT + SSD (~$50-100)
- Install Ubuntu Server 24.04 ARM64 on Pi
- Install Postgres 16
- Backup discipline locked BEFORE first cutover
- Star-lord designs dual-write migration

### Step 5 (gated on Tier 1 stability)
Tier 2 / Tier 3 / Tier 4 items evaluated on their own gates as those resolve. **None block on each other.**

---

## 10. What this doc is NOT

- NOT a commitment to Pi-Postgres
- NOT a commitment to closed-loop pipeline
- NOT a commitment to Docker / CI/CD
- NOT operational scoping (that's star-lord + elrond + drax — to be commissioned via knight-rider dispatch when G1 resolves)
- NOT a roadmap entry (the canonical roadmap doesn't yet include infrastructure work; if D1 commits to Pi-Postgres, gandalf authors a roadmap amendment)

It IS:
- A recognition record of the infrastructure architectural surface
- A framing-audit identifying load-bearing assumptions and which are currently FALSE
- An enumeration of decisions + gating empirical criteria
- A near-term sequence recommendation

---

## 11. Cross-references

- `canonical/00-ground-state.md` § 5 — active workstreams (this doc adds a row in § 12 below)
- `canonical/38-downstream-delivery-strategy-2026-05-23.md` — keystone delivery; D9 player-facing analytics is loadout-DB adjacent
- `canonical/37-engine-and-game-two-products.md` — Variant C engine-as-general-product; containerized sim aligns with Variant C philosophy
- `agentic_orchestration/operating-procedures/gandalf.md` § 3.4 (recognition-validate-commit) + § 4.1 (framing-audit checklist) — disciplines applied in this doc
- `~/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md` Discipline #11 (empirical inspection over assumption) + Discipline #18 (methodology-before-execution) — applies to any infrastructure execution that fires

---

## 12. Ground-state amendment proposal

Add to `canonical/00-ground-state.md` § 5 active workstreams:

```
| **Infrastructure: Pi + Postgres + closed-loop (recognition record)** | RECOGNITION 2026-05-25 — recognition doc at `canonical/story/infrastructure-raspberry-pi-postgres-and-closed-loop-pipeline-2026-05-25.md`; 13 decisions D1-D10 deferred per § 8 empirical gates; near-term action = G1 + G12 measurement (star-lord) + G11 Tailscale install (Matt 15 min) | gandalf author; star-lord G1/G12/G6 ownership; elrond G3; drax G4/G7; Matt G8/G11/G13 |
```

(This amendment is authored separately if Matt ratifies the framing in this recognition record. The recognition record itself is the canonical artifact; ground-state addition is the visibility surface.)

---

## 13. Sign-off

**Author:** gandalf (story-and-design steward; Pattern-B sustained dialogue with Matt 2026-05-25)
**Status:** RECOGNITION RECORD — architectural commitments deferred per § 7 + § 8
**Empirical-evidence gates:** 13 enumerated (G1-G13); each names specific owner + trigger window
**Routing:** operational specifics route through star-lord (G1/G12/G6) + elrond (G3) + drax (G4/G7); Matt holds D1-D10 ratification authority
**Next action:** knight-rider dispatch of G1 + G12 measurement to star-lord at next natural seam (post-Cycle-10 close, OR within Cycle 10 close window if scoped as Sidecar)

**Per gandalf OP § 3.4:** recognition NOW; architectural commitments AFTER empirical evidence validates. The recognition record stands as the durable thinking; the gates determine when commitment fires.
