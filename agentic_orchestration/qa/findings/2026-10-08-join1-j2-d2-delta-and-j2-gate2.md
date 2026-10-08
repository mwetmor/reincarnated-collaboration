# Finding — 2026-10-08 — JOIN-1 J2: the D2-gate delta (port hook) + the J2 Gate-2 on the whole

**Reviewer:** jack-ryan (DEV-MODE Gate-2, BLOCK authority; KP-342…351)

**Severity:**
- **(a) D2 delta: PASS-WITH-FINDINGS** (0 BLOCK · 0 WARN · 3 INFO). KP-312 condition 4 is met, so work may depend on runtime **X = `8a4da5f8…`**.
- **(b) H-18b: DECLARED, not added.** A port-side refusal is owed, out of tree, with no runtime change.
- **(c) KP-348: CONCUR.**
- **(d) The two D3 misses: honest; both upheld as misses.**
- **(e) The invariance-script note: ACCEPTED,** with a standing rule.
- **J2 Gate-2 on the whole: PASS. J2 is DONE,** with the carried items in § 7.
- **Decisions-log entry written** (engine `design/decisions/decisions-log.md`, "2026-10-08 — JOIN-1 J2: rulebook v0 is accepted …").
- **Matt:** nothing new to rule. Two things are on his calendar already: the windowed `.app` self-test, and the future second KP-312 ruling (§ 7).

**Machine rule (KP-346) honoured.** No heavy-lock run was made at this Gate. Every port claim below was re-derived from committed evidence or from git, in seconds of CPU. The one Python check was import-only (P-J2-5's spot value).

## Pins derived at this Gate

| artifact | value | label |
|---|---|---|
| godot `1b244fb` (= tag `kc2/referent-v1-sealed-r2-runtime-kp333-d2b`) and HEAD | `kc2_runtime` tree `416c7ffe…`, identical at both; clean | GIT TREE OID |
| runtime of record | `8a4da5f8247623776393b82ca513c579a2445f08bd1b3e17fe3e8c48e9735c0b` (`kc2_runtime/MANIFEST.json`) | FILE (runtime tree digest) |
| `0aabbdf^..0aabbdf` (the hook) | `sim/kc2rt_fight.gd`, `sim/kc2rt_summons.gd`, `sim/kc2rt_gd_engage.gd`, `MANIFEST.json`, and nothing else | diff |
| `0aabbdf..1b244fb` within `kc2_runtime/` | `tests/kc2rt_booking_census.gd` (49 changed lines) + `MANIFEST.json` (the file sha + tree digest) | diff |
| engine rulebook worktree | `0dda17bd…`, tree `cb38bbdf…` (the mirror's re-pin target, per gamora's MIGRATION `543c10d4`) | COMMIT / GIT TREE OID |

---

## § 1 · (a) The D2 delta

### 1.1 Re-derived here

- **Approved scope.** P1 `pass: true`, `sites_equal_approved_set: true`. I also read the guards myself at X:
  - **ADJ-1 holds.** H-1's else-branch is `rulebook.pth_equation(_oa_for(rec), player_da * r8_da_multiplier())`, i.e. the sealed DA expression.
  - **ADJ-2 holds.** H-1 and H-2 are separate guards, and the to-hit roll (`_trng().randi_range_at(SITE_TO_HIT, …)`) is unguarded, at base indentation, between H-2 and H-3.
  - **ADJ-3:** P1 asserts `res_used(` 1× and `_physical_applied(` 1× in `_mitigate`'s else-branch, and no `rulebook.mitigate(`. The composed `_mitigate` grid is 500/500 equal to `Forms.mitigate` and 500/500 equal to the null branch.
  - **ADJ-4 / INFO-D1-1:** the mirror is re-pinned to `0dda17bd`. GRID PASS 102,699 / 102,699, and NC-D1-a RED.
  - **ADJ-5:** the re-pin grid carries `hitacc` 34/34 and `hitacc_kit` 2/2 bit-equal. P5 shows H-18 at kit 200 as REACHED-INSENSITIVE, declared in advance; that is the saturation ceiling, reproduced rather than fixed.
  - **ADJ-6:** the D3 NC-J2-2 pair is instrumentation-only (§ 4).
- **ORACLE identity at X.**
  - **T-A `cell.json` at X is FILE-equal to KP-310's on 25/25 cells.** I hashed both directories (`2026-10-07-ta-preread-kp310-472cffc4-cells` vs `2026-10-08-ta-preread-d2b-8a4da5f8-cells`). This is stronger than the claimed "cell digests + terminals".
  - Both J-S8 diffs (`p4-js8-port-oracle-D2`, `join-gd-25`) read `all_equal: true`.
- **The census relocation is digit-only.** Within `kc2_runtime/`, every changed line of `kc2rt_booking_census.gd` pairs with its counterpart once digits are removed. The only unpaired lines are the two hex fields of `MANIFEST.json`. **No sim file is touched,** which matches DIGEST-BRIDGE's `sim_files_identical_between_0aabbdf_and_1b244fb: true`.

### 1.2 Accepted on the evidence (KP-346: no re-run)

- P5 reach: 17/18, with H-10 under NC-4 ending at the sealed twin's point, all 7 grains equal.
- G3 25/25 = KP-310, `trace_sha256` included.
- § 4.7: 4 modes × 5 seeds identical.
- J-S8 port null: 7/7 over 25 cells at `cbe8e274`, plus the bridge cell at X. The sim is identical between the two digests.
- attempt-2: 54/0.
- `.app` clean of `res://join/`.
- Port pack loader: JOIN-only; P-J2-9 31/31 on the port.
- P-J2-11: stage 2 169/169, stage 1 `schema-change-owed`.
- P-J2-12: 2,352.
- Port structural rows: one prediction miss, the ADJ-3 transcription site, disposition TRANSCRIPTION.
- D3: port `JOIN[warlord, GD]` 7/7 at two runtimes, from the pack.
- Perf parity at about ±500 µs/tick resolution.

### 1.3 INFO

- **INFO-D2-1 (#73).** `DIGEST-BRIDGE.json` still reads `"t_a_pre_read": "OWED at 8a4da5f8"`, but the T-A pre_read at X landed in `c625ff9`. The record of the bridge does not carry the state. Append a line naming `2026-10-08-ta-preread-d2b-8a4da5f8-cells` and this Gate's 25/25 FILE-equality. Do not edit the earlier text.
- **INFO-D2-2.** The windowed `.app` self-test is **owed**. It was skipped with the declared flag, because it drives Matt's display during C-9. It is not a KP-312 condition, but it is the build's standing GREEN criterion. **Nothing ships to a player-facing `.app` from X until it runs.**
- **INFO-D2-3.**
  - Matt approved **one** hook commit. The approved change landed as **two** commits: `0aabbdf`, and the census relocation `1b244fb`.
  - The runtime of record is the second.
  - The intermediate `cbe8e274` is tagged and accounted for in the bridge.
  - The record should say "the approved change set", not "the commit".

## § 2 · (b) H-18b: the bleed rider is not gated on cadence in the port

- **Confirmed.** Python gates the bleed rider on the cadence verdict: `run.py:3312-3313`, `if po_hits:` before `apply_bleed`.
- **In the port:** H-18 guards only `_resolve_channel()` on `po_hits` (`kc2rt_fight.gd:1966-1972`). `_secondary_streams(disc_hits)`, which applies the bleed rider, runs **ungated**.
- **At GD this is identity,** since every channelling tick hits. It matters only at kit AS ≠ world AS, where the two mirrors diverge.

**Ruling: do NOT add the site in J2; DECLARE it, with an out-of-tree refusal.**

- **It is within J2-forms scope.** It is row 31's reach, so KP-333's delegation would cover it. **But I decline to add it now:**
  1. it changes nothing on any J2 graded profile, all of which are at GD;
  2. it moves the runtime digest again, which means repeating the full KP-312 proof set (T-A, G3, § 4.7, J-S8) during the C-9 priority window;
  3. J3's L-01 work (kits above the world clock; E4 § 1.4) rewrites the cadence gate anyway.
- **Owed (drax, out of tree, no runtime change):** the port JOIN session tool **refuses** any profile with `kit_as_pct ≠ world_as_pct` unless the run is NON-GRADED-CONTROL. The refusal message names H-18b. Add one test.
- **Consequences:**
  - P5's H-18 kit-98 probe stays a reach probe and is **not** cross-mirror evidence against Python's NC-J2-5c.
  - H-18b joins the **J3 sealed-runtime change**, under its own (second) KP-312 ruling, alongside the out-of-form lever sites.

## § 3 · (c) KP-348: the census relocation ruled covered by KP-333. CONCUR.

- Unlike the V22 case I dissented on at Gate-1 § 8(b), this adds **no input and no behaviour**. It restores a sealed self-check (the booking census, which pins 47 rows by line number) that the approved hook made stale by shifting lines.
- It is digit-only and sim-untouched (§ 1.1).
- The precedent is every earlier runtime change, each of which relocated the census in the same commit.
- T-A at X being FILE-equal to KP-310 on 25/25 is the decisive proof that nothing the census guards moved.
- **The defect was the omission, not the relocation.** drax self-reported it and launched nothing further until it was ruled. That is the correct conduct.

## § 4 · (d) The two D3 misses: honest, both upheld

1. **NC-J2-2: count 23,863 vs Python's 26,406.**
   - The prediction carried Python's count onto a different population.
   - Both twins change applied damage, so the port's `--draws` replay desynchronises: 7,330–9,448 draw mismatches per arm, **equal across the pair**. The port then falls back to its own generator, which is the declared hybrid-tail mechanism (NC-3c precedent).
   - The pair is still like-for-like, because both sides share the same desync.
   - The substantive clauses all **held exactly**:
     - `applied` equal on 100,632 / 100,632;
     - 0 rows on one side only;
     - every armour packet differs (23,546 Physical + 317 SlowPhysical);
     - 0 other packets differ.
   - **Miss upheld.**
2. **Field list: `armour_branch` not predicted.**
   - The port emitter's region record carries the stage-1 input's absorb/overflow, recomputed under the sealed order label. Python's region record does not carry it.
   - It is instrumentation, not outcome.
   - **Miss upheld.**

**Also upheld as recorded:**
- P5's H-18 G7 wording miss: the world-clock fields were unchanged; the wave tick spans moved.
- The port structural-row miss: the ADJ-3 site is a TRANSCRIPTION.

## § 5 · (e) The invariance-script note

The POST was emitted at the D2 tag. Stream 1 (ROWSETs) and stream 3 (stderr) are EQUAL. Stream 2 (normalised stdout) differs in **exactly one** line: the start-up-limbs provenance line (`L2 HEAD …`, `L3 tree …`), which names the runtime under test.

**ACCEPTED.** That line changes by construction whenever the runtime digest moves.

**Standing rule for every future sealed-runtime change:** either
- (i) declare that single line in the PREDICTIONS before the run, as was done here; or
- (ii) amend the pinned normaliser to strip it, with its own negative control (a second, behavioural line difference must still go RED).

**Never both silently** (#75 cl. 6).

---

## § 6 · J2 Gate-2 on the whole

### 6.1 Charter § 4.3 / § 4.7 / § 5 row J2

| Row | Verdict |
|---|---|
| § 4.3 (i), the J-S8 numeric fixture diff | **GREEN on both mirrors.** Engine: FILE-equal 7/7 at rulebook `5779b342` (E3), `a3eb0e54` (E4), `4da5044b` (E5, PACK), `0dda17bd` (Gate-2 owed), each re-hashed by this Gate across the sittings. Port: 7/7 ROWSET at `cbe8e274` and at X |
| § 4.3 (ii), the EXECUTES rows TA-X-07/20/29/30 | **Reported equal** on the engine (E3, E4, E5, Gate-2 owed) |
| § 4.7, ORACLE / PLAY invariance at every join-path commit | **Held.** Engine: § 4.7 v3/v4 ORACLE BYTE-IDENTICAL at every gated HEAD. Port: the KP-312 proof set at X (§ 1) |
| J-P2 § 5, controls RED before green | **Per mechanism, satisfied** (E4 § 1.6). Port controls: D3 |
| B0-N C-1(a)(b) | (a) reproduced (E3 § 5); (b) never arose |
| KC-1b delta; INFO-C1 | discharged (W1; `conversion.py`; P-J2-7 corpus) |

### 6.2 The predictions (design note § 7.1, as amended)

| P | Status |
|---|---|
| P-J2-1 | ✓ at every engine commit |
| P-J2-2 | ✓ (FILE-equal, four rulebook commits) |
| P-J2-3 | ✓ 440/440, engine and port |
| P-J2-4 | ✓ 0 bits differ |
| **P-J2-5** | **PARTIAL.** 74/74 measured path pairs ≥ 100 (min 105.98). I spot-checked the table's minimum, 103.5368 at DA 2770.09, and the threshold **DA\* = 2897.2555** with the sealed equation. **122/196 path pairs are UNMEASURED,** and the design's `OffenseHitUndecided` guard is **not built**. The referent's `HIT_CHANCE = 1.0` is a theorem only on the measured 37.8 %. This does not block J2: at GD the sealed constant stands, and JOIN reproduces it. **Owed before any non-referent defender (J4a):** source DA, or build the guard |
| P-J2-6 | ✓ (C-1(a)) |
| P-J2-7 | ✓ corpus level (R-CV1 stamped) |
| P-J2-8 | ✓. The committed scan has 20 holders and 0 STALE. One characterisation miss is recorded: the `SOULFIRE_PERIOD_S` holders hold the shared `Cited` |
| P-J2-9 | ✓ engine (31/31, independent at S1/E5) and port (31/31) |
| P-J2-10 | ✓ (port § 4.7, JOIN 7/7, the hit grid through the mirror) |
| P-J2-11 | stage 2 ✓ 169/169; stage 1 `schema-change-owed` |
| P-J2-12 | recorded (2,352); X-1 OUT |
| P-J2-13 | ✓ as restricted (NC-J2-11a) |

**Verdict: PASS. J2 is DONE.**

## § 7 · Carried forward (none blocks J2's DONE)

**To J3 (conductor's owner-eye sheet; a second KP-312 ruling is needed for the runtime parts):**
- the intake order's single home (NC-J2-2);
- L-01 above the world clock (NC-J2-5b);
- the `resolve_attack` transcription for intake L-06 (E1-b R-3);
- **H-18b** (§ 2);
- the out-of-form lever sites (L-02, L-03, L-07, L-08, L-06(b), offense L-04);
- L-08 ratification.

**Owed elsewhere:**

| Item | When | Owner |
|---|---|---|
| L-17 ratification | J4b | — |
| P-J2-5 coverage or guard | before any non-referent defender (J4a) | — |
| V22 stage-1 operands | `schema-change-owed` | star-lord S1, via elrond J-L4 |
| the H-18b refusal (§ 2) | — | drax |
| INFO-D2-1 (bridge record) | — | drax |
| INFO-D2-2: windowed `.app` self-test at X | — | Matt's calendar |
| the sealed port's `fsum` special values and disc `sqrt` | new Matt questions only if a reachable path ever needs them | — |

## References

- godot: `0aabbdf`, `1b244fb`, `a8ed50b`, `f1b5e83`, `c625ff9`, `48dfba1`, `7243f3d` · `/Users/admin/Games/reincarnated-godot/evidence/join1/j2-d2-hook/` (RESULTS.md, PREDICTIONS.md, `p1_hunk_audit.json`, `p5/`, `DIGEST-BRIDGE.json`, `p4-*`, `census-relocation-kp348/`) · `…/j2-d3-join/` · `…/j2-d1-rulebook-mirror/repin-0dda17bd/` · `…/evidence/kc2-play/2026-10-07-ta-preread-kp310-472cffc4-cells/` and `…/2026-10-08-ta-preread-d2b-8a4da5f8-cells/` · `kc2_runtime/sim/kc2rt_fight.gd` (:1966-1972, the H-1…H-3 region)
- engine: `src/reincarnated/simulation/kc2/run.py` :3312-3313 · `/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/gamora/analyses/2026-10-07-join1-j2-gate2-owed/README.md` · `design/decisions/decisions-log.md` (2026-10-08 entry)
- prior J2 findings: `…/qa/findings/2026-10-07-join1-j2-{design-gate1, w1-gate2, e2b-gate2, e2c-e2e-gate2, e3-gate2, e4-d1-gate2, s1-e5-gate2}.md`
