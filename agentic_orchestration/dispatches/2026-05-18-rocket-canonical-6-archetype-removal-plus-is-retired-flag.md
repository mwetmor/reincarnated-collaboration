# 2026-05-18 — rocket — Canonical-6 transition: hybrid_mage archetype-list removal + is_retired flag on 17 staged instances

**Authority:** Matt L3 RETIRE verdict 2026-05-18; canonical-6 transition chain (gandalf design doc + jack-ryan decisions-log in parallel).
**Type:** Pattern B — engine archetype-list removal + data flag pass; ~1-2 hours.
**Status:** 🟢 **ACTIVE — fire immediately. Parallel-safe with gandalf + jack-ryan + drax + elrond.**

---

## Why this matters

Hybrid_mage retired per Matt L3 (D11.0/D11.1/D11.2 cycle failures + smoke environment fidelity bug). Engine must:
1. Drop hybrid_mage from canonical archetype list so future generation produces canonical-6
2. Flag the 17 existing hybrid_mage instances in staged seasons 002011-015 with `is_retired: true` so demo + loadout filter them at consume time
3. Cleanly handle the transition without breaking historical telemetry references

This unblocks Matt's stated milestone: "develop a completely new LLM generated season once we feel those issues are resolved" — once you ship + drax filter ships, new-season regen at canonical-6 can fire.

---

## Required reading

1. **D11.2 Phase B failure** — `agentic_orchestration/dispatches/2026-05-17-rocket-d11-2-phase-b-full-salvage-scale-0-75.md` § completion (your prior; root-cause is gear-environment fidelity)
2. **Phase B decision file** — `reincarnated-engine/output/d11_2_phase_b_decision.json` (per-instance data; 17 instance IDs you need to flag)
3. **D11.2 Lever B code** — `reincarnated-engine/src/reincarnated/generation/d10_kit_constraints.py` (LEVER_B_TARGET_ARCHETYPE_TAG constant; `_apply_dps_density_scale`; remove or guard now-dead-code paths)
4. **Canonical archetype list locations** — search codebase for "hybrid_mage" + canonical-7 enumeration sites; likely include:
   - `config/_archetype_*.yaml` or roles.yaml
   - generation pipeline archetype-tag enumeration
   - templates / prompts
   - test fixtures
   - balance_loop.py (if archetype-specific logic exists)
5. **balance_metadata schema** — for the is_retired field addition (additive; non-breaking)
6. **MIGRATION.md** — `reincarnated-engine/src/reincarnated/simulation/MIGRATION.md` (your v1.11 + Phase B amendment); append v1.13 entry for canonical-6 transition

---

## Scope — five deliverables

### Deliverable 1 — Archetype list removal at canonical sites

Identify + remove "hybrid_mage" from every canonical archetype enumeration in the engine codebase:
- Config files (roles.yaml or equivalent)
- Generation pipeline archetype-pool definitions
- LLM prompt templates that enumerate archetypes (so LLM doesn't generate hybrid_mage classes)
- Test fixtures (if test data references hybrid_mage, decide: amend or mark deprecated)
- Any archetype-specific branches in balance_loop.py / d10_kit_constraints.py

**Cleanup of D11.2-specific code:** the Lever B code path (`_apply_dps_density_scale`) becomes dead code once hybrid_mage is gone. Two options:
- (a) Remove dead code now (cleanest)
- (b) Keep dead code with comment "RETIRED 2026-05-18 — kept for historical reference + potential alternative-archetype reuse" (more conservative)

Recommend **(b)** — Lever B was a generalizable lever; it might be useful for future archetypes. Comment + leave; mark unused.

### Deliverable 2 — `is_retired: true` flag on staged 17 instances

Author backfill script `reincarnated-engine/scripts/canonical_6_retire_hybrid_mage_flag.py`:
- Iterates 17 hybrid_mage instances across seasons 002011-015
- For each instance: add `is_retired: true` to the class JSON top-level
- Add `retirement_reason: "canonical_6_transition_2026_05_18"` for provenance audit
- Writes back to both `reincarnated-engine/output/standard-demo-regen-2026-05-17/season_<id>/classes/` and `reincarnated-demo/public/seasons/season_<id>/classes.json` + `reincarnated-loadout/data/season_<id>/classes/<id>.json` per-class files (mirror your v1.13.2/v1.14-d11.1-demo-sync + v1.14-d11.1-loadout-sync patterns)
- Idempotent (running twice doesn't corrupt; field stays true)

### Deliverable 3 — Verify generation pipeline canonical-6 default

After deliverable 1, run a quick generation smoke (single class, dry-run or test mode) to verify:
- No hybrid_mage classes generated
- 6 archetypes remain in the rotation
- Generation works end-to-end without hybrid_mage references
- LLM prompts don't include hybrid_mage in archetype enumeration

If any test failures emerge, document and address. If clean: log smoke verdict in completion record.

### Deliverable 4 — MIGRATION.md v1.13 entry

Append canonical-6 transition entry:
- Description: hybrid_mage retired from canonical archetype list; 17 staged instances flagged is_retired; generation default = canonical-6
- Cross-seam impact: drax + loadout must filter is_retired classes at consume time (drax dispatch downstream)
- D11.2 Lever B code: retained as commented-out / unused; reference for potential future alternative-archetype reuse
- Historical telemetry: existing ClassBalanceResult rows for hybrid_mage instances stay (no DB cleanup); future regen produces canonical-6 only

### Deliverable 5 — New-season regen readiness flag

Brief in completion record: confirm engine is ready to fire a fresh new-season regen (rocket --new-season-regen canonical-6 OR equivalent) once gandalf + jack-ryan + drax-filter all land. Matt will explicitly authorize the regen; don't auto-fire from this dispatch.

---

## Acceptance criteria

- [ ] Hybrid_mage removed from all canonical archetype enumeration sites
- [ ] D11.2 Lever B code retained with retirement comment (or removed cleanly per your call)
- [ ] Backfill script authored at named path
- [ ] All 17 hybrid_mage instances flagged is_retired across engine/staged + demo/public + loadout/data
- [ ] Generation pipeline smoke verified canonical-6 (no hybrid_mage)
- [ ] MIGRATION.md v1.13 entry appended
- [ ] `pytest` clean on simulation + generation seams
- [ ] New-season regen readiness confirmed in completion record
- [ ] PRE-SIGNAL § 14.1.1 before hive-log append
- [ ] AGENT_STATE STATE entry
- [ ] Tag `rocket/v1.17-canonical-6-retire-hybrid-mage-1`

---

## Out of scope (DO NOT)

- ❌ DO NOT fire a fresh new-season regen (separate dispatch; Matt authorizes)
- ❌ DO NOT delete historical telemetry rows for hybrid_mage (preserve for record)
- ❌ DO NOT modify demo or loadout code (drax seam; separate dispatch handles is_retired filter at consume time)
- ❌ DO NOT touch gandalf's canonical-6 design doc (different repo)
- ❌ DO NOT re-litigate RETIRE
- ❌ DO NOT push tag (ADR-006)

---

## Coordination

- **Parallel-safe with:** gandalf canonical-6 design doc; jack-ryan decisions-log + Discipline #17; drax v1.16.2 audio + holy VFX; elrond dungeon-objects audit
- **Triggers downstream:** drax v1.17 is_retired filter + dungeon-objects swap (knight-rider fires post-elrond scout + post-your-flag); new-season regen authorization to Matt (knight-rider surfaces when chain locks)
- **PRE-SIGNAL § 14.1.1** before hive-log appends

---

*Dispatched 2026-05-18 by knight-rider per Matt L3 RETIRE verdict. ~1-2h. Append completion record + generation smoke verdict when done.*

---

## Completion record

**Status:** COMPLETE
**Executed by:** rocket
**Date:** 2026-05-18
**Time:** ~2h

### Acceptance criteria — all met

- [x] Hybrid_mage removed from all canonical archetype enumeration sites
- [x] D11.2 Lever B code retained with retirement comment (`d10_kit_constraints.py` `_apply_dps_density_scale` + `LEVER_B_TARGET_ARCHETYPE_TAG`)
- [x] Backfill script authored at `scripts/canonical_6_retire_hybrid_mage_flag.py`
- [x] All 17 hybrid_mage instances flagged is_retired across engine staged + demo/public + loadout/data
- [x] Generation pipeline smoke verified canonical-6: 5/5 PASS, 0 hybrid_mage generated
- [x] MIGRATION.md v1.13 entry appended
- [x] pytest: 44/44 balance_loop PASS; targeted generation/simulation tests 544 pass, 10 skip, 8 pre-existing failures (confirmed pre-existing)
- [x] New-season regen readiness confirmed
- [x] PRE-SIGNAL § 14.1.1 honored before hive-log append
- [x] AGENT_STATE.md STATE entry updated
- [x] Tag `rocket/v1.17-canonical-6-retire-hybrid-mage-1` created (local; push gated per ADR-006)

### Smoke verdict

PASS. 5/5 classes generated at canonical-6 without hybrid_mage.
`hybrid_mage` absent from `b6_archetype_templates.ARCHETYPE_TEMPLATES`.
`role_orientation="hybrid"` now falls through to elemental substrate derivation (fire→fire_mage, etc.).
44/44 balance_loop tests pass. Targeted tests: 544 pass, 10 skip.

### Data flag result

17/17 hybrid_mage instances flagged `is_retired: true` + `retirement_reason: "canonical_6_transition_2026_05_18"`.
All 3 locations clean (engine staged + demo classes.json + loadout per-class).
Script idempotent (second run: all 17 already_flagged, 0 errors).

### New-season regen readiness

CONFIRMED. Engine ready for canonical-6 fresh regen. Waiting on: gandalf (DONE), jack-ryan (DONE), drax is_retired filter (pending drax dispatch). Matt authorizes regen once drax-filter ships.

### Commits

- engine: `1aa5e99` `reincarnated-engine/main`
- demo: `686711b` `reincarnated-demo/main`
- loadout: `b8e0bf5` `reincarnated-loadout/main`

### Adjacent open item (flagged, not in scope)

gandalf § 8.2 + § 8.3 flagged: `stat_allocator.allocate_stats()` Pattern P7 fallback silently uses hybrid_mage stats for unknown archetypes. Post-canonical-6, the fallback target no longer exists as a generation-valid archetype. Recommend `ValueError` on unrecognized archetype_tag. Not addressed in this dispatch (scope was archetype-list removal only). Flagged for separate dispatch post-regen.
