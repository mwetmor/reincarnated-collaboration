# Finding — 2026-10-07 — JOIN-1 J2 rulebook v0 design note, Gate-1

**Reviewer:** jack-ryan (DESIGN-MODE, Gate-1 peer critic with BLOCK authority)
**Severity:** **BLOCK** on three design defects (B-1, B-2, B-3). **The BLOCK lifts when the J2-E1 addendum lands ALONE carrying amendments A-1…A-13 and I have done a delta check of that addendum only.** The addendum is the note's own § 4.1 slot, before any code. Everything else is **GO-WITH-AMENDMENTS**. Option B, the out-of-tree binder with no oracle edit, is **sound as an architecture and is endorsed**. The defects are in how it is wired and how it is witnessed, not in the choice.
**Target:** engine `285a2364` · `simulation/math/join1-j2-rulebook-v0-design-2026-10-07.md` · FILE `a7fa8d4401e733c795df993e6273e288fc1e9bee6de4e917d76dd79ccd01c181` (derived this Gate; equals the ledger's `a7fa8d44…`)
**Developer:** gamora (oracle) · downstream star-lord (pack) and drax (port)
**Conductor:** gandalf (JOIN-1 RUN-CONDUCTOR), ledger KP-315
**Principles applied:** 1 (math before code) · 3 (cross-seam impact) · 4 (decisions-log and ledger as truth) · 5 (severity) · 6 (cross-seam round trip: pack and port)
**Disciplines cited:** #3 · #12 · #24 · #73 · #75 (cl. 6) · #86 · ADR-002 · ADR-004

---

## Pins derived at this Gate (none carried)

| artifact | value | label |
|---|---|---|
| engine HEAD | `285a2364d56fc4d7e9476dba7e49fd2a39f90040` | COMMIT |
| `simulation/kc2` at HEAD and at `285a2364` | `7496a28a9126be568a2ee714d3f8f5e5dbc17af7` | GIT TREE OID |
| sealed worktree `reincarnated-engine-join1-v311` HEAD | `969fbd8d3cb7d07d05c22c80ee925dd34444118c` | COMMIT |
| J-S8 oracle half `join1-gm-fixture-v1/oracle/manifest.json` | `f82807fb6de68a6cee4eff69bb7028457143b4951fe9abccee94caa735c4d217` (equals note R-3) | FILE |
| J-S8 oracle `G1.jsonl` | `eb335ebabffb87960629f1dd24410bad32d7bd3230bcb11edd58b04324b68600` | FILE |
| G1 population census (this Gate, from that FILE) | monster: 8,019 miss · 26,998 hit ×1.0 · **148 hit ×>1.0** · summon: 18,999 hit ×1.0 · **2,347 hit ×>1.0** · 0 summon misses | derived |

---

## § 0 · Verdict in one table

| # | Gate question | Verdict |
|---|---|---|
| 1 | Out-of-tree binder: sound and auditable? Does the emitter observe JOIN as it observes ORACLE? | **Architecture sound. Two BLOCKs on the wiring.** **B-1:** as laid out, the FILE-pinned emitter cannot run JOIN at all. **B-2:** the substitution set is not closed, and the alias-scan claim is true only because of that. WARN on Limb B′ scope (A-4) and on reach-probe sensitivity (A-5) |
| 2 | FORM/OPERAND inventory complete vs the P0 and Sorceress censuses? | **No crosswalk; six gaps (A-7).** WARN |
| 3 | Inherited items (D-1/C-1, RAW_EXPECTATION, INFO-C1 and the rest) | **Accepted with corrections** (A-5, A-6, I-1…I-4) |
| 4 | Six new findings: does any block J2? | **F-J2-1 is wrong as stated (B-3):** the referent already has a live offense crit that J-S8 sees, on the summon lane. F-J2-2 needs its predicate fixed (A-8). F-J2-3 has no mechanism (folded into B-2). F-J2-4, -5, -6 accepted |
| 5 | Golden-master gate table and port hook | **Re-sequence (A-9); add the § 4.3(ii) rows (A-10).** One null-guarded hook commit is acceptable **only with an enumerated site list and the A-11 proof set.** "Identical by construction when null" holds on the engine side. On the port it is **identical by mechanical inspection plus empirical proof**, not by construction |
| 6 | Separate rulebook pack | **AGREE** (never a v3.11 member). Layer it (A-12) and keep it out of the port's ORACLE and PLAY configurations |
| 7 | Predictions and controls | Discriminating in part. **Control equivalence covers one mechanism of nine (A-13).** P-J2-13 is falsified as worded (B-3) |
| 8 | Conductor rulings KP-315 | **(a) AGREE**, with the A-9 clarification. **(b) DISSENT IN PART** (§ 8) |

---

## § 1 · The binder (question 1)

### B-1 (BLOCK) · The FILE-pinned emitter cannot observe `JOIN[warlord, GD]` as designed (#75)

**What exists.** The J-S8 emitter (`gamora_join1_gm_emit_2026_09_29.py`) runs a start-up assertion before any `reincarnated` import:
- **LIMB 1** is a sweep, `_sweep()` at :47-59, re-run at :339 and :761. Every loaded module named `reincarnated*` must have its `__file__` under `JOIN1_SEALED_SRC`.
- **LIMB 2** requires `HEAD == JOIN1_ORACLE_COMMIT ==` the oracle tag's commit, on a clean tree.
- `--config` accepts **only `("ORACLE",)`** (:911).

The B0-N precedent passes that assertion because its binder (`join1_b0n_hook/sitecustomize.py`) imports **only sealed modules** and binds **values**. It runs with `PYTHONPATH = hook dir : sealed src` (`gamora_join1_b0n_selfjoin_2026_10_06.py:284`). It loads no code from outside the sealed tree.

**What the design does.** The rulebook is `simulation/rulebook/`, which imports as `reincarnated.simulation.rulebook` (§ 1.5). In a JOIN interpreter built the B0-N way:
1. **It cannot be imported.** `reincarnated/` and `reincarnated/simulation/` are regular packages resolved from the sealed worktree. That worktree is at `969fbd8d` and has no `rulebook/` (checked this Gate).
2. If it is forced in from the HEAD tree, LIMB 1 halts with `JOIN1-HALT location`.
3. If the run uses a HEAD worktree instead, LIMB 2 halts: HEAD is not the seal commit.
4. Even if loading worked, the emission would be labelled `ORACLE`.

So the claim that "the J-S8 emitter observes `JOIN[warlord, GD]` with its FILE-pinned bytes unchanged" (§ 1.4 R-1; KP-315) **does not hold for the layout in § 1.5.** P-J2-2, the golden master itself, has no runnable instrument.

**The part of R-1 that IS right, confirmed this Gate.** Symbol-preserving substitution does keep the emitter's G2 capture working:
- `threat.py` calls `mitigate` through its module global, so the emitter's `_mit` wraps whatever the binder installed.
- `IntakeFold.physical` calls `physical_applied` and `order_fork_delta` through `intake`'s globals.
- The transcribed form must call `ik.armour_branch` live.

The emitter's G2 instrument also depends on **call count and position**: `ph["primary"] = (ph["n_pa"] == 3)`, emitter :563-577, which picks the third `physical_applied` call per hit. This is why A-2's do-not-substitute list is required.

**Fix: amendment A-1.**

### B-2 (BLOCK) · The substitution set is not closed. The "exactly two aliases" claim is true only because of that (#86, #73)

R-2 names eight symbols: four delegations and four transcriptions. The note's own § 2 inventory and § 7 controls need the binder to reach sites outside that set:

| Needed by | Site | Why the eight do not reach it |
|---|---|---|
| § 2.5, F-J2-3, NC-J2-5 (world tick) | `run.py:1215` `period = tick_period_s(as_pct)` and `:1216` `ticks_per_s` | `run.py:46` imports `tick_period_s, ticks_per_s` **by name** from `channel`, so substituting at `channel` does not reach. **The note specifies no mechanism for the world-tick split** |
| § 2.2 offense, NC-J2-4 (Lightning refusal at the first Soulfire row) | `SecondaryStreams.soulfire_applied` :262-277 · `.bleed_dps_against` :289-293 | Inline `max(0, 1 − res/100)` inside instance methods. No R-2 symbol covers them, so NC-J2-4 cannot fire as designed |
| § 2.2 offense, W1, L-06 | `summon_offense.applied_for` :462-475 | **A third offense resist/crit form,** inline. Its physical branch goes through `po.applied_damage` (reached); its non-physical branch does not |
| NC-J2-6 | `GdReposition._stop_where_close_enough` :655 | Not in R-2 |
| F-J2-2 `pth_source`; L-06 | `board.pth_for` / `board.apply_crit_reading` (threat.py:1869, :1879) | Not in R-2 |
| § 2.7 pursuit halt | `locomotion.py:1198`, inline in a `Mover` method | No symbol exists. Transcribe the whole method, or declare it outside v0 |

**The scan I ran this Gate.** By-name imports (single-line and parenthesised) in `kc2/`:
- `run.py:46` (`tick_period_s`, `ticks_per_s`) and `run.py:59` (`D_ENGAGE_M`)
- `EOR_RADIUS_M` in five modules: `channel` :39, `disc` :40, `dodge` :35, `player_drive` :37, `threat` :44
- `FIXTURE_ATTACK_SPEED_PCT` in three: `run` :51, `monster_stats` :26, `micro_oracles` :60
- `SOULFIRE_PERIOD_S` in two: `channel` :48, `energy` :38
- plus the two `player_sustain` aliases the note found

P-J2-8 ("exactly the two `player_sustain` aliases") is true **only over R-2's eight symbols**. That set is narrower than the design's own reach requirements. **Fix: amendment A-2.**

### WARN · Limb B′ cannot see a sitecustomize, a non-`reincarnated` rulebook, or the emitter's children

- Limb B (s47 v2 :114) filters `sys.modules` by `startswith("reincarnated")`, and its audit hook is installed after interpreter start. A `sitecustomize`, and under A-1(i) a rulebook loaded under a top-level name, are **invisible to it**.
- Limb B **does** already catch a rulebook *file* loaded under a `reincarnated` name at HEAD, through `files_changed_between_seal_and_HEAD`. A-9 relies on this.
- `Limb A (i)` builds the sealed subprocess env as `dict(os.environ, PYTHONPATH=…)`, so it **inherits any `JOIN2_*` or `JOIN1_B0N_*` key** from the caller.

**Fix: amendment A-4.**

### WARN · Reach probes: a fixed +1 ulp is not a sensitivity proof (#75)

A +1 ulp move can be absorbed by a threshold, a `max(0, …)` or a quantised grain. That gives a false NOT-REACHED. Worse, `energy.EnergyModel.interval_s` feeds no grain at all: the note's § 3 item 1 says its effective cost is 0.0. By the note's own NC-J2-9 rule, D-1's second consumer would be declared NOT-REACHED **while § 3 claims it is bound.** **Fix: amendment A-5.**

---

## § 2 · Inventory completeness (question 2) · WARN

The note organises § 2 by the charter's eight categories. It gives **no crosswalk** from the census rows, so "nothing silently left welded" cannot be checked row by row. Against P0 (`738bec52…`) and the Sorceress census (`6ed4bbf2…`), I find six gaps:

| Gap | Census row | What is missing |
|---|---|---|
| (a) | P0 **B-16**, Sorceress **17** (BOUNDARY: CC/status on the PLAYER, B7) | **No § 2 row at all.** `control_application.player_control_resists` :287 and `suppression_matrix` :318 (the Warlord's control-resist operands), `REF_P_CAST_INTERRUPTS = 0.15`, L-18. § 2.4 covers monsters only |
| (b) | P0 **row 1** (B7, AS-IS) | § 2.7 omits the measured movement operands: `channel_policy.MovementWrap`, `REF_FRAC_MOVING_FIGHT 0.6265`, `REF_P_CHANNEL_GIVEN_MOVING 0.8920`. These are Warlord-measured operands on a BOUNDARY row |
| (c) | Sorceress **13** (splash at the impact point, B6) | § 2.6's form fixes **centre = player**. The centre must be an operand slot (GD value: the player), or the form is welded to the Warlord's geometry |
| (d) | Sorceress **15** (B8) · KP-165 W1 | § 2.2 offense omits the **summon lane**. `summon_offense.resist_column_for` :431 is an existing offense-side element→column mapper, and `applied_for` reads `defence.get(col, 0.0)`: **a silent 0 resist for an element with no column. W1's hazard is already live in sealed code on this lane.** Under #86, W1's refusal must bind every path that reaches the state, the summon lane included |
| (e) | P0 **row 10** (L-06) | § 2.1 omits `board.apply_crit_reading` (threat.py:1879; the identity under the record reading, U-O-1). The L-06 intake hook site (`:1875`) sits **before** it, and the design must say which side the hook takes |
| (f) | P0 **row 12** (mitigation order) | § 2.3 calls the operand "a 6-row region table". But `IntakeFold.physical` (intake.py:553-631) calls the substituted `physical_applied` **six times per hit**, including counterfactual telemetry with `global_flat=not self.global_flat` (the **PIECE** table) and with the **other absorption limb**. The operand set must carry `PIECE_ARMOUR` and all three absorption tables, or those telemetry sums change |

**Fix: amendment A-7.**

---

## § 3 · Inherited items (question 3)

- **D-1 / C-1: ACCEPTED as designed.** That means one operand row under RB-REPR-F32, both consumers bound, C-1(a) as P-J2-6, and C-1(b) not done. Two corrections:
  - **I-1:** there is a **third reader**. `channel.py:232` reads `v(SOULFIRE_PERIOD_S)`, the fixture's decimal `Cited`, through the by-name import at :48, inside `ChannelMachine.run_hold`. Nothing outside `channel.py` calls it, so it is off the graded path. Name it, with a call-count-0 witness. If D-1 binds through the shared `Cited` object, fixture first (the B0-N route, which my R3-F32 used), all three readers are reached at once.
  - **The energy consumer needs a read-back witness** (A-5), not a grain witness.
- **Frozen `secondary_streams` constants (item 2): ACCEPTED.** These are kit-internal, with bind-at-consumer and no oracle read-at-use. A-6 adds the binding kinds and the derived-constant closure.
- **RAW_EXPECTATION (item 3): the location is ACCEPTED** (`player_offense.py:106-113`; `RawLimb.raw` reads it live, so an `attr` binding reaches). **I-2:** label the two halves separately: *location* CLOSED; *weapon-damage-share decomposition* `schema-change-owed` (J-S4b / elrond J-L4). The note's "V2-EOR-WD-DEAD closes" is one word too strong for KP-307's two-part question.
- **Region armour (item 4) and CSV operands (item 5): ACCEPTED**, with A-7(f) and A-12.
- **OA and crit as witnesses (item 6): ACCEPTED.** Turning `HIT_CHANCE = 1.0` into a theorem, with `OffenseHitUndecided` when it fails, is the right shape. Keep the two "no roll" causes distinct in the registry: *GD certainty* (the referent) vs *spells have no hit roll* (Sorceress row 10).
- **z3 tolerance (8) and the completion probe (9): ACCEPTED.** No tolerance is granted after the fact, consistent with my J0-F WARN-3 ruling.
- **Port attack-speed guards (10), the hit grid (12) and W1 (+): ACCEPTED.**
  - **I-4:** the grid's digests are cited "per AGENT_STATE". Derive them at E2 (derive, don't relay).
  - W1 sequencing: see A-9.
- **INFO-C1 refusals (11): ACCEPTED** (`PartialConversionUnsupported`, `ConversionScopeMismatch`). **I-3:** the note does not say what `family_of_compiled` does **when the record has no scope field**: raise, or pass with a flag. Derive at E1 whether the referent's conversion row carries a scope. P-J2-7 depends on the answer.

---

## § 4 · The six new findings (question 4)

### B-3 (BLOCK) · F-J2-1 is wrong as stated. The offense direction already carries a live crit, and J-S8 sees it

F-J2-1 and P-J2-13 rest on "at the referent's offense crit 1.0, `x·1.0 == x`: the golden master cannot see the difference". **That is true only for the player's own streams** (EoR, Soulfire; `crit_mult` LO 1.0). The player's **summons**:
- roll `th.resolve_hit(pth, roll)` (`summon_offense.py:879-880`), and
- apply the tier multiplier **after** armour and resist (`applied_for(dr, defence, mult)` :891 → `po.applied_damage(…, crit_mult=mult)` :471-473, or `raw·max(0, 1 − res/100)·crit_mult` :475).

**Derived this Gate from the FILE-pinned G1** (`eb335eba…`): **2,347 summon hit rows carry `damage_multiplier > 1.0`** (and 148 monster rows). The offense crit stage is therefore **live in the referent and inside the golden master's domain**. Summon damage feeds monster HP and so kill timing.

**Why this blocks before J2 and not J3.** Which stage is correct remains J3's question; that deferral is accepted. But the registry **schema** is built at W1. As written it keys `crit_stage` **per family** (§ 2.8: `family → {…, crit_stage}`), and the same fact is stored a second time per direction in `RB-LAW-CRIT-STAGE` (§ 5.1). Neither can express the referent. Physical is `pre` for monster→player, `post` for player-stream→monster, and `post` (and observable) for summon→monster. Sorceress row 10 needs `none` for spells. A J3 lever that moves "offense crit stage" as one switch would move a referent-visible lane. **Fix: amendment A-3.**

### Others

- **F-J2-2: ACCEPTED, with the predicate fixed (A-8).** In the oracle the board replaces `pth` **regardless of Resilience's DA window**: `_da` is computed at :1852 and discarded when `pth_for` resolves (:1869-1872). The port does the same (fight :5723-5729). A validity predicate on the *effective* DA would switch to `equation` whenever the window opens and break P-J2-2.
- **F-J2-3: ACCEPTED as a finding. Its mechanism is missing** (see B-2).
- **F-J2-4: ACCEPTED. I-9:** there is a third instance, on the summon lane: `defence is None → raw·crit_mult` (`summon_offense.py:466-468`). Include it in the `absent_defender` policy row.
- **F-J2-5: ACCEPTED.** The port rulebook uses `hypot_py`. The sealed predicate stays as it is, and a reachable divergence is a new Matt question. The note says this correctly.
- **F-J2-6: ACCEPTED.**
- **None of F-J2-2…6 blocks J2.**

---

## § 5 · Gate table and port hook (question 5)

- **Sequencing conflict (A-9).** § 4.2 makes the Limb B′ extension "J2-E2's first" commit. KP-315(a) makes W1 J2's first commit "provided no other J2 commit lands before it". The two cannot both hold. Re-sequence as in A-9.
- **§ 4.3(ii) missing (A-10).** The charter's golden master reports the `EXECUTES-THE-BOUNDARY-RULEBOOK` rows (TA-X-07/20/29/30) beside the J-S8 diff, and B0-N did. The § 4.1 table omits them.
- **"J-S8 oracle half re-emitted at HEAD" (E2) cannot run.** LIMB 2 refuses any tree whose HEAD is not the seal commit. Restate it as "from the sealed worktree".
- **WARN-A1 is discharged** (KP-316, godot `d017d54`). D2's precondition is met. Update the § 4.2 text (I-5).
- **Engine side: identity by construction holds.** ORACLE's files do not change, and B′ plus the symbol census (A-4) witness that.
- **Port side: not by construction.** Wrapping a site in `if rulebook == null:` re-indents the original lines and splits inferred-type declarations. Examples: fight :6243-6244 `var res := …`, `var d := …`, and the stream sites at :3830-3877. "Byte-untouched" is literally false. **Bit-identity is still provable: by mechanical inspection plus empirical evidence (A-11).**
- **Is ONE commit enough?** For J2's boundary forms, yes, **if the site list is enumerated**. Today three site groups have no line pins: the "clock / cadence accumulator, disc predicate call sites, pursuit halt / intercept call sites". It is **not** enough for J3's levers whose sites sit outside the forms: L-02 emission count per tick, L-03 max-HP mutation, L-07/L-08 packet kind and stage entry. Either D2 pre-places those sites, null-guarded, or the note declares now that J3 needs a second KP-312 ruling (A-11 P6).

---

## § 6 · The separate rulebook pack (question 6) · AGREE

A pack movement voids J-S8 wholesale (J-P2 § 7(c)), so the rulebook must not be a v3.11 member. The design handles this correctly: pointer rows with bits asserted at cut, cross-pins derived and not retyped, and its own ROWSET law. MIGRATION per ADR-004. Two amendments (A-12):
- **Layering.** `operands_gd.json` mixes **LAW** constants (floor 55, thresholds, divisor 70, OA 12/53, cap rule) with **KIT:warlord** operands: raw 51,726.0, `kit.warlord.soulfire_period_s`, player DA 2,591 and OA 3,259, the resist sheet, region armour, Resilience. § 3 items 2-3 call several of these INTERNAL. Unlayered, the pack meant to undo P0 finding 5 re-welds the Warlord inside the rulebook, and J4a cannot swap a defender without editing "rulebook" rows.
- **Input boundary.** The port's ORACLE and PLAY configurations must **never open** `kc2-rulebook-pack-v0`. Otherwise it becomes an ORACLE input (see § 8(b)).

---

## § 7 · Predictions and controls (question 7)

**What discriminates well already:**
- NC-J2-1: grid RED 140/440 = NC-H1, with the J-S8 non-movement stated.
- NC-J2-2: order flip ≡ the sealed `OrderLimb`, row for row.
- NC-J2-3: = NC-4.
- NC-J2-6: = NC-3c.
- NC-J2-7: = B0-N R1. This one and NC-J2-6 are equivalence-to-record.
- NC-J2-4: the offense refusal, which today's oracle cannot produce. Once B-2 is fixed so it can fire, it is the best positive proof that the offense half is on the path.

**The gap.** The golden master tests **one operand point**, GD's. At that point a transcription that hard-codes GD's literals and one that reads its operands **give identical output**. Only a second operand point separates them. Control equivalence does that, and today it covers the mitigation order only. **Fix: amendment A-13.**

**Two more items:**
- **P-J2-13 is falsified as worded** (B-3). Restate it for the player-stream lane only, and add NC-J2-11.
- **I-6:** the control runs move levers off GD (NC-J2-1 is L-04 at 5). Declare the control profiles a non-graded class written only under the controls directory, so the charter § 6 HALT ("any lever moved off its GD setting outside the joined kits' own profiles") cannot be tripped by ambiguity.

---

## § 8 · The conductor's KP-315 rulings (question 8)

**(a) W1 as J2's first commit counts as "before J2 opens": AGREE.**
- W1 was my KP-165 finding. Its intent was that no kit packet may route through the offense side without a refusal table. No kit packet routes before J4b, so first-build-commit placement meets the intent.
- **Two clarifications for the ruling text:**
  1. "J2 commit" means a **build or instrument commit on the join path**. It excludes the design note (`285a2364`) and the Gate-1 addendum (E1), which are documents and preregistration. Read literally, the ruling is already breached by the note itself.
  2. W1 must carry the **A-3 schema** and cover the **summon lane** (A-7(d)), so it lands after E1. Sequence as in A-9.

**(b) The V22 operands fall under KP-310's class clause: DISSENT IN PART.**
- **Agree on the kind.** V22 `oa_pre_modifier` / `oa_eff` is a pack literal where the oracle computes from operands (threat.py:949-951).
- **Disagree on the reach of the authority, for two reasons:**
  1. KP-313's same-class grep (drax) **listed v22/u3 `oa_eff` as "operand absent or not the class"**, and KP-314 (mine) recorded that V22 *lacks operands*.
  2. KP-310 authorised computing "from **the pack operand**", an input the port's ORACLE already reads (v3.11). The design sources V22's operands from **`kc2-rulebook-pack-v0`, a new artifact.** If the sealed runtime's ORACLE or PLAY computed `oa_eff` from it, that would **add an input to ORACLE**. Matt's words do not cover that, and charter § 4.7 makes it a HALT.
- **Recommended reading:**
  - In J2, the V22 operands are read **only by the port rulebook mirror (JOIN)**. ORACLE and PLAY keep the literal. P-J2-11 compares the two.
  - If every row is bit-equal, nothing in ORACLE changes and no ruling is needed.
  - **If any row differs, that is a new Matt question** (an ORACLE input change, or a v3.11 movement that voids J-S8), not an application of KP-310.
- If the conductor keeps (b) as written, it conflicts with the scope of a Matt ruling and **escalates to Matt** per ADR-002.

---

## § 9 · Amendments (exact) for the J2-E1 addendum

**BLOCK-class (must land before the first build commit; my delta check of the addendum lifts the BLOCK):**

- **A-1 (B-1) · Emitter provenance and package placement.** The addendum chooses **one** route and specifies it:
  - **(i) Recommended; keeps the emitter's bytes fixed:**
    - In JOIN interpreters the rulebook is loaded **under a top-level name outside `reincarnated*`**, by file location from a pinned commit, with relative imports only.
    - The binder asserts and logs, **per pid (parent and every per-(arm, salt) child)**: the rulebook source GIT TREE OID at a named commit, and a clean tree.
    - JOIN emissions are written **only outside** `join1-gm-fixture-v1/`, carry a sidecar `JOIN-PROVENANCE.json` (rulebook tree OID, profile id, A-2 table digest, every pid's bind log), and are compared at **ROWSET level only**.
    - The emitter's `ORACLE` label on a JOIN emission is declared a known label of the unchanged instrument and is **never quoted**.
  - **(ii) Alternative:** amend the emitter to add `--config JOIN` and a rulebook-provenance limb.
    - Edit only the start-up and provenance region and the `choices` tuple; the hook block (:480-640) stays byte-identical, shown by a diff limited to those lines.
    - Mint a new FILE pin.
    - Run its own controls: an ORACLE re-emission through the amended emitter reproduces `f82807fb`'s seven ROWSETs and grain FILEs; a dirty rulebook tree HALTs.
  - **Either route:**
    - Commit a dry run showing the start-up assertion passes with the binder loaded, before E3.
    - Restate E2's "re-emitted at HEAD" as "from the sealed worktree".
    - Restate § 1.5's layout to match the chosen route.
- **A-2 (B-2) · A closed substitution table in § 1.4.**
  - **One row per touched symbol:** module · symbol · kind ∈ {delegate, transcribe, `attr`, `dictitem`, `cited`, `default-arg`, `dataclass-default`, alias-rebind} · oracle line · every consumer, by-name aliases included · grain fed · reach witness (A-5).
  - **The table must include at least:**
    - the world-tick mechanism through the `run.py:46` aliases (`tick_period_s`, `ticks_per_s`)
    - `SecondaryStreams.soulfire_applied` and `.bleed_dps_against`
    - `summon_offense.applied_for`
    - `GdReposition._stop_where_close_enough`
    - `board.pth_for` and `board.apply_crit_reading`
    - the pursuit halt: transcribe the `Mover` method, or declare it outside v0 with the `D_ENGAGE_M` (`run.py:59`) binding route
  - **DO-NOT-SUBSTITUTE list:** the emitter-wrapped symbols whose call structure the instrument depends on: `IntakeFold.physical` (the `n_pa == 3` primary detection), `order_fork_delta`, `MovingDisc.resolve_tick`, `SummonOffenseFold.swing`.
  - **R-3's scan set** = the table's symbols ∪ every operand name.
  - **P-J2-8 restated:** "the scan's committed output is the alias set; each alias is rebound and identity-asserted". Not "exactly two".
- **A-3 (B-3) · Crit stage keyed by lane.**
  - `crit_stage` (and `armour_applies`) are keyed per **(direction, lane/source class)**, in **one home** (the registry), with `RB-LAW-CRIT-STAGE` pointing at it.
  - Referent rows: monster→player `pre` · player-stream→monster `post` (unobservable at 1.0) · **summon→monster `post` (observable; 2,347 G1 rows)**. Add the value `none` (Sorceress row 10).
  - **P-J2-13** is restricted to the player-stream lane.
  - **New NC-J2-11:** summon crit stage post→pre in JOIN gives a predicted RED. The movable set is summon physical rows with tier > 0 on the DGP branch, **counted at E1 before any build**. Pair it with an intake pre→post control (G2 moves on monster crit rows).
  - **§ 6 L-06** names the lanes it governs.

**WARN-class (in the same addendum):**

- **A-4 · Limb B′.**
  1. Check every loaded module's `__file__` against the rulebook dir and both hook dirs, **regardless of module name**.
  2. Run a symbol-identity census over the A-2 table: for each row, `getattr(mod, name)` is the sealed object (`__code__.co_filename` under the sealed `kc2`), or its value bits equal the oracle's import-time bits.
  3. Build every ORACLE subprocess env with the `JOIN2_*` and `JOIN1_B0N_*` keys **removed**, and record the env-key census.
  4. Give a per-pid witness for the emitter's children on every ORACLE-half emission quoted as J2 evidence.
  5. NC-J2-8 gains a second limb: the binder loaded under a non-`reincarnated` name makes B′ go RED.
- **A-5 · Reach witness, two limbs (NC-J2-9).**
  - **(a) Call-count parity, in a probe run that is never graded.** Tripwires go on the captured sealed objects:
    - a transcribed sealed body is called **0** times under JOIN;
    - the rulebook form's count equals the sealed body's count under ORACLE on the same cell, per pid.
    - Value bindings get a **read-back at the consumer's read**, for example `EnergyModel.interval_s` bits.
  - **(b) Perturbation, at a per-site magnitude declared at E1**, naming the grain it must move.
- **A-6 · R-4 binding kinds and closure.**
  - Name the kind per site: `default-arg` (`MovingDisc.__init__` radius, disc.py:113); `dataclass-default` (energy.py:89, channel.py:169); or the B0-N "bind the `Cited` before the importer loads" route. Each gets a read-back.
  - Bind the **derived-constant closure**: `MIN_/MAX_ARMOUR_OPERAND_LAPY` (intake.py:208-209, read at :563) derive from `ARMOUR_OPERAND_LAPY`.
- **A-7 · Census crosswalk.** Add a table: every P0 and Sorceress BOUNDARY row → § 2.x (F / O + source / weld oracle and port / GD), or an explicit "no form (build item / GD-EMPTY)". Close gaps (a)–(f) of § 2 above. W1's offense table covers the summon lane's `resist_column_for` path (#86).
- **A-8 · F-J2-2 predicate** is keyed on the **base (sheet) DA operand**, not the windowed DA. Record that Resilience's DA term is inert wherever the board resolves.
- **A-9 · Sequencing:**
  - **E2a** = W1 ALONE: `families.py`, both halves, with the A-3 schema and the summon lane; tests RED first; its own Gate-2.
  - **E2b** = Limb B′ and NC-J2-8, both limbs.
  - **E2c** = forms, operands, hooks and grids.
  - **E3** = the binder (after A-1's dry run).
  - The existing Limb B already catches a rulebook file loaded under `reincarnated*` at HEAD (`files_changed_between_seal_and_HEAD`), so W1 is safe under it. B′ needs to precede E3, not W1.
- **A-10 ·** Report TA-X-07/20/29/30 beside P-J2-2 at E3 and beside P-J2-10 at D3 (charter § 4.3(ii)).
- **A-11 · D2 proof set and Matt ruling request:**
  - **P1:** a committed out-of-tree hunk audit. Every removed line reappears verbatim, apart from one added indentation level, inside the `if rulebook == null:` branch. The only added lines are the guard, the `else:` branch, the untyped member and listed declaration splits. No `preload`/`load` of the rulebook.
  - **P2:** no RNG draw inside either branch. Draws stay before the guard, and the `else` form takes the roll as an argument.
  - **P3:** per-site ORACLE execution coverage, each site executed at least once in the § 4.7 harness or the J-S8 port run. Otherwise it is declared "covered by inspection only".
  - **P4:** the note's existing set (§ 4.7 4×5, G3, T-A, **J-S8 port ORACLE 7/7**, the digest bridge).
  - **P5:** a per-site fail-first, with NC-J2-9 mirrored per site (not a single probe).
  - **P6:** the Matt ruling request carries the enumerated site list with line pins, and states whether J3's out-of-form lever sites are included or will need a second KP-312 ruling.
- **A-12 · Pack layering and input boundary.** Every operand row is tagged `layer ∈ {LAW, WORLD, KIT:warlord}`. KIT rows move to their own member (`rulebook/kit_warlord.json`). The note states that the port's ORACLE and PLAY never open `kc2-rulebook-pack-v0`.
- **A-13 · Control equivalence per mechanism.** Where a sealed in-memory perturbation exists (B0-N binder kinds on sealed constants), each mechanism gets one control, row for row against the sealed perturbation:

  | Mechanism | Rulebook-side perturbation | Equivalent sealed perturbation / expected result |
  |---|---|---|
  | Hit | one `PTH_THRESHOLDS` entry or `NORMAL_PTH_DIVISOR` | the same on the sealed constant (grid and J-S8) |
  | Intake resist | `RESIST_PCT['Physical']` 16→17 | the same (G2) |
  | Region armour | one `ARMOUR_OPERAND_LAPY` entry, closure per A-6 | the same (G2) |
  | PCL | 26→25 | the same |
  | Disc radius | 3.0→3.1 | **NC-B1 of record** |
  | World tick | world tick and kit cadence moved together | sealed `attack_speed_pct` 196→200 |
  | World tick, separation (**NC-J2-5b**) | the kit's AS moved alone in JOIN | **G7 GREEN** while kit-cadence grains move. This is the only test that F-J2-3's split exists |
  | `pth_source` | `equation` | sealed with `board=None` |
  | Offense resist | one V23A row | the same row perturbed in the sealed board cache, or declared "not testable" with the reason |
  | Crit stage | — | NC-J2-11 (A-3) |

**INFO (record; no gate):**
- **I-1** D-1's third reader, `channel.py:232`.
- **I-2** V2-EOR-WD-DEAD gets two labels.
- **I-3** `family_of_compiled` behaviour when the scope field is absent.
- **I-4** Derive the hit-grid digests.
- **I-5** WARN-A1 discharged (KP-316).
- **I-6** Control-profile class vs the charter HALT.
- **I-7** The fixture file is `manifest.json`; the note writes `MANIFEST.json`.
- **I-8** Soulfire's crit is copied by value at run start (`run.py:1224`). A J3 `crit_model` hook must act before that copy or at both sites.
- **I-9** F-J2-4's summon-lane instance.
- **I-10** Pets as control victims (`summon_offense.route_control`, mutable `register_families`) are player-side. Class them in the crosswalk.

---

## Rationale

- **B-1** is #75: the instrument must bind the artifact that ships. The golden master's only instrument, as configured, refuses the configuration it is meant to grade.
- **B-2** is #86 (a guard's population is every path that reaches the state) and #73 (a claim true only of an under-enumerated set is a record that does not carry the state).
- **B-3** is a finding contradicted by the frozen fixture. It also fixes a schema at W1 that J3 would inherit. The schema, not the ruling, is what must be right now.
- **A-13** is Principle 1: the golden master at one point cannot discriminate the defect class the transcriptions risk.

## Action

- [ ] **gamora:** J2-E1 addendum ALONE carrying A-1…A-13 (and the I-items as one-line acknowledgements). Then route it to me for a **delta check of the addendum only** (not a full re-Gate). No build commit (W1 included) before that.
- [ ] **gamora:** under A-3, derive the summon-crit movable-row count at E1, before any build.
- [ ] **star-lord:** none until the addendum. A-12 changes the pack's member list before the S1 prereg.
- [ ] **drax:** none until the addendum. A-11 changes the D2 proof set and the ruling request.
- [ ] **conductor (gandalf):** record the BLOCK and its lift path in the ledger. Restate KP-315(a) with the A-9 clarification. Adopt the § 8(b) narrower reading, or route (b) to Matt.
- [ ] **Matt:** nothing from this Gate unless the conductor maintains KP-315(b) as written. The D2 ruling request comes later, with A-11's enumerated site list.

## References

- `/Users/admin/Games/reincarnated-engine/src/reincarnated/simulation/math/join1-j2-rulebook-v0-design-2026-10-07.md`
- `/Users/admin/Games/reincarnated-engine/src/reincarnated/simulation/scripts/gamora_join1_gm_emit_2026_09_29.py` (:34-80 start-up assertion; :498-590 hook block; :911 `--config`)
- `/Users/admin/Games/reincarnated-engine/src/reincarnated/simulation/scripts/join1_b0n_hook/sitecustomize.py`
- `/Users/admin/Games/reincarnated-engine/src/reincarnated/simulation/scripts/gamora_join1_b0n_selfjoin_2026_10_06.py` (:281-293)
- `/Users/admin/Games/reincarnated-engine/src/reincarnated/simulation/scripts/gamora_join1_b0n_s47_evidence_2026_10_06.py` (:85-127 Limbs A and B)
- `/Users/admin/Games/reincarnated-engine/src/reincarnated/simulation/kc2/`: `run.py` (:46, :50-59, :1212-1224, :3334-3341) · `threat.py` (:266-330, :1848-1880, :2136-2160, :2226-2236, :945-962) · `intake.py` (:199-209, :275-277, :373-409, :553-631) · `player_offense.py` (:100-132, :321-336, :515-533) · `secondary_streams.py` (:30, :61, :256, :262-293) · `summon_offense.py` (:431-437, :462-475, :600-760, :870-901) · `channel.py` (:34-48, :79, :169, :232) · `energy.py` (:38, :89) · `disc.py` (:40, :113) · `locomotion.py` (:1198) · `gd_reposition.py` (:651-672) · `player_sustain.py` (:41-45)
- `/Users/admin/Games/reincarnated-engine/src/reincarnated/simulation/output/join1-gm-fixture-v1/oracle/` (`manifest.json`, `G1.jsonl`)
- `/Users/admin/Games/reincarnated-godot/kc2_runtime/sim/kc2rt_fight.gd` (:5722-5750, :6239-6247, :3830-3877)
- `/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/gandalf/notes/2026-09-29-join-1-run-charter.md` (§ 2, § 4.3-4.7, § 5, § 6, § 7)
- `/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/gandalf/notes/2026-09-20-kc2-play-run-charter.md` (KP-165, KP-305…KP-316)
- `/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/elrond/notes/2026-09-28-join1-p0-internal-boundary-census.md` · `…/2026-10-01-join1-j0-sorceress-census.md`
- `/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/qa/findings/2026-10-06-join1-b0n-gate2.md` (C-1, R3-F32) · `…/2026-10-07-join1-j0f-port-gate2.md` (WARN-A1, INFO-B2, INFO-C1) · `…/2026-10-02-join1-j0f-oracle-half-gate2.md` (WARN-1, WARN-3)
- `/Users/admin/Games/reincarnated-collaboration/CLAUDE.md` § Sealed-artifact change protocol
