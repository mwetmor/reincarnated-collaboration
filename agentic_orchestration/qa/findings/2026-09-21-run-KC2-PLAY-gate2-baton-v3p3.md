# Finding — 2026-09-21 — Run KC2-PLAY, Gate-2, the baton-v3.3 cut

**Reviewer:** jack-ryan (DEV-MODE, Gate-2, BLOCK authority)
**Requested by:** gandalf (`RUN-CONDUCTOR`), charter § 4 row 1 applied to v3.3
**Severity (worst):** WARN
**Verdict:** ⚑ **PASS-WITH-WARN** — the cut ships; four WARNs are queued for v3.4, none blocks drax
**Target:** engine `8d54ac12` (prereg, ALONE, zero code) + `07cf9897` (cut, 32 files), both pushed
**Developer:** star-lord (export seam). **Rows by:** gamora (simulation seam)
**Principles applied:** REVIEW_PROCESS §1 P-1 (math-before-code), P-2 (smoke-gate), P-3 (cross-seam impact), P-5 (severity matters)
**Disciplines cited:** #11, #64, #70, #72, #73, #75 cl. 2 / cl. 6, #76, #79, #80 (cl. 1, cl. 5, cl. 5(a))

---

## § 0 · DIGESTS AS **I** DERIVED THEM

Derived by me from each manifest's own `members` array under the law as the manifest now pins it —
two ASCII spaces, `\n` **between** lines only, **no trailing newline**, relpath ascending by Unicode
code point, UTF-8 — then every member digest and byte count re-hashed from disk.

| pack | members | **digest I derived** | claimed | all members re-verify |
|---|---|---|---|---|
| v3.3 model | 17 | `1b2dc13403ba7cfedb4faaa8410040648fe607ef41c549b174b5a94cf3eb8307` | ✅ identical | 17/17, 0 mismatches |
| v3.3 reference | 7 | `288c5dadff237e0f38088f92af1ed57ab79ef558c5e13d74d5232c9134cfe1c4` | ✅ identical | 7/7, 0 mismatches |
| v3.2 model | 15 | `9ab771ef2fa27fba8ddd9e023d1d247a926b29eae76d659a4a5083b963cafaa6` | ✅ identical | 15/15 |
| v3.2 reference | 7 | `f54bc5a1cb0c0e216a59a0547d9709abd160b417657fb2e803ec60c22b034028` | ✅ identical | 7/7 |

**⚑ v3.2 WARN-2 IS DISCHARGED, AND THE PROOF IS THAT v3.2 STILL REPRODUCES.** My v3.2 finding
recorded four readings of `pack_digest_law`. The v3.3 text admits **exactly one**: the two rival
byte forms I computed alongside it — trailing-newline `7d7bc01f…`, single-space `ebb4c08f…` — are
well-formed 64-hex digests that match nothing, which is precisely the abort-a-valid-pack failure the
clause now forecloses. Cross-generational check: `pack_digest_law` is **byte-identical at v3.0, v3.1
and v3.2** (194 chars, sha `1dbf821b…`) and **new at v3.3 on BOTH manifests** (787 chars, sha
`7f5509a8…`, with `pack_digest_law_exact` sha `c2c1e2a1…` also identical across the pair). The v3.2
pack reproducing under the v3.3 reading is the evidence that this repair **documented existing
behaviour rather than changing it** — a claim the receipt asserts and that I can now confirm
independently of the assertion.

---

## § 1 · WHAT I FOUND — the attack, in order of consequence

### ✅ (1) The digest law — ONE reading, reproduces. See § 0.
One residual, INFO-2 below.

### ✅ (2) ADDITIVITY — independently confirmed, and confirmed at a **wider** population than the cut's

Computed by me against the written bytes of both packs, twice, with two different instruments.

| assertion | cut's claim | **my derivation** |
|---|---|---|
| v3.2 member paths lost | 0 of 15 | **0** |
| v3.2 row ids lost | 0 of 42,003 | **0 of 42,013 distinct** (42,014 row-shaped dicts — a *wider* population than the cut's; see INFO-5) |
| carried rows byte-changed | 0 | **0 of 42,014** shared `(path, id)` keys, canonical-JSON identical |
| v3.2 row paths lost | — | **0** |
| new ids | +19,556 | **exactly 19,556** |
| top-level keys removed | 0 | **0**, by full recursive diff of all 15 shared members |

The set identity holds and the arithmetic corroborates it: 19,556 artifact rows − 1 declared id
collision (`V0-LAW-1`) + 1 minted (`V25-P5a`) = 19,556 new ids; per-member deltas
(config_of_record +2, math_rules +12, provenance +23, monster_defense +16,590, monster_offense
+2,930) = **19,557 = 19,556 + the minted row**. ⚑ The receipt's own note that its first draft did
this as arithmetic and failed a correct pack by one is confirmed as the right call: the set identity
is the sound instrument and the subtraction is not.

### ⚑ (3) THE `V25-P5` MECHANISM — verified against the bytes. Correct, with ONE gap: **WARN-1**

**What I verified holds:**
- **The row is byte-verbatim.** All 11 `v25_absence_law` rows reproduce gamora's artifact **in her
  order, whole-row, canonical-identical** — as do all 8 rowsets / 19,556 rows (§ 4).
- **Exactly one row superseded.** Four `⚑ v3p3_superseded_by` sites exist pack-wide; exactly **one**
  sits on a lifted row (`math_rules.json :: ⚑ v3p3_row_annotations.V25-P5 → V25-P5a`). The other
  three are member-level or registry-level (`config_of_record` → `V0-LAW-1`, `monsters.blocks_coverage`
  → `V24-19`, `provenance.absence_registry[25]` → `V24-4`). V-42's population is the right one.
- **Every other byte verbatim.** Full recursive diff: no v3.2 path removed, no v25 row touched.
- **`V25-P5a` is not among the lifted rows** — it sits in its own `⚑ v3p3_cut_minted_rows` block,
  self-declaring `supersedes: V25-P5` with its authority named.
- **ORACLE/PLAY reads correctly to a pack-only consumer** *once the annotation block is open*: the
  disposition is stated three times in the pack in mutually consistent terms —
  `V25-P5a.value.{ORACLE, PLAY}` as machine-readable keys, the prohibition prose, and
  `provenance.json :: ABS-MONSTER-OFFENSE-NO-DATA-POOL466 :: ⚑ the_disposition_is_PER_CONFIG_and_it_is_not_symmetric`.

**⚑ WARN-1 — the marker is right; the pack's INDEX to it does not reach it.**

`V25-P5` on the wire carries **seven keys and no marker**:

```
math_rules.json :: ⚑ v3p3_rows.v25_absence_law[id == "V25-P5"]
  {id, key, precedence: "NORMATIVE", provenance, scope, unit,
   value.prohibition: "Do REFUSE a NO-DATA body (no profile at all) and count the refusal as telemetry."}
```

A consumer iterating `⚑ v3p3_rows.v25_absence_law` — the traversal the pack's **own grain law**
prescribes (`⚑ v3p3_grain_law.v25_absence_law.resolves_on: ["id"]`) — reads a `NORMATIVE`
prohibition that the pack elsewhere states is **false under `ORACLE`**, with nothing in the row
pointing anywhere else. The correction lives in a **sibling top-level key the row does not
reference**.

⚑ **And the pack's one purpose-built index for exactly this hazard omits it.**
`meta.json :: ⚑ supersession :: ⚑ read_before_you_build` names `V0-LAW-1` ✅ and
`monsters.json :: blocks_coverage` ✅ — and **does not mention `V25-P5`** ❌. That is the single key
a builder is told to read first, and the one hazard MIGRATION § 1 ranks as *"READ THIS AND STOP, IF
YOU ONLY READ ONE SECTION"* item (a) is the one hazard missing from it.

**Why WARN and not BLOCK.** The mechanism is conductor-ratified, the row genuinely cannot carry the
marker without redding V-32, and the hazard IS carried loudly on three independent surfaces
(MIGRATION § 1(a) with a config table; `meta.json :: headline`; the residual registry row). The only
in-pack remedy moves a digest already accepted, pushed, and under this review — the same trade the
conductor correctly ratified for the `_n_` rename. **But the reader who follows the pack's own
prescribed traversal gets the wrong rule, and that is not marked at the point of traversal.**

**⚑ The structural finding underneath, and it is the one worth carrying forward:** `V-33` asserts
that the annotations **exist**. Nothing asserts that the **index reaches them**. Those are two
different predicates over two different populations, and only the second is what a consumer walks.

### ✅ (4) THE ELEVEN MINTED GATES — I ran **seven** predicates myself, against the bytes

| gate | predicate I ran | my result | receipt | verdict |
|---|---|---|---|---|
| **V-32** | all 8 rowsets, artifact ↔ pack, gamora's order, whole row, canonical JSON | **0 diffs / 19,556** | 0 | ✅ |
| **V-34(b)** | v20 grain `(record_path, kind, slot)` vs `+skill` | **678 / 688** then **688 / 688** | 678 / 688 | ✅ reproduces exactly |
| **V-36 / V21-G1** | `\|v21\|` vs `V24-22.value.rows_consumed` | **2,073 == 2,073** | holds | ✅ |
| **V-36 / V23-G1** | `\|v23b\|` vs distinct `(record_path, wave)` of `monsters.json::blocks` | **15,800 == 15,800** | holds | ✅ *(see INFO-5)* |
| **V-36 / V0-G3** | `V0-LAW-1` arm keys vs `V0-ARM-*` ids in `config_of_record` | **5 == 5**, same names | holds | ✅ |
| **V-38** | three-state completeness over v20 `⚑ or_zero_fields` | **2,752 cells** = 688 × 4; MEASURED 1,286 / ABSENT-FIELD-BLANK 942 / ABSENT-NO-SLOT-ROW 524; **0 unlabelled** | identical | ✅ exact |
| **V-39** | every `record_path` resolves in `monsters.json::blocks` or flags outside | **19,520 checked, 0 unresolved**; 791 distinct paths in the board | 19,520 / 0 | ✅ |
| **V-41** | every `ABS-` id resolves in the registry **BY KEY** | **42 referenced == 42 registry rows, 0 outside** | 0 | ✅ |

**⚑ V-41's "by key, never by regex" is load-bearing and I confirmed the contrast myself.** A regex
sweep of the same bytes returns `ABS-30760` (a substring of `MS-ABS-30760` in a provenance string)
plus four truncated prefixes — **five phantoms, none real.** The prereg recorded this as a
non-finding before the emitter existed (#75 cl. 2 posture: the instrument was shown against a known
negative before its reading counted). Correct then, correct now.

**⚑ V-40 — the routed defect, discharged, and the discharge is exemplary.**
All 20 `out` blocks equal the expectation already on the wire: `out.after_armor ==
in.expect_after_armor` and `out.applied_damage == in.expect_applied_per_rev` on **20 of 20, zero
exceptions**. Full recursive diff confirms **every `in` block byte-unchanged** — the *only* paths
that moved under `test_vectors` are `[*].out`. **No value invented, none recomputed.** Both
structural cases assert by predicate: 1 immune case (`V6-VEC-02`, `applied 0.0`) and 3 zero-armour
identity vectors. The change is disclosed **in the pack**, not only in the commit body, at
`math_rules.json :: rules[14] :: ⚑ v3p3_harness_law`. See INFO-4 for the one grain note.

### ✅ (5) V-30's dialect clause inverts as INFO-4 predicted — and it was NOT loosened

Measured by me over the written bytes:

- **v3.2 rows under `⚑ v3p2_rows`: 791 rows, exactly 1 distinct `scope`** (`cell:M-POL-2@E-s09-cp150`).
  V-30(b)'s clause is **intact, true, and running over the population it was written for.**
- **v3.3 rows under `⚑ v3p3_rows`: 19,556 rows, 791 distinct scopes** — **790 `record:` + 1 `cell:`**.
  The clause does not weaken. It **inverts**.

V-30 was not re-pointed, not re-scoped, not relaxed; the v3.3 rows got V-34 asserting the DR-3 tie
hazard at the grain instead. **This is #75 cl. 6 applied correctly and pre-emptively** — a remedy
declining to inherit its predecessor's instrument — and it is the first instance in this corpus where
the clause was applied *before* the mismatch shipped rather than after it embarrassed someone.

### ✅ (6) `ABS-B3-STAT-DIMENSIONS` narrows and does not retire — and the pack does not read as if the skill tree were lifted

- `ABS-B3-STAT-DIMENSIONS`: `class` → `LIFTED`, `blocks_playability` **true → false**,
  `runtime_choice_required` **stays true**, the v3.2 reading kept whole at
  `⚑ superseded_reading_named_in_place`, the lowering labelled `⚑ v3p3_blocks_playability_ruling`
  as *"a READING, not a measurement — surfaced to the conductor veto-open."*
- `ABS-MONSTER-STAT-BLOCKS`: **untouched**, `blocks_playability: true`, still in `blocker_row_ids`,
  and the `overlaps` block names B3 as its child. **Hole B3 survives narrowed through its parent.**
- Residual `ABS-MONSTER-OFFENSE-NO-DATA-POOL466` minted, `UNDECODABLE-FROM-SUBSTRATE`, carrying the
  per-config disposition and the 338 / 342 on **both** denominators.
- ⚑ **The skill tree is explicitly excluded in three places** — `the_distinct_holes[2]`
  (*"NARROWED AT v3.3, NOT CLOSED … the SKILL TREE is still not lifted"*), `ABS-B3 :: ⚑ v3_lift_status`,
  and MIGRATION § 3. **Honest.** I looked for a reading in which v3.3 claims the tree and found none.

**Discharged, not a finding:** `ABS-B3`'s `what` / `why` are still the pre-lift prose beside
`class: LIFTED`. The pack anticipates this — `provenance.json :: class_enum_note` states that
`LIFTED` *"does NOT mean the row's `why` is still true — a LIFTED row's `why` is usually the stale
claim the lift refuted, which is why `⚑ v3_lift_status` is OBLIGATORY and gated by V-35."* That is
the correct disposition and it is published (INFO-2 from v3.2, discharged).

### ✅ (7) The remaining structural checks

- **V6 not superseded by v23** — `⚑ v3p3_relationship` carries `⚑ THIS_IS_NOT_A_SUPERSESSION: true`
  and V-40 asserts both structural cases by predicate. ✅
- **Dialect exemption extended, not loosened** — `⚑ dr3_scope_dialect_exemption.⚑ v3p3_extension`
  states the extension, the measurement (`_is_parameter` 19,556/19,556), and the refusal to re-point
  V-30, citing #75 cl. 6 by name. ✅
- **V33-G0 three-dict pin** — V-37 records six sources across **three** substrate dicts and states
  that a `threat.py`-only gate covers 4 of 6, *so the green cannot be misread.* ✅ That sentence is
  #80 cl. 1 practised voluntarily.
- **`V21-G1` / `V23-G1` / `V0-G3`** — all three re-derived by me against the pack, not read off a
  note. ✅ See the table above.

### ✅ (8) K-7 — three sealed cells, **re-hashed by me**, never opened

| cell | pinned | **derived by me** | bytes |
|---|---|---|---|
| `kc2-checkpoint-E-s09-cp150-mpol2-20260825_114420.json` | `ad61ad2a…` | `ad61ad2a…` ✅ | 123,564 |
| `kc2-checkpoint-E-s09-cp150-mech-20260816_124031.json` | `20b05cb4…` | `20b05cb4…` ✅ | 2,125,271 |
| `kc2-checkpoint-E-s09-cp150-w1walls-20260825_220058.json` | `7a992c81…` | `7a992c81…` ✅ | 403,084 |

PRE == POST, 3/3, both by digest **and** byte count. **No cell opened, by the cut or by me** — I
read bytes into a hash and nothing else. gamora's artifact verifies at
`e51b54a118f657ba7abd4298e5fcea86cfab3aeedebf8dd70a1239c5ea1b776e`, **11,847,705 B**, both as
claimed. The cut prereg verifies at `d270143a…` against the receipt's `CUT_PREREG`.

### ✅ (9) STALE VALUES — the sweep, including what is **clean**

- **The conductor's 229 / 297 / 302 sizing: ZERO occurrences** in any sizing context, in the pack or
  in MIGRATION § v3.3. Cleanly superseded by 338 / 342, which appear **always with their
  denominator named** (338/466 *and* 0/169, never the flattering one alone). ✅
- **"the 169"** — every substantive occurrence labels its population (`ANCHOR-169`, *"the RECORDED
  ROSTER"*, *"169/169 of the ROLLED roster"*). My sweep's apparent hits were row ids (`V20-169`,
  `MS-169`) and a source line number. ✅ **Clean.**
- **Banner ×2.0** and **θ 0.49** appear **only as named-refuted values**, with the correction at the
  same site: *"THE BANNER IS x1.031887755102041 UNDER THIS LIMB, NOT x2.0"*; *"THETA OF RECORD IS
  0.22972972972972974, NOT 0.49."* ✅ #64 practised.
- **coverage `k/72`** — zero occurrences. ✅
- ⚑ **Two stale strings DO survive, both in `meta.json`, both hand-authored beside machine-verified
  content: WARN-2 and WARN-4 below.**

### (10) What a GDScript consumer following the pack literally gets wrong

**WARN-1** (the `V25-P5` traversal) is the one that matters and is the only one with a runtime
consequence. Everything else a literal reader could trip on is marked, and marked well: the
published-grain trap ships as `⚑ v3p3_grain_law` on **every** carrier with the resolving tuple and a
worked two-row counter-example; `pack_schema_version` vs `_schema_version` ships with
`⚑ version_fields_of_record` naming all five fields and which one is the authority; `v22` base DA vs
`v23b` wave-resolved DA is called out in the headline. **WARN-2 and WARN-4 are read-wrong-number
hazards, not build-wrong-thing hazards.**

---

## § 2 · FINDINGS

**BLOCK: 0 · WARN: 4 · INFO: 5**

### ⚑ WARN-1 — `V25-P5` is not reachable from the pack's own consumer index

**Evidence:**
`src/reincarnated/output/kc2-model-pack-v3-E-s09-cp150-mech-v3p3-20260921_022612/model/math_rules.json`
→ `⚑ v3p3_rows.v25_absence_law[id=="V25-P5"]` — 7 keys, **no marker**, `precedence: "NORMATIVE"`.
Same member → `⚑ v3p3_row_annotations.V25-P5.⚑ v3p3_superseded_by.row == "V25-P5a"` — the correction.
`…/model/meta.json` → `⚑ supersession.⚑ read_before_you_build` — names `V0-LAW-1`, names
`blocks_coverage`, **does not name `V25-P5`.**

**Rationale:** Discipline **#73** (state changed, record did not follow) at index grain, and
**#80 cl. 1** — `V-33`'s green is a claim about the *annotations* population, never about the
*hazards* population the index is supposed to span. Review principle **P-3** (cross-seam impact):
drax is the consumer and the pack is his wire.

**Action:**
- [ ] **star-lord (v3.4, with WARN-2/3/4 in one re-cut):** `⚑ read_before_you_build` enumerates
      **every** `⚑ v3p3_superseded_by` site, derived (#76), never hand-listed; and a gate asserts
      that index is **complete over that population** — not merely that each annotation exists.
- [ ] **drax (now, no re-cut needed):** build the NO-DATA disposition from
      `math_rules.json :: ⚑ v3p3_cut_minted_rows.V25-P5a` (or the identical per-config block on
      `ABS-MONSTER-OFFENSE-NO-DATA-POOL466`). **Do not implement `⚑ v3p3_rows.v25_absence_law[V25-P5]`.**
      MIGRATION § 1(a) is correct and is your instruction of record.

### WARN-2 — `playability_statement` reads 8/5; the view it points at reads 6/4

**Evidence:** `…/model/meta.json :: playability_statement` — *"it is EIGHT rows over FIVE distinct
holes."* `…/model/provenance.json :: ⚑ playability_blocker_view` — `n_blocker_ROWS: 6`,
`n_DISTINCT_HOLES: 4`, `len(blocker_row_ids) == 6`.

**Measured across three cuts, by me:**

| pack | statement | view | agree |
|---|---|---|---|
| v3.1 | 8 / 5 | 8 / 5 | ✅ correct when written |
| v3.2 | 8 / 5 | **7 / 4** | ❌ **my own v3.2 Gate-2 missed this** |
| v3.3 | 8 / 5 | **6 / 4** | ❌ drifted a second time |

**Rationale:** **#73**, and **#80 cl. 1** — a hand-set constant sitting beside a computed list is the
"constant the emitting artifact stamps" shape my own v3.2 **INFO-4** named for `scope`. It arrived at
a second field in the same pack one cut later. MIGRATION § 3 carries the **right** figure (*"7 rows /
4 holes → 6 rows / 4 holes"*), so the number was known at cut time and the prose was not swept (**#72**).

**Mitigating, and why not BLOCK:** the same sentence defers to the list (*"The exact list is
… blocker_row_ids, and V-26 checks the view against this predicate rather than trusting either"*),
`V-26` gates the list at 0 disagreements, and the error is **conservative** — it overstates blockage.

**Action:**
- [ ] **star-lord (v3.4):** the figure is **computed at emit from the view, or deleted.** Correcting
      the literal repairs this instance and guarantees the third recurrence. A gate asserts
      prose-figure == view-figure; nothing in the 41 does today.
- [x] **jack-ryan:** own the v3.2 miss. Recorded here, not softened.

### WARN-3 — `V25-P5a` is asserted "verbatim" and is not

**Evidence:** `…/model/math_rules.json :: ⚑ v3p3_cut_minted_rows.V25-P5a.provenance` — *"gamora v3.3
prereg ADDENDUM § 5 …, **verbatim**"*. Source:
`src/reincarnated/simulation/math/kc2-play-v3p3-monster-offense-prereg-2026-09-20.md` § 5
(Addendum), the `V25-P5` bullet. Mechanical diff after stripping markup and whitespace:
**word-level similarity 0.786**, not 1.0; not identical case-insensitively either.

Substantive deltas: `"11 such bodies"` → `"11 NO-DATA bodies"`; **inserted** `"has fewer bodies than
the oracle and"` (true, but imported from § 5's *`V25-P4`* bullet, not the `V25-P5` one);
`"the one thing"` → `"the only thing"`; `"so it must be tested … not by a T-A band"` → `"It is
tested … never by a T-A band"` (modal strengthened); the PLAY clause relocated; *"not a universal
law"* demoted from value text into a key name.

**⚑ Nothing is invented and nothing inverts.** The `ORACLE` / `PLAY` dispositions, the 11-of-97
empirical forcing, the three `run.py` sites, the stream-neutrality argument and the divergence-register
status are all exact. **The defect is the claim, not the row.** KP-32 clause 2 said *verbatim*; a
provenance field that says *verbatim* is a checkable assertion, and it fails its check.

**Rationale:** **#64** (referent-binding — a provenance string binds what it names), **#19.1(b)** via
**#80 cl. 3(a)** (an unverified sentence sitting beside verified content reads as verified).

**Action:**
- [ ] **star-lord (v3.4):** either restore the § 5 bytes exactly, or change `provenance` to
      `"…, RE-SET FROM (not verbatim); deltas listed at ⚑ v3p3_deltas_from_source"` and list the five.
      ⚑ **Prefer the second** — the re-set reads better and imports a true clause from the neighbouring
      bullet; it is the *label* that should move, not the text.

### WARN-4 — `source_pins.V3_PREREG` points at the **v3.0** prereg under the role *"this cut's"*

**Evidence:** `…/model/meta.json :: source_pins.V3_PREREG` →
`src/reincarnated/export/math/2026-08-25-kc2-baton-v3-cut-prereg.md`, 12,058 B, role
**`"this cut's pinned criteria (D4, committed alone)"`**. Identical at v3.1, v3.2 and v3.3 — so the
role string has been **false for three consecutive cuts**. The pin itself is valid (digest
re-verified by me against disk ✅); it is the *label* that is stale. This cut's actual prereg
(`2026-09-20-kc2-baton-v3-3-cut-prereg.md`, `d270143a…`) is pinned **only in the receipt**, which is
not a pack member — so a pack-only consumer asking *"what criteria was this cut held to?"* is handed
the v3.0 document, labelled as this one's.

**Rationale:** **#73** + **#72**. Second instance of WARN-2's exact shape, in the same member, which
is what makes the remedy structural rather than a correction.

**Action:**
- [ ] **star-lord (v3.4):** `V3_PREREG` carries the prereg of the cut that emitted the pack, and
      gamora's v3.3 prereg + both addenda join `source_pins` (they are in the receipt, not the pack).
      `role` strings that say *"this cut's"* are emitted, never literal.

### INFO-1 — the receipt's counter namespace, measured

Confirmed and **extended**. The four population counters sum to exactly **25**
(`V-12_n_w2_rows` 4 · `V-14_n_bias_rows` 8 · `V-17_n_devotion_proc_rows` 7 · `V-23_n_in_scope` 6).
**All 20 keys whose name contains `violation` are zero, and no nested `n_violations` is non-zero.**
⚑ **The hazard extends past `_n_` to `_sites`**, which star-lord's flag did not name: of 37 `_sites`
lists, exactly one is non-empty — `V-23_in_scope_sites` (6) — and it is a **population** list. A
reviewer's natural two-line audit (`any non-zero _n_`, `any non-empty _sites`) reads **25 violations
and one violation site on a clean pack**, from both namespaces. The refusal to rename is
**ratified** — renaming re-runs the cut and moves digests already on `origin`, and *"the cheap fix is
cheap only BEFORE the cut"* is right. Queue with WARN-1/2/3/4 for **one** v3.4 re-cut. Prefix the
population counters `pop_`, not just the violation ones.

### INFO-2 — `pack_digest_law_exact` is labelled machine-readable and is not executable

`digest = sha256("\n".join(f"{relpath}  {sha256}" for relpath in sorted(members)).encode("utf-8"))`
— against this manifest, `members` is a list of dicts, so `sorted(members)` raises `TypeError`, and
`sha256` inside the f-string names both the hash function and the member field. The **byte form is
unambiguous from the prose** and I reproduced all four digests from it, so this creates no digest
ambiguity. Rename to `pack_digest_law_pseudocode`, or make it run.

### INFO-3 — one genuine dangling pointer: `TA-X-25(c)`

Appears twice, both inside `V25-P5a`'s own text, resolves **nowhere** in either pack, and prereg v1.4
is not in `source_pins`. It is **corroborative, not load-bearing** — the replacement rule's substance
(*"a per-ARM PRESENCE test, which proves MEMBERSHIP and NEVER COMPOSITION"*) is stated inline beside
the id, so a pack-only reader loses the citation but not the rule. ⚑ By contrast
`DIV-nodata-refusal` is **self-resolving** — it names its own `ORACLE` / `PLAY` values at all three
sites. That is the right pattern; `TA-X-25(c)` should follow it or be dropped.

### INFO-4 — "ADDITIVE / 0 carried rows changed a byte" is true at row grain and false at byte grain

`math_rules.json :: rules[14]` (`RULE-MONSTER-TO-PLAYER-MITIGATION-ORDER`) **did** change: two keys
added and **20 `test_vectors[*].out` values written from `null`**. It is keyed `rule_id`, not `id`,
so it is not a "row" under the pack's definition, and the `10 of 15 shared members byte-identical`
figure carries it honestly. The change is disclosed in-pack at `⚑ v3p3_harness_law` and verified
sound (§ 1(4)). **Both readings are correct; only the grain separates them.**
⚑ **This is candidate A limb 2, live, in the cut's own headline** — and I offer it as evidence for
the ratification below rather than as a defect. One line at `⚑ what_changed` closes it:
*"ADDITIVE at ROW grain; one v3.2 `rules[]` entry changed at byte grain — see `⚑ v3p3_harness_law`."*

### INFO-5 — ⚑ **my own two population defects, at this gate, on this artifact**

Recorded because they are the strongest evidence in this finding for candidate A, and because
**#80 cl. 3(a)** obliges a reviewer to state what their instrument did and did not reach.

1. **My additivity walker keyed on `"id"`.** That population **cannot see `rules[]`**, which keys on
   `rule_id`. My first "0 carried rows byte-changed" was computed over a set that structurally
   excluded the one thing that changed. I found the 20 `out` edits only on a second pass with a full
   recursive diff. ⚑ **The check ran, returned zero, and the zero was about the wrong set.**
2. **My V23-G1 re-derivation returned 15,801 against the gate's 15,800 — and the gate was right.**
   My population included the single null-wave record (`krieg_aethertrap`, the GL-12 null); excluding
   it gives **790 records × 20 waves = 15,800** exactly. I was one keystroke from filing a
   discrepancy against a correct gate.

Both are limb-1 defects, committed by the **auditor**, at the gate, against a correct artifact.
Neither would have been caught by re-deriving harder. Both would have been caught by naming the
population before quoting the figure.

---

## § RATIFICATION

Two candidates, `canonical-doc-format.md § 6.7`, gandalf proposes → jack-ryan rules. Corpus state
verified at the moment of writing (**#79** — a rule number is derived, never recalled):
`design/working-agreement/engineering-disciplines.md` runs to **#81**; **#77 is VACANT BY
CONTAMINATION, never to be assigned**; **82 and 83 are free.**

---

### A · gamora's population candidate — ⚑ **ADOPT, BOTH LIMBS, UNMERGED, AS #82**

**⚑ gamora was right to refuse the collapse, and I can now prove it from this session's own
evidence rather than from argument.**

The two limbs have **different detection methods**, and that — not their subject matter — is what
makes them two rules:

- **Limb 1 is detected by re-deriving with the population named.** My INFO-5 defects are both limb 1
  and both were found by a second, wider derivation.
- **Limb 2 is detected ONLY by labelling.** INFO-4 is the proof: I re-derived "0 carried rows changed
  a byte" **twice** and got zero **both times**, because my population also excluded `rules[]`. The
  arithmetic was right at every pass. ⚑ **No amount of re-deriving finds a grain ambiguity, because
  re-deriving reproduces the same grain.**

**Merging them makes limb 2 unenforceable** — a reader would discharge the merged rule by
re-deriving, which is exactly the operation that cannot see it. That is the **#63** emitter/reader
precedent and the **§ 75.5** reasoning: two halves are one number only when satisfying one cannot be
mistaken for satisfying the other. Here it can, and trivially.

**Wording as adopted:**

> ### 82. A figure carries the population it ranges over, and where two grains coexist it carries the grain — at the figure, not in a neighbouring sentence
>
> **cl. 1 — NAME THE POPULATION BEFORE QUOTING THE FIGURE.** A count, fraction, dispersion or
> difference is a claim about a set. **State the set at the site of the number.** A subtraction is
> not a substitute for an intersection when the two operands overlap partially; a label is not a
> population; a measured-inert count does not belong in a data-absence column; and a dispersion is
> quoted over **the unit actually drawn**, never over the bodies that unit produced.
> *Six founding instances — five from gamora's KC2-PLAY v3.3 lift* (the shortfall that owed a set
> intersection, 41 of ANCHOR-169 outside POOL-466 · *"the 169"* naming three populations · a
> measured-inert count in a data-absence column · a roster let to imply it held the spawns · a
> dispersion over 97 bodies when the drawn unit is 23 pool picks, design effect **2.05×**,
> z **4.72 → 2.30**, dissolving an apparent 4.7 σ anomaly) *— and two more from the Gate-2 review of
> that lift, committed by the reviewer against a correct artifact* (INFO-5).
>
> **cl. 2 — WHERE TWO GRAINS COEXIST, NAME THE GRAIN AT THE FIGURE, EVEN WHEN BOTH ARE CORRECT.**
> ⚑ **This clause is detectable ONLY BY LABELLING and NEVER BY CHECKING.** Both numbers are right,
> the arithmetic reproduces at every re-derivation, and the ambiguity is invisible to the instrument
> because the instrument shares the grain. Founding instances: **342 vs 338 + 4** (source-row grain
> vs constructed grain; `342 = 338 + 4` exactly, both correct); and **"0 carried rows changed a
> byte"** — true at ROW grain, false at BYTE grain, in the same cut's own headline (INFO-4).
>
> **Trigger points:** quoting any count, coverage, fraction, dispersion or delta across a seam ·
> any shortfall computed by subtraction where the operands may overlap partially · any figure a
> second seat will re-derive · any artifact carrying a source grain and a constructed grain · any
> review that re-derives another seat's number (**#80 cl. 3(a)**).
>
> **Cross-references (and the reason this is a new number rather than an amendment):**
> **#80 cl. 1** is the nearest neighbour but binds *fractions and regions*; cl. 1 here reaches
> counts, subtractions and dispersions that carry no denominator. **#70** binds what a *source*
> declares it does not cover; this binds what a *figure* declares it ranges over. **#76** says
> derive the population; this says **print** it. **#64** (referent-binding) is cl. 2's parent — cl. 2
> is #64 applied where both referents are valid, which #64 does not currently reach.

**Number: #82.** ⚑ **And it is the one discipline in this run whose founding evidence includes the
seat that ratified it.**

---

### B · star-lord's surface candidate — ⚑ **ADOPT AS #83.** The conductor's third shape — ⚑ **REJECT as a new number; it already exists at #80, and gains cl. 6**

**B itself: ADOPT, own number, not a clause under #75.**

> ### 83. Before mandating a remedy, confirm the surface can carry it
>
> A remedy is specified **at** a surface: a field, a key, a row, a document section, an id class. The
> specifier owes a check that the surface **exists and can bear the remedy** before the instruction
> is issued — because the builder who receives it must either violate the instruction or violate the
> constraint it was meant to protect, and will resolve that silently.
>
> **Three founding instances, all KC2-PLAY, 2026-09-20:**
> * **jack-ryan Gate-2 v3.2 WARN-3** — *"add a note BESIDE `V0-LAW-1`"*, at a surface that could not
>   disambiguate *beside* from *inside*; a key written into the row moves its bytes and reds V-28.
> * **gandalf's crack-law gate** — keyed to id-mask classes that **KP-19 had already deleted**.
>   *No referent in first-party data.*
> * **conductor ruling KP-32, clauses 2 and 3** — *"ship it verbatim"* and *"carrying the marker"*,
>   **mutually unsatisfiable on their face**: a key added to a row is not verbatim.
>
> ⚑ **Distinct from `#75` cl. 6, and the discriminator is sharp: there, the instrument EXISTED and
> went STALE; here, the surface NEVER EXISTED AS SPECIFIED.** Cl. 6's trigger is *a predecessor
> remedy is being carried forward*; #83's trigger is *a remedy is being authored*. Different moment,
> different actor, different check. Folding #83 into #75 would file it where the specifier does not
> look — #75's trigger points are all addressed to whoever **runs** an instrument.
>
> **The discharge is cheap and that is the argument:** name the surface, open it, confirm the remedy
> is expressible there, and if it is not, say so in the ruling. **Every one of the three instances
> was resolved correctly by the builder** — drax on the push conflict, star-lord twice here — which
> is exactly why it must be a rule: the system is currently relying on builders being good enough to
> repair their instructions, and recording the repair is optional.
>
> **Cross-references:** **#75 cl. 6** (the stale-instrument sibling; read the two together).
> **#72** (when the remedy lands, sweep its citation sites). **#79** (a citation into an executable
> dispatch is the citer's liability).

**Number: #83.**

---

**⚑ The conductor's third shape: REJECT the new number. It is `#80`, and this is a `#79` instance.**

The conductor's lean — *"an empty input and a passing input return the same verdict, so every check
must assert its input POPULATION"* — describes a real defect. **But the corpus already holds it, and
holds it better than the proposed wording.**

`design/working-agreement/engineering-disciplines.md` **§ 80**, minted by me 2026-08-25:

> **80. A gate's GREEN is not evidence until that gate has been shown to go RED, on this population,
> in this configuration.** *Founding sentence, drax's, generalised:* **⚑ "'fixed' and 'blind' print
> the same zero."**
> **cl. 5(a):** *"`PASS = True` over `[0]` and over `[0, 0]` are different claims wearing one
> token"* — a verdict over a set carries **both** the count evaluated **and** the count defined.

That is the H-KP-1 harness defect verbatim (*reads `out`, all null, passes 20 having checked
nothing* — `marks_evaluated` 0, `marks_defined_for_row` 20) and V-40's first draft is its mirror
(**#80 cl. 2(a)**: a gate that cannot compute its own floor returns UNEVALUABLE, not PASS — V-40
returned BLOCK, the safe sign, which is the only reason it surfaced at the cut and not in a green T-0).

⚑ **Three seats inventing it independently is not evidence the corpus lacks it. It is evidence the
corpus HAS it and nobody looked — which is `#79` (citation provenance: a rule number is DERIVED from
the corpus at the moment of writing), fired at the conductor's seat, in this run.** I record it
without prejudice: #79's own founding instances are mine and knight-rider's, one day apart.

**And the sharpening matters, because the conductor's proposed wording would NOT have caught
V-40.** *"Name N, assert N is what it should be, then evaluate"* is **#82 cl. 1**. V-40's N **was**
20, and 20 **was** right; the draft still found neither structural case. What is empty there is not
the population — it is the **evaluated content**. Of the three instincts cited, gamora's
`PRE == POST`-as-enumeration and star-lord's census-from-the-artifact are **#82 cl. 1**; only drax's
coverage gate **refusing to close at 0/89, red by construction** is #80, and it is #80 exactly.

**What IS genuinely missing — and it is narrow, so it lands as an amendment:** #80's trigger points
name *gates, thresholds, PASS/FAIL criteria, fractions in receipts, boolean verdict keys*. **They do
not name the FIXTURE.** A test-vector set whose expectation field is empty is not a gate, not a
fraction and not a verdict key — it is the **data every downstream check asserts against**, and it
blinds all of them at once while each individually looks compliant. Both V-40 instances live there.

> **#80 cl. 6 — THE FIXTURE, not only the checker.** *(Amendment 2026-09-21, jack-ryan, routed by
> star-lord via gandalf from KC2-PLAY V-40.)* An expectation set, golden file, vector table or
> reference fixture whose expectation field is **empty, null, or absent** makes **every** consumer of
> it blind simultaneously, and each consumer independently reports green. **Therefore the fixture
> asserts its own expectation population before it is shipped, and emptiness reaches the FAIL
> branch, never the PASS branch by default.** Founding instances, one artifact, opposite signs:
> KC2-PLAY's 20 `V6-VEC-*` test vectors carried `out: null` with their expectations stranded inside
> `in` — a harness reading `out` compares `None` to `None` twenty times and passes (charter H-KP-1
> defect 3); the gate written to audit them read the same empty field, found neither structural
> case, wrote nothing and **BLOCKED** — the same blindness with the safe sign, and the only reason it
> was repaired at the cut. ⚑ **The failing direction is the one that surfaces; the passing direction
> is the one that ships.** Cl. 6's discharge is a predicate on the fixture (*"n expectations
> populated == n vectors"*), not a comment. Cross-reference **#82 cl. 1**: cl. 6 is what remains
> after the population is correctly named — N right, content empty.

**Summary of rulings:**

| candidate | ruling | number |
|---|---|---|
| **A** · population + grain (gamora) | ⚑ **ADOPT — both limbs, unmerged** | **#82**, cl. 1 + cl. 2 |
| **B** · surface can carry the remedy (star-lord) | ⚑ **ADOPT — own number, not under #75** | **#83** |
| conductor's third shape (empty ≡ passing) | ⚑ **REJECT as new — already #80**; **AMEND** #80 to reach fixtures | **#80 cl. 6** |

**Canonical write owed, not done here.** This finding is the ruling; the landing into
`~/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md` (#82, #83, #80
cl. 6, plus the **#72** citation sweep — #80's own cross-reference list and #75's cl. 6 pointer both
need to name #83) is a separate commit on my seam. ⚑ **Per #80's own mint-lateness record: do not
cite #82 or #83 by number in any dispatch until that landing exists.**

---

## § 3 · DISPOSITION

**PASS-WITH-WARN.** The v3.3 model and reference packs are **accepted as of record.** drax is
**unblocked** on charter § 4 row 1, subject to the WARN-1 interim instruction above.

**Queued as ONE v3.4 re-cut** (not four): WARN-1 index completeness + gate · WARN-2 computed
playability figure + gate · WARN-3 provenance label · WARN-4 `V3_PREREG` pin and role · INFO-1
`pop_` prefix on the four population counters and the one population `_sites` list · INFO-2 rename
`pack_digest_law_exact` · INFO-3 drop or inline `TA-X-25(c)` · INFO-4 one grain line at
`⚑ what_changed`. **None of these is worth moving an accepted digest on its own; together they are
one cheap cut.**

**Nothing escalates to Matt.** Every WARN is within the seam's authority to fix and none conflicts
with a locked decisions-log entry. The two conductor rulings I was asked to verify against the bytes
— KP-32's mechanism as amended by star-lord, and the `_n_` re-cut refusal — **both hold.**

**⚑ Two things I want on the record about the seats rather than the artifact.** star-lord reported
`V-21`-does-not-run, the `_n_` hazard, the KP-32 unsatisfiability and his own V-40 draft failure
**before I could find any of them**, and his V-40 repair is the cleanest instance of #75 cl. 2 in
this corpus — the gate went red first and the red was believed. gamora refused a discipline
collapse that would have over-claimed, and § 2's ratification exists because she was right.
**I found four WARNs; three of them are labels, and none of them is a number.**

---

## References

- `/Users/admin/Games/reincarnated-engine/src/reincarnated/output/kc2-model-pack-v3-E-s09-cp150-mech-v3p3-20260921_022612/` (manifest + 17 members)
- `/Users/admin/Games/reincarnated-engine/src/reincarnated/output/kc2-reference-pack-v3-E-s09-cp150-mech-v3p3-20260921_022612/` (manifest + 7 members)
- `/Users/admin/Games/reincarnated-engine/src/reincarnated/output/kc2-baton-v3-cut-receipt-v3p3-20260921_022612.json`
- `/Users/admin/Games/reincarnated-engine/src/reincarnated/output/kc2-model-pack-v3-E-s09-cp150-mech-v3p2-20260920_214030/` · `…-v3p1-20260826_031143/` (comparanda)
- `/Users/admin/Games/reincarnated-engine/src/reincarnated/simulation/output/kc2-lifted-rows-KC2PLAY-v3p3-monster-offense-20260920_214408.json` (`e51b54a1…b776e`, 11,847,705 B)
- `/Users/admin/Games/reincarnated-engine/src/reincarnated/simulation/math/kc2-play-v3p3-monster-offense-prereg-2026-09-20.md` (`27fc5937…` at this review; Addendum § 5 at lines 761-795)
- `/Users/admin/Games/reincarnated-engine/src/reincarnated/export/math/2026-09-20-kc2-baton-v3-3-cut-prereg.md` (`d270143a…`)
- `/Users/admin/Games/reincarnated-engine/src/reincarnated/export/MIGRATION.md` (§ v3.3 at lines 9-182)
- `/Users/admin/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md` (#75 at 3648, #79 at 3897, **#80 at 3962**, #81 at 3995 — corpus state verified at write time per #79)
- `/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/gandalf/notes/2026-09-20-kc2-play-run-charter.md` (KP-30…KP-36)
- `/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/gandalf/notes/2026-09-20-kc2-play-ta-prereg-v1.4.md`
- `/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/qa/findings/2026-09-20-run-KC2-PLAY-gate2-baton-v3p2.md` (WARN-2/3/4, INFO-1/2/3/4 — all discharged or carried here)
- `/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/qa/findings/2026-09-20-run-KC2-PLAY-w1-preread.md`
