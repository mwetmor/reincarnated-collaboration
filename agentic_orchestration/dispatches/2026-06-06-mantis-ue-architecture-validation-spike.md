# Dispatch — Mantis UE Architecture-Validation Spike (P1)

**Date:** 2026-06-06
**Author:** gandalf (story-and-design steward)
**Authority:** Matt 2026-06-06 — UE workstream pre-scoping per cosmograph Phase A close-out; spike per canonical 38 § 4 acceptance criteria 3.1-3.6 + 3D cosmograph viability stretch criterion
**To:** mantis (UE-seam agent; PC-resident; SSH-invoked from Mac per 2026-05-31 placement decision)
**Cycle:** UE workstream prerequisite — P1 architecture-validation spike (the only remaining gate before WS1-WS5 port workstreams fire)
**Type:** SPIKE — empirical validation; no production code generation; report findings
**Cost budget:** $0 LLM (spike work; reads + writes UE configs + runs UE tools; no LLM calls)
**Time budget:** ~1-2 weeks mantis time across 6 primary criteria + 1 stretch + 1 legolas-collaboration sub-step
**Critical anchors:**
- `canonical/38-downstream-delivery-strategy-2026-05-23.md` § 4 immediate next actions (3.1-3.6 acceptance criteria)
- `canonical/story/2026-05-31-ue-seam-agent-placement-decision.md` (your placement decision + SSH invocation pattern)
- `canonical/story/2026-06-05-cosmograph-pivot.md` (cosmograph architectural commitment; current player-surface manifestation milestone)
- `canonical/story/2026-06-06-atomic-substrate-registry.md` (Layer 0 atomic substrate registry)
- `canonical/story/asset-pipeline-meshy-swap-2026-05-22.md` (Meshy + image-pass-through validation source)
- `~/Games/reincarnated-collaboration/matt_notes_handoff_docs/reincarnated-headless-ssh-handoff.md` (SSH→UE command patterns)
- `agentic_orchestration/legolas/research/2026-06-02-constellation-form-ue-techniques/synthesis.md` (existing UE VFX research — may compose with stretch criterion)
- `agentic_orchestration/legolas/research/2026-06-02-unreal-character-customization-research/synthesis.md` (UE 5.5+ character pipeline research — composes with criterion 3.2)

---

## 0. TL;DR

Mantis validates that the engine's JSON output → Meshy → UE 5.7 → playable form pipeline works end-to-end, plus that Niagara + PCG + TAA/TSR perform adequately for the cosmograph 3D port. Spike is read-only on engine + design-side; mantis exercises UE tooling on PC and reports pass/fail/blocker per criterion.

**Six primary criteria** per canonical 38 § 4 (acceptance gates for port workstreams to begin):
1. 3.1 — JSON output from engine imports cleanly into Meshy + produces usable 3D model
2. 3.2 — Meshy Control Rig export imports into UE 5.7 with bones / skeleton intact + animatable
3. 3.3 — Image-pass-through-to-Meshy validation (per canonical 38 § 4 step 3.3 + asset-pipeline-meshy-swap)
4. 3.4 — Niagara VFX consumes engine ability-spec JSON + produces visible in-engine effect
5. 3.5 — PCG framework consumes engine geo-spatial output + produces navigable room layout
6. 3.6 — TAA/TSR fast-combat readability validated with rapid motion

**One stretch criterion** (cosmograph-specific):
7. 3.7 STRETCH — 3D cosmograph viability: 100-star Niagara point cloud + procedural constellation lines + nebula volumetric + 60fps on PC + projected feasibility on mid-tier mobile

**One legolas-collaboration sub-step:**
- Legolas Mode A research sweep: UE FAB + marketplace cosmic-VFX assets compatible with 5.7 + composable with procedural Niagara cosmograph rendering. Produces short-list of 5-10 assets. Fires PARALLEL with primary criteria 3.1-3.6.

**Spike verdict format per criterion:** PASS / YELLOW (with notes) / RED (with blocker description + proposed mitigation). Spike overall verdict gates port workstream WS1-WS5 sequencing.

---

## 1. Scope

### 1.1 What mantis produces

A delivery packet at `agentic_orchestration/mantis/research/ue-architecture-validation-spike-2026-06-XX/` containing:

| Artifact | Format | Purpose |
|---|---|---|
| `spike-findings-report.md` | markdown | Per-criterion findings + verdict + blocker analysis + recommendations |
| `criterion-3-1-meshy-json-import.md` | markdown | 3.1 detailed findings |
| `criterion-3-2-meshy-ue-import.md` | markdown | 3.2 detailed findings + screenshots from PC |
| `criterion-3-3-image-pass-through.md` | markdown | 3.3 detailed findings + 3-5 weapon-sample test results |
| `criterion-3-4-niagara-json.md` | markdown | 3.4 detailed findings + Niagara emitter screenshots |
| `criterion-3-5-pcg-json.md` | markdown | 3.5 detailed findings + room-layout screenshots |
| `criterion-3-6-taa-tsr.md` | markdown | 3.6 detailed findings + perf measurements |
| `criterion-3-7-stretch-3d-cosmograph.md` | markdown | 3.7 STRETCH findings + 100-star demo project + FPS measurements |
| `legolas-fab-asset-short-list.md` | markdown | Curated 5-10 UE 5.7-compatible cosmic-VFX assets (legolas-authored; mantis verifies install + integration smoke) |
| `port-workstream-gating-verdict.md` | markdown | Final verdict on whether WS1-WS5 port workstreams can fire |

### 1.2 What mantis does NOT produce in this spike

- **No production UE game code.** Spike is validation; not implementation. Production code lands in WS1-WS5 port workstreams post-spike PASS.
- **No engine-side changes.** Engine JSON output schema is read-only input; if a gap surfaces, escalate to gandalf + star-lord for engine-side discussion.
- **No LLM-driven content.** Spike work is pure UE tooling + engine JSON consumption + Meshy API consumption.
- **No commits to engine or loadout repos.** Mantis commits only to `reincarnated-unreal` (PC) + spike packet artifacts in meta-repo.

---

## 2. Criterion 3.1 — JSON → Meshy import

**Scope:** verify engine JSON output (kit composition + substrate-trace JSON packet from current cosmograph Phase A delivery) imports into Meshy + produces a usable 3D model.

**Test pattern:**
1. Take 3 representative kit JSON specs from the engine output:
   - 1 cycle-14 wave-5 named-bearer kit (e.g., Duskweaver of the Eclipsed Meridian — has cohesion-judge-approved identity)
   - 1 simulated PROVISIONAL kit (bc_cell_id placeholder)
   - 1 archetypally distinct kit (e.g., a Stoneward / Embermage / similar — substrate diversity)
2. For each kit: extract the kit's primary appearance descriptor (element + attribute + cultural-tradition + weapon-form-token)
3. Feed to Meshy 6 (current version) via API or CLI
4. Capture Meshy output (.glb / .fbx)
5. Inspect mesh quality: poly count, texture quality, riggability for humanoid skeleton

**Acceptance:**
- PASS: 3/3 kits produce usable humanoid 3D models (poly count within range; textures readable; mesh closed)
- YELLOW: 2/3 PASS + 1 has resolvable issues (specific issue description + proposed mitigation)
- RED: ≤1/3 PASS or systemic issue (Meshy can't ingest engine JSON schema; needs star-lord export schema amendment)

**Discipline:** Discipline #11 empirical-first inspection — measure mesh quality empirically, not by Meshy's marketing claims.

---

## 3. Criterion 3.2 — Meshy → UE 5.7 import

**Scope:** verify Meshy Control Rig export imports into UE 5.7 with bones + skeleton intact + animatable.

**Test pattern:**
1. Use the 3 meshes produced in 3.1
2. Configure Meshy export for Unreal-compatible Control Rig per Meshy 6 documentation
3. Import each into the UE 5.7 project at `C:\dev\reincarnated-unreal\Reincarnated\`
4. Verify:
   - Skeleton hierarchy is intact (humanoid bones present + named per UE conventions)
   - Control Rig auto-generates or imports cleanly
   - Mesh + skeleton + Control Rig compose into a Skeletal Mesh asset
   - Asset can be dropped into a scene + animated via existing UE 5.7 animation Blueprint
5. Run the 5.7 headless smoke test per § 4.2 of the mantis OP:
   ```
   ssh mhwet@192.168.1.133 '"C:\Program Files\Epic Games\UE_5.7\Engine\Binaries\Win64\UnrealEditor-Cmd.exe" "C:\dev\reincarnated-unreal\Reincarnated\Reincarnated.uproject" -unattended -nullrhi -nosound -ExecCmds="LoadMap /Game/TestMaps/MeshyImportTest; quit"'
   ```

**Acceptance:**
- PASS: 3/3 meshes import with bones intact + animatable
- YELLOW: 2/3 PASS + 1 has Control Rig regeneration issue (resolvable with manual rigging step documented)
- RED: ≤1/3 PASS or systemic Meshy-UE 5.7 incompatibility (escalate)

**Compose with** legolas research at `agentic_orchestration/legolas/research/2026-06-02-unreal-character-customization-research/synthesis.md` — CC5 + Mutable + Reallusion + FAB alternatives if Meshy → UE 5.7 path is blocked.

---

## 4. Criterion 3.3 — Image-pass-through-to-Meshy validation

**Scope:** per canonical 38 § 4 step 3.3 + canonical/story/asset-pipeline-meshy-swap-2026-05-22 — validate that direct substrate-image-pass-through to Meshy produces equal-or-better output vs the ChatGPT-gen path.

**Test pattern:**
1. Select 3-5 weapons from the museum-tier substrate subset (Royal Armouries / Met Museum weapons; high-quality images)
2. For each weapon, run TWO Meshy generation paths:
   - **Path A — Direct image-pass-through:** feed the museum image directly to Meshy → produces 3D model
   - **Path B — ChatGPT-gen intermediate:** feed image description to ChatGPT → produces synthetic image → feeds synthetic image to Meshy → produces 3D model
3. Compare outputs per weapon:
   - Mesh quality (poly count, surface fidelity)
   - Rigging quality (does it auto-rig sensibly?)
   - UE import compatibility (re-runs criterion 3.2 process)
   - Visual fidelity to original image

**Acceptance:**
- PASS: Path A produces equal-or-better output on ≥4/5 weapons → lock direct-pass-through as production default for ~91.5% of weapon assets (substrate-resident with quality-suitable image); ChatGPT-gen remains fallback for substrate coverage gap (~8.5%)
- YELLOW: Path A matches Path B but doesn't exceed (no clear winner) → keep both paths available; document selection rule
- RED: Path A significantly worse than Path B → lock ChatGPT-gen as default; investigate Meshy direct-pass-through limitations

**Cost:** Meshy generation cost per criterion ≈ $5-15 (10 generations across paths × 3-5 weapons); within $0 spike budget but flag for Matt if exceeds.

---

## 5. Criterion 3.4 — Niagara VFX consumes engine ability-spec JSON

**Scope:** verify Niagara VFX system in UE 5.7 can ingest an engine ability-spec JSON + produce a visible in-engine effect.

**Test pattern:**
1. Take 3 representative ability specs from engine output:
   - 1 elemental burst (fire / lightning / shadow — high-VFX)
   - 1 control effect (freeze / stun — geometry-aware)
   - 1 movement skill (teleport / leap-strike — position-dependent)
2. Configure a Niagara emitter to consume each spec:
   - Read geometry tag → choose emitter type (scatter / cone / area / etc.)
   - Read tempo → set spawn rate
   - Read element_primary → set color
   - Read range → set particle reach
3. Run in UE 5.7 scene; verify visible effect

**Acceptance:**
- PASS: 3/3 abilities produce visible Niagara VFX matching spec
- YELLOW: 2/3 PASS + 1 has Niagara module-incompatibility (documented + proposed workaround)
- RED: ≤1/3 PASS or systemic Niagara → engine JSON schema mismatch

---

## 6. Criterion 3.5 — PCG framework consumes engine geo-spatial output

**Scope:** verify UE 5.7 PCG (Procedural Content Generation) framework can ingest engine geo-spatial output (encounter / room layouts) + produce navigable room geometry.

**Test pattern:**
1. Take 2 representative encounter/room specs from engine output (or synthesize if engine doesn't yet emit room geometry directly)
2. Configure PCG graph to consume:
   - Room dimensions / shape
   - Spawn points
   - Obstacle / cover positions
3. Generate room geometry in UE 5.7
4. Verify navmesh generates over the room + AI can pathfind

**Acceptance:**
- PASS: 2/2 rooms generate + navigate
- YELLOW: 1/2 PASS + 1 has resolvable PCG configuration issue
- RED: PCG can't ingest engine geo-spatial output (schema gap; engine doesn't yet emit room-layout JSON — defer this criterion to engine-side workstream)

**Note:** if engine doesn't yet emit room-layout JSON at all, mark this criterion as DEFERRED (not RED) with cross-reference to engine workstream that produces it. Does NOT block port workstreams 1-3.

---

## 7. Criterion 3.6 — TAA/TSR fast-combat readability

**Scope:** validate UE 5.7's TAA (Temporal Anti-Aliasing) + TSR (Temporal Super Resolution) handle fast-combat motion without blur compromising readability.

**Test pattern:**
1. Create a UE 5.7 test scene with 1 Meshy-imported humanoid character (from criterion 3.2)
2. Apply rapid motion: character runs + attacks + dashes at ARPG-typical speeds (10-20 m/s movement; 200-400ms attack swing)
3. Capture frames at 60fps target; measure:
   - Motion blur visibility (does the character read clearly during dash?)
   - Edge clarity (anti-aliased edges hold up under motion?)
   - VFX legibility (Niagara effects from 3.4 don't smear into noise?)
4. Test both TAA and TSR (compare); test at PC native + projected mobile resolution

**Acceptance:**
- PASS: combat reads clearly at 60fps; no major blur compromise; TSR preferred over TAA for fast-motion
- YELLOW: blur acceptable at PC but mobile projection borderline (note + flag for WS5 mobile-polish)
- RED: blur compromises readability at PC (systemic problem; UE 5.7 TAA/TSR tuning needed — escalate to mantis design call)

---

## 8. Criterion 3.7 STRETCH — 3D cosmograph viability

**Scope:** validate procedural Niagara rendering of 3D cosmograph achieves target performance + visual quality before WS2 port workstream commits to the 3D approach.

**Test pattern:**
1. Build a minimal Niagara point cloud renderer in UE 5.7:
   - 100 stars at procedurally-generated 3D positions (mimicking UMAP output distribution)
   - Per-star color + brightness driven by configurable parameters
   - Procedural constellation lines connecting random subsets (mimicking kit primitive-set composition)
   - 1-2 nebula volumetric effects for atmospheric depth
2. Run in UE 5.7 with Lumen GI + Nanite (if applicable) + post-process atmospherics
3. Measure:
   - FPS sustained on PC at native resolution (target ≥60fps)
   - FPS on mobile-projected resolution (target ≥30fps at mid-tier)
   - Visual register: does it feel like a cosmos? (subjective; Matt + gandalf assess via screenshots)
   - Memory budget: scene RAM + GPU memory usage
4. Validate the substrate-led discipline holds: positions ARE the substrate; atmospherics are decorative

**Acceptance:**
- PASS: 60fps PC + 30fps mobile-projected + cosmos register confirmed + memory budget reasonable → 3D cosmograph approach VIABLE; WS2 commits to 3D
- YELLOW: PC passes; mobile borderline → 3D viable but mobile needs WS5 polish pass
- RED: PC drops below 60fps OR cosmos register doesn't materialize OR memory blows out → 2D approach may be retained for UE port (loss of cosmos-register elevation; substrate-led architecture preserved)

**Compose with:** legolas FAB asset short-list (parallel sub-step) — if FAB assets accelerate atmospheric polish, 3D cosmograph viability strengthens.

---

## 9. Legolas-collaboration sub-step — FAB asset research

**Fires PARALLEL with criteria 3.1-3.6 (does not block sequential spike progress).**

**Scope (legolas Mode A):** research UE FAB + UE marketplace cosmic-VFX assets compatible with UE 5.7 + composable with procedural Niagara cosmograph rendering.

**Target asset classes:**
- Nebula Niagara VFX packs (volumetric atmospheric polish)
- Cosmic dust / stardust particles (background atmospherics)
- Lens flare / bloom packs (per-star brightness elevation)
- Skybox space textures (8K starfield backdrops)
- Constellation-line aesthetics (3D ribbon/glow reference patterns)
- UE 5.7 confirmed-compatibility filter (critical)

**Output:** `agentic_orchestration/legolas/research/ue-fab-cosmograph-vfx-survey-2026-06-XX/short-list.md` — 5-10 curated assets with:
- Asset name + creator + price
- UE 5.7 compatibility verification (per FAB listing or empirical test)
- Composability with procedural Niagara cosmograph
- Cost: free vs paid (Matt authorizes paid)
- Acquisition status (installed on PC? available on FAB? sample-validation done?)

**Time:** ~half-day legolas Mode A time; ~$0 (research only; asset install + integration falls to mantis).

**Cross-reference:** existing legolas research at `agentic_orchestration/legolas/research/2026-06-02-constellation-form-ue-techniques/synthesis.md` may already cover much of this; legolas extends + filters for UE 5.7 compatibility.

---

## 10. Discipline anchors

| Discipline | Application in this spike |
|---|---|
| #5 — Right tool for validation question | Each criterion has a specific empirical test; use the right tool for that test (e.g., headless cook test, in-editor inspection, perf profiler) |
| #11 — Empirical inspection before assumption | Every criterion verdict is grounded in empirical measurement; not in Meshy / UE marketing claims |
| #18 — Math-hotspot methodology consultation | If criterion 3.7 stretch surfaces a math-hotspot decision (LOD algorithm; UMAP 3D math), consult gandalf via Pattern-A query |
| #41 — Substrate-led discipline | Render what the substrate says; cosmograph 3D positions stay UMAP-derived; do NOT manufacture positions to fit aesthetic |
| #42a — Framing-audit | Q1-Q3 applied at spike start; per-criterion framing-audit before each test fires |
| #43 — Design-quality wave-close audit | Apply at spike close before final verdict |
| #46 — DB anti-materialization | Apply if criterion 3.5 PCG uses engine telemetry queries |
| #48 — R48.4 host-RAM-aware concurrency | UE Editor + Visual Studio + Niagara compile compete for PC RAM; respect single-seam during heavy operations; pre-flight `wmic OS get FreePhysicalMemory` before each fire unit |
| #59 — Substrate coverage honesty | If criterion 3.5 PCG depends on engine geo-spatial output that doesn't exist yet, surface as DEFERRED not RED |
| D7 — AI-tell line (canonical 38) | No raw LLM-named content in any test scene; Meshy-generated meshes are imported as raw mesh data (player-facing identity layer is downstream) |

---

## 11. Pre-commission Pattern-A query opportunity

Mantis is authorized to fire a single Pattern-A query to gandalf BEFORE primary criterion testing fires if spike scoping surfaces:
- Engine JSON schema gap that materially blocks Meshy + Niagara + PCG ingestion
- Meshy 6 API breaking changes since canonical 38 § 4 acceptance criteria authoring (2026-05-23)
- UE 5.7 plugin compatibility gap that affects Niagara / PCG / TSR
- Other load-bearing question that materially affects spike sequencing

Pattern-A query format: cheapest empirical refutation; ~30-min surface time to gandalf.

---

## 12. Spike close protocol

When all 6 primary criteria + 1 stretch + legolas sub-step complete:

1. Author `port-workstream-gating-verdict.md` with overall verdict:
   - **OVERALL GREEN:** all 6 primary PASS; stretch PASS or YELLOW → WS1-WS5 port workstreams can fire
   - **OVERALL YELLOW:** most primary PASS; specific resolvable issues documented → WS1-WS5 fire with documented mitigations
   - **OVERALL RED:** systemic blocker on ≥2 primary criteria → port workstreams delayed; escalation to gandalf + Matt for replanning
2. Author wave-close record at `canonical/story/2026-06-XX-ue-architecture-validation-spike-wave-close.md`
3. Notify gandalf via dispatch-response
4. Port workstream WS1 (data layer) commission spec authoring fires (gandalf) post-spike-GREEN
5. No push to remote required from spike (gandalf + Matt coordinate push pattern)

---

## 13. Sign-off

**Authored:** gandalf 2026-06-06 per UE workstream pre-scoping ratification post-cosmograph-Phase-A close
**Authority:** Matt 2026-06-06 design call — UE workstream sequencing per canonical 38 § 4 + cosmograph-pivot architectural-anchor lock + atomic-substrate-registry + hypothesis-flow CANONICAL
**Anchor evidence:** canonical 38 § 4 acceptance criteria 3.1-3.6 + 3D cosmograph viability stretch surfaced 2026-06-06 + 2026-05-31 UE seam placement decision + 5.5→5.7 migration test verified clean (`af4a71b1b05659942` general-purpose agent)
**Empirical-evidence trigger for downstream commissions:** spike PASS at criteria 3.1-3.6 (+ stretch 3.7 outcome informing 2D-vs-3D port direction) → WS1 data layer port commission authoring fires

**End of spike dispatch.**
