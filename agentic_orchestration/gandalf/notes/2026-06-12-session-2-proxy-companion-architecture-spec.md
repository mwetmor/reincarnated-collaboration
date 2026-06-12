# Session 2 — Proxy + Companion Architecture Spec

**STATUS:** DRAFT — Matt-authorized 2026-06-12 (Pattern B session, architecture cascade); locks after Session 1 ratification; gamora kernel handoff fires immediately on lock
**Author:** gandalf
**Date:** 2026-06-12
**Grounding docs:**
- `canonical/story/2026-05-31-hypothesis-flow-pattern-library-architecture.md` — PRIMARY source
- `agentic_orchestration/gandalf/notes/2026-06-12-session-1-t4-architecture-spec.md` — T4 catalog (prerequisite)
- `agentic_orchestration/gandalf/notes/2026-06-12-architecture-sessions-overview.md` — 5-session cascade
- Today's proxy + companion design notes (Pattern B session 2026-06-12)
- Legolas research: fantasy ARPG + sci-fi/roguelike proxy type taxonomy

**GAMORA KERNEL HANDOFF:** fires immediately on Session 2 lock. Companion dispatch at `agentic_orchestration/dispatches/2026-06-12-gamora-proxy-kernel-handoff.md`.

> **NORMALIZATION PASS (gandalf, 2026-06-12, Matt-authorized):** axis bin vocabulary re-pointed to the locked definitions in `canonical/story/qd-engine-bc-axes-lock-2026-05-20.md` § 3, and kernel premises corrected against engine code (read-only verification, see legibility verdict § 6). Three conventions apply throughout:
> 1. **Generation-time vs measurement-time:** generation priors below bind to generation-time structural properties (declared `energy_type`, CC effect tags, skill geometry assignments) or to PREDICTED BC bins. Actual bins are measured downstream by the BC pipeline.
> 2. **Energy types are not Axis 5 bins:** focus/mana/rage are declared `energy_type` values (structural). The locked Axis 5 bins are HP-economy / damage-taken-converts / charge-stack / starved / overflow / generator-spender / steady (measured). Prior tables below label energy rows accordingly.
> 3. **Axis 2A deferral retirement:** the lock doc marks Axis 2A (Proxy Density) as ALWAYS sim-deferred because the sim was solo-only. The ProxyCombatant kernel extension (§ 3) RETIRES that deferral — once proxies are fight entities, Axis 2A becomes measurable. This is a lock-doc consequence to record at Session 2 ratification, not an amendment to any locked bin.
>
> Delta summary: `gandalf/notes/2026-06-12-normalization-pass-delta-summary.md`.

---

## 0. Design mandate

Deliver complete specs for: all 14 Tier 1 proxy types, the ProxyCombatant kernel interface, companion modifier vector, NPC/Companion season generation criteria, Monster season generation criteria, faction taxonomy, monster binding categories, and support/CC skew parameters. This session unlocks the gamora kernel extension (ProxyCombatant entity model) and the rocket generation seam (proxy type assignment, companion season, monster season).

**Architectural decision (2026-06-12):** Tier 2 NPC/Companion and Tier 3 Monster companions are **modifier vectors**, not fight entities. Only Tier 1 mechanical proxies are ProxyCombatant entities in the fight loop. This collapses 400×N full fight simulations to 400×~100 modifier-vector applications per faction/category gating.

---

## 1. Three-tier proxy system

| Tier | Name | Entity model | Fight participation | Season | Generation |
|---|---|---|---|---|---|
| **Tier 1** | Mechanical proxy | ProxyCombatant (kernel entity) | Present in `simulate_fight` | Any season | Via summon-first allocation OR low-probability trait OR proxy-family T4 |
| **Tier 2** | NPC/Companion | Modifier vector (pre-fight parameter) | NOT a fight entity | NPC/Mercenary season | Via COMPANION_CONTRACT T4 + faction filter |
| **Tier 3** | Monster | Modifier vector (pre-fight parameter) | NOT a fight entity | Monster season | Via MONSTER_PACT T4 + binding category filter |

---

## 2. Tier 1 — Proxy type catalog (14 confirmed distinct types)

The following 14 types are confirmed mechanically distinct by the proxy taxonomy research (Legolas 1 + 2, 2026-06-12). Each type is assigned a behavioral tier that determines which ProxyCombatant interface features it requires.

### 2.1 Behavioral tier definitions

| Behavioral tier | Required features |
|---|---|
| **Minimal** | HP + death event + damage contribution (or resource gen); no position, no targeting |
| **Mid** | HP + position + enemy AI targeting + damage contribution; no independent skill rotation |
| **Full** | HP + position + enemy AI targeting + independent skill rotation + cooldown tracking |

### 2.2 Type catalog

| # | Type name | Behavioral tier | Distinguishing mechanic | T4 upgrade (PROXY_ASCENSION) |
|---|---|---|---|---|
| 1 | **Passive Fighter** | Mid | Auto-attacks the player's current target; follows player position; simple combat AI | → Autonomous Caster (gains independent skill rotation from player skill subset) |
| 2 | **Autonomous Caster** | Full | Independent skill rotation with cooldown tracking; does NOT track player targeting; acts on own initiative | → Enhanced Caster (rotation depth increases; +1 skill slot) |
| 3 | **Golem/Construct** | Full | High HP; draws enemy aggro (taunt behavior: enemies preferentially target Golem); tanky damage mitigation | → Sovereign Golem (gains its own energy pool; executes 2-skill rotation) |
| 4 | **Totem/Turret** | Mid | Stationary at placement point; fires projectiles at nearest enemy within range_m; zero repositioning | → Range-Gated Turret (activates/deactivates by player proximity; +15% player damage when adjacent) |
| 5 | **Bodyguard** | Full | Intercepts player-targeted hits: when player would take >20% max HP in a single hit, Bodyguard absorbs it instead (substitution event); moves to stay between player and primary enemy | → Sacrificial Bodyguard (PROXY_INVERSION eligible) |
| 6 | **Volatile Emitter** | Mid | Stationary; emits periodic AoE pulses (configurable: damage or debuff) at fixed interval; no targeting AI | → Slot-Queue Emitter (gains queued burst mode alongside passive tick; burst fires on manual evoke) |
| 7 | **Terrain Anchor** | Mid | Placed at position; projects a zone effect (player buff zone OR enemy debuff zone); holds position; low HP | → Damage Amplification Zone (PROXY_INVERSION eligible) |
| 8 | **Resource Conduit** | Minimal | Passive resource generation for player (+N resource per tick or per player hit); no combat contribution | → Enhanced Conduit (resource generation rate increases; gains on-kill burst resource grant) |
| 9 | **Trap/Mine** | Mid | Placed at position; triggers on enemy proximity (proximity trigger) OR on player manual activation; single use; then respawns after cooldown | → Chained Trap (respawns at half cooldown; trigger radius increases) |
| 10 | **Warcry/Buff Spirit** | Minimal | Emits player buff aura (damage amp, speed, resource regen — one buff type per instance); presence-only; no attack | → Reverse-Buff Spirit (PROXY_INVERSION eligible; becomes enemy debuff emitter) |
| 11 | **Fragile Escort** | Mid | Moves alongside player; high reward contribution (resource drops, damage bonus for player) while alive; very low HP; does NOT attack | → Protected Escort (gains a temporary shield absorbing N damage on spawn) |
| 12 | **Slot-Queue Emitter** | Mid | Generates a queue of projectiles over time; fires entire queue as a burst when queue is full (configurable queue depth 3-8 projectiles); positional at launch point | → Overflow Emitter (queue overflow fires bonus projectile at double damage) |
| 13 | **Delayed Position Shadow** | Mid | Records player's position at spawn; after a configurable delay (0.5-3.0s), replays the player's last N skill uses from the recorded position | → Persistent Shadow (records position continuously; can be re-triggered; delay window reset on each player skill use) |
| 14 | **Charged Threshold Proxy** | Full | Accumulates charge stacks from enemy hits (own hits or player hits in range); at threshold (configurable 5-10 stacks), unleashes a high-damage burst or strong CC event then resets | → Overcharged Threshold (threshold burst magnitude +50%; triggers a Fission if PROXY_FISSION T4 also present) |

---

## 3. ProxyCombatant interface spec (gamora kernel handoff — primary artifact)

### 3.1 Design constraints

- ProxyCombatant is a NEW entity class; NOT an extension of Combatant
- Proxies are fight-participants, NOT fight opponents (they fight alongside player, not against)
- Kernel remains brownfield: ProxyCombatant is additive — existing `simulate_fight` path unchanged when `proxies_a=None` and `proxies_b=None`
- All 14 proxy types map to this single interface using optional feature groups

### 3.2 Interface spec

```python
@dataclass
class ProxyCombatant:
    # --- Identity ---
    proxy_id: str              # unique instance identifier
    proxy_type: str            # one of 14 type strings (catalog § 2.2)
    behavioral_tier: str       # "minimal" | "mid" | "full"
    
    # --- Core stats (ALL tiers) ---
    base_hp: float             # base HP pool; 0.0 for Minimal types (no HP tracking)
    current_hp: float          # mutable during fight; starts at base_hp
    damage_multiplier: float   # vs player base damage output (0.0 for support-only types)
    
    # --- Position (Mid + Full tiers) ---
    position: tuple[float, float] | None = None   # spatial position; None for Minimal
    range_m: float = 0.0                          # engagement range; 0 = stationary AoE
    follows_player: bool = False                  # True for Passive Fighter, Golem, Bodyguard, Fragile Escort
    
    # --- Targeting (Mid + Full tiers) ---
    targeting_behavior: str = "none"
    # "nearest"         — targets closest enemy (Totem/Turret, Autonomous Caster)
    # "player_target"   — targets player's current target (Passive Fighter)
    # "taunt"           — draws enemy aggro toward self (Golem)
    # "intercept"       — intercepts player-targeted hits (Bodyguard)
    # "positional"      — no targeting; fires from position (Volatile Emitter, Terrain Anchor)
    # "proximity"       — triggers on enemy entering range (Trap/Mine)
    # "none"            — no targeting AI (Resource Conduit, Warcry/Buff Spirit)
    
    # --- Skill rotation (Full tier only) ---
    skills: list[ProxySkill] | None = None
    cooldowns: dict[str, float] | None = None     # per-skill cooldown state; None for non-Full
    energy_state: ProxyEnergyState | None = None  # for PROXY_SOVEREIGNTY independent energy pool
    
    # --- Zone effect (Terrain Anchor, Volatile Emitter, Warcry/Buff Spirit) ---
    zone_effect: ProxyZoneEffect | None = None
    
    # --- Resource generation (Resource Conduit) ---
    resource_generation: ProxyResourceGen | None = None
    
    # --- Death event ---
    death_event: ProxyDeathEvent | None = None
    # ProxyDeathEvent contains: event_type ("fission" | "explosion" | "transfer" | "none");
    #   fission: fission_count, stat_fraction, sub_proxy_template
    #   explosion: damage_multiplier, radius_m, element
    
    # --- Threshold events ---
    threshold_events: list[ProxyThresholdEvent] = field(default_factory=list)
    # ProxyThresholdEvent: hp_threshold (fraction of base_hp) OR stack_threshold (int);
    #   event_type ("burst" | "cc" | "transform" | "summon"); magnitude
    
    # --- Accumulation state (Charged Threshold Proxy, TEMPORAL_CHARGE if proxy uses skill) ---
    accumulation_state: ProxyAccumulationState | None = None
    # ProxyAccumulationState: current_stacks, max_stacks, accum_trigger ("on_hit" | "on_player_hit_nearby"),
    #   threshold, event_type
    
    # --- Position history (Delayed Position Shadow) ---
    position_history: deque[tuple[float, float, list[SkillUse]]] | None = None
    # stores (position, timestamp, skill_uses) tuples; replay_delay_s configures delay
    replay_delay_s: float = 0.0
    
    # --- Burst queue (Slot-Queue Emitter) ---
    burst_queue: list[ProxyProjectile] | None = None
    queue_depth: int = 0
    
    # --- Intercept state (Bodyguard) ---
    intercept_threshold_pct: float = 0.20  # intercept hits > 20% max HP
    intercepts_remaining: int = 0          # 0 = unlimited
```

### 3.3 Supporting type sketches (gamora defines full implementation)

```python
@dataclass
class ProxySkill:
    skill_id: str
    damage_multiplier: float   # vs proxy's own damage_multiplier
    element: str
    geometry: str              # skill geometry type
    cooldown_s: float
    cc_effect: str | None = None  # CC type if this skill has CC

@dataclass
class ProxyEnergyState:
    energy_type: str           # "charge-stack" for PROXY_SOVEREIGNTY
    current: float
    maximum: float
    accum_per_hit: float

@dataclass
class ProxyZoneEffect:
    zone_type: str             # "player_buff" | "enemy_debuff" | "damage_amp"
    radius_m: float
    magnitude: float           # multiplier or additive amount
    buff_type: str | None = None   # "damage_amp" | "speed" | "resource_regen"
    debuff_type: str | None = None # "damage_reduction" | "slow" | "armor_reduction"
    duration_s: float = 0.0    # 0 = permanent while proxy alive

@dataclass
class ProxyResourceGen:
    resource_type: str         # must match player energy_type
    amount_per_tick: float
    tick_interval_s: float
    on_kill_bonus: float = 0.0

@dataclass
class ProxyDeathEvent:
    event_type: str            # "fission" | "explosion" | "none"
    fission_count: int = 2
    fission_stat_fraction: float = 0.60
    explosion_damage_mult: float = 0.0
    explosion_radius_m: float = 0.0
    explosion_element: str = ""

@dataclass
class ProxyThresholdEvent:
    threshold_type: str        # "hp_pct" | "stack_count"
    threshold_value: float     # fraction for hp_pct; integer for stack_count
    event_type: str            # "burst" | "cc" | "transform"
    magnitude: float
    resets_after: bool = True  # True = threshold resets and can fire again
```

### 3.4 simulate_fight signature extension

**Actual current signature (verified against `simulation/fight_engine.py:107`):** the kernel is SYMMETRIC — `simulate_fight(combatant_a: Combatant, combatant_b: Combatant, ...)` with additional kwargs (max_duration, seed, spatial/gauntlet parameters). There is no player/enemy asymmetry in the kernel; "player" and "enemy" are caller-side roles.

**Proposed extension (symmetric, matching kernel convention):**
```python
def simulate_fight(
    combatant_a: Combatant,
    combatant_b: Combatant,
    *,
    proxies_a: list[ProxyCombatant] | None = None,
    proxies_b: list[ProxyCombatant] | None = None,
    # ... existing kwargs unchanged
) → FightResult:
```

Symmetry preserves the kernel's design invariant AND gives the validation seam future enemy-side proxies (gauntlet bosses with adds) for free. The player-proxy use case passes `proxies_a` only. Backward compatibility: both default to `None`, producing identical fight behavior to current. Existing golden-master oracle is the regression anchor.

### 3.5 FightResult extension (telemetry)

FightResult must track proxy contributions separately from player contributions:

```python
# Additions to FightResult (additive; no existing field removal):
proxy_damage_contributed: float = 0.0          # total proxy-attributable damage
proxy_damage_by_type: dict[str, float] = {}    # per proxy_type
proxy_death_events: list[str] = []             # list of proxy_id values that died
proxy_resource_generated: float = 0.0          # resource contributed by Resource Conduit
```

---

## 4. Tier 2 — NPC/Companion generation spec (rocket seam)

NPC/Companion companions are generated via an NPC/Mercenary season. They are FULLY PLAYABLE kit instances (weapon + armor + accessory + convergence item equipped) drawn from the standard kit generation pipeline with the following constraints.

### 4.1 NPC/Mercenary season — generation parameters

| Parameter | NPC/Mercenary season value | Normal season value |
|---|---|---|
| Kit count target | 800 (2× normal) | 400 |
| Kit scope | Standard generator (all seams apply) | Standard |
| T4 strategy filter | Support-eligible subset only (§ 7 Session 1) | All 21 strategies |
| BC axis prior weights | Support/CC skewed (see § 4.2 below) | Uniform |
| Gear loadout | Full 4-slot (weapon + armor + accessory + convergence item) | Full 4-slot |
| Faction requirement | Faction assigned at generation (lineage × period × register → faction tag; see § 7) | No faction tag |
| Season label | `npc_mercenary` | Standard |
| QD engine | Runs standard QD pipeline | Standard |
| Win-rate gate | NOT applied (NPC kits are not solo fighters; win-rate invalid) | Applied |
| In-band criterion | Companion modifier vector within cap bounds (see § 6) | Win-rate band |

### 4.2 NPC/Companion BC axis prior weights (skew parameters)

These are prior weights on axis bin selection during rocket's generation phase. Higher weight = higher selection probability. Normal season weight = 1.0 for all bins.

| Axis / property | Bin / value (locked vocabulary) | NPC weight | Rationale |
|---|---|---|---|
| Axis 2B (Control Density) | control-pure (predicted; ≥60% control share) | 2.5 | Support role; CC primary |
| Axis 2B (Control Density) | mixed (predicted; 20–60%) | 1.5 | Hybrid support viable |
| Axis 2B (Control Density) | damage-pure (predicted; <20%) | 0.5 | Deprioritize damage-only |
| Axis 4 (Defensive Profile) | mitigator (predicted) | 2.0 | NPC must survive; reactive sustain maps to mitigator |
| Axis 4 (Defensive Profile) | tank (predicted; eHP ratio ≥5.0) | 1.5 | Durable companion acceptable |
| Axis 4 (Defensive Profile) | glass (predicted; eHP ratio <2.0) | 0.2 | NPC fragility is anti-pattern |
| Axis 3B (Amplitude Variance) | flat (predicted; CV <0.3) | 1.5 | Consistent contribution preferred *(original draft said "Axis 3A Sustained" — consistency is a 3B property, not tempo)* |
| Axis 3B (Amplitude Variance) | spiky (predicted; CV ≥0.7) | 0.7 | NPC burst risks waste |
| `energy_type` (structural, generation-time — NOT an Axis 5 bin) | focus | 1.8 | Focus energy supports patience |
| `energy_type` (structural) | mana | 1.4 | Mana supports the kit space |
| `energy_type` (structural) | rage | 0.5 | Rage is player-style energy |
| Axis 1 (Engagement) | All 6 bins (close/mid/ranged × fast/slow) | 1.0 | No skew; NPC range varies |

### 4.3 Faction gating in companion assignment

When a player kit with COMPANION_CONTRACT T4 is matched to an NPC companion:
1. Player kit faction is derived from its generation parameters (lineage × period × register → faction tag; see § 7)
2. Valid companion pool = all NPC/Mercenary season kits with matching faction tag
3. Companion is selected from valid pool; if pool is empty (faction coverage gap), fallback = widest-faction-overlap kit
4. Faction filter reduces valid companion space to approximately 1/F (where F = faction count ≈ 8)

---

## 5. Tier 3 — Monster season generation spec (rocket seam)

Monster companions use the Meshy pipeline (JSON → image gen → Meshy 3D model + rig + animation → UE). The monster kit is generated via a special "Monster season" with constrained generation and visual asset integration.

### 5.1 Monster season — generation parameters

| Parameter | Monster season value |
|---|---|
| Kit count target | 600 |
| Kit scope | Monster-adapted generator: creature geometry (non-humanoid range options); CC-primary skill set |
| T4 strategy filter | CC-eligible subset only (see § 7.4 Session 1) |
| BC axis prior weights | CC/debuff skewed (see § 5.2 below) |
| Gear loadout | None (monsters have stats not gear) — stat baseline from monster tier system |
| Binding category | Assigned at generation per eligibility criteria (see § 8) |
| Season label | `monster_companion` |
| Asset pipeline | JSON → image gen → Meshy 3D model → UE |
| Win-rate gate | NOT applied (monsters are not solo combatants) |
| In-band criterion | Modifier vector within CC/debuff cap bounds |

### 5.2 Monster BC axis prior weights

| Axis / property | Bin / value (locked vocabulary) | Monster weight | Rationale |
|---|---|---|---|
| Axis 2B (Control Density) | control-pure (predicted) | 3.0 | Monsters are CC specialists |
| Axis 2B (Control Density) | damage-pure (predicted) | 0.3 | |
| Layer 2 `stackability` (structural — NOT an Axis 2 geometry bin) | stacking DoT skills | 1.8 | Monster DoT + CC combination *(original draft mislabeled as "Axis 2 DoT_stack")* |
| Axis 2 (Damage Geometry) | small-AOE / large-AOE (predicted) | 1.5 | Monster AoE CC |
| Axis 4 (Defensive Profile) | glass (predicted) | 0.1 | Monster fragility invalid |
| Axis 4 (Defensive Profile) | dodger (predicted; avoidance ≥0.40) | 1.6 | Monster evasion creates tension *(original draft said "Evasion" — locked bin name is dodger)* |
| Axis 3B (Amplitude Variance) | flat (predicted; CV <0.3) | 2.0 | Persistent threat model |
| Axis 3B (Amplitude Variance) | spiky (predicted; CV ≥0.7) | 0.5 | Monster burst punishes player; deprioritize |
| `energy_type` (structural, generation-time — NOT an Axis 5 bin) | rage | 1.5 | Monster rage: primal accumulation |
| `energy_type` (structural) | focus | 1.5 | Monster patience: focus energy |

---

## 6. Companion modifier vector spec

### 6.1 Model

NPC companions and monster companions are applied as pre-fight modifier vectors to the player kit's effective parameters BEFORE `simulate_fight` fires. No kernel change required — modifier application is in the balance loop at companion pairing stage.

**Application point:** `balance_loop.py` — at companion pairing, before `simulate_fight(player, enemy)` call, player combatant parameters are adjusted by the modifier vector.

### 6.2 Modifier types

| Modifier | Parameter affected | Applied as | NPC cap | Monster cap |
|---|---|---|---|---|
| `damage_amp` | Player damage output | Multiplicative (×) | 1.15 (max 15% increase) | 1.10 (max 10% increase) |
| `cc_duration_mult` | Player CC duration on enemies | Multiplicative (×) | 1.25 (max 25% increase) | 1.35 (max 35%; monster CC primary) |
| `survivability_mod` | Player effective HP / incoming damage reduction | Additive (+) | 0.10 (max 10% additive) | 0.0 (monsters don't protect) |
| `resource_gen_mod` | Player resource generation rate | Additive (+) | 0.10 (max 10% additive) | 0.05 (minor resource contribution) |
| `aoe_radius_mod` | Player AoE skill radius | Additive (+) | 0.15 (max 15% radius increase) | 0.10 (max 10%) |
| `enemy_cc_mult` | Enemy CC duration received (enemy debuff) | Multiplicative (×) | 1.0 (NPC does not debuff enemy) | 1.25 (monster-exclusive: enemy stays CCed longer) |

Modifiers compose additively across modifier types (no multiplicative compounding between types). Example: companion gives `damage_amp=1.12` AND `cc_duration_mult=1.20` — these apply independently to their respective parameters.

### 6.3 BC archetype → modifier vector mapping

A companion kit's BC archetype (its axis signature) determines which modifier types it contributes and at what magnitude. Mapping table (rocket derives modifier vector from companion kit's generated BC archetype):

| Primary companion archetype signature (locked vocabulary) | Dominant modifier type(s) | Secondary modifier type(s) |
|---|---|---|
| Axis 2B ∈ {control-pure, mixed} + Axis 4 ∈ {mitigator, tank} | `cc_duration_mult` (near cap) | `survivability_mod` (mid) |
| Axis 2 ∈ {small-AOE, large-AOE} + Axis 3B = spiky | `damage_amp` (near cap) | `aoe_radius_mod` (mid) |
| `energy_type` ∈ {focus, mana} + Axis 3B = flat | `resource_gen_mod` (mid) | `cc_duration_mult` (low) |
| Axis 4 = dodger + any Axis 2 | `survivability_mod` (near cap) | `aoe_radius_mod` (low) |
| Layer 2 stacking-DoT dominant + Axis 2B = control-pure | `enemy_cc_mult` (monster only; near cap) | `cc_duration_mult` (high) |
| Axis 4 ∈ {mitigator, tank} + Axis 5 ∈ {steady, generator-spender} | `resource_gen_mod` (near cap) | `survivability_mod` (mid) |

*(Note: companion kits HAVE run through the BC pipeline by modifier-derivation time — these are MEASURED bins, not predictions. This is the one table in this spec where measurement-time vocabulary applies directly.)*

Intermediate archetype signatures: interpolate between nearest rows. Rocket computes modifier vector at kit finalization time; modifier vector is stored in kit record as a companion-tagged field.

### 6.4 Validation protocol

Balance validation: 400-kit × ~100 valid companion pairs per faction/binding gating = ~40,000 modifier applications (not full fight simulations). Each application verifies:
- No modifier exceeds its cap
- Player WR delta vs no-companion baseline ≤ 0.10 (10 WR points maximum boost from companion)
- If WR delta > 0.10: reduce the dominant modifier by 20% and revalidate

---

## 7. Faction taxonomy

### 7.1 Definition

A faction is a named player-kit grouping derived from the intersection of cultural lineage × historical period × register. Factions serve as the companion pool gating mechanism: player kit and companion kit must share a faction for a valid pairing.

Faction count: **8 factions** (enough to create meaningful restriction without deadlocking pools).

### 7.2 Faction catalog

| Faction | Cultural lineage | Historical period | Register |
|---|---|---|---|
| **Iron Covenant** | Western European (Germanic, Frankish, Arthurian) | Medieval (500–1400 CE) | High fantasy, mythological |
| **Shadow Courts** | Western European (Gothic, Slavic, dark fae) | Medieval / Early Modern | Dark fantasy, grimdark |
| **Eternal Dynasties** | East Asian (Chinese imperial, Japanese shogunate, Korean) | Ancient / Medieval | Mythological, high fantasy |
| **Sunfire Dominion** | Middle Eastern / North African (Islamic Golden Age, Egyptian, Persian) | Ancient / Medieval | Mythological, arcane-golden |
| **Rune-Clans** | Norse / Germanic / Celtic | Ancient / Medieval | Mythological, primal |
| **Bronze Sanctum** | Greek / Roman / Mycenaean / Minoan | Ancient | Mythological, martial |
| **Forge Republics** | Western European / Pan-industrial | Industrial (1800–1920) | Steampunk, arcane-modern |
| **Void Covenant** | Any lineage (liminal / cosmically displaced) | Any period (void-touched) | Cosmic horror, void, void-arcane |

**Void Covenant is a flex faction:** kits whose register = cosmic horror / void can pair with kits from any other faction. This prevents void-register kits from deadlocking the companion pool.

> **Q10 — FACTION COVERAGE GAP (flagged at normalization pass, 2026-06-12):** Session 4's generation directives draw from **14 cultural lineages**, but the 8 factions above cover only the European / East Asian / MENA / Norse-Celtic / Greco-Roman / industrial slices. **Mesoamerican, sub-Saharan African, and South/Southeast Asian lineages have no faction home** — under § 7.3 rule 3 they get nearest-match absorbed into thematically wrong factions (a Mesoamerican obsidian-priest kit lands in "Sunfire Dominion" or "Bronze Sanctum" by tie-break accident). Resolution options: (a) add 1–2 factions covering the gap lineages; (b) define explicit absorption mappings as intentional design; (c) re-derive factions empirically from the generated population (substrate-led). Q10 joins the Session 1 dialogue queue (Q1–Q9). The marginal-lineage tagging discipline (`canonical/story/marginal-lineage-tagging-pattern-2026-05-23.md`) applies: semantic-layer faction identity requires rep-audit, not just nearest-centroid assignment.

### 7.3 Faction assignment rules (rocket seam)

1. Rocket derives faction from the kit's generated `cultural_lineage` + `historical_period` + `register` fields
2. Mapping table (§ 7.2) produces a deterministic faction tag
3. If a kit's combination does not match a primary faction row: assign to nearest-matching faction (tie-break: register has highest weight → lineage → period)
4. Kit record gets a `faction` field (new field in kit output; no kernel impact)
5. Void Covenant assignment: if `register ∈ {"cosmic_horror", "void", "void_arcane"}` → faction = "Void Covenant" regardless of lineage/period

---

## 8. Monster binding category taxonomy

### 8.1 Definition

Monster binding categories define which monster types a player kit is eligible to bind via MONSTER_PACT T4. Eligibility is a property of the player kit's element, energy_type, and T4 strategy — NOT a property of the monster's kit. A player kit can be eligible for 1-3 binding categories based on its properties.

### 8.2 Binding category catalog (6 categories)

| Category | Binding lore | Player eligibility gate | Monster types (thematic) |
|---|---|---|---|
| **Spirit Binding** | Binds ghostly, spectral, and astral entities through shadow-affinity | `element == "shadow"` | Wraiths, shades, spectral constructs, echo-entities |
| **Radiant Binding** | Binds celestial, divine-touched, and sanctified beings through holy resonance | `element == "holy"` | Angels, divine constructs, light elementals, consecrated beasts |
| **Physical Chaining** | Coerces brutes, beasts, and semi-sapient entities through demonstrated dominance | `has_coercion_skill == True` (skill with CC + target_debuff in Layer 2 dimensions) | Ogres, trolls, beasts, golem-class constructs |
| **Elemental Resonance Lock** | Binds pure elementals through matching elemental attunement | `element ∈ {"fire", "water", "earth", "wind", "lightning"}` AND element matches monster's primary element | Fire elementals, storm spirits, earth titans, water serpents |
| **Necromantic Contract** | Raises and contracts undead, liches, and death-entities through command | `energy_type == "mana"` AND `element ∈ {"shadow", "holy"}` | Undead, skeletons, liches, death knights, bone constructs |
| **Primal Pact** | Bonds primal and feral entities through raw will and survival resonance | `energy_type == "rage"` OR `element ∈ {"earth", "lightning"}` AND `engagement_profile == "close"` | Wolves, dire beasts, storm-born, earth-walkers, primal spirits |

### 8.3 Multi-eligibility

Player kits can satisfy multiple binding categories simultaneously. Example: a shadow-element, mana energy_type kit satisfies both Spirit Binding AND Necromantic Contract → eligible for a larger monster pool.

### 8.4 Monster season binding tag assignment

At Monster season generation, each generated monster kit receives a `binding_category` field. Generation targets a roughly equal distribution across binding categories (±20% of target 600/6 = 100 per category). If QD engine produces imbalance, rocket adds a binding-category bin to the QD grid as a secondary dimension (6 bins × existing 8 BC axes → expanded QD space).

---

## 9. Support/CC skew parameters — implementation summary

### 9.1 NPC/Mercenary season skew (applied by rocket at generation time)

```python
NPC_GENERATION_PRIORS = {
    # Predicted-BC-bin priors (locked bin names; bins measured downstream)
    "axis2b_control_pure": 2.5,
    "axis2b_mixed": 1.5,
    "axis2b_damage_pure": 0.5,
    "axis4_mitigator": 2.0,
    "axis4_tank": 1.5,
    "axis4_glass": 0.2,
    "axis3b_flat": 1.5,
    "axis3b_spiky": 0.7,
    # Structural generation-time priors (declared energy_type; NOT Axis 5 bins)
    "energy_type_focus": 1.8,
    "energy_type_mana": 1.4,
    "energy_type_rage": 0.5,
    # All unspecified bins/values: weight = 1.0
}

NPC_T4_ELIGIBLE = [
    "NETWORK_AMPLIFIER",
    "DEFENSIVE_TRADEOFF",
    "RESONANCE_LOOP",
    "PROXY_SOVEREIGNTY",
    "COMPANION_CONTRACT",  # nested sub-companion; rare but valid
]
```

### 9.2 Monster season skew (applied by rocket at generation time)

```python
MONSTER_GENERATION_PRIORS = {
    # Predicted-BC-bin priors (locked bin names; bins measured downstream)
    "axis2b_control_pure": 3.0,
    "axis2b_damage_pure": 0.3,
    "axis2_small_aoe": 1.5,
    "axis2_large_aoe": 1.5,
    "axis4_glass": 0.1,
    "axis4_dodger": 1.6,
    "axis3b_flat": 2.0,
    "axis3b_spiky": 0.5,
    # Structural generation-time priors (Layer 2 + declared energy_type; NOT BC bins)
    "layer2_stackability_stacking": 1.8,
    "energy_type_rage": 1.5,
    "energy_type_focus": 1.5,
    # All unspecified bins/values: weight = 1.0
}

MONSTER_T4_ELIGIBLE = [
    "NETWORK_AMPLIFIER",
    "GEOMETRY_COLLAPSE",
    "MOMENTUM_CASCADE",
]
```

---

## 10. Gamora kernel handoff — what fires immediately

See companion dispatch: `agentic_orchestration/dispatches/2026-06-12-gamora-proxy-kernel-handoff.md`

**Five items in the handoff:**
1. ProxyCombatant full interface spec → this document § 3
2. `simulate_fight` signature extension → § 3.4
3. Companion modifier vector application spec → § 6 (pre-fight modifier; NO kernel change)
4. Charge-stack `_ENERGY_CONFIGS` entry → handoff dispatch § 4
5. Terrain-reactive geometry assessment request → handoff dispatch § 5

**What gamora begins immediately after Session 2 lock:**
- ProxyCombatant entity model (all 14 types; § 3)
- Behavioral-tier dispatch in fight_engine
- Death event handler (PROXY_FISSION foundation)
- Companion modifier vector application in balance_loop (pre-fight)
- charge-stack `_ENERGY_CONFIGS` entry (kernel-change-protocol item)
- Terrain-reactive geometry boundary assessment (gamora judgment on caller-side vs kernel-side)

Sessions 3 and 4 run in parallel with gamora's kernel extension work.

---

## 11. Session 2 open questions (must resolve before lock)

| # | Question | Priority | Note |
|---|---|---|---|
| 1 | Faction names: confirm or rename the 8 proposed factions (§ 7.2). Are these thematically right for the game world? | HIGH | Matt call |
| 2 | Monster binding categories: is "Radiant Binding" vs "Spirit Binding" the right split for holy vs shadow? Or merge into one binding category? | MEDIUM | Design preference |
| 3 | NPC/Mercenary season gear: does the companion's convergence item slot activate during balance validation, or is it a UE/loadout-only slot with simplified modifier? | HIGH | Affects sim scope |
| 4 | Companion modifier vector: is `aoe_radius_mod` meaningful in the sim, or is it loadout-surface only (no spatial geometry in fight loop for standard kits)? | HIGH | Gamora boundary question |
| 5 | Win-rate gate alternative for NPC/Monster kits: confirm that modifier vector cap bounds are the correct in-band criterion (replaces win-rate gate) | MEDIUM | Balance architecture |
| 6 | Faction coverage for monster companions: do monsters share the same faction taxonomy as NPCs, or do monsters use binding categories exclusively for pool gating? | MEDIUM | Architecture decision |
| 7 | Fragile Escort reward contribution model: reward is described as "resource drops, damage bonus for player while alive." How is resource-drop simulated in fight loop vs loadout layer? | LOW | Gamora boundary |
| 8 | **Q10 (faction coverage gap):** Mesoamerican / sub-Saharan African / South-SE Asian lineages have no faction home among the 8 factions (§ 7.2 flag). Add factions, define intentional absorption, or derive factions from substrate? | HIGH | Matt call; joins Session 1 dialogue queue |

---

**Author:** gandalf, 2026-06-12. Matt-authorized Session 2 spec from Pattern B session. Gamora kernel handoff fires on Session 2 lock.
