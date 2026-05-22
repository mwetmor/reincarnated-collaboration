# Dispatch — legolas: Unity Asset Catalogue (Weapons + Armor) + Meshy Armor Capability

**Date:** 2026-05-22
**Author:** gandalf (commissioning research; design-side)
**Recipient:** legolas (Mode A + Mode B mixed; analytical for Meshy capability, catalogue crawl for Asset Store)
**Authority:** Matt 2026-05-22 (this session) — explicit research commission following the Meshy pipeline research return
**Priority:** HIGH — load-bearing for Reincarnated Profile A asset procurement + general engine multi-aesthetic substrate planning
**Estimated effort:** 2-3 days (mixed-mode; catalogue crawl is the larger piece)
**Fire condition:** none; pre-authorized by Matt

---

## 0. TL;DR

Two priorities, both consequences of your prior Meshy pipeline research (`agentic_orchestration/legolas/research/meshy-pipeline-2026-05-22/findings.md`):

| Priority | Scope | Mode |
|---|---|---|
| **1 — Meshy armor capability** | Confirm whether Meshy produces armor meshes; if yes, whether output is skinnable to a humanoid skeleton (Pattern C — Skinned Mesh Renderer per your prior findings); coverage across armor categories (chest / shoulder / helmet / glove / boot / cloak) | Mode A analytical (vendor docs + capability verification) |
| **2 — Unity Asset Store catalogue crawl: weapons + armor** | Systematic enumeration of available weapon and armor packs across the Unity Asset Store with prices; categorize by aesthetic register (medieval-European / industrial-grim / ancient-Asian / sci-fi / etc.) and by mechanical archetype; match against project needs | Mode B catalogue crawl |

Single deliverable directory: `agentic_orchestration/legolas/research/unity-catalogue-armor-meshy-2026-05-22/` with structured findings (paths in § 4).

---

## 1. Priority 1 — Meshy armor capability

### 1.1 Why this is unfinished

Your 2026-05-22 Meshy pipeline findings covered Pattern C (Skinned Mesh Renderer for body-worn armor) briefly but flagged it as "secondary concern" because the 15-archetype catalogue is weapon/held-prop focused. Matt has now surfaced an explicit question: **does the project intend armor as a substrate dimension, and can Meshy produce it?**

The general-engine reframe Matt landed today (engine produces coherent serial content; Reincarnated is one profile) makes this more important. Multiple profiles may want armor as a visual surface; the Reincarnated profile specifically may want armor distinct from gear (per `memory/project_gear_and_spirit_guide.md`).

### 1.2 Research questions

**1.2.1 Can Meshy generate armor meshes?**

- Vendor docs: does Meshy's text-to-3D produce armor when prompted? (chest plate, full plate harness, leather cuirass, scale mail, robe, cloak, helmet, gauntlets, greaves, sabatons, pauldrons)
- Library coverage: does Meshy's pre-made 58K+ model library include armor as a tag/category?
- Marketing copy + tag pages: confirm via meshy.ai/tags/armor or equivalent (compare to your /tags/weapon finding)

**1.2.2 If yes, is the output skinnable to a humanoid skeleton?**

- **The critical question.** Armor must deform with the character. That requires either:
  - (a) Armor mesh with bone weights skinned to the same Humanoid Avatar skeleton as the character body (drop-in Skinned Mesh Renderer); OR
  - (b) Static armor mesh attached as rigid pieces to bone anchor points (shoulder pauldron parented to shoulder bone, helmet parented to head bone — viable for some armor types, not others)
- Does Meshy output armor with bone weights, or only as static meshes?
- If static-only: which armor categories work as rigid attachments (helmets, pauldrons, gauntlets, boots) vs. require skinning (chest pieces, cloaks, full robes)?
- Does Meshy's rigging API accept armor as input (the API doc said "humanoid bipedal assets" — does that mean "characters wearing armor" or specifically "naked humanoid character meshes")?

**1.2.3 If Meshy can't fully cover armor, what's the alternate path?**

- Asset Store armor packs with already-skinned meshes that fit Unity Humanoid Avatar skeleton?
- Per-character armor as part of the character mesh (armor baked into the body model at Meshy generation time, rather than as a separate piece)?
- Hand-skin in Blender (one-time per armor archetype family)?

### 1.3 Priority 1 deliverable shape

Structured table at `agentic_orchestration/legolas/research/unity-catalogue-armor-meshy-2026-05-22/meshy-armor-capability.md`:

```
Armor category   | Meshy can mesh? | Output skinnable?  | Alt path if needed
chest plate      | TBD             | TBD                | TBD
helmet           | TBD             | TBD (rigid OK)     | —
gauntlets        | TBD             | TBD (rigid OK)     | —
cloak / cape     | TBD             | TBD (cloth sim?)   | TBD
full robe        | TBD             | TBD                | TBD
pauldrons        | TBD             | TBD (rigid OK)     | —
greaves / boots  | TBD             | TBD                | TBD
```

Plus a confidence read: does Meshy + Unity cover the dominant armor case cleanly, or does armor require a substantively different pipeline than weapons?

---

## 2. Priority 2 — Unity Asset Store catalogue crawl: weapons + armor

### 2.1 Why this is needed now

Matt's strategic reframe today (engine-as-general-serial-content-product; Reincarnated as Profile A) makes asset procurement a profile-level concern. For Profile A specifically, the procurement decision is "Meshy + Asset Store hybrid"; the catalogue needs to be sized realistically against project needs and budget.

Your prior substrate-sufficiency-audit Phase 1 (`agentic_orchestration/legolas/research/substrate-sufficiency-audit-2026-05-20/phase-1-reconnaissance/`) touched the Unity Asset Store landscape but did not produce a comprehensive weapons/armor catalogue with pricing. This dispatch fills that gap.

### 2.2 Research questions

**2.2.1 Catalogue enumeration**

- List the major weapon-pack publishers on the Asset Store (PROTOFACTOR, Synty POLYGON, INFINITY PBR, Magic Pig Games, Hovl Studio, Quirky Series, Adventure Assets, etc.)
- Per-publisher: weapon packs with title, price, model count, aesthetic register, animation inclusion (if any), Unity version compatibility, render pipeline support (Built-in / URP / HDRP)
- Same enumeration for armor packs
- Don't enumerate every single pack — focus on the publishers and packs that meaningfully cover the substrate space

**2.2.2 Aesthetic register coverage**

Categorize each pack by aesthetic register, using the multi-genre vocabulary from today's theory-craft:
- `tech_level`: primitive / medieval / industrial / advanced / post-singularity
- `tone`: heroic / grim / mystical / absurd
- `cultural_lineage`: European / East-Asian / South-Asian / Mesoamerican / African / fictional-hybrid

Identify regions of the substrate space that are dense in Asset Store coverage (likely: medieval-heroic-European, advanced-fictional-hybrid sci-fi) and regions that are sparse (likely: ancient-mystical-South-Asian, industrial-grim-African).

**2.2.3 Match against project needs**

The Reincarnated Profile A needs to be matched against:

- **15-archetype gear catalogue** (`canonical/story/gear-archetype-rule-table-v1-2026-05-22.md` § 2): greatsword, twin-daggers, battle-spear, mace/warhammer, longbow, crossbow, blunderbuss, throwing-knives, wand, orb, caster-staff, tome, censer, holy-symbol, war-horn
- **7-element substrate** (`canonical/story/multi-dim-convergence-algorithm-2026-05-21.md`): fire, water, earth, wind, lightning, holy, shadow — each may want themed weapon variants
- **Reincarnated locked style register** (`canonical/story/style-register.md`): HD-2D Octopath-coded painterly + cel-shaded fantasy
- **Multi-genre architecture surfacing today** (gandalf theory-craft 2026-05-22): medieval-European / sci-fi / grimdark / ancient-Asian as candidate aesthetic registers; identify which Asset Store packs serve which

Output: per-archetype × per-aesthetic-register matrix showing best-available Asset Store coverage with price.

**2.2.4 Density-routing readiness**

Per my theory-craft yesterday + the density-routing approach from the other-Claude dialogue Matt summarized: identify regions where Asset Store coverage is **insufficient** to cover the 15-archetype catalogue × aesthetic registers, and flag those as Meshy-generation candidates. Total estimated procurement budget for Profile A:

- Tier 1: minimum viable catalogue (cover the dominant aesthetic register only — medieval-European-heroic) — estimated $ ?
- Tier 2: multi-aesthetic catalogue (cover 2-3 registers) — estimated $ ?
- Tier 3: comprehensive catalogue (cover 4+ registers with depth) — estimated $ ?

### 2.3 Priority 2 deliverable shape

Three files at `agentic_orchestration/legolas/research/unity-catalogue-armor-meshy-2026-05-22/`:

- `weapons-catalogue.md` — publisher-organized weapons enumeration with prices + aesthetic-register tags + match-to-15-archetype-coverage
- `armor-catalogue.md` — same structure for armor; armor categories may diverge from weapon categories
- `procurement-recommendation.md` — Tier 1 / Tier 2 / Tier 3 budget framing; per-tier Asset Store shortlist; Meshy-generation gap-fill recommendations; URP compatibility flags per pack; specific pre-procurement verification items (e.g., "verify Protofactor HFCFP Vol 1 URP support before $349.99 commit")

Plus a top-level `findings-summary.md` with the headline conclusions.

---

## 3. Out of scope

- **Procurement decisions.** Findings inform Matt's calls; do NOT pre-empt them
- **Per-pack URP compatibility for every pack** — flag the top 10-15 highest-value packs for URP verification; don't try to verify all packs
- **VFX packs** — your Phase 1 audit covered the VFX procurement landscape; this dispatch is weapons + armor specifically; do not re-enumerate VFX
- **Mixamo or Adobe-side assets** — Matt confirmed Mixamo swap to Meshy; Mixamo coverage is no longer of interest
- **Animation packs** — Meshy's 500+ animation library + Unity Animation Rigging cover the animation question per your prior findings; do not re-research
- **Engine-side implementation** — implementation is rocket/drax/star-lord territory; this dispatch is asset-strategy scoping only

---

## 4. Deliverable summary

Single directory: `agentic_orchestration/legolas/research/unity-catalogue-armor-meshy-2026-05-22/`

| File | Content |
|---|---|
| `meshy-armor-capability.md` | Priority 1 findings; Meshy armor capability + skinning analysis |
| `weapons-catalogue.md` | Priority 2 weapons enumeration with prices + aesthetic tags + archetype-coverage matrix |
| `armor-catalogue.md` | Priority 2 armor enumeration with prices + aesthetic tags + body-part-coverage matrix |
| `procurement-recommendation.md` | Tier 1/2/3 budget framing + Asset Store shortlist + Meshy-gap-fill flags |
| `findings-summary.md` | Headline conclusions + cross-references to detail files |

Length budget per file: ~1000-3000 words depending on coverage. Total: 5000-12000 words.

---

## 5. Downstream consumers

1. **gandalf** — folds findings into the Profile A asset-pipeline canonical doc (currently `canonical/story/asset-pipeline-meshy-swap-2026-05-22.md` — to be reframed tomorrow morning under Matt's general-engine reframe)
2. **Matt** — procurement decisions (Tier 1/2/3 budget commitment; specific pack purchases)
3. **drax** — G5-LITE Unity integration; armor pattern (Skinned Mesh Renderer vs. rigid attachment) per archetype
4. **rocket** — W1.15-LITE signature_gear_archetype derivation must include armor coverage if armor lands as a substrate dimension
5. **knight-rider** — protocol v1.3 → v1.4 amendment workstream (W1.7 legolas-Phase-2 procurement update + new W1.7b armor-scoping workstream if armor needs separate handling)

---

## 6. Timing

- **Earliest fire:** now (no fire-gate; Matt pre-authorized)
- **Duration:** 2-3 days mixed-mode research
- **No babysit.** Per Discipline #19 (RATIFIED 2026-05-22) — bounded sub-agent with explicit deliverables; findings directory is the cross-session continuity artifact

---

## 7. Cross-references

- `agentic_orchestration/legolas/research/meshy-pipeline-2026-05-22/findings.md` — your prior 2026-05-22 weapon-pipeline + irregular-monster research (foundation for this dispatch)
- `agentic_orchestration/legolas/research/substrate-sufficiency-audit-2026-05-20/phase-1-reconnaissance/` — your Phase 1 Asset Store partial coverage (build on this; do not re-derive)
- `canonical/story/gear-archetype-rule-table-v1-2026-05-22.md` § 2 — 15-archetype catalogue (Priority 2 matching target)
- `canonical/story/asset-pipeline-meshy-swap-2026-05-22.md` — Profile A pipeline doc (Priority 1 + 2 findings fold into § 3 + § 4)
- `canonical/story/style-register.md` — locked Reincarnated visual register
- `canonical/story/multi-dim-convergence-algorithm-2026-05-21.md` — 7-element substrate
- `~/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md` § 19 — RATIFIED 2026-05-22 (no babysit on the research)

---

**Signed:** gandalf (story-and-design steward; research commissioner)
**For:** Profile A asset procurement scoping + Meshy armor capability close + multi-genre Asset Store coverage analysis under Matt's general-engine reframe.
