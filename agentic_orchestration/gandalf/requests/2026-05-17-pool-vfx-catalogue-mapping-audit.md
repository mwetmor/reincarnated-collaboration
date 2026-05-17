# Gandalf request to knight-rider — Pool × VFX catalogue mapping audit (Drift-14 gap closure)

**From:** gandalf
**To:** knight-rider (for legolas + gandalf joint dispatch authoring)
**Date:** 2026-05-17 (Day 4 evening into Day 5 close)
**Authorized by:** Matt direct ("yes please" 2026-05-17 following Drift-14 surfacing)
**Type:** Bounded gap-closure commission — adds `vfx_catalogue_mapping_clean` property to D1 rubric; produces culled pool for VS2b cipher migration ship
**Estimated effort:** Combined ~1-2 days. Legolas Mode A ~3-5h; gandalf re-scoring ~4-6h.

**Source artifact:** `canonical/story/drift-audit.md` § Drift-14 (Per-season vocabulary pool scored on D1 rubric but not against VFX-catalogue-mapping coherence) — Pattern P6 instance.

---

## Why this commission exists

The 156-entry seasonal-element pool (`data/seasonal_elements/pool.json`) was D1-rubric scored Stage A1 (commit `98f1e3f`) against conceptual visualizability + fantasy-heroic + genre-precedent + common-vocabulary properties. **The rubric did NOT score whether each entry maps cleanly to our 2D elemental / VFX catalogue.**

Cipher migration architecture (per `canonical/37-form-bias-diagnosis-and-recovery.md` § 6 + `canonical/story/form-bias-cadence-strategy.md` § 7.2) commits to:
- L1 substrate (canonical-four) drives **VFX**
- L3 per-season vocabulary drives **player-visible labels**

This works elegantly *only if* L3 vocabulary entries are conceptually VFX-coherent with their canonical slot. Failure mode: a season selects `throne` (earth-allow-list, D1 total=11) as the earth-slot substance; demo renders earth-canonical VFX (stone particles); player-visible label reads "throne strike." Cognitive dissonance.

**Pre-VS2b-ship gap.** Pre-Stage-3 cipher migration, the gap is camouflaged (LLM still sees canonical-four). Post-Stage-3 + drax-side Stage 3 + manifest parallel structure → per-season vocabulary goes player-visible end-to-end → throne-strikes-with-stone-VFX become observable.

---

## Two-track commission

### Track A — Legolas Mode A: VFX catalogue concept-coverage audit

**Owner:** legolas (Mode A — analytical research; read-only)
**Estimated effort:** 3-5h
**Output:** `agentic_orchestration/research/knowledge/pool-vfx-catalogue-mapping-audit-2026-05-17.md`

**Scope:**

1. **Inventory VFX catalogue concept-coverage** for the canonical-four slots (fire / wind / water / earth):
   - **Direct coverage:** which substance-concepts does Pimen GREEN-list (11/13 elements) + CreativeKind palette-shift capability render as-is? Examples: `fire-canonical → cinder / ember / scorch / blaze / spark` all direct; `earth-canonical → granite / stone / sand / clay` all direct.
   - **Palette-shift coverage:** which substance-concepts require ONLY a palette shift on existing VFX to render coherently? Examples: `water-canonical + blue → ice / glacier`; `water + silver → mercury`; `water + white-reflective → pearl`.
   - **Compositing coverage:** which substance-concepts require palette + compositing (e.g., adding sparkle overlay; texture-replacement)? Examples: `obsidian` (earth + dark + glossy); `amber` (earth + warm + translucent).
   - **Custom-VFX required:** which substance-concepts have no clean catalogue mapping? Examples: `throne` (conceptual); `marrow` (biological); `whisper` (auditory).

2. **For each of the 156 pool entries**, assign a `vfx_mapping_tier`:
   - **Tier A (direct):** maps to canonical-slot VFX with no modification
   - **Tier B (palette-shift):** maps with palette change only
   - **Tier C (composite):** maps with palette + minor compositing
   - **Tier D (custom-required):** no clean catalogue mapping; bespoke VFX commission would be needed
   - **Tier E (non-visual):** auditory / textural / conceptual entries that cannot render as visual VFX at all

3. **Sub-category flags** for borderline cases (legolas annotates; gandalf adjudicates in Track B):
   - `biological-organic` — bone / marrow / chitin / claw / horn / scale / thorn / tooth / husk / shell (earth-primary but visually distinct from mineral)
   - `liquid-specific` — blood / mercury / pearl / honey / nectar (water-primary but distinct from canonical water visual)
   - `conceptual-abstract` — throne / threshold / hearth (no substance-shape to render)
   - `auditory` — whisper / hum / sigh / thrum / breath / exhalation / whistle / howl
   - `textural` — gauze / silk / gossamer / feather (textile-like, not weather)

**Constraints:**
- Read-only across all sources
- $0 LLM budget; pure analytical research + existing catalogue inspection
- 5h time cap; surface findings-blockers if Pimen + CreativeKind coverage data is insufficient

**Required reading:**
- `data/seasonal_elements/pool.json` (the 156-entry pool — source of entries)
- `data/seasonal_elements/element-pool.md` (design-doc reference; slot affinity context)
- `agentic_orchestration/research/catalogue/cross-vendor-substrate-inventory-2026-05-16.jsonl` (Step B Tier-1 VFX inventory)
- `canonical/story/style-register.md` (consumption-time filter framing)
- `canonical/story/geometry-vfx-coverage-assessment.md` (existing VFX coverage assessment)
- Pimen pack docs for the GREEN-list 11/13 elements (per existing catalogue records)

### Track B — Gandalf re-scoring pass + rubric extension

**Owner:** gandalf
**Estimated effort:** 4-6h (depends on Legolas Track A return)
**Output:** Three artifacts:

1. **Rubric extension proposal** at `canonical/story/d1-rubric-vfx-mapping-extension-2026-05-17.md`:
   - Document the new `vfx_catalogue_mapping_clean` rubric property
   - Define operational scoring methodology (Tier A=2 pts, Tier B=1 pt, Tier C=0.5 pt, Tier D=0 pt, Tier E=-2 pt as demotion)
   - Bridge to existing D1 rubric (extend max from ~11 to ~13)
   - Define new pool-status thresholds: vfx-clean (≥10 combined; allow-list eligibility); vfx-acceptable (8-9; eligible eligibility); vfx-blocked (≤7; quarantine — irrespective of D1 score)

2. **Per-entry re-scoring** at `data/seasonal_elements/pool.json` (or amendment file):
   - Add `vfx_mapping_tier` field per entry (consumes legolas Track A annotations)
   - Add `vfx_mapping_score` numeric per entry (per scoring methodology)
   - Update `d1_status` per the new combined-score thresholds (some allow-list entries may demote; some quarantine entries may stay quarantine; net pool composition shifts)

3. **Culled-pool summary** at `canonical/story/pool-vfx-mapping-culled-2026-05-17.md`:
   - List of entries demoted/promoted
   - Specific findings (e.g., "throne demoted allow-list → quarantine due to vfx-Tier-D; whisper stays quarantine due to vfx-Tier-E auditory")
   - Selector-side implications (does selector need a hard-floor on vfx_mapping_tier?)

**Constraints:**
- Gandalf authors directly (canonical-story design-steward scope)
- Knight-rider drafts decisions-log entry capturing the rubric extension after gandalf surfacing (post-authorship)
- No selector code changes in this commission; if hard-floor selector logic is recommended in artifact 3, separate rocket dispatch follows

**Required reading (gandalf):**
- Legolas Track A return doc (the operational anchor for Track B)
- Same source set as Track A

---

## Acceptance criteria

- [ ] Track A: legolas doc filed at `agentic_orchestration/research/knowledge/pool-vfx-catalogue-mapping-audit-2026-05-17.md`; 156 entries each have `vfx_mapping_tier` assignment + sub-category flag where applicable
- [ ] Track B artifact 1: rubric extension doc filed; methodology defined; Matt-readable
- [ ] Track B artifact 2: pool.json amended with new fields; entries re-scored; status updated per combined-score
- [ ] Track B artifact 3: culled-pool summary doc filed; demotion/promotion deltas enumerated
- [ ] Cross-references between Track A + Track B docs are reciprocal
- [ ] Drift-14 entry in `canonical/story/drift-audit.md` updated with resolution status

---

## What this commission unblocks

- Stage 3 cipher migration ship-readiness verification — pool is ready for player-visible per-season vocabulary
- VS2b loadout embodiment-narrative display — narrative beats reference per-season vocabulary that visually coheres with VFX
- Forward catalogue work (VS2c+ Tier-2/Tier-3 vendor sweeps) — D1 rubric extension applies to future pool additions; no new entries land without VFX-mapping scoring

---

## Sequencing relative to in-flight work

Independent of:
- Movement-speed cascade (rocket schema-defaults + gamora Gate 3b + drax MS implementation)
- Stage B export-DTO fix (star-lord)
- B6 main + skill-tree UI (rocket + gamora + drax)
- Path A-prime monster scale lookup work
- Case A / Case D Fire_Lord swap dispatches (separate sprite-scale workstream)

Can run in parallel with all the above; only consumes legolas + gandalf bandwidth.

**Recommended priority:** moderate. Drift-14 is pre-VS2b-ship gap, not VS2a-blocking. Sequencing flexibility means knight-rider can route legolas Track A when capacity allows; gandalf Track B follows legolas return.

---

## Discipline #15 candidate input (forward-flag)

This commission's output produces the empirical-basis input for a Discipline #15 candidate (per Drift-11 sibling-cluster-sweep prescription + P6 sub-pattern naming from `p6-forward-audit-2026-05-16.md`):

**D15 candidate text:** *"Pool-vs-catalogue mapping must be scored at pool-introduction time, not deferred to ship-time. Any pool entry that will become player-visible at a downstream ship MUST be scored against the operational catalogue at pool-introduction time, not just against conceptual rubric properties."*

Surface to next jack-ryan engineering-disciplines pass alongside R11(b) + Pattern P7 silent-drop cluster + Drift-11 sibling-cluster-sweep lesson.

---

— gandalf, 2026-05-17 (Day 4 evening into Day 5 close)
