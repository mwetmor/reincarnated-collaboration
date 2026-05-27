# Dispatch — 2026-05-27 — elrond — Cycle 14 Wave 1.5 Stage 1: class-roster substrate-evidence audit

**From:** knight-rider
**To:** elrond (data steward — catalogue DB + abstraction-analysis seam)
**Approved by:** Matt 2026-05-27 ratified **Option C** for class-roster sub-decision (substrate-evidence audit → gandalf design call) per scaffold-drift consolidated package § 3.5
**Estimated effort:** ~4-8 hours (substrate query + archetype-vocabulary extraction + candidate roster compilation)
**Acceptance:** archetype-vocabulary pool extracted from v1_scope substrate; candidate class-roster compiled with substrate-evidence anchoring; archetype + chain-count + supporting-chain candidates surfaced for gandalf Stage 2 design call

## Context

Matt 2026-05-27 ratified Option C (substrate-evidence audit → gandalf design call) over Option A (Cycle 13 16-archetype list) + Option B (gandalf-only 3-4 weeks design call). Option C composes with Path A substrate-led architectural commitment + Wave 1 BC-target review evidence already landed.

This is **Wave 1.5 Stage 1** — the substrate-evidence prerequisite for gandalf's Stage 2 class-roster design call. Stage 3 (rocket Wave 1.5 implementation) gates on Stage 2 output.

**Per consolidated doc § 3.5 Option C:** "Wave 1 BC-target review pulls archetype-vocabulary from substrate; gandalf curates class list." Wave 1's concentration architecture landed `98b68aa`; substrate's v1_scope content (2,293 rows; 5-family weapon-type taxonomy; primary_stat distribution DEX/STR/INT/WIS) is the evidence foundation.

**What this audit produces:** a candidate archetype-vocabulary pool drawn from substrate evidence, organized by:
- Primary stat family (STR / DEX / INT / WIS)
- Weapon-type family (martial-heavy / martial-light / ranged / caster-arcane / caster-faith)
- Named-template archetype evidence (mythological characters, historical archetypes encoded in named-template substrate entries)
- BC-axis coverage (which BC cells does each candidate archetype cover?)

**What this audit does NOT do:** select the final class roster, lock per-class chain counts, OR identify supporting chains — those are gandalf Stage 2 design-call territory. This is empirical evidence-gathering only.

## Required reading before starting

- `canonical/00-ground-state.md` — ground-state oracle
- `agentic_orchestration/gandalf/notes/2026-05-27-scaffold-drift-recognition-and-corrective-package.md` § 3 (Wave 1.5 substantive spec; § 3.5 Option C path)
- `agentic_orchestration/gandalf/notes/2026-05-27-scaffold-drift-kr-kicker.md` § 2 Dispatch 2 (Wave 1.5 routing source)
- `canonical/40-gear-balance-guide-architecture-2026-05-26.md` § 8.3 (variable 3-or-4 chains AMENDED 2026-05-27) + § 6.6.1 (supporting chain Option C; class-intrinsic)
- `canonical/46-concentration-architecture-2026-05-27.md` (Wave 1 architectural foundation)
- `agentic_orchestration/elrond/notes/2026-05-27-cycle-14-sc-6-substrate-weapon-audit.md` (substrate composition reference; primary_stat + weapon_type_family distributions)
- `agentic_orchestration/elrond/notes/2026-05-27-cycle-14-sc-6b-substrate-enrichment-implementation.md` (SC-6b enrichment values; per-family L50 baselines)
- Cycle 13 archetype roster reference: `~/Games/reincarnated-engine/output/cycle-13-mechanical-season-001/characters/` — 16 character names (`S1_endgame_dex_01_dagger_assassin` etc.); use as INFORMATIONAL only (Q9 disregarded for Cycle 14; this audit produces FRESH evidence)
- `.claude/skills/reincarnated-elrond-operating-procedure`
- `.claude/skills/reincarnated-hive-mind-protocol`
- `.claude/skills/reincarnated-substrate-vector-cheatsheet` (BC axes for archetype cross-axis coverage analysis)

## Math-before-code

Not applicable directly — this is empirical-evidence gathering, not algorithmic. However, the audit deliverable is an INPUT to gandalf's Stage 2 design call, which IS a design-spec authoring math-note territory. Stage 1 produces the substrate evidence; Stage 2 produces the canonical design-spec.

## Cross-seam contract change? (Principle 6 gate)

**NO** — audit-only; no DB write; no schema change; no inter-seam fixture dict change. Round-trip not applicable.

## Scope

### Item 1 — Substrate archetype-vocabulary extraction (~2-4 hrs)

- [ ] Query v1_scope substrate for `named_template` + `unique` rows (carry mythological/historical archetype evidence per SC-6 audit; ~969 candidate-rich rows)
- [ ] Per row: extract `canonical_name` + `weapon_type_family` + `primary_stat` + `named_mythological_match` + `cultural_lineage_canonical` + `register_canonical`
- [ ] Cluster archetype-vocabulary candidates by:
  - Primary stat family (4 buckets: STR / DEX / INT / WIS)
  - Weapon-type family (5 buckets per SC-6b weapon_type_family enum)
  - Cultural lineage / register (cross-cutting taxonomy from SC-6 audit § 1.4 enrichment columns)
- [ ] Surface ~30-50 candidate archetype seeds with substrate-evidence anchoring (e.g., "Berserker — STR + martial-heavy + 47 substrate rows of two-handed great-weapon named templates spanning European/Norse/Slavic lineage")

### Item 2 — BC-axis coverage cross-reference (~1-2 hrs)

- [ ] For each candidate archetype seed, identify BC-axis coverage:
  - Engagement profile (melee / mid / ranged)
  - Damage geometry (point / line / arc_sweep / cone_aoe / etc.)
  - Damage tempo (fast / measured / slow / channeled)
  - Stat affinity (STR / DEX / INT / WIS)
  - Proxy density (low / medium / high)
  - Other BC axes per substrate-vector cheatsheet § 1
- [ ] Surface BC-cell coverage gaps (cells with no candidate archetype) AND BC-cell over-saturation (cells with many candidates competing)
- [ ] This informs gandalf Stage 2 — which archetypes fill which BC cells; which need design synthesis vs which are over-represented

### Item 3 — Chain-count + supporting-chain candidate evidence (~1-2 hrs)

- [ ] For each candidate archetype, surface evidence on:
  - **Chain count candidates (3 or 4)** — does the archetype's substrate naturally suggest 3 chains (e.g., melee + ranged hybrid like a Ranger) OR 4 chains (e.g., specialist with broad utility like a Mage)? Evidence from substrate weapon-kind variety + tier coverage.
  - **Supporting chain candidates** — what's the class-intrinsic passive theme that absorbs into supporting chain (per doc 40 § 6.6.1 Option C)? Substrate evidence: shared aesthetic / tone / register across the archetype's substrate row cluster.
- [ ] Note: this is EVIDENCE for gandalf's Stage 2 design call, NOT a final per-class decision. Gandalf reads + curates.

### Item 4 — Audit report

- [ ] File audit report at `agentic_orchestration/elrond/notes/2026-05-27-cycle-14-wave-1-5-class-roster-substrate-audit.md`
- [ ] Required sections:
  - § 1 Substrate evidence overview (counts; distributions; coverage)
  - § 2 ~30-50 candidate archetype seeds with substrate anchoring
  - § 3 BC-axis coverage cross-reference + gaps + over-saturation
  - § 4 Chain-count + supporting-chain candidate evidence per archetype
  - § 5 Recommended Stage 2 design-call agenda (questions for gandalf to answer)
- [ ] Cross-reference SC-6 audit + SC-6b enrichment + Wave 1 BC-target review + doc 40 § 8.3 + § 6.6.1

### Closure

- [ ] Append completion record to this dispatch
- [ ] Commit + push per Matt 2026-05-27 per-cycle push pattern (auto-fire per CLAUDE.md addendum)
- [ ] Note: when this dispatch lands, KR authors Stage 2 (gandalf class-roster design call dispatch) + Stage 3 (rocket Wave 1.5 implementation dispatch); Gate-1 routing follows

## Acceptance criteria

- [ ] Audit report filed at the specified path with all 5 sections
- [ ] ~30-50 candidate archetype seeds surfaced with substrate-evidence anchoring per archetype
- [ ] BC-axis coverage cross-reference complete; gaps + over-saturation identified
- [ ] Chain-count + supporting-chain candidate evidence surfaced per archetype
- [ ] Stage 2 design-call agenda recommended (questions for gandalf)
- [ ] No DB schema changes; no canonical doc amendments (gandalf seam for canonical work)
- [ ] Completion record appended; commit + push

## Out of scope (explicit non-goals)

- Do NOT select the final class roster (gandalf Stage 2 territory)
- Do NOT lock per-class chain counts (gandalf Stage 2)
- Do NOT identify final supporting-chain identities (gandalf Stage 2 design call)
- Do NOT amend doc 40 / doc 46 / doc 47 (gandalf canonical seam)
- Do NOT touch substrate library DB (audit only)
- Do NOT touch character JSON output schema (rocket Stage 3 territory)
- Do NOT enter Wave 1.5 implementation scope (Stage 3 / rocket)
- Do NOT reproduce Cycle 13 16-archetype roster as the candidate pool (Q9 DISREGARD; Option A explicitly rejected)
- Do NOT block on Wave 1 Gate-2 review (firing in parallel; substrate audit is read-only)

## Open questions for elrond

- **Q-W15-S1-1:** Candidate archetype count — is ~30-50 the right pool size? Smaller (~20) for tighter gandalf curation; larger (~80) for broader design surface. Elrond decides per substrate evidence + records rationale.
- **Q-W15-S1-2:** BC-axis coverage — should the audit prioritize cells that the Cycle 13 cohort FAILED to cover (per gauntlet sim PASS criteria 16-of-18 cells)? OR comprehensive coverage regardless? Elrond's call per substrate evidence; document either way.
- **Q-W15-S1-3:** Cultural lineage / register filtering — should the audit surface lineage-balanced candidates (e.g., not 80% European) OR substrate-natural distribution (whatever the library skews to)? Elrond decides + records rationale; gandalf can refine at Stage 2.
- **Q-W15-S1-4:** Named-template vs category — does the audit prioritize named-template rows (carry archetype identity by name) OR include category rows (broader weapon-type vocabulary)? Likely named-template primary + category as supporting evidence; elrond confirms.

## References

- `agentic_orchestration/gandalf/notes/2026-05-27-scaffold-drift-recognition-and-corrective-package.md` § 3 + § 3.5 (Wave 1.5 substantive + Option C path)
- `agentic_orchestration/elrond/notes/2026-05-27-cycle-14-sc-6-substrate-weapon-audit.md` (substrate composition)
- `agentic_orchestration/elrond/notes/2026-05-27-cycle-14-sc-6b-substrate-enrichment-implementation.md` (SC-6b enrichment values)
- `canonical/40-gear-balance-guide-architecture-2026-05-26.md` § 8.3 + § 6.6.1 (chain count + supporting chain)
- `canonical/46-concentration-architecture-2026-05-27.md` (Wave 1 foundation)
- Substrate-vector-cheatsheet skill (BC axes for archetype cross-axis coverage)
- Engineering disciplines #11 + #18 + #40 (LOAD-BEARING)
- Hive-mind protocol § 4 (decision-routing) + § 2.2.2 (wave-entry-fire-discipline)

## Sequencing note

After this dispatch lands, KR authors:

- **Stage 2 dispatch (gandalf class-roster design call)** consuming elrond Stage 1 audit; gandalf curates canonical class roster from substrate evidence + authors per-class chain count + supporting chain identity + active T4 mechanism design-spec; also authors doc 41 § 4 season cardinality amendment (n_kits=40 default per consolidated doc § 3.4)
- **Stage 3 dispatch (rocket Wave 1.5 implementation)** consuming Stage 2 design-spec + math-notes; implements per consolidated doc § 3.3 items 1-5 (chain count + T4 count rule + supporting chain + branching + active T4 marker)

Stage 1 → Stage 2 → Stage 3 sequential per Option C path.
