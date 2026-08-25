# W4 · THE TWIN-TEST SPEC — how drax proves the Godot build is a faithful twin

> ▶ **ROLE: SPEC-AUTHOR** — Wave-4 piece, charter tag **F-5**.
>
> **STATUS:** SPEC — consumable by a later drax session. **Spec, not code.** No production code in this seat; the build is a separate session (charter § 7 seat-map: drax is **recipient-only** this run, and this file lives in the run's notes, never in `reincarnated-godot/`).
> **Run:** KC2 MODEL-COMPLETION RUN · **Wave:** 4 (export + handoff) · **Date:** 2026-08-25
> **Author:** gandalf (named sub-agent, `SPEC-AUTHOR`) · **Conductor:** gandalf `RUN-CONDUCTOR`
> **Companion:** `2026-08-25-kc2-mc-w4-godot-runtime-spec.md` (charter tag SKIRT) — *what* the runtime implements. This file is *how it is proven.* Read that one first; this one grades it.
> **Authority rows:** charter `2026-08-24-kc2-model-completion-run-charter.md` § 1.4 + § 3 Wave 4 · ledger **L-83** (Wave-4 gate = the policy-fix seal) · **L-85** (measured release policy + the two DO-NOTs) · **L-88** (the fix delivered; the residual does not move; R-L88-5 figure hygiene) · **L-89** (R-L89-2: the uniform 0.15 is a named approximation) · **L-90** (R-L90-2: binding exclusivity is the Layer-1 rule — **superseded by D-CP2-2, § 5**; R-L90-6 fires this wave) · **L-68** (R-L68-2: the metre-scale pin fires at Wave-4 assembly) · schema `2026-08-24-s1-baton-v2-schema-draft.md` §§ 3–5.
> **Standing law binding on every line:** **Law 3** (no fitted constants, no invented rules) · **D5** (`E-s09-cp150` immutable; siblings only) · **GL-6** (verify digest before load) · **GL-12** (absence is DECLARED, not filled) · **D4** (prereg before results) · **#72** (mechanical enumeration) · **wave-160 is a GRADED ROW, never a gate** (Matt-ruled).
> **Pattern law binding on the DESIGN of this instrument:** `operating-procedures/desirable-run-pattern.md` § 6 **obs-1** (coverage-gates before accuracy-gates) · **obs-2** (owner-eye as a pre-registered mid-run gate) · **obs-3** (rubric law).
>
> ⚑ **RULING-CURRENT AS OF 2026-08-25 — read the body, not a stack of notes over it.** This text is **integrated** to owner-eye checkpoint-#2 rulings **D-CP2-1 · D-CP2-2 · D-CP2-3** (KC2-MC charter **L-94**), by the **KC2 LIFT RUN, Wave-2** (`2026-08-25-kc2-lift-run-charter.md`). The post-seal supersession note at the foot is **retained as lineage and marked INTEGRATED**. Superseded readings are **named in place**, never deleted (forward supersession). **K-7 held:** every sentence describing the **sealed reference** is unchanged — it was generated **wall-less**, under a **uniform 0.15 roll**, and this spec still says exactly that. **§ 0's rubric declaration is untouched and remains the first thing a reader meets.**
>
> ⚑ **SECOND INTEGRATION PASS, 2026-08-25 (LIFT ledger R-L5-4) — rulings `R-L91-4..8` + `R-L92-2` folded.** The load-bearing change is to the **§ 3 drive contract** and **§ 9 OQ-3**: this test no longer consumes an RNG **tape**. **R-L91-4 rules BANDS-NOT-TAPE** (*ship the rules, never the ladder* — a tape is a ladder) and **R-L92-2** reclassifies the `ABS-RNG-TAPE` honest-fail **CONVERGENT-NOT-DEFECT**: **`reference/rng_tape.jsonl` does not exist, no recorder sibling fires to make it, and the tape was ruled unwanted.** Drive substrate: **the draw-site registry (a G-0 RULES-facet key space) + T-1/T-2 band grading.** Also folded: **R-L91-5** rules **OQ-4** (A) — **OE-1 gates on the `R-L68-2` scale pin**, and the § 6 gate table now says so; **R-L91-6** rules **OQ-5** (shared row schema, disjoint row sets) and **OQ-6** (split harness), and corrects the post-seal note's claim that OQ-6 went forward unruled. **§ 0's rubric declaration remains untouched by this pass as well.**

---

## 0 · Headline — and the one sentence that keeps this instrument honest

The twin-test proves **the Godot runtime derives the same fight the Python sim derives, from the same model.** It runs in two halves and the order is not negotiable: **first a COVERAGE gate** on the watched surface, **then ACCURACY gates** on the covered fraction.

> ⚠ **The rubric declaration, stated before any gate is designed (obs-3, and applied here against my own instrument):** this test grades **runtime ≡ sim**. It does **not** grade **sim ≡ Matt**. The Layer-2 reference is a *sim* run under a pinned seed; its "recorded player path" is the **pilot model's** path, not the path Matt's hands made on 2026-08-05. Matt's fidelity question is graded elsewhere — by KC2-PM5 against the referent — and **L-88 already reported the answer there is open** (the corrected channel policy moved terminal wave 153.0 → 153.2 against a referent 160; playing like Matt's release pattern was never the survival driver). A green twin-test therefore certifies *implementation fidelity*, and a session that reads it as *"the Godot build plays like Matt"* has swapped the owner's question for a narrower proxy. **That is the KIT-FIDELITY failure, and it is named here so it cannot be discovered later.**

What this test IS the instrument for, in the charter's own terms: it is what **transfers the proof obligation** for "a Godot team could build the playable fight from this artifact without guessing a rule" to the consuming session (charter § 6, self-diff item 1). The run cannot prove Godot playability. This spec is how the next session can.

---

## 1 · GATE ORDER — the law, and why it is first in this document

**G-0 COVERAGE runs to closure before any accuracy tier is scored. A tier scored on an unclosed coverage census is VOID, not preliminary.**

obs-1 exists because KIT-FIDELITY gauged byte-exactness on the joined fraction and never gated what fraction of the watched surface was joined at all: a real byte-chain lock certifying 40/41 entities, unjoined player HP, a compiler-default cost, and a flagship kit that never cast its signature skill. **The shape of this run is exactly the shape that failed** — a fidelity/twin claim against a rich model — so the ordering is imported as law rather than as guidance.

Operational consequence for drax: **do not report a T-1 or T-2 number before the G-0 census closes.** A partial census plus a good trajectory band is the sliver-certification pattern wearing a green hat.

---

## 2 · G-0 — THE COVERAGE GATE

### 2.1 The watched surface (five facets, each with a key space the PACK defines)

| facet | key space (mechanically enumerable from the pack) | source |
|---|---|---|
| **ENTITIES** | every `record_path` in `model/monsters.json` + `model/summons.json` + the player | S-1 § 2.2 / § 2.3d |
| **SKILLS** | every `skill_id` on the bar, every devotion proc, every monster skill + special slot | S-1 § 2.3 / § 2.2 |
| **STATS** | every field of every stat block (offense · defense · life · ai) | S-1 § 2.2 |
| **BEHAVIORS** | every `state_id` and `transition_id` in `model/ai_states.json`; the player channel policy + the **per-skill `interrupts_channel` flag** (D-CP2-2) — one census row **per skill**, so an unassigned flag is `UNCOVERED` rather than silently false | S-1 § 2.1; runtime spec § 3–4 |
| **RULES** | every `rule_id` in `model/math_rules.json`; every `draw_site_id` in `model/rng_contract.json` | S-1 § 2.4 / § 2.7 |

### 2.2 The disposition enum — three values, no fourth

For every row of every facet the runtime declares exactly one:

- **`IMPLEMENTED`** — the runtime executes it, and names the T-0 vector rows or the T-1/T-2 rows that exercise it.
- **`BINNED`** — deliberately not implemented, **with a reason and a reachability claim** (*"unreachable in the reference window"* is a claim the harness can falsify from the Layer-2 event stream; *"not needed"* is not a reason).
- **`UNCOVERED`** — neither. **Any `UNCOVERED` row that is reachable in play is RED.**

This is **FG-13 generalised from an event census to a RULE census** (S-1 § 4). v1's loader already derives its need-list from the artifact's own `event_type` column and goes RED on an uncovered need; v2 widens the same instrument to rules, states, skills, stats and entities. The generalisation is the point: *"we implemented your model"* becomes a countable claim.

### 2.3 Two clauses the census inherits from #72, and they are the ones that get skipped

1. **The enumeration is MECHANICAL.** The key space is read out of the pack by script and pasted; a hand-written list of "the skills we did" is a *labelled expectation*, checked **against** the mechanical sweep, never substituted for it.
2. **Mechanical does not license narrow.** The census declares what its instrument excludes. A row the instrument cannot classify is emitted **UNRESOLVED** — never folded into a green count.

### 2.4 Closure predicate

> **G-0 CLOSES iff:** every row of every facet carries a disposition · zero `UNCOVERED`-and-reachable · zero `UNRESOLVED` · every `BINNED` reason survives a reachability check against the Layer-2 event stream · every `absent_ref` the runtime touched has a **runtime-choice ledger entry** (S-1 § 4, GL-12).

The runtime-choice ledger is the countable form of *"the Godot team guessed here."* It is a required output of a green G-0, not an appendix.

---

## 3 · ACCURACY TIERS — T-0 … T-3

Run only after G-0 closes. Each row is graded independently; a tier is not a pass/fail unit.

| Tier | asserts | instrument | why it exists |
|---|---|---|---|
| **T-0 · unit** | every `math_rules.test_vectors` row reproduces to declared precision | vector table, exact | a mitigation formula misread is caught by a 40-row table in milliseconds instead of by a 300-second fight divergence with fifteen candidate causes |
| **T-1 · trajectory** | driven along `reference/tracks.json`, the runtime's player HP / energy / **channel** tracks stay in band | per-tick band + max-excursion | the channel track is the row this whole wave was fought for |
| **T-2 · fight state** | board occupancy per tick, cumulative damage dealt/taken, wave-clear ticks | per-wave band | catches AI/state divergence that the player tracks average away |
| **T-3 · outcome** | waves cleared, run duration, end reason, **terminal wave** | **report-only** (§ 4) | reported prominently, asserted never |

**T-0 is normative and `expr` is documentary** (S-1 § 2.4). The runtime is not required to implement an expression evaluator; it is required to implement the rule in GDScript and reproduce every vector. Vectors are emitter-generated from the sim, so they cannot drift from the sim's actual behaviour.

**Drive contract for T-1/T-2** (S-1 § 3, one sentence — ⚑ **amended at the RNG clause ONLY**, R-L91-4 + R-L92-2): *load `model/` only into the runtime; drive the player actor along the recorded path (positions authoritative, GL-7 interpolation); **draw from the runtime's own RNG at every `draw_site_id` declared in `model/rng_contract.json`, in the declared consumption order**; run to the recorded end; emit the same track + event shapes; diff `acceptance.json` row by row **against the pre-registered bands**.*

⚑ **SUPERSEDED CLAUSE, named in place (second integration pass, 2026-08-25).** The contract previously read *"consume `reference/rng_tape.jsonl` at the declared draw sites."* **Overruled twice over.** **R-L91-4 — BANDS-NOT-TAPE:** *ship the rules, never the ladder*, and a tape **is** a ladder; it certifies replay, not derivation. **R-L92-2:** the `ABS-RNG-TAPE` honest-fail is reclassified **CONVERGENT-NOT-DEFECT** — no sealed checkpoint emits a draw log, **K-7** forbids re-running one to make it, and **no gamora recorder sibling fires**; the absence row stays as record. **`reference/rng_tape.jsonl` does not exist and is not wanted.** What replaces it is already in this document and needs no new machinery: the **draw-site registry** is a G-0 **RULES**-facet key space (§ 2.1) — so *where and in what order draws happen* is a **censused, three-valued claim**, which is the part a twin-test can actually own — and **T-1/T-2 grade against pre-registered bands**, which is what those tiers' instruments already say on their face in the § 3 table (*per-tick band + max-excursion*; *per-wave band*). See § 9 OQ-3 for the cost accepted with this ruling.

⚑ **WHICH REFERENCE THE CONTRACT DRIVES AGAINST — ruled by D-CP2-1.** Both sides of this diff now carry **authored walls and DoT-ticking spawn pools**, so the reference side is the **walls+pools gamora sibling** (LIFT RUN item **W1**), not the sealed wall-less cells. **K-7 is the reason, not an exception to it:** the sealed reference stays the historical referent and **is never regraded** — the sibling is a *new* object built to its own prereg. **The comparison stays apples-to-apples because both sides change together**, which is exactly what a structural asymmetry would have destroyed. The behavioral asymmetry — *the pilot's policy stays out of the pools, as the referent did* — is a **graded behaviour**, not a difference in the world the two sides inhabit.

---

## 4 · REPORT-ONLY — a structural guarantee, not a procedural promise

A row with `report_only: true` **may not carry a tolerance**, the validator rejects a pack where it does, and **the harness has no code path that turns a report-only row into a FAIL** (S-1 § 3).

Rows that are report-only **by construction**:

1. **`ACC-T3-TERMINAL-WAVE`** — Matt-ruled: wave-160 is a graded row, never a gate. This is how the ruling survives a session that does not remember it.
2. **Any row whose reference value depends on a Layer-1 rule marked `DECLARED_ABSENT`.** Grading a runtime against behaviour the model refused to specify grades the consumer's guess, not the consumer's fidelity.
3. **Any row downstream of a NAMED APPROXIMATION** — the enumerated set is in the runtime spec § 9; the cast-interrupt row is § 5 below and is the important one.

> **The twin-test does NOT gate on closing the 153→160 residual.** L-88 is explicit and the candidates are *named-not-adjudicated* (Type-B phase unmeasured, target selection, defensive weave usage). A twin-test that gated on survival would be grading an open research question as an implementation defect — and would fail a correct implementation for it.

---

## 5 · THE CAST-INTERRUPT DIVERGENCE — pre-registered, because it is designed in

This is the one place where **the model and the reference disagree by construction**, and it must be registered **before** the harness runs (D4), not explained after a red row.

**The state of the evidence:**

- **Layer 1 (the rule the runtime implements — D-CP2-2, superseding R-L90-2's reading):** *casting a skill flagged **`interrupts_channel`** while the channel is **ACTIVE** releases it.* **A per-skill property, not a rule over mouse buttons and not a per-cast die roll.** The mechanism transfers to Godot **carrying no Grim Dawn skill with it** — and now carrying no *keybind* with it either.
  > ⚑ **Superseded reading, named in place:** this bullet previously read *"casting the opposite-mouse-bound skill releases the channel — binding exclusivity, not skill identity."* **Overruled.** Mouse-exclusivity demotes to (i) the **referent's explanation** and (ii) the **default-assignment heuristic** (a skill bound opposite the channel's button defaults flag-true). Runtime spec § 3 carries the full derivation.
- **Layer 2 (measured reference values, and the flag assignment they warrant):** per-skill interrupt rate — **Blitz (left mouse) 0.385 → flag `true`** · **Vire's Might (key 2) 0.136 → flag `true`** · **War Cry (key 3) 0.000 → flag `false`**, and War Cry's casts sit in silences *shorter* than the duration-weighted null (p = 4.9 × 10⁻⁷): the channel **tightens** around them. **The decisive datum is attribution, not rate: 8/8 Type-B releases attributed with zero orphans — 5 to Blitz, 3 to Vire's Might** (L-89). A **keyboard-bound** skill released the channel three times, which is what a pure-binding rule cannot say.
- **The sealed sim (which generated the reference tracks):** a **uniform 0.15 per-cast roll** — sealed before 2c landed, held per R-L89-2 rather than re-opened (K-7). **It is a named approximation: arithmetically true, mechanically false** — a cancellation of an interrupting family against a never-interrupting one. *(Wording aligned with runtime spec § 3 at integration: under D-CP2-2's conditional the flagged family is not **always**-interrupting — it interrupts when the channel is active. The seal, and everything else in this bullet, is unchanged.)* 8/54 = 0.148 pooled; pooled, the casts are statistically indistinguishable from randomly-timed moments (MW p = 0.286) *because two strong opposite effects meet at the average.*

**Pre-registered prediction (this is the falsifiable form, and it is the deliverable of this section):**

| quantity | prediction | grading |
|---|---|---|
| aggregate release **count** and **duty** over the run | **agrees** with the reference within the T-1 band (both mechanisms produce ≈0.15 aggregate by construction) | **asserted** |
| **per-cast attribution** — which casts a release follows | **DIVERGES**, and the direction is pre-named: the runtime releases **on flagged casts taken while the channel is active, and never on unflagged casts** (War Cry: 0 for 0); the reference releases on ~15 % of casts **irrespective of which skill was cast** | **report-only, with the divergence direction pre-registered** |
| **run-level fight state** downstream of it (T-2 occupancy, damage) | agrees within band; the mechanism difference is texture, not aggregate | asserted, **with this row named as its first suspect** if it reds |

**Fork disposition — ✅ RULED (A), R-L91-2; kept here because the reasoning still binds the build.** Three ways to handle a model/reference disagreement of this kind: **(A)** runtime implements the rule; attribution rows go report-only with the divergence pre-registered *(the design above)*; **(B)** runtime carries a `twin_compat` mode implementing the uniform roll for the test and the rule for free play; **(C)** re-cut the reference from a sim implementing the flag. **(A) accepted.** (B) builds a second mechanism the team knows to be mechanically false and gives it the only code path that is ever *tested* — compat paths become the real path. (C) re-opens a sealed seat for a refinement that does not move its gates: K-7 erosion, already refused at R-L89-2.

⚑ **What D-CP2-1/-2 change about this pre-registration — stated as a CONDITIONAL, because the object it depends on does not exist yet.** The W1/W2 sibling implements **walls, pools, and the `interrupts_channel` flag**. If and when the twin-test's reference side is that sibling (per § 3, D-CP2-1), then *both* sides carry the flag and **the per-cast attribution divergence pre-registered above collapses to zero by construction** — the divergence is an artifact of grading a flag-implementing runtime against a **0.15-roll** reference, and it dies with that pairing, not with the mechanism. ⚠ **This pre-registration is NOT amended on that expectation.** D4 forbids editing a prereg toward an anticipated result, and the sibling **is not cut**. The table above stands **exactly as written**, and the reconciliation — *which reference side each row is graded against, and which rows survive it* — belongs to the **baton-v3 cut (LIFT RUN Wave-3)**, not to this spec. A session that finds the divergence row inapplicable because both sides carry the flag has found **a prereg discharged by supersession**, which is a disposition, not a defect.

**And the sharper instrument (A) buys, which (B) and (C) do not:** a **T-0 footage-vector table** for the **interrupt-flag rule**, graded against the *measured footage* values rather than against the sim — *does an **unflagged** cast ever release the channel (expect: never — War Cry, 19/19 clean)? does a **flagged** cast release it (expect: at rate, and for 0.60 s median, 0.53–0.67 s range, n = 8)?* This moves the proof obligation for the mechanism to the instrument that actually measured it, **and it survives every reference re-pairing above**, because footage is not a sibling.

**Two named residuals carried into every quote of this section:**

1. **Slot 7 (L-90).** **Rune of Rush**, a third charge skill, is **footage-blind** — its casts are outside the 53 — so **its flag is `UNDETERMINED`, not `false`.** A per-skill reading and a charge-class reading cannot be fully separated on this evidence. The runtime ships a registered **default**; the residual ships with it.
2. **The conditional's rate residual (runtime spec § 3).** D-CP2-2's conditional predicts a flagged skill's rate ≈ **P(channel active at cast)**; fight-wide uptime is **0.838** and Blitz measures **0.385**. ⚠ **A red T-1 channel row must not be closed by fitting a per-cast probability** — that re-creates the 0.15 cancellation. If this row reds, **it is its own first suspect**, and the named cheap test (per-slot *P(channel active | cast)*, a re-query of already-measured footage) is the response.

---

## 6 · OWNER-EYE CHECKPOINTS — pre-registered mid-build gates (obs-2), including F-5

obs-2 was paid for: both KIT-FIDELITY catches were Matt's, mid-stream, unprompted, while the run's own gates said green twice. **The owner's eye is an instrument of record, not a briefing recipient.** For a build whose output is a watched surface, it is scheduled at named points *before* downstream gates build on unviewed state.

| gate | when | object | what it rules |
|---|---|---|---|
| **OE-1 · CAMERA (F-5)** | **first frame that shows the player in the arena** — before any accuracy work — ⚑ **and after the `R-L68-2` metre-scale pin lands** (**R-L91-5**, § 9 OQ-4: *a camera ratified before a 1.7× scale move ratifies a different scene*) | one still + one short clip under the starting-recommendation camera | the register (see § 6.1). **Blocks OE-2.** |
| **OE-2 · THE FIGHT MOVES** | after G-0 closes, before T-1/T-2 are reported | a clip of ~30 s of live combat at a mid-range wave | does it read as the character fighting — channel held through movement, releases at wave flips, monsters arriving in a drip |
| **OE-3 · THE REPORT CARD** | at twin-test seal | the coverage census + tier table + runtime-choice ledger | the whole instrument, with the § 0 rubric declaration on its face |

### 6.1 · F-5 — CAMERA RE-RATIFICATION UNDER TRANSLATION (the requirement, stated plainly)

**No prior camera ratification transfers to this build.** Carry the ratified camera as the **starting recommendation**; render; route to Matt; **do not lock**.

What exists, and exactly what it covers:

- **The provisional-canon arena camera** (R-CPB-18, gate 1 + gate 2 both passed on Matt's eye): `player_lock` **yaw 47.0 / pitch 52.9535411256029 / fov_v 31.7861018306101 / k = 0.665**; ruling object `arena-pl-k0665-n160-1920x1080.png`, sha `4c88de0d92cdcaffd995233fc69990f9ed1d7e9a30f9d2ca79c2bb943af2d71f`. It was ratified on the **SB-1 arena presentation subject** — a cut-pattern/parade scene — **not on a playable KC2 runtime with a live player and live monsters.**
- **The project ARPG camera** (game tracker **A′1/B1**, `canonical/current-to-end-state/current-to-end-state-game.md:357,370`) is **BANKED, not ratified** — its ratifying scene was cancelled; B1 is OPEN and MVP-critical, and ratifies at the demo's first authored floor.
- **Matt's own gate discipline governs the value** (R-CPB-17b, verbatim): *"I have never eyeballed this fixed boom ≈ 72.9 m, so we won't want to check it off as canon until I can eyeball…"* — **he ratifies a LOOK, not a number**, and a transcription gets eyeball-verified. A camera transcribed into a new scene is a new transcription.
- **R-CPB-16's own scope**: canon *"for the time being, especially while testing GD scenes"*, changeable later, Matt's word.

**And the requirement that is not about ratification but about the test's validity — the reason F-5 belongs in the twin-test spec rather than only in the runtime spec:**

> **A camera that cannot resolve the behaviour being ratified turns an owner-eye gate into sliver-certification** (obs-1, at the presentation layer). WW-8 measured exactly this: at k = 0.665 an in-place motion contrast that read clearly as formation texture at the 72.857 m boom **does not announce itself** — *formation grammar is a wide-register language.* The KC2 behaviours Matt would be ruling on at OE-2 are **channel-through-movement, release-at-wave-flip, the spawn drip, and the monster state changes**. If the chosen register cannot show them, the gate must be run at a register that can, **and that second frame is a diagnostic, not a canon candidate** (the A2g demotion precedent, R-CPB-17(c)).

**F-5 closes when:** Matt's eye is on a rendered frame *of this build*, and his word is recorded against it with the frame identified by path + sha (the NOTE-96 identification discipline: never assume the artifact). Until then, the camera row of this build is **PROVISIONAL**, and the twin-test's report card says so on its face.

---

## 7 · INSTRUMENT HYGIENE — three rules that bind every number this test emits

1. **Ship RATIOS, not absolutes, for movement.** `D-MPOL2-2`: three instruments give the referent's `frac_moving` as **0.883 / 0.705 / 0.6265** — a **1.41×** spread. On this evidence *"movement excess"* is an **instrument disagreement about the referent**, routed not adjudicated. Every movement-derived acceptance row is expressed as a ratio so the instrument cancels; an absolute movement figure in a green report is a defect in the report.
2. **G5's uptime is 0.0960, not 1.9 %** (`R-L88-5`, a 5.2× correction). Any forward quote uses 0.0960. **The derived "~40×" figure moves with it and must be RE-DERIVED, never re-quoted.**
3. **A published aggregate can be arithmetically true and mechanically false** (`R-L89-4`). Where an aggregate is reported, the report names whether it is a *rate* or a *cancellation*. The 0.15 is the founding instance and it is labelled everywhere it appears.

Plus the blind-residual carry: galadriel's **6.2 % blind residual** on the release population is CARRIED, not closed; a twin-test row whose reference value derives from that population states it.

---

## 8 · ACCEPTANCE CRITERIA — when THIS SPEC is satisfied

The twin-test spec is discharged when the consuming drax session produces, in this order:

- [ ] **A-1** — a **mechanical coverage census** over all five facets with three-valued dispositions, plus the runtime-choice ledger; **G-0 closure predicate green** (§ 2.4). No accuracy figure reported before this line.
- [ ] **A-2** — **T-0 green**: every `test_vectors` row reproduced to declared precision, including the § 5 footage-vector table for the **`interrupts_channel` rule** (flagged vs unflagged cast, graded against the footage).
- [ ] **A-3** — **T-1 / T-2 graded row-by-row** against `acceptance.json`, each red row carrying a named first suspect rather than a re-tuned band. **No band widened post-hoc, by anyone** (the L-88 precedent: a failed band was carried FAILED-AS-REGISTERED rather than widened, by seat *and* by conductor).
- [ ] **A-4** — **T-3 reported, asserted nowhere**; terminal wave prominent and un-gated.
- [ ] **A-5** — **§ 5 divergence report**: aggregate agreement asserted, per-cast attribution divergence reported against its pre-registration — **or the pre-registration declared DISCHARGED BY SUPERSESSION**, naming the reference side actually graded against (§ 3, D-CP2-1). Silence on the row is not a disposition.
- [ ] **A-6** — **OE-1 (F-5) ruled by Matt on an identified frame**, OE-2 and OE-3 held in order.
- [ ] **A-7** — the report card carries the **§ 0 rubric declaration verbatim on its face**, so no reader can mistake *runtime ≡ sim* for *build ≡ Matt*.

**And one anti-criterion, stated as a criterion:** the twin-test is **not** satisfied by a green tier table over an unclosed census, and it is **not** failed by a terminal wave below 160.

---

## 9 · OPEN QUESTIONS BACK TO THE CONDUCTOR

*Decision-shaped. Not resolved here.*

✅ **OQ-1 — the cast-interrupt divergence handling. RULED, twice over.** *Handling:* **(A)** accepted (R-L91-2) — rule + report-only attribution + footage-vector table. *Mechanism:* **D-CP2-2** — Matt saw the fork and ruled it (*"should we not bind the interrupts to the two skills directly?"* → **yes, as a per-skill flag**), which is the half this OQ said should reach him. And the visible consequence it named came out as the flag predicted: **the kit has skills that are safe to weave and skills that are not, and the player learns which** — rather than every skill being occasionally clumsy. Nothing open.

⚠ **OQ-2 — which sibling is Layer 2 cut from. RE-FRAMED by D-CP2-1; the pinning rule is unchanged and still correct.** S-1 pinned `E-s09-cp150-mech` (`20b05cb4…`), and B-1…B-5, B-2app, B-3app, B-4app, PM5 and **M-POL-2** (`ad61ad2a…`) landed after it. **The requirement is no longer "the final post-M-POL-2 sibling" — it is the walls+pools+flag sibling (LIFT RUN W1/W2)**, because D-CP2-1 requires both sides of the diff to carry walls and ticking pools. **This spec still deliberately hard-codes no sha**: the **baton manifest governs** (R-L91-3); star-lord's cut sets it; the shas named in this paragraph are **historical pins quoted as history, never as the pointer this spec resolves against.** D5 forbids touching the parent, and K-7 forbids regrading the seal — **the sibling is a new object, not a re-cut.**

✅ **OQ-3 — RNG tape vs statistical bands. RESOLVED BY RULING: `BANDS`** (**R-L91-4**, reinforced by **R-L92-2**). *As asked (S-1 OQ-3, costed by this document):* the tape makes T-1/T-2 exactly reproducible; without it every tier degrades to a distributional comparison and the § 5 attribution test loses its sharpness; tape size is unknown until the completed model's draw count is known. ⚑ **The spec's lean — *"tape, with per-wave segmentation if size bites"* — is OVERRULED, and this is no longer an open question.**

- **R-L91-4 (the principle):** *ship the rules, never the ladder* is standing run law and **a tape is a ladder.** A runtime that replays a recorded draw sequence has demonstrated that it can read a file; the claim the twin-test exists to make is that it **derives** the same fight from the same rules.
- **R-L92-2 (the artifact):** the question is moot at the object as well as at the principle — **no sealed checkpoint emits a draw log**, **K-7** forbids re-running one to make it, so `ABS-RNG-TAPE` was filed as an honest fail and then reclassified **CONVERGENT-NOT-DEFECT**: *the tape the cut cannot ship is a tape the twin-test no longer wants.* **No gamora recorder sibling fires**; the absence row stays as record.
- **The costed objection, answered rather than waved.** The § 5 attribution test does **not** rest on the tape. Its sharpness comes from the **T-0 footage-vector table** for the `interrupts_channel` rule (§ 5, final paragraph; acceptance row **A-2**) — graded against the **measured footage**, which is why that paragraph already claims it *"survives every reference re-pairing."* This is one more re-pairing and it survives this one too.
- **What is genuinely paid, and it is paid knowingly:** T-1/T-2 are distributional comparisons. That was already their declared instrument in the § 3 table (*per-tick band + max-excursion*; *per-wave band*) — the tape would have bought an exactness above that table which the run was never in a position to sell.

**Drive substrate of record: the draw-site registry (`model/rng_contract.json`, a G-0 RULES-facet key space) + T-1 band grading.** Nothing open.

✅ **OQ-4 — does the metre-scale pin land before or after the first owner-eye gate? RULED (A): OE-1 GATES ON THE PIN** (**R-L91-5**, *accepted as ruled — the lean was right*). *As asked:* `R-L68-2` fires the scale pin **at Wave-4 baton assembly** (register the Class-1 minimap footprint against the final pursuit model's occupancy hull); until it lands, `u = 0.198 m/px` carries a **1.7×** band `[0.094, 0.366]`. **A camera ratified against an arena whose metre scale later moves by up to 1.7× is a ratification of a different scene.** Option (B) — fire OE-1 on native-px geometry and re-run it if the pin moves scale past a threshold — is **refused**: it spends Matt's eye twice on the same question. **The ruling's own sentence, carried because it is the reason and not merely the verdict: *ordering is conduction.*** ⚑ **Operational consequence, binding on the § 6 gate table:** OE-1's *when* is not only *"first frame that shows the player in the arena"* — it is **that frame, after the R-L68-2 scale pin has landed**. A build that renders the first arena frame before the pin has a frame, not a gate.

✅ **OQ-5 — does PM5's report card share a row schema with `acceptance.json`? RULED: shared row SCHEMA, disjoint row SETS** (**R-L91-6**, lean accepted). (S-1 OQ-8. The reason it is load-bearing: § 0's rubric declaration is *why* the two instruments must never be conflated — shared **schema** is the cheapest way to make wave-160's `report_only` flag honoured by both, and disjoint **sets** are what keep *runtime ≡ sim* from being read as *sim ≡ Matt*.) ⚑ **Ruled with a named settling point, not resolved to the field list:** R-L91-6 settles the **detail** at **Wave-4 seal review against star-lord's cut** — which landed (R-L92-4, cross-check PASSES). A consuming session that finds a row-schema mismatch against the cut resolves it *to the cut*, and reports it; it does not re-open the shape.

✅ **OQ-6 — who owns the harness? RULED (C): SPLIT** (**R-L91-6**, lean accepted). The twin-test needs a runner that loads both layers and grades rows. (A) drax builds it inside the Godot seam · (B) star-lord builds it engine-side against emitted runtime output · **(C) both halves, meeting at a declared output format — ACCEPTED.** The runtime emits track + event shapes; the grading lives with the emitter that generated the reference, **so the two sides of the diff are never written by the same hand.** The ruling names the safety it is buying: this is the **proposer/judge separation**, the same shape as § 5's refusal of a `twin_compat` path — an instrument whose two halves share an author cannot catch the author's shared assumption. ⚑ **Correction of record:** the post-seal note at the foot of this file states OQ-6's lean was *"carried into the LIFT RUN charter § 4 unruled."* **That is wrong** — R-L91-6 ruled it at Wave-4, before the note was filed. Annotation appended at the note; see the foot.

---

## ⚑ POST-SEAL SUPERSESSION NOTE (run close, charter L-95; rulings D-CP2-1..2, 2026-08-25) — **INTEGRATED 2026-08-25**

> **STATUS: INTEGRATED INTO THE BODY 2026-08-25** (KC2 LIFT RUN, Wave-2, gandalf `SPEC-AUTHOR`). **Retained as lineage — never deleted.** When first filed, this note was *appended forward* and governed over an unrewritten body; the body has since been rewritten to the rulings, so the note's job is now **historical**: it records what was overruled, when, and by whose word. Read the body for how the twin is graded; read this to see how it got there. Should the body and this note ever appear to disagree, **that is a defect in the body** — the rulings govern, in either text.

Appended FORWARD — nothing above is rewritten; where this note conflicts with the body, this note governs for all future use. *(Original clause, preserved as written; superseded in force by the STATUS block above now that integration has landed.)*

- **D-CP2-1 (Matt verbatim: "live walls for both, dot ticks in spawn pools for both (have the sim stay out of there)")** supersedes the walls facet: the twin-test's two sides BOTH carry authored walls + spawn-pool DoT ticks; the surviving asymmetry is BEHAVIORAL only (the pilot's policy avoids pools, as the referent did). Comparisons stay apples-to-apples because both sides change together.
- **Referent boundary (K-7):** the sealed wall-less reference stays the historical referent and is never regraded. The twin-test grades runtime ≡ **the walls+pools gamora sibling** (LIFT RUN item W1) once it exists — not runtime ≡ the sealed wall-less cells.
- **D-CP2-2:** interrupt behavior enters the row schema as the per-skill `interrupts_channel` flag (skill property), not as mouse-binding or uniform rate.
- **OQ dispositions at close:** OQ-6 lean (C) carried into the LIFT RUN charter § 4 unruled; F-5's G-0 coverage-before-accuracy gate performed as designed and carries forward unchanged.
  > ⚑ **CORRECTED IN PLACE (second integration pass, 2026-08-25) — the clause "OQ-6 … unruled" is FALSE as filed.** **R-L91-6 ACCEPTED OQ-6's split lean at Wave-4**, before this note was written; the note recorded as carried-forward a question that had already been answered. Corrected per the L-93 strike-in-place precedent — **the clause is annotated, not deleted**, because *how a ruling got mislaid* is the part worth keeping. Same family as the L-94 *"all three R-L91-8 items DISPOSED"* overstatement caught at LIFT L-5: **a disposition evaporating inside a close-out summary.** Twice in one run, in opposite directions — once a routed item summarised as ruled, once a ruled item summarised as routed. The rest of this bullet (F-5's G-0 gate carrying forward unchanged) **stands**.

*Filed 2026-08-25 by gandalf (`SPEC-AUTHOR`), Wave-4, KC2 MODEL-COMPLETION RUN. No production code. Files to run notes per charter § 7; committed, not pushed — the conductor releases.*

*Integrated 2026-08-25 by gandalf (named sub-agent, `SPEC-AUTHOR`), **KC2 LIFT RUN Wave-2** (`2026-08-25-kc2-lift-run-charter.md` § 4). Scope of that pass: **D-CP2-1..3 only.** Forward supersession — nothing deleted, superseded readings named in place. **K-7 held**: the sealed reference's wall-less, 0.15-roll description is unaltered. **§ 0's rubric declaration untouched.** **No hard-coded pack digests** — the baton manifest governs (R-L91-3). No production code.*

*Second integration pass 2026-08-25 by gandalf (named sub-agent, `SPEC-AUTHOR`), **KC2 LIFT RUN**, authorised at ledger **R-L5-4**. Scope of that pass: **R-L91-4..8 + R-L92-2 only** — no D-CP2 integration re-opened, no design content added beyond the rulings. The RNG **tape** is out of the drive contract and out of OQ-3; **bands + the draw-site registry** replace it. Forward supersession throughout; superseded readings named in place, nothing deleted. **K-7 held**; **§ 0's rubric declaration untouched.** No production code.*
