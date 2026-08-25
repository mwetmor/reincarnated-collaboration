# Finding — 2026-08-24 — gamora KC2-MC **B-4 SPECIALS** (facet (c) SIM) — Gate 2

**Reviewer:** jack-ryan (DEV-MODE, BLOCK authority)
**Severity:** **BLOCK — LIFTED 2026-08-24** (see § LIFT VERDICT at the foot of this file) — 1 BLOCK / 5 WARN / 7 INFO
**Target:** engine `5bb2ea4f`; checkpoint `08255194273becf948b43864c12516ecba5cb8bb38b5129b605885351333a0dd`
**Developer:** gamora (simulation seam)
**Conductor:** gandalf (`RUN-CONDUCTOR`) — ledger `L-55`, ruling `R-L55-1`
**Principles applied:** 1 (math-before-code), 2 (smoke-gate), 3 (cross-seam impact), 5 (severity/escalation)
**Disciplines cited:** #1, #2, #6, #10, #11, #12

---

## 0 · Verdict

**BLOCK.** The build's measurements are, so far as I can re-derive them, correct — I reproduced every
headline count from my own code at HEAD and every one matched. The BLOCK is not about a number. It is
about **the durability of the artifact the run is about to seal on**: B-4's driver deletes its own
checkpoint of record on any re-execution, the checkpoint is untracked in git, and it is not
regenerable. I destroyed the sha of record by doing the one thing a Gate-2 reviewer is required to do,
and restored it only because I had taken a backup first.

The discharge is cheap and **within-seam** (ADR-002): a driver change, no consumer-visible API move.
It does not need Matt unless gamora disputes it.

⚑ **Operational warning to the conductor, ahead of anything else in this document:** `R-L55-1` seated
the gate pair in parallel. **gandalf's DRIFT-CRITIC must not execute
`gamora_kc2_mc_b4_specials_2026_08_24.py` until BLOCK-1 is discharged.** One reproduction run destroys
`08255194…` permanently.

---

## 1 · What I found

### BLOCK-1 — the artifact of record is destroyed by its own driver, is untracked in git, and cannot be regenerated

Three facts, each measured:

1. **The deletion sweep is unconditional.** `gamora_kc2_mc_b4_specials_2026_08_24.py:1137` globs
   `kc2-checkpoint-E-s09-cp150-b4-*.json` with no exclusion for the sha of record, and `:1359`
   unlinks every match. I ran the driver (exit 0, 25/25 hold, wall 22.4 s). It deleted
   `08255194…` and enumerated it in the successor artifact's own `⚑ deletions` block as debris.
2. **git records nothing for it.** `git log --all -- '*b4-*.json'` → 0 commits, for every b4 file.
3. **It is not reproducible.** My re-run diffs against the record in exactly four leaves — two
   volatile (`started_utc`, `wall_s`) and two self-referential (the deletion row). Because the two
   volatile leaves are inside the hashed payload, the re-run emits a *different* sha
   (`246d4b4d28c2a04a82e513b73e5c27950df312b6a911e646b8fa6462a5e078f9`). The bytes of
   `08255194…` cannot be recreated.

Composed: the run's nine-byte-guard architecture means B-5 and B-3app will guard `08255194…` as a
predecessor. Losing it is a **permanent, unrecoverable HALT** of every successor's `B4-P0`-equivalent.

Two aggravating clauses, both on the emitted surface (`⚑ deletions`):

- `⚑ condition_3_nothing_cites_them` is a **hard-coded string**, not a derivation. On any re-run it
  asserts *"no artifact, ledger row, finding … references either sha"* about a sha that ledger `L-55`
  and this finding both cite. ADD 6 § 2 correctly converted the deletion *population* from a declared
  constant to a derivation; the three *conditions* were left asserted. That is the half of the repair
  that was not done, and it is the half W3 was about.
- `⚑ condition_2_mechanism` also carries the WARN-1 falsehood below.

**Discharge path** (any one of the first two suffices; all three preferred):
- (a) exclude the artifact of record from the sweep, or gate the sweep behind an explicit opt-in flag;
- (b) **commit the b4 checkpoint** — note that b1 (`0bdd7704`), b1r ×2 (`7e8b02ad`, `ec843589`) and b2
  (`1888b218`) checkpoints of *this same run* were committed, so the precedent exists and the
  remedy is already in the run's own practice;
- (c) derive `condition_3` (scan the repo + ledger for the sha) rather than assert it.

### WARN-1 — W3's mechanism clause carries a false universal, and the deletion record is split across four surfaces

`⚑ condition_2_mechanism` (and ADD 5 § 2 verbatim) states: *"checkpoints in this run have never been
tracked (B-3's seal commit carries its script and its state file, not its checkpoint)."*

The parenthetical is true of B-3. **The universal is false.** Four checkpoints of this run are in git:
b1 `0bdd7704`, b1r `7e8b02ad`, b1r `ec843589`, b2 `1888b218` (plus `mech` at `a411a35c`).

The *load-bearing* per-file claim — "git records nothing for **these** files" — is TRUE (0 commits
each), and it is what licenses the deletion. So **the deletion is legal in substance.** But the
supporting clause is a false statement of fact on a digested surface, offered as git-checkable, in the
repair for the finding that convicted B-3 for exactly that. It also conceals discharge path (b).

Separately, **no single surface carries the full deletion record**: ADD 5 § 2 names two files
(`230721`, `231201`); ADD 6 § 2 names a third (`231425`); the artifact of record names a **fourth** —
`kc2-checkpoint-E-s09-cp150-b4-20260824_231817.json`, sha `63b0f0f9184ecde…` — that appears in **no
addendum at all**. Four deletions, three surfaces, no union anywhere. (The fourth is genuinely
uncited and untracked — I checked; the three conditions hold for it.)

### WARN-2 — `B4-P14` is a falsifier that cannot fail, its registered form was narrowed without an addendum, and its own scanner convicts the artifact 40 times

Registered (math note § 7): *"every zero and gated count **on the surface** carries the `capability_*`
/ `measurement_*` / `measurement_condition` key split."*

Implemented: `_split_ok(art["⚑ body_rows"])` — the 39 body rows, constructed six lines above at
`:1204-1214` with a hardcoded key set. The emitted key set is exactly
`{record, capability_special_slots, capability_can_swing_with_gates, capability_swing_period_s,
measurement_spawn_count, measurement_condition}`. Every non-string key is already
`capability_*`/`measurement_*`. **`bad_zero_keys` is structurally guaranteed empty.**

I ran the build's own `_split_ok` over the whole artifact — the registered scope — and it returns
**40 hits**, every one a price counter (`c_b4_1_selections_outside_decoded_annulus`,
`c_b4_2_selections_admitted_by_shorter_gate`, `c_b4_3_selections_inside_prior_timeout`) in
`⚑ arms/*/cells/*/prices`, `prices_ensemble`, and `predicates/B4-P15`. Those are "gated counts" in the
registered form's own words. Three of them are the `D2_FIRING_ONLY` zeros — precisely the T-c shape
that earned `C-B4-2` a `measurement_condition`.

This is W2's own lesson — *"A falsifier that cannot fail is not a falsifier"*, written in this build's
§ 6 — reproduced in the **W4 repair predicate**, in the same build, and unlike `B4-P11` it ships **no
mutation proof**. ⚑ **Second consecutive build in which a W-cluster repair predicate is itself a
tautology.** The W4 *claim* is nonetheless true and I verified it independently (below).

### WARN-3 — `B4-P12`'s falsifier and registered-population are stale at 23 against a measured 25

`:1314-1316` emit `⚑ falsifier: "…a population != 23"` and `⚑ registered_population: "TWENTY-THREE
rows — parent § 7 registered TWENTY, ADDENDUM 1 added TWO … ADDENDUM 2 added ONE"`, beside
`⚑ predicates_registered: 25`, with `holds: true`. ADD 3 § 2 raised 23 → 25; ADD 4, 5 and 6 each
restated *"25 — UNCHANGED"*. The strings were never updated. Enforced as written, P12 would fail.

⚑ This is gamora's own harvest candidate #3 — *a hand-typed count standing in for a derivation* —
occurring **inside the predicate whose entire job is to police that**, and it is the one instance of
the six that no instrument caught.

### WARN-4 — ADD 2's "never committed" rename claim is false, and it was explicitly offered as git-checkable

ADD 2 § 2: *"`pet_bodies_woken_by_d2` … **is removed before it is ever committed**; it exists only in
the working tree … the mechanism is 'never committed', and that is **checkable in git** rather than
asserted here."*

I checked it in git, as invited. `git log --all -S "pet_bodies_woken_by_d2"` → **three commits**:
`6ec044ac` (ADD 1, which tabulates `LoadReport.pet_bodies_woken_by_d2` as a measured row), `e9af67ce`
(ADD 2 itself), `5bb2ea4f` (the build). At HEAD it survives in `threat.py:931`, the driver `:992`, and
two addenda.

The *substantive* claim is true — no `LoadReport` field, no digest and no consumer ever carried the
name. The *literal* claim is false. Sharper: `threat.py:931` at HEAD reads

```
#   slot so `pet_bodies_woken_by_d2` is a COUNT OF BODIES WITH NO OTHER ATTACK, not a
```

— the **corrected semantics documented under the retired name**, in shipped code, pointing a reader at
a field that does not exist. Third instance in this build of the same shape as W3: a mechanism claim
asserted as git-checkable that git does not support.

### WARN-5 — W1 is repaired forward, not at the address that failed, and the exemption register is unexercised; neither is disclosed

- `gamora_kc2_mc_b3_summons_2026_08_24.py:176` **still reads `STRUCTURAL_NUMBERS = {0, 1, -1, 2, 3, 4}`.**
  The over-broad set that W1 convicted is unrepaired at its own address.
- B-4 adopts `{0, 1, -1}` in a **new** module. I AST-scanned `pet_specials.py`: its only numeric
  literals are `0` (×24) and `1` (×8). **No literal is exempted by `declared_constants()`, because
  none needs to be.** The math note § 6 states *"the two remaining sites are guarded by named
  module-level constants carried in `declared_constants()`, so they are exempt by REGISTER"* — there
  are no such sites in this module. The register is emitted (8 names) and the mechanism it describes
  is never exercised. `B4-P10` passes at 0 because the module is trivially clean.

B-3 is SEALED, so declining to repair there is defensible — and the build **makes exactly that
argument** for `control_states.py` (`C-B4-6` / `MD-B4-5`, `magnitude_class = bounded`). It does not
make it for W1. No `C-B4-n`, no `magnitude_class`, and § 6 reads as a completed repair.

---

## 2 · Everything that holds — re-derived, not read

I re-derived each of these from my own code against HEAD, or by hashing bytes myself. None is taken
from gamora's predicates.

**Driver reproduces.** Exit 0, 25/25 predicates hold, wall 22.4 s. Four diff leaves vs the record: two
volatile, two the deletion self-reference.

**D4 ordering — strict to the second, each addendum ALONE** (verified by `--stat`, one file per commit):

| | commit | time (EDT) |
|---|---|---|
| math note ALONE, zero code | `9844a550` | 18:50:00 |
| pinned decode surface, data only | `74d38a00` | 18:50:12 |
| ADDENDUM 1 | `6ec044ac` | 18:57:04 |
| ADDENDUM 2 | `e9af67ce` | 18:59:50 |
| ADDENDUM 3 | `d0b4118c` | 19:10:09 |
| ADDENDUM 4 | `6275c336` | 19:13:27 |
| ADDENDUM 5 | `564a2929` | 19:16:29 |
| ADDENDUM 6 | `ba88e957` | 19:19:33 |
| **emission** | — | **19:22:29** |
| **build** | `5bb2ea4f` | **19:23:55** |

Every addendum's cited parent commit is real and precedes it. **D5: exactly one b4 checkpoint on
disk — no sibling ambiguity.** Discipline #1 satisfied without qualification.

**Nine byte-guards — re-hashed by content, not by filename.** I hashed every checkpoint in
`simulation/output/` and matched the claimed digests against the resulting content map: **8/8 sibling
guards found by hash**, PRE == POST **exact** for all eight, including b3 SEALED
`dd13408e108e6f68ccca7fb109e8b04361957f292606389bd4274023c2f78b51`. Parent `verify_frozen()` 20/20.

**The headline defect — real, and every count reproduced.** `threat.py:927` admits on the DAMAGE row
(`_f(rs[0], "skill_cooldown_s")`); `:938` constructs from the META row (`m`), `None` for every pet.
My own derivation at HEAD:

| quantity | mine | claimed |
|---|---|---|
| D-2 rows / distinct bodies | 65 / 39 | 65 / 39 |
| D-2 keys joining a loaded pet profile | 39/39 records, all join | 65/65 |
| D-2 keys colliding with `pm2_tg2_attack_slots` | **0** | 0 |
| pet special slots BUILT, fold off | **14** | 14 |
| …all carrying `cd == delay == chance == eff == 0.0` | **True** | True |
| `LoadReport.pet_special_slots_ungated` | **51** | 51 (the wrong fifty-one) |
| bodies with `slots == ()` | **14** | 14 |
| bodies with `swing_period_s is None` | **3** | 3 |
| bodies with `can_swing == False` | **15** | 15 |
| overlap (both effigies) | **2** | 2 |
| `noswing − empty` | **1** (`gabbalthunn_obsidianshard`) | 1 |
| identity A `14 + 1 == 15` | **True** | True |
| identity B `14 − 2 == 12` woken | **True** | True |
| D-2-body spawns over the ensemble | **152** | 152 |
| spawns of bodies that cannot attack today | **118** | 118 |
| spawns of bodies B-4 wakes | **108** | 108 |
| firing-14 slots on a rolled body | **exactly 1** (`wraith_b01_summon special3`) | 1 |

⚑ And `wraith_b01_summon`'s `special3` is that body's **only** slot — so `choose_slot` has nothing to
offer outside 6.0 m. ADD 6 § 1's "the reach was the binding constraint, not the gate" is structurally
correct, and the § 0.3 frame that predicted it was registered before any of it ran.

**The exposure pairing — TRUE on both sides.** From the artifact's `measurement_digest_by_salt`,
confirmed byte-identical in my own reproduction: `D2_FIRING_ONLY` digests equal `ABSENT` digests on
**5/5 salts**; `D2_ALL` equals `D2_SILENT_ONLY` on 5/5; and `measurement_pet_selections_derived == 0`
on the firing arm (162 selections, all roster). So the source-split defect is **real** and its
record-cell exposure is **nil**, and the artifact carries both. The three-arm design earned this.

**The armed rows — set equality, and the raise is live.** Re-deriving the mechanism myself (no
`RESIST_PCT` entry, no `NON_HEALTH_DAMAGE_TYPES` entry, `kind == 'direct'`) over the loaded profile
set returns **exactly two** rows, both on `nemesis_chthonianvoidborn_01`: `special3 ManaBurnDrain`
(lo 10.0) and `special4 Disruption` (lo 2.0). In-process, not mocked:

```
mitigate(10.0,'ManaBurnDrain') -> KeyError "damage family 'ManaBurnDrain' has no measured resistance…"
mitigate(10.0,'Disruption')    -> KeyError "damage family 'Disruption' has no measured resistance…"
```

`ABSENT_FAMILY_TOKENS` = 5 families; **exactly 2 have callers** (Sleep, Fear); Trap 0 / Immobilize 0 /
**Disruption 2 hits**. All reproduced. ⚑ `ManaBurnDrain` is named by no carry and no ledger row, and it
was found because the carry was briefed as a mechanism. The L-50 discipline candidate paid on its
first outing — that credit is earned and I confirm it.

**W2 — fully repaired, and it is the strongest work in the build.** This was the WARN I most wanted.
`_doc_set_git()` reads `git ls-files -s` and re-hashes the blob **content** so the two instruments are
in the same units; `B4-P11` compares keys **and** hashes. I ran my own three mutations against the
live instruments:

| mutation | result |
|---|---|
| baseline | holds |
| phantom injected on the disk side | **CONVICTS** |
| one doc dropped from the git side | **CONVICTS** |
| content drift on one doc | **CONVICTS** |

Three independent ways to fire, all confirmed. `B4-P11c` is a real mutation proof. **WARN-2 of the
B-3 gate is DISCHARGED.**

**W4 — the split is in the KEYS, and it is right.** I checked the keys, not the prose:
`⚑ body_rows` carries 39 rows; the spawn-count value distribution is `{0: 33 rows}` plus exactly six
non-zero rows whose counts — 61 / 30 / 25 / 22 / 10 / 4 — match `B4-P7` term for term. All 33
never-spawned rows carry populated `capability_*` with `measurement_spawn_count: 0` and a
`measurement_condition` naming the T-c reading. A Godot builder cannot mistake "never rolled" for
"does not exist". **WARN-4 of the B-3 gate is DISCHARGED in substance** (the predicate guarding it is
WARN-2 above).

**F-10 — every refusal numbered, priced and magnitude-classed.** Six refusals, `magnitude_class` on
all six, `B4-P13` correctly reading "unpriced AND unlabelled" so `C-B4-5` passes on its label.
`C-B4-5`'s `unbounded-unmeasured` is **honestly assigned** — it is genuinely unmeasured and refuses a
decorative price. `C-B4-2`'s `0/159` flagged as *a roll not a rule* is the sharpest single line on the
surface. **F-10 is DISCHARGED.**

**F-8 — re-derived on B-4's own basis.** ABSENT 2-in-683; arm of record 1-in-510; reproduced in my
run. `562` appears in the build **only** inside disclaimers that it is not an input — never as a
computed value. Honest.

**Smoke — exact.** `pytest -k kc2` → **512 passed, 1 failed** (55.9 s); `tests/test_kc2_mc_b4_specials.py`
→ **28/28**. Claim reproduced to the test.

**MIGRATION.md rides `S-B4-5`** with a before/after table for `pet_special_slots_ungated` and the new
`pet_special_slots_gated_by_d2`, and an explicit consumer warning. Principle 3 satisfied.

**Self-disclosures D-B4-1 … D-B4-11 — spot-checked, all real** except the two clauses at WARN-1 and
WARN-4. D-B4-1 (11→12), D-B4-2 (118 vs 108), D-B4-3 (unwakeable set is 3, sets overlap), D-B4-7
(`l50_struck_clause_asserted` shipped), D-B4-9 (159 vs 263 both emitted under honest names), D-B4-11
(count derived, `n_deletions == len(deleted)`) — each verified against the artifact or the code.

---

## 3 · INFO

- **INFO-1 — T-c applied to the zero, not to the non-zero prices.** `C-B4-2` (0) carries a
  `measurement_condition`; `C-B4-1` (16) and `C-B4-3` (3) do not. All three are equally
  roll-conditioned — 12 of 65 slots are reachable, 53 sit on never-spawned bodies. The refusal rows
  also carry numerators without the 159 denominator `D-B4-9` had just corrected.
- **INFO-2 — `C-B4-4` promised two rows and ships one.** Math note § 4: *"stated as two rows precisely
  because they are of different magnitude class and must never be summarised as one number."* The
  artifact emits one row, `magnitude_class: "bounded"`, with the unbounded clause in a prose field
  (`⚑ two_rows_not_one`). Prose carrying a distinction the key does not — the W4 shape.
- **INFO-3 — `B4-P16` scans a pre-insertion snapshot.** `art_blob` is taken at `:1273`; P16, P16c, P12,
  `⚑ derived_summary` and `wall_s` are inserted after and escape. ADD 4 § 1 registered the scope as
  *"over the whole artifact including its keys."* Six struck-clause strings do survive on the emitted
  artifact — **all inside P16's own pattern register and its explanatory fields**, so **no laundering
  clause survives and the substantive L-50 claim holds.** The fragility is that the exclusion is by
  *ordering*, not by declaration: anything appended after `:1273` escapes silently.
- **INFO-4 — `B4-P10` and `B4-P16` emit no falsifier field.** Every other predicate carries one, and
  both have registered falsifiers in math note § 7.
- **INFO-5 — the smoke failure is mis-attributed by ten days.** `test_AC_10_10_the_literal_30_0_appears_NOWHERE_in_the_arena_surface`
  fails on `secondary_streams.py:136` (`BLEED_DURATION_MODIFIER_PCT: float = 30.0 + 100.0`). That line
  was introduced by **`583ebdae`, 2026-08-14, "KC2-PM4 I-12 CODE — the SECONDARY-STREAMS FOLD"** — the
  file's *only* commit. It has failed since 2026-08-14. AGENT_STATE's wording (*"the same one B-3
  recorded"*) is accurate; `L-55`'s compression to *"attributed to B-3 → DISPOSITION OWED at B-3app"*
  would route the disposition to a build that did not cause it. **True owner: I-12.** B-4's diff does
  not touch the file (verified: 0 hits in `git show --name-only`).
- **INFO-6 — `_doc_set_git()` reads the INDEX, not HEAD.** `git ls-files -s` means a staged-but-uncommitted
  note would pass, while the docstring says *"committed blob hashes"* and the falsifier says *"written
  and never committed."* Immaterial here — all seven docs are committed, verified — but it is the
  third registered-vs-implemented gap of the same shape in one build.
- **INFO-7 — engine-wide failures outside the graded surface, not B-4's.** A full run
  (~10,800 tests) showed a failure cluster around the `test_c*` region. The `cascade` subset passes
  **468/468 standalone**, and `test_baton_v1.py` — the only non-kc2 test importing `simulation.kc2` —
  passes **115/115**. So B-4 breaks nothing outside its scope; the cluster looks like cross-test
  pollution. I did not isolate it. Outside B-4's diff and outside the graded surface — **flagged to
  the KR lane, not graded here.**

---

## 4 · My own emissions and deletions, declared under the three-condition rule

- **Emitted:** `kc2-checkpoint-E-s09-cp150-b4-20260824_232932.json`, sha
  `246d4b4d28c2a04a82e513b73e5c27950df312b6a911e646b8fa6462a5e078f9`, by reproducing the driver.
  **Deleted.** Mechanism: never `git add`ed (0 commits), cited by nothing but this paragraph,
  superseded by the restored original.
- **Restored:** the driver deleted `08255194…` during my reproduction. I restored it byte-identical
  from a copy taken **before** the run (`/tmp/jr-b4-gate/`). Re-hashed after restoration:
  `08255194273becf948b43864c12516ecba5cb8bb38b5129b605885351333a0dd` — **exact**. Only `mtime`
  differs. **This restoration is the evidence for BLOCK-1.**
- No other file in any repo was modified by this gate.

---

## 5 · Action

- [ ] **gamora (BLOCK-1, within-seam per ADR-002 — discharge and I re-gate):** stop the driver
      deleting its own artifact of record; derive `condition_3` instead of asserting it; and record
      whether the b4 checkpoint is committed (the b1/b1r/b2 precedent in this run says it can be).
- [ ] **gamora (WARN-1):** strike the false universal *"checkpoints in this run have never been
      tracked"* from the emitted `condition_2_mechanism` and from ADD 5 § 2; publish the union of all
      four deleted b4 files on one surface.
- [ ] **gamora (WARN-2):** widen `B4-P14` to its registered scope and add a mutation proof, or narrow
      the registered form and say so in an addendum. The 40 hits are its own scanner's output.
- [ ] **gamora (WARN-3):** derive `B4-P12`'s population rather than typing it; the `!= 23` falsifier is
      stale against 25.
- [ ] **gamora (WARN-4):** correct ADD 2's "never committed" clause; remove or rename the dead
      `pet_bodies_woken_by_d2` reference in `threat.py:931`.
- [ ] **gamora (WARN-5):** give W1's forward-only repair a `C-B4-n` and a `magnitude_class`, on the
      same reasoning `C-B4-6` already uses for the sealed `control_states.py`.
- [ ] **gandalf (RUN-CONDUCTOR):** hold DRIFT-CRITIC's driver execution until BLOCK-1 is discharged;
      re-point the `test_AC_10_10` disposition from B-3app to I-12 (INFO-5).
- [ ] **knight-rider:** INFO-7, engine-wide test pollution outside the KC2-MC surface.
- [ ] **Matt:** no decision required. BLOCK-1 is within-seam; escalate only if gamora disputes.

⚑ **Not blocked on:** the measurements. Facet (c) SIM's numbers are sound as far as I can re-derive
them, and the `D2_FIRING_ONLY` byte-identity is the cleanest decomposition this run has produced.
BLOCK-1 is about whether the bytes survive being checked.

---

## 6 · References

- `~/Games/reincarnated-engine/src/reincarnated/simulation/math/kc2-mc-b4-specials-2026-08-24.md`
- `~/Games/reincarnated-engine/src/reincarnated/simulation/math/kc2-mc-b4-specials-ADDENDUM-{,2-,3-,4-,5-,6-}2026-08-24.md`
- `~/Games/reincarnated-engine/src/reincarnated/simulation/kc2/pet_specials.py`
- `~/Games/reincarnated-engine/src/reincarnated/simulation/kc2/threat.py` (`:920-963` the source-split site)
- `~/Games/reincarnated-engine/src/reincarnated/simulation/scripts/gamora_kc2_mc_b4_specials_2026_08_24.py`
  (`:1137`, `:1146-1160`, `:1190-1214`, `:1273-1274`, `:1314-1316`, `:1359`)
- `~/Games/reincarnated-engine/src/reincarnated/simulation/scripts/gamora_kc2_mc_b3_summons_2026_08_24.py:176` (WARN-5)
- `~/Games/reincarnated-engine/src/reincarnated/simulation/kc2/secondary_streams.py:136` (INFO-5)
- `~/Games/reincarnated-engine/src/reincarnated/simulation/output/kc2-checkpoint-E-s09-cp150-b4-20260824_232229.json`
- `~/Games/reincarnated-engine/src/reincarnated/export/MIGRATION.md`
- `~/Games/reincarnated-collaboration/agentic_orchestration/gandalf/notes/2026-08-24-kc2-model-completion-run-charter.md` (L-50 … L-55)
- `~/Games/reincarnated-collaboration/agentic_orchestration/qa/findings/2026-08-24-gamora-kc2-mc-b3-gate2.md` (W1–W4)

---

# LIFT VERDICT — 2026-08-24 — B-4rep

**Reviewer:** jack-ryan (DEV-MODE) · **Seated by:** gandalf `RUN-CONDUCTOR`, ledger `L-60`, ruling `R-L60-1`
**Scope:** bounded BLOCK-lift verification. **NOT** a full Gate-2 re-run of B-4rep.
**Target:** engine `7cda1d11` → `30a31ef0` → `e8976e99` → `f1007366` → `71508028`

## ⚑ BLOCK-1 — **LIFTED**

**Checkpoint sha, my own measurement:**
`PRE 08255194273becf948b43864c12516ecba5cb8bb38b5129b605885351333a0dd`
`POST 08255194273becf948b43864c12516ecba5cb8bb38b5129b605885351333a0dd`
`cmp` against my own pre-run backup (`/tmp/jr-b4-lift/`): **byte-identical**. `mtime` **Aug 24 19:30, unchanged** — the file was never opened for write. `git status` on the path: unmodified vs index.

### (a) Tracked, and the git copy is the real recovery path

`git ls-files -s` → blob `7216c177870adee1b3ba0804f5baa37b8460e7fa`, committed at `30a31ef0`, one commit in `git log --all` for the path. `git cat-file blob 7216c177 | shasum -a 256` → **`08255194…`**. The committed *content* equals the disk bytes, so the record is now recoverable from git rather than from one reviewer's `/tmp`. Discharge path (b) is real, not nominal.

### (c) I ran the act that destroyed it, and it survived

I ran `gamora_kc2_mc_b4_specials_2026_08_24.py` in full — the exact execution that destroyed `08255194…` during Gate 2. Exit 0, wall 24.9 s, **26/26 predicates HOLD**, nine byte-guards verified. The record's own `⚑ deletions` block in my emission: `n_deletions: 0`, `n_retained: 1`, `capability_retained_because: ["TRACKED-IN-GIT", "CITED-BY-A-SURFACE"]`, `measurement_n_citing_surfaces: 6` — including `collab:2026-08-24-gamora-kc2-mc-b4-gate2.md`, this file. **Two independent locks, both derived, neither pinned.** I read the sweep source: no filename literal, no sha literal (`:308-435`).

⚑ **And the run produced a proof stronger than the one claimed.** My subsequent b4rep run executed the b4 glob over the **real** `simulation/output/` with two b4 files present, and its `⚑ b4_glob_deletions` block:

| file | tracked | citers | outcome |
|---|---|---|---|
| `…-b4-20260825_015300.json` (my re-emission, `2013113289d1…`) | false | 0 | **DELETED** |
| `…-b4-20260824_232229.json` (`08255194…`) | true | 6 | **RETAINED** |

That is the historical deletion re-enacted with a live payload in the real directory — not `tmp_path` — refusing the record and still taking genuine debris in the same pass. `B4R-P1c`'s synthetic triple-proof is corroborated by an accidental live one.

### (b) Everything I ran myself

| instrument | result |
|---|---|
| `tests/test_kc2_mc_b4rep_sweep.py` | **19 passed** |
| `tests/test_kc2_mc_b4_specials.py` | **28 passed** |
| `gamora_kc2_mc_b4rep_2026_08_24.py` | **14/14 HOLD**; `B4R-P0` tenth guard `PRE == POST == 08255194…`, `unmoved=True` |
| `gamora_kc2_mc_b4_specials_2026_08_24.py` | **26/26 HOLD** |
| `pytest -k kc2` | **531 passed / 1 failed** — the 1 is `test_AC_10_10` on `secondary_streams.py:136`, **I-12** per INFO-5. Registered pass condition met exactly. |

Claim 2 (tenth byte-guard) and claim 6 (531/1) confirmed to the number. Claim 3 confirmed by source read — the exclusion is caused by tracking + citation, hand-listed nowhere.

## W-1 … W-5 — spot-checks

- **W-2 DISCHARGED, and this is the one I checked hardest.** `B4-P14` now grades `split_scan(art)` over the **assembled** artifact (`:1874-1881`), which is its registered scope. My own scanner, run by me: **40 hits** on the historical record (preserved deliberately as the `B4R-P5c` payload), **0 hits** on the b4rep artifact **and 0 on my own b4 re-emission**. The repair is a **rename** — `PetSpecialGateFold.prices()` now emits `measurement_c_b4_*` — not a scanner exemption. I confirmed that in-process. The falsifier that could not fail now fails on real input.
- **W-1 DISCHARGED.** The false universal is **struck** on the emitted `condition_2_mechanism` — I read it in my own emission, not in an addendum. The four-file union is on **one** surface, derived, per-member provenance: `230721`, `231201`, `231425`, and ⚑ `231817` / `63b0f0f9184ecde7…` labelled *"the artifact of record only — no addendum"*, which is precisely the gap I named. Members whose sha no surviving surface carries emit `sha256: ""` rather than an invented one. Correct.
- **W-3 DISCHARGED.** `registered_predicate_ids()` derives the population as a set from the docs; no integer survives to go stale.
- **W-4 DISCHARGED.** `pet_bodies_woken_by_d2`: **0 hits** in `src/**/*.py`. Survives only in addenda and emitted artifacts, where it is evidence.
- **W-5 DISCHARGED as a disclosed refusal**, which is what I asked for. `C-B4R-1` carries `magnitude_of: population`, class `measured`. `gamora_kc2_mc_b3_summons_2026_08_24.py:176` still reads `{0, 1, -1, 2, 3, 4}` — unrepaired at its own address, now **priced and classed** rather than silently forward-repaired. `B4R-P7` exercises the exemption register with two synthetic sources and convicts exactly one; the never-fired mechanism has now fired.

## What still rides — none of it blocks the lift

- ⚑ **WARN-R1 — the same hostage condition is live one directory over.** `kc2-checkpoint-E-s09-cp150-b3-20260824_202328.json` — the **B-3 SEALED** record, byte-guarded as `dd13408e…` by every successor and read by B-4's `§A PRE` as the record-cell parent — is **UNTRACKED**. So are both `b2app` checkpoints. Mitigating and materially different from BLOCK-1: I read the b3 driver and it contains **no `unlink()`**, so nothing self-destructs. But it is one copy of a non-regenerable file that eight-plus predicates depend on, and the remedy is the one `30a31ef0` already demonstrates. Cheap now, unrecoverable later.
- **INFO-R1** — the b4rep record is retained on **one** lock (`TRACKED-IN-GIT`, 0 citing surfaces) where b4's has two. Adequate; asymmetric.
- **INFO-R2** — `_git_tracked_output` matches by **name**, so a same-named file elsewhere reads as tracked. Disclosed in the test as deliberate, erring toward RETAIN. I agree with the direction.
- **INFO-R3** — the citation lock is a **monotonic ratchet**: any sha written into a committed surface becomes permanently undeletable. Registered as `S-B4R-1`, sign DOWN-deletion-permissiveness. Direction correct; the retention set only grows.
- **INFO-R4** — `pytest -k kc2` emitted ~8 further untracked `cycle-13-gauntlet-sim-results-*.json` into `simulation/output/` (~300 accumulated). Nothing sweeps them. Outside B-4rep's scope — **KR lane, with INFO-7.**

## My own emissions and deletions, declared under the three-condition rule

- **Emitted** `kc2-checkpoint-E-s09-cp150-b4-20260825_015300.json`, sha `2013113289d1401c5b181dbd1840e11907c34a452c82c8af1bfeb58f93308126`. **Deleted by the repaired sweep itself**, correctly classified untracked + uncited.
- **Emitted** `kc2-checkpoint-E-s09-cp150-b4rep-20260825_015354.json`, sha `9efe5a37b7f762b9c22df46dd4f8d4a6cc67896fcae3f7f21ffd208b18116d12`. Classified `DELETABLE` by the admission test; I deleted it on that verdict rather than on my own judgement.
- Backups at `/tmp/jr-b4-lift/`. **No file in any repo was modified by this verification**, and `simulation/output/` ends with exactly one b4 and one b4rep checkpoint — D5 clean.

## Action

- [x] **gamora — BLOCK-1 DISCHARGED. The gate is LIFTED.** No further action on the BLOCK.
- [x] **gandalf (RUN-CONDUCTOR):** the `R-L55-1` operational hold on DRIFT-CRITIC's driver execution is **RELEASED**. The driver is now safe to run; I ran it twice.
- [ ] **gamora (WARN-R1, within-seam, not blocking):** `git add` the b3 SEALED and b2app checkpoints. Same remedy as `30a31ef0`, same reasoning, and B-3 being sealed is an argument *for* committing it, not against.
- [ ] **gandalf:** `test_AC_10_10` disposition still owed against **I-12**, not B-3app (INFO-5, unchanged).
- [ ] **Matt:** no decision required. The discharge was within-seam and it landed.

⚑ **On the record.** I raised BLOCK-1 because I destroyed the artifact by reviewing it. gamora's repair did not bolt an exclusion list beside the claim — it turned the three declared conditions into the admission test, so the sweep now *executes its own stated licence*. That is the difference between a fix and a repair, and the run should keep the distinction. `S-B4R-1` is signed in the right direction: the build is strictly more reluctant to delete than it was.
