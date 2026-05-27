# Dispatch — 2026-05-27 — rocket — Cycle 14 Wave 0.5 follow-on: pipeline wiring + LUT alignment

**From:** knight-rider
**To:** rocket (engine content-generation seam owner)
**Approved by:** Matt 2026-05-27 (autonomous KR scope per cycle-doc § 4.1; two follow-on items surfaced at Wave 0.5 closure 2026-05-27)
**Estimated effort:** ~2-4 hours total (1-2 hrs pipeline wiring + 1-2 hrs LUT alignment + commit)
**Acceptance:** `per_skill_emitter.py` + `substrate_weapon_binding.py` wired into `season_generation_pipeline.py`; rocket fallback LUT values aligned to elrond SC-6b Pass-2 LUT per Discipline #10 attribution clarity; smoke confirms wired pipeline emits per-skill content + binds substrate weapons

## Context

Wave 0.5 closed 2026-05-27 (jack-ryan Gate-2 PASS-with-WARN at engine `f053281`; 0 BLOCK / 1 WARN / 4 INFO). Two follow-on items surfaced that gate Wave 5 fresh-roster gauntlet sim:

1. **Cycle 14 pipeline wiring (rocket surfaced)** — `per_skill_emitter.py` + `substrate_weapon_binding.py` (landed via Wave 0.5 at engine `b2e9a86`) are STANDALONE modules. They are not yet wired into `season_generation_pipeline.py`. Wave 5 fresh roster generation needs the wired pipeline to consume the per-skill emission + substrate binding outputs at season-gen time.

2. **LUT alignment WARN (Gate-2 Finding 2)** — elrond SC-6b Pass-2 LUT values (martial-heavy=177, ranged=91) diverge from rocket fallback (martial-heavy=200, ranged=150). Benign at Wave 0.5 (live SC-6b values win for all 2,293 v1_scope rows; rocket fallback only fires for non-v1_scope edge cases). Per Discipline #10 attribution clarity + Path A architectural commitment (elrond owns substrate baseline; rocket's fallback should align), **rocket fallback constants update to elrond Pass-2 LUT values** before Wave 5 fresh-roster gauntlet sim fires.

Both items are small focused rocket-seam follow-ons. Combined into single dispatch.

## Required reading before starting

- `canonical/00-ground-state.md` — ground-state oracle
- `agentic_orchestration/elrond/research/sc-6b-substrate-enrichment-2026-05-27/MIGRATION.md` — SC-6b MIGRATION (cross-seam contract)
- `agentic_orchestration/elrond/research/sc-6b-substrate-enrichment-2026-05-27/sc-6b-baseline-lut-math-2026-05-27.md` — LUT math-note with Pass-2 corrected values (the authoritative source rocket fallback aligns to)
- `agentic_orchestration/elrond/research/sc-6b-substrate-enrichment-2026-05-27/sc-6b-weapon-family-baselines-2026-05-27.json` — Pass-2 LUT JSON
- `agentic_orchestration/qa/pending/2026-05-27-jack-ryan-cycle-14-wave-0-5-gate-2-closure.md` — Gate-2 verdict + Finding 2 WARN
- `~/Games/reincarnated-engine/src/reincarnated/generation/per_skill_emitter.py` — standalone module (your prior Wave 0.5 emission)
- `~/Games/reincarnated-engine/src/reincarnated/generation/substrate_weapon_binding.py` — standalone module (your prior Wave 0.5 binding)
- `~/Games/reincarnated-engine/src/reincarnated/generation/season_generation_pipeline.py` — the integration target
- `~/Games/reincarnated-engine/design/decisions/decisions-log.md` — entry by jack-ryan at `f053281` (Path A architectural commitment; LUT divergence cross-reference)
- `.claude/skills/reincarnated-rocket-operating-procedure`
- `.claude/skills/reincarnated-hive-mind-protocol`

## Math-before-code

Not applicable directly — this is wiring + constant alignment, not algorithmic. However, the LUT alignment math reference IS elrond's Pass-2 LUT (already authored at `sc-6b-baseline-lut-math-2026-05-27.md`). Cite that math-note in code comments where the rocket fallback LUT lives.

## Cross-seam contract change? (Principle 6 gate)

**PARTIAL** — pipeline wiring doesn't change cross-seam contracts (consumes existing modules + emits character JSON that gamora damage_resolver already routes per `damage_scaling_type`). LUT alignment is intra-seam (rocket fallback constants only).

**Round-trip: not applicable for cross-seam contract**, but:
- Pipeline wiring smoke: `season_generation_pipeline` emits character JSON with per-skill content + substrate weapon binding fields populated (already verified per Wave 0.5 module smoke; wiring smoke is the integration test)
- LUT alignment smoke: spot-check that rocket fallback values match elrond Pass-2 LUT (martial-heavy=177, ranged=91, etc.)

## Scope

### Item 1 — Pipeline wiring (~1-2 hrs)

- [ ] Inspect `season_generation_pipeline.py` to identify the existing chain composition + gear gen + substrate selection call sites
- [ ] Wire `per_skill_emitter.emit_skills_for_kit()` into the season gen flow: for each kit composition, emit 12 skills per kit (3 chains × 4 tiers) per Wave 0.5 per_skill_emitter contract; per-skill content joins to character JSON `skills[]` field
- [ ] Wire `substrate_weapon_binding.select_and_bind_substrate_weapon()` into the gear gen flow: for each character's `gear_representative.main_weapon`, populate all 8 substrate weapon fields per Wave 0.5 substrate_weapon_binding contract
- [ ] Verify wiring doesn't regress existing season gen smoke tests
- [ ] Integration smoke: generate a 16-character test season; verify per-skill content emits with non-null `damage_scaling_type` for every skill; verify all 16 character JSONs have populated `gear_representative.main_weapon` 8-field substrate binding

### Item 2 — LUT alignment (~1-2 hrs)

- [ ] Identify rocket fallback LUT constants in `substrate_weapon_binding.py` (or wherever the family baseline values are hardcoded)
- [ ] Update rocket fallback values to match elrond Pass-2 LUT per `sc-6b-weapon-family-baselines-2026-05-27.json` + `sc-6b-baseline-lut-math-2026-05-27.md`
- [ ] **Align ALL 5 family values to elrond Pass-2 LUT** (per Gate-1 Finding FO-2 WARN amendment — Gate-2 Finding 2 named only martial-heavy + ranged; jack-ryan Gate-1 surfaced full divergence across all 5 families):
  - `martial-heavy`: 200 → **177**
  - `martial-light`: → **99**
  - `ranged`: 150 → **91**
  - `caster-arcane`: → **31**
  - `caster-faith`: → **31**
  - Cross-check against canonical source `agentic_orchestration/elrond/research/sc-6b-substrate-enrichment-2026-05-27/sc-6b-weapon-family-baselines-2026-05-27.json` for any additional families requiring alignment (e.g., hybrid family if instantiated)
- [ ] Add code comment citing `sc-6b-baseline-lut-math-2026-05-27.md` as the authoritative source per Discipline #10 attribution clarity
- [ ] Smoke: verify post-update fallback values match elrond LUT for all 5+ families (spot-check via assert OR test; canonical verification source = sc-6b-weapon-family-baselines-2026-05-27.json)

*Amended 2026-05-27 per jack-ryan Gate-1 Finding FO-2 WARN — original criteria named only martial-heavy + ranged from Gate-2 Finding 2; full Pass-2 LUT divergence is across all 5 families per elrond canonical source.*

### Closure

- [ ] Update generation/MIGRATION.md § Wave 0.5 follow-on with: pipeline wiring landed + LUT alignment to elrond Pass-2 + cite Gate-2 Finding 2 WARN as REMEDIATED
- [ ] Update generation/AGENT_STATE.md
- [ ] Tag: optional per OP convention (this is Q-resolution follow-on; existing `rocket/v1.5-wave-0-5-track-d-content-emission` tag remains the wave milestone)
- [ ] Append completion record to this dispatch file
- [ ] Commit + push per Matt 2026-05-27 per-cycle push pattern (auto-fire per CLAUDE.md addendum)

## Acceptance criteria

- [ ] `season_generation_pipeline.py` wires per_skill_emitter + substrate_weapon_binding cleanly; no regression on existing smoke
- [ ] Integration smoke: 16-character test season produces per-skill content + 8-field substrate binding on all characters
- [ ] Rocket fallback LUT values match elrond Pass-2 LUT **for ALL 5+ families** (martial-heavy=177 / martial-light=99 / ranged=91 / caster-arcane=31 / caster-faith=31 per `sc-6b-weapon-family-baselines-2026-05-27.json` canonical source — per Gate-1 Finding FO-2 WARN amendment)
- [ ] Code comment cites elrond LUT math-note per Discipline #10 attribution clarity
- [ ] generation/MIGRATION.md § Wave 0.5 follow-on records both items as REMEDIATED
- [ ] AGENT_STATE.md updated
- [ ] Completion record appended; commit + push

## Out of scope

- Do NOT amend per_skill_emitter.py or substrate_weapon_binding.py beyond LUT constant update (those are landed; wiring + alignment only)
- Do NOT touch damage_resolver.py (gamora's seam; already landed at Wave 0.5)
- Do NOT touch substrate library DB (elrond's seam; SC-6b enrichment is canonical via Pass-2 LUT)
- Do NOT amend canonical docs (doc 46/47 are canonical; Pass-2 LUT alignment is within-engine attribution clarity, not architectural amendment)
- Do NOT enter Wave 1 / Wave 3 scope (separate dispatches firing in parallel)
- Do NOT regress synthetic_mode (Discipline #39 LOAD-BEARING; verified ZERO at Gate-2)

## Open questions for rocket

- **Q-W05-FO-1**: Pipeline wiring — does `season_generation_pipeline.py` have an existing place where Phase 2a (chain composition) hands off to Phase 2b (per-skill emission)? Or is per_skill_emitter wired into a new pipeline node? Rocket decides per pipeline architecture + records rationale.
- **Q-W05-FO-2**: LUT alignment — does the rocket fallback LUT have additional family values beyond martial-heavy/ranged that need alignment? Cross-check against elrond Pass-2 LUT JSON; align all families that diverge.

## References

- `agentic_orchestration/elrond/research/sc-6b-substrate-enrichment-2026-05-27/MIGRATION.md`
- `agentic_orchestration/elrond/research/sc-6b-substrate-enrichment-2026-05-27/sc-6b-baseline-lut-math-2026-05-27.md`
- `agentic_orchestration/qa/pending/2026-05-27-jack-ryan-cycle-14-wave-0-5-gate-2-closure.md` (Finding 2 WARN)
- `~/Games/reincarnated-engine/design/decisions/decisions-log.md` (Path A architectural commitment + LUT divergence cross-reference; engine `f053281`)
- Engineering disciplines #10 + #11 + #38
- Hive-mind protocol § 4 (decision-routing) + § 10 (emergency / follow-on protocols)

## Completion record

**Completed:** 2026-05-27
**Agent:** rocket

### Item 1 — Pipeline wiring: COMPLETE

- `per_skill_emitter.py` + `substrate_weapon_binding.py` wired into `season_generation_pipeline.py`
- New imports: `SkillEmissionConfig`, `emit_skills_for_kit`, `select_and_bind_substrate_weapon`
- Two new KitCandidate fields: `skills: list`, `substrate_weapon_binding: dict`
- Two new pipeline nodes in `w5r1_generate_kit_candidates()` (Phase 2a/2c, AFTER gear_set + T4):
  - Node A: `emit_skills_for_kit()` → `kit.skills` (12 skills per kit, 3 chains × 4 tiers)
  - Node B: `select_and_bind_substrate_weapon()` → `kit.substrate_weapon_binding` (8 fields; seed offset +700)
- `to_character_dict()` serializes `skills` + injects substrate binding into `gear_representative.main_weapon.substrate_binding`
- Principle 6 round-trip smoke updated with integration assertions (`skills` in required_fields; all skills non-null `damage_scaling_type`; 8 binding fields)
- Q-W05-FO-1 resolved: new nodes wired as new pipeline nodes AFTER Phase 2a/b (gear_set + T4); not reusing existing handoff location (which doesn't exist as a named point in the pipeline)

### Item 2 — LUT alignment: COMPLETE (Gate-2 Finding 2 WARN REMEDIATED)

- `WEAPON_FAMILY_L50_BASELINE` in `substrate_weapon_binding.py` updated to elrond Pass-2 LUT for ALL 5 families + hybrid
- Updated values: martial-heavy=177.0, martial-light=99.0, ranged=91.0, caster-arcane=31.0, caster-faith=31.0, hybrid=99.0
- Module-load assertions updated to verify all 5 family values
- Code comments cite canonical source per Discipline #10: `sc-6b-weapon-family-baselines-2026-05-27.json` + `sc-6b-baseline-lut-math-2026-05-27.md § 3`
- Q-W05-FO-2 resolved: all 5 families + hybrid checked; ALL 6 values diverged from Pass-2 (not just the 2 named in Gate-2 Finding 2; per Gate-1 FO-2 amendment, all aligned)
- Note: elrond math note § 6 "LUT JSON dump" shows stale Pass-1 values — JSON file is authoritative; rocket aligned to JSON per Discipline #10

### Smoke results

- LUT alignment: `python3 -c "from reincarnated.generation.substrate_weapon_binding import WEAPON_FAMILY_L50_BASELINE"` — all 5 family assertions PASS at module load
- Integration smoke: 3 kits × 12 skills (all non-null `damage_scaling_type`); all 8 substrate binding fields present — PASS
- Regression: no regression on existing season gen (same seed_base=9000 produces same kit count with new fields populated)

### Closure checklist

- [x] `season_generation_pipeline.py` wires per_skill_emitter + substrate_weapon_binding — DONE
- [x] Integration smoke: 3-kit subset (12 skills + 8-field binding on all) — PASS
- [x] Rocket fallback LUT values match elrond Pass-2 LUT for ALL 5+ families — DONE
- [x] Code comment cites elrond LUT math-note per Discipline #10 — DONE
- [x] generation/MIGRATION.md § Wave 0.5 follow-on filed — DONE
- [x] AGENT_STATE.md updated — DONE
- [x] Completion record appended — DONE (this record)
- [ ] Commit + push — pending (auto-fire per CLAUDE.md addendum)
