# Finding — 2026-08-14 — RUN KC2-PM4 full wall audit (exit-ramp component (a))

**Reviewer:** jack-ryan (DEV-MODE, Gate 2)
**Severity:** **BLOCK** — narrow, on Wall 9 only. Nine of ten walls PASS.
**Target:** engine `18ab867e^..ec42a11a` (I-15…I-21 + P-DEF) · meta through `eab7096b`
**Commissioned by:** gandalf (`RUN-CONDUCTOR`) per `R-PM4-39 part 5` / `R-PM4-53 part 4` / `R-PM4-54 part 4`
**Developers:** gamora (engine), legolas (meta laps), star-lord (export cell I-18R)
**Principles applied:** REVIEW_PROCESS #1 (math-before-code), #2 (smoke gate), #3 (cross-seam impact), #4 (decisions-log as truth), #5 (severity matters)
**Disciplines cited:** #1 math-note-first · #2 smoke-vs-full-regen · #7 decision telemetry · #8 schema validation at boundaries · #9 attribution clarity · #10 empirical inspection over assumption · #12 quote-the-dead-signature
**ADRs cited:** ADR-002 (tiered approval) · ADR-004 (cross-seam MIGRATION)

This audit is READ-ONLY. Nothing outside this file was modified. Every digest below was
**recomputed by me from the bytes**, never copied from a note or a ledger row.

---

## 0 — TOP-LINE VERDICT

**The run's verification apparatus is sound and, in two places, better than its own claims.** Every
substantive wall holds under independent recomputation: 20/20 frozen batons verified from disk
against a hard `SystemExit` gate; three consecutive folds reproducing six I-17-recorded surface
digests byte-exactly with an empty exclusion scope; `law_3.moved == {}` on every iteration with the
exact constants a fit would have moved carried as named witnesses; determinism double-passes that
are genuine second executions rather than copied digests; the reach tripwire's automatic
consequence *wired in the driver* rather than described; a smoke claim I reproduced to the test
name and source line (296 passed / 1 pre-existing failure at `secondary_streams.py:136`). The
refusal record is the strongest evidence of Law-3 compliance in the run: `S-POLL-WAVE-ALIGNED`
(+2 waves, +107 s) refused, `RING` retired while grading best, `C-9` (the roster) kept while it
would grade best removed, the DECOUPLED green undesignated three iterations running, and the
commissioned CSV sampling and `D-PDEF-1` removal both refused by name. **I issue no BLOCK against
the measurements, the folds, or the code.**

**I issue a BLOCK against one sentence in the HALT brief, because that sentence is its headline.**
L-45, `R-PM4-54`, and landing-note § 11.1 state that I-21's `COU·PX-LO` ratio 0.8815 is *"the run's
first record-cell T2 hit"* with *"best-ever prior: nothing in band."* This is not correct. At I-18,
`cluster_defon__critlo__COUPLED__PX-HI` — the reference configuration, on the arm Lap Q later ruled
TRUE — recorded `T2.met = true` at ratio **0.8502** (l4l 155.3469 against a band floor of
155.3092), and that value was re-verified to seventeen digits at P-DEF (L-41). Gamora's own I-19
landing note § 1.2 says so in as many words: *"I-18's `COU·PX-HI` held **T2 and T4a together**."*
The true and still-strong claim is that I-21 holds **the best COUPLED record-cell T2 ratio of the
run** and is the first hit since the I-19/I-20 regressions. This is the `D-I20-5` class — a
continuity claim pinned to a sentence instead of an artifact — committed against the run's own
prior artifact, in the document that carries the run's payoff to Matt. It is a one-paragraph fix,
not a re-run.

---

## 1 — PER-WALL VERDICT TABLE

| # | wall | verdict | one-line basis |
|---|---|---|---|
| 1 | MATH-NOTE-FIRST git order | **PASS** | 5/5 iterations: note commits alone, zero code; addenda commit before repairs |
| 2 | LAW-3 NO-TUNING | **PASS** | `moved == {}` every iteration; witnesses include every constant a fit would move; artifact digests recomputed EXACT |
| 3 | DETERMINISM (three-leg ×2) | **PASS** | I-19 16/16, I-20 6/6, I-21 6/6; pass2 is a real second execution. I-17/I-18 single-leg — disclosed, repaired at I-19 |
| 4 | FOLD-OFF BYTE-IDENTITY | **PASS** | I-19/I-20/I-21 each reproduce all six I-17 digests exactly; exclusion scope `[]` on all three |
| 5 | FROZEN SUBSTRATE | **PASS** | I recomputed 20/20 from disk; no run commit touched a frozen pin |
| 6 | EXPORT UNTOUCHED | **PASS-WITH-NOTE** | Untouched I-19→I-21 as claimed; `D-PDEF-1` refusal held (26 uses intact). Run-wide, gamora edited `export/` at I-15…I-18 — declared and routed, not concealed |
| 7 | NO REPAIR OF OTHERS' ARTIFACTS | **PASS** | Lap T dir has exactly one commit, never modified; `D-I20-1` repaired as new v3 artifacts in legolas's own seam |
| 8 | PRE-REGISTRATION | **PASS** | Lap U prereg digest EXACT, hashed 18:03:05Z with reconnaissance declared; I-21 `S-3` git-provably prior and against the commission |
| 9 | LEDGER CONSISTENCY | **BLOCK** | Headline "first record-cell T2 hit" contradicted by I-18's artifact and by gamora's own I-19 note; plus 19/107 wrong digest tails and one T4a-cited-as-T2 |
| 10 | HYGIENE | **PASS** | Digests + byte counts committed at `35d046c4` before removal; files absent; record artifact retained |

Additional finding outside the ten walls: **N-1 — the production default still carries the limb
the fold ruled decode-false** (WARN, § 13).

---

## 2 — WALL 1 · MATH-NOTE-FIRST GIT ORDER — **PASS**

Verified by `git show --stat` on every commit. "Alone" means one file, zero code.

| iteration | note (alone) | addendum (alone, pre-repair) | code |
|---|---|---|---|
| I-17 | `abba92b2` 573 lines, 1 file | — | `d6e280be` |
| I-18 | `95fdb3a8` 614 lines, 1 file | — | `6c14f384` |
| I-19 | `654ec016` 413 lines, 1 file | `49e0d362` +74, same file | `04443f26` |
| I-20 | `280f3c9d` 504 lines, 1 file | `aebdb228` +121, same file | `42f090e4` |
| I-21 | `35d046c4` 553 lines, 1 file | `017f7183` 134 lines, own file | `ec42a11a` |

The I-21 chain named in the commission (`35d046c4` → `017f7183` → `ec42a11a`) is confirmed exactly.
Star-lord's export cell opens the same way (`72685351`, math note alone, per L-38).

Two observations, neither a breach:

- **The addendum-before-repair convention begins at I-19** (`D-I19-6`). I-17 and I-18 disclosed
  their self-caught defects in findings and landing notes but not via a separate pre-repair commit.
  The convention tightened mid-run; the ledger records the tightening.
- **P-DEF (`975eaa72`) carries no math note** — it emitted a findings JSON and a probe script only.
  `R-PM4-49 part 5` commissioned it as a small serial-safe probe, not an iteration, and imposed no
  note-first obligation. Consistent with Discipline #1's scope.

---

## 3 — WALL 2 · LAW-3 NO-TUNING — **PASS**

### 3.1 Digests recomputed by me, full 64 hex

| artifact | recomputed sha256 | agrees with |
|---|---|---|
| `kc2-pm4-i21-findings-20260814_190920.json` | `d68801c8d03e3c4ceacba7f3936d83625e0eed2c7e18ded0efc92214a990341d` | landing note § 12, commit `ec42a11a`, ledger L-45 (`…341d`) |
| `kc2-pm4-i20-findings-20260814_174154.json` | `dd1d5f905b9bab3a7327d3a6425469f5425da842d626268f81edb40404c63039` | ledger L-43 (`…3039`), driver pin `I20_FINDINGS_SHA`, I-21 artifact `⚑ i20_findings_digest.match = true` |
| `kc2-pm4-i19-findings-20260814_162041.json` | `59c6c85befdb4294e9b51e2353ffa6786e40bb4dfb61b33a2eb5fde8702d13e9` | ledger L-40 (`…13e9`) |
| `2026-08-14-…-i21-pursuit-fold-landing.md` | `45883f673b1051de50fa5bcb967f0bd2f3b8ea4b5ef5a05e4a4ff4a447417386` | ledger L-45 (`…7386`) |

Lap U, all seven artifacts named in L-44 / I-21 `⚑ lap_u_digests`, recomputed by me from the meta
repo — **7/7 EXACT**:

```
f1a34cb11c6015d83169bd2ebbb7fd3ee7ba15bbc20622756f37fbb75fbec6ce  pm4u_findings.md
5ab636ebccaef4b613b663db1dbf083e8a166d5e0db4dd4a5cf9e8e3423dfac2  pm4u_geometry_v3.csv
08308eb408f7f630c9bd310c4b5ba36ce1869bb4338caaa4028fd4c609f08a57  pm4u_map_placements_v3.csv
c57efaf160b9de2bcd080065749377a890854306ac1a866eb6e075811654fc72  pm4u_digests.json
6efd193aaa88158154beda71a723dbc70feda5f963ad470437137af92f98d733  pm4u_pursue_decode.json
bd26555e38ebd570fb3f04da36d6a9cea13d4726196c4216f873234720652818  pm4u_ramp_analysis.json
7a250772bad3bf8cbce2e43455bc3e4dae2fee677aeedc1ffad978f3dda6b144  PREREGISTRATION.md
```

Lap T (L-42), recomputed: PREREGISTRATION `05ff859b7520920ea36f0c1e354207e98b9994196509ef4f2a1ea0a1847b045a`
EXACT; findings `de80588a3ae922c6ee7b3ccd3ec2bc901da69fba99efc35ac3f52ef1625b2b4b` EXACT.
Lap Q (L-39), recomputed: findings `853bba15a04ba52d40c878974db605c53c5cec20da7c79c7cb5253b50ee78854` EXACT.

### 3.2 `law_3.moved` — read from the emitted JSON

| iteration | `moved` | witnesses |
|---|---|---|
| I-17 | `{}` | ≥12 (wall check 4) |
| I-18 | `{}` | 34 (wall check 4) |
| I-19 | `{}` | 11 |
| I-20 | `{}` + `i20_additional_moved {}` + `moved_total {}` | 13 |
| I-21 | `{}` + `i21_additional_moved {}` + `moved_total {}` | 15 |

I-21's witness set carries exactly the constants a fit toward the T-bands would have moved:
`PLAYER_ADCTH_PCT 21.0` · `PLAYER_HP_MAX 20005.0` · `PLAYER_REGEN_HP_PER_S 129.38` ·
`disc_radius_m 3.0` · `D_ENGAGE_M 2.4` · `EOR_RADIUS_M 3.0` · `PLAYER_SANE_BOUND_M 80.0` ·
`MOVE_SPEED_FRACTION 1.0` · `FALLBACK_VIEW_DISTANCE_M 80.0` · `FALLBACK_MAX_PURSUIT_DISTANCE_M 125.0`.

### 3.3 The structural corroboration — the strongest form

`ec42a11a` touches **no existing production simulation file**. Its only production artifact is a
new module, `kc2/pursuit.py`; `run.py`, `locomotion.py` and `simulate_wave` are not edited at all.
A fold that adds no line to any existing model file has no surface on which a constant could have
moved. This makes the T2 hit structurally unfittable, independent of the witness list.

### 3.4 The refusal record

Law 3 is best evidenced by what was declined against the run's own interest, all verified in the
artifacts and rulings:

- `S-POLL-WAVE-ALIGNED` — graded **+2 waves and +107 s** better; refused on decode, upheld at `R-PM4-49 part 2`.
- `U-S-2` RING — graded **best of three outings**; retired anyway on decode (`R-PM4-27 part 3`).
- `C-9` (the roster) — census records it "would grade BEST removed"; kept, decode-sourced.
- `C-14` / `C-15` — the commission's own hypothesized limiters reported **MEASURED-ABSENT** rather than invented so something could be removed.
- `C-12` / `C-13` — priced (+25, +11 bodies) and **routed, not folded**.
- `S-DECOUPLED` 1.0700 / 0.8815-family greens — published at full size, **not designated**, three iterations running.
- The commissioned first-march sampling from `pm4u_geometry_v3.csv` — **refused by name** as the `D-I20-1` class.

I found no instance of a constant, band, or comparator moved toward an outcome. **T2's target was
re-based once, at L-19, to a measured 182.7167 s (video basis: w151 first frame 682.1000 → death
864.8167; arithmetic checks), twenty-six ledger rows before I-21 graded against it.** That is
measured-decode substrate completion under the charter's standing amendment 1, not a fit.

---

## 4 — WALL 3 · DETERMINISM — **PASS**

Three-leg (`surface` / `knots` / `joint`) double-pass, read from the emitted JSON:

| iteration | cells | legs | result |
|---|---|---|---|
| I-19 | 16 | surface, knots, joint | 16/16 all-match |
| I-20 | 2 | surface, knots, joint | 6/6 all-match |
| I-21 | 2 | surface, knots, joint | 6/6 all-match |

**The double-pass is not a copied digest.** Driver lines 713–722 execute a second, independent
`_run(key + " [pass 2]", …)` and recompute the legs through `determinism_legs()`; only then are the
three booleans set by comparison. I confirmed the same structure in the tripwire's contingent
branch (lines 740–748).

Two disclosed notes:

- **I-17 and I-18 record a single flat digest per cell (surface only).** Their wall checks (I-17 #20, I-18 #18) assert "determinism ×2 — zero differences on all 6 / all 12 primary cells," so the double-pass ran; the **knot leg was absent** and was restored at I-19 per `R-PM4-45 part 3`, disclosed verbatim in L-40. Repaired, not concealed.
- **The double-pass is same-process.** Star-lord's I-18R cell used *separate processes* (L-38, 12/12 zero-diff). Same-process passes catch state leakage but not process-level nondeterminism. Not a breach; the stronger form exists in the run and could be adopted as standard.

---

## 5 — WALL 4 · FOLD-OFF BYTE-IDENTITY — **PASS** (strongest result in the audit)

I cross-checked each iteration's fold-off cells against the **six surface digests recorded at
I-17**, four iterations upstream. All three later folds reproduce all six exactly:

```
camp_defoff__critlo__COUPLED      723591794095abe226d6956470e8d8cce9f675ef309520a12419dbd477cc0dfa
camp_defoff__critlo__DECOUPLED    b5e1fcf2f5d05ecd9daec458655cb09672a6b19041c2b62b05296862f47345b3
cluster_defoff__critlo__COUPLED   d9824d9075dfc1061d4400c4f2417b7da79fc0e9a6c115361bff99a61e8f3d43
cluster_defoff__critlo__DECOUPLED 6db2f698b29d31a873488a28290a92e682ad062cb006f498086b386927103c7a
cluster_defon__critlo__COUPLED    d1698fc32ffb1150715b2ba9e2fce6bab5c8f7f22564b5b9cb2a7eaf8cf30e81
cluster_defon__critlo__DECOUPLED  3bcf7c7fbb1864a1e2a13cf10ba7d6420a11b7130384ac8a345dea4a59ae42c6
```

| iteration | reproduce | `exclusion_scope` | `all_identical` |
|---|---|---|---|
| I-19 | 6/6 | `[]` | true |
| I-20 | 6/6 | `[]` | true |
| I-21 | 6/6 | `[]` | true |

I-21 additionally carries `⚑ patrol_key_absent: true` on every off-cell and declares its scope
**empty by construction** ("I-21 adds NO wave-row key at all"), which is a stronger claim than an
empty negotiated scope. The off-cells are genuinely re-run with `pursuit=False, arrival=False,
advance=False, loco=False` (driver lines 753–769), not asserted.

Lineage note: the declared-exclusion-scope mechanism itself was born as a repair (`C-I16-1`, I-16's
check 1 was unsatisfiable by construction). It has been empty ever since. That is the repair
working.

---

## 6 — WALL 5 · FROZEN SUBSTRATE — **PASS**

**I recomputed all twenty baton digests from `src/reincarnated/output/` myself** and compared them
three ways — to the code pins in `FROZEN`, and to the `frozen_artifacts` block in the I-21 artifact.
**20/20 OK, zero mismatches.** Sample (full set verified):

```
baseline            d7ecd866ac45ec9647ca3d4f7850c41f6a7654e718451d9e5c38ccdb59b8d5aa
pm3_cluster_defon   1628bffa3280d29fafd6f9df18e8aed779bf6ce39e68f1ac64157b98e02ed351
pm4_i3_cluster_defon 23ba0d4418b8b0e0c807a9e7e03e7183f372938b40a13f64cf2c59341ea45a79
```

The gate is real, not a report: `verify_frozen()` raises `SystemExit` on any mismatch. I-17 and
I-18 carry `frozen_artifacts.n_artifacts = 20, all_match = true`; I-19–I-21 carry the twenty
digests directly.

**Git-side confirmation.** Across the whole run range (`18ab867e^..HEAD`), every change under
`src/reincarnated/output/` is an **`A`** (new baton) except one **`D`** — `82e51e1c`, which removes
`kc2-baton-v1-…-pm4-i15-camp-defoff-critlo-20260814_103459.json` on its own commit with its reason
(`D-I15-6`, an unreported I-15 baton). That file is not among the twenty pins. **No frozen
substrate path was modified by any run commit.**

---

## 7 — WALL 6 · EXPORT UNTOUCHED — **PASS-WITH-NOTE**

### 7.1 As claimed, I-19 → I-21: PASS

Git confirms **zero** `src/reincarnated/export/` touches in `654ec016..8fa25100` (I-19),
`975eaa72` (P-DEF), `280f3c9d..42f090e4` (I-20), and `35d046c4..ec42a11a` (I-21).

### 7.2 `D-PDEF-1` — flagged, routed, and verifiably NOT repaired: PASS

`defenses_enabled` survives intact — **26 occurrences** in `export/kc2_run_adapter.py`, including
the live selector the refusal turns on:

```python
# src/reincarnated/export/kc2_run_adapter.py:2720
    if spec.defenses_enabled:
```

The I-20 artifact records the reasoning with the governance citation: *"Deleting it breaks
`export/`, which ADR-004 puts behind a MIGRATION and star-lord's sign-off."* Landed instead: a
Discipline-#12 quote of the dead signature, a per-wave `defence_wiring` census, and a removal
proposal filed in MIGRATION for star-lord. I-21's MIGRATION § 3 re-states it as still open and
still star-lord's. **This is NOTE-9 and ADR-004 executed correctly.**

### 7.3 The note — the wall is narrower than "no run commit modified export/"

I must correct the wall as it was handed to me. `export/` **was** modified during the run, by
gamora, in a seam gamora does not own:

| commit | iteration | file | size |
|---|---|---|---|
| `e446d731` | I-15 | `export/kc2_run_adapter.py` | +107 |
| `8b6431d8` | I-15 | `export/kc2_run_adapter.py` | ±6 |
| `276f5c13` | I-16 | `export/kc2_run_adapter.py` | +119/−1 |
| `0f57b646` | I-16 | `export/kc2_run_adapter.py` | ±3 |
| `6199fc6e` | I-17 | `export/kc2_run_adapter.py` | +163 |
| `2052f145` | I-18 | `export/kc2_run_adapter.py` | +199 |

These are baton adapter specs. **This is disclosed, not concealed:** L-38 flags it and
`R-PM4-47 part 4` routes it — *"`export/MIGRATION.md` I-12..I-17 gap → knight-rider's queue (run
does not backfill another seam's migration ledger)"* — and it is carried in `R-PM4-54 part 5`'s
star-lord flag list. The right disposition already exists; my note is only that the wall's stated
scope should read **"`export/` untouched from I-19 onward, with the I-15…I-18 adapter-spec edits
and their MIGRATION gap carried as a routed star-lord debt."** Reporting it as a run-wide
untouched claim would overstate.

---

## 8 — WALL 7 · NO REPAIR OF OTHERS' ARTIFACTS (NOTE-9) — **PASS**

**The decisive check.** `agentic_orchestration/legolas/notes/2026-08-14-kc2-pm4-lap-t-arrival-decode/`
has **exactly one commit in its entire history** — `de9de38e`, the landing — and has never been
modified since, despite Lap U convicting Lap T's reader (`D-U-2`) and I-20 convicting its CSV
(`D-I20-1`). The `pm4t_map_placements_v2.csv` bytes that were proven displaced are still on disk,
unpatched. **The ledger amended; the record stood.**

`D-I20-1` was repaired **by legolas, in legolas's own seam**, as new artifacts —
`pm4u_map_placements_v3.csv` and `pm4u_geometry_v3.csv` in Lap U's directory, with `v2_dbr`
retained for audit. Gamora consumed v3 as a **control** and re-measured agreement rather than
sampling it, refusing the commissioned use by name.

Other NOTE-9 instances verified: `D-PDEF-1` refused in star-lord's seam (§ 7.2); `D-I19-7`
framed and not repaired; `D-I21-1` (the sim player traverses where the referent mills) filed
against gamora's own seam with Lap U's number as its falsifier and **routed, not repaired**, on the
stated ground that the repair is not decoded.

---

## 9 — WALL 8 · PRE-REGISTRATION — **PASS**

### 9.1 Lap U

`PREREGISTRATION.md` digest **`7a250772bad3bf8cbce2e43455bc3e4dae2fee677aeedc1ffad978f3dda6b144`** —
recomputed by me, EXACT against L-44, against `pm4u_digests.json`, and against gamora's independent
re-hash in the I-21 artifact. `pm4u_digests.json` records `preregistration_hashed_utc:
2026-08-14T18:03:05Z`; every instrument output carries a later mtime (14:08–14:31 local). § 0
declares the reconnaissance preceding the hash **in full**, including the honest admission that one
limb's headline was already observed.

**The strongest evidence is behavioural, not chronological:** the pre-registered `V-a1` follow-test
fired **NOT SUPPORTED at n=0** against the lap's own primary limb, and the lap reported it as
starvation rather than refutation and let the binary carry the verdict. A post-hoc author does not
write that outcome.

### 9.2 I-21 `S-3` — git-attested

`S-3` is present in `35d046c4` (math note alone, zero code), fifteen minutes before the fold
`ec42a11a` and the findings artifact:

> **PREDICTION:** `ALL_ARMS_ZERO_REACH == True` on **every** arm … **FALSIFIER / AUTOMATIC
> CONSEQUENCE:** any arm reports a non-unit CONSUMED multiplier ⇒ **the defence axis returns inside
> this iteration, `defon/defoff × px` = 4 arms, no discretion**

This predicts the **non**-fire against `R-PM4-53 part 3c`'s stated expectation, names the mechanism
rather than only the outcome, and — critically — **the automatic consequence is wired in the
driver** (lines 727–749 construct and run the four extra arms if `all_zero` is false). Measured
result: produced-not-1 = 6, **CONSUMED non-unit = 0**, `ALL_ARMS_ZERO_REACH = true`,
`TRIPWIRE_FIRED = false`. A tripwire that would have acted, and reported that it did not need to.

### 9.3 Structural note (INFO)

**Every legolas lap N–U lands in a single commit.** Prereg priority is therefore self-attested
(recorded hash instant + mtimes + falsifier outcomes), not git-attested. The engine side has the
stronger form — note-alone commits give git-order proof. Laps could adopt it at negligible cost by
committing `PREREGISTRATION.md` alone before running instruments. Not a breach; a cheap hardening.

---

## 10 — WALL 9 · LEDGER CONSISTENCY — **BLOCK**

### 10.1 What holds

Every adoption row L-39…L-45 carries an explicit CL-10 claim naming the artifact keys read.
`R-PM4-29`'s basis discipline is honored where it is hardest: `D-I20-2` corrects `R-PM4-51 part 3`'s
*stated basis* while confirming its verdict, and `R-PM4-53 part 2` banks the F-12 correction-of-a-
correction (0.36 → 10.47 → 0.6089 m) **with its basis**, explicitly recording that `D-T-2` was
computed on labels its own lap's reader had displaced. Bracket resolutions (`U-P-N-1`, `U-S-2`,
`U-T-1`) each cite `R-PM4-27 part 3` and each resolved against the better-grading arm. This is the
discipline working.

### 10.2 **BLOCK — the headline claim is contradicted by the run's own artifacts**

L-45: *"the first record-cell T2 hit of the run **(best-ever prior: nothing in band)**."*
`R-PM4-54 part 3` and landing-note § 11.1 ("best EVER on a record cell … **I-21**") carry it forward.

Read from `kc2-pm4-i18-findings-20260814_105832.json`, `⚑ T_scorecard`:

| I-18 cell | death wave | `T2.met` | ratio | l4l (s) |
|---|---|---|---|---|
| `cluster_defon__critlo__COUPLED__PX-HI` | 156 | **true** | **0.8502** | **155.3469** |
| `cluster_defon__critlo__DECOUPLED__PX-LO` | 156 | true | 0.9047 | 165.3061 |
| `cluster_defon__critlo__DECOUPLED__PX-HI` | 156 | true | 0.8511 | 155.5102 |

The T2 band is `[155.309195, 210.124205]`. **155.3469 is inside it.** The first row is the
**reference configuration** (`cluster_defon`) on the **COUPLED** arm — the family `R-PM4-48`
subsequently ruled TRUE, so it cannot be excluded as a regraded continuity control the way the
DECOUPLED rows can. L-41 re-verified that exact l4l to seventeen digits at P-DEF, after I-19.

And the run already knew. Gamora's I-19 landing note, § 1.2, line 71:

> I-18's `COU·PX-HI` held **T2 and T4a together** (0.9123). **No I-19 arm holds both.**

**Why this is a BLOCK and not a WARN.** It is not a measurement error — 0.8815 is correct and I
verified it. It is a **superlative in the sentence that carries the run to Matt**, and it is false
against the run's own committed artifacts and its own prior landing note. `R-PM4-54 part 3` rests
the convergence assessment partly on it. It is precisely the `D-I20-5` lesson the run banked one
iteration earlier — *a continuity check must pin to the artifact, not the sentence about it* —
applied to everything except this claim.

**The path forward is one paragraph, and the corrected claim is still strong:** I-21's 0.8815 is
the **best COUPLED record-cell T2 ratio of the run** (|1−0.8815| = 0.1185 against I-18's
|1−0.8502| = 0.1498) and **the first T2 hit since the I-19 and I-20 regressions**, achieved with a
board that is decode-truer in four respects than the board I-18 ran. Say that, and nothing is lost
but the word "first."

### 10.3 **WARN — a T4a value cited as a T2 comparison**

`R-PM4-49 part 3`: *"the best COUPLED cell is COU·PX-LO·RING … ratio 0.7658 — a REGRESSION from
I-18's COU·PX-HI **0.9123**."* The subject is a T2 ratio; **0.9123 is I-18's T4a.** I-18's
`COU·PX-HI` T2 ratio is 0.8502. The string `0.9123` appears in no I-18 or I-19 findings artifact as
a T2 quantity. The I-19 landing note uses it correctly; the ledger compressed two quantities into
one number. The regression direction is unaffected (0.7658 < 0.8502); the cited magnitude is wrong.

### 10.4 **WARN — 19 of 107 truncated digests in the ledger have incorrect tails**

I extracted every `` `<head>…<tail>` `` digest reference from the ledger (110 refs, 107 resolvable)
and matched each against a 37,645-file digest index across both repos. **All heads resolve
correctly to real artifacts. Nineteen printed tails do not match the file's actual tail.** Examples:

| ledger prints | actual digest | artifact |
|---|---|---|
| `f1a34cb1…2bce` | `f1a34cb1…75fbec6ce` | `pm4u_findings.md` (L-44) |
| `d1441874…f3a7` | `d1441874…80f6a3a7` | I-20 landing note (L-43) |
| `da62709f…7d77` | `da62709f…c07dfa77` | Lap Q `PREREGISTRATION.md` (L-39) |
| `075b31c0…2fbc` | `075b31c0…b5d02bfc` | `pm4o_digests.json` |
| `941976fc…77dba` | `941976fc…6077dbda` | I-12 camp baton |

The failures look like transcription noise — transpositions and one-character shifts — and they are
**confined to ledger prose**. Every *machine* pin I checked is correct at full 64 hex
(`I20_FINDINGS_SHA`, `⚑ lap_u_digests`, `⚑ lap_t_digests`, each lap's `pm4*_digests.json`). **No
verification in this run was performed against a mis-transcribed value, and no adopted finding
rests on one.** But the ledger is the run's constitution and its printed digests are its audit
handles; a reader auditing from the ledger gets nineteen spurious mismatches. The run's own I-4
lesson applies — *a prefix compare is a check that looks like a check* — and here even the
head-plus-tail form fails. **Recommendation: print full 64 hex in the ledger, or drop the tails and
point at the lap's `digests.json`.**

### 10.5 INFO — the numbered assert-wall was discontinued after I-18 without a stated retirement

I-17 and I-18 each carry a 26-check `assert_wall` with `n_green` / `n_red` and a `keys_asserted`
list per check — the mechanism that discharges `R-PM4-37 part 6` / `D-I14-4` (*"check-instrument
key-existence now a **standing wall obligation**"*), itself minted in response to my I-9…I-12
wall-of-walls audit. **I-19, I-20 and I-21 findings carry no `assert_wall` key at all**, and their
math notes do not mention one. I found no ruling retiring it.

I record this as INFO rather than WARN because **no verification was actually lost**: the
underlying wall quantities moved onto the artifact as raw data and the conductor read them from the
emitted JSON at CL-10 — which is arguably the better pattern and close to my own W-3 recommendation
(*a check that asserts nothing is a report*). The defect is that a change to the verification
apparatus went undeclared, which is the class `R-PM4-37 part 6` exists to prevent. Either re-arm it
or retire it on the record.

---

## 11 — WALL 10 · HYGIENE — **PASS**

Verified in the correct order. Math note § 9, **committed at `35d046c4`** (note alone, before the
fold), banks all three digests *and their byte counts*:

| file | sha256 | bytes |
|---|---|---|
| `kc2-pm4-i20-findings-20260814_173814.json` | `c7e6a41438689f3647987b95ac6245ed6c17d97de864d48fe4957fe89a858402` | 735,256 |
| `kc2-pm4-i20-findings-20260814_174031.json` | `f578ee2028b97e6b18b8971a8acf9fb0e5b0b2ae3e000039ab43880cdee597bc` | 737,249 |
| `kc2-pm4-i20-findings-probe-20260814_173233.json` | `1134059986976bed2363ce41e72245200cacd354be7a1db6f479f88163afe665` | 722,963 |

I confirmed all three are absent from `src/reincarnated/simulation/output/`, and that the record
artifact `…174154.json` is retained and digest-verified. The three were **classified by
measurement** — structurally identical to the record artifact but missing `⚑ P10_march_base_ast_census`,
i.e. pre-`D-I20-6`-repair builds — not assumed superseded. The reasoning is `D-I20-1` turned on its
author: *"a look-alike in a consumed directory is a consumer trap … committing them by name would
preserve the trap under a nicer label."* Correct, and correctly sequenced.

**INFO:** the same shape survives at I-18, where **two** findings files remain committed —
`…105605.json` and `…105832.json`. L-36 declares the first as the `D-I18-7` per-wave experiment
rather than a second determinism pass, so it is disclosed; but a downstream reader globbing
`kc2-pm4-i18-findings-*.json` still finds two files distinguished only by ledger prose. Recommend
the same disposition applied to I-20.

---

## 12 — SMOKE GATE (REVIEW_PROCESS #2, Discipline #2) — **VERIFIED**

The I-21 commit claims *"Smoke 296 passed / 1 pre-existing failure (test_AC_10_10_…,
secondary_streams.py:136) unchanged since I-18."* **I ran it.**

```
FAILED tests/test_kc2_locomotion.py::test_AC_10_10_the_literal_30_0_appears_NOWHERE_in_the_arena_surface
E   Failed: bare 30.0 survives in secondary_streams.py:136
1 failed, 296 passed, 10270 deselected in 44.94s
```

Count, test name and source line all reproduce exactly. This is a claim verified to the digit.

---

## 13 — N-1 · FINDING OUTSIDE THE TEN WALLS — **WARN**

**The engine's production default still carries the limb I-21 ruled decode-false.**

```python
# src/reincarnated/simulation/kc2/run.py:365
    limb: MotionLimb = MotionLimb.ZONE_FIRST,
# src/reincarnated/simulation/kc2/calibration.py:1455
    "motion_limb_default": MotionLimb.ZONE_FIRST.value,
```

`R-PM4-54 part 1` adopts I-21 and characterises the `C-1` removal as *"a STRUCTURAL CORRECTION with
its decode cited."* But the correction is applied by the **driver** passing `GATE_FIRST` to an
existing parameter; `ZONE_FIRST` (L-A) remains what any other caller of `simulate_wave` or
`calibration.t1_table` receives. MIGRATION § 2 discloses the *value* shift on folded runs and
retires four downstream beliefs with numbers — good Discipline-#12 work — but does not name the
unmoved default, and it appears nowhere in `R-PM4-54 part 5`'s carried list.

**Not a breach, and not something the run should have done:** moving a shared default mid-run is
exactly the cross-seam scope creep `R-PM4-29` and ADR-004 exist to prevent, and deferring it was
right. But the HALT brief is where the deferral gets named, and right now it is not named. **This
belongs in the debt disposition:** *the pursuit decode is adopted for the run's record cells; the
engine's standing default is unchanged and still carries the reading the decode contradicts.*

---

## 14 — CARRIED DEBTS I OWN (status at the ramp)

The five-entry decisions-log package routed to me via KR — **D-I15-2** (arrival-time semantics) ·
**D-I16-1** · **D-I17-1** (ADCTH basis semantics, Discipline #12 shift) · **D-I18-5** · **D-I18-6** —
is **not yet written** to `design/decisions/decisions-log.md` (last entry: 2026-08-08, Discipline
#72). This is correct and expected: `R-PM4-42 part 6` and `R-PM4-46` scheduled them as an
*end-of-run* package. The ramp is the trigger. I will draft them on routing; per ADR-002 they are
mine to write, and any that constitutes an architectural commitment goes to Matt.

---

## 15 — ACTION

- [ ] **BLOCK · gandalf (conductor), before the HALT brief leaves):** correct L-45 / `R-PM4-54 part 3` / landing-note § 11.1. Replace *"the run's first record-cell T2 hit (best-ever prior: nothing in band)"* with the true and equally strong claim: **best COUPLED record-cell T2 ratio of the run, and the first hit since the I-19/I-20 regressions**; record I-18 `cluster_defon__critlo__COUPLED__PX-HI` (0.8502 / l4l 155.3469 / wave 156) as the prior in-band record cell, citing gamora's own I-19 landing note § 1.2. (§ 10.2)
- [ ] **WARN · gandalf:** correct `R-PM4-49 part 3` — 0.9123 is I-18's **T4a**, not its T2 ratio (0.8502). Carry the basis, per `R-PM4-29`. (§ 10.3)
- [ ] **WARN · gandalf:** disposition the 19 mis-transcribed digest tails. Preferred: print full 64 hex in the ledger going forward and append a corrections row rather than silently editing history. (§ 10.4)
- [ ] **WARN · gamora + gandalf:** add N-1 to the HALT brief's debt disposition — the engine's `MotionLimb` default remains `ZONE_FIRST` while the run adopted `GATE_FIRST`. (§ 13)
- [ ] **INFO · gamora:** re-arm the numbered `assert_wall` with `keys_asserted`, or retire it on the record with a ruling. It is currently discontinued without either. (§ 10.5)
- [ ] **INFO · gamora:** apply the I-20 look-alike disposition to the two committed I-18 findings files. (§ 11)
- [ ] **INFO · legolas:** commit `PREREGISTRATION.md` in its own commit before running instruments, so prereg priority becomes git-attested rather than self-attested. (§ 9.3)
- [ ] **INFO · knight-rider:** the `export/MIGRATION.md` I-12…I-17 gap and the S-* `KC2RunSpec` registration flags remain on your queue per `R-PM4-47 part 4`; they survive the run. (§ 7.3)
- [ ] **jack-ryan (me):** draft the five-entry decisions-log package on KR routing. (§ 14)
- [ ] **Matt:** no decision is required *by this audit* except acceptance of the corrected headline. Nine walls pass; the BLOCK is on wording, not on work.

---

## 16 — REFERENCES

**Ledger / rulings**
`/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/gandalf/notes/2026-08-13-kc2-pm4-replication-run-charter.md` (L-0…L-45, R-PM4-1…54)

**Engine artifacts (all digests recomputed by me)**
`/Users/admin/Games/reincarnated-engine/src/reincarnated/simulation/output/kc2-pm4-i21-findings-20260814_190920.json`
`/Users/admin/Games/reincarnated-engine/src/reincarnated/simulation/output/kc2-pm4-i20-findings-20260814_174154.json`
`/Users/admin/Games/reincarnated-engine/src/reincarnated/simulation/output/kc2-pm4-i19-findings-20260814_162041.json`
`/Users/admin/Games/reincarnated-engine/src/reincarnated/simulation/output/kc2-pm4-i18-findings-20260814_105832.json`
`/Users/admin/Games/reincarnated-engine/src/reincarnated/simulation/output/kc2-pm4-i18-findings-20260814_105605.json`
`/Users/admin/Games/reincarnated-engine/src/reincarnated/simulation/output/kc2-pm4-i17-findings-20260814_085045.json`
`/Users/admin/Games/reincarnated-engine/src/reincarnated/simulation/output/kc2-pm4-pdef-findings-20260814_165633.json`

**Engine source**
`/Users/admin/Games/reincarnated-engine/src/reincarnated/simulation/kc2/pursuit.py`
`/Users/admin/Games/reincarnated-engine/src/reincarnated/simulation/kc2/run.py` (line 365 — N-1)
`/Users/admin/Games/reincarnated-engine/src/reincarnated/simulation/kc2/calibration.py` (line 1455 — N-1)
`/Users/admin/Games/reincarnated-engine/src/reincarnated/simulation/scripts/gamora_kc2_pm4_i21_pursuit_fold_2026_08_14.py` (lines 713–722 determinism; 727–749 tripwire; 753–769 fold-off)
`/Users/admin/Games/reincarnated-engine/src/reincarnated/simulation/scripts/gamora_kc2_pm4_i4_match_and_fold_2026_08_13.py` (`FROZEN`, `verify_frozen`)
`/Users/admin/Games/reincarnated-engine/src/reincarnated/export/kc2_run_adapter.py` (line 2720 — D-PDEF-1 unrepaired)
`/Users/admin/Games/reincarnated-engine/src/reincarnated/simulation/MIGRATION.md`
`/Users/admin/Games/reincarnated-engine/tests/test_kc2_locomotion.py` (line 117 — the pre-existing failure)

**Math notes (git-order evidence)**
`/Users/admin/Games/reincarnated-engine/src/reincarnated/simulation/math/kc2-pm4-i21-pursuit-fold-2026-08-14.md` (§ 7 `S-3`, § 9 hygiene)
`/Users/admin/Games/reincarnated-engine/src/reincarnated/simulation/math/kc2-pm4-i21-pursuit-fold-ADDENDUM-2026-08-14.md`
`/Users/admin/Games/reincarnated-engine/src/reincarnated/simulation/math/kc2-pm4-i20-arrival-fold-2026-08-14.md`
`/Users/admin/Games/reincarnated-engine/src/reincarnated/simulation/math/kc2-pm4-i19-structure-fold-2026-08-14.md`

**Meta artifacts**
`/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/gamora/notes/2026-08-14-kc2-pm4-i21-pursuit-fold-landing.md` (§ 11.1 — the BLOCK)
`/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/gamora/notes/2026-08-14-kc2-pm4-i19-structure-fold-landing.md` (§ 1.2 line 71 — the contradicting record)
`/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/gamora/notes/2026-08-14-kc2-pm4-i20-arrival-fold-landing.md`
`/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/legolas/notes/2026-08-14-kc2-pm4-lap-u-ramp-decode/` (PREREGISTRATION.md, pm4u_digests.json, v3 CSVs)
`/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/legolas/notes/2026-08-14-kc2-pm4-lap-t-arrival-decode/` (one commit, never modified)
`/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/jack-ryan/notes/2026-08-14-kc2-pm4-wall-of-walls-audit.md` (the I-9…I-12 predecessor audit)

*Audit by jack-ryan, 2026-08-14. Read-only. Nine walls PASS, one BLOCK on the HALT brief's headline.*
