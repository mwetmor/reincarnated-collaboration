# KC2-PLAY · THE DIVERGENCE REGISTER — **v0.2**

> **STATUS:** CURRENT — **v0.2, 2026-09-20. SUPERSEDES v0.1 FORWARD.**
> **v0.1 (`540fd4b4`) and v0 (`1f5489af`) are NOT edited.** Superseded readings named in place at **§ A**.
> **Occasioned by:** jack-ryan's **W1 PRE-READ — NO-SEAL on pinning** (`agentic_orchestration/qa/findings/2026-09-20-run-KC2-PLAY-w1-preread.md`, `9e02f5b2`): **BLOCK-2** (the register cross-pins galadriel at a sha that **does not contain the content the register cites**) · **WARN-3** (the canonicalisation rule is ambiguous where it must not be) · **WARN-4** (KP-12's charter amendment is an **inference** from Matt's words) · **INFO-1** (the Companion line still names prereg v1.1).
> ⚑ **This fires before the first recording exists, so nothing un-pools** (§ F ¶3: EPOCH 0 = zero recordings). That window closes the moment a runtime writes a telemetry file.
> **Companion:** ⚑ `2026-09-20-kc2-play-ta-prereg-**v1.3**.md` (`66d2fc89`) — *v0.1 still named v1.1; INFO-1.* **No `DIV` row below is graded by T-A, by construction.**
> **Author:** gandalf (named sub-agent, `SPEC-AUTHOR`), Wave 1.

### ⚑ PINS — all four derived this session by `shasum -a 256`, never retyped

| # | artifact | **sha256** | what moved |
|---|---|---|---|
| **P-a** | `agentic_orchestration/gamora/notes/2026-09-20-kc2-play-ta-band-widths.md` | **`1c971da9d5f1e1cb3385965e44c38a6a32d1d3f24fdd260757bea748b0d0a121`** | ⚑ **Addendum 3** (`16d1b6a7`) — § E-3's coverage rule **72/72 → 89/89**. *The pre-read named `6709cfe6…`; Addendum 3 has landed since, and pinning a superseded state is the very defect being closed — so this pins CURRENT and says so.* |
| **P-b** | `agentic_orchestration/galadriel/notes/2026-09-20-kc2-play-w1-tb-expected-values-and-u-rider.md` | **`8186202cc0c78ae9ef428c57164fac35bd1adb0e14ec5310c395783361653158`** | ⚑ **BLOCK-2** — v0.1 pinned `0411e6b8…`, the **`10a85641`** state (16:24:39). The note was amended at **`b3f175ff`** (16:48:57, +38 lines). **v0.1 was committed at 16:55:26 — seven minutes after the amendment.** |
| **P-c** | `…/2026-09-20-kc2-play-w1-tb-expected-values.json` | **`a8b85331764ba3fe90f45cf7cd6f1a25f6dc0dae4a7e7fa555c487f0b153ea0b`** | ⚑ **NEW — consumed and pinned nowhere** |
| **P-d** | `…/2026-09-20-kc2-play-w1-tb-release-labels.json` (473 lines) | **`15dace604c8d5bb4888223a8b25a07a038bae44431ebd194d682545c0f29c58a`** | ⚑ **NEW — consumed and pinned nowhere; it does not exist at all at v0.1's pinned sha** |

---

## § A · CHANGE TABLE — v0.1 → v0.2

| # | clause | v0.1 | **v0.2** | reason | finding |
|---|---|---|---|---|---|
| 1 | **galadriel pin** | `0411e6b8…` | ⚑ **`8186202c…`** (P-b) | ⚑ **This is not staleness — the register consumed content that does not exist at the sha it pinned.** **DIV-04**'s *"σ = 48 ms, MEASURED"* is present **only** at `b3f175ff`; a grep of the pinned state returns **nothing**. **DIV-15** ships slot-indexed rows off a **file that does not exist** at the pinned sha. **The pin resolved to a document that falsifies two of the register's own rows.** Law 3 and *derived-at-use* exist so a reader can dereference a pin and **find the claim** | **BLOCK-2** |
| 2 | **the two JSONs** | ⚑ **pinned nowhere at all** | ⚑ **PINNED** — P-c, P-d | a consumed artifact with no pin sits outside the immutability guarantee entirely | **BLOCK-2** |
| 3 | **width pin** | `6709cfe6…` | ⚑ **`1c971da9…`** (P-a) | Addendum 3 (89/89) | BLOCK-1 |
| 4 | **Companion line** | prereg **v1.1** | ⚑ **prereg v1.3** (`66d2fc89`) | lineage only; folds into the re-pin | **INFO-1** |
| 5 | **§ F canonicalisation** | *"rows sorted by `id`, keys sorted, UTF-8 NFC, **whitespace collapsed**, no insignificant JSON whitespace"* | ⚑ **REPLACED by an exact eight-clause rule with a WORKED EXAMPLE** (§ F.1–F.2) | ⚑ *"Collapsed"* is ambiguous exactly where it must not be: **if collapse reaches inside string values, the hash is not over the emitted bytes**, and the emitter and the grader can implement it differently — at which point § F declares a perfectly good recording *"not comparable."* An EXACT-adjacent mechanism with an under-specified predicate | **WARN-3** |
| 6 | **KP-12 citation** | *(the register did not cite it)* | ⚑ **ADDED at § C.1, with the SAID / INFERRED boundary drawn explicitly and KP-14 named as the ratification** | Matt's verbatim carries the **depiction** requirement; it **does not narrow § 1's "no painted asset minting."** The conductor's narrowing is a *reasonable* reading and **KP-14 (*"agreed on interior nave"*) ratifies it downstream** — but *"Matt's word"* and *"inferred from Matt's word, later ratified"* are different claims. ⚑ **This is the distinction BLOCK-D was fought over and won at v0.2 of the charter; only the attribution boundary slipped, not the outcome** | **WARN-4** |
| 7 | **two-epoch statement** | declared | ⚑ **CONFIRMED and re-verified** (§ F.3) | asked at KP-5(10); the pre-read confirms it is buildable and that EPOCH 0's zero recordings are **recorded rather than left silent** | — |
| 8 | **coverage denominator** | 89 (carried from KP-9) | **89 — unchanged**, and § F's mismatch → `COVERAGE FAIL` fires at prereg **P-1** at 89/89 | — | BLOCK-1 |

---

## § B · INDEX — 15 DIV · 8 ND

| id | switch | class | status |
|---|---|---|---|
| **DIV-01** | arena wall — circle `R = 43.758…` m vs the video-measured ring at `u = 0.285` | DIVERGENCE | ACTIVE |
| **DIV-02** | spawn-pool DoT — `0.0` vs D-LIFT-1/2 | DIVERGENCE | ACTIVE |
| **DIV-03** | cast-interrupt — uniform 0.15 cancellation vs the per-skill flag | DIVERGENCE | ACTIVE |
| **DIV-04** | Type-B auto-resume under held RMB | DIVERGENCE | ACTIVE — ⚑ **its evidence is at P-b, not at v0.1's pin** |
| **DIV-05** | pilot — `DRIVE_TO_PACK` vs Matt's hands | DIVERGENCE | ACTIVE |
| **DIV-06** | bound-skill additions OFF vs ON; riders `PLACEHOLDER-INERT` | DIVERGENCE | ACTIVE |
| **DIV-07** | Banner **placement** (magnitude **×1.0319** is MODEL-BOUND, not a divergence) | DIVERGENCE | ACTIVE |
| **DIV-08** | summons presentation — no health bar, no view-side `hp` | DIVERGENCE | ACTIVE |
| **DIV-09** | `u = 0.285` (`DR-u`) — the metre scale the oracle does not have | DIVERGENCE | ACTIVE |
| **DIV-10** | zoom register — `ZOOM-GD` 75.668 px/m default, `ZOOM-HOUSE` 160.394 toggle | DIVERGENCE | ACTIVE |
| **DIV-11** | player kinematics at render rate, sampled per tick | DIVERGENCE | ACTIVE |
| **DIV-12** | one life · restart key · scope window | DIVERGENCE | ACTIVE |
| **DIV-13** | entry state — **resumes `cp150`, opens at 151** | DIVERGENCE | RULED, veto-open (Matt at G-IMG) |
| **DIV-14** | potion agency — ORACLE auto-fires at **θ 0.2297**; PLAY manual | DIVERGENCE | RULED, veto-open (the key is F3's = Matt's) |
| **DIV-15** | bar-slot skill **names** `DECLARED-not-decoded`; T-B rows slot-indexed | DIVERGENCE | ACTIVE — ⚑ **its source file is P-d, which does not exist at v0.1's pin** |
| **ND-01** | fire-time resolution — strafing does not dodge | ND + confound | CARRIED |
| **ND-02** | no player crit | ND + confound | CARRIED |
| **ND-03** | base cooldowns; CDR not recovered | ND + confound | CARRIED |
| **ND-04** | **ONE** known-bad live limb (`LifeMonitorLimb.POLL_AT_SLOT`) | ND + confound | CARRIED (v0.1 corrected 3 → 1) |
| **ND-05** | `health_max` constancy (`D-Q1` / B-18) | ND + known model gap | CARRIED |
| **ND-06** | spawn scatter — polar disc in both; the pack says box | ND + pack trap | CARRIED — closed in T-A by `TA-X-17`/`TA-X-18` |
| **ND-07** | `hit_test_model` — pack says `"point"`; both run the 3.0 m disc | ND + pack trap | CARRIED — half-closed by `TA-X-20` |
| **ND-08** | monster-side mitigation | ND + **RESOLVED** | RESOLVED at v0.1 — the row that moved the hash |

*Every row's text, tests, expected directions and handoff sentences carry unchanged from v0.1 except where § A names a move. The two rows whose EVIDENCE moved are below.*

---

## § C · THE ROWS WHOSE SOURCES ARE NOW CORRECTLY PINNED

### DIV-04 · Type-B auto-resume — the evidence lives at P-b

**ORACLE:** no such mechanism — the sim has no held-input notion at the fight layer (`ChannelMachine` is not used by `run.py`; only `compose_damage_basis, tick_period_s, ticks_per_s` are imported).
**PLAY:** **Type-B releases AUTO-RESUME while RMB remains held; Type-A resumes on input only.** `channel_held` sampled as a **LEVEL, never an edge**.
**Authority:** KP-1 (conductor ruling **from measurement**, veto-open), Matt-accepted at KP-2 L5. The load-bearing leg is the **within-subject contrast**: the same hand, same fight, gave Type-A **IQR 0.62–1.56 s, max 3.50 s** (n = 11) against Type-B **median 0.60 s, IQR 0.55–0.63, range 0.53–0.67** (n = 8).
⚑ **`σ = 48 ms, MEASURED` (KP-10) — and that sentence exists only at P-b (`b3f175ff`).** It confirms Gate-1 **WARN-17**'s strike: a 0.14 s range over n = 8 is *ordinary* reaction-time variance, so **"a human cannot hold that spread" was always an overstatement, and the conclusion rests on the contrast, not on an impossibility.** All five release reproductions check exactly.

### DIV-15 · Bar-slot skill names — the source file is P-d

**ORACLE:** the sim casts no bar skill by name; there is no naming surface.
**PLAY:** the HUD needs tooltips, so slots carry names — **and the measuring lap forbids naming them.** T-B interrupt rows ship **SLOT-INDEXED** off ⚑ **P-d, `…-w1-tb-release-labels.json`, 473 lines — a file that does not exist at v0.1's pinned sha at all.**
⚑ **What this does NOT touch:** the `interrupts_channel` **flag values** are model-grade and **D-CP2-2 stands** — *the values are model-grade while the skill attachment is a declaration.*
**Tested:** every T-B row emits a slot index; a name never appears in a graded row, only in a tooltip.

### § C.1 · ⚑ THE ARENA PLATE'S SUBJECT — what Matt SAID, what was INFERRED, and where it was ratified

*Cited here because DIV-01's plate is the object it governs, and because the register is where a claim about authority has to be exact.* **It is NOT a `DIV` row:** the plate's *art* is FREE ART under the geometry-true clause, and a register enumerates **switches**, not depictions. The geometry is asserted either way (`R2D-6`).

| | |
|---|---|
| ⚑ **What Matt SAID** (KP-12, verbatim) | *"Will we re-use the same art for both the 8 % and 17 % versions?"* · *"Can you please have Astra produce one image at the start of the burst and pause, sending it to me for style/register review? It needs to match to our exact existing cliffside 2D art scene but it should represent the cathedral from that scene."* |
| ⚑ **What the conductor INFERRED** | that § 1's **"no painted asset minting"** is **narrowed** — one painted arena **PLATE** in scope, in the cliffside's exact H1 register, depicting the burning gothic cathedral of the `far_ruins` layer. ⚑ **Matt's words carry the DEPICTION requirement; they do not narrow the asset-minting clause.** The reading is reasonable; it is a reading |
| ⚑ **Where it was RATIFIED** | **KP-14, Matt verbatim: *"agreed on interior nave."*** The plate is the nave from inside — ring = nave walls, four islands = fallen pillar bases, six pools = something burning through the floor; the `far_ruins` exterior is the building you walked toward |
| **Why the distinction is kept** | ⚑ *This is the distinction **BLOCK-D** was fought over and won.* The outcome is right and unchanged; only the **attribution boundary** had slipped — *"Matt's word"* and *"inferred from Matt's word, later ratified by his word"* are different claims, and a register that blurs them teaches the next reader that they are the same |

---

## § D · WHAT IS NOT A REGISTER ROW

The 43-state AI graph (*the oracle never ran it*) · loot / levelling / meta / shop (F6) · Web / phone (F3) · pets (`L-83 D-3`) · celestial blessings (**a measured zero, both sittings**) · the three Crucible beacons' output (**they do not fire** in either config; cadence UNREAD; bias **away** from reaching 160) · ⚑ **the plate's painted subject** (§ C.1 — free art, not a switch).

---

## § E · THE FIVE ATTRIBUTION CLASSES AND THE DECISION PROCEDURE

**1 PORT** (bounded, not eliminated, by T-A) · **2 DECLARED DIVERGENCE** (a `DIV-nn` row; **includes `PLACEHOLDER-INERT` riders**) · **3 MODEL GAP** (the `ND` confounds) · **4 PILOT** · **5 INSTRUMENT**.

⚑ **Class 5's two founding cases:** **B-8 `frac_moving`** reads **0.883 / 0.705 / 0.6265** across three footage instruments — a **1.41×** spread, so ratios ship regardless (D-MPOL2-2). And ⚑ **the LIVE-MAX denominator law** (P-b): HP occupancy against `hp_max` **as read that frame** reproduces **42.84 %**; NOMINAL 20,005 gives **39.76 %** — **3.08 pp with no fight in it**; HP window **181.0 s** vs energy/motion **182.65 s**. *A grader that picks the wrong one manufactures a port defect.*

**The procedure — cheapest-falsifier-first, stop at the first hit.**
**Step 0 · INSTRUMENT** — does the row's denominator and window match the footage instrument's? *Test:* recompute the twin side on the footage instrument's construction.
**Step 1 · DECLARED DIVERGENCE** — a `DIV-nn` row whose **pre-registered direction matches the sign of the miss**? *Test:* **re-run under `ORACLE`** — buildable only because there is ONE runtime with two configurations.
**Step 2 · PORT vs MODEL GAP** — does the miss **survive under `ORACLE` with the scripted pilot**? **T-A row red → PORT · green → MODEL GAP · no covering row → `UNATTRIBUTABLE-PENDING`**, ⚑ **never PORT by default** (prereg § E lists which surfaces have no covering row — the board roll above all).
**Step 3 · PILOT** — appears only with Matt at the controls, vanishes under the scripted pilot in the same config.
**Step 4 · none of the above** → **a defect in this register.** File a row, re-hash, record why it was missed.
**Tie-break:** assign the class whose OFF-state test is **cheapest**, run it, record the result. **Never by narrative plausibility.**

> ⚑ *A green T-A row plus a T-B miss that survives under `ORACLE` with the scripted pilot is a **MODEL GAP**, not a port bug.*

---

## § F · THE REGISTER HASH

**Purpose.** Every telemetry header carries `register_sha256`. A recording whose header hash does not match the register in force at grading time **is not comparable, and the grader says so**.
**Ownership.** The runtime **EMITS** the machine form from its own configuration tables (#72). **This document is the labelled expectation checked against it, never substituted for it. A mismatch is a COVERAGE FAIL at prereg P-1 (89/89).**
⚑ *Known and expected:* the W1 skeleton currently emits **9** rows against this register's **23** (`TRANSCRIPT.md:72`). **The mismatch catch is working, and it will fire at T-0 unless the emitter is filled at W3.** Named so it is met as a scheduled event, not a surprise.

### F.1 · ⚑ THE CANONICALISATION RULE — exact, eight clauses (replaces *"whitespace collapsed"*)

1. **Shape.** The machine form is a JSON **array** of row objects, one per `DIV`/`ND` row, each with exactly the members `authority`, `class`, `direction`, `id`, `oracle`, `play`, `status`, `switch`, `test`.
2. ⚑ **EVERY VALUE IS A JSON STRING.** No numbers, no booleans, no nulls, no nested objects or arrays. *This clause exists to delete an entire failure class: with no numbers there is no number-formatting rule to disagree about (shortest round-trip repr, exponent form, `-0`, precision). A magnitude is carried as the string it is printed as.*
3. **Row order.** Rows sorted **ascending by `id`**, comparing Unicode code points.
4. **Member order.** Within each object, members sorted **ascending by name**, comparing Unicode code points.
5. ⚑ **String values are emitted VERBATIM** — the value's own code points, with **only** JSON's mandatory escaping (`"` → `\"`, `\` → `\\`, and U+0000–U+001F as `\u00XX`). ⚑ **NO whitespace collapse, NO trimming, NO case folding, and NO Unicode normalisation is applied at hash time.** *Normalisation is an **authoring** rule — values are authored in NFC — never a **hashing** rule. That separation is the whole of WARN-3: a hash must be over the bytes that were emitted, or emitter and grader can both be right and still disagree.*
6. **Whitespace.** **None** between tokens: separators are exactly `,` and `:` with nothing around them.
7. **Encoding.** UTF-8, **no BOM, no trailing newline.**
8. `register_sha256 = sha256(canonical_bytes)` — **full 64 hex in the telemetry header, 12-char prefix in prose, DERIVED AT USE, NEVER RETYPED.**

*Reference implementation, one line, and the grader must reproduce it byte-for-byte:*
`json.dumps(sorted(rows, key=lambda r: r["id"]), sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")`

### F.2 · ⚑ WORKED EXAMPLE — so emitter and grader cannot disagree

Two rows, deliberately supplied **out of `id` order** and with **member names out of order**, to exercise clauses 3 and 4:

```
[{"id":"DIV-02","class":"DIVERGENCE","switch":"spawn-pool DoT","oracle":"0.0",
  "play":"1/6 max pool per tick","authority":"D-LIFT-1/2",
  "test":"unit probe: 6 ticks from full","direction":"bimodal, mediated by occupancy","status":"ACTIVE"},
 {"id":"DIV-01","class":"DIVERGENCE","switch":"arena wall","oracle":"CIRCLE R = 43.758085029822276 m",
  "play":"video-measured ring at u = 0.285","authority":"R-KP-0c","test":"R2D-6 geometry-true",
  "direction":"tighter: shorter time-to-contact","status":"ACTIVE"}]
```

**Canonical bytes begin:**
`[{"authority":"R-KP-0c","class":"DIVERGENCE","direction":"tighter: shorter time-to-contact","id":"DIV-01","oracle":"CIRC…`

| | |
|---|---|
| **canonical byte length** | **497** |
| ⚑ **`register_sha256`** | **`bf648e51d14fc9313c4fce7774c5567628e1d3aca48d68c6a29d0d9225fe165e`** |

⚑ **Note what clause 5 preserves in this example, deliberately:** the interior spaces in `"CIRCLE R = 43.758085029822276 m"` and `"tighter: shorter time-to-contact"` are **kept exactly**. Under the old *"whitespace collapsed"* wording a conforming implementation could have squeezed them and produced a different digest — **two correct implementations, two hashes, and a perfectly good recording declared "not comparable."**
**An implementation that does not reproduce `bf648e51…` from the input above is non-conforming, and this is the test for it.**

### F.3 · ⚑ THE EPOCH STATEMENT — confirmed

1. **(c-2) HAS resolved** (ND-08). Its status moved `PENDING-W1 → RESOLVED`, the eHP semantic shift landed in **V6**, and **the register hash HAS moved.**
2. **EPOCH 1 begins at v3.2** — the lift complete at KP-8 (`kc2-lifted-rows-KC2PLAY-W1-v3p2-full-20260920_163932.json`, sha256 `e0117429…`). Every recording from this point carries a **v0.2** hash.
3. ⚑ **EPOCH 0 PRODUCED ZERO RECORDINGS — re-verified at v0.2.** No runtime has yet written a telemetry file, so the two-epoch rule has nothing to un-pool and **fires forward only.** ⚑ **This is also why BLOCK-2 was free to fix**: a pin correction after the first recording would have split an epoch; before it, it splits nothing. Recorded explicitly, because *"the rule was pre-declared and never needed"* is a disposition and **silence is not**.
4. **Forward:** any later `status` change re-hashes. Recordings under different hashes are **reported separately, never pooled**, and each wave seal records the hash before and after.

---

## § G · OPEN QUESTIONS — one lean each

**OQ-1 · The pin defect was mine twice in one wave** (v0.1's galadriel pin; v1.2's, in the change table that re-pinned the *other* file). → **Adopt a standing rule for this run: a document that pins any companion re-derives EVERY pin it carries at each new version, and prints them in one table — never carries one forward untouched.** Both misses were carry-forwards; neither would have survived a table that must be regenerated whole. The prereg v1.3 and this file both now have that table.

**OQ-2 · WARN-4's discharge belongs in the charter, not only here.** → **Add one line at KP-12 separating Matt's said words from the conductor's inference, naming KP-14 as the ratification.** § C.1 states it register-side, but the ledger row is the one a future reader will cite, and *"costs nothing"* is jack-ryan's own assessment.

**OQ-3 · Charter L4 still reads "two oracle limbs are known-bad"; the measured answer is ONE** (WARN-2). → **Annotate L4 forward citing KP-7(ii), the way S-2 was annotated.** ND-04's rewritten handoff sentence already governs and is correct — but **L4 is the source text for a Matt-facing page he has already accepted**, and inconsistent treatment inside one document is how the wrong version gets quoted.

**OQ-4 · The skeleton emits 9 rows against this register's 23.** → **Leave the mismatch catch armed and expect it to fire at T-0.** It is the instrument working; the emitter fills at W3.

**OQ-5 · `register_sha256` now has a conformance test (`bf648e51…`) and nothing yet runs it.** → **Make the worked example a startup assertion in the emitter** — six lines, run once at load, and it converts *"the grader and the emitter agree"* from a hope into a boot condition. That is the same move R2D-10 and the quoting cap make everywhere else in this run: **a structural guarantee, not a procedural promise.**

---

*Filed 2026-09-20 by gandalf (named sub-agent, `SPEC-AUTHOR`), Wave 1, Run KC2-PLAY. **v0.1 and v0 not edited; superseded readings named in place at § A** — including two pins that were mine. **All four pins derived this session by `shasum -a 256`, never retyped.** **The worked digest `bf648e51…` was computed, not asserted.** **Law 3 held; GL-12 held; K-7 held.** No production code, no dispatch, no push.*
