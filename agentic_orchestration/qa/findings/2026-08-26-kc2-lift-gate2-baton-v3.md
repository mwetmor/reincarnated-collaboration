> **CONDUCTOR CAPTURE HEADER (gandalf, RUN-CONDUCTOR, 2026-08-26).** The harness blocks seat-authored findings files; per the md-b4app-2d protocol (5th instance) the jack-ryan Gate-2 seat returned this finding IN FULL and the conductor captured it VERBATIM below — authority is jack-ryan's, the keystrokes are the conductor's. Nothing between the rule below and end-of-file is conductor-authored. Ledger fold: LIFT charter L-14.

---

# Finding — 2026-08-26 — KC2 LIFT RUN Wave-3 · baton-v3 cut (Gate-2, run-final)

**Reviewer:** jack-ryan
**Severity:** **BLOCK** (one finding) · 4 WARN · 6 INFO
**Target:** `893d62e9` (prereg) · `1c60130b` (cut) · `78135961` (AGENT_STATE) — engine, pushed
**Developer:** star-lord (Wave-3 cut) · gamora (Wave-2 `mech_lift` rows, carried)
**Principles applied:** REVIEW_PROCESS #1 (math-before-code), #2 (smoke-gate), #3 (cross-seam impact), #4 (decisions-log/ledger as truth), #5 (severity matters) · Disciplines #1, #8, #9, #10 · ADR-002, ADR-004

---

## 0 · What I re-derived myself (not read off the receipt)

Every load-bearing claim below was produced by my own instrument, written in this session:

| check | my result |
|---|---|
| model pack digest, re-walked from bytes | `17aabafd8c603212…` **MATCH**, 12 members |
| reference pack digest | `79599c5ae2dfc7c4…` **MATCH**, 7 members |
| baton-v2 pair | `302620c76347fae1…` / `b1034c77944dd84d…` **MATCH — untouched** |
| K-7 seals, hand `shasum`, no sim run | `ad61ad2a…dc5c` · `20b05cb4…5f4b` **exact**; W1W2 seal `7a992c81…7881b` exact |
| V-21, 332 rows re-derived through `mech_lift.all_rowsets()` | 14 rowsets / **332 rows, byte-equal to the seal** |
| id census, whole model tree | MS- 31601 · CP- 8162 · PM- 576 · WSC- 312 · WS- 156 · DP- **7** — **0 duplicate ids**, no prefix ambiguity |
| pytest `tests/test_kc2_baton_v3_cut.py` | **26 passed** |

**Eye-order item 1 (SEVEN devotions) — CONFIRMED, no concern.** Seven `DP-` rows, seven distinct `proc_id`s, seven distinct `devotion_skill_record`s; `DPI-`/`DPE-` separate cleanly (the hyphen *is* in the prefix, as the fixed predicate asserts). `FIND-DEVOTION-COUNT-SEVEN-NOT-EIGHT` present with its triple-attestation basis. R-L2-2 discharged.

**Discharge spot-audits, all green by my predicates:** V-10/V-11 paired rows mutual with `instrument-uncorroborated` on the REFUTED row only · V-12 all 4 W2 rows carry rider + `[0.000, 0.385]`, `REF-W2-CAST-MIX` present · V-13 `retargeted` occurs exactly once, inside `prohibitions[0]` · V-14 8 bias rows, all `function_unknown_ref → ABS-SELECTIONBIAS-FUNCTION`, U-1…U-11 present · V-15 `viresmight1` **0**, `viremight1` 6 · V-16 576 rows / 117 distinct pools / 0 empty `member_record`, both DO-NOT rows present · V-22 **66** absent limits, all EXPLICIT `unlimited`, `limit_ruling` citing R-L9-3 verbatim on every row, zero `0`/blank.

**D-LIFT-1 layer-separation (the new check) — CLEAN.** `MATT-RULED`, `D-LIFT-1`, defense-bypass and %-max-health phrasings occur **nowhere** in either pack. The only `0.1666` hits are `slot_weight_share` on six-slot pools (a derived weight share, correctly labelled `⚑ DERIVED here, not a corpus value`). The pool-damage design law did not leak into a measured row.

**Instrument story — the fixes are sound.** V-17 and V-18 both now run structure-adjacent predicates, and both carry the defect narrative in-code (`kc2_baton_v3_schema.py:234-238`, `:260-266`). I ran the `WS-`/`WSC-` claim myself: they separate. The stories are preserved.

**R-L45-1(b) residue — flagged, not fixed, verified.** `AGENT_STATE.md` item ⑨ carries it; `git log` on `export/goldens/devotion_envelope_disclosure.provenance.json` shows last touch at `a53c97fc`, **not** in this cut. No silent regeneration.

---

## BLOCK-1 — The pack ships, as a ⚑-flagged fact, a figure its own pinned source declares FALSE two lines above it — and `ABS-CRIT-MODEL`'s blocker was cleared on that basis

### What I found

`model/math_rules.json · lifted_mechanics.crit_model` ships:

```
"id": "CM-BOARD-PTH",
"value": {"player_oa": 3259, "pth_pct_range": [149.2, 182.2]},
"note": "⚑ THE BOARD CLEARS THE TOP THRESHOLD ON EVERY BODY. The tier ladder is
         therefore SATURATED on this fixture — a fact about the fixture, not about the law.",
"provenance": "... CRIT_BASIS · Lap L check L4-player-cannot-miss-this-board"
```

`src/reincarnated/simulation/kc2/player_offense.py` — the file that supplies that string — carries a 35-line banner ending at line 218, **two lines above `CRIT_BASIS` at line 220**:

```
# ⚑ KC2-MC · B-1r · `F-B1r-1` — THE TWO STRINGS BELOW ARE FALSE IN ONE FIGURE …
#   `p2m_pth_effective` runs 103.5368 – 124.8879 over waves 151-160 …
#   103.54 does NOT clear `pthThreshold6 = 135`, so
#   `CRIT_BASIS`'s "clears the top threshold on every body" is FALSE.
```

The lift (`mech_lift.py:1019`) parses `po.CRIT_BASIS` and promotes the refuted sentence from a *filed-known-false string* into an emphatic model row asserting it as "a fact about the fixture."

**The refutation travels zero times.** Escaped-regex counts across the whole model pack, the receipt, and the MIGRATION v3 section:

| token | occurrences |
|---|---|
| `149\.2` | **1** (this row) |
| `F-B1r-1` · `C-B1r-2` · `D-B1r-3` | **0 · 0 · 0** |
| `103\.5368` · `124\.8879` · `pm4o_oa_da` (as the crit predicate) | **0 · 0 · 0** |

Same at the Wave-2 seal `7a992c81…`: `149.2` ×1, `F-B1r-1` ×0.

**Blast radius.** `CM-LIMB-HI`'s note reads *"the UPPER end — **the top tier applies on every resolution**"* — that sentence is true only under the refuted figure. A Godot implementer reading `CM-BOARD-PTH` + `CM-LIMB-HI` builds a flat ×1.5 player damage multiplier. KC2-MC ruling **F-2** puts the corrected expectation at **1.0135–1.0597**, with ×1.4/×1.5 reachable on **0 of 95 rows**. That is a ~40 % error on *all* player damage — the largest single-number error available in this pack.

**And it lands on the row that was downgraded.** `ABS-CRIT-MODEL` leaves this cut `blocks_playability: false` **and** `runtime_choice_required: false`. The second is falsified by the pack's own adjacent row:

```
"CM-LIMB-OF-RECORD": value null —
"⚑ THERE IS NO LIMB OF RECORD … A consumer that picks one is making a
  decision this sim declined to make."
```

That is the definition of a runtime choice. The `⚑ v3_reclassification_reason` for `ABS-CRIT-MODEL` mentions neither `D-L5`, nor the absent limb-of-record, nor `F-B1r-1`.

**The governing ruling was never carried.** KC2-MC charter, DRIFT-CRITIC **F-2**: *"the licence DIES on the merits … D-L5 superseded by Lap O (pinned since 2026-08-14). Sim INSULATED …; **the baton is NOT** → Wave-4 emitter carries the corrected crit expectation + the Layer-1 CritLimb row re-grades on Lap-O basis."* I searched: **F-2 has no discharge row.** baton-v2 carries no crit rows and keeps `ABS-CRIT-MODEL blocks=true`. The obligation does not appear in the LIFT charter's § 6 standing laws, nor in the L-11 consolidated carried-rows list handed to Wave-3. So the LIFT run lifted crit on the basis F-3 ruled defective (*"Lap L's `defense_of()` omits the level and attribute terms"*, DA 64–1169 vs 2011–2770) and cleared the blocker without the re-grade the prior conductor ordered.

`D-L5` is described on the row as *"ROUTED TO THE CONDUCTOR"* — it appears **0 times** in the LIFT charter ledger, and has no `ABS-` registry row, so `V-3` cannot reach it and `P-1` cannot count it.

### Rationale

- **Review principle #4 (the ledger is truth).** A prior conductor ruling (KC2-MC F-2/F-3) was superseded by silence, not by ruling. This is exactly the family the run itself named twice — **R-L5-3** (a commitment item evaporating inside an "all disposed" clause) and **R-L8-2** (*close-out summaries reconstructed from memory instead of derived from the ledger*). It was named, and then it bit, one run later.
- **R-L10-2 / V-11, generalised.** This run's own law: *"the instrument-uncorroborated stamp travels with the verdict everywhere it is quoted."* Here the source did not merely caveat the figure — it **refuted** it — and nothing travelled.
- **Discipline #9 (attribution clarity) + #10 (empirical inspection over assumption).** `mech_lift` read a constant past the banner that refutes it. `CRIT_BASIS` is *parsed* rather than transcribed — a good discipline that in this case launders a known-false string into a model row with a ⚑ on it.
- **The seat's own consistency standard points the same way.** `ABS-DEVOTION-PROC-ICD` was *kept* blocking with the rationale *"proc RATES will be wrong even though proc LOGIC is right."* Crit is the identical shape at strictly larger magnitude (~×1.4 on all player damage vs proc rates on 7 procs) and was *lowered*. Applied twice, two answers.
- **Prereg § 6.2** ("Not repair upstream findings … carried, not fixed here") was the right posture and star-lord honoured it. Carrying a flagged-false string, however, means carrying the flag with it. The string rode; the flag did not.

### Where responsibility sits (stated, so the fix routes correctly)

The defective row **originates in gamora's Wave-2 `mech_lift` crit rowset** (accepted at R-L7-1), and star-lord carried it **byte-equal**, which is exactly correct under V-21/K-7. **What is star-lord's, and what this gate is scoped to, is the P-3 reclassification** — `blocks_playability` and `runtime_choice_required` on `ABS-CRIT-MODEL` — which is the registry row, is this seat's judgment, and was explicitly submitted for per-row disagreement. **I disagree with that row.** No gate caught it because no gate asks *"is this lifted string one its own source declares false?"* — and that is the discipline candidate this finding mints.

### Action

- [ ] **star-lord:** revert `ABS-CRIT-MODEL.runtime_choice_required` → `true` (falsified by `CM-LIMB-OF-RECORD` in the same pack) and `blocks_playability` → `true`, **or** split the crit residual out the way `ABS-DEVOTION-PROC-ICD` was split from `ABS-DEVOTION-PROCS` — mint `ABS-CRIT-ROLL-RULE` (D-L5) carrying the blocking weight, and let the parent lower honestly. The split precedent is this seat's own and it is the better shape.
- [ ] **gamora:** amend `mech_lift`'s `CM-BOARD-PTH` and `CM-LIMB-HI` to carry `F-B1r-1` — the re-derived range `103.5368–124.8879`, the `pm4o_oa_da.csv` pin, and the explicit statement that the saturation claim is refuted. Do **not** edit `player_offense.py`'s constants: `D-B1r-3` correctly forbids moving a digested surface for a prose reason. The correction belongs on the lifted row, not on the source string.
- [ ] **gandalf (conductor):** give KC2-MC **F-2** a disposition row in the LIFT ledger. *"Discharged at v3.1"* or *"carried forward, named"* both take one line; silence is the defect (charter's own corollary on mooted escalations).
- [ ] **Matt (BLOCK → escalation per ADR-002):** this is cross-seam (gamora row + star-lord registry + drax/Godot consumer) and touches a prior conductor ruling. Your call on whether v3 re-cuts at a new digest or ships with the crit blocker restored and the correction appended.

---

## WARN-1 — The 47.6 % figure is quoted as measured against its own author's explicit instruction not to

`model/provenance.json · ⚑ named_findings[FIND-B2-B3-WORLD-DISAGREEMENT]` states *"158 resolve to no controller at all"* and `consequence: "a runtime that rolls a body from B3 has a 47.6 % chance of finding no AI parameters for it."` `ABS-B2-CONTROLLER-FIELD-COVERAGE.why` introduces both holes as *"Two holes, **both measured**."*

elrond's curation § 11, the pinned source: *"If either bridge is roster-scoped in a way I did not detect, the '158 records with no controller' figure is an artefact of **my instrument**, not of the substrate. The direction of the finding is robust; **the exact number is not, and should not be quoted as measured without re-derivation.**"* Ledger L-2 recorded the self-flag. It did not travel to the row.

The robust floor is **64/466 = 13.7 %** (inside B2's own key space); 47.6 % is the ceiling and is the only number shipped. Same law as R-L10-2/V-11, different row. **Fix:** state it as `[13.7 %, 47.6 %]` with the two bridges named unpinned, or stamp the row `instrument-uncorroborated` the way `FIND-BOARD-BLINDNESS-REFUTED` is stamped.

## WARN-2 — The reclassification moved `blocks_playability` and left `class` and `why` at their v2 values, so six rows now say two things

All six lowered rows still carry `class: "DECODED-NOT-YET-LIFTED"` and their verbatim v2 `why` text (`ABS-CRIT-MODEL`: *"NOT YET LIFTED into Layer 1"*; `ABS-DOT-STACKING`: *"DECODED, NOT YET LIFTED (the D-4 target)"*) while the pack ships their rows. Only `⚑ v3_reclassification_reason` is current.

This is load-bearing, not cosmetic, because `meta.json · playability_statement` gives `class` an operational meaning: *"Rows of class DECODED-NOT-YET-LIFTED name the file and digest where the data already lives."* A consumer following that instruction goes to fetch six blocks that are already in the pack. `class` is not in any closed enum and no validator gates it (V-7 gates `grade`, a different field). **Fix:** add a `LIFTED` class member and gate it, or fold the v3 reason into `why`.

## WARN-3 — Seven `ABS-*` ids live outside the absence registry, which is the exact split `registry_law` says v3 abolished

`registry_law`: *"ONE absence registry. v1 split absences across out_of_model / declarations / informative_rows … **A consumer should never need a footnote to find an absence.**"*

Outside `absence_registry`, carrying `id` keys: six `ABS-SUMMON-*` rows at `summons.json/declared_absences[0..5]`, and **`ABS-TARGET-SELECTION-POLICY`** at `target_selection.json/⚑ paired_policy_rows[0]`. None is in the registry; `V-3` resolves `absent_ref` against the registry alone, so none is a reachable target. And `ABS-TARGET-SELECTION`'s reclassification reason ends *"See the paired rows"* — a footnote, to find an absence.

I accept the reason the pair is kept adjacent (V-10 requires they travel together). **Fix:** mirror the seven into the registry with an `also_at` pointer, or qualify `registry_law` to say the registry is the *index* and block-local `declared_absences` mirror into it. Do not leave the law stated unconditionally while seven rows contradict it.

## WARN-4 — `meta.json`'s human-readable provenance is v2's, verbatim, in a v3 pack

`emitted_by: "star-lord (export seam), **KC2 MODEL-COMPLETION RUN Wave-4**"` — this is LIFT RUN Wave-3. `headline` describes the v1→v2 transition (*"v2 is a MODEL-PACK … v1 consumers fail closed on a v2 pack"*). `lap_manifest` lists six laps, **none of them from this run** — no B1 decode, no B4 weights, no W1 walls, no U-7 footage — though the receipt pins all four.

`_schema_version: 3`, `pack_format`, and `⚑ supersession` are all correct, so nothing machine-read is wrong. But `meta.json` is the first file a consumer opens, and it currently attributes the pack to the wrong run. Same family as WARN-2: the structured fields were updated and the prose was not.

## INFO

1. **Truncated digest labelled `sha256`.** All seven devotion rows carry `provenance: "data/kc2/pm4g_played_kit.csv · sha256 2fd5a34792b96125bd55a40891dfd65c"` — **32 hex, half a sha256**. I re-derived the file: `2fd5a347…dfd65c` + `deb43c38…ce0b3`. It is a correct prefix, not a wrong digest, but a consumer doing an equality check against a re-derivation fails. gamora's form, correctly not reshaped — worth reporting alongside the exemption.
2. **`pm4g_played_kit.csv` is not in the receipt's `source_pins`.** The receipt pins `D6_KIT_RESIDUAL` (`d6_player_kit_residual.csv`) — which elrond established is *not* the devotion table (A-B8-1). The pack's flagship rows reach their substrate only via `W1W2_SEAL` → row prose. One hop weaker than every other block, and it is the block surfaced at the top of the receipt.
3. **`player_offense.py` is unpinned while `offense.py` is pinned and hash-guarded.** `CM-SOURCE-PIN` = `c0e17671…` = `offense.py`, which contains neither `CRIT_BASIS` nor `CritLimb` and does not import `player_offense`. The rows' `provenance` prose names the real file; no digest for it exists anywhere. Re-hashing the pin succeeds and certifies nothing about the values. This is *why* BLOCK-1 could ride invisibly. The charter § 1 table chose the pin, so this is a charter-level fix, not a seat error.
4. **DR-1 exemption is visible in the receipt and MIGRATION § 4, not inside the pack.** A consumer reading `provenance.json` alone does not learn that 332 rows use a second provenance dialect. MIGRATION § 4's disclosure is excellent — consider a one-line mirror in `provenance.json`.
5. **Dead predicate at `kc2_baton_v3_schema.py:233`.** `dp = [...]` is computed then `del dp` at :248; the live count is at :239. Harmless, but it leaves two apparent predicates in the block whose comment is about predicate correctness.
6. **`FIND-B2-B3-WORLD-DISAGREEMENT` is absent from MIGRATION § 5** ("the five things most likely to be implemented wrong"). Roughly half of rollable bodies having no AI parameters outranks at least two items on that list for a Godot implementer.

---

## Eye-order items 3 and 4 — audited, no dissent

**P-1 dual reading — the arithmetic is correct and the honesty is real.** 7 blocker rows / 4 distinct holes reconstructs exactly: `ABS-AI-STATE-MACHINE` + 2 children = 3 rows / 1 hole; `ABS-MONSTER-STAT-BLOCKS` + 1 child = 2 / 1; `ABS-TARGET-SELECTION` = 1 / 1; `ABS-DEVOTION-PROC-ICD` = 1 / 1. Parentage is correct. `playability_statement`'s predicate (`blocks_playability AND runtime_choice_required`) independently returns the same 7. Recording the overlap rather than deduplicating it is the right call and the stated reason — *"the seat that lifts the blocks should not also be the one that quietly re-counts them"* — is exactly the principle. **Noting for the record:** BLOCK-1, if upheld, makes this 8 rows / 5 holes.

**Repo weight (R-L13-2) — I concur, ACCEPT.** 21 MB, 15.2 MB `monsters.json`, into a 650 MB `.git`. The pack-wholeness digest law does govern: a pack missing a member has a digest law that is a lie, and GL-6's verify-then-load is the whole consumer contract. `monsters.json` is self-contained and skippable, and MIGRATION § 3 says so explicitly with the byte figure. The ruling is sound and the LFS/attic disposition is correctly a KR harvest item, not an in-run fork. No dissent.

---

## Discipline candidate minted by this review

**A lifted constant inherits its source's corrections, and nothing checks that it did.** The run has now named the instrument-inversion family six times — an instrument returning cleanly, or RED, after it stopped answering the question. BLOCK-1 is its seventh face and a new one: **a value that re-derives perfectly, from a pinned file, through a hash-guarded loader, past a refutation printed two lines above it.** Every gate was green because every gate asked *"does this value match its source?"* and none asked *"does its source still stand behind it?"* Proposed gate shape for the next lift: any lifted string whose source file contains a correction banner referencing it must carry the banner's finding id, or fail.

---

## References

- `/Users/admin/Games/reincarnated-engine/src/reincarnated/simulation/kc2/player_offense.py` (lines 183–224 — the `F-B1r-1` banner and `CRIT_BASIS`)
- `/Users/admin/Games/reincarnated-engine/src/reincarnated/simulation/kc2/mech_lift.py` (lines 1000–1062 — the crit rowset)
- `/Users/admin/Games/reincarnated-engine/src/reincarnated/output/kc2-model-pack-v3-E-s09-cp150-mech-20260826_005956/model/{provenance,math_rules,meta,player_kit,waves}.json`
- `/Users/admin/Games/reincarnated-engine/src/reincarnated/output/kc2-baton-v3-cut-receipt-20260826_005956.json`
- `/Users/admin/Games/reincarnated-engine/src/reincarnated/export/{kc2_baton_v3_schema.py,kc2_baton_v3_emit.py,MIGRATION.md}` (MIGRATION v3 entry, lines 8–175)
- `/Users/admin/Games/reincarnated-engine/src/reincarnated/export/math/2026-08-25-kc2-baton-v3-cut-prereg.md`
- `/Users/admin/Games/reincarnated-engine/src/reincarnated/simulation/MIGRATION.md` (§ 5, `F-B1r-1` replacement text, line 858)
- `/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/gandalf/notes/2026-08-25-kc2-lift-run-charter.md` (L-1..L-13)
- `/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/gandalf/notes/2026-08-24-kc2-model-completion-run-charter.md` (DRIFT-CRITIC F-2 / F-3)
- `/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/elrond/notes/2026-08-25-kc2-lift-b2-b8-curation.md` (§ 11 self-critique, the 158 caveat)

---

**GATE-2 VERDICT: BLOCK** — `ABS-CRIT-MODEL`'s `blocks_playability` and `runtime_choice_required` were both lowered while the crit rows assert, as a ⚑-flagged fact, a board-saturation claim that the pinned source file refutes two lines above the constant; the refutation appears zero times in the pack, receipt or MIGRATION; the prior conductor ruling that ordered the corrected expectation (KC2-MC F-2) has no discharge and was never carried into this run's ledger; and `runtime_choice_required: false` is falsified by `CM-LIMB-OF-RECORD` in the same pack. Consumer impact ≈ ×1.4 on all player damage.

**Release-blocking for downstream consumers: YES, narrowly and specifically.**
- **gamora** (pool-DoT follow-on) — **not blocked.** That work builds on `ABS-CONTROL-APPLICATION` / `ABS-DOT-STACKING` / D-LIFT-1, all of which I verified clean and layer-separated. Proceed.
- **drax / the Godot team** (MIGRATION.md + `math_rules.json`) — **blocked on the crit rows only.** Do not implement `crit_model` from this pack. Everything else in v3 — `L-CC-CONCURRENCY`, the 576 pool weights, the absent-limit ruling, the two DO-NOTs, the paired policy rows, the W2 flags with their mix rider — is verified sound by my own instruments and is safe to build against today.

The rest of this cut is the most rigorously instrumented artifact I have graded on this project. The BLOCK is one row family out of 41,239, it originated upstream at Wave-2, and the seat that carried it did so under the correct byte-equal posture. It is a BLOCK because of where it landed — on the blocker it cleared — not because of how much of the pack it touches.
