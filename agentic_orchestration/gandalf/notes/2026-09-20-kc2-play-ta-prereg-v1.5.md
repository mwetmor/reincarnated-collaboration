# KC2-PLAY · T-A PREREGISTRATION **v1.5** — the EXACT half is the instrument; the tolerance half is a DIAGNOSTIC and gates nothing

> ⚑ **STATUS: IMMUTABLE ON COMMIT — v1.5, authored 2026-09-21. SUPERSEDES v1.4 FORWARD.**
> *(The filename carries the series' `2026-09-20` prefix; the document's date is 2026-09-21.)*
>
> ⚑ **v1.4 IS IMMUTABLE AND A GRADED RUN EXISTS AGAINST IT.** Graded run #1 — gamora, 2026-09-21,
> verdict **`STRUCTURAL @ coverage 89/89`** (`gamora/notes/2026-09-21-kc2-play-ta-grade.md`, commit
> `df2dc1188`). Under v1.4 § G that makes any change **a HALT to Matt**, and v1.4's own header says
> *"Any change after a graded run exists is a HALT to Matt."* **This file is legal for one reason
> only: Matt ruled it.**
>
> ⚑ **THE AUTHORITY, IN HIS WORDS** (charter ledger **KP-49**, 2026-09-21, all five ELICITOR forks
> ruled — verbatim as recorded):
>
> > **"F1 = yes · F2 = re-base · … Agree on all specs"**
>
> and, as the ledger row records the five forks:
> * **F4** — *prereg **v1.5 AUTHORIZED*** (`Q84` struck; `canonical/matt_decision_needed/README.md`
>   row `Q84`, struck 2026-09-21).
> * **F5** — ⚑ ***"the EXACT half is kept permanently; the TOLERANCE half is a DIAGNOSTIC, NEVER A
>   GATE."***
> * **F3** — *the last graded run is spent **after** the decode lap and drax's repairs.*
> * **F2** — ⚑ ***RE-BASE*** — the oracle moves onto the decoded substrate once the decode lands,
>   reversing the conductor's KP-32-era ruling that pinned the oracle to v3.3.
>
> **v1.4, v1.3 (`66d2fc89`), v1.2 (`72204f7a`), v1.1 (`30111ac8`) and v1.0 (`5f2c27cf`) are NOT
> edited.** Superseded readings are named in place at **§ A**. **The v1.4 grade of record does not
> move** — nothing in this file regrades, rescues, widens or reclassifies anything that was graded.
>
> **Author:** gandalf (named sub-agent, `SPEC-AUTHOR`), Run KC2-PLAY. **Decision rules only.**
> ⚑ **NO BAND WIDTH IS MINTED HERE.** Where a width is owed it is left **named and empty**.
> **Occasioned by:** charter ledger **KP-43** (the grade) · **KP-44** / **KP-45** / **KP-48** (drax's
> two repair passes and his hold work) · **KP-46** (gamora's two reads, her own withdrawal, and the
> confound enumerated across the whole band set) · **KP-47** (ratification 2) · **KP-49** (Matt).

---

### ⚑ PINS — **every pin re-derived this session by `shasum -a 256`, none retyped from a prior document**

*(The standing rule, born from my own double carry-forward defect at KP-20 and re-earned at
KP-43 § 0.1: **a new version re-derives every pin it carries, including the ones it believes are
unchanged, and prints them in one table.** At v1.4, three of seven were "believed unchanged" and one
of those had moved. At v1.5, one of eight is **replaced outright** because the pin itself was wrong.)*

| # | artifact | **sha256 — derived 2026-09-21** | what moved since v1.4 |
|---|---|---|---|
| **P-a** | `agentic_orchestration/gamora/notes/2026-09-20-kc2-play-ta-band-widths.md` — the governing width file | **`7a5d4aa3305ed14748a903b60ebfe48ac1a186fdb951fb6b8608abba92406750`** | **unchanged** — re-derived, not carried. *(This file has moved three times across the series; it has not moved since v1.4.)* |
| **P-b** | `agentic_orchestration/galadriel/notes/…-w1-tb-expected-values-and-u-rider.md` | **`8186202cc0c78ae9ef428c57164fac35bd1adb0e14ec5310c395783361653158`** | unchanged — re-derived |
| **P-c** | `agentic_orchestration/galadriel/notes/…-w1-tb-expected-values.json` | **`a8b85331764ba3fe90f45cf7cd6f1a25f6dc0dae4a7e7fa555c487f0b153ea0b`** | unchanged — re-derived |
| **P-d** | `agentic_orchestration/galadriel/notes/…-w1-tb-release-labels.json` | **`15dace604c8d5bb4888223a8b25a07a038bae44431ebd194d682545c0f29c58a`** | unchanged — re-derived |
| **P-e** | `~/Games/reincarnated-engine/src/reincarnated/simulation/math/kc2-play-v3p3-monster-offense-prereg-2026-09-20.md` | ⚑ **`27fc59378aee8c9d412f486a63864a3b2ceb5c5473520b60ad80128d47d99cdc`** | ⚑ **REPLACED. v1.4 pinned `97e5a4c7…` and that pin was WRONG** — it predates Addendum 2 by three minutes and still carried the **dead refusal rule live** at all four sites. `C1` tripped on it at the grade (KP-43 § 0.1). **v1.5 pins the CURRENT revision, derived here**, and the annotation is corrected in place at **§ A row 1** |
| **P-f** | `…/simulation/output/kc2-lifted-rows-KC2PLAY-v3p3-monster-offense-20260920_214408.json` — **11,847,705 B, verified by `stat`** | **`e51b54a118f657ba7abd4298e5fcea86cfab3aeedebf8dd70a1239c5ea1b776e`** | unchanged — re-derived |
| **P-g** | `…/simulation/output/kc2-lifted-rows-KC2PLAY-W1-v3p2-full-20260920_163932.json` — **362,156 B, verified** | **`e011742935f14efaba2e9eb45e7bca11e1131fc19d6f936526498d4f7ac1af96`** | unchanged — re-derived |
| ⚑ **P-h** | ⚑ **NEW — THE MODEL PACK.** `…/simulation/output/kc2-model-pack-v3-E-s09-cp150-mech-v3p3-20260921_022612/model/` | `waves.json` **`38c43a9c3b35560a3dce88ac16c189cb03b120b1ba2085ae2458040113621072`** · `monsters.json` **`3839322955b7d4af0a6c8c8b169656136a0271a7ab9bb68893a272df703701a0`** · `monster_offense.json` **`e1b5072ef246088b7b7ba9f907f65128bc01be39a21919f8fd6244fb6385cb7f`** · `math_rules.json` **`2becfb4ff532de708f51cb0c1b598c551cf07bbcf9db811cb7d46a155d8abf5f`** · `monster_defense.json` **`00ffab1576577164cc132b498817d5480822df3234f3f3bcf286c0a407193aac`** · `arena.json` **`e65b7da05e87028136e616ad5f7391ca88cb1ae4db3956fc679c1cf0008f3ba6`** · `rng_contract.json` **`ff6f77b0d54037f61847ab7785b58db324a7a0294d666c952b85fc955127a308`** · `config_of_record.json` **`d34ce0d8d5546ac7de5ab6ea6b30bc5dfae6460c078643d90c54a9209b78ebc4`** | ⚑ **THE LARGEST SILENT HOLE v1.4 LEFT — see § A row 2** |
| ⚑ **P-i** | ⚑ **NEW** — `~/Games/reincarnated-engine/data/kc2/pm4p_leech_resistance.csv` (**3,312,159 B**) | **`cb6a008bde1e102573181968ab7f60958cd28fee07ff8736078fa092a80dd62e`** | ⚑ **the table `V1-JOIN-1` joins and the port did not load. `TA-X-26` grades against it** |
| **P-j** | ⚑ **NEW, for lineage only** — `~/Games/reincarnated-engine/data/kc2/pm4l_mitigation_by_body.csv` (**5,444,380 B**) | **`a8c1ffd97dc703419f8447f3d7bbba3903e0f14d2c2e6746a938ceefae9ecec6`** | pinned because § 7.2's *"undone work, not absent data"* finding rests on it; **not graded by any row** |

**Documents of record, derived here so the next reader need not:**

| document | sha256 |
|---|---|
| prereg **v1.4** (superseded by this file, **not edited**) | `3c83c7ac9a80bf20f34034a6e91765f08bcad34a8d5b97dc4c354e2e2e245cdf` |
| **the grade** — `gamora/notes/2026-09-21-kc2-play-ta-grade.md`, body + Addendum 1 + Addendum 2 | `c2ab0d38f31496d6d42f6054557dd7d338e7f101b577836e5e2f220236935134` |
| divergence register **v0.3** (companion; file form) | `5028b555313df2f4690cd96881c700c7d66a4733612894c150c2448915510444` |
| divergence register v0.3 (**machine** form, emitter-derived, 28 rows) | `453231e0afefbf101010677bb72e685c43c2fa68666dbac44f118d1e14b07e68` — ⚑ **carried from the grade § 0, gamora-derived; I cannot derive a form only the emitter produces, and I do not pretend to** |

### ⚑ SEALED CELLS — **hash-verified this session; K-7 held, never opened, never re-run**

| cell | path (`~/Games/reincarnated-engine/src/reincarnated/simulation/output/`) | sha256 **derived** | bytes **verified** |
|---|---|---|---:|
| `[M-POL2]` | `kc2-checkpoint-E-s09-cp150-mpol2-20260825_114420.json` | `ad61ad2a8c799d6ef11a68436756c253f0a34fbb1052e575cdf9f9cd3a44dc5c` | 123,564 |
| `[MECH]` | `kc2-checkpoint-E-s09-cp150-mech-20260816_124031.json` | `20b05cb4ef3bd888b998cbc46c68b41a8051111c12fbcf2066d101b0a4b15f4b` | 2,125,271 |
| `[W1W]` | `kc2-checkpoint-E-s09-cp150-w1walls-20260825_220058.json` | `7a992c81ca6e56e54a53534b438a9ddf87ed42f1bf1a3d0ecc2d2f3c3db7881b` | 403,084 |

**Counts at v1.5:** **4 preconditions** · **26 EXACT** · **19 DIAGNOSTIC ids (0 counted, 0 gating — F5)** · 2 emitted-not-graded.
**Standing law:** Law 3 · K-7 · D4 · GL-6 / GL-12 · Disciplines **#72 · #75 · #78 · #79 · #84 · #85** · R-L91-4 · D-MPOL2-2 · R-L89-4 · `L-49` · digests **derived at use, never retyped**.

---

## § A · CHANGE TABLE — v1.4 (2026-09-20 22:12) → v1.5 (2026-09-21)

| # | clause | v1.4 | **v1.5** | reason | authority |
|---|---|---|---|---|---|
| 1 | **P-e's pin + its annotation** | `97e5a4c7…`, annotated *"This sha covers the body AND both addenda"* | ⚑ **`27fc5937…`, and the annotation is STRUCK as FALSE.** `grep -c "ADDENDUM 2"` on the pinned revision returns **0**; the pinned commit predates Addendum 2 by three minutes and carries the **dead refusal rule live at all four sites** | ⚑ **My defect, and it is worse than a stale byte: a builder obeying that pin would have implemented refusal under `ORACLE`, reddened `TA-X-25(a)`, and measured every band on a board 216–273 bodies per arm lighter than the one the widths came from.** drax built against the **current file** and that is why `TA-X-25` is green — **`#75` cl. 1(a): a pin proves what a REVIEWER checked, never what a BUILDER used** | **KP-43 § 0.1** · **KP-47** (`D → AMEND #75 cl. 1(a)`) |
| 2 | ⚑ **THE MODEL PACK** | *(never pinned, in any version)* | ⚑ **NEW pin `P-h` + precondition `P-4`** — the pack directory **named**, eight load-bearing files **individually hashed** | ⚑ **THE LARGEST SILENT HOLE v1.4 LEFT.** `TA-X-09` grades vectors *"from the pack"*; `P-3` asserts `POOL-466`'s cardinality from the pack; `TA-X-16`'s spawn-point keys, `TA-X-24`'s phase model and `TA-X-27`'s degenerate-pair census are all pack properties — **and no version of this prereg said WHICH pack.** ⚑ **There are SEVEN `kc2-model-pack*/model/waves.json` on this host, THREE of them `v3p3` minted within six minutes of each other.** I hashed the three: they are **byte-identical on all four load-bearing files**, so the hazard is **live in the instrument and benign in the outcome** — which is the only kind of hazard you get to fix for free. **v1.4's own change-row 3 already ruled this class:** *a consumed artifact with no pin is outside the immutability guarantee entirely* | **v1.4 row 3 / BLOCK-2, applied forward** · ⚑ **and it becomes load-bearing under F2: the pack is exactly what a re-base moves** |
| 3 | ⚑ **THE BAND HALF** | **6 COUNTED** band rows; a counted band red ⇒ verdict `STATISTICAL` | ⚑ **DEMOTED WHOLESALE TO DIAGNOSTIC. NO BAND GATES ANYTHING. `STATISTICAL` IS RETIRED AS A VERDICT.** The verdict rests on the **EXACT rows alone** | ⚑ **Matt F5, verbatim: *"keep the exact-match half permanently; treat the tolerance half as a DIAGNOSTIC, NEVER A GATE."*** The evidence is § A.1's perfect-port table: **zero of six counted bands can discriminate a faithful port at this fight length** | **KP-49 (F5)** · **KP-46** |
| 4 | ⚑ **PER-WAVE RESTATEMENT** | every rate on `D` (per-tick), numerators counting per-wave events | ⚑ **FOUR NEW DIAGNOSTIC ids — `TA-B-16…19`** — released / stationary / motion-suppressed ticks **per wave**, plus **ticks per wave** itself | ⚑ **`TA-B-07` goes from a 5× miss to a 1.5× miss on a port whose Type-A limb is entirely absent** — *it stops charging the port for surviving and starts charging it for the thing that is actually wrong.* **Computable on both sides from artifacts that already exist; `K-7` does not block it** | **KP-46** · grade **B5** |
| 5 | ⚑ **`TA-B-06`'s CONSTRUCTION** | *"plant ratio (window 5.0 s)"* — **the statistic was never defined anywhere in the corpus** | ⚑ **DEFINED, AND THE DEFINITION IS DERIVED AND REPRODUCES 5/5 — § F.3a.** And ⚑ **the port is computing a DIFFERENT STATISTIC, not merely over a different window** | ⚑ **gamora declared the window under-specification as hers (grade § 10 item 1). The under-specification was deeper than she said: the ORACLE's `n_window` is a TICK COUNT (61 ticks per wave) and the PORT's `n_windows` is a WINDOW COUNT (`D/61`). One symbol, two dimensions.** ⚑ **`TA-B-06`'s red does not localise a fidelity failure at all** | **grade § 10 item 1** · **B3**; the derivation is mine |
| 6 | ⚑ **CALIBRATION RANGE ON EVERY WIDTH'S FACE** | *(absent)* | ⚑ **MANDATORY REPORT-FACE FIELD on every diagnostic — § F.5 cl. 5** | ⚑ **The widths were calibrated over ticks-per-wave ∈ [106, 185] — a 1.75× span — and applied at 482.4, which is 2.6× outside the top of it, AND NOTHING SAID SO.** *"A correction belongs where the rule is read"* (`WARN-6`) applied to a **precondition** rather than to a correction | **KP-46** · grade **B1 / B5** |
| 7 | ⚑ **TWO NEW EXACT ROWS** | 24 EXACT | ⚑ **26 — `TA-X-26` (declared-JOIN conformance) · `TA-X-27` (degenerate-draw consumption)** | ⚑ **Both are things the run learned the hard way and NO EXISTING ROW CAUGHT.** § A.2 | **KP-46** · **KP-48** · **KP-49** |
| 8 | ⚑ **THE THREE UNGRADEABLE EXACT ROWS** | `TA-X-01` · `TA-X-15` · `TA-X-16`(enforcement) UNGRADEABLE | ⚑ **ALL THREE GIVEN A CLOSING CONDITION, and two of them close on drax's landed repairs** — § F.2c | ⚑ *"A repair pass that fixes only the two reds lands on `INDETERMINATE`, which trips the cap just as hard."* **All five must close** | **grade § 3.2** · **KP-44** · **KP-48** |
| 9 | ⚑ **`TA-X-07`'s TOLERANCE** | bare **`1e-6`**, absolute-or-relative **not stated**; graded ABSOLUTE ⇒ RED on 11 of 25 | ⚑ **RELATIVE, with an absolute floor, and with an ACCUMULATION BUDGET that makes the constant checkable instead of chosen** — § F.2d | ⚑ **`1.7e-6` on a quantity near `1e8` is float64 accumulation, not damage created — `ulp(1e8) ≈ 1.49e-8`, so the worst residual is ≈ 114 ulps.** *The tolerance does a different job than the sentence justifying it.* ⚑ **v1.4's RED STANDS; `Q83(c)` is untouched.** This is a v1.5 construction pre-registered before any v1.5 run, **not a post-hoc widening of a graded instrument** | **KP-43** · `Q83(c)` recommendation text · **KP-49 F4** (*"Agree on all specs"*) |
| 10 | ⚑ **`TA-X-06`** | EXACT, graded **RED** | ⚑ **CARRIED AS CLASSED — EXACT — with gamora's mis-class evidence printed on its face and `Q83(b)` flagged OPEN** — § F.2e | ⚑ **I decline to reclass it in v1.5 while `Q83(b)` asks Matt to reclass it in v1.4.** Reclassing here would **moot** the question instead of answering it — the CLAUDE.md corollary the run already paid for once: *an escalation overtaken by events still requires a disposition; silence is not one.* ⚑ **One ruling moves BOTH versions** | `Q83(b)` **OPEN** · grade **§ 6** |
| 11 | ⚑ **THE STRUCTURAL-ZERO CLASS** | named ad hoc, row by row (`TA-X-11`'s caveat, then `TA-X-12`, then `TA-X-19`) | ⚑ **PROMOTED TO A STANDING REPORT-FACE RULE — § F.5 cl. 6: every EXACT row satisfied by an ABSENCE prints the absence** | ⚑ **Four instances, and the run discovered each one separately:** `TA-X-11` (*a port with no wall also scores zero*) · `TA-X-12` (aprons **absent**, not present-at-zero) · `TA-X-19` (**no arrival limb at all**) · ⚑ **`TA-X-15`(b), NEW — drax reports the intra-point stagger as *unrepresentable rather than absent***. **Stop re-discovering the class; make the report print it** | grade **§ 3.1** · **KP-44** |
| 12 | **verdict taxonomy** | 4 verdicts, `STATISTICAL` among them | ⚑ **3 verdicts. `STATISTICAL` retired** — § G | F5's direct consequence, **including the one place it LOOSENS the instrument, declared at § G.1 rather than buried** | **KP-49 (F5)** |
| 13 | ⚑ **THE GRADED-RUN CAP** | *"two graded runs against the same prereg version"* — a **version**-scoped counter | ⚑ **v1.5 DOES NOT RESET IT. ONE graded run remains.** The counter is **run**-scoped against the **v3.3 reference**, and § H states the only thing that resets it | ⚑ **Matt F3 says *"the LAST graded run"* — singular.** A counter that resets whenever the run rebuilds its own instrument **is not a cap**, and reading the charter's version-scoping as licence would make v1.5 an evasion of the gate it was authorized to improve | **KP-49 (F3)** |
| 14 | **supersession sweep** | run at v1.4 | ⚑ **RUN AND RECORDED — § A.3** | the standing rule | — |

### ⚑ A.1 · THE SPINE OF THIS REWRITE — **a hypothetically PERFECT port, at the port's fight length**

**This table is the reason the band half is demoted, and it is the first thing a grader must read.**
It is gamora's (grade **Addendum 2 § B4**), transcribed with its derivation, not re-computed by me.

**The dilution factor, derived from the seal and the emission:**

| | per-salt `D` | `n_waves` | ticks/wave | **mean-of-salts** |
|---|---|---|---|---:|
| **oracle `M-POL-2`** | `[1084, 305, 106, 185, 1103]` | `[6, 2, 1, 1, 6]` | `[180.7, 152.5, 106.0, 185.0, 183.8]` | **161.6** |
| **port `M-POL-2`** | `[5064, 4704, 4908, 4764, 4680]` | `[10 × 5]` | `[506.4, 470.4, 490.8, 476.4, 468.0]` | **482.4** |

> ⚑ **DILUTION FACTOR = 482.4 / 161.6 = `2.985×`.**

⚑ **Cross-checked against drax's independent motion attribution, and the two agree:** the oracle's
stationary fraction **0.1425** ÷ `2.985` **predicts 0.0477**; his repaired port **measures 0.0320**;
the residual is the **absent Type-A motion-suppress** (his 80 ticks), which the port does not fire at
all. **Mechanism and arithmetic agree** (KP-45, KP-46).

**And the consequence, which is the whole of F5's justification:**

| row | oracle mean | **perfect port at `T = 482`** | band (P-a) | **outcome** |
|---|---:|---:|---|---|
| `TA-B-02` uptime | 0.879189 | **0.9379** | [0.7840, **1.0**] | ⚑ **GREEN — and green for the BROKEN port too. CANNOT FAIL.** |
| `TA-B-04` `P(chan\|moving)` | 0.907002 | → **clip** | [0.8120, **1.0**] | ⚑ **GREEN. The confound pushes it at the clip. CANNOT FAIL.** |
| `TA-B-03` `frac_moving` | 0.857462 | **0.9523** | [0.8331, 0.8818] | ⚑ **RED, +2.9 half-widths. CANNOT PASS.** |
| `TA-B-09` channel split | 0.115395 | **0.038658** | [0.105100, 0.125689] | ⚑ **RED, −6.45 half-widths. CANNOT PASS.** |
| `TA-B-05` `P(chan\|stationary)` | 0.715784 | — | [0.5868, 0.8448] | ⚑ **INDETERMINATE — the dilution largely cancels; gamora declines to name a direction she cannot derive** |
| `TA-B-06` plant ratio | 1.284877 | — | [1.0052, 1.5646] | ⚑ **STATISTIC IMMUNE, INSTRUMENT BROKEN** — § F.3a |

> ⚑ **ZERO OF SIX COUNTED BANDS CAN DISCRIMINATE A FAITHFUL PORT FROM AN UNFAITHFUL ONE AT
> `T = 482`.** Two cannot fail, two cannot pass, one is indeterminate, one is measured by a broken
> instrument.

⚑ **What this does NOT say, and the distinction is load-bearing.** The four band reds in the grade
are **not** four fidelity failures. They are **one pilot-motion divergence** — real, and localised —
**plus a confound that would have reddened two of them regardless.** `TA-B-09` at **+32.5**
half-widths is far beyond the **−6.45** the confound alone predicts **and its sign is wrong**, so a
genuine defect sits underneath. *(gamora did not draw that distinction at her § 4.1 and drew it at
Addendum 2 § B4; it is carried here because a grader reading only § 4.1 would over-count.)*

⚑ **And the sharpest sentence in the whole finding, which is why § F.5 cl. 5 exists:**
*"I never asked whether these statistics were scale-free in the one dimension the port was free to
move."*

### ⚑ A.2 · THE TWO NEW EXACT ROWS — what the run learned the hard way, and no row caught

**Both are `v0_limb_set` / draw-stream failures that every existing row walked past.**

1. ⚑ **THE LEECH JOIN WAS LIFTED, PUBLISHED, WRITTEN INTO THE PORT'S OWN SOURCE, AND NEVER
   CALLED.** `V1-JOIN-1` — the per-body leech-**resistance** gate joined from
   `pm4p_leech_resistance.csv` — is applied by the oracle at `player_sustain.py:663` (`mult =
   self.adcth_mult(record)`) and `:699` (`out = portion * mult`). The port **defined**
   `adcth_mult_coupled` at `kc2rt_laws.gd:110`, **documented the law** at `:106`, and had **zero call
   sites**; the CSV was never loaded. **The port over-healed by `1/0.266406 = 3.754×` on every body
   on every tick, and by `∞` on the leech-immune records** (grade **Addendum 1 § A1.2–A1.4**).
   ⚑ **The framing that matters: this is a `v0_limb_set` CONFORMANCE failure. The runtime prints
   `sustain = LeechResistLimb.COUPLED (DRIVER-OF-RECORD)` into the header the prereg says is
   *"diffed line-by-line against `V0` before any row is read"* — and the limb it declares has no
   implementation. The header diff cannot catch it, BECAUSE THE HEADER IS WHERE THE CLAIM IS MADE.**
   *(`TA-X-16` in a second costume, on the sustain path — gamora's words.)* Wired at KP-48; `leech/intake`
   **~149× → ~29×**.
2. ⚑ **A DEGENERATE DRAW IS NOT A FREE DRAW, AND THE PORT'S OBVIOUS OPTIMISATION DESYNCHRONISES THE
   BOARD STREAM ON WAVE 1.** CPython's `randint(30,30)` → `randrange(30,31)` → `_randbelow(1)` →
   `getrandbits(1)` **and reject until it draws 0**. Measured over 20 seeds: `[2,1,5,1,1,2,4,1,1,1,
   2,1,1,1,1,2,1,2,1,2]` — ⚑ **1, 2, 4 or 5 calls; GEOMETRIC, not a constant 1** (grade Addendum 1
   § A2.1; drax's vector, KP-48). ⚑ **And the hazard is live at a site nobody had pointed at:**
   `rng.randint(int(b.n_min), int(b.n_max))` at `wave_engine.py:840` / `:949` is **inside the 29
   registered sites**, on the board roll itself.
   ⚑ **DERIVED INDEPENDENTLY THIS SESSION, against `P-h`'s pinned `waves.json`:** over
   `pools.wave_spawn_count` at global waves 151–160, **139 min/max pairs, of which 97 are degenerate
   (`n_min == n_max`) = 69.8 %.** ⚑ **gamora's figure reproduces exactly — and it now carries a pack
   pin, which hers did not.**
   ⚑ **Seven of every ten board-roll count draws in the graded window are degenerate.** A port
   writing `if lo == hi: return lo` takes **zero** draws where the oracle takes **one to five** —
   and the failure is **intermittent, on roughly half the occasions, which is the worst possible
   failure mode because it looks like noise.** **Invisible to every row v1.4 had:** `TA-X-25(c)`
   proves membership only, the bands cannot see which monsters were picked, `P-2` covers *fold*
   granularity and not per-site draw counts, and `S5` is out of scope.
   ⚑ **My own ruling was wrong three times in its phrasing before it was right** — *"a degenerate
   draw the oracle takes is still a draw"* (singular) would also have desynchronised. **gamora
   corrected it to *reproduce the rejection loop*; drax's measurement corrected the count.** Recorded
   because the row exists in its correct form only because two seats pushed back on the conductor.

### ⚑ A.3 · SUPERSESSION SWEEP — run against the documents, not against recollection

| stale figure hunted | found live-tense? | disposition |
|---|---|---|
| ⚑ **`183.58`** — the analytic `E[bodies]` | ⚑ **NOT in v1.4** (its § E.3 carries `98.08`/`97`, which are correct and unaffected). **It is live in the GRADE's § 8 H3 and § 4.5 table** — and **gamora withdrew it in her own Addendum 1 § A3**: the pack recomputation gives **137.58** at p06 ON and **126.08** at p06 OFF | ⚑ **`TA-B-15`'s and § F.5's reference points must NOT range against `183.58`.** The corrected figures are carried; **`P-e` Addendum § 3's re-derivation is OWED BY GAMORA and the slot is left named and empty (§ F.3c)** |
| ceiling **`C-c`** (*"34–45 bodies short per salt, 3–4× the cap's predicted effect"*) | ⚑ **live in the GRADE § 9** | ⚑ **VOID** — there is no body-count shortfall for the `limitN` cap to be compared against (Addendum 1 § A3.1). **Struck at § E.2** |
| `bodies/pick` **2.50 vs 4.22** as a port defect | live in the grade § 8 H3 | ⚑ **WITHDRAWN.** The port's **2.638** matches the pack's **2.683**; the outlier is the sealed `[MECH]` cell's **4.217**, ⚑ **a DIFFERENT ARM** — the cross-arm caveat gamora printed and then reasoned past in the same paragraph |
| the **refusal discriminator** promise (*"nonzero ⇒ UNGRADEABLE"*) | ⚑ **struck in P-e at `b87e282c`** — which is **why `P-e`'s pin moved** and why v1.4's `C1` tripped | **dead under `ORACLE` by construction; `TA-X-25(a)` grades the zero as an identity.** Ceiling `C-a` holds |
| coverage **`72`** | ⚑ **still live in the CHARTER** (§ 4.3 / § 4.4 / § 3 F1 / § 9) and in `kc2rt_coverage.gd`'s **constant NAME** | **`OQ-1` and `OQ-3` still owed — carried forward at § I.** ⚑ **The sweep's own finding, unchanged from v1.4: the prereg and register were never the carriers. The charter was, and still is.** |

---

## § B · CONFIGURATION AND PRECONDITIONS — **four**

### B.1 · `ORACLE` — v3.2 `V0`, five arms, five salts *(unchanged from v1.4 § B.1; restated because v1.4 is superseded and a grader must not hold two files open)*

`V0` carries five `V0-ARM-*` rows — `M0`, `M-POL-2`, `M-POL-2-NULL`, `W1`, `W1-NULL` — each a
**DELTA against the base row set, never a second full copy**. **5 arms × 5 salts = 25 headless
runs**, each arm the base set with **exactly one fold moved**; that single-fold delta is the entire
reason the inertness relations are readable, and it is why `W1-NULL` returns to **`M-POL-2`** and not
to `M0` (`TA-X-04`).

Limbs of record: `spawn_fold: POLAR_UNIFORM_RHO` · `sustain: COUPLED` · `intake: ARMOUR_THEN_RESIST
+ global_flat` · `summons: PRESENT_INERT + offense MEASURED_BASIC` · `arena_fold: None` (armed only
in `W1`) · `interrupts_fold: None` · `WarCryLimb.COOLDOWN` (7.5 s) · `PotionLimb.TRACE_CONSISTENT`
(θ 0.22972972972972974) · `CritLimb: LO` · **`p06: OFF`** · `PhaseModel: ENGAGE`.

**The runtime prints its RESOLVED limb set into the verdict header (`v0_limb_set`), diffed
line-by-line against `V0` before any row is read; it refuses to boot on an unset limb rather than
defaulting one.** ⚑ **AND AT v1.5 THAT IS NOT SUFFICIENT ON ITS OWN — see `TA-X-26`. A header diff
cannot catch a declared limb with no implementation, because the header is where the claim is made.**

**Pilot:** scripted — `DRIVE_TO_PACK` + the M-POL-2 channel policy; `v_ref = 4.0` is a
DECLARED-FREE-PARAMETER → 5.4 m/s; **no facing model**. ⚑ **The pilot's MOTION LAW is `V0-04`** —
*"drive-THROUGH with rolling re-target; the step is never clamped at the target"* — **and it is
declared on the wire.** drax's early-return on a body inside the 3.0 m disc was his sentence and not
the wire's (KP-44); repaired, `frac_moving` **0.538 → 0.968**, ⚑ **not tuned toward any band.**

**Declared fight scope: waves 151–160.**

### B.2 · `P-1` · COVERAGE — **89 / 89** *(unchanged)*

All **89 enumerated census row ids** mapped **mechanically** to exactly one of `IMPLEMENTED` ·
`DIVERGENCE(DIV-nn)` · `RUNTIME-CHOICE(absent_ref)` · `OUT-OF-SCOPE`. **Counts sum to 89. Zero
unmapped.** Graded as `TA-X-02`.

⚑ **Three conditions raised at the grade, carried forward and NOT closed by re-declaring them:**
1. **`P-1` gates COMPLETENESS, not TRUTH, and at least one mapping was false** — census `M4` mapped
   `IMPLEMENTED` with a note describing an implementation that did not exist (grade § 2 cl. 1). **The
   mapping is a claim; `TA-X-15` is the check.** ⚑ **v1.5 adds cl. 1a below.**
2. ⚑ **THE GATE HAS NO CELL FOR *"the pack cannot supply this."*** Three rows are carried as
   `RUNTIME-CHOICE(absent_ref)` with registered choice `REFUSED` and counted as `refusals: 3`, which
   is the right handling of a gate shape with no cell for the case. ⚑ **`P-1` at v1.5 REQUIRES the
   refusal count to be emitted, so the mapping cannot hide them.**
3. `kc2rt_coverage.gd` still holds a constant **named** `CHARTER_DENOMINATOR` (value now 89).
   **`OQ-3`'s point was the NAME** — it asserts the charter as authority for a number the census
   enumerates. **Rename owed.**

⚑ **`P-1` cl. 1a, NEW:** **every `IMPLEMENTED` mapping whose census row is ALSO graded by an EXACT
row must name that row id in its note.** Then a false `IMPLEMENTED` is caught by the *cross-reference*
rather than by a grader reading the source — which is how `M4` was caught, and it took a human read.

### B.3 · `P-2` · STREAM DISJOINTNESS — and what it still does not cover *(unchanged in construction)*

**Probe:** run `M-POL-2` salt 0 twice, once with a **no-op fold inserted that draws zero values**;
assert identical digests. **COVERS** stream isolation at *fold* granularity.

⚑ **DOES NOT COVER:** (1) that the port's draw sites are the **same sites in the same order** —
V9's registry is **29 live sites across 11 streams** (+2 NOT-LIVE); (2) the **BOARD ROLL's
composition** (trap 6); (3) whether the per-site assignment is *lifted* or *chosen*.
⚑ **NARROWED AT v1.5 BY ONE BIT AND ONLY ONE:** `TA-X-27` now covers the **degenerate-draw
consumption** class at the two `randint` sites. **The rest of (1) and all of (2) stand open.**

**`P-2` red → `TA-X-03…06` UNGRADEABLE → `INDETERMINATE` → the cap trips.**

### B.4 · `P-3` · ROLL POPULATION AND ROLL LAW *(unchanged in ruling; re-pinned)*

**RULED (KP-32): T-A rolls from `POOL-466`, as the oracle rolls. `ANCHOR-169` is not forced and it
is NOT AVAILABLE.**

| id | n | the rule |
|---|---:|---|
| **ROSTER-790** | **790** | every `record_path` in `monsters.json::blocks` carrying a `wave`; **+1 declared-absence key** (`krieg_aethertrap`) ⇒ 791 distinct keys. **GL-12: a declared null is NOT-MODELLED, never a measured zero** |
| ⚑ **POOL-466** | **466** | pool members of every pool referenced by waves 151–160; cross-checked by a second independent route. ⚑ **THIS IS WHAT `L-49` HAS THE RUNTIME ROLL FROM** |
| **ANCHOR-169** | **169** | the records in `pm2_tg2_monster_timing.csv` — **the threat DECODE's coverage** |
| **BOTH-128** | **128** | `ANCHOR-169 ∩ POOL-466` |

**THE ROLL LAW — two stages, and only one is weighted:** **WEIGHTED** by `pool_weight` at the
pool-alternative stage (`wave_engine.py:974 _weighted_pick`); ⚑ **UNIFORM** at the name stage
(`:849, :869 rng.randrange(len(roster_names))`). **The port implements the ORACLE's law, not the
referent's.** A port that weights the name draw is wrong, and wrong in a direction no diagnostic
localises.

⚑ **THREE OF THESE FOUR CARDINALITIES ARE DECODE-COVERAGE FIGURES AND F2 MOVES THEM — § H.**

`roll_population` / `roll_law` are declared in the header and diffed at boot. **`P-3` red →
`INDETERMINATE`.** ⚑ **A declaration is self-reported; `TA-X-25(c)` is the behavioural check, and
the two are not redundant.**

### B.5 · ⚑ `P-4` · **PACK IDENTITY** — NEW

**The runtime declares the model pack it consumed and the loader hash-verifies it before any row is
read:**

```
pack_dir     : "kc2-model-pack-v3-E-s09-cp150-mech-v3p3-20260921_022612"
pack_files   : {waves.json: 38c43a9c…, monsters.json: 38393229…, monster_offense.json: e1b5072e…,
                math_rules.json: 2becfb4f…, monster_defense.json: 00ffab15…, arena.json: e65b7da0…,
                rng_contract.json: ff6f77b0…, config_of_record.json: d34ce0d8…}
```

⚑ **Every hash above is `P-h`, derived this session. A mismatch is `C1` and the cap trips** — the
cap's `C1` already reads *"any pinned sha mismatched"*, so no new cap condition is needed and none
is added.

> ⚑ **Why this is not bookkeeping.** **Seven `waves.json` exist on this host; three are `v3p3`,
> minted within six minutes.** I hashed all three and they agree byte-for-byte on the four
> load-bearing files, so nothing that has been graded is wrong. ⚑ **But `TA-X-09` grades "the
> pack's" nine vectors; `P-3` asserts a cardinality read from the pack; `TA-X-16`'s spawn-point keys,
> `TA-X-24`'s phase model and `TA-X-27`'s degenerate-pair census are all pack facts — and the
> instrument never said which pack.** The port's own source names
> `…v3p3-20260921_022612` at eight sites, **which is a BUILDER's statement and exactly the thing
> `#75` cl. 1(a) says a pin must be checked against.** ⚑ **And under F2 the pack is the object that
> MOVES.** A re-base with no pack pin is a re-base with no before-state.

---

## § C · THE DENOMINATOR LAW — and ⚑ **THE GRAIN LAW, NEW AT v1.5**

```
D_constructed = CHANNELLING + CHANNELLING_AND_MOVING + MOVING + IDLE      (PRE_FIGHT and DEAD excluded)
```
Verified on the seal: pooled `287 + 2211 + 166 + 119 = 2783 = D`; the per-salt sum equals the pooled
sum, so the partition is exact at both grains. ⚑ **No sealed artifact carries `D`. It is CONSTRUCTED.**

**Two identities, 5/5 on the seal, graded as `TA-X-08`:** `n_player_ticks_observed = D + PRE_FIGHT` ·
`n_channelling + n_released = D` ⇒ `uptime + n_released/D = 1.000000` exactly.
⚑ **The seal publishes `release_duty` on `D + PRE_FIGHT`** — the **0.215-vs-0.217 tell** resolves
entirely to a denominator difference. **Every per-tick rate divides by `D` and by nothing else.**

**C.2 · Pooled vs mean-of-salts.** Every diagnostic is on the **MEAN-OF-SALTS**; a port's pooled
figure is never compared against these. `D` per salt is **[1084, 305, 106, 185, 1103]** — a **10.4×
span.**
**C.3 · The compared object** is the **mean of a NEW 5-salt run**; the interval is a **prediction
interval** carrying both runs' sampling error; `ddof = 1`; `half-width = t(0.975, df=4) · s · √(2/5)
= 1.755978 · s`. **All widths live in P-a. None is minted here.**
**C.4 · T-B denominators are NOT these** (P-b). HP occupancy on `LIVE-MAX` reproduces 42.84 %;
NOMINAL gives 39.76 % — **3.08 pp with no fight in it.** HP window 181.0 s; energy / motion / release
/ cast 182.65 s.
**C.5 · A THIRD DENOMINATOR CLASS — BODIES.** `TA-B-15` and the per-wave coverage lines divide by
**BODIES** and cluster by **POOL PICKS** — populations with no relationship to `D` or to the T-B
windows. **Never pool them, never compare them, and never print a body-fraction under a heading that
has been printing tick-fractions.**

### ⚑ C.6 · **THE GRAIN LAW** — the discipline this run produced, stated as a rule

> ⚑ **BEFORE BANDING A RATE, NAME ITS NUMERATOR'S GRAIN AND ITS DENOMINATOR'S GRAIN SEPARATELY, AND
> STATE THE RANGE OF THE RATIO BETWEEN THEM OVER WHICH THE BAND WAS CALIBRATED.**

**The mechanical test:** *a fraction is confounded iff its numerator and its denominator scale with
**different** quantities.* `per-wave / per-tick` → **diluted by ticks-per-wave**. `per-wave /
per-wave` and `per-tick / per-tick` → **immune**.

⚑ **A FOURTH GRAIN EXISTS AND THE RUN FOUND IT AT `TA-B-06`: ABSOLUTE TIME.** A window of **5.0
seconds** is neither per-wave nor per-tick — it is a fixed duration, and its **coverage of a wave**
therefore dilutes by exactly the same `2.985×`. ⚑ **So `TA-B-06`'s statistic is immune and its
WINDOW is not**, and a report that prints the ratio without printing the window's coverage of a wave
has printed half the fact. **§ F.3a implements this.**

⚑ **AND THE CLAUSE THAT KEEPS v1.5 FROM REPEATING v1.4'S MISTAKE IN A NEW COSTUME.** The four
per-wave restatements at `TA-B-16…19` are **SCALE-FREE BY CONSTRUCTION (mechanism), NOT BY
MEASUREMENT.** The oracle's measurement range — ticks-per-wave ∈ **[106, 185]**, a 1.75× span —
**is still too narrow to test the claim.** ⚑ *A low CV inside the calibration range is not evidence
of invariance outside it.* **The diagnostic that CAN test it is `TA-B-19`, and that is its whole
purpose.** Where dispersion and mechanism disagree, ⚑ **MECHANISM WINS**, and the reason is printed:
the dispersion was measured over a range that could not distinguish *"this rate is scale-free in
`T`"* from *"`T` barely moved."*

---

## § D · ROW-ID CONCORDANCE — the single namespace

⚑ **Every citation uses the `TA-` id; a width is looked up by STATISTIC NAME in the table named
"governs", never by a bare `B-n`.** ⚑ **No retired id is ever re-used** (`TA-X-23` and `TA-B-13`'s
band form stay retired).

| **canonical** | statistic | gandalf v1.0 | gamora § 2.4 | gamora Add. 1 | **width governs** |
|---|---|---|---|---|---|
| `TA-B-01` | terminal wave | B-1 | B-1 | — | § 2.4 · **REPORT-ONLY** |
| `TA-B-02` | **uptime** on `D` | B-3 | **B-2** | **B-4** | Add. 1 restatement |
| `TA-B-03` | `frac_moving` on `D` | B-4 | B-3 | B-3 | Add. 1 restatement |
| `TA-B-04` | `P(chan \| moving)` | B-5a | B-4 | B-5a | Add. 1 restatement |
| `TA-B-05` | `P(chan \| stationary)` | B-5b | B-5 | B-5b | Add. 1 restatement |
| `TA-B-06` | plant ratio | B-8 | B-6 | B-6 | ⚑ **P-a's width is on the OLD construction — § F.3a** |
| `TA-B-07` | release duty on `D` | B-7 | B-7 | B-7 (restated) | Add. 1 |
| `TA-B-09` | channel split | *(v1.1)* | — | — | **Addendum 2 § B2** |
| `TA-B-15` | NO-DATA spawn count / fraction | — | — | — | **none, and none may ever be minted** |
| ⚑ `TA-B-16…19` | ⚑ **the per-wave restatements** | — | — | — | ⚑ **OWED — named and empty (§ F.3b)** |
| `TA-X-03…06` | inertness / distinctness | E-2, E-3, E-4 | **E-1 (a–d)** | A4 | — |
| `TA-X-07` | conservation, 7 terms | E-5 | **E-2** | — | — |
| `TA-X-02` | coverage | E-1 | **E-3** *at 89/89* | — | — |
| `TA-X-08` | denominator identity | *(implicit)* | **E-4** | A1 | — |
| `TA-X-11` | wall-clamp zeros | E-7b | — | **A2** | — |
| `TA-X-25` | NO-DATA path, 3 clauses | — | — | — | **P-e Addendum § 5** |
| ⚑ `TA-X-26` | ⚑ **declared-JOIN conformance** | — | — | — | ⚑ **`P-i` + this document** |
| ⚑ `TA-X-27` | ⚑ **degenerate-draw consumption** | — | — | — | ⚑ **`P-h` + this document** |

*The uptime row remains the reason this table exists: **B-3 · B-2 · B-4 — three ids, one statistic,
two files.*** ⚑ *And `TA-X-26`/`TA-X-27` extend it across a third artifact class: their governing
text is in **this** document and their governing DATA is a CSV and a pack — neither of which is P-a.*

---

## § E · OUTSIDE T-A'S REACH — the catching-row audit

### E.1 · The traps

| # | trap | **caught by** | verdict at v1.5 |
|---|---|---|---|
| **1** | `V5-GUARD-2` — arrival `px, py` are TELEMETRY ONLY | `TA-X-19` | **CLOSED** ⚑ *(and see § F.5 cl. 6 — the port has no arrival limb, so the negative is satisfied vacuously)* |
| **2** | `V9-DEAD-2` — the retired square-box scatter draws at the **same stream position** | `TA-X-17` + `TA-X-18` | **CLOSED** |
| **3** | `V17` — `hit_test_model = "point"` vs the sim's uniform 3.0 m disc | `TA-X-20` (resolved predicate); `R2D-5` owns the DRAWN radius | **HALF-CLOSED — declared** |
| **4** | `V4-LAW-1` — the cadence law is **not RNG-neutral** | `TA-X-21` | **CLOSED** |
| **5** | `V18 + V19` — flag **AND** coin = 0.15 applied twice | `TA-X-22` | **CLOSED** |
| **6** | ⚑ **THE BOARD ROLL** | `TA-X-25(c)` (membership) + `P-3` + ⚑ **`TA-X-27` (degenerate-draw consumption), NEW** | ⚑ **STILL OPEN — and narrower again.** `TA-X-27` closes the *draw-count* half of the stream hazard; **composition stays open** |
| **7** | attack-**PHASE** model — `HASH` default vs `ENGAGE` of record | `TA-X-24` | **CLOSED** |
| ⚑ **8** | ⚑ **NEW — A DECLARED LIMB OR JOIN WITH NO IMPLEMENTATION.** The `v0_limb_set` header diff **cannot** catch it | ⚑ **`TA-X-26`** | ⚑ **NEWLY INSTRUMENTED.** It cost the run a 3.754× over-heal and was found by a `grep` nobody had run on their own claim |

⚑ **Trap 6, restated with v1.5's movement stated honestly.** **12 of the 29 live draw sites are the
board roll.** Its divergence shows as **a different SET of monsters, not a different number.**
`TA-X-25(c)` proves **membership**, never **composition** — a port rolling POOL-466 with wrong
`pool_weight`s, wrong `count_bounds`, or a weighted name draw passes it cleanly. ⚑ **And the grade
proved that concretely: the composition question walked straight through `TA-X-25(c)` and was
settled by ARITHMETIC AGAINST THE PACK, not by any T-A row.** **Closure is still a sibling that
emits per-wave class counts.**

⚑ **The limit on `TA-X-11` that must not be over-read, and it now has a general form (§ F.5 cl. 6):**
the oracle's clamp counters are **structural zeros** — the wall never binds (margin
`43.758085 − 43.404802 = 0.353283` m = **0.807 %**). `TA-X-11` says *"the port never needed to
clamp"*, **not** *"the port's wall works"*; **a port with no wall at all also scores zero.**

### E.2 · DECLARED CEILINGS

| # | ceiling | status at v1.5 |
|---|---|---|
| **C-a** | The refusal discriminator is **structurally dead under `ORACLE`** | ⚑ **HOLDS; the port confirmed it (`refused = 0` on 25/25).** The run traded a **per-salt discriminator** for a **per-arm one-bit presence test**; the trade was correct and the report must not print it as though the discriminator survived. Only the `PLAY`-side probe can settle it |
| **C-b** | The ten-wave composition expectation has **NO empirical check** — the sealed census covers 151–155; the fight scope is 151–160 | ⚑ **HOLDS AND IS LOAD-BEARING.** Waves 156–160 carry **50.9 %** of the port's bodies. **No cell has ever validated that half, and `K-7` forbids making one.** ⚑ **F2's re-base is the first thing that could** |
| ~~**C-c**~~ | ~~the `limitN` residual, against a measured shortfall~~ | ⚑ **STRUCK — VOID.** The shortfall it was compared against was `183.58`, **which does not reproduce from the pack.** There is no shortfall for the cap to explain (Addendum 1 § A3.1). ⚑ **The `limitN` question itself is NOT struck** — it is simply un-measured, and it is re-opened at § I OQ-6 |
| **C-d** | honest-fail row (b) `342` does not decompose against (a) `338` + 6 measured-inert | ⚑ **OPEN, and gamora confirms the grain disagreement is real:** `v20_monster_attack_slot` resolves **688** distinct rows on `(record_path, kind, slot, damage_type)` against **678** on the published key — **10 rows silently collide, including a 15.0 m attack against a 3.0 m one on the same record.** One line closes the label |
| ⚑ **C-e** | ⚑ **NEW — `TA-B-12` (intake / leech) has NO ORACLE SIDE, and it is the most expensive ceiling in the run** | ⚑ **HOLDS.** `leech`, `intake` and `damage_total` return **zero keys on both seals**; the port emits all three richly. ⚑ **UNTIL A SIBLING EMITS THE ORACLE SIDE, A GREEN T-A IS COMPATIBLE WITH AN UNKILLABLE PLAYER — and § F.5 cl. 7 requires that sentence on the report's face.** The port is `terminal_reason = cleared` on **25/25**, `killer_id` empty, **HP never below 79.44 %**, against an oracle that is `player_death` **20/20**. ⚑ **The port did not narrowly survive. It ran out of content while never in danger** |
| ⚑ **C-f** | ⚑ **NEW — THE `~29×` LEECH SURPLUS IS UNEXPLAINED AFTER `V1-JOIN-1` WAS WIRED** | ⚑ **OPEN.** ~149× → ~29×; gamora's time-to-kill hypothesis is **REFUTED for the port** by drax's emission (armed bodies do swing: never-swung **5–11 (7–12 %)**, dead inside one swing period **1–3 (1–4 %)**, **426–458 swings landed**). ⚑ **Conductor read, labelled as a read: the residual is plausibly dominated by THE DECODE GAP ITSELF** — 338 records with no offense at all, **plus 996 attack slots declared against 667 decoded (67 %) inside the armed set.** **Testable the moment the decode lands, and that is F2** |
| ⚑ **C-g** | ⚑ **NEW — EVERY WIDTH IN P-a WAS CALIBRATED OVER TICKS-PER-WAVE ∈ [106, 185] AND APPLIED AT 482.4** | ⚑ **THE CEILING THAT PRODUCED THIS DOCUMENT.** 2.6× outside the top of the calibration range, on **all six** counted rows. **§ F.5 cl. 5 makes it un-missable rather than closing it** |
| **S5 / 29 sites** | a stream divergence is **visible and not locatable** | **HOLDS.** 34 sites declared / **29 live** / 5,856 draws on `M-POL-2` s0, and no sealed cell to place them against |

---

## § F · THE GRADED ROWS

### F.1 · Decisiveness classes — **AMENDED BY F5**

**EXACT** — identity, invariant, count, or declared-precision reproduction; a red says **the port is
wrong**; may carry a **NUMERICAL** tolerance, **never a STATISTICAL one**. ⚑ **The EXACT set is the
entire instrument. Every verdict antecedent is an EXACT-row fact.**

⚑ **DIAGNOSTIC** *(replaces v1.4's `BAND` / `COUNTED` / `REPORTED-NOT-COUNTED` / `CONDITIONAL`
sub-classes)* — distributional at n = 5. ⚑ **NO DIAGNOSTIC GATES ANYTHING. A diagnostic cannot
produce, raise, or lower a verdict. It cannot trip the cap. It cannot be counted in a PASS label.**
Matt, F5: ***"treat the tolerance half as a DIAGNOSTIC, NEVER A GATE."***

⚑ **What a diagnostic IS for, so the demotion is not read as deletion.** A diagnostic **localises a
mechanism.** `TA-B-09` at +32.5 half-widths with the **wrong sign** told the run that a genuine
motion defect sat underneath the confound — that is worth more than any pass/fail it could have
emitted, and it is why F5 keeps them rather than striking them. **The demotion removes their
AUTHORITY, not their VALUE.**

⚑ **The structural-zero class, retained verbatim from v1.4 because it is now cited four times.** An
EXACT row may assert a **STRUCTURAL ZERO or a STRUCTURAL NON-ZERO** — a quantity whose value is fixed
by the construction of the system rather than by a distribution. **The test for membership: can you
name the mechanism that makes the other value impossible?** If the answer is *"it would be very
unlikely"*, **it is a diagnostic and it does not belong here.**

### F.2 · EXACT rows — **26**

| id | statistic | basis | tolerance | ⚑ **F2 re-base** |
|---|---|---|---|---|
| `TA-X-01` | port self-determinism — any arm/salt run twice → identical digest | run-internal | byte-exact | invariant |
| `TA-X-02` | **coverage 89/89**, zero unmapped | the census id list | integer | ⚑ **total invariant; the 4-way COUNTS move** |
| `TA-X-03` | inertness A — `port(M-POL-2-NULL, s) ≡ port(M0, s)`, all 5 | `[M-POL2]` | byte-exact | invariant in form; **digests move** |
| `TA-X-04` | inertness B — `port(W1-NULL, s) ≡ port(M-POL-2, s)`, all 5 ⚑ **not M0** | `[W1W]` | byte-exact | invariant in form |
| `TA-X-05` | distinctness C — `port(M-POL-2, s) ≢ port(M0, s)`, ≥ 1 salt | `[M-POL2]` | exact, one-sided | invariant in form |
| ⚑ `TA-X-06` | distinctness D — `port(W1, s) ≢ port(M-POL-2, s)`, ≥ 1 salt | `[W1W]` | **RELATION ONLY, never magnitude** | ⚑ **§ F.2e — `Q83(b)` OPEN** |
| ⚑ `TA-X-07` | **conservation — SEVEN terms** `offered = applied + dropped + voided + pool_truncated + pcl_reclaim + counterplay_absorbed` | run-internal | ⚑ **§ F.2d — RELATIVE, with a floor and a budget** | invariant |
| `TA-X-08` | denominator identity, both sub-identities | `[M-POL2]`, 5/5 | exact | invariant |
| `TA-X-09` | all **9** `math_rules.test_vectors` | ⚑ **`P-h`'s `math_rules.json`** | per-vector | ⚑ **RE-PIN; the nine may move** |
| `TA-X-10` | containment supremum `max_body_radius_m ≤ 43.758085029822276` (W1) | `[W1W]` · `P-h`'s `arena.json` | exact, ≤ | ⚑ **re-derive from the re-based arena** |
| `TA-X-11` | wall-clamp zeros — `n_wall_clamps_{player,body} == 0`, every W1 arm | `[W1W]` | integer | invariant in form; ⚑ **the 0.807 % margin re-measures** |
| `TA-X-12` | pool inertness under ORACLE — total pool damage `== 0.0` | `[W1W]` ⚑ **`DIV-19`: the entrance aprons must not defeat this** | exact | invariant |
| `TA-X-13` | no player crit | `V0 · CritLimb LO` | integer | invariant |
| `TA-X-14` | the two DO-NOTs (`cause == "energy"` → 0; no release-on-every-cast) | pack prohibitions, R2D-4 | integer | invariant |
| ⚑ `TA-X-15` | **release schedule — TWO CLAUSES at v1.5** | census M4 / `V11` | § F.2c | invariant |
| ⚑ `TA-X-16` | **p06 OFF — declared value AND enforcement** | `V0-36` · `P-h`'s `waves.json` | § F.2c | ⚑ **re-derive the pick count** |
| `TA-X-17` | spawn offset — `‖spawn_xy − anchor_xy‖ ≤ 8.0` m, every body, arm, salt | `ρ = 8.0·u₂` | exact, ≤ | invariant |
| `TA-X-18` | **scatter-law three-law discriminator** — feed `u₁ = u₂ = 0.5`, assert **`(−4.0, 0.0)`** | polar → `(−4.0, 0)` · uniform-in-area → `(−5.656854, 0)` · box → `(0.0, 0.0)` | exact | invariant |
| `TA-X-19` | arrival unconditionality; **no damage predicate reads an arrival's `px, py`** | `deferred_arrival.py:13-17` | integer | invariant ⚑ **· § F.5 cl. 6** |
| `TA-X-20` | player hit-test predicate — 2.99 m hit / 3.01 m miss; no angular gate; no target cap | census D7 | exact | invariant |
| `TA-X-21` | **quantisation rule per site + zero bare `round(`** on the port's threat path | four modules | exact | ⚑ **re-verify the LIVE site list** |
| `TA-X-22` | flag-off release cause under ORACLE — `cause == "interrupts_channel_flag"` **0** | `V0`; V18+V19 | integer | invariant |
| ~~`TA-X-23`~~ | ~~board-roll composition~~ | ⚑ **STRUCK at v1.2. Id retired, never re-used** | — | — |
| `TA-X-24` | **attack-phase model is `ENGAGE`** — `sha256(actor_id) mod n` never evaluated | `V0`; `run.py:696` / `threat.py:1246` carry `HASH` as the **DEFAULT** | exact | invariant |
| ⚑ `TA-X-25` | **THE NO-DATA PATH — three clauses** | P-e Addendum § 5 | integer / exact, one-sided | ⚑ **THE ROW F2 GUTS — § H.3** |
| ⚑ **`TA-X-26`** | ⚑ **DECLARED-JOIN CONFORMANCE — five clauses** | § F.2a | integer / exact / declared-precision | ⚑ **clauses (a)–(d) invariant; (e) re-bases** |
| ⚑ **`TA-X-27`** | ⚑ **DEGENERATE-DRAW CONSUMPTION — four clauses** | § F.2b | integer / byte-exact | ⚑ **(d) re-derives from the new pack** |

#### ⚑ F.2a · `TA-X-26` — **DECLARED-JOIN CONFORMANCE** *(NEW)*

> ⚑ **THE PRINCIPLE, AND IT IS THE REASON THE ROW EXISTS:** the `v0_limb_set` header diff cannot
> catch a declared limb with no implementation, **because the header is where the claim is made.**
> The limb-consumption audit drax built at KP-44 covers **declared LIMBS**. ⚑ **It must cover
> declared JOINS.**

| clause | assertion | class | what a RED means |
|---|---|---|---|
| ⚑ **(a)** | **every declared JOIN in `V0`/`V1` is either CONSUMED — with a named call site emitted — or DECLARED-UNCONSUMED BY NAME against an absence row.** The runtime emits `join_consumption_audit` with one entry per declared join and asserts `n_declared == n_consumed + n_declared_unconsumed`, **zero joins in neither state**, and **refuses the cell otherwise** | **EXACT · integer identity** | ⚑ **a `v0_limb_set` conformance failure — the header states a claim the runtime does not implement.** *`TA-X-16` in a second costume* |
| ⚑ **(b)** | `V1-JOIN-1` specifically: `pm4p_leech_resistance.csv` is **LOADED**, its sha verified against **`P-i` = `cb6a008bde1e102573181968ab7f60958cd28fee07ff8736078fa092a80dd62e`**, and the emitted audit names **≥ 1 call site on the sustain path** | **EXACT · structural non-zero** | the join is defined and not called — **the exact defect, byte for byte** |
| ⚑ **(c)** | **PARSE INTEGRITY — RFC-4180.** On load: **7,900 data rows** · **790 distinct `record` values** · ⚑ **exactly 8 distinct `total_leech_resist_pct` values** · **exactly 5 distinct `adcth_mult_COUPLED` values** · **all 790 records wave-invariant** in `adcth_mult_COUPLED` | **EXACT · integer counts** | ⚑ **the parse is shifted.** **THE TIER GATE ALREADY CAUGHT THIS ONCE AND IT POINTED THE WRONG WAY:** `"Galakros, the Mountain"` carries a **quoted comma** — ⚑ **and I derived it independently: 210 of the 7,900 rows carry a comma inside `display_name`**, which shifted 210 rows and landed **`0.0` = LEECH-IMMUNE at the multiplier's index**, in the **OPPOSITE** direction from the defect being repaired. ⚑ *"The gate was not loosened to admit the 9th value; the 9th value was the defect."* |
| ⚑ **(d)** | **THE LAW IS READ, NEVER RECOMPUTED** (`V1-LIMB-2`): the applied multiplier comes from the CSV **column**; any helper implementing `max(0, 1 − res/100)` exists **only as a cross-check** and has **exactly one call site** | **EXACT · structural** | ⚑ **wiring the helper as the SOURCE would be a second, smaller infidelity** — drax's own retraction at KP-48, and the row makes it enforceable rather than remembered |
| ⚑ **(e)** | **MAGNITUDE, ON THE ARMED SET** — over the armed records of `POOL-466`: `mean(adcth_mult_COUPLED)` reproduces **`0.266406`**, median `0.25`, max `0.35`, min `0.0` | **EXACT · declared-precision, `± 5e-7`** | the armed-set join is wrong. ⚑ **THIS IS THE ONE CLAUSE THAT RE-BASES** — see below |

> ⚑ **A DESIGN DECISION MADE IN ANTICIPATION OF F2, AND STATED SO IT IS NOT MISTAKEN FOR AN
> OVERSIGHT.** Clauses **(a)–(d) are anchored on SUBSTRATE-INVARIANT facts** — the CSV's sha, its
> 7,900 rows, its 790 records, its 8 tiers, its parse, its single call site. ⚑ **Clause (e) is
> anchored on the ARMED SET, and the armed set is DEFINED BY THE OFFENSE DECODE THAT F2 ENLARGES.**
> gamora's `0.266406` and her *"5 records at exactly 0.0"* are measured over **the 128 armed records**
> (grade Addendum 1 § A1.4 — its heading says so).
> ⚑ **DERIVED HERE, AND IT PROVES THE POINT:** over **all 790** records the same column gives
> **mean `0.252215`**, median `0.25`, max `0.35`, and ⚑ **48 records at exactly `0.0` — not 5.**
> **Same file, same column, two populations, two answers.** *This is the fifth instance in this run
> of one shape — the arithmetic correct, the POPULATION it ranged over the defect* — and **clause (e)
> carries its population in its own sentence for exactly that reason.**
>
> ⚑ **And the tiers are not decoration.** Derived: `total_leech_resist_pct ∈ {65, 75, 83, 88, 105,
> 115, 565, 588}` — which **reproduces the port's own source comment verbatim** (*"the 8 tiers FLOOR
> at 65 % on every Ultimate enemy, and tiers 7/8 are 565 % / 588 %"*). Under `max(0, 1 − res/100)`
> the last four tiers all collapse to `0.0`, which is why **8 tiers give 5 multiplier values.** ⚑ **A
> gate asserting 5 where it should assert 8, or 8 where it should assert 5, would be green on a
> shifted parse. Both counts are asserted, and they are not redundant.**

#### ⚑ F.2b · `TA-X-27` — **DEGENERATE-DRAW CONSUMPTION** *(NEW)*

| clause | assertion | class | what a RED means |
|---|---|---|---|
| ⚑ **(a)** | **SOURCE NEGATIVE — no short-circuit.** A purity scan over the whole runtime tree finds **zero** `lo == hi` / `n_min == n_max` / equivalent early-returns on **any registered draw site**. ⚑ **The scan censuses every draw-site call and refuses any it cannot classify** — the same shape as the `register_choice` census, **not a hand-picked set** | **EXACT · integer, scanned** | ⚑ **the board stream desynchronises on wave 1 and never recovers** |
| ⚑ **(b)** | **THE REJECTION LOOP IS REPRODUCED, NOT APPROXIMATED.** A vector table replays CPython's `_randbelow_with_getrandbits` — reject-and-redraw while `r >= n`, every `getrandbits` counted — and asserts the **per-seed** consumption counts, **never the mean** | **EXACT · byte-exact per vector** | ⚑ **the consumption is GEOMETRIC, measured mean ~2 and values in `{1,2,4,5}` over 20 seeds. A port accounting a degenerate draw as ONE value desynchronises intermittently, on roughly half the occasions — the worst failure mode, because it looks like noise** |
| ⚑ **(c)** | **THE CONDUCTOR'S RULING, IN ITS CORRECTED FORM, IS ASSERTED AT THE SITE:** the port consumes exactly what the **ORACLE** consumes. Where the oracle takes no draw (**p05 — `wave_engine.py:683-695` takes no `rng`**), the port takes none; `V9`'s registry stays at **29 live sites** | **EXACT · integer identity** | a registry defect, or an invented draw. ⚑ **The `P05_BURST_DRAW_CONSUMED` constant carries both branches and the reasoning AT THE SITE, so a later reversal is a flag flip and a re-register, not a hunt** |
| ⚑ **(d)** | **THE DEGENERATE-PAIR CENSUS.** Reading **`P-h`'s `waves.json::pools.wave_spawn_count`** over global waves 151–160, the port reports **139 min/max pairs** of which ⚑ **97 are degenerate (69.8 %)** | **EXACT · integer counts** | the port is not reading the pinned pack, or is reading it at the wrong grain |

> ⚑ **Clause (d) derived independently this session against `P-h`, and it reproduces gamora's figure
> exactly — 139 pairs, 97 degenerate, 69.8 %.** ⚑ **Her figure carried no pack pin and there are
> three `v3p3` packs on this host; `P-h` supplies the pin her derivation lacked.**
> ⚑ **And the honest limit of this whole row, printed so nobody over-reads it: `TA-X-27` closes the
> DRAW-COUNT half of trap 6. It says nothing about WHICH monsters were picked.** Composition closure
> is still a sibling emitting per-wave class counts.
>
> ⚑ **THE RULING'S LINEAGE, RECORDED BECAUSE IT IS THE ROW'S STRONGEST CREDENTIAL.** The conductor
> ruled *"a degenerate draw the oracle takes is still a draw."* **gamora measured that "still a draw"
> (singular) would ALSO have desynchronised** and corrected it to *reproduce the rejection loop*;
> **drax measured that the consumption is geometric.** ⚑ *The row exists in a correct form only
> because two seats pushed back on the conductor, twice, on the same sentence.*

#### ⚑ F.2c · THE THREE UNGRADEABLE EXACT ROWS — **each given its closing condition**

⚑ **The consequence a grader must not let pass silently, restated: a repair pass that fixes only the
reds lands on `INDETERMINATE`, and `INDETERMINATE` trips the cap just as hard. All five must close.**

| row | v1.4 state | ⚑ **v1.5 closing condition** | state after drax's landed repairs |
|---|---|---|---|
| **`TA-X-01`** | ⚑ **UNGRADEABLE — no probe existed.** `P-2` runs `M-POL-2` s0 twice **with a fold inserted**; the harness conceded it | ⚑ **A genuine repeat probe: ANY arm, ANY salt, run twice with NOTHING inserted, byte-exact — and the emission NAMES the arm and the salt, which MUST DIFFER from `P-2`'s (`M-POL-2`, salt 0).** ⚑ **The name requirement is the row: without it, `TA-X-01` and `P-2` could silently rest on one execution path, and two rows resting on one path are one row** | ⚑ **CLOSES.** drax exercised it *"on a deliberately different arm/salt from P-2's"* (KP-44) — **emission still owed** |
| **`TA-X-15`** | ⚑ **UNGRADEABLE — no value emitted**, and census `M4` was mapped `IMPLEMENTED` with **no implementation** | ⚑ **SPLIT INTO TWO CLAUSES, because they are two different kinds of fact.** **(a) POSITIVE, MEASURED:** the realised release schedule is **emitted** — p01–p04 at `t = 0.0`, **p05 one burst at `t = 4.000 s`** *(= tick 49 at 12.2 ticks/s)*. **(b) NEGATIVE:** **no intra-point stagger** | ⚑ **(a) CLOSES** — implemented, p05 at tick 49 (KP-44). ⚑ **(b) IS `GREEN-BY-CONSTRUCTION`, NOT MEASURED** — drax reports the stagger **"unrepresentable rather than merely absent"**, i.e. the structure cannot express one. **It must print that, per § F.5 cl. 6.** ⚑ **This is the FOURTH structural zero in the run and the first one caught BEFORE a grader had to name it** |
| **`TA-X-16`** | ⚑ **GREEN on the declared value · UNGRADEABLE on enforcement.** `p06: false` at **`MODULE-DEFAULT`** precedence with **one consumer** (a required-key list); the board rolled **spawn_point 6 in 7 of 10 waves** | ⚑ **THE IDENTITY QUESTION IS ANSWERED BEHAVIOURALLY, BY TWO INDEPENDENT ROUTES THAT AGREE — and it needed no ruling.** gamora's pack recomputation gives **54 picks at p06 ON** and **47 at p06 OFF**; drax's port gave **54 picks pre-fix** and **47 post-fix**. ⚑ **Assert, under `p06: OFF`: `n_pool_picks == 47`, `n_spawn_point_6_keys_rolled == 0`, and a COUNTER for the filtered keys** — *a filter with no counter is indistinguishable from a filter that never fired* | ⚑ **CLOSES.** drax's repair landed (KP-44); it was ⚑ **a real defect nobody had listed.** **Emission owed.** ⚑ **The NOMINAL question — is "spawn point p06" the same OBJECT as "p06 bonus spawns" — is left unadjudicated on purpose: the row grades BEHAVIOUR, and behaviour is settled** |

#### ⚑ F.2d · `TA-X-07` — **THE TOLERANCE, SPECIFIED**

**v1.4 said `1e-6` and did not say which. It was graded ABSOLUTE — correctly, because the text's own
citation chain (§ D → P-a § E-2's *"module tolerance 1e-6"*, a CITATION not an adjective) routes to
an instrument reading `abs(residual) <= 1e-6` with no reference to `offered`.** ⚑ **That grade STANDS.
`Q83(c)` is untouched. Nothing here widens a graded instrument.**

**The arithmetic, which is the reason the tolerance was doing the wrong job:**

| | |
|---|---|
| observed residuals | `1.07 – 1.699e-6` on an `offered` near `1.0e8` |
| relative | ⚑ **all 25 cells `\|rel\| ≤ 1.6e-14`** |
| `ulp(1.0e8)` in float64 | **≈ 1.49e-8** |
| ⚑ **the worst residual, in ulps** | ⚑ **≈ 114 ulps** |

⚑ **114 ulps on a sum of thousands of terms is float64 ACCUMULATION. It is not damage created, and a
tolerance that cannot tell those apart is measuring the wrong thing.**

**v1.5's construction — three clauses, and the third is what stops it being a chosen number:**

| clause | assertion |
|---|---|
| ⚑ **(a) GRADED — RELATIVE** | `\|residual\| / max(1.0, \|offered\|) ≤ **1e-12**` |
| ⚑ **(b) REPORTED, NOT GRADED — ABSOLUTE** | `\|residual\|` printed **with `offered` beside it**, every cell, so the absolute magnitude never disappears behind a ratio |
| ⚑ **(c) THE ACCUMULATION BUDGET — the clause that makes `1e-12` CHECKABLE rather than CHOSEN** | `1e-12 ≈ 4.5e3 × float64 eps (2.220446e-16)` — **an accumulation-depth budget of ~4,500 terms.** ⚑ **The runtime EMITS the realised number of terms summed into `offered`. If the realised depth EXCEEDS 4,500, the row is `UNGRADEABLE`, not green** — because the tolerance was sized for a depth the run exceeded |

> ⚑ **Why `1e-12` and not `2e-14`.** `2e-14` would be **fitted to the observation** — the exact thing
> Law 3 forbids, and the exact thing drax's refusal to fit toward `183.58` proved the value of.
> **`1e-12` comes from the ARITHMETIC (eps × a declared depth budget) and the observed worst case
> sits 62× inside it.** ⚑ **A tolerance derived from the machine and checked against the realised
> depth is falsifiable; a tolerance derived from the data is a restatement of the data.**
> ⚑ **And the assert-wall gap is carried, unchanged:** the row names **SEVEN** quantities and the
> live driver assert-wall checks **SIX**. **The wall is not the row.**

#### ⚑ F.2e · `TA-X-06` — **CARRIED AS CLASSED, WITH THE EVIDENCE ON ITS FACE**

⚑ **`Q83(b)` IS OPEN. Matt has not ruled it** (KP-49 ruled F1–F5; `canonical/matt_decision_needed/README.md`
row `Q83` records *"(b) and (c) REMAIN OPEN"*). **The row is therefore carried at v1.5 EXACTLY AS
CLASSED — `EXACT`, distinctness D, relation only.**

⚑ **WHY I AM NOT RECLASSING IT HERE, EVEN THOUGH v1.5 IS A FRESH INSTRUMENT AND I COULD.**
Reclassing it in v1.5 while `Q83(b)` asks Matt to reclass it in v1.4 would **moot** the question
rather than answer it — **and this run has already paid for that failure mode once.** The standing
corollary (`CLAUDE.md`, the mooted-escalation ruling): *an escalation overtaken by events still
requires a disposition; "resolved by supersession" is a legitimate disposition and takes one line;
silence is not.* ⚑ **ONE RULING MOVES BOTH VERSIONS. If Matt rules `TA-X-06` UNGRADEABLE-declared,
it moves in v1.4 for the record AND in v1.5 for the instrument, and § I OQ-1 says so.**

**gamora's evidence, restated because the next grader must not have to reconstruct it:**

| arm | `avoidance` | clamps player | clamps body | ⚑ `n_avoidance_vetoes` | ⚑ `n_pool_occupancy_ticks` |
|---|---|---:|---:|---:|---:|
| `W1` | True | **0** | **0** | ⚑ **2** | 0 |
| `W1-NULL` | True | **0** | **0** | **0** | 0 |
| `W1-PROBE` | **False** | **0** | **0** | **0** | ⚑ **2** |

1. ⚑ **The WALL contributes NOTHING to the oracle's `W1`-vs-`M-POL-2` distinction.** Its clamp
   counters are **zero on every arm.** The only counter that separates `W1` from `W1-NULL` is
   **`n_avoidance_vetoes`, 2 against 0.**
2. ⚑ **So the distinctness is carried ENTIRELY by the avoidance limb** — the limb with **no published
   trigger rule**, on a boundary `ABS-ARENA-BOUNDARY` declares absent, in a cell `V8-CELL-1` says ran
   **wall-less**.
3. ⚑ **`W1` shows 2 vetoes / 0 occupancy; `W1-PROBE` — the same configuration with `avoidance =
   False` — shows 0 vetoes / 2 occupancy. An exact complementary pair.** The limb **vetoes entry into
   the pool region**; without it the same two ticks are spent occupying it. ⚑ **That tells us the
   limb's EFFECT. It does not tell us its TRIGGER** — and without the trigger the effect cannot be
   reproduced.
4. ⚑ **THE MIS-CLASS, PRECISELY:** `TA-X-06` was classed **EXACT** while **the only mechanism that
   makes its relation true was classed `TA-B-14` — report-only, *"oracle values 0–2"*, no width, no
   trigger rule, nothing owed — SEVEN LINES AWAY IN THE SAME DOCUMENT.** ⚑ **An EXACT row built on
   an input the same prereg declared unspecifiable.** That is not a judgement call that went the
   wrong way; **it is two rows in one file that cannot both be right.**
5. ⚑ **The evidence was on the record BEFORE v1.0 existed.** P-a Addendum 2 § A2 — **the file the
   prereg pins as `P-a`** — printed the `2`-vs-`0` vetoes **in the same table as the `0/0` clamps**,
   and its own caveat says *"a port with no wall at all also scores zero."* ⚑ **v1.0 quoted that
   caveat at `TA-X-11` and did not apply it to `TA-X-06`, one row above.**
6. ⚑ **THE CONSEQUENCE: the row is unfalsifiable in the honest direction. The only route to green is
   to invent a veto rule — and then the row is green about a rule nobody wrote.** A row that can only
   be passed by invention is not an EXACT row; **it is a trap for the conscientious builder.**
7. ⚑ **drax's call was correct and the record says so.** He declared the absence, routed it, named
   the consequence in the code comment, in the emitted absence ledger, and in the relation row's own
   `why`, and **did not fill it.** Given a choice between a true red and a green about a fiction he
   **chose the true red** — and at KP-44 he made that red **legible from inside the runtime** by
   formally declaring `arena_fold :: avoidance` unconsumed against `ABS-ARENA-AVOIDANCE-MECHANISM`.
8. ⚑ **What a reclass must NOT do, flagged so it is not discovered later: striking `TA-X-06` does not
   make anything PASS.** `TA-X-07` was independently red and `TA-X-01`/`TA-X-15` independently
   UNGRADEABLE. **The verdict survives the removal of the row most likely to be challenged.**

### F.3 · DIAGNOSTIC rows — **19 ids, 0 gating**

⚑ **Every diagnostic prints five fields beside its value, per § F.5: `value` · `@ coverage k/89` ·
**grain pair (numerator / denominator)** · **calibration range** · **dilution factor at this run's
ticks-per-wave.** A diagnostic printed without those five fields is a number without an instrument.

#### CLASS I · ⚑ **MECHANISM — the per-wave restatements** *(NEW ids; widths OWED)*

| id | statistic | numerator grain | denominator grain | confounded? | **width** |
|---|---|---|---|---|---|
| ⚑ `TA-B-16` | **released ticks PER WAVE** *(restates `TA-B-07` / `TA-B-02`)* | per-wave | per-wave | ⚑ **IMMUNE by construction** | ⚑ **OWED — gamora. NAMED AND EMPTY** |
| ⚑ `TA-B-17` | **stationary ticks PER WAVE** *(restates `TA-B-03`)* | per-wave | per-wave | ⚑ **IMMUNE by construction** | ⚑ **OWED — NAMED AND EMPTY** |
| ⚑ `TA-B-18` | **motion-suppressed ticks PER WAVE** — `CHANNELLING` (stationary ∧ channelling) *(restates `TA-B-09`)* | per-wave | per-wave | ⚑ **IMMUNE by construction** | ⚑ **OWED — NAMED AND EMPTY** |
| ⚑ `TA-B-19` | ⚑ **TICKS PER WAVE — `D / n_waves`, per salt** | per-tick | per-wave | ⚑ **IT IS THE DILUTION FACTOR ITSELF** | ⚑ **OWED — NAMED AND EMPTY** |

> ⚑ **THE CONSTRUCTIONS ARE VERIFIED COMPUTABLE ON BOTH SIDES, AND I VERIFIED THEM — WITHOUT MINTING
> A WIDTH.** The oracle side needs no new emission: `n_waves` is in the seal and `D` is constructible
> from the census block (§ C). Worked from the seal's own published per-salt figures:
>
> | salt | `D` | `n_waves` | `1 − uptime` | **released ticks** | **released / wave** |
> |---|---:|---:|---:|---:|---:|
> | 0 | 1084 | 6 | 0.095941 | **104** | 17.333 |
> | 1 | 305 | 2 | 0.104918 | **32** | 16.000 |
> | 2 | 106 | 1 | 0.216981 | **23** | 23.000 |
> | 3 | 185 | 1 | 0.086486 | **16** | 16.000 |
> | 4 | 1103 | 6 | 0.099728 | **110** | 18.333 |
>
> ⚑ **Mean-of-salts = 18.1333 — which reproduces gamora's published figure EXACTLY**, and the
> coefficient of variation reproduces her **0.1595** exactly. **The same route on stationary ticks
> (`1 − frac_moving`) returns [154, 45, 16, 22, 169] and reproduces her CV of `0.2004` exactly**, and
> on motion-suppressed ticks returns **[113, 33, 10, 18, 113], which SUMS TO 287 — the seal's own
> pooled `CHANNELLING`.** ⚑ **Three independent reproductions of her figures from the seal. The
> construction is unambiguous and it is computable today.**
> ⚑ **I STOP HERE. I do not compute `s`, a half-width, or a band.** The widths are gamora's to mint
> in a new P-a addendum; **this document carries decision rules and mints no width.**
>
> ⚑ **AND THE CLAUSE THAT MUST TRAVEL WITH THEM (§ C.6):** these four rows are **SCALE-FREE BY
> CONSTRUCTION, NOT BY MEASUREMENT.** The oracle's calibration range is still **ticks-per-wave ∈
> [106, 185]**, and **that range cannot test the claim.** ⚑ **Swapping one un-audited invariance
> claim for another is how this defect would survive its own repair. `TA-B-19` is the row that can
> falsify it, and that is why it exists.**
>
> ⚑ **What `TA-B-16` buys, in gamora's own demonstrated numbers:** released ticks **per tick** gives
> oracle `0.120811` against port `0.024430` — a **5× miss**; released ticks **per wave** gives
> `18.1333` against `11.76` — a ⚑ **1.5× miss, on a port whose Type-A limb is entirely absent.**
> *It stops charging the port for surviving and starts charging it for the thing that is actually
> wrong.* **No sealed cell is re-run, so `K-7` does not block it.**

#### CLASS II · ⚑ **CARRIED AS WRITTEN — the per-tick originals, with the confound printed**

`TA-B-02` · `TA-B-03` · `TA-B-04` · `TA-B-05` · `TA-B-07` · `TA-B-08` · `TA-B-09` — **7 ids.**

⚑ **Retained deliberately, and the reason is not sentiment: run #1's numbers exist in these forms,
and striking them would make the two runs incomparable.** They are carried **with P-a's widths
unchanged** — ⚑ **no width is adjusted by this document, in either direction** — and each prints,
mandatorily:

* its **grain pair** and whether it is confounded, from gamora's Addendum 2 § B2 enumeration
  (`TA-B-02` YES/UP · `TA-B-03` YES/UP · `TA-B-04` YES/UP-to-clip · `TA-B-05` WEAK/INDETERMINATE ·
  `TA-B-07` YES/DOWN · `TA-B-09` YES/DOWN · `TA-B-08`'s **sign may survive, its margin 0.0048 does
  not**);
* its **calibration range** — *"derived at ticks-per-wave ∈ [106, 185]"*;
* the **dilution factor at this run's realised ticks-per-wave**, from `TA-B-19`.

⚑ **AND TWO SENTENCES THAT MUST APPEAR VERBATIM WHEREVER THESE ARE PRINTED:**
1. ⚑ ***"`TA-B-02` and `TA-B-07` are ONE ROW WITH A SIGN FLIP (`released/D ≡ 1 − uptime`, exactly).
   They are not two pieces of evidence."***
2. ⚑ ***"`TA-B-02`'s green in run #1 rests on the CLIP. The unclipped upper bound is `0.974330` and
   the port's `0.975570` EXCEEDS it by `+0.001240`."*** *(No width was adjusted to produce that
   sentence and none may be adjusted to erase it.)*

#### ⚑ F.3a · CLASS III · `TA-B-06` — **THE CONSTRUCTION, DERIVED AND SPECIFIED**

⚑ **gamora declared the window under-specification as her own defect. It was deeper than she said,
and closing it was possible from the numbers already published.**

**What v1.4 and P-a actually said:** *"plant ratio (window 5.0 s)"* and *"(window 5.0 s /
fight-wide)"*. ⚑ **Neither the STATISTIC nor the WINDOW is defined anywhere in the corpus.**

**What the seal's own numbers say — reconstructed this session and reproducing on ALL FIVE SALTS:**

| salt | `n_window` (seal) | `D` | stationary ticks **in window** | in-window stationary rate | overall stationary rate | **ratio** | P-a's published value |
|---|---:|---:|---:|---:|---:|---:|---:|
| 0 | 366 | 1084 | **75** | 0.204918 | 0.142066 | **1.44241** | 1.442410 ✓ |
| 1 | 122 | 305 | **22** | 0.180328 | 0.147541 | **1.22222** | 1.222222 ✓ |
| 2 | 61 | 106 | **11** | 0.180328 | 0.150943 | **1.19467** | 1.194672 ✓ |
| 3 | 61 | 185 | **8** | 0.131148 | 0.118919 | **1.10283** | 1.102832 ✓ |
| 4 | 366 | 1103 | **82** | 0.224044 | 0.153218 | **1.46225** | 1.462250 ✓ |

> ⚑ **THE DEFINITION, RECOVERED:**
> `plant_ratio = (stationary ticks inside the measured window / window length in ticks) ÷ (stationary ticks over the whole fight / D)`
> — **a ratio of two stationary fractions**, with the window **61 ticks per wave** (5.0 s at
> **12.2 ticks/s**), so `n_window = 61 × n_waves`. ⚑ **Every stationary-in-window count it implies is
> an integer** (75, 22, 11, 8, 82), which is the check that it is the right reconstruction and not a
> curve fit.

⚑ **AND THE FINDING THIS EXPOSES, WHICH IS BIGGER THAN THE WINDOW GRAIN.** On the **port** side, the
published values times the port's own window counts return integers too — **40/83, 37/77, 37/80,
34/78, 37/76, all exact.** ⚑ **So the port computed the FRACTION OF 5-SECOND WINDOWS CONTAINING A
PLANT.** The oracle computed a **ratio of two stationary rates.**

> ⚑ **`TA-B-06`'s red in run #1 does not localise a fidelity failure at all. The two sides computed
> DIFFERENT STATISTICS.** ⚑ **And the symbol itself carried the ambiguity: the oracle's `n_window` is
> a TICK COUNT (61 per wave) and the port's `n_windows` is a WINDOW COUNT (`D / 61`). One name, two
> dimensions** — *the `0.215`-vs-`0.217` tell in a new costume, and this project's standing proof of
> what one shared name costs.*

**v1.5's specification:**

| clause | ruling |
|---|---|
| **the statistic** | ⚑ **the ratio of stationary rates above, stated in full, on both sides** |
| **the window** | ⚑ **61 ticks per wave, anchored at wave start — the ORACLE's grain** *(the port's whole-run tiling was a defensible reading of an under-specified construction, and it is superseded, not blamed)* |
| **the emission the port owes** | ⚑ **stationary ticks within the first 61 ticks of each wave, per salt** — a new counter; **stream-neutral by construction, because a counter consumes no draw** |
| ⚑ **the window's own coverage** | ⚑ **MANDATORY on the face, BOTH SIDES: `window_coverage = 61 / (D / n_waves)`.** Oracle ≈ **0.377** (range 0.330–0.575); port ≈ **0.126** |
| ⚑ **the residual confound, DECLARED rather than repaired** | ⚑ **THE STATISTIC IS IMMUNE AND ITS WINDOW IS NOT.** A **5.0-second** window is **absolute time** (§ C.6's fourth grain) and its coverage of a wave dilutes by the same `2.985×`. **If stationary ticks are not uniformly distributed within a wave — and plants happen on engagement, so they are not — the two sides sample different parts of the wave.** ⚑ **I do not correct this by making the window elastic: a "plant" is a five-second BEHAVIOUR and an elastic window would make five seconds mean different things on the two sides.** The coverage is printed instead, and the row stays a **diagnostic** |
| **the width** | ⚑ **P-a's `[1.0052, 1.5646]` was derived on this same statistic and stands as the ORACLE-side reference — but a PORT value cannot be compared against it until the port emits the corrected construction.** ⚑ **NO NEW WIDTH IS MINTED HERE** |

#### ⚑ F.3b · CLASS IV · `TA-B-15` — **SUBSTRATE, NOT PORT** *(carried; promotion permanently barred)*

**It measures the SUBSTRATE.** The NO-DATA fraction is a property of *the records POOL-466 happens to
contain*, which the port neither chooses nor influences. ⚑ **A fidelity band over it would score the
port on the oracle's data coverage — that is the `TA-B-13` mistake in a new costume.** It is the
**only structurally clean band in the whole set** (numerator and denominator are both BODIES) **and
it is the one that measures the substrate rather than the port** — a fact worth sitting with.

**What it prints, per arm per salt:** the **count**, the **fraction of bodies**, the **pool-pick
count**, and **both reference points labelled as what they are.**
⚑ **THE ANALYTIC REFERENCE POINT IS UNDER REPAIR.** `0.3828` / `0.6172` rest on `P-e` Addendum § 3,
**whose `E[bodies] = 183.58` does not reproduce from the pack and is withdrawn.** ⚑ **The corrected
body counts are `137.58` (p06 ON) and `126.08` (p06 OFF, the config of record); the corrected
COVERAGE FRACTIONS are OWED — gamora's `P-e` Addendum § 3 re-derivation. NAMED AND EMPTY. A report
must print `[owed]`, never `0.3828`.**
**A salt reporting ZERO is the anomaly, not a salt reporting many** — and at the salt level a zero is
a flag for investigation, never a red.

#### CLASS V · **NON-DISCRIMINATING BY CONSTRUCTION** — `TA-B-01` · `TA-B-13` · `TA-B-14`

| id | why it cannot discriminate | mandatory sentence |
|---|---|---|
| `TA-B-01` terminal wave | its band **admits every arm in the seal, including the `M-POL` G5 control the run built to be different** | ⚑ ***"`BAND / NON-DECISIVE / REPORT-ONLY`. A terminal wave inside or outside this band is not evidence of fidelity either way."*** ⚑ **And run #1 retired any reading of it as a near-miss: `[160 × 5]` is not "four waves past the band", it is THE LADDER RUNNING OUT** |
| `TA-B-13` `max_body_radius_m` | an **extreme over n draws**, not a mean; the per-salt sample is **degenerate (4 of 5 identical)**; ⚑ **its own t-band REJECTS the oracle's observed maximum** | ⚑ ***"A band that rejects the oracle cannot grade a port."*** Its falsifying power sits entirely in `TA-X-10` / `TA-X-11`, both EXACT |
| `TA-B-14` vetoes / occupancy | raw counts, oracle values **0–2**, no denominator | ⚑ ***"This is the counter that carries `TA-X-06`'s ENTIRE MECHANISM, and it is the one the prereg declined to band."*** § F.2e |

#### CLASS VI · **NO ORACLE SIDE** — `TA-B-10` · `TA-B-11` · `TA-B-12`

| id | state at v1.5 |
|---|---|
| `TA-B-10` per-wave durations | ⚑ **UNGRADEABLE AT THE PER-WAVE-VECTOR GRAIN, AND THE ROW WAS WRITTEN AT THE WRONG GRAIN.** The port emits `per_wave_durations` (10 rows/salt, with `ticks`, `bodies`, `coverage`, `pool_picks`); **the seals carry `terminal_wave` / `terminal_reason` / `n_waves` and no per-wave `duration_s`.** ⚑ **BUT THE AGGREGATE FORM HAS AN ORACLE SIDE AND ALWAYS DID: `D / n_waves` is constructible from the seal's census block, and gamora derived exactly that to get `161.6`.** ⚑ **THE ONE STATISTIC THAT WOULD HAVE MEASURED THE CONFOUND WAS AVAILABLE ALL ALONG AND THE ROW ASKED FOR IT AT A GRAIN THE SEAL DOES NOT PUBLISH.** ⚑ **That is `TA-B-19` and it is why `TA-B-19` exists.** `TA-B-10` stays UNGRADEABLE at its own grain; **what would close it is a sealed emission carrying per-wave `duration_s`, which does not exist and which `K-7` forbids manufacturing** |
| `TA-B-11` arrival latency / co-arrival / `n_deferred` | **absent from both seals — and now absent from the port too**: no arrival limb exists (`TA-X-19`). ⚑ **Structurally the cleanest pair of grains in the set, and no referent** |
| `TA-B-12` intake by wave and family; **leech per tick** | ⚑ **`leech`, `intake`, `damage_total` return ZERO keys on BOTH seals**, re-swept at the grade. The port emits all three richly. ⚑ **Ceiling `C-e`: THE LARGEST DIVERGENCE IN THE RUN IS INSIDE THIS UNGRADEABLE ROW.** What would close it: **a sibling that emits the oracle-side sustain statistics** — nothing else can |

### F.4 · Emitted, not graded

Per-registered-site draw counters (**29 live sites**; they localise nothing without S5) · the
tick-resolution HP trace.

### F.5 · ⚑ REPORT-FACE RULES

1. **Every diagnostic prints `value @ coverage k/89`** — a **rule** coverage (`P-1`), *not* a
   population coverage (§ C.5).
2. ⚑ **EVERY ROW KEYED BY WAVE PRINTS ITS OWN COVERAGE.** Coverage is **not uniform across waves**:
   the analytic runs from **`0.2999` at wave 157** to **`1.000`** at several; the empirical cell gives
   **`0.471` at wave 155**. **A per-wave row on a thin wave would otherwise read as if it rested on
   the pooled base.**
3. ⚑ **AND IT PRINTS THE NUMBER OF POOL PICKS BEHIND IT, NOT ONLY THE BODY COUNT.** Under clustering
   — **median 3 bodies per pool-alternative pick, max 9** — the body count **overstates the evidence
   by the design effect.** ⚑ *A wave at 0.30 over 4 picks and a wave at 0.30 over 20 picks are not
   the same claim.* **Run #1's per-wave table had 4–6 picks on every wave: no per-wave figure rested
   on more than six independent draws, and the body counts made two of them look very different.**
4. **Wave labels are not assumed to be total.** A per-wave denominator and a whole-fight denominator
   do not sum to the same population, and the report says so rather than letting the difference
   surface as an unexplained residual.
5. ⚑ **NEW — EVERY DIAGNOSTIC PRINTS ITS GRAIN PAIR, ITS CALIBRATION RANGE, AND THE REALISED DILUTION
   FACTOR.** *"numerator per-wave / denominator per-tick · derived at ticks-per-wave ∈ [106, 185] ·
   realised 482.4 · dilution 2.985×."* ⚑ **This is `WARN-6`'s lesson — a correction belongs where the
   rule is READ — applied to a PRECONDITION instead of to a correction.** ⚑ **And for `TA-B-16…19` the
   field reads *"SCALE-FREE BY CONSTRUCTION; the calibration range [106, 185] cannot test this."***
6. ⚑ **NEW — EVERY EXACT ROW SATISFIED BY AN ABSENCE PRINTS THE ABSENCE.** A `GREEN-BY-CONSTRUCTION`
   or `GREEN-VACUOUSLY` verdict must name **what is absent** and **why the other value is
   impossible.** ⚑ **The run found this class FOUR TIMES, separately, and named it late each time:**
   `TA-X-11` (*a port with no wall also scores zero*) · `TA-X-12` (the aprons are **ABSENT**, not
   present-at-zero — *a zero satisfied because the pilot never entered is a structural zero wearing a
   measurement's badge*) · `TA-X-19` (**no arrival limb at all** — and therefore `TA-X-21`'s `CEIL`
   assertion is **asserted in a vector table and never exercised**) · `TA-X-15(b)` (**the stagger is
   unrepresentable, not absent**). ⚑ **Also: `TA-X-17` is `GREEN-BY-CONSTRUCTION` with a named
   mechanism and the prereg asked for a per-body aggregate the emission does not carry — a
   report-face gap, not a red, and the rule makes it visible.**
7. ⚑ **NEW — THE SUSTAIN SENTENCE, MANDATORY ON ANY T-A REPORT UNTIL `C-e` CLOSES:**
   ⚑ ***"T-A cannot see the largest divergence in this run. `leech` and `intake` have no oracle side,
   the port is `terminal_reason = cleared` on 25/25 with HP never below 79.44 %, and the oracle is
   `player_death` 20/20. A GREEN T-A IS CURRENTLY COMPATIBLE WITH AN UNKILLABLE PLAYER."***

---

## § G · FAIL TAXONOMY AND THE T-B QUOTING CAP — **rebuilt under F5**

| verdict | antecedent | consequence |
|---|---|---|
| **`STRUCTURAL`** | **≥ 1 EXACT row RED** | port is wrong; **no W4 until repaired**; cap **TRIPS**; increments the attempts counter |
| **`INDETERMINATE`** | 0 EXACT red, **≥ 1 EXACT UNGRADEABLE** (incl. `P-1`, `P-2`, `P-3` or ⚑ `P-4` red) | cap **TRIPS**; does **not** increment the counter |
| ~~`STATISTICAL`~~ | ⚑ **RETIRED — § G.1** | — |
| **`PASS`** | **all EXACT green; none UNGRADEABLE** | ⚑ **`PASS @ coverage k/89, 26/26 EXACT rows green, dilution <f>×` — never unqualified, and the dilution factor is part of the label** |

**Order:** `STRUCTURAL → INDETERMINATE → PASS`, stop at the first hit. ⚑ **No diagnostic appears in
any antecedent.** **A GRADED RUN** = one execution of the 5 × 5 matrix producing a conforming verdict
file; a port repair between attempts does not reset the counter. **No post-hoc widening, by anyone.**

### ⚑ G.1 · **WHERE F5 LOOSENS THE INSTRUMENT — DECLARED, NOT BURIED**

⚑ **Retiring `STATISTICAL` makes one case LOOSER, and a change table that only lists its tightenings
is a sales document.** Under v1.4, a port with **all EXACT green and one counted band red** was
`STATISTICAL` — *a finding; handoff proceeds; cap does not trip.* ⚑ **Under v1.5 that same port is
`PASS`.**

**Why that is nevertheless correct, and it is F5's own argument:** ⚑ **at `T = 482` the counted bands
could not tell a faithful port from an unfaithful one.** A verdict issued by an instrument that
cannot discriminate is **not a weak signal — it is no signal wearing a verdict's badge**, and it
produced **false positives** (two rows that cannot fail, inflating `n/6`) **and false negatives**
(two that cannot pass) **in the same run.** Removing it removes both.

⚑ **AND THE COMPENSATING TIGHTENINGS, SO THE LEDGER BALANCES ON THE FACE:**
1. **EXACT grows 24 → 26** — two rows covering defects that cost the run a **3.754× over-heal** and a
   **live wave-1 stream-desynchronisation hazard**, neither of which any band could ever have seen.
2. **A fourth precondition (`P-4`)**, and `C1` already makes its mismatch trip the cap.
3. **Three UNGRADEABLE EXACT rows must CLOSE** — under the old taxonomy their `INDETERMINATE` was
   subordinate to a `STRUCTURAL` and could be read as a smaller problem. **It is not.**
4. **`PASS` must print the dilution factor in its own label**, so a pass at an un-calibrated fight
   length cannot be quoted as a clean one.
5. ⚑ **§ F.5 cl. 7 puts the unkillable-player sentence on the face of any report, including a
   passing one.**

**Verdict file** `kc2play.ta_verdict.v1`:

```
prereg_version                    : "v1.5"
prereg_sha256                     : <this file, derived at emission>
band_widths_sha256                : 7a5d4aa3…          (P-a)
galadriel_note_sha256             : 8186202c…          (P-b)
galadriel_expected_values_sha256  : a8b85331…          (P-c)
galadriel_release_labels_sha256   : 15dace60…          (P-d)
⚑ v3p3_prereg_sha256              : 27fc5937…          (P-e — REPLACED; v1.4's 97e5a4c7… was wrong)
⚑ v3p3_lifted_rows_sha256         : e51b54a1…          (P-f)
⚑ v3p2_lifted_rows_sha256         : e0117429…          (P-g)
⚑ model_pack                      : {dir: "…v3p3-20260921_022612", files: {…8 shas…}}   (P-h, NEW)
⚑ leech_resistance_csv_sha256     : cb6a008b…          (P-i, NEW)
register_sha256                   : <v0.3's MACHINE form, emitter-derived — never this document's file hash>
preconditions.P1_coverage         : {"mapped":89,"total":89,"unmapped":0,"refusals":<n>}
preconditions.P3_roll             : {"population":"POOL-466","cardinality":466,
                                      "law":{"alternative":"WEIGHTED:pool_weight","name":"UNIFORM:randrange"}}
⚑ preconditions.P4_pack           : {"dir":<name>,"files_verified":8,"mismatches":0}
v0_limb_set                       : <diffed line-by-line against V0>
⚑ join_consumption_audit          : [{join_id, consumed, call_site | declared_unconsumed_ref}, …]
⚑ draw_site_census                : {registered:29, short_circuits_found:0, degenerate_pairs:"97/139"}
⚑ conservation                    : {residual_abs, offered, n_terms_accumulated} per cell
nodata                            : {"refused":0, "spawn_inert":<n>, "measured_inert":<n>}  per arm per salt
⚑ diagnostics                     : [{id, value, coverage, grain_pair, calibration_range, dilution}, …]
```

**Cap — three refusal conditions, UNCHANGED:** **C1** verdict file absent / unparseable / **any
pinned sha mismatched** *(⚑ which now covers `P-h` and `P-i` without adding a condition)* · **C2**
`verdict ∈ {STRUCTURAL, INDETERMINATE}` · **C3** coverage not 89/89-mapped.
**"A fidelity figure"** (mechanical): a row pairing a twin statistic with a referent statistic; or a
ratio/percentage/delta/residual/score between them; or `fidelity`/`faithful`/`accuracy`/`match`/
`agreement`/`% of referent` in a label. ⚑ **`TA-B-15` is expressly NOT one** — it pairs a twin
statistic with a **substrate** statistic.
**Degraded behaviour:** raw twin-side statistics only, each with its own denominator and window; a
**banner before** the statistics naming the condition; **non-zero exit.**

### ⚑ G.2 · THE GRADED-RUN CAP — **v1.5 DOES NOT RESET IT**

**Graded run #1 exists** (v1.4, `STRUCTURAL`, counter = **1**). ⚑ **Matt F3: *the last graded run is
spent AFTER the decode lap and drax's repairs.* SINGULAR. ONE REMAINS.**

⚑ **The charter's definition — *"two attempts = two graded T-A runs against the same prereg
version"* — is VERSION-scoped, and reading that as licence would make v1.5 an evasion of the gate it
was authorized to improve.** ⚑ **A counter that resets whenever the run rebuilds its own instrument
is not a cap.** **The counter at v1.5 is RUN-scoped against the v3.3 reference and stands at 1.**
**§ H states the one thing that resets it, and why that is not the same evasion.**

---

## § H · ⚑ **THE RE-BASE (F2) — WHAT MUST BE RE-DERIVED BEFORE ANYTHING IS GRADED AGAINST IT**

> **Matt, KP-49: `F2 = re-base`.** ⚑ **This REVERSES the conductor's KP-32-era ruling that pinned the
> oracle to v3.3 while the decode fed `PLAY` only** — *"pinning preserved fidelity to a reference we
> have proven is systematically softer than the game."* **Both sides move onto the decoded substrate
> together.**
> ⚑ **I pre-compute nothing here.** The decode has not landed; every figure below is an obligation,
> not a value.

### H.1 · ⚑ K-7 IS NOT BREACHED, AND SAYING SO NOW PREVENTS AN ARGUMENT LATER

**K-7 forbids RE-RUNNING the three sealed v3.3 cells.** ⚑ **A re-base does not re-run them — it MINTS
A NEW SEALED SET.** The three v3.3 cells (`ad61ad2a…`, `20b05cb4…`, `7a992c81…`) **stay sealed,
un-re-run, and become the lineage.** **The new set carries new digests, new paths, and its own pin
table.** ⚑ **Any document that compares a v1.5 figure to a re-based figure is comparing across
epochs, and the register's TWO-EPOCH RULE already governs that: recordings under different hashes are
reported separately, never pooled.**

### H.2 · ⚑ SUBSTRATE-INVARIANT — carries across the re-base untouched

**Identities, geometry, quantisation rules, config assertions and language facts.**
`TA-X-01` (run-internal) · `TA-X-07` (identity; **the accumulation BUDGET may need re-sizing if the
richer board deepens the sum — § F.2d cl. (c) makes that self-reporting rather than silent**) ·
`TA-X-08` · `TA-X-12` · `TA-X-13` · `TA-X-14` · `TA-X-15` · `TA-X-17` · `TA-X-18` · `TA-X-19` ·
`TA-X-20` · `TA-X-22` · `TA-X-24` · `TA-X-27`(a)(b)(c) · `TA-X-26`(a)(b)(c)(d).
**The inertness/distinctness family `TA-X-03…06` is invariant IN FORM** — the relations are
port-to-port at one substrate — ⚑ **but every DIGEST they compare moves, so no digest may be carried
forward as a constant.**

### H.3 · ⚑ MUST BE RE-DERIVED — and `TA-X-25` must be RE-AUTHORED, not re-derived

| what | why it moves |
|---|---|
| ⚑ **`TA-X-25` — ALL THREE CLAUSES** | ⚑ **THIS IS THE ROW THE RE-BASE GUTS, AND IT IS THE BIGGEST SINGLE CONSEQUENCE OF F2.** Its whole mechanism is *"`ANCHOR-169` contains ZERO NO-DATA members while `POOL-466` contains 338."* **A decode that reaches the 338 collapses that count — possibly to zero — and `(c)`'s STRUCTURAL NON-ZERO INVERTS INTO A STRUCTURAL ZERO.** ⚑ **The row cannot be re-derived; it must be re-authored, and the successor may have to assert the opposite sign.** ⚑ **`§ F.1`'s class test decides it: can you name the mechanism that makes the other value impossible? If the answer after the decode is "it would be very unlikely", it is a DIAGNOSTIC and it leaves the EXACT set** |
| **the four population cardinalities** | `ANCHOR-169` and `BOTH-128` **are decode-coverage figures and both move — that is what the lap is FOR.** `ROSTER-790` and `POOL-466` are pack-structure figures and should not, ⚑ **but must be re-derived, not assumed: the decode lap could add records to pools** |
| **the honest-fail table (338 / 342 / 6 / 0)** | ⚑ **it is ENTIRELY decode coverage. It should COLLAPSE, and how far it collapses is the lap's headline result.** ⚑ **`C-d`'s grain question travels with it and gets cheaper, not harder** |
| `TA-X-26` clause **(e)** | ⚑ **anchored on the ARMED SET by design (§ F.2a). The armed set is what F2 enlarges.** `0.266406` and *"5 of 128"* are 128-record figures; over all 790 the same column gives `0.252215` and **48**. **Re-measure; do not carry** |
| `TA-X-27` clause **(d)** | the degenerate-pair census is read from the pack; **the pack is re-emitted ⇒ re-derive `139` and `97`** |
| `TA-X-09` · `TA-X-16` · `TA-X-21` · `TA-X-10` | the vectors, the pick count, the LIVE quantisation-site list and the arena supremum are all **pack properties**. ⚑ **Re-derive each; do not assume a monster-offense lift leaves them alone — VERIFY it** |
| `TA-X-11`'s margin | a property of the oracle's **realised** maximum; different bodies spawn ⇒ **re-measure** |
| `P-1`'s four-way counts | ⚑ **rows carried as `RUNTIME-CHOICE(absent_ref)` for absent monster offense may become `IMPLEMENTED`. The TOTAL stays 89; the COUNTS move** |
| ⚑ **EVERY WIDTH IN P-a. WITHOUT EXCEPTION.** | ⚑ **Every width is derived from the sealed `M-POL-2` cells' per-salt values. New cells ⇒ new per-salt values ⇒ EVERY WIDTH IS VOID.** ⚑ **Not one row of the tolerance half survives a re-base, and the calibration range changes with it — which, under § C.6, is the first chance anyone has had to test the scale-freeness claims at `TA-B-16…19`** |
| **the ceilings** | `C-b` (no cell validates waves 156–160) is **the one F2 can actually close.** `C-e` and `C-f` are **the ones it is most likely to EXPLAIN** — the conductor's read is that the `~29×` leech residual is plausibly dominated by the decode gap itself, **and it is testable the moment the decode lands** |

### H.4 · ⚑ THE GRADED-RUN CAP **RESETS AT A RE-BASE — BY CONSTRUCTION, AND UNDER ONE GUARD**

⚑ **The reset is structural, not a concession.** A re-based oracle is **a different reference
object**: every width is void, four EXACT rows need re-authoring, and one of them may have to assert
the opposite sign. **The two-attempts counter counts attempts at the SAME QUESTION. When the
reference moves, the question moves,** and a counter that carried across would be counting failures
against an instrument that no longer exists.

⚑ **AND THE GUARD THAT KEEPS THAT FROM BEING THE EVASION § G.2 REFUSES — it is the whole difference
between the two cases:**

1. ⚑ **The re-base was ruled FROM OUTSIDE THE RUN.** Matt's F2. **The run did not decide to reset its
   own cap by rebuilding its own instrument** — which is precisely what v1.5 would have been doing,
   and why v1.5 does not reset it.
2. ⚑ **The successor prereg (v2.0) is COMMITTED — alone, with every pin re-derived — BEFORE the
   re-based cells are graded.** D4. A prereg written after seeing the new reference's numbers is not
   a prereg.
3. ⚑ **The v1.4 and v1.5 attempts STAY ON THE RECORD as attempts against the v3.3 reference**, with
   their verdicts, and the successor's header names them. **A reset that erases its predecessors is
   not a reset; it is an amnesia.**
4. ⚑ **The re-base must be DECLARED IN THE HEADER of every artifact that crosses it**
   (`substrate_epoch`), so the two-epoch rule is mechanical rather than remembered.

⚑ **If any of those four is not true, the reset is not legitimate and the cap carries.** *(Stated as
the construction, with the guard; § I OQ-2 puts it to Matt as a one-word ruling, because a cap that
a document resets for itself is not a cap either.)*

---

## § I · OPEN QUESTIONS — **one lean each**

**OQ-1 · ⚑ `TA-X-06` — `Q83(b)` IS OPEN, AND ONE RULING MOVES BOTH VERSIONS.**
→ ⚑ **LEAN: reclass to `UNGRADEABLE-DECLARED`, in v1.4 FOR THE RECORD and in v1.5 FOR THE
INSTRUMENT, in one word.** The row is **unfalsifiable in the honest direction** — the only route to
green is inventing a veto rule nobody wrote — and it was classed EXACT while the only mechanism
making it true was classed report-only **seven lines away in the same file.** ⚑ **Nothing is rescued:
the cap trips either way, and v1.4's verdict survives the row's removal.** ⚑ **v1.5 carries it AS
CLASSED precisely so the ruling is not mooted by this document.**

**OQ-2 · ⚑ THE CAP RESET AT THE RE-BASE (§ H.4).**
→ ⚑ **LEAN: YES — the cap resets at a re-base, under the four guards at § H.4, and the reset is
YOUR word rather than this document's.** **v1.5 explicitly does NOT reset it** (§ G.2), so the
question is narrow: *does a new sealed reference start a new count?* ⚑ **The reason to say yes is
that every width is void and four EXACT rows need re-authoring — you would be capping attempts
against an instrument that no longer exists. The reason it needs your word at all is that a run which
can reset its own cap by rebuilding its own instrument has no cap.**

**OQ-3 · ⚑ `TA-X-07`'s TOLERANCE — `Q83(c)` is open for v1.4 and v1.5 specifies the form (§ F.2d).**
→ ⚑ **LEAN: hold v1.4's RED (do not widen post-hoc) and adopt v1.5's relative-with-budget form.**
The two are not in tension: v1.4's grade records what the instrument as written decided; v1.5's form
is pre-registered before any run against it. ⚑ **The budget clause is the part worth your attention —
it makes the constant falsifiable by the run itself rather than by argument.**

**OQ-4 · ⚑ THE PER-WAVE WIDTHS AT `TA-B-16…19` ARE OWED BY GAMORA AND THE SLOTS ARE EMPTY.**
→ ⚑ **LEAN: they are a new P-a addendum, derived from the seal, and they block nothing — because
under F5 no diagnostic gates anything.** ⚑ **The constructions are verified computable on both sides
(§ F.3b) and three of gamora's published figures reproduce exactly from them, so the derivation is
mechanical.** **I mint no width here and a document that did would be the goalpost-moving F5 exists
to prevent.**

**OQ-5 · ⚑ `P-e` ADDENDUM § 3's RE-DERIVATION IS OWED (the withdrawn `183.58`).**
→ ⚑ **LEAN: gamora re-derives the COVERAGE FRACTIONS, not just the body count** — `137.58` /
`126.08` are landed, but `TA-B-15`'s reference points (`0.3828` / `0.6172`) and ceiling `C-b`'s
expectation **rest on the withdrawn derivation**. ⚑ **Until it lands, `TA-B-15` prints `[owed]` and
never `0.3828`.** **Ceiling `C-c` is struck as void in the meantime (§ E.2).**

**OQ-6 · ⚑ THE `limitN` QUESTION IS UN-MEASURED, NOT ANSWERED.**
→ ⚑ **LEAN: re-open it at the re-base, not before.** `C-c` was struck because the shortfall it was
compared against (`183.58`) does not reproduce — ⚑ **but "the comparison was void" is not "the cap has
no effect", and collapsing those two would be the same error in the opposite direction.** A measured
pass over the capped config settles it, and the re-base is when that is cheap.

**OQ-7 · THE CHARTER STILL CARRIES `72` AND THE SUPERSEDED SIZING, LIVE-TENSE** (§ 4.3 / § 4.4 /
§ 3 F1 / § 9; KP-26's `229 / 297 / 302`).
→ **LEAN: annotate all of them forward in one pass, in the same strike-through form S-2 carries.**
**Propagation, not a new ruling — no Matt.** ⚑ **The sweep at § A.3 is the argument: the prereg and
register were clean, so every hour these figures still cost is charged entirely to the charter.**
**Companion: `OQ-3`'s `CHARTER_DENOMINATOR` rename, still owed — the constant's NAME is half the
defect.**

**OQ-8 · ⚑ `TA-X-11` / `TA-X-19` / `TA-X-12` / `TA-X-15(b)` ARE FOUR STRUCTURAL ZEROS AND § F.5 cl. 6
MAKES THEM PRINT — BUT PRINTING IS NOT CLOSING.**
→ ⚑ **LEAN: accept the print rule now and route the ARRIVAL LIMB as a real fidelity gap, separately.**
⚑ **The oracle has a deferred-arrival limb and the port has none at all** — `Kc2RtLaws.arrival_tick`
has zero call sites — which also means **`TA-X-21`'s `CEIL` assertion is asserted in a vector table
and never exercised.** **That is not a reporting gap; it is a missing limb wearing a green row.**

---

## § J · ⚑ THE DISCIPLINE THIS RUN PRODUCED

> ⚑ **BEFORE BANDING A RATE, NAME THE GRAIN OF ITS NUMERATOR AND OF ITS DENOMINATOR SEPARATELY, AND
> STATE THE RANGE OF THE RATIO BETWEEN THEM OVER WHICH THE BAND WAS CALIBRATED.**

**gamora's, proposed forward at grade Addendum 2 § B6 cl. 5. Recorded here in the instrument it
repairs, and routed to jack-ryan for ratification through the conductor.**

⚑ **It is the FOURTH instance this run of ONE shape — a statistic correct in its arithmetic and wrong
in the population or the scale it ranged over:**

| # | instance | whose |
|---|---|---|
| 1 | **σ over 97 BODIES when the draws are over 23 POOL PICKS** — design effect `√(97/23) ≈ 2.05×`, `z` **4.72 → 2.30**, and a *"mechanism I have not identified"* withdrawn | gamora |
| 2 | **`466 − |source|` — SUBTRACTION where it owed a SET INTERSECTION.** 41 of the 169 sit outside the 466; `229/297/302` → **338/342** | ⚑ **the conductor's** |
| 3 | **`183.58`** — an analytic that does not reproduce from the pack by the oracle's own law; **1.46× the correct figure**; a port exonerated and a ceiling voided | gamora |
| 4 | ⚑ **THE PER-WAVE/PER-TICK CONFOUND** — bands calibrated over ticks-per-wave ∈ [106, 185] and applied at 482.4, **2.6× outside the range, with nothing on their face saying so** | gamora |
| ⚑ 5 | ⚑ **NEW, FOUND WHILE WRITING THIS FILE** — `mean(adcth_mult_COUPLED)` is **`0.266406` over 128 ARMED records and `0.252215` over all 790`**; leech-immune records are **5** or **48** by the same fork. **Same file, same column, two populations, two answers** | ⚑ **surfaced here; the underlying figures are gamora's** |

⚑ **And the companion discipline, which is what actually kept instance 3 findable:** `#79` / Law 3 —
**drax declined to fit a multiplier toward `183.58`** on the grounds that *"one fitted to reach
183.58 would be fitted against the very figure it must be independent of."* ⚑ **The figure was
wrong.** In gamora's words: ***"had he fitted toward 183.58, my arithmetic error would now be a
constant inside the runtime and unfindable."*** **The strongest argument for the no-fitted-constants
rule this project has produced, and it arrived as a builder's refusal rather than as a gate.**

⚑ **The second discipline, mine, carried forward from KP-43 and already amended into `#75` cl. 1(a)
at KP-47:** ***nobody reads a pinned revision, they read the file. A pin is an audit instrument, not
a gate — it proves what a REVIEWER checked, never what a BUILDER used.*** **Remedy: a builder states
which revision he built against, and that statement is what a pin is checked against.** ⚑ **v1.5's
`P-h` is that remedy applied to the one artifact class that had no pin at all.**

---

*Filed 2026-09-21 by gandalf (named sub-agent, `SPEC-AUTHOR`), Run KC2-PLAY. **v1.4 / v1.3 / v1.2 /
v1.1 / v1.0 NOT edited; superseded readings named in place at § A.** **v1.4's grade of record —
`STRUCTURAL @ coverage 89/89` — does not move; nothing here regrades, rescues, widens or reclassifies
anything that was graded.** **Legal only because Matt ruled it (KP-49, F4 — his words on the face of
this document).** **All ten pins, both document-of-record hashes and all three sealed-cell digests
derived this session by `shasum -a 256`, never retyped — and one pin was REPLACED because it was
wrong, not stale.** ⚑ **NO BAND WIDTH MINTED. Three slots left named and empty for gamora
(`TA-B-16…19`'s widths, `TA-B-06`'s corrected port-side comparison, `P-e` Addendum § 3's coverage
fractions).** **K-7 held** — the three sealed cells were reached by digest and byte count only, never
opened, never re-run. **Law 3 held: every predicate in this file was run against the documents and
the substrate, never against recollection — and four of them (the degenerate-pair census, the leech
table's shape, the per-wave constructions, and `TA-B-06`'s definition) were re-derived rather than
transcribed.** No production code, no dispatch, no push.*
