# 31 — Reincarnated Engine Explainer: Future State (post-file-28 engine queue)

> **STATUS:** HISTORICAL-INFORMATIVE (pre-Epoch-4; consult for lineage only — not current truth) — see `canonical/00-ground-state.md` for current truth

**Captured:** 2026-05-11
**Last updated:** 2026-05-12 (consolidated additions section below; base content below preserved but partially superseded by Section 1-12 progression locks)
**Status:** Forward-looking projection of the engine as it will exist once file 28's engine queue is implemented. Represents the design synthesis from project conversations 2026-05-10/11/12. Treat as **target state**, not committed implementation.

This document describes **Engine 1 (Content Generation Engine) future state** after Track A engine maturation per file 29 completes. Engine 2 (World Generation Engine) is separately scoped in file 29 and not detailed here; companion future-Engine-2 explainer would be a separate document when that work begins.

For the **current state** (the engine as it ships with demo1 v1.2), see file 30.

---

## Locks added 2026-05-11/12 — consolidated supersession notes

Substantial design locks landed through 2026-05-11/12 via file 32 (progression-design, Sections 1-12) and file 33 (progression-skeleton). The base content of this doc was captured 2026-05-11 morning before those locks fully resolved. The below summarizes what's NEW or REVISED beyond this doc's base content; refer to file 32 + file 33 + file 28 for canonical detail:

### Act structure (LOCKED 2026-05-11)
- **3 acts per game** (supersedes any prior "4-6 acts" framing in this doc)
- Per-act level bands: A1: L1-17, A2: L18-33, A3: L34-50
- 1 Trial body-swap opportunity per act (3 per season)

### Geometry palette (LOCKED — extended beyond B11 25-count)
- B11 brings 16 → 25 active types (already in this doc)
- **B13 adds 5 defensive mobility geometries** (roll, defensive_dash, strafe_mode, blink, dodge_stance) bringing palette to **30 active types**
- Active-discrete-AOE: 7 → 16 (post-B11) → 21 (post-B13)
- See `09-geometry-palette-discussion.md` for canonical palette; file 28 § B11 + B13 for engine queue

### Multi-band convergence simulator B14 (LOCKED 2026-05-11; refined 2026-05-11)
- Option β: 3-band act-aligned discrete convergence at L17/L33/L50
- **9 convergence runs per class** (6 kit + variance + 3 doppelganger validation)
- Per-band gauntlet generation
- Per-band monster pools (separate flavor per band — matches genre's "5-15 new archetypes per act")
- Recompose-first failure handling
- Cost: ~30-45 min/season (was ~3-5 min)
- Spirit Guide consumes per-band optimal_distribution for cross-phase coaching
- See file 28 § B14; file 32 § Section 8

### Hierarchical Skill Tree (LOCKED 2026-05-11; B6 extension)
- Each class kit organized as TREE: 4 tiers × 2-4 chains
- Tier 1 (3-5 primaries) → Tier 2 (3-5 mids) → Tier 3 (2-4 advanced) → Tier 4 (1-3 keystones)
- Tier unlock thresholds: ≥3 ranks (T1→T2); ≥5 (T2→T3); ≥8 (T3→T4)
- Smooth rank cap per skill: `min(15, floor(level/3.33))` → L17 cap 5; L33 cap 10; L50 cap 15
- Cross-chain unlock asymmetry per element distribution: single-element classes strict same-chain; multi-element classes flexible cross-chain
- Tier-specific scaling coefficients: T1 1.05-1.08, T2 1.08-1.12, T3 1.12-1.18, T4 1.18-1.25
- Chain count variance allowed per class (specialists 2 chains × 4 tiers; generalists 4 chains × 3 tiers; asymmetric depths OK)
- See file 28 § B6 extension; file 32 § Section 4 Q4.3

### Body-swap mechanics (LOCKED 2026-05-11)
- Trial body-swap (full reward path) and Doppelganger path (refuse path) chosen UPFRONT at each Trial
- Body-swap pool = within-season generated classes (NOT cross-season library); pool shrinks by 1 per Trial OR Death body-swap
- Death body-swap: dying class permanently lost for season + cannot ascend
- Doppelganger fight = mirror of player's current class; partial reward (1/4 XP + half SP + half resistances); end-game quest reclaims the rest
- Only 1 form ascends per season (the one alive at end)
- See file 32 § Section 9 + Section 11; file 33 § "Body-swap pool dynamics"

### Per-act SP scaling + resistance system (LOCKED 2026-05-11)
- Per-act Trial body-swap SP: 4 / 7 / 9 = 20 total (matches B9b 100+20 budget)
- Per-Trial resistance bonus: +10% (body-swap path) / +5% (doppelganger path)
- Within-season resistance cap: +75% (gear must provide ~+45% to reach cap)
- XP grant per Trial: 50% / 75% / 100% of XP-to-next-level per band
- See file 32 § Section 11

### Gear progression (LOCKED 2026-05-11; B12 + B15)
- **10 final gear slots:** weapon / off-hand / head / chest / gloves / boots / belt / 2 rings / amulet
- Boots primary affix = +% movement speed; +25% gear cap
- **Seasonal Sets (B15):** one class-specific endgame set per playable class per season; L50-only drops; 2-piece / 4-piece / full-set bonuses
- Auto-pickup with rarity filter (mobile-first; common/uncommon auto-sell-to-gold; rare+ to inventory)
- Pet system parked as design intent (see `project_pet_system.md` memory)
- See file 28 § B12 + B15; file 32 § Section 5; file 33 § "Gear slots"

### Active mobility + telegraphs (LOCKED 2026-05-11; B13)
- 5 defensive mobility geometries (roll/defensive_dash/strafe_mode/blink/dodge_stance)
- Engine emits `cast_time`, `damage_resolution_time`, `i_frame_window` per skill
- Demo renders telegraphs with asymmetric indicator scaling (0.92× player / 1.08× enemy)
- Last Epoch per-class mobility model (NOT D4 universal Evade) — generator emits per archetype
- Archetype-emergence observability: kit-mobility composition surfaced in export packet
- See file 28 § B13; file 32 § Section 12.5

### Stat allocation (LOCKED 2026-05-11; Section 3)
- Auto-allocated per class identity (D3-style)
- No player stat allocation
- Stats do NOT drive movement speed
- AGI dead/reserved; do NOT revive for movement

### Earth Self meta-layer (DESIGN INTENT captured 2026-05-11)
- Reincarnated Phase 0 = SEASONAL JOURNEY portion of larger eventual game
- Earth Self = persistent player identity (far-future; not in current development)
- Form library = gacha-style accumulation of LLM-generated ascended spirits (≤1 per season)
- Eventual Earth events (PVP/PVE rift; gameplay loop TBD)
- Multiplayer scope: out of scope for seasonal play indefinitely; envisioned for Earth meta-layer events
- See `project_earth_meta_layer.md` memory + future `../collaboration-handoff/34-earth-meta-layer.md`

### Output packet schema (LOCKED additions)

Beyond this doc's base packet schema, the future packet includes:
- `convergence_report.endgame_L50` + `mid_band_L33` + `early_band_L17` + `variance_check_L50` + `doppelganger_validation` (per Section 8 telemetry lock)
- `kit_mobility_tag` per class: `none` / `offensive_only` / `defensive_only` / `mixed` (archetype-emergence observability)
- Per-class element_distribution (single vs multi) — locks cross-chain unlock rule for Hierarchical Skill Tree
- Per-skill `tier`, `chain_id`, `chain_position`, `parent_skill_ids` (tree structure)
- Per-skill `cast_time` + `damage_resolution_time` + `i_frame_window` (B13 metadata)
- Per-monster `movement_speed` + per-class `movement_speed` (B12)
- Per-class `seasonal_set` (B15): which slots in set, set bonuses at 2/4/full

### Cost projection update

- Per-season LLM cost: ~$5-10 (was ~$0.87 baseline)
- Per-band monster pool generation: ~3× monster LLM cost = ~+$1-2/season
- Seasonal set generation: ~25-36 LLM calls/season = ~+$1-2/season
- Convergence compute: ~30-45 min/season (was ~3-5 min)

---

## Base future-state content (2026-05-11 morning — partially superseded by above)

---

## TL;DR

The future-state engine produces ARPG seasons where **classes differ by COMPOSITION first, by NUMBERS last** — the "shaped balance" philosophy fully realized.

Where the current engine generates uniform-shaped class kits and uses a wide-range `damage_modifier` (0.05-1.94×) to balance them, the future engine generates kits with **enforced axis-level diversity** (geometry mix, element distribution, role coverage, AOE coverage) and uses `damage_modifier` only as a fine-tune lever in a tight range (~0.85-1.15).

Three new balance dimensions stack into the generation pipeline:

1. **Class kit composition** with per-archetype diversity rules (file 28 B6)
2. **Gear-percentile variance gate** rejecting pathological scaling at extreme gear (file 28 B7)
3. **Traits + skill point distribution** with leveled progression scaffolding (file 28 B9)

The balance loop tries each of these design-space dimensions BEFORE adjusting numeric modifier. Result: classes are mechanically distinct from each other AND characters within the same class can play very differently based on trait selection + skill point allocation.

The Spirit Guide extends from gear marginal-value analysis (Phase 5.5f, demo1 v1.0) to **build coaching** — recommends skill point allocations and trait choices using the same shaped-balance math the generator uses.

Generation cost projection: **~$1.50-2.50 per season** (up from ~$0.87 due to richer content: traits, skill tree branches, more skills per class, possibly legendary gear abilities). Balance loop convergence takes longer (~10-20 minutes per season) because it now explores design-space dimensions before falling back to numeric scaling.

---

## Level 1: System overview

### The generation pipeline (future)

```
Seed + Config
    ↓
[Anchor Selection]      ──→  130+-entry library; deterministic + history-aware
    ↓
[Element Flavors]       ──→  LLM substitution + QUALITY RUBRIC FILTER (B6/D1)
    ↓
[Archetype Selection]   ──→  Dimensional sampling per validity matrix
    ↓
[Kit Size Determination]──→  10-15 skills per class, archetype-appropriate
    ↓
[Kit Composition]       ──→  AXIS-AWARE DIVERSITY: element distribution + geometry
                              mix + AOE coverage + role coverage per archetype rules
    ↓
[Per-Skill Scaling]     ──→  Engine-determined scaling coefficients per skill
    ↓
[Trait Pool Generation] ──→  5-10 traits per class; varied acquisition floors;
                              endgame power calibrated to converge at level 50
    ↓
[Skill Point Optimization]→  Engine finds optimal 120-point distribution across kit
    ↓
[Balance Loop v2]       ──→  Tries kit recomposition + trait variation + scaling
                              re-roll BEFORE adjusting damage_modifier
    ↓
[Gear-Percentile Gate]  ──→  Variance check at 50th/75th/95th/99th percentiles;
                              reject pathological scaling
    ↓
[Monster Pool]          ──→  Per-tier + SWARM-TIER native generation (B4)
    ↓
[Gear Pool]             ──→  Now with LEGENDARY POWERS (B5): granted abilities,
                              auras, on-hit procs on legendary tier
    ↓
[Naming Pipeline]       ──→  Cascades benefit from richer inputs; trait names,
                              skill-with-element-variety names; lower collision rate
    ↓
[Telemetry/Export]      ──→  Includes trait pools, skill scaling coefficients,
                              recommended skill distribution per class
```

### The simulation layer (future)

Mostly unchanged from current state, with additions:

- **Per-skill geometry dimensions** (`range`, `half_angle`, `area_radius`) replace catch-all heuristics (B6/A2 integration)
- **Per-skill geometry parameters** (B11): `collision_mode` on lines, `angle_distribution` on multi_projectile, `sweep_shape` on melee_arc, `damage_falloff` (uniform/linear/exponential) on all radial geometries. Engine produces the hitbox/damage curve from these as source-of-truth; demo renderer consumes for VFX
- **Per-skill ailment chance scaling** (cost-based) replaces flat `BASE_AILMENT_CHANCE = 0.35` (B2)
- **Shield magnitude scaling** by WIS or damage_modifier (A4)
- **Legendary gear abilities** consumed (auras tick, on-hit procs fire, granted abilities equipped)
- **Knockback consumer** in sim (C2 — only if Path X / multi-target dispatch is committed)
- **Multi-target dispatch** (C1 — only if Path X is committed; required by `chain_lightning`/`ricochet_bounce`/`fork` to fully express; demo can approximate via splash, but engine-side is cleaner)

**Hitbox-vs-indicator asymmetry (B11 second-wave / post-B11 geometry extension):** engine emits hitbox as source of truth; demo renderer scales the visible indicator by a per-source asymmetry constant (player AOE indicator ~0.92× hitbox → edge catches feel generous; enemy AOE indicator ~1.08× hitbox → dodges feel narrow). Zero engine change; one VFX-layer parameter pair. Nests cleanly with `damage_falloff` (concentric rings naturally give a soft edge — inner = full damage, outer = falling damage). Requires telegraphed enemy AOE (B10-adjacent VFX polish) to be a meaningful pattern; parked until telegraphs ship.

### Spirit Guide as build coach (extends Phase 5.5f)

The Spirit Guide marginal-value system currently evaluates gear fit-for-class. Future state extends to:

- Recommend optimal skill point distribution from generator's "meta build" output
- Surface trait selection guidance (which traits to invest in / max first)
- Trigger free guided reset when player is "struggling" (simulation-average heuristic; cohort comparison if telemetry available)

UI surfacing follows the existing "Strong / Solid / Marginal / Sidegrade / Downgrade" categorical language for skill choices.

---

## Level 2: Pipeline stages in detail

### Stage 1 — Seasonal foundation (with quality filtering)

**Anchor selection** unchanged from current state — library lookup, deterministic from seed + history. Anchor selector duplicate detection bug fixed (D3).

**Element flavor substitution + QUALITY RUBRIC (D1)** — significant upgrade:

Current state: LLM proposes element flavors with no quality filter. Outputs like `milk` (water, season 1003) and `thrum` (wind, season 1001) land badly downstream — they don't visualize in combat or compound well in names.

Future state: rubric filters candidate elements before downstream cascade. Rubric scores candidates on:
- **Concreteness** — names a physical thing, not a process/abstraction
- **Visualizability** — player can imagine `X-bolt` or `X-armor`
- **Fantasy/heroic associative space** — fits ARPG genre vocabulary
- **Compound formation** — works in name templates ("Frost-Bone Ranger" yes; "Milk-Breath Cantor" no)
- **Combat-compatible connotations** — not soft/intimate/medical/domestic

Hybrid implementation:
- Allow-list of vetted candidates per canonical element (floor — known-good fallback)
- Scoring function on LLM-proposed candidates (primary path)
- If all candidates score below threshold, fall back to allow-list

### Stage 2 — Class generation (dimensional, unchanged at top level)

The validity matrix and dimensional axis selection remain as in current state. What changes is **what happens AFTER archetype selection** — specifically, the kit generation step (Stage 3).

### Stage 3 — Kit size determination (NEW per B6 + B9b)

Each archetype has a `kit_size_distribution` parameter — a tuple `(min, mode, max)` describing kit complexity:

| Archetype family | Kit size distribution | Feel |
|---|---|---|
| Simple casters (fire_mage, water_mage) | (10, 11, 12) | Approachable |
| Warriors, brutes | (10, 11, 12) | Direct |
| Standard archetypes (hunter, controller variants) | (12, 13, 13) | Genre baseline |
| Hybrid mages, multi-element specialists | (13, 14, 15) | Mastery-rewarding |

Generator samples kit size per class from this distribution. Becomes a balance lever: larger kits → more allocation choice at endgame → higher mastery ceiling.

### Stage 4 — Kit composition with axis-aware diversity (B6)

The core architectural change. Replaces current "sample each slot independently" with "compose kit such that diversity constraints are satisfied across axes."

**Constraint axes:**

**Element distribution.** Dominant + secondary model. Replaces single-element-per-class:
- Dominant element: 60% of kit (e.g., fire_mage → 60% fire skills)
- Secondary element: 30% (chosen from thematically-affined: fire↔wind, fire↔earth, NOT fire↔water)
- Tertiary element: 10% (occasional flavor)

Thematic affinity rules:
| Dominant | Allowed secondaries |
|---|---|
| fire | wind (combustion), earth (volcanic) |
| water | earth (mineral water, silt), wind (mist, storms) |
| earth | fire (volcanic), water (mud/clay) |
| wind | fire (combustion), water (mist) |
| physical | any |

**Geometry distribution.** Per-archetype rules:
- Each kit must have ≥3 distinct geometries (no same-geometry duplication unless intentional spam+spender pair)
- AOE coverage target per archetype (table below)
- Spam+spender pair exception: two skills can share geometry if they're a Diablo-style "low-cost build + high-cost spend" pair (e.g., Bone Spear + Bone Spirit)

**AOE coverage targets by archetype** (revised 2026-05-11 per genre research — Diablo / PoE clear-meta data):

| Archetype family | AOE share of kit |
|---|---|
| Controllers (fire/water/earth/wind) | 60-75% (heavy AOE; matches genre default) |
| Single-element mages | 40-55% (PoE/D4 elementalist standard) |
| Hunters, snipers | 20-30% (Lightning Arrow / Multishot / Tornado Shot are genre meta) |
| Warriors, brawlers, brutes | 40-50% (cleave + AOE spender standard) |
| Skirmishers, rogues | 25-35% (Whirlwind / Cyclone are skirmisher meta) |
| Hybrid mages | 65-80% (broadest area presence) |

**These shares require expanded geometry palette (B11) to fit kit-variety rules** — current 7-active-discrete-AOE palette is too narrow for heavy-AOE archetypes (controllers need 8-10 AOE slots from a 7-geometry pool). B11 expansion (scope locked 2026-05-11 evening after geometry-options review) brings active-discrete-AOE count from **7 → 16** via 9 new AOE-coded geometries:

| Bucket | Geometries |
|---|---|
| Un-defer (3) | `whirlwind`, `dash_attack`, `leap_strike` (consumability blockers retired by demo1 Phase 6 movement + Phase 12 VFX pack) |
| New multi-target dispatch (3) | `chain_lightning` (target-jumping), `ricochet_bounce` (bouncing), `fork` (split-on-impact) |
| New positional/radial (3) | `vortex_pull` (positional + AOE), `ring` (donut — proper Shock-Nova archetype), `multi_projectile` (radial burst — hunter/skirmisher AOE answer) |

**Parameter expansions on existing geometries** (cross-cutting; NOT new types — adopted to keep palette bounded while expanding expressivity):
- `line.collision_mode`: `stop_on_first` | `pierce_all` (piercing line — PoE Lightning Arrow)
- `multi_projectile.angle_distribution`: `spread` | `cardinal` | `diagonal` | `star` (cross/plus, X/diagonal, asterisk patterns)
- `melee_arc.sweep_shape`: `pie` | `crescent` (curved-band sweep variant)
- All radial geometries (`circle`, `ground_slam`, `ground_targeted_circle`, `ring`, `vortex_pull`, `aura`): `damage_falloff`: `uniform` | `linear` | `exponential` (proximity damage — clean "positioning matters" lever)

**Total palette: 16 → 25 active types.** Heavy-AOE archetypes (controllers, hybrid mages) draw 8-11 AOE slots from 16 active-discrete-AOE geometries — comfortable kit-variety headroom with no forced repeats. See file 28 § B11 for full rationale, skip-list (compound geometries, spiral, checkerboard, Pac-Man, tethered AOE, stack/spread marks — explicitly out of scope), and second-wave park list (trail, persistent_ring_animated, rotating_zone, telegraphed-enemy-AOE + asymmetric indicator scaling).

**Role coverage.** Each kit must include skills filling distinct roles (primary attack + burst + AOE + DoT + defensive + utility/ult). Roles enforce distinct functional purpose in player kit.

**Temporal pattern coverage.** Each kit should include a mix of:
- Instant (most skills)
- Channeled (1-2)
- Over-time / DoT (1-2)
- Delayed-trigger / charged (occasional)

**Effect category coverage.** Each kit should mix:
- Direct damage
- DoT
- Control (chill/root/silence/knockback)
- Heal/shield/buff
- (Self-only effects like self_buff don't double-count toward "buff" coverage)

### Stage 5 — Per-skill scaling coefficients (B9b)

Each skill receives an engine-determined `scaling_coefficient` for skill point investment:

| Skill role | Typical scaling coefficient |
|---|---|
| Primary attack (spammable) | 1.05-1.10 per point (low-power-investment) |
| Burst spender | 1.10-1.15 per point |
| AOE | 1.10-1.15 per point |
| Ultimate / heavy CD | 1.15-1.20 per point |
| Sustain / defensive | 1.05-1.10 per point |

Per-skill scaling becomes a balance lever — if a class doesn't converge, the engine can re-roll scaling coefficients on specific skills before falling back to damage_modifier.

**Cap per skill: 15 points** (hard cap, diminishing returns above).

### Stage 6 — Skill point distribution optimization (B9b)

Endgame budget: 120 points (2 × level 50 = 100 + 20 from quests/act-bosses).

**Math implication:** `120 / 15 = 8 fully-maxable skills`. Every kit size (10-15) forces meaningful endgame specialization.

| Kit size | Cap sum | Budget | Allocation shape |
|---|---|---|---|
| 10 skills | 150 | 120 | 8 maxed + 2 partial/zero |
| 12 skills | 180 | 120 | 8 maxed + 4 partial/zero |
| 15 skills | 225 | 120 | 8 maxed + 7 partial/zero |

**Engine optimization step:** for each class, the engine computes the OPTIMAL 120-point distribution by:
- Combinatorial search over distributions (with cap=15 constraint)
- Each candidate distribution simulated against the gauntlet
- Find the distribution producing 50% win rate at endgame (level 50, traits at max, gear at 75th percentile)

This is the **"meta build"** for the class — the engine-balanced optimal allocation. Player can use the meta or experiment with own distribution.

### Stage 7 — Trait pool generation (B9a)

Each class receives a trait pool of 5-10 traits, archetype-appropriate. Each trait has:

```
class Trait:
    name: str                       # LLM-generated, archetype-thematic
    effect: TraitEffect             # mechanical: +X% fire damage, etc.
    min_character_level: int        # acquisition floor: 1, 12, 25, or 38
    max_trait_level: int            # rank cap (1-4)
    endgame_value: float            # power at max rank (used for balance)
    power_curve: PowerCurve         # scaling formula from rank 1 → max
```

**Acquisition floor distribution** within a trait pool: typically a mix like 2 traits at floor 1, 2 at floor 12, 2 at floor 25, 1-2 at floor 38.

**Power-curve calibration:** higher-floor traits start more powerful AND ramp faster (less time before character level 50). The endgame target: all eligible traits reach similar power at level 50 — so a level-1-floor trait has 50 ranks of scaling vs a level-38 floor trait's 12 ranks; both reach similar value.

**Endgame baseline:** balance loop assumes all eligible traits at max rank.

### Stage 8 — Balance loop v2 (with design-space exploration)

The future balance loop:

```python
def converge_class_v2(cls, gauntlet, target_winrate=0.50, tolerance=0.05):
    # Initialize design state
    state = {
        'kit_composition': cls.initial_kit,
        'trait_pool': cls.initial_traits,
        'skill_scaling': cls.initial_scaling_coefs,
        'damage_modifier': 1.0,
    }
    
    for iteration in range(MAX_ITERATIONS_V2):  # higher than v1
        # Optimize skill point distribution given current state
        distribution = optimize_skill_distribution(cls, state, target_winrate)
        
        # Run convergence batch with all dimensions
        winrate = run_batch_v2(cls, gauntlet, state, distribution, n_fights=200,
                                gear_percentile=0.75)
        
        if abs(winrate - target_winrate) < tolerance:
            # CONVERGED — also run variance check (B7)
            variance_pass = check_gear_variance(cls, state, distribution,
                                                  percentiles=[0.50, 0.75, 0.95, 0.99])
            if variance_pass:
                return state, distribution
            else:
                # Pathological gear scaling; recompose
                state = recompose_for_variance(state)
                continue
        
        # Try design-space recomposition BEFORE damage_modifier:
        # Tier 1: re-roll skill scaling coefficients
        if iteration < MAX_SCALING_REROLLS:
            state['skill_scaling'] = reroll_scaling(state['skill_scaling'])
            continue
        
        # Tier 2: vary trait pool composition
        if iteration < MAX_TRAIT_REROLLS:
            state['trait_pool'] = revise_trait_pool(state['trait_pool'])
            continue
        
        # Tier 3: kit recomposition (within archetype/diversity rules)
        if iteration < MAX_KIT_REROLLS:
            state['kit_composition'] = recompose_kit(state['kit_composition'],
                                                      cls.archetype)
            continue
        
        # Tier 4: damage_modifier as LAST RESORT (tight range 0.85-1.15)
        if state['damage_modifier'] < 0.85 or state['damage_modifier'] > 1.15:
            return None  # reject class for regeneration
        state['damage_modifier'] *= (target_winrate / winrate) ** 0.5
    
    return None  # didn't converge across all dimensions
```

**Key changes from current:**
- Multiple design dimensions explored before falling back to damage_modifier
- damage_modifier constrained to ~0.85-1.15 (vs current 0.05-1.94)
- Gear variance check (B7) is a pass/fail gate AFTER convergence
- Failure to converge across all dimensions REJECTS the class for regeneration (vs current "stretch modifier to floor/ceiling")

### Stage 9 — Gear-percentile variance check (B7)

After damage_modifier convergence, run secondary check at multiple gear percentiles:

```python
def check_gear_variance(cls, state, distribution, percentiles):
    """Pass/fail: does this class scale smoothly across the gear distribution?"""
    
    dps_curve = {}
    for p in percentiles:
        winrate, avg_dps, ttk = run_batch_at_gear_percentile(cls, state, distribution,
                                                              gear_percentile=p, n_fights=50)
        dps_curve[p] = {'winrate': winrate, 'avg_dps': avg_dps, 'ttk': ttk}
    
    # Pathology checks
    if dps_curve[0.95]['avg_dps'] > 2.0 * dps_curve[0.75]['avg_dps']:
        return False  # flat-damage stacking pathology
    if dps_curve[0.99]['ttk'] < 0.3 * dps_curve[0.75]['ttk']:
        return False  # critical-damage stack break
    if dps_curve[0.95]['avg_dps'] / dps_curve[0.50]['avg_dps'] > 4.0:
        return False  # excessive variance across the distribution
    
    return True
```

Demo1's "hunter with 2× legendary flat-damage items feels OP" pattern would be caught here at generation time, not at playtest.

### Stage 10 — Monster pool with swarm tier + genre-aligned gauntlet (B4 + B10)

**Per-tier scaling** (revised 2026-05-11 per genre research):

| Tier | HP scale | Damage scale | AI tier | Count per room | Genre analog |
|---|---|---|---|---|---|
| swarm | 0.10× | 0.20× | simple-tier basic | 5-12 per pack | PoE white monsters; D3 trash |
| magic | 0.25× | 0.40× | simple | 1-3 per pack | PoE magic monsters |
| trash | 0.5× | 0.6× | simple | 1-2 per room | (mid threat baseline) |
| elite/rare | 1.5× | 1.2× | smart | 1 per elite room | PoE rare monsters; D3 elites |
| mini-boss | 4.0× | 2.0× | smart | 1 per mini-boss room | (rare reward gate) |
| boss | 8.0× | 3.0× | optimal | 1 per boss room | Map boss / Helltide boss |
| act-boss | 10×+ | 3.5× | optimal | 1v1 final encounter | Pinnacle boss / Uber boss |

**Gauntlet shape per act (B10)** — replaces current 7-wave linear structure:

| Room type | Count per act | Density | Clear-time target |
|---|---|---|---|
| Trash-pack room | ~6 | 8-15 swarm/magic mobs | 5-15s |
| Magic-pack room | ~2 | 1-3 magic + 5-8 swarm | 15-30s |
| Elite room | ~2 | 1 elite + 5-8 trash | 30-60s |
| Mini-boss room | ~1 | 1 mini-boss + 3-5 trash | 30-60s |
| Boss room | ~1 | 1 boss (1v1 cinematic) | 30-60s |
| Act-boss room | 1 (final) | 1 act-boss (1v1 cinematic) | 60-120s |

**Genre clear-rate target:** ~80-100 mobs per minute of clear in dense layouts (matches D3 GR / PoE meta).

**Key changes from prior projection:**
- Swarm tier scaling dropped from 0.15× HP / 0.25× damage to **0.10× / 0.20×** — matches "trash dies in 1-2 AOE hits" genre pattern
- Swarm count per pack rose from 3-5 to **5-12** — matches PoE pack scale
- Gauntlet structure shifts from 7-wave linear to **10-12 room generated act** with composition ~70% trash + ~20% magic/mid + ~10% elite+
- Boss fights stay 1v1 (genre convention preserved)

**Co-dependency:** B10 (this restructure), B6 (kit composition), B11 (expanded geometry palette — 16 → 25 types with 16 active-discrete-AOE), and B7 (gear variance check) must ship together. Landing in isolation creates architectural mismatch — e.g., B6 AOE shares without B10 density would push classes back toward single-target through convergence; B6+B10 without B11's geometry expansion would crunch heavy-AOE archetypes against limited geometry options; B11's parameter expansions (proximity damage falloff, piercing line, cardinal/star distributions, crescent sweep) ship as part of the same sprint to expand expressivity without further inflating palette type count.

### Stage 11 — Gear pool with legendary powers (B5)

Future legendaries carry mechanical novelty, not just stat-stick scaling:

```
class LegendaryItem(Item):  # extends current Item schema
    # ... existing power_score, fit_*, etc. ...
    granted_ability: Optional[Ability]    # weapon-only: 7th hotbar slot OR replace existing
    aura: Optional[AuraEffect]            # armor/shield: passive aura tick (regen, thorns, etc.)
    on_hit: Optional[OnHitEffect]         # weapon: chance proc (chill, burn, mini-AOE, etc.)
    cast_on_attack: Optional[Ability]     # weapon: deterministic Nth-attack trigger
```

Legendary tier becomes mechanically distinct from epic/rare/etc. — not just statistically larger. ARPG-genre-correct (D3 Legendaries, D4 Aspects, PoE Uniques, Last Epoch Uniques).

### Stage 12 — Naming pipeline (with richer inputs)

The naming pipeline is structurally unchanged from current state but benefits from B6's richer inputs:

- Skill names: each slot now has distinct element + geometry + role combinations, giving the LLM substrate to name distinctly. Collision rate drops as a side effect of generation-side diversity, not LLM-side dedup.
- Trait names: new layer of LLM calls (~5-10 per class) for thematic trait naming
- Element naming: rubric-filtered (D1) so awkward outputs like `milk`/`thrum` are rejected before downstream cascade

Cost projection: ~30% increase in LLM calls per season due to traits + slightly richer skill kits. Estimate: ~$1.50-2.50 per season (vs current ~$0.87).

### Stage 13 — Telemetry + export

Future packet adds:
- `trait_pool` per class (full structure with floors, levels, curves)
- `skill_scaling_coefficients` per class
- `optimal_skill_distribution` per class (the engine-computed "meta build")
- `kit_size_target` per class (the archetype kit size used)
- `convergence_iterations` reporting which dimensions were explored
- `gear_variance_report` (B7 pass/fail + per-percentile DPS curve)
- `swarm_tier_monsters` (separate from trash; explicitly tagged)

Telemetry infrastructure expands to support cohort comparison for Spirit Guide struggling detection (Phase 1 work; not yet specified). Anonymized per-player metrics would feed back to a backend for cohort analysis.

---

## Level 3: Math, code, iteration procedures (future state)

### Combat damage formula (mostly unchanged + per-skill geometry dims)

Future damage flow adds per-skill geometry dimensions for hit detection:

```python
# Per-skill geometry replaces catch-all heuristics
if skill.geometry == 'cone':
    targets_in_range = filter(lambda t: in_cone(attacker, t, skill.range, skill.half_angle), all_targets)
elif skill.geometry == 'line':
    targets_in_range = filter(lambda t: in_line(attacker, t, skill.range, skill.width), all_targets)
elif skill.geometry == 'circle' or skill.geometry == 'ground_targeted_circle':
    targets_in_range = filter(lambda t: in_radius(target_point, t, skill.area_radius), all_targets)
# ... etc per geometry
```

Demo's current 870px catch-all retires (file 28 A2 demo override removal).

### Skill point distribution optimization

The engine computes the optimal allocation by combinatorial search:

```python
def optimize_skill_distribution(cls, state, target_winrate=0.50):
    """Find the 120-point distribution that produces target_winrate at endgame."""
    
    skills = cls.kit
    budget = 120
    cap = 15
    
    # Generate candidate distributions (subset of compositions of budget into len(skills) bins)
    candidates = generate_distribution_candidates(budget, cap, len(skills))
    # In practice: directed search rather than exhaustive enumeration
    # — start from uniform-ish; greedy reallocation toward skills with high scaling_coefficient × usage_frequency
    
    best_dist = None
    best_winrate_distance = float('inf')
    
    for dist in candidates:
        winrate = run_batch_with_distribution(cls, state, dist, n_fights=30)
        distance = abs(winrate - target_winrate)
        if distance < best_winrate_distance:
            best_winrate_distance = distance
            best_dist = dist
    
    return best_dist
```

Output: the "meta build" — recorded in the export packet for Spirit Guide use during play.

### Trait power-curve calibration

For traits to "reach similar power at character level 50" across varied acquisition floors:

```python
def calibrate_trait_curve(min_level, max_trait_level, target_endgame_value):
    """Determine the per-rank scaling such that this trait reaches target at level 50."""
    
    char_levels_available = 50 - min_level
    rank_steps_available = max_trait_level  # typically 4 ranks
    
    # Step duration: every (char_levels_available / max_trait_level) character levels
    step_duration = char_levels_available / rank_steps_available
    
    # Power per rank: linear from base_value at rank 1 to target_endgame_value at rank 4
    # Higher-floor traits have higher base because they start more powerful
    base_value = target_endgame_value * (min_level / 50.0)  # higher floor → higher base
    rank_increment = (target_endgame_value - base_value) / (max_trait_level - 1)
    
    return {
        'rank_values': [base_value + rank_increment * i for i in range(max_trait_level)],
        'min_level': min_level,
        'step_duration': step_duration,
    }
```

A trait acquired at level 1 with max rank 4: base ~0.02 × endgame, scales gently over 50 levels.
A trait acquired at level 38 with max rank 4: base ~0.76 × endgame, scales sharply over 12 levels.
Both reach `target_endgame_value` at character level 50.

### Spirit Guide struggling-detection heuristic

```python
def is_struggling(player_state, sim_baseline, cohort_data=None):
    """Composite heuristic for triggering Spirit Guide intervention."""
    
    # Simulation-baseline check (Phase 0 — works immediately)
    encounter_time_ratio = player_state.current_clear_time / sim_baseline.predicted_clear_time
    if encounter_time_ratio > 1.5:
        cumulative_underperform_time += dt
    
    death_count_in_window = player_state.deaths_in_last(window=300)  # 5 min
    encounter_difficulty_weighted = player_state.recent_encounter_difficulty_weighted_deaths
    
    # Cohort check (Phase 1 — requires telemetry)
    if cohort_data is not None:
        player_xp_per_hour = player_state.xp_per_hour
        cohort_25th_percentile = cohort_data.xp_per_hour_p25_for_similar_build
        if player_xp_per_hour < cohort_25th_percentile:
            cumulative_underperform_time += dt
    
    # Composite trigger
    if (cumulative_underperform_time > 900 or  # 15 min underperformance in last hour
        death_count_in_window > 3 or
        encounter_difficulty_weighted > 2.0):
        return True
    
    return False
```

Cooldown: once-per-session Spirit Guide intervention unless explicitly dismissed and player continues struggling.

### Shield magnitude with scaling (A4 resolved)

Future shield formula (assuming HoT-style `damage_modifier` scaling — Option B from earlier discussion):

```python
elif name == "shield":
    magnitude = float(effect.params.get("magnitude", 0.0)) * attacker.damage_modifier
    duration = float(effect.params.get("duration_seconds", 5.0))
    attacker.active_effects.append(ActiveEffect(name="shield",
        params={"magnitude": magnitude}, duration_remaining=duration))
```

Alternative (heal-style WIS scaling — Option A):

```python
    shield_bonus = 1.0 + attacker.attribute_values.get("wisdom", 0) * 0.002
    magnitude = float(effect.params.get("magnitude", 0.0)) * shield_bonus
```

Engine team picks one when B-tier work begins; both restore engine-faithful symmetric scaling between heal and shield.

### Combo cost generator (A1 resolved)

Future generator clamps combo skill costs at pool_max:

```python
def generate_combo_skill_cost(skill_role, pool_max=5):
    """Combo costs clamped at pool_max - 1 (allow 'spend everything' as max)."""
    base_cost = sample_cost_for_role(skill_role)  # may emit higher
    return min(base_cost, pool_max)
```

Demo's `effectiveEnergyCost` override (currently `min(base, 5)` for combo classes) retires once engine emits compatible costs.

### Focus cost calibration (A1b resolved)

Future generator either:

**Option B (recommended):** raise `FOCUS_RESTORE_PER_SKILL` from 10 to 25 in engine:

```python
FOCUS_RESTORE_PER_SKILL = 25.0  # was 10.0
```

Or **Option A:** clamp focus skill costs at FOCUS_RESTORE_PER_SKILL:

```python
def generate_focus_skill_cost(skill_role, restore_per_skill=10):
    """Focus costs clamped to net positive at typical play rate."""
    base_cost = sample_cost_for_role(skill_role)
    return min(base_cost, restore_per_skill - 2)  # ~7 max cost, leaving net positive
```

Either restores focus class sustainability without demo overrides.

---

## Output packet schema (future state)

The exported JSON packet expands significantly:

```json
{
  "season_id": "001006",
  "anchor": { ... },
  "element_flavors": { ... },
  "classes": [
    {
      "class_id": "...",
      "name": "...",
      "archetype_tag": "...",
      "dominant_element": "fire",
      "secondary_elements": {"wind": 0.30, "earth": 0.10},
      "energy_type": "mana",
      "range_profile": "long",
      "role_orientation": "damage",
      "kit_size": 13,
      "skills": [
        {
          "skill_id": "...",
          "name": "...",
          "geometry": "cone",
          "element": "fire",
          "role": "burst_damage",
          "range": 600,
          "half_angle": 0.6,
          "area_radius": null,
          "energy_cost": 30,
          "cooldown_seconds": 8.0,
          "scaling_coefficient": 1.12,
          "max_invested_level": 15,
          "effects": [...]
        },
        ...
      ],
      "trait_pool": [
        {
          "trait_id": "...",
          "name": "...",
          "effect": { ... },
          "min_character_level": 1,
          "max_trait_level": 4,
          "endgame_value": 0.30,
          "power_curve": { ... }
        },
        ...
      ],
      "optimal_skill_distribution": {
        "skill_id_1": 15, "skill_id_2": 15, "skill_id_3": 12, "skill_id_4": 10,
        "skill_id_5": 10, "skill_id_6": 8, "skill_id_7": 5, ...
      },
      "damage_modifier": 1.04,
      "convergence_report": {
        "iterations": 23,
        "dimensions_explored": ["scaling", "traits", "kit"],
        "fell_back_to_modifier": false,
        "variance_check_passed": true
      }
    },
    ...
  ],
  "monsters_by_tier": { swarm: [...], trash: [...], ... },
  "gear_pool": [
    {
      "gear_id": "...",
      "tier": "legendary",
      "granted_ability": { ... },  // NEW for legendaries
      "aura": null,
      "on_hit": { "effect": "chill", "chance": 0.15, "magnitude": 0.30 },
      ...
    },
    ...
  ],
  "metadata": { ... }
}
```

## Generation cost projection

- Estimated ~$1.50-2.50 per season in LLM calls (up from ~$0.87)
- ~30% more LLM calls cumulative due to trait naming + slightly richer skill kits + possibly element-rubric re-rolls
- Balance loop convergence: 10-20 minutes per season (up from 3-5 min) due to design-space exploration
- Cost per game (incl. ~5 seasons of content for a player's full game): ~$10-15 in seasonal generation

## Cross-references

- **File 16:** project roadmap (tactical near-term)
- **File 28:** engine ARPG rebalance design (the queue this doc projects forward)
- **File 29:** Reincarnated architecture and game scope (strategic anchor)
- **File 30:** Engine explainer — current state (companion to this doc)
- **Memory `project_engine_state_findings.md`** — recurring lessons learned + finding history

## What this document is and isn't

**This is:** a target-state projection. What the engine WILL look like after Track A engine maturation completes. Useful as a reference when implementing file 28 items so the integrated end-state is held in mind.

**This is not:** a committed implementation. File 28 holds the actual work items; not all are pre-decided (B6 architectural details, trait curve calibration, etc., need engine-session design conversations).

**Update protocol:** as each file 28 item ships and reality lands, update this doc with what actually happened. Items that ship simpler than projected should be revised here. Items that ship different from the projection should be re-described.

**Companion doc (file 30):** describes the engine as it actually exists today. Compare side-by-side to see the gap between current and target.
