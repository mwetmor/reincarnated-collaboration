# Finding — 2026-05-16 — Decisions-log batch Gate 1 (4 entries)

**Reviewer:** jack-ryan
**Severity:** WARN (overall) — no BLOCKs; two items need attention before the entries are treated as fully closed
**Target:** 4 pending entry drafts in `qa/pending/`, 2026-05-16
**Developer:** knight-rider (authored all 4 drafts)
**Principles applied:** Principle 2 (design decisions recorded), Principle 4 (decisions-log is source of truth), Discipline #12 (semantic-shifting must be named)

---

## Preliminary observation — entries already committed

All four pending entry sets are already present in `reincarnated-engine/design/decisions/decisions-log.md`. The commits appear to have landed before Gate 1 review completed. This finding therefore operates as a **post-commit Gate 1 review** rather than a pre-commit gate. The verdicts below describe what is in the log, what needs a follow-on correction, and what can stand as-is.

This is a process note, not a BLOCK. Matt should be aware that the four batches landed without formal Gate 1 sign-off. The substantive review below determines whether any corrections are needed.

---

## Overall verdict: PASS WITH FLAGS

Two items require follow-on correction (both are WARN, not BLOCK). The other content is internally consistent, appropriately scoped, and correctly cited. No entry requires reversion.

---

## Entry 1 — Engine-balance stewardship: View A lock + divergence framework + movement-modeling

**Verdict: PASS WITH FLAGS**

### What I found

The entry correctly locks View A, operationalizes the divergence framework, and names the movement-modeling limitation. Content is internally consistent with file 29's "shaped balance over numeric scaling" philosophy. The rejection of View B is correctly grounded. The "conservative margin" argument (movement-speed-aware sim would close the gap further) is sound and appropriately hedged.

The B10.2 supersession scope is correctly bounded in the companion entry (Entry 2 below): it replaces only the "Convergence = full fidelity" clause, not the PackProxy architecture, swarm gauntlet composition (Model C), or the AOE multiplier. The two entries together preserve the correct historical layers.

### Flags

1. **General-principle clause not updated (WARN).** The old B10.2 Two-Gauntlet Pattern entry (line 966 of decisions-log.md) still contains: *"General principle: Any future proxy entity... Recompose = proxy-free 1v1. Convergence = full fidelity."* My Q2 WARN in `qa/findings/2026-05-15-b10-4-option-2-and-aoe-philosophy.md` explicitly required this clause to be restated in the supersession entry. The supersession entry (line 1272) correctly describes Option 2's semantics but does NOT include a revised general-principle clause for future proxy entity treatment. The old clause now reads as operative to anyone scanning the superseded entry without reading the supersession entry's cross-reference. A reader following the general-principle clause would implement the wrong pattern.

   **Required action:** knight-rider should add a revised general-principle clause to the supersession entry (line 1272 block). Proposed text: *"Revised general principle: Any future proxy entity that modifies encounter shape (swarm, split, summon, etc.) requires the same treatment: proxy-free 1v1 for recompose evaluation; excluded from convergence binary-search target (diagnostic-only surface for convergence)."* This closes the Q2 WARN that was a stated prerequisite for Option 2 to proceed.

2. **Discipline #14 reference in pending draft not carried through (INFO).** The naming-triad entry's implementation cascade references "Discipline #14 anti-bias scaffolding" for star-lord LLM prompt construction. This is reflected in the committed entry (line 1158). However, the engine-balance-stewardship entry does NOT reference Discipline #14 even though the movement-speed-aware sim extension (Lock 3b) could interact with the same anti-bias scaffolding concern if movement modeling produces bias by class substrate. This is a low-priority observation — not blocking and not a principles violation in the current entry. File for consideration during Stage A2 dispatch authoring.

3. **"3c timing flexibility" decision authority ambiguous (INFO).** The entry states: *"Stage A2 alongside B14.5 calibration work. Matt's call if gamora bandwidth differs."* In the committed version (line 1238), the language reads: *"Stage A2 alongside B14.5 calibration work. Acceptable to defer if gamora's bandwidth is constrained; lock the position for now."* The committed version removes Matt's explicit decision authority on timing. This is a minor softening — the spirit is preserved — but if gamora defers Stage A2 without Matt's explicit sign-off, the precedent for autonomous deferral is ambiguous. Not a BLOCK; note for dispatch authoring.

---

## Entry 2 — B10.2 Two-Gauntlet Pattern supersession

**Verdict: PASS WITH FLAGS (same flag as Entry 1 item 1)**

### What I found

The supersession is correctly scoped. The committed entry (line 1272-1296) leaves intact:
- PackProxy architecture and Model C (S6 pack rendering still references PackProxy per B10.2)
- Swarm gauntlet composition
- AOE N× multiplier

It replaces only the convergence-target definition: "Convergence = full fidelity" → "non-pack WR = 50%." The original entry's status was correctly updated to Superseded (line 968). The two-entry pattern (old entry status updated + new entry added) follows the decisions-log format convention. The "diagnostic surface" framing correctly preserves pack-fight telemetry without making it a convergence input.

### Flags

1. **General-principle clause gap (WARN — same as Entry 1 flag 1).** The supersession entry does not restate the revised general-principle for future proxy entity treatment. This is the primary open item for this entire batch. See Entry 1 flag 1 for the required action.

2. **Cross-seam follow-on language discrepancy (INFO).** The pending draft says the milestone tag "is held pending Option 2 implementation." The committed entry (line 1291) says the tag "was held pending Option 2 implementation + this entry landing." The past tense implies Option 2 is already implemented. If Option 2 has NOT yet been implemented in gamora's code, the committed language overstates completion status and may cause gamora to believe the BLOCK is cleared. Knight-rider should verify gamora's implementation status and correct the tense if Option 2 is still in flight.

---

## Entry 3 — Court of Forms canonical + meaning-of-the-arc

**Verdict: PASS**

### What I found

The entry is well-scoped. The Court framing (the form library's relational identity) is correctly distinguished from the Earth Self hub (the UX container that holds the Court). The committed entry (line 1024) says "The Earth Self's hub holds the Court" — this preserves the hub as TBD while locking the Court as its content. The knight-rider self-flagged stress-test (does this accidentally lock the hub?) is answered: no. "Drax (Earth-Self-hub presentation...)" in the implementation cascade correctly implies presentation work is still to be dispatched, not locked.

The Fate/Zero rejection is correctly grounded in doc 37 § 9.1 (implicit-pillar drift pattern). The Solo Leveling precedent is correctly cited with the non-humanoid substrate caveat (Beru, Tank). The meaning-of-the-arc statement is load-bearing and appropriate for its canonical role.

The knight-rider self-flagged question about forthcoming docs (`embodiment-narrative-layer.md`, `trial-moment-ritual.md`): these are pointers to future work, not load-bearing on the current lock. The entries correctly name them as forthcoming. No issue.

### Flags

None substantive. Entry is clean.

---

## Entry 4 — Enemy visual legibility

**Verdict: PASS**

### What I found

The "6-12 initial base monster archetypes" language is correctly qualified as "initial" in both the pending draft and the committed entry (line 1065: "6-12 initial base monster archetypes"). The knight-rider self-flagged concern (does S1 over-specify the registry sizing?) is answered: no, the "initial" qualifier gives Legolas flexibility at implementation time.

S6 correctly references PackProxy per B10.2. S7's Mirror exception is correctly scoped as a canonical exception to S1, not a contradiction of it. The emit-surface fields (8 fields) are correctly noted as "mostly derivable from existing data." The MIGRATION.md requirement for star-lord → drax cross-seam schema change (per ADR-004) is present in the implementation cascade.

The anti-pattern rejection as a Discipline #13 application is appropriate — this is exactly the implicit-pillar use case Discipline #13 was designed for.

### Flags

None substantive. Entry is clean.

---

## Entry 5 — Style register locked

**Verdict: PASS**

### What I found

The "consumption-time filter, not a crawl-scope constraint" framing is load-bearing and correctly stated. The demo1 legacy-state handling ("operationally accepted as legacy; locked register applies to forward work") is the right pattern — it avoids making the lock retroactively disruptive.

The four-candidate analysis (A/B/C/D) is present and alternatives are correctly rejected. No design-principle violations.

### Flags

None substantive. Entry is clean.

---

## Entry 6 — Naming triad locked

**Verdict: PASS**

### What I found

The universal-frame + per-season-variant pattern is correctly motivated. The "Mirror" and "Passage" renames are correctly grounded in substrate-incompatibility (Discipline #13-adjacent reasoning for doppelganger; Discipline #12 for the semantic shift from "death-body-swap"). The engine-side technical name retention (`doppelganger_validation_runs` stays) correctly distinguishes player-facing register from internal technical names — this is a clean Discipline #12-compliant pattern.

The Yomi worked example is appropriate. The one-call generation integration with the cipher architecture (doc 37 § 6) is correctly cited.

### Flags

None substantive. Entry is clean.

---

## Entry 7 — research.db retired

**Verdict: PASS**

### What I found

The task description framing this entry as "elrond is the new data steward; catalogue.db is the successor" is NOT what the pending file actually asserts — those claims do not appear in the draft text. The committed entry correctly limits itself to: research.db retired, 2026-05-07 deferral closed, archive preserved. The Steward-judgment paragraph is appropriately included and correctly frames Elrond's authority as Tier C+ data-steward operating correctly.

The SHA-256 hash for the archive snapshot is a useful integrity anchor. The cross-seam follow-on (star-lord script cleanup per ADR-004) is correctly noted as in-flight.

The 2026-05-07 entry's status line was correctly updated (line 147: "Superseded by 2026-05-16..."). The format convention is followed.

### Flags

None substantive. Entry is clean.

---

## Required actions before entries are treated as fully closed

- [ ] **knight-rider (WARN — Entry 1 + 2):** Add a revised general-principle clause to the 2026-05-16 B10.2 supersession entry in decisions-log.md. The clause should replace the old "Convergence = full fidelity" general principle with the Option 2 proxy-treatment rule. See Entry 1 flag 1 for proposed language. This was a stated prerequisite in my 2026-05-15 Q2 WARN.

- [ ] **knight-rider (INFO — Entry 2):** Verify gamora's Option 2 implementation status. If Option 2 code is not yet merged, correct the committed entry's past-tense language ("was held pending") to present-tense ("is held pending") to prevent gamora from treating the BLOCK as cleared prematurely.

- [ ] **Matt (INFO — process):** Four entries committed before Gate 1 sign-off. No reversion required — content is sound — but the pattern of commit-before-Gate-1 should be noted as a deviation from the drafted process and agreed on explicitly if it's the intended workflow going forward.

---

## References

- `/Users/admin/Games/reincarnated-engine/design/decisions/decisions-log.md` — lines 145-157 (2026-05-07 superseded entry), 958-970 (B10.2 Two-Gauntlet original + status update), 1024-1047 (Court), 1050-1094 (enemy viz), 1098-1116 (style register), 1120-1162 (naming triad), 1166-1202 (research.db retired), 1206-1268 (engine-balance stewardship), 1272-1296 (B10.2 supersession)
- `/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/qa/findings/2026-05-15-b10-4-option-2-and-aoe-philosophy.md` — Q2 WARN: general-principle clause update required
- `/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/qa/pending/2026-05-16-decisions-log-engine-balance-stewardship.md`
- `/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/qa/pending/2026-05-16-decisions-log-court-and-enemy-viz.md`
- `/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/qa/pending/2026-05-16-decisions-log-style-register-and-naming-triad.md`
- `/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/qa/pending/2026-05-16-decisions-log-research-db-retired.md`
