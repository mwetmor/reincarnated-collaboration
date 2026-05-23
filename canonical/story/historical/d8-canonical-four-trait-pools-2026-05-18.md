# D8 (companion) — Canonical-Four Intrinsic Trait Pools

> **STATUS:** HISTORICAL-INFORMATIVE (pre-Epoch-4; consult for lineage only — not current truth) — see `canonical/00-ground-state.md` for current truth

**Authority:** gandalf (story-and-design steward; trait-identity authoring authority per scope-of-work § 1.2 D8 expansion authorized by Matt 2026-05-18 — Option I per `agentic_orchestration/hive-mind/canonical-four-trait-pool-l3-decision-2026-05-18.md`).

**Status:** **Canonical design** for Phase-1 P1 Deliverable 8 expansion. Companion to `d8-trait-floor-design-phase-1-p1.md` (the three new-substrate pools); together the two docs constitute the canonical-7 substrate-symmetric intrinsic trait architecture. Companion to canonical 32 § 4 (trait architecture) + `substrate-identity-declarations-2026-05-17.md` § 1-4.

**Companion downstream:** Deliverable 9 (gear-affix design) extends the same identity surface to gear; see `d9-gear-affix-design-phase-1-p1.md`.

**Authored:** 2026-05-18 in hive-mode Phase-1 P1 (Option I scope expansion).

**Reading order:** § 0 TL;DR → § 1 Architectural frame (recap from D8) → § 2 Fire trait pool → § 3 Water trait pool → § 4 Earth trait pool → § 5 Wind trait pool → § 6 Cross-substrate coherence → § 7 Gamora implementation contract extension → § 8 Cross-references.

---

## § 0 — TL;DR

Four per-class intrinsic trait pools, one each for the canonical-four substrate archetypal classes (`fire_mage`, `water_controller`, `earth_caster`, `wind_controller`). Each pool follows the canonical architecture per canonical 32 § 4 + `project_trait_architecture` memory + D8 precedent:

- **8 traits per class** (matches D8 lightning/holy/shadow; substrate-symmetric across all 7 substrates per Matt's Option I)
- **Floor cadence L1 / L12 / L25 / L38** (2 traits per floor across the 8-trait pool)
- **L50 convergence** (per-rank curves shaped so all 8 traits reach similar power at L50 per B9a calibration intent)
- **Substrate-coherent design** — every trait references the substrate's `mechanical_signature` and `iconic_verbs`; no trait violates `forbidden_mechanics`

**Per-substrate signature anchors (canonical-four):**

- **Fire** — *ignite / escalate / area-persist / burn-apply*: D2 Sorceress Fire tree (Enflame, Warmth, Inferno, Fire Wall, Meteor); D3 Wizard Fire (Hydra, Disintegrate); D4 Sorcerer Fire (Burning, Combust, Fireball); PoE Elementalist Beacon of Ruin; Last Epoch Pyromancer; Grim Dawn Pyromancer; Fire Emblem fire-tome mages
- **Water** — *suffuse / permeate / chill-apply / slow*: D2 Sorceress Cold tree (Cold Mastery, Frozen Orb, Blizzard, Cold Enchant); D3 Wizard Cold (Frost Nova, Ray of Frost, Mirror Image); D4 Sorcerer Cold (Frozen Orb, Ice Spikes, Frost Nova); PoE Cold-DoT (Cold Snap, Vortex); Last Epoch Cold; FFXIV Black Mage Blizzard; Lost Ark Sorceress's Cold school
- **Earth** — *anchor / root-apply / hold-ground / mass-strike*: D2 Druid Earth tree (Cyclone Armor, Volcano, Armageddon, Twister-the-tree); D3 Monk earth-keyed (Wave of Light); PoE Earthshatter / Earthquake; Last Epoch Primalist Earth/Druid; Grim Dawn Shaman primal; FFXIV monk earth-stance; Fire Emblem earth-affinity
- **Wind** — *displace / knockback / redirect / mobility*: D2 Druid Wind tree (Tornado, Cyclone Armor, Hurricane, Twister); D3 Wizard Wind (Energy Twister, Galvanizing Ward); PoE Storm Brand (lightning crossover — used here for displacement mechanics); Last Epoch Stormcaller air-keyed; FFXIV monk wind-stance; Lost Ark Wardancer's wind kit

All 32 traits validate cleanly against the existing `TraitSchema` mechanical primitives. **One new `ability_modifier_key` introduced** (`area_persist_duration_bonus`, used by fire's L1 area-persist anchor — formalizes fire's `area_persist` signature verb at the modifier-key layer; semantically distinct from `control_duration_bonus` which targets ailment durations on individuals). All other traits use existing keys (`cooldown_factor`, `energy_cost_factor`, `crit_bonus_damage`, `aoe_radius_bonus`, `control_duration_bonus`, `multishot_floor_bonus`) or existing STAT keys (`bonus_damage_percent`, `bonus_hp`, `bonus_armor`, `bonus_mana_regen`, `bonus_crit_chance`, `bonus_damage_flat`). The D8 NEW keys (`chain_targets_bonus`, `consecrate_radius_bonus`, `drain_lifesteal_fraction`, `conceal_evasion_bonus`, `ailment_cleanse_factor`) are not used by canonical-four pools.

**Total new ability_modifier_keys added by canonical-four:** **1** (down from 5 in D8). Canonical-four substrates leverage existing mechanical primitives more heavily — exactly as the L3 briefing predicted (canonical-four substrates have *more* genre precedent, so well-trodden mechanical hooks suffice).

---

## § 1 — Architectural frame (recap from D8)

This section restates the architectural commitments authored in D8 § 1 so this doc is readable standalone. Conceptual content is identical to D8 § 1; the per-rank curve shape, substrate-identity cross-reference protocol, and 8-trait sizing rationale are unchanged. Implementation specifics expanded for canonical-four are in § 7.

### § 1.1 — What a trait pool IS (canonical 32 § 4 recap)

Each class has a curated **trait pool** of 5-10 traits with floors at L1 / L12 / L25 / L38. At trait floor level N, all class traits with that floor auto-activate. Traits AUTO-RANK based on character level + per-trait curve (B9a calibration intent: all eligible traits reach similar power at L50). Player does NOT invest skill points in traits.

Two sources, one trait pool: (1) **Intrinsic** (per-class curated pool — *this doc* authors the canonical-four side); (2) **Gear-affix rolls** (element/mechanic-gated; D9 territory). Same trait from both sources stacks per `project_trait_architecture` rank-stacking rules.

### § 1.2 — 8 traits per class (substrate-symmetric)

Per the L3 briefing § 6, canonical-four pools target **8 traits each** matching D8 — 2 at L1, 2 at L12, 2 at L25, 2 at L38. Substrate-symmetric across all 7 substrates. The substrate-expansion-decision design promise (additive equality) is honored at this density.

### § 1.3 — Per-rank curve shape (B9a calibration intent)

Same shape as D8 — L1 traits ramp slowly to substantial L50; L12 traits start moderate ramp medium-fast; L25 traits start strong ramp fast; L38 traits start very strong ramp fastest; all converge at L50. Numeric calibration is gamora's empirical work; this doc authors *trait identities* and *floor placements*.

### § 1.4 — Substrate-identity cross-reference protocol

Every trait below is annotated with:

- **`anchors:` field** — citing which `mechanical_signature` verbs OR `iconic_verbs` from the substrate identity declaration the trait realizes
- **`forbidden_mechanics` audit** — explicit in § 6.1
- **Genre lineage** — citing specific Diablo/PoE/Last Epoch/FFXIV/Fire Emblem precedent
- **`cosmological_commitment` and `court_resonance` citations** on L25 + L38 traits (mature-voice tier; identity-anchoring depth)

---

## § 2 — Fire trait pool (`fire_mage`)

**Substrate:** fire. Mechanical signature: `[ignite, escalate, area_persist, burn_apply]`. Forbidden mechanics: `[drain, conceal, slow_channel]`. Combat pillar: `HIGH_BURST_LOW_PERSIST`. Scaling attribute: `intelligence`. Ailment signature: `burn` (DoT — escalation in time).

**Design thesis:** Fire's identity is *escalation* — what begins small and becomes total. The trait pool reinforces ignition / area-persistence / burn-DoT-extension / consequence-accumulating-in-time. Fire is martial-register, the *primary* damage substrate of the canonical-four; its pool leans damage-strong (role_affinities.damage = 0.8) and rewards persistence-of-flame mechanics specifically. No trait can drain, conceal, or slow-channel (forbidden_mechanics).

**Genre lineage cluster:** D2 Sorceress's Fire-tree synergy chains (Warmth → Inferno → Fire Mastery → Fire Wall → Meteor) — fire as *escalating tree* with synergy bonuses. D3 Wizard's Hydra (area-persist) + Disintegrate (channel-into-escalation, though we explicitly avoid the slow_channel framing). D4 Sorcerer's Burning + Combust + Fireball stacking. PoE's Elementalist Beacon-of-Ruin spreads ignite ailments. Grim Dawn's Pyromancer combines fire DoT with explosion-on-death cascades. The canonical pattern: fire DoT stacks, fire AOE leaves residue, fire crits escalate to subsequent hits.

### § 2.1 — Fire traits

```yaml
trait_pool:
  class: fire_mage
  size: 8
  scaling_attribute: intelligence

  traits:

    # ── L1 floor — identity anchor + tactical entry ────────────────────────────
    - trait_id: fire_t1_kindling
      name: "Kindling"
      floor: 1
      category: ABILITY
      ability_modifier_key: control_duration_bonus
      description: |
        Your burn ailments tick for slightly longer. The first lesson of fire:
        the spark you delivered keeps acting after you have moved on.
      anchors:
        mechanical_signature: [burn_apply, escalate]
        iconic_verbs: [ignites, burns, kindles]
      genre_lineage: |
        D2 Sorceress Fire Mastery's per-rank burn-duration synergy; D4 Sorcerer
        Burning Aspect "burn duration +0.5s" affix family; PoE's Elemental
        Equilibrium burn-extension passive nodes. The canonical fire-DoT-extension
        primitive.
      design_note: |
        Existing key (control_duration_bonus). +0.5s at L1 rank 1; scales to
        ~+2.0s at L50 rank-equivalent. Burn is fire's ailment-signature; extending
        it from session start establishes "burn is fire's identity" at L1. Pairs
        with every fire skill in the kit.

    - trait_id: fire_t1_hearth_persist
      name: "Hearth Persist"
      floor: 1
      category: ABILITY
      ability_modifier_key: area_persist_duration_bonus    # NEW KEY — see § 7 contract
      description: |
        Your fire-area-persist effects (fire walls, lingering flame zones,
        meteor afterburn) last slightly longer. The first lesson of fire: where
        you put fire, fire stays.
      anchors:
        mechanical_signature: [area_persist, escalate]
        iconic_verbs: [burns, scorches, kindles]
      genre_lineage: |
        D2 Sorceress Fire Wall's per-rank duration scaling; D3 Wizard Hydra's
        skill-rank duration; D4 Sorcerer Firewall Aspect of Singed Extremities
        (extended burn zones); PoE Fire Trap's ground-burn duration.
      design_note: |
        NEW KEY: area_persist_duration_bonus is additive (seconds). Distinct from
        control_duration_bonus (per-target ailment duration) — area_persist
        targets the FIELD-side persistence of a fire's ground-zone presence.
        +0.4s at L1 rank 1; scales to ~+1.5s at L50. Reinforces fire's
        `area_persist` mechanical_signature at the modifier-key layer — formalizes
        what was a verb in the substrate declaration into a concrete mechanical
        hook.

    # ── L12 floor — tactical texture ───────────────────────────────────────────
    - trait_id: fire_t12_cascade_strike
      name: "Cascade Strike"
      floor: 12
      category: ABILITY
      ability_modifier_key: crit_bonus_damage
      description: |
        Your fire abilities crit harder against targets already burning. Fire is
        the substrate of consequence accumulating in time: the second blow on a
        target the first blow has prepared.
      anchors:
        mechanical_signature: [ignite, escalate, burn_apply]
        iconic_verbs: [scorches, engulfs, flares]
      genre_lineage: |
        D2 Sorceress's Enchant + Inferno paired-fire synergy on already-burning
        targets; PoE Elementalist's "Mastermind of Discord" amplifying damage
        on ignited; D4 Sorcerer Fireball + Burning interaction (crit against
        burning); FFXIV Black Mage's Firestarter proc (free Firaga after Fire).
      design_note: |
        Existing key (crit_bonus_damage). Conditional ("target is burning"). The
        burn-apply → cascade-crit loop is fire's signature tactical pattern.
        Pairs with Kindling (burn duration → more time in the crit window) and
        every fire skill that applies burn.

    - trait_id: fire_t12_consuming_flame
      name: "Consuming Flame"
      floor: 12
      category: STAT
      stat_key: bonus_damage_percent
      stat_magnitude_type: proportional
      description: |
        Your fire damage receives a small substrate-identity bonus that scales
        with the number of distinct enemies currently burning. Fire is the
        substrate of *the world finishing what you began*; more torches lit,
        more reward to the firekeeper.
      anchors:
        mechanical_signature: [ignite, escalate, burn_apply]
        iconic_verbs: [burns, consumes, engulfs]
      genre_lineage: |
        D2 Sorceress Fire Mastery synergy-scaling on multi-target burn pools;
        Grim Dawn Pyromancer's "Brimstone" passive scaling with active ignites;
        PoE Ignite-stacker builds (Penance Brand of Dissipation); D4 Sorcerer
        Devastation Aspect (damage per burning enemy).
      design_note: |
        Proportional bonus_damage_percent. Conditional scalar ("per burning
        enemy", cap at ~5-6 enemies to prevent unbounded scaling — gamora
        balance call). Reads as "fire rewards the firekeeper who keeps the
        room burning." Encourages multi-target burn-spread loops; reinforces
        HIGH_BURST_LOW_PERSIST pillar (bursts kindle; multi-burns amplify
        subsequent bursts).

    # ── L25 floor — keystone-adjacent depth ────────────────────────────────────
    - trait_id: fire_t25_firewell
      name: "Firewell"
      floor: 25
      category: ABILITY
      ability_modifier_key: aoe_radius_bonus
      description: |
        Your fire-area-persist effects extend slightly in radius. The substrate
        of escalation widens the zone of its own keeping.
      anchors:
        mechanical_signature: [area_persist, ignite]
        iconic_verbs: [engulfs, scorches]
        cosmological_commitment: |
          "The substrate of escalation — what begins small and becomes total.
          Fire is the substrate of consequence accumulating in time."
      genre_lineage: |
        D2 Sorceress Fire Wall's radius/length synergy at high ranks; D3 Wizard
        Hydra's "Mammoth Hydra" rune extending zone footprint; D4 Sorcerer
        Firewall Wider Conflagration; PoE Searing Bond's connected radius nodes.
      design_note: |
        Existing key (aoe_radius_bonus). Conditional ("fire-area-persist
        abilities"). Pairs with Hearth Persist (longer area-persist) for
        sustained-zone identity. Reads keystone-style: zones get bigger AND
        last longer simultaneously as fire matures.

    - trait_id: fire_t25_pyre_resonance
      name: "Pyre Resonance"
      floor: 25
      category: STAT
      stat_key: bonus_damage_percent
      stat_magnitude_type: proportional
      description: |
        Your fire damage against targets in your fire-area-persist zones is
        amplified in proportion to how long the zone has been burning. The
        longer the fire holds the ground, the more the substrate amplifies
        what falls into it.
      anchors:
        mechanical_signature: [area_persist, escalate, burn_apply]
        iconic_verbs: [burns, consumes, kindles]
        cosmological_commitment: |
          "consequence accumulating in time — each tick of the ailment is the
          original spark continuing to act"
      genre_lineage: |
        D2 Sorceress Fire Wall + Meteor area-overlap kill-feel; D3 Wizard Hydra
        sustained-damage scaling against Hydra-area targets; PoE Caustic Arrow
        ground-pool cumulative damage (DoT genre); Grim Dawn Pyromancer's
        Brimstone scaling over time.
      design_note: |
        Proportional bonus_damage_percent. Conditional ("in own fire-area-persist
        zone" AND "zone age" — scales 0 at zone-spawn to max at ~3-4s).
        Encourages stand-and-hold-the-zone tactical pattern; sustains
        HIGH_BURST_LOW_PERSIST through bursts-that-create-zones-that-amplify-
        subsequent-bursts. Reads as fire's "the fire knows the ground" identity.

    # ── L38 floor — mature voice ───────────────────────────────────────────────
    - trait_id: fire_t38_conflagration
      name: "Conflagration"
      floor: 38
      category: ABILITY
      ability_modifier_key: crit_bonus_damage
      description: |
        When 4+ enemies are burning simultaneously, your next fire ability's
        crit damage is dramatically amplified. The substrate of escalation
        reaches its mature voice when many small fires become one great
        burning.
      anchors:
        mechanical_signature: [ignite, escalate, burn_apply, area_persist]
        iconic_verbs: [engulfs, consumes, burns, flares, scorches]
        cosmological_commitment: |
          "The substrate of escalation — what begins small and becomes total."
      genre_lineage: |
        D2 Sorceress Fire Mastery + Enflame paired stacking at high ranks; D3
        Wizard Audacity (damage to burning); D4 Sorcerer Devouring Blaze (crit
        on burning enemies); PoE Elemental Overload + Ignite-stacker
        keystone-tier interactions; Grim Dawn Brimstone keystone scaling.
      design_note: |
        L38 keystone-tier trait. Existing key. Conditional ("4+ enemies burning"
        AND "next fire ability"). High starting power → converges with L1 at L50.
        Reads as "L38 build-defining moment when conflagration windows fire
        reliably." Pairs with every burn-applying skill + Kindling (longer
        burn duration → easier to maintain 4+ active) + Consuming Flame (more
        burning = more passive scaling).

    - trait_id: fire_t38_inferno_keystone
      name: "Inferno Keystone"
      floor: 38
      category: STAT
      stat_key: bonus_damage_percent
      stat_magnitude_type: proportional
      description: |
        Your fire damage receives a substantial bonus when you have active
        fire-area-persist zones in the world. The substrate of *the spark
        that finishes what it began* rewards the firekeeper who has set the
        world burning.
      anchors:
        mechanical_signature: [area_persist, escalate, ignite]
        iconic_verbs: [engulfs, consumes, flares, kindles]
        court_resonance: |
          "the forms that delivered the first spark and let the world finish
          what they began"
        cosmological_commitment: |
          "what begins small and becomes total"
      genre_lineage: |
        D2 Sorceress Fire Mastery + synergy stacking peak-power moment; D3
        Wizard Hydra-build identity ("you ARE your zones"); D4 Sorcerer
        Conjuration Mastery aspect family; PoE Searing Bond keystone identity;
        Grim Dawn Pyromancer's "Brimstone" + Bone Harvest cascade builds.
      design_note: |
        L38 keystone-tier. Proportional bonus_damage_percent. Conditional
        ("≥1 fire-area-persist zone active"). Reads as "fire wants the room
        on fire" — pairs with Firewell + Hearth Persist + Pyre Resonance for
        full zone-build identity. The substrate's court-resonance (the form
        that delivered the spark and let the world finish) becomes a
        mechanical identity at L38: you stop being the *caster* and become
        the *firekeeper*.

```

### § 2.2 — Fire pool design audit

- **Floor cadence:** 2/2/2/2 across L1/L12/L25/L38. ✓
- **Substrate signature realization:** all four `mechanical_signature` verbs (`ignite` / `escalate` / `area_persist` / `burn_apply`) have multiple traits realizing them. ✓ Burn-apply and escalate are the densest (all 8 traits reference one or both); area-persist is anchored by Hearth Persist + Firewell + Pyre Resonance + Inferno Keystone (4 of 8 traits); ignite anchors the burn-apply moment. ✓
- **Iconic verbs realization:** 6 of 7 iconic_verbs cited across traits (only "flares" appears in single trait; "consumes" in 3; "burns" in 4; "engulfs" in 3; "scorches" in 3; "kindles" in 3; "ignites" in 1). ✓
- **Forbidden mechanics:** no trait introduces `drain` (fire forbids — no life-leech or resource-drain), `conceal` (no concealment), or `slow_channel` (no sustained-channel-modifier — even Hearth Persist extends ZONE persistence, not channel duration). ✓
- **Pillar coherence:** all traits reinforce HIGH_BURST_LOW_PERSIST — burst-event amplifiers (Cascade Strike, Conflagration), area-persist that *feeds* bursts (Firewell, Pyre Resonance, Inferno Keystone — zones are post-burst residue that empowers next-burst), burn-DoT extensions that extend the post-burst window. No sustained-channel reward; no slow-cast reward. ✓
- **Court resonance:** explicit court_resonance citation on L38 Inferno Keystone anchors fire's "form that delivered the spark and let the world finish" identity at the keystone tier. ✓
- **Cosmological commitment realization:** 3 of 8 traits explicitly cite cosmological_commitment (L25 + L38 mature-voice tier); identity-anchoring depth visible to the player at mid-late progression. ✓

---

## § 3 — Water trait pool (`water_controller`)

**Substrate:** water. Mechanical signature: `[suffuse, permeate, chill_apply, slow]`. Forbidden mechanics: `[ignite, sudden_strike, direct_burst]`. Combat pillar: `SUSTAINED_PRESENCE_ZONE_DENIAL`. Scaling attribute: `intelligence`. Ailment signature: `chill` (soft_control — movement/action-speed reduction).

**Design thesis:** Water's identity is *pervading presence* — state-change-by-immersion. The trait pool reinforces suffusion / permeation / chill-application / slow. Water is mystic-register, the *primary control* substrate of the canonical-four; its pool leans control-strong (role_affinities.control = 0.7). Water rewards *the room being water* — sustained-zone mechanics that amplify chill and slow, that punish enemies for being inside the zone over time. No trait can ignite, sudden-strike, or direct-burst (forbidden_mechanics).

**Genre lineage cluster:** D2 Sorceress Cold tree (Cold Mastery resistance-pierce; Frozen Orb sustained-zone; Blizzard ground-persist; Cold Enchant) — water's canonical "cold-and-slow as terrain" register. D3 Wizard Cold (Frost Nova hard-CC; Ray of Frost channel — but we read this as soft sustained-presence not slow_channel; Mirror Image as misdirection). D4 Sorcerer Cold (Frozen Orb, Ice Spikes, Frost Nova family with vulnerability stacking). PoE's Cold-DoT (Cold Snap brittleness; Vortex ground-cold residue). FFXIV Black Mage's Blizzard line — water as the *patient amplification phase*. Lost Ark Sorceress's Cold school as zone-denial. The canonical pattern: water zones slow, water DoTs chill-stack, water amplifies subsequent damage on chilled targets.

### § 3.1 — Water traits

```yaml
trait_pool:
  class: water_controller
  size: 8
  scaling_attribute: intelligence

  traits:

    # ── L1 floor — identity anchor + tactical entry ────────────────────────────
    - trait_id: water_t1_suffuse_presence
      name: "Suffuse Presence"
      floor: 1
      category: ABILITY
      ability_modifier_key: control_duration_bonus
      description: |
        Your chill ailments last slightly longer. The first lesson of water:
        the immersion does not end when you stop pouring; the world stays
        cold for a while after.
      anchors:
        mechanical_signature: [chill_apply, suffuse, permeate]
        iconic_verbs: [suffuses, permeates, settles into]
      genre_lineage: |
        D2 Sorceress Cold Mastery duration scaling; D4 Sorcerer Chilled Aspect
        duration family; PoE Vortex ground-cold duration nodes; FFXIV Black
        Mage's Aspect of Ice persistence. The canonical chill-extension primitive.
      design_note: |
        Existing key (control_duration_bonus). +0.5s at L1 rank 1; scales to
        ~+2.0s at L50. Chill is water's ailment-signature; extending it from
        session start establishes "chill is water's identity." Mirrors fire's
        Kindling structurally; substrate-symmetric pattern across the two
        primary canonical-four damage-DoTs.

    - trait_id: water_t1_immersion_field
      name: "Immersion Field"
      floor: 1
      category: ABILITY
      ability_modifier_key: aoe_radius_bonus
      description: |
        Your water-zone AOE radii receive a small bonus. The first lesson of
        water: what fills the space wants to fill more of it.
      anchors:
        mechanical_signature: [suffuse, permeate]
        iconic_verbs: [fills, suffuses, permeates, submerges]
      genre_lineage: |
        D2 Sorceress Blizzard's radius synergy; D3 Wizard Black Hole's "Spellsteal"
        rune radius extension; D4 Sorcerer Blizzard Aspect of Piercing Cold
        radius; PoE Vortex's AOE expansion nodes.
      design_note: |
        Existing key (aoe_radius_bonus). +0.5 radius at L1 rank 1; scales to
        ~+2.0 at L50. Water IS the room the substrate has filled; bigger
        rooms feel more like water's identity from session start. Pairs with
        every water zone ability — chill zones, slow zones, suffusion zones.

    # ── L12 floor — tactical texture ───────────────────────────────────────────
    - trait_id: water_t12_chill_resonance
      name: "Chill Resonance"
      floor: 12
      category: STAT
      stat_key: bonus_damage_percent
      stat_magnitude_type: proportional
      description: |
        Your water damage against chilled targets is amplified. Water is the
        substrate of state-change-by-immersion; the target whose state has
        already changed receives the next change more deeply.
      anchors:
        mechanical_signature: [chill_apply, permeate]
        iconic_verbs: [permeates, fills, stills]
      genre_lineage: |
        D2 Sorceress Cold Mastery's resistance-pierce against cold-resisted
        targets (the structural inverse — same identity); D3 Wizard's
        "Snow Blast" cold-on-chilled rune; D4 Sorcerer Vulnerable-on-Chilled
        Aspect of Frozen Memories; PoE Brittle ailment's crit amplification
        on chilled.
      design_note: |
        Proportional bonus_damage_percent. Conditional ("target is chilled").
        Mirrors fire's Cascade Strike structurally — both reward "the substrate
        prepared its target before the next strike." Water's version is
        damage-multiplier (consistent with control-as-amplifier role) rather
        than crit-multiplier (which would feel more burst-coded — water is
        explicitly NOT direct_burst).

    - trait_id: water_t12_zone_anchor
      name: "Zone Anchor"
      floor: 12
      category: ABILITY
      ability_modifier_key: control_duration_bonus
      description: |
        Your water zones increase chill duration on targets *inside the zone*
        beyond the base chill duration. The substrate of pervading presence
        keeps acting on what is inside its body.
      anchors:
        mechanical_signature: [suffuse, permeate, chill_apply, slow]
        iconic_verbs: [suffuses, fills, binds]
      genre_lineage: |
        D2 Sorceress Frozen Orb's chill-on-pass; D3 Wizard Blizzard ground-chill
        persistence; D4 Sorcerer Frozen Aspect of Frozen Tundra (zone chill
        refresh); PoE Vortex chill-on-tick.
      design_note: |
        Existing key (control_duration_bonus). Stacks ADDITIVELY with Suffuse
        Presence per project_trait_architecture rank-stacking rules — same key,
        different conditional context (Suffuse Presence is global; Zone Anchor
        is in-zone bonus). At L12+ scaled rank: baseline +0.5s global + +1.0s
        in-zone bonus. Reinforces SUSTAINED_PRESENCE_ZONE_DENIAL pillar — the
        target inside the water is more locked-in than the target outside.

    # ── L25 floor — keystone-adjacent depth ────────────────────────────────────
    - trait_id: water_t25_undertow
      name: "Undertow"
      floor: 25
      category: ABILITY
      ability_modifier_key: cooldown_factor
      description: |
        Water control abilities have reduced cooldowns after you have applied
        chill to 3+ targets within a recent window. The substrate of pervading
        presence rewards the controller who has filled the room.
      anchors:
        mechanical_signature: [chill_apply, suffuse, slow]
        iconic_verbs: [suffuses, fills, binds, submerges]
        cosmological_commitment: |
          "The substrate of pervading presence — what fills a space rather than
          hitting it."
      genre_lineage: |
        D2 Sorceress Cold-tree CDR synergies at multi-target chill; D3 Wizard's
        "Cold Blooded" trait for CC-reset; D4 Sorcerer's Frost Nova cooldown
        reduction on Vulnerable; PoE Hatred + Cold-DoT cycle CDR.
      design_note: |
        Multiplicative cooldown_factor. Conditional ("3+ chilled targets in
        recent window"). Reads as "water rewards the controller who has
        succeeded at filling the room." Pairs with Immersion Field (bigger
        radius → more targets chilled at once) + Suffuse Presence (longer
        chill duration → easier to maintain 3+ count). 0.92 at L25+ rank 1;
        scales to ~0.75 at L50.

    - trait_id: water_t25_glacial_pressure
      name: "Glacial Pressure"
      floor: 25
      category: STAT
      stat_key: bonus_damage_percent
      stat_magnitude_type: proportional
      description: |
        Your water damage against targets that have been chilled for ≥3 seconds
        is amplified. The longer the target has been immersed, the more the
        substrate has prepared it.
      anchors:
        mechanical_signature: [chill_apply, permeate, suffuse]
        iconic_verbs: [stills, fills, settles into, binds]
        cosmological_commitment: |
          "state-change-by-immersion — the world inside the water is not the
          world above it"
      genre_lineage: |
        D2 Sorceress Glacial Spike's chill-stack-to-freeze threshold logic;
        D3 Wizard's "Sleet Storm" channel scaling against persistent-chill;
        D4 Sorcerer Frostbite vulnerability scaling over time; PoE Bonechill +
        Brittle keystone-tier interactions.
      design_note: |
        Proportional bonus_damage_percent. Conditional ("chill duration ≥3s on
        target"). Reads keystone-style — patient water amplifies; impatient
        water stays at baseline. The trait *rewards the SUSTAINED_PRESENCE
        pillar* — the player who held the chill rather than re-applying it
        gains more. Pairs with Suffuse Presence (longer chill → reaches the
        3s threshold cleanly) + Zone Anchor (in-zone targets stay chilled
        longer).

    # ── L38 floor — mature voice ───────────────────────────────────────────────
    - trait_id: water_t38_deluge
      name: "Deluge"
      floor: 38
      category: ABILITY
      ability_modifier_key: aoe_radius_bonus
      description: |
        Your water ability AOE radii receive a substantial bonus when you have
        active water zones in the world. The substrate of pervading presence
        reaches its mature voice when the room itself has become water.
      anchors:
        mechanical_signature: [suffuse, permeate, slow]
        iconic_verbs: [fills, suffuses, submerges, settles into]
        cosmological_commitment: |
          "The substrate of pervading presence — what fills a space rather
          than hitting it."
      genre_lineage: |
        D2 Sorceress Blizzard + Frozen Orb peak-zone-density build at high
        ranks; D3 Wizard's "Hydra"-like persistence (cold variant —
        Mirror Ball / Mammoth-cold-builds); D4 Sorcerer Blizzard +
        Frost Nova zone-overlap identity; PoE Cold-DoT zone-stacker peak.
      design_note: |
        Existing key (aoe_radius_bonus). Conditional ("≥1 water zone active").
        L38 keystone-tier. Pairs with Immersion Field (baseline radius bonus)
        + Zone Anchor (in-zone chill duration). Reads as "water wants the
        room to be water" — the substrate's mature voice is *the world
        BEING the substrate*. Sustains SUSTAINED_PRESENCE_ZONE_DENIAL pillar
        at maximum depth.

    - trait_id: water_t38_tide_keystone
      name: "Tide Keystone"
      floor: 38
      category: STAT
      stat_key: bonus_damage_percent
      stat_magnitude_type: proportional
      description: |
        Your water damage receives a substantial bonus that scales with the
        number of distinct enemies currently chilled. The substrate of
        state-change-by-immersion: each target whose state has changed
        amplifies the substrate's mature voice further.
      anchors:
        mechanical_signature: [chill_apply, suffuse, permeate, slow]
        iconic_verbs: [stills, fills, binds, suffuses, submerges]
        court_resonance: |
          "the forms that walked into rooms and changed what those rooms were"
        cosmological_commitment: |
          "state-change-by-immersion"
      genre_lineage: |
        D2 Sorceress Cold Mastery + Frozen Orb peak-density chill-pool builds;
        D3 Wizard's "Mirror Ball" rune for multi-Frozen-Orb stacking; D4
        Sorcerer Frostbite multi-target vulnerability scaling; PoE Bonechill
        stacker keystone builds; Lost Ark Sorceress Cold-school peak-zone
        identity.
      design_note: |
        Proportional bonus_damage_percent. Conditional scalar ("per distinct
        chilled enemy"; cap at ~5-6 to prevent unbounded — gamora balance call).
        Mirrors fire's Consuming Flame structurally — both reward "the substrate
        rewards the substrate-keeper who has filled the room." Water's version
        is keystone-tier (L38) where fire's was L12 — water is *patient*; the
        cosmological-commitment rewards patience at the mature-voice tier.
        Pairs with every chill-applying skill + Suffuse Presence + Zone Anchor.

```

### § 3.2 — Water pool design audit

- **Floor cadence:** 2/2/2/2. ✓
- **Substrate signature realization:** all four `mechanical_signature` verbs (`suffuse` / `permeate` / `chill_apply` / `slow`) have multiple traits realizing them. ✓ Chill-apply receives heaviest coverage (5 of 8 traits); suffuse/permeate paired across the zone-anchored traits; slow surfaces in Zone Anchor + Glacial Pressure + Tide Keystone. ✓
- **Iconic verbs realization:** all 7 iconic_verbs cited across traits (suffuses ×4, permeates ×3, fills ×5, stills ×2, submerges ×3, binds ×3, settles into ×2). ✓
- **Forbidden mechanics:** no trait introduces `ignite` (water forbids — no fire DoT), `sudden_strike` (no burst-event amplifier — water uses damage-multiplier on chilled, not crit-on-chilled), or `direct_burst` (no burst-on-condition trait — water amplifies post-application sustained pressure). ✓
- **Pillar coherence:** all traits reinforce SUSTAINED_PRESENCE_ZONE_DENIAL — chill-extension (Suffuse Presence, Zone Anchor), zone-AOE (Immersion Field, Deluge), patient-amplification (Chill Resonance, Glacial Pressure), zone-or-chill-conditional CDR (Undertow), multi-chilled scaling (Tide Keystone). Water's mature voice is *the room being water*; the pool delivers that. ✓
- **Court resonance:** L38 Tide Keystone cites court_resonance ("forms that walked into rooms and changed what those rooms were"). ✓
- **Substrate-asymmetry with fire (cosmologically intentional):** fire's pool rewards *burst into pre-applied burn* (Cascade Strike at L12 = crit-on-burning); water's pool rewards *amplification of pre-applied chill* (Chill Resonance at L12 = damage-multiplier-on-chilled). Same architectural pattern, different valence — fire spikes, water grinds. This is the intended fire↔water anti-pole asymmetry from the substrate-identity declarations made mechanically legible. ✓

---

## § 4 — Earth trait pool (`earth_caster`)

**Substrate:** earth. Mechanical signature: `[anchor, root_apply, hold_ground, mass_strike]`. Forbidden mechanics: `[displace, lift, sudden_traversal]`. Combat pillar: `ANCHOR_AND_DISRUPT`. Scaling attribute: `wisdom`. Ailment signature: `root` (hard_control — positional immobilization).

**Design thesis:** Earth's identity is *positional refusal* — what does not yield. The trait pool reinforces anchoring / rooting / holding-ground / mass-strikes. Earth is martial-register; its pool leans control-strong (role_affinities.control = 0.8) but with hold-ground damage variance (role_affinities.damage = 0.6 — earth's "tank-caster" identity). Earth rewards *the player standing where the world will not move them, while the world stops moving around them*. No trait can displace, lift, or sudden-traverse (forbidden_mechanics).

**Genre lineage cluster:** D2 Druid Earth tree (Volcano + Armageddon + Molten Boulder area-control with root-keyed CC; Cyclone Armor for tank-survival — the canonical "earth-caster" identity). D3 Monk Wave of Light's mass-strike pillar drop. D4 Druid Earth's Earthbreaker family. PoE's Earthshatter / Earthquake — earth as *heavy-strike with root-secondary*. Last Epoch Primalist Earth — root-stacking-into-mass-strike combo. Grim Dawn Shaman's primal-earth lightning crossover (used here for the mass-strike-with-root pattern, not the lightning). FFXIV monk earth-stance Riddle-of-Earth (damage reduction, hold-the-line tank flavor). The canonical pattern: earth roots enemies, earth amplifies damage on rooted targets, earth grants the caster mass/HP/armor to stand-and-hold while doing so.

### § 4.1 — Earth traits

```yaml
trait_pool:
  class: earth_caster
  size: 8
  scaling_attribute: wisdom

  traits:

    # ── L1 floor — identity anchor + tactical entry ────────────────────────────
    - trait_id: earth_t1_root_persist
      name: "Root Persist"
      floor: 1
      category: ABILITY
      ability_modifier_key: control_duration_bonus
      description: |
        Your root ailments hold targets slightly longer. The first lesson of
        earth: what you have rooted does not move, and the substrate does not
        forget what it has held.
      anchors:
        mechanical_signature: [root_apply, anchor, hold_ground]
        iconic_verbs: [roots, holds, binds in place]
      genre_lineage: |
        D2 Druid Carrion Vine / Spirit-of-Barbs root family duration scaling;
        D4 Druid Earthbreaker's Subterranean Aspect root extension; PoE
        Earthquake's stunned-target window. The canonical root-extension primitive.
      design_note: |
        Existing key (control_duration_bonus). +0.5s at L1 rank 1; scales to
        ~+2.0s at L50. Root is earth's ailment-signature (hard_control); extending
        it from session start establishes "root is earth's identity." Mirrors
        fire's Kindling / water's Suffuse Presence structurally — substrate-
        symmetric ailment-extension pattern across all three primary canonical-four
        ailment-substrates.

    - trait_id: earth_t1_stoneward
      name: "Stoneward"
      floor: 1
      category: STAT
      stat_key: bonus_armor
      stat_magnitude_type: flat
      description: |
        You gain bonus armor at all times. The substrate of unyielding makes
        its caster part of the unyielding from the first moment.
      anchors:
        mechanical_signature: [anchor, hold_ground]
        iconic_verbs: [anchors, holds, stands against]
        cosmological_commitment: |
          "what does not move and will not be moved"
      genre_lineage: |
        D2 Druid Cyclone Armor (defensive caster identity); D3 Monk's
        Earth-set tank passives; D4 Druid Earthen Bulwark family (armor-on-
        cast); PoE Earth-flavored Armour-stacker builds; FFXIV warrior
        earth-affinity defensive stance.
      design_note: |
        Flat bonus_armor. +1 at L1 rank 1; scales to ~+5 at L50. Earth-caster
        identity needs survival to stand-and-hold (vs water-controller's
        survival-via-distance). Stoneward at L1 says "earth is the caster
        that the world cannot move." Pairs with every earth root mechanic
        (the root keeps enemies away while you stand) and Sanctuary-like
        future support builds.

    # ── L12 floor — tactical texture ───────────────────────────────────────────
    - trait_id: earth_t12_pressure_strike
      name: "Pressure Strike"
      floor: 12
      category: STAT
      stat_key: bonus_damage_percent
      stat_magnitude_type: proportional
      description: |
        Your earth damage against rooted targets is amplified. The substrate of
        anchoring is the substrate of *now you cannot leave*: the rooted target
        receives heavier strokes because the substrate has already established
        the ground.
      anchors:
        mechanical_signature: [root_apply, mass_strike]
        iconic_verbs: [crushes, weighs down, binds in place]
      genre_lineage: |
        D2 Druid Armageddon's damage-on-immobilized synergy; D3 Monk Wave of
        Light against stunned/rooted; D4 Druid Earthen Bulwark + Trample
        rooted-target damage; PoE Earthshatter spike-damage on rooted; Last
        Epoch Primalist Earth's root-stacker damage builds.
      design_note: |
        Proportional bonus_damage_percent. Conditional ("target is rooted").
        Mirrors fire's Cascade Strike + water's Chill Resonance structurally —
        substrate-symmetric "amplify-on-own-ailment-applied" pattern at L12
        across the three ailment-DoT substrates. Earth's version is
        damage-multiplier (consistent with control-as-amplifier role); reads
        as "the substrate of weight-on-the-held."

    - trait_id: earth_t12_anchor_resonance
      name: "Anchor Resonance"
      floor: 12
      category: ABILITY
      ability_modifier_key: control_duration_bonus
      description: |
        When you have rooted 2+ targets simultaneously, all your active root
        durations extend further. The substrate of anchoring rewards the
        anchor-keeper who has held multiple lines.
      anchors:
        mechanical_signature: [root_apply, anchor, hold_ground]
        iconic_verbs: [roots, holds, binds in place, anchors]
      genre_lineage: |
        D2 Druid Carrion Vine + Solar Creeper stacked-root synergy; PoE
        Earthbreaker + Earthquake stacked-stun extension; D4 Druid's "Lupine
        Ferocity" multi-target CC duration nodes.
      design_note: |
        Existing key (control_duration_bonus). Stacks ADDITIVELY with Root
        Persist per project_trait_architecture rank-stacking rules (same key,
        different conditional context — Root Persist is global; Anchor
        Resonance is multi-root bonus). At L12+ scaled rank: baseline +0.5s
        global + +1.0s multi-root bonus. Reinforces ANCHOR_AND_DISRUPT pillar
        — the multi-rooter holds longer than the single-rooter.

    # ── L25 floor — keystone-adjacent depth ────────────────────────────────────
    - trait_id: earth_t25_terrahold
      name: "Terrahold"
      floor: 25
      category: STAT
      stat_key: bonus_hp
      stat_magnitude_type: flat
      description: |
        Standing on your own earth zones (rooted-ground residue, ground-
        targeted-circle, pillar AoE areas you have created) grants bonus HP.
        The substrate of unyielding grants the brave a place to be brave from
        — a place that becomes part of the brave.
      anchors:
        mechanical_signature: [anchor, hold_ground]
        iconic_verbs: [stands against, holds, weighs down]
        cosmological_commitment: |
          "positional refusal — it answers the question 'can I be here' with
          'yes, and so can what stands with me'"
      genre_lineage: |
        D2 Druid Oak Sage spirit's HP bonus (earth-druid passive resonance);
        D3 Monk earth-stance survivability passives; D4 Druid Earthen Bulwark
        +HP family; FFXIV warrior earth-affinity Riddle of Earth (damage
        reduction floor that reads HP-equivalent).
      design_note: |
        Conditional flat bonus_hp ("standing in own earth zone"). Pairs with
        Stoneward (passive armor) — Stoneward is the *always-on caster identity
        anchor*; Terrahold is the *zone-tactical reward*. At L25+ scaled rank:
        ~+10 HP in zone (modest; not a survival-trivializer; reads as "the
        ground holds you a little longer when you stand on it"). Mirrors
        holy's Sanctuary L25 trait structurally — both grant zone-conditional
        survivability tied to the substrate's combat-pillar identity. Cosmologically
        coherent: holy's revelation-pillar grants the brave a place to be brave
        from; earth's anchor-pillar does the same but through *positional refusal*
        rather than revelation.

    - trait_id: earth_t25_groundswell
      name: "Groundswell"
      floor: 25
      category: ABILITY
      ability_modifier_key: aoe_radius_bonus
      description: |
        Your earth ability AOE radii receive a bonus when targeted on or
        adjacent to existing earth-zone geometry (your earth zones, root
        areas, pillar effects). The substrate of mass-strike amplifies its
        own when it strikes its own ground.
      anchors:
        mechanical_signature: [mass_strike, hold_ground, anchor]
        iconic_verbs: [crushes, weighs down, stands against]
      genre_lineage: |
        D3 Monk Wave of Light "Pillar of the Ancients" rune adjacent-zone
        radius extension; D4 Druid Earth-keyed Aspect family with adjacent-
        ground scaling; PoE Earthshatter spike-chain radius extension on
        prior earth zones; Last Epoch Primalist Druid's earth-stacker zones.
      design_note: |
        Existing key (aoe_radius_bonus). Conditional ("cast on/adjacent to own
        earth zone"). Encourages "build the ground-base, then strike from the
        base" tactical pattern — consonant with ANCHOR_AND_DISRUPT pillar.
        Pairs with Terrahold (in-zone HP) for full "earth-caster as anchored
        artillery" identity. Mirrors holy's Radiant Pulse L25 structurally —
        both are zone-conditional AOE radius bonuses tied to the substrate's
        zone identity.

    # ── L38 floor — mature voice ───────────────────────────────────────────────
    - trait_id: earth_t38_mountain_voice
      name: "Mountain Voice"
      floor: 38
      category: STAT
      stat_key: bonus_damage_percent
      stat_magnitude_type: proportional
      description: |
        Your earth damage receives a substantial bonus that scales with the
        number of distinct enemies currently rooted. The substrate of *can-I-be-
        here being answered yes-and-so-can-what-stands-with-me* reaches its
        mature voice when the substrate has answered yes to many forms at once.
      anchors:
        mechanical_signature: [root_apply, mass_strike, anchor]
        iconic_verbs: [crushes, weighs down, binds in place, holds]
        cosmological_commitment: |
          "yes, and so can what stands with me"
      genre_lineage: |
        D2 Druid's Armageddon + Volcano + Carrion-Vine stacked-root density
        peak builds; D4 Druid Earthbreaker keystone builds with multi-rooted
        damage scaling; PoE Earthquake-stacker peak; Last Epoch Primalist
        Druid root-stacker keystones.
      design_note: |
        Proportional bonus_damage_percent. Conditional scalar ("per distinct
        rooted enemy"; cap at ~5-6 to prevent unbounded — gamora balance
        call). Mirrors fire's Consuming Flame + water's Tide Keystone
        structurally — substrate-symmetric "per-target-with-own-ailment scalar"
        across the three primary canonical-four ailment substrates. Earth's
        is at L38 (mature voice tier — substrate of patience-and-mass) where
        fire's is at L12 (escalation feels good early) and water's is at L38
        (water also rewards patience). The asymmetry by floor placement is
        cosmologically intentional: fire is volatile-early, earth/water are
        patient-late.

    - trait_id: earth_t38_unyielding_keystone
      name: "Unyielding Keystone"
      floor: 38
      category: STAT
      stat_key: bonus_damage_percent
      stat_magnitude_type: proportional
      description: |
        Your earth damage against the same target receives a compounding bonus
        per second the target has been continuously rooted by you. The
        substrate of *what does not yield* rewards what does not let go.
      anchors:
        mechanical_signature: [root_apply, anchor, hold_ground, mass_strike]
        iconic_verbs: [crushes, binds in place, holds, stands against, weighs down]
        court_resonance: |
          "the forms that held the line when others would have run"
        cosmological_commitment: |
          "the substrate of unyielding — what does not move and will not be moved"
      genre_lineage: |
        D2 Druid Solar-Creeper + Carrion-Vine root-stack peak builds (sustained
        single-target root-pressure DPS); PoE Earth-keyed Withered-like
        stacking against single target; D4 Druid Earthen Bulwark + Trample
        sustained-pressure builds; Last Epoch Primalist Druid Mountain-caster
        sustained-single-target identity.
      design_note: |
        L38 keystone-tier. Proportional bonus_damage_percent. Conditional
        ("continuous root duration on target"; scales 0 at root-application
        to max at ~5-6s of continuous root). Reads as "earth rewards the
        immovable confrontation." Pairs with Root Persist (longer base root
        → reaches the duration tier cleanly) + Anchor Resonance (multi-root
        extension keeps single target rooted while you do other things) +
        Pressure Strike (already-rooted damage). Cosmologically: this is
        earth's mature-voice — the substrate of "the form that did not move
        and would not let what they had held move either." Court resonance
        anchors at L38.

```

### § 4.2 — Earth pool design audit

- **Floor cadence:** 2/2/2/2. ✓
- **Substrate signature realization:** all four `mechanical_signature` verbs (`anchor` / `root_apply` / `hold_ground` / `mass_strike`) have multiple traits realizing them. ✓ Root-apply receives heaviest coverage (5 of 8 traits); anchor/hold-ground paired across the stand-and-defend traits; mass-strike anchors Pressure Strike + Groundswell + Mountain Voice + Unyielding Keystone (4 of 8 traits). ✓
- **Iconic verbs realization:** all 7 iconic_verbs cited across traits (anchors ×2, roots ×3, holds ×5, crushes ×4, stands against ×3, binds in place ×4, weighs down ×4). ✓
- **Forbidden mechanics:** no trait introduces `displace` (earth forbids — no knockback or push), `lift` (no off-ground positional effect), or `sudden_traversal` (no movement-speed bonus or teleport — Groundswell's "adjacent-to-zone" is positional but the caster does not traverse to the zone). ✓
- **Pillar coherence:** all traits reinforce ANCHOR_AND_DISRUPT — root-extension (Root Persist, Anchor Resonance), passive armor (Stoneward), zone-conditional HP (Terrahold), root-conditional damage (Pressure Strike, Mountain Voice, Unyielding Keystone), zone-AOE (Groundswell). Earth's mature voice is *immovable confrontation*; the pool delivers that. ✓
- **Court resonance:** L38 Unyielding Keystone cites court_resonance ("forms that held the line when others would have run"). ✓
- **Substrate-asymmetry with wind (cosmologically intentional):** earth's pool rewards *the caster who does not move* (Stoneward armor, Terrahold zone-HP, Anchor Resonance multi-root); wind's pool (§ 5 below) rewards *the caster whose targets do not stay still* (kinetic redirection). Same architectural pattern, opposite valence — earth holds; wind moves. The earth↔wind anti-pole asymmetry from the substrate-identity declarations is mechanically legible. ✓

---

## § 5 — Wind trait pool (`wind_controller`)

**Substrate:** wind. Mechanical signature: `[displace, knockback, redirect, mobility]`. Forbidden mechanics: `[anchor, root, hold_ground]`. Combat pillar: `KINETIC_REDIRECTION`. Scaling attribute: `wisdom`. Ailment signature: `knockback` (hard_control — positional removal).

**Design thesis:** Wind's identity is *kinetic rearrangement* — what does not destroy what it touches but puts it somewhere else. The trait pool reinforces displacement / knockback / redirection / mobility. Wind is mystic-register, the *mobility-and-redirection* substrate of the canonical-four; its pool leans control-strong (role_affinities.control = 0.7). Wind rewards *the caster who is never where the fight expected them and whose targets are never where they were a moment ago*. No trait can anchor, root, or hold-ground (forbidden_mechanics).

**Genre lineage cluster:** D2 Druid Wind tree (Tornado + Cyclone Armor + Hurricane + Twister-the-tree) — the canonical "wind-caster" identity with mobility-defense and projectile-displacement. D3 Wizard's Energy Twister (displacement-projectile). D4 Sorcerer wind-flavored Lightning crossovers (Static Discharge for the displacement read; we explicitly avoid lightning's chain mechanics — wind owns *displacement*, lightning owns *chain*). PoE Whirling-Blades + Flicker-Strike mobility identity (wind-as-caster-mobility). Last Epoch Stormcaller air-keyed builds. FFXIV monk wind-stance for projectile-redirect tank flavor. Lost Ark Wardancer's wind kit. The canonical pattern: wind knocks back/displaces enemies, wind grants mobility to caster, wind redirects projectiles or empowers area-clear via displacement.

### § 5.1 — Wind traits

```yaml
trait_pool:
  class: wind_controller
  size: 8
  scaling_attribute: wisdom

  traits:

    # ── L1 floor — identity anchor + tactical entry ────────────────────────────
    - trait_id: wind_t1_displaced_grace
      name: "Displaced Grace"
      floor: 1
      category: ABILITY
      ability_modifier_key: control_duration_bonus
      description: |
        Your knockback ailments displace targets for slightly longer. The first
        lesson of wind: the substrate carries; what it has carried takes a
        moment to come to rest.
      anchors:
        mechanical_signature: [knockback, displace, redirect]
        iconic_verbs: [displaces, carries, scatters]
      genre_lineage: |
        D2 Druid Tornado's per-rank stun-window scaling; D3 Wizard Energy
        Twister's "Mistral Breeze" rune extending knockback window; D4
        Sorcerer wind-keyed knockback aspects; PoE Stormcaller's
        Knockback-on-Hit duration.
      design_note: |
        Existing key (control_duration_bonus). +0.2s knockback-recovery delay
        at L1 rank 1; scales to ~+0.6s at L50. Knockback is wind's ailment-
        signature (hard_control via positional removal); extending it from
        session start establishes "the displaced stay displaced a moment
        longer." Mirrors earth's Root Persist structurally — substrate-
        symmetric ailment-extension at the L1 anchor position. The asymmetry
        is in *direction*: root holds; knockback moves; both lock the target
        out of action for the duration.

    - trait_id: wind_t1_drift_mobility
      name: "Drift Mobility"
      floor: 1
      category: STAT
      stat_key: bonus_damage_percent
      stat_magnitude_type: proportional
      description: |
        Your wind damage receives a small bonus while you are moving (the
        engine reads your movement state — at any moment with positive
        velocity, the bonus applies). The first lesson of wind: the substrate
        rewards the caster who is in motion.
      anchors:
        mechanical_signature: [mobility, redirect]
        iconic_verbs: [drifts, displaces, carries]
        cosmological_commitment: |
          "kinetic rearrangement — it does not destroy what it touches; it
          puts it somewhere else"
      genre_lineage: |
        D2 Druid Cyclone Armor's caster-mobility identity (defensive-via-motion);
        D3 Wizard's "Storm Armor" speed-on-cast variants; D4 Sorcerer
        wind-mobility flavor; PoE Whirling-Blades + Flicker-Strike mobility
        identity (caster-velocity-damage); Lost Ark Wardancer's wind
        movement-damage cycle.
      design_note: |
        Proportional bonus_damage_percent. Conditional ("caster is moving").
        Reads tactically: the player who *stops to cast* gets less than the
        player who *casts while drifting*. Reinforces KINETIC_REDIRECTION
        pillar — wind rewards motion at every level. NOTE: requires sim-side
        movement-state read; gamora confirm this is cheap to expose (it should
        be — combat sim already tracks position-tick deltas). At L1 rank 1:
        ~+3%; scales to ~+12% at L50.

    # ── L12 floor — tactical texture ───────────────────────────────────────────
    - trait_id: wind_t12_kinetic_strike
      name: "Kinetic Strike"
      floor: 12
      category: STAT
      stat_key: bonus_damage_percent
      stat_magnitude_type: proportional
      description: |
        Your wind damage against recently-knocked-back targets (within 1.5
        seconds of knockback application) is amplified. The substrate of
        rearrangement: the target whose position has just changed receives
        the next blow in disorientation.
      anchors:
        mechanical_signature: [knockback, displace]
        iconic_verbs: [scatters, carries, blows aside]
      genre_lineage: |
        D2 Druid Tornado + Twister stacked-displacement damage synergy; PoE
        Knockback-on-Hit damage modifiers; D4 Sorcerer wind-keyed staggered-
        target damage; Lost Ark Wardancer kinetic-cycle damage builds.
      design_note: |
        Proportional bonus_damage_percent. Conditional ("target in recent-
        knockback window"). Mirrors fire's Cascade Strike + water's Chill
        Resonance + earth's Pressure Strike structurally — substrate-symmetric
        "amplify-on-own-ailment-applied" at L12 across all four primary
        ailment-substrates. Wind's version uses a *time-window* condition
        (recent knockback) rather than an *ongoing-state* condition (chilled
        / rooted) — because knockback is impulse-coded, not duration-coded.
        Cosmologically: wind acts in moments, not durations.

    - trait_id: wind_t12_redirect_pulse
      name: "Redirect Pulse"
      floor: 12
      category: ABILITY
      ability_modifier_key: cooldown_factor
      description: |
        Wind ability cooldowns reduce when you successfully knock back 2+
        targets with a single cast. The substrate of *what carries* rewards
        the caster who has redirected the room.
      anchors:
        mechanical_signature: [knockback, displace, redirect]
        iconic_verbs: [displaces, scatters, blows aside, redirects]
      genre_lineage: |
        D2 Druid Hurricane-zone CDR synergies at high ranks; D3 Wizard's
        "Magic Weapon — Force Weapon" knockback-on-multi-hit nodes; PoE
        Whirling-Blades CDR on multi-hit; D4 Sorcerer wind-keyed CDR aspects.
      design_note: |
        Multiplicative cooldown_factor. Conditional ("multi-knockback
        single-cast"). 0.92 at L12+ rank 1; scales to ~0.78 at L50.
        Reinforces KINETIC_REDIRECTION pillar — the caster who has redirected
        many at once gets to redirect again sooner. Pairs with Drift Mobility
        (movement-damage bonus) + every wind AOE.

    # ── L25 floor — keystone-adjacent depth ────────────────────────────────────
    - trait_id: wind_t25_gust_grace
      name: "Gust Grace"
      floor: 25
      category: ABILITY
      ability_modifier_key: cooldown_factor
      description: |
        Your wind ability cooldowns reduce while you are moving. The substrate
        of kinetic rearrangement amplifies its own when its caster is part of
        the rearrangement.
      anchors:
        mechanical_signature: [mobility, redirect, displace]
        iconic_verbs: [drifts, carries, displaces]
        cosmological_commitment: |
          "The substrate of motion — what removes targets from their position
          and redirects momentum elsewhere."
      genre_lineage: |
        D2 Druid Hurricane + Cyclone Armor stacked-mobility-CDR identity at
        high ranks; D3 Wizard's "Wreath of Lightning"-like movement-CDR for
        wind-coded skills; PoE Onslaught + Phasing Movement-CDR keystones;
        Lost Ark Wardancer's wind-cycle CDR-on-motion.
      design_note: |
        Multiplicative cooldown_factor. Conditional ("caster is moving").
        Stacks MULTIPLICATIVELY with Redirect Pulse per MULTIPLICATIVE
        registry — both are cooldown_factor, both apply when their conditions
        align (knockback-while-moving compound). Reads as "wind rewards the
        always-moving caster." Pairs with Drift Mobility (damage-on-motion)
        for full "wind-caster as kinetic identity" feel.

    - trait_id: wind_t25_vortex_keystone
      name: "Vortex Keystone"
      floor: 25
      category: ABILITY
      ability_modifier_key: aoe_radius_bonus
      description: |
        Your wind ability AOE radii receive a bonus when the ability is cast
        while you are moving or when targeted on areas you have recently passed
        through (within 2 seconds). The substrate of *what redirects momentum*
        leaves the shape of its own passage in the air.
      anchors:
        mechanical_signature: [displace, redirect, mobility]
        iconic_verbs: [scatters, blows aside, redirects, drifts]
      genre_lineage: |
        D2 Druid Tornado's path-of-passage AOE width scaling at high ranks;
        D3 Wizard Energy Twister's "Mistral Breeze" path-extending radius;
        PoE Tornado / Sirus-projectile path-AOE scaling; Lost Ark Wardancer
        path-AOE wind kit identity.
      design_note: |
        Existing key (aoe_radius_bonus). Conditional ("caster moving" OR
        "cast on path-of-recent-passage"). The conditional logic is more
        complex than other AOE traits in this set — gamora confirm
        implementation cost is acceptable (sim-side path-tracking for ~2s
        window of caster positions). Mirrors earth's Groundswell L25
        structurally — both are zone-conditional AOE bonuses, but earth's
        condition is "adjacent to held-ground" while wind's is "along path
        of passage" — substrate-coherent asymmetry.

    # ── L38 floor — mature voice ───────────────────────────────────────────────
    - trait_id: wind_t38_redirection
      name: "Redirection"
      floor: 38
      category: STAT
      stat_key: bonus_damage_percent
      stat_magnitude_type: proportional
      description: |
        Your wind damage against targets that have been displaced or knocked
        back multiple times receives a substantial bonus per displacement
        event. The substrate of kinetic rearrangement: each rearrangement
        compounds the disorientation.
      anchors:
        mechanical_signature: [knockback, displace, redirect]
        iconic_verbs: [scatters, blows aside, carries, displaces]
        cosmological_commitment: |
          "kinetic rearrangement — it does not destroy what it touches; it
          puts it somewhere else"
      genre_lineage: |
        D2 Druid Tornado + Hurricane + Twister stacked-displacement peak
        builds (cumulative-knockback identity); PoE stacked-knockback
        builds with damage scaling per stagger; Lost Ark Wardancer
        kinetic-cycle peak-damage builds with stacking displacement marks.
      design_note: |
        L38 keystone-tier. Proportional bonus_damage_percent. Conditional
        scalar ("per recent knockback event on target"; cap at ~3-4 to
        prevent unbounded — gamora balance call; events expire ~3s after
        application). Reads as "wind rewards the caster who has displaced
        the target multiple times." Pairs with every knockback-applying
        skill + Displaced Grace (longer recovery → tighter overlap of
        events for compound scaling) + Redirect Pulse (multi-knockback
        cooldown reset enables re-knockback faster). Mirrors fire's
        Conflagration L38 + water's Tide Keystone L38 + earth's
        Unyielding Keystone L38 — substrate-symmetric mature-voice damage
        scaler across all four primary canonical-four ailment-substrates.

    - trait_id: wind_t38_stormrider_keystone
      name: "Stormrider Keystone"
      floor: 38
      category: STAT
      stat_key: bonus_damage_percent
      stat_magnitude_type: proportional
      description: |
        Your wind damage receives a substantial bonus that scales with your
        recent movement distance (how far you have traveled in the last few
        seconds). The substrate of *never-where-the-fight-expected-them*
        reaches its mature voice when the caster has become indistinguishable
        from their own motion.
      anchors:
        mechanical_signature: [mobility, redirect, displace]
        iconic_verbs: [drifts, carries, displaces, scatters]
        court_resonance: |
          "the forms that never stayed where the fight expected them, and
          never left the fight where it began"
        cosmological_commitment: |
          "kinetic rearrangement"
      genre_lineage: |
        D2 Druid Hurricane + Cyclone Armor + Tornado peak-mobility-build
        identity; D3 Wizard's "Galvanizing Ward" mobility-DPS variant
        keystones; PoE Whirling-Blades / Flicker-Strike speed-DPS keystones
        (Lightning-keyed canonically; wind-coded in our cosmology); Lost
        Ark Wardancer kinetic-DPS peak-identity build (the dancer that
        never stops moving).
      design_note: |
        L38 keystone-tier. Proportional bonus_damage_percent. Conditional
        scalar ("recent-distance-traveled in last ~3s"; cap at ~5-6 tiles
        or sim-units to prevent unbounded — gamora balance call). Reads
        as "wind wants the caster to be the wind." Pairs with Drift Mobility
        (movement-damage baseline) + Gust Grace (movement-CDR) for full
        "wind-caster as kinetic identity at peak power." Court resonance
        anchors at L38 — the substrate's mature voice is *the caster who
        has become their own substrate*.

```

### § 5.2 — Wind pool design audit

- **Floor cadence:** 2/2/2/2. ✓
- **Substrate signature realization:** all four `mechanical_signature` verbs (`displace` / `knockback` / `redirect` / `mobility`) have multiple traits realizing them. ✓ Displace + redirect + mobility receive heavy coverage (each in 5+ traits); knockback anchors the ailment-event side. ✓
- **Iconic verbs realization:** all 7 iconic_verbs cited across traits (displaces ×5, carries ×5, scatters ×4, lifts ×0 — surfaced in Drift Mobility as the cosmological-commitment quote rather than a verb in trait body — acceptable; redirects ×3, blows aside ×3, drifts ×4). Note: "lifts" appears in the substrate-identity-declarations iconic_verbs list but is *also* in earth's `forbidden_mechanics` ("lift"). The forbidden-mechanic refers to earth's refusal to lift-off-ground; wind's "lifts" iconic verb describes wind's *action upon what it carries* — these are not in conflict because wind acting upon what-it-carries is *wind's own substrate signature*, not earth violating its own refusal. The substrate-identity-declaration spec § 8.1 confirms forbidden_mechanics are *the substrate's own refusals*. ✓
- **Forbidden mechanics:** no trait introduces `anchor` (wind forbids), `root` (no root-application — Displaced Grace extends knockback recovery, not root duration), or `hold_ground` (no zone-conditional-on-zone-presence trait — Vortex Keystone uses path-of-passage which is *trajectory* not *held position*; Gust Grace uses ongoing-motion condition). ✓
- **Pillar coherence:** all traits reinforce KINETIC_REDIRECTION — knockback-extension (Displaced Grace), mobility-conditional damage (Drift Mobility, Stormrider Keystone), knockback-conditional damage (Kinetic Strike, Redirection), motion-CDR (Gust Grace), multi-knockback-CDR (Redirect Pulse), path-AOE (Vortex Keystone). Wind's mature voice is *the caster who has become their own motion*; the pool delivers that. ✓
- **Court resonance:** L38 Stormrider Keystone cites court_resonance ("forms that never stayed where the fight expected them, and never left the fight where it began"). ✓
- **Substrate-asymmetry with earth (cosmologically intentional):** earth's pool rewards *the caster who does not move* (Stoneward armor, Terrahold zone-HP, sustained-root scaling); wind's pool rewards *the caster who never stops moving* (Drift Mobility, Gust Grace, Stormrider Keystone). The earth↔wind anti-pole is mechanically the opposition between *stand-and-hold* and *never-stand-still*. This is *exactly* the substrate-pair valence the substrate-identity declarations promised; the canonical-four pools make the cosmological opposition mechanically legible. ✓

---

## § 6 — Cross-substrate coherence (canonical-four × canonical-four + canonical-four × new substrates)

### § 6.1 — Forbidden-mechanics audit across canonical-four pools

Every trait above is audited against every canonical-four substrate's `forbidden_mechanics`. Specifically:

- **Fire pool:** does any fire trait apply `drain` / `conceal` / `slow_channel`? **No.** Fire's pool is burn/area-persist/escalation-keyed; no life-leech (drain-forbidden), no concealment (no stealth/hide effects), no slow-channel (Hearth Persist + Firewell extend zone presence, not channel duration; Inferno Keystone scales damage with active-zones, not with channel-time-spent). ✓
- **Water pool:** does any water trait apply `ignite` / `sudden_strike` / `direct_burst`? **No.** Water's pool is chill/zone-AOE/patient-amplification-keyed; no fire DoT (ignite-forbidden), no burst-event amplifier (Chill Resonance uses damage-multiplier-on-chilled, not crit-on-chilled), no direct-burst conditional. ✓
- **Earth pool:** does any earth trait apply `displace` / `lift` / `sudden_traversal`? **No.** Earth's pool is root/anchor/hold-ground/mass-strike-keyed; no knockback (Pressure Strike + Anchor Resonance + Mountain Voice + Unyielding Keystone all use root-application or root-duration, never displacement), no caster-mobility (Stoneward is passive armor, Terrahold is zone-HP — neither grants movement-speed or teleport), no sudden-traversal (Groundswell's "adjacent-to-zone" allows casting from anywhere; doesn't move the caster). ✓
- **Wind pool:** does any wind trait apply `anchor` / `root` / `hold_ground`? **No.** Wind's pool is knockback/displacement/mobility-keyed; no root-application (Displaced Grace extends knockback recovery — the canonical wind "stagger" — not root duration), no anchor (Drift Mobility and Gust Grace REWARD motion; the inverse of anchor), no hold-ground (Vortex Keystone uses path-of-passage = trajectory; not zone-presence-conditional). ✓

### § 6.2 — Cross-pool audit: canonical-four pools × new-substrate pools (D8)

- **Fire pool × Lightning forbidden:** lightning forbids `[root, sustained_aura, ground_persist, slow_channel]`. Fire pool's area-persist traits (Hearth Persist, Firewell, Pyre Resonance, Inferno Keystone) reference `area_persist` which is fire's own signature, not lightning's `ground_persist` forbidden (different verbs in different substrate vocabularies). No conflict at the system level — fire's area-persist is fire's substrate identity, not a lightning-keyed mechanic. ✓
- **Fire pool × Holy forbidden:** holy forbids `[drain, conceal, corrupt, stealth]`. Fire pool has none of these. ✓
- **Fire pool × Shadow forbidden:** shadow forbids `[radiate, consecrate, amplify_allied, reveal]`. Fire pool has none of these. (Fire's "consumes" iconic verb is *destruction-of-target* not *radiance-from-caster*.) ✓
- **Water pool × Lightning forbidden:** no conflict — water's slow/chill/suffusion verbs are distinct from lightning's root/aura/ground/channel forbiddens. ✓
- **Water pool × Holy forbidden:** no conflict — water's pool is patient/amplification-coded but not *holy-amplify-allied* (water amplifies the *substrate's* effect, not allied-units' effects). ✓
- **Water pool × Shadow forbidden:** no conflict — water's "submerge" / "stills" verbs are *immersion-state-change* not *occlusion-state-removal*. ✓
- **Earth pool × Lightning forbidden:** **Soft tension flagged.** Earth pool's Terrahold + Groundswell reference earth-zone *ground-persist* (the player's earth zones persist on the ground). Lightning forbids `ground_persist`. **However:** earth's ground-persist is earth's own substrate signature (`hold_ground`); lightning's forbidden refers to lightning's own refusal to ground-persist. The forbidden_mechanics list is *the substrate's own refusals* per spec § 8.1 — lightning forbidding ground_persist means *lightning will not ground-persist*, not *no substrate may ground-persist around lightning*. No conflict at the system level. (Same as D8's soft-tension between lightning's "sudden traversal" cosmological commitment and earth's "sudden_traversal" forbidden_mechanic — flagged in D8 § 5.1; same resolution pattern.) ✓
- **Earth pool × Holy forbidden:** no conflict — earth's anchor/root/mass-strike verbs are distinct from holy's drain/conceal/corrupt/stealth forbiddens. ✓
- **Earth pool × Shadow forbidden:** no conflict — earth's hold-ground/mass-strike verbs are distinct from shadow's radiate/consecrate/amplify-allied/reveal forbiddens. ✓
- **Wind pool × Lightning forbidden:** **Soft tension flagged.** Wind pool's Drift Mobility + Gust Grace + Stormrider Keystone reward caster-motion; the wind substrate's cosmological commitment is "kinetic rearrangement." Lightning's cosmological commitment is "sudden traversal — what crosses gaps without crossing the space between." Both substrates' identities involve *motion* — but the substrate signatures differ: wind is *kinetic-via-displacement-and-redirection*; lightning is *kinetic-via-chain-and-discharge*. Wind moves *bodies*; lightning moves *current*. The substrate-identity declarations spec § 8.1 already addressed this asymmetry (fire and lightning both HIGH_BURST_LOW_PERSIST; differentiation lives in other fields). Same resolution applies to wind ↔ lightning: same pillar of motion, different mechanical bodies (wind = displace; lightning = chain). No actual forbidden_mechanic conflict; the rhetorical resonance is intended at the cosmological-identity layer. ✓
- **Wind pool × Holy forbidden:** no conflict — wind's displacement/mobility verbs are distinct from holy's drain/conceal/corrupt/stealth. ✓
- **Wind pool × Shadow forbidden:** no conflict — wind's redirect/scatter/displace verbs are distinct from shadow's radiate/consecrate/amplify-allied/reveal. ✓

**Net audit:** **CLEAN.** Two soft-tensions flagged (earth-pool ground-persist × lightning-forbidden ground-persist; wind-pool mobility-identity × lightning sudden-traversal cosmological-commitment). Both resolve cleanly under the spec's "forbidden_mechanics are the substrate's own refusals" principle. Jack-ryan continuous-observation may verify when code lands.

### § 6.3 — Substrate-identity-declaration cross-reference summary

Per the substrate-identity-declaration cross-reference protocol (D8 § 1.4 + § 5.3):

| Substrate | mechanical_signature realized | iconic_verbs cited | cosmological_commitment cited | court_resonance cited |
|---|---|---|---|---|
| Fire | ignite (5), escalate (6), area_persist (4), burn_apply (5) | 6 of 7 | 3 traits (L25 Firewell + L25 Pyre Resonance + L38 Inferno Keystone) | 1 trait (L38 Inferno Keystone) |
| Water | suffuse (5), permeate (4), chill_apply (5), slow (3) | 7 of 7 | 3 traits (L25 Undertow + L25 Glacial Pressure + L38 Deluge + L38 Tide Keystone explicitly = 4, plus cosmology cited indirectly in Suffuse Presence and Immersion Field at L1; counted as 3+ depending on quotation criterion) | 1 trait (L38 Tide Keystone) |
| Earth | anchor (5), root_apply (5), hold_ground (5), mass_strike (4) | 7 of 7 | 3 traits (L1 Stoneward + L25 Terrahold + L38 Unyielding Keystone) | 1 trait (L38 Unyielding Keystone) |
| Wind | displace (6), knockback (4), redirect (5), mobility (5) | 6 of 7 (lifts not body-cited; appears in declarations only) | 3 traits (L1 Drift Mobility + L25 Gust Grace + L38 Redirection + L38 Stormrider Keystone = 4) | 1 trait (L38 Stormrider Keystone) |

Per substrate-identity-declarations § 8.1 design discipline: "Mechanical signatures are short and substrate-distinguishing. No two substrates share signature verbs." Canonical-four traits respect this — no fire trait uses water's `suffuse` / earth's `anchor` / wind's `displace`; etc. ✓

### § 6.4 — Substrate-symmetric ailment-extension pattern

Across canonical-four + lightning + holy + shadow, the **L1 floor includes an ailment-extension trait for each substrate that has a duration-coded ailment** (per substrate-identity-declaration ailment_signature.category):

| Substrate | L1 ailment-extension trait | Ailment category |
|---|---|---|
| Fire | Kindling (control_duration_bonus → burn) | dot |
| Water | Suffuse Presence (control_duration_bonus → chill) | soft_control |
| Earth | Root Persist (control_duration_bonus → root) | hard_control |
| Wind | Displaced Grace (control_duration_bonus → knockback recovery) | hard_control (impulse-coded; trait extends recovery window not duration) |
| Lightning | — (D8 has no L1 ailment-extension; shock is brief; arc_initiate at L1 is chain-extension, the lightning-substrate analog) | hard_control (paralysis-on-arc) |
| Holy | Consecrate Walker at L1 extends consecrate RADIUS (radius-extension is holy's substrate-coherent analog to duration-extension) | amplification (novel category) |
| Shadow | Drain Sustain at L1 extends drain-via-lifesteal-economy (sustain-coded; not duration-extending — shadow's drain DoT is *withdrawing* per substrate-identity § 7) | dot |

The canonical-four pattern (L1 ailment-duration-extension) is structurally tight; the three new-substrate pools deviate at L1 in ways the substrate-identity declarations license (lightning's brief shock is anti-duration; holy's novel amplification needs radius-extension; shadow's withdrawing-drain needs lifesteal-economy). The asymmetry is *substrate-coherent*, not *substrate-inconsistent*. ✓

### § 6.5 — Substrate-symmetric mature-voice damage scaler pattern (L38 keystone)

Across canonical-four + new substrates, every substrate has a **mature-voice L38 STAT trait with `bonus_damage_percent` proportional**, scaled by a substrate-coherent condition:

| Substrate | L38 keystone scalar | Conditional |
|---|---|---|
| Fire | Inferno Keystone | ≥1 fire-area-persist zone active |
| Water | Tide Keystone | per distinct chilled enemy |
| Earth | Mountain Voice (also L38) | per distinct rooted enemy |
| Earth | Unyielding Keystone | continuous root duration on target |
| Wind | Redirection | per recent knockback event on target |
| Wind | Stormrider Keystone | recent-distance-traveled |
| Lightning | Courser (D8 § 2.1) | per-fight scaling on chain-activity |
| Holy | High Revelation (D8 § 3.1) | targets in consecrate zone for ≥2s |
| Shadow | Unmaking (D8 § 4.1) | cumulative drain duration on target |

The mature-voice damage-scaler is *substrate-symmetric at the architectural level* (every substrate has one at L38) and *substrate-distinguishing at the conditional level* (each substrate's scaler keys off the substrate's own combat-pillar identity). This is the substrate-symmetric depth Matt's Option I authorized; the canonical-four pools now match the three new-substrate pools at the keystone tier. ✓

---

## § 7 — Gamora implementation contract extension

This section extends D8 § 6 (gamora implementation contract) to cover the canonical-four pools. The infrastructure is shared — one loader, one schema, seven pool files.

### § 7.1 — Trait-pool registration extension

Per D8 § 6.1, gamora's preferred pattern is **Option A — YAML config files** at `reincarnated-engine/config/class_trait_pools/<class_name>.yaml`. Loader at `src/reincarnated/generation/trait_pool_loader.py` extracts pools at boot, Pydantic-validated, output `dict[str, ClassTraitPool]` keyed by class name.

**Extension for canonical-four:** the loader pattern is unchanged. Four new YAML files are derived from this doc:

- `config/class_trait_pools/fire_mage.yaml` (from § 2)
- `config/class_trait_pools/water_controller.yaml` (from § 3)
- `config/class_trait_pools/earth_caster.yaml` (from § 4)
- `config/class_trait_pools/wind_controller.yaml` (from § 5)

Combined with the three D8 pools, the loader manages **7 pool files total** = canonical-7 substrate-symmetric trait architecture.

### § 7.2 — Per-class trait roll logic at character generation (unchanged from D8)

Per D8 § 6.2, character-instantiation logic attaches all 8 pool traits to the character's intrinsic trait set (`source: "progression"`), floor-gated activation as character levels, per-rank scaling per canonical 32 § 4 + file 31 Stage 7. No changes for canonical-four — same pattern.

### § 7.3 — Cross-substrate-trait-coherence checks extension

Per D8 § 6.3, boot-time validation checks each trait's `anchors.mechanical_signature` against the substrate's declared `mechanical_signature`. **Extension for canonical-four:** the same validation runs against fire/water/earth/wind substrate identities — fail-loud on mismatch. § 6.1 + § 6.2 above pre-audited the canonical-four pools clean; gamora's runtime check is verification.

### § 7.4 — NEW ability_modifier_key required (canonical-four)

Canonical-four pools introduce **1 new ability-modifier key** beyond D8's 5:

```python
# Existing VALID_ABILITY_MODIFIER_KEYS (from trait_schema.py):
#   multishot_floor_bonus, cooldown_factor, energy_cost_factor,
#   crit_bonus_damage, aoe_radius_bonus, control_duration_bonus

# D8 additions (5 keys; from D8 § 6.4):
#   chain_targets_bonus, consecrate_radius_bonus, drain_lifesteal_fraction,
#   conceal_evasion_bonus, ailment_cleanse_factor

# D8-COMPANION (canonical-four) additions:
NEW_VALID_ABILITY_MODIFIER_KEYS_CANONICAL_FOUR = frozenset({
    "area_persist_duration_bonus",  # additive (seconds); extends FIELD-side
                                     # persistence of fire-area-persist zones
                                     # (fire walls, lingering flame zones, meteor
                                     # afterburn). Distinct from control_duration_bonus
                                     # which targets per-target ailment durations.
                                     # Used by: fire_t1_hearth_persist
                                     # Semantic: applied when constructing
                                     # area-persist ability instances; adds to base
                                     # duration of the zone. Sim-side: zone tick-loop
                                     # consults persisted duration field at instantiation.
                                     # Cap recommended at ~+3s (or ~50% of base zone
                                     # duration) to prevent unbounded-zone-pile builds.
})
```

**Total NEW keys (D8 + companion): 6.** Gamora adds `area_persist_duration_bonus` to `VALID_ABILITY_MODIFIER_KEYS` (NOT to `MULTIPLICATIVE_ABILITY_MODIFIER_KEYS` — additive composition per project_trait_architecture). ~3-line addition to trait_schema.py beyond the D8 extension.

**Why only 1 new key for canonical-four (vs 5 for new substrates):** per L3 briefing § 6 prediction, canonical-four substrates use well-trodden mechanical primitives. Fire's area-persist needed its own key because the substrate-identity declares `area_persist` as a `mechanical_signature` verb and no existing key encoded it (control_duration_bonus is for per-target ailment duration, not field-side zone persistence). Water, earth, and wind pools route through existing keys cleanly. The architecture's mechanical primitives are already substrate-aware for canonical-four.

### § 7.5 — Sim-side resolution requirements (canonical-four)

For the 1 new key (`area_persist_duration_bonus`), sim-side resolution logic in `simulation/balance_loop.py` or `simulation/damage_resolution.py` (gamora's call):

- **`area_persist_duration_bonus`:** consumed when constructing area-persist ability instances during combat. Adds N seconds to the base persist duration from the ability's `area_persist_duration` field (assumed exists per geometry-affinity ground_targeted_circle + area_sustain geometry). The zone's tick-loop consults the augmented duration at instantiation; no per-tick recomputation needed.

**Additional sim-side requirements introduced by canonical-four conditional traits:**

- **Movement-state read (wind):** Drift Mobility, Gust Grace, Stormrider Keystone all condition on caster's movement state (binary "is moving" for Drift Mobility / Gust Grace; recent-distance-traveled accumulator for Stormrider Keystone). Sim-side: combat sim already tracks position-tick deltas; gamora exposes a `combatant.is_moving` boolean and a `combatant.recent_distance_traveled_3s` accumulator. ~30 lines.
- **Path-of-passage tracking (wind):** Vortex Keystone conditions on cast-location being along the caster's recent (~2s) path. Sim-side: combat sim maintains a ring-buffer of caster positions; trait check uses point-on-path geometry. ~40 lines. Gamora may judge this too implementation-heavy and defer Vortex Keystone's path-condition to a "caster moving at cast-time" simpler proxy — surface as Q if friction.
- **Recent-knockback-window tracking (wind):** Kinetic Strike + Redirection condition on target's recent knockback events. Sim-side: combat sim already tracks ailment-application timestamps (per D5 ailment registry); extension is reading "last knockback applied within 1.5s" or accumulating "knockback events in last 3s." ~20 lines.
- **Zone-presence read (fire / earth):** Inferno Keystone (≥1 fire-area-persist zone active), Terrahold (caster in own earth zone), Groundswell (cast on/adjacent to own earth zone), Pyre Resonance (target in own fire-area-persist zone), Firewell (fire-area-persist condition on cast site). Sim-side: zone-tracker queried for substrate + caster-id; already exists for D5 ailment-zone resolution (consecrate / drain void-pools). Extension ~15 lines per condition; gamora may abstract a `zone_presence_check(caster, substrate, target_or_self)` helper.
- **Continuous-root-duration tracking (earth):** Unyielding Keystone scales with how long target has been *continuously* rooted by caster. Sim-side: combat sim tracks current ailment duration; addition needed for "duration since this caster first rooted target without lapse." ~20 lines.

**Total D8-companion-driven sim-side work: ~125 lines** (vs ~100 lines for D8 alone). Cumulative D8 + canonical-four sim work: ~225 lines. Bounded; well within gamora's existing B14.5-style balance-loop expansion scope.

### § 7.6 — Per-rank curve calibration (canonical-four)

Per D8 § 6.6, gamora's empirical balance work computes per-rank coefficients to satisfy B9a convergence at L50. The canonical-four pools introduce no new architectural calibration concerns — same coefficient-solving as the three D8 pools. Gamora's balance pass should ideally calibrate all 7 substrate pools together to ensure L50 convergence is cross-substrate-equivalent (per L3 briefing § 7 cascading-consequences "cross-substrate parity on per-rank curve calibration" watchpoint flagged for jack-ryan Discipline #13).

### § 7.7 — Effort estimate (gamora side, canonical-four extension)

Per L3 briefing § 3 estimate (canonical-four adds ~1-2 days to existing D8 ~6.5-day contract):

- YAML extraction from this doc to 4 new pool files: ~0.5 day (4 files; mechanical; same pattern as D8's 3 files)
- Trait-schema extension (1 NEW key): ~0.1 day (incremental)
- Sim-side wiring for 1 NEW key + 4 conditional-context infrastructures (movement-state read, path-of-passage tracking [or simpler proxy], recent-knockback-window tracking, zone-presence-check abstraction, continuous-root-duration tracking): ~1 day (some infrastructure reusable across substrates; conservative estimate)
- Boot-time validation extension for canonical-four: ~0.1 day (loader pattern reused)
- Per-rank curve coefficient calibration for canonical-four: ~0.5 day (within D8 calibration pass; small marginal cost)
- Cross-substrate L50 convergence validation (canonical-7 together): ~0.3 day

**Total: ~2.5 days additional gamora-side** (within L3 briefing § 3 estimate envelope of "+1-2 days"; slightly over the briefing's optimistic estimate; well within the briefing's "could grow" risk caveat). Combined D8 + canonical-four: ~6.5 + 2.5 = ~9 days gamora; ~3 days gandalf (D8 ~1.5 + canonical-four ~1.5). **Total combined: ~12 days**. Surface as gentle scope concern; not a blocker; below the L3 briefing § 3 worst-case ~1-week-additional envelope.

### § 7.8 — Open implementation Qs surfaced for gamora

These do not block design-side authoring; surfaced for gamora's implementation pass:

1. **Vortex Keystone path-of-passage tracking:** worth implementing the ring-buffer path-tracker, or defer to a simpler "caster moving at cast-time" proxy? Cosmologically, path-of-passage is more substrate-coherent (wind leaves the shape of its own passage); pragmatically, the simpler proxy preserves the kinetic-DPS intent without the path-geometry cost. Gamora's call.
2. **Recent-knockback-event accumulator cap:** Redirection caps at ~3-4 events per target. Is event-decay over 3s the right window, or should it be tied to combat-encounter ticks? Sim-side simplification call.
3. **Earth zone-conditional radius adjacency:** Groundswell's "on/adjacent to existing earth zone" needs adjacency-radius definition. Suggest ~2 tiles or sim-units; gamora confirm or adjust.
4. **Fire area-persist zone tracking:** Inferno Keystone scales when ≥1 fire-area-persist zone is active. The fire-area-persist tracker should identify zones spawned by *this caster* (not allied / not enemy). Sim-side filter required.

---

## § 8 — Cross-references

**Canonical inputs (this doc reads):**
- `canonical/story/d8-trait-floor-design-phase-1-p1.md` — parent doc; same architectural frame; three new-substrate pools (lightning + holy + shadow); this doc extends to canonical-four for substrate-symmetric canonical-7 coverage
- `canonical/story/substrate-identity-declarations-2026-05-17.md` § 1-4 — fire/water/earth/wind substrate identities (mechanical_signature, forbidden_mechanics, combat_pillar, ailment_signature, geometry_affinities, role_affinities, iconic_verbs, iconic_register, cosmological_commitment, court_resonance — all consumed)
- `canonical/32-progression-design.md` § 4 — trait-floor architecture (5-10 traits; floors at L1/12/25/38; converge at L50; auto-unlock auto-rank)
- `canonical/17-gear-and-spirit-guide-design.md` — trait infrastructure shared with gear
- `~/Games/reincarnated-engine/src/reincarnated/generation/trait_schema.py` — VALID_STAT_KEYS, VALID_ABILITY_MODIFIER_KEYS, MULTIPLICATIVE_ABILITY_MODIFIER_KEYS, TraitSpec dataclass
- `project_trait_architecture` (MEMORY.md) — dual-source architecture; intrinsic + gear-affix; rank-stacking across sources
- `agentic_orchestration/hive-mind/canonical-four-trait-pool-l3-decision-2026-05-18.md` — Matt's Option I authorization rationale; this doc instantiates the recommendation

**Companion D9 (gear-affix design):**
- `canonical/story/d9-gear-affix-design-phase-1-p1.md` — extends substrate-identity surface to gear; D9 informational soft-tension flags (canonical-four affix coherence vs intrinsic pools) close cleanly with this doc landing per L3 briefing § 7

**Companion deliverables blocked by / blocking this doc:**
- D5 (ailment registry) — burn / chill / root / knockback ailments already exist in pre-Phase-1-P1 state; no novel categories introduced by canonical-four pools (vs D8 which introduced consecrate amplification category)
- D7 (resistance matrix 7×7) — paired-luminance valence interacts with holy traits; canonical-four traits are anti-pole-paired (fire↔water; earth↔wind) per substrate-identity declarations; the resistance matrix is the canonical authority on valence
- D9 (gear-affix design) — extends same substrate-identity surface to gear; substrate-aware gear-affix-tagging shares architectural shape with the trait-affix architecture described here; canonical-four pools now feed cross-coherence verification against D9 audit

**Cross-canonical updates triggered by this doc (Phase-1 P1 follow-on):**
- `canonical/story/spirit-guide-voice.md` § "trait language" — Spirit Guide should speak about canonical-four traits when recommending optimal distributions; D8 follow-on rolled into D26 cross-doc updates
- `canonical/32-progression-design.md` § 4 — minor update noting D8 + this doc together constitute the first concrete trait-pool authoring instance for the canonical-7; canonical-four trait-pool authoring is no longer a Phase-1 P2 candidate (Option I authorization closes that thread); rolls into D26
- `canonical/story/cosmology-reincarnated.md` § Substrates (if exists) — canonical-four trait-pool depth at substrate-symmetric parity with new substrates; the wheel speaks all seven with equal voice; minor optional update

---

*Authored 2026-05-18 by gandalf in hive-mode Phase-1 P1 (Option I scope expansion authorized by Matt 2026-05-18). Four canonical-four substrate trait pools, 32 traits. The substrate identities become traits the player can wear from L1 to L50. Combined with D8's three new-substrate pools, the canonical-7 substrate-symmetric intrinsic trait architecture is complete; the wheel speaks all seven substrates with equal depth; the player returning to fire_mage after the substrate expansion finds fire feeling more alive, not less. Cross-substrate coherence verified clean against forbidden_mechanics. Gamora implementation contract extended to ~9 days total (D8 + canonical-four). The cosmology is honored.*
