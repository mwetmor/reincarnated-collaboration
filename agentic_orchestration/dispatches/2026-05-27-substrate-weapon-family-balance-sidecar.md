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
