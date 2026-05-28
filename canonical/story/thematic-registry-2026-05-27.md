# THEMATIC REGISTRY — substrate-led term-pool for Phase 5 LLM consumption

**STATUS:** CURRENT (Stage 1 of 4 — header + reconciliations + schema; Stages 2-4 pending)
**Date:** 2026-05-27
**Author:** gandalf
**Status:** authoring — incremental write per stall-recovery protocol; sections 1-5 land in this commit
**Authority:** Matt-gate Path (1) RATIFIED 2026-05-27 (THEMATIC_REGISTRY gates Wave 3 Phase 5 LLM impl); knight-rider routing under hive-mind crash-recovery § 2.4

**Companion docs:**

- `~/Games/reincarnated-engine/src/reincarnated/generation/math/phase-5-pm-2-faction-label-assignment-math-2026-05-27.md` § 12 (consumption surface — Wave A faction-level)
- `~/Games/reincarnated-engine/src/reincarnated/generation/math/wave-1-5-option-alpha-kit-naming-policy-math-2026-05-27.md` § 5.2 (consumption surface — Wave B per-kit identity)
- `canonical/00-ground-state.md` § 1 registration: pending Stage 4 sign-off
- `canonical/story/marginal-lineage-tagging-pattern-2026-05-23.md` (substrate contamination disposition baseline)
- `agentic_orchestration/dispatches/2026-05-27-gandalf-thematic-registry-continuation-incremental.md` (stage protocol)
- `agentic_orchestration/dispatches/2026-05-27-gandalf-thematic-registry-authoring.md` (original dispatch + acceptance criteria)

**Authority chain:**

Matt-gate (2026-05-27 ratification) → gandalf authorship → knight-rider sequencing → jack-ryan Gate-1/Gate-2 review at sign-off → star-lord Phase 5 LLM-prompt consumption at Wave A + Wave B fire-time.

---

## § 1 Purpose and scope

The THEMATIC REGISTRY is the **substrate-led term-pool** that Phase 5 LLM prompts (PM-2 faction-label assignment; Wave 1.5 Option Alpha per-kit naming) draw vocabulary from. It exists to enforce two anti-patterns simultaneously:

1. **NO pre-authored faction taxonomy.** The registry does NOT prescribe "the Order of X," "the Ashen Cult," or any pre-named factions. Factions emerge from clustering at Wave A; the registry provides only the *vocabulary palette* the labeller draws from.
2. **NO class-vocabulary leak into faction/kit naming.** Words like "warrior," "mage," "rogue," "tank," "support" do not appear in this registry. Class identity is an engine-internal concept; faction identity is a thematic-cohesion concept; the two surfaces are kept lexically isolated.

The registry is consumed at Phase 5 fire-time by:

- **Wave A (PM-2 § 12):** faction-label assignment over the BC-axis cluster ground; LLM picks a faction epithet + motif + lore-fragment per cluster from the registry, conditioned on cluster centroid + dominant weapon_type_family + dominant cultural_lineage.
- **Wave B (Note 4 § 5.2):** per-kit identity naming within a faction; LLM picks archetype-name + place-name + secondary motif from the registry, conditioned on kit substrate-vector + assigned faction.

**Out of scope for this registry:** narrative prescription (no faction backstory beyond lore-fragment seeds), theological systematization (faith/holy cell provides motif tokens NOT doctrine), kit-specific class identity (handled engine-internal at the role/orientation layer per `canonical/historical/role_orientation_taxonomy`).

## § 2 Ground rules

The registry obeys six discipline rules. Violations are caught by jack-ryan Gate-2 + grep audit at Stage 4 sign-off.

1. **Substrate-led (Discipline #41).** Every entry traces to substrate evidence — either telemetry.db `weapon_knowledge_entries` v1_scope=1 rows (cultural_lineage + element columns), legolas crawl outputs, or existing canonical/story/ thematic-vocabulary precedent. No pre-imposed terms that lack substrate anchor.
2. **Term-pool NOT prescriptive taxonomy.** Entries are vocabulary atoms (epithets, motifs, names) the LLM samples from. The registry does not say "fire+european means X faction"; it says "the dense fire×european cell has these epithet tokens available."
3. **Sketch tier 20-50 entries per dense cell** (Stages 2-3). Below 20 = SPARSE label; below 5 = EMPTY label. Density imbalance reflects substrate reality (Discipline #41 not violated by under-dense cells — substrate is the determinant).
4. **No class-vocabulary leak.** Hard ban list: warrior, mage, rogue, hunter, paladin, summoner, monk, druid, necromancer, sorcerer, witch, knight, soldier, ranger, archer, assassin, berserker, gladiator, fighter, controller, tank, support, healer, damage, dps. Plus role-orientation tokens (damage / support / control / hybrid).
5. **Marginal-lineage contamination is a watch-item (NOT a blocker).** 4 of 5 marginal lineages (arctic_circumpolar / oceanic / n.am.indigenous / s.am.indigenous; mesoamerican exempted per disposition docs 2026-05-23) carry substrate contamination per Mode A/B/C/D pattern. Entries derived from these cells are flagged in-cell at Stage 2-3 authoring; elrond substrate re-curation candidate is logged at Stage 4 but is NOT a Stage-1 gate. (Q-TR-Cont-2 disposition: registry-level watch-item; do not escalate to Discipline #41 violation at this stage because substrate-anchored entries are still substrate-anchored even when sourced from contaminated cells — the contamination is about *cell density misattribution*, not about the *terms themselves being non-substrate*.)
6. **Lexical isolation from engine internals.** The registry is the player-facing thematic surface vocabulary. Engine-internal identifiers (cluster_id, kit_signature, BC-axis bin labels, role_orientation tags) do NOT appear here.

## § 3 Element reconciliation

The engine canonical element axis has **8 elements** (per `canonical/historical/geometry_palette_discussion` lineage; ratified through substrate Mode A/B/C/D crawl):

| Element | Canonical | Caster-route note |
|---|---|---|
| arcane | yes | routes to weapon_type_family = caster-arcane (staves, orbs, foci, sigils) |
| faith-holy | yes | routes to weapon_type_family = caster-faith (relics, censers, sacred-text-instruments, prayer-foci) |
| fire | yes | element-class agnostic (any weapon_type_family) |
| water | yes | element-class agnostic |
| earth | yes | element-class agnostic |
| wind | yes | element-class agnostic |
| shadow | yes | element-class agnostic |
| lightning | yes | element-class agnostic |

**Routing note for LLM prompt construction:** when a cluster centroid lands in arcane or faith-holy AND weapon_type_family is caster-arcane or caster-faith respectively, the registry cell access is the *intersection* (arcane × caster-arcane × cultural_lineage; faith × caster-faith × cultural_lineage) — these are the densest cells in their respective columns by substrate count. Other element × weapon_type_family combinations are non-routed (any combination valid).

**Why 8 not more:** the registry does not subdivide elements further (no "frost" sub-element under water; no "ash" sub-element under fire). Element granularity is locked at the engine-canonical 8; sub-thematic variation is captured via *motif tokens within a cell* (e.g., fire cell contains both "ember-glow" and "ash-fall" motifs without making them separate elements).

**Cell coordinate convention:** registry cells are indexed as `(element, weapon_type_family, cultural_lineage)`. Total possible cells = 8 × 6 × 15 = 720. Realistic dense cells per substrate: ~12-15 (per prior fire's planning; confirmed at Stage 3 authoring).

## § 4 Cultural_lineage reconciliation

The substrate `weapon_knowledge_entries.cultural_lineage` column carries **13 lineage tags + 2 meta-tags** (per gandalf prior fire's enumeration; cross-checked against marginal-lineage disposition docs 2026-05-23):

| Lineage tag | Substrate density (qualitative) | Contamination watch-item |
|---|---|---|
| european | dense | no |
| east_asian | dense | no |
| south_asian | moderate-dense | no |
| southeast_asian | moderate | no |
| middle_eastern | dense | no |
| african | moderate | no |
| n.am.indigenous | SPARSE | YES (Mode A/B/C/D contamination — `n-am-indigenous-no-cluster-disposition-2026-05-23.md`) |
| mesoamerican | moderate | no (exempted per `mesoamerican-marginal-lineage-disposition-2026-05-23.md`) |
| s.am.indigenous | SPARSE | YES (per `south-american-indigenous-marginal-lineage-disposition-2026-05-23.md`) |
| arctic_circumpolar | SPARSE | YES (per `arctic-circumpolar-marginal-lineage-disposition-2026-05-23.md`) |
| oceanic | SPARSE | YES (per `oceanic-marginal-lineage-disposition-2026-05-23.md`) |
| fantasy_generic | dense | no (generic-pool not contaminated; intentionally synthetic) |
| sci_fi_generic | moderate | no |
| **cross_cultural** (meta-tag) | applied at LLM-prompt-time when cluster spans 3+ lineages | n/a |
| **unknown** (meta-tag) | applied at LLM-prompt-time when cluster has insufficient lineage signal | n/a |

**Marginal-lineage contamination caveat (Q-TR-Cont-2 disposition):**

The 4-of-5 marginal-lineage contamination pattern (per Mode A/B/C/D substrate analysis) means substrate entries tagged with `n.am.indigenous`, `s.am.indigenous`, `arctic_circumpolar`, and `oceanic` have elevated misattribution risk — some entries may reflect generic-fantasy or european substrate that picked up the marginal tag through crawl noise. This is **logged as a registry-level watch-item** for Stage 2-3 authoring (cells in these columns are flagged in-cell with `[contamination-watch]` marker) and as an **elrond substrate re-curation candidate** for post-Wave-3 work. It is NOT a Stage 1 gate because the registry's job is to provide vocabulary the LLM can draw from; contaminated cells still surface valid substrate-anchored vocabulary, they just under-represent the named lineage's actual signal. Phase 5 LLM-prompt consumption can apply additional `[contamination-watch]` weighting at fire-time if Wave A/B output shows lineage-misattribution patterns.

**Why 13 not more:** lineage granularity is locked at the substrate-column resolution. Sub-regional variation (e.g., "celtic" within european; "tibetan" within east_asian) is captured via *place-name tokens within a cell* — not as separate lineage axes.

## § 5 Per-cell schema (term-type tags)

Each registry cell is a bag of vocabulary atoms. Every atom carries a **term-type tag** from the 5-tag schema:

| Term-type tag | Purpose | LLM consumption pattern | Example shape (not substantive — Stages 2-3 fill cells) |
|---|---|---|---|
| `epithet` | faction or kit honorific / descriptor (Wave A primary; Wave B secondary) | drawn at faction-label assignment as the *modifier* (e.g., "{epithet} of the {motif}") | "ashen-handed" / "sea-bound" / "iron-hearted" |
| `motif` | central thematic image / symbol (Wave A primary; Wave B reinforcement) | drawn at faction-label as the *substantive* paired with epithet | "the broken oath" / "the long winter" / "the watchful sun" |
| `archetype-name` | character archetype the kit identity evokes (Wave B primary) | drawn at per-kit naming as the *identity anchor* — explicitly NOT a class name | "the wanderer" / "the keeper" / "the witness" |
| `place-name` | location / region / landmark token (Wave B reinforcement) | drawn at per-kit naming when faction-place-binding is signaled by cluster | "the bonefields" / "the salt-roads" / "the cinder-passes" |
| `lore-fragment` | seed phrase the LLM can paraphrase into 1-2 sentence faction backstory (Wave A only) | drawn at faction-label as the *backstory seed* — phrase NOT full sentence | "exiled when the third star fell" / "the river chose them" |

**Term-type discipline rules:**

- Each cell SHOULD contain entries across multiple term-types (mixed-bag, not single-type cells). Target distribution per dense cell: ~10 epithet + ~10 motif + ~5 archetype-name + ~3 place-name + ~3 lore-fragment (~31 entries; within 20-50 sketch tier).
- `archetype-name` entries MUST NOT collide with the class-vocabulary ban list (Ground Rule #4). The archetype is *narrative role*, not *combat role*.
- `lore-fragment` entries are intentionally elliptical — they are seeds for LLM elaboration, not finished prose. The LLM paraphrases into context-fitting backstory at fire-time.
- `place-name` entries are *evocative*, not *geographic*. They do not need to map to a fictional world-map (which Reincarnated does not maintain at Phase 0); they are tone-anchors.
- `motif` and `epithet` are the LLM's *combinatorial pair*: faction names assemble as `{epithet} {meta-noun} of the {motif}` or `the {motif} {meta-noun}` where `{meta-noun}` is supplied by the LLM (NOT from the registry) from a small allowed set (`order`, `circle`, `host`, `path`, `vigil`, `keepers`, `chosen`, `legion`, `covenant`).

**Why this schema and not freeform tokens:** the LLM benefits from term-type tagging because it constrains the prompt assembly. Without tags, the LLM must guess which token is a faction epithet vs a kit archetype-name; with tags, the prompt can directly slot tokens into the assembly template per Wave A § 12 / Wave B § 5.2 consumption surfaces.

---

*Stages 2-4 to follow: § 6 element-only registry (~200 entries) / § 7 per-cell sketches (dense cells 20-50 entries each, SPARSE/EMPTY labels for thin) / § 8 anti-patterns / § 9 consumption-pattern documentation / § 10 Cycle 15+ expansion path / § Sign-off + framing-audit + Discipline #41 grep-audit record.*
