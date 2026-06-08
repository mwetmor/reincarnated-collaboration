# Next-Session Plan — Design Recognition Capture + MCP Workstream-Spanning Research

**STATUS:** CURRENT (next-session plan; load-bearing for next gandalf invocation)
**Date:** 2026-06-08
**Author:** gandalf (story-and-design steward)
**Authority:** Matt 2026-06-07 design contribution + ratification "Please write both of these (legolas and design recognition) into tomorrow's session. Then let's wind down."
**Companion docs:**
- `canonical/story/2026-06-07-earth-avatar-cosmograph-creation-moment-architecture.md` (d3ced92 — foundational architectural commitment this session's design contribution amends)
- `canonical/story/2026-06-07-cosmograph-cross-surface-LOD-architecture.md` (cross-surface LOD vocabulary lock)
- `canonical/story/2026-06-05-cosmograph-pivot.md` § 9 (primitive-as-star + kit-as-constellation substrate lock)
- `agentic_orchestration/dispatches/2026-06-07-david-h-earth-avatar-creation-moment-vertical-slice-spike.md` (vertical-slice spike commission; design contribution will inform amendments)
- `agentic_orchestration/dispatches/2026-06-07-legolas-ue-mcp-prior-art-research.md` (first legolas MCP research; commission and synthesis at 32e34db)
- `agentic_orchestration/legolas/research/2026-06-07-ue-mcp-prior-art/synthesis.md` (legolas synthesis; REFERENCE+BUILD verdict)

---

## 0. TL;DR

Two tasks for next gandalf session. Both authored efficiently; both fire without sustained design dialogue. Substantive canonical amendments + Pattern B dialogue questions deferred to subsequent sessions per recognition-validate-commit discipline.

**Task 1 — Author Option A legolas commission (workstream-spanning MCP scope research)** and fire as sub-agent immediately. ~15 min author + ~1-2 hr legolas autonomous execution. Output informs MCP bridge spike re-scoping AND vertical-slice spike execution pattern.

**Task 2 — Author design recognition record capturing Matt + son design contribution from 2026-06-07.** ~30-45 min gandalf authoring. Preserves design content while fresh; flags amendments for subsequent canonical work; queues clarification questions for Pattern B dialogue.

---

## 1. Task 1 — Fire Option A legolas commission

### 1.1 Context

First legolas MCP research commission (2026-06-07 commit 32e34db) was creation-moment-scoped. Matt surfaced the scoping gap; ratified Option A (comprehensive workstream-spanning MCP scope research) before winding down.

### 1.2 Commission scope to author

Path: `agentic_orchestration/dispatches/2026-06-08-legolas-ue-mcp-workstream-spanning-prior-art.md`

Six research questions covering MCP-tool-coverage requirements per workstream:

1. **WS1 (data layer port) MCP needs:** batch asset import; DataTable manipulation; Asset Registry queries; build configuration; engine JSON ingestion pipeline integration
2. **WS2 (rendering layer) MCP needs:** Niagara authoring patterns (HTTP + C++/Blueprint scope); Material instance management; LOD setup; Lumen/Lighting config
3. **WS3 (materialization cinematic) MCP needs:** Sequencer manipulation (cinematics); camera animation; audio cueing
4. **WS4 (continuity / save-load) MCP needs:** Save game systems; asset persistence patterns (mostly runtime; less MCP-relevant)
5. **WS5 (mobile polish) MCP needs:** Mobile preview launch; platform-specific build settings; perf profiling triggers
6. **General iteration + gameplay code authoring MCP needs:** PIE start/stop; log file tailing; hot-reload; breakpoint manipulation; Blueprint editing (lasso input handlers, ingredient drag-drop, materialization cinematic triggers, tablet drawing input handler per design contribution § 2.5 below)

Reference baseline: first legolas commission verdict REFERENCE+BUILD. Three existing UE-MCP implementations identified (chongdashu/unreal-mcp; remiphilippe/mcp-unreal; NAJEMWEHBE/unreal-ai-connection). Workstream-spanning research evaluates whether these cover broader workstream needs OR if MCP bridge spike scope expands beyond Remote Control HTTP MVP.

### 1.3 Deliverable

Synthesis at `agentic_orchestration/legolas/research/2026-06-08-mcp-workstream-spanning-prior-art/synthesis.md`.

Structure: TL;DR + per-question findings (Q1-Q6) with citations + recommendations for MCP bridge spike scope expansion + Blueprint editing scope decision revisit (legolas first commission recommended scope OUT for creation moment; workstream-spanning evaluation may revise) + open questions for gandalf consideration + sign-off.

### 1.4 Execution

Author commission (~15 min) → commit + push (per cycle pattern) → invoke legolas as sub-agent immediately → legolas runs ~1-2 hr autonomous → synthesis lands + brief inline summary returned to gandalf.

### 1.5 What it informs downstream

- MCP bridge spike commission amendments (may add tools beyond Remote Control HTTP MVP; may revise Blueprint editing scope-out)
- Vertical-slice spike execution pattern (informed by MCP bridge expected capabilities)
- WS1-WS5 commission scoping (tooling-aware vs tooling-naive)
- Productionization scope estimate if MCP bridge spike returns GREEN

---

## 2. Task 2 — Author design recognition record

### 2.1 Context

Matt + son 2026-06-07 design contribution substantively elaborates the Earth-Avatar Creation Moment architecture (locked at d3ced92 earlier same day). Multiple substantive elements added; substantial canonical amendments implied but deferred per recognition-validate-commit discipline. Recognition record preserves design content while fresh.

### 2.2 Recognition record path

`canonical/story/2026-06-08-creation-moment-design-additions-recognition-record.md`

Format per `reincarnated-canonical-doc-format` skill recognition record special case: STATUS stamp + Date + Author + Authority + Companion docs header + explicit "Recognition Record — architectural commitments deferred per § X" framing + empirical-evidence criteria for re-engagement + sign-off.

### 2.3 Five design elements to capture

**Element 1: Earth-self creation moment is EARLIER (Q4 RESOLVED)**

Matt verbatim 2026-06-07: "the character creation for the earth self to have been earlier" + "the spirit form selected from the constellation should retain the earth-self's face/body traits. This is the definition of reincarnation."

- Earth-self pre-scene EXISTS (Q4 from Earth-avatar canonical § 4.4 RESOLVED)
- Player composes Earth-self identity (name, face, body) BEFORE the grassy knoll spirit-selection scene
- Spirit form COMPOSITION RULE: retains earth-self face/body + acquires kit identity (element, archetype, weapon, etc.) — literal reincarnation mechanic at visual-identity layer
- Implication: Earth Self meta-layer anchor STRONGER than canonical d3ced92 already captured; reincarnation mechanic locks at visual-identity layer not just narrative layer

**Element 2: Scene element — hill-climb + spirit materialization + sky transition**

Matt verbatim: "When you reach the top of the grassy knoll, a nearly insivible spirit form materializes next to you, and the sky turns from day to night (not the ground, but just above the horizon and above turns to night)."

- Walking to top of grassy knoll = trigger for creation moment proper
- Spirit form materializes (nearly invisible at first; becomes more present as composition progresses)
- Sky transitions day → night ABOVE HORIZON only (ground stays day-lit)
- Cinematic transition lands player in creation moment with appropriate gravitas
- Genre precedent: Sky: Children of the Light + Outer Wilds (sky transitions narratively); FFXIV story moments (partial-sky-transitions for liminal-space framing)

**Element 3: iPad/tablet as Path I diegetic input device**

Matt verbatim: "in addition to the spirit lasso, the earth self should have an actual tablet/ipad. On the ipad, the player will draw the icons representing the primitives they would like to add/change within their selected spirit form."

- Path I refinement: REPLACES generic "drag-and-drop primitive tokens" with "diegetic in-fiction tablet device on which player draws icons for primitives"
- Drawing-based input that's tactile but doesn't require artistic skill (per Matt's mobile-Claude conversation snippet)
- Earth-self holds an actual tablet in-world — diegetic UI surface
- Genre precedent: Death Stranding (in-fiction tablet for Sam's interface); Persona 5 (in-fiction tools as UI surfaces); various sci-fi-themed games using diegetic tools

**Element 4: Two-layer cosmograph (Stellaris nebulas + cosmograph cluster overlay)**

Matt verbatim: "I want to overlay the cosmograph on top of the stellaris nebulas, but only the primitives from the cosmograph and not allow the lassoing of the cosmograph. This will allow the players to see elements clustered, movement traits clustered, and begin to understand the puzzle and what to draw on the tablet."

- **Stellaris nebula layer (bottom; selection-capable):** Each kit rendered as a nebula containing its primaries (repeated per kit). Kits become visible regions in space.
- **Cosmograph cluster overlay (top; learning-surface; NOT selection-capable):** Underlying primitive-cluster structure visible (element clusters / movement clusters / engagement clusters). Helps players UNDERSTAND the puzzle so they know what to draw on the tablet.
- Complicates the spherical-shell architecture locked at d3ced92 § 2.6 (need amendment for two-layer composition)
- Mobile-Claude conversation snippet (Matt 2026-06-07) elaborates multi-scale visualization patterns; references symbol vocabulary emerging through exploration; LOD strategy at cluster + nebula + primary-element levels

**Element 5: Lasso scope RATIFIED (Matt 2026-06-07 wind-down)**

Matt verbatim ratification: "This is correct: Most likely reading: lasso operates on NEBULAS + within-nebula PRIMITIVES; cosmograph CLUSTER OVERLAY is read-only visual structure for player learning."

- Lasso semantics LOCKED: operates on NEBULAS (whole kits) + within-nebula PRIMITIVES (specific kit variations/elements)
- Cosmograph cluster overlay is READ-ONLY visual structure for learning; NOT selectable via lasso
- Tablet drawing operates on PRIMITIVES for composition (Path I)
- Spirit lasso operates on NEBULAS + within-nebula PRIMITIVES (Path L)
- This RESOLVES the tension between Matt's direct statement (lasso only on primitives) and mobile-conversation snippet (multi-scale lasso) — lasso at nebula-and-within-nebula-primitive scale; cosmograph cluster overlay is not lasso-able

### 2.4 Composition with existing canonical commitments

The recognition record explicitly notes which existing canonical commitments need amendment in subsequent sessions:

- **`canonical/story/2026-06-07-earth-avatar-cosmograph-creation-moment-architecture.md` (d3ced92):**
  - § 2.1 scene: ADD hill-climb + spirit materialization + sky-above-horizon transition (Element 2)
  - § 2.3 Path I: REPLACE generic ingredients with iPad/tablet drawing mechanic (Element 3)
  - § 2.4 spirit form: ADD earth-self face/body retention logic (Element 1)
  - § 2.6 spherical shell geometry: AMEND for two-layer composition (Element 4)
  - § 4.4 Q4: RESOLVE — Earth-self creation scene is EARLIER (Element 1)
- **`canonical/story/2026-06-05-cosmograph-pivot.md` § 9:** may need amendment for two-layer Stellaris-nebula + cosmograph-cluster composition (Element 4); cluster overlay as learning-surface (not selection-surface) is new architectural element
- **`canonical/story/2026-06-07-cosmograph-cross-surface-LOD-architecture.md` (18eee69):** LOD architecture extends to BOTH layers (Stellaris nebula LOD + cosmograph cluster overlay LOD); cross-surface lock STILL HOLDS but applies to both layers (Element 4)
- **`canonical/17-gear-and-spirit-guide-design.md`:** spirit form composition logic (earth-self face/body + kit identity) may need amendment for explicit reincarnation-mechanic clarification (Element 1)
- **NEW canonical doc candidate:** tablet-drawing input device architecture (Element 3 standalone canonical OR amendment to Earth-avatar canonical § 2.3)
- **NEW canonical doc candidate:** two-layer cosmograph composition (Element 4 standalone canonical OR amendment to cosmograph-pivot doc)

### 2.5 Clarification questions for subsequent Pattern B dialogue

The recognition record queues these for Matt + gandalf sustained dialogue (NOT for next session's auto-fire scope):

**Q-clarify-1:** Tablet drawing recognition pattern — what's the resolution / vocabulary? Free-form drawing recognized via shape-matching against primitive icons? Or stencil-style guided drawing? Or hybrid?

**Q-clarify-2:** Symbol vocabulary — per mobile-conversation snippet, "symbols emerge through galaxy exploration at appropriate levels (cluster-level + nebula-level symbols)." What are these symbols? Are they primitives? Are they higher-level abstractions? How do they relate to the icons player draws on the tablet?

**Q-clarify-3:** Two-layer cosmograph rendering — how do the two layers compose visually? Stellaris nebulas as foreground + cosmograph clusters as background tint? Or transparent overlay? Or modal toggle? Or smooth-blend per zoom level?

**Q-clarify-4:** Seasonal cultural/racial rotation — per mobile-conversation snippet, "a seasonal structure with cultural and racial rotation that uses your engine's natural strengths." How does this compose with Season Archive Realm Expansion canonical (2026-06-02)? Is racial rotation a NEW canonical element or an existing one being reframed?

**Q-clarify-5:** Earth-self pre-scene scope — Element 1 resolved Q4 (pre-scene EXISTS), but what's its specific scope? Brief identity-establishment (~2-3 min onboarding) per my earlier gandalf-lean? Substantial customization (face + body + name + background story)? Light minimum (name + face only)?

### 2.6 Empirical-evidence criteria for re-engagement

- Q-clarify-1 to Q-clarify-5: gates on Matt + son availability for sustained Pattern B dialogue + Matt's intended scope answers
- Canonical amendments: gate on Q-clarify resolution + gandalf authoring window (~2-4 hr substantial)
- New canonical docs for tablet-drawing + two-layer cosmograph: gate on Q-clarify-1 + Q-clarify-3 resolution
- WS2 commission scoping: inherits all amendments + clarifications when ready

### 2.7 Mobile-Claude conversation snippet preservation

The recognition record includes verbatim excerpt of Matt's mobile-Claude conversation 2026-06-07 (preserved in full in this gandalf session conversation log). Key elements from that snippet to preserve in recognition record:
- Two-layer visualization rationale
- Multi-scale lasso vocabulary discussion (later reconciled by Matt direct statement § 2.3 Element 5)
- Symbol vocabulary emerging through exploration
- LOD strategy across cluster + nebula + primary-element scales
- Integration tracing across multiple design elements
- "Trust the integration you just achieved" framing — substantive design click moment

---

## 3. State at this session close (2026-06-07)

### 3.1 Commits landed this session

| # | Commit | Description |
|---|---|---|
| 1 | `06a42bd` | gandalf: drax cosmograph A/B spike dispatch |
| 2 | `39299c4` | gandalf: federated PC team architecture commit |
| 3 | `6e08ba1` | gandalf: federated PC team role definitions |
| 4 | `814bf94` | gandalf: federated PC team operating procedures |
| 5 | `03d9ed9` | gandalf: federated PC team state updates |
| 6 | `cf112ff` | gandalf: drax cosmograph A/B spike dispatch — Gate-1 Finding 3 amendment |
| 7 | `d72569e` | gandalf: CLAUDE.md PC team auto-commit extension |
| 8 | `aed70cb` | Merge mantis spike-close commits from PC |
| 9 | `cb2d60d` | jack-ryan: Gate-2 PASS-with-INFO — drax cosmograph A/B spike Phase 2 |
| 10 | `d3ced92` | gandalf: Earth-Avatar Cosmograph Creation Moment Architecture |
| 11 | `18eee69` | gandalf: Cosmograph Cross-Surface LOD Architecture lock |
| 12 | `9dbcac8` | jack-ryan: Gate-2 PASS-with-INFO — mantis UE spike OVERALL GREEN |
| 13 | `0b2460b` | gandalf: UE Remote Control MCP Bridge Spike commission |
| 14 | `0c5c2b2` | gandalf: Earth-Avatar Creation Moment Vertical-Slice Spike commission |
| 15 | `810326a` | jack-ryan: three decisions-log entries (engine repo) |
| 16 | `2c38d73` | gandalf: legolas Mode A research commission (UE MCP prior art) |
| 17 | `32e34db` | legolas: Mode A research synthesis (REFERENCE+BUILD verdict) |
| 18 | (this commit) | gandalf: next-session plan for design recognition + workstream-spanning MCP research |

All pushed to origin per per-artifact cycle pattern.

### 3.2 Architectural commitments LOCKED today

- Federated PC team architecture (3 PC-resident counterparts + cross-host coordination)
- Drax cosmograph Phase 2 (live in production at Vercel)
- Mantis UE architecture-validation spike OVERALL GREEN (WS1-WS5 unblocked)
- Earth-Avatar Creation Moment Architecture (foundational; substantial amendments deferred per § 2 of this plan)
- Cosmograph Cross-Surface LOD Architecture (Level 0/1/2 centroid-first)

### 3.3 Commissions queued for execution (fire when David-H session opens)

- MCP bridge spike (Tier 2; ~4-8 hr david-h + mantis) at `agentic_orchestration/dispatches/2026-06-07-david-h-ue-remote-control-mcp-bridge-spike.md`
- Earth-Avatar vertical-slice spike (~4-6 sessions david-h + mantis) at `agentic_orchestration/dispatches/2026-06-07-david-h-earth-avatar-creation-moment-vertical-slice-spike.md`

Recommended sequencing: legolas workstream-spanning MCP research (Task 1 of next session) → MCP bridge spike commission amendments per legolas findings → MCP bridge spike fires → vertical-slice spike fires (with or without MCP per spike outcome)

### 3.4 Tracks active / standing-by

- David-H: closed Session 1; re-engagement when PC orchestration triggers
- Mantis: closed Session 3 spike-overall GREEN; re-engagement for MCP bridge spike + vertical-slice spike
- Drax: cosmograph A/B spike CLOSED; Phase 2 in production
- Gandalf (next session): Task 1 + Task 2 per this plan + remaining queue

### 3.5 Resume protocol for next gandalf session

Next gandalf session, read in order:

1. `canonical/00-ground-state.md` (always first; non-negotiable)
2. This plan doc (operational sequencing for next session)
3. `canonical/story/2026-06-07-earth-avatar-cosmograph-creation-moment-architecture.md` (foundational architectural commitment; Element 1-5 amendments are about THIS doc)
4. `agentic_orchestration/legolas/research/2026-06-07-ue-mcp-prior-art/synthesis.md` (first legolas synthesis; informs workstream-spanning research scope)
5. `agentic_orchestration/dispatches/2026-06-07-david-h-ue-remote-control-mcp-bridge-spike.md` (commission to be amended per workstream-spanning research outcome)
6. Original Matt + son design contribution captured in this session's conversation (verbatim Matt statements preserved in § 2.3 of this plan)

---

## 4. Sign-off

**Authored:** gandalf 2026-06-07 per Matt directive "Please write both of these (legolas and design recognition) into tomorrow's session. Then let's wind down."

**Routing:** next gandalf session reads this plan at session-start (after canonical/00-ground-state.md per session-start protocol); executes Task 1 + Task 2 in order; defers canonical amendments + Pattern B dialogue per recognition-validate-commit discipline.

**Empirical-evidence trigger for next gandalf re-engagement:** Matt fires next gandalf session.

**End of next-session plan.**
