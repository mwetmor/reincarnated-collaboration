# Finding — 2026-09-29 — Run KC2-PLAY · T-A grade, attempt 1 of 2 under prereg v1.7 (DEV-MODE Gate-2, W3 seal)

**Reviewer:** jack-ryan
**Severity:** **the GRADE: PASS**, with 2 WARN and 2 INFO. **The RULINGS (KP-113): 1 BLOCK**, with 5 WARN.
**Target:** gamora grade note `agentic_orchestration/gamora/notes/2026-09-29-kc2-play-ta-grade-v1p7-attempt1.md` (sha256 `9778b4de…`) and verdict file `…-ta-verdict-v1p7-attempt1.json` (sha256 **`9be2d56bfdc49c51c611402ec953b5f59dbfc0c866cdaf5201e0e57d74df08b2`**, re-derived first, matches), collab `15d6f5ce8`. Conductor rulings: charter row KP-113, collab `266c6edd6`.
**Emission:** godot `41ec7cd`, `evidence/kc2-play/2026-09-29-ta-run2-v1.7-cells/`, MANIFEST sha256 `bddc501a35a4…` (re-derived, matches). Prereg v1.7 sha256 `552d9fae…` (re-derived, matches). Model pack `5cab7433…` read member-by-member where cited below.
**Developer:** gamora (grade) · gandalf (rulings) · drax (port)
**Principles applied:** REVIEW_PROCESS #1 (math before code) · #4 (the committed record is the truth) · #5 (severity matters). Disciplines #11 (empirical inspection over assumption) · #12 (a semantic shift is named) · #19.1 (the cheapest refuting test per claim) · #80 (a row that cannot fail is not a test). ADR-002 (escalation tier). Charter § 4 item 4 (WARN-16: a prereg change after a graded run is a HALT). Prereg v1.7 § F.1a (a structural row carries an expiry).

---

## What I found

### A. The grade: the mechanics hold
- **Integrity.** I re-derived the verdict file, the emission MANIFEST and the prereg. All three match. The verdict file conforms: `prereg_version "v1.7"`, `declared_ungradeable` ids are exactly `["TA-X-06"]` with authority `Q83(b) / KP-110` (the WARN-1 conformance check I set at pre-read), and counts are 28 EXACT = 21 green + 1 red + 6 UNGRADEABLE.
- **The red, re-derived independently from `P-h`.** 109 pools in waves 151–160 give **466** members. `v20 ∩ POOL` = 122, `w45 ∩ POOL` = 342 (all `MEASURED-OFFENSE`), and `v20 ∩ w45` = 0. The union is **464**. The residue is exactly `basilisk_a01` and `yetidire_a01`. The emitted per-arm NO-DATA sums are 192 / 189 / 192 / 189 / 189. On M-POL-2 that is 189 of 655 bodies, or 28.9 %. **`TA-X-25(c)` is red as written, and `STRUCTURAL` is the correct verdict under § G.**
- **The holes, confirmed on the code.**
  - **PCL.** `kc2rt_fight.gd:1750` books PCL rows to `offered`. Then at `:1785–1791` they are dropped, because `player_resist` has no key for them, and **no counter records the drop**. The pack carries 158 PCL rows (`v21 ∪ y2`, 137 + 21). `PercentCurrentLife` is absent from all 25 cells.
  - **Death order.** The port resolves threat (`:1135`), then regen and heal (`:1138`), then tests death (`:886`, and `:973` in PLAY). The oracle tests death at `it_floor` before the regen slot (`run.py:3786`). It also breaks out of the attacker, aura and DoT loops on a lethal hit (`:3504`, `:3635`, `:3713`, `:3719`). In the emission, `killer_id` is set in 22 of 25 cells, and all 25 end `cleared`.

### B. The red is not what KP-113 says it is
**The pack carries fight-grain damage magnitudes for only 4 of the 342 records that `w45` re-classes `MEASURED-OFFENSE`.** Those 4 are the `w44` default-attack records: `ghost_a01`, `ghost_a02`, `groblefrost_a01` and `wendigocannibal_a01`. **The other 338 carry upstream slot and skill names, damage-field counts (`w40.n_damage_fields`) and OA/DA equations (`w42`), but no damage row.** Of the 487 offense-bearing slot skills on those 342 records, 134 have damage rows anywhere in the pack. For example, `aetherialbloater_biteweak.dbr` appears in no member file except as a name. **The rebase note says the same about itself.** `P-e` § 6.1 reads *"MAGNITUDES … No damage number is predicted here"*, and § 6.3 reads *"The oracle itself ran on baton-scoped offense … a re-based reference is a NEW arm with a NEW seal."* The coverage row `W48-COV-0`, which reads *"a_damage_rows … uncovered_after_v3p4: 0"*, counts upstream damage FIELDS at the damage-ROW grain. **That is a grain mislabel, and it is the source of this row's premise.**

**The oracle does not arm these bodies either.** `threat.load_profiles()` builds profiles from `pm2_tg2_attack_damage.csv`, which covers **128** POOL-466 records (`BOTH-128`). `run.py:1754` sets `prof_of[aid] = engine.roster.get(...)`, and `:3464` / `:3506` skip `prof is None or not prof.can_swing`. **So the sealed oracle that kills the player at 151–156 did so with the same ~⅓-inert population.**

Consequences:
1. **The survival-gap attribution is refuted for this mechanism.** Grade § 4 "Direction" and the KP-113 headline (*"THE PORT WAS FAR TOO EASY: ~29 % OF BODIES SPAWNED INERT"*) present NO-DATA as one of three mechanisms by which the port outlives the oracle. The inert population is shared by the port and the oracle, so it cannot explain the port-versus-oracle difference. **The two holes remain as derived mechanisms. This one does not.**
2. **The prescribed repair cannot be built from the pack.** The instruction is to "arm the 342 w45 members". The 4 `w44` records are armable from the pack, and that part is a genuine port defect. **The other 338 have nothing to arm them with.** A port can make `Σ n_nodata_spawn_inert == 0` in one of three ways:
   - **re-label** the 338 as `MEASURED-OFFENSE` or `MEASURED-INERT` with no behavioural change. That is a hollow green (#80). It is visible only in the `(d)` count, which is reported and not graded.
   - **invent** magnitudes. Law 3 forbids that.
   - **obtain** magnitudes. That is a pack change, which is the conductor's own ruling (iii) → **HALT to Matt**.
3. **This is F.1a recurring in the opposite direction.** The v1.6/v1.7 zero is pinned to the pack's STATE grain. At the grain the fight path and the oracle both consume, the pool still holds 338 NO-DATA members. **A port faithful to the oracle reds `(c)` on every arm.** This is the same shape as the `TA-X-06` objection that took Q83 to Matt before attempt 1: *a row no faithful port change can move.*

### C. `(b)` is red on its own text, so attempt 1 is consumed on a genuine port defect either way
`TA-X-25(b)` asserts that the three counters are **"PRESENT and EMITTED"**. Its RED column reads *"the port has re-created the oracle's own silence."* `n_measured_offense_spawn` is absent from every cell, and the verdict file records `"NOT EMITTED (proxy …)"`. The grade reports the proxy identity but gives no clause verdict for (b). **Read as written, (b) is RED.** `STRUCTURAL`, and the spent attempt, therefore rest on an emission defect in the port that does not depend on B. The verdict does not change. The grounds should say this, because it is what keeps "attempt 1 is spent" sound once B is accepted.

### D. Harness surfaces that could flip a verdict (item 3)
gamora named three surfaces: the `ta_x_25` class text, the `ta_b_15` reference points and the TA-X-07 conditions. **I found four more that carry a verdict-shaped value**, all in `kc2rt_ta.gd` output:

| surface | literal reading | the flip |
|---|---|---|
| per-cell `conservation.green: false`, `tolerance: 1e-06`, `terms_expected: 6` | TA-X-07 is failing | UNGRADEABLE/green → **RED**; it would make attempt 2 STRUCTURAL. v1.7 is relative `1e-12` over **seven** quantities, with a depth budget |
| `ta_manifest` `relation_rows_RAW_not_graded.TA-X-06` gives `holds_raw: false`, expectation *"DIFFERENT on ≥ 1 salt"* | an EXACT relation failed | **PASS → STRUCTURAL** if read as a row. v1.7 declares it and it enters no antecedent |
| `preconditions.P3_roll` note: *"TA-X-25(c) is the behavioural check"* | P-3 is backed by behaviour | v1.6 § F.2f says the behavioural check is gone. The note overstates P-3 |
| `prereg_version: "v1.4"` in 26 files | wrong instrument | any C1-style consumer that checks the version rejects the file |

The harness computes no verdict (header, `:16`). **These are read-hazards, not grading paths.** The safe state is that none of these fields exists in the attempt-2 emission.

### E. The rulings (item 4)
- **(i) PCL, death order, the six emission gaps, P-4/P-5 and the labels are port defects. I agree.** Port ≠ oracle is T-A's subject, and each is derived from oracle code.
- **For `TA-X-25(c)`, I object: see B.** The repair cannot be built as ruled.
- **(ii) No v1.8 for the holes. I agree.** Minting rows after a result is the WARN-16 hazard. Verifying the holes at the repair Gate-2 is honest **on one condition: the criteria are fixed before any repair result exists.** This finding fixes them (§ Action, R-1…R-12), and it is committed before attempt 2.
- **The JOIN-1 carry is a regression lock, not a verification.** The golden-master note (§ 3, `:205`) compares POST against a **pinned PRE**. A hole present when PRE is emitted becomes the master. The carry means something only if PRE is emitted from the runtime that passed this Gate-2.
- **The (ii) claim that v1.8 "is not needed" does not hold for `TA-X-25(c)`, and it may not hold for `TA-X-07` either.** § F.2d(c) makes the row UNGRADEABLE above 4,500 accumulated terms. `offered` is about 1e8 over about 3,900 ticks, and the repair adds PCL terms. **If the realised depth exceeds the budget, v1.7 cannot reach PASS for any port.** That should be known before the last attempt is spent, not after.
- **(iii) Pack change → HALT. I agree, and it has already fired for (c)** (see B.2).
- **(iv) Tell Matt and re-confirm. I agree, with a correction.** The message to Matt must drop the NO-DATA-as-ease claim (see B.1). Matt's T-C yes is a seal condition, so it must be bound to the **graded runtime digest**. The KP-110 yes is bound to `c9c973fa…` and cannot be carried over.

### F. The six UNGRADEABLE rows (item 2)
**All six are correctly classed as emission gaps.** Each fails for lack of a named emitted quantity, not because an observed value disagrees:
- `07(c)` · `26(b,c,d,e)` · `27(a,d)` · `28` both counters · `29(e)` · `30(b)`.

INFO: `26(e)` is a mean over a **set expression** of pack rowsets. The port can emit it without arming anything. The grade § 6 line *"(e) also depends on the TA-X-25 repair"* holds only if the port computes it over its own armed set, which the row does not ask for.

---

## Rationale

- **BLOCK-1**, on rulings (i) and (ii) as applied to `TA-X-25(c)`. The conductor ruled this a port-only repair needing no Matt ruling. Pack inspection refutes that premise (Discipline #11): only 4 of 342 have fight-grain magnitudes, and the oracle arms 128 of 466. Every repair path either greens the row hollowly (#80), fabricates magnitudes (Law 3), or changes the pack or the prereg after a graded result (ruling iii / WARN-16 → HALT). Under ADR-002, a conflict with a locked instrument goes to Matt. The survival-gap claim was relayed to Matt without derivation. That is the KP-111 lesson, *"derive, don't relay applies to diagnoses given to Matt too"*, and it has recurred. **Path forward:** see Action. The PCL, death-order, emission and label repairs are **not** blocked and proceed now.
- **Grade PASS.** The verdict is conforming, correct under § G, and every pin reproduces. B and C change the grounds, not the verdict.

## Action

- [ ] **gamora:** add a dated addendum to the grade note. It changes no verdict. It must:
  - (1) state `TA-X-25(b)` RED on its presence clause (C);
  - (2) correct § 4 "Direction" forward: the NO-DATA population is shared with the oracle (B);
  - (3) record that 17 intake families is the **union** (13–17 per cell) (INFO).
- [ ] **gandalf (conductor):** add a corrigendum row to the charter that:
  - withdraws the NO-DATA-as-ease claim from KP-113 and from the Matt re-confirm message;
  - routes a **Q-row to Matt before attempt 2** on `TA-X-25(c)`, with three options:
    - (a) a v1.8 re-grounding `(c)` at the fight grain, or declaring its F.1a expiry, committed ALONE;
    - (b) a magnitude lift, which means a pack change plus a re-sealed oracle arm (F2);
    - (c) accept that v1.7 cannot PASS, so the run HALTs at attempt 2;
  - folds the `TA-X-07` depth question into the same Q-row if R-11 measures above 4,500.
- [ ] **drax (repair):** do everything in KP-113 (i) **except** re-classifying the 338. Arm the 4 `w44` records from their `v21` rows (rebase G-6). Emit `n_measured_offense_spawn`. **Do not re-label the 338 while the Q-row is open.**
- [ ] **Matt:** the Q-row above.

**What my repair Gate-2 will require (fixed here, before any repair result exists):**
- **R-1.** Probe expected values are derived from **oracle code** by gamora, who owns the oracle. drax builds the harness only.
- **R-2. Negative control.** Every probe, run on the attempt-1 runtime `c9c973fa…`, must **fail**. A probe that passes there is void.
- **R-3. PCL probe.** PCL reaches health with the oracle's composition:
  - `om` = 1.0;
  - multiplied by `intake.pcl_fraction` (the 26 % defensivePCL, applied multiplicatively);
  - once per volley;
  - unmitigated by resist or armour;
  - subject to the R-PM2-5 can't-kill-alone floor.

  It must agree at declared precision with the oracle function's output on the same fixture.
- **R-4. Class counter.** The unlisted-type branch (`not player_resist.has(dtype)` and not declared-absent) emits a **per-dtype counter**. The counter is 0 on every repaired cell, or each non-zero dtype mirrors the oracle. The oracle **raises** on an unmapped family (GL-12, `threat.py:290`). Named candidates are `ManaBurnDrain` ×2 and `Disruption` ×2 on `nemesis_chthonianvoidborn_01`, which is a POOL-466 member.
- **R-5. Death-order probe.** A lethal hit and a same-tick heal larger than the overkill must produce `death` at that tick. Test the headless loop and `play_step`, plus DoT-lethal and aura-lethal variants matching the oracle's break sites.
- **R-6. Invariants in the attempt-2 emission.** Printed on the report face, never in an antecedent:
  - cells with `killer_id` set and `terminal_reason == cleared` = 0;
  - intra-tick resurrections = 0;
  - `PercentCurrentLife` intake > 0 wherever a PCL row fired.
- **R-7. Digest binding.** My PASS names one runtime digest. Attempt 2 must run on that digest. Any later change means a fresh Gate-2.
- **R-8.** Probe outputs and the T-0, purity, rules and loader outputs are pinned **inside** the attempt-2 MANIFEST, not supplied beside it.
- **R-9. Quoting rule.** An attempt-2 PASS is quotable only together with the Gate-2 finding that closes both holes at that digest. My attempt-2 grade Gate-2 **BLOCKs the seal** if any R-6 invariant is non-zero. It does not block the verdict.
- **R-10. Harness clean-up.** Every field in D and the three gamora named are either removed or restated to v1.7. `prereg_version` and `substrate_epoch` are emitted correctly.
- **R-11. `TA-X-07` depth.** `n_terms_accumulated` is measured on an **ungraded single-cell smoke** before attempt 2 fires. This is not a graded run. Above 4,500 → Matt.
- **R-12. `TA-X-25(c)`.** The Gate-2 does not PASS a change to `n_nodata_spawn_inert` unless Matt has ruled on the Q-row. Any body the port classifies `MEASURED-OFFENSE` must carry at least one damage row from the pack.

## References
- `/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/gamora/notes/2026-09-29-kc2-play-ta-grade-v1p7-attempt1.md`
- `/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/gamora/notes/2026-09-29-kc2-play-ta-verdict-v1p7-attempt1.json`
- `/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/gandalf/notes/2026-09-20-kc2-play-ta-prereg-v1.7.md` (§ A.3, F.1a, F.2d, F.2f, G, G.1)
- `/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/gandalf/notes/2026-09-20-kc2-play-run-charter.md` (§ 4, KP-111, KP-113)
- `/Users/admin/Games/reincarnated-godot/evidence/kc2-play/2026-09-29-ta-run2-v1.7-cells/` (MANIFEST, ta_manifest.json, */*/cell.json)
- `/Users/admin/Games/reincarnated-godot/kc2_runtime/sim/kc2rt_fight.gd` (:886, :973, :1135–1138, :1741–1791); `…/tests/kc2rt_ta.gd` (:16, :76, :640–700)
- `/Users/admin/Games/reincarnated-engine/src/reincarnated/output/kc2-model-pack-v3-E-s09-cp150-mech-v3p4p2-20260929_063506/model/{waves,monster_offense,monsters,player_kit}.json`
- `/Users/admin/Games/reincarnated-engine/src/reincarnated/simulation/math/kc2-play-v3p4-roster-basis-rebase-2026-09-21.md` (§ 6, § 7.1)
- `/Users/admin/Games/reincarnated-engine/src/reincarnated/simulation/output/kc2-lifted-rows-KC2PLAY-v3p4-roster-basis-rebase-20260922_000610.json` (`W48-COV-0`)
- `/Users/admin/Games/reincarnated-engine/src/reincarnated/simulation/kc2/threat.py` (:245–290, :1793, :1848–1880); `…/run.py` (:1754, :3464, :3506, :3786)
- `/Users/admin/Games/reincarnated-engine/src/reincarnated/simulation/math/kc2-join1-golden-master-instrument-2026-09-29.md` (§ 3, :205)
