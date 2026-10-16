# Finding — 2026-10-16 — JOIN-1 J4b design-finding chain (tier 1, row 22, tier 2, KP-500) — delta Gate-2

**Reviewer:** jack-ryan
**Severity:** WARN (verdict: **PASS-WITH-NOTES**; 0 BLOCK / 2 WARN / 5 INFO). Rows 23/24 are not graded here; they get a separate delta.
**Target:** ledger KP-493…503. Godot: tier-1 maps, the row 22 levers, tier-2 levers `08372d9` (fail-first `824fa8c`), the 13 tier-2 arms, KP-500 `12d4eff` / `d6cf39b` / `fb4d5a9`, trace `a7044d7`. Engine: replay bindings, mirror `c1cc27c3`. Collab grades: `5e9c7e1b3`, `567ac3dc9`, `2b281856b`, `9e6ba806c`, `13030889d`, `1becafb0f`.
**Developers:** drax, gamora; conductor rulings KP-500 and KP-503
**Principles applied:** REVIEW_PROCESS 1, 2, 4; Disciplines #8, #10, #12; prereg §§ 2, 8; ADDENDUM-A § F

## Independent re-derivations (my scripts, against the bulk grains)
Every figure below matches gamora exactly:

| Item | Statistic | Result |
|---|---|---|
| NC-ANCHOR | whole-cell M-c, raw vs car2 | **311,690.5 vs 1,991,085.2**, 0/25 against; raw dies in **25/25** |
| Row 19 | Σ intake, block-gd vs car2 | **6,305,422 vs 6,338,689**, 9 / 10 / 6 ties. Strict reversal |
| r_HP order | offered per tick | R2 **5,670,849** < R1 **7,222,531** < non-ladder **9,467,914**, 0/25 and 25/0 |
| Row 11 | Σ applied | 24-cell **3,286.8 M vs 2,716.4 M** (+21.0 %, 24/0); 25-cell **25/0** |
| Row 12 | Σ applied | 24-cell **21/3**; 25-cell **22/3** |
| Row 13 | Σ applied | **25/0** up |
| Row 14 | Σ applied | 24-cell **−0.07 %, 9/10/5**; 25-cell **−0.02 %, 10/10/5** |
| Worst-case M0 re-emission | file comparison vs `775e29d` bulk | **0/21 files differ**; vs raw **20/21 differ** (G6 is empty in both) |

## Q1 — FALSE AS REGISTERED / failed NCs carried as results
**Carried correctly in gamora's prints:**
- rows **11, 12, 13** FALSE (FAILED NC);
- row **19** FALSE (FAILED NC, not discounted);
- **fraction (b) 13 + 0 / 23 against the predicted 22 + 1 / 23: FALSE AS PRE-STATED**;
- row 22's RI prediction FALSE, with the row ACTIVE;
- **row 21's "mana-bound phase"**: labelled *"not delimited in registration … POST-HOC operationalisation"*.

**WARN-2 — fraction (a) is missing from the chain.** My ruling `0fb1ae171` recorded **fraction (a) FALSE AS PRE-STATED, 31/32 of record (29/32 pack reading beside)**. No tier-1 or tier-2 print carries it. Add it to the chain's results table and to the J4b close-out.

## Q2 — KP-500 (Confusion / Convert → drop)
- **Native in the oracle: confirmed in code.** In the sealed oracle `control_application.py:911–916`, a non-involuntary family on a player books `EffectModel.DECODED_ZERO` ("Confusion / Convert / Fear / Taunt — DECODED player-side ZEROS (D-7 § 3.4)").
  - **D2 side:** "no player confusion or convert state" is asserted in `739da26ae` without a primary-source cite. It agrees with my understanding, but **legolas should cite it** (Arreat Summit / D2MOO) for the record (INFO-1).
- **Authority: within the conductor's power.** (A) chooses **between nothing**: both games agree, nothing is invented, and (B) was rejected for that reason. It is labelled POST-HOC SEMANTICS and reported to Matt as reversible. It moves **no primary cell**: car2 ran under the old registry with **0 refusals**, so no Confusion was ever delivered to the graded primary. It stays within KP-420's GD-default boundary rule, and no Matt ruling is required.
- **The bind guard: complete, and conservative.**
  - It enumerates the sealed fold's `control_rows` (`kc2rt_control.gd:222–248`). That table is built once from the **whole pack table**, filtered to slot surface, `OK` status, kind / grade and rows with a min value.
  - The fold's **only** delivery path reads `control_rows` (`:402`), so no family can be delivered that the guard did not enumerate.
  - The table is a **superset** of what this lineup delivers. That is why K3 (car2 M0/1, Confusion present but never delivered) refuses at bind under the old registry.
  - In short, the guard can over-refuse but cannot miss. "Profiles" in the ruling text is loose; the enumeration is table-derived. The lineup-derived census is correctly on J4a (N-10).
- **The 24-cell and 25-cell labels: see WARN-1.**

**WARN-1 — the runs gate on the body arms.** Prereg § 8 lists *"A 'runs' FAIL"* as a halt, and the grader's `runs_gate` fails on any raised cell. Each of the three body arms had one cell raise `ControlFamilyUnmapped: Confusion`.
- So **the registered status of rows 11, 12 and 14 is NO VERDICT (runs FAIL)**. It is *not* the 24-cell grade.
- The 24-cell grade drops a cell after the fact (named, but still a drop). The 25-cell grade is a rerun under a post-hoc semantic (KP-500).
- **Relabel both:**
  - registered = "RUNS FAIL → NO VERDICT (1 cell raised, named)";
  - printed = "24-cell, refused cell excluded (POST-HOC)" and "25-cell, CELL RERUN UNDER KP-500 (POST-HOC SEMANTICS)";
  - **neither "of record"**.
- **No conclusion moves.** Rows 11 and 12 are FALSE on both prints, row 13 had no refusal, and row 14 is a pass on both. Fraction (b) is unchanged.

## Q3 — the body-arm NC design: AGREE, with a sharpening
- **Agree on the statistic.** Σ applied, HP-capped, over a board she clears completely, measures **the board, not her output**. It is **confounded by construction, and the confound pushes the opposite way.** A body off lengthens the clear (63,464 vs 34,088 ticks for Fire Ball off), and the longer clear brings more summons and more leech healing (275 M vs 18 M), so the capped total *rises*.
- **Per tick, my re-derivation shows the M-c statistic does discriminate:** M-c falls in 25/25 cells (Fire Ball), **23/25** (Meteor) and **24/25** (splash). Pyre is mixed: **12 down / 8 up / 5 ties**, and it is a small share of damage.
- **Agree with the J4a carry** ("NC statistics per tick or uncapped"). I add that every registered NC gets a written **"can this fail, and which way does the confound push"** check before registration.
- **Reflexive:** my own prereg Gate-1 (`09f080754`) passed these four NCs without catching the cap-and-clear construction. I am adding that check to my Gate-1 list.

## Q4 — row 14: your disposition is right; strengthen the label
- Rows 11–13 are carried as failures, so row 14's pass must count by the same registered rule. **ACTIVE as registered is correct.**
- But row 14 used the **same non-discriminating statistic** as 11–13, so its pass carries no evidential weight. Its per-tick M-c is also mixed (12 down / 8 up).
- **Label:** *"ACTIVE AS REGISTERED — NC statistic non-discriminating by construction (as rows 11–13, KP-501); LOW EVIDENTIAL VALUE"*.
- **Fraction (b) print:** "13 ACTIVE (row 14 low-evidential) + 0 RI / 23".

## Q5 — out of tree / zero sealed lines: CONFIRMED
- **No runtime files.** `08372d9`, `a7044d7`, `12d4eff` (and `d6cf39b`, `63af677`, `f25ee1f`, `db3fff2`) touch **0 files under `kc2_runtime/`**.
- **Digest unchanged.** The runtime tree digest at HEAD recomputes to **`fb49080f…`** (107 members, 0 mismatches), and `kc2_runtime/` is clean.
- **The trace overrides are observe-only.** `_drive` and `_dot_open` read state before and after `super()` and write only their own logs. KP-500's change is confined to the out-of-tree `kc2rb_d2_laws.gd` and the lane.

## Notes (INFO)
- **INFO-1:** legolas cites the primary source for "no D2 player confusion / convert state".
- **INFO-2:** row 22 R3 (gd) rests on the sealed counters in drax's `verdict.json`, outside the grain set. It is labelled as such, and is acceptable.
- **INFO-3:** the worst-case re-emission confirmation holds on all 21 files. drax's "0/14" counted a subset.
- **INFO-4:** ADDENDUM-B off/off and the r_DMG orderings are carried with their ceiling / low-evidence labels. No change.
- **INFO-5:** I did not re-run every arm's replay (gamora's and drax's PASS lines stand). My re-derivations cover the registered statistics above.

## Action
- [ ] gamora: WARN-1 relabel on rows 11, 12, 14; WARN-2 put fraction (a) into the chain table; the row 14 label (Q4).
- [ ] legolas: the D2 citation (INFO-1).
- [ ] jack-ryan: the NC confound check added to the Gate-1 list (Q3).
- [ ] Matt: none. KP-500 stays within conductor authority and is reported as reversible.

## References
- grains `/Users/admin/Games/join3c-bulk/{car2/*,t2/*,kp500/*,car-wc-confirm}`
- `reincarnated-engine/src/reincarnated/simulation/kc2/control_application.py:895–920` (read-only); `reincarnated-godot/kc2_runtime/sim/kc2rt_control.gd:66, 222–248, 402`
- `agentic_orchestration/gamora/analyses/2026-10-15-join1-j4b-{TIER1-AND-ROW22,TIER2}/`, `…/2026-10-16-join1-j4b-CONFUSION-REFUSAL/`
