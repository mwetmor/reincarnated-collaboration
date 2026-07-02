# Asset Pipeline — Meshy Replaces Mixamo; Irregular-Monster Strategy

> **STATUS:** CURRENT (load-bearing as of 2026-05-23) — see `canonical/00-ground-state.md`
>
> **2026-05-23 amendment:** doc originally authored 2026-05-22 with Unity as target engine. Doc 38 (`canonical/38-downstream-delivery-strategy-2026-05-23.md`) D1 locked **Unreal Engine** on 2026-05-23. **Unity references in this doc should be read as Unreal going forward.** Conceptual mappings: Unity Animation Rigging package → Unreal Control Rig; Unity Humanoid Avatar → Unreal Skeletal Mesh + IK Retargeting; Unity VFX Graph → Unreal Niagara. Underlying pipeline shape is unchanged; engine target is updated.
>
> **2026-05-23 amendment:** § 3.6 added — **image-pass-through-to-Meshy** named as default pipeline path for substrate-resident weapons (~91.5% coverage on 89K substrate). Reduces ChatGPT image-gen step; aligns with D7 AI-tell line; grounded in real reference data.
>
> **2026-05-23 amendment (Sidecar A close-out):** § 3.6.2 refined to **Path-1 / Path-2 routing terminology** disambiguated from existing § 3.6.4 **Tier-1 / Tier-2 / Tier-3 source-classification** vocabulary. § 3.6.4 compound-object closure narrowed to N=1 validated subcase. § 3.6.3 economic-win table updated to tier-conditional. § 3.6.1 91.5% framing clarified by tier sub-breakdown. Polearm aspect-ratio threshold methodology deferred to legolas Mode A consult — long-shaft weapons in portrait format route to **Path-2 unconditionally** until threshold methodology lands. **Two new recognitions filed** at `canonical/story/v1-1-plus-design-discipline-recognitions-2026-05-23.md` Recognitions 5 (polearm aspect-ratio gate) + 6 (Meshy polygon-count delta as diagnostic). Empirical basis: `agentic_orchestration/star-lord/research/image-pass-through-vs-llm-gen-meshy-comparison-2026-05-23/comparison.md` (Sidecar A MIXED verdict, 5 weapons × 2 paths = 10 Meshy submissions).

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

Of the 91.5% image-coverage substrate, approximately **50% qualifies for Tier-1 direct-pass-through** (museum-studio high-resolution photographic, neutral background, favorable weapon-pixel-density); **~30% Tier-2 conditional** (operational/manufacturer regime ~600-1000px, gated by quality-score function pending Sidecar A.2 score-stability verification); **~20% Tier-3 Path-2 mandatory** (game-render/wiki sources <600px, editorial_only licenses, or stylized non-photographic). Tier proportions are empirical estimates per Sidecar A 2026-05-23 (`agentic_orchestration/star-lord/research/image-pass-through-vs-llm-gen-meshy-comparison-2026-05-23/comparison.md` § 7); refined sample-size validation deferred to Sidecar A.2. Per § 3.6.2 path-routing protocol.

Without the substrate, the ChatGPT-gen path was the only option. With the substrate, the substrate IS the reference library — and Meshy 6 can ingest reference imagery directly.

#### 3.6.2 Pipeline routing — Path-1 vs Path-2 (post-Sidecar A refinement)

**Vocabulary discipline (Sidecar A close-out):** this doc distinguishes **two orthogonal axes**:
- **Tier-1 / Tier-2 / Tier-3 = source classification** (see § 3.6.4 image-quality table): museum-studio high-res / operational manufacturer / game-render-wiki-stylized. Per-row property of substrate.
- **Path-1 / Path-2 = routing decision** (this section): image-pass-through to Meshy / ChatGPT-synthetic-gen then Meshy. Per-asset pipeline choice.

The tier-to-path mapping is **no longer 1:1** post-Sidecar A. The MIXED verdict shows Tier-2 can route to Path-1 at parity with Path-2 (cost-savings, no quality penalty); Tier-1 has a polearm subcase that routes to Path-2; Tier-3 mandates Path-2. The two vocabularies must not be conflated.

```
WEAPONS + GEAR — Path-1 image-pass-through (DEFAULT for Tier-1 standard + Tier-2 viable):
  Substrate image URL → fetch + cache → quality-score gate → routing-decision:
    - Tier-1 source, NOT long-shaft-portrait: Path-1 PASS (museum-studio fast path)
    - Tier-1 source, long-shaft polearm in portrait: ROUTE TO PATH-2 (see § 3.6.5 polearm exception)
    - Tier-2 source, resolution ≥ 600px, weapon-pixel-density passes gate: Path-1 conditional
    - Tier-2 source, fails any gate: ROUTE TO PATH-2
    - Tier-3 source: ROUTE TO PATH-2 (mandatory)
    → Meshy 6 → Control Rig → Unreal

WEAPONS + GEAR — Path-2 synthetic-gen (fallback + Tier-3 mandatory + Tier-1 polearm exception):
  ChatGPT (gpt-image-1) → GPT-4o coherence-gate → Meshy 6 → Control Rig → Unreal
```

**Polearm aspect-ratio exception (interim policy pending legolas Mode A consult):** long-shaft weapons in portrait-format museum photographs route to **Path-2 unconditionally** regardless of source-tier resolution. Empirical basis: Halberd of Archduke Ferdinand II (entry_id 167849) at 2250×4000 px museum-quality input produced Path-1 over-triangulated 295K-tri mesh vs Path-2's clean 48K-tri output. Threshold methodology (30% bbox-occupancy? 20%? other%?) is a Discipline #18 methodology hotspot — execution cannot self-validate threshold choice. Pending legolas Mode A: long-shaft weapon classes (polearm, staff, lance, spear; weapon_form tags) **route to Path-2** by default. Tier-1 PASS criteria for Path-1 require source NOT match the polearm-portrait subcase. Recognition 5 filed at `canonical/story/v1-1-plus-design-discipline-recognitions-2026-05-23.md` § 5 — threshold methodology refinement deferred to Sidecar A.2 + legolas Mode A consult.

#### 3.6.3 Why this is right (four reasons)

| Win | Why it matters |
|---|---|
| **Authenticity uplift** | Real museum/wiki/community photographs > synthetic concept art. Royal Armouries' Edo katana photograph carries 400 years of provenance; DALL-E produces average-of-internet katana. **Direct alignment with D7 (AI-tell line) per doc 38.** |
| **Variance uplift** | 89K real weapons span 400+ years of metallurgy + regional craft + design lineages. DALL-E on same prompt produces variations of same idea. The substrate gives actual diversity, not synthetic diversity. |
| **Quality uplift** | Museum-API images are studio-lit professional photography (~1024×1024 or higher); typically higher source-quality than DALL-E HD output. Meshy 6 performs better on cleaner references. |
| **Provenance / legal clarity** | ~24K CC0 + ~12K CC-BY/permissive substrate has known-clean license. DALL-E output IP status remains contested. Direct-pass-through gives clearer legal grounding for commercial use. |

**Economic win (Sidecar A close-out — now tier-conditional):**

| Source tier | Substrate fraction | Approx weapon count | ChatGPT-gen savings/year | Status |
|---|---|---|---|---|
| Tier-1 (museum-studio high-res, favorable aspect, Path-1 default) | ~50% of license-clean substrate | ~18K weapons | **$720-1800/year eliminated** | CONFIRMED Sidecar A (1 weapon Claymore + 1 weapon Crossbow + 1 weapon Halberd-as-Path-2-exception) |
| Tier-2 (operational/manufacturer, Path-1 conditional) | ~30% | ~11K weapons | Conditional savings; equal to Path-2 at parity | PENDING Sidecar A.2 (1 weapon Barrett, EQUAL verdict — single data point not yet stable) |
| Tier-3 (game-render/wiki/editorial-only, Path-2 mandatory) | ~20% | ~7K weapons | $0 savings; Path-2 required | CONFIRMED Sidecar A (Yellow Quartz Longsword 99×134px → Path-1 fails decisively) |
| Tier-1 polearm-portrait exception | subset of Tier-1 | TBD | $0 (Path-2 unconditional pending § 3.6.5 threshold methodology) | INTERIM POLICY pending legolas Mode A |

The § 3.6.3 prior "$120-300/year" estimate was too conservative. At full Tier-1 confirmation, savings on ChatGPT-gen costs are **~$720-1800/year** on the Tier-1 segment alone (per Sidecar A § 8 cost model). The **architectural-coherence wins are major** — same design instinct as pattern-recognition methodology (P2/P3) and substrate-as-cohesion architecture: *ground output in real substrate, not synthetic interpretation.*

#### 3.6.4 Concerns architected against

| Concern | Mitigation |
|---|---|
| **Image quality variance across substrate sources** | Tier-1 sources (museum APIs ≥1000px, Sketchfab attachment renders, modern military operational at high-res, Warhammer AoS minis) = Path-1 default. Tier-2 sources (operational/manufacturer 600-999px, Wikipedia thumbnails) = gated by image-quality score (resolution + weapon-pixel-density + background-type). Tier-3 (game-wiki screenshots <600px, paintings, line drawings, editorial-only licenses) = Path-2 mandatory. **Image-quality scoring pre-pipeline is a load-bearing gate.** Sidecar A empirical resolution-floor confirmed: ~700px lower bound for Path-1 parity (Barrett M82 EQUAL verdict at 700px); 1000px+ recommended for Path-1 superiority. |
| **Angle / orientation suitability for Meshy** | Meshy 6 documentation indicates tolerance across angles; 3/4 view is optimal but profile + top-down are workable. **Sidecar A 2026-05-23 empirical:** landscape-format museum photos (Crossbow at 1957×1487) and high-res neutral-background standard-form museum photos (Claymore at 1636×3264) produce Path-1 superiority. **Long-shaft weapons in portrait-format museum photos fail Path-1** (Halberd at 2250×4000 → Path-1 295K-tri over-triangulation vs Path-2 48K-tri clean). See polearm-aspect row below. |
| **Weapon-pixel-density for long-shaft weapons (NEW — Sidecar A finding)** | Polearms, staffs, lances, spears in portrait-format images have low weapon-bbox-occupancy even at very high total resolution. Empirical: Halberd at 2250×4000 occupied a narrow vertical stripe → Meshy over-triangulated to fill uncertainty. **Interim policy:** weapon_form ∈ {polearm, staff, lance, spear} **routes to Path-2 unconditionally** regardless of source-tier. Threshold methodology (bbox-occupancy percentage gate; 30%? 20%?) deferred to legolas Mode A consult per Discipline #18 methodology-hotspot routing. Recognition 5 in `canonical/story/v1-1-plus-design-discipline-recognitions-2026-05-23.md` § 5. |
| **License compliance for derivative works (3D model = derivative)** | Filter substrate to CC0 + CC-BY + permissive licenses before pipeline runs. ~36K rows qualify (CC0 ~24K + CC-BY/permissive ~12K per substrate license-tier breakdown). Editorial / fan-wiki / non-commercial substrate (~40K rows) is **excluded from the pass-through path** but remains indexable for content generation that doesn't produce 3D-asset derivatives. |
| **Image-fetch implementation** | Currently URL-only registration per ADR. Add fetch-and-cache workflow to asset-pipeline. Star-lord's seam (output/asset-pipeline integration). |
| **URL staleness / hotlink breakage** | Cache-on-first-fetch into asset-pipeline's persistent store. Cache scope = license-clean subset only. |
| **Coverage gap fallback** | ~7,648 weapons (~8.5%) lack registered images. Fallback to ChatGPT-gen path automatically when substrate image is missing or quality-score below threshold. **No "no-asset" failure mode** — every weapon has either substrate-image-pass-through or synthetic-gen path. |
| **Compound-object handling (closure narrowed to N=1)** | **Validated for N=1 only (Sidecar A 2026-05-23):** Crossbow with Cranequin Winder (entry_id 193565, Met Museum, full-assembly photograph at 1957×1487). Both paths produced unified single-mesh output (1 object, 1 material) — no fragmentation. Generalization to other compound-object morphologies (chained weapons, sectioned polearms, weapon-plus-sheath assemblies, modular firearms) **remains untested**. Permitted for compound objects from high-resolution museum photographs that show full assembly; per-subcase Sidecar A.2-style validation when other compound subcases first encountered. The architecture-validation spike concern is **conditionally closed** for the validated subcase only. |
| **Meshy over-triangulation as Path-1-quality diagnostic (NEW — Sidecar A finding)** | When Path-1 produces significantly higher triangle counts than expected (3x+ target_polycount), this is a leading indicator of input-quality problems (low weapon-pixel-density, low resolution, stylized non-photographic input). Halberd Path-1 at 295K tris vs Path-2 at 48K tris is the empirical case. Potential use: post-submission polygon-count delta as Path-1-quality diagnostic enabling reroute-to-Path-2 retry. Cost-trade-off complexity (second Meshy credit cost vs reroute decision quality) is unresolved. Recognition 6 in `canonical/story/v1-1-plus-design-discipline-recognitions-2026-05-23.md` § 6. Sidecar A.2 evaluates whether the signal correlates reliably across more cases. |

#### 3.6.5 Implementation hooks

1. **Quality-score function** — pre-pipeline filter on substrate images. Inputs: image resolution, source-tier classification (Tier-1/2/3 per § 3.6.4), license-tier classification, weapon-form check (long-shaft polearm exception), format suitability. Output: Path-1-pass / Path-2-fallback (per § 3.6.2 routing). Owner: star-lord (asset-pipeline integration) + elrond (substrate license/source classification). **Polearm aspect-ratio threshold methodology pending legolas Mode A consult** (Discipline #18 hotspot — Recognition 5).
2. **Image-fetch + cache layer** — pulls registered URL, caches locally, hands to Meshy. Owner: star-lord.
3. **Fallback router** — when substrate image fails quality, is missing, or matches polearm-portrait exception, route to ChatGPT-gen Path-2. Owner: star-lord.
4. **Acceptance validation — Sidecar A LANDED 2026-05-23** — architecture-validation spike per doc 38 § 4.3 executed by star-lord. 5 weapons × 2 paths = 10 Meshy submissions. Verdict: **MIXED — per-regime conditional routing required.** Tier-1 museum-studio Path-1 CONFIRMED for standard-form weapons; long-shaft polearm-portrait exception identified (Path-2 unconditional pending threshold); Tier-2 operational ~700px Path-1 PARITY (single data point, N=1 score-stability gap); Tier-3 game-render/wiki Path-2 mandatory. Empirical artifact: `agentic_orchestration/star-lord/research/image-pass-through-vs-llm-gen-meshy-comparison-2026-05-23/comparison.md`. **Sidecar A.2 recommended:** (a) 3-5 long-shaft weapons at varied resolutions for polearm-threshold characterization; (b) additional Tier-2 weapons for score-stability; (c) other compound-object morphologies for generalization beyond N=1.

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
- `canonical/story/historical/gear-as-substrate-2026-05-21.md` § 0.5.6 — LITE path; G2-LITE/G5-LITE Unity integration cross-reference
- `canonical/story/style-register.md` — locked visual style (consumes pipeline output)
- `canonical/story/tier-4-architecture-defaults-2026-05-22.md` § 5 — gear-anchored signature capstones (consumes asset pipeline output for player surfaces)
- `agentic_orchestration/legolas/research/substrate-sufficiency-audit-2026-05-20/` — Phase 1 Asset Store landscape (Priority 2 starting point)
- `~/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md` § 19 — RATIFIED 2026-05-22 (no babysit on the research)
- **`agentic_orchestration/star-lord/research/image-pass-through-vs-llm-gen-meshy-comparison-2026-05-23/comparison.md`** — Sidecar A empirical artifact (MIXED verdict, 5 weapons × 2 paths, basis for § 3.6.2-§ 3.6.5 refinements)
- **`canonical/story/v1-1-plus-design-discipline-recognitions-2026-05-23.md` § 5 + § 6** — Recognition 5 (polearm aspect-ratio gate / weapon-pixel-density threshold methodology) + Recognition 6 (Meshy polygon-count delta as Path-1-quality diagnostic). Empirical basis: same Halberd N=1 case
- **`agentic_orchestration/gandalf/notes/2026-05-23-sidecar-A-weapon-nomination-verdict.md`** — gandalf weapon-nomination verdict that scoped Sidecar A inputs

---

**Signed:** gandalf (story-and-design steward; canonical doc author)
**For:** clean Mixamo → Meshy swap with weapon/gear + irregular-monster scoping informed by legolas Mode A research; protocol v1.4 amendment-ready when research lands. **2026-05-23 Sidecar A close-out:** § 3.6 image-pass-through path empirically validated as MIXED-verdict tier-conditional routing; Path-1 / Path-2 routing vocabulary disambiguated from Tier-1/2/3 source classification per jack-ryan Gate-2 WARN; polearm aspect-ratio + over-triangulation findings filed as Recognitions 5 + 6 in v1.1+ recognitions doc.
