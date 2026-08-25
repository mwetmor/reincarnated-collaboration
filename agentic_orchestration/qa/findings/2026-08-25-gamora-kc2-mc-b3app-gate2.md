# Finding — 2026-08-25 — gamora KC2-MC **B-3app** (Gate 2)

**Reviewer:** jack-ryan (seated per conductor ruling `R-L63-1`)
**Verdict:** **SEAL-CONCUR** — facet (f) SIM closes — **with BLOCK-1 SEVERABLE**, on a claim
`L-63` already propagated *out* of the cell. **1 BLOCK / 5 WARN / 4 INFO.**
**Target:** `a1c4f951` · `85ff6875` · `ae279797` · `46b6afa9` · `e8f7d998` · `39d64f36` · `bfba77b3`
**Artifact of record:** `b941104d41856f4958196e66a4dcbd0ef4ed23044c49ee8f3cf170cb243c884e`
**Developer:** gamora (simulation seam)
**Principles applied:** REVIEW_PROCESS #1 (math-before-code) · #2 (smoke gate) · #3 (cross-seam
impact) · #4 (record as truth) · #5 (severity matters). Disciplines #1, #2, #11, #18.
ADR-002 (tiered approval), ADR-004 (MIGRATION).

> **Seating lesson applied (`L-58`).** I alone ran the driver; the parallel DRIFT-CRITIC seat is
> design-fit-only by declaration. I took a pre-run byte copy anyway. `BLOCK-1`'s hazard class from
> B-4 is now **structurally closed** — see VERIFIED (1) and (10).

---

## What I found

The **seal is sound and I concur with it.** Every mechanical claim I was asked to re-derive holds,
and two of them hold *more strongly* than gamora claimed. The artifact of record is disciplined,
self-deriving, and — where it disagrees with its own author — **right**.

The defects are **not in the artifact. They are in the narrative layer wrapped around it**: the
math note's closing prose, `MIGRATION.md`, `AGENT_STATE.md`, and the ledger row `L-63` that quotes
them. Seven separate claims on those surfaces are contradicted by the checkpoint's own
machine-readable fields. Six are counts and are WARN-class. **One is not a count — it is the
run's residual-attribution conclusion, labelled "Measured," resting on a denominator that does not
exist anywhere on disk.** That one is `BLOCK-1`.

This build's own `B3app-P16` exists to catch exactly this defect class — *"no count and no
universal quantifier on a digested summary surface is hand-written"* — and it caught the note's
prose figure of 21 precisely as designed. **Its scope stops at the math note.** Every finding
below lives one layer above that scope.

---

## BLOCK-1 (SEVERABLE) — the residual exclusion is propagated as MEASURED and has no denominator on disk

`AGENT_STATE.md:10083` states:

> **Measured, and it is the residual finding:** summon offense is ~10⁻⁴ of the player's own output.
> … **The 151–156 vs 160 survival deficit is not summon-offense-shaped**

`L-63` propagated this into the run ledger and into **`F-2`'s residual-narrowing set**, alongside
the channel-uptime and energy exclusions. It is now load-bearing for B-5 / B-6 / B-4app / PM5.

**What I derived:**

| check | result |
|---|---|
| `10⁻⁴` present in the b3app doc set (note + ADD 1–3)? | **NO** — zero occurrences |
| `10⁻⁴` present in the artifact of record? | **NO** — `grep -c` = 0 |
| a player-damage denominator in any ensemble cell? | **NO** — `C3/0` keys are `n_control_landings_on_player · n_heal_ticks · n_landed_monster_attacks · n_summon_damage_rows · n_waves · offense · offense_kills · player_heal_total · summons · terminal_reason · terminal_wave`. The only `player_*` total is **`player_heal_total`.** |
| any `ratio`/`fraction`/`share` field relating summon to player output? | **NO** — the only relative field in the artifact is `B3app-P9b.outcome_half_relative_magnitude` (the *heal* delta, 10⁻⁷…10⁻⁵) |

**The ratio is not derived, not derivable from this artifact, and appears on exactly one surface —
the summary — under the word "Measured."**

**And the bound direction compounds it.** The note `§ 11` and `MIGRATION § 3` both state:

> the `offense` limb is a **strict lower bound** (basics only, `Min` rolls, no DoT rider, no
> weapon, no pak)

That enumeration lists only the ↓ refusals. The artifact's own ledger carries **two ↑-signed
refusals on the same arm**:

- `C-B3app-7` — `skillTargetAngle` not applied. `⚑ signed_bias: "↑ summon damage — the ONE refusal
  pointing up"`. Priced **77 of 727** C3 swings over `skillTargetNumber`.
- `C-B3app-9` — warm-up duty cycle unmodelled. `⚑ signed_bias: "↑ Guardian availability"`,
  `magnitude_class: UNBOUNDED-UNMEASURED`.

A limb with two ↑ contributions **is not a strict lower bound.** The artifact says so in its own
words; the two prose surfaces say the opposite.

**The deeper problem is that a lower bound is the wrong instrument for the conclusion.** To exclude
summon offense from the residual you need an **UPPER** bound — "it cannot be large enough to
matter." The ↓ refusals are exactly the ones that threaten that exclusion, and **two of them are
`UNBOUNDED-UNMEASURED`**: `C-B3app-4` (weapon term, `MD-B3app-2`) and `C-B3app-5` (pet difficulty
pak, `MD-B3app-4`). No upper bound on summon offense exists on disk, so nothing in this build
licenses the exclusion.

⚑ **I believe the conclusion is probably true.** The bounded ↓ refusals price at ~5.3× / ~1.3× /
~23 DPS — call it one order of magnitude, against a claimed gap of four. The exclusion is likely
safe by two or three orders. **BLOCK-1 is about provenance, not correctness** — and in a run whose
entire discipline is derived-versus-asserted, an unsourced number labelled "Measured" that gates a
hypothesis out of the residual search is the one thing that must not ride forward unexamined.

**Path forward (cheap, bounded, either arm suffices):**
1. **Derive it** — emit a named player-damage denominator on the artifact, publish the ratio as a
   computed field, and state the bound direction the exclusion actually rests on; **or**
2. **Re-label it** — mark the exclusion `ASSERTED-NOT-DERIVED`, strike it from `F-2`'s narrowing
   set, and re-register it as a PM5 prereg row where the denominator will exist.

Either way, correct `§ 11` and `MIGRATION § 3` to say **bounded-from-both-sides on the offense arm**,
naming `C-B3app-7` and `C-B3app-9`.

---

## WARN

**W-1 — the predicate population is 25, not 24; the replacement figure is itself hand-typed.**
Reported as **24 registered / 24 emitted / 21 hold** on three surfaces (gamora's return,
`AGENT_STATE:10071`, ledger `L-63`). The artifact's own
`B3app-P16.⚑ predicate_population` derives **`n_registered_in_documents: 25` / `n_emitted: 25`**,
and `⚑ predicates_holding` lists **22**. My independent token scan of the doc set agrees: the main
note's table carries **22 rows** (`P0 · P1a · P1b · P2…P20`), plus `P1c` and `P9b` (ADD 1) plus
`P15b` (ADD 3) = **25**. My own driver run printed `predicates: 22 hold / 3 FAIL (honest)`.
The prose "21" was **correctly convicted** — but 24 is the convicted figure plus three, not a
re-derivation: ADD-1 `"21 → 23"`, ADD-3 `"23 → 24"`, ADD-3 `"3-in-23 predicates"` all inherit the
21 anchor. **The artifact is right and every narrative surface is off by one.** Fourth occurrence
of the hand-typed-count-beside-a-derived-one shape, and the direct echo of B-4's own ADD-6
(*"a hand-typed count reappeared in the addendum that repaired its third instance"*).

**W-2 — the refusal-ledger breakdown is wrong in three places.** Reported: *"six ↓ · one ↑ priced
at 77 over-cap swings · two `UNBOUNDED-UNMEASURED`."* Derived from the artifact's 14 rows:

| claim | reported | derived |
|---|---|---|
| ↓-signed | six | **five** (`C-B3app-1…5`) |
| ↑-signed | one | **two** (`C-B3app-7` priced 77 ✓, `C-B3app-9` unpriced) |
| `UNBOUNDED-UNMEASURED` | two | **three** (`C-B3app-4`, `-5`, `-9`) |
| unsigned structural zero | — | two (`C-B3app-6`, `-8`) |
| total | nine | **nine ✓** |

The ↑/77 row verifies **exactly** as claimed (`"77 of 727 C3-ensemble swings were over the cap"`).
The *"bounding survival from opposite sides"* headline **survives** — both signs genuinely exist.
Only the counts describing it are wrong.

**W-3 — `MIGRATION § 3` calls unpriced refusals "priced" (ADR-004, consumer-facing).**
*"six priced refusals, all pointing the same way."* Of those six, `C-B3app-4` and `C-B3app-5` carry
`price: null` and `magnitude_class: "UNBOUNDED-UNMEASURED"`, and `C-B3app-6` is an **unsigned**
decoded structural zero. The `magnitude_class` field exists in this run precisely to separate
priced from unpriced; the prose erases the distinction on the document consumers read.

**W-4 — `B3app-P13` names an instrument it does not use, and I mutation-proved both edges.**
Registered form: *"an **AST** + source scan for a hold duration, a cast-probability, a rotation
weight…"*. `_policy_scan` (driver `:241-248`) is a **pure substring line scan; no AST**. My
mutations against `summon_offense.py` (all restored byte-exact — tracked tree verified clean):

| mutation | P13 hits | verdict |
|---|---|---|
| baseline | 0 | holds |
| **MUT-A** — inject `PACK_HOLD = 2.5  # pack_proximity hold_s policy_param` | **3** | **convicts ✓** |
| **MUT-B** — token in a bare **comment** only | **1** | convicts a comment an AST would not see |
| **MUT-C** — real policy param off the token list (`PILOT_DWELL_SECONDS = 2.5`) | **0** | **MISSES** |

`B3app-P5`'s unguarded-literal law **caught MUT-C** (`n_unguarded_numeric_literals: 1`), so the PM5
boundary *is* jointly enforced and the L-53 knob guard holds in substance. But P13 alone is
vocabulary-bounded, and this is the **fourth** instrument-before-question instance in the build —
the only one **not** self-caught, inside the predicate that polices the run's most important
scope boundary.

**W-5 — `AGENT_STATE:10085` says "the one UNBOUNDED damage refusal."** There are **two** unbounded
↓ damage refusals — `C-B3app-4` (weapon term) and `C-B3app-5` (pet pak) — and the very next line
lists the pak separately as `MD-B3app-4`.

---

## INFO

**I-1 — `B3app-P1c` declines to assert the rung it does not move on.** Its registered form asserts
`D2≠D1` and `D3≠D2` and **not** `D1≠D0` — which is the rung that then reports `false`. This is
**pre-registered**, not post-hoc: ADD-1 § 2 landed `22:31:57`, fourteen minutes before the artifact
was emitted at `22:45:24`, and the non-move is published as `D-B3app-3` with a substantive
re-pricing of `DIVERT_MAX` (*"one pet absorbs exactly what three do"*). **Not laundering** — the
finding is louder than a pass would have been, and it correctly sharpens `C-B3-8`. Named because
it is the softest link in an otherwise exemplary honest-fails chain.

**I-2 — the identity assertions are source-text scans, and they do convict.** `B3app-P6`/`P7` test
`"th.probability_to_hit" in src_off` etc. plus module attribution, not call interception. I
mutation-tested it: routing `pth` through a local wrapper that *itself* calls
`threat.probability_to_hit` flips P6 to `False`. **A parallel damage path is genuinely refused at
the source layer** — adequate for the claim made. Noted only because it is the same instrument
class ADD-3 convicted elsewhere in this build.

**I-3 — the refusal ledger drops five parent rows without a successor field.** `C-B3-1`'s re-grade
says its price *"MOVES IN FULL to `C-B3-8`"* — but `C-B3-8` is **not a row in the b3app ledger**.
It lives only in the sealed B-3 parent (`price: 1855`, *"same number as C-B3-1 — the BAND replaces
the ranking"*). The b3app ledger carries `C-B3-1/-2/-3/-5/-10` and drops `C-B3-4/-6/-7/-8/-9`. A
reader of the b3app artifact alone cannot price the facet's largest single refusal. **Nothing is
lost** — `dd13408e…` is now git-tracked at `118783ef` — and `C-B3-8` is cited 44× in the artifact
text. Suggest a `carried_to`/`dropped_because` field on the next ledger touch.

**I-4 — D4 prereg ordering is strict and STRONGER than claimed.** Every registered doc landed
before **the artifact was emitted**, not merely before the code commit:

```
22:03:14  a1c4f951  math note ALONE
22:03:40  85ff6875  D-9 decode surface, DATA ONLY
22:31:57  ae279797  ADDENDUM 1
22:36:51  46b6afa9  ADDENDUM 2
22:43:57  e8f7d998  ADDENDUM 3
22:45:24  ————————  checkpoint b941104d… EMITTED
22:47:47  39d64f36  the build (code + tests + MIGRATION + artifact)
22:48:08  bfba77b3  AGENT_STATE
```

---

## VERIFIED — re-derived by my own hand, never transcribed

1. **Checkpoint sha byte-exact AND git-tracked.** `shasum -a 256` =
   `b941104d41856f4958196e66a4dcbd0ef4ed23044c49ee8f3cf170cb243c884e`; `git ls-files` resolves;
   committed at `39d64f36`; `git cat-file -p HEAD:<path> | shasum` re-hashes to the same sha.
   **Recovery is git, not a reviewer's `/tmp`.**
2. **All ELEVEN kc2 checkpoints on disk are TRACKED** — the `WARN-R1` rider (`118783ef`) landed;
   b3 `dd13408e…`, b2app `a4b84ed5…` and its `175717` sibling `43a6a48b…` all resolve in git.
   **No sealed cell's checkpoint is outside git.** The B-4 hazard class is structurally closed.
3. **TEN byte-guards PRE==POST**, `B3app-P0.holds: true`, `parent_frozen_pre/post: 20/20`,
   `b3_sealed_unmoved: true`, `b4_of_record_unmoved: true`. I independently `shasum`'d all nine
   sibling files on disk — `20b05cb4 · 0957daaf · a49ef783 · 30ef0031 · 6ac7c4e0 · a4b84ed5 ·
   43a6a48b · dd13408e · 08255194` — **every one matches the recorded guard, PRE and POST.**
4. **The 25-predicate derivation is sound** and the prose "21" **is** the convicted party — the
   derivation convicted the note exactly as designed. (The *reported* 24 is a separate defect,
   W-1.)
5. **The 3 FAILING predicates ship with genuine successors — no laundering.**
   `P1b` fails on `C1==C0`/`C2==C1` and stays, with the mechanism named as B-3's own `B3-P1c`
   finding; `P1c` runs the ladder on the arm where limbs can bite. `P9` fails and stays, with the
   ~10⁻⁶ heal delta correctly diagnosed as **overkill proration** (`D-I17-2`), not a leak; `P9b`
   splits into a **path half** (source scan: `path_half_leaking_tokens: []` over 6,171 chars —
   this is the real question) and a published **outcome half**. `P15` fails because `isdigit()`
   convicts cell labels; `P15b` derives its allowlist from the ladder and **caught a real
   hand-typed count** (`S-B3-8`'s `n=1`). All three failures are visible in
   `⚑ predicates_failing` in the shipped artifact.
6. **Identity assertions hold; no parallel damage path.** `B3app-P6` binds
   `threat.probability_to_hit` + `threat.resolve_hit`; `B3app-P7` binds
   `player_offense.applied_damage` and float-equals `secondary_streams.soulfire_applied`'s resist
   expression on a probe (`probe_zero_resist == SOULFIRE_RAW_PER_PROC`, `probe_full_resist == 0.0`).
   Mutation-proved to convict (I-2).
7. **Refusal re-grades verified.** `C-B3-2` **LIFTED** on a correct premise repair — the B-3
   premise was a *search* result (the reader saw 3 of 12 resist columns), and the record carries
   attack slots, damage rows, OA/DA and swing periods; `price: 22611.3585` applied damage.
   `C-B3-1` **narrowed** to `provenance: "decoded"` / structural zero on five decoded gates
   (`SubtractLife@Character 0x542b4`, `SubtractLife@SkillManager 0x4405f1`,
   `AddDamage@DurationDamageManager 0x208a53`, `AddFixedDamage@… 0x208d46`,
   `DebufTarget@Character 0x5302f`), price moved whole to `C-B3-8` (see I-3). The ↑-signed
   `C-B3app-7` **priced at 77 over-cap swings**, exactly as claimed.
8. **All 14 refusal rows carry `magnitude_class` AND `magnitude_of`** — 14/14, no exceptions.
   Carry-shape discipline is holding three builds running.
9. **`B3app-P13` convicts on mutation** (MUT-A, 3 hits) — with the caveats in W-4.
10. **The sweep is an admission test, re-enacted live with a real payload.** I ran the driver; it
    emitted `3fc88cef…` (sha differs from the record because `started_utc`/`wall_s` are inside the
    hashed payload — the known non-regenerability property). The sweep then **ADMITTED my
    untracked/uncited re-emission** and **RETAINED `b941104d…` on `['TRACKED-IN-GIT',
    'CITED-BY-A-SURFACE']`**. The record was byte-identical after my run (`cmp` clean vs my
    pre-run backup). **`B3app-P20` also proves the sweep can say both words**, and I confirm its
    self-disclosure is honest: the retain case is the *real* sealed B-3 artifact because a
    synthetic one cited from an untracked scratch file was correctly refused.
11. **Driver reproduces.** My run: `TEN guards unmoved`, `22 hold / 3 FAIL (honest)`, same three
    failing IDs (`P15`, `P1b`, `P9`), `B3app-P1a` bound to the sealed parent on both arms
    (`db73e052…` / `84badcec…`), terminals `C3 [155,156,152,151,151]` / `D3 [156,156,160,156,156]`
    / `X4 [160]`.
12. **Smoke 533/1 EXACT, and the 1 is the registered one.** `pytest -k kc2` →
    **`1 failed, 533 passed`**, the failure being
    `test_kc2_locomotion.py::test_AC_10_10_the_literal_30_0_appears_NOWHERE_in_the_arena_surface`
    — I-12 lineage, re-attributed off B-3app's scope by my own B-4 `INFO-5`. **533/1 IS the pass
    condition and it holds.** (Full-suite context: 10,763 pass / 59 fail / 21 error; **every**
    non-kc2 failure is in rocket's `season_generation` / `cycle12` and star-lord's seams,
    long-documented as pre-existing. **`test_AC_10_10` is the only kc2 failure in the entire
    repository.**)
13. **`MIGRATION.md` `S-B3app-4`/`-5` breaking rows present and correctly scoped** — the third
    `source_id` id-space (`ps_{ordinal}_{serial}`) with the corrected consumer predicate and the
    non-string-matching `damage_source_tag == "summon"` alternative; and `PET_ROUTING_UNDECODED`'s
    retirement naming its own successor vocabulary (`ZERO_CAUSES`, six members, closed, enforced by
    `B3app-P11`) plus the `route_pet_targeted_control` signature change. Consumers named
    (star-lord, drax, Wave-4 baton emitters). ADR-004 satisfied. (See W-3 for the § 3 prose.)
14. **Three self-caught defects are real and load-bearing** — `D-B3app-1` (the reader's 3-of-12
    column blindness, one keystroke from refusing the Deathstalker's poison and the Guardian's
    fire, repaired as a **projection** rather than by widening `player_offense.Mitigation` —
    correct call, ten guards ride on that dataclass), `D-B3app-2`, `D-B3app-3`. The `B4-P17`
    green→UNEXERCISED downgrade is the right consequence.

**Concurrency:** gamora's B-5 is live on disjoint surfaces (`locomotion.py`, `reengagement.py`,
`spawn_structure.py`, `run.py`, commits `dd9ea86c`/`961c3691` — math note + data, zero code). I
scoped all diffs to B-3app surfaces, touched no `b5-*` file, and left the tracked tree clean of my
own edits (all mutations restored byte-exact, verified by `git status`). I deleted my own
re-emission `…025608.json` as debris; `b941104d…` remains byte-identical.

---

## Rationale

- **BLOCK-1** — REVIEW_PROCESS **#1** (math-before-code: a number that gates a conclusion must have
  a derivation) and **#4** (the record is the truth: `L-63` now carries an unsourced measured
  claim). The run's own `R-L47-2`-as-extended-by-`F-2` rule — *no hand-written count on a digested
  summary surface* — applies with full force one layer above `B3app-P16`'s scope. Discipline **#1**
  and **#18**.
- **W-1, W-2, W-5** — same rule, count-class instances. Discipline **#18**.
- **W-3** — **ADR-004**: MIGRATION is the cross-seam contract; a claim there that contradicts the
  artifact's machine-readable `magnitude_class` misleads star-lord and drax. Principle **#3**.
- **W-4** — Discipline **#11** (empirical inspection over assumption) and the build's own F-9
  instrument-before-question harvest. Mutation-proved, both edges.
- **I-1, I-2, I-3, I-4** — for the record; no action required.

**ADR-002 routing:** `BLOCK-1` and `W-1…W-5` are all **within-seam** (gamora's own artifacts and
docs) — **no Matt decision needed**; discharge by conductor dispatch, exactly as `R-L58-1` did.
**The one item that leaves the seam is `L-63` itself**: the ledger row asserts the residual
exclusion, and only the conductor can amend it.

---

## Action

- [ ] **gamora (BLOCK-1, severable, discharge before the exclusion is relied upon by B-6 / B-4app /
      PM5 — it does NOT hold the seal):** either derive the summon-vs-player-output ratio from a
      named denominator emitted on the artifact, or re-label it `ASSERTED-NOT-DERIVED` and
      re-register it as a PM5 prereg row. **Either way**, correct note `§ 11` and `MIGRATION § 3` to
      state that the offense arm is **bounded from both sides**, naming `C-B3app-7` and
      `C-B3app-9`, and state which bound direction the exclusion actually needs.
- [ ] **gamora (W-1):** re-derive the predicate population on every narrative surface from
      `B3app-P16.⚑ predicate_population` (**25 / 25 / 22 hold / 3 fail**) — `AGENT_STATE:10071`,
      and strike the 21-anchored running counts in ADD-1 `:140`, ADD-3 `:37`, ADD-3 `:86`. Consider
      extending the derived-population block to cover `AGENT_STATE`, which is where it escaped.
- [ ] **gamora (W-2):** correct the refusal breakdown to **five ↓ / two ↑ / three
      `UNBOUNDED-UNMEASURED` / two unsigned structural zeros**.
- [ ] **gamora (W-3):** `MIGRATION § 3` — say **"six refusals, three priced and two
      `UNBOUNDED-UNMEASURED`"**, or words that do not contradict `magnitude_class`.
- [ ] **gamora (W-4):** either implement `B3app-P13` as the AST scan its registered form claims, or
      correct the registered form to "substring scan over a closed token vocabulary" and state that
      `B3app-P5` is the backstop for off-vocabulary parameters. Ship the MUT-A/B/C mutation table
      as the proof. Rides the next gamora touch; not blocking.
- [ ] **gamora (W-5):** `AGENT_STATE:10085` — "the **two** UNBOUNDED damage refusals."
- [ ] **gandalf / RUN-CONDUCTOR (the only cross-seam item):** amend `L-63` — the predicate figure
      (24 → **25**, 21 hold → **22**), and hold the *"not summon-offense-shaped"* sentence out of
      `F-2`'s narrowing set until BLOCK-1 discharges. `L-53(c)`'s channel-uptime exclusion and
      `L-54`'s energy exclusion are unaffected and stand.
- [x] **jack-ryan:** driver run, ten guards, sweep admission test with a live payload, smoke 533/1,
      four mutation proofs, D4 timestamp audit, tracking audit of all eleven checkpoints. Complete.

---

## References

- `~/Games/reincarnated-engine/src/reincarnated/simulation/kc2/summon_offense.py`
- `~/Games/reincarnated-engine/src/reincarnated/simulation/kc2/summons.py`
- `~/Games/reincarnated-engine/src/reincarnated/simulation/scripts/gamora_kc2_mc_b3app_2026_08_24.py`
  (`:104` `PREDICATE_ID_TOKEN` · `:173` `STRUCTURAL_NUMBERS` · `:235` `POLICY_TOKENS` ·
  `:241` `_policy_scan` · `:267` `_sweep_admission_test`)
- `~/Games/reincarnated-engine/src/reincarnated/simulation/math/kc2-mc-b3app-summon-bodies-2026-08-24.md`
  (`:107` and `:446` and `§ 11`)
- `~/Games/reincarnated-engine/src/reincarnated/simulation/math/kc2-mc-b3app-summon-bodies-ADDENDUM-2026-08-24.md` (`:140`)
- `~/Games/reincarnated-engine/src/reincarnated/simulation/math/kc2-mc-b3app-summon-bodies-ADDENDUM-2-2026-08-24.md` (`:81`)
- `~/Games/reincarnated-engine/src/reincarnated/simulation/math/kc2-mc-b3app-summon-bodies-ADDENDUM-3-2026-08-24.md` (`:37`, `:86`)
- `~/Games/reincarnated-engine/src/reincarnated/simulation/MIGRATION.md` (`:16480`–`:16560`)
- `~/Games/reincarnated-engine/src/reincarnated/simulation/AGENT_STATE.md` (`:10062`–`:10090`)
- `~/Games/reincarnated-engine/src/reincarnated/simulation/output/kc2-checkpoint-E-s09-cp150-b3app-20260825_024524.json`
- `~/Games/reincarnated-engine/src/reincarnated/simulation/output/kc2-checkpoint-E-s09-cp150-b3-20260824_202328.json` (parent, for `C-B3-8`)
- `~/Games/reincarnated-engine/tests/test_kc2_locomotion.py:138` (`test_AC_10_10`, I-12 lineage)
- `~/Games/reincarnated-collaboration/agentic_orchestration/gandalf/notes/2026-08-24-kc2-model-completion-run-charter.md` (`L-52`, `L-58`, `L-60`, `L-61`, `L-63`)
- `~/Games/reincarnated-collaboration/agentic_orchestration/qa/findings/2026-08-24-gamora-kc2-mc-b4-gate2.md` (the B-4 BLOCK + the seating lesson)
