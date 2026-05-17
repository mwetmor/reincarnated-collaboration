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
| **Hybrid mage** | `hybrid_mage` | `area_damage` (×2), `burst_damage` (×2), `damage_over_time`, `defensive`, `utility` | `nova_radial`, `nova_wave`, `aura_radial`, `beam_channel`, `projectile_straight` |

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
| **Applies to** | `projectile_straight` (mage/caster/hunter/rogue), `beam_channel` (hybrid_mage), `dash_attack` + `defensive_dash` (rogue/hunter/skirmisher). Does NOT apply to instant-delivery geometries (`impact_burst`, `nova_radial`, `ground_targeted_circle`). |
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

**beam_channel (hybrid_mage):**
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

## Section 4 — Per-encounter scene-walkthroughs (VS2b forward-looking, per Sub-decision C = Option II)

**(Pending — gandalf parallel session)**

---

## Section 5 — Open questions surfaced by the spec

**(Pending — gandalf parallel session; drax open questions embedded in Section 2 via TODO(drax) annotations and § 2.5 CC-BY gap note)**

---

## Completion record

**(To be filled in jointly on full spec completion)**

**Completed:**
**Spec path:**
**Encounter types enumerated:**
**VFX slots enumerated:**
**Substrate-tag inventory size:**
**Gaps flagged (count):**
**Section 4 (VS2b forward-looking) status:** included (per Sub-decision C = Option II)
**Open questions parked (count):**
**Notes for knight-rider:**
