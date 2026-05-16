# 08 — Archetype Decomposition Report
# Season_000042 — Dimensional Analysis

**Date:** 2026-05-08
**Purpose:** Apply the dimensional generation proposal (`03-architectural-proposal.md`) to all 11 season_000042 archetypes. Produce evidence for the A/B/C architectural decision.
**Constraint:** Read-only investigation. No code changes. No regeneration.

---

## Pre-Decomposition Findings — Load-Bearing for the Architectural Decision

These three findings emerged from reading the engine source before decomposing a single class. They materially reframe the A/B/C options as framed in `04-decision-options.md`. Read these before the per-class decompositions.

---

### Finding 1: Element is already a first-class generation input. Archetype is already an emergent output.

The `class_generator.py` takes `dominant_element` as its primary input. After generating skills, `archetype_classifier.py` derives the archetype label post-hoc from element + role profile. The stat template is then looked up by archetype label. The pipeline flow is:

**element → roles → archetype label → stats**

The archetype label is not a generation input — it is a classification of what was generated. This means the engine is structurally closer to dimensional generation than `03-architectural-proposal.md` assumed. Element is already a dimension. Archetype is already emergent.

**Why this reframes the A/B/C decision:**

Option C is described in the docs as a "fundamental refactor" — replacing archetype-driven generation with dimensional generation. But there are no archetype-driven generation templates to replace. The generator doesn't use archetype as an input. What Option C actually requires is **adding 2–3 more generation dimensions to a pipeline that already operates dimensionally on element.** The scope is meaningfully smaller than the "2–3 week" estimate assumed.

Conversely, Option B's framing — "energy types within current architecture, added per archetype" — is confused by this finding. There are no archetype templates that generation flows through. Archetypes are derived labels. "Adding energy type to the warrior archetype" would require adding energy type as a generation input (i.e., a new dimension), which is structurally what Option C does. Options B and C are closer in shape than the docs suggested; the difference is primarily how many dimensions are added and whether melee geometry is included.

---

### Finding 2: Physical warriors have mana costs, but their stat distribution gives them essentially no mana pool.

Every physical warrior ability has `mana_cost_pct` in the range 14–30%. The physical warrior stat template is `str=150, vit=80, dex=30, int=5, wis=5`. With int=5 and wis=7, the mana pool is close to the base minimum. At 14–30% cost per ability fired, these classes exhaust their mana in approximately 2 seconds of combat.

This is not a bug in the mana sustainability validator — it's a consequence of the generation pipeline assigning mana costs to a class whose stat distribution does not support mana. The pipeline assigns `mana_cost_pct` to every class because mana is the only resource type that exists. There is nothing to validate against because the pipeline has no concept of "this class should not have mana costs."

**Why this reframes Option A:**

Option A's proposed tactical fix is: "validate sustainability at generation time — reject combinations where mana depletes too quickly." But the issue isn't the combination — it's the assumption that physical warriors have mana at all. A validator would need to either (a) reject every physical warrior ability set (because no combination is sustainable with int=5, wis=5) or (b) special-case physical warriors to have no mana cost. Either approach patches the symptom while keeping the structural assumption that everything has mana.

Dimensional generation removes this assumption: a rage-typed combatant doesn't have a mana pool. The bug becomes structurally impossible, not just caught by a validator. Option A's patch feels more like a band-aid in this light than `04-decision-options.md` conveyed.

---

### Finding 3: Melee geometry does not exist. Building it is real scope for Option C.

The ability grammar (`role_constraints.py`) defines these geometry options: `single_target`, `projectile`, `cone`, `circle`, `line`, `persistent_zone`. "Melee" is not in the list. Both physical warriors in season_000042 have `projectile` as their primary attack geometry — because that was the closest available option in the grammar.

Close-range combat (the warrior's design intent) has no mechanical representation in the current engine. "Range profile = close" is a design intent that requires building a new geometry type, updating the simulator to handle it (melee range combat, facing mechanics, etc.), and constraining the ability grammar to use it only for close-range archetypes.

**Why this matters for Option C's estimate:**

`03-architectural-proposal.md` estimated 2–3 weeks for Option C. That estimate does not appear to account for melee geometry as a distinct work item. If melee geometry is treated as a prerequisite for the range dimension to be meaningful, it's real work — probably 3–5 days for the geometry type itself plus simulator support. Not a deal-breaker, but a budgeting reality that the estimate glossed over. Any decision to proceed with Option C should include this explicitly in the scope.

---

*The above three findings are pre-decomposition. The per-archetype analysis follows.*

---

## Data Sources

- Telemetry DB (`data/telemetry.db`): `classes` and `abilities` tables — canonical element, stats, balance metadata, geometry/role/mana data per skill
- Season JSON (`seasons/season_000042/classes/class_XXXX.json`) — full skill specs including effects
- Source files read for engine context:
  - `src/reincarnated/generation/stat_allocator.py` — archetype stat templates
  - `src/reincarnated/generation/archetype_classifier.py` — how archetype labels are derived
  - `src/reincarnated/generation/role_constraints.py` — ability grammar role definitions
  - `src/reincarnated/generation/class_generator.py` — generation inputs and flow

---

## Important Caveats on This Report

Three of the four axes require inference or are prospective. Read the quality judgments with this in mind.

**Energy type — prospective, not descriptive.** No rage/combo/focus mechanics exist in the engine. All 11 classes use `mana_cost_pct` for every ability. Energy type assignments in this report represent what each class *would get* under dimensional generation — not what it currently has. Where I write "rage (intended) / mana (actual)" I am naming a design gap, not a classification ambiguity.

**Range profile — inferred from geometry, contested.** No range field exists in the DB or JSON. Range is inferred from geometry_type patterns and archetype semantics. More importantly: **the engine has no melee geometry type.** `single_target`, `projectile`, `cone`, `circle`, `line`, `persistent_zone` exist. "Melee" does not. Close-range combat is a design intent with no implementation basis in the current engine.

**Armor weight — cleanly inferred from stats.** High str+vit (stat budget = 270 total) = heavy; high int or wis = light; balanced = medium. No ambiguity in any case.

**Damage type — directly from DB.** `canonical_element` field is first-class in the DB and JSON. No inference.

---

## The Four Proposed Axes

| Axis | Options |
|------|---------|
| Energy type | rage / combo / focus / mana / stamina-as-resource / none (cooldown-only) |
| Range profile | close / medium / long |
| Armor weight | light / medium / heavy |
| Damage type | physical / fire / wind / water / earth / hybrid |

---

## One Architectural Observation Before Decompositions

Discovered while reading source: the archetype label (`fire_mage`, `physical_warrior`, etc.) is already an **output** in the current engine, not an input. `archetype_classifier.py` derives it post-hoc from `dominant_element` + role profile after skills are generated. `class_generator.py` takes `dominant_element` as its primary generation input. The archetype label then determines which stat template to apply.

The flow is: **element → roles → archetype label → stats**.

This means the engine is structurally closer to dimensional generation than its surface appearance suggests. Element is already a first-class generation dimension. Archetype is already emergent. What's missing is the other three dimensions (energy type, range profile, armor weight) as generation inputs rather than derived labels.

---

## Per-Archetype Decompositions

### class_0001 — fire_mage (A)

**Stats:** str=5, vit=67, int=163, wis=16, dex=19

**Abilities:**
| Role | Geometry | Mana% | Effects |
|------|----------|-------|---------|
| primary_attack | single_target | 5.2 | damage (fire 625) |
| burst_damage | cone | 38.5 | damage (fire 2500) |
| area_damage | cone | 24.1 | damage (fire 1500) |
| damage_over_time | circle | 19.3 | burn (750/tick, 5.2s) + damage (fire 750) |
| defensive | single_target | 22.5 | shield (1000, 5.8s) + buff_dodge (14%) |

**Convergence:** CONVERGED — 49.45% win rate. Modifier: 0.30.

**Decomposition:**

| Axis | Assignment | Basis |
|------|-----------|-------|
| Energy type | **mana** | All abilities have mana_cost_pct (5.2–38.5%). int=163 → large mana pool. Passive regen model. |
| Range profile | **long** | No melee geometry; all abilities cast from range. Cone and circle at caster engagement scale. |
| Armor weight | **light** | int+wis=179, str+vit=72. Classic glass cannon ratio. |
| Damage type | **fire** | canonical_element=fire on all skills. |

**Verdict: NATURAL.** Textbook mana+long+light+fire glass cannon. No friction on any axis.

**Beyond-axis aspects:** Burn (DOT ailment) is the fire element's signature — it's sub-dimensional flavor within fire, not a separate axis. Defensive ability is generic (shield + dodge) and doesn't add dimensional complexity.

---

### class_0006 — fire_mage (B)

**Stats:** str=9, vit=70, int=162, wis=10, dex=19

**Abilities:**
| Role | Geometry | Mana% | Effects |
|------|----------|-------|---------|
| primary_attack | single_target | 14.7 | damage (fire 625) |
| burst_damage | cone | 22.4 | damage (fire 2500) + burn (750/tick, 5.9s) |
| area_damage | line | 17.7 | damage (fire 1500) + burn (750/tick, 4.0s) |
| damage_over_time | single_target | 17.6 | burn (750/tick, 5.2s) |
| defensive | single_target | 18.4 | shield (1000, 6.9s) + buff_dodge (32%) |
| utility | circle | 13.6 | buff_damage (11%) |

**Convergence:** CONVERGED — 51.35% win rate. Modifier: 0.2125.

**Decomposition:**

| Axis | Assignment | Basis |
|------|-----------|-------|
| Energy type | **mana** | mana_cost_pct on all abilities (13.6–22.4%). Same mana economy profile as class_0001. |
| Range profile | **long** | Line geometry on area_damage reinforces long-range identity; same caster profile. |
| Armor weight | **light** | int+wis=172, str+vit=79. Glass cannon. |
| Damage type | **fire** | canonical_element=fire on all skills. Burn appears on 4/6 abilities — heavily burn-specialized. |

**Verdict: NATURAL.**

**Notable:** class_0001 and class_0006 have **identical dimensional profiles**: mana+long+light+fire. Under the proposed 5–6 class per season structure with dimensional diversity constraints, this duplication should not occur. Two classes sharing the same dimensional profile give the trial-room player a choice between clones, not distinct combatants.

---

### class_0002 — water_mage (A)

**Stats:** str=5, vit=79, int=150, wis=10, dex=26

**Abilities:**
| Role | Geometry | Mana% | Effects |
|------|----------|-------|---------|
| primary_attack | projectile | 12.7 | damage (water 625) + chill (slow 26%, 3.2s) |
| burst_damage | cone | 34.6 | damage (water 2500) |
| area_damage | circle | 19.9 | damage (water 1500) |
| damage_over_time | circle | 20.2 | chill (slow 39%, 3.5s) + damage (water 750) |
| defensive | single_target | 22.0 | shield (1000, 5.0s) |

**Convergence:** CONVERGED — 52.85% win rate. Modifier: 0.40.

**Decomposition:**

| Axis | Assignment | Basis |
|------|-----------|-------|
| Energy type | **mana** | mana_cost_pct on all abilities (12.7–34.6%). int=150 → large mana pool. |
| Range profile | **long** | Projectile primary attack (explicit ranged). Cone/circle at caster scale. |
| Armor weight | **light** | int+wis=160, str+vit=84. Glass cannon. |
| Damage type | **water** | canonical_element=water on all skills. |

**Verdict: NATURAL.**

**Beyond-axis aspects:** Chill (slow) on 2/5 abilities gives this class meaningful control — slowing enemies affects pacing. Chill is water's signature ailment, sub-dimensional within water. Does not require a separate axis. However, this is the first class where a "control orientation" sub-property is visible; it will be more significant in the earth casters.

---

### class_0007 — water_mage (B)

**Stats:** str=6, vit=85, int=149, wis=10, dex=20

**Abilities:**
| Role | Geometry | Mana% | Effects |
|------|----------|-------|---------|
| primary_attack | single_target | 11.3 | damage (water 625) |
| burst_damage | cone | 37.7 | damage (water 2500) |
| area_damage | circle | 25.7 | damage (water 1500) + chill (slow 40%, 2.2s) |
| damage_over_time | single_target | 10.7 | chill (slow 42%, 4.3s) |
| defensive | single_target | 20.2 | shield (1000, 4.6s) |
| utility | single_target | 18.3 | buff_damage (13%) + buff_mana_regen (14%) |

**Convergence:** CONVERGED — 47.75% win rate. Modifier: 0.3812.

**Decomposition:**

| Axis | Assignment | Basis |
|------|-----------|-------|
| Energy type | **mana** | Same profile as class_0002. Utility ability provides buff_mana_regen — this class sustains mana actively as well as passively. |
| Range profile | **long** | Same caster profile as class_0002. |
| Armor weight | **light** | int+wis=159, str+vit=91. Glass cannon. |
| Damage type | **water** | canonical_element=water on all skills. |

**Verdict: NATURAL.**

**Notable:** class_0002 and class_0007 are dimensionally identical (mana+long+light+water). Same duplication concern as the two fire mages. The buff_mana_regen utility differentiates them sub-dimensionally (self-sustaining mana vs. not) but doesn't warrant a new axis.

---

### class_0003 — earth_caster (A)

**Stats:** str=9, vit=70, int=16, wis=158, dex=17

**Abilities:**
| Role | Geometry | Mana% | Effects |
|------|----------|-------|---------|
| primary_attack | single_target | 8.1 | damage (earth 625) |
| burst_damage | single_target | 36.1 | damage (earth 2500) + root (3.1s) + buff_damage (16%) |
| area_damage | circle | 19.4 | damage (earth 1500) |
| damage_over_time | single_target | 15.0 | root (1.6s) + damage (earth 750) |
| defensive | single_target | 20.0 | shield (1000, 4.3s) + buff_dodge (17%) |

**Convergence:** CONVERGED — 47.0% win rate. Modifier: 0.35.

**Decomposition:**

| Axis | Assignment | Basis |
|------|-----------|-------|
| Energy type | **mana** | mana_cost_pct on all abilities (8.1–36.1%). wis=158 → large mana pool (wis as mana stat). |
| Range profile | **medium** *(contested)* | No projectile primary; single_target dominant. Root mechanics intuitively imply engaging a target at controlled distance (can't root from extreme range in most design conventions). Assigning medium is a judgment call — there is no geometric evidence because melee geometry doesn't exist. |
| Armor weight | **light** | int+wis=174, str+vit=79. |
| Damage type | **earth** | canonical_element=earth on all skills. |

**Verdict: SOMEWHAT FORCED** — primarily on the range axis.

Energy type (mana) and armor weight (light) are clean. Damage type (earth) is direct. The range call requires design inference that the engine cannot support yet. The assignment is defensible but not observed.

**Beyond-axis aspects:** Root on 2/5 abilities (burst_damage and damage_over_time) establishes a **controller identity** — immobilizing enemies is a distinct tactical role. Root ≠ burn ≠ chill ≠ knockback in gameplay feel, even though all are ailments within their elements. The earth caster is already starting to feel like "earth controller" rather than "earth caster," and this identity is not captured by any proposed axis.

---

### class_0008 — earth_caster (B)

**Stats:** str=10, vit=74, int=11, wis=155, dex=20

**Abilities:**
| Role | Geometry | Mana% | Effects |
|------|----------|-------|---------|
| primary_attack | single_target | 13.3 | damage (earth 625) + root (1.9s) |
| burst_damage | single_target | 34.4 | damage (earth 2500) + root (1.9s) + buff_damage (34%) |
| area_damage | circle | 20.4 | damage (earth 1500) |
| damage_over_time | circle | 17.8 | root (3.4s) + damage (earth 750) |
| defensive | single_target | 16.8 | shield (1000, 6.2s) |
| utility | circle | 12.3 | buff_damage (31%) |

**Convergence:** CONVERGED — 51.8% win rate. Modifier: 0.45.

**Decomposition:**

| Axis | Assignment | Basis |
|------|-----------|-------|
| Energy type | **mana** | Same as class_0003. |
| Range profile | **medium** *(contested)* | Same reasoning as class_0003. |
| Armor weight | **light** | int+wis=166, str+vit=84. |
| Damage type | **earth** | canonical_element=earth on all skills. |

**Verdict: SOMEWHAT FORCED** — same friction as class_0003, amplified.

Root appears on 3/6 abilities including the **primary attack**. This class is more "earth controller" than "earth caster" — the controller role is dominant, not secondary. Under the four proposed axes, it decomposes identically to class_0003 (mana+medium+light+earth), masking a meaningful functional difference between the two.

**Notable:** If a "control orientation" axis (low/medium/high) existed, class_0003 would be medium and class_0008 high. Under four axes, they're indistinguishable. This is the clearest evidence yet that role/function orientation is a missing axis.

---

### class_0004 — wind_caster (A)

**Stats:** str=6, vit=74, int=6, wis=154, dex=30

**Abilities:**
| Role | Geometry | Mana% | Effects |
|------|----------|-------|---------|
| primary_attack | single_target | 12.1 | damage (wind 625) + knockback (3.3m, stagger 1.0s) |
| burst_damage | circle | 23.5 | damage (wind 2500) |
| area_damage | cone | 28.2 | damage (wind 1500) |
| damage_over_time | circle | 10.4 | knockback (3.4m, stagger 1.0s) + damage (wind 750) |
| defensive | single_target | 22.4 | shield (1000, 4.2s) + buff_dodge (22%) |

**Convergence:** CONVERGED — 50.95% win rate. Modifier: 0.4812.

**Decomposition:**

| Axis | Assignment | Basis |
|------|-----------|-------|
| Energy type | **mana** | mana_cost_pct on all abilities (10.4–28.2%). wis=154 → large mana pool. |
| Range profile | **medium** *(contested)* | Knockback displacement mechanics suggest engaging at medium distance — you push enemies away from you, which implies proximity. Cone geometry implies frontal orientation. No close or long geometry available to confirm. |
| Armor weight | **light** | int+wis=160, str+vit=80. High dex (30) hints at mobility orientation. |
| Damage type | **wind** | canonical_element=wind on all skills. |

**Verdict: SOMEWHAT FORCED.**

Assignments are defensible but none feel inevitable. Wind casters are intuitively mobile disruptors — knockback + high dex + buff_dodge reads as "hits hard, sends enemies flying, stays evasive." This is functionally different from earth controllers (root = lock down), even though both decompose to mana+medium+light+their-element. The four axes distinguish them by damage type but not by their tactical identities.

**Beyond-axis aspects:** Knockback (displacement) is mechanically distinct from root (immobilization) and burn (sustained damage). Earth controllers lock enemies in place; wind disruptors send them flying. The tactical difference is significant. A "mobility/disruption orientation" sub-dimension (or full axis) would capture this.

---

### class_0009 — wind_caster (B)

**Stats:** str=6, vit=67, int=9, wis=153, dex=35

**Abilities:**
| Role | Geometry | Mana% | Effects |
|------|----------|-------|---------|
| primary_attack | single_target | 6.5 | damage (wind 625) |
| burst_damage | circle | 26.6 | damage (wind 2500) |
| area_damage | cone | 27.3 | damage (wind 1500) |
| damage_over_time | single_target | 12.3 | knockback (**7.6m**, stagger 0.8s) + damage (wind 750) |
| defensive | single_target | 20.0 | shield (1000, 7.9s) |

**Convergence:** INTENTIONAL_OUTLIER — 59.7% win rate (target 60%). Modifier: 0.40.

**Decomposition:**

| Axis | Assignment | Basis |
|------|-----------|-------|
| Energy type | **mana** | Same as class_0004. |
| Range profile | **medium** *(contested)* | Same reasoning as class_0004. |
| Armor weight | **light** | int+wis=162, str+vit=73. Highest dex in dataset (35). |
| Damage type | **wind** | canonical_element=wind on all skills. |

**Verdict: SOMEWHAT FORCED** — same pattern as class_0004.

**Notable:** The 7.6m knockback DOT (vs. 3.3–3.4m on class_0004) is a power-level difference, not a dimensional one. This class is INTENTIONAL_OUTLIER at 60% target — overtuned. Under the new generation structure (5–6 playable + 3 act-boss), this would be a later-act boss dimensional profile. The dimensional profile (mana+medium+light+wind) is identical to class_0004, but the balance target and power ceiling separate them structurally into different generation roles (playable vs. boss). This is the clearest case in the dataset showing how balance target interacts with dimensional profile to determine generation role.

---

### class_0005 — physical_warrior (A)

**Stats:** str=145, vit=83, int=5, wis=7, dex=30

**Abilities:**
| Role | Geometry | Mana% | Effects |
|------|----------|-------|---------|
| primary_attack | **projectile** | 14.0 | damage (physical 625) |
| burst_damage | cone | 30.2 | damage (physical 2500) |
| area_damage | circle | 27.4 | damage (physical 1500) |
| damage_over_time | circle | 15.6 | bleed (750/tick, 3.3s) + damage (physical 750) |
| defensive | single_target | 22.2 | shield (1000, 6.0s) |

**Convergence:** INTENTIONAL_OUTLIER — 42.4% win rate (target 40%). Modifier: 0.50.

**Decomposition:**

| Axis | Assignment | Basis |
|------|-----------|-------|
| Energy type | **rage** *(intended)* / **mana** *(actual)* | mana_cost_pct: 14.0–30.2%. With int=5, wis=7, this class has almost no mana pool. It burns through its mana within ~2 seconds of combat at these cost rates. The intended dimensional identity for a physical warrior is rage. The actual implementation assigns mana by default. **This is the mana economy bug expressed as a dimensional misassignment.** |
| Range profile | **close** *(intended)* / **projectile** *(actual)* | "Warrior" semantics in every ARPG genre reference mean close-range melee. The actual primary attack geometry is **projectile** — explicitly ranged. **The engine has no melee geometry type.** Close-range is a design intent without any implementation basis. |
| Armor weight | **heavy** | str+vit=228, int+wis=12. Unambiguous. |
| Damage type | **physical** | canonical_element=physical on all skills. |

**Verdict: FORCED** — two axes are structurally broken, not just ambiguous.

Armor weight (heavy) and damage type (physical) are clean. Energy type and range profile are both fundamentally misassigned by the current engine — not because the classification is difficult but because the correct axis values don't exist in the implementation. "Rage" mechanics and "melee" geometry would both need to be built.

**Significance:** This class is the most important case in the dataset. Its two forced axes are not labeling problems — they are the **root causes** of two distinct known issues: the mana economy bug (energy type mismatch) and the lack of close-combat geometry (range profile mismatch). Dimensional generation would make both of these structurally impossible by only assigning mana to mana-typed classes and only assigning projectile geometry to ranged classes.

---

### class_0010 — physical_warrior (B)

**Stats:** str=150, vit=78, int=7, wis=5, dex=30

**Abilities:**
| Role | Geometry | Mana% | Effects |
|------|----------|-------|---------|
| primary_attack | **projectile** | 14.6 | damage (physical 625) + bleed (750/tick, 3.5s) |
| burst_damage | cone | 20.7 | damage (physical 2500) + bleed (750/tick, 6.5s) + buff_damage (12%) |
| area_damage | circle | 29.3 | damage (physical 1500) |
| damage_over_time | single_target | 18.1 | bleed (750/tick, 3.1s) + damage (physical 750) |
| defensive | single_target | 18.2 | shield (1000, 7.6s) |

**Convergence:** CONVERGED — 49.5% win rate. Modifier: 0.25.

**Decomposition:**

| Axis | Assignment | Basis |
|------|-----------|-------|
| Energy type | **rage** *(intended)* / **mana** *(actual)* | Same structural problem as class_0005. |
| Range profile | **close** *(intended)* / **projectile** *(actual)* | Same structural problem as class_0005. |
| Armor weight | **heavy** | str+vit=228, int+wis=12. |
| Damage type | **physical** | canonical_element=physical on all skills. |

**Verdict: FORCED** — same structural problems as class_0005.

**Beyond-axis aspects:** Bleed on 3/5 abilities (primary, burst, DOT) makes this class more bleed-specialized than class_0005 (where bleed appears on only 1/5). Both physical warriors share the same dimensional profile, but bleed density distinguishes them at the ailment sub-dimension level.

---

### class_0011 — support_healer

**Stats:** str=12, vit=78, int=31, wis=140, dex=9

**Abilities:**
| Role | Geometry | Mana% | Effects |
|------|----------|-------|---------|
| sustain | single_target | 20.8 | heal (1250) |
| sustain | single_target | 34.2 | heal (1250) |
| primary_attack | projectile | 6.9 | damage (fire 625) |
| primary_attack | projectile | 6.2 | damage (fire 625) |
| defensive | single_target | 20.3 | shield (1000, 6.0s) |
| sustain | single_target | 30.1 | heal (1250) |

**Convergence:** CONVERGED — 48.05% win rate. Modifier: 0.5625.

**Decomposition:**

| Axis | Assignment | Basis |
|------|-----------|-------|
| Energy type | **mana** | mana_cost_pct on all abilities (6.2–34.2%). wis=140 → large mana pool. |
| Range profile | **medium** | Projectile primary attacks (ranged); heals are self-targeted (single_target). The class attacks at range and heals inward. Medium is the least-wrong assignment but doesn't describe either action cleanly. |
| Armor weight | **medium** | int+wis=171, str+vit=90. Neither glass cannon (wis+vit combination is more durable) nor heavy. A "durable support" profile. |
| Damage type | **fire** *(nominal)* | canonical_element=fire on all 6 skills including the 3 heals. The heals deal no fire damage — the fire tag is carried by the class's dominant element, not by the heal effect itself. A "fire healer" and a "fire mage" share the same damage type label under this scheme despite having completely different functional identities. |

**Verdict: FORCED** — one axis is structurally insufficient for this class type.

Energy type (mana), range profile (medium), and armor weight (medium) are defensible if imprecise. The fundamental problem is that the four proposed axes **cannot distinguish a healer from a damage dealer that shares its element**. A fire mage and a fire healer would both be mana+long+light+fire (or mana+medium+medium+fire in this case). Their entire functional identities differ — one heals through combat, one blasts through it — but the dimensional framework has no axis that expresses this difference.

This is not an edge case. Healers/supporters are a standard ARPG archetype. The framework needs a fifth axis to handle them.

---

## Aggregate Findings

### Decomposition quality summary

| Class | Archetype | Dimensional Profile | Quality |
|-------|-----------|---------------------|---------|
| class_0001 | fire_mage (A) | mana + long + light + fire | **Natural** |
| class_0006 | fire_mage (B) | mana + long + light + fire | **Natural** |
| class_0002 | water_mage (A) | mana + long + light + water | **Natural** |
| class_0007 | water_mage (B) | mana + long + light + water | **Natural** |
| class_0003 | earth_caster (A) | mana + medium + light + earth | **Somewhat forced** |
| class_0008 | earth_caster (B) | mana + medium + light + earth | **Somewhat forced** |
| class_0004 | wind_caster (A) | mana + medium + light + wind | **Somewhat forced** |
| class_0009 | wind_caster (B) | mana + medium + light + wind | **Somewhat forced** |
| class_0005 | physical_warrior (A) | rage*/mana + close*/projectile + heavy + physical | **Forced** |
| class_0010 | physical_warrior (B) | rage*/mana + close*/projectile + heavy + physical | **Forced** |
| class_0011 | support_healer | mana + medium + medium + fire† | **Forced** |

*intended / actual split — axes structurally broken in current engine
†fire is nominal; heals are element-agnostic in effect

**Natural: 4 (36%)** — fire and water mages
**Somewhat forced: 4 (36%)** — earth and wind casters
**Forced: 3 (27%)** — physical warriors and support healer

---

### Sources of friction

**1. Energy type — structurally absent for physical archetypes (critical)**

The current engine assigns mana to every class regardless of archetype. Physical warriors have mana_cost_pct of 14–30% on every ability but int=5 and wis=7, producing a mana pool so small it depletes within ~2 seconds of combat. "Energy type" as a dimensional axis doesn't exist — it's not in the DB, not in the JSON, not in the class generator's inputs. The intended mapping (warrior → rage) would require building rage mechanics from scratch. The mana economy bug is the observable symptom of this absent dimension.

**2. Range profile — no melee geometry exists (critical)**

The ability grammar has no melee geometry. `single_target`, `projectile`, `cone`, `circle`, `line`, `persistent_zone` — none of these express close-range melee. A physical warrior's primary attack in this dataset is `projectile` — because it's the closest available geometry to "something that attacks one target." Close-range combat is design intent without implementation. This must be built as part of dimensional generation, not labeled onto existing data.

**3. Role/function orientation — missing from the proposed axes (significant)**

The support_healer is the clearest case: it shares all four proposed axes with what would be a fire mage variant, yet its entire functional identity is different. The earth casters (root-heavy controllers) demonstrate the same gap in a subtler form: class_0003 and class_0008 are dimensionally identical under the four axes, but class_0008's 3-of-6 root abilities make it a controller, not a caster. A fifth axis — **role orientation: damage / sustain / control / hybrid** — appears necessary for the framework to be complete.

**4. Dimensional duplicates — current generation produces two of each type (structural)**

Season_000042 contains two fire mages, two water mages, two earth casters, two wind casters, two physical warriors. Under the proposed axes, each pair has identical dimensional profiles. This is expected from the current generation structure (two instances of each archetype per season), but it is incompatible with the trial-room mechanic where the player chooses among visibly distinct combatants. Under dimensional generation with a diversity constraint, no two classes in the same season should share a complete dimensional profile.

---

### Evidence for the dimensional generation approach

**Strong evidence for:**

1. The four axes cleanly describe 4/11 classes (fire and water mages) with zero friction. The concept is structurally valid for the cases it currently fits.

2. The physical warrior's failures trace directly to absent dimensional specificity. The mana economy bug exists because no energy type was specified at generation time, so the generator assigned mana by default. The projectile-geometry warrior exists because no range profile was specified, so the grammar used the available pool without constraint. These are not bugs in the implementation — they are the consequence of the dimension not existing. Dimensional generation would make them impossible.

3. The stat axis (armor weight) maps onto all 11 classes without ambiguity. When a dimension is actually implemented (as stats currently are), the mapping is clean and unforced.

4. The archetype label is already emergent, not an input. The engine is structurally pre-positioned for dimensional generation — the heavy lifting of making element a primary generation input is already done.

**Evidence for caution / additions:**

1. A fifth axis (role orientation: damage/sustain/control) appears necessary. The four-axis framework is incomplete without it. This adds scope to Option C — the generator's validity rules need to handle 5D combinations.

2. Range profile requires building melee geometry before it can be meaningful as a generation dimension. It cannot be retro-fitted onto existing geometry types.

3. Energy type requires building rage (and possibly combo, focus) mechanics before physical and other non-mana archetypes have correct dimensional assignments. The mana axis is already functional for elemental casters.

4. Ailment identity (burn/chill/root/knockback/bleed) is sub-dimensional within each element. It doesn't require a new axis but is part of what makes each element's identity distinct. It should be first-class in the generation spec even if not a primary axis.

---

### Implications for the A/B/C decision

These observations do not make the decision. They are evidence.

**Option C (full dimensional refactor):**
- The four proposed axes are directionally correct but incomplete by one dimension (role orientation).
- Implementation must include: rage mechanics (or equivalent non-mana physical resource), melee geometry type, and a role orientation dimension alongside the four proposed.
- The 2–3 week estimate may be optimistic given these additions, especially melee geometry and rage mechanics being net-new systems.
- The decomposition confirms that Option C addresses the root causes of both the mana economy bug and the warrior geometry problem — these are dimensional absences, not implementation bugs. Patching them tactically (Option A) would address symptoms; Option C addresses why the symptoms are possible.

**Option B (energy types within current architecture):**
- Adding per-archetype energy types would address the physical warrior's mana issue.
- Melee geometry would still not exist — warrior range profile stays wrong.
- Duplicate dimensional profiles (two fire mages, two water mages) would persist.
- Role orientation gap persists regardless of option.
- The five-axis concern is deferred but not resolved.

**Option A (tactical fix only):**
- Addresses convergence failure rate; doesn't address dimensional completeness.
- Class quality measurement (Cluster 2) would operate without a framework capable of expressing what makes two classes dimensionally distinct.
- All four friction points persist.

---

## DB Telemetry Gaps Identified

None of these gaps blocked the decomposition. All are relevant for future analysis work.

| Gap | Impact | Recommended action |
|-----|--------|--------------------|
| `base_mana` / `base_stamina` not written to DB | Can't query mana pool size directly; must re-derive from stat formulas | ~3 lines in `recorder._insert_classes` — fix independently of dimensional work |
| No `energy_type` field in schema | Can't track energy type until dimensional generation exists | Add field when dimensional generation lands |
| No `range_profile` field in schema | Same; requires melee geometry to land first | Add field when dimensional generation lands |
| No `armor_weight` field in schema | Inferrable at query time from stats, but not stored | Low priority — can derive on demand |
| `stamina_cost_pct` always null in abilities | No stamina resource exists yet | Add when stamina-as-resource is implemented |

**The one gap worth fixing in its own small scope:** `base_mana` and `base_stamina` are computed by the math model during generation but never stored. The schema columns exist in `classes`; `_insert_classes` in the recorder simply doesn't populate them. This would make mana sustainability analysis (particularly for Priority 11 investigation) queryable directly from the DB rather than requiring re-derivation. Estimated: three lines.

---

*Report written 2026-05-08. Data source: season_000042 from `data/telemetry.db` and `seasons/season_000042/`. Engine source files read but not modified.*
