# Dispatch — 2026-05-27 — legolas — Cycle 14 SC-5 Mode A damage scaling pattern research

**From:** knight-rider
**To:** legolas (research + catalogue-crawl seam)
**Approved by:** Matt 2026-05-27 (framing brief Q5 ratified — sidecar list confirmed including SC-5)
**Estimated effort:** ~8-12 hours Mode A analytical research
**Acceptance:** research artifact filed at `agentic_orchestration/research/2026-05-27-cycle-14-sc-5-damage-scaling-patterns.md` cataloguing physical / magical / hybrid scaling formulas across ARPGs with structural recommendations for Reincarnated Wave 0.5 implementation

## Context

Cycle 14 Wave 0.5 implements doc 47 damage scaling architecture (physical / magical / hybrid routing). Doc 47 § 4 specifies the three formulas:

- **Physical**: `weapon_base_physical_damage × skill_damage_multiplier × (1 + STR/DEX_bonus/100) × (1 + global_physical_modifier/100) × tier_coefficient × element_conversion (if T4) × crit_multiplier`
- **Magical**: `base_spell_damage × skill_damage_multiplier × (1 + INT/WIS_bonus/100) × element_affinity × (1 + weapon_spell_modifier/100) × tier_coefficient`
- **Hybrid**: per-skill design; cross-attribute ω-penalty per Option C substrate composition policy

Matt verbatim that surfaced the architecture: "I get that physical skills might want to scale weapon damage, but magical skills? Why would ice spike have anything to do with wooden staff physical damage?" The architectural distinction (weapon is damage source for physical; spell is damage source for magical; weapon modifies HOW via +%spell damage / element affinity / to-skill-level) requires implementation-time confirmation against community-canonical ARPG patterns.

This sidecar gates Wave 0.5 (per framing brief § 5 SC-5 entry: "Wave 0.5 gate"). Legolas Mode A research from ARPG community-canonical damage-formula catalogues informs gamora's damage_resolver implementation + rocket's per-skill `damage_scaling_type` + `scaling_attribute` field schema implementation.

Doc 47 surfaces what was implicit in skill-system-2026-05-24.md (composition pattern = element × geometry × tempo × amplitude × tier_coefficient; **weapon base damage absent from composition**) and weapon-substrate-composition-policy-v1-2026-05-24.md (Option α martial / Option β caster / Option C cross-attribute). This research grounds the formulas against community-canonical genre patterns.

## Required reading before starting

- `canonical/00-ground-state.md` — ground-state oracle
- `canonical/47-damage-scaling-architecture-2026-05-27.md` — particularly § 1.2 genre canon table + § 2 (three scaling types) + § 4 (formulas) + § 5 (doc 40 amendments) + § 6 (Discipline candidate #38)
- `canonical/story/skill-system-2026-05-24.md` — skill composition pattern that doc 47 surfaces the implicit damage-scaling-path of
- `canonical/story/weapon-substrate-composition-policy-v1-2026-05-24.md` — Option α / β / C cell-type matching
- `canonical/story/attribute-system-2026-05-24.md` — 4-attribute system (STR / INT / WIS / DEX)
- `canonical/46-concentration-architecture-2026-05-27.md` § 2 (Layer 1 stat-range bounds) — formulas must respect bounds
- `canonical/41-progression-framework-2026-05-27.md` § 4 #1 (per-level scaling formulas deferred; Cycle 14 v1 uses L50 cap baseline only)
- `agentic_orchestration/gandalf/notes/2026-05-27-cycle-14-framing-brief.md` § 2 Wave 0.5 + § 3.4 (damage scaling routing impl) + § 5 SC-5
- `~/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md`
- `.claude/skills/reincarnated-legolas-operating-procedure` — Mode A protocol

## Math-before-code

This is methodology consultation per Discipline #18 at a math hotspot — damage-formula architecture is load-bearing for Wave 0.5 implementation. Output should make explicit formula structural recommendations + edge-case enumeration.

## Cross-seam contract change?

**NO** — research output, no code emission. Round-trip not applicable. (Cross-seam impact lands at Wave 0.5 when gamora implements damage_resolver + rocket emits per-skill `damage_scaling_type` field.)

## Scope

- [ ] Survey 7+ ARPGs (D2 LoD / D3 / D4 / PoE / Last Epoch / Grim Dawn / Lost Ark; add Wolcen / Diablo Immortal / Path of Exile 2 if accessible) for damage scaling formula documentation
- [ ] Map each game's physical formula + magical formula + hybrid handling to doc 47's three-path architecture
- [ ] Identify edge cases (per § 7 below)
- [ ] Surface community-canonical genre patterns that validate or refute doc 47's structural commitments
- [ ] File research artifact at `agentic_orchestration/research/2026-05-27-cycle-14-sc-5-damage-scaling-patterns.md`
- [ ] Append completion record to this dispatch file
- [ ] Round-trip: not applicable

## Acceptance criteria

- [ ] Research artifact filed with per-game per-path formula tables
- [ ] Structural commitments confirmed or amendment-recommendations surfaced (per § 7 below)
- [ ] Edge-case catalogue (per § 7.3 below)
- [ ] AI-tell + community-perception-of-arpg-damage-flavor noted
- [ ] Completion record appended; commit + push per Matt 2026-05-27 per-cycle push pattern

## Out of scope (explicit non-goals)

- Do NOT implement damage_resolver code — Wave 0.5 implementation work owned by gamora
- Do NOT emit per-skill schema changes — that's rocket's seam at Wave 0.5
- Do NOT make per-level scaling formula recommendations — that's deferred per doc 41 § 4 #1; Cycle 14 v1 is L50 cap baseline only
- Do NOT enter Mode B catalogue crawl — Mode A analytical research only
- Do NOT touch substrate library / DB — read-only research

## Research questions (legolas resolves)

### 7.1 Per-game per-path formula mapping

For each surveyed ARPG, document:

| Game | Physical formula structure | Magical formula structure | Hybrid handling | Caster weapon role |
|---|---|---|---|---|

Detail level: structural skeleton (which factors multiply / add) per community-wiki + community-theorycraft sources. Goal is structural pattern recognition, not exact coefficients.

### 7.2 Structural validation of doc 47 formulas

- **Q-SC5-1**: Doc 47 § 4 physical formula multiplies `weapon_base_physical_damage × skill_damage_multiplier × (1 + attribute_bonus/100) × (1 + global_modifier/100) × tier_coefficient × ...`. Does community-canonical genre pattern support this structure? What community variations exist (additive vs multiplicative composition of modifiers; pre-mitigation vs post-mitigation crit; etc.)?
- **Q-SC5-2**: Doc 47 § 4 magical formula uses `base_spell_damage` (skill-derived, not weapon-derived) × skill_damage_multiplier × attribute_bonus × element_affinity × (1 + weapon_spell_modifier/100) × tier_coefficient. Does community-canonical genre pattern support `base_spell_damage` as the seed (vs alternative: weapon-derived "weapon damage" that scales appropriately for caster items as D3/D4 do)? What variations exist and what are their tradeoffs?
- **Q-SC5-3**: Doc 47 § 2.1 hybrid type uses per-skill design + cross-attribute ω-penalty per Option C substrate composition policy. What community-canonical genre patterns exist for hybrid skills (Red Mage / Spellsword / Holy Knight / Monk archetypes)? Identify common patterns: weighted-sum / max-of / each-stat-feeds-half / element-on-physical-hit-flat-bonus / etc.
- **Q-SC5-4**: Doc 47 § 1.2 genre canon table surveys 6 ARPGs at high-level "weapon damage scales physical / spell damage scales magical / caster weapons modify spell damage via multipliers." Does legolas' deeper research confirm or refine this characterization? Surface any community-canonical contradictions.

### 7.3 Edge-case catalogue

Catalog edge cases that doc 47 implementation must handle:

- **Weapon-element-conversion skills** (T4 ELEMENT_CONVERSION) — does element-converted physical scale fully like physical or partially like magical?
- **Weapon-attribute scaling for caster weapons** — e.g., a wooden staff has physical damage stat; if a STR character somehow equips it, does that physical damage scale by STR? (Recommendation: probably enforce weapon_type_family + attribute_requirement at equip)
- **Hybrid skills with both physical and magical components** — sum_paths approach vs per-path-isolated approach
- **Element affinity stacking** — `+%fire damage` partition affixes + element_affinity weapon modifier — additive or multiplicative composition?
- **Crit on magical** — does spell power crit work the same as physical crit?
- **DOT scaling** — burn / poison / bleed / freeze — do these scale from instant damage or have separate scaling formula?
- **Off-hand item scaling** — secondary_item for off-hand caster items per `off-hand-items-2026-05-24.md`

### 7.4 AI-tell + community-perception

- **Q-SC5-5**: What damage-formula failure modes do community discussions surface as "feels-bad" (e.g., D4 launch builds where 5+ multiplicative damage modifiers stacked into 50000x multipliers)? What mitigations exist?
- **Q-SC5-6**: What patterns produce "wooden-staff-scaling-Ice-Spike"-style failure modes in community-canonical implementations (where the formula architecture is technically correct but produces feels-bad outcomes)?

## References

- `canonical/47-damage-scaling-architecture-2026-05-27.md` (the doc this research grounds + validates)
- `canonical/story/skill-system-2026-05-24.md` (composition pattern + tier_coefficient)
- `canonical/story/weapon-substrate-composition-policy-v1-2026-05-24.md` (Option α / β / C cell-type matching)
- `canonical/story/attribute-system-2026-05-24.md` (4-attribute system)
- `canonical/46-concentration-architecture-2026-05-27.md` § 2 (Layer 1 stat-range bounds — formulas respect bounds)
- `canonical/41-progression-framework-2026-05-27.md` § 4 #1 (per-level deferred; L50 cap baseline)
- `agentic_orchestration/gandalf/notes/2026-05-27-cycle-14-framing-brief.md` § 2 Wave 0.5 + § 3.4 + § 5 SC-5
- Path of Exile wiki / D2 LoD theorycrafting / D3 / D4 / Last Epoch / Grim Dawn / Lost Ark community-canonical sources
- Engineering disciplines #18 + #11 + #1

---

## Completion record

**Completed:** 2026-05-27 (Cycle 14 Wave 0; legolas Mode A research session)
**Status:** COMPLETE — research artifact filed; appendices + source list complete
**Author:** legolas (substantive research) + knight-rider (orchestration completion recovery — see note below)
**Artifact:** `agentic_orchestration/research/2026-05-27-cycle-14-sc-5-damage-scaling-patterns.md` (658 lines; 64KB)

### Notes for KR integration

Legolas Mode A session completed substantive research (per-game per-path formula tables; structural validation of doc 47; edge-case catalogue; AI-tell + community-perception; appendix A doc 47 formula amendments table; appendix B framing-audit checklist) but session stream stalled at the final commit + completion-record step (stream watchdog timeout at 600s after final artifact write). KR completed orchestration recovery: completion record appended + commit + push.

### Acceptance criteria summary

- [x] Research artifact filed at `agentic_orchestration/research/2026-05-27-cycle-14-sc-5-damage-scaling-patterns.md` — 658 lines
- [x] Per-game per-path formula tables (D2 LoD / D3 / D4 / PoE / Last Epoch / Grim Dawn / Lost Ark + others)
- [x] Structural validation of doc 47 formulas (per § 7.2 of dispatch)
- [x] Edge-case catalogue (per § 7.3 of dispatch)
- [x] AI-tell + community-perception per § 7.4
- [x] Round-trip: not applicable

### Key findings (for KR Wave 0.5 dispatch authoring)

Per Appendix A doc 47 formula amendments table:

- **Magical formula REFINE:** pool weapon_spell_mod + element_affinity + global_spell into ONE additive `(1 + sum_pct/100)` term (matches PoE / LE / post-S2 D4 canonical pattern)
- **Physical formula MINOR REORDER:** element_conversion_factor before tier_coefficient (canonical genre ordering)
- **DOT sub-formula ADD:** doc 47 § 4 does not currently specify DOT scaling; gamora damage_resolver needs DOT sub-formula
- **Crit on magical CONFIRMED:** unified `player.crit_chance` model is valid (D4/LE precedent)
- **Off-hand integration ADD:** § 4.3 needs note that off-hand modifier fields aggregate into same pools as main-hand

Per Appendix B framing-audit (Discipline #23):

- Live risk: substrate weapon library must expose `spell_damage_modifier` per-weapon (doc 47 § 8.3 audit-needed flag) — this is SC-6 elrond's audit scope
- BASE_SPELL_DAMAGE table (per-skill calibrated data source at Wave 0.5) — rocket's Track D.2 per-skill emission populates this OR generated as separate calibration artifact

### Open questions for gamora at Wave 0.5

Documented in research artifact body; not surfaced to Matt (no framing-level concerns; doc 47 architecture sound and well-grounded per Discipline #23 Q3).
