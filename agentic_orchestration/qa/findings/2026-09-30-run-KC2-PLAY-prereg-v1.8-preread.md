# Finding — 2026-09-30 — Run KC2-PLAY · T-A prereg v1.8 pre-read (DESIGN-MODE, before any graded result) + the pre-registered REPAIR Gate-2 requirement set

**Reviewer:** jack-ryan
**Severity:** **WARN** — 3 WARN, 5 INFO, 0 BLOCK. **The prereg may stand as committed. It needs no new version.** Every gap found here is closed by a repair Gate-2 criterion fixed below. None is closed by a prereg edit.
**Target:** prereg v1.8 `agentic_orchestration/gandalf/notes/2026-09-20-kc2-play-ta-prereg-v1.8.md`, collab `948bb8082`. **FILE sha256 `69e1de1890a24fb9d9a4dc37cda6edfc39e6c34e45b877a2999b565b4710c49c`.** I derived this hash before reading the file, and it matches the brief. Oracle at engine HEAD `96b4529a`. Pack v3.6 (model `4fd35330…`, reference `4e23ffc6…`).
**Developer:** gamora (author) · drax (port) · gandalf (conductor)
**Principles applied:** REVIEW_PROCESS #1 (math before code) · #4 (the committed record is the truth) · #5 (severity matters). Disciplines #11 · #1.2 (implementation claims cite line references) · #19.1 (the cheapest refuting test) · #75 cl. 1(a) · #80 (a green is not evidence until the gate has gone red) · #85 (cross-implementation invariance) · #87 (name the rival behaviour). ADR-002. Charter WARN-16.
**Read-before-result attestation:** I have read **no v3.6 repair result**: no godot commit after KP-130, no side-by-side output and no R-11 re-measure. Every criterion below is fixed before those results exist.

---

## What I found

### A. Verified, each re-derived rather than read (Discipline #11)

| claim | how I checked it | result |
|---|---|---|
| The file is the one named | `shasum -a 256` before reading; `git log` | `69e1de18…`, collab `948bb8082` ✓ |
| **POOL-466 / SWING-456 / NONSWING-10** set digests | I ran the oracle at HEAD with **P-5's loader call verbatim** (`load_profiles(dot_corrections=True, pet_special_gates=None, winner_surface=from_x8(P-n.2), pool_lift=pool_lift.load(), c11a=C11aLoader(CLASS))`). I built POOL-466 from v3.6 `waves.json` (109 pools, waves 151–160) and applied the § PINS law | **`33c886a1…` · `706a61d5…` · `00b4cb0e…` all reproduce.** NO-DATA = 0. The ten NONSWING members equal § A.3's table ✓ |
| The terminal reference **`[156, 152, 155, 152, 152]`** is derived from the substrate | P-n.3 FILE sha `b6c9e795…` ✓. Key `v1p8_seat_cell_pool_lift_winner_surface.arms.PW-FOLDED.leg_a_terminal_waves` = `[156,152,155,152,152]`, config `retaliation_gate: true`, `aura_scope: CLASS`. `PW-BASE` = `[156,152,151,151,156]` (= the sealed `[M-POL2]`). `git diff 28735961 96b4529a -- src/reincarnated/simulation/` is **empty**, and 28735961 is an ancestor of HEAD, so the cell ran on HEAD's oracle code | ✓. **Note:** the same file's `main_salts_0_19.arms.FOLDED` (without the pool lift) reads `[156,152,155,**154**,152]` on salts 0–4. v1.8 took the correct key. A relay that took the other key would carry 154 on salt 3 |
| The EXACT set is unmoved | v1.7 (`552d9fae…` ✓) § F.2 rows against v1.8 § F.2 | Same **28** ids. `TA-X-23` is still struck. No row added, none removed ✓ |
| The declared set is closed at exactly `["TA-X-06"]` | § F.2e, § G, § G.3 (`declared_ungradeable`, "EXACTLY this one"), and T-B cap C1 | Stated in words, and any other id is C1 ✓ (v1.7 pre-read WARN-1 is discharged) |
| The attempt counter reads 0 of 2 under v1.8 | § G.1 against charter KP-115 (Matt verbatim: *"Reset to 2"*) | ✓. v1.7 attempt 1 stays on the record as spent. The naming rule gives *"v1.8 attempt 1 (overall attempt 2)"* |
| § G.2 makes a PASS unquotable without the hole-closure finding | § G.2 R-9 cl. 1–3 · § F.5 cl. 11 · the § G.3 `hole_closure` field | ✓ |
| The oracle does not arm `w44` | `threat.py:600-604` (`can_swing` requires `slots != ()`) · `:1828` (`weapon_rows` ride only inside `is_weapon_swing`) | ✓. See INFO-4 |

**Row diff, re-derivation versus goalpost movement.** Each move is justified:
- **`TA-X-25(c)`** was re-grounded to a fight-grain partition. This is **option (a)** of the Q-row my attempt-1 Gate-2 routed, and Matt ruled Q91 before this file sealed. It is authorized re-grounding.
- **`TA-X-29(e)`**, `3.406 → 3.207764`, corrects a real error. v1.7 walked config A while its own P-5 said the winner surface was ARMED. The new target is **neither** drax's 3.42341 **nor** v1.7's value. It is derived from P-5 config E, so it moved toward the oracle's derivation and not toward the port's figure.
- **P-5** grew from 4 settings to 11. This is the oracle's own configuration, now written down, and it tightens the instrument.

**Not goalpost movement.** The one scope change that § 0 does not label is INFO-1.

### B. The author's four asks

**1 · Hole 7 and the C-11a grant law** have no criteria in the file (§ G.2 defers both to me). They are assigned below as **R-17** and **R-18**.

**2 · OQ-10 is adequate for the label split, but it is NOT closed as claimed → WARN-1.** The author's claim is: *"a port that labels an oracle-swinging record inert reds (c)(2), so the label freedom does not reach the swing decision."* That holds for the `nodata`/`measured_inert` split, and I ratify (d). **But (c) grades the port's self-reported class against the oracle's swing set. It does not grade swinging.** Rival behaviours under #87, both of which green (c)(2)/(3):
- (i) a SWING-456 record labelled `measured_offense` whose body never resolves a swing (empty reachable rows, a speed of 0.0 (*"a statue"*, KP-126), a slot the gate never opens);
- (ii) a NONSWING-10 record labelled inert whose body swings through a path that does not consult the label, for example natural-weapon rows armed on a slotless `w44` profile.

§ F.2f's *"PROVES: it arms exactly the records the oracle can swing"* holds **only if the label and the fight loop's gate are one predicate.** The row does not test that. It is closed pre-fire by **R-19**.

**3 · `C-k` → WARN-2. The exposure sits exactly where the fight is.** `TA-X-29(e)` grades w159/w160. Those waves hold **0** of the 264, and **no oracle salt reaches them** (terminals 152–156). The walk's own identity-path counts are **8 · 94 · 73 · 4 · 53 · 5 · 69 · 95 · 0 · 0**. So the 264 are concentrated in waves 152, 153, 155, 157 and 158, where the player actually dies. Under #87, the rival *"a port that invents supply for them"* produces the same `TA-X-29(e)` number. The prereg names this itself (§ E.2 `C-k`), and I agree with OQ-11 that widening `(d)` belongs to a version that exists for that purpose. The ten-wave walk is already emitted, so the cheapest refuting test costs nothing. It becomes a **pre-fire** Gate-2 criterion (**R-20**). It still gates nothing in the verdict.

**4 · H-6 / R-11.** This re-measure is required. Its specification is under R-11 below. I add no headroom rule: § F.2d's own three cases already cover every outcome, and adding headroom would be a goalpost.

### C. The side-by-side → WARN-3: the on-record divergence has an underived attribution

KP-130 records the v3.5.2 port on the ORACLE-config M-POL-2 arm, salt 0, **dying at w151, tick 95**. The attribution given is *"C-11's composition surplus, which v3.6 corrects."* **That does not survive the oracle's own sibling.** `PW-BASE` runs the **same unfolded model**: the pool lift armed, the winner surface armed, no C-11a, and aura pulses firing as damage. It dies on salt 0 at **156 @ 5.959 s**, not 151. A composition surplus that both sides share cannot explain a five-wave gap between them. **The divergence is live evidence of a port≠oracle item that is not among the seven holes, until it is localized.** Its direction is lethal, the same direction as hole 7 and the missing grant phase.

Caveat, stated so it is not over-read: I have not established that KP-130's port cell and `PW-BASE` share one configuration. `PW-BASE` does reproduce the sealed `[M-POL2]` terminals exactly. The side-by-side must establish the configuration identity (R-22 S-1). This is the same failure class as KP-111 and KP-114: a relayed diagnosis treated as derived.

### D. INFO

- **INFO-1. `TA-X-29(e)` gained per-record assertions** (*"each priced record's ratio matches the table below"*, ± 5e-4). v1.7 asserted only the two wave ratios. § 0 labels (e) "CORRECTED and RE-DERIVED" and does not mention the added scope, and § A.4 calls the table a localization aid (*"so the port can localise a miss"*). **My reading, recorded before any result: § F.2h's row text is normative, so the per-record clause IS graded.** It tightens the row, it predates any result, and it points at oracle-derived values, so no new version is needed. The grader applies it as written.
- **INFO-2.** § B.6 says "ELEVEN" settings, but its table carries ten rows, with setting 10 in a blockquote. KP-130's runtime verified "all **six** fold settings". R-21 requires all eleven.
- **INFO-3.** § J cites *"Law 3 / `#79` (no fitted constants)"*. #79 is *Citation provenance*. The no-fitted-constant rule is Law 3 (and R-PM4-29). This has no effect on any row.
- **INFO-4. SELF-CORRECTION.** My attempt-1 Gate-2 Action told drax to *"Arm the 4 `w44` records from their `v21` rows (rebase G-6)."* **That was wrong at the fight grain.** The oracle cannot swing a slotless profile (`threat.py:600-604`, `:1828`). **I withdraw it.** v1.8 § A.3 is right, and the conductor's "do not arm / revert" ruling stands.
- **INFO-5.** § G.1 L2 names "R-1…R-16". I read that as **"R-1…R-16 plus the criteria § G.2 defers to this pre-read."** § G.2 defers hole 7 and the grant law to me in terms. They are fixed here before any repair result, so this reading moves no goalpost.

---

## Rationale

- **No BLOCK on the prereg.** The pins, set digests, terminal reference, EXACT set, declared closure and counter all reproduce (A). Each weakness in (B) and (C) sits at the hole-closure layer, which the prereg explicitly gives to this Gate (§ G.2, L2). Closing them there keeps the instrument unedited, so WARN-16 is untouched and no version churns.
- **WARN-1:** #87. A label graded against a set is evidence about the label, and evidence about behaviour only if the label is the gate.
- **WARN-2:** #87 and #80. A row whose waves the fight never reaches cannot catch a defect that lives in the waves it does reach.
- **WARN-3:** #11, #85, #19.1. The cheapest refuting test for *"v3.6 corrects it"* is the unfolded oracle's own salt 0, and it refutes the claim.

---

## Action

- [ ] **drax:** build to R-17…R-22. Run the side-by-side per R-22 **on the digest you submit to the Gate** (R-7). Take R-11's depth from those same cells.
- [ ] **gamora (R-1):** supply the oracle-side expected values that R-17(b), R-18(f), R-19(b) and R-20(b) need, derived from oracle code at `96b4529a`: the per-record composed speeds; the fixed-fixture C2 counters; the 466 per-record profiles; and the 264-record identity-path list with its set digest (law as § PINS).
- [ ] **gandalf:** amend KP-130's side-by-side attribution forward (WARN-3). Record that attempt-1 Gate-2's `w44` action is withdrawn (INFO-4).
- [ ] **Matt:** nothing now. The side-by-side's case (ii) under R-22 S-3 can route to you.

---

## THE PRE-REGISTERED REPAIR GATE-2 (applies before v1.8 attempt 1 = overall attempt 2 may fire)

**The two phases, so that "hole-closure GREEN" has one meaning.**
- **Phase 1:** the repair Gate-2 PASSes digest **D** on R-1…R-22 below. Only then may the attempt fire, **on D**.
- **Phase 2:** the attempt-grade Gate-2 verifies that the graded run used D (R-7), that the probes are inside the MANIFEST (R-8), and that the R-6 values are all zero.
- **The hole-closure finding is GREEN only when both phases pass.** Neither phase ever enters a verdict antecedent.

### Carried
- **R-1.** Expected values come from **oracle code** (gamora). drax builds the harness only.
- **R-2 (restated at v1.8).** Every probe must FAIL on a runtime that lacks the mechanism. **The failure must come from the mechanism, not from loading** (#80). A v3.6 probe that "fails" on `c9c973fa…` only because that binary cannot load v3.6 is **not** a control. Acceptable controls are:
  - `c9c973fa…` when the probe runs on pack-independent fixture data; or
  - the repaired runtime rebuilt at the commit **immediately before** the mechanism's commit.
- **R-3** PCL composition. **R-4** per-dtype counter. **R-5** death order (headless loop + `play_step`, DoT-lethal and aura-lethal). ⚑ At v3.6 the "aura-lethal" variant covers **granted-row** kills.
- **R-6** the three invariants, printed on the report face.
- **R-7** one runtime digest. ⚑ The side-by-side, R-11 and every probe run on it, and any later commit means a fresh Gate-2 **and** a re-run side-by-side.
- **R-8** probes inside the MANIFEST.
- **R-9** the quoting rule (§ G.2).
- **R-10** stale harness fields restated to **v1.8 / v3.6**, verified **on the emission** (H-4).
- **R-11 (H-6).** `n_terms_accumulated` is read from **all five side-by-side M-POL-2 cells** through the graded emitter's own path (`kc2rt_ta_emit.collect`), on D, on v3.6, with P-5 complete.
  - **max ≤ 4,500:** attempt 1 may fire.
  - **max > 4,500:** it does not fire, and the question goes to Matt (§ F.2d case 2). No headroom is added.
- **R-12 (restated).** The Matt clause is **discharged** (Q91 ruled). Carried: no body is labelled `measured_offense` without a pack damage row, and **the four `w44` records and the three HONEST-FAILs are NOT armed.**
- **R-13…R-16** (holes 3–6) are carried and **re-run on D against v3.6 profiles**. ⚑ R-13's *"705/705 row sequences match `load_profiles()`"* was measured at v3.5. At v3.6 it must match `load_profiles(…, c11a=C11aLoader(CLASS))`, which removes the aura-buff rows.

### NEW
- **R-17 · HOLE 7, the march base.**
  - (a) The monster and monster-pet speed base is read from `monster_kinematics.json :: ⚑ v3p5p2_rows :: k4_march_base_law` (K4-0) and equals `patrol.MARCH_BASE_M_PER_S[PxArm.LO]` = 3.209466 **bitwise** (`patrol.py:99-100`). Loading fails closed if the row is absent or MID is requested. A source scan finds no literal `3.209466` and no `v_ref` on the monster-speed path.
  - (b) For **every POOL-466 record and every monster pet**, port speed equals the oracle's `multiplier × march_base_m_per_s(v_ref)`, bitwise or ≤ 1e-12 relative. The partition reads 128 / 180 / 158 = 466/466, and FALLBACK-158 hashes `e8114efa…`.
  - (c) The **player's** speed is byte-identical to the pre-hole-7 runtime (`patrol.py:214-224`).
  - (d) Kinematic fixture: a body at multiplier 1.000 advances `min(3.209466·dt, max(0, dist − 2.4))` per tick, agreeing with the oracle mover. `TA-X-30`'s halt is unchanged.
  - (e) (a), (b) and (d) FAIL on `c9c973fa…` (4.0).
  - (f) The verdict face prints `P5_folds.monster_march_base.port_m_per_s = 3.209466`, read by running the binary.
- **R-18 · THE C-11a GRANT LAW, and fold conformance.**
  - (a) **Slot removal.** Per-record slots and rows over POOL-466 ∪ monster pets equal the oracle's under the C-11a loader: **131 slots emptied / 157 rows claimed**. The `can_swing` flips are exactly `[pet chthonianminion_b01_summon]`, and SWING-456 is unchanged.
  - (b) **Coverage (D-C11a-1).** The carriers are the **alive, on-board** (`spawn_t_s ≤ t`) monsters plus the alive monster pets, snapshotted at the oracle's phase (`run.py:1711-1722`). A body is covered iff `hypot ≤ radius_m`: inclusive, centre-to-centre, with the carrier covering itself (`c11a_corrections.py:357-372`).
    - Fixture probes: bodies at r−ε, r and r+ε, and a carrier that dies at tick k.
  - (c) **Stacking (D-C11a-2).** One instance per buff record. A rank conflict goes to the **higher rank** and is counted. Different buffs **add**: rows concatenate in sorted buff order, `om_add` values sum, and resistances sum per stream (`:374-397`).
    - Fixtures: same buff ×2; same buff at different ranks; two buffs.
  - (d) **The rider.** Granted rows (`APPLIED-FLAT/DOT/PCL/LEECH-G3`) ride the covered body's weapon swing, and `om_add` joins `om`. Each granted row's chance is drawn **at the oracle's site and in its order**. G-3, re-run against the oracle's sites, stays green **with grants live**.
  - (e) **Resistance grants** (`defensivePhysical/Lightning/Bleeding`) apply to player hits, pet hits and secondary-stream hits on covered bodies, including the ≥ 100 % zeroing case (`run.py:2863-2944`, `:3098-3101`).
  - (f) **Counter mirror.** The port emits the oracle's C2 counters by name (`n_cover_queries · n_covered · n_multi_cover_same_buff · n_multi_cover_rank_conflict · n_grant_rows_applied · n_om_grant_rows · n_player_hits_res_bonus · n_player_hits_zeroed_by_grant · covered_by_buff`). The C1/C4 counters read **0**. On one fixed fixture wave, **port counters == oracle counters exactly.**
  - (g) The grant table sha `749d58f4…` is verified at load, and a mismatch RAISES. The port adds no DoT attribute scaling (R4) and no C3.
  - (h) Negative control under R-2: (b)–(f) FAIL on the pre-grant-phase build.
- **R-19 · OQ-10: the label is the gate.**
  - (a) `spawn_by_record.class` is computed by the **same function** the fight loop consults to skip a body, equal to `swing_period ≠ null ∧ slots ≠ ()`. Line references are cited (#1.2).
  - (b) The port's own loader dump over all 466 reproduces the **three set digests**, and each SWING record carries ≥ 1 choosable slot with ≥ 1 reachable row and a speed > 0.
  - (c) On the side-by-side cells, NONSWING-10 bodies make **0** weapon-swing resolutions. `aetherialimp_a01`'s dying fire is counted separately (hole 5).
- **R-20 · `C-k`.**
  - (a) The port's ten-wave walk (config E) reproduces gamora's ten values to within |Δ| ≤ 5e-4 per wave, and reproduces the identity-path counts `8·94·73·4·53·5·69·95·0·0` **exactly**.
  - (b) Each of the 264 resolves to attr 1.0, type 1.0 and own 0.0. None is estimated from a sibling, donor or median.
  - (c) The walk calls the port's **fight** resolver, not a re-implementation (#75 cl. 1(a)).
  - The walk still gates nothing in the verdict.
- **R-21 · P-4/P-5, checked before firing.**
  - The header `pack_digest` reads `4fd35330…` and the reference reads `4e23ffc6…`, both **read by running the binary**.
  - **All eleven** P-5 settings are verified, and the runtime refuses to boot on any unset one.
- **R-22 · THE SIDE-BY-SIDE. My position: a divergence MUST be localized and dispositioned before the attempt fires. It need NOT be closed to equality.**
  - **S-1 (same epoch, same config).** The side-by-side uses digest D, v3.6, P-5 complete, salts 0–4, in the configuration of P-n.3 `PW-FOLDED`. That configuration identity is **shown**, not assumed. It prints the terminal wave, the death second, the killer, and landed damage per wave on both sides. Cross-epoch comparisons are void (§ C.7), and that includes KP-130's v3.5.2 cell.
  - **S-2.** If all five terminal waves are equal, record them. No action follows.
  - **S-3 (any divergence, e.g. port w151 against oracle w156 on salt 0).** Before Phase 1 can PASS, a **first-divergence localization** is filed. Both sides run that salt, traced per tick at the J-S8 grains (G1 hit, G2 applied damage per packet, draw counts per site). The **first** differing tick and quantity is named, with its mechanism derived from oracle code. The divergence then takes exactly one disposition:
    - (i) **port defect:** repaired in its own commit with a fail-first probe, which produces a new D, a fresh Gate-2 and a re-run side-by-side;
    - (ii) **oracle-side:** routed to gamora and the conductor, and to Matt if it touches the reference. The attempt does not fire until it is dispositioned;
    - (iii) **a derived non-comparability** (#85: enumerate what the two may differ on): accepted only with the derivation that the first divergence *is* that mechanism.
  - *"Unexplained"* and *"explained by assertion"* do not pass. If the two sides are shown not to be draw-comparable at tick 0, the localization moves to a fixed-script fixture at the G2 grain.
  - **S-4.** A residual terminal difference that is attributed to an accepted mechanism does not block. **`TA-B-01` stays DIAGNOSTIC. No constant is tuned toward an oracle terminal** (KP-44; Law 3).
  - **S-5.** The side-by-side is print-only, and it must be incapable of emitting a graded artifact (KP-44). **No port change may be justified by an EXACT-row value observed on it**, only by a localized mechanism.

**Deferred with their gates:** `C-h`/OQ-9 and `C-k`'s widening of `(d)`/OQ-11 wait for a version that exists for them. `C-m′`/OQ-12 waits for C-11 and Matt. C-11b A+B and C-11c go to REFERENT-v2 (KP-132).

## References
- `/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/gandalf/notes/2026-09-20-kc2-play-ta-prereg-v1.8.md` (§ 0, A.3–A.5, B.6, E.1–E.2, F.2d, F.2f, F.2h, G.1–G.3, H, I)
- `/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/gandalf/notes/2026-09-20-kc2-play-ta-prereg-v1.7.md` (§ F.2)
- `/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/qa/findings/2026-09-29-run-KC2-PLAY-ta-grade-v1p7-attempt1-gate2.md` (R-1…R-12)
- `/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/gandalf/notes/2026-09-20-kc2-play-run-charter.md` (KP-44, KP-113…KP-132)
- `/Users/admin/Games/reincarnated-engine/src/reincarnated/simulation/output/kc2-play-c11a-fold-pricing-NOT-A-GRADED-RUN-20260930_043045-SUMMARY.json` (P-n.3)
- `/Users/admin/Games/reincarnated-engine/src/reincarnated/simulation/kc2/threat.py` (:600-604, :829-834, :1828) · `…/run.py` (:1700-1735, :2863-2944, :3098-3101) · `…/c11a_corrections.py` (:155-218, :295-397) · `…/patrol.py` (:99-100, :214-224)
- `/Users/admin/Games/reincarnated-engine/src/reincarnated/output/kc2-model-pack-v3-E-s09-cp150-mech-v3p6-20260930_045353/model/{waves,monster_kinematics}.json`
