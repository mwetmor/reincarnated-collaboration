# Commission — gandalf — Form-bias cadence: strategy through the ARPG ↔ Isekai axis

**From:** knight-rider (relaying Matt's framing verbatim where indicated)
**To:** gandalf (story + game-design steward — Tier A)
**Approved by:** Matt at 2026-05-16 (Day 4 open)
**Status:** PENDING — active, sequenced after current canonical-story work if any is in flight
**Type:** Knight-rider commission to gandalf for design-canonical authoring
**Direction:** knight-rider → gandalf
**Output:** `canonical/story/form-bias-cadence-strategy.md` (new canonical-story doc) + any decisions-log drafts it produces

## Why this exists — Matt's framing (verbatim)

Matt's 2026-05-16 framing of the question this commission asks you to think through. Treat the language here as the brief, not as restatement:

> "This is an open documented action item to catalogue and analyze the impact of all labels and associated logic within the engine which are prior to the last LLM API call with the goal to understand their implication on embodiment (humanoid/other).
>
> And when combining the elements concept with embodiment, the essential question becomes: how does the inherent bias coded into the labels + associated logic's of the elements and all other pre-LLM API finality skew the engine's thematic seasonal story and class/archetype convergence?
>
> And even more importantly: how does this skew match to ARPG canon? How does it match to Isekai canon? What is the appropriate push/pull between the two? How do we decide where to land?"

This is **the** generative-side design question on the table right now. Knight-rider has been treating form-bias resolution as the file-37 / Option I/II/III cadence problem; Matt's reframing pulls back further — *before* deciding cadence, the question is whether the project should land closer to ARPG-canonical form (which favors humanoid bias as a feature, since the genre's expectations and player vocabulary assume it) or closer to Isekai-canonical form (which favors radical embodiment variance as a feature, since the genre's narrative beats turn on reincarnation-as-non-self).

You are uniquely positioned for this because:
- You sit at the **generative-side design steward** seam (Tier A, parallel-escalation privilege).
- You have **Legolas's five-pass research base** already filed (isekai evolution; Diablo; PoE; ARPG community; adjacent ARPGs) — the empirical grounding for ARPG/Isekai canon characterization.
- You authored the locked **HD-2D-shaped pixel-art style register**, the **Court of Forms** structural framing, the **naming triad**, and the **enemy visual legibility** spec — all of which encode latent assumptions about embodiment that this commission must surface and re-examine.

## What this commission asks for

A canonical-story doc at `canonical/story/form-bias-cadence-strategy.md` that addresses the four nested questions Matt named. Roughly 4-6 pages — this is a design-strategy document with stakes, not a single position-lock.

### Question 1 — Inventory: what carries the bias?

Catalogue and analyze the impact of all labels and associated logic in the engine that exist *prior to the last LLM API call* and that carry embodiment implication (humanoid vs other).

The catalogue work is partial — file 37 § 2 lists a starting inventory, and the action item Matt named has been deferred (no rocket sweep dispatch yet). **You can either:**

- **(a)** Treat the file-37 § 2 list as the working inventory and proceed to analysis on it, flagging completeness as a known limitation. Recommend a rocket-led generation-internals sweep as a follow-on dispatch if you want broader grounding.
- **(b)** Invoke rocket as Pattern A subagent (or schedule Pattern B) to produce the comprehensive pre-LLM label/logic inventory before you analyze. Rocket owns the generation/element/anchor/foundation seam and knows what labels/logic enter the LLM prompt-construction code. Direct-dialogue privilege applies — coordinate timing directly.

Either path is acceptable. Document which you chose and why.

**The inventory should at minimum cover, per Matt's framing:**
- **Element labels** — the canonical four (fire/water/earth/wind) and the D1 element-name pool (156 entries; allow-list / eligible / quarantine tiers)
- **Class archetype labels** — warrior/mage/rogue/hunter and any sub-archetypes
- **Gear slot labels** — weapon / armor / accessory + display-side sub-slots (head/chest/main/off/neck/ring1/ring2)
- **Attribute axes** — STR / DEX / INT / WIS / VIT (math-bearing, per the 2026-05-09 decisions-log entry — these are not just labels but flow into `can_equip()` and `stat_requirements`)
- **Role orientation taxonomy** — damage / support / control / hybrid (per the 2026-05-08 Phase 2 decision)
- **Geometry palette labels** — the 16-type active palette + the labels themselves (lance / cone / arc / etc. — file-37 flags these as carrying humanoid weapon-semantic gravity)
- **Wields / wears / weapon / armor / accessory categorical axes** — per Matt's file-37 § 1 origin statement
- **Spirit Guide kit-composition framing** — "kit of skills," not "body-with-properties"
- **The skill verb grammar in the seed taxonomy** that the LLM expands on
- **The naming triad mechanics** — anchor → spirit name → embodiment-flavored name (you authored this; surface what the triad presupposes about form)
- **The trait architecture** — per-class intrinsic trait pool + gear-affix rolls (per the 2026-05-12 trait architecture decision)

The output of this question is a structured inventory — possibly a table — with a column per item naming the embodiment implication (humanoid-presupposing / form-agnostic-but-named-humanoid / form-agnostic). This is the **substrate** the next questions analyze.

### Question 2 — Skew analysis: how does combining elements + embodiment skew the engine?

When you combine the element labels + their associated logic with the embodiment-implicating labels from Q1, the engine's thematic seasonal story and class/archetype convergence carry a *skew*. Characterize the skew.

Specific dimensions to analyze:
- **Thematic seasonal story skew.** When the engine generates a season around a chosen element + chosen anchor + chosen class composition, the seasonal narrative the LLM produces is constrained by what those labels can structurally express. A fire-themed season with humanoid-presupposing class labels produces a *certain kind* of fire season (knight, mage, rogue against humanoid demons in volcanic landscapes). What seasons can it NOT produce? What latent embodiment intent (per file 37 § 1) is structurally suppressed?
- **Class / archetype convergence skew.** Across seasons, archetypes converge on humanoid-mappable shapes. The B14.5 sidecar analyses (memory `project_b14_5_sidecar_analyses.md`) showed hunter has the highest modifier-range (1.82) — the least consistent archetype across seeds. Is this connected to embodiment skew? Does the convergence framework systematically punish embodiment-divergent classes because the simulation models them against humanoid-shaped pack/elite/boss content (per Position C in file 37)?
- **Element selection bias.** The same sidecar finding showed fire over-represented at 23.6% vs the 20% expected uniform rate. Is this a generation-side selection bias, or does it reflect that fire-themed seasons compose more cleanly against humanoid embodiment than (e.g.) earth-themed or wind-themed seasons?
- **The PackProxy precedent.** PackProxy (B10.2 ship) is the codebase's existing non-humanoid composite entity — a precedent the engine *can* hold non-humanoid composition. Does this argue for or against the skew being structurally inherent vs implementation-default?

The output of this question is a **named-skew description** — pattern-language that the rest of the team can use when discussing form-bias work going forward. Be specific and concrete.

### Question 3 — Canon match: how does this skew compare to ARPG canon and Isekai canon?

This is the central question. Two parallel analyses:

**Q3a — ARPG canon match.**
Draw on Legolas Pass 2 (Diablo retrospectives), Pass 3 (PoE design philosophy), Pass 4 (ARPG community discourse), Pass 5 (Last Epoch / Grim Dawn).

- What is ARPG canon's relationship to embodiment? Is humanoid form a feature of the genre or an implementation default that the genre never had to question? (Diablo's heroes have always been humanoid; PoE classes are all humanoid; Last Epoch's masteries are humanoid sub-archetypes.) Is this load-bearing for the player vocabulary the genre depends on (gear, slots, attributes, build identity)?
- What does ARPG canon say about element design? The PoE elemental triad (fire/cold/lightning) plus chaos plus physical is the modern reference. Diablo 4 has fire/cold/lightning/poison/shadow/physical. Does this canonical structure presuppose embodiment patterns?
- Where does the engine's *current* skew sit relative to ARPG canon? Is it *more* humanoid-presupposing than canonical ARPGs (which would be a problem — over-shooting genre conventions), *aligned* with them (which would be fine for the ARPG-side audience), or *less* humanoid-presupposing in ways that read as inexplicable to ARPG-aware players?

**Q3b — Isekai canon match.**
Draw on Legolas Pass 1 (isekai evolution).

- What is Isekai canon's relationship to embodiment? The genre's defining narrative beat is *reincarnation-as-not-self*. Isekai protagonists are often non-humanoid (Slime, Spider, Sword, Vending Machine, etc.) — the genre's player/reader vocabulary explicitly includes radical embodiment variance.
- What does Isekai canon say about elements / mechanics? Isekai stories tend to layer *system narratives* on top of game-style stat displays — the protagonist gets a "Skill: [Predation]" or "Title: [Demon Lord]" and the system explains it. Mechanics are *narrated*; the framing is meta-aware.
- Where does the engine's current skew sit relative to Isekai canon? The project name is Reincarnated; the Spirit Guide system carries isekai genre conventions; the seasonal arc is *fundamentally* an isekai descent. But the engine's pre-LLM label structure (per Q1) doesn't reflect this — it reads as ARPG-canonical with isekai-flavored skin. **Is this gap the structural problem file 37 surfaced?**

The output of Q3 is two parallel characterizations — engine-vs-ARPG-canon and engine-vs-Isekai-canon — with the gaps named explicitly.

### Question 4 — Push/pull: how do we decide where to land?

Now the strategy question. Given the canon-match analysis from Q3, what's the appropriate push/pull between ARPG-side concessions and Isekai-side commitments?

This is **NOT** asking you to recommend a specific lock. It's asking you to articulate the **decision framework** and identify the **decision points** Matt will need to navigate. Some candidate framings to consider (use what fits, replace what doesn't):

- **Audience prioritization.** Which audience is the project's primary? An ARPG-audience-first project lands closer to genre conventions and absorbs isekai-flavor as narrative skin (current default skew). An Isekai-audience-first project lands closer to embodiment variance and treats ARPG conventions as the mechanical substrate (file-37 latent intent). These are different commitments with different player vocabularies.
- **Embodiment as gameplay vs embodiment as narrative.** Is embodiment supposed to *change how the game plays* (mechanical consequence — different stats / different skills / different content interactions) or *change how the game feels* (narrative skin — same mechanical substrate, different framing)? File 37 § 3 locked Position C — *slot-as-functional-mechanic + embodiment-as-narrative-skin* — but Matt's Q4 reframing invites re-examining whether Position C is the right lock.
- **The Phase 0 vs post-Phase-0 split.** Per the Earth Meta-Layer concept (memory `project_earth_meta_layer.md`), Phase 0 is the seasonal-descent portion; post-Phase-0 introduces gacha-style form-library accumulation. Should the ARPG ↔ Isekai push/pull resolve *differently* in Phase 0 vs post-Phase-0? (Phase 0 may land ARPG-side for legibility; post-Phase-0 may lean Isekai-side because the form-library mechanism is fundamentally isekai.)
- **The catalogue-based form-bias resolution path.** The 2026-05-16 catalogue-based resolution (file 37 § "Catalogue-based form-bias resolution path") is currently the primary implementation strategy. Does it bias toward one canon over the other? (Catalogue contents from Pimen + future sources are HD-2D-shaped pixel-art with broad embodiment variance — this seems Isekai-friendly, but the rendering register is ARPG-comfortable, so the bias might cut differently than expected.)
- **The form-bias cadence options (I/II/III).** The cadence options were always going to be downstream of this strategy question. Surface — at the end — what the cadence options should look like *given* the strategy framing you've established.

The output of Q4 is a **decision framework** Matt can use to make the strategic call, plus your design-instinct recommendation if you have one (with explicit acknowledgement that the final call is Matt's).

## Direct-dialogue option

Per gandalf.md, you have direct-invocation privilege for engine-state and design-state questions during authoring. Recommended dialogue partners:

- **Rocket** (Pattern A or B) — for the Q1 inventory if you choose path (b). Rocket is the seam owner for generation/element/anchor/foundation and knows what labels/logic enter the LLM prompt-construction code.
- **Gamora** (Pattern A) — for Q2 convergence-skew analysis. Gamora authored the B10.4 work and knows where the simulation framework strains around archetype divergence and modifier-range distribution.
- **Jack-ryan** (DESIGN-MODE) — for stress-testing your Q3/Q4 framing if you want a Gate-1-style review before publishing. Optional.

Knight-rider does not need to be present for any of these dialogues. Coordinate timing directly.

## Required reading before starting

**The action-item context Matt referenced:**
- `canonical/37-form-bias-diagnosis-and-recovery.md` — full doc, especially § 1 (origin), § 2 (form-agnostic vs humanoid-bound inventory), § 6 (element architecture), § 10 (open questions)
- `~/.claude/projects/-Users-admin-Games-reincarnated-collaboration/memory/MEMORY.md` references to `project_engine_state_findings.md`, `project_design_intent.md`, `project_earth_meta_layer.md`

**Your own canonical-story corpus (for surfacing latent assumptions):**
- `canonical/story/court-of-forms.md`
- `canonical/story/cosmology-reincarnated.md`
- `canonical/story/enemy-visual-legibility.md`
- `canonical/story/embodiment-narrative-layer.md`
- `canonical/story/naming-triad.md`
- `canonical/story/style-register.md`
- `canonical/story/engine-balance-stewardship.md`
- `canonical/story/season-feel-rubric.md`
- `canonical/story/drift-audit.md`
- `canonical/story/engine-generic-meta-structure.md`

**The empirical research base for canon characterization:**
- `agentic_orchestration/research/knowledge/isekai/2026-05-16-isekai-evolution.md`
- `agentic_orchestration/research/knowledge/diablo/2026-05-16-diablo-design-retrospectives.md`
- `agentic_orchestration/research/knowledge/poe/2026-05-16-poe-design-philosophy.md`
- `agentic_orchestration/research/knowledge/arpg-community/2026-05-16-arpg-design-discourse.md`
- `agentic_orchestration/research/knowledge/arpg-adjacent/2026-05-16-adjacent-arpgs.md`

**The engine's structural commitments to test against:**
- `canonical/29-design-overview.md` (file 29 strategic anchor)
- `canonical/32-progression-design.md` (file 32 progression design)
- `canonical/33-trait-design.md` (file 33 trait architecture, if it exists at that path)
- `reincarnated-engine/design/decisions/decisions-log.md` (latest entries)
- `reincarnated-engine/design/working-agreement/engineering-disciplines.md` (especially candidate Disciplines #13 and #14 from the form-bias diagnosis)

**Memory references with direct bearing:**
- `project_trait_architecture.md` — trait surface (humanoid-archetype-bound today)
- `project_role_orientation_taxonomy.md` — damage/support/control/hybrid (Phase 2 decision)
- `project_geometry_palette.md` — 16-type palette and labels
- `project_b14_5_sidecar_analyses.md` — hunter-modifier-range + fire-over-representation findings
- `project_iterative_dev_disciplines.md` — discipline catalog

## What this commission unblocks

When this doc lands and Matt locks a strategic direction (or explicitly defers it with a documented framework):

- **Form-bias cadence options (I/II/III)** can be reformulated against the strategy lock rather than against the file-37 framing alone
- **Engineering disciplines #13 (implicit-pillar drift) and #14 (internal-vs-generative schema separation)** can be codified — both have been held pending cadence choice
- **Kit-anchor rename dispatch** for rocket can finally release (held pending cadence)
- **D1 element-name pool stewardship** can lock its decision criteria (the recent vocab-obscure / matt-promote / matt-demote pattern is currently ad-hoc; a strategic lock gives it structural grounding)
- **The catalogue-based form-bias resolution path's full operational shape** crystalizes — what abstractions to derive, what filters to consume, what the seasonal-generation pipeline does with the catalogue

## Decisions-log entries expected to follow

Per ADR-002 process: knight-rider drafts from your canonical work; jack-ryan Gate 1; Matt approves; commit. Anticipated:

- **Strategic-axis lock** (if Matt locks a position) — ARPG-canon-primary / Isekai-canon-primary / explicit-hybrid-with-defined-axis
- **Q1 inventory** — as a decisions-log entry OR as a sibling canonical doc per your preference
- **Position C revisit outcome** — if Q4 analysis surfaces that Position C lock (slot-as-mechanic / embodiment-as-skin) should be revisited, the revisit becomes its own decisions-log entry
- **Cadence-option reformulation** — once strategy lock is in place, the I/II/III options get a new draft tied to it

## Out of scope

- Specific implementation dispatch authoring (e.g., kit-anchor rename, embodiment-axis generation). Those follow once strategy locks.
- D1 element-name pool entry-by-entry review. Pattern-level analysis is in scope (what does the rubric structurally enforce vs not?); per-entry review is downstream.
- The Pimen catalogue contents themselves. Form-bias-cadence strategy is engine-side framing; catalogue contents are content-side. They will couple in implementation; they decouple in strategy.
- Multi-player / online-mode considerations. Project remains solo per `project_design_intent.md`; form-bias cadence is solo-context only.

## Acceptance criteria

- [ ] `canonical/story/form-bias-cadence-strategy.md` filed
- [ ] All four questions addressed with structured analysis + citations from Legolas research + cross-references to your own canonical-story corpus
- [ ] Q1 inventory documented (with rocket-dialogue or noted limitation)
- [ ] Q3 ARPG-canon and Isekai-canon characterizations both completed
- [ ] Q4 decision framework articulated; recommendation (if any) explicit-as-recommendation-not-lock
- [ ] Any dialogues invoked (rocket / gamora / jack-ryan) summarized in the doc
- [ ] Knight-rider notified at completion: doc path, headline takeaways per question, what the doc unblocks, readiness signal for decisions-log drafting

## Priority

**Active.** This is the highest-stakes generative-side design question on the table. No hard SLA, but it gates real downstream work — schedule it as your next focus block after any in-flight work completes.

---

## Completion record

**Completed:** 2026-05-16 (Day 4, gandalf session — restart after rate-limit cap on prior attempt; per Matt's parallel-workstream mandate this lands now via Path (b))

**Doc path:** `canonical/story/form-bias-cadence-strategy.md`

**Headline per-question takeaways:**

- **Q1 (Inventory):** Path (a) chosen; rocket Pattern A pass already filed; this doc reasons against the cluster organization in `pre-llm-substrate-inventory.md` rather than re-enumerating 53 items. Cluster A (14 humanoid-presupposing — gear schema) is one tight problem; Cluster B (18 form-agnostic-but-named-humanoid — distributed) is a labels-on-mechanics surface; Cluster C/D are form-agnostic/embodiment-orthogonal; Cluster E is the universal LLM-drift surface.
- **Q2 (Convergence shape):** Three orthogonal patterns under the terminology lock — P1 schema-cluster humanoid-presupposition (Cluster A), P2 labels-on-mechanics distributed pattern (Cluster B), P3 universal LLM-drift surface (Cluster E). Each has its own resolution lever. Terminology lock honored — *skew* off-limits without per-variable evidence; descriptive patterns named for shared vocabulary; B14.5 sidecar findings cited as observations, not attributions.
- **Q3 (Canon match):** **Asymmetric gap.** Engine substrate is ARPG-canon-comfortable across the board AND isekai-canon-incompatible at one specific cluster (Cluster A — gear/loadout schema). Outside Cluster A, isekai-incompatibility is either neutral or already partly-resolved. The push/pull question is not "which canon" but "where on each layer." Citations specific: Diablo II / D3 / D4 / PoE / Last Epoch / Grim Dawn humanoid-only across the board; Slime / Spider / Dragon Hatchling 2024 non-humanoid-reincarnation sub-genre per Legolas Pass 1.
- **Q4 (Push/pull):** **Explicit-hybrid Phase-0 with two locked sub-positions** + four deferred catalogue-track sub-locks. Sub-lock (a): ARPG-canon-primary at substrate-mechanical layer. Sub-lock (b): Isekai-canon-primary at narrative-skin and convergence layers. Position C reaffirmed not revisited. Four sub-locks deferred (cipher-width; Foundation layer placement; D1 reconsideration; per-season vocabulary coupling). Cipher-width framework explicit even with width itself deferred-pending-experiment. Cadence: Option II (Parallelized) recommended; four-stage backbone locked across all options.

**Dialogues invoked:** none in this session (rocket Pattern A already-filed; gamora not engaged — the Q2 work proceeded against the cluster framing without requiring fresh empirical-decomposition that the terminology lock barred anyway; jack-ryan not engaged — strategy doc lands for Matt-approval first, jack-ryan Gate 1 review will happen at knight-rider's decisions-log drafting time per the standard chain).

**Recommended strategic-axis position:** explicit-hybrid Phase-0 with sub-locks (a) ARPG-canon-primary at substrate-mechanical layer + (b) Isekai-canon-primary at narrative-skin and convergence layers. Phase-0 vs post-Phase-0 split named (post-Phase-0 deepens into isekai-canon at the Court / form-library). Cadence recommendation: Option II (Parallelized).

**Decisions-log drafts requested** (per § 8 of the strategy doc):
1. Strategic-axis lock entry — explicit-hybrid framing + two sub-positions + Position C reaffirmation
2. Three-layer model + cipher-width framework entry — refines doc 37 § 6
3. Four catalogue-track sub-locks deferred entry — explicit deferral + gates that resolve each
4. Disciplines #13a/#13b/#14 codification entry — terminology lock as the lens; routes via jack-ryan for engineering-disciplines.md authorship
5. Cadence option lock entry — Option II (Parallelized); four-stage backbone

**Notes for knight-rider:**

- Per § 9 the cross-seam cascades are documented per-seam (rocket / star-lord / gamora / drax / elrond / legolas) with strategic-axis context. Dispatch authoring sequenced behind the decisions-log entries; per Matt's parallel-workstream mandate the kit-anchor rename dispatch can release once the strategic-axis decisions-log entry lands.
- The four VS2b workstreams (S1 embodiment-axis schema; S2 pair-structure layer; display work; Pimen integration) named in the roadmap's Substrate Realignment Workstream § are unblocked by this strategy's locks + the staged sequencing in § 7.
- Open questions (§ 11) are tracked but non-blocking; Q11.3 (demo2's specific form-bias requirements) likely surfaces as a dispatch-shape soon if Matt confirms the demo2 milestone direction per the roadmap-stewardship dispatch's in-session message.
- The strategic-axis lock is Matt-approval-pending; jack-ryan Gate 1 happens at knight-rider's decisions-log drafting per the standard chain. Until those entries land, this strategy doc is canonical-story design intent; downstream work consumes its framing but does not yet commit to any decisions-log-level lock from it.
- Recommended next action for knight-rider: open the decisions-log drafting work (Gate 1 → Matt approves → commit); in parallel, the four deferred sub-locks remain queued for their catalogue-track gates (Experiment 2 returns informs three of four; Experiment 1 + Flag-A test resolve the remaining).
