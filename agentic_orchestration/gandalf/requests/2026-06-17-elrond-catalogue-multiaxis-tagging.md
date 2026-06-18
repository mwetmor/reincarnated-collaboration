# elrond commission — Synty catalogue multi-axis tagging (manifest substrate-half + density map)

**STATUS:** REQUEST (gandalf → elrond, routed via KR)
**Date:** 2026-06-17
**Author:** gandalf (story-and-design steward)
**Authority:** Matt 2026-06-17 — author the elrond brief for the consumption-time partition; gear-spec asset architecture (asset-class→geometry-source) verified against the locked docs same session.
**Seam:** elrond (catalogue/data steward). Additive to the existing Synty catalogue; no destructive change.
**Companions:**
- `agentic_orchestration/gandalf/notes/2026-06-17-synty-acquisition-run-ruling.md` § 4 — the consumption-time partition this materializes (corrected per Matt Q3: register filter survives; genre-discard RETRACTED → temporal×cultural tag).
- `canonical/story/styleprofile-output-shape-ruling-2026-06-17.md` — the §7.6 ruling whose consumers select against this manifest.
- `canonical/story/engine-as-general-serial-content-product-2026-05-22.md` — the density-routed asset pipeline (Synty-dense → Synty base mesh; sparse → image-to-3D / Sidekick gap-fill) this density-map feeds. (Note: the 2026-05-22 doc predates the 2026-06-16 gear-spec record; where it says "Meshy lane," read it through the corrected architecture — image-to-3D is legendary-tier, gap-fill is Sidekick/image-to-3D.)
- `canonical/48-cycle-14-class-roster-2026-05-27.md` — proof the engine ALREADY ships non-fantasy registers (Siege-Master early-modern/industrial; firearm class modern/magitech). The tag must serve all eras.
- `canonical/story/marginal-lineage-tagging-pattern-2026-05-23.md` — the Mode A/B/C/D tagging-collapse the cultural-identity axis must avoid.

---

## 0. Framing — the gear-spec asset architecture (per the LOCKED docs)

> **Provenance note (trust-but-verify):** an earlier draft of this brief carried a "Synty/Meshy/Godot three-lane" framing from Matt's memory. Matt flagged the memory as suspect and directed verification against the docs (2026-06-17). The docs (`gear-spec-generation-deferred-architecture-2026-06-16.md` CURRENT + the pipeline recommendation it wraps) tell a different story; this framing is corrected to the docs. The divergence: weapons route through the **100k corpus** (not Meshy); image-to-3D (Meshy/Rodin/Tripo) is **legendary/hero tier only**; Godot is a **render target** (one of two, with UE), not an augmentation lane.

The organizing axes are **asset-class → geometry source** and **tier → authorship mechanism** — NOT a tool-split.

**Geometry source by asset class:**
- **Armor (chest/legs/boots/helmet — SKINNED to the rig):** Synty fixed meshes — the armor catalogue to select-and-adapt from (gear-spec record § 3.6, "Synty IS the armor reference catalogue; dissolves the weapon/armor asymmetry"). Differentiation = restyle, NOT new geometry.
- **Weapons (STATIC, socket-attached):** the **100k-weapon corpus** (select+adapt). Common = base mesh + restyle; legendary = image-to-3D from the reference picture. Not Synty-primary, not Meshy-primary.
- **Accents (STATIC, socket-attached — belts/shoulders/capes):** Synty **accent meshes** via `BoneAttachment3D` — the silhouette-breaker on shared torso/legs.

**Authorship mechanism by tier (L2 drive-router, § 3.2):**
- Common/Magical → base mesh + **parametric restyle** (StyleProfile shader: palette-remap / finish / emission / overlay / wear).
- Rare/Set → constrained API/agent StyleProfile fill (manifest menu; D7 constrained-blank).
- Legendary/Hero → **image-to-3D** (Meshy / Rodin / Tripo, corpus-reference-seeded) — bounded; the ONLY mesh-generation tier.

**Render target (L4 adapter, § 3.4):** StyleProfile = engine-neutral render-intent → Godot `.tres` OR UE material (BOTH). Master shader + `BoneAttachment3D` execute restyle + accents at render time.

**Consequence for tagging:** each Synty pack is tagged by what it **contributes** to this architecture (armor base-mesh / weapon base-mesh / accent source / environment / anim / ui) — see axis 2. (The legendary image-to-3D tier is corpus-reference-seeded, not Synty-pack-keyed, so it is not a Synty-pack tag value.)

## 1. The job

Tag all **157 packs** on the five axes below. Output = (a) the **manifest substrate-half** the §7.6 StyleProfile ruling's consumers (rocket §7.2, star-lord §7.3, drax §7.5) select against; (b) the **density map** across temporal-cultural space that feeds the **base-mesh-gap routing** (temporal-cultural regions where Synty skinned-character coverage is sparse route to image-to-3D / Sidekick — NOT to a Synty base mesh). Additive to the existing catalogue schema.

## 2. The five axes (with the discipline each obeys)

| # | Axis | Values | Discipline |
|---|---|---|---|
| 1 | `register` | `POLYGON` \| `POLYGON_MINI` \| `SIMPLE` | **substrate-GIVEN** (Synty's own pack naming). Locked-register filter: POLYGON = consumption line; MINI + SIMPLE = corpus-retained, set-aside. |
| 2 | `contribution_role` | `armor-base-skinned` (skinned armor/character meshes — the restyle base) \| `weapon-base-static` (Synty weapon meshes — common-weapon base; the 100k corpus is primary) \| `accent-attach-static` (belts/shoulders/capes/props — `BoneAttachment3D`) \| `environment` (set-dressing) \| `anim` \| `ui` | **doc-DERIVED** (gear-spec record asset-class × skinned/static split). |
| 3 | `time_period` | **substrate-VOTED** — propose strata bottom-up | hypotheses ONLY (antiquity / medieval-fantasy / renaissance-early-modern / industrial-steampunk / modern / sci-fi-future); let the catalogue vote, **gandalf curates labels**. |
| 4 | `cultural_identity` | **substrate-VOTED** — propose strata bottom-up | hypotheses ONLY (w-euro-medieval / norse / east-asian / egyptian / mesoamerican / indo-asian / …); substrate votes, **gandalf curates**. Guard the Mode A/B/C/D collapse (geographic-origin vs cultural-tradition vs naming-allusion vs metadata-error). |
| 5 | `seam` | `descent` \| `overworld` \| `nature` \| `char-skeletal` \| `char-named-silhouette` \| `weapon-prop` \| `bestiary` \| `anim` \| `ui` | **substrate-GIVEN** (Synty pack category) + light curation. |

**The substrate-led split is deliberate:** axes 1+5 are factual (Synty naming); axis 2 is doc-derived design taxonomy (gear-spec record asset-class × skinned/static split); axes 3+4 are where the substrate must vote and I curate the labels at a rep-audit. Do NOT hand-impose a rigid time-period/culture enum — propose strata WITH rep examples per stratum and I curate (geometry/grouping is substrate-binding; the *labels* are curation — the semantic-layer rep-audit discipline).

## 3. Density-map findings to surface explicitly (design-valuable — own findings section)

- **The sci-fi POLYGON skinned-character question.** Apparent gap: the POLYGON sci-fi packs are *environments* (Sci-Fi City / Cyber City / Space / Worlds / Outpost); the only sci-fi *characters* seen are `SIMPLE - Space Characters` (set-aside register). Confirm whether POLYGON sci-fi skinned-character coverage exists or whether sci-fi-body routes to Sidekick/Meshy. (galadriel's parallel spike answers the mask-mechanism half; you confirm the existence/coverage half.)
- **Steampunk/industrial thinness** (Western covers frontier; Victorian-steampunk proper likely thin).
- **Aztec/Mesoamerican + Indo-Asian cultural thinness** (Egypt/Samurai/Vikings covered; the rotation's later cultural registers may be gaps).
- These gaps = **where base-mesh gap-fill is forced** (image-to-3D / Sidekick — Synty supplies no skinned-character base there). This UPDATES the previously-canon "sci-fi = zero coverage, full image-to-3D, deferred v1.1+" density entry: Synty's sci-fi *environment* packs partially close it; sci-fi *character* base may remain image-to-3D / Sidekick.

## 4. Acceptance

- All 157 packs tagged on all 5 axes.
- Axes 3+4 strata **PROPOSED with rep examples** for gandalf curation — NOT unilaterally labeled.
- contribution_role + gap-fill routing complete (every pack routes).
- Density gaps surfaced as an explicit findings section (§ 3 questions answered).
- Additive to the existing catalogue (no destructive schema change).

**Deliverable path:** elrond's call (catalogue seam); recommend `agentic_orchestration/research/catalogue/synty-recon-2026-06-16/multiaxis-tags-2026-06-17.{jsonl,md}` and/or the catalogue DB.

**gandalf reviews on return:** I curate the axis-3/4 semantic labels at a rep-audit and sign off the partition. This is the manifest substrate-half that resolves Q2 gate 1 (the in-flight gear-spec upstream-wiring decision).

**Signed:** gandalf, 2026-06-17.
