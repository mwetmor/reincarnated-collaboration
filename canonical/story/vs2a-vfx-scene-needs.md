# VS2a VFX Scene-Needs Spec — Per-Encounter VFX Slot Enumeration

**Status:** **Canonical design spec.** Authored 2026-05-17 jointly by gandalf (sections 1, 3, 4, 5 + top-level register-fence authoring rule) and drax (section 2). Activated per `agentic_orchestration/dispatches/2026-05-16-gandalf-drax-vfx-scene-needs-spec.md` (Matt L3 2026-05-17 ~19:30 EDT). All three micro-decisions LOCKED: **(A) HYBRID a3** canonical-7 at combat-text + per-season at flavor with register-fence-per-UI-surface authoring rule; **(B) mix-mode** — humanoid + non-humanoid both supported at generation, ~75% failure rate, curation selects (feature not bug); **(C) Option II** — VS2a + VS2b forward-looking content.

**Downstream consumers:** elrond (Pimen subset selection — § 3 input; VS2b attribution-pipeline schema dispatch — § 4 + § 5 input); drax (VS2a ad-hoc first-VFX integration — sections 1, 2, 4 + register-fence rule).

**Authoring boundary.** This is a *spec*. It is NOT:
- a Pimen subset selection (elrond owns; downstream dispatch consumes section 3 output)
- a VS2b attribution-pipeline schema (elrond owns; downstream dispatch)
- per-pack asset evaluation (drax ingest pipeline already handles consumption)
- amendment to existing canonical-story docs (this references; does not edit)
- an engine-side ask (substrate-tags here are what the engine emits at current state + Phase-1 P1 closures)

**Scope claim.** This spec is authored at **substrate-level granularity**, intentionally agnostic of the four deferred catalogue-track sub-locks (cipher-width, Foundation layer, D1, per-season vocabulary coupling). It anticipates a VS2b forward-looking layer per Option II but does NOT pre-commit cipher-width to any specific outcome — Section 4's forward-looking content uses the canonical-7 substrate as the rendering target and parks cipher-width-expansion as an amendment-trigger (per Section 5 Q4).

**Companion docs (binding references):**
- `canonical/story/style-register.md` — HD-2D-pixel locked register; consumption-time filter on every catalogue mapping below
- `canonical/story/enemy-visual-legibility.md` — S1-S7 commitments; the visual-legibility architecture this spec's per-encounter rendering serves
- `canonical/story/court-of-forms.md` — Trial encounter ritual; C5 commemorated-event pattern (informs Trial VFX)
- `canonical/story/embodiment-narrative-layer.md` — 8-embodiment taxonomy; Mix-mode generation scope per Sub-decision B
- `canonical/story/grouping-layer-vocabulary.md` v1.2 — canonical-7 substrate (`fire/water/earth/wind/lightning/holy/shadow`) + impact foundation
- `canonical/story/form-bias-cadence-strategy.md` § 5 + § 6 + § 7 — strategic-axis lock; three-layer model; Option II cadence framing
- `canonical/29-design-overview.md` § "Engine 1 outputs" + § "Genre-anchored gauntlet" — encounter taxonomy + gauntlet anchor

**Pending follow-on commissions:**
- elrond downstream Pimen subset selection dispatch consumes Section 3
- drax ad-hoc VS2a first-VFX integration consumes Sections 1, 2, 4
- elrond VS2b attribution-pipeline schema dispatch consumes Sections 4, 5
- knight-rider drafts decisions-log entry on the **register-fence-per-UI-surface authoring rule** at top-level (per § "Top-level binding authoring discipline" below) — that rule's authority is broader than this spec and deserves canonicalization in its own right

---

## Top-level binding authoring discipline — Register-fence per UI surface block

**LOCKED CANONICAL 2026-05-17.** Lifted from gandalf v1.10 Sub-A advisory per dispatch resolution; promoted from Sub-A guard to top-level spec discipline per knight-rider follow-up directive.

**The rule:**

> Within any single UI surface block, exactly one vocabulary register appears. The blocks and their authoritative registers are:
>
> | UI surface block | Authoritative register | Forbidden content |
> |---|---|---|
> | **Stats block** (damage numbers, resistance values, attribute scores, stat-line breakdown) | **canonical-7 substrate only** (`fire / water / earth / wind / lightning / holy / shadow / impact`) | per-season vocabulary words |
> | **Status-effect labels** (in-combat status icons + tooltips: "burning", "frozen", "shocked", "stunned", "rooted", "silenced", etc.) | **canonical-7-derived status vocabulary** | per-season status names |
> | **Hotbar tooltips** (skill name shown on hotkey hover; key-bound action text) | **canonical-7-derived skill labels** at VS2a; per-season-derived deferred to Stage 3 (VS2b) | per-season *substrate-replacement* words at VS2a |
> | **Combat log lines** ("Player hit Frost-Wight for 87 fire damage") | **canonical-7 substrate words for element/damage-type tokens** | per-season vocabulary; flavor-text register |
> | **Flavor-text block** (item card flavor blurb; quest description prose; NPC dialog body) | **per-season vocabulary only** | canonical-7 substrate words — NEVER appear here |
> | **Item-label block** (item name as displayed on the loot drop / inventory tile) | **season-authored derived label** (may echo per-season *theme* words; never the per-season *substrate-replacement* word AND never canonical-7 substrate words) | mixing canonical-7 + flavor in same label |
> | **Skill-name block** (player skill name in skill tree + skill description body) | **canonical-7-derived for VS2a; per-season-derived deferred to Stage 3** | mixed-register within a single skill-name string |
> | **Naming-triad surfaces** (Trial-name; Mirror-name; Passage-name) | **per-season vocabulary** (per `naming-triad.md` cipher integration) | canonical-7 substrate words |
> | **Lore codex entries** (out-of-combat reading; story moments) | **per-season vocabulary** | canonical-7 substrate words |

**Why this is top-level, not just a Sub-A guard.** The rule is load-bearing for ALL VS2a+ player-facing content regardless of cipher migration timing. It governs how stats render, how items read, how skills name themselves, how seasons skin their narrative. The cipher migration changes WHICH register lives at the skill-name and hotbar surfaces; the fence between stats and flavor is the same either way.

**Genre precedent grounding.** Diablo II/III/IV and PoE all enforce this fence implicitly. PoE's GGG postmortems on the One With Nothing era explicitly call out: when players parsed stats and flavor as the *same* register, click-target latency rose and the loop's flow state collapsed. Last Epoch shipped per-class skill-rename in 0.8.x, walked it back after telemetry showed first-character-bounce on returning players. The fence is the architectural shape that produces ARPG-grade combat cognition at the 200ms target named in `enemy-visual-legibility.md`.

**Authoring failure modes the rule prevents:**

1. **Mixed-register item card** (Matt's bigger concern at v1.10 consult): item displays `Searing Brand / "the searing tongue of liquid memory" / +12 fire damage`. Player reads three registers; noise rises; immersion drops. Under the fence: label register (theme-echo of season) ≠ flavor register (per-season substrate-replacement) ≠ stats register (canonical-7). Eye learns the geography after the first item; cognitive load stays low.

2. **Status-effect register collision**: a season replaces "burning" with "memory-touched" in flavor and the LLM bleeds this into the in-combat status icon tooltip. Under the fence: status-effect labels are canonical-7-derived regardless of season vocabulary. The flavor blurb describing the status in the codex IS per-season; the icon-on-the-enemy's tooltip is not.

3. **Skill-tooltip cipher drift**: post-cipher VS2b, the LLM is hidden from canonical-7 substrate but the skill-name surface accidentally pulls a canonical-7 word from a training-default. Under the fence: skill-name strings are scrubbed to the locked register; star-lord LLM-prompt construction at Stage 3 cipher migration enforces canonical-7-hidden discipline.

**Spec consumption.** Every section below honors the rule. Where a section names a substrate-tag, that's the canonical-7 substrate register (Section 3's inventory format). Where a section names a season-flavored experience, that's the per-season vocabulary register (Section 4's scene-walkthroughs). VFX assets themselves are register-agnostic — they render the substrate's *visual* identity; the LLM-generated text decorating them lives in the appropriate fence-block.

---

## Section 1 — Encounter-type inventory (gandalf design framing)

The gauntlet's seven content-type encounters (per `canonical/29-design-overview.md` § "Genre-anchored gauntlet" + file 33 § "Tier structure" + `enemy-visual-legibility.md` S3-S5 tier coding) carry distinct VFX presence. Each encounter type's VFX expectation is grounded in what the player must *perceive and feel* at that encounter — not just what the engine emits mechanically.

The table below enumerates per-encounter VFX presence at substrate-granularity. Diegetic-load is gandalf design judgment (what makes the encounter type matter); cardinality columns are operational sizing for drax + elrond consumption.

### 1.1 The seven encounter types — VFX presence matrix

| Encounter type | Combatant count typical | Skill-cast VFX presence | Per-impact VFX presence | Per-status / ambient VFX presence | Cinematic-frame trigger | Tier-aura class (per `enemy-visual-legibility.md` S3) |
|---|---|---|---|---|---|---|
| **Swarm** | 5-12 units per pack (PackProxy entity per gamora B10.2) | Low per-unit (units don't independently cast); pack-level group-cast OK | High frequency but visually-simplified per-unit (cluster reads as one); pack-cluster impact aggregation | Pack-level unified aura ONLY (no per-unit ambient — clutter) | NO | **swarm** — unified pack-cluster aura, element-coded |
| **Trash** | 1-3 units; baseline mob | Standard per-unit (each unit casts independently); cast-charge expected but brief | Standard per-impact; canonical impact-burst signature | Brief ambient (element-coded shimmer at minimum); status effects render per-unit | NO | **trash** — none baseline; silhouette + name-banner carry tier |
| **Magic** | 1-3 units; tier-up from trash | Standard cast-charge + projectile/melee VFX; subtly more elaborate animation than trash | Standard impact + small element-secondary aura on hit (the "magic" tier-bump made visible) | Faint shimmer aura (element-palette tint); status effects render with slightly-brighter tint | NO | **magic** — faint shimmer in element palette |
| **Pack** | 1-3 units, geometrically arranged (Diablo III-style affix-pack precedent) | Standard cast-charge; pack-coordinated cast moments (cardinal-direction synchronous casts when affix supports) | Standard impact; potential pack-shared status application (one cast → all pack units carry the status) | Pack-shared visible aura (element + pack-affix coloring); status-cascade visuals | NO | **pack** — visible aura, element + affix-coloring |
| **Elite** | 1 unit; bestiary "elite" tier | Pronounced cast-charge with windup; longer projectile/melee VFX; **first encounter type where cast-charge carries meaningful telegraph weight** (per B13 narrow-slice landing universal dodge mechanic) | Stronger impact VFX; impact-shake or screen-edge tint at high-magnitude hits | Persistent visible aura; status applications carry distinct VFX class (status-application-burst on first contact, then status-ambient) | NO | **elite** — visible aura, element-coded, single-color |
| **Mini-boss** | 1 unit; pre-Trial cinematic preview tier | Strong cast-charge with multi-stage windup (charge → release sub-phases); cinematic-tier projectile/melee VFX | Strong impact + camera-shake; screen-edge element-coded tint on signature attacks | Strong persistent aura, possibly two-color (primary element + secondary element-flavor or status-prefigure); status effects render distinct from elite | OPTIONAL — encounter-banner only; no full cinematic pause | **mini-boss** — strong aura, element-coded, possibly two-color |
| **Boss / Trial encounter** | 1 unit; act-culmination | Cinematic-tier cast-charge with phase-based variation (boss-phase-transition VFX); signature attack VFX distinct from any tier below | Cinematic-tier impact; signature impact-burst + camera-shake + screen-edge tint + slow-mo at high-magnitude moments (B13 territory; VS2a budget-limited) | Cinematic-tier persistent aura (often pulsing or animated); status applications carry signature VFX class | **YES — Trial moment ritual fires** (pause-the-game cinematic frame + full LLM-name banner + Spirit Guide voice + Body-swap/Mirror choice screen) | **boss / act-boss / Trial encounter** — cinematic-tier aura, screen-edge tint, distinctive shape |

### 1.2 What VFX moments are diegetic-load-bearing per encounter type

Per-encounter design framing — what does the VFX work do that gameplay-text + audio cannot?

**Swarm encounter.** The diegetic load is *legibility under density*. The player sees 5-12 units; the visual contract is "this is one *thing*, not 12 independent threats." Pack-cluster aura is the load-bearing VFX presence (per `enemy-visual-legibility.md` S6); per-unit VFX is intentionally *understated* to prevent the swarm from reading as visual chaos. PoE shipped this exact lesson — early-PoE swarm packs without unified aura read as noise; rare-pack visualization with shared aura solved it.

**Trash encounter.** The diegetic load is *substrate teaching*. Trash is where the player learns "fire looks like THIS in this season; water looks like THAT." Element-palette teaching happens almost entirely at trash tier because that's where 70% of mob-clear time lives (per gauntlet density per file 29 § "Genre-anchored gauntlet"). VFX at trash tier must be *clean and consistent* — every fire-trash uses the same element-palette signature; every water-trash uses the same. Consistency is the design constraint; flair is anti-pattern.

**Magic encounter.** The diegetic load is *substrate variant*. Magic-tier introduces "this monster uses fire BUT also carries a status-application or a secondary-element flavor." The faint shimmer + small element-secondary aura on hit is the visible promotion above trash. Diablo II's Magic-tier monsters with one prefix/suffix shipped this exact pattern — the prefix's element flavor is *visible in combat*, not just text on the kill notification.

**Pack encounter.** The diegetic load is *coordinated-threat recognition*. Pack-shared aura signals "these units are *together*; they share affixes; killing one doesn't change the others' status." The pack-shared cast moment (when supported by affix) is the diegetic-load-bearing VFX — Diablo III's affixed packs ship this in the form of synchronous teleport, synchronous nova-burst, etc. The visual coordination *is* the gameplay information. Without VFX coordination, the affix mechanic reads as separate-monster random behavior.

**Elite encounter.** The diegetic load is *threat-arrival presence + telegraph teaching*. Elite is the FIRST encounter type where the player *should* feel a threat-arrival moment ("ah, an elite — slow down and read") and the cast-charge VFX is where the threat-arrival presence lives. Elite cast-charge VFX also teaches the player the telegraph vocabulary that mini-boss + boss tiers will demand the player respect — if elite cast-charges are insufficiently distinct, the player arrives at mini-boss tier without the cognitive scaffolding to read the telegraphs there. **This is the load-bearing per-tier teaching moment B13 narrow-slice depends on.** PoE map-tier rare monsters ship this; Last Epoch's rare-spawn elites ship this.

**Mini-boss encounter.** The diegetic load is *pre-Trial cinematic preview*. Mini-boss exists structurally as a tier-up signal between elite and Trial encounter — it tells the player "the act is approaching its culmination; the bestiary is showing its hand." Mini-boss multi-stage cast-charge VFX + screen-edge tint + signature ambient aura is the visual contract for "this is bigger than elite, smaller than Trial." Diablo II's act-2 / act-3 / act-4 mini-bosses (Radament, Ancients, Diablo's gauntlet) ship this; D4's mini-bosses ship this. Reincarnated's mini-bosses are *the same architectural slot* — fewer than 1 per gauntlet run but more than 0; cinematic enough to remember; not the act-culmination itself.

**Boss / Trial encounter.** The diegetic load is *act culmination + ritual moment*. The Trial encounter triggers the Trial moment ritual (per `enemy-visual-legibility.md` S4 + `court-of-forms.md` C5 + forthcoming `trial-moment-ritual.md`). Cinematic frame, Spirit Guide voice, Body-swap/Mirror choice screen. The VFX work here is the *most asset-cost-intensive* per encounter; per-season cinematic-aura signatures are the candidate (per `enemy-visual-legibility.md` Q4 option (b) — one signature per season; three per season; act-end ritual weight). Solo Leveling's manhwa adaptation handles each Shadow recruitment moment at this scale; the genre-precedent register is *ceremonious*, not *combat-intense*.

### 1.3 Embodiment-axis presence per encounter (Sub-decision B mix-mode lock)

Per Sub-decision B's mix-mode lock — humanoid + non-humanoid both generation-supported; curation selects which seasons ship at ~75% generative failure rate accepted as design feature.

**VS2a humanoid baseline.** All seven encounter types have humanoid-embodiment coverage at VS2a (the engine's current default; chierit character pack handles player + class-converged Trial bosses).

**VS2a non-humanoid coverage.** Non-humanoid embodiments are generation-eligible at VS2a but not curation-guaranteed-shipped. Specifically:

| Embodiment | Per-encounter VFX-renderability at VS2a | Asset-availability at VS2a (per locked HD-2D-pixel register catalogue) | Curation likelihood |
|---|---|---|---|
| **Humanoid** | All 7 encounter types | Chierit Elementals + Pimen humanoid-sprite assets | 100% (engine default) |
| **Slime** | Swarm + Trash + Magic + Elite cleanly; Mini-boss + Boss + Trial possible with elite/boss slime asset acquisition (Pimen ships zero slime sprites at current crawl per § 4.8 of pre-inventory) | **Gap — no curated slime sprites at VS2a; per-embodiment sprite-archetype work blocked on Legolas Mode B non-humanoid commission** | Low at VS2a; high at VS2b after non-humanoid asset acquisition |
| **Beast** | All 7 plausibly; depends on catalogue | Partial — Pimen fantasy-skeleton-enemies + skeleton-archetype-coded assets cover some beast-undead-coded encounters; pure beast (cat/wolf/kitsune) coverage gap | Low-medium at VS2a |
| **Dragonling** | Mini-boss + Boss + Trial well-suited (cinematic-tier asset density required); under-suited for Swarm/Trash (dragonling-as-trash reads wrong) | **Gap — no curated dragonling assets at VS2a** | Low at VS2a |
| **Swarm** (hive-mind embodiment, distinct from swarm-encounter-type) | Swarm encounter cleanly (the embodiment IS the encounter shape); Pack encounter partial | **Gap — Pimen's swarm-tier monster assets cover swarm-encounter mechanically; embodiment-narrative swarm coverage is content-curation territory** | Medium at VS2a |
| **Construct** | All 7 plausibly | **Gap — Earth Elemental enemy from Pimen earth-spell-effect-03 is the only curated construct asset** | Low at VS2a |
| **Spirit** | Magic / Elite / Mini-boss / Trial well-suited (the spirit-form is cosmologically loaded); under-suited for Swarm/Trash | **Gap — no curated spirit-coded assets** | Low at VS2a |
| **Plant** | Trash / Magic / Pack plausibly; under-suited for Boss/Trial (plant-as-act-boss is niche-precedent) | **Gap — no curated plant-embodiment assets** | Low at VS2a |

**Operational implication for VS2a.** Curation at VS2a will most likely ship humanoid-only seasons (or humanoid + 1 non-humanoid with constrained encounter-type coverage on the non-humanoid side). The ~75% failure rate Matt-locked is exactly this — seven non-humanoid embodiment slots, partial catalogue coverage, asset acquisition behind the curation choice. The spec authors against the mix-mode generation architecture; what ships at VS2a is curation's call against the asset landscape at curation-time.

**VS2b forward-looking implication (per Sub-decision C Option II).** Section 4's per-encounter scene-walkthroughs include non-humanoid embodiment rendering for the three highest-genre-precedent forms (Slime / Spider / Dragon-Hatchling per `embodiment-narrative-layer.md` + Legolas Pass 1 isekai non-humanoid sub-genre lineage). Post-Legolas Mode B non-humanoid asset commission, the VS2b catalogue covers these forms; the spec's Section 4 scene-walkthroughs become implementation-ready.

### 1.4 Cross-encounter-type VFX continuity rules

Three load-bearing continuity rules across the seven encounter types — these are gandalf design judgments protecting the player's combat-cognition stack.

**Continuity rule R1: Element-palette consistency across tiers within a season.**

The fire-trash in season N and the fire-elite in season N use the SAME element-palette signature (per `enemy-visual-legibility.md` S2). The elite carries MORE aura, longer cast-charge, stronger impact — but the *color identity* and the *element-coded visual identity* don't shift between tiers. Player reads "fire" at trash; recognizes "fire" at elite without re-learning. ARPG canon shipped — D2's Fire Tower (boss) is recognizably the same fire-mode the player saw on Fire Towers (trash) in act-1; PoE's Fire-themed map-bosses use the same fire-tint as the trash mobs in that map.

**Continuity rule R2: Tier-aura class progression is monotonic.**

Per `enemy-visual-legibility.md` S3: swarm pack-cluster < trash baseline < magic shimmer < pack visible+affix < elite visible single-color < mini-boss strong two-color < boss/Trial cinematic. The player's eye learns the gradient. A magic encounter does NOT carry visible-aura that reads stronger than an elite encounter's aura — that breaks the tier vocabulary. Drax rendering pipeline enforces; engine emits `display_aura_tier` per monster (already specified at `enemy-visual-legibility.md` § "What engine generation must emit").

**Continuity rule R3: Cast-charge telegraph density grows monotonically with tier.**

The cast-charge VFX (the pre-cast visual moment, the windup, the prep) is the dodge-mechanic's anchoring surface (per B13 narrow-slice landed at Phase-1 P1 D28). Cast-charge density is *thin* at trash (player should not need to dodge every trash cast); *moderate* at magic; *meaningful* at elite (first tier where dodge cognition matters); *cinematic* at mini-boss + boss. The player's dodge muscle-memory builds at elite tier; transfers to boss/Trial. If trash cast-charges are too elaborate, dodge-tax fatigue sets in; if elite cast-charges are insufficiently distinct, the dodge mechanic never teaches.

This continuity rule constrains Section 2's per-skill VFX slot enumeration (drax territory): the same skill cast by a trash-tier enemy and the same skill cast by an elite-tier enemy may render with DIFFERENT cast-charge VFX density (shorter windup at trash; longer at elite), even though the substrate-tag and mechanical effect are identical. This is per-tier *animation scaling*, not per-tier *asset substitution* — same asset family; different frame count or timing curve. Drax pipeline owns the timing-curve layer.

### 1.5 Encounter-type inventory — completion summary

| Metric | Value |
|---|---:|
| Encounter types enumerated | 7 |
| Per-encounter VFX-presence cells filled | 7 × 5 = 35 (skill-cast / per-impact / per-status-ambient / cinematic / tier-aura) |
| Continuity rules canonicalized | 3 |
| Embodiment-axis coverage gaps flagged | 7 non-humanoid embodiments (slime/beast/dragonling/swarm/construct/spirit/plant); explicit feed to Section 3 catalogue-gap surface |

---

## Section 2 — Per-skill VFX slot enumeration (drax render-constraint framing)

**Author:** drax
**Date:** 2026-05-17
**Scope:** This section enumerates per-archetype-aggregate VFX slots — the SHAPE of what the render pipeline needs, not a per-skill listing. Framed entirely from the consumption side: what Pixi.js must load, when it fires, how layers stack, what the performance ceiling is.

### 2.0 — Render pipeline baseline (how VFX lands in demo today)

Before enumerating slots, the render infrastructure they plug into:

**Layer stack (demo `src/rendering/stage.ts`):**
```
app.stage (Pixi root)
  └─ bg         (static arena floor / color fill)
  └─ arena      (wave decorations, ambient motes)
  └─ entities   (combatant sprites + attached bars/labels)
  └─ particles  (ALL ability VFX + floating damage numbers)  ← VFX target layer
  └─ ui         (HUD — always on top)
```

All VFX lives in `_layers.particles`. This is a flat `Container` — no sub-layering within it today. The slot enumeration below surfaces where sub-layering WITHIN particles will be necessary (specifically: cast-charge behind the caster; projectiles above the floor but below the caster entity; impacts composited above the entity at peak and then below on fade). These sub-container slots are a VS2a integration task.

**Object model (demo `src/main.ts` vfxPools):**
VFX is pool-managed: `projectiles`, `aoeRings`, `hitFlashes`, `meleeFlashes`, `totems`, `auras`, `beams`, `spriteVfx`, `floatingNumbers`, `chainArcs`, `ringAoes`, `vortexPulls`, `whirlwinds`. Each pool is tick-advanced each frame via the main ticker. Sprite-based VFX (Pimen packs) enter via `spriteVfx` pool today; the pool handles `AnimatedSprite` lifecycle (spawn, tick, despawn on animation complete).

**Spritesheet consumption model (demo `src/abilities/vfx.ts` + ingest pipeline):**
- Pimen packs ingested via `scripts/pimen-ingest/` stages 1-3 → produce `public/assets/pimen/<slug>/sheets/<anim-name>.png` + `metadata.json`
- `metadata.json` schema: `{ pack_slug, animations: [{ name, frame_count, canvas_width, canvas_height, sheet_width, sheet_height, cols, rows, fps_hint }] }`
- Pixi loads the spritesheet via `Texture.from(sheet_path)` + subdivides into frame-count textures using `canvas_width × canvas_height` frame dimensions
- `AnimatedSprite` constructed from the texture array; `animationSpeed` set from `fps_hint / app.ticker.FPS` (12.5fps default for Pimen's 80ms frame rate)
- Loop behavior per slot: see § 2.3 below

**Performance budget:** The existing vfxPools architecture keeps each frame's VFX tick at <0.5ms on a typical encounter. The demo's current bottleneck is sprite rendering, not JS tick logic. For VS2a content density (single-player combat, ~5-15 VFX objects active simultaneously), the constraint is texture-swap count, not arithmetic. **Rule: no more than 1 texture atlas per VFX slot per encounter if avoidable** — atlas consolidation per element is the optimization target for VS2b attribution pipeline.

---

### 2.1 — Archetype families and their VFX slot demands

The engine emits skills against these archetype families (per `b6_archetype_templates.py` + `archetype_composer.py`):

| Archetype family | Representative tags | Dominant skill roles | Key geometry palette items |
|---|---|---|---|
| **Elemental mage** | `fire_mage`, `water_mage`, `lightning_mage`, `holy_mage`, `shadow_mage` | `burst_damage`, `primary_attack` | `projectile_straight`, `impact_burst`, `nova_radial` |
| **Elemental caster** | `fire_caster` (= fire_mage alias), `earth_caster`, `wind_caster`, `lightning_caster`, `holy_caster`, `shadow_caster` | `area_damage`, `primary_attack` | `nova_radial`, `nova_wave`, `ground_targeted_circle`, `cone` |
| **Elemental controller** | `fire_controller`, `water_controller`, `earth_controller`, `wind_controller`, `lightning_controller`, `holy_controller`, `shadow_controller` | `control` (ailments), `area_damage` | `vortex_pull`, `aura_radial`, `ring_aoe`, `ground_slam_directional` |
| **Physical warrior** | `physical_warrior`, `physical_grappler`, `physical_skirmisher` | `burst_damage`, `area_damage`, `control` (CC), `defensive` | `melee_arc`, `melee_strike`, `ground_slam_directional`, `leap_strike` (composite) |
| **Hunter** | `hunter` | `burst_damage`, `mobility`, `defensive` | `projectile_straight`, `impact_burst`, `dash_attack` |
| **Rogue** | `rogue` | `burst_damage`, `mobility` (×2) | `dash_attack`, `projectile_straight`, `melee_strike` |
*Note: `hybrid_mage` was removed from this archetype coverage table per canonical-6 transition 2026-05-18. The hybrid mage row (area_damage ×2, burst_damage ×2, damage_over_time, defensive, utility; nova_radial / nova_wave / aura_radial / beam_channel / projectile_straight) is historical record. VFX commissions originally scoped for hybrid_mage should be re-mapped to substrate-coherent canonical-6 archetypes where needed. `beam_channel` geometry is not uniquely hybrid_mage's — controller archetypes can use it per b6_archetype_templates. See `canonical/story/canonical-6-transition-retire-hybrid-mage-2026-05-18.md` for context.*

The VFX slot enumeration that follows covers these families in aggregate. Per-archetype variations are noted where they materially differ.

---

### 2.2 — VFX slot taxonomy

Six canonical slots. All skills cast by any archetype family consume a subset of these slots; the subset depends on geometry and effect type.

#### Slot A: Cast-charge

| Property | Constraint |
|---|---|
| **What it is** | Pre-release visual at the caster's position: the "preparation moment." Wind-up glow, energy gathering, stance shift, particle accumulation. |
| **Duration** | Tightly coupled to skill's `cast_time` engine field. For VS2a at current archetype templates: 0–0.4s typical; instant-cast skills (e.g., primary_attack projectiles) may emit a 1-3 frame "muzzle-prep" flash only. |
| **Anchor** | Caster sprite origin (`entities` layer coordinate). VFX Container must track caster position if cast_time > 0.1s (the caster can be repositioned by a knockback mid-cast; the cast-charge should follow or snap-cancel). |
| **Layer** | `particles` layer, BEHIND caster entity in Z-order. Implemented as a `particles` sub-container rendered before `entities` re-addition, OR as a separate VFX injected at `entities` z-index - 1 (to-be-resolved at VS2a integration). |
| **Sprite vs procedural** | Procedural acceptable for VS2a (radial glow Graphics object scaled to element color). Pimen asset preferred when available — cast-charge from `aura_radial` pack subset (the "charging" frame range of an aura animation). |
| **Substrate-tag target** | `<element>-cast-charge` (e.g., `fire-cast-charge`, `water-cast-charge`). One per canonical-7 element. For physical archetypes: `physical-cast-charge` (melee stance). |
| **Loop behavior** | Loop ON during cast_time; terminate on skill-released OR interrupted. Must be interruptible mid-loop cleanly (pool.release() must not leave a zombie AnimatedSprite). |
| **Archetypes that skip this slot** | Instant-cast `primary_attack` skills in hunter / rogue (e.g., ranged auto-fire) may use a minimal 2-frame muzzle-flash variant rather than a sustained cast-charge. |
| **VS2b forward hook** | Per-embodiment narrative-skin: the "charging moment" for a non-humanoid form (e.g., Slime swelling, Spider raising forelegs) is character-animation territory, not VFX territory. Slot A for non-humanoid is thin (element-glow only; character animation owns the preparation gesture). |

---

#### Slot B: Projectile / movement

| Property | Constraint |
|---|---|
| **What it is** | In-flight visual for skills with a travel leg: projectile moving toward a target, dash-arc of the caster, or beam channel from caster to impact point. |
| **Applies to** | `projectile_straight` (mage/caster/hunter/rogue), `beam_channel` (hybrid_mage *[RETIRED 2026-05-18 — beam_channel re-maps to controller archetypes in canonical-6]*), `dash_attack` + `defensive_dash` (rogue/hunter/skirmisher). Does NOT apply to instant-delivery geometries (`impact_burst`, `nova_radial`, `ground_targeted_circle`). |
| **Duration** | Travel-time-bound: `range / speed` engine fields. Typical: 0.1–0.5s for melee range; 0.3–1.2s for max-range projectile. Beam_channel: sustain duration, 0.5–2s. |
| **Anchor** | Moving: projectile Container translates from `fromX/fromY` to `toX/toY` each frame via `tickProjectiles()`. Current demo implementation moves a Graphics-drawn circle; Pimen sprite replaces the circle primitive. |
| **Layer** | `particles` layer, ABOVE arena floor but BELOW entity sprites (so a projectile travels "through" the world plane rather than over the caster). Z-index between `bg` and `entities`. |
| **Sprite vs procedural** | Sprite preferred (the "in-flight" frame of a spell-effect pack). Typically 1–4 looping frames from the projectile sub-animation. The Pimen `projectile` and `bullet` mechanic-tagged assets are the catalogue source. |
| **Substrate-tag target** | `<element>-projectile` for straight projectile; `<element>-beam` for channel; `<element>-dash-trail` for movement. Physical: `physical-projectile` (arrow/bolt), `physical-dash-trail` (motion blur). |
| **Loop behavior** | Loop ON while in flight; STOP on arrival (replaced by Slot C impact). The transition from B → C must be frame-exact to avoid visual double-flash. In practice: when `tickProjectiles` calls the impact handler, it despawns the Slot B sprite in the same tick and spawns the Slot C impact. |
| **Special: beam_channel** | Beam is rendered as a STATIC sprite (or tiled repeat) between two anchor points, not a moving object. Pixi Graphics `moveTo/lineTo` with a custom GLSL shader is the correct path for non-trivial beams; a simple sprite strip (repeated texture at fixed intervals) is acceptable for VS2a. |
| **Special: dash_attack / defensive_dash** | The caster entity moves, leaving a "trail" — this is the Slot B visual for dash geometries. Trail is typically a fading alpha of the caster's sprite (or a motion-blur smear). Pimen `smear` tag is the catalogue source. NOT the same as a projectile. |
| **VS2b forward hook** | For non-humanoid embodiments: the "dash trail" visual depends on the creature's silhouette (a Slime's dash leaves a different trail than a humanoid's). Tag: `<element>-<embodiment>-dash-trail` (VS2b schema; VS2a uses `<element>-dash-trail` only). |

---

#### Slot C: Impact

| Property | Constraint |
|---|---|
| **What it is** | Hit-resolution visual at the target's position (or AOE center): the "strike landed" moment. Explosion burst, slash flash, energy wave, terrain slam. |
| **Applies to** | ALL skills that deal damage or apply control. This is the most visually load-bearing slot — the player's primary hit-confirmation read. |
| **Duration** | Short: 0.15–0.5s. One-shot (play once and despawn). For AOE skills, the impact may play simultaneously at multiple positions (per-target instance) or as a single centered radial (per-geometry). |
| **Anchor** | Target position (`tx, ty` from the engine hit event). For AOE radial skills: the AOE center coordinate. For `cone` and `ground_slam_directional`: the center of the cone's arc or the slam's forward point. |
| **Layer** | `particles` layer, ABOVE entity sprites at peak frame (the brightest frame should read over the caster/target). Fade frames drop below entities. Sub-layering within `particles` needed: a `particlesBelow` / `particlesAbove` split, where impact-peak frames use `particlesAbove` and fade frames use `particlesBelow`. |
| **Sprite vs procedural** | Sprite required for VS2a — this is the visible frame the player reads as "hit confirmed." The demo currently uses procedural `hitFlashes` (Graphics circles); Pimen `impact` / `explosion` / `hit-effect` mechanic-tagged assets replace these. |
| **Frame discipline** | The "peak impact frame" (the brightest, most readable frame) must land on frame 1 or 2 of the animation, not after a build-up. Pimen's `impact` packs generally respect this (most are front-loaded). Verify at acquisition: if a pack has a 3-5 frame build-up before the peak, it is NOT suitable for Slot C (it reads as a delayed hit, not a crisp hit-confirm). |
| **Substrate-tag target** | `<element>-impact` for direct-hit skills; `<element>-aoe-impact` for AOE radial skills; `physical-impact` for melee; `physical-slash` for melee-arc. Sub-tags needed: `fire-impact`, `water-impact`, `earth-impact`, `wind-impact`, `lightning-impact`, `holy-impact`, `shadow-impact`. Physical sub-tags: `physical-impact`, `physical-slash`, `physical-slam`. |
| **AOE scaling note** | For large AOE radials (radius > 150 demo-px), the impact sprite must scale. Do NOT use `Transform.scale` on a single-canvas animation without first verifying canvas_width at the intended scale. Pimen's `impact_burst` packs (many at 64×64 canvas) will pixelate at 3× scale. The correct path for large AOEs: source a larger-canvas asset OR use a tiled/layered multi-instance ring pattern (existing `aoeRings` pool) as the outer ring and a single impact at center. |
| **VS2b forward hook** | Per-embodiment impact skins: a Slime taking a fire hit receives a `fire-impact-slime` override (bubbling scorch rather than standard explosion). Tag structure: `<element>-impact-<embodiment>`. VS2a: single skin only. |

---

#### Slot D: Status-application

| Property | Constraint |
|---|---|
| **What it is** | The visual moment when a status effect attaches to the target: a brief overlay flash or ring that confirms "ailment applied." Distinct from the ongoing Slot E ambient. |
| **Applies to** | Skills with `control` role (controller archetypes) that apply ailments (stun, root, slow, burn DoT, etc.). Also: `damage_over_time` skills (fire_mage burn tick, shadow DoT). |
| **Duration** | Very short: 0.1–0.3s. One-shot, concurrent with the tail of Slot C. Slot D fires immediately after Slot C peak; the player reads "hit + ailment applied" as a single compound event. |
| **Anchor** | Target position, same as Slot C. If multiple targets receive the ailment simultaneously (AOE controller skill), one Slot D instance per target. |
| **Layer** | `particles` layer, ABOVE entity sprites. Rendered slightly after Slot C (1 frame delay) so the status ring appears to emerge from the impact flash. |
| **Sprite vs procedural** | Sprite preferred. The Pimen `buff`/`debuff`/`status-effect` packs are the catalogue source. The `debuff` packs apply here — they are "application" animations (a ring, swirl, or overlay appears on the target). |
| **Substrate-tag target** | `<element>-status-apply` for elemental ailments (fire: burn-apply, water: slow-apply, earth: root-apply, wind: knockback-apply, lightning: stun-apply, holy: blind-apply, shadow: curse-apply). `physical-status-apply` for control-with-ailment (grappler `require_control_with_ailment` constraint). |
| **Register-fence note (Sub-decision A)** | The status-application VFX is a VISUAL SUBSTRATE signal — it uses canonical-7 element vocabulary in the sprite substrate-tag, NOT per-season vocabulary. The LLM-authored skill name that appears in the combat log at this moment uses per-season vocabulary. The VFX asset catalogue is indexed by canonical-7 substrate tag only. This register-fence is load-bearing for the attribution pipeline. |
| **Concurrency** | A target may receive multiple ailments simultaneously (multi-ailment controller skill). Each ailment fires its own Slot D instance. The `spriteVfx` pool handles concurrent AnimatedSprites at the same position — no special de-dup needed, but visual stacking must be tested: 3 status-apply rings at the same (x,y) must read as distinct, not as a combined blob. Spacing offset (~8px radial jitter) recommended at integration. |
| **VS2b forward hook** | Control ailment secondary-damage signatures (`project_ailment_damage_thematic.md` — DEFERRED per `680a3f1`). If that design lands post-B14.5, Slot D may need to split into "ailment application + secondary-damage flash" as a compound event. No action at VS2a. Tag: `<element>-status-apply-secondary` reserved. |

---

#### Slot E: Status-ambient

| Property | Constraint |
|---|---|
| **What it is** | The ongoing visual while a status effect persists on the target: slow-pulse, aura tint, particle emission above the afflicted entity. Confirms to the player that the ailment is still active. |
| **Applies to** | All control ailments (stun, root, slow, burn DoT, etc.) that have non-zero duration. The `aura_radial` and `ambient` mechanic-tagged packs in the Pimen catalogue are the source material. |
| **Duration** | Matches ailment duration from the engine. Typical: 1–4s. Must sustain at loop for the full duration and terminate cleanly on ailment-clear. |
| **Anchor** | Target position, updated per frame (the afflicted enemy may still move while slowed/rooted — the ambient must track). For rooted targets: fixed anchor is fine. For slowed targets: the ambient Container must follow the entity's current position. |
| **Layer** | `particles` layer, BELOW entity sprites for ambient halos (a burn aura below the target reads as "ground fire"), ABOVE entity sprites for debuff overlays (a frost lattice over the target reads as "frozen"). Two sub-layers needed within `particles`: `particlesGroundLevel` (below entities) and `particlesOverlay` (above entities). |
| **Sprite vs procedural** | Sprite strongly preferred — this is a sustained visual and procedural particles (Graphics) will produce Z-fighting artifacts if not managed. The Pimen `buff`/`debuff`/`status-effect` packs' looping animations are intended for this slot. Catalog observation: these packs have high animation-frame-density (Pimen's buff/debuff packs have 9 assets with `status-effect` tags) — well-suited for sustained loop. |
| **Substrate-tag target** | `<element>-status-ambient` per ailment family: `fire-burn-ambient`, `water-slow-ambient`, `earth-root-ambient`, `wind-knockback-ambient` (brief; most wind ailments are short-duration), `lightning-stun-ambient`, `holy-debuff-ambient`, `shadow-curse-ambient`. Physical: `physical-stun-ambient` (stagger stars). |
| **Performance discipline** | If 4-6 enemies in a room are simultaneously rooted/burned/slowed, the `status-ambient` slot will have 4-6 concurrent AnimatedSprites. At 12.5fps each with typical Pimen 9–17 frame cycles: ~12-17 texture-object updates per frame. This is within budget but is the slot most likely to cause performance pressure at pack-content density. **Rule: status-ambient sprites must use the same Texture atlas across all instances of the same ailment type** (e.g., all `fire-burn-ambient` instances pull from the same loaded spritesheet, not re-loaded per instance). Pixi's texture cache handles this automatically if loaded once via `Texture.from()`. |
| **Termination discipline** | When ailment clears (engine `ailment_cleared` event), the Slot E AnimatedSprite must despawn cleanly. A brief 2-4 frame "dissipate" animation is preferred to abrupt pop-off — the `spriteVfx` pool's on-complete handler should trigger the dissipate variant rather than immediate pool.release(). **TODO(drax): dissipate variant support is not yet in `spriteVfx` pool — add at B11 integration.** |
| **VS2b forward hook** | Per-embodiment ailment rendering: `fire-burn-ambient-slime` (Slime burns differently than humanoid). Tag structure reserved. VS2a: single skin only. |

---

#### Slot F: Skill-expired / cooldown-feedback

| Property | Constraint |
|---|---|
| **What it is** | Optional sixth slot — a brief visual at the caster confirming the skill has finished executing and the cooldown has begun. Not a hit-confirm (that is Slot C). Not a status (that is Slots D/E). This is "your skill is now on cooldown" feedback. |
| **Applies to** | High-visual-impact skills where the player must know the skill window has closed: `burst_damage` finisher skills, long-cooldown `area_damage` nukes, `defensive` skills (the player needs to know dash is now cooling). |
| **Duration** | Very short: 0.05–0.2s. Minimal — one-shot at caster position. |
| **Anchor** | Caster position. |
| **Layer** | `particles` layer above entities (brief overhead flash at caster). |
| **Sprite vs procedural** | Procedural acceptable (a single-frame "puff" of element-colored particles). Sprite overkill for VS2a. |
| **Substrate-tag target** | Not a hard substrate tag requirement for VS2a. Mark as `<element>-skill-expired` if a Pimen asset naturally fits. Low priority for VS2a first integration — the `DashCooldownHud` HUD element (shipped at drax/v1.4) provides the primary cooldown read; Slot F is a secondary reinforcement. |
| **Rationale for inclusion** | Surfaced by gandalf's VFX design notes in `canonical/story/court-of-forms.md` context: the player needs clear "skill-window-open vs closed" legibility particularly on the burst archetypes. The HUD radial sweep handles this for the active player skill; Slot F handles it for the player's observed cooldown on NPC combat (the player watching an enemy burst-mage needs to know when the burst window resets). |
| **VS2b forward hook** | Cooldown feedback on enemy archetypes is a VS2b narrative-skin concern: a Dragon-Hatchling mage's cooldown tells a different story than a humanoid mage's. Slot F for VS2a = minimal / procedural. |

---

### 2.3 — Slot activation matrix by archetype family

Which slots fire, in what sequence, per archetype family aggregate.

| Archetype family | Slot A (cast-charge) | Slot B (projectile/movement) | Slot C (impact) | Slot D (status-apply) | Slot E (status-ambient) | Slot F (expired) |
|---|---|---|---|---|---|---|
| **Elemental mage** | YES — full sustained | YES — projectile | YES — impact burst | Rare (only if skill has ailment) | Rare (only if DoT) | YES on burst finisher |
| **Elemental caster** | YES — full sustained | No (instant AOE delivery) | YES — AOE impact | No (damage only) | No | YES on major AOE |
| **Elemental controller** | YES — brief (cast_time short) | Situational (vortex_pull has travel; most control is instant) | YES — impact flash | YES — per ailment applied | YES — per ailment sustained | YES on control finisher |
| **Physical warrior / grappler** | YES — brief stance (melee windup) | No (melee range delivery) | YES — slash/slam impact | YES (grappler: `require_control_with_ailment`) | YES (grappler only) | Optional |
| **Hunter** | Minimal (auto-attack: muzzle flash only) | YES — arrow/bolt projectile | YES — impact burst | No | No | No |
| **Rogue** | Minimal | YES — dash trail | YES — impact at end of dash | No (rogue is damage only at current templates) | No | No |
| **Hybrid mage** | YES — full sustained | YES — beam channel (sustained; Slot B and Slot C are concurrent for beam skills) | YES — AOE impact | YES (DoT slot: damage_over_time role) | YES (DoT sustained) | YES |

---

### 2.4 — Timing and sequencing constraints

**Tick-accuracy requirement:** Slots C and D fire in the same tick as the engine's hit event. The engine emits `skill_hit` events which drax consumes; the slot C+D spawn must happen in the event handler, not deferred by a setTimeout or next-tick. Current `vfxPools` architecture handles this correctly (direct push into pool in the event handler).

**Overlap discipline — Slot A and Slot B:**
- For projectile skills: Slot A plays at caster → Slot A terminates → Slot B spawns at caster position and travels → Slot B terminates at target → Slot C spawns at target.
- For instant AOE: Slot A plays at caster → terminates → Slot C spawns at AOE center simultaneously.
- For beam skills: Slot A plays at caster → Slot B (beam strip) appears spanning caster to target, sustained → Slot C plays at target position during beam sustain.

**Overlap discipline — Slot C and Slot D:**
- Slot D fires 1 frame after Slot C peak. In practice: push Slot D into pool 1 frame delayed (via a 1-frame counter in the event handler, or simply spawn both simultaneously and rely on Slot D's brief build-up frame to create the natural offset).

**Overlap discipline — Slot E and Slot D:**
- Slot E spawns on Slot D complete (or shortly after Slot D's one-shot animation finishes). The `spriteVfx` pool's `onComplete` callback is the hook: Slot D's AnimatedSprite's onComplete spawns the Slot E loop. **This is the primary integration pattern for the controller archetype VFX chain.**

**Slot E termination:**
- Engine emits `ailment_cleared` (or ailment duration expires per engine tick). Slot E AnimatedSprite switches to dissipate variant OR crossfades to invisible over 2-4 frames. The `spriteVfx` pool needs a `releaseWithFade(frames)` method. Currently unimplemented — **TODO(drax): add releaseWithFade() to spriteVfx pool at B11 integration.**

---

### 2.5 — Physical archetype VFX notes (distinct from elemental)

Physical archetypes (warrior/grappler/skirmisher/hunter/rogue) have no element substrate but their VFX slots still require substrate-tagged assets. The physical substrate-tags are:

- `physical-cast-charge` — melee stance/windup (brief; 0.1-0.2s for most melee)
- `physical-projectile` — arrow/bolt (hunter only)
- `physical-impact` — generic strike burst
- `physical-slash` — for melee_arc geometry (the blade-arc flash)
- `physical-slam` — for ground_slam_directional (grappler, physical_warrior)
- `physical-status-apply` — for grappler control ailments
- `physical-stun-ambient` — for grappler stun

**Gap note (from catalogue pre-inventory § 3.4):** The only physical impact/slash assets in the current Pimen catalogue (`pixel-battle-effects`, `cutting-and-healing`) carry CC-BY attribution. If drax-side consumption avoids attribution-required assets, physical impact and slash mechanic coverage in the catalogue collapses to zero. Flag for elrond Pimen subset selection dispatch: the `physical-slash` and `physical-impact` substrate-tags have no attribution-free coverage in the current catalogue. A vendor sweep or additional Pimen acquisition that addresses physical impacts without CC-BY constraint is needed before B11 physical-archetype integration.

---

### 2.6 — Composite-skill VFX (leap_strike and beam_channel)

These two geometry types require composite Slot B rendering — two simultaneous VFX components in the same slot.

**leap_strike (physical_warrior):**
- Slot A: standard melee windup at caster
- Slot B: character leap-arc animation (character-track, NOT a VFX sprite — this is the animated character entity traveling from origin to target; the VFX component is a `physical-dash-trail` or dust-cloud emitted along the arc)
- Slot C: `ground_slam` impact VFX at landing point (Pimen earth/fire/physical slam assets are the source)
- Per `geometry-vfx-coverage-assessment.md` § 2, this composite path (leap arc + ground_slam VFX) is the approved VS2a rendering strategy for leap_strike. Drax wires the composite.

**beam_channel (hybrid_mage):** *[hybrid_mage RETIRED 2026-05-18 per canonical-6 transition; this VFX pattern is historical record. beam_channel VFX rendering pattern below remains valid for any canonical-6 archetype that uses beam_channel geometry (e.g., controller archetypes). The Slot A/B/C pattern is geometry-driven, not archetype-specific. See `canonical/story/canonical-6-transition-retire-hybrid-mage-2026-05-18.md` for context.]*
- Slot A: standard mage cast-charge at caster
- Slot B: beam strip (static sprite or tiled repeat between caster and target positions; rendered for the full channel duration)
- Slot C: concurrent with Slot B — ongoing `<element>-impact` flash at the target end of the beam, ticking at beam-tick-rate (NOT at 12.5fps — at the engine's DoT tick rate, typically 1/s)
- The Slot B/C overlap for beam is the only case where C is sustained rather than one-shot. Implementation note: spawn C as a LOOPING AnimatedSprite at the target position with loop=true during beam sustain; despawn both B and C simultaneously on beam expiry.

---

### 2.7 — Sub-layer requirement (particles container)

Current `_layers.particles` is a flat Container. VS2a first VFX integration requires partitioning it into at minimum three sub-layers:

```
_layers.particles
  └─ particlesGround   (z: below entities — Slot E auras that read as floor halos)
  └─ particlesMid      (z: same level as entities — Slot B projectiles in flight)
  └─ particlesOver     (z: above entities — Slot C impact peaks, Slot D status rings)
```

**Implementation note:** Pixi renders Container children in insertion order. To achieve these three z-levels relative to `entities`, the options are:
- (A) Split `particles` into `particlesUnder` + `particlesOver` on either side of `entities` in `app.stage.addChild()` order — simplest; covers 90% of cases.
- (B) Add `particlesMid` between under and over — needed for projectile-travels-through-world reading.
- (C) Dynamic z-sort per frame (expensive; not recommended).

**VS2a recommendation: Option (A) minimum — split particles into under/over around entities. Adds particlesMid as a VS2a first-integration deliverable if projectile depth reads incorrectly without it.** This is a ~1-hour refactor of `stage.ts` and `main.ts` + all vfxPools spawn logic.

**TODO(drax): layer split is a prerequisite for correct Slot C (impact above entity at peak, below on fade) and Slot E (aura ground halos below entity). File as VS2a first-integration step 0, before any Pimen sprite integration begins.**

---

### 2.8 — Sprite-vs-procedural summary per slot

| Slot | VS2a target | Rationale |
|---|---|---|
| A — cast-charge | Procedural acceptable (element-color radial glow) | Short duration; low visual bandwidth; Pimen aura-subset assets are a bonus not a requirement |
| B — projectile | Sprite preferred | The "flying spell" is the archetype's primary identity visual |
| B — dash trail | Procedural acceptable (fading caster-sprite alpha) | Character-track problem; VFX is secondary |
| B — beam | Sprite tiled strip | Procedural line would not match HD-2D register |
| C — impact | Sprite required | Primary hit-confirm; must match element substrate exactly |
| D — status-apply | Sprite required | Ailment confirmation; Pimen buff/debuff packs purpose-built for this |
| E — status-ambient | Sprite required | Sustained loop; procedural particles create Z-fighting at density |
| F — expired | Procedural acceptable | Secondary feedback; HUD carries primary cooldown read |

---

### 2.9 — VS2b forward-looking render hooks

Per Sub-decision C = Option II, these hooks are enumerated now and marked as NOT implemented at VS2a:

1. **Per-embodiment impact skins** (`<element>-impact-<embodiment>`): Slot C rendering switches asset based on target's `embodiment_tag`. VS2a: no per-embodiment switch (single skin per element). Hook: `getImpactAsset(element, embodiment)` lookup table in the attribution pipeline; VS2a implementation uses `getImpactAsset(element, 'humanoid')` always.

2. **Per-season vocabulary isolation** at VFX surface: the VFX assets are indexed by canonical-7 element substrate tags. Season-authored skill names (LLM-generated per-season vocabulary) appear ONLY in combat-log text, tooltips, and hotbar labels — never as a lookup key into the VFX catalogue. This register-fence is structural in the attribution pipeline schema. VS2a and VS2b both enforce it; it is not a VS2b addition.

3. **releaseWithFade() for Slot E termination:** a clean dissipate animation variant per ailment. Pimen buff/debuff packs may include dissipate variants in their animation set — elrond should flag this at subset selection. **TODO(drax): remove this TODO when dissipate-variant support lands in spriteVfx pool.**

4. **Atlas consolidation:** VS2a attribution is ad-hoc (one asset per slot, loaded independently). VS2b attribution pipeline consolidates element-substrate VFX into atlas textures to reduce texture swaps. The VS2b schema should define an `atlas_group` field on catalogue rows that guides elrond's subset selection toward atlas-eligible packs. Hook: `metadata.json` schema extended with `atlas_group` field (VS2b ingest pipeline task).

5. **Character-animation track (Slot B dash-trail + leap_strike arc):** physical archetype movement VFX is currently the caster-entity's sprite. VS2b per-embodiment rendering requires character-animation primitives (Mixamo / Spine rigs) to replace the sprite-translation. Slot B for physical archetypes is a character-animation concern, not a VFX-catalogue concern, and is fully out of scope for both Pimen subset selection and the current VS2a VFX integration.

---

*Section 2 authored by drax, 2026-05-17. Sections 1/3/4/5 pending gandalf.*

---

## Section 3 — Substrate-tag inventory + cross-vendor gap flagging (gandalf)

This section aggregates the substrate-tags Sections 1 and 4 surface together with the per-archetype slot surface from drax's Section 2; compares against the Pimen-9 baseline + Step B Tier-1 candidates + cipher-width-expanded substrate (per Option II forward-looking); flags coverage gaps that downstream dispatches must absorb (elrond Pimen subset selection; future catalogue-follow-on commissions).

### 3.1 Substrate-tag inventory the spec needs

The spec's VFX needs decompose along three orthogonal substrate-tag axes:

**Axis 1 — Canonical-7 element substrate (per `grouping-layer-vocabulary.md` v1.2):**

`fire / water / earth / wind / lightning / holy / shadow`

Plus the foundation:

`impact / physical`

Per `style-register.md` lock + `enemy-visual-legibility.md` S2 element palette-shift, every encounter type's VFX must support these 8 substrate identities at:
- cast-charge stage (drax Slot A; 8 substrate-tagged cast-charge VFX needed; `<element>-cast-charge` × 7 + `physical-cast-charge`)
- projectile / movement stage (drax Slot B, where applicable per skill archetype; 8 substrate-tagged projectile families)
- impact stage (drax Slot C; 8 substrate-tagged impact-burst VFX needed)
- status-application stage (drax Slot D; status-effect attachment moment; 8 substrate-tagged or substrate-modulated)
- status-ambient stage (drax Slot E; persistent status visual; 8 substrate-tagged or substrate-modulated)
- ambient-aura stage (tier-aura class per `enemy-visual-legibility.md` S3, modulated by element-palette)

**Axis 2 — Mechanic-family substrate-tags (per `2026-05-16-gandalf-step-b-gate3-review.md` § B.3 Gap 2 extension):**

`buff-debuff-status / ambient-environmental / smoke-dust / impact-burst / projectile-bullet / melee-slash / heal / movement-displacement / reactive-defensive / cast-prep-sustained`

These 10 families (7 Pimen-derived + 3 Step-B-extension) are the mechanic-family axis. Each encounter type touches some subset; per-skill VFX (drax Section 2) determines which.

**Axis 3 — Tier-aura substrate-tags (per `enemy-visual-legibility.md` S3 `display_aura_tier` enum):**

`none / faint / standard / visible / strong / signature / cinematic`

Plus the pack-cluster variant (Section 1.4 R1 / `enemy-visual-legibility.md` S6 swarm-tier rendering).

### 3.2 Cross-vendor coverage map (substrate-tag × vendor)

The table below maps each substrate-tag against the catalogue's three coverage tiers (Pimen baseline; Step B Tier-1 candidates committed; cipher-width-expanded VS2b hypothesis).

**Axis 1 — Element substrate coverage:**

| Substrate-tag | Pimen-9 coverage | Step B Tier-1 coverage (post-crawl) | VS2b cipher-width-expanded hypothesis |
|---|---|---|---|
| **fire** | ✅ 3 packs (fire-spell-01 / fire-spell-02 / fire-spell-effect-3 paid bundle) | ✅ Frostwindz Fire Mage; CreativeKind fire-coded packs | ✅ Robust |
| **water** | ✅ 3 packs (water-spell-01 / water-spell-02 / water-spell-effect-03 paid) | ✅ CreativeKind Water spell sets | ✅ Robust |
| **earth** | ✅ 3 packs (earth-spell-01 / earth-spell-02 / earth-spell-effect-03 paid + Earth Elemental enemy) | ✅ CreativeKind Earth spell sets; Fellor crystal-substrate adjacent | ✅ Robust |
| **wind** | ✅ 3 packs (wind-spell-01 / wind-spell-02 / wind-spell-effect-03 paid) | ⚠ Sparse Tier-1 wind specialists (catalogue pre-inventory notes thin) | Robust if Tier-1 surfaces; gap if not |
| **lightning** | ✅ 3 packs (Pimen "thunder" element-tag = lightning per substrate-expansion-decision) | ✅ Frostwindz Starcaller (cosmic/stellar lightning-adjacent); 404'd at sweep — verify | ✅ Robust |
| **holy** | ⚠ 1 pack (Pimen "holy") + paid bundle constituent | ✅ Frostwindz Paladin holy/light pack (404'd at sweep — verify); CreativeKind potential | Robust if Tier-1 closes; gap if not |
| **shadow** | ⚠ 1 pack (Pimen "dark" = shadow per substrate-expansion-decision) + paid bundle constituent | ✅ Frostwindz Deathbringer / Dark Mage / Warlock (necrotic + dark-arcane); robust shadow-adjacent | ✅ Robust |
| **impact / physical** | ✅ Pimen Hit Spark + Battle VFX Projectile + pixel-battle-effects (CC-BY) + cutting-and-healing (CC-BY) | ✅ CodeManu 44-animation kinetic specialist; Frostwindz class-archetype slash coverage | ✅ Robust |

**Axis 2 — Mechanic-family coverage:**

| Mechanic-family substrate-tag | Pimen-9 coverage | Step B Tier-1 coverage (post-crawl) | Notes |
|---|---|---|---|
| **buff-debuff-status** | ✅ 9 packs (heaviest single Pimen family per pre-inventory § 2.8) | ✅ Cross-vendor coverage strong | Per Step B review § B.4: aura-vs-instant split flagged for post-Step-B revision |
| **ambient-environmental** | ✅ 4 packs | Partial Tier-1 coverage | Spec needs more aura-ambient at boss/Trial tier |
| **smoke-dust** | ✅ 5 packs | Partial Tier-1 coverage | Often used as transitional VFX |
| **impact-burst** | ✅ 3 packs (impact + explosion + hit-effect + muzzle-flash) | ✅✅ CodeManu specialist; Frostwindz class-archetype packs | Robust |
| **projectile-bullet** | ✅ 2 packs (projectile + bullet) | ✅ Cross-vendor | Robust |
| **melee-slash** | ✅ 2 packs (slash + thrust + cutting + smear) — but `slash/thrust/cutting` concentrated in CC-BY assets (attribution risk per pre-inventory § 4.6 + drax Section 2.5) | ✅✅ CodeManu + Frostwindz class-archetype packs close CC-BY-attribution risk | Robust at Tier-1 |
| **heal** | ⚠ 1 pack (heal + healing tags) — concentrated in CC-BY assets (per pre-inventory § 4.6) | ✅ Cross-vendor; need to verify Tier-1 explicit | Attribution-risk at Pimen-only; closes at Tier-1 |
| **movement-displacement** (NEW per Step B extension) | ❌ Pimen zero coverage (per pre-inventory § 4.2) | ⚠ Tier-1 partial — Frostwindz class-archetype dash/teleport may cover | **Gap at Pimen-only; flag for Tier-1 verify** |
| **reactive-defensive** (NEW) | ❌ Pimen zero coverage | ⚠ Tier-1 partial — Frostwindz Paladin/Knight aura/parry/block may cover | **Gap at Pimen-only; flag for Tier-1 verify** |
| **cast-prep-sustained** (NEW) | ❌ Pimen zero coverage (cast-charge VFX implied in spell packs but not standalone) | ⚠ Tier-1 partial — Frostwindz class-archetype cast-prep may cover | **Gap at Pimen-only; flag for Tier-1 verify; load-bearing for B13 dodge-mechanic telegraph teaching AND drax Slot A integration per § 2.2** |

**Axis 3 — Tier-aura coverage:**

| Tier-aura substrate-tag | Pimen-9 coverage | Step B Tier-1 coverage | Notes |
|---|---|---|---|
| **none** | N/A (no asset needed) | N/A | Baseline |
| **faint** (magic tier) | ⚠ Implicit in element-spell-effect packs (element-palette shimmer); no dedicated faint-aura asset | ⚠ Verify Tier-1 | Spec implies element-palette tint composition, not dedicated asset |
| **standard** (trash tier) | N/A | N/A | Baseline |
| **visible** (elite tier) | ⚠ Pimen ambient/environmental adjacent | ⚠ Verify Tier-1 — Frostwindz class-archetype auras candidate | Critical for elite-tier presence per § 1.2 |
| **strong** (mini-boss tier) | ❌ Pimen explicit zero | ✅ Frostwindz class-archetype + Pixogen aura coverage candidate | **Gap at Pimen-only** |
| **signature** (boss tier) | ❌ Pimen explicit zero | ⚠ Tier-1 likely surfaces; verify | **Gap at Pimen-only** |
| **cinematic** (act-boss / Trial tier) | ❌ Pimen explicit zero | ⚠ Tier-1 likely partial; cinematic-tier may require custom-asset commission | **Significant gap — see § 3.3 boss-cinematic flag** |
| **pack-cluster** (swarm pack rendering per S6) | ❌ Pimen explicit zero | ⚠ Tier-1 partial; aura-pack rendering may require composition | **Gap at Pimen-only; addressable via composition (drax pipeline composes element-tint + frame-loop)** |

### 3.3 Substrate-tag gaps flagged for downstream consumption

**Gap G1 — Movement-displacement / reactive-defensive / cast-prep-sustained substrates absent at Pimen-only.**

The three mechanic-families that the Step B Gate3 review pre-extended (per § B.3 Gap 2) are zero-covered by Pimen. The spec's Section 1 § 1.4 R3 continuity rule (cast-charge telegraph density growing monotonically with tier) is *load-bearing for B13 dodge-mechanic*, and the cast-prep-sustained substrate-tag is the asset axis that B13 narrow-slice depends on for ship. Drax Section 2.2 Slot A notes "Procedural acceptable for VS2a (radial glow Graphics object scaled to element color)" — this is the operational fallback while cast-prep-sustained Tier-1 coverage closes.

**Routing:** elrond Pimen subset selection dispatch should explicitly call out these three families as "must verify Tier-1 vendor coverage before VS2a ships." If Tier-1 coverage is partial, follow-on catalogue commission territory (post-VS2a; Stage A2 closeout).

**Gap G2 — Tier-aura coverage thin at strong/signature/cinematic tiers from Pimen-only.**

Pimen's catalogue covers VFX-as-skill-effect well but ships zero dedicated "monster passive aura" assets. The aura tiers required by `enemy-visual-legibility.md` S3 (visible / strong / signature / cinematic) need either Tier-1 vendor close OR composition strategy (drax pipeline composing element-tint + frame-loop for aura rendering on top of base monster sprite).

**Routing:** elrond + drax converge — does the catalogue ship dedicated aura assets at Tier-1 OR does drax compose? Spec is agnostic; both paths produce the required visual outcome; cost is in pipeline engineering vs asset acquisition.

**Gap G3 — Non-humanoid embodiment sprite coverage thin (per § 1.3 embodiment matrix).**

Pimen ships 1 character + 2 enemy assets total. The seven non-humanoid embodiments (slime / beast / dragonling / swarm / construct / spirit / plant) are each zero-or-near-zero at Pimen-only and partially-covered at Step B Tier-1 (mostly via beast-coded fantasy-skeleton-style assets; no slime/spirit/plant coverage at Tier-1 per the curated catalogue).

**Routing:** known gap per `style-register.md` § "What this locks operationally" — Legolas Mode B non-humanoid sprite commission is queued. The spec REFERENCES this gap; does not commission. Future catalogue-follow-on dispatch addresses.

**Gap G4 — Heal/healing + physical-impact/physical-slash CC-BY attribution risk.**

Per pre-inventory § 4.6 + drax Section 2.5: 100% of Pimen heal/healing coverage AND the only physical impact/slash assets in Pimen are CC-BY (attribution-required). If drax filter behavior excludes attribution-required for any reason, heal/healing/physical-slash/physical-impact mechanic coverage at Pimen-only drops to zero or collapses by 50%.

**Routing:** Tier-1 vendors close this risk if they ship heal/healing without attribution AND physical-impact without attribution (CodeManu 44-animation kinetic specialist is the strong candidate). elrond Pimen subset selection should not select-on heal/healing or physical-slash at Pimen-only without conscious attribution-acceptance OR Tier-1 acquisition decision.

**Gap G5 — Curation pruning opportunity (Pimen over-coverage).**

The Pimen catalogue ships 22 fragmented mechanic-leaning tags across 47 assets. Some are spec-irrelevant (e.g., character-sprite + enemy-sprite assets when the spec is VFX-only; smoke-only assets when spec needs primarily element/impact/aura). elrond's Pimen subset selection should *prune* — select 5-10 packs that maximally cover the spec's substrate-tag axes, not crawl-the-whole-catalogue-into-the-demo.

**Recommendation for elrond subset selection priority (gandalf design ordering):**

1. fire-spell-effect-3 (paid; high-fidelity; element-substrate; all of Slots A-E across fire)
2. water-spell-effect-03 (paid; high-fidelity; element-substrate)
3. earth-spell-effect-03 + Earth Elemental (paid; element + monster bundled; addresses Slot C + ambient + sprite-archetype)
4. wind-spell-effect-03 (paid; element-substrate)
5. mega-pack-elemental-spell-effects-02 OR mega-pack-elemental-spell-effects (bundle; multi-element coverage; cost-efficient acquisition path)
6. Pimen Hit Spark + Battle VFX Projectile (Slot C impact + Slot B projectile core for physical archetypes)
7. pixel-battle-effects (CC-BY; melee/slash; attribution-accepted if Tier-1 CodeManu acquisition gated)
8. Buff/debuff/status-effect packs subset (~2 packs sufficient for Slot D + Slot E coverage)

This is *gandalf's design ordering* — operational selection is elrond's call via their downstream dispatch; this list is the input.

**Gap G6 — Atlas-consolidation strategy gap (drax Section 2.9 hook).**

Drax Section 2.0 names "no more than 1 texture atlas per VFX slot per encounter if avoidable" as the optimization target for VS2b attribution pipeline. Drax Section 2.9 #4 surfaces this as VS2b atlas-consolidation work. **The spec's Section 3 substrate-tag inventory is the input to that consolidation** — packing element-substrate × Slot-A/B/C/D/E into atlas groups is exactly the substrate-tag × slot cross-product. Per-element atlas (e.g., one atlas for all fire VFX across A/B/C/D/E) is the natural consolidation target; per-slot atlas (one atlas for all impacts across elements) is the alternative.

**Routing:** elrond VS2b attribution-pipeline schema dispatch designs the `atlas_group` schema field per drax Section 2.9 #4; the substrate-tag × slot cross-product here is the input. Decision deferred to that schema dispatch.

### 3.4 Cipher-width forward-looking substrate-tags (VS2b hypothesis per Option II)

Section 4 forward-looking content (per Sub-decision C Option II) uses the canonical-7 substrate as the rendering target and DOES NOT pre-commit cipher-width to specific outcome. But if cipher-width-expanded outcome lands (post-Step B + elrond emergent-grouping analysis), the spec's substrate-tag inventory may need to grow.

**Hypothesized cipher-width expansion targets (parked per Section 5 Q4):**

- `necrotic` (Frostwindz Deathbringer/Blood Knight introduces evidence beyond shadow)
- `cosmic / stellar` (Frostwindz Starcaller introduces evidence)
- `void` (Pixogen distinct from shadow; spatial-absence register)
- `crystal` (Fellor introduces; per Step B Gate3 review § A.1 entry)
- `technology / arcane-machine` (Pixogen distinct from arcane; novel substrate)
- `time / warp` (Pipoya partial coverage; temporal substrate; PoE Temporal Chains genre-precedent)
- `poison / acid` (Pimen acid + Fellor poison; biological/chemical substrate distinct from shadow)
- `psychic / mental / dream` (per Step B Gate3 review § A.2.3: structurally absent at the catalogue layer; addressable at per-season vocabulary if seasons want it)

The spec **does not pre-commit** to any of these expanding cipher-width. Section 4 forward-looking content assumes canonical-7 + impact baseline; cipher-width-amendment-trigger conditions are parked in Section 5 Q4.

### 3.5 Section 3 — completion summary

| Metric | Value |
|---|---:|
| Substrate-tag axes enumerated | 3 (element / mechanic-family / tier-aura) |
| Element substrate-tags | 8 (canonical-7 + impact foundation) |
| Mechanic-family substrate-tags | 10 (7 Pimen-derived + 3 Step-B-extension) |
| Tier-aura substrate-tags | 8 (none/faint/standard/visible/strong/signature/cinematic + pack-cluster) |
| Cross-vendor coverage cells filled | 3 axis-tables × multiple vendors |
| Substrate-tag gaps flagged | 6 (G1-G6) |
| Cipher-width hypothesis substrate-tags parked | 8 (necrotic/cosmic/void/crystal/technology/time/poison/psychic) |

---

## Section 4 — Per-encounter scene-walkthroughs (gandalf; Option II forward-looking)

Per Sub-decision C Option II lock: per-encounter scene-walkthroughs for VS2a + VS2b forward-looking. Each walkthrough describes what the encounter *looks and feels like* in the rendered demo — VFX choreography, substrate-tag selection, drax Slot (A-F) sequencing, embodiment renderings (per Sub-decision B mix-mode), and amendment-trigger placeholders for post-Step-B sub-locks.

These walkthroughs are **the visual storyboards** for the encounter types. Drax's first VS2a integration consumes them as "what the gauntlet should look like when it ships," cross-referenced against drax's Section 2 slot taxonomy. Elrond's Pimen subset selection consumes them as "what substrate-tags Section 3 needs to deliver."

### 4.1 Walkthrough — Swarm encounter

**Encounter profile.** Player enters a room. 8-12 swarm units (PackProxy entity per gamora B10.2) cluster in the middle distance. Pack-cluster aura envelops the cluster — element-coded (Section 1.4 R1 element-palette consistency), single uniform color, *visible at room-clear distance* so the player reads "swarm threat" before melee engagement.

**Substrate-tag selection (canonical-7 element example: fire-coded swarm).**
- Tier-aura substrate-tag: **pack-cluster** (unified, fire-palette, low-frequency pulse animation)
- Per-unit silhouette: simple; 16-24px monster sprites for high-density rendering
- Per-unit element identity: implicit through cluster aura, NOT through per-unit palette-tint (would crowd visual field)

**VFX choreography during combat (mapped to drax Slot taxonomy):**
1. Player approaches; cluster aura intensifies subtly (drax pipeline: Slot E ambient-style sustained loop; aura-pulse-on-detection trigger locked to player-proximity event)
2. Pack engages; per-unit attacks fire (simple melee or projectile)
3. Per-unit Slot A (cast-charge): minimal or absent — swarm units don't telegraph individually; the pack-cluster aura IS the threat read
4. Per-unit Slot B (projectile, where applicable): visually small — 32×32 frame budget per unit; element-substrate-tagged projectile
5. Per-unit Slot C (impact): brief impact-burst at 4-6 frames; element-substrate-tagged; intentionally less elaborate than trash-tier impact to prevent visual chaos at density
6. Pack-shared status applications (rare; affixed swarms only): Slot D triggers cluster-wide aura-color-shift for 2-4 sec, then aura reverts to baseline
7. As swarm depletes (units die), cluster aura visibly thins (asset count of aura particles tied to surviving-unit count; drax pipeline composition with `aoeRings` or `auras` pool)
8. Last 1-2 units alive: cluster aura collapses to faint individual aura per surviving unit (per `enemy-visual-legibility.md` S6: pack collapses, transition to individual-trash rendering); allows the player to "clean up" without losing visual clarity

**Embodiment-axis rendering (per Sub-decision B mix-mode).**
- **Humanoid swarm** (default; chierit-derived simple humanoid sprite): standard rendering per above
- **Beast swarm** (skeleton-archetype Pimen; rat-pack genre-precedent): same rendering; beast silhouette substituted
- **Swarm embodiment** (hive-mind self-similar; per `embodiment-narrative-layer.md`): cluster aura BECOMES the entity-identity; per-unit silhouette even simpler — the swarm-form makes more visual sense than humanoid swarm
- **Other embodiments** (slime / plant / construct / etc.): generation-eligible but VFX-mapping requires non-humanoid sprite assets not curated at VS2a; defers to VS2b

**Per-substrate variant (canonical-7 walkthrough applies to each):**

| Element substrate | Pack-cluster aura signature | Per-unit attack VFX expectation |
|---|---|---|
| fire | Warm reds/oranges pulse; ember-particle accents | Quick melee with fire-trail; mini-fireball projectile |
| water | Blue/teal slow pulse; mist-particle accents | Splash-impact melee; water-bolt projectile |
| earth | Brown/ochre stable hum; dust-particle accents | Slam impact; pebble-projectile |
| wind | Pale-blue/white quick pulse; dust-streak accents | Air-slash melee; wind-bolt projectile |
| lightning | Yellow-white sharp pulse with arc-flicker; spark accents | Zap melee; lightning-bolt projectile |
| holy | Warm gold/white steady glow; light-shimmer accents | Light-strike melee; light-bolt projectile |
| shadow | Deep purple/black low pulse; void-particle accents | Drain-strike melee; shadow-bolt projectile |
| physical (no element) | Neutral grey/iron clinical pulse; no element accents | Pure-impact melee; arrow/dart projectile |

**Register-fence per UI surface application.** Damage numbers off swarm-pack render in canonical-7 substrate words ("fire 12"); status-effect labels render canonical-7-derived ("burning"); item drops from the pack carry per-season label register; flavor text on those items carries per-season vocabulary. No mixed register within any single block.

**Cinematic frame trigger.** None. Swarm is mob-density experience; encounter-banner sufficient.

**Amendment-trigger conditions (VS2b forward-looking per Option II).**
- IF cipher-width-expanded substrate lands (e.g., `necrotic` becomes a substrate slot): pack-cluster aura signature for necrotic-swarm is dark-purple-decay register; Frostwindz Deathbringer asset family supplies the visual evidence
- IF per-embodiment narrative-skin display (Stage 4 form-bias migration) lands: per-unit sprite rendering of slime-swarm / construct-swarm becomes scope-active; non-humanoid sprite assets required
- IF status-application cipher rendering at Stage 3 cipher-migration lands: status-effect label register on the pack shifts from canonical-7-derived to per-season-derived in flavor-text surfaces only (stats-block stays canonical-7 per the register-fence rule)

### 4.2 Walkthrough — Trash encounter

**Encounter profile.** Player enters a room. 1-3 trash-tier monsters scattered in the room. No pack-cluster aura (trash is per-unit threat read). Each unit reads as a *singular threat* — element-palette tint visible on the sprite; tier-aura class is `none` (baseline); name-banner is `standard`.

**Substrate-tag selection (canonical-7 element example: fire-coded trash).**
- Tier-aura substrate-tag: **none** baseline (silhouette + name-banner carry tier)
- Element substrate-tag: **fire** palette-tint applied to base sprite via Pixi.js tint operation
- Per-unit silhouette: standard 32-64px monster sprite (sprite-archetype tag per `enemy-visual-legibility.md` S1)

**VFX choreography during combat (mapped to drax Slot taxonomy):**
1. Player approaches; trash unit aggro-trigger fires; minimal pre-aggro VFX
2. Slot A (cast-charge): brief — 4-6 frames at 80ms each; visible but not dodge-demanding (per § 1.4 R3 continuity rule). For elemental mage trash, drax Section 2.2 Slot A "Procedural acceptable for VS2a (radial glow Graphics object scaled to element color)" — fits trash-tier perfectly without per-element catalogued cast-charge asset
3. Slot B (projectile, where applicable): substrate-tagged projectile asset (fire-bolt at 8-12 frames, element-coded)
4. Slot C (impact): standard impact-burst (substrate-tagged: `fire-impact` at 6-8 frames; front-loaded peak frame per drax Section 2.2 Slot C frame discipline)
5. Slot D (status-application, where the skill has one): brief status-application VFX (faint particle burst at impact)
6. Slot E (status-ambient): persists for status duration (simple looping element-coded particle, low frame count to avoid frame-rate cost at gauntlet density — per drax Section 2.2 Slot E performance discipline)
7. Trash unit dies: standard death animation; loot drops (canonical loot-drop VFX, currently demo1-default)

**Embodiment-axis rendering.**
- **Humanoid trash** (chierit-derived simple monster sprite): standard
- **Beast trash** (Pimen skeleton-archetype): well-supported
- **Slime trash**, **Spirit trash**, etc.: deferred to VS2b; curation drives at VS2a

**Per-substrate teaching role (per § 1.2 substrate teaching).** Trash encounter is where the player builds element-identity recognition. Same season; multiple seasons of trash; player learns "fire trash = warm-red palette + ember-particle + fire-bolt projectile" by the second encounter of season N. The teaching depends on **consistency**: ALL fire-trash in season N renders identically at the substrate-VFX level. Drax pipeline enforcement: substrate-tag → asset-family lookup is deterministic per season.

**Cinematic frame trigger.** None.

**Amendment-trigger conditions (VS2b forward-looking).**
- IF cipher-width-expanded substrate lands: trash-tier element-palette tint extends to new substrate slots; e.g., `crystal-trash` renders with gem-mineral element-palette
- IF Stage 4 per-embodiment narrative-skin display lands: trash-tier non-humanoid renderings unlock; sprite-archetype + element-palette compose
- IF B13 dodge-mechanic Stage A2 closeout lands: trash cast-charge VFX may extend windup slightly (still brief but more telegraph-readable for cast-prep teaching); Slot A register stays trash-tier

### 4.3 Walkthrough — Magic encounter

**Encounter profile.** Player enters a room. 1-3 magic-tier monsters — visually distinct from trash via faint shimmer aura (per `enemy-visual-legibility.md` S3 magic tier). Magic-tier monsters carry a prefix-style affix (Diablo II precedent): "Fire Burning" (status-application affix); "Quick" (movement speed affix); etc.

**Substrate-tag selection (canonical-7 element example: fire-coded magic; "Fire Burning" affix).**
- Tier-aura substrate-tag: **faint** (element-palette shimmer; low-frequency animation; sustained Slot-E-style loop)
- Element substrate-tag: fire (primary palette + aura coloring)
- Status-affix substrate-tag: status-application (burning); burning DoT visualizable on player-character post-hit (Slots D + E on player)
- Per-unit silhouette: standard 32-64px monster sprite, slightly upgraded animation density vs trash

**VFX choreography during combat (mapped to drax Slot taxonomy):**
1. Player approaches; magic unit's faint shimmer aura visible at engagement distance (Diablo II shipped this exact pattern — magic-tier monsters glow blue or pulse with their affix color)
2. Slot A (cast-charge): more elaborate than trash (8-12 frames; visible windup); element-coded
3. Slot B (projectile): carries element-substrate + secondary status-affix tint
4. Slot C (impact): element-coded impact-burst PLUS small status-application secondary VFX (small "burning" particle attaching to player)
5. Slot D (status-apply): brief status-application animation (Pimen `debuff` pack source per drax Section 2.2)
6. Slot E (status-ambient): persists on player (burning DoT animation; 4-6 frames looping; subtle but visible)
7. Magic unit's aura subtly intensifies during its own active-attack moments (pulse-on-cast pattern)

**Embodiment-axis rendering.** Same as trash but with the magic-tier shimmer aura applied; aura asset is element-coded composition (drax pipeline: aura-particle-system + element-tint).

**Per-substrate variant.** Each canonical-7 element has its faint-shimmer rendering target:

| Element | Shimmer signature |
|---|---|
| fire | Warm-red flickering ember-shimmer; brief duration, frequent recurrence |
| water | Blue-teal flowing-shimmer; gentle, steady |
| earth | Brown-ochre stable-shimmer; minimal animation, palette-coded |
| wind | Pale-blue dusty-shimmer; quick wisps |
| lightning | Yellow-white static-shimmer; brief sharp flicks |
| holy | Gold-white halo-shimmer; soft, steady |
| shadow | Purple-black void-shimmer; ominous, slow |

**Affix layering.** When the affix is element-mixed (e.g., a fire-monster with `Cold-Slowing` affix), the aura blends two element palettes; the affix-status-application uses the secondary element's substrate-tag.

**Register-fence application.** Affix names render in canonical-7-derived register at combat-text surfaces ("Fire Burning Goblin"); flavor on the affix (e.g., codex entry) renders in per-season vocabulary.

**Cinematic frame trigger.** None.

**Amendment-trigger conditions (VS2b forward-looking).**
- IF affix-on-monster substrate cipher-width expands: magic-tier affix vocabulary at LLM-visible surface shifts (per cipher migration); register-fence rule preserves stats-block at canonical-7
- IF status-application cipher renames at Stage 3 cipher: status-ambient particle name in player-facing surfaces (codex/flavor) becomes per-season-vocabulary; status-effect icon tooltip stays canonical-7

### 4.4 Walkthrough — Pack encounter

**Encounter profile.** Player enters a room. 1-3 monsters arranged geometrically (Diablo III pack-precedent: synchronous teleport, formation arrangement). Pack-shared visible aura links the units; pack-shared affix(es) carry distinct VFX signature(s).

**Substrate-tag selection (canonical-7 example: fire-pack with Vortex + Burning affixes).**
- Tier-aura substrate-tag: **visible** with pack-shared coloring (element + affix-coloring; per `enemy-visual-legibility.md` S3)
- Element substrate-tag: fire (primary)
- Affix substrate-tags: vortex (mechanic-family: ambient-environmental persistent area), burning (status-application)
- Per-unit silhouette: standard, but linked by aura visualization

**VFX choreography during combat (mapped to drax Slot taxonomy):**
1. Player approaches; pack-shared aura visible (single envelope around the geometric arrangement of units); slow synchronized pulse-pattern
2. Pack-coordinated cast moment fires: ALL units simultaneously trigger Slot A (cast-charge); cast-charge VFX is synchronized; Slot C impact lands as multi-source convergent burst
3. Vortex affix creates persistent area effect (ambient-environmental substrate-tag; element-coded fire-vortex; 12-24 frame loop; covers ~3×3 tile arena segment) — drax `aoeRings` or dedicated `vortexPulls` pool per `vfxPools`
4. Burning affix Slot D applies status to player on contact with vortex OR on direct hit; Slot E sustains burn ambient
5. Pack-shared aura intensifies during synchronous-cast; relaxes between moments
6. Killing one pack unit: pack-shared aura unchanged for remaining units (Diablo III precedent: rare-pack affixes persist while any unit alive); affix area-effects unchanged
7. Last pack unit dying: pack-shared aura collapses; remaining vortex-area-effect fades over 2-4 seconds

**Embodiment-axis rendering.** Same as trash/magic; pack-shared aura overlays atop per-unit sprite-archetype rendering.

**Affix-variety design framing.** Pack affixes are *the variety surface* — packs can ship 2-3 affix combinations (Vortex+Burning; Slowing+Pulling; Teleporting+Explosive). Each affix maps to a mechanic-family substrate-tag from Section 3 Axis 2; each affix VFX is asset-composition (drax pipeline: base mob + affix-aura + affix-effect-asset).

**Cinematic frame trigger.** None.

**Amendment-trigger conditions (VS2b forward-looking).**
- IF mechanic-family substrate-tag expansion lands (e.g., `movement-displacement` Step B extension): teleport-affix-coded packs get dedicated assets; pre-extension packs render via fallback impact-burst
- IF per-embodiment narrative-skin display lands: pack composition of non-humanoid forms (e.g., slime-swarm pack with crystallization affix) unlocks; requires non-humanoid sprite + element-palette composition

### 4.5 Walkthrough — Elite encounter

**Encounter profile.** Player enters a room. ONE elite-tier monster, prominently positioned (often central or guarding doorway). Visible element-coded aura; pronounced cast-charge VFX on signature attacks; elevated silhouette-detail.

**Substrate-tag selection (canonical-7 example: lightning-coded elite).**
- Tier-aura substrate-tag: **visible** (single-color, lightning-palette aura, distinct pulse-pattern; per `enemy-visual-legibility.md` S3)
- Element substrate-tag: lightning
- Per-unit silhouette: standard-to-detailed (`display_silhouette_complexity = standard or detailed`)
- Cast-prep-sustained substrate-tag: needed for elite signature cast-charge (load-bearing per Section 1.4 R3; mechanic-family from Step B extension; drax Section 2.2 Slot A primary consumer)

**VFX choreography during combat (mapped to drax Slot taxonomy):**
1. Player approaches; elite aura visible at room-clear distance; signals threat-arrival per § 1.2 elite diegetic load
2. Encounter-banner appears (per `enemy-visual-legibility.md` S5 elite name-banner class = colored text + tier icon); player reads tier + element + name; ~1 second on-screen
3. Elite engages; first attack: standard Slot A cast-charge (similar to magic tier but slightly more elaborate)
4. Second attack: SIGNATURE Slot A cast-charge — multi-stage windup (charge → focus → release); 16-24 frames at full density; element-coded; lightning-arcs-building or fire-orb-charging or similar substrate-tagged signature
5. Slot C signature impact: stronger impact-burst (16-frame cinematic-density); screen-edge tint (lightning-yellow flash on screen-corners) at high-magnitude hit
6. Slot D (status-application from elite attacks): carries elite-coded status-application VFX (distinct from trash status-application — brighter, longer, more deliberate)
7. Elite low-HP threshold: aura intensifies and color-shifts slightly (warning state); player reads "phase-shift incoming"
8. Slot F (skill-expired) optional: on high-cooldown elite signature attacks, brief cast-position flash signals signature is on cooldown (per drax Section 2.2 Slot F NPC-cooldown rationale)
9. Elite dies: stronger death-VFX; element-coded burst on death; loot drop with elite-tier rarity-visual signature

**Embodiment-axis rendering.**
- **Humanoid elite** (chierit-derived; the chierit Elementals are *exactly* elite-tier rendered sprites per Path A-prime per-slug scale lookup): default + well-supported
- **Beast elite**, etc.: deferred to VS2b; curation drives at VS2a; Frostwindz class-archetype packs candidate-Tier-1 partial coverage

**Per-substrate variant.** Each canonical-7 element has a signature-attack rendering target. Examples:
- fire elite: charge-the-flame-orb signature → release-as-massive-fireball impact
- lightning elite: gather-arc-static signature → release-as-chain-lightning impact
- shadow elite: coalesce-darkness signature → release-as-shadow-rending impact
- holy elite: gather-light signature → release-as-radiant-pillar impact
- (etc., per element)

**Telegraph-teaching role (per § 1.2 elite diegetic load).** The elite Slot A cast-charge is the FIRST encounter type where dodge cognition matters. The signature-attack windup VFX must be visually distinct enough that the player can read "this is the windup; I should dodge or interrupt" within the 16-24 frame budget. B13 narrow-slice's universal dodge mechanic depends on this; the Slot A signature IS the telegraph surface. **This binds Section 3 Gap G1 (cast-prep-sustained substrate coverage) to elite-tier ship.**

**Register-fence application.** Elite name banner (per `enemy-visual-legibility.md` S5 colored + tier icon) renders with element-substrate icon in canonical register; elite's flavor/lore reference in codex renders in per-season vocabulary.

**Cinematic frame trigger.** None at elite tier (encounter-banner suffices).

**Amendment-trigger conditions (VS2b forward-looking).**
- IF B13 Stage A2 closeout lands defensive mobility geometry expansion: elite Slot A signature density may extend further (more frames; clearer phase markers); same substrate-tag, more rendering density
- IF per-embodiment narrative-skin display lands: elite-tier slime / dragonling / spirit renderings unlock; substrate-tag composition with non-humanoid sprite-archetype
- IF cipher-width-expanded substrate lands (e.g., `crystal`, `void`): new element-coded elite signatures author per the new substrate's visual identity

### 4.6 Walkthrough — Mini-boss encounter

**Encounter profile.** Player approaches a sub-arena (often pre-Trial gating). Mini-boss monster centrally positioned; strong two-color aura; encounter-banner with mini-boss tier-flag; possible Spirit-Guide voice-line ("Be wary — this one has tested forms before"). Mini-boss is the gauntlet's *pre-Trial preview* — visually elevated above elite; cinematically a notch below boss/Trial.

**Substrate-tag selection (canonical-7 example: fire-coded mini-boss with secondary shadow flavor).**
- Tier-aura substrate-tag: **strong** (two-color: fire-primary + shadow-secondary; per `enemy-visual-legibility.md` S3 mini-boss possibly two-color)
- Element substrate-tag (primary): fire
- Element substrate-tag (secondary): shadow (flavors aura + carries signature-attack status-application)
- Per-unit silhouette: detailed-or-distinct (`display_silhouette_complexity = detailed or distinct`)
- Cast-prep-sustained substrate-tag: extended; multi-stage windup more pronounced than elite

**VFX choreography during combat (mapped to drax Slot taxonomy):**
1. Pre-encounter: room-edge transitions (drax: scene-transition VFX or screen-fade); player walks into mini-boss arena
2. Mini-boss aura visible from arena-entry; strong pulse-pattern; two-color rendering (fire + shadow-edge)
3. Encounter-banner with mini-boss tier-flag appears (per `enemy-visual-legibility.md` S5 colored + tier icon + tier-flag); Spirit Guide voice (1-2 sec) — optional
4. First attack: ELITE-equivalent Slot A signature attack; mini-boss carries elite-tier signature as baseline AND adds mini-boss-only variant
5. Mini-boss-only signature: multi-stage Slot A cast-charge with PHASE markers — initial windup → mid-cast warning particle (player should dodge NOW) → release. The phase markers are visually distinct: a brief pause + color-shift + secondary aura-pulse at the warning particle moment, then release
6. Slot C mini-boss-only impact: cinematic-tier impact-burst (20-frame density); camera-shake; screen-edge tint with element-coloring
7. Mid-fight aura-evolution: at mid-HP, aura shifts (e.g., fire+shadow → fire+shadow+intensified-secondary); player reads "the fight is escalating"
8. Sub-phase mechanic (Reincarnated mini-bosses often carry one sub-phase): triggered at HP-threshold; mini-boss casts a phase-transition VFX (asset: cinematic-tier phase-transition; signature-pulse animation); arena dynamic shifts
9. Mini-boss dies: cinematic death-VFX (16-24 frames; element-coded multi-burst); elite-tier-plus loot drop; possible Spirit Guide voice-line ("Add this one to your record" or similar)

**Embodiment-axis rendering.**
- **Humanoid mini-boss**: chierit-derived; mini-boss tier scale per Path A-prime (200 px rendered midpoint); well-supported
- **Beast mini-boss**: Pimen skeleton-archetype scaled; partial support
- **Dragonling mini-boss**: deferred to VS2b; dragonling-class-fantasy precedent shipped in Slime franchise + Drifting Dragons; non-humanoid asset gap at VS2a

**Per-substrate variant.** Each canonical-7 element has a mini-boss-signature rendering target. The two-color aura always pairs primary + secondary (per `enemy-visual-legibility.md` S3); pairing combinations like fire+shadow, water+holy, earth+wind, lightning+impact, etc. The secondary signals flavor / status-affinity / sub-cosmology depending on per-season cosmology context.

**Register-fence application.** Mini-boss name banner renders cinematic text with element-substrate icon; mini-boss flavor / codex renders in per-season vocabulary; Spirit Guide voice-line uses per-season vocabulary if the line references season-specific lore (per `embodiment-narrative-layer.md` speech-vocabulary section).

**Cinematic frame trigger.** OPTIONAL at mini-boss tier per § 1.1 table — encounter-banner only is the default; full cinematic pause is reserved for Trial encounter. Mini-boss could OPTIONALLY trigger a brief Spirit Guide voice + banner moment (1-2 seconds) without full screen-takeover.

**Amendment-trigger conditions (VS2b forward-looking).**
- IF per-embodiment narrative-skin display lands: non-humanoid mini-boss renderings unlock (slime/dragonling/spirit etc. at mini-boss tier); requires non-humanoid sprite + tier-coded scale
- IF cipher-width-expanded substrate lands: two-color aura combinations may pair canonical-7 with cipher-expanded slot (e.g., fire+crystal mini-boss); secondary substrate-tag composition expands
- IF Trial moment ritual lands (forthcoming `trial-moment-ritual.md`): mini-boss-as-pre-Trial-preview gets formalized as a specific ritual shape; spec section gets cross-referenced
- IF boss-cinematic asset register option (b) lands per `enemy-visual-legibility.md` Q4: per-season cinematic-aura set covers mini-boss tier too

### 4.7 Walkthrough — Boss / Trial encounter

**Encounter profile.** Act-culmination. Player approaches the Trial arena. The arena itself has cinematic visual treatment (per-season aura at room-edge; per-season environment tile-set; signature ambient-environmental VFX). Trial encounter triggers the Trial moment ritual: pause-the-game cinematic frame → full LLM-name banner at cinematic-banner scale → Spirit Guide leans in with one contextual voice line → Body-swap/Mirror choice screen surfaces.

**Substrate-tag selection (canonical-7 example: holy-coded Trial boss; "Lantern-Keeper of Yomi's Winds" name per generation).**
- Tier-aura substrate-tag: **cinematic** (signature aura, often pulsing or animated; screen-edge tint; distinctive shape; per `enemy-visual-legibility.md` S3)
- Element substrate-tag (primary): holy
- Element substrate-tag (secondary, where applicable): per Trial boss's converged class fantasy
- Per-unit silhouette: distinct (`display_silhouette_complexity = distinct`)
- Cinematic-frame VFX: full screen-takeover at encounter trigger
- Trial-boss cloak overlay (per `enemy-visual-legibility.md` S4): distinctive aura + silhouette enhancement applied on top of base archetype-sprite

**VFX choreography during combat — Pre-encounter ritual (mapped to drax Slot taxonomy):**
1. Pre-arena: room-transition VFX with cinematic-tier signature (screen-fade, element-edge-glow, ambient soundscape if audio shipped); Spirit Guide voice-line builds anticipation
2. Player enters Trial arena; environmental VFX renders (per-season environment tile-set with ambient-environmental aura; e.g., Yomi-season Trial = pomegranate-tree silhouette + wind-shifted ambient particles)
3. Trial boss revealed; cinematic-tier signature aura visible immediately at room-clear distance (sustained Slot E-class ambient aura at boss-tier intensity)
4. Trial moment ritual fires (per `enemy-visual-legibility.md` S4 + `court-of-forms.md` C5):
   - Pause-the-game: combat suspends; player input locked
   - Cinematic frame: narrative-moment-tier fidelity (per `style-register.md` § "Narrative-moment tier") full-screen frame; LLM-generated cinematic-frame asset OR LLM-image-generated bespoke per Trial
   - Trial-boss name banner: cinematic-banner scale (large text; element + season-flavor coloring)
   - Spirit Guide voice: 1-2 sec contextual line referencing the player's specific class build + the Trial boss's flavor
   - Choice screen surfaces: Body-swap path OR Mirror path (per `cosmology-reincarnated.md` § Trial Path); player chooses
5. Combat resumes (after choice); from this point forward, the Trial boss is rendered per the chosen path:
   - **Body-swap path**: Trial boss renders as the LLM-generated class (sprite-archetype-tagged per the Trial boss class; cinematic aura + cloak overlay applied)
   - **Mirror path**: Trial boss renders as the PLAYER'S current class/sprite (per `enemy-visual-legibility.md` S7 Mirror exception); recognition-coded subtle cues per cosmology doc

**VFX choreography during combat — Active combat (mapped to drax Slot taxonomy):**
1. Trial boss multi-attack rotation; Slot A signature attacks at cinematic-tier density
2. Each signature attack: Slot A cast-charge with explicit phase markers (matches mini-boss + extends); Slot C cinematic impact-burst; camera-shake significant; screen-edge tint sustained for 0.5-1 sec
3. Phase-transition (Trial bosses typically 2-3 phases): cinematic phase-transition VFX (asset: dedicated cinematic-phase-transition; element-coded multi-burst with screen-takeover-flash)
4. Mid-phase aura evolution: cinematic aura color-shifts and shape-shifts per phase; arena environment may dynamically shift (drax pipeline: per-phase arena VFX overlay)
5. Trial boss low-HP: pre-death VFX (gathering-energy signature; ominous aura intensification; possibly Spirit Guide voice if narrative beat warrants)
6. Trial boss dies: cinematic death-VFX (24+ frames; element-coded multi-burst; screen-takeover-flash; possible cinematic frame for the ascension moment if Body-swap path was chosen)
7. Post-combat: ascension cinematic frame (per `court-of-forms.md` C5 commemorated-event pattern; Court accumulation moment); narrative-moment-tier fidelity

**Embodiment-axis rendering.**
- **Humanoid Trial boss**: chierit-derived + element-coded; tier scale per Path A-prime (370 px rendered midpoint); well-supported
- **Non-humanoid Trial boss** (per Sub-decision B mix-mode): generation-eligible; curation-likely at VS2a low-medium; well-suited for VS2b once non-humanoid sprite assets land via Legolas Mode B commission

**Per-substrate variant — Cinematic aura signature.** Each canonical-7 element has its cinematic-tier signature (per `enemy-visual-legibility.md` Q4 option (b) recommendation: per-season cinematic-aura set; three signatures per season honoring three act-end bosses):
- fire Trial: blazing-corona signature with screen-edge ember-tint
- water Trial: depth-of-ocean signature with screen-edge wave-tint
- earth Trial: stone-stability signature with screen-edge mineral-tint
- wind Trial: rushing-currents signature with screen-edge atmospheric-tint
- lightning Trial: storm-crowning signature with screen-edge static-tint
- holy Trial: pillar-of-light signature with screen-edge radiance-tint
- shadow Trial: enveloping-darkness signature with screen-edge void-tint

The signatures are *per-season-modulated* — the season's cosmology shapes the rendering. A Yomi-themed wind Trial boss reads with rushing-current signature flavored by Yomi's threshold cosmology (pomegranate-petal-wind particles, threshold-coded color-modulation, etc.). The substrate-tag is wind; the cinematic rendering layers per-season-flavor on top.

**Register-fence application.** Trial boss name banner: cinematic text with element-substrate icon at canonical register; Spirit Guide voice-line uses per-season vocabulary (Yomi season uses threshold/pomegranate/winter-king vocabulary; never uses canonical-7 substrate words like "wind" or "holy" in the line); choice screen UI uses canonical-register at the action labels ("Body-swap" / "Mirror") and per-season flavor at the descriptive prose; post-combat ascension cinematic uses per-season vocabulary in the dialogue + canonical at the mechanical "ascension confirmed" UI.

**Cinematic frame trigger.** YES — full Trial moment ritual.

**Amendment-trigger conditions (VS2b forward-looking).**
- IF Stage 4 per-embodiment narrative-skin display lands: non-humanoid Trial boss renderings unlock; slime / spirit / dragonling Trial bosses become curation-eligible at VS2b
- IF cipher-width-expanded substrate lands: cinematic-aura signature library expands; per-season cinematic-aura set covers new substrate slots (the Q4 option (b) approach scales naturally)
- IF Trial moment ritual doc (`trial-moment-ritual.md`) lands: ritual-specific VFX details get formalized; this section's ritual choreography becomes pointer-to-canonical-doc rather than load-bearing
- IF per-LLM-cinematic-frame image generation lands at star-lord (per `style-register.md` § "What this locks operationally" Star-lord directive): each Trial encounter gets bespoke LLM-generated cinematic frame asset; current state is asset-library-composed cinematic frames
- IF B14.5 Trial-boss convergence balance work refines tier mechanics: VFX presence may need to scale with refined difficulty curve; substrate-tag layer unchanged

### 4.8 Section 4 — completion summary

| Encounter type | Drax Slots referenced | VS2b amendment-triggers parked | Substrate-tags referenced |
|---|---|---:|---|
| Swarm | E (sustained pack-cluster); minimal A/B/C per-unit | 3 | element + tier-aura.pack-cluster + mechanic.ambient-environmental |
| Trash | A (procedural OK) / B / C / D / E | 3 | element + tier-aura.none |
| Magic | A / B / C / D / E (status-application + ambient on player) | 2 | element + tier-aura.faint + mechanic.buff-debuff-status |
| Pack | A (synchronized) / B / C / D / E + ambient-environmental affix area | 2 | element + tier-aura.visible + mechanic.ambient-environmental + mechanic.movement-displacement |
| Elite | A (signature) / C (cinematic-density) / D / E / F (optional) | 3 | element + tier-aura.visible + mechanic.cast-prep-sustained + mechanic.buff-debuff-status |
| Mini-boss | A (multi-stage signature) / C (cinematic) / phase-transition asset / D / E | 4 | element (primary + secondary) + tier-aura.strong + mechanic.cast-prep-sustained |
| Boss / Trial | A (phase-marked signature) / C (cinematic) / cinematic-frame asset / Trial-cloak / E (boss-tier ambient) | 5 | element (primary + season-flavor) + tier-aura.cinematic + mechanic.cast-prep-sustained + Trial-cloak overlay |
| **TOTAL** | **All 6 drax slots used across 7 encounter types** | **22 amendment-triggers** | **8 substrate-tag axes referenced across walkthroughs** |

---

## Section 5 — Open questions surfaced by the spec (parking lot)

Per dispatch § "Section 5 — Open questions surfaced by the spec," the following surface from the authoring session but SHOULDN'T be resolved unilaterally. Each is tagged with downstream dispatch / Matt-decision dependency. Drax's Section 2 surfaces additional TODO(drax) items inline; those are tracked at drax pipeline; the questions below are spec-level.

### Q1 — Pimen subset selection: which 5-10 packs do VS2a's slots actually need?

**Source:** Section 3.3 Gap G5 + § 3.3 gandalf-design-ordering recommendation. **Dependency:** elrond downstream dispatch (Pimen subset selection). **Status:** OPEN. The 8-pack ordering in § 3.3 is *gandalf design input*; elrond owns operational selection with consumption-pipeline constraints (RAR-unpack effort, atlas-pad budget, file-format normalization, etc.).

**Decision-by:** before drax VS2a first-VFX integration ships (per knight-rider 4-step plan step 2).

### Q2 — VFX-attribution-pipeline schema: what does the manifest schema look like?

**Source:** the spec's substrate-tag → catalogue-asset mapping is currently implicit; the manifest formalization is downstream. Drax Section 2.9 #4 surfaces `atlas_group` schema field as a target VS2b extension. **Dependency:** elrond VS2b attribution-pipeline schema dispatch (per knight-rider 4-step plan step 3). **Status:** OPEN. This spec feeds substrate-tag inventory + slot-cross-product (Section 3 Gap G6) but does not pre-design the schema.

**Decision-by:** after VS2a ad-hoc integration produces friction findings; elrond's schema absorbs those findings.

### Q3 — Per-embodiment rendering decisions: which embodiments ship at VS2a, in what scenes, with what asset support?

**Source:** Sub-decision B mix-mode lock + § 1.3 embodiment matrix. **Dependency:** Matt + curation decision (per Sub-decision B's "curation selects" framing); elrond + drax converge on what assets are operationally consumable at VS2a. **Status:** OPEN. The spec authors against generation-supported mix-mode; what ships is curation's call.

**Decision-by:** before each VS2a-eligible season closes for curation; ~per-season rolling decision.

### Q4 — Cipher-width amendment-trigger conditions: when does the spec need updating per post-Step-B sub-lock resolutions?

**Source:** Section 3.4 cipher-width forward-looking hypotheses + § 4 walkthroughs' amendment-trigger placeholders. **Dependency:** Step B Tier-1 crawl completion + elrond emergent-grouping analysis + the four catalogue-track sub-locks (cipher-width / Foundation / D1 / per-season vocabulary coupling) resolving. **Status:** PARKED per § 5.3 of `form-bias-cadence-strategy.md`.

**Amendment trigger conditions:**

| Trigger | Spec section affected | Update scope |
|---|---|---|
| Cipher-width Option A / B / C resolves to NOT canonical-7 | Sections 3.1, 3.4, 4 | Add new substrate-tag rows; update per-substrate walkthrough variants; preserve canonical-7 fallback |
| Mechanic-family substrate-tag extension lands (movement-displacement / reactive-defensive / cast-prep-sustained verified at Tier-1) | Section 3.2 Axis 2; Section 4 elite/mini-boss/boss walkthroughs | Update mechanic-family cells; promote cast-prep-sustained from "gap" to "covered" if true |
| Per-embodiment narrative-skin display lands (Stage 4 form-bias migration) | Section 1.3 + Section 4 embodiment-axis renderings; drax Section 2.9 #1 per-embodiment impact skins | Update embodiment matrix; promote non-humanoid renderings from "deferred to VS2b" to "active" |
| Status-application cipher renames at Stage 3 | Section 4 register-fence applications + status-application walkthroughs | Re-confirm per-status-effect register: canonical-7-derived stays at combat-text; per-season flavor stays at codex |

**Decision-by:** rolling per catalogue-track milestone closes.

### Q5 — Status-effect register canonicalization (canonical-7 extensions)

**Source:** gandalf v1.10 advisory § "Completion record" footnote — *"holy = 'blessed'? 'consecrated'? shadow = 'shrouded'? 'withered'? lightning = 'shocked' already canonical."* **Dependency:** gandalf design-call + drax UI integration. **Status:** OPEN.

The register-fence rule above lists status-effect-labels as canonical-7-derived. The canonical-7-derived status vocabulary needs explicit lock for the substrates from canonical-7 expansion:

**Recommendation (gandalf design call; pending Matt confirmation):**

| Substrate | Canonical-7 status label |
|---|---|
| fire | **burning** (locked; genre-canonical) |
| water | **frozen** (locked; genre-canonical) — water-as-cold uses "frozen"; water-as-water can also surface "drenched" / "soaked" for slow effects |
| earth | **rooted** (control-coded; genre-canonical) — earth-as-poison uses "poisoned" for ailment if substrate fully separated |
| wind | **dazed** OR **disoriented** (control-coded) — neither is genre-locked; gandalf-pick **dazed** for brevity |
| lightning | **shocked** (locked; genre-canonical; D2/D4 precedent) |
| holy | **consecrated** OR **blessed** — gandalf-pick **consecrated** (locked; D2/D4 holy-status-precedent for player-affecting holy) — holy-as-buff-on-self uses "blessed"; holy-as-debuff-on-enemy uses "consecrated" |
| shadow | **withered** OR **shrouded** — gandalf-pick **withered** (locked; D2 necromancer / D4 shadow-DoT precedent) — shadow-as-buff-on-self could use "veiled"; shadow-as-debuff uses "withered" |
| impact / physical | **stunned** (locked; genre-canonical for physical-CC) — physical-as-DoT uses "bleeding" for explicit blood-substrate |

**Decision-by:** drax VS2a UI integration consumes; lock at first integration.

### Q6 — Item-label generation lexical-distance rule (per v1.10 advisory follow-up flag)

**Source:** gandalf v1.10 advisory § "Completion record" — *"Per-season vocabulary's interaction with item-label generation needs a separate guard: item labels are typically 2-4 words and the boundary between 'derived label' and 'flavor text' is fuzzy; recommend the spec defines an explicit lexical-distance rule (item label may share per-season theme words but never the per-season substrate-replacement word)."* **Dependency:** gandalf + star-lord LLM-prompt construction. **Status:** OPEN.

**Recommendation (gandalf design proposal):**

> **Item-label generation rule:** item labels may echo per-season *theme* words (drawn from the season's cosmology) but MUST NOT include the per-season *substrate-replacement* word (the per-season vocabulary that ciphers to a canonical-7 substrate). E.g., for a "wind" season that uses "the Stream" as its substrate-replacement, item labels may use "currents", "breeze", "rushing" (theme echoes) but NOT "Stream" (substrate replacement). The substrate-replacement word lives in flavor text and naming-triad surfaces only.
>
> **Operational measure:** star-lord LLM-prompt construction for item-label generation: pass the per-season cosmological-theme vocabulary as *allowed* + the per-season substrate-replacement words as *forbidden* tokens. The LLM-pipeline is responsible for prompting around the substrate-replacement leak.

**Decision-by:** before star-lord per-season vocabulary generation Stage 3 lands (cipher migration).

### Q7 — Cinematic-frame asset register option (b) operationalization

**Source:** Section 4.7 Trial walkthrough + `enemy-visual-legibility.md` Q4 option (b) recommendation. **Dependency:** Matt + future LLM-image generation budget call + drax asset-pipeline integration. **Status:** OPEN.

The `enemy-visual-legibility.md` Q4 option (b) recommendation is *per-season cinematic-aura set (3 signatures per season, one per act-end boss)*. This produces ~3 LLM-image generations per season at Trial-cinematic-frame asset register; cost ~$0.30-1.50 per season at current LLM-image pricing.

**Decision-by:** before star-lord per-season LLM-image generation work begins (post-VS2b cipher migration; Stage A7 territory).

### Q8 — Per-encounter VFX timing / animation-frame-budget standardization

**Source:** Section 1.4 R3 continuity rule + drax Section 2 per-skill VFX slot enumeration + drax Section 2.4 timing-and-sequencing constraints. **Dependency:** drax pipeline engineering. **Status:** OPEN; drax owns.

The spec is asset-level granular; drax pipeline owns frame-rate normalization across encounter tiers (swarm fast cycles; trash standard; magic moderate; elite slower; mini-boss / boss / Trial cinematic). The 80ms-per-frame Pimen default vs CodeManu 100×100 vs CreativeKind density-density needs reconciliation at consumption time, not at spec time.

**Decision-by:** drax first VS2a integration; surfaces frame-budget findings as elrond pipeline-schema feedback.

### Q9 — Mirror-path VFX rendering specifics

**Source:** Section 4.7 Trial walkthrough Mirror-path branch + `enemy-visual-legibility.md` S7 Mirror exception. **Dependency:** drax + gandalf at Trial moment ritual doc landing. **Status:** OPEN.

The Mirror-path uses the PLAYER'S current sprite + recognition-coded subtle cues. Specifically how do those cues render? Candidate cues:
- Slight palette-shift toward an ominous register (saturation reduction + warm-tone-shift OR cool-tone-shift toward shadow)
- Mirrored animations (left-right reversal of player attack frames)
- Voice lines quoting player's recent build choices (per `cosmology-reincarnated.md` § "The Mirror"; star-lord LLM-call territory)
- Ambient aura with player's element-palette but darker

**Decision-by:** at `trial-moment-ritual.md` authoring; this spec parks.

### Q10 — VFX-asset acquisition pipeline + acquisition-decision authority

**Source:** Sections 3 + 4 reference asset families across Pimen + Step B Tier-1 + cipher-width-hypothesized; some packs are paid + some are CC-BY + some require Mode B crawls. **Dependency:** Matt + elrond + drax converge. **Status:** OPEN per ADR-006 (Matt-acquisition-decision territory).

**Decision-by:** rolling per catalogue-acquisition decision; outside this spec's scope.

### Q11 — Drax Section 2 follow-up TODOs

**Source:** Drax Section 2 surfaces multiple inline TODOs and forward-looking hooks. **Dependency:** drax pipeline. **Status:** TRACKED INLINE (Section 2). Surfacing here at spec level for downstream visibility:
- TODO(drax): dissipate-variant support in `spriteVfx` pool (Section 2.2 Slot E termination discipline; Section 2.4 Slot E termination)
- TODO(drax): releaseWithFade(frames) method on spriteVfx pool (Section 2.4)
- TODO(drax): particles layer split (`particlesGround` / `particlesMid` / `particlesOver`) — VS2a first-integration step 0 (Section 2.7)
- Section 2.9 forward-looking hooks: per-embodiment impact skins; releaseWithFade; atlas consolidation; character-animation track for physical archetype Slot B

**Decision-by:** drax B11 integration / VS2a first-VFX integration.

### Q12 — Spec amendment cadence post-VS2a + VS2b sub-lock resolutions

**Source:** This entire spec exists at the "before-VS2a-ships" snapshot. Many forward-looking placeholders will resolve over coming months. **Dependency:** knight-rider sequencing. **Status:** OPEN.

**Recommendation:** spec amendment lands as an append-block at first major sub-lock resolution (likely cipher-width landing) with full re-versioning + diff-record. Don't re-author from scratch; preserve archaeology of what was anticipated vs what landed.

**Decision-by:** when first significant amendment-trigger fires; knight-rider drafts amendment commission.

### 5.13 Section 5 — completion summary

| Metric | Value |
|---|---:|
| Open questions parked | 12 (Q1-Q12) |
| Downstream-dispatch-dependent | 5 (Q1, Q2, Q4, Q6, Q11) |
| Matt-decision-dependent | 4 (Q3, Q7, Q10, Q12) |
| Gandalf/Drax-design-dependent | 3 (Q5, Q8, Q9) |

---

## Spec-level completion summary

| Section | Author | Status |
|---|---|---|
| Header + register-fence top-level rule | gandalf | LANDED |
| Section 1 — Encounter-type inventory | gandalf | LANDED |
| Section 2 — Per-skill VFX slots | drax | LANDED |
| Section 3 — Substrate-tag inventory + gaps | gandalf | LANDED |
| Section 4 — Per-encounter walkthroughs | gandalf | LANDED |
| Section 5 — Open questions | gandalf (with drax TODOs tracked at Q11) | LANDED |

**Cross-references for knight-rider follow-up:**
- The register-fence top-level rule (§ "Top-level binding authoring discipline") deserves its own decisions-log entry — its authority extends across the project, not just VFX-spec scope. Recommend knight-rider drafts a decisions-log entry capturing the rule (per ADR-002 cross-seam authority).
- Section 3.3 gap G1 (cast-prep-sustained substrate-tag) is *load-bearing for B13 narrow-slice* dodge-mechanic telegraph teaching AND drax Section 2.2 Slot A integration. Verify Tier-1 vendor coverage closes the gap before VS2a ships; otherwise queue follow-on commission.
- Section 4 Trial walkthrough's Trial moment ritual choreography is rich enough to inform `trial-moment-ritual.md` authoring (Phase 2 work queue item #5); cross-pollinate when that doc lands.
- Drax Section 2.5 + Section 3 Gap G4 jointly raise the **physical-impact / physical-slash + heal/healing CC-BY attribution risk** — load-bearing for B11 physical-archetype integration. CodeManu acquisition is the primary close-path; bring to Matt acquisition-decision when commissioning.

---

## Maintenance protocol

When spec amendments land (per Q4 + Q12 + Q11 close):

1. Append new sections under a clear amendment heading; preserve original spec content
2. Update Section 3 substrate-tag inventory with new substrate-tags
3. Update Section 4 walkthroughs with cipher-width-expanded variants
4. Update Section 5 open-question list — close resolved questions; surface new ones
5. Maintain the register-fence top-level rule's authority across amendments

When downstream dispatches consume:

1. elrond Pimen subset selection (Q1): read Section 3.3 gandalf-design-ordering input
2. elrond VS2b attribution-pipeline schema (Q2): read Section 4 walkthroughs as schema-shape input; cross-reference drax Section 2.9 hooks
3. drax VS2a first VFX integration: read Sections 1 + 2 + 3.5 + 4 + register-fence rule

When new canonical-story docs touch VFX presentation:

1. Cross-reference this spec
2. Defer to the register-fence top-level rule on register-mixing decisions
3. Defer to Section 1's encounter-type inventory + Section 4 walkthroughs on per-encounter VFX presence

---

## Completion record

**Completed:** 2026-05-17 (joint gandalf + drax authoring session per dispatch ACTIVATED Matt L3 ~19:30 EDT)

**Spec path:** `canonical/story/vs2a-vfx-scene-needs.md`

**Encounter types enumerated:** 7 (swarm / trash / magic / pack / elite / mini-boss / boss / Trial — 7 types with Trial collapsed under boss tier per gauntlet structure)

**VFX slots enumerated (drax):** 6 canonical (A cast-charge / B projectile-movement / C impact / D status-application / E status-ambient / F skill-expired)

**Substrate-tag inventory size:** 3 axes × 26 tags total (8 element + 10 mechanic-family + 8 tier-aura)

**Gaps flagged (count):** 6 (G1-G6: cast-prep-sustained absent at Pimen-only; tier-aura strong/signature/cinematic thin; non-humanoid embodiment sprite gap; CC-BY attribution risk for physical/heal; Pimen-curation pruning opportunity; atlas-consolidation schema gap)

**Section 4 (VS2b forward-looking) status:** INCLUDED (per Sub-decision C = Option II); 22 amendment-trigger conditions parked across 7 walkthroughs

**Open questions parked (count):** 12 (Q1-Q12) — 5 downstream-dispatch-dependent / 4 Matt-decision-dependent / 3 gandalf-drax-design-dependent

**Notes for knight-rider:**
1. **Register-fence top-level rule** (§ "Top-level binding authoring discipline") deserves its own decisions-log entry per ADR-002. Authority is broader than this spec — covers all VS2a+ player-facing content regardless of cipher migration timing.
2. **Gap G1 cast-prep-sustained** is load-bearing for B13 dodge-mechanic + drax Slot A; verify Tier-1 vendor coverage before VS2a ships.
3. **CC-BY attribution risk** (Gap G4 + drax Section 2.5) requires Matt acquisition-decision input on CodeManu acquisition for physical-archetype VFX coverage close.
4. **Atlas-consolidation strategy** (Gap G6 + drax Section 2.9 #4) feeds elrond VS2b attribution-pipeline schema; substrate-tag × slot cross-product is the natural input.
5. **Race-condition discipline applied** per § 14.1.1: drax authored Section 2 first (~280 lines); gandalf integrated sections 1, 3, 4, 5 + top-level rule via explicit-path Edit operations against the existing file. No overwriting of drax's content. Pre-signal fetched origin before commit.

— gandalf, primary author of sections 1, 3, 4, 5 + top-level register-fence rule, 2026-05-17
— drax, secondary author of section 2 (parallel session), 2026-05-17
