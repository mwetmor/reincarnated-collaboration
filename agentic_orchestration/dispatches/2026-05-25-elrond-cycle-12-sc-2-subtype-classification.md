# Dispatch — 2026-05-25 — elrond + rocket — Cycle 12 SC-2 weapon_kind_classified_subtype backfill (~50-100 items)

**From:** knight-rider
**To:** elrond (lead — data steward; catalogue DB) + rocket (consultant — classification judgment for ambiguous items)
**Approved by:** Matt 2026-05-25 (Cycle 12 framing brief bulk-ratification — Q5 sidecars SC-1 + SC-2; KR autonomously orchestrates Cycle 12 sidecars per scope-doc § 1)
**Estimated effort:** ~1-2 hours combined (~30-60 min elrond enumeration + bulk classification + ~30-60 min rocket consultation on ambiguous items + ~30 min finalization)
**Acceptance:** Backfill `weapon_kind_classified_subtype` field for ~50-100 currently-unset items in catalogue DB (fantasy + military_modern subset); per-item before/after audit; MIGRATION.md if cross-seam impact; rocket consults on ambiguous-classification items

---

## Context

Cycle 12 framing brief § 2 SC-2 surfaces a substrate-curation cleanup: ~50-100 items in the catalogue DB currently have `weapon_kind_classified_subtype` field unset, predominantly in the fantasy + military_modern subset. This field provides finer-grained classification beyond the parent `weapon_kind` (e.g., parent: `polearm`; subtype: `glaive` vs `naginata` vs `halberd` — capturing per-product-line register variation per Discipline #25 + composition policy v1).

Per framing brief § 2 SC-2, this sidecar is co-owned: elrond leads the DB enumeration + backfill execution; rocket consults on ambiguous-classification items (rocket has engine-canonical-library knowledge useful for classification judgment on fantasy items per Pattern A-light routing).

Cycle 12 fires in parallel with Cycle 11 close. SC-2 fires as a sidecar at any time during Cycle 12 Day 1 per scope-doc § 1; no specialist contention.

---

## Required reading before starting

- `canonical/00-ground-state.md` § 1
- **`agentic_orchestration/gandalf/notes/2026-05-25-cycle-12-new-engine-parallel-build-framing-brief.md`** § 2 SC-2 (scope statement) + § L9 (substrate split — weapon_kind_classified_subtype is mechanical-layer per L9, NOT semantic-overlay; subtype identifies mechanical sub-category)
- `agentic_orchestration/cycles/cycle-12-hive-mind-scope.md`
- `canonical/story/weapon-substrate-composition-policy-v1-2026-05-24.md` § 1 (per-register coverage targets) + § 3 (Option α/β/C cell-matching — subtype affects cell-tuple matching) + § 5 (per-cell coverage)
- Cycle 10 Stage 0a accessory+armor classifier precedent (elrond): `dispatches/2026-05-24-elrond-cycle-10-stage-0a-accessory-armor-classifier.md` or commit `6f3c288` (pattern: enumerate untagged + classify into subtype enum)
- Cycle 10 Stage 4 mechanical-tagging dispatch (rocket): `dispatches/2026-05-25-rocket-cycle-10-stage-4-mechanical-tagging.md` (rocket's subtype-classification authority context)
- v1_scope substrate state: 3,042 rows curated (per Cycle 10 wind-down); subset has `weapon_kind_classified_subtype` unset
- elrond seam state: `agentic_orchestration/elrond/` notes + recent commits
- rocket seam state: `~/Games/reincarnated-engine/src/reincarnated/generation/AGENT_STATE.md` (engine-canonical-library subtype knowledge)
- `~/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md` #11 empirical inspection + #25 semantic-layer rep-audit + ADR-004 MIGRATION.md cross-seam

---

## Math-before-code (per Discipline #1)

No math. Database enumeration + backfill operation; no new computation.

Pre-fire: elrond should query the catalogue DB to enumerate items currently with `weapon_kind_classified_subtype IS NULL` AND filtered to fantasy + military_modern register-subset (per framing brief § 2 SC-2 scope). Report scope finding back to KR in completion record: how many items found; per-parent-weapon-kind breakdown; per-register breakdown.

---

## Scope (elrond + rocket co-execution)

### Phase 1 — elrond enumeration (lead)

- Query catalogue DB for items with `weapon_kind_classified_subtype IS NULL` AND register in (`fantasy`, `military_modern`) per framing brief § 2 SC-2
- Report: total count; per-parent-weapon-kind count; per-register count
- Per-row metadata snapshot: weapon name + parent weapon_kind + register + cultural_tradition + period (for rocket consultation context)
- If count > 100, flag to KR — surface whether SC-2 scope expansion is in-scope per scope-doc § 1 (KR judgment; likely yes if cheap; escalate if >>100)
- If count <50, proceed with the smaller set; no scope adjustment needed

### Phase 2 — elrond classifies obvious items (lead)

- For items where subtype classification is obvious from name + parent weapon_kind + cultural_tradition (e.g., parent=polearm + cultural=feudal_japanese + name="naginata" → subtype="naginata"; parent=sword + cultural=european_medieval + name="longsword" → subtype="longsword"), elrond classifies directly per existing canonical subtype enum
- For ambiguous items (e.g., fantasy-original weapon with no clear historical precedent; military_modern items where parent could subdivide multiple ways), DEFER to rocket consultation per Phase 3
- Per-classified-item: rationale captured (e.g., "naginata: feudal_japanese polearm per cultural_tradition + canonical subtype enum")

### Phase 3 — rocket consultation on ambiguous items (consultant; sub-agent invocation by KR if needed)

- KR invokes rocket sub-agent (Agent tool) with the ambiguous-item list from elrond Phase 2
- Rocket consults engine-canonical-library + Cycle 10 Stage 4 mechanical-tagging context to recommend subtype classifications for ambiguous items
- For fantasy items with no historical precedent, rocket may invent a subtype (per existing fantasy subtype enum if available) OR flag for gandalf Pattern A-light if subtype-naming-design is genuinely a design question
- Rocket returns per-item classification recommendation + rationale
- Elrond consumes rocket's recommendation + applies backfill

### Phase 4 — elrond bulk backfill + audit (lead)

- Apply backfill SQL to all classified items (Phase 2 + Phase 3 combined)
- Post-update audit: confirm all enumerated items now have non-NULL `weapon_kind_classified_subtype`
- Per-item before/after sample in completion record (at least 10 items, covering both elrond Phase 2 + rocket Phase 3 classifications)

### Phase 5 — MIGRATION.md if cross-seam impact

- Per Discipline ADR-004 — if other seams consume `weapon_kind_classified_subtype` (likely: Architecture B Phase 2 substrate-binding uses subtype for cell-match; composition policy uses subtype for register-share; cohesion-judge uses for naming), MIGRATION.md authored
- MIGRATION.md flags the data change for downstream awareness

---

## Out of scope

- Backfill of register subsets outside fantasy + military_modern (per framing brief § 2 SC-2; defer historical / mythological to existing tags or v1.1+)
- Subtype enum schema extension (use existing canonical enum; if extension needed, route to gandalf via KR — likely escape-hatch)
- Cross-seam consumer code changes (other seams may consume the backfilled values, but elrond + rocket do not change their code)
- New items addition (this is cleanup of existing entries)
- SC-1 substrate-tagging cleanup (separate dispatch — fires in parallel)
- SC-3 off-hand mechanical contract design (absorbed into Layer 3 rocket dispatch per framing brief § 2)

---

## Acceptance criteria

- [ ] Phase 1 enumeration query authored + run; total count + per-parent-weapon-kind breakdown + per-register breakdown captured
- [ ] Phase 2 elrond direct classifications applied; per-classified-item rationale captured
- [ ] Phase 3 rocket consultation completed (if ambiguous items surfaced); rocket recommendations applied
- [ ] Phase 4 backfill audit: all enumerated items now have non-NULL `weapon_kind_classified_subtype`
- [ ] Per-item before/after sample in completion record (≥10 items)
- [ ] MIGRATION.md authored if cross-seam consumer impact per ADR-004
- [ ] Per Discipline #11 empirical inspection: direct-inspected catalogue DB rows BEFORE updating
- [ ] Per Discipline #25 semantic-layer rep-audit: confirm `weapon_kind_classified_subtype` correctly classifies mechanical sub-category, not semantic overlay
- [ ] Auto-commit + auto-push per elrond seam authorization (CLAUDE.md addendum)
- [ ] Tag: `elrond/cycle-12-sc-2-subtype-classification-2026-05-25`

---

## Open questions for the agent to resolve

- Exact enumerated count + scope adjustment (if count >>100, escalate to KR for scope decision; if count <50, proceed with smaller set)
- Whether rocket consultation needs to fire (depends on Phase 2 ambiguous-item count; if elrond classifies all directly, Phase 3 skips)
- Exact subtype enum values per parent weapon_kind — elrond reads existing canonical enum from catalogue schema OR rocket engine canonical library; if enum coverage incomplete, route to gandalf Pattern A-light for subtype-naming-design judgment
- Whether MIGRATION.md is needed (depends on which seams actually consume this field; elrond checks via grep)
- Whether gandalf Pattern A-light routing surfaces for items where subtype-naming-design is genuinely a design question (e.g., fantasy items with no historical precedent; KR routes via parallel sub-agent if rocket flags)

---

## Cross-seam impact

Round-trip: not applicable — substrate-classification backfill is a data update on existing column; no schema change; no fixture-dict shape change. Other seams (Architecture B Phase 2 substrate-binding; composition policy register-share targets; cohesion-judge naming) consume these values but their consumer code is unaffected (same column reads; new values). MIGRATION.md authored to flag the data change.

---

## References

- `agentic_orchestration/gandalf/notes/2026-05-25-cycle-12-new-engine-parallel-build-framing-brief.md` § 2 SC-2 + § L9
- `agentic_orchestration/cycles/cycle-12-hive-mind-scope.md`
- `canonical/story/weapon-substrate-composition-policy-v1-2026-05-24.md` § 1 + § 3 + § 5
- Cycle 10 Stage 0a accessory+armor classifier (elrond precedent): commit `6f3c288`
- Cycle 10 Stage 4 mechanical-tagging dispatch (rocket precedent): `dispatches/2026-05-25-rocket-cycle-10-stage-4-mechanical-tagging.md`
- `~/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md` #11 + #25 + ADR-004

---

## Sign-off

**Author:** knight-rider (orchestrator)
**Authority:** Matt 2026-05-25 Cycle 12 framing brief bulk-ratification (Q5 sidecars SC-2 fires); KR autonomously orchestrates per scope-doc § 1; co-execution per framing brief § 2 SC-2 owner declaration
**Status:** FIRE — Day-1 sidecar; fires in parallel with legolas MC-1+MC-2 + jack-ryan Gate-1 + elrond SC-1 + Cycle 11 close drax Wave 3b

**Matt-touch sequence:** elrond + rocket complete → KR captures completion in state file → if subtype-enum-extension OR fantasy-naming-design surfaces emerge, KR routes Pattern A-light to gandalf; otherwise auto-close
