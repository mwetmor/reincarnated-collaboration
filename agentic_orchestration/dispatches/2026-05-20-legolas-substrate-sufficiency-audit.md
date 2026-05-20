# Dispatch — Legolas Mode A: Substrate-Sufficiency + Comprehensive External-Asset Catalog Audit

**Date:** 2026-05-20
**Author:** gandalf
**Recipient:** legolas (Mode A — analytical research, multi-phase commission)
**Status:** ACTIVE (v3 — comprehensive scope after 2026-05-20 evening amendments)
**Priority:** HIGH (gates QD-engine rebuild commitment)
**Estimated effort:** 60-100+ hours of structured research + synthesis across multi-phase commission

---

## 0. TL;DR

This is a **comprehensive five-track research commission** that gates the QD-engine rebuild. It expanded substantially during 2026-05-20 evening conversation between Matt and gandalf as the architectural target sharpened.

**Five tracks:**

1. **Track A — Internal substrate inventory** (current engine state per axis × bin)
2. **Track B — Unity Asset Store comprehensive VFX catalog** (every relevant pack, tagged by geometry / timing / size / element / Mixamo-rig-compatibility)
3. **Track C — Mixamo deep animation inventory** (every detail; rig-anchor compatibility constraints)
4. **Track D — ARPG canon vision-layer skill geometry enumeration** (comprehensive enumeration of shipped skills across the ARPG canon to validate bin cuts and surface anything folded)
5. **Track E — Production pipeline integration audit** (ChatGPT Image Gen → Meshy 3D Model → Mixamo Rig → VFX-mapped — the canonical Reincarnated asset-creation pipeline)

**Two architectural layers (Matt's framing 2026-05-20 evening):**

- **Vision layer** — what is conceptually possible across the canon (Track D research feeds this)
- **Operational layer** — what fills the 8-axis × 24-bin space at ≥5× sufficiency (Tracks A, B, C feed this; Track E governs integration)

The vision layer informs whether our 8-axis lock captures the canon comprehensively or accidentally folds a meaningfully-distinct geometry/mechanic. The operational layer governs ship-readiness.

---

## 1. The locked 8 BC axes (operational target)

Reference: `canonical/story/qd-engine-bc-axes-lock-2026-05-20.md`

| # | Axis | Bins | Bin labels |
|---|---|---|---|
| 1 | **Engagement profile** | 6 | close-fast / close-slow / mid-fast / mid-slow / ranged-fast / ranged-slow |
| 2 | **Damage geometry** | 5 | single-target / small-AOE / large-AOE / chain / multi-spawn |
| 2A | **Proxy density** | 3 | solo / proxy-light / proxy-heavy |
| 2B | **Control density** | 3 | damage-pure / mixed / control-pure |
| 3A | **Damage tempo** | 3 | low / medium / high |
| 3B | **Damage amplitude variance** | 3 | flat / variable / spiky |
| 4 | **Defensive profile** | 4 | tank / mitigator / dodger / glass |
| 5 | **Resource economy** | 7 | HP-economy / charge-stack / damage-taken-converts / starved / overflow / generator-spender / steady |

Sufficiency rule: substrate must produce ≥ 5× the bin count of distinguishably-different outputs per axis.

---

## 1.5 Element / substrate dimension (cross-cutting tag)

Element is a **substrate-tagging dimension, NOT a 9th BC axis.** Each kit has an element tag (fire/water/earth/wind/etc.) that drives:

- Theme coalescence (LLM chooses element-themed names + flavor)
- Substrate filtering at generation time (use fire-VFX for fire kits)
- Profile filtering (B2B customers may want element-specific season packs)
- Style register alignment (visual element coherence)

**Canonical element list:** confirm from `reincarnated-engine/src/reincarnated/canonical/` element files. Initial prior (subject to verification): fire / water / earth / wind / lightning + possibly nature / arcane / dark / holy / void / blood. The D1 element-name pool work (2026-05-12) suggests a 5-primary core (fire / water / earth / wind / one-other) but the audit should confirm the operative list.

**Critical implication for Track B (Unity Asset Store catalog):** every VFX asset must be tagged with its element. When the engine generates a fire kit, the substrate-filtering layer needs to know which Unity packs provide fire-tinged effects. Same for water, earth, wind, etc.

---

## 1.6 Production pipeline integration constraint (Track E governance)

**The canonical Reincarnated asset-creation pipeline (per Matt 2026-05-20):**

```
ChatGPT Image Gen  →  Meshy 3D Model  →  Mixamo Rig  →  VFX mapped
```

Each stage constrains the next:

| Stage | Output | Constrains downstream |
|---|---|---|
| ChatGPT Image Gen | 2D image of character/monster/effect | Must produce Meshy-importable image (consistent perspective, clear silhouette) |
| Meshy 3D Model | 3D mesh from image | Must be Mixamo-compatible topology (humanoid preferred for Mixamo; other rigs need alternative rigging path) |
| Mixamo Rig | Rigged humanoid model with animation library | Must be VFX-mountable (standard Mixamo bone anchor points: hands, feet, head, weapon-attachment) |
| VFX mapped | Final usable asset for engine | Must work at Mixamo-rig anchor points with consistent style + element |

**Implications for Track B (Unity VFX catalog):**

Every Unity VFX pack assessed must be tagged for:
- Mixamo-rig compatibility (does it mount on standard Mixamo anchor points?)
- Required attachment points (hands? weapon? full-body aura? ground-anchored?)
- Scale matching (does it scale to Mixamo standard humanoid proportions?)
- Style register match (does it work with ChatGPT-Meshy stylization, or does it require a different visual style?)

VFX packs that don't fit this pipeline (e.g., custom-rig-required, non-humanoid-anchored, mismatched style register) are documented but flagged as low-priority for procurement.

---

## 2. Research tracks — five-track structure

### 2.1 Track A — Internal substrate inventory (codebase survey)

For each axis × bin, document what currently exists in the engine that could feed that bin:

- **Generation systems** — `reincarnated-engine/src/reincarnated/generation/`, `element/`, `anchor/`, `foundation/`
- **Canonical palette / library** — `reincarnated-engine/src/reincarnated/canonical/`
- **Skill / gear / kit templates** — current variety; BC-tagging discipline state
- **Simulation outcomes** — what telemetry currently exists to support BC measurement

**Key existing references:**
- `canonical/09-geometry-palette-discussion.md` — 16-type damage geometry palette
- `canonical/17-gear-and-spirit-guide-design.md` — gear architecture
- `canonical/32-progression-design.md` + `canonical/33-progression-skeleton.md` — class progression
- `reincarnated-engine/src/reincarnated/canonical/` — engine canonical library

**Deliverable:** per-axis CSV with current internal substrate count + 5×-rule gap analysis.

---

### 2.2 Track B — Unity Asset Store comprehensive VFX catalog (PRIMARY DELIVERABLE)

**Matt's directive 2026-05-20:** "research every single Unity VFX pack and list the geometry / timing / size / element"

The intent is comprehensive coverage. Practical scoping:
- "Every single" means **every relevant + quality-rated pack** (filter out abandoned packs, low-rated packs, single-asset junk; include high-rated packs even if niche)
- Phase 1: top 30-50 most-relevant packs cataloged in depth
- Phase 2: expansion to comprehensive coverage (200-500+ packs surveyed; ~100-200 cataloged in depth)
- Phase 3: synthesis + procurement recommendations

**Per-asset metadata required (each VFX in each pack):**

| Field | Values |
|---|---|
| `pack_name` | text |
| `pack_url` | text (Unity Asset Store URL) |
| `publisher` | text |
| `pack_price_usd` | numeric |
| `pack_license` | enum: single-seat / multi-seat / commercial / royalty-free |
| `asset_name` | text (specific VFX within pack) |
| `geometry` | enum: single-target / small-AOE / large-AOE / chain / multi-spawn / line / cone / radial-blast / persistent-ground / projectile / aura / point |
| `timing` | enum: instant / charge-up / channel / sustained / triggered / DOT |
| `size` | enum: small / medium / large / scaling / variable |
| `element` | enum: fire / water / earth / wind / lightning / nature / arcane / dark / holy / void / blood / physical / neutral |
| `target_type` | enum: self / target-locked / ground-aoe / projectile / aura |
| `mixamo_rig_compatible` | enum: yes / partial / no |
| `anchor_points` | comma-list: hands / weapon / feet / head / body / ground / target-locked |
| `style_register` | enum: realistic / stylized / cartoon / pixel / hybrid |
| `performance_tier` | enum: mobile / mid / high |
| `quality_rating` | numeric: 1-5 (publisher rating + review-derived) |
| `bc_axis_mapping` | per-axis mapping (axis_1 through axis_5: which bins does this asset serve?) |
| `notes` | text |

**Search priorities by axis (entry points; not exhaustive):**

| Axis | Unity Asset Store search targets |
|---|---|
| Axis 1 (Engagement) | Movement-skill VFX (dash, blink, teleport, charge); cyclone/channel-move VFX; ranged-cast traversal effects |
| Axis 2 (Geometry) | AOE VFX (radial blast, ground-effect persistent), chain-lightning, multi-spawn (meteor/area-explosion), single-target projectile |
| Axis 2A (Proxy) | Summon/minion/totem VFX; spawn-effect VFX; convert/charm effect packs |
| Axis 2B (Control) | CC VFX (stun, freeze, root, fear, blind, knockback); slow-aura; debuff visualizations |
| Axis 3 (Rhythm) | Channel-skill VFX; charge-up effects; burst-skill telegraphs |
| Axis 4 (Defense) | Shield/aura VFX; dodge/iframe cues; stealth/invisibility shaders; reflection effects; thorns/spike-aura |
| Axis 5 (Economy) | Resource-conversion VFX (life-leech, mana-conversion); charge-stack visualizers; HP-cost feedback |

**Per-element search priority (the substrate-element catalog):**
- Fire VFX packs (likely high availability — fire is dominant in Unity asset library)
- Water/ice/frost VFX packs
- Earth/stone/nature VFX packs
- Wind/air/storm VFX packs
- Lightning/electric VFX packs
- Dark/void/blood VFX packs (if those elements are canonical)

---

### 2.3 Track C — Mixamo deep animation inventory

**Matt's directive 2026-05-20:** "gather all of the details we can from Mixamo"

Mixamo is Adobe's free animation library tied to the canonical production pipeline. Deep inventory required because **VFX must mount on Mixamo-rigged characters** — the two go hand in hand.

**Per-category catalog required:**

| Field | Notes |
|---|---|
| Category name | Mixamo's classification (e.g., "Melee attack," "Spell casting," "Dodge / evade") |
| Animation count | How many distinct animations in this category |
| Sub-categories | If applicable (e.g., melee → sword / spear / bow / unarmed) |
| Rig type | Standard Mixamo humanoid? Other? |
| Animation length range | Min/max duration |
| Loop-capable count | How many loop cleanly |
| Compatible VFX anchor points | Which body parts move; which can host VFX attachments |
| BC axis relevance | Per-axis mapping (especially Axis 1 mobility, Axis 2 geometry, Axis 4 defensive — dodge animations) |
| License terms | Mixamo standard terms; commercial use; any restrictions |

**Specific Mixamo categories to inventory:**
- Movement (walk, run, sprint, dodge, dash, blink-substitutes)
- Combat — melee (all weapon types)
- Combat — ranged (bow, throw, cast)
- Combat — spell-casting (channel, instant cast, charge-cast)
- Combat — defensive (block, parry, evade, hit-react)
- Death / down
- Idle / breathing
- Emote / non-combat
- Boss / monster (if Mixamo has non-humanoid rigs)

---

### 2.4 Track D — ARPG canon vision-layer skill geometry enumeration (NEW PER MATT 2026-05-20)

**The vision-vs-operational distinction (Matt's insight 2026-05-20 evening):**

- The **operational layer** locks 5 bins for damage geometry (single-target / small-AOE / large-AOE / chain / multi-spawn). The substrate audit measures sufficiency against these bins.
- The **vision layer** asks: across the entire ARPG canon, are there shipped skill geometries that don't fit cleanly into these 5 bins? If so, the bin cuts may be wrong, OR we may have folded something that deserves its own bin in a future revision.

**Track D commission:** comprehensive enumeration of shipped skill geometries across the ARPG canon. For each skill:

| Field | Notes |
|---|---|
| `game` | Diablo 1/2/3/4/Immortal, PoE, PoE2, Last Epoch, Grim Dawn, Torchlight 1/2/3, Lost Ark, Wolcen, Wolcen, Marvel Heroes, others |
| `class` | The class the skill belongs to |
| `skill_name` | Canonical name |
| `geometry` | Same enum as Track B (single-target / small-AOE / large-AOE / chain / multi-spawn / line / cone / etc.) |
| `element` | Fire / cold / lightning / poison / physical / etc. |
| `timing_pattern` | Instant / channel / charge-up / DOT / triggered / etc. |
| `defensive_offensive_role` | Primary damage / support / mobility / defense / utility |
| `signature_or_minor` | Signature skill (a build-defining choice) vs minor (gap-filler skill) |
| `notes` | Special mechanics: charge stacks, reactive triggers, etc. |

**Scope honest-truth:** there are ~10,000+ shipped ARPG skills. Comprehensive enumeration is not realistic in a single phase. Practical scoping:

- **Phase 1**: 50-100 most-iconic, signature shipped skills (the ones every ARPG fan knows by name)
- **Phase 2**: expansion to 300-500 (full canonical class skill rosters for D2, D3, D4, PoE)
- **Phase 3**: comprehensive sweep targeting ~1000+ unique geometries

**Cross-references for canonical enumeration:**
- PoE Wiki skill gem inventory
- Diablo 3 Diablofans / Maxroll skill databases
- Diablo 4 official codex
- Last Epoch wiki
- Grim Dawn wiki
- Diablo 2 wiki / Path of Diablo databases

**Vision-layer-validation output:**

After enumeration, surface:
1. Skill geometries that don't fit cleanly into our 5 operational bins (candidates for future bin-cut revision)
2. Element distributions across the canon (informs canonical element list)
3. Timing patterns across the canon (validates Axis 3A/3B + structural tags)
4. Recurring geometry/element/timing combinations (validates whole-kit archetypes)

---

### 2.5 Track E — Production pipeline integration audit

**The canonical pipeline:** ChatGPT Image Gen → Meshy 3D Model → Mixamo Rig → VFX mapped

For each stage, document:

| Stage | Audit questions |
|---|---|
| ChatGPT Image Gen | What prompts produce Meshy-importable images? Style consistency? Cost per image? Iteration speed? |
| Meshy 3D Model | What image formats work best? Output mesh quality? Topology compatibility with Mixamo? Manual cleanup required? Cost per model? |
| Mixamo Rig | Which Meshy outputs auto-rig cleanly? Manual rigging fallback? Animation-library compatibility? Custom-rig path for non-humanoid? |
| VFX mapping | Unity workflow for attaching VFX to Mixamo-rigged characters? Anchor-point conventions? Performance implications? |

**Deliverable:** integration playbook documenting the working pipeline, known failure modes, manual-intervention steps, and recommendations for pipeline improvements.

---

## 3. Deliverables (multi-phase)

Final deliverable location:

```
agentic_orchestration/legolas/research/substrate-sufficiency-audit-2026-05-2X/
  ├── phase-1-reconnaissance/
  │   ├── summary.md
  │   ├── unity-store-initial-survey.md
  │   ├── mixamo-initial-inventory.md
  │   ├── arpg-canon-initial-enumeration.md
  │   ├── pipeline-integration-notes.md
  │   ├── internal-substrate-state.md
  │   └── methodology-questions-for-matt.md
  ├── phase-2-depth-pass/
  │   └── (deeper per-track research)
  ├── phase-3-synthesis/
  │   └── (final recommendations + procurement shortlist)
  └── data/
      ├── unity-asset-catalog.csv          ← Track B comprehensive
      ├── mixamo-animation-catalog.csv     ← Track C comprehensive
      ├── arpg-canon-skill-catalog.csv     ← Track D comprehensive
      ├── per-axis-internal-substrate.csv  ← Track A
      └── pipeline-integration-checklist.csv ← Track E
```

### 3.1 Phase 1 — Reconnaissance pass (initial Agent invocation)

**Scope:** establish methodology + initial findings across all five tracks. Out of scope: comprehensive coverage.

**Deliverables:**
- `summary.md` (3-4 pages): reconnaissance findings, methodology validation, surprises, recommendations for Phase 2 scoping
- `unity-store-initial-survey.md`: top 20-30 candidate packs cataloged in depth with all metadata fields
- `mixamo-initial-inventory.md`: category-level inventory + animation counts per category
- `arpg-canon-initial-enumeration.md`: 50-100 most-iconic shipped skills cataloged
- `pipeline-integration-notes.md`: initial pipeline audit findings
- `internal-substrate-state.md`: per-axis quick assessment of current engine substrate
- `methodology-questions-for-matt.md`: scoping questions + recommendations for Phase 2 priorities
- All Phase 1 data CSVs populated with initial entries

**Phase 1 effort estimate:** 8-15 hours of focused research time

### 3.2 Phase 2 — Depth pass (subsequent invocations as authorized)

**Scope:** comprehensive coverage of all five tracks based on Phase 1 methodology + Matt's Phase 1 review feedback.

**Phase 2 effort estimate:** 30-60 additional hours; potentially split across multiple Agent invocations

### 3.3 Phase 3 — Synthesis + procurement recommendations

**Scope:** final analysis, gap closure recommendations, procurement shortlists with cost estimates, integration sequencing.

**Phase 3 effort estimate:** 8-15 hours

---

## 4. Methodology constraints

- **Read-only across all sources.** No code changes, no asset acquisitions, no schema modifications. Pure research.
- **Cite specifically.** Internal: file paths + line numbers. External: pack/asset name + URL + asset count + license terms verbatim.
- **Estimate honestly.** When "distinguishable output count" is fuzzy, say so. Better to flag as `~15-25, hard to count` than commit to a false-precision `19`.
- **Stay in Mode A.** Do not invoke sub-agents (per `.claude/agents/legolas.md` § sub-agent constraint).
- **No commitment authority.** Recommendations are recommendations; gandalf reviews + Matt approves before procurement or engineering work begins.
- **Phase 1 is reconnaissance, not comprehensive.** Do not over-commit Phase 1 effort to depth in one track at the expense of breadth across all five.
- **Surface methodology questions early.** If a track has ambiguous scope or unclear sources, ask in `methodology-questions-for-matt.md` rather than guess.

---

## 5. Cross-references

- `canonical/story/engine-architecture-vision-qd-profile-2026-05-19.md` — the architectural target
- **`canonical/story/qd-engine-bc-axes-lock-2026-05-20.md`** — **AUTHORITATIVE 8-axis operational spec; this dispatch operationalizes the audit of that spec**
- `canonical/story/hive-mind-protocol-per-tier-recompose-validation-2026-05-19.md` — concurrent hive (recompose validation)
- `reincarnated-engine/design/working-agreement/engineering-disciplines.md` — disciplines #13a / #13b / #17
- `canonical/09-geometry-palette-discussion.md` — 16-type geometry palette; Axis 2 baseline
- `canonical/17-gear-and-spirit-guide-design.md` — gear architecture; Axes 3, 4, 5 baseline
- `reincarnated-engine/src/reincarnated/canonical/` — canonical engine library (element list source)

---

## 6. Timing + phasing

- **Phase 1 start:** immediately upon Agent fire
- **Phase 1 completion:** single Agent session (8-15 hours of effective research time)
- **Phase 1 review:** gandalf + Matt review Phase 1 findings; scope Phase 2
- **Phase 2 start:** authorized after Phase 1 review
- **Phase 2 completion:** 30-60 hours, potentially across multiple Agent invocations
- **Phase 3 start:** authorized after Phase 2 review
- **Total commission completion target:** 1-3 weeks

**Blocks:** QD-engine rebuild start (cannot commit until commission Phase 3 + recompose-hive both ship)

**Concurrent with:** recompose-validation hive (firing now); no interaction needed

---

## 7. Escalation

- **Methodology questions:** route to gandalf via Phase deliverable `methodology-questions-for-matt.md`
- **Scope/priority disputes:** gandalf decides; escalate to Matt only if gandalf+legolas cannot converge
- **External-asset license ambiguities:** flag in summary; do not attempt to resolve
- **If audit surfaces axes that look structurally impossible given current architecture:** flag immediately to gandalf; may trigger axis-lock revision
- **If Track D enumeration surfaces a geometry that doesn't fit our 5 bins:** flag explicitly; this is the vision-layer-validation output we want

---

**Signed:** gandalf (story-and-design steward)
**For:** the QD-engine architectural commitment, fully operationalized with vision-layer validation.
