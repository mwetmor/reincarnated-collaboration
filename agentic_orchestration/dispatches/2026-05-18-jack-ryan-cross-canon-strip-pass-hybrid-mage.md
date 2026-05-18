# 2026-05-18 — jack-ryan — Cross-canon strip pass: remove hybrid_mage references per gandalf § 8

**Authority:** Gandalf v1.11 canonical-6 design doc § 8 cleanup list; downstream of jack-ryan v1.7 decisions-log RETIRE entry; rocket v1.17 archetype-list removal complete.
**Type:** Pattern A — doc-only retain-with-annotation pass; ~45-60 min.
**Predecessor (shipped):** gandalf v1.11 canonical-6 transition doc + jack-ryan v1.6/v1.7 + rocket v1.17.
**Status:** 🟢 **ACTIVE — fire immediately.**

---

## Why this matters

Canonical-6 transition is 3/4 complete on the orchestration side. Cross-canon docs across `canonical/` + `canonical/story/` still reference hybrid_mage in design context. Gandalf § 8 enumerated the ~14 docs needing amendment + recommended a **retain-with-annotation pattern** (§ 8.6) — keep historical context, add "RETIRED 2026-05-18; see decisions-log + canonical-6-transition" annotation pointing to the new canonical truth.

Goal: complete the cross-canon coherence sweep so future agents reading these docs find clear retirement pointers and don't try to design against / re-introduce hybrid_mage.

---

## Required reading

1. **Gandalf canonical-6 doc § 8** — `canonical/story/canonical-6-transition-retire-hybrid-mage-2026-05-18.md` § 8 (cross-canon cleanup list with annotation pattern at § 8.6)
2. **Your prior decisions-log RETIRE entry** — `reincarnated-engine/design/decisions/decisions-log.md` (your authoritative pointer)
3. **Discipline #17 entry** — `reincarnated-engine/design/working-agreement/engineering-disciplines.md` (your other recent landing; cross-ref target for the smoke environment fidelity case study)

---

## Scope — ~14 docs amended (per gandalf § 8)

Per gandalf § 8 list, the cleanup spans:

### canonical/ docs
- canonical/09-XX (verify exact filename per gandalf list)
- canonical/17-gear-and-spirit-guide-design.md
- canonical/28-XX
- canonical/30-XX
- canonical/32-progression-design.md
- canonical/33-XX
- canonical/16a-XX (or similar variant)

### canonical/story/ docs
- D11 chain docs (D11 advisory; D11.1 if exists; D11.2 advisory + post-mortem)
- archetype-coupling-archaeology-2026-05-17.md (Coupling #3 stat_allocator finding — annotate)
- embodiment-narrative-layer-*.md (if hybrid_mage named)
- vs2a-vfx-scene-needs.md (if hybrid_mage named in archetype context)

### Engine code references (flag for rocket, don't modify yourself)
- Note any engine-code docstrings or comments rocket left annotated (he retained Lever B code with retirement comment)

### Consume-time surfaces (flag for drax, don't modify yourself)
- reincarnated-loadout/data references (data-side only; class JSON has is_retired flag from rocket)
- reincarnated-demo/data references (same)

## Method — retain-with-annotation pattern

Per gandalf § 8.6:

For each hybrid_mage reference in a canonical doc, ADD an annotation inline:

> *(Hybrid_mage archetype RETIRED from canonical 2026-05-18 per Matt L3 verdict; see [decisions-log](path/to/decisions-log.md#retire-hybrid-mage) + [canonical-6 transition](path/to/canonical-6-transition.md). Historical context retained.)*

Don't delete the surrounding context — the design rationale that mentioned hybrid_mage may still be relevant for the remaining 6 archetypes or for understanding why retirement happened.

**Exception:** If a doc has a top-level archetype enumeration list (e.g., "the 7 canonical archetypes are: X, Y, Z, hybrid_mage, ..."), AMEND that list to canonical-6 directly (remove hybrid_mage from the enumeration; add a footnote pointing to retirement docs).

## Deliverables

1. **Per-doc amendments** — ~14 docs annotated per pattern above
2. **Amendment audit log** — short file at `reincarnated-collaboration/agentic_orchestration/research/curated/cross-canon-strip-pass-audit-2026-05-18.md` listing each doc + amendment type (annotation vs enumeration-amend) + line/section refs
3. **Hive-log STATE entry** — strip pass complete; canonical coherence restored
4. **AGENT_STATE update** — cross-canon coherence pass shipped

---

## Acceptance criteria

- [ ] All ~14 docs from gandalf § 8 amended (annotation or enumeration-amend per pattern)
- [ ] Each amendment retains historical context; cross-references decisions-log + canonical-6 transition
- [ ] Audit log authored at named path with per-doc summary
- [ ] No accidental deletion of design context (retain-with-annotation, not strip-and-delete)
- [ ] PRE-SIGNAL § 14.1.1 before hive-log append
- [ ] AGENT_STATE STATE entry
- [ ] Tag `jack-ryan/v1.8-cross-canon-strip-pass-1`

---

## Out of scope (DO NOT)

- ❌ DO NOT modify engine code (rocket retained Lever B with annotation; that's complete)
- ❌ DO NOT modify demo / loadout data files (rocket backfilled is_retired flag; drax filter is downstream)
- ❌ DO NOT delete D11.2 advisory or post-mortem content (annotate with "retracted" pointer; preserve historical record)
- ❌ DO NOT re-litigate RETIRE
- ❌ DO NOT push tag (ADR-006)

---

## Coordination

- **Predecessors:** gandalf v1.11 (cleanup list); your v1.7 decisions-log + v1.6 Discipline #17 (cross-ref targets); rocket v1.17 (code-side complete)
- **Parallel-safe with:** drax v1.16.2 (in flight; different repo); drax v1.17 (queued; different repo)
- **Triggers downstream:** none — terminal node of canonical-6 transition chain (along with drax v1.17 in parallel)
- **PRE-SIGNAL § 14.1.1** before hive-log appends

---

## After this lands

Canonical-6 transition is 3/4 complete (gandalf + jack-ryan + rocket); drax v1.17 is_retired filter is the 4th and final node. Once drax v1.17 ships, the canonical-6 chain is **fully locked** and new-season regen at canonical-6 unlocks per Matt's stated milestone.

---

*Dispatched 2026-05-18 by knight-rider per gandalf § 8 cleanup list + rocket v1.17 completion. ~45-60 min. Append completion record + audit log path when done.*

---

## Completion record — jack-ryan v1.8

**Completed:** 2026-05-18
**Tag:** `jack-ryan/v1.8-cross-canon-strip-pass-1` (local; push gated per ADR-006)
**Commit:** `4c05383` (reincarnated-collaboration main; 16 files)

**All acceptance criteria MET:**
- [x] All ~14 docs from gandalf § 8 amended (annotation or enumeration-amend per pattern) — canonical-17 confirmed clean (no hybrid_mage archetype-tag references)
- [x] Each amendment retains historical context; cross-references decisions-log + canonical-6 transition
- [x] Audit log authored at `agentic_orchestration/research/curated/cross-canon-strip-pass-audit-2026-05-18.md`
- [x] No accidental deletion of design context (retain-with-annotation honored throughout; D11 advisory chain body preserved with top-level block annotations)
- [x] PRE-SIGNAL § 14.1.1 verified before hive-log append (fetch origin; log inspection; local 26-ahead; no remote conflict)
- [x] AGENT_STATE at `agentic_orchestration/qa/AGENT_STATE.md` (new file; first jack-ryan state file)
- [x] Tag `jack-ryan/v1.8-cross-canon-strip-pass-1`

**Engineering follow-up flagged (non-blocking):** Coupling #3 stat_allocator fallback → ValueError on unrecognized archetype (post-canonical-6 the fallback target is retired). Recommend separate dispatch post-regen per Matt/knight-rider sequencing.

**Chain status:** gandalf DONE / jack-ryan DONE (v1.6 + v1.7 + v1.8) / rocket DONE — **drax v1.17 is_retired filter is the last dependency.** Once drax v1.17 ships: CANONICAL-6 LOCKED → new-season regen authorization unlocks.
