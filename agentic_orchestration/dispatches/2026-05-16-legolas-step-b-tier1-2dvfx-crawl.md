# Dispatch — 2026-05-16 — legolas — Step B: Tier-1 2D-VFX exhaustive crawl (Mode B)

**From:** knight-rider (authored per gandalf commission `agentic_orchestration/gandalf/requests/2026-05-16-step-b-tier1-2dvfx-crawl-commission.md`)
**To:** legolas
**Approved by:** Matt at 2026-05-16 Day 4 dialogue (commission binding criteria + sequencing locked; per-vendor depth = Q2(b) substrate-distinct + sampled). Step B activation approved 2026-05-16 Day 4 after gandalf gate-3 review PASS-WITH-AMENDMENTS (finding at `agentic_orchestration/qa/findings/2026-05-16-gandalf-step-b-gate3-review.md`) + Matt approval on Pipoya inclusion (10-vendor list).
**Status:** PENDING — ACTIVE (2026-05-16 Day 4 — both HELD gates closed; gandalf gate-3 review PASS-WITH-AMENDMENTS; Matt approved Pipoya inclusion bringing finalized Tier-1 list to 10 vendors; 3 dispatch amendments C.1-C.3 integrated below)
**Held-pending-gates (HISTORICAL — all closed 2026-05-16):**
1. ✅ Step A methodology validation — elrond GREEN-LIGHT verdict (findings `qa/findings/2026-05-16-elrond-step-a-methodology-smoke-test.md`); methodology locked (7-mechanic-family collapse accepted with post-Step-B amendment-trigger per Q-PRI-2)
2. ✅ Vendor-discovery sweep findings — legolas Mode A sweep COMPLETE (`research/knowledge/asset-catalogues/2026-05-16-vendor-discovery-sweep.md` — 4 net-new candidates); gandalf gate-3 review screened the candidates against binding inclusion criteria + finalized the Tier-1 list (10 vendors)

**Estimated effort:** 2–4 sessions Mode B (~6–16 hours total); depends on the final vendor count after gandalf screening (expected: 6–10 vendors).
**Acceptance:** Per-vendor JSONL crawl artifacts + per-vendor findings summaries + cross-vendor substrate-tag inventory delivered. Elrond's downstream emergent-grouping analysis commission consumes the output.

---

## Context — why this dispatch exists

Per gandalf commission `agentic_orchestration/gandalf/requests/2026-05-16-step-b-tier1-2dvfx-crawl-commission.md` and the form-bias-cadence-strategy doc § 5.3 + § 6.2:

- The cipher-width sub-lock (Options A / B / C from the parked canonical-elements thread) is the largest of four deferred form-bias sub-locks
- Per § 6.2's framework, three outcomes are possible from elrond's emergent-grouping analysis:
  - 3-5 robust groupings emerge → multiple-groupings architecture viable
  - 1-2 groupings survive → refined-Option-A collapses to single fixed grouping
  - No grouping survives → canonical-four cipher remains operative
- **Step B's substrate-width crawl determines the ceiling on which outcome can land.** Substrate-evidence quality determines cipher-width decision quality.

The commission locks five binding criteria (Q1-Q5) via Day-4 Matt dialogue. This dispatch operationalizes them per Legolas Mode B convention.

## Strategic-axis context (load-bearing)

Per form-bias-cadence-strategy § 5.1:
- **Sub-lock (a):** ARPG-canon-primary at substrate-mechanical layer — preserved through Step B (no substrate addition disrupts the mechanical schema)
- **Sub-lock (b):** Isekai-canon-primary at narrative-skin and convergence layers — the substrate work feeds the cipher's grouping/vocabulary layers per § 6.1's three-layer model

The four deferred catalogue-track sub-locks resolve at named gates downstream of this commission. Step B is the catalogue-evidence supplier for the cipher-width decision specifically.

## Binding inclusion criteria (all three must hold for a vendor to enter the Tier-1 list)

Per commission § "Binding criteria for Tier-1 list":

1. **Empirical-research-base eligibility.** Source appears in `research/knowledge/asset-catalogues/2026-05-16-pixijs-compatible-2d-vfx-libraries.md` (existing research) OR in `research/knowledge/asset-catalogues/2026-05-16-vendor-discovery-sweep.md` (Dispatch 1 output) as Pixi.js-compatible above quality floor.
2. **Substrate-variance contribution.** Source either:
   - (a) ships effects under at least one label distinct from Pimen's 9 + standard canonical-four, OR
   - (b) ships across >7 distinct effect-type labels (multi-element breadth, even if labels overlap with Pimen), OR
   - (c) ships strong kinetic-VFX coverage (weapon-trails / slashes / impact / stagger / stun / knockback) regardless of elemental breadth.
3. **License clarity.** Free or paid; commercial-licensing terms unambiguous; provenance documentable; no AI-content-default.

## Binding rejection criteria (any one is disqualifying)

1. **3D-render or runtime-shader sources** — architecture-incompatible.
2. **Single-element specialist below substrate-novelty threshold** — adds quantity-within-tag, not substrate variance. (Specialists shipping a *novel* substrate-tag — e.g., necrotic-only — qualify under inclusion #2a or #2c.)
3. **AI-generated content default** — pitch-positioning risk.

## Finalized Tier-1 list (10 vendors — gandalf-screened 2026-05-16; Matt approved Pipoya)

Per gandalf's gate-3 review finding (`agentic_orchestration/qa/findings/2026-05-16-gandalf-step-b-gate3-review.md`):

| # | Vendor | Verdict | Substrate gap closed / role |
|---|---|---|---|
| 1 | **Pimen** | included (baseline; already crawled at `research/catalogue/pimen/full-2026-05-16.jsonl`) | substrate reference anchor — do NOT re-crawl; reference the existing JSONL |
| 2 | **ansimuz** | PASS | retro-band complementary; multi-element breadth |
| 3 | **Brackeys VFX Bundle** | PASS | free impact/burst baseline |
| 4 | **CraftPix** | PASS | vector + niche-mechanic (petrification, charm, midas, starfall) + weapon-trail/slash |
| 5 | **CreativeKind** | PASS | hand-drawn-pixel sub-register variance |
| 6 | **Frostwindz (full catalogue)** | PASS | closes death/necrotic + blood/life-drain + cosmic substrate gaps (5 distinct novel substrates) + class-archetype kinetic. **Flag C.3 applies** — see § "Amendments C.1-C.3" below |
| 7 | **Pixogen** | PASS-WITH-CAVEAT (license) | Void distinct from Dark + fully novel Technology substrate; 11 effect-type labels. **Flag C.2 applies** — see § "Amendments C.1-C.3" below |
| 8 | **CodeManu** | PASS-WITH-CAVEAT (100x100 canvas) | deepest kinetic vendor (44 impact/hit); directly addresses Q5 kinetic-VFX inclusion clause. Drax ingest pipeline already supports variable canvas sizes (Stage 2) — no blocker |
| 9 | **Fellor** | PASS-WITH-CAVEAT (quality-floor) | Crystal substrate fully novel; Poison palette-register variance |
| 10 | **Pipoya** | PASS (Matt-approved 2026-05-16 per gandalf C.4 recommendation) | Time/Warp substrate — cipher-width framework should not assume away temporal-grouping outcome |

This is the screened list; no further gandalf screening required. Crawl all 10 vendors per the per-vendor methodology below.

## Amendments C.1, C.2, C.3 (gandalf gate-3 review — operational disciplines for the crawl)

Per gandalf gate-3 review finding § "Step B dispatch amendments recommended". These augment the per-vendor methodology below; apply them to every vendor crawl.

### C.1 — Vendor-namespaced mechanic-tag extraction requirement

**What:** For each pack, extract mechanic-tags using the **vendor's own vocabulary** (e.g., Frostwindz's "necrotic-cast" / "blood-drain" / "cosmic-burst"; CodeManu's "weapon-trail" / "impact-burst"; etc.) — NOT pre-collapsed into elrond's 7 mechanic-families. Store the raw vendor mechanic-tag string in the JSONL row as a separate field (e.g., `vendor_mechanic_tags: ["necrotic-cast", "death-bolt"]`).

**Why:** Elrond's Step A methodology collapses 22 fragmented Pimen mechanic-tags into 7 families for clustering. That collapse is locked for Step B's emergent-grouping analysis BUT loses substrate-distinct signal at the original vocabulary level. Preserving the vendor-namespaced raw tags means the substrate-evidence is recoverable downstream when elrond extends to ~10 families post-Step-B (per gandalf's amendment-trigger).

**Applies to:** every pack in every vendor crawl (substrate-distinct AND substrate-redundant).

### C.2 — License-verification artifact requirement

**What:** For vendors where license terms are not publicly readable from the vendor catalogue page (specifically flagged: **Pixogen** — license file in downloadable 18kB artifact), fetch the license artifact at crawl time and record full terms verbatim in the per-vendor findings summary doc. If the license cannot be verified (artifact unavailable; download requires purchase; vendor unresponsive), flag the vendor as `license_unverified: true` and SURFACE TO KNIGHT-RIDER before considering the vendor for inclusion in the elrond emergent-grouping analysis (downstream commission).

**Why:** Operationalizes binding inclusion criterion #3 (license clarity) for vendors hiding license behind a download. Avoids the failure mode where a vendor passes screening on inferred license but the actual terms are incompatible.

**Applies to:** vendors where vendor-page license inspection is insufficient. Pixogen confirmed; others may surface.

### C.3 — 404-retry + inferred-substrate flagging discipline

**What:** When a pack page returns 404 (specifically flagged: **Frostwindz** Starcaller / Warlock / Paladin packs surfaced in the legolas Mode A sweep), apply this discipline:

1. **Retry with alt slugs** — try canonical-name variants (e.g., url-encoding fix; trailing-slash; case variants; vendor's typical URL-shape patterns)
2. **If 404 persists,** mark the pack metadata with `direct_pack_verification: false` AND `substrate_inference_source: "<vendor-profile-text / search-result-snippet / etc.>"` — recording WHERE the substrate claim came from when it wasn't direct
3. **Do NOT include the pack in JSONL row** as if it were directly verified — separate-section in the per-vendor findings summary doc captures "inferred packs (not directly verified)" for transparency

**Why:** Preserves substrate-evidence provenance quality. Inferred packs may still inform substrate-coverage analysis (knowing a vendor SHIPS necrotic effects matters even if the specific pack page is dead), but they must NOT contribute to the substrate-distinct-evidence pool with the same weight as directly-verified packs. Elrond's downstream emergent-grouping analysis depends on this distinction.

**Applies to:** any 404'd pack page across any vendor crawl.

## Per-vendor crawl methodology (locked: Q2 option b — substrate-distinct + sampled)

For each Tier-1 vendor:

### Step B.1 — Metadata-only pre-pass

Inspect vendor's catalogue index pages. Identify substrate-distinct packs — packs surfacing a label not yet seen across previously-crawled Tier-1 vendors.

This is a labeling exercise, not a crawl. Output: a per-vendor pre-pass note listing pack-IDs flagged substrate-distinct vs substrate-redundant.

### Step B.2 — Substrate-distinct packs: exhaustive crawl

Full Mode B treatment per the `pimen/full-2026-05-16.jsonl` precedent:
- One JSONL row per pack
- Full metadata extraction (pack name, primary URL, element/mechanic coverage, file format, license, cost)
- Canvas info (resolution_band, sprite layout, file format)
- License terms with attribution requirements explicit if applicable
- Format flags (RAR / ZIP / individual frames / Aseprite source available / etc.)

### Step B.3 — Substrate-redundant packs: representative sampling

2-3 packs per redundant substrate-tag per vendor. Enough to confirm coverage breadth without full-catalogue depth.

**Rationale (per commission):** the substrate-variance question is answerable from substrate-distinct + sampled coverage. Full-exhaustive depth becomes useful at consumption time (purchase decisions), which is downstream of cipher-width lock. Saves ~50% Legolas bandwidth with no substrate-evidence loss.

## VFX-category scope (locked: Q3 — all three included)

Crawl scope includes ALL THREE categories:

1. **Skill-effect VFX** (Fireball, Ice Spike, etc.) — primary target; full crawl per methodology above.
2. **Ambient / environmental VFX** (burning torches, flowing water, weather effects, ambient glow) — included; substrate-evidence contributor (e.g., a vendor's ambient-water differs from their skill-water in register and signals catalogue depth).
3. **Status / impact / hit-spark / collision / force VFX** — included; combat-feel layer; kinetic-VFX evidence per Q5.

## Bundled-character handling (locked: Q4)

- **Bundled inside primary-VFX packs** (e.g., Pimen Earth Spell 03's bundled Earth Elemental enemy character): **included free**; no extra crawl cost; flag in pack metadata as `bundled_character: true`.
- **Standalone character-only vendors:** **out-of-scope**. Separate follow-on character-track sub-commission per the gandalf-pimen-design-review's flag.

## Kinetic-VFX explicit inclusion clause (locked: Q5 practical)

The existing engine has skills/abilities that aren't element-coded and need VFX: sword-strikes, weapon-trails, impact bursts, stagger/stun visuals, knockback effects. Pimen does not purpose-cover this (Hit Spark and Buff/Debuff are closest; neither is a true weapon-trail or slash pack).

**Step B explicitly seeks kinetic-VFX coverage.** Vendors specializing in kinetic-VFX qualify under inclusion #2c even with thin elemental breadth.

**Architectural rename ("physical → kinetic" + per-embodiment narrative skin) is NOT a Step B decision.** It lands at Stage 4 of the form-bias migration (display layer + per-embodiment skin work — see strategy doc § 7.1). Step B's job is substrate-evidence; the rename's job is player-facing-vocabulary downstream. Foundation 4+1 stays operative through Step B unchanged.

## Output format

**Per-pack JSONL row:** schema matches `research/catalogue/pimen/full-2026-05-16.jsonl` precedent. Add `bundled_character: true/false` field per Q4.

**File location:** `agentic_orchestration/research/catalogue/<vendor-slug>/full-2026-05-XX.jsonl` (one file per vendor; XX = crawl date).

**Per-vendor findings summary doc:** `agentic_orchestration/research/catalogue/<vendor-slug>/findings-summary-2026-05-XX.md` — substrate-evidence headline; novel substrate tags surfaced; license summary; consumption-readiness flags.

**Cross-vendor substrate-tag inventory:** `agentic_orchestration/research/catalogue/cross-vendor-substrate-inventory-2026-05-XX.md` — the load-bearing synthesis output that elrond consumes.

## Cross-seam considerations

- **Gandalf:** screened the Tier-1 list at hand-off; available for in-flight ambiguity resolution (e.g., "this vendor's pack is on the boundary between substrate-distinct and substrate-redundant — which way?")
- **Elrond:** primary downstream consumer. Cross-vendor substrate-tag inventory is what feeds elrond's emergent-grouping analysis (commission to be authored after Step B completes per commission § "What knight-rider needs to do" item 3).
- **Knight-rider:** notify at each per-vendor crawl completion; flag any vendor surfacing a Dispatch-1-class new candidate (vendor catalogue inspection sometimes reveals adjacent vendors).
- **Star-lord + drax:** out of seam for this dispatch; no cross-seam ask.

## Required reading

- `agentic_orchestration/gandalf/requests/2026-05-16-step-b-tier1-2dvfx-crawl-commission.md` (this dispatch's source-of-truth; all binding criteria + methodology + scope)
- `agentic_orchestration/dispatches/2026-05-16-legolas-vendor-discovery-sweep.md` + its output (`research/knowledge/asset-catalogues/2026-05-16-vendor-discovery-sweep.md`) — your Tier-1 list comes from gandalf's screening of THAT output + the existing research base
- `agentic_orchestration/research/knowledge/asset-catalogues/2026-05-16-pixijs-compatible-2d-vfx-libraries.md` (existing research base — first half of the candidate pool)
- `agentic_orchestration/research/catalogue/pimen/full-2026-05-16.jsonl` (Pimen crawl precedent — schema reference)
- `canonical/story/form-bias-cadence-strategy.md` § 5.3 + § 6.1 + § 6.2 (cipher-width framework; why substrate-evidence quality matters)
- `canonical/story/style-register.md` § "Operational precision — deferred to Elrond's rubric design" (score-don't-filter principle; do NOT pre-filter by register at crawl time)
- `agentic_orchestration/AGENTS.md` § Legolas Mode B (crawl methodology)

## Acceptance criteria

- [ ] Knight-rider has flipped this dispatch's Status from HELD → PENDING — ACTIVE (gates closed; methodology validated; Tier-1 list finalized)
- [ ] Per-vendor metadata-only pre-pass conducted; substrate-distinct vs substrate-redundant flagged
- [ ] Substrate-distinct packs crawled exhaustively per `pimen` JSONL schema
- [ ] Substrate-redundant packs sampled 2-3 per redundant tag per vendor
- [ ] All three VFX-categories (skill / ambient / status) covered per scope
- [ ] Bundled characters flagged with `bundled_character: true` in pack metadata
- [ ] Kinetic-VFX coverage surfaced per Q5 (or absence noted with reasoning)
- [ ] Per-vendor JSONL files filed under `research/catalogue/<vendor-slug>/`
- [ ] Per-vendor findings summaries filed
- [ ] Cross-vendor substrate-tag inventory authored at `research/catalogue/cross-vendor-substrate-inventory-2026-05-XX.md`
- [ ] Knight-rider notified at completion; elrond's downstream emergent-grouping commission queued

## Out of scope (explicit)

- **Vendor screening or Tier-1 list authorship** — that's gandalf's job between Dispatch 1 and this dispatch's release
- **3D-rendered VFX vendors** (rejection criterion #1)
- **AI-content-default vendors** (rejection criterion #3)
- **Single-element specialists below substrate-novelty threshold** (rejection criterion #2)
- **Character-only vendors** — separate track per Q4
- **Architectural rename "physical → kinetic"** — Stage 4 of form-bias migration; not this dispatch
- **Foundation 4+1 expansion** — explicitly preserved through Step B; the rename + expansion decision lands at form-bias Stage 4
- **Pack purchasing / acquisition** — Matt-decision; this is research-only
- **Cipher-width determination** — Elrond's emergent-grouping analysis does that on YOUR output; this dispatch is substrate-evidence supply only

## Sequencing — how this dispatch fits

```
                                                          ┌─→ Dispatch 1 (legolas Mode A vendor-discovery sweep) ─┐
Form-bias-cadence-strategy locked (gandalf) ─→ Commission ─┤                                                       ├─→ Gandalf reviews + screens
                                                          └─→ Step A (Elrond methodology validation)  ─────────────┘
                                                                                                                              │
                                                                                                                              ▼
                                                                                                                          THIS DISPATCH fires
                                                                                                                              │
                                                                                                                              ▼
                                                                                                                          Cross-vendor inventory + per-vendor JSONLs delivered
                                                                                                                              │
                                                                                                                              ▼
                                                                                                                          Knight-rider authors elrond emergent-grouping analysis dispatch
                                                                                                                              │
                                                                                                                              ▼
                                                                                                                          Elrond runs emergent-grouping analysis at full substrate width
                                                                                                                              │
                                                                                                                              ▼
                                                                                                                          Cipher-width sub-lock resolves → form-bias strategy doc + decisions-log amendment
```

---

## Completion record

(To be filled in by legolas on completion — DO NOT FILL UNTIL DISPATCH IS UN-HELD AND ALL ACCEPTANCE CRITERIA MET)

**Completed:**
**Vendors crawled (final list):**
**Per-vendor JSONL paths:**
**Per-vendor findings-summary paths:**
**Cross-vendor inventory path:**
**Total packs surfaced:**
**Novel substrate tags surfaced (vs Pimen's 9 + canonical-four baseline):**
**Kinetic-VFX coverage assessment:**
**Notes for knight-rider:**
