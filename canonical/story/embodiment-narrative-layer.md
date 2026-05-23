# Embodiment Narrative Layer

> **STATUS:** HISTORICAL-INFORMATIVE (pre-Epoch-4; consult for lineage only — not current truth) — see `canonical/00-ground-state.md` for current truth

**Status:** **Canonical.** Authored 2026-05-15 by gandalf. Captures the embodiment-aware narrative skinning that *three* primary consuming surfaces require: **gear-slot names per doc 37 § 4 Position C**, **Court class-role labels per `court-of-forms.md` C8**, and (added 2026-05-16) **energy-type names per the three-tier system landed by rocket's B6 pre-work**.

**Why it exists:** doc 37 locked Position C (slot-as-functional-mechanic + embodiment-as-narrative-skin) — mechanical sameness across embodiments, narrative variance. court-of-forms.md C8 locked the dual-label pattern for Court class-roles — universal function tag + embodiment-flavored name. Rocket's B6 pre-work (2026-05-16) established the energy_type three-tier balance system (mana / combo-focus / rage at tiers 50 / 58 / 65). All three surfaces need a canonical reference for *what humanoid vs slime vs swarm vs etc. CALL their gear / their roles / their parts / their energy-source.* Without that reference, the locks are pattern-only; with it, they're implementable.

**Pending:**
- knight-rider to draft a decisions-log entry capturing the embodiment-taxonomy lock and the dual-layer pattern (per ADR-002; cross-seam — affects rocket generation, star-lord LLM prompts, drax UI display, future Court implementation)
- knight-rider to draft a decisions-log entry capturing the energy_type three-tier system per rocket B6 pre-work (separate entry; mechanical-tier discrimination per energy_type is now load-bearing for balance, not just labeling)
- gandalf to author energy_type rename treatment as part of Stage 4 of the form-bias migration (per form-bias-cadence-strategy.md § 7.1; the Layer 2 narrative-skin values below are the rendering targets when the rename lands)

**Companion docs:**
- Doc 37 § 4 Position C — gear-slot embodiment-as-narrative-skin lock
- `court-of-forms.md` C8 — Court class-role dual-label pattern
- `cosmology-reincarnated.md` — Earth Self / Wheel / Spirit Guide cosmology that contextualizes embodiment as "what the Earth Self wears this week"
- `style-register.md` — HD-2D-pixel locked register; embodiment variance happens *within* the register (per § "Per-embodiment register awareness")
- `gandalf-design-lineage.md` Layer 5 — isekai studio precedents (Mushoku, Slime, Konosuba, Solo Leveling) that establish the genre's embodiment breadth

---

## What this doc is

This doc is the **canonical embodiment vocabulary reference.** It locks:

1. The **embodiment taxonomy** — the starter set of forms the project canonically supports, with explicit expansion protocol
2. The **dual-layer naming pattern** — universal mechanical surfaces × embodiment narrative skin, with per-season variation as a third layer when generated
3. **Worked examples** for well-developed embodiments at the three primary consuming surfaces (gear slots; Court class-roles; energy_type tier rendering)
4. **Generation guidance** for how rocket / star-lord produce per-form vocabulary at form-creation time
5. **Engine emit requirements** for surfacing the narrative-layer data through to demo consumption

It explicitly **does NOT** attempt to enumerate every possible (embodiment × surface) lookup. That would be both incomplete (the isekai genre admits more forms than any list can anticipate) and operationally wrong (some per-form variation is the right job for LLM generation at form-creation time, not for canonical pre-enumeration). The doc commits the **pattern + key examples**; generation fills in specifics per form.

---

## The canonical embodiment taxonomy

The project commits to a **starter set of 8 canonical embodiments** covering the isekai genre's most common patterns. Additional embodiments can be added via canonical amendment when generated forms surface them or when design needs them.

### Starter set

| Embodiment | Brief characterization | Isekai precedent |
|---|---|---|
| **Humanoid** | The genre default. Bipedal, two-armed, head-bearing. The project's pre-doc-37 implicit default. | Re:Zero (Subaru), Mushoku Tensei (Rudeus), most isekai protagonists |
| **Slime** | Amorphous, semi-fluid body. Pseudopods for manipulation. Core/nucleus as perceptual center. Mass-distribution flexible. | That Time I Got Reincarnated as a Slime (Rimuru), Re:Monster early forms |
| **Beast** | Bipedal-or-quadrupedal furred / scaled / feathered animal-form. Claws, fangs, tails common. The "kemonomimi" / cat-human / wolf-human / kitsune register. | Konosuba (various), Re:Zero (Felix the cat-spirit, Beatrice in fox-coded moments), Made in Abyss creatures |
| **Dragonling** | Small-to-medium dragon form. Scaled body, sometimes quadrupedal-with-wings, sometimes bipedal-with-tail. Breath-weapon capability common. | Slime franchise (various dragonkin), Re:Monster, Drifting Dragons |
| **Swarm** | Hive-mind. Multiple physical bodies operating as one consciousness. Distribution-pattern variable (clustered / dispersed). Specialized members (workers, scouts, fighters). | Solo Leveling (Beru the ant-king; antswarm), various lower-tier "monster reincarnation" isekai |
| **Construct** | Non-organic crafted body. Stone, crystal, metal, or wood. Often immobile-or-slow base; movement via internal mechanism or magic. Geomancer / Golem register. | Slime franchise (golems), various magical-construct subplots |
| **Spirit** | Non-corporeal or partially-corporeal. Mist, vapor, ghost-form. Defies clean anatomy. Spirit-of-place register. | Spirited Away spirits, various yokai-coded forms |
| **Plant** | Plant-bodied. Root-anchored or mobile. Vines, leaves, flowering structures as anatomy. The dryad / treefolk register. | Re:Monster (treefolk), various nature-spirit characters |

These eight cover ~85% of the genre's mainstream embodiment patterns per my survey. The remaining ~15% (mecha, undead, demon, vampire, merfolk, deity-form, etc.) are not excluded; they're deferred to canonical amendment when needed.

### Expansion protocol

When a generated form surfaces an embodiment not in the starter set:

1. The form generation pipeline emits a tentative embodiment tag (rocket dispatch territory; per future doc 37 § 4 embodiment-axis implementation work).
2. Gandalf is invoked to review the tentative tag — does it fit an existing embodiment with extension, or is it a new canonical embodiment?
3. If new: gandalf authors an amendment to this doc adding the embodiment with characterization + worked examples for the primary consuming surfaces.
4. If extension: gandalf adds notes to the existing embodiment's section.
5. Matt approves the amendment; knight-rider files decisions-log entry.

This is intentionally a senior-design call (per AGENTS.md gandalf authority). Embodiment taxonomy is load-bearing; ad-hoc expansion would drift.

---

## The dual-layer naming pattern (with optional third per-season layer)

Every embodiment-narrative-skinning surface follows this pattern:

| Layer | What it is | Stability | Owner |
|---|---|---|---|
| **Layer 1 — Universal mechanical** | Form-agnostic. What the engine carries; what cross-embodiment queries operate on. | Stable. Foundation-level. | Engine schema (rocket / star-lord) |
| **Layer 2 — Embodiment narrative skin** | Embodiment-aware. The "humanoid says chest-armor; slime says viscosity-layer" layer. | Stable per embodiment. Locked in this doc + expansion amendments. | gandalf (this doc) |
| **Layer 3 — Per-season variation** (optional) | Season-aware. The cosmology-flavored modulation of the Layer 2 name. | Generated at form-creation time per the season's cosmology. | star-lord LLM call (consumes this doc + cosmology + cipher per doc 37 § 6) |

**Worked example for the gear surface:**

| Layer | Slot reference |
|---|---|
| **L1 universal** | `gear_slot.defensive` |
| **L2 embodiment skin (slime)** | "viscosity layer" |
| **L3 per-season variant (Yomi slime)** | "shadow-viscosity layer" (modulated by the Yomi season's underworld cosmology) |

The engine carries the L1 tag. Display rendering (drax) selects L2 from this doc. Per-season generation (star-lord LLM call) optionally modulates L2 into L3 when the cosmological resonance warrants it.

**Most consumer use cases stop at L2.** L3 is an opt-in flavor enrichment, not a default. The base L2 names are *good enough* to ship without L3 modulation. L3 is for the per-season cosmological-resonance work that the cipher architecture (doc 37 § 6) makes possible — Yomi's pomegranate-themed Passage is the L3 instance for the naming-triad; Yomi's shadow-viscosity-layer slime gear is the L3 instance for embodiment.

---

## Primary consuming surface 1 — Gear-slot embodiment narrative

Per doc 37 § 4 Position C, the 10 final gear slots (file 33) have **identical mechanical contribution** across all embodiments. The narrative skin varies. Worked-example tables for the well-developed starter embodiments below; defer LLM-generation-time naming for less-developed embodiments and per-season L3 variants.

### The 10 gear slots, Layer 2 by embodiment

| Slot (L1 universal) | Humanoid (L2) | Slime (L2) | Beast (L2) | Dragonling (L2) | Swarm (L2) |
|---|---|---|---|---|---|
| Main hand weapon | weapon (sword/staff/etc.) | primary tendril / projecting-form | claw / fang-mantle | claw / breath-stance | primary swarm-cluster |
| Off-hand | shield / off-hand / orb / focus / grimoire | secondary tendril | off-claw / second-paw | wing-grip / off-claw | secondary swarm-cluster |
| Head | helm / hood / circlet | core / nucleus | headband / ear-band | crown-ridge / horn-cap | lead-individual / queen-presence |
| Chest | chest / robe / cuirass | viscosity layer | fur-mantle / chest-mantle | scale-mantle / chest-plates | carapace ratio / body-distribution |
| Hands (gloves) | gloves / gauntlets | manipulator nodules | paw-wraps / claw-bindings | talon-wraps | manipulator-individuals |
| Feet (boots) | boots | locomotor base | padded-footing | claw-shod / digit-shod | ground-runners |
| Belt | belt / sash | median band | tail-wrap / loin-mantle | belt-of-scales / waist-band | central-band-density |
| Ring 1 | ring | embedded inclusion 1 | talon-band 1 | claw-ring 1 | satellite-cluster 1 |
| Ring 2 | ring | embedded inclusion 2 | talon-band 2 | claw-ring 2 | satellite-cluster 2 |
| Amulet | amulet | nucleus-shard / core-pendant | neck-charm | breast-jewel | swarm-singular / core-individual |

### For the remaining starter embodiments

**Construct, Spirit, Plant** — names are LLM-generated at form creation time using this doc as guidance, until enough worked examples accumulate to commit canonical L2 values. Guidance for the generation:

- **Construct (stone / crystal / metal / wood):** slot names reference the construct's material substrate and crafted-form anatomy. Defensive slot → "armor plate" / "outer panel" / "mantle-plate." Head → "headstone" / "crown-core" / "apex-piece." Etc.
- **Spirit (mist / vapor / ghost):** slot names reference the spirit's incorporeality and presence-based existence. Defensive slot → "shroud" / "mantle-of-mist" / "ward-veil." Head → "wisp" / "crown-of-light" / "ghost-cap." Rings → "binding-tether" / "anchor-thread." The amulet often becomes the *most-corporeal* part — the "anchor-stone" or "core-ember."
- **Plant (dryad / treefolk):** slot names reference plant anatomy. Defensive slot → "bark-mantle" / "leaf-armor" / "thorn-veil." Head → "crown-of-leaves" / "blooming-crown." Hands → "thorn-grips" / "vine-bindings." Feet → "root-base" / "ground-anchors."

When 3-5 production seasons surface these embodiments, gandalf authors an amendment to this doc locking the canonical L2 values for them.

### Per-season L3 modulation (illustrative)

For a Yomi-season slime form:
- chest (slime L2 = viscosity layer) → L3 = *"shadow-viscosity layer"* (Yomi's underworld register modulates the base name)
- head (slime L2 = core) → L3 = *"underworld-core"* or *"abyssal-core"*

For a Cathedral-of-Bone-season beast form:
- chest (beast L2 = fur-mantle) → L3 = *"marrow-fur"* or *"ossuary-pelt"*

L3 is generated by the star-lord LLM call at form creation when cosmological resonance is desired. It is **not required;** unmodulated L2 ships fine.

---

## Primary consuming surface 2 — Court class-role labels

Per `court-of-forms.md` C8: each Court member carries a universal function tag (Layer 1) + embodiment-flavored class-name (Layer 2). Optional per-season modulation is Layer 3.

### The 7 universal function tags (Layer 1) — LOCKED

These are committed canonical. They are derived from the engine's existing archetype taxonomy + the mechanical-function-vocabulary common across loot-ARPGs.

| Function tag | What it names mechanically | Engine archetype mapping (existing) |
|---|---|---|
| **Front-Line** | Sustained close-range engagement; primary damage-soaker | physical_warrior, physical_grappler, brute |
| **Ranged** | Distance damage; non-magical or magical-archery; primary projectile | hunter, sniper |
| **Control** | Battlefield manipulation; status / debuff / positional control | controller variants, some caster variants |
| **Sustain** | Regenerative; defensive-augmenter; survivability-focused | some hybrid_mage, sustain-archetype emergent |
| **Burst** | High-magnitude spike damage; spender-cycle; risk/reward | rogue, fire_mage at burst-focus, some hybrid |
| **Mobility** | Repositioning specialist; kiting; in-and-out engagement | physical_skirmisher, mobility-archetype emergent |
| **Specialist** | Niche-function; doesn't fit the above; novel-archetype emergent | hybrid_mage variants, novel emergent archetypes |

*[hybrid_mage RETIRED 2026-05-18 per canonical-6 transition; references to hybrid_mage in the Sustain and Specialist rows above are historical record. Post-canonical-6, the Specialist row maps to novel emergent archetypes only; the Sustain row's hybrid_mage mapping no longer applies. The seven function-tag system remains valid for the canonical-6 roster; controller + caster variants now anchor Control and Specialist respectively. See `canonical/story/canonical-6-transition-retire-hybrid-mage-2026-05-18.md` for context.]*

Mapping notes:
- Most existing player-class archetypes map cleanly to one function tag.
- "Hybrid_mage" can land in multiple tags depending on which side of the hybrid dominates; the engine emits the most-fitting tag at convergence time per the archetype-emergence work (file 28 § B13 emergence observability). *[hybrid_mage RETIRED 2026-05-18 per canonical-6 transition; this note is historical record.]*
- The seven tags are sized to give the Court a recognizable hierarchy without flattening too many archetypes into one bucket. Solo Leveling's Shadow Army has comparable role-grouping (~5-7 roles; commanders/knights/scouts/soldiers/specialists).

### The 7 × embodiment Layer 2 lookup

| Function (L1) | Humanoid (L2) | Slime (L2) | Beast (L2) | Dragonling (L2) | Swarm (L2) | Construct (L2) | Spirit (L2) | Plant (L2) |
|---|---|---|---|---|---|---|---|---|
| **Front-Line** | Knight | Bulwark / Coagulant | Stalker / Vanguard | Warden / Wyrm-guard | Phalanx | Resonance-pillar / Bulwark-construct | Guardian-shade | Bark-warden |
| **Ranged** | Archer | Spit-form / Lash | Hunter / Bowstance | Breath-singer | Dart-cluster | Sentinel-bolt | Wisp-caster | Thorn-flinger |
| **Control** | Sage / Priest | Suspending-form | Charm-singer / Snare-walker | Throat-binder | Hive-binder | Resonance-binder | Veil-weaver | Root-weaver |
| **Sustain** | Cleric / Healer | Replenishing-form | Pack-tender | Brood-tender | Hive-tender | Resonance-restorer | Veil-keeper | Bloom-tender |
| **Burst** | Berserker / Striker | Surge-form | Rending-stalker | Flame-stoker | Swarm-strike | Resonance-burst | Voidstrike-shade | Thornlash |
| **Mobility** | Rider / Skirmisher | Flowing-form | Pouncer / Strider | Wingstride | Scatter-cluster | (constructs often lack mobility — LLM-generation territory) | Drift-shade | Ambulant-vine |
| **Specialist** | (varies; LLM-generated per emergent archetype) | (varies) | (varies) | (varies) | (varies) | (varies) | (varies) | (varies) |

### Per-season L3 modulation for Court class-roles

For a Yomi-season humanoid Knight (Front-Line):
- L2 = "Knight"
- L3 = *"Threshold-Knight"* or *"Yomi-Knight"*

For a Deep-Trench slime Bulwark (Front-Line):
- L2 = "Bulwark"
- L3 = *"Trench-Bulwark"* or *"Pitch-Coagulant"*

These are generated at ascension time by the star-lord LLM call, using this doc + the cosmology + the seasonal vocabulary as prompt context.

---

## Primary consuming surface 3 — Energy-type narrative skin

**Added 2026-05-16** per rocket's B6 pre-work landing the three-tier energy_type balance system. This surface differs from the other two primary surfaces in one important way: **the underlying mechanic is tier-discriminated, not slot-discriminated.** Each energy_type carries a distinct `skill_power_tier` (and therefore a distinct magnitude-ratio); the per-embodiment narrative skin renders the *experiential identity* of that tier without disturbing the mechanical assignment.

### Background — what rocket's B6 pre-work established

Per the form-bias-cadence-strategy doc § 5 sub-lock (a) (ARPG-canon-primary at substrate-mechanical layer) and the engineering-disciplines refactor-not-rewrite + math-before-code pattern, rocket's B6 pre-work landed a three-tier energy_type-to-power-tier mapping that addresses the structural DPS-per-modifier disadvantage previously observed for physical rage classes:

| Tier name | energy_type values | `skill_power_tier` | Magnitude ratio (vs mana baseline) | Archetype examples |
|---|---|---|---|---|
| **Baseline** | `mana` | 50 | 1.00× | fire/water/earth/wind mage, caster, controller, hybrid_mage *[RETIRED 2026-05-18]* |
| **Partial** | `combo`, `focus` | 58 | 1.35× (58² / 50²) | hunter, rogue, physical_skirmisher |
| **Full** | `rage` | 65 | 1.69× (65² / 50²) | physical_warrior, physical_grappler |
| **Outlier** | (any) | 50 | 1.00× | experimental (intentional baseline; does not participate in tier shift) |

The three-tier refinement (vs a simpler binary mana-vs-physical shift) reflects rocket's empirical observation that hunter's avg modifier 0.594 sits closest to the [0.5, 1.0] target band already; pushing combo/focus archetypes through full 1.69× would overshoot before B14.5 V2 lands. Combo/focus gets partial; rage/melee gets full; mana stays baseline. Math verified (58²/50² = 1.346; observed smoke ratio 1.355 within RNG noise); 104 tests pass.

**This makes `energy_type` load-bearing for balance, not just for labeling.** Where the pre-LLM-substrate-inventory placed `energy_type` in Cluster B (form-agnostic-but-named-humanoid; rage/stamina-as-resource specifically called out), the cluster-B treatment options (hide / rename / keep) must now preserve the tier-discriminator role. **Any Stage-4 rename to embodiment-neutral vocabulary must map onto the three-tier structure cleanly.** That mapping is what this section commits.

### One conceptual clarification — `hybrid_mage` placement

*[hybrid_mage RETIRED 2026-05-18 per canonical-6 transition; hybrid_mage no longer exists in the canonical roster. The naming-discipline note below is retained as a standing discipline for any future archetype with "hybrid" in its name. See `canonical/story/canonical-6-transition-retire-hybrid-mage-2026-05-18.md` for context.]*

`hybrid_mage` (when it existed) landed in the baseline (mana) tier. "Hybrid" in class-name refers to **element-mixing** (a class drawing from multiple element pools), not **energy-type-mixing**. There is no "hybrid energy_type"; energy_type is single-valued per class. **This naming discipline remains active:** a future "hybrid_warrior" class (if generated) would still be tier=65 by energy_type; its hybrid-ness would be at the element layer, not the energy layer. Star-lord and rocket dispatches authoring class-template prompts should reflect this.

### The energy_type three-tier per-embodiment narrative skin

Each energy_type is a *thing that gets spent* to power effects, with characteristic accumulation/release semantics:

- **Mana** — ambient resource that powers effects; passive accumulation; cost-spent
- **Combo / Focus** — action-built resource; accumulates via specific engagements; released as combination-effects
- **Rage** — emotional/state resource; builds under pressure or in combat; releases as bursts

The Layer 2 narrative skin preserves these accumulation/release semantics per embodiment, while changing the *vocabulary* of what carries the resource:

| Energy tier (L1 universal) | Humanoid (L2) | Slime (L2) | Beast (L2) | Dragonling (L2) | Swarm (L2) | Construct (L2) | Spirit (L2) | Plant (L2) |
|---|---|---|---|---|---|---|---|---|
| **Mana (baseline)** | mana | viscosity-charge | spirit-pool | aether-reserve | hive-charge | resonance-charge | presence-charge | sap-charge |
| **Combo / Focus (partial)** | combo / focus | pressure-state | stalk-momentum | hunt-flux | formation-charge | alignment-charge | coalescence-state | bloom-tension |
| **Rage (full)** | rage / fury | surge-state | blood-fury | dragon-heat | kill-frenzy | overcharge | wrath-coalescence | thornlash-bloom |

**The mechanic is identical across rows; the rendering varies.** A slime in the rage tier has surge-state; a humanoid in the rage tier has rage; both have `skill_power_tier=65` and `energy_type=rage` at the engine level. The L2 rendering is what reaches the player.

### Per-tier conceptual notes (load-bearing for L3 modulation later)

These notes capture *why* each tier renders the way it does, so per-season L3 modulation can preserve the semantics:

- **Mana tier** is *passive-resource semantics*. The resource exists in some quantity, gets spent, regenerates over time. Per-embodiment renderings emphasize the *substance* that holds the charge — viscosity (slime), spirit (beast), aether (dragonling), hive (swarm), resonance (construct), presence (spirit), sap (plant).
- **Combo/Focus tier** is *active-build semantics*. The resource doesn't exist passively; it accumulates through specific engagement patterns and gets released as combinations. Per-embodiment renderings emphasize *what action builds it* — pressure (slime building internal pressure), stalking (beast tracking prey), hunting (dragonling on hunt), formation (swarm coordinating), alignment (construct attuning), coalescence (spirit gathering corporeality), blooming (plant tensioning for release).
- **Rage tier** is *state-escalation semantics*. The resource is an emotional/internal-pressure state that escalates under conditions and releases as bursts. Per-embodiment renderings emphasize the *escalation register* — fury (humanoid), surge (slime building volatile charge), blood-fury (beast hunting-rage), dragon-heat (dragonling's elemental rage), kill-frenzy (swarm in killing momentum), overcharge (construct exceeding safe operation), wrath-coalescence (spirit gathering hostile intent), thornlash-bloom (plant releasing thorned bursts).

### Per-season L3 modulation (illustrative)

For a Yomi-season humanoid rage class:
- L2 = "rage"
- L3 = *"underworld-fury"* or *"shade-wrath"*

For a Deep-Trench slime mana class:
- L2 = "viscosity-charge"
- L3 = *"trench-pressure-charge"* or *"pitch-substance-charge"* (modulated by the deep-trench cosmology's pressure-coded substrate)

For a Music-Spirit dragonling combo/focus class:
- L2 = "hunt-flux"
- L3 = *"melody-flux"* or *"rhythm-tension"* (modulated by the music-spirit cosmology)

L3 is generated by the star-lord LLM call at form creation when cosmological resonance is desired. The base L2 rendering ships fine without modulation.

### Stage 4 rename context (per form-bias-cadence-strategy.md § 7.1)

The energy_type field-name and L1 universal labels (`mana` / `combo` / `focus` / `rage`) currently sit in Cluster B (form-agnostic-but-named-humanoid) per the pre-LLM-substrate-inventory. The form-bias migration's Stage 4 may rename these to embodiment-neutral L1 labels. The Layer 2 rendering above is the **per-embodiment target vocabulary** the rename should preserve; the rename's mechanical contribution is **identical to current** because rocket's B6 pre-work already established the tier discriminator.

In other words: Stage 4's rename is *labeling-only work*, not mechanical-refactor work. The mechanical contribution (50/58/65 tiers) survives intact; the L1 labels and the L2 renderings either ship as-is (if the rename keeps current labels) or get a per-embodiment skin applied (if the rename adopts embodiment-neutral L1 labels).

### Generation guidance for energy_type narrative skin

- **Rocket** (form generation): emit `energy_type` per current schema; emit `embodiment_tag`; the L2 rendering is a lookup from this doc using both fields as the key. Implementation choice: rocket emits the L2 string directly, OR rocket emits the tags and demo does the lookup. Recommend the latter for flexibility (display-side rendering can be updated without engine regen).
- **Star-lord** (LLM prompt construction): when LLM prompts generate flavor text that references a class's energy source, look up the L2 rendering and pass it as embodiment-aware vocabulary. For per-season L3 modulation, pass the season's cosmology + L2 base + ask the LLM for cosmological resonance.
- **Drax** (demo / loadout UI): render the L2 vocabulary at player-facing surfaces. Class-sheet "Energy Source" field shows L2 (e.g., "viscosity-charge" for slime mage), not L1 (`mana`). Tooltips can show L1 for technical detail but L2 is the headline.

### What this protects against (energy_type-specific)

- **Humanoid-default leakage at the energy-source layer.** Without this section, LLM-generated content would render every class's energy as "mana" or "fury" by training-default, even for slime / construct / spirit embodiments where those words don't fit. With it, embodiment-aware energy vocabulary is the canonical reference.
- **Stage 4 rename mechanical-drift.** The rename's risk is breaking the 50/58/65 tier mapping. With L2 vocabulary committed per embodiment, the rename has explicit rendering targets that preserve the tier discriminator role.
- **`hybrid_mage` energy-tier ambiguity (naming discipline, retained post-retire).** Without explicit clarification, "hybrid" in class names could be read as "hybrid energy type." This section locks "hybrid = element-mixing only" so future class generation doesn't drift toward "hybrid_warrior_in_rage-mana-tier-50" or similar incoherence. *[hybrid_mage RETIRED 2026-05-18 per canonical-6 transition; the naming discipline described here is retained for any future archetype with "hybrid" in its name, even though hybrid_mage itself no longer exists in the canonical roster.]*

---

## Secondary consuming surfaces (named; not yet exhaustively locked)

The embodiment narrative layer extends beyond gear and class-roles. Other surfaces this doc names but does not yet exhaustively enumerate:

### Body-part vocabulary

For combat hit descriptions, equipment-fit descriptions, injury narration. Examples:

- Humanoid: arm / leg / head / chest / hand / foot
- Slime: tendril / nucleus / mass / pseudopod / inclusion
- Beast: paw / fang / tail / pelt / ear
- Dragonling: scale / wing / talon / breath-throat / tail-spine
- Swarm: cluster / lead-individual / satellite / queen-presence / runner
- Construct: panel / joint / core / shell / facet
- Spirit: tendril / wisp / coalescence / veil / anchor
- Plant: branch / root / bloom / leaf / stem

When LLM-generated combat text references body parts, it uses the embodiment-aware vocabulary. The engine emits the embodiment tag with the entity; the LLM consumes the tag + this lookup.

### Action verbs

For skill descriptions, combat narration, story moments. Examples:

- Humanoid: strikes / casts / steps / parries / sings
- Slime: surges / lashes / coalesces / divides / engulfs
- Beast: pounces / rends / stalks / cries / leaps
- Dragonling: claws / breathes / wings / lashes / coils
- Swarm: swarms / engulfs / disperses / clusters / overwhelms
- Construct: strikes / activates / shifts / grinds / rotates
- Spirit: flows / passes-through / coalesces / fades / haunts
- Plant: lashes / roots / blooms / withers / entwines

LLM-generated skill flavor text consumes embodiment-specific action verbs. A slime's primary attack reads as *"surges forward and engulfs"* not *"strikes."*

### Injury / death vocabulary

For combat outcomes, story moments, Passage / Trial moments. Examples:

- Humanoid: bleeds / falls / collapses / dies / breaks
- Slime: dissipates / scatters / loses-cohesion / unmakes / dissolves
- Beast: bleeds / falls / cries / collapses / dies (close to humanoid for organic embodiments)
- Dragonling: bleeds / falls / cries / scales-crack / dies
- Swarm: scatters / depletes / loses-the-queen / disperses / collapses
- Construct: cracks / shatters / loses-coherence / falls-apart / breaks
- Spirit: fades / unbinds / dissipates / returns-to-mist / unmoors
- Plant: withers / breaks / dries / falls / decomposes

This vocabulary is particularly load-bearing for the **Passage** moment — the dying form's collapse description varies meaningfully per embodiment, and the Wheel's offer is more powerful when the death-language is form-specific.

### Communication / speech vocabulary

For Spirit Guide dialogue, NPC interaction, Court member voice presence. Examples:

- Humanoid: speaks / whispers / shouts / laughs / cries
- Slime: pulses / resonates / vibrates / hums / ripples (slime communication via vibration)
- Beast: speaks (if anthropomorphic) / growls / cries / purrs / yowls
- Dragonling: speaks / roars / hisses / sings (Dragon-singer trope) / chuffs
- Swarm: chitters / clicks / hums (collective vocalization)
- Construct: resonates / rings / chimes / vibrates / sounds
- Spirit: whispers / sings / fades-into-words / echoes / chimes
- Plant: rustles / creaks / sighs / blossoms-into-words / hums

Voiced Court members (per court-of-forms.md C4) use embodiment-appropriate speech registers. A slime Court-member's brief dialogue presence might *pulse a low resonance into the chamber* before speaking; a swarm Court-member might *chitter in chorus*.

---

## Generation guidance

### For rocket (form generation)

When the engine generates a form for a season, it should emit:

- `embodiment_tag` — string; one of the canonical taxonomy values (humanoid / slime / beast / dragonling / swarm / construct / spirit / plant) or a tentative tag if a novel embodiment surfaces (triggers expansion protocol)
- `embodiment_anatomy_tags` — array; the body-part vocabulary tags for this form (consumed by combat-text generation)
- `embodiment_action_register` — string; the action-verb register tag

Most of this is derivable from the embodiment tag itself + this doc's lookup tables; the engine emits the *tag*, and downstream consumers (LLM calls, demo rendering) look up the vocabulary from this doc.

### For star-lord (LLM prompt construction)

When LLM prompts generate flavor text that references a form:

- Include the form's `embodiment_tag` in the prompt context.
- Reference this doc's vocabulary tables as prompt guidance.
- For per-season L3 modulation: pass the season's cosmological vocabulary (per doc 37 § 6 cipher) alongside the embodiment tag; ask the LLM to find resonance where it lands naturally.
- Anti-bias scaffolding (Discipline #14 candidate): do not expose canonical-four element labels or humanoid-default action verbs as defaults; the LLM should be working from embodiment-aware vocabulary.

Per-form L3 generation can land in the same LLM call as the season's elemental vocabulary generation (per naming-triad.md § "Generation integration with the cipher architecture"). Bundle the cosmological-vocabulary work into one coherent per-season call.

### For drax (demo rendering / UI)

When displaying gear slot names, class-role labels, or other embodiment-narrative content:

- Read the form's `embodiment_tag` from the engine output.
- Look up the appropriate L2 value from this doc.
- If a generated L3 value is available for the season, prefer it for in-season display; fall back to L2 otherwise.
- Universal frame (L1) language is for technical/operational contexts only; player-facing UI uses L2 or L3.

---

## Engine emit requirements

Beyond the existing per-form fields, the engine must emit:

- `embodiment_tag` — string per the canonical taxonomy
- `embodiment_anatomy_tags` — array of body-part references for this form
- `embodiment_action_register` — string tag for action-verb register
- `class_role_function` — one of the 7 universal function tags (per Layer 1 above; consumed by Court labeling at ascension)
- `gear_slot_labels` — per-form lookup output (engine reads this doc's table for the form's embodiment and emits the L2 values directly OR emits the embodiment tag and lets demo do the lookup; implementation choice)
- `energy_type` (existing field; now also load-bearing for L2 rendering) — used jointly with `embodiment_tag` to look up the energy-source L2 rendering from Primary consuming surface 3. `skill_power_tier` (existing field; landed by rocket B6 pre-work) is the mechanical contribution and does not need a separate rendering — it's an internal-tier indicator that the L2 rendering communicates experientially.
- For seasons that opt into L3 generation: a `per_season_narrative_modulation` field with the season-modulated names alongside the L2 defaults

The implementation is largely **explicit emission for consumer use,** similar to enemy-visual-legibility.md's pattern.

---

## Open questions

These do not block the canonical lock. They surface during implementation.

### Q1 — L3 modulation cost / trigger

Generating per-season L3 modulations for every form × surface combination is operationally expensive (many LLM calls per season). Options:

- **Always generate** L3 for all surfaces — most expressive; highest LLM cost
- **Selective generation** — L3 only for high-narrative-weight surfaces (Court class-role; perhaps gear chest slot; defer the rest)
- **No L3 by default** — ship L2 base names; L3 reserved for special cases (the player's ascended form gets L3 Court label; trial-boss encounters get L3 gear labels)

My recommendation: **selective generation.** L3 lands for the player's currently-played form's gear (when entering inventory) and for Court members at ascension. Other forms (random monsters; brief encounters) stay at L2. Cost is bounded; narrative weight lands where it matters most.

### Q2 — Hybrid / chimeric embodiments

What if a form is genuinely hybrid — a beast-construct, a slime-spirit, a dragonling-swarm? The current taxonomy admits one embodiment per form. Hybrid forms exist in the isekai genre (Slime franchise's Beretta — a slime that constructs an armor body around itself; Re:Monster's various hybrid evolutions).

Options:
- **Force single-tag** — generation picks the dominant embodiment; hybrid is collapsed
- **Allow dual-tag** — `embodiment_tag_primary` + `embodiment_tag_secondary` with weight; vocabulary blends from both
- **Composite embodiments as taxonomy expansion** — add specific composite embodiments via amendment when needed

My recommendation: **start with single-tag; expand if generation produces hybrids that don't fit.** Don't pre-build complexity that may not be needed.

### Q3 — Body-part overlap between embodiments

Some body-part vocabulary overlaps (humanoid and beast both have "head," "chest," "hand"). Some doesn't (slime's "core" doesn't match construct's "panel"). Open: when LLM-generated text references body parts, does it use the embodiment's preferred vocabulary even when humanoid-default would also fit? My instinct: yes, always use embodiment-specific. The body-part vocabulary signals which embodiment is being narrated; default-humanoid leaks the bias the form-bias work was meant to remove.

### Q4 — Movement / locomotion vocabulary

The body-part and action-verb sections name movement vocabulary implicitly (humanoid steps, slime surges, beast pounces). Open: does this deserve its own dedicated section/table? Probably yes when the demo's combat-narration / quest-narration work matures. Parked for a future amendment.

### Q5 — Voice-over / audio register per embodiment

Far-future: if the project ever ships voiced content (Spirit Guide dialogue, Court member voice), the audio register per embodiment matters (slime "pulse" is not the same as a beast "growl"). Out of scope for this doc; surfaces when audio work begins.

---

## What this protects against

- **Humanoid-default leakage at the narrative layer.** Without this doc, LLM-generated content would reach for humanoid vocabulary by training-default. With it, embodiment-aware vocabulary is the canonical reference; humanoid is one embodiment among eight.
- **Gear-slot rename drift.** Doc 37 § 4 Position C committed embodiment-as-narrative-skin; this doc gives the lookup that makes that implementable. Without it, the rename stays pattern-only.
- **Court class-role label drift.** court-of-forms.md C8 committed the dual-label pattern; this doc finalizes the 7 universal tags AND gives the per-embodiment lookup.
- **LLM-generated combat / quest / dialogue content reaching for "the warrior strikes" / "her chest is wounded" / "his hand grasps" defaults.** With this doc, the LLM consumes embodiment-aware vocabulary from a canonical reference.
- **Ad-hoc embodiment expansion.** New embodiments enter via the expansion protocol; not via individual LLM-call invention that drifts the taxonomy silently.

This is the Discipline #13 application at the embodiment-narrative-vocabulary layer. Name the pillar; lock the canonical reference; protect against silent drift.

---

## Cross-references

- Doc 37 § 4 (Position C — gear-slot mechanic + embodiment-narrative split) — the architectural lock this doc operationalizes
- Doc 37 § 6 (cipher architecture — per-season vocabulary) — the L3 modulation source
- `court-of-forms.md` C8 (dual-label pattern for Court class-roles) — the second primary consuming surface
- `form-bias-cadence-strategy.md` § 5 sub-lock (a) + § 6.4 Cluster B treatment + § 7.1 Stage 4 — the strategic framing within which the energy_type narrative-skin work is the rendering target for the future Stage-4 rename
- `cosmology-reincarnated.md` — the cosmological framing within which embodiment-narrative content is rendered
- `style-register.md` — the visual register within which all embodiment work happens
- `naming-triad.md` — the parallel cipher-integration pattern for encounter-moment naming
- `enemy-visual-legibility.md` § "Per-embodiment register awareness" — the visual side of embodiment work
- `gandalf-design-lineage.md` Layer 5 — isekai genre embodiment precedents
- File 17 + file 33 (10 gear slot list) — the universal mechanical reference for gear surface
- File 28 § B13 (archetype-emergence observability) — surfaces the data for class-role function tags
- Rocket B6 pre-work (2026-05-16; commit reference per knight-rider dispatch log) — established the three-tier energy_type-to-`skill_power_tier` mapping (50 / 58 / 65) that Primary consuming surface 3 renders

---

## Maintenance protocol

When implementation work consumes this doc:

1. **Rocket dispatch (embodiment-axis schema work):** add `embodiment_tag` and adjacent fields per § "Engine emit requirements." MIGRATION.md required.
2. **Star-lord dispatch (LLM prompt construction):** integrate embodiment-vocabulary lookup into prompt templates; integrate L3 generation into per-season cosmological-vocabulary call.
3. **Drax dispatch (UI display + combat text):** consume embodiment tags; look up vocabulary; render embodiment-aware labels. Energy-source field in class-sheet UI renders L2 (Primary surface 3).
4. **Gandalf (expansion amendments):** when new embodiments surface from generation, author amendments adding canonical L2 vocabulary. When energy_type rename lands at Stage 4 of the form-bias migration, author amendment updating Primary surface 3's L1 labels accordingly (L2 rendering values stay; L1 universal labels may change).

When future canonical design docs reference embodiments:

1. Reference this doc.
2. Use canonical embodiment taxonomy values; do not invent parallel embodiment tags.
3. For surfaces this doc names but doesn't enumerate (body parts, action verbs, etc.), generate per the guidance; submit notable additions back as amendments.

When new generated forms surface novel embodiments:

1. Trigger the expansion protocol (per § "Expansion protocol").
2. Do not let the form ship with an ad-hoc embodiment label that's not in this doc's taxonomy.
3. Senior-design review by gandalf is required.

— gandalf, with Matt's standing approval on the locks consumed (doc 37 Position C; court-of-forms.md C8; this doc's taxonomy itself 2026-05-15; Primary consuming surface 3 amendment 2026-05-16 per rocket B6 pre-work + Matt's same-day approval to author)
