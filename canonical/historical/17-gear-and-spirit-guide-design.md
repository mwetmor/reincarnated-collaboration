# Gear System and Spirit Guide Architecture — Design

> **STATUS:** HISTORICAL-INFORMATIVE (pre-Epoch-4; consult for lineage only — not current truth) — see `canonical/00-ground-state.md` for current truth

**Last updated:** 2026-05-09 base + 2026-05-12 supersession notes (see "Updates 2026-05-11/12" section immediately below)

## Status

Design conversation 2026-05-08 / 2026-05-09 between project owner and Claude session, after Phase 3 of the dimensional refactor merged. Captured here as design intent for the Priority 02 (gear) implementation. **Priority 02 is now B5 + B12 + B15 in current naming** (file 28 queue); ships across Stages A2 (B12) and A4 (B5 + B15) per file 16 restructure 2026-05-12.

This document supersedes the gear-related framing in `engine-repo/test-plans/priority-02-gear-status.md`, which was a Phase 0-era plan that didn't yet have the dimensional refactor's findings or the Spirit Guide pillar in scope.

---

## Updates 2026-05-11/12 — locks layered on top of original design

The 2026-05-08/09 base of this doc captures the gear system in pre-progression-design form. Substantial additions were locked through 2026-05-11/12 via file 32 (progression-design Section 5) and file 33 (progression-skeleton). The below summarizes what's NEW beyond this doc's base content — refer to canonical sources for full detail:

### Final gear slot list (LOCKED 2026-05-11; B12) — 10 slots

The base doc lists "weapon / off-hand / armor / accessory" with armor split into helmet/chest/hood/robe. The locked final list is 10 slots:

1. Main hand weapon (1H or 2H per handedness)
2. Off-hand (shield / orb / focus / off-hand-weapon / grimoire — 1H weapons only)
3. Head (helmet for heavy archetypes; hood for caster archetypes)
4. Chest (chest for heavy; robe for caster)
5. **Hands (gloves)** — NEW per B12
6. **Feet (boots)** — NEW per B12; primary movement speed source
7. **Belt** — NEW per B12
8. Ring 1
9. Ring 2 (matches D3/D4/PoE; 2 ring slots)
10. Amulet

Canonical reference: `33-progression-skeleton.md` § "Gear slots."

### Movement speed primary affix on boots (LOCKED 2026-05-11; B12)

- Boots primary affix = +% movement speed
- NOT stat-driven (no stat affects base movement speed)
- Hard cap +25% from gear total
- Engine emits `movement_speed` per class + monster tier

Canonical reference: file 28 § B12; file 33 § "Movement and mobility."

### Resistance affix system (LOCKED 2026-05-11; gear constraint added per Section 11 closures)

Within-season +75% all-element resistance cap reached via:
- Trial body-swap path: +10% per Trial × 3 acts = +30% from milestones
- Gear: must support **~+45% all-element resistances across the equipment loadout**

This is a NEW constraint on gear generation. Implementation: per-piece resistance affixes summing to ~+45% across a full loadout. Likely per-piece values: chest +8-12%, helmet/head +5-8%, gloves/boots/belt/rings/amulet each contributing element-specific or smaller all-resistance rolls. Matches PoE per-piece resistance pattern.

No cross-season resistance accumulation — each season starts at +0% baseline; form library carries class identity only, not stat state.

Canonical reference: file 32 § Section 11 Q3 lock; file 33 § "Global resistance system."

### Seasonal Sets ⭐ (LOCKED 2026-05-11; NEW B15 queue item)

**The "Set bonuses / armor sets — could fit later as a special trait category; not in initial scope" framing at line 622 of this doc is SUPERSEDED.** Seasonal Sets are now in scope and ship in Stage A4 alongside B5 legendary mechanical novelty.

Highlights:
- **One unique set per playable class per season** (5-6 sets per season)
- Sets are class-specific (only fit one class's archetype + stat requirements)
- Set pieces drop ONLY at L50 endgame (Act 3)
- Set pieces are individually rare (legendary-tier or above)
- Set bonuses at 2-piece / 4-piece / full-set thresholds
- "Real seasonal goal: gather your favorite class's weekly seasonal set"
- Form library trophy value: set-wearing ascended spirits = visible accomplishment + Earth meta-layer event power

Canonical reference: file 28 § B15; file 32 § Section 5 Q5.8; file 33 § "Seasonal Sets."

### Per-band drop rates + ilvl as separate axis (LOCKED 2026-05-11; Section 5 Q5.1, Q5.4)

**Monster-level-tied drop rates per band:**

| Band | common | uncommon | rare | epic | legendary |
|---|---|---|---|---|---|
| A1 (L1-17) | 70% | 25% | 4% | 0.9% | 0.1% |
| A2 (L18-33) | 50% | 30% | 15% | 4% | 1% |
| A3 (L34-50) | 30% | 30% | 25% | 12% | 3% |

**`*_DROPS_PER_SLOT` per band:** L17 = 10; L33 = 25; L50 = 50 (existing endgame baseline). Replaces this doc's single endgame-only `END_GAME_DROPS_PER_SLOT = 50` framing — the multi-band approach (B14) requires per-band drop budgets.

**ilvl as separate axis** (PoE/LE pattern): gear stamps with ilvl at drop time; affix-tier gating on ilvl; equip = stat_thresholds + character_level ≥ ilvl - 3. Cross-season smuggled gear retains ilvl forever.

Canonical reference: file 32 § Section 5; file 33 § "Tier-availability + drop curves."

### Legendary mechanical novelty (LOCKED 2026-05-10; B5)

- `granted_ability` on weapons → 7th hotbar slot (not replace-existing)
- `aura` on armor/shield/accessory → passive tick
- `on_hit` on weapons → chance proc
- `cast_on_attack` → deterministic Nth-attack trigger
- All legendaries grant abilities (variable richness — some procs, some full skills)

Canonical reference: file 28 § B5.

### Auto-pickup with rarity filter (LOCKED 2026-05-11; Section 5 Q5.9 / mobile-first solution)

- Common/uncommon: auto-pickup → auto-convert to gold
- Rare+: auto-pickup → inventory; Spirit Guide marginal-value review at room/encounter end
- Pet system parked as design intent (see `project_pet_system.md` memory file)

Canonical reference: file 32 § Section 5 Q5.9.

---

### Heal-cooldown affix family — retires potion-interaction affixes (LOCKED 2026-05-17)

**Source:** gandalf DoE feel-target doc `canonical/story/mobile-feel-target-doe-2026-05-17.md` (§§ 5.4, 7.2); Matt L3 lock 2026-05-17 evening — Path A doc-cascade dispatch (`agentic_orchestration/dispatches/2026-05-17-gandalf-doe-doc-cascade-path-a-portrait-primary.md`).

The healing mechanic is now a cooldown-gated ability rather than an inventory-stack of potions (per canonical-32 § 13.1). Gear affixes that previously would have interacted with the potion-inventory mechanic are retired; a new affix family targets the cooldown ability.

**Retired affixes (do not generate):**

- `+1 potion slot` / `+N max potion stack`
- `+X% potion drop rate`
- `+X% potion magnitude` (the inventoried-potion variant)
- `+X potions granted on kill / on level-up`
- Any affix premised on multiple potion types (greater/lesser/health/mana inventory) — Reincarnated has one heal, one cooldown; the affix surface follows.

**Note:** the *mana / energy* resource model survives unchanged (see canonical-32 § 13.1). Affixes that modify mana regeneration, mana max, energy cost reduction, and resource-substrate interactions are NOT retired; they are independent of the heal mechanic.

**New affix family — `heal_*` affixes (eligible on all gear slots; tier-gated per existing affix budget):**

| Affix | Range (rough; rocket calibrates at gen time) | Tier eligibility | Notes |
|---|---|---|---|
| `heal_cooldown_reduction` | `-0.5s` to `-3.0s` flat reduction | Magic+ (uncommon roll); Rare+ (stronger rolls) | Subtracts from the 10.0s baseline (per canonical-32 § 13.1). Floor at ~5s effective cooldown via stacking cap. |
| `heal_cooldown_reduction_pct` | `-5%` to `-15%` percentage | Rare+ | Multiplicative reduction; stacks additively with flat reduction. |
| `heal_magnitude_bonus_pct` | `+5%` to `+30%` | Magic+ | Increases the `heal_magnitude_pct_max_hp` baseline (35% → up to 45.5% per cast at max roll). |
| `heal_magnitude_bonus_flat_hp` | `+10 HP` to `+100 HP` | Magic+ | Adds to the `heal_floor_hp_flat` (50 HP baseline → up to 150 HP). Most useful early-game where % is small. |
| `heal_secondary_effect` (enum) | one of: `brief_invuln_1s` / `brief_invuln_2s` / `cleanse_1_debuff` / `mana_refund_25pct` / `cleanse_all_dots` | Epic+ (legendary-tier in some cases) | Rarer "mechanical novelty" tier per existing legendary-mechanic system (file 17 § "Legendary mechanical novelty"). One per item; stacks across items capped at 2 total active. |

**Stacking caps (preserves balance against runaway-CDR builds):**

- Total flat CDR floor: `heal_cooldown_seconds` cannot drop below **5.0s** (50% of baseline).
- Total magnitude bonus: `heal_magnitude_pct_max_hp` cannot exceed **60%** of max HP (baseline 35% + cap 25 percentage-points of bonuses).
- `heal_secondary_effect` cap: 2 concurrent (e.g., `brief_invuln_1s` + `cleanse_1_debuff` is permitted; three is not).

**CC interaction — heals BLOCKED during stun / freeze / silence (LOCKED 2026-05-17; Matt L3 verdict #121):**

Heal-affix-triggered heals (and the heal ability proper) are **BLOCKED during stun / freeze / silence states**. The heal is **suppressed** — not queued, not partial, not delayed. The cooldown does not advance during the CC window. When the CC ends, the heal becomes available on its normal cooldown timer: if the affix or ability was off-cooldown when CC was applied, it remains off-cooldown when CC ends.

This applies to all `heal_*` affix resolutions, including `heal_secondary_effect` variants — if the primary heal is CC-suppressed, no secondary effect fires either (the heal never resolves; there is nothing to trigger a secondary from).

The CC gate is defined as: actor has one or more of `{ stun, freeze, silence }` in its active ailment set, or any future CC ailment whose design spec satisfies "actor cannot take voluntary action." Ailments that do not satisfy that definition (e.g., a slow that only reduces movement speed) do not block heal and must be explicitly noted as non-blocking in their individual design specs.

Cross-reference: `reincarnated-engine/design/decisions/decisions-log.md` entry "2026-05-17: Heal blocked by CC ailments — #121 verdict"; `canonical/32-progression-design.md` § 13.1 CC-gate clause.

**Affix-coherence interaction (per existing § "Affix coherence" filter):**

- `heal_*` affixes are **role-orientation-agnostic** — heal is a universal survival floor, not a class-flavor mechanic. All classes benefit equally; no archetype gating.
- `heal_*` affixes can roll on **any gear slot** (no slot bias). This is intentional: heal-CDR is a build-defining choice; players who prioritize survival can stack it across slots; players who prioritize damage will see CDR rolls as decisively replaceable.
- `heal_secondary_effect` is **gated to high-tier gear** (epic+) consistent with the legendary-mechanic-tier pattern (existing § "Legendary mechanical novelty"); these are the affixes that make a piece feel build-defining.

**Spirit Guide interaction:**

- Spirit Guide's marginal-value math treats heal-CDR and heal-magnitude affixes as standard contributors to `power_score` (calibrated as defensive expected-value contributions).
- Spirit Guide does NOT bias recommendations toward heal-affixes for struggling classes (per § "Why this avoids the patronizing adaptive difficulty trap"). If heal-CDR gear happens to help a struggling form more (because that form takes more damage, so heal-frequency matters more), that is the same emergent equalization mechanic operating; no per-affix tuning.
- `heal_secondary_effect = "brief_invuln_*"` produces interesting Guide-recommendation dynamics for fragile classes (the invuln-window has high marginal value when the player dies frequently); these emerge as natural recommendations without special-casing.

**Cross-references:**

- `canonical/32-progression-design.md` § 13.1 (canonical heal-mechanic definition)
- `canonical/story/mobile-feel-target-doe-2026-05-17.md` § 7.2 (decision provenance)
- `agentic_orchestration/dispatches/2026-05-17-gandalf-doe-doc-cascade-path-a-portrait-primary.md` (this dispatch)
- File 17 § "Affix coherence — affix pool filtered by dimensional fit + stat affinity" (existing affix-filter rules apply unchanged)
- File 17 § "Legendary mechanical novelty" (the `heal_secondary_effect` family rides this existing tier-gating infrastructure)

**Engine-side execution (deferred to VS2b; informational here):**

- `rocket`: update gear-affix generation to emit `heal_cooldown_reduction` / `heal_magnitude_bonus_*` / `heal_secondary_effect` per the table above; retire potion-interaction affix generation pathways.
- `star-lord`: telemetry update — emit per-heal-cast event records (timestamp, cooldown-at-cast, magnitude-resolved, secondary-effect-triggered) to support D11-style empirical balance analysis on the heal surface.
- `gamora`: re-run convergence with the new affix family included to verify that heal-CDR stacking doesn't break per-class win-rate distributions outside their convergence band.
- **Gate-1 advisory flag:** this is a load-bearing canon change to the gear-affix pool. jack-ryan Gate-1 advisory gates the VS2b rocket implementation per the discipline-#12 semantic-shift pattern (heal-affix family is a new affix taxonomy entrant).

---

## Priority naming → current (Stage A) naming

The base doc below uses the older "Priority 02 / Priority 13 / Priority 14 / Priority 15" naming. Translation for cross-reading:

| Old | Current |
|---|---|
| Priority 02 (gear) | B5 (legendary novelty) + B12 (movement speed + slot audit) + B15 (Seasonal Sets) |
| Priority 13 (encounter quality + monster tier infrastructure) | B10 (gauntlet restructure + native swarm tier) |
| Priority 14 (Traits-and-Skills progression) | B9 series (B9a/b/c — endgame math; Stage A3) + Stage A7 (player-facing progression scaffold; design fully resolved in file 32 + file 33) |
| Priority 15 (Loot Economy Validation) | No formal B-letter yet; needs scoping when ready |

---

## Original design content (2026-05-08/09)

## Why this exists

Three converging design questions raised by Priority 02 needed an integrated answer:

1. **How should gear contribute mechanically?** Stats only, or stats + ability modifiers + traits + granted abilities? (Tier gradient question.)
2. **How does gear avoid amplifying class imbalance?** Standard ARPG gear amplifies meta builds. The project's design intent is the inverse — gear should buff weak classes and not compound dominant ones. (Balance equalizer question.)
3. **How does the Spirit Guide know when to recommend gear swaps?** ("Auto-detour" mechanism: "you just looted better gear; auto-equipping in 5...4...3...")

The answers turn out to be deeply unified: a single mechanism (Spirit Guide marginal-value analysis) provides the equalization, the swap recommendations, and the player attention management. The gear architecture flows from this unification.

## The unified mechanism

**Gear generates universally.** Not class-aware. Not weak-class-favored. Drops follow the same generation rules regardless of whose form the player is currently inhabiting.

**Each gear instance has two deterministic properties** computed at generation time:

- `power_score` — a normalized number representing the gear's mechanical contribution (stat budget + ability-modifier expected value + trait expected value, weighted by tier).
- `class_fit_profile` — a **5-axis** vector of dimensional fit weights matching the dimensional generation: `energy_type`, `range_profile`, `armor_weight`, `damage_type`, `role_orientation`. Each coefficient is between 0.0 and 1.0. A bow has high fit for `range_profile=long` + `energy_focus`, near-zero for caster archetypes.

The fit profile is **deterministic — computed by the engine** from the gear's mechanical content (which stats it modifies, which abilities it enhances, which dimensional axes its effects target). The LLM does not propose fit weights; the LLM only proposes flavor (name, description, visual prompt). Same pattern as everywhere else in the project: LLM as creative proposer, engine as deterministic validator.

**The Spirit Guide does marginal-value analysis** to recommend swaps:

```
marginal_value = (new_gear.power_score × new_gear.fit_for_current_class)
               - (current_gear.power_score × current_gear.fit_for_current_class)
```

**Recommendation threshold is a single absolute marginal-value floor.** A meaningful improvement crosses the threshold; a marginal one doesn't. The threshold is calibrated to "noticeable to the player" — *not* tuned per class state. There is no hidden per-class bias.

### Why this is force-multiplying

The single mechanism produces three behaviors simultaneously:

1. **Swap recommendations** — meaningful gear improvements cross threshold; the Guide surfaces them.
2. **Equalization** — emerges naturally as a *consequence* of marginal-value math: strong classes have low headroom (their balance modifier already throttles them), so most drops produce small marginal values that don't cross threshold. Weak classes have high headroom, so the same drops produce large marginal values that do cross threshold. The Guide ends up effectively recommending more gear to weak classes — but only because the math says those drops genuinely help more.
3. **Attention management** — emerges as another consequence: dominant classes get silence (few drops cross threshold), struggling classes get help (many drops cross threshold). The Guide is more helpful when you need help, but never patronizingly so.

All three flow from the same calculation. The tuning surface collapses to one parameter (the absolute threshold). When the absolute threshold is calibrated to "noticeable improvement," all three behaviors emerge correctly without per-goal tuning.

### Three goals, one mechanism — explicit metrics

Even though the implementation is unified, the goals are conceptually separate. Stating each explicitly with a measurable success criterion makes tuning trade-offs visible:

| Goal | Success criterion (measurable) |
|---|---|
| **Swap recommendations** | A proposed swap, if accepted, increases the player's class effective power by ≥ X% (where X is the threshold value). |
| **Equalization** | Across many drops, weak-form drops produce more above-threshold recommendations than strong-form drops, *without any class-state-dependent threshold tuning*. The asymmetry is empirical, not enforced. |
| **Attention management** | Subjective: "the Guide speaks when I need help." Measurable proxy: recommendation frequency correlates inversely with class modifier without a programmed bias. |

If during playtest one of these feels off, the tuning question becomes: is the absolute threshold too low (Guide nags everyone) or too high (Guide is silent always)? That's one parameter, not three.

### Why this avoids the "patronizing adaptive difficulty" trap

The equalization is *not* "make gear weaker for strong classes" or "lower the recommendation threshold for weak classes." Gear drops are class-agnostic. The threshold is class-agnostic. What differs is the *marginal value of the same drop* across different forms — and that's just math.

A savvy ARPG player attempting to reverse-engineer the system finds: "the Guide recommends gear when it would meaningfully improve my current loadout for my current form." That's an honest description of what's happening. There's no hidden per-class bias to discover; the system does what it says.

### Gear balance is calibrated against average gear, not max gear

A subtle but consequential design choice: when the convergence loop tunes class balance, it does so against **scenario-appropriate average gear**, not maximum-possible gear.

- Players running with average drops produce the convergence baseline (~50% win rate at scenario tier).
- Players who min-max above-average gear *feel* stronger than baseline — they're "breaking the meta" relative to where balance assumes they are.
- Players who run with below-average gear feel weaker, but the gap from baseline is bounded by how far below average they go.

This produces the "break the meta" player experience as a structural property of how balance is calibrated. Min-maxers are rewarded for outperforming the baseline; the baseline assumes typical play. In a high-drop-volume game, this matters a lot — players will accumulate well-fitting gear by sheer drop count, and the balance system shouldn't punish them for that accumulation.

**Practical implication for the convergence loop:** the convergence loop calibrates against the **end-game equipped distribution**, not the per-drop distribution. These are different in a load-bearing way (CP6c finding):

- **Per-drop rate** (~80% common, ~15% uncommon, ~4% rare, ~0.8% epic, ~0.2% legendary) is what a single fresh drop produces.
- **Equipped distribution** is what an end-game player actually wears: the *best of their accumulated drops per slot*. After dozens of drops in a given slot, the best is far more likely to be high tier than any single drop is.

The model: for each gear slot, draw `END_GAME_DROPS_PER_SLOT` candidates from the eligible pool at per-drop rates, then equip the highest-tier candidate (tie-break by `power_score` within tier). The default `END_GAME_DROPS_PER_SLOT = 50` represents a "modest end-game player" with ~1–2 weeks of post-leveling play.

Equipped distribution at N=50:

| Best tier in slot | Probability | (vs. per-drop) |
|---|---|---|
| Legendary | ~9.5% | (vs. 0.2%) |
| Epic+ | ~39.5% | (vs. 1.0%) |
| Rare+ | ~92.3% | (vs. 5.0%) |
| Common-only | <1% | (vs. 80%) |

The order-of-magnitude difference between per-drop and equipped distributions is why the convergence loop must use the equipped form. Calibrating against the per-drop distribution biases monsters too easy and classes too low-modifier (because the loop is calibrating against a sub-realistic player baseline).

Both player and monster sides participate in the convergence calibration, but the implementation is **asymmetric** (clarified by the pre-CP7 status check 2026-05-10):

- **Player side** carries a sampled best-of-N gear loadout per fight (`sample_scenario_loadout(catalog, class_stats, rng, n_drops=END_GAME_DROPS_PER_SLOT)`)
- **Monster side** has no gear; `from_monster()` and `from_trial()` construct combatants from raw schema stats. `bonus_damage_flat = 0.0` always for monsters.
- **Calibration absorbs the asymmetry** via the search:
  - Per-class `damage_modifier` is binary-searched to produce 50% win rate against the gauntlet (gauntlet monsters have no monster-side modifier; their stats are fixed at generation)
  - Per-trial-boss `damage_modifier` is binary-searched separately to produce ~50% defeat rate across all player classes (trial bosses have an explicit modifier tuning lever)

This asymmetry is correct under the current scope but is a known design consequence — modifier values are calibrated against the *specific* player gear baseline. Any change to player gear (e.g., shifting `END_GAME_DROPS_PER_SLOT`) re-runs convergence and re-derives modifiers. The same would be true if monsters were ever to gain explicit gear; that's deferred to Priority 13 work (encounter quality + monster system depth).

Monster tier infrastructure exists (`TIER_EFFECTIVE_ATTRIBUTE` with standard/elite tiers, tier-parameterized stat ranges) but a richer tier hierarchy (trash/standard/elite/champion/boss) and explicit per-tier balance levers are Priority 13 territory, not Priority 02.

**The "scenario" parameter scales with progression scope.** Currently end-game only (per the dimensional refactor's scope), so all classes calibrate against N=50 equipped distributions. When Priority 14 (Traits-and-Skills progression) lands and introduces early-game and mid-game balance gauntlets, those scenarios use lower N values reflecting accumulated drops to that point — `END_GAME_DROPS_PER_SLOT` becomes one entry in a tier of `*_DROPS_PER_SLOT` constants per progression phase.

Min-maxers who play significantly longer than the calibration window (effective N higher than 50) feel like they "break the meta" because their equipped distribution exceeds the baseline. Players who haven't reached the calibration window feel slightly under-tuned. The "feel of breaking the meta" is the structural property; calibration assumes typical play.

## Class `damage_modifier` — why the convergence-tuned scalar stays exposed

The per-class `damage_modifier` is convergence-tuned (binary search to ~50% win rate against the gauntlet) and applied at fight resolution as a multiplier on class damage output. A reasonable question raised during Priority 02 design: now that gear, traits, and abilities together shape class output, why isn't the modifier "baked in" to per-ability coefficients at generation time, removing the runtime scalar?

**Answer: the scalar protects per-ability variance, which is core to the seasonal journey.** It's a structural enabler of design intent at a different layer — not just a diagnostic readout.

### Per-ability variance is intentional

Abilities within a class aren't supposed to be flat across a class. Some are strong, some weak, some niche, some build-defining. That variance is what makes ability acquisition meaningful — finding a tier-3 ability that synergizes with your class's profile is satisfying *because* tier-1 and tier-3 abilities feel different. Flattening that distribution erases exactly the texture that makes the seasonal journey rewarding.

The LLM-naming layer compounds this: abilities have flavor and archetypal weight. A "Devastating Strike" should *feel* devastating, and its coefficient should match the name. If the math drifts from the flavor, players see numbers that don't match what they read, and the experience breaks.

### Why per-ability tuning would flatten the distribution

If the convergence loop tuned per-ability coefficients individually (instead of the class-level scalar), the optimization-correct answer is to push everything toward the mean. The loop only sees aggregate win rate; variance from the mean adds noise to the convergence signal without improving the target. So the loop would push individual abilities toward parity — flattening the distribution.

The class-level scalar prevents this by absorbing aggregate equalization at the *class* level. It says: "across the distribution of abilities this class will encounter, the average power level needs this correction to hit 50% win rate." It shifts the whole distribution as a unit. Internal variance survives intact — just shifted up or down uniformly.

So strong abilities stay strong, weak ones stay weak, build-defining tiers retain their identity, and the class scalar shifts the shape to land at the convergence target. The journey of acquiring better abilities, hitting build-defining tiers, finding synergies — all of that depends on the distribution having shape, and the scalar is what lets the shape exist without breaking convergence.

### The narrow valid case for an export-time flattening transform

There IS a defensible case for producing per-ability coefficients with the scalar baked in: **downstream developer / modder / licensee audiences.** Engineers trained by Diablo, PoE, Last Epoch, etc., expect balance to live at the ability level. A class scalar reads as foreign; they'd either misuse it (treating it as a difficulty knob, breaking convergence) or work around it (tuning abilities anyway, double-counting the correction).

For those audiences, an **export-time flattening transform** — separate from the convergence loop — produces the expected hand-tunable surface without compromising the convergence-native view. The convergence loop keeps the scalar exposed internally and continues to operate on it; a downstream export step multiplies the scalar through into each ability's magnitude, producing a flattened artifact for human tuners.

This is meaningfully different from "remove the scalar." It's **two views of the same data**:
- **Convergence-native view** with `damage_modifier` exposed — what the engine uses internally; preserves diagnostic value, ability-variance protection, and re-tunability
- **Flattened export view** with the scalar pre-multiplied into per-ability coefficients — what downstream tuners expect; produced as a snapshot at season export time

The runtime can use either; the convergence loop only operates on the first; humans tune the second.

### Decision: deferred until the downstream audience question is settled

If this is a closed system shipped by the project owner alone, the scalar's internal-only existence is correct and complete. The convergence loop benefits from the diagnostic value; class identity benefits from the ability-variance protection.

If engine licensing, mod support, or contractor handoff becomes real, the export view becomes near-essential. Without it, every downstream tuner reinvents the same mental model conversion, badly.

**Middle path (recommended):** don't build the export view now, but document the flattening recipe (multiply class `damage_modifier` through into each ability's magnitude in a season-snapshot transform) so a future developer could build it in an afternoon if the audience materializes. The math is trivial; the value is in knowing it's safe to do without breaking anything.

The downstream-developer question doesn't need to be answered now. Capturing the reasoning here means future sessions don't have to re-derive it.

## Gear architecture

### Universal generation properties

Every gear instance has:

- **Slot type** — weapon, off-hand, armor, accessory (initial set; can expand later).
- **Base type** — a specific item subtype within the slot. The initial roster:
  - **weapon** (1H) — sword, dagger, hammer, **wand**
  - **weapon** (2H) — staff, bow, **greatsword**
  - **off-hand** — shield, off-hand-weapon (dagger / sword for dual-wield), grimoire, orb, focus
  - **armor (heavy / medium)** — helmet, chest
  - **armor (light)** — hood, robe (added in CP5b — caster archetypes need an equippable armor option; the heavy / medium variants gate on STR or DEX which casters can't satisfy)
  - **accessory** — ring, amulet
- **Handedness** (weapons only) — `1h` or `2h`. Determines whether the off-hand slot is equippable (see "Handedness and off-hand mechanics" section below).
- **Tier** — common / uncommon / rare / epic / legendary.
- **`power_score`** — universal numeric magnitude.
- **`class_fit_profile`** — dimensional fit vector.
- **`stat_requirements`** — per-base-type equip thresholds (STR / DEX / INT / WIS floors). Auto-calibrated from the season's actual stat distributions. See "Equip-time stat thresholds" section below.
- **Mechanical content** — stats, ability modifiers, traits, granted abilities (depending on tier — see gradient below).
- **Element flavor** — for theming; tied to canonical_element values.
- **`visual_prompt`** (optional, populated for rare+) — LLM-generated description specifically for visual generation; consumed by Meshy / Unity downstream.

### Handedness and off-hand mechanics

Weapons have a `handedness` attribute: `1h` or `2h`. This determines off-hand slot availability:

- **2H weapon equipped:** off-hand slot is unused (the weapon implicitly occupies both hands).
- **1H weapon equipped:** off-hand slot is available for an off-hand item.

**Stat budget rule:** the total weapon-side stat budget is roughly equivalent across configurations. A 2H weapon carries the full budget in one piece; a 1H weapon + off-hand carries the same total split across two pieces. The trade is:

- **2H gear:** higher per-piece stat magnitude; fewer slot decisions; coarser customization.
- **1H + off-hand:** lower per-piece magnitude; more granular customization; two `class_fit_profile` matches instead of one.

This produces meaningful build choices without inflating gear's mechanical surface — the *total* power is held constant; what varies is *how it's distributed*.

### Off-hand base types and dimensional fit

Three off-hand base types in the initial roster, each with a clear archetype lean:

| Base type | Primary use | Class fit lean |
|---|---|---|
| **Shield** | Defensive — introduces block mechanic (see below) | High fit for control orientation, physical_warrior, physical_grappler, hybrid |
| **Off-hand weapon** (dagger / sword) | Offensive dual-wield | High fit for combo (rogue), some skirmishers |
| **Grimoire / orb / focus** | Caster amplifier | High fit for mana-using elemental classes (mages, casters, controllers) |

The `class_fit_profile` mechanism handles cross-fit naturally — a shield in a fire_mage's off-hand has low caster-fit but valid block, so the Spirit Guide might still recommend it for survivability in specific scenarios. The dimensional fit weights guide recommendations without forbidding equipment.

### Block mechanic (new combat-sim feature)

Shields introduce a defensive mechanic the engine doesn't have today. Two stats per shield:

- `block_chance: float` — probability per incoming hit that the shield activates
- `block_value: float` — damage reduction when block activates (proportion or flat magnitude — implementation detail to be settled in CP3)

When an attack resolves, the damage resolver checks for block before applying damage. Block is the canonical *control-class survivability tool* — control archetypes (physical_grappler, the `*_controller` variants) take hits while CCing; the shield mechanic is how the engine expresses that durability.

Combat-sim impact: two new fields on `CombatantState` (`block_chance`, `block_value`, derived from equipped shield) and one check in damage resolution. Roughly half a day of sim work; small but real.

### Why bow, wand, and greatsword are all in the initial weapon set

Three specific cases where the initial weapon/off-hand roster must extend beyond the obvious "sword + staff + dagger + hammer" minimum:

- **Bow** is the dimensionally-coherent weapon for the **hunter** archetype (focus + physical + long-range), an actively generated class today (Phase 3). Without bow, hunters have no weapon-slot option that fits their dimensional profile.
- **Wand** is the dimensionally-coherent **1H caster weapon** required to pair with caster off-hands (grimoire / orb / focus). Without wand, casters who want an off-hand are forced to either a sword/dagger off-hand (low caster-fit) or an empty off-hand slot. Adding grimoire to the off-hand roster therefore *requires* wand in the weapon roster — they're a complementary pair.
- **Greatsword** (2H sword) is added so every active archetype has at least one 2H weapon option. Without it, physical close-range classes (warrior / grappler / skirmisher) would be 1H-only at the dimensionally-coherent level — they could *equip* staff or bow but the fit would be poor. Greatsword closes that gap and lets the sim observe whether 2H usage becomes a meta-bias trend (visible in convergence data: classes consistently equipping 2H produce different modifier distributions than classes preferring 1H + off-hand). If a trend emerges, balance can be tuned at the level that matters (stat budgets, off-hand value, etc.). Without greatsword we'd have no signal.

These are instances of a general rule: **when the dimensional generator produces an archetype, the initial gear roster must include at least one weapon (and off-hand, where applicable) that fits its dimensional profile, including coverage of both 1H-with-off-hand and 2H configurations where the archetype could plausibly use either.** Off-hand types follow the same rule — adding a caster off-hand (grimoire) requires a 1H caster weapon (wand) to pair with it.

**The "every archetype has a 2H option" rule:** all currently-generated archetypes can equip at least one 2H weapon with high dimensional fit. Casters → staff. Hunters → bow. Physical close-range → greatsword. Combo (rogue) is the partial exception — combo identity is dual-wield-leaning by ARPG convention, and a 2H combo build is unusual; combo can equip greatsword but with reduced fit. Acceptable for now; revisit if the sim shows combo classes converging poorly without a 2H option that fits their identity.

The deferred list is now narrower: maul (2H hammer variant); spear (medium-range physical); off-hand-only items beyond the initial three. Add these when concrete archetype gaps demand them.

### Equip-time stat thresholds (archetype-implicit gating)

Beyond the dimensional fit-profile mechanism (which drives Spirit Guide recommendations and affix coherence), gear carries **stat-threshold equip requirements** that act as hard gates on equipment eligibility. This addresses two failure modes of pure soft-recommendation:

1. **Convergence loop integrity.** The simulator has no Spirit Guide. Without hard gates, the gear-selection logic could equip mismatched gear (fire-caster-in-plate) based on raw `power_score × fit`, skewing balance data. A fire caster in heavy armor would diverge as a survivability outlier in the convergence loop without the player ever making the choice.
2. **Player override path.** Even with a perfect Guide, a player can stash-then-equip-anyway. For weapon and armor class identity (a fury warrior with a staff, a fire mage in plate), this should not be possible — these are visual lies, not meaningful build choices.

Stat thresholds are **per base type**, not derived from `class_fit_profile`. CP2's empirical finding (the "effects drive fit, not weapon label" pattern surfaced in the bow/sword fit table) confirms why: a fire-enchanted sword's fit profile leans long-range due to its on-crit fire effect, even though the sword itself is mechanically melee. Using `class_fit_profile` for equip eligibility would let casters equip elemental swords because the fit happens to match. Stat thresholds on base type avoid this contamination.

| Slot / base type | Stat requirement |
|---|---|
| Heavy armor (chest, helmet) | STR ≥ heavy_floor |
| Medium armor | STR ≥ medium_floor OR DEX ≥ medium_floor |
| Light armor (cloth / robe) | No requirement |
| 1H sword, hammer, dagger | STR ≥ melee_floor_1h |
| Greatsword (2H) | STR ≥ melee_floor_2h (higher than 1H) |
| Bow | DEX ≥ ranged_floor |
| Wand, staff, grimoire, orb, focus | No requirement |
| Shield | STR ≥ shield_floor |

**Threshold auto-calibration:** floors are computed per season from the actual stat distributions of generated classes, not hard-coded constants. Observed stat coalescence (per the engine's existing telemetry: STR-build classes allocate 145–165 STR; casters allocate 5–15) makes the math straightforward — a floor at ~60% of the typical primary-stat allocation bites comfortably without overtuning, and shifts automatically if a season generates classes with different stat magnitudes. No magic numbers to retune as generation evolves.

**Archetype-implicit gating:** the result is archetype-coherent equip behavior without a discrete archetype taxonomy. A class is "physical" if it allocates STR; that allocation gates it into heavy armor and STR weapons; class identity emerges from dimensional axes + stat allocation, not from an explicit archetype label. This preserves the dimensional refactor's architectural direction while giving players intelligible equip rules ("Requires STR 100" instead of an opaque dot-product threshold).

**Why stat thresholds and not `class_fit_profile` floors:**

| Mechanism | Intelligibility | Calibration | Future-proofness |
|---|---|---|---|
| Stat thresholds | "Requires STR 100" — clear | Auto from stat distributions | Stable; new dimensional combinations don't need new threshold types |
| `class_fit_profile` dot product | "Requires fit ≥ 0.6" — opaque | Magic number per slot | Sensitive to fit-computation drift (e.g., the effects-drive-fit pattern from CP2) |

The `class_fit_profile` mechanism still earns its keep at two layers where its strengths matter:

- **Spirit Guide marginal-value math** — continuous fit measure for ranking recommendations *above* the equip threshold. The two layers compose: stat thresholds gate eligibility; fit profile + power score rank within the eligible pool.
- **Affix coherence** — fine-grained sub-flavor (a fire mage's robe rolls fire affixes; an ice mage's rolls ice; both share INT-affinity but the dimensional vocabulary distinguishes them). See affix coherence section below.

### Affix coherence — affix pool filtered by dimensional fit + stat affinity

A real risk in Priority 02's affix system: without filtering, gear can roll incongruous affixes. A staff (caster weapon, mana-leaning, long-range) shouldn't roll `+15% melee_strike damage`. A hammer (physical close-range) shouldn't roll `+10% fire blast damage`. A heavy plate shouldn't roll `+10 INT`. A wand shouldn't roll `+10 STR`. Without these constraints, gear flavor breaks down — you end up with absurd combinations that confuse both the LLM (try writing a coherent name for "a wizard's staff that boosts physical melee") and players (reading their inventory).

The affix catalog uses **two complementary tag layers**, both checked when filtering the roll pool for a gear instance:

**Layer 1 — Dimensional tags** (same vocabulary as `class_fit_profile`; primary mechanism for ability/effect affixes):

| Affix example | Dimensional tags |
|---|---|
| `+15% melee_strike damage` | `range_profile=close`, `damage_type=physical` |
| `+10% fire damage` | `damage_type=fire` |
| `−10% mana cost` | `energy_type=mana` |
| `+1 multishot floor` | `range_profile=long`, geometry-tagged |
| `+5% block chance` | `role_orientation=control`, defensive-tagged |

**Layer 2 — Stat-affinity tags** (coarser; primary mechanism for stat-specific affixes):

| Affix example | Stat-affinity tag |
|---|---|
| `+10 STR` | `str_affinity` |
| `+10 INT` or `+10 WIS` | `int_wis_affinity` |
| `+10 DEX` | `dex_affinity` |
| `+5% all damage`, `+10 VIT` | `none` (universal) |

Stat-affinity ties affixes to the gear's stat-threshold profile (the equip-gating mechanism above). A heavy plate (STR threshold) won't roll `+10 INT`. A wand (no threshold, caster slot) won't roll `+10 STR`. The two layers together produce coherent affix pools — Layer 1 handles flavor coherence (no fire on a hammer), Layer 2 handles archetype coherence (no INT on plate).

**Affix-roll filter:** when generating gear, the affix-roll pool is filtered to affixes that satisfy both:

1. Stat-affinity matches the gear's stat-threshold archetype (or is `none` / universal), AND
2. Dimensional tags align with the gear's `class_fit_profile` (dot product threshold, e.g. ≥ 0.3 on the gear's high-fit dimensions).

Most affixes need only one layer's tags — dimensional for ability/effect affixes, stat-affinity for stat affixes. Compound affixes (e.g., `+5% physical damage and +5 STR`) carry both. The filter applies during the affix-roll step in gear generation.

The behavior at the gear-class level:

- Staff (caster, no stat threshold): excludes `+melee_strike damage` (Layer 1: range mismatch); excludes `+10 STR` (Layer 2: STR-affinity on a non-STR slot).
- Hammer (STR threshold, physical close-range): excludes `+fire damage` (Layer 1: element mismatch); excludes `+10 INT` (Layer 2: INT-affinity on STR slot).
- Bow (DEX threshold, physical long-range): excludes `−mana cost` (Layer 1: energy mismatch); excludes `+10 STR` (Layer 2: wrong stat-affinity for DEX slot).
- Shield (STR threshold, defensive): leans toward `+block chance`, `+block value`, `+armor`, control-flavored traits, plus STR-affinity.

The pattern reuses the existing `class_fit_profile` vocabulary for Layer 1 (no new dimensional concepts) and adds a small stat-affinity enum for Layer 2. The affix catalog needs each affix tagged on whichever layer applies.

**Implementation note (post-CP3, locked 2026-05-10):** the affix catalog is the existing `EffectPoolEntry` pool, extended with two optional fields rather than replaced by a parallel `AffixSpec` schema. This was investigated during CP3's lookahead window:

- `EffectPoolEntry` has 7 frozen Pydantic fields (id, effect_type, element, trigger, magnitude_range, compatible_slots, rarity_min). Adding `dimensional_tags: list[str] = []` and `stat_affinity: str | None = None` as optional fields is straightforward.
- The `_add()` helper in `build_effect_pool()` gains two kwargs.
- No DB migration needed — these are generation-time fields, not persisted to telemetry.
- The dual-layer filter (Layer 1 dimensional tags + Layer 2 stat-affinity) runs against the extended pool during the affix-roll sub-step in `generate_gear_item()`.

CP5c scope: extend `EffectPoolEntry`; tag the existing ~30–60 entries; implement the filter; verify against a sample of generated gear that obvious mismatches don't appear. Half a day to a day of work, no parallel infrastructure needed.

### Tier gradient

Different tiers contribute different shapes of mechanical value, and trigger different LLM treatment:

| Tier | Primary contribution | Naming approach | LLM cost |
|---|---|---|---|
| **Common** | Stats only (small budget) | Template — `"<Material> <SlotType>"` (Iron Sword) | None |
| **Uncommon** | Stats + small ability modifier | Template with affix prefix/suffix — `"<Adjective> <Material> <SlotType> of <Element>"` | None |
| **Rare** | Stats + larger ability modifier OR small trait | LLM-named (first tier where uniqueness matters) | One call per item |
| **Epic** | Stats + trait + ability modifier | LLM-named with richer flavor | One call per item with longer prompt |
| **Legendary** | Stats + trait + new ability OR major modifier | LLM-named with origin story / lore hook | One call with full creative brief |

The gradient is intentional: most gear drops are common/uncommon (template-named, cheap, mechanical-only). Rare+ gear is where uniqueness lives (LLM-named, deeper mechanical content, stronger flavor).

### LLM call frequency budget

For a typical season (estimating drops):

- Common gear: ~80% of drops, no LLM cost.
- Uncommon: ~15%, no LLM cost.
- Rare: ~4%, one LLM call each.
- Epic: ~0.8%, one LLM call each.
- Legendary: ~0.2%, one LLM call with richer prompt.

For a season generating ~500 gear items, that's ~25 LLM-named items (~5% of drops). Manageable cost. Common drops don't add LLM volume at all.

**Note:** the 500-drops-per-season figure is a ballpark estimate, not a committed budget. Actual ARPG drop rates can be much higher (per-player drop counts of 5,000+ over a season are not unusual). At 5,000 drops, the LLM-named tier produces ~250 calls per player per season — still manageable, but worth confirming against the actual drop rate during implementation. **The implementation should sanity-check this estimate** and adjust the percentages or thresholds if the LLM call volume exceeds budget.

This pattern matches how rare-uniqueness works in ARPGs: most gear is forgettable and templated; the rare drops you remember are the ones with names.

## Spirit Guide engine-layer API

The Spirit Guide as a player-facing entity (voice, UI, fade-in/fade-out, countdown timer) is far-future UI work. It is not built now.

But the **engine-level decision API** is built alongside gear. The Spirit Guide's reasoning is pure deterministic functions over engine state. The eventual UI just calls these functions and presents their results in the player-facing voice.

The API consists of (sketched, not final signature):

```python
class SpiritGuideAPI:
    def evaluate_gear_swap(
        self,
        current_loadout: Loadout,
        candidate_gear: GearInstance,
        class_state: ClassState,
    ) -> SwapRecommendation:
        """Compute marginal value and threshold; return recommendation."""

    def evaluate_class_health(
        self,
        class_state: ClassState,
        peer_classes: list[ClassState],
    ) -> ClassHealthSignal:
        """Is the player struggling unusually? (Used for class-abandonment recommendations.)"""

    def recommend_class_for_context(
        self,
        available_forms: list[ClassState],
        upcoming_encounter: Encounter,
    ) -> Optional[FormRecommendation]:
        """Given upcoming context, suggest a form. Used at trial-room choice points."""

    def quick_simulate(
        self,
        loadout: Loadout,
        opponent: Combatant,
        n_iterations: int = 5,
    ) -> FitSignal:
        """Run a quick simulation. Returns a categorical signal
        (strong_fit / marginal_fit / unclear / weak_fit), NOT a numeric percentage.
        Five iterations is too few for false-precision percentage output;
        the categorical signal is honest about its uncertainty."""
```

### Default UX: batch recommendations with single-click-accept-all

Lots of gear drops in this game (high drop volume is a defining ARPG pattern). Per-item Spirit Guide prompts would be invasive; auto-equip-on-countdown is too aggressive a default for a player base that has strong loadout preferences.

**The default UX is batched recommendations:** the Guide surfaces a list of pending swap recommendations periodically (e.g., when returning to a hub, finishing a fight, or opening inventory). The default action on the surfaced list is **"accept all" with one click.** Players who want finer control can drill into individual items, accept selectively, or reject the batch entirely.

Auto-equip-with-countdown remains an option — for players who want it, the Guide can be configured to commit recommendations automatically with a 5-second cancel window. But that's a player setting, not the default. The default is recommend-with-batch-accept.

This handles high drop volume gracefully:

- Common/uncommon gear: most drops never even surface as recommendations (they don't cross threshold for any form). They quietly populate inventory; vendor / discard / sort by player preference.
- Rare+ gear: surfaces as a recommendation when it would meaningfully improve the current loadout. Player accepts the batch periodically.
- Stash management: gear that doesn't help the current form but might help a future form goes to stash, gets re-evaluated when the player switches forms.

These are pure functions. They consume engine state, produce structured recommendations. No UI dependencies. They can be tested in the engine layer using existing convergence infrastructure.

### Why "engine-layer API now, UI later"

This is the same separation the project has applied throughout: simulator capabilities now, visual / UX presentation later. We've been doing it for class identity (Phase 1–3 build the architecture; UI/VFX renders it later); we apply the same to the Spirit Guide.

Building the Spirit Guide's reasoning logic now means:
- Gear can be designed with these decisions in mind from day one.
- The engine has analytical capabilities that future game-experience features can build on.
- We avoid having to retroactively expose internal state when the UI eventually arrives.

Building the *user-facing presentation* now would be premature — same reason summoner is deferred to post-UI/VFX.

## Trait infrastructure (shared with Priority 14)

Traits acquired via:
- **Class progression** (Priority 14: Traits-and-Skills system) — unlocked at game milestones
- **Gear drops** (Priority 02 — this design) — granted by equipped gear

are the **same kind of thing** mechanically. Both contribute to the player's effective trait state during combat. Both are read by the Spirit Guide for marginal-value analysis. Both are applied by the simulator the same way.

**Implication: gear and Priority 14 share trait infrastructure.** Specifically:

- Same trait schema (`TraitSpec`)
- Same engine validation (which traits map to existing mechanical primitives)
- Same combat-sim application (modifying ability behavior at fight time based on active traits)
- Same telemetry (traits get recorded the same way regardless of source)

The first of {Priority 02, Priority 14} to land builds the trait infrastructure. The second extends it. Since gear is the immediate priority, **gear's implementation builds the trait system, and Priority 14 inherits it later.**

This means gear implementation work isn't just "add gear to the engine" — it's "add gear to the engine, including the trait infrastructure that Priority 14 will eventually exercise more fully."

### Trait classes

Traits divide into roughly three categories based on what they modify:

- **Stat traits** — flat or proportional modifications to STR, VIT, DEX, etc. Composable; sum.
- **Ability traits** — modify how existing abilities work (multishot floor +1, mana cost -10%, cooldown -0.5s). Apply per-ability based on type/role/dimensional fit.
- **Granted abilities** — add a new ability to the class's repertoire. Rarer; legendary-tier gear or late-game progression unlocks.

The validation rule: every proposed trait must map to an existing mechanical primitive (stat, ability modifier, ability template). Traits that don't map are deferred (marked as "future trait, await new mechanic") rather than implemented inertly.

### Trait application formula

For stat traits, the math semantic matters and was surfaced explicitly during CP5:

```
final_stat = (base_class + Σ gear_flat + Σ trait_flat) × (1 + Σ trait_proportional)
```

Proportional traits multiply the **full accumulated stat** (base + flat contributions), not just the gear contribution in isolation. The latter ordering produces nonsense — e.g., a `+10% STR` proportional trait fails on a class whose gear contributes 0 raw STR (`0 × 1.10 = 0`). Implementation rule: **keep gear-stat values and trait-flat values raw at aggregation; sum them with the class base; then apply proportional as a single multiplier.** Pre-computing "adjusted gear values" by folding proportional into the gear contribution is the wrong order.

For ability traits (cooldown_factor, energy_cost_factor, multishot_floor_bonus, crit_bonus_damage, control_duration_bonus, etc.), the formula is per-key and per-ability, applied during ability resolution. Multiplicative keys aggregate per the canonical registry (`MULTIPLICATIVE_ABILITY_MODIFIER_KEYS`) before the resolver applies them to the per-ability value.

For granted abilities, "application" means adding the granted Skill to the actor's ability set during fight initialization; no formula.

### Trait provenance and stacking rules

Traits acquired from gear vs. traits acquired from progression have **different lifecycles** even though they share the schema and combat application. Pinning down the rules now (before implementation) prevents Priority 14 from re-opening this work later.

**Lifecycle differences:**

| Source | Attach | Detach | Persistence |
|---|---|---|---|
| **Gear traits** | When item equipped | When item unequipped (or item destroyed/lost) | Per-equip-state; tied to inventory state |
| **Progression traits** | When unlocked at progression milestone | Generally never (or only on form-switch — see open question) | Permanent for the player; survives across sessions |

Gear traits need clean **attach / detach semantics** in the engine: equipping an item activates its traits in the player's effective trait set; unequipping deactivates them. Edge cases to handle:

- Item destroyed while equipped → gracefully detach
- Equip-slot conflict (two items competing for the same slot) → unequip the previous occupant before equipping the new one; old item's traits detach atomically with new item's traits attaching
- Form-switch with gear equipped → gear stays equipped; gear traits stay active; only their *effectiveness* changes per the new form's `class_fit_profile`

**Stacking rules — within source:**

- Multiple gear instances each contributing the same trait class (e.g., two pieces of gear with `+10% fire damage`): **additive within category** (total = +20% fire damage). Follows the principle that "more gear should compound."
- Multiple progression unlocks of related traits: same — additive within category.
- **Exception — rate-modifier keys** (cooldown_factor, mana_cost_factor, similar percent rate keys): **multiplicative within source as well as across** (locked 2026-05-10 per CP4). Two gear pieces with -10% cooldown each → `0.9 × 0.9 = 0.81` (effective -19%, not -20%). Accepts a ~1pp feel tax at typical magnitudes in exchange for a uniform unbounded-stacking guarantee — prevents the edge case of two gear pieces with -50% each saturating to -100%. The "more gear should compound" principle remains in force for additive-friendly keys (HP, fire damage, stat traits, etc.); it's specifically rate-modifier keys that compose multiplicatively.

**Stacking rules — across sources (gear + progression):**

- Same-trait-from-different-sources: **additive across sources** by default (a +10% fire damage progression trait + a +10% fire damage gear trait = +20% total).
- Exception for *granted abilities*: **source-priority dedup, gear wins** (locked 2026-05-10 per CP4). If both gear and progression grant the same `granted_role` (e.g., "Volley Master"), the gear grant is kept and the progression grant is suppressed. Enforced inside `aggregate_traits()` via stable sort by source priority before deduplication — doesn't depend on caller order.
- Exception for *rate-modifier keys* (cooldown reductions, mana cost reductions, etc.): **multiplicative** — same uniform rule as the within-source exception above. Single rule for these keys, source-agnostic.

**Implementation anchor:** the multiplicative-key set is encoded as a canonical registry (`MULTIPLICATIVE_ABILITY_MODIFIER_KEYS` per CP4) rather than via the trait's `composition` field. A misconfigured trait declaring `composition=ADDITIVE` for a multiplicative key (e.g., cooldown_factor) is still aggregated multiplicatively — the registry overrides. The trait's `composition` field is documentation for human readers, not the execution path. New rate-modifier keys added in future work must be added to the registry, not just declared on individual traits.

These rules are deliberately simple. If playtest data surfaces edge cases, refine then.

**Edge cases worth surfacing now:**

1. **Trait disabled via gear unequip while in combat** — does the trait detach immediately, or persist until end-of-fight? Default: immediate detach (consistent with "what's equipped is what's active"); fight-time mid-detach is a real impact, but rare in practice.
2. **Stacking with class baseline** — gear traits stack on top of class baseline (whatever the class is naturally); they don't replace baseline. A class with naturally `multishot=2` getting a `multishot floor +1` trait → effective floor 3.
3. **Negative traits** — gear could conceptually have downsides ("at the cost of X"). Default: *no negative traits in initial scope.* All gear traits are positive contributions. This avoids the analysis-paralysis pattern from PoE-style "is this drawback worth it?"; gear is straightforwardly good.

## Bounded pre-computation: per-(class, monster) win rates

The convergence loop already runs class-vs-gauntlet fights. Currently it records aggregate per-class win rate; the per-(class, monster) breakdown is computed but not stored.

**Decision: store the per-pair breakdown — explicitly as bare-class win rate** (no gear contribution baked in). Bounded size: ~10 classes × ~10 monsters = ~100 pairs per season. Trivial DB cost. The data already gets generated; we're just persisting the slice we currently throw away.

**Important:** the stored matrix is the **bare-class baseline**, not the equipped-class win rate. Gear's contribution is computed via marginal-value at decision time, layered on top of the bare-class baseline. This means the matrix doesn't go stale every time the player equips/unequips gear — gear is added to the equation when a recommendation is being computed, not when the data is being stored.

This data powers Spirit Guide context-aware recommendations:

- *"You're 80% vs fire monsters but 30% vs ice monsters; consider switching forms before the next zone."*
- *"This new gear improves your hunter form's expected win rate against the upcoming wind boss from 55% to 78%."*
- *"Your current form has the highest expected win rate against the next 5 encounters; stay in this form."*

None of these require simulating "all combinations" of class × gear × monster on demand. The class × monster matrix is pre-computed; gear's contribution is added via the marginal-value formula at decision time.

## Cross-class smuggling — gated discovery mechanic

Smuggling is a *discovery feature*, not a routine inventory mechanic. Gear from prior seasons can be used on past-season characters (now spirits in the earth realm controlled by the player's real-human-body meta-character), but the path is gated by four constraints. Most cross-season drops will *never* actually be smuggled — that rarity is the design point. When smuggling DOES happen, it's a moment of recognition and discovery.

### The four gates (in order of player encounter)

1. **Equipped at ascension.** At season end (natural or via early ascension), only the items the player has *equipped* at the moment of transition carry forward to earth realm. Backpack contents are lost. This is a deliberate scarcity constraint — typically ~4–6 items per ascension survive (one per equipped slot). Players have to value an item enough to wear it at the transition moment.

2. **Archetype match.** A smuggled item must fit the receiving spirit's archetype — same `class_fit_profile` + stat-affinity rules as live gear (CP5b/CP5c/CP6b enforcement). A staff brought back from a caster season can't be equipped on a warrior spirit, regardless of element compatibility.

3. **Canonical element pair.** Gear carries a canonical element (fire / water / wind / earth / physical) underneath its seasonal flavor name. Smuggling requires the receiving past spirit to use the same canonical element. A "Frost Bow" (canonical: water) can equip on a past spirit whose canonical element was water, regardless of what flavor name that past season used ("Spring Bow," "Tide Bow," etc.).

4. **Decryption state.** Players don't initially know the canonical name of their gear — they see seasonal flavor names ("hearth," "amber," "frost"). Rift encounters within a season reveal the canonical mapping (the canonical element name appears explicitly in VFX and combat logs during rift fights). Until a player has decrypted a given canonical element, items tagged with that element can't be smuggled — they sit dormant in the spirit-realm inventory awaiting decryption.

### Why this design

The four gates produce two distinct discovery moments that are central to the player experience:

- **Discovery moment 1 (season 2+):** "Wait — this gear from my old character actually works on my old character?!" The first time a player ascends, returns in a new season, and realizes that some past-character spirit can equip carried-forward gear, the meta-game becomes legible. This requires gates 1–3 to align organically.
- **Discovery moment 2 (rift encounters):** "Oh — *that's* what amber really is." Rifts are fast-paced encounters where canonical elemental themes emerge as VFX and named in combat logs. Decrypting a flavor → canonical mapping unlocks all dormant gear of that element for smuggling.

Both moments make the player feel like they've discovered structural truth about the world — not been *told* about a feature.

### Realistic smuggling volume

Across a player's lifetime (e.g., 8+ seasons), the smugglable inventory is much smaller than total accumulated drops would suggest. Of ~1600 lifetime drops, maybe ~40–60 reach the spirit realm via Gate 1 (equipped-at-ascension; 4–6 slots × 8 ascensions). Of those, after Gates 2–4 filter for archetype + canonical pair + decryption, the *currently usable* smugglable inventory at any given time is more like 5–15 items.

That feels right for a discovery mechanic — each smuggle moment carries weight ("this old item from season 3 saves my run in season 7"), rather than smuggling becoming a routine optimization layer.

### Engine implications (post-Priority-02 work)

The gating logic is post-Priority-02 scope, but the foundations being built in Priority 02 align cleanly with it:

- **Per-gear canonical element tag** — already in scope (gear has canonical element underneath seasonal flavor)
- **Archetype fit (class_fit_profile + stat affinity)** — built across CP5b/CP5c/CP6b
- **Per-class carried_gear with harvested canonical loadouts** — companion-track engine work (captured 2026-05-10 alongside the demo1 design). Convergence persists per-fight loadout details; post-convergence canonical loadout selection populates `class.carried_gear` from the historically best-performing loadout per class. Gives every smuggled item *real provenance* — a historical record of having mattered in actual simulation. Strengthens the smuggling discovery story: a smuggled legendary isn't generic gear, it's the specific item a specific class carried successfully in a specific past season.
- **Persistent past-character roster** — needs a future system to track all past-season spirits accessible to the player
- **Decryption state per player** — needs a future system tracking which canonical elements the player has discovered via rifts
- **Rift encounter system** — needs a future encounter type that reveals canonical names

The Spirit Guide engine API (CP7) should *not* recommend smuggle-equips on locked items (failing Gate 4) — it would spoil the discovery. The Guide treats undecrypted gear as if it doesn't exist for recommendation purposes; only after decryption does smuggling enter the marginal-value calculation.

### Interaction with the 70/30 loot model

The aggressive gating is what makes the 70/30 loot split defensible. Under permissive smuggling (e.g., any cross-class gear usable across seasons), 30% pure RNG would produce too much abundance — players would constantly cycle through cross-class options. Under gated smuggling, the 30% RNG produces a stream of *potential future* smugglable items, most of which will never actually surface because they fail Gate 1 (not equipped at ascension) or Gate 4 (player hasn't decrypted that element yet). The rarity is preserved by the gates.

Tuning the loot split without considering smuggling gates would miscalibrate. The two systems must be tuned together at validation time (Priority 15).

## Color integration (added 2026-05-09)

The engine already has a structural color system — abilities, classes, monsters, and trial bosses all carry color data sampled deterministically per element. Gear should reuse this same infrastructure rather than reinvent visual identity. Three layers exist:

1. **Color spectrum** (`src/reincarnated/foundation/color_spectrum.py`) — a 0–1,000,000 range partitioned into 256 bands. Each canonical element has a fixed color range (fire 0–90k reds/oranges; water 560k–700k blues/cyans; etc.).
2. **`ColorLabelLibrary`** — 256 LLM-generated descriptive labels for the bands, generated *once* during foundation setup and cached forever. NOT regenerated per season.
3. **Naming pipeline integration** — `name_skill()` and `name_class()` already pass `Color: {color_label}` to the LLM via `ColorLabelLibrary.label_for(color_value)`. The label informs flavor coherence without adding API calls.

### Gear color additions

Three fields added to gear schema (mirroring the pattern abilities and classes already use):

| Field | Type | Source | Tier |
|---|---|---|---|
| `color_value` | `int` (sampled from gear's dominant element range) | Engine deterministic — `sample_color_in_range(element, rng)` | Every gear instance |
| `color_palette` | `list[int]` | Engine — derived from gear's element flavor + any sub-element traits | Every gear instance |
| `color_signature` | `str` (hex like `"#A8472A"`) | LLM — produced inside the existing consolidated `gear_unique_naming` call | Legendary only |

**Cost: zero new LLM calls.** Color enters via:

- `color_value` and `color_palette`: pure engine sampling; no LLM.
- Color label flowed to the gear-naming prompt as `Color: {color_label}` (existing pattern); the existing rare+ naming call now has color context in its input. **No new call** — just richer prompt input.
- `color_signature` (legendary only): added as one more field in the existing consolidated JSON response (`{name, flavor_text, visual_prompt, color_signature}`). Still **one call per legendary item**, not multiple.

The LLM call delta from the call-map document (file 19) — ~25 new calls per season for rare+ gear — does not change. Color is incorporated *inside* the existing prompts and JSON responses.

### Why this matters

**For LLM naming flavor coherence:** a "fire weapon with smoldering-ember coloring" names differently from a "fire weapon with golden-flame coloring." Color label gives the LLM more material to work with, producing more variation across same-element gear. This is the same mechanism that makes `Frostbitten Hearthcaller` feel visually cohesive at the class level — extending it to gear means gear names match the visual identity their color implies.

**For downstream visual consumers (Meshy / Unity):**

- `color_palette` is structured numeric data the consumer can use directly (mapped to RGB / HSL).
- `color_signature` (hex string, legendary tier only) is a direct color hint Meshy can use as a generation-prompt parameter.
- `visual_prompt` (existing field) is prose-level description; color is the structured complement.

When the Meshy/Unity work eventually happens (post-UI/VFX, far-future), these fields are direct inputs — the consumer doesn't have to invent color from prose. And because gear's color sits in the same band as its element's classes and monsters, visual consistency emerges automatically (a fire weapon, a fire mage, and fire monsters all sit in the 0–90k red/orange range — they read as visually related without explicit coordination).

### Cross-class smuggling implication

Color is tied to the gear's *dominant element* at generation time, not to the equipping class. A fire-flavored bow keeps its red/orange coloring whether equipped by a fire mage (same color band — visually integrated) or by a hunter (different color band — visually contrasting, "the red bow on my green-coded ranger" reads as a meaningful customization). Cross-class smuggling produces *visible* contrast through color, in addition to the mechanical fit-profile differences.

---

## Visual prompt field (forward-compat with Meshy / Unity)

Gear schema includes `visual_prompt: Optional[str]` populated at LLM-naming time for rare+ tiers. This field is the LLM's description of the gear's *visual* appearance, geared specifically as an input to a visual-generation pipeline:

- Three.js prototype phase: visual_prompt could be parsed for color/shape hints to drive simple meshes.
- Meshy / Unity production phase: visual_prompt is the text input to Meshy's text-to-3D generation.
- The mechanical layer doesn't consume this field; it's pure forward-compat for downstream consumers.

Common/uncommon gear (template-named) doesn't need a visual_prompt; their visual treatment is template-based. Rare+ gear needs it because their unique identity demands unique visuals.

## What this design does NOT include

- **Spirit Guide UI / voice / countdown timer** — far-future UI work. Build the engine API now; ship the user-facing Guide post-UI/VFX.
- **Pre-computation of all class × gear × monster combinations** — combinatorially infeasible and unnecessary. The bounded slices (per-(class, monster) win rates, gear power scores, gear class-fit profiles) are sufficient for Spirit Guide decisions.
- **Vendor / economy mechanics** — out of scope.
- **Gear crafting / upgrading** — out of scope.
- **Set bonuses / armor sets** — could fit later as a special trait category; not in initial scope.
- **Gear durability / repair** — out of scope.
- **Trade between players** — multiplayer is explicitly out of scope; gear is single-player only.

## Open questions

1. **Common/uncommon LLM call exclusion threshold.** Should we LLM-name *some* uncommon gear (e.g., 10% of uncommon drops promoted to LLM-naming) for variety, or stay strictly template-only below the rare tier? Default: strictly template; revisit if uncommon gear feels samey in playtest.

2. **Visual prompt field for legendary gear** — should it be a separate LLM call (prompt the LLM specifically for visual description), or should the existing rare/legendary naming call be extended to include a visual paragraph? Default: extend the existing call; cheaper and cohesive.

3. **Bad luck protection.** Should the Spirit Guide track "this player has been struggling for a while with no useful drops" and bias the next drop's class-fit toward their current form? This is a slippery slope (becomes adaptive difficulty). Default: no, accept RNG; rely on form-switching as the player-side mitigation. Revisit if playtest shows runs feel hopeless.

   **Related: absolute usefulness floor on recommendations.** The Spirit Guide's recommendation threshold is "marginal value above current loadout AND above an absolute usefulness floor for the scenario." If a player is struggling AND the available gear is objectively poor (below the average-gear baseline for the scenario), the Guide does not recommend equipping the bad gear; it stays silent. In extreme cases where nothing in the player's inventory crosses the floor, the Guide may instead suggest *form-switching* as the better mitigation (a separate recommendation type). This prevents the Guide from doing the patronizing "here, this terrible gear is slightly better than your terrible gear" recommendation in low-quality drop streaks.

4. **Trait magnitudes** — what's the typical numeric range for stat traits, ability traits, granted-ability traits? Empirical tuning territory; let CP-equivalent verification data drive this.

5. **Threshold tuning — absolute marginal-value floor.** The single threshold's exact value is empirical. CP-level convergence runs determine what marginal-value floor produces the right "noticeable improvement" calibration without nagging on every drop. Initial guess: 0.05–0.10 in power_score units. Refine against player-observable behavior (recommendation frequency, accept-rate of recommendations).

6. **AGI stat — current state.** All telemetry rows show `agi_stat = NULL` while STR / VIT / INT / WIS / DEX carry meaningful values. Three possibilities to disambiguate before stat-threshold gating commits to a 5-stat model: (a) deprecated stat (drop the column), (b) reserved for future mechanics like dodge / initiative (document and preserve), (c) a write gap (small bug to fix). Worth a brief investigation during CP3-equivalent work.

7. **Stat-threshold floor calibration.** Heavy armor STR floor, melee STR floor (1H vs 2H), bow DEX floor, shield STR floor — exact values are empirical, calibrated against the season's actual stat distributions. CP-level acceptance: a season's casters cannot equip heavy armor; a season's STR-build classes can; medium armor admits both STR-build and DEX-build classes at the threshold. Initial guess: ~60% of the typical primary-stat allocation for that build.

8. **Elemental ailments on physical weapons (CP5c finding).** Burn / freeze / shock affixes are currently tagged `energy_type=mana`, meaning a fire-themed hammer wielded by a rage warrior can't roll burn-on-hit. Defensible default — burn is a magical effect channeled through mana — but it eliminates cross-class flavor for physical archetypes acquiring elemental weapons. The cleaner long-term resolution is to retag elemental ailments as `damage_type=fire` (etc.) instead of `energy_type=mana`. This requires the `damage_type` axis to be active in fit profiles (currently deferred — all profiles carry `{"all": 1.0}` for damage_type). Tied to the broader element-on-physical question deferred since Phase 1. Revisit when damage_type axis activates (likely Phase 4 or post-Priority-14).

9. **Bow empty-affix-pool gap (CP6 verification finding).** Bow's fit profile carries `energy_type=focus` and `range_profile=long`, but no current affixes are tagged for those dimensions. Result: bow falls through to the universal-affix fallback on every roll, with `log.warning` firing. Bows still produce functional gear (universal pool covers stat boosts and generic effects), but hunters get less affix *variety* than other archetypes. Fix: add ranged-archetype affixes to the catalog tagged with `range_profile=long`, `stat_affinity=dex`, and where appropriate `energy_type=focus` (multishot extensions, ranged crit modifiers, range extensions, focus-resource regen). ~Half a day of catalog work. Track as polish-tier; addressable post-Priority-02.

10. **Loot economy validation — journey vs. outcome (post-Priority-02 concern).** CP6c's `END_GAME_DROPS_PER_SLOT=50` asserts an *outcome*: an end-game player has 50 drops per slot. The unvalidated assumption is that the *journey* to that outcome is feasible and equitable across archetypes. Once loot drop rules are defined (drop rates per encounter type, encounter density per level, class-awareness model), a separate simulation should walk a class through level 1 → cap and measure actual equipped-loadout fit at milestones. Failure modes it catches that no other validation pass does: archetype starvation (one class gets 80% unusable drops), specific-slot stagnation (bow class never gets bow drops), tier-progression unevenness across slots, stash overflow from cross-class smuggling. Belongs as a candidate priority (Priority 15: Loot Economy Validation) prerequisite for the Three.js demo Phase 3 (loot + boss looping). Crosses Priority 14 (level scaling becomes first-class) and the future loot-economy design layer. Out of scope for Priority 02 (which generates gear instances; loot economy is the layer on top that determines drop rules).

11. **DoT ailment damage bypass — RESOLVED 2026-05-10 (CP7b).** Originally surfaced in CP7: the `resolve_skill` damage path applied DoT ailments using baked-in magnitudes without applying `buff_dmg_mult` or `damage_modifier`, meaning gear and class scalar didn't reach DoT damage. Pressure-test analysis confirmed 41% of generated classes were DoT-significant and 9/63 DoT-primary classes were FAILING convergence outright (e.g., a fire_mage with 75.9% DoT fraction at modifier=0.20 had 100% win rate at max iterations — broken in the convergence model). CP7b applied the fix in `_try_apply_ailment` (burn / bleed) and `heal_over_time` paths, plus re-converged existing seasons. Post-fix: convergence failures dropped from 3/10 to 1/10 (the remaining one is non-DoT, separate concern); DoT-primary class modifiers rose modestly (mean +0.024, mostly visible as freeing floor-pinned classes). **Important secondary finding from CP7b:** the dominant calibration effect across all archetypes is CP6c gear power, not the DoT bypass. The DoT bypass was a secondary compounding effect; the four-baseline progression (pre-CP6 → CP6 → CP6c → CP7b) shows the CP6→CP6c step (best-of-N gear distribution) accounts for the majority of the modifier shift, with CP7b providing a smaller upward correction.

12. **Non-DoT class floor-pinning at CP6c gear levels (CP7b finding).** Earth_caster seed 42 remains floor-pinned at 0.0509 modifier after the DoT fix despite having no DoT abilities. Two possibilities to disambiguate over time: (A) generation outlier — that specific class has unusually high-magnitude direct abilities; one-off, not systemic; (B) calibration headroom is too tight — even non-DoT casters with normal abilities can't be modulated down enough at `END_GAME_DROPS_PER_SLOT=50` gear levels, suggesting either lowering the convergence floor (currently 0.05) or revisiting the equipped-distribution constant. Track over the next several generated seasons. If pattern recurs, address; if it stays a one-off, accept.

13. **Convergence sampling variance — gear loadout Monte Carlo noise.** The current convergence process samples a fresh loadout per fight (30 fights/matchup × 4 slots = 120 slot-rolls per matchup × multiple binary-search iterations). At N=50 best-of-distribution this produces low but real variance (~std deviation of 3 legendaries over 120 rolls). Binary search across modifier values currently re-samples loadouts each iteration, adding noise unrelated to the modifier itself. **Two surgical refinements available, both at ~zero compute cost:** (C) **stratified sampling** — pre-compute the 120 slot-rolls to collectively match expected distribution exactly, then shuffle into 30 loadouts; preserves within-loadout variance, eliminates aggregate noise; (D) **common random numbers across binary search iterations** — cache the 30 sampled loadouts per (class, monster) matchup, reuse across all modifier values in the binary search; isolates the modifier as the only variable being searched. **Status: not blocking; track for application if Q12 floor-pinning recurs.** A Process B alternative (fixed average loadout) would change the design philosophy from "expected-over-distribution" to "median-loadout-only" — argued against because it interacts awkwardly with the loot economy (lucky players would feel less rewarded; unlucky more punished). Process A (more samples) is a fallback if C+D aren't enough.

## Loot economy model (locked 2026-05-10)

Two design parameters are now settled and should inform Priority 15 work + Demo Phase 3 + Spirit Guide threshold calibration (CP7):

**Season cadence: one-week seasons.** Each season runs roughly one week of player time. New class roster, new monster set, new generated content per season. Gear and player progression are assumed to persist across seasons (per the cross-class smuggling design intent — gear accumulated in season 5 becomes useful in season 7 when player switches forms). This means the equipped-distribution calibration target (N=50 drops per slot) represents accumulated drops across several seasons, not a single week.

**Loot class-awareness: 70/30 hybrid.** Drops are 70% smart loot (biased toward current class's archetype-usable pool) and 30% pure RNG (any class's gear can drop). Rationale:

- One-week season cadence means players can't afford to spend days on bad RNG; smart loot ensures the gameplay loop stays rewarding.
- 30% RNG preserves: cross-class smuggling (gear for other classes still drops at meaningful rate), "lucky drop" surprise moments (unexpected legendary tier still happens), form-switch loot incentive (committed-form players still accumulate some cross-form options).
- This is a meaningful gameplay knob: form selection becomes consequential for *what gear accumulates*, not just for combat. Players who alternate forms build more balanced inventories; players who commit to one form get deeper specialization in that form's gear.

**Implications for Spirit Guide threshold (CP7):** under smart loot, most drops are *targeted* at the player's archetype, so the marginal-value threshold needs to be higher than under pure RNG to avoid nag-on-every-drop. Initial calibration target ~0.10–0.15 in `power_score` units (refined empirically against weekly drop volume). Without this adjustment, Spirit Guide would prompt on most rare+ drops because most are mathematically eligible upgrades.

**Implications for cross-class smuggling math:** at typical play (~200 drops/week × 8 weeks = ~1600 drops, of which 30% = ~480 are cross-class), the smuggling story is real but bounded. Stash overflow is unlikely; form-switch usefulness is genuine.

## Cross-references

- `../collaboration-handoff/06-trial-room-and-class-scoping.md` — design intent: spirit-swap, form library, class scoping, trial room (cross-class smuggling implication).
- `09-geometry-palette-discussion.md` — geometry palette (gear interacts with geometry types via ability modifiers).
- `../collaboration-handoff/10-decision-log-entry-dimensional-generation.md` — the architectural decision that gear builds on top of.
- `16-project-roadmap.md` — Priority 02 (gear) and Priority 14 (Traits-and-Skills) positioning.
- `engine-repo/test-plans/priority-02-gear-status.md` — Phase 0-era plan, now superseded by this doc as the canonical design intent.

## Memory pointers

When implementation begins, the relevant memory files are:
- `project_engine_state_findings.md` — empirical findings, accumulating concerns
- `project_progression_concept.md` — Priority 14 sketch (note the trait infrastructure shared)
- `project_role_orientation_taxonomy.md` — role-orientation values, sub-flavor taxonomy
- `project_geometry_palette.md` — geometry palette decisions

The eventual gear implementation CLI prompt should be drafted with this design doc as its primary scope reference.
