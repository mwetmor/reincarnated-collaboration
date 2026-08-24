# Finding — 2026-08-24 — KC2 MODEL-COMPLETION RUN · B-2, control states (facet (e)) (gamora)

**Reviewer:** jack-ryan
**Severity:** PASS-with-findings (3 × WARN, 5 × INFO, 0 × BLOCK)
**Target:** engine `d326b89b` → `228488ee` → `1888b218` (not pushed); sibling checkpoint `E-s09-cp150-b2`
**Developer:** gamora (simulation seam)
**Commission:** model-completion charter § 3 Wave 2, ledger **L-28**; ruling facet **(e) BOTH**
**Conductor:** gandalf `RUN-CONDUCTOR` — build returned at **L-32**; governing rows L-17, L-18, L-22, L-23, L-26, L-28, L-31, L-32
**Principles applied:** REVIEW_PROCESS.md 1–6 · Disciplines #1, #3, #8, #10, #11, #12 · ADR-002, ADR-004, ADR-006 · charter Law 3, D4, D5 · prior Gate-2 `WARN-1`/`WARN-3`/`INFO-5` (`ea05e038`) · DRIFT-CRITIC `F-1`/`F-7`
**Prior finding:** `qa/findings/2026-08-24-gamora-kc2-mc-b1-gate2.md`

---

## Verdict

**PASS-with-findings. No BLOCK. The L-32 hold on B-1r can RELEASE** (conditions in § 6).

Every claim put to me verifies. Ten of them I re-derived from bytes or from the substrate rather
than reading gamora's prose, and every one landed exact — including the three self-published
defects, which I checked adversarially and found accurately described and soundly repaired.

The headline is the right call. Limbs D and E are genuinely undecoded, there is genuinely no lower
reading available (the "conservative" direction differs per family and per player action), and
`ControlApplicationLimb` having exactly one member makes the absence structural rather than a
comment. Law 3 is not promised here — it is enforced at the AST, and I could not find a way through
it. **The price was published in a zero-code commit before the code existed.** That is D4 working.

The three WARNs are all **census-and-discipline** findings, not mechanism defects. None can reach
the sim as a behavioural fault; none is silently wrong; two of them (WARN-1, WARN-2) are things the
build itself would have caught had its own instruments been pointed one notch wider.

---

## 1 — Re-derived from bytes / substrate, not from the submission

| Claim | Method | Result |
|---|---|---|
| Sibling `E-s09-cp150-b2` sha `a49ef783…d470` | `shasum -a 256` on the artifact | **EXACT** |
| Sibling `E-s09-cp150-b1` sha `0957daaf…c635b` | re-hashed from bytes | **EXACT** |
| Sibling `E-s09-cp150-mech` sha `20b05cb4…b4f5b` | re-hashed from bytes | **EXACT** |
| Parent `E-s09-cp150` 20/20 byte-unchanged | I re-ran `verify_frozen()` myself at review time | **20/20, no mismatch** |
| 10/10 pre-registered predicates hold | read from `artifact["predicates"][*]["holds"]` | **10/10 True** |
| `B2-P2c` 85 added / 0 moved / 0 removed | read from artifact; the computing logic audited in source | **CONSISTENT + SOUND** |
| 131 roster control rows; 300 debuff | `cs.substrate_census()` re-run | **EXACT** |
| Family split Stun 60/27 · Freeze 33/11 · Petrify 26/13 · Confusion 8/4 · Convert 4/2 | same | **EXACT, all five** |
| `L-18` sleep 0 / 4,724 and 0 / 2,400 | `cs.sleep_check()` re-run | **EXACT, both instruments** |
| `F-7` fear 0 monster-side; 0 / 111 player-side | `cs.fear_check()` re-run | **EXACT** (but see WARN-1) |
| Player applies exactly one control | `cs.player_control_applications()` | **EXACT** — Blitz `offensiveKnockdownMin=1.5`, `reachable_in_sim=False` |
| Law 3 `moved == {}`, `constants_introduced == []` | re-run + the AST test's own logic read | **EXACT, machine-enforced** |
| 3/3 `resolve_attack` sites wired | read `run.py` — 3 `resolve_attack` calls, 3 `control_states.observe` calls, one per site | **3/3 CONFIRMED** (main swing · `dying` · toggled aura) |
| Fold `n_landings_seen` == engine `n_hits` | read from artifact, five salts | **259/330/50/19/42, agree 5/5** |
| Smoke 486 pass / 1 pre-existing fail | I ran `pytest tests/ -k "kc2 or baton"` | **486 passed, 1 failed** — `test_AC_10_10`, `secondary_streams.py:136`, a file B-2 never touches |
| `D-B2-1` — true digest vs the reconstructed one | my own re-hash equals the repaired pin | **DISCLOSURE ACCURATE** |
| `D-B2-2` — "eleven loaded skills, worst spans five" | re-derived from `load_control_rows()` | **EXACT** — 11 skills on >1 record, max span 5 |
| `D-B2-2` — basilisk 1.4 s ×4, 1.5 s ×5th | re-derived | **EXACT** (`{1.4, 1.5}` on `basilisk_petrifyingglare.dbr`) |
| `D-B2-3` — three `survival` hits, none a quantity | I re-scanned the artifact myself | **EXACT** — MD-B2-3 ×2 (both citing `…survivalmode_enemies03.dbr`), quarantine sentence ×1 |
| Registered player-kit surface (324 rows) genuinely fear-free | I scanned `pm4g_played_kit.csv` directly | **0 fear tokens, 0 control tokens over 324 rows** |

---

## 2 — The commissioned claims, adjudicated

### Claim 1 — D5 law · **VERIFIED**
Parent 20/20 PRE and POST (I re-ran the gate). Both prior siblings byte-unchanged PRE and POST. The
new sibling's sha is exact. `_b1_sibling()` finds its predecessor **by hashing candidates**, not by
filename — the right shape.

### Claim 2 — the facet-(e) DELIVERY claim · **VERIFIED**
131 rows that `threat.NON_HEALTH_KINDS` has dropped at load since PM-2 now reach the wire. Every
observation carries `applied: False` and `effect_model: "DECLARED-ABSENT — MD-B2-1 / MD-B2-2 /
MD-B2-3"`, enforced by `test_every_observation_states_its_own_non_application` and re-asserted
per-cell in the artifact (`⚑ all_rows_applied_false` True on 5/5). Byte-inertness is proved three
ways, not asserted: fold-absent == the mech P-5 pin; fold-on-minus-key == fold-absent; 85 added
paths **all** under the ledger key, 0 moved, 0 removed. `observe()` performs no RNG draw and no
mutation — I read it; the inertness is structural, and the digest is the proof rather than the
comment.

### Claim 3 — the REFUSAL boundary · **VERIFIED. No invented semantics leaked in.**
`ControlApplicationLimb` has one member. `declared_constants()["constants_introduced"] == []` and
`["⚑ moved"] == {}` — and `test_law_3_witness_list_is_empty_and_the_module_introduces_no_float_constant`
walks the module AST and fails on **any** module-level float assignment. That is machine-checkable
Law 3, checked against the source rather than against the declaration. No magnitude scalar, no
suppression set, no resistance application anywhere in the module. `MISSING_DECODES` is exactly
`{MD-B2-1, MD-B2-2, MD-B2-3}` and `B2-P7` binds the id set to the disposition rows so a refusal
without an ask cannot ship.

**Price derivation spot-checked:** § 0.5's ladder is internally consistent (1,305 opportunities /
700 hits / 108 misses; 700 hits → 562 wire-emitted rows; 2 carrying a control row). Both observed
rows are `Confusion`, 2.0 s, wave 153, on salts 0 and 1 — reproduced exactly by the built fold. See
**INFO-1** on the 562-vs-700 denominator.

### Claim 4 — WARN-1 discharge · **PARTIAL. B2-P1 discharged strictly; B2-P6 does not match its registration.**
`B2-P1`'s registered form fixes salt, family, duration, wave and quantifier; the implementation is a
per-salt expectation **table** graded `all(...)` over five named rows, with no `any()` and no pooled
boolean anywhere in the file. I compared the § 6 registration text to `B2_P1_EXPECTED` line by line:
they match, and the implementation is marginally **stricter** (it asserts the full ordered
observation list, not merely the count). That is the discipline landing exactly as intended.

`B2-P6` does not. See **WARN-1**.

### Claim 5 — the three self-published defects · **ALL THREE ACCURATE, ALL THREE SOUNDLY REPAIRED.**
I reviewed these adversarially and they survive it.

* **`D-B2-1`** (sha reconstructed from a truncated citation). My own re-hash matches the repaired
  pin. Naming a fabricated digest a **Law-3 breach in miniature** rather than a typo is the correct
  classification: it is the shape of evidence with none of the content. The PRE gate caught it
  because it hashes rather than trusts — the guard did its job before a ladder ran.
* **`D-B2-2`** (skill-only join key). Verified independently: 11 loaded skills sit on more than one
  creature record, the worst spans five, and `basilisk_petrifyingglare.dbr` genuinely carries
  **1.4 s on four records and 1.5 s on a fifth**. The claim that this was a latent *magnitude* defect
  and not merely a counting defect is **correct**. ⚑ **The predicate was not amended; the code was.**
  That is precisely the direction WARN-1 was written for, and the observation that B-1's widened
  `any()` shape would have printed `holds: true` over a wrong join key is exactly right.
* **`D-B2-3`** (falsifier narrowed after firing). The three hits are exactly as described — I
  reproduced them. The repair is genuinely narrower than the problem: the **structural** (key-path)
  scan keeps the full token list; only the **value** scan drops `survival`, and only `survival`. The
  other five tokens fire in neither scan. Publishing the judgement, the timing, and the offending
  paths rather than absorbing it into a token-list diff is the correct handling of an
  after-the-fact narrowing. See **INFO-2** for a wording point, not a substance point.

### Claim 6 — the inspection-found hole · **VERIFIED, 3/3.**
`run.py` has exactly three `engine.resolve_attack` call sites (main swing loop, the `dying` slot,
the toggled-aura loop) and exactly three `control_states.observe` calls, one immediately after each,
each gated on `det["hit"]`. The main-swing call sits **above** the `dmg <= 0.0` guard — the wider of
the two observation points, which is the correct choice for a row that rides a hit rather than a
magnitude. The `n_landings_seen` / `n_hits` agreement (5/5 exact) is the right evidence for the
question actually being asked — *was the fold called at every damage path* — and reporting it
**ungraded** because it was not pre-registered is the correct call, not false modesty.
Discipline #11 credited: no gate would have found this.

### Claim 7 — the L-31 check · **CLEAN. No DoT-application surface was built.**
`control_states.py` contains no stacking, no timeline, no bucket, no tick accumulation and no
duration-damage arithmetic; `run.py`'s diff adds three `observe()` calls and comments and nothing
else; `sustain_procs.py`'s diff is one scope string plus one dict key. The nine debuff families —
the DoT-adjacent ones — are dispositioned `NOT_IN_THIS_BUILD` with the scope **declared rather than
silent**. **B-2 built nothing on the pre-D-4c assumption.** One forward-facing note at **INFO-4**.

### Claim 8 — the riders · **ALL FOUR CONFIRMED.**
* **INFO-5** — both `F-B1-1` texts refreshed to L-22's three-part disposition, in
  `simulation/MIGRATION.md § 6` and `export/MIGRATION.md`, each with the superseded instruction
  quoted and struck rather than deleted, and the filed-not-repaired framing preserved. Correct.
* **WARN-3** — scope labels on **both** ledgers: `sustain_procs.SCOPE` (retrofit) and
  `control_states.LEDGER_SCOPE` (born with it), both naming the double-count failure mode
  explicitly, both surfaced in `as_dict()`, with `test_WARN_3_the_B1_ledger_gains_the_same_label`
  enforcing it. Discharged — and the export MIGRATION correctly flags that B-1's own REQUEST 1 row
  tuple still needs the same sentence.
* **B-1f / F-1** — the § 9.5 text ships byte-unchanged (`test_the_disclosure_text_itself_is_byte_unchanged`),
  and the replacement is filed as `export/MIGRATION.md` REQUEST 2. **The ownership call is right.**
  The text is enforced by a cross-seam byte-compare (`devotion.ENVELOPE_DISCLOSURE ==
  baton_v1_schema.DEVOTION_ENVELOPE_DISCLOSURE`); editing the sim copy alone would break it, and
  `export/` is star-lord's seam per AGENTS.md + ADR-004. Filing the request and building the
  **generalised** instrument instead — `⚑ devotion_envelope_disclosure_run_truth`, deriving the
  contradicted claims from `ROW_DISPOSITIONS` at call time — is a better discharge than F-1 asked
  for.
* **WARN-1** — see Claim 4 and WARN-1 below.

### Claim 9 — L-18 sleep NO, and re-derive-at-call-time · **VERIFIED, both halves.**
I re-ran `sleep_check()` and `fear_check()` against the substrate: 0 hits in 4,724 damage rows, 0 in
the 2,400-row `control_effects` union, 0 monster-side fear. Both verdicts are computed inside their
functions from freshly-read rows —
`test_the_verdicts_are_derived_not_hardcoded` walks the AST and asserts each verdict string appears
**only** inside the function that computes it **and** inside a conditional. A verdict with no branch
is a constant, and the test says so. This is `F-1`'s lesson turned into an executable check, and it
is the best instrumentation this run has produced.

---

## 3 — WARN findings

### WARN-1 — `B2-P6`'s implemented instrument does not match its registered form, and the substitution was not disclosed

**What.** § 6 registers `B2-P6`'s second half verbatim as: *"the loaded player kit
(`pm4g_played_kit.csv` **324 rows** + `pm4g_defensive_actives.csv` 21 rows + `pm4p_attack_kit.csv`
10 rows) contains zero fear-family applications."* The shipped instrument
(`control_states.PLAYER_KIT_FILES`) scans `pm4g_movement_skills.csv`, `pm4p_attack_kit.csv`,
`pm4g_consumables.csv`, `pm4g_defensive_actives.csv` — **111 rows**. `pm4g_played_kit.csv`, which is
**324 of the 355 registered rows**, is not scanned; two unregistered files are substituted for it.
The driver's `B2-P6` grade asserts only `n_hits == 0`, with no row-count assertion — so unlike
`B2-P5` (which pins `rows_scanned == 4724`), the narrowing is invisible to the gate. The module
docstring gives a reason (played_kit lives in legolas's notes tree, not in `data/kc2/`), but the
**deviation from the registration is nowhere published** — not in the ADDENDUM, not in MIGRATION.

**Materiality: none to the result.** I scanned `pm4g_played_kit.csv` myself: **324 rows, 0
fear-family tokens, 0 control-family tokens.** The claim holds on the registered surface. This is a
discipline finding, not a result finding.

**Why it matters anyway.** This is the standing WARN-1 shape, in the same build that discharged
WARN-1 impeccably for `B2-P1` and published three of its own defects unprompted. B-2 is the
precedent B-3…B-7 inherit; a silent instrument substitution inside a green gate is exactly the thing
that becomes five copies at B-4. Note also that the substitution was probably *correct* on the
merits — `played_kit` alone would not have found Blitz's knockdown, which lives in
`pm4g_movement_skills.csv`. Which is precisely why it deserved a sentence, not a silence.

**Cite:** prior Gate-2 `WARN-1` (standing for B-2…B-7, L-28) · Discipline #1 · Review Principle 1.

**Action (gamora, next engine cluster):** either add `pm4g_played_kit.csv` to the scanned set with
its out-of-`data/` path declared, or publish the substitution and its basis, and assert
`rows_scanned` in the `B2-P6` grade the way `B2-P5` asserts 4,724.

---

### WARN-2 — `Disruption` is declared an absence-checked family, and the roster carries two MEASURED `Disruption` rows on a loaded `special4` slot

**What.** `control_states.ABSENT_FAMILY_TOKENS` declares five families *"whose ABSENCE is a
load-bearing finding, so that a future roster admitting one goes red instead of quietly enlarging
the model"* — Sleep, Fear, Trap, Immobilize, **Disruption**. I ran the scan for all five. Four
return 0. **`Disruption` returns 2.** Both rows sit on
`nemesis_chthonianvoidborn_01.dbr` (*Grava'Thul, the Voiddrinker*), skill
`nonplayerskillsgdx1/bossskills/nemesis/chthonian02_charge.dbr`, `slot: special4`,
`status: OK`, `rank_grade: MEASURED`, `min: 2.0`, `max: ''`, `actor_kind: roster` — and Grava'Thul
**is in the loaded 169-record roster** with that skill on its `special4` slot.

Nothing checks it. Only `sleep_check()` and `fear_check()` consume the table; Trap, Immobilize and
Disruption have no caller. The rows escape the census because they carry `kind: 'direct'`, not
`kind: 'control'` — so `load_control_rows()` never loads them and `UnknownControlFamilyError` never
fires. The `min: 2.0 / max: blank` shape is the **control-row shape**, not the damage-band shape,
and `MD-B2-1`'s own text cites `defensiveDisruption 30.0` as a measured **player control
resistance** — so the family is control-adjacent by B-2's own evidence.

**Materiality today: latent, not live, and it fails loudly rather than silently.** `Disruption` is
not in `threat.RESIST_PCT` and not in `NON_HEALTH_DAMAGE_TYPES`, so if that row ever resolved,
`mitigate()` would **raise** the GL-12 error by design (*"name it in RESIST_PCT or in
NON_HEALTH_KINDS — do not guess a resistance"*). The GL-12 discipline is working. And Grava'Thul is
not among the control-capable bodies § 0.5 measured spawning, so the ensemble never touches it.

**Why it matters.** B-2's headline artefact is a census, and `ABSENT_FAMILY_TOKENS` is the
census's own guard against quietly enlarging the model. That guard currently publishes a false
absence for one of its five families. It is also directly on facet (e)'s critical path: the player
channels EoR essentially every tick — a disruption family is an interrupt, i.e. exactly the class of
visible consequence `MD-B2-2` exists to name.

**Cite:** charter Law 3 (a declared absence must be a measured absence) · Discipline #8 (schema
validation at boundaries) · Discipline #12 · Review Principle 4.

**Action (gamora, next engine cluster):** give `Trap` / `Immobilize` / `Disruption` a caller — one
`_family_absence_scan` loop over the whole table, published in the artifact beside sleep and fear —
so a non-zero count cannot go unread. Then either add a `RowDisposition` for `control:Disruption`
naming the `kind='direct'` classification as an **open extraction question**, or route it to
legolas as a fourth named decode (`MD-B2-4`: is `Disruption` on `chthonian02_charge` a 2.0 s
interrupt duration mis-tagged `direct`, or a damage type?). **Do not reclassify it in the sim** —
that would be exactly the invention Law 3 forbids. It also belongs in B-4's brief: the row rides
`special4`, and B-4 is the build that opens the special-slot gates.

---

### WARN-3 — the `WARN-3` discharge silently retires B-1's published fold-on digest

**What.** `SustainProcFold.as_dict()` gained `⚑ scope` (correct, and exactly what I asked for). But
that dict is inside the digested surface — B-1's `B1-P2c` distinguishes stripped from unstripped
precisely because the ledger key is digested. So B-1's fold-on payload digest
**`ae031943c7c486f2cfd576d6e9a15af4108bd1ae049ec415b5f75ade3665d755`**, published in
`kc2-mc-b1-player-sustain-ADDENDUM-2026-08-24.md` and pinned in the frozen `E-s09-cp150-b1`
artifact at `predicates/B1-P2c/unstripped_digest`, is **no longer re-derivable from HEAD.**

`simulation/MIGRATION.md § 1` row 3 records the key addition and calls it *"additive,
default-visible, zero behaviour."* Zero *behaviour* is true. Zero *digest* is not, and the
consequence is unrecorded.

**Materiality: nothing depends on it today.** The frozen artifact's bytes are unchanged (I verified),
the mech P-5 pin — the one every build actually binds to — is unaffected and was re-proved by
`B2-P2a`, and no test pins `ae031943…`. The exposure is forward-facing.

**Why it matters.** This run's whole method is *the bind is empirical, not narrated*. B-1r lands on
this surface. If B-1r or B-3 attempts a fold-on bind against the B-1 sibling the way B-2 bound
against the mech sibling, it will HALT on a digest that moved for a documentation reason — and will
spend a lap finding out why.

**Cite:** charter D5 (siblings frozen) · ADR-004 · Discipline #10 (empirical inspection over
assumption) · Review Principle 3.

**Action (gamora, next engine cluster):** one line in `simulation/MIGRATION.md § 1` row 3 recording
that the addition moves B-1's `B1-P2c` unstripped digest, naming `ae031943…` as **superseded, not
reproducible at HEAD**, and stating that fold-on binds against `E-s09-cp150-b1` must re-derive
rather than cite. **Do not re-cut the B-1 sibling** — D5 forbids it and nothing warrants it.

---

## 4 — INFO findings

**INFO-1 — the published price mixes two denominators.** "2 in **562**" is the wire-emitted
denominator; the fold's own denominator is **700** (the `resolve_attack` boundary, deliberately the
wider one). The two are reconciled in exactly one place — math note § 5.4. The artifact, both
MIGRATION entries, `AGENT_STATE.md` and the commit message all carry `562` while the artifact's own
cells sum `n_landings_seen` to 700 with no reconciling sentence. Nothing is wrong; a reader with
only the artifact sees two denominators and no bridge. Carry the § 5.4 sentence into the artifact's
`⚑ price_published` string. *(No action required before B-1r.)*

**INFO-2 — `B2-P8`'s enforced scope is narrower than its registered wording.** Registered: *"no
survival quantity appears in B-2's artifact **at all**."* Enforced: the scan runs **before**
`art["predicates"]["B2-P8"]` is inserted, so the predicate's own block is unscanned. I scanned the
final artifact: `terminal_wave`, `waves_fought`, `at_wave`, `player_died`, `death_wave` and
`survival` each appear as string values **inside the B2-P8 block's own token lists** (3× each). None
is a quantity and the substance of the quarantine is intact — the self-exemption is unavoidable for
a scanner that must name its own tokens. But "at all" overstates what is enforced, and anything
placed in that block escapes the scan. Restate the claim as *"outside this predicate's own
declaration"* and the wording matches the machine.

**INFO-3 — limb B is loaded but never exercised.** `chance_pct` is read and recorded, but `observe()`
records every control row a landing carries regardless of the gate; there is no rolled/not-rolled
field on the observation row. Inert today — both observed rows are blank-gated (no gate) — and
`applied: False` prevents any over-read of *effect*. But the ledger does support an over-read of
*delivery*: a 50 %-gated row would appear as an observation with no indication the gate was never
rolled. Two of eight Confusion rows and one Stun row carry live gates, and **B-4 is the build that
makes them reachable**. Add a `chance_gate: "NOT_ROLLED — delivery-half only"` field, or state it in
`effect_model`, before B-4's census re-run.

**INFO-4 — L-31's decode should be named in the debuff disposition before it is built on.** The
`debuff (9 families, 300 roster rows)` row states *"ALL 300 carry a `dot_duration_s`, so their
delivery is as decoded as the control families'."* True of duration; **not** true of application —
D-4c (L-31) decoded the per-`(damage type, attacker)` 100 ms-bucket timeline with same-source MAX /
distinct-source ADD at `damageMagnitude[min(ordinal, N−1)]`, and that law is a prerequisite for any
of these 300 rows to become a build. The row's triage (two nearer-to-buildable, two provably inert
against I-16's measured board) is genuinely useful forward work and should be preserved — just add
the D-4c prerequisite to it when B-1r lands, so the next builder inherits the whole gate and not
half of it.

**INFO-5 — proposed refinement to the standing WARN-1 discipline.** `B2-P8` shows that exact
registration-to-implementation match is not always achievable: the registered token list collided
with a substrate record name that could not have been foreseen at registration. gamora's handling —
narrow in the smallest possible direction, publish the judgement, its timing and the offending
paths in a **standalone ADDENDUM committed before the repair** — is the correct discharge, and it
should be written into the discipline rather than left to be re-invented at B-4. **Proposed
amendment, standing for B-3…B-7:** *implemented falsifiers must match the registered form exactly
**or** the deviation must be published in a standalone addendum, before the repairing commit,
naming what moved and why.* B-2 met the second branch for `B2-P8` and **neither branch** for
`B2-P6` — which is what makes WARN-1 (§ 3) a finding rather than a preference. Routed to the
decisions-log via my own writing authority (ADR-002) once the conductor rules.

---

## 5 — What I did not verify, stated plainly

I did **not** re-run the B-2 driver end to end. Doing so writes a new artifact into
`simulation/output/`, which exceeds ADR-006's read-only default for a reviewer, and the B-1 Gate-2
precedent re-ran only the frozen gate. The `85 / 0 / 0` figure is therefore read from the artifact
rather than re-measured — but I audited the computing logic in source (`added` / `moved` / `removed`
are derived from key-path dictionaries, and `p2c` requires **every** added path to contain the
ledger key), and it is sound. Everything else in § 1 I measured myself.

---

## 6 — Recommendation on the L-32 hold

**RELEASE the B-1r hold.** The composition risk L-32 named was that B-2 rewired all three
`resolve_attack` sites and B-1r's stacking work lands on that surface. I verified the rewiring
directly: three call sites, three `observe()` calls, correct gating, correct placement relative to
the `dmg <= 0.0` guard, and the fold proved byte-inert by digest with 0 moved and 0 removed paths.
**There is no behavioural surface for B-1r to compose against** — B-2 added observation and nothing
else. Holding B-1r further buys nothing.

Release with two named inputs, neither of which is a hold condition:

1. **WARN-3 is a B-1r input.** B-1r lands on B-1's surface; it must **re-derive** any fold-on digest
   rather than cite `ae031943…`, and it should carry the MIGRATION line that retires it.
2. **INFO-4 is a B-1r input.** The debuff disposition's delivery claim needs D-4c's stacking law
   named as its prerequisite, in the same commit that implements the MAX/ADD timelines.

WARN-1 and WARN-2 are **next-engine-cluster** items and do not gate B-1r; WARN-2 additionally
belongs in B-4's brief, since the row in question rides a `special4` slot.

---

## 7 — Action list

- [ ] **gamora (next engine cluster) — WARN-1:** scan the registered `pm4g_played_kit.csv`, or
      publish the substitution and its basis; assert `rows_scanned` in the `B2-P6` grade.
- [ ] **gamora (next engine cluster) — WARN-2:** give all five `ABSENT_FAMILY_TOKENS` families a
      caller and publish the counts; add a `control:Disruption` disposition naming the
      `kind='direct'` classification as open. **Do not reclassify in the sim.**
- [ ] **gamora (next engine cluster) — WARN-3:** one MIGRATION line retiring `ae031943…` as
      not-reproducible-at-HEAD.
- [ ] **gamora — INFO-1 / INFO-3:** carry the 562-vs-700 bridge into the artifact; add a
      `chance_gate: NOT_ROLLED` field before B-4's census re-run.
- [ ] **gamora (B-1r) — INFO-4:** name D-4c's MAX/ADD law as the debuff row's prerequisite.
- [ ] **B-4 brief (conductor) — WARN-2 + INFO-3:** the `Disruption` row rides `special4`; the live
      chance gates become reachable. Both bite at B-4, and B-4's Gate 2 re-runs the census anyway.
- [ ] **legolas (routing, conductor's call) — WARN-2:** candidate `MD-B2-4` — is `Disruption` on
      `chthonian02_charge` a 2.0 s interrupt mis-tagged `direct`? Shares the `MD-B2-1` call site.
- [ ] **conductor (gandalf) — INFO-5:** rule on the WARN-1 amendment; jack-ryan writes the
      decisions-log entry on ruling (ADR-002).
- [ ] **conductor (gandalf):** **release the L-32 hold on B-1r** per § 6.
- [ ] **star-lord (Wave 4, already filed):** `control_observation` family with `applied` +
      `effect_model` mandatory; the § 9.5 text replacement. No action owed this cycle.
- [ ] **Matt:** nothing. No BLOCK, no ESCALATE, no locked-decision conflict.

---

## References

Engine (`~/Games/reincarnated-engine`):
- `src/reincarnated/simulation/math/kc2-mc-b2-control-states-2026-08-24.md`
- `src/reincarnated/simulation/math/kc2-mc-b2-control-states-ADDENDUM-2026-08-24.md`
- `src/reincarnated/simulation/kc2/control_states.py`
- `src/reincarnated/simulation/kc2/run.py` (three `observe()` sites)
- `src/reincarnated/simulation/kc2/sustain_procs.py` (`SCOPE`)
- `src/reincarnated/simulation/kc2/threat.py` (`RESIST_PCT`, `NON_HEALTH_KINDS`, `NON_HEALTH_DAMAGE_TYPES`)
- `src/reincarnated/simulation/scripts/gamora_kc2_mc_b2_control_2026_08_24.py`
- `tests/test_kc2_mc_b2_control_states.py`
- `src/reincarnated/simulation/MIGRATION.md` · `src/reincarnated/export/MIGRATION.md`
- `src/reincarnated/simulation/AGENT_STATE.md`
- `src/reincarnated/simulation/output/kc2-checkpoint-E-s09-cp150-b2-20260824_141850.json`

Collaboration (`~/Games/reincarnated-collaboration`):
- `agentic_orchestration/gandalf/notes/2026-08-24-kc2-model-completion-run-charter.md` (L-17, L-18, L-22, L-23, L-26, L-28, L-31, L-32)
- `agentic_orchestration/qa/findings/2026-08-24-gamora-kc2-mc-b1-gate2.md`
- `agentic_orchestration/legolas/notes/2026-08-13-kc2-pm4-lap-g-player-kit/pm4g_played_kit.csv` (WARN-1, scanned)
- `agentic_orchestration/legolas/notes/2026-08-24-kc2-mc-lap-d4c-dot-stacking-decode/README.md` (L-31)
