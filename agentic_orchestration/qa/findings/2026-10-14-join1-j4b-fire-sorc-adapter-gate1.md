# Finding — 2026-10-14 — JOIN-1 J4b D2 adapter / conversion-key design note (Fire Sorceress), Gate-1 (DESIGN-MODE)

**Reviewer:** jack-ryan
**Severity:** WARN (verdict **GO-WITH-AMENDMENTS**: the design is sound; two WARNs must be folded into the J4b prereg before any adapter form or port site is built)
**Target:** engine `f72316b7`, `src/reincarnated/simulation/math/join1-j4b-d2-adapter-fire-sorc-design-2026-10-14.md` (doc-only)
**Developer:** gamora · conductor gandalf
**State checked against:** J3c CLOSED (KP-419; runtime `a0e75469`; rulebook pin `3eefaa2e`; pack v3 `2713e4cd`); Matt's J3→J4 GO (2026-10-14)
**Principles applied:** 1, 3, 5 · Disciplines #10, #12

**Ruling-dependency key.** Matt's rulings land as an addendum. Each finding is tagged with the open item it depends on:
- **[M-1]** port-emitted kit vs re-seal;
- **[M-2]** defensive sheet;
- **[M-3]** raw vs normalisation sensitivity;
- **[BLK]** shield block in or out (census Gate-2 W4, J-S3b row pin);
- **[—]** independent of all of them.

## WARN-1 [—, magnitude M-2/M-3] — The rotation policy is undefined exactly where the note predicts she lives: mana-bound

§ 1 predicts she runs dry after about 13 s and then casts at about a third duty. § 2's policy ("Meteor whenever its delay has expired, else Fire Ball") does not say what happens on a **refused** cast. Three choices are open, and each moves M-c directly:
- **(a) Meteor is refused for mana:** fall back to Fire Ball (cheaper, 20.5 vs 32.5 at slvl 32), or wait for Meteor's mana?
- **(b) A refused cast:** does it consume the cadence slot (the accumulator credit is spent, nothing is cast), or retain the credit and re-poll each world tick?
- **(c) Mana is credited between the start of a cast and its action frame:** the cost is an impulse at cast start, so does a cast in progress ever refuse?

D2 behaviour exists for each (no cast animation on insufficient mana; the client retries on input). The adapter needs a **declared, sourced-or-JUDGED rule** for all three. The row-replay instrument then checks it per cast.

*Action:* fold (a)–(c) into the prereg as policy rows. Predict the **realised Meteor:Fire Ball ratio and casts per second in the mana-bound regime**, alongside the unconstrained 1:4 at 3.125/s.

## WARN-2 [—] — Event-time discretisation: two laws in one lane, plus an unstated composition rule (KP-410's hazard class)

§ 2 starts casts from a `HitAccumulator` at h = 0.2551. § 4 converts each frame count with `ceil(frames·AS/400)`. The note does not say whether sub-event times are taken:
- from **absolute frame offsets** (relative to cast start), or
- **chained segment by segment**.

At 196 the two diverge. Meteor impact at frame 5 + 60 = 65:
- absolute: `ceil(31.85)` = **32 ticks**;
- chained: `ceil(2.45) + ceil(29.4)` = 3 + 30 = **33 ticks**.

The Meteor-delay eligibility test has the same ambiguity: action frame 5, delay 30, eligible at frame 35, so `ceil(17.15)` = 18 versus 3 + 15 = 18. That one agrees by luck.

The mana frame accumulator is specified in float (`25 · period` frames per tick), not as the integer law KP-410 established (accumulate 400 per tick, emit a frame per AS units).

*Action:* the prereg fixes one composition rule (recommended: absolute offsets from the cast-start tick, each through the integer law). It writes the regen accumulator in exact integer form, and adds both to the adapter grid. A one-tick disagreement between engine forms and port is exactly what the row replay must not have to adjudicate after the fact.

## Checks requested

**(1) The spell lane at h = 0.2551 and X = 196: SOUND [—].**
- `(25/8)/12.25` = 0.25510204…
- Effective AS 50 ≤ the Warlord's 196, so under KP-356 (ii) the world stays at 196.
- The four clock-pinned values (control fold 12.25, `player_drive` 12/24, S-11 channel parameters, S-12 enter tick) all equal their sealed values at 196, so **no rebind arises**.
- The comparison baseline is the G-D3 re-emission, engine = port bit-equal, and KP-393's re-quantisation cost does not arise.
- Declaring X = 400 as sensitivity-only is right.
- **INFO-1:** the lane is a **new** sub-1 accumulator consumer (P-2), not row 31. The discharge in (6) covers row 31, the bleed rider and the charge; P-2's own fidelity rests on the row replay.

**(2) Port sites P-1…P-8 and the KP-312 consent shape: CORRECT IN KIND [M-1].**

Each is a new sealed site, ruled at build time. The consent shape should copy KP-360/363 explicitly:
- **one** null-guarded change set (guard forms G-A/G-B);
- the predicate-at-defaults table (ADJ-J2);
- hunk-audit fail-first;
- census row additions where `_offer`/`_cons_add` lines are added;
- per-site fail-first;
- null-path T-A 25/25 + J-S8 port 7/7 at defaults;
- the KP-363 P0 inventory of pack-precomputed values bound to the **Warlord's kit**, which P-1 must leave unread under her profile;
- my delta Gate-2;
- Matt's windowed `.app` self-test.

**INFO-2:** the engine refusal of her profile needs a **named** refusal at bind (`PortOnlyKit`, the R-5 / `PortOnlyLever` analogue) with its own form test. Otherwise "the engine refuses her" is prose.

**INFO-3:** P-1 (kit replacement) also switches off S-10, the row-36 port mirror. State that under her profile `oracle_energy_cost_per_tick` is never called, rather than called with zero.

**(3) B0-N is NOT discharged for her: AGREED [—, re-minted under M-1].**
- KP-305 passed by disposition under the APPROX ceiling, explicitly provisional on the D2 mapping grade.
- Both owed items are right: the numeric re-run on the re-minted J-S4b, and the bit-exact adapter grid against legolas's tables, including the FCR 0/9/20/37/63/105/200 table and the H01/H02 sensitivity rows.
- **INFO-4:** the adapter grid needs its own **negative control**. Perturb one table cell (e.g. Meteor EMin at slvl 32 by 1/256) and show the grid goes RED. Otherwise a grid that reads legolas's tables back to itself proves nothing (#78 shape).

**(4) The d2-mana law vs row 36: SOUND [—].**
- One `resource_law` per kit, never both. Row 36 stays the Warlord's; under hers the EoR channel does not run.
- The cast refusal reuses `refuses_activation`.
- Regen per D2 frame through a frame accumulator is clock-invariant per second by construction.
- I spot-checked the regime: max mana ≈ 510–600; regen ≈ 600/120 × (1 + 3.78 + 0.25) ≈ 25/s; Fire Ball (9+32)/2 = 20.5 and Meteor (33+32)/2 = 32.5 → 114.5 per 1.6 s cycle ≈ 72/s. Mana-bound is the right expectation, which is why WARN-1 matters.
- **INFO-5:** write the regen expression's integer operation order exactly as D2MOO does (each `floor` and division placed). `floor(max_256/3000) · (100 + %)/100` is ambiguous about whether the second product is floored, and which comes first.

**(5) Predictions and directions: PREREGISTERED IN THE RIGHT FORM.** Paired totals and exact sign tests throughout, no per-cell thresholds (the J3a lesson).
- **[M-2, M-3]** The directions (M-a LOWER, M-c LOWER) are stated under § 3 option (I) and raw magnitudes. If M-2 → (II), or M-3 adds a normalisation lever, the prereg must re-state the directions **per ruling**, not carry these silently.
- **INFO-6 [—]:** define M-c's "damage dealt" exactly: **applied, HP-capped**, Σ over bodies per world tick, the same definition on both arms. The Warlord's multi-body disc and her splash then compare like for like.
- **INFO-7 [BLK]:** if Matt rules block **IN**, the census gains a row and its BOUNDARY count changes. Fraction (a) 18/18 and (b) 10/10 must then be re-predicted (19 rows; block's lever ACTIVE or a named shortfall), and under M-2 (I) block becomes a D2 defensive mechanic **on the referent's sheet**. Hold the fraction predictions until the block ruling lands.
- **INFO-8 [—]:** **L-17 `cast_move_lock` may be reached-insensitive.** The J-S8 cells run `CAMP_THEN_COLLECT`, with pure CAMP as the reported limb, so a camped player never moves and a cast-move lock is inert. If so, row 9 cannot be shown ACTIVE by a paired-total negative control. Report it as "implemented, REACHED-INSENSITIVE under the policy" (the L04-1 precedent), or state the phase in which she moves.

**(6) Routed items.**
- **Yard → metre key [—]:** a legolas question plus a JUDGED anchor with a printed sensitivity is right.
  - Add **0.9144** (the literal yard) to the 0.67 / 1.0 / 1.5 set.
  - Prefer an anchor that both games state in-world (melee reach or body collision radius: GD `meleeTargetDistance` 2.4 m against D2's melee range in yards).
  - Print the **arena margin at each value**: radius drives splash multiplicity, and so M-c.
- **OBS-1 timeout-as-terminal for joined kits [—]:** agreed as a **JOIN-only, declared clause**, on three conditions:
  1. a **negative control** that the Warlord's GD path still classes a `timeout` as `harness_error:TruncatedSalt`, so a real truncation defect is never masked;
  2. the tick cap is the referent's, unchanged;
  3. M-b counts a timed-out wave as reached-not-cleared.
- **INFO-9 [—]:** her wave-clear and killability gate must key on **her damage family's resist** (`res_fire`), not `res_physical` (J3d's `killable_under` is physical). On this board the two sets coincide: 5 (record, wave) pairs in the 248-pair population are immune to both — `trap_lightningspike_hero_a01` @152/157, `loghorrean_void` @154, `beast_bloodpool` @154/160. So no clearability difference arises **here**, but the port rule must be family-keyed, with a test. The board's `res_fire` spans −25…500 on w151–160 (250 body-rows ≥ 100 overall), so § 6's −100 floor domain check never binds.
- **Pyre overlap [—]:** model the **18 DATAMINED offsets** (recommended). "3 overlapping" is admissible only as a declared sensitivity.
- **drax's S-7 / row-36 refusal discharge [—]:** **evidenced.** S-7 and S-10 (the row-36 port energy site, KP-395) are both in the sealed diff `f414985` (my J3c close-out, collab `101638805`). L01-P (kit 196 in world 300, h < 1) ran **bit-equal on the port** at `a0e75469` (KP-413). drax should still write the one-line discharge into MIGRATION, so the refusal text stops reading as live.

## Also noted (no action)
- § 5 (no CB, no physical component, CoH life steal inert) and § 6 (fire → `Fire` on the spell lane; no armour leg; MDR/absorb absent by GD rule, declared; `UnmappedDamageFamily` refuses) are sound.
- § 10 (C-9 art timing) is presentation input. The sim-never-times-from-art rule is right.

## Action
- [ ] gamora: the J4b prereg folds WARN-1 and WARN-2 and INFO-2/4/5/6/8/9. Directions are re-stated per Matt's M-2/M-3 rulings, and the fractions are held for the block ruling (INFO-7).
- [ ] drax: MIGRATION discharge line for S-7/row 36. At build, the P-1…P-8 consent shape per (2).
- [ ] legolas / conductor: the yard → metre anchor (6).
- [ ] Matt: M-1, M-2, M-3, block (already routed). Nothing new from this gate.

## References
- engine `f72316b7` (the note); `data/kc2/pm4l_mitigation_by_body.csv` (`res_fire`, `res_physical`); pack v3 `offense_da.json` (population P); charter ledger KP-360/363/395–397/412/413/419; collab `101638805` (J3c close-out) — all read-only
