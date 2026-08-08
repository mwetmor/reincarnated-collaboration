# Finding — 2026-08-08 — KC2-SIM Gate-2 **Phase-D2**

**Reviewer:** jack-ryan (DEV-MODE, BLOCK authority live)
**Severity (overall):** **BLOCK ×1** (limb 6) · PASS-with-findings ×4 · PASS ×1
**Targets:** engine `13451fdf` (gamora beat-3) · `a53c97fc` + `248f8738` (star-lord trio) ·
meta `75b27f65` / `d580e5fd` (reports) · spec + ledger **working copy** (uncommitted per charter § 4.7)
**Developers:** gamora · star-lord · gandalf `RUN-CONDUCTOR`
**Authority for this review:** desirable-run-pattern standing safety #2 — independent Gate-2 on
in-run reclassifications; the conductor may not self-clear. gamora's own report § 12 flags
*"Gate-2 REQUIRED and NOT self-cleared."*
**Principles applied:** REVIEW_PROCESS #1 (math-before-code) · #2 (smoke-gate) · #3 (cross-seam
impact) · #4 (decisions-log as truth) · #5 (severity matters). Disciplines **#1, #2, #3, #10, #12**.
ADR-002 (tiered approval) · ADR-004 (cross-seam MIGRATION) · ADR-006 (read-only external systems).

---

## 0 — Verdict table

| # | Limb | Verdict | Findings |
|---|---|---|---|
| 1 | gamora beat-3 substance | **PASS-with-findings** | D2-2 · D2-3 · D2-9 · D2-14 · D2-15 |
| 2 | Conductor dispositions L-43(c) (C-1..C-5 + pause) | **PASS-with-findings** | D2-4 · D2-5 · D2-11 |
| 3 | star-lord trio (S-W2 / S-I1 / CD-2) | **PASS-with-findings** | D2-6 · D2-7 · D2-13 |
| 4 | F-11 registration | **PASS-with-findings** | D2-8 |
| 5 | Test-count reconciliation (D-I1 class) | **PASS** | D2-10 |
| 6 | Conductor five-edit spec volley | **BLOCK** | **D2-1** · D2-12 |

**One BLOCK.** It is narrow, cheap to clear, and does **not** gate the locomotion lap, the legolas
citation probe, or the galadriel fourth extraction. It gates the **Phase-E emit** and the star-lord
`_ac_11_4g` rider.

**Everything I could re-measure, I re-measured on my own instruments rather than reading the
reports.** Reproductions are listed in § 7.

---

## 1 — Limb 1: gamora beat-3 substance — **PASS-with-findings**

### 1.1 (a) The negative control — refusal-to-fit as measurement: **SOUND, and the fit is quarantined**

The move is legitimate and the strongest thing in the beat. Fitting a declared free parameter to a
pinned target is forbidden by charter § 4.2; running the fit as a **negative control** converts the
refusal from an argument into a measurement, which is exactly the pattern Discipline #10 asks for
(empirical inspection over assumption). It also pre-empts the obvious reviewer objection ("you
didn't try the licensed calibration") by having tried it and shown it buys nothing structural.

**Quarantine — CLEAN, verified four ways:**

- `fixture.py:253` `V_REF_M_PER_S = Cited(4.0, …)` — **unchanged**; the fitted value never touches
  a module constant.
- The fitted `10.5` appears in the engine only as (i) an element of `vref_sensitivity`'s default
  sweep tuple, (ii) prose in docstrings, and (iii) an unrelated `ARENA_S2` o'clock bearing. No
  production path consumes it.
- Every sweep row carries `is_negative_control: True` **plus** the
  `VREF_SENSITIVITY_IS_A_NEGATIVE_CONTROL` string, so a row cannot be lifted out and called
  calibrated.
- `micro_oracles.py:226` passes `float(v(V_REF_M_PER_S))` **explicitly** rather than relying on the
  default — MO-5 cannot silently inherit an overridden speed.

The one thing that would break the quarantine (a test asserting the fitted value as a PASS) does not
exist: `test_D1_fitting_v_ref_buys_the_MEAN_and_NOTHING_ELSE` asserts the fit **still fails**.

→ but see **D2-2**: the published numbers of the control do not reproduce as a coherent set.

### 1.2 (b) The lower-bound argument — **ARITHMETIC EXACT, and I confirmed the assumption it rests on**

Reproduced on my own instrument, bit-for-bit: FALSIFIED **89**, CONSISTENT **3** = `[80, 90, 92]`.
I additionally verified something neither the note nor the ledger states: **FALSIFIED ≡ OVER as
sets** (89 = 89, set-equal). That is a consistency check worth having, because the two are computed
by different predicates — `OVER` on `sim_mean`, `FALSIFIED` on `sim_min`. `min ≤ mean`, so
FALSIFIED ⊆ OVER necessarily; equal cardinality forces set equality. The sign argument therefore
uses the **strictly conservative** statistic (most-favourable seed) and still falsifies the same 89.
That is the right direction and it is not stated as such anywhere.

The three survivors are correctly identified. Their *characterisation* is not — see **D2-3**.

### 1.3 (c) The mechanism diagnosis — **VERIFIED AGAINST THE CODE**

The static-board claim is exactly true, at three sites in `run.py`:

- `:319` — `actors=[(aid, (a["spawn_x"], a["spawn_y"])) for aid, a in actors.items() if a["alive"]]`
  is handed to `disc.resolve_tick` **every tick**.
- `:287–288` — the player's target is chosen by distance to `spawn_x/spawn_y`, and only `px, py`
  are advanced (`:300–301`).
- Nowhere in the module is `a["spawn_x"]` or `a["spawn_y"]` ever assigned after spawn. **Actors hold
  spawn coordinates forever. CONFIRMED.**

I also verified the companion claim that makes the kill term identically zero: with `hp_lookup=None`,
`:253` sets `hp = 0.0`; at `:332` `applied = min(per_tick_damage, 0.0) = 0.0`; `:345` then reads
`hp <= 0.0` and kills the body on the **first** tick of coverage. `kill_time_s = 0.0` is a real
structural zero, not a modelling shortcut. **CONFIRMED.**

§ C.3's tour-length table reproduces **all six rows exactly** (2.49× / 3.01× / 4.07× / 4.90× / 0.92× /
5.12×).

---

## 2 — Limb 2: conductor dispositions (L-43(c)) — **PASS-with-findings**

**T-1 UNCHANGED — correct, and the most important call in the fold.** A pre-registered BINDING gate
failed and the conductor processed it as a finding rather than re-forming the predicate. That is
standing safety #1 operating exactly as designed. I want it on the record that this is the
disposition a run under pressure gets wrong, and it was got right.

**C-1 ADOPT (per-record eHP emission) — sound.** Note the non-obvious coherence: the lower-bound
argument says eHP *cannot rescue* T-1 on 89/92, and C-1 commissions eHP anyway. Those are not in
tension — eHP is needed for the model to be *right*, not to make the gate *pass*. Adopting it while
holding that it will not rescue the gate is the honest ordering.

**C-2 ADOPT (v_ref calibration suspended) — sound.** The licence's precondition (a kill term that
separates traversal from clear time) demonstrably does not hold; § 13's strike carries lineage.

**C-3 ADOPT (locomotion; v_mob DB-CITED only) — sound in substance.** The degeneracy claim is
overstated — see **D2-11**.

**C-4 ADOPT (6-emitter completion + F-12a + MO-5 provisional) — sound, and F-12a is well-founded.**
I verified F-12a's citation: spec `:1089` reads *"(`arena_id` + the six bearings + player spawn)"* —
**no radial coordinate**, exactly as claimed. I also verified the MO-5 re-grade against the code:
`micro_oracles.py:216–225` `observe_cycle_floor_s()` calls `cycle_time(emitter_distance_m =
ARENA_S2.emitter_radius_m, …)` — the PASS **does** consume the uncited 30.0 m default. The
annotation claims only what the evidence supports. → but see **D2-12** for a C-4 execution hazard.

**C-5 PARKED-REGISTERED — the parking is SOUND, and I can now prove it costs nothing.** See **D2-4**.

**Beats 4–5 PAUSED — target-state check PASSES; the rationale does not.** See **D2-5**.

---

## 3 — Limb 3: star-lord trio — **PASS-with-findings**

**S-W2 golden-pin chain — INTACT, and live-verified.** spec § 9.5 → `goldens/*.value.txt` +
`*.provenance.json` → `DEVOTION_ENVELOPE_DISCLOSURE` → wire. Three always-running tests plus the
cross-repo re-extraction. On this host the cross-repo test **runs** (does not skip) and passed in my
own `51 passed` run — which independently establishes that the § 9.5 block survived the L-41
seventeen-edit and L-43 five-edit volleys **byte-unchanged**. That is a free confirmation of the
conductor's historical-vs-operative discipline on one section, obtained from star-lord's chain.

**S-I1 AST-scan extension — 5/5 with a firing positive control.** The scope self-assert (scanned set
compared against `baton_v1_*.py` discovered on disk) is the actual fix, and it is the right one: a
sixth module joining the surface fails the test instead of silently re-narrowing the guard.

**CD-2 — implemented as ruled, not reinterpreted.** Implementing `code-surface-v1` literally (path
prefix, not a judgement about importability) and erring toward `dirty` is the correct posture for a
provenance claim. The entries-vs-files discovery — caught by a scratch-repo test, field renamed
before shipping — is Discipline #10 working.

**The sanctioned coupling claim — VERIFIED EXACTLY AS CLAIMED.** `tests/test_baton_v1.py:204` is the
**only** import of `simulation.kc2` anywhere in the baton surface, it is inside one test, it is
read-only, and it reaches `devotion` alone. **No `baton_v1_*` module imports anything from
`simulation.kc2`.** `count_model_provenance()` is not consumed anywhere in `export/`. **Zero exposure
to `p06_state` via that surface — confirmed.**

*(The p06 exposure that does exist arrives by a completely different route — the export seam's own
schema default. That is D2-1, and it is not a defect in star-lord's coupling discipline.)*

**CD-2 § 11.4 transcription fidelity — two drifts.** See **D2-6** and **D2-7**.

---

## 4 — Limb 4: F-11 registration — **PASS-with-findings**

**The framing is measurement-clean and the interim is right.** My independent porcelain census
reproduces the conductor's **exactly**: `2,414 / 2,404 / 10`, and the ten non-output entries match
his enumeration **item-for-item** (1 export delta note · 2 generation notes · 2 simulation math notes
· 2 simulation scripts · 1 telemetry backup · 2 telemetry-seed WAL/shm). Star-lord's `2,403 / 2,393`
differs by the same +11 and yields the same 10 — the two measurements are consistent, and attributing
the delta to gamora's beat-3 writing artifacts between readings is correct. Entries-not-files is
correctly named. `v1 STANDS until Matt rules` is the right interim.

**No code change was smuggled in.** I diffed `248f8738`: it edits a **docstring only**, correcting a
claim that contradicted the same commit's own measurement. Behaviour is untouched. That is a
correction toward the evidence, which is the direction you want.

One framing overstatement, and one materially decision-relevant omission — see **D2-8**.

---

## 5 — Limb 5: test-count reconciliation — **PASS**

Fully reconciled with no conflict. See **D2-10** for the authoritative counts and for the origin of
the disputed figure.

---

## 6 — Limb 6: the conductor's five-edit spec volley — **BLOCK**

Four of the five edits are byte-clean and I verified each in place:

| edit | verdict |
|---|---|
| § 11.4 CD-2 fields (`:1542–1550`) | **CLEAN** as text; two semantic drifts vs implementation → D2-6/D2-7 |
| § 12 MO-5 provisional-on-geometry (`:2060`) | **CLEAN** — verified against `micro_oracles.py:225`; claims only what the code does; the measured pin correctly left standing |
| § 13 HALT-2 C-2 suspension (`:2086`) | **CLEAN** — strike `~~calibrated at D against traversal times~~` carries lineage, ledger row, and the reason; original disposition preserved as struck text |
| § 14 F-11 + F-12 blocks | **CLEAN** as registrations; content findings D2-2/D2-3/D2-8/D2-11 |
| § 11.4 `fixture_p06_state: true → false` (`:1557`) | **INCOMPLETE — see D2-1** |

Historical-vs-operative discrimination held everywhere I checked: every deletion in the working diff
is a replacement-in-place whose successor carries a strike plus lineage (`:1033` is the reference
form: `~~RESOLVED: p06 is ON (L-21)~~ → DEMOTED-OPEN (L-33(g)) → RULED OFF …`). No dated RECORD text
was amputated.

---

# FINDINGS

## D2-1 — **BLOCK** — the superseded p06-ON claim is live at three more spec addresses **and is the default value in the cross-seam schema**

### What I found

L-43(f) states the `fixture_p06_state` sweep-set gap was *"fixed at this fold."* **That claim is
false of the text.** The fix landed at **one** address. Three more survive, all operative (present
tense, no strike, no date, no lineage):

| addr | text | spelling |
|---|---|---|
| `:1714` § 11.4 item 12 | *"the fixture side is now MEASURED. `fixture_p06_state: true` records the L-21 census result … the 5th body **is** the p06 hero slot"* | "L-21 census" |
| `:1991` M-1 disposition row | *"**ADOPTED** — fixture side now `true`, MEASURED (L-21)"* | "MEASURED (L-21)" |
| `:2102` § 13 Declared-not-HALT | *"(Former members CLOSED and struck: … U9-6 → measured ON L-21.)"* | "measured ON" |

`:1714` does not merely assert the wrong value — it restates the **evidentiary leg L-33(g) STRUCK**
("the 5th body *is* the p06 hero slot") as live, at a spec address whose own `:1191` row already
carries the strike.

**Two of the three are inside the conductor's own declared spelling set** ({p06 = ON · MEASURED ON ·
RESOLVED-ON · L-21 census}). So the L-43(f) diagnosis — "sweep sets must enumerate all historical
spellings" — is not the operative failure. **The set was right; the sweep was not run.** The fix was
executed as a single-address edit where a grep over the declared set was owed. That is the *identical*
failure mode the conductor diagnosed and adopted verbatim at L-40(d) (D-W3, "address-list editing
where a value-set grep was owed, Discipline #2"), now on its third consecutive fold.

### Why this is a BLOCK and not another WARN

Because it is not confined to prose. The same superseded claim is the **live default in the export
schema that binds before the Phase-E emit**, and the guards make the superseded state the
self-consistent one:

```
src/reincarnated/export/baton_v1_schema.py:392-393
    # [M-1] the fixture side is MEASURED provenance; the run side is what THIS run did.
    fixture_p06_state: bool = True
```

```
src/reincarnated/export/baton_v1_schema.py:694    u9_bonus_spawn_state: str = "RESOLVED"

src/reincarnated/export/baton_v1_validator.py:228  expected = "RESOLVED" if fixture is True else "UNKNOWN"
```

- The schema comment cites `[M-1]` and calls the fixture side *"MEASURED provenance"* — transcribed
  from the two stale spec sites above.
- `baton_v1_fixture.py:357–362` sets `run_p06_enabled` but **not** `fixture_p06_state`, so it takes
  the default `True`.
- The default pair `(u9_bonus_spawn_state="RESOLVED", fixture_p06_state=True)` **passes AC-11.4g**.
  The struck claim is the state the emitter reaches by doing nothing, and every guard agrees with it.
- `tests/test_baton_v1.py:448` currently uses `fixture_p06_state = False` — the **ruled-correct**
  value — as its *disagreement* case.

Meanwhile the simulation that would produce the baton runs `calibration.py:224
S1_BONUS_SPAWNS_ENABLED = False`, and the count model of record is **p06-OFF, 271.50 / 63.00**. A
Phase-E baton emitted today would carry a provenance field contradicting the run it describes, and
nothing in the pipeline would object.

**The type-gap framing understates this.** The queued rider (bool + `_ac_11_4g`'s RESOLVED/UNKNOWN
mapping cannot express RULED-OFF) is real but *secondary*. The **value** is wrong today and is
correctable today, with no type change, by defaulting to `False` / `"UNKNOWN"`. Conflating the two
risks the value correction being deferred as a schema-design item past the emit it must precede.

### Rationale

Conflicts with two locked rulings — **L-37(b)** (p06 RULED OFF, MEASURED-NULL, positive-controlled)
and **L-33(g)** (the L-21 census leg STRUCK). Review Principle **#4** (decisions-log as truth) and
**#3** (cross-seam impact). Discipline **#2** (right tool for the validation question — a value-set
grep, not an address list). ADR-004: the corrected value crosses the gamora↔star-lord seam.

### Action

- [ ] **Conductor** — three spec edits, using the `:1033` lineage form, at `:1714` / `:1991` / `:2102`.
      Correct the L-43(f) completeness claim in the ledger (it currently reads as done).
- [ ] **Conductor** — register the method rule as **standing**, not re-owned per fold: *a superseded
      claim is retired by grepping its declared spelling set to exhaustion and annotating every hit;
      a single-address edit does not discharge it.* Three folds of recurrence is a process defect,
      not three lapses.
- [ ] **star-lord** — `fixture_p06_state: bool = False`, `u9_bonus_spawn_state: str = "UNKNOWN"`,
      correct the `[M-1]` comment, and move the `test_baton_v1.py:448` perturbation to `True`.
      **Value fix only — this is not the type-expressiveness rider and must not wait on it.**
- [ ] **Matt (escalation only if unresolved before the Phase-E emit)** — the emit gate.

**Unblocks on:** the three spec edits + the schema default flip. Does **not** gate the locomotion
lap, the legolas citation probe, or the galadriel fourth extraction.

---

## D2-2 — **WARN** — F-12's negative-control column does not reproduce as a coherent set; the parameterisation is undeclared

The **base** column reproduces exactly (+23.16 / 0-in-band / +0.737 / 0.86×). The **fitted** column
does not. Published: *mean +0.44 s · 17/92 in-band (75 fail) · corr +0.757 · inversion 0.84×.*
Measured, sweeping both axes:

| n_seeds @ v_ref = 10.5 | in-band | fail | Δmean | corr | ratio |
|---:|---:|---:|---:|---:|---:|
| **1** | **17** | **75** | +0.289 | 0.7071 | 0.8871 |
| 6 | 14 | 78 | +0.395 | 0.7465 | 0.8659 |
| **8 (shipped default)** | 15 | 77 | +0.395 | 0.7534 | 0.8556 |
| 32 (declared band) | 15 | 77 | +0.372 | 0.7673 | 0.8646 |

**No single parameterisation produces all four numbers.** `75/92 fail` occurs only at **n_seeds = 1**;
`+0.757` sits at n_seeds ≈ 8–16; `0.84×` occurs **nowhere** in the grid (nor across v_ref 10.0–11.0).
Running the module's own shipped probe, `vref_sensitivity()`, does **not** reproduce its own docstring
at `calibration.py:539–540`.

The set has propagated verbatim into the commit message, the report, the math note § D.1/§ H.2, the
module docstring, ledger **L-43(b)**, and **spec § 14 F-12**.

**The conclusion is unaffected and I want that stated plainly.** Across the entire grid the structure
claim holds without exception: corr stays ≥ 0.70 against a measured 0.154, the ratio stays < 1.0
against a measured 2.00, and 74–81 of 92 still fail. *"A scale parameter cannot repair a structure
error"* is robust. Only the published digits are wrong, and they are now in the spec.

**Cite:** Discipline **#3** (seed policy — no undeclared parameterisation) and **#10**.
**Action:** gamora — re-run at the declared 32 seeds and restate § D.1 with `n_seeds` in the table
header; correct the module docstring. Conductor — restate the F-12 negative-control bullet from the
re-run.

---

## D2-3 — **WARN** — the survivors' causal characterisation is unsupported on both legs

F-12 reads *"Survivors: waves 80/90/92 (**few-bodies/high-HP**, kill-term-dominated)"*; L-43(b) says
*"survivors 80/90/92, few-bodies/high-HP"*; the math note § D says *"precisely the waves where the
fixture spent a long time on few, high-HP bodies."*

Measured on the run's **own** count model of record:

| wave | E[bodies] | class | class mean | measured |
|---:|---:|---|---:|---:|
| 80 | **25.00** | ×10 | 14.28 | 82.13 s |
| 90 | 2.00 | ×10 | 14.28 | 26.43 s |
| 92 | **27.33** | non-×10 | 20.23 | 78.45 s |

- **"few-bodies" is false of two of the three.** w80 carries 1.75× its own class mean; w92 carries
  1.35× its class mean. Only w90 is few-bodies.
- **"high-HP" is not measurable for band A**, by § C.1's own census: eHP is absent for 889 of 896
  band-A records. The beat is scrupulous about naming that absence and then leans on it as a cause.

**What the evidence does support**, and it is enough: the three survivors are the fixture's **1st,
2nd and 4th slowest** measured waves, and the absent kill term is the only modelled term whose sign
could lengthen the sim on them. That claim needs no body-count or HP premise and is fully carried.

The set membership, the 89/3 split and the arithmetic are **exact** — only the gloss is unsupported.

**Cite:** Principle **#1** (math-before-code — a stated cause needs a stated measurement); charter
§ 4.2 (named, never estimated).
**Action:** conductor — restate the F-12 survivor bullet. gamora — correct math note § D.

---

## D2-4 — **WARN** — C-5's parking is **sound**, and I can now demonstrate it is costless; the disposition carries no such demonstration

**Verdict on the parking itself: SOUND, in both directions.** Re-forming a tolerance *after* seeing a
92/92 FAIL is the textbook goalpost move, and refusing it is standing safety #1 working. The reverse
worry — that parking *preserves* a FAIL a better-formed predicate would not produce — is the one
worth testing, because nobody had.

I tested it. Verdict sensitivity, 32 seeds, declared `v_ref`:

| tolerance | in-band | lower-bound FALSIFIED |
|---|---:|---:|
| ± 1.00 s (pinned) | **0 / 92** | 89 |
| ± 2.00 s | **0 / 92** | 89 |
| ± 3.21 s (= 1 process sd) | **0 / 92** | 86 |
| ± 5.00 s | **0 / 92** | 84 |
| ± 6.42 s (= 2 process sd) | **0 / 92** | 82 |
| ± 10.0 s | 4 / 92 | 78 |
| per-wave band `max(1.0, 2 × that wave's own sd)` | **0 / 92** | — |
| per-wave band `max(1.0, 3 × that wave's own sd)` | 3 / 92 | — |

**No reformulation anywhere near the modelled process's own variance changes the verdict.** The FAIL
is tolerance-form-independent; it takes a ±10 s band — 10× the pin, 3× the process sd — to recover
four waves. C-5 therefore cannot move this run's outcome in either direction, and the parking costs
the run precisely nothing.

That is the fact that converts *"may NOT move this run's goalposts"* from a principled assertion into
a demonstrated one — and C-5 goes to **Matt** as a surface. Sending him a failed BINDING gate and a
"the tolerance may be mis-formed, parked" note **side by side, with no sensitivity measurement**,
leaves him unable to tell whether the parking is load-bearing. It is not, and he should be told so.

Corollary worth recording: the F-12 *diagnosis* never depended on the tolerance either — it rests on
a **sign** (2.00× vs 0.86×), a **correlation gap** (0.737 vs 0.154), and a **min-statistic**
falsification. Parking C-5 launders nothing.

**Cite:** Principle **#5** (severity matters — a Matt surface must carry the evidence that sizes it);
Discipline **#10**.
**Action:** conductor — fold the sensitivity table into C-5 / F-12 before the Matt surface. Table
above is reproducible from `calibration.t1_table()`.

---

## D2-5 — **WARN** — the pause does **not** change the decidable target state, but its stated rationale does not hold for beat 4

**Target-state check: PASSES.** T-1 was the only BINDING band-A gate; beat 4 is INFORMATIVE and beat
5 is explicitly unbound. Pausing them removes **no binding gate**. The un-pause condition
(*"locomotion lap lands AND s1 re-runs against UNCHANGED T-1"*) is pre-registered, falsifiable, and
names the pinned predicate it must clear. This is not a quiet target-state change.

**The rationale, though, is over-applied.** F-12 says *"s2 + full-ladder against a known 2.5×–5.1×
traversal inflation produce structurally-known-wrong numbers."* That is correct for **beat 5**
(unbound reported numbers that enter the record). It is **not** correct for beat 4. From § 12's own
ordering block, beat 4 is:

> s2 one-sided inequality (**INFORMATIVE tripwire**: sim kit-alone at 151–160 must clear **≤**
> fixture-with-defenses; **faster ⇒ anomaly tripwire → finding**)

The known defect biases the sim **slow**. A slow sim can only satisfy a `≤` inequality *more* easily.
**The known bias runs toward the tripwire's null**, so the defect cannot manufacture a false trip —
under the current build the tripwire's only failure mode is a *real* anomaly. A one-sided test whose
known error runs toward its null is not made uninformative by that error; it is made *conservative*,
which is the safe direction.

Two things are forgone by pausing it, both cheap:

1. The tripwire itself — a direction-safe observation available now.
2. **A second-geometry positive control on F-12's own diagnosis.** s2 is a *different arena*
   (`ARENA_S2` bearings 1.8/10.5/4.5/7.5). The locomotion hypothesis predicts the body-count
   correlation and the tour/farthest-spawn inflation reappear there. s2's *diagnostic* value is
   distinct from its *calibration* value, and the pause rationale only addresses the latter.

**Cite:** Discipline **#5** (triage) and **#2** (right tool for the validation question).
**Action:** conductor — either un-pause beat 4 on the direction-safety argument, or record why it is
declined. Beat 5's pause stands as reasoned.

---

## D2-6 — **WARN** — CD-2: the spec asserts a constraint the implemented check does not enforce for 2 of 5 policies

Spec `:1548–1549`: *"`tree_state_untracked_entries_outside_src` — int ≥ 0, NULLABLE; **set only under
code-surface-v1**."* Star-lord's § 1.3 table agrees, giving `null` for `any-change-v1` and
`tracked-only-v1` with the reason *"this policy draws no inside/outside line, so a number would be a
fiction."*

`_g_cd2_policy` (`baton_v1_validator.py:203–212`) enforces only:

- `code-surface-v1` **without** a count → fail
- a count that is negative / non-integral / bool → fail
- `declared-override` or `unavailable` **with** a count → fail

A baton carrying `any-change-v1` **plus** a count **passes**. The documented invariant is stricter
than the guard for 2 of 5 policies.

This is precisely the class star-lord himself diagnosed one level down at S-I1 — *"the guard was
narrower than the claim it was cited for"* — recurring one level up, in the same commit that fixed it.

Exposure is limited (the emitter always sets correctly), so the risk is a hand-built or third-party
baton. Small, but the whole point of CD-2 is that a provenance claim must not be able to be false.

**Cite:** Principle **#3**; Discipline **#8** (schema validation at boundaries).
**Action:** star-lord — extend check 5 to `policy != "code-surface-v1" and count is not None`;
**or** conductor — narrow the spec text to what is enforced. Either closes it; the drift must not
persist.

---

## D2-7 — **WARN** — CD-2 landed as fields with **no acceptance criterion** in the spec's own AC namespace

§ 11.4's AC table runs `AC-11.4a` … `AC-11.4h`. **No row binds `tree_state_policy` or
`tree_state_untracked_entries_outside_src`.** Enforcement lives solely in the export seam's private
`G-CD2-POLICY`.

Star-lord flagged this explicitly and pre-empted it (*"Carried as a `G-` id, not `AC-11.4i`, on
purpose… the conductor lands the § 11 row… Renaming it is one line in the `CHECKS` dict"*). The
conductor landed the **field inventory** but not the **criterion**. `AC-11.4g` — which binds
`u9_bonus_spawn_state` against `fixture_p06_state` — is the exact precedent for the row that is
missing.

Consequence: nothing in the spec requires the field to be present. A future emitter dropping it
breaks no spec AC, and `AC-11.4e`'s `FULL` refusal would then be issued without the rule that
produced the grade — the unrecorded claim CD-2 exists to prevent.

**Cite:** Discipline **#8**; Principle **#3**.
**Action:** conductor — land `AC-11.4i` (star-lord's five failure modes transcribe directly), or
explicitly ratify the `G-` namespace as sufficient for CD-2 so the absence is a decision rather than
an omission.

---

## D2-8 — **WARN** — F-11: "zero code" is contradicted by its own enumeration, and **option (a) does not deliver a clean tree**

**The census is exact and I reproduce it independently** (§ 7). Two problems with the framing:

**(i) "All notes/artifacts, zero code" is wrong.** Two of the ten are `.py`:

```
src/reincarnated/simulation/notes/step3_f3_boss_scale_smoke_2026_07_07.py
src/reincarnated/simulation/scripts/gamora_step3_f3_boss_scale_sweep_2026_07_07.py
```

F-11's own enumeration names them (*"2 simulation scripts"*) and star-lord's census counts them
(*"… of those, `.py` files: **2**"*). The summary bullet contradicts the two measurements it summarises.

**(ii) The decision-relevant omission.** Option **(a)** — the conductor's stated lean,
`code-surface-v2` = `src/` minus `src/**/output/` — would take the count from 2,414 to **10**. Ten is
not zero. **The tree still grades `dirty`; `AC-11.4e` still forbids `FULL`.** F-11 presents (a) as
the option that *"makes the policy measure the code surface its name claims"* — true — without stating
that **the Phase-E consequence is unchanged** unless those 10 entries are also committed or ignored,
and that 2 of them are `.py` under `src/` and would survive any plausible v2 scoping.

This goes to **Matt** as a fork. He should not have to derive that (a) alone does not restore a
FULL-capable grade. The complete fork is closer to: *v2-scoping **plus** disposing of 10 residual
entries*, or *(b) honest non-FULL*.

Everything else about the registration is sound: the mechanism confirming itself live is a legitimate
and rather good observation; `v1 STANDS until ruled` is the right interim; and I verified no code
change was smuggled in (`248f8738` is docstring-only, toward the measurement).

**Cite:** Discipline **#10**; Principle **#5** (a Matt surface must carry the arithmetic that sizes
the decision).
**Action:** conductor — correct "zero code", and add the residual-10 arithmetic to the fork before
the Phase-E touch.

---

## D2-9 — **INFO** — the sd triple: two of three figures do not reproduce, at two sites

Math note § F.2 and `calibration.py`'s `T1Row` docstring both read *"mean 3.21 s, max **5.04** s, min
**1.00** s."* Measured across the 92-wave table at 32 seeds: mean **3.2177** ✓, max **5.1036**
(wave 50), min **0.9499** (wave 90). `5.0463` is wave 67 — the *second*-highest, consistent with an
off-by-one on a sorted list.

gamora's **report** is correct at both places it appears (§ C-5 conflict row and the wave-50 table
row read 5.10), and `test_kc2_s1_ramp.py:236` reads 5.10. So the two wrong sites are intra-commit
outliers against three correct ones. Spec and ledger cite only 3.21 and are unaffected.

**Action:** gamora — correct math note § F.2 and the `T1Row` docstring. Two sites, no consumer.

---

## D2-10 — **INFO** — test-count reconciliation: **no conflict exists**, and the disputed figure is unsourced

**The `"129 green / 180 total"` attributed to star-lord at L-43(g) appears nowhere in his artifacts.**
His report § 0 and § 6, his commit message on `a53c97fc`, and his `AGENT_STATE.md` entry all read
**51 baton / 128 KC2**, consistently. The quotation appears only in the conductor's ledger; the most
likely origin is an arithmetic slip (51 + 128 = 179).

**There is no disagreement to adjudicate.** The two numbers are the same quantity at two commits:

| commit | `tests/test_kc2_*.py` | files | source |
|---|---:|---:|---|
| `a53c97fc` (+`248f8738`) | **128** | 6 | star-lord — correct at his HEAD |
| `13451fdf` | **155** | 7 | gamora — correct at hers (+27 = 26 new `test_kc2_s1_ramp.py`, 1 new `test_kc2_opposition_wave_engine.py`) |

`test_kc2_s1_ramp.py` did not exist when star-lord measured. Both are right.

**Authoritative counts, measured by me at engine HEAD `248f8738` + working tree:**

| selection | count |
|---|---:|
| `pytest tests/test_kc2_*.py --collect-only` | **155** |
| `pytest tests/ -k kc2 --collect-only` | **155** of 10,361 collected (10,206 deselected) — the glob and the `-k` expression **agree**, so the selection basis is not a source of drift |
| `pytest tests/test_baton_v1.py` | **51** |
| gamora's declared 9-file blast radius | **209 passed / 0 failed in 18.03 s** |
| whole `tests/` collection | **10,361** |

**209 = 155 (kc2) + 51 (baton) + 3 (`test_telegraph_value_set_census`)** — reconciles exactly. Her
19.8 s vs my 18.03 s is timing variance on the same 209.

**Action:** conductor — strike the `"129/180"` quotation from L-43(g) as unsourced; record
**KC2 155 · baton 51 · blast radius 209/209 green** as the counts of record.

---

## D2-11 — **INFO** — C-3's degeneracy claim is approximate, not exact, and it scopes the legolas probe

F-12 C-3: *"time ∝ radius / v_ref ⇒ (radius, v_ref) collapse to ONE free timescale; an engine m/s
citation … collapses the whole free-parameter surface by citation."*

`wave_engine.cycle_time` (`:599`):

```python
traversal = max(0.0, (emitter_distance_m - disc_radius_m)) / float(approach_speed_m_s)
```

`disc_radius_m = 3.0` is an **absolute** length. Under `(R, v) → (kR, kv)` traversal is **not**
invariant: `(kR − 3)/(kv) ≠ (R − 3)/v`. The same holds in `simulate_wave` for
`contact_distance_m = 1.0` and for the absolute spawn scatter, neither of which scales with R.

At the operating point the residual is not negligible: `(30 − 3)/4 = 6.75` against `R/v = 7.5` — a
**10 %** correction, which is the same order as **MO-5's own one-sided margin (+10.7 %)**.

So `(radius, v_ref)` are weakly but genuinely separable, and a `v_ref` citation collapses *most* of
the surface, not all of it. This matters operationally: **the legolas T3 radius-residency leg stays
live regardless of what T2 returns.** Under the C-3 wording as written, a successful T2 could be read
as retiring T3.

**Action:** conductor — soften the C-3/F-12 wording to "collapses the dominant free parameter";
keep T3 scoped independently of T2's outcome.

---

## D2-12 — **INFO** — cross-seam hazard for the C-4 lap: the only six-bearing "s1" list in the repo is arena-pooled

```
src/reincarnated/export/baton_v1_fixture.py:61
_SPAWN_POINT_BEARINGS = (3.0, 5.2, 6.9, 9.6, 1.8, 10.5)   # o'clock, s1 (L-21)
```

That is s1's four measured bearings **plus s2's first two** (`ARENA_S2 = Arena("s2", (1.8, 10.5,
4.5, 7.5))`), labelled *"s1 (L-21)"*.

**Not a live provenance defect.** The module header disclaims every number in it (*"a run-record
produced by this module must never be presented as a calibration result"*), and no calibration path
consumes it. It landed at `68e2e372` (Phase C) — not a defect of this fold.

**But** § 10.6 calls pooling bearings across sittings *"a spec violation, not a modelling choice"*,
and `Arena.merge` **raises** rather than averages precisely to prevent it. **C-4 is about to complete
`ARENA_S1` from four bearings to six**, and this is the only six-bearing "s1" list in the repo — it
is what an executor searching for prior art would find first.

**Action:** gamora — the two new s1 bearings must come from footage or be DECLARED; do **not** source
them here. star-lord — retag the comment `# SYNTHETIC — not s1 geometry`.

---

## D2-13 — **INFO** — the golden's provenance sidecar records a whole-file digest for a section-scoped extraction

`devotion_envelope_disclosure.provenance.json` records `spec_sha256
6aa777e192d1b3b1…` at `spec_git_commit_at_extraction 135dfa8a…`. The spec note today hashes
`b912291c39a37698…` — it has taken **+265 / −29 lines** since that commit.

**No false-pass risk.** No test compares the recorded spec digest; the cross-repo test re-extracts the
§ 9.5 block from the *live* file and it passed in my run. The field is simply not checkable, and will
read as stale to any human who looks at it.

A digest over the **extracted section** (rather than the whole note) would be both stable across
unrelated spec edits and actually assertable — which would let the in-repo pins detect a § 9.5 change
without needing the meta-repo present.

**Action:** star-lord — optional hardening; ADR-002 test/fixture tier, **my approval, no escalation.**

---

## D2-14 — **INFO** — Discipline #1 "written first": **verified by asymmetry**, and the mechanism is worth recording

The math note and the module landed in one commit, so ordering is not directly observable. I verified
it by three independent proxies:

1. **All ten** § G "Surfaces" exist in `calibration.py` with matching names and signatures.
2. § J's **J.1 … J.10** map one-to-one onto `test_J1 … test_J10`.
3. **The discriminating asymmetry.** § J.5 states only the bare rule (*"no measured clear literal is
   restated"*). The implemented
   `test_J5_no_measured_clear_time_LITERAL_is_restated_inside_the_mechanism` carries the entire
   `opposition.py` **11.0 / 13.0 / 19.0** false-positive discovery (`BIO_CURVES` coefficients
   colliding with the three measured clear times on whole seconds) and the narrowing to the 76
   non-integral values. **The note does not know what the implementation discovered.** A back-filled
   note would.

**One precision caveat.** §§ C–F carry *measured results*, which the note declares were taken on the
beat-2 build `6927dee5`. `t1_table` did not exist at `6927dee5`, so a scratch implementation of the
comparison preceded both. "Written BEFORE the code" is therefore true of the **shipped module**, not
of all code. That is fine and it is declared — and Discipline #1's purpose survives intact because
**no tuning surface exists**: T-1 is externally pinned in the spec, the target table is galadriel's,
and the sim was frozen at `6927dee5` (conductor-verified 27/27). The module could not have been
tuned to make the note's numbers come out.

**PASS as claimed.** No action.

---

## D2-15 — **INFO** — the lower-bound argument's separability assumption holds here, is asserted rather than established, and **will invert under C-3's amended model**

The argument is stated additively:

```
cycle_true(model) = 0.5 + traversal + kill + 0.5  >=  0.5 + traversal + 0 + 0.5 = cycle_sim
```

This treats `traversal` as invariant under supplying the kill term. In the harness the two are
**coupled**: with HP > 0 the player dwells at each stop, and bodies inside the 3 m disc accumulate
damage during the dwell — so collateral kills could in principle *shorten* the tour.

I checked the direction, then measured it rather than arguing it (`hp_lookup` swept, `ARENA_S1`,
seed = `S1_SEED_BASE + wave×1000`):

| wave | hp/body 0 | 1,000 | 20,000 | 200,000 |
|---:|---:|---:|---:|---:|
| 1 | 22.04 s / 87.8 m | 22.86 / 91.1 | 68.49 / 99.6 | *tick-cap, non-clear* |
| 47 | 39.92 / 159.3 | 40.98 / 163.6 | 113.80 / 175.8 | *tick-cap, non-clear* |
| 91 | 49.88 / 199.2 | 52.73 / 210.6 | 205.22 / 228.1 | *tick-cap, non-clear* |

**`t_end` and tour length both increase monotonically** with the supplied kill term, on every wave
tested, until the tick cap truncates into a non-clear (which is outside the T-1 comparison anyway).
The reason is structural: at HP = 0 every body swept by the disc dies on the tick it is covered, so
**collateral is already maximal**; with HP > 0 bodies survive sweeps and must be revisited. The bound
holds *a fortiori*. **The claim is correct.**

**The forward-looking part, which is why this is worth recording.** Under C-3's amended model —
monsters path to the player — the coupling **reverses sign**: bodies converge on the player, so
collateral *rises* with dwell time, and the same one-line separability argument will **not** carry
over. The locomotion lap must re-establish the bound rather than inherit it.

**Action:** gamora — one sentence in the math note establishing separability rather than assuming it;
carry the sign-reversal caveat into the locomotion lap's math note.

---

## 7 — What I reproduced independently (instruments: my own scripts, engine HEAD `248f8738` + working tree)

**T-1, full 92-wave table at the declared 32 seeds — every headline reproduces:**

| claim | published | measured |
|---|---|---|
| split | 0 / 89 / 3 | **0 / 89 / 3** ✓ |
| Δ mean · median | +23.16 · +24.48 | **+23.1556 · +24.4850** ✓ |
| Δ range | [−36.85, +39.05] | **[−36.8487, +39.0487]** ✓ |
| corr(sim, bodies) | +0.737 | **+0.7375** ✓ |
| corr(measured, bodies) | +0.154 | **+0.1537** ✓ |
| corr(sim, measured) | +0.212 | **+0.2118** ✓ |
| ×10 measured / sim / bodies | 28.57 / 34.04 / 14.28 | **28.5722 / 34.0382 / 14.2778** ✓ |
| non-×10 measured / sim / bodies | 14.29 / 39.37 / 20.23 | **14.2918 / 39.3656 / 20.2324** ✓ |
| ratios measured / sim | 2.00 / 0.86 | **1.9992 / 0.8647** ✓ |
| sign argument | 89 FALSIFIED, survivors 80/90/92 | **89 / [80, 90, 92]** ✓ |
| — *(my addition)* | — | **FALSIFIED ≡ OVER as sets** ✓ |
| eHP coverage | 466 / 434 / 896 / 28 / 7 | **466 / 434 / 896 / 28 / 7 / 889 uncovered** ✓ |
| § C.3 tour ratios | 2.49 / 3.01 / 4.07 / 4.90 / 0.92 / 5.12 | **all six exact** ✓ |
| sd mean | 3.21 | **3.2177** ✓ |
| sd max | 5.04 | **5.1036** ✗ → D2-9 |
| negative control (fitted) | +0.44 / 17 in-band / +0.757 / 0.84× | **does not reproduce as a set** ✗ → D2-2 |

**Code claims verified by reading, not by report:** static board (`run.py:287–288, 300–301, 319`;
spawn coords never reassigned) · kill term structurally zero (`run.py:253, 332, 345`) · `v_ref`
quarantine (`fixture.py:253`; no production consumer of 10.5) · MO-5 consumes the uncited radius
(`micro_oracles.py:216–225`) · F-12a's `:1089` citation · export↔simulation coupling (one read-only
import at `test_baton_v1.py:204`; zero `baton_v1_*` imports from `simulation.kc2`).

**Suites, run by me:** `test_baton_v1.py` **51 passed** · 9-file blast radius **209 passed / 0 failed
in 18.03 s** · `tests/test_kc2_*.py` collects **155** · whole `tests/` collects **10,361**.

**Tree-state census, run by me:** `2,414 / 2,404 / 10`, ten non-output entries **enumerated
item-for-item identical** to the conductor's L-42(d) list.

**Spec working diff vs `135dfa8a`:** +265 / −29; every deletion is a replacement-in-place carrying a
strike plus lineage. No dated RECORD text amputated.

---

## 8 — Actions, by owner

**Conductor (gandalf) — BLOCK-clearing first:**
- [ ] **D2-1** three spec edits (`:1714`, `:1991`, `:2102`) in the `:1033` lineage form; correct the
      L-43(f) completeness claim; register the value-set-grep rule as **standing**
- [ ] **D2-4** fold the tolerance-sensitivity table into C-5 / F-12 **before** the Matt surface
- [ ] **D2-8** correct "zero code"; add the residual-10 arithmetic to the F-11 fork
- [ ] **D2-3** restate the F-12 survivor bullet · **D2-2** restate the negative-control bullet after gamora's re-run
- [ ] **D2-5** un-pause beat 4 on direction-safety, or record the declination
- [ ] **D2-10** strike the unsourced `"129/180"`; record KC2 155 · baton 51 · 209/209
- [ ] **D2-11** soften C-3's degeneracy wording; keep legolas T3 independent of T2
- [ ] **D2-7** land `AC-11.4i`, or ratify the `G-` namespace as sufficient

**star-lord:**
- [ ] **D2-1** `fixture_p06_state → False`, `u9_bonus_spawn_state → "UNKNOWN"`, fix the `[M-1]`
      comment, move the `:448` perturbation — **value fix, independent of the type rider**
- [ ] **D2-6** widen the CD-2 count check (or accept the conductor narrowing the spec)
- [ ] **D2-12** retag `baton_v1_fixture.py:61` as SYNTHETIC
- [ ] **D2-13** *(optional)* section-scoped digest in the golden sidecar — **jack-ryan approved,
      ADR-002 test/fixture tier, no escalation**

**gamora:**
- [ ] **D2-2** re-run the negative control at 32 seeds; declare `n_seeds` in § D.1; fix the docstring
- [ ] **D2-3** correct math note § D's survivor gloss
- [ ] **D2-9** correct math note § F.2 and the `T1Row` docstring (5.04 → 5.10, 1.00 → 0.95)
- [ ] **D2-15** establish separability rather than assume it; carry the sign-reversal caveat into the
      locomotion lap
- [ ] **D2-12** do not source the two new s1 bearings from the baton fixture

**Matt — escalation only:**
- [ ] **D2-1** if unresolved before the Phase-E emit
- [ ] F-11 policy fork *(already queued; D2-8 completes the arithmetic he needs)*
- [ ] C-5 tolerance form *(already queued; D2-4 supplies the sensitivity evidence)*

---

## 9 — Note on the run's overall posture

Two things deserve saying at the level of the run rather than the finding.

**The gate FAIL was processed correctly, and that is the whole point of pre-registration.** T-1 was
pinned before the numbers existed, it failed 92/92, and neither the seam nor the conductor touched
it. gamora ran the licensed rescue as a *negative control* and reported that it does not work; the
conductor suspended the licence rather than exercising it. That sequence is the run behaving exactly
as the desirable-run-pattern intends, and my measurement at **D2-4** now shows the FAIL survives every
reasonable reformulation of its own tolerance — so the verdict was never tolerance-shopped and cannot
be.

**The one recurring process defect is superseded-claim retirement.** D-W3 at L-40, ~9 stale sites at
L-41(e), and now three more at L-43(f) — three consecutive folds of the same failure, each time
diagnosed correctly and each time re-owned as a fresh lapse. It is not a lapse; it is a missing
standing method. **D2-1**'s second action item is the fix, and it matters more than the three edits
that clear the BLOCK.

---

**Filed:** jack-ryan, DEV-MODE Gate-2 Phase-D2, 2026-08-08, KC2-SIM.
Spec and ledger **not edited** (conductor-owned; findings route back through this note).
Engine **not edited**. **Push NOT fired.**
