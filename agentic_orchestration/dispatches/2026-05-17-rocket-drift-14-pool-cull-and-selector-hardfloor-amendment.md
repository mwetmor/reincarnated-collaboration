# Dispatch — 2026-05-17 — rocket — Drift-14 pool-cull execution + D1 rubric selector hard-floor amendment

**From:** knight-rider (authored as side-output of gandalf Drift-14 Track B synthesis per dispatch `2026-05-16-gandalf-drift-14-track-b-pool-cull-and-selector-hardfloor-synthesis.md`)
**To:** rocket
**Approved by:** Matt at 2026-05-17 (cascade-fire authorization per Day-4 close directive: "I really don't want to ship any more canonically biased seasonal themes" + Day-5 Drift-14 VS2a-gating confirmation; rocket-side execution conditional on Matt re-approval after reviewing this dispatch + the canonical-side decisions doc)
**Status:** PENDING — DRAFTED. Substrate-expansion design doc landed (gandalf commit `1df535b` 2026-05-17); HOLD condition lifted. **Requires Matt fire-approval only.** Amendment scope finalized per gandalf substrate-expansion doc:
- D1 rubric extension ADDS `substrate_native` as third dimension alongside `canonical_pair_leak` + `vfx_catalogue_mapping_clean`
- Pool D1 re-score scopes 156 entries across **6-substrate target state** (fire/water/earth/wind/lightning/holy/shadow) per design doc § 5.2
- **CRITICAL constraint:** vocab freeze remains active during re-score; 7 frozen entries (thunder/lightning/bolt/holy/divine/shadow/umbra) re-score to substrate-native primary slots but do NOT lift to allow-list until Phase-1 P1 activates 6-substrate runtime
- VS2a/VS2b runtime selection stays canonical-four-bounded (selector allow-list filter unchanged)
- Optional 4th D1 dimension `freeze_list_member` (advisory per gandalf; surface to rocket scoping but not blocking)

Per gandalf cascade order (substrate-expansion doc § 6): decisions-log entry drafts AFTER this dispatch fires so log references unified state. Gate-1 friendly post-Matt-approval (single-seam execution; cross-seam contract change properly flagged per R11(b)).
**Estimated effort:** ~4-6 hours (schema extension ~30min; manifest authoring ~1h; selector code changes ~1h; pool.json re-scoring + auto-demote logic ~1h; validation run ~30min; smoke test + tag ~30min; MIGRATION.md authoring ~30min)
**Tag intent (intermediate):** `rocket/v1.4-drift14-pool-cull-and-selector-amendment-1` post-smoke; Matt-approved milestone tag may follow per ADR-004 conventions.

**Acceptance:** Pool-cull execution applied to `data/seasonal_elements/pool.json` per § 1 of `canonical/story/drift-14-pool-cull-decisions-2026-05-17.md`; D1 rubric selector hard-floor amendment (minimum-viable cut: Tracks 1+2; defer Track 3) implemented in `element/schema.py` + `element/selector.py`; catalogue-coverage manifest authored at `data/seasonal_elements/vfx_coverage_manifest.json`; re-scoring run validates resulting status distribution matches § 1 target ± reasonable delta; MIGRATION.md entry authored for cross-seam impact (gamora simulation consumes pool via balance-loop selection; star-lord LLM-bound paths consume via prompt construction; drax consumes via VFX-mapping at render); smoke + tag.

---

## Why this dispatch exists — Drift-14 closure execution

Per gandalf commit `8a89d1b` § Drift-14 re-amendment (VS2a-gating reclassification) + canonical-side decisions doc `canonical/story/drift-14-pool-cull-decisions-2026-05-17.md`:

The 156-entry seasonal-element pool was D1-rubric scored at Stage A1 (commit `98f1e3f`) against conceptual visualizability + fantasy-heroic + genre-precedent + common-vocabulary properties. **The rubric did NOT score VFX-catalogue-mapping coherence.** This is a structural enforcement gap: the rubric pushes selector toward canonical-four conformity even while claiming to enable per-season variety — a form-bias instance the cipher migration Stage 1 was supposed to close.

Track A (legolas, RETURNED) gathered empirical data; Track B (gandalf, RETURNED) synthesized canonical-side decisions. This dispatch is the rocket-side execution.

**Two-part change:**

1. **Pool-cull execution** — apply gandalf's per-entry cull decisions (27 actions) to `pool.json`. Reduces allow-list from 81 → ~55; reshapes selector distribution to break canonical-four bias.
2. **Selector hard-floor amendment** — add `vfx_catalogue_mapping_clean` boolean gate (required for allow-list status) + `canonical_pair_leak` audit flag to schema + selector. Closes the structural enforcement gap.

## Cross-seam contract change — R11(b) clause

**This dispatch ships a cross-seam contract change.** The `PoolElement` schema is consumed by:

- **Gamora (simulation seam):** via balance-loop pool sampling — sees pool entries' `d1_status`; cull rebalances which entries can be sampled at allow-list weight
- **Star-lord (LLM seam):** via prompt construction in `llm/naming.py` and `element/selector.py:_SYSTEM_PROMPT` — sees the post-cull pool composition when constructing element-selection prompts AND the D1 Phase-C scoring prompt construction at `_build_d1_rubric_questions`
- **Drax (loadout/demo seam):** via export packet (post-Stage-3 cipher migration) — sees the per-season vocabulary selected from the post-cull pool

**R11(b) required clause (chosen path):** MIGRATION.md entry. Author MIGRATION.md entry at `reincarnated-engine/MIGRATION.md` (or `reincarnated-engine/design/migrations/2026-05-17-drift-14-pool-cull-and-selector-amendment.md` per current convention) covering:

- Schema change (PoolElement field additions: `vfx_mapping_tier`, `vfx_catalogue_mapping_clean`, `canonical_pair_leak`)
- Pool composition change (allow-list distribution shift; selector sampling weight redistribution)
- Manifest-file dependency (NEW: `data/seasonal_elements/vfx_coverage_manifest.json`)
- Downstream consumer impact:
  - **Gamora:** no schema reader changes required (consumes via pool.py load path; new fields are additive with defaults); pool sampling distribution shifts (empirical change, not API change) — flag for empirical validation in next regen
  - **Star-lord:** `_score_novel_word` prompt update (new Q6 + Q7); element-selection prompt may need update to reference new VFX-coverage gate semantics (verify per § 5.1 of canonical doc; star-lord prompt-template audit side-routing)
  - **Drax:** no schema reader changes required (consumes via export packet, downstream of Stage 3 cipher migration); empirical change to per-season vocabulary entries selected post-cull
- Sequencing: this change ships WITH Stage 3 (combined cascade per PATH-D1 finding); Stage 3 launch checklist add precondition #4 (this dispatch landed)

## What this dispatch produces

### Section 1 — Pool-cull execution

Apply the 27 cull actions from `canonical/story/drift-14-pool-cull-decisions-2026-05-17.md` § 1 to `data/seasonal_elements/pool.json`.

**Pre-execution: reconcile with legolas Track A per-entry annotations.**

Gandalf's first-principles derivation in § 1.4 of the canonical doc (the "remaining 12 cull candidates") may differ slightly from legolas's exact per-entry findings. If you have access to legolas's inline-delivered per-entry annotations (via session transcript or filed at `agentic_orchestration/research/knowledge/pool-vfx-coverage-audit-2026-05-16.md` if subsequently filed), reconcile:

- Where legolas's per-entry annotations agree with gandalf's call: execute the cull as gandalf specified
- Where legolas's per-entry annotations specify a different action (e.g., gandalf says CULL → eligible, legolas says CULL → quarantine): defer to legolas's per-entry call (legolas had access to actual catalogue inspection data; gandalf had aggregate)
- Where legolas flagged an entry gandalf missed entirely: cull per legolas's per-entry call; surface to gandalf for canonical-doc amendment
- Where gandalf flagged an entry legolas didn't: maintain gandalf's cull; surface to gandalf for canonical-doc note

**Cull execution (per canonical doc § 1.2 / § 1.3 / § 1.4):**

**§ 1.2 critical allow-list — 7 entries → quarantine:**
- `chitin` (earth, d1_total=11) → quarantine
- `scale` (earth, d1_total=11) → quarantine
- `horn` (earth, d1_total=11) → quarantine
- `tooth` (earth, d1_total=11) → quarantine
- `claw` (earth, d1_total=11) → quarantine
- `throne` (earth, d1_total=11) → quarantine
- `marrow` (earth, d1_total=9) → quarantine

**§ 1.3 wind-storm cluster — 1 keep, 7 cull:**
- `gale` (wind, d1_total=10) → KEEP at allow-list (representative)
- `hurricane` (wind, d1_total=11) → eligible
- `cyclone` (wind, d1_total=10) → eligible
- `tempest` (wind, d1_total=10) → eligible
- `gust` (wind, d1_total=9) → eligible
- `howl` (wind, d1_total=9) → quarantine (auditory)
- `typhoon` (wind, d1_total=9) → eligible
- `squall` (wind, d1_total=9) → eligible

**§ 1.4 other demotions — ~12 entries** (verify against legolas annotations; gandalf-derived from pattern):
- `bone` (earth, d1_total=11) → eligible
- `thorn` (earth, d1_total=11) → eligible
- `husk` (earth, d1_total=8) → quarantine
- `shell` (earth, d1_total=8) → quarantine
- `blood` (water, d1_total=11) → eligible
- `mercury` (water, d1_total=11) → eligible
- `pearl` (water, d1_total=8) → quarantine
- `whisper` (wind) → quarantine
- `hum` (wind) → quarantine
- `sigh` (wind) → quarantine
- `whistle` (wind) → quarantine
- `breath` (wind) → quarantine

**For each cull action:**
- Update `d1_status` field in the entry
- DO NOT modify `d1_total` (preserves audit trail of original rubric score)
- Add `cull_tag` field (NEW; optional convention) noting the rationale tag from canonical doc — e.g., `"cull_tag": "drift-14-biological-organic"`, `"cull_tag": "drift-14-wind-storm-cluster-collapse"`, `"cull_tag": "drift-14-auditory-non-visual"`. (This is operationally optional but architecturally valuable for future audits.)

### Section 2 — D1 rubric selector hard-floor amendment

Implement the MINIMUM-VIABLE cut per canonical doc § 2.2:

**2.1 — Schema extension (`element/schema.py:PoolElement`):**

Add three new fields with backward-compat defaults:

```python
class PoolElement(BaseModel, frozen=True):
    # ... existing fields ...
    # NEW (Drift-14): VFX-catalogue-mapping coherence dimension
    vfx_mapping_tier: str = "unscored"           # "A" | "B" | "C" | "D" | "E" | "unscored"
    vfx_catalogue_mapping_clean: bool = False    # True iff tier in {A, B}; gates allow-list eligibility
    canonical_pair_leak: bool = False            # True iff entry name structurally implies canonical-four pair binding
    # OPTIONAL: cull provenance tag
    cull_tag: str | None = None                  # Rationale tag for any cull action; None for non-culled entries
```

**2.2 — Catalogue-coverage manifest (NEW file: `data/seasonal_elements/vfx_coverage_manifest.json`):**

Author the manifest with per-entry tier + cleanness + canonical-pair-leak flags. Schema:

```json
{
  "version": "1.0",
  "generated_date": "2026-05-17",
  "source_attribution": "Drift-14 Track A (legolas) + Track B (gandalf) joint output",
  "entries": [
    {
      "id": "ember",
      "vfx_mapping_tier": "A",
      "vfx_catalogue_mapping_clean": true,
      "canonical_pair_leak": true,
      "rationale": "direct Pimen fire-spell coverage; lexically implies fire"
    },
    {
      "id": "throne",
      "vfx_mapping_tier": "D",
      "vfx_catalogue_mapping_clean": false,
      "canonical_pair_leak": false,
      "rationale": "conceptual not substance; no clean catalogue mapping"
    }
  ]
}
```

**Coverage requirement:** every entry in `pool.json` MUST have a corresponding manifest entry. Pool-load asserts manifest coverage; on miss, defaults `vfx_mapping_tier="unscored"` + `vfx_catalogue_mapping_clean=False` + logs warning.

**Source for per-entry manifest content:**
- Where legolas Track A annotations specify per-entry tier: USE those
- Where legolas annotations are not available: gandalf provides aggregate guidance in canonical doc § 1; rocket derives conservative defaults (Tier A for direct canonical-slot substances like fire-ember; Tier B for palette-shift substances; Tier C for composite-required; Tier D for custom-required; Tier E for non-visual auditory/conceptual)
- For the cull set (~27 entries), the manifest tier should align with the cull action (Tier D / E for quarantine; Tier C for eligible-borderline)

**Recommendation:** if legolas's per-entry annotations are unavailable AND deriving manifest tiers for 156 entries is heavy lift, scope the manifest authoring as a follow-on commission to legolas/gandalf rather than rocket. In that case, this dispatch ships the SCHEMA + GATE LOGIC + REGRESSION on the cull set only, and the full-pool manifest authoring becomes a follow-on item. Surface this option to knight-rider if applicable.

**2.3 — Selector code changes (`element/selector.py`):**

**a) Pool-load auto-demote (defensive guard):**

At pool-load time (in `load_element_pool` or a new validator wrapper), iterate entries:

```python
def _validate_pool_invariants(pool: list[PoolElement]) -> list[PoolElement]:
    """
    Drift-14 invariant: every allow-list entry MUST have vfx_catalogue_mapping_clean = True.
    Auto-demote violators to 'eligible' at load-time with WARN-level log.
    """
    validated = []
    for entry in pool:
        if entry.d1_status == "allow-list" and not entry.vfx_catalogue_mapping_clean:
            log.warning(
                "Drift-14 invariant violation: '%s' is allow-list but vfx_catalogue_mapping_clean=False; "
                "auto-demoting to eligible. Fix pool.json or vfx_coverage_manifest.json.",
                entry.name,
            )
            entry = entry.model_copy(update={"d1_status": "eligible"})
        validated.append(entry)
    return validated
```

**b) Phase-C scoring extension (`_build_d1_rubric_questions` + `_score_novel_word`):**

Add Q6 and Q7 to the rubric question construction:

```python
# Q6 — VFX-catalogue-mapping coherence
q6 = (
    f"6. Does \"{word}\" map to a 2D-VFX-catalogue-renderable visual register for "
    f"the {primary_slot} slot — either direct coverage (canonical-slot VFX as-is) or "
    f"simple palette-shift on canonical-slot VFX? Answer N if the word requires "
    f"custom VFX commission (e.g., a conceptual or biological-organic substance) "
    f"or has no visual register at all (e.g., auditory or purely abstract)."
)

# Q7 — canonical-pair-leak audit flag (audit-only; not a demotion criterion)
q7 = (
    f"7. Does \"{word}\" structurally imply the canonical-four label binding "
    f"(e.g., 'gale' implies 'wind', 'cinder' implies 'fire', 'tide' implies 'water')? "
    f"This is an audit flag — Y/N — not a quality gate."
)
```

Update the prompt to expect 7 answers; update parsing:

```python
raw_score = sum(2 for a in answers[:5] if str(a).strip().upper() == "Y")  # Q1-Q5: existing
vfx_clean = str(answers[5]).strip().upper() == "Y"                        # Q6: new
canonical_leak = str(answers[6]).strip().upper() == "Y"                   # Q7: new

# Combined score: Q6 adds 2 pts to total if Y (so max becomes 12); Q7 is audit-only
if vfx_clean:
    raw_score += 2
genre_bonus = 0
total = raw_score + genre_bonus

# Status threshold update: allow-list requires BOTH total >= 8 AND vfx_clean
if total >= 8 and vfx_clean:
    d1_status = "allow-list"
elif total >= 5:
    d1_status = "eligible"
else:
    d1_status = "quarantine"

# Persist new fields on the resulting PoolElement
# (caller in add_proposal_to_pool needs update to write vfx_catalogue_mapping_clean + canonical_pair_leak)
```

**c) Threshold constants:** `D1_ACCEPT_THRESHOLD = 7` remains; add `D1_ALLOW_LIST_THRESHOLD = 8` constant for clarity (currently inline in `_score_novel_word`). The new gate is the AND with `vfx_clean`, not a threshold change.

### Section 3 — Re-scoring run + validation

After Sections 1 + 2 land:

**3.1 — Run pool-load validation:**

```bash
python -c "
from reincarnated.element.pool import load_element_pool
pool = load_element_pool()
from collections import Counter
status_dist = Counter(e.d1_status for e in pool)
print('Post-amendment d1_status distribution:', dict(status_dist))
# Sanity check: every allow-list entry has vfx_catalogue_mapping_clean
for e in pool:
    if e.d1_status == 'allow-list':
        assert e.vfx_catalogue_mapping_clean, f'INVARIANT VIOLATION: {e.name}'
print('Invariant OK: all allow-list entries have vfx_catalogue_mapping_clean=True')
"
```

**3.2 — Compare to § 1 target:**

Expected target distribution: ~55 allow-list / ~46 eligible / ~55 quarantine (from canonical doc § 1.5; exact numbers depend on legolas reconciliation).

**3.3 — Surface discrepancies:**

If auto-demote logic moved entries NOT in § 1's cull list, surface those entries with their tier/cleanness justification. These are either:
- Cases where the manifest tier was set stricter than gandalf's cull → confirm with gandalf
- Cases gandalf missed in § 1.4 → confirm with gandalf for canonical-doc amendment

### Section 4 — MIGRATION.md authoring

Author MIGRATION.md entry at the appropriate path (per current convention; recommend `reincarnated-engine/design/migrations/2026-05-17-drift-14-pool-cull-and-selector-amendment.md` if migrations are per-file, or append to monolithic `reincarnated-engine/MIGRATION.md`).

**Required content:**

- **Schema change:** PoolElement field additions (3 fields, all with backward-compat defaults; reader-side: no required changes for consumers using `**entry` deserialization)
- **Data change:** pool.json `d1_status` redistribution (27 entries shift status; selector behavior change is empirical, not API)
- **New file dependency:** `data/seasonal_elements/vfx_coverage_manifest.json` (pool-load consumes this)
- **Behavior change:** pool-load now applies an auto-demote invariant check (allow-list entries without `vfx_catalogue_mapping_clean=True` are demoted to eligible with WARN log)
- **Cross-seam impact analysis:**
  - Gamora: no API change; empirical change to pool sampling distribution; recommend post-merge regen as standard practice
  - Star-lord: D1 Phase-C scoring prompt now includes Q6 + Q7 (new prompt content); if star-lord has separate LLM-prompt audits or integration tests for the scoring prompt, those need update; flag for star-lord-side review
  - Drax: no immediate impact (Stage 3 cipher migration is downstream; this change ships WITH Stage 3 per canonical doc § 4)
- **Sequencing requirement:** ships WITH Stage 3 cipher migration; Stage 3 dispatch launch checklist adds this as precondition #4
- **Cross-references:** canonical doc, Drift-14 audit entry, this dispatch

### Section 5 — Smoke + tag

**Smoke (recommended scope):**

- Generate 5-seed mini-regen using post-cull pool (one season per seed; element selection only; no full sim run required)
- Assert no allow-list entry is the wind-storm cluster (except `gale`); assert no allow-list entry is in the 7 critical-allow-list cull set
- Verify Phase-C scoring path for one novel-word test case (e.g., propose word "echo" or "lattice"; verify Q6/Q7 are sent; verify result writes new fields)
- Log post-cull selector distribution across 100 seeded selections per slot; verify wind-storm cluster aggregate selection rate dropped from ~62% to ~14% (per canonical doc § 1.3 math)

**Tag:** `rocket/v1.4-drift14-pool-cull-and-selector-amendment-1` post-smoke. Milestone tag (Matt-approved) deferred to combined post-cascade regen completion.

## Out of scope (explicit)

- **NO Track 3 (cluster effective-selection-probability floor) implementation.** Deferred per canonical doc § 2.2 (rationale: cull-plus-collapse solves wind-storm structurally; floor mechanism is over-engineered for current problem). Revisit if post-cull empirical regen surfaces a new cluster-pressure pattern.
- **NO selector code refactor beyond the scoped Q6/Q7 + auto-demote + threshold updates.** Existing weighted-sampling architecture remains.
- **NO Stage 3 cipher migration work.** This dispatch ships WITH Stage 3 as combined cascade; Stage 3 is star-lord's dispatch.
- **NO vendor acquisition work.** That's a Matt-decision-routing item per canonical doc § 3; knight-rider routes.
- **NO drax-side VFX-asset wiring.** Separate workstream.
- **NO gamora-side selector-consumer changes.** New schema fields are additive with defaults; no reader changes required.
- **NO authoring of star-lord prompt-template updates** beyond the Phase-C scoring path in `element/selector.py`. The downstream `llm/naming.py` prompt-template work is part of Stage 3 cipher migration (star-lord seam).
- **NO removal of any pool entries.** Cull means d1_status change only; entries remain in pool.json with audit-trail intact.

## Required reading

- `canonical/story/drift-14-pool-cull-decisions-2026-05-17.md` — the canonical-side decisions; § 1 has per-entry cull list; § 2 has rubric amendment spec; § 4 has PATH-D1 sequencing
- `agentic_orchestration/dispatches/2026-05-16-gandalf-drift-14-track-b-pool-cull-and-selector-hardfloor-synthesis.md` — the dispatch that produced the canonical doc
- `data/seasonal_elements/pool.json` — the source-of-truth being modified
- `data/seasonal_elements/element-pool.md` — design-doc reference; slot affinity context
- `src/reincarnated/element/schema.py` — schema being extended
- `src/reincarnated/element/selector.py` — selector code being modified
- `src/reincarnated/element/pool.py` — pool-load code where invariant validator lands
- `agentic_orchestration/research/catalogue/cross-vendor-substrate-inventory-2026-05-16.jsonl` — VFX vendor inventory backing the manifest content
- `agentic_orchestration/research/cipher-migration-paths-audit-2026-05-16.md` — the 48 runtime sites; PATH-D1 is the upstream path
- `reincarnated-engine/design/working-agreement/engineering-disciplines.md` R11(b) — cross-seam round-trip discipline (motivates MIGRATION.md authoring)
- `reincarnated-engine/design/working-agreement/engineering-disciplines.md` Discipline #1 (math-before-code), #4 (right tool for the validation question), #13 (implicit-pillar drift)
- `agentic_orchestration/dispatches/2026-05-16-star-lord-form-bias-stage-3-cipher-migration.md` — Stage 3 dispatch; add this dispatch as precondition #4 in the launch checklist (knight-rider authorship of that update; rocket flags for routing)
- Legolas Track A inline-delivered findings — if available via session transcript; for per-entry manifest tier reconciliation. If unavailable, proceed with gandalf's first-principles guidance + conservative manifest-authoring (see Section 2.2 Recommendation).

## Acceptance criteria

- [ ] Pool-cull execution applied to `data/seasonal_elements/pool.json` per canonical doc § 1 (27 actions); audit trail preserved (`d1_total` unchanged; `cull_tag` annotation optional but recommended)
- [ ] PoolElement schema extended with `vfx_mapping_tier`, `vfx_catalogue_mapping_clean`, `canonical_pair_leak` (+ optional `cull_tag`) fields with backward-compat defaults
- [ ] Catalogue-coverage manifest authored at `data/seasonal_elements/vfx_coverage_manifest.json` (full-coverage of pool.json entries) — OR follow-on commission surfaced if scope is too heavy to land in this dispatch
- [ ] Pool-load validator implements auto-demote of allow-list entries with `vfx_catalogue_mapping_clean=False` (WARN log)
- [ ] Phase-C scoring (`_score_novel_word`) extends to Q6 + Q7; status threshold gates allow-list on `vfx_clean=True`
- [ ] MIGRATION.md entry authored covering schema change + behavior change + cross-seam impact + Stage 3 sequencing requirement
- [ ] Re-scoring smoke run validates post-amendment status distribution within reasonable delta of canonical doc § 1.5 target
- [ ] Smoke + tag (`rocket/v1.4-drift14-pool-cull-and-selector-amendment-1`)
- [ ] Cross-seam side-routing items surfaced to knight-rider:
  - Star-lord prompt-template audit (per canonical doc § 5.1)
  - Stage 3 launch checklist precondition #4 update
  - Manifest-authoring follow-on commission (IF rocket scoped out per Section 2.2 Recommendation)
- [ ] Completion record filled with: cull count actually applied, status distribution before/after, any discrepancies from canonical doc § 1 target with rationale, smoke output reference, MIGRATION.md path

## Tag policy

- **Intermediate tag:** `rocket/v1.4-drift14-pool-cull-and-selector-amendment-1` post-smoke (per ADR-004 intermediate tag convention)
- **Milestone tag (Matt-approved):** deferred — combined post-cascade regen completion will trigger a milestone tag covering pool-cull + Stage 3 + other VS2a items per knight-rider sequencing

---

## Completion record

**Completed:** 2026-05-17
**Cull actions applied:** 21 of 27 expected (delta: 5 auditory entries already quarantine before dispatch — whisper/hum/sigh/whistle/breath required no action; 1 entry was gale which was KEEP not cull; count reconciles to 21 actual state-changes from 22 listed targets)
**Pool status distribution (post-amendment):**
- Post-cull (pool.json only): 60 allow-list / 50 eligible / 46 quarantine
- Post-load with auto-demote: **57 allow-list / 53 eligible / 46 quarantine** (total: 156)
- Canonical doc § 1.5 target: ~55 allow-list / ~46 eligible / ~55 quarantine
- Delta explanation: 5 auditory entries already quarantine before cull (counted as cull-candidates in aggregate but required no action); 3 auto-demoted beyond § 1 list (lantern/torch/tinder — see discrepancies below)

**Schema fields added:** `vfx_mapping_tier` (str, default "unscored"), `vfx_catalogue_mapping_clean` (bool, default False), `canonical_pair_leak` (bool, default False), `substrate_native` (str, default ""), `cull_tag` (str|None, default None)

**Manifest authored:** `reincarnated-engine/data/seasonal_elements/vfx_coverage_manifest.json` (156 entries; full coverage; Tier distribution A=29/B=57/C=41/D=21/E=8; conservative first-principles derivation from legolas Track A aggregate + gandalf Track B decisions + cross-vendor-substrate-inventory-2026-05-16.jsonl)

**MIGRATION.md entry:** `reincarnated-engine/src/reincarnated/element/MIGRATION.md` (new file; element seam)

**Math note:** `reincarnated-engine/design/notes/drift-14-d1-substrate-native-rescore-math-2026-05-17.md` (Discipline #1; filed before code)

**Smoke output reference:** Inline in AGENT_STATE.md. Key results:
- Invariant OK: all 57 allow-list entries have vfx_catalogue_mapping_clean=True
- Cull verification: 11 quarantine + 10 eligible correctly placed
- Wind allow-list post-cull: [cloud, dust, frost, gale, hail, plume, sleet] — storm cluster = gale only
- Storm selection-pressure: ~57% → ~14% of allow-list weight (4× reduction, consistent with canonical doc § 1.3)
- Vocab-freeze: no frozen entries in pool.json (thunder/bolt/divine/umbra reserved for Phase-1 P1)
- Q6/Q7 rubric: 7-question prompt confirmed; allow-list gate now requires vfx_clean=True
- 26/26 test_element_selector.py pass

**Tag:** `rocket/v1.4-drift14-pool-cull-and-selector-amendment-1` @ commit `65e6d77`

**Cross-seam side-routing surfaced:**
- Star-lord prompt-template audit: YES — flagged for knight-rider routing. Q6/Q7 additions to `_build_d1_rubric_questions` need audit against `llm/naming.py:_elements_summary_line()` + Stage 3 cipher migration rubric changes + `element/selector.py:_SYSTEM_PROMPT`. Surfaced in MIGRATION.md § cross-seam impact analysis.
- Stage 3 launch checklist update: NOT yet authored (knight-rider seam). Dispatch flags this as routing item for knight-rider to update the star-lord Stage 3 dispatch with precondition #4.
- Manifest-authoring follow-on: NOT needed. Full 156-entry manifest authored in this dispatch.

**Discrepancies / surfacings for gandalf:**
- **3 additional auto-demotions beyond canonical doc § 1 cull list:** `lantern`, `torch`, `tinder` — all fire-slot allow-list entries that received Tier C VFX tier in the manifest (object framing; not substances; no direct catalogue entry). Auto-demote fired correctly per the new vfx_catalogue_mapping_clean invariant. These are correctly demoted; surface to gandalf for canonical-doc amendment note if desired.
- **5 auditory entries already quarantine:** whisper/hum/sigh/whistle/breath were listed as § 1.4 cull candidates in canonical doc but were already at quarantine in pool.json. No action taken; no discrepancy in outcome — target state achieved.
- **Legolas per-entry annotations unavailable:** gandalf's first-principles derivation used as-is per dispatch § 1.4 guidance. Manifest tier assignments are conservative; if legolas per-entry annotations surface later, recommend a manifest update pass.

**Notes for knight-rider:**
1. **This dispatch satisfies Stage 3 precondition #4** (per canonical doc § 4.2 Option B decision). Stage 3 dispatch launch checklist needs updating.
2. **Decisions-log entry can now be authored** — pool is in unified post-cull state; `substrate_native` field is on-schema; Phase-1 P1 cascade can now be sequenced.
3. **Vendor acquisition routing:** CraftPix premium wood-nature (HIGH — gates earth-slot post-cull rebuild), Fellor Crystal pack (MED — supports kept entries). Both need Matt approval per canonical doc § 3.
4. **Gamora recommendation:** post-merge regen advised to validate selector distribution against canonical doc § 1.3 math (storm-register ~14% of allow-list weight vs ~57% pre-cull).
5. **Phase-1 P1 substrate expansion:** schema is ready (`substrate_native` field present; `_VOCAB_FREEZE_IDS` enforcement in pool.py). Knight-rider can begin sequencing Phase-1 P1 dispatch chain when VS2a+VS2b ship.
