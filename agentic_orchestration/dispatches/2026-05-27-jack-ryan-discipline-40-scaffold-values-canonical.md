# Dispatch — 2026-05-27 — jack-ryan — Discipline #40 ratification (scaffold-values-require-canonical-decision)

**From:** knight-rider
**To:** jack-ryan (analyst + QA gatekeeper; canonical-write authority for engineering-disciplines.md)
**Approved by:** Matt 2026-05-27 ratified the recognition that scaffold values calcifying into "this is what the system does" is a real failure mode per scaffold-drift consolidated package; jack-ryan ratifies the discipline-form per § 4.5
**Estimated effort:** ~2-4 hours (canonical-write + cross-discipline composition + operational hook documentation)
**Acceptance:** Discipline #40 entry authored at `~/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md`; cross-references to #11, #13, #18, #39 per § 4.4; operational hooks per § 4.3 documented

## Context

Three concrete scaffold-drift cases surfaced 2026-05-27 (consolidated doc § 1.2):

1. SC-6b substrate enrichment + uniform sampling → STR heavy-melee monoculture + ammo contamination
2. Cycle 13 gauntlet PASS criteria (16-of-18 cells) → 16-character de facto season size (no canonical doc locks 16)
3. Wave 0.5 per_skill_emitter minimum-viable 3-chain × 4-tier grid → contradicts six locked architectural commitments (doc 40 § 8.3 + D66 + D69 + D83 + supporting chain Option C)

Each scaffold WAS appropriate at scaffold time. Each became drift because nobody re-decided when production consumption began. **Discipline #13 (implicit-pillar drift) was authored thinking about CONCEPTUAL drift; the mechanical analog — SCAFFOLD VALUES that nobody re-decided — is the same failure mode in a different layer.**

Discipline #40 generalizes #39 (no-synthetic-stub-as-permanent-fallback; the specific synthetic_mode case) into the broader scaffold-as-drift pattern. Required for Cycle 14 Wave 5 production gauntlet pre-fire checklist per consolidated doc § 5.3.

**Sequencing:** parallel to KR scaffold-drift Dispatch 1 (substrate sidecar) + Dispatch 2 (Wave 1.5 — Matt-gated on class-roster sub-decision); non-gating Cycle 14 substantive work. **Pre-Wave-5 gating:** must close before Wave 5 production gauntlet so Wave 5's MIGRATION.md can use the discipline.

## Required reading before starting

- `canonical/00-ground-state.md` — ground-state oracle
- `agentic_orchestration/gandalf/notes/2026-05-27-scaffold-drift-recognition-and-corrective-package.md` § 4 (Discipline #40 candidate substantive spec)
- `agentic_orchestration/gandalf/notes/2026-05-27-scaffold-drift-kr-kicker.md` § 2 Dispatch 3 (this dispatch's routing source)
- `~/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md` — canonical target (your seam); particularly Disciplines #11, #13, #18, #39 for cross-reference composition
- `.claude/skills/reincarnated-jack-ryan-operating-procedure` (your OP)
- `.claude/skills/reincarnated-engineering-disciplines` (wrapper of current 39 disciplines)
- `.claude/skills/reincarnated-hive-mind-protocol`
- `.claude/skills/reincarnated-decision-log-format` (no decisions-log entry needed; this is engineering-disciplines.md canonical-write)

## Math-before-code

Not applicable — discipline ratification is canonical-write work, not math/code. However, the discipline's load-bearing claim is grounded in empirical evidence (the three concrete drift cases surfaced 2026-05-27 per consolidated doc § 1.2). Discipline #11 (empirical inspection over assumption) is the cross-reference for that grounding.

## Cross-seam contract change? (Principle 6 gate)

**NO** — discipline canonical writes are engineering-disciplines.md amendments, not code or schema. Round-trip not applicable. (Downstream consumers — all agents — read engineering-disciplines.md as authoritative; cross-seam impact lands at agent-discipline-citation time, not at canonical-write time. Operational hooks per § 4.3 apply to KR + jack-ryan workflow, not to inter-seam fixture dicts.)

## Scope

### Discipline #40 canonical-write

Author the entry at `~/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md` per consolidated doc § 4.1-4.4. Required content:

#### Statement (per § 4.1)

> **Discipline #40 — Scaffold values shipped to production-output paths require canonical decision before next wave fires.**
>
> When a Wave-N implementation introduces a hardcoded default (cohort size, chain count, tier count, per-class architecture, sampling distribution, etc.) into a code path that feeds production output artifacts, that default MUST either:
>
> - **(a)** be ratified as a canonical design lock in the appropriate canonical doc with explicit STATUS update, OR
> - **(b)** be flagged as `SCAFFOLD-WITH-PENDING-DECISION` in:
>   - the introducing wave's MIGRATION.md entry
>   - the roadmap (`canonical/02-roadmap.md` § 3 or equivalent)
>   - the next wave's dispatch as a gating decision
>
> **No "we shipped it so it's the design" inertia permitted.** A scaffold value passing Gate-2 does NOT ratify it as canonical.

#### Why this discipline is needed (per § 4.2)

Three concrete drift cases on 2026-05-27 demonstrate the failure mode (cite consolidated doc § 1.2 + each instance):
1. SC-6b enrichment + uniform substrate sampling
2. Cycle 13 gauntlet PASS criteria → 16-character de facto cohort
3. Wave 0.5 Track D minimum-viable per-skill emission

Each scaffold WAS appropriate at scaffold time. Each became drift because nobody re-decided.

#### Operational hooks (per § 4.3)

- **At dispatch authoring (KR):** out-of-scope section enumerates scaffold values introduced + names decision-required-before for each
- **At Gate-2 review (jack-ryan):** scaffold-flag verification added to checklist — "scaffold values in this wave: are they flagged per Discipline #40?"
- **At wave close (KR):** MIGRATION.md entry for the wave lists scaffold values with STATUS = RATIFIED-AS-CANONICAL OR SCAFFOLD-WITH-PENDING-DECISION
- **At roadmap update (KR):** § 3 production progress tracker shows scaffold-pending items as ⚠ visual flag

#### Cross-references (per § 4.4)

- **Discipline #11 (empirical inspection over assumption):** Discipline #40 is the temporal-axis composition — assumption that "scaffold becomes canonical by default" must be empirically tested at every wave-close
- **Discipline #13 (implicit-pillar drift):** Discipline #40 is the mechanical-value analog of #13's conceptual-pillar focus
- **Discipline #18 (math-before-code at hotspots):** Discipline #40 composes — math-notes that introduce scaffold values must include "this is scaffold; canonical decision required by Wave N" provenance
- **Discipline #39 (no-synthetic-stub-as-permanent-fallback):** Discipline #40 is the broader generalization — #39 covers the specific synthetic_mode case; #40 covers the general scaffold-as-drift pattern

#### Anchored examples

Three drift cases per consolidated doc § 1.2 + the meta-corrective sequencing per § 5 cross-referenced. Cite specific commits / lines where appropriate (e.g., `per_skill_emitter.py:L130-152` for Instance 3; `bc_target_subspace_generator.py:L173` for Instance 2; `substrate_weapon_binding.py:L238-269` for Instance 1).

## Acceptance criteria

- [x] Discipline #40 entry authored at `~/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md` with § Statement + § Why + § Operational hooks + § Cross-references
- [x] Cross-references to #11, #13, #18, #39 explicit + reciprocal where appropriate (e.g., if #13 should reference #40 as its mechanical-value analog, amend #13's entry accordingly)
- [x] Three anchored example cases per consolidated doc § 1.2 cited with specific commit/line provenance per Discipline #1.2 code-citation discipline
- [x] Engineering-disciplines.md commit + push per Matt 2026-05-27 per-cycle push pattern (auto-fire per CLAUDE.md addendum)
- [x] Completion record appended to this dispatch file
- [x] Round-trip: not applicable (no inter-seam fixture dict change)

## Out of scope (explicit non-goals)

- Do NOT amend the three concrete drift cases (substrate sidecar Dispatch 1 + Wave 1.5 Dispatch 2 are the remediation paths; this dispatch is the canonical-write only)
- Do NOT amend doc 40 / doc 46 / doc 47 / doc 41 (canonical commitments preserved; #40 is engineering-discipline scope only)
- Do NOT author decisions-log entry (per consolidated doc § 4 — engineering-disciplines.md is the authoritative target; not decisions-log)
- Do NOT enter DEV-MODE Gate-2 review (this is canonical-write work in discipline-ratification mode)
- Do NOT touch other queued disciplines (#33-#39 are RATIFIED via SC-1 at `d148808`)
- Do NOT author canonical doc updates outside engineering-disciplines.md (gandalf seam)

## Open questions for jack-ryan to resolve

- **Q-DISC40-1:** STATUS handling — is Discipline #40 LOAD-BEARING (like #39 per Matt Q4 emphatic lock) OR routine? Per consolidated doc § 5.3 pre-Wave-5 gating, #40 must close before Wave 5; that suggests LOAD-BEARING. Jack-ryan judgment + record rationale.
- **Q-DISC40-2:** Reciprocal cross-references — should Discipline #13 entry get amended to reference #40 as its mechanical-value analog? Jack-ryan judgment per engineering-disciplines.md canonical structure.
- **Q-DISC40-3:** Anchored examples — are the three concrete drift cases per consolidated doc § 1.2 sufficient OR should #40 anchor additional historical examples from prior cycles (e.g., Cycle 13 synthetic_mode → #39 lineage)?

## References

- `agentic_orchestration/gandalf/notes/2026-05-27-scaffold-drift-recognition-and-corrective-package.md` § 4 (substantive spec)
- `agentic_orchestration/gandalf/notes/2026-05-27-scaffold-drift-kr-kicker.md` § 2 Dispatch 3
- `~/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md` (canonical target)
- Engineering disciplines #11 + #13 + #18 + #39 (cross-reference targets)
- Hive-mind protocol § 4 (decision-routing) + § 2.2.2 (wave-entry-fire-discipline)
- `agentic_orchestration/cycles/cycle-14-cohesion-coalescence-scope.md` § 5 (load-bearing disciplines)

---

## Completion Record

**Completed:** 2026-05-27
**Agent:** jack-ryan
**Commit:** `b282966` (reincarnated-engine main)
**Pushed:** YES — per Matt 2026-05-27 per-cycle push pattern

### What landed

**Discipline #40 — Scaffold-values-require-canonical-decision** authored at:
`~/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md`

Entry includes:
- § Statement (verbatim per consolidated doc § 4.1)
- § Why this discipline is needed with three anchored instances (code-line provenance per Discipline #1.2):
  - Instance 1: `substrate_weapon_binding.py:L238-269` (uniform sampling scaffold)
  - Instance 2: `bc_target_subspace_generator.py:L173` (n_kits default; 16-char cohort drift)
  - Instance 3: `per_skill_emitter.py:L130-152` (3-chain 4-tier grid scaffold)
- § Operational hooks (dispatch authoring / Gate-2 checklist / wave-close MIGRATION.md status / roadmap visual flag)
- § Cross-references to #11, #13a, #18, #39 with explicit composition rationale per each
- § Composition with #39 (broader generalization)
- § Triggerable Gate-1 and Gate-2 questions

Reciprocal cross-reference added to Discipline #13a entry pointing to #40 as its mechanical-value analog.

Scope note + anatomy table at top of engineering-disciplines.md updated to reflect #40 landing.

### Open question resolutions

- **Q-DISC40-1: STATUS = LOAD-BEARING.** Rationale: pre-Wave-5 gating criterion (Wave 5 MIGRATION.md depends on this discipline per consolidated doc § 5.3); same authority class as #39 which was Matt Q4 emphatic lock. A discipline required as a pre-condition for the production gauntlet wave is by definition load-bearing.

- **Q-DISC40-2: Reciprocal cross-reference YES.** Amended #13a's cross-references section to add pointer to #40 as its mechanical-value analog. Rationale: #13a and #40 guard the same failure mode (implementation-vs-intent drift) at different observable surfaces — #13a at code-vs-doc comparison; #40 at wave-to-wave MIGRATION.md audit. Bidirectional citation makes both findable from either entry point and clarifies the relationship explicitly. The amendment is within jack-ryan's direct-approval authority (within-seam refinement of an existing entry; no API change to consumers).

- **Q-DISC40-3: Three concrete instances sufficient.** The three 2026-05-27 instances are empirically specific, code-cited, temporally current, and cover the three distinct scaffold types (sampling distribution / cardinality default / architecture scaffold). Adding historical examples from prior cycles would be padding — the discipline is grounded on fresh evidence and the "how to extend" protocol specifies to keep disciplines load-bearing and durable, not encyclopedic.
