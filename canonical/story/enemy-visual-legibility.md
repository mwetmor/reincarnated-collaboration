# Enemy Visual Legibility — Player-Perception Architecture

**Status:** **Canonical.** Authored 2026-05-15 by gandalf on Matt's commission after family-playtest finding surfaced. Cross-seam architectural reference for engine generation (rocket), demo rendering (drax), LLM image generation (star-lord), and design-coherence enforcement.

**Triggered by:** demo1 family-playtest finding (Matt, 2026-05-15) — *enemies looked the same as player combatants, made larger.* This is a load-bearing player-experience failure; the design rejects it as canonical anti-pattern. This doc names the failure, locks the corrective architecture, and assigns the cross-seam responsibilities.

**Companion docs:**
- `style-register.md` — the visual idiom this doc operates within (HD-2D pixel hand-drawn, proposed)
- `cosmology-reincarnated.md` — the Mirror-fight visual identity-grammar exception
- `court-of-forms.md` — Trial encounter ritual that triggers cinematic-tier enemy presentation
- `gandalf-design-lineage.md` Layer 2 — Diablo / PoE enemy-legibility shipped standards

**Pending:**
- knight-rider to draft a decisions-log entry capturing the canonical anti-pattern rejection (per ADR-002; cross-seam by nature)
- rocket dispatch for engine-emit fields (after Matt approval)
- drax dispatch for demo-side rendering architecture (after Matt approval)
- Forthcoming `trial-moment-ritual.md` (Phase 2 work queue #5) will consume this doc's `is_trial_encounter` flag for the Trial cinematic-frame ritual

---

## What this doc is

This doc is **player-perception architecture for enemies.** It is structurally adjacent to but distinct from the style-register decision. Style-register answers *"what visual idiom is the project rendered in."* This doc answers *"given that idiom, how does the player perceive who they are fighting at the 200ms recognition target ARPG combat demands."*

The 200ms target is empirical. ARPG combat involves rapid threat-assessment-and-response cycles. At any moment a player sees 1-12 enemies on screen, must classify each by threat-tier and engagement-strategy, and must commit to action within the genre's signature reaction window. **Enemies the player cannot classify at 200ms degrade combat into noise.** This is not opinion; it is the design constraint every successful loot-ARPG has converged on.

---

## The anti-pattern explicitly named

**Anti-pattern:** Enemies rendered as scaled-up player-class sprites with no further visual differentiation.

**Where observed:** demo1 family-playtest (2026-05-15 Matt finding). Trial bosses, who are mechanically generated as player classes per the engine's bestiary architecture, were rendered using the same sprite tooling as the playable classes — *larger, but visually identical in archetype, palette, and silhouette.* The player could not visually distinguish "this is a Trial boss" from "this is a scaled-up version of my own class" without reading the encounter banner.

**Why it fails:**
- Defeats the genre's at-a-glance threat-assessment expectation
- Conflates trial-boss-as-narrative-culmination with trial-boss-as-numerically-tuned-player (the engine generates trial bosses as player-class converged-against-the-player, but that mechanical fact must not surface visually)
- Specifically breaks the Mirror Trial vs Body-swap Trial visual distinction (if every Trial visually reads as a mirror, the body-swap-path's narrative weight is undercut)
- Compounds with the form-bias work (doc 37) — humanoid player class scaled up looks more like *another humanoid player class*, not like *the seasonal cosmology's culminating opponent*

**The canonical rejection:** Any future dispatch proposing "reuse player sprites for enemies with scale variance" is **rejected at Gate 1**. This is a Discipline #13 application — a load-bearing player-perception pillar that is now structurally enforced by being named, locked, and referenced.

---

## What the player must perceive at 200ms

Six perceptual axes the player must classify on encounter. Each requires a visual signal.

| Axis | Question the player is answering | Primary signal | Secondary signal |
|---|---|---|---|
| **Tier** | How threatening? | Silhouette complexity + aura presence | Size (supplemental, not primary) |
| **Element** | What strategy / resistance? | Primary palette coloring | Element-coded aura/VFX |
| **Archetype** | How does it fight? | Sprite shape and silhouette | Animation idiom |
| **Trial-encounter** | Is this the act's culmination? | Cinematic frame on encounter | Distinct silhouette + tier banner |
| **Mirror-of-me** | Is this my reflection? | Same-palette mirrored animation | Recognition-coded visual cues (see § Mirror exception) |
| **Pack-vs-individual** | Swarm or discrete? | Density at spawn + per-unit simplicity | Per-pack name banner / unified aura |

The signals stack. A swarm of fire-coded swarmers looks distinct from a trash fire-mage, which looks distinct from an elite fire-mage, which looks distinct from a Trial fire-boss — *each tier reveals more visual information,* and the player can read the stack at-a-glance.

---

## Structural commitments

### S1 — Sprite-archetype registry, NOT sprite-from-player-pool

Enemy sprites come from a **separate registry of monster sprites,** mapped per `sprite_archetype_tag`. The registry is populated from the asset catalogue (Legolas Mode B work) sourced from itch.io vendors (Elthen, LuizMelo, ansimuz, pimen monster extensions, etc.). Per the catalogue research, this is well-covered at the locked HD-2D-pixel register.

The engine's six monster archetypes (brute / caster / controller / sniper / swarmer / tank) map to ~6 base sprite archetypes; per-season variation comes via *palette and decoration overlays*, not via per-season bespoke sprite assets. Initial registry sizing: **6-12 base monster sprite archetypes** covering the taxonomy; expanded per playtest feedback. **Not 18+** — operational cost of bespoke-per-season would exceed family-pace budget.

Player-class sprites and monster sprites are **drawn from separate asset pools.** The demo's rendering logic does not fall back to player-class sprites for monsters under any condition. If a monster archetype lacks a registered sprite, the rendering logic emits an error rather than degrading to player-sprite reuse.

### S2 — Element palette-shift as primary element signal

Element is communicated visually through **primary palette coloring of the sprite,** applied at runtime via Pixi.js tint or filter pass. Element palettes are canonical per element:

- **Fire / fire-flavored** — warm reds, oranges, deep ambers
- **Water / water-flavored** — blues, teals, deep marines
- **Earth / earth-flavored** — browns, ochres, stone-greys, mineral greens
- **Wind / wind-flavored** — pale blues, whites, dusty pales, atmospheric tints
- **Physical** — neutral browns / greys / iron-tints (the seasonal sub-flavoring matters less here)
- **Hybrid** — palette-blend per the hybrid's element pair
- **Per-season vocabulary variants** — palette modulations on the canonical element they cipher to (per doc 37 § 6; "pressure" inherits Earth palette with a darker/heavier shift; "vacuum" inherits Wind palette with a darker shift; etc.)

The engine emits `display_color_primary` and `display_color_secondary` per monster; the demo applies them as tint operations on the base sprite. Per-monster recoloring is operationally cheap.

### S3 — Tier-coded aura class

Visible passive auras communicate tier at-a-glance. Aura assets are sourced from the locked-register catalogue (per Legolas research, aura coverage is Tier-2: solid coverage):

| Monster tier | Aura signal |
|---|---|
| **swarm** | None per-unit; instead a unified pack-cluster aura enveloping the pack |
| **magic** | Faint shimmer in element palette |
| **trash** | None (the baseline; tier is signaled by silhouette + name-banner) |
| **elite** | Visible aura, element-coded, single-color |
| **mini-boss** | Strong aura, element-coded, possibly two-color |
| **boss** | Signature aura, element-coded, often pulsing or animated |
| **act-boss / Trial encounter** | Cinematic-tier aura, screen-edge tint, distinctive shape |

The engine emits `display_aura_tier` per monster; the demo selects the catalogued aura asset.

### S4 — Trial encounter cinematic frame

When `is_trial_encounter` flag is set, the demo triggers the **Trial moment ritual** before combat begins (per forthcoming `trial-moment-ritual.md`). The Trial encounter is preceded by:

- A pause-the-game cinematic frame at narrative-moment-tier fidelity (per style-register.md § "Narrative-moment tier")
- The trial-boss's full LLM-generated name displayed at cinematic-banner scale
- The Spirit Guide leans in with one line of contextual voice
- The choice screen (Body-swap-path / Mirror-path) surfaces, per cosmology-reincarnated.md

The trial-boss sprite itself does **not** need to be bespoke per-season. The trial-boss reuses an appropriate archetype sprite from the registry, with a **trial-boss cloak overlay** — a distinctive aura + silhouette enhancement — applied. The cinematic frame, the cloak, and the cinematic aura together communicate "this is the act's culmination" without requiring per-season custom sprite art. Operationally feasible at family pace.

### S5 — Name-banner tier coding

Health bars / name banners are tier-coded:

| Tier | Name banner treatment |
|---|---|
| **swarm** | No per-unit name; pack name displayed once for the cluster |
| **magic** | Small element-coded text |
| **trash** | Standard text |
| **elite** | Colored text + tier icon |
| **mini-boss** | Colored text + tier icon + tier-flag |
| **boss** | Cinematic text + tier banner + element banding |
| **act-boss / Trial encounter** | Full cinematic name + tier banner + season-anchor flag |

The engine emits `display_name_banner_class`; the demo styles per class.

### S6 — Pack rendering for swarm tier

Swarm packs (5-12 units, per file 33 § "Tier structure") render with:

- **Per-unit simple silhouette** — players cannot parse 12 detailed sprites simultaneously; swarm units are visually simpler than trash
- **Unified pack-cluster aura** — a single aura envelops the cluster, color-coded to element, signaling pack composition
- **Single pack-level name banner** — not per-unit name; the pack has one name (the engine emits this via PackProxy entity per gamora B10.2 work)

Per PoE shipped pattern: rare-rarity packs share visualizations that read the pack as a unit.

### S7 — The Mirror-fight exception

When `is_mirror_encounter` flag is set (player chose Mirror-path at a Trial), the rendering rules **reverse.** The opponent renders using:

- The player's *current sprite asset* (not from the monster registry)
- The player's *current animations*
- The player's *current color palette*
- Recognition-coded subtle cues that signal *"this is you, not a copy"* (slight palette shift toward an ominous register; mirrored animations; voice lines that quote the player's recent build choices per cosmology-reincarnated.md § "The Mirror")

This is the canonical exception to S1's enemies-from-separate-pool rule. The exception is the design's narrative payoff — *"you see yourself, and you choose what stays."* Rendering distinction here would break the Mirror's core purpose.

The implementation: the engine sets `is_mirror_encounter=true` and the encounter's combatant config points to the player's current class; the demo's rendering logic consumes the flag and routes to player-sprite-rendering instead of monster-registry-rendering.

---

## What engine generation must emit

Per-monster, in addition to existing mechanical fields, the engine must emit:

- `sprite_archetype_tag` — string; visual creature-family tag mapping to the demo's sprite registry. Values include the six base archetypes (brute / caster / controller / sniper / swarmer / tank) plus future expansions as the catalogue grows.
- `display_color_primary` — RGB hex string; primary element palette color.
- `display_color_secondary` — RGB hex string; secondary tint for sprite shading / aura.
- `display_aura_tier` — enum: `none / faint / standard / visible / strong / signature / cinematic`. Maps to S3's tier-coded aura class.
- `display_silhouette_complexity` — enum: `simple / standard / detailed / distinct`. Maps to tier expectations.
- `display_name_banner_class` — enum: `none / small / standard / colored / colored-iconed / cinematic / cinematic-banner`. Maps to S5's name treatment.
- `is_trial_encounter` — boolean; flags trial-boss encounters for cinematic frame triggering (S4).
- `is_mirror_encounter` — boolean; flags Mirror-path Trial encounters for player-sprite-rendering exception (S7).

**Implementation note:** most of these fields are *derivable from existing engine data*, not new generation. The work is **explicit emission for demo consumption,** not new generation. Star-lord schema dispatch + rocket emit-surface dispatch territory. Estimated cost: small (~1-2 days per seam) given the derivability.

---

## What demo rendering must do

- **Maintain a sprite-archetype registry** keyed on `sprite_archetype_tag`. Asset sources: locked-style-register catalogue (HD-2D pixel hand-drawn). Initial registry: 6-12 base archetypes.
- **Apply element palette-shift** at runtime via Pixi.js tint / filter. Read `display_color_primary` and `display_color_secondary`; apply to the registry-selected sprite.
- **Apply aura VFX** from style-register-locked aura assets. Read `display_aura_tier`; select corresponding aura asset; render at appropriate scale.
- **Render name banner** styled per `display_name_banner_class`.
- **Trigger Trial moment ritual** on `is_trial_encounter`. Hand off to the Trial cinematic-frame routine (per forthcoming `trial-moment-ritual.md`).
- **Route to player-sprite rendering** on `is_mirror_encounter`. The Mirror's opponent renders using the player's current sprite/animations/palette assets, with the recognition-coded subtle cues per S7.
- **NEVER fall back to player-class sprites** for any non-Mirror enemy. If a monster archetype lacks a registered sprite, emit an error and log; do not degrade to player-sprite reuse.

---

## What this protects against

Specifically and explicitly:

1. **The demo1 finding** — enemies looking like scaled-up player classes. Locked rejected.
2. **Trial-boss-as-scaled-up-player** — trial bosses get cinematic encounter frames + cloak overlay + tier-banner; their visual treatment is unmistakable from any playable class.
3. **Element-blind enemy presentation** — every monster's element is visible via palette + aura.
4. **Tier-flattening** — every tier gets distinct visual signals (silhouette, aura, name-banner); the player can read threat at-a-glance.
5. **Swarm-vs-individual confusion** — swarm packs read as packs, not as N independent threats.
6. **Mirror-fight rendering drift** — the Mirror-path's visual exception is locked canonical; future work cannot accidentally render the Mirror as just-another-enemy.

This is the Discipline #13 application: name the failure, name the corrective architecture, name what's rejected. Future drift toward sprite reuse, tier flattening, or Mirror-rendering simplification is now structurally obstructed.

---

## Open questions

These do not block the canonical lock. They surface during implementation work.

### Q1 — Per-archetype animation idioms

Each sprite archetype's animation IDIOM is visually distinct from others. Brutes lunge and slam; casters cast with arms-extended idioms; controllers gesture-and-emit; snipers anchor-and-aim; swarmers cluster-and-rush; tanks plant-and-strike. Open: do these need to be explicitly specified per archetype, or do they emerge naturally from sprite-asset selection? My instinct: name them in a `monster-animation-grammar.md` follow-on doc when drax's enemy-rendering work begins; for now, asset selection from the catalogue covers most of the signal.

### Q2 — Per-season palette modulation specifics

Doc 37 § 6's cipher architecture means each season has its own vocabulary that ciphers to canonical-four elements internally. The palette signal in S2 needs to honor *both* the player-visible seasonal vocabulary AND the engine-internal cipher. *"Pressure"* in Yomi's wind-shift season palette-shifts wind's pale-blue/white range toward a heavier, more compressed signature; the player reads pressure-coded; the engine cipher-resolves to wind for resistance math. Open: per-season palette modulation tables — authored by whom (rocket via element-data generation? star-lord via LLM context? gandalf design intent into a per-season-flavor doc?)? Likely rocket-emit territory but coordinated with `season-feel-rubric.md` (work queue #10).

### Q3 — Sprite-archetype-tag taxonomy growth

The initial registry of 6-12 archetypes covers the engine's current taxonomy. As the engine generates more diverse monster archetypes (per doc 37 § 4 embodiment work — non-humanoid forms; per file 28 swarm-tier expansion), the registry will need new tags. Open: who authorizes registry growth — Drax based on catalogue availability? Rocket based on generation outputs? Matt approval each time? Probably: drax proposes, knight-rider sequences, Matt approves new entries. Not blocking initial implementation.

### Q4 — Boss-tier cinematic asset register

The boss/act-boss cinematic-aura tier is the most asset-cost-intensive. Each boss encounter wants a distinct cinematic signature. Options: (a) one signature per element (4 cinematic auras serving all seasonal bosses by element; lower cost, lower uniqueness), (b) one signature per season (3 cinematic auras per season — one per act-boss/Trial — generated per-season; higher cost, higher uniqueness), (c) one signature per generated boss (cinematic asset generated alongside the boss; highest cost, highest uniqueness). Recommendation: option (b) — per-season cinematic-aura set generated alongside seasonal vocabulary, three signatures per season honoring the act-end weight without per-boss bespoke. Decision deferred to implementation conversation.

### Q5 — Color-blindness accessibility

Element palettes per S2 use color heavily. Players with color-vision differences need alternative signals — possibly icon overlays on aura, shape variations, or pattern-coded aura signatures. Genre-standard accessibility settings. Open: what specifically; drax dispatch territory when accessibility pass occurs; should not block initial implementation but should be tracked as a known concern.

---

## Cross-seam dispatch implications

When implementation work begins on this doc, the dispatch sequence:

1. **Rocket dispatch** — add `sprite_archetype_tag`, `display_color_primary`, `display_color_secondary`, `display_aura_tier`, `display_silhouette_complexity`, `display_name_banner_class`, `is_trial_encounter`, `is_mirror_encounter` fields to monster schema and engine generation. Most are derivable; emission is the work. MIGRATION.md required (touches export contract).
2. **Star-lord dispatch** — schema validation at export boundary (Discipline #8); JSON export includes the new fields.
3. **Drax dispatch** — sprite-archetype registry; rendering logic consuming the new fields; Trial cinematic frame routine; Mirror-path player-sprite rendering routing; aura asset integration from style-register catalogue.
4. **Legolas commission** — Mode B catalogue crawl prioritizing monster-sprite vendors at the locked register (Elthen, LuizMelo, ansimuz monster extensions, pimen monster packs); per-archetype coverage; non-humanoid monster sprite coverage for doc 37 § 4 embodiment work.

Knight-rider coordinates the dispatch sequence. Jack-ryan reviews at Gate 1 each dispatch. This doc serves as the canonical reference all four dispatches inherit from.

---

## Cross-references

- `style-register.md` — the visual idiom (HD-2D pixel hand-drawn) within which enemy-legibility operates
- `cosmology-reincarnated.md` § "The Mirror" — the Mirror-fight exception's narrative source
- `cosmology-reincarnated.md` § "The Trial" — the Trial cinematic frame's narrative source
- `court-of-forms.md` C5 — the commemorated-event pattern that informs the Trial cinematic
- File 28 § B10 + § B11 + § B13 — gauntlet structure / geometry palette / telegraphs (the mechanical substrate this doc renders)
- File 30 — current state monster generation (the engine pipeline that emits the new fields)
- File 32 § 12.5 — asymmetric indicator scaling (player 0.92× / enemy 1.08×) — adjacent player-perception design
- Doc 37 § 4 — Position C embodiment-as-narrative-skin (the non-humanoid extension this doc's S1 registry must eventually serve)
- `agentic_orchestration/research/knowledge/asset-catalogues/2026-05-16-pixijs-compatible-2d-vfx-libraries.md` — asset landscape that supplies the registry

---

## Maintenance protocol

When implementation work begins on this doc:

1. Re-read with implementers (rocket, drax, star-lord, legolas).
2. Convert structural commitments (S1-S7) into specific schema fields / rendering routines / dispatch scopes.
3. Resolve open questions (Q1-Q5) with Matt before locking implementation details.
4. Preserve canonical-lock-date history; supersession via append.

When LLM prompt work needs to reference enemy presentation:

1. Use the canonical vocabulary: *monster archetypes*, *trial encounter*, *Mirror Trial*, *cinematic-tier aura*, etc.
2. Do not invent parallel framings.

When future canonical design docs touch player-perception:

1. Cross-reference this doc.
2. Discipline #13 applies: name the failure pattern, name the corrective architecture, name what's rejected.

— gandalf, with Matt's commission and standing approval on captured locks (2026-05-15)
