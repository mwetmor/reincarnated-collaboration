# Dispatch — 2026-05-26 — rocket — Cycle 13 GAP 5 Trait Constellation Audit

**From:** knight-rider
**To:** rocket
**Approved by:** Matt 2026-05-26 (via Cycle 13 framing brief Q3 scope-of-autonomy KR § 4.1 + pre-launch design session-start doc Block D GAP 5 audit input)
**Estimated effort:** 2-4 hrs audit (Pattern A subagent-sized)
**Acceptance:** audit memo at `agentic_orchestration/rocket/notes/2026-05-26-trait-constellation-audit-gap-5.md` covering current trait pool coverage vs expected for v1; gap identification; recommendation (expand-in-Cycle-13 vs sufficient-for-first-season)

## Context

Pre-launch design session-start doc (Block D — audit + verification) lists 4 audit items where the session needs CURRENT-STATE empirical inputs before Matt + gandalf can decide. GAP 5 is trait constellation completeness:

> **Trait constellation completeness** (GAP 5) — Audit current trait pool against expected coverage; identify gaps; decision whether trait pool needs expansion in Cycle 13 OR is sufficient for first season

Per project_trait_architecture.md (memory file): the design specifies per-class intrinsic trait pool (5-10 traits per class, floors at L1/12/25/38, converge at L50) + gear-affix rolls (element/mechanic-gated, no skill-specific on gear). Cycle 13 builds spec-driven gear gen with rarity escalation + capability toolkit; trait coverage interacts with kit composition (Phase 2a) + gear partition (Wave 1).

Question for the audit: does the v2_narrow / v1_scope trait pool COVER the expected per-class intrinsic trait surface? If gaps exist, can they be filled at Cycle 13 OR should they defer?

This is read-and-report audit — no engine modification. Output feeds Block D verification (Matt + gandalf decision).

## Required reading before starting

1. `canonical/00-ground-state.md` (current epoch + Cycle 13 scope)
2. `~/.claude/projects/-Users-admin-Games-reincarnated-collaboration/memory/project_trait_architecture.md` (canonical trait architecture; per-class intrinsic + gear-affix dual source)
3. `canonical/historical/32-progression-design.md` (predecessor; some entries LOCKED stand)
4. `canonical/historical/33-progression-skeleton.md` (locked-only summary of 32)
5. `canonical/40-gear-balance-guide-architecture-2026-05-26.md` § 3 (gear gen) — trait interaction with gear affixes
6. `agentic_orchestration/gandalf/notes/2026-05-26-cycle-13-pre-launch-design-session-start.md` § 2 Block D + GAP 5 framing
7. Current generation code: `reincarnated-engine/src/reincarnated/generation/` — locate trait pool definitions + trait emission logic (rocket-seam owned)
8. Most recent v2_narrow form output: spot-check what traits land in actual generated kits (cite specific kits)

## Math-before-code (audit; no code)

NOT applicable — audit + reporting only. No engine modifications. No regen.

## Cross-seam contract change? (Principle 6 gate)

**Round-trip: not applicable — no cross-seam contract change in this dispatch.** Audit memo is a design-input artifact for Block D verification; no schema / fixture / boundary change.

## Scope

### Audit dimensions

- [ ] **Current trait pool enumeration:** for each v1_scope class (or class-set if classes aren't named yet), list the trait pool currently defined in generation code (path + line number citations per Discipline #1.2)
- [ ] **Per-class trait count:** target = 5-10 per class per memory architecture; report actual counts; flag classes outside band
- [ ] **Floor coverage:** target = L1 / L12 / L25 / L38 floors with L50 convergence per memory architecture; report which floors are present per class; flag missing floors
- [ ] **Trait taxonomy coverage:** what TYPES of traits exist? (offensive multipliers / defensive mitigations / resource modifiers / mobility / utility / on-trigger / etc.); report distribution per class
- [ ] **Gear-affix trait surface:** per memory architecture "gear-affix rolls (element/mechanic-gated)"; report current gear-affix trait pool (if any exists for v1_scope); flag what's defined vs not
- [ ] **Empirical emission in v2_narrow:** spot-check 5-10 v2_narrow forms — what traits actually emit in production output? (sanity check: defined ≠ used)
- [ ] **Per-class intrinsic vs gear-affix interaction:** verify per memory architecture that per-class intrinsic and gear-affix sources rank-stack correctly; flag if intrinsic and affix collide or duplicate
- [ ] **Coverage vs Cycle 13 needs:** for each Wave 2 kit composition need (T4 algorithm Phases 1-2 implement chains), does trait coverage support the kit compositions expected?

### Audit output

- [ ] Audit memo at `agentic_orchestration/rocket/notes/2026-05-26-trait-constellation-audit-gap-5.md` with:
  - § 1 TL;DR (gap count + severity)
  - § 2 Current state per dimension above
  - § 3 Expected coverage per memory + doc 40 + framing brief
  - § 4 Gap identification (concrete: "Class X is missing L25 floor"; "Class Y has only 3 traits but target is 5-10")
  - § 5 Recommendation (expand-in-Cycle-13 with specific work-unit OR sufficient-for-first-season with rationale OR partial — name what's blocking-vs-non-blocking)
  - § 6 Source citations per dimension (file + line number per Discipline #1.2)

## Acceptance criteria

- [ ] Audit memo authored at the specified path
- [ ] All 8 audit dimensions covered with empirical data
- [ ] Source citations per dimension per Discipline #1.2
- [ ] Recommendation is explicit + actionable (not "needs more research")
- [ ] Memo length ~3-6 pages (proportional to actual gap surface — if gaps are minimal, memo can be shorter)
- [ ] **Empirical-count discipline per WARN-pattern note (per skill_handoff_2026-05-25 § 1 Priority 2):** post-script empirical count assertions pasted as evidence — "I cite 7 classes in trait pool; verified by grep `<file>` showing 7 entries" — to avoid Discipline #11 instrumentation gap pattern
- [ ] Round-trip: not applicable — no cross-seam contract change

## Out of scope (explicit non-goals)

- Modifying trait pool definitions (audit only; expansion is separate Cycle 13 work-unit if recommended)
- Modifying generation code
- Regenerating v2_narrow or any other generation output
- Authoring canonical doc updates (memo is in `rocket/notes/`, not `canonical/`)
- Recommending specific traits to add (audit identifies gaps; gandalf design decisions fill them)
- Trait pool expansion implementation work (Cycle 13 wave dispatch if Matt + gandalf decide expand-in-Cycle-13)

## Open questions for the agent to resolve

- Class-set granularity — if classes aren't formally named in v1_scope yet, audit at the "class-archetype" or "kit-family" level (whatever granularity v2_narrow emits)
- Coverage-vs-design tradeoff — if a class has 3 traits where target is 5-10 BUT the kit composition seems to work fine in v2_narrow, flag as "low-priority-gap" vs "load-bearing-gap"
- Empirical spot-check sample size — 5-10 v2_narrow forms recommended; adjust if pattern is obvious at smaller sample

## References

- `~/.claude/projects/-Users-admin-Games-reincarnated-collaboration/memory/project_trait_architecture.md` (canonical trait architecture)
- `canonical/historical/32-progression-design.md` (predecessor design)
- `canonical/40-gear-balance-guide-architecture-2026-05-26.md` § 3 (gear-affix interaction)
- `agentic_orchestration/gandalf/notes/2026-05-26-cycle-13-pre-launch-design-session-start.md` § 2 Block D (audit framing)
- `agentic_orchestration/skill_handoff_2026-05-25.md` § 1 Priority 2 (WARN-pattern context — empirical-count discipline)
- `~/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md` #1.2 (code-citation discipline) + #11 (empirical inspection over assumption)

---

**Cycle:** 13
**Wave:** 0 / Block D feed-in
**Gates:** Block D verification in pre-launch design session
**Priority:** P5 — fire parallel; quick turnaround
