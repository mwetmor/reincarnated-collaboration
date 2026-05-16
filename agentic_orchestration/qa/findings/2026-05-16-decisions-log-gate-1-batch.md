# Finding — 2026-05-16 — Decisions-log Gate 1 Batch (7 entries, reconciliation)

**Reviewer:** jack-ryan
**Severity:** WARN (overall — no BLOCKs; one residual item needs confirmation; one cosmetic fix)
**Target:** Working-tree `reincarnated-engine/design/decisions/decisions-log.md` (+286 lines uncommitted)
**Developer:** knight-rider (entry author); gamora (B10.2/B10.4 implementation context)
**Principles applied:** Principle 2 (design decisions recorded before code), Principle 4 (decisions-log is source of truth), ADR-002 (decisions-log review process), Discipline #12 (semantic-shifting must be named and framed)

---

## Reconciliation table

The dispatch presented three hypotheses for the mismatch between qa/pending (4 files, 7 entry drafts) and the decisions-log working tree (+286 lines). The reconciliation finding is **scenario (a): entries were written to the file before Gate 1 formally closed**.

The evidence:

- The skill_handoff_2026-05-16.md § "Engine working tree" states explicitly: "the qa/pending entries above are SEPARATE and NOT included in this diff." This is the handoff's claimed state at Day-3 close.
- The actual git diff shows all 7 entries ARE in the working tree. The +286 lines cover all 7 entry locations listed in the dispatch, verbatim.
- The git log on `design/decisions/decisions-log.md` shows the most recent commit (`097281f`) was "B10.2 closure docs: decisions-log + gauntlet-analysis §13 + AGENT_STATE." The 7 new entries are all in the UNCOMMITTED working tree — meaning they were written to the file during Day 3 but the file has not been committed since `097281f`.
- A prior Gate 1 review (`qa/findings/2026-05-16-decisions-log-batch-gate1.md`) already exists, authored by jack-ryan, covering all 7 entries. That file begins with the explicit note: "All four pending entry sets are already present in `reincarnated-engine/design/decisions/decisions-log.md`. The commits appear to have landed before Gate 1 review completed."
- The handoff end-of-day-3 update section records that both WARN items from the batch gate1 review were resolved: "B10.2 supersession entry now includes revised general-principle clause (jack-ryan WARN resolved)" and "B10.2 cross-seam follow-on now explicitly states condition (a) met / condition (b) PENDING (jack-ryan INFO resolved)."

**What actually happened:** Multiple agents wrote to decisions-log.md during Day 3 before the session ended. Knight-rider drafted the qa/pending files as formal review artifacts, but the entries were also written directly to the decisions-log working tree in the same session. Gate 1 was then run retroactively against the in-file text. The handoff's "SEPARATE and NOT included in this diff" language was stale or aspirational at the point it was written.

**Scenario (b) and (c) are ruled out.** There is no partial state — all 7 entries are present. There is no evidence of process bypass for malicious or negligent reasons; the sequence was entry authoring during a long session, retroactive Gate 1, and amendments already applied per the end-of-Day-3 handoff note.

| Entry | In file? | In qa/pending? | Diverges? | Notes |
|---|---|---|---|---|
| Court of Forms (L1024) | Yes | Yes — court-and-enemy-viz.md Entry 1 | Minor | In-file version adds C8 structural commitment detail and Solo Leveling precedent clause not in draft; in-file "Related" section uses full canonical paths. Draft is substantively the same position. No conflict. |
| Enemy visual legibility (L1050) | Yes | Yes — court-and-enemy-viz.md Entry 2 | Minor | In-file version adds S5 name-banner details as inline bullet list vs table format in draft; "anti-pattern is canonically rejected as Discipline #13 application" language appears in both. No conflict. |
| Style register (L1098) | Yes | Yes — style-register-and-naming-triad.md Entry 3 | Trivial | In-file version and draft are substantively identical. In-file adds "Gandalf (design conversations reference this lock)" to implementation cascade; draft has it listed. No conflict. |
| Naming triad (L1120) | Yes | Yes — style-register-and-naming-triad.md Entry 4 | Trivial | In-file version and draft are substantively identical. In-file uses "Discipline #14 candidate" for star-lord anti-bias scaffolding; draft says "Discipline #14 anti-bias scaffolding." No conflict. |
| research.db retired (L1166) | Yes | Yes — research-db-retired.md | Substantive additions | In-file version adds "Steward-judgment save worth noting" paragraph (dispatch summary was loose; Elrond overrode) and the full row-count table in a more structured format. Draft lacks these additions. In-file is MORE complete, not less. No conflict. |
| View A / divergence framework / movement-modeling (L1206) | Yes | Yes — engine-balance-stewardship.md Entry 1 | Minor | In-file version compresses the Lock 1 structure (no sub-headers per entry), removes "3c timing flexibility" with "Matt's call if gamora bandwidth differs" language (replaced with "Acceptable to defer if gamora's bandwidth is constrained; lock the position for now"). The removed Matt-authority language is noted below as INFO. No structural conflict. |
| B10.2 supersession (L1272) | Yes | Yes — engine-balance-stewardship.md Entry 2 | Significant additions | In-file version includes a **Revised general principle clause** (the WARN item from batch-gate1 review) and updated cross-seam follow-on language (condition a met / condition b PENDING). These are the two amendments recorded as resolved in the end-of-Day-3 handoff. In-file is the authoritative and more complete version. |

**Authoritative source for Gate 1:** The in-file working-tree text is authoritative. The qa/pending drafts are precursor documents superseded by the in-file versions. Gate 1 runs against the in-file text, per the batch-gate1 findings file already on record.

---

## Process finding — pre-existing Gate 1 record

A Gate 1 findings file (`qa/findings/2026-05-16-decisions-log-batch-gate1.md`) already exists that covers all 7 entries. That file was authored prior to this dispatch. This reconciliation dispatch was not redundant — it was needed to confirm the prior review was complete, amendments were applied, and the working tree is in a committable state.

The prior findings file is substantive and correct. Its verdicts:

- Entry 1 (View A / divergence framework): PASS WITH FLAGS
- Entry 2 (B10.2 supersession): PASS WITH FLAGS (same flag as Entry 1)
- Entry 3 (Court of Forms): PASS
- Entry 4 (Enemy visual legibility): PASS
- Entry 5 (Style register): PASS
- Entry 6 (Naming triad): PASS
- Entry 7 (research.db retired): PASS

The two WARN items from that file were both resolved per the end-of-Day-3 handoff update. The amended in-file text at lines 1282-1283 (revised general-principle clause) and lines 1291-1293 (condition a met / condition b PENDING) confirms the amendments landed.

This current findings file serves as the reconciliation record and disposition recommendation. The prior findings file stands as the substantive Gate 1 review.

---

## Gate 1 verdicts — per entry (post-reconciliation, running against in-file text)

### Entry 1 — View A locked + divergence framework + movement-modeling (L1206)

**Verdict: PASS WITH FLAGS (1 INFO residual)**

The entry is internally consistent, correctly grounded in Gandalf's engine-balance-stewardship canonical doc, and the critical WARN (revised general-principle clause) is confirmed resolved at L1282. The divergence framework's three constraints are correctly stated with operational measures. The "conservative margin" argument for Lock 1 holding under movement-speed-aware sim is sound.

**Residual INFO (not blocking commit):** The in-file version removed the explicit "Matt's call if gamora bandwidth differs" qualifier on Lock 3c timing flexibility, replacing it with "Acceptable to defer if gamora's bandwidth is constrained." The draft was clearer about decision authority. This is a minor softening. If gamora self-interprets this clause and defers Stage A2 without knight-rider confirmation, the authority chain is ambiguous. Recommend knight-rider add a note to the gamora B10.4 Option 2 dispatch making the Stage A2 timing decision explicit rather than relying on the decisions-log entry language alone.

**Discipline #12 check (semantic-shifting):** The entry does not introduce or blur any semantic shifts. `convergence_winrate` vs `actual_winrate` is correctly identified in the handoff as a separate star-lord fix; it does not affect this entry.

**Matt's three-question framing (drift-audit Q1/Q2/Q3):** The entry's Lock 1 covers Q1 (divergence floor: "less-efficient, not helpless"), Lock 2 covers Q2 (operational divergence measures), Lock 3 covers Q3 (movement modeling). All three are addressed. No language drift from Gandalf's source doc detected.

---

### Entry 2 — B10.2 supersession (L1272)

**Verdict: PASS WITH FLAGS (1 INFO residual, same as Entry 1)**

The WARN item (revised general-principle clause) is confirmed resolved. The in-file text at L1282 reads: "Revised general principle (supersedes the original B10.2 general-principle clause): Any future proxy entity that modifies encounter shape (swarm, split, summon, etc.) requires the same treatment: proxy-free 1v1 for recompose; excluded from convergence binary-search target (diagnostic-only surface)." This is exactly the text the batch-gate1 finding required. The original B10.2 entry (L966) status line was correctly updated.

The cross-seam follow-on language at L1293 correctly reads: "Condition (a) is now met. Condition (b) is not yet complete — gamora's implementation dispatch is PENDING pickup." Present tense, accurate.

**Supersession well-formed check (per dispatch open question):** The supersession entry:
- Has a clear cross-link to the original entry ("2026-05-14 'B10.2 — Two-Gauntlet Pattern: Recompose vs. Convergence' entry (superseded by this entry)")
- The original entry's Status line was updated (L968: "Superseded by 2026-05-16: B10.2 Two-Gauntlet Pattern superseded — Option 2")
- Alternatives-considered section is honest (Option 1 rejected for semantic reasons; pack-slot-count reduction rejected)
- The "why the original framing failed" explanation is present and clear (pack-fight WR floor math)

Supersession is well-formed. PASS.

**Residual INFO:** Same Stage A2 timing authority ambiguity as Entry 1. Not blocking.

---

### Entry 3 — Court of Forms (L1024)

**Verdict: PASS**

In-file text confirms: Court (what the hub holds) is locked; Earth Self hub (the UX container) remains TBD. No accidental hub lock. The Fate/Zero rejection is doc-37-§9.1 grounded. Solo Leveling precedent correctly includes non-humanoid substrate (Beru, Tank). Forthcoming doc references (`embodiment-narrative-layer.md`, `trial-moment-ritual.md`) are correctly pointer-only, not load-bearing on the current lock.

No flags.

---

### Entry 4 — Enemy visual legibility (L1050)

**Verdict: PASS**

"6-12 initial base monster archetypes" correctly qualified as initial; implementation flexibility preserved. S6/PackProxy cross-reference maintained. S7 Mirror exception correctly scoped. MIGRATION.md requirement for star-lord → drax cross-seam schema change correctly present (per ADR-004). Anti-pattern rejection as Discipline #13 application is appropriate.

No flags.

---

### Entry 5 — Style register (L1098)

**Verdict: PASS**

"Consumption-time filter, not crawl-scope constraint" framing is load-bearing and correctly stated. Demo1 legacy-state handling is correct pattern. Four-candidate analysis is present. No design-principle violations detected.

No flags.

---

### Entry 6 — Naming triad (L1120)

**Verdict: PASS**

Universal-frame + per-season-variant pattern is correctly motivated. Rename rationale (substrate-incompatibility for "doppelganger"; cosmological-register motivation for "Passage") is sound. Engine-side technical name retention (`doppelganger_validation_runs` stays until export-boundary rename) correctly distinguishes player-facing register from internal technical names — clean Discipline #12 pattern. One-call generation integration (doc 37 § 6 cipher architecture) correctly cited.

No flags.

---

### Entry 7 — research.db retired (L1166)

**Verdict: PASS WITH FLAGS (1 cosmetic WARN)**

Entry is correct and complete. Steward-judgment paragraph correctly documents Elrond's Tier C+ authority override. SHA-256 hash is present. Cross-seam follow-on (star-lord script cleanup per ADR-004) correctly noted as in-flight.

**Cosmetic WARN (minor, not blocking commit):** The original 2026-05-07 entry's Status line at L157 still reads "Active. Consolidation deferred until `research.db` contents and schema are audited." The supersession block was prepended to the entry heading and a **Status update 2026-05-16** paragraph was added immediately after the heading — but the original `**Status**` field body at L157 was not rewritten. The heading `[SUPERSEDED 2026-05-16]` and the Status update paragraph together make the supersession clear, but a reader scanning only the Status field line would see "Active" without the superseded signal.

This is cosmetically inconsistent with the decisions-log format convention, which the batch-gate1 findings file interpreted as resolved. Strictly, the Status field body should read "Superseded by 2026-05-16: research.db retired" per the pending draft's companion action. Recommend knight-rider update line 157 before committing. However: this does NOT block the commit if knight-rider judges the heading + Status update paragraph combination to be sufficient signal. It is a presentation judgment call, not a principle violation.

---

## Summary verdict table

| Entry | Gate 1 verdict | Blocking? | Action required |
|---|---|---|---|
| View A / divergence framework / movement-modeling | PASS WITH FLAGS | No | INFO only: clarify Stage A2 timing authority in gamora dispatch |
| B10.2 supersession | PASS WITH FLAGS | No | INFO only: same as above; supersession is well-formed |
| Court of Forms | PASS | No | None |
| Enemy visual legibility | PASS | No | None |
| Style register | PASS | No | None |
| Naming triad | PASS | No | None |
| research.db retired | PASS WITH FLAGS | No | WARN: consider updating Status field body at L157 (cosmetic) |

**No BLOCKs. All 7 entries are cleared to commit.**

---

## Reconciliation finding — process deviation

The entries landed in the working tree before Gate 1 formally closed, deviating from the "draft → Gate 1 → Matt approve → commit" flow the qa/pending files specified. Gate 1 was then run retroactively (batch-gate1 findings file), amendments were applied, and the working tree now reflects a reviewed state.

This pattern — "agents write to decisions-log during session, Gate 1 runs against in-file text retroactively" — is a variant of the intended workflow, not a bypass. The substantive review did happen; the ordering was inverted. The practical risk of this inversion is that an incorrect entry could have been hard to reverse if it had been committed before Gate 1. Since the file is uncommitted, the risk did not materialize.

**Process note for Matt:** The qa/pending draft files described a sequential process (draft first, then Gate 1, then commit) that the team did not follow in practice. This is worth making explicit: either (a) revise the qa/pending process docs to describe the retroactive-review variant as acceptable, or (b) enforce pre-write Gate 1 by having knight-rider stage decisions-log edits in a separate branch or temp file. Neither is blocking current work; note for the process retrospective.

---

## Recommendation

### What to commit

**Commit the +286-line decisions-log working-tree diff as-is**, subject to the one cosmetic fix below. All 7 entries have cleared Gate 1. The prior WARN items were resolved and confirmed. No reverts required.

**Before committing — one optional cosmetic fix (WARN):**
- `reincarnated-engine/design/decisions/decisions-log.md` L157: change the original Status field body from "Active. Consolidation deferred until `research.db` contents and schema are audited." to "Superseded by 2026-05-16: research.db retired — consolidation deferral closed." The heading + Status update paragraph already communicate supersession; this makes the Status field itself consistent. Knight-rider's call whether to include this in the commit.

**The commit should also include the other working-tree changes** (db.py deleted, export files, tests) as described in the handoff. This finding covers only the decisions-log portion.

### What to do with qa/pending

The four qa/pending files have served their purpose as drafts. They are superseded by the in-file entries (which are more complete). They may be moved to `qa/findings/` as historical record or deleted. Recommend: move to a `qa/pending/archive/` subdirectory or leave in place — they do not interfere with any active work and serve as a paper trail for the process deviation noted above. Knight-rider's call.

### Gamora B10.4 milestone tag unblock status

Per this Gate 1 finding and the prior batch-gate1 review: **the decisions-log prerequisite for gamora's `v1.3-b10-4-swarm-calibration` tag is cleared.** Specifically:
- View A lock: in decisions-log, Gate 1 PASS
- B10.2 supersession: in decisions-log, Gate 1 PASS, revised general-principle clause confirmed present
- Condition (a) "this entry landing" for the B10.4 milestone tag: **SATISFIED** once the working tree commits

The tag still requires condition (b): "Option 2 implementation + full regen confirming convergence." Per the end-of-Day-3 handoff update, gamora's B10.4 Option 2 code is complete (commits b15ecb2, 540160c; 10/10 converged). Condition (b) is SATISFIED per the gamora intermediate tag `gamora/v1.3-b10-4-option-2-impl`. The milestone tag cut requires Matt's explicit authorization per ADR-003 (milestone tags are Matt-only authority). Matt has the milestone on hold per the Day-4 dispatch; once the working tree commits, knight-rider can request Matt's authorization to release the hold.

### Drax downstream unblock

Drax's v0.7-encounter-analytics interpretation work was authored against View A as a working assumption. The View A lock is confirmed Gate 1 PASS. Drax's downstream interpretation logic is grounded. The v0.7 milestone hold can also be released by Matt once the decisions-log commits.

---

## References

- `/Users/admin/Games/reincarnated-engine/design/decisions/decisions-log.md` — lines 145-159 (2026-05-07 superseded), 958-970 (B10.2 original + status), 1024-1056 (Court), 1060-1106 (enemy viz), 1108-1128 (style register), 1132-1174 (naming triad), 1176-1214 (research.db retired), 1216-1270 (engine-balance stewardship), 1272-1299 (B10.2 supersession)
- `/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/qa/findings/2026-05-16-decisions-log-batch-gate1.md` — prior Gate 1 review; all substantive verdicts on record here
- `/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/qa/findings/2026-05-15-b10-4-option-2-and-aoe-philosophy.md` — Q2 WARN origin (general-principle clause; confirmed resolved)
- `/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/skill_handoff_2026-05-16.md` § "End-of-Day-3 update" — amendment confirmation
- `/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/qa/pending/2026-05-16-decisions-log-engine-balance-stewardship.md`
- `/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/qa/pending/2026-05-16-decisions-log-court-and-enemy-viz.md`
- `/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/qa/pending/2026-05-16-decisions-log-style-register-and-naming-triad.md`
- `/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/qa/pending/2026-05-16-decisions-log-research-db-retired.md`
