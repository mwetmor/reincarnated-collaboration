# Representative-Loadout Measurement Contract — 2026-06-16

> **STATUS:** CURRENT (load-bearing as of 2026-06-16) — see `canonical/00-ground-state.md` § 1. This is the **measurement keystone** of the authorized autonomous run (Wave 2; charter task #21). It DEFINES the canonical loadout a generated kit is *measured at* in the balance sim — closing the measurement gap (charter § 2.4) where kits enter the sim stripped of ~60–70% of their realized power.

**Date:** 2026-06-16
**Author:** gandalf (story-and-design steward)
**Status:** v1 — design contract. The measured-loadout definition is FULLY DETERMINED from existing canon (the calibration anchor is the measurement point). ONE design question is PARKED: the set-bonus *content* (4-piece full-bonus semantics) — see § 6.
**Authority:** Matt 2026-06-16 — Wave-2 keystone of the authorized autonomous run (`canonical/story/2026-06-16-engine-state-and-autonomous-run-plan.md` § 3 Blocker List A item 3, § 5.3 Wave 2). Tier-1 authoring with a Tier-3 park option per the three-tier envelope (§ 5.2 of the run plan).
**Companion docs:**
- `canonical/story/2026-06-16-engine-state-and-autonomous-run-plan.md` — the run plan; § 2.4 the measurement gap; § 3 Blocker List A; § 5.3 Wave 2.
- `canonical/41-progression-framework-2026-05-27.md` — L50 hybrid; § 1.5 endgame post-cap; § 3 node-to-level-band mapping; 70-point endgame budget.
- `canonical/51-investment-scaling-6-pattern-architecture-2026-05-28.md` — Pattern 1+2; § 3.5/§ 4.5 max-investment anchor; **§ 10.1 Option A all-skills-max; § 10.2.3 max-profile Mode A; § 10.3 the allocation algorithm.** THE load-bearing canon for the node-selection half of this contract.
- `canonical/40-gear-balance-guide-architecture-2026-05-26.md` — § 3.5 gear tier structure (T0/0.5/1/2); § 3.6 9-category × 11-slot stat surface; D33/D35/D48/D51 set + T4-attunement; D38 deferred set-bonus structure.
- `canonical/42-stat-sheet-modifier-partition-intent-2026-05-27.md` — per-slot affinity matrix (the stat surface real gear rolls on).
- `canonical/story/weapon-as-identity-surface-recognition-2026-06-14.md` — § 4 three-layer identity model; the weapon is the identity surface (Layer 1 physical/caster committed); the representative weapon is the kit's OWN `selected_weapon`, materialized at the spec'd tier.

**Code anchors (the two stopgaps this contract retires):**
- `reincarnated-engine/src/reincarnated/generation/gear_catalog.py:173` `compute_balance_gear_stats()` — the synthetic stopgap (~937 hp / ~225 armor / ~3% crit / ~150 flat-dmg), marked "Remove this block."
- `reincarnated-engine/src/reincarnated/generation/per_skill_emitter.py:232` `compute_investment_multiplier_p1()` — the Pattern-1 multiplier; read at `damage_resolver.py:792,896` off `skill.investment_points` which **defaults to 0** → kits measure at the 0.35× floor.

---

## 0. TL;DR — the contract in one frame

A generated kit must enter the balance sim **at its canonical measurement point: the fully-realized endgame build.** That point is NOT a new design choice — it is the **calibration anchor canon already locked** (doc 51 § 10.1 Option A "all-skills-max"; § 10.2.3 max-profile Mode A). The measurement seam and the calibration seam **must measure at the same point**, or the sim is calibrated against one kit and judged at another.

**The canonical measured loadout =**

1. **Skill nodes — max-profile Mode A (all-skills-max):** every active node at `NODE_MAX.active = 15` → Pattern-1 multiplier = 1.0 (no more 0.35× floor); every passive node at `NODE_MAX.passive = 5` → Pattern-2 magnitude = 1.0; the kit's algorithm-chosen T4 unlocked. This is doc 51 § 10.3 `construct_profile_distribution(K, profile=max)`.
2. **Gear — the spec'd endgame loadout:** all 11 slots filled at **Tier-1 (end-game-start) baseline**: a **Legendary T1 main-hand weapon** that IS the kit's own `selected_weapon` (the identity surface), plus a **4-piece Set** (2pc + 4pc bonuses active) occupying 4 of the armor/accessory slots, with the remaining slots filled by Tier-1 legendaries. Gear rolls on the doc 42 affinity matrix; this retires `compute_balance_gear_stats`.
3. **Measurement semantics — a SINGLE canonical point, deterministic + reproducible.** The measured loadout is ONE construction (max-profile Mode A + Tier-1 spec'd gear), not a set. The multi-profile *set* (low/mid/max/mixed) belongs to the Phase-4 *calibration sweep*; the *measurement* the gauntlet verdicts read is the single max-point. Rationale: § 4.

**Why this is the keystone:** the rogue's "~192 mean damage / zero kills vs a 123,356-HP boss" was a kit measured at ~30–40% power (0.35× damage floor + synthetic gear). No deletion (1D / b6) may fire on stopgap-loadout evidence; cond.5 boss re-validation MUST run on this loadout to be trustworthy (run plan § 5.2 Tier-2).

---

## 1. The principle — measure at the calibration anchor

### 1.1 The single load-bearing rule

> **The point a kit is MEASURED at must equal the point the kit is CALIBRATED at.**

Doc 51 § 3.5 + § 4.5 lock the calibration anchor at **max-investment**: "the cohort_median KPM at the max-investment profile (15/15 active; 5/5 passive; T4 chosen) lands on the doc 50 § 4 five targets." Doc 51 § 10.1 resolves *which* max-investment construction: **Option A, all-skills-max** (gandalf recommendation, ratified path). Doc 51 § 10.2.3 names it **max-profile Mode A**.

The measurement gap (charter § 2.4) is precisely a **calibration/measurement mismatch**: gear is being calibrated toward an endgame target, but kits are measured at *implicit-no-investment + synthetic-stopgap-gear*. The sim is judging the wrong kit. This contract makes the measurement point coincide with the already-locked calibration point. **It introduces no new design surface for the node half** — it operationalizes existing canon for the measurement seam (doc 51 § 10.3 was authored for the Phase-4 *sweep*; this contract names the *measurement* consumer of the same algorithm).

### 1.2 Why max, not midpoint or realistic (the canon already argued this)

Doc 51 § 3.5 + § 10.1 settled the "why max" debate; this contract inherits it rather than re-litigating:

- **Max-investment is the endgame player profile** (doc 51 § 3.5) — doc 50's bounded-viability band is defined for the endgame-realized cohort. The gauntlet's job is to certify *the kit at its full power*, then bounded-viability guarantees the sub-max journey toward it stays in-band via the Pattern-1/2 floors.
- **Midpoint anchor would force endgame players above the band** (doc 51 § 3.5) — wrong player-consequence semantics.
- **Mode A (all-skills-max) over Mode B (realistic specialization)** for the measurement point: Mode A is a *single canonical construction* (doc 51 § 10.1 rationale 4: "the reference baseline at the max-end of the profile axis MUST be a single canonical construction"). Mode B introduces a per-build specialization-pattern axis — fine for the Phase-4 variance *check*, wrong for the *measurement* that must be deterministic + reproducible (§ 4).
- **Genre precedent** (doc 51 § 10.1 rationale 3): PoE balances against "every gem L20 + 23% quality"; D2 LoD against "all synergies L20"; Last Epoch against max-rank-per-skill. The genre's calibration anchor is the structural ceiling, not the realistic mid-build. Reincarnated joins the convention. **The measured loadout is the spreadsheet ceiling — the "ideal build the player aspires toward" (doc 51 § 10.1 rationale 5).**

---

## 2. Skill-node selection — the canonical measured node-set

### 2.1 Definition (max-profile Mode A; doc 51 § 10.2.3 / § 10.3)

The measured kit's node investment is the output of `construct_profile_distribution(K, profile=max)` with the Mode A branch:

```
For each active skill node S in kit K:        S.investment_points          = NODE_MAX.active  = 15
For each passive node P in kit K:             P.investment_points_passive  = NODE_MAX.passive = 5
For the kit's single algorithm-chosen T4:     T4.unlocked = True
```

**Construction property (doc 51 § 10.3 step 5; the whole point):**

```
Pattern 1 (active):  damage_multiplier_at_points(S, 15) = base_at_max × (0.35 + 0.65 × 15/15) = base_at_max × 1.00
Pattern 2 (passive): effect_magnitude_at_points(P, 5)   = base_at_max × (0.50 + 0.50 × 5/5)   = base_at_max × 1.00
```

At the measured loadout, both investment multipliers are uniformly **1.0** — the kit's damage is its `base_at_max`, not the 0.35× floor it currently suffers. This is the Discipline #47 § 7.2 max-investment proof; specialization peaks then emerge **solely from `base_at_max` distribution** across skills/encounters, NOT from investment scaling. That is doc 50's load-bearing "specialization-as-emergent-property" principle (doc 51 § 10.1 rationale 2).

### 2.2 What "15 points" means — the cap, not a budget

The charter asks: "Is it 15 points = the investment cap that yields the 1.0× multiplier?" **Yes, and a clarification the contract must make explicit:** `15` is the **per-node cap** (`NODE_MAX.active`), not a per-kit budget. Mode A sets *every* active node to its 15-cap and *every* passive node to its 5-cap simultaneously — this is the all-skills-max *counterfactual ceiling* (doc 51 § 10.1: "if every skill were maxed simultaneously, where would the kit's KPM land?").

This is deliberately ABOVE the realistic ~70-point endgame budget (doc 41; D71) — and that is correct for the *measurement* anchor. The realistic budget governs *play* (the player distributes ~70 points across nodes); the calibration/measurement anchor governs *the ceiling the band is defined against*. Doc 51 § 10.1 rationale 3 ("calibration ≠ play") makes this distinction load-bearing genre canon: the budget bounds what a player *achieves*; the all-skills-max ceiling is what the kit is *balanced against*. Measuring at the ceiling, with bounded-viability floors (Pattern-1 0.35 / Pattern-2 0.50) guaranteeing the sub-ceiling journey stays in-band, is the design.

### 2.3 T4 selection at the measured point

The kit's **single algorithm-chosen T4 is unlocked** (Mode A; D66 active-identity discipline — ONE T4 at a time). The measured loadout does NOT sweep all T4 variants — that is the Phase-4 T4-identity-cycling sweep (doc 51 § 10.7). For the deterministic measurement point, the canonical T4 is the kit's **primary/algorithm-default T4** (the one rocket's T4 algorithm scored highest for the kit). If a kit's design ships multiple in-band T4 variants (doc 51 § 10.8 strip-and-ship), the measured loadout uses the **primary** variant; per-variant measurement is a separate downstream concern, not the keystone measurement point.

---

## 3. Gear — the canonical measured loadout

### 3.1 The spec'd loadout (retires `compute_balance_gear_stats`)

All **11 slots** (doc 40 § 3.6: 1 main-hand + 1 off-hand + 5 armor + 4 accessory) are filled. The measured tier is **Tier-1 (end-game-start)** as the contract baseline — the tier at which sets unlock (doc 40 § 3.5: "Set items ✅ unlocked at Tier 1") and at which all 4 legendary tiers enter the drop pool. Tier-1 (not Tier-2) is the contract baseline because Tier-1 is the **entry into the endgame band** (doc 41 § 3: T1 dominant at L30-45 endgame-start) — it is the floor of "fully-realized endgame," which is the right measurement anchor for the bounded-viability band (over-anchoring at Tier-2 godlike-gear would inflate the band ceiling beyond the 85th-percentile target, doc 40 § 4).

| Slot family | Slots | Measured-loadout content |
|---|---|---|
| **Weapon (main-hand)** | 1 | **Legendary T1 — the kit's OWN `selected_weapon`** (the identity surface; § 3.3) |
| **Off-hand** | 1 | Legendary T1 (or Set piece if the set spans off-hand) per the kit's weapon profile |
| **Armor** | 5 (head/chest/hands/feet/legs) | **4-piece Set** occupies 4 of the {5 armor + 4 accessory} slots; remaining armor slots = Legendary T1 |
| **Accessory** | 4 (amulet/ring×2/belt) | balance of the loadout = Legendary T1 |

**The 4-piece Set occupies 4 of the 9 non-weapon slots; the other 5 non-weapon slots + off-hand are Tier-1 legendaries.** Set + legendary together fill all 11 slots. This is the spec'd "Legendary T1 + 4-piece Set" the charter names.

### 3.2 Stat surface — gear rolls on the affinity matrix, not flat scalars

The synthetic stopgap supplied 4 flat scalars (bonus_hp / bonus_armor / bonus_crit / bonus_damage_flat). The real measured gear rolls on the **doc 40 § 3.6 9-category × 11-slot affinity matrix** operationalized in **doc 42** — primary ~50% / secondary ~30% / tertiary ~15% / off-affinity ~5% per slot per category, resource-model-gated (doc 40 § 3.6 principle 3), with the no-skill-modifier rule (principle 5: gear NEVER adds +levels to chain skills; capability toolkit adds triggered-passives / rare true-actives only). The Legendary differentiator is modifier-surface expansion (doc 40 § 3.4 / D56), not scalar inflation.

**T4-attunement at the measured point:** the Legendary T1 weapon + the Set carry T4-attunement (doc 40 D51: tier 1+2 legendaries + all sets). Per the content-compositional model (D33), attunement is *metadata recording generation-time alignment* — the gear's *content* (passives, weapon specs, set bonuses) IS the attunement. The measured loadout's gear content is aligned to the kit's chain + algorithm-chosen T4 (so the measured kit's gear *reinforces its own build*, not a random roll — this is what a realized endgame player would have assembled).

### 3.3 The weapon IS the kit's identity surface (not a generic stat-stick)

Per `weapon-as-identity-surface-recognition-2026-06-14.md` § 4: the weapon is the **Layer-1 identity surface** (physical/caster — committed, proxy-rooted). The measured main-hand is therefore **not a generic "best weapon"** — it is the kit's **own `selected_weapon`, materialized as a Legendary T1.** The weapon-as-ENVELOPE mechanism (§ 6-ter-amendment) means the weapon gates the kit's geometry sub-palette; measuring the kit on a *different* weapon would measure a different kit. The contract is explicit: **the representative weapon = the kit's selected weapon at the spec'd Legendary T1 tier, carrying its weapon-derived geometry/range/tempo + its kit-aligned legendary capability.**

This also closes a latent honesty gap: kit identity lives in the physical/weapon envelope (recognition § 3); a measurement that strips the weapon to a synthetic stat-block was measuring the kit *without its identity*. The real-weapon measurement restores it.

---

## 4. Measurement semantics — SINGLE canonical point

**Decision: the measured loadout is a SINGLE deterministic, reproducible construction — NOT a representative set.**

The charter asks whether the measured loadout is one point or a small set. It is **one point: max-profile Mode A + Tier-1 spec'd gear (§ 2 + § 3).** Rationale:

1. **Determinism + reproducibility are non-negotiable for the gauntlet verdict** (charter task #21 §3: "the sim needs a deterministic, reproducible 'measured loadout' definition"). A *set* makes "did this kit pass?" ambiguous (pass at which point? all? median? worst?). A single point makes the verdict unambiguous.
2. **The multi-profile SET already exists — and it is a different seam.** Doc 51 § 10.2 (low/mid/max/mixed) + § 10.3 + § 10.7 (T4 cycling) define the **Phase-4 calibration sweep** — a multi-cell space (paths × cohorts × encounter_types × investment_profiles, doc 51 § 12.5) that *validates the band holds across profiles*. That sweep is the *set*. The **measurement point** this contract defines is the *single max-end* of that sweep's profile axis — doc 51 § 10.1 rationale 4 explicitly requires "the reference baseline at the max-end of the profile axis MUST be a single canonical construction."
3. **Separation of concerns:** the gauntlet *measures* a kit at the single max-point (this contract); Phase-4 *calibration* sweeps the multi-profile set to verify the floors (doc 51 § 10.2). The keystone re-measurement (re-run the rogue + gauntlet on real loadouts) uses the single point. Bounded-viability's sub-max guarantees come from the Pattern-1/2 floors + Phase-4 sweep, NOT from the gauntlet measuring multiple points.

**The DoT-bridge / Mode-B realistic variance** (run plan § 5.4; doc 51 § 10.2.3 Mode B) remains a *check* run in the Phase-4 sweep — it does not re-anchor the measurement point.

---

## 5. Composition with the deletion gates (why this is upstream)

Run plan § 3 Blocker List A: the representative-loadout fix (item 3) is **upstream of trustworthy 1D-deletion (item 2 / W-F cond.5)** and **upstream of b6-deletion** (run plan § 5.2 Tier-2: "b6 deletion fires when the envelope hits b6-parity boss efficacy, **re-measured on real loadouts**").

- **cond.5 boss re-validation MUST run on this loadout.** A defensive-bridge boss validated against a 0.35×-damage / synthetic-gear kit proves nothing. Tier-2 1D-deletion auto-fire is gated on "cond.5 runs on real loadouts" — i.e., on this contract being materialized + wired.
- **Option 1 (envelope-vs-b6 boss-efficacy diff) re-measures on real loadouts** (run plan § 5.3 Wave 4). The b6-parity question — "does the envelope composer reach b6's boss efficacy?" — is only answerable when both are measured at the same real loadout. b6 is the answer key; the answer key and the candidate must be measured at the same point. This contract supplies that point.

**Discipline:** no deletion may fire on stopgap-loadout evidence (run plan § 2.4). This contract is the precondition for *trustworthy* deletion evidence.

---

## 6. PARKED design question (Tier-3) — the set-bonus CONTENT

**The node-selection half (§ 2) and the gear-tier/slot/weapon half (§ 3.1, § 3.3) are FULLY DETERMINED from canon.** One genuine design question is **parked** rather than invented:

### 6.1 The parked question

> **What is the CONTENT of the 4-piece set bonus the measured loadout wears — the actual 2pc + 4pc bonus effects (and their magnitudes) — and is it a fixed canonical set per kit, or a kit-aligned generated set?**

**Why this is genuinely under-determined (not authoring laziness):**
- Doc 40 **D35** locks the *structure*: "4-piece sets standard; 2pc minor bonus (always-active) + 4pc full bonus (content composed with chain + T4)."
- Doc 40 **D38** explicitly DEFERS the *content*: "T4-attuned gear architectural specifics (attunement magnitudes, cross-rarity distribution, **set bonus structure**, binary vs graduated)" — listed as a deferred decision point.
- Doc 40 § 6.5 / the set-bonus line (`§ around line 527`): "Set bonus structure (2pc/4pc/full bonuses; T4-attunement granularity within sets) — **implementation territory**."

So the *slot count* (4-piece) and the *presence* of 2pc/4pc bonuses are canon (§ 3.1 uses them safely). But the **bonus content + magnitude** — what the 4pc *does*, and how strong — is canonically deferred. The measured loadout needs the set's *stat/capability contribution* to be a concrete number for the sim, and that number is a real design decision (a strong 4pc bonus materially shifts the measured kit's power → shifts the bounded-viability band the gauntlet judges against).

### 6.2 The two sub-options (for Matt; do NOT auto-pick)

| Option | Description | Trade-off |
|---|---|---|
| **6a — Generated kit-aligned set** | The measured set is GENERATED per kit (rocket's gear strategy registry produces a set spec aligned to the kit's chain + T4, like the legendary it sits beside), with 2pc/4pc bonuses drawn from the doc 40 § 3.3 capability toolkit at set-density (D54: sets concentrate via multi-piece commitment). | Substrate-honest + per-kit-coherent (the set reinforces the kit's own identity). BUT requires the set-bonus generation spec (D38) to land first → couples this keystone to a deferred design surface. |
| **6b — Fixed canonical "reference set" for measurement** | A single fixed reference-set stat contribution (a designed 2pc + 4pc magnitude profile) used uniformly for the measurement point — a *measurement instrument*, not a shipped item. The shipped per-kit sets are a separate downstream concern. | Unblocks the keystone NOW (no dependency on D38); deterministic + reproducible. BUT the measured kit wears a generic set, slightly less identity-coherent than 6a (mitigated: the *weapon* still carries identity per § 3.3, so identity is not lost — only the set is generic). |

### 6.3 gandalf's lean (a recommendation, NOT a ruling)

**Lean toward 6b for the keystone, with 6a as the eventual shipped form** — i.e., decouple the *measurement instrument* from the *shipped set generation*. The keystone's job is to make the sim measure the *right power level*; a fixed reference-set magnitude profile (calibrated so the 11-slot loadout lands at the spec'd Tier-1 endgame power) achieves that without waiting on D38. The per-kit generated set (6a) then lands as a refinement when the set-bonus generation spec is authored, and the measurement instrument is swapped for the real generated set at that point. This honors recognition→validate→commit: commit the measurement-unblocking instrument now; commit the substrate-honest generated set when D38's design surface is ready. **But the magnitude of the reference set IS a design call** (it sets the band ceiling), so it parks for Matt.

**This is the only Tier-3 park.** Everything else in this contract is determined.

---

## 7. Acceptance hooks for the downstream seams

### 7.1 rocket (generation seam) — materialize real gear; retire the stopgap

1. **Materialize the Legendary T1 main-hand = the kit's own `selected_weapon`** at Legendary T1 tier, carrying its weapon-derived geometry envelope (weapon-as-ENVELOPE, recognition § 6-ter-amendment) + a kit-aligned legendary capability from the doc 40 § 3.3 toolkit (T4-attuned per D51).
2. **Materialize the 11-slot legendary loadout** filling all non-set slots with Tier-1 legendaries rolling on the doc 42 affinity matrix (resource-model-gated; no-skill-modifier rule; modifier-surface expansion over scalar — doc 40 § 3.4).
3. **Materialize the 4-piece Set** per the § 6 disposition (6a generated OR 6b reference-set — **awaits Matt's § 6 call**; if 6b, rocket consumes a fixed reference-set magnitude profile; if 6a, rocket's set-gen spec must land first).
4. **Retire `compute_balance_gear_stats()`** (`gear_catalog.py:173`) — the "Remove this block" stopgap. The real 11-slot loadout supplies hp/armor/crit/damage *and* the full 9-category surface, not 4 flat scalars.
5. **Acceptance:** the materialized loadout, summed across 11 slots, lands the kit at the spec'd Tier-1 endgame power profile (gamora validates against doc 50 band at the measured point). jack-ryan Gate-2 on the gear-materialization commit.

### 7.2 gamora (simulation seam) — wire the measured loadout into the sim

1. **Set `skill.investment_points`** for every active node to `NODE_MAX.active = 15` and every passive node's investment to `NODE_MAX.passive = 5` at the measured-loadout construction point (doc 51 § 10.3 `construct_profile_distribution(K, profile=max)`, Mode A branch). This makes `compute_investment_multiplier_p1` (`per_skill_emitter.py:232`, read at `damage_resolver.py:792,896`) return **1.0** instead of the 0.35× floor.
2. **Unlock the kit's algorithm-chosen T4** (Mode A; D66 one-T4-at-a-time; § 2.3 primary variant).
3. **Consume the real materialized gear** (rocket § 7.1 output) in place of `compute_balance_gear_stats` at all five `balance_loop.py` call sites (`:2880, :2939, :3218, :3663, :3810`).
4. **Determinism guarantee:** the measured loadout is a single reproducible construction (§ 4) — same kit → same measured loadout → same verdict. No profile sweep at the gauntlet *measurement* point (the sweep is Phase-4 calibration, separate).
5. **Re-measure the rogue + gauntlet on the real loadout** (run plan § 5.3 Wave 2 close) — the "~192 mean damage / zero kills" verdict re-runs at full power; the re-measured result is the trustworthy baseline for cond.5 + Option 1.
6. **Acceptance:** the re-measured kits enter the doc 50 bounded-viability band at the measured point; cond.5 boss re-validation (run plan § 5.2) runs on THIS loadout; jack-ryan Gate-2 + gandalf design-endorse on the wire.

### 7.3 Sequencing note (for KR)

- § 7.1 (rocket materialize) and § 7.2 step 1-2 (gamora node-wire) are **partially parallel** — gamora can wire the node-investment half (which depends only on doc 51 § 10.3, already canon) while rocket materializes gear; they contend only at § 7.2 step 3 (consuming real gear) + step 5 (re-run). Matches run plan § 5.3 ("they contend only at the final wire + re-run").
- The § 6 park (set-bonus content) **does not block** the node-investment wire (§ 7.2 step 1-2) or the legendary/weapon materialization (§ 7.1 step 1-2). It blocks ONLY the set-piece materialization (§ 7.1 step 3). If Matt rules 6b, rocket proceeds with the reference-set immediately. The keystone can advance to ~90% on the determined parts while the set-content park resolves.

---

## 8. Predictions registered (for empirical validation)

Per recognition→validate→commit, the contract registers predictions the re-measurement will confirm or falsify:

1. **The re-measured rogue clears the boss (or comes far closer) on the real loadout.** At 1.0× damage (vs 0.35×) + real Tier-1 gear, the rogue's effective power is ~2.5–3× the stopgap measurement. The "zero kills" verdict is predicted to be a measurement artifact, not a kit deficiency — at least partially. (If the rogue STILL fails at full power, that isolates a *real* kit-composition deficiency — which is exactly the b6-parity question Option 1 investigates; either outcome is informative.)
2. **The bounded-viability band, re-measured at the real loadout, shifts upward** but the cross-path variance (doc 50 Target 1, ≤1.5×) holds — because Mode A's uniform 1.0× multiplier means specialization peaks come from `base_at_max` distribution, which the calibration already shaped.
3. **cond.5 boss re-validation on the real loadout produces a different (trustworthy) verdict** than it would on the stopgap loadout — strong enough to gate the Tier-2 1D-deletion auto-fire honestly.

**Empirical gate (NOT time-passage):** these resolve the moment gamora re-runs the rogue + gauntlet on the materialized real loadout (run plan § 5.3 Wave 2 close).

---

## 9. Sign-off

**Author:** gandalf (story-and-design steward)
**Status:** CURRENT — the measurement-keystone design contract. Node-selection + gear-tier/slot/weapon halves FULLY DETERMINED from canon (doc 51 § 10 + doc 40 § 3.5 + recognition § 4). ONE design question PARKED (§ 6: set-bonus content — 6a generated vs 6b reference-set; gandalf leans 6b-for-keystone / 6a-as-shipped, magnitude is Matt's call).
**Composition:** with the run plan (§ 3 keystone), doc 51 (the calibration anchor = the measurement point), doc 40/42 (gear surface), doc 41 (L50 endgame framework), the weapon-as-identity recognition (the weapon is the measured kit's identity surface).

**For:** the canonical definition of the loadout a generated kit is MEASURED at in the balance sim — closing the calibration/measurement mismatch (charter § 2.4) so that no deletion (1D / b6) fires on stopgap-loadout evidence and cond.5 boss re-validation runs on the real kit. The measured loadout = max-profile Mode A skill investment (all nodes at cap; investment multipliers uniformly 1.0) + Tier-1 spec'd gear (the kit's own Legendary-T1 weapon as identity surface + a 4-piece Set + Tier-1 legendaries filling all 11 slots), as a SINGLE deterministic reproducible point. Acceptance hooks defined for rocket (materialize + retire `compute_balance_gear_stats`) and gamora (wire 15/5 node investment + real gear + re-measure). Set-bonus content parked for Matt.

**Signed:** gandalf (story-and-design steward), 2026-06-16.
