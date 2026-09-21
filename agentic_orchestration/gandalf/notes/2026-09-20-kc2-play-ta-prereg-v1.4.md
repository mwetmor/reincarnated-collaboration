# KC2-PLAY · T-A PREREGISTRATION **v1.4** — decision rules, row decisiveness, FAIL taxonomy, denominator law, **and the roll population**

> ⚑ **STATUS: IMMUTABLE ON COMMIT — v1.4, 2026-09-20. SUPERSEDES v1.3 FORWARD.**
> **v1.3 (commit `66d2fc89`, file sha256 `75987c08…` — both derived this session, not carried), v1.2 (`72204f7a`), v1.1 (`30111ac8`) and v1.0 (`5f2c27cf`) are NOT edited.** Superseded readings named in place at **§ A**. ⚑ **No graded run exists against any version — re-verified this session, not assumed:** a recursive grep for `ta_verdict` across `reincarnated-collaboration/agentic_orchestration`, `reincarnated-engine/src` and `reincarnated-godot` returns **only the five prereg documents themselves**, and no file named `*ta_verdict*` exists in any of the three repos. That is the only reason a new version is legal (WARN-16). **Any change after a graded run exists is a HALT to Matt.**
> **Occasioned by:** charter ledger **KP-30** (Matt approves Q82; the § 1 substrate amended to admit the v3.3 monster-offense lift) · **KP-31** (the lift delivered; two conductor corrections; the refusal rule re-classed) · **KP-32** (⚑ **COMPOSITION RULED — T-A rolls from POOL-466**) · gamora's v3.3 prereg **and both of its addenda** (**P-e**).
> **Author:** gandalf (named sub-agent, `SPEC-AUTHOR`), Wave 1. **Decision rules only. NO WIDTH IS TRANSCRIBED HERE.**

### ⚑ PINS — **every pin re-derived this session by `shasum -a 256`, none retyped from a prior document**

*(The standing rule, born from my own double carry-forward defect at KP-20: a new version re-derives **every** pin it carries, including the ones it believes are unchanged, and prints them in one table. Three of the seven below were "believed unchanged" and one of those three had moved.)*

| # | artifact | **sha256** | what moved |
|---|---|---|---|
| **P-a** | `agentic_orchestration/gamora/notes/2026-09-20-kc2-play-ta-band-widths.md` — **the governing width file** | **`7a5d4aa3305ed14748a903b60ebfe48ac1a186fdb951fb6b8608abba92406750`** | ⚑ **MOVED AGAIN.** v1.3 pinned `1c971da9…`; **verified by `git show 16d1b6a7a:<path> \| shasum -a 256` → `1c971da9…`**, so v1.3's pin was exactly the Addendum-3 state and was correct when made. The file then moved at **`2339d631d` — the WARN-6 strike-through pointer at § E-3**, *not* at Addendum 3. **Content-innocent** (the annotation restates 72 → 89, which this prereg already governs); **pin-discipline-material** |
| **P-b** | `agentic_orchestration/galadriel/notes/2026-09-20-kc2-play-w1-tb-expected-values-and-u-rider.md` | **`8186202cc0c78ae9ef428c57164fac35bd1adb0e14ec5310c395783361653158`** | unchanged — **re-derived, not carried** |
| **P-c** | `agentic_orchestration/galadriel/notes/2026-09-20-kc2-play-w1-tb-expected-values.json` | **`a8b85331764ba3fe90f45cf7cd6f1a25f6dc0dae4a7e7fa555c487f0b153ea0b`** | unchanged — **re-derived** |
| **P-d** | `agentic_orchestration/galadriel/notes/2026-09-20-kc2-play-w1-tb-release-labels.json` | **`15dace604c8d5bb4888223a8b25a07a038bae44431ebd194d682545c0f29c58a`** | unchanged — **re-derived** |
| **P-e** | ⚑ **NEW** — `~/Games/reincarnated-engine/src/reincarnated/simulation/math/kc2-play-v3p3-monster-offense-prereg-2026-09-20.md` | **`97e5a4c7ad40f931946bcb1897c5b451fdb523066625834cd2ef5c543311c8c2`** | ⚑ **the governing document for § B.4, `TA-X-25` and `TA-B-15`. This sha covers the body AND both addenda** — the Addendum-2 σ correction is inside it |
| **P-f** | ⚑ **NEW** — `…/simulation/output/kc2-lifted-rows-KC2PLAY-v3p3-monster-offense-20260920_214408.json` (11,847,705 B) | **`e51b54a118f657ba7abd4298e5fcea86cfab3aeedebf8dd70a1239c5ea1b776e`** | ⚑ **the rows the port consumes for monster offense.** KP-31 recorded `e51b54a1…`; **independently derived here and it agrees** |
| **P-g** | ⚑ **PROMOTED FROM PROSE TO A PIN** — `…/simulation/output/kc2-lifted-rows-KC2PLAY-W1-v3p2-full-20260920_163932.json` (362,156 B) | **`e011742935f14efaba2e9eb45e7bca11e1131fc19d6f936526498d4f7ac1af96`** | v1.3 carried this as a bare prose prefix (*"Lifted rows: `e0117429…`"*) with **no pin row and no byte count** — the same class of gap BLOCK-2 closed for P-c/P-d. **Derived and pinned** |

### ⚑ SEALED CELLS — **VERIFIED THIS SESSION, and for the first time their PATHS are on the record**

**K-7 held: hash-verified only, never opened, never re-run.** v1.3 carried these three as recorded digest/byte-count pairs with **no path**, which made them un-re-derivable by the next reader — a pin you cannot re-derive is a transcription, not a pin.

| cell | path (`~/Games/reincarnated-engine/src/reincarnated/simulation/output/`) | sha256[0:16] **derived** | bytes |
|---|---|---|---:|
| `[M-POL2]` | `kc2-checkpoint-E-s09-cp150-mpol2-20260825_114420.json` | **`ad61ad2a8c799d6e`** | 123,564 |
| `[MECH]` | `kc2-checkpoint-E-s09-cp150-mech-20260816_124031.json` | **`20b05cb4ef3bd888`** | 2,125,271 |
| `[W1W]` | `kc2-checkpoint-E-s09-cp150-w1walls-20260825_220058.json` | **`7a992c81ca6e56e5`** | 403,084 |

**Companion register:** `2026-09-20-kc2-play-divergence-register-v0.3.md`.
**Counts:** **3 preconditions** · **24 EXACT** · **15 BAND ids — 6 COUNTED · 5 REPORTED-NOT-COUNTED · 0 CONDITIONAL · 4 UNGRADEABLE-DECLARED** · 2 emitted-not-graded.
**Standing law:** Law 3 · K-7 · D4 · GL-6 / GL-12 · Discipline #72 · R-L91-4 · D-MPOL2-2 · R-L89-4 · `L-49` · digests **derived at use, never retyped**.

---

## § A · CHANGE TABLE — v1.3 → v1.4

| # | clause | v1.3 | **v1.4** | reason | authority |
|---|---|---|---|---|---|
| 1 | **width-file pin** | `1c971da9…` | ⚑ **`7a5d4aa3…`** (P-a) | the file moved at the **WARN-6 annotation** (`2339d631d`). ⚑ **And the commission's own framing is corrected in place: it moved at WARN-6, not "again at Addendum 3."** v1.3's pin *was* the Addendum-3 state — proven by `git show` — so this is the third move of one file, not a re-statement of the second | jack-ryan WARN-6 residual |
| 2 | **the v3.3 substrate** | *(did not exist)* | ⚑ **PINNED — P-e, P-f** | the charter's § 1 substrate was **amended** to admit the monster-offense lift. A prereg that grades a port consuming rows it does not pin is outside its own immutability guarantee | **KP-30** (Matt) · **KP-31** |
| 3 | **v3.2 lifted rows** | bare prose prefix, no pin row, no byte count | ⚑ **P-g — derived and pinned** | symmetric with BLOCK-2's ruling on P-c/P-d: *a consumed artifact with no pin is outside the immutability guarantee entirely* | BLOCK-2, applied forward |
| 4 | **sealed cells** | three digest/byte pairs, **no paths** | ⚑ **paths named; all three digests DERIVED this session** | a pin the next reader cannot re-derive is a transcription. **K-7 is untouched** — hash-verify is precisely the permitted operation | K-7 |
| 5 | ⚑ **THE ROLL POPULATION** | *(absent — the prereg never said what the port rolls from)* | ⚑ **NEW § B.4 + precondition `P-3`: the port rolls from POOL-466, two-stage, WEIGHTED across pool alternatives and UNIFORM across names within the chosen pool** | **the largest silent hole in v1.3.** Every band compares monster behaviour; none of the three prior versions said **which monsters**. A port rolling ANCHOR-169 would have gone green on rows that were comparing different populations | **KP-32** · P-e § 1, Addendum § 1 |
| 6 | ⚑ **the conductor's "the roll is WEIGHTED"** | *(carried as premise in the commission, never in the prereg)* | ⚑ **SUPERSEDED IN PLACE: half wrong.** Weighted at the **pool-alternative** stage (`wave_engine.py:974 _weighted_pick`); **UNIFORM at the name stage** (`:849, :869 rng.randrange(len(roster_names))`) | modelling the referent's name-weighting without per-entry `limitN` would be **invention** (`UNREACHED-I22-1`); the oracle's own `_emit` docstring says so | **KP-32** · P-e Addendum § 1 |
| 7 | ⚑ **NEW EXACT ROW `TA-X-25`** | — | the **NO-DATA path**, three clauses (§ F.2b). **EXACT 23 → 24** | the composition ruling is only a ruling if something checks it. § B.4's declaration is self-reported; `TA-X-25(c)` is the behavioural check | **KP-32** |
| 8 | ⚑ **NEW BAND ROW `TA-B-15`** | — | **NO-DATA spawn count per arm per salt — REPORTED-NOT-COUNTED.** BAND ids **14 → 15**; REPORTED-NOT-COUNTED **4 → 5** | it measures the **substrate**, not the port, so it **cannot be a fidelity band**. Reported because a salt reporting **zero** is the anomaly | **KP-32** |
| 9 | ⚑ **THE REFUSAL DISCRIMINATOR IS DEAD UNDER `ORACLE`** | v1.3 was silent; **KP-26 and P-e § 5 (lines 421–425) both promise *"T-A must report refusals per salt; nonzero ⇒ that salt's stream rows UNGRADEABLE"*** | ⚑ **Under `ORACLE` refusal is FORBIDDEN, so the refusal count is `0` BY CONSTRUCTION and discriminates nothing. T-A cannot grade refusals at all.** The clause is superseded; `TA-X-25(a)` grades the `0` as an identity, and the surviving signal is `TA-X-25(c)` + `TA-B-15` | refusing the oracle's own eleven gives the port **fewer bodies than the cell the bands come from** | **KP-31** · **KP-32** · P-e Addendum § 5 |
| 10 | ⚑ **PER-WAVE COVERAGE** | *"every band prints `value @ coverage k/89`"* — **one number, pooled** | ⚑ **NEW § F.5: every row keyed by wave prints ITS OWN coverage AND the number of pool picks behind it** | coverage is **not uniform across waves** (analytic w157 **0.2999**, empirical w155 **0.471**, four waves at **1.000**). A band on a thin wave would otherwise read as if it rested on the pooled base | **KP-32** · P-e Addendum § 4, Addendum 2 § 4 |
| 11 | ⚑ **THE 4.7 σ GAP** | *(did not exist in v1.3; the commission carried it as* **unreconciled** *)* | ⚑ **RECORDED AS RESOLVED, NOT CARRIED AS A CEILING** (§ E.2) | ⚑ **The commission's item 5 is superseded by evidence that landed before this file did.** gamora's Addendum 2 refutes the census-bias hypothesis on three independent proofs, refutes the window-mismatch hypothesis by a count identity, and locates the defect in **her own σ** — quoted over 97 bodies when the independent unit is the **23 pool-alternative picks**. `z` falls **4.72 → 2.30`. She **withdraws** *"a mechanism I have not identified"* | P-e **Addendum 2 §§ 1–3** |
| 12 | **supersession sweep** | — | ⚑ **RUN AND RECORDED** (§ A.1) | the standing rule | — |

### ⚑ A.1 · SUPERSESSION SWEEP — run against the documents, not against recollection

| stale figure hunted | found live-tense in v1.3 / v0.2.1? | disposition |
|---|---|---|
| honest-fail sizing **229 / 297 / 302** | ⚑ **NO occurrences.** Those figures never entered the prereg or the register — they lived in **KP-26** and were corrected at **KP-31** | nothing to strike here; **the charter row is the one that needs the annotation** (§ H OQ-1) |
| *"the 169 the oracle rolled"* | ⚑ **NO occurrence.** The only `169` substrings in v1.3 are inside `θ 0.22972972972972974` and `0.7830189` | clean. The phrase is **the conductor's, in KP-26, and KP-31 already convicts it** |
| coverage **`k/72`** / `72/72` | ⚑ **NO live-tense occurrence.** v1.3's only `72`s are **Discipline `#72`**, the substring in **`47.072`**, and two explicit *"the charter still says 72 and is superseded-pending-annotation"* citations | correct as written; the charter annotation is still owed |
| **v1.3's own honest-fail numbers** | ⚑ v1.3 carried **none** — it never named a honest-fail count | **v1.4 introduces them for the first time, at the corrected values (§ B.4)** |

**The sweep's own finding:** *the prereg and the register were never the carriers of the stale sizing. The charter was, and still is.* Naming that precisely matters more than sweeping a file that was already clean — **a sweep that reports "clean" without saying where the defect actually lives has told you nothing.**

---

## § B · CONFIGURATION AND PRECONDITIONS

### B.1 · `ORACLE` — v3.2 `V0`, five arms, five salts

`V0` carries five `V0-ARM-*` rows — `M0`, `M-POL-2`, `M-POL-2-NULL`, `W1`, `W1-NULL` — each a **DELTA against the base row set, never a second full copy**. **5 arms × 5 salts = 25 headless runs**, each arm the base set with **exactly one fold moved**: that single-fold delta is the entire reason the inertness relations are readable, and it is why `W1-NULL` returns to **`M-POL-2`** rather than to `M0` (`TA-X-04`).

Limbs of record include `spawn_fold: POLAR_UNIFORM_RHO` · `sustain: COUPLED` · `intake: ARMOUR_THEN_RESIST + global_flat` · `summons: PRESENT_INERT + offense MEASURED_BASIC` · `arena_fold: None` (armed only in `W1`) · `interrupts_fold: None` · **`WarCryLimb.COOLDOWN` (7.5 s)** · **`PotionLimb.TRACE_CONSISTENT` (θ 0.22972972972972974)** · `CritLimb: LO` · **`p06: OFF`** · **`PhaseModel: ENGAGE`** (`TA-X-24`).

**The runtime prints its RESOLVED limb set into the verdict header (`v0_limb_set`), diffed line-by-line against `V0` before any row is read; it refuses to boot on an unset limb rather than defaulting one.** ⚑ *"Is X wired?" is a driver fact a module default cannot answer.*

**Pilot:** scripted — `DRIVE_TO_PACK` + the M-POL-2 channel policy; `v_ref = 4.0` is a DECLARED-FREE-PARAMETER → 5.4 m/s; **no facing model**.

**Declared fight scope: waves 151–160.** (`DIV-13` opens play at 151; P-e § 1.2 treats 161–170 as *"past the charter's declared fight scope"*; P-e Addendum § 3's analytic is computed over exactly 151–160 at the config of record.)

### B.2 · `P-1` · COVERAGE — **89 / 89**

All **89 enumerated census row ids** mapped **mechanically** (`kc2_runtime/loader/kc2rt_coverage.gd` carries the id list) to exactly one of `IMPLEMENTED` · `DIVERGENCE(DIV-nn)` · `RUNTIME-CHOICE(absent_ref)` · `OUT-OF-SCOPE`. **Counts sum to 89. Zero unmapped.** T-A does not run until green; graded as `TA-X-02`.

⚑ **Why 89 and not 72:** the census's `17 / 41 / 14 = 72` is a **class-share headline taken after collapsing ~a dozen genuinely split rows to their primary class**, and *the note never records which id collapses into which*. **No rule reproduces 72 from the tables.** The **89 enumerated ids govern** (M 23 · D 19 · P 7 · K 26 · W 14); the 72 survives as a headline and **is not a gate**. P-a now carries this as a strike-through pointer **at § E-3, where the rule is read**, rather than only at Addendum 3, ~525 lines below it (WARN-6).

### B.3 · `P-2` · STREAM DISJOINTNESS — and what it does not cover

**Probe:** run `M-POL-2` salt 0 twice, once with a **no-op fold inserted that draws zero values**; assert identical digests. **COVERS** stream isolation at *fold* granularity — exactly what `TA-X-03…06` need.

⚑ **DOES NOT COVER:** (1) that the port's draw sites are the **same sites in the same order** — V9's registry is **29 live sites across 11 streams** (+2 NOT-LIVE); (2) ⚑ **the BOARD ROLL's composition** (§ E trap 6 — now *partially* instrumented, see below); (3) whether the per-site assignment is *lifted* or *chosen*.

**P-2 red → `TA-X-03…06` UNGRADEABLE → `INDETERMINATE` → the cap trips.**

### B.4 · ⚑ `P-3` · **THE ROLL POPULATION AND THE ROLL LAW** — NEW, and the largest hole v1.3 left open

**RULED (KP-32): T-A rolls from `POOL-466`, as the oracle rolls. `ANCHOR-169` is not forced and it is NOT AVAILABLE.**

#### B.4.1 · The four populations — one number each, never substituted for one another

| id | n | the rule (P-e § 1, resolved at emission) |
|---|---:|---|
| **ROSTER-790** | **790** | every `record_path` in `monsters.json::blocks` carrying a `wave`; uniform 20 waves/record, 151–170. **+1 declared-absence key** (`krieg_aethertrap`, no wave) ⇒ 791 distinct keys. **GL-12: a declared null is NOT-MODELLED, never a measured zero** |
| ⚑ **POOL-466** | **466** | pool members of every pool referenced by waves 151–160. ⚑ **Cross-checked by a second independent route; both return 466.** Tier 16 ≡ waves 151–160 exactly (wave 150 is tier 15). ⚑ **THIS IS WHAT `L-49` HAS THE RUNTIME ROLL FROM** |
| **ANCHOR-169** | **169** | the records in `pm2_tg2_monster_timing.csv` — **the threat DECODE's coverage**. Extent 151–170 |
| **BOTH-128** | **128** | `ANCHOR-169 ∩ POOL-466` — rollable at 151–160 **and** offense-covered |

⚑ **`ANCHOR-169` is the RECORDED ROSTER, proven by two exact identities against the pack** (`sum(n_actors) = 344 == n_recorded_actors`; 167 archetype tags, symmetric difference ∅) and by `run.py:1735-1738`'s own comment. **`L-49` rules it: the recorded composition VALIDATES, IT DOES NOT SPAWN.**

> ⚑ **Why the fork DISSOLVED rather than being chosen.** `ANCHOR-169` is not merely not-forced — **it cannot hold the answer**, because **the oracle's own sealed cell spawned five records that are not in it** (P-e Addendum § 2.1). A port pinned to the anchor would be unable to reproduce the cell the bands were measured from. *The decision was made by the substrate; the conductor's two thresholds were asked of a quantity that turned out not to govern.*

#### B.4.2 · ⚑ THE ROLL LAW — two stages, and only one of them is weighted

| stage | law | site |
|---|---|---|
| which **pool alternative** fires at a spawn point | ⚑ **WEIGHTED** by `pool_weight` | `wave_engine.py:974 _weighted_pick` |
| which **member name** of that pool's roster spawns | ⚑ **UNIFORM** — `rng.randrange(len(roster_names))` | `wave_engine.py:849, :869; _emit` |

⚑ **The commission's premise — *"the roll is WEIGHTED"* — is HALF WRONG and is superseded in place.** It is true of the **referent engine** and false of the **oracle**. The oracle's own `_emit` docstring states the divergence *and why it was not "fixed"*: the decoded picker weights and decrements per-entry `limitN`, but the sidecar publishes **only the SUM** of those limits (`UNREACHED-I22-1`), so **modelling the weighting without the per-entry limits would be invention.** The pack carries the same fact as a finding (`PRR-UNIFORM-IS-WRONG-ON-NORMAL`: a uniform draw over the flattened roster is demonstrably the wrong mix on 34 of 81 multi-slot normal pools — *the right count and the wrong composition*), and `ABS-POOL-ROLL-ORDER` declares the roll **procedure** unlifted.

**The port implements the ORACLE's law, not the referent's.** A port that weights the name draw is **wrong**, and it is wrong in a direction no band localises.

#### B.4.3 · What POOL-466 costs, pre-declared — the honest-fail table

Transcribed from **P-e § 5**, both denominators, neither preferred:

| dimension | over **POOL-466** (what `L-49` rolls) | over **ANCHOR-169** | over **BOTH-128** |
|---|---:|---:|---:|
| (a) damage rows | **338** | 0 | 0 |
| (b) slots + gates | **342** | ⚑ **5** | ⚑ **6** *(measured-inert, not data-absent)* |
| (c) OA / DA | **338** | 0 | 0 |
| (d) swing period | **338** | 0 | 0 |
| (d₂) run speed | **338** | 0 | 0 |
| (e) mitigation board | ⚑ **0** | 0 | 0 |

⚑ **Reader trap, named so nobody tries the arithmetic:** row **(b)** does **not** decompose as `338 + 6 = 344`. It is **342**, because (b) is counted on the **CSV grain** while (a)/(c)/(d) are on the **constructed profile grain** — and P-e § 4.1 states the two grains disagree in both directions (*the CSV includes rows that never become slots and omits 39 `tree_attack` slots that fire*). **I do not reconstruct the difference here; inventing a reconciliation is the thing Law 3 forbids** (§ H OQ-4 carries it with a lean).

⚑ **And the correction that produced these numbers is on the conductor's account, not gamora's.** KP-26 sized the honest-fails at **229 / 297 / 297 / 302** by computing `466 − |source|` — **subtraction where it owed a SET INTERSECTION**; 41 of the 169 sit outside the 466. True values **338** and **342**, promoted to prohibition `V25-P10`.

#### B.4.4 · The three body-states and their per-config disposition — `V25-P4 / P5`

| state | n over POOL-466 | `ORACLE` | `PLAY` |
|---|---:|---|---|
| **MEASURED-OFFENSE** | **122** | spawn, attack | spawn, attack |
| ⚑ **MEASURED-INERT** — profile present, `slots == ()` | **6** *(9 over ANCHOR-169; **6 of the 9 are rollable**)* | ⚑ **SPAWN INERT AND COUNT — BOTH CONFIGS** | ⚑ **SPAWN INERT AND COUNT** |
| ⚑ **NO-DATA** — no profile at all | **338** | ⚑ **SPAWN INERT AND COUNT. REFUSAL IS FORBIDDEN** | **REFUSE AND COUNT THE REFUSAL** |

⚑ **The nine MEASURED-INERT bodies are not data gaps and refusing them would be a self-inflicted `STRUCTURAL` red.** Every one has **a measured swing period, a real OA (1905–2184) and 1–4 natural-weapon damage rows**. They are inert *by the oracle's architecture*: `threat.py:1667` rides natural-weapon damage **on a slot** (`rows += list(prof.weapon_rows)` inside `if slot.is_weapon_swing`), so no slot ⇒ nothing for the weapon to ride ⇒ `can_swing` is correctly `False`. **The oracle is internally consistent; there is no defect here.** *(gamora's sharpest HALT hypothesis — a sealed grade computed with nine armed bodies silent — was tested and cleared as a non-finding. No code touched, no grade moved.)*

⚑ **The `ORACLE` NO-DATA disposition is EMPIRICALLY FORCED, not chosen.** The sealed `[MECH]` cell spawned **11 NO-DATA bodies of 97**, across **5 records, none of them in ANCHOR-169** — each resolving `None` at `run.py:1738` and dropped at `:3425 / :3467 / :3611` **with no counter, inside the grade of record**. A port refusing those eleven **has fewer bodies than the cell the bands come from** and breaks exactly the rows T-A rests on. **The COUNT is the only thing the port adds over the oracle's silence, and a counter consumes no draw — so it is stream-neutral by construction.**

#### B.4.5 · `P-3` — the precondition, and the honest limit of a declaration

**The runtime declares `roll_population` and `roll_law` in the verdict header and they are diffed at boot**, exactly as `v0_limb_set` is:

```
roll_population : "POOL-466"        (cardinality asserted == 466)
roll_law        : {"alternative":"WEIGHTED:pool_weight", "name":"UNIFORM:randrange"}
```

**`P-3` red → `INDETERMINATE` → the cap trips.** A port rolling the wrong population is not producing a wrong *number*; it is producing a number about **different monsters**, and no band can see that.

> ⚑ **What a declaration cannot do, said once.** `P-3` is **self-reported**. A port can declare `POOL-466` and roll `ANCHOR-169`. That is why `TA-X-25(c)` exists as the **behavioural** check, and why the two are not redundant: the declaration catches the honest builder at boot for free; the behavioural row catches the mistaken one after the run. **This is the same instrument-vs-claim split that `TA-X-11`'s caveat is built on** — *a port with no wall at all also scores zero.*

---

## § C · THE DENOMINATOR LAW, STATED ONCE

```
D_constructed = CHANNELLING + CHANNELLING_AND_MOVING + MOVING + IDLE      (PRE_FIGHT and DEAD excluded)
```
Verified on the seal: pooled `287 + 2211 + 166 + 119 = 2783 = D`; the per-salt sum equals the pooled sum, so the partition is exact at both grains. ⚑ **No sealed artifact carries `D`. It is CONSTRUCTED.**

**Two identities, 5/5 on the seal, graded as `TA-X-08`:** `n_player_ticks_observed = D + PRE_FIGHT` · `n_channelling + n_released = D` ⇒ `uptime + n_released/D = 1.000000` exactly.
⚑ **The seal publishes `release_duty` on `D + PRE_FIGHT`**: `23/106 = 0.2169811 = 1 − 0.7830189` on `D`, against `23/107 = 0.2149533`. **The 0.215-vs-0.217 tell resolves entirely to a denominator difference. Every rate row here divides by `D` and by nothing else.**

**C.2 · Pooled vs mean-of-salts.** Every band is on the **MEAN-OF-SALTS**; a port's pooled figure is **never** compared against these bands. `D` per salt is **[1084, 305, 106, 185, 1103]** — a **10.4× span**. On the plant ratio the pooled/mean gap consumes **38 %** of the whole tolerance.
**C.3 · The graded object** is the **mean of a NEW 5-salt run**; the interval is a **prediction interval** carrying both runs' sampling error; `ddof = 1`; `half-width = t(0.975, df=4) · s · √(2/5) = 1.755978 · s`. All widths live in **P-a**.
**C.4 · T-B denominators are NOT these** (from **P-b**). HP occupancy on **`LIVE-MAX`** reproduces **42.84 %**; NOMINAL gives **39.76 %** — **3.08 pp with no fight in it**. HP window **181.0 s**; energy / motion / release / cast **182.65 s**.

⚑ **C.5 · A THIRD DENOMINATOR CLASS ENTERS AT v1.4, and it is not `D`.** `TA-B-15` and the per-wave coverage lines divide by **BODIES** and cluster by **POOL PICKS** — populations with no relationship to `D` or to the T-B windows. **Never pool them, never compare them, and never let a report print a body-fraction under a heading that has been printing tick-fractions.** *(The 0.215-vs-0.217 tell is this project's standing proof of what one shared name costs.)*

---

## § D · ROW-ID CONCORDANCE — the single namespace

⚑ **Every citation uses the `TA-` id; a width is looked up by STATISTIC NAME in the table named "governs", never by a bare `B-n`.**

| **canonical** | statistic | gandalf v1.0 | gamora § 2.4 | gamora Add. 1 | **width governs (in P-a)** |
|---|---|---|---|---|---|
| `TA-B-01` | terminal wave | B-1 | B-1 | — | § 2.4 · **REPORT-ONLY** |
| `TA-B-02` | **uptime** on `D` | B-3 | **B-2** | **B-4** | ⚑ Add. 1 restatement |
| `TA-B-03` | `frac_moving` on `D` | B-4 | B-3 | B-3 | Add. 1 restatement |
| `TA-B-04` | `P(chan \| moving)` | B-5a | B-4 | B-5a | Add. 1 restatement |
| `TA-B-05` | `P(chan \| stationary)` | B-5b | B-5 | B-5b | Add. 1 restatement |
| `TA-B-06` | plant ratio (window 5.0 s) | B-8 | B-6 | B-6 | Add. 1 restatement |
| `TA-B-07` | release duty on `D` | B-7 | B-7 | B-7 (restated) | Add. 1 · **reported-not-counted** |
| `TA-B-09` | **channel split** | *(nominated v1.1)* | — | — | ⚑ **Addendum 2 § B2** |
| ⚑ `TA-B-15` | **NO-DATA spawn count / fraction** | — | — | — | ⚑ **none — REPORTED-NOT-COUNTED; expectation in P-e Add. § 3–5** |
| `TA-X-03…06` | inertness / distinctness | E-2, E-3, E-4 | **E-1 (a–d)** | A4 | — |
| `TA-X-07` | conservation, 7 terms | E-5 | **E-2** | — | — |
| `TA-X-02` | coverage | E-1 | **E-3** ⚑ *at 89/89* | — | — |
| `TA-X-08` | denominator identity | *(implicit)* | **E-4** | A1 | — |
| `TA-X-11` | wall-clamp zeros | E-7b | — | **A2** | — |
| ⚑ `TA-X-25` | **NO-DATA path — refusal identity, counter presence, arm-level presence** | — | — | — | ⚑ **P-e Addendum § 5 (`V25-P4/P5/P9`)** |

*The uptime row remains the reason this table exists: **B-3 · B-2 · B-4 — three ids, one statistic, two files.*** ⚑ *And `TA-B-15`/`TA-X-25` are the reason it now extends across **repos** — their governing text is in the engine (P-e), not in P-a.*

---

## § E · ⚑ OUTSIDE T-A'S REACH — the catching-row audit

### E.1 · The traps

| # | trap | **caught by** | verdict |
|---|---|---|---|
| **1** | **V5-GUARD-2** — arrival `px, py` are **TELEMETRY ONLY** | `TA-X-19` | **CLOSED** |
| **2** | **V9-DEAD-2** — the retired square-box scatter draws at the **same stream position**; **invisible to a digest** | `TA-X-17` + `TA-X-18`; `TA-X-10`/`TA-X-11` indirectly | **CLOSED** |
| **3** | **V17** — `hit_test_model = "point"` in the pack vs the sim's **uniform 3.0 m disc** | `TA-X-20` for the resolved predicate. ⚑ `R2D-5` still owns the DRAWN radius | **HALF-CLOSED — declared** |
| **4** | **V4-LAW-1** — the cadence law is **not RNG-neutral** | `TA-X-21` | **CLOSED** |
| **5** | **V18 + V19** — flag **AND** coin = the 0.15 applied twice | `TA-X-22` | **CLOSED** |
| **6** | ⚑ **THE BOARD ROLL** | ⚑ **PARTIALLY INSTRUMENTED at v1.4 — `TA-X-25(c)` + `P-3`.** `TA-X-23` remains **STRUCK, never minted, id retired.** Both seals still carry **no roster counts by class** | ⚑ **OPEN — DECLARED, and the opening is narrower than it was** |
| **7** | the attack-**PHASE** model — `HASH` default vs `ENGAGE` of record; both deterministic | `TA-X-24` | **CLOSED** |

⚑ **Trap 6, restated for the report's face, with the v1.4 movement stated honestly.** **12 of the 29 live draw sites are the board roll.** It is the mechanism most likely to be rewritten from scratch in GDScript; **its divergence shows as a different SET of monsters, not a different number.** v1.4 adds a **one-bit test**: `TA-X-25(c)` asks *"did the port draw from a population that contains NO-DATA records at all?"* — which a port pinned to `ANCHOR-169` **must** fail, because the anchor has **zero** NO-DATA members.

> ⚑ **What that one bit does NOT prove, said plainly so no report over-reads it.** It proves **membership**, never **composition**. A port rolling POOL-466 with **completely wrong weights**, a wrong `count_bounds`, or a weighted name draw instead of a uniform one would spawn NO-DATA bodies and **pass `TA-X-25(c)` cleanly**. **Trap 6 remains open for exactly the thing it was opened for.** Closure is still **a sibling that emits per-wave class counts**, not a T-A row.

**Also outside reach:** per-site draw localisation (S5 out of scope — at **29** sites the ceiling is *lower* than the charter assumed) · the tick-resolution HP trace · every `DIV-nn` row, by construction.
⚑ **And the limit on `TA-X-11` that must not be over-read:** the oracle's clamp counters are **structural zeros** — the wall never binds (margin `43.758085 − 43.404802 = 0.353283` m = **0.807 %**). `TA-X-11` says *"the port never needed to clamp"*, **not** *"the port's wall works"*; **a port with no wall at all also scores zero.**

### E.2 · ⚑ DECLARED CEILINGS INTRODUCED BY THE COMPOSITION RULING

| # | ceiling | what would settle it |
|---|---|---|
| **C-a** | ⚑ **THE REFUSAL DISCRIMINATOR IS STRUCTURALLY DEAD UNDER `ORACLE`.** KP-26 and P-e § 5 both promise *"T-A reports refusals per salt; nonzero ⇒ that salt's stream rows UNGRADEABLE."* **Under the ruling, refusal is FORBIDDEN under `ORACLE`, so the count is `0` by construction and carries no information.** `TA-X-25(a)` grades the zero as an **identity**; it is not a discriminator | **the `PLAY`-side probe**, where refusal is the rule and the count is live (`DIV-18`). ⚑ **Under `ORACLE` nothing can settle it, and that is the point of recording it** |
| **C-b** | ⚑ **The ten-wave composition expectation (`0.6172` covered / `0.3828` NO-DATA) has NO empirical check.** The sealed `[MECH]` census covers **waves 151–155 only**; the declared fight scope is **151–160**. **The back half of every T-A salt runs at an expectation that no cell has ever validated** | a census over a cell covering 156–160 — **and none exists.** Not buildable without a new sealed run, which K-7 forbids. **Carried, not closed** |
| **C-c** | **The `limitN` residual.** The analytic assumes `roster_fold = None` (the incumbent; the config of record carries no roster fold). Under I-22's `limitN` cap the expected body count falls by **−11.500 over 151–160**; the cap truncates **EMISSION** without re-weighting the name draw, so the coverage **fraction** is expected near-invariant | ⚑ **STATED AS AN EXPECTATION, NOT A MEASUREMENT, and flagged as such by gamora herself.** A measured pass over the capped config would settle it |
| **C-d** | ⚑ **Row (b) of the honest-fail table (342) does not decompose against (a) (338) + measured-inert (6)** | P-e § 4.1's CSV-vs-constructed grain distinction is the declared reason; **stating which grain (b) is counted on** closes it in one line (§ H OQ-4) |

### E.3 · ⚑ WHAT IS **NOT** A CEILING — the 4.7 σ, and why it is recorded as CLOSED

**The commission handed me this as an unreconciled gap to carry. It is not one any more, and carrying it as one would have been the error.**

| | analytic (151–155) | sealed cell (salt 0) |
|---|---:|---:|
| `E[bodies]` | **98.08** | **97** ⚑ the count model was always validated |
| coverage fraction | **0.6595** | **0.8866** |

**Three hypotheses were live. Two were the conductor's; all three are disposed of by measurement, not by argument:**

1. ⚑ **SELECTION BIAS — REFUTED.** The conductor's hypothesis was that `salt0_knots` is event-sourced (biased toward bodies that acted). **It is spawn-sourced**, on three independent proofs any one of which suffices: `extract_paths` iterates **`for m in r.movers`**, not an event log (`:255`); **a body with no knots is a recorded VIOLATION, not an omission**, and the cell publishes `n_violations = 0` (`:266-268`); and **`knot_kind_counts["spawn"] = 97` against `n_actors = 97`, exactly 1:1** (`:273-278` anchors every row on the spawn event). The emitter even publishes `actors_never_stepped` — *a statistic whose only purpose is to count non-acting bodies* — and reports **0**, meaning all 97 stepped, **not** that non-steppers were excluded. The one real filter (`run.py:4004-4015`) drops bodies that **never spawned**, keyed on spawn timing and liveness, **with no offense correlation**.
2. **WINDOW MISMATCH — REFUTED.** `0.6595` was **already** restricted to 151–155; the ten-wave figure is the separate `0.6172`. **Proven by the count identity** — 98.08 against 97 could not match if the windows differed.
3. ⚑ **THE ACTUAL DEFECT — a dispersion quoted over the wrong unit.** `σ = sqrt(p(1−p)/n)` was computed with **n = 97 bodies**, assuming independent draws. **They are not independent:** `_weighted_pick` fires **once per spawn point per wave**, and every body emitted there comes from that single pick's roster. Measured from the cell: **23 independent pool-alternative picks behind 97 bodies** (min 1 · median 3 · max 9 per cluster). Design effect **√(97/23) ≈ 2.05×** — **exactly** the factor between the two `z` values.

| n used | σ | **z** |
|---|---:|---:|
| 97 bodies — the original, wrong | 0.0481 | **4.72** |
| ⚑ **23 clusters — the independent unit** | 0.0988 | ⚑ **2.30** |

> ⚑ **At `z = 2.30` on a SINGLE SALT, `0.8866` against an expectation of `0.6595` is an ordinary draw.** The analytic model and the cell **agree on the count AND on the composition.** gamora **withdraws** *"there is a mechanism I have not identified."* **Nothing ships differently:** `V25-P4/P5/P9` rest on a **direct count of 11 NO-DATA bodies of 97** and on `ANCHOR-169 ⊉ spawns` — observations, not model output — so star-lord's cut is untouched.

**The bracket, correctly described.** `[0.617, 0.887]` is **not** "the range the true value lies in." **`0.617` is the EXPECTATION over ten waves (`0.660` over 151–155); `0.887` is ONE SALT'S FIVE-WAVE DRAW around it**, consistent at `z = 2.30`. ⚑ **A T-A reader carries the ANALYTIC point estimate; the empirical is one sample of it** — and a report that quotes `0.887` as the expectation is quoting a sample as a parameter.

⚑ **The discipline this yields, and it belongs beside `#72`:** **before quoting a dispersion, name the unit that was actually DRAWN.** A per-body σ over cluster-drawn bodies **overstates precision by √(design effect)**. gamora's own reading is the one to keep: *"the count cross-check was already telling me the model was sound; I read a composition gap as a model failure because my error bar was too narrow to admit the model."* **This is the fifth instance this session of one shape — the arithmetic correct, the POPULATION it ranged over the defect** (KP-26's subtraction-for-intersection · the "169" naming three populations · a measured-inert count in a data-absence column · ANCHOR-169 implying it held the spawns · and now a σ over bodies when the draws are over pools). **§ B.4's four-population table and § C.5's third-denominator warning exist because of it.**

---

## § F · THE GRADED ROWS

### F.1 · Decisiveness classes

**EXACT** — identity, invariant, count, or declared-precision reproduction; a red says **the port is wrong**; may carry a **NUMERICAL** tolerance, **never a STATISTICAL one**.
**BAND** — distributional at n = 5; **individually and collectively non-decisive**. Forms: `INTERVAL` · `RATIO` · `ORDERING`.
⚑ **No width is defaulted.** ⚑ **Cross-implementation rows are NOT salt-paired**; **inertness rows are salt-paired within the port.**

⚑ **One class note added at v1.4, because `TA-X-25(c)` would otherwise look like a statistical row wearing an EXACT badge.** An EXACT row may assert a **STRUCTURAL ZERO or a STRUCTURAL NON-ZERO** — a quantity whose value is fixed by the construction of the system rather than by a distribution. **`TA-X-05` and `TA-X-06` are the standing precedent** (*"exact, one-sided"*: distinctness asserted on ≥ 1 salt, no width, no tolerance). `TA-X-25(c)` is the same shape in the opposite direction. **The test for whether an assertion belongs in this class: can you name the mechanism that makes the other value impossible?** If the answer is *"it would be very unlikely"*, it is a BAND and it does not belong here.

### F.2 · EXACT rows — **24**

| id | statistic | basis | tolerance |
|---|---|---|---|
| `TA-X-01` | port self-determinism — any arm/salt run twice → identical digest | run-internal | byte-exact |
| `TA-X-02` | **coverage 89/89**, zero unmapped | the census id list | integer |
| `TA-X-03` | inertness A — `port(M-POL-2-NULL, s) ≡ port(M0, s)`, all 5 | `[M-POL2]` | byte-exact |
| `TA-X-04` | inertness B — `port(W1-NULL, s) ≡ port(M-POL-2, s)`, all 5 ⚑ **not M0** | `[W1W]` | byte-exact |
| `TA-X-05` | distinctness C — `port(M-POL-2, s) ≢ port(M0, s)`, ≥ 1 salt | `[M-POL2]` | exact, one-sided |
| `TA-X-06` | distinctness D — `port(W1, s) ≢ port(M-POL-2, s)`, ≥ 1 salt | `[W1W]` | ⚑ **RELATION ONLY, never magnitude** |
| `TA-X-07` | **conservation — SEVEN terms** `offered = applied + dropped + voided + pool_truncated + pcl_reclaim + counterplay_absorbed` | run-internal | **`1e-6`** ⚑ a live driver assert-wall checks **six** |
| `TA-X-08` | denominator identity, both sub-identities | `[M-POL2]`, 5/5 | exact |
| `TA-X-09` | all **9** `math_rules.test_vectors` | the pack | per-vector |
| `TA-X-10` | containment supremum `max_body_radius_m ≤ 43.758085029822276` (W1) | `[W1W]` | exact, ≤ |
| `TA-X-11` | wall-clamp zeros — `n_wall_clamps_{player,body} == 0`, every W1 arm | `[W1W]` | integer |
| `TA-X-12` | pool inertness under ORACLE — total pool damage `== 0.0` | `[W1W]` ⚑ **see `DIV-19`: the entrance aprons must not defeat this** | exact |
| `TA-X-13` | no player crit | `V0 · CritLimb LO` | integer |
| `TA-X-14` | the two DO-NOTs (`cause == "energy"` → 0; no release-on-every-cast) | pack prohibitions, R2D-4 | integer |
| `TA-X-15` | release-schedule negative — p01–p04 at `t = 0.0`, p05 one burst at `t = 4.000 s`, no intra-point stagger | census M4 / `V11` | exact |
| `TA-X-16` | **p06 OFF** | `V0` ⚠ code default disagrees. ⚑ **Cross-check: P-e's analytic assumes `p06_bonus_spawns = false` per `V0-36` — the composition expectation is computed at THIS config, not another** | integer |
| `TA-X-17` | spawn offset — `‖spawn_xy − anchor_xy‖ ≤ 8.0` m, every body, arm, salt | `ρ = 8.0·u₂`; box reaches **11.313708 m**; **21.46 %** of box draws exceed 8.0 | exact, ≤ |
| `TA-X-18` | **scatter-law three-law discriminator** — feed `u₁ = u₂ = 0.5`, assert **`(−4.0, 0.0)`** | polar → `(−4.0, 0)` · uniform-in-area → `(−5.656854, 0)` · box → `(0.0, 0.0)` | exact |
| `TA-X-19` | arrival unconditionality; **no damage predicate reads an arrival's `px, py`** | `deferred_arrival.py:13-17` | integer |
| `TA-X-20` | player hit-test predicate — 2.99 m hit / 3.01 m miss; no angular gate; no target cap | census D7 | exact |
| `TA-X-21` | **quantisation rule per site** — § F.2a | four modules | exact |
| `TA-X-22` | flag-off release cause under ORACLE — `cause == "interrupts_channel_flag"` occurs **0** times | `V0`; V18+V19 | integer |
| ~~`TA-X-23`~~ | ~~board-roll composition~~ | ⚑ **STRUCK at v1.2. Id retired, never re-used** | — |
| `TA-X-24` | **attack-phase model is `ENGAGE`** — `sha256(actor_id) mod n` never evaluated | `V0`; `run.py:696` / `threat.py:1246` carry `HASH` as the **DEFAULT** | exact |
| ⚑ `TA-X-25` | **THE NO-DATA PATH — three clauses** | § F.2b | integer / exact, one-sided |

#### F.2a · ⚑ `TA-X-21` — THE QUANTISATION RULE, PER SITE *(unchanged from v1.3; restated in full because v1.3 is superseded and a grader must not have to hold two files open)*

> ⚑ **No bare `round(` may appear on THE PORT'S threat path.**
> **The oracle's Python threat path DOES use `int(round(…))` at all four LIVE sites — and that is the point, not a contradiction.** Python's built-in `round` on a float is **ROUND-HALF-TO-EVEN**, and **that rule is what the port must reproduce EXPLICITLY**, because **GDScript's `round()` rounds half AWAY FROM ZERO** (`round(2.5)` → **2** in Python, **3** in GDScript). A port that writes `round(` inherits the wrong rule silently; the oracle that writes `round(` inherits the right one. *The assertion is about the port's source, never the oracle's.*
> ⚑ **And the cost is not one tick.** The swing period sets `is_opportunity`, which sets **how many `choose_slot` calls draw** — so a bare GDScript `round()` **desynchronises the threat RNG stream** (V4-LAW-1).
> **Corroborated by the seal:** the M-POL-2 fold's `⚑ quantisation_error` block says *"round-half-to-EVEN to the nearest whole tick (Python's `round`)"*. `threat.py` imports no `numpy` and no `decimal`, so the built-in is the one in play.

| site | expression (oracle) | **rule the port implements** | graded |
|---|---|---|---|
| `threat.py:1402` | `max(1, int(round(per / mult * ticks_per_s)))` — **the cadence law** | ⚑ **HALF-TO-EVEN, explicit** | **vector** |
| `threat.py:1522` | `max(1, int(round(s.delay_s * ticks_per_s)))` — first-cast gate | ⚑ **HALF-TO-EVEN, explicit** | **vector** |
| `threat.py:1555` | `tick + max(1, int(round(cd * ticks_per_s)))` — slot cooldown | ⚑ **HALF-TO-EVEN, explicit** | **vector** |
| `threat.py:1867` | `tick + max(1, int(round(r.dot_duration_s * ticks_per_s)))` — DoT expiry | ⚑ **HALF-TO-EVEN, explicit** | **vector** |
| `deferred_arrival.py:330` | `int(math.ceil(raw))` | **`CEIL`**, half-insensitive | assert `CEIL` |
| `dot_timeline.py:380` | `int(exact) if TRUNCATE_NTICKS else …` | **`TRUNCATE`** (`R-DOT-2`) | assert `TRUNCATE` |
| `control_application.py:591` | `max(0, int(exact) if TRUNCATE_BUCKETS else …)` | **`TRUNCATE`** | assert `TRUNCATE` |
| `counterplay.py:212` | `int(round(x * BAR_PX))` | presentation quantisation — **not on a damage path** | not graded |

**Vectors at each of the four LIVE sites:** `n_raw = 8.5 → 8` · `10.5 → 10` · `2.5 → 2`. *(GDScript's `round` returns 9, 11, 3 — every one discriminates.)*
**Negative assertion:** a source scan **of the built port** finds **zero** bare `round(` calls on the threat / cadence / arrival path.

#### F.2b · ⚑ `TA-X-25` — THE NO-DATA PATH, THREE CLAUSES

**Governing text: P-e Addendum § 5 (`V25-P4` / `V25-P5` / `V25-P9`), adopted as shipped.**

| clause | assertion | class | what a RED means |
|---|---|---|---|
| ⚑ **(a)** | under `ORACLE`, `n_nodata_refused == 0`, **every arm, every salt** | **EXACT · integer identity — `0` BY CONSTRUCTION** (refusal is FORBIDDEN under this config) | the port is running the `PLAY` refusal rule under the `ORACLE` config. ⚑ **A config leak, not a fidelity miss** — and it would have silently removed bodies the bands were measured with |
| ⚑ **(b)** | the counters `n_nodata_spawn_inert` and `n_measured_inert_spawn` are **PRESENT and EMITTED** per arm per salt, and `n_measured_inert_spawn > 0` summed across each arm's 5 salts | **EXACT · schema presence + structural non-zero** | the port has re-created the oracle's own silence. ⚑ **The oracle drops NO-DATA bodies at three sites with NO COUNTER (`run.py:3425 / :3467 / :3611`) — the count is the ONE thing the port must add, and a counter consumes no draw, so adding it is stream-neutral by construction.** `measured_inert` is asserted non-zero because **6 of the 9 are rollable from POOL-466** and they are spawned in **both** configs |
| ⚑ **(c)** | ⚑ **across the 5 salts of an arm, `Σ n_nodata_spawn_inert > 0` — every arm** | **EXACT · one-sided, structural non-zero** *(same class as `TA-X-05`/`TA-X-06`)* | **the port is not rolling POOL-466.** The mechanism that makes zero impossible: **`ANCHOR-169` contains ZERO NO-DATA members** (P-e § 3.2, `ANCHOR-169` NO-PROFILE column = **0**) while **POOL-466 contains 338**, and the oracle's own five-wave single-salt cell produced **11 of 97**. A full arm is **5 salts × ten waves ≈ 900 bodies** at a NO-DATA rate the evidence brackets at **[0.113, 0.383]** |

⚑ **Why the arm level and not the salt level — the judgement the commission left to me, and the reasoning behind it.** A **per-salt** `> 0` assertion would be tighter and I am declining it. The draws are **CLUSTERED** — median 3 bodies per pool-alternative pick, and a single salt's NO-DATA presence rests on a few dozen categorical picks, not on hundreds of independent bodies. **I cannot name a mechanism that makes a single salt's zero impossible, and § F.1's own test for this class says that if the best I can say is *"very unlikely"*, it is a BAND and does not belong in EXACT.** At the **arm** level — five independent salts, ~4,500 bodies, ~1,000 picks — **`ANCHOR-169`'s zero NO-DATA members is a set-membership fact, not a probability**, and the row grades a mechanism. *The tighter row would have been the more impressive one and the less defensible one.*

> ⚑ **WHAT `TA-X-25` DOES AND DOES NOT PROVE — for the report's face, stated where a grader will read it.**
> **PROVES:** the port draws from a population containing NO-DATA records (so not `ANCHOR-169`); the NO-DATA spawn path is **wired and firing**; the ORACLE/PLAY config split is **not leaking**; the counters exist.
> ⚑ **DOES NOT PROVE:** that the composition is right. It is **one bit — membership, never distribution.** A port rolling POOL-466 with wrong `pool_weight`s, wrong `count_bounds`, or a **weighted** name draw instead of a uniform one passes all three clauses. **Trap 6 stays open** (§ E.1).
> ⚑ **AND IT IS NOT A SUBSTITUTE FOR WHAT WAS LOST.** KP-26 planned a **per-salt refusal count** as a live discriminator. The ruling that made the port faithful **killed that instrument** (§ E.2 C-a). **The run traded a per-salt discriminator for a per-arm one-bit presence test. That trade was correct — the alternative broke the bands — but the report must not print it as though the discriminator survived.**

### F.3 · BAND rows — **15 ids**

| id | statistic | sub-class | width (in **P-a**) |
|---|---|---|---|
| `TA-B-09` | **channel split** `CHANNELLING / (CHANNELLING + CH_AND_MOVING)` | ⚑ **COUNTED · INTERVAL — the strongest BAND row T-A has** | **Addendum 2 § B2** |
| `TA-B-03` | `frac_moving` on `D` | COUNTED · INTERVAL — second | Add. 1 restatement |
| `TA-B-02` | uptime on `D` | COUNTED · INTERVAL — weak, **clips at 1.0** | Add. 1 |
| `TA-B-04` | `P(chan \| moving)` | COUNTED · INTERVAL — weak, clips at 1.0 | Add. 1 |
| `TA-B-05` | `P(chan \| stationary)` | COUNTED · INTERVAL — weak; small stationary population | Add. 1 |
| `TA-B-06` | plant ratio (window 5.0 s) | COUNTED · INTERVAL — weak, **§ C.2-fragile** | Add. 1 |
| `TA-B-01` | terminal wave | **REPORT-ONLY** — its band **admits every arm in the seal, including the G5 control** | § 2.4 |
| `TA-B-07` | release duty on `D` | **REPORTED-NOT-COUNTED** — `released/D ≡ 1 − uptime`; one row with a sign flip | Add. 1 |
| `TA-B-08` | ordering `P(chan\|moving) > P(chan\|stationary)` | **REPORTED-NOT-COUNTED** — implied by `TA-B-04 ∧ TA-B-05`; survives a denominator dispute that would void both | none |
| `TA-B-14` | `n_avoidance_vetoes`, `n_pool_occupancy_ticks` | **REPORTED-NOT-COUNTED** — oracle values 0–2 | none |
| ⚑ `TA-B-15` | ⚑ **NO-DATA SPAWN COUNT AND FRACTION, per arm per salt** | ⚑ **REPORTED-NOT-COUNTED — see the box below** | ⚑ **none, and none may ever be minted** |
| `TA-B-10` | per-wave durations | ⚑ **UNGRADEABLE-DECLARED** · T-B-only ⚑ **and now subject to § F.5** | — |
| `TA-B-11` | arrival latency / co-arrival / `n_deferred` | ⚑ **UNGRADEABLE-DECLARED** — absent from both seals | — |
| `TA-B-12` | intake by wave and damage family; leech per tick | ⚑ **UNGRADEABLE-DECLARED** ⚑ **subject to § F.5** | — |
| `TA-B-13` | `max_body_radius_m` (W1) | ⚑ **UNGRADEABLE-DECLARED** — an **extreme, not a mean**; sample degenerate; **its t-band rejects the oracle's own maximum** | — |

**Sub-class counts: 6 COUNTED · 5 REPORTED-NOT-COUNTED · 0 CONDITIONAL · 4 UNGRADEABLE-DECLARED = 15.**

> ⚑ **`TA-B-15` — why it is REPORTED-NOT-COUNTED AND WHY IT CAN NEVER BE PROMOTED.**
> **It measures the SUBSTRATE, not the port.** The NO-DATA fraction is a property of *the records POOL-466 happens to contain*, which the port neither chooses nor influences. **A fidelity band over it would score the port on the oracle's data coverage** — and on an artifact `K-7` forbids re-running to improve. ⚑ **That is the `TA-B-13` mistake in a new costume** (grading a port against a statistic whose own sample rejects the oracle), and it is pre-empted here rather than discovered at the seal.
> **What it MUST print, per arm per salt:** the **count**, the **fraction of bodies**, and **both reference points labelled as what they are** — the **analytic expectation `0.3828` over ten waves** (`0.3405` over 151–155) and the **single-salt five-wave observation `0.1134`**. ⚑ **The analytic is the expectation; the empirical is one sample of it, and a report that quotes `0.1134` as the expected value is quoting a sample as a parameter** (§ E.3).
> **What makes it interesting:** ⚑ **a salt reporting ZERO is the anomaly, not a salt reporting many.** A zero is graded by `TA-X-25(c)` at the arm level; at the salt level it is a **flag for investigation, never a red.**

### F.4 · Emitted, not graded

Per-registered-site draw counters (**29 sites**; they localise nothing without S5) · the tick-resolution HP trace.

### F.5 · ⚑ REPORT-FACE RULES — what every row must print beside itself *(NEW at v1.4)*

1. **Every band prints `value @ coverage k/89`** (unchanged — `P-1`, and it is a **rule** coverage, not a **population** coverage; see § C.5).
2. ⚑ **EVERY ROW KEYED BY WAVE PRINTS ITS OWN COVERAGE.** Coverage is **not uniform across waves**: the analytic runs from **`0.2999` at wave 157** to **`1.000`** at several waves; the empirical cell gives **`0.471` at wave 155** against **1.000 at 151, 153 and 154**. ⚑ **A per-wave band on a thin wave would otherwise read as if it rested on the pooled base — and it does not.** Binds `TA-B-10`, `TA-B-12`, galadriel's `TB-WV-01` and the per-wave HP shape, and any row a grader adds later that is keyed by wave.
3. ⚑ **AND IT PRINTS THE NUMBER OF POOL PICKS BEHIND IT, NOT ONLY THE BODY COUNT.** Under clustering — **median 3 bodies per pool-alternative pick, max 9** — the body count **overstates the evidence by the design effect**. ⚑ *A wave at `0.300` over 4 picks and a wave at `0.300` over 20 picks are not the same claim*, and a reader given only the body count cannot tell them apart. **This is § E.3's discipline applied as a printing rule: name the unit that was actually drawn.**
4. **Wave labels are not assumed to be total.** galadriel's grid audit found **frame 10860 (`t = 864.0`) carrying an EMPTY wave label**, mapped to `wave = -1` (UNLABELLED), **excluded from per-wave rows and included in whole-fight rows**. ⚑ **A per-wave denominator and a whole-fight denominator therefore do not sum to the same population**, and the report says so rather than letting the one-frame difference surface as an unexplained residual.

---

## § G · FAIL TAXONOMY AND THE T-B QUOTING CAP

| verdict | antecedent | consequence |
|---|---|---|
| **`STRUCTURAL`** | **≥ 1 EXACT row RED** | port is wrong; **no W4 until repaired**; cap **TRIPS**; **two graded runs against v1.4 both STRUCTURAL → HALT to Matt** |
| **`INDETERMINATE`** | 0 EXACT red, **≥ 1 EXACT UNGRADEABLE** (incl. `P-1`, `P-2` or ⚑ `P-3` red) | cap **TRIPS**; does **not** increment the two-attempts counter |
| **`STATISTICAL`** | all EXACT green; **≥ 1 COUNTED BAND row RED** | a **finding**; handoff proceeds; cap does not trip |
| **`PASS`** | all EXACT green; no counted BAND red | **`PASS @ coverage k/89, n/6 counted band rows graded`** — never unqualified |

**Order:** `STRUCTURAL → INDETERMINATE → STATISTICAL → PASS`, stop at the first hit. **A BAND row can never outrank an EXACT row in either direction.** UNGRADEABLE is orthogonal. **A GRADED RUN** = one execution of the 5 × 5 matrix producing a conforming verdict file; a port repair between attempts does not reset the counter. **No post-hoc widening, by anyone** (A-3; L-88).

**Verdict file** `kc2play.ta_verdict.v1`:

```
prereg_version                    : "v1.4"
prereg_sha256                     : <this file, derived at emission>
band_widths_sha256                : 7a5d4aa3…          (P-a)
galadriel_note_sha256             : 8186202c…          (P-b)
galadriel_expected_values_sha256  : a8b85331…          (P-c)
galadriel_release_labels_sha256   : 15dace60…          (P-d)
⚑ v3p3_prereg_sha256              : 97e5a4c7…          (P-e)
⚑ v3p3_lifted_rows_sha256         : e51b54a1…          (P-f)
⚑ v3p2_lifted_rows_sha256         : e0117429…          (P-g)
register_sha256                   : <v0.3's MACHINE form, emitter-derived — never this document's file hash>
preconditions.P1_coverage         : {"mapped":89,"total":89,"unmapped":0}
⚑ preconditions.P3_roll           : {"population":"POOL-466","cardinality":466,
                                      "law":{"alternative":"WEIGHTED:pool_weight","name":"UNIFORM:randrange"}}
v0_limb_set                       : <diffed line-by-line against V0>
⚑ nodata                          : {"refused":0, "spawn_inert":<n>, "measured_inert":<n>}  per arm per salt
```

**Cap — three refusal conditions:** **C1** verdict file absent / unparseable / **any pinned sha mismatched** · **C2** `verdict ∈ {STRUCTURAL, INDETERMINATE}` · **C3** ⚑ **coverage not 89/89-mapped — and THIS PREREG GOVERNS the threshold** (charter § 4.4's `72/72` is superseded-pending-annotation; **a cap with two thresholds has none**).
**"A fidelity figure"** (mechanical): a row pairing a twin statistic with a referent statistic; or a ratio/percentage/delta/residual/score between them; or `fidelity`/`faithful`/`accuracy`/`match`/`agreement`/`% of referent` in a label. ⚑ **`TA-B-15` is expressly NOT one** — it pairs a twin statistic with a **substrate** statistic, and the cap must not suppress it.
**Degraded behaviour:** raw twin-side statistics only, each with its own denominator and window; a **banner before** the statistics naming the condition; **non-zero exit**. Composes with R2D-10.

---

## § H · OPEN QUESTIONS — one lean each

**OQ-1 · The charter still carries the superseded sizing AND the superseded refusal promise, in two rows, live-tense.** KP-26 prints `229 / 297 / 302` and *"the 169 the oracle ever rolled"*; charter § 4.3 / § 4.4 / § 3 F1 / § 9 still print `72`. → **Annotate all of them forward in the same strike-through form S-2 already carries, in one pass, before the W3 seal.** It is **propagation, not a new ruling — no Matt.** ⚑ **The sweep at § A.1 is the argument: the prereg and register were clean, so every hour of confusion these figures still cost is charged entirely to the charter.**

**OQ-2 · ⚑ P-e § 5 lines 421–425 still promise *"T-A must report refusals per salt; nonzero ⇒ UNGRADEABLE"* — and its own Addendum § 5 supersedes that ~320 lines below.** → **Ask gamora for a strike-through pointer AT § 5, not only at the addendum.** ⚑ **This is WARN-6 exactly, in a second file, one day later:** jack-ryan's finding was that *a correction filed ~525 lines below the place a reader looks the rule up is a correction the next reader does not receive*. **star-lord cuts against § 5. A builder reading it top-down implements a dead discriminator and then wonders why it always reports zero.** One line, and the class of defect is already ruled.

**OQ-3 · `kc2rt_coverage.gd:48` still holds `CHARTER_DENOMINATOR := 72`.** → **Rename it `CENSUS_DENOMINATOR := 89` and retire the disagreement branch entirely.** The constant's *name* is half the defect: it asserts the charter as the authority for a number the **census** enumerates, which is what let the two drift.

**OQ-4 · Row (b) of the honest-fail table (342) does not decompose against (a) (338) and the 6 measured-inert.** → **Lean: ask gamora to state (b)'s grain in one line** (CSV rows vs constructed slots), **and do not attempt the reconciliation from this side.** P-e § 4.1 already establishes the two grains disagree in both directions; the number is almost certainly right and the *label* is what is under-specified. ⚑ **Naming a grain is a measurement; inferring one is an invention.**

**OQ-5 · The emitter emits 9 divergence rows against the register's 28.** → **Leave the `COVERAGE FAIL` at `P-1` armed and expect it to fire at T-0.** The right catch working; naming it now means it is met as a scheduled event. The emitter fills at W3. ⚑ **The gap widened at v0.3 (25 → 28), so this fires harder, not softer.**

**OQ-6 · `TA-X-20` half-closes V17** *(carried)*. → **Adopt both halves and print the split:** `TA-X-20` clears the resolved predicate, `R2D-5` clears the drawn radius, and a green T-A clears only the first.

**OQ-7 · `M-POL` (G5) is in the seal and not in the arm set** *(carried)*. → **Leave it out.** The third inertness relation is not runnable at five arms, and a sixth arm buys one distinctness row against an arm the run is not porting.

---

*Filed 2026-09-20 by gandalf (named sub-agent, `SPEC-AUTHOR`), Wave 1, Run KC2-PLAY. **v1.3 / v1.2 / v1.1 / v1.0 not edited; superseded readings named in place at § A.** **All seven pins AND all three sealed-cell digests derived this session by `shasum -a 256`, never retyped** — and one of the three "believed unchanged" pins had moved. **No width transcribed.** **K-7 held** — the three sealed cells were reached by digest and byte count only, never opened. **Law 3 held; every predicate in this file was run against the documents, and the commission's item 5 was superseded by a document that landed before this one.** No production code, no dispatch, no push.*
