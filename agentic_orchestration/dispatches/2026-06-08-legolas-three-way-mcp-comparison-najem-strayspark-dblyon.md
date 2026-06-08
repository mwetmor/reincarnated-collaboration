# Dispatch — Legolas Mode A Research: Three-Way Deep Comparison — NAJEMWEHBE vs StraySpark vs db-lyon

**Date:** 2026-06-08
**Author:** gandalf (story-and-design steward)
**Authority:** Matt 2026-06-08 directive following StraySpark pricing-page unreachable + db-lyon BUSL-1.1 license-text rep-audit ("let's explore it with a mindset of removal/replacement later if we can't get in touch. But we should do a more thorough comparison between NAJEMWEHBE and StraySpark and db-lyon first.")
**To:** legolas (researcher / scout; Mode A analytical research)
**Cycle:** Pre-MCP-bridge-spike + pre-WS1-WS5-commissioning research investment; informs three-way adoption decision + migration-cost assessment + Matt licensing-inquiry routing
**Type:** Mode A — analytical research; three-way feature-depth comparison + risk assessment; NOT a new inventory crawl
**Cost budget:** $0 LLM (web fetch + analysis); ~1-2 hr legolas wall-clock
**Critical anchors:**
- `agentic_orchestration/legolas/research/2026-06-08-mcp-workstream-spanning-prior-art/synthesis.md` (PRIOR Part A inventory — three candidates already characterized at uneven depth; this commission equalizes depth)
- `agentic_orchestration/legolas/research/2026-06-07-ue-mcp-prior-art/synthesis.md` (PRIOR first-pass synthesis on NAJEMWEHBE + others)
- `canonical/story/2026-06-07-earth-avatar-cosmograph-creation-moment-architecture.md` (WS1-WS5 workstream needs derive from this architectural commitment + downstream commissions)
- `agentic_orchestration/dispatches/2026-06-07-david-h-ue-remote-control-mcp-bridge-spike.md` (the spike this comparison informs)
- `agentic_orchestration/dispatches/2026-06-07-david-h-earth-avatar-creation-moment-vertical-slice-spike.md` (the vertical-slice spike this comparison's outcomes inform)

---

## 0. TL;DR

Equalize characterization depth across three adoption candidates so Matt + gandalf can make the build-vs-adopt-vs-extend decision on equal evidence. PRIOR Part A inventory characterized **NAJEMWEHBE/unreal-ai-connection** deeply, **StraySpark** at medium depth, **db-lyon/ue-mcp** at light depth. This commission deep-equalizes all three.

Matt's directive: "explore db-lyon with mindset of removal/replacement later if we can't get in touch." Implies the comparison must include **migration cost** as a first-class column — if we adopt db-lyon now and licensing path doesn't materialize, what's the cost to migrate to NAJEMWEHBE (or StraySpark)?

**Deliverable:** structured side-by-side comparison report with explicit recommendation tier-table.

**Timeline:** ~1-2 hr legolas wall-clock as sub-agent invocation.

---

## 1. Three candidates — confirm scope

Compare ONLY these three (do NOT re-survey the ecosystem; that's PRIOR commission's scope):

| # | Name | Maintainer | URL | License | Architecture |
|---|---|---|---|---|---|
| 1 | unreal-ai-connection | NAJEMWEHBE | https://github.com/NAJEMWEHBE/unreal-ai-connection | MIT | C++ plugin + Python TCP bridge (127.0.0.1:18888) |
| 2 | Unreal MCP Server | StraySpark | https://www.strayspark.studio + https://www.fab.com/listings/aa699a85-04b1-4746-a29c-962fc3a78f55 | Commercial (Fab) | C++ plugin + HTTP JSON-RPC (port 13579) |
| 3 | ue-mcp | db-lyon | https://github.com/db-lyon/ue-mcp + https://db-lyon.github.io/ue-mcp/ | BUSL-1.1 (free indiv/edu; paid commercial) | TypeScript/Node.js MCP server + WebSocket JSON-RPC + C++ bridge plugin |

---

## 2. Comparison dimensions — equalize depth across all three

### 2.1 Per-workstream coverage depth (tool-name-granular, not summary-level)

For each workstream, enumerate **specific tool names** each candidate exposes that fit the workstream need. Don't report "partial" / "covered" — name the actual tools.

**WS1 — Data layer port (engine → UE):**
- Batch asset import (mesh, texture, material from external file system / JSON)
- DataTable manipulation (CRUD on rows; structure/schema definition; programmatic editing)
- Asset Registry queries (asset lookup, dependency walking, reference resolution)
- Build configuration scripting (per-platform config; cook target switching)
- Engine JSON ingestion (consuming the cosmograph-pivot kit corpus packet)

**WS2 — Rendering layer (Niagara VFX, materials, lighting):**
- Niagara authoring patterns (emitter creation; module configuration; bound-parameter exposure; HTTP-driven parameter iteration)
- Material instance management (parameter set, parent material swap, dynamic instance creation)
- LOD setup (mesh LOD chain; material LOD; HLOD)
- Lumen / Lighting config (Lumen scene config; Reflection Capture; Sky Light)
- Per-skill VFX asset selection patterns

**WS3 — Materialization cinematic:**
- Sequencer track types (camera cut, audio, visibility, transform, event, subscene, MRQ render)
- Camera animation (CineCamera Actor; FOV/focus animation; camera shake)
- Audio cueing (Sound Cue trigger; Wwise integration if relevant)
- Cinematic trigger logic
- **CRITICAL gap-check:** PRIOR synthesis flagged "5 of NAJEMWEHBE's 9 Sequencer tool names unverified" — verify the unverified tools by source-code dive (`grep` for tool registration in repo). Same depth check for StraySpark's 12 Sequencer tools and db-lyon's Sequencer coverage (in Animation category per prior inventory; verify enumeration).

**WS4 — Continuity / save-load:**
- Confirm all three exclude (runtime game concern; not editor concern)
- If any candidate exposes save-game tooling, surface as differentiator

**WS5 — Mobile polish:**
- Mobile preview launch (mobile preview PIE; Android/iOS specific)
- Platform-specific build settings (per-platform .ini overrides; device-profile management)
- Perf profiling triggers (Insights / Trace start/stop; stat capture)

**General iteration + gameplay code authoring:**
- PIE start / stop / pause
- Log file tailing (Output Log capture; category filtering)
- Hot-reload (Live Coding; C++ recompile; Blueprint reinstancing)
- Breakpoint manipulation (Blueprint debugger; C++ debugger bridge)
- **Blueprint editing at property/compile/inspect tier** (not complex node-graph CRUD): reading Blueprint variables; triggering compilation; setting exposed properties; inspecting Blueprint structure; reading event graph (read-only)
- Console command execution
- Asset save / auto-save (StraySpark notable here per prior — "Editor does not auto-save" was flagged as remiphilippe limitation; check three-way)

### 2.2 Architecture comparison

| Dimension | NAJEMWEHBE | StraySpark | db-lyon |
|---|---|---|---|
| Transport layer | (fill) | (fill) | (fill) |
| Port + protocol | (fill) | (fill) | (fill) |
| SSH-remote topology fit | (fill) | (fill) | (fill) |
| Install burden | (fill) | (fill) | (fill) |
| C++ plugin build required? | (fill) | (fill) | (fill) |
| External runtime dependency? | (fill) | (fill) | (fill) |
| Latency characteristics | (fill if documented) | (fill) | (fill) |
| Reliability under load | (fill if documented) | (fill) | (fill) |
| Crash recovery / state reset | (fill) | (fill) | (fill) |

**SSH-remote topology critical:** mantis is a PC-resident Claude Code agent invoked via SSH from Mac. The MCP bridge must work over this topology. Assess each candidate's compatibility with SSH-tunneled local-TCP forwarding.

### 2.3 Engineering quality

| Dimension | NAJEMWEHBE | StraySpark | db-lyon |
|---|---|---|---|
| Test suite (count + framework) | 607 pytest + CI per prior | (verify) | (verify) |
| Smoke test against live editor | Yes per prior | (verify) | (verify) |
| Documentation completeness | (fill) | (fill) | (fill) |
| Tool registration patterns (consistency / discoverability) | (fill) | (fill) | (fill) |
| Error handling discipline | (fill) | (fill) | (fill) |
| Logging discipline | (fill) | (fill) | (fill) |

### 2.4 Production-readiness traits

| Dimension | NAJEMWEHBE | StraySpark | db-lyon |
|---|---|---|---|
| Auth (bearer token / scope gates / etc) | (fill) | Bearer-token + origin allow-list + Read/Scene/Destructive scope gates per prior | (fill) |
| Transaction safety / undo support | (fill) | Every mutating action is first-class UE editor transaction per prior | (fill) |
| Idempotency / retry safety | (fill) | (fill) | (fill) |
| Editor-thread dispatch safety | (fill) | Game-thread dispatch per prior | (fill) |
| Multi-version iteration history | v0.9.1 May 2026; ongoing | v1 207 tools → v2 305 → v3 359 per prior | v1.0.79 June 6 2026; ongoing |
| Auto-save behavior | (fill) | (fill) | (fill) |

### 2.5 Maintainer + community signals

| Dimension | NAJEMWEHBE | StraySpark | db-lyon |
|---|---|---|---|
| Maintainer (org / individual) | HD Media (Kuwait) per prior | StraySpark Studio (commercial entity) | David Bingham (individual; per LICENSE) |
| Recent activity (last 30 days) | (fill) | (fill) | (fill) |
| Star/fork count | 6 / 3 per prior | N/A (Fab commercial) | 125 / 29 per prior |
| Issue tracker activity | (fill) | Forum activity per prior | (fill) |
| Response to user issues | (fill) | (fill — forum thread for signal) | (fill) |
| Sponsorship / commercial backing | None per prior | Studio is commercial; revenue from licensing | None publicly visible |
| Project orphan-risk signal | High (single low-star maintainer) | Low (commercial entity with revenue motive) | Medium (active solo maintainer; recent ramp) |

### 2.6 License + commercial path

| Dimension | NAJEMWEHBE | StraySpark | db-lyon |
|---|---|---|---|
| License type | MIT | Commercial via Fab.com listing | BUSL-1.1 |
| Cost during dev | $0 | Pre-purchase needed? Verify free trial / eval terms | $0 (under non-production-use base grant) |
| Cost at commercial release | $0 | Per Fab listing terms (unknown — page 403'd) | Per db-lyon commercial license inquiry (website unreachable per Matt 2026-06-08) |
| Lock-in risk profile | None (MIT permanent) | Per-Fab-listing terms; perpetual vs subscription unknown | High during pre-pricing (BUSL terms set unilaterally by Licensor) |
| Migration cost if license path closes | N/A (no migration ever needed) | Unknown until pricing known | KEY DIMENSION — see § 2.7 |

### 2.7 Migration cost — db-lyon → NAJEMWEHBE (or → StraySpark)

**This is the critical column per Matt 2026-06-08 directive.** If Matt adopts db-lyon now and licensing path doesn't materialize (Licensor unreachable; pricing unacceptable; or terms-change), what's the migration cost to NAJEMWEHBE or StraySpark?

Estimate per dimension:

| Migration dimension | Estimated cost |
|---|---|
| Tool-call site count (~how many places does Reincarnated dev pipeline invoke MCP tools?) | TBD per dev-pipeline state |
| Tool-name compatibility (do the three implementations share tool names / signatures?) | Compare per § 2.1 enumeration |
| Architecture compatibility (TypeScript vs Python bridge — does mantis client code change?) | NAJEMWEHBE = Python; StraySpark = HTTP; db-lyon = TypeScript/Node — three different transports |
| Capability gap if migrating (any db-lyon capability NOT in NAJEMWEHBE/StraySpark?) | Compare per § 2.1 enumeration |
| Behavioral difference (same tool but different semantics; e.g., transaction-wrapped vs not) | Surface per candidate-pair |
| Install / setup re-burden | Compare per § 2.2 install burden row |

**Recommendation shape:** quantify migration cost as one of (LOW / MEDIUM / HIGH / BLOCKING) with rationale, per migration pair (db-lyon → NAJEMWEHBE; db-lyon → StraySpark).

### 2.8 Extension cost — NAJEMWEHBE base + named gap-fills

If posture is ADOPT-AND-EXTEND with NAJEMWEHBE as base, what's the work to fill identified gaps?

| Gap | Estimated extension cost (LOW / MEDIUM / HIGH) | Rationale |
|---|---|---|
| DataTable CRUD depth (NAJEMWEHBE has 2 tools per prior; needs more) | (fill) | (fill) |
| Sequencer depth (NAJEMWEHBE has 9 tools; 5 unverified per prior; check completeness) | (fill) | (fill) |
| Niagara HTTP authoring (NAJEMWEHBE has 3 tools — adequate? gap?) | (fill) | (fill) |
| SSH-remote topology validation (no documented SSH usage; needs proof) | (fill) | (fill) |
| Auth / scope gates (if production-readiness needed; not present in NAJEMWEHBE) | (fill) | (fill) |
| Transaction safety / undo (not present in NAJEMWEHBE per inventory) | (fill) | (fill) |

---

## 3. Comparison output structure

Synthesis at `agentic_orchestration/legolas/research/2026-06-08-three-way-mcp-comparison/synthesis.md`.

Required structure:

- **TL;DR** (1 paragraph: which candidate per posture, with confidence + rationale)
- **§ 1 Per-workstream coverage matrix** (tool-name-granular, three columns)
- **§ 2 Architecture comparison table** (per § 2.2 dimensions)
- **§ 3 Engineering quality + maintainer + production-readiness comparison** (per § 2.3 + § 2.4 + § 2.5 dimensions)
- **§ 4 License + commercial path comparison** (per § 2.6 dimensions; flag db-lyon Licensor-unreachable per Matt 2026-06-08 finding)
- **§ 5 Migration cost assessment** (per § 2.7 dimensions; LOW / MEDIUM / HIGH / BLOCKING per migration pair)
- **§ 6 Extension cost assessment** (per § 2.8 dimensions for NAJEMWEHBE-base posture)
- **§ 7 Recommendation tier table** (per posture: ADOPT-OUTRIGHT / ADOPT-AND-EXTEND / EVAL-THEN-MIGRATE / DEFER)
- **§ 8 Open questions for gandalf review** (anything legolas surfaces that requires gandalf judgment)
- **Sign-off**

Estimated length: 5-8 pages markdown.

---

## 4. Methodology

Standard Mode A pattern per legolas OP:
- Source-code-level inspection of three repos (NAJEMWEHBE + db-lyon are open source; StraySpark public docs only)
- Tool-name enumeration via repo `grep` patterns (search for MCP tool registration sites)
- Cross-reference WS1-WS5 needs to discovered tools per candidate
- Architecture + engineering-quality assessment from repo structure + tests + docs
- License terms confirmed (NAJEMWEHBE MIT confirmed prior; StraySpark Fab listing public; db-lyon BUSL-1.1 LICENSE confirmed prior at https://github.com/db-lyon/ue-mcp/blob/main/LICENSE)
- Migration cost reasoning from tool-name + tool-signature comparison

**Discipline #25 rep-audit MANDATORY** on:
- Tool count claims per candidate
- Sequencer coverage depth (PRIOR synthesis flagged 5/9 NAJEMWEHBE Sequencer tools unverified — verify by source)
- StraySpark "359 tools / 50+ categories" claim verification at deeper depth than prior
- db-lyon "569+ actions" claim verification at deeper depth than prior

**Out of scope:**
- Don't re-survey the ecosystem (PRIOR commission did that)
- Don't deep-dive UE Remote Control API docs (mantis spike work)
- Don't attempt commercial inquiry (Matt will handle Fab / licensing@ue-mcp.com routing)
- Don't try to BUILD anything — research only

---

## 5. Verdict shapes for recommendation tier

| Tier | Trigger | Action |
|---|---|---|
| **ADOPT-OUTRIGHT (StraySpark)** | StraySpark covers WS1-WS5 + general iteration at production-grade quality with auth + transaction safety; license pricing turns out reasonable per future Matt-led inquiry | MCP bridge spike pivots to evaluation + adoption |
| **ADOPT-AND-EXTEND (NAJEMWEHBE)** | NAJEMWEHBE covers ~70-80% with named identifiable gaps; extension cost LOW-to-MEDIUM; no license risk | MCP bridge spike pivots to NAJEMWEHBE evaluation + gap-fill scope |
| **EVAL-THEN-MIGRATE (db-lyon now; NAJEMWEHBE if license closes)** | db-lyon offers strongest breadth at zero immediate license risk during dev; migration cost to NAJEMWEHBE is LOW; Licensor-unreachable means migration MUST be planned for | Use db-lyon during eval / dev pre-commercial-deployment; plan for NAJEMWEHBE migration if commercial-license inquiry fails or terms unacceptable |
| **EVAL-MULTIPLE-DEFER** | All three have material gaps; deeper info needed | Use NAJEMWEHBE during initial spike; defer commitment until vertical-slice spike surfaces empirical evidence |

---

## 6. Anti-patterns

- **Don't redo the ecosystem inventory.** PRIOR commission characterized 17 implementations; this commission narrows to three. The narrowing IS the work.
- **Don't enumerate at category-summary level.** "Sequencer: 12 tools" is what PRIOR did. This commission asks: WHICH 12, do they cover camera cuts + audio tracks + visibility tracks + transform tracks + MRQ render? Tool-name level.
- **Don't auto-trust README claims.** Rep-audit per § 4 mandatory for tool counts at all three.
- **Don't recommend posture without explicit cost reasoning.** ADOPT-AND-EXTEND vs EVAL-THEN-MIGRATE depends on quantified extension cost vs migration cost. Show the math, not just the verdict.
- **Don't editorialize about license morality.** Just report what each license allows and what migration costs if license path closes. Matt + gandalf make the strategic call.

---

## 7. Sign-off

**Authored:** gandalf 2026-06-08 per Matt 2026-06-08 directive "let's explore it with a mindset of removal/replacement later if we can't get in touch. But we should do a more thorough comparison between NAJEMWEHBE and StraySpark and db-lyon first."

**Authority:** gandalf cross-cutting research-commission authority for Mode A analytical research informing adoption-decision evidence; equalization of characterization depth across three known candidates.

**Routing:** legolas executes Mode A sub-agent invocation immediately upon dispatch reaching legolas; returns synthesis findings inline + writes deliverable to disk path per § 3.

**Empirical-evidence trigger for adoption decision:** legolas comparison output per § 5 verdict tier — gandalf reviews with Matt; Matt routes commercial inquiries (Fab StraySpark pricing; licensing@ue-mcp.com db-lyon pricing); MCP bridge spike commission amended per locked posture.

**Composition with prior commissions:** EXTENDS the 2026-06-08 workstream-spanning inventory commission. NOT a replacement; the inventory's broad-scope verdict (ADOPT-AND-EXTEND with NAJEMWEHBE; StraySpark commercial alternative; db-lyon BUSL-1.1 third option) is provisional pending this commission's deeper three-way assessment.

**End of dispatch.**
