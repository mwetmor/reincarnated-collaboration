# The Seven Substrate Identity Declarations

**Authority:** gandalf (story-and-design steward).
**Status:** **Canonical Layer-1 declarations** for the canonical-7 substrate set. Each substrate's commitment manifest per the substrate-identity-declaration-spec.
**Companion spec:** `substrate-identity-declaration-spec-2026-05-17.md` (the shape these declarations instantiate).
**Companion decision:** `substrate-expansion-decision-2026-05-17.md` (the substrate set: fire/water/earth/wind + lightning + holy + shadow).
**Companion resolution:** `earth-self-diversity-tension-2026-05-17.md` (Court-as-grace; introduces `court_resonance` field).

**Layout:** This doc is the human-readable canonical authorship of all 7 declarations. The engine-consumable YAML files will be derived from these declarations (one file per substrate at `reincarnated-engine/config/substrate_identities/<name>.yaml`; rocket Phase-1 P1a implementation extracts machine-readable YAML from this canonical doc).

**Reading order:** § 0 TL;DR → § 1 Fire → § 2 Water → § 3 Earth → § 4 Wind → § 5 Lightning → § 6 Holy → § 7 Shadow → § 8 Cross-references.

---

## § 0 — TL;DR

Seven substrates, seven identity declarations. Each substrate commits to:

- **Mechanical signature** (3-5 verbs it IS)
- **Forbidden mechanics** (verbs it REFUSES)
- **Combat pillar** (one-tag commitment)
- **Ailment signature** (its native control/DoT/buff)
- **Scaling attribute** (the stat it scales with)
- **Geometry affinities** (preferred/avoided shapes)
- **Role affinities** (which roles it naturally produces)
- **Iconic verbs** (LLM anchor vocabulary)
- **Iconic register** (tonal commitment)
- **Cosmological commitment** (the substrate's poetic claim)
- **Court resonance** (how the Court remembers forms of this substrate)
- **Pair-structure metadata** (paired_with / pair_axis / forbidden_hybrid_with where applicable)
- **Grouping label** (L2 grouping-vocabulary mapping)

**2026-05-17 23:45Z amendment (gandalf):** `forbidden_hybrid_with` field added to all seven declarations per substrate-identity-declaration-spec § 2.1 + § 3.6 + § 5.3 amendment (filed in hive log at same timestamp; gandalf authorship; routed to knight-rider for L2/L3 disposition). Field formalizes the canonical-four anti-pole hybrid-forbidden pairings (fire↔water; earth↔wind) at the declaration layer rather than as a hardcoded constant in `b6_archetype_templates.py:24-30`. Holy↔shadow are paired-luminance (amplification) NOT forbidden-hybrid (mechanical-erasure) — the two relationships are cosmologically distinct.

**Pairing summary:**

| Substrate | Paired with | Pair axis | Forbidden hybrid | Grouping label (current/proposed) |
|---|---|---|---|---|
| Fire | — | — | water (anti-pole) | ignition (locked) |
| Water | — | — | fire (anti-pole) | suffusion (locked) |
| Earth | — | — | wind (anti-pole) | bulwark (locked) |
| Wind | — | — | earth (anti-pole) | displacement (locked) |
| Lightning | (none — unpaired) | — | — (none) | **resonance** (proposed) |
| Holy | Shadow | luminance | — (amplification-pair NOT erasure-pair) | **radiance** (proposed) |
| Shadow | Holy | luminance | — (amplification-pair NOT erasure-pair) | **penumbra** (proposed) |

*New grouping labels (resonance / radiance / penumbra) require grouping-vocab extension per pending Task #4. Until that lands, lightning/holy/shadow remain provisionally unmapped at the L2 layer.*

---

## § 1 — Fire

```yaml
substrate: fire

identity:
  mechanical_signature: [ignite, escalate, area_persist, burn_apply]
  forbidden_mechanics: [drain, conceal, slow_channel]
  combat_pillar: HIGH_BURST_LOW_PERSIST

  ailment_signature:
    name: burn
    category: dot
    description: |
      Damage-over-time on contact. Small spark cascades into larger consequence
      over time. The ailment that grows after you have delivered it.

  scaling_attribute: intelligence

  geometry_affinities:
    burst: PREFER
    cone: PREFER
    area_sustain: PREFER
    ground_targeted_circle: PREFER
    projectile: NEUTRAL
    branching: NEUTRAL
    melee_arc: NEUTRAL
    vortex_pull: AVOID
    bolt_line: AVOID

  role_affinities:
    damage: 0.8
    support: 0.2
    control: 0.4
    hybrid: 0.5

  iconic_verbs:
    - "ignites"
    - "burns"
    - "scorches"
    - "engulfs"
    - "flares"
    - "consumes"
    - "kindles"

  iconic_register: martial

  cosmological_commitment: |
    The substrate of escalation — what begins small and becomes total.
    Fire is the substrate of *consequence accumulating in time* —
    each tick of the ailment is the original spark continuing to act.

  court_resonance: |
    The Court remembers Firewalkers as the forms that delivered the first
    spark and let the world finish what they began.

  paired_with: null
  pair_axis: null
  forbidden_hybrid_with: [water]   # canonical-four anti-pole: suffusion erases escalation

grouping_label: ignition
```

---

## § 2 — Water

```yaml
substrate: water

identity:
  mechanical_signature: [suffuse, permeate, chill_apply, slow]
  forbidden_mechanics: [ignite, sudden_strike, direct_burst]
  combat_pillar: SUSTAINED_PRESENCE_ZONE_DENIAL

  ailment_signature:
    name: chill
    category: soft_control
    description: |
      Movement and action speed reduction by immersion. Slows without striking;
      binds without grasping. State-changing presence rather than direct damage.

  scaling_attribute: intelligence

  geometry_affinities:
    area_sustain: PREFER
    circle: PREFER
    wave: PREFER
    ground_targeted_circle: PREFER
    cone: NEUTRAL
    projectile: NEUTRAL
    bolt_line: AVOID
    branching: AVOID
    burst: AVOID

  role_affinities:
    damage: 0.5
    support: 0.5
    control: 0.7
    hybrid: 0.6

  iconic_verbs:
    - "suffuses"
    - "permeates"
    - "fills"
    - "stills"
    - "submerges"
    - "binds"
    - "settles into"

  iconic_register: mystic

  cosmological_commitment: |
    The substrate of pervading presence — what fills a space rather than
    hitting it. Water is the substrate of *state-change-by-immersion* —
    the world inside the water is not the world above it.

  court_resonance: |
    The Court remembers Tidecallers as the forms that walked into rooms and
    changed what those rooms were.

  paired_with: null
  pair_axis: null
  forbidden_hybrid_with: [fire]   # canonical-four anti-pole: escalation erases suffusion

grouping_label: suffusion
```

---

## § 3 — Earth

```yaml
substrate: earth

identity:
  mechanical_signature: [anchor, root_apply, hold_ground, mass_strike]
  forbidden_mechanics: [displace, lift, sudden_traversal]
  combat_pillar: ANCHOR_AND_DISRUPT

  ailment_signature:
    name: root
    category: hard_control
    description: |
      Positional immobilization. Locks the target's movement; held until
      duration expires or root is broken by external effect. The ailment of
      *what does not yield*.

  scaling_attribute: wisdom

  geometry_affinities:
    ground_targeted_circle: PREFER
    pillar: PREFER
    slam: PREFER
    melee_arc: PREFER
    area_sustain: PREFER
    cone: NEUTRAL
    projectile: NEUTRAL
    vortex_pull: AVOID
    bolt_line: AVOID
    branching: AVOID

  role_affinities:
    damage: 0.6
    support: 0.4
    control: 0.8
    hybrid: 0.5

  iconic_verbs:
    - "anchors"
    - "roots"
    - "holds"
    - "crushes"
    - "stands against"
    - "binds in place"
    - "weighs down"

  iconic_register: martial

  cosmological_commitment: |
    The substrate of unyielding — what does not move and will not be moved.
    Earth is the substrate of *positional refusal* — it answers the question
    "can I be here" with "yes, and so can what stands with me."

  court_resonance: |
    The Court remembers Bulwarks as the forms that held the line when others
    would have run.

  paired_with: null
  pair_axis: null
  forbidden_hybrid_with: [wind]   # canonical-four anti-pole: displacement erases anchoring

grouping_label: bulwark
```

---

## § 4 — Wind

```yaml
substrate: wind

identity:
  mechanical_signature: [displace, knockback, redirect, mobility]
  forbidden_mechanics: [anchor, root, hold_ground]
  combat_pillar: KINETIC_REDIRECTION

  ailment_signature:
    name: knockback
    category: hard_control
    description: |
      Positional removal. Target is forced from current position. The ailment
      of *what carries things elsewhere*. Contrasts with root's positional
      refusal as wind's kinetic opposite.

  scaling_attribute: wisdom

  geometry_affinities:
    cone: PREFER
    swirl: PREFER
    vortex_pull: PREFER
    projectile: PREFER
    line: PREFER
    area_sustain: NEUTRAL
    burst: NEUTRAL
    bolt_line: NEUTRAL
    pillar: AVOID
    melee_arc: AVOID
    ground_targeted_circle: AVOID

  role_affinities:
    damage: 0.5
    support: 0.5
    control: 0.7
    hybrid: 0.6

  iconic_verbs:
    - "displaces"
    - "carries"
    - "scatters"
    - "lifts"
    - "redirects"
    - "blows aside"
    - "drifts"

  iconic_register: mystic

  cosmological_commitment: |
    The substrate of motion — what removes targets from their position and
    redirects momentum elsewhere. Wind is the substrate of *kinetic
    rearrangement* — it does not destroy what it touches; it puts it
    somewhere else.

  court_resonance: |
    The Court remembers Stormriders as the forms that never stayed where the
    fight expected them, and never left the fight where it began.

  paired_with: null
  pair_axis: null
  forbidden_hybrid_with: [earth]   # canonical-four anti-pole: anchoring erases displacement

grouping_label: displacement
```

---

## § 5 — Lightning

```yaml
substrate: lightning

identity:
  mechanical_signature: [chain, propagate, arc, discharge]
  forbidden_mechanics: [root, sustained_aura, ground_persist, slow_channel]
  combat_pillar: HIGH_BURST_LOW_PERSIST

  ailment_signature:
    name: shock
    category: hard_control
    description: |
      Paralysis-on-arc. Brief immobilization triggered by chain-arc damage;
      each chain hop applies shock to the next target. Lightning's hard
      control is its own propagation mechanism.

  scaling_attribute: intelligence

  geometry_affinities:
    branching: PREFER
    arc: PREFER
    bolt_line: PREFER
    chain_lightning: PREFER
    projectile: PREFER
    cone: NEUTRAL
    ground_targeted_circle: NEUTRAL
    area_sustain: AVOID
    vortex_pull: AVOID
    melee_arc: AVOID
    pillar: AVOID

  role_affinities:
    damage: 0.7
    support: 0.3
    control: 0.6
    hybrid: 0.5

  iconic_verbs:
    - "arcs"
    - "chains"
    - "discharges"
    - "leaps to"
    - "stuns"
    - "flashes"
    - "strikes"
    - "courses through"

  iconic_register: scientific

  cosmological_commitment: |
    The substrate of sudden traversal — what crosses gaps without crossing
    the space between. Lightning is the substrate of *interruption* — it
    ends what was about to happen by being faster than it could happen.

  court_resonance: |
    The Court remembers Stormcallers as the forms that walked between
    moments, never quite where they had been seen.

  paired_with: null
  pair_axis: null
  forbidden_hybrid_with: []   # lightning is unpaired per genre convention; composes freely with all substrates

grouping_label: resonance   # proposed; pending grouping-vocab extension (Task #4)
```

**Lightning notes:**
- Lightning is **unpaired** by genre convention (Diablo, PoE, Last Epoch — lightning is its own thing, not opposed to a specific substrate). Treating it as paired would require inventing a substrate; that's not in scope.
- Combat pillar HIGH_BURST_LOW_PERSIST overlaps with fire — this is **intentional and correct genre-wise.** The diversity gate (Layer 3) handles the push-apart between fire and lightning at the geometry + mechanical_signature level (fire prefers burst/cone/area_sustain; lightning prefers branching/arc/bolt_line; fire forbids drain; lightning forbids root). Same pillar, different mechanical bodies.
- `iconic_register: scientific` differentiates lightning from fire's `martial` register at the LLM-vocabulary layer. "Discharges" reads scientific; "scorches" reads martial.

---

## § 6 — Holy

```yaml
substrate: holy

identity:
  mechanical_signature: [radiate, consecrate, cleanse, amplify_allied]
  forbidden_mechanics: [drain, conceal, corrupt, stealth]
  combat_pillar: REVELATION_AND_AMPLIFICATION

  ailment_signature:
    name: consecrate
    category: amplification
    description: |
      Ground-consecration zone applying DoT to opposed-substrate targets +
      heal-amplification to allies inside the zone. Unique among ailments
      in being *valenced* — beneficial to one side, harmful to the other,
      based on substrate alignment.

  scaling_attribute: wisdom

  geometry_affinities:
    radiant_aura: PREFER
    shaft: PREFER
    nova: PREFER
    ground_targeted_circle: PREFER
    area_sustain: PREFER
    cone: NEUTRAL
    burst: NEUTRAL
    projectile: NEUTRAL
    tendril: AVOID
    swirl: AVOID
    chain_lightning: AVOID

  role_affinities:
    damage: 0.5
    support: 0.8
    control: 0.4
    hybrid: 0.4

  iconic_verbs:
    - "consecrates"
    - "sanctifies"
    - "burns away"
    - "judges"
    - "reveals"
    - "blesses"
    - "uplifts"
    - "shines through"

  iconic_register: clerical

  cosmological_commitment: |
    The substrate of revelation — what exposes and what cannot abide
    exposure. Holy is the substrate of *amplification-of-aligned* — it
    makes what is true brighter, and what is hidden cannot remain hidden.

  court_resonance: |
    The Court remembers Lightbearers as the forms that walked with their
    own dawn around them, and could not be unseen.

  paired_with: shadow
  pair_axis: luminance
  forbidden_hybrid_with: []   # holy's pair with shadow is amplification (luminance valence), NOT forbidden — holy/shadow can compose in a kit with valenced damage interactions

grouping_label: radiance   # proposed; pending grouping-vocab extension (Task #4)
```

**Holy notes:**
- `combat_pillar: REVELATION_AND_AMPLIFICATION` is paired-axis with shadow's CONCEALMENT_AND_DRAIN. The mechanical commitments are opposite.
- `ailment_signature.category: amplification` is **novel** — neither hard-control, soft-control, DoT, nor debuff. Holy introduces a new ailment category. The wide-net-coupling-archaeology § 2.2 fix-shape (`config/ailments.yaml` registry with per-ailment metadata) supports this; until that lands, consecrate's mechanical implementation will need careful Phase-1 P1 design.
- `role_affinities: support: 0.8` — holy is genre-canonically support-heavy (paladin auras; cleric heals). This affinity drives Layer-2 composition to generate more holy_support archetypes than holy_damage archetypes per season.
- The deity-coding concern (per substrate-expansion-decision § 3.1): `iconic_register: clerical` and `iconic_verbs` carry *sacred / devotional* register without locking in a specific deity. "Judges" / "sanctifies" / "blesses" read as religious-tradition-agnostic enough for Reincarnated's impersonal Wheel cosmology.

---

## § 7 — Shadow

```yaml
substrate: shadow

identity:
  mechanical_signature: [drain, conceal, corrupt, dim_perception]
  forbidden_mechanics: [radiate, consecrate, amplify_allied, reveal]
  combat_pillar: CONCEALMENT_AND_DRAIN

  ailment_signature:
    name: drain
    category: dot
    description: |
      Sustained life/resource-drain over time. Unlike fire's burn (escalating)
      or water's chill (state-changing), drain is *withdrawing* — what is
      drained returns to no one; it is simply removed from the world.

  scaling_attribute: intelligence

  geometry_affinities:
    tendril: PREFER
    void_pool: PREFER
    creep: PREFER
    area_sustain: PREFER
    swirl: NEUTRAL
    vortex_pull: NEUTRAL
    projectile: NEUTRAL
    radiant_aura: AVOID
    nova: AVOID
    shaft: AVOID
    melee_arc: AVOID

  role_affinities:
    damage: 0.7
    support: 0.3
    control: 0.5
    hybrid: 0.6

  iconic_verbs:
    - "drains"
    - "corrupts"
    - "withdraws"
    - "shrouds"
    - "dims"
    - "creeps into"
    - "unmakes"
    - "occludes"

  iconic_register: shadow

  cosmological_commitment: |
    The substrate of withdrawal — what takes without striking and arrives
    without warning. Shadow is the substrate of *occlusion* — it removes
    what was there without the world noticing the removal until later.

  court_resonance: |
    The Court remembers shadows as the forms that walked alongside what
    they did not name, and were not always seen even by themselves.

  paired_with: holy
  pair_axis: luminance
  forbidden_hybrid_with: []   # shadow's pair with holy is amplification (luminance valence), NOT forbidden — holy/shadow can compose in a kit with valenced damage interactions

grouping_label: penumbra   # proposed; pending grouping-vocab extension (Task #4)
```

**Shadow notes:**
- `paired_with: holy` — mechanically opposed; mutual amplification per substrate-expansion-decision § 5.1 resistance valence.
- The Solo Leveling precedent (per `gandalf-design-lineage.md` Layer 5) is honored at the cosmological_commitment + court_resonance fields. Shadow is *occlusion*, not malice — the moral-asymmetry observation (gandalf seven-reflections VI) is consciously bracketed at the substrate-identity layer.
- `ailment_signature: drain` is mechanically a DoT (like burn) but **semantically different** — burn escalates (consequence growing); drain withdraws (consequence removing). Layer-4 LLM prompts must distinguish these vocabulary registers.
- `iconic_register: shadow` — a register of its own that is neither martial, mystic, clerical, nor scientific. The shadow register is *quieter, lower-frequency, weight-of-absence* in tone.

---

## § 8 — Authorship notes and design discipline

### § 8.1 — What was held when authoring

1. **Mechanical signatures are *short* and *substrate-distinguishing*.** Each substrate's 3-5 signature verbs were chosen to be unambiguously this-substrate-not-another. No two substrates share signature verbs.

2. **Forbidden mechanics are *strong* declines.** Each substrate's forbidden list opposes at least one other substrate's signature — fire forbids slow_channel (water's territory); wind forbids root (earth's signature); holy forbids drain (shadow's signature); shadow forbids radiate (holy's signature). The opposition is *architecturally enforced*.

3. **Combat pillars are *one of seven*.** The pillars are designed to allow strategic overlap (fire and lightning both HIGH_BURST_LOW_PERSIST) while remaining differentiable through other declarations (geometry, mechanical_signature, iconic_register). The pillar is the *coarsest* axis of identity; finer differentiation lives in the other fields.

4. **Iconic verbs anchor against LLM training-distribution bias.** Per Legolas Mode A literature pass Finding A: LLM training-distribution favors fire/lightning over shadow/holy. Each substrate's iconic_verbs are deliberate anchor vocabulary the LLM must extend from, not from generic mage-tropes.

5. **Cosmological commitments are *poetic but functional*.** Each commitment is a 1-3 sentence statement that (a) captures the substrate's identity in language a player can perceive, (b) provides LLM scaffold for per-season vocabulary generation, (c) anchors Spirit Guide voice references.

6. **Court resonances honor the Earth-Self diversity tension resolution.** Each substrate has a 1-2 sentence statement of *how the Court remembers* this substrate's forms. These are read at cross-season moments by Layer-4 LLM. The phrasing leans into accumulation-of-identity vocabulary ("the forms that...") rather than singular-form vocabulary.

### § 8.2 — What was deliberately NOT in these declarations

- **Specific archetype names.** Archetypes (lightning_controller; holy_support) compose at Layer 2 from substrate × role; they are not authored in declarations.
- **Numerical balance values.** Damage scaling coefficients, resistance values, base stats are Phase-1 P1 gamora/jack-ryan work and live in their own specs.
- **Per-season vocabulary fills.** "Stormcaller" / "Threshold-Spark" / "Pressure-Release" are LLM-generated per season; declarations provide scaffold, not content.
- **Cross-substrate interaction rules.** Whether lightning conducts through water; whether fire melts ice; whether holy purifies shadow zones — these are Phase-1 P2+ design decisions; the canonical-four explicitly does not have elemental-physics interactions per substrate-expansion-decision § 5.1.

### § 8.3 — Revision discipline

Per substrate-identity-declaration-spec § 4.3: declarations are not lightly revisable. Changes propagate to:

- All archetypes Layer 2 generates for that substrate
- All per-season vocabulary Layer 4 has generated against the substrate
- All telemetry-pressure baselines Layer 5 has accumulated
- All player-facing surface text (Spirit Guide voice; Court browser; loadout substrate descriptions)

Revisions should be batched and treated as canonical-amendments via the maintenance protocol. Avoid one-line declaration tweaks; gather revisions into intentional canonical-update passes.

---

## § 9 — Pending integration items

These 7 declarations are *canonically authored*; engine integration requires:

1. **Grouping-vocab extension** (Task #4 pending) — register new L2 labels: resonance / radiance / penumbra. Without this, lightning / holy / shadow's `grouping_label` references dangle.

2. **Substrate identity loader implementation** (rocket Phase-1 P1a) — extract these YAML blocks into `config/substrate_identities/<name>.yaml`; build typed `SubstrateIdentity` dataclass; integrate with `foundation.get_rotating_elements()`.

3. **Ailment registry** (rocket Phase-1 P1a per wide-net § 2.2) — register the new ailments (shock / consecrate / drain) with their categories and per-ailment metadata. Consecrate's `amplification` category is *novel* — design discipline review at Phase-1 P1 Gate 1.

4. **Layer-2 composition refactor** (gamora Phase-1 P1) — `b6_archetype_templates.py` replaced with substrate × role composition. The 14 hardcoded archetype templates become emergent outputs.

5. **Cross-doc updates:**
   - `cosmology-reincarnated.md` — substrate set extended at § Substrates (if such § exists; otherwise authored)
   - `court-of-forms.md` — Court-resonance vocabulary integrated
   - `spirit-guide-voice.md` — Guide voice register extended with per-substrate cosmological_commitment + court_resonance phrasing patterns

---

### § 9.1 — Amendment 2026-05-17: Layer-0 spatial-combat substrate underwrites these declarations

**Authority:** gandalf L3 briefing `canonical/story/dodge-plus-telegraphed-combat-l3-briefing-2026-05-17.md` (tag `gandalf/v1.2-dodge-and-telegraphed-combat-l3-briefing-1` @ `3ec108f`); Matt standing delegation; PARTIAL Phase-1 P1 extension chosen per briefing § 7.

The seven substrate identity declarations above instantiate **Layer-1** of the diversity architecture (per `substrate-identity-declaration-spec-2026-05-17.md`). Their perceptual legibility — what makes wind's `displace` verb feel different from fire's `escalation` verb in a 90-second fight — is **conditional on a Layer-0 spatial-combat substrate** that the spec deliberately did not specify (it presupposed ARPG conventions).

Matt's son surfaced the missing Layer-0 in focused-playtest test 6 (2026-05-17): *"it would be way more fun if it seemed like the monsters could move out of range of your AOE and vice versa, if you could dodge roll out of the way, or run."* This is the engagement-loop substrate that the Layer-1 declarations assume but the engine did not yet ship.

**Specifically, these Layer-1 declarations are dependent on Layer-0 spatial combat for perceptual legibility:**

- **Wind** `mechanical_signature: [displace, knockback, redirect, mobility]` — collapses into "fire with cyan tint" if monsters cannot be moved out of position AND cannot move to evade.
- **Earth** `cosmological_commitment: "the substrate of unyielding — what does not move and will not be moved"` — unfalsifiable if nothing moves.
- **Fire** `combat_pillar: HIGH_BURST_LOW_PERSIST` vs **Water** `SUSTAINED_PRESENCE_ZONE_DENIAL` — pillars resolve identically into "do damage in a fixed area" without movement-into-and-out-of-presence-zones.
- **Lightning** `mechanical_signature: [chain, propagate, arc, discharge]` — `chain` is identical to flat AOE if monsters cannot reposition between arcs.
- **Holy / shadow** — `consecrate` zones only matter if targets can enter or leave them; `conceal` only matters if perception decides hit/miss windows.

**Resolution:** the narrow-slice Phase-1 P1 extension (Deliverable 28) ships the Layer-0 substrate:

- Universal player dodge mechanic (Shift-key; substrate-VFX-coupled animation per briefing § 2.2; substrate numerical asymmetry for earth/wind only)
- Enemy-AOE ground-indicator system with per-substrate windup character (per briefing § 3.2; rocket schema fields `windup_duration_seconds` + `indicator_color_hex` per `2026-05-17-rocket-narrow-slice-engine-schema-fields.md` dispatch)
- Elite-tier reactive escape AI (gamora narrow-slice work)

Full B13 polish (5 defensive mobility geometries as kit-pool additions; mini-boss/boss strategic + substrate-coherent escape AI; archetype-emergence observability) stays in its existing post-VS2a slot per `canonical/16-project-roadmap.md` § Stage A2 closeout (B13 scope reduced ~25% by narrow slice; ~2.5-3 weeks remaining).

**These declarations are unchanged at the Layer-1 layer by this amendment.** The amendment-note merely acknowledges that Layer-1 legibility *requires* Layer-0 — which the narrow slice now delivers in time for the D27 perception test to land cleanly. See briefing § 1.3 for the D27-false-negative-risk analysis the narrow slice closes.

---

## § 9.5 — Substrate-identity at the surface — pipeline dependency (R8 amendment 2026-05-19)

**Empirical confirmation from R8 A/B run.** The R8 A/B run (2026-05-19; see `canonical/story/r8-disposition-2026-05-19.md` + `output/R8-ab-run-2026-05-19/`) tested whether substrate-identity is invariant across three season-generation pipelines: baseline (input-themed + per-entity LLM naming), inverted (coalescence-first + per-entity LLM naming retained), and inverted_no_naming (coalescence-first + template-based downstream naming).

**Finding (mechanical substrate): Substrate-identity at the canonical-element level is PERFECTLY INVARIANT across all 3 pipelines for 3 seeds.** Per-seed canonical-element distribution (fire:N, water:N, earth:N, wind:N, physical:N) is byte-identical across the 3 arms. The mechanical substrate IS the substrate; naming pipeline is a downstream cosmetic decoration of that substrate. This is the strongest possible empirical form of substrate-identity preservation: substrate is a property of the mechanical-generator + seed, not of the naming-pipeline.

**Finding (surface substrate-mode-of-action): Player-facing READABILITY of substrate-mode depends on the naming pipeline.** Per-entity LLM naming (the R8-committed `inverted` default) preserves substrate-mode-of-action in ~90% of player-facing skill names. Template-based composition (the deferred `inverted_no_naming` opt-in) preserves substrate-mode in only ~63% of skill names; the remaining ~37% are surface-token-bearing but mode-of-action-mismatched (e.g., a `bulwark`-slot skill composing as "Ink Strike" with `self_buff` geometry — the token honors substrate, the mode does not).

**Implication for substrate-identity declarations:** the seven identity declarations in §§ 2-8 hold at the mechanical-substrate layer regardless of naming pipeline (Layer-1 trait-as-promise is mechanical, not naming-derived). The Layer-2 grouping-vocabulary surface (slot labels, skill names, monster names, trial-boss names) preserves substrate-mode at ~90% under per-entity LLM naming; at ~63% under template-distribution. Future implementations choosing template-distribution for cost reasons should be aware that ~1 in 3 skill-name surfaces will read as substrate-mode-mismatched until template-distribution is repaired to honor slot-mode-of-action (per R8 disposition § 5a follow-on item).

**The substrate is preserved at the level of what it commits to be (mechanical). The substrate's surface-readability — what a player FEELS when they read a skill name — is pipeline-dependent.** The declarations remain authoritative for what the substrate IS; the pipeline determines how reliably the player can sense it through naming.

---

## § 10 — Cross-references

- `canonical/story/substrate-identity-declaration-spec-2026-05-17.md` — the spec these declarations instantiate
- `canonical/story/substrate-expansion-decision-2026-05-17.md` — the substrate set
- `canonical/story/earth-self-diversity-tension-2026-05-17.md` — Court-as-grace resolution; introduces `court_resonance`
- `canonical/story/substrate-coupling-archaeology-2026-05-17.md` — the substrate-keyed coupling sites these declarations fix
- `canonical/story/archetype-coupling-archaeology-2026-05-17.md` — the archetype-keyed coupling sites these declarations fix (Path a refactor enabled)
- `canonical/story/wide-net-coupling-archaeology-2026-05-17.md` — the broader coupling concerns these declarations partially address (substrates + ailments)
- `canonical/story/grouping-layer-vocabulary.md` — L2 grouping vocabulary; new labels (resonance / radiance / penumbra) pending
- `canonical/story/cosmology-reincarnated.md` — cosmological frame
- `canonical/story/spirit-guide-voice.md` — Guide voice register
- `canonical/story/court-of-forms.md` — Court accumulation arc
- `canonical/37-form-bias-diagnosis-and-recovery.md` — form-bias precedent (intra-substrate convergence; this work is the inter-substrate sequel)
- `agentic_orchestration/research/knowledge/diversity-architecture-literature-pass-2026-05-17.md` — Legolas Mode A findings informing iconic_verbs anti-bias rationale

---

*Authored 2026-05-17 by gandalf. Seven substrates, seven identity declarations. Each substrate's promise of what it commits to be. The diversity architecture's Layer-1 foundation. Companion canonical to substrate-identity-declaration-spec.*
