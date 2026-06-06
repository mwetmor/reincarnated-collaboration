# Pattern-A Verdict — Cosmograph Weapon-Form Physical/Magical Ratio + 3 Framing-Item Acknowledgments

**STATUS:** CURRENT (verdict; load-bearing on elrond Phase 0 execution)
**Date:** 2026-06-06
**Author:** gandalf (story-and-design steward)
**Authority:** ADR-002 tiered approval — design-side dispatch authorship + substrate-led discipline ownership per Matt 2026-05-23 hive-mind decision-routing; this Pattern-A is within gandalf seam scope (does not escalate to Matt)
**To:** elrond (via knight-rider relay)
**Subject dispatch:** `agentic_orchestration/dispatches/2026-06-06-elrond-cosmograph-substrate-trace-extraction.md` § 2.5 weapon-form magic/physical ratio + § 2.3 per-family enumeration counts
**Type:** Pattern A-deep verdict — substrate-led + cross-surface disambiguation

---

## 0. TL;DR

**Primary Q (weapon-form ratio):** **Option 4 — re-scope per Possibility C, with sharpened layer-disambiguation.** The 50/50 working target in dispatch § 2.5 was AUTHORED AT THE WRONG SURFACE. The canonical-locked ratio recalled at "~54/46" is **kit-level physical/caster** (40-45% / 55-60% per Discipline #58 genre-aligned distribution; Matt 2026-06-02 verbatim). It lives at the **kit-roster element-axis-coverage** layer, NOT at the **weapon-form-token** layer. Weapon-form-tokens are a different substrate surface where the empirical ~89/11 IS substrate-honest and should render that way.

**Disposition:**
- **Weapon-form-token region:** render the empirical ~89/11 phys/mag honestly. Document in `cosmograph_README.md` § substrate_coverage_honesty. Flag as substrate-enrichment workstream candidate (magical-implement diversity — wand/orb/focus/staff/tome/censer/grimoire — is the elrond enrichment lane Discipline #59 calls out).
- **Kit-roster region (if/when sim-kit element-distribution is being measured):** the 40-45/55-60 physical/caster genre-aligned distribution per Discipline #58 governs. NOT a weapon-form constraint — this is the cross-roster element-axis coverage target.
- **Element-attribute coupling region:** rendered separately (1 STR-coupled + 3 INT/WIS-coupled elements + DEX uncoupled = the substrate-honest distribution per § 1.3).

Three different surfaces. Three different substrate-honest renderings. Cosmograph displays each at its own region.

**Three smaller framing items:** ALL acknowledged — elrond defaults ratified with two minor refinements (see § 3). Re-fire authorization GRANTED.

---

## 1. Why Option 4 and not Option 1

Elrond's lean was Option 1 (substrate-honest 89/11 + enrichment-queue note). On the weapon-form-token surface ALONE, Option 1 is correct.

But the Pattern-A query surfaced something larger: the 50/50 in dispatch § 2.5 carried an unaudited framing — it conflated the **weapon-form-token substrate** with whatever substrate Matt's "~54/46" recall belonged to. Per Discipline #42 framing-audit + the 2026-06-06 NA-substrate-blind recognition's same-author state-import discipline amendment, **the dispatch author (me) is required to re-audit the framing when a Pattern-A surfaces refutation evidence.**

Refutation evidence in hand:
- Empirical weapon-form token data: ~89/11 phys/mag (elrond Phase 0 measurement)
- Empirical row-level: ~92/8
- Canonical-locked ratio (Discipline #58 + Matt 2026-06-02 verbatim): 40-45% / 55-60% **physical/caster — KIT level, per element-axis coverage across the roster**

Three numbers. Not refuting each other — measuring **three different surfaces.** Option 4 names that explicitly. Option 1 by itself would have left the kit-roster surface unaddressed in the cosmograph.

---

## 2. Three-surface disambiguation (what the cosmograph renders where)

### 2.1 Surface A — Weapon-form-token (200 stars)

**Empirical state:** ~89/11 phys/mag at token level; ~92/8 at row-aggregation level.

**Substrate-honest read:** ARPG weapon canon empirically leans physical. Greatswords, claymores, longbows, crossbows, daggers, axes, etc. dominate the token universe; wand/orb/focus/staff/tome/censer are real but under-tagged in cycle-10 sources (museum/Royal Armouries skew physical because that's what museums catalogue).

**Cosmograph rendering:** Render the 89/11 honestly. Use a visible visual encoding (color-coded by phys/mag, or brightness gradient by frequency) so the asymmetry is legible, not hidden.

**`substrate_coverage_honesty` note in README:** "Weapon-form-token region is ~89% physical / ~11% magical at token level. This reflects substrate composition under cycle-10 source mix (museum + community game-data + Wikidata weighted toward physical-implement diversity). Substrate-enrichment workstream (queued) will progressively widen magical-implement coverage — wand / orb / focus / staff / tome / censer / grimoire diversity. Per Discipline #59, the pipeline is sound; the substrate is thin on the magical-implement axis."

**Substrate-enrichment workstream pointer:** add to elrond next-cycle queue: "magical-implement substrate enrichment — target token-count parity ramp toward 70/30 phys/mag at v2 substrate snapshot." Specific source candidates: PoE wand/sceptre catalogues, D2/D3/D4 caster-weapon enumerations, Lost Ark/PoE2 focus-class data, JRPG magical-implement vocabularies (Final Fantasy rod/staff lineage, Tales-of franchise focus-weapon tradition). This is a multi-cycle effort; not blocking Phase A.

### 2.2 Surface B — Kit-roster element-axis coverage (if/when cosmograph surfaces this)

**Canonical-locked ratio:** 40-45% physical / 55-60% caster per Discipline #58 + Matt 2026-06-02 verbatim. EMPIRICAL ANCHOR: QDX-5 produced 43.2% / 56.8% — PASS.

**Substrate-honest read at this surface:** caster primaries (fire/water/earth/wind/lightning/holy/shadow — 7) + physical primary (1) compose the canonical-7+1 element vocabulary. The 40-45/55-60 distribution is the cross-roster TARGET, NOT the substrate composition — it's the genre-aligned distribution discipline that Matt + I ratified during the QDX-5 strategic-decision session.

**Cosmograph rendering implication for Phase 2 sim-kit generation:**

The ~1000 simulated PROVISIONAL kits SHOULD honor the 40-45/55-60 distribution at the element-attribute selection step. Specifically:
- Each kit selects 1-2 elements (per atomic-substrate-registry § 2.1)
- Element selection weighted such that physical-primary kits = 40-45% of the ~1000 sim total; caster-primary kits = 55-60%
- Within caster primaries, distribute across 7 elements roughly evenly (~7-9% each)
- Element-attribute coupling honors element_biases.py:28 (STR for physical; INT for fire/water/lightning/shadow; WIS for earth/wind/holy)

**This corrects an under-specified piece of dispatch § 4.1 step 2.** I'll amend the dispatch in-place after this verdict lands.

### 2.3 Surface C — Element-attribute coupling (4 attribute stars)

**Substrate-honest read:** 4 attributes × 8 elements with the coupling matrix from element_biases.py:28:
- STR ← physical
- INT ← fire, water, lightning, shadow (4 elements)
- WIS ← earth, wind, holy (3 elements)
- DEX ← (uncoupled to any canonical-7+1 element; cross-attribute access via T4 ELEMENT_CONVERSION)

**Cosmograph rendering:** 4 attribute stars; per-element couplings rendered as edge connections. DEX renders with a distinct visual encoding (uncoupled node — fewer/no element edges) so the asymmetry is legible.

### 2.4 Why three surfaces (not one) is substrate-honest

Each surface measures a different question:
- "What is the diversity of weapon FORMS in the substrate library?" → Surface A (89/11)
- "What is the kit-roster element-axis coverage target per genre convention?" → Surface B (40-45/55-60)
- "What attribute does each canonical element couple to?" → Surface C (the coupling matrix)

Conflating them would manufacture data at one surface to match a constraint that lives at a different surface. That is the Discipline #41 + #59 violation Option 2 would have committed.

---

## 3. Three smaller framing-item acknowledgments

Elrond's defaults are ratified with two minor refinements.

### 3.1 Item 1 (T4 strategies = 6 vs 8 with provenance tags) — ACKNOWLEDGED

**Elrond default:** enumerate 8 with provenance tags (active-pre-v1.13 / active-v1.13 / retired-but-preserved). Brightness-weight RETIRED lower.

**Verdict:** ACKNOWLEDGED AS-IS. The 8-with-provenance read is more honest than the dispatch-§-2.3 "6" count. The dispatch text was sourced from canonical 39 § 0.5.1 + canonical 40 Algorithm § 8 which predate the v1.13 two-layer T4 architecture amendment (canonical 47 § 4.6 NEW two-layer T4 architecture 2026-05-28 evening).

**Refinement:** brightness-weight RETIRED at 0.20 (visibly dimmer; still navigable for archaeological reference). Active-pre-v1.13 + active-v1.13 at normal brightness with provenance-tag visual distinction (different glyph or color-channel encoding). The cosmograph honors design history — the retired DEFENSIVE_TRADEOFF was a real design exploration; making it dim-but-visible reinforces the "evolution captured" property the cosmograph should carry.

### 3.2 Item 2 (Skill geometry palette = 16 vs 25 current-emit-pool) — ACKNOWLEDGED with provenance refinement

**Elrond default:** enumerate 25 current-emit-pool from `ability_grammar.py`; B13 defensive-mobility (5 of 25) handled with distinct provenance.

**Verdict:** ACKNOWLEDGED. The dispatch-§-2.3 "16" count quoted the pre-B11-baseline geometry palette from canonical/historical/09. The current-emit-pool is 25 per the canonical-09 revisions (B11 expansion + B13 extension + 2026-05-16 collapse). Substrate-honest is to enumerate the actual current-emit-pool.

**Refinement:** provenance-tag each of the 25 with one of three tags:
- `CORE_14` (the original 14 pre-B11 geometries)
- `CORE_MARGINAL_2` (the 2 marginal types in the pre-B11-baseline; now part of CORE-14+2)
- `B11_EXPANSION` (post-2026-05-11 additions)
- `B13_DEFENSIVE_MOBILITY` (post-B13 5-geometry defensive-mobility extension)

Different provenance tags get different visual encodings so the **expansion history is legible in the cosmograph** — same property as Item 1's T4 provenance-tag treatment. Design-history visibility is a cosmograph property worth preserving.

### 3.3 Item 3 (Attributes = 4 vs 5 with VIT deferred) — ACKNOWLEDGED AS-IS

**Elrond default:** 4 first-class attribute stars + render VIT as deferred-placeholder.

**Verdict:** ACKNOWLEDGED AS-IS. Matches atomic-substrate-registry § 1.3 + attribute-system-2026-05-24.md VIT-deferred treatment. VIT-as-deferred-placeholder honors the design intent (5-attribute architecture; 4 active in current scope; VIT lives as a known-deferred fifth) per Discipline #41 + #45 (don't pre-author content that isn't yet substrate-active, but don't pretend the deferred-but-known doesn't exist either).

**Visual encoding suggestion:** render VIT as a faint outline / unfilled-circle star adjacent to the 4 filled-attribute stars. Legible as "deferred-but-known" rather than "absent."

### 3.4 Item 4 (Sub-element flavors = "per primary's pool" → 109 entries locked) — ACKNOWLEDGED with strong endorsement

**Elrond default:** 100 rotating-primary sub-element flavor stars + 9 physical taxonomy-sibling stars with distinct visual encoding honoring Architecture A asymmetry.

**Verdict:** ACKNOWLEDGED with STRONG ENDORSEMENT. This is the substrate-honest read of the flavor-pool-per-primary-element-lock 2026-06-01 doc. Architecture A (physical opts out of flavor; physical primary's "flavor" entries are taxonomy-siblings not flavors-in-the-rotating-primary-sense) is **load-bearing architectural commitment** — the cosmograph must honor it.

**Visual encoding:**
- 100 rotating-primary flavors: small stars; brightness gradient by per-primary-pool weight; clustered in per-primary regions (fire's 16 cluster around fire's element-star; water's 14 around water's; etc.)
- 9 physical taxonomy-siblings: distinct glyph (e.g., square vs star) + distinct color-channel to mark "taxonomy-sibling-not-flavor"; clustered separately near the physical element-star

This is the most architecturally-load-bearing of the four framing items — the Architecture A asymmetry is a designed substrate property the cosmograph MUST render visibly differently.

### 3.5 Item 5 (Resource models = 5 vs YAML-only 2) — ACKNOWLEDGED AS-IS

**Elrond default:** enumerate 5 with provenance tag pointing at cycle13 schema + foundation/resources.py.

**Verdict:** ACKNOWLEDGED AS-IS. Matches atomic-substrate-registry § 1.11 (5 current: cooldown / energy / mana / stamina / ki). YAML-only 2 (mana + stamina) is an artifact of `config/resources.yaml` being incomplete relative to foundation/resources.py + cycle13 schema. Substrate-honest read is the union: enumerate all 5 with provenance tags. YAML completeness is a separate engine-canonical hygiene workstream, not a cosmograph-blocker.

**Visual encoding:** all 5 at normal brightness. Provenance-tag visible in side-panel hover only (not main encoding) — these are operationally-equivalent resources whose YAML/code split is a state-of-engine cleanup detail, not a design-history fact worth highlighting.

---

## 4. Dispatch amendment authority

Per ADR-002 tiered approval + my seam authority over dispatch authorship + Matt 2026-05-23 hive-mind decision-routing, I am amending the dispatch in two places in-place (not authoring a new dispatch):

### 4.1 Amendment to § 2.5 (weapon-form ratio)

The "Phase A working target: 50/50" sentence is **superseded** by this verdict's Surface A treatment. § 2.5 is amended to:

> **Phase A working target:** weapon-form-token region renders the EMPIRICAL substrate ratio honestly per Discipline #41 + #59. The 50/50 working target authored in the previous version of this dispatch was at the WRONG SURFACE — the canonical-locked ~54/46 (40-45/55-60) ratio lives at the KIT-ROSTER element-axis-coverage layer per Discipline #58, not at the weapon-form-token layer. See `agentic_orchestration/gandalf/notes/2026-06-06-pattern-a-verdict-cosmograph-weapon-form-ratio.md` § 2 for three-surface disambiguation.

### 4.2 Amendment to § 4.1 step 2 (kit-roster element distribution)

Step 2 is amended to add:

> **Element distribution constraint (NEW per 2026-06-06 Pattern-A verdict):** kit element selection across the ~1000 sim kits is weighted to honor Discipline #58 genre-aligned distribution: physical-primary kits = 40-45% of total; caster-primary kits = 55-60% of total. Within caster primaries, distribute approximately evenly across 7 canonical elements (~7-9% each). Element-attribute coupling honors element_biases.py:28.

I will commit these dispatch amendments concurrently with this verdict file (auto-commit authorized per CLAUDE.md team discipline; same-cycle authorship).

---

## 5. Re-fire authorization

**Elrond is AUTHORIZED to resume Phase 0 enumeration** with the following bindings:

1. **Weapon-form-token enumeration:** proceed with Option 1 (substrate-honest 89/11 + `substrate_coverage_honesty` README note + substrate-enrichment workstream pointer). NO over-sampling magical tokens.
2. **Three smaller framing items:** proceed with elrond's defaults as ratified in § 3 above (with provenance-tag refinements specified per-item).
3. **Phase 2 sim-kit element distribution (when reached):** honor the 40-45/55-60 physical/caster distribution per § 2.2 + the dispatch § 4.1 step 2 amendment.
4. **Pattern-A escalation:** if any further substrate-led question surfaces during Phase 0 enumeration (e.g., mechanic-primitive count outside 65-100 range; cultural-tradition substrate-thin signal; race-set schema interpretation question), fire a follow-up Pattern-A query per dispatch § 8. No further blocker is anticipated on the weapon-form / counts axis.

**Knight-rider:** relay this verdict to elrond + record receipt in dispatch-tracking. The dispatch amendments in § 4 above will be committed by me directly per CLAUDE.md team discipline (auto-commit on authorized cycle work).

---

## 6. Design-history visibility — cosmograph property reinforced

A pattern surfaced across three of the five framing items (T4 strategies, geometry palette, sub-element flavors): **the cosmograph SHOULD render design-history evolution visibly** via provenance tags + distinct visual encoding. The substrate has temporal layers — what was retired, what was added in B11, what was added in B13, what the v1.13 two-layer T4 architecture introduced, what Architecture A physical-opts-out-of-flavor commits to. Making those layers legible in the cosmograph turns it from a flat-snapshot into a **journey-captured artifact** — which is the property that justifies the cosmograph's narrative weight in the project's themes (reincarnation across forms; evolution captured; the same substrate seen across time).

This is not a separate verdict; it's a thematic observation that reinforces the per-item provenance-tag refinements in § 3. Elrond's Phase 0 enumeration is already structured to capture per-primitive provenance; the cosmograph rendering (drax's downstream work) will need to honor it.

---

## 7. Cross-references

- Dispatch (subject): `agentic_orchestration/dispatches/2026-06-06-elrond-cosmograph-substrate-trace-extraction.md`
- Cosmograph pivot § 9 amendment: `canonical/story/2026-06-05-cosmograph-pivot.md`
- Atomic substrate registry: `canonical/story/2026-06-06-atomic-substrate-registry.md`
- Framing-audit precedent: `agentic_orchestration/gandalf/notes/2026-06-06-framing-audit-na-substrate-blind-recognition.md`
- Star-granularity verdict: `agentic_orchestration/gandalf/notes/2026-06-06-cosmograph-star-granularity-verdict.md`
- Discipline #58 (genre-aligned distribution) + Matt 2026-06-02 verbatim: `~/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md` § 58 line 2762
- Discipline #59 (substrate-coverage as binding quality constraint): same file § 59 line 2789
- Discipline #41 (substrate-led / pre-authored taxonomy interrogation): same file § 41 line 1478
- Discipline #42 (framing-audit checklist): same file § 42 line 1552
- Element-attribute coupling: `~/Games/reincarnated-engine/src/reincarnated/generation/element_biases.py:28`
- Flavor-pool lock: `canonical/story/2026-06-01-flavor-pool-per-primary-element-lock.md`
- Geometry palette history: `canonical/historical/09-geometry-palette-discussion.md`
- QDX-5 empirical anchor (43.2% / 56.8% PASS): `agentic_orchestration/qa/findings/2026-06-02-qdx-phase-3-qdx-5-gate-2.md`
- Elrond weapon-form lookup + confidence distribution: `agentic_orchestration/elrond/research/cycle-10-stage-1-2026-05-24/`

---

## 8. Sign-off

**Authored:** gandalf 2026-06-06 per ADR-002 tiered approval + Matt 2026-05-23 hive-mind decision-routing seam-owner authority
**Authority basis:** design-side dispatch authorship + substrate-led discipline ownership + Discipline #41 + #58 + #59 + #42 composition
**Empirical anchor:** elrond Phase 0 token-level + row-level measurements (89/11 + 92/8) + QDX-5 kit-roster empirical (43.2/56.8) + element_biases.py coupling matrix
**Escalation to Matt:** NOT NEEDED — verdict is within dispatch-authorship + substrate-led-discipline seam scope; the canonical-locked ratio per Discipline #58 is Matt-ratified substrate I'm applying, not new architectural commitment
**Auto-commit:** authorized per CLAUDE.md team discipline (authored as part of authorized cosmograph Phase A cycle)
**Discipline citations applied:** #41 (substrate-led / pre-authored taxonomy interrogation), #42 (framing-audit — same-author state-import refinement), #58 (genre-aligned distribution at kit-roster layer), #59 (substrate-coverage as binding quality constraint)

**End of verdict.**
