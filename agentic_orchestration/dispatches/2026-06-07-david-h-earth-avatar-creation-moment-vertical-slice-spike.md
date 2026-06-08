# Dispatch — Earth-Avatar Creation Moment Vertical-Slice Spike

**Date:** 2026-06-07
**Author:** gandalf (story-and-design steward)
**Authority:** Matt 2026-06-07 ratification ("Maybe we should start with 500 constellations to be conservative yet deliver all primitives per cluster" + "important to mention that it should be DH led sessions invoking Mantis as a sub agent")
**To:** David-H (PC-side orchestrator; PC-resident) — Mantis invoked as Pattern A sub-agent per phase
**Cycle:** Pre-WS1 vertical-slice spike — empirical validation of Earth-Avatar Creation Moment architectural commitment at minimum viable scope before WS1-WS5 commission cascade fires
**Type:** SPIKE — empirical architecture validation; build minimum-viable working prototype of the creation moment scene; validate dual-path creation mechanism + spherical shell geometry + ambiguous spirit form transformation + LOD architecture
**Cost budget:** $0 LLM / $0 Meshy (uses existing Crusader pre-rigged GLBs on PC); UE-tooling-time only
**Time budget:** ~4-6 mantis sessions wall-clock (each ~2-4 hr)
**Critical anchors:**
- `canonical/story/2026-06-07-earth-avatar-cosmograph-creation-moment-architecture.md` (foundational architectural commitment this spike validates)
- `canonical/story/2026-06-07-cosmograph-cross-surface-LOD-architecture.md` (LOD vocabulary lock; implement Level 0/1/2 from start)
- `canonical/story/2026-06-05-cosmograph-pivot.md` § 9 (primitive-as-star + kit-as-constellation substrate lock)
- `canonical/story/2026-06-06-atomic-substrate-registry.md` (Layer 0 primitives = Path I ingredients)
- `agentic_orchestration/mantis/research/ue-architecture-validation-spike-2026-06-06/port-workstream-gating-verdict.md` (spike OVERALL GREEN unblocks this commission)
- `agentic_orchestration/qa/findings/2026-06-07-mantis-ue-architecture-validation-spike-gate-2.md` (jack-ryan Gate-2 PASS-with-INFO)
- `agentic_orchestration/dispatches/2026-06-07-david-h-ue-remote-control-mcp-bridge-spike.md` (parallel tooling spike; this commission inherits MCP outcome if GREEN)
- `agentic_orchestration/elrond/research/cosmograph-substrate-trace-2026-06-06/cosmograph_README.md` (substrate source for 500 PROVISIONAL constellations)
- `agentic_orchestration/mantis/research/ue-architecture-validation-spike-2026-06-06/criterion-3-2-meshy-ue-import.md` (Crusader GLB import learnings + Hips root skeleton convention)
- `agentic_orchestration/mantis/research/ue-architecture-validation-spike-2026-06-06/criterion-3-7-stretch-3d-cosmograph.md` (Niagara sprite + LOD perf data)
- `canonical/38-downstream-delivery-strategy-2026-05-23.md` § 4 (downstream delivery strategy; this spike is pre-WS1 vertical slice)

---

## 0. TL;DR

Build minimum-viable working prototype of the **Earth-Avatar Creation Moment** scene in UE 5.7 — validates the foundational architectural commitment (canonical `2026-06-07-earth-avatar-cosmograph-creation-moment-architecture.md`) at production-relevant scale before WS1-WS5 commission cascade fires.

**Scene scope:**
- Green grassy hill environment on Earth (simple UE 5.7 ambient outdoor setup; not production-art-quality; aesthetic-direction-validation-quality)
- Pre-selected Earth avatar character (deferred Q4 refinement; uses placeholder humanoid for prototype; identity emerges at WS3 production scope)
- Ambiguous spirit form companion (luminescent mist-cloud humanoid silhouette adjacent to Earth avatar)
- Celestial sphere overhead with 500 PROVISIONAL constellations + 4 named-bearer anchors (Duskweaver + Tide Warden + Ember Sweeper + 1 more) using pre-rigged Crusader GLBs at materialization moments

**Interaction scope:**
- Path L (Lasso the Sky) operational — twirl celestial sphere overhead + spirit-lasso draws polygon on sphere interior surface + lookup → constellation identification → spirit form transforms toward matched identity
- Path I (Drop Ingredients) operational — curated palette of ~20-30 atomic-substrate-registry primitives presented as alchemical vials/tokens; player drags onto spirit form; sphere progressively focuses on convergent constellation; spirit form solidifies progressively
- Both paths share substrate (500 PROVISIONAL + 4 named) + converge on same outcome (kit selection)

**LOD architecture from start:**
- Level 0 = ~6 mechanic-family centroid markers OR ~3 faction halos at default sphere-overview view
- Level 1 = 500 constellation-centroid markers + bounded cluster outlines visible at mid zoom-in
- Level 2 = full per-primitive stars (each constellation × ~15 primitives = ~7500 nodes total) at close zoom within hovered/lassoed region

**Effects stack DEFERRED to WS2** — prototype uses simple sprite stars + basic constellation lines + ambient sky lighting only. No VDB nebula context. No ribbon edges between constellations. No emissive aura materials. Aesthetic polish is WS2 production scope; this spike validates architecture not polish.

**Operational pattern:** David-H led orchestration; mantis invoked as Pattern A sub-agent per phase. Matt-pilot UE Editor when MCP bridge unavailable OR specific UI-only interactions required. If MCP bridge spike GREEN (parallel commission), mantis sub-agent leverages MCP tools for direct UE state manipulation.

**Spike verdict shape per phase:** each phase has GREEN/YELLOW/RED criteria; David-H aggregates into spike-overall verdict at close.

---

## 1. Scope

### 1.1 What David-H produces (orchestration)

Delivery packet at `agentic_orchestration/david-h/notes/2026-06-07-earth-avatar-vertical-slice-spike/`:

| Artifact | Format | Purpose |
|---|---|---|
| `spike-findings-report.md` | markdown | Aggregate verdict + per-phase findings + architectural-amendment surfaces + WS1-WS5 scoping informants |
| `phase-N-findings.md` (one per phase) | markdown | Detailed findings per phase (mantis sub-agent invocation log + Matt-pilot observations + verdict GREEN/YELLOW/RED) |
| `session-boundary-memos/` | directory | David-H session-boundary memos per Session per OP § 5 |
| `architectural-surfaces.md` | markdown | Cross-phase architectural observations for gandalf review post-spike (LOD vocabulary refinements; Path L/I friction points; spirit form transformation visual gaps; etc.) |

### 1.2 What Mantis produces (sub-agent invocations + UE artifacts)

Per David-H sub-agent invocations + direct UE work:
- UE 5.7 project additions: scene assets + Niagara systems + UMG widgets + Blueprints + materials
- Commit to `reincarnated-unreal/` repo (PC-local; push handled per established cycle-pattern + push-credential workaround)
- Per-phase reports to David-H synthesizing what was built + perf + findings + issues

### 1.3 What spike does NOT produce

- **No production-art-quality assets.** Aesthetic-direction-validation-quality only. Hill environment is functional; not WS2 production-grade lighting/atmosphere/materials.
- **No VDB nebula / ribbon edges / emissive aura effects.** Effects stack DEFERRED to WS2.
- **No identity-defining Earth avatar customization scene.** Pre-selected default avatar; Q4 refinement deferred.
- **No materialization cinematic.** Confirm fires basic spirit-form-solidification animation; full cinematic is WS3 production scope.
- **No multi-platform optimization.** PC-only prototype; mobile is D8/WS5 scope.
- **No tutorial / onboarding flow.** Prototype is a sandbox for architecture validation, not player-onboarding-flow validation.
- **No save/load / persistence.** WS4 scope.
- **No real engine-validated kit corpus.** Uses PROVISIONAL substrate per Move B amendment + 4 named-bearer anchors.

---

## 2. Five-phase execution

David-H orchestrates phases sequentially; Mantis invoked per phase as Pattern A sub-agent. Matt-pilot when UE Editor interactive work + MCP bridge unavailable.

### Phase 1 — Earth-Hill Environment + Pre-Selected Avatar Setup (~1 session, 2-4 hr)

**Goal:** scene foundation operational. Player can stand on Earth and see the sky overhead.

David-H sub-agent invocation to Mantis: "Build minimal Earth-hill environment in UE 5.7. Green grassy hill + ambient daylight-evening lighting transition + Earth avatar character (use UE5 Mannequin or Crusader GLB as placeholder) standing on hill. Camera positioned at first-person OR third-person-over-shoulder per design intent. Player can move camera (mouse-look) to see sky overhead. Initial sky is empty (no stars yet; that's Phase 2). Save level as `L_CreationMoment.umap`. Commit + report."

Mantis returns: scene operational + camera control working + screenshot of Earth-hill scene.

David-H verdict criteria:
- GREEN: scene loads in PIE; player can navigate camera; visual atmosphere is contemplative+pastoral; lighting reads as "evening/dusk transition"
- YELLOW: scene loads but visual atmosphere doesn't read clearly (lighting too bright/dark; wrong feel)
- RED: scene fails to load OR fundamental UE constraint blocks the scene composition

### Phase 2 — Celestial Sphere Cosmograph Rendering (~2 sessions, 4-8 hr; largest)

**Goal:** sky operational with 500 PROVISIONAL constellations + LOD architecture functional.

David-H sub-agent invocation to Mantis (or sub-phases):

**Sub-phase 2a — Substrate ingestion:**
- Ingest substrate from elrond Phase 4 packet (`cosmograph-substrate-trace-2026-06-06/kit_constellations.parquet` + `primitive_registry.parquet`)
- Curate subset of 500 PROVISIONAL constellations (most representative of full 1000 by element/faction distribution)
- Designate 4 named-bearer anchor positions (specific spherical coordinates; e.g., 4 cardinal-quadrant positions for visibility from all rotations)
- Output: `Content/Data/Cosmograph/constellation_layout_vertical_slice.json` (UE-consumable format mirroring drax /forge Phase 2's `constellation_layout.json` pattern; ~500 entries + 4 named-bearer entries)

**Sub-phase 2b — Spherical Fibonacci distribution + Niagara emitter:**
- Spherical Fibonacci OR Poisson-disk point distribution on sphere surface for 500 constellations + 4 named-bearer positions
- Niagara point-cloud emitter NS_CosmographSphere consuming ingested data
- Per-primitive sprite rendering within each constellation (full ~7500-node detail at Level 2)
- Element-tinting at primitive level (per cosmograph-pivot § 9.4 visual encoding)
- PROVISIONAL demarcation: dotted MST lines between primitives in 499 of 500 constellations; solid lines for 4 named-bearer constellations
- Brightness encoding for BDI ω+τ load-bearing primitives (per substrate-trace ω+τ values)

**Sub-phase 2c — LOD architecture implementation:**
- Level 0 (default sphere-overview): ~6 mechanic-family centroids OR ~3 faction halos rendered; 500 constellations condensed to overview markers
- Level 1 (mid zoom): 500 constellation-centroid markers + bounded cluster outlines visible
- Level 2 (close zoom): full per-primitive star detail within proximate region (camera-distance-triggered)
- Smooth opacity transitions between levels (not modal snaps)
- Reference: cross-surface LOD canonical doc + mantis Session 3 Level 0/1/2 design

**Sub-phase 2d — Camera interaction (twirl-the-sky):**
- Implement camera/sphere interaction: player drag-rotates the celestial sphere overhead
- Trackball-style spherical rotation (not free camera orbit; constrained to sphere viewing from interior surface)
- Smooth easing on rotation gesture
- Optional: subtle parallax with 3D nebula context background (even though full nebula effects deferred, simple star-field-far-background OK)

Mantis returns: cosmograph operational + screenshots at Level 0/1/2 + perf measurements at each level + sphere rotation interaction confirmed.

David-H verdict criteria:
- GREEN: all 500 constellations rendered at expected positions; LOD transitions smooth at 60 FPS; sphere rotation responsive; element-tinting + faction-halos visible
- YELLOW: subset of above (e.g., LOD transitions noticeable but acceptable; perf marginal at Level 2; rotation slightly clunky)
- RED: fundamental rendering failure; constellation positions incorrect; perf <30 FPS at Level 2; LOD architecture doesn't transition

### Phase 3 — Ambiguous Spirit Form + Transformation System (~1 session, 2-4 hr)

**Goal:** spirit form companion operational; transforms responsively to player action.

David-H sub-agent invocation to Mantis:

**Sub-phase 3a — Ambiguous spirit form mesh + material:**
- Create or place spirit form mesh adjacent to Earth avatar in scene
- Material: translucent emissive humanoid silhouette (luminescent mist-cloud appearance)
- Soft edges + subtle internal motion (particle drift; soft glow pulse via material panner)
- Initial state: undefined color + soft silhouette + low emissive intensity

**Sub-phase 3b — Transformation system:**
- Blueprint or animation logic: spirit form responds to selection state
- Element-primitive committed → color saturation increases (e.g., fire primitives → orange/red tint accumulates)
- Weapon-form primitive committed → silhouette begins outlining weapon shape
- Archetype primitives committed → posture/silhouette adjusts toward archetype
- Full kit identity → use named-bearer Crusader GLB asset for materialization when player lassos region containing named-bearer constellation OR composes ingredients converging on named-bearer

**Sub-phase 3c — State machine:**
- Ambiguous → Partially defined (responds continuously as primitives/constellations selected)
- Confirm trigger → Full kit avatar appearance (snaps to selected kit's visual; spirit form solidifies)

Mantis returns: spirit form operational + transformation responds to test selections + screenshots at ambiguous/partial/defined states.

David-H verdict criteria:
- GREEN: spirit form visible + ambiguous initial state reads correctly; transformations responsive (sub-second feedback); final state snaps cleanly
- YELLOW: visual gaps (transformation feels mechanical not organic; final-state snap is jarring)
- RED: spirit form fails to render; transformations don't trigger; state machine broken

### Phase 4 — Path L (Lasso the Sky) Mechanic (~1 session, 2-4 hr)

**Goal:** player can lasso a region of the celestial sphere + lookup returns constellation match + spirit form transforms.

David-H sub-agent invocation to Mantis:

**Sub-phase 4a — Spirit-lasso input + screen-projection:**
- Player draws polygon on sphere surface via mouse/controller gesture (spirit-lasso visual: shimmering ethereal thread following cursor)
- Screen-projection: polygon vertices projected to spherical coordinates (lat/lon) at current camera rotation
- Visual feedback: lasso polygon rendered on sphere surface during drag

**Sub-phase 4b — Lasso completion + constellation lookup:**
- On lasso-close (cursor returns near start): polygon vertices finalized
- Project polygon to spherical region; identify constellations whose centroids fall within projected region (Level 1 lasso semantics per cross-surface LOD § 2.3)
- Apply constellation-overlap composite-score algorithm (per `2026-06-06-cosmograph-star-granularity-verdict.md` § 4.3: `0.4 × coverage_fraction + 0.3 × density_score + 0.3 × β-weighted overlap`)
- Identify best-match constellation (highest composite score)

**Sub-phase 4c — Spirit form transformation toward match:**
- Spirit form transforms toward the matched constellation's identity (via Phase 3 transformation system)
- If matched constellation is a named-bearer: full kit identity visible; Crusader GLB appears
- If matched constellation is PROVISIONAL: placeholder identity; substrate-aligned color + silhouette emergence but no named identity

**Sub-phase 4d — Refinement:**
- Player can re-lasso (replace selection; spirit form transforms toward new match)
- Player can confirm (commit; phase ends; materialization snapshot logged)

Mantis returns: lasso mechanic operational + spirit form transformations responsive to lasso selections + screenshots/recordings at multiple lasso operations.

David-H verdict criteria:
- GREEN: lasso draws smoothly; constellation lookup returns expected matches; spirit form transformations are continuous + responsive; both named-bearer and PROVISIONAL paths work
- YELLOW: subset of above (lasso draws but laggy; matches return correctly but spirit transformation is mechanical; named-bearer ID works but PROVISIONAL placeholder feels empty)
- RED: lasso input broken; lookup returns wrong matches; spirit form fails to transform

### Phase 5 — Path I (Drop Ingredients) Mechanic (~1 session, 2-4 hr)

**Goal:** player can drop substrate-primitive ingredients onto spirit form; sky progressively focuses on convergent constellation.

David-H sub-agent invocation to Mantis:

**Sub-phase 5a — Ingredient palette UI:**
- UMG widget: ingredient palette panel showing ~20-30 curated primitives as alchemical vials/tokens
- Each ingredient visual: small icon + element-tinted vial appearance + tooltip showing primitive name/category
- Curated palette per design intent: ~8-12 element primitives + ~5-8 attribute primitives + ~5-8 weapon-form-token primitives + ~2-3 archetype hint primitives
- Source: atomic-substrate-registry Layer 0 primitives; curated for vertical-slice prototype (full ~570 primitives is overwhelming for prototype)

**Sub-phase 5b — Drag-and-drop interaction:**
- Player drags ingredient from palette onto spirit form
- Drop triggers: ingredient is "consumed" + added to spirit's current composition state
- Spirit form transformation responds (Phase 3 system): color/silhouette/features adjust per accumulated ingredients

**Sub-phase 5c — Celestial sphere narrowing:**
- Each ingredient drop progressively narrows visible constellations on the sphere
- Constellations matching all accumulated ingredients: brighten (full opacity + element-tint glow)
- Constellations NOT matching: dim (low opacity; muted color)
- Visible filtering happens at Level 1 LOD by default (player sees constellation-centroid markers brightening/dimming)

**Sub-phase 5d — Convergence detection + confirm:**
- When accumulated ingredients narrow to ≤1-3 candidates: "MATCH FOUND" indicator appears
- Player can confirm at any time (don't need full uniqueness)
- Player can backtrack: remove an ingredient (re-expand visible candidates)
- Confirm fires materialization (per Phase 4 confirm logic)

Mantis returns: ingredient mechanic operational + sphere narrowing responsive + convergence detection working + screenshots/recordings of full Path I flow.

David-H verdict criteria:
- GREEN: drag-and-drop responsive; sphere narrowing visual is intelligible; convergence detection accurate; spirit form responsiveness preserved
- YELLOW: subset (lag; narrowing visual too subtle; convergence threshold needs tuning)
- RED: input mechanic broken; sphere doesn't narrow; convergence detection fails

### Phase 6 — Integration + Vertical-Slice Verdict (~1 session, 2-4 hr)

**Goal:** end-to-end vertical slice operational + David-H authors verdict.

David-H sub-agent invocation to Mantis: "End-to-end integration test. Run through full creation moment per design intent: scene loads → spirit form ambiguous → player chooses Path L OR Path I → spirit form transforms → player confirms → materialization snapshot. Test 4-6 representative scenarios (Path L on named-bearer + Path L on PROVISIONAL + Path I on named-bearer + Path I on PROVISIONAL + hybrid Path L+I combination + edge cases). Document any integration bugs or UX friction."

Mantis returns: integration test results + scenarios documented + bug list + UX friction observations + screenshots/recordings.

David-H synthesizes spike-overall verdict:
- GREEN: all phases GREEN; end-to-end flow operational; architecture validated; ready for WS1-WS5 commission scoping
- YELLOW: some phases YELLOW; architecture valid but refinements needed; specific surfaces routed to gandalf for amendments before WS1
- RED: architectural blocker discovered; commission requires gandalf re-engagement for architectural re-design

David-H authors spike-findings-report.md + architectural-surfaces.md + session-boundary-memo.md + commits + pushes (via SSH-bundle workaround if needed).

---

## 3. Verdict criteria

| Spike-overall verdict | Criteria |
|---|---|
| **GREEN** | All 6 phases GREEN; end-to-end vertical slice operational; architecture validated empirically; WS1-WS5 commission scoping unblocked with confidence |
| **YELLOW** | Most phases GREEN with isolated YELLOWs; architecture valid but specific refinements needed; gandalf authors targeted amendments to canonical commit before WS1 fires |
| **RED** | Architectural blocker(s) discovered (e.g., spherical-shell rendering fundamentally inadequate; dual-path mechanism doesn't compose; spirit form transformation system unworkable); commission requires gandalf re-engagement for architectural re-design before WS1 |

---

## 4. Composition with parallel + downstream commitments

### 4.1 Parallel: MCP bridge spike

If MCP bridge spike (parallel commission) returns GREEN before Phase 2 fires: David-H invocations of mantis sub-agent leverage MCP tools for direct UE state manipulation. Dramatically reduces Matt-pilot relay. Phase 2-5 execution faster.

If MCP bridge YELLOW: hybrid pattern; mantis uses MCP for code-controllable actions; Matt-pilot for UI-only operations.

If MCP bridge RED: full Matt-pilot pattern per mantis Session 3 precedent. Slower but achievable. Vertical slice still ships.

### 4.2 Downstream: WS1 port commission scoping

Vertical slice findings inform WS1 commission scoping (gandalf, next session). Specifically:
- LOD architecture refinements (if Phase 2 surfaces tuning needs)
- Lasso mechanic UX refinements (if Phase 4 surfaces friction)
- Ingredient palette curation refinements (if Phase 5 surfaces ingredient-set issues)
- Spirit form transformation visual refinements (if Phase 3 surfaces gaps)
- Performance characteristics at production scale (Phase 2 + 6 measurements inform WS2 effects-stack budgeting)

### 4.3 Downstream: WS2 commission inherits aesthetic polish work

This spike defers effects stack to WS2 (VDB nebula context + ribbon edges + emissive auras + production-grade environment art). WS2 commission scoping inherits the vertical-slice prototype as foundation + adds effects + asset-pipeline production work.

### 4.4 Downstream: WS3 materialization cinematic

Confirm-time materialization in vertical slice is basic (spirit form solidifies via Phase 3 transformation system). Full cinematic with camera fly-out into nebula context + materialization payoff is WS3 scope.

### 4.5 Refinement questions deferred per Earth-avatar canonical § 4

Five refinement questions (Q1 ingredient palette / Q2 Path-I convergence criterion / Q3 path composition / Q4 Earth-avatar pre-scene scope / Q5 spirit form visual logic) are addressed BY this vertical slice via Matt+son input as the prototype is built. Final answers refine the canonical commit post-spike.

---

## 5. Substrate sources

### 5.1 500 PROVISIONAL constellations

Source: `agentic_orchestration/elrond/research/cosmograph-substrate-trace-2026-06-06/kit_constellations.parquet` (1000 entries; curate 500 most representative).

Curation criteria for the 500-subset:
- Preserve element distribution (8 canonical elements with proportional representation)
- Preserve faction overlay structure (7 attribute-group factions per Phase A)
- Preserve mechanic-family distribution (6 emergent mechanic families per Phase A)
- Skip uniformly-similar constellations (preserve diversity in the subset)

Mantis (or David-H + mantis collaboration) executes curation; documents which 500 selected + rationale.

### 5.2 4 named-bearer anchors

Source: `agentic_orchestration/cycle-14-wave-5-season-001/` cycle-14 named-bearer kits (Duskweaver + 36 others). Select 4 for vertical-slice anchors.

**Recommended 4:**
- Duskweaver of the Eclipsed Meridian (canonical Top-1 per Matt 2026-06-02; cosmograph-pivot worked example)
- Tide Warden (named via Crusader pre-rigged GLBs already on PC)
- Ember Sweeper (named via Crusader pre-rigged GLBs)
- 1 additional cycle-14 named-bearer of David-H + mantis choice (preferably contrasting element/archetype from above 3 for diversity)

Each named-bearer anchor: spherical coordinate position on sphere (cardinal-quadrant suggested for visibility from all rotations) + visual identity using corresponding Crusader pre-rigged Meshy GLB at `C:\dev\reincarnated-collaboration\duskweaver\Meshy_AI_Crusader_of_the_Ember_biped\` (and equivalent paths for other named-bearers).

### 5.3 Ingredient palette curation (~20-30 primitives)

Source: `canonical/story/2026-06-06-atomic-substrate-registry.md` Layer 0 primitives.

Recommended palette:
- 8 element primitives (fire / water / earth / wind / lightning / holy / shadow / physical) — full canonical element coverage
- 4-5 attribute primitives (STR / INT / WIS / DEX + maybe VIT) — full attribute coverage
- 6-8 weapon-form-token primitives (sword / spear / bow / staff / shield / dagger / hammer / etc.) — diverse weapon-form representation
- 3-4 archetype hint primitives (warrior / mage / hunter / support) — quick-identity helpers
- 2-3 scaling-pattern primitives (additive / multiplicative / transformative per canonical 47) — advanced compositional layer

Total: ~25-28 ingredients. David-H + mantis (or gandalf consultation if needed) finalizes during Phase 5a.

---

## 6. Operational pattern — David-H led; Mantis as sub-agent

Per Matt 2026-06-07 directive + federated-team-commit § 5.

**David-H session pattern per phase:**
1. David-H reads dispatch + relevant anchor docs at session-start
2. David-H plans phase execution
3. David-H invokes mantis as Pattern A sub-agent with phase-scoped task: `Agent({ subagent_type: "mantis", description: "Phase N execution", prompt: "<phase-specific prompt with references>" })`
4. Mantis sub-agent executes + returns work-product + status
5. David-H synthesizes + commits orchestration record
6. David-H invokes Matt-pilot if specific UE Editor UI work needed (waits for Matt-typed UE state updates; relays to mantis sub-agent as needed)
7. David-H decides next sub-phase fire OR phase-completion verdict
8. At phase close: David-H commits phase findings + pushes (or surfaces push to Matt per cycle pattern)

**MCP bridge composition (if GREEN):**
- Mantis sub-agent has access to MCP tools for direct UE state manipulation
- Reduces Matt-pilot dependency dramatically
- David-H + mantis sub-agent flow becomes more autonomous

**Matt-pilot fallback (if MCP unavailable):**
- For UE Editor UI-only interactions (placing actors visually, configuring Niagara emitters via UI, materializing visual ideas Matt has in his head): Matt opens UE Editor + describes state to David-H session terminal + David-H relays to mantis + mantis directs next step + Matt executes
- Slower than MCP-direct but proven workable per Session 3 precedent

**Cross-host coordination:**
- David-H + mantis are both PC-resident; operating within PC seam
- Mac-side coordination only at phase-aggregate level: David-H surfaces architectural amendment surfaces to gandalf via consultation note (`agentic_orchestration/david-h/notes/<date>-consultation-mac-gandalf-<topic>.md`) if substantive
- Routine progress reports stay PC-side

**Push pattern:**
- Per established Matt 2026-06-07 cycle pattern: per-artifact push
- Push from PC may hit credential gap (Windows Credential Manager TTY issue); SSH-bundle workaround proven (Matt or Mac-resident agent bundles PC commits + pushes from Mac)
- Optional: GitHub CLI install on PC for permanent push fix (David-H surfaces to Matt if appropriate)

---

## 7. Anti-patterns to avoid

- **Building production-art-quality environment.** Vertical slice validates architecture; aesthetic polish is WS2 scope.
- **Adding effects stack mid-spike.** VDB nebula + ribbon edges + emissive deferred to WS2. Sticking to simple sprites preserves perf headroom for iteration.
- **Curating 1000+ constellations instead of 500.** Conservative scope per Matt 2026-06-07; 500 validates architecture + delivers vast-sky resonance without perf-headroom-loss risk.
- **Skipping LOD architecture for "simplicity."** LOD is load-bearing at 500-constellation scale per cross-surface LOD canonical; implement from start.
- **Matt-pilot pattern as primary execution when MCP bridge is available.** If MCP GREEN, leverage it; David-H + mantis autonomous flow is the intended pattern.
- **Surfacing every per-phase architectural observation to gandalf.** Cluster architectural surfaces at phase-aggregate level (David-H synthesizes); only consult Mac-gandalf for substantive cross-cutting design questions.
- **Pushing speculative refinements to canonical commit mid-spike.** Refinement questions deferred per Earth-avatar canonical § 4; spike validates architecture; canonical refinement happens post-spike via gandalf if needed.

---

## 8. Sign-off

**Authored:** gandalf 2026-06-07 per Matt ratification of substrate scope (500 + 4) + David-H-led-with-mantis-sub-agent operational pattern + post-mantis-spike-OVERALL-GREEN-aggregation unblock.

**Authority:** gandalf cross-cutting design authority for pre-WS1 vertical-slice commission targeting David-H as PC-side orchestrator per federated-team-commit § 5.1.

**Empirical-evidence trigger for spike-overall verdict:** all 6 phases execute; David-H authors aggregate verdict; routes to gandalf for ratification + WS1 commission scoping unblock OR architectural amendment if YELLOW/RED.

**Recommended execution sequencing:** fire AFTER OR IN PARALLEL with MCP bridge spike (parallel commission). If both fired in parallel: vertical slice can absorb MCP bridge mid-execution if MCP spike returns GREEN; falls back to Matt-pilot per Session 3 precedent if MCP RED.

**Estimated timeline:** ~4-6 mantis sessions wall-clock across 6 phases. Could compress if MCP bridge GREEN reduces Matt-pilot dependency.

**Routing:** David-H consumes at session-start; executes per § 2 phase-by-phase; returns spike-overall verdict to gandalf for ratification + WS1 commission scoping unblock.

**End of dispatch.**
