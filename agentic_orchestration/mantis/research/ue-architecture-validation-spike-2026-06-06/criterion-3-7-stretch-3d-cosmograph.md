# Criterion 3.7 STRETCH — 3D Cosmograph Viability

**Verdict:** IN PROGRESS (Session 1 — framework built; execution pending UE 5.7 project verification)
**Date:** 2026-06-06 Session 1
**Legolas FAB survey:** CONSUMED from `agentic_orchestration/legolas/research/ue-fab-cosmograph-vfx-survey-2026-06-06/short-list.md` (commit f989302)

---

## 0. Context from prior research

Two legolas research deliverables inform this criterion:

1. **`2026-06-02-constellation-form-ue-techniques/synthesis.md`** — core constellation rendering technique:
   - Dual-renderer Niagara plexus: Emitter A (star sprites via `Sample Skeletal Mesh`) + Emitter B (constellation lines via `SpriteBasedLine` module reading Particle Attribute Reader)
   - For the *cosmograph* (not per-character): adapt Emitter A to spawn at substrate-UMAP-derived 3D positions (not skeleton vertices)
   - `EmergenceAlpha` DMI parameter pattern for substrate → visual feature binding
   - Blueprint → Niagara User Parameter binding fully supported, per-tick updatable

2. **`2026-06-06/short-list.md` (legolas FAB survey)** — 9 assets for atmospheric polish:
   - Asset 1: Epic Niagara Examples Pack (UE5.7, FREE) — foundation
   - Asset 2: VDB Nebula by Arghanion (5.3+, FREE) — volumetric nebula backdrop
   - Asset 3/4: Skybox HDRIs (PAID ~$10-20 each) — far-background
   - Asset 5: LENS FLARE VFX (5.7 CONFIRMED-VERBATIM, $29.99) — per-star brightness
   - Asset 7: Niagara Constellations (version UNCONFIRMED) — reference study only
   - Asset 8: Niagara Galaxy (version unconfirmed, $29.99) — background vortex
   - Asset 9: Volumetric Nebula and Clouds (version unconfirmed, $49.99) — only if VDB insufficient

---

## 1. Planned test architecture

### 1.1 Scene composition

```
[Scene: TestCosmograph_Spike_37]
  - HDRI Backdrop / SkyLight source: Asset 3 or 4 (or procedural for test)
  - Heterogeneous Volumes actor: Asset 2 VDB Nebula (mid-distance atmospheric)
  - NS_Cosmograph_PointCloud (custom Niagara):
      - 100 star particles at UMAP-derived 3D positions
      - Per-star sprite: emissive, additive blend, brightness driven by substrate tier
      - Constellation lines: SpriteBasedLine module connecting adjacent kit pairs
  - (optional) Asset 5 lens flare instances at per-star positions
```

### 1.2 Niagara point cloud architecture (custom — NO drop-in pack)

The cosmograph position data is UMAP-derived substrate coordinates. It violates substrate-led discipline to use a pre-authored constellation (Asset 7 fixed topology) as the cosmograph output — those are visual references only.

The custom Niagara system:

**Emitter A — Star positions:**
```
Spawn module: Spawn Per Frame (100 particles, once)
Position: consume JSON-provided 3D coordinates (or procedural mock for spike)
  → For spike: use Grid3D / In Line Array module with 100 hardcoded UMAP-analogue positions
  → For production WS2: consume cosmograph JSON packet position array via Blueprint
Render: Sprite Renderer
  Material: Emissive additive, UnlitSprite, parameter: StarBrightness (float), StarColor (vec3)
  Size: driven by substrate tier (T1=small, T4=large)
```

**Emitter B — Constellation lines:**
```
Spawn module: Spawn Per Frame (N line segments, once)
  → For spike: wire pairs per the kit-primitive-set composition adjacency
  → Uses SpriteBasedLine module (built-in UE5.1+) reading Emitter A particle positions
Render: SpriteBasedLine renderer
  Material: Emissive additive line, parameter: LineOpacity (float), LineColor (vec3)
  Tension: 1.0 (straight lines = constellation diagram aesthetic)
```

### 1.3 Cosmograph JSON ingestion path (production target, validated in spike)

The spike will verify that UE5 Blueprint can:
1. Read a JSON file from disk via `FFileHelper::LoadFileToString` (C++) or Blueprint JSON library
2. Parse an array of `{star_id, x, y, z, tier, element_primary}` records
3. Feed positions to Niagara via `UNiagaraDataInterfaceArrayFunctionLibrary::SetNiagaraArrayVector` (UE5 confirmed API)
4. Feed per-star attributes to Niagara User Parameters via `SetNiagaraVariableFloat`/`SetNiagaraVariableLinearColor`

This is the production ingestion path. For the spike, a hardcoded JSON file with 100 procedural positions will be used as the data source.

---

## 2. Asset acquisition plan (legolas priority sequence)

**Free-path (before Matt authorization needed):**
1. Asset 1 — Epic Niagara Examples Pack: download via Epic Launcher, add to project
2. Asset 2 — VDB Nebula: add from FAB via Epic Launcher (FREE, coupon VDBNEBULA100)

**Paid path (pending Matt authorization, ~$30-60 minimum):**
3. Asset 3 or 4 — Skybox: verify price on FAB before requesting (~$10-20)
4. Asset 5 — LENS FLARE VFX: $29.99, UE5.7 CONFIRMED-VERBATIM

**Do not acquire without additional Matt authorization:**
- Asset 6 (Cinematic Lens Flares v4): price unconfirmed, version unconfirmed
- Asset 7 (Niagara Constellations): version risk MEDIUM-HIGH; acquire only for reference study
- Asset 8 (Niagara Galaxy): $29.99, version unconfirmed
- Asset 9 (Volumetric Nebula): $49.99, version unconfirmed, highest integration complexity

**Maximum authorization request:** ~$130-150 total if all paid assets are acquired. Recommend requesting Assets 3/4 + 5 first (~$40-50) and evaluating cosmos-register before committing to Assets 8/9.

---

## 3. Acceptance criteria (per dispatch § 8)

| Test | Target | Pass condition |
|---|---|---|
| PC FPS at native resolution | ≥60fps | Sustained at target resolution with 100 stars + constellation lines + VDB nebula |
| Mobile-projected FPS | ≥30fps | At mid-tier mobile resolution settings (720p, scalability Medium) |
| Cosmos register | Subjective | Matt + gandalf assess via screenshots: "does it feel like a cosmos?" |
| Memory budget | Reasonable | Scene RAM + GPU memory within D8 mobile-aware budgets |
| Substrate-led position check | Pass | Star positions are UMAP-derived (or procedural analogue); NOT pre-authored fixed topology |

---

## 4. Current execution gate

**Blocked by:** UE 5.7 smoke test result (running at Session 1, PID 15600).
- If Cook PASS → project verified for 5.7 → create test map → author custom Niagara → install free assets → run FPS test
- If Cook FAIL → investigate migration issue → resolve or escalate

**Estimated sessions after gate clears:** 2-3 sessions to author + test + profile the minimal cosmograph demo.

---

## 5. Substrate-led discipline check

Per dispatch § 8 point 4: "Validate the substrate-led discipline holds: positions ARE the substrate; atmospherics are decorative."

The test will verify:
- Star positions come from the UMAP-derived coordinate array (procedural mock for spike = acceptable; substrate must feed production)
- VDB nebula, skybox, lens flares are purely additive over the point cloud
- Constellation line topology derives from the kit primitive-set adjacency (not pre-authored fixed constellations from Asset 7)
- No manufactured star added to fill aesthetic gaps

---

*Criterion 3.7 status: IN PROGRESS — execution begins after UE 5.7 smoke test confirms project stability.*
*Legolas FAB survey integration: COMPLETE — asset priority sequence documented, free-path clear.*
