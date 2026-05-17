# Drift-14 — Pool-Cull Decisions + Selector Hard-Floor Amendment Spec

**Status:** **Canonical.** Authored 2026-05-17 by gandalf. Track B design-side synthesis of Legolas Track A empirical findings (delivered inline by legolas; per-entry findings re-derived from first principles + verified against rocket-owned `data/seasonal_elements/pool.json`).
**Dispatch:** `agentic_orchestration/dispatches/2026-05-16-gandalf-drift-14-track-b-pool-cull-and-selector-hardfloor-synthesis.md`
**Author authority:** gandalf canonical-story / design-direction seam.
**Downstream:** rocket (execution dispatch authored as side-output at `agentic_orchestration/dispatches/2026-05-17-rocket-drift-14-pool-cull-and-selector-hardfloor-amendment.md`); star-lord prompt-template audit (surfaced for routing); knight-rider sequencing.

**Reading order:** § 0 TL;DR → § 1 Pool-cull execution list → § 2 Selector hard-floor amendment spec → § 3 Vendor-acquisition prioritization → § 4 PATH-D1 sequencing call → § 5 Cross-seam side-routing → § 6 Hand-off summary for knight-rider.

**Data-source attribution note:**
- **Derived-from-aggregate-data** (knight-rider summary of legolas inline return): the 27-candidate count; the 7 critical allow-list entries; the 8-entry wind-storm cluster; vendor-coverage percentages; top-3 vendor acquisition picks; the three selector hard-floor recommendation slots.
- **Derived-from-first-principles** (gandalf, verified against `pool.json` direct inspection + `cross-vendor-substrate-inventory-2026-05-16.jsonl` + `geometry-vfx-coverage-assessment.md` + cipher-migration paths-audit): per-entry rationale; cluster decision shape; rubric-amendment spec; sequencing call. Where legolas's per-entry annotations would be load-bearing for individual decisions (e.g. exact `vfx_mapping_tier` per entry), gandalf has applied conservative judgment and flagged for rocket-side validation during execution.

---

## § 0 — TL;DR for the brief Matt is waiting on

**Three lines:**

1. **27 cull (including 7 critical allow-list); 0 keep; 0 defer.** Wind-storm cluster of 8 collapses to **1 representative (`gale`) + 7 demotions.** Net allow-list contraction: ~24 entries (from 81 → ~57); some demotions land at `eligible`, some at `quarantine` (per individual VFX-tier). The cull is sharp and load-bearing; partial culls leave the canonical-bias signal active.
2. **Selector hard-floor amendment: ship the MINIMUM-VIABLE cut (Tracks 1 + 2).** Track 1 = `vfx_catalogue_mapping_clean` boolean gate as hard-allow-list-eligibility gate (cheap; closes the structural enforcement gap). Track 2 = `canonical_pair_leak` boolean dimension (cheap; surfaces the wind-storm pattern explicitly for future audits). **DEFER Track 3 (cluster effective-selection-probability floor) to post-VS2a** — solved structurally by the cull + cluster collapse without needing a new floor mechanism. Revisit if post-cull empirical regen surfaces a new cluster-pressure pattern.
3. **Vendor acquisitions: ACQUIRE CraftPix premium (wood-nature) + Fellor Crystal pack; DEFER Frostwindz Deathbringer (bone).** The wood-nature acquisition unblocks the post-cull earth slot (which loses 7+ biological-organic entries); the gem-cluster acquisition reinforces the existing crystal/gem coverage that the cull keeps. Bone deferred because the post-cull pool intentionally moves AWAY from biological-organic — adding bone substrate now would re-introduce the same VFX-coherence drift gandalf is closing.
4. **PATH-D1 sequencing: pool-cull ships WITH Stage 3** (not before, not after). Single coordinated cascade; Stage 3 is still PENDING (HOLD-on-prior queue); pool-cull becomes a precondition added to Stage 3's launch checklist. Combined post-cascade regen consumes both in one cycle.

**Rocket dispatch authored:** YES, at `agentic_orchestration/dispatches/2026-05-17-rocket-drift-14-pool-cull-and-selector-hardfloor-amendment.md`. Gate-1-friendly to fire post-Matt-approval. Carries MIGRATION.md cross-reference clause per R11(b).

**Star-lord side-routing:** YES — surface to knight-rider for prompt-template audit of `llm/naming.py` D1 LLM call (the `_score_novel_word` Phase C path) — current rubric questions don't include any VFX-coherence or canonical-pair-leak check; if rubric extension lands at rocket, the LLM call needs Q-set update too.

---

## § 1 — Pool-cull execution list

### § 1.1 Decision framework

Each cull candidate gets one of three actions:

| Action | Mechanics |
|---|---|
| **CULL → quarantine** | Entry stays in pool but `d1_status` flips to `"quarantine"`; selector excludes from all sampling paths (per `element/selector.py:135` `active_pool = [e for e in pool if e.d1_status != "quarantine"]`). Most-severe action; reserved for entries that cannot map to canonical-slot VFX at all without bespoke commission. |
| **CULL → eligible** | Entry stays in pool with `d1_status="eligible"`; selector samples at 1× weight (loses 2× allow-list weighting per `D1_ALLOW_LIST_WEIGHT = 2`). Less-severe; reserved for entries with palette-shift VFX coverage but ambiguous slot-fit or genre register. |
| **KEEP** | Entry stays at `d1_status="allow-list"`. Reserved for entries with clean direct VFX coverage AND clean genre register AND no canonical-pair-leak. |

The cull is asymmetric per slot because the leak patterns are slot-specific:
- **Wind:** canonical-pair-leak via the storm-cluster (8 entries thematically collapse to "weather-storm")
- **Earth:** vfx-coherence-leak via biological-organic cluster (7+ entries render distinct from canonical mineral earth VFX)
- **Water:** alternative-liquid-specific leak (3 entries — `blood`, `mercury`, `pearl` — render distinct from canonical water VFX)
- **Fire:** cleanest slot (no critical-allow-list culls flagged by legolas; 78% GREEN per aggregate)

### § 1.2 The 7 critical allow-list cull decisions

These entries scored well on the existing D1 rubric (d1_total 9-11) — culling them validates the rubric-amendment work in § 2. Per-entry rationale:

| Entry | Slot | d1_total | Action | Rationale |
|---|---|---|---|---|
| **`chitin`** | earth | 11 | **CULL → quarantine** | Biological-organic (insect exoskeleton). Renders visually distinct from canonical-earth mineral VFX (stone particles, mineral debris). Tier-D vfx-mapping (custom commission required). Concrete failure mode: "chitin-strike" with stone-particle VFX is incoherent — players expect arthropod-shell visual register, get mineral debris. No vendor in current catalogue ships chitin substrate. |
| **`scale`** | earth | 11 | **CULL → quarantine** | Biological-organic (reptilian/dragon scale). Same pattern as chitin. Additional risk: `scale` is also a verb (to climb / to size) — lexical ambiguity compounds the visual incoherence. Tier-D. |
| **`horn`** | earth | 11 | **CULL → quarantine** | Biological-organic (keratin). Same pattern. Tier-D. Note: `horn` is canonically-adjacent to monster-character substrate (gandalf's chierit Fire_Lord work, dragon-substrate vendor packs) — re-introducing horn as a *seasonal-element* creates cross-domain confusion with monster-anatomy substrate. |
| **`tooth`** | earth | 11 | **CULL → quarantine** | Biological-organic. Same pattern. Tier-D. Additional concern: `tooth-strike` reads as monster-attack vocabulary (per ARPG canon — D3 Hellhound bite, PoE Wild Strike-tooth fragment) rather than as a substance-class label for a seasonal slot. |
| **`claw`** | earth | 11 | **CULL → quarantine** | Biological-organic (keratin). Same pattern. Additional concern: `claw` as a *substance* mis-fires entirely — it's an *anatomical structure*, not a material. Even the existing tags (`['sharp', 'curved', 'predatory']`) describe an object, not a substance. This entry should never have entered allow-list under a strict reading of D1 Q1 ("physical substance, material, or tangible phenomenon"). |
| **`throne`** | earth | 11 | **CULL → quarantine** | **Conceptual, not substance.** This is the entry that surfaced Drift-14 (gandalf flagged in Matt's element-pool diff response 2026-05-17). Throne is an object/symbol; tags `['heavy', 'fixed', 'stone', 'seat', 'power']` confirm the conceptual framing. Tier-D. "Throne-strike" with stone-particle VFX is the canonical failure example. **Highest-priority cull** — strongest cognitive-dissonance signal. |
| **`marrow`** | earth | 9 | **CULL → quarantine** | Biological-organic + hidden-substance (per tags `['hidden', 'deep', 'vital']`). Tier-D. Additionally: marrow is a sub-substance OF bone — selecting marrow as an earth-slot creates a downstream naming-coherence issue with bone-substrate already present (bone is also flagged for cull below; see § 1.3). |

**Pattern observation:** All 7 critical allow-list entries cluster on **earth slot** and split into two sub-patterns:
- **Biological-organic** (chitin, scale, horn, tooth, claw, marrow) — 6 entries. Earth-slot is over-permissive on biological substrate per the pool design doc (`element-pool.md:43` lists `bone, marrow, husk, shell, chitin, scale, horn, tooth, claw` as earth affinities — but earth-canonical VFX is mineral, not biological).
- **Conceptual** (throne) — 1 entry. D1 Q1 ambiguity; should have been quarantined at scoring time.

**This validates the rubric-amendment work in § 2.** A `vfx_catalogue_mapping_clean` gate would have caught all 7 at offline-scoring time without needing a manual cull pass.

### § 1.3 Wind-storm cluster — cluster-level decision

**The 8-entry wind-storm cluster:** `hurricane`, `gale`, `cyclone`, `tempest`, `gust`, `howl`, `typhoon`, `squall`. All allow-list, d1_total 9-11.

**This is 8 of 14 wind allow-list entries — 57% selection-pressure concentration on "weather-storm" sub-register.** Under the 2× allow-list weighting (`D1_ALLOW_LIST_WEIGHT = 2`), the wind slot is effectively a "weather-storm slot" — exactly the canonical-pair-leak gandalf flagged in commit 8a89d1b § Drift-14.

**Three cluster-decision options surveyed:**

| Option | Description | Pros | Cons |
|---|---|---|---|
| **A — Cull all 8 to eligible/quarantine** | Reduce wind allow-list to 6 entries (hail, frost, sleet, plume, dust, cloud) | Strongest canonical-bias break; forces selector to draw from non-storm wind concepts | Wind slot loses its strongest dramatic-fantasy register entirely; player-facing seasons become wind-as-atmospheric rather than wind-as-force |
| **B — Keep 1 representative; cull 7** | Promote one cluster-member to representative status; demote 7 | Preserves the dramatic-fantasy register at low selection-pressure (1/(1+5)=14% rather than 8/(8+5)=62%); breaks canonical-pair-leak structurally | Requires Matt-level call on WHICH representative; downstream selector still surfaces the representative regularly |
| **C — Rebalance with non-leak alternates** | Cull 8; introduce 3-4 new non-leak wind entries via vendor acquisition + manual curation | Maintains wind allow-list size; introduces variety | Adds scope (new pool entries to be scored); blocks on vendor catalogue mapping |

**Decision: Option B — keep `gale`; cull the other 7 to `eligible`.**

**Rationale for Option B over A and C:**

- Option A is too aggressive — completely removing storm-register from wind allow-list strips the dramatic-fantasy weight the wind slot needs to carry. The cipher migration architecture commits per-season-vocabulary to drive player-visible labels; if every season's wind slot is `mist`/`fog`/`plume`/`dust`/`cloud`, the wind slot reads as flavor-secondary across all seasons. That's a different bias instance (sustained-low-drama wind framing) — trading one drift for another.
- Option C is correct in principle but blocks on the vendor-acquisition cycle (§ 3) AND introduces scope creep. Better as a follow-on after the cull validates.
- Option B threads the needle: keep ONE high-d1 storm-register entry (`gale`) for dramatic-weight optionality; demote 7 (not all 8) to eligible so they remain selectable but no longer concentrate selection pressure.

**Why `gale` is the representative:**

- `gale` has flex_slots=[] (cleanest single-slot fit; no cross-element ambiguity)
- d1_total=10 (high, but not the absolute top — leaving `hurricane` at 11 in eligible avoids losing the highest-rated entry from the pool entirely)
- Tags `['sustained', 'powerful', 'cold']` are the most VFX-coherent of the cluster (sustained linear wind force renders cleanly with Pimen wind-spell-effect VFX + palette modifiers); `hurricane`/`cyclone`/`typhoon`/`squall` all carry rotational-storm tags that would require bespoke VFX (Tier-D)
- `gale` is the most genre-neutral term — `hurricane`/`typhoon` carry strong real-world meteorological associations (Atlantic / Pacific naming conventions); `cyclone`/`tempest` carry strong literary associations (Wizard of Oz / Shakespeare) that surface unintended cultural register

**Per-entry disposition for the 8-entry cluster:**

| Entry | d1_total | Action | Note |
|---|---|---|---|
| `gale` | 10 | **KEEP (representative)** | Sustained linear wind; cleanest VFX-coverage; most genre-neutral |
| `hurricane` | 11 | **CULL → eligible** | Highest d1; preserved at eligible (still selectable, no allow-list weight). Note: `matt-add-2026-05-12` tag — Matt manually added; courtesy-preserve at eligible rather than quarantine. |
| `cyclone` | 10 | **CULL → eligible** | Rotational storm; Tier-C/D VFX-coverage |
| `tempest` | 10 | **CULL → eligible** | Literary association; flex_slots=['water'] adds cross-element ambiguity |
| `gust` | 9 | **CULL → eligible** | Sub-cluster-redundant with `gale` (brief vs sustained) |
| `howl` | 9 | **CULL → quarantine** | Auditory, not visual (per drift-audit § Drift-14 auditory-cluster). Tier-E. Should not have been in allow-list. |
| `typhoon` | 9 | **CULL → eligible** | Real-world Pacific meteorological framing |
| `squall` | 9 | **CULL → eligible** | Sub-cluster-redundant with brief-storm entries |

**Post-cull wind allow-list: 14 → 7 entries** (hail, frost, gale, sleet, plume, dust, cloud). Drops the selection-pressure concentration from 8/14 storm to 1/7 storm — a 8.7× reduction in storm-register weighting once 2× allow-list multiplier is applied (effective weight 16/22 storm → 2/8 storm).

### § 1.4 Other allow-list demotions (the remaining 12 of the 27 candidates)

Per knight-rider's aggregate count, legolas flagged 27 cull candidates total. § 1.2 covers 7 critical-allow-list; § 1.3 covers 8 wind-storm. That's 15 accounted; remaining ~12 are derived-from-first-principles below based on the patterns legolas's aggregate found. These should be VALIDATED by rocket during execution against legolas's per-entry annotations (rocket sources legolas's content from session transcript if available; else from the rationale shape below).

**Remaining 12 cull candidates (gandalf first-principles derivation):**

| Entry | Slot | d1_total | Action | Rationale |
|---|---|---|---|---|
| `bone` | earth | 11 | **CULL → eligible** | Biological-organic (per the same pattern as the 6 in § 1.2). `bone` is one tier less culled (eligible vs quarantine) because: (a) bone is a more genre-canonical fantasy-substance (D2 Necromancer Bone Spirit / Bone Spear; PoE Bone Offering); (b) palette-shift VFX coverage may be acceptable with white/grey particle re-tint of earth VFX. Tier-C borderline. Status: eligible-with-watch-flag. |
| `thorn` | earth | 11 | **CULL → eligible** | Plant-anatomical; semi-biological. Tier-C palette-shift over earth VFX possible (green/brown tint on stone). flex_slots=[] (single-slot fit; no cross-element ambiguity). Keep selectable at eligible. |
| `husk` | earth | 8 | **CULL → quarantine** | Biological-residue (per same pattern); already low d1=8; clean cull to quarantine. |
| `shell` | earth | 8 | **CULL → quarantine** | Biological. flex_slots=['water'] — cross-element ambiguity compounds the leak. Clean cull. |
| `blood` | water | 11 | **CULL → eligible** | Alternative-liquid-specific (red, not blue/cyan). Tier-C palette-shift POSSIBLE but creates strong cultural register (gore/violence) that may not fit all seasons. Eligible-with-watch-flag. Note: gandalf's prior `gandalf-design-lineage.md` work has notes on blood-substrate genre-register — defer to design-direction follow-on if eligible-tier still surfaces it too frequently. |
| `mercury` | water | 11 | **CULL → eligible** | Alternative-liquid-specific (silver, metallic). Tier-C palette-shift POSSIBLE (silver-tinted water VFX). Eligible. |
| `pearl` | water | 8 | **CULL → quarantine** | Already low d1=8; flex_slots=['earth'] cross-element ambiguity; biological-organic origin; non-liquid form (solid object, not water-substance). Tier-D. Clean cull. |
| `whisper` | wind | (likely 7-8) | **CULL → quarantine** | Auditory (per drift-audit § Drift-14). Should have been quarantined at scoring time. Verify d1 + status at rocket execution time. |
| `hum` | wind | (likely 7-8) | **CULL → quarantine** | Auditory. Same pattern. |
| `sigh` | wind | (likely 7-8) | **CULL → quarantine** | Auditory. Same pattern. |
| `whistle` | wind | (likely 7-8) | **CULL → quarantine** | Auditory. Same pattern. |
| `breath` | wind | (likely 7-8) | **CULL → quarantine** | Auditory + intimate (per D1 Q3 "not domestic, food, or intimate"). Same pattern. |

**Note for rocket execution:** Entries in § 1.4 marked `(likely 7-8)` need verification against current pool.json status. If any are already at `quarantine` (which the pool composition tally suggests 7 entries scattered across slots may be), no action needed — they're correctly excluded. The CULL action only applies if currently at `allow-list` OR `eligible`. Rocket should treat § 1.4 as a *target-state declaration* rather than as a *required state-change list* — entries already in the target state require no action.

### § 1.5 Cull execution summary

| Category | Count | Net allow-list impact |
|---|---|---|
| Critical allow-list → quarantine (§ 1.2) | 7 | -7 allow-list |
| Wind-storm cluster: 1 keep + 7 cull (§ 1.3) | 8 | -7 allow-list |
| Other allow-list demotions (§ 1.4) | ~12 | -12 allow-list (assuming all currently allow-list) |
| **Total cull actions** | **~27** | **~-26 allow-list** |

**Net pool composition shift (target):** 81 allow-list / 40 eligible / 35 quarantine → **~55 allow-list / ~46 eligible / ~55 quarantine.**

Some of the eligible→quarantine reclassifications inside the § 1.4 set will push numbers further; final breakdown TBD on rocket execution.

---

## § 2 — Selector hard-floor amendment spec

### § 2.1 Three tracks surveyed

Per legolas Track A top-3 recommendations:

| Track | Mechanism | Implementation cost | Drift-14 leverage | Architecture cleanliness |
|---|---|---|---|---|
| **Track 1: `vfx_catalogue_mapping_clean` boolean gate** | Required-true for allow-list status; offline-scored once per entry against a cached catalogue-coverage manifest | LOW | HIGH (closes the structural enforcement gap that Drift-14 named) | HIGH (matches existing d1_status three-tier mechanism; minimal new code) |
| **Track 2: `canonical_pair_leak` D1 property** | New scoring dimension (0-1 boolean or 0-2 graduated) on the 5-property D1 rubric; flag entries whose name structurally implies canonical-four pair binding | LOW-MED | MED (surfaces the leak pattern for audit but doesn't itself enforce a hard floor unless combined with Track 1 or a separate gate) | MED (extends rubric Q-set; requires the LLM-scored Phase C path to update too) |
| **Track 3: cluster effective-selection-probability floor** | Define thematic clusters (tag-based? embedding? hand-curated manifest?); cap aggregate selection-probability across cluster (e.g. max 20%) | HIGH | LOW post-cull (Section 1 § 1.3 solves wind-storm structurally; floor mechanism only fires on future re-emergence) | LOW (new infrastructure: cluster manifest, selection-tracking instrumentation, probability arithmetic over weighted sampling) |

### § 2.2 Decision: ship MINIMUM-VIABLE cut (Tracks 1 + 2; defer Track 3)

**Minimum-viable rationale:**

- Track 1 alone closes the structural enforcement gap Drift-14 named — "VFX-catalogue-mapping coherence was implicit-deferred from the D1 rubric." Adding a boolean gate makes the deferred dimension explicit and structurally enforced.
- Track 2 is cheap to ship alongside Track 1 and gives gandalf an audit dimension to query future pool additions against ("does this new entry structurally suggest its canonical-pair label?"). Without Track 2, the wind-storm pattern can re-emerge from a new vendor acquisition or LLM proposal without detection.
- Track 3 is over-engineered for the current problem. The wind-storm cluster surfaced because of selection-pressure concentration AFTER weighting; the cull + cluster-collapse in § 1.3 solves it structurally (1/7 weighted vs 8/14 weighted = 8.7× reduction). Building a generic cluster-floor mechanism to solve a single empirical instance is the wrong abstraction. Re-evaluate IF post-cull empirical regen surfaces a new cluster-pressure pattern (e.g., earth slot ends up dominated by mineral-precious sub-cluster after the biological-organic cull).

**Hybrid cut (recommended explicit form):**

- **`vfx_catalogue_mapping_clean: bool`** — new field on `PoolElement` schema. True iff entry's `vfx_mapping_tier` ∈ {A, B} (per the legolas Track A tier definitions: A=direct VFX coverage, B=palette-shift coverage). False for Tiers C, D, E.
- **Gate semantic:** `d1_status == "allow-list"` REQUIRES `vfx_catalogue_mapping_clean == True`. Entries with `vfx_catalogue_mapping_clean == False` can be at most `eligible` (or `quarantine` if d1_total < 5).
- **`canonical_pair_leak: bool`** — new field on `PoolElement` schema. True iff entry's name lexically/semantically implies one of the canonical-four labels (hand-curated leak-set + future LLM-scored rubric Q6 — see § 2.3).
- **Gate semantic:** `canonical_pair_leak == True` does NOT automatically demote (an entry can be canonically-pair-leak-y AND still allow-list-worthy; e.g. `cinder` clearly suggests fire and that's fine). But it MUST be flagged in pool composition audits for cluster-pressure detection. Audit-only gate, not a hard demotion gate.

### § 2.3 Implementation spec for rocket (handoff to dispatch § 2)

**Schema changes (`element/schema.py:PoolElement`):**

```python
class PoolElement(BaseModel, frozen=True):
    # ... existing fields ...
    # NEW: VFX-catalogue-mapping coherence dimension (Drift-14 closure)
    vfx_mapping_tier: str = "unscored"           # "A" | "B" | "C" | "D" | "E" | "unscored"
    vfx_catalogue_mapping_clean: bool = False    # True iff tier in {A, B}; gates allow-list eligibility
    # NEW: canonical-pair-leak audit dimension
    canonical_pair_leak: bool = False            # True iff entry name structurally implies canonical-four pair binding
```

**Selector gate changes (`element/selector.py`):**

- At pool-load time (in `load_element_pool` or a new validator), assert: for every entry where `d1_status == "allow-list"`, `vfx_catalogue_mapping_clean` MUST be True. If False, log a warning + demote to `eligible` at load-time (defensive auto-demote — defends against pool.json hand-edits that violate the invariant).
- At Phase-C scoring time (`_score_novel_word`), add two new questions to `_build_d1_rubric_questions`:
  - Q6: "Does this word map to a 2D-VFX-catalogue-renderable visual register for the {primary_slot} slot, using either direct coverage (Tier A) or simple palette-shift (Tier B)? Answer N if the word requires custom VFX commission or has no visual register at all."
  - Q7: "Does this word structurally imply the canonical-four label binding (e.g., 'gale' implies 'wind', 'cinder' implies 'fire')? Answer Y/N; this is an audit flag, not a demotion criterion."
- Status threshold update: `d1_status = "allow-list"` only if `total >= 8 AND vfx_catalogue_mapping_clean == True`. Otherwise `d1_status = "eligible"` (or `quarantine` if total < 5).

**Catalogue-coverage manifest:**

The `vfx_catalogue_mapping_clean` field is populated by an offline scoring pass that consumes a catalogue-coverage manifest. The manifest is a JSON document derived from `cross-vendor-substrate-inventory-2026-05-16.jsonl` + legolas Track A per-entry annotations. Suggested location: `data/seasonal_elements/vfx_coverage_manifest.json` (NEW file; rocket-owned in source-of-truth, gandalf-authored content for the catalogue-coverage decisions).

**Schema of the catalogue-coverage manifest:**

```json
{
  "version": "1.0",
  "generated_date": "2026-05-17",
  "entries": [
    {"id": "ember", "vfx_mapping_tier": "A", "vfx_catalogue_mapping_clean": true, "canonical_pair_leak": true, "rationale": "direct Pimen fire-spell coverage; lexically implies fire"},
    ...
  ]
}
```

The manifest is consumed at pool-load time (or at re-scoring time via a CLI command). Pool entries are joined to manifest entries by `id`. On manifest miss, entry defaults to `vfx_mapping_tier="unscored"` + `vfx_catalogue_mapping_clean=False` (conservative; pushes unscored entries below allow-list eligibility — this is intentional).

**Re-scoring run validation:**

After rocket lands the schema change + populates the manifest + executes the auto-demote logic, do an end-to-end run that:
1. Loads pool.json + manifest
2. Validates every allow-list entry has `vfx_catalogue_mapping_clean = True`
3. Surfaces any entries that the auto-demote logic moved
4. Compares the resulting status distribution to § 1 target

If the auto-demote logic surfaces entries NOT in § 1's cull list, gandalf needs to be notified — could indicate (a) the legolas Track A annotations are stricter than gandalf's first-principles call, OR (b) gandalf missed an entry. Either way, surface for review.

### § 2.4 What is explicitly NOT in this amendment

- **Track 3 (cluster floor):** deferred. Re-evaluate post-cull empirical regen.
- **Generic cluster manifest infrastructure:** deferred.
- **Embedding-based leak detection:** deferred — hand-curated `canonical_pair_leak` flag is sufficient for current scope; embedding-based detection is over-engineered.
- **D1 rubric weight rebalancing:** out of scope. Existing 5-property weighting holds; adding Q6 + Q7 increases max score from 10 to 14 (or with Q7 audit-only, max becomes 12). Threshold semantics adjust per § 2.3.
- **Dynamic catalogue-coverage recompute:** the manifest is static at scoring time. If a new vendor lands (e.g., CraftPix wood-nature acquisition; see § 3), the manifest is regenerated and pool re-scored on the next pool-edit cycle. No live catalogue lookup at selection time.

---

## § 3 — Vendor-acquisition prioritization

### § 3.1 Decisions on the legolas top-3 picks

| Vendor pick | Decision | Rationale | Sequencing |
|---|---|---|---|
| **CraftPix premium (wood-nature substrate)** | **ACQUIRE — surface to Matt for license/cost approval** | The post-cull earth slot loses 7+ biological-organic entries (chitin, scale, horn, tooth, claw, marrow + bone-borderline). Net earth allow-list shrinks from 33 → ~25. Wood-nature substrate is the cleanest non-mineral earth flex that has clean VFX coverage (per `cross-vendor-substrate-inventory-2026-05-16.jsonl` "CraftPix Bamboo Wall (plant/nature substrate) is a variation worth noting"). Acquiring unblocks adding `root`, `bark`, `leaf`, `petal`, `vine`, `moss`, `lichen`, `wood` (currently scattered across eligible/quarantine; many would move to allow-list with clean wood-nature VFX coverage backing them). Estimated +5-8 allow-list entries to earth slot post-acquisition. | **POST-cull** (acquisition fills gaps surfaced by post-cull D1 re-scoring). |
| **Fellor Crystal pack (gem cluster)** | **ACQUIRE — surface to Matt** | Reinforces the crystal/gem/precious-metal cluster that the cull KEEPS at allow-list (gem, crystal, geode, quartz, amber, obsidian, ore, iron, gold, silver, copper, bronze, lead). These are 13 of the post-cull earth allow-list — the dominant sub-cluster. Crystal-pack VFX coverage strengthens the in-pool entries' renderability and supports future per-season visual variation. Lower-priority than CraftPix but higher-confidence (existing pool entries directly benefit; not speculative). | **PARALLEL with cull** (acquisition supports existing kept-entries; no dependency on post-cull pool state). |
| **Frostwindz Deathbringer (bone substrate)** | **DEFER (declined for current cycle; revisit post-VS2b empirical regen)** | The cull intentionally moves AWAY from biological-organic substrate. Acquiring bone-substrate VFX coverage NOW would create downstream pressure to re-introduce bone/marrow/skull/skeleton-type entries to allow-list, reversing the canonical-bias-break the cull is making. Bone is a load-bearing fantasy substance (D2 Necromancer-class identity; PoE Bone Offering; Diablo skeleton lineage) — but the right time to add it is AFTER a post-cull empirical regen surfaces a clear gap that bone substrate fills, with explicit design framing for "bone as a deliberate sub-register inside a Necromancer-themed season" (not as a default earth-slot entry). | **AFTER VS2b empirical regen + design-direction review.** Re-surface at next gandalf design-direction pass. |

### § 3.2 Acquisition sequencing relative to pool-cull execution

- **Fellor Crystal pack:** parallel — no dependency on cull state; supports existing kept entries.
- **CraftPix premium (wood-nature):** post-cull — fills gaps surfaced after the cull validates and earth-slot composition is empirically observed in post-cull regen.
- **Frostwindz Deathbringer (bone):** deferred — no acquisition in current cycle.

**Matt-decision items surfaced to knight-rider for routing:**

1. CraftPix premium license/cost approval (priority: high — gates earth-slot post-cull rebuild)
2. Fellor Crystal pack license/cost approval (priority: med — supports existing kept entries; not blocking)

### § 3.3 What is NOT being acquired (explicit declines)

- **Frostwindz Deathbringer:** declined for current cycle (rationale above)
- Any vendor sweep for the auditory cluster (`whisper`, `hum`, etc.) — these are Tier-E (non-visual); no VFX vendor can render auditory substances; cull stays
- Any vendor sweep for the conceptual cluster (`throne`, etc.) — Tier-D bespoke-commission territory; not appropriate to acquire vendor packs for one-off conceptual substances

---

## § 4 — PATH-D1 sequencing call

### § 4.1 Three sequencing options surveyed

Per legolas novel finding PATH-D1: "D1 rubric offline scoring path is upstream of all 48 runtime sites in cipher-migration paths-audit — pool composition fix must precede/co-ship with Stage 3 for full Drift-14 closure."

| Option | Description | Pros | Cons |
|---|---|---|---|
| **A — Pool-cull BEFORE Stage 3** | Land pool-cull + rubric amendment now; Stage 3 ships on the post-cull pool state | Clean state before Stage 3 work; Stage 3 cipher migration operates on a canonically-bias-clean pool | Sequencing rigidity; Stage 3 is on HOLD-on-prior queue (per its dispatch); pool-cull would land in the gap, creating one isolated regen cycle BEFORE Stage 3 ships its own |
| **B — Pool-cull WITH Stage 3 (combined cascade)** | Add pool-cull + rubric amendment as preconditions to Stage 3 launch checklist; single coordinated cascade; combined regen consumes both | Single regen cycle; minimal scheduling overhead; both changes are upstream of the same downstream consumer (export packet + LLM prompts) | Adds one more precondition to Stage 3 launch (currently 3 dependencies: Stage 2 + V2.4 telemetry + V2 CLI/regen); slight launch-time delay |
| **C — Pool-cull AFTER Stage 3** | Stage 3 ships first on existing pool; pool-cull is a follow-on hygiene pass | No additional Stage 3 dependency; clean separation of concerns | **Defeats Drift-14 closure rationale** — Stage 3 cipher migration would surface per-season vocabulary end-to-end on a still-canonically-biased pool; player-visible exposure of canonical-bias names ships before the cull. Per Matt's quote: *"I really don't want to ship any more canonically biased seasonal themes."* — Option C ships exactly that. |

### § 4.2 Decision: Option B — pool-cull WITH Stage 3 (combined cascade)

**Rationale:**

- Stage 3 is currently PENDING — HOLD-on-prior (per dispatch line 6); it's not racing toward launch this week. Adding one more precondition costs minimal delta.
- The combined cascade is the right structural shape: pool composition state + cipher migration state are *both* required for VS2a to ship canonically-bias-clean. Shipping either alone gives partial closure.
- Combined post-cascade gamora regen (currently gated on Track B return per the dispatch's broader cascade) consumes both pool-cull state AND Stage 3 cipher migration state in one cycle. This is the cleanest single-regen architecture.
- Matt's quote ("I really don't want to ship any more canonically biased seasonal themes") names a state — *seasonal themes shipped without canonical-bias closure*. Option B is the only sequencing that ships the next set of seasonal themes WITH closure in place.

### § 4.3 Dependency-graph implications

**Combined post-cascade Gamora regen (currently gated on Track B return):**

- Track B (this synthesis) — RETURNS today
- Rocket dispatch (authored as side-output) — fires next per knight-rider sequencing
- Stage 3 unblock sequence — Stage 2 → V2.4 telemetry → V2 CLI/regen → **+ pool-cull/rubric amendment** → Stage 3
- Combined regen — runs ONCE after Stage 3 ships, consuming pool-cull state + Stage 3 cipher migration state + end-game-anchored MS values + form-bias Stage 1+2 fields + Stage B export-DTO fix + B6 main + chierit characters

**Update to Stage 3 launch checklist** (knight-rider authorship; gandalf surfaces as note):

> Add to Stage 3 dispatch dependencies: "(4) pool-cull + rubric amendment landed at rocket (per `drift-14-pool-cull-decisions-2026-05-17.md`)."

### § 4.4 Critical-path observation

The legolas PATH-D1 finding is correct AND structurally consequential: the D1 rubric is upstream of every runtime emission site that surfaces vocabulary through the cipher migration. Without the pool-cull, Stage 3 ships an architecturally-clean cipher migration on top of canonically-biased pool composition — visible to the player. The closure is incomplete.

**This generalizes:** any rubric upstream of a cipher migration must be coherent with the cipher migration's intent BEFORE the migration ships, or the cipher migration becomes a high-resolution leak path for the upstream rubric's biases. Future cipher migrations should audit upstream rubrics for the same pattern. (Forward discipline candidate; surface to next jack-ryan engineering-disciplines pass — see § 5.)

---

## § 5 — Cross-seam side-routing

### § 5.1 Star-lord prompt-template audit

**Surface to knight-rider for routing:** the D1 Phase-C LLM scoring path at `element/selector.py:_score_novel_word` constructs a prompt via `_build_d1_rubric_questions(word)` and sends 5 yes/no questions to the LLM. The current questions cover the existing D1 rubric properties. The § 2.3 rubric extension adds Q6 (vfx-coverage check) and Q7 (canonical-pair-leak audit) — these are NEW LLM prompt content.

**Audit ask for star-lord:** verify that the `_build_d1_rubric_questions` function update (rocket-owned) doesn't conflict with other LLM prompt templates that consume D1 fields. Specifically:
- Does the per-season element selection prompt (`element/selector.py:_SYSTEM_PROMPT` line 43-47) need an update to reference the new VFX-coverage gate? (Likely no — selection consumes only post-scored fields, not the rubric itself. But verify.)
- Is the `llm/naming.py` `_elements_summary_line()` function (per cipher-migration paths-audit SG-02) affected? (Likely no — naming consumes the selected element name, not the rubric. But verify.)
- Does Stage 3 cipher migration's planned rubric-prompt changes (per star-lord Stage 3 dispatch) interact with the new Q6/Q7? (Verify — Stage 3 changes the grouping-layer abstraction; Q6/Q7 are at the pool-scoring layer; they should be orthogonal but confirm.)

**Why star-lord and not rocket:** rocket owns the schema + selector code; star-lord owns the LLM prompt-template surface AND the cipher migration that is downstream of this change. Coordination is between rocket (executing) and star-lord (downstream prompt-consumer); knight-rider routes.

### § 5.2 Forward discipline candidate

**Candidate D17 (provisional naming):** "Rubric coherence with downstream cipher/translation layers must be audited before the cipher ships, or the cipher becomes a high-resolution leak path for the upstream rubric's biases."

Surface to next jack-ryan engineering-disciplines pass alongside D14, D15, D16, R11(b), Pattern P7 cluster, Drift-11 sibling-cluster-sweep lesson. Disciplinary cluster is growing (now 7+ candidates) — strong empirical basis for a coordinated jack-ryan pass when capacity allows.

---

## § 6 — Hand-off summary for knight-rider

**Single paragraph:**

Drift-14 Track B synthesis complete. Pool-cull = 27 actions: 7 critical allow-list to quarantine (chitin/scale/horn/tooth/claw/throne/marrow — all earth-slot biological-organic + conceptual), 8-entry wind-storm cluster collapsed to 1 representative (`gale` keep; 7 others demoted to eligible or quarantine), 12 more allow-list demotions across biological-organic earth + alternative-liquid water + auditory wind. Net allow-list contraction ~81 → ~55. Selector hard-floor amendment ships MINIMUM-VIABLE cut: `vfx_catalogue_mapping_clean` boolean gate (Track 1) + `canonical_pair_leak` audit flag (Track 2); cluster-floor mechanism (Track 3) DEFERRED — cull-plus-collapse solves the wind-storm pattern structurally without needing a generic floor. Vendor acquisitions: ACQUIRE CraftPix premium (wood-nature, post-cull) + Fellor Crystal pack (parallel); DEFER Frostwindz Deathbringer (bone — would re-introduce the biological-organic drift the cull closes). PATH-D1 sequencing: pool-cull ships WITH Stage 3 in combined cascade (add as Stage 3 launch precondition #4); not before, not after. Rocket dispatch authored at `agentic_orchestration/dispatches/2026-05-17-rocket-drift-14-pool-cull-and-selector-hardfloor-amendment.md` with R11(b) MIGRATION.md cross-reference clause for the downstream cipher-migration cross-seam impact. Side-routing: star-lord prompt-template audit on the rubric Q-set extension (verify no conflict with `element/selector.py:_SYSTEM_PROMPT` or `llm/naming.py:_elements_summary_line` or Stage 3 cipher migration's planned rubric changes). Forward discipline candidate D17 surfaced ("rubric coherence with downstream cipher layers must be audited before cipher ships"). Matt-decision items for routing: CraftPix premium acquisition (high — gates earth-slot post-cull rebuild); Fellor Crystal pack acquisition (med); pool-cull + rubric amendment dispatch approval (firing).

---

## Appendix A — Data-source attribution explicit

| Claim or decision | Source |
|---|---|
| 27 cull candidate count | Knight-rider summary of legolas inline return |
| 7 critical allow-list entries (chitin/scale/horn/tooth/claw/throne/marrow) | Knight-rider summary + gandalf direct verification via `pool.json` inspection (all 7 confirmed at d1_total 9-11, allow-list) |
| 8-entry wind-storm cluster names | Knight-rider summary + gandalf direct verification via `pool.json` inspection (all 8 confirmed at allow-list, d1_total 9-11) |
| Per-entry rationale for the 7 critical (§ 1.2) | Gandalf first-principles + pool tags + D1 rubric Q-set + cipher migration architecture |
| Cluster-decision shape (Option B keep-1-cull-7) | Gandalf first-principles + selection-pressure math + style-register coherence |
| Choice of `gale` as representative | Gandalf first-principles based on flex_slots / tags / genre-register reading |
| Remaining 12 cull candidates (§ 1.4) | Gandalf derivation from leak patterns implied by aggregate data; FLAGGED for rocket validation against legolas per-entry annotations during execution |
| Three selector hard-floor recommendation slots | Knight-rider summary of legolas inline return |
| Minimum-viable cut decision (Tracks 1+2; defer Track 3) | Gandalf first-principles + implementation cost vs leverage analysis |
| Vendor pick names (CraftPix / Fellor / Frostwindz) | Knight-rider summary of legolas inline return |
| Acquisition decisions (ACQUIRE/DEFER) | Gandalf first-principles + post-cull pool composition analysis + design-direction read |
| PATH-D1 finding | Knight-rider summary of legolas inline return |
| Sequencing decision (Option B WITH Stage 3) | Gandalf first-principles + Matt-quote interpretation + Stage 3 dispatch status read |

**Where legolas's per-entry annotations would refine gandalf's first-principles judgment:**

- § 1.4 entries marked `(likely 7-8)` for d1_total — rocket should validate against actual pool.json or legolas annotations during execution.
- Specific `vfx_mapping_tier` assignments per entry (gandalf has applied tier inferences based on tags + cross-vendor inventory; legolas's per-entry tier assignment may differ for borderline entries). Rocket should treat gandalf's tier-inference as guidance and adjudicate against legolas's annotations if available.
- The 27-candidate total — gandalf's accounting (7 critical + 8 wind-storm + ~12 other = ~27) may not exactly match legolas's. The shape is right; the exact set may have one or two delta entries either direction. Rocket should reconcile during execution.

---

## Appendix B — Cross-references

- `canonical/story/drift-audit.md` § Drift-14 — the surfacing
- `agentic_orchestration/dispatches/2026-05-16-gandalf-drift-14-track-b-pool-cull-and-selector-hardfloor-synthesis.md` — this dispatch
- `agentic_orchestration/dispatches/2026-05-17-rocket-drift-14-pool-cull-and-selector-hardfloor-amendment.md` — side-output rocket dispatch
- `agentic_orchestration/gandalf/requests/2026-05-17-pool-vfx-catalogue-mapping-audit.md` — original two-track commission framing
- `agentic_orchestration/research/cipher-migration-paths-audit-2026-05-16.md` — the 48 runtime sites; PATH-D1 is the novel upstream path
- `agentic_orchestration/dispatches/2026-05-16-star-lord-form-bias-stage-3-cipher-migration.md` — Stage 3 dispatch (PENDING HOLD-on-prior); add pool-cull as launch precondition #4
- `reincarnated-engine/data/seasonal_elements/pool.json` — current pool source-of-truth (156 entries)
- `reincarnated-engine/src/reincarnated/element/selector.py` — D1 selector + Phase-C scoring (the code rocket modifies)
- `reincarnated-engine/src/reincarnated/element/schema.py:PoolElement` — schema extension target
- `agentic_orchestration/research/catalogue/cross-vendor-substrate-inventory-2026-05-16.jsonl` — VFX vendor inventory backing the manifest
- `canonical/story/geometry-vfx-coverage-assessment.md` — prior VFX coverage assessment
- `canonical/37-form-bias-diagnosis-and-recovery.md` § 6 — cipher migration architecture
- `canonical/story/form-bias-cadence-strategy.md` § 7.2 — cipher migration strategy
- `reincarnated-engine/design/working-agreement/engineering-disciplines.md` R11(b) — cross-seam round-trip discipline (motivates the MIGRATION.md clause in the rocket dispatch)

---

*Authored 2026-05-17 by gandalf. Drift-14 Track B synthesis. Pending: Matt approval to fire rocket dispatch; knight-rider routing of vendor-acquisition Matt-decisions; star-lord prompt-template audit side-routing.*
