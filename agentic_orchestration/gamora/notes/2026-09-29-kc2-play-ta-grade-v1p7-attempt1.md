# KC2-PLAY · T-A GRADE, graded attempt 1 of 2 under prereg v1.7: verdict `STRUCTURAL`

> **STATUS:** CURRENT. W3 grade seat, SEAL LAP. **Author:** gamora (simulation seam), 2026-09-29. **Conductor:** gandalf.
> **Graded object:** drax's emission `reincarnated-godot/evidence/kc2-play/2026-09-29-ta-run2-v1.7-cells/`, godot `41ec7cd`.
> **Graded against:** prereg **v1.7**, FILE sha256 `552d9faecd83d955c77f2be35991ec51e3908d9f586ab70b5a78b6c156b92896`. I derived it before reading any row.
> **Verdict file:** `gamora/notes/2026-09-29-kc2-play-ta-verdict-v1p7-attempt1.json` (`kc2play.ta_verdict.v1`). The commit message records its sha256.
> **Authority:** grading only. No width was minted or adjusted. No row was reclassified. Nothing graded was re-run. **K-7 held:** all three sealed cells were hash-verified, and `[M-POL2]` was read by key (`⚑ arms.*.terminals`) and nothing else.

---

## § 0 · Integrity, derived before reading anything else

| object | expected | **derived** | |
|---|---|---|---|
| emission `MANIFEST.json` | `bddc501a…` | `bddc501a35a4f19c3f2230cdeae48fdafd4a112460afb0ab0aeef797653b2698` | ✓ (no HALT) |
| emission members | 27 | **27/27** sha256 and byte counts match | ✓ |
| emission tree digest (pack law) | `db33d54f…` | `db33d54f7fc7e1f61faedbe1aed7b5bc98093293b30388af758bcfb740a2ff59` | ✓ |
| runtime tree `kc2_runtime/` | `c9c973fa…` | `c9c973fa456d1f4c8ff01f4e3166067677003220747d8eb151d44da698b5e3ef`, 48/48 | ✓ |
| model pack (17 members, `pack_digest_law_exact`) | `5cab7433…` | `5cab743335c6a721f57680e151d6e949d3387ca164342ffc97fefd04916835e2` | ✓ |
| reference pack (7 members) | `978f54ab…` | `978f54ab275de4f932fd8a7116b3fd44646268ee2b625fcae5516e81ab77b7de`; `cross_pin.model_pack_digest == 5cab7433…` | ✓ (grader-derived; see P-4) |
| P-a / P-b / P-c / P-d | § PINS | `1c80f080…` / `d48512aa…` / `a8b85331…` / `15dace60…` | ✓ all |
| P-e / P-e′ | § PINS | `4b7b78c8…` / `27fc5937…` | ✓ |
| P-i / P-k | § PINS | `cb6a008b…` / `58205679…` | ✓ |
| `[M-POL2]` / `[MECH]` / `[W1W]` | § PINS | `ad61ad2a…` / `20b05cb4…` / `7a992c81…` | ✓ |

**Supplementary evidence from outside the emission MANIFEST.** It comes from the same W3 session and the same pack, and the emitter did not hash-pin it. I hashed it at grade time. Four rows are graded from it, and each is labelled where it appears:
`tmp/kc2/t0/t0_report.json` `4bdff8da5fac77421d346a2200198f533ca0997f6064eeba562d265bf388af93` · `tmp/kc2/kc2rt_purity_scan.json` `d7d3da80…` · `tmp/kc2/kc2rt_rules_smoke.json` `17d981f7…` · `tmp/kc2/kc2rt_loader_smoke.json` `71c31eb9…`.
**drax should fold these into the emission for attempt 2.** Until then, the grade is what pins them.

**Label defects, reported and not used as grade inputs** (drax's note 1 and 2, confirmed):
1. `kc2rt_ta.gd:76` hard-codes `prereg_version := "v1.4"`. The emission carries it in 26 files.
2. The harness emits no `substrate_epoch`; `MANIFEST.json` declares it.
3. ⚑ **The label is stale in the harness's row text too, and there it would mislead a literal reader.** Every cell's `board.ta_x_25` block still describes clause (c) as *"one-sided structural non-zero"*. That is the v1.4 sign. v1.6 inverted it and v1.7 carries the inversion. `ta_b_15` still prints the reference points `0.3828 / 0.1134` and `zero_is_the_anomaly: false`, where v1.7 has both points at `0.0000`. The ten `conditions_raised_to_the_grader` still argue v1.4's absolute-versus-relative ambiguity for `TA-X-07`, which v1.5 settled. **Anyone who read the harness's own annotations would grade the one red row of this run GREEN.**

---

## § 1 · THE VERDICT

```
STRUCTURAL @ coverage 89/89 — 21/28 EXACT green · 1 RED (TA-X-25) · 6 UNGRADEABLE
(TA-X-07, TA-X-26, TA-X-27, TA-X-28, TA-X-29, TA-X-30) · TA-X-06 UNGRADEABLE-declared (Q83(b), KP-110)
· dilution 2.431× · substrate_epoch v3.4.2 / 5cab7433…
```

**Antecedent (§ G, walked in order `STRUCTURAL → INDETERMINATE → PASS`):** at least one EXACT row is RED. **`TA-X-25` is red on clause (c) on all five arms.** Those five arms are **two** independent outcomes (§ 5).

**Consequences as written:**
* The port is wrong, and there is **no W4** until it is repaired.
* This **consumes attempt 1 of 2**. **L2:** attempt 2 fires only after jack-ryan Gate-2 PASSes drax's repair.
* The T-B quoting cap **TRIPS** on `C2`. `C1` is clean: every pin reproduces and the verdict file exists. `C3` is clean at 89/89.
* The run is not sealable.

⚑ **The six UNGRADEABLE rows and the two unmet preconditions (P-4 and P-5, § 2) would give `INDETERMINATE` by themselves. They are outranked here, not dismissed.** Fixing the red and nothing else does not reach PASS. It reaches `INDETERMINATE`. Almost all of these need **emission**, not repair. § 6 lists them.

⚑ **`TA-X-06`, declared.** It enters no antecedent and is not counted in 28/28. It is printed here as the prereg requires: the relation is `W1 ≡ M-POL-2` on **5/5** salts (`a192c460… · 32ec61b7… · 8864064f… · d2ecad46… · 6ccfd158…`, identical pairs). `TA-B-14` on W1 reads vetoes `[0,0,0,0,0]` and occupancy `[0,0,0,0,0]`, against the oracle's 2 / 0. **Conformance check (jack-ryan v1.7 pre-read WARN-1):** the verdict file's `declared_ungradeable` has ids exactly `["TA-X-06"]` with authority `Q83(b) / KP-110`. The build script asserts this. **MET.**

---

## § 2 · PRECONDITIONS

| id | emitted | state |
|---|---|---|
| **P-1** | 89/89 mapped, 0 unmapped, refusals **3** (M17, D3, D9). Counts: IMPLEMENTED 65 · DIVERGENCE 8 · RUNTIME-CHOICE 13 · OUT-OF-SCOPE 3 | GREEN on completeness. ⚑ **cl. 1a NOT MET:** the IMPLEMENTED notes for **M4** (`TA-X-15`), **M10** (`TA-X-30`) and **D19** (`TA-X-29`) do not name their EXACT row. Only 7 of the 65 IMPLEMENTED notes cite any `TA-X` id. ⚑ **M17 still cites `ABS-MONSTER-OFFENSE-NO-DATA-POOL466`**, the v3.3 absence that the re-base closed. It is a live pointer to the red's mechanism |
| **P-2** | `M-POL-2` s0 plain == with no-op fold == `a192c460…`, 0 draws | GREEN (within epoch only, § C.7) |
| **P-3** | `POOL-466` / 466; law WEIGHTED:pool_weight + UNIFORM:randrange | GREEN (self-reported). ⚑ The behavioural check that used to back it (`TA-X-25(c)`) now shows the **classification basis** is wrong. The roll population is not |
| **P-4** | the model pack is verified 17/17 by the runtime (loader G1) | ⚑ **NOT MET AS WRITTEN.** The runtime holds the reference digest as a **string constant** (`kc2rt_pack_of_record.gd:47`). It verifies no reference member and emits no cross-pin. I derived both myself and both hold. **A grader's derivation is not the runtime's check** (#75 cl. 1(a)) |
| **P-5** | no fold-settings declaration in any header | ⚑ **NOT MET AS WRITTEN.** From source, the settings are correct: y1/y2 CRUCIBLE rows are consumed; `COST_COLUMN := "⚑ charge_PARENT_PLUS_MODIFIER"` (`kc2rt_per_cast_energy.gd:79`); the C-7 policy module is present; the gmag fold is armed. **But the precondition is the declaration, and it is absent** |

---

## § 3 · THE 28 EXACT ROWS

| id | observed | verdict |
|---|---|---|
| `TA-X-01` | M0 s2 run twice with nothing inserted: `80176c40…` == `80176c40…`. Different arm and salt from P-2 | **GREEN** |
| `TA-X-02` | 89/89, 0 unmapped | **GREEN** |
| `TA-X-03` | `M-POL-2-NULL ≡ M0`, **5/5** | **GREEN** |
| `TA-X-04` | `W1-NULL ≡ M-POL-2`, **5/5** | **GREEN** |
| `TA-X-05` | `M-POL-2 ≢ M0`, **5/5** distinct | **GREEN** |
| `TA-X-07` | (a) max \|rel\| = **1.563e-14** ≤ 1e-12 on 25/25; absolute ≤ 1.55e-6 beside offered ~1e8. (c) ⚑ **`n_terms_accumulated` NOT EMITTED**, so the 4,500-term budget cannot be checked | **UNGRADEABLE** |
| `TA-X-08` | both sub-identities hold on 25/25 | **GREEN** |
| `TA-X-09` | 9/9 REPLAYED (T-0, supplementary). Of 29 in total: 0 fail against the law and 7 against the stored digits, all 7 outside the nine | **GREEN** |
| `TA-X-10` | W1 max_body_radius `[42.2038, 42.5433, 41.8029, 42.8368, 42.7285]`; max 42.8368 ≤ 43.758085 (margin 0.921 m) | **GREEN** |
| `TA-X-11` | W1 wall armed (r = 43.758085), clamps 0/0 on 5/5. *A port with no wall also scores zero* (§ F.5 cl. 6) | **GREEN** |
| `TA-X-12` | pool damage 0.0 on 25/25. Under `ORACLE` the aprons are **absent**, not present at zero | **GREEN** |
| `TA-X-13` | crits 0 on 25/25 | **GREEN** |
| `TA-X-14` | `cause == energy` 0 on 25/25. Releases are event-scheduled (22 on M-POL-2 s0). Purity SKIRT do-nots: 0 violations | **GREEN** |
| `TA-X-15` | (a) p01–p04 at tick 0 and p05 at tick **49** on 25/25. (b) **GREEN-BY-CONSTRUCTION**: one release tick is computed per point, so an intra-point stagger cannot be expressed | **GREEN** |
| `TA-X-16` | `n_pool_picks` **47** on 25/25; active points per wave == `V11-P06-1`; filtered-key counter `picks_suppressed = 18`. That counter is at the manifest grain, not per cell | **GREEN** |
| `TA-X-17` | `ρ = 8.0·u₂` with `u₂ ∈ [0,1)`, so exceeding 8.0 m is impossible. No per-body statistic is emitted | **GREEN-BY-CONSTRUCTION** |
| `TA-X-18` | polar `(−4.0, 4.9e-16)`; uniform-in-area `−5.656854`; box `(0,0)` (T-0) | **GREEN** |
| `TA-X-19` | **the port has no arrival limb.** `Kc2RtLaws.arrival_tick` has no caller in `sim/` | **GREEN-VACUOUSLY** |
| `TA-X-20` | 2.99 m hit · 3.01 m miss · hit from behind · hit from the side · 12 bodies inside → 12 hits (T-0) | **GREEN** |
| `TA-X-21` | 12 vector rows, 0 failures; purity no-bare-`round(`: 0 violations. **Site list re-verified as the row requires:** at engine `291dc582` the oracle's four quantisation sites are `threat.py:1451 / 1571 / 1604 / 1916`, all `round(` (half-to-even), and the gmag fold added none. The port's T-0 still cites `1402 / 1522 / 1555 / 1867`. **Only the citations are stale; the rule is unchanged** | **GREEN** |
| `TA-X-22` | flag cause 0 on 25/25 | **GREEN** |
| `TA-X-24` | `PhaseModel.ENGAGE`, DRIVER-OF-RECORD. The negative (`HASH` never evaluated, `kc2rt_fight.gd:1549`) is verified by search, not by a scanned assertion | **GREEN** |
| ⚑ **`TA-X-25`** | **(a)** refused 0 on 25/25, satisfied over an empty refusal set. **(b)** ⚑ the named counter `n_measured_offense_spawn` is **absent from every cell**. The partition identity does hold 25/25 on the proxy `time_to_kill.n_armed_died` (e.g. M-POL-2 s0: 91 + 42 + 6 = 139). **(c)** ⚑ **`Σ n_nodata_spawn_inert` per arm: M0 192 · M-POL-2 189 · M-POL-2-NULL 192 · W1 189 · W1-NULL 189. The row expects 0 on every arm** | ⚑ **RED** |
| `TA-X-26` | (a) join audit green. (b) sha verified and table loaded, but no call site is named. (c) 7,900 rows and 8 tiers; 790 records, 5 multipliers and wave-invariance are not emitted. (d) 0 formula disagreements; the single-call-site check is not emitted. **(e) the mean over `ARMED-464` is NOT EMITTED.** ⚑ The port's armed set is 122, so its figure could not be `0.2468965517`. That points RED; **I did not convert it** | **UNGRADEABLE** |
| `TA-X-27` | (a) the short-circuit scan is not emitted. (b) rules smoke: 58 checks, 0 failures, including degenerate `randint(30,30)` geometric consumption (supplementary). (c) 29 live sites; the p05 draw is elided per the ruling. (d) the 97/139 census is not emitted | **UNGRADEABLE** |
| `TA-X-28` | `n_leech_target_caps_applied` and `n_leech_tick_caps_applied` are not emitted; no oracle side is emitted. Per-tick cap `null` (MEASURED-ABSENT) | **UNGRADEABLE** |
| `TA-X-29` | (a) `PRED-GMAG-WHOLE` WHOLE: **193/154** and **527/104**. (b) declared composition: om = M_inst + own/100, leech DROPPED, dot and PCL take nothing; clamp cross-check 527 rows, 0 disagreements. (c) `z3` 10/10 agree (1.82 ×5, 1.83 ×5). (d) 29 records take the identity path. *Unexercised: 0 of 29 inert records fall inside waves 151–160* (WARN-4). **(e) the terminal ×3.406 / ×5.418 is NOT EMITTED.** Grains (INFO-2): `attr_limb_records: 193` beside `attr_limb_actors: 344` | **UNGRADEABLE** |
| `TA-X-30` | (a) halt declared as `HaltLimb.INCUMBENT @ 2.4 m` (census M10); no NaN test is emitted. (b) `n_bodies_halted_beyond_d_engage` is **NOT EMITTED** | **UNGRADEABLE** |

`TA-X-23` is struck and retired. `TA-X-06` is declared (§ 1).

---

## § 4 · THE RED: `TA-X-25(c)`, and its mechanism, derived and not inferred

**What the row says (§ F.2f):** at v3.4.2, `POOL-466` holds **zero** NO-DATA members. A port that spawns bodies it classifies NO-DATA has a **roster-basis error**.

**What the port holds:** its own roster assertions, which are emitted and all pass, are `NO-DATA over POOL-466 = 338`, `MEASURED-INERT = 6`, `MEASURED-OFFENSE = 122`. **That is the v3.3 table, to the digit.** `ta_manifest.roster.body_states_over_POOL466` says the same.

**What the pack holds, which I re-derived this session from `P-h`:** 109 pools over waves 151–160 give **466** members. `v20 ∩ POOL` = **122**. `w45_monster_offense_state ∩ POOL` = **342**, every one `MEASURED-OFFENSE`. `w44 ∩ POOL` = **4**. The union is **464**. The unarmed remainder is exactly `basilisk_a01` and `yetidire_a01`, as the prereg predicted by name.

**Why:** `loader/kc2rt_v3p4.gd` indexes `w40/w41/w44/w45` as rowsets, and its presence is asserted at gate G2D. **No fight-path consumer arms a body from them.** The runtime still declares `ABS-MONSTER-OFFENSE-NO-DATA-POOL466` ("338 of POOL-466 carry no offense profile") at v3.4.2, and census M17 still refuses on it.

**Magnitude:** on M-POL-2, 189 of 655 bodies (**28.9 %**) spawn NO-DATA and inert, plus 21 MEASURED-INERT. At v3.4.2 only 2 of 466 records are meant to be inert. Per-salt NO-DATA fractions are `[0.302, 0.226, 0.312, 0.237, 0.370]`. **Close to a third of the board does nothing, on a board the oracle arms almost completely.**

**Direction:** this makes the port **easier to survive**. It is one of three independent mechanisms behind *"the port clears to 160 while the oracle dies at 151–156"*. The other two are the holes in § 7.

---

## § 5 · THE HONEST `n` (§ C.8; legolas F-3/F-4)

**The 25 cells carry 10 distinct outcomes.** `{M0, M-POL-2-NULL}` are byte-identical per salt (`TA-X-03`). `{M-POL-2, W1, W1-NULL}` are byte-identical per salt (`TA-X-04`, plus `TA-X-06`'s declared relation, which is identity here).
* *"RED on all five arms"* rests on **two** independent sums, 192 and 189.
* *"0 of 25 cells died"* is **0 of 10**, with n = 5 per arm class.
* Every diagnostic below is a mean over 5 salts of one arm (**n = 5**, `ddof = 1`, df = 4). None carries a √25 claim.
* The draws are also clustered, 47 pool picks per cell (§ C.8 companion). **No per-wave figure rests on more than about 5 independent picks.**

---

## § 6 · WHAT ATTEMPT 2 NEEDS: repair versus emission

| item | kind | what closes it |
|---|---|---|
| `TA-X-25(c)` | **REPAIR** | Arm the 342 `w45` members, plus the 4 `w44` default attacks, on the fight path. Retire `ABS-MONSTER-OFFENSE-NO-DATA-POOL466` and re-point M17. Expect `Σ nodata = 0`, and MEASURED-INERT rolls only from the 2 named records |
| `TA-X-25(b)` | emission | emit `n_measured_offense_spawn` by name |
| `TA-X-07` | emission | `n_terms_accumulated` per cell. ⚑ With about 3,900–4,250 ticks and several hits per tick feeding `offered`, **the realised depth may well exceed 4,500**. In that case the row is UNGRADEABLE by its own clause (c), and emitting the count will say so honestly. That is a question for the prereg author before attempt 2, not something to discover afterwards |
| `TA-X-26` | emission | the call site; 790 / 5 / wave-invariance; (e) over the `ARMED-464` set expression. **(e) also depends on the `TA-X-25` repair** |
| `TA-X-27` | emission | (a) the scan; (d) the 97/139 census |
| `TA-X-28` | emission | both cap counters, on both sides |
| `TA-X-29` | emission | (e) the terminal multipliers at w159 and w160 |
| `TA-X-30` | emission | `n_bodies_halted_beyond_d_engage`; the NaN test |
| P-1 cl. 1a | emission | name the EXACT row in the M4, M10 and D19 notes |
| P-4 | emission | the runtime verifies reference members and cross-pin, and emits the result |
| P-5 | emission | header declaration of all four folds; refuse to boot on an unset one |
| labels | emission | `prereg_version`, `substrate_epoch`, the stale `ta_x_25` / `ta_b_15` / `TA-X-07` row text, and T-0's `TA-X-21` line citations |
| T-0 evidence | emission | fold T-0 / purity / rules / loader outputs into the pinned emission |

---

## § 7 · ⚑ THE PCL FLAG, AND A SECOND HOLE FOUND WHILE CHECKING IT

### 7.1 · PCL: CONFIRMED. The port drops every `percent_current_life` row, and **no EXACT row catches it**

drax's view-only trace was correct. **Code path** (`sim/kc2rt_fight.gd`):
1. `:1741–1748` computes the PCL magnitude (`player_hp × mag/100`, re-clamped, reclaim booked).
2. `:1750` books it to `conservation.offered`.
3. `:1787–1791` then takes the *unlisted damage type* branch. `player_resist` has no `PercentCurrentLife` key, because `player_kit.json` carries none: I enumerated all 26 `player.resist_pct[*]` keys. The row is **dropped into `conservation.dropped` with no counter.** It is not routed to the non-health count, because it is not declared absent.

**Empirical:** `intake_by_damage_family` has 17 families on every cell, and **`PercentCurrentLife` is absent on 25/25**. The pack carries **137 roster + 21 pet** PCL damage rows (`v21 ∪ y2`).
**Oracle:** `threat.py:1848–1880` applies PCL **unmitigated by resistance** with `om = 1.0`, reduced ×(1 − 0.26) by `defensivePercentCurrentLife`. The oracle's own comment puts it at **43.26 % of I-5's intake**.

**Which EXACT row sees it: none.**
* **`TA-X-07`:** the drop is booked as `dropped`, so the identity balances. **The conservation row absorbs the defect.**
* **`TA-X-29(b)`:** grades the **multiplier** (`om = 1.0` for PCL), which the port's fold returns correctly. **It grades the factor applied to rows that never land.**
* **`TA-X-09` and ceiling `C-h`:** I opened all 29 vectors. The 20 mitigation-order vectors are **physical-only**; their inputs are `raw / armor / res_physical_pct / absorption_pct`. **None is a PCL case.** ⚑ **So `GM-OQ-1` (widening `TA-X-09` to all 29) would not catch this either.**
* **`TA-B-12`** (intake) has no oracle side (`C-e`).

**A hole in the instrument, stated plainly: the port can drop about 43 % of the oracle's reference intake and T-A is green-shaped about it.**

### 7.2 · ⚑ HOLE-2: the port checks player death AFTER the tick's heal. The oracle checks it BEFORE

I found this checking why `hp_min` sits at **10.5616 HP**, which is exactly one tick of regen, in 8 of the 10 distinct outcomes.
* **Port:** `_tick()` resolves player→monster (the leech accrues as `healed`), then `_resolve_threat()` (`:1135`), which can take HP to 0, set `killer_id` and return. Then it applies `player_hp + regen + healed` (`:1138`). **Only after that** does the loop test `player_hp <= 0` (`:886` headless, `:973` in `play_step`, so **Matt's PLAY session has the same order**).
* **Oracle:** `run.py` takes `it_floor` at the intra-tick minimum and tests `hp_player <= 0.0 → player_dead` **before** the regen / ADCtH slot. Its own comment: *"the minimum HP … is its value RIGHT HERE, at the death check."*
* **Evidence:** `killer_id` is set on **9 of 10** distinct outcomes, yet `terminal_reason = cleared` on **25/25**. There are **47** sub-11-HP ticks across the 10 distinct cells: M-POL-2 s0 goes 17,399 → 9,881 → **0 → +10.56**, and so on. **The player dies and the same tick's heal resurrects them.**
* **Caught by:** **nothing.** `TA-B-01` is class V (report-only), and no EXACT row grades the death check.

### 7.3 · What the two holes mean for attempt 2. This is the part that matters

⚑ **Repairing `TA-X-25(c)` and emitting the six UNGRADEABLE rows could produce `PASS 28/28` on a port that still drops about 43 % of reference intake and still resurrects the player on a lethal tick.** Both defects run in the survival direction, and so does the red. A green T-A would then seal REFERENT-v1 on a port that cannot die the way the oracle does.

**Both are PORT defects, and T-A should be the place that sees them.** Adding a row after a graded result exists is the thing `WARN-16` and D4 guard against. v1.7 is immutable, and a new version with new rows written *after* seeing this run is a goalpost question. **So I route this and do not decide it.** Two options, for the conductor to put to Matt:
- (i) drax repairs both alongside `TA-X-25`, as port defects found by the grader, while the instrument stays blind to them.
- (ii) a v1.8 adds a PCL-delivery row and a death-order row before attempt 2, under Matt's word.

---

## § 8 · DIAGNOSTICS: reported, gating nothing (F5). Arm M-POL-2, mean of salts, n = 5

Every row prints: `@ coverage 89/89` · calibration `tpw ∈ [106, 185]` from `[M-POL2]`, **sealed 2026-08-25 on a pre-v3.3 substrate** (WARN-1) · realised tpw **392.88** · **dilution 2.431×** · **`[width VOID @ re-base — P-a's widths derive from the v3.3 sealed cells]`** · effective n = 5.

| id | grain pair | value (per salt) |
|---|---|---|
| `TA-B-01` | terminal wave | **port `[160 ×5]` on every arm, `cleared` 25/25.** Oracle `[M-POL2]` (sealed 2026-08-25, pre-v3.3 substrate): `M-POL-2 [156, 152, 151, 151, 156]`, `player_death` 5/5 |
| `TA-B-02` | per-tick / D | **0.937984** `[0.938008, 0.931631, 0.941738, 0.934335, 0.944209]` |
| `TA-B-03` | per-tick / D | 0.970107 |
| `TA-B-04` | per-tick / per-tick | 0.950961 |
| `TA-B-05` | per-tick / per-tick | 0.548108 (sd 0.162) |
| `TA-B-06` | **windows-with-plant / windows**, the statistic the port computes, not the v1.5 recovered one | 0.028653; `window_coverage = 61 / 392.88 = 0.155` |
| `TA-B-07` | per-tick / D | 0.062016 |
| `TA-B-08` | ordering | holds 5/5; *the sign may survive, the margin does not* |
| `TA-B-09` | per-tick / per-tick | 0.016499 |
| `TA-B-13` | extreme | `[42.2038, 42.5433, 41.8029, 42.8368, 42.7285]` |
| `TA-B-14` | raw counts | W1 vetoes 0 ×5, occupancy 0 ×5 (oracle 2 / 0) |
| `TA-B-15` | bodies / bodies | **NON-ZERO on 25/25: THE ANOMALY.** M-POL-2 `[0.302, 0.226, 0.312, 0.237, 0.370]` over 47 picks per cell; M0 `[0.223, 0.388, 0.353, 0.331, 0.272]`. Reference points **0.0000 / 0.0000**, not `0.3828` |
| `TA-B-16` | per-wave / per-wave | released ticks/wave 24.26 *(still one grain-mixed row; the 16a/16b split is owed)* |
| `TA-B-17` | per-wave / per-wave | stationary ticks/wave 11.68 |
| `TA-B-18` | per-wave / per-wave | motion-suppressed ticks/wave 5.44 |
| `TA-B-19` | ticks/wave, **the dilution factor itself** | 392.88 `[393.6, 387.6, 418.8, 339.6, 424.8]` |
| `TA-B-10 / 11 / 12` | no oracle side | M-POL-2 intake 389,959 HP, leech 1,522,579 HP (heal : intake ≈ 3.9) |

TA-B-16 to 19 are **scale-free by construction, not by measurement.** The calibration range [106, 185] cannot test that.

**Verbatim sentences the prereg requires:**
* *"`TA-B-02` and `TA-B-07` are ONE ROW WITH A SIGN FLIP (`released/D ≡ 1 − uptime`, exactly). They are not two pieces of evidence."*
* *"`TA-B-02`'s green in run #1 rested on the CLIP. The unclipped upper bound was `0.974330` and the port's `0.975570` EXCEEDED it by `+0.001240`."*
* *"`BAND / NON-DECISIVE / REPORT-ONLY`. A terminal wave inside or outside this band is not evidence of fidelity either way."* *"The oracle's sealed `M-POL-2` arm terminates at `[156, 152, 151, 151, 156]`, `player_death` on every salt. A port that clears to wave 160 has not survived a hard board; it has failed to be in one."* ⚑ **This run supplies that sentence's mechanism three times over: § 4 and § 7.1–7.2.**
* *"A band that rejects the oracle cannot grade a port."* (`TA-B-13`)
* *"This is the counter that carries `TA-X-06`'s ENTIRE MECHANISM, and it is the one the prereg declined to band."* (`TA-B-14`)

---

## § 9 · REPORT-FACE RULES (§ F.5 cl. 6–10), verbatim where the prereg requires it

**cl. 6, absences:**
* `TA-X-11`: *a port with no wall also scores zero.*
* `TA-X-12`: the aprons are absent, not present at zero.
* `TA-X-15(b)`: a stagger is unrepresentable.
* `TA-X-17`: green by construction.
* `TA-X-19`: no arrival limb exists, so `TA-X-21`'s `CEIL` is asserted in a vector table and never exercised.
* `TA-X-25(a)`: satisfied over an empty set.
* `TA-X-28(a)`: not reached (UNGRADEABLE).
* `TA-X-29(d)`: *unexercised: 0 of 29 inert records fall inside waves 151–160.*

**cl. 7:** *"`leech` and `intake` still have no oracle side in the seals (`C-e`). What HAS been measured off-seal is that the oracle's sealed stack KILLS THE PLAYER AT WAVES 151–156, four or more waves earlier than the referent's 160. The two replicas bracket the referent from opposite sides: the port ~15× LOW on intake per body, the oracle ~1.9× HIGH. A GREEN T-A IS COMPATIBLE WITH BOTH."* **§ 7 names two port mechanisms for the port side of that bracket.**

**cl. 8:** *"Three declared absences are the ORACLE's holes and not the port's defects. No row grades them and a port that does not implement them is CORRECT: `ABS-NINE-WINNER-SURFACE-HONEST-FAILS` (13 slots — 12 `NO-DAMAGE-DECODED`, 1 `RANK-UNASSIGNED`) · `ABS-GLOBAL-MAGNITUDE-FOLD-INERT-RECORDS` (29 records, 0 of them inside waves 151–160) · `ABS-C-I14-2-SOURCED-UNFOLDED` (a sourced wave-level physical modifier, ≤ 2.2 % pooled and exactly ×1.000 at w159/160, unfolded on BOTH sides)."*

**cl. 9:** *"The resume cadence of a starved channel is DECLARED, not sourced (`ABS-CHANNEL-STARVED-RESUME-CADENCE`; closer = Matt-to-do T32; the alternative `STUTTER_WHILE_HELD` is `STRUCTURAL-INFERRED` and is NOT adopted). And the oracle's starvation TERMINATION — the `break` at `run.py:2137`, reached through `refuses_activation` at `:2133` — is `UNSOURCED-INCUMBENT`: behaviour written by default long before the question was asked, carried unchanged and ratified by nothing. NO ROW GRADES THE PORT AGAINST IT."*

**cl. 10:** *"T-A compares the port and the oracle under the SAME scripted pilot and the SAME folds. It therefore cannot see the occupancy gap (`N` 1.43–2.30 across pilots against the referent's 0.72–1.84), cannot see the oracle's ~×1.9 over-lethality (`C-i`), and cannot see anything T-C is for. A PASS here means the replica matches the reference. It does not mean the reference matches Matt's video."* ⚑ **And, from this run: a PASS would also not mean the replica applies PCL or honours a lethal tick (§ 7), because no row looks.**

---

## § 10 · Carried obligations

**Discharged here:**
* jack-ryan v1.7 WARN-1: `declared_ungradeable` conformance, **met**.
* v1.6 WARN-1: `[M-POL2]`'s epoch printed beside `TA-B-01`.
* v1.6 WARN-4: the cl. 6 prints for `TA-X-25(c)`, `TA-X-28(a)` and `TA-X-29(d)`. **`TA-X-25(c)` is not absence-satisfied; it is red.**
* v1.6 INFO-1: `TA-X-29(d)` treated as gradable.
* v1.6 INFO-2: grains labelled.

**Still owed:** `OQ-9`'s *"wrong about every hit the player takes"* belongs on the **W4 packet** face. It is sharpened by § 7.1: the 29 vectors carry no PCL case at all.

*Filed by gamora, W3 grade seat. No code. No push. K-7 held. The verdict file is `kc2play.ta_verdict.v1`, prereg_version `"v1.7"`.*
