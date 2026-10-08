# Finding — 2026-10-08 — JOIN-1 J3b levers prereg (L-01 / L-04 / L-05), DESIGN-MODE delta

**Reviewer:** jack-ryan
**Severity:** WARN (verdict **GO-WITH-AMENDMENTS**: one prereg amendment, alone, before the fail-first tests)
**Target:** engine `9bd4e840`, `src/reincarnated/simulation/math/join1-j3b-levers-prereg-2026-10-08.md`; against design `join1-j3-levers-v0-design-2026-10-08.md` (§§ 4.2, 4.4), ADDENDUM-E1 rows 19/22, and KP-356 (ii)
**Developer:** gamora · conductor gandalf (KP-386)
**Principles applied:** 1, 3, 5 · Disciplines #10, #12

## WARN-1 — The ordinary (ii) case, kit < world, has no control, and two definitions are open there

Under (ii) the harness sets the world to the fastest kit. **Every slower kit, including the Warlord re-run at X (G-D4 @ X), runs at `hits_per_tick = kit/world < 1`.** That is the configuration J4a's comparisons actually use. The prereg tests:
- kit = world = 300 (L01-W);
- kit > world (L01-K, a refusal);
- kit = world = 196 with a table (L01-1).

The nearest prior coverage is NC-J2-5 (world 200, kit 196, giving 0.98). It was G7-only and directional.

**Open definitions:**
- (a) **`acc_bound`** is said to be "empty at GD". But at GD with kit < world, row 31 (ADDENDUM-E1 row 22) *does* build `HitAccumulator(196/300)`. State whether `acc_bound` counts GD-model accumulators. I recommend it does, keyed by the bits of `hits_per_tick`.
- (b) **`frame-breakpoint`** maps the kit's AS **directly to `hits_per_tick`**, so the world AS never enters. That is right only when world = 196. Define the composition: for example, the table yields the kit's *effective* AS, and `hits_per_tick = eff/world`, still ≤ 1. Otherwise the same table means different things in different comparison sets.

**Action:** add **NC-J3-L01-P**: world 300, kit 196, GD model.
- G7 `tick_period_s` == `channel.tick_period_s(300)` on every row.
- `acc_bound` == {repr(196/300): n} with n == the instances built.
- Paired total: Σ player-hit events per world tick < the L01-W run's.
- Mark it **owed before J4a**, beside L01-W.

## INFO-1 — The L01-W oracle twin is a valid comparator, on conditions

- With world = kit, the sealed oracle cannot separate the two either (ADDENDUM-E1 F-J2-3). So a sealed run with `FIXTURE_ATTACK_SPEED_PCT = 300` is the right identity: it shows the rulebook at world = kit = X adds nothing beyond row 19.
- **Conditions:**
  - the twin is produced by an in-process constant override in a child, never by editing `simulation/kc2/**` (the deny rule);
  - it is written to its own directory, labelled `ORACLE-TWIN@300`, and never to the J-S8 fixture or golden master;
  - it is **not a fidelity claim about GD at 300 %**. AS-measured data tables (for example the swing-pause JSON) are identical on both sides. The equality tests reach, not realism.
- Say so in § 5.

## INFO-2 — Deferring H-18b is sound for the engine, and binds J3c

- `run.py:3312` gates the bleed rider on `po_hits`. **Verified.** So the engine controls are faithful.
- The port's `_secondary_streams(disc_hits)` is ungated (design § 4.4). **Any port run with `hits_per_tick < 1` diverges**: L01-1, L01-P, and every kit < world comparison, G-D4 @ X included.
- J3c's pin text must carry: *port refuses `hits_per_tick < 1` until S-7 lands in the KP-312 change set.* L01-W (exactly 1) is port-safe.

## INFO-3 — The semantic-shift declaration is adequate. Name what it retires

The `KitAboveWorldClock` refusal is correct fail-closed behaviour under (ii), and it is declared as #12.

Add:
- **NC-J2-5b is retired** as a runnable control and superseded by NC-J3-L01-K. Its J2 evidence stays historical.
- The fail-first commit updates any test still asserting the old saturation.
- **Grep callers that set kit > world**, so none breaks silently in a harness.

## INFO-4 — Row 35's other readers: correctly listed, with one report field that will mislabel

`threat.PTH_MINIMUM` is read at `threat.py:396` (replaced by the row-2 form), `:2325` (the wire) and `player_kit_residual.py:621`.

The last one feeds a **report-only** `holds` boolean (`pth_base >= PTH_MINIMUM`). Under any floor above the board minimum of 103.54 it flips to `false`, which reads like a failed player-path check. Declare it in A-7. The player lane itself is safe: `crit.offense_p` reads `ops.pth_minimum`.

## Confirmed (no finding)

- **Predictions are falsifiable and pre-registered:**
  - directions on paired Σ (L01-1 c/d, L04-2 d, L05-2 b), with the sign test reported only (INFO-2 applied);
  - per-row law checks and first-divergence identities are deterministic;
  - L05-1 honestly predicts no direction (18 hits);
  - L04-1 is declared reach-insensitive.
- **The refusals fail closed at the right points:**
  - `KitAboveWorldClock`, `FloorAboveCeiling` and `UnknownLaneCaller` at bind;
  - `SplitRecordRefused` per call;
  - `OffenseFloorUnbuilt` keeps the player lane out of J3b.
- **No ORACLE / PLAY / J-S8 leak at defaults:**
  - lever operands are profile-level, not pack `_FIELDS`;
  - certification at defaults requires J-S8 7/7, 0 JOIN draws, empty `acc_bound`, § 4.7 v4 and P-J2-9;
  - all binder mutations are in-process;
  - PLAY is touched only by J3c under KP-312.

## Action
- [ ] gamora: prereg amendment, alone, folding WARN-1 (L01-P, the `acc_bound` definition, the frame-breakpoint composition with world) and INFO-1…4. Then fail-first.
- [ ] conductor: carry INFO-2's port refusal into the J3c pin text.
- [ ] Matt: none.

## References
- engine `src/reincarnated/simulation/kc2/run.py:3300–3318`, `threat.py:339/396/2325`, `player_kit_residual.py:605–622` (read-only)
- engine design `join1-j3-levers-v0-design-2026-10-08.md` §§ 4.2, 4.4; `join1-j2-rulebook-v0-design-2026-10-07-ADDENDUM-E1.md` rows 19, 22, F-J2-3
