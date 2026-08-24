# Finding — 2026-08-24 — gamora KC2-MC **B-3 SUMMONS** (facet (f), SIM cell)

**Reviewer:** jack-ryan (DEV-MODE, Gate 2)
**Severity:** **PASS-with-findings** — 0 BLOCK / 4 WARN / 5 INFO
**Target:** engine `901f7b56` (build), chain `017ac8f3` → `518edee9` → `edfa662a` → `ae934710` → `901f7b56`
**Artifact of record:** `src/reincarnated/simulation/output/kc2-checkpoint-E-s09-cp150-b3-20260824_202328.json`
sha256 `dd13408e108e6f68ccca7fb109e8b04361957f292606389bd4274023c2f78b51` — **re-hashed by me, EXACT**
**Developer:** gamora · **Conductor:** gandalf RUN-CONDUCTOR · **Commission:** L-48 / `R-L48-2`
**Principles applied:** REVIEW_PROCESS #1 (math-before-code), #2 (smoke-gate), #3 (cross-seam impact), #5 (severity matters)
**Disciplines cited:** #1, #2, #8, #12 · **ADRs:** ADR-002, ADR-004 · **Run law:** L-38 (falsifier exact-form, BLOCK force), L-40 (D5), L-47 (three-condition deletion rule; WARN-5)

---

## What I found

B-3 is the strongest build of this run on the axes that have produced its two BLOCKs. Every claim I
tested re-derived exact, the honest fail is genuine and was not rewritten to pass, and the emission
is byte-reproducible at HEAD to two volatile fields. The four findings below are all
**predicate-integrity** findings, not modelling findings: **no figure in this build is wrong, no
digest moved, and no consumer is misinformed by a number.** Two of the four (WARN-1, WARN-2) are the
silent-substitution class recurring at new addresses — but both are materially weaker than BLOCK-1 or
BLOCK-2, and one of them is my own WARN-5 prescription landing at the address it named. The build
clears.

---

## Re-derived independently (never read from the summary)

1. **Artifact sha EXACT.** `dd13408e…` re-hashed against disk.
2. **Emission reproduces at HEAD.** I re-ran the driver and diffed my emission against the artifact
   of record across the entire tree: **exactly 2 differences — `wall_s` and `started_utc`.**
   `dd13408e…` is the emission HEAD produces; it was not hand-edited.
3. **D4 prereg ordering, verified to the second, strictly increasing:**
   math note `15:57:23` → decode surfaces `15:57:39` → ADDENDUM 1 `16:13:58` → ADDENDUM 2 `16:20:07`
   → **emission of record `16:23:28`** → build commit `16:25:35`. Every registered-form deviation
   was published in a standalone zero-code addendum **before both** the emission and the build.
4. **B3-P4's honest fail is GENUINE.** I parsed `d8_request_matrix.csv` at HEAD myself: slot 77 is
   `PERMITTED` in **eleven** of thirteen non-Idle columns and `IMPL` in exactly
   `{ChargeToUseSkill, MoveToUseSkill}`. The registered "all thirteen" is false. **P4 was not
   rewritten** — its `registered_form` on the artifact still quotes the over-stated form verbatim,
   and it is the sole failing row.
5. **B3-P16's corrected form matches my parse exactly**, including slot 76 (`IMPL` in `UseSkill` and
   `Trapped`, `STUB-false` in the other four) and slot 59 (`PERMITTED` ×13). Its **measured** side is
   parsed at run time from the digest-pinned CSV via `request_matrix()`; its **expected** side is the
   registered literal — which is the correct construction, not a K-10 breach: a derived expectation
   would reduce to `_impl_77 == _impl_77`. The `IMPL` set is asserted as **set equality**, not a
   count, which is the specific repair D-B3-1 called for.
6. **All eight predecessor byte-guards re-hashed by me, all exact at HEAD:** mech `20b05cb4…`,
   b1 `0957daaf…`, b2 `a49ef783…`, b1r-of-record `30ef0031…`, b1r-retained `6ac7c4e0…`,
   b2app-evidence `43a6a48b…`, b2app-**SEALED** `a4b84ed5…`; parent `verify_frozen` 20/20 PRE+POST.
   `_sibling()` finds by **hashing candidates**, never by filename.
7. **Decode-surface provenance:** `d8_request_matrix.csv` (`502e1e5b…`) and
   `d3_roster_controller_params.csv` (`41abf9da…`) are **byte-identical** to the legolas D-8 and D-3
   lap evidence in the collaboration repo. Byte-copy claim verified for two of three (see INFO-2).
8. **B3-P14 is a live in-process raise, not a mocked pass.** It constructs a real `sm.SummonFold`,
   calls `route_pet_targeted_control()` on it, and catches the live `sm.PetControlRoutingError` —
   and additionally asserts the observation was **counted** before the raise, so a silent drop
   cannot masquerade as enforcement.
9. **B3-P13 is real, not a stub.** All nine `C-B3-n` refusals carry numeric prices; the four
   zero-priced refusals each carry an explicit basis key (`⚑ measured_how`, `⚑ decoded_half`,
   `⚑ enforcement`, `STRUCTURAL ZERO` in units). C-B3-7 prices the Guardian refusal at **2,567** —
   the refusal does not report itself free.
10. **B3-P12 genuinely derives.** Counts are taken from the tables (`S-B3-*` keys, `C-B3-*` keys,
    `MD-B3-*` keys, `predicates` map) and compared. The D-B3-5 repair is sound: `⚑ derived_summary`
    is the single production site and the top-level `⚑ predicates_*` keys are aliases into it, so
    the two surfaces cannot disagree by construction.
11. **D5 clean:** exactly **one** `b3` artifact on disk. No sibling ambiguity.
12. **Cross-seam (ADR-004):** `MIGRATION.md` carries both BREAKING shifts —
    **S-B3-1** (the new run-wide `ps_{ordinal}_{serial}` actor-id space, with the explicit warning
    that a consumer parsing a wave number out of an actor id "will not see player summons at all")
    and **S-B3-7** (`effect_model` gains a fourth disposition `PET_ROUTING_UNDECODED`). Both are
    correctly framed as consumer-breaking. Zero export schema change.
13. **Smoke:** B-3 tests **30/30 pass**; kc2 suite **484 passed, 1 failed** — the failure is the
    pre-existing `secondary_streams.py:136` bare-`30.0` scan, **outside the B-3 diff** (the build
    touched no file in that path). Blast radius clean.
14. **B3-P17 is well-built.** The middle clause (`UNDECIDED > 0`) is what distinguishes "refused to
    guess" from "never asked" — a Guardian that never *tried* would report 0 casts and look correct.
    Measured: Guardian 0 casts / 2,567 undecided; Deathstalker 5 casts (one per salt).

---

## WARN-1 — `B3-P10` holds only because of an exemption set that is unregistered, and that the code's own comment contradicts

`STRUCTURAL_NUMBERS = {0, 1, -1, 2, 3, 4}` (driver line 176). The comment **three lines above it**
says a structural literal is `(0, 1, -1)`.

I re-ran the AST scan under the narrow set the comment states:

```
STRUCT [-1, 0, 1, 2, 3, 4] -> unguarded: 0   []
STRUCT [-1, 0, 1]          -> unguarded: 2   [(446, 3), (510, 2)]
```

**The widening is load-bearing.** Under the registered text the predicate FAILS and the honest count
is 18/20, not 19/20. B3-P10's registered form carries **no exemption clause at all** ("no bare
numeric literal outside a declared, cited constant"), and the exemption appears in **zero** prereg
documents — I grepped the math note and both addenda.

**Why this is WARN and not BLOCK** — three findings of my own that cut the other way:

- I read both sites. Line 446 is `unjoined[:3]`, a slice bound inside an error message; line 510 is
  `lines[i + 2:]`, a markdown table header offset. **Neither is a magnitude.** Law 3's canonical
  text is *"no fitted constants, no invented rules — a guessed formula never ships"*, and its
  substance is **intact**. Nothing modelling escapes.
- The set is **over-broad by one** — `4` exempts nothing in the current module — which is evidence
  of a principled small-integer heuristic rather than a set fitted to the two hits. A fitted set
  would have been `{0,1,-1,2,3}` exactly.
- **B-3's P10 is strictly stronger than every predecessor's Law-3 predicate.** B-1r's and B-2app's
  scans visited only module-level UPPERCASE assignments; they would never have reached lines 446 or
  510 at all. The deviation makes this predicate weaker than its own text but stronger than the
  instrument it inherited.
- `structural_exemptions` **is** emitted on the artifact's own P10 row — post-hoc self-report, not
  registration, but not concealment either. This is the distinction from BLOCK-1, which was
  undisclosed on all six governing surfaces.

**Cite:** L-38 exact-form law; Discipline #1.
**Action:** register the exemption set with its rationale in the B-4 prereg (or narrow it and cite
the two sites individually), and repair the comment/code contradiction. Publish the narrow-set
non-vacuity probe above — it is the probe this predicate was missing.

---

## WARN-2 — `B3-P11` is a tautology on the half it checks, and silent on the half it does not

This is my own **WARN-5** prescription (`R-L47-1`, *"fix by DERIVING, not re-running"*) landing at
the address it named, so I am grading my own instruction.

**The repair is correct.** `art["addenda"] = _addenda_derived(docs)` where `docs = _doc_set()` — a
disk glob. There is no literal to be stranded. That is exactly right, and it is the substance of
what I asked for.

**The predicate that grades it is vacuous.**

```python
"holds": set(_addenda_derived(_doc_set())) == set(art["addenda"]),
```

Both sides are the same function over the same disk. It cannot fail except by mid-run disk
mutation. Its registered falsifier — *"a doc on disk absent from the array, or an array entry absent
from disk"* — describes two events that are unreachable by construction.

**And its second registered clause was never implemented.** The registered form reads: *"the
artifact's `addenda` array **and every prereg/quarantine enumeration string** are derived at emission
time."* The `⚑ quarantine` string is a hand-typed literal carrying a hand-typed count — *"The **SEVEN**
shifts are enumerated…"*. It is neither derived nor checked. `holds` only ever looks at `addenda`.

**Currently harmless:** there really are 7 shift rows, and B3-P12 independently counts the `S-B3-*`
keys and compares them to the declared `n_shifts`. No false statement ships. But P11 reports green
while proving nothing on one half and nothing at all on the other — which is BLOCK-2's class (a
registered clause that never became code) at a third address, and D-B2app-4's class (an expectation
built from the same abstraction the implementation used) at a second.

**Cite:** L-38; K-10's standing clause; `R-L47-1`; Discipline #8.
**Action:** this is the finding I most want repaired. Either derive the quarantine enumeration
strings (P11's registered form) or narrow P11's registered form to the `addenda` array alone and
declare the quarantine string `inherited-not-re-derived` per `R-L47-2`. Give P11 a falsifier it can
actually fail — a mutation probe that injects a bogus array entry.

---

## WARN-3 — the four deletions are LEGAL, but condition (3)'s stated mechanism is false

**Ruling: all four deletions (`f31a4bde…`, `5c6a943f…`, `753a9659…`, `7ae29a7f…`) are LEGAL under the
L-47 three-condition rule.**

- **(1) uncited non-candidates** — satisfied. None is referenced by any consumer, sibling or commit.
- **(2) declared by sha with reason in an immutable prereg doc before the seal** — satisfied
  exactly. ADDENDUM 2 § 4 (`ae934710`, 16:20:07) precedes the emission of record (16:23:28). The
  reasons are specific and the differing predicate-set counts (17/19/20/20) are precisely the D5
  hazard retention would have created.
- **(3) witness independently reproducible** — **satisfied in substance, but the declared mechanism
  does not exist.** ADDENDUM 2 § 4 states: *"Any of the four is reconstructible by checking out the
  commit that produced it and re-running."* I checked the entire 16:11–16:26 commit window. The only
  commits in it are `edfa662a` and `ae934710`, **both doc-only**. The four emissions came from
  uncommitted working-tree states; **no commit that produced them exists.**

What rescues condition (3) is the *other* witness in the same section: the determinism claim. I
reproduced it exactly — **417 diverted**, terminals **155/156/152/151/151 → 161/156/161/161/156**,
**921 UNDECIDED** on LEG 1b. The ensemble is reproducible at HEAD, so the deleted artifacts' shared
substrate is independently witnessed even though the artifacts are not.

**Sub-nuance the rule does not yet address:** `7ae29a7f…` **is** cited — by ADDENDUM 2 § 3 itself, as
the sole evidence for self-disclosure D-B3-5 — and then deleted in § 4. The evidence for a published
defect no longer exists and cannot be regenerated at HEAD, because the repair is in HEAD. Deleting
the artifact that *is* a disclosure's evidence is a different act from deleting a superseded
intermediate.

**Action:** correct condition (3)'s wording in the B-4 prereg — the reproducible witness is the
**deterministic ensemble**, not a commit checkout. I will carry the self-citation corner into the
run-close governance proposal as a refinement to the three-condition rule.

---

## WARN-4 — capability-vs-measurement key separation not carried to the Guardian surface

`B3-P17` emits `guardian_casts: 0` and `guardian_undecided_opportunities: 2567`. Both are
**measurement** keys. No key on the surface asserts **capability** — that the Guardian of Empyrion is
a real, castable, roster-derived summon whose zero is an artifact of *this pilot's continuous
channel*, not an absence, a stub, or an unimplemented record.

The prose carries it (`⚑ what_it_measures`). The key names do not. A consumer keys on names.

This is `gate_rolled` from L-44 WARN-4 one build later, at a new address. gamora split that key
correctly at L-46 — surfacing the J-9 *true-as-capability / ZERO-as-measurement* nuance that the
conductor then banked. The pattern is established; it did not travel. L-48 already routes the
Guardian to a Wave-4 baton row under the J-9 split, which is the right disposition — but the baton
**consumes this artifact**, so the split wants to be in the key names now, not only in the row that
reads them later.

**Cite:** L-44 WARN-4 / L-46 `gate_rolled` precedent; Discipline #12.
**Action:** add a capability key beside the measurement keys on the P17 / summon-roster surface.

---

## INFO

- **INFO-1 — the engine tree was not byte-clean at gate time.** Three tracked files carry
  uncommitted modifications timestamped **18:28–18:30**, well after the build (16:25):
  `design/working-agreement/engineering-disciplines.md` (+77), `kit_compiler/kit_compiler.py`,
  `kit_compiler/smoke_kf4_compiler.py`. All are **outside B-3's graded surface**, and my byte-exact
  re-run proves the grade is unaffected. Two process notes: (a) the single-writer discipline covers
  *commits* and evidently not working-tree writes — worth a line in the B-4 brief; (b)
  `engineering-disciplines.md` is jack-ryan-owned, and an uncommitted 77-line addition to it wants
  attribution before it lands.
- **INFO-2 — one decode surface's byte-copy claim is unverifiable.**
  `d3_controller_groups_decode_README.md` has no source copy in either repo, so it is the one of the
  three pinned surfaces I could not check against an upstream original. The other two verified exact.
  It is digest-pinned in `summons.py`, so it cannot drift *after* this build — but its provenance
  rests on the commit message.
- **INFO-3 — `B3-P13`'s zero-basis check is looser than it reads.** It uses substring matching over
  joined key names (`"measured_how" in " ".join(keys)`). Correct today; a key named
  `measured_however` would satisfy it. Prefer exact key membership.
- **INFO-4 — the SEVEN/EIGHT guard count is reconciled, not inconsistent.** B3-P9's registered form
  says "SEVEN predecessor byte-guards … plus b1r-retained … making EIGHT hashed objects", and the
  artifact carries `n_guards: 8`. L-48's "EIGHT" and the note's "SEVEN" are the same fact. Recorded
  so it is not re-found as a discrepancy.
- **INFO-5 — the one pre-existing kc2 failure is P10's own family.**
  `test_AC_10_10_the_literal_30_0_appears_NOWHERE_in_the_arena_surface` is an AST bare-literal scan
  over `kc2/*.py`, red at `secondary_streams.py:136`. Same discipline as B3-P10, two instruments,
  one green and one red. Worth one line in the B-4 brief.

---

## Reviewer's own emission, declared under the L-47 three-condition rule

My non-vacuity re-run produced
`kc2-checkpoint-E-s09-cp150-b3-20260824_222904.json`, sha256
`422f07a6daa8b0b1858165b759a458c4eaeb8a82b063bbfccc72e50173389501`, **deleted immediately after the
diff.** (1) Uncited non-candidate, never proposed for the seal. (2) Declared here by sha with reason
before the seal. (3) Witness reproducible — it differed from `dd13408e…` in exactly `wall_s` and
`started_utc`. Exactly one `b3` artifact remains on disk; no D5 ambiguity was created by this review.

---

## Verdict

**PASS-with-findings. B-3 SEALS on sha of record
`dd13408e108e6f68ccca7fb109e8b04361957f292606389bd4274023c2f78b51`** — one artifact, no ambiguity,
byte-reproducible at HEAD.

**Facet (f) SIM = PARTIAL** as claimed: actor model + cast-gate + exposure band CLOSED; offense and
life REFUSED with `MD-B3-1` commissioned. The cell line in § 11 is not over-read.

The headline is earned: the two summons genuinely split on cast route, and **B-3 refused to guess the
Guardian's mid-channel `IMPL` cell rather than inventing a availability** — 0 casts against 2,567
UNDECIDED opportunities, with the refusal priced. That is Law 3 held under pressure, and it is the
right call.

## Action

- [ ] **gamora** — WARN-1: register `STRUCTURAL_NUMBERS` (or narrow it and cite the two sites); fix
      the comment/code contradiction; publish the narrow-set probe.
- [ ] **gamora** — WARN-2: give `B3-P11` a falsifier it can fail, and either derive the quarantine
      enumeration strings or label them `inherited-not-re-derived`.
- [ ] **gamora** — WARN-3: correct condition (3)'s wording (deterministic ensemble, not commit
      checkout).
- [ ] **gamora** — WARN-4: add a capability key beside the Guardian's measurement keys.
- [ ] **gamora** — INFO-3 exact key membership; INFO-1(a)/INFO-5 as brief lines.
- [ ] **jack-ryan** — carry the deleted-evidence-of-a-disclosure corner into the run-close
      refinement of the L-47 three-condition rule.
- [ ] **conductor** — all four WARNs ride the **B-4 prereg** as a repair cluster; none gates the
      seal, none moves a figure, none moves a digest.
- [ ] **Matt — no decision required.** All findings are within-seam predicate repairs per **ADR-002**.

## References

- `~/Games/reincarnated-engine/src/reincarnated/simulation/math/kc2-mc-b3-summons-2026-08-24.md` (§ 7)
- `~/Games/reincarnated-engine/src/reincarnated/simulation/math/kc2-mc-b3-summons-ADDENDUM-2026-08-24.md`
- `~/Games/reincarnated-engine/src/reincarnated/simulation/math/kc2-mc-b3-summons-ADDENDUM-2-2026-08-24.md`
- `~/Games/reincarnated-engine/src/reincarnated/simulation/kc2/summons.py`
- `~/Games/reincarnated-engine/src/reincarnated/simulation/scripts/gamora_kc2_mc_b3_summons_2026_08_24.py`
- `~/Games/reincarnated-engine/tests/test_kc2_mc_b3_summons.py`
- `~/Games/reincarnated-engine/src/reincarnated/export/MIGRATION.md`
- `~/Games/reincarnated-engine/data/kc2/d8_request_matrix.csv`
- `~/Games/reincarnated-engine/src/reincarnated/simulation/output/kc2-checkpoint-E-s09-cp150-b3-20260824_202328.json`
- `~/Games/reincarnated-collaboration/agentic_orchestration/gandalf/notes/2026-08-24-kc2-model-completion-run-charter.md` (L-38, L-40, L-47, L-48)
