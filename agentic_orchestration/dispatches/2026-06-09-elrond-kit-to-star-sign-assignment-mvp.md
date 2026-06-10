# Elrond Commission — Kit-to-Star-Sign Assignment (MVP Scope: 3 Hand-Curated + Rest Random)

**STATUS:** ACTIVE (commission ready to fire)
**Date authored:** 2026-06-09
**Author:** gandalf (story-and-design steward)
**Authority:** Matt 2026-06-09 directive — "for kits to starsigns... for now, we only need 3 kits to map cleanly to starsigns. the rest will be random"
**Mode:** Elrond substrate-curation seam (schema extension + per-row assignment; no kit regeneration required)
**Audience:** elrond (primary executor), rocket (consultation if regeneration touch surfaces), gandalf (Phase 1 hand-curation authoring), Matt (preview review at Phase 2 close)
**Companion docs (read first):**
- `agentic_orchestration/legolas/research/2026-06-09-zodiac-substrate-corpus/synthesis.md` (423-entry zodiac corpus complete; the substrate this assignment draws from)
- `agentic_orchestration/legolas/research/2026-06-09-zodiac-substrate-corpus/corpus.yaml` (aggregated machine-readable 423-entry corpus)
- `canonical/story/2026-06-09-tal-rasha-glyphic-primitive-anchor-architecture-recognition.md` (Branch A; kit-binds-1:1-to-star-sign is the OTHER HALF of Branch A; this commission operationalizes the MVP scope)
- `agentic_orchestration/gandalf/notes/2026-06-02-qdx-5-top-5-character-curation.md` (gandalf-curated top-5 Featured Characters; candidate pool for the 3 hand-curated mappings)
- `canonical/story/2026-06-02-cycle-18-drax-amend-full-wave-close-record.md` (Duskweaver of the Eclipsed Meridian as canonical lead identity; T4 = Twilight Inversion Shell)
- `canonical/story/2026-06-06-atomic-substrate-registry.md` (canonical substrate registry where new `star_sign_id` field is added)

---

## 0. TL;DR

**Mission:** add `star_sign_id` field to kit corpus schema + populate via two-tier rule: 3 hand-curated kit-to-star-sign mappings (gandalf-authored per Phase 1) + rest random-assigned from 423-entry zodiac corpus (Phase 2).

**Scope discipline (Matt 2026-06-09):** MVP scope. Don't over-engineer. The 3 hand-curated kits are the narratively-load-bearing showcase mappings for vertical-slice spike + ongoing iteration; the rest of the corpus randomly populates the cosmograph for visual richness without per-kit narrative depth at this stage.

**Phases:**
- **Phase 1 — Gandalf hand-curates 3 mappings** (~45-60 min gandalf-only authoring; standalone artifact at `agentic_orchestration/gandalf/notes/2026-06-XX-3-kit-to-star-sign-canonical-mappings.md`)
- **Phase 2 — Elrond schema extension + assignment** (~30-60 min elrond seam work: add `star_sign_id` field; populate via hand-override script applying gandalf's 3 mappings + random assignment for the rest from 423-entry zodiac pool)

**Estimated wall-clock:** ~2-3 hours total across both phases; can fire in parallel to other workstreams.

**Critical constraint:** NO KIT REGENERATION REQUIRED. The kit corpus EXISTS at current state; this commission adds a metadata field and populates it. Rocket consultation only if elrond surfaces a regeneration-touch issue.

**Out of scope:** canonical semantic-mapping methodology for the full corpus (DEFERRED — full-corpus semantic mapping is Cycle 15+ territory; MVP is sufficient for vertical-slice spike + current iteration); kit-corpus regeneration (not required).

---

## 1. Why this scope is appropriate

**MVP discipline (Matt 2026-06-09):** The vertical-slice spike + ongoing player-surface iteration need kit-to-star-sign assignment ARCHITECTURE in place. They do NOT need full-corpus canonical semantic mapping at this stage. 3 hand-curated mappings give 3 narratively-rich showcase moments where kit identity + star-sign mythic narrative compose richly; the rest of the corpus randomly populates the visualization layer with kit-to-constellation visual binding (which is the architectural commitment per Branch A) without per-kit semantic depth.

**This is recognition-validate-commit at the methodology layer.** Full-corpus semantic-mapping is a substantial design call (methodology choice: semantic similarity / curated rule-table / hybrid; per-kit reasoning; rep-audit at semantic layer). It belongs to a later Pattern B with Matt when the cosmograph is empirically live + iteration has informed what semantic-match patterns actually work for player experience. The MVP scope unblocks downstream work (vertical-slice spike + UE port) without pre-committing methodology.

**Composition with Branch A:** Tal Rasha recognition record § 4 captured Branch A architectural-commitment. The kit-binds-1:1-to-star-sign architecture is the LOAD-BEARING half (alongside primitive-as-glyph). The MVP scope satisfies the architectural commitment minimally — kits HAVE star-sign assignments; the cosmograph CAN render kit-to-constellation visual binding; downstream work isn't blocked. Full-corpus semantic mapping fires when empirical validation surfaces the methodology requirements.

---

## 2. Phase 1 — Gandalf hand-curation (gandalf-only authoring)

**Authored by gandalf** at `agentic_orchestration/gandalf/notes/2026-06-XX-3-kit-to-star-sign-canonical-mappings.md` (date per actual completion).

### 2.1 The 3 kits — REFERENCED TO VIDEO WORK (Matt 2026-06-09 directive)

Per Matt 2026-06-09 verbatim: "we will just need to find those 3 in the video."

**The 3 hand-curated kits are NOT arbitrarily picked from top-5 — they are the 3 kits FEATURED IN MM-P1 video work.** This preserves narrative coherence across video + cosmograph + canonical lore: a player who sees the video, then enters the cosmograph, finds the same 3 kits as canonical anchor mappings; cross-surface consistency reinforces the lead identity narrative.

**Phase 1 prerequisite — identify the 3 video-featured kits:**

Candidate video references (gandalf identifies actual reference at execution; Matt confirms if ambiguous):
- `Generated Video June 02, 2026 - 9_56PM.mp4` (meta-repo root; untracked)
- `duskweaver-mm-p1/` (directory; MM-P1 video production work)
- Any other Matt-directed video reference

**Top-1 mandatory inclusion: Duskweaver of the Eclipsed Meridian.** Duskweaver is the canonical lead identity per cycle-18 work + likely featured as the lead in MM-P1 video work. If the video features additional kits beyond Duskweaver, those are the 2 + 3 mappings. If the video features only Duskweaver, the 2 + 3 selections fall back to gandalf-discretion within top-5 candidate pool (per `agentic_orchestration/gandalf/notes/2026-06-02-qdx-5-top-5-character-curation.md`) — but surface this to Matt at Phase 1 close for direction.

**Identification method:** gandalf consults the video work directly OR Matt-provides the kit list. Gandalf does NOT have native video-viewing capability — surface to Matt at Phase 1 start: "which 3 kits are featured in the MM-P1 video?" if Matt has explicit knowledge; OR review video metadata / shot list / accompanying notes within `duskweaver-mm-p1/` directory; OR Matt watches video together with gandalf relay.

**Kit identity criteria (preserved):**
- Strong kit identity (T4 selection + faction + element + flavor cohesion lands cleanly)
- Mythic narrative depth available for the matched star-sign (cross-tradition richness preferred — Pleiades / Sirius / Polaris / Antares / Orion-region offer 6-11 traditions of mythic narrative per Legolas synthesis)
- Cross-element representation across the 3 kits (avoid all-3 being the same element; surface architectural breadth)

### 2.2 Per-mapping documentation required

For each of the 3 mappings, document:
- **Kit identity** (kit_id from current 37-kit corpus + 1000-kit substrate-trace; kit name; element; T4 selection; faction; flavor identity)
- **Star-sign identity** (star_sign_id from Legolas corpus; sign name + cultural tradition; mythic narrative summary)
- **Semantic-match reasoning** (why THIS kit maps to THIS star-sign; element correspondence + mythic-archetype correspondence + cultural-register fit + narrative resonance)
- **Cross-tradition note (if applicable)** — if the matched star-sign appears in multiple traditions (Pleiades / Sirius / etc.), note the trans-cultural richness

### 2.3 Output

Standalone gandalf-authored doc at `agentic_orchestration/gandalf/notes/2026-06-XX-3-kit-to-star-sign-canonical-mappings.md` (~45-60 min gandalf authoring). Commits to meta-repo per CLAUDE.md addendum.

---

## 3. Phase 2 — Elrond schema extension + assignment

**Executed by elrond** at substrate-curation seam (with rocket consultation only if regeneration-touch surfaces; not expected for this MVP).

### 3.1 Schema extension

Add `star_sign_id` field to kit corpus schema:

```yaml
kit:
  # ... existing fields ...
  star_sign_id: string  # FK reference to Legolas zodiac corpus sign_name primary; nullable until populated
  star_sign_assignment_method: enum  # values: HAND_CURATED | RANDOM
  star_sign_tradition: string  # denormalized — cultural_tradition.primary_culture from corpus (for downstream filtering / display)
```

**Where the field lives:** elrond seam discretion on schema-extension target — likely the substrate-trace data layer that drax /forge consumes; possibly also engine-side kit corpus schema if rocket consultation surfaces engine-side need.

**MIGRATION.md entry per ADR-006:** elrond authors per cross-seam contract; rocket reviews if engine-side touch confirmed.

### 3.2 Hand-override application

Apply gandalf Phase 1 hand-curated 3 mappings as overrides:
- Read Phase 1 output doc
- Apply 3 specific kit_id → star_sign_id assignments
- Set `star_sign_assignment_method: HAND_CURATED` for these 3 entries

### 3.3 Random assignment for the rest

For all OTHER kits in the corpus:
- Random-assign star_sign_id from the 423-entry Legolas zodiac corpus pool
- Set `star_sign_assignment_method: RANDOM` for these entries
- Random seed: deterministic seed (e.g., kit_id hash + fixed salt) for reproducibility; document seed in implementation script

**Constraint on random assignment:** uniform random across the 423-entry pool. Do NOT pre-weight by cultural-tradition / element / etc. — random IS random for this MVP. Substrate-led discipline preserved: future semantic-mapping methodology (Cycle 15+ Pattern B) replaces random for kits where canonical mapping is warranted.

### 3.4 Cultural-sensitivity audit (substrate-tagging discipline per Discipline #25)

Before populating, audit Legolas corpus entries for `cultural_sensitivity.flag_level`:
- **`none` and `low`:** eligible for random assignment
- **`medium`:** eligible for random assignment (default include)
- **`high`:** SUBJECT TO REVIEW — surface to gandalf for include/exclude decision before random pool inclusion
- **`restricted`:** EXCLUDE from random pool (substrate-cleanliness > volume per Legolas commission protocol)

Operationally: elrond filters the 423-entry pool down to the eligible subset (likely ~400 entries after restricted exclusion + high-sensitivity review). Random assignment draws from the filtered pool.

### 3.5 Output

- Schema extension committed in appropriate substrate-curation file (elrond seam discretion on file location)
- Random-assignment script committed at `agentic_orchestration/elrond/scripts/kit-to-star-sign-mvp-assignment.py` (or similar)
- Populated assignment data committed at appropriate substrate file
- Phase 2 close report at `agentic_orchestration/elrond/notes/2026-06-XX-kit-to-star-sign-mvp-assignment-close.md` summarizing:
  - 3 hand-curated mappings applied
  - N random-assigned entries (likely ~37 kits in current corpus minus 3 hand = ~34 random; or 1000 in substrate-trace minus 3 = ~997 random — depending on which corpus layer elrond operates on)
  - Cultural-sensitivity audit outcome (X entries excluded; Y entries flagged for gandalf review)
  - Schema migration notes
  - Cross-seam handoff readiness (drax /forge consumes via existing pipeline; UE port WS1 absorbs via DataTable ingestion)

---

## 4. Acceptance criteria

| # | Criterion | How validated |
|---|---|---|
| 1 | `star_sign_id` field added to kit corpus schema | Code review of schema-extension commit |
| 2 | 3 hand-curated mappings applied per gandalf Phase 1 doc | Manual verification: 3 specific kits have HAND_CURATED assignment_method + correct star_sign_id |
| 3 | Rest of kits have RANDOM assignment_method + star_sign_id from filtered 423-entry pool | Spot-check N random kits |
| 4 | Cultural-sensitivity audit applied (restricted excluded; high reviewed) | Phase 2 close report documents audit outcome |
| 5 | Random seed is deterministic (reproducible assignment) | Re-running script produces identical assignments |
| 6 | `star_sign_tradition` denormalized field populated for downstream filtering | Spot-check: tradition field matches Legolas corpus cultural_tradition.primary_culture |
| 7 | MIGRATION.md entry written per ADR-006 (cross-seam contract) | Code review of MIGRATION.md commit |
| 8 | No kit regeneration triggered (MVP scope discipline) | No rocket-seam regeneration commits |
| 9 | Drax /forge can consume kit corpus with star_sign_id field (no /forge breakage) | Vercel preview deploys cleanly post-Phase-2 |
| 10 | Phase 2 close report at elrond notes path | Doc exists with required sections per § 3.5 |

---

## 4.5 Quality criterion

**Game-quality goal this dispatch serves:** The vertical-slice spike + ongoing /forge iteration have a working kit-to-star-sign architecture in place — 3 hand-curated showcase mappings give 3 narratively-rich kit-to-constellation moments where mythic narrative composes with kit identity (Duskweaver mapped to a star-sign whose mythic narrative resonates with shadow/twilight/inversion themes carries player-experience weight); the rest of the corpus populates the cosmograph visualization layer without per-kit narrative depth (acceptable for MVP scope — visual richness without semantic over-commitment). The architecture works; the semantic mapping iterates over time. Absent this MVP, downstream work either blocks on full-corpus methodology design (over-engineering for current stage) OR proceeds without the kit-to-star-sign architectural commitment (Branch A half-implemented; cosmograph cannot render kits-as-constellations).

**Refutation conditions** (sub-agent surfaces if any apply):
- This dispatch contradicts canonical anchor X (Tal Rasha glyphic primitive-anchor architecture recognition 2026-06-09 — Branch A; Earth-Avatar Creation Moment Architecture 2026-06-07; Legolas zodiac-substrate-corpus 2026-06-09)
- Alternative execution Y serves the named quality goal better (e.g., 5 hand-curated kits instead of 3; canonical semantic mapping for full corpus before any assignment; random assignment without hand-curated overrides at all)
- Acceptance criteria can pass without advancing the quality goal (e.g., schema extension lands + 3 mappings applied + random assignment works, yet the 3 hand-curated mappings are semantically weak — fail to advance the showcase-moment quality goal)
- Dispatch framing pre-commits to a decision Matt has not ratified (specific 3 kit selections — DEFERRED to gandalf Phase 1 authoring; specific star-sign choices — DEFERRED to gandalf semantic-match work)
- Dispatch introduces a pre-authored taxonomy without justification (#41 candidate — assignment_method enum values; gandalf cultural-sensitivity review threshold)
- Dispatch introduces a scaffold value not flagged as pending-decision (#40 candidate — random seed methodology; cultural-sensitivity exclusion threshold)

---

## 5. Discipline citations

### 5.1 Discipline #25 (semantic-layer rep-audit)
Phase 1 gandalf hand-curation IS semantic-layer rep-audit at per-kit layer for 3 mappings. Phase 2 cultural-sensitivity audit IS rep-audit at the corpus pool layer. Both layers preserve substrate-led discipline.

### 5.2 Discipline #40 (scaffold-with-pending-decision)
Multiple scaffolds in this MVP:
- 3-kit count (MVP scope; expand later per empirical validation)
- Random assignment for the rest (Cycle 15+ Pattern B replaces with canonical semantic mapping)
- Cultural-sensitivity exclusion threshold (high reviewed; restricted excluded)
- Random seed methodology (deterministic for MVP; revisit if reproducibility-vs-fresh-randomization trade matters)
All flagged in Phase 2 close report.

### 5.3 Discipline #41 (pre-authored taxonomy interrogation)
The 3-kit selection is NOT canonically pre-imposed; gandalf curates per substrate-evidence (top-5 + semantic richness against 423-entry corpus). The "random for the rest" approach is deliberate substrate-honesty — random IS the right MVP because full-corpus methodology isn't ready; pre-imposing weighted random would over-commit before substrate-led methodology fires.

### 5.4 ADR-006 (read-only-default external-systems rule)
This commission is SUBSTRATE-INTERNAL — modifies kit corpus + Legolas corpus consumption; no external-system writes. MIGRATION.md per cross-seam contract.

### 5.5 Recognition-validate-commit (gandalf OP § 3.4 + 4.1)
MVP scope IS the validate-now-commit-later application — Branch A architectural commitment is validated by having the assignment architecture in place; full-corpus canonical mapping commits later when empirical iteration informs methodology.

### 5.6 No-regeneration discipline (Discipline #11 attribution + Discipline #20 density-based row-duplication adjacent)
No kit regeneration. Existing kit corpus + substrate-trace gain metadata field via additive operation; existing kits unchanged at their other fields. Preserves all upstream work + telemetry attribution.

---

## 6. What this commission does NOT include

- ❌ Full-corpus canonical semantic mapping (Cycle 15+ Pattern B territory)
- ❌ Kit-corpus regeneration (additive field only)
- ❌ Methodology lock for semantic-similarity / curated rule-table / hybrid approach (DEFERRED to future Pattern B)
- ❌ Visual rendering of kits-as-constellations at /forge or UE (downstream drax / mantis consumption work; separate dispatches)
- ❌ Star-sign-to-kit reverse-mapping (per-star-sign list of all assigned kits — out of scope; can be derived at query time from forward mapping)
- ❌ Per-tradition seasonal-rotation operator integration (atomic-substrate-registry Layer 0.5 seasonal-substrate-rotation composition is downstream design work; not MVP)
- ❌ Cross-cycle / scope-amendment commits without Matt-authorization (per CLAUDE.md addendum)

---

## 7. Composition with prior work

| Prior work | Composition |
|---|---|
| Legolas zodiac-substrate-corpus 2026-06-09 (N=423) | THIS commission consumes the corpus as the random-assignment pool + gandalf semantic-search target |
| Tal Rasha glyphic primitive-anchor architecture recognition 2026-06-09 | Branch A architectural commitment; this commission operationalizes the kit-binds-1:1 half (the other half — primitive-as-rune-per-group — is Phase 4 amended) |
| Earth-Avatar Creation Moment Architecture 2026-06-07 | Vertical-slice spike requires kit-to-constellation architecture; THIS commission unblocks |
| `2026-06-02-qdx-5-top-5-character-curation.md` | Candidate pool for the 3 hand-curated mappings |
| Duskweaver of the Eclipsed Meridian (cycle-18 canonical lead) | Mandatory inclusion in Phase 1 3-kit set |
| Drax /forge Phase 4 amended (in flight) | Phase 4 amended renders rune-per-group at primitive layer; THIS commission populates kit layer for downstream Phase 5 (or amendment) kit-as-constellation rendering |
| Mantis UE port WS1 (downstream) | Absorbs star_sign_id field via DataTable ingestion |
| Cultural-sensitivity protocol (Legolas commission § 4.2) | Inherited at substrate consumption per § 3.4 |

---

## 8. Deliverables

### Phase 1 (gandalf)
- Standalone hand-curation doc at `agentic_orchestration/gandalf/notes/2026-06-XX-3-kit-to-star-sign-canonical-mappings.md` (3 mappings + per-mapping reasoning + Duskweaver mandatory inclusion)
- Auto-commit per CLAUDE.md addendum

### Phase 2 (elrond)
- Schema extension commit
- MIGRATION.md entry
- Random-assignment script + populated assignment data
- Phase 2 close report at `agentic_orchestration/elrond/notes/2026-06-XX-kit-to-star-sign-mvp-assignment-close.md`
- Auto-commit per CLAUDE.md addendum
- Cross-seam handoff signal to drax (/forge can consume) + future mantis (WS1 DataTable ingestion)

---

## 9. Sign-off

**Authored:** gandalf 2026-06-09 per Matt 2026-06-09 directive — "for kits to starsigns... for now, we only need 3 kits to map cleanly to starsigns. the rest will be random".

**Authority:** gandalf cross-cutting design-steward commission authority for kit-to-star-sign architectural commitment + composition with Tal Rasha recognition record § 4 Branch A operationalization (the kit-binds-1:1 half; primitive-as-rune-per-group half is Phase 4 amended) + Earth-Avatar Creation Moment Architecture vertical-slice preparation.

**Routing:** Phase 1 fires gandalf-seam (gandalf hand-curates 3 mappings; standalone doc). Phase 2 fires elrond-seam (schema + assignment script + populate). KR sequences Phase 1 → Phase 2 (Phase 2 consumes Phase 1 output); both can fire in parallel to other in-flight workstreams (Phase 4 amended, Mantis Session 3, etc.). Phase 2 close report routes to gandalf for design review + Matt for awareness.

**Empirical-evidence triggers:**
- Phase 2 close → drax /forge unblocked for kit-as-constellation rendering work (separate Phase 5 or amendment dispatch)
- Phase 2 close → mantis UE port WS1 commission scope absorbs `star_sign_id` ingestion
- Full-corpus canonical semantic mapping → Cycle 15+ Pattern B with Matt when vertical-slice spike playtest informs methodology requirements

**Composition with prior canonical commitments:** all preserved (Tal Rasha 2026-06-09 + Earth-Avatar Creation Moment Architecture 2026-06-07 + Legolas zodiac-substrate-corpus 2026-06-09 + atomic-substrate-registry 2026-06-06 + cosmograph-pivot 2026-06-05 + Duskweaver identity from cycle-18).

**End of commission.**
