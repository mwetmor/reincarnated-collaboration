# KC2-PLAY · T-A PREREGISTRATION **v1.7** — the goalposts for the graded run on the **v3.4.2** substrate

> ⚑ **STATUS: IMMUTABLE ON COMMIT — v1.7, authored 2026-09-29. SUPERSEDES v1.6 FORWARD.**
> *(The filename carries the series' `2026-09-20` prefix; the document's date is 2026-09-29.)*
>
> ⚑ **v1.7 = v1.6 + EXACTLY ONE CHANGE: `TA-X-06` MOVES FROM `EXACT` TO `UNGRADEABLE-declared`.**
> **Authority: Matt, `Q83(b)` — RULED YES, 2026-09-29 (charter ledger KP-110).** Everything else in
> this file is carried from v1.6 (`db2c0ca3…`) **BYTE-FOR-BYTE IN SUBSTANCE**: no row is added,
> widened, narrowed, re-derived to a new value or re-worded beyond what the one change forces.
> **Every site the change touches is marked `⚑ v1.7` in place and listed at § 0.2**, so the pre-read
> is a diff of named sites. **Every pin was re-derived this session and NONE moved** (§ PINS).
>
> ⚑ **THE REASON, IN ONE PARAGRAPH.** `TA-X-06` asserts distinctness D — `port(W1, s) ≢
> port(M-POL-2, s)` on at least one salt — and it was classed `EXACT` while the only mechanism that
> makes that relation true in the oracle is the avoidance limb, whose sole trace is `TA-B-14`'s
> `n_avoidance_vetoes` (**2 against 0**): a **report-only** counter with no width and **no published
> trigger rule**, on a boundary `ABS-ARENA-BOUNDARY` declares absent. The wall contributes nothing —
> its clamp counters are zero on every arm. **The row is therefore unfalsifiable in the honest
> direction:** a correct port cannot green it without inventing a veto rule nobody wrote, and under
> Q87 (*"all EXACT rows green"*) that would seal REFERENT-v1 on a fiction. Declaring it
> `UNGRADEABLE-declared` keeps the row, its relation and its argument **on the record** (§ F.2e); it
> **stops it gating**; and it **rescues nothing** — v1.4's grade of record `STRUCTURAL @ coverage
> 89/89` stands independently on `TA-X-07`, and no graded result exists under v1.6 for the change to
> move.
>
> ⚑ **WHY A NEW VERSION AND NOT A HALT.** v1.6 is immutable on commit, and `WARN-16` makes any
> change after a graded run exists against it a HALT to Matt. ⚑ **No graded run exists against
> v1.6** — graded attempt 1 HELD at the commitment boundary for exactly this ruling (KP-106; KP-107:
> *"W3 HOLDS only for Matt's Q83(b)"*). The ruling names its own route (KP-110: *"via prereg v1.7
> committed ALONE before attempt 1 (v1.6 is immutable; no graded run exists yet, so this is a new
> dated version, not a HALT)"*).
>
> ⚑ **THIS FILE IS IMMUTABLE ONCE COMMITTED. ANY CHANGE AFTER A GRADED RUN EXISTS AGAINST IT IS A
> HALT TO MATT — `WARN-16`.** Not a correction, not an erratum, not a clarification: a **HALT**.
> **A prereg that can be edited after results exist is not a prereg.**
>
> ⚑ **D4 HELD: this file is committed ALONE, zero code, before any graded run against v3.4.2
> exists.** The substrate was declared final at **KP-103** before a line of v1.6 was written, and
> nothing in it has moved since (§ PINS).
>
> **Authority, in Matt's words and the conductor's sequencing — carried from v1.6, re-pointed at v1.7
> only where the one change requires:**
> * ⚑ **Q83(b) — RULED 2026-09-29 (KP-110): YES. `TA-X-06` → UNGRADEABLE-declared, via prereg
>   v1.7.** **This is the one change.**
> * ⚑ **Q85 — RULED 2026-09-28 (KP-83): the graded-run cap RESETS — TWO graded attempts.**
>   ⚑ **v1.7: THE ALLOWANCE ATTACHES TO v1.7, AND NONE OF IT HAS BEEN SPENT — no graded run executed
>   under v1.6.** Counter **`0` of `2`** (§ G.1).
> * ⚑ **Q87 — RULED 2026-09-28 (KP-83): REFERENT-v1 seals on ALL EXACT rows green + coverage 89/89
>   mapped + T-B reported DIAGNOSTIC + Matt's T-C yes.** ⚑ **v1.7: "ALL EXACT rows green" = `28`
>   rows** — `TA-X-01…30`, less the struck `TA-X-23`, less the declared `TA-X-06`. The conductor's
>   earlier *"feel-load-bearing rows"* framing was circular and stays **withdrawn**.
> * ⚑ **L2 (KP-84): attempt 2 fires only after jack-ryan Gate-2 PASSes drax's repair of an
>   attempt-1 STRUCTURAL red.** A repair without a passed gate does not buy the second attempt.
> * **F5 (KP-49) stands unchanged: the EXACT half is the instrument; the tolerance half is a
>   DIAGNOSTIC and GATES NOTHING.**
> * **Sequencing:** KP-103 (v1.6 written ALONE, D4) · KP-106 (attempt 1 HOLDS for `Q83(b)`) ·
>   ⚑ **KP-110 (Matt rules `Q83(b)` YES; v1.7 ALONE before attempt 1).**
>
> **Author:** gamora (simulation + spirit-guide seam), Run KC2-PLAY SEAL LAP.
> **Decision rules only.** ⚑ **NO BAND WIDTH IS MINTED HERE, AND EVERY WIDTH IN `P-a` IS VOID
> (§ A.4). Where a width is owed it is left named and empty.**
> **v1.6 (`db2c0ca3…`), v1.5 (`efac4bd5…`), v1.4, v1.3, v1.2, v1.1 and v1.0 are NOT edited.**
> **v1.4's grade of record — `STRUCTURAL @ coverage 89/89` — does not move.** Nothing in this file
> regrades, rescues, widens or reclassifies anything that was graded: the one reclassification is of
> a row that has **never been graded under v1.6 or v1.7**.
>
> **Occasioned by:** charter ledger **KP-110** (Matt's `Q83(b)` ruling) · **KP-106** (jack-ryan's
> v1.6 pre-read and the attempt-1 hold) · **KP-105** (v1.6 sealed; the seal blocker surfaced).
> v1.6's own occasion list (KP-83 … KP-103) is carried in § A as lineage.

---

## § 0 · ⚑ CHANGE TABLE — v1.6 (2026-09-29, `db2c0ca3…`) → v1.7 (2026-09-29) — **ONE ROW**

| # | clause | v1.6 | **v1.7** | reason | authority |
|---|---|---|---|---|---|
| **1** | ⚑ **`TA-X-06`** — distinctness D, `port(W1, s) ≢ port(M-POL-2, s)`, ≥ 1 salt | `EXACT`, carried AS CLASSED; `Q83(b)` OPEN; *"it now BLOCKS THE SEAL"* (§ F.2e, `H-5`, `OQ-1`) | ⚑ **`UNGRADEABLE-declared`.** On record under its own id; the relation is **emitted and printed** with its label; it **enters no verdict antecedent, counts in no `PASS` label, and is not a Q87 seal condition** | the header paragraph; § F.2e's reasoning, carried verbatim | ⚑ **Matt, `Q83(b)` YES — KP-110** |

### 0.1 · THE COUNTS

| | preconditions | **EXACT** | UNGRADEABLE-declared | DIAGNOSTIC ids | emitted-not-graded |
|---|---:|---:|---:|---:|---:|
| v1.6 | 5 | **29** | 0 | 19 (0 gating) | 2 |
| ⚑ **v1.7** | 5 | ⚑ **28** | ⚑ **1 (`TA-X-06`)** | 19 (0 gating) | 2 |

⚑ **The id namespace does not move:** `TA-X-01…30`; `TA-X-23` struck at v1.2 and retired;
`TA-X-06` **retained on record under its own id**, never re-used.
⚑ **Q87's reading at v1.7: "all EXACT rows green" means these 28** — `TA-X-01 · 02 · 03 · 04 · 05
· 07 · 08 · 09 · 10 · 11 · 12 · 13 · 14 · 15 · 16 · 17 · 18 · 19 · 20 · 21 · 22 · 24 · 25 · 26 · 27
· 28 · 29 · 30`. **The count's history, so it never moves silently again (jack-ryan WARN-2, #73):**
Matt ruled Q87 when v1.5 carried **26** · v1.6 carried **29** (`TA-X-28/29/30` added after the
ruling, stricter; reconciled on the `Q83` queue row at KP-106) · ⚑ **v1.7 carries 28 — and the one
row removed is the one Matt removed by name.**

### 0.2 · EVERY SITE THE ONE CHANGE TOUCHES — the complete edit list against v1.6

| site | what changed | why it had to |
|---|---|---|
| header · § 0 | new | the version, its authority, its reason |
| § PINS | the opening paragraph and one column heading re-state the **v1.7 re-derivation**; two rows added to *Documents of record* (v1.6 itself; the pre-read) | the pin rule: a new version re-derives every pin |
| counts line (under the sealed cells) | 29 → **28 EXACT + 1 UNGRADEABLE-declared** | the one change |
| § A | one italic line under the heading: *carried verbatim as the v1.5 → v1.6 record* | § A's row 11 (29) and row 13 (`TA-X-06`) are true **of v1.6** and are superseded forward by § 0, not edited |
| § B.3 | `TA-X-03…06` → `TA-X-03…05`, with `TA-X-06`'s status in parentheses | a `P-2` red cannot make a declared row "more" ungradeable |
| § F.2 | the heading, and the `TA-X-06` row's tolerance / disposition / reason cells | the one change |
| § F.2e | the heading, the **status** text and the **closing** paragraph replaced by the ruling and what the declaration means mechanically; **the six-point reasoning (and its lead-in) is carried verbatim** | v1.6's status text (*"`Q83(b)` IS OPEN"*) became false at KP-110 |
| § G | one clause after the *Order* paragraph (a declared row is **not** "an EXACT row UNGRADEABLE"); the `PASS` label (28/28); verdict file `prereg_version` → `"v1.7"` and **one** new field, `declared_ungradeable` | without the clause, a literal grader could read `UNGRADEABLE-declared` into the `INDETERMINATE` antecedent — the INFO-1 shape |
| § G.1 | the counter line | Q85's allowance attaches to v1.7 |
| § H | `H-5` discharged | ruled |
| § I | `OQ-1` marked RESOLVED BY RULING; the lean is retained verbatim as the record | ruled |
| footer | new | the version |

⚑ **Nothing else is edited.** In particular § F.3 CLASS V's mandatory `TA-B-14` sentence —
*"This is the counter that carries `TA-X-06`'s ENTIRE MECHANISM, and it is the one the prereg
declined to band"* — **stays verbatim, because it is still true and it is the reason for the ruling.**

### 0.3 · WHAT IS DELIBERATELY NOT FOLDED IN — one change, so the pre-read is trivial

1. ⚑ **`GM-OQ-1` (KP-108) — widening `TA-X-09` to all 29 `math_rules` test vectors.** **NOT HERE.**
   `TA-X-09` stays at **9**; ceiling `C-h` and `OQ-9` are carried verbatim. It is a separate change
   for a separate version with its own pre-read.
2. **jack-ryan's v1.6 pre-read "v1.7 (not now)" items** — extend § C.7 to name the sealed-cell epoch
   (WARN-1); derive § F.5 cl. 6's instance list mechanically (WARN-4). **NOT HERE.** Both are carried
   at § 0.5 as **grader obligations at emission**, exactly as he stated them.
3. **KP-110's other rulings** — T-C *"seal: yes with findings"*, the two named model gaps (enemy AI;
   elite/champion damage), the enemy-AI own-files inventory, the JOIN-1 launch sheet. **They are
   recorded on the ledger and change no row here.** Q87's four seal conditions are carried
   unchanged; which of them is met is a run fact, never a prereg assertion.
4. **drax's view-only legibility pass** (KP-110) — `kc2_runtime` byte-unchanged; no bearing on any row.
5. **KP-107's port measurements** — read into no row; the like-for-like comparison is T-A itself.

### 0.4 · ⚑ THE GRADED-RUN ALLOWANCE — **ATTACHES TO v1.7; `0` OF `2` SPENT**

⚑ **Q85's two graded attempts now attach to v1.7.** **None was spent under v1.6: no graded run
executed against it** — W3 held at the commitment boundary for `Q83(b)` (KP-106) and was still
holding at KP-107 (*"every W2 piece is DONE. W3 HOLDS only for Matt's Q83(b)"*). ⚑ **Counter at
v1.7: `0` of `2`.** L2 is carried unchanged. The v1.4 and v1.5 attempts stay on the record as
attempts against the **v3.3** reference (§ C.7 cl. 4), and are not priors.

⚑ **AND THE ESCALATION THIS CLOSES, GIVEN ITS DISPOSITION IN ONE LINE (CLAUDE.md corollary: an
escalation overtaken by events still requires one):** the conductor's KP-105 pre-ruling and
jack-ryan's objection to it (a `TA-X-06`-only red would spend an attempt on a row no port change can
move) are **RESOLVED BY RULING, not by supersession** — the branch `STRUCTURAL @ TA-X-06-ONLY`
cannot occur under v1.7, because `TA-X-06` enters no antecedent. **jack-ryan's preferred option (1),
*"route `Q83(b)` to Matt before attempt 1 fires"*, is the one that was taken, and it was right.**

### 0.5 · jack-ryan's v1.6 PRE-READ — **CARRIED FORWARD AS IT STOOD**

**Source:** `agentic_orchestration/qa/findings/2026-09-29-run-KC2-PLAY-w2-prereg-v1.6-preread.md`
(sha256 **`5a5f45d76098746ce1dbd31d0091b9a7d62f16978fb52a21ff27990181e0b6c0`**, derived this
session) · verdict **PASS-WITH-WARNS — 4 WARN · 3 INFO · 0 BLOCK** · ledger KP-106.
⚑ **Every item below is carried as he stated it. None is actioned inside this file** (§ 0.3); the
column on the right records where each stands, not a new disposition.

| item | his finding (one line) | his action, as stated | **where it stands at v1.7** |
|---|---|---|---|
| **WARN-1** | `TA-B-01`'s oracle side is `[M-POL2]`, sealed **2026-08-25**, pre-v3.3 — an epoch § C.7 does not name; § A.4 voids widths from the same cell | **grader, at emission:** print *"`[M-POL2]`, sealed 2026-08-25, pre-v3.3 substrate"* beside the array; **v1.7:** extend § C.7 | ⚑ **OPEN — grader obligation at emission.** The § C.7 extension is **not** folded here (§ 0.3 item 2). Gates nothing (DIAGNOSTIC class V) |
| **WARN-2** | Q87 was ruled over **26** EXACT rows; the instrument carried **29** | **conductor:** one ledger line reconciling 26 → 29 before a PASS is claimed | ⚑ **DISPOSITIONED by the conductor on the `Q83` queue row (KP-106).** v1.7 re-states the count forward: **26 → 29 → 28** (§ 0.1) |
| **WARN-3** | the `Q83` queue row still called (b) record-only (*"nothing is rescued"*), false under Q87 | **conductor:** restate the `Q83` row with its Q87 stakes before routing | ⚑ **DISPOSITIONED by the conductor (row RESTATED, KP-106) — and DISCHARGED by the ruling (KP-110)** |
| **WARN-4** | § F.5 cl. 6's instance list was not re-derived: `TA-X-25(c)`, `TA-X-28(a)` (absence-satisfied) and `TA-X-29(d)` (unexercised: 0 of 29 inert records in waves 151–160) are missing | **grader:** apply cl. 6's rule to all three; `TA-X-29(d)` prints *"unexercised: 0 of 29 inert records fall inside waves 151–160"*; **v1.7:** derive the list mechanically | ⚑ **OPEN — grader obligation at emission.** The rule binds and the list is illustrative, so the three inherit the print obligation with no edit. Mechanical re-derivation **not** folded here |
| **INFO-1** | § F.5 cl. 8's blanket wording vs `TA-X-29(d)` | none required: cl. 8 forbids reddening a port for **not implementing** an absence; `(d)` reds a port for **inventing** supply — opposite directions, both stand | ⚑ **carried: the grader treats `TA-X-29(d)` as GRADABLE** |
| **INFO-2** | two grains under one fold name (`344` actors in `P-5`; `193` records in `TA-X-29(a)`) | **grader:** label the grain in `gmag_conformance` — `attr_limb_records: 193` beside `attr_limb_actors: 344` | ⚑ **OPEN — grader obligation at emission** |
| **INFO-3** | `P-4` red at writing (the `.app` reported the v3.4 pack) | none — declared on the face | ⚑ **a run fact, read at the run and never asserted by this file.** (KP-107 records the `.app` header reading `5cab7433…` by running the binary) |
| *Answers* | `OQ-1` carry-as-classed **correct** · `OQ-2` `TA-X-25`'s re-authoring **RATIFIED** (a substrate re-derivation, not a goalpost move) · `OQ-9` **honest scope**, and *"wrong about every hit the player takes"* belongs on the **W4 packet's** face beside § F.5 cl. 10 | — | `OQ-1` **resolved by ruling**; `OQ-2` carried ratified; the `OQ-9` sentence stays a **W4-packet obligation**, not a prereg edit |

---

### ⚑ PINS — **every pin re-derived this session by `shasum -a 256`, none retyped from a prior document** — ⚑ **v1.7: RE-DERIVED AGAIN, AND NONE MOVED SINCE v1.6**

> ⚑ **v1.7 RE-DERIVATION, 2026-09-29.** All **14** pinned files (`P-a` · `P-b` · `P-c` · `P-d` ·
> `P-e` · `P-e′` · `P-i` · `P-j` · the **six** `P-l` notes) reproduce v1.6's digests **exactly**.
> **Both pack digests were RE-COMPUTED from their member files by `pack_digest_law_exact`** and
> reproduce — `5cab7433…` with **17/17** members verified, `978f54ab…` with **7/7**, and the
> reference manifest's `cross_pin.model_pack_digest == 5cab7433…` verified. The three sealed cells
> reproduce digest **and** byte count. The documents of record reproduce. `P-k` (still *"derived at
> use"*) reads `58205679e36f0e0361ccd41c844d6bc254ada034447dd1f80e2a46a2b47c7aca` this session —
> printed for the reader; **its pin law is unchanged**. ⚑ **The table's right-hand column is v1.6's
> movement-since-v1.5, carried as lineage. Movement since v1.6 is NONE on every row.**

*(The standing rule, born at KP-20 and re-earned at KP-43 § 0.1: **a new version re-derives every
pin it carries, including the ones it believes are unchanged, and prints them in one table.** At
v1.5, one of ten had to be replaced because it was wrong. At v1.6, **two moved, one was replaced,
three are new, and the model pack is repointed whole.**)*

| # | artifact | **sha256 — derived 2026-09-29** ⚑ *(re-derived at v1.7: identical)* | movement since v1.5 *(v1.6's column, carried)* |
|---|---|---|---|
| **P-a** | `agentic_orchestration/gamora/notes/2026-09-20-kc2-play-ta-band-widths.md` | ⚑ **`1c80f08075a1ed0e30e30b348752d2505b39994f7e2c55c348413f6e591248f9`** | ⚑ **MOVED.** v1.5 pinned `7a5d4aa3…`; **Addendum 4 (THE WARRANTS, 2026-09-21 23:16) landed after v1.5 was filed.** ⚑ **AND EVERY WIDTH IN IT IS VOID AT v1.6 — § A.4.** The file is pinned as the **construction** of record, never as a live width table |
| **P-b** | `agentic_orchestration/galadriel/notes/2026-09-20-kc2-play-w1-tb-expected-values-and-u-rider.md` | ⚑ **`d48512aa6e3c9ea70de6675750880a6c8914f0984c3cfe65c6ccb9a24403438f`** | ⚑ **MOVED — and it reproduces KP-88's declared new pin exactly.** galadriel's full 10,959-frame re-read is **appended** to the same file (append-only). v1.5's `8186202c…` is superseded |
| **P-c** | `…/2026-09-20-kc2-play-w1-tb-expected-values.json` | **`a8b85331764ba3fe90f45cf7cd6f1a25f6dc0dae4a7e7fa555c487f0b153ea0b`** | **unchanged — re-derived, not carried** (KP-88 says so; this confirms it) |
| **P-d** | `…/2026-09-20-kc2-play-w1-tb-release-labels.json` | **`15dace604c8d5bb4888223a8b25a07a038bae44431ebd194d682545c0f29c58a`** | **unchanged — re-derived** |
| ⚑ **P-e** | ⚑ **REPLACED.** `~/Games/reincarnated-engine/src/reincarnated/simulation/math/kc2-play-v3p4-roster-basis-rebase-2026-09-21.md` | ⚑ **`4b7b78c834c7fbabd61700dda3e730a95ab89990bfa01470e8fb293f41ac7a73`** | ⚑ **THE GOVERNING DOCUMENT FOR `TA-X-25` / `TA-B-15` MOVES TO THE REBASE NOTE.** v1.5's `P-e` (the v3.3 monster-offense prereg, `27fc5937…` — **re-derived here, unchanged, and retained at `P-e′`**) describes a substrate that no longer exists. **It is the ROSTER-BASIS REBASE that states what `TA-X-25`'s mechanism became** |
| **P-e′** | `…/math/kc2-play-v3p3-monster-offense-prereg-2026-09-20.md` — **lineage only** | **`27fc59378aee8c9d412f486a63864a3b2ceb5c5473520b60ad80128d47d99cdc`** | unchanged — re-derived. **Its § B.4 body-state table is SUPERSEDED by § A.3 below and no row grades against it** |
| ⚑ **P-f** | ⚑ **REPLACED BY THE PACK.** The v3.3 lifted-rows file `kc2-lifted-rows-KC2PLAY-v3p3-monster-offense-20260920_214408.json` is **not a consumed artifact at v1.6** | — | ⚑ **STRUCK AS A PIN.** Its rows are inside `P-h`'s `monster_offense.json`, which is pinned member-by-member. **Pinning a lift's intermediate file alongside the pack it was cut into is pinning the same fact twice and inviting the two to disagree** |
| ⚑ **P-g** | ⚑ **STRUCK, same reason** (the v3.2 lifted rows) | — | inside `P-h` |
| ⚑ **P-h** | ⚑ **REPOINTED WHOLE — THE MODEL PACK.** `…/src/reincarnated/output/kc2-model-pack-v3-E-s09-cp150-mech-v3p4p2-20260929_063506` | ⚑ **pack digest `5cab743335c6a721f57680e151d6e949d3387ca164342ffc97fefd04916835e2`**, **re-derived from the 17 member files by the manifest's own `pack_digest_law_exact`** (two ASCII spaces, `\n` between lines only, no trailing newline, relpath-ascending, UTF-8) — **not read off the manifest.** All **17** member digests verified against the manifest: **17/17 match.** Full member table at § B.5 | ⚑ **THE OBJECT THE RE-BASE MOVED. See § A.1 — it moved LESS than v1.5 § H.3 assumed, and that is a derived fact, not an assumption** |
| ⚑ **P-h2** | ⚑ **NEW — THE REFERENCE PACK.** `…/output/kc2-reference-pack-v3-E-s09-cp150-mech-v3p4p2-20260929_063506` | ⚑ **pack digest `978f54ab275de4f932fd8a7116b3fd44646268ee2b625fcae5516e81ab77b7de`**, re-derived the same way from **7** members, 7/7 verified | ⚑ **NEVER PINNED IN ANY VERSION, AND IT CARRIES A CROSS-PIN THAT MAKES THE OMISSION LOAD-BEARING:** its manifest's `cross_pin.model_pack_digest` is `5cab7433…`, with the law *"a reference pack graded against a different model pack is grading two different things and will not know it."* **`P-5` enforces it** |
| **P-i** | `~/Games/reincarnated-engine/data/kc2/pm4p_leech_resistance.csv` (**3,312,159 B**) | **`cb6a008bde1e102573181968ab7f60958cd28fee07ff8736078fa092a80dd62e`** | **unchanged — re-derived.** `TA-X-26` grades against it |
| **P-j** | `~/Games/reincarnated-engine/data/kc2/pm4l_mitigation_by_body.csv` (**5,444,380 B**) — lineage only | **`a8c1ffd97dc703419f8447f3d7bbba3903e0f14d2c2e6746a938ceefae9ecec6`** | unchanged — re-derived; **graded by no row** |
| ⚑ **P-k** | ⚑ **NEW — `ANCHOR-169`'s carrier.** `~/Games/reincarnated-engine/data/kc2/pm2_tg2_monster_timing.csv` | ⚑ **derived at use in § A.3 (169 distinct `record` values, `BOTH-128 = 128`)** | ⚑ **v1.5 asserted `ANCHOR-169`'s cardinality and `BOTH-128`'s and pinned NEITHER carrier. Both numbers reproduce, and now they reproduce against a named file** |
| ⚑ **P-l** | ⚑ **NEW — THE SEAL-LAP MATH NOTES, the derivation chain behind § B.5's fold settings.** | `kc2-c2-per-cast-energy-cost-fold-2026-09-28.md` **`b42684e55325bd4caf705b1e7d43462acb5c5818cd5abe3d79eb0d3b9ba6f8c7`** · `kc2-c7-insufficient-energy-refuse-fold-2026-09-29.md` **`072f9ab787ec840a9bc62ae76a0576fa5db7be0da0b63457851557ea164a7e1f`** · `kc2-play-nine-winner-surface-reconstruction-2026-09-29.md` **`2c7c3679af67569fff88bb56837ea1ba37499fe9fcbeca85ab63a473b0d7a6dd`** · `kc2-play-upn4-occupancy-by-pilot-2026-09-29.md` **`787d1a99d9adfedbb34bda69a3c530a653a8df3fc117969e3920c5625791a3cf`** · `kc2-play-upn5-global-magnitude-fold-lift-2026-09-29.md` **`bfa44b4722ec8b7326987042101f32310c986e3fae489a4372fcc4e0dd5553c7`** · `…-ADDENDUM-…` **`5323c1fa9f156e80ced5b1324e4297150cfc759c4e54426f440c33a6c9745fc6`** | ⚑ **Each was committed ALONE before its code existed (D4). `P-5`'s fold settings are not a choice made in this document; they are read out of these** |

**Documents of record, derived here so the next reader need not:**

| document | sha256 |
|---|---|
| ⚑ prereg **v1.6** (superseded by this file, **not edited**) — *v1.7's only predecessor* | ⚑ **`db2c0ca3c6cdba022b83d0229439a3ad9e0709cd25732304ffc979a200be7b0e`** |
| prereg **v1.5** (superseded by v1.6, **not edited**) | `efac4bd51f2d2c1f1130a58c85f37d1c7738e51ac15afd3c70930f7ac3eef143` |
| **the grade of record** — `gamora/notes/2026-09-21-kc2-play-ta-grade.md` | `600f68a7378329c298cd69863903804a6ab7d1ee8a27f666688717f741b9c1c3` |
| ⚑ **the discrimination audit** — `gamora/notes/2026-09-21-kc2-play-discrimination-audit.md` (86 rows; **33 carry weight they cannot bear**) | `852d0bd7d637280cbc42e2ba8494ea7e163b4f6c91741f24eb0ef3da105e674a` |
| divergence register **v0.3** (companion; file form) | `5028b555313df2f4690cd96881c700c7d66a4733612894c150c2448915510444` |
| ⚑ **jack-ryan's v1.6 pre-read** — `qa/findings/2026-09-29-run-KC2-PLAY-w2-prereg-v1.6-preread.md` (carried at § 0.5) | ⚑ **`5a5f45d76098746ce1dbd31d0091b9a7d62f16978fb52a21ff27990181e0b6c0`** |
| divergence register v0.3 (**machine** form, emitter-derived, 28 rows) | `453231e0afefbf101010677bb72e685c43c2fa68666dbac44f118d1e14b07e68` — ⚑ **carried from the grade § 0; a form only the emitter produces, and I do not pretend to derive it** |

### ⚑ SEALED CELLS — **hash-verified this session; K-7 held, never opened for re-execution, never re-run**

| cell | path (`~/Games/reincarnated-engine/src/reincarnated/simulation/output/`) | sha256 **derived** | bytes **verified** |
|---|---|---|---:|
| `[M-POL2]` | `kc2-checkpoint-E-s09-cp150-mpol2-20260825_114420.json` | `ad61ad2a8c799d6ef11a68436756c253f0a34fbb1052e575cdf9f9cd3a44dc5c` | 123,564 |
| `[MECH]` | `kc2-checkpoint-E-s09-cp150-mech-20260816_124031.json` | `20b05cb4ef3bd888b998cbc46c68b41a8051111c12fbcf2066d101b0a4b15f4b` | 2,125,271 |
| `[W1W]` | `kc2-checkpoint-E-s09-cp150-w1walls-20260825_220058.json` | `7a992c81ca6e56e54a53534b438a9ddf87ed42f1bf1a3d0ecc2d2f3c3db7881b` | 403,084 |

> ⚑ **K-7, STATED PRECISELY, BECAUSE v1.6 READS FIGURES OUT OF `[M-POL2]` AND SOMEONE WILL ASK.**
> **K-7 forbids RE-RUNNING a sealed cell. It does not forbid READING its published numbers** —
> v1.5 § F.3a worked from *"the seal's own published per-salt figures"* and reproduced three of
> gamora's statistics from them. **§ A.5's terminal-wave derivation is a READ of `[M-POL2]`'s own
> `⚑ arms.M-POL-2.terminals` array.** No cell was executed, re-executed, edited or moved.

⚑ **v1.7 — Counts at v1.7:** **5 preconditions** · ⚑ **28 EXACT** + ⚑ **1 UNGRADEABLE-declared (`TA-X-06`, Matt `Q83(b)`, KP-110)** · **19 DIAGNOSTIC ids (0 counted, 0 gating — F5)** · 2 emitted-not-graded. *(v1.6: 29 EXACT = 26 carried/re-derived/re-authored + 3 NEW. v1.7 = v1.6's 29 less the one row Matt reclassified — § 0.1.)*
**Standing law:** Law 3 · K-7 · D4 · GL-6 / GL-7 / GL-12 · the Commission Rule · Disciplines **#1 · #12 · #72 · #75 · #78 · #79 · #84 · #85** · `WARN-16` · digests **derived at use, never retyped**.

---

## § A · CHANGE TABLE — v1.5 (2026-09-21) → v1.6 (2026-09-29)

*⚑ v1.7: this section is carried VERBATIM as the v1.5 → v1.6 record. Its rows describe v1.6 and are
true of v1.6; row 11's count (29) and row 13 (`TA-X-06`) are superseded FORWARD by § 0, not edited
here.*

| # | clause | v1.5 | **v1.6** | reason | authority |
|---|---|---|---|---|---|
| 1 | ⚑ **THE SUBSTRATE** | v3.3 pack `…v3p3-20260921_022612`, 8 files pinned | ⚑ **v3.4.2 model pack `5cab7433…` (17 members) + reference pack `978f54ab…` (7), both digests RE-DERIVED BY THE LAW, plus a `P-5` cross-pin gate** | **F2's re-base landed across three cuts (v3.4 · v3.4.1 · v3.4.2).** ⚑ **And § A.1 measures how far it actually moved — which is much less than § H.3 assumed** | **KP-94 · KP-99 · KP-103** |
| 2 | ⚑ **THE GRADED-RUN CAP** | *"v1.5 DOES NOT RESET IT. ONE graded run remains."* | ⚑ **RESET. TWO graded attempts against v1.6.** | ⚑ **Matt, Q85, 2026-09-28: RESET, two attempts.** v1.5 § H.4's four guards are all satisfied: (1) the reset was ruled **from outside the run**; (2) this prereg is committed **alone, before** anything is graded against v3.4.2; (3) the v1.4 and v1.5 attempts **stay on the record** and are named in this header; (4) `substrate_epoch` is declared in every artifact (§ C.7) | **KP-83 (Q85)** |
| 3 | ⚑ **THE SEAL CRITERION** | not stated — v1.5 predated it | ⚑ **STATED ON THE FACE: REFERENT-v1 seals on ALL EXACT rows green + coverage 89/89 mapped + T-B reported DIAGNOSTIC + Matt's T-C yes.** Nothing else seals it, and a diagnostic cannot contribute | **Matt, Q87.** The conductor's *"feel-load-bearing rows"* framing was **circular** and is withdrawn | **KP-83 (Q87)** |
| 4 | ⚑ **`TA-X-25`** | three clauses, **two of them STRUCTURAL NON-ZEROS** resting on *"POOL-466 contains 338 NO-DATA members"* | ⚑ **RE-AUTHORED AS ACCOUNTING IDENTITIES — § F.2f.** Carried forward unchanged it **REDS A CORRECT PORT ON EVERY ARM** | ⚑ **Derived, § A.3: POOL-466's NO-DATA population is `338 → 0`.** v1.5 § H.3 said the row *"cannot be re-derived; it must be re-authored, and the successor may have to assert the opposite sign."* ⚑ **The re-authoring adopts my own recorded recommendation (`OQ-B` of the rebase note): identities, not sign assertions, so the row survives the NEXT substrate move too** | **KP-80** · rebase note § 3 / `OQ-B` |
| 5 | ⚑ **`TA-B-15`** | reference points `0.3828` / `0.6172`, *"a salt reporting ZERO is the anomaly"* | ⚑ **INVERTED. Both reference points are `0.0000`; ZERO IS NOW THE EXPECTATION AND A NON-ZERO IS THE ANOMALY.** DIAGNOSTIC — gates nothing (F5) | same derivation as row 4 | rebase note § 3 |
| 6 | ⚑ **THE ORACLE'S OWN HOLES** | not a named class | ⚑ **A STANDING REPORT-FACE RULE AND A GRADING PROHIBITION — § F.5 cl. 8.** `ABS-NINE-WINNER-SURFACE-HONEST-FAILS` (**13**) · `ABS-GLOBAL-MAGNITUDE-FOLD-INERT-RECORDS` (**29**, of which **0** in the graded window) · `ABS-C-I14-2-SOURCED-UNFOLDED` (**≤ 2.2 % pooled, ×1.000 at w159/160**). ⚑ **NO ROW MAY GRADE A PORT RED ON ANY OF THEM** | ⚑ **Each is the oracle declining to invent supply it could not decode. The pack says so in its own registry, at the cut, *"because after a graded run it reads as an excuse."*** ⚑ **A port that does not implement them is CORRECT** | **KP-97 · KP-99 · KP-102** · pack `provenance.json` absence_registry [47] [49] |
| 7 | ⚑ **THE STARVED CHANNEL** | absent | ⚑ **TWO CLAUSES, BOTH NEGATIVE — § F.5 cl. 9.** The **resume cadence is DECLARED** (`ABS-CHANNEL-STARVED-RESUME-CADENCE`, closer = Matt-to-do **T32**), and the oracle's starvation **TERMINATION** is `UNSOURCED-INCUMBENT`. ⚑ **NO ROW GRADES THE PORT AGAINST THE TERMINATION** | ⚑ **`per_cast_energy.CHANNEL_STARVED_RESUME` grades ITSELF `UNSOURCED-INCUMBENT`: *"the INCUMBENT behaviour of run.py's wave loop, carried unchanged and ratified by nothing."*** **Grading a port against a behaviour nothing ratified is grading the oracle's accident** | **KP-90 · KP-95** |
| 8 | ⚑ **CROSS-EPOCH COMPARISON** | the two-epoch rule was named in § H.1 for the re-base | ⚑ **PROMOTED TO A LAW WITH A NAMED MECHANISM — § C.7. `v3.3` AND `v3.4+` BOARDS ARE NOT DRAW-COMPARABLE AT A FIXED SALT.** No row, no diagnostic and no report line may compare across them | ⚑ **drax G-3, measured both ways: reads are stream-neutral 5/5, and the SUBSTRATE moves the stream 5/5 — because a refusal takes ONE draw, not three.** A fixed salt does not fix the board when the roster changed | **KP-98** |
| 9 | ⚑ **THE HONEST `n`** | § C.2/C.3 already used mean-of-salts, `ddof=1`, `t(0.975, df=4)` | ⚑ **PROMOTED TO A LAW AND EXTENDED TO THE REPORT FACE — § C.8. THE 25 CELLS ARE 5 SALTS × 5 ARMS, AND ON ANY DIMENSION THE ARM DELTAS DO NOT TOUCH, `n = 5`, NOT 25.** Any figure printed over "the 25 cells" prints its **effective n** beside it | ⚑ **legolas F-3/F-4: the "132×" was the exact median of 25 cells that carry FIVE distinct sustain outcomes.** ⚑ **A median over replicates is not a median over samples, and the error is √5 = 2.24× in the wrong direction — the same one-shape defect this run has now found six times** | **KP-86 (F-3/F-4)**, routed to jack-ryan at this pre-read |
| 10 | ⚑ **`P-a`'s WIDTHS** | live, applied, 6 counted + the rest | ⚑ **EVERY WIDTH VOID — § A.4. NOT ONE ROW OF THE TOLERANCE HALF SURVIVES.** The diagnostics keep their **ids, constructions and grain pairs** and print `[width VOID @ re-base]` where a number used to be | ⚑ **v1.5 § H.3, verbatim: *"Every width is derived from the sealed `M-POL-2` cells' per-salt values. New cells ⇒ new per-salt values ⇒ EVERY WIDTH IS VOID."*** **This costs nothing that gates anything, because F5 already removed their authority** | **KP-49 (F5)** · v1.5 § H.3 |
| 11 | ⚑ **THREE NEW EXACT ROWS** | 26 EXACT | ⚑ **29 — `TA-X-28` (the leech target law) · `TA-X-29` (global-magnitude fold conformance) · `TA-X-30` (the pursuit halt)** | ⚑ **Each is a thing the lap learned at a cost and NO EXISTING ROW CATCHES.** `TA-X-28` is the best-sourced line in the fold and a cap would be a fitted constant; `TA-X-29` is the D19 hole, and the pack ships a PREDICATE for it; `TA-X-30` is an 80.5 % divergence that census row M10 read `IMPLEMENTED` through. § F.2g–F.2i | **KP-96 (i)** · **KP-100 / KP-101 / KP-103** · **KP-87 / KP-93** |
| 12 | ⚑ **`P-5` · THE ORACLE FOLD SETTINGS** | `V0`'s limb set only | ⚑ **NEW PRECONDITION. FOUR FOLDS LANDED IN THE ORACLE THIS LAP AND ONE OF THEM IS DEFAULT-OFF. § B.5 SAYS WHICH SETTING T-A RUNS UNDER, FOR EACH, WITH ITS SOURCE** | ⚑ **A default-OFF fold that the graded run must arm is exactly the `P-4` shape one layer in: the instrument never said WHICH CONFIGURATION.** ⚑ **And getting the winner surface wrong is not a small miss — with it OFF the oracle builds the nine from `merged()` while the port builds them from the pack's CRUCIBLE rows, and T-A reds a correct port** | **KP-97** · `winner_surface` MIGRATION § 2 |
| 13 | **`TA-X-06`** | carried AS CLASSED, `Q83(b)` flagged OPEN | ⚑ **CARRIED AS CLASSED AGAIN — AND THE CONFLICT IS NOW LOAD-BEARING FOR THE SEAL. § F.2e** | ⚑ **`Q83(b)` IS STILL OPEN** (`matt_decision_needed/README.md` row `Q83`: *"(b) and (c) REMAIN OPEN"*). Reclassing here would **moot** it. ⚑ **BUT Q87 NOW SAYS THE SEAL NEEDS ALL EXACT ROWS GREEN, AND THIS ROW IS UNFALSIFIABLE IN THE HONEST DIRECTION — so an unruled `Q83(b)` BLOCKS THE SEAL.** Raised at § I OQ-1 as the single highest-priority item, not buried | `Q83(b)` **OPEN** · **Q87** |
| 14 | ⚑ **`TA-X-09`'s SCOPE** | *"all **9** `math_rules.test_vectors`"* | ⚑ **CARRIED AT NINE — AND THE OTHER TWENTY ARE DECLARED, NOT SILENTLY SWEPT IN. Ceiling `C-h`, NEW** | ⚑ **DERIVED: `math_rules.json` carries **29** test vectors across 15 rules, of which **20** sit on `RULE-MONSTER-TO-PLAYER-MITIGATION-ORDER`, `normative: true`, and have been ungraded in every version of this prereg.** ⚑ **Widening the row here would be moving a goalpost with results pending; leaving it silent would be the defect the discrimination audit is about. It is DECLARED** | derived · audit § 0 |
| 15 | **supersession sweep** | run at v1.5 | ⚑ **RUN AND RECORDED — § A.6**, including one correction to v1.5 itself | the standing rule | — |

---

### ⚑ A.1 · HOW FAR THE SUBSTRATE ACTUALLY MOVED — **derived file by file, and it is LESS than v1.5 § H.3 assumed**

**v1.5 § H.3 said: *"the vectors, the pick count, the LIVE quantisation-site list and the arena
supremum are all pack properties. Re-derive each; do not assume a monster-offense lift leaves them
alone — VERIFY it."* ⚑ I verified it. Six of the eight v1.5-pinned files are BYTE-IDENTICAL.**

| v1.5 `P-h` file | v1.5 sha256 | **v3.4.2 sha256 (derived)** | |
|---|---|---|---|
| `waves.json` | `38c43a9c…` | **`38c43a9c3b35560a3dce88ac16c189cb03b120b1ba2085ae2458040113621072`** | ⚑ **IDENTICAL** |
| `monsters.json` | `38393229…` | **`3839322955b7d4af0a6c8c8b169656136a0271a7ab9bb68893a272df703701a0`** | ⚑ **IDENTICAL** |
| `monster_defense.json` | `00ffab15…` | **`00ffab1576577164cc132b498817d5480822df3234f3f3bcf286c0a407193aac`** | ⚑ **IDENTICAL** |
| `arena.json` | `e65b7da0…` | **`e65b7da05e87028136e616ad5f7391ca88cb1ae4db3956fc679c1cf0008f3ba6`** | ⚑ **IDENTICAL** |
| `rng_contract.json` | `ff6f77b0…` | **`ff6f77b0d54037f61847ab7785b58db324a7a0294d666c952b85fc955127a308`** | ⚑ **IDENTICAL** |
| `config_of_record.json` | `d34ce0d8…` | **`d34ce0d8d5546ac7de5ab6ea6b30bc5dfae6460c078643d90c54a9209b78ebc4`** | ⚑ **IDENTICAL** |
| ⚑ `math_rules.json` | `2becfb4f…` | ⚑ **`cc4a9fdb83138fd187f96e2b7f9ce560a401218e21a5bf89035b989d5386015f`** | ⚑ **MOVED — and § A.2 shows the graded content did not** |
| ⚑ `monster_offense.json` | `e1b5072e…` | ⚑ **`c39f4b9eb8e41ca1a6afdbfff17c727dda16b9974d87029656fa35f847812103`** | ⚑ **MOVED — this is the whole re-base** |

**Nine further members are pinned for the first time** (they existed at v3.3 and no version of this
prereg named them): `ai_states.json` `928ded88…` · `controllers.json` `b4217daa…` ·
`meta.json` `b6a14a14…` · `monster_kinematics.json` `e39daa82…` · `player_kit.json` `02819cdd…` ·
`projectiles.json` `ed32ff8a…` · `provenance.json` `0c7e4d2f…` · `summons.json` `6a7cc5af…` ·
`target_selection.json` `e1df3cf6…`. **Full table at § B.5.**

> ⚑ **WHAT THIS BUYS, AND IT IS THE REASON THE ROW-BY-ROW DIFF IS SHORT.** `TA-X-10` (arena
> supremum), `TA-X-16` (the pick count), `TA-X-17` (the 8.0 m offset), `TA-X-18` (the scatter-law
> discriminator) and `TA-X-27(d)` (the degenerate-pair census) are all functions of `arena.json`
> and `waves.json` **alone**, and both files are byte-identical. ⚑ **Their values are CARRIED ON A
> BYTE IDENTITY, NOT ON AN ASSUMPTION — and I re-derived every one of them anyway, because a byte
> identity proves the INPUT did not move and not that my reading of it was right the first time.**

---

### ⚑ A.2 · `math_rules.json` MOVED AND THE NINE VECTORS DID NOT — **derived, rule by rule**

**All 15 rules compare byte-identical between v3.3 and v3.4.2 under a sorted-key JSON diff, and all
29 test vectors with them.** The digest moved because the cut **appended** its annotation blocks —
`⚑ v3p4_rows`, `⚑ v3p4_grain_law`, `⚑ v3p4p1_rows`, `⚑ v3p4p1_grain_law`, `⚑ v3p4p2_rows`
(carrying the `z5` composition law), `⚑ v3p4p2_grain_law`.

| rule_id | `normative` | vectors | graded by `TA-X-09`? |
|---|---|---:|---|
| `RULE-CHANNEL-MOVEMENT` | true | 2 | ✓ |
| `RULE-RELEASE-TYPE-A` | true | 2 | ✓ |
| `RULE-RELEASE-TYPE-B` | true | 1 | ✓ |
| `RULE-CAST-INTERRUPT-BINDING-EXCLUSIVITY` | true | 2 | ✓ |
| `RULE-DMG-APPLIED` | true | 2 | ✓ |
| `RULE-NO-ENERGY-GATED-RELEASE` | false (**prohibition**) | 0 | via `TA-X-14` |
| `RULE-NO-RELEASE-ON-EVERY-CAST` | false (**prohibition**) | 0 | via `TA-X-14` |
| seven `RULE-GD-*` equations | false | 0 | — (documentary) |
| ⚑ `RULE-MONSTER-TO-PLAYER-MITIGATION-ORDER` | ⚑ **true** | ⚑ **20** | ⚑ **NO — ceiling `C-h`** |

> ⚑ **`TA-X-09` HAS ALWAYS GRADED 9 OF 29, AND NO VERSION SAID SO.** The twenty un-graded vectors
> are `normative: true` on the **mitigation order** — the rule that decides how every monster hit
> lands on the player, and therefore the rule under which the whole intake thread (`C-6`, `C-8`,
> `C-I14-2`) is being argued. ⚑ **I am not widening the row.** A prereg written the session before
> a graded run does not grow its own instrument on the author's judgement; that is what `F5` exists
> to prevent, and it is what `C-g` cost the last run. ⚑ **It is declared as ceiling `C-h` and
> routed to § I `OQ-9` as a one-word question, so the next version can widen it deliberately.**

---

### ⚑ A.3 · THE BODY-STATE TABLE OVER `POOL-466` — **derived three ways, and it is why `TA-X-25` is re-authored**

**Derivation, all from `P-h` and `P-k`, no figure transcribed:**
`POOL-466` = the union of `pools.pool_member.member_record` over every `pool_record` referenced by
`pools.wave_spawn` at `global_wave ∈ [151, 160]`. **109 distinct pools ⇒ 466 distinct members.**
`ANCHOR-169` = the 169 distinct `record` values of `pm2_tg2_monster_timing.csv` (`P-k`).
`BOTH-128 = ANCHOR-169 ∩ POOL-466` = **128**. ⚑ **All four cardinalities reproduce exactly.**

| state over `POOL-466` | **v3.3 (derived)** | **v3.4.2 (derived)** |
|---|---:|---:|
| **MEASURED-OFFENSE** | **122** | ⚑ **464** |
| **MEASURED-INERT** | **6** | ⚑ **2** |
| ⚑ **NO-DATA** | ⚑ **338** | ⚑ **0** |
| | 466 ✓ | 466 ✓ |

**How the 464 is built, so nobody has to take it on trust.** A `POOL-466` member is **armed** at
v3.4.2 iff it appears in any of `⚑ v3p3_rows.v20_monster_attack_slot` (**122** members),
`⚑ v3p4_rows.w45_monster_offense_state` (**342**, every one `body_state_after_v3p4 =
MEASURED-OFFENSE`), `w40_monster_attack_slot_upstream`, `w41_monster_granted_tree_skill`, or
`w44_default_weapon_attack` (**4**, the engine-default weapon-attack class). ⚑ **The union is 464.
122 + 342 = 464 exactly: the two populations are disjoint, which is itself the check that the
roster-basis rebase armed the NO-DATA set and not a re-slice of the already-armed one.**

⚑ **THE RESIDUE IS TWO RECORDS AND THEY WERE PREDICTED BY NAME.** The rebase note (`P-e`) § 5 said
*"MEASURED-INERT → 0 — **if the default-attack path lands; § 5 says it may be 2**"*, and its
table B named them: **`records/creatures/enemies/basilisk_a01.dbr` and
`records/creatures/enemies/yetidire_a01.dbr`** — class **B · CONSTRUCTION DROP**, a named
upstream skill (`special1 :: Skill_AttackWeaponCharge`) our constructor discards. ⚑ **Measured on
the shipped pack: exactly those two, and no others.** The prediction and the cut agree by name.

> ⚑ **AND THAT IS WHY `TA-X-25` CANNOT BE CARRIED.** Its clause (c) is a **STRUCTURAL NON-ZERO**
> admitted to the EXACT class by § F.1's test — *"name the mechanism that makes the other value
> impossible"* — and the mechanism it named was *"`POOL-466` contains 338 NO-DATA members."*
> ⚑ **That population is now empty, so the row is not merely failing: it is FALSE, and a correct
> port reds on it on every arm.** Clause (b)'s `n_measured_inert_spawn > 0` survives only as
> *"2 of 466 records might roll"* — which is exactly the *"it would be very unlikely"* that § F.1
> says **is a diagnostic and does not belong in EXACT**.
>
> ⚑ **THE DISCIPLINE-LEVEL FINDING, RAISED AS ONE (rebase note § 3, carried here):** a
> STRUCTURAL-NON-ZERO row is a row pinned to a **substrate fact**, and `TA-X-25`'s fact was *a
> property of our decode's completeness, not of the port*. **§ F.1's admission test asks *can you
> name the mechanism?* — it should also ask *CAN THE MECHANISM BE REPAIRED?*, and if so the row
> carries an EXPIRY.** § F.1 at v1.6 adds that clause.

---

### ⚑ A.4 · EVERY WIDTH IN `P-a` IS VOID — **and the honest accounting of what that costs**

`P-a`'s widths are all derived from the sealed `M-POL-2` cell's per-salt values. **The graded run
happens on a board built from a different `monster_offense.json`, against a port that now applies a
global-magnitude fold and halts at 2.4 m. New per-salt values ⇒ every width void.** Nothing in this
document adjusts a width; **it voids them and leaves the slots named and empty.**

**What that costs: NOTHING THAT GATES ANYTHING.** Under F5 no diagnostic could gate anything
already. **What it costs in signal is real and is declared:** the localising power `TA-B-09`'s
+32.5 half-widths gave the last run — *"a genuine motion defect sits underneath the confound"* — is
not available at v1.6 until a new addendum mints widths from a new sealed set. ⚑ **A diagnostic
without a width still prints its VALUE, its GRAIN PAIR and its DILUTION FACTOR, and those three
fields did most of the work last time.** The number it cannot print is the half-width.

⚑ **AND THE SLOTS THAT WERE ALREADY OWED STAY OWED, NOT QUIETLY CLOSED:** `TA-B-16…19`'s widths
(and `P-a` Addendum 4 § A4.4's finding that **`TA-B-16` must split into `16a`/`16b`** before a width
over it is honest) · `TA-B-06`'s corrected port-side comparison · `P-e′` Addendum § 3's coverage
fractions — **which § A.3 now answers at the member grain (`1.0000`) and leaves owed at the body
grain.**

---

### ⚑ A.5 · THE TERMINAL-WAVE ROW — **what it now expects, and why that is SUBSTRATE-DERIVED**

**Two independent routes, and they agree exactly.**

**Route 1 — read straight out of the sealed cell.** `[M-POL2]` `⚑ arms.M-POL-2.terminals`:

| arm | terminals (per salt) | `terminal_reason` |
|---|---|---|
| `M0` | `[155, 152, 155, 151, 152]` | `player_death` |
| ⚑ **`M-POL-2`** | ⚑ **`[156, 152, 151, 151, 156]`** | ⚑ **`player_death`, every cell** |
| `M-POL-2-NULL` | `[155, 152, 155, 151, 152]` | `player_death` — ⚑ **identical to `M0`, which is `TA-X-03`'s relation showing up at the terminal grain** |
| `M-POL` (the G5 control) | `[151, 151, 151, 151, 151]` | `player_death` |

**Route 2 — U-P-N-4's harness** (`P-l`, `…upn4-occupancy-by-pilot-20260929.json`), cell
`SEALED-KMILL | SEP-ON`, `LEG_A_first_death_waves` = **`[151, 151, 152, 156, 156]`**.

> ⚑ **THE SAME MULTISET. `{151, 151, 152, 156, 156}` both ways.** And across all **15**
> pilot × separation cells the first-death waves span **151–156**, with exactly one cell
> (`CAMP_THEN_COLLECT* | SEP-BLOCK`) reaching the tick cap with no death.

**What `TA-B-01` expects at v1.6, therefore:**

* **Oracle side, `M-POL-2`:** `terminal_wave = [156, 152, 151, 151, 156]`, `terminal_reason =
  player_death` **5/5**. ⚑ **This is READ, not chosen** — it is the seal's own array, and the
  U-P-N-4 harness reproduces it from a different direction.
* **Port side:** run #1 gave `[160 × 5]`, `terminal_reason = cleared`, HP never below 79.44 %.
  ⚑ **v1.5 said *"`[160 × 5]` is not four waves past the band, it is THE LADDER RUNNING OUT."*
  That reading is now SHARPER AND WORSE: the port is 4–9 waves past the point at which the oracle's
  own sealed cell KILLS THE PLAYER, on every salt.**
* ⚑ **THE ROW STAYS DIAGNOSTIC AND NON-DISCRIMINATING (CLASS V), AND THAT IS NOT A CONTRADICTION.**
  A terminal wave cannot *grade* fidelity — its band admits the `M-POL` control the run built to be
  different. **What changes is its printed reference point**, from *"the ladder ran out"* to
  ⚑ ***"the oracle dies at 151–156; a port that clears to 160 has not survived a hard board, it has
  failed to be in one."*** **That sentence is mandatory on the face (§ F.5 cl. 10).**

⚑ **AND THE CORRIGENDUM THIS RETIRES, STATED BECAUSE IT WAS MINE.** KP-95 recorded *"the heal
surplus is a MODEL gap against the referent… Matt's T-C would answer NO"*, and KP-96 routed it to
the pilot. **Both rested on U-P-N-3's BARE stack — no pilot argument, no offense, sustain, intake,
pursuit or kinematics armed — which I relayed as the oracle's behaviour without opening what it had
armed.** ⚑ **The oracle is not unkillable. It is OVER-lethal.** `[M-POL2]`'s own `terminals` array
said so before the lap started, and nobody read it.

---

### ⚑ A.6 · SUPERSESSION SWEEP — run against the documents and the substrate, not against recollection

| stale figure hunted | found live-tense? | disposition |
|---|---|---|
| ⚑ **`0.266406` as *"mean over the ARMED records"*** | ⚑ **LIVE IN v1.5 § F.2a clause (e)**, which reads *"over the armed records of `POOL-466`"* | ⚑ **THE NUMBER IS RIGHT AND ITS POPULATION LABEL IS WRONG — MY OWN, AND I FOUND IT BY RE-DERIVING RATHER THAN CARRYING.** Derived: over **`BOTH-128`** the column gives **`0.266406`, 5 zeros — reproduces EXACTLY.** Over the **actually-armed 122** (`v20 ∩ POOL-466`) it gives **`0.262295`, 5 zeros.** Over **all 790**, **`0.252215`, 48 zeros.** ⚑ **`BOTH-128` is a DECODE-COVERAGE population, not an ARMED one.** ⚑ **Sixth instance in this run of one shape — the arithmetic correct, the POPULATION it ranged over the defect — and v1.5 named the fifth instance on this very clause while mislabelling it. Clause (e) at v1.6 states its population as a SET EXPRESSION** |
| **`338` NO-DATA in `POOL-466`** | live in v1.5 § F.2b, § E.1 trap 6, `TA-B-15` | ⚑ **SUPERSEDED — `0` (§ A.3).** `TA-X-25` re-authored; `TA-B-15`'s reference points → `0.0000` |
| **`9 of 9` records diverge on the winner surface** | ⚑ **live in KP-95, which is MINE** | ⚑ **CORRECTED AT KP-97 AND CARRIED HERE: IT IS ONE SLOT** — `korvaakmessenger_02b :: special5` (`messenger_02_impale`). `ThreatProfile.slots` is a union of three differently-sourced populations and `x8` enumerates one; my step-2 instrument differenced three vocabularies as one set. **KP-95's step-1 materiality finding measured SPAWNS, not surfaces, and STANDS** |
| **`5.62` bodies-in-disc / `~72.5` heal:intake as *the oracle's behaviour*** | live in KP-95 and KP-96 | ⚑ **SUPERSEDED BY KP-100 — it was the BARE stack with nothing armed.** The **sealed** stack, pooled 151–159, gives `N` **1.43–2.30** across pilots. `NEAREST_SEEK`'s 1.43 is **inside** the referent's `[0.72, 1.84]` |
| **the cluster-seeking pilot as the occupancy mechanism** (legolas C-8 § 5.4; my own KP-96 ruling (ii)) | live in C-8 and KP-96 | ⚑ **REFUTED BY MEASUREMENT: a player who NEVER MOVES (`CAMP`) reaches `5.617`, the same number.** The gap is not PILOT class |
| **`183.58`** — the withdrawn analytic `E[bodies]` | ⚑ **not live in v1.5**; the corrected `137.58` / `126.08` are carried | ⚑ **`126.08` (p06 OFF, the config of record) is CONFIRMED UNCHANGED at v3.4.2**, because it is a function of `waves.json` and `waves.json` is byte-identical (§ A.1) |
| **coverage `72`** and KP-26's `229 / 297 / 302` | ⚑ **STILL LIVE IN THE CHARTER** (§ 4.3 / § 4.4 / § 3 F1 / § 9) and in `kc2rt_coverage.gd`'s **constant NAME** `CHARTER_DENOMINATOR` (value 89, verified at godot `d9ed2ef`) | ⚑ **`OQ-7` / `OQ-3` STILL OWED, third version running.** **The prereg and the register were never the carriers; the charter is, and still is.** The rename is a propagation, not a ruling |
| **`C-c`** (the `limitN` residual ceiling) | struck void at v1.5 | ⚑ **STAYS STRUCK; `OQ-6` (the un-measured `limitN` question) is re-opened at § I, and the re-base has now happened, so it is cheap** |

---

## § B · CONFIGURATION AND PRECONDITIONS — **five**

### B.1 · `ORACLE` — `V0`, five arms, five salts *(restated; v1.5 is superseded and a grader must not hold two files open)*

`V0` carries five `V0-ARM-*` rows — `M0`, `M-POL-2`, `M-POL-2-NULL`, `W1`, `W1-NULL` — each a
**DELTA against the base row set, never a second full copy**. **5 arms × 5 salts = 25 headless
runs**, each arm the base set with **exactly one fold moved**. That single-fold delta is the entire
reason the inertness relations are readable, and it is why `W1-NULL` returns to **`M-POL-2`** and
not to `M0` (`TA-X-04`). ⚑ **It is also why § C.8 exists: single-fold deltas mean most statistics
have FIVE independent observations, not twenty-five.**

Limbs of record: `spawn_fold: POLAR_UNIFORM_RHO` · `sustain: COUPLED` · `intake: ARMOUR_THEN_RESIST
+ global_flat` · `summons: PRESENT_INERT + offense MEASURED_BASIC` · `arena_fold: None` (armed only
in `W1`) · `interrupts_fold: None` · `WarCryLimb.COOLDOWN` (7.5 s) · `PotionLimb.TRACE_CONSISTENT`
(θ 0.22972972972972974) · `CritLimb: LO` · **`p06: OFF`** · `PhaseModel: ENGAGE`.

**The runtime prints its RESOLVED limb set into the verdict header (`v0_limb_set`), diffed
line-by-line against `V0` before any row is read; it refuses to boot on an unset limb rather than
defaulting one.** ⚑ **AND THAT IS NOT SUFFICIENT ON ITS OWN — `TA-X-26` and now `TA-X-29` exist
because a header diff cannot catch a declared limb or a declared FOLD with no implementation:
THE HEADER IS WHERE THE CLAIM IS MADE.**

**Pilot:** scripted — `DRIVE_TO_PACK` + the M-POL-2 channel policy; `v_ref = 4.0` is a
DECLARED-FREE-PARAMETER → 5.4 m/s; **no facing model**. The pilot's MOTION LAW is `V0-04` —
*"drive-THROUGH with rolling re-target; the step is never clamped at the target"* — declared on the
wire. ⚑ **The BODY halt is a different law and it is now graded: `TA-X-30`.**

**Declared fight scope: waves 151–160.**

### B.2 · `P-1` · COVERAGE — **89 / 89**

All **89 enumerated census row ids** mapped **mechanically** to exactly one of `IMPLEMENTED` ·
`DIVERGENCE(DIV-nn)` · `RUNTIME-CHOICE(absent_ref)` · `OUT-OF-SCOPE`. **Counts sum to 89. Zero
unmapped.** Graded as `TA-X-02`. ⚑ **Q87 names 89/89 MAPPED as a seal condition, so this
precondition is now load-bearing twice.**

**Carried unchanged from v1.5, and still not closed by re-declaring them:**
1. **`P-1` gates COMPLETENESS, not TRUTH, and at least one mapping was false** — census `M4`,
   mapped `IMPLEMENTED` with a note describing an implementation that did not exist.
   ⚑ **AND THE LAP PRODUCED A SECOND AND A THIRD:** **`M10`** read `IMPLEMENTED` for a reason true
   of the wrong consumer (KP-87/93), and **`D16`** read `IMPLEMENTED` while its multiplier sat at
   ×1.000 — an ~11× DoT over-read (KP-98). **The mapping is a claim.**
2. **`P-1` REQUIRES the refusal count to be emitted**, so a `RUNTIME-CHOICE(absent_ref)` mapping
   cannot hide behind the gate's missing cell.
3. **`P-1` cl. 1a:** **every `IMPLEMENTED` mapping whose census row is ALSO graded by an EXACT row
   must name that row id in its note.** ⚑ **M10 and D16 are the argument for this clause: both were
   caught by a human reading source, and cl. 1a is what makes the cross-reference catch them.**
4. ⚑ **THE FOUR-WAY COUNTS MOVE AT v1.6 AND THE TOTAL DOES NOT.** **D19** flips
   `RUNTIME-CHOICE(ABS-GLOBAL-MAGNITUDE-FOLD)` → carried, once drax's W2f lands (`PRED-GMAG-WHOLE`
   decides it, not a self-report). **M10** is corrected. **D16** is re-classed.
   ⚑ **A grader must read the COUNTS off the run, never off this document.**
5. `kc2rt_coverage.gd` still holds a constant **named** `CHARTER_DENOMINATOR` (value 89, verified
   this session). **`OQ-3`'s point was the NAME.** Rename owed, third version running.

### B.3 · `P-2` · STREAM DISJOINTNESS

**Probe:** run `M-POL-2` salt 0 twice, once with a **no-op fold inserted that draws zero values**;
assert identical digests. **COVERS** stream isolation at *fold* granularity.

⚑ **DOES NOT COVER:** (1) that the port's draw sites are the **same sites in the same order**;
(2) the **BOARD ROLL's composition** (trap 6); (3) whether the per-site assignment is *lifted* or
*chosen*. `TA-X-27` covers the **degenerate-draw consumption** class at the two `randint` sites.
**The rest of (1) and all of (2) stand open.**

⚑ **AND `P-2` NOW CARRIES THE EPOCH LAW ON ITS FACE (§ C.7).** drax's G-3 measured that a
**substrate change moves the stream 5/5**, because a refusal takes one draw and not three.
⚑ **`P-2` is a WITHIN-EPOCH probe. It says nothing across a pack revision, and no report may read
it as though it did.**

**`P-2` red → `TA-X-03…05` UNGRADEABLE → `INDETERMINATE` → the cap trips.** *(⚑ v1.7: `TA-X-06` is
UNGRADEABLE-declared regardless of `P-2`, and enters no antecedent — § F.2e.)*

### B.4 · `P-3` · ROLL POPULATION AND ROLL LAW

**RULED (KP-32): T-A rolls from `POOL-466`, as the oracle rolls. `ANCHOR-169` is not forced and it
is NOT AVAILABLE.** ⚑ **All four cardinalities RE-DERIVED at v1.6 (§ A.3), and all four hold:**

| id | n | re-derived from | the rule |
|---|---:|---|---|
| **ROSTER-790** | **790** | `P-i`'s `record` column (790 distinct) | every `record_path` in `monsters.json::blocks` carrying a `wave`; **+1 declared-absence key** (`krieg_aethertrap`) ⇒ 791 distinct keys. **GL-12: a declared null is NOT-MODELLED, never a measured zero** |
| **POOL-466** | **466** | `P-h`'s `waves.json` — 109 pools over waves 151–160 | ⚑ **THIS IS WHAT `L-49` HAS THE RUNTIME ROLL FROM** |
| **ANCHOR-169** | **169** | ⚑ **`P-k`, pinned for the first time** | the threat DECODE's coverage |
| **BOTH-128** | **128** | `ANCHOR-169 ∩ POOL-466` | ⚑ **the population `TA-X-26(e)`'s v1.5 figure actually ranged over (§ A.6)** |

**THE ROLL LAW — two stages, and only one is weighted:** **WEIGHTED** by `pool_weight` at the
pool-alternative stage (`wave_engine.py:974 _weighted_pick`); ⚑ **UNIFORM** at the name stage
(`:849, :869 rng.randrange(len(roster_names))`). **The port implements the ORACLE's law, not the
referent's.** A port that weights the name draw is wrong, and wrong in a direction no diagnostic
localises.

⚑ **`ANCHOR-169` AND `BOTH-128` ARE DECODE-COVERAGE FIGURES AND THEY DID NOT MOVE — because the
timing CSV did not.** ⚑ **What moved is what they were used to EXPLAIN: `ANCHOR-169` is no longer
the armed set (§ A.3). Carrying `BOTH-128` forward as *"the armed records"* is precisely the
mislabel § A.6 corrects.**

`roll_population` / `roll_law` are declared in the header and diffed at boot. **`P-3` red →
`INDETERMINATE`.** ⚑ **A declaration is self-reported; `TA-X-25` is no longer the behavioural
check it was, and § F.2f says what replaced it.**

### B.5 · ⚑ `P-4` · **PACK IDENTITY — BOTH PACKS, AND THE CROSS-PIN**

**The runtime declares the model pack AND the reference pack it consumed, hash-verifies every
member before any row is read, and verifies the reference pack's `cross_pin` against the model
pack's digest:**

```
model_pack_dir      : "kc2-model-pack-v3-E-s09-cp150-mech-v3p4p2-20260929_063506"
model_pack_digest   : 5cab743335c6a721f57680e151d6e949d3387ca164342ffc97fefd04916835e2   (17 members)
reference_pack_dir  : "kc2-reference-pack-v3-E-s09-cp150-mech-v3p4p2-20260929_063506"
reference_pack_digest: 978f54ab275de4f932fd8a7116b3fd44646268ee2b625fcae5516e81ab77b7de  (7 members)
cross_pin_verified  : reference.manifest.cross_pin.model_pack_digest == model_pack_digest
```

| # | `model/` member | sha256 (derived) | bytes |
|---|---|---|---:|
| 1 | `ai_states.json` | `928ded88e74e636422cbc107bdb02ff4cf27521dc74636e5e7e0e1680bd6060e` | 2,497 |
| 2 | `arena.json` | `e65b7da05e87028136e616ad5f7391ca88cb1ae4db3956fc679c1cf0008f3ba6` | 12,932 |
| 3 | `config_of_record.json` | `d34ce0d8d5546ac7de5ab6ea6b30bc5dfae6460c078643d90c54a9209b78ebc4` | 26,909 |
| 4 | `controllers.json` | `b4217daac06f2f55acb3ec68571dd7766d31ac156ee01ee903b721f26042e478` | 5,384,891 |
| 5 | ⚑ `math_rules.json` | `cc4a9fdb83138fd187f96e2b7f9ce560a401218e21a5bf89035b989d5386015f` | 153,607 |
| 6 | `meta.json` | `b6a14a14d8daac740497f57fcd24fc5ba238fdece3e95a6a4642baf06b4b5961` | 45,098 |
| 7 | `monster_defense.json` | `00ffab1576577164cc132b498817d5480822df3234f3f3bcf286c0a407193aac` | 8,816,113 |
| 8 | `monster_kinematics.json` | `e39daa82ce129cb3f11ea1716f46ac8a18dfa0561de840d973a9667071bf260b` | 464,402 |
| 9 | ⚑ `monster_offense.json` | `c39f4b9eb8e41ca1a6afdbfff17c727dda16b9974d87029656fa35f847812103` | 10,923,543 |
| 10 | `monsters.json` | `3839322955b7d4af0a6c8c8b169656136a0271a7ab9bb68893a272df703701a0` | 15,211,150 |
| 11 | `player_kit.json` | `02819cdd1ab6abcc2cd39478679642996d670bc1f5c32d638847c4d5108a95b6` | 100,481 |
| 12 | `projectiles.json` | `ed32ff8a648d2b3c24918cd20150f27856b371e2a45a0e699cc1c8b6c949a0e5` | 74,198 |
| 13 | `provenance.json` | `0c7e4d2f132e05f13f0e990f46677b5c2713e0258b8d127abf5a035eb527d0b9` | 309,772 |
| 14 | `rng_contract.json` | `ff6f77b0d54037f61847ab7785b58db324a7a0294d666c952b85fc955127a308` | 31,824 |
| 15 | `summons.json` | `6a7cc5af2bd7291b46c1beafedf2e13b70990a3f9a1a194f2092c1a64e586a93` | 111,259 |
| 16 | `target_selection.json` | `e1df3cf69d2f3f91cce5ab5f9a71de4b7be4fb2372d18de2cc99517d399d68ce` | 31,936 |
| 17 | `waves.json` | `38c43a9c3b35560a3dce88ac16c189cb03b120b1ba2085ae2458040113621072` | 1,087,499 |

**reference pack (7):** `acceptance.json` `f5ce2c17…` · `actors.json` `ef03536f…` ·
`meta.json` `0c23b30c…` · `rng_tape.json` `607bf3bf…` · `skill_interrupt_reference.json`
`45522df2…` · `tracks.json` `bb349521…` · `u7_heading_conditioning.json` `5ad6ab0f…`.

⚑ **Every digest above was derived this session, and the two PACK digests were RE-COMPUTED from the
member list by the manifest's own `pack_digest_law_exact` rather than read off the manifest.**
A mismatch on any of them is **`C1`** and the cap trips — the cap's `C1` already reads *"any pinned
sha mismatched"*, so no new condition is added.

> ⚑ **THE ONE THING A GRADER MUST CHECK FIRST, BECAUSE IT IS ALREADY WRONG AT THE TIME OF WRITING.**
> drax's `.app` header at W2b reports `pack_digest = c8ab8952…` — **the v3.4 pack**. At W2d it moved
> to v3.4.1. ⚑ **The graded run must read `5cab7433…`, and `P-4` is red until it does.** This is not
> a criticism: **W2f is the scheduled piece that moves it, and it has not run yet.** It is written
> here so that a green `P-4` means something.

### B.6 · ⚑ `P-5` · **THE ORACLE FOLD SETTINGS — NEW, AND IT SAYS WHICH SETTING T-A RUNS UNDER**

**Four folds landed in the oracle during this lap. One of them is DEFAULT-OFF. The graded run
declares all four in its header and the loader refuses to boot on an unset one.**

| fold | site | **default** | ⚑ **THE SETTING T-A RUNS UNDER** | source |
|---|---|---|---|---|
| ⚑ **the nine on the CRUCIBLE winner surface** | `threat.load_profiles(winner_surface=…)` · `kc2/winner_surface.py` | ⚑ **`None` — OFF, and `winner_surface=None` is the incumbent BYTE FOR BYTE** (`G-W4`: both rosters, both pet dicts, the whole `LoadReport`) | ⚑ **ON. `winner_surface = WinnerSurfaceFold.from_x8(…)`, ARMED.** | ⚑ **`winner_surface` MIGRATION § 2, verbatim: *"the v1.6 reference is re-derived FORWARD with the fold ON — a SIBLING, not a re-grade"* (`x9`'s `SIBLING_NOT_REGRADE`).** ⚑ **AND THE MECHANICAL REASON, which is the one that matters: the PORT reads the nine from the v3.4.1 pack's `y1`/`y2` rows, which ARE the CRUCIBLE winner surface. With the fold OFF the oracle builds them from `merged()` — the CAMPAIGN surface — and T-A would grade a correct port against a reference the cut deliberately replaced.** `KP-97` |
| **C-2 · per-cast energy cost** | `kc2/per_cast_energy.py` · `CostColumn` | **no default — `CostColumn` is a TYPE and forces the consumer to NAME its claim** | ⚑ **`CostColumn.PARENT_PLUS_MODIFIER` — `43.20 / 27.90 / 106.20 / 59.40`.** ⚑ **NOT a free choice: Matt's L1 names those four values, and drax's port consumes the column `charge_PARENT_PLUS_MODIFIER`. Grading two sides on two columns would be the `n_window`/`n_windows` defect in a new costume** | **KP-84 (L1)** · **KP-89** · **KP-98** |
| **C-7 · insufficient energy** | `per_cast_energy.refuses_activation`, one predicate at all three sites | ⚑ **`InsufficientEnergyPolicy.REFUSE` — the default FLIPPED from RAISE to REFUSE, and that is a SEMANTIC SHIFT, not a bug fix (#12)** | ⚑ **REFUSE (the default). `regen_ungated = true`.** `CLAMP` is refuted and retained only as a negative control | **KP-90 · KP-95** · `P-l`'s C-7 note |
| **the global-magnitude fold** | `run.py:1661 / :1690-1691` · consumed at `threat.py:1826-1836`, the ONLY site | ⚑ **the ORACLE ARMS IT UNCONDITIONALLY AND LIVE** — there is no off switch on the reference path | ⚑ **ON, unconditionally. And `run.py:1690-1691` attaches `monster_measured_board` as `.board`, so the ATTRIBUTE LIMB REACHES 344/344, NOT I-14's 23/344** | **KP-100 · KP-101** |

> ⚑ **WHY THIS IS A PRECONDITION AND NOT A FOOTNOTE.** `P-4` exists because *"the instrument never
> said WHICH PACK."* ⚑ **`P-5` exists because the instrument never said WHICH CONFIGURATION — and a
> default-OFF fold is the sharper version of the same hazard, because the pack pin catches a wrong
> pack and NOTHING catches a fold left at its default.** The winner-surface fold is inert by
> construction when off: no dict is consulted, no counter increments, no draw is consumed,
> `simulate_wave` produces identical bytes. ⚑ **Its inertness is exactly what makes forgetting it
> invisible.**
>
> ⚑ **AND THE HONEST LIMIT ON THE PILOT AXIS, STATED HERE BECAUSE U-P-N-4 MADE IT MEASURABLE:**
> T-A compares port and oracle **under the same scripted pilot**, so the occupancy question
> (`N` 1.43–2.30 across pilots) **does not reach T-A at all.** It reaches **T-C**, where the
> occupancy is Matt's own hand. **A green T-A says nothing about it, and § F.5 cl. 10 prints that.**

---

## § C · THE DENOMINATOR LAW · THE GRAIN LAW · ⚑ **THE EPOCH LAW** · ⚑ **THE HONEST-`n` LAW**

```
D_constructed = CHANNELLING + CHANNELLING_AND_MOVING + MOVING + IDLE      (PRE_FIGHT and DEAD excluded)
```
⚑ **Verified this session by reading `[M-POL2]`'s own pooled census: `287 + 2211 + 166 + 119 =
2783 = D_constructed`, which the cell publishes as `⚑ D_constructed: 2783`.** The per-salt sum
equals the pooled sum, so the partition is exact at both grains. ⚑ **No sealed artifact carries
`D` as a field. It is CONSTRUCTED, and the identity is the check.**

**Two identities, 5/5 on the seal, graded as `TA-X-08`:** `n_player_ticks_observed = D + PRE_FIGHT` ·
`n_channelling + n_released = D` ⇒ `uptime + n_released/D = 1.000000` exactly.
⚑ **The seal publishes `release_duty` on `D + PRE_FIGHT`** — the **0.215-vs-0.217 tell** resolves
entirely to a denominator difference. **Every per-tick rate divides by `D` and by nothing else.**

**C.2 · Pooled vs mean-of-salts.** Every diagnostic is on the **MEAN-OF-SALTS**; a port's pooled
figure is never compared against these. ⚑ **The hazard is live in the seal itself and I re-read it:
`[M-POL2]`'s published POOLED `uptime` is `0.897593` and the MEAN-OF-SALTS is `0.879189`. Two
numbers, one name, one file.** `D` per salt is **[1084, 305, 106, 185, 1103]** — a **10.4× span.**

**C.3 · The compared object** is the **mean of a NEW 5-salt run**; the interval is a **prediction
interval** carrying both runs' sampling error; `ddof = 1`; `half-width = t(0.975, df=4) · s ·
√(2/5) = 1.755978 · s`. ⚑ **ALL WIDTHS ARE VOID AT v1.6 (§ A.4). The CONSTRUCTION stands; no number
does.**

**C.4 · T-B denominators are NOT these** (`P-b`). HP occupancy on `LIVE-MAX` reproduces 42.84 %;
NOMINAL gives 39.76 % — **3.08 pp with no fight in it.** HP window 181.0 s; energy / motion /
release / cast 182.65 s. ⚑ **T-B is DIAGNOSTIC (F5) and is one of Q87's four seal conditions as a
REPORTED diagnostic, never as a gate.**

**C.5 · A THIRD DENOMINATOR CLASS — BODIES.** `TA-B-15` and the per-wave coverage lines divide by
**BODIES** and cluster by **POOL PICKS** — populations with no relationship to `D` or to the T-B
windows. **Never pool them, never compare them, and never print a body-fraction under a heading
that has been printing tick-fractions.**

### C.6 · **THE GRAIN LAW** *(carried verbatim; it is this run's discipline)*

> ⚑ **BEFORE BANDING A RATE, NAME ITS NUMERATOR'S GRAIN AND ITS DENOMINATOR'S GRAIN SEPARATELY, AND
> STATE THE RANGE OF THE RATIO BETWEEN THEM OVER WHICH THE BAND WAS CALIBRATED.**

**The mechanical test:** *a fraction is confounded iff its numerator and its denominator scale with
**different** quantities.* `per-wave / per-tick` → **diluted by ticks-per-wave**. `per-wave /
per-wave` and `per-tick / per-tick` → **immune**. ⚑ **A FOURTH GRAIN EXISTS — ABSOLUTE TIME** (a
5.0-second window is neither per-wave nor per-tick, and its coverage of a wave dilutes). ⚑ **And
the clause that keeps this from repeating in a new costume: `TA-B-16…19` are SCALE-FREE BY
CONSTRUCTION, NOT BY MEASUREMENT. Where dispersion and mechanism disagree, MECHANISM WINS, and the
reason is printed.**

### ⚑ C.7 · **THE EPOCH LAW — NEW, AND IT IS A PROHIBITION**

> ⚑ **A `v3.3` BOARD AND A `v3.4+` BOARD ARE NOT DRAW-COMPARABLE AT A FIXED SALT. NO ROW, NO
> DIAGNOSTIC AND NO REPORT LINE MAY COMPARE ACROSS THEM.**

**The mechanism, measured by drax at G-3 and not inferred:** the port's reads off the pack are
**stream-neutral 5/5** — and **the SUBSTRATE moves the stream 5/5**, because **a refusal takes ONE
draw, not three.** A different roster reaches a different point in the tape at a different tick.
⚑ **A fixed salt fixes the SEED. It does not fix the BOARD.**

**What this forbids, concretely and by name:**
1. **Carrying any v1.4/v1.5-era DIGEST forward as a constant.** `TA-X-03`/`04`/`05`/`06` are
   invariant **in form** — port-to-port at one substrate — **and every digest they compare moves.**
2. **Comparing any v3.4.2 figure to a v3.3 figure as though the difference were a port change.**
   The measured `heal:intake` walk (`24.1 → 14.1 → …`) is a walk across **three** substrates and
   two port repairs; it is a narrative, not a delta.
3. **Reading `P-2` across a pack revision** (§ B.3).
4. **Pooling v1.4's graded cells with v1.6's.** The v1.4 and v1.5 attempts stay on the record as
   attempts against the **v3.3** reference and are named in this header; they are **not** priors.

**Every artifact that crosses the boundary declares `substrate_epoch` in its header**, so the rule
is mechanical rather than remembered. ⚑ **`substrate_epoch = "v3.4.2 / pack 5cab7433…"` for
everything graded under this document.**

### ⚑ C.8 · **THE HONEST-`n` LAW — NEW**

> ⚑ **THE 25 CELLS ARE 5 SALTS × 5 ARMS, AND THE ARMS ARE SINGLE-FOLD DELTAS. ON ANY DIMENSION THE
> MOVED FOLD DOES NOT TOUCH, THE 25 CELLS CARRY FIVE DISTINCT OUTCOMES, AND THE EFFECTIVE `n` IS
> `5`.**

**Occasioned by legolas F-3/F-4 (KP-86):** the *"132×"* heal surplus was published as *"the exact
median of the 25 T-A cells."* ⚑ **It is the median of five distinct sustain outcomes replicated
across five arms.** `M-POL-2-NULL ≡ M0` and `W1-NULL ≡ M-POL-2` are **asserted by `TA-X-03` and
`TA-X-04` as EXACT identities** — so on any statistic those two arms cannot move, the prereg's own
rows prove the replication.

**What the law requires, mechanically:**
1. **Every aggregate printed over more than one cell prints its EFFECTIVE `n` beside it**, and the
   effective `n` is the number of cells that could have differed on that statistic, **not the cell
   count**.
2. **`ddof = 1` on the mean-of-salts, `df = 4`** — which § C.3 already does. ⚑ **The defect was
   never in the band arithmetic. It was in the PROSE beside it.**
3. ⚑ **A statistic with `n = 5` never gets a `√25` claim.** The inflation is `√5 = 2.236×` and it
   runs in the direction that makes a finding look stronger than it is — which is why it survived.

⚑ **AND THE COMPANION CLAUSE, from `P-a` Addendum 4 and the discrimination audit:** the draws are
also **CLUSTERED** — median **3 bodies per pool-alternative pick, max 9** — so a body-level `n` is
inflated over a pick-level one by the design effect. **Run #1's per-wave table had 4–6 picks on
every wave: no per-wave figure rested on more than six independent draws.**

---

## § D · ROW-ID CONCORDANCE — the single namespace

⚑ **Every citation uses the `TA-` id; a construction is looked up by STATISTIC NAME, never by a
bare `B-n`.** ⚑ **No retired id is ever re-used** (`TA-X-23` and `TA-B-13`'s band form stay
retired).

| **canonical** | statistic | gandalf v1.0 | gamora § 2.4 | gamora Add. 1 | **construction governed by** |
|---|---|---|---|---|---|
| `TA-B-01` | terminal wave | B-1 | B-1 | — | ⚑ **`[M-POL2]`'s `terminals` array (§ A.5)** · REPORT-ONLY |
| `TA-B-02` | **uptime** on `D` | B-3 | **B-2** | **B-4** | `P-a` Add. 1 · **width VOID** |
| `TA-B-03` | `frac_moving` on `D` | B-4 | B-3 | B-3 | `P-a` Add. 1 · **width VOID** |
| `TA-B-04` | `P(chan \| moving)` | B-5a | B-4 | B-5a | `P-a` Add. 1 · **width VOID** |
| `TA-B-05` | `P(chan \| stationary)` | B-5b | B-5 | B-5b | `P-a` Add. 1 · **width VOID** |
| `TA-B-06` | plant ratio | B-8 | B-6 | B-6 | **v1.5 § F.3a's recovered definition** · **width VOID** |
| `TA-B-07` | release duty on `D` | B-7 | B-7 | B-7 | `P-a` Add. 1 · **width VOID** |
| `TA-B-09` | channel split | *(v1.1)* | — | — | `P-a` Add. 2 § B2 · **width VOID** |
| `TA-B-15` | NO-DATA spawn count / fraction | — | — | — | ⚑ **`P-e` § 3 — INVERTED; both points `0.0000`** |
| `TA-B-16…19` | the per-wave restatements | — | — | — | ⚑ **OWED; and `TA-B-16` must SPLIT first (`P-a` Add. 4 § A4.4)** |
| `TA-X-03…06` | inertness / distinctness | E-2, E-3, E-4 | **E-1 (a–d)** | A4 | — |
| `TA-X-07` | conservation, 7 terms | E-5 | **E-2** | — | v1.5 § F.2d |
| `TA-X-02` | coverage | E-1 | **E-3** *at 89/89* | — | — |
| `TA-X-08` | denominator identity | *(implicit)* | **E-4** | A1 | — |
| `TA-X-11` | wall-clamp zeros | E-7b | — | **A2** | — |
| `TA-X-25` | NO-DATA path | — | — | — | ⚑ **RE-AUTHORED — `P-e` § 3 + § F.2f** |
| `TA-X-26` | declared-JOIN conformance | — | — | — | `P-i` + § F.2a |
| `TA-X-27` | degenerate-draw consumption | — | — | — | `P-h` + § F.2b |
| ⚑ `TA-X-28` | ⚑ **leech target law** | — | — | — | ⚑ **legolas C-8 + KP-96 (i) + § F.2g** |
| ⚑ `TA-X-29` | ⚑ **global-magnitude fold conformance** | — | — | — | ⚑ **`P-h`'s `PRED-GMAG-WHOLE` + `Z5-LAW` + § F.2h** |
| ⚑ `TA-X-30` | ⚑ **the pursuit halt** | — | — | — | ⚑ **`P-h`'s `arena.json :: d_engage_m` + § F.2i** |

*The uptime row remains the reason this table exists: **B-3 · B-2 · B-4 — three ids, one statistic,
two files.*** ⚑ *And at v1.6 the concordance spans a THIRD artifact class again: `TA-X-28`'s
governing text is a legolas finding, `TA-X-29`'s is a PREDICATE inside the pack, and `TA-X-30`'s is
a single scalar on the wire.*

---

## § E · OUTSIDE T-A'S REACH — the catching-row audit

### E.1 · The traps

| # | trap | **caught by** | verdict at v1.6 |
|---|---|---|---|
| **1** | `V5-GUARD-2` — arrival `px, py` are TELEMETRY ONLY | `TA-X-19` | **CLOSED** *(vacuously — the port has no arrival limb; § F.5 cl. 6)* |
| **2** | `V9-DEAD-2` — the retired square-box scatter draws at the **same stream position** | `TA-X-17` + `TA-X-18` | **CLOSED** |
| **3** | `V17` — `hit_test_model = "point"` vs the sim's uniform 3.0 m disc | `TA-X-20`; `R2D-5` owns the DRAWN radius | **HALF-CLOSED — declared** |
| **4** | `V4-LAW-1` — the cadence law is **not RNG-neutral** | `TA-X-21` | **CLOSED** |
| **5** | `V18 + V19` — flag **AND** coin = 0.15 applied twice | `TA-X-22` | **CLOSED** |
| **6** | ⚑ **THE BOARD ROLL** | `P-3` + `TA-X-27` (draw-count) | ⚑ **OPEN, AND WIDER THAN IT WAS.** `TA-X-25(c)` used to give a one-bit **membership** test; ⚑ **the re-base DELETED that bit** (§ A.3: there are no NO-DATA members left to spawn). **Composition was never covered and membership no longer is.** Closure is still a sibling emitting per-wave class counts |
| **7** | attack-**PHASE** model — `HASH` default vs `ENGAGE` of record | `TA-X-24` | **CLOSED** |
| **8** | a declared LIMB or JOIN with no implementation | `TA-X-26` | **INSTRUMENTED** |
| ⚑ **9** | ⚑ **NEW — A DECLARED FOLD WITH A PARTIAL IMPLEMENTATION.** ⚑ **Worse than trap 8, because a PARTIAL lift REPORTS ITSELF WHOLE**: a loader taking I-14 alone reaches **23 of 344** actors and **39/423** limb records and looks finished | ⚑ **`TA-X-29`, against the pack's own `PRED-GMAG-WHOLE`** | ⚑ **NEWLY INSTRUMENTED. The pack ships the predicate precisely so this is not a matter of care** |
| ⚑ **10** | ⚑ **NEW — A FOLD LEFT AT ITS DEFAULT.** The winner-surface fold is **byte-inert when off**, so forgetting to arm it produces no error, no counter and no digest change | ⚑ **`P-5`** | ⚑ **NEWLY INSTRUMENTED as a PRECONDITION rather than a row, because a row that grades it would already be reading a board built the wrong way** |

⚑ **Trap 6, restated with v1.6's movement stated honestly and in the losing direction.** **12 of
the 29 live draw sites are the board roll.** Its divergence shows as **a different SET of monsters,
not a different number.** `TA-X-25(c)` proved **membership** and never **composition**; the re-base
removed the population that made even the membership bit readable. ⚑ **v1.5 could say *"narrower
again."* v1.6 must say *"wider."*** **Stating that plainly is the point of the trap table.**

### E.2 · DECLARED CEILINGS

| # | ceiling | status at v1.6 |
|---|---|---|
| **C-a** | the refusal discriminator is **structurally dead under `ORACLE`** | ⚑ **MOOT IN BOTH CONFIGS.** With `NO-DATA = 0` the `PLAY` refusal rule has nothing to refuse either. **The whole NO-DATA apparatus goes inert together** |
| **C-b** | the ten-wave composition expectation has **NO empirical check** — the sealed census covers 151–155; the fight scope is 151–160 | ⚑ **HOLDS, AND THE RE-BASE DID NOT CLOSE IT.** v1.5 said F2's re-base *"is the first thing that could."* ⚑ **It did not: `K-7` still forbids minting a cell over 156–160, and none was minted.** Waves 156–160 carry **50.9 %** of the port's bodies |
| ~~**C-c**~~ | ~~the `limitN` residual~~ | **STRUCK — VOID.** The question is re-opened at `OQ-6` |
| **C-d** | honest-fail row (b) `342` does not decompose against (a) `338` + 6 measured-inert | ⚑ **RESOLVED BY THE RE-BASE, AND THE ARITHMETIC IS CLEAN: `344 = 342 + 2`.** The 344 `POOL-466` members with no `v20` slot at v3.3 partition exactly into the **342** the rebase armed and the **2** class-B construction drops. **The grain disagreement was real and it was `338` (member-minus-`BOTH-128`) against `344` (no-`v20`-row); both are correct at their own grain and 338 + 6 = 344** |
| **C-e** | `TA-B-12` (intake / leech) has **NO ORACLE SIDE** in the seals | ⚑ **HOLDS AS A T-A CEILING AND ITS URGENCY HAS COLLAPSED.** `leech`, `intake` and `damage_total` still return zero keys on both seals. ⚑ **BUT the question it guarded is ANSWERED OFF-SEAL: the sealed stack kills the player at 151–156 (§ A.5), so *"a green T-A is compatible with an unkillable player"* is no longer the live risk. The live risk INVERTED** |
| **C-f** | the `~29×` leech surplus unexplained | ⚑ **LARGELY EXPLAINED AND RE-POINTED.** legolas F-1 (`M_inst` ×1.830, ÷1.715 measured) + the pursuit repair + the global-magnitude fold. **Residual at w160 on the port: intake per body ~168 HP/s against the referent's ~2,452.** ⚑ **The oracle brackets the referent from the OTHER side (4,822.7 HP/s/body pooled = ×1.97). THE TWO REPLICAS BRACKET THE REFERENT FROM OPPOSITE SIDES, and that is a T-C fact, not a T-A one** |
| **C-g** | every `P-a` width calibrated at ticks-per-wave ∈ [106, 185], applied at 482.4 | ⚑ **SUPERSEDED BY § A.4 — the widths are VOID, so there is nothing left to mis-apply.** The **calibration-range field stays mandatory** (§ F.5 cl. 5) so the successor cannot re-introduce it |
| ⚑ **C-h** | ⚑ **NEW — `TA-X-09` GRADES 9 OF 29 `math_rules` TEST VECTORS.** The 20 ungraded sit on `RULE-MONSTER-TO-PLAYER-MITIGATION-ORDER`, `normative: true` | ⚑ **OPEN, DECLARED, NOT WIDENED HERE (§ A.2).** ⚑ **They govern the rule the entire intake thread is argued under. `OQ-9`** |
| ⚑ **C-i** | ⚑ **NEW — THE ORACLE IS ~×1.9 OVER-LETHAL AGAINST THE REFERENT AND T-A CANNOT SEE IT.** Death at 151–156 against Matt's 160 | ⚑ **HOLDS, AND IT IS A `T-C` EXPOSURE, NOT A `T-A` ONE** — T-A compares port and oracle under the same pilot and the same folds. **Commission `C-11` is REGISTERED, not issued** (KP-102 (iii)). ⚑ **A green T-A and a `NO` from Matt at T-C are fully compatible, and § F.5 cl. 10 says so on the face** |
| ⚑ **C-j** | ⚑ **NEW — `ABS-C-I14-2-SOURCED-UNFOLDED`: a sourced wave-level term is DECLARED AND UNFOLDED ON BOTH SIDES** | ⚑ **HOLDS AND IS HARMLESS TO T-A BY SYMMETRY.** `offensivePhysicalModifier`, MEASURED −18 % @ w151 → −25 % @ w171, **bound ≤ 2.2 % pooled and exactly ×1.000 at w159/160** (every priceable body there is `physical_clamped`). **Neither side folds it, so no row grades it.** Folded at the next forward revision |
| **S5 / 29 sites** | a stream divergence is **visible and not locatable** | **HOLDS.** 34 sites declared / **29 live**; no sealed cell to place them against |

---

## § F · THE GRADED ROWS

### F.1 · Decisiveness classes — **F5, plus one new admission clause**

**EXACT** — identity, invariant, count, or declared-precision reproduction; a red says **the port is
wrong**; may carry a **NUMERICAL** tolerance, **never a STATISTICAL one**. ⚑ **The EXACT set is the
entire instrument. Every verdict antecedent is an EXACT-row fact, and Q87 makes ALL of them a seal
condition.**

**DIAGNOSTIC** — distributional at `n = 5`. ⚑ **NO DIAGNOSTIC GATES ANYTHING. A diagnostic cannot
produce, raise, or lower a verdict. It cannot trip the cap. It cannot be counted in a PASS label.**
Matt, F5: ***"treat the tolerance half as a DIAGNOSTIC, NEVER A GATE."*** ⚑ **The demotion removed
their AUTHORITY, not their VALUE** — `TA-B-09` at +32.5 half-widths with the **wrong sign** told the
run a genuine motion defect sat underneath a confound, which is worth more than any pass/fail.

**The STRUCTURAL-ZERO / STRUCTURAL-NON-ZERO class.** An EXACT row may assert a quantity whose value
is fixed by the construction of the system rather than by a distribution. **The admission test: can
you name the mechanism that makes the other value impossible?** If the answer is *"it would be very
unlikely"*, **it is a diagnostic and it does not belong here.**

> ⚑ **NEW ADMISSION CLAUSE — `F.1a`, AND `TA-X-25` IS WHY IT EXISTS.**
> **A structural row must ALSO answer: *CAN THE MECHANISM BE REPAIRED?* If the mechanism is a
> property of OUR OWN decode's completeness rather than of the system, the row CARRIES AN EXPIRY
> and names the event that voids it.**
> ⚑ *`TA-X-25` rested on "POOL-466 contains 338 NO-DATA members" — a measure of how much we had not
> yet decoded. When the substrate improved, the row did not merely fail; **it became false, and it
> reddened a correct port on every arm.*** **Every structural row in § F.2 now carries an
> `expiry` column stating what would void it.**

### F.2 · EXACT rows — ⚑ **v1.7: 28 EXACT + `TA-X-06` UNGRADEABLE-declared (on record)**, each with its explicit v1.5 → v1.6 disposition

*⚑ v1.7: the v1.6 → v1.7 disposition is **NONE** for every row below except `TA-X-06`.*

| id | statistic | basis | tolerance | ⚑ **v1.5 → v1.6** | ⚑ **reason / expiry** |
|---|---|---|---|---|---|
| `TA-X-01` | port self-determinism — any arm/salt run twice → identical digest; **the arm+salt is NAMED and MUST DIFFER from `P-2`'s** | run-internal | byte-exact | **CARRIED** | run-internal; no substrate dependency. **No expiry** |
| `TA-X-02` | **coverage 89/89**, zero unmapped | the census id list | integer | **CARRIED; the 4-way COUNTS move (§ B.2 cl. 4)** | the total is a property of the census, not the pack. **Expiry: a census amendment** |
| `TA-X-03` | inertness A — `port(M-POL-2-NULL, s) ≡ port(M0, s)`, all 5 | `[M-POL2]` | byte-exact | **CARRIED IN FORM; ⚑ EVERY DIGEST MOVES (§ C.7 cl. 1)** | port-to-port at one substrate. ⚑ **No v1.4/v1.5 digest may be carried as a constant** |
| `TA-X-04` | inertness B — `port(W1-NULL, s) ≡ port(M-POL-2, s)`, all 5 ⚑ **not `M0`** | `[W1W]` | byte-exact | **CARRIED IN FORM; digests move** | as above |
| `TA-X-05` | distinctness C — `port(M-POL-2, s) ≢ port(M0, s)`, ≥ 1 salt | `[M-POL2]` | exact, one-sided | **CARRIED IN FORM; digests move** | as above |
| ⚑ `TA-X-06` | distinctness D — `port(W1, s) ≢ port(M-POL-2, s)`, ≥ 1 salt | `[W1W]` | **RELATION ONLY, never magnitude** — ⚑ **v1.7: EMITTED AND PRINTED, NOT GRADED** | ⚑ **v1.7: `UNGRADEABLE-declared` — Matt, `Q83(b)` YES, KP-110. ON RECORD; GATES NOTHING; § F.2e.** *(v1.6: carried AS CLASSED, `Q83(b)` open)* | ⚑ **the row is unfalsifiable in the honest direction; its only mechanism (`TA-B-14`'s veto counter) is report-only** |
| ⚑ `TA-X-07` | conservation — **SEVEN terms** `offered = applied + dropped + voided + pool_truncated + pcl_reclaim + counterplay_absorbed` | run-internal | ⚑ **RELATIVE `\|residual\|/max(1,\|offered\|) ≤ 1e-12`, absolute REPORTED beside `offered`, and an ACCUMULATION BUDGET of ~4,500 terms** | **CARRIED (v1.5's construction, authorized under F4)** | ⚑ **the richer board deepens the sum; clause (c) makes that SELF-REPORTING — a realised depth above 4,500 makes the row `UNGRADEABLE`, not green.** ⚑ **The assert-wall checks SIX of the seven; the wall is not the row** |
| `TA-X-08` | denominator identity, both sub-identities | `[M-POL2]`, 5/5 | exact | **CARRIED; re-verified against the seal (`D = 2783`)** | an identity. **No expiry** |
| ⚑ `TA-X-09` | all **9** `math_rules.test_vectors` | ⚑ **`P-h`'s `math_rules.json` `cc4a9fdb…`** | per-vector | ⚑ **RE-DERIVED — THE PIN MOVES AND THE NINE DO NOT (§ A.2). Scope stays 9; the other 20 are ceiling `C-h`** | ⚑ **all 15 rules byte-identical v3.3 → v3.4.2; the digest moved on appended annotation blocks only** |
| `TA-X-10` | containment supremum `max_body_radius_m ≤ 43.758085029822276` (W1) | `[W1W]` · `arena.json` | exact, ≤ | ⚑ **RE-DERIVED, UNCHANGED** | ⚑ **`max‖spawn_xy‖ + placement_extents_m = 35.758085029822276 (p01) + 8.0`. `arena.json` byte-identical** |
| `TA-X-11` | wall-clamp zeros — `n_wall_clamps_{player,body} == 0`, every W1 arm | `[W1W]` | integer | **CARRIED; ⚑ the 0.807 % margin RE-MEASURES on the new board** | ⚑ **structural zero. Expiry: any spawn-law or arena change.** *A port with no wall also scores zero* — § F.5 cl. 6 |
| `TA-X-12` | pool inertness under ORACLE — total pool damage `== 0.0` | `[W1W]` · `DIV-19` | exact | **CARRIED** | structural zero, **satisfied by ABSENCE** — the aprons are absent, not present-at-zero |
| `TA-X-13` | no player crit | `V0 · CritLimb LO` | integer | **CARRIED** | config identity |
| `TA-X-14` | the two DO-NOTs (`cause == "energy"` → 0; no release-on-every-cast) | ⚑ **`math_rules` `RULE-NO-ENERGY-GATED-RELEASE` + `RULE-NO-RELEASE-ON-EVERY-CAST`, both present and `normative: false` prohibitions (verified)** | integer | **CARRIED** | ⚑ **AND IT NOW INTERACTS WITH C-7: a REFUSED cast is not a release, and `cause == "energy"` must still be 0. § F.2f cl. (d)** |
| `TA-X-15` | **release schedule — TWO CLAUSES.** (a) POSITIVE: p01–p04 at `t = 0.0`, **p05 one burst at `t = 4.000 s`** (tick 49 at 12.2 ticks/s). (b) NEGATIVE: **no intra-point stagger** | census `M4` / `V11` | exact | **CARRIED; (b) is `GREEN-BY-CONSTRUCTION` and must PRINT the absence** | **(b): the structure cannot express a stagger — *unrepresentable rather than absent*** |
| `TA-X-16` | **p06 OFF — declared value AND enforcement.** `n_pool_picks == 47`, `n_spawn_point_6_keys_rolled == 0`, **and a COUNTER for the filtered keys** | `V0-36` · `waves.json` | integer | ⚑ **RE-DERIVED, UNCHANGED** | ⚑ **distinct `(global_wave, spawn_point)` pairs over waves 151–160: `54` with p06, `47` without; `spawn_point 6` appears in 7 of 10 waves. Both figures reproduce exactly. `waves.json` byte-identical.** *A filter with no counter is indistinguishable from a filter that never fired* |
| `TA-X-17` | spawn offset — `‖spawn_xy − anchor_xy‖ ≤ 8.0` m, every body, arm, salt | `ρ = 8.0·u₂` | exact, ≤ | ⚑ **RE-DERIVED, UNCHANGED** | ⚑ **`arena.json :: placement_extents_m = 8.0`, byte-identical** |
| `TA-X-18` | **scatter-law three-law discriminator** — feed `u₁ = u₂ = 0.5`, assert **`(−4.0, 0.0)`** | polar → `(−4.0, 0)` · uniform-in-area → `(−5.656854249492381, 0)` · box → `(0.0, 0.0)` | exact | ⚑ **RE-DERIVED, UNCHANGED** | ⚑ **computed from `placement_extents_m = 8.0`: `8.0 × 0.5 = 4.0` vs `8.0 × √0.5 = 5.656854249492381`. The three laws remain separated by 1.66 m** |
| `TA-X-19` | arrival unconditionality; **no damage predicate reads an arrival's `px, py`** | `deferred_arrival.py:13-17` | integer | **CARRIED** | ⚑ **GREEN-VACUOUSLY — the port has NO arrival limb. § F.5 cl. 6, and `OQ-8` routes the missing limb as a real gap** |
| `TA-X-20` | player hit-test predicate — 2.99 m hit / 3.01 m miss; no angular gate; no target cap | census `D7` | exact | **CARRIED** | ⚑ **AND `TA-X-28` now grades the LEECH consequence of the same disc, which `TA-X-20` never reached** |
| `TA-X-21` | **quantisation rule per site + zero bare `round(`** on the port's threat path | four modules | exact | **CARRIED; ⚑ RE-VERIFY THE LIVE SITE LIST** | ⚑ **the global-magnitude fold adds arithmetic at `threat.py:1826-1836`; the site list is a property of the CODE, and the code moved** |
| `TA-X-22` | flag-off release cause under ORACLE — `cause == "interrupts_channel_flag"` **0** | `V0`; V18+V19 | integer | **CARRIED** | config identity |
| ~~`TA-X-23`~~ | ~~board-roll composition~~ | ⚑ **STRUCK at v1.2. Id retired, never re-used** | — | — | — |
| `TA-X-24` | **attack-phase model is `ENGAGE`** — `sha256(actor_id) mod n` never evaluated | `V0`; `run.py` / `threat.py` carry `HASH` as the **DEFAULT** | exact | **CARRIED** | ⚑ **a DEFAULT that differs from the config of record is the `P-5` hazard one layer down, and this row is the precedent for `P-5` existing** |
| ⚑ `TA-X-25` | ⚑ **THE NO-DATA PATH — RE-AUTHORED AS ACCOUNTING IDENTITIES** | ⚑ **`P-e` § 3 · § F.2f** | integer identity | ⚑ **RE-AUTHORED. Carried unchanged it REDS A CORRECT PORT ON EVERY ARM** | ⚑ **§ A.3: `NO-DATA 338 → 0`. Two of three clauses were structural non-zeros whose mechanism the re-base deleted** |
| `TA-X-26` | **DECLARED-JOIN CONFORMANCE — five clauses** | `P-i` · § F.2a | integer / exact / declared-precision | ⚑ **(a)–(d) RE-DERIVED, UNCHANGED. (e) RE-DERIVED AND ITS POPULATION CORRECTED** | ⚑ **(c) reproduces exactly: 7,900 rows · 790 records · 8 resist tiers · 5 multiplier values · 790/790 wave-invariant. (e): `0.266406` was `BOTH-128`, not "armed" — § A.6** |
| `TA-X-27` | **DEGENERATE-DRAW CONSUMPTION — four clauses** | `P-h` · § F.2b | integer / byte-exact | ⚑ **(a)(b)(c) CARRIED. (d) RE-DERIVED, UNCHANGED** | ⚑ **`waves.json` byte-identical: 139 min/max pairs over waves 151–160, 97 degenerate = 69.8 %. Reproduces to the decimal** |
| ⚑ **`TA-X-28`** | ⚑ **THE LEECH TARGET LAW — three clauses** | ⚑ **§ F.2g** | integer / structural | ⚑ **NEW** | ⚑ **KP-96 (i): *"NO CAP, in oracle or port. `n_caps_applied == 0` is the best-sourced line in the fold; a cap would be a fitted constant (Law 3)."*** |
| ⚑ **`TA-X-29`** | ⚑ **GLOBAL-MAGNITUDE FOLD CONFORMANCE — five clauses** | ⚑ **§ F.2h** | integer / declared-precision | ⚑ **NEW** | ⚑ **the D19 hole. The pack ships `PRED-GMAG-WHOLE` precisely so a PARTIAL lift cannot report itself whole** |
| ⚑ **`TA-X-30`** | ⚑ **THE PURSUIT HALT — two clauses** | ⚑ **§ F.2i** | exact / integer | ⚑ **NEW** | ⚑ **80.5 % of movers halted beyond `d_engage` before the repair, and census `M10` read `IMPLEMENTED` through it** |

---

#### ⚑ F.2a · `TA-X-26` — **DECLARED-JOIN CONFORMANCE** *(carried; clause (e) re-derived)*

| clause | assertion | class | ⚑ **v1.6** |
|---|---|---|---|
| **(a)** | **every declared JOIN in `V0`/`V1` is either CONSUMED — with a named call site emitted — or DECLARED-UNCONSUMED BY NAME against an absence row.** The runtime emits `join_consumption_audit` and asserts `n_declared == n_consumed + n_declared_unconsumed`, **zero joins in neither state**, refusing the cell otherwise | **EXACT · integer identity** | **CARRIED** |
| **(b)** | `V1-JOIN-1`: `pm4p_leech_resistance.csv` is **LOADED**, its sha verified against **`P-i` = `cb6a008bde1e102573181968ab7f60958cd28fee07ff8736078fa092a80dd62e`** (re-derived), and the audit names **≥ 1 call site on the sustain path** | **EXACT · structural non-zero** | **CARRIED; `P-i` re-derived unchanged** |
| **(c)** | **PARSE INTEGRITY — RFC-4180.** On load: **7,900 data rows** · **790 distinct `record`** · **exactly 8 distinct `total_leech_resist_pct`** · **exactly 5 distinct `adcth_mult_COUPLED`** · **all 790 records wave-invariant** | **EXACT · integer counts** | ⚑ **RE-DERIVED, ALL FIVE HOLD.** Tiers `{65, 75, 83, 88, 105, 115, 565, 588}`; multipliers `{0.0, 0.12, 0.17, 0.25, 0.35}`; **790/790 wave-invariant.** ⚑ **8 tiers → 5 values because `max(0, 1 − res/100)` collapses the last four; asserting 5 where 8 belongs, or 8 where 5 belongs, would be GREEN ON A SHIFTED PARSE. Both counts are asserted and they are not redundant** |
| **(d)** | **THE LAW IS READ, NEVER RECOMPUTED** (`V1-LIMB-2`): the applied multiplier comes from the CSV **column**; any helper implementing `max(0, 1 − res/100)` exists **only as a cross-check** and has **exactly one call site** | **EXACT · structural** | **CARRIED** |
| ⚑ **(e)** | ⚑ **MAGNITUDE, ON A POPULATION STATED AS A SET EXPRESSION.** Over `ARMED-464 := POOL-466 ∩ (v20 ∪ w40 ∪ w41 ∪ w44 ∪ w45)`: `mean(adcth_mult_COUPLED)` reproduces **`0.2468965517`**, median **`0.25`**, max **`0.35`**, min **`0.0`**, **17 leech-immune records** | **EXACT · declared-precision, `± 5e-7`** | ⚑ **RE-DERIVED. v1.5's `0.266406` / "5 of 128" belong to `BOTH-128` and are RETAINED AS LINEAGE, not as this clause's target** |

> ⚑ **THE CORRECTION, AND IT IS MINE TWICE OVER.** v1.5's clause (e) read *"over the armed records
> of `POOL-466`"* and pinned `0.266406` — and warned, in its own note, that *"same file, same
> column, two populations, two answers"* was the **fifth instance** of this run's one shape.
> ⚑ **It then committed the sixth in the sentence immediately following: `0.266406` is `BOTH-128`
> (`ANCHOR-169 ∩ POOL-466`), a DECODE-COVERAGE population, and the ARMED population at v3.3 was
> **122** with mean **`0.262295`**.** Three populations, three answers, one column:

| population | definition | n | mean | zeros |
|---|---|---:|---:|---:|
| `BOTH-128` | `ANCHOR-169 ∩ POOL-466` — decode coverage | 128 | **0.266406** | 5 |
| `ARMED-122` | `POOL-466 ∩ v20` — armed at v3.3 | 122 | **0.262295** | 5 |
| ⚑ **`ARMED-464`** | ⚑ **`POOL-466 ∩ (v20 ∪ w40 ∪ w41 ∪ w44 ∪ w45)` — armed at v3.4.2** | **464** | ⚑ **0.2468965517** | ⚑ **17** |
| `ROSTER-790` | every record in `P-i` | 790 | **0.252215** | 48 |

> ⚑ **CLAUSE (e) AT v1.6 CARRIES ITS POPULATION AS A SET EXPRESSION RATHER THAN A PHRASE, because a
> phrase is what went wrong. A grader can evaluate the expression; nobody can evaluate "armed."**

#### ⚑ F.2b · `TA-X-27` — **DEGENERATE-DRAW CONSUMPTION** *(carried; (d) re-derived)*

| clause | assertion | class | ⚑ **v1.6** |
|---|---|---|---|
| **(a)** | **SOURCE NEGATIVE — no short-circuit.** A purity scan over the whole runtime tree finds **zero** `lo == hi` / `n_min == n_max` early-returns on **any registered draw site**; the scan censuses every draw-site call and **refuses any it cannot classify** | **EXACT · integer, scanned** | **CARRIED** |
| **(b)** | **THE REJECTION LOOP IS REPRODUCED, NOT APPROXIMATED.** A vector table replays CPython's `_randbelow_with_getrandbits` — reject-and-redraw while `r >= n`, every `getrandbits` counted — asserting **per-seed** consumption, never the mean | **EXACT · byte-exact per vector** | **CARRIED.** *The consumption is GEOMETRIC — values in `{1,2,4,5}` over 20 seeds. A port accounting a degenerate draw as ONE value desynchronises on roughly half the occasions, which looks like noise* |
| **(c)** | the port consumes exactly what the **ORACLE** consumes; where the oracle takes no draw (**p05**, `wave_engine.py:683-695`), the port takes none; `V9`'s registry stays at **29 live sites** | **EXACT · integer identity** | **CARRIED** |
| ⚑ **(d)** | **THE DEGENERATE-PAIR CENSUS.** Over `P-h`'s `waves.json::pools.wave_spawn_count`, global waves 151–160: **139 min/max pairs**, of which **97 are degenerate = 69.8 %** | **EXACT · integer counts** | ⚑ **RE-DERIVED AND UNCHANGED, on a BYTE-IDENTICAL `waves.json` (§ A.1)** |

⚑ **The honest limit, restated: `TA-X-27` closes the DRAW-COUNT half of trap 6 and says nothing
about WHICH monsters were picked** — and at v1.6 the membership half that `TA-X-25(c)` used to give
is gone too (§ E.1 trap 6).

#### ⚑ F.2c · THE THREE FORMERLY-UNGRADEABLE EXACT ROWS — **their closing conditions, carried**

⚑ **The consequence a grader must not let pass silently: a repair pass that fixes only the reds
lands on `INDETERMINATE`, and `INDETERMINATE` trips the cap just as hard. ALL of them must close,
and Q87 now makes "all EXACT green" the seal itself.**

| row | closing condition | state |
|---|---|---|
| **`TA-X-01`** | a genuine repeat probe: **ANY arm, ANY salt, run twice with NOTHING inserted, byte-exact — and the emission NAMES the arm and the salt, which MUST DIFFER from `P-2`'s (`M-POL-2`, salt 0)** | ⚑ **CLOSES.** drax exercised it on a deliberately different arm/salt (KP-44); **the emission is still owed.** ⚑ **The name requirement IS the row: two rows resting on one execution path are one row** |
| **`TA-X-15`** | (a) the realised release schedule is **emitted**; (b) **no intra-point stagger**, printed as `GREEN-BY-CONSTRUCTION` with its mechanism | ⚑ **(a) CLOSES** (p05 at tick 49, KP-44). **(b) is green-by-construction, not measured** |
| **`TA-X-16`** | `n_pool_picks == 47` · `n_spawn_point_6_keys_rolled == 0` · **a counter for the filtered keys** | ⚑ **CLOSES.** Two independent routes agreed at v1.5 (pack recomputation 54/47; port 54 pre-fix / 47 post-fix), and ⚑ **the pack recomputation RE-DERIVES to 54/47 here on a byte-identical `waves.json`** |

#### ⚑ F.2d · `TA-X-07` — **THE TOLERANCE, CARRIED AS SPECIFIED AT v1.5**

| clause | assertion |
|---|---|
| **(a) GRADED — RELATIVE** | `\|residual\| / max(1.0, \|offered\|) ≤ **1e-12**` |
| **(b) REPORTED, NOT GRADED — ABSOLUTE** | `\|residual\|` printed **with `offered` beside it**, every cell |
| **(c) THE ACCUMULATION BUDGET** | `1e-12 ≈ 4.5e3 × float64 eps (2.220446e-16)` — an accumulation-depth budget of **~4,500 terms**. The runtime **EMITS the realised number of terms summed into `offered`. If the realised depth EXCEEDS 4,500, the row is `UNGRADEABLE`, not green** |

> ⚑ **AND CLAUSE (c) IS NOT DECORATION AT v1.6.** The v3.4.2 board arms **464** records instead of
> 122 and applies a per-body multiplier of **×5.418 at w160**. ⚑ **The sum got deeper and richer in
> exactly the way clause (c) was written to notice.** If the depth exceeds the budget the row goes
> `UNGRADEABLE` and the cap trips — **which is the correct outcome, because the tolerance was sized
> for a depth the run exceeded.** *A tolerance derived from the machine and checked against the
> realised depth is falsifiable; a tolerance derived from the data is a restatement of the data.*
> ⚑ **The assert-wall gap is carried unchanged: the row names SEVEN quantities and the live driver
> assert-wall checks SIX. The wall is not the row.**

#### ⚑ F.2e · `TA-X-06` — ⚑ **v1.7: `UNGRADEABLE-declared` BY MATT'S RULING (`Q83(b)`, KP-110). ON RECORD; GATES NOTHING.**

⚑ **v1.7: `Q83(b)` IS RULED — YES, 2026-09-29 (KP-110).** `TA-X-06` is `UNGRADEABLE-declared`.
v1.6's status text in this section (*"`Q83(b)` IS OPEN. Matt has not ruled it"* and *"Why I do not
reclass it here, for the third version running"*) **became false at KP-110 and is not carried**; it
stands in v1.6 (`db2c0ca3…`), unedited. **It was right when written:** reclassing inside the
document that asked Matt to reclass would have mooted the question rather than answered it
(jack-ryan, pre-read `OQ-1`: *"correct"*). **It was answered, by ruling.**

**What the declaration means, mechanically — and it is the whole of the change:**

1. **The row stays ON RECORD.** Its id, statistic (distinctness D, relation only) and basis
   (`[W1W]`) are unchanged. It is not struck, and the id is never re-used.
2. **It is EMITTED AND PRINTED, NOT GRADED.** The runtime emits the per-salt relation (the `W1` /
   `M-POL-2` digest pair) with `TA-B-14`'s counters beside it, and the report prints it under the
   label **`UNGRADEABLE-declared (Q83(b), KP-110)`**, with no colour.
3. ⚑ **IT ENTERS NO VERDICT ANTECEDENT.** It cannot produce `STRUCTURAL`; it is **not** *"an EXACT
   row UNGRADEABLE"* and so cannot produce `INDETERMINATE`; it is not counted in a `PASS` label
   (**28/28**). § G says so in terms.
4. ⚑ **IT IS NOT A Q87 SEAL CONDITION.** *"All EXACT rows green"* is the 28 of § 0.1.
5. ⚑ **NOTHING IS RESCUED.** v1.4's grade of record `STRUCTURAL @ coverage 89/89` stands on
   `TA-X-07` independently (with `TA-X-01` / `TA-X-15` independently `UNGRADEABLE` at v1.4). No
   graded result exists under v1.6 for the declaration to move.

**The reasoning Matt ruled on — v1.6 § F.2e, carried verbatim:**

⚑ **AND WHAT IS NEW AND WHY IT CANNOT WAIT.** At v1.5 the row's status was a bookkeeping question:
the verdict was `STRUCTURAL` either way and *"the verdict survives the removal of the row most
likely to be challenged."* ⚑ **Q87 changed that. The seal now requires ALL EXACT rows green — and
this row cannot be honestly greened:**

1. **The WALL contributes NOTHING to the oracle's `W1`-vs-`M-POL-2` distinction.** Its clamp
   counters are **zero on every arm**. The only counter that separates `W1` from `W1-NULL` is
   **`n_avoidance_vetoes`, 2 against 0.**
2. **The distinctness is carried ENTIRELY by the avoidance limb** — the limb with **no published
   trigger rule**, on a boundary `ABS-ARENA-BOUNDARY` declares absent, in a cell `V8-CELL-1` says
   ran **wall-less**.
3. **`W1` shows 2 vetoes / 0 occupancy; `W1-PROBE` (same config, `avoidance = False`) shows 0 / 2 —
   an exact complementary pair.** That gives the limb's **EFFECT**, never its **TRIGGER**, and
   without the trigger the effect cannot be reproduced.
4. **THE MIS-CLASS:** `TA-X-06` was classed **EXACT** while the only mechanism making its relation
   true was classed `TA-B-14` — report-only, no width, no trigger rule — **seven lines away in the
   same document.** *An EXACT row built on an input the same prereg declared unspecifiable.*
5. ⚑ **THE CONSEQUENCE, RESTATED UNDER Q87: the only route to green is to INVENT a veto rule — and
   then the row is green about a rule nobody wrote, and REFERENT-v1 is sealed on a fiction.**
   **A row that can only be passed by invention is a trap for the conscientious builder, and under
   Q87 it is a trap for the SEAL.**
6. **drax's call was correct and the record says so.** Given a choice between a true red and a
   green about a fiction he **chose the true red**, and made it legible from inside the runtime by
   declaring `arena_fold :: avoidance` unconsumed against `ABS-ARENA-AVOIDANCE-MECHANISM`.

⚑ **v1.7: v1.6 closed this section by naming it *"the ONE item in this document that can stop the
seal on a correct port"*, raised as `OQ-1` with a one-word lean. The lean was ruled YES and the item
is gone.** *(It was, precisely, the shape of MUST-CARRY #2 — a row that reds a correct port on a hole
that is not the port's. `TA-X-25` I could re-author from the substrate; this one needed Matt's word,
and has it.)*

#### ⚑ F.2f · `TA-X-25` — **THE NO-DATA PATH, RE-AUTHORED AS ACCOUNTING IDENTITIES**

> ⚑ **THE PRINCIPLE, AND IT IS `F.1a` IN PRACTICE.** v1.5's clauses asserted **SIGNS** (`> 0`), and
> a sign is only as durable as the substrate fact under it. ⚑ **v1.6 asserts IDENTITIES, which
> survive the next substrate move as well as this one.** The population figures below are
> **derived** (§ A.3) and are stated so the row can be checked, **not so it can be passed.**

| clause | assertion | class | what a RED means | ⚑ **expiry** |
|---|---|---|---|---|
| ⚑ **(a)** | under `ORACLE`, `n_nodata_refused == 0`, **every arm, every salt** | **EXACT · integer identity** | ⚑ **a config leak — the port is running the `PLAY` refusal rule under `ORACLE`** | ⚑ **NONE — and it is now VACUOUS as well as true: there are no NO-DATA bodies to refuse. § F.5 cl. 6 requires it to PRINT that it is satisfied over an empty set** |
| ⚑ **(b)** | ⚑ **THE SPAWN ACCOUNTING IDENTITY, replacing v1.5's structural non-zero.** Per arm per salt, the counters `n_nodata_spawn_inert`, `n_measured_inert_spawn` and `n_measured_offense_spawn` are **PRESENT and EMITTED**, and **`n_nodata_spawn_inert + n_measured_inert_spawn + n_measured_offense_spawn == n_bodies_spawned`** | **EXACT · integer identity** | the port has re-created the oracle's own silence, **or** it is classifying bodies into a fourth bucket it has not declared | ⚑ **NONE. An identity over a partition cannot be voided by a substrate that changes the partition's contents** |
| ⚑ **(c)** | ⚑ **SIGN INVERTED AND DEMOTED TO A CONSEQUENCE OF (b).** Across the 5 salts of an arm, **`Σ n_nodata_spawn_inert == 0`, every arm** | **EXACT · structural ZERO** | the port is spawning bodies it classifies NO-DATA from a population that contains none — **a roster-basis error, not a roll-population one** | ⚑ **EXPIRES IF THE POOL REGAINS A NO-DATA MEMBER.** Mechanism: **`POOL-466` contains ZERO NO-DATA members at v3.4.2** — 464 MEASURED-OFFENSE + 2 MEASURED-INERT + 0 NO-DATA = 466 (§ A.3) |
| ⚑ **(d)** | ⚑ **NEW, AND IT IS WHAT (c) COST US.** `Σ n_measured_inert_spawn` is **EMITTED, per arm, and REPORTED — NOT GRADED.** `POOL-466` holds exactly **2** MEASURED-INERT records (`basilisk_a01`, `yetidire_a01`), so a zero over five salts is **plausible and is not a defect** | ⚑ **EMITTED, NOT GRADED** | — | ⚑ **§ F.1's own test forbids grading it: two records out of 466 makes a non-zero *likely*, never *impossible*, and *"it would be very unlikely"* is a diagnostic** |

> ⚑ **WHAT `TA-X-25` PROVES AT v1.6, AND WHAT IT HAS STOPPED PROVING — for the report's face.**
> **PROVES:** the spawn classification is a complete partition of the bodies spawned; the
> `ORACLE`/`PLAY` config split is not leaking; the counters exist and are wired.
> ⚑ **HAS STOPPED PROVING:** that the port draws from `POOL-466` at all. **v1.4 bought a one-bit
> membership test with clause (c); the re-base spent it.** ⚑ **Trap 6 is WIDER at v1.6 than at
> v1.5, and § E.1 says so rather than letting the change read as progress.**
> ⚑ **AND THE HONEST NOTE ON WHAT REPLACED IT: nothing did.** `P-3`'s declaration is self-reported
> and `TA-X-25` was its behavioural check. **The behavioural check is gone and the declaration is
> not a substitute.** Closure remains a sibling emitting per-wave class counts.

#### ⚑ F.2g · `TA-X-28` — **THE LEECH TARGET LAW** *(NEW)*

> ⚑ **THE PRINCIPLE: the most expensive question of this lap was answered by an ABSENCE, and an
> absence that strong deserves a row, because the next builder's instinct will be to add a cap.**

| clause | assertion | class | what a RED means |
|---|---|---|---|
| ⚑ **(a)** | **NO CAP, EITHER SIDE.** `n_leech_target_caps_applied == 0` and `n_leech_tick_caps_applied == 0`, every arm, every salt, **oracle and port** | **EXACT · structural zero** | ⚑ **a fitted constant has entered the fold (Law 3).** ⚑ **legolas C-8: `DB-EXHAUSTIVE-ABSENCE` — the complete string tables of ALL EIGHT archives name no target-count, cap, diminishing or primary-target term for leech, while Crate NAMES its other caps in `gameengine.dbr` (`playerReflectCap 30.0`, `petLimit`). It capped retaliation and not leech** |
| ⚑ **(b)** | **FULL PER-TARGET, FULL DISC.** Leech accrues **once per hit body**, inside the loop over hits, with **no primary-target privilege and no arc gate**; the applied portion is the incumbent **`0.57 × D_weapon`** | **EXACT · structural** | the port has re-scoped the leech to a primary target or an arc. ⚑ **`OFFICIAL-GUIDE-VERBATIM`: EoR ticks are weapon attacks (57 % WD) and equipment ADCtH *"applies as if you attacked with your weapon"*; EoR's template chain does not reach `skillTargetNumber`; skill-sourced ADCtH follows a different rule and is correctly excluded; DoT never triggers it** |
| ⚑ **(c)** | **THE ORACLE IS THE SAME SHAPE, ASSERTED AND NOT ASSUMED.** The oracle's own accumulation is per body inside the hit loop with no target cap and no per-tick cap; **the port's structure matches it** | **EXACT · structural** | the two sides differ on a law neither is free to choose |

> ⚑ **WHY THIS IS AN EXACT ROW AND NOT A DIAGNOSTIC.** It asserts a **STRUCTURAL ZERO with a named
> mechanism**: not *"we did not find a cap"* but *"the complete string tables of eight archives do
> not contain one, and the same corpus contains the caps Crate did write."* **The mechanism that
> makes the other value impossible is the exhaustive absence itself.**
>
> ⚑ **AND THE LIMIT, PRINTED SO NOBODY OVER-READS A GREEN.** `TA-X-28` green says the two replicas
> implement the same leech law. ⚑ **It says NOTHING about whether that law reproduces Matt's fight:
> the footage EXCLUDES the oracle's own occupancy by 3.4–21× and brackets the referent at
> `N ≈ 1–1.7` bodies in the disc, where `heal:intake = 1.01`.** **The gap is OCCUPANCY, it lives in
> T-C, and § F.5 cl. 10 puts it on the face of any T-A report including a passing one.**

#### ⚑ F.2h · `TA-X-29` — **GLOBAL-MAGNITUDE FOLD CONFORMANCE** *(NEW)*

> ⚑ **THE PRINCIPLE, AND IT IS TRAP 8 ONE LEVEL UP.** `TA-X-26` catches a declared join with **no**
> implementation. ⚑ **This catches a declared fold with a PARTIAL one — and a partial lift is worse,
> because it produces numbers and reports itself finished.** A loader lifting I-14 alone reaches
> **23 of 344** actors and looks whole.

| clause | assertion | class | what a RED means |
|---|---|---|---|
| ⚑ **(a)** | **`PRED-GMAG-WHOLE`, the pack's own predicate, evaluates TRUE:** the attribute limb reaches **193** records of which **154** cite `pm4o_trash_terms.csv` (Lap O / I-16), **AND** the own limb reaches **527** records of which **104** do. A loader short of either **MUST REPORT ITSELF INCOMPLETE** | **EXACT · integer counts, from the pack** | ⚑ **the port lifted `pm4m_body_chain.csv ∪ pm4i_band_c_roster.csv` only, reaching 39 and 423 — short by exactly the Lap-O populations — and called itself whole** |
| ⚑ **(b)** | **THE COMPOSITION LAW `Z5-LAW` IS OBEYED VERBATIM (NORMATIVE):** `om` = `M_inst` (direct / leech) · `M_dot[family]` (dot) · **`1.0` (percent-current-life)**; the body's own percentage joins **ADDITIVELY into the pool** — `om += own_pct/100` — **never as a second multiply**; the attribute limb is **per family**; **leech rows are DROPPED** by G3; **the chain folds whole** | **EXACT · declared-precision** | ⚑ **the wrong form over-reads by `+25.5 %` at w159 (`om × (1 + own/100)` = 3.312 against the additive 2.640 at `own_pct = 81`)** |
| ⚑ **(c)** | **`z3` IS A CHECK AND IS ASSERTED BEFORE `own_add`:** the port's `M_inst` per wave equals the pack's `z3_wave_damage_modifier_check` rows **before** any own-term is added | **EXACT · declared-precision** | ⚑ **the own-term sum composes against a different pool and EVERY folded body is wrong by that difference** |
| ⚑ **(d)** | **THE 29 INERT RECORDS TAKE THE IDENTITY PATH** — `attr 1.0`, `type 1.0`, `own 0.0` — and are **NEVER estimated from a sibling, a bio-record donor or a class median** | **EXACT · structural identity** | ⚑ **supply has been invented. `ABS-GLOBAL-MAGNITUDE-FOLD-INERT-RECORDS`, 29 records, of which ⚑ 0 fall inside waves 151–160** |
| ⚑ **(e)** | **THE TERMINAL MAGNITUDE IS REPRODUCED, NOT ASSUMED INERT:** the supply-weighted pre-mitigation fold ratio is **×3.406 at w159** and **×5.418 at w160** | **EXACT · declared-precision** | ⚑ **a port reading the module's *"×1.000 at w159/160"* as inertness has read an EQUIVALENCE-VS-I-13 statement as an IDENTITY statement. ⚑ This was MY OWN caveat at U-P-N-4 and it resolved against my worst case: THE FOLD IS DENSEST WHERE THE RUN ENDS** |

#### ⚑ F.2i · `TA-X-30` — **THE PURSUIT HALT** *(NEW)*

| clause | assertion | class | what a RED means |
|---|---|---|---|
| ⚑ **(a)** | **THE HALT READS THE WIRE.** Every body halts at the single scalar `arena.json :: d_engage_m` — ⚑ **re-derived from `P-h`: `2.4`** — with `travel = min(v·dt, max(0, dist − d_engage_m))`, centre-to-centre distance, inclusive `<=`, per-tick order unchanged. **NaN is tested explicitly** | **EXACT · exact scalar + structural** | ⚑ **the port is halting at `_max_reach(record)` — the MAX over the body's attack slots — which is a TRUE identity about the WRONG CONSUMER: the oracle does gate ATTACKS on max-over-slots reach (`threat.py:1464`), so the attack test stays and only the PURSUIT test moves** |
| ⚑ **(b)** | **`n_bodies_halted_beyond_d_engage == 0`**, every arm, every salt | **EXACT · structural zero** | ⚑ **measured before the repair on Matt's own seed: 103 of 128 movers (80.5 %) halted beyond `d_engage`, 98 outside the 3.0 m disc, 13 at ≥ 32 m, the widest at 90 m — WIDER THAN THE ARENA'S 77 m CHORD. Two parked `wraith_c01` at ~35 m dealt 171 of the 226 hits Matt took** |

> ⚑ **WHY A ROW AND NOT A REPAIR NOTE.** The repair landed (godot `26ff0e6`; parked-beyond-`d_engage`
> **9/14 → 0/14**, worst halt **35.00 m → 0.00 m**). ⚑ **But census row `M10` read `IMPLEMENTED`
> for it — a true identity about the wrong consumer, equal to the max on 25 of 128 movers — and
> `P-1` cl. 1 says a mapping is a claim.** A row is what makes the claim checkable.
> ⚑ **AND THE CONFOUND THAT TRAVELS WITH IT, DECLARED: the repair amplified the heal surplus ~45×
> (mean bodies in disc 0.030 → 0.803).** The whirlwind had been **starved** — every earlier
> `OPEN-UNKILLABLE` reading on the port was taken with the mechanism eating nothing. **No earlier
> occupancy figure may be quoted without that sentence.**

### F.3 · DIAGNOSTIC rows — **19 ids, 0 gating, and every width VOID**

⚑ **Every diagnostic prints SIX fields beside its value: `value` · `@ coverage k/89` · **grain pair
(numerator / denominator)** · **calibration range** · **dilution factor at this run's
ticks-per-wave** · ⚑ **effective `n` (§ C.8)**. A diagnostic printed without those six is a number
without an instrument. ⚑ **And where a width used to print, the face reads `[width VOID @ re-base
— P-a's widths derive from the v3.3 sealed cells]`.**

**CLASS I · MECHANISM — the per-wave restatements** (`TA-B-16` · `TA-B-17` · `TA-B-18` · `TA-B-19`).
Released / stationary / motion-suppressed ticks **per wave**, plus **ticks per wave** itself.
Numerator and denominator both per-wave ⇒ **IMMUNE by construction**, except `TA-B-19`, which
**IS the dilution factor**. ⚑ **Widths OWED and NAMED AND EMPTY — and `TA-B-16` must SPLIT into
`16a`/`16b` before a width over it is honest (`P-a` Add. 4 § A4.4: its numerator has TWO GRAINS and
the port's mixture is 100 % of the one that is NOT scale-free).** ⚑ **The constructions were
verified computable on both sides at v1.5 and three of gamora's published figures reproduce exactly
from the seal; nothing about the re-base touches the CONSTRUCTION.**
⚑ **The clause that must travel with them: SCALE-FREE BY CONSTRUCTION, NOT BY MEASUREMENT. The
oracle's calibration range (ticks-per-wave ∈ [106, 185], a 1.75× span) cannot test the claim.
`TA-B-19` is the row that can falsify it, and that is why it exists.**

**CLASS II · CARRIED AS WRITTEN — the per-tick originals, with the confound printed.**
`TA-B-02` · `TA-B-03` · `TA-B-04` · `TA-B-05` · `TA-B-07` · `TA-B-08` · `TA-B-09` — **7 ids.**
Each prints its **grain pair and confound direction** (`TA-B-02` YES/UP · `TA-B-03` YES/UP ·
`TA-B-04` YES/UP-to-clip · `TA-B-05` WEAK/INDETERMINATE · `TA-B-07` YES/DOWN · `TA-B-09` YES/DOWN ·
`TA-B-08`'s **sign may survive, its margin 0.0048 does not**), its **calibration range**, and the
**realised dilution factor** from `TA-B-19`.

⚑ **TWO SENTENCES THAT MUST APPEAR VERBATIM WHEREVER THESE ARE PRINTED:**
1. ⚑ ***"`TA-B-02` and `TA-B-07` are ONE ROW WITH A SIGN FLIP (`released/D ≡ 1 − uptime`, exactly).
   They are not two pieces of evidence."***
2. ⚑ ***"`TA-B-02`'s green in run #1 rested on the CLIP. The unclipped upper bound was `0.974330`
   and the port's `0.975570` EXCEEDED it by `+0.001240`."*** *(Past tense at v1.6 — the width is
   void. No width was adjusted to produce that sentence and none may be adjusted to erase it.)*

**CLASS III · `TA-B-06` — the plant ratio.** v1.5 recovered the definition from the seal and it
reproduces on all five salts: `plant_ratio = (stationary ticks in the window / window length in
ticks) ÷ (stationary ticks over the whole fight / D)`, **window = 61 ticks per wave** (5.0 s at
12.2 ticks/s), anchored at wave start. ⚑ **The port computed a DIFFERENT STATISTIC — the fraction
of 5-second windows containing a plant — so `TA-B-06`'s red in run #1 localises nothing.**
**Mandatory on the face, both sides: `window_coverage = 61 / (D / n_waves)`.** ⚑ **The residual
confound is DECLARED, not repaired: the statistic is immune and its WINDOW is not, because 5.0
seconds is absolute time. An elastic window would make five seconds mean different things on the
two sides.**

**CLASS IV · `TA-B-15` — SUBSTRATE, NOT PORT** *(carried; promotion permanently barred)*.
It measures the **substrate**: the NO-DATA fraction is a property of *the records `POOL-466` happens
to contain*, which the port neither chooses nor influences. **A fidelity band over it would score
the port on the oracle's data coverage.**
⚑ **INVERTED AT v1.6. Both reference points are `0.0000` — analytic and sampled.** ⚑ **ZERO IS NOW
THE EXPECTATION AND A NON-ZERO IS THE ANOMALY**, which is the exact reverse of v1.5's
*"a salt reporting ZERO is the anomaly."* **It prints, per arm per salt: the count, the fraction of
bodies, the pool-pick count, and both reference points labelled as what they are.**

**CLASS V · NON-DISCRIMINATING BY CONSTRUCTION** — `TA-B-01` · `TA-B-13` · `TA-B-14`.

| id | why it cannot discriminate | mandatory sentence |
|---|---|---|
| `TA-B-01` terminal wave | its band **admits every arm in the seal, including the `M-POL` G5 control the run built to be different** | ⚑ ***"`BAND / NON-DECISIVE / REPORT-ONLY`. A terminal wave inside or outside this band is not evidence of fidelity either way."*** ⚑ **AND THE NEW REFERENCE POINT (§ A.5): *"the oracle's sealed `M-POL-2` arm terminates at `[156, 152, 151, 151, 156]`, `player_death` on every salt. A port that clears to wave 160 has not survived a hard board; it has failed to be in one."*** |
| `TA-B-13` `max_body_radius_m` | an **extreme over n draws**, not a mean; the per-salt sample is **degenerate (4 of 5 identical)**; **its own t-band REJECTS the oracle's observed maximum** | ⚑ ***"A band that rejects the oracle cannot grade a port."*** Its falsifying power sits entirely in `TA-X-10` / `TA-X-11`, both EXACT |
| `TA-B-14` vetoes / occupancy | raw counts, oracle values **0–2**, no denominator | ⚑ ***"This is the counter that carries `TA-X-06`'s ENTIRE MECHANISM, and it is the one the prereg declined to band."*** § F.2e |

**CLASS VI · NO ORACLE SIDE** — `TA-B-10` · `TA-B-11` · `TA-B-12`.
`TA-B-10` stays **UNGRADEABLE at the per-wave-vector grain** (the seals carry no per-wave
`duration_s`); its aggregate form **is** `TA-B-19`. `TA-B-11` (arrival latency / co-arrival) is
absent from both seals **and from the port** — no arrival limb exists. `TA-B-12` (intake / leech
per tick) returns **zero keys on both seals** — ceiling `C-e`, and ⚑ **`TA-X-28` now grades the LAW
even though no row can grade the MAGNITUDE.**

### F.4 · Emitted, not graded

Per-registered-site draw counters (**29 live sites**; they localise nothing without S5) · the
tick-resolution HP trace.

### F.5 · ⚑ REPORT-FACE RULES — **ten**

1. **Every diagnostic prints `value @ coverage k/89`** — a **rule** coverage (`P-1`), *not* a
   population coverage (§ C.5).
2. **EVERY ROW KEYED BY WAVE PRINTS ITS OWN COVERAGE.** Coverage is **not uniform across waves**.
3. **AND IT PRINTS THE NUMBER OF POOL PICKS BEHIND IT, NOT ONLY THE BODY COUNT.** Under clustering
   — median 3 bodies per pick, max 9 — the body count **overstates the evidence by the design
   effect.** *A wave at 0.30 over 4 picks and a wave at 0.30 over 20 picks are not the same claim.*
4. **Wave labels are not assumed to be total.**
5. **EVERY DIAGNOSTIC PRINTS ITS GRAIN PAIR, ITS CALIBRATION RANGE, AND THE REALISED DILUTION
   FACTOR** — *"numerator per-wave / denominator per-tick · derived at ticks-per-wave ∈ [106, 185]
   · realised ⟨f⟩ · dilution ⟨d⟩×"*. ⚑ **And, at v1.6, `[width VOID @ re-base]` where a half-width
   used to be.** For `TA-B-16…19` the field reads *"SCALE-FREE BY CONSTRUCTION; the calibration
   range [106, 185] cannot test this."*
6. **EVERY EXACT ROW SATISFIED BY AN ABSENCE PRINTS THE ABSENCE.** A `GREEN-BY-CONSTRUCTION` or
   `GREEN-VACUOUSLY` verdict must name **what is absent** and **why the other value is
   impossible.** Instances: `TA-X-11` (*a port with no wall also scores zero*) · `TA-X-12` (aprons
   **absent**, not present-at-zero) · `TA-X-19` (**no arrival limb at all**, which also means
   `TA-X-21`'s `CEIL` assertion is asserted in a vector table and never exercised) · `TA-X-15(b)`
   (the stagger is **unrepresentable**, not absent) · `TA-X-17` (green-by-construction with a named
   mechanism) · ⚑ **`TA-X-25(a)`, NEW — satisfied over an EMPTY SET.**
7. **THE SUSTAIN SENTENCE — AMENDED, BECAUSE THE RISK INVERTED.** v1.5 required *"a green T-A is
   currently compatible with an unkillable player."* ⚑ **At v1.6 the mandatory sentence is:**
   ⚑ ***"`leech` and `intake` still have no oracle side in the seals (`C-e`). What HAS been measured
   off-seal is that the oracle's sealed stack KILLS THE PLAYER AT WAVES 151–156, four or more waves
   earlier than the referent's 160. The two replicas bracket the referent from opposite sides: the
   port ~15× LOW on intake per body, the oracle ~1.9× HIGH. A GREEN T-A IS COMPATIBLE WITH BOTH."***
8. ⚑ **NEW — THE ORACLE'S OWN HOLES ARE NAMED ON THE FACE AND GRADED BY NOTHING.** Any report
   carries, verbatim:
   ⚑ ***"Three declared absences are the ORACLE's holes and not the port's defects. No row grades
   them and a port that does not implement them is CORRECT: `ABS-NINE-WINNER-SURFACE-HONEST-FAILS`
   (13 slots — 12 `NO-DAMAGE-DECODED`, 1 `RANK-UNASSIGNED`) · `ABS-GLOBAL-MAGNITUDE-FOLD-INERT-RECORDS`
   (29 records, 0 of them inside waves 151–160) · `ABS-C-I14-2-SOURCED-UNFOLDED` (a sourced wave-level
   physical modifier, ≤ 2.2 % pooled and exactly ×1.000 at w159/160, unfolded on BOTH sides)."***
   ⚑ **Stated at the prereg, because after a graded run it reads as an excuse.**
9. ⚑ **NEW — THE STARVED CHANNEL, TWO NEGATIVES.** Any report carries, verbatim:
   ⚑ ***"The resume cadence of a starved channel is DECLARED, not sourced (`ABS-CHANNEL-STARVED-RESUME-CADENCE`;
   closer = Matt-to-do T32; the alternative `STUTTER_WHILE_HELD` is `STRUCTURAL-INFERRED` and is NOT
   adopted). And the oracle's starvation TERMINATION — the `break` at `run.py:2137`, reached through
   `refuses_activation` at `:2133` — is `UNSOURCED-INCUMBENT`: behaviour written by default long before
   the question was asked, carried unchanged and ratified by nothing. NO ROW GRADES THE PORT AGAINST IT."***
   *(Corrigendum-forward: KP-95 cited `run.py:2103`; that was the pre-fold file. The site at engine
   HEAD `29a66055` is `:2133`/`:2137`, re-derived here.)*
10. ⚑ **NEW — WHAT A GREEN T-A DOES NOT BUY.** Any report, **including a passing one**, carries:
    ⚑ ***"T-A compares the port and the oracle under the SAME scripted pilot and the SAME folds. It
    therefore cannot see the occupancy gap (`N` 1.43–2.30 across pilots against the referent's
    0.72–1.84), cannot see the oracle's ~×1.9 over-lethality (`C-i`), and cannot see anything T-C
    is for. A PASS here means the replica matches the reference. It does not mean the reference
    matches Matt's video."***

---

## § G · FAIL TAXONOMY, THE T-B QUOTING CAP, AND THE GRADED-RUN CAP

| verdict | antecedent | consequence |
|---|---|---|
| **`STRUCTURAL`** | **≥ 1 EXACT row RED** | port is wrong; **no W4 until repaired**; ⚑ **consumes one of the two attempts**; ⚑ **and L2 applies: attempt 2 fires only after jack-ryan Gate-2 PASSes the repair** |
| **`INDETERMINATE`** | 0 EXACT red, **≥ 1 EXACT UNGRADEABLE** (incl. `P-1`, `P-2`, `P-3`, `P-4` or ⚑ `P-5` red) | ⚑ **does NOT consume an attempt** — but nothing seals, and the run is no further forward |
| ~~`STATISTICAL`~~ | ⚑ **RETIRED at v1.5 under F5. Not revived** | — |
| **`PASS`** | **all EXACT green; none UNGRADEABLE** | ⚑ **`PASS @ coverage k/89, 28/28 EXACT rows green, TA-X-06 UNGRADEABLE-declared (Q83(b)), dilution ⟨d⟩×, substrate_epoch v3.4.2/5cab7433…` — never unqualified** *(⚑ v1.7: 28/28, was 29/29)* |

**Order:** `STRUCTURAL → INDETERMINATE → PASS`, stop at the first hit. ⚑ **No diagnostic appears in
any antecedent.** **A GRADED RUN** = one execution of the 5 × 5 matrix producing a conforming
verdict file; a port repair between attempts does not create a third. **No post-hoc widening, by
anyone.**

⚑ **v1.7 — A DECLARED ROW IS NOT AN UNGRADEABLE EXACT ROW.** `TA-X-06` is `UNGRADEABLE-declared`
(§ F.2e). It appears in **no** antecedent above: it cannot produce `STRUCTURAL`, it cannot produce
`INDETERMINATE`, and it cannot block `PASS`. **A grader who reads the declaration into the
`INDETERMINATE` row has re-imposed the gate Matt removed.**

⚑ **AND THE SEAL, WHICH IS A DIFFERENT AND STRICTER THING THAN A `PASS` (Q87):**
`PASS` (all EXACT green) **AND** coverage **89/89 mapped** **AND** T-B **reported as DIAGNOSTIC**
**AND** **Matt's T-C yes**. ⚑ **A `PASS` is necessary and not sufficient. Three of the four
conditions are mechanical and the fourth is Matt's, and no agent may substitute for it.**

**Verdict file** `kc2play.ta_verdict.v1`:

```
prereg_version                    : "v1.7"            ⚑ v1.7
prereg_sha256                     : <this file, derived at emission>
⚑ substrate_epoch                 : "v3.4.2 / model 5cab7433… / reference 978f54ab…"
band_widths_sha256                : 1c80f080…          (P-a — CONSTRUCTIONS ONLY; every width VOID)
galadriel_note_sha256             : d48512aa…          (P-b, MOVED — the full re-read)
galadriel_expected_values_sha256  : a8b85331…          (P-c)
galadriel_release_labels_sha256   : 15dace60…          (P-d)
⚑ roster_rebase_prereg_sha256     : 4b7b78c8…          (P-e — governs TA-X-25 / TA-B-15)
⚑ v3p3_prereg_sha256              : 27fc5937…          (P-e′, lineage only)
⚑ model_pack                      : {dir: "…v3p4p2-20260929_063506", digest: 5cab7433…, files_verified: 17}
⚑ reference_pack                  : {dir: "…v3p4p2-20260929_063506", digest: 978f54ab…, files_verified: 7}
⚑ cross_pin_verified              : true
leech_resistance_csv_sha256       : cb6a008b…          (P-i)
⚑ anchor_timing_csv_sha256        : <P-k, derived at emission>
register_sha256                   : <v0.3's MACHINE form, emitter-derived — never this document's file hash>
preconditions.P1_coverage         : {"mapped":89,"total":89,"unmapped":0,"refusals":<n>}
preconditions.P3_roll             : {"population":"POOL-466","cardinality":466,
                                      "law":{"alternative":"WEIGHTED:pool_weight","name":"UNIFORM:randrange"}}
preconditions.P4_pack             : {"model":<dir>,"reference":<dir>,"files_verified":24,"mismatches":0,"cross_pin":true}
⚑ preconditions.P5_folds          : {"winner_surface":"ARMED",
                                      "per_cast_energy_column":"PARENT_PLUS_MODIFIER",
                                      "insufficient_energy_policy":"REFUSE","regen_ungated":true,
                                      "global_magnitude":"ARMED_UNCONDITIONAL",
                                      "measured_board_attached":true}
⚑ declared_ungradeable            : [{"id":"TA-X-06","authority":"Q83(b) / KP-110","graded":false,
                                       "relation_per_salt":<W1 vs M-POL-2 digest pair>}]   ⚑ v1.7
v0_limb_set                       : <diffed line-by-line against V0>
join_consumption_audit            : [{join_id, consumed, call_site | declared_unconsumed_ref}, …]
⚑ gmag_conformance                : {"pred_gmag_whole": true, "attr_limb": 193, "attr_lap_o": 154,
                                      "own_limb": 527, "own_lap_o": 104, "inert_records": 29,
                                      "terminal_multiplier": {"w159": 3.406, "w160": 5.418}}
⚑ leech_law                       : {"n_leech_target_caps_applied": 0, "n_leech_tick_caps_applied": 0,
                                      "scope": "ALL_BODIES_IN_DISC", "weapon_portion": 0.57}
⚑ pursuit                         : {"d_engage_m": 2.4, "source": "arena.json", "n_halted_beyond": 0}
draw_site_census                  : {registered:29, short_circuits_found:0, degenerate_pairs:"97/139"}
conservation                      : {residual_abs, residual_rel, offered, n_terms_accumulated} per cell
⚑ nodata                          : {"refused":0, "nodata_spawn_inert":0, "measured_inert_spawn":<n>,
                                      "measured_offense_spawn":<n>, "bodies_spawned":<n>}  per arm per salt
⚑ diagnostics                     : [{id, value, coverage, grain_pair, calibration_range, dilution,
                                      effective_n, width: "VOID@rebase"}, …]
⚑ oracle_holes_printed            : true    (§ F.5 cl. 8)
⚑ starved_channel_printed         : true    (§ F.5 cl. 9)
⚑ t_a_limits_printed              : true    (§ F.5 cl. 10)
```

**T-B quoting cap — three refusal conditions, UNCHANGED:** **C1** verdict file absent /
unparseable / **any pinned sha mismatched** *(which now covers both packs, `P-i` and `P-k` without
adding a condition)* · **C2** `verdict ∈ {STRUCTURAL, INDETERMINATE}` · **C3** coverage not
89/89-mapped.
**"A fidelity figure"** (mechanical): a row pairing a twin statistic with a referent statistic; or a
ratio/percentage/delta/residual/score between them; or `fidelity`/`faithful`/`accuracy`/`match`/
`agreement`/`% of referent` in a label. ⚑ **`TA-B-15` is expressly NOT one** — it pairs a twin
statistic with a **substrate** statistic.
**Degraded behaviour:** raw twin-side statistics only, each with its own denominator and window; a
**banner before** the statistics naming the condition; **non-zero exit.**

### ⚑ G.1 · THE GRADED-RUN CAP — **RESET, TWO ATTEMPTS, AND THE FOUR GUARDS ARE MET**

⚑ **Matt, Q85, 2026-09-28: RESET, two attempts.** v1.5 § G.2 refused to reset the cap for itself
and § H.4 named the four conditions under which a reset would be legitimate. **All four hold:**

1. ⚑ **The reset was ruled FROM OUTSIDE THE RUN.** *"The reset came from outside the run, as it had
   to"* (KP-83). **v1.5 did not reset its own cap and was right not to.**
2. ⚑ **This prereg is COMMITTED ALONE, with every pin re-derived, BEFORE anything is graded against
   v3.4.2.** D4. **A prereg written after seeing the new reference's numbers is not a prereg.**
3. ⚑ **The v1.4 and v1.5 attempts STAY ON THE RECORD** as attempts against the **v3.3** reference,
   with their verdicts, and this header names them. **A reset that erases its predecessors is an
   amnesia.**
4. ⚑ **`substrate_epoch` is declared in every artifact that crosses the boundary** (§ C.7), so the
   two-epoch rule is mechanical rather than remembered.

⚑ **v1.7 — Counter at v1.7: `0` of `2`. The allowance ATTACHES TO v1.7; none was spent under
v1.6, because no graded run executed against it (W3 held for `Q83(b)`, KP-106 / KP-107).** ⚑ **And L2 sits on top of it: the second attempt fires only after
jack-ryan Gate-2 PASSes drax's repair of an attempt-1 STRUCTURAL red.** A repair without a passed
gate does not buy the attempt; an `INDETERMINATE` does not consume one but buys nothing either.

---

## § H · WHAT IS OWED BEFORE W3, AND WHAT IS OWED AFTER

**Before the graded run (blocking):**

| # | owed | owner | why it blocks |
|---|---|---|---|
| **H-1** | **the port onto v3.4.2** — pack swap, the global-magnitude fold per the `Z5` law, `.app` rebuilt and its header `pack_digest` read by RUNNING the exported binary | **drax (W2f)** | ⚑ **`P-4` is RED until the `.app` reports `5cab7433…`, and `TA-X-29` cannot be graded against a port that has not lifted the fold** |
| **H-2** | **`TA-X-01`'s repeat-probe emission, naming its arm and salt** | drax | ⚑ **`UNGRADEABLE` trips the cap as hard as a red** |
| **H-3** | **`TA-X-16`'s filtered-key counter emission** | drax | *a filter with no counter is indistinguishable from a filter that never fired* |
| **H-4** | **the `z3` `M_inst` CHECK asserted before `own_add`** | drax | `TA-X-29(c)`; a wrong pool makes every folded body wrong by that difference |
| ~~**H-5**~~ | ~~`Q83(b)` — Matt's one word on `TA-X-06`~~ | **Matt** | ⚑ **v1.7: DISCHARGED — RULED YES, KP-110; carried by this version (§ 0, § F.2e).** *(v1.6: "under Q87 this blocks the seal")* |

**Not blocking, and named so they are not lost:**
`TA-B-16…19`'s widths (and the `16a`/`16b` split) · `TA-B-06`'s corrected port-side emission ·
`P-e′` Addendum § 3's body-grain coverage fractions · the `CHARTER_DENOMINATOR` rename and the
charter's live `72` / `229` / `297` / `302` (`OQ-7`) · `wendigo_frenzyswipes` (six ranks, zero
decoded, on an armed basic attack of a wave-160 nemesis — **commission candidate, registered**) ·
`pet_limit` `DECLARED-UNRESOLVED` (`wendigo_summonwraiths` permits **24** wraiths, not 12) ·
`load_pet_contracts()`'s missing path-duplicate dedup (harmless only incidentally) · the
`chainInitial`/`chainNext` enumeration gap in `x8` for the other 457 records · 15 committed files
carrying DBR paths with no provenance column (`CORROBORATED-NOT-PROVEN`; **the cheap instrument is
a provenance column, not a re-derivation**) · E/W shield-handedness (`R-C8-7`, **deferred by Matt**,
flagged so nobody re-files it).

---

## § I · OPEN QUESTIONS — **one lean each**

**OQ-1 · ⚑ `TA-X-06` — `Q83(b)` IS OPEN AND IT NOW BLOCKS THE SEAL, NOT JUST THE ROW.**
⚑ **v1.7: RESOLVED BY RULING — Matt, `Q83(b)` YES, KP-110. The lean below was ruled as written for
the instrument; it is retained verbatim as the record.**
→ ⚑ **LEAN: reclass to `UNGRADEABLE-DECLARED`, in v1.4 FOR THE RECORD and in v1.5 / v1.6 FOR THE
INSTRUMENT, in one word.** The row is **unfalsifiable in the honest direction** — the only route to
green is inventing a veto rule nobody wrote — and it was classed EXACT while the only mechanism
making it true was classed report-only **seven lines away in the same file.** ⚑ **At v1.5 this was
bookkeeping. Under Q87 ("all EXACT rows green") it is the difference between a sealable referent
and one that cannot be sealed on a correct port.** ⚑ **Nothing is rescued by the reclass: v1.4's
`STRUCTURAL` survives the row's removal, `TA-X-07` was independently red and `TA-X-01`/`TA-X-15`
independently UNGRADEABLE.** **v1.6 carries it AS CLASSED precisely so this document does not moot
the question.**

**OQ-2 · ⚑ `TA-X-25` WAS RE-AUTHORED BY ME, AND THE RE-AUTHORING IS THE ONLY PLACE IN THIS DOCUMENT
WHERE A ROW'S CLASS MOVED ON MY JUDGEMENT.**
→ ⚑ **LEAN: ratify the accounting-identity form.** The alternatives were (a) carry v1.5's clauses —
which **reds a correct port on every arm** (KP-80's own finding) — or (b) strike the row, which
loses the config-leak check and the counter-presence check as well as the membership bit. ⚑ **The
identity form keeps everything that survives the substrate and grades nothing that does not.**
**It is also my own recorded recommendation (`OQ-B` of the rebase note), routed to the conductor
before this document existed, so it is adopted rather than invented here.** ⚑ **jack-ryan's
pre-read should test exactly this.**

**OQ-3 · ⚑ THREE NEW EXACT ROWS ENTER A PREREG WHOSE CAP JUST RESET.**
→ ⚑ **LEAN: keep all three.** Each covers a defect that cost this lap real time and that **no
existing row catches**: an uncapped-leech assumption that would have been "fixed" by a fitted
constant (`TA-X-28`), a partial fold that reports itself whole (`TA-X-29`), and an 80.5 % pursuit
divergence a census row read `IMPLEMENTED` through (`TA-X-30`). ⚑ **The honest counter-argument is
that a bigger EXACT set makes a `PASS` harder and Q87 makes a `PASS` the seal. That is the point:
a seal on an instrument that cannot see the thing that went wrong is not a seal.**

**OQ-4 · ⚑ `TA-B-16…19`'s WIDTHS ARE STILL OWED AND NOW SO IS EVERY OTHER WIDTH.**
→ ⚑ **LEAN: a new `P-a` addendum, derived from a NEW sealed set, AFTER the graded run — and it
blocks nothing, because under F5 no diagnostic gates anything.** ⚑ **AND THE ORDER MATTERS: minting
widths from cells that do not yet exist is impossible, and minting them from the v3.3 cells would
be exactly the cross-epoch comparison § C.7 forbids.** `TA-B-16` must SPLIT first (`16a`/`16b`).

**OQ-5 · ⚑ `P-e′` ADDENDUM § 3's COVERAGE FRACTIONS — PARTLY ANSWERED, PARTLY STILL OWED.**
→ ⚑ **LEAN: the MEMBER-grain fraction is answered (`128/466 = 0.2747` → `464/466 = 0.9957`, and the
NO-DATA fraction is `0`); the BODY-grain fraction over waves 151–160 is still owed and needs a run,
not a note.** `E[bodies] = 126.08` at p06 OFF is **confirmed unchanged** because `waves.json` is
byte-identical. **`TA-B-15` prints `0.0000` and never `0.3828`.**

**OQ-6 · ⚑ THE `limitN` QUESTION IS UN-MEASURED, NOT ANSWERED.**
→ ⚑ **LEAN: measure it now — the re-base has happened and that is when it was going to be cheap.**
`C-c` was struck because the shortfall it was compared against (`183.58`) does not reproduce, **but
"the comparison was void" is not "the cap has no effect", and collapsing those two would be the
same error in the opposite direction.**

**OQ-7 · THE CHARTER STILL CARRIES `72` AND KP-26's `229 / 297 / 302`, LIVE-TENSE** (§ 4.3 / § 4.4 /
§ 3 F1 / § 9), and `kc2rt_coverage.gd` still names its constant `CHARTER_DENOMINATOR`.
→ **LEAN: annotate all of them forward in one pass, in strike-through form. Propagation, not a new
ruling — no Matt.** ⚑ **THIRD VERSION OF THIS PREREG CARRYING IT. The sweep's own finding is
unchanged: the prereg and register were never the carriers; the charter is, and every hour these
figures still cost is charged entirely to it.**

**OQ-8 · ⚑ THE ARRIVAL LIMB IS ABSENT FROM THE PORT AND `TA-X-19` IS GREEN ABOUT IT.**
→ ⚑ **LEAN: accept the print rule (§ F.5 cl. 6) and route the arrival limb as a real fidelity gap,
separately from T-A.** The oracle has a deferred-arrival limb; `Kc2RtLaws.arrival_tick` has **zero
call sites**, which also means **`TA-X-21`'s `CEIL` assertion is asserted in a vector table and
never exercised.** **That is not a reporting gap; it is a missing limb wearing a green row.**

**OQ-9 · ⚑ NEW — `TA-X-09` GRADES 9 OF 29 NORMATIVE TEST VECTORS, AND THE 20 IT SKIPS GOVERN THE
MONSTER-TO-PLAYER MITIGATION ORDER.**
→ ⚑ **LEAN: declare at v1.6 (done — ceiling `C-h`), widen at the next version, NOT here.** ⚑ **The
20 sit on the rule under which the entire intake thread is argued — `C-6`, `C-8`, `C-I14-2`, the
×1.9 bracket. A port that reproduces 9 of 29 vectors and diverges on the mitigation order would
pass `TA-X-09` and be wrong about every hit the player takes.** ⚑ **I am not widening it in the
session before a graded run, because an author who grows his own instrument at the last moment has
built a goalpost, not a gate. But it should be the FIRST row the next version adds.**

---

## § J · ⚑ THE DISCIPLINES THIS LAP PRODUCED

> ⚑ **THE GRAIN LAW** *(carried; § C.6)* — **before banding a rate, name the grain of its numerator
> and of its denominator separately, and state the range of the ratio between them over which the
> band was calibrated.**

> ⚑ **THE EXPIRY CLAUSE, NEW** *(§ F.1a)* — **a structural row must name not only the mechanism that
> makes the other value impossible, but whether that mechanism is a property of the SYSTEM or of
> OUR OWN DECODE'S COMPLETENESS. If the latter, the row carries an EXPIRY and names the event that
> voids it.** ⚑ *`TA-X-25` cost this lap a re-authoring because nobody asked that question when it
> was admitted.*

> ⚑ **THE HONEST-`n` LAW, NEW** *(§ C.8)* — **the cell count is not the sample size. On any
> dimension the arm deltas do not touch, `n = 5`.** *(legolas F-3/F-4; routed to jack-ryan at this
> pre-read.)*

⚑ **The one-shape tally, now at SIX — a statistic correct in its arithmetic and wrong in the
population or the scale it ranged over:**

| # | instance | whose |
|---|---|---|
| 1 | **σ over 97 BODIES when the draws are over 23 POOL PICKS** — design effect `√(97/23) ≈ 2.05×`, `z` **4.72 → 2.30** | gamora |
| 2 | **`466 − |source|` — SUBTRACTION where it owed a SET INTERSECTION** | the conductor's |
| 3 | **`183.58`** — an analytic that does not reproduce from the pack; **1.46× the correct figure** | gamora |
| 4 | **THE PER-WAVE/PER-TICK CONFOUND** — bands calibrated at ticks-per-wave ∈ [106, 185], applied at 482.4 | gamora |
| 5 | **`mean(adcth_mult_COUPLED)` is `0.266406` over one population and `0.252215` over another** | surfaced by the conductor at v1.5 |
| ⚑ **6** | ⚑ **NEW, FOUND WHILE WRITING THIS FILE, AND IT IS THE SAME CLAUSE AS #5 — v1.5 named instance 5 and then MISLABELLED the population in the very clause it was warning about. `0.266406` is `BOTH-128` (decode coverage), not the armed set (122 at v3.3, 464 at v3.4.2).** ⚑ **Naming a defect class does not immunise the sentence that names it** | ⚑ **mine, on the conductor's text, found by re-deriving rather than carrying** |
| ⚑ **7** | ⚑ **AND ONE THAT IS NOT ARITHMETIC AT ALL — KP-95's *"the heal surplus is a MODEL gap… Matt's T-C would answer NO"* and KP-96's routing to the pilot both rested on a BARE stack with nothing armed, which I relayed as the oracle's behaviour without opening what it had armed. `[M-POL2]`'s own `terminals` array said `player_death` at 151–156 the whole time** | ⚑ **mine** |

⚑ **And the companion discipline, which is what keeps these findable:** `#79` / Law 3 — **no fitted
constants.** drax declined to fit a multiplier toward `183.58` on the grounds that *"one fitted to
reach 183.58 would be fitted against the very figure it must be independent of."* **The figure was
wrong.** ⚑ **`TA-X-28` is the same refusal made into a row: a leech cap would be a fitted constant,
and `n_caps_applied == 0` is the best-sourced line in the whole fold.**

⚑ **And the third, carried from KP-43 and amended into `#75` cl. 1(a):** ***nobody reads a pinned
revision, they read the file. A pin proves what a REVIEWER checked, never what a BUILDER used.***
⚑ **`P-4` + `P-5` are that remedy extended twice: the pack pin says WHICH ARTIFACT, and the fold
declaration says WHICH CONFIGURATION — and a default-OFF fold is the case where the artifact is
right and the answer is still wrong.**


---

*Filed 2026-09-29 by **gamora** (simulation + spirit-guide seam), Run KC2-PLAY SEAL LAP.
⚑ **v1.7 = v1.6 + ONE change: `TA-X-06` EXACT → UNGRADEABLE-declared, on Matt's `Q83(b)` (KP-110).
Every touched site is marked `⚑ v1.7` and listed at § 0.2; everything else is carried from v1.6
byte-for-byte in substance.** **v1.6 / v1.5 / v1.4 / v1.3 / v1.2 / v1.1 / v1.0 NOT edited.**
**v1.4's grade of record — `STRUCTURAL @ coverage 89/89` — does not move; nothing here regrades,
rescues, widens or reclassifies anything that was graded.** **Legal because Matt ruled `Q83(b)` and
no graded run exists against v1.6; Q85's two attempts attach to v1.7, `0` spent.**
**Every pin, both pack digests (re-computed from 17 + 7 members by the manifest's own law), the
documents of record and all three sealed-cell digests re-derived this session by `shasum -a 256`;
none moved since v1.6.** ⚑ **NO BAND WIDTH MINTED, AND EVERY EXISTING WIDTH STILL VOID.**
**`GM-OQ-1` (widening `TA-X-09`) and every other pending item deliberately NOT folded in (§ 0.3).**
**K-7 held** — the sealed cells were hash-verified only; none was opened for execution, re-run,
edited or moved.
⚑ **THIS FILE IS IMMUTABLE. Any change after a graded run exists against it is a HALT (`WARN-16`).**
**No production code. No dispatch. No push. D4 held: committed ALONE.***
