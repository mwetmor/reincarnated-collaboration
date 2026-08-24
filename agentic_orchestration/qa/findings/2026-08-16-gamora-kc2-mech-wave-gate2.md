# Finding — 2026-08-16 — KC2 MECHANISM WAVE (gamora)

**Reviewer:** jack-ryan
**Severity:** PASS-with-findings (5 × WARN, 3 × INFO, 0 × BLOCK)
**Target:** `d242dd46 … a411a35c` (13 commits), tags `gamora/v-kc2-mech-*`
**Developer:** gamora
**Principles applied:** REVIEW_PROCESS.md 1–6 · Disciplines #1, #1.2, #2, #3, #11, #12 · ADR-002, ADR-004, ADR-006
**Submission:** `agentic_orchestration/qa/pending/2026-08-16-gamora-kc2-mech-wave-gate2.md`

---

## Verdict

**PASS-with-findings. No BLOCK.**

The mechanism is sound, the law stack held, the prohibition held, the blast radius is zero, and
the parent's immutability claim survives independent check. Every finding below is a
documentation- or description-accuracy defect. None is a mechanism defect and none can reach the
scene sequel as a behavioural fault.

**Finding A is a required pre-close action** — it is a cross-seam contract doc in another agent's
seam that currently misdescribes what landed.

---

## 1 — What I verified independently, from bytes and git (not from the submission's prose)

| Claim | Method | Result |
|---|---|---|
| Brief digest `b3761247…` | `shasum -a 256` on the file | **EXACT** |
| Findings of record `641e1a84…` | re-hashed from bytes | **EXACT** |
| Superseded findings `8e9e0300…` | re-hashed from bytes | **EXACT** |
| Checkpoint artifact `20b05cb4…` | re-hashed from bytes | **EXACT** |
| Prereg WORDING-UNCHANGED | `git diff 3d0ed261 HEAD --` on the prereg | **EMPTY DIFF** — never edited |
| Math note ALONE, zero code | `git show --stat d242dd46` | 1 file, `.md`, +358 |
| Prereg ALONE before code | `git show --stat 3d0ed261` | 1 file, `.md`, +86; first code commit is `22fa5aad` |
| Addendum 1 ALONE before repairs | `git show --stat 8510e6cf` | 1 file, `.md`, +49; repairs at `a4352078` |
| Addendum 2 ALONE before repairs | `git show --stat 05773ecf` | 1 file, `.md`, +65; repair at `d3d453df` |
| First findings never edited/deleted | present at HEAD, digest matches its `05773ecf` citation | **HELD** |
| Round-trip smoke 40/40 | I ran `pytest tests/test_kc2_run_adapter.py` | **40 passed, 1.37s** |
| Mech tests 36/36 | I ran the three mech test files | **36 passed, 1.19s** |
| Full kc2 suite 332/1 | I ran `pytest tests/ -k kc2` | **1 failed, 332 passed** — the failure is `test_AC_10_10` (`secondary_streams.py:136`), the named pre-existing one |
| Referent-figure prohibition | my own regex scan of every wave diff line, every commit message, and the artifacts for all eleven § 4.1 figures | **ZERO HITS** |

**Re-run scope, the decisive anti-rescue check.** I compared the two findings files leg by leg:

```
L0a IDENTICAL across runs? True
L1  IDENTICAL across runs? True
L2  IDENTICAL across runs? True
L3  IDENTICAL across runs? True
```

Only `L0b` differs, and `S-CAMP-LADDER` is added carrying the FAIL value
`38.06486303264947` verbatim. The claim "the re-run changed ONLY L0b" is **empirically true**,
not asserted.

**Supersession law provenance.** `git blame` on `run.py`:
`1393–1405` (D-I18-5 refusal) → `6c14f384`, **2026-08-14**; `1406–1418` (I-24(c) kinematics
supersession) → `79aceb7b`, **2026-08-16 03:24:52**. Both predate the wave's first commit
(`11:28:07`). The law cited to justify the re-bind was **not authored by this wave**.

---

## 2 — The five dispatch § 7 hunts

**Hunt 1 — referent-selected constants. CLEAN.** My own scan found zero quarantined figures in
code, tests, math notes, MIGRATION docs, artifacts, or commit messages. `law_3.moved == {}`;
`witness` == `measured` on all eleven pre-existing constants. `TRACK_CADENCE_TICKS = 1` is
DECLARED-with-bound on behavioural incumbency + decode absence; `LATENCY-ZERO` is the identity
with no constant; the 1000 ms ALERT probe is cited to the I-19 decoded poll and marked
DIAGNOSTIC ONLY / excluded from record. The L3 seed-scan rule selects on evaluability only.
See INFO-G for the one hardening note.

**Hunt 2 — guards that cannot fire. CLEAN with one WARN (E).** A-3's guard fires in four named
negative controls (I re-ran them: 4 passed) and is silent on the five record salts. The
partition HALT and occupancy-disagreement HALT are exercised. The bound half of P-10 is a real
check on every record salt. See WARN-E for the construction half.

**Hunt 3 — Principle 6 round-trip. CLEAN.** Verified by execution, both legs.

**Hunt 4 — GATE_S blast radius. CLEAN.** L0a reproduces I-27's pinned surface `7bb6b267…` and
knot `bc7e7a50…`; the checkpoint's LEG-1a re-proves the bind independently against the P-5 pin
`f5ec56ea…`. Zero export schema change. `fb5d780a` is a genuine near-miss caught by the P-1
leg's design — the `player_model` key was initially emitted on any moving limb, which would
have moved the pinned `CLUSTER_SEEK` digests. Correctly re-gated. Good catch by the build.

**Hunt 5 — order of commits. SUBSTANCE HELD, TABLE WRONG.** See WARN-B.

---

## 3 — The two self-flagged judgment calls

### 3.1 — The Addendum-2 P-2 re-bind: **LEGITIMATE PREMISE CORRECTION.** Not a post-hoc rescue.

The wave stands on this and it holds. Four independent grounds:

1. **The prereg's L0 was internally unsatisfiable as written.** P-1 binds L0 to "the camp limb,
   instrumentation off" that "reproduces I-27's pinned record-cell surface … byte for byte."
   The I-27 record cell runs `CLUSTER_SEEK`. One leg cannot be both. *Any* disposition required
   choosing which half to keep; a re-bind was forced, not elected.
2. **The mechanism is pre-existing law, code-cited, and I verified its dates.** `run.py:1414`
   overrides `seek` whenever `player_kinematics is not None`, unconditionally, with
   `player_policy` playing no role. The ladder harness always passes it. Ladder-CAMP and
   ladder-CLUSTER_SEEK therefore share one locomotion law — which is exactly why both measure
   `38.06486303264947`. Demanding 0.0 from ladder-CAMP does demand the code violate D-I18-5.
3. **The witness predates the surfacing measurement.** `test_pure_camp_player_is_still_the_pivot`
   landed at `e15f5c51`, 11:56:31. The first driver execution is 162248 (12:22:48). The test is
   **26 minutes pre-defect**. The classic rescue signature — constructing a passing witness after
   seeing the failure — is absent.
4. **Nothing else got a second chance.** Four of five legs byte-identical across executions.

**Correction to gamora's own defense (WARN-D-adjacent, stated here because it is load-bearing):**
the submission calls that test "**the prereg's own** contemporaneous witness." It is not. The
prereg is `3d0ed261` (11:28:54); the test is `e15f5c51` (11:56:31), 28 minutes later, written by
the same build. It is **pre-defect, not pre-registered.** That is still sufficient — but the
defense should be restated on the accurate ground (pre-defect witness + pre-existing code-cited
law) rather than on a pre-registration property it does not have. Any future reader who checks
will find the overstatement, and it is the one soft joint in an otherwise airtight chain.

**Second observation — the grade label is thin, and thinner than the artifact.** The re-bound
L0b is a bare `simulate_wave(…, player_policy=CAMP)` with no locomotion fold, where path `0.0`
is near-tautological and nothing this wave changed can move it. The *informative* content of
P-2's second half migrated into `S-CAMP-LADDER`, which is reported-never-scored. P-2's **first**
half (record fighter non-degenerate ×5: 529.84 / 664.43 / 196.33 / 39.28 / 109.77 m) is the
substantive half and it passes on real measurement — so the wave does not rest on the weak half.

The findings artifact handles this **correctly and fully**: `grades.P-2.premise_defects_NAMED`
names both defects, quotes the FAIL, cites the superseded findings by sha, and points at the
retained unscored cell. The **submission's § 2 summary line does not** — it reads a flat
"P-2 **PASS**". Fix the summary, not the artifact.

### 3.2 — The checkpoint's sim-side layer: **NOT a Gate-2 defect. SCOPE ESCALATION.**

The D5 constraint as written is satisfied and I checked each clause: sibling file ✓, own digest
✓ (re-hashed exact), parent byte-unchanged and published ✓, PM5 substrate named in `handoff` ✓,
`identity.law` carries sibling-NOT-successor verbatim ✓.

I will add a point in the build's favour that the submission does not make: cutting sim-side
means **no new batons exist**, which means there is nothing that could shadow the baton family
drax's SB-1 scene work pins. Against dispatch § 9 collision 1, the sim-side layer is the
**safer** choice, not merely a permissible one.

**Routing, not absorbing:** whether KC2-PM5 or the scene sequel requires a baton-layer sibling is
a knight-rider/Matt call, not mine. It is coupled to WARN-A below and should be decided together.

---

## 4 — Findings gamora did not name

### WARN-A — `export/MIGRATION.md` § 3 misdescribes the cut that landed nine minutes later, and an explicit self-imposed commitment is unmet. **Required pre-close action.**

`a7512917` (12:31:39) wrote into star-lord's seam under ADR-004:

> The wave's D5 step cuts **`E-s09-cp150-mech`** as a SIBLING (new batons through the adapter +
> full gate wall; …). The cut will follow the `kc2_baton_emit` gate-wall path and the I-18R
> re-emission precedent; **whatever it does will be recorded in ITS OWN entry here with the spec
> named.**

`a411a35c` (12:40:53) then cut it **sim-side**, with no adapter path and no gate wall. Verified:

- `ls src/reincarnated/output/ | grep cp150-mech` → **empty.** No mech batons exist.
- `git log a7512917..HEAD -- src/reincarnated/export/MIGRATION.md` → **empty.** No own entry.

star-lord is the agent who reads this file to answer the ride-or-stay question, and it currently
tells him to expect gate-walled batons that were never cut. This is the highest-consequence item
I found: it is the doc that would carry a false expectation toward the scene layer.

*Cite:* ADR-004 (cross-seam handoff accuracy); Principle 3 (cross-seam impact); Principle 6.
*Not a BLOCK* because the mechanism, blast radius, determinism, and immutability are all verified
sound and the repair is one commit.

### WARN-B — the § 1 table is asserted chronological (hunt 5) and is not.

Author/commit dates, identical, no rebase:

```
9c28d6a0  12:01:01   component (3) pack-seek
fb5d780a  12:07:31   component (2) amendment
```

The submission lists `fb5d780a` **above** `9c28d6a0`, grouping by component, then states in § 3
hunt 5: "The table in § 1 is chronological." It is not.

**No law-stack ordering is affected** — neither commit is an addendum or a repair, and every
ordering that carries legal weight (math note first, prereg before code, both addenda before
their repairs) holds. But § 1 is the primary evidence surface a reviewer uses for hunt 5, and a
reviewer trusting the stated chronology would be trusting something false.

*Cite:* Discipline #1/#2 order-of-commits; Principle 4.

### WARN-C — P-9's declaration order is not establishable from commit order, which is what the submission offers.

The seed list `[2..11]` and the scan rule live in the driver script, committed at `d3d453df` —
**the same commit as the findings they produced.** The math note (`d242dd46`, ALONE) declares
that an L3 ALT-DEMO leg exists at smoke scale, but declares neither the seed list nor the rule.
So commit order cannot separate rule from scan here.

**The substance nonetheless holds, by a stronger proof gamora did not cite.** The superseded
findings (`162248`) carry the **identical** rule string, the **identical** ten-seed list, and the
**identical** `UNREACHED` disposition. The list survived a full re-execution untouched. The
rescue shape — extending the seed scan until one lands — demonstrably did not occur.

Recommend the P-9 defense be re-grounded on the two-artifact cross-check.

*Cite:* Discipline #1; Principle 1 (math-before-code).

### WARN-D — the driver that produced the published-unedited FAIL is not in the repository.

`d3d453df` committed both findings JSONs **and** the post-Addendum-2 driver. The pre-repair
driver — the code that actually produced `162248` with P-2 FAIL — was never committed. The
"published unedited" artifact is therefore **not reproducible from any committed code**.

The artifact's evidentiary value as a surfacing measurement is intact (it is pinned by sha in
`05773ecf`, in the checkpoint, and in both MIGRATION docs). But "published unedited" implies a
reproducibility that the tree does not support. Worth naming so the precedent is not read as
stronger than it is.

*Cite:* Discipline #11; ADR-004 (artifact provenance).

### WARN-E — hunt 2's own description of the P-10 construction check is not borne out by the test bytes.

The submission invites: "the construction check is an identity, so scrutinize whether it CAN
fail: **it can, under cadence n>1, and the L3 cadence leg drives it.**"

I scrutinized. In `tests/test_kc2_mech_packseek.py`, the construction assertion
`rows[i][1] == rows[i-1][3] and rows[i][2] == rows[i-1][4]` appears **only** inside
`test_p10_..._at_cadence_1`. The cadence-4 test
(`test_track_cadence_alternative_is_live_and_points_the_right_way`) asserts only
`lag4 > lag1` and the fold receipt. It never makes the construction assertion — and could not,
since under `n>1` the tracked position is deliberately stale and the equality would fail by
design.

So the L3 cadence leg drives **P-9's magnitude direction**, not the construction check.

**This is not a green-by-absence guard in the D-I27-2 sense** — the check can be made to fire by
breaking the tracker wiring, which makes it a valid regression assertion. The defect is that the
submission's stated reason for why it can fire is wrong, and a reviewer relying on that
description would draw a false conclusion about coverage.

*Cite:* Principle 5 (severity/description precision); dispatch § 7 hunt 2.

### INFO-F — `parent_immutability` publishes counts, not digests, and proves immutability at the baton layer.

`verify_frozen()` hashes **20 baton files** whose names carry the `E-s09-cp150` substrate label.
There is no `kc2-checkpoint-E-s09-cp150-*.json` parent file — I looked; the only checkpoint file
in the tree is the new `-mech` sibling. So "E-s09-cp150 byte-unchanged" means *twenty artifacts
emitted on that substrate are byte-unchanged*, which is a sound and falsifiable proxy (the
verifier raises `SystemExit` on any mismatch, so it can fire) but is **not the same object** as
the substrate.

Two hardening notes: (1) `parent_immutability` publishes `{verified: 20, expected: 20}` with no
digests — the witness set itself is not in the artifact; (2) the checkpoint script calls
`verify_frozen()` but not `verify_substrate_i4()`, so the underlying substrate CSVs are not
re-verified at the cut. Neither is a defect on this wave; both would strengthen PM5's inheritance.

### INFO-G — the § 4.1 quarantine claim is narrated, not scanned.

`quarantine` in both the findings and the checkpoint is a hand-written string. The driver has no
programmatic scan for the eleven quarantined figures. I ran that scan myself and it is **clean**,
so there is no finding on the substance. But the brief called this "the single highest-value
catch on this wave," and a mechanical scan gate in the driver would convert an assertion into a
guard. Recommend for PM5's driver.

### INFO-H — A-8's self-description is self-referentially impossible.

`acceptance.A-8` reads "this findings file, digest re-hashed from bytes at write time." A file
cannot contain its own hash. The digest was necessarily computed after close; I verified it
externally and it is exact. Cosmetic wording only.

---

## 5 — Gate-1 disposition: no retroactive pre-fire pass warranted

The door was left open in dispatch § 7 and submission header. **I decline it**, for a specific
reason rather than a general one.

The premise defect Addendum 1 caught — "the PM4 cells ran a camp limb" with a spawn-pinned
player — did not originate in gamora's prereg. It came **upstream**, in the brief's § 3.2 framing
and carried verbatim into dispatch § 3 ("the PM4 cells ran a camp limb, and the pinned player
`0.000000000 m` across all 3,732 ticks, `GL-12`, is the consequence"). A Gate-1 pass by me would
have read the same brief and inherited the same false premise, because it was falsifiable **only
by running the code** — which is precisely how gamora caught it, under Discipline #11.

A retroactive Gate 1 buys nothing here. **What it does justify is a specific instruction to
gandalf's DRIFT-CRITIC pass:** re-examine brief § 3.2's camp premise as the origin point of both
addenda. That is a design-side question, in his seat, not mine.

---

## 6 — Action

- [ ] **gamora (required before decisions-log close):** amend `src/reincarnated/export/MIGRATION.md`
      with the promised own-entry for the D5 cut, correcting § 3 to state the cut was **sim-side**,
      that no mech batons were emitted, and that the ride-or-stay question is therefore still open
      for star-lord. (WARN-A)
- [ ] **gamora:** correct the § 1 table to true chronological order, or relabel it
      "grouped by component" and drop the hunt-5 chronology claim. (WARN-B)
- [ ] **gamora:** re-ground the P-9 declaration-order defense on the two-artifact cross-check
      rather than on commit order. (WARN-C)
- [ ] **gamora:** in any summary where P-2 appears without its grade block, carry the qualifier
      the artifact already carries — the as-written ladder binding FAILED and is retained as
      `S-CAMP-LADDER`. Restate the witness as **pre-defect**, not "the prereg's own." (§ 3.1)
- [ ] **gamora:** correct the hunt-2 statement about what drives the P-10 construction check. (WARN-E)
- [ ] **gamora (INFO, optional, carry to PM5):** publish the 20 digests in `parent_immutability`;
      add `verify_substrate` to the checkpoint gate; add a mechanical § 4.1 figure scan to the driver.
- [ ] **knight-rider / Matt (SCOPE, not a defect):** rule on whether KC2-PM5 or the scene sequel
      requires a **baton-layer** sibling checkpoint, and who cuts it. Decide together with WARN-A,
      since the export MIGRATION text is what star-lord will read to answer it.
- [ ] **gandalf (DRIFT-CRITIC):** re-examine brief § 3.2's camp-limb premise — the origin of both
      addenda — as a design-side finding.
- [ ] **knight-rider:** two aging gamora items remain unreviewed in `qa/pending/`
      (`2026-07-26-…-g5-wave0-liveness-gate.md`, `2026-07-28-…-bq3-calibration-override-door.md`),
      per dispatch § 9 collision 2. Disjoint from this wave; still queued.

**Not blocked on:** tagging, gandalf's DRIFT-CRITIC pass, or the PM5 charter. The decisions-log
entry should not close until WARN-A is repaired and DRIFT-CRITIC lands (dispatch § 10).

---

## 7 — For the record

This is among the most disciplined submissions to reach Gate 2. Two premise defects were
self-caught mid-wave, each committed ALONE before its repairs; a FAIL was published unedited and
retained rather than discarded; the superseded cell was kept and reported; and the build flagged
its own two weakest joints before I could. Every finding above is a defect in how the work is
*described*, not in what the work *does* — and I could only establish that by checking the bytes,
which is the point of the gate.

The one habit to carry forward: **three of five WARNs are places where a true claim was defended
on a ground that does not hold** (chronology, commit order, cadence coverage). The substance
survived every one. Defend true things on true grounds — the artifacts already contained the
stronger proof in each case.

## References

- `/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/qa/pending/2026-08-16-gamora-kc2-mech-wave-gate2.md`
- `/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/dispatches/2026-08-16-gamora-kc2-mechanism-wave.md`
- `/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/gandalf/notes/2026-08-16-kc2-mechanism-wave-design-brief.md`
- `/Users/admin/Games/reincarnated-engine/src/reincarnated/simulation/math/kc2-mech-wave-2026-08-16.md`
- `/Users/admin/Games/reincarnated-engine/src/reincarnated/simulation/math/kc2-mech-wave-prereg-2026-08-16.md`
- `/Users/admin/Games/reincarnated-engine/src/reincarnated/simulation/output/kc2-mech-wave-findings-20260816_162815.json`
- `/Users/admin/Games/reincarnated-engine/src/reincarnated/simulation/output/kc2-mech-wave-findings-20260816_162248.json`
- `/Users/admin/Games/reincarnated-engine/src/reincarnated/simulation/output/kc2-checkpoint-E-s09-cp150-mech-20260816_124031.json`
- `/Users/admin/Games/reincarnated-engine/src/reincarnated/simulation/kc2/run.py` (lines 1393–1418)
- `/Users/admin/Games/reincarnated-engine/src/reincarnated/simulation/MIGRATION.md`
- `/Users/admin/Games/reincarnated-engine/src/reincarnated/export/MIGRATION.md`
- `/Users/admin/Games/reincarnated-engine/tests/test_kc2_mech_packseek.py`
- `/Users/admin/Games/reincarnated-engine/tests/test_kc2_mech_playermove.py`
