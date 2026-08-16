# KC2-PM4 · LAP AB — THE REFERENT'S MARCH DISPERSION + TWO CARRIED ITEMS · PRE-REGISTRATION

**Agent:** legolas (UNKNOWN-RESEARCHER) · **Conductor:** gandalf (RUN-CONDUCTOR)
**Commissioned by:** `R-PM4-70 part 3` (ledger `L-60`) · **Date:** 2026-08-16
**Charter:** `agentic_orchestration/gandalf/notes/2026-08-13-kc2-pm4-replication-run-charter.md`
**Written and committed ALONE, before any instrument of this lap exists.**
**Hash stamp:** authored `2026-08-16T09:04:53Z`.

---

## § 0 — RECONNAISSANCE DECLARED (Lap U § 0 convention, adopted)

Reconnaissance was performed BEFORE this file was hashed, and is declared here in full so that
nothing below can be mistaken for a prediction made in ignorance. Everything in this section is a
*feasibility* observation, not a finding, and **none of it is graded**. Every number below is
re-derived from scratch by this lap's instruments or it does not appear in the findings.

1. **Pinned-artifact inventory read** (the Lap Y lesson, applied first): Lap R findings §§ 1/5.2/5.4,
   Lap T findings §§ 3.1–3.5 + T-11 + `UNREACHED-T1`, Lap U findings § 0/§ 1.4–1.7 +
   `pm4u_ramp_analysis.json` + `pm4u_arrival_stats.json` + `pm4u_arrivals.csv` header +
   `pm4u_geometry_v3.csv` header, Lap AA findings §§ 2.4/3.1–3.3/5.1–5.2/6, Lap PM3-C `README.md § 1`.
   **⚑ The deciding record for fork (a) DATA SIDE is substantially ALREADY PINNED by Lap T § 3.1**
   (three independent negatives on Crucible wave-scaling and roster run-speed modifiers). This lap's
   data side is therefore scoped as *(i) re-verify the pins from my own seat, (ii) decode the surface
   Lap T did NOT read.*
2. **Corpus reachable.** All seven `.arz` layers open under the project's `gd_arz_adapter_2026_07_24`;
   `templates.arc` and `resources/Creatures.arc` open under `gd_arc_reader_2026_07_26`; `Game.dll`
   and `Engine.dll` open under `pm4s_pe_2026_08_14.PE32`. A small number of `templates.arc` entries
   raise on decompress; the instrument must count and publish them rather than silently skip.
3. **Fork (b) feasibility:** `resources/Creatures.arc` carries **1,770 `.anm` files**, magic `ANM\x02`,
   with a fixed 16-byte numeric header before a length-prefixed bone name. 38 entries carry `alert`
   in the path. A trial ratio `filesize / (hdr[0] × hdr[1])` sat near a constant on five sampled
   files. **This is a hypothesis about the header layout, not a decode** — § 4.2 states the test that
   must pass before any duration is published.
4. **Fork (b) risk identified in recon and carried into § 4.2 as a named decoy:** a naive
   "literal-order in `Game.dll` `.rdata` == `AnimationSet_Type` enum" mapping puts ordinal `0x21` on
   a **`SpecialAnim`** slot, not on `AlertAnim1`; and the recon filter that produced that ordering is
   **known to be defective** (its regex dropped two-digit `SpecialAnimNN` names, so the ordering it
   printed has a hole in it). Separately, `charanimationtable.tpl` field order puts `AlertAnim1` at a
   *different* ordinal again. **Two candidate orderings already disagree.** No ordinal→slot claim may
   rest on either without the § 4.2 three-start convergence.
5. **Fork (c) feasibility:** `pm4u_geometry_v3.csv` carries 120 per-spawn-point rows with
   `to_nearest_patrol_m`, `to_patrol_centroid_m`, `placement_extents_m` and a `parse_complete` gate —
   exactly the point set fork (c) needs, already pinned and already repaired (`D-I20-1`).
6. **Nothing in the sim's cells, code, or telemetry was opened during recon and none will be opened
   during this lap.** Outcome firewall, as standing.

---

## § 1 — WHAT THIS LAP IS, AND THE LAW IT RUNS UNDER

The run's ring occupancy sits ~17× below the referent's with the spawn structure verified
referent-true (`I-26`, `L-60`). Gamora's pre-code decomposition points at **the speed spread**: the
tier-16 roster's per-record `characterRunSpeed` values are decode-true and span a wide band, which
over a ~33 m march carries an order of magnitude more arrival spread than any other measured source.

**The question no lap in this run has asked: is the REFERENT's march equally dispersed, or does
something in the referent compress it?**

**Law 3 (charter):** measured decode of the referent is authorized; **referent numbers are GRADES for
the sim, never inputs.** Nothing this lap emits is a fold instruction.

**`D-CON-6` orientation-only law:** every number in the commission that fired this lap is orientation
only. In particular the commission's *"1.83–4.74 m/s"* is **not** pinned here: it is a product of a
decode-true scalar band with the **`UNREACHED-T1` conversion constant**, which Lap T carries as a
**two-edge bracket** (`3.055412` / `3.209466` m/s per unit, INFERRED-WITH-EVIDENCE). Under the
`R-PM4-70 part 4(ii)` law — **brackets stay brackets** — this lap will publish every m/s quantity on
**both edges** and will never render that bracket as a scalar. If the findings contain a single-edge
m/s number anywhere, that is a defect and must be filed as one.

**`R-PM4-70 part 4(i)` law:** any falsifier on a distributional statistic declares its like-for-like
window **in the criterion**. § 5's `F-AB-1` does so explicitly.

---

## § 2 — EVIDENCE HIERARCHY (binding; ties broken downward, never averaged)

1. **DECODED** — read out of shipped bytes: `.arz` record fields, `.arc` payloads, `.anm` headers,
   or instructions/literals in `Game.dll` / `Engine.dll`. Requires the exact
   artifact + record path or module + RVA/offset (`D-V2-1`).
2. **MEASURED** — computed by an instrument in this lap from a pinned artifact, with the artifact's
   full-64-hex sha256 asserted at instrument start.
3. **IMPORTED-BY-IDENTITY** — a prior lap's number, taken from that lap's **emitted artifact** with
   its digest re-hashed and asserted, never restated from prose (`R-PM4-67 part 2`).
4. **CORROBORATION** — an independent signal that agrees with a class-1/2 finding. **May never
   establish** a finding on its own; may only strengthen or contradict one.
5. **UNREACHED** — the honest negative, with the obstacle **named**. Preferred over any estimate.
   `GL-12`: decode, never estimate.

**No designation by grade** (`R-PM4-27 part 3`): nothing in this lap's findings elects, ranks, or
recommends anything for the sim.

**New mechanisms beyond the three forks: NAME, do not decode** (`R-PM4-56 part 4`). A `NAMED-AB-*`
tag, one line, and stop.

---

## § 3 — VERDICT CLASSES

Every deliverable below lands in exactly one of:
**DECODED** · **DECODED-NEGATIVE** · **MEASURED** · **MEASURED-NEGATIVE** · **CORROBORATION** ·
**UNREACHED** · **NAMED** (mechanism named, not decoded).

A verdict of **MEASURED-INACTIVE** is additionally available for a term that exists in the corpus and
is decoded to *not fire* in the referent's context (the Lap R § 5.1 convention). It is emitted, never
dropped, so the exclusion is legible.

---

## § 4 — THE THREE FORKS: DELIVERABLES, METHODS, DECOY SETS

### 4.1 FORK (a) — THE REFERENT'S MARCH DISPERSION

#### 4.1.1 DATA SIDE — instrument `I-AB-1`

**Question, stated exactly:** do Crucible-context modifiers act on monster movement speed for the
tier-16 roster, and if so by how much — and does any of them act to **compress the spread** rather
than shift the mean?

**⚑ THE DECOY SET, ENUMERATED (`D-Z-1` / `D-AA-1` guard).** Speed fields have decoys at several
layers. The instrument must read the **complete** field surface from `templates.arc` and publish it,
so that a chosen field is visibly chosen rather than accidentally found. The surface recon located
(to be re-derived exhaustively, not trusted from this list):

| family | fields | why it is a decoy for this question |
|---|---|---|
| base scalar | `characterRunSpeed` | **the target**; Lap R/T read it |
| base modifiers | `characterRunSpeedModifier`, `characterRunSpeedMaxModifier`, `characterRunSpeedJitter` | `Modifier` is the one Lap T proved zero; `MaxModifier` and `Jitter` are **different fields with similar names** |
| **⚑ second multiplier layer** | `characterTotalSpeedModifier` | **Lap T's `pm4t_march_speed.csv` does NOT carry this column.** A distinct layer; must be read, not assumed inert |
| applied slow (offensive) | `offensiveSlowRunSpeed{Min,Max,Chance,DurationMin,DurationMax,DurationModifier,DurationModifierChance,Global,Modifier,ModifierChance,XOR}` | the **only** family that can act *during* a march; `Min`/`Max` vs `Modifier` vs `Global` are three different semantics |
| applied slow (total) | `offensiveSlowTotalSpeed{Min,Max,Chance,DurationMin,DurationMax,Global,XOR}` | a **different stat** from RunSpeed; conflating the two is the trap |
| retaliation | `retaliationSlowRunSpeed{…}`, `retaliationSlowTotalSpeed{…}` | fires on the *player being hit*, not on the march |
| defensive | `defensiveTotalSpeedChance`, `defensiveTotalSpeedResistance`, `defensiveTotalSpeedMaxResist` | monster **resistance** to the above — changes magnitude, not direction |
| engine caps | `monsterRunSpeedCapMin/Max`, `bossRunSpeedCapMin/Max`, `absoluteRunSpeedCapMin/Max`, `playerRunSpeedCapMin/Max` | **caps, not multipliers**; `absoluteRunSpeedCapMin` is a **per-difficulty array** and is the closest thing to a difficulty-tier term |
| UI | `tab1RunSpeed*`, `tab2RunSpeed*`, `tab2PetRunSpeed*` | display strings; never a mechanic |
| animation | `*AnimSpeed*`, `activateAnimationSpeed`, `activeAnimationSpeed`, `WaveSpeed`, `TrailShrinkSpeed` | **not locomotion** — the largest decoy family by count |
| record-path decoys | any `records/sandbox/**`, `records/ingameui/**`, `**/backup/**`, `copy of *` | the `D-Z-1` class exactly: Lap AA found `records/ingameui/gameengine.dbr` carrying a *different* `alertDistance`. Every shipped-record claim must cite the **exact path** and the instrument must publish the non-shipped near-misses it excluded |

**Legs (each lands its own verdict):**

* **`A-d1` PIN RE-VERIFY.** Re-read from my own seat, and assert against Lap T's emitted
  `pm4t_march_speed.csv` (digest asserted): `characterRunSpeedModifier` on the roster; the run-speed
  surface of `balancingadjustment_survivalmode_enemies01/02/03` reached through `survivalinfo.dbr`.
  Verdict class: DECODED-NEGATIVE (expected) or a **contradiction to be published loudly**.
* **`A-d2` THE UNREAD LAYER.** `characterTotalSpeedModifier` (and `characterRunSpeedMaxModifier`)
  across the tier-16 roster and across all 790 roster records. Never read by this run before.
* **`A-d3` THE PURCHASED DEFENCES.** Lap PM3-C pinned that the referent bought **four defence-site
  constructions and zero celestial blessings** (Deathchill / Stormcaller / Inferno Beacons +
  Vanguard Banner), and named `turretice_icebolt.dbr :: offensiveSlowRunSpeed`. Walk all four
  records' full skill chains and decode **every** run-speed-family term that lands on monsters:
  magnitude, chance, duration, and the **radius/range within which it can act**. This is the one
  candidate in the corpus that can act on a *march in progress*.
* **`A-d4` THE COUNTERFACTUAL BLESSINGS.** The four celestial blessings, walked for run-speed terms
  and published **flagged MEASURED-INACTIVE for the referent** (not purchased, per Lap PM3-C). The
  commission asks; the answer is published; the inactivity is stamped on every row.
* **`A-d5` DIFFICULTY-TIER TERMS.** Probe for any difficulty-indexed run-speed multiplier:
  `gameengine.dbr`'s per-difficulty arrays, and an enumerated search of the corpus for records whose
  run-speed-family fields are non-neutral AND whose path or fields indicate difficulty indexing.
  Expected outcome UNREACHED-or-negative; either is publishable, an estimate is not.
* **`A-d6` HERO/CHAMPION MODIFIERS.** Lap T bucketed always-on/conditional/transient speed terms
  **on the 790-record roster**. The open question is whether the Crucible applies *additional*
  spawn-time modifier records (champion/hero affix-style) beyond the rolled records. If the path is
  decodable in-lap, decode it; **if not, it is NAMED, not estimated** (`NAMED-AB-*`).
* **`A-d7` THE DISPERSION QUESTION ITSELF.** For every term that fires, classify its action on the
  roster's speed **distribution**: `SHIFT` (moves the mean), `COMPRESS` (reduces the spread),
  `EXPAND`, or `NONE`. **This is the deliverable the commission actually asks for**, and it is
  reported even when every term's answer is `NONE`.

#### 4.1.2 VIDEO / TRACK SIDE — instrument `I-AB-2` (re-query only)

**The Lap Y lesson governs: the deciding record may already be pinned.** This leg re-queries
ALREADY-PINNED Lap R and Lap U artifacts under the new question. **Raw video will NOT be re-opened.**
If the pins are insufficient, the answer is **UNREACHED with the obstacle named** — not a new
video pass.

* **`A-v1` PER-WAVE ARRIVAL CLUSTERING.** From Lap U's pinned ramp artifact: the referent's living-
  count ramp, its `t50` and `t90`, and — if the pinned artifact carries per-wave decomposition — the
  per-wave spread. **The like-for-like functional is the LIVING-COUNT ramp, not the entry-interval
  distribution:** Lap U's own `D-U-3` demoted `pm4u_arrivals.csv` to a **strict upper bound** on
  arrival rate that **MUST NOT be graded against a sim as-is**. That demotion is inherited in full.
  Any use of `pm4u_arrivals.csv` in this lap carries the caveat in-line or it is a defect.
* **`A-v2` PER-BODY APPROACH SPEEDS.** Interrogate whether the pinned track artifacts support a
  **per-body** approach-speed distribution. Recon indicates the tracks exist only inside an observed
  ~11.6 m frustum window near the player, i.e. over the last ~11 m of a 29–39 m march, and are
  contaminated by nameplate re-appearance. **The pre-registered expectation is that per-body march
  speed over the full march is UNREACHED from the pins**, and § 5 registers that as a prediction so
  it can fail. If it is reachable, it is measured and published on both bracket edges.
* **`A-v3` THE COMPRESSION TEST — the lap's headline arithmetic.** Take the referent's roster
  `characterRunSpeed` band (IMPORTED-BY-IDENTITY, Lap R/T artifacts), convert on **both** `UNREACHED-T1`
  edges, apply the **candidate-restricted** march-distance bound (Lap AA § 2.4, DO-NOT 5), and compute
  the **arrival-time spread the referent's own record band PREDICTS** if every body expressed its own
  scalar over the full march. Compare that predicted spread against the referent's **measured** ramp
  width from `A-v1`. Publish both, as a two-edge bracket, with the comparison stated as a ratio and
  **no cause attached**. Candidate compressors are NAMED (`A-d3`'s slow, the alert gate's per-body
  offset, pack co-location, the frustum window's own truncation, actor-weighting toward the modal
  1.00) and **none is elected** — election is the conductor's, on a later lap.

**Firewall on `A-v3`:** it is a **referent-internal** comparison. The sim's occupancy, the sim's
arrival gaps, and the sim's speed spread are not consulted, quoted, or graded against.

### 4.2 FORK (b) — `UNREACHED-AA-3`, THE ALERT ANIMATION LENGTH — instrument `I-AB-3`

**Named consumer (from the commission):** the sim's absolute arrival clock; `T2`/`T3` carry the
omission with sign known and magnitude not.

**Three sub-decodes, in dependency order. A failure at any one lands the whole fork UNREACHED with
that obstacle named — the later legs may not be run on an assumed earlier one.**

* **`B-1` THE ORDINAL.** What animation slot is `AnimationSet_Type` ordinal `0x21`, as read by
  `ControllerMonsterStateAlertBeforePursue::OnBegin` (`Game.dll 0x10109410`, Lap AA)?
  **Three-start convergence required** (standing discipline), from three *independent* starts:
  (i) the ordered animation-field literal block in `Game.dll` `.rdata`, enumerated **exhaustively**
  (the recon filter's two-digit bug repaired and the repair stated);
  (ii) the animation-table loader's field-read sequence, disassembled;
  (iii) an independent anchor — a *different* call site whose ordinal↔slot pairing is
  independently determined (e.g. a death, spawn, or run animation whose ordinal can be tied to its
  slot by a second route).
  **⚑ DECOY, DECLARED IN ADVANCE:** two candidate orderings already disagree (§ 0.4) — `.rdata`
  literal order puts `0x21` on a **`SpecialAnim`** slot; `charanimationtable.tpl` field order puts
  `AlertAnim1` elsewhere entirely. **Neither may be adopted without convergence.** If the three
  starts do not converge, `B-1` lands **UNREACHED** and fork (b) stops there.
* **`B-2` THE `.anm` DURATION LAW.** Decode the `ANM\x02` header sufficiently to establish frame
  count and frame rate. **Acceptance gate, declared before any file is parsed:** the header reading
  is accepted only if a structural invariant holds **across the whole 1,770-file population**, not
  on a sample — specifically that `(payload_bytes − header_bytes) / (field₀ × field₁)` is constant
  to within a declared tolerance across all files that parse, with the count of non-conforming files
  published. A sample-only agreement is **CORROBORATION and may not establish the law** (§ 2 class 4).
  The frame-rate field must be independently corroborated (a second route: a constant across the
  population is *consistency*, not *proof that it is fps*) or the duration is published as
  **frames, with the seconds conversion marked UNREACHED**.
* **`B-3` THE ROSTER JOIN.** Map the tier-16 roster records → their animation-table record → the
  alert slot's `.anm` path(s), `AlertAnimSpeed*` multiplier and `AlertAnimWeight*` pool weights.
  Publish the **distribution** of alert durations over the roster (weighted by the pool weights and
  by rostered actor count), on the population that resolves, with the unresolved count published.

**⚑ THREE THINGS FORK (b) MAY NOT CLAIM, declared now:**
1. That the animation length **is** the state duration. Lap AA decoded `OnEnd` as a bare `ret` and
   did not decode the state's **exit condition**. If the exit condition is not decoded in-lap, the
   deliverable is *"the alert animation's length is X"*, and *"therefore the state lasts X"* is
   **UNREACHED** and stated as such.
2. That the body is immobile during it (Lap AA DO-NOT 4, carried).
3. A duration for the *anger* limb of the gate (`NAMED-AA-1`, carried).

### 4.3 FORK (c) — `OBS-I26-1` DISPOSITION — instrument `I-AB-4`

**The contradiction to be ruled:** Lap AA § 5.2 says the alert gate holds for *"essentially every
body"* (spawns 29–39 m out vs `alertDistance = 6.0`); Lap AA § 2.4's candidate-restricted distance
bound has **minimum 0.112 m**; gamora measured a **14.29 %** pack split at the sim's own near
emitter. These cannot all stand unqualified.

**Semantics, pinned before computing** (getting this backwards would invert the whole answer): the
decoded gate at `Game.dll 0x1010a360 +0x35f` is `if (d <= alertDistance) goto skip` — a body **inside**
6.0 m **SKIPS** the alert and goes straight to Pursue. "The gate holds" = the body is **outside** 6.0 m
and **does** enter the alert state.

**Method — no new source is opened; both inputs are pinned:**
* Point set: `pm4u_geometry_v3.csv`, IMPORTED-BY-IDENTITY, digest asserted, `parse_complete` gate
  honoured, split **candidate arenas (a/b/e)** vs all 20 — **the candidate-restricted figure governs**
  (Lap AA DO-NOT 5).
* Scatter law: Lap AA § 3.2 — polar, **uniform in ρ** (not area), `ρ ~ U(0, placementExtents)`,
  `θ ~ U(0, 2π)`, `placementExtents = 8.0`. **DO NOT model as a uniform disc** (Lap AA DO-NOT 2).
  The fold-relevant object is the **SHAPE**, not the CRT `rand` stream (Lap AA DO-NOT 2 / `R-PM4-69`).
* Compute `P(d_body ≤ 6.0)` per spawn point analytically over the exact `U(0,E) × U(0,2π)` law, plus
  a large-N draw as an **independent second route** (agreement = CORROBORATION of the analytic form;
  disagreement = a defect to publish).

**⚑ THE NAMED WEAKNESS, declared before the number exists.** The gate's `d` is monster→**enemy**
(the player). **The player's per-wave world position is not pinned by any artifact in this run.**
The computation therefore runs against **named proxies** — `to_patrol_centroid_m` and
`to_nearest_patrol_m` — and the result is published as a **bracket across proxies**, with the
player-referenced fraction marked **UNREACHED** and the proxy substitution stated in every row's
basis. Lap U's `implied spawn → player ≈ 21–22 m` is itself INFERRED-WITH-EVIDENCE and may be cited
as CORROBORATION only, never as the distance.

**The disposition to be ruled** — one of exactly these, chosen by the number:
(i) AA § 5.2 stands as written; (ii) AA § 5.2 stands **with a named qualifier** and the qualifier is
supplied verbatim for downstream carry; (iii) AA § 5.2 is **too strong** and is corrected here; or
(iv) **UNREACHED**, with the missing artifact named. **This is load-bearing for anyone who folds the
gate later, so the qualifier — if any — is written as a quotable sentence.**

---

## § 5 — PREDICTIONS, GRADED AT THE END WORDING-UNCHANGED

Each is graded **PASS / FAIL / UNGRADED (leg did not reach)**. A FAIL is a finding, not an
embarrassment; the wording is frozen at commit and is reproduced verbatim in the findings.

| # | prediction | falsified by |
|---|---|---|
| **P-1** | Lap T's three negatives re-verify from my own seat: `characterRunSpeedModifier` is `0.0` on every roster record, and the run-speed field surface of all three `balancingadjustment_survivalmode_enemies0{1,2,3}` records is zero. | any non-zero |
| **P-2** | `characterTotalSpeedModifier` — the layer Lap T's artifact does not carry — is **also** neutral (absent or `0.0`) on the tier-16 roster. | any non-neutral value on a rostered record |
| **P-3** | At least one **purchased** referent defence carries a run-speed-family term that lands on monsters, with a **finite radius** smaller than the march. | no purchased defence carries such a term |
| **P-4** | No decoded term acts to **COMPRESS** the roster's run-speed spread. Every term that fires classifies as `SHIFT` or `NONE` under `A-d7`. | any term whose action is spread-reducing |
| **P-5** | **Per-body approach speed over the full march is UNREACHED from the pinned track artifacts**, because the pinned tracks exist only inside the observed frustum window near the player. | a per-body full-march speed distribution is recoverable from the pins |
| **P-6** | The referent's **measured** ramp width (`t90 − t50`, living count) is **smaller** than the arrival-time spread its own roster `characterRunSpeed` band predicts over the candidate-restricted march, on **both** `UNREACHED-T1` edges. | measured ≥ predicted on either edge |
| **P-7** | The three candidate orderings for `AnimationSet_Type 0x21` do **not** all agree on first inspection, and at least one recon-level candidate is refuted by the three-start convergence. | all starts agree immediately |
| **P-8** | The `.anm` bytes-per-key invariant of `B-2` holds across **≥ 95 %** of the 1,770-file population. | < 95 % conform |
| **P-9** | The alert-slot `.anm` durations over the tier-16 roster are **not** a single constant — they vary by rig by at least a factor of two. | the distribution is degenerate or spans < 2× |
| **P-10** | Fork (c): the fraction of referent spawn **placements** falling inside the 6.0 m gate radius is **non-zero but small** — strictly between 0 % and 25 % — on the candidate-restricted point set under **both** proxies. | 0 %, or ≥ 25 %, under either proxy |
| **P-11** | Fork (c) resolves to disposition **(ii)** — AA § 5.2 stands *with a named qualifier* — rather than (i), (iii) or (iv). | any other disposition |
| **P-12** | No fork of this lap requires opening the referent video, the sim's cells, or any source outside the pinned corpus + pinned prior-lap artifacts. | any such source is opened |

**Pre-registered falsifier `F-AB-1`, with its like-for-like window declared IN the criterion
(`R-PM4-70 part 4(i)`):**

> **`F-AB-1`.** *The referent's march is dispersed as much as its own record band predicts.*
> **Window:** the comparison is made **per wave**, over the **same ten waves 151–160**, between
> (x) the referent's measured living-count ramp width `t90 − t50` and (y) the ramp width predicted
> by the roster's actor-weighted `characterRunSpeed` distribution over the candidate-restricted
> march distance, on **each** `UNREACHED-T1` edge separately, **never pooled across edges**.
> If the pinned artifacts do not carry a per-wave ramp, the window degrades to **pooled across the
> ten waves** and **that degradation is declared in the grading, not silently taken**.
> **`F-AB-1` HOLDS** if (x) ≥ (y) on either edge — the referent is as dispersed as its records
> predict, and the sim's speed spread is referent-true and is **not** the next address.
> **`F-AB-1` FAILS** if (x) < (y) on both edges — something in the referent compresses the march,
> and the compressor is the next question. **If it fails, this lap NAMES the candidates and elects
> none.**

---

## § 6 — DISCIPLINE STACK (standing, asserted here in full)

* **`GL-12`** decode-never-estimate. Every UNREACHED names its obstacle.
* **`GL-6`** full **64-hex** sha256 on every artifact consulted and every artifact emitted. Digests
  are computed **after the final write** and the findings quote what was computed
  (`D-AA-5`: the run has already banked one stale-digest report defect).
* **`D-V2-1`** every claim cites the exact artifact / record path / module + offset.
* **`D-Z-1` / `D-AA-1`** decoy sets **ENUMERATED, not avoided**. Publishing the near-misses is the
  guard; § 4.1.1 and § 4.2 pre-enumerate them.
* **Three-start convergence** on any disassembly-derived claim.
* **`NOTE-9`** no repair outside my own seam; prior instruments imported unchanged.
* **`R-PM4-67 part 2` / `D-CON-6`** prior-lap numbers imported from **artifacts**, never from prose.
* **`R-PM4-70 part 4(ii)`** brackets stay brackets; an unruled bracket is never rendered as a scalar.
* **No designation by grade** (`R-PM4-27 part 3`).
* **Read-only** on `/Users/admin/Games/vendor/**` and on every prior lap's notes. Writes only into
  this lap's directory and `agentic_orchestration/research/scripts/`.
* **Outcome firewall:** no sim artifact is opened by any leg.
* **Determinism:** every instrument is run twice and the emitted artifacts must be byte-identical.
* **DO-NOT blocks carried unchanged:** Lap V § 7.2, Lap V-2 § 11.2, Lap W § 7.2, Lap X § 12.2,
  Lap Y § 11.6, Lap Z § 5, **Lap AA § 6 (all eight)**. In particular AA DO-NOT 2 (never a uniform
  disc), DO-NOT 3 (never estimate the alert duration), DO-NOT 4 (never claim immobility), DO-NOT 5
  (the candidate-restricted arena bound governs).

---

## § 7 — COMMIT PLAN

1. **This file, ALONE**, in its own commit — before any instrument of this lap exists.
2. Instrument(s) under `agentic_orchestration/research/scripts/` + emitted artifacts + a
   `pm4ab_findings.md` carrying: full-64-hex digests **consulted and emitted**, a binding **DO-NOT
   block**, a **defect table** (self-caught defects declared, not hidden), an honest **UNREACHED
   census**, and § 5's predictions graded **wording-unchanged**.
3. **DO NOT PUSH.**
