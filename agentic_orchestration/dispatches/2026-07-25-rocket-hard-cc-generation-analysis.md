# Dispatch — 2026-07-25 — rocket — Hard-CC generation analysis (C5)

**From:** knight-rider
**To:** rocket (generation seam)
**Origin:** Gate-2 condition **C5**, `agentic_orchestration/qa/findings/2026-07-25-gate2-gamora-f8-cc-wiring.md`
— routing assigned to knight-rider, *"routing CONFIRMED, not redirected… correctly generation-side → rocket."*
**Authorization:** standing Gate-2 process; no new Matt authorization required for the **analysis**.
A **build** requires a design ruling that does not yet exist — see § 6.
**Estimated effort:** ~2–4 hours (Pattern B — needs its own session; the pipeline surface is wide)
**Mode:** **ANALYSIS-FIRST. NO PRODUCTION CODE.**

---

## 1. The finding, stated exactly

The simulation seam just wired the **consumption** half of the hard-CC stack (`stun` / `freeze` /
`root` / `silence`) into the live loop. Before that change these effects had complete *application*
machinery — effect registry, DR immunity windows, boss resist tier, refresh law, state predicates —
and **zero live consumers**. They are now consumed: they gate action and movement.

Then gamora measured, and found the other half of the problem:

> Across **66 kit configs** in the census: **61 have `cc_effects = 0`**, **5 have `cc_effects = 4`**,
> and the census `magnitudes` dict has exactly **one key — `chill`** — at exactly one magnitude
> (`duration_seconds: 3.0`, `slow_percent: 0.35`).

Runtime instrumentation over the full 64-cell frame agrees, and does so in the strongest available
form. The harness's counter uses a create-on-first-increment `bump()`, so **key absence is a hard
zero**:

```
nav_calls 5664356 · select_calls 1685024 · attempt:chill 14802 · landed:chill 5116
nav_slowed 12180 · attempt:burn 14919 · landed:burn 5009
```

No `select_action_locked` key. No `nav_move_locked` key. **Across 5.66 M navigate calls and 1.69 M
selector calls, stun / freeze / root / silence were attempted zero times.**

jack-ryan verified this independently at Gate 2 (`Counter({0: 61, 4: 5})`, single `chill` key,
single magnitude) and it was **re-confirmed byte-identical in the post-remediation re-run**. This is
not an estimate and it is not "small" — it is a measured hard zero.

**Consequence:** the engine has a fully built, unit-proven hard-CC mechanic that **no generated
content can invoke**. The sim cannot measure what is never emitted. This dispatch establishes why.

---

## 2. Your question — three parts, all descriptive

**Q1 — WHERE would hard CC be emitted?** Map the generation-pipeline surface at which an effect of
type `stun` / `freeze` / `root` / `silence` would attach to a generated skill. Name the file:line
seams. Known starting points (do not treat as exhaustive; find the real path):

- `src/reincarnated/generation/layer2_dimensions.py:75` — `SILENCE = "silence"` exists as a
  generation dimension. So at least one hard-CC concept is already *declared* generation-side.
- The ailment registry `config/ailments.yaml` carries 16 entries including `root` (`:91-96`),
  `freeze` (`:238-242`), `stun`. **`silence` is deliberately NOT in the registry** — it is documented
  as a non-ailment status effect at `src/reincarnated/foundation/effect_categorization.py:36`, with
  a live producer at `damage_resolver.py:1182-1187`. **Silence and the three registry ailments may
  therefore have entirely different emission paths.** Do not assume one answer covers all four.
- Candidate seams to walk: `ability_grammar.py`, `mechanic_alteration.py`, `per_skill_emitter.py`,
  `kit_finalization.py`, `d10_kit_constraints.py`, `role_constraints.py`, `skill_schema.py`,
  `element_biases.py`. This list is a starting hypothesis, not a finding.

**Q2 — WHY are they not emitted?** This is the load-bearing question and it has materially different
answers with materially different build costs. Discriminate between at least:

- **(a) Never implemented** — no code path attaches these effect types to a generated skill at all.
- **(b) Implemented but gated** — a path exists behind a flag, role constraint, tier gate, element
  gate, or BC-axis constraint that is never satisfied by the current pool.
- **(c) Pool/config-shaped** — the path exists and is reachable, but the config the census sampled
  (weights, allow-lists, element biases, D10 constraints) drives the probability to zero or near-zero.
- **(d) Emitted upstream, dropped downstream** — attached at one layer and filtered out before
  kit finalization.

**Do not settle for a plausible answer. Discriminate empirically** (Discipline #10 — empirical
inspection over assumption). The cheapest refuting test per hypothesis, run read-only, beats a
confident reading. If the answer differs per effect type — which is likely given silence's
out-of-registry status — say so per type.

**Q3 — What would a BUILD look like?** A proposal, not an implementation. Scope, seams touched,
config surface, cross-seam impact, what would need a math note, what the smoke gate would be, and
an honest cost estimate. If the answer to Q2 is (c), the "build" may be a config change and you
should say so plainly rather than manufacture work.

---

## 3. Out of scope — explicitly

- **No production code.** No emission path is to be built, unblocked, or reweighted in this dispatch.
- **No config changes** — not even a one-line weight nudge to prove reachability. If you need to
  demonstrate reachability, do it in a throwaway probe under `agentic_orchestration/rocket/notes/`,
  not in `config/`.
- **No ruling on whether kits SHOULD emit hard CC.** See § 6. That is not yours and it is not mine.
- **No simulation-seam work.** The consumer side is built, Gate-2-cleared, and closed. If you find
  a consumer-side defect, report it — do not fix it.
- **No ailment-registry edits.** `config/ailments.yaml` is spec-governed
  (`canonical/reap-die-rise-engine/ailment-layer-engine-spec.md`, Gate-1 PASS-WITH-AMENDMENTS).
- **Do not re-derive gamora's census or blast-radius numbers.** They cleared Gate 2 and were
  re-confirmed post-remediation. Consume them; don't re-litigate them. If you believe one is wrong,
  that is an escalation to me, not a work item.

---

## 4. Required reading before starting

| Document | Why |
|---|---|
| `agentic_orchestration/qa/findings/2026-07-25-gate2-gamora-f8-cc-wiring.md` | The Gate-2 finding that generated C5. Read the "A/B evidentiary asymmetry" section and the L0 ruling. |
| `agentic_orchestration/gamora/notes/2026-07-25-f8-cc-wiring-and-blast-radius.md` **§ 4.4** | The census finding, verbatim, with the exercise counters. This is your primary evidence. |
| `~/Games/reincarnated-engine/src/reincarnated/simulation/MIGRATION.md` (top entry + `gamora/v-f8-cc-2` AMENDMENT) | What the consumer side now does, and the semantic shifts it named. Cross-seam contract — this is truth (REVIEW_PROCESS #4). |
| `~/Games/reincarnated-engine/config/ailments.yaml` `:91-103`, `:238-248`, `:264-273` | Registry semantics for root / freeze / stun. Note: **root locks movement only, not action** — a root that blocked action would be a freeze. |
| `~/Games/reincarnated-engine/src/reincarnated/foundation/effect_categorization.py:35-38` | Why silence is not in the registry, and what that implies for its emission path. |
| `canonical/reap-die-rise-engine/ailment-layer-engine-spec.md` | The governing spec. Check whether it already says anything about *generation-side* emission — the Gate-2 finding established there is **no ailment-layer spec intent for silence**; verify whether the same is true for the three registry ailments. |
| `agentic_orchestration/dispatches/2026-07-25-gamora-f8-cc-consumer-wiring.md` | The build charter, and Matt's ruling that governs this whole program (§ 6 below). |

---

## 5. Math-before-code (Discipline #1)

This dispatch is analysis-only, so no implementation math note is owed. **But if your § 2 Q3 build
proposal recommends a build, the proposal must name what math the build would owe** — specifically:
if hard CC becomes emittable, the **control-density BC axis** changes meaning. `MIGRATION.md` already
flags this on the consumer side:

> *"The `control density` BC axis measured a population whose control effects moved nothing. Any BC
> coordinate derived from control density pre-2026-07-25 was measuring an emitted PROPERTY, not a
> realized EFFECT."*

Your proposal should state whether making hard CC emittable **re-opens that axis** and, if so, what
re-derivation it would owe. Flag it; do not attempt the re-derivation here.

**Discipline #25 (semantic-layer rep-audit) applies** if any part of your analysis inherits cluster
identity from substrate work as design substrate.

---

## 6. The design ruling that GATES any build — not yours, not mine

**Whether generated kits SHOULD emit hard CC is an open design question.** It is queued for **Matt's
grill session**, with **gandalf owning the elicitation**. No build fires until that rules.

This is not bureaucratic sequencing. The question is genuinely load-bearing — hard CC on generated
mob kits means player-facing stun/freeze/root lockouts, which is a **player-experience commitment**,
not a generation-parameter tweak. It sits squarely in gandalf's lane.

**What your analysis is FOR:** giving that ruling something real to rule on. A design call made
without knowing whether the answer is "flip a config weight" or "build a new emission layer" is a
call made blind. Your job is to remove that blindness — not to pre-empt the call.

**Frame your Q3 output accordingly:** *"if the ruling is yes, here is what it costs and touches"* —
not *"here is what we should do."* If your analysis surfaces evidence that bears on the design
question itself (e.g. an existing intent buried in a spec, or a reason emission was deliberately
suppressed), **surface it prominently** — that is exactly the input gandalf's elicitation needs, and
it is the highest-value thing you could find.

**Matt's governing ruling for this program (verbatim, 2026-07-25):**

> *"We ARE building all mechanics needed into our engine. If we don't yet have CC in the sim, then we
> build it in — we don't work around it."*

Note the scope word: **"needed."** The boundary on "needed" comes from the **G1-B scope ruling**
(two-sided attestation census, dispatched to elrond at
`dispatches/2026-07-25-elrond-gd-attestation-scope-census.md`, Matt ratifies the census *output*
roster). If your analysis touches attestation-relevant ground, cross-reference it rather than
duplicating it.

---

## 7. Cross-seam contract change? (Principle 6 gate — completed at authoring)

**No.** This dispatch is analysis-only and moves no schema surface. No `MIGRATION.md` is owed.

**However** — flag in your output if a *future* build would move any of:
- a `loadout` dict key (rocket → star-lord / drax boundary)
- the season-JSON export packet shape (`season_writer.py`)
- the skill schema consumed by `season_exporter.py`

If the answer to any of those is yes, say so; that determines whether the eventual build dispatch
carries a `MIGRATION.md` requirement per ADR-004.

---

## 8. Acceptance

Analysis output at `agentic_orchestration/rocket/notes/2026-07-25-hard-cc-generation-analysis.md`
containing:

1. **Q1 — the emission-surface map**, file:line, per effect type (`stun` / `freeze` / `root` /
   `silence` handled separately — silence is likely to differ).
2. **Q2 — the cause**, discriminated empirically among (a)/(b)/(c)/(d), **with the evidence that
   discriminates it**, per effect type. "I could not discriminate between (b) and (c) and here is
   why" is an acceptable and honest finding. A confident unfalsified guess is not.
3. **Q3 — the build proposal**: scope, seams, config surface, cross-seam impact, math owed, smoke
   gate, honest cost. Explicitly framed as conditional on the § 6 ruling.
4. **Anything you find that bears on the DESIGN question** — flagged prominently for gandalf's
   elicitation.
5. **Completion record appended to this dispatch file** per `dispatches/README.md`.

**No tag required** (no code). **Commit auto-fires** per team discipline — the analysis is the
work-product of an authorized task. **Do not push** (ADR-006, Matt-gated).

**Gate:** analysis output routes back to knight-rider, who folds it into the gandalf elicitation
packet. **No Gate 2 is pre-registered** — there is no code to review. If your Q3 proposal is adopted
by the ruling, the resulting *build* dispatch carries its own Gate 1 + Gate 2.

---

## 9. Dispatch ledger — associated non-blocking items

Recorded here so they are not lost; **neither is yours to action**.

| Item | Owner | Status |
|---|---|---|
| `export/season_exporter.py:266` — player-facing silence text reads *"Prevents ability use"* with no mobility/defensive carve-out. Realized F8 behavior gates **offensive** skills only, so the text **under-describes** actual behavior. | **star-lord** | **INFO, non-blocking.** No standalone dispatch fired; folds into star-lord's next export-surface pass. Text-accuracy item, no schema surface moves. *Relevant to you only if your analysis changes what silence does.* |
| Player-side `curse:decrepify` deliberately unwired (Wave-D scope) | gamora | Named follow-on, not a gap |
| `M_min = 0.06` combined movement floor — no design authority to introduce one | gandalf / Matt | Routed design item |
| Corpse-chill application ordering — ailments apply post-damage with no defender-liveness gate; **91.8% of chill landings hit an already-dead defender** (re-measured, full frame, Gate-2 C2) | gandalf / Matt | Routed design item. **Note for your Q3:** if hard CC becomes emittable, this ordering question applies to it too — a stun stamped on a corpse is as inert as a chill on one. Worth a sentence in your proposal. |

---

**Standing watch item you should know about:** `select_action_locked` and `nav_move_locked` are
currently hard zeros in every production frame the engine has ever run. If your work leads to a build
that makes them non-zero, **the first hard-CC ladder run is a novel-path event** and jack-ryan has
asked that it be watched rather than treated as routine telemetry. Carry that forward into your Q3
smoke-gate proposal.

**Signed:** knight-rider, 2026-07-25. C5 routing per Gate-2 finding. Analysis first; the ruling gates the build.

---

## Completion record

**Agent:** rocket (generation seam) · **Date:** 2026-07-25 · **Status:** COMPLETE
**Output:** `agentic_orchestration/rocket/notes/2026-07-25-hard-cc-generation-analysis.md`
**Constraints honored:** no production code, no config change, no ailment-registry edit, no
re-derivation of gamora's census (reproduced as a control only), no simulation-seam work.
**Probes (throwaway, read-only, under `rocket/notes/`):** `2026-07-25-hard-cc-probe.py` (P1-P7
surface probes), `2026-07-25-hard-cc-probe2.py` (census-population effect histogram).
**Tag:** none owed (no code). **Push:** not performed (ADR-006).

### Answers, one line each

- **Q1 (WHERE).** Two pipelines. **Pipeline A — live:** `per_skill_emitter.py:1337-1342` (primary
  effect, role-named) and `:1351-1356` → `_make_signature_ailment_effect():800` with its hard-control
  gate at **`:817`**. **Pipeline B — orphaned:** `ability_grammar._sample_effects():556` /
  `_make_ailment():649` (root/knockback/shock at `:712-718`) / `_make_effect():636-638` (silence),
  plus `role_constraints.py:120`. Pipeline B has **no production caller** — `MonsterGenerator` /
  `TrialGenerator` are instantiated only in `scripts/` and `tests/`; `season_orchestrator.py` is gone.
- **Q2 (WHY).** Per type: **root = (b) gated** — unconditional `return None` at `:817`, keyed on the
  registry `is_control` field; not a weight, so **not (c)**. **freeze / stun = (a) then (b)** —
  `SECONDARY_AILMENT_MAP` (`element_biases.py:120`) has **zero production readers**, and even with a
  reader `:817` refuses them. **silence = (a)** — out of registry, no site exists in the live emitter
  to gate. **(d) ruled out** for all: `_build_real_player_class` consumes `kit.skills` unfiltered.
- **Q3 (COST).** **Not a config change** — stated plainly as the dispatch asked. Smallest honest
  build is Option A (control-role payload), **10-17 h / 2-3 sessions**, ~$0 LLM, plus a DR-guardrail
  math note that is gandalf+gamora's, not mine. `MIGRATION.md` **IS owed** (no key moves, but the
  `effects[].name` value domain widens — three downstream readers).

### Flagged for gandalf's elicitation (dispatch § 6 / acceptance item 4)

1. **Matt already ruled adjacent to this, on 2026-06-20** — the `is_control != hard` cut
   (`gandalf/notes/2026-06-20-is-control-cut-classification-and-signature-assignment.md`). The live
   exclusion is a faithful implementation of it. **Its scope was hard CC riding every chain_A primary
   attack, not hard CC in a dedicated control slot**; gandalf's own §5 says the guardrail is
   "retired for this cut, not deleted from the design space." The elicitation should rule on the
   question the cut never reached, not re-litigate the cut.
2. **The exclusion set silently widened after that ruling.** `freeze` and `stun` joined
   `_HARD_CONTROL_AILMENTS` at registry-edit time (2026-07-16) with no design ruling — inverting the
   ailment-layer spec's own §3.4 intent for ice→freeze. Unnamed Discipline-#12 shift; the stale
   comment at `per_skill_emitter.py:797` is its visible trace.
3. **The larger gap is not hard CC — it is that the control role has no mechanism at all.** 133
   effects literally named `"control"` in the 66-config census population; `damage_resolver`'s effect
   loop has no branch for that string and no `else`. Control-role skills are inert on both axes. This
   sharpens the `simulation/MIGRATION.md` control-density caveat: for control-role skills there was
   not even an emitted property, only a placeholder string.
4. **Silence is design-blocked, not engineering-blocked** — working producer and consumer predate the
   registry ailments; no spec anywhere says what it is for.
5. **Corpse ordering matters more for hard CC than for chill** — a lockout budget fitted to `landed:`
   counters at the measured 91.8% corpse ratio would be ~12× the realized one. Resolve before the
   calibration run, not after.

### Non-blocking items surfaced, routed not actioned

- **star-lord:** `export/season_exporter.py:255-266` — the player-facing ailment table is stale
  beyond the one sentence in the dispatch ledger. Documents 6 of 16 ailments, marks `root` "(demo2)",
  and labels `silence` **"Fire-element signature"** (silence has no element and is not in the
  registry). Whole-table pass, not a one-line fix.
- **rocket (own seam, future):** `mechanic_alteration.py:1235` `zone_control_effect:
  "element_signature"` — declared, zero consumers anywhere. A second inert control declaration.
- **rocket (own seam, future):** `d10_kit_constraints._element_specific_effects:364` omits
  freeze/stun/silence/knockback — a curation-path drop risk the moment hard CC is emitted.

**Routes to:** knight-rider, for the gandalf elicitation packet.
