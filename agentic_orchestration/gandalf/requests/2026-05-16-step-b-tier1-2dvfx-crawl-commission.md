# Request to knight-rider — Step B Tier-1 2D-VFX exhaustive crawl commission scaffolding

**From:** gandalf
**To:** knight-rider (to author the dispatches per ADR-002)
**Date:** 2026-05-16 (Day 4)
**Priority:** **Two dispatches.** (1) Vendor-discovery sweep — author NOW (runs in parallel with Step A; not blocking). (2) Step B Tier-1 exhaustive crawl — author NOW but HELD pending Step A methodology validation + vendor-discovery sweep completion. Both dispatches are Legolas Mode B work.
**Type:** Cross-seam commission scaffolding — Legolas crawl work, Elrond consumes downstream.

---

## Approval trail

Matt approved this commission's binding criteria + sequencing in Day-4 dialogue (2026-05-16). Specifically:

- **Sequencing:** Step A (Elrond methodology smoke test on Pimen substrate) → Step B (Legolas Tier-1 crawl) → Elrond emergent-grouping analysis at full width → cipher-width sub-lock resolves. Locked.
- **Q1 — vendor-discovery sweep before Step B:** Approved. Small Legolas commission, ~1 session, runs in parallel with Step A.
- **Q2 — per-vendor crawl depth = (b) substrate-distinct + sampled.** Approved. Metadata-only pre-pass identifies substrate-distinct packs per vendor; exhaustive on those; representative coverage on rest. Saves ~50% Legolas bandwidth vs full exhaustive depth.
- **Q3 — ambient + environmental + status-VFX:** All three included. Skill-effect + ambient + status all contribute to substrate-vocabulary evidence.
- **Q4 — bundled character/enemy assets:** Included free when bundled inside primary-VFX packs we're already crawling; standalone character-only vendors out-of-scope (separate follow-on character-track sub-commission per the gandalf-pimen-design-review).
- **Q5 — kinetic-VFX coverage:** Explicit inclusion clause. Non-element-coded skills/abilities (weapon-strikes, slashes, impact bursts, stagger/stun, knockback) need VFX. Vendors specializing in kinetic-VFX qualify regardless of elemental breadth. **Architectural rename "physical → kinetic" + per-embodiment narrative skin is DEFERRED to Stage 4 of the form-bias migration; not a Step B decision.** Foundation 4+1 stays operative through Step B unchanged.

---

## Strategic-axis context (load-bearing)

This commission lands under the form-bias-cadence-strategy doc's locked sub-positions (`canonical/story/form-bias-cadence-strategy.md` § 5.1):

- **Sub-lock (a):** ARPG-canon-primary at substrate-mechanical layer (preserved through Step B; no substrate addition disrupts the mechanical schema)
- **Sub-lock (b):** Isekai-canon-primary at narrative-skin and convergence layers (the substrate work feeds the cipher's grouping/vocabulary layers per § 6.1's three-layer model)

The four deferred catalogue-track sub-locks (cipher-width; Foundation layer placement; D1 reconsideration; per-season vocabulary coupling) resolve at named gates downstream of this commission. Step B is the catalogue-evidence supplier for the cipher-width decision specifically.

**Per § 6.2 of the strategy doc, three outcomes are possible from the emergent-grouping analysis at full substrate width:**
- 3-5 robust groupings emerge → multiple-groupings architecture viable; cross-season grouping variance becomes a structural pillar
- 1-2 groupings survive → refined-Option-A collapses to single fixed grouping
- No grouping survives → canonical-four cipher remains operative

Step B's substrate-width crawl determines the ceiling on which outcome can land. Bind the crawl-list carefully; the substrate-evidence quality determines the cipher-width decision quality.

---

## Dispatch 1 — Vendor-discovery sweep (NOW; ~1 Legolas session)

**Target:** Legolas (Mode A — analytical research).

**What it does:** Web-sweep for indie 2D pixel-art VFX vendors with distinct element vocabulary or kinetic-VFX coverage **not already in** `agentic_orchestration/research/knowledge/asset-catalogues/2026-05-16-pixijs-compatible-2d-vfx-libraries.md`.

**Expected yield:** 1-3 net-new vendor candidates. Closes the "did we miss the vendor with the missing substrate tag?" risk before committing Legolas to the broader Step B crawl.

**Sweep criteria for vendor inclusion in the candidate-discovery output:**

1. Active commercial source (Itch.io, Unity Asset Store, GameDevMarket, Gumroad, vendor's own site, etc.)
2. 2D pixel-art or hand-drawn-pixel register (not 3D-rendered; not shader-runtime)
3. Either (a) ships effects under a label distinct from Pimen's 9 (fire/water/earth/wind/ice/holy/dark/thunder/acid) + the standard canonical-four set OR (b) ships strong kinetic-VFX coverage (weapon-trails / slashes / impact / stagger / stun / knockback) regardless of elemental breadth
4. License clarity (paid or free, clear commercial terms; not abandoned-rights)
5. No-AI provenance OR documentable provenance

**Specific search vectors to surface candidates the existing research file may have missed:**

- Specialty necrotic-VFX / decay-VFX / poison-VFX vendors
- Specialty void-VFX / arcane-VFX / aether-VFX vendors
- Specialty psychic-VFX / mental-VFX / dream-VFX vendors (low likelihood; surface if found)
- Weapon-trail / slash-effect specialists (Fippe, Drinkscoffee tier indie creators)
- Stagger/stun/knockback/status visual specialists
- Indie creators on Bluesky / Mastodon / Twitter active in pixel-art-VFX community

**Output:** structured list, ~10-15 lines per candidate vendor: name, primary URL, distinctness signal (which substrate gap they fill), preliminary license assessment, recommendation for Step B inclusion.

**Out of scope:**
- 3D-rendered VFX vendors (architecture-incompatible)
- AI-content-default vendors (pitch-positioning risk per gandalf-pimen-design-review)
- Single-element specialists below substrate-novelty threshold (fire-only vendors when Pimen has fire covered)
- Character-only vendors (separate track per Q4)

**Acceptance:** Legolas files findings at `agentic_orchestration/research/knowledge/asset-catalogues/2026-05-16-vendor-discovery-sweep.md`. Gandalf reviews; merged candidates feed Dispatch 2's screened Tier-1 list.

---

## Dispatch 2 — Step B Tier-1 exhaustive crawl (HELD pending Step A + Dispatch 1)

**Target:** Legolas (Mode B — systematic catalogue crawl).

**Status:** Held pending two gates:
1. Step A methodology validation — Elrond's emergent-grouping smoke test on Pimen substrate must produce coherent groupings (not mush). If methodology fails, Step B doesn't run yet; the methodology rebuilds first.
2. Dispatch 1 vendor-discovery sweep — produces the final screened Tier-1 list.

**Estimated effort:** 2-4 Legolas Mode B sessions; depends on final vendor count.

### Binding criteria for Tier-1 list (locked from Day-4 dialogue)

**Inclusion (all three must hold for a vendor to enter the list):**

1. **Empirical-research-base eligibility.** Source appears in `2026-05-16-pixijs-compatible-2d-vfx-libraries.md` (existing research) OR in `2026-05-16-vendor-discovery-sweep.md` (Dispatch 1 output) as Pixi.js-compatible above quality floor.
2. **Substrate-variance contribution.** Source either (a) ships effects under at least one label distinct from Pimen's 9 + standard canonical-four, OR (b) ships across >7 distinct effect-type labels (multi-element breadth, even if labels overlap with Pimen), OR (c) ships strong kinetic-VFX coverage (weapon-trails / slashes / impact / stagger / stun / knockback) regardless of elemental breadth.
3. **License clarity.** Free or paid; commercial-licensing terms unambiguous; provenance documentable; no AI-content-default.

**Rejection (any one is disqualifying):**

1. **3D-render or runtime-shader sources.** Architecture-incompatible.
2. **Single-element specialist below substrate-novelty threshold.** Adds quantity-within-tag, not substrate variance. (Specialists shipping a *novel* substrate-tag — e.g., necrotic-only — qualify under inclusion #2a or #2c.)
3. **AI-generated content default.** Pitch-positioning risk.

### Expected Tier-1 candidates (subject to Dispatch 1 sweep additions)

From the existing research file, expected to survive screening:
- **Pimen** — baseline (already crawled; included as substrate reference)
- **ansimuz** — retro-band complementary; multi-element breadth
- **Brackeys VFX Bundle** — free baseline; impact/burst general-purpose
- **CraftPix** — vector + niche-mechanic; weapon-trail and slash-effect coverage
- **CreativeKind** — hand-drawn-pixel different sub-register
- **+1-3 from Dispatch 1 sweep**

Expected final list: **6-10 vendors total.**

### Per-vendor crawl methodology (locked: Q2 option b)

For each Tier-1 vendor:

1. **Metadata-only pre-pass** — Legolas inspects vendor's catalogue index pages; identifies substrate-distinct packs (packs surfacing a label not yet seen across previously-crawled Tier-1 vendors).
2. **Substrate-distinct packs: exhaustive crawl** — full Mode B treatment (one row per pack; full metadata extraction; canvas info; license terms; format flags).
3. **Substrate-redundant packs: representative sampling** — 2-3 packs per redundant substrate-tag per vendor; enough to confirm coverage breadth without full-catalogue depth.

**Rationale:** the substrate-variance question is answerable from substrate-distinct + sampled coverage. Full-exhaustive depth becomes useful at consumption time (purchase decisions), which is downstream of cipher-width lock. Saves ~50% Legolas bandwidth with no substrate-evidence loss.

### VFX-category scope (locked: Q3 all three included)

- **Skill-effect VFX** (Fireball, Ice Spike, etc.) — primary target; full crawl per methodology above.
- **Ambient / environmental VFX** (burning torches, flowing water, weather effects, ambient glow) — included; substrate-evidence contributor.
- **Status / impact / hit-spark / collision / force VFX** — included; combat-feel layer; kinetic-VFX evidence.

### Bundled-character handling (locked: Q4)

- **Bundled inside primary-VFX packs** (e.g., Pimen Earth Spell 03's Earth Elemental): included free; no extra crawl cost; flag in pack metadata as `bundled_character: true`.
- **Standalone character-only vendors**: out-of-scope. Separate follow-on character-track sub-commission per the gandalf-pimen-design-review's flag.

### Kinetic-VFX explicit inclusion clause (locked: Q5 practical)

The existing engine has skills/abilities that aren't element-coded and need VFX. Sword-strikes, weapon-trails, impact bursts, stagger/stun visuals, knockback effects. Pimen does not purpose-cover this (Hit Spark and Buff/Debuff are closest; neither is a true weapon-trail or slash pack).

**Step B explicitly seeks kinetic-VFX coverage.** Vendors specializing in kinetic-VFX qualify under inclusion #2c even with thin elemental breadth.

**Architectural rename ("physical → kinetic" + per-embodiment narrative skin) is NOT a Step B decision.** It lands at Stage 4 of the form-bias migration (display layer + per-embodiment skin work). Step B's job is substrate-evidence; the rename's job is player-facing-vocabulary downstream. Foundation 4+1 stays operative through Step B unchanged.

### Output format

Legolas Mode B output convention: one JSONL row per pack at `agentic_orchestration/research/catalogue/<vendor-slug>/full-2026-05-XX.jsonl`. Schema matches the Pimen full-crawl precedent (`pimen/full-2026-05-16.jsonl`).

**Per-vendor crawl deliverables:**
1. Full JSONL file (substrate-distinct exhaustive + representative-sampled).
2. Vendor summary findings doc at `agentic_orchestration/research/catalogue/<vendor-slug>/findings-summary-2026-05-XX.md` — substrate-evidence headline; novel substrate tags surfaced; license summary; consumption-readiness flags.

**Cross-vendor synthesis** (post-crawl): Elrond consumes the JSONL files + summary findings to run the emergent-grouping analysis at full substrate width. Cipher-width sub-lock resolves on that analysis's output.

### Acceptance criteria

- [ ] All Tier-1 vendors crawled per the per-vendor methodology
- [ ] Per-vendor JSONL files filed under `research/catalogue/<vendor-slug>/`
- [ ] Per-vendor findings summaries filed
- [ ] Cross-vendor substrate-tag inventory authored at `research/catalogue/cross-vendor-substrate-inventory-2026-05-XX.md` (Legolas; consumed by Elrond)
- [ ] Knight-rider notified at completion; Elrond's downstream emergent-grouping commission authored

---

## Cross-references

- **Strategic context:** `canonical/story/form-bias-cadence-strategy.md` § 5.3 + § 6.1 + § 6.2 (three-layer model; cipher-width framework; deferred sub-locks)
- **Parent commission:** `agentic_orchestration/gandalf/requests/2026-05-16-catalogue-mapping-and-grouping-experiment.md` (Step A methodology + experiment-1/2 framing)
- **Existing research base:** `agentic_orchestration/research/knowledge/asset-catalogues/2026-05-16-pixijs-compatible-2d-vfx-libraries.md`
- **Pimen sample precedent:** `agentic_orchestration/qa/findings/2026-05-16-gandalf-pimen-sample-design-review.md` (sets the substrate-evidence baseline)
- **Pimen full crawl precedent:** `agentic_orchestration/research/catalogue/pimen/full-2026-05-16.jsonl` (schema reference for Step B vendor JSONLs)
- **Score-don't-filter principle:** `agentic_orchestration/AGENTS.md` § Viability-gate workflow + `canonical/story/style-register.md` § "Operational precision — deferred to Elrond's rubric design"
- **AGENTS.md:** § Legolas Mode B (crawl methodology)

---

## What knight-rider needs to do

1. **Author Dispatch 1 (vendor-discovery sweep) NOW.** Standard Legolas Mode A dispatch shape; reference this commission for binding criteria. Runs in parallel with Step A. Notify gandalf at findings landing for screening review.
2. **Author Dispatch 2 (Step B Tier-1 crawl) NOW but mark HELD.** Standard Legolas Mode B dispatch shape; reference this commission for binding criteria, methodology, per-vendor scope. Held-pending-gates explicit in the dispatch header. Gates: (a) Step A methodology validation passes; (b) Dispatch 1 sweep findings land and gandalf review confirms the Tier-1 list.
3. **Sequence the Elrond downstream commission** as a future authored-after-Step-B item: emergent-grouping analysis at full substrate width. Not authored now; surfaces when Step B completion approaches.
4. **No decisions-log entry needed for the commission itself** — it operationalizes the already-locked form-bias-cadence-strategy decisions. If Step B's outcome surfaces a cipher-width lock, that's a future decisions-log entry per ADR-002.

---

— gandalf, 2026-05-16 (Day 4)
