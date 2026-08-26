# Finding — 2026-08-26 — KC2 LIFT RUN · baton-v3.1 re-cut (Gate-2 DELTA re-review)

**Reviewer:** jack-ryan
**Severity:** **PASS-with-WARN** — 0 BLOCK · 3 WARN · 4 INFO
**Target:** `4aac2d0c` + `47523a03` (gamora REMED-①) · `f0b163cf` + `9fd60cee` (star-lord REMED-②) — engine, pushed
**Developer:** gamora (crit-row correction + re-seal) · star-lord (v3.1 re-cut)
**Conductor:** gandalf (RUN-CONDUCTOR), autonomous per charter L-16
**Principles applied:** REVIEW_PROCESS #1 (math-before-code), #2 (smoke-gate), #4 (ledger as truth), #5 (severity matters) · Disciplines #1, #9, #10, #12 · ADR-002
**Scope:** DELTA ONLY per the brief. v3.0's accepted surface is not re-litigated.

---

## 0 · What I re-derived myself

Every claim graded below was produced by an instrument I wrote in this session, or by hand-hashing.
The conductor's greens are recorded; none of them is an input to a verdict here.

| check | my instrument | my result |
|---|---|---|
| all six pack digests, re-walked from member bytes | standalone `sha256` + newline-join, not their `pack_digest()` | v3.1 `2c7fc61f…f4a7` / `f50e5e25…4ed6` · v3.0 `17aabafd…` / `79599c5a…` · v2 `302620c7…` / `b1034c77…` — **6/6 MATCH, 0 member mismatches** |
| K-7 seals | hand `shasum -a 256`, no sim run | `ad61ad2a…dc5c` · `20b05cb4…5f4b` **exact** |
| w1walls predecessor | hand `shasum` | `7a992c81…7881b` **exact — untouched** |
| gamora successor seal | hand `shasum` | `29cc2e95…0154` **exact** |
| substrate pin `pm4o_oa_da.csv` | hand `shasum` | `5c55998d…c564` **exact** |
| `player_offense.py` (newly pinned) | hand `shasum` | `5be276e7…c010` — matches the pin the pack publishes |
| **F-B1r-1, re-derived from the CSV** | my own `csv` reader | **95 monster rows · `p2m_pth_effective` [103.5368, 124.8879] · OA uniformly 3259.0 · DA [2011.527, 2770.0885] · waves 151–160 · expected mult [1.013537, 1.059664] · 0 of 95 clear 135.0 · 0 of 95 carry tier-5 or tier-6 mass** |
| the `DA ≈ 1168` back-solve | fitted PTH(DA) from 63 distinct pairs (max resid **0.00058**), then inverted at PTH=149.2 | **DA = 1166.92** — the refuted figure does belong to a board ~2× weaker |
| V-23 run by me on both packs | imported the gate, loaded packs off disk myself | v3.0 → **6 in scope / 6 violations** · v3.1 → **6 in scope / 0 violations** |
| V-24 / V-25 / V-26 | my own registry census, my own `ABS-` walk, my own predicate | **0 / 0 / 0**; predicate returns the same 8 ids the view publishes |
| V-21 | 14 rowsets / 332 rows off the successor seal; every `math_rules` rowset hashed against the seal | **byte-equal on all six rowsets that live there, incl. `crit_model`** |
| pytest, my invocation | `test_kc2_baton_v3_1_recut.py` + `test_kc2_baton_v3_cut.py` | **59 passed** |
| broader kc2/export selection | `pytest -k "kc2 or baton or export"` | **1204 passed, 1 failed** — the pre-existing AC-10.10 item only |

**Prereg-before-code verified against git, not against the seat's word.** `f0b163cf` is one file, 407
insertions, zero `.py` (D4 held); `4aac2d0c` is one file, 200 insertions, zero `.py`. The v3.1 prereg
DELTA § 2.3 pins `n_in_scope = 6, n_violations = 6` on v3.0 and `0` on v3.1 **and enumerates all six
row ids**, at a commit that predates the gate's existence. All five deviations are declared in that
same pre-code commit. This is a falsifiable pre-registration, not a description of output.

**AC-10.10 confirmed genuinely pre-existing by my own blame:** `secondary_streams.py:136` last touched
at `583ebdae` (2026-08-14), and no remediation commit touches that file or its test. R-L18-7 is
accurate; held-not-silently-fixed is the correct posture per R-L7-4.

---

## (a) BLOCK-1 discharge — **PASS**

**Discharged in full, on every one of the three counts I raised.**

1. **The corrected value GOVERNS the machine-read field.** `CM-BOARD-PTH.value.pth_pct_range` is
   `[103.5368, 124.8879]`; `expected_crit_multiplier_range` is `[1.013537, 1.059664]`; the refuted
   pair survives adjacent under `⚑ REFUTED_CRIT_BASIS_pth_pct_range` with an explicit
   `⚑ governing_reading` clause. Every figure re-derives from the pinned CSV by my own reader.
   R-L17-1's sharpening of the brief — *a note cannot be the governing reading of a machine-read
   field* — is the right call and I ratify it.
2. **`ABS-CRIT-ROLL-RULE` is minted** with `blocks_playability: true` and
   `runtime_choice_required: true`, source-pinned to `player_offense.py`, carrying the D-L5 gap, the
   absent limb of record, and an explicit **DO NOT BUILD A FLAT ×1.5**. The parent lowers on a reason
   that names all three of my counts by name. This is the `ABS-DEVOTION-PROC-ICD` shape applied a
   second time and it is the better shape.
3. **The blocker view is 8 rows / 5 holes and v3.0's "five holes closed" is WITHDRAWN in the pack.**
   My independent predicate over the registry returns exactly the same eight ids. The count going
   **up** at a re-cut whose whole subject was a blocker-lowering is what an honest correction looks
   like, and the pack says so in those words.

**The refutation now travels where I measured it at zero.** My escaped-regex counts: `F-B1r-1` — model
pack **23**, receipt **19**, export MIGRATION **2** (all were 0). Every one of the five surviving
`149.2` sites lives in `math_rules.json` and is refutation-adjacent within ±700 chars by my own
adjacency check; none escaped into `waves.json` or the reference pack. The bonus find is real too:
`HIT_BASIS`'s *"waves 151-180"* is refuted by the same substrate (it stops at 160) and ships labelled.

**gamora's falsifier is the part I want on the record.** `_crit_correction()` raises if any body ever
clears `pthThreshold6`. **This correction cannot outlive its own predicate the way the claim it
replaced did.** That is a strictly stronger artifact than the one I asked for.

---

## (b) V-23 implementation — **PASS-with-WARN**

**The red proof is sound and I reproduced it.** I loaded v3.0 off disk myself, re-derived its digest
first, ran the gate: **6 in scope, 6 violations, exactly the six pinned row ids.** On v3.1: **the same
6 in scope, 0 violations.** Green by correction, not by shrunken scope — and both numbers are asserted
in the tests rather than one. `test_V23_would_have_caught_the_v3_0_crit_rows` calls the red proof
**live** rather than reading it off the receipt, which is the right call for the one test that matters.

**The carrier clause is sound and I ratify deviation 3 (see (d)).** `_carrier_carries` requires a
structured three-way match — `finding_id` equal, `const` present in `governs`, `row_id` present in
`rows_in_scope` — so a stray prose mention cannot satisfy it, and the tests assert the negative case.
The carrier block itself pins `player_offense.py` at `5be276e7…`, which I hand-derived.

### WARN-1 — the gate indexes ONE of the two constants its own banner declares false

The banner's headline reads **"THE TWO STRINGS BELOW ARE FALSE"**. `banner_index()` returns, for
`player_offense.py`, exactly `{"CRIT_BASIS": ["F-B1r-1"]}`. **`HIT_BASIS` is not in it.** I proved the
mechanism by running `correction_banners()` directly:

- the banner names `CRIT_BASIS` in backticks; it never names `HIT_BASIS` in backticks;
- `BANNER_LOOKAHEAD_LINES = 8` covers lines 219–226; `HIT_BASIS` is assigned at **line 230**.

So a row sourced from `HIT_BASIS` with `player_offense.py` provenance is **not in V-23's scope at all**,
and the gate returns green without having asked. **No live consequence at this cut** — I swept both
packs and the only row referencing `HIT_BASIS` is `CM-BOARD-PTH`, which carries `F-B1r-1` on the row.

**Why this is a WARN and not an INFO.** This is the gate my own BLOCK minted, and its first
implementation exhibits a milder form of the family it exists to catch: **an instrument returning
cleanly over a domain narrower than the question it was asked.** The banner declares two constants
false and the index carries one. `#75` cl. 6 territory — the remedy did not inherit the full scope of
the thing it remedies. Recorded now, cheaply, rather than as a face-eight later.

**Cite:** REVIEW_PROCESS #2 · Discipline #10 · the L-14 harvest (a) discipline candidate, which this
finding sharpens rather than retracts.

**Fix, one line, seam's choice:** either name `` `HIT_BASIS` `` in the banner prose (a comment edit —
it does not touch the constants and so does not engage D-B1r-3), or index the banner's plain-text
UPPER_SNAKE mentions in addition to backticked ones. Do **not** simply raise the lookahead: that
answers this instance and not the question.

---

## (c) WARN-1..4 and INFO-1..6 as shipped

| my v3.0 item | disposition | verdict |
|---|---|---|
| **WARN-1** 47.6 % quoted as measured | ships as `[13.7 %, 47.6 %]` with `floor_basis` 64/466, `ceiling_basis` 222/466, **both unpinned bridges named with `pinned: false`**, and `what_would_settle_it`. `ABS-B2-CONTROLLER-FIELD-COVERAGE` no longer says "both measured". Arithmetic re-checked: 64/466 = 13.73 %, 222/466 = 47.64 %. | **PASS** — and the reasoning for preferring a range over an `instrument-uncorroborated` stamp is better than my suggestion: the floor depends on no bridge, so a stamp would discard a number that is not in doubt. |
| **WARN-2** `class` / `why` say two things | `LIFTED` added to a closed enum, **V-24 gates it** (nothing did — V-7 gates `grade`), `playability_statement` spells out class semantics, `⚑ v3_lift_status` added to all eight rows. | **PASS-with-WARN** — see WARN-2 below. |
| **WARN-3** seven stray `ABS-*` ids | all seven mirrored into the registry with `also_at` + `mirror: true`; `registry_law` amended to *the registry is the INDEX; block-local absences mirror, they do not move*; V-10 paired rows unmoved byte-for-byte; **V-25 enforces it**. My own independent `ABS-`-id walk over both packs: **39 distinct ids, 39 in registry, zero stray.** | **PASS** |
| **WARN-4** v2 prose in a v3 `meta.json` | `emitted_by` names this run and this remediation; `headline` describes v3.1; `lap_manifest` carries **8 laps, every one from this run**, each with its ledger row. | **PASS** |
| **INFO-1** 32-hex prefix labelled `sha256` | disclosed at `⚑ truncated_digest_disclosure_INFO_1` with the full `2fd5a347…ce0b3` (which I hand-derived — it matches) and an explicit `startswith`-not-equality instruction. | **PASS** — see (d) deviation 5. |
| **INFO-2** `pm4g_played_kit.csv` unpinned | promoted to a first-class `source_pins` entry. | **PASS** |
| **INFO-3** `player_offense.py` unpinned | pinned; and the substantive fix is that **V-23 now reads the file's content**, which is strictly stronger than a digest. | **PASS** — see INFO-1 below on the word "ENFORCED". |
| **INFO-4** DR-1 exemption invisible inside the pack | `⚑ dr1_provenance_dialect_exemption` now lives in `provenance.json` with the 332-row count and the two-dialect explanation. | **PASS** |
| **INFO-5** dead predicate at `:233` | removed; the story kept in-comment. | **PASS** |
| **INFO-6** `FIND-B2-B3-WORLD-DISAGREEMENT` absent from MIGRATION § 5 | now item 3 on the list, flagged as *"this belonged on the list at v3.0"*. | **PASS** |

### WARN-2 — eight rows still say two things; the contradiction moved from `class` to `why`

All eight `class: LIFTED` rows carry a `why` that reads **"NOT YET LIFTED"** — `ABS-CRIT-MODEL`:
*"NOT YET LIFTED into Layer 1."* · `ABS-DOT-STACKING`: *"DECODED, NOT YET LIFTED (the D-4 target)."*
· and six more. I searched `provenance.json` for any statement that `why` is preserved v2-era text:
**zero hits** for `historical`, `v2-era`, `the why field`, or any equivalent.

**What is genuinely fixed:** the *operational* half. `playability_statement` keys its fetch-instruction
on `class`, `class` is now correct on all eight, and V-24 gates it. A consumer following the pack's
stated instruction no longer goes hunting for blocks that are three keys away. My WARN-2 offered the
class-enum fix **or** the `why`-fold as sufficient and the seat took the first — **so the letter of my
WARN is discharged and I am not re-issuing it.**

**What remains:** a human-readable field, on the eight largest and most load-bearing absence rows,
that states the opposite of the row's own class, with nothing telling a reader which governs. The
correct reading is present and ⚑-flagged (`⚑ v3_lift_status`, `⚑ v3_1_reclassification_reason`); the
stale reading is not flagged at all. In a pack whose declared audience is a Godot implementer reading
prose, that ordering is backwards.

**Not blocking:** no machine-read field is wrong, no consumer instruction points at `why`, and the
correct statement is on every affected row.

**Cite:** REVIEW_PROCESS #5 · Discipline #9. **Fix:** one line — either fold the current status into
`why`, or add a single registry-level note that `why` is the absence's original v2 statement and
`⚑ v3_lift_status` governs. Either takes a sentence.

---

## (d) The five declared deviations — **NO VETO EXERCISED ON ANY**

My veto was open on each. I decline to exercise it on all five, and I ratify the conductor's
R-L18-1..5 adjudications. Where I add something, it is below.

**1 · Eight rows take `class: LIFTED`, not six — APPROVED.** The seat read the WARN's intent past its
letter and was right to. My count of six was a count of rows *lowered*; the contradiction I described
is a property of `class`, and `ABS-AI-STATE-MACHINE` (8162 rows) and `ABS-MONSTER-STAT-BLOCKS` (31601
rows) carried it while never having been lowered. **Fixing six of eight would have half-remediated my
own WARN at precisely the two largest rowsets in the pack.** Correct call; I would have flagged the
six-row version at the next gate.

**2 · Four new gates, not one — APPROVED.** V-24 (class enum), V-25 (no stray `ABS-` id), V-26
(view vs. predicate), V-27 (predecessors verify at POST). Each pins a defect **this wave actually
exhibited**, which is the right test for an additive gate. I ran all four independently and got 0/0/0
and byte-stable predecessors. V-27 in particular is real enforcement, not a report line — it flips
`BLOCKS` and honest-fails the emit; I read the code path.

**3 · V-23 admits carrier-block satisfaction — APPROVED, and I want the reasoning on the record as
mine too.** The four unamended rows (`CM-THRESHOLD-TABLE`, `CM-ROLL-RULE`, `CM-LIMB-LO`,
`CM-LIMB-OF-RECORD`) are sealed bytes carried byte-equal, and **their content is not wrong** — the
refuted claim lives in the two rows gamora amended. Failing them offered only *rewrite sealed bytes to
green a gate* or *allow-list them*, and **both are the failure class the gate exists to catch.** K-7
outranks gate aesthetics. The clause is narrow by construction and the tests assert the negative case.

**4 · Mirrors excluded from counting — mechanism APPROVED; see WARN-3, the justification is not.**

**5 · INFO-1 discharged by disclosure, not correction — APPROVED.** Extending the 32-hex prefix means
editing a sealed row. That is the same move BLOCK-1's remediation refused to make, and refusing it
twice in one cut is consistency, not evasion. The full digest is published beside the row and I
hand-derived it: it matches.

### WARN-3 — the mirror-exclusion rationale is a counterfactual that was stated, not run

The mechanism is right and defensive and I approve it. **The justification recorded for it is false
against the shipped bytes**, in three places:

- pack, `⚑ mirror_rows_excluded_from_count.why`: *"counting the mirror too would report one hole twice"*
- pack, `⚑ counted_on`: *"Counting this mirror as well would report five holes where there are four plus crit"*
- ledger R-L18-4: *"without it the pack ships a predicate returning 9 beside a view saying 8"*

I ran it both ways over the shipped registry:

```
predicate WITH mirrors counted : 8
predicate WITHOUT mirrors      : 8
difference: set()
```

`ABS-TARGET-SELECTION-POLICY` ships `blocks_playability: false` (its home row in
`target_selection.json` has no `blocks_playability` key at all, so the mirror builder's
`src.get("blocks_playability", False)` defaults it), and the predicate is an **AND**. **The count is
eight either way.** No version of this pack ever returns 9.

**The mechanism still earns its place** — precisely because the home row's `blocks_playability` is
*absent* rather than *false*. Anyone who later gives that row the value its own hole warrants makes
the exclusion load-bearing overnight. Keep the code; correct the sentence.

**Cite:** REVIEW_PROCESS #1 · Discipline #10. This is the run's signature family one more time — **a
claim about what an instrument would do, asserted rather than executed** — and it appears inside the
remediation whose entire subject was that family. Cheap to fix, and worth fixing precisely because
this cut's credibility rests on its numbers having been run.

**Fix:** restate as forward-looking (*"a mirror that inherits a blocking home row would double-count;
at this cut none does, and the predicate returns 8 with or without the exclusion"*), and append a
corrigendum line to R-L18-4. Do not change the code.

---

## (e) Untouchables — **PASS.** Verified by hashing, not trusted.

| artifact | pinned | my hand-derived | |
|---|---|---|---|
| K-7 `mpol2` checkpoint | `ad61ad2a…dc5c` | `ad61ad2a…dc5c` | ✅ |
| K-7 `mech` checkpoint | `20b05cb4…5f4b` | `20b05cb4…5f4b` | ✅ |
| w1walls predecessor seal | `7a992c81…7881b` | `7a992c81…7881b` | ✅ |
| baton-v2 model / reference | `302620c7…` / `b1034c77…` | both re-walked from members | ✅ |
| baton-v3.0 model / reference | `17aabafd…` / `79599c5a…` | both re-walked from members | ✅ |

Zero member-digest mismatches across all six packs. **The supersession is correctly SCOPED**: the
successor seal owns the 332 rows and nothing else; the predecessor remains seal-of-record for the SIM
and did not move a byte. The `W1_SEAL_REL` re-point is a path change, not a parser change — V-21 asks
the identical question of the new bytes and I re-derived the same 14 rowsets / 332 rows.

---

## (f) Layer law — **PASS. Zero.**

My own regex sweep over both v3.1 packs (21.9 MB model, 2.0 MB reference) and the receipt:
`D-LIFT-1`, `D-LIFT-2`, `MATT-RULED`, defense-bypass and max-health phrasings, ground-degen,
uncampable, crossable — **zero occurrences in either pack and in the receipt.**

Two hits examined and cleared:
- `0.166667` ×12 in `waves.json` — `slot_weight_share` on six-slot pool families (normal + champion),
  a derived weight share, correctly labelled. Twelve rather than v3.0's six because two families ship.
- `Matt-ruled` ×1 in `reference/acceptance.json` — the 2026-08-24 ruling that **wave-160 is a graded
  row, never a gate**. That is a *harness-grading* ruling, not a design value, and it is exactly the
  kind of ruling that should survive in the artifact so a future session cannot forget it. Not a leak.

**D-LIFT-2 (Q67, ruled at L-16 mid-remediation) did not leak into the artifact.** A design value ruled
by Matt *during* the wave is the hardest case for this law and it held.

---

## (g) KC2-MC F-2 — **DISCHARGE ACCEPTED**

**I accept the discharge, explicitly, per charter L-14's disposition row and L-18's terms.**

The obligation was: *the Wave-4 emitter carries the corrected crit expectation, and the Layer-1
CritLimb row re-grades on the Lap-O basis.* Both are satisfied and I verified both against the
substrate rather than against the claim:

- the corrected expectation **1.0135–1.0597** ships on `CM-BOARD-PTH.value.expected_crit_multiplier_range`
  as a governing machine-read field, and I re-derived `[1.013537, 1.059664]` from `pm4o_oa_da.csv` myself;
- `CM-LIMB-HI` re-grades: the value `1.5` correctly does not move (it is read off `CritLimb.HI`), and
  its **justification** is replaced — *the top tier applies on 0 of 95 resolutions*, which I confirmed
  independently (zero rows carry tier-5 or tier-6 probability mass);
- `KC2-MC F-2` is cited **9 times** in the model pack, on the rows a consumer actually reads.

**One location note, not a finding:** `F-2` occurs **0 times in the v3.1 receipt**. The receipt reaches
the obligation through its `commission` block pointing at my v3.0 finding, so the chain is intact; but
the discharge of a predecessor-run ruling is the kind of thing a future close-out sweep will look for
in the receipt. Worth one line in the run-close packet, not a change to the artifact.

**F-2 IS DISCHARGED as of this acceptance.** The conductor should record it as such — and the
successor-charter carry-table candidate (L-14 harvest (b)) is the thing that prevents the next one,
not this discharge.

---

## INFO

1. **"ENFORCED" overstates the pin's mechanism.** `PLAYER_OFFENSE` is digested from bytes at emit
   time, like every other `source_pins` entry; nothing asserts it against a frozen literal, so a
   future edit to the file yields a *new pin value*, silently, not a failure. The **substantive**
   remediation of my INFO-3 is V-23 reading the file's *content*, which is strictly stronger than any
   digest equality would be — so the fix is real and the word is what is loose. Prefer *"pinned and
   scanned"*.
2. **Several v3.1 tests assert receipt values rather than re-deriving.**
   `test_V23_is_green_on_v3_1_and_the_scope_did_not_shrink` reads `receipt["validation"]`; so do the
   V-24/V-25/V-27 and census tests. The red-proof test and the pack-content tests do load from disk,
   which is the right split — but a test that reads the emitter's own report is asserting what the
   emitter said about itself. I re-ran every one of those numbers live and they hold; noting the shape
   because it is the "conductor's greens are not your greens" rule one level down, inside the suite.
3. **The `_all_rows_with_carrier` walker has a dead branch** — `kc2_baton_v3_schema.py:140-145`, both
   arms of the `if/else` set `nxt = n`. Harmless and the behaviour is correct (carrier = nearest
   enclosing dict), but it reads as though row-dicts and non-row-dicts are treated differently and
   they are not. Kin to the INFO-5 dead predicate that this same cut removed.
4. **The `⚑ counted_on` sentence is internally muddled independently of WARN-3** — *"would report five
   holes where there are four plus crit"* — the view's own count of distinct holes **is** five ("four
   plus crit" = five). Fold this into the WARN-3 rewrite rather than treating it separately.

---

## Discipline candidate — sharpened, not retracted

My v3.0 review minted: *a lifted constant inherits its source's corrections, and nothing checks that
it did.* V-23 makes it executable and the red proof makes it credible. **WARN-1 above is its first
refinement, and the refinement is the interesting part:**

> A gate built to ask *"does the source still stand behind this value?"* must be able to name **every**
> constant the source's correction governs. V-23's index carries `CRIT_BASIS` and not `HIT_BASIS`
> because the banner backticked one and assigned the other eleven lines down — so the gate is green
> over a domain narrower than the banner's own headline (*"THE TWO STRINGS BELOW"*).

This is the **ninth face** the run has produced of *an instrument returning cleanly after it stopped
answering the question* — and the first one to appear **inside the remedy built for the eighth**.
R-L18-6 already made that argument from the seat's two self-caught test defects; this is the same
argument from the gate itself, and it is a stronger instance because the gate shipped green.

**The generalisation worth carrying forward:** *a gate's SCOPE is a claim, and a claim requires a
falsifier.* V-23 has a superb falsifier for its **verdict** (the v3.0 red proof) and none for its
**scope** — nothing asks whether the six rows it found are the six rows it should have found. The next
form of this discipline is a scope-falsifier: assert the in-scope set against an independently
enumerated expectation, not only the violation count against a pinned number.

---

## Release scoping

- **drax / the Godot team — UNBLOCKED, including the crit rows.** The v3.0 crit block is lifted. Build
  `CM-BOARD-PTH` from `value`, never from `⚑ REFUTED_*`, and read `ABS-CRIT-ROLL-RULE` before
  implementing any crit behaviour: **the roll rule is a declared gap and there is no limb of record.**
  Do not build a flat ×1.5 — expected multiplier is 1.0135–1.0597 and the HI limb is reached on 0 of
  95 rows.
- **gamora (pool-DoT follow-on) — not blocked, unchanged.** D-LIFT-1 + D-LIFT-2 give it a complete
  spec kernel and neither leaked into the artifact.
- **The three WARNs are prose-and-scope items.** None blocks release; all three are cheap and all
  three are the kind of thing that becomes expensive only by being deferred twice.

---

## Verdicts

| item | verdict |
|---|---|
| (a) BLOCK-1 discharge | **PASS** |
| (b) V-23 implementation | **PASS-with-WARN** (WARN-1 — `HIT_BASIS` outside the index) |
| (c) WARN-1..4 / INFO-1..6 dispositions | **PASS** (WARN-2 — `why` staleness on the eight LIFTED rows) |
| (d) five declared deviations | **PASS on all five, no veto exercised** (WARN-3 — deviation 4's rationale) |
| (e) untouchables byte-stable | **PASS** — all hand-hashed |
| (f) layer law | **PASS** — zero |
| (g) KC2-MC F-2 | **DISCHARGE ACCEPTED** |

**OVERALL: PASS-with-WARN. No BLOCK. The run does NOT park for Matt** — every finding here is inside
L-15's ruled scope and none requires new design law, so all three WARNs resolve under the conductor's
L-16(ii) delegation, at seam discretion, or ride the harvest packet.

**What I want said plainly, because the record should carry it:** I issued a BLOCK on the largest
single-number error the pack could hold, and the remediation came back having **raised its own blocker
count**, carried the correction into the field a machine reads, built the gate that would have caught
it, **run that gate red against the defective bytes with the expectation pinned before the code
existed**, and declared five divergences from my brief in a pre-code commit rather than discovering
them afterwards. On four of the five I would have ruled the same way; on the first — eight rows, not
six — the seat read my WARN's intent past its letter and was right where I was narrow. Neither seat
moved a sealed byte to make anything green, and both had the opportunity.

The three WARNs are the price of that speed and they are small. **This is the strongest remediation
I have graded on this project.**

---

## References

- `/Users/admin/Games/reincarnated-engine/src/reincarnated/output/kc2-model-pack-v3-E-s09-cp150-mech-v3p1-20260826_031143/model/{math_rules,provenance,meta}.json`
- `/Users/admin/Games/reincarnated-engine/src/reincarnated/output/kc2-reference-pack-v3-E-s09-cp150-mech-v3p1-20260826_031143/`
- `/Users/admin/Games/reincarnated-engine/src/reincarnated/output/kc2-baton-v3-cut-receipt-v3p1-20260826_031143.json`
- `/Users/admin/Games/reincarnated-engine/src/reincarnated/export/kc2_baton_v3_schema.py` (V-23 at :163-313 — `correction_banners` :192, `banner_index` :228, `_carrier_carries` :245; V-24..V-26 at :493-541; the dead branch at :140-145)
- `/Users/admin/Games/reincarnated-engine/src/reincarnated/export/kc2_baton_v3_emit.py` (`v23_red_proof` :184, `V23_RED_PROOF_EXPECT` :168, `PY_PIN_KEYS` :152, V-27 at :1475-1490, the carrier block at :897)
- `/Users/admin/Games/reincarnated-engine/src/reincarnated/export/math/2026-08-26-kc2-baton-v3-1-recut-prereg-DELTA.md` (§ 2.3 red-proof expectation; § deviations)
- `/Users/admin/Games/reincarnated-engine/src/reincarnated/simulation/math/kc2-lift-remed1-crit-row-correction-2026-08-26.md`
- `/Users/admin/Games/reincarnated-engine/src/reincarnated/simulation/kc2/player_offense.py` (banner :183-218, `CRIT_BASIS` :220, `HIT_BASIS` :230 — the WARN-1 gap)
- `/Users/admin/Games/reincarnated-engine/src/reincarnated/simulation/output/kc2-lifted-rows-E-s09-cp150-remed1-20260826_024526.json`
- `/Users/admin/Games/reincarnated-engine/data/kc2/pm4o_oa_da.csv` (`5c55998d…c564` — the F-B1r-1 substrate I re-derived from)
- `/Users/admin/Games/reincarnated-engine/tests/test_kc2_baton_v3_1_recut.py` · `tests/test_kc2_baton_v3_cut.py`
- `/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/qa/findings/2026-08-26-kc2-lift-gate2-baton-v3.md` (the v3.0 BLOCK this discharges)
- `/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/gandalf/notes/2026-08-25-kc2-lift-run-charter.md` (L-14..L-18)
