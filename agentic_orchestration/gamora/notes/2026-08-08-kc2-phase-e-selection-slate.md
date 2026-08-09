# KC2 Phase E — the SLATE: selection re-run under R-KC2-13, and the flip materialized

**Date:** 2026-08-08
**Author:** gamora (simulation seam)
**Commission:** L-78(d) — conductor-fired, named-agent (OP § 4.10)
**Ruling applied:** **R-KC2-13** (Matt, Q54, *"E-1′ as leaned"*, 2026-08-08) — ledger row **L-78**
**Population:** the SAME 20 runs, engine results JSON at engine commit `4ce23b66`
(`src/reincarnated/simulation/output/kc2-phase-e-seeded-batch-full-20260808_205104.json`)
**Predecessor note:** `2026-08-08-kc2-phase-e-seeded-batch.md` (the HALT + § 3.4 counterfactual)
**Grade (R-KC2-7):** every quantity below is **MEASURED** — recomputed from the committed artifact.
The § 3.4 **COUNTERFACTUAL** label **RETIRES** for this output; this is a **SLATE**.

> **NO new simulation was run. NO filter was relaxed. `filters_relaxed` remains `false`.**
> This note is pure selection arithmetic over data that already existed. Nothing in the engine
> tree was touched; the artifact JSON was **read, not rewritten** (see § 6.3 on the stale
> `terminal_admissible` field).

---

## 1 · What changed, and what did not

| Element | Status under R-KC2-13 |
|---|---|
| Population (20 runs = 10 seeds × {wave-1, checkpoint-150}) | **UNCHANGED** |
| Filter — band relevance | **UNCHANGED** → the 10 `*-cp150` runs |
| Filter — narrative shape, **wall test** (`max ratio ≥ 1.5`, math note § C.4) | **UNCHANGED** |
| Filter — narrative shape, **terminal clause** | **RE-SCOPED** — instrument terminals `ehp_band_exhausted` / `arena_tier_exhausted` are **ADMISSIBLE-BY-DECLARATION** per R-KC2-13 |
| Filter — mechanism coverage | **UNCHANGED** |
| Filter — technical cleanliness (zero anomaly flags) | **UNCHANGED** |
| **Rank keys** | **RESTATED** — reproduction-fidelity: primary `|W* − 159|` ASC · tb-1 ratio DESC · tb-2 uptime DESC |
| Duration-agreement keys | **EXCLUDED** from the rank (F-6/F-7 → the baton's divergence ledger) |
| `filters_relaxed` | **`false`** — asserted in the artifact, unchanged |

### 1.1 Filter-numbering reconciliation — stated so the two notes can be read together

The commission numbers the four pre-registered classes **1 = band relevance · 2 = narrative shape ·
3 = mechanism coverage · 4 = technical cleanliness** (charter § 4 rule 5's class list, in order).
My batch note § 3.2 used a **local** numbering in which "filter 2" fused the anomaly-flag test with the
terminal-state clause. **The arithmetic is identical either way**; only the label moves. Under the
charter's own numbering the re-scoped clause belongs to **narrative shape**, and **technical
cleanliness passed 20/20 all along** (§ 2.1 of the batch note) — it was never the blocker. The blocker
was, and is now discharged as, the **terminal clause**.

---

## 2 · Filters applied

### 2.1 Filter 1 — band relevance (HARD): **10/20 pass** — UNCHANGED

10 `*-cp150` runs fight waves 151…160 (all ten band waves). 10 `*-w1` runs reach deepest wave 93 and
contribute **no** band waves — they fail for the geometric reason recorded at F-4 (`ARENA_S1` carries
p01 placements to tier 15 = wave 150, one short of the band; `Arena.merge` forbids pooling per L-21).
**The 10 wave-1 runs are excluded from the slate and do not appear in the rank below.**

### 2.2 Filter 2 — narrative shape: **10/10 of the band-reaching runs pass**

**Wall limb (UNCHANGED):** `max ratio ≥ 1.5` — passes **10/10**. Range 1.6667 … 2.0833.

**Terminal limb (RE-SCOPED per R-KC2-13):** all 10 terminate `arena_tier_exhausted` at wave 171
(`simulate_wave(171)` raises `KeyError: sm1/survivalworld_a.map has no p01_tier18`), class
**INSTRUMENT** → **ADMISSIBLE-BY-DECLARATION (R-KC2-13)**: the legitimate ending of a kit-throughput
instrument per R-KC2-12 § 1.1, to be **DECLARED in the baton provenance**. Cited per run in § 3.

**Death sub-limb:** reported **`False` with its reason**, never silently dropped — player death is
structurally unreachable (batch note F-2: 0 emitters of `player_death`, 0 rows with
`target_id="player"`, 0 post-init writes to `hp_player`, monster attack model `abstract-schedule`
emits no monster-side damage). Unchanged by this ruling.

### 2.3 Filter 3 — mechanism coverage: **10/10 pass**

Channel uptime **90.20 – 91.49 %** of alive-time (100.000 % of engagement-time on 10/10); aura
reservation **982.0 absolute, 100.0 % of alive-time, 10/10**. **RF stacks are STRUCK from the class**
(RF DISSOLVED at Phase B) — the fixture carries none and none was evaluated.

### 2.4 Filter 4 — technical cleanliness: **10/10 pass**

Zero anomaly flags across all five classes on all 10 (and on all 20 — 1,130 wave-simulations, zero
flags of any class).

### 2.5 Composition

```
filters 1 ∧ 2 ∧ 3 ∧ 4  →  survivors = 10        (was ∅ pre-ruling)
rank                   →  reached, 10 runs ranked
TOP-3                  →  POPULATED
```

---

## 3 · SLATE — all 10 passing runs, ranked

Wall detector reproduced **verbatim** from the driver (`wall_detection`, math note § C.4):
`trailing5_median(i) = median(c[i−5 … i−1])`, `ratio(i) = c[i] / trailing5_median(i)` for `i ≥ 6`,
`W* = argmax ratio`. Rank keys per **L-78(c)**, pinned BEFORE this re-run.

| rank | run id | W* | **\|W*−159\|** | ratio | uptime % | clear @ W* (s) | trailing-5 med (s) | terminal class | admissibility |
|---:|---|---:|---:|---:|---:|---:|---:|---|---|
| **1** | **`E-s09-cp150`** | **161** | **2** | 1.7500 | **91.487** | 21.0 | 12.0 | `arena_tier_exhausted` / INSTRUMENT | **ADMISSIBLE-BY-DECLARATION (R-KC2-13)** |
| **2** | **`E-s01-cp150`** | **156** | **3** | **2.0833** | 90.678 | 25.0 | 12.0 | `arena_tier_exhausted` / INSTRUMENT | **ADMISSIBLE-BY-DECLARATION (R-KC2-13)** |
| **3** | **`E-s03-cp150`** | **156** | **3** | **2.0000** | 91.210 | 24.0 | 12.0 | `arena_tier_exhausted` / INSTRUMENT | **ADMISSIBLE-BY-DECLARATION (R-KC2-13)** |
| 4 | `E-s08-cp150` | 156 | 3 | 1.9231 | 90.624 | 25.0 | 13.0 | `arena_tier_exhausted` / INSTRUMENT | ADMISSIBLE-BY-DECLARATION (R-KC2-13) |
| 5 | `E-s07-cp150` | 156 | 3 | 1.7857 | 90.801 | 25.0 | 14.0 | `arena_tier_exhausted` / INSTRUMENT | ADMISSIBLE-BY-DECLARATION (R-KC2-13) |
| 6 | `E-s02-cp150` | 156 | 3 | 1.7333 | 90.841 | 26.0 | 15.0 | `arena_tier_exhausted` / INSTRUMENT | ADMISSIBLE-BY-DECLARATION (R-KC2-13) |
| 7 | `E-s05-cp150` | 156 | 3 | 1.6667 | 90.203 | 25.0 | 15.0 | `arena_tier_exhausted` / INSTRUMENT | ADMISSIBLE-BY-DECLARATION (R-KC2-13) |
| 8 | `E-s04-cp150` | 167 | 8 | 1.8750 | 90.945 | 30.0 | 16.0 | `arena_tier_exhausted` / INSTRUMENT | ADMISSIBLE-BY-DECLARATION (R-KC2-13) |
| 9 | `E-s06-cp150` | 167 | 8 | 1.8125 | 91.249 | 29.0 | 16.0 | `arena_tier_exhausted` / INSTRUMENT | ADMISSIBLE-BY-DECLARATION (R-KC2-13) |
| 10 | `E-s10-cp150` | 167 | 8 | 1.7059 | 91.379 | 29.0 | 17.0 | `arena_tier_exhausted` / INSTRUMENT | ADMISSIBLE-BY-DECLARATION (R-KC2-13) |

**TOP-3:** `E-s09-cp150` · `E-s01-cp150` · `E-s03-cp150`
**TOP-1:** **`E-s09-cp150`** (conductor-seed 9, `seed_first_wave` 601 008, arena `sm1/survivalworld_a`,
waves 151–170, terminal `arena_tier_exhausted` @ 171).

**Tiebreak-2 was never reached.** Every `|W*−159|` tie (the six-run W*=156 group; the three-run W*=167
group) resolved on tiebreak-1 — no two runs share a ratio. Uptime is reported for completeness only.
Note that had tb-2 been decisive within the W*=156 group it would have **reordered** it: uptime ranks
s03 > s02 > s07 > s01 > s08 > s05, which is close to the *inverse* of the ratio order. The keys are
near-orthogonal on this population; the pin's ordering of them is load-bearing.

**Rank-key completeness:** `W*` for the excluded wave-1 limb is **13 on 10/10** (ratios 2.6429–3.2308)
— all fail filter 1 and none enters the slate.

---

## 4 · THE FLIP — it materialized, exactly as L-78 pre-stated

**YES.** The ranking flipped.

| | § 3.4 counterfactual (pre-ruling) | **SLATE (R-KC2-13)** |
|---|---|---|
| top-1 | `E-s01-cp150` (W*=156) | **`E-s09-cp150` (W*=161)** |
| top-2 | `E-s03-cp150` | `E-s01-cp150` |
| top-3 | `E-s08-cp150` | `E-s03-cp150` |
| `E-s09-cp150` | **rank 9 of 10** | **rank 1 of 10** |

**Mechanism of the flip, stated plainly.** The counterfactual's primary key was the charter's original
rule-3 ordering — *wall-inside-[151,160] first, then wall depth*. `E-s09-cp150`'s wall sits at
**w161**, one wave outside the showcase band, which put it below every in-band run regardless of
depth. R-KC2-13 replaces that binary band-membership gate with a **continuous distance to w159**, and
under distance `|161 − 159| = 2 < |156 − 159| = 3`. **`E-s09-cp150` moves from rank 9 to rank 1 in a
single step — the largest rank movement on the slate, and the precise consequence L-78(c) named before
the re-run fired.**

**⚑ Named for the conductor, not buried.** The top-1's wall lies **outside** `[151,160]`. This is
**consistent with every filter as written** — filter 1 asks that the *run reach the band* (s09 fights
all ten of 151…160), while the rank asks that the *wall sit near w159*. Those are different
predicates and s09 satisfies both. But the two are no longer the same question, and the emitted baton
will carry a showcase run whose narrative peak is at **wave 161**. That is a property of the pinned
metric, ruled in advance, not a defect and not an improvisation. **Veto-open per L-78(b).**

### 4.1 Fidelity readout for the top-3 vs the feel reference (context, NOT a rank key)

Fixture wall: **w159 @ 26.25 s** (galadriel sitting 2, `MEASURED_S2_CLEAR_S`).

| run | wall wave | wall clear (s) | Δ wave vs w159 | sim @ w159 (s) | Δ vs 26.25 |
|---|---:|---:|---:|---:|---:|
| `E-s09-cp150` | 161 | 21.0 | **+2** | 10.0 | −16.25 |
| `E-s01-cp150` | 156 | 25.0 | −3 | 11.0 | −15.25 |
| `E-s03-cp150` | 156 | 24.0 | −3 | 11.0 | −15.25 |

The top-1 reproduces the wall's **position** better than the W*=156 group and its **magnitude** worse
(21.0 s vs the fixture's 26.25 s; the W*=156 group's 24–25 s is closer in seconds). The pinned key is
position, so position wins. **F-7's duration divergences — including the −16.25 s miss at w159 — ride
the baton's DIVERGENCE LEDGER per R-KC2-13, never the rank, and must not be silent** (Discipline #13
guard).

---

## 5 · No anomalies in the selection pass

- **Data completeness:** all rank inputs present for all 10 slate runs. No run required
  interpolation, substitution, or re-simulation. **No HALT condition arose.**
- **Detector reproduction:** the recompute reproduces the driver's `wall_detection` output and the
  batch note's § 3.4 W*/ratio column **exactly**, on 20/20 runs.
- `filters_relaxed` read back from the artifact: **`false`**.

---

## 6 · Errata against my own batch note, and one stale artifact field

Filed because they were found while recomputing, and a silent correction is worse than a loud one.

### 6.1 F-6 prose — wrong count, non-load-bearing

F-6 reads *"`W* = 156` on **7/10** cp150 runs (the other three: 161, 167, 167)."*
**MEASURED census: `W*` = 156 on 6/10 · 161 on 1/10 · 167 on 3/10.** The § 3.4 **table** was correct;
only the F-6 **prose** miscounted. **STRIKE and replace** with: *"`W* = 156` on 6/10 cp150 runs (the
other four: 161, 167, 167, 167)."* F-6's substantive claim — that the wall is ~seed-invariant and the
rank discriminates waves rather than runs — is **unaffected**; 6/10 sharing one wave and 3/10 sharing
another is if anything the same finding.

### 6.2 § 3.4 table, row 7 (`E-s04-cp150`) — two cells wrong, ratio right

Listed `clear @ W* = 28.0`, `trailing-5 median = 14.9`. **MEASURED: 30.0 and 16.0.** The **ratio
1.8750 was correct** in the counterfactual and is correct here (30/16 = 1.875 exactly; 28/14.9 =
1.8792 does not equal the printed 1.8750, which is how the transcription error surfaced). **No rank
key is affected** — `E-s04-cp150` is rank 8 on both slates. Corrected in § 3 above.

### 6.3 `terminal_admissible: false` in the committed artifact is now STALE — deliberately not rewritten

Every cp150 run carries `terminal_admissible: false` in the JSON. That field records the **pre-ruling**
predicate as it stood at execution. **R-KC2-13 supersedes it at the selection layer.** I did **not**
rewrite the artifact: re-emitting it would destroy the pre-registration evidence that the filter was
applied strictly before the ruling existed, which is the whole reason the HALT is credible. The
admissibility is applied **here**, with its citation, per run. **Any downstream consumer (star-lord's
F-5 adapter, the baton provenance block) must read admissibility from R-KC2-13 / this slate, NOT from
the artifact's `terminal_admissible` field.** Flagged for the fold.

---

## 7 · What this slate does not claim

- It does **not** claim the band's physics improved. **F-1 stands** — MEASURED opposition eHP coverage
  on `[151,160]` is **2.92 %**, and on eight of the ten band waves the kill term is a declared zero.
  The ruling made the terminal clause satisfiable; it did not make the band measurable.
- It does **not** claim seed-level discrimination. **F-6 stands** — clear time is ~95 % wave-determined
  (seed CV median 6.4 %), which is *why* L-78(c) excluded duration keys. The slate orders runs by
  **where their wall landed**, and on this population that is a 3-valued quantity (156/161/167). The
  top-1 is the sole occupant of its key value.
- It does **not** re-open **F-KC2-E-2** (close the band-B eHP absence). That fork remains **NAMED, NOT
  TAKEN** and is the only one that makes the rank mean what its name says.

---

**Refs:** R-KC2-13 (L-78) · L-78(a)(b)(c)(d) · R-KC2-12 § 1.1 · R-KC2-7 · R-KC2-6 · R-L73-1 · L-75 F-7 ·
L-21 · charter § 4 rule 5 (amended) · § 6 (amended) · math note § C.4 · batch note §§ 2, 3.4, 5 (F-1/2/4/6/7).

**Artifact:** engine `4ce23b66` — `src/reincarnated/simulation/output/kc2-phase-e-seeded-batch-full-20260808_205104.json` (read-only).
**Engine tree:** untouched this lap. **COMMIT-ONLY, NO PUSH** (R-KC2-10 — the conductor pushes at fold).
