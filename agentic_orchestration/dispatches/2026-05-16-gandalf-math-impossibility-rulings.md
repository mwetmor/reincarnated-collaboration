# Dispatch — 2026-05-16 — gandalf — Math-impossibility rulings on legolas Section 4 synthesis

**From:** knight-rider (authored per legolas pixel-scale research completion 2026-05-16; Section 4 flagged 3-4 mathematical-impossibility cases requiring design-track judgment)
**To:** gandalf
**Approved by:** Matt at 2026-05-16 Day 4 ("fire all three follow-ons")
**Status:** PENDING
**Mode:** Design-track analytical (gandalf-style canonical doc authoring)
**Estimated effort:** 1 session (~1-1.5h)

**Gate-1 bypass rationale:** Matt-directed, single-seam (gandalf-only), reversible (design-doc only; no code change), follows established gandalf canonical-doc authoring pattern. Per CHANGELOG rubric.

**Acceptance summary:** Rulings filed at `canonical/story/sprite-scale-math-impossibility-rulings-2026-05-16.md` (or analogous gandalf canonical path) on the 3-4 mathematical-impossibility cases legolas surfaced. Per case: ruling category (accept quality loss / swap monster / leave best-achievable / acquire alternate vendor pack); rationale anchored to Diablo + HD-2D genre framework + style register; recommendation feeds the per-slug scale-lookup table gandalf is authoring.

---

## Why this dispatch exists

Legolas pixel-scale research returned 2026-05-16 with Section 4 synthesis flagging mathematical-impossibility cases — where the intrinsic source-sheet pixel size makes the target tier-render ratio impossible without unacceptable quality loss.

You (gandalf) are authoring the per-slug scale lookup table that drax's eventual `MONSTER_SCALE_BY_SLUG` refactor consumes. The math-impossibility cases need explicit design rulings before that table can be finalized.

Three (plus one) cases from legolas Section 4:

1. **fire-elemental (192×68 source)** — Reaching elite tier floor (90 px) requires 1.5× upscale; tier midpoint (102 px) requires exactly 1.50×. **Strongest mathematical impossibility in monster set.** Flat-sideview aesthetic; character art may be considerably shorter than even 68 px.
2. **angel-guardian** — Reaching boss-tier midpoint requires 1.52× upscale.
3. **sword-warrior (280×280)** — Reaching trash-tier requires 4.3× **downscale**. Legolas note: 280×280 canvas likely contains substantial transparent padding (actual character art smaller); recommends gandalf inspect sprite before assigning trash-tier scale.
4. **god-of-lightning** — Single-frame static sheet flagged; animated content may not exist in current on-disk pack. Acquisition-completeness question rather than scale question.

## Cross-seam contract change?

**Round-trip: not applicable** — gandalf canonical doc output; no schema or contract change; no production code modified. Per R11(b) Principle 6.

## What this dispatch produces

A canonical ruling doc at: `canonical/story/sprite-scale-math-impossibility-rulings-2026-05-16.md` (final path your call; pattern-match to your existing canonical naming).

### Per-case structure

For each of the 4 cases, document:

**Case header:**
- Slug + tier + intrinsic source-sheet dimensions
- Target render px-height per legolas Section 4
- Required scale factor + quality-loss flag

**Ruling — pick ONE per case (or hybrid with explicit framing):**
- **(a) Accept quality loss** — render at the required scale, accept visible upscaling artifacts. Justify against style register + visual-legibility commitments. Note that HD-2D-shaped pixel-art tolerates some upscale better than other registers.
- **(b) Swap monster** — remove this monster from the VS2a 11-slot pool; replace with a CreativeKind alternate that fits the tier cleanly. Identify candidate replacement if known (drax's MONSTER_TRACK_INTEGRATION_NOTES.md flagged 19+ deferred packs; some may be candidates).
- **(c) Leave best-achievable** — render at the closest non-impossible scale (e.g., fire-elemental at 1.0× = 68 px = magic/trash boundary, not elite); accept tier-coherence violation; document the violation.
- **(d) Acquire alternate vendor pack** — request Matt authorize acquisition of a different vendor's version of this monster (e.g., a true elite-sized fire elemental from CraftPix or another vendor). Effort estimate + cost surface for Matt.

**Rationale (anchor to existing canonical):**
- Reference style-register.md (HD-2D-shaped pixel-art commitment)
- Reference enemy-visual-legibility.md (genre-tier hierarchy)
- Reference gandalf's Diablo size hierarchy + HD-2D register framework (Day 4 council response)
- Reference drax's MONSTER_TRACK_INTEGRATION_NOTES.md (deferred packs, P6.d sub-commission)

**Implication for per-slug lookup table:**
- Recommended scale factor for this slug
- Special-case note for drax MONSTER_SCALE_BY_SLUG refactor

### Cross-case synthesis section

Close the doc with a synthesis section addressing:

- Are these impossibilities driven by vendor-side intrinsic-size design choices (CreativeKind shipped specific px-counts that don't match Reincarnated's HD-2D register)?
- Does the pattern indicate the VS2a monster pool needs broader curation (move to (b) swap for multiple cases)?
- Should there be a forward Discipline / register rule for future vendor acquisitions (e.g., "minimum 96×96 frame for elite tier; minimum 160×160 for boss tier")?

### Sequencing note

This dispatch produces design RULINGS. The actual lookup-table assembly (per-slug scale factors for all 11 monsters + 10 chierit) is your existing in-flight authoring work consuming v0.20.2 monster composite + (when it returns) drax v0.20.3 chierit composite + legolas synthesis. The ruling doc is a PREREQUISITE input to that table, not a substitute for it.

## Out of scope (explicit)

- **NO direct refactor authoring.** drax MONSTER_SCALE_BY_SLUG refactor is a separate knight-rider-authored dispatch consuming your rulings + lookup table.
- **NO vendor acquisition execution.** Option (d) surfaces Matt-decisions on acquisition; Matt + knight-rider routes follow-on.
- **NO per-slug scale-factor table.** That's your existing in-flight authoring; this dispatch is the math-impossibility input.
- **NO HD-2D-register revision.** The 80-100 px target is your canonical anchor; this dispatch applies the anchor, doesn't redefine it.
- **NO commentary on legolas Section 1 / Section 2 raw data.** Those are clean empirical inputs; rulings address Section 4 flags only.

## Required reading

- Legolas pixel-scale research: `agentic_orchestration/research/knowledge/character-monster-pixel-scale-2026-05-16.md` — Section 4 synthesis flags
- Drax v0.20.2 monster composite notes: `agentic_orchestration/gandalf/findings/2026-05-16-monster-scale-inspection-strip-notes.md`
- Drax v0.20.2 surfaced 4 per-monster sizing concerns (sword-warrior tier-size inversion; evil-eye tiny; fire-elemental height-only-metric insufficient; demon-mage row_index missing) — overlap with legolas Section 4
- Your existing canonical: `canonical/story/style-register.md` + `canonical/story/enemy-visual-legibility.md`
- Drax MONSTER_TRACK_INTEGRATION_NOTES.md — deferred 19+ packs (option (b) candidates)

## Acceptance criteria

- [ ] Doc filed at gandalf canonical path (you pick exact path consistent with prior pattern)
- [ ] 4 cases addressed (fire-elemental / angel-guardian / sword-warrior / god-of-lightning), each with: ruling category + rationale + lookup-table implication
- [ ] Cross-case synthesis section addresses: vendor-side pattern? broader curation needed? forward register rule?
- [ ] Cross-references to legolas research + drax v0.20.2 notes + your prior canonical
- [ ] Knight-rider notified with: doc path, rulings summary (which cases got which category), any Matt-decision points surfaced (especially acquisition-authorization requests from option (d))

## Tag policy

- **No git tag** (gandalf canonical-doc persona convention)

---

## Completion record

**Completed:** _<date>_
**Doc path:** _<path>_
**Rulings summary:** _<fire-elemental: X / angel-guardian: X / sword-warrior: X / god-of-lightning: X>_
**Matt-decision points (especially option-d acquisition asks):** _<list>_
**Notes for knight-rider:**
