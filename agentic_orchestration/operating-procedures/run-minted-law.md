# Run-Minted Law — the F0 harvest

> **STATUS: LAW-CURRENT** — authored 2026-08-10 by gandalf (SPEC-AUTHOR / CANON-STEWARD) as **phase F0**
> of `operating-procedures/software-factory.md` § 9. **jack-ryan ratification queued** per
> `canonical-doc-format.md § 6.7` (gandalf proposes + executes; jack-ryan ratifies process canon).
> **Parents:** `desirable-run-pattern.md` (charter layer) · `software-factory.md` (spine + labor layers).
> **Children:** `gandalf/notes/2026-08-10-factory-spine-spec.md` § 4 (the gate catalogue extends it).

---

## 0 · What this is

The runs minted law. BR-1/BR-2 (baton render), WR1/WR2/WR3 (wave-relay, encounter-geometry,
kite-commit), KC2-SIM (the baton) each ended with rulings that outlive the run that made them —
scattered across charters, ledgers and wind-downs, findable only by whoever was there. **This
document is the harvest:** the durable fraction, lifted out, given stable IDs, and pointed at its
consumer.

Four law-sets, because the runs minted four kinds of rule:

| Part | Law-set | ID | Consumer |
|---|---|---|---|
| **I** | **Godot implementation law** — how a presentation surface must be authored | `GL-n` | drax; gandalf `SCENEWRIGHT`; every scene cell brief |
| **II** | **Factory gate definitions** — the mechanical verdicts, and the law every gate obeys | `FL-n` / `FG-n` | star-lord (spine, F1); every workflow YAML |
| **III** | **Conduct law** — how a run, a cell, and a conductor must behave | `CL-n` | any `RUN-CONDUCTOR`; KR sequencing |
| **IV** | **Eye law** — what must NEVER be compiled | `EL-n` | everyone; the factory's refusal list |

**How to cite:** `GL-3` / `FG-9` / `CL-1`. Each row carries its **lineage** — the run-local rule ID and
the file it was minted in. A law with no lineage is not law here (CL-4).

**Two honesty rules on the harvest itself.** (1) Where a run-local ruling was *generalized* into law,
the row is marked **[gen]** — the generalization is contestable and must be visibly so; it was never
promoted silently. (2) Rules I did not read in this pass are listed in § 5.3 as **NOT-HARVESTED**, with
the reason. The harvest declares its own absences (GL-12), because a law-set that quietly omits is
indistinguishable from one that quietly invents.

---

## PART I · GODOT IMPLEMENTATION LAW

### 1.1 · Substrate → presentation

| ID | Law | Lineage |
|---|---|---|
| **GL-1** | **The pack supplies MATERIAL; the trace supplies GEOMETRY.** How many, at what angle, how fast, how far come from the trace's typed fields (`prong_count`, `spoke_offset_rad`, `projectile_velocity_ms`, `radius_m`, `orientation_rad`, `duration_s`, `stage_count`, `stage_interval_s`, `hit_radius_m`). The asset pack supplies look only. | R-BR-35 (br2 charter:320) |
| **GL-2** | **`duration_s` is LIVENESS; sweep time is TRAVEL — different quantities.** Travel is always derived from velocity and extent, never from `duration_s`. | R-BR-36 (:420) |
| **GL-3** | **Match on `family`, NEVER on `shape`.** `shape` is a drawing hint; `family` is the contract. A consumer branching on `shape` breaks the moment an enum is corrected. | R-BR-40 (:767) |
| **GL-4** | **A projectile is drawn only when the trace carries its travel fields** (`projectile_velocity_ms`, `t_launch_s`). Absent them: muzzle-flash + impact, nothing between. Never invent travel. | R-BR-18 + R-BR-24 (:308), which REVERSED R-BR-3 |
| **GL-5** | **Presentation labour follows the substrate's distribution, not the drama we assumed.** Count an actor's share of the trace's events before authoring for it. | R-BR-47 (:1449); see CL-7 |

### 1.2 · Reading the wire (binding on any baton-v1 consumer)

The KC2 handoff's ten consumer semantics, as law. Each is declared on the wire and defended by a
falsification test in the engine suite (FG-14).

| ID | Law | Lineage |
|---|---|---|
| **GL-6** | **Verify the digest before you load.** A different digest is a different measurement. | KC2 handoff § 1 |
| **GL-7** | **Linear interpolation between path knots IS the position function, not an approximation.** Speed is uniform *within* a leg and never assumed uniform *across* a leg boundary. A 2-knot path is a measured straight walk, not a subsample; a dwell is two knots at one place, two times — draw the wait. | handoff § 3.1–3.3 |
| **GL-8** | **`spawn_tick` is LAST-STILL-TICK.** The body is not on the board until `path[0].run_tick + 1`; **do not hit-test at `path[0]`**. The spawn knot's ≤1-tick `tick`/`t_s` disagreement IS the measured spawn drip — do not snap it to the grid. | handoff § 3.4 |
| **GL-9** | **Read the placement PRIMITIVE from the wire's shape word, never infer it from a magnitude field.** KC2 scatter is a BOX (`placement_extents_m` half-widths); an 8 m circle places 72 of 344 bodies wrong. **[gen]** | handoff § 3.5 |
| **GL-10** | **Use the wire's constant; never re-derive one it carries.** Tick period is the sim's exact float `0.0816326530612245`; a "same" number written differently moves 20 of 344 spawn ticks. | handoff § 3.6 |
| **GL-11** | **`tick` is wave-local; `run_tick` is the global clock.** | handoff § 3.6 |
| **GL-12** | **Absence is DECLARED, not filled.** Where the wire gives no position or timing, render a visible UNDEFINED state and file it — never fabricate (summons carry NO path, R-L53-2). A null under a `NOT_MODELLED` declaration means not-modelled, never "measured zero". Read `provenance.informative_rows` before judging any feel mismatch. | Rider-1 verbatim; handoff § 3.7, 3.9, 3.10 |

### 1.3 · Composition, colour, camera

| ID | Law | Lineage |
|---|---|---|
| **GL-13** | **Telegraph fields clip at the arena's FLOOR-MESH footprint** (not scene collision). This REVERSES the Addendum-7 "draw truthfully, do not clip" ruling. | R-BR-41 (:958) |
| **GL-14** | **Telegraphs dress as their ability, with a legibility floor.** They share material language with the ability that casts them; fill opacity may drop, rim/edge definition may not. The floor is a measured contrast gate, not a taste call. | R-BR-43 (:1002) |
| **GL-15** | **The render distinguishes DAMAGE ARRIVING from DAMAGE ONGOING** — two deliberately unequal channels. Hits: release beat, impact burst, victim flash, hit-react flinch. DoT: none of these; the persistent aura already carries the channel. | R-BR-49 (:1575) |
| **GL-16** | **Colour is judged at WATCH-SCALE camera distance, and a palette ruling states the distance it was sampled at.** The BR-2 boss shell measured 0.7145 red at inspection distance and 0.4172 at watch scale — the same material, two verdicts. A colour approved at inspection distance is unapproved at watch scale. **[gen from R-BR-52]** | R-BR-52 (:1952) |
| **GL-17** | **A visual reference is authority over FRAME, LAYOUT, ORNAMENT and PALETTE. It is NEVER authority over COPY, DATA, or SEMANTICS.** Any cell working from a reference image restates this before it starts, and the copy census re-runs against the shipped surface. (BR-2's reference carried three of the six exact copy needles its census hunted.) | R-BR-54 (:2108) |
| **GL-18** | **Hit-stop is budgeted; the trace clock is INVIOLATE; knockback is forbidden.** Camera impulse rides a second arm so CAM-LOCK stays clean. | R-BR-19, R-BR-20 (br1-exit:125) |
| **GL-19** | **Locomotion from kinematics** (position/heading drive, blend by speed); attack anims keyed to telegraph wind-up + damage emission; death on `alive → false`. Residual foot-slide is named debt, never hidden debt. | R-BR-2 (br1 charter:65) |

---

## PART II · FACTORY GATE DEFINITIONS

### 2.1 · Gate law (binds EVERY gate, v1 and after)

| ID | Law | Lineage |
|---|---|---|
| **FL-1** | **No stub gates, ever.** A gate that cannot execute returns `FAIL / NOT-RUNNABLE` **with reason** — never green. | software-factory § 6; Spec A § 4 |
| **FL-2** | **A gate runs on the ARTIFACT ON DISK** — never on the envelope's word, never on in-memory state. KC2's re-emit re-ran `consume_file()` + `validate_baton_wire()` against the written bytes. | per-landing law (CL-3); KC2 re-emit § 0 |
| **FL-3** | **Every gate ships a falsification test that puts it back to RED.** Strip the declaration, plant the defect — the gate must fail. A gate with no falsification test is a gate nobody has proven can fail. | KC2 ledger L-84(i) |
| **FL-4** | **A threshold is pinned to the substrate it was measured on.** A seed re-pin or corpus re-cut INVALIDATES every threshold derived from it; they are re-measured, not carried. | R-BR-48 (:1510) |
| **FL-5** | **A threshold instrument reports PASS/FAIL only.** Counts below its noise floor may not be compared, ranked, or cited as evidence of anything except "did not pass." | R-BR-39 (:613) |
| **FL-6** | **A presence gate states its noise floor** — same units, **measured at the frames where the verdict is taken**, not asserted at frame 5 and assumed to hold. | R-BR-53 (:2057) |
| **FL-7** | **Only failures travel.** A passing suite never re-enters context; a command runs and its failures alone enter the next prompt. | software-factory § 5 |
| **FL-8** | **Greens are audited, not trusted.** BR-2 shipped two gates that PASSED WHILE FAILING (G-14 presence clauses via the noise floor; G-5d via a soot prefab the burn-shader gate never saw). Both were caught by Matt's eye; neither by a gate. Audit greens. | software-factory § 6; EL-1 |
| **FL-9** | **A red goes green ON EVIDENCE.** No tolerance is moved and no evidence is removed to clear a gate. KC2's last red went green on a digest re-point alone (62 → 63 of 66) — the tolerance never moved. | KC2 ledger L-84 |

### 2.2 · Gate catalogue

`gate(envelope, run) -> GateReport`. **v1** = the six inherited from Spec A § 4. **F0** = the run-minted
extensions this harvest adds. Each row carries the falsification test FL-3 requires.

| ID | Gate | Verdict source | Falsification test | Lineage |
|---|---|---|---|---|
| **FG-1** | `artifacts_exist` | every declared artifact path exists | delete a declared artifact → RED | Spec A § 4 (v1) |
| **FG-2** | `files_non_empty` | no zero-byte deliverables | truncate to 0 bytes → RED | v1 |
| **FG-3** | `json_parses` | declared JSON artifacts parse | append a stray brace → RED | v1 |
| **FG-4** | `diff_matches_claims` | git change-set ⊆ what the envelope claims touched | plant an unclaimed edit → RED | v1 |
| **FG-5** | `verdict_consistent` | a PASS envelope beside a red gate is itself a red | assert PASS with one gate red → RED | v1 |
| **FG-6** | `tests_pass(command)` | exit code is the verdict; **only failures travel** | force one test to fail → RED | v1 + FL-7 |
| **FG-7** | `digest_matches(path, sha256)` | recompute SHA-256 on disk vs the declared digest, **before load and before promotion** | flip one byte → RED. **NOT-RUNNABLE** (never green) if no expected digest is declared | GL-6; KC2 L-82→L-84 |
| **FG-8** | `subprocess_returncode_zero(cmd)` | an instrument's output MAY NOT BE READ until `returncode == 0` is asserted — a silent non-zero exit is indistinguishable from a clean negative | point at a command exiting 1 with plausible stdout → RED | R-BR-38 (:599) |
| **FG-9** | `media_verified(path, expect)` | `ffprobe` duration + stream inventory vs declared expectation. **A re-render writes to a TEMPORARY name and is promoted to the deliverable name only on green** — a partial render must never be able to land on the deliverable path | truncate the render → RED (BR-2's 21.9 s no-audio cut landed on the deliverable and survived only by luck) | R-BR-56 (:2177) |
| **FG-10** | `determinism_asserted(config, layer)` | re-run of an identical config produces identical gate verdicts AND an identical artifact digest; the assertion is **printed**, and the LAYER it covers is recorded | introduce a random seed → RED. **Rider:** a passing assertion is not proof of determinism in a layer it does not cover — BR-2's N3 term (up to 2,305 lit px) passed under an assertion blind to it | R-BR-51 (:1755) + R-BR-53; KC2 L-85 (EXACT ×3, identical digest across a predicate extension) |
| **FG-11** | `noise_floor_declared(gate)` | a presence/threshold gate carries a floor measured at its verdict frames | strip the floor → **NOT-RUNNABLE**, not green | FL-6 / R-BR-53 |
| **FG-12** | `frames_pruned(run)` | a render that was measured deletes its own intermediate frames; a cell that cannot prune SAYS SO | leave frames on disk → RED | R-BR-50 (:1659) |
| **FG-13** | `need_list_complete(source)` | the need list is derived from the artifact's own event vocabulary, not the conductor's recollection — the gate gates the list's COMPLETENESS, not only coverage of it | add an event type to the source → an uncovered need must appear → RED | R-BR-46 (:1270) |
| **FG-14** | `declarations_present(wire, required)` | the consumer-binding declarations are present on the wire | remove the boundary sentence → the six suppressed ticks come back → RED (R-L82-4, exactly this test) | KC2 L-84(f) |
| **FG-15** | `absences_named(artifact)` | every absence is NAMED-ABSENT-DECLARED with a reason; an unexplained null is red | strip a provenance declaration → RED. **NOT-RUNNABLE** if the artifact carries no provenance block | Rider-1; handoff § 3.9 |
| **FG-16** | `evidence_cited(ruling_set)` | every ruling whose validity depends on a field existing carries the census line or probe that confirms it. **Declared limit:** this gate checks the PRESENCE of a citation, never its truth (FL-1 honesty) | strip a citation token → RED | R-BR-34 (:242) |
| **FG-17** | `permissions_fingerprint(phase)` | tree diff before/after; any write outside the phase's `writes` allowlist → rollback the excess + **ABORT the run** (a breach is evidence, never a retry) | plant an out-of-allowlist write → abort | Spec A § 8; D5 |
| **FG-18** | `ceiling_declared(statistic)` | a target-state statistic that can saturate pre-declares the saturation and registers a DISCRIMINATOR beside it | register a saturating statistic with no discriminator → **NOT-RUNNABLE** | WR3 wind-down § 5.2 (P-ACC-A: H1 = 1.0 in all 6,400 fights) |
| **FG-19** | `licence_cleared(assets)` | shipped audio/visual assets resolve to a cleared licence — **restricted audio is restricted in EVERY container** | plant a restricted asset → RED | R-BR-16 (br1-exit:122). **STATUS: REGISTERED, NOT-RUNNABLE** — precondition (an asset licence manifest) does not exist. It reports NOT-RUNNABLE-with-reason until it does; it never reports green (FL-1) |

**Recommended F1 v1 slice** (gandalf lean, veto-open — star-lord's call at build): FG-1…FG-6 (inherited)
+ **FG-7, FG-8, FG-9, FG-10, FG-17**. That is exactly the set the ported baton-scene mechanical cells
need (digest gate · subprocess honesty · ffprobe promotion · determinism · containment), and it matches
Spec A § 11's acceptance list. FG-11…FG-16, FG-18 land as their first consuming workflow appears;
FG-19 lands when its precondition does.

---

## PART III · CONDUCT LAW

| ID | Law | Lineage |
|---|---|---|
| **CL-1** | **THE SPLIT CELL.** When a cell is one small edit plus a render, SPLIT it: a **named** sub-agent makes the edit and commits; the **conductor** runs the render as mechanical execution. Measured: **13 tool calls vs 129–278** for the same deliverable class. Model choice is deliberate — **sonnet, not haiku**: a wrong edit costs a full re-render, which dwarfs the model delta. *Ultra-low spend comes from removing the render from the agent, not from under-powering the judgment.* **In the factory this becomes: the mechanical leg is a SPINE PHASE, not an agent turn.** | R-BR-57 (:2290) |
| **CL-2** | **A cell whose work spans multiple independent items COMMITS AFTER EVERY ITEM**, not at the end. Two agents died on the usage cap with completed work stranded on disk; both recovered only because the conductor went looking. **Recovery-by-luck is not a discipline.** | R-BR-55 (:2156) |
| **CL-3** | **THE PER-LANDING LAW** — *verify artifacts → bank ruling → push → report*, at every landing. Distilled: **"reproduce the number from the artifact, not from the report."** Five consecutive WR3 landings under it caught three premise errors and two falsified attributions at the verify step — **two of them in the conductor's own accepted text.** *The step that audits the conductor is the step that earned the ledger its trust.* | WR3 wind-down § 5.3 + § 6 |
| **CL-4** | **A ruling that names no evidence is a recollection wearing a ruling's clothes.** Any ruling or fallback whose validity depends on a field existing cites the census line or probe that confirms it, **in the ruling itself**. | R-BR-34 (:242) |
| **CL-5** | **A synthesis that unifies two findings must be MEASURED, not inferred.** The elegance of a unification is not evidence for it. | R-BR-45 (:1127) |
| **CL-6** | **A census is valid only for the substrate it was run on.** When a run re-pins its seed or its corpus, every census the decisions rest on is invalidated and re-runs. (KC2's corpus MOVED under the live run — Edition-II → III — and the run re-pinned rather than carried.) | R-BR-48 (:1510); KC2 L-59 / R-KC2-9 |
| **CL-7** | **Count before you author.** Labour allocation follows the substrate's measured distribution, not the assumed drama. | R-BR-47 (:1449) |
| **CL-8** | **Pre-registration lands as its OWN COMMIT, before the battery fires** — so that math-before-code is checkable at Gate-2. All three WR3 math notes landed same-commit as their data, which is why no Gate-2 in that run could check it. | WR3 § 5.1; Discipline #1 clause 1.3 |
| **CL-9** | **Do not move the goalpost after seeing the result.** BR-1's dust/beam coupling measured 76.7 % against a pre-registered ~80 % bar, did not trigger, and the bar did not move. | R-BR-15 (br1-exit:121) |
| **CL-10** | **TRUST-BUT-VERIFY, every hop.** Each hop re-derives the previous hop's numbers from the object. In KC2's endgame the chain caught a defect at **every** hop — including two of the conductor's own (an L-75 misquote and an L-82(h) miscount). | KC2 ledger L-85 |
| **CL-11** | **A contract that constrains a consuming seam is COUNTERSIGNED by that seam.** Objections are named and stand until answered (KC2 OBJ-1 on `path_coverage`); schema changes "named, not taken" wait for the signature rather than landing on assumption. | KC2 handoff § 4 |
| **CL-12** | **A breach is EVIDENCE, not noise.** A permissions breach rolls back and **aborts**; it never retries. | Spec A § 8 |
| **CL-13** | **Restricted audio is restricted in EVERY container.** A licence constraint does not weaken because the asset moved into a working file, a temp render, or a watch cut. | R-BR-16 (br1-exit:122) |

---

## PART IV · EYE LAW — what NEVER compiles

The factory is the stagehand, not the playwright. These are the verdicts it must never claim.

| ID | Law | Lineage |
|---|---|---|
| **EL-1** | **The owner's eye is the instrument of record for "does it read right?"** BR-2 shipped **two gates that passed while failing**; both were caught by Matt, neither by a gate. This is the second independent evidencing of `desirable-run-pattern.md` § 6 obs. 2. | BR wind-down; software-factory § 6 |
| **EL-2** | **IDENTIFY BEFORE YOU REMOVE.** Do not remove a visual element that has not been identified — it may already be measured, and the removal condition may be false. (BR-2: the ring was the boss's icearmor.) | R-BR-42 (:979), R-BR-44 (:1064) |
| **EL-3** | **A HOLD can be right for the wrong reason.** The decision stands; the reasoning is re-derived. Do not let a bad rationale retire a good hold. | R-BR-23 (br1-exit:128) |
| **EL-4** | **Playtest-readiness is a MILESTONE gate at Matt's hands — never an emit gate.** The sim's player model is discarded at the render boundary: **Matt IS the player.** | Rider-1; Q52 ruling § 1.1 |
| **EL-5** | **An instrument at its ceiling cannot see its own failures, and neither can an author reading his own sentence.** Choosing the discriminating statistic that replaces a saturated one is a design judgment, not a gate. | WR3 § 1 + § 6 |

**Corollary (the factory's refusal list).** Workflows that must NOT be compiled: elicitation · design
dialogue · ruling-making · owner-eye judgment. A run that fails the charter's fit test does not get a
spine config — the factory cannot launder an undeserving run into existence.

---

## PART V · REGISTERS

### 5.1 · Reversals — do not resurrect

| Dead rule | Reversed by | What now holds |
|---|---|---|
| **R-BR-3** — "travel is ABSENT from schema; no invented projectiles" | **R-BR-24** | travel IS in schema (`projectile_velocity_ms`, `t_launch_s`) → **GL-4** |
| **Addendum-7** — "draw telegraphs truthfully, do not clip" | **R-BR-41** | telegraph fields clip at the floor-mesh footprint → **GL-13** |
| **KC2 E-3 bound (`modified ≤ 7`)** | **L-35** | the bound was the SPEC's error; measured 8 is right — bound RETIRED |

### 5.2 · Deliberately NOT promoted (and why)

These are real rulings. They are **not law** — they are scene-local, veto-open, or homed elsewhere.
Recorded so a future harvest does not mistake omission for oversight.

- **R-BR-32** (the orb reads `ENERGY`) · **R-BR-33** (the arena is LIVED-IN) · **R-BR-44** (the ring is
  the boss's icearmor, re-registered floor → body) — **scene-content rulings, veto-open by one word.**
- **R-BR-52's numbers** (0.60–0.71 watch-scale red) — the *method* is promoted as GL-16; the numbers
  stay scene-local per FL-4.
- **R-BR-8** (shadow depth 3.50, MATT-SIGNED) and every other Matt-signed constant — these belong to the
  **locked presentation grammar in `current-to-end-state-game.md` PART A**, not to a law harvest.
  Pointed at, never copied (twin-drift hazard).
- **All measured tolerances** (nova 22.5° ± 0.5°, extent 12.0 m ± 0.2 m, wave 16.0 × 6.0 m ± 0.3 m,
  presence bars ≥ 90 %, legibility 80 %, pixel harvest ≥ 500 px, noise floors ~500 px / ~2,305 px) —
  seed- and asset-pinned per **FL-4**. They live in their gate definitions; re-measured on any re-pin.

### 5.3 · NOT-HARVESTED — declared, not missing

Read this before assuming a rule is absent because it was judged unimportant. These were **not read in
this pass**; a later harvest lap closes them.

- **R-BR-5, 6, 9, 13, 17, 21, 22** and **R-BR-25 … R-BR-31** — BR-1 rulings living in Scopes 40–43 and
  the exit review. **R-BR-17 (the "three-layer VFX law") is the most likely law-bearing item here** and
  is deliberately NOT restated from recollection (CL-4).
- **R-WR1-\* / R-WR2-\*** ledgers — WR3's were harvested via its wind-down; WR1/WR2 charters were not
  walked. Their per-landing and banking practice is already generalized as CL-3.
- **R-KC2-1 … R-KC2-13 and the 85-row KC2 ledger's in-run rulings** — harvested via the handoff, the
  emit record and L-84/L-85 only. Run-local mechanism rulings (eHP chain, level law, count model) are
  **engine substrate findings, not law**, and correctly stay in the ledger.

---

## PART VI · CONSUMERS AND OPEN ITEMS

**Who reads what:** star-lord → Part II (the FG catalogue extends Spec A § 4; the recommended v1 slice
is in § 2.2). drax → Part I (+ CL-11: two countersigns are still yours). Any `RUN-CONDUCTOR` → Part III.
Everyone → Part IV. KR → § 2.2's v1 slice when sequencing the spine wave.

**Open items (ARCHITECT table — resolve or surface, do not silently default):**

| # | Item | Disposition |
|---|---|---|
| **O1** | Which FG land in F1 v1 | gandalf lean recorded in § 2.2 (FG-1…6 + 7/8/9/10/17), **veto-open**; star-lord rules at build and records the ruling |
| **O2** | Should Part I be mirrored into `reincarnated-godot/` for build-side proximity? | **Lean NO — pointer only.** The OP↔skill twin-drift case (2026-07-21, ~6 weeks stale) is the precedent; one home, many readers |
| **O3** | FG-19's precondition (an asset licence manifest) | UNOWNED. Surfaces to drax/KR when an audio-bearing surface next ships; gate reports NOT-RUNNABLE until then |
| **O4** | Ratification | **jack-ryan**, per `canonical-doc-format.md § 6.7`, riding the same sitting as the software-factory strategy doc + the desirable-run-pattern amendments (R-BR-57 → § 6; § 6 obs. 2 now twice-evidenced) |
| **O5** | F4 memory loop | This document is F4's **first law-diff target**: receipts → harvest → law-diff → config recompile. F4 amends here rather than starting a second register |

**Signed:** gandalf, 2026-08-10. The runs already knew these things; until now only the people who were
there did.
