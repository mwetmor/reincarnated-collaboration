# Proxy-Add Design Spec — 2026-06-16

> **STATUS:** CURRENT (load-bearing as of 2026-06-16) — see `canonical/00-ground-state.md` § 1. The authoritative design spec for the **proxy-add cycle**: proxy SKILLS (generation), proxy GEAR MODIFIERS (capability toolkit), and the kit-side surface of the **Proxy-Commander** profile (set #6 of the six-profile Set-Gear architecture). The paired companion to `canonical/story/six-profile-set-architecture-2026-06-16.md` § 11.1.

**Date:** 2026-06-16
**Author:** gandalf (story-and-design steward)
**Status:** v1 — design-spec-as-math hand-off. Authored from the Pattern-B equipment session with Matt 2026-06-16. **Matt ruling (verbatim intent):** *"We just wired proxy battle into the 2D spatial sim and we just added proxy to T4 capstones. If we don't have proxy skills and gear modifiers, let's add them … I will not skip proxy."* + *"all 6 profiles … v1 skipped, v1.1 = current."* Proxy is first-class.
**Authority:** Matt 2026-06-16 directed the build ("let's add them"). This spec authors the design intent; **rocket** (generation) + **gamora** (simulation calibration) + **star-lord** (naming/telemetry) + **drax** (render) execute; gandalf reviews. knight-rider sequences.
**Companion docs:**
- `canonical/story/six-profile-set-architecture-2026-06-16.md` § 2.6 / § 5 / § 11.1 — the Proxy-Commander profile (set #6) this spec supplies the kit-side surface for.
- `canonical/40-gear-balance-guide-architecture-2026-05-26.md` § 3.3 (capability toolkit), § 3.6 point-5 (no-skill-modifier rule; D54/D55), § 4 (85th-percentile endgame band).
- `canonical/46-concentration-architecture-2026-05-27.md` § 3.3 (capability toolkit), Layer 3 (T4-scope reservation), D66 (one chain-T4 at a time).
- `canonical/story/weapon-as-identity-surface-recognition-2026-06-14.md` § 4 — the three-layer identity model; **summon identity = skill-composition-derived runtime label** (D2/D4/Last-Epoch genre-true); the proxy surface inherits this layer.
- `canonical/story/2026-06-13-companion-as-hall-of-heroes-ally-commitment.md` corollary 1 — **proxies are GENERIC constructs, NOT Hall-of-Heroes ascended forms** (scarcity-as-emotional-engine). The non-negotiable discipline this spec holds.
- The 1D→2D battle-sim deletion (Matt-ruled 2026-06-16) — proxy contribution is **only honestly measurable spatially**; the deletion is ENABLING (§ 8).

**Code anchors (the scaffolded-but-unpopulated proxy surface):**
- `reincarnated-engine/src/reincarnated/generation/kit_architecture.py:44-48` — `Architecture` enum (THREE members); `proxy_primary` is the PENDING fourth, "INTENTIONALLY ABSENT — empirically gated."
- `…/kit_architecture.py:6-8` (docstring proxy-primary guard) — gate = "gamora Items 1-2 + `proxy_contribution_pct` ~0.5 reachability."
- `…/kit_architecture.py:151` — `AOE_AXIS2_BINS` already contains `"multi-spawn"` (substrate-voted geometry bin).
- `…/kit_architecture.py:230, 290-292` — `proxy_delegation: bool` param; proxy kits are EXEMPT from the AoE-skill floor (their AoE *is* the proxies).
- `…/generation/composed_kit_adapter.py:~130` — `_EFFECT_CATEGORY_RANGE_M` already keys `"summon": 3.0` (summon is a recognized `effect_category` with a range derivation).
- `…/generation/skill_schema.py` + `ability_schema.py` — **NO proxy/summon fields** (the gap this spec fills).
- `…/simulation/spatial_gauntlet/spatial_engine.py:1175,1228,1288,1314,1687-1690,1827` — `track_proxy_population` / `_build_player_proxies()` / `_step_proxy_population(elapsed, enemy_dps_est)` / `mean_active_proxy_count` (gamora D4 proxy-port, LIVE, flag-OFF in production).
- `…/simulation/spatial_gauntlet/spatial_bc_measurement.py:187-196` — Axis-2A (Proxy Density) measures **COUNT, not CONTRIBUTION** (the explicit COUNT≠CONTRIBUTION cut; D4 math-note `d4-proxy-port-axis2a-2026-06-16.md` § 4.1).

---

## 0. TL;DR

The proxy/summon surface is **scaffolded across four seams but populated in none.** The substrate already votes `multi-spawn` as a geometry (kit_architecture.py:151); the architecture layer reserves `proxy_primary` as a gated 4th type; the adapter recognizes `summon` as an effect_category; the spatial sim measures proxy population. What is MISSING is the connective tissue: **(1) proxy SKILLS** that compose summon abilities with real count/power/duration/spawn-cadence semantics, **(2) proxy GEAR MODIFIERS** that scale them, and **(3) the Proxy-Commander SET** (#6, already homed in the six-profile doc). This spec specifies all three.

**The load-bearing mechanism (corrected per Matt 2026-06-16): the `proxy_primary` hypothesis test IS the selector — proxy-primary is a hypothesis-test-flagged SUBSET OF CASTER KITS, not a generation-time tuple predicate.**

> **(1) Add proxy/summon skills into the caster skill rotation** (generation work; ships now — this is the "I will not skip proxy" deliverable; one summon skill — **Beast Taming** — also populates the physical-ranged hunter rotation, § 4.5). **(2) The `proxy_primary` architecture-type hypothesis test** — run in the 2D spatial sim, on the proxy CONTRIBUTION measure (§ 8) — **flags which caster kits are proxy-DOMINANT** (proxies do ≥ ~50% of the work). **(3) The flagged kits get the Proxy-Commander #6 set + the proxy-primary T4 capstone skills.** Proxy-primary kits are a **subset of caster kits** (summoning is *predominantly* a caster/mana-gated mechanic — with one deliberate genre-precedent carve-out, **Beast Taming** for physical-ranged hunters, § 4.5, which is *expected sub-threshold*), **not a separated tuple.** You cannot read proxy-dominance off the static tuple — *having a summon skill ≠ being proxy-dominant*; only the sim, measuring where the kit's output actually comes from, can flag it. The test is not an obstacle the profile "ships around" — **the test is the assignment engine.**

This is recognition→validate→commit, honestly applied: Matt's ruling **commissions the build** (add the skills); the **spatial sim votes** (the hypothesis test flags membership on CONTRIBUTION evidence — not designer fiat, not time-passage); the flag **assigns** the set + T4 capstones. This realigns with the already-locked weapon-as-identity § 4 framing (**summon = a skill-composition-derived RUNTIME label**, not a generation-time class) — the earlier "generation-time multi-spawn tuple predicate" framing drifted from that canon and is retired here.

---

## 1. The framing — activate a scaffolded surface, do not invent one

The temptation is to read "add proxy skills and gear modifiers" as greenfield. It is not. The honest framing — and the substrate-led one — is **completion of a partially-built surface.** Four seams already carry proxy scaffolding:

| Seam | What exists | What's missing (this spec) |
|---|---|---|
| Substrate (`kit_architecture.py:151`) | `multi-spawn` is a recognized Axis-2 geometry bin | nothing — the substrate already votes; we consume it |
| Architecture (`kit_architecture.py:44-48`) | `proxy_primary` reserved, gated | the **selector**: the hypothesis test flags proxy-dominant casters → those ARE the Proxy-Commander members (§ 8); runs once gamora adds the contribution measure |
| Skill composition (`composed_kit_adapter.py:130`) | `summon` effect_category + range derivation | the proxy-skill **schema fields** + composition logic (§ 4) |
| Simulation (`spatial_engine.py`) | population accumulator + Axis-2A COUNT measure | a CONTRIBUTION measure + real proxy stats fed from gen (§ 7-8) |
| Gear (`doc 40 § 3.3`) | six-capability toolkit, no proxy capability | a proxy capability + the Proxy-Commander 4pc (§ 5-6) |

**Why this matters for the spec's discipline:** because the substrate already votes `multi-spawn` as a *geometry*, summon skills are substrate-supported today — the bin just has no skills to express it and no gear to scale it. We are not pre-imposing a proxy class (Discipline #36 would forbid that); we give summon skills their kit-side vocabulary and let the **hypothesis test (§ 8) — not a static tuple-predicate — decide which casters are proxy-dominant.** Note the asymmetry with the other five profiles: those emerge from a generation-time substrate predicate over the kit tuple; the Proxy-Commander is **sim-flagged on measured contribution.** The test stands in for the tuple-predicate (and is the more honest selector here, because proxy-dominance is emergent, not readable off the tuple).

---

## 2. Genre grounding — what proxy/summon builds get right and wrong

Proxy builds are a genre cornerstone and a genre minefield. The specific lessons, by game and decision:

- **Diablo 2 Summon-Necromancer (skeletons + revives + golem + Amplify Damage + Corpse Explosion).** One of D2's most beloved AND most dominant builds. The lesson is the *command layer*: the Necro player is BUSY — re-summoning, cursing, corpse-exploding. The army does not play itself. **Design import:** the Proxy-Commander must have player AGENCY (re-summon cadence, a command/target verb, a sacrifice/detonate verb), or it violates the auto-combat-not-canonical correction (doc 40 § 1) — proxies that fight entirely on their own are a screensaver, not a build.

- **Diablo 3 Witch Doctor (gargantuans / zombie dogs / fetishes) + Necromancer (command skeletons / skeletal mages).** The **pet-doctor problem**: at high difficulty, pets evaporated to boss AoE and ground effects, and D3 had to bolt on survivability passives (Life Link, Midnight Feast, "pets take reduced AoE damage") to make pet builds playable at all. **Design import:** proxy survivability vs boss damage must be *designed*, not assumed. Our sim already models this honestly — `_step_proxy_population(elapsed, enemy_dps_est)` takes `enemy_dps_est`, so proxies attrite against real enemy output. gamora must calibrate spawn-cadence / proxy-HP so the steady-state population is neither "evaporates to zero" (the D3 failure) nor "invincible swarm" (the D2-dominance failure).

- **Diablo 3 Helltooth / Inna's / Mundunugu sets.** Pet builds became top-tier *because of the SET*. The set is the proxy-build enabler. **This is exactly the Proxy-Commander set #6 model** — the profile's payoff lives in its flagship set (six-profile doc § 5).

- **Path of Exile (Spectres / SRS / Animate Guardian / golems).** Deep minion ecosystem, two chronic complaints: (a) minion AI/pathing (minions get stuck, mis-target) — a *piloted-game* problem the sim treats as a no-op but drax/the live game must address; (b) **"minion damage is a separate scaling tree from my gear"** — minions scale off `+minion damage` affixes, so the player feels *disconnected* from their army. **Design import — the genre-fix:** the Proxy-Commander 4pc capstone is "your proxies inherit a share of YOUR offensive profile" (six-profile doc § 5). This deliberately solves PoE's disconnection complaint — gearing yourself gears your army. It is the *reason* the capstone has that shape.

- **Last Epoch (Necromancer army / Beastmaster companion).** Minion-as-build-identity done well — minions get their own specialization trees and the build feels like *commanding*, not babysitting. **Design import:** the proxy build wants enough COMMAND agency to feel piloted (target / regroup / sacrifice), echoing the D2 lesson.

- **WoW Hunter (Beast Mastery) + the monster-taming lineage (SMT/Persona demon-capture, Pokémon, the *Beast Tamer* isekai sub-genre).** The *capture-from-enemy* loop — subdue a wild thing, it fights for you — is a distinct acquisition model from conjure-from-mana. **Design import:** this is the **Beast Taming** carve-out (§ 4.5) — ONE summon skill that populates *physical-ranged hunter* kits, expected to sit *sub-threshold* (it supplements the bow; it does not replace it). It is the in-roster proof that *having a summon skill ≠ being proxy-dominant* — the exact distinction the test-as-selector model (§ 0 / § 8) exists to honor.

- **Isekai grounding.** The summoner/commander power-fantasy (Overlord's Ainz commanding the Floor Guardians; the necromancer-isekai sub-genre; Slime's Rimuru and his named subordinates). The fantasy is **command — being the one whose constructs are extensions of will.** But note the genre's own scarcity instinct: the *named unique* subordinates are revered; the *disposable* summons are generic. This is precisely our companion-vs-proxy distinction (§ 4.4).

**Net design posture:** proxies are a *distributed-output, survivability-by-delegation, command-agency* play-pattern — NOT a "press summon, go afk" pattern. The spec encodes command agency + the gear-scaling-link genre-fix + designed attrition.

---

## 3. The play-pattern (player consequence anchor)

> *"I don't fight directly. My constructs do — and the better I command and gear, the more they become extensions of me."*

The Proxy-Commander trades **single-target burst** for **distributed sustained output + survivability-by-proxy** (the army soaks; the commander is safer at range) **+ command tempo** (re-summon, target, sacrifice). It must read as a *different spatial shape* (Axis-2A proxy-heavy) at *comparable total efficacy* (§ 7) — not weaker, not stronger, differently-shaped. The "extensions of me" line is the scaling-link (§ 5.2) made emotional: your army is your reach.

---

## 4. Part 1 — Proxy SKILLS (generation seam — rocket)

### 4.1 The summon-skill schema fields (the gap to fill)

`summon` is already a recognized `effect_category` (composed_kit_adapter.py:130) but no skill carries proxy semantics. Add proxy fields to the skill schema (`skill_schema.py` / `ability_schema.py`) so a summon skill is fully specified:

| Field | Meaning | Bound / source |
|---|---|---|
| `proxy_count` | number of constructs this skill spawns per activation | small int; bounded by Layer-1 caps |
| `proxy_power_per` | per-construct effective output (the unit the budget math uses, § 7) | scalar; gamora-calibrated |
| `proxy_duration_s` | construct lifetime if not killed (0 = permanent-until-death, D2-skeleton style) | seconds |
| `proxy_spawn_cadence_s` | re-summon cooldown (the command-tempo lever; D2 lesson) | seconds |
| `proxy_geometry` | the construct's own attack geometry (melee / projectile / aura) | from the existing geometry vocab (ability_grammar) |
| `proxy_max_active` | cap on simultaneously-active constructs (anti-invincible-swarm) | small int; gamora-calibrated |

These fields populate the sim's `_build_player_proxies()` / `_step_proxy_population()` (today those build from defaults; § 8 wires them to real values).

### 4.2 Composition rules (where proxy skills come from)

- Proxy/summon skills enter the **caster** skill rotation as composable `summon`-category skills (the effect_category already exists, composed_kit_adapter.py:130). The `multi-spawn` geometry bin (kit_architecture.py:151) is the substrate's vote that a summon skill is *available* to a caster kit — but composing a summon skill does NOT make the kit a Proxy-Commander. **Profile membership is the hypothesis-test flag (§ 0 / § 8), not the presence of a summon skill** — a caster with one minor summon among many is not proxy-dominant. **No hand-assignment, and no static "has-summon-skill" predicate** (both would violate the test-as-selector model + Discipline #36). **One bounded exception to the caster-only rule:** the single skill **Beast Taming** populates the physical-ranged hunter rotation (§ 4.5) — the same test-as-selector logic applies (it is *expected* sub-threshold, but the sim, not the tuple, decides).
- A Proxy-Commander-region kit should set `proxy_delegation=True` (kit_architecture.py:230) so the AoE-skill-floor validator (line 290-292) correctly exempts it — its "AoE" is its constructs, not a self-cast nova. **Acceptance:** a proxy kit must pass `validate` without a spurious "no AoE skill" error.
- The summon **identity label** (the construct's name/flavor) is the **skill-composition-derived runtime label** per weapon-as-identity § 4 — D2/D4/Last-Epoch-genre-true. It is NOT an element/archetype coordinate; it emerges from what the kit summons.

### 4.3 Command agency (the anti-screensaver discipline)

Per the D2/Last-Epoch lesson + the auto-combat-not-canonical correction (doc 40 § 1), a Proxy-Commander kit must carry **at least one player-agency verb** beyond "summon": a command/target redirect, a sacrifice/detonate (D2 Corpse-Explosion lineage), or a rally/regroup. The sim treats these as no-ops (it cannot model piloting — same discipline as the dodge layer, telegraph-dodge doc); the LIVE game makes them the build's tempo. **Acceptance (design-review, gandalf):** a generated Proxy-Commander kit's skill set is not 100% passive-summon — it has a command surface.

### 4.4 Scarcity discipline (NON-NEGOTIABLE — proxies are NOT Hall forms)

Per the companion commitment (corollary 1): the Proxy-Commander's army is **generic constructs** — skeletons, elementals, spirit-echoes, golems. They may be *visually flavored* as form-echoes (a fire kit's constructs read as ember-wisps) but they must **never be literal Hall-of-Heroes ascended-form entries.** The singular companion (Q8 layer, 4th gear slot — the season-2 arrival beat) is ONE reverent ally drawn from the player's lived past selves; proxies are MANY disposable constructs. **If a proxy ever reads as "one of my past selves," the scarcity-as-emotional-engine that makes the companion land is diluted.** This is a watch-flag at every wire-in: the proxy generation path must be structurally incapable of reading a Hall entry as a proxy source.

### 4.5 Beast Taming — the physical-ranged carve-out (genre precedent: the hunter-tamer)

One summon skill — **Beast Taming** — populates the **physical-ranged (hunter) skill rotation**, not the caster rotation. This is a deliberate, bounded exception to the caster-only rule (§ 4.2), grounded in genre precedent: the hunter who tames wild things is a load-bearing archetype, and Matt directed leaning into it (2026-06-16).

**The mechanic — capture, not conjure.** The hunter subdues an enemy combatant of **beast type** present in the fight and converts it into a proxy that fights for them. This is mechanically distinct from caster summons (which spawn generic constructs from mana):

| | Caster summon (conjure) | Beast Taming (capture) |
|---|---|---|
| Source | spawned from nothing (mana) | converted from a live enemy beast in the fight |
| Count | many, disposable (`proxy_count` > 1) | few — typically one tamed beast at a time |
| Per-unit power | low (swarm math) | higher (a single meaningful proxy) |
| Acquisition | spawn-cadence (`proxy_spawn_cadence_s`) | capture-opportunity-gated (a beast enemy must be present) |
| Availability | full summon pool, caster kits | this ONE skill, physical-ranged hunter kits |

**Genre grounding.** The WoW Hunter (tame a beast → it becomes your pet; Beast Mastery) is the canonical reference; Last Epoch's Beastmaster (companions with their own trees) is the modern-ARPG done-well case (§ 2); the monster-taming lineage (SMT/Persona demon-capture, Pokémon) is the *capture-from-enemy* loop specifically; the beast-tamer isekai sub-genre (the 2022 *Beast Tamer* anime; the kicked-out-tamer-becomes-OP trope) is the isekai anchor. The fantasy is **mastery over the wild** — distinct from the caster's **command over the conjured.**

**It is expected SUB-THRESHOLD — and that is the point.** A Beast-Taming hunter still hunts: the physical-ranged primary (the bow) is the main output; the single tamed beast supplements. Under the test-as-selector model (§ 0 / § 8), this kit carries a proxy skill but the sim is *expected* to flag its `proxy_contribution_pct` *below* the ~0.5 proxy-dominance threshold — so it keeps its physical-ranged profile and does **not** get the Proxy-Commander set. **This makes Beast Taming the canonical in-roster illustration of `has-a-summon-skill ≠ is-proxy-dominant`** — the exact distinction the test-as-selector model exists to honor. (The model is *test-decides*, not *tuple-decides*: I do not hand-rule "hunters are categorically excluded." If a hunter ever built all-in on the beast and the sim measured it past threshold, the test would flag it. The *expectation* is sub-threshold; the *authority* is the sim.)

**Scarcity discipline holds (§ 4.4).** A tamed beast is a captured *enemy* — generic wild fauna, a trophy of mastery. It is NOT a Hall-of-Heroes ascended form. The emotional registers stay distinct: the tamed beast reads as "a wild thing I subdued," the singular companion as "a revered past self." Beast Taming must never source a Hall entry.

---

## 5. Part 2 — Proxy GEAR MODIFIERS (capability toolkit — rocket)

### 5.1 Where they live — recommend a new `Proxy-adjusting` capability

Doc 40 § 3.3 has six capabilities (Multiplicative / Mechanic-adjusting / Spatial-adjusting / Axis-adjusting / Added-skill-passive / Added-skill-true-active). Proxy modifiers could be smuggled into **Spatial-adjusting** (proxies *are* a geometry phenomenon — multi-spawn). **gandalf recommendation: add a seventh capability, `Proxy-adjusting`**, parallel to the other "-adjusting" members:

| Capability | Description | Slot constraint |
|---|---|---|
| **Proxy-adjusting** (NEW) | Changes construct count / power / duration / spawn-cadence / behavior (e.g., "+1 max construct," "constructs explode on death," "constructs taunt") | All legendary/set slots |

Rationale: Spatial-adjusting changes *your* skill geometry; proxy modifiers change *the constructs'* properties — a distinct object. A dedicated capability keeps the toolkit honest and gives the Proxy-adjusting modifiers a clean home (parallel to how Mechanic-adjusting and Axis-adjusting are distinct even though both "change how a skill works"). This is a small, additive amendment to doc 40 § 3.3.

### 5.2 The scaling-link (the genre-fix; ties to the 4pc capstone)

Per the PoE disconnection complaint (§ 2): proxy power must scale with the **player's own offensive profile**, not a separate `+minion damage` silo. Encode this as the FORM of `proxy_power_per`:

```
proxy_power_per  =  proxy_base_power  +  k_link × (player_offensive_profile)
```

where `k_link` is small at the gear-modifier level (a `Proxy-adjusting` modifier raises it incrementally) and **becomes a profile-defining global at the Proxy-Commander 4pc capstone** (six-profile doc § 5: "your proxies inherit a share of your offensive profile"). So:

- **2pc (set):** accelerates the kit's own chosen proxy chain-T4 (the entry nudge; six-profile § 4.1).
- **4pc (set, T4-scope global):** the scaling-link goes global — constructs inherit a meaningful share of the player's offense + gain count/power/duration. This is the genre-fix made into the set's reason to exist. Magnitude = gamora calibration at the T4-scope anchor (six-profile § 4.2 / § 9).

### 5.3 The no-skill-modifier rule (constraint — hold it)

Doc 40 § 3.6 point-5 (D54/D55): gear NEVER modifies existing chain-node skills (no "+3 to your Summon Skeletons"). Proxy gear modifiers obey this: they add **proxy-scope modifiers** (max-active, behavior, the scaling-link `k_link`) and **proxy-triggered-passives** ("on-kill, spawn a construct"; the D2 "chance to cast on hit" lineage, doc 40 § 3.3 dominant flavor) — they do NOT add levels to the summon skill itself. This keeps proxy gear inside the established gear grammar.

---

## 6. Part 3 — Proxy-Commander SET PROFILE #6 (the kit-side surface)

The six-profile doc (§ 2.6, § 5) already homes the Proxy-Commander as full member #6 with its 2pc/4pc shapes. This spec supplies what fills it:

- **The kit lands in the profile** when the hypothesis test (§ 8) flags it proxy-dominant — emergent, sim-measured, NOT tuple-determined.
- **The 2pc** accelerates the kit's chosen proxy chain-T4 (§ 5.2).
- **The 4pc** is the scaling-link-goes-global capstone (§ 5.2) — count/power/duration + offense-inheritance, T4-scope, coexists with the chain-T4 (six-profile § 4.2; D66 held — the proxy chain-T4 is still one-at-a-time; the set capstone is a separate gear-scope).
- **The aura apex** (six-profile § 7) at 4-piece-complete is element-tinted; for the Proxy-Commander it is thematically the "commander's authority" glow — and may *visually* extend a faint echo to the constructs (a tinted rim on the army) WITHOUT making them Hall forms (§ 4.4 holds).
- **Element-flavoring** (six-profile § 6): the set is mechanically element-agnostic; a fire-Proxy-Commander's constructs read as ember, a water's as frost — StyleProfile-layer, not mechanical.

---

## 7. The proxy power-budget math (design-spec-as-math; gamora calibrates constants)

The balance question: make proxies a viable PRIMARY without the D3-evaporate failure or the D2-dominance failure. The FORM (gandalf); the CONSTANTS (gamora):

**Target parity.** A proxy kit's total effective output `O_proxy` should sit in the SAME endgame band as a non-proxy kit (the 85th-percentile cumulative band, doc 40 § 4). Not weaker, not stronger — differently *shaped*.

```
O_proxy  =  O_direct  +  O_proxies
O_proxies  =  N_active × proxy_power_per × uptime_factor
```

**Steady-state population** (the anti-evaporate / anti-invincible lever) is governed by the existing sim accumulator `_step_proxy_population(elapsed, enemy_dps_est)`:

```
N_active(steady)  ≈  spawn_rate / death_rate
   spawn_rate  =  proxy_count / proxy_spawn_cadence_s   (capped at proxy_max_active)
   death_rate  ∝  enemy_dps_est / proxy_hp
```

- **D3-evaporate failure** = `death_rate ≫ spawn_rate` → `N_active → 0`. gamora must keep `proxy_hp` high enough (or spawn-cadence fast enough) that the army survives boss AoE — the lesson D3 learned the hard way.
- **D2-dominance failure** = `death_rate → 0` and no cap → `N_active` unbounded. `proxy_max_active` (§ 4.1) is the hard wall.
- **Beast Taming (§ 4.5) acquisition differs.** Capture is *event-driven* (a beast enemy must be present and subdued), not cadence-driven. gamora abstracts it as a *capture-opportunity rate* feeding the same `N_active` math, with small `proxy_max_active` (typically 1) and higher `proxy_power_per` (one meaningful proxy, not a swarm). Its `O_proxies` flows through the same contribution measure (§ 8) — and is expected to land *sub-threshold*.

**The `proxy_primary` contribution measure** (kit_architecture.py:6-8) — the input the hypothesis test (§ 8) reads:

```
proxy_contribution_pct  =  O_proxies / O_proxy   →  target ≈ 0.5  (proxies do ~half the work)
```

**This is the architecture-type gate, and it is NOT yet measurable.** The D4 port measures `mean_active_proxy_count` (a COUNT, the explicit COUNT≠CONTRIBUTION cut, spatial_bc_measurement.py:187-196). The gate needs `O_proxies` (a CONTRIBUTION — proxy share of damage/kills), which the sim does not yet compute. **§ 8 names this as the gate's empirical precondition.**

---

## 8. The selector — the `proxy_primary` hypothesis test (spatial CONTRIBUTION, not population-COUNT)

The `proxy_primary` hypothesis test IS the Proxy-Commander selector (§ 0). Here is exactly how it assigns membership and what it needs, grounded in the code:

1. **Build the proxy surface** (§ 4-6): real proxy skills + gear + set. This gives the test a REAL proxy kit to measure (it had only an empty scaffold before — which is *why* `proxy_primary` was "intentionally absent").
2. **Add a proxy CONTRIBUTION measure to the spatial sim.** The D4 port stopped at population-COUNT (gamora's deliberate COUNT≠CONTRIBUTION cut). The test needs `O_proxies / O_proxy`. gamora extends the spatial telemetry with a proxy-damage / proxy-kill accumulator (parallel to `mean_active_proxy_count`). **This is a math hotspot extension — Discipline #18 refinement (OP § 4.2): the contribution-measure methodology fires AFTER the population-COUNT baseline lands, which it now has.**
3. **Run the hypothesis test: measure `proxy_contribution_pct` on each caster kit's composed skill set in the 2D spatial sim.** The kits whose proxies do ≥ ~0.5 of the work at parity-band efficacy (§ 7) **ARE the Proxy-Commander members** — they get the #6 set + the proxy-primary T4 capstone skills. This is the *assignment*, done by measurement, not designer fiat. A caster that composes a summon skill but stays sub-threshold is simply not proxy-dominant — it keeps its caster profile (Stormcaller, Controller) and does not get the set. (A physical-ranged Beast-Taming hunter, § 4.5, is the same case from the other side — one proxy skill, expected sub-threshold, no set.) Whether the `proxy_primary` enum member is *also* added to the `Architecture` type — i.e. whether proxy-dominance becomes a formal architecture coordinate or stays a measured runtime flag layered on the kit's caster architecture — is **rocket's implementation call**; the test resolves the *membership* either way. (The "subset of caster kits, not a separated tuple" framing leans toward runtime-flag, consistent with weapon-as-identity § 4.)

**Why the test-as-selector is the honest model:** proxy-dominance is *emergent and measured*, not declared. You cannot read it off the static kit tuple — a caster with one minor summon among many is not proxy-dominant; only the sim, measuring where the kit's output actually comes from, can tell. This is consistent with the golden-oracle architecture (the spatial sim is the behavioral-identity authority) and with weapon-as-identity § 4 (**summon = a skill-composition-derived RUNTIME label**, not a generation-time class). It keeps faith with recognition→validate→commit: Matt's ruling **commissions the build** (add the skills — happens now); the **sim votes** (the test flags membership on CONTRIBUTION evidence — not designer fiat, not time-passage); the **flag assigns** the set + T4 capstones. I do not flip a gamora empirical measure by design fiat. The 1D→2D deletion is load-bearing: proxy contribution (positioning, soaking, distributed kills) was NEVER honestly measurable in the 1D duel — the test could not have run on the deleted instrument. The spatial sim is the right and only instrument.

---

## 9. Acceptance criteria per seam

### 9.1 rocket (generation)
- Add the § 4.1 proxy fields to `skill_schema.py` / `ability_schema.py`; compose `summon`-category skills into the **caster** rotation (§ 4.2); set `proxy_delegation=True` so the AoE-floor validator exempts proxy kits (acceptance: proxy kit passes `validate` cleanly).
- Compose **Beast Taming** as the single summon skill available to **physical-ranged hunter** kits (§ 4.5) — capture-acquisition semantics (small count, higher per-unit power); it obeys the scarcity discipline (a tamed beast is never a Hall entry) and is expected to flag sub-threshold.
- Add the § 5.1 `Proxy-adjusting` capability to the toolkit; proxy modifiers obey the no-skill-modifier rule (§ 5.3).
- Author the Proxy-Commander set #6 content (2pc accelerate + 4pc scaling-link global, § 5.2 / § 6) in the `set_generator` six-profile pass (six-profile doc § 11.1).
- Hold the scarcity discipline (§ 4.4): proxy generation is structurally incapable of sourcing a Hall entry.
- Math-note before code (Discipline #1). Do NOT activate the `proxy_primary` enum member until § 8 clears it.

### 9.2 gamora (simulation)
- Wire the § 4.1 proxy fields into `_build_player_proxies()` / `_step_proxy_population()` (replace defaults with real per-kit values).
- Calibrate the § 7 constants (`proxy_hp`, spawn-cadence, `proxy_max_active`, `proxy_base_power`, the 4pc `k_link` magnitude at the T4-scope anchor) so a proxy kit lands at parity-band efficacy with neither failure mode.
- **Add the proxy CONTRIBUTION measure** (§ 8 step 2) — the input the hypothesis test reads to assign Proxy-Commander membership. Methodology consultation per Discipline #18 refinement (extension fires after the COUNT baseline).
- Model Beast Taming's **capture-opportunity acquisition** (§ 4.5 / § 7) — event-driven, not cadence-driven; expected sub-threshold contribution.
- Validate all proxy work in the **2D spatial sim** (the sole battle sim post 1D-deletion).

### 9.3 star-lord (telemetry + LLM)
- Proxy CONTRIBUTION telemetry flows to export (a new measured coordinate, MIGRATION as needed).
- Phase-5 LLM *names/flavors* constructs (D7 narrow-blank only — "ember-wisp," "bone-sentinel"); the mechanical proxy content is human-authored. The construct name is the skill-composition runtime label (weapon-as-identity § 4).

### 9.4 drax (player-surface)
- Render constructs (count, the army) + the commander's aura apex echo (§ 6) WITHOUT Hall-form confusion (§ 4.4).
- Surface the command-agency verbs (§ 4.3) in the loadout/skill UI.

### 9.5 elrond (substrate)
- The multi-spawn region predicate (§ 4.2) is substrate-curatable; supply the region definition over the geometry × summon-skill space.

---

## 10. Composition with prior canon

- **Six-profile Set-Gear architecture** — this spec is the kit-side surface of profile #6 (§ 6). The set carries the proxy payoff; the skills + gear carry the per-kit expression.
- **1D→2D battle-sim deletion (2026-06-16)** — ENABLING (§ 8): proxy contribution is only honestly spatial; the deleted 1D duel could never have measured it.
- **Companion-as-Hall-of-Heroes commitment** — the scarcity discipline (§ 4.4) is the hard line; proxies generic, companion singular.
- **Weapon-as-identity recognition § 4** — the construct identity is the skill-composition runtime label (§ 4.2 / § 9.3), genre-true to D2/D4/Last Epoch.
- **Doc 46 Layer 3 / D66** — the 4pc proxy capstone is a gear-scope T4 that coexists with the proxy chain-T4 (§ 6); one chain-T4 at a time still holds.
- **Doc 40 § 3.3 / § 3.6** — the `Proxy-adjusting` capability is an additive amendment (§ 5.1); the no-skill-modifier rule holds (§ 5.3).

---

## 11. Predictions registered (for empirical validation)

Per recognition→validate→commit:

1. **A proxy kit reaches parity-band efficacy with a distinct spatial shape** (Axis-2A proxy-heavy) — not weaker, differently-shaped. *Gate:* gamora spatial-sim measurement at calibrated constants (§ 7).
2. **`proxy_contribution_pct` reaches ~0.5 on a proxy-heavy caster kit once the contribution measure exists** — the hypothesis test flags it a Proxy-Commander member. *Gate:* § 8 step 3. (If no caster crosses threshold, the set's membership is empty until tuning closes the gap — a tuning signal, not a blocker; the skills + gear still ship.)
3. **The scaling-link (4pc) is felt as connection** — players report their gear improving their army (the PoE disconnection complaint dissolved). *Gate:* playtest, post-pipeline.
4. **Command agency keeps the build piloted** — Proxy-Commander does not read as a screensaver. *Gate:* playtest + gandalf design-review of generated kit skill sets (§ 4.3).

**Empirical gate (NOT time-passage):** predictions 1-2 resolve when the proxy surface + contribution measure land and gamora runs the spatial calibration; predictions 3-4 at playtest.

---

## 12. Cross-references

- `canonical/story/six-profile-set-architecture-2026-06-16.md` § 2.6 / § 5 / § 11.1 — the Proxy-Commander profile.
- `canonical/40-gear-balance-guide-architecture-2026-05-26.md` § 3.3 (capability toolkit — `Proxy-adjusting` added § 5.1) / § 3.6 point-5 (no-skill-modifier) / § 4 (endgame band).
- `canonical/46-concentration-architecture-2026-05-27.md` Layer 3 / D66.
- `canonical/story/weapon-as-identity-surface-recognition-2026-06-14.md` § 4 — summon runtime-label.
- `canonical/story/2026-06-13-companion-as-hall-of-heroes-ally-commitment.md` corollary 1 — proxies generic, NOT Hall forms.
- Engine: `kit_architecture.py:6-8,44-48,151,230,290-292`; `composed_kit_adapter.py:~130`; `skill_schema.py`/`ability_schema.py`; `spatial_gauntlet/spatial_engine.py` (D4 port); `spatial_gauntlet/spatial_bc_measurement.py:187-196`; D4 math-note `generation/math/d4-proxy-port-axis2a-2026-06-16.md`.
- `canonical/00-ground-state.md` § 1 — this doc registers as a new CURRENT entry.

**Decisions-log:** the `Proxy-adjusting` capability addition (doc 40 § 3.3 amendment) + the `proxy_primary`-gate-resolution criterion (§ 8) warrant a decisions-log entry — routed to jack-ryan (gandalf recommends; Matt approves; knight-rider drafts; jack-ryan reviews).

---

## 13. Sign-off

**Author:** gandalf (story-and-design steward)
**Status:** CURRENT — the authoritative design spec for the proxy-add cycle. Proxy SKILLS (schema fields + composition + command agency + scarcity discipline), proxy GEAR MODIFIERS (new `Proxy-adjusting` capability + the scaling-link genre-fix + no-skill-modifier constraint), and the Proxy-Commander set #6 kit-side surface. The proxy/summon SKILLS ship now (Matt-ruled — added to the caster rotation, plus **Beast Taming** to physical-ranged hunters, § 4.5); the `proxy_primary` **hypothesis test** assigns Proxy-Commander membership on spatial-sim CONTRIBUTION (§ 8), which the proxy-add work makes measurable for the first time. The test is the selector — proxy-primary is a hypothesis-test-flagged *subset of caster kits*, not a generation-time tuple.
**Composition:** with the six-profile Set-Gear architecture (profile #6), the 1D→2D deletion (enabling), the companion commitment (scarcity), the weapon-as-identity recognition (summon label), doc 46 (Layer 3 / D66), and doc 40 (capability toolkit / no-skill-modifier / endgame band).
**For:** rocket (build the surface), gamora (calibrate + add the contribution measure), star-lord (name/flavor + telemetry), drax (render + command UI), elrond (region predicate); knight-rider sequences; gandalf reviews. The proxy ships first-class — *"I will not skip proxy."*

**Signed:** gandalf (story-and-design steward), 2026-06-16.
