# Finding — 2026-09-20 — Run KC2-PLAY · Wave 2 · the **baton-v3.2 CUT** (Gate-2, DEV-MODE)

**Reviewer:** jack-ryan (DEV-MODE, BLOCK authority)
**Severity (overall):** **PASS-WITH-WARN** — **0 BLOCK · 4 WARN · 4 INFO**
**Target:** engine `5abb3a55` (prereg, ALONE) + `4beaa537` (the cut)
**Developer:** star-lord (export seam) · rows by gamora (KC2-PLAY W1 passes 1+2)
**Requested by:** gandalf (`RUN-CONDUCTOR`) · charter § 4 row 1 — *"jack-ryan Gate-2: no BLOCK outstanding"*
**Principles applied:** REVIEW_PROCESS #1 (math-before-code), #2 (smoke-gate), #3 (cross-seam impact), #5 (severity matters) · ADR-002, ADR-004, ADR-006 · Disciplines #1, #1.2, #2, #9, #11, #12, #19.1

> **Charter § 4 row 1 is SATISFIED. No BLOCK is outstanding.** The four WARNs are
> annotations and one false sentence; none of them changes a byte a runtime loads, and none
> requires a re-cut. **The pack releases.** Release/push is the conductor's call; milestone
> tagging remains Matt's (ADR-002).

---

## 0 · DIGESTS, DERIVED BY ME — both reproduce

Re-walked from **member bytes on disk**, not from star-lord's numbers: every member re-hashed,
every `bytes` field re-counted, then composed per the manifest's **own** `pack_digest_law`
(*"sha256 of the newline-joined `<relpath>  <sha256>` lines, sorted by relpath"*).

| pack | derived by me | claimed | |
|---|---|---|---|
| **v3.2 model** (15 members) | `9ab771ef2fa27fba8ddd9e023d1d247a926b29eae76d659a4a5083b963cafaa6` | same | ✅ |
| **v3.2 reference** (7 members) | `f54bc5a1cb0c0e216a59a0547d9709abd160b417657fb2e803ec60c22b034028` | same | ✅ |
| v3.1 model | `2c7fc61f6a6f4efa61e535ad504929e0c94c78e3e8ed9f14eaaa13dbaf1cf4a7` | same | ✅ |
| v3.1 reference | `f50e5e2548cf785bd846ec027021ae6b0539f3991651c39c7f6529854ea1edf6` | same | ✅ |

**0 member digest mismatches, 0 byte-count mismatches, 22/22 members across the two v3.2 packs.**
The reference pack's `cross_pin.model_pack_digest` re-derives to the v3.2 model digest. 6 of its 7
members are **byte-identical** to v3.1; only `reference/meta.json` moves (revision, cross-pin,
`emitted_by`, `⚑ supersession`, `⚑ v3p2_lift`), with **0 keys removed**.

*(⚠ the join admits two readings — see **WARN-2**.)*

---

## 1 · WHAT I FOUND

I ran the ten-item attack independently of the receipt in every case. **Nine of ten came back clean
against the bytes.** Item (10) produced three of the four WARNs.

### ✅ (2) Additivity — verified by a third process, against the written bytes

Enumerated every `{id, value}` row object across both member trees:

| claim | my measurement |
|---|---|
| every v3.1 member path present | **12 of 12**, 0 lost; 3 new (`config_of_record`, `monster_kinematics`, `projectiles`) |
| 41,212 v3.1 row ids present | **41,212 / 41,212**, 0 lost, 0 duplicated |
| v3.1 rows byte-unchanged | **0 changed** under canonical serialisation, and none of them lives inside a `⚑ v3p2_rows` block |
| exactly +791 | **42,003 − 41,212 = 791**, 0 id collisions |
| no top-level key removed | **0 removed** across all 12 members; only additions (`⚑ v3p2_rows`, `⚑ v3p2_lift`, `⚑ v3p2_superseded_by`, `⚑ dr3_scope_dialect_exemption`) |

3 model members (`ai_states`, `controllers`, `target_selection`) are **byte-identical** to v3.1 —
which is the method (§ 7(a), load-don't-re-derive) showing through, exactly as declared.

### ✅ (3) Row fidelity — I ran **791/791, not a sample of 40**

The brief asked for ≥ 40 across the 21 rowsets. The whole population is cheap and strictly stronger,
so I took it: **all 791 rows, order-preserving, whole-object byte-equal** to gamora's artifact under
canonical serialisation. 21/21 rowset names match; 0 artifact-only, 0 pack-only; no rowset carried by
two members; **every row carries all four DR quartet fields** (`value`, `scope`, `precedence`,
`provenance`) — 0 gaps. Artifact sha re-derived: `e011742935f14efa…` (prefix `e0117429` per charter KP-8) ✅.

**PRE==POST is a RULE, and I confirmed the rule — not the number.** Per-rowset PRE is
`⚑ rowset_census[k]` read off the pinned artifact; I re-summed the artifact's own census to 791,
re-counted the pack to 791, and checked all 21 keys agree pairwise. `⚑ PRE_is_a_RULE` is on the wire.
The `gamora_carried` refinement (prereg § 4 said 1123; V-18 runs inside the dialect view where it is
332) is **named, not silently re-pointed** — both censuses ship. That is gamora's G-2 honoured.

### ✅ (4) Six carries over nine surfaces — each verified in the bytes, at the exact surface

| # | MIG | surface | marker | row of record |
|---|---|---|---|---|
| 1 | MIG-1 | `monsters.json` top level | ✅ | `V6-SHIFT-1` |
| 2 | MIG-2 | `monsters.json :: mitigation_note` | ✅ | `V6-RETIRE-1` |
| 3 | MIG-3 | `rng_contract.json` top level | ✅ | `V9-CENSUS-1` |
| 4 | MIG-4 | `arena.json :: containment.runtime_containment` | ✅ | `V8-CONTAIN-1` |
| 5 | MIG-5 | `provenance.json :: absence_registry[ABS-DEVOTION-PROC-ICD]` | ✅ | `V7-BLOCKS-1` |
| 6 | MIG-6 | `rng_contract.json :: draw_site_registry[DS-SPAWN-SCATTER]` | ✅ | `V11B-SCATTER-1` |
| 7 | MIG-6 | `player_kit.json :: channel.hit_test_model` | ✅ | `V17-HITTEST-1` |
| 8 | MIG-6 | `math_rules.json :: rules[RULE-CAST-INTERRUPT-BINDING-EXCLUSIVITY]` | ✅ | `V18-INTERRUPT-1` |
| 9 | MIG-6 | `rng_contract.json :: draw_site_registry[DS-TYPEB-RELEASE].parameters.p_per_tick` | ✅ | `V19-TYPEB-1` |

All nine row ids exist in the pack. Each marker keeps the superseded reading **verbatim in place** (GL-7).

* **eHP semantic shift — value-unchanged CONFIRMED BY ME.** I extracted all `stat="ehp"` block
  objects from both packs: **31,601 in v3.1, 31,601 in v3.2, set-identical byte-for-byte.** The
  meaning moves; not one number does. MIGRATION.md notes it twice — § 1 (the drax table, with the
  1.902× consequence) **and § 2, which reaches this seam's own telemetry exports.** That second
  section is the one most cuts omit; it is Discipline #12 done properly.
* **`runtime_containment` → AUTHORED-WALLS with `arena_bounds` NOT written — CONFIRMED.** I walked
  `arena.json` for `arena_bounds` **as a key**: **zero occurrences.** The only textual hits are the
  prose asserting it is not written. `substrate_model: UNBOUNDED-OPEN-PLANE` retained beside the
  ruling. And `V8-CELL-1` rides beside it — *the sealed cell ran `arena_fold = None`, WALL-LESS* —
  which is the row that stops the ambiguity re-opening.
* **`ABS-DEVOTION-PROC-ICD` 7 → 2 — CONFIRMED.** `blocks_playability` **true → false**, class
  `DECODED-NOT-YET-LIFTED` → `UNDECODABLE-FROM-SUBSTRATE`, five ICDs named with values, two residuals
  named, v3.1 reading kept in place.
* **The four `⚑ v3p2_superseded_by` markers beside their stale-valued fields — CONFIRMED at the field
  itself**, not at the parent. `p_per_tick` still reads `0.0035510204081632656` with the CANCELLATION
  note attached to that key; `hit_test_model` still reads `"point"` with the 3.0 m disc attached to
  that key. That is V-29 doing the job it was minted for.

### ✅ (5) K-7 — three sealed cells, hashed only, never opened

| cell | my `shasum -a 256` | charter pin | bytes |
|---|---|---|---|
| M-POL-2 | `ad61ad2a8c79…44dc5c` | `ad61ad2a…` ✅ | 123,564 |
| mech | `20b05cb4ef3b…b15f4b` | `20b05cb4…` ✅ | 2,125,271 |
| W1 walls | `7a992c81ca6e…b7881b` | `7a992c81…` ✅ | 403,084 |

Three hashes, three byte counts. **No cell opened, no cell re-executed, no simulation run, no grade
moved.** Receipt records PRE and POST identically.

### ✅ (6) The dialect exemption — honest, narrow, published; it re-scopes nothing

`provenance.json · ⚑ dr3_scope_dialect_exemption` names the failure (V-4 `AttributeError` on
`"str".get`, V-2 would report 791), names the **measurement** (791/791 `_is_parameter` matches vs
v3.1's **0 / 41,212**), names **what covers them instead** (V-30), and names **the two moves not
taken** and why each is a violation. Its scope is the 791 rows and nothing else.

**On star-lord's own first-run red — the widened `carried_row_ids` that silently re-scoped V-18's
`gamora_carried`: it is genuinely closed, not renamed.** I checked the mechanism: the exemption is
now a **view** (`v2_dialect_view`), not a widened set, so V-18 counts inside v3.1's dialect and
returns 332 == 332. The full-tree 1123 is reported in a **separate** key. One variable is no longer
doing two jobs. ⚑ **That an agent measured its own near-miss, refused both shortcuts, and published
the finding rather than the fix is the single best thing in this cut.** Discipline #11 and #19.1
exactly as written.

### ✅ (7) Absence registry — both mints, and the blocker view re-derived by me

* `ABS-EOR-RANK-OF-RECORD` (the ONE honest-fail, `V1-WD-1`): `blocks_playability: false`,
  `runtime_choice_required: true`, what-was-searched quoted, consequence-if-a-runtime-guesses on the
  wire. **Picking a rank would be invention — Law 3.** Correctly refused.
* `ABS-W2-CAST-MIX`: a genuine dangling reference closed. I confirmed it **was** dangling —
  cited by `V18-INTERRUPT-1` and v3.1's `interrupts_channel` rows with no registry row.
* **Blocker view — I re-ran the predicate myself.** `blocks_playability == True` over all 41 registry
  rows returns **exactly the 7 published ids**, and the mirror exclusion (`ABS-TARGET-SELECTION-POLICY`)
  is respected. **7 rows / 4 holes**, down from 8/5. The pre-registered expectation was 7/4 and the
  predicate returned 7/4 (V-26 ✅).
* **V-24 class enum:** 4 classes in use, all inside the enum. ✅ (but see **INFO-2**).
* **V-31 full-tree closure:** 41 registry rows, 0 stray `ABS-*` anywhere in the tree, 0 census ids missing. ✅

### ✅ (8) `config_of_record.json` names **all five** T-A arms — not only the arm of record

`V0-ARM-M0` · `V0-ARM-M-POL-2` · `V0-ARM-M-POL-2-NULL` · `V0-ARM-W1` · `V0-ARM-W1-NULL` — five
per-arm rows, each a **delta** against the 45 base rows rather than a second copy, each with its
`sealed_terminals` and a one-line `what_this_arm_is`. `V0-ARM-W1` is explicitly labelled
*"its OWN seal, not this one."* KP-5(1) / KP-13 satisfied. *(But see **WARN-3** on `V0-LAW-1`.)*

The 54-row composition matches the member's own claim (35 driver-of-record + 6 module-default +
4 absent + 5 per-arm + 3 known-bad + 1 law). Placement matches prereg § 3 **rowset for rowset**:
54 / 355 / 171 / 62 / 81 / 10 / 51 / 4 / 3 = **791**, and `meta.json · ⚑ v3p2_lift · index` agrees
with the bytes on all 21 entries (member **and** count).

### ✅ (9) Stale values — every one appears ONLY inside an explicit correction

I grepped the whole tree for each named hazard and read every hit in context:

| value | occurrences | disposition |
|---|---|---|
| **×2.0 Banner** | 5 (`arena.json` ×3, `config_of_record.json` ×2) | all inside *"THE BANNER IS ×1.031887755102041 … NOT ×2.0"* / *"a ×2.0 build overstates the term by 93.8 %"* |
| **θ 0.49** | 6 (`player_kit.json` ×4, `config_of_record.json` ×2) | all inside *"THETA OF RECORD IS 0.2297…, NOT 0.49"* or `status: NOT-IN-CELL-OF-RECORD` |
| **three known-bad limbs** | `I8_LEGACY`, `I4_EXCURSION_MAX`, `POLL_AT_SLOT` | each carries **STATUS**; two stamped `NOT-IN-CELL-OF-RECORD`, `POLL_AT_SLOT` stamped `⚑ LIVE ON THE CELL OF RECORD` |
| **"~13 draw sites"** | 1 | shipped as `census_claim_superseded: "'>= 13 sites across >= 7 streams'"` beside `live_sites_found: 29` |
| **72** | **0** | absent from the tree entirely |

**No unmarked stale value found.** Item (9) is clean.

### ⚑ Explicitly-checked non-finding, recorded because it was my sharpest BLOCK hypothesis

**V-1…V-27 run over a view that excludes the three new members — so does substantive content ship
ungated?** I opened all three. Each carries **exactly five top-level keys**: `_do_not_hand_edit`,
`_minted_at`, `_schema_version`, `⚑ what_this_is`, and `⚑ v3p2_rows`. There is **no substantive
content outside the rows block**, so the view's exclusion opens **no gate hole** — the rows are
covered by V-28/V-30 and the whole tree by V-31. Hypothesis refuted against the bytes (Discipline #11).

---

## 2 · WARN — four

### ⚑ WARN-1 — **V-21 did not run, and two documents say it did while a third leans on its authority**

**What.** The receipt carries **30 gate ids: V-1…V-20, V-22…V-31. `V-21` is absent.** The arithmetic
that makes 30 honest is **26 carried + 4 minted**, not 27 + 4. But:

* prereg § 5.1: *"**V-1 … V-27** run exactly as at v3.1"*
* MIGRATION.md § 5: *"**V-1…V-27** carried forward unchanged over the dialect view, plus four minted"*

Both are **false of V-21**. And both documents, in their most load-bearing paragraph, cite V-21 as the
live authority for the cut's central decision — prereg § 5.1 and MIGRATION § 4:
*"reshaping gamora's rows … **the failure V-21/K-7 exist to refuse**"* (also `emit.py:493`,
`emit.py:820`, `schema.py:32`). **The cut invokes a gate it did not run, in the sentence that
justifies its most consequential choice.**

**Root cause, traced.** V-21 was **cut-local to v3.1**, never folded into the shared base validator.
The v3.1 receipt reports `V-21_carried_rows` (`byte_equal: true`, 332 rows re-derived from the seal,
14 rowset census), but `kc2_baton_v3_schema.validate_v3` — which `validate_v3p2` calls at
`kc2_baton_v3p2_schema.py:346` — implements no V-21. It only *mentions* it, at `:135`, `:255`, `:351`.
So the v3.2 cut inherited a 26-gate base and described it as 27.

**Why this is WARN and not BLOCK.** V-21's *substance* is covered, twice over: (i) my own additivity
walk shows **0 of 41,212 v3.1 rows changed a byte**, and the 332 carried rows are a subset of those
41,212; (ii) v3.1's own V-21 proved those 332 byte-equal to the seal, and v3.1's bytes are
re-verified untouched at POST (V-27, 4 predecessors). **The carried rows are provably still the
seal's rows.** Nothing about the pack is wrong. What is wrong is a sentence in the consumer-facing
document.

**Why it is a WARN and not an INFO.** star-lord quoted the governing principle into this pack's own
`registry_law` at v3.1: *"a stated law with seven live exceptions is worse than no law, **because a
consumer trusts it**."* This is that shape with one exception instead of seven, in the paragraph most
likely to be quoted forward — and the next cut that reasons *"V-21 refuses this, so I needn't check"*
is relying on a gate that has not executed since 2026-08-26.

**Evidence:** receipt `validation` key set (no `V-21*` key; `n_gates: 30`) ·
v3.1 receipt `validation.V-21_carried_rows` · `kc2_baton_v3p2_schema.py:346` ·
`kc2_baton_v3_schema.py:135, 255, 351` · prereg § 5.1 · `MIGRATION.md` § 5.

**Discharge (no re-cut; documentation + one queued gate):**
1. Amend the prereg's and MIGRATION § 5's phrasing to **"V-1…V-20 and V-22…V-27"** with a one-line
   footnote: *"V-21 was cut-local to v3.1 and is not in `validate_v3`; its substance is covered at
   v3.2 by the additivity check (0 of 41,212 rows changed a byte) plus v3.1's own V-21."*
2. Where V-21 is cited as authority (prereg § 5.1, MIGRATION § 4, `emit.py:493/820`, `schema.py:32`),
   either say **"V-28/K-7"** — which *did* run and *does* refuse the move — or keep V-21 with the
   footnote. **Do not leave a citation to a gate that has not run in a month.**
3. Queue V-21 for folding into `validate_v3` at the next cut, so the claim becomes true rather than
   footnoted.

*Cites: Discipline #1.2 (a claim must cite what actually ran) · Discipline #9 (attribution clarity) ·
REVIEW_PROCESS #2 · this pack's own `registry_law`.*

### WARN-2 — `pack_digest_law` does not fix the join's byte form, and GL-6 makes the guess a LOAD ABORT

**What.** The law reads *"sha256 of the **newline-joined** `<relpath>  <sha256>` lines, sorted by
relpath"* and then: *"A member whose digest fails is a **LOAD ABORT**, not a warning."* I had to
compute **both** readings to find the right one:

| reading | model pack | |
|---|---|---|
| **no trailing newline** (`"\n".join(lines)`) | `9ab771ef2fa27fba…` | ✅ the pack's own claim |
| trailing newline (a line-per-`\n` writer) | `38da8c4b107ffb0e…` | ❌ |

Writing `line + "\n"` per member is the more common idiom in a naive port, and it is a **silent**
wrong answer: the consumer gets a well-formed 64-hex digest that simply differs, and GL-6 instructs
it to **abort loading a valid pack**. The runtime spec's own load-gate (§ 1 item 1) also says only
*"verify the pack digest"* and does not pin the byte form either — so the ambiguity is **unclosed on
both surfaces the consumer reads.**

⚑ **This is inherited from v3.0/v3.1 and I did not raise it then** — I silently resolved it by trial
at the v3.1 gate and moved on. It becomes worth raising **now** because v3.2 is the first pack drax
actually configures `ORACLE` from, making GL-6 executable in GDScript for the first time.

**Evidence:** `…v3p2…/manifest.json:83` and `…reference…/manifest.json:46` ·
`2026-08-25-kc2-mc-w4-godot-runtime-spec.md:30`.

**Discharge:** add one sibling key, e.g.
`"pack_digest_law_exact": "digest = sha256(\"\\n\".join(lines)) — NO trailing newline; two spaces between relpath and sha256"`,
and mirror the sentence into the runtime spec § 1 load-gate. Pack-external; does not touch a member.
*Cites: Discipline #8 (schema validation at boundaries) · REVIEW_PROCESS #3 (cross-seam impact).*

### WARN-3 — `V0-LAW-1.arm_order` carries a dangling arm name and omits two arms the same rowset ships

**What.** `config_of_record.json · v0_fold_limb_of_record · V0-LAW-1 · value.arm_order` reads:

```
["M0", "M-POL-2", "M-POL-2-NULL", "M-POL"]
```

Two problems in one field. **`M-POL` resolves to nothing** — I grepped the whole model tree: it
occurs **exactly once**, here, and there is no `arm_config.M-POL` row in the pack. And **`W1` /
`W1-NULL` are absent from the order** although the *same rowset* ships `V0-ARM-W1` and
`V0-ARM-W1-NULL`. The row's own note — *"T-A must run the SAME five salts in the SAME arm order"* —
invites a reader to treat this list as the arm-of-record enumeration, which it is not.

**This is not a cut defect.** The row is gamora's, byte-for-byte (V-28 ✅), and its `provenance`
points at the M-POL-2 driver's `ARM_ORDER` constant, which predates the W1 arms — so it is **faithful
transcription of a pre-W1 constant.** The cut authored no `scope` and no `precedence` and was right
not to (prereg § 8). But it **shipped unmarked**, and it is precisely the shape the cut went out of
its way to close elsewhere: `ABS-W2-CAST-MIX` was minted because *"it was a DANGLING REFERENCE … cited
by name with NO REGISTRY ROW."* V-31 closes `ABS-*` ids only; **nothing in the 30 gates reaches an arm
name.**

**Evidence:** `model/config_of_record.json` · `⚑ v3p2_rows.v0_fold_limb_of_record[V0-LAW-1].value.arm_order`
(member line ≈ 511) · the five `V0-ARM-*` rows in the same array.

**Discharge:** do **not** edit the sealed row. Add a `⚑ v3p2_note` **beside** `V0-LAW-1` — the same
in-place-annotation pattern V-29 already uses — saying that `arm_order` is the M-POL-2 driver's own
pre-W1 constant, that `M-POL` has no `arm_config` row in this pack, and that the arm enumeration of
record is the five `V0-ARM-*` rows. Route the stale constant back to gamora for the next lift.
*Cites: Discipline #12 (semantic shift must be marked) · REVIEW_PROCESS #3 · prereg § 6(2) precedent.*

### WARN-4 — the LIFTED-status key is not uniform, and the one row it misses is the one whose `why` is now false

**What.** v3.1's Gate-2 WARN-2 remediation established that a `LIFTED`-class absence row carries
`⚑ v3_lift_status` to say what its stale `why` has been superseded by. **Eight of the nine LIFTED rows
do.** `ABS-MONSTER-MITIGATION` — retired into `LIFTED` **by this cut** — carries
`⚑ v3p2_status` and `⚑ v3p2_prior`, and **no `⚑ v3_lift_status` at all.**

It is the one row where this bites hardest. Its `why` still reads, as a live claim:

> *"NONE-MODELLED on the monster side, BY CONSTRUCTION … A runtime that adds a mitigation term on top
> of eHP **will double-count**."*

That sentence is now **false of v3.2** — the V6 order **must** be applied per body — and a consumer
following the v3.1 rule *"on a LIFTED row, read `⚑ v3_lift_status`"* reads **nothing** and is left
holding the false `why`. **The correction is present; it is under a key the established reading rule
does not look at.**

**Not BLOCK** because the same correction ships at three louder surfaces: the in-place
`⚑ v3p2_superseded_by` at `monsters.json :: mitigation_note` (V-29 surface 2, verified), MIGRATION § 1
and § 3, and `⚑ v3p2_status` on the row itself. A builder is warned; a **programmatic** consumer
keyed to `⚑ v3_lift_status` is not.

**Evidence:** `model/provenance.json · absence_registry[ABS-MONSTER-MITIGATION]` (has `⚑ v3p2_status`,
`⚑ v3p2_prior`; no `⚑ v3_lift_status`) vs the eight rows `ABS-AI-STATE-MACHINE`,
`ABS-MONSTER-STAT-BLOCKS`, `ABS-WAVE-ROLL-POOLS`, `ABS-DOT-STACKING`, `ABS-CONTROL-APPLICATION`,
`ABS-SUMMON-BODIES`, `ABS-DEVOTION-PROCS`, `ABS-CRIT-MODEL` (all carry it).

**Discharge:** add `⚑ v3_lift_status` to `ABS-MONSTER-MITIGATION` pointing at `V6-RETIRE-1` (one key;
`⚑ v3p2_status` may stay), and extend V-24 or V-25 with a clause: *every `class: "LIFTED"` row carries
`⚑ v3_lift_status`.* That converts a convention into a gate, which is what the v3.1 remediation
intended.
*Cites: Discipline #12 · jack-ryan Gate-2 v3.1 WARN-2 (carried forward) · REVIEW_PROCESS #4.*

---

## 3 · INFO — four

**INFO-1 — `V-23_sites` breaks the receipt's own key convention.** Every other gate's `<gate>_sites`
key holds **violation** sites and is empty on green. `V-23_sites` holds **6 SATISFIED** sites
(`satisfied_by: "carrier_block" | "row"`), while the empty list is `V-23.violation_sites`. Any
automated Gate-2 scan of the shape *"any `*_sites` non-empty ⇒ red"* — which is the obvious way to
read a 90-key validation block — **false-alarms on V-23 with six phantom violations.** Rename to
`V-23_in_scope_sites`, or move the satisfied list under the `V-23` sub-object.
*Evidence:* receipt `validation.V-23_sites` vs `validation.V-23.violation_sites`.

**INFO-2 — the `class` enum V-24 gates against is not published on the wire.** `provenance.json`
publishes `grade_enum` (4 values, plus a `grade_enum_note`); it publishes **no class enum**. V-24's
6-value enum (`NOT-YET-DECODED`, `UNDECODABLE`, `UNDECODABLE-FROM-SUBSTRATE`, `OUT-OF-CHARTER`,
`DECODED-NOT-YET-LIFTED`, `LIFTED`) lives only in validator code, so a consumer cannot validate a
`class` it reads, and `LIFTED`'s non-obvious semantics (*the data this absence named is IN THIS pack*)
are recoverable only from prose inside one row. Add `class_enum` + a `class_enum_note` beside
`grade_enum`.

**INFO-3 — the rowset→member index now exists in two packs and nothing gates their agreement.**
`model/meta.json · ⚑ v3p2_lift` and `reference/meta.json · ⚑ v3p2_lift` both carry the full 21-entry
index. I verified **both agree with the bytes today.** No gate compares them, so a future single-sided
edit drifts silently. Cheapest fix: extend V-31 with a cross-pack index-equality clause.

**INFO-4 — V-30(b)'s green is a property of a constant, and it is worth saying so.** *"Exactly one
distinct `scope` across all 791"* is true — I confirmed it: every row reads
`"cell:M-POL-2@E-s09-cp150"`. But that includes `V0-ARM-W1` and `V0-ARM-W1-NULL`, whose own text says
*"its OWN seal, not this one."* So the scope field is a **constant the emitting artifact stamps**, not
a discriminator the rows earned — and the DR-3 tie hazard is structurally absent because nothing is
scoped, not because scoping was disciplined. The gate's wording (*"structurally absent, not merely
unobserved"*) is accurate and I am not asking for a change here; **this routes to gamora's next lift**,
where a second arm's rows would make the constant actively misleading. Naming it now so the next cut
does not inherit a green gate whose meaning has quietly changed.

---

## 4 · WHAT I WOULD SINGLE OUT AS GOOD

1. **V-29 is the right gate and it was minted for the right reason.** *"A lift that lands 791 correct
   rows beside an unmarked `hit_test_model: "point"` has shipped the trap it was written to remove."*
   Nine surfaces, enumerated **in the prereg before the emitter existed** and transcribed into
   `SUPERSESSION_SURFACES` with a comment saying exactly that — so the gate could not be authored to
   fit what got built. I verified the code table against the prereg table: **identical, all nine.**
2. **Declaring SIX carries over NINE surfaces against the brief's SEVEN, and printing the
   reconciliation.** *"The ARTIFACT governs"* — with the difference named rather than resolved to
   whichever number was convenient. That is Discipline #9 under mild pressure to round.
3. **The one honest-fail is honest.** `ABS-EOR-RANK-OF-RECORD` ships with three mutually inconsistent
   readings on the wire, `runtime_choice_required: true`, and an explicit
   `⚑ consequence_if_a_runtime_guesses`. Picking a rank would have made every gate greener and the
   pack wrong.
4. **`P-1` reported and never gated.** *"A non-zero P-1 is not a failure of the cut; concealing it
   would be."* Seven blockers listed by id.
5. **The prereg landed ALONE, zero code (D4), and its sha re-derives** to `957ac23d…` as pinned in the
   receipt; gamora's prereg to `dc4eea47…`. Pins **derived at emit, not retyped** (G-1 / charter
   WARN-10) — I re-derived both by hand and both match.

---

## 5 · ACTION

- [ ] **star-lord — WARN-1:** correct the "V-1…V-27" phrasing in prereg § 5.1 and MIGRATION § 5 to
      "V-1…V-20, V-22…V-27" + footnote; re-point or footnote the five V-21 authority citations; queue
      V-21 for folding into `validate_v3`. **Documentation + a queued gate — no re-cut.**
- [ ] **star-lord — WARN-2:** add `pack_digest_law_exact` to both manifests; mirror into runtime spec § 1.
- [ ] **star-lord — WARN-3:** add a `⚑ v3p2_note` beside `V0-LAW-1`; do not edit the sealed row.
- [ ] **star-lord — WARN-4:** add `⚑ v3_lift_status` to `ABS-MONSTER-MITIGATION`; extend V-24/V-25
      with *every `LIFTED` row carries `⚑ v3_lift_status`*.
- [ ] **star-lord — INFO-1..3:** rename `V-23_sites`; publish `class_enum`; gate the two lift indices.
- [ ] **gamora — WARN-3 / INFO-4 (next lift):** `V0-LAW-1.arm_order` is a pre-W1 driver constant
      carrying a dangling `M-POL` and omitting W1 / W1-NULL; and the single constant `scope` will
      mislead the moment a second arm's rows are lifted.
- [ ] **gandalf (RUN-CONDUCTOR):** **charter § 4 row 1 is SATISFIED — no BLOCK outstanding.** The cut
      is releasable as it stands; the four WARNs are follow-ups, not gates. Release/push is yours.
- [ ] **Matt — no decision required.** ADR-002: `_schema_version` stays **3**, `pack_format` stays
      `kc2-model-pack/v3`, no consumer contract moves, and MIGRATION.md is present and complete per
      **ADR-004** — so this is within my tier to pass. Milestone tagging, if it is ever proposed for
      this pack, remains yours.

**Empirical criterion that gates re-engagement:** a v3.3 (or remediation) receipt whose gate-id set
includes **`V-21`**, and whose `V-24`/`V-25` block reports a `LIFTED`-row `⚑ v3_lift_status` clause.
Until one of those exists, WARN-1 and WARN-4 stay open on the record.

---

## 6 · REFERENCES

**Under review (engine, `~/Games/reincarnated-engine/`):**
- `/Users/admin/Games/reincarnated-engine/src/reincarnated/output/kc2-model-pack-v3-E-s09-cp150-mech-v3p2-20260920_214030/` (15 members; `manifest.json:83` = `pack_digest_law`)
- `/Users/admin/Games/reincarnated-engine/src/reincarnated/output/kc2-reference-pack-v3-E-s09-cp150-mech-v3p2-20260920_214030/` (7 members)
- `/Users/admin/Games/reincarnated-engine/src/reincarnated/output/kc2-baton-v3-cut-receipt-v3p2-20260920_214030.json`
- `/Users/admin/Games/reincarnated-engine/src/reincarnated/export/MIGRATION.md` (top entry, § 1–§ 5)
- `/Users/admin/Games/reincarnated-engine/src/reincarnated/export/kc2_baton_v3p2_emit.py` (`:183`, `:239`, `:493`, `:712`, `:820`)
- `/Users/admin/Games/reincarnated-engine/src/reincarnated/export/kc2_baton_v3p2_schema.py` (`:32`, `:64` `SUPERSESSION_SURFACES`, `:153` `_resolve`, `:333` `validate_v3p2`, `:346`)
- `/Users/admin/Games/reincarnated-engine/src/reincarnated/export/kc2_baton_v3_schema.py` (`:135`, `:255`, `:316`, `:351` — **the base validator, which has no V-21**)
- `/Users/admin/Games/reincarnated-engine/src/reincarnated/export/math/2026-09-20-kc2-baton-v3-2-cut-prereg.md` (§ 4, § 5.1, § 5.2, § 6, § 7)

**Inputs of record:**
- `/Users/admin/Games/reincarnated-engine/src/reincarnated/simulation/output/kc2-lifted-rows-KC2PLAY-W1-v3p2-full-20260920_163932.json` (`e011742935f14efa…`)
- `/Users/admin/Games/reincarnated-engine/src/reincarnated/simulation/math/kc2-play-v3p2-lift-prereg-2026-09-20.md` (`dc4eea4794f4997f…`)
- `/Users/admin/Games/reincarnated-engine/src/reincarnated/output/kc2-model-pack-v3-E-s09-cp150-mech-v3p1-20260826_031143/` · `…-reference-pack-…-v3p1-20260826_031143/`
- `/Users/admin/Games/reincarnated-engine/src/reincarnated/output/kc2-baton-v3-cut-receipt-v3p1-20260826_031143.json` (**`validation.V-21_carried_rows` — the gate that ran at v3.1 and not at v3.2**)
- sealed cells: `kc2-checkpoint-E-s09-cp150-{mpol2-20260825_114420, mech-20260816_124031, w1walls-20260825_220058}.json`

**Governing (collaboration, `~/Games/reincarnated-collaboration/`):**
- `/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/gandalf/notes/2026-09-20-kc2-play-run-charter.md` (§ 1, § 4 row 1, § 7; S-6 pins at `:25`)
- `/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/gandalf/notes/2026-08-25-kc2-mc-w4-godot-runtime-spec.md` (`:30` load-gate)
- `/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/qa/findings/2026-08-26-kc2-lift-gate2-baton-v3p1.md` (the bar and the V-gate vocabulary; WARN-2 carried forward as **WARN-4**)
- `/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/GOVERNANCE.md` (ADR-002, ADR-004, ADR-006)

---

*Gate-2, DEV-MODE. Read-only except this file. Digests derived from member bytes, not read off the
receipt; row fidelity run at 791/791 rather than the sampled 40; the blocker-view predicate re-run
rather than trusted; sealed cells hashed, never opened. No push.*
*jack-ryan — 2026-09-20.*
