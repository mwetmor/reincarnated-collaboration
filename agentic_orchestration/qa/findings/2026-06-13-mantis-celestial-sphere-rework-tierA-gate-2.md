# Finding — 2026-06-13 — mantis celestial-sphere rework Tier-A (Gate-2, post-output)

**Reviewer:** sam (PC-seam)
**Severity:** PASS-WITH-WARN (1 WARN, 2 INFO; no BLOCK) — **scoped to Tier-A (A1–A7) ONLY**
**Target:** commit `1828499` on `main`, tag `mantis/v1.0-celestial-sphere-rework-tierA-1`
**Developer:** mantis (UE 5.7 seam)
**Scope:** PC-seam only (`reincarnated-unreal/`); consumes `cosmograph_sphere_001000stars_R8000.json` read-only; no engine JSON-contract write
**Mode:** DEV-MODE / Gate-2 critique-pair Pattern E
**Principles applied:** #1 (math-before-code), #2 (smoke-gate / empirical-evidence), #4 (decisions-log single source of truth), #5 (severity matters); Discipline #1; D7; R48.4
**Gate-1 predecessor:** `agentic_orchestration/qa/findings/2026-06-13-mantis-celestial-sphere-rework-gate-1.md` (PASS-WITH-WARN, 4 WARN)

## Verdict

**PASS-WITH-WARN — Tier-A.** Mantis closed every headless-closeable Tier-A criterion to standard, honored Discipline #1 at the load-bearing point (the 1,005,000 root-cause is a genuine structural diagnosis, not a knob-turn), and applied my Gate-1 WARN-1 fallback correctly — STOPPED at the unbridgeable Niagara edit class and produced an ordered manual-BP list rather than forcing a windowed editor over SSH. Nothing in the commit persists session-only state into the level. The single WARN is a documentation-completeness gap on the figure-lighting DIRECTION (A4), not a correctness defect. **No BLOCK.**

**Tier-B (B1–B5) remains OPEN and is NOT gated by this verdict** — it confirms post-render with Matt at the `TheSa` console per dispatch § 7.4 / my Gate-1 WARN-4. The wave-close push is authorized by this Tier-A PASS and does not wait on the render pass.

---

## What I found

The commit (`1828499`) contains exactly the two declared Tier-A deliverables (`notes/2026-06-13-celestial-sphere-math-transform-and-particle-count-rootcause.md`, `notes/...-MANUAL-BP-STEPS-for-matt-console.md`) and nothing else — no `.umap`, no `.uasset`, no `.ini`, no `Saved/` artifact (verified via `git show --name-only`). The math/transform note root-causes the 1,005,000 count to a structural cause (a `duplicate_asset`-cloned point-cloud system, `NS_CelestialSphere` ex `NS_CosmographPointCloud`, whose `StarPositions` array was never bound, running inherited CPUSim + SpawnBurst_Instantaneous × InfiniteLoop spawn — runtime-accumulated against the 1M CPU cap, decoupled from the 1,000-star JSON). The coordinate transform is correct (verified independently: Rx(+90°) → `(x,−z,y)` maps source +Y pole → UE +Z up, det +1, |r|=8000 preserved). A6/D7 is PASS by construction. A7's `stat gpu` threshold is objectively measurable. A2/A3/A4/A5 were correctly handed to the M1–M7 manual list under the WARN-1 fallback. The one gap: A4 figure-lighting DIRECTION is specified in the manual-BP list (M4) and the partition table, but is thinner on the WHICH-rotation specificity than A1–A3 are on their respective math (see WARN-1 below).

## Per-criterion disposition (Tier-A only)

| # | Criterion | Disposition | Note |
|---|---|---|---|
| **A1** | 1,005,000 root-caused + documented | **CLOSED** | Genuine structural root-cause (absence-of-binding + CPUSim cap + infinite-loop accumulation), not a silent count reduction. Discipline #1 honored: count→1,000 is framed explicitly as a *consequence of binding real data*, not a knob-turn. Exact Spawn Count integer correctly deferred to M1 (unreadable from packed binary; honestly flagged). |
| **A2** | GPU sim; no CPU-cap warning | **DEFERRED → M2** (correct) | Not a bridge primitive (no `set_niagara_sim_target`); fixed-bounds requirement (±8200 UU ≥ R) correctly captured. |
| **A3** | `BP_CelestialSphere` drives `StarPositions`/`StarColors` on R=8000 sphere; origin cloud removed | **DEFERRED → M1/M3** (correct) | `set_niagara_parameter` has no array support; BP graph authoring is windowed. Transform application (`Rx(+90°)`) is made a hard, non-skippable step in M3b with a fallback (DataTable/Curve bake) that preserves the transform. |
| **A4** | Figure-lighting rig standalone, no-longer-black, motivated night-key + ambient fill (DIRECTION) | **DIRECTION specified → M4** | See **WARN-1** — direction is present and the root-cause hypothesis (directional lit-face aimed away) is sound, but the aim is given as a qualitative quadrant ("moon over the shoulder") rather than a concrete pitch/yaw the way A1–A3 carry their math. Acceptable for DIRECTION-now (§ 3 constraint 3 defers VALUES), but flagged. |
| **A5** | Rig A/B toggle wired + distinct poles | **DEFERRED → M5** (correct) | Toggle pre-exists (RigA/RigB tags from prior spike); distinctness read is a Tier-B values judgment, correctly partitioned. Correctly notes A5 closes the LIGHTING-RIG question only, NOT the aesthetic mundane-vs-supernatural read (§ 6 forward item). |
| **A6** | D7; stars/runes hand/JSON-authored, no runtime LLM | **CLOSED** | PASS by construction; render path has no LLM. |
| **A7** | Nebula cost-cut + `stat gpu` budget threshold documented | **CLOSED** | Threshold is objectively measurable: stable ≥30 s, GPU frame ≤16.6 ms (≥60 fps), flat/no-climb, HeterogeneousVolumes + VolumetricFog line-items each bounded. Lever-order on miss specified (MaxStepCount 32→16, DownsampleFactor 4→8 before disabling nebula). Good enough to gate Tier-B against. |

## Findings

### WARN-1 — A4 figure-light DIRECTION is qualitative where A1–A3 are quantitative
**Section:** math note § 8 partition table (A4 row); manual-BP M4
The Niagara/transform half of the dispatch carries exact math (R=8000, `Rx(+90°)`→`(x,−z,y)`, ±8200 bounds). The figure-light DIRECTION half carries a *qualitative* aim ("high, slightly-behind-camera key… moon over the shoulder… pitch it down from the camera's upper-front quadrant") plus the correct root-cause hypothesis (a directional whose lit `-X` face points away → black-in-Lit). This is defensible — dispatch § 3 constraint 3 explicitly defers VALUES to Tier-B M7 tune-on-screen, and a directional light's aim is genuinely easier to set by eye at the console than to pre-derive blind — so this does NOT rise to BLOCK and does not hold the commit. But the asymmetry is worth recording: a downstream executor (Matt) gets a precise recipe for the sphere and a judgment-call for the light. M4 step 1 ("camera is at ~`(0,−300,170)` looking up/back toward the figure at origin") actually contains enough to state a concrete target aim-vector, and stating it would close the asymmetry.
**Citation:** Principle #1 (math-before-code — DIRECTION is the "math" tier for A4; it is present but softer than the geometry tier); Principle #5 (this is WARN, not BLOCK — DIRECTION-now/values-later is the dispatch's own design constraint, satisfied).
**Fix (non-blocking, optional):** In M4, convert the qualitative aim to a concrete starting rotation derived from the M4-stated camera vector `(0,−300,170)`→figure-at-origin (e.g. a directional aimed from the camera's upper-front toward origin, stated as pitch/yaw), as the *starting* value Matt then tunes on-screen. Not required for Tier-A PASS; tightens the M4 handoff.

### INFO-1 — Discipline #1 honored at the load-bearing point; the root-cause is genuine
**Section:** math note § 4
This is the criterion my Gate-1 INFO-1 flagged as the load-bearing unknown (the ~1,000× multiplier). Mantis did not reduce a count — it diagnosed *why* the count is 1,005,000 (inherited CPUSim emitter + SpawnBurst×InfiniteLoop, decoupled from JSON because the array was never bound) and showed the fix is *binding real data*, with the count→1,000 as a downstream consequence. The honesty marker is explicit ("The fix is NOT 'reduce the spawn count.' Reducing the inherited count would still spawn an origin cloud of the wrong stars."). The one residual — the exact per-burst Spawn Count integer — is correctly flagged as unreadable from the packed binary and deferred to M1 (read-it-at-console), not guessed. This is exactly the posture Discipline #1 requires. Recording as a strength.

### INFO-2 — WARN-1 fallback (Gate-1) applied correctly; pristine-level discipline held
**Section:** math note § 8; manual-BP § Pre-flight / Pristine-scene note; commit contents
My Gate-1 WARN-1 fallback was: *if the headless/bridge path cannot complete-and-verify a Niagara edit class, STOP and hand Matt an ordered manual-BP list rather than persist unverified mutations into the pristine level.* Mantis applied it precisely: no UE session opened, A2/A3 (no bridge path) and A4/A5 (DXGI-render-gated success) routed to an ordered M1–M7 list, and the commit persists zero level/config state (verified: only the two `.md` notes; no `.umap`/`.uasset`/`.ini`/`Saved/`). The pristine-scene note in the manual list correctly anticipates the original 12-actor scene (sphere deletion + CVar disarm reverted on reload) and writes the steps against that pristine state. This satisfies dispatch § 6 ❌ ("no saving session-only CVar/visibility state into the level") and my Gate-1 WARN-1 in full. Recording as a strength.

## M1–M7 manual-list completeness assessment (the load-bearing Gate-2 judgment for a split wave)

The list is **precise, ordered, and complete enough for Matt to execute Tier-B at the console without re-deriving anything.** Per-step acceptance is present (M1 "Record the Spawn Count number"; M2 "no 1M CPU-cap warning"; M3 "1,000 particles on R=8000, not origin cloud"; M4 "figure stays lit with celestial sphere OFF"; M6 re-enable; M7 `stat gpu` ≤16.6 ms / ≥30 s / flat). Pre-flight safety (CVar disarm BEFORE piloting `Cam_GroundLookUp`; free-cam only) correctly prevents a repeat of the GPU crash that lost the prior session. The Rx(+90°) transform is restated at M3b with a "DO NOT skip this" guard and a friction-fallback (DataTable/Curve bake) that still mandates the transform. Tier-A↔Tier-B mapping is stated at the foot of the list. The only completeness softness is the A4 aim (WARN-1) — a qualitative-not-quantitative starting rotation; every other step is executable as written.

## Cross-seam flag — STANDS DOWN (does not fire)

My Gate-1 caveat: *"If the 1,005,000 root-cause turns out to be a defect in how the engine-side JSON is consumed at the emitter binding, that would become a cross-cutting flag at Gate-2."* The condition is **not met.** Mantis root-caused the ~1,000× to the **ABSENCE of any binding** (the array was never bound; the emitter runs inherited point-cloud spawn that never saw the JSON), not to a defective consumption of the JSON. The note records star-lord's JSON export as verified clean (exactly 1,000 stars, RGBA stride-4, |r|=8000.0 min=mean=max). This is a UE-side wiring gap inside `reincarnated-unreal/`, wholly PC-seam-scoped. **No engine bug to raise; no Mac-jack-ryan / star-lord consultation required.** Per Principle #4, no decisions-log conflict (geometry lock already lives in canonical § 2.6; this is routine PC-seam implementation, not an architectural commitment).

## Tier-B explicit carve-out (NOT gated by this verdict)

Per dispatch § 7.4 + Gate-1 WARN-4: B1 (stars render on R=8000 sphere) / B2 (nebula renders look-up view without crash at the A7 threshold) / B3 (figure reads in Lit, values console-tuned) / B4 (Rig A key distinct from Rig B spirit-glow) / B5 (`stat gpu`/`fps`/`unit` captured) all confirm at Matt's console render session. They do **NOT** block this commit's Gate-2 or the wave-close push. Tier-B confirmation is a separate render-evidence pass. Mantis must NOT over-read a clean Rig A/B toggle on the `FigureStandIn` placeholder as closing the aesthetic mundane-vs-supernatural contrast (dispatch § 6 forward item; radagast↔Mac-gandalf consult on the real ambiguous-spirit visual).

## Action
- [x] sam: Tier-A Gate-2 PASS-WITH-WARN issued; wave-close push authorized (this PASS is the authorization moment per standing PC-seam wave-close pattern).
- [ ] mantis (optional, non-blocking): on a future pass, convert M4 figure-light aim to a concrete starting rotation per WARN-1 fix. Not required for Tier-A.
- [ ] Matt (at console, Tier-B render session): execute M1–M7; close B1–B5; report the M1 exact Spawn Count integer back to david-h/sam for the A1-arithmetic footnote.
- [ ] David-H: push accumulated wave commits at wave-close (this Tier-A PASS + session-boundary memo).

## References
- `agentic_orchestration/mantis/notes/2026-06-13-celestial-sphere-math-transform-and-particle-count-rootcause.md`
- `agentic_orchestration/mantis/notes/2026-06-13-celestial-sphere-MANUAL-BP-STEPS-for-matt-console.md`
- `agentic_orchestration/dispatches/2026-06-13-mantis-celestial-sphere-rework-and-figure-lighting-rig-repair.md` (§ 4 tier split, § 6 pristine constraint, § 7.4 Gate-2 Tier-A-only scope)
- `agentic_orchestration/qa/findings/2026-06-13-mantis-celestial-sphere-rework-gate-1.md` (predecessor; WARN-1 fallback, WARN-4 gate re-sequence)
- commit `1828499` / tag `mantis/v1.0-celestial-sphere-rework-tierA-1` (`git show --name-only` verified: 2 `.md` files only, no level/config mutation)
