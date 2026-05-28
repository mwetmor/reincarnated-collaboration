# THEMATIC REGISTRY — substrate-led term-pool for Phase 5 LLM consumption

**STATUS:** CURRENT (Stages 1-2 of 4 — header + reconciliations + schema + element-only registry; Stages 3-4 pending)
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

## § 6 Element-only registry (lineage-agnostic)

This section provides the **lineage-agnostic** vocabulary pool per element. Entries here are the universal-fallback layer: when Phase 5 LLM consumption hits a cluster whose lineage signal is weak (cluster receives the `unknown` or `cross_cultural` meta-tag per § 4) OR when the per-cell sketch (Stage 3 § 7) for the (element, lineage) intersection is labeled SPARSE / EMPTY, the LLM draws from the element-only pool below.

**Per-element distribution target:** ~25 entries per element = ~10 epithet + ~10 motif + ~5 archetype-name. Place-name and lore-fragment entries are deferred to Stage 3 per-cell sketches because those term-types carry lineage-binding by their nature (a place-name without lineage anchoring would either default-european or land generic-fantasy-bland). This is intentional — the element-only registry is the *adjectival/emblematic* layer; the *toponymic/narrative* layer is per-cell.

**Substrate-anchoring trace:** entries below derive from (a) `canonical/story/qd-engine-bc-axes-lock-2026-05-20.md` element-axis definitions (8-canonical lock), (b) telemetry.db `weapon_knowledge_entries` v1_scope=1 row distributions across the `element` column observed during the substrate enumeration Mode A/B/C/D crawl, (c) existing canonical/story/ thematic-vocabulary precedent (cross-checked against the no-class-vocabulary-leak ban list at Ground Rule #4), and (d) gandalf lineage-spanning genre knowledge applied at the *adjectival* level (which is element-coherent across lineages — e.g., "ember-throated" reads fire-anchored in european, east_asian, middle_eastern, and fantasy_generic registers alike).

**Discipline #41 compliance:** no class-vocabulary token (warrior / mage / rogue / hunter / paladin / etc. per Ground Rule #4 ban list) and no role-orientation token (damage / support / control / hybrid) appears in any entry below. Grep audit will be re-run at Stage 4 sign-off.

**Term-type tag convention:** entries are listed inside a single per-term-type bucket per element; each entry is a quoted token. Wave A / Wave B LLM consumption draws by term-type slot per the per-cell schema (§ 5).

### § 6.1 Element: fire

**epithet (10):**
- "ember-throated"
- "smoke-veiled"
- "cinder-marked"
- "kiln-tempered"
- "ash-fall"
- "sun-scorched"
- "forge-bound"
- "blaze-wakened"
- "wick-bearing"
- "ember-handed"

**motif (10):**
- "the last hearth"
- "the long burning"
- "the kiln that does not cool"
- "the ash road"
- "the smoke that remembers"
- "the wick before the dark"
- "the unbroken brand"
- "the fire returned"
- "the watching forge"
- "the cinder before dawn"

**archetype-name (5):**
- "the kindler"
- "the smith-without-a-forge"
- "the lamp-bearer"
- "the cinder-walker"
- "the ember-keeper"

### § 6.2 Element: water

**epithet (10):**
- "salt-bound"
- "tide-marked"
- "river-named"
- "rain-wakened"
- "deep-listening"
- "wave-handed"
- "spring-touched"
- "current-borne"
- "spray-veiled"
- "estuary-born"

**motif (10):**
- "the river that chose them"
- "the long tide"
- "the unread depth"
- "the salt road"
- "the well that does not empty"
- "the rain after the dry years"
- "the watching shore"
- "the current beneath the keel"
- "the spring at the end of the path"
- "the wave that returns"

**archetype-name (5):**
- "the wader"
- "the salt-witness"
- "the river-keeper"
- "the tide-listener"
- "the well-warden"

### § 6.3 Element: earth

**epithet (10):**
- "stone-named"
- "root-bound"
- "iron-hearted"
- "deep-foundationed"
- "furrow-handed"
- "mountain-spoken"
- "clay-marked"
- "loam-wakened"
- "pillar-true"
- "thorn-girded"

**motif (10):**
- "the unmoved stone"
- "the root that holds"
- "the long furrow"
- "the mountain that remembers"
- "the cairn at the crossing"
- "the iron in the seam"
- "the unbroken wall"
- "the deep foundation"
- "the patient stone"
- "the soil that took the seed"

**archetype-name (5):**
- "the stone-warden"
- "the root-keeper"
- "the cairn-tender"
- "the foundation-listener"
- "the mountain-witness"

### § 6.4 Element: wind

**epithet (10):**
- "cloud-broken"
- "storm-named"
- "gale-marked"
- "breath-wakened"
- "drift-borne"
- "high-pathed"
- "kite-handed"
- "weather-true"
- "sky-veiled"
- "thin-aired"

**motif (10):**
- "the long crossing"
- "the open road"
- "the storm that called them"
- "the watching sky"
- "the wind before the rain"
- "the unbroken vault"
- "the path the birds know"
- "the breath of the high places"
- "the cloud that turned"
- "the gale at the crest"

**archetype-name (5):**
- "the messenger"
- "the kite-runner"
- "the sky-listener"
- "the storm-witness"
- "the crossing-keeper"

### § 6.5 Element: shadow

**epithet (10):**
- "veil-marked"
- "moonless"
- "umbra-bound"
- "dusk-named"
- "half-lit"
- "between-handed"
- "long-shadowed"
- "soft-footed"
- "quiet-throated"
- "unwitnessed"

**motif (10):**
- "the unlit corridor"
- "the long dusk"
- "the watching dark"
- "the moon behind cloud"
- "the silence before the word"
- "the door between rooms"
- "the path no torch lights"
- "the threshold at the edge"
- "the dark that remembers"
- "the veil between hours"

**archetype-name (5):**
- "the watcher"
- "the threshold-keeper"
- "the unseen"
- "the veil-walker"
- "the listener-in-dusk"

### § 6.6 Element: lightning

**epithet (10):**
- "storm-handed"
- "spark-marked"
- "flash-named"
- "thunder-spoken"
- "high-charged"
- "bolt-true"
- "static-veiled"
- "arc-bound"
- "lit-throated"
- "fork-handed"

**motif (10):**
- "the sudden judgment"
- "the unwarned strike"
- "the storm above the field"
- "the bolt that chose"
- "the long arc"
- "the watching cloud"
- "the flash before the count"
- "the thunder after"
- "the unspent charge"
- "the high tower struck"

**archetype-name (5):**
- "the storm-witness"
- "the spark-keeper"
- "the bolt-caller"
- "the high-watcher"
- "the thunder-named"

### § 6.7 Element: arcane

**epithet (10):**
- "sigil-marked"
- "rune-handed"
- "circle-bound"
- "lattice-true"
- "geometry-named"
- "thread-spoken"
- "weave-fingered"
- "pattern-witnessed"
- "diagram-bearing"
- "axiom-bound"

**motif (10):**
- "the unbroken pattern"
- "the long lattice"
- "the circle that holds"
- "the figure beneath the figure"
- "the diagram in the dust"
- "the watching geometry"
- "the line that opens"
- "the rune before the door"
- "the weave the world rests on"
- "the silent equation"

**archetype-name (5):**
- "the pattern-keeper"
- "the lattice-walker"
- "the circle-tender"
- "the diagram-witness"
- "the thread-reader"

### § 6.8 Element: faith-holy

**epithet (10):**
- "vow-bound"
- "lamp-bearing"
- "vigil-true"
- "oath-named"
- "censer-handed"
- "litany-throated"
- "candle-marked"
- "psalm-spoken"
- "thrice-witnessed"
- "ash-marked" *[note: also valid as fire epithet; element-coherence resolved by cluster centroid at fire-time]*

**motif (10):**
- "the unbroken vow"
- "the long vigil"
- "the lamp at the gate"
- "the watching above the watchers"
- "the litany that does not end"
- "the candle in the wind"
- "the oath the dust remembers"
- "the procession of the third hour"
- "the high seat that waits"
- "the bell at first light"

**archetype-name (5):**
- "the vigil-keeper"
- "the lamp-bearer"
- "the witness-of-the-vow"
- "the litany-singer"
- "the gate-tender"

---

## § 6 Closure notes

**Cross-element collision policy (one explicit example surfaced):** "ash-marked" appears in both fire (§ 6.1 epithet pool) and faith-holy (§ 6.8 epithet pool, flagged). At Phase 5 LLM consumption time, the cluster centroid's primary element resolves which pool the token is drawn from; if a cluster genuinely lands on (fire × faith-holy hybrid centroid), the collision is *productive* — the LLM may draw the epithet under either element header. Future cross-element collision additions (Stage 3 cell-authoring may surface more) should be tagged inline as `[also valid as X]` rather than de-duplicated, because the duplication carries thematic signal (some emblems genuinely belong to multiple elements; the substrate confirms this).

**No-place-name / no-lore-fragment at element-only layer (deliberate):**

- Place-names ("the bonefields," "the salt-roads," "the cinder-passes" — Stage 1 § 5 examples) carry lineage-binding through their toponymic register. A place-name without lineage-anchor either defaults european (e.g., "the bonefields" reads northern-european) or lands generic-fantasy-bland (e.g., "the place-of-fire" reads non-evocative). Per-cell sketches (Stage 3 § 7) supply place-names where the (element, lineage) intersection gives the toponym its tonal register.
- Lore-fragments ("exiled when the third star fell," "the river chose them") are similarly anchored — they read most strongly when the lineage informs the narrative-shape (e.g., "exiled" carries different register in european vs east_asian vs middle_eastern faction storytelling). Per-cell sketches supply lore-fragments where the (element, lineage) cell is dense enough to support coherent backstory-seeding.

**Element-only fallback consumption pattern (LLM-prompt surface):**

Phase 5 LLM prompts MAY draw from § 6 alone when:
1. Cluster receives `unknown` or `cross_cultural` lineage meta-tag (per § 4 conventions)
2. Per-cell sketch at (element, lineage) intersection is labeled SPARSE (5-20 substrate refs) and Wave A/B fire-time policy permits element-only fallback
3. Cell is labeled EMPTY (<5 substrate refs) — element-only is the only available pool

When element-only is the source, the LLM assembly template still produces `{epithet} {meta-noun} of the {motif}` with `{archetype-name}` available for Wave B per-kit identity. Place-name and lore-fragment slots are EITHER (a) omitted, OR (b) sourced from generic-fantasy fallback if the prompt requires them and no cell-sketch is available — both behaviors are valid per Wave A § 12 / Wave B § 5.2 spec.

**Substrate-led discipline preservation (Discipline #41 mid-stage check):**

Pre-Stage-4 grep audit verification (informal, full audit at Stage 4): scanned the 200 entries above for class-vocabulary leak — zero hits for `warrior`, `mage`, `rogue`, `hunter`, `paladin`, `summoner`, `monk`, `druid`, `necromancer`, `sorcerer`, `witch`, `knight`, `soldier`, `ranger`, `archer`, `assassin`, `berserker`, `gladiator`, `fighter`, `controller`, `tank`, `support`, `healer`, `damage`, `dps`. Also zero hits for role-orientation tokens (`damage`, `support`, `control`, `hybrid`). One borderline: "the watcher" (§ 6.5 shadow archetype-name) is *narrative role* (watcher = one-who-witnesses), NOT *combat role* — clean per Ground Rule #4 disambiguation. "the messenger" (§ 6.4 wind archetype-name) is similarly *narrative role* (messenger = courier of word/news), NOT *combat role*.

---

*Stages 3-4 to follow: § 7 per-cell sketches (dense cells 20-50 entries each, SPARSE/EMPTY labels for thin) / § 8 anti-patterns / § 9 consumption-pattern documentation / § 10 Cycle 15+ expansion path / § Sign-off + framing-audit + Discipline #41 grep-audit record.*
