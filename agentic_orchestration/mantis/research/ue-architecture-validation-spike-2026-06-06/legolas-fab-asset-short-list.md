# Legolas FAB Asset Short-List — Mantis Integration Notes
# 2026-06-06

**Source:** `agentic_orchestration/legolas/research/ue-fab-cosmograph-vfx-survey-2026-06-06/short-list.md` (commit f989302)
**Purpose:** mantis integration notes and acquisition readiness for criterion 3.7 STRETCH cosmograph test
**Status:** Research COMPLETE (legolas); Mantis integration PENDING UE 5.7 project verification

---

## Acquisition status

| Asset | Cost | UE 5.7 | Acquired on PC | Install status |
|---|---|---|---|---|
| 1. Epic Niagara Examples Pack | FREE | CONFIRMED | No | Pending |
| 2. VDB Nebula (Arghanion) | FREE | INFERRED (5.3+, low risk) | No | Pending |
| 3. Cosmic Forge Skybox (Arghanion) | PAID (price TBD) | INFERRED (low risk) | No | Pending Matt auth |
| 4. 8K HDRI Galaxy (Mathew81) | PAID (~$10-20) | CONFIRMED (engine-agnostic HDR) | No | Pending Matt auth |
| 5. LENS FLARE VFX | $29.99 | CONFIRMED-VERBATIM | No | Pending Matt auth |
| 6. Cinematic Lens Flares v4 | PAID (price TBD) | NOT CONFIRMED | No | Deferred |
| 7. Niagara Constellations | PAID (price TBD) | NOT CONFIRMED (medium-high risk) | No | Deferred — reference study only |
| 8. Niagara Galaxy | $29.99 | NOT CONFIRMED (low-med risk) | No | Deferred |
| 9. Volumetric Nebula and Clouds | $49.99 | NOT CONFIRMED (medium risk) | No | Deferred |

**Free-path total cost:** $0 (Assets 1 + 2)
**Minimal paid-path total:** ~$29.99 (add Asset 5)
**Full acquisition ceiling:** ~$130-150 (all paid assets)

---

## Substrate-led discipline check (per dispatch § 9 / legolas survey)

All 9 assets are classified CLEAR or CONDITIONAL in the legolas survey:
- Assets 1-6, 8, 9: CLEAR — purely atmospheric/decorative, do not distort substrate positions
- Asset 7 (Niagara Constellations): CONDITIONAL — pre-authored fixed topology; use as reference only; NOT as cosmograph output. Custom procedural Niagara system required for production.

**Discipline #41 compliance:** confirmed by legolas survey. Mantis will verify at install time.

---

## Mantis installation notes (to be completed when UE 5.7 project verified)

### Asset 1 — Epic Niagara Examples Pack
- Open Epic Launcher → Library → My Assets → Search "Niagara Examples"
- Add to Project: select Reincarnated project + UE 5.7
- No plugin dependency; native UE5.7 pack
- First action after project verification

### Asset 2 — VDB Nebula (Arghanion)
- Add from FAB via Epic Launcher (search "VDB Nebula Arghanion")
- Alternatively: get from Gumroad with coupon VDBNEBULA100 (free)
- After install: verify Heterogeneous Volumes actor is available in UE5.7 (it is — native feature since 5.3)
- Test: place Heterogeneous Volumes actor in test scene; assign VDB material; confirm renders without errors

### Asset 5 — LENS FLARE VFX (when Matt authorizes $29.99)
- Add from FAB: https://www.fab.com/listings/0e920fbc-fb78-4331-a4e1-878dc3504bad
- UE 5.7 compatibility: CONFIRMED-VERBATIM (4.27 And 5.0-5.7)
- Sprite-based: each Niagara star can have one lens flare component
- Integration: spawn a lens flare actor per star; wire `StarBrightness` Niagara User Parameter to flare intensity
- Test: confirm 100 simultaneous flare instances ≥60fps on PC

---

## Version verification checklist (to complete at install time)

For each asset, open in Epic Launcher → check "Supported Engine Versions" field:
- [ ] Asset 1: should show 5.7 (Epic confirmed)
- [ ] Asset 2: should show 5.3+ (inferred; verify)
- [ ] Asset 3: verify version range
- [ ] Asset 4: N/A (pure HDR textures, engine-version-agnostic)
- [ ] Asset 5: should show 4.27-5.7 (confirmed verbatim)
- [ ] Assets 6, 7, 8, 9: MUST verify before acquisition (risk status UNCONFIRMED)

---

*Integration handoff complete. Awaiting UE 5.7 project verification to begin install sequence.*
