# Pivot-Insurance Ledger — Catalogue Coverage Monitoring

**Status:** **Active (substrate-layer resolutions recorded 2026-05-16; per-asset curation passes still pending).** Substrate-track entries below; per-pass embodiment-coverage entries will append when curation script processes the first Legolas sample.
**Author:** elrond.
**Pattern:** gandalf-commissioned (dialogue 2026-05-16 Topic 6 addition). Surfaces silent pivot-insurance erosion at the catalogue layer — the asymmetric-stewardship analogue of `engineering-disciplines.md` Discipline #13 (implicit-pillar drift).
**Audience:** elrond + knight-rider, monthly-ish scan. Surfaces to gandalf when erosion thresholds trip.
**Companion:** `curation-pipeline.md` § 3 step 12 (where the curation script writes here); `catalogue-schema.md` § 5.4 (the underlying query); `catalogue-rubric-schema.md` § 9 dialogue Topic 6.

---

## 0. What this ledger is

Score-don't-filter (`AGENTS.md`) is only honored if pivot-insurance coverage is **actively monitored as the catalogue grows**, not just queryable on demand. This ledger is the active monitor.

Each curation pass appends one entry capturing:
- Total catalogue size after this pass
- Per-`derived_register` asset counts (the score-don't-filter signal)
- Per-embodiment coverage in `hand-drawn-pixel` (the locked register) AND in next-most-populated register (the pivot candidate)
- Embodiments where pivot-insurance is near-zero (< 5 assets in pivot-candidate register)

The first time pivot-insurance drops below viability on a specific embodiment — say, 200 hand-drawn-pixel slimes but 3 retro-16bit slimes — that's a coverage gap that means a register pivot *cannot* preserve that embodiment without a fresh crawl. The ledger surfaces this so the team can act before it's an emergency.

---

## 1. Erosion thresholds (initial v1.0)

Each entry's coverage table is scanned against these thresholds. Threshold trips drive surfaces to knight-rider in the run summary.

| Threshold | Condition | Surface |
|---|---|---|
| **Yellow — thin coverage** | Embodiment has <10 assets in `hand-drawn-pixel` AND <5 in next register | Log to ledger; mention in run summary |
| **Orange — pivot-blocked** | Embodiment has ≥10 in `hand-drawn-pixel` but 0 in any other register | Log + flag to knight-rider; consider gap-fill Legolas commission |
| **Red — locked-register thin** | Embodiment has <5 in `hand-drawn-pixel` itself | Log + flag to knight-rider + surface to gandalf; locked-register coverage gap, not just pivot gap |
| **Black — register-wide erosion** | A whole `derived_register` value has dropped below 10 catalogue-wide | Should not happen organically; would signal a curation-fail event |

Thresholds are tunable per future data; v1.0 starts conservative.

---

## 2. Coverage entries (append-only)

Newest entry at the top. Format documented; first real entry appended when curation runs.

### Template

```markdown
## Pass <YYYY-MM-DD> — session <session-id>

**Triggered by:** <legolas-session-id> curation pass
**Total catalogue size:** <N> rows current (non-superseded)

### Per-register counts

| derived_register | count | delta vs prior pass |
|---|---|---|
| hand-drawn-pixel | <N> | <+M / -M / new> |
| retro-16bit | <N> | <delta> |
| clean-vector | <N> | <delta> |
| painterly-raster | <N> | <delta> |
| anime-cel | <N> | <delta> |
| manual-review | <N> | <delta> |

### Per-embodiment coverage (character + enemy categories only)

| embodiment_tag | hand-drawn-pixel | next-most-populated register (count) | erosion threshold |
|---|---|---|---|
| humanoid | <N> | retro-16bit (<N>) | <green / yellow / orange / red / black> |
| slime | <N> | retro-16bit (<N>) | <threshold> |
| beast | <N> | retro-16bit (<N>) | <threshold> |
| dragonling | <N> | retro-16bit (<N>) | <threshold> |
| swarm | <N> | retro-16bit (<N>) | <threshold> |
| construct | <N> | retro-16bit (<N>) | <threshold> |
| spirit | <N> | retro-16bit (<N>) | <threshold> |
| plant | <N> | retro-16bit (<N>) | <threshold> |
| pending-amendment | <N> | (n/a — blocked from filtering) | (n/a) |

### Pending-amendment hint clusters

| hint pattern | count | candidate amendment | accumulation since first observed |
|---|---|---|---|
| 'undead-skeleton' | <N> | undead | <date> first observed |
| ... | | | |

### Threshold flags

<list any embodiments tripping yellow / orange / red / black; rationale; recommended action>

### Notes

<curator notes; cross-source observations; vendor patterns>
```

---

## 3. Initial state (pre-curation baseline — 2026-05-16)

No assets curated yet. Catalogue.db is empty. The v1.0 schema is applied; the first Legolas Pimen sample dispatch (held pending this rubric lock) will produce the first inputs.

**Pre-curation expected initial state** (per `catalogue-rubric-validation-2026-05-16.md` § 4 coverage report — what the catalogue should look like after the first major curation passes named in the validation pass):

- **Total catalogue size:** ~800-1100 assets across `hand-drawn-pixel` + `retro-16bit` + `clean-vector`
- **Per-embodiment in `hand-drawn-pixel`** (character+enemy):
  - humanoid: ~60 (LuizMelo / Elthen / CreativeKind) — GREEN
  - slime: ~5-10 — **YELLOW or RED**
  - beast: ~15-20 — YELLOW
  - dragonling: ~10-15 — YELLOW
  - swarm: ~3-5 — **RED**
  - construct: ~5-10 — **YELLOW**
  - spirit: ~5-10 — **YELLOW**
  - plant: ~3-5 — **RED**

**Anticipated first threshold flags:**

- **RED**: swarm + plant + likely slime — fewer than 5 assets in the locked register. These embodiments need direct gap-fill via either targeted Legolas commission or LLM image generation.
- **YELLOW**: beast / dragonling / construct / spirit — thin coverage. Acceptable for v1.0 but monitor.
- **`pending-amendment` cluster expected**: `'undead-skeleton'` from LuizMelo Skeleton pack will be the first canonical `pending-amendment` entry; accumulation pressure for an `undead` narrative-layer amendment.

This pre-curation snapshot is a forecast — the first real ledger entry will overwrite/confirm/refute it. Recorded here so future entries have a baseline.

---

## 3a. Substrate-layer resolutions — 2026-05-16 (cipher-width sub-lock resolution)

This section captures substrate-track resolutions from elrond's 2026-05-16 emergent-grouping analysis (delivered inline; operationalized via dispatch `2026-05-16-elrond-catalogue-cleanup-post-step-b.md`). It runs orthogonal to the per-pass embodiment-coverage entries below — both layers participate in pivot-insurance monitoring, but at different abstraction levels.

### Substrate-width resolution (Outcome 2 — single classical-element-anchored grouping)

- **Decision:** 4-6-substrate-tag width; classical-element-anchored single grouping (fire / water / earth / lightning + optional ice / wind / holy / dark / melee-slash as substrate-anchor candidates).
- **Cipher-width sub-lock status:** RESOLVED per in-pending decisions-log entry `qa/pending/2026-05-16-decisions-log-cipher-width-resolution.md`.
- **Pivot-insurance implication:** Outcome 1 (multi-grouping architecture) remains AVAILABLE but is currently INACTIVE — per-substrate n is thin (1-2) for the 17 novel substrate tags; multi-grouping cannot be supported empirically without Tier-2 crawl raising per-substrate n above 3.

### 4 flag adjudications applied operationally

| Flag | Adjudication | Operational state | Reversal path |
|---|---|---|---|
| Pixogen include-vs-exclude | EXCLUDE (license-pending) | Pixogen rows flagged `cipher_width_analysis_inclusion: false` in `cipher-width-inclusion-flags-2026-05-16.jsonl`; cross-vendor inventory's Pixogen substrates (void-spatial, technology-vfx) flagged with inclusion=false breakdown; technology-vfx substrate becomes UNATTESTED (Pixogen-exclusive). | If Matt verifies the Pixogen license (afgameassets@gmail.com — terms in 18 kB downloadable file), re-include Pixogen rows. Per-effect sub-pack curation precedes re-clustering (separate elrond dispatch). Cluster CLARITY of classical-element anchors will degrade with Pixogen re-included; this is acceptable cost if license verifies. |
| Blood split-vs-merge | MERGE (single L2 substrate) | Cross-vendor inventory `blood` substrate row supersedes prior `blood-life-drain` + `blood-wound` rows. Vendor sub-registers (`physical-injury` vs `sanguine-magic`) preserved as L3 vocabulary differentiation. | If future evidence (e.g., a Tier-2 crawl that introduces a third blood sub-register that doesn't cluster with the existing two) shows substrate-layer separation is empirically supported, re-split. Currently no empirical signal for split. |
| Acid vs Poison adjacency | SPLIT (distinct L2 substrates) | Cross-vendor inventory keeps `acid` (Pimen) and `poison-biological` (Fellor + CreativeKind + CraftPix) as distinct L2 substrate rows. Mechanical adjacency (both DoT) noted; cluster-distinct per elrond's analysis (acid → C2 buff/status; poison-biological → C7 kinetic mega-cluster). | If future LLM prompt-construction work surfaces semantic collisions that the cluster-distinct boundary doesn't resolve cleanly, reconsider merge. Currently no operational pressure for merge. |
| CraftPix vector inclusion | INCLUDE (substrate-side); defer register filtering to drax | Cross-vendor inventory marks `craftpix-topdown-wind-lightning` + `craftpix-magic-sprite-vector` with `register_axis: "vector"` + `cipher_width_analysis_inclusion: true`. New substrate row `multi-element-vector-aura` added to capture the second vector pack's register-axis explicitly. | If drax's register-filter consumption-side work surfaces a need for substrate-side register separation (e.g., vector-only substrate analysis), revisit. Currently register-axis is consumption-side; substrate-side is register-agnostic. |

### Pivot-insurance status across substrate layer (post-cleanup)

- **Outcome 2 width (4-6 tags):** STABLE; matches Foundation 4-rotating-plus-1-physical structure (L2-decoupled per Sub-lock 2). No pivot pressure.
- **Outcome 1 (multi-grouping):** AVAILABLE but EVIDENCE-CONSTRAINED. Per-substrate n needs to grow above 3 for novel substrates before Outcome 1 can be empirically supported. Future Tier-2 catalogue crawl (specialist novel-substrate vendors) is the binding pivot prerequisite. Ledger documents the gap; not a current blocker.
- **Pixogen reversal:** SINGLE-POINT-OF-FAILURE for technology-vfx substrate (Pixogen-exclusive; license-pending exclusion strips all evidence). If Matt does not verify Pixogen license, technology-vfx substrate remains UNATTESTED in operational analysis. Acceptable degraded state: technology-themed seasons would lose substrate-evidence support and would rely on per-season vocabulary L2-decoupled fill against the L1 abstract pair structure (β coupling already accommodates this).
- **Singleton-vendor novel substrates:** crystal-gem-arcane (Fellor), time-temporal (Pipoya), warp-teleportation (Pipoya), chromatic-arcane (CreativeKind), shadow-kinetic (Frostwindz), midas-golden-transform (CraftPix), implosion-gravity (CraftPix), summoning-ritual-object (CraftPix), void-adjacent-arcane (Frostwindz). All n=1; no independent grouping; available for per-season vocabulary L2 fill but cannot anchor a multi-grouping architecture without n raising.

### Cross-refs

- `agentic_orchestration/research/catalogue/cross-vendor-substrate-inventory-2026-05-16.jsonl` — substrate inventory (modified 2026-05-16 to apply 4 flag adjudications)
- `agentic_orchestration/research/curated/cipher-width-inclusion-flags-2026-05-16.jsonl` — per-asset inclusion-flag sidecar (read-only respect for legolas's per-vendor JSONLs)
- `agentic_orchestration/research/curated/post-step-b-cleanup-2026-05-16.md` — cleanup-note capturing the operational application
- `agentic_orchestration/qa/pending/2026-05-16-decisions-log-cipher-width-resolution.md` — in-pending decisions-log entry (this ledger entry precedes the entry's commit; downstream consumers benefit from operational state matching the locked state)

---

## 4. Scan protocol

Knight-rider or elrond scans the ledger:
- **Routinely** — at every curation pass, the script summary surfaces threshold flags. Quick read.
- **Monthly-ish** — full-ledger read to catch slow erosion. If a yellow embodiment has been yellow for 3+ passes, that's structural; surface for design discussion.
- **At register-pivot-evaluation moments** — full-ledger read is the empirical basis for "can we pivot?" Each embodiment's pivot-candidate count is the actual answer.

---

## 5. Cross-references

- `curation-pipeline.md` § 3 step 12 — where the curation script writes to this ledger
- `catalogue-schema.md` § 5.4 — the SQL query underlying ledger generation
- `catalogue-rubric-schema.md` § 9 Topic 6 — the dialogue origin of this monitoring discipline
- `catalogue-rubric-validation-2026-05-16.md` § 4 — coverage report informing the pre-curation forecast
- `canonical/story/style-register.md` § "Pivot insurance" — the design intent this ledger serves
- `canonical/story/embodiment-narrative-layer.md` — embodiment taxonomy

---

## 6. Maintenance protocol

When v2.0 rubric or schema changes the embodiment enum, the ledger format updates accordingly. Historical entries are preserved as-was — historical coverage was correct under the prior rubric version.

When a new register becomes a serious pivot-candidate (currently `hand-drawn-pixel` is the lock; `retro-16bit` is the de facto first-pivot; `clean-vector` is the second), the ledger format updates to track the relevant candidate's coverage.

When the project pivots register, the ledger's pivot-candidate column shifts to the new candidate; the prior locked register becomes the new pivot-candidate. The ledger transitions; old entries are preserved.

---

— elrond, 2026-05-16
