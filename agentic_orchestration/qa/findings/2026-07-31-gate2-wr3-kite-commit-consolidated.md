# Finding — 2026-07-31 — WR3-KITE-COMMIT consolidated Gate-2 (packet + stage-2c + anchor-refit)

**Reviewer:** jack-ryan
**Severity:** **PASS with 2 WARN, 0 BLOCK** (per-section verdicts below)
**Target:** engine `dbb2d6a9` (= `56881b52` + doc-only AGENT_STATE checkpoint); stage-2c at `f1039b3a` · `b20f1b9a` · `c3887bd3`
**Developer:** gamora (simulation seam); packet consolidated by gandalf (RUN-CONDUCTOR)
**Commission:** R-WR3-37(7) — Gate-2 on the consolidated packet + stage-2c + refit
**Packet:** `agentic_orchestration/qa/pending/2026-07-30-gandalf-wr3-gate2-consolidated.md`
**Principles applied:** 1 (math-before-code), 2 (smoke/full-regen gate), 3 (cross-seam impact), 4 (decisions-log as truth), 5 (severity matters), 6 (cross-seam round-trip)
**Disciplines cited:** #1, #8, #9, #10, #11, #12, #19/§19.2, #53, #63, #64, #65, #66, Pattern P7, Pattern P8, R11(b), ADR-002, ADR-004

> **STAGE-2 CLOSE IS NOT GATED BY THIS VERDICT'S WARNs.** Both WARNs are additive documentation
> edits with no measurement consequence. Owner-eye render (drax) → stage 2 CLOSES may proceed.
> The WARN remediations are owed at gamora's next simulation-seam session, not before the render.

---

## 0. Verdict summary

| Section | Verdict | Note |
|---|---|---|
| **§A** — three ledger corrections | **PASS** | all three verified against primary source |
| **§B** — six discipline candidates | **RATIFIED (4 numbers + 1 amendment + 1 pattern)** | six numbers deliberately not minted |
| **§C** — melee band pre/post-mit unit flag | **PASS-with-carry (INFO)** | code-site units already discharged; route target has moved |
| **§E-10** — still-live `getattr` in the s2c cell | **DISPOSITION ISSUED** | annotate artifact + tree-wide allow-list guard + strike at next re-run |
| **§E-11** — melee default-False debt tracking | **PARTIAL — WARN** | tracked at producer; absent at the consumer-facing surface |
| **§E-12** — conduct corollary | **RATIFIED** as Discipline #19 amendment §19.2 | not a new number |

**Landing quality, stated for the record.** This is the strongest evidence package I have reviewed
from this seam. Byte-inertness was PROVEN four ways rather than asserted; semantic shifts were
declared BEFORE implementation per Discipline #12; the anchor cell structurally cannot emit a band
verdict and a test pins that it never gains one; and the defect that voided a graded gate was found,
named, and routed *by the author* rather than by the gate. The two WARNs below are documentation
placement, not measurement.

---

## 1. §A — Ledger corrections: **PASS**

All three verified by empirical inspection against primary source (Discipline #11), not accepted on
report.

1. **U-1 premise FALSIFIED — VERIFIED.** `greatestDamageReceived` / `greatestDamageInflicted` are
   literal `Game.dll` strings in the contiguous `PlayStats` field-name block. Confirmed at
   `legolas/research/2026-07-30-wr3-veteran-characterization.md` §6.2, with the correct scoping
   preserved: the swap hypothesis stays dead (`lastHit` / `lastHitBy` remain unattested; the only
   near symbol, `Character::GetLastHitFrame`, is unrelated). The ledger correcting a *basis* while
   leaving the *conclusion* standing is the right shape — a conclusion that survives the repair of
   its own premise is stronger than one that was never tested.
2. **Arm-B confound re-characterized — VERIFIED.** Measurement supersedes the R-WR3-27(3) reading:
   the flag made icearmor PERMANENT (`tick_calls=0`, buff up 95.0 % vs clean 33.2 %), so
   ΔF2 = **+0.467 clean** (was +0.500 confounded), and every "kit-only" reading of arm B in
   R-WR3-25/27 carries the correction. This is Pattern P8's founding instance (§3 below).
3. **283.14 STRUCK; charter carries 95.36 — VERIFIED** at charter lines 902–904. The refutation is
   geometric and complete: three simultaneous far-band crossings where `n_bounds=(0,1)` is
   impossible as a per-event maximum. Struck at the source rather than annotated — correct, because
   an annotated-but-present number gets re-quoted.

**INFO (§A carry, no action):** legolas §6.1 banks a fourth item of the same family that the packet
did not route — the referent save's `play_stats.maxLevel = 12` while `character_bio.level = 13`, a
lagging high-water mark rather than a parse drift. I have folded it into Discipline #64 as the
**grain-form** third-seam instance; it is now covered rather than loose.

---

## 2. §B — Discipline candidates: **4 numbers + 1 amendment + 1 pattern RATIFIED; 0 DEFERRED**

Ratification is jack-ryan direct authority per **ADR-002**. All six candidates are ratified in
substance. **Six numbers were deliberately not minted**, on the **#58-DECLINED precedent** (a
candidate redundant with an existing body adds a founding instance, not a number) and on this
document's own extension protocol (*"Avoid bloat. Each discipline should be load-bearing and
durable."*).

| Packet item | Disposition | Landed as |
|---|---|---|
| 5 — conditionally-emitted counter blocks declare absence | **RATIFIED, MERGED** | **#63** clause (b) |
| 9 — the `get(k,0)` / `or 0` hazard class | **RATIFIED, MERGED** | **#63** clause (a) |
| 4 — charLevel standing check | **RATIFIED, GENERALIZED** | **#64** |
| 7 — full-sweep run law | **RATIFIED, PROMOTED** | **#65** |
| 8 — discriminator lost at the seam | **RATIFIED** | **#66** |
| 6 — state-object degeneracy class | **RATIFIED as a PATTERN** | **Pattern P8** |

### 2.1 Items 5 + 9 → **Discipline #63 — "Unmeasured is not zero"** (MERGED)

Submitted as two rules; ratified as one discipline with two clauses. **Rationale for merging:** they
are the emitter half and the reader half of a single proposition. Split across two numbers, a
codebase can satisfy one and violate the other while believing itself compliant — which is exactly
what the founding run did.

**The merge is not an editorial preference; the evidence forced it.** The same file that carries the
worst read-side instance already implements the emit-side rule correctly, forty lines later:

```python
# wr3_cell_s2c_2026_07_30.py
 88:  worst = max(worst, float(getattr(fr, "worst_received_event_hp", 0.0) or 0.0))   # ← VIOLATION
 93:      if v is not None:                      # None stays None: UNMEASURED != zero  ← COMPLIANT
113:      _n = lambda v: "  n/a" if v is None else "%5d" % v   # noqa: E731  absent != zero
```

A rule that a *compliant, rule-aware author* violates inside the same function does not need better
documentation — it needs mechanical enforcement. #63 therefore ships with an enforcement mechanism
that already exists in-tree: the AST-sweep-plus-explicit-allow-list pattern of
`tests/_door_opening_sites()` + `_DOOR_ALLOW_LIST` (`tests/test_bq3_calibration_override_door.py`).
`tests/test_wr3_anchor_refit.py::test_F2` is the single-file instance of exactly that shape; the
tree-wide sweep is its generalization, and the cost of ratifying is therefore near zero.

**Severity basis:** this is the highest-cost class in the run. Clause (a) **voided a graded gate** —
G-N3″ was graded PASS against a 260.50 ceiling on a `getattr` default. Verified: `SpatialFightResult`
carries no such field, and all **twelve** legs of `output/kitcal_g5/wr3_stage2c/wr3_stage2c.json`
carry `worst_received_event_hp: 0.0`. No assertion, band check, or schema validator can catch this —
`0.0` is inside every band a real measurement would also have been inside. That property is why #63
gets a number rather than a note, and why it now also extends the **#19.1 cheapest-refuting-test
table** with a `Graded gate PASS` row.

### 2.2 Item 4 → **Discipline #64 — Referent-binding declaration** (GENERALIZED)

Submitted as a `charLevel` standing check. Ratified in general form, because **the run's own evidence
generalized it past `charLevel` before the packet reached Gate-2** — the seam's MIGRATION entry §4
already names the precedent explicitly: *"Same prescription as R-WR3-27(5)'s `char_level` binding,
applied to a magnitude."* Ratifying only the `charLevel` form would have shipped a rule narrower than
its own founding evidence.

General form: **a field whose name underdetermines its referent must declare it at the site.** Three
attested forms: **rank** (instance 5 — the boss row carried `char_level=13`, *the player's level*,
while every other row in the file bound its own monster's), **magnitude** (`dmg_per_hit` becomes the
physical channel on a split row; a reader taking it as the total reads 77.4 % of it), and **grain**
(the `play_stats.maxLevel` high-water mark from §A above).

### 2.3 Item 7 → **Discipline #65 — Full-sweep run law** (PROMOTED)

In-run law at R-WR3-31(8), promoted to standing discipline. **The decisive instance is not the four
BQ-3 door occurrences — it is the stage-2c middle sweep**, where a labelled expectation authored in
good faith by a compliant author still missed a shipped digest-moving regression and two latent
defects. A rule justified by careless authors is weak; a rule justified by a careful one is not.

I have written the boundary against **Discipline #2** explicitly, because it is the obvious place a
future reader will try to collapse them: #2 governs SMOKE-vs-FULL-REGEN of *substrate*; #65 governs
the *test suite* at a landing boundary and **does not inherit #2's scale exemption** — a smoke-scale
change still gets the full sweep, precisely because the blast radius was not where the author looked.

**The anchor-refit sweep is banked in #65 as the compliant exemplar:** run to completion without
`-x`, name-diff against a NAMED baseline commit, both name sets recorded, `+31 passed` reconciled
exactly to the new file's collected count, and the new modules proven tracked rather than assumed.

### 2.4 Item 8 → **Discipline #66 — Discriminator survival**

Ratified with an explicit distinction paragraph against the two neighbours it would otherwise be
folded into, because that distinction is the whole content of the rule:

- **Pattern P7** = absence — the consumer gets nothing, and a presence check finds it.
- **R11(b)** = contract change — needs a round-trip smoke.
- **#66** = **conflation** — every field present, every value valid, two upstream-distinct kinds
  arriving as one downstream shape. Founding instance 2 is exact: an unqualified circle-test passes
  on a blizzard it believed was a nova, **and reports PASS**.

The three founding instances landing in ONE commission is what carried it over the generalization bar.

### 2.5 Item 6 → **Pattern P8 — State-object degeneracy** (PATTERN, not a number)

Submitted as a discipline candidate; ratified as a **named Pattern**. This is not a downgrade — it is
this document's own taxonomy applied correctly: *"Patterns are not prescriptions — each pattern entry
cross-references the discipline or R-prescription that provides the prevention gate."* Item 6 is a
recognition shape, and its prevention gate already exists and already worked: **Discipline #10**
(change one thing, measure one thing), operationalized as the **clean-ablation arm**, is what caught
it. Minting a number for a shape whose gate is already ratified would have added a citation without
adding an enforcement.

The defining property is banked because it is what makes the class invisible: **the counters stay
plausible.** Two of three mechanisms measured NOTHING, one measured EVERYTHING forever, and all three
produced counter values inside ranges a healthy mechanism would also produce. Detection is by **duty
cycle against a clean arm** (95.0 % vs 33.2 %) and by nothing else.

### 2.6 What was NOT ratified

Nothing was deferred or declined in substance. **Six numbers were not minted** (two merged into #63,
one amendment instead of a number, one pattern instead of a number). Recorded here so a future reader
does not read the packet's nine items against four numbers and conclude candidates were dropped.

---

## 3. §C — Melee band pre/post-mitigation units: **PASS-with-carry (INFO)**

**Verified: the code-site half is already discharged**, by the anchor-refit landing itself. The
constants now carry their unit in the name — `REFERENT_MELEE_LO_PRE_MIT` (43.1),
`REFERENT_MELEE_HI_PRE_MIT` (60.8), `REFERENT_MELEE_POST_MIT_BAND` (17.13, 27.90),
`REFERENT_MELEE_POST_MIT_BAND_OWN_CELL` (16.59, 27.07) — at
`spatial_gauntlet/kitcal_g5_scenarios.py:140-149`. A unit suffix is a referent declaration, so this
is now a **Discipline #64** compliance instance and is banked there as such.

**INFO-1 — the packet's stated route is stale.** §C routes the fix *"WITH the melee-graduation work
in stage-2c."* Stage-2c has landed, and **R-WR3-36 detached the `[0.40, 0.60]` band to a future RDR
design lap**. The residual work — charter prose that quotes "melee band 43.1–60.8" adjacent to
post-mitigation A-NOVA-2 / A-WAVE-1 / A-BLIZ-1 pins without the qualifier — is gandalf-seam
documentation and its route target is now **the RDR design-lap charter**, alongside the band and the
default (§4.2 below). `BOSS_DMG_SWEEP = (43.1, 52.0, 60.8)` remains correctly deferred; no unit-mixed
comparison has been executed.

**INFO-2 — packet numbering collision.** §C's item is numbered **8**, which §B already uses for the
discriminator class. Cosmetic; noted so the ledger's item numbers stay resolvable when this packet is
cited later. §C also cites the s2c cell at `spatial_gauntlet/wr3_cell_s2c_2026_07_30.py`; the actual
path is `src/reincarnated/simulation/wr3_cell_s2c_2026_07_30.py` (one directory up).

---

## 4. §E — Dispositions ISSUED

### 4.1 Item 10 — the still-live `getattr` in `wr3_cell_s2c_2026_07_30.py:88`

**gamora's judgement not to edit the banked cell is UPHELD.** Editing a cell that reproduces a banked
artifact is a silent re-base, and the run has correctly treated re-base as requiring a ruling.

**But the disposition the packet framed is aimed at the wrong object.** The three options offered
(annotate the key / version the cell / strike at re-run) all act on the CELL. The durable, quotable,
consumable object is the **ARTIFACT** — and I verified it carries twelve unannotated
`worst_received_event_hp: 0.0` entries across `A_arm_sweep`, `B_leech_scope`, `C_f2_cap`,
`D_icearmor`, and `E_battery_of_record`. Anyone opening that JSON reads a plausible measured zero.
The warning currently lives in three places (MIGRATION §6, the refit cell's `_ReceivedSink`
docstring, gamora's AGENT_STATE) — **none of which is the file the consumer opens.**

**DISPOSITION — three parts, all additive, none a re-base:**

- **(a) ANNOTATE THE ARTIFACT — do this one first, it is the whole risk surface.** Add ONE new
  top-level key to `output/kitcal_g5/wr3_stage2c/wr3_stage2c.json`. Touch **no existing key and no
  existing value** — this is ADDITIVE-AND-REVERSIBLE and therefore within seam-owner authority per
  **Discipline #53**, and it is not a re-base because no measured quantity moves:

  ```json
  "_DEFECT_worst_received_event_hp": "UNMEASURED — NOT a measured zero. Every `worst_received_event_hp: 0.0` in this artifact is a `getattr` default on a field `SpatialFightResult` does not carry (47 fields; none named `worst*` or `*received*`). R-WR3-37(3). DO NOT QUOTE THIS KEY. Gate G-N3\" PASS against it is VOID. Properly measured value: 91.3688 (wr3_anchor_refit, off the hit stream). Report §8's 91.369 came from a different instrument and STANDS."
  ```

  Verified safe: nothing in `src/` or `tests/` digests or schema-validates this file, and the
  before-leg reproduction compares the 17 comparable measurement keys, not a whole-file digest.

- **(b) GENERALIZE THE GUARD, AND DECLARE THE EXEMPTION.** `test_F2`'s AST sweep covers only
  `wr3_cell_refit_2026_07_30`. Promote it to the tree-wide `_door_opening_sites` shape (AST, not
  grep — docstrings quoting the defect must not trip it) and add `wr3_cell_s2c_2026_07_30.py:88` as a
  **NAMED allow-list entry with its reason** ("frozen for artifact fidelity; struck at next re-run
  per Gate-2 2026-07-31"). This is the pattern gamora already used in this landing — *two allow-list
  entries declared in the same landing that creates them*. The exemption becomes **declared rather
  than implicit**, and the class cannot spread silently.

- **(c) STRIKE AT NEXT RE-RUN, not before.** When the s2c cell is next executed for any reason, the
  read is repaired to the `None`-preserving form its own line 93 already uses, and the key is emitted
  as `null`. The re-run regenerates the artifact, so no separate re-base event occurs. If the cell is
  never re-run, (a) and (b) are sufficient and this clause expires harmlessly.

**Rationale:** Discipline #63 clause (a) + Discipline #8 (validation belongs at the boundary the
consumer reads) + Discipline #53 (additive-and-reversible is seam-owner authority) + Pattern P7's
lesson that the warning must live where the reader looks, not where the author knows.

### 4.2 Item 11 — is the `wr3_melee_split_v1` default-False debt TRACKED? **PARTIAL — WARN-1**

I verified tracking, not the deferred ruling (which is correctly the RDR design lap's).

**TRACKED — and better than the packet claims (PASS half).** `boss_rows`' docstring
(`kitcal_g5_scenarios.py:579-587`) states the debt at the producing site AND enumerates the affected
consumers by name — *"WR1 battery-2, the WR1 probes, WR2 cell BAT, the kitcal-G5 harness defaults and
the nine clean-ablation cells all call this function with banked figures taken on the 100 %-cold
row"* — and closes with *"A ruling is owed on promoting it (note §10.1)."* That is exactly where a
WR1/WR2/G-5 consumer meets it: the function they call. Math note §10 item 1 carries it as the first
held ruling. `test_F3` pins the default False at both signatures so it cannot drift silently.

**NOT TRACKED (WARN half).** Two gaps, both at surfaces a consumer reads *without* reading the code:

1. **`MIGRATION.md` — the ADR-004 cross-seam surface — does not carry it.** Its anchor-refit §0 says
   *"Off the flag, NOTHING MOVES — and that is proven, not asserted."* True byte-wise, and correctly
   evidenced. But it reads as an all-clear, and it is the counterweight that is missing: flag-OFF is
   **a known-wrong default deliberately retained, which is a debt, not a resting state**
   (R-WR3-37(4)'s own words). A consumer reading only MIGRATION.md — which is what ADR-004 exists to
   make sufficient — gets the reassurance without the debt.
2. **The banked WR1 / WR2 / G-5 artifacts carry no such note.** Same shape as item 10: the durable
   quotable object is unannotated. Lower priority — those artifacts were correct *as measured*; the
   debt is comparability against the referent, not a defect in the numbers.

**REMEDIATION (WARN, non-blocking, gamora's next seam session):** add one short paragraph to
MIGRATION.md's anchor-refit entry §0, immediately after the "NOTHING MOVES" sentence — naming that
flag-OFF is a known-wrong default retained for comparability, the **~2× the referent's post-mitigation
melee** magnitude, and the pointer to the deferred re-base ruling (RDR design-lap charter; math note
§10.1). One edit, no re-base, no measurement consequence. Discipline #64 + ADR-004 + Principle 3.

**Why WARN and not BLOCK:** the debt is named in four places (docstring, math note §10.1, AGENT_STATE,
R-WR3-37(4) in the ledger), and the ruling it awaits is correctly deferred to a chartered lap rather
than dropped. This is a placement gap, not an untracked debt.

### 4.3 Item 12 — conduct corollary: **RATIFIED as Discipline #19 amendment §19.2**

*"A commission is discharged by its verdict, not by its instrumentation."*

**Ratified in substance; NOT minted as a new number.** Discipline #19 already states this rule from
the orchestrator's end — practical rule 1: a long-running process *"does NOT depend on any agent
session continuing"*; rule 2: *"cross-session continuity is file-based, not agent-based."* A
session-scoped "watcher" is precisely the dependency rule 1 forbids. The gap #19 has is that it
addresses only the ORCHESTRATOR (*don't spawn an agent to wait*) and never the COMMISSIONED AGENT
(*don't return while your decisive measurement is in flight*). That is one rule with two ends, and a
second number would let a compliant reading of one miss the other. **§58-DECLINED precedent applies.**

§19.2 states the two — and only two — acceptable discharge shapes: **block on the measurement**, or
**explicit hand-off (detached process + PID + completion sentinel at a named path)**. The founding
incident supplies both arms of the comparison in one landing: the first agent left a dead log with no
process behind it (sweep died with its agent; relaunched **from zero**); the second left detached
process + PID 49004 + `EXIT=` sentinel, which let the conductor hold the watch and independently
reproduce the name-diff. The difference between those two returns is the entire content of the
amendment.

**Secondary lesson banked with it:** the dead log's *"froze at ~55 %"* was **block-buffered stdout,
not a hang** — the relaunched run sat at the identical 55 % at 100 % CPU for minutes before flushing.
Percentage-of-progress off a block-buffered redirect is not a liveness signal; liveness is the process
table, completion is the sentinel. This is worth more than the corollary itself, because it would
otherwise have entered the record as *"55 % is a suspicious site."*

---

## 5. Independent verification performed (Discipline #11)

Reported state was not accepted as file state. Executed this session:

| Check | Result |
|---|---|
| `pytest tests/test_wr3_anchor_refit.py tests/test_wr3_stage2c.py -q` | **64 passed in 0.21s** (33 + 31; the 31 reconciles the sweep's `+31`) |
| `_band` absence on the refit cell | CONFIRMED — no helper, `"IN BAND"` absent from source, `test_F1` pins it |
| `worst_received_event_hp` on `SpatialFightResult` | CONFIRMED ABSENT (`test_F2` asserts it by `dataclasses.fields`) |
| Banked s2c artifact poisoned keys | **12 instances**, all `0.0`, all unannotated in-file |
| `getattr` at `wr3_cell_s2c_2026_07_30.py:88` | CONFIRMED LIVE (double hazard: `getattr(..., 0.0)` **and** `or 0.0`) |
| Refit cell line 74 `getattr` | **NOT a violation** — inside the `_ReceivedSink` docstring quoting the defect to explain it; `test_F2` uses AST for exactly this reason |
| `wr3_melee_split_v1` default at both signatures | CONFIRMED `False`; `test_F3` pins both |
| MIGRATION.md anchor-refit entry §§0–6 | READ IN FULL — §6 carries the getattr defect; **no debt paragraph** (WARN-1) |
| §A correction 1 vs legolas §6.2 | VERIFIED verbatim, including the scoping that keeps the swap hypothesis dead |
| §A correction 3 vs charter | VERIFIED at charter 902–904 (STRUCK, not annotated) |
| Pre/post-mit constants in `kitcal_g5_scenarios.py` | VERIFIED at 140–149 — units carried in the names |
| Allow-list enforcement mechanism | VERIFIED EXISTS — `_door_opening_sites` + `_DOOR_ALLOW_LIST` |
| Artifact digest/schema consumers | VERIFIED NONE — annotation in 4.1(a) is safe |

**NOT independently re-verified — conductor-attested, and stated as such:** the full-regression sweep
(`60F / 9927P / 21E`, 81 names, NAME-DIFF 0/0 vs `c3887bd3`, 20:35 runtime). Re-running it exceeds
this review's budget. It is accepted on **corroborated** provenance — two parties (completion gamora
and the conductor) independently diffed the same artifact and reached identical results, with the
baseline artifact path recorded. Under **Discipline #65** that is the compliant shape, and
corroboration by two independent readers is stronger than a single re-run by me. Recorded as attested,
not re-verified, so a later reader knows which it is.

---

## 6. Action

- [x] **jack-ryan:** ratify #63 / #64 / #65 / #66 into `engineering-disciplines.md` — **DONE**
- [x] **jack-ryan:** ratify §19.2 amendment + Pattern P8 + #19.1 table row — **DONE**
- [x] **jack-ryan:** update the document-anatomy record with the six not-minted numbers — **DONE**
- [x] **jack-ryan:** decisions-log entry — **DONE**
- [ ] **gamora (WARN-1, next seam session):** MIGRATION.md anchor-refit §0 — one paragraph naming
      flag-OFF as a known-wrong default retained for comparability (~2× referent post-mit) + pointer
      to the deferred RDR re-base ruling
- [ ] **gamora (item 10a, next seam session):** add `_DEFECT_worst_received_event_hp` top-level key to
      the banked stage-2c artifact — additive only, no existing key or value touched
- [ ] **gamora (item 10b, next seam session):** promote `test_F2`'s AST sweep tree-wide with a NAMED
      allow-list entry for `wr3_cell_s2c_2026_07_30.py:88`
- [ ] **gamora (item 10c, conditional):** strike the key at the s2c cell's next re-run, if it re-runs
- [ ] **gandalf (INFO-1, RDR design-lap charter):** carry the pre/post-mitigation unit qualifier into
      the band + default package; the §C route target has moved off stage-2c
- [ ] **drax:** owner-eye render — **UNBLOCKED, may proceed**
- **Matt:** no decision required by this verdict. The two deferred rulings (split-as-default
  promotion; the `[0.40, 0.60]` band) are already chartered to the RDR design lap per R-WR3-36 /
  R-WR3-37(4) and are not re-opened here.

---

## 7. References

**Reviewed:**
- `agentic_orchestration/qa/pending/2026-07-30-gandalf-wr3-gate2-consolidated.md`
- `agentic_orchestration/gandalf/notes/2026-07-30-wr3-kite-commit-run-charter.md` (R-WR3-37, 1183–1231; corrections at 902–904)
- `agentic_orchestration/gamora/notes/2026-07-30-wr3-anchor-refit-report.md` (§4.3, §6.1–6.5)
- `agentic_orchestration/gamora/notes/2026-07-30-wr3-stage2c-report.md` (provenance header, §0–§1)
- `agentic_orchestration/legolas/research/2026-07-30-wr3-veteran-characterization.md` (§6.1, §6.2)

**Engine code inspected (`dbb2d6a9`):**
- `src/reincarnated/simulation/wr3_cell_s2c_2026_07_30.py` (88, 93, 113)
- `src/reincarnated/simulation/wr3_cell_refit_2026_07_30.py` (`_ReceivedSink`, 60–95)
- `src/reincarnated/simulation/spatial_gauntlet/kitcal_g5_scenarios.py` (120, 140–149, 578–645)
- `src/reincarnated/simulation/spatial_gauntlet/kitcal_g5_harness.py` (1008–1009, 2028–2033)
- `src/reincarnated/simulation/MIGRATION.md` (anchor-refit entry, 11–101)
- `src/reincarnated/simulation/math/wr3-anchor-refit-2026-07-30.md` (§10)
- `src/reincarnated/simulation/output/kitcal_g5/wr3_stage2c/wr3_stage2c.json`
- `tests/test_wr3_anchor_refit.py` (F1/F2/F3, 240–289) · `tests/test_bq3_calibration_override_door.py` (652–681)

**Written this session:**
- `~/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md` — #63, #64, #65, #66, §19.2, Pattern P8, #19.1 table row, anatomy record
- `~/Games/reincarnated-engine/design/decisions/decisions-log.md` — ratification entry
