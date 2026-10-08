# Finding — 2026-10-08 — JOIN-1 J3: the second KP-312 site list (drax) + a challenge to KP-358's crit decision

**Reviewer:** jack-ryan (Gate review before the ruling goes to Matt; KP-358/359; doc-only, no run)

**Severity:**
- **(1) Site list: ACCEPTED with 6 adjustments** (ADJ-J1…J6).
  - **One is a correction** that must land before the text goes to Matt: **ADJ-J1, S-4 guard form.**
  - **One is a scope question for Matt:** ADJ-J5, the port world clock.
  - drax's two INFOs are **accepted**, with dispositions.
  - The draft scope sentence is in § 3.
- **(2) KP-358: CHALLENGED on four points** (C-1…C-4). C-1 is substantive, C-4 is procedural. None argues against the core decision: the referent stays LO, and kits use explicit crit vocabulary. gamora folds C-1…C-4 into the J3a prereg, and I delta-check that before code.

**Target:** godot `712e2de`, `kc2_play/join/J3-SITE-LIST-8a4da5f8.md` (runtime X `8a4da5f8…`; `kc2_runtime/` untouched) · conductor note KP-358
**Disciplines cited:** #24 · #75 (cl. 6) · #86 · R-4 · KP-312 · charter § 6

---

## § 1 · The site list

### 1.1 Completeness for J3's port levers

| Lever (J3 design + ADDENDUM-E1) | Port route | Verdict |
|---|---|---|
| L-02 | S-1 | ✓ |
| L-03 | S-2 | ✓ |
| L-07 | S-3 | ✓ |
| L-08 | S-4 (gate) + an S-3 form parameter (chain entry) | ✓ (see ADJ-J1) |
| L-06 values, all lanes; intake/summon draws | H-3 / H-5 (D2) | ✓, no site |
| L-06 player-stream draws | H-11 + H-12 (D2) | ✓, no site (A-5 confirmed, § 1.2) |
| L-06 Soulfire draws | S-5 | ✓ |
| L-04/L-05 at intake/summon; L-01's breakpoint table | H-3 / H-5; H-18 | ✓, no site |
| L-04 at offense scope | S-6 HELD | ✓ |
| H-18b | S-7 | ✓ |
| L-06(a) intake `post` | deferred (design § 4.3) | ✓ |
| L-01 above the clock (Matt: (ii)) | S-8 none for the cadence; **the world clock itself needs X-3** | see ADJ-J5 |

**No lever is missing.**

### 1.2 The A-5 finding: confirmed

- **The player stream needs no sealed edit.** H-11 is the port's only evaluation of the player packet, 1:1 with row 32. H-12 runs in the same iteration and reads the mirror's stash. The skips and the loop gate are equal (J-S8 7/7 at GD both ways).
- **Soulfire needs S-5. Confirmed against the source:**
  - **Python:** `_sf_ids = [h.target_id for h in hits]` under `SoulfireReach.DISC` (`run.py:3296-3298`). That list has **no alive filter**, and `soulfire_damage_against` runs before `_ss_hit` drops a body already dead (`run.py:3236-3242`, `:3307`). So a body killed by the disc earlier in the same tick is **counted** and would **draw**.
  - **Port:** `if not bool(b.get("alive", false)): continue` sits **before** H-13 (`kc2rt_fight.gd:3848-3849`).
  - **Consequence:** without S-5, `crit:soulfire` falls out of step on the first proc tick after a disc kill.
  - **S-5's added-only skip hook** advances the stream exactly where Python calls the counting wrapper. It is the minimal fix, and it needs no identity.
- **The order equality is "evidenced, not proven"** (G3 `heal_hp` bit-equal as the witness). That is the honest statement. **The zero-cost order census at GD (§ 1.4) is REQUIRED** before NC-J3-L06-4 is quoted as cross-mirror evidence. The seeding law `(cell seed, stream id)` is fixed as **text** Python-side first.

### 1.3 Guard form G-B and its control: accepted

- `if rulebook == null or <predicate>: <existing>` / `else: <lever path>`.
- GDScript's `or` short-circuits, so with `rulebook` null the predicate is never evaluated, and the null projection is the existing lines.
- Under `JOIN[warlord, GD]` the predicate is true, so the D2-proven path runs and JOIN-GD stays off the lever code.
- The audit learning G-B, with **its own fail-first control** (P0: a one-byte null-branch difference → RED), is the #75 cl. 6 discipline.

**ADJ-J3** below adds the clause the audit also needs for S-1.

### 1.4 Booking-census ROW ADDITIONS: the ruling must cover them explicitly

- **Correct, and it must be in the ruling text.** KP-348's concurrence covered **relocation** (digit-only, no sim change). S-1 and S-3 **add** `_offer` / `_cons_add` lines in lever-only branches, and so add **new census rows**. That is a change to a sealed self-check's **content**, not its line map.
- **Conditions:**
  - each new row is listed with (code, caller, account, class) and audited one by one;
  - existing rows are relocated by the tool (digit-only, as KP-348);
  - `census_grep` reads MATCH ROW FOR ROW **in the same commit**;
  - T-A pre_read `cell.json` FILE-equal to KP-310 on 25/25 is the null-path proof, since T-A's H-4 reads the census.

### 1.5 The per-site proof plan (§ 3): accepted, with ADJ-J1/J3

P0 (instrument first) → P1 → P1b → P2 → P3 → P4 → P4b → P5 → order census → my delta Gate-2. The site → control mapping in P5 is right:
- S-7 is proven at **kit < world** (NC-J3-L01-1, 0.8 hits per tick). At kit > world it is REACHED-INSENSITIVE by the ceiling.
- The out-of-tree refusal of kit ≠ world relaxes only after S-7 lands, and only for NON-GRADED-CONTROL runs.
- The windowed `.app` self-test, still owed at X, is correctly carried into P4. It must run **before** the new digest is cut, so that its baseline is X.

### 1.6 Adjustments

- **ADJ-J1 · S-4 must be G-B, not G-A. Correction.**
  - As listed, S-4's G-A block `if rulebook != null: return rulebook.gates_clear(rec, inv)` **diverts every `_gates_clear` call under JOIN, defaults included**, to the mirror's transcription of the sealed predicate (`kc2rt_fight.gd:6474-6478`).
  - That contradicts the list's own P3 claim ("with the rulebook set at the defaults … the G-A blocks are no-ops, so JOIN-GD stays on the D2 path"). It would also put a new mirror transcription under the golden master unannounced.
  - **Required:** `if rulebook == null or not rulebook.unmitigable_proportional_on(): <the existing body>` / `else: return rulebook.gates_clear(rec, inv)`. At the defaults the sealed predicate runs.
  - S-2, S-3 and S-5 are true no-ops at the defaults (S-2's call returns null; S-3's predicate is false; S-5 only counts) and stay G-A.
- **ADJ-J2 · State, for each G-A/G-B predicate, its value at the defaults,** in the commit's PREDICTIONS:
  - S-1 `packets_per_tick() == 1`: true;
  - S-7 `last_po_hits()`: true at GD, since `kit_tick()` is evaluated every tick in H-18's else-branch, exactly as Python's `po_hits` at `run.py:2963`;
  - S-3 `proportional_on()`: false;
  - S-4 per ADJ-J1: false;
  - S-2: `max_hp_change(...)` returns null.

  P4b's JOIN-GD 7/7 is then a check on those stated values, not an assumption.
- **ADJ-J3 · S-1's lever path re-implements sealed lines per packet** (k-vector scaling, `_offer`, the three bookings, `prow`, the leech basis), so it can drift from the null path silently.
  - **The P1 audit gains one clause:** the lever path's per-packet block is the null path's lines **verbatim, modulo a declared substitution map** (`applied → applied_k`, `hp → hp_k`, …).
  - Any other difference is RED.
  - **Control:** a one-token drift in the lever-path copy goes RED.
- **ADJ-J4 · S-3's two open questions are settled Python-side first, in the J3c prereg:**
  - (a) whether the proportional packet feeds the leech basis;
  - (b) that `pct-current` reads post-weapon HP.

  The engine form `proportional_raw` / `packets_applied` defines them, and the port follows. Because the engine cannot **emit** L-07, the port's packet order is a **declaration printed on the fidelity table**, not a parity claim.
- **ADJ-J5 · X-3: a scope question for Matt. Recommend asking it NOW, as S-9.**
  - Under Matt's L-01 ruling the world clock follows the fastest kit.
  - The D2 Barbarian sets L-02 (dual-wield packets) and L-03 (Battle Orders max HP), so it is **port-only** (Gate-1 § 4 item 3), and its IAS likely puts it above 196. **Its first port run therefore needs the world clock bound to X ≠ 196**, i.e. X-3 (`kc2rt_pack.gd:1284`, `kc2rt_fight.gd:564-576`, with their 1e-12 consistency check).
  - The same holds for my L-01 condition (a): the Warlord re-run at X on the port.
  - Deferring X-3 makes a **third** KP-312 cycle certain before J4a, with a full T-A / G3 / § 4.7 / J-S8 proof set during C-9's machine-priority period.
  - **Recommendation:** include X-3 as **S-9** (G-B, predicate `rulebook == null or rulebook.world_as_pct() == <the pack's own value>`, a control-reach site), proven by the (ii) control `world = kit = X` on the port.
  - If Matt prefers deferral, the ruling sentence must **say** that a third ruling is certain before J4a.
- **ADJ-J6 · The A-6 table changes (INFO-2's consequence).** Summon-lane port controls cannot run at J3a. This covers NC-J3-L06-2, the summon part of L06-3, L05-2 and **LANE-2**. ADDENDUM-E1's A-6 said "LANE-1/2's law check runs on the port's G1"; that is true for LANE-1 only. A-6 is corrected in the J3a prereg.

### 1.7 drax's INFOs

- **INFO-1 (the port's `sf_n_rows` excludes dead-body rows): ACCEPTED as an existing ORACLE-vs-port counter difference.** No grain reads it, and it is not to be fixed (that would be a sealed counter change with no grain behind it).
  - **Recorded in the fidelity notes.**
  - The port's draw-count limb for NC-J3-L06-4 is `crit:soulfire` draws == `sf_n_rows` + the mirror's skip count. **The prediction is written that way before the run.**
- **INFO-2 (the port emitter re-evaluates summon G1 with the sealed law): ACCEPTED, and disposed of by ADJ-J6.** Confirmed: `kc2p_join1_gm_emit.gd:645` calls `Kc2RtLawsR.resolve_hit(pth, roll, sm.pth_minimum, sm.pth_thresholds, sm.pth_multipliers, …)` and cross-checks totals at `:653-666`.
  - **Summon-lane port controls are engine-only at J3a.**
  - **Before any summon-lane port claim (J3b/J3c):** the JOIN session tool supplies the summon re-evaluation from the mirror's form (lane `summon`, the lane's operands), as an instrument change **with its own negative control** (#75 cl. 6). It is not a sealed site.
  - **Also inventory H-4.** The emitter recomputes the summon PTH equation itself (`:644`), so an L-06 change to the PTH form, if any, would split the same way.

---

## § 2 · KP-358, the conductor's crit decision: challenged on four points

**The decision, as I read it:**
- the referent and golden master stay crit LO;
- JOIN adopts an explicit crit-chance + multiplier vocabulary for all kits;
- GD abilities get **JUDGED** values from the M2 threshold-banded roll against the arena population, in a new `gd-judged` profile (labelled JUDGED, D-L5 undecoded);
- kits are compared against the Warlord under `gd-judged`.

**The core is sound:**
- The golden master is untouched.
- Judged values are labelled.
- Comparing kits against a Warlord built with the same vocabulary is the right instinct.

**Four points must be settled in the J3a prereg:**

- **C-1 · Which lanes. Do not overwrite decoded lanes (substantive).** "For all kits" must not reach lanes whose GD rule is **decoded**:
  - the **monster → player** lane (pth-tiered, MEASURED ×2);
  - the **summon** lane (the oracle applies GD's `resolve_hit` law to summons).

  `gd-judged` may replace only the **undecoded** lane: player-stream (D-L5). The spell lane is `none` by the census. Converting a decoded tiered law into (c, m) would turn a measured mechanic into a judged one.
  - **Requirement:** the profile lists its lanes; the decoded lanes stay `pth-tiered`; the registry prints the per-lane status.
- **C-2 · The judged value's inputs must be named, and some are not yet available.**
  - **Range of the law.** On the player lane every measured path pair has p ≥ 100 (P-J2-5: 74/74, min 103.54). GD's threshold-banded law with a d100 then reduces to **one** effective crit band: rolls ≥ 90 → tier 2, ×1.1, about 11 %. Thresholds ≥ 105 are unreachable by a d100.
  - **The sheet's crit damage.** It reads +57 %, and it is the slot design § 3.1 already names (m = 1.57). It is **either** added to the tier multiplier **or** not. Either choice is a judgment and must be stated as one: it changes the judged m by a factor of about 1.4.
  - **"Against the arena population" needs DA for that population.** 122 of 196 path pairs have **no measured DA** until Matt's calibration-first sourcing lands (KP-356, before J4a). A judged value computed now would rest on the measured 37.8 %.
  - **Requirement:** `gd-judged`'s values are computed **after** the DA sourcing; until then the profile refuses. The prereg names the population (records × waves, and the weighting: per attempt, per record, or per encounter) and the M2 law precisely.
- **C-3 · The comparison baseline composes with the L-01 condition.** Kits are compared against `JOIN[warlord, gd-judged]` **at the same world clock X** (my L-01 condition (a), Matt-adopted). So the baseline is `JOIN[warlord, gd-judged @ X]`.
  - **And the judgment's own cost is printed:** `JOIN[warlord, gd-judged @ 196]` against J-S8 (`JOIN[warlord, GD]`, crit LO), per metric, on the fidelity table.
  - Otherwise a reader cannot separate "the kit differs from the Warlord" from "the judged crit differs from the referent's LO".
- **C-4 · Charter § 6 HALT boundary (procedural).**
  - Charter § 6 lists as a HALT: "any lever moved off its GD setting (or its declared-invented default) outside **the joined kits' own profiles**."
  - `gd-judged` moves **L-06 for the Warlord**, who is not a joined kit.
  - **Two ways to make that compliant:**
    - (a) Matt's delegation (KP-358) is recorded **as a charter amendment row** that names `gd-judged` as a sanctioned non-kit profile; or
    - (b) the judged player-lane value is registered as L-06's **declared-invented default** for the undecoded player lane (author, reason, JUDGED). In that case LO remains the referent value for J-S8 only.
  - **I recommend (a):** it keeps the registry's GD-setting column honest (D-L5 bracket LO…HI).
  - **Either way it is written down before J3a builds `gd-judged`.** A delegated decision that crosses a HALT boundary must cite the delegation at the boundary, not only in the ledger (the CLAUDE.md conflict-rule lesson).

## § 3 · Draft scope sentence for Matt's ruling

> *Approve ONE null-guarded change set in `kc2_runtime/` at runtime `8a4da5f8` for JOIN-1 J3's out-of-form lever sites, as listed in `kc2_play/join/J3-SITE-LIST-8a4da5f8.md` with jack-ryan's adjustments (collab `qa/findings/2026-10-08-join1-j3-site-list-review.md`):*
> - *S-1 (L-02 packets per tick; guard G-B);*
> - *S-2 (L-03 max-HP policy; G-A);*
> - *S-3 (L-07 proportional packet; G-A);*
> - *S-4 (L-08: the chain-entry parameter of S-3, and `_gates_clear` under G-B);*
> - *S-5 (Soulfire draw-stream parity at the dead-body skip; G-A);*
> - *S-7 (H-18b, the bleed rider's cadence gate; G-B);*
> - *[S-9 (X-3: the world-clock binding, a control-reach site; G-B), if ruled IN].*
>
> *Conditions: KP-312's four conditions and the list's § 3 proof set. The approval INCLUDES:*
> - *(a) adding booking-census rows for the new `_offer` / `_cons_add` lines of S-1 and S-3 (each row audited), with the existing rows relocated;*
> - *(b) the hunk-audit instrument learning guard forms G-A and G-B, with its own fail-first control.*
>
> *S-6 (L-04 at offense scope) is HELD until the P-J2-5 guard exists. The engine oracle is not edited. A joined kit whose profile sets L-02, L-03 or L-07 is emittable on the port only (the engine carries form-level grid parity). [If S-9 is OUT: the port's world-clock binding needs a further ruling before any port run at a world clock other than 196, which the D2 Barbarian requires.]*

## § 4 · Owed

| Before | Item | Owner |
|---|---|---|
| the text goes to Matt | ADJ-J1 (S-4 as G-B), the ADJ-J2 predicate table, and the ADJ-J5 S-9 question in the text | drax / conductor |
| the J3a prereg | ADJ-J6 (A-6 corrected); C-1…C-4; the INFO-1 draw-count form | gamora (I delta-check it) |
| the J3c commit | ADJ-J3 audit clause and its control; ADJ-J4 settled Python-side; the order census | drax / gamora |
| the next runtime digest | the windowed `.app` self-test at X | Matt's calendar |

## References

- `/Users/admin/Games/reincarnated-godot/kc2_play/join/J3-SITE-LIST-8a4da5f8.md` (godot `712e2de`)
- port: `kc2_runtime/sim/kc2rt_fight.gd` :1966-1972, :3842-3862, :6470-6478 · `kc2_play/tools/kc2p_join1_gm_emit.gd` :640-668
- sealed Python: `kc2/run.py` :2963, :3236-3242, :3296-3308, :3312-3313
- J3 design: engine `d97e1fc0` + ADDENDUM-E1 `b5d3cfbf` (A-5, A-6) · Gate-1 `…/qa/findings/2026-10-08-join1-j3-design-gate1.md` (§ 4, § 7)
- charter `gandalf/notes/2026-09-29-join-1-run-charter.md` § 6 (the HALT boundaries) · ledger KP-348, KP-356, KP-358
