# J3 → J4 owner-eye sheet: inputs from gamora (DRAFT, for the conductor)

**Date:** 2026-10-07 · **Author:** gamora · **Status:** DRAFT input. These are not rulings. Each item gives its options, their consequences, and a recommendation.

**Occasioned by:**
- conductor KP-336;
- jack-ryan's E4 Gate-2 finding, `agentic_orchestration/qa/findings/2026-10-07-join1-j2-e4-d1-gate2.md` (`bfd5af650`), § 1.4 and § 4;
- earlier items from KP-321 (the `resolve_attack` cost) and the E2c Gate-2 (L-08), plus ADDENDUM-E1 B-3 (F-J2-1).

**Code references:**
- sealed oracle: `reincarnated-engine-join1-v311` at `969fbd8d`;
- rulebook: `reincarnated-engine-join2-rb` at `a3eb0e54`;
- J-S8 emitter: `gamora_join1_gm_emit_2026_09_29.py`.

> **Mathematical claim:** not applicable. Each option below is a route, and each route that is taken gets its own math note and Gate.

---

## 1. One home for the intake order (from NC-J2-2)

**The defect.** Today the order has two sources.
- **Rulebook side.** `intake_order_override` moves only the arithmetic inside the substituted `physical_applied` (rulebook `forms.py:101`).
- **Sealed side.** `IntakeFold.order` (`intake.py:533`) is on the do-not-substitute list. It drives the attribution text and the emitter's G2 stage map (`ph["order"] = self.order.value`, emitter `_phys`).
- **Why the obvious fix is closed.** `IntakeFold.__init__` and `IntakeFold.physical` are emitter-wrapped, so the binder cannot set the order there.
- **Status.** The operand is now labelled CONTROL-ONLY, split-source (E4 README § 7, INFO-E4-3).

**A fact that opens a cheap route.** The composition already passes the order explicitly, at construction:
- `intake_factory=(lambda: ik.IntakeFold(order=ik.OrderLimb.ARMOUR_THEN_RESIST, global_flat=True))` (e.g. `scripts/gamora_kc2_w1w2_lift_build_2026_08_25.py:172`; the v3.7 closure records this call site).
- The order is therefore a **composition operand that is already explicit**. It is not something buried inside `IntakeFold`.

| Option | What it does | Consequences |
|---|---|---|
| **A. Bind at the composition's `intake_factory`** | The JOIN binder supplies `order=ops.intake_order` to the factory's constructor argument. `IntakeFold.__init__` / `.physical` stay sealed and unwrapped by the binder. The `physical_applied` form drops its override and always takes the caller's order (it already receives `order=self.order`) | **One home:** arithmetic, attribution and the G2 stage map all read `self.order`.<br>The do-not-substitute fingerprints are unchanged, so the classifier accepts with no rule change.<br>Cost: one new A-2 row (the factory call site, a substitute row with an installed fingerprint), a math note, and a Gate.<br>Open item for the math note: pin the **J-S8 emitter's** composition route to the factory (if it builds its own factory, that is the row).<br>**Built-in control:** the NC-J2-2 re-run is predicted ROWSET-equal to the sealed NC-2 on all 7 grains, because NC-2 also sets `self.order` after init. That is the exact miss turned into a pass |
| B. Amend the do-not-substitute rule for `IntakeFold.__init__` | The binder wraps `__init__` to set `order` after construction | Two layers of wrapping on one symbol: the binder's and the emitter's (NC-2 path). The classifier has to learn a substituted-and-emitter-wrapped class for a constructor.<br>Needs a do-not-substitute amendment with a Gate (#75 cl. 6: the remedy brings its own instrument).<br>More instrument work than A, for the same result |
| C. Declare the order a sealed LAW, not a lever | Retire `intake_order_override`. `ARMOUR_THEN_RESIST` (the GD lineage) holds for every profile | Zero cost and no split.<br>The order becomes unavailable to any J4 game whose witness reads resist-then-armour. That is decided by the census, and I have not checked it |
| D. Keep it as-is (CONTROL-ONLY) | Nothing changes | Honest, but the operand stays unusable as a lever, and any profile that needs a different order has no route |

**Recommendation: A.** It is the only option that gives one home without touching the do-not-substitute list. It reuses an argument the composition already passes explicitly. It comes with a control that turns the NC-J2-2 miss into a predicted pass.
- If no J4 census row needs a non-GD order, **C is the fallback**, and A's cost is not paid.
- **The owner's question:** does any J4 target game need resist-then-armour? If none does, take C.

---

## 2. L-01: kit attack speed above the world clock (from NC-J2-5b)

**The limit.** The sealed `HitAccumulator.tick()` (`player_offense.py:288-295`) returns one boolean per world tick, gated at `run.py:2963`. When `hits_per_tick = kit_AS / world_AS ≥ 1`, it fires every tick and the excess credit is silently lost.

**What is shown.** The world/kit split (F-J2-3) is shown only for `kit_AS ≤ world_AS`, by NC-J2-5c.

**Why this matters for J4.**
- **D2 Barbarian:** IAS takes the attack rate above the warlord's 196 % basis.
- **Sorceress:** FCR is likely to as well. Caveat: FCR is a cast-rate stat. Whether it rides the kit cadence accumulator at all or needs its own spell-lane accumulator is a census question, and I have not settled it.

**A fact that frames the choice.** At the referent, **the world clock IS the kit's attack speed by construction.** `world_as_pct` is inherited from the referent kit's AS (rulebook `operands.py:40`), and the tick law is `0.16 · 100 / AS%` (`channel.py:70`). So "the world clock follows the kit" is the GD lineage itself, not an invention.

| Option | What it does | Consequences |
|---|---|---|
| **(i) Multi-hit gate** | `tick()` returns an integer number of hits (floor of credit), and the hot loop applies that many hits per tick | **Faithful at any AS.**<br>Cost: transcribing the `po_hits` consumer inside the sealed `run.simulate_wave` (the disc branch, leech basis, pet arm, per-hit crit and RNG order). That is a large, hot-loop, do-not-substitute surface needing its own Gate, and it changes intra-tick ordering (N hits at one position and one instant).<br>The port mirror (drax ADJ-5 grid) would need the same.<br>Highest cost and highest risk |
| **(ii) A world clock that follows the fastest kit** | The profile sets `world_as_pct = max(kit AS)` (the row-19 Cited route, already bindable at E4a and proven by NC-J2-5), so `hits_per_tick ≤ 1` always | **No new code path:** the route exists, and NC-J2-5 is its control.<br>One hit per tick is preserved.<br>Costs:<br>(1) **Performance:** ticks per second scale with AS. 196 % gives 12.25/s; 300 % gives 18.75/s (+53 % ticks).<br>(2) **Re-quantisation:** monster cadence, movement steps, energy regen and wave boundaries all move to a finer clock. That is a fidelity change for every other actor. It is the "whole-model perturbation" the `CadenceLimb` docstring warns about, so it must be printed on the fidelity table.<br>(3) Multi-actor compositions with different AS (summons have their own `effective_tps`) still need the split below the maximum. That is already shown to work |
| (iii) Declared ceiling | `hits_per_tick` is clamped at 1. Printed on the fidelity table: "kit AS above world AS is not represented" | Zero cost.<br>It **under-states** the fast kit's damage, leech and on-hit counts by the ratio kit/world. For the Barbarian that biases exactly the build J4 most wants to compare.<br>A variant (iii-b) scales per-hit damage by the ratio, which preserves expected linear damage, but per-hit effects (leech event count, procs, crit rolls, overkill) stay wrong. Not recommended, because it is silent in the wrong places |

**Recommendation: (ii), with (iii)'s ceiling kept as the declared fallback.**
- The world clock follows the fastest kit in the composition.
- The kit split below that is already shown.
- Performance and re-quantisation are printed as known costs. D3's per-tick performance measurement gives the real figure.
- **(i) only if** the census shows a case (ii) cannot serve: two player-side cadences, both above any single clock the owner will accept on performance.

**Required control for (ii):** a JOIN run at `world = kit = X > 196`, with a prediction committed first: G7 `tick_period_s` equals `0.16·100/X` on every row, and `hits_per_tick = 1.0` exactly.

**The port must inherit the ceiling as it is today (ADJ-5) until this is ruled.**

---

## 3. The `resolve_attack` transcription cost (KP-321; E1-b R-3)

**Why it would be needed.** Only for an intake crit stage other than `pre` (L-06 intake = `post`). The `mult` that reaches `mitigate(_im * mult)` is post-`apply_crit_reading` (threat :1879), and the only correct place to re-stage it is inside `ThreatEngine.resolve_attack`.

**Size:**
- `threat.py:1834-2272`: 439 source lines, about 210 of them code.
- 2 RNG draw sites whose order must be preserved bit for bit: the hit roll `randint(1, 100)` and the per-row chance `uniform`.
- 3 crit-premultiplied `mitigate` call sites: Life, DoT and direct.
- Branches for `n_volley`, leech, DoT and direct, plus the composition fold.

**Instrument cost:**
- a new row class, *substitute-then-emitter-wrapped* (the emitter wraps it at :474);
- the classifier's installed-fingerprint path covering an emitter wrapper around an installed object;
- its own math note and Gate;
- a golden master of `JOIN[warlord, GD]` 7/7 with the transcription installed.

**Runtime cost:** negligible, since it is the same calls.

**Risk:** the GL-12 shape. A transcription that drifts in RNG order shifts every subsequent draw, which would show as a whole-fixture RED.

**Recommendation: do not transcribe in J3 unless a census row demands it.**
- Declare intake `crit_stage = pre` for every J3 profile.
- Print it as a known limit.
- Price the transcription as above if a J4 witness needs monster crits applied after armour.

---

## 4. L-08 `proportional_damage_mitigable`: ratification

**Current state:** `yes`, PROVISIONAL (gamora). The E2c Gate agreed it as a declared-invented default; the ratification venue is J3.
- It is inert while L-07 (`proportional_damage_offense`) is `off`.
- `yes` keeps one mitigation chain, and it is the lower-damage reading.

| Option | Consequence |
|---|---|
| Ratify `yes` as the default | One chain, no unmitigable packet. Profiles with a witness value override it. Only witness-less profiles see the default |
| Ratify `no` | An unmitigable packet kind enters the chain. That is the higher-damage reading and the second chain entry (an out-of-form site, A-11 P6) |
| Per-profile only, with no default (refuse when unset) | GL-12-consistent. It forces every profile that turns L-07 on to state L-08 |

**Recommendation:**
- **Ratify `yes` as the default, AND require every profile that sets L-07 ≠ off to state L-08 explicitly.** An unset L-08 with L-07 on is refused.
- Ratify when L-07's alternate is implemented, together with its owed control: L-07 on, L-08 yes vs no, predicted RED on G2 `applied` for proportional packets only.
- Record the ratification in the decisions-log. It is not a Matt item.
- The witnesses (D2 WW, VS) set their own values from the census. I have not read those values.

---

## 5. F-J2-1: crit stage by lane, for ruling

**Current registry** (`families.py`, one home, no setter):

| Lane | Stage | Basis |
|---|---|---|
| monster→player / monster | `pre` | exercised: 148 G1 tier-2 rows, 675 G2 packets |
| player→monster / player-stream | `post` | unobservable at the referent, where crit = LO = 1.0 |
| player→monster / summon | `post` | the multiplier is exercised; the stage is ulp-inert **on the referent board only** |
| player→monster / spell | `none` | a JOIN row (D2 Sorceress census row 10) |

**Where the stage matters numerically:** only where armour overflows. NC-J2-11b shows the 138 overflow-bearing packets out of 170 physical ones.

**Items for the sheet:**
1. **Rule the registry as the J3 default** and keep the stage **not a lever** in J3: no setter. Changing intake is § 3's cost. Changing the offense lanes is cheap (the forms already carry `crit_stage`), but it is unwitnessed until GD's offense crit roll is decoded (D-L5).
2. **The player-stream lane goes live the moment J3 sets `crit_model` ≠ LO.** The J3 `crit_model` hook must install on `PlayerOffense.crit_mult` **before** the `run.py:1224` copy into `SecondaryStreams.crit_mult` (A-2 row 30), or bind both sites. That must be stated and Gated (E1-b).
3. **The summon lane's "inert" is a property of the referent board** (no body armour in (0, 195]), not of the lane. A J4 board with armoured bodies makes it live.

**Recommendation:** rule items 1-3 as written. The only owner decision is whether J3 ships a non-LO `crit_model` at all, because that alone wakes the player-stream lane.

---

## Summary for the sheet

| Item | Recommendation | Known cost |
|---|---|---|
| Intake order home | **A** (composition `intake_factory`), or **C** if no J4 game needs another order | 1 A-2 row, a math note, a Gate; NC-J2-2 re-run as its control |
| Kit AS above the world clock | **(ii)** the world clock follows the fastest kit; (iii) as the declared fallback | ticks ∝ AS (+53 % at 300 %); every actor re-quantised; printed on the fidelity table |
| `resolve_attack` transcription | **defer**; intake `pre` for all J3 profiles | about 210 code lines, 2 RNG sites, a new row class, a Gate |
| L-08 | ratify `yes` as default; L-07 on requires L-08 stated | its control when L-07 lands |
| F-J2-1 | ratify the registry; no setter in J3; the `crit_model` hook installs before the :1224 copy | none until `crit_model` ≠ LO |
