# UE Architecture Validation Spike — Findings Report
# 2026-06-06 — Ongoing

**Status:** IN PROGRESS (Session 1 of ~1-2 weeks)
**Dispatch:** `agentic_orchestration/dispatches/2026-06-06-mantis-ue-architecture-validation-spike.md`
**Agent:** mantis (UE seam, PC-resident)
**Session:** 2026-06-06 Session 1

---

## Executive summary (updated each session)

Six primary criteria + one stretch criterion for the UE architecture-validation spike. Session 1 establishes the environment baseline, fires the UE 5.7 smoke test, and documents per-criterion status + blocking gates.

**Session 1 key findings:**
1. **UE 5.7 PASS.** Cook smoke test PASS — 290 cooked items, SM5+SM6 shaders, uproject migrated 5.5→5.7. UE 5.7 confirmed operational for spike.
2. **Criterion 3.1: PASS.** 3 kits (Ember Sweeper/fire/DEX, Tide Warden/holy/WIS East Asian, Duskweaver/shadow/INT) → Meshy v2 text-to-3D → humanoid meshes at ~49,600 triangles each. All clearly humanoid, closed-mesh, within 30K-80K target range. Cost: 60 credits (~$3.00 of $20 budget).
3. **Criterion 3.3: PASS.** Sidecar A (star-lord, 2026-05-23, 5 weapons × 2 paths) covers this criterion empirically. Tier-1 museum: Path 1 WINS. Tier-2 operational: EQUAL. Tier-3 game-render: Path 2 REQUIRED. Polearm policy confirmed. Production routing lock confirmed.
4. **Criterion 3.2: YELLOW.** Meshy API preview = mesh only, NO skeleton. Rigging requires Matt to run "Rig Character" in Meshy web app on 3 task IDs, then export with UE5 preset. Import test ready as soon as rigged FBX available.
5. **Criterion 3.5 (PCG geo-spatial) → DEFERRED.** Engine doesn't emit room-layout JSON — per dispatch § 6, DEFERRED not RED. Does NOT block WS1-3.
6. **Criterion 3.4 (Niagara JSON) + 3.7 (cosmograph):** UE 5.7 verified → execute next session. Ability-spec JSON drafted; Niagara system design documented.
7. **Legolas FAB survey consumed.** 9 assets shortlisted; free-path (Assets 1+2, $0) sufficient for 3.7 smoke test.

---

## Per-criterion status table

| # | Criterion | Verdict | Session |
|---|---|---|---|
| 3.1 | JSON → Meshy | **PASS** ✅ (3/3 humanoid meshes, ~49.6K tris each) | Session 1 |
| 3.2 | Meshy → UE 5.7 | **YELLOW** — awaiting Matt to rig kits in Meshy web app | Session 1 |
| 3.3 | Image-pass-through | **PASS** ✅ (Sidecar A: Path 1 wins Tier-1, conditional routing confirmed) | Session 1 |
| 3.4 | Niagara JSON | **IN PROGRESS** | Session 1 |
| 3.5 | PCG geo-spatial | **DEFERRED** (engine doesn't emit room JSON yet) | Session 1 |
| 3.6 | TAA/TSR readability | **YELLOW** — can run with UE Mannequin fallback if 3.2 delayed | Session 1 |
| 3.7 STRETCH | 3D cosmograph | **IN PROGRESS** — execute after UE 5.7 project confirmed ✅ | Session 1 |
| UE 5.7 migration | Smoke test | **PASS** ✅ (290 cooked items, SM5+SM6 shaders, uproject → 5.7) | Session 1 |
| Legolas sub-step | FAB asset survey | **COMPLETE** ✅ (legolas, commit f989302) | — |

---

## Detail: per-criterion findings

### Criterion 3.1 — JSON → Meshy

**File:** `criterion-3-1-meshy-json-import.md`
**Verdict:** BLOCKED
**Blocker:** Meshy API key not available in this agent session. Kit JSON in meta-repo (cycle-14 wave-5) has kit_name + identity_narrative but not the full substrate tuple Meshy prompt needs (element_primary, weapon_form_token, cultural_tradition, attribute). Need to either: (a) get full kit substrate from engine repo on Mac, or (b) Matt provide Meshy API key + 3 test kits' substrate specs.
**Non-blocker finding:** The kit JSON schema is understood. From `wave_b_identities.json` and `phase2_kit_candidates.json`, kit_ids encode the BC axis signature (e.g., `S1_endgame_bc_melee_high_flat_dex_none_s0`). The primary appearance descriptor for Meshy should be constructed from: `element_primary + attribute + cultural_tradition + weapon_form_token` per dispatch § 2.

### Criterion 3.2 — Meshy → UE 5.7

**File:** `criterion-3-2-meshy-ue-import.md`
**Verdict:** BLOCKED pending 3.1
**Pre-finding:** UE 5.7 project baseline confirmed running. Once 3.1 meshes are available, import test follows dispatch § 3 protocol exactly.

### Criterion 3.3 — Image-pass-through

**File:** `criterion-3-3-image-pass-through.md`
**Verdict:** BLOCKED pending Meshy API key
**Pre-finding:** Path-1/Path-2 routing policy fully documented in `canonical/story/asset-pipeline-meshy-swap-2026-05-22.md`. Museum images for 3-5 weapons can be sourced from Royal Armouries + Met Museum (URLs already in 89K substrate). Test protocol clear; just needs API key.

### Criterion 3.4 — Niagara VFX consumes ability-spec JSON

**File:** `criterion-3-4-niagara-json.md`
**Verdict:** IN PROGRESS (see detailed file)
**Session 1 findings:**
- Engine JSON schema understood from cycle-14 output. Kit BC-axis signature encodes: engagement geometry (melee/ranged/mid), damage amplitude (high/medium/low), amplitude variance (flat/spiky/variable), attribute (str/dex/int/wis), support chain type.
- Prior legolas synthesis (`2026-06-02-constellation-form-ue-techniques`) confirms Niagara can bind substrate fields to visual parameters via UE5 User Parameters + Blueprint.
- Niagara test map creation blocked pending UE 5.7 project verification (smoke test running).
- Ability-spec JSON schema: the engine's kit JSON carries enough substrate for Niagara parameterization (element_primary → emitter color, bc_geometry → emitter shape, engagement proxy → spawn rate). Need to verify exact field names from engine output JSON.

### Criterion 3.5 — PCG geo-spatial

**File:** `criterion-3-5-pcg-json.md`
**Verdict:** DEFERRED
**Rationale:** Per dispatch § 6: "if engine doesn't yet emit room-layout JSON at all, mark this criterion as DEFERRED (not RED) — does NOT block port workstreams 1-3." Engine doesn't emit room-layout JSON in cycle-14 output. This criterion is deferred to the engine workstream that adds geo-spatial emission. Cross-seam note to star-lord/gandalf: PCG integration needs a room-layout JSON schema commitment before WS4 (continuity) can engage.

### Criterion 3.6 — TAA/TSR fast-combat readability

**File:** `criterion-3-6-taa-tsr.md`
**Verdict:** BLOCKED pending 3.2 character
**Pre-finding:** UE 5.7 has TSR (Temporal Super Resolution) which supersedes UE 5.5 TAA for fast-motion clarity. Per D1 (canonical 38), TSR was explicitly named as the mitigation for TAA blur during fast combat. TSR must be validated against the actual Meshy-imported character once 3.2 completes.

### Criterion 3.7 STRETCH — 3D cosmograph viability

**File:** `criterion-3-7-stretch-3d-cosmograph.md`
**Verdict:** IN PROGRESS (see detailed file)
**Session 1 findings:** Legolas FAB survey consumed; full asset priority sequence documented. Free-path plan: Assets 1 (Epic Niagara) + 2 (VDB Nebula) = $0 entry cost, sufficient for a minimal cosmos-register smoke test. Paid additions (Asset 5 lens flares $29.99 for per-star brightness, Assets 3/4 skybox for backdrop) total $30-60 at minimal paid path. Matt authorization needed for any paid assets. Custom Niagara point cloud + SpriteBasedLine constellation technique (per 2026-06-02 synthesis) ready to implement once UE 5.7 project verified.

---

## Overall spike verdict (preliminary)

Not yet determinable. Primary blocking gates:
1. UE 5.7 smoke test result (running at Session 1 close — determines 3.4 + 3.7 viability)
2. Meshy API key (determines 3.1 → 3.2 → 3.3 chain)
3. Engine ability-spec JSON with full substrate fields (determines 3.4 quality)

Criteria that do NOT block port workstreams WS1-3:
- 3.5 PCG (DEFERRED — explicitly non-blocking per dispatch § 6)
- 3.6 TAA/TSR (evaluable post-3.2; blocking WS3 character payoff only)

**Most likely overall verdict after 3.1-3.4 complete:** OVERALL YELLOW → WS1-WS5 fire with documented mitigations. No RED indicators from research phase.

---

## Cross-seam findings (route to gandalf/star-lord)

1. **Engine JSON schema gap for Meshy:** cycle-14 kit output has identity/name but not the full substrate tuple mantis needs for Meshy prompt construction. Suggest star-lord add a `substrate_trace` field to the export packet that includes: `element_primary`, `attribute_primary`, `weapon_form_token`, `cultural_tradition`, `historical_period` per kit_id.

2. **PCG room-layout JSON:** engine doesn't emit this yet. When star-lord/gamora scope the room-layout export, mantis needs: `{room_id, dimensions: {x,y,z}, spawn_points: [{pos, type}], obstacle_positions: [{pos, radius}], navmesh_hint}` schema minimum.

3. **Pi share connectivity:** `\\reincarnated-pi.local` mDNS doesn't resolve from PC. `\\192.168.1.100` resolves via `Test-Path` but fails on actual directory access. Pi Phase 1 Samba may not be fully configured for PC→Pi direction. Not blocking current spike (engine JSON found in meta-repo), but will be needed for production pipeline.

---

*Report maintained by mantis across spike sessions.*
*Next update: after UE 5.7 smoke test result + Niagara test map execution.*
