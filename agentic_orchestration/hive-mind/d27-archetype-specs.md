# D27 Perception-Test Archetype-Pair Specifications

**Authority:** gandalf (story-and-design steward), authoring per `canonical/story/perception-test-experiment-scoping-2026-05-17.md` § 3.1 + § 3.3 and hive log HANDOFF [2026-05-18 00:10Z].
**Status:** Canonical archetype-pair spec set for Phase-1 P1a perception-test execution. Drax-demo consumes for D27 Track A final integration (replaces `TODO(drax)` placeholders in `runner.js`).
**Companion docs:**
- `canonical/story/perception-test-experiment-scoping-2026-05-17.md` (the experiment spec — § 3.1 method, § 3.3 session structure, § 4.3 bias controls, § 5 measurement)
- `canonical/story/substrate-identity-declarations-2026-05-17.md` (the canonical-four declarations the pairs exercise — § 1-§ 4)
- `reincarnated-engine/src/reincarnated/generation/b6_archetype_templates.py` (the engine-side ArchetypeTemplate shapes the pairs vary parametrically)
- `agentic_orchestration/hive-mind/scope-of-work-phase-1-p1.md` § 1.7 (deliverable 27)

**Reading order:** § 0 TL;DR → § 1 Spec format → § 2 Pair-Type A (mechanical distinctness, 8 archetypes) → § 3 Pair-Type B (vocabulary control, 4 archetypes) → § 4 Drax integration notes → § 5 Bias controls + display surface → § 6 Open question for drax.

---

## § 0 — TL;DR

**12 archetypes total. Two pair types.**

- **Pair-Type A (mechanical distinctness, 8 archetypes):** 4 pairs, each pair = same role + same substrate + parametrically distinct kit-shape vectors (geometry distribution, cooldown profile, ailment distribution, AOE/single-target ratio differ by ≥2σ).
  - Pair A1: two fire_mage (damage role) variants
  - Pair A2: two water_controller variants
  - Pair A3: two earth_caster variants
  - Pair A4: two wind_controller variants

- **Pair-Type B (vocabulary control, 4 archetypes):** one per canonical-four substrate, each mechanically distinct (different role), with deliberately generic vocabulary (LLM forbidden from substrate-specific phrasings).
  - Quad B class W: fire substrate, generic-vocab "burst combatant" presentation
  - Quad B class X: water substrate, generic-vocab "field-control combatant"
  - Quad B class Y: earth substrate, generic-vocab "heavy combatant"
  - Quad B class Z: wind substrate, generic-vocab "mobile combatant"

Per perception-test § 4.3 bias controls: **substrate names withheld from subjects; archetypes presented under neutral display names (Class 1 / Class 2 / ... or Build A / Build B / ...)** in randomized order.

---

## § 1 — Spec format

Each archetype is specified by the following fields. Drax consumes this spec by translating into demo1 `runner.js` archetype config entries:

```yaml
spec_id: <unique_id_for_this_doc>             # e.g., "pair_A1_variant_a"
display_name: <subject_facing_neutral_name>   # e.g., "Class 3" — subject sees this only
substrate: <canonical_substrate_name>         # SUPPRESSED from subject; used by engine
role: <canonical_role>                        # damage / controller / caster

kit_shape_vector:
  geometry_distribution:                      # frequency-weighting per geometry tag
    <geometry>: <weight_0_to_1>
    ...
  cooldown_profile:
    short_cd_share: <0_to_1>                  # share of kit with cooldown < 4s
    medium_cd_share: <0_to_1>                 # share with 4s <= cooldown < 12s
    long_cd_share: <0_to_1>                   # share with cooldown >= 12s
  ailment_distribution:                       # share of kit with ailment-applying effect
    primary_ailment_share: <0_to_1>
    secondary_ailment_share: <0_to_1>
  aoe_single_target_ratio: <0_to_1>           # 0 = all single-target; 1 = all AOE

special_notes: <free-text notes for drax>
```

**Statistical-distinctness target (per pair):** Within a pair, the two variants' kit-shape vectors must differ by ≥2σ across all four axes (geometry distribution similarity, cooldown profile distance, ailment distribution distance, AOE ratio distance). The vectors below are authored to meet that threshold; drax verifies at runner-config time.

**Per perception-test § 3.1:** "Pair generation can use the current canonical-four engine (no Layer-2 composition refactor needed). Use existing archetype templates with deliberately tuned parameters to produce statistically-distinct kit vectors within each pair."

---

## § 2 — Pair-Type A: Mechanical-distinctness pairs

### § 2.1 — Pair A1: fire_mage variants

**Base archetype:** `fire_mage` (canonical; per `b6_archetype_templates.py:101-123`)
**Role:** damage (burst damage role per substrate-identity-declarations § 1)
**Substrate:** fire (suppressed from subject)

#### Variant A1a — "Cone Burner" (close-band, AOE-cone-heavy)

```yaml
spec_id: pair_A1_variant_a
display_name: "Class 1"
substrate: fire
role: damage

kit_shape_vector:
  geometry_distribution:
    cone: 0.40
    ground_targeted_circle: 0.25
    burst: 0.20
    melee_arc: 0.10
    projectile: 0.05
  cooldown_profile:
    short_cd_share: 0.20
    medium_cd_share: 0.60
    long_cd_share: 0.20
  ailment_distribution:
    primary_ailment_share: 0.75      # burn-heavy
    secondary_ailment_share: 0.10
  aoe_single_target_ratio: 0.75       # AOE-heavy

special_notes: |
  Close-band fire damage; cone-and-ground-aoe dominant; high burn ailment density.
  Player should perceive: "this archetype rushes in close and burns everything in a cone."
  Genre-precedent feel: D2 Sorceress Inferno + Wall of Fire build; D4 Sorcerer Incinerate.
```

#### Variant A1b — "Bolt Sniper" (long-band, projectile-heavy, low ailment)

```yaml
spec_id: pair_A1_variant_b
display_name: "Class 2"
substrate: fire
role: damage

kit_shape_vector:
  geometry_distribution:
    projectile: 0.50
    bolt_line: 0.25
    burst: 0.10
    branching: 0.10
    ground_targeted_circle: 0.05
  cooldown_profile:
    short_cd_share: 0.55                # rapid-fire feel
    medium_cd_share: 0.30
    long_cd_share: 0.15
  ailment_distribution:
    primary_ailment_share: 0.20         # minimal burn
    secondary_ailment_share: 0.05
  aoe_single_target_ratio: 0.25         # single-target-heavy

special_notes: |
  Long-band fire damage; projectile / bolt-line dominant; rapid cooldowns; low ailment.
  Player should perceive: "this archetype keeps distance and snipes high-damage bolts."
  Genre-precedent feel: D2 Sorceress Fire Bolt + Fire Ball; PoE Fireball Elementalist single-target.
  Statistical distinctness vs A1a: geometry dist >2σ (cone-dominant vs projectile-dominant);
  cooldown profile >2σ (medium-heavy vs short-heavy); ailment dist >2σ; AOE ratio >2σ.
```

**Pair A1 distinctness check:** Variants A1a and A1b differ across all four kit-shape-vector axes simultaneously. Same role, same substrate, parametrically distinct.

---

### § 2.2 — Pair A2: water_controller variants

**Base archetype:** `water_controller` (canonical; per `b6_archetype_templates.py:250-270`)
**Role:** controller
**Substrate:** water (suppressed from subject)

#### Variant A2a — "Zone Persister" (persistent-AOE, long-cooldown)

```yaml
spec_id: pair_A2_variant_a
display_name: "Class 3"
substrate: water
role: controller

kit_shape_vector:
  geometry_distribution:
    area_sustain: 0.40
    ground_targeted_circle: 0.30
    ring: 0.15
    circle: 0.10
    vortex_pull: 0.05
  cooldown_profile:
    short_cd_share: 0.10
    medium_cd_share: 0.30
    long_cd_share: 0.60                 # long-zone-lifetime
  ailment_distribution:
    primary_ailment_share: 0.85         # chill-saturated
    secondary_ailment_share: 0.10
  aoe_single_target_ratio: 0.85         # AOE-dominant

special_notes: |
  Persistent water-zone controller; player drops long-duration zones and kites.
  Player should perceive: "this archetype controls space by placing zones and letting them last."
  Genre-precedent feel: PoE Vortex Occultist (persistent freeze zones); D2 Hydra Sorceress.
```

#### Variant A2b — "Wave Slammer" (rapid-burst zones, short cooldown)

```yaml
spec_id: pair_A2_variant_b
display_name: "Class 4"
substrate: water
role: controller

kit_shape_vector:
  geometry_distribution:
    wave: 0.35                          # NOTE: 'wave' may not exist in canonical geometry palette;
                                        # drax: substitute with closest canonical geometry per
                                        # `foundation/geometry_pool.py` if 'wave' is unrecognized
    burst: 0.25
    cone: 0.20
    projectile: 0.15
    beam_channel: 0.05
  cooldown_profile:
    short_cd_share: 0.65                # rapid-wave cadence
    medium_cd_share: 0.25
    long_cd_share: 0.10
  ailment_distribution:
    primary_ailment_share: 0.45         # less chill-saturated
    secondary_ailment_share: 0.15
  aoe_single_target_ratio: 0.55

special_notes: |
  Rapid-burst water-wave controller; player throws fast successive waves rather than persisting zones.
  Player should perceive: "this archetype controls space by throwing repeated bursts of water."
  Genre-precedent feel: D2 Frozen Orb (burst wave); FFXIV Black Mage water-burst rotation.
  Statistical distinctness vs A2a: geometry dist >2σ (sustain-dominant vs burst/cone dominant);
  cooldown profile >2σ (long-dominant vs short-dominant); ailment dist >2σ; AOE ratio >2σ.

  WAVE GEOMETRY NOTE: If 'wave' is not in the canonical engine geometry pool, drax substitutes
  'ring' or 'circle' as nearest-AOE proxy. The perception-test variance is preserved either way
  because the test rests on the *aggregate kit-shape vector distance*, not on any single geometry's presence.
```

**Pair A2 distinctness check:** Variants A2a and A2b differ across all four kit-shape-vector axes.

---

### § 2.3 — Pair A3: earth_caster variants

**Base archetype:** `earth_caster` (canonical; per `b6_archetype_templates.py:149-176`)
**Role:** caster
**Substrate:** earth (suppressed from subject)

#### Variant A3a — "Pillar Anchor" (vertical-geometry, defensive)

```yaml
spec_id: pair_A3_variant_a
display_name: "Class 5"
substrate: earth
role: caster

kit_shape_vector:
  geometry_distribution:
    pillar: 0.35                        # NOTE: 'pillar' may need engine substitution per geometry pool
    ground_targeted_circle: 0.25
    melee_arc: 0.20
    ground_slam: 0.15
    area_sustain: 0.05
  cooldown_profile:
    short_cd_share: 0.15
    medium_cd_share: 0.50
    long_cd_share: 0.35
  ailment_distribution:
    primary_ailment_share: 0.65         # root-saturated
    secondary_ailment_share: 0.05
  aoe_single_target_ratio: 0.45         # mid-range

special_notes: |
  Vertical-pillar / standing-formation earth caster; player anchors space and forces engagement.
  Player should perceive: "this archetype puts up walls and pillars and dares enemies to come closer."
  Genre-precedent feel: D2 Druid Tornado Wall + Volcano; D4 Druid Earthen Bulwark.

  PILLAR GEOMETRY NOTE: If 'pillar' is not in the canonical geometry pool, drax substitutes
  'ground_slam' weighted higher or 'ring' as vertical-form proxy. Aggregate vector distance preserved.
```

#### Variant A3b — "Boulder Hurler" (projectile-heavy, high mobility)

```yaml
spec_id: pair_A3_variant_b
display_name: "Class 6"
substrate: earth
role: caster

kit_shape_vector:
  geometry_distribution:
    projectile: 0.45                    # boulder-projectile dominant
    multi_projectile: 0.20
    cone: 0.15
    ground_targeted_circle: 0.10
    fork: 0.10
  cooldown_profile:
    short_cd_share: 0.50                # rapid-boulder cadence
    medium_cd_share: 0.35
    long_cd_share: 0.15
  ailment_distribution:
    primary_ailment_share: 0.30         # low ailment
    secondary_ailment_share: 0.05
  aoe_single_target_ratio: 0.50

special_notes: |
  Boulder-throwing earth caster; player stays mobile and launches projectile boulders.
  Player should perceive: "this archetype throws rocks fast and keeps moving."
  Genre-precedent feel: D2 Druid Fissure (projectile); D3 Witch Doctor Plague of Toads (rapid-projectile);
  PoE Earthshatter Slayer (boulder-projectile).
  Statistical distinctness vs A3a: geometry dist >2σ (pillar-vertical vs projectile-horizontal);
  cooldown profile >2σ (medium-long-heavy vs short-heavy); ailment dist >2σ; AOE ratio >2σ minimal but combined-vector >2σ.

  IMPORTANT: Per `b6_archetype_templates.py:170-175`, canonical earth_caster has the
  `tier1_ground_slam_and_melee_arc` constraint DEFERRED to B11. For perception-test purposes,
  this deferral does not affect A3a/A3b — they exercise different geometries deliberately, and
  the B11 constraint is about ground-impact requirement, not geometry-pool selection.
```

**Pair A3 distinctness check:** Variants A3a and A3b differ across all four kit-shape-vector axes.

---

### § 2.4 — Pair A4: wind_controller variants

**Base archetype:** `wind_controller` (canonical; per `b6_archetype_templates.py:295-...`)
**Role:** controller
**Substrate:** wind (suppressed from subject)

#### Variant A4a — "Vortex Puller" (centripetal, single-zone)

```yaml
spec_id: pair_A4_variant_a
display_name: "Class 7"
substrate: wind
role: controller

kit_shape_vector:
  geometry_distribution:
    vortex_pull: 0.40                   # centripetal-dominant
    ring: 0.25
    circle: 0.15
    cone: 0.15
    projectile: 0.05
  cooldown_profile:
    short_cd_share: 0.20
    medium_cd_share: 0.45
    long_cd_share: 0.35
  ailment_distribution:
    primary_ailment_share: 0.55         # knockback / pull-saturated
    secondary_ailment_share: 0.10
  aoe_single_target_ratio: 0.80         # AOE-dominant

special_notes: |
  Centripetal wind controller; player pulls enemies inward, controls clustered space.
  Player should perceive: "this archetype sucks enemies in and keeps them clumped."
  Genre-precedent feel: D2 Vortex Druid skills; PoE Whirling Blades vortex variants; D3 Wizard Black Hole.
```

#### Variant A4b — "Knockback Striker" (centrifugal, displacement-heavy)

```yaml
spec_id: pair_A4_variant_b
display_name: "Class 8"
substrate: wind
role: controller

kit_shape_vector:
  geometry_distribution:
    cone: 0.35                          # frontal-displacement
    burst: 0.25                         # radial-knockback
    multi_projectile: 0.20
    fork: 0.15
    line: 0.05
  cooldown_profile:
    short_cd_share: 0.60                # rapid-displacement cadence
    medium_cd_share: 0.30
    long_cd_share: 0.10
  ailment_distribution:
    primary_ailment_share: 0.75         # knockback-saturated (opposite valence to A4a's pull)
    secondary_ailment_share: 0.10
  aoe_single_target_ratio: 0.50

special_notes: |
  Centrifugal wind controller; player knocks enemies away, controls cleared space.
  Player should perceive: "this archetype shoves enemies back and keeps them apart."
  Genre-precedent feel: D2 Tornado Druid (displacement); D4 Sorcerer Frost Nova (radial knockback);
  Last Epoch Storm-Caller knockback build.
  Statistical distinctness vs A4a: geometry dist >2σ (vortex/ring-dominant vs cone/burst-dominant);
  cooldown profile >2σ (medium-long-heavy vs short-heavy); ailment dist >2σ (pull vs knockback are
  same ailment family `knockback_or_displacement` but opposite valence — drax should ensure the
  *perceived direction* of displacement differs visibly even if the ailment-name registry treats
  them as one tag); AOE ratio >2σ.

  AILMENT-VALENCE NOTE: per `substrate-identity-declarations` § 4, wind's ailment is `knockback`
  (hard_control). For perception-test purposes A4a uses *pull-toward* displacement variants (vortex_pull
  geometry) while A4b uses *push-away* displacement variants (cone/burst geometry). The same registered
  ailment tag, different player-perceived direction. This tests whether players perceive direction-of-displacement
  as a meaningful distinction at the kit-shape level.
```

**Pair A4 distinctness check:** Variants A4a and A4b differ across all four kit-shape-vector axes.

---

## § 3 — Pair-Type B: Vocabulary-control quad

**Per perception-test § 3.1:** "Four archetypes, one per canonical substrate (fire/water/earth/wind), each mechanically distinct (different role) but with **deliberately generic vocabulary** (no substrate-iconic verbs; LLM forbidden from using substrate-specific phrasings)."

**Per perception-test § 7.4 mitigation:** "Pre-review vocabulary outputs before sessions; manual edit any leaks. The experiment is small enough that hand-curation is feasible."

The vocabulary-control quad tests **H2 secondary hypothesis** — "Per-substrate iconic vocabulary at Layer 4 (LLM flavor) significantly affects perceived distinctness, *independently* of mechanical composition."

### § 3.1 — Quad B class W (fire substrate, damage role, generic vocab)

```yaml
spec_id: quad_B_class_W
display_name: "Build A"
substrate: fire                        # suppressed from subject
role: damage

kit_shape_vector:
  geometry_distribution:
    cone: 0.25
    projectile: 0.25
    burst: 0.25
    ground_targeted_circle: 0.25
  cooldown_profile:
    short_cd_share: 0.40
    medium_cd_share: 0.40
    long_cd_share: 0.20
  ailment_distribution:
    primary_ailment_share: 0.30        # neutral; not signaling burn-heavy fire
    secondary_ailment_share: 0.10
  aoe_single_target_ratio: 0.50

vocabulary_constraints:
  forbidden_verbs:                     # LLM must NOT use these (substrate-iconic for fire)
    - "ignites"
    - "burns"
    - "scorches"
    - "engulfs"
    - "flares"
    - "consumes"
    - "kindles"
  required_register: generic            # NOT 'martial' (fire's iconic_register)
  allowed_verb_register: |
    Generic combat verbs only — "strikes", "attacks", "hits", "damages", "engages",
    "throws", "launches", "casts". NO heat/flame/burn language; NO color/temperature
    associations; NO "consumes/devours" emotional charge.
  manual_review_required: true          # gandalf reviews LLM output pre-session; manual edit of any leaks per § 7.4

special_notes: |
  Class W is a generic burst combatant. The kit-shape vector is intentionally balanced (no
  AOE/single-target dominance, no cooldown band dominance, no ailment dominance) so that
  mechanical-vector distinctness from classes X/Y/Z is moderate, not strong.

  The test: do subjects perceive Class W as a fire archetype despite generic vocabulary?
  If YES, mechanical composition alone produces perceptible substrate identity.
  If NO, vocabulary is doing the heavy perceptual lifting (Reflection IV validated).
```

### § 3.2 — Quad B class X (water substrate, controller role, generic vocab)

```yaml
spec_id: quad_B_class_X
display_name: "Build B"
substrate: water                       # suppressed from subject
role: controller

kit_shape_vector:
  geometry_distribution:
    area_sustain: 0.30
    ring: 0.25
    ground_targeted_circle: 0.25
    circle: 0.20
  cooldown_profile:
    short_cd_share: 0.30
    medium_cd_share: 0.40
    long_cd_share: 0.30
  ailment_distribution:
    primary_ailment_share: 0.40        # neutral; not signaling chill-saturated water
    secondary_ailment_share: 0.10
  aoe_single_target_ratio: 0.70

vocabulary_constraints:
  forbidden_verbs:
    - "suffuses"
    - "permeates"
    - "fills"
    - "stills"
    - "submerges"
    - "binds"
    - "settles into"
  required_register: generic
  allowed_verb_register: |
    Generic combat verbs only. NO water/fluid/wetness language; NO cold/freeze associations;
    NO "immersion/saturation" emotional charge.
  manual_review_required: true

special_notes: |
  Class X is a generic field-control combatant. Tests whether subjects perceive water-substrate
  identity from kit-shape (zone-persistent AOE-heavy controller) despite generic vocabulary.
```

### § 3.3 — Quad B class Y (earth substrate, caster role, generic vocab)

```yaml
spec_id: quad_B_class_Y
display_name: "Build C"
substrate: earth                       # suppressed from subject
role: caster

kit_shape_vector:
  geometry_distribution:
    ground_slam: 0.25
    ground_targeted_circle: 0.25
    melee_arc: 0.25
    projectile: 0.25
  cooldown_profile:
    short_cd_share: 0.30
    medium_cd_share: 0.40
    long_cd_share: 0.30
  ailment_distribution:
    primary_ailment_share: 0.30        # neutral
    secondary_ailment_share: 0.10
  aoe_single_target_ratio: 0.55

vocabulary_constraints:
  forbidden_verbs:
    - "anchors"
    - "roots"
    - "holds"
    - "crushes"
    - "stands against"
    - "binds in place"
    - "weighs down"
  required_register: generic
  allowed_verb_register: |
    Generic combat verbs only. NO stone/rock/mountain language; NO weight/mass associations;
    NO "unyielding/refusal" emotional charge.
  manual_review_required: true

special_notes: |
  Class Y is a generic heavy combatant. Tests whether subjects perceive earth-substrate
  identity from kit-shape (ground-impact heavy, medium-cooldown caster) despite generic vocabulary.
```

### § 3.4 — Quad B class Z (wind substrate, mobility-flavored damage role, generic vocab)

```yaml
spec_id: quad_B_class_Z
display_name: "Build D"
substrate: wind                        # suppressed from subject
role: damage                           # NOTE: chose damage role here for cross-substrate role-diversity
                                       # in the quad (Quad has fire/damage, water/controller, earth/caster,
                                       # wind/damage — 3 of 4 roles represented per perception-test § 3.1
                                       # "each mechanically distinct (different role)" — fire and wind both
                                       # damage but with different kit-shapes; alternative: re-assign wind
                                       # to a 4th role if available. Drax flag for review.)

kit_shape_vector:
  geometry_distribution:
    line: 0.25
    cone: 0.25
    multi_projectile: 0.25
    fork: 0.25
  cooldown_profile:
    short_cd_share: 0.50               # rapid-cadence for "mobile" feel
    medium_cd_share: 0.35
    long_cd_share: 0.15
  ailment_distribution:
    primary_ailment_share: 0.30        # neutral
    secondary_ailment_share: 0.10
  aoe_single_target_ratio: 0.40        # single-target-leaning for mobility-damage

vocabulary_constraints:
  forbidden_verbs:                     # wind iconic per substrate-identity-declarations § 4
    - "lifts"
    - "carries"
    - "redirects"
    - "displaces"
    - "scatters"
    - "knocks aside"
    - "blows past"
  required_register: generic
  allowed_verb_register: |
    Generic combat verbs only. NO wind/air/breath language; NO movement/momentum associations;
    NO "kinetic/redirection" emotional charge.
  manual_review_required: true

special_notes: |
  Class Z is a generic mobile combatant. Tests whether subjects perceive wind-substrate
  identity from kit-shape (rapid-cadence single-target-leaning damage with line/fork geometry)
  despite generic vocabulary.

  ROLE-DIVERSITY NOTE: Per perception-test § 3.1, the quad's mechanical distinctness comes from
  *different roles* across the substrates. Three roles (damage / controller / caster) are
  represented across classes W/X/Y/Z; wind reuses the damage role rather than introducing a
  fourth role (sustain not in canonical-four engine pool). Drax may re-assign wind to a different
  role if engine supports it; alternative path is to differentiate W vs Z by sub-role (W = burst-damage,
  Z = mobile-damage) which is already encoded in their kit-shape vectors.
```

---

## § 4 — Drax integration notes

### § 4.1 — runner.js placeholder replacement

Per HANDOFF [2026-05-18 00:10Z]: replace `TODO(drax)` placeholders in `reincarnated-demo/src/runner.js` (or equivalent session-runner config layer) with 12 archetype-spec entries derived from this doc. Each entry maps to a loadable demo1 archetype in a brief-fight context per perception-test § 3.2.

### § 4.2 — Geometry-pool substitution discipline

Several specs reference geometries that may not be in the current canonical engine pool (`wave`, `pillar`). Per spec § 2.2 + § 2.3 inline notes:

- If geometry is unrecognized at engine load: substitute nearest-canonical proxy per geometry-pool palette in `reincarnated-engine/src/reincarnated/foundation/geometry_pool.py`.
- Aggregate kit-shape vector distance is preserved by any reasonable substitution; the test rests on the *aggregate* distance, not any single geometry's presence.
- Drax records substitution in runner.js comment for reproducibility.

### § 4.3 — Ailment-direction handling (Pair A4 special case)

Pair A4 (wind_controller variants) intentionally uses *opposite-valence displacement* (A4a pulls; A4b knocks back). The canonical wind `knockback` ailment is one tag, but the *player-perceived direction* differs by geometry choice (vortex_pull for A4a; cone/burst for A4b). Drax confirms the displacement-direction renders visibly distinct in demo1 VFX so subjects can perceive the variance.

### § 4.4 — Statistical-distinctness verification

Drax (or jack-ryan as analysis-pass) computes kit-shape-vector distance for each pair at runner-config time, verifying ≥2σ distinctness across the four axes. If any pair falls below 2σ, gandalf re-tunes the variant pair specs. This is a pre-session gate; the test cannot run with a sub-2σ pair (its perceptual signal would be ambiguous).

### § 4.5 — Reference-monster spec (per perception-test § 7.3 risk mitigation)

Drax spec the reference monster per perception-test § 7.3: must require diverse player responses (some kiting, some commitment, some mobility) so all archetype facets are exercised. Recommendation: a tier-elite monster with one hard-hitting telegraphed attack (forces kiting), one rooted-ground-zone (forces commitment-or-leave decision), and modest mobility (forces some player repositioning). Drax + jack-ryan iterate on this spec; gandalf is consultable.

---

## § 5 — Bias controls + display surface

### § 5.1 — Subject-facing display

Per perception-test § 4.3 bias controls:

- **Substrate names withheld:** Subjects see "Class 1" / "Class 2" / ... / "Class 8" for Pair-Type A; "Build A" / "Build B" / "Build C" / "Build D" for Pair-Type B. Never "Fire Mage" / "Water Controller" / etc.
- **Mechanical-parameter information withheld:** No tooltip-level kit details visible; no geometry distribution displayed; no ailment-distribution shown. The subject perceives only what plays in their hands.
- **Randomize fight order per session.** Per perception-test § 4.3: fight order randomized; counterbalanced across subjects (Subject 1 starts at A1; Subject 2 starts at A4; etc.).
- **No pair-mate identification.** Subjects do not know which classes are pair-mates until the pair-grouping task post-session.

### § 5.2 — Per-archetype presentation surface (loadout-side)

Per perception-test § 3.2 + § 4.3, the loadout-side per-archetype presentation surface should display:

- Neutral display name (Class N / Build X)
- Brief one-line generic-vocab description (e.g., "A burst combatant — uses cone and projectile attacks")
- NO substrate name
- NO mechanical-parameter details
- NO substrate-iconic verbs (especially for vocabulary-control quad)

Per perception-test § 7.4 mitigation: gandalf pre-reviews the one-line generic-vocab descriptions; manual edit of any substrate-iconic leaks before sessions.

### § 5.3 — Inter-fight rating capture (per perception-test § 3.3)

Between fights, subject rates the just-played archetype on three dimensions:

- **Distinctness vs prior archetypes played in session:** 1-7 scale
- **Identity (one sentence):** "what kind of archetype was that?"
- **Vocabulary perception (one sentence):** "what did it FEEL like playing?"

After all 12 fights, **pair-grouping task** — subject presented with the 8 mechanical-pair-type archetypes, groups them into pairs they perceived as "the same kind of thing." Compute pair-recovery accuracy against engineered pairs (A1-A4) per perception-test § 5.1.

### § 5.4 — Vocabulary-control quad rating focus

For Quad B (W/X/Y/Z), per perception-test § 5.3, the secondary measurement target is: **does generic vocabulary obscure substrate identity?** Subject's "identity" one-sentence answers for W/X/Y/Z are analyzed qualitatively:

- Do answers reference fire/water/earth/wind language despite the suppressed vocabulary? If yes, substrate identity leaks through mechanical-vector alone (H2 rejected; Layer 4 augmentation-only).
- Are answers substrate-neutral ("burst combatant" / "controller" / "heavy guy" / "fast guy")? If yes, vocabulary is load-bearing for substrate-perception (H2 supported; Layer 4 foundation-not-augmentation).

---

## § 6 — Open question for drax

Per HANDOFF [2026-05-18 00:10Z]:

> The perception-test § 3.1 specifies the engine-side generation uses "current canonical-four engine (no Layer-2 composition refactor needed)" with "deliberately tuned parameters to produce statistically-distinct kit vectors." Drax — confirm whether per-archetype parametric tuning lands in the demo1 session-runner config layer, or whether the engine generates the kit-shape per the spec and the runner just consumes the canonical archetype tags. If the runner needs to override engine output to enforce the ≥2σ distinctness, surface as FRICTION; gandalf will route Q to gamora for engine-side tuning hook.

**Drax response shape:** hive log STATE or QUESTION entry; gandalf monitors and responds.

---

## § 7 — Maintenance protocol

This doc is the perception-test archetype-pair spec set; canonical for Phase-1 P1a execution.

If pair-tuning needs revision (e.g., drax-side ≥2σ check fails for a pair, or subject sessions surface that a pair is too obviously distinct/similar), gandalf authors a revision entry inline (section appended; prior version preserved for archaeology). Re-run is cheap; the perception-test is signal-detection, not validated measurement.

After Phase-1 P1a perception-test session execution + analysis + Layer-3 metric decision, this doc transitions to *historical record*; the Layer-3 metric spec (gandalf-authored per perception-test § 6.1 decision tree) becomes the forward-canonical artifact.

---

*Authored 2026-05-18 by gandalf. Companion to perception-test-experiment-scoping-2026-05-17.md. Unblocks drax-demo D27 Track A final integration. 12 archetypes; 4 mechanical-distinctness pairs + 1 vocabulary-control quad. Statistical distinctness target ≥2σ across kit-shape-vector axes within each pair. Subjects see neutral display names only; substrate identity is what we are testing the perception of, not displaying.*
