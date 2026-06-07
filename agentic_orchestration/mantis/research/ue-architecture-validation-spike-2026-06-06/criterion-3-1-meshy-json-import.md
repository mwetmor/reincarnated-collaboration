# Criterion 3.1 — JSON → Meshy Import

**Verdict: PASS** ✅ (with one noted limitation → gates criterion 3.2 scope)
**Date:** 2026-06-06 Session 1
**API:** Meshy v2 text-to-3D endpoint, preview mode

---

## Substrate tuple → prompt construction

Engine JSON (cycle-14 wave-5 season-001) encodes BC-axis signature in kit_id and provides identity narrative via `wave_b_identities.json`. Full substrate fields (element_primary, cultural_tradition, weapon_form_token) were derived from kit identity narratives per the substrate-to-prompt mapping below.

| Kit | kit_id | Substrate signal | Meshy prompt theme |
|---|---|---|---|
| Kit A — Ember Sweeper | `S1_endgame_bc_melee_high_flat_dex_none_s0` | fire (name: Scorch Line), DEX (kit_id), European melee | Agile fire warrior, light European armor, curved blades |
| Kit B — Tide Warden | `S1_endgame_bc_melee_high_variable_wis_none_s0` | holy (narrative: "holy force"), WIS, East Asian ("east asian martial discipline") | East Asian warrior monk, flowing robes, staff |
| Kit C — Duskweaver type | shadow/INT archetype per canonical ground-state | shadow (Dusk, Eclipsed, Twilight), INT, robes/grimoire | Shadow arcane caster, dark robes, orb-staff |

**Note on substrate gap:** cycle-14 JSON does not include explicit `element_primary` or `cultural_tradition` field in the kit_id or wave_b_identities output. These were derived from the identity narrative. For production, star-lord should add substrate_trace fields to the export packet (cross-seam finding filed in spike report).

---

## Meshy submissions

| Kit | Task ID | Status | Credits |
|---|---|---|---|
| Kit A (Ember Sweeper/fire/DEX) | `019ea025-fe66-71d2-b139-2687d74b5aa5` | SUCCEEDED | 20 |
| Kit B (Tide Warden/holy/WIS) | `019ea026-074b-705d-ac86-6d5f2405e8ec` | SUCCEEDED | 20 |
| Kit C (Duskweaver/shadow/INT) | `019ea026-100e-7339-bc41-c57937bba495` | SUCCEEDED | 20 |

**Total cost: 60 credits (~$3 at ~$0.05/credit). Within $20 spike budget.**

---

## Mesh quality evaluation

| Metric | Kit A | Kit B | Kit C | Target | Pass? |
|---|---|---|---|---|---|
| Triangles | 49,579 | 49,673 | 49,720 | 30K–80K | ✅ |
| Vertices | 49,281 | 49,436 | 49,415 | — | ✅ |
| OBJ file size | 8.01 MB | 8.04 MB | 7.98 MB | — | ✅ |
| GLB file size | 6.56 MB | — | 6.44 MB | — | ✅ |
| Humanoid shape | ✅ (dual-blade warrior) | ✅ (sage with staff) | ✅ (robed caster) | required | ✅ |
| Mesh appears closed | ✅ (from preview) | ✅ (from preview) | ✅ (from preview) | required | ✅ |
| Textures | — (preview mode) | — (preview mode) | — (preview mode) | readable | N/A |

### Visual quality notes (from thumbnail inspection)

**Kit A (Ember Sweeper):** Dynamic dual-blade crouching combat pose. Hooded, armored warrior with curved swords. Fire aesthetic achieved via aggressive posture and blade design. Limbs clearly distinct — favorable for auto-rigging.

**Kit B (Tide Warden):** Bearded East Asian sage-warrior with topknot, flowing robes, elaborate staff with figure at top. Older male appearance matches "wise monk" aesthetic. Cultural tradition accurately rendered.

**Kit C (Duskweaver):** Shadow mage in long flowing dark robes. Hooded, holding orb-staff. Cast pose. Cloth topology may challenge rigging slightly (Meshy needs to estimate bone influence through draped fabric).

---

## Critical finding: FBX skeleton status

**Meshy text-to-3D preview mode does NOT include skeleton/bone data in the FBX export.**

Empirical verification: Kit A FBX downloaded (3.7 MB), parsed for skeleton markers — zero bone entries found.

This is expected: Meshy's rigging is a SEPARATE STEP performed in the web app:
1. Open task in Meshy web app
2. Click "Rig Character" (auto-detects humanoid skeleton)
3. Export with "Unreal Engine" preset → FBX + Control Rig

The text-to-3D API delivers mesh + texture (after refine). Rigging requires the web app step.

**Implication for criterion 3.2:** criterion 3.2 requires a manual Meshy web app step to add the humanoid rig. Matt must log into Meshy web app, rig these 3 tasks, and export with UE5 preset. Mantis then imports the rigged FBX into UE 5.7.

---

## Acceptance evaluation

- **PASS:** 3/3 kits produced usable humanoid 3D models. ✅
  - Poly count within range (all ~49,600 tris = within 30K-80K) ✅
  - Mesh appears closed (no visible holes in preview thumbnails) ✅
  - Textures: preview mode = unshaded; textures generated in refine step (not evaluated for criterion 3.1)
  - All three clearly humanoid (two legs, two arms, head, distinct body segments) ✅

**Criterion 3.1: PASS**

---

## Cost tracking

| Item | Credits | $ (est.) |
|---|---|---|
| Kit A text-to-3D preview | 20 | ~$1.00 |
| Kit B text-to-3D preview | 20 | ~$1.00 |
| Kit C text-to-3D preview | 20 | ~$1.00 |
| **Total criterion 3.1** | **60** | **~$3.00** |

Running spike Meshy spend: ~$3.00 of $20 budget used.

---

## Artifacts

| File | Location |
|---|---|
| Kit A thumbnail | `meshy-3d-outputs/KitA_EmberSweeper_thumb.png` |
| Kit B thumbnail | `meshy-3d-outputs/KitB_TideWarden_thumb.png` |
| Kit C thumbnail | `meshy-3d-outputs/KitC_Duskweaver_thumb.png` |
| Kit A GLB | `meshy-3d-outputs/KitA_EmberSweeper.glb` |
| Kit C GLB | `meshy-3d-outputs/KitC_Duskweaver.glb` |
| Kit A OBJ | `meshy-3d-outputs/KitA_EmberSweeper.obj` |
| Kit B OBJ | `meshy-3d-outputs/KitB_TideWarden.obj` |
| Kit C OBJ | `meshy-3d-outputs/KitC_Duskweaver.obj` |
| Task JSONs | `meshy-3d-outputs/Kit[A/B/C]_task_result.json` |

---

*Criterion 3.1: PASS — 3/3 usable humanoid meshes at target poly count. Rigging step (for 3.2) requires Meshy web app, not API.*
