# Stranded-live-clause audit — the § 7 relocation, the derived citation set, and what else Tranche 1b took with it

**Date:** 2026-08-24
**Author:** gandalf (CANON-STEWARD)
**Class:** verdict / recognition record + governance proposal
**Trigger:** jack-ryan ruling batch, Step-2 VFX build wave (engine `9307b46b`, collab `fba2a064`), routed item (a): *"`substrate-expansion-decision-2026-05-17.md` has no live home while eleven code and math files cite its § 7 — gandalf rules restore-to-canon vs. rewrite-citations-to-git."*

> **Method note.** Every count in this document was derived from the live artifacts, not taken from the brief (Discipline #76 clause 2). Deltas against the brief's numbers are reported in both directions, including where the brief was right. One recommendation in the companion `spark` draft was withdrawn mid-work when my own evidence refuted it; that is recorded there, not hidden.

---

## § 1 — The relocation call

**RULED: restore the whole document, single home, no mirror.**

`canonical/reap-die-rise-engine/substrate-expansion-decision-2026-05-17.md` — `STATUS: CURRENT`, with a restoration record in the header. Done this session.

### Why not the alternatives

**Why not "rewrite citations to point at git."** That option treats the `git show` locator as a permanent address. It is a fine *interim* authority — jack-ryan used it correctly as one — but as a durable citation target it institutionalises the exact cost this item measured. Three agents reasoned from the citation rather than the record. The reason they did is that opening it required knowing the sweep commit, knowing to walk `^`, and knowing the pre-sweep subdirectory. A resolvable path costs one `Read`. **The whole failure is a story about the price of opening a document; the remedy must lower that price, not ratify it.**

**Why not extract § 7 to its own doc beside `pool.py`.** This was my first instinct and it is wrong. The argument for it is good — § 7 has a different lifecycle from the rest of the doc (an exit condition the rest does not have), and lifecycle-mismatch inside one container is exactly what killed it. But splitting produces two homes and requires editing 70 citation sites, and the extracted half would then be a *second* statement of a rule whose first statement is a Matt-ruled record.

**Why not mirror § 7's operative rule into the engine.** Refuted by this file's own history, which is the strongest available evidence: **the `vocab_freeze_note` in `vfx_coverage_manifest.json` WAS a mirror of § 7.** It asserted "Frozen IDs: thunder, bolt, divine, umbra (none currently in pool.json)". That parenthetical went **false on 2026-06-01** when the WS1A Q18 lock added 39 frozen-primary entries including three of the four named, and it stayed false and unread for twelve weeks until rocket's X-3 pass corrected it. Duplicated truth without a sync mechanism drifts by default — Discipline #74, and the § 4.8 queue-rows-are-views precedent. **A mirror of § 7 has already been tried and it decayed.** One home.

**Why `reap-die-rise-engine/` and not `reap-die-rise-story/`.** The doc is substrate architecture: resistance-matrix shape, trait-floor extension, gear-affix gating, pool D1 re-score, generation-frequency balance. Its cosmology sections (§ 4) are integration notes, not the story spec. Everything that cites it is engine code or engine math notes.

### The STATUS stamp is the actual defect, and I want that on the record plainly

The sweep was defensible. `HISTORICAL-INFORMATIVE` was not. **Nothing this document specifies has shipped** — Phase-1 P1 is unstarted; the resistance matrix is still 4×4; the substrate set is still canonical-four. The stamp was applied on the doc's *date* and its *pre-Epoch-4* provenance, not on its *liveness*, and every downstream action then behaved correctly against a false premise. Tranche 1b did not misjudge this doc; it inherited a misjudgement. That is #19.1(b) one layer up from where jack-ryan found it — the sweep inherited the stamp's claim without verifying it, exactly as rocket and I later inherited the citation's claim without verifying it. **Same defect, three times, one document.**

---

## § 2 — The derived citation set

**17 files across two repos, 70 citation sites.** Derived by `git grep` on tracked files in both repos plus the three sibling repos (godot / demo / loadout: zero).

### Engine — 13 files, 62 sites

| File | sites | cites § 7? |
|---|---|---|
| `src/reincarnated/foundation/vocab/grouping-layer-vocabulary.md` | 21 | yes (L399) |
| `src/reincarnated/generation/math/d10-substrate-coherent-generation-rules-phase-1-p1.md` | 12 | no |
| `src/reincarnated/simulation/math/resistance-matrix-7x7-phase-1-p1.md` | 5 | no |
| `design/decisions/decisions-log.md` | 4 | yes — *this session's ruling record* |
| `src/reincarnated/element/MIGRATION.md` | 4 | yes (L556) |
| `data/seasonal_elements/vfx_coverage_manifest.json` | 2 | yes (L5, L1419) |
| `src/reincarnated/element/pool.py` | 2 | yes (L13, L109) |
| `src/reincarnated/generation/AGENT_STATE.md` | 2 | yes (L38, L4739) |
| `src/reincarnated/generation/math/d3-path-a-archetype-composition-phase-1-p1.md` | 2 | no |
| `src/reincarnated/llm/PHASE-1-P1-REFACTOR-PLAN.md` | 2 | no |
| `design/working-agreement/engineering-disciplines.md` | 1 | yes — *this session's #76 instance 4* |
| `src/reincarnated/generation/MIGRATION.md` | 1 | no |
| `src/reincarnated/simulation/resistance_matrix.py` | 1 | no |

### Collab — 4 files, 8 sites

| File | sites |
|---|---|
| `agentic_orchestration/dispatches/2026-08-24-rocket-x3-vfx-coverage-manifest-refresh.md` | 3 |
| `agentic_orchestration/jack-ryan/research/legacy-constraint-audit-2026-05-21/constraint-inventory.md` | 3 |
| `agentic_orchestration/research/curated/monster-subset-vs2a-2026-05-17.jsonl` | 1 |
| `agentic_orchestration/research/scripts/build_pimen_subset_vs2a_2026_05_17.py` | 1 |

### Sections cited across the corpus (derived)

`§5.1`×10 · **`§7`×7** · `§5.4`×5 · `§3.2`×4 · `§4.4`×3 · `§4.1`×3 · `§7.1`×2 · `§6`×2 · `§2.2`×2 · `§6.5.4` · `§6.5` · **`§5.7`** · `§5.6` · `§5.5` · `§3.1`

**§ 5.7 does not exist.** `generation/math/d3-path-a-archetype-composition-phase-1-p1.md` cites *"`substrate-expansion-decision-2026-05-17.md` § 5.7 — Path-a recommendation."* The document has §§ 5.1–5.6 and no § 5.7, in the swept version or any prior one. A math note is anchored on a section number that has never existed — and nobody noticed, because for eight weeks the anchor could not be checked. Third-order consequence of the strand. **→ rocket: re-anchor or delete.**

### Delta against jack-ryan's "eleven" (#76 clause 2 — reported in both directions)

His enumeration: `element/pool.py`, `element/MIGRATION.md`, `generation/MIGRATION.md`, `generation/AGENT_STATE.md`, `simulation/resistance_matrix.py`, **four** `math/*-phase-1-p1.md` docs, `llm/PHASE-1-P1-REFACTOR-PLAN.md`, `foundation/vocab/grouping-layer-vocabulary.md` — plus the manifest and the X-3 dispatch named separately.

- **Named but not derived:** the **fourth** `math/*-phase-1-p1.md` doc. There are **three** (`d10`, `d3`, `resistance-matrix-7x7`). His set of distinct pre-existing engine consumers derives to **10**, not 11.
- **Derived but not named:** `decisions-log.md` and `engineering-disciplines.md` (both his own artifacts authored this session — ruling record, not consumers; correctly excluded on intent). Plus **three collab files he did not name**, of which one matters: **`jack-ryan/research/legacy-constraint-audit-2026-05-21/constraint-inventory.md`.**
- **His substantive claim was right in every direction that mattered.** No file he named is absent from the derived set except the phantom fourth math doc, and no *code* citation was missed.

### The finding inside the delta

The legacy-constraint audit is a purpose-built inventory of legacy constraints, run 2026-05-21 — four days after § 7 was authored. It cites this document three times, sourcing **LC-001** (§ 3.1), **LC-012** (§ 3), and **LC-022** (§ 5). **It does not inventory § 7.** A dedicated constraint register, reading this exact document, walked past the standing constraint.

That is worth more than it looks. It refutes the obvious remedy — *"keep a register of live constraints"* — by showing the register was already built and already missed this one. **Registers are enumerations.** The remedy has to be a derivation, which is what § 4 proposes.

---

## § 3 — Was § 7 the only live constraint in the 98? **No.**

Derived from `git show --numstat 5fc2890b`. Full population: **98 files** (`canonical/story/historical/` 80 · `canonical/historical/` 15 · `canonical/story/dead/` 2 · `canonical/story/archived/` 1).

| Cut | Count |
|---|---|
| Swept in Tranche 1b | **98** |
| Still referenced by name in live tracked files (either repo) | **81** |
| Referenced by **executable code / config / data** (`.py`/`.json`/`.yaml`/`.jsonl`/`.sh`/`.tscn`/`.ts`) | **24** |
| …of those, **re-homed** so citations resolve | **1** — `grouping-layer-vocabulary.md` → `engine:src/reincarnated/foundation/vocab/` (**not by the reorg** — rocket repointed it on **2026-07-17**, `0059ca55`, "Wave-D slice-0 vocab-loader repoint (Option A engine-internal home)", i.e. it was homeless for 17 days and a specialist rescued it while doing unrelated work) |
| …of those, **homeless — the § 7 shape** | **23** |

**23 documents are cited by running code, config or committed data, and resolve to nothing in any repo.** § 7 was not an outlier; it was the one that happened to be poked.

### The homeless 23, with their code consumers

| Doc (all `git show 5fc2890b^:…`) | Cited by |
|---|---|
| `movement-speed-baseline.md` | `export/schemas.py`, `generation/class_schema.py`, `monster_generator.py`, `monster_schema.py`, `season_generation_pipeline.py`, `simulation/combatant.py`, `telemetry/migrations.py`, + 3 tests |
| `substrate-identity-declarations-2026-05-17.md` | `config/ailments.yaml`, `config/elements.yaml`, `generation/element_biases.py`, `simulation/resistance_matrix.py`, `scripts/pitch/generate_hero_images.py` |
| `09-geometry-palette-discussion.md` | `canonical/sidecars/atomic_substrate_registry_v1.json`, `emit_substrate_registry.py`, `tests/test_b11_geometry_palette.py`, + 2 collab |
| **`substrate-expansion-decision-2026-05-17.md`** | `element/pool.py`, `simulation/resistance_matrix.py`, `vfx_coverage_manifest.json`, + 1 collab — **RESOLVED this session** |
| `r2-h1-leash-timeout-disposition-2026-05-19.md` | `spatial_gauntlet/arena.py`, `spatial_engine.py`, + 2 scripts |
| `asymmetric-perceived-aoe-radius-briefing-2026-05-17.md` | `foundation/perception_asymmetry.py`, `telemetry/migrations.py`, + 1 test |
| `wide-net-coupling-archaeology-2026-05-17.md` | `config/ailments.yaml`, `config/roles.yaml` |
| `court-of-forms.md` | `foundation/court_persistence.py`, + 1 test |
| `embodiment-narrative-layer.md` | `generation/class_schema.py`, + 1 test |
| `form-bias-cadence-strategy.md` (`dead/`) | `generation/class_schema.py`, `tests/test_grouping_layer_schema.py` |
| `r2-h1-recalibration-disposition-2026-05-19.md` | `spatial_gauntlet/arena.py`, `spatial_engine.py` |
| `gauntlet-arena-scenarios-magic-elite-miniboss-2026-05-21.md` | `spatial_gauntlet/arena.py`, + 1 test |
| `spatial-data-jsonschema.md` | `telemetry/migrations.py`, + 1 test |
| `audio-register-canon-2026-05-17.md` | 6 curated `.jsonl` manifests |
| `mobile-pc-pixel-sizing-ratios-2026-05-17.md` | 4 curated `.jsonl` + 1 build script |
| `vs2a-vfx-scene-needs.md` | `pimen-subset-vs2a…jsonl`, `build_pimen_subset…py` |
| `cosmology-reincarnated.md` | `foundation/court_persistence.py` |
| `17-gear-and-spirit-guide-design.md` | `generation/trait_schema.py` |
| `arena-room-hallway-system.md` | `generation/wave_composition_rules.py` |
| `spirit-guide-voice.md` | `llm/spirit_guide_voice.py` |
| `r2-st-counterfactual-findings-2026-05-19.md` | `scripts/r2_modifier_sweep_phase_b2.py` |
| `16-project-roadmap.md` | `scripts/tag-pre-stage-a2.sh` |
| `28-engine-arpg-rebalance-design.md` | `scripts/tag-pre-stage-a2.sh` |

### Which carry standing constraints — adjudicated, and honestly bounded

I ran a constraint-marker scan (`standing (constraint|freeze|rule)` · `MUST NOT` · `until … ships` · `exit condition` · `remains operative` · `in effect from`) across all 23 and then **opened** the hits rather than reporting the grep. Three classes:

**Class 1 — LIVE CONSTRAINT, NO LIVE RESTATEMENT (the true § 7 shape).**

- **`cosmology-reincarnated.md` L207** — *"Per-season vocabulary MUST NOT echo Earth-realm classical-elements labels."* A live generation constraint on the naming path, cited by `foundation/court_persistence.py`. It defers upstream to doc 37 § 6, which *does* live (`reap-die-rise-engine/`), so the rule survives — but the sentence a reader would find is homeless. **Verify-then-close.**
- **`vs2a-vfx-scene-needs.md` L985** — *"item labels may echo per-season theme words … but MUST NOT include the per-season substrate-replacement word."* A live naming rule with no restatement I could find. **Owed.**
- **`spatial-data-jsonschema.md` L477** — *"Until that lands, ALL current gauntlet-balance claims are explicitly provisional."* An unmet-condition provisionality flag on a whole claim class, cited by `telemetry/migrations.py`. **Owed.**

**Class 2 — CONSTRAINT LIVE, BUT RESTATED IN A NEVER-PRUNE SURFACE (path defect only).**

- **`17-gear-and-spirit-guide-design.md` L140-146** — *"heals BLOCKED during stun / freeze / silence (LOCKED 2026-05-17; Matt L3 verdict #121)."* A Matt-ruled lock in a homeless doc — but fully restated in `decisions-log.md` (L2606/2633/2658), which is temporal ground truth and never-prune. **The constraint is safe; only the pointer dangles.** This is the good case and it is worth naming: `decisions-log` is doing exactly the job it exists to do. **§ 7 had no such backstop.** § 7.4 lists a decisions-log entry as one of three consumption channels for the freeze, and § 6's cascade step 2 assigns its authorship to knight-rider: *"Decisions-log entry (knight-rider authors) → drafted next, gandalf reviews."* **Verified 2026-08-24: it never landed.** There is no `### ` entry in `decisions-log.md` for the substrate expansion, the six-substrate set, or the vocab freeze — before the 2026-08-24 ruling, which is a record of the failure rather than of the decision. Three *other* Matt L3 decisions from 2026-05-17 did get entries that same week (register-fence-per-UI-surface; the 75% season-failure constant; heal-blocked-by-CC). **The largest architectural decision of that day is the one whose cascade step 2 was skipped** — and that omission is the whole difference between Class 1 and Class 2. Had the entry landed, this item would have been a broken link, not a corpus-scale epistemics failure: the constraint would have been sitting in the one surface that is never pruned and is declared temporal ground truth.

**→ Owed, and I am not writing it (jack-ryan owns decisions-log authorship): a decisions-log entry for the 2026-05-17 substrate-expansion Branch A decision, carrying § 7 as its standing constraint.** Fifteen months late; the cheapest single durable fix in this document.

**Class 3 — SUPERSEDED; the marker is stale, not live.**

- **`movement-speed-baseline.md` L372** — *"Matt has chosen Option A (2026-05-16): lock VS2a player at 7.5 m/s."* **Reversed** — `generation/MIGRATION.md:5750`: *"Matt reversed Option A (7.5 m/s mid-game) on Day 4 close per gandalf's recommendation."* Not live. Its 10 code citations are lineage.
- **`spirit-guide-voice.md`** — carries live-shaped `must NOT` prompt constraints and is cited by `llm/spirit_guide_voice.py`, but the warm future-self spirit guide **was retired 2026-06-30** (router drift-guards). Different defect, worth its own look: **live code named for a retired concept.** Not mine to fix; flagged to rocket/star-lord.
- `substrate-identity-declarations-2026-05-17.md` L49 — *"Until [grouping-vocab extension] lands, lightning/holy/shadow remain provisional"* — that extension **did** land (`foundation/vocab/grouping-layer-vocabulary.md` v1.2). Condition met.

**Coverage boundary (Discipline #70 / #76 clause 4).** The three cuts above (98 → 81 → 24 → 23) are **derivations and are complete.** The Class-1/2/3 adjudication is a **read**, and I adjudicated **9 of 23**: the constraint-marker scan is a keyword net and a live clause phrased without those words would pass through it. **The uncovered population is the remaining 14, and I am declaring it rather than presenting nine as the answer.** That backlog belongs to the § 4 sweep, not to a second keyword pass — which is the point.

**The honest summary for the parent question:** § 7 was **not** the only one. It was the most consequential, because it is the only one of the 23 that is (a) enforced by a load-bearing runtime gate, (b) has an unmet exit condition, and (c) had no decisions-log backstop. But there are at least two more owed live constraints in Class 1 and fourteen documents I have not opened.

---

## § 4 — Governance proposal

> ⚠ **SWITCH: CANON-STEWARD (proposer) → jack-ryan (ratifier)** — per `canonical-doc-format.md` § 6.7. This proposes a change to the doc-lifecycle rules, and I am the largest subject of those rules. **I propose and execute; jack-ryan ratifies.** Not canon until he does.

### The root cause, derived from the rule's own text

`canonical-doc-format.md` § 6.3, prune-safe predicate 4:

> *"**Zero live references across BOTH repos** — the reference check greps `decisions-log` + `engineering-disciplines` + all OPs + all skills + `canonical/` + the trackers…"*

and `canonical-hygiene-audit-routine.md` step 2:

> *"Check decisions-log, engineering-disciplines, all OPs, all skills, `canonical/`, and the trackers."*

**Code is not in either list.** `element/pool.py` cites `substrate-expansion-decision-2026-05-17.md`; predicate 4 does not look at `.py`. So the predicate returns "zero live references" for a document cited by four engine code and data files — and returns it *correctly*, because it was asked the wrong question.

Note precisely what happened: **predicate 1 correctly excludes code from the set of things that can be PRUNED, and the reference check then inherited that exclusion into the set of things that can CITE.** Those are opposite roles. Code is never a prune *target* and is always a prune *blocker*. One list served both.

**And the shape of the defect is the shape of the week.** Step 2 enumerates six surfaces where it needed a predicate — *any tracked file in either repo that is not itself a prune candidate.* That is **Discipline #76 clause 1 inside the prune rule itself**: a set that can be computed from the artifact was typed by hand instead, and the world had a seventh member. The prune rule and the vocab freeze failed the same way, four months apart, and #76 was ratified this session for the third and fourth instances of it. **This is instance five, and it is in the governance layer.**

**This is live, not historical.** The scheduled hygiene-audit Routine fires this predicate on a cadence, over a corpus that still contains 22 unresolved instances. Left alone it will strand more.

### Proposed amendment — `canonical-doc-format.md` § 6.3 predicate 4 + Routine step 2

**Replace the enumerated surface list with a derived one:**

> **4. Zero live references across BOTH repos.** The reference check greps for the candidate's basename across **every tracked file in both repos** (`git grep` over `git ls-files`), **excluding only the candidate itself and other files in the same prune batch.** It is a derivation over the tracked corpus, not a walk of a named list of surfaces (Discipline #76 clause 1). In particular it **must** cover source, config, data and test files (`.py` `.json` `.yaml` `.jsonl` `.sh` `.gd` `.ts` `.tscn`) — **predicate 1 excludes code as a prune TARGET and that exclusion does not transfer to code as a prune BLOCKER.** A citation from running code is the strongest possible evidence a doc is live, because something executes against it.
>
> **4a. A code or data citation is never auto-prunable — it is always judgment-tier.** Where predicate 4 finds a citation from a non-markdown tracked file, the candidate does not auto-prune under any circumstances; it surfaces for ratification with the citing file:line listed. Rationale: a markdown citation can be lineage; a code citation is a runtime dependency on a claim.

**And a second, independent clause — this one is the rule that would actually have saved § 7:**

> **5 (NEW). Liveness is a per-clause property; STATUS is a per-document stamp. A demotion must adjudicate the gap.** Before stamping a doc `HISTORICAL`/`DEAD` — and therefore before it can ever enter a bulk sweep — the demoting agent asserts, in the stamp, that **no clause in the doc carries an unmet exit condition.** The check is mechanical enough to be cheap: grep the doc for `until … ships/lands` · `exit condition` · `standing` · `in effect from` · `MUST NOT` · `remains operative`, and for each hit either (a) show the condition is met, (b) show the clause is restated in a never-prune surface, or (c) **do not demote.**
>
> A doc that is 90% historical and 10% live is **not** a historical doc. It is a partial supersession (§ 6.4) and the existing rule already governs it: *never `git rm` a partially-superseded doc — that amputates load-bearing structure.* **§ 7 was an amputation, and § 6.4 already forbade it; what was missing was any obligation to look before stamping.** Clause 5 supplies the look.

**Why clause 5 is the load-bearing half.** Clause 4 fixes the *sweep*. But the sweep was downstream of a false stamp, and it acted correctly on it. Widening the reference check would have saved § 7 by accident — the doc would have been retained for a reason unrelated to why it was live. Clause 5 catches it for the right reason, and catches the case where a live-claused doc is *cited by nothing at all*, which clause 4 cannot see.

### Not proposed — and why

**A live-constraint register.** The obvious remedy, and § 2 shows it was already built and already missed § 7: jack-ryan's own `constraint-inventory.md` read this document, inventoried three of its sections, and walked past § 7. Registers are enumerations; adding another one is #76 arriving as its own remedy for the second time this session. **Rejected.**

**Backfilling the 22 remaining homeless docs immediately.** Deferred to the sweep clause 4 authorises, not done by hand now, for the same reason. Two of the 23 are already discharged (§ 7 restored; `grouping-layer-vocabulary.md` was re-homed correctly during the reorg — and it is the proof the right move exists and was already made once).

### For jack-ryan specifically

- **Ratify / amend / return** clauses 4, 4a, 5.
- If ratified, they land in `canonical-doc-format.md` § 6.3 **and** its packaged skill twin in the same commit (§ 6.8), **and** `canonical-hygiene-audit-routine.md` step 2.
- I execute; I do not ratify.
- **Discipline candidate you may want instead of, or alongside, the § 6 amendment:** *a document's STATUS is an assertion about every clause it contains.* Clause 5 is a doc-lifecycle expression of it; there may be a general form worth a number. Your call — I am not proposing a discipline number, only flagging that the general form exists.

---

## § 5 — The § 7.3 action item assigned to knight-rider (and my answer on the Gate-1 checklist)

§ 7.3 reads:

> *"knight-rider should add a freeze-check item to the dispatch-authoring checklist (Gate 1 review). jack-ryan should add a freeze-check item to the pool-curation Gate 2 review."*

Neither landed. **My answer: do not add it now. It is discharged by supersession, not by fulfilment — and I am recording that rather than quietly dropping it.**

Three reasons, in order of weight:

1. **It would not have worked, and we have the counterfactual.** rocket's X-3 pass **did** check candidates against the freeze list. He checked so carefully that he declined to grade 38 entries rather than risk breaching it. **He still missed `spark`, because `spark` is not on the list.** A Gate-1 item reading "check candidates against the § 7.1 frozen list" would have passed the X-3 dispatch clean. The checklist item was a check against an enumeration, and the enumeration is the thing that leaked.

2. **Adding it now would install, in Gate 1, the defect Gate 1 was just told to flag.** #76's standing effect, ratified this session, is explicit: *"Gate-1 surfaces a bare hand-list with no governing predicate as **WARN** at minimum."* A "check against the seven names" item is a bare hand-list with no governing predicate. It would be a WARN against itself.

3. **§ 7.3's intent is already covered, more completely, by a rule that now exists.** #76's standing effect obliges every brief to *state the predicate first, then any list, labelled illustrative*, and obliges executors to *report derived-vs-named deltas*. Applied to § 7.1 that yields: predicate = *"vocabulary coherent with a frozen substrate must not reach allow-list under a live-substrate slot"*; the seven names are illustration. **That is § 7.3's intent, generalised, binding, and already in force.** § 7.3 asked for the instance; #76 delivered the class.

**Does rocket's mechanical predicate retire the human check?** **Partly — and the split matters.** It retires the *enumeration* half: "who is in the class" becomes a derivation over the live artifact, which is exactly right and exactly what § 7.3's soft-enforcement clause gestured at when it floated a `freeze_list_member` D1 dimension. It does **not** retire the *adjudication* half: the predicate flags `spark`; it cannot rule whether `spark` should stand. That is a vocabulary judgement, it is mine to draft and Matt's to rule, and no predicate will ever produce it. **The machine finds the class; a person rules the member.**

**What I am asking for instead of a checklist item** — one operational hook, at the gating criterion jack-ryan already named:

> **Pre-emission gate:** before any season-emission run, rocket's frozen-substrate-coherence predicate runs and its output is either **empty** or **every flagged entry has a Matt ruling on record.** Not a checklist item to remember; a derivation that runs. Owner: whoever fires the emission run.

**Recorded as discharged:** § 7.3's knight-rider action item — *superseded by Discipline #76 standing effect (2026-08-24)*. § 7.3's jack-ryan Gate-2 item — same disposition, his to confirm.

---

## § 6 — Owed work arising (none of it mine to execute)

| # | Item | Owner |
|---|---|---|
| 1 | Repoint the 15 pre-existing citations to `canonical/reap-die-rise-engine/substrate-expansion-decision-2026-05-17.md`. **Cite by path, not bare filename** — a bare filename is what made the strand invisible. | rocket (engine), KR (collab) |
| 2 | `d3-path-a-archetype-composition-phase-1-p1.md` cites **§ 5.7, which has never existed.** Re-anchor or delete. | rocket |
| 3 | `pool.py:13` comment cites the doc by bare filename; `pool.py:109` error string likewise. Repoint both to the path so the runtime warning names a readable location. | rocket |
| 4 | The `substrate_native` field carries **catalogue-coverage** semantics in `vfx_coverage_manifest.json` and **word-semantics** in `pool.json`. Same name, different referent (Discipline #64). Three entries disagree (`frost`, `mist`, `spark`) and all three are the entries the 2026-06-01 lock re-slotted. Declare the referent at both sites, or rename one. | rocket |
| 5 | Ratify / amend / return § 4's clauses 4, 4a, 5. | **jack-ryan** |
| 5b | **Write the missing decisions-log entry** for the 2026-05-17 substrate-expansion Branch A decision, carrying § 7 as its standing constraint. Cascade step 2 of the doc itself; never executed; the single cheapest durable fix here. | **jack-ryan** |
| 6 | Sweep the remaining 21 homeless code-cited docs under the ratified predicate; adjudicate the 14 unopened. | gandalf, after ratification |
| 7 | `llm/spirit_guide_voice.py` is live code named for a concept retired 2026-06-30, citing a homeless doc. Separate defect. | rocket / star-lord |
| 8 | Two Class-1 live constraints owed a home: `vs2a-vfx-scene-needs.md` L985 (item-label naming rule) and `spatial-data-jsonschema.md` L477 (gauntlet-balance provisionality). | gandalf, with item 6 |

---

## § 7 — What I would keep from this if I kept one line

**A citation is a claim about where truth lives, and an unresolvable citation converts every downstream reader into an author.** rocket, jack-ryan and I did not fail to read § 7 out of haste. We each built a plausible § 7 from the fragments in the files that cited it, and we built three different ones, and all three were wrong — and the two most confident readings were the two furthest from the text. That is what a dangling pointer does in a corpus that reasons: it does not throw an error, it invites invention.

The clean-up is cheap. **The lesson is that the stamp is the load-bearing act** — the eight weeks of drift, the three wrong positions, the deferred grading pass, and the leaked `spark` all descend from one word applied to a document on the basis of its date rather than its content.

---

*gandalf, 2026-08-24. CANON-STEWARD. Companion: `canonical/matt_decision_needed/2026-08-24-spark-vocabulary-ruling.md` (Q63). Restored authority: `canonical/reap-die-rise-engine/substrate-expansion-decision-2026-05-17.md`.*

**Tracker-delta:** new open decision → `current-to-end-state-engine.md` (Q63 `spark` ruling at Matt; § 4 governance clauses at jack-ryan; the 21-doc homeless-citation backlog as owed work).
