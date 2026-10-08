# Finding — 2026-10-08 — JOIN-1 J3 levers v0 design note, Gate-1

**Reviewer:** jack-ryan (DESIGN-MODE Gate-1, BLOCK authority; KP-353)

**Severity:**
- **BLOCK on two design defects** in the engine `crit_model` / scoped-lever wiring (B-1, B-2).
  - They block **J3a** and the scoped controls of **J3b** only.
  - **They lift on a doc-only addendum** carrying A-1 and A-2, plus my delta check.
- Everything else is **GO-WITH-AMENDMENTS** (A-3…A-9).
- On the five Matt items:
  - **agree:** § 4.8 (a), § 4.9 (c);
  - **agree with conditions:** § 4.2 (ii);
  - **dissent in part:** § 4.5 (S-5's framing, and the J4 consequence left unstated);
  - **dissent in wording:** § 4.1 C.
- **L-08 = `yes` ratified** in the decisions-log (§ 6).

**Target:** engine `d97e1fc0`, `simulation/math/join1-j3-levers-v0-design-2026-10-08.md` (doc-only, 359 lines)
**Developer:** gamora · **Conductor:** gandalf
**Principles applied:** 1 · 3 · 4 · 5
**Disciplines cited:** #24 · #75 (cl. 6) · #86 · R-4 (no split sources) · GL-12
**KP-346:** doc-only Gate. I read sealed code and the emitter source; no run was made.

---

## § 1 · BLOCKs

### B-1 · Row 32 cannot write `self.crit_mult`, and a rolling Soulfire form breaks the D-I11-1 purity contract (R-4, #86)

**(a) The property.** `PlayerOffense.crit_mult` is a read-only `@property` (`player_offense.py:487-489`, `return self.crit_limb.multiplier`), with no setter. § 2's mechanism ("writes the rolled multiplier to `self.crit_mult` before returning") raises `AttributeError` as written, so R-4 for the ADCtH basis has no implementation.

The leech basis reads the property after each `damage_against` call (`run.py:3090`, `:3147`). The **D-I11-1 contact instrument** reads it too (`run.py:3341`). So does the run-start copy into Soulfire (`run.py:1224`).

**(b) The pure Soulfire query.** § 2 puts the Soulfire crit roll **in row 11's form**, `SecondaryStreams.soulfire_applied`. That method is the **pure** query (its docstring says *"counting NOTHING"*). It is called both:
- from the counting wrapper `soulfire_damage_against` (`run.py:3307`, once per emitted projectile row), and
- from the contact instrument (`run.py:3346`), which deliberately uses pure queries so that measuring cannot corrupt state.

A rolling form there would **draw from `crit:soulfire` on every instrument call** and overwrite `self.crit_mult`. The instrument would then perturb the JOIN stream's sequence and the damage of the next projectile: a measurement changing the fight.

**Required (A-1):**
1. **Rolls happen only at counting sites** (one call per landed packet): row 32 `PlayerOffense.damage_against` for the player stream, and a **new row** substituting `SecondaryStreams.soulfire_damage_against` (dispatch-then-delegate) for Soulfire. **The pure forms (rows 5 and 11) never draw.**
2. **Substitute the property.** A new A-2 row installs `PlayerOffense.crit_mult` as a rulebook property:
   - it returns the per-instance stash that row 32 writes;
   - with no stash it returns `self.crit_limb.multiplier`, which is bit-equal at the default;
   - Soulfire's pure form reads its own stash the same way.
3. **Declare the contact instrument's reading.** In `independent-proc`, `run.py:3341`/`:3346` read the **last** roll of the tick, not their own contact's. State whether `note_contact` feeds any J-S8 grain:
   - if it does not, declare it a telemetry-only split under R-4;
   - if it does, the prediction must carry it.
4. **A control limb:** under NC-J3-L06-4, the `crit:soulfire` draw count equals the number of emitted Soulfire rows, **not** rows + contacts.

### B-2 · There is no lane discrimination at row 2, but L-06, L-04 and L-05 are per-lane / per-scope (A-3 schema, #86)

**The problem.**
- `threat.resolve_hit` (row 2) is reached by **both** lanes through one symbol: the monster lane from `ThreatEngine.resolve_attack` (`threat.py:1875`), and the summon lane from `SummonOffenseFold.swing` (`summon_offense.py:880`, `th.resolve_hit`).
- Both callers are **do-not-substitute** and emitter-wrapped.
- The emitter records G1 multipliers from its own `th.resolve_hit` wrapper (emitter :433-456).
- The note says "the summon roll … reaches the same form", but never says **how the form knows which lane it is serving**.

**What depends on it.** NC-J3-L06-1 (intake only), -2 (summon only) and -3 (`crit:intake`), and NC-J3-L04-2 / L05-1 / L05-2 (scoped floor and ceiling), all presuppose that it does.

**Alternatives that fail:**
- Rebinding `summon_offense.th` to a proxy would bypass the emitter's wrapper, giving a G1 false RED (R-1).
- Applying the summon crit at row 10 instead would leave G1's recorded multiplier at 1.1 while damage used 1.0. That is a split source (R-4).

**The port has no such problem:** H-3 and H-5 are separate sites. The engine is where it is unsolved.

**Required (A-2), one of:**
- **(i) Lane-by-caller (recommended).**
  - The row-2 form identifies its lane by walking the call stack: skip frames whose code is the J-S8 emitter (pinned file) or the rulebook, then match the first sealed frame's (file, qualname): `ThreatEngine.resolve_attack` gives intake; `SummonOffenseFold.swing` gives summon.
  - **Any other caller must pass `lane=` explicitly, or the call refuses (GL-12).** This includes the hit grid and the tests.
  - At GD the result is unused, so the golden master is unaffected; state that.
  - **Control:** an intake-only setting leaves every summon G1 row bit-equal, and the converse; predicted first.
- **(ii) Declare L-06/L-04/L-05 lane-global on the engine in v0,** with per-lane setting port-only, and say so on the registry rows.

---

## § 2 · Amendments (GO-WITH-AMENDMENTS)

- **A-3 · Prediction-text corrections** (they discriminate either way, but must be exact before the prereg):
  - **NC-J3-L05-2:** "tiers ≥ 105 become unreachable" is vacuous. The d100 already makes every tier above 90 unreachable (summon tier > 0 rows are all tier 2, ×1.1). The binding effect is the **1,050** summon hits with roll > 95 becoming misses.
  - **NC-J3-L04-2:** "the first G1 monster row in every cell has `pth_effective` = 90.0" holds only if that row's pth < 90 (30,950/35,165 = 88 % of rows). Write it as "the first monster row **with pth_used < 90**".
  - **NC-J3-L04-2** also removes the sub-70 damage scalar (p/70 < 1 multipliers vanish once p ≥ 90). Name it in the direction argument, since it is the dominant intake rise.
- **A-4 · NC-J3-L04-1 (floor 5) is non-movement.** Accept it as **declared REACHED-INSENSITIVE**, with reach shown at grid level (NC-H1 140/440). **The discriminating floor control is L04-2 (90)**, which must run on **both** mirrors. A floor control that cannot move J-S8 is not counted as this lever's emission control.
- **A-5 · S-5 (L-06(b) port draws).**
  - The note puts "new JOIN-only draw sites … outside any guarded branch" into **sealed** code. That conflicts with what P2 is for: in ORACLE a sealed draw site must not draw.
  - **Put the JOIN draws in the mirror** (out of tree), on a JOIN-only stream seeded `(cell seed, stream id)`, consumed in the mirror's counting forms in the same per-packet order as Python's (cross-mirror equality needs identical call order; declare it).
  - Then re-derive whether L-06(b) needs **any** sealed edit at all. H-11, H-12 and H-13 are already guarded and receive the packet. It may need only a body/tick identity passed to the existing else-branches.
  - Shrink S-5 accordingly before the ruling text is drafted.
- **A-6 · Build-order conflict.**
  - J3a claims L-06 "engine + port mirror", but the port's player-stream `independent-proc` needs S-5, which lands in J3c.
  - Either NC-J3-L06-4 is engine-only in J3a and is mirrored at J3c, or A-5 removes the dependency. Say which.
  - **The owner-eye checkpoint must say which crit controls were mirrored before it.**
- **A-7 · R-4 inventory per lever.** For each lever, list every record of its arithmetic (attribution strings, emitter recomputations, counters, contact telemetry) and state whether it follows. NC-J2-2 was found by a control; J3 should find these by inventory. Starting points:
  - L-06: G1 multiplier, the leech basis, the contact instrument;
  - L-02: the per-packet leech basis, the `n_bodies_hit` counters;
  - L-07: the immune-gate counters.
- **A-8 · P-J2-5 option (c) is calibration-first.** Before applying the "table's own decomposition (level + attribute + flat)" to the 112 absent records, re-derive DA for the **74 measured** path pairs from the same decomposition and require bit-equality (or a declared, pre-registered tolerance) against `pm4o_oa_da.csv`. A decomposition that cannot reproduce the measured rows is not evidence for the unmeasured ones. My J2 Gate-2 recorded the same trap at the WITHDRAWN board-DA reading (~1,600 DA low).
- **A-9 · R-2 draw census.** At the defaults it must hold on **both** mirrors: the port's dynamic draw census, not only the engine's. The control runs report `crit:*` / `hit:*` draw counts per cell beside the red.

## § 3 · Agreed as written

- **§ 0 and § 1** (8 ids implemented, 13 unexercised, R-1…R-6).
- **§ 3.2 L-01:** the frame-breakpoint control mirrors NC-J2-5c's observable (world clock fields only, per my D2 Gate on the P5 wording). The `kit > world` refusal stands until § 4.2.
- **§ 3.3** floor-then-ceiling ordering law, with `floor > ceil` refused.
- **§ 3.4–3.6** semantics, the synthetic-step design for L-03 (both arms stepped; only the policy flips, #24), and L-08's immune-body limb.
- **§ 4.3 defer `resolve_attack`:** AGREE. The size and instrument cost are as stated, and no witness row needs intake `post`. Intake `pre` is printed as a known limit.
- **§ 4.4 (a) H-18b in the second KP-312 commit:** AGREE. It replaces my D2-Gate declaration.
- **§ 4.7 F-J2-1:** registry ratified as the J3 default; **no stage setter in J3**. (The row-32 / `:1224` mechanics are corrected by B-1.)
- **§ 5 order J3a → owner-eye → J3b → J3c → J3d**, subject to A-6. Every step ends with J-S8 7/7 on both mirrors, § 4.7 v4 and the draw census.

---

## § 4 · The five Matt items: my position, for the conductor's sheet

| # | gamora's recommendation | jack-ryan |
|---|---|---|
| 1 · § 4.8 non-LO `crit_model` | (a) implement the alternates; the GD profile stays LO | **AGREE.** (b) is a referent change (a HALT to Matt by charter, not a lever); (c) starves the owner-eye checkpoint of the one value it exists to see. B-1/B-2 must be fixed before any of (a) is built |
| 2 · § 4.2 L-01 above the clock | (ii) the world clock follows the fastest kit; (iii) as the fallback | **AGREE, with two conditions.** **(1)** Under (ii) the WORLD is re-quantised per kit. The kit's arena margin must therefore be compared against **the Warlord re-run at the same world clock X** (`JOIN[warlord, GD]` with `world_as_pct = X`), never against J-S8 at 196. Otherwise kit and world-quantisation effects are confounded in exactly the comparison J4a reports. **(2)** The (ii) control (`world = kit = X`) and the per-tick cost at X are measured **before** J4a, and printed. The Sorceress's spell-lane cadence stays a J4b census question, not settled by (ii) |
| 3 · § 4.5 the second KP-312 ruling | S-1…S-5 + S-7 in one null-guarded commit; S-6 held; engine: no sealed edit | **AGREE on S-1…S-4, S-7, and S-6 held. DISSENT IN PART:** **(a)** S-5 is re-framed per A-5 (JOIN draws in the mirror; minimal or no sealed surface) **before** the ruling text is drafted. **(b)** The sheet must state the **J4 consequence** of "no engine sealed edit" plainly. Any joined kit whose profile sets L-02, L-03 or L-07 (e.g. the D2 Barbarian: dual-wield packets, Battle Orders max HP) is **emittable only on the port**; the engine JOIN refuses it (R-5). Its arena margin then has no engine cross-emission, only form-level grid parity. Matt should accept that knowingly. The alternative, a null-guarded engine oracle hook, would mean a re-seal and is not recommended. It should still be named as the option declined |
| 4 · § 4.1 intake order | C (a sealed law) now; A on demand | **AGREE with C, DISSENT IN WORDING.** `ARMOUR_THEN_RESIST` is **not a decoded GD law.** It is a lineage choice (R-PM4-62 part 3) over an item Lap X graded `UNREACHED-X-4`, with the fork Δ published (398.384 on a 5,000-point hit). C must read "**declared by lineage; GD's order undecoded**", printed on the fidelity table. **Reframe Matt's question:** a D2 defender has no armour-absorption stage at all (D2 defense acts on to-hit; damage reduction is a percentage). So "does a target game need resist-then-armour?" is the wrong test. J4a's **defender mapping** decides whether the order is even meaningful for that kit. Revisit then |
| 5 · § 4.9 P-J2-5 | (c) source DA for the 112, then build the guard, before J4a | **AGREE, calibration-first (A-8).** The guard alone (b) would refuse every graded run (122 absent pairs). Sourcing without calibration repeats the withdrawn board-DA error |

---

## § 5 · Verdict and path

- **BLOCK** on B-1 and B-2 for J3a, and for J3b's scoped L-04/L-05 controls. **It lifts** when gamora's doc-only addendum lands ALONE carrying A-1 and A-2 (with the A-3…A-9 corrections) and I have done a delta check of the addendum only.
- **J3b's unscoped parts** (L-01; an L-04/L-05 profile declared lane-global under A-2(ii)) may be specified in the same addendum.
- **The conductor may put § 8's five items to Matt now,** using § 4 above as the Gate's position. None of B-1/B-2 changes what Matt is asked.

## § 6 · L-08 ratification (decisions-log, engine)

**Ratified:** the declared-invented default **`yes`** (a proportional packet enters the mitigation chain).
- Every profile with L-07 ≠ `off` must **state** L-08 explicitly. An unset L-08 with L-07 on **refuses** (R-5, GL-12).
- The ratification is of the **default value**, which GD is silent on. NC-J3-L08-1 at J3c shows that the lever **reaches**; it does not and cannot validate the value.
- The witnesses' values (D2 WW, VS) are set per kit from the J4 census.

## References

- `/Users/admin/Games/reincarnated-engine/src/reincarnated/simulation/math/join1-j3-levers-v0-design-2026-10-08.md`
- sealed: `kc2/player_offense.py` :487-489 (`crit_mult` property), :512-533 · `kc2/secondary_streams.py` :262-283 (pure `soulfire_applied` vs counting `soulfire_damage_against`) · `kc2/run.py` :1224, :3070-3090, :3127-3147, :3307, :3330-3348 (the D-I11-1 contact instrument) · `kc2/threat.py` :1834, :1874-1879 · `kc2/summon_offense.py` :869-891
- emitter: `src/reincarnated/simulation/scripts/gamora_join1_gm_emit_2026_09_29.py` :423-456 (`th.probability_to_hit` / `th.resolve_hit` wrappers), :491 (summon attribution)
- prior: `…/qa/findings/2026-10-08-join1-j2-d2-delta-and-j2-gate2.md` § 2, § 7 · `…/2026-10-07-join1-j2-e4-d1-gate2.md` § 1.4 · `…/2026-10-07-join1-j2-design-gate1.md` (B-3, A-3) · decisions-log engine `506ebf0b`
