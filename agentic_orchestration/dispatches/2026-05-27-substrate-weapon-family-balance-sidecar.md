# Dispatch — 2026-05-27 — Substrate Weapon Family Balance Sidecar (Fix A + Fix B + Fix C)

**From:** knight-rider
**To:** rocket (Fix A + Fix B); elrond (Fix C)
**Approved by:** Matt 2026-05-27 ratified three-fix substrate recommendation inline per scaffold-drift consolidated package § 2
**Estimated effort:** Fix A ~1 hr (rocket) + Fix B math-note ~2-3 hrs + impl Wave 2 (rocket) + Fix C ~2-3 hrs (elrond)
**Acceptance:** Fix A landed (hygiene filter + module-load assertion); Fix B math-note authored NOW + implementation queued for Wave 2; Fix C audit complete + remediation routing (if needed) via gandalf design call

## Context

Scaffold-drift recognition surfaced 2026-05-27 (`agentic_orchestration/gandalf/notes/2026-05-27-scaffold-drift-recognition-and-corrective-package.md` § 2). Substrate composition empirically:

- **STR characters:** 90% martial-heavy / 10% ranged — Diablo II "every barbarian carries a two-hander" pattern (90:10 too steep)
- **Ammo contamination:** 148 ammo/consumable + 36 shield/talisman/banner/horn = 185 rows eligible as main weapons via `substrate_weapon_binding.py:_query_substrate_weapon` (no `weapon_kind` filter; uniform sampling)
- **Caster variety:** within-family identity beat (orb vs tome vs wand vs staff vs scepter vs focus) unaudited

Three discrete fixes per consolidated doc § 2.2 / § 2.3 / § 2.4. Bundled as one sidecar dispatch per kicker § 2 Dispatch 1.

**Pre-Wave-5 gating per consolidated doc § 5.3:** Fix A + Fix B must close before Wave 5 production gauntlet fires. Fix C is non-gating (audit-first; remediation only if needed).

**Wave 1 in-flight context:** rocket Wave 1 (concentration architecture Layers 1-4+7) landed `98b68aa` 2026-05-27 — concurrent with scaffold-drift package authoring. Fix A folds into a Wave 1 closure window OR fires as small follow-on; Fix B math-note authored now + implementation queued for Wave 2.

## Required reading before starting

- `canonical/00-ground-state.md` — ground-state oracle
- `agentic_orchestration/gandalf/notes/2026-05-27-scaffold-drift-recognition-and-corrective-package.md` § 2 (substrate sidecar substantive spec)
- `agentic_orchestration/gandalf/notes/2026-05-27-scaffold-drift-kr-kicker.md` § 2 Dispatch 1 (this dispatch's routing source)
- `canonical/47-damage-scaling-architecture-2026-05-27.md` § 3 (per-attribute weapon profile — Fix B aligned)
- `agentic_orchestration/elrond/notes/2026-05-27-cycle-14-sc-6-substrate-weapon-audit.md` (SC-6 audit; substrate composition reference)
- `~/Games/reincarnated-engine/src/reincarnated/generation/substrate_weapon_binding.py` L238-269 (Fix A + Fix B target)
- `.claude/skills/reincarnated-rocket-operating-procedure` (rocket loads)
- `.claude/skills/reincarnated-elrond-operating-procedure` (elrond loads)
- `.claude/skills/reincarnated-hive-mind-protocol`
- `.claude/skills/reincarnated-engineering-disciplines` (#1 + #11 + #18 + #38 + Discipline #40 candidate)

## Math-before-code

**Fix B math-note REQUIRED** (Discipline #1): `~/Games/reincarnated-engine/src/reincarnated/generation/math/within-attribute-family-weight-math.md` documenting:
- 70/30 STR martial-heavy/ranged derivation per consolidated doc § 2.3
- 60/40 DEX ranged/martial-light derivation (mild rebalance from 66/34)
- Variance implications on N-character cohort (e.g., 4-STR cohort expected ~2.8 heavy-melee + ~1.2 ranged)
- Composition with doc 47 § 3 per-attribute weapon profile + SC-6b enriched substrate

Math-note is Gate-1 input for Wave 2 implementation.

**Fix A** does not require math-note (pure correctness; module-load assertion verifies count).
**Fix C** does not require math-note (empirical audit; SQL only).

## Cross-seam contract change? (Principle 6 gate)

- **Fix A**: PARTIAL — substrate query filter is intra-seam rocket scope; downstream characters get cleaner main_weapon binding but no JSON shape change. Round-trip: not applicable cross-seam contract.
- **Fix B**: PARTIAL — sampling logic change is intra-seam rocket; downstream characters see different family distribution but same JSON shape. Round-trip: not applicable cross-seam contract.
- **Fix C**: NO — audit-only; no schema or contract change. Round-trip: not applicable.

**MIGRATION.md** updates per ADR-004:
- generation/MIGRATION.md § Wave 1 closure follow-on: Fix A landed (hygiene filter + module-load assertion)
- generation/MIGRATION.md § Wave 2 (when Fix B fires): WITHIN_ATTRIBUTE_FAMILY_WEIGHT table + sampling logic change

## Scope

### Fix A — Hygiene filter (rocket; ~1 hr)

- [ ] Amend `~/Games/reincarnated-engine/src/reincarnated/generation/substrate_weapon_binding.py:_query_substrate_weapon` (~L238-269) to add `WHERE wke.weapon_kind IN ('category', 'named_template', 'unique')` to substrate query
- [ ] Eliminates 185 contamination rows (148 ammo/consumable + 36 shield/talisman/banner/horn + 1 unknown)
- [ ] Add module-load assertion verifying eligible row count (~2,108 post-filter)
- [ ] Update generation/MIGRATION.md § Wave 1 closure follow-on with Fix A entry
- [ ] AGENT_STATE.md updated
- [ ] Smoke: test season generation; verify no main_weapon binding is ammo/shield/etc.
- [ ] Commit + push per Matt 2026-05-27 per-cycle push pattern

### Fix B — Within-STR family rebalancing (rocket; math-note NOW; impl Wave 2)

- [ ] Author math-note at `~/Games/reincarnated-engine/src/reincarnated/generation/math/within-attribute-family-weight-math.md`
- [ ] Math-note content per § Math-before-code above
- [ ] Implementation DEFERRED to Wave 2 (alongside Layer 8 set keying — both touch substrate sampling logic)
- [ ] Wave 2 dispatch (separate; KR authors later) will scope:
  - Add `WITHIN_ATTRIBUTE_FAMILY_WEIGHT` table per consolidated doc § 2.3
  - Two-step sampling: sample family per attribute weight; uniform within family rows
  - Acceptance: 4-STR cohort produces ~2.8 heavy-melee + ~1.2 ranged
- [ ] Math-note routes to jack-ryan Gate-1 DESIGN-MODE before Wave 2 dispatch fires

### Fix C — Caster weapon_kind variety audit (elrond; non-gating; fire anytime)

- [ ] Run empirical SQL audit per consolidated doc § 2.4:
  ```sql
  SELECT wsp.weapon_type_family, wke.weapon_kind, COUNT(*) AS n
  FROM weapon_sim_props wsp JOIN weapon_knowledge_entries wke ON wke.id = wsp.weapon_id
  WHERE wke.v1_scope = 1 AND wsp.weapon_type_family IN ('caster-arcane', 'caster-faith')
  GROUP BY wsp.weapon_type_family, wke.weapon_kind ORDER BY n DESC;
  ```
- [ ] If `category` dominates: drill into `canonical_name` keyword analysis for "staff" / "wand" / "orb" / "tome" / "scepter" / "focus" sub-categories
- [ ] Output findings at `agentic_orchestration/elrond/notes/2026-05-27-caster-weapon-kind-audit.md`
- [ ] If audit surfaces remediation need: route via knight-rider to gandalf for design call
- [ ] If audit surfaces no remediation need: close as INFO; no further action
- [ ] Commit + push per Matt 2026-05-27 per-cycle push pattern

## Acceptance criteria

- [ ] **Fix A:** substrate query has `weapon_kind` filter; module-load assertion verifies ~2,108 eligible rows; smoke test confirms no ammo/shield/banner/etc. binds as main_weapon; jack-ryan Gate-2 (folds into Wave 1 closure Gate-2 or separate)
- [ ] **Fix B:** math-note authored at the specified path; Wave 2 implementation queued via subsequent dispatch
- [ ] **Fix C:** audit findings filed at the specified path; remediation routing decision documented
- [ ] All three sub-fixes have completion records appended to this dispatch
- [ ] Both seams commit + push per Matt 2026-05-27 per-cycle pattern

## Out of scope (explicit non-goals)

- Do NOT implement Fix B sampling logic in this dispatch (deferred to Wave 2 per consolidated doc § 5.1)
- Do NOT touch other substrate tables beyond `weapon_knowledge_entries` + `weapon_sim_props`
- Do NOT amend canonical docs (gandalf seam; if remediation surfaces via Fix C, route via KR)
- Do NOT touch character JSON output schema (rocket Wave 0.5 + future scope; no contract change)
- Do NOT enter Wave 1.5 scope (Skill-Tree Architecture; separate dispatch gated on Matt class-roster sub-decision)
- Do NOT regress Wave 1 outputs (concentration architecture Layers 1-4+7 landed at `98b68aa`)
- Do NOT regress synthetic_mode (Discipline #39 LOAD-BEARING; RETIRED at Wave 0.5)

## Open questions for sub-agents

- **Q-SIDE-1 (rocket Fix B):** STR 70/30 + DEX 60/40 weights are gandalf's design-call ratified-inline values; any reason rocket diverges at math-note authoring? Pattern-A to gandalf if uncertain.
- **Q-SIDE-2 (elrond Fix C):** if audit surfaces caster `weapon_kind` heavily skewed (e.g., 90% staves), what's the remediation path? gandalf design call OR substrate library enrichment OR runtime variety injection? Elrond proposes; KR routes.

## References

- `agentic_orchestration/gandalf/notes/2026-05-27-scaffold-drift-recognition-and-corrective-package.md` § 2 (substantive substrate sidecar spec)
- `agentic_orchestration/gandalf/notes/2026-05-27-scaffold-drift-kr-kicker.md` § 2 Dispatch 1
- `canonical/47-damage-scaling-architecture-2026-05-27.md` § 3 (per-attribute weapon profile)
- `agentic_orchestration/elrond/notes/2026-05-27-cycle-14-sc-6-substrate-weapon-audit.md`
- `~/Games/reincarnated-engine/src/reincarnated/generation/substrate_weapon_binding.py` L238-269
- Engineering disciplines #1 + #11 + #18 + #38 + #40 (candidate)
- Hive-mind protocol § 4 (decision-routing) + § 2.2.2 (wave-entry-fire-discipline)

---

## Completion record

### Fix A — rocket — COMPLETE (2026-05-27)

**Commit:** `dac5f9e` (engine `main`)

**What landed:**

`substrate_weapon_binding.py:_query_substrate_weapon` amended with weapon_kind hygiene filter:
- `AND wke.weapon_kind IN ('category', 'named_template', 'unique')` added to WHERE clause
- Eliminates 185 contamination rows: ammo_or_consumable(148) + shield(17) + talisman(11) + banner(7) + unknown(1) + horn(1)
- Post-filter eligible pool: **2,108 rows exact** (empirically verified — category:1139 + named_template:927 + unique:42)

Module-load assertion `_assert_eligible_row_count()` added:
- Fires at import time via module-level call
- Expects 2,108 ±50; warns+skips if DB absent; raises AssertionError if count outside tolerance
- `_EXPECTED_ELIGIBLE_ROW_COUNT = 2108`, `_ELIGIBLE_ROW_COUNT_TOLERANCE = 50`

**Smoke results:**
- Module-load assertion: PASS (2108 rows; exact match)
- Filtered pool contamination: PASS (0 contamination-kind rows)
- Live selection (4 attrs × 6 seeds = 24 weapons): 0 contamination-kind weapons selected
- "Horn Bow" false-positive confirmed benign (weapon_kind=category, not the horn kind)
- Regression: test_cycle14_wave1_concentration.py 29/29 PASS

**MIGRATION.md:** § Wave 1 Closure Follow-on — Fix A entry filed per ADR-004.

**Q-SIDE-1 resolution:** No divergence from gandalf design-call ratified-inline values (70/30 STR + 60/40 DEX). Math note authored exactly as specified; no Pattern-A to gandalf required.

**Gate-2 routing:** Fix A folds into Wave 1 closure Gate-2 (jack-ryan) per dispatch acceptance criteria.

---

### Fix B — rocket — Math Note COMPLETE; Implementation DEFERRED to Wave 2 (2026-05-27)

**Commit:** `dac5f9e` (same commit as Fix A; both in rocket seam)

**Math note path:**
`~/Games/reincarnated-engine/src/reincarnated/generation/math/within-attribute-family-weight-math.md`

**Content authored:**
- 70/30 STR martial-heavy/ranged derivation: reduces all-heavy-melee-cohort probability 65.6% → 24.0%; yields E[ranged]=1.2 per 4-STR cohort (from 0.4); binomial σ=0.92 for heavy-melee count in 4-STR cohort; comparison table across 90/10/80/20/70/30/60/40/50/50 options with rationale for 70/30 selection
- 60/40 DEX ranged/martial-light derivation: mild rebalance from substrate raw 67.2/32.8; doc 47 "light melee + ranged" co-equal framing alignment; E[martial-light]=1.6 per 4-DEX cohort
- Variance implications on N-character cohort: 4-STR cohort binomial distribution fully worked; 95% CI [1,4] practical range; 20-trial acceptance criteria for Wave 2 smoke
- WITHIN_ATTRIBUTE_FAMILY_WEIGHT table specification per consolidated doc § 2.3 (exact Python constant spec at § 5.1)
- Two-step sampling implementation spec with fallback logic at § 5.2 (cites `substrate_weapon_binding.py` post-Fix-A line references per Discipline #1.2)
- Composition with doc 47 § 3 per-attribute weapon profile + SC-6b enriched substrate at § 6
- Wave 2 MIGRATION.md required notes at § 7

**Wave 2 implementation queue note:**
Fix B implementation is Wave 2 scope (alongside Layer 8 set keying). Dispatch to be authored by KR. Gate-1 DESIGN-MODE (jack-ryan) required before implementation fires — math note is the input document. No code change in this session per dispatch out-of-scope clause.

---

### Fix C — elrond seam — NOT rocket scope (firing in parallel)

Fix C (caster weapon_kind variety audit) is elrond's seam. Rocket makes no record here; elrond appends their own completion record when audit completes.

---

### Fix C — elrond — AUDIT COMPLETE (2026-05-27)

**Findings file:** `agentic_orchestration/elrond/notes/2026-05-27-caster-weapon-kind-audit.md`

**Verdict shape:** mixed — INFO close on caster-arcane; REMEDIATION NEEDED on caster-faith.

**Empirical findings (post-Fix-A footprint):**

- **caster-arcane (159 rows):** GENUINELY DIVERSE on the within-caster identity beat. Staff 40% (64), rod 30% (47), wand/scepter/tome/orb/focus collectively ~7% (12), plus ~23% mis-categorized source-noise (Crystal-prefixed melee weapons mis-tagged caster, museum-piece Smithsonian noise, moctezuma_atlatl etc.). The substrate's caster-arcane diversity hypothesis HOLDS. No remediation needed; optional non-gating curation pass queued for the 36-row miscategorization tail.

- **caster-faith (146 rows):** **MACE-DOMINATED at 62% (90/146).** D&D "cleric carries a mace" trope bleeding into the substrate's family classifier. Genuine faith-flavor instruments (censers, holy-water sprinklers, crucifixes, vajra, rosaries, thuribles) total ~25 rows (~17%). Staff-shape faith instruments essentially absent (5 rows, 3%). Within-family identity beat structurally broken — sampling uniformly produces a mace 62% of the time.

**Architectural finding (out-of-scope but flagged):** `weapon_kind` enum is a row-role classifier (template/unique/contamination), NOT a sub-shape classifier. Sub-shape lives ONLY in `canonical_name` free-text. `weapon_kind_classified_subtype` is too coarse (handheld_weapon / accessory_handheld / armor_shield / NULL). No native sub-shape granularity exists. Future Cycle-15 substrate-architecture candidate: add `weapon_sub_shape` enum column.

**Remediation recommendation:** **gandalf design call** to pick between two pre-Wave-5-feasible paths:

- **Path A (elrond Tier 1 recommendation):** substrate-classifier reclassification — move mace-family rows from `weapon_type_family = 'caster-faith'` to `martial-heavy`/`martial-light`. Caster-faith shrinks 146→~56 rows dominated by genuine faith-instrument shapes. Addresses root cause; aligns vocabulary with mechanics. Cross-seam impact: rocket main_weapon binding volume change, gandalf design-intent on faith-caster identity, gamora BC measurement refresh.

- **Path B (Tier 2):** runtime within-family sampling adjustment — `WITHIN_CASTER_SHAPE_WEIGHT` table in `substrate_weapon_binding.py`; under-weight mace-keyword rows when sampling caster-faith. Non-destructive; reversible; ships Wave 2 alongside Fix B. Cross-seam impact: rocket-only; gandalf scopes acceptance ratios.

- **Path C (queued for later, NOT pre-Wave-5):** substrate library enrichment — commission legolas Mode B re-crawl with sub-shape targeting (prayer-staff, censer, orb-of-faith, tome-of-scripture, crozier, scepter, focus, relic, monstrance) to add ~80-120 non-mace faith-instrument rows. Highest cost; best long-term; queue for Cycle 15.

**Q-SIDE-2 answer:** caster `weapon_kind` is NOT heavily skewed in the spec's sense (named_template dominates over category) — but the deeper sub-shape question reveals caster-faith IS heavily skewed at the canonical_name-derived sub-shape layer (62% mace). Recommended remediation path: gandalf design call selecting between Path A (preferred) and Path B (fallback); Path C queued as future substrate work.

**Routing to KR:**
- Route gandalf design call for Path A vs Path B decision (pre-Wave-5; small scope)
- Queue caster-arcane miscategorization cleanup pass (non-gating; future elrond curation dispatch)
- Queue Cycle-15 substrate-architecture candidate (`weapon_sub_shape` enum column; deferred design call)

**Anti-stall discipline observed:** stopped after audit + recommendation per dispatch § Out of scope. No substrate library modification fired. No remediation implementation in this session. No touch to Fix A / Fix B (rocket's seam).

**Authority basis:** dispatch 2026-05-27 substrate-weapon-family-balance-sidecar.md Fix C; Matt 2026-05-27 ratified three-fix substrate recommendation inline; elrond OP § 2 Pattern A-light mode (small focused empirical audit) + § 3.2 substrate-led discipline (substrate's vote on family classification surfaced; semantic interpretation deferred to gandalf design call).
