# Dispatch — 2026-06-02 — QDX-3 — Single-entry-point QD-engine workflow fire script

**From:** knight-rider (orchestrator)
**To:** rocket (PRIMARY — engine generation seam owner)
**Authority:** Matt 2026-06-02 QDX chain Locks A-P preserved + LOCK Q (QD-engine workflow integration authority; ADDITIVE-ONLY) + LOCK R (QDX-5 fire parameters bounded by KR + rocket + star-lord)
**Wave:** cycle-17 QDX QD-Engine Re-Fire — Phase 1 (parallel with QDX-1 + QDX-2)
**State file:** `agentic_orchestration/cycle-17-qdx-qd-engine-re-fire/wave-state.md`
**Tag intent:** `rocket/v1.5-qdx-3-qd-engine-fire-script-<n>`
**Estimated horizon:** ~1-2 sessions

---

## 1. Authoritative reading (READ before any code work)

1. **`canonical/39-qd-engine-end-to-end-workflow-2026-05-24.md`** § 1 (full workflow visual flow — Phase 1 archive inspection → Phase 2 generation [substrate-bound + multi-T4 + spec-driven gear] → Phase 3 sim convergence → Phase 4 archive insertion → Phase 5 cohesion + naming → Phase 6 visual [deferred Cycle 15+] → Phase 7 gate [2-LAYER for Cycle 14 v1] → Phase 8 export) — THE pipeline this script orchestrates
2. **`canonical/story/2026-06-02-season-archive-realm-expansion-pivot.md`** § 3 (architectural commitments preserved)
3. **`~/Games/reincarnated-engine/src/reincarnated/generation/season_generation_pipeline.py`** (Cycle 13 wave 5 lineage — the existing QD-engine workflow entry point; reference for module composition + sequencing patterns)
4. **`~/Games/reincarnated-engine/src/reincarnated/generation/phase5_pm1_multimodal_clustering.py`** (cohesion clustering; faction emergence at Phase 5b)
5. **`~/Games/reincarnated-engine/src/reincarnated/generation/phase5_skill_naming.py`** (THE Phase 5 naming module; QDX-1 will add `ws1a4_active=True` parameter; QDX-3 fire script invokes Phase 5 with that activation)
6. **`~/Games/reincarnated-engine/src/reincarnated/generation/phase5_t4_narration.py`** (T4 narration)
7. **`~/Games/reincarnated-engine/src/reincarnated/llm/phase5_orchestrator.py`** (Phase 5 LLM orchestration; reference for LLM-call composition)
8. **`~/Games/reincarnated-engine/scripts/eaa5_kit_space_first_fire_20260602.py`** (EAA-5 v2 reference — the FAILED-path (ClassGenerator instead of QD-engine workflow); QDX-3 is the corrected path)
9. **`~/Games/reincarnated-loadout/public/engine-state/season-001/`** (Cycle 14 wave-5 historical output — visual reference for richness target: Pareto + faction clusters + Wave B identity)
10. **`agentic_orchestration/cycle-17-qdx-qd-engine-re-fire/wave-state.md`** (QDX wave-state; LOCK Q + R + S + escape clauses)

---

## 2. Target seam + scope

**Owner seam:** generation (rocket); reads from llm + export seams (already-stable APIs)

**Target file:** `~/Games/reincarnated-engine/scripts/qdx_qd_engine_re_fire_20260602.py` (NEW; date-suffixed per script convention)

**Scope:**

Author a single-entry-point fire script that composes the QD-engine workflow with WS1A.4-lite + kit_space emit + Wave A/B identity LLM + multi-T4 selection. Each phase invokes existing engine modules (via QDX-1 + QDX-2 wirings); the script is the orchestration layer that produces Cycle 14 wave-5-equivalent + WS1A.4-lite output in a single invocation.

**Phases the script orchestrates (per canonical 39 § 1):**

1. **Phase 1 — Archive state inspection** (gamora module if present; OR best-substitute that produces a BC-target queue or substrate-cell coverage analysis adequate for n_candidates seed at Phase 2)
2. **Phase 2 — Candidate kit generation** (BC-target-driven + substrate-bound + multi-T4 + spec-driven gear per doc 39 + doc 40)
   - `n_candidates` (LOCK R parameter; KR-selected; Cycle 14 wave-5 reference ~650; engine performance bounds may dictate lower if substrate or compute is constrained)
3. **Phase 4 — Pareto reduction** (substrate-led; ~30-40 surviving kits per LOCK R)
4. **Phase 5 — Cohesion clustering + skill naming + T4 narration**
   - Phase 5a: cohesion clustering → ≥3 named factions (phase5_pm1_multimodal_clustering)
   - Phase 5b: skill naming with `ws1a4_active=True` (per QDX-1 wiring)
   - Phase 5c: T4 narration (phase5_t4_narration)
5. **Wave A — Faction naming LLM** (per canonical 39 § 1 Phase 5 spirit-guide explainer; faction-level naming after cohesion clusters identified)
6. **Wave B — Per-kit emergent identity LLM** (per canonical 39 § 1 Phase 5 archetypal player-facing naming; emergent kit concept per kit)
7. **Phase 7 — Gate** (2-LAYER per canonical 39 § 5.7 Cycle 14 v1: mechanical + cohesion)
8. **Phase 8 — Export via kit_space emitter** (per QDX-2 wiring; routes through workflow terminal phase when skip_*=True)

### Fire parameters (LOCK R — bounded; no Matt-touch within these)

```python
# LOCK R defaults (KR-selected; bounded by engine performance + cost projection)
N_CANDIDATES = 200              # KR-selected (Cycle 14 wave-5 was ~650; QDX-3 starts lower for cost+wall-clock bound; tune per smoke results)
PARETO_TARGET = 35              # ~30-40 surviving range per LOCK R
COHESION_MIN_FACTIONS = 3       # ≥3 factions emerge per LOCK R
WS1A4_ACTIVE = True             # per LOCK Q QDX-1 wiring
WAVE_A_LLM_ACTIVE = True        # faction naming LLM
WAVE_B_LLM_ACTIVE = True        # per-kit emergent identity LLM
T4_SELECTION_ACTIVE = True      # multi-T4 per canonical 43/44/47
SKIP_THEME_COALESCENCE = True   # EAA-2 default (Realm Expansion)
SKIP_COSMOLOGICAL_VOCABULARY = True  # EAA-2 default (Realm Expansion)
SEED = 20260602                 # date-based; deterministic-where-applicable
```

**Cost projection (Discipline #1.1 — REQUIRED before tagging):**

Pre-fire resource-bounds projection MUST be computed in the script (logged at startup) — including:
- Phase 5 skill naming: ~n_pareto_kits × 7 skills avg × 1 LLM call/skill = ~245 calls (PASS-only; reroll may inflate × 1.5)
- WS1A.4-lite: ~n_pareto_kits × 7 skills avg × 1 LLM call/skill = ~245 calls (physical opt-out reduces; ~7/8 of total)
- Wave A faction naming: ~3-5 LLM calls (per faction; small)
- Wave B per-kit identity: ~n_pareto_kits × 1 LLM call = ~35 calls
- T4 narration: per canonical_43/44/47 T4 algorithm cost projection

**Total projection:** ~$5-15 (Pareto-fired; LOCK R upper-bound $30 allows comfortable margin). If projection >$60 at startup → ABORT and escalate (LOCK R escape).

**Out of scope (CRITICAL — do NOT touch):**
- Semantic behavior of existing season_generation_pipeline.py for other callers (the script may CALL into it, but does NOT amend its existing semantics for non-QDX callers)
- Re-implementing Phase 2 / Phase 4 / Phase 5 modules — the script CONSUMES existing modules via composition
- WS1A.4-lite module itself (consumed via QDX-1 wiring; no changes)
- kit_space_emitter module itself (consumed via QDX-2 wiring; no changes)
- Any change to Q18 lock contents (IMMUTABLE)

---

## 3. Acceptance criteria

### 3.1 Functional

1. **Single invocation produces Cycle 14-equivalent + WS1A.4-lite output** — `python scripts/qdx_qd_engine_re_fire_20260602.py` runs end-to-end and emits ~30-40 kits to `data/kit_space/` with full identity emergence.

2. **All 8 phases execute in canonical 39 order** — Phase 1 → 2 → 4 → 5 (a/b/c) → Wave A → Wave B → 7 → 8. Phase 6 (visual coalescence) DEFERRED per canonical 39 § 5.6 Cycle 14 v1; Phase 7 is 2-LAYER per canonical 39 § 5.7.

3. **Pareto reduction surviving count in 30-40 range** — when n_candidates=200 (or whichever LOCK R parameter is selected) is fed in, Pareto reduction produces 30-40 kits. If outside range, the script logs a WARNING + continues; if <20, ABORT per LOCK R escape.

4. **Cohesion clustering produces ≥3 named factions** — Phase 5a output has ≥3 cohesion clusters; Wave A LLM names them.

5. **Per-skill flavor-or-canonical naming via WS1A.4-lite active** — Phase 5b fires WS1A.4-lite per-skill (per QDX-1); non-physical kits have `ws1a4_*` metadata on skill nodes; physical kits opt out per Architecture A.

6. **Wave B per-kit emergent identity** — each surviving kit has a unique emergent identity (e.g., "Necromancer of the Pale Court", "Frost-Witch of the Glacial Marches") — NOT template "Element Archetype" generic. If template-repeat detected (e.g., all kits named "{Element} {Archetype}"), Gate-2 BLOCK + LOCK L iteration.

7. **Multi-T4 selection per kit** — each kit's `t4_selection` field is populated (not null); per canonical 43/44/47 multi-T4 semantics.

8. **Output emits via kit_space emitter (per QDX-2)** — `data/kit_space/kit_space_chronicle.json` has new event entry; `data/kit_space/kits/kit_<primary>_<seq6>.json × n` files exist; FK linkage verified.

9. **Generation parameters captured in chronicle** — chronicle event_id's `generation_parameters` dict captures n_candidates, pareto_target, cohesion_min_factions, ws1a4_active, wave_a/b_llm_active, t4_selection_active, skip flags, seed, ws1a4_flavor_rate, llm_cost breakdown.

### 3.2 Pre-fire smoke gate (Discipline #54 + LOCK S preparation)

10. **Pre-fire script smoke** — the script MUST support a `--smoke` mode that fires Phase 1 + a single-candidate Phase 2 + a minimal Phase 4 (`pareto_target=1`) + Phase 5 (single-kit) + Wave A (1 faction) + Wave B (1 kit) + T4 (1 kit) + Phase 7 (1 kit) + Phase 8 emit. Smoke ≤ $0.10 LLM cost. Smoke verifies pipeline composition before LOCK S full QDX-4 smoke-gate.

11. **Smoke variety check** — smoke single-kit MUST have ≥1 ws1a4_flavor=True skill AND ≥1 ws1a4_flavor=False skill (variety check); MUST have non-null `t4_selection`; MUST have non-template emergent identity.

### 3.3 Documentation

12. **Docstring at script top** — comprehensive docstring per `eaa5_kit_space_first_fire_20260602.py` pattern: pipeline summary, fire parameters, cost projection (Discipline #1.1), authority citation, dispatch reference, tag intent.

13. **Per-phase logging** — each phase logs entry + exit with timing + key counts (n_candidates, n_survived_pareto, n_factions, n_skills_named, ws1a4_flavor_rate, etc.).

### 3.4 Resource bounds (Discipline #1.1)

14. **Pre-fire resource-bounds projection logged at startup** — script logs projected LLM cost + projected memory peak + projected wall-clock before doing any expensive work. If projection >$60 → ABORT + escalate (LOCK R escape).

15. **Memory peak bounded** — per Discipline #46 (Phase 4 protection); per-cell bounding for math gates; prevents O(n²) kernel-panic-class failures as candidate pool grows.

---

## 4. Smoke-test expectation

`python scripts/qdx_qd_engine_re_fire_20260602.py --smoke` runs in <5 minutes wall-clock; <$0.10 LLM cost. Expected output structure (illustrative):

```
=== QDX-3 QD-Engine Re-Fire (SMOKE MODE) ===
Pre-fire resource-bounds projection:
  Projected LLM cost: $0.07 (smoke; ≤$0.10 bound)
  Projected wall-clock: ~3 min
  Projected memory peak: ~200 MB
  ABORT threshold: $60 (LOCK R escape) — NOT TRIGGERED
[PASS: pre-fire bounds]

=== Phase 1 — Archive state inspection ===
BC-target queue produced: 1 cell
[OK]

=== Phase 2 — Candidate generation ===
n_candidates=1 (smoke)
generated: 1 kit (shadow primary)
[OK]

=== Phase 4 — Pareto reduction ===
pareto_target=1 (smoke); surviving: 1 kit
[OK]

=== Phase 5a — Cohesion clustering ===
n_clusters=1 (smoke)
[OK]

=== Phase 5b — Skill naming (ws1a4_active=True) ===
skills_named: 7
ws1a4_flavor_decisions: True=3, False=4 [variety check PASS]
phase5_attempts: avg 1.0; PASS rate 100%
[OK]

=== Phase 5c — T4 narration ===
t4_selection: populated [PASS]
[OK]

=== Wave A — Faction naming LLM ===
1 faction named: "Pale Court Ascendants"
[OK]

=== Wave B — Per-kit emergent identity ===
kit identity: "Necromancer of the Pale Court" [non-template PASS]
[OK]

=== Phase 7 — Gate (2-LAYER) ===
mechanical: PASS
cohesion: PASS
[OK]

=== Phase 8 — Emit via kit_space ===
event_id: kse_20260602_003
kit JSON: data/kit_space/kits/kit_shadow_000026.json
chronicle entry written
FK linkage verified
[OK]

=== Smoke COMPLETE ===
wall_clock: 2.7 min
llm_cost: $0.064 [PASS: under $0.10]
```

---

## 5. Cross-seam impact + MIGRATION.md

- **generation seam (rocket):** primary; depends on QDX-1 (Phase 5 WS1A.4-lite wiring) and QDX-2 (terminal-phase kit_space routing). If QDX-1 or QDX-2 aren't tagged, QDX-3 smoke will fail at the depending phase; script may be authored with import fallbacks for parallel-development testing but the FULL fire requires QDX-1 + QDX-2 PASS.
- **export seam (star-lord):** consumed via QDX-2; no direct cross-seam contract changes from QDX-3.
- **llm seam (star-lord):** Phase 5 + Wave A/B LLM calls consume LLM client (existing infrastructure); cost telemetry composes per existing pattern.
- **MIGRATION.md** entry recommended: `~/Games/reincarnated-engine/src/reincarnated/generation/MIGRATION.md` § new entry: "QDX-3 — single-entry-point fire script composing QD-engine workflow with WS1A.4-lite + kit_space emit; reference fire-script for kit-space-expansion events".
- **ADR-004 compliance:** the script is a generation-seam orchestration layer; no NEW cross-seam contracts; uses existing imports.

---

## 6. Tag intent

`rocket/v1.5-qdx-3-qd-engine-fire-script-<n>`

---

## 7. Critique-pair coverage

- **Gate-1 (DESIGN-MODE):** jack-ryan reviews this dispatch BEFORE rocket fires. Common Gate-1 catches: missing pre-fire bounds projection; missing variety smoke check; missing n_candidates → pareto_target sizing rationale; missing Wave A vs Wave B distinction.
- **Gate-2 (DEV-MODE):** jack-ryan reviews the tagged commit + smoke output. Common Gate-2 catches: regression on existing pipeline; template-repeat emergent identity (Wave B prompt failure); cost overrun; FK linkage broken.
- **LOCK L iteration discipline:** if Gate-2 BLOCKs on Wave B template-repeat → seam re-fires Wave B prompt within authority (1st BLOCK); 2+ BLOCKs → Matt escalation per LOCK R escape.

---

## 8. Quality criterion

**Game-quality goal this dispatch serves:** with a single `python scripts/qdx_qd_engine_re_fire_20260602.py` invocation, the QD-engine workflow produces the Cycle 14 wave-5-equivalent richness experience composed with WS1A.4-lite per-skill flavor naming throughout. The result: ~30-40 kits in the continuous kit_space, each with a distinct emergent identity, grouped into ≥3 emergent factions, with per-skill thematic flavor on non-physical kits — i.e., the empirical artifact that closes Matt's actual chain-close goal.

**Refutation conditions** (rocket surfaces if any apply):
- This dispatch contradicts canonical 39 phase ordering or semantics (alters QD-engine workflow non-additively)
- Alternative execution (e.g., re-firing EAA-5 v2 ClassGenerator with parameters tweaked) would deliver the named quality goal better
- Acceptance criteria can pass without advancing the quality goal (e.g., 35 kits emitted but all template-repeat names, OR Wave B fires but produces "Element Archetype" generic, OR multi-T4 fires but all kits have identical T4 selection)
- Dispatch framing pre-commits to a decision Matt has not ratified
- Dispatch introduces a pre-authored taxonomy without justification (#41 candidate)
- Dispatch introduces a scaffold value not flagged as pending-decision (#40) — e.g., n_candidates=200 is a KR-selected scaffold; rocket may amend within LOCK R if engine performance dictates
- Cost projection exceeds LOCK R escape threshold (>$60)

---

## 9. Required completion record

On work-completion (Phase 1 close; before QDX-4 smoke-gate fires), append a completion record block to this dispatch file with:

```markdown
## Completion record

**Completed by:** rocket (date)
**Tag:** `rocket/v1.5-qdx-3-qd-engine-fire-script-<n>`
**Engine commit:** `<sha>`
**Script path:** `scripts/qdx_qd_engine_re_fire_20260602.py`
**Smoke output:** <paste smoke run output; including variety check + cost + FK linkage>
**Cost projection vs actual (smoke):** projected $<x> / actual $<y>
**Phase composition verified:** Phase 1 → 2 → 4 → 5(a/b/c) → Wave A → Wave B → 7 → 8 [PASS]
**Dependencies on QDX-1 / QDX-2:** <verified PASS / pending integration tests>
**Gate-2 verdict:** PASS / PASS-with-INFO / BLOCK + jack-ryan finding file path
**Notes for QDX-4 smoke-gate:** <any parameters for the formal LOCK S smoke fire; e.g., suggested seed, suggested primary>
**Notes for QDX-5 full fire:** <any tuning recommendations based on smoke; e.g., adjust n_candidates if engine performance bound hit>
```

---

**End of QDX-3 dispatch.**
