# Path B resist design — design-of-record spec (cap-everything-but-costly)

**Author:** gandalf (design seam). **Mode:** Pattern-B, verification-first. **Status:** DESIGN-OF-RECORD — Matt affirmed Path B (2026-06-22) and directed "write the spec on this basis." This is the Step-0 artifact. It routes to **jack-ryan Gate-1 DESIGN-MODE** before any build seam touches code.

**Supersedes:** the spiky / anti-tax resist design locked at the typed-resistance wave (anchor ruling `2026-06-21-typed-resistance-boss-anchor-ruling.md`; decisions-log `ea39ecc`). The supersession is a **deliberate foundation pivot**, not a drift — see §13 (governance).

**Synthesizes:** the verified resist mechanism (`2026-06-22-player-resist-vs-encounter-element-explainer.md`), the fork disposition (`2026-06-22-cap-everything-vs-spiky-resist-fork.md`), Legolas's D2/PoE research (`legolas/findings/2026-06-22-d2-poe-endgame-resist-and-monster-modifiers.md`), and Matt's affirmed decisions in this session.

---

## 1. TL;DR — what is being built

**Path B = resist is a mandatory-but-costly baseline.** Every endgame player is *expected* to reach ~0.75 on all 7 rotating elements; reaching it consumes ~the entire defensive gear budget, so capping genuinely **competes with offense for gear slots.** This is the D2-Hell / PoE-maps endgame model, native-adapted (slot-competition, not an imported difficulty-tier deficit).

Path B retires the locked Path A (resist scarce ~1.5 units; cap 1–2 elements; "bring the right form" = spike-matching). Under Path B, "bring the right form" means **bring overcap + the right counter to THIS rare pack** — the threat is the rare/unique monster that strips your cap, not the one element you didn't build.

**Path B is load-bearing on three pieces that must ship together (§9). Any one missing turns Path B into the PoE under-cap tax.** The build sequence (§12) is: this spec → Gate-1 → **sim Loadout widening 4→10** (the gating correction, §5) → breadth-affix taxonomy + budget recalibration → reduction-monster cycle (Matt-gated).

**No change to the resist formula or the caps.** Path B is a generation-budget + affix + sim-Loadout + monster-content change. The math model (§10) already supports it.

---

## 2. The model — Path B, slot-competition variant

`damage_taken = incoming × (1 − resist[element])`, clamped `min(0.95, max(0.0, …))`, elemental always-hits. (Unchanged — `foundation/math_model.py:116-128`.)

Path B makes capping **necessary AND achievable**. The safety condition that separates it from the rejected dm=6.0 tax and from the PoE one-shot tax:

> **Capping must be ACHIEVABLE within budget.** Necessary-but-achievable = genre standard (works). Necessary-but-UNachievable = the PoE one-shot tax (the failure). Path B does **not** touch per-hit damage; it makes capping reachable-but-total.

**Why slot-competition, not the D2/PoE deficit.** D2 (Hell −100 all-res, stack +175 to reach 75) and PoE (−60% campaign, stack +135) manufacture cost via a **baseline penalty you climb out of** — an artifact of difficulty tiers (Normal→NM→Hell) we do not have. Importing it is gratuitous. Instead: **resist starts at 0; the budget is tuned so uniform-capping consumes ~the whole defensive affix budget; offense competes for the same gear slots.** The opportunity cost is identical to D2/PoE; the mechanism is native.

---

## 3. The slot model — 10 slots, 9 resist-capable

**Locked (Matt 2026-06-22):** 10 gear slots; **9 are resist-capable** (every slot except the main weapon).

**AUTHORITATIVE slot inventory = `gear_slot_labels` (file 33 / `class_schema.py:131-142`), 10 slots.** This is the target the §4 / Rule-2 math is anchored to. The 10 canonical slots: **Weapon** (no resist), Off-hand, Helm, Chest, Gloves, Boots, Belt, Ring, Ring, Amulet. The "+9 → 9 resist-capable slots to cap" arithmetic in §4 (property 2) and Rule 2 is anchored to **exactly this 9** (10 minus the non-resist weapon). Any rep that disagrees with this 10/9 model is the outlier to be reconciled to it, NOT a competing authority (see §3.0).

### 3.0 The slot-inventory reconciliation — three reps, one locked target (CONCERN-1 close, jack-ryan Gate-1)

Three reps disagree on slot count; the locked 10/9 model picks the winner and folds the outliers. Verified first-hand:

| Rep | File | Count | Naming | Has LEGS? |
|---|---|---|---|---|
| **`gear_slot_labels` (AUTHORITATIVE)** | `class_schema.py:131-142` | **10** (9 resist-capable) | `off_hand` | **No** |
| `GearSlot` enum (generation-side) | `partition_schema.py:53-64` | **11** (comment: "11 slots") | `SECONDARY_ITEM` | **Yes** |
| live `Loadout` (sim, pre-1a) | `gear_schema.py:198-228` | **4** (3 resist-capable) | `off_hand` | No |

**The `gear_slot_labels` 10-slot model wins** — it is the file-33 canonical, humanoid-display, consumer-facing inventory, and it is what Matt locked. The other two are reconciled TO it:

- **The 4-slot live `Loadout` is the under-rep** → widened 4→10 by Step 1a (this is the whole gating build, §3.1).
- **The 11-member `GearSlot` enum is the over-rep** — its extra member is **`LEGS`**. **RULING (gandalf, design-owned): `LEGS` folds into `CHEST`** (armor consolidation — the natural humanoid grouping; keeps the resist-capable count at exactly 9; does NOT re-open the §4 +9 math). The 1a enum→loadout bridge maps `LEGS`-slot generation output onto the chest slot. **This is NOT a new player-facing slot** and does not become an 11th equipped slot; the equipped/resist model is 10/9, full stop.
  - *Why not surface an 11th slot to Matt:* an 11th resist-capable slot would make it 10-resist-capable (10 × +9 = +90 of slack), which §9 explicitly warns is the free-baseline tax — capping gets *easier*, the "+9 is load-bearing" gate-rationale collapses. The locked 10/9 model is the deliberate anti-tax choice. Folding LEGS preserves it. (If Matt later WANTS an 11th slot, that is a budget-math re-open, not a reconciliation — out of scope here.)

### 3.1 The correction that gates everything — the sim does NOT carry 10 slots today

> **Matt's working premise was "this exists in the sim today, right?" — it does NOT.** Verified, rigorously (having been burned by the stale-export error earlier this session):
>
> - The **equipped Loadout the sim sums is 4 slots** — `gear_schema.py:198-292`, `class Loadout(BaseModel)`, docstring line 200: *"up to four slots."* Fields: `weapon, off_hand, armor, accessory`. `_slots()` returns ≤4 pieces; `combined_stats()` SUMS resist across those 4 only. Of the 4, the weapon carries no resist → **3 resist-capable slots in the live sim.**
> - The **11-member `GearSlot` enum** (`partition_schema.py:53-64`, comment line 51 literally "11 slots": MAIN_WEAPON, **SECONDARY_ITEM**, HEAD, CHEST, HANDS, FEET, **LEGS**, AMULET, RING_1, RING_2, BELT) exists **generation/partition-side only** (gear_instance_generator, partition_roller, keystone_loadout_materializer, partition_modifier_pool). It does **not** flow into the equipped Loadout the sim runs. Note: this enum names the off-hand `SECONDARY_ITEM` (NOT `OFF_HAND`) and includes a `LEGS` member the locked 10-model folds into CHEST per §3.0.

**Consequence: widening the sim Loadout from 4→10 (9 resist-capable) is the FIRST Path B build piece, and it gates the affix taxonomy.** It is not "the obvious choice because it already exists" — it is a real build. The good news (the silver lining): a 10/11-slot representation already exists on the generation side, so Path B **bridges** an existing generation rep into the equipped loadout (folding the enum's LEGS into CHEST per §3.0) rather than inventing the slot model from nothing.

**Scope of the widening (rocket + gamora + star-lord + drax, under jack-ryan Gate-2):** the `Loadout` schema (4 fields → 10), `_slots()`, and **every `_slots()` consumer** — `combined_stats()` (sum resist across 10), `combined_ability_modifiers()` (`gear_schema.py:281-296`, also iterates `_slots()`), `combined_traits()` (`:298-303`), `total_power_score()` (`:305-306`); the spirit-guide displaced-value branch (`spirit_guide.py:228-251` `_displaced_value()` — hard-codes the 4 slot-names "weapon"/"off_hand"/"armor"/"accessory" and returns 0.0 displaced-value for any other slot, so 6 of the 10 slots would be silently mis-valued unless extended); canonical serialization (`canonical_loadout.py:18-41`, 4-slot today); telemetry (`player_loadout` / resist export fields); spirit-guide aggregation; and the loadout web app (drax — surface the 10 slots). The enum→loadout bridge applies the §3.0 LEGS→CHEST fold. This is a cross-seam interface change → MIGRATION.md per ADR-004.

---

## 4. The breadth-affix taxonomy

Resist is minted in four **breadth tiers**. Today the engine mints **single-element only** (`gear_catalog.py:149` — `element_resist`, 0.05–0.25, single element, armor+off_hand; `gear_generation.py:969-980` sums it). **The dual / trio / all branches are net-new mint work for rocket** and are the load-bearing addition that makes uniform-capping a *puzzle* instead of a slog (§9.1).

Magnitudes below are expressed in **resist-points** (1 point = 0.01 mitigation; 75 points = 0.75 = the cap). Ranges are **proposed starting points — gamora calibrates** to hit the §8 budget targets and the §2 safety condition.

| Breadth | Elements hit | Per-element range (proposed) | Max total points/roll | Role |
|---|---|---|---|---|
| **single** | 1 | +18 → **+25** | 25 | the only fast-cap-one-element path (3 slots → cap one element) |
| **dual** | 2 | +12 → +16 ea | 32 | concentrate on a pair (e.g. a fire+water boss-pair counter) |
| **trio** | 3 | +9 → +13 ea | 39 | mid-breadth coverage |
| **all (7)** | 7 | +6 → **+9** | 63 | the efficient breadth path; the uniform-cap engine |

**Two properties this table must preserve (gamora's calibration invariants):**

1. **Total-points efficiency rises with breadth** (25 < 32 < 39 < 63) but **concentration falls.** Resist-all gives the most *total* mitigation per slot but cannot be aimed; single gives the least total but the only way to *fast-cap a chosen element.* This is the D2/PoE all-resist-affix design exactly — the efficient capping path is breadth, the concentration path is single.
2. **Uniform cap ≈ all 9 resist slots.** 9 slots × resist-all max (+9) = +81 to **every** element → all 7 at 75 with 6 points spare toward the 0.80 gear ceiling. At min rolls (+6 × 9 = +54) you fall short — **so uniform capping requires good resist-all rolls across all 9 slots.** That "you need the rolls" is the itemization puzzle; it is the intended texture, not a defect.

---

## 5. The two locked rules

### Rule 1 — one resistance affix per gear slot (LOCKED, Matt 2026-06-22)

A gear slot may roll **at most one** affix from the resistance family. Resist-all on a pair of boots **excludes** resist-trio (or any other resist breadth) on the same boots.

- **This is NEW.** Today nothing prevents a slot from rolling fire-resist AND water-resist as two separate `element_resist` effects (`gear_generation.py:1127-1129` `replace=False` blocks only identical pool entries, not two different resist entries). Rule 1 must be enforced by **rocket** via a resistance-family dedupe in the effect-roll selection.
- **It composes with the breadth taxonomy:** "fire + water on one slot" is no longer two single rolls — it is **one `dual` roll.** Breadth is the *only* way to put multiple elements on one slot. This is what gives the taxonomy its teeth (without Rule 1, a slot could stack singles and the breadth tiers would be redundant).
- **Player-experience consequence:** each of the 9 resist slots is one decision — *which breadth, which elements* — not a stacking exercise. It makes the 9-slot resist budget legible (D2's "one suffix per affix-group" legibility, applied to resist).

### Rule 2 — ranges per breadth, resist-all max +9 (LOCKED, Matt 2026-06-22)

Each breadth tier rolls within a range (the §4 table). **Resist-all caps at +9.** The +9 ceiling is load-bearing: it is what makes "uniform cap consumes ~all 9 slots" true (§4 property 2). gamora must not calibrate resist-all above +9 without re-deriving the slot-consumption math (a higher cap would let fewer slots cap everything → free baseline → the tax §9).

---

## 6. The budget math (Matt's affirmed targets)

In resist-points (0.75 = 75):

| Build | Per-element resist | Total points |
|---|---|---|
| **Fully-defensive** | 0.75 on all 7 | **525** |
| **Offense (concentrated)** | 0.75 on 4, **0.40 on 3** | 4×75 + 3×40 = **420** |
| **Delta** | drops 3 elements 0.75→0.40 | **105** (= 3 × 35) |

The 105-point delta is the offense player's **purchase**: by accepting 0.40 on three elements instead of 0.75, they free gear budget for offense.

### 6.1 The binding currency is SLOTS, not points

Points are the legible accounting; **the 9 resist-capable slots (one resist affix each, Rule 1) are what actually bind.** Path B enables three archetypal itemizations:

1. **Full-cap (defensive):** ~all 9 slots → resist (heavy resist-all). 0.75 on all 7. Defense is *solved*; the player sweats only the reduction cycle (§11). ~0 offense from these slots.
2. **Concentrated (Matt's offense build):** fewer slots → resist; singles/duals cap 4 priority elements; the other 3 sit at ~0.40. Frees slots for offense affixes. **The reduction cycle bites precisely the 3 low elements** — that is the dynamic closure (§6.2).
3. **Glass:** ~0 resist slots, all offense. Kill-fast-or-die. The reduction cycle is lethal on everything.

**The 105-point delta in slot terms** frees roughly **2–4 offense affixes** depending on which breadth is dropped (105 ÷ 63 ≈ 1.7 if dropping resist-all rolls; 105 ÷ 25 ≈ 4.2 if dropping singles). gamora's calibration nails the exact conversion so the tradeoff is **meaningful — not free (would be a flat tax), not crippling (would be match-or-die).**

### 6.2 Why concentrated-vs-uniform is a FEATURE, not a leak

Path A allowed only one shape (spiky). Path B preserves **genuine itemization choice** — uniform-under-cap vs concentrated-cap-some vs full-cap — and the reduction cycle makes each choice *live*:
- the uniform-under-cap player is reduced below survivable on **everything** at once;
- the concentrated player is fine on their 4 but **cliffs on their 3** when a pack strips them;
- the full-cap player sweats but survives, having paid for it in offense.

This is the itemization richness Path B buys over Path A. **It must survive calibration** — if gamora's ranges collapse it to "everyone runs resist-all" or "everyone runs full-cap," the choice is gone and we've rebuilt a flat baseline.

---

## 7. Opportunity cost — the offense side of the trade

The resist affixes compete, slot-for-slot, with the offense pool (`gear_catalog.py`: `damage` on_hit 0.15–0.30 / on_crit 0.25–0.45; `buff_damage` 0.05–0.15). Every resist affix on one of the 9 slots is an offense affix not taken.

**gamora's calibration obligation:** tune the resist ranges (§4) AND the offense ranges so the §6 trade is real — full-cap meaningfully lowers DPS; glass meaningfully raises it; concentrated sits between. The proof is §11.x: *resist genuinely competes with offense* (not a free add, not a crippling tax).

---

## 8. The overcap buffer — 0.80→0.95 is already PoE's design

The formula clamps resist at **0.95**; gear stacks each element to a **0.80** ceiling (`gear_schema.py` `_RESIST_CEILING = 0.80`). The **0.80→0.95 headroom is reachable only from non-gear sources** — and it **IS PoE's overcap buffer, already in our math.**

- A reduction pack applies −0.20 to fire. At 0.80 gear-cap you drop to 0.60 against that pack. With an overcap source pushing you to 0.95, you drop to 0.75 — **still capped.**
- This gives **set bonuses / spirit-guide / a keystone** a clear, non-redundant role: **buffer against the reduction cycle.** Exactly PoE's overcap design.
- **Path A left this headroom inert; Path B gives it purpose.** No formula change needed — this is why Path B costs no math-model work.

**Retained:** per-element **gear** cap 0.80; 0.80→0.95 reserved for overcap sources. (These are unchanged from today.)

---

## 9. The three load-bearing pieces — must ship TOGETHER

Path B is a **set.** Ship any subset and you build the tax. (This is the hard gate on the build — §12 sequences them but none can be the *end state* alone.)

### 9.1 The breadth affix (rocket) — makes capping ACHIEVABLE
The dual/trio/all mint branches (§4). Without resist-all, uniform-capping off single rolls alone is brutal (D2's lesson) → an unachievable mandate → the tax. **This is the single most important generation piece for Path B viability.**

### 9.2 The budget raised to ≈ cap-everything cost — AND NOT PAST IT (gamora)
Tune the §4 ranges + the 9-slot model so uniform cap consumes ~all 9 slots. **Do not overshoot:** a budget past cap-everything cost makes capping a free flat baseline everyone gets → mandatory tax, zero decision (the worst outcome). Budget ≈ cost-to-cap, never ≫.

### 9.3 The reduction-monster cycle (Matt's rare/unique ask) — keeps capped resist LIVE
Without it, a capped player has **solved** defense and the system goes inert. This is the payoff of Path B and Matt's explicit want. PoE-layered model (§11). **It is itself a multi-wave build (≈ the proxy's weight) — Matt-gated (§12 Step 2).**

> **Do NOT raise the budget without (9.1) and (9.3).** High budget + no breadth affix = unachievable mandate = tax. High budget + no reduction cycle = solved, boring baseline.

---

## 10. The amplification floor (affirmed)

The formula clamps player resist at `max(0.0, …)` (`math_model.py:116-128`) — reduction can at most strip a player to **0% (full damage), never negative (amplified >100%).** Affirmed asymmetric design:

- **Player as defender: keep the 0.0 floor.** Reduction's worst case is full damage. Fits the always-hit / no-dodge floor — amplification on top of unavoidable hits is over-punishing.
- **Monster as defender: allow negative** (penetration as the offense reward; already partially present via the floored monster path, `combatant.py:1104`).

Asymmetric floor is correct: it rewards offense penetration against monsters without making the player's unavoidable hits amplifiable.

---

## 11. The reduction-monster cycle — PoE-layered, bounded enum

**Model: PoE-layered, NOT D2-brutal.** Legolas's divergence note: our system (always-hit, 0.95 clamp, no immunity wall, linear scaling) is **structurally PoE.** D2's binary immunity wall and Conviction cap→0 do not fit; PoE's layered-reduction-plus-overcap does.

- **Layers (PoE-faithful):** Elemental-Weakness-style −15–30%, Exposure-style −10–15%, penetration ~34%, and −max-resist analogues (−9–12%), with **overcap (§8) as the buffer.**
- **NOT** D2 Conviction (−75% → a 75%-capped player to 0%). Max-resist does not protect against reduction in D2 (it caps how high you go, not how far you're reduced) — too brutal for our always-hit floor.

### 11.1 The bounded modifier-archetype enum (the answer to "test cycles or averages?")
**Neither extreme.** The resist×element grid is deterministic (§12) — analytically free, no sim. Sim is only for the **dynamic fight** (survive + kill). So:
- **Do NOT** sim every monster-element permutation (combinatorial explosion).
- **DO** define a **small fixed enum of rare/unique modifier archetypes** — exactly as D2 ships ~5 champion types + ~13 boss affixes (bounded, not combinatorial). Candidate archetypes: **resist-stripper** (Exposure-pack), **high-elemental-burst**, **all-resist-tank**, **penetration-boss**, **dual-element**. Sim each against a representative spread of player builds.
- The cycling Matt wants **IS** this enum, not a continuous space. Tractable on compute AND genre-proven.

---

## 12. Sim methodology — what is free, what must be sized

- **Deterministic (analytically free, no sim):** the full player-resist × encounter-element grid. `damage_taken = incoming × (1 − resist)` is a multiply; the §5 table in the explainer was computed by hand. The resist×reduction grid is the same.
- **Sim-required:** dynamic fight outcome (survive + kill — depends on HP/timing/rotation) against the §11.1 bounded enum.

---

## 13. Proof obligations (gandalf-owned design acceptance)

The player-experience spec — what must be **proven** before Path B is accepted (numbers are gamora's calibration under jack-ryan's gate; the *criteria* are mine):

1. **Capped players sweat-not-die against reduction packs.** A full-cap build meeting an Exposure/penetration pack should drop from comfortable to tense — never to one-shot. (PoE-layered, not D2 cap→0.)
2. **Resist genuinely competes with offense.** Full-cap measurably lowers DPS; glass measurably raises it; the §6 trade is real (not a free add, not a crippling tax).
3. **No one-shot under maximum reduction.** Stack every reduction layer on a *capped* player and they still survive a representative hit (the overcap buffer §8 is the safety margin — verify it actually buffers).
4. **Itemization choice survives calibration (§6.2).** Uniform / concentrated / full-cap remain distinct viable shapes; the reduction cycle makes each live. If calibration collapses them to one dominant shape, Path B has failed its core promise.

   **Measurable collapse-criterion (CONCERN-2 close, jack-ryan Gate-1 — so 1c Gate-2 can tell pass from fail):** the three reference shapes (uniform-under-cap / concentrated-cap-4 / full-cap-all-7) are run against the §11.1 reduction enum at calibrated budget. The discriminator has two parts:
   - **(a) Each shape is VIABLE** — all three clear the survive-AND-kill bar against the non-counter portion of the enum (i.e., each is a playable build, not a trap). The numeric survive/kill threshold is **gamora's calibration target, jack-ryan-ratified at 1c Gate-2** (it is the same survive+kill bar §13.1/§13.3 use — not a new number).
   - **(b) No shape DOMINATES** — across the enum spread, no single shape's aggregate outcome (survive-rate × clear-time, or whatever composite gamora locks) exceeds the next-best shape's by more than a **dominance margin Y**. **Y is gamora's to set and jack-ryan's to ratify** — I do not pre-set the number (per §17, calibration is gamora's). My design contract is only: *if one shape wins by more than Y on every enum archetype, the choice has collapsed and Path B §6.2 has failed.* gamora picks Y such that "meaningfully different but not strictly ordered" holds; jack-ryan gates that Y is defensible.

   The threshold-setting is **explicitly delegated to gamora's calibration with jack-ryan ratifying at 1c Gate-2** — this proof obligation gives the *shape* of the test (three reference builds, viable-AND-non-dominant) so it is no longer un-falsifiable, while leaving the magnitudes where §17 puts them.

### 13.5 The §11.3 homogenization-guard reconciliation (Gate-1 record)

Path B's headline — "every endgame player is *expected* to reach ~0.75 on all 7" (§1) — reads, on its surface, like the defensive-axis design-half §11.3 named failure ("hit 75% resist or die to everything" = a uniform, un-substitutable, build-collapsing tax). This is the obvious fair Gate-1 objection a reviewer holding the defensive-axis note in canon (jack-ryan) will raise, and it must be answered explicitly. **The resolution: Path B is guard-compliant by construction.** It satisfies both §11.3 conditions — (a) multiple defensive strategies are viable (full-cap / concentrated-cap-4 / glass per §6.1) and (b) offense partially substitutes for defense via the slot-competition the 9 resist slots impose (§7) — and it is PoE-layered (capping necessary-AND-achievable, never the D2 Conviction cap→0 one-shot floor; §11). The difference between "the §11.3 tax" and "Path B" is precisely whether capping is a *free-or-forced flat floor* versus a *costly, substitutable, non-dominant choice.* The full treatment is the reconciliation note (`2026-06-22-path-b-defensive-axis-homogenization-reconciliation.md`, commit `2543222`); its §5 adds the compound proof obligation below.

5. **The compound defensive read is not a tax** (per the reconciliation note §5, evaluated at the Step-1c / defensive-axis co-calibration). The §11.3 guard must be evaluated on the **compound** defensive demand — elemental resist (Path B) *plus* physical mitigation (the Matt-ruled `MOB_DAMAGE_SCALE` 0.40→4.0 recal) — not per-axis. Run the reference shapes across both axes: a kit may under-invest in resist OR in armor/HP and remain viable by compensating (offense, or the other axis); no (resist-floor + armor-floor) pair is strictly mandatory; offense-substitution holds against the **summed** defensive demand. If the only viable kits are those that pay both defensive axes near-fully, the compound tax has formed — calibration fails this obligation regardless of how each axis scores alone. Numeric thresholds are gamora's to set and jack-ryan's to ratify (§17); the design contract is only the *shape* — the guard is a **compound** guard now.

---

## 14. What stays UNCHANGED

- **The resist formula and both caps** (0.95 clamp, 0.80 gear ceiling). No math-model work.
- **Armor ≠ elemental** (separate axes; `armor/(armor+3000)`, K=3000, physical only). Path B does not touch armor.
- **All 7 elements every season** (no rotation/subset — Matt-confirmed; `monster_generator.py:490`).
- **The player-defender RAW / monster-defender floored asymmetry** (`combatant.py:926` / `:1104`).

---

## 15. Build sequencing

| Step | Work | Seam | Gate |
|---|---|---|---|
| **0** | **This spec** (design-of-record) | gandalf | → **jack-ryan Gate-1 DESIGN-MODE** |
| **1a** | **Sim Loadout widening 4→10** (§3.1 — schema 4→10; `_slots()` + ALL its consumers: `combined_stats`, `combined_ability_modifiers`, `combined_traits`, `total_power_score`; spirit-guide `_displaced_value` 4-name branch; enum→loadout LEGS→CHEST fold per §3.0; serialization; telemetry; loadout app) | rocket + gamora + star-lord + drax | jack-ryan Gate-2; MIGRATION.md per ADR-004 |
| **1b** | **Breadth-affix taxonomy** (dual/trio/all mint branches; Rule 1 dedupe) — *gated on 1a* | rocket | Gate-2 |
| **1c** | **Budget recalibration** (§4 ranges + offense ranges → §6/§8 targets + §13 proofs) — *gated on 1a+1b* | gamora | Gate-2; §13 proof obligations |
| **2** | **Reduction-monster cycle** (§11; the bounded enum; reduction-event telemetry) — **MATT-GATED multi-wave build** | rocket (modifiers) + gamora (sim) + star-lord (telemetry) | Matt authorization → Gate-1 → Gate-2 |

**Steps 1a–1c are one workstream** (the floor); Step 2 is a separate Matt-gated extension (the payoff that keeps the floor live). The floor without the cycle is a solved baseline — so **Step 2 is not optional to the design**, only to the *schedule* (Matt sequences when).

---

## 16. Governance — the supersession

Path B retires the locked Path A anchor ruling (`2026-06-21-typed-resistance-boss-anchor-ruling.md`; decisions-log `ea39ecc`). This must be **recorded as a deliberate pivot** so the spiky / anti-tax design does not drift back in (Discipline #13).

**Routing (recommend to KR):** KR drafts the decisions-log supersession entry → **jack-ryan reviews** → **Matt approves.** The entry states: the typed-resistance wave's anti-tax guard (max total resist 1.60 < 2.0, capping deliberately unreachable) is **superseded** by Path B (capping necessary-AND-achievable, ~9-slot cost); the dm=5.0 boss lock and swarm dm=0.20 **stand** (Path B does not touch per-hit damage); the soft-median watch-item disposition (`2026-06-21-encounter-model-firm-up-disposition.md`) **composes** — the dodge-ceiling remains the texture on top of the now-Path-B floor.

---

## 17. What's mine vs routes elsewhere

- **gandalf owns:** the design recognition, this spec, the §13 proof obligations / player-experience acceptance criteria, the §6.2 itemization-richness invariant, and the dodge-ceiling design contract when Godot combat lands.
- **Routes to gamora+rocket+star-lord+drax under jack-ryan's gate:** the sim-Loadout widening, the breadth-affix mint, the budget/range numbers, the reduction-event telemetry. **The numbers are NOT my call to set** — I set targets and criteria; calibration is gamora's.
- **Routes to KR→jack-ryan→Matt:** the §16 supersession entry.
- **Matt-gated (unchanged):** Step 2 (reduction cycle) authorization; content emission; all push; the proxy build.
- **No code touched by this spec.** Design recognition + recommendation only.
