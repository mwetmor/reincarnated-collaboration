# Dispatch — 2026-06-02 — QDX-5 — Full QD-engine workflow fire (Option B4 weighted distribution)

**From:** knight-rider (orchestrator)
**To:** rocket (PRIMARY — fire the composed QD-engine workflow at full scale via ClassGenerator Option B path with Option B4 weighted round-robin distribution)
**Authority:** Matt 2026-06-02 Pattern B + gandalf transmission ratifying **Option B + Option B4 weighted distribution** (~40-45% physical / ~55-60% caster across 7 rotating elements). QDX chain Locks A-T preserved + Matt verbatim "No further Matt-touch required before QDX-6 acceptance verification."
**Wave:** cycle-17 QDX QD-Engine Re-Fire — Phase 3 (gates on Phase 2 ✅ PASS-with-INFO + Matt generator-path decision ratified)
**State file:** `agentic_orchestration/cycle-17-qdx-qd-engine-re-fire/wave-state.md`
**Tag intent:** `rocket/v1.5-qdx-5-full-fire-option-b4-1`
**Estimated horizon:** ~1-3 sessions including multi-hour generation execution

---

## 1. Authoritative reading (READ before fire)

1. **`agentic_orchestration/cycle-17-qdx-qd-engine-re-fire/qdx-5-generator-path-strategic-decision-2026-06-02.md`** § 3 Option B (the ratified path) + Matt amendment to Option B4 weighted distribution
2. **Matt + gandalf transmission 2026-06-02** (verbatim "Proceed with QDX-5 fire (Option B4 weighted distribution)") — full guidance in this dispatch § 3
3. **`canonical/story/2026-06-02-eaa-chain-wave-close-record.md`** § EAA-5 v2 (ClassGenerator + round-robin canonical element assignment; the path this dispatch extends with the QDX richness layer)
4. **`canonical/39-qd-engine-end-to-end-workflow-2026-05-24.md`** § 1 (8-phase composition)
5. **`canonical/story/2026-06-02-season-archive-realm-expansion-pivot.md`** § 3 (architectural commitments preserved)
6. **`agentic_orchestration/cycle-17-qdx-qd-engine-re-fire/wave-state.md`** Locks A-T + escape clauses
7. **Phase 1 + Phase 2 deliverables** — `scripts/qdx_qd_engine_re_fire_20260602.py` (engine `cf6e9ae` + amendments `cd3b10c`); `apply_phase5_skill_naming(ws1a4_active=True, ...)` (engine `76adb6e`); `run_qd_engine_terminal_phase()` (engine `9fba775`)
8. **`~/Games/reincarnated-engine/scripts/eaa5_kit_space_first_fire_20260602.py`** (EAA-5 v2 reference for ClassGenerator + element-assignment patterns; QDX-5 EXTENDS this with QDX richness)

---

## 2. Target seam + scope

**Owner seam:** generation (rocket)

**Scope:**

Execute the full QD-engine workflow at production scale via ClassGenerator (Option B) with **Option B4 weighted round-robin canonical element assignment** producing ~30-40 kits at ~40-45% physical / ~55-60% across 7 rotating elements. This is the empirical-truth-moment for the QDX chain.

The fire produces:
- ~30-40 distinct kits in `data/kit_space/` with Wave B emergent identity per kit
- Faction emergence via Phase 5a cohesion clustering (≥3 named factions via Wave A)
- Multi-T4 selection per kit (`t4_selection` not null on all kits)
- WS1A.4-lite per-skill flavor decisions on non-physical kits (`ws1a4_flavor_rate > 0`)
- Physical kits opt out of WS1A.4-lite per Architecture A
- New chronicle event `kse_20260602_007` (or next sequential)

**Out of scope (CRITICAL):**
- Substrate enrichment (parallel future workstream; not gating this fire)
- Drax MVP refresh (QDX-7; sequential after this + QDX-6)
- Any amendments to canonical 39 architecture beyond Option B interpretation already ratified
- Any amendments to existing engine module APIs (LOCK Q ADDITIVE-ONLY preserved)

---

## 3. Fire parameters — Option B4 distribution (Matt + gandalf ratified)

### 3.1 Per-primary distribution target

KR-selected from gandalf transmission Option B4.5 (gandalf-preferred for 30-40 kit roster):

```python
# Option B4.5 distribution (gandalf-preferred; KR-selected)
# Total: 37 kits (within LOCK R 30-40 bound)
# Physical: ~43% (16/37) — within Matt's 40-45% target
# Caster: ~57% (21/37) — within Matt's 55-60% target
TARGET_DISTRIBUTION = {
    "physical": 16,
    "fire": 3,
    "water": 3,
    "earth": 3,
    "wind": 3,
    "lightning": 3,
    "holy": 3,
    "shadow": 3,
}
# Total = 37
```

**Rocket has LOCK R authority to amend the distribution** within Matt's ratified bounds (~40-45% physical ± 5%; total kits within LOCK R 30-40 range):
- If engine performance / substrate availability dictates fewer total kits, scale proportionally maintaining ~40-45% physical
- If LLM cost projection at startup signals upper bound proximity, consider 35-kit version (`physical=14, others=3 each = 35`; ~40% physical)
- If specific element substrate is empty (e.g., shadow has 0 magical-weapon entries), rocket may shift +1 to another rotating element + reduce shadow by 1 (with rationale in completion record)

Other Option B4 sub-options Matt + gandalf endorsed: B4.1 (9-slot rotation ~33% physical), B4.2 (10-slot ~30%), B4.3 (11-slot ~36%), B4.4 (2-of-9 ~44%). KR-pick is B4.5 for predictability + gandalf preference; rocket may switch sub-option if implementation easier.

### 3.2 LOCK R fire parameters (preserved + extended)

```python
# LOCK R baseline (preserved from prior dispatches)
GENERATOR_PATH = "ClassGenerator"        # Option B ratified by Matt 2026-06-02
PARETO_TARGET = 30-40                    # LOCK R bound
COHESION_MIN_FACTIONS = 3                # ≥3 factions emerge per LOCK R
WS1A4_ACTIVE = True                      # per QDX-1 wiring
WAVE_A_LLM_ACTIVE = True                 # faction naming LLM
WAVE_B_LLM_ACTIVE = True                 # per-kit emergent identity LLM
T4_SELECTION_ACTIVE = True               # multi-T4 per canonical 43/44/47
SKIP_THEME_COALESCENCE = True            # EAA-2 default (Realm Expansion)
SKIP_COSMOLOGICAL_VOCABULARY = True      # EAA-2 default (Realm Expansion)
SEED = 20260602                          # date-based; deterministic-where-applicable

# Option B4 amendment
ELEMENT_ASSIGNMENT = "weighted_round_robin"  # NOT pure round-robin
ELEMENT_DISTRIBUTION = TARGET_DISTRIBUTION   # § 3.1

# LOCK R cost + escape thresholds
LLM_COST_PROJECTION_BOUND = 30.0         # $30 LOCK R upper-bound (cost escape >$60 = 2x)
ABORT_COST_THRESHOLD = 60.0              # >$60 → ABORT + escalate per LOCK R
WALL_CLOCK_BOUND_HOURS = 4               # bounded multi-hour expectation
```

### 3.3 Implementation guidance

**Path:** EXTEND `scripts/qdx_qd_engine_re_fire_20260602.py` (NOT a new script) by:

1. Add Option B4 distribution capability:
   - When `--full-fire` (or default non-smoke mode) is specified, use `TARGET_DISTRIBUTION` dict
   - For each `(element, count)` pair, generate `count` kits via ClassGenerator with `dominant_element=element`
   - Existing ClassGenerator pattern from EAA-5 v2 fire script `scripts/eaa5_kit_space_first_fire_20260602.py` is the reference
2. The fire script orchestrates the QDX richness pipeline AROUND ClassGenerator generation:
   - Phase 2 candidate generation = ClassGenerator producing kits per `TARGET_DISTRIBUTION`
   - Phase 4 Pareto reduction = mostly pass-through (the distribution IS the curation); apply Pareto only for tie-breaking if substrate produces >37 candidates per element
   - Phase 5a cohesion clustering = `phase5_pm1_multimodal_clustering` against the 37-kit set
   - Phase 5b skill naming = `apply_phase5_skill_naming(ws1a4_active=True, ...)` per QDX-1 wiring
   - Phase 5c T4 narration + multi-T4 selection
   - Wave A faction naming LLM (post-cohesion)
   - Wave B per-kit emergent identity LLM
   - Phase 7 gate (2-LAYER mechanical + cohesion)
   - Phase 8 emit via `run_qd_engine_terminal_phase()` per QDX-2 wiring → kit_space schema

### 3.4 Pre-fire resource-bounds projection (Discipline #1.1 REQUIRED)

At script startup, log:
- Projected LLM cost breakdown:
  - WS1A.4-lite: ~21 caster kits × ~7 skills avg × 1 call/skill = ~147 calls × ~500 tokens × $0.002/call = ~$0.30
  - Phase 5 cohesion-judge: ~37 kits × ~8 skills avg × 1 call/skill = ~296 calls × ~750 tokens × $0.003/call = ~$0.90 (allowing 1.5x reroll inflation: ~$1.35)
  - Wave A faction naming: ~3-5 calls × ~1000 tokens = ~$0.05
  - Wave B per-kit identity: ~37 calls × ~1000 tokens = ~$0.40
  - T4 narration: ~37 kits × T4 narration cost (~$0.10 per kit) = ~$3.70
  - **Total projection: ~$5-7** (within LOCK R bound)
- Projected memory peak (per Discipline #46 DB anti-materialization)
- Projected wall-clock: ~2-4 hours
- **ABORT if projection > $60 (LOCK R escape clause #2)**

### 3.5 Smoke pre-flight (Discipline #54 composition)

Before full fire, OPTIONAL pre-flight smoke (rocket judgment):
- Run `--smoke` mode at small scale (e.g., 3-5 kits with B4 distribution) to verify the script's Option B4 implementation works correctly
- If smoke confirms, proceed with full fire
- Smoke cost ~$0.10; smoke wall-clock ~5 min

This is a self-smoke per rocket discretion; the formal LOCK S smoke-gate already PASSED at QDX-4.

---

## 4. Acceptance criteria

### 4.1 Original 7 criteria (preserved)

1. Kit count in 30-40 range — Option B4.5 produces 37 kits target
2. Distinct emergent kit identities (no template-repeat across kits sharing primary)
3. Faction emergence ≥3 named clusters
4. Multi-T4 selection populated on all kits (`t4_selection` not null)
5. `ws1a4_flavor_rate > 0`; per-skill `ws1a4_*` metadata present on non-physical kits
6. Substrate-led element distribution — INTERPRETED per Matt-ratified Option B: **substrate determines fill (cultural-tradition + period + skill structure) within each element axis; element axis follows Option B4 weighted round-robin** (NOT pure round-robin; NOT pure substrate-driven)
7. Per-skill flavor decisions thematically coherent (sample inspection)

### 4.2 NEW criterion #8 (Matt + gandalf amendment 2026-06-02)

8. **Per-primary distribution matches Option B4 target** — ~40-45% physical ± 5%; ~55-60% across 7 rotating elements; substrate-led fill WITHIN each element axis. Spotcheck:
   - Physical kits: 14-18 (37 kits @ 16 ± 2)
   - Each rotating element: 2-4 (3 ± 1)
   - Total: 30-40 (LOCK R bound)

### 4.3 Cost + bounds

9. **LLM cost** ≤ $30 (LOCK R upper bound); ABORT triggered if cost projection > $60 at startup
10. **Wall-clock** ≤ 4 hours (LOCK R bound)
11. **No regressions** — existing test suites continue to PASS; LOCK Q ADDITIVE-ONLY preserved

---

## 5. Tag intent + commit + push

Tag: `rocket/v1.5-qdx-5-full-fire-option-b4-1`

Auto-commit + auto-push per CLAUDE.md team commit + push discipline + Matt 2026-06-02 cycle-push authorization.

Commit message should include:
- Engine commit SHA + tag
- Cost actual vs projection
- Wall-clock actual
- Kit count actual + distribution actual (per-primary)
- Event_id minted
- WS1A.4-lite flavor rate aggregate
- Wave A faction names
- Notes for QDX-6 verification

---

## 6. Cross-seam impact + MIGRATION.md

- **No new cross-seam contracts** — uses existing wirings from QDX-1 + QDX-2; consumes existing modules
- **Generation seam:** primary; fire script is the only modified file (additive `--full-fire` or default fire path)
- **Export seam:** no changes (consumed via QDX-2 wiring)
- **LLM seam:** consumed via existing LLM client infrastructure
- **MIGRATION.md** entry recommended at `generation/MIGRATION.md` § QDX-5 — documents the fire script's Option B4 distribution amendment + first canonical-39-equivalent (with Option B path) kit-space-expansion event

---

## 7. Quality criterion

**Game-quality goal this dispatch serves:** with a single command, deliver Matt the Cycle 14 wave-5-equivalent kit-richness experience PLUS WS1A.4-lite per-skill flavor naming PLUS genre-true distribution. ~37 kits in the continuous kit_space, distributed ~43% physical / ~57% caster matching ARPG/JRPG genre convention, each with distinct emergent identity, grouped into ≥3 emergent factions, with per-skill thematic flavor on non-physical kits.

This is the empirical-truth-moment for the entire QDX chain. The artifact this fire produces is what Matt's chain-close goal is empirically tested against.

**Refutation conditions** (rocket surfaces if any apply):
- This dispatch contradicts Matt's 2026-06-02 Option B ratification or Option B4 distribution amendment
- Alternative execution would serve the named quality goal better
- Acceptance criteria can pass without advancing the quality goal (e.g., 37 kits emitted but Wave B all template-repeat; OR distribution within target but every physical kit identical; OR substrate-fill thin enough that kits feel undifferentiated)
- Dispatch framing pre-commits to a decision Matt has not ratified
- Dispatch introduces a pre-authored taxonomy without justification
- Dispatch introduces a scaffold value not flagged as pending-decision (the `TARGET_DISTRIBUTION` dict IS a scaffold flagged at LOCK R amendment authority)
- Cost projection exceeds LOCK R escape threshold (>$60)

---

## 8. Required completion record

On work-completion, append a completion record to this dispatch file with:

```markdown
## Completion record

**Completed by:** rocket (date)
**Tag:** `rocket/v1.5-qdx-5-full-fire-option-b4-<n>`
**Engine commit:** `<sha>`
**Script path:** `scripts/qdx_qd_engine_re_fire_20260602.py` (extended)
**Pre-fire cost projection:** $<x> (vs $30 LOCK R bound; ABORT threshold $60)
**Pre-fire memory projection:** <peak MB>
**Cost actual:** $<y> (vs $<x> projection)
**Wall-clock actual:** <z hours>
**Kit count actual:** <n> (vs 37 target)
**Per-primary distribution actual:** {<element>: <count>, ...}
**% physical:** <p>% (vs ~40-45% target)
**WS1A.4-lite stats:** flavor_count=<a>; canonical_count=<b>; fallback_count=<c>; flavor_rate=<r>; physical_opt_out=<n> kits
**Phase 5 cohesion:** average=<x>; PASS rate=<r>; <n> faction clusters
**Wave A faction names:** [<list>]
**Wave B emergent identities sample:** [<3-5 examples>; verify no template-repeat]
**Multi-T4 selection:** <n>/<n> kits populated
**Event_id:** `kse_20260602_<NNN>`
**Chronicle entry:** WRITTEN; FK linkage PASS/FAIL
**Kit JSONs:** <count>
**Generic-name fallback:** <count> (<%> of total skills)
**Regressions:** none / list
**Gate-2 readiness:** ready for QDX-6 verification
**Notes for QDX-6:** <any verification context; e.g., known WARNs; specific kits worth sample-inspection>
**Notes for QDX-7 (drax MVP):** <any data-shape implications]
```

---

**End of QDX-5 dispatch.**
