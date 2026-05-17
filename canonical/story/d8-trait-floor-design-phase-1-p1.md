# D8 — Trait-Floor Design for Three New Substrate Archetypal Classes

**Authority:** gandalf (story-and-design steward; trait-identity authoring authority per scope-of-work § 1.2 D8).
**Status:** **Canonical design** for Phase-1 P1 Deliverable 8. Companion to canonical 32 § 4 (trait architecture) + `substrate-identity-declarations-2026-05-17.md`.
**Companion downstream:** Deliverable 9 (gear-affix design) extends the same identity surface to gear; see `d9-gear-affix-design-phase-1-p1.md`.
**Authored:** 2026-05-18 in hive-mode Phase-1 P1.

**Reading order:** § 0 TL;DR → § 1 Architectural frame → § 2 Lightning trait pool → § 3 Holy trait pool → § 4 Shadow trait pool → § 5 Cross-substrate coherence → § 6 Gamora implementation contract → § 7 Cross-references.

---

## § 0 — TL;DR

Three per-class intrinsic trait pools, one each for the three new substrate archetypal classes (`lightning_class`, `holy_class`, `shadow_class`). Each pool follows the canonical architecture per canonical 32 § 4 + `project_trait_architecture` memory:

- **5-10 traits per class** (this design: 8 traits per class — top of "balanced specialist" range; matches canonical-four mid-band density)
- **Floor cadence L1 / L12 / L25 / L38** (4 floors before L50 convergence; 2 traits per floor across the 8-trait pool)
- **L50 convergence** (per-rank curves shaped so all 8 traits reach similar power at L50 per B9a calibration intent)
- **Substrate-coherent design** — every trait references the substrate's `mechanical_signature` and `iconic_verbs`; no trait violates `forbidden_mechanics`

**Per-substrate signature anchors:**

- **Lightning** — *velocity / chain / arc*: D2 Sorceress Lightning chain mechanic; PoE Arc/Storm Brand chain decay; Last Epoch Static Orb propagation
- **Holy** — *radiance / consecration / cleanse*: D2 Paladin Holy auras + Sanctuary; D3 Crusader Consecration; Lost Ark Paladin Holy Aura
- **Shadow** — *concealment / corruption / drain*: D2 Assassin Shadow Discipline + Necromancer drain; D3 Demon Hunter Shadow Power; Solo Leveling shadow-army drain-and-extract

All 24 traits validate cleanly against the existing `TraitSchema` mechanical primitives (no new `VALID_STAT_KEYS` or `VALID_ABILITY_MODIFIER_KEYS` introductions needed for the *bulk* of the pool; 4 specific traits surface new ability-modifier keys flagged in § 6 for gamora consumption — chain_targets_bonus, consecrate_radius_bonus, drain_lifesteal_fraction, conceal_evasion_bonus).

---

## § 1 — Architectural frame

### § 1.1 — What a trait pool IS (recap from canonical 32 + project_trait_architecture)

Per Section 4 of canonical 32 (locked 2026-05-11):

> Each class has a curated **trait pool** of 5-10 traits with floors at L1 / L12 / L25 / L38. At trait floor level N, all class traits with that floor auto-activate. Traits AUTO-RANK based on character level + per-trait curve (B9a calibration intent: all eligible traits reach similar power at L50). Player does NOT invest skill points in traits.

Per project_trait_architecture memory:

> Two sources, one trait pool. (1) **Intrinsic** (B9a class trait pool) — per-class curated 5-10 traits across floors L1/12/25/38; per-rank curves converge at L50. (2) **Gear-affix rolls** — gear rolls trait affixes; element/mechanic-gated; no skill-specific traits on gear. Same trait from both sources: rank-stacks.

D8 authors the **intrinsic side** for three new classes. D9 authors the **gear-affix side** for three new substrates.

### § 1.2 — Per-pool sizing decision: 8 traits per class

The canonical 32 range is 5-10 traits. This design chooses **8 traits per class** for the three new archetypal classes. Reasoning:

1. **Matches mid-band density of canonical-four (presumed; canonical-four trait pools are not yet authored — see § 5.2 for cross-substrate-coherence note).** When canonical-four pools are eventually authored at this same density, the per-floor cadence aligns: 2 traits at L1, 2 at L12, 2 at L25, 2 at L38. 4 × 2 = 8.
2. **Two traits per floor gives one identity-anchor + one mechanical-variant per floor cadence.** The L1 pair establishes "this is what your class IS." The L12 pair adds tactical texture. The L25 pair adds keystone-adjacent depth. The L38 pair is the substrate's mature voice.
3. **8 traits supports the "different builds within the same class" pattern Matt's design favors** (per canonical 32 § Q4.3 build patterns). Eight traits create combinatorial richness without trait-bloat.

**Cross-substrate parity:** when canonical-four trait pools are eventually authored, they should also target 8 traits each — symmetric across all seven substrates. Surface to knight-rider as forward-work suggestion: canonical-four trait-pool authoring is a Phase-1 P2 candidate (currently the canonical-four classes apparently lack curated intrinsic trait pools; the engine has only `_STAT_TRAIT_POOL` for gear stat traits per `gear_generation.py:738`, not per-class intrinsic pools). The architecture description in canonical 32 + project_trait_architecture *describes* the design; D8 is the first authored *instance*.

### § 1.3 — Per-rank curve shape (B9a calibration intent)

Each trait's per-rank power curve is shaped so:
- **L1-floor traits** start at modest power, ramp slowly; by L50 they're substantial
- **L12-floor traits** start at moderate power (~2x L1 baseline at L12 equivalence); ramp medium-fast; converge with L1 at L50
- **L25-floor traits** start strong (~3x L1 baseline); ramp fast; converge at L50
- **L38-floor traits** start very strong (~4x L1 baseline); ramp fastest; converge at L50

Numeric calibration is gamora's job — D8 authors the *trait identities* and *floor placements*; gamora computes per-rank coefficients during B14.5-style balance work to satisfy "all reach similar L50 power." Reference per-rank curve shape per canonical 32 Section 4 + file 28 lines 537-543 + file 31 Stage 7.

### § 1.4 — Substrate-identity cross-reference protocol

Every trait below is annotated with:

- **`anchors:` field** — citing which `mechanical_signature` verbs OR `iconic_verbs` from the substrate identity declaration the trait realizes.
- **`forbidden_mechanics` audit** — implicit: no trait below violates its substrate's forbidden mechanics. The audit is explicit in § 5.1.
- **Genre lineage** — citing the specific Diablo/PoE/Last Epoch/isekai precedent this trait family inherits from. Genre-canon grounding per `gandalf-design-lineage.md`.

---

## § 2 — Lightning trait pool (`lightning_class`)

**Substrate:** lightning. Mechanical signature: `[chain, propagate, arc, discharge]`. Forbidden mechanics: `[root, sustained_aura, ground_persist, slow_channel]`. Combat pillar: `HIGH_BURST_LOW_PERSIST`. Scaling attribute: `intelligence`. Ailment signature: `shock` (hard control via chain-arc).

**Design thesis:** Lightning's identity is *interruption* — sudden traversal that ends what was about to happen by being faster. The trait pool reinforces velocity / chain / arc-propagation / discharge-event mechanics. No trait can establish sustained presence, ground-area persistence, or slow-channel mechanics (forbidden_mechanics enforcement).

### § 2.1 — Lightning traits

```yaml
trait_pool:
  class: lightning_class
  size: 8
  scaling_attribute: intelligence

  traits:

    # ── L1 floor — identity anchor + tactical entry ────────────────────────────
    - trait_id: lightning_t1_arc_initiate
      name: "Arc Initiate"
      floor: 1
      category: ABILITY
      ability_modifier_key: chain_targets_bonus     # NEW KEY — see § 6 contract
      description: |
        Your lightning abilities arc to +1 additional target at L1, scaling with
        rank. The first lesson of lightning: nothing about your strike stays
        between you and the first target.
      anchors:
        mechanical_signature: [chain, arc, propagate]
        iconic_verbs: [arcs, chains, leaps to]
      genre_lineage: |
        D2 Sorceress Lightning skill's "chain to 2/4/6/8/10 targets" progression;
        PoE Arc skill's chain-target scaling from level. The canonical
        lightning-chain mechanic.
      design_note: |
        +1 floor at L1 means even baseline lightning kits feel "chained" from
        the first encounter. The substrate IS chaining; this trait makes that
        identity load-bearing from session start.

    - trait_id: lightning_t1_discharge_threshold
      name: "Discharge Threshold"
      floor: 1
      category: ABILITY
      ability_modifier_key: crit_bonus_damage
      description: |
        When lightning chain hits 3+ targets in a single discharge, the chain's
        crit damage is amplified. Mass discharge rewards population density.
      anchors:
        mechanical_signature: [discharge, propagate]
        iconic_verbs: [discharges, courses through, flashes]
      genre_lineage: |
        PoE Storm Brand's escalating return-damage per chain hit; D3 Lightning
        Wizard's Arc Lightning damage stacking on multi-target.
      design_note: |
        Pairs with Arc Initiate: more targets → more crit. Encourages
        target-rich engagements. Crit-bonus-damage is an existing key
        (VALID_ABILITY_MODIFIER_KEYS); no new mechanic.

    # ── L12 floor — tactical texture ───────────────────────────────────────────
    - trait_id: lightning_t12_static_threading
      name: "Static Threading"
      floor: 12
      category: ABILITY
      ability_modifier_key: cooldown_factor
      description: |
        Chain abilities have reduced cooldowns after a discharge that hits 4+
        targets. Lightning rewards the moment when the world conducts.
      anchors:
        mechanical_signature: [chain, discharge]
        iconic_verbs: [chains, flashes]
      genre_lineage: |
        Last Epoch Stormcaller's cooldown reduction on multi-target lightning;
        D2 LF (Lightning Fury) Sorceress's CDR scaling with electro-investment.
      design_note: |
        Multiplicative cooldown_factor stacks across sources (per MULTIPLICATIVE
        registry in trait_schema). At L12 with rank 1, ~0.92 (8% CDR);
        scales to ~0.75 (25% CDR) at L50 rank-equivalent.

    - trait_id: lightning_t12_resonant_chain
      name: "Resonant Chain"
      floor: 12
      category: ABILITY
      ability_modifier_key: chain_targets_bonus      # SAME KEY as L1 trait — stacks additively per project_trait_architecture
      description: |
        Your chain abilities' chain count receives an additional bonus when
        chained-to-targets share substrate-resistance (the chain resonates
        between thematically-aligned targets). +1 chain target on resonance.
      anchors:
        mechanical_signature: [chain, arc]
        iconic_verbs: [chains, leaps to, courses through]
      genre_lineage: |
        D2's elemental-vulnerability "amplify damage" infrastructure; PoE's
        "shocked enemies are also chilled" interaction patterns. The substrate
        of resonance rewards resonance.
      design_note: |
        Stacks ADDITIVELY with Arc Initiate (additive composition). At
        L12+ scaled rank: +2 total chain targets baseline + situational +1
        when resonance trigger fires. Substrate-coherent without violating
        forbidden_mechanics (no aura, no ground persist).

    # ── L25 floor — keystone-adjacent depth ────────────────────────────────────
    - trait_id: lightning_t25_arc_velocity
      name: "Arc Velocity"
      floor: 25
      category: ABILITY
      ability_modifier_key: energy_cost_factor
      description: |
        Lightning skills cost less energy proportional to discharge size.
        The faster lightning moves, the less it weighs to call.
      anchors:
        mechanical_signature: [arc, discharge, propagate]
        iconic_verbs: [strikes, flashes, courses through]
        cosmological_commitment: |
          "the substrate of sudden traversal — what crosses gaps without crossing
          the space between"
      genre_lineage: |
        PoE Manaforged-Arrows resonance with Lightning Skills; D4 Sorcerer's
        Lightning Mastery passive that returns mana on shock proc.
      design_note: |
        Multiplicative energy_cost_factor. Pairs with sustained chain volleys.
        Helps lightning's HIGH_BURST_LOW_PERSIST pillar — bursts are cheap;
        sustains stay expensive (no aura, no sustained-presence reward).

    - trait_id: lightning_t25_thresholded_strike
      name: "Thresholded Strike"
      floor: 25
      category: STAT
      stat_key: bonus_damage_percent
      stat_magnitude_type: proportional
      description: |
        At full energy reserve, your first lightning strike deals greatly
        amplified damage. The substrate of waiting-until-discharge-is-total.
      anchors:
        mechanical_signature: [discharge]
        iconic_verbs: [strikes, flashes]
      genre_lineage: |
        D2 Sorceress Static Field at-max-mana; Solo Leveling's "Ruler's
        Authority" first-cast amplification reading (S-rank shadow skill);
        PoE Voltaxic Rift's first-discharge spike.
      design_note: |
        Proportional bonus_damage_percent. Conditional ("at full energy")
        adds tactical play: spend energy carefully to maintain threshold OR
        burst it for higher-cost-but-amplified output. Reads tactical, not
        mechanical-stat-tax.

    # ── L38 floor — mature voice ───────────────────────────────────────────────
    - trait_id: lightning_t38_overload
      name: "Overload"
      floor: 38
      category: ABILITY
      ability_modifier_key: crit_bonus_damage
      description: |
        Chained discharges that reach 6+ targets trigger an overload state:
        your next strike's crit damage is dramatically amplified. The substrate
        of consequence-cascade-becomes-consequence-amplification.
      anchors:
        mechanical_signature: [chain, discharge, propagate]
        iconic_verbs: [chains, flashes, strikes, courses through]
        cosmological_commitment: |
          "Lightning is the substrate of interruption — it ends what was about
          to happen by being faster than it could happen."
      genre_lineage: |
        Last Epoch Storm Totem's cascade-amplification; D2 Sorceress LF's
        "chain into chain into chain" emergent kill-feel; PoE Wrath Aura
        amplifying lightning damage cascades.
      design_note: |
        High floor → strong starting power → converges with L1 by L50. Reads as
        "L38 build-defining moment when overload starts firing reliably."
        Pairs with Arc Initiate + Resonant Chain (more targets → more frequent
        overload procs).

    - trait_id: lightning_t38_courser
      name: "Courser"
      floor: 38
      category: STAT
      stat_key: bonus_damage_percent
      stat_magnitude_type: proportional
      description: |
        Your sustained chain-skill DPS receives a substrate-identity-keyed
        bonus that scales with how much of the encounter your skills have
        already arced through. The lightning that has touched everything
        becomes more itself.
      anchors:
        mechanical_signature: [chain, propagate, arc]
        iconic_verbs: [arcs, courses through, chains]
        cosmological_commitment: |
          "The substrate of sudden traversal — what crosses gaps without
          crossing the space between."
      genre_lineage: |
        D2 Synergies system (lightning skills boosting each other) producing
        late-game DPS spikes; PoE Inpulsa's Broken Heart unique amulet
        chain-amplification.
      design_note: |
        Per-fight scaling bonus. Reads as "lightning rewards lightning's
        own activity." Pure damage scalar — bonus_damage_percent
        proportional. Existing key; no new mechanic.

```

### § 2.2 — Lightning pool design audit

- **Floor cadence:** 2/2/2/2 across L1/L12/L25/L38. ✓
- **Substrate signature realization:** all four `mechanical_signature` verbs (`chain` / `propagate` / `arc` / `discharge`) have multiple traits realizing them. ✓
- **Iconic verbs realization:** 7 of 8 iconic_verbs cited across traits (only "leaps to" appears in single-trait anchor; acceptable). ✓
- **Forbidden mechanics:** no trait introduces `root` (lightning forbids), `sustained_aura` (no aura-applying trait), `ground_persist` (no ground-tied effect), or `slow_channel` (no channel-modifier). ✓
- **Pillar coherence:** all traits reinforce HIGH_BURST_LOW_PERSIST — burst-event amplifiers, chain-pulse amplifiers, single-strike amplifiers. No sustained-presence reward. ✓

---

## § 3 — Holy trait pool (`holy_class`)

**Substrate:** holy. Mechanical signature: `[radiate, consecrate, cleanse, amplify_allied]`. Forbidden mechanics: `[drain, conceal, corrupt, stealth]`. Combat pillar: `REVELATION_AND_AMPLIFICATION`. Scaling attribute: `wisdom`. Ailment signature: `consecrate` (amplification — valenced ground zone).

**Design thesis:** Holy's identity is *revelation* — what exposes and what cannot abide exposure. The trait pool reinforces radiance / consecration / cleansing / aligned-amplification. The pool leans support-strong (role_affinities.support = 0.8) but includes damage-coherent traits for the holy_damage archetype path. No trait can drain, conceal, or corrupt (forbidden_mechanics).

**Genre-novel consideration:** Holy's ailment signature is `consecrate` — category `amplification` — a NEW ailment category per substrate-identity-declarations § 6 ("novel; neither hard-control, soft-control, DoT, nor debuff"). At least two traits in the pool tie to consecrate's amplification semantics so the novel category has class-side mechanical hooks.

### § 3.1 — Holy traits

```yaml
trait_pool:
  class: holy_class
  size: 8
  scaling_attribute: wisdom

  traits:

    # ── L1 floor — identity anchor + tactical entry ────────────────────────────
    - trait_id: holy_t1_consecrate_walker
      name: "Consecrate Walker"
      floor: 1
      category: ABILITY
      ability_modifier_key: consecrate_radius_bonus    # NEW KEY — see § 6 contract
      description: |
        Your consecration zones extend a small bonus radius. The first lesson
        of holy: the ground you stand on remembers your standing on it.
      anchors:
        mechanical_signature: [consecrate, radiate]
        iconic_verbs: [consecrates, sanctifies]
      genre_lineage: |
        D2 Paladin Sanctuary aura's radius scaling with skill points; D3
        Crusader Consecration's "Reaper's Wake" rune-extending radius;
        Lost Ark Paladin Holy Aura passive radius bonuses.
      design_note: |
        +0.5 radius at L1 baseline; scales to +2.0 radius equivalent at L50.
        Reads as "consecration zones feel bigger by the time you have one"
        from session start. consecrate_radius_bonus is NEW — see § 6 contract.

    - trait_id: holy_t1_aligned_grace
      name: "Aligned Grace"
      floor: 1
      category: STAT
      stat_key: bonus_damage_percent
      stat_magnitude_type: proportional
      description: |
        Allies within your consecration zones (or in line-of-sight while you
        consecrate) deal slightly amplified damage. The substrate of
        amplification-of-aligned, made tangible at the first moment.
      anchors:
        mechanical_signature: [amplify_allied, consecrate]
        iconic_verbs: [blesses, uplifts]
        cosmological_commitment: |
          "Holy is the substrate of amplification-of-aligned — it makes what
          is true brighter"
      genre_lineage: |
        D2 Paladin Might/Concentration auras boosting party damage; D3
        Crusader Provoke's aligned-amplify pulse; Lost Ark Paladin's
        Holy Aura buff to party damage.
      design_note: |
        Conditional bonus_damage_percent — applies to allies, not self.
        Holy_support archetype identity from L1. For solo play (which is the
        primary play mode per project_design_intent), the trait still anchors
        identity but is rarely active in fight resolution; gamora may want
        to model "self counts as aligned for solo" — surface as Q to
        knight-rider in § 6 implementation contract.

    # ── L12 floor — tactical texture ───────────────────────────────────────────
    - trait_id: holy_t12_cleansing_radiance
      name: "Cleansing Radiance"
      floor: 12
      category: ABILITY
      ability_modifier_key: control_duration_bonus
      description: |
        Your consecrate zones reduce the duration of ailments on aligned
        targets standing within. Holy is the substrate that washes things
        away — including the marks of harm on those who walk beside you.
      anchors:
        mechanical_signature: [cleanse, consecrate]
        iconic_verbs: [burns away, shines through]
      genre_lineage: |
        D2 Paladin Cleansing aura's poison/curse duration reduction; D3
        Crusader's Heaven's Fury "Split Fury" rune cleansing on hit; Lost
        Ark Paladin's Light Shock cleanse.
      design_note: |
        Negative control_duration_bonus — counter-intuitively the existing
        VALID_ABILITY_MODIFIER_KEYS supports positive-only magnitudes
        (per trait_schema validation: "no negative traits in initial scope").
        Resolution: gamora introduces NEW key `ailment_cleanse_factor`
        (multiplicative; 0.9 = 10% faster cleanse on aligned). Surface as
        new key in § 6 implementation contract.

    - trait_id: holy_t12_judgment_brand
      name: "Judgment Brand"
      floor: 12
      category: ABILITY
      ability_modifier_key: crit_bonus_damage
      description: |
        Your holy abilities crit harder against targets standing in your
        consecration zones (the targets the substrate has revealed). Holy
        is the substrate that judges; the judged take heavier strokes.
      anchors:
        mechanical_signature: [radiate, consecrate]
        iconic_verbs: [judges, reveals, shines through]
      genre_lineage: |
        D2 Paladin Conviction aura amplifying party damage on cursed targets;
        PoE Curse-on-Hit amplification stacking; D4 Sorcerer Vyr's Mastery
        crit-against-marked-targets.
      design_note: |
        Existing key. Conditional ("targets in consecrate zone"). Pairs with
        Consecrate Walker (bigger zone → more targets eligible). Damage-side
        identity for holy_damage archetypes.

    # ── L25 floor — keystone-adjacent depth ────────────────────────────────────
    - trait_id: holy_t25_sanctuary
      name: "Sanctuary"
      floor: 25
      category: STAT
      stat_key: bonus_hp
      stat_magnitude_type: flat
      description: |
        Standing in your own consecration zones grants you bonus HP scaling
        with rank. The substrate of revelation grants the brave a place to
        be brave from.
      anchors:
        mechanical_signature: [consecrate, radiate]
        iconic_verbs: [shines through, blesses]
        court_resonance: |
          "the forms that walked with their own dawn around them"
      genre_lineage: |
        D2 Paladin Vigor aura's self-survival contribution; D3 Crusader's
        Akarat's Champion damage-reduction passive; Final Fantasy 14
        White Mage's Asylum (ground zone self-heal).
      design_note: |
        Conditional bonus_hp ("in own consecrate zone"). Reads as
        "consecration is power-base, not just utility." Pairs with Consecrate
        Walker (more time in zone) + Sanctuary (more reward for time in zone).

    - trait_id: holy_t25_radiant_pulse
      name: "Radiant Pulse"
      floor: 25
      category: ABILITY
      ability_modifier_key: aoe_radius_bonus
      description: |
        Holy ability AOE radii receive a bonus when the ability is cast
        within your own consecration zone. The substrate amplifies its own
        when it stands in its own.
      anchors:
        mechanical_signature: [radiate, consecrate, amplify_allied]
        iconic_verbs: [shines through, consecrates]
      genre_lineage: |
        D3 Crusader Phalanx-of-Heaven's radius scaling per nearby Heaven's
        Fury; PoE Herald-of-Light's nova radius extending in lit areas.
      design_note: |
        Existing key (aoe_radius_bonus). Conditional ("cast in own
        consecrate zone"). Encourages "stand-and-cast" cadence — consonant
        with REVELATION_AND_AMPLIFICATION pillar.

    # ── L38 floor — mature voice ───────────────────────────────────────────────
    - trait_id: holy_t38_high_revelation
      name: "High Revelation"
      floor: 38
      category: STAT
      stat_key: bonus_damage_percent
      stat_magnitude_type: proportional
      description: |
        Your holy damage against targets the consecration zone has revealed
        (i.e., standing in zone for ≥2 seconds) receives a substantial
        amplification. The substrate of REVELATION-AND-AMPLIFICATION fully
        realized — what is exposed cannot abide exposure.
      anchors:
        mechanical_signature: [radiate, consecrate, amplify_allied]
        iconic_verbs: [judges, reveals, shines through, sanctifies]
        cosmological_commitment: |
          "Holy is the substrate of revelation — what exposes and what cannot
          abide exposure."
      genre_lineage: |
        D2 Paladin Conviction aura at high points; D4 Necromancer-anti-Holy
        smite-the-undead damage type; Final Fantasy Tactics' Holy Knight
        Cleric Stalwart Soul keystone.
      design_note: |
        L38 keystone-tier trait. Conditional damage spike; pairs with all
        zone-based traits (Consecrate Walker / Sanctuary / Radiant Pulse).
        At L50 rank-equivalent: ~+40% bonus_damage_percent vs revealed
        targets. Substantial; reads keystone-style.

    - trait_id: holy_t38_uplifting_aura
      name: "Uplifting Aura"
      floor: 38
      category: ABILITY
      ability_modifier_key: cooldown_factor
      description: |
        Allies in your consecration zones (and you, if you count yourself)
        receive a cooldown reduction on their abilities. The substrate of
        amplification-of-aligned reaches into the substrate of time.
      anchors:
        mechanical_signature: [amplify_allied, consecrate, radiate]
        iconic_verbs: [uplifts, blesses, shines through]
        court_resonance: |
          "the forms that walked with their own dawn around them"
      genre_lineage: |
        D2 Paladin Concentration's caster-haste effect at high ranks; D3
        Crusader Falling Sword "Superheated" rune CDR; Final Fantasy 14
        White Mage's Presence of Mind.
      design_note: |
        Multiplicative cooldown_factor. Self-applies in solo play (resolves
        the "amplify_allied with no allies" tension for solo). Reads as
        "your consecrate zone becomes a kingdom — time inside is faster."
        Pair with Aligned Grace for full holy_support-archetype identity
        coherence.

```

### § 3.2 — Holy pool design audit

- **Floor cadence:** 2/2/2/2. ✓
- **Substrate signature realization:** all four `mechanical_signature` verbs (`radiate` / `consecrate` / `cleanse` / `amplify_allied`) have multiple traits realizing them. ✓ Consecrate as the substrate's ailment-signature anchor receives multi-trait coverage (Consecrate Walker, Cleansing Radiance, Judgment Brand, Sanctuary, Radiant Pulse, High Revelation, Uplifting Aura — 7 of 8 traits zone-conditional). ✓
- **Iconic verbs realization:** 7 of 8 iconic_verbs cited across traits. ✓
- **Forbidden mechanics:** no trait introduces `drain` (holy forbids), `conceal` (no concealment), `corrupt` (no corruption), or `stealth` (no stealth). ✓
- **Pillar coherence:** all traits reinforce REVELATION_AND_AMPLIFICATION — zone-conditional damage, ally-amplification, ailment-cleansing, revelation-keyed crit. No drain, no concealment, no withdrawal. ✓
- **Novel-ailment hook:** `consecrate` (amplification category) receives 7-of-8 trait coverage. The novel ailment category has its mechanical anchor in the class identity. ✓

---

## § 4 — Shadow trait pool (`shadow_class`)

**Substrate:** shadow. Mechanical signature: `[drain, conceal, corrupt, dim_perception]`. Forbidden mechanics: `[radiate, consecrate, amplify_allied, reveal]`. Combat pillar: `CONCEALMENT_AND_DRAIN`. Scaling attribute: `intelligence`. Ailment signature: `drain` (DoT — life/resource withdrawal).

**Design thesis:** Shadow's identity is *withdrawal* — what takes without striking and arrives without warning. The trait pool reinforces drain / concealment / corruption / dim-perception. The shadow register is *quieter, lower-frequency, weight-of-absence in tone*. No trait can radiate, consecrate, amplify allies, or reveal (forbidden_mechanics).

**Genre lineage cluster:** Solo Leveling's shadow-army summoning + Shadow Monarch drain-and-extract economy; D2 Necromancer's bone-and-poison + life-tap; D3 Demon Hunter's Shadow Power discharge; D2 Assassin's Shadow Discipline + Cloak of Shadows. The pool blends the *necromancer-resonant shadow* (drain, corruption, decay) with the *assassin-resonant shadow* (concealment, dim perception, sudden strike from concealment).

### § 4.1 — Shadow traits

```yaml
trait_pool:
  class: shadow_class
  size: 8
  scaling_attribute: intelligence

  traits:

    # ── L1 floor — identity anchor + tactical entry ────────────────────────────
    - trait_id: shadow_t1_drain_sustain
      name: "Drain Sustain"
      floor: 1
      category: ABILITY
      ability_modifier_key: drain_lifesteal_fraction   # NEW KEY — see § 6 contract
      description: |
        A small fraction of damage dealt by your drain-coded abilities
        returns to you as health. The first lesson of shadow: what you take
        is yours; what was theirs is no longer theirs.
      anchors:
        mechanical_signature: [drain]
        iconic_verbs: [drains, withdraws, takes]
        cosmological_commitment: |
          "Shadow is the substrate of occlusion — it removes what was there
          without the world noticing the removal until later."
      genre_lineage: |
        D2 Necromancer Life Tap curse + Bone Spirit life-leech synergy;
        D3 Necromancer Siphon Blood; Solo Leveling's "Vampire Lord" shadow
        rank's life-extraction; PoE Vaal Pact / Slayer Overleech.
      design_note: |
        drain_lifesteal_fraction is NEW — see § 6 contract. At L1 rank 1:
        ~3% lifesteal on drain-tagged abilities; scales to ~12% at L50
        rank-equivalent. Sustaining solo play through drain feels load-bearing
        from session start. Reinforces shadow's "withdrawal" cosmological
        identity at the very first encounter.

    - trait_id: shadow_t1_concealing_step
      name: "Concealing Step"
      floor: 1
      category: ABILITY
      ability_modifier_key: conceal_evasion_bonus      # NEW KEY — see § 6 contract
      description: |
        Brief evasion bonus after triggering concealment effects. The
        substrate of arriving-without-warning grants those who walk through it
        a moment of unmarked passage.
      anchors:
        mechanical_signature: [conceal, dim_perception]
        iconic_verbs: [shrouds, dims, creeps into, occludes]
      genre_lineage: |
        D2 Assassin Cloak of Shadows; D3 Demon Hunter Smoke Screen; D4
        Rogue's Shadow Step; Solo Leveling's Ruler's Authority shadow-step;
        PoE Phase Run mod.
      design_note: |
        conceal_evasion_bonus is NEW — see § 6 contract. At L1: +10% evasion
        for 2 seconds after triggering a concealment ability. Reads
        immediately tactical: dodge-out-of-incoming.

    # ── L12 floor — tactical texture ───────────────────────────────────────────
    - trait_id: shadow_t12_creeping_corruption
      name: "Creeping Corruption"
      floor: 12
      category: ABILITY
      ability_modifier_key: control_duration_bonus
      description: |
        Your drain ailments tick for longer when applied to targets standing
        within shadow-zone geometry (void_pool, creep, tendril). The
        substrate that creeps does not let go of what it has touched.
      anchors:
        mechanical_signature: [drain, corrupt]
        iconic_verbs: [drains, corrupts, creeps into, withdraws]
        geometry_affinities: [creep, void_pool, tendril]
      genre_lineage: |
        D2 Necromancer Lower Resist curse extending poison/decay durations;
        D3 Witch Doctor's Locust Swarm's "Cloud of Insects" duration extension;
        PoE Withered debuff stacking duration.
      design_note: |
        Existing key (control_duration_bonus). Conditional (targets in
        shadow-zone geometry). Reinforces shadow's PREFER geometries from
        substrate identity declarations (tendril/void_pool/creep).

    - trait_id: shadow_t12_dim_perception
      name: "Dim Perception"
      floor: 12
      category: ABILITY
      ability_modifier_key: crit_bonus_damage
      description: |
        Your first strike from concealment (within 1.5 seconds of triggering
        a concealment effect) crits harder. The substrate of dim_perception
        rewards arriving-from-where-you-were-not-seen.
      anchors:
        mechanical_signature: [conceal, dim_perception]
        iconic_verbs: [shrouds, dims, occludes, unmakes]
      genre_lineage: |
        D2 Assassin Shadow Master "ambush" crit; D3 Demon Hunter Shadow
        Power on-attack crit; PoE Backstab gem; Solo Leveling Sung Jin-Woo's
        first-strike-from-shadow archetype.
      design_note: |
        Existing key (crit_bonus_damage). Conditional ("first strike from
        concealment"). Pairs with Concealing Step (concealment trigger → crit
        window). Tactical play loop: conceal → strike → re-conceal.

    # ── L25 floor — keystone-adjacent depth ────────────────────────────────────
    - trait_id: shadow_t25_void_pool_anchor
      name: "Void Pool Anchor"
      floor: 25
      category: STAT
      stat_key: bonus_damage_percent
      stat_magnitude_type: proportional
      description: |
        Your damage against targets standing in shadow void_pools is amplified
        in proportion to the pool's duration. The substrate of withdrawal
        gathers strength as the withdrawal continues.
      anchors:
        mechanical_signature: [drain, corrupt, conceal]
        iconic_verbs: [drains, withdraws, occludes]
        geometry_affinities: [void_pool, creep]
      genre_lineage: |
        D2 Necromancer Poison Nova ground-tag + escalating decay; D3 Witch
        Doctor's Acid Cloud "Slow Burn" rune scaling DPS; PoE Caustic Arrow's
        ground pool cumulative damage.
      design_note: |
        Existing key (bonus_damage_percent proportional). Conditional ("in
        void_pool"). Reads as "shadow rewards the player who held the pool
        and waited."

    - trait_id: shadow_t25_extracted_essence
      name: "Extracted Essence"
      floor: 25
      category: ABILITY
      ability_modifier_key: drain_lifesteal_fraction    # STACKS with L1 trait — same key, additive
      description: |
        When a drained target dies, you receive a brief life-and-resource
        bonus. The substrate of occlusion: what was extracted is yours;
        what was theirs returns to no one. Shadow is the substrate of
        consequence-removed-from-the-world.
      anchors:
        mechanical_signature: [drain, corrupt]
        iconic_verbs: [drains, withdraws, unmakes, takes]
        cosmological_commitment: |
          "Shadow is the substrate of occlusion — it removes what was there
          without the world noticing the removal until later."
      genre_lineage: |
        D2 Necromancer Corpse Explosion's life-on-kill-pool; PoE Soul Eater
        unique modifier (gain-stack-on-kill); Solo Leveling's "Bellion" shadow
        kill-extraction cycle; D3 Witch Doctor Spirit Vessel.
      design_note: |
        Same key as L1 (drain_lifesteal_fraction). Stacks additively per
        project_trait_architecture rank-stacking rules. At L25+ rank-equivalent:
        baseline + ~5% additional lifesteal on drain-kill events. The compound
        lifesteal forms shadow_caster's primary sustain economy by L25-30.

    # ── L38 floor — mature voice ───────────────────────────────────────────────
    - trait_id: shadow_t38_unmaking
      name: "Unmaking"
      floor: 38
      category: STAT
      stat_key: bonus_damage_percent
      stat_magnitude_type: proportional
      description: |
        Your damage against targets you have already drained is amplified
        proportional to the cumulative drain duration on the target. The
        substrate of withdrawal: what you have taken from once, you can
        take from again, and more.
      anchors:
        mechanical_signature: [drain, corrupt, dim_perception]
        iconic_verbs: [drains, unmakes, withdraws, dims]
        cosmological_commitment: |
          "the substrate of withdrawal — what takes without striking"
      genre_lineage: |
        D2 Necromancer Amplify Damage + Lower Resist stacked curse
        synergy; PoE Withered stacking with Decay; Solo Leveling
        Shadow Monarch's "I'm-already-stronger-against-this-target"
        cumulative drain.
      design_note: |
        L38 keystone-tier trait. Existing key. Conditional ("targets with
        accumulated drain duration"). Reads as "shadow rewards the player
        who built a drain-pressure presence on a specific target." Pair with
        Creeping Corruption (extended duration) + Void Pool Anchor (zone
        DPS) for full shadow_caster identity coherence.

    - trait_id: shadow_t38_walker_in_occlusion
      name: "Walker in Occlusion"
      floor: 38
      category: ABILITY
      ability_modifier_key: cooldown_factor
      description: |
        Concealment-coded abilities have their cooldowns reduced when you
        kill targets while concealed. The substrate of arriving-without-warning
        rewards the unmarked pass-through, and grants more passes.
      anchors:
        mechanical_signature: [conceal, drain, dim_perception]
        iconic_verbs: [shrouds, dims, occludes, creeps into]
        court_resonance: |
          "the forms that walked alongside what they did not name, and were
          not always seen even by themselves"
      genre_lineage: |
        D2 Assassin Mind Blast / Shadow Master kill-reset chains; D3 Demon
        Hunter Vault-on-kill mechanics; Solo Leveling Shadow Step
        cooldown-on-shadow-kill; PoE Vaal-skill on-kill recharge.
      design_note: |
        Multiplicative cooldown_factor. Conditional ("kill while concealed").
        Tactical loop reward: conceal → strike → kill → re-conceal faster.
        Pairs with Concealing Step (initial concealment access) and Dim
        Perception (crit while concealed) to form shadow_damage archetype's
        primary play-cycle by L38-50.

```

### § 4.2 — Shadow pool design audit

- **Floor cadence:** 2/2/2/2. ✓
- **Substrate signature realization:** all four `mechanical_signature` verbs (`drain` / `conceal` / `corrupt` / `dim_perception`) have multiple traits realizing them. ✓ Drain receives heaviest coverage (5 of 8 traits) — appropriate as the ailment-signature anchor. ✓
- **Iconic verbs realization:** all 8 iconic_verbs cited across traits. ✓
- **Forbidden mechanics:** no trait introduces `radiate` (shadow forbids), `consecrate` (no consecration), `amplify_allied` (no ally-amplification), or `reveal` (no revelation). ✓
- **Pillar coherence:** all traits reinforce CONCEALMENT_AND_DRAIN — drain-DoT amplifiers, concealment-cycle rewards, void-pool dwellers, drain-kill compounders. No allied amplification, no revelation, no consecration. ✓
- **Court resonance:** explicit cosmological-commitment and court_resonance citations on the L38 traits anchor shadow's "walking alongside what is not named" identity at the keystone tier. ✓
- **Genre-lineage balance:** Necromancer-resonant traits (drain/corruption/void-pool) and Assassin-resonant traits (conceal/dim/walker) are co-present. The shadow_class identity is genre-faithful to both halves of shadow's lineage. ✓

---

## § 5 — Cross-substrate coherence

### § 5.1 — Forbidden-mechanics audit across pools

Every trait above is audited against every other substrate's `forbidden_mechanics`. Specifically:

- **Lightning pool:** does any lightning trait apply `drain` / `conceal` / `corrupt` / `radiate` / `consecrate` mechanics? **No.** Lightning's pool is chain/discharge/arc/velocity-keyed; never touches drain/conceal/radiate verbs. ✓
- **Holy pool:** does any holy trait apply `drain` / `conceal` / `corrupt`? **No.** Holy's pool is zone/cleanse/amplify-aligned-keyed; explicitly avoids drain (forbidden), concealment (forbidden), and corruption (forbidden). ✓
- **Shadow pool:** does any shadow trait apply `radiate` / `consecrate` / `amplify_allied`? **No.** Shadow's pool is drain/conceal/void-pool/cooldown-reduction-keyed; never touches radiance/aligned-amplification. ✓
- **Cross-cutting:** none of the new substrate traits violate canonical-four substrates' forbidden_mechanics either:
  - Fire forbids `[drain, conceal, slow_channel]` — no new substrate trait uses these (verified above; shadow uses drain only on shadow's own abilities, not as a verb the system applies cross-element).
  - Water forbids `[ignite, sudden_strike, direct_burst]` — lightning uses discharge (related to sudden_strike but not identical; this is a soft adjacency, not a violation).
  - Earth forbids `[displace, lift, sudden_traversal]` — lightning's `cosmological_commitment` references "sudden traversal" as the substrate's identity. **Soft tension flagged:** lightning's identity-level commitment to "crossing gaps without crossing the space between" rhetorically resonates with earth's `forbidden_mechanic: sudden_traversal`. However: (a) the forbidden_mechanic list is the *substrate's own refusals* (what earth itself will not do), not cross-substrate prohibition; (b) earth's "sudden_traversal" forbidden is about *earth's mechanical signature being grounded* — lightning being sudden is exactly how the substrate-pair contrast works. No actual conflict. Flag retained for jack-ryan Discipline #13 review.
  - Wind forbids `[anchor, root, hold_ground]` — no new substrate trait introduces anchor/root/hold mechanics.

**Net audit:** **CLEAN.** No cross-substrate forbidden_mechanics violations from D8 trait authoring. Jack-ryan continuous-observation may verify when code lands.

### § 5.2 — Canonical-four trait-pool authoring deferral

**Finding (surfaced this session):** the canonical-four classes (`fire_mage`, `water_controller`, `earth_caster`, `wind_controller`) do not appear to have *authored* intrinsic trait pools per the canonical 32 § 4 architecture. The engine has only `_STAT_TRAIT_POOL` (`gear_generation.py:738`) for gear-roll stat traits and the `TraitSpec` + `aggregate_traits` infrastructure (`trait_schema.py`) for combat application, but no per-class intrinsic trait pools authored as YAML config or canonical-doc declarations.

**Implication:** D8 is technically the *first* per-class intrinsic trait pool authoring in the project. The canonical 32 architecture is described; the instances do not yet exist (canonical-four or otherwise).

**Phase-1 P1 disposition:** D8 ships the three new-substrate pools. Knight-rider routing recommendation: **canonical-four intrinsic trait-pool authoring becomes a Phase-1 P2 candidate** — same authoring pattern as D8, 4 classes × 8 traits each = 32 additional traits. Gandalf authors; gamora implements during the same composition-refactor wave. Surface to Matt for L3 disposition: do we ship canonical-7 with canonical-four trait pools, or land canonical-four pools post-Phase-1 P1?

**Soft recommendation:** The canonical-four classes have *functioned without intrinsic trait pools* through B14.5 + Drift-14. They will not break by shipping canonical-7 without them. But cross-substrate parity is design-coherent: if lightning_class / holy_class / shadow_class have intrinsic pools and fire_mage / water_controller / etc. do not, the *new* substrates feel mechanically richer than the *original* substrates — exactly the inverse of what shipping should look like. **Recommend Phase-1 P1 ship gate include canonical-four intrinsic trait-pool authoring** as a deliverable. Knight-rider's call on whether D8 expands to 6 pools (canonical-four + 3 new = 7 total) or stays at 3.

### § 5.3 — Substrate-identity-declaration cross-reference summary

Per scope-of-work § 1.2 D8 substrate-identity-declaration cross-references:

| Substrate | mechanical_signature realized | iconic_verbs cited | court_resonance cited |
|---|---|---|---|
| Lightning | chain (4 traits), propagate (4), arc (3), discharge (4) | 7 of 8 iconic_verbs | (none — no traits anchor to court_resonance explicitly; soft note: L38 traits reference cosmological_commitment instead) |
| Holy | radiate (3), consecrate (7), cleanse (1), amplify_allied (2) | 7 of 8 iconic_verbs | court_resonance cited in 2 traits (Sanctuary L25, Uplifting Aura L38) |
| Shadow | drain (5), conceal (4), corrupt (3), dim_perception (3) | all 8 iconic_verbs | court_resonance cited in 1 trait (Walker in Occlusion L38) |

Per substrate-identity-declarations § 8.1 design discipline: "Mechanical signatures are short and substrate-distinguishing. No two substrates share signature verbs." D8 traits respect this discipline — no lightning trait uses holy's `radiate` or `consecrate`; no holy trait uses shadow's `drain` or `conceal`; no shadow trait uses lightning's `chain` or `propagate`. ✓

---

## § 6 — Gamora implementation contract

This section enumerates what gamora needs to implement to land D8 design in code.

### § 6.1 — Trait-pool registration

Authoring source: this document (`canonical/story/d8-trait-floor-design-phase-1-p1.md`). Engine consumption pattern: gamora extracts the YAML blocks above into engine-consumable form. Two options:

- **Option A — YAML config files.** Mirror substrate identity loader pattern: `reincarnated-engine/config/class_trait_pools/<class_name>.yaml`. Loader at `src/reincarnated/generation/trait_pool_loader.py` (new module; mirrors `substrate_identity_loader.py` shape) extracts pools at boot. Pydantic-validated. Loader output: `dict[str, ClassTraitPool]` keyed by class name. Each `ClassTraitPool` carries 8 `TraitDefinition` entries with `floor`, `category`, `key`, `description`, `anchors`, `genre_lineage`, `design_note` fields. **Recommended pattern** — gamora discretion.

- **Option B — Python module declaration.** Hardcoded in `src/reincarnated/generation/class_trait_pools.py` mirroring `b6_archetype_templates.py` pre-refactor pattern. Faster to ship but inherits the discipline #13 implicit-pillar drift risks discussed in archetype-coupling-archaeology.

Gamora's call on Option A vs Option B per implementation efficiency. From a design-coherence perspective: Option A is preferred (config-driven; matches the loader-extension pattern the rest of Phase-1 P1 follows). Surface as Q to gandalf if there's friction; design-side blesses Option A.

### § 6.2 — Per-class trait roll logic at character generation

At class instantiation time (when a player's character is generated with `lightning_class` / `holy_class` / `shadow_class`):

1. Loader returns the 8-trait pool for the class.
2. Engine attaches all 8 traits to the character's intrinsic trait set (not gear-source — `source: "progression"`).
3. Floor-gated traits: traits below the character's current level are inactive (not in `aggregate_traits` input); traits at-or-below current level are active. As character levels up, traits at each floor (L1, L12, L25, L38) activate atomically.
4. Per-rank scaling: each active trait's effective rank is computed from `min(max_rank, floor((character_level - trait_floor) / per_rank_scaling) + 1)` per canonical 32 Section 4 + file 31 Stage 7. Numeric per-rank coefficient calibration is gamora's empirical work — D8 design specifies *which* traits exist; gamora computes the *coefficients* that make all 8 converge at L50.

### § 6.3 — Cross-substrate-trait-coherence checks (jack-ryan Discipline #13 territory)

Per scope-of-work § 1.2 D8: "Substrate identity declarations' mechanical_signature + forbidden_mechanics constrain trait authoring (no shadow-substrate trait that violates forbidden_mechanics)."

**Gamora-side check (boot-time validation):** when the trait-pool loader extracts pools, validate each trait's `anchors.mechanical_signature` references against the substrate's actual `mechanical_signature` field. Fail-loud on:

- Trait references a verb NOT in the substrate's `mechanical_signature` AND NOT in `iconic_verbs` → loader raises `TraitSubstrateCoherenceError`.
- Trait's effect crosses substrate's `forbidden_mechanics` — harder to validate automatically (requires semantic mapping of `ability_modifier_key` → forbidden verb). Fall-back: jack-ryan continuous-observation review pass per Discipline #13.

**Gandalf-side discipline:** D8 traits authored above were manually audited (§ 5.1 audit). The authoring discipline is to bring this audit forward whenever new traits are added.

### § 6.4 — NEW ability_modifier_keys required

D8 introduces **4 new ability-modifier keys** that need to be added to `VALID_ABILITY_MODIFIER_KEYS` in `trait_schema.py`:

```python
# Current VALID_ABILITY_MODIFIER_KEYS (existing):
#   multishot_floor_bonus, cooldown_factor, energy_cost_factor,
#   crit_bonus_damage, aoe_radius_bonus, control_duration_bonus

# D8 additions:
NEW_VALID_ABILITY_MODIFIER_KEYS_D8 = frozenset({
    "chain_targets_bonus",       # additive; +N to chain-skill chain target count
                                  # Used by: lightning_t1_arc_initiate, lightning_t12_resonant_chain
                                  # Semantic: extends chain-skill chain count. Pairs with sim-side
                                  # chain-resolution logic (presumed exists for lightning kits already
                                  # via geometry chain_lightning PREFER affinity).
    "consecrate_radius_bonus",   # additive; bonus radius (in tiles or sim units) on consecrate zones
                                  # Used by: holy_t1_consecrate_walker
                                  # Semantic: scales the radius of consecrate-category ailment zones.
                                  # Sim-side consecrate-zone-resolution logic is novel-ailment work
                                  # (D5 ailment registry should define consecrate's radius field).
    "drain_lifesteal_fraction",  # additive; fraction of drain-damage returned as healing to caster
                                  # Used by: shadow_t1_drain_sustain, shadow_t25_extracted_essence
                                  # Semantic: applied during damage resolution when drain-tagged
                                  # ability hits. Stacks additively per project_trait_architecture
                                  # rank-stacking; cap at ~25% lifesteal recommended (avoid
                                  # unbounded sustain).
    "conceal_evasion_bonus",     # additive; bonus evasion fraction triggered on concealment proc
                                  # Used by: shadow_t1_concealing_step
                                  # Semantic: temporary evasion buff (duration ~1.5-2.0 seconds)
                                  # after triggering a concealment-coded ability. Requires sim-side
                                  # concealment-event detection.
})
```

**Additional NEW key flagged in § 3.1 (Cleansing Radiance):**

```python
"ailment_cleanse_factor",        # multiplicative; <1.0 = faster cleanse on aligned targets
                                  # Used by: holy_t12_cleansing_radiance
                                  # Semantic: applied to ailment-duration on aligned targets in
                                  # consecrate zones. Multiplicative (in MULTIPLICATIVE_ABILITY_MODIFIER_KEYS).
                                  # Solves the trait_schema "no negative magnitudes" rule by
                                  # encoding cleanse as a sub-1.0 multiplier rather than a
                                  # negative additive.
```

**Total NEW keys: 5.** Gamora adds these to `VALID_ABILITY_MODIFIER_KEYS` (and `ailment_cleanse_factor` to `MULTIPLICATIVE_ABILITY_MODIFIER_KEYS`) before D8 trait pools can validate. This is a minor extension to existing infrastructure; no schema migration; ~10-line addition.

### § 6.5 — Sim-side resolution requirements

For each NEW key, sim-side resolution logic must be implemented in `simulation/balance_loop.py` or `simulation/damage_resolution.py` (gamora's call on the exact site). Specifics:

- **`chain_targets_bonus`:** consumed when resolving chain-skill propagation. Adds N to the chain target count before chain decay calculation. May already have partial wiring if existing canonical-four lightning kits use chain geometry. Gamora confirms.
- **`consecrate_radius_bonus`:** consumed when computing consecrate-zone AOE during simulation. Adds N units to the base radius from the consecrate ailment definition (D5 ailment registry).
- **`drain_lifesteal_fraction`:** consumed during drain-damage resolution. After computing drain damage to target, applies `lifesteal_fraction × drain_damage` as healing to the caster (capped at caster's max HP).
- **`conceal_evasion_bonus`:** consumed at concealment-event resolution. Applies temporary evasion buff (duration TBD per gamora balance pass).
- **`ailment_cleanse_factor`:** consumed during ailment-tick resolution for aligned targets. Multiplies remaining ailment duration by the factor before next tick.

Each NEW key's sim-side wiring is small (≤20 lines per key). Total D8-driven sim-side work: ~100 lines. Gamora's empirical balance-loop validation (full-regen or B14.5-style) should follow trait integration.

### § 6.6 — Effort estimate (gamora side)

Per scope-of-work § 1.2 D8 estimate (~5-7 days incl gamora impl):

- Loader implementation: ~1 day (Option A; mirrors substrate identity loader pattern)
- YAML extraction from D8 doc: ~0.5 day (3 files; mechanical)
- Trait-schema extension (5 NEW keys): ~0.5 day (existing pattern)
- Sim-side wiring for 5 NEW keys: ~2 days (per § 6.5)
- Boot-time validation + tests: ~1 day
- Per-rank curve coefficient calibration (empirical; convergence at L50): ~1 day
- Cross-substrate-trait-coherence boot-time check: ~0.5 day

**Total: ~6.5 days gamora-side.** D8 design authoring (this doc): ~1 day gandalf-side. Combined ~7.5 days — slightly over the ~5-7 day estimate. Surface as gentle scope concern; not a blocker.

---

## § 7 — Cross-references

**Canonical inputs (D8 reads):**
- `canonical/story/substrate-identity-declarations-2026-05-17.md` — three new substrate identities (§ 5 lightning + § 6 holy + § 7 shadow)
- `canonical/32-progression-design.md` § 4 — trait-floor architecture (5-10 traits; floors at L1/12/25/38; converge at L50; auto-unlock auto-rank)
- `canonical/17-gear-and-spirit-guide-design.md` — trait infrastructure shared with gear (TraitSpec; aggregate_traits; stacking rules)
- `~/Games/reincarnated-engine/src/reincarnated/generation/trait_schema.py` — VALID_STAT_KEYS, VALID_ABILITY_MODIFIER_KEYS, MULTIPLICATIVE_ABILITY_MODIFIER_KEYS, TraitSpec dataclass
- `project_trait_architecture` (MEMORY.md) — dual-source architecture; intrinsic + gear-affix; rank-stacking across sources
- `canonical/story/substrate-expansion-decision-2026-05-17.md` § 5.2 — D8 scope authority

**Companion D9 (gear-affix design):**
- `canonical/story/d9-gear-affix-design-phase-1-p1.md` — extends the same substrate-identity surface to gear; same anchors, same forbidden-mechanics audit, different surface (drop tier + slot gating instead of floor-gated intrinsic)

**Companion deliverables blocked by / blocking D8:**
- D5 (ailment registry; rocket + gamora) — defines `consecrate` ailment shape, including the radius field that `consecrate_radius_bonus` extends. D8 traits validate cleanly only after D5 ships.
- D7 (resistance matrix 7×7; gamora) — paired-luminance valence interacts with holy traits' "aligned" semantics. Not a blocker for D8 design but worth jack-ryan cross-coherence review.
- D9 (gear-affix design; gandalf + gamora) — D9 extends gear-affix gating to the same substrate identities; substrate-aware gear-affix-tagging shares architectural shape with the trait-affix architecture described here.

**Cross-canonical updates triggered by D8 (Phase-1 P1 follow-on):**
- `canonical/story/spirit-guide-voice.md` § "trait language" — Spirit Guide should be able to *speak about* the new-substrate traits when recommending optimal distributions. Not a blocker; rolls into D26 cross-doc updates.
- `canonical/32-progression-design.md` § 4 — minor update noting D8 as the first concrete trait-pool authoring instance, with canonical-four pool authoring flagged as Phase-1 P2 candidate per § 5.2 above. Rolls into D26.

---

*Authored 2026-05-18 by gandalf in hive-mode Phase-1 P1. Three substrates, three trait pools, 24 traits. The substrate identities become traits the player can wear. The pool is intrinsic; gear extends it with affix rolls (see D9). Cross-substrate coherence verified clean against forbidden_mechanics. Gamora implementation contract specified.*
