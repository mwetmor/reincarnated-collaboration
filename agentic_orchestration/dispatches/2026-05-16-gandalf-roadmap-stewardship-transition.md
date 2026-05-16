# Commission — gandalf — Roadmap stewardship transition + sequencing call on form-bias-cadence-strategy

**From:** knight-rider (relaying Matt's Day-4 directive)
**To:** gandalf
**Approved by:** Matt at 2026-05-16 Day 4 (explicit pushback on knight-rider's earlier proposal; Matt directed roadmap stewardship to gandalf because "he is the only agent set as generative with the goal of proactively recommending new content during conversations"; explicit reasoning that this couples roadmap to story/design priority)
**Status:** COMPLETE
**Type:** Stewardship transition + first stewardship action
**Output:** Updated `canonical/16-project-roadmap.md` + scheduling call on form-bias-cadence-strategy session

## What this is

Two coupled work items in one dispatch:

### Item A — Take roadmap stewardship ownership

Matt has explicitly assigned **forward-roadmap stewardship to gandalf** as a new responsibility. The split:

- **Gandalf owns roadmap stewardship** — the WHY/WHAT: story/design priority, strategic re-orientation, sequencing recommendations, scope changes. Generative-side ownership couples roadmap to design priority.
- **Knight-rider feeds drift signal** — the IS-vs-IS-STATED gap. Knight-rider tracks in-flight work, surfaces drift to gandalf for design-side reconciliation. Mechanical role; no design authority.

This is a scope expansion of your Tier-A design-steward role into project-management-adjacent territory, motivated by the observation that the FORWARD-LOOKING strategic-priority component genuinely lives in your purview while the IN-FLIGHT-TRACKING component fits knight-rider's coordinator nature.

**Authority profile:** you can recommend roadmap reordering, scope additions, scope removals, and structural reframings (e.g., splitting a track, merging tracks, adding a new track). Recommendations route through Matt for approval via the standard decisions-log Gate-1 flow when they touch locked design positions. Mechanical updates (e.g., flipping a stage from "in-flight" to "complete," updating timeline estimates) you author directly with a brief commit note.

### Item B — Reconcile the 5-day drift (knight-rider's input attached below)

Knight-rider read `canonical/16-project-roadmap.md` (last updated 2026-05-11) and produced a structured drift report. Five-day gap; substantive change. Drift report (verbatim from knight-rider's read):

---

#### A. Stage A2 progress not reflected

| Item | Roadmap status | Actual status |
|---|---|---|
| B10.1 (structure) | ✅ COMPLETE noted | ✅ landed `v1.3-b10-1-structure` |
| B10.2 (pack-proxy) | ✅ COMPLETE noted | ✅ landed `v1.3-b10-2-pack-proxy` |
| **B10.4 (swarm calibration / Option 2)** | NOT in roadmap as item | ✅ Landed `v1.3-b10-4-swarm-calibration`. Convergence binary-search refactor on non-pack WR. Should be added to Stage A2 table. |
| **B14.5 V1 primary loop** | "scope expanded 2026-05-12" — but V1 architecture not described | ✅ Shipped; canonical pattern locked for balance loops |
| **Telemetry tier-1** | NOT mentioned (star-lord seam) | ✅ Schema V2.0; supports B14 multi-band sim work |
| B14 multi-band sim | "in Stage A2 scope" | Not yet started; remains as scoped |

#### B. Structural realignment work — entirely missing from roadmap

The biggest drift category. The roadmap is built around Track A stage-completion. But starting 2026-05-14, a parallel structural realignment workstream emerged that doesn't fit cleanly into any existing track:

- **File 37 (form-bias diagnosis and recovery)** — discovered 2026-05-14; identified humanoid-form bias as structural rather than promptural
- **Catalogue-based form-bias resolution path** — locked 2026-05-16; replaces CV-3D-generation as the primary path
- **Pimen catalogue work** — sample crawl + viability gate + full crawl + curation all completed in last 5 days
- **In-flight substrate inventory + form-bias cadence strategy** (you've been authoring this)
- **Cipher-width decision parked** (canonical-elements thread; Options A/B/C — re-parked under the three-layer-model reframe)

**Structural question for gandalf+Matt:** Does form-bias realignment become its own track (Track E?), or restructure Track A's stage order, or interleave somehow? The current roadmap can't accommodate it.

#### C. Team topology not reflected

Roadmap implicitly assumes 6-entity team. Now 9 entities (gandalf/legolas/elrond added). New workstreams (catalogue work, research, design critique) emerge from the additions. Throughput assumptions may need re-tuning.

#### D. New canonical docs not cross-referenced

The roadmap names files 09, 17, 22, 26-33. New canonical docs since:

- `canonical/37-form-bias-diagnosis-and-recovery.md` (the structural realignment doc)
- `canonical/story/` subdir with 14+ docs (court-of-forms, naming-triad, style-register, engine-balance-stewardship, season-feel-rubric, drift-audit, **pre-llm-substrate-inventory** (just landed), etc.)
- Orchestration docs (`AGENTS.md`, `GOVERNANCE.md`, `REVIEW_PROCESS.md`)

#### E. New locked decisions not reflected in "Closed/locked" section

Per `decisions-log.md` since 2026-05-11:
- View A locked as AOE balance philosophy
- Multi-dimensional divergence framework
- Movement-modeling abstraction limitation named
- B10.2 Two-Gauntlet superseded by Option 2 (canonical pattern)
- Court of Forms canonical
- Enemy visual legibility canonical
- Style register locked (HD-2D-shaped pixel-art)
- Naming triad locked
- research.db retired

#### F. New open decisions not in "Open design decisions" section

- 🔴 Cipher width (4-element vs 7-9-element substrate — re-parked under three-layer-model reframe; resolution lives inside form-bias-cadence-strategy doc)
- 🔴 Foundation layer placement (L1 engine substrate vs L2 Reincarnated cosmology — empirically surfaced via Flag B from rocket pass)
- 🟡 ARPG ↔ Isekai canon push/pull (form-bias-cadence-strategy doc in flight)
- 🟡 D1 rubric humanoid-fantasy screening (Flag A from rocket pass — needs empirical test before D1 pool reconsideration)
- 🟡 Pimen acquisition decisions (cost analysis ready; Matt-level)
- 🟡 Per-season-vocabulary-coupling (α/β/γ) — sibling experiment authored
- 🟡 Multiple-canonical-groupings architecture — sibling experiment authored

#### G. Yellow flags / new open items not in roadmap

- Modifier range 0.09–0.52 vs target 0.85–1.15 (gamora investigation Gate-1-cleared; awaiting launch)
- Tier-1 telemetry coverage ~3% (star-lord investigation; awaiting launch)
- Engineering Discipline #13 (implicit-pillar drift) — held pending form-bias resolution
- Engineering Discipline #14 (internal-vs-generative schema separation) — held pending form-bias resolution

#### H. Stage A7 readiness signals

Roadmap says "Design FULLY RESOLVED 2026-05-12 in file 32 + 33." Still true. But the form-bias realignment may layer NEW requirements onto Stage A7 (e.g., embodiment-axis fields per `embodiment-narrative-layer.md`). Worth gandalf surfacing whether Stage A7 needs scope additions.

---

### What to produce

Per the new stewardship split, you author the updates. Knight-rider does NOT edit `16-project-roadmap.md` directly. Specifically:

1. **Update the roadmap** with the drift items resolved. Add Stage A2 progress notes; add new canonical docs to cross-references; add new locked + open decisions; update team topology references; flag yellow flags.
2. **Add structural framing for the form-bias workstream.** Your call: new track (Track E?), interleaved with Track A, or some other shape. The strategy doc you're about to author informs this — so the roadmap update can name the workstream and reference the strategy doc as the place where the architectural shape gets locked.
3. **Surface Stage A7 scope-addition question** (whether form-bias realignment adds requirements to Stage A7) — your call whether to add a section or just note it.
4. **"Last updated" date** updated to today.

### Item C — Sequencing call: when does form-bias-cadence-strategy session land?

Matt's Day-4 directive: *"Form-bias-cadence-strategy session timing depends on gandalf's roadmap prioritization."*

In the same dispatch (or as a sibling decision), use your fresh roadmap stewardship view to call when `canonical/story/form-bias-cadence-strategy.md` gets its fresh focused session (per `2026-05-16-gandalf-form-bias-cadence-strategy.md` dispatch — 3-4 hours minimum, deferred from this session for fresh-cognition reasons).

Options to consider in your scheduling call:
- **Soon (next session):** strategy doc lands before the catalogue-mapping experiment results return (the experiment authored sibling to your request file will execute when Matt's authorized budget runs); strategy doc absorbs experiment findings retroactively
- **After experiment lands:** strategy doc absorbs experiment findings up front; cleaner integration
- **Other framing you surface:** e.g., specific session conditions that should be met first

Document your scheduling call in the roadmap update so the team knows when to expect the strategy doc.

## What this dispatch does NOT do

- **Doesn't lock any architectural decision.** Roadmap updates that touch locked design positions still route through Matt via knight-rider drafts a decisions-log entry → jack-ryan Gate 1 → Matt approve. Same as the existing flow. The stewardship transition gives you authoring authority on the roadmap doc; design locks are still distributed authority.
- **Doesn't supersede the form-bias-cadence-strategy doc dispatch.** That's a separate piece of work; this dispatch sequences when it happens but doesn't author it.
- **Doesn't supersede knight-rider's drift-signal role.** Knight-rider continues to surface IS-vs-IS-STATED gaps to you proactively; you absorb them into stewardship calls.

## Required reading

- `canonical/16-project-roadmap.md` (the current doc; your starting point)
- This dispatch's drift report (above)
- Your own canonical-story corpus (especially `pre-llm-substrate-inventory.md` which is the most-recently-filed; this is the substrate the strategy doc builds on)
- `canonical/37-form-bias-diagnosis-and-recovery.md` (the structural realignment doc; primary context for the new workstream)
- `agentic_orchestration/CHANGELOG.md` 2026-05-16 entries (team-level events; dispatch-flow discipline; Gate-1 rubric)
- `agentic_orchestration/AGENTS.md` (current 9-entity topology + authority tiers + viability-gate workflow)
- `~/.claude/agents/gandalf.md` (your own definition; stewardship-scope addition lives in this dispatch as commission-level authority pending future update to your agent definition if you want it formal there)

## Acceptance criteria

- [ ] `canonical/16-project-roadmap.md` updated with drift items
- [ ] Structural framing for form-bias workstream surfaced (your call on track structure)
- [ ] "Last updated" date updated
- [ ] Stage A7 scope-addition question surfaced (your judgment on framing)
- [ ] Sequencing call on form-bias-cadence-strategy session timing documented
- [ ] Knight-rider notified at completion with summary of changes + scheduling call

---

## Completion record

**Completed:** 2026-05-16 (Day 4, gandalf session)

**Updates landed in roadmap (`canonical/16-project-roadmap.md`):**
- "Last updated" date refreshed; stewardship lock added at top (gandalf authoring authority codified; knight-rider drift-signal role)
- Status snapshot updated: 9-entity team topology; loadout v0.8; telemetry-tier-1 shipped; Stage A2 ~30% complete
- Stage A2 sub-progress table added (B10.1 / B10.2 / B10.4 / B14.5 V1 / telemetry-tier-1 marked complete with tags)
- Yellow flags section added under Stage A2 (modifier range 0.09–0.52 vs target; tier-1 coverage ~3.4%)
- Stage A7 scope-overlap question surfaced with three reconciliation options and recommendation
- **NEW: Substrate Realignment Workstream section** inserted between Track A and Track B — full framing with workstream-not-track rationale, canonical references, empirical experiments, provisional stages (S1-S4+), HELD engine items, scheduling call, unblock map
- Open design decisions updated: 🔴 cipher width + Foundation layer placement; 🟡 ARPG↔Isekai canon push/pull, D1 rubric humanoid-fantasy screening, Pimen acquisition, per-season vocabulary coupling (α/β/γ), multiple-canonical-groupings architecture
- Closed/locked decisions updated: View A + divergence framework; Court of Forms canonical; Enemy visual legibility; Style register HD-2D pixel-art; Naming triad; research.db retired; Pimen full crawl + viability gate; engine + game two-products framing. Canonical-four lock flagged as "under live re-examination" via Substrate Realignment.
- Doc cross-references restructured: Strategic / Form-bias / Canonical-story (14 entries) / Orchestration / Historical sections

**Structural framing call (form-bias workstream):** Named as **"Substrate Realignment Workstream"** — NOT a new track. Cross-cutting; interleaves with Track A stages. Provisional S1-S4+ stages (cipher migration sequence per staging discipline established in canonical-elements thread re-park). Stage interleaving with Track A locks downstream of form-bias-cadence-strategy doc Q4.

**Stage A7 scope-addition disposition:** Surfaced as open question with three options. **Gandalf recommendation: option (c)** — Stage A7 narrows to NON-embodiment-narrative content; Substrate Realignment workstream owns embodiment-narrative integration. Cleanest seam ownership; resolves at form-bias-cadence-strategy doc Q4 + Matt's Stage A7 scope-lock decision when sequencing activates (~6-12 months out).

**Form-bias-cadence-strategy scheduling call:** **After the catalogue-mapping-and-grouping experiment returns findings.** Reasoning: Q4 has four catalogue-track dependency gates per substrate inventory § 11; drafting Q4 without experiment input would either commit a position prematurely or produce abstracted framework with no operational value. Downstream work blocked by strategy doc is blocked by same experiment findings — waiting does not add critical-path delay. Caveat: if experiment stalls, strategy doc can land with Q4 marked "pending experiment" — Q1/Q2/Q3 + Q4 framework still lands.

**Notes for knight-rider:**
- Roadmap is the new gandalf-authored stewardship surface per Matt's Day-4 directive. Future drift signals from knight-rider feed into gandalf-authored updates rather than knight-rider direct edits.
- The Substrate Realignment workstream section names HELD items that depend on the form-bias-cadence-strategy doc; kit_anchor rename is flagged as a possible early-unblock candidate worth knight-rider judgment.
- Pitch-2026-05-18 reference added in cross-references; engine-generic-meta-structure.md is now the pitch's load-bearing layer-separation doc.
- **In-session message from Matt (mid-stewardship update):** asked whether roadmap needs adjustment to support a new demo with updated engine (elements + isekai form-bias), updated gauntlet battle system **including sequential rooms (B10 V2) and added geometry palette (B11)**, and new 2D catalogue VFX/characters. Gandalf preparing response that recommends a follow-on stewardship pass to add an explicit "Demo Vertical Slice 2" milestone as a sequencing target — captured in next session if Matt confirms direction.
