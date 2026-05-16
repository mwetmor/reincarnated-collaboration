# Dispatch — 2026-05-16 — legolas — Vendor-discovery sweep (Mode A; Step B precursor)

**From:** knight-rider (authored per gandalf commission `agentic_orchestration/gandalf/requests/2026-05-16-step-b-tier1-2dvfx-crawl-commission.md`)
**To:** legolas
**Approved by:** Matt at 2026-05-16 Day 4 dialogue (commission Q1: "vendor-discovery sweep before Step B: approved")
**Status:** PENDING — ACTIVE
**Estimated effort:** 1 session Mode A web-sweep (~2-4 hours research; can run in parallel with the still-pending Elrond Step A methodology validation; not blocking)
**Acceptance:** Structured candidate-list document filed at `agentic_orchestration/research/knowledge/asset-catalogues/2026-05-16-vendor-discovery-sweep.md`. Findings handed to gandalf for screening review.

---

## Context — why this dispatch exists

Gandalf's commission for the Step B Tier-1 2D-VFX exhaustive crawl explicitly precondiitions a small Mode A vendor-discovery sweep BEFORE the heavier Step B Mode B crawl. Purpose:

> Closes the "did we miss the vendor with the missing substrate tag?" risk before committing Legolas to the broader Step B crawl.

The existing research base (`agentic_orchestration/research/knowledge/asset-catalogues/2026-05-16-pixijs-compatible-2d-vfx-libraries.md`) was contributed via external Claude conversation. It is solid as a starting point but pre-dates the form-bias-cadence-strategy's three-layer model + cipher-width framework. The sweep refreshes the candidate pool against the specific substrate-evidence questions the cipher-width sub-lock turns on.

**Expected yield:** 1–3 net-new vendor candidates. Low absolute count is the point — the sweep is risk-mitigation, not breadth-expansion.

This dispatch is Legolas Mode A (analytical research), NOT Mode B (systematic catalogue crawl). The Mode B Step B crawl is held separately at `dispatches/2026-05-16-legolas-step-b-tier1-2dvfx-crawl.md` pending two gates (see § "Sequencing" below).

## Strategic-axis context (load-bearing)

Per the form-bias-cadence-strategy doc § 5.1 + § 6.2:
- Sub-lock (a) ARPG-canon-primary at substrate-mechanical layer
- Sub-lock (b) Isekai-canon-primary at narrative-skin and convergence layers
- Three-layer model (substrate / grouping / vocabulary)
- Cipher-width sub-lock (Options A / B / C) resolves on full-substrate-width emergent-grouping analysis — and the analysis quality is bounded by the substrate-evidence quality this sweep + Step B together produce

**Bind the sweep carefully.** The vendor list feeding Step B determines the substrate ceiling for the cipher-width decision.

## Sweep inclusion criteria (all five must hold for a vendor to enter the candidate-discovery output)

Per commission Q1 + § Sweep criteria:

1. **Active commercial source** — Itch.io, Unity Asset Store, GameDevMarket, Gumroad, vendor's own site, etc. Abandoned-rights / dead-vendor catalogues do NOT qualify.
2. **2D pixel-art or hand-drawn-pixel register.** Not 3D-rendered. Not shader-runtime. Architecture-incompatible vendors are out-of-scope.
3. **One of the following substrate-novelty signals:**
   - (a) Ships effects under a label distinct from Pimen's 9 (fire / water / earth / wind / ice / holy / dark / thunder / acid) + the standard canonical-four set, OR
   - (b) Ships strong kinetic-VFX coverage (weapon-trails / slashes / impact / stagger / stun / knockback) regardless of elemental breadth
4. **License clarity.** Paid or free; commercial licensing terms unambiguous; provenance documentable. No AI-content-default vendors (pitch-positioning risk per `gandalf-pimen-sample-design-review.md`).
5. **No-AI provenance OR documentable provenance.** Vendors using AI-content as default workflow are out-of-scope.

## Specific search vectors

Per commission § Specific search vectors, prioritize finding candidates the existing research file may have missed:

- **Specialty necrotic-VFX / decay-VFX / poison-VFX vendors** — substrate tag the existing research file under-covers
- **Specialty void-VFX / arcane-VFX / aether-VFX vendors** — similarly under-covered
- **Specialty psychic-VFX / mental-VFX / dream-VFX vendors** — low likelihood; surface if found
- **Weapon-trail / slash-effect specialists** (Fippe, Drinkscoffee-tier indie creators; reference vendors in that quality + creator-shape band)
- **Stagger / stun / knockback / status visual specialists** — kinetic-VFX coverage per the explicit inclusion clause
- **Indie creators on Bluesky / Mastodon / Twitter active in pixel-art-VFX community** — surface-active creators may have catalogues not yet indexed by Itch.io aggregators

## Out-of-scope (do NOT include in candidate list)

- **3D-rendered VFX vendors** (architecture-incompatible)
- **AI-content-default vendors** (pitch-positioning risk per `agentic_orchestration/qa/findings/2026-05-16-gandalf-pimen-sample-design-review.md`)
- **Single-element specialists below substrate-novelty threshold** (fire-only vendors when Pimen has fire covered — adds quantity within a tag, not substrate variance)
- **Character-only vendors** (separate track per commission Q4 — follow-on character-track sub-commission)

## Output format

File at `agentic_orchestration/research/knowledge/asset-catalogues/2026-05-16-vendor-discovery-sweep.md`.

Per-candidate entry (~10–15 lines each):

```
### Vendor: <name>
- **Primary URL:** <vendor URL>
- **Distribution platform:** <itch.io / unity asset store / vendor site / etc.>
- **Distinctness signal:** <which substrate gap they fill — "ships necrotic-coded effects not in Pimen", "kinetic-VFX specialist with weapon-trail packs", etc.>
- **Element / mechanic coverage observed:** <inventory at the catalogue-page level; not pack-by-pack>
- **Register:** <pixel-art / hand-drawn-pixel / both / unclear>
- **Cost structure:** <paid / free / mixed; price range if observable>
- **License:** <commercial-royalty-free / CC-BY / CC0 / vendor-specific / unclear>
- **AI-content signals:** <none observed / AI-content-default / mixed / unclear>
- **Recommendation for Step B inclusion:** <yes / no / yes with caveat — explain in one sentence>
```

## Sequencing — how this dispatch fits

This dispatch (Dispatch 1 per the commission) runs **in parallel with Step A** (Elrond methodology smoke test — separate dispatch per the parent commission `agentic_orchestration/gandalf/requests/2026-05-16-catalogue-mapping-and-grouping-experiment.md`). Neither blocks the other.

**Both Dispatch 1 (this) AND Step A must complete** before Dispatch 2 (Step B exhaustive crawl, held at `dispatches/2026-05-16-legolas-step-b-tier1-2dvfx-crawl.md`) can fire. Sequencing:

```
Step A (Elrond)  ─┐
                  ├─→ Gandalf review → Dispatch 2 (Step B exhaustive crawl) fires
Dispatch 1 (you) ─┘
```

Notify gandalf when your findings land. Gandalf reviews the candidates against the binding inclusion criteria → finalizes the Tier-1 vendor list for Dispatch 2.

## Cross-seam considerations

- **Gandalf:** primary review-and-screening partner for this dispatch's output. Findings hand-off is the gate to Dispatch 2's Tier-1 list finalization.
- **Elrond:** downstream consumer. The final Tier-1 list (from Dispatch 2's crawl) becomes elrond's emergent-grouping analysis input. This dispatch produces no elrond-facing artifact directly.
- **Knight-rider:** notify at completion. Coordinates Dispatch 2 hold-release once both gates (Step A + this sweep) close.

## Required reading

- `agentic_orchestration/gandalf/requests/2026-05-16-step-b-tier1-2dvfx-crawl-commission.md` (this dispatch's source-of-truth)
- `agentic_orchestration/research/knowledge/asset-catalogues/2026-05-16-pixijs-compatible-2d-vfx-libraries.md` (the baseline you're augmenting — do NOT duplicate vendors already named there)
- `agentic_orchestration/qa/findings/2026-05-16-gandalf-pimen-sample-design-review.md` (AI-content pitch-positioning rationale)
- `canonical/story/form-bias-cadence-strategy.md` § 5.3 + § 6.1 + § 6.2 (strategic context; why substrate-variance matters for cipher-width)
- `canonical/story/style-register.md` § "Operational precision — deferred to Elrond's rubric design" (score-don't-filter principle)
- `agentic_orchestration/AGENTS.md` § Legolas Mode A (analytical-research methodology)

## Acceptance criteria

- [ ] Sweep performed against the 5 inclusion criteria + 6 search vectors
- [ ] Candidates filed at `agentic_orchestration/research/knowledge/asset-catalogues/2026-05-16-vendor-discovery-sweep.md` per the output-format template
- [ ] No duplicate vendors from the existing research base (cross-check against `2026-05-16-pixijs-compatible-2d-vfx-libraries.md`)
- [ ] Each candidate carries a Step-B-inclusion recommendation (yes / no / yes-with-caveat + one-sentence rationale)
- [ ] Knight-rider notified at completion; gandalf review handoff staged

## Out of scope (explicit)

- Mode B crawl on any candidate — that's Dispatch 2's territory; do not begin per-pack catalogue extraction here
- License-verification deep dive — surface what's observable from vendor-page metadata; full-license audit happens at Step B crawl time
- Recommending Tier-1-vs-Tier-2 split — present candidates flat; gandalf does the screening for Tier-1
- Character-only vendor evaluation (separate track per commission Q4)
- Pricing comparison / acquisition-cost analysis — out-of-scope (Matt-decision territory)

---

## Completion record

**Completed:** 2026-05-16
**Output path:** `agentic_orchestration/research/knowledge/asset-catalogues/2026-05-16-vendor-discovery-sweep.md`
**Candidates surfaced (count):** 4 net-new vendor candidates (Frostwindz full catalogue, Pixogen, Fellor, CodeManu)
**Substrate gaps addressed by candidates:** death/necrotic (Frostwindz Deathbringer), blood/life-drain (Frostwindz Blood Knight), void-as-distinct-label (Pixogen), cosmic/stellar (Frostwindz Starcaller), crystal/gem-arcane (Fellor), kinetic-impact depth 44 animations (CodeManu), technology VFX (Pixogen)
**Notes for knight-rider:** Frostwindz was in the existing research file as a single-pack lightning vendor; the sweep reveals a 13-pack catalogue spanning death, blood, cosmic, dark-arcane substrates — this is a material baseline gap. Pixogen's explicit "Void" label (distinct from Dark) is the strongest single substrate-novelty signal. Psychic/mental/dream and dedicated weapon-trail gaps remain unresolved — no specialist vendor found. Dispatch status: COMPLETE. Awaiting gandalf screening review before Dispatch 2 fires.
