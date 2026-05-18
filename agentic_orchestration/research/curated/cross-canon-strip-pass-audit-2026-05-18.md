# Cross-Canon Strip Pass Audit — 2026-05-18

**Author:** jack-ryan (QA / design-principle guardian)
**Authority:** Dispatch `2026-05-18-jack-ryan-cross-canon-strip-pass-hybrid-mage.md` + gandalf § 8 cleanup list
**Method:** retain-with-annotation per gandalf § 8.6 pattern; enumeration-amend where live design statements existed
**Status:** COMPLETE — 14 docs amended (13 canonical/ + story/ docs + 1 created; canonical-17 confirmed clean)

---

## Annotation pattern used

Historical references received inline annotation:
> `*[hybrid_mage RETIRED 2026-05-18 per canonical-6 transition; this reference is historical record. See canonical/story/canonical-6-transition-retire-hybrid-mage-2026-05-18.md for context.]*`

Top-level blocks on D11 chain docs:
> `> *[RETIRED OUTCOME — hybrid_mage RETIRED 2026-05-18 per canonical-6 transition; this reference is historical record. ...]*`

Enumeration amendments replaced the archetype list directly and added a canonical-6 note.

---

## Per-doc amendments

### 1. canonical/09-geometry-palette-discussion.md
- **Amendment type:** Annotation (historical reference)
- **Location:** B11 palette expansion section — AOE coverage targets passage (line ~159)
- **Content:** "controllers 60-75% AOE, hybrid_mage 65-80%" — context retained; inline annotation added after the revision-2026-05-11 Status paragraph noting this is pre-canonical-6 context
- **Rationale:** B11 palette decisions are historical record; AOE coverage targets for canonical-6 roster governed by B6/B11 substrate-coherent archetype palette

### 2. canonical/17-gear-and-spirit-guide-design.md
- **Amendment type:** No amendment — CLEAN
- **Location:** Grepped for hybrid_mage; two "hybrid" occurrences are generic English usage (Shield class-fit lean "hybrid" = mixed orientation; "70/30 hybrid" loot awareness) — not the archetype_tag hybrid_mage
- **Rationale:** Per gandalf § 8.1 item 2 verify instruction — confirmed no `hybrid_mage` archetype-tag references

### 3. canonical/28-engine-arpg-rebalance-design.md
- **Amendment type:** Annotation (5 historical references)
- **Locations:**
  - Line ~349: B-series cross-chain rule "Multi-element classes (hybrid_mage, etc.)" — annotated inline
  - Line ~497: B11 AOE palette problem statement "hybrid_mage 65-80%" — annotated inline
  - Line ~868: B14.5 V1 adaptive quick-estimate "e.g., hybrid_mage near 0.054" — annotated inline
  - Line ~881: B14.5 V1 doppelganger modifier floor "hybrid_mage ~0.054" — annotated inline
  - Line ~1137: Kit size band "Complex archetypes (hybrid_mage, multi-element specialists): 14-15" — annotated inline with note that "complex 14-15" band no longer has a primary canonical-6 member
- **Rationale:** All five references are load-bearing B-series design history; retain per gandalf guidance

### 4. canonical/30-engine-explainer-current.md
- **Amendment type:** Enumeration-amend (STRIP + canonical-6 statement)
- **Location:** Line ~120 — archetype list "fire_mage, water_mage, earth_caster, wind_caster, hybrid_mage, fire_controller..."
- **Content:** Removed `hybrid_mage` from the enumeration list; added paragraph noting canonical-6 transition, that hybrid_mage was removed, and forward pointers
- **Rationale:** Live design statement — archetype enumeration must reflect canonical-6 roster

### 5. canonical/32-progression-design.md
- **Amendment type:** Annotation (2 live design rule references)
- **Locations:**
  - Line ~260: "Multi-element hybrid_mage → favor more chains" — annotated inline; noted this chain-count rule no longer applies post-canonical-6
  - Lines ~282-285: Cross-chain unlock rule table row "Multi-element (hybrid_mage, etc.)" + surrounding text — block annotation added after table noting multi-element row is historical record, cross-chain rule no longer applies to any actively-generated archetype, post-canonical-6 gear-secondary-element cross-chain rules are a future design decision
- **Rationale:** These were live design rules for hybrid_mage; the rules themselves are now historical record for the canonical-6 roster

### 6. canonical/33-progression-skeleton.md
- **Amendment type:** Annotation (inline)
- **Location:** Line ~237: "Complex archetypes (hybrid_mage, multi-element specialists): 14-15"
- **Content:** Inline annotation noting "complex 14-15" band no longer has a primary member in canonical-6; post-canonical-6 kit size distribution collapses to approachable (10-11) and standard (12-13) bands
- **Rationale:** Historical reference to a now-empty kit-size band; retain with clarification

### 7. canonical/16a-roadmap-shipped-log.md
- **Amendment type:** Annotation (historical shipped-log entry)
- **Location:** Line ~27: "B6 templates documented: 14 archetypes (4 mages + 4 controllers + hybrid_mage + hunter + 3 physical + rogue)"
- **Content:** Inline annotation noting shipped-log is historical record of B6 template state at documentation time; canonical roster has since transitioned to canonical-6 (13 archetypes)
- **Rationale:** Shipped-log is historical record; retain with transition pointer

### 8. canonical/story/d11-hybrid-mage-tuning-advisory-2026-05-17.md
- **Amendment type:** Top-level block annotation (RETIRED OUTCOME)
- **Location:** After doc title + before authority line
- **Content:** Block annotation: "RETIRED OUTCOME — hybrid_mage RETIRED 2026-05-18 per canonical-6 transition; this reference is historical record. The identity-preservation argument in this advisory is retracted; the RETIRE clause in the D11.2 advisory § 6 is activated."
- **Rationale:** The advisory advocated retaining hybrid_mage; that argument is retracted by canonical-6 outcome. Internal body references are covered by the top-level annotation.

### 9. canonical/story/d11-hybrid-mage-tuning-postmortem-2026-05-17.md
- **Amendment type:** Top-level block annotation (RETIRED OUTCOME)
- **Location:** After doc title + before authority line
- **Content:** Block annotation: "RETIRED OUTCOME — hybrid_mage RETIRED 2026-05-18 per canonical-6 transition; this reference is historical record."
- **Rationale:** Post-mortem is historical record of the D11.0 cycle

### 10. canonical/story/d11-postmortem-option-b-verdict-2026-05-17.md
- **Amendment type:** Top-level block annotation (RETIRED OUTCOME)
- **Location:** After doc title + before authority line
- **Content:** Block annotation: "RETIRED OUTCOME — hybrid_mage RETIRED 2026-05-18 per canonical-6 transition; this reference is historical record."
- **Rationale:** Option B verdict is historical record of the D11.1 authorization

### 11. canonical/story/d11-2-structural-redesign-advisory-2026-05-17.md
- **Amendment type:** Top-level block annotation (RETIRE clause activated)
- **Location:** After doc title + before author line
- **Content:** Block annotation: "RETIRE outcome triggered — RETIRE clause per § 6 of this advisory is ACTIVATED per Matt L3 verdict 2026-05-18. hybrid_mage RETIRED from canonical-7; canonical-6 transition complete. This advisory is historical record of the lever-shape work that preceded the retire verdict."
- **Rationale:** The D11.2 advisory itself contained the RETIRE clause; that clause is now active; the activation state should be clear at doc header

### 12. canonical/story/archetype-coupling-archaeology-2026-05-17.md
- **Amendment type:** Annotation (4 locations)
- **Locations:**
  - Line ~43: "1 hybrid_mage" in the 14-template list — inline annotation noting canonical roster is now 13 archetypes
  - Line ~69: `return "hybrid_mage"` in the classifier code snippet — inline code comment noting branch commented out in engine per rocket v1.17
  - Lines ~89-91: Coupling #3 stat allocator fallback — block annotation after fix-shape noting that post-canonical-6 the fallback target is a retired archetype; the fallback should become ValueError; flagged as non-urgent follow-up for a future dispatch; rocket retained hybrid_mage stats in _PHYSICAL_STAT_PROFILES with retirement comment
  - Line ~196: "Stat allocation fallback (Coupling #3) — falls to hybrid_mage stats" in top-3 convergence vectors — inline annotation cross-referencing the Coupling #3 block annotation
- **Rationale:** Coupling #3 is especially important: the fallback target archetype no longer exists in the canonical roster. The annotation surfaces a real engineering follow-up (ValueError on unrecognized archetype) per gandalf § 8.2 item 12 recommendation.

### 13. canonical/story/embodiment-narrative-layer.md
- **Amendment type:** Annotation (5 locations) + retention of naming-discipline note
- **Locations:**
  - Lines ~147/150: Function-tag table Sustain + Specialist rows — block annotation after table noting hybrid_mage references are historical record; post-canonical-6 mapping notes
  - Line ~156: Mapping notes "Hybrid_mage can land in multiple tags..." — inline annotation "historical record"
  - Line ~193: Energy tier table Baseline row — inline annotation "[RETIRED 2026-05-18]" on the hybrid_mage example
  - Lines ~202-204: "One conceptual clarification" section header + first paragraph — section header annotated with RETIRED block; paragraph reworded to past tense + "naming discipline remains active" to preserve the forward-pointing value
  - Line ~264: "hybrid_mage energy-tier ambiguity" in What-this-protects-against — inline annotation noting the naming discipline is retained for future archetype naming even though hybrid_mage itself is retired
- **Rationale:** Per gandalf § 8.2 item 13 — naming discipline (hybrid = element-mixing only) is retained as standing discipline for future archetype naming; hybrid_mage references in function-tag table and energy tier table are historical record

### 14. canonical/story/vs2a-vfx-scene-needs.md
- **Amendment type:** Enumeration-amend (strip hybrid mage row from coverage table) + annotation (2 locations)
- **Locations:**
  - Line ~205: VFX archetype coverage table "Hybrid mage | hybrid_mage | ..." row — row removed; replaced with a note block recording the removed row's content as historical record + VFX re-mapping guidance (beam_channel re-maps to controller archetypes)
  - Line ~236: Slot B "Applies to" — beam_channel mapping updated with inline annotation noting hybrid_mage is retired and beam_channel re-maps to controller archetypes
  - Line ~378: "beam_channel (hybrid_mage):" section header — annotated with RETIRED block; Slot A/B/C rendering pattern retained as it is geometry-driven and remains valid for any canonical-6 archetype using beam_channel
- **Rationale:** Per gandalf § 8.2 item 14 — VFX coverage table row stripped (live design statement); beam_channel VFX rendering pattern retained because it is geometry-driven, not archetype-specific; no orphaned VFX commission risk as beam_channel is available to controller archetypes

---

## Out-of-scope confirmed (not touched)

- Engine code: not modified (rocket v1.17 handles; scope honored)
- reincarnated-demo / reincarnated-loadout data: not modified (rocket backfill + drax filter handles)
- D11 advisory / postmortem / D11.2 advisory body content: not deleted (retained per pattern; top-level annotations cover)
- No re-litigation of RETIRE verdict
- No tag push (ADR-006)

---

## Engineering follow-up flagged (not blocking strip pass)

**Coupling #3 stat_allocator fallback (non-urgent, future dispatch):** rocket retained hybrid_mage stats in `_PHYSICAL_STAT_PROFILES` for Pattern P7 continuity with a retirement comment. However, `stat_allocator.allocate_stats()` fallback path should become `ValueError` on unrecognized archetype rather than silently returning a retired archetype's stats. Flagged at Coupling #3 annotation in archetype-coupling-archaeology. Recommend separate dispatch post-regen when Matt/knight-rider authorizes.

---

*Authored 2026-05-18 by jack-ryan. Deliverable 2 of 4 per dispatch.*
