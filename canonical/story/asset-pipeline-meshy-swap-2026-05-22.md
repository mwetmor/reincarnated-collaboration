# Asset Pipeline — Meshy Replaces Mixamo; Irregular-Monster Strategy

> **STATUS:** CURRENT (load-bearing as of 2026-05-23) — see `canonical/00-ground-state.md`
>
> **2026-05-23 amendment:** doc originally authored 2026-05-22 with Unity as target engine. Doc 38 (`canonical/38-downstream-delivery-strategy-2026-05-23.md`) D1 locked **Unreal Engine** on 2026-05-23. **Unity references in this doc should be read as Unreal going forward.** Conceptual mappings: Unity Animation Rigging package → Unreal Control Rig; Unity Humanoid Avatar → Unreal Skeletal Mesh + IK Retargeting; Unity VFX Graph → Unreal Niagara. Underlying pipeline shape is unchanged; engine target is updated.
>
> **2026-05-23 amendment:** § 3.6 added — **image-pass-through-to-Meshy** named as default pipeline path for substrate-resident weapons (~91.5% coverage on 89K substrate). Reduces ChatGPT image-gen step; aligns with D7 AI-tell line; grounded in real reference data.

**Date:** 2026-05-22 (amended 2026-05-23)
**Author:** gandalf (canonical doc skeleton; awaits legolas findings to finalize)
**Status:** **SKELETON — § 3.1-§ 3.5, § 4-§ 5 pending legolas Mode A research findings** (per `agentic_orchestration/dispatches/2026-05-22-legolas-meshy-pipeline-research.md`); **§ 3.6 RESOLVED 2026-05-23** ahead of legolas findings per substrate-evidence reasoning
**Authority:** Matt 2026-05-22 (explicit directive to swap Mixamo → Meshy where listed, conditional on Meshy capability research); Matt 2026-05-23 (Unreal lock D1 + image-pass-through Amendment A)
**Companion artifacts:**
- `agentic_orchestration/dispatches/2026-05-22-legolas-meshy-pipeline-research.md` — research commission
- `canonical/story/hive-mind-protocol-qd-engine-rebuild-2026-05-21.md` § 6.2.2 W1.9 + W1.10 — target of post-research amendment
- `canonical/story/gear-archetype-rule-table-v1-2026-05-22.md` — 15-archetype catalogue consumed in § 3
- `canonical/38-downstream-delivery-strategy-2026-05-23.md` — D1 Unreal lock; D7 AI-tell line; § 4 architecture-validation spike acceptance criteria (consumes § 3.6 below)
- `agentic_orchestration/weapon-library-import-wind-down-summary-2026-05-22.md` — 89,839 substrate + 82,191 image URLs (the substrate that § 3.6 consumes)

---

## 0. TL;DR

Matt 2026-05-22 directive: **replace Mixamo with Meshy across the asset pipeline** where listed in protocol v1.3 (§ 6.2.2 W1.9 + W1.10). Conditional empirical basis: Meshy's site documents built-in humanoid + quadruped rigging + 500+ prebuilt animations — covers the dominant player-form case cleanly without Mixamo dependency.

**Two scoping conditions** Matt surfaced that this doc captures:

1. **Weapon and gear pipeline (Priority 1 — gates the swap).** Whether Meshy can produce weapon and gear models, how Unity handles weapon/gear animation, and whether gear models need their own animations or rely on bone-anchored attachment. Without this, the 15-archetype gear catalogue (G1-LITE) and G5-LITE Unity integration have a pipeline gap.

2. **Irregular-monster pipeline (Priority 2 — scopes the swap).** Meshy's two-rig coverage (humanoid + quadruped) does not cover slimes, multi-segment serpents, hydras, eyeball/no-body monsters, insectoids, floating wraiths, or swarms. ARPG canon (and Reincarnated's trial-boss-gallery + spirit-form-library) needs these. The swap is still net-positive for the dominant case; this section scopes the alternate path for irregular monsters.

**Pipeline summary (under Meshy):**

```
PLAYER FORMS (humanoid + quadruped spirits):
  ChatGPT → Meshy (mesh + rig + animation) → Unity

MONSTERS (humanoid + quadruped):
  Same as player forms; Meshy-driven

MONSTERS (irregular topology):
  Asset Store packs (preferred) | Hand-authored signature bosses (~5-10/season)
  | Shader-based amorphous (slimes via vertex displacement) | Procedural swarms

GEAR + WEAPONS:
  [§ 3 pending legolas Priority 1 findings]
```

---

## 1. Why the swap

### 1.1 Historical context

Mixamo was named in protocol v1.0-v1.3 as the canonical free auto-rigger because at protocol authoring time, Meshy's rigging capability was less mature. The pipeline shape was `ChatGPT → Meshy (mesh) → Mixamo (rig + anim) → Unity (VFX attachment)` — Meshy was treated as mesh-only.

### 1.2 What changed (Matt 2026-05-22)

Matt confirmed via Meshy's site documentation:

> *Built-in Rigging & Animation. Rig humanoid and quadruped characters with a few clicks — no manual bone setups or Inverse Kinematics required. Choose from 500+ prebuilt animations, including walks, attacks, and jumps, ready for immediate use in your game development.*

Meshy now covers both rigging + animation. Mixamo's role collapses out of the pipeline.

### 1.3 Net swap benefits

| Dimension | Before (Mixamo step) | After (Meshy direct) |
|---|---|---|
| Vendor count | 2 (Meshy mesh + Mixamo rig/anim) | 1 (Meshy mesh + rig + anim) |
| TOS surface | 2 (Meshy + Adobe Mixamo commercial-use confirmation) | 1 (Meshy only) |
| Ratification gates (P1) | Mixamo TOS interpretation gate | Dropped |
| Manual hand-off steps per character | ~3 (Meshy export → Mixamo upload → Mixamo download → Unity import) | ~1 (Meshy export → Unity import) |
| Bone-remapping pipeline | Required (Mixamo → Unity Humanoid Avatar) | Not required (Meshy → Unity direct) |
| Format conversion friction | Real (FBX flavors differ) | Eliminated |

The swap is structurally cleaner. The two-rig coverage gap (humanoid + quadruped only) was always implicit in Mixamo too (Mixamo is also a humanoid-focused character animation library) — swapping doesn't reveal a new gap, it surfaces a gap that was always there.

---

## 2. What this swap explicitly does NOT change

- The substrate-as-cohesion architectural commitment (canonical/story stack; engine-internal)
- The QD-engine rebuild's P0-P7 critical path (this is a sub-phase pipeline change, not a phase reorganization)
- Any decisions about gear as derived-tag (G1-LITE) vs. full substrate (G-PROMOTE-v1.1)
- The 15-archetype gear catalogue itself (`canonical/story/gear-archetype-rule-table-v1-2026-05-22.md` § 2 — the catalogue is asset-pipeline-agnostic)
- The Reincarnated visual style register (`canonical/story/style-register.md` — locked separately)
- Engine-side telemetry, schema, or signature_gear_archetype derivation function (W1.15-LITE)
- T4-A Tier 4 architecture defaults (`canonical/story/tier-4-architecture-defaults-2026-05-22.md` — keystone authorship is design, not asset)
- Spirit-form library / gacha-accumulator (`memory/project_earth_meta_layer.md` — meta-layer design, not asset pipeline)

---

## 3. Weapon and gear pipeline [PENDING legolas Priority 1 findings]

**Skeleton structure (to be filled when legolas findings land):**

### 3.1 Unity weapon/gear animation pattern

[Pending: how Unity handles weapon and gear animation — bone-attachment vs. independent armature; Animation Rigging pattern; static-mesh vs. skinned-mesh for armor pieces; VFX Graph attachment for VFX-bearing gear]

### 3.2 Meshy weapon/gear capability

[Pending: whether Meshy produces weapon and gear models; output format; pivot-point handling; PBR material output for Unity consumption]

### 3.3 15-archetype production-path classification

For each archetype in `canonical/story/gear-archetype-rule-table-v1-2026-05-22.md` § 2:

[Pending table: archetype × hypothesis (A static-bone-attached / B own-rigging / C VFX-anchored) × Meshy-can-cover × alt-path-if-needed]

### 3.4 Confidence read on dominant-case coverage

[Pending: legolas's confidence read on whether Meshy + Unity Animation Rigging cleanly covers ~10-12 of 15 archetypes; alt-path enumeration for the remainder; budget/effort implications]

### 3.5 Open questions surfaced by Priority 1 findings

[Pending: any close-calls or design-call items legolas surfaces during research]

### 3.6 Image-pass-through path — DEFAULT for substrate-resident weapons (RESOLVED 2026-05-23)

**Decision (Matt 2026-05-23):** for weapons that exist in the weapon-knowledge substrate catalogue (`weapon_knowledge_entries`), the default Meshy input is the **substrate-resident reference image** (when available, license-clean, and quality-suitable) — NOT a ChatGPT-generated image. ChatGPT image generation is the **fallback path** for the substrate coverage gap only.

#### 3.6.1 Provenance of this decision

This path is enabled by the 2026-05-22 weapon-library-import campaign landing:
- 89,839 clean weapon knowledge entries
- **82,191 image URLs registered (URL-only per ADR policy) = ~91.5% image coverage**

Without the substrate, the ChatGPT-gen path was the only option. With the substrate, the substrate IS the reference library — and Meshy 6 can ingest reference imagery directly.

#### 3.6.2 Two pipeline paths

```
WEAPONS + GEAR — Image-pass-through path (DEFAULT for ~91.5% of substrate weapons):
  Substrate image URL → fetch + cache → quality-score gate → Meshy 6 → Control Rig → Unreal

WEAPONS + GEAR — Synthetic-gen fallback (~8.5% — substrate coverage gap):
  ChatGPT → Meshy 6 → Control Rig → Unreal
```

#### 3.6.3 Why this is right (four reasons)

| Win | Why it matters |
|---|---|
| **Authenticity uplift** | Real museum/wiki/community photographs > synthetic concept art. Royal Armouries' Edo katana photograph carries 400 years of provenance; DALL-E produces average-of-internet katana. **Direct alignment with D7 (AI-tell line) per doc 38.** |
| **Variance uplift** | 89K real weapons span 400+ years of metallurgy + regional craft + design lineages. DALL-E on same prompt produces variations of same idea. The substrate gives actual diversity, not synthetic diversity. |
| **Quality uplift** | Museum-API images are studio-lit professional photography (~1024×1024 or higher); typically higher source-quality than DALL-E HD output. Meshy 6 performs better on cleaner references. |
| **Provenance / legal clarity** | ~24K CC0 + ~12K CC-BY/permissive substrate has known-clean license. DALL-E output IP status remains contested. Direct-pass-through gives clearer legal grounding for commercial use. |

The **economic win is modest** in absolute dollars (~$120-300/year saved on ChatGPT image-gen at projected weapon-asset volumes). The **architectural-coherence wins are major** — same design instinct as pattern-recognition methodology (P2/P3) and substrate-as-cohesion architecture: *ground output in real substrate, not synthetic interpretation.*

#### 3.6.4 Concerns architected against

| Concern | Mitigation |
|---|---|
| **Image quality variance across substrate sources** | Tier-1 sources (museum APIs, Sketchfab attachment renders, modern military, Warhammer AoS minis) = fast-path. Tier-2 sources (Wikipedia thumbnails, painted illustrations, low-res photos) = gated by image-quality score. Tier-3 (game-wiki screenshots, paintings, line drawings) = case-by-case or fallback to synthetic-gen. **Image-quality scoring pre-pipeline is a load-bearing gate.** |
| **Angle / orientation suitability for Meshy** | Meshy 6 documentation indicates tolerance across angles; 3/4 view is optimal but profile + top-down are workable. **Validate empirically in architecture-validation spike per doc 38 § 4.3.** If angle-tolerance is narrower than documented, expand the quality-score to include orientation. |
| **License compliance for derivative works (3D model = derivative)** | Filter substrate to CC0 + CC-BY + permissive licenses before pipeline runs. ~36K rows qualify (CC0 ~24K + CC-BY/permissive ~12K per substrate license-tier breakdown). Editorial / fan-wiki / non-commercial substrate (~40K rows) is **excluded from the pass-through path** but remains indexable for content generation that doesn't produce 3D-asset derivatives. |
| **Image-fetch implementation** | Currently URL-only registration per ADR. Add fetch-and-cache workflow to asset-pipeline. Star-lord's seam (output/asset-pipeline integration). |
| **URL staleness / hotlink breakage** | Cache-on-first-fetch into asset-pipeline's persistent store. Cache scope = license-clean subset only. |
| **Coverage gap fallback** | ~7,648 weapons (~8.5%) lack registered images. Fallback to ChatGPT-gen path automatically when substrate image is missing or quality-score below threshold. **No "no-asset" failure mode** — every weapon has either substrate-image-pass-through or synthetic-gen path. |

#### 3.6.5 Implementation hooks

1. **Quality-score function** — pre-pipeline filter on substrate images. Inputs: image resolution, source-tier classification, license-tier classification, format suitability. Output: pass / fallback-to-synthetic. Owner: star-lord (asset-pipeline integration) + elrond (substrate license/source classification).
2. **Image-fetch + cache layer** — pulls registered URL, caches locally, hands to Meshy. Owner: star-lord.
3. **Fallback router** — when substrate image fails quality or is missing, route to ChatGPT-gen path. Owner: star-lord.
4. **Acceptance validation** — architecture-validation spike (doc 38 § 4.3) tests image-pass-through vs ChatGPT-gen on 3-5 weapons from the museum-tier subset of substrate. Pass criterion: direct-pass-through produces equal-or-better Meshy output (mesh quality, rigging quality, Unreal-import compatibility). Owner: matt + galadriel (visual evaluation) + drax/star-lord (technical integration).

#### 3.6.6 Strategic context — why this matters beyond the pipeline

This decision is the **asset-layer analog** of the methodological commitment to pattern recognition on substrate (per `canonical/story/legacy-categorical-cleanup-audit-2026-05-22.md` Pattern 4-5-6 retirements). Same design instinct, two layers:

- **Methodological layer** — emergent axes / clusters discovered from substrate, NOT pre-imposed taxonomies
- **Asset layer** — 3D models generated from substrate reference images, NOT synthetic concept art

Together these form a coherent architectural commitment: **the engine operates on real-world reference substrate rather than on synthetic generation.** This is competitive moat material — only possible because we built the substrate — and aligns with D7 (AI-tell line) at every layer where it operates.

For the commercial pitch (engine-as-product per Variant C): "Our engine doesn't just generate content — it operates on a vast real-world reference substrate, discovers latent content axes via statistical methodology, AND produces 3D assets grounded in authentic source imagery." Three-layer differentiator.

---

## 4. Irregular-monster pipeline [PENDING legolas Priority 2 findings]

**Skeleton structure (to be filled when legolas findings land):**

### 4.1 Irregular-monster categories (the gap Meshy doesn't cover)

| Category | ARPG-canon examples | Reincarnated relevance |
|---|---|---|
| Amorphous / blobs | D2 Blood Lords; PoE Stygian; Slime-class isekai protagonists | Trial-boss + spirit-form (slime form is canonical isekai beat) |
| Multi-segment serpents | PoE Bramble Hellion; D3 snake elites | Trial-boss-gallery variety |
| Multi-headed | Hydras (D2, PoE); three-headed boss patterns | Signature trial-room boss tier |
| Eyeball / mouth / no-body | D2 Eye-Beasts; PoE Beyond entities | Atmospheric monster gauntlet entries |
| Insectoid (>4 limbs) | D2 Burning Souls; PoE spider-types | Monster gauntlet diversity |
| Floating wraith | D2 wraiths; PoE Spectres; D3 grotesques | Atmospheric / shadow-element themed |
| Construct / mineral / plant | Treants; golems; PoE Bramble-class | Earth-element thematic depth |
| Swarms | PoE Spectres; swarming insects | Pack-tier monster encounters |

### 4.2 Asset-Store coverage findings

[Pending: which Asset Store packs cover each category; per-pack cost estimate; typical animation coverage; commercial-use licensing]

### 4.3 Shader-based approaches

[Pending: vertex-shader amorphous monsters; sprite-billboard wraiths; procedural mesh deformation for swarms; indie-ARPG community precedent]

### 4.4 Hand-rigging budget for signature bosses

[Pending: realistic per-monster authoring time / cost for signature trial-room bosses; pattern recommendation for which subset warrants hand-authoring vs. Asset Store]

### 4.5 Per-season monster-roster budget framing

[Pending: estimated time + dollar cost to populate one season's monster roster under this strategy]

---

## 5. Protocol v1.3 amendment — items to update post-finalization

When § 3 + § 4 are filled in by legolas findings, the following protocol amendments fire:

### 5.1 W1.9 Mixamo integration setup — rewrite

**Current (v1.3 § 6.2.2 W1.9):**

> Dispatch: confirm Mixamo TOS for commercial use; set up bone-remapping pipeline for ChatGPT→Meshy character imports; integrate Unity Animation Rigging package for VFX attachment to humanoid rig anchor points.

**Revised (v1.4):**

> Dispatch: confirm Meshy commercial TOS for production use; configure Meshy → Unity import pipeline (no Mixamo step); integrate Unity Animation Rigging package for VFX attachment anchor points; verify Meshy rigging produces Unity-Humanoid-compatible bone structure per `canonical/story/asset-pipeline-meshy-swap-2026-05-22.md` § 3.

### 5.2 W1.10 Pipeline test runs — pipeline string update

**Current (v1.3 § 6.2.2 W1.10):**

> Dispatch: end-to-end pipeline validation with 5-10 test characters spanning the 7-element substrate — ChatGPT → Meshy → Mixamo → VFX

**Revised (v1.4):**

> Dispatch: end-to-end pipeline validation with 5-10 test characters spanning the 7-element substrate — ChatGPT → Meshy (mesh + rig + animation) → Unity Animation Rigging → VFX

### 5.3 New workstream W1.9b — Irregular-monster asset strategy

To be added as a parallel workstream under P1:

> **W1.9b — Irregular-monster asset strategy** (drax + gandalf)
> Per `canonical/story/asset-pipeline-meshy-swap-2026-05-22.md` § 4: enumerate Asset Store packs covering slimes / multi-segments / hydras / wraiths / etc.; implement Meshy + Asset-Store hybrid pipeline; document per-category production path; estimate per-season monster-roster budget. Effort: ~1 week scoping; integration is per-season operational expense.

### 5.4 P1-P7 walkthrough ratification matrix — gate update

Drop "Mixamo TOS interpretation" row from the P1 ratification matrix. Replace with "Meshy commercial TOS confirmation" (one-shot; lands when W1.9 begins).

---

## 6. Cross-references

- `agentic_orchestration/dispatches/2026-05-22-legolas-meshy-pipeline-research.md` — research commission filling § 3 + § 4
- `canonical/story/hive-mind-protocol-qd-engine-rebuild-2026-05-21.md` v1.3 § 6.2.2 W1.9 + W1.10 — target of post-research amendment
- `canonical/story/gear-archetype-rule-table-v1-2026-05-22.md` — 15-archetype catalogue (§ 3.3 consumes this)
- `canonical/story/gear-as-substrate-2026-05-21.md` § 0.5.6 — LITE path; G2-LITE/G5-LITE Unity integration cross-reference
- `canonical/story/style-register.md` — locked visual style (consumes pipeline output)
- `canonical/story/tier-4-architecture-defaults-2026-05-22.md` § 5 — gear-anchored signature capstones (consumes asset pipeline output for player surfaces)
- `agentic_orchestration/legolas/research/substrate-sufficiency-audit-2026-05-20/` — Phase 1 Asset Store landscape (Priority 2 starting point)
- `~/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md` § 19 — RATIFIED 2026-05-22 (no babysit on the research)

---

**Signed:** gandalf (story-and-design steward; canonical doc author)
**For:** clean Mixamo → Meshy swap with weapon/gear + irregular-monster scoping informed by legolas Mode A research; protocol v1.4 amendment-ready when research lands.
