# Dispatch — 2026-06-02 — EAA-5 v2 RE-FIRE — `ClassGenerator` path

**From:** knight-rider (orchestrator)
**Primary owner:** star-lord (script execution + emit + Gate-2 coordination)
**Co-owner:** rocket (already authored root-cause diagnosis + v2 script; consult if needed)
**Cycle:** cycle-16-eaa-engine-architectural-amendment (Phase 2 v2 iteration)
**Authority:** Matt 2026-06-02 + Locks A-P (LOCK L iteration discipline: first BLOCK → seam re-fire authority; LOCK N first-fire parameters)
**Wave tag:** `EAA-5-v2`
**Predecessor v1 BLOCK finding:** `agentic_orchestration/qa/findings/2026-06-02-eaa-5-v1-first-fire-gate-2-block.md`
**Rocket root-cause investigation:** captured in agent `a1edce40c35768f1c` final report (preserved in KR session record)
**Estimated horizon:** 1 session — ~5-10 minutes execution + Gate-2 inspection + commit + push

---

## 1. Context — v1 BLOCK summary

EAA-5 v1 fire produced 25/25 physical kits with `skills: []` because the call-site invoked `BcTargetSubspaceGenerator` (new v2.0 generator; substrate-cell stub layer) and passed stubs directly to `emit_kit_space_expansion_event()` without running Layer-3 generation phases. `BcTargetSubspaceGenerator.infer_element_from_name()` returns `"physical"` as residual fallback for any canonical-weapon name lacking elemental keywords; physical weapons (swords/axes/etc.) all hit the fallback. WS1A.4-lite fired zero times.

v1 output remains on disk (preserved per pre-commit HOLD); kit JSONs at `data/kit_space/kits/kit_physical_000001.json` through `_000025.json` + chronicle event `kse_20260602_001`. NOT committed.

## 2. v2 recovery — already AUTHORED

**v2 script:** `reincarnated-engine/scripts/eaa5_kit_space_first_fire_20260602.py` (authored by star-lord post-v1; currently untracked)

**Key amendments per rocket diagnosis:**
- Uses `ClassGenerator` (canonical pipeline; matches Cycle 14 + season_orchestrator pattern) instead of `BcTargetSubspaceGenerator`
- Explicit per-primary round-robin element assignment (canonical-7 + physical opt-out distribution)
- Invokes Layer-3 skill generation phases (chain composition + t4 selection + supporting chain + skill generation) before emit
- WS1A.4-lite fires per-skill via `apply_kit_space_skill_naming_batch()` for non-physical kits
- Phase 5 cohesion judge fires per-skill for naming review

**Dry-run validation (per rocket investigation):** 25/25 kits + 8/8 elements represented + 5-12 skills per kit (avg 9.1). Lightning/holy/shadow B6 builder falls back to standard generator (non-fatal INFO logs). Experimental kit triggers stat-allocator fallback warning (non-fatal).

## 3. Execution sequence

### 3.1 Pre-fire cleanup (per jack-ryan BLOCK recommendation)

Star-lord clears v1 defective artifacts before v2 fires:

```bash
# Preserve forensic record by NOT removing — instead reset directory state
rm /Users/admin/Games/reincarnated-engine/data/kit_space/kits/kit_physical_*.json
# Reset chronicle to empty events array
cat > /Users/admin/Games/reincarnated-engine/data/kit_space/kit_space_chronicle.json <<'EOF'
{"schema_version": "1.0", "events": []}
EOF
```

**Rationale:** v1 output is preserved in the BLOCK finding + rocket investigation report (forensic record). On-disk cleanup is required so v2 fire produces clean kit_space state (no orphan physical-only kits alongside diverse v2 kits). Per jack-ryan BLOCK finding pre-commit gate.

**Alternative (NOT recommended):** preserve v1 kits alongside v2 kits — would pollute kit_space with stub content misrepresenting pipeline capability. KR rejects this alternative.

### 3.2 v2 fire

Run the v2 script with `ANTHROPIC_API_KEY` set:

```bash
cd /Users/admin/Games/reincarnated-engine
ANTHROPIC_API_KEY=<set> python scripts/eaa5_kit_space_first_fire_20260602.py
```

**Expected output:**
- 25 kits at `data/kit_space/kits/kit_<primary>_<seq6>.json` with diverse primaries (~3-4 per of canonical-7+1)
- Chronicle event `kse_20260602_002` (since `kse_20260602_001` exists; rocket diagnosis confirms script anticipates this — actually with v1 chronicle reset per § 3.1, the v2 event will be `kse_20260602_001`)
- Non-empty `skills` arrays (5-12 skills per kit; avg 9.1)
- Populated `chain_composition`, `t4_selection`, `supporting_chain`
- WS1A.4-lite metadata: `flavor_decision: bool` + `flavor_word_used: str | null` per-skill on non-physical kits
- WS2.P2 modern caster weapons surface in non-physical kit weapon selections (substrate-driven)

**Cost projection:** ~$0.50 (168 WS1A.4-lite calls + ~175 Phase 5 calls). Within LOCK L iteration budget. Ceiling at 2× ($1.00).

### 3.3 Post-fire validation

- Verify 25 kits on disk + chronicle event `kse_20260602_001` (post-cleanup reset)
- Verify per-primary distribution spans ≥5 of 8 canonical elements (Gate-2 v1 BLOCK requirement)
- Verify `ws1a4_flavor_rate > 0.0` in chronicle (confirms LLM naming fired)
- Verify FK linkage integrity
- Verify no `.tmp` files left behind
- Spot-check 3-5 kits across different primaries for skill content + naming quality

### 3.4 jack-ryan Gate-2 re-fire (you invoke)

Route v2 output to jack-ryan for STRUCTURAL Gate-2:
- All 5 v2 fire requirements from v1 BLOCK finding (§ v2 fire requirements)
- All 8 EAA-5 acceptance criteria from original dispatch § 6
- Aesthetic spot-check default-accept unless >10% non-grammatical (LOCK L escape clause #3)

If Gate-2 STRUCTURAL PASS + aesthetic acceptable: **EAA-5 closes; Phase 2 complete; Phase 3 unblocks.**

If Gate-2 STRUCTURAL BLOCK: **second BLOCK in EAA-5 sequence → escalate to Matt per LOCK L escape clause** (KR composes Matt surface).

### 3.5 Commit + push

Per Matt 2026-06-02 explicit cycle-push authorization:
- Auto-commit work-products: data/kit_space/ contents + new v2 script + wave-state update + dispatch completion + Gate-2 finding
- Auto-push per established cycle-push pattern
- Tag commit: `star-lord/v1.4-eaa-5-v2-class-generator-fire-1`

Concurrent-write coordination awareness — KR is currently the only meta-repo writer; star-lord may commit directly without absorption risk.

---

## 4. Out of scope

- v1 cleanup deeper than directory reset (BLOCK finding + rocket diagnosis preserve forensic record)
- Cosmetic refinements to flavor naming (aesthetic — Matt-scope only at >10% threshold)
- Additional kit-space-expansion events beyond the n_kits=25 first-fire
- BcTargetSubspaceGenerator amendments (separate workstream if engine wants the v2.0 generator's element-inference behavior corrected; out of EAA chain scope)
- Phase 3 (EAA-6 + EAA-7 drax MVP reframe) — unblocks AFTER EAA-5 Gate-2 PASS
- Integration-smoke-gate discipline (queued for jack-ryan EAA-8 wave-close ratification)

---

## 5. Cross-seam contract

- All ADDITIVE per LOCK J + LOCK K (no new MIGRATION.md required for v2 fire; consumes already-ratified Phase 1 schemas)
- Round-trip not applicable (no new cross-seam contract surface)

---

## 6. Acceptance criterion (per original EAA-5 dispatch § 6 + v1 BLOCK § "v2 fire requirements")

EAA-5 v2 PASSES when:
1. 25 kits generated and emitted to `data/kit_space/kits/`
2. Chronicle event recorded with correct schema + FK regex
3. All 25 per-kit JSONs validate against `validate_per_kit_entry()` (0 validation errors)
4. FK linkage integrity (per-kit event_id matches chronicle event_id)
5. engine_version_sha populated + per-primary distribution spans ≥5 of 8 canonical elements + per-skill flavor_decision metadata populated on non-physical kits
6. WS2.P2 modern caster weapons surface in some non-physical kits
7. jack-ryan Gate-2 STRUCTURAL PASS
8. Aesthetic default-accept (no >10% non-grammatical at per-skill flavor naming)
9. **NEW v2-specific:** `ws1a4_flavor_rate > 0.0` in chronicle (confirms WS1A.4-lite actually fired)

---

## 7. Tag intent + auto-commit/push

- Tag: `star-lord/v1.4-eaa-5-v2-class-generator-fire-1`
- Wave-close milestone tag deferred to EAA-8 (chain-level)
- Auto-commit + auto-push per Matt 2026-06-02 explicit authorization

---

## 8. Report back to KR

On completion:
- Commit shas (engine + meta-repo)
- Chronicle event_id minted
- Per-primary distribution (e.g., fire=3 / water=4 / earth=3 / wind=3 / lightning=3 / holy=3 / shadow=3 / physical=3)
- Sample 3-5 kits showing: kit_id + primary + 1-2 skill names with flavor_decision metadata
- jack-ryan Gate-2 STRUCTURAL verdict
- LLM cost (vs $0.50 projection)
- Phase 3 readiness signal: EAA-6 + EAA-7 unblock

---

## 9. References

- v1 BLOCK finding: `qa/findings/2026-06-02-eaa-5-v1-first-fire-gate-2-block.md`
- Original EAA-5 dispatch: `dispatches/2026-06-02-eaa-5-first-kit-space-expansion-generation-fire.md`
- Original Gate-1 finding: `qa/findings/2026-06-02-eaa-5-first-fire-gate-1.md`
- Canonical commitment: `canonical/story/2026-06-02-season-archive-realm-expansion-pivot.md`
- Joint design spec: `agentic_orchestration/elrond/notes/2026-06-02-eaa-3-plus-4-joint-ingest-and-chronicle-spec.md`
- Chronicle schema: `reincarnated-engine/data/kit_space/chronicle/CHRONICLE_SCHEMA.md`
- v2 script: `reincarnated-engine/scripts/eaa5_kit_space_first_fire_20260602.py` (untracked; commit as part of v2 fire)
- Generator paths: `reincarnated-engine/src/reincarnated/generation/class_generator.py` (canonical; v2 fire) vs `reincarnated-engine/src/reincarnated/generation/bc_target_substrate_engine.py` (v2.0 substrate generator; v1 mis-use)

---

**End of EAA-5 v2 dispatch. Fires after KR signal.**
