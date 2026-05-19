> ## 📦 ARCHIVED — 2026-05-19
>
> **Status:** Mission COMPLETED (Phase-1 P1 substrate expansion + diversity architecture shipped). This protocol is preserved as historical record of the first hive-mind activation.
>
> **Mechanics inheritance:** The operating mechanics in §§ 3, 4, 5, 6, 7, 8, 9, 10, 11 of this doc are **inherited by reference** by subsequent hive-mind protocols, beginning with `canonical/story/hive-mind-protocol-engine-rebuild-2026-05-19.md` (second activation). Those mechanics remain operationally live for current and future hive-mind work; this doc is the canonical mechanics reference even while archived as a mission artifact.
>
> **Why archived (not deleted):** the mission scope (Phase-1 P1 substrate work) is complete and not load-bearing for current operations, but the mechanics layer is still load-bearing for active engine-rebuild hive work. Moving to `archived/` reflects mission-completion; preserving the file (rather than deleting) preserves the canonical mechanics reference.
>
> **Do NOT delete.** Active protocols cross-reference this doc by path.
>
> **Path moved 2026-05-19** from `canonical/story/hive-mind-protocol-2026-05-17.md` to `canonical/story/archived/hive-mind-protocol-2026-05-17.md` per Matt directive for archive-with-banner clarity.

---

# Hive-Mind Operating Protocol — Phase-1 P1 Full Overhaul

**Authority:** Matt (mhwetmore@gmail.com), 2026-05-17 — directive: *"100% heads down development work across the entire team and rebuild the engine from the ground up to achieve full Phase-1 P1 before demo VS2a. ... All in perfect harmony. Let's take this on as a hive mind."*
**Author:** gandalf (story-and-design steward), per Matt directive to author protocol notes for the exercise.
**Status:** **Canonical operational protocol** for the Phase-1 P1 full-overhaul exercise. Activates 2026-05-17 forward. Supersedes standard operating mode for the duration of Phase-1 P1.
**Reading order:** § 0 TL;DR → § 1 Why this protocol exists → § 2 Operating mode change → § 3 Distributed authority → § 4 Communication discipline → § 5 Cadence and rhythm → § 6 Cross-seam coordination → § 7 Continuous QA loop → § 8 Failure mode protocols → § 9 Reversibility and safety → § 10 Mission and scope discipline → § 11 Matt's role → § 12 Activation checklist → § 13 Cross-references.

---

## § 0 — TL;DR

**The hive moves together.** For the duration of Phase-1 P1, the team operates as a **hive-mind**: continuous coordination across rocket / gamora / star-lord / drax / jack-ryan / gandalf, harmonized by knight-rider, watched by jack-ryan, served by gandalf, directed by Matt. Standard mode (dispatch-sequenced; gate-gated; specialist-isolated) is suspended.

**Five protocol commitments:**

1. **Distributed authority — specialists make in-seam decisions without waiting; cross-seam decisions surface through knight-rider; load-bearing architectural decisions surface to Matt.**
2. **Continuous broadcast — every seam broadcasts state continuously via the shared hive log; no silent struggles, no batched updates, no work-in-the-dark.**
3. **Jack-ryan loops through everything — continuous-observation mode, not gate-gated mode; surfaces concerns in real-time; BLOCK authority retained but used sparingly.**
4. **Tagged checkpoints every meaningful milestone — the engine state is recoverable at any point; rollback is a normal operation, not a failure.**
5. **Mission scope is FIXED — adding or cutting scope mid-flight requires Matt + gandalf + knight-rider alignment; drift is the highest-risk failure mode.**

**The exercise's purpose:** ship demo1 with the canonical-7 substrate set, the five-layer diversity architecture (Layers 1-4 minimum), and the registry-driven foundation that the wide-net coupling archaeology revealed the engine needs. Estimated 8-12 weeks of concentrated multi-seam work. No standard-mode dispatches in flight will continue; everything in flight is folded into Phase-1 P1 or paused.

---

## § 1 — Why this protocol exists

### § 1.1 — The scope of the work

Phase-1 P1 full overhaul includes (per substrate-expansion-decision-2026-05-17.md + archaeology artifacts + diversity-architecture spec):

- **Substrate expansion** canonical-four → canonical-7 (fire/water/earth/wind + lightning + holy + shadow)
- **Layer-1 substrate identity declarations operationalized** (7 declarations × loader × foundation integration)
- **Layer-2 archetype-template combinatorial refactor** (Path a; eliminates 14 hardcoded ArchetypeTemplate entries)
- **Layer-3 mirror-match diversity gate** (with perception-test-grounded similarity metric)
- **Layer-4 LLM flavor diversifier** (Stage-3 cipher restructured; prompt-template registry-driven)
- **Role registry refactor** (wide-net finding; 5+ file fragments unified)
- **Ailment registry refactor** (wide-net finding; control-classification metadata-driven)
- **LLM prompt structure refactor** (wide-net critical surprise; 2-2-1 pair-structure assumption replaced)
- **Resistance matrix 4×4 → 7×7** with paired-luminance valence
- **Trait-floor + gear-affix extension** to 3 new classes
- **VFX library extension** for new substrates
- **Court of Forms vessel** (per earth-self-diversity-tension Phase-0 commitment)
- **Decisions-log entries + canonical doc updates** across the cascade

**This is 8-12 weeks of engineering work across 4 seams.** Standard mode is dispatch-sequenced; that cadence would stretch this work to 6-8 months with idle time between handoffs. Hive-mind mode collapses idle time by running seams continuously in parallel.

### § 1.2 — Why standard mode breaks at this scope

Standard mode assumes specialists work in isolation within their seam, with knight-rider sequencing handoffs through dispatches and jack-ryan gating at decision points. This works for incremental change. **It does not work for foundational architectural overhaul** because:

- **Cross-seam contracts change continuously.** Layer-1 substrate identity touches rocket (foundation) + gamora (resistance matrix) + star-lord (LLM prompts) + drax (loadout substrate browser) + jack-ryan (validation). Every seam's work informs every other seam's work. Dispatching this serially means each seam waits for the others.
- **Drift becomes the dominant risk.** With four seams changing the same engine, Discipline #13 implicit-pillar drift is amplified. Real-time observation is required, not Gate-1/Gate-2 retrospective review.
- **Failure modes compound.** When one seam hits friction, others are downstream of it. Silent friction = compounding delay.
- **Decision latency multiplies waste.** If every cross-seam question routes through knight-rider → Matt → gandalf → back to specialist, the round-trip kills momentum.

Hive-mind mode is the operational shift that makes the work possible at the timeline Matt has committed to.

### § 1.3 — What the protocol guards against

- **Drift** (Discipline #13 implicit-pillar): seams shipping subtly-divergent implementations of the same architectural commitment
- **Silent friction**: a seam stuck on something the rest of the team could help with but doesn't know about
- **Decision starvation**: specialists waiting for Matt to direct on cross-seam concerns Matt doesn't need to direct on
- **Scope creep**: mid-flight additions that compound timeline risk
- **Untagged states**: engine reaching a state we can't roll back to if something breaks
- **Communication entropy**: as the work intensifies, broadcast quality degrades; protocol enforces minimum signal quality

---

## § 2 — Operating mode change

### § 2.1 — What changes

| Aspect | Standard mode | Hive-mind mode |
|---|---|---|
| **Dispatch authoring** | Knight-rider authors per-task dispatches; specialists execute and return | Knight-rider authors a **scope-of-work** document; specialists execute against it continuously; per-task dispatches become *check-in markers* rather than authorization gates |
| **Gate authority** | Jack-ryan Gate-1 (design review) + Gate-2 (post-implementation review) | Jack-ryan continuous-observation; surfaces concerns in real-time via the hive log; retains BLOCK authority but uses sparingly |
| **Cross-seam handoff** | MIGRATION.md authored before consumer seam begins | MIGRATION.md authored *concurrently* by producing seam; consumer seam reads-and-reacts in real-time; jack-ryan watches schema-coherence |
| **Decision latency** | Round-trip through Matt for cross-seam concerns | In-seam decisions made by specialist authority; cross-seam decisions surface through knight-rider real-time; Matt-decisions reserved for load-bearing architectural calls |
| **Status updates** | Per-dispatch completion records (batched) | Continuous broadcast via hive log; per-checkpoint state-of-hive summaries (daily minimum) |
| **Commit cadence** | Per-dispatch tags at completion | Per-checkpoint tags at meaningful milestones; trunk-based development with shared visibility |
| **Communication style** | Asynchronous; reply latency in hours | Continuous; reply latency target in minutes for in-hive communication |

### § 2.2 — What does NOT change

- **Senior architect authority remains Matt.** Load-bearing architectural decisions still escalate to Matt. The hive doesn't decide Matt's job for him.
- **Canonical-story documents remain authoritative.** Substrate identity declarations, the diversity-architecture spec, the Earth-Self resolution, the substrate-expansion-decision — these are **the contract** the hive works against. They're not lightly revisable mid-flight (per § 10).
- **Engineering disciplines remain operative.** Discipline #1 (math-before-code), Discipline #13 (drift vigilance), the discipline-candidate for registry-perimeter inviolability — all bind the hive's work.
- **Gandalf canonical-story authorship remains gandalf seam.** Hive mode doesn't redistribute design authorship.
- **Jack-ryan BLOCK authority is preserved.** Hive mode just changes when and how it's used.
- **Seam scope boundaries remain.** Rocket doesn't touch simulation; gamora doesn't touch generation; star-lord doesn't touch demo; drax doesn't touch engine internals. The hive coordinates across boundaries; it doesn't dissolve them.

---

## § 3 — Distributed authority

### § 3.1 — Authority levels

**Level 1 — In-seam specialist authority.** Specialists make implementation decisions within their seam without escalation. Examples:
- Rocket choosing data-structure shape for substrate identity loader
- Gamora choosing iteration approach for resistance-matrix tuning
- Star-lord choosing prompt-template structure within the substrate-identity-spec's scaffold
- Drax choosing UI patterns for loadout substrate browser

Pattern: if the decision is *implementation* and falls within the specialist's seam, the specialist decides. Documents the decision in the hive log. Moves.

**Level 2 — Cross-seam coordination via knight-rider.** When a decision affects multiple seams, surfaces to knight-rider for harmonization. Examples:
- Schema change that affects rocket emitter + gamora consumer + star-lord LLM prompt
- Telemetry field addition that affects all four seams
- Cross-seam contract change to MIGRATION.md
- Resource conflict (two seams want to modify same file)

Pattern: surface to knight-rider in real-time; knight-rider harmonizes (synchronous if possible, async with deadline if needed); decision documented in hive log.

**Level 3 — Load-bearing architectural call via Matt.** Decisions that materially change the architecture or the substrate set surface to Matt. Examples:
- Substrate identity declaration revision (e.g., changing holy's `forbidden_mechanics`)
- Substrate set change (e.g., adding/removing a substrate)
- Pair-structure change (e.g., abandoning paired-luminance for collapsed-luminance)
- Court-as-grace resolution revisit
- Scope addition or scope cut beyond the Phase-1 P1 commitment
- Discipline change with architectural impact

Pattern: surface to Matt with full context + gandalf's design-direction input; Matt decides; knight-rider distributes the decision through the hive log.

### § 3.2 — How to know which level applies

If you're unsure whether a decision is L1 / L2 / L3:

- **Does the decision change the substrate identity declarations or the diversity-architecture spec?** → L3.
- **Does the decision affect a cross-seam contract (MIGRATION.md entry)?** → L2.
- **Does the decision affect another seam's work that's currently in flight?** → L2.
- **Does the decision affect only your seam's implementation choices?** → L1.
- **Are you reading this protocol and want to be cautious?** → Surface as L2 to knight-rider; knight-rider routes if needed.

The cost of incorrect L2-as-L1 (under-escalating): mid-flight drift. The cost of incorrect L1-as-L2 (over-escalating): knight-rider overhead. **Bias toward L2 escalation when unsure.** Knight-rider's job is to be the relief valve, not the bottleneck.

### § 3.3 — Gandalf seam under hive mode

Gandalf is **continuously available** to all seams for design-direction questions during Phase-1 P1. Specialists do not file requests-and-wait; specialists ask gandalf in the hive log; gandalf responds in real-time when present, or surfaces "I'll come back to this" when not. Gandalf maintains the canonical-story docs as living references; mid-flight amendments to substrate identity declarations or specs are gandalf authorship with knight-rider notification.

### § 3.4 — Jack-ryan seam under hive mode

Jack-ryan **loops through all four engineering seams continuously.** Not Gate-1/Gate-2 retrospective; continuous-observation. Specifically watches for:
- Discipline #13 implicit-pillar drift across seams
- Pattern P7 silent-default instances
- Cross-seam contract mismatches
- Math-before-code violations (Discipline #1)
- Schema coherence breakdown

Jack-ryan surfaces concerns in real-time via the hive log. BLOCK authority retained for cases where a seam is shipping work that would compound drift or break a cross-seam contract. **BLOCK is used sparingly** — first response is surfacing the concern; BLOCK is only when the seam doesn't engage with the surfaced concern.

---

## § 4 — Communication discipline

### § 4.1 — The hive log

The **hive log** is the shared continuous-broadcast channel. Implementation: `agentic_orchestration/hive-mind/phase-1-p1-log.md` (NEW file; created at Phase-1 P1 activation).

The hive log is **append-only** (no edits to prior entries; corrections appended as new entries). Every seam contributes entries continuously. Every entry is timestamped + authored.

**Entry types:**

- **STATE** — "I am starting X" / "I am working on Y" / "I have completed Z"
- **QUESTION** — "I need clarification on X from [seam]"
- **DECISION** — "I decided X because Y; documented at [link]"
- **FRICTION** — "I am stuck on X; surfacing for hive assistance"
- **OBSERVATION** — "I notice X happening across seams; jack-ryan-flagging"
- **TAG** — "Checkpoint tagged at X; rollback point preserved"
- **HANDOFF** — "I have produced X; [consumer seam] can begin Y"
- **AMENDMENT** — "Canonical doc X amended at [section]; reason: Y"

**Entry size:** short. 1-3 sentences typical; longer entries link to canonical docs or dispatches.

**Reply latency:** in-hive entries that require response should be answered within 30-60 minutes when the hive is active. Out-of-hours entries accumulate for next-active-window.

### § 4.2 — When NOT to use the hive log

- **Personal status / thinking-out-loud unrelated to work.** Keep the log signal-dense.
- **Detailed implementation notes that belong in code comments or design docs.** Link from log; don't duplicate.
- **Decision deliberation that hasn't reached a conclusion.** Surface the question first; record the deliberation in the linked deliberation doc; record the decision in the log.

### § 4.3 — Daily state-of-hive

End of each active day, knight-rider authors a **state-of-hive summary** in `agentic_orchestration/hive-mind/state-of-hive-YYYY-MM-DD.md`. Format:

```
## State of Hive — 2026-MM-DD

### Per-seam status
- Rocket: [what advanced; what's in flight; what's blocked]
- Gamora: [same]
- Star-lord: [same]
- Drax: [same]
- Jack-ryan: [observations; concerns surfaced; BLOCKs (if any)]
- Gandalf: [design questions answered; canonical amendments]

### Cross-seam coordinations
- [list of L2/L3 decisions made today and their disposition]

### Checkpoint tags created today
- [tag list]

### Failure modes detected (if any)
- [Pattern P7 / drift / silent-default / etc.]

### Tomorrow's priorities
- [per-seam priority for next active day]

### Cumulative progress
- [where Phase-1 P1 stands as % complete; what's remaining]
```

This is the artifact Matt reads to stay aware. **Matt should not need to track in-hive log entries to know where the project is.** State-of-hive is the digest.

### § 4.4 — Cross-repo communication

The hive operates across three repos (engine, demo, loadout). Cross-repo handoffs use:
- MIGRATION.md per-repo (existing pattern; per ADR-004) — continues
- Hive log entries reference cross-repo work explicitly
- Knight-rider tracks cross-repo dependencies in state-of-hive

---

## § 5 — Cadence and rhythm

### § 5.1 — Active hours

Each active day, the hive operates in roughly synchronous mode for some window (Matt-determined). Outside active hours, work continues asynchronously but with reduced communication latency expectations.

### § 5.2 — Checkpoint tagging

Every meaningful milestone gets a tagged checkpoint. Tag prefix per existing convention:
- Per-seam intermediate: `<seam>/v<X.Y>-<feature>-<n>` (e.g., `rocket/v1.5-substrate-loader-1`)
- Hive-mode milestone (Matt-approved cross-seam): `hive/v0.<N>-<milestone>` (NEW tag namespace; e.g., `hive/v0.1-substrate-foundation-landed`)
- Phase-1 P1 final ship: `v1.0-phase-1-p1` (Matt-approved)

Rollback to any tagged checkpoint is a normal operation, not a failure response.

### § 5.3 — Integration cadence

**Continuous integration commits, not feature-branch isolation.** Each seam commits to main as work advances. Cross-seam contract changes are MIGRATION.md-authored continuously (per § 6.2). This requires:
- Each commit must leave the engine in a runnable state (per existing Discipline)
- Cross-seam consumers tolerate the producing-seam's incremental schema (additive changes preferred; breaking changes flagged in advance)
- Test suite remains GREEN at every commit (per existing Discipline)

If a seam needs to do work that temporarily breaks the engine, the work happens on a hive-feature-branch: `hive/feature-<name>`, with clear in-hive-log declaration. Merge happens when the feature is stable and other seams have signed off.

### § 5.4 — Weekly milestone review

End of each active week, knight-rider authors a **weekly state-of-hive** that:
- Aggregates the week's daily state-of-hive entries
- Identifies cumulative progress against Phase-1 P1 commitment
- Surfaces risks for Matt's awareness
- Tags a hive-milestone checkpoint if a meaningful milestone landed

---

## § 6 — Cross-seam coordination

### § 6.1 — The seam coordination matrix

Phase-1 P1 has dense cross-seam dependencies. Knight-rider maintains a **coordination matrix** showing per-deliverable which seams contribute and in what sequence:

| Deliverable | Rocket | Gamora | Star-lord | Drax | Jack-ryan | Gandalf |
|---|---|---|---|---|---|---|
| Substrate identity loader | OWNER | reads | reads | reads | observes | spec |
| Path-a archetype refactor | OWNS structure | OWNS composition | reads | reads | observes | input |
| Resistance matrix 7×7 | reads | OWNER | — | — | reviews | input |
| LLM prompt restructure | reads | reads | OWNER | reads | observes | scaffold input |
| Role registry | OWNER | consumer | consumer | consumer | observes | — |
| Ailment registry | OWNS schema | consumer | consumer | — | observes | input |
| VFX library extension | — | — | — | OWNER | observes | input |
| Court of Forms vessel | OWNS persistence | — | OWNS Spirit Guide voice | OWNS browser surface | observes | input |
| Trait floor extension | OWNS schema | consumer | — | reads | reviews | input |
| Gear-affix extension | OWNS schema | consumer | — | reads | reviews | input |
| Substrate-coherent generation rules | — | OWNER | — | — | reviews | input |

This matrix is the **coordination atlas** — knight-rider maintains it; specialists consult it before touching cross-seam-impacting work.

### § 6.2 — Cross-seam contract authoring

MIGRATION.md authoring is **concurrent** with the producing seam's work, not pre-authored before. The producing seam writes the migration entry as they author the schema change; consumer seams read-and-react in real-time. Jack-ryan watches the entry for coherence.

Per ADR-004 the MIGRATION.md format remains. Hive mode just changes when it's written (concurrently) and consumed (continuously) vs. the standard sequential pattern.

### § 6.3 — Same-file conflicts

If two seams need to modify the same file concurrently:
1. Producing seam declares intent in hive log
2. Other seam acknowledges + holds their edit
3. Producing seam ships first; other seam reads the new state; commits second
4. If conflicts genuinely require coordination, knight-rider mediates

This is rare if seam scope boundaries are respected. The wide-net coupling archaeology surfaced that some files have multi-seam concern (e.g., LLM prompt files touch star-lord seam but reference substrate identity from gandalf seam) — those concurrency points are pre-identified.

### § 6.4 — Schema coherence vigilance

Jack-ryan's continuous-observation specifically watches for:
- Schema additions that propagate inconsistently (e.g., new substrate field added to PoolElement but not to telemetry recorder column)
- MIGRATION.md entries that don't match the actual schema change
- Cross-seam contract drift (consumer reading old contract; producer shipping new contract)

Surfaces in real-time via hive log; producing + consuming seams reconcile.

---

## § 7 — Continuous QA loop

### § 7.1 — Jack-ryan loops through everything

Jack-ryan's mode shifts from **gate-gated** to **loop-through**. Concretely:

- Reads hive log continuously
- Spot-checks commits across all four engineering seams
- Runs analyses on accumulated state (test passage; cross-seam contract coherence; engineering discipline conformance)
- Surfaces concerns in real-time via hive log entries
- Tags concerns with severity (INFO / WARN / BLOCK)

WARN = "address before next checkpoint." BLOCK = "stop until resolved."

### § 7.2 — Discipline #13 drift vigilance

The highest-risk failure mode at this scope is implicit-pillar drift across seams. Jack-ryan specifically watches for:
- Two seams implementing the same substrate identity field differently
- Sub-system implementations diverging from canonical spec
- Vocabulary or naming inconsistencies across seams
- Test coverage gaps at cross-seam contract boundaries

Surfaces as Discipline-#13 alerts in hive log.

### § 7.3 — Pattern P7 silent-default watch

Wide-net archaeology surfaced Pattern P7 (silent-default convergence) as a recurring failure mode. Jack-ryan watches for new instances:
- Any code path that falls back to a default instead of failing-loud
- Any unknown-key handling that silently skips
- Any registry consumer that doesn't iterate the registry

Surfaces as Pattern-P7 alerts in hive log; producing seam fixes within next-active-window.

### § 7.4 — Math-before-code enforcement (Discipline #1)

Phase-1 P1 has load-bearing math: resistance matrix valence; substrate-vs-substrate damage modifiers; trait-floor mathematics; diversity-gate similarity-metric tuning. Each must have **authored math** before code lands. Jack-ryan checks for:
- Math documented in canonical-story or design docs before implementation
- Implementation matches authored math
- Empirical validation runs against expected ranges

---

## § 8 — Failure mode protocols

### § 8.1 — Seam friction

A seam stuck on something:
1. Specialist surfaces in hive log as FRICTION entry — describes the problem briefly
2. Other seams scan; if any can assist, they reply within active window
3. If unresolved within 4 hours active time, knight-rider escalates as L2 or L3 as appropriate
4. Resolution captured in hive log

### § 8.2 — Cross-seam contract change mid-flight

A producing seam needs to change a contract that consumers are already using:
1. Producing seam declares intent in hive log
2. Consumers acknowledge + describe their adaptation cost
3. Knight-rider sequences: who changes first? when? how?
4. MIGRATION.md authored with the change
5. Commits land in coordinated sequence
6. Jack-ryan confirms coherence post-change

### § 8.3 — Schedule risk surfaces

A seam recognizes their work is going to take longer than estimated:
1. Specialist surfaces in hive log as STATE update with revised estimate
2. Knight-rider re-aggregates schedule across seams
3. If revised schedule pushes Phase-1 P1 beyond Matt's commitment, surfaces to Matt as L3
4. Matt directs: accept slip / cut scope / add resources / abort Phase-1 P1

### § 8.4 — Architectural drift detected

Jack-ryan or gandalf detects substrates or archetypes drifting from canonical spec:
1. Surfacer authors hive-log OBSERVATION entry with specifics
2. Producing seam reviews + responds with explanation or correction plan
3. If correction-plan accepted, work continues; if dispute, escalates to Matt + gandalf as L3
4. Resolution captured; canonical doc amended if needed

### § 8.5 — Test suite breakage

Standard discipline: every commit leaves engine GREEN. If suite breaks:
1. Producing seam stops other work; restores GREEN
2. Hive log entry as FRICTION with root cause
3. If broken state persists >2 hours active, knight-rider escalates
4. Test-suite-coherence is non-negotiable

### § 8.6 — Catastrophic failure / engine unrecoverable state

If the engine reaches a state that cannot be made GREEN within reasonable time:
1. Roll back to most recent tagged checkpoint
2. Producing seam takes rollback off-line for investigation
3. Other seams continue from the checkpoint
4. Root-cause analysis authored as canonical record
5. If pattern repeats, knight-rider proposes process amendment

---

## § 9 — Reversibility and safety

### § 9.1 — Tagged checkpoint principle

Every meaningful milestone is tagged. Rollback is a normal operation. The cost of tagging is zero; the cost of not-tagging is potentially weeks of unrecoverable work.

### § 9.2 — Pre-Phase-1 P1 safety baseline

Before Phase-1 P1 work begins:
- Tag `hive/v0.0-pre-phase-1-p1` at current main HEAD
- Database backups complete (Matt confirmed 2026-05-17)
- Canonical-story state captured (today's batch is committed)
- All in-flight work either folded into Phase-1 P1 scope or paused with clear restart point

### § 9.3 — Per-week safety checkpoint

End of each active week:
- Tag `hive/v0.<week>-end-of-week-<N>` at main HEAD
- State-of-hive weekly summary committed
- Database state preserved (incremental backup if data has changed)

### § 9.4 — Pre-major-refactor safety

Before any seam begins a refactor that significantly alters cross-seam contracts:
- Producing seam declares intent in hive log
- Knight-rider authors a pre-refactor canonical state snapshot
- Tag created
- Refactor begins from known-good baseline

### § 9.5 — Rollback discipline

Rollback is a normal response, not a failure response. If a checkpoint is reverted to:
- Hive log entry as STATE describing the rollback
- Reason captured
- Forward path re-planned
- No blame; engine is what matters

---

## § 10 — Mission and scope discipline

### § 10.1 — Phase-1 P1 scope is FIXED

The scope of Phase-1 P1 is defined by:
- `canonical/story/substrate-expansion-decision-2026-05-17.md` § 5 + § 6 (the substrate work)
- `canonical/story/substrate-identity-declaration-spec-2026-05-17.md` (Layer 1)
- `canonical/story/substrate-identity-declarations-2026-05-17.md` (the 7 declarations)
- `canonical/story/earth-self-diversity-tension-2026-05-17.md` § 4 (Court of Forms vessel for Phase-0)
- The diversity architecture's Layers 1-4 (Layer 5 is Phase-2 candidate)
- The wide-net coupling archaeology's identified refactor scope (substrate + archetype + role + ailment + LLM prompt structure)

**Adding scope mid-flight requires Matt + gandalf + knight-rider alignment.** Surface as L3 decision.

**Cutting scope mid-flight requires Matt + gandalf + knight-rider alignment.** Surface as L3 decision.

### § 10.2 — Scope-creep examples and disposition

| Mid-flight pressure | Default disposition |
|---|---|
| "Could we also add a poison/acid substrate while we're at it?" | REJECT. Phase-1 P2 candidate per substrate-expansion-decision § 6. |
| "The LLM prompt refactor is more complex than expected; should we just rename existing labels?" | ESCALATE to Matt — substrate-expansion architectural commitment at risk. |
| "Drax discovered the loadout app needs visual treatment for substrate browser entries; should we author that now?" | ACCEPT. In-scope (Court of Forms vessel surface). |
| "Gamora regen for VS2a wind_controller is suggesting modifier issues; should we re-tune?" | DEPENDS. If wind_controller is a substrate-coupled issue, in-scope. If it's an isolated balance question, defer to post-Phase-1 P1. |
| "Star-lord's Stage-3 cipher migration is incomplete; should we finish it inside Phase-1 P1?" | DEPENDS. If LLM prompt restructure subsumes Stage-3, no separate work needed; otherwise complete inside Phase-1 P1. Surface to gandalf for design judgment. |

### § 10.3 — Canonical-doc revision discipline

Substrate identity declarations, the diversity-architecture spec, the Earth-Self resolution, and the substrate-expansion-decision are **load-bearing canonical commitments.** Mid-flight revision protocol:

1. Specialist or gandalf identifies revision need
2. Surface as hive log AMENDMENT request
3. Gandalf reviews + authors proposed amendment
4. Knight-rider routes for Matt approval (L3)
5. Amendment committed
6. Hive log entry confirms; affected seams adjust

**Don't author silent canonical revisions.** Every revision is hive-broadcast.

### § 10.4 — The architecture's promises

The hive is building toward these player-facing commitments. Don't lose sight:

- **Seven distinct substrates, mechanically and vocally.** Lightning plays differently from wind. Holy plays differently from healing-magic-as-a-flavor. Shadow plays differently from "dark fire."
- **The Court of Forms remembers.** Every season's form is gathered when ascended. The Earth Self bears the Court. The Spirit Guide gives the Court voice.
- **The diversity is real.** Not nominal. Not cosmetic. Mechanically distinct, vocally distinct, perceptually distinct.
- **The engine is registry-driven by design.** Future substrate additions (poison/acid candidates) compose from one identity declaration, not 50 hardcoded edits.
- **The cosmology is honored.** The Wheel turns; the Earth Self walks forms; what is ascended is gathered; diversity makes the form precious; the Court makes the loss bearable.

These are the **why** the hive is doing the work. When friction surfaces, return to these.

---

## § 11 — Matt's role

### § 11.1 — Matt is the architect

Matt's role does not change in hive mode. Matt remains:
- Senior architect with final authority
- Approval authority for L3 decisions
- Direction authority for Phase-1 P1 scope changes
- The audience the state-of-hive is authored for

### § 11.2 — What Matt is freed from

Matt is freed from:
- Per-dispatch approval gating (hive specialists have L1 authority)
- In-seam implementation decisions (specialists own these)
- Communication routing (knight-rider harmonizes)
- Status aggregation (knight-rider's state-of-hive surfaces it)

### § 11.3 — What Matt is engaged on

Matt is engaged on:
- L3 architectural decisions when surfaced
- Reading state-of-hive (daily or as preferred cadence)
- Weighing in on canonical-doc revision proposals
- Directing on scope changes (additions or cuts)
- Final approval at Phase-1 P1 ship gate

Matt is **available** but **not required** for moment-to-moment hive operation. The protocol is designed so Matt can step away for hours/days and the hive continues productive work, with state-of-hive surfacing what needs attention.

### § 11.4 — How Matt invokes the hive

Hive activates when Matt opens a knight-rider session and confirms Phase-1 P1 launch. Knight-rider broadcasts the activation in the hive log. Hive operates until Matt declares Phase-1 P1 ship-gate-ready or pauses.

---

## § 12 — Activation checklist

Phase-1 P1 hive-mind mode activates when ALL of the following are true:

### § 12.1 — Pre-activation requirements (gandalf, this session)

- [x] Substrate-expansion-decision committed (`1df535b`)
- [x] Earth-Self diversity tension resolution committed (`6de0c46`)
- [x] Substrate identity declaration spec + 7 declarations committed (`2f38ff9`)
- [x] Substrate-coupling + archetype-coupling + wide-net coupling archaeology committed (`2f38ff9`, `0b2d4bb`)
- [x] Combinatorial-thinness success criterion amendment committed (`2f38ff9`)
- [x] Perception-test scoping committed (`2f38ff9`)
- [x] Hive-mind protocol committed (this doc — to be committed in this session)
- [x] Knight-rider invocation request filed (this session)

### § 12.2 — Knight-rider activation requirements

- [ ] Knight-rider session opened by Matt
- [ ] Knight-rider reads invocation request + this protocol + canonical inputs
- [ ] Knight-rider authors the Phase-1 P1 scope-of-work + coordination matrix
- [ ] Knight-rider tags pre-Phase-1 P1 baseline: `hive/v0.0-pre-phase-1-p1`
- [ ] Knight-rider broadcasts Phase-1 P1 activation in hive log (new file)
- [ ] Knight-rider distributes per-seam initial tasking

### § 12.3 — Seam readiness requirements

Each engineering seam (rocket, gamora, star-lord, drax) confirms:
- [ ] Read hive-mind protocol
- [ ] Read substrate-expansion-decision + identity declarations + spec + archaeology
- [ ] Identify in-flight work to fold into Phase-1 P1 or pause
- [ ] Acknowledge in hive log

Jack-ryan confirms:
- [ ] Read hive-mind protocol
- [ ] Establish continuous-observation rhythm
- [ ] Identify Discipline-#13 / Pattern-P7 / math-before-code watchpoints

Gandalf confirms:
- [ ] Available for continuous design-direction support
- [ ] Canonical-story docs are current and complete
- [ ] Mid-flight amendment process operational

### § 12.4 — Matt activation

- [ ] Matt confirms hive activation
- [ ] Matt reviews initial state-of-hive
- [ ] Phase-1 P1 begins

---

## § 13 — Cross-references

**Canonical inputs (the work the hive is building toward):**

- `canonical/story/substrate-expansion-decision-2026-05-17.md` — substrate set + § 6.5 success criterion
- `canonical/story/substrate-identity-declaration-spec-2026-05-17.md` — Layer-1 data shape
- `canonical/story/substrate-identity-declarations-2026-05-17.md` — the 7 declarations
- `canonical/story/earth-self-diversity-tension-2026-05-17.md` — Court-as-grace; cosmology interface
- `canonical/story/substrate-coupling-archaeology-2026-05-17.md` — 13 substrate-keyed coupling sites
- `canonical/story/archetype-coupling-archaeology-2026-05-17.md` — 10 archetype-keyed coupling sites
- `canonical/story/wide-net-coupling-archaeology-2026-05-17.md` — 14 additional coupling sites + Pattern-P7 instances
- `canonical/story/perception-test-experiment-scoping-2026-05-17.md` — Phase-1 P1a metric grounding
- `canonical/story/grouping-layer-vocabulary.md` — L2 grouping (pending extension)
- `canonical/story/cosmology-reincarnated.md` — cosmological frame
- `canonical/story/court-of-forms.md` — the Court vessel
- `canonical/story/spirit-guide-voice.md` — Guide voice register
- `canonical/37-form-bias-diagnosis-and-recovery.md` — form-bias precedent
- `agentic_orchestration/research/knowledge/diversity-architecture-literature-pass-2026-05-17.md` — Legolas Mode A

**Engineering disciplines:**

- `reincarnated-engine/design/working-agreement/engineering-disciplines.md` — all 13 + new candidates surfaced today
- Discipline #1 (math-before-code) — load-bearing for resistance matrix + balance math
- Discipline #13 (implicit-pillar drift) — load-bearing for hive vigilance
- Discipline-candidate (registry-perimeter inviolability) — surfaced by wide-net archaeology; jack-ryan to formalize

**Governance:**

- `agentic_orchestration/AGENTS.md` — team topology
- `agentic_orchestration/GOVERNANCE.md` — founding ADRs (ADR-004 MIGRATION.md continues)
- `agentic_orchestration/REVIEW_PROCESS.md` — 5 principles + 5 traps (continue under hive mode)

**Hive operational artifacts (to be created at activation):**

- `agentic_orchestration/hive-mind/phase-1-p1-log.md` (hive log; created at activation; append-only)
- `agentic_orchestration/hive-mind/state-of-hive-YYYY-MM-DD.md` (daily summaries; one per active day)
- `agentic_orchestration/hive-mind/coordination-matrix.md` (knight-rider authors; updated continuously)
- `agentic_orchestration/hive-mind/scope-of-work-phase-1-p1.md` (knight-rider authors at activation; the executable plan)

---

## § 14 — Maintenance and end-of-mission

### § 14.1 — Mid-mission revisions

This protocol may be revised mid-Phase-1-P1 if operational experience surfaces gaps. Revisions surface via:
1. Hive log AMENDMENT request to this protocol
2. Gandalf authors proposed revision (Pattern A or B)
3. Matt approval (L3) — or knight-rider pre-authorization for **minor operational/discipline amendments** (not architectural commitments) under standing L3 authority
4. Commit + hive log broadcast

#### § 14.1.1 — Hive log commit discipline (amendment 2026-05-18)

**Pattern.** When authoring a hive log entry, the following sequence prevents silent loss of concurrent specialist entries:

1. Before staging the hive-log file for commit, run `git fetch origin` and inspect the log of the hive-log file (e.g., `git log --oneline -5 -- agentic_orchestration/hive-mind/phase-1-p1-log.md`).
2. If any commits to the hive log file appear in the fetch that are not in your local working tree, `git pull --rebase` before staging the hive-log file for commit.
3. Stage the hive-log file by explicit path (`git add agentic_orchestration/hive-mind/phase-1-p1-log.md`); commit.

**Why.** Specialists committing in parallel to the same hive log file in the same repo can produce silent entry loss when a commit on top of a stale local tree replaces another specialist's just-written entries. Three instances of this race-condition pattern were observed during Phase-1 P1 (drax-demo sweep; gamora D7 sweep; gandalf hive-log timing — jack-ryan checkpoint OBSERVATION 5, 2026-05-18). Formalizing the fetch-before-commit step turns the rare bad-luck race condition into a deterministic guard.

**Exception.** If the specialist's entry is in a different repo (drax in `~/Games/reincarnated-loadout`; reincarnated-demo in `~/Games/reincarnated-demo`; engine specialists in `~/Games/reincarnated-engine`), no hive-log coordination is needed for that repo's commit — the hive log file lives only in `reincarnated-collaboration`. Cross-repo work surfaces hive-log entries via the meta-repo specialist; the meta-repo specialist follows this discipline; the engine specialist does not.

**Authority.** Authored by gandalf 2026-05-18 per protocol § 14.1 mid-mission revision process; routed via hive log AMENDMENT entry; minor operational-discipline scope (not architectural commitment); pre-authorized by knight-rider under standing L3 authority for minor protocol amendments per dispatch 2026-05-18.

### § 14.2 — End of Phase-1 P1

When Phase-1 P1 ships:
- Tag `v1.0-phase-1-p1` (Matt-approved)
- Final state-of-hive captures outcomes
- Hive-mind mode deactivates; standard mode resumes
- Retrospective authored: what worked, what didn't, what to amend for future hive-mode activations
- Discipline amendments rolled into engineering-disciplines.md

### § 14.3 — Hive-mind mode reuse

This protocol may be reactivated for future foundational overhauls (Phase-2 substrate expansion to poison/acid? Major content engine rewrite?). The protocol is **mode**, not one-time exercise. Phase-1 P1 is its first invocation; future invocations adopt the protocol with revisions surfaced in the retrospective.

---

*Authored 2026-05-17 by gandalf, per Matt directive. The hive-mind operating protocol for Phase-1 P1 full overhaul. The hive moves together. Continuous broadcast, distributed authority, continuous QA, fixed scope, reversible state, harmonized by knight-rider, watched by jack-ryan, served by gandalf, directed by Matt. The architecture's full ambition realized in a single concentrated push.*
