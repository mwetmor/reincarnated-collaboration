# D1 Rubric × VFX-Catalogue-Mapping Extension — Drift-14 Framework

> **STATUS:** HISTORICAL-INFORMATIVE (pre-Epoch-4; consult for lineage only — not current truth) — see `canonical/00-ground-state.md` for current truth

**Status:** **Canonical.** Authored 2026-05-19 by gandalf under autonomous-operation authority (VS2a hive-mind protocol § 4.0). F3 deliverable per dispatch `agentic_orchestration/dispatches/2026-05-19-gandalf-vs2a-drift14-15-framework.md`. Gates F5 (legolas Mode A Drift-14 audit + gandalf re-scoring pass).

**Supersedes (forward-extends):**
- `canonical/story/drift-14-pool-cull-decisions-2026-05-17.md` — § 1 cull list + § 2 selector hard-floor amendment spec (consumed; not replaced). This doc is the framework-level formalization that the 2026-05-17 cull decisions were authored against implicitly.
- `reincarnated-engine/design/notes/drift-14-d1-substrate-native-rescore-math-2026-05-17.md` — rocket math note (math remains canonical; this doc names the design-side principles around it).

**Companion docs:**
- `canonical/story/style-register.md` — score-don't-filter principle (this framework is its operational instantiation for the seasonal-vocabulary surface)
- `canonical/37-form-bias-diagnosis-and-recovery.md` § 6 — cipher migration architecture (L1 substrate → VFX; L3 vocabulary → player-visible labels)
- `canonical/story/form-bias-cadence-strategy.md` § 7.2 — Stage 3 cipher migration ship gate
- `canonical/story/drift-audit.md` § Drift-14 — pattern-archived instance
- `canonical/story/substrate-expansion-decision-2026-05-17.md` — Branch-A confirmation; this framework propagates substrate_native + vocab-freeze handling forward

---

## § 0 — TL;DR

The D1 rubric (5 questions × 2 pts + genre-precedent bonus = ~11 max) scored seasonal-element pool entries on *conceptual visualizability*, but did NOT score whether each entry maps cleanly to the operational 2D VFX catalogue. This framework adds **Q6 `vfx_catalogue_mapping_clean`** as a sixth rubric property (Tier A–E methodology) and **Q7 `canonical_pair_leak`** as an audit-only boolean. Pool-status thresholds redefine as an AND-conjunction: allow-list requires both `d1_total ≥ 8` AND `vfx_catalogue_mapping_clean == True`. Selector-side hard-floor enforces the gate at pool-load with auto-demote-with-WARN. Drift-14 closure mechanism: legolas Mode A audits the 156-entry pool against the catalogue at concept level (Tier A/B/C/D/E annotations); gandalf re-scores the residual unscored entries; rocket's auto-demote logic already lands at the loader. Final result: a per-season vocabulary surface free of canonical-bias residue and free of VFX-incoherent entries that would surface as "throne-strike with stone-particle VFX" at Stage 3 cipher migration ship.

**This framework is the formalization of doctrine.** The 2026-05-17 implementation cascade (rocket dispatch; gandalf cull-decisions doc; manifest at `data/seasonal_elements/vfx_coverage_manifest.json`; schema + selector wiring) was authored under the doctrine. This doc names the doctrine canonically so future pool additions (Phase-1 P1 substrate-expansion entries; future season-themed vocabulary growth) inherit it without re-derivation.

---

## § 1 — Why this rubric extension exists

### § 1.1 The structural gap D1 left open

The D1 rubric was authored at Stage A1 (commit `98f1e3f`, 2026-05-12), before the VFX catalogue (Pimen, CreativeKind) had been crawled. Its 5 properties scored entries against:

- Q1 — Physical substance / evocative cosmological force (0 / 2)
- Q2 — Player can picture {word}-bolt / {word}-armor (0 / 2)
- Q3 — Heroic/gritty fantasy vocabulary (0 / 2)
- Q4 — {word}-Knight / {word}-Mage compounds (syllable gate; 0 / 2)
- Q5 — Appropriate in action-combat context (0 / 2)
- Genre-precedent bonus (+1 if appears in shipped ARPG canon)

These are all *conceptual* properties — they answer "can the player picture / accept this word?" without answering "does our renderer produce a coherent visual when it picks this word?"

The two questions are correlated but not identical. `throne` scores d1_total=11 (top score) on every conceptual axis — players can picture a throne; it's heroic-gritty; it has genre precedent; "Throne Knight" is a clean compound. But `throne` is **a conceptual symbol, not a substance**, and the canonical-earth-slot VFX (stone particles, mineral debris) does not render anything that reads as "throne." The pool-introduction-time scoring missed this because the scoring framework didn't have a VFX-mapping question.

### § 1.2 The cipher-migration architecture that makes the gap load-bearing

Per `canonical/37-form-bias-diagnosis-and-recovery.md` § 6 + `canonical/story/form-bias-cadence-strategy.md` § 7.2:

- **L1 substrate** (canonical-four / six post-Phase-1 P1) drives **VFX**
- **L3 per-season vocabulary** drives **player-visible labels**

Pre-Stage-3 cipher migration: the LLM still sees canonical-four labels. The pool-vocabulary layer is camouflaged — `throne` may be in the pool but the demo doesn't surface it player-visibly at VS2a yet. At Stage 3 (the ship-gate this framework closes ahead of), per-season vocabulary becomes player-visible end-to-end. At that point, a season selecting `throne` produces "throne-strike with stone-particle VFX" as a directly-observable player surface.

### § 1.3 Why this is Pattern P6 and why now

This is a Pattern P6 instance (load-bearing dimension deferred to a later milestone that becomes upstream of a near-term ship). It is the third sibling P6 instance after Drift-11A (movement-speed-baseline) and Drift-11B (geometry × element VFX coverage), and its closure pattern is identical: explicit rubric extension + bounded audit pass + closes before the ship the deferred dimension gates.

Matt verdict 2026-05-17 (verbatim): *"I really don't want to ship any more canonically biased seasonal themes."* The pushback is sharper than the technical-camouflage framing — D1, as scored, has a structural canonical-four bias in its allow-list composition. Closure folds into the VS2a regen cycle already scheduled.

---

## § 2 — Rubric extension methodology (Q6 + Q7)

### § 2.1 Q6 — `vfx_catalogue_mapping_clean` (composite, scored)

**Property statement:** *"Does this substance / phenomenon map cleanly to the operational 2D VFX catalogue at the canonical slot level?"*

**Operational scoring rule:** For each pool entry, the legolas Mode A audit assigns a **Tier (A–E)** annotation against the current catalogue (Pimen GREEN-list 11/13 elements + CreativeKind palette-shift coverage at minimum; Tier-2 vendor packs as in-scope as the catalogue grows). The Tier maps to a boolean `vfx_catalogue_mapping_clean` field consumed by the auto-demote logic at pool-load.

| Tier | Definition | `vfx_catalogue_mapping_clean` | Allow-list eligibility |
|---|---|---|---|
| **A — Direct** | Maps to canonical-slot VFX with no modification. Vendor catalogue ships this substance-concept as-is. Example: `ember`, `cinder`, `spark`, `granite`, `stone`, `sand`, `clay`. | **True** | Eligible (subject to `d1_total ≥ 8`) |
| **B — Palette-shift** | Maps to canonical-slot VFX with palette change only. Example: `frost`, `ice` (water + cyan/blue → ice), `pearl` (water + white-reflective), `coal` (fire + darkened), `soot` (fire + black-particle). | **True** | Eligible (subject to `d1_total ≥ 8`) |
| **C — Composite** | Maps with palette + minor compositing (e.g., adding a sparkle overlay; texture-replacement). Example: `obsidian` (earth + dark + glossy), `amber` (earth + warm + translucent). Renders coherent but requires per-asset compositing work. | **False** (conservative) | Demoted to `eligible` |
| **D — Custom-required** | No clean catalogue mapping; bespoke VFX commission would be needed to render the substance-concept coherently. Examples: `throne` (conceptual; no substance-shape), `marrow` (biological-organic, distinct from mineral-earth register), `chitin`. | **False** | Demoted to `eligible` or `quarantine` per § 2.3 |
| **E — Non-visual** | Auditory / textural / conceptual entries that cannot render as visual VFX at all. Examples: `whisper`, `hum`, `sigh`, `gauze`, `silk`. | **False** | Quarantine |

**Numerical scoring (within the existing 5-question rubric format):**

- Tier A → Q6 = 2 pts; `vfx_catalogue_mapping_clean = True`
- Tier B → Q6 = 2 pts; `vfx_catalogue_mapping_clean = True`
- Tier C → Q6 = 1 pt;  `vfx_catalogue_mapping_clean = False`  *(conservative: half-credit on the conceptual axis; demote on the hard gate)*
- Tier D → Q6 = 0 pts; `vfx_catalogue_mapping_clean = False`
- Tier E → Q6 = -2 pts (demotion penalty); `vfx_catalogue_mapping_clean = False`

**New rubric max:** `d1_score` max grows from 10 → 12 (6 questions × 2 pts); `d1_total` max grows from 11 → 13 (adding genre-precedent bonus unchanged). Per rocket math note § 2.2 (which is the binding implementation reference).

### § 2.2 Q7 — `canonical_pair_leak` (audit-only, no composite effect)

**Property statement:** *"Does this entry, when surfaced at its primary_slot, structurally bias the season-theme toward a canonical-four reading rather than expressing per-season variety?"*

This is a **boolean flag** captured at scoring time; it does NOT contribute to `d1_score` or `d1_total`. It exists for two purposes:

1. **Cluster audit** — surfaces the wind-storm cluster pattern (8 wind entries collapsing thematically to "weather-storm" sub-register, producing 57% effective selection-pressure at the canonical-four ratio). Future audits can query `WHERE canonical_pair_leak = True GROUP BY primary_slot` to detect new clusters at addition time.
2. **Forward selector instrumentation** — if a future selector pass needs cluster-collapse logic (Track 3 of § 2 cull-decisions, currently DEFERRED post-VS2a), this flag is the natural input.

Q7 is annotated by legolas Mode A alongside Tier A–E. Gandalf re-scoring pass adjudicates borderline cases.

### § 2.3 Sub-category flags (legolas annotates; gandalf adjudicates)

For borderline cases that don't fit cleanly into Tier A/B/C/D/E, the audit attaches sub-category flags. These are not scoring inputs — they are routing inputs for the gandalf re-scoring pass:

- `biological-organic` — bone / marrow / chitin / claw / horn / scale / thorn / tooth / husk / shell. Earth-primary by D1 scoring but visually distinct from mineral. Default Tier-D.
- `liquid-specific` — blood / mercury / pearl / honey / nectar. Water-primary by D1 but distinct from canonical-water visual register. Default Tier-C (palette-shift+composite achievable) or Tier-D per visual-distinctness severity.
- `conceptual-abstract` — throne / threshold / hearth. No substance-shape to render. Tier-D.
- `auditory` — whisper / hum / sigh / thrum / breath / exhalation / whistle / howl. Tier-E.
- `textural` — gauze / silk / gossamer / feather. Tier-E (renders as character-trim, not as combat-substance).

---

## § 3 — Pool-status threshold redefinition

### § 3.1 Pre-Drift-14 thresholds (D1 only)

```
allow-list:  d1_total >= 8
eligible:    d1_total >= 5
quarantine:  d1_total < 5
```

Single-axis: a conceptual score alone determined allow-list eligibility. `throne` at d1_total=11 lands on allow-list under this rule.

### § 3.2 Post-Drift-14 thresholds (D1 ∧ VFX-coherent)

```
allow-list:  d1_total >= 8  AND  vfx_catalogue_mapping_clean == True
eligible:    d1_total >= 5   (vfx_clean irrelevant — eligible tier is not pressure-weighted)
quarantine:  d1_total < 5
```

**Critical property:** the threshold value (8) is unchanged. The new gate is the AND-conjunction with `vfx_catalogue_mapping_clean`. A word scoring 11/13 with `vfx_clean = False` lands at `eligible`, not `allow-list` — this is intentional and is the structural fix.

### § 3.3 Three pool-status categories

| Category | Definition | Selector behavior |
|---|---|---|
| **`vfx-clean` (allow-list)** | `d1_total ≥ 8` AND `vfx_catalogue_mapping_clean = True` AND `canonical_pair_leak = False`-or-cluster-collapsed | 2× weighted in sampling per `D1_ALLOW_LIST_WEIGHT = 2` |
| **`vfx-acceptable` (eligible)** | `d1_total ≥ 5` AND (`vfx_catalogue_mapping_clean = True` OR `d1_total ≥ 8 AND Tier-C`) | 1× weighted in sampling; surfaces for variety but doesn't dominate |
| **`vfx-blocked` (quarantine)** | `d1_total < 5` OR Tier-D-with-biological-organic-flag OR Tier-E | Excluded from sampling per `element/selector.py:135` |

The naming `vfx-clean / vfx-acceptable / vfx-blocked` is the canonical operational vocabulary going forward. Existing pool entries' `d1_status` field continues to carry `allow-list / eligible / quarantine` for backward-compatibility with the selector. The two vocabularies are isomorphic.

### § 3.4 Auto-demote logic at pool-load

Already shipped per rocket dispatch 2026-05-17. Pool loader (`element/pool.py`) on load:

1. Merges per-entry tier annotations from `vfx_coverage_manifest.json` into the in-memory `PoolElement`.
2. For each entry where `d1_status == "allow-list"` AND `vfx_catalogue_mapping_clean == False`: auto-demotes to `eligible` and logs WARN.
3. For each entry where manifest assigns Tier-E: auto-demotes to `quarantine` regardless of `d1_total`.

This means new entries can be safely added to `pool.json` at any time WITHOUT requiring an immediate manifest update — they default to `vfx_mapping_tier='unscored' / vfx_catalogue_mapping_clean=False` and auto-demote to `eligible` until the manifest catches up. Conservative-by-default; no silent allow-list promotions.

---

## § 4 — Legolas Mode A commission criteria (F5)

### § 4.1 What legolas executes in F5

F5 is the post-F3 legolas commission. Scope per the 2026-05-17 commission doc (`agentic_orchestration/gandalf/requests/2026-05-17-pool-vfx-catalogue-mapping-audit.md`):

1. **Inventory VFX catalogue concept-coverage** at the canonical-slot level:
   - Direct coverage (Tier A): which substance-concepts ship as-is from Pimen GREEN-list + CreativeKind palette-shift capability?
   - Palette-shift coverage (Tier B): which require palette-only modification?
   - Composite coverage (Tier C): which require palette + compositing?
   - Custom-required (Tier D): which have no clean catalogue mapping?
   - Non-visual (Tier E): which cannot render visually at all?

2. **Per-entry annotation** for the 156 pool entries:
   - `vfx_mapping_tier` ∈ {A, B, C, D, E}
   - Sub-category flag where applicable (biological-organic / liquid-specific / conceptual-abstract / auditory / textural)
   - `canonical_pair_leak` boolean
   - Rationale string per entry

3. **Output document** at `agentic_orchestration/research/knowledge/pool-vfx-catalogue-mapping-audit-2026-05-19.md` (date-shifted from the 2026-05-17 commission doc per F3 fire-date).

### § 4.2 Crucial: prior 2026-05-17 manifest coverage status

Of the 156 pool entries, 156 already have manifest annotations per `data/seasonal_elements/vfx_coverage_manifest.json` (legolas Track A 2026-05-17 inline + gandalf first-principles synthesis per `drift-14-pool-cull-decisions-2026-05-17.md` § 1). **The F5 commission is therefore an audit-and-refinement pass, not a greenfield annotation pass.** Legolas Mode A scope is:

- Verify the 156 existing tier annotations against the current catalogue state (which has not changed since 2026-05-17 — Pimen GREEN-list still 11/13; CreativeKind unchanged).
- Surface any annotations whose Tier judgment is borderline-disputable (e.g., Tier-C-vs-D cases where compositing-difficulty is contested).
- Annotate the residual `canonical_pair_leak` boolean for entries where the 2026-05-17 synthesis didn't capture it explicitly (the manifest carries this field but coverage may be partial).
- Verify the auto-demote outcomes: which `d1_total ≥ 8` entries currently carry `vfx_catalogue_mapping_clean = False` and therefore get auto-demoted at load time. This is the operational ground-truth for the post-cull pool composition.

**Time cap:** 3–5h legolas (the existing 156-entry manifest collapses this from the original "audit all 156 from scratch" scope to "verify + refine 156 existing").

### § 4.3 Findings-blocker surfacing

If F5 surfaces:

- A Tier-D-vs-Tier-C disagreement where the rocket auto-demote outcome would shift materially → gandalf re-scoring pass adjudicates (§ 5)
- A new sub-category flag pattern not yet captured (e.g., a "monster-anatomy" cluster surfaces with horn / claw / tooth being adjacent to chierit monster-substrate) → flag for gandalf canonical-doc amendment
- A Tier-2 vendor pack (e.g., CraftPix premium wood-nature; Fellor Crystal pack from 2026-05-17 cull-decisions § 3) that, if acquired, would shift a cluster of entries from Tier-D to Tier-B → flag for vendor-acquisition routing

These surface to gandalf at F5 closure; gandalf decides scope (in-VS2a refinement vs VS2b deferral).

---

## § 5 — Re-scoring pass workflow (gandalf-side; F5 closure deliverable)

After legolas Mode A lands, gandalf re-scores the 156 entries against the refined annotations:

### § 5.1 Pass 1 — Verify auto-demote outcomes

Inspect `data/seasonal_elements/pool.json` post-F5-manifest-update for the auto-demote state:

```bash
# operational sanity check (not a script; the inspection pattern)
For each entry in pool.json:
  If d1_status == "allow-list" AND vfx_catalogue_mapping_clean == False:
    Verify: this entry is being auto-demoted at pool-load (WARN log fires)
    Adjudicate: should the manifest annotation flip (Tier-D → Tier-C upgrade), or should this entry stay demoted?
```

Per rocket math note § 2.4: target post-auto-demote allow-list size is ~55 entries (down from 81 pre-cull). The actual post-F5 number is the empirical anchor; if it deviates materially from the target, surface for gandalf review.

### § 5.2 Pass 2 — Refine borderline Tier judgments

For Tier-C-vs-Tier-D borderline cases that legolas surfaced (per § 4.3), gandalf adjudicates with the design lens: *"would shipping this entry surface as 'X-strike with Y-VFX' produce cognitive dissonance the player would notice?"* If yes → Tier-D. If no → Tier-C.

### § 5.3 Pass 3 — Author the culled-pool summary (forward-reference doc)

If material changes land at F5 (beyond what the 2026-05-17 cull-decisions doc already captured), author a forward-reference summary at `canonical/story/pool-vfx-mapping-culled-2026-05-19.md` enumerating:

- Entries with status changes vs the 2026-05-17 baseline
- New cluster-collapse decisions (if any)
- Forward routing for vendor-acquisition opportunities

If the F5 outcome is "manifest annotations verified; no material changes" → no new summary doc needed; this framework + the existing 2026-05-17 cull-decisions doc are the canonical reference.

### § 5.4 Effort estimate

Per the 2026-05-17 commission doc § Track B: ~4–6h gandalf. Post-F5 (where 156 entries are already annotated), the realistic effort is ~2–3h gandalf to verify + adjudicate residual borderline cases.

---

## § 6 — Selector hard-floor recommendation

### § 6.1 Status: SHIPPED 2026-05-17

The selector hard-floor on `vfx_catalogue_mapping_clean` is **already shipped** per rocket dispatch 2026-05-17 (`agentic_orchestration/dispatches/2026-05-17-rocket-drift-14-pool-cull-and-selector-hardfloor-amendment.md`). Per implementation at `reincarnated-engine/src/reincarnated/element/pool.py` lines 73-99:

- Pool loader merges manifest annotations at load time.
- Entries with `d1_status == "allow-list"` AND `vfx_catalogue_mapping_clean == False` are auto-demoted to `eligible` with WARN log.
- Entries with Tier-E annotation are auto-demoted to `quarantine` regardless of `d1_total`.

This is Track 1 of the 2026-05-17 § 2 amendment ("MINIMUM-VIABLE cut, Tracks 1 + 2"). Track 2 (`canonical_pair_leak` boolean dimension) is also captured in schema. Track 3 (cluster effective-selection-probability floor) is DEFERRED post-VS2a per the 2026-05-17 decision and remains DEFERRED in this framework — revisit if post-pool-cull empirical regen surfaces a new cluster-pressure pattern.

### § 6.2 Forward-extension recommendation

For future pool additions (Phase-1 P1 substrate-expansion entries; future season-themed vocabulary growth):

**REQUIREMENT:** Any new pool entry MUST be added with both:
1. `pool.json` entry (canonical fields + D1 conceptual scoring)
2. `vfx_coverage_manifest.json` entry (Tier A–E annotation + `vfx_catalogue_mapping_clean` boolean + sub-category flag + rationale)

The pool loader already enforces this in the conservative direction (missing manifest entry → defaults to `vfx_catalogue_mapping_clean = False` → auto-demote on next load). The recommendation here is **process discipline** — pool additions should fire as paired commits (pool entry + manifest entry) rather than relying on auto-demote as the safety net.

**No new selector code change is recommended in F3 / F5 closure.** The Track 1 + Track 2 amendment shipped 2026-05-17 covers the scope of this framework. The selector hard-floor recommendation surface is **forward-flag only** for Phase-1 P1 substrate-expansion routing.

---

## § 7 — Discipline #15 candidate

This framework's existence operationalizes a forward-discipline-candidate originally surfaced in the 2026-05-17 commission doc and the drift-audit § Drift-14 entry:

**D15 candidate text:** *"Pool-vs-catalogue mapping must be scored at pool-introduction time, not deferred to ship-time. Any pool entry that will become player-visible at a downstream ship MUST be scored against the operational catalogue at pool-introduction time, not just against conceptual rubric properties."*

**Forward-flag for jack-ryan engineering-disciplines pass.** Surface alongside the cluster identified in `canonical/story/drift-audit.md` § Drift-15 Action (D16 candidate; "Multi-axis-catalogue-scoping requires explicit axis-enumeration at scoping time"). Disciplinary cluster currently at 6+ items per the drift-audit forward-flag (D14, D15, D16, R11(b), Pattern P7 cluster, Drift-11 sibling-cluster-sweep lesson) — strong empirical basis for a coordinated jack-ryan pass when capacity allows.

---

## § 8 — Drift-14 entry update for drift-audit.md

The Drift-14 entry in `canonical/story/drift-audit.md` § Drift-14 was filed 2026-05-17 with action items:
- Drift-14 entry archived (DONE)
- Gap-closure commission filed (DONE — both legolas Track A + gandalf Track B commissions executed 2026-05-17)
- Discipline #15 forward-flag (PENDING)

**F3 framework update (this doc) makes the following amendments to the Drift-14 entry:**

- **Closure status:** advance from "in-progress" to "framework-formalized; F5 audit + gandalf re-scoring pass remaining". The Track A legolas inline + Track B gandalf cull-decisions + rocket auto-demote logic + schema + manifest are all SHIPPED. The F5 commission is the verification + refinement pass.
- **Final closure trigger:** F5 lands → manifest verified → auto-demote outcomes confirmed → `vs2a/v0.10-drift14-audit-complete` tag fires.
- **Cross-reference addition:** point to this framework doc as the formalization-of-doctrine reference.

The entry text amendment is appended below in § 8.1 for direct application to `drift-audit.md`.

### § 8.1 Drift-audit entry amendment (apply to drift-audit.md § Drift-14 § Action)

Replace:
```
**Action:**
- Drift-14 entry archived here (this section).
- Gap-closure commission filed at `agentic_orchestration/gandalf/requests/2026-05-17-pool-vfx-catalogue-mapping-audit.md` — legolas Mode A catalogue audit + gandalf re-scoring pass...
- Forward discipline candidate (D15-candidate territory per P6 forward audit § sub-pattern naming): "Pool-vs-catalogue mapping must be scored at pool-introduction time, not deferred to ship-time."
```

With:
```
**Action:**
- Drift-14 entry archived here (this section).
- Gap-closure commission filed 2026-05-17 at `agentic_orchestration/gandalf/requests/2026-05-17-pool-vfx-catalogue-mapping-audit.md`. Legolas Track A inline annotations + gandalf Track B cull-decisions doc + rocket selector-hardfloor amendment SHIPPED 2026-05-17 (manifest at `data/seasonal_elements/vfx_coverage_manifest.json`; schema + auto-demote at `reincarnated-engine/src/reincarnated/element/pool.py`).
- Framework formalization SHIPPED 2026-05-19 at `canonical/story/d1-rubric-vfx-mapping-extension-2026-05-19.md` (F3 deliverable; gates F5). Names the doctrine so future pool additions inherit it without re-derivation.
- F5 legolas Mode A audit + gandalf re-scoring pass remaining (verification + refinement of 156-entry manifest annotations); `vs2a/v0.10-drift14-audit-complete` tag fires at F5 closure.
- Forward discipline candidate D15 territory (per P6 forward audit § sub-pattern naming): "Pool-vs-catalogue mapping must be scored at pool-introduction time, not deferred to ship-time." Surface to next jack-ryan engineering-disciplines pass alongside D16 territory + R11(b) + Pattern P7 silent-drop cluster + Drift-11 sibling-cluster-sweep lesson.
```

---

## § 9 — Cross-references

- F3 dispatch authoring this framework: `agentic_orchestration/dispatches/2026-05-19-gandalf-vs2a-drift14-15-framework.md`
- Drift-14 commission origin: `agentic_orchestration/gandalf/requests/2026-05-17-pool-vfx-catalogue-mapping-audit.md`
- Cull-decisions execution: `canonical/story/drift-14-pool-cull-decisions-2026-05-17.md`
- Rocket dispatch (auto-demote + schema): `agentic_orchestration/dispatches/2026-05-17-rocket-drift-14-pool-cull-and-selector-hardfloor-amendment.md`
- Rocket math note: `reincarnated-engine/design/notes/drift-14-d1-substrate-native-rescore-math-2026-05-17.md`
- Drift-audit entry: `canonical/story/drift-audit.md` § Drift-14
- Cipher migration architecture: `canonical/37-form-bias-diagnosis-and-recovery.md` § 6 + `canonical/story/form-bias-cadence-strategy.md` § 7.2
- Style register (score-don't-filter principle): `canonical/story/style-register.md`
- VFX catalogue: `agentic_orchestration/research/catalogue/cross-vendor-substrate-inventory-2026-05-16.jsonl`
- VFX coverage assessment: `canonical/story/geometry-vfx-coverage-assessment.md`
- Pool data: `reincarnated-engine/data/seasonal_elements/pool.json` + `reincarnated-engine/data/seasonal_elements/vfx_coverage_manifest.json`
- Substrate-expansion (Branch-A confirmation; carries Drift-14 amendment forward): `canonical/story/substrate-expansion-decision-2026-05-17.md`
- VS2a scope-of-work: `agentic_orchestration/hive-mind/scope-of-work-vs2a.md` § 1.3 (F3) + § 2.8 (F5)

---

*Framework filed 2026-05-19 by gandalf under autonomous-operation authority (VS2a hive-mind protocol § 4.0). F3 deliverable. The doctrine the 2026-05-17 cull-cascade was authored against; named here so future seasons inherit it cleanly. F5 legolas commission unblocked.*
