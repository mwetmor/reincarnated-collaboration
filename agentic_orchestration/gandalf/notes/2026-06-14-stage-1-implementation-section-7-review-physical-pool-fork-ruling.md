# §7-review ruling — Stage-1 IMPLEMENTATION gate (BC-coordinate cutover) — VERDICT: PASS-WITH-AMENDMENTS · physical fork = (a) for the cut + (b) deferred to a content-add sub-stage with Matt authorization

**Type:** design-contract implementation-review ruling (gandalf seam) — the design half of the implementation gate on Stage 1 of the BC-coordinate-identity cutover program. jack-ryan runs the analytical Gate-2 (DEV-MODE, BLOCK authority) in parallel.
**Date:** 2026-06-14
**Author:** gandalf
**Authority:** the §7 design contract this implements is Matt-authorized (`2026-06-14-class-generator-bc-target-cutover-ruling.md` §7). The math-note review (`2026-06-14-stage-1-unit-1-math-note-section-7-review-ruling.md`, `ee4f785`) is the predecessor gate; this is its implementation successor.
**Reviews:** implementation tag `rocket/v1.0-bc-coordinate-cutover-stage-1` @ `19b27f3` (amendment fold `c610ae6`, NOT pushed). New: `generation/bc_target_source.py` + `composed_kit_adapter.py`; modified `class_generator.py`, `class_schema.py`, `season_orchestrator.py`; `MIGRATION.md` amended.
**Empirical grounding (do-not-rule-blind discharged):** gandalf verified at source 2026-06-14 — the without-replacement draw `sample_mechanics` (`bc_target_composer.py:498-517`, `n_to_draw = min(count, len(pool))`); the physical primary-pool population (rage=4 / focus=4 / combo=2 / stamina=2 PRIMARY non-CC-non-movement; max-reachable kit_size = total cost-type pool = 8/6/4/2 vs legacy 10-13); `ELEMENT_SCALING_ATTRIBUTE` IS element-shaped (`element_biases.py:28-38`); the stat-allocation site keys on the kit's OWN `skills[0].scaling_attribute` (`class_generator.py:452`), not a fresh element lookup; the `PhysicalPoolInfeasibleError` STOP-AND-ESCALATE path (`composed_kit_adapter.py:85-117`, `class_generator.py:615-668`).

---

## 0. VERDICT — PASS-WITH-AMENDMENTS

The implementation is a **faithful, source-grounded realization of the §7 contract and the four math-note rulings.** It cuts the elemental path cleanly (16/21 coordinates compose behavior-preservingly), it honors the loud-fail discipline exactly where I demanded it, and — most importantly — **rocket hit a genuine structural infeasibility on the 5 physical coordinates and STOPPED instead of shipping a degraded kit.** That is the gate behaving precisely as designed. R4's whole purpose was to make "a kit cannot form" a loud, principled, escalated event rather than a silent 5-skill fallback (the water_mage 1/29 original sin in a new form). Rocket raised `PhysicalPoolInfeasibleError`, did not infinite-loop a re-draw, did not degrade — and escalated to me. This is the discipline working.

It is **PASS-WITH-AMENDMENTS, not PASS,** because the physical fork requires my explicit ruling (below) and two documentation conditions must be folded before Stage-1-partial tags. It is **not BLOCK** because nothing in the elemental cut violates the §7 contract, the lock, #13a, or the one-variable discipline — and the physical infeasibility is correctly surfaced, not buried.

---

## 1. THE PHYSICAL-POOL FORK — RULING: (a) FOR THE CUT, (b) DEFERRED to a content-add sub-stage with Matt authorization. SHIP the elemental 16/21 cut NOW as Stage-1-partial.

This is the ruling rocket correctly escalated against my own R1+R3 conditions. I split it cleanly:

### 1.1 For Stage 1 (the architectural cut): (a). The coordinate composes what the pool allows; the physical pool is simply too sparse to compose ANY behavior-preserving kit — so for physical, (a) cannot apply either.

I need to be precise, because the fork as posed is not symmetric across the two physical sub-cases.

**The empirical fact I verified at source:** `sample_mechanics` is a draw **WITHOUT replacement** (`n_to_draw = min(count, len(pool))`, `bc_target_composer.py:515`). The physical primary pools are 4 rage / 4 focus / 2 combo / 2 stamina (non-CC, non-movement), and the total cost-type pools (primary + CC + mobility) are 8 / 6 / 4 / 2. A physical coordinate targeting kit_size 10-14 is **hard-capped at the pool size** — it CANNOT reach 10. The legacy b6 builder drew physical kits from the **grammar** (unbounded generation), not this finite cost-filtered pool; that is why legacy hunter/rogue = 13 while compose_kit reaches 2-5. **This is not a re-drawable off-pick** (the pool is identical every draw; the coordinate is deterministic). It is a genuine pool-population infeasibility.

So the fork's option (a) — "accept a smaller physical kit band as behavior-preservation" — **fails on the merits for physical**, and I reject it, for two reasons:

1. **A 2-5-skill physical kit is not "a smaller band." It IS the water_mage 1/29 degraded kit, structurally identical.** The whole architectural acceptance proof of this program is that the `KitConstraintError → pre-B6 5-skill fallback` path is STRUCTURALLY REMOVED — the disease was a degraded 5-skill kit nobody noticed. Accepting a 2-5-skill physical kit as "behavior-preservation" would re-import the exact pathology the cut exists to delete, dressed as a design choice. A hunter that fires 4 skills where the legacy hunter fired 13 is not a smaller-band hunter; it is a broken hunter. The player would feel a martial class with a third of its kit missing — sparse rotation, dead air, no tier-4 capstone. That is not behavior-preservation; it is behavior-destruction.

2. **It violates the one-variable discipline in the worst direction.** Stage 1's contract is "change ONLY the pipe; behavior-preserving." A physical kit dropping from 13 to 4 skills is not a pipe change — it is a massive behavioral regression bundled into the architectural cut, the precise cert-wave attribution error the program guards against (you could never tell whether a later physical balance regression came from the pipe-change or the kit-size collapse).

**Therefore for the elemental 16/21 — option (a) is the ruling, cleanly:** the mana pool (51 mechanics) composes kit_size 10-14 without strain; the coordinate composes what the pool allows AND what the pool allows IS the behavior-preserving band. The smoke confirms it (water_mage kit_size 12-13, the 1/29 dissolved). Elemental (a) holds.

**For the 5 physical coordinates — neither (a) nor a same-stage fix is legitimate.** The pool cannot compose a behavior-preserving physical kit at all. That routes to (b).

### 1.2 For physical: (b) EXPAND the physical mechanic pool — a behavior-CHANGING content add, OUTSIDE rocket's Stage-1 seam authority, requires its own gate AND Matt authorization (new scope).

I rule **(b) explicitly, and I state explicitly: this requires Matt authorization.** Expanding the physical mechanic pool from ~4-rage/4-focus/2-combo PRIMARY mechanics to a population that can compose a 10-13-skill physical kit is **net-new content** — new mechanic definitions in `unified_mechanic_pool.yaml`, each with geometry/range/cost/cd/cc/bc-axis-hints, each a design artifact that the cohesion of the martial classes depends on. That is:

- **Behavior-CHANGING** — it adds mechanics that did not exist; physical kits composed from an expanded pool will not be bit-identical to legacy b6 physical kits (which were grammar-drawn). This is by definition outside the one-variable "behavior-preserving" Stage-1 envelope.
- **Outside rocket's seam authority** — adding content to the substrate pool is not a pipe re-point; it is a content-authoring decision with thematic and balance weight (what does a rage mechanic feel like? how many? what geometry distribution? does the martial fantasy hold?). That is a design call routed THROUGH me and authorized by Matt, then executed by rocket against a fresh spec — not folded into a cutover.
- **A separate gate** — the expanded pool needs its own math note (pool-population target sizing per cost-type, against the legacy physical kit_size band and the role/CC floor constraints), its own gandalf design review (martial-fantasy coherence of the new mechanics), and its own jack-ryan Gate-2.

### 1.3 SHIP the elemental 16/21 cut NOW as Stage-1-partial; physical deferred to a content-add sub-stage. The whole stage does NOT hold.

This is the sequencing half of the fork ruling, and I rule **ship the elemental cut now.** Reasoning:

1. **The elemental cut is independently complete and independently valuable.** 16/21 coordinates compose behavior-preservingly; the water_mage 1/29 — the landmine that triggered this entire program — DISSOLVES in the elemental cut. The form-bias root at the generation head is retired for the elemental classes (the overwhelming majority of the class space). Holding all of that hostage to the physical pool-expansion gives up a complete, ratified architectural win to wait on a content-authoring effort that is genuinely separate scope.

2. **The physical defer does not corrupt the elemental cut — the loud-fail guarantees it.** Because physical coordinates raise `PhysicalPoolInfeasibleError` (STOP-AND-ESCALATE), there is no path by which a physical coordinate silently produces a degraded kit in a shipped Stage-1-partial. A physical coordinate, encountered, halts loudly. The Stage-1-partial season must therefore **route physical coordinates through the legacy b6 path** for now (the b6 machinery STAYS RESIDENT until Stage 3 — MIGRATION.md:61-62 confirms it is not deleted), OR the season generator must not emit physical coordinates into the coordinate path until the pool-expansion sub-stage lands. Either is clean; **the discipline guard I add is: the Stage-1-partial must make the physical→legacy-path routing EXPLICIT and loud-logged, not an implicit fall-through** — so it is impossible to mistake "physical still on the legacy path" for "physical migrated." (See Condition C-3.)

3. **This is the W-E → W-F gated prove-then-proceed pattern applied at the seam.** We prove the elemental coordinate path load-bearing-complete (16/21 + the A3 gate when gamora's sim runs), ship it, and the physical pool-expansion becomes a named, Matt-authorized content sub-stage that, once landed, brings the final 5 coordinates onto the coordinate path. Generation-first (elemental), then the physical content-add, then Stage 2 (gamora sim AI), then Stage 3 (deletion). The physical sub-stage slots between Stage-1-elemental and Stage-2, OR runs in parallel with Stage-2 since they touch different seams — KR sequences.

**Naming the deferred item precisely (recognition → validate → commit):** the physical-pool-expansion sub-stage is RECOGNIZED now (the pool is structurally too sparse). The COMMIT (authoring the new mechanics) is gated on (a) Matt authorization of the new content scope and (b) a gandalf design spec sizing the pool-population target per cost-type against the legacy physical kit_size band + the role/CC floors. The empirical criterion that proves the sub-stage complete: a physical coordinate composes kit_size ≥ 10 through `compose_kit` and the A3 gate passes for the 5 physical default-coordinates. Until then, physical rides the legacy path under explicit loud-logged routing.

### 1.4 Why (b)-with-defer is the only ruling consistent with the program's own discipline

The temptation is (a)-accept-smaller, because it "keeps Stage 1 a pure pipe-change, no content add." But that temptation is exactly the form-bias habit wearing a new mask: it would normalize a degraded martial kit as acceptable output, the way the legacy 5-skill fallback normalized the water_mage degradation for 29 seasons. The genre lesson is the same one D2's class design taught — a Barbarian (martial) with a thin skill kit feels hollow in a way a thin caster does not, because the martial fantasy IS the rotation density and the weapon-tempo. Diablo III's launch-era melee classes felt anemic precisely when their resource-and-cooldown rhythm was too sparse. A 4-skill rage "warrior" is that failure. We do not ship it; we author the pool that makes the martial fantasy whole, under its own gate, when Matt authorizes the scope.

---

## 2. RULING-2 PREMISE CORRECTION — CONFIRMED. Rocket's resolution honors #13a; the substrate rides in via the kit's OWN resolved property, not a fresh element coupling.

My math-note Ruling 2 asserted "stats are substrate-blind for elemental archetypes — the per-archetype distributions are role/defense-shaped, not element-shaped, and binding element into stats would be a NEW coupling." **Rocket found this empirically incorrect, and rocket is right.** I verified at source: `ELEMENT_SCALING_ATTRIBUTE` (`element_biases.py:28-38`) IS element-shaped — fire/water/lightning/shadow → intelligence; earth/wind/holy → wisdom; physical → strength. And the simulator scales damage by `skill.scaling_attribute = ELEMENT_SCALING_ATTRIBUTE[element]` (`damage_resolver.py:308`). So legacy stat distributions ARE element-shaped, and a stat allocator that ignored the element would silently undercount damage at the simulator. My premise was wrong; the collision I anticipated in the math-note Ruling 2 ("if two archetypes share (role, def_bin) but had different distributions, key on a third dimension") was real, but the third disambiguator is the caster-attribute, not energy_type.

**Rocket's resolution CONFIRMED as #13a-honoring.** `allocate_stats_from_coordinate(role, bc_target, scaling_attribute, rng)` keys the SHAPE on `(role, def_bin)` and takes the PRIMARY ATTRIBUTE IDENTITY from `scaling_attribute` — and critically, `scaling_attribute` is read at the call site as `skills[0].scaling_attribute` (`class_generator.py:452`), i.e. **the kit's OWN already-resolved property**, set upstream during skill composition. It is NOT a fresh `ELEMENT_SCALING_ATTRIBUTE[element]` lookup re-introduced at the stat-allocation seam.

This is the #13a-correct shape, and here is why precisely:

1. **#13a forbids a fresh substrate coupling, not the substrate's downstream consequences.** The partition keeps `compose_kit` substrate-BLIND (the coordinate is pure mechanics). The substrate binds ONCE, provisionally, in the adapter (`canonical_element ← dominant_element`, §7.3). Everything downstream that needs element — the simulator's damage scaling, the skill's scaling_attribute, and now the stat allocation — reads the substrate from the kit's OWN resolved property, riding the single binding. The stat allocator reading `skills[0].scaling_attribute` is reading the consequence of the ONE adapter binding, not opening a SECOND channel to `ELEMENT_SCALING_ATTRIBUTE`. There is one substrate entry point; stats follow it for consistency, they do not re-derive it.

2. **The alternative — a label-keyed or element-relookup allocator — IS the disease.** If the allocator did `ELEMENT_SCALING_ATTRIBUTE[dominant_element]` itself, that would be a parallel substrate coupling at a second site, and worse, it would be the kind of element-keyed lookup the program is retiring. Reading the kit's resolved `scaling_attribute` is the substrate-led-discipline-correct move: the kit's resolved property votes; the allocator consumes the vote.

3. **It is behavior-preserving by construction AND simulator-consistent.** Because the primary attribute is the kit's own scaling_attribute, the stat allocation aligns with exactly the attribute the simulator scales damage by — so a fire kit (INT-primary scaling_attribute) gets INT-primary stats and the simulator finds the stats it expects. No silent damage undercount. The legacy element-shaped distribution is reproduced through the kit's own property, not a re-coupling.

**One amendment condition (C-1):** this finding is currently documented only in the adapter code comment (`composed_kit_adapter.py:195-209`). It corrects a premise in my OWN ratified math-note ruling — that is a load-bearing correction that must not live only in a code comment. **MIGRATION.md must NAME it** as a third documented Stage-1 finding ("Ruling-2 premise correction — legacy stats ARE element-shaped; resolved behavior-preservingly via the kit's own scaling_attribute, single substrate binding preserved, #13a honored"), so the correction to a ratified ruling is auditable at the program level, not buried. This is the rep-audit-at-the-semantic-layer discipline (OP §4.4): the substrate rides in correctly at the mechanical layer, and the design-level record must say so explicitly.

---

## 3. CONFIRMATIONS — mono-element delta NAMED; loud-fail HONORED

### 3.1 Mono-element behavioral delta — NAMED in MIGRATION.md. CONFIRMED.

MIGRATION.md:40-46 ("NAMED behavioral delta #1 — mono-element Stage-1") names it explicitly, cites the Ruling-4 condition, identifies the source (legacy multi-element came from the separate `STAT_ELEMENT_POOLS` hybrid-promotion pipeline surface, NOT `compose_kit`), and flags hybrid re-introduction as Phase-5/diversification scope. This satisfies my math-note Ruling 4 condition ("must be NAMED in MIGRATION.md, not buried"). The tier/chain topology delta is also named (delta #2, MIGRATION.md:48-54) with the A3 backstop cited. Both honest deltas are documented. CONFIRMED.

### 3.2 LOUD-FAIL infeasibility — HONORED, exactly as R4 demanded. CONFIRMED.

I verified the full infeasibility-handling path at source:

- `PhysicalPoolInfeasibleError` (`composed_kit_adapter.py:85-117`) is a STOP-AND-ESCALATE — no degraded kit, the docstring explicitly states "rocket STOPS and escalates rather than shipping a degraded physical kit (which would re-create the water_mage 1/29 sin in a new form) or infinite-looping a re-draw."
- `DegradedKitError` (`composed_kit_adapter.py:57-78`) catches the mana-pool cost_type off-pick degradation (kit below `KIT_SIZE_FLOOR=10`) and surfaces it loudly with the failed bc_target + (role,range,energy,element) at season-summary-visible severity — exactly my math-note Ruling 4 fold-in obligation #6.
- The orchestrator loop (`class_generator.py:615-668`) routes physical infeasibility to `PhysicalPoolInfeasibleError` (not re-drawable — the pool is identical every draw), routes mana off-picks to a BOUNDED re-draw (cap 12), and on cap-exhaustion for a non-physical coordinate raises a loud `RuntimeError` ("a coordinate that should compose clean did not; investigation trigger; do not silently degrade"). No silent degradation, no unbounded re-draw, no 5-skill fallback. The `KitConstraintError → 5-skill fallback` is structurally removed (`_generate_skills` DELETED — MIGRATION.md:58, A-3.1 PASS).

This is the loud-fail discipline realized precisely. CONFIRMED.

---

## 4. THE FOLD-IN CONDITIONS (what PASS-WITH-AMENDMENTS obligates before Stage-1-partial tags)

- **C-1 (Ruling-2 finding to MIGRATION.md):** add a third named finding to the MIGRATION.md Stage-1 entry recording the Ruling-2 premise correction (legacy stats ARE element-shaped; resolved via the kit's own `scaling_attribute`, single substrate binding, #13a preserved). It corrects a premise in a ratified gandalf ruling and must be auditable at the program level, not only in a code comment.
- **C-2 (physical fork ruling to MIGRATION.md):** update the MIGRATION.md "BLOCKING FINDING" block to record THIS ruling: physical = fork-(b), pool-expansion is a Matt-authorized content-add sub-stage (separate gate + gandalf design spec + jack-ryan Gate-2); the elemental 16/21 ships as **Stage-1-partial**; physical rides the legacy b6 path under explicit loud-logged routing until the sub-stage lands. Re-stamp the Status line from "PARTIAL — physical kits ESCALATED" to "PARTIAL — physical DEFERRED to Matt-authorized pool-expansion sub-stage (gandalf ruling 2026-06-14)."
- **C-3 (explicit physical→legacy routing guard):** the Stage-1-partial season generator must make physical-coordinate routing to the legacy path EXPLICIT and loud-logged — not an implicit fall-through. A physical coordinate must be visibly logged as "routed to legacy b6 path pending pool-expansion sub-stage," so "physical still legacy" can never be mistaken for "physical migrated." (If the chosen Stage-1-partial mechanism is instead "the orchestrator does not emit physical coordinates into the coordinate path yet," that is equally acceptable and equally must be explicit.)

None of C-1/C-2/C-3 re-open a design problem; they record the rulings made here. They are documentation + routing-explicitness conditions, not re-design.

---

## 5. WHAT I CHECKED FOR AND DID NOT FIND (the BLOCK conditions that would have stopped this)

- No silent degraded physical kit — `PhysicalPoolInfeasibleError` STOP-AND-ESCALATE; rocket halted and escalated rather than shipping a 4-skill warrior.
- No re-introduced element coupling at the stat allocator — `scaling_attribute` is the kit's own resolved property, single substrate binding (#13a intact).
- No label smuggled as a runtime key — the source (`bc_target_source.py`) is a pure binning function of the four inputs; the legacy-format label is OUTPUT-only (the bridge, dies Stage-3).
- No diversification bundled in — zero off-legacy coordinate sampling; the element nudges are TRANSITIONAL(Phase-5)-marked and refine 1-2 axes only.
- No unbounded re-draw, no infinite loop — re-draw is capped (12); physical sparsity is correctly identified as not-re-drawable.
- No undocumented behavioral delta — both deltas (mono-element, tier/chain) NAMED in MIGRATION.md; the Ruling-2 finding is in code-comment and routed to MIGRATION.md via C-1.

---

## 6. DISPOSITION

- **VERDICT: PASS-WITH-AMENDMENTS.** The elemental cut is contract-conformant and behavior-preserving for 16/21 coordinates; the physical escalation is correctly surfaced and loud-failed; the four math-note rulings are faithfully implemented; the Ruling-2 premise correction honors #13a.
- **PHYSICAL FORK RULING: (a) for the elemental cut · (b) for physical, DEFERRED to a Matt-authorized content-add sub-stage.** A 2-5-skill physical kit is the water_mage 1/29 degradation in a new form, not a "smaller band" — rejected. The physical pool-expansion is behavior-CHANGING net-new content outside rocket's Stage-1 seam authority; it requires Matt authorization, its own math note, a gandalf design spec (martial-fantasy coherence + pool-population sizing), and jack-ryan Gate-2.
- **SHIP DECISION: the elemental 16/21 cut ships as Stage-1-PARTIAL NOW;** the whole stage does NOT hold. Physical rides the legacy b6 path under explicit loud-logged routing (C-3) until the pool-expansion sub-stage lands. The loud-fail guarantees no physical-coordinate corruption in the shipped partial.
- **RULING-2 PREMISE CORRECTION: CONFIRMED #13a-honoring.** My math-note premise was empirically wrong (legacy stats ARE element-shaped); rocket's resolution rides the single adapter substrate binding via the kit's own resolved `scaling_attribute`, not a fresh element lookup. Routed to MIGRATION.md via C-1.
- **MONO-ELEMENT DELTA: NAMED (MIGRATION.md:40-46). LOUD-FAIL: HONORED (PhysicalPoolInfeasibleError + DegradedKitError + bounded-cap loud RuntimeError).** Both CONFIRMED.
- **The elemental cut MAY proceed toward Stage 2 once (a) C-1/C-2/C-3 are folded AND (b) jack-ryan's parallel Gate-2 clears.** Both gate-halves must pass — this is the design half; jack-ryan's analytical half (including the A3 gate disposition + the 3 `test_role_orientation` test-contract deltas, which are HIS lane) is independent and concurrent. The A3 calibration gate (OPEN, gamora-sim-dependent) is the named empirical criterion gating the elemental cut's full validation; it does not block the Stage-1-partial tag but must be run before the elemental cut is declared load-bearing-complete.
- **The deferred physical sub-stage** is registered now; its commit is gated on Matt authorization of the content scope + a gandalf pool-sizing design spec; its completion criterion is a physical coordinate composing kit_size ≥ 10 through `compose_kit` with the 5 physical default-coordinates passing A3.

---

**Signed:** gandalf, 2026-06-14
**For:** the §7-review of the Stage-1 IMPLEMENTATION — the design half of the implementation gate; verdict PASS-WITH-AMENDMENTS; the physical-pool fork ruled (a)-for-elemental + (b)-deferred-to-a-Matt-authorized-content-add-sub-stage with the elemental 16/21 shipping as Stage-1-partial NOW; the Ruling-2 premise correction confirmed #13a-honoring (substrate rides the single adapter binding via the kit's own resolved scaling_attribute); mono-element delta named + loud-fail honored; the elemental cut proceeds toward Stage 2 once C-1/C-2/C-3 fold and jack-ryan's Gate-2 clears.
