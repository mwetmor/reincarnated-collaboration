# Dispatch — 2026-05-27 — rocket — Cycle 14 Wave 1.5 Stage 3: Skill-Tree Architecture implementation

**From:** knight-rider
**To:** rocket (engine content-generation seam owner; primary implementer)
**Approved by:** Matt 2026-05-27 ratified Option C (substrate-evidence → gandalf design call → rocket impl) per scaffold-drift consolidated package § 3.5
**Estimated effort:** ~1 week anchor (per framing brief Q10 quality > timeline; extends as needed)
**Acceptance:** Wave 1.5 implementation per doc 48 § 7 + consolidated doc § 3.3 items 1-5; 10-class roster registry data; per-class chain count + T4 count rule + supporting chain + branching + active T4 marker; n_kits=40 default per doc 41 § 4.6 amendment; jack-ryan Gate-2 PASS; cross-seam round-trip with gamora damage_resolver

## Context

Wave 1.5 Stages 1 + 2 landed clean 2026-05-27:
- **Stage 1 (elrond):** substrate class-roster audit at `06a3b7f`; 34 archetype seeds + BC-axis coverage + chain-count vote (~65% 3-chain natural) + 14 questions
- **Stage 2 (gandalf):** 10-class canonical roster at `6a28e39`; **canonical doc 48 authored** (`canonical/48-cycle-14-class-roster-2026-05-27.md`); doc 41 § 4.6 season cardinality amendment landed (n_kits=40 default); 17 Q-resolutions

**This is Wave 1.5 Stage 3** — rocket implementation consuming doc 48 § 7 implementation guidance + 17 Q-resolutions + consolidated doc § 3.3 items 1-5.

**Canonical class roster (per doc 48 § 1):**

| # | Class | Stat | Chain count | T4 capstones |
|---|---|---|---|---|
| 1 | Barbarian | STR | 3 | 2 |
| 2 | Hoplite | STR | 3 | 2 |
| 3 | Siege-Master | STR | 3 | 2 |
| 4 | Assassin | DEX | 3 | 2 |
| 5 | Duelist | DEX | 3 | 2 |
| 6 | Wildhunter | DEX | 3 | 2 |
| 7 | **Gunslinger** | DEX | **4** | 3 |
| 8 | Skirmisher | DEX | 3 | 2 |
| 9 | Magus | INT | 3 | 2 |
| 10 | **Crusader** | WIS | **4** | 3 |

8 × 3-chain + 2 × 4-chain; aggregate 22 T4 capstones + 10 supporting chains + 38 total chains.

**Discipline #40 LOAD-BEARING:** class roster is CANONICAL LOCK per doc 48 § 0; rocket Stage 3 implementation consumes from doc 48 as input; NOT scaffold-with-pending-decision.

**Composition with caster-faith HYBRID** (Matt approved `37479dc` + Interpretation III locked): Crusader class composes with HYBRID Wave 2 Path B (Fix B-prime within-caster-shape sampling) — Wave 2 dispatch bundles Fix B + Fix B-prime per gandalf verdict `38d0d73`. Stage 3 implementation does NOT include Fix B-prime (Wave 2 scope); Crusader Wave 1.5 implementation operates on current substrate sampling (mace-heavy until Fix B-prime lands in Wave 2).

**Pre-Wave-5 prerequisite:** Wave 1.5 Stage 3 close is item #3 of 5 (Fix A ✅ / Fix B math-note ✅ / Wave 1.5 ⬅ Stage 3 / season cardinality bundled via doc 48 / Discipline #40 ✅).

## Required reading before starting

- `canonical/00-ground-state.md` — ground-state oracle
- `canonical/48-cycle-14-class-roster-2026-05-27.md` — **PRIMARY SUBSTANTIVE INPUT** (10-class roster + § 2 per-class chain architecture + § 2.3 active T4 mechanism design-spec + § 7 implementation guidance)
- `agentic_orchestration/elrond/notes/2026-05-27-cycle-14-wave-1-5-class-roster-substrate-audit.md` (Stage 1 substrate evidence)
- `canonical/41-progression-framework-2026-05-27.md` § 4.6 (season cardinality amendment; n_kits=40 default)
- `canonical/40-gear-balance-guide-architecture-2026-05-26.md` § 8.3 + § 6.6.1 + D66 + D69 + D83
- `canonical/46-concentration-architecture-2026-05-27.md` (Wave 1 architectural foundation; landed `98b68aa`)
- `canonical/47-damage-scaling-architecture-2026-05-27.md` § 3 + § 4.1 (per-attribute weapon profile; T4 damage routing)
- `agentic_orchestration/gandalf/notes/2026-05-27-scaffold-drift-recognition-and-corrective-package.md` § 3.3 (Wave 1.5 5-item scope)
- `~/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md` Discipline #40 (LOAD-BEARING; `b282966`) + #1 + #1.2 + #11 + #18 + #33 + #34
- `~/Games/reincarnated-engine/src/reincarnated/generation/per_skill_emitter.py` L130-152 (primary touch surface)
- `~/Games/reincarnated-engine/src/reincarnated/generation/bc_target_subspace_generator.py` L173 (n_kits default touch surface)
- `.claude/skills/reincarnated-rocket-operating-procedure`
- `.claude/skills/reincarnated-hive-mind-protocol`
- `.claude/skills/reincarnated-engineering-disciplines`

## Math-before-code

Per Discipline #18 + #1, **3 math-notes required** BEFORE implementation per consolidated doc § 3.3:

1. **Class-chain architecture math-note** at `~/Games/reincarnated-engine/src/reincarnated/generation/math/wave-1-5-class-chain-architecture-math.md` documenting:
   - Per-class chain_count + T4_count = chain_count − 1 rule (D83) per doc 48 § 2.1 table
   - Supporting chain identification per class per doc 48 § 2.2 (10 distinct identities)
   - Class-roster registry data structure
   - Discipline #1.2 code-citation discipline (cite `file.py:NNN` for emission claims)

2. **Branching math-note** at `~/Games/reincarnated-engine/src/reincarnated/generation/math/wave-1-5-branching-math.md` documenting:
   - D69 depth-≥4 branching rule (wide-vs-tall lever)
   - Per-class chain depth assignment (per doc 48 § 2.1 target depth column)
   - Branch consumption rules (T2 or T3 split into 2 parallel sub-paths consuming same T-tier)
   - Node-count accounting (3-chain class with depth-6 chains has more wide-vs-tall lever than 4-chain class with depth-3 chains)

3. **Active T4 runtime math-note** at `~/Games/reincarnated-engine/src/reincarnated/generation/math/wave-1-5-active-t4-runtime-math.md` documenting:
   - D66 runtime-active marker (`active_t4_chain: str | None`)
   - Switching mechanism via legendary-trigger respec per D65
   - Validation rules per doc 48 § 2.3 (only one T4 capstone active; supporting chain has no T4; non-active T4 chains' T1-T3 always active)
   - Default `active_t4_chain` at character creation (gandalf doc 48 § 2.3 design-spec)

Math-notes are jack-ryan Gate-1 inputs.

## Cross-seam contract change? (Principle 6 gate)

**YES** — character JSON schema adds 3 new fields per doc 48 § 7.1 + consolidated doc § 3.6:

- `active_t4_chain: str | None` (runtime-active marker per D66)
- `supporting_chain: str` (T3-cap class-intrinsic chain identifier)
- `class_archetype: str` (class registry reference; one of the 10 doc-48-locked names)

**MIGRATION.md REQUIRED** per ADR-004 at `~/Games/reincarnated-engine/src/reincarnated/generation/MIGRATION.md § Wave 1.5` capturing:
- 3 new character JSON fields + downstream consumer expectations
- gamora damage_resolver consumes `active_t4_chain` for T4 damage routing per doc 47 § 4.1
- star-lord Track C transform (Wave 5+) consumes new fields for loadout export schema
- drax loadout app skill-tree rendering (Wave 5+) consumes for class display
- Round-trip clause: "rocket Stage 3 per-class emission → character JSON contains `active_t4_chain` + `supporting_chain` + `class_archetype` fields populated per doc-48-locked class roster; gamora damage_resolver routes T4 damage per `active_t4_chain`; star-lord + drax consume cleanly."

## Scope

### Pre-implementation

- [ ] Author 3 math-notes per § Math-before-code above
- [ ] Apply Discipline #1.2 code-citation discipline (cite `file.py:NNN` for all "X applied at stage Y" claims)
- [ ] Route 3 math-notes to jack-ryan Gate-1 DESIGN-MODE review WITHIN your session per dispatch convention
- [ ] Pattern-A query to gandalf (optional): supporting chain identity edge cases (per doc 48 § 2.2)

### Item 1 — Class roster registry data (~1 day)

- [ ] Author class-roster registry data structure (10 entries per doc 48 § 1; one per class)
- [ ] Per-class fields: `class_archetype` + `primary_stat` + `chain_count` + `t4_chain_ids` (2 or 3 IDs) + `supporting_chain_id` + `target_chain_depth` + `substrate_weapon_binding_hints` (primary_stat + weapon_type_family preference list per doc 48 § 1)
- [ ] Persistent location: rocket OP convention (likely `~/Games/reincarnated-engine/src/reincarnated/generation/class_roster.py` or equivalent; rocket decides per OP)
- [ ] Smoke: registry has 10 entries; cross-check class names + chain counts against doc 48 § 1 table

### Item 2 — Per-class chain count + T4 count rule + supporting chain (~2-3 days)

- [ ] Amend `per_skill_emitter.py` L130-152 REPLACE hardcoded `chains = ["chain_A", "chain_B", "chain_C"]` + `tiers_per_chain = [1, 2, 3, 4]` flat grid with per-class chain_count + per-chain T4-eligibility flag + per-chain target depth + supporting-chain T3-cap enforcement
- [ ] Replace `_CHAIN_ROLE` flat role-per-tier mapping with per-class supporting-chain role identification + T4 capstone gating per active_t4_chain runtime marker
- [ ] Emission rule: T4 capstones emit ONLY on chains in `t4_chain_ids` list; supporting chain caps at T3 (no T4 capstone)
- [ ] Per-class kit emission produces correct chain count (3 for 8 classes; 4 for Gunslinger + Crusader) + correct T4 count (chain_count − 1 per D83)
- [ ] Smoke: 10-class roster × 4 kits per class = 40-kit test season; verify chain count + T4 count per class matches doc 48 § 1 + § 2.1

### Item 3 — Depth-≥4 branching (~1-2 days)

- [ ] Implement D69 depth-≥4 branching rule
- [ ] Per-class chain depth assignment per doc 48 § 2.1 (target depth column)
- [ ] Branch points: T2 or T3 splits into 2 parallel sub-paths consuming same T-tier
- [ ] At least one test class demonstrates a branched chain (per gandalf design-spec; coordinate Pattern-A if uncertain which class gets branching for v1)
- [ ] Branch consumption rules clear in math-note + code comment
- [ ] Smoke: branched chain test produces parallel sub-path skills; node count math correct

### Item 4 — Active T4 runtime marker (~1-2 days)

- [ ] Add `active_t4_chain: str | None` field to character JSON schema (per doc 48 § 2.3 + § 7.1)
- [ ] Add `supporting_chain: str` field to character JSON schema
- [ ] Add `class_archetype: str` field to character JSON schema
- [ ] Default `active_t4_chain` at character creation per doc 48 § 2.3 design-spec (gandalf may have specified — if not, Pattern-A query to gandalf)
- [ ] Validation rules per doc 48 § 2.3:
  - Only one T4 capstone active at any moment
  - Supporting chain has NO T4 capstone
  - Non-active T4 chains' T1-T3 skills are ALWAYS active (only T4 capstone gated)
  - Supporting chain skills are ALWAYS active (not gated by `active_t4_chain`)
- [ ] Switching mechanism (D65 legendary-trigger respec) — implementation depth: stub-level interface OR full implementation per rocket judgment + doc 48 § 2.3
- [ ] Smoke: test character with active_t4_chain = chain_A; switch to chain_B; verify previously-active T4 capstone deactivates + new T4 capstone activates; T1-T3 of both chains remain active

### Item 5 — Season cardinality n_kits=40 (~1 hr)

- [ ] Amend `bc_target_subspace_generator.py` L173: `def generate(self, n_kits: int = 40)` (was 22)
- [ ] Multi-fire extension cap 50 preserved per doc 48 § 6.3
- [ ] Smoke: test season generation with default n_kits=40

### Closure

- [ ] generation/MIGRATION.md § Wave 1.5 authored per § Cross-seam contract above
- [ ] generation/AGENT_STATE.md updated
- [ ] Cross-seam round-trip smoke: 40-kit test season → 10-class roster correctly emitted per class; per-class chain count + T4 count correct; active_t4_chain populated; supporting_chain populated; class_archetype populated
- [ ] jack-ryan Gate-2 review of Wave 1.5 Stage 3 outputs (verify class roster locked-in; Discipline #40 compliance; cross-seam round-trip)
- [ ] Tag: `rocket/v1.5-wave-1-5-skill-tree-architecture` (or rocket-OP-preferred)
- [ ] Append completion record to dispatch
- [ ] Commit + push per Matt 2026-05-27 per-cycle push pattern (auto-fire per CLAUDE.md addendum)

## Acceptance criteria

- [ ] 10-class roster registry data implemented per doc 48 § 1; smoke confirms all 10 entries with correct chain_count + supporting_chain
- [ ] Per-class chain count + T4 count rule (D83) implemented; 40-kit test season produces correct chain count per class (8 classes × 3 chains + 2 classes × 4 chains = 38 total chains; 22 T4 capstones)
- [ ] Supporting chain (T3-cap, class-intrinsic per doc 48 § 2.2) implemented; supporting chain has no T4 capstone
- [ ] Depth-≥4 branching implemented; at least one test class demonstrates branched chain
- [ ] Active T4 runtime marker implemented; switching mechanism produces expected behavior per doc 48 § 2.3
- [ ] n_kits=40 default per doc 41 § 4.6 amendment
- [ ] Character JSON schema adds `active_t4_chain` + `supporting_chain` + `class_archetype` fields
- [ ] MIGRATION.md § Wave 1.5 authored
- [ ] AGENT_STATE.md updated
- [ ] 3 math-notes authored + jack-ryan Gate-1 PASS pre-implementation
- [ ] jack-ryan Gate-2 PASS post-implementation; Discipline #40 compliance verified
- [ ] Cross-seam round-trip smoke: 40-kit test season produces 10-class output with all new fields populated
- [ ] Completion record appended; commit + push + tag

## Out of scope (explicit non-goals)

- Do NOT implement Wave 2 Layer 5 / Layer 8 / Layer 9 (Wave 2 scope per scope-doc § 6)
- Do NOT implement Fix B-prime caster-faith mace dial-back (Wave 2 scope per gandalf HYBRID verdict `38d0d73` + Matt approval `37479dc`)
- Do NOT touch damage_resolver / fight engine (gamora seam; consumes `active_t4_chain` at runtime)
- Do NOT touch substrate library DB (elrond seam)
- Do NOT amend doc 40 / doc 46 / doc 47 / doc 41 / doc 48 (gandalf canonical seam; doc 48 IS the canonical input)
- Do NOT implement per-level scaling formulas (deferred per doc 41 § 4 #1)
- Do NOT regress Wave 1 outputs (concentration architecture Layers 1-4+7 landed at `98b68aa`)
- Do NOT regress synthetic_mode (Discipline #39 LOAD-BEARING; RETIRED at Wave 0.5)
- Do NOT close BC-cell gaps deferred to v1.1 per doc 48 § 3.2 (INT-AoE / INT-high-tempo / WIS-high-tempo / WIS-melee-light / STR-thrown-ranged / multi-spawn summoner)
- Do NOT close substrate-enrichment commissions deferred per doc 48 § 5 (Q-S2-12/13/14 — Cycle 15 queue per HYBRID approval `37479dc`)
- Do NOT include cross-attribute hybrid classes (Q-S2-11 deferred per doc 48; v1.1 scope)

## Open questions for rocket

- **Q-W15-S3-1:** Default `active_t4_chain` at character creation — does doc 48 § 2.3 specify OR does rocket Pattern-A query gandalf? If doc 48 doesn't specify, recommend default = first T4 chain ID in `t4_chain_ids` list (deterministic + reproducible).
- **Q-W15-S3-2:** Which class gets branching for v1 demonstration (per Item 3)? Cleanest fit per doc 48 § 2.1 target depth column likely indicates; rocket Pattern-A to gandalf if uncertain.
- **Q-W15-S3-3:** Legendary-trigger respec mechanism implementation depth — stub-level interface (just supports active_t4_chain swap; no UI / cost / cooldown) OR full implementation? Stub is acceptable for Wave 1.5; full implementation Wave 4+ alongside acquisition curve calibration. Rocket decides + records rationale.
- **Q-W15-S3-4:** Class roster registry persistent location — `class_roster.py` OR yaml config OR class metadata in existing seasonal_generator? Rocket decides per OP convention.

## References

- `canonical/48-cycle-14-class-roster-2026-05-27.md` (PRIMARY input; especially § 1 + § 2 + § 7)
- `canonical/41-progression-framework-2026-05-27.md` § 4.6 (season cardinality amendment)
- `canonical/40-gear-balance-guide-architecture-2026-05-26.md` § 8.3 + § 6.6.1 + D66 + D69 + D83
- `canonical/46-concentration-architecture-2026-05-27.md`
- `canonical/47-damage-scaling-architecture-2026-05-27.md` § 3 + § 4.1
- `agentic_orchestration/elrond/notes/2026-05-27-cycle-14-wave-1-5-class-roster-substrate-audit.md` (Stage 1 substrate evidence)
- `agentic_orchestration/gandalf/notes/2026-05-27-scaffold-drift-recognition-and-corrective-package.md` § 3.3
- `~/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md` (Discipline #40 LOAD-BEARING `b282966` + #1 + #1.2 + #11 + #18 + #33 + #34)
- Engineering disciplines #1 + #1.2 + #11 + #18 + #33 + #34 + #38 + #40
- Hive-mind protocol § 4 (decision-routing) + § 2.2.2 (wave-entry-fire-discipline) + § 7 (math hotspots)

## Sequencing note

After Stage 3 lands, Wave 1.5 CLOSED. Then KR authors:

- **Wave 2 dispatch** (concentration architecture Layers 5+8+9 + Fix B + Fix B-prime composed per gandalf HYBRID verdict `38d0d73` + Matt approval `37479dc`) — gates: Wave 1 ✅ + Wave 1.5 close + gamora baseline measurement (per jack-ryan Gate-2 Wave 1 closure carry-forward)
- **Wave 3 dispatch** (Phase 5 cohesion-judge LLM; gandalf primary + star-lord + rocket; SC-3 Pattern B PRIMARY recommendation) — gates: Wave 0.5 ✅ + SC-3 ✅; CAN fire parallel with Wave 2

Cycle 14 substrate state at Stage 3 firing time:
- Wave 0 / Wave 0.5 / Wave 0.5 follow-on / Wave 1 / Substrate sidecar / Discipline #40 / Matt class-roster gate / caster-faith HYBRID + Interpretation III — all ✅ CLOSED OR APPROVED
- Wave 1.5 Stage 1 ✅ / Stage 2 ✅ / Stage 3 ← THIS DISPATCH
- Wave 2 + Wave 3 + Wave 4 + Wave 5 queued

Pre-Wave-5 checklist post Stage 3 close: 4 of 5 closed (Fix A ✅ / Fix B math-note ✅ / Wave 1.5 ✅ / Discipline #40 ✅); season cardinality landed via doc 48 § 6 (bundled into Stage 2 close).

---

## Completion record

**Completed by:** rocket
**Date:** 2026-05-27
**Duration:** Single session

### Status: COMPLETE

### Items completed

- [x] 3 math notes authored (class-chain-architecture + branching + active-t4-runtime)
- [x] Item 1 — Class-roster registry (`class_roster.py` new module; 10 entries per doc 48 § 1 CANONICAL LOCK)
- [x] Item 2 — Per-class chain count + T4 count rule + supporting chain (`emit_skills_for_class()` in `per_skill_emitter.py`)
- [x] Item 3 — Depth-≥4 branching (D69; Assassin Shadow-Strike T2 branch as v1 demonstration)
- [x] Item 4 — Active T4 runtime marker (`active_t4_chain` + `supporting_chain` + `class_archetype` fields on `PlayerClassV2`)
- [x] Item 5 — Season cardinality n_kits=40 (`bc_target_subspace_generator.py` L173 amended)
- [x] `generation/MIGRATION.md` § Wave 1.5 authored per ADR-004
- [x] `generation/AGENT_STATE.md` updated
- [x] Cross-seam round-trip smoke: 40-kit test season, all 3 new fields populated, 22 T4 capstones + 10 supporting chains correct
- [x] 232/232 regression tests PASS

### Aggregate counts (doc 48 § 2.1 canonical lock; all verified)

| Metric | Expected | Actual |
|---|---|---|
| Classes | 10 | 10 |
| 3-chain classes | 8 | 8 |
| 4-chain classes | 2 (Gunslinger + Crusader) | 2 |
| T4 capstones | 22 | 22 |
| Supporting chains | 10 | 10 |
| n_kits default | 40 | 40 |

### Open questions resolved

- Q-W15-S3-1: default `active_t4_chain` = None (pre-T4 unlock); first t4_chain_ids[0] after unlock — resolved in math note + code
- Q-W15-S3-2: Assassin Shadow-Strike T2 branch as v1 demonstration — resolved
- Q-W15-S3-3: stub-level respec interface (Wave 4+ full implementation) — resolved
- Q-W15-S3-4: class_roster.py new module per seam convention — resolved

### Cross-seam Pattern-A queries

Both Q-W15-S3-1 and Q-W15-S3-2 resolved by rocket from dispatch guidance + doc 48 content without requiring gandalf Pattern-A query. No open Pattern-A queries outstanding.

### Files created/modified

- NEW: `~/Games/reincarnated-engine/src/reincarnated/generation/class_roster.py`
- NEW: `~/Games/reincarnated-engine/src/reincarnated/generation/math/wave-1-5-class-chain-architecture-math.md`
- NEW: `~/Games/reincarnated-engine/src/reincarnated/generation/math/wave-1-5-branching-math.md`
- NEW: `~/Games/reincarnated-engine/src/reincarnated/generation/math/wave-1-5-active-t4-runtime-math.md`
- AMENDED: `~/Games/reincarnated-engine/src/reincarnated/generation/per_skill_emitter.py` (emit_skills_for_class + helpers)
- AMENDED: `~/Games/reincarnated-engine/src/reincarnated/generation/bc_target_player_class.py` (3 new fields)
- AMENDED: `~/Games/reincarnated-engine/src/reincarnated/generation/bc_target_subspace_generator.py` (n_kits=40)
- AMENDED: `~/Games/reincarnated-engine/src/reincarnated/generation/MIGRATION.md` (§ Wave 1.5)
- AMENDED: `~/Games/reincarnated-engine/src/reincarnated/generation/AGENT_STATE.md`

### For Wave 2 dispatch authoring

- Fix B implementation (WITHIN_ATTRIBUTE_FAMILY_WEIGHT + two-step sampling): math note ready at `math/within-attribute-family-weight-math.md`
- Fix B-prime (caster-faith mace dial-back): Crusader class_archetype + Wave 2 sampling fix compose naturally
- gamora null-safe note: `active_t4_chain = None` is valid pre-T4 state; gamora must handle null gracefully (no crash; T4 capstone not applied)
- Branching skeleton in place; Wave 4+ investment routing can build on branch node emission structure
