# W4 · THE TWIN-TEST SPEC — how drax proves the Godot build is a faithful twin

> ▶ **ROLE: SPEC-AUTHOR** — Wave-4 piece, charter tag **F-5**.
>
> **STATUS:** SPEC — consumable by a later drax session. **Spec, not code.** No production code in this seat; the build is a separate session (charter § 7 seat-map: drax is **recipient-only** this run, and this file lives in the run's notes, never in `reincarnated-godot/`).
> **Run:** KC2 MODEL-COMPLETION RUN · **Wave:** 4 (export + handoff) · **Date:** 2026-08-25
> **Author:** gandalf (named sub-agent, `SPEC-AUTHOR`) · **Conductor:** gandalf `RUN-CONDUCTOR`
> **Companion:** `2026-08-25-kc2-mc-w4-godot-runtime-spec.md` (charter tag SKIRT) — *what* the runtime implements. This file is *how it is proven.* Read that one first; this one grades it.
> **Authority rows:** charter `2026-08-24-kc2-model-completion-run-charter.md` § 1.4 + § 3 Wave 4 · ledger **L-83** (Wave-4 gate = the policy-fix seal) · **L-85** (measured release policy + the two DO-NOTs) · **L-88** (the fix delivered; the residual does not move; R-L88-5 figure hygiene) · **L-89** (R-L89-2: the uniform 0.15 is a named approximation) · **L-90** (R-L90-2: binding exclusivity is the Layer-1 rule; R-L90-6 fires this wave) · **L-68** (R-L68-2: the metre-scale pin fires at Wave-4 assembly) · schema `2026-08-24-s1-baton-v2-schema-draft.md` §§ 3–5.
> **Standing law binding on every line:** **Law 3** (no fitted constants, no invented rules) · **D5** (`E-s09-cp150` immutable; siblings only) · **GL-6** (verify digest before load) · **GL-12** (absence is DECLARED, not filled) · **D4** (prereg before results) · **#72** (mechanical enumeration) · **wave-160 is a GRADED ROW, never a gate** (Matt-ruled).
> **Pattern law binding on the DESIGN of this instrument:** `operating-procedures/desirable-run-pattern.md` § 6 **obs-1** (coverage-gates before accuracy-gates) · **obs-2** (owner-eye as a pre-registered mid-run gate) · **obs-3** (rubric law).

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
| **BEHAVIORS** | every `state_id` and `transition_id` in `model/ai_states.json`; the player channel policy + input-exclusivity rule | S-1 § 2.1; runtime spec § 4–5 |
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

**Drive contract for T-1/T-2** (S-1 § 3, one sentence, unchanged): *load `model/` only into the runtime; drive the player actor along the recorded path (positions authoritative, GL-7 interpolation); consume `reference/rng_tape.jsonl` at the declared draw sites; run to the recorded end; emit the same track + event shapes; diff `acceptance.json` row by row.*

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

- **Layer 1 (the rule the runtime implements, R-L90-2):** *casting the opposite-mouse-bound skill releases the channel.* **Binding exclusivity, not skill identity** — the channel is the right-mouse skill; the left-mouse skill releases it; keyboard-bound skills are transparent. The mechanism transfers to Godot **carrying no Grim Dawn skill with it.**
- **Layer 2 (measured reference values):** per-skill interrupt rate — **Blitz (left mouse) 0.385** · **Vire's Might (key 2) 0.136** · **War Cry (key 3) 0.000**, and War Cry's casts sit in silences *shorter* than the duration-weighted null (p = 4.9 × 10⁻⁷): the channel **tightens** around them.
- **The sealed sim (which generated the reference tracks):** a **uniform 0.15 per-cast roll** — sealed before 2c landed, held per R-L89-2 rather than re-opened (K-7). **It is a named approximation: arithmetically true, mechanically false** — a cancellation of an always-interrupting family against a never-interrupting one. 8/54 = 0.148 pooled; pooled, the casts are statistically indistinguishable from randomly-timed moments (MW p = 0.286) *because two strong opposite effects meet at the average.*

**Pre-registered prediction (this is the falsifiable form, and it is the deliverable of this section):**

| quantity | prediction | grading |
|---|---|---|
| aggregate release **count** and **duty** over the run | **agrees** with the reference within the T-1 band (both mechanisms produce ≈0.15 aggregate by construction) | **asserted** |
| **per-cast attribution** — which casts a release follows | **DIVERGES**, and the direction is pre-named: the runtime releases on left-mouse casts and never on keyboard casts; the reference releases on ~15 % of casts irrespective of binding | **report-only, with the divergence direction pre-registered** |
| **run-level fight state** downstream of it (T-2 occupancy, damage) | agrees within band; the mechanism difference is texture, not aggregate | asserted, **with this row named as its first suspect** if it reds |

**Fork disposition (lean recorded; conductor rules — OQ-1).** Three ways to handle a model/reference disagreement of this kind: **(A)** runtime implements the rule; attribution rows go report-only with the divergence pre-registered *(the design above)*; **(B)** runtime carries a `twin_compat` mode implementing the uniform roll for the test and the rule for free play; **(C)** re-cut the reference from a sim implementing the flag. **Lean: (A).** (B) builds a second mechanism the team knows to be mechanically false and gives it the only code path that is ever *tested* — compat paths become the real path. (C) re-opens a sealed seat for a refinement that does not move its gates: K-7 erosion, already refused at R-L89-2.

**And the sharper instrument (A) buys, which (B) and (C) do not:** a **T-0 footage-vector table** for the exclusivity rule, graded against the *measured footage* values rather than against the sim — *does a keyboard-bound cast ever release the channel (expect: never, 19/19 clean)? does a left-mouse cast release it (expect: at rate, and for 0.60 s median, 0.53–0.67 s range, n = 8)?* This moves the proof obligation for the mechanism to the instrument that actually measured it.

**Named residual carried into every quote of this section (L-90):** slot 7 = **Rune of Rush**, a third charge skill, is **footage-blind** — its casts are outside the 53. *"Left-click interrupts"* and *"charge skills interrupt"* cannot be fully separated on this evidence. The runtime implements left-click; the residual ships with it.

---

## 6 · OWNER-EYE CHECKPOINTS — pre-registered mid-build gates (obs-2), including F-5

obs-2 was paid for: both KIT-FIDELITY catches were Matt's, mid-stream, unprompted, while the run's own gates said green twice. **The owner's eye is an instrument of record, not a briefing recipient.** For a build whose output is a watched surface, it is scheduled at named points *before* downstream gates build on unviewed state.

| gate | when | object | what it rules |
|---|---|---|---|
| **OE-1 · CAMERA (F-5)** | **first frame that shows the player in the arena** — before any accuracy work | one still + one short clip under the starting-recommendation camera | the register (see § 6.1). **Blocks OE-2.** |
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
- [ ] **A-2** — **T-0 green**: every `test_vectors` row reproduced to declared precision, including the § 5 footage-vector table for the exclusivity rule.
- [ ] **A-3** — **T-1 / T-2 graded row-by-row** against `acceptance.json`, each red row carrying a named first suspect rather than a re-tuned band. **No band widened post-hoc, by anyone** (the L-88 precedent: a failed band was carried FAILED-AS-REGISTERED rather than widened, by seat *and* by conductor).
- [ ] **A-4** — **T-3 reported, asserted nowhere**; terminal wave prominent and un-gated.
- [ ] **A-5** — **§ 5 divergence report**: aggregate agreement asserted, per-cast attribution divergence reported against its pre-registration.
- [ ] **A-6** — **OE-1 (F-5) ruled by Matt on an identified frame**, OE-2 and OE-3 held in order.
- [ ] **A-7** — the report card carries the **§ 0 rubric declaration verbatim on its face**, so no reader can mistake *runtime ≡ sim* for *build ≡ Matt*.

**And one anti-criterion, stated as a criterion:** the twin-test is **not** satisfied by a green tier table over an unclosed census, and it is **not** failed by a terminal wave below 160.

---

## 9 · OPEN QUESTIONS BACK TO THE CONDUCTOR

*Decision-shaped. Not resolved here.*

**OQ-1 — the cast-interrupt divergence handling.** (A) rule + report-only attribution + footage-vector table *(§ 5, leaned)* · (B) `twin_compat` dual mode · (C) re-cut the reference. **Lean: (A).** Conductor's call whether the pre-registered prediction table in § 5 is sufficient, or whether Matt should see the fork (it is the visible-consequence kind: it decides what the character's kit *feels* like — one safe skill to weave, or every skill occasionally clumsy).

**OQ-2 — which sibling checkpoint is Layer 2 cut from.** S-1 pinned `E-s09-cp150-mech` (`20b05cb4…`), but B-1…B-5, B-2app, B-3app, B-4app, PM5 and **M-POL-2** (`ad61ad2a…`) have all landed since. **This spec deliberately hard-codes no sha** and requires only *"the final post-M-POL-2 sibling."* Conductor/star-lord pin it at cut; the twin-test spec must never carry a stale sha, and D5 forbids touching the parent.

**OQ-3 — RNG tape vs statistical bands** (S-1 OQ-3, still open and now costed by this document). The tape makes T-1/T-2 exactly reproducible; without it every tier degrades to a distributional comparison and the § 5 attribution test loses its sharpness. Tape size is unknown until the completed model's draw count is known. **Lean: tape, with per-wave segmentation if size bites.**

**OQ-4 — does the metre-scale pin land before or after the first owner-eye gate?** `R-L68-2` fires the scale pin **at Wave-4 baton assembly** (register the Class-1 minimap footprint against the final pursuit model's occupancy hull); until it lands, `u = 0.198 m/px` carries a **1.7×** band `[0.094, 0.366]`. **A camera ratified against an arena whose metre scale later moves by up to 1.7× is a ratification of a different scene.** (A) OE-1 waits for the pin · (B) OE-1 fires on native-px geometry and is explicitly re-run if the pin moves scale beyond a pre-registered threshold. **Lean: (A)** — it costs sequencing, and (B) spends Matt's eye twice on the same question.

**OQ-5 — does PM5's report card share a row schema with `acceptance.json`?** (S-1 OQ-8, unresolved and now load-bearing: § 0's rubric declaration is the *reason* the two instruments must not be conflated, and a shared row schema is the cheapest way to make wave-160's `report_only` flag honoured by both.) **Lean: shared row SCHEMA, disjoint row SETS.**

**OQ-6 — who owns the harness?** The twin-test needs a runner that loads both layers and grades rows. (A) drax builds it inside the Godot seam · (B) star-lord builds it engine-side against emitted runtime output · (C) both halves, meeting at a declared output format. **Lean: (C)** — the runtime emits track + event shapes; the grading lives with the emitter that generated the reference, so the two sides of the diff are never written by the same hand.

---

*Filed 2026-08-25 by gandalf (`SPEC-AUTHOR`), Wave-4, KC2 MODEL-COMPLETION RUN. No production code. Files to run notes per charter § 7; committed, not pushed — the conductor releases.*
