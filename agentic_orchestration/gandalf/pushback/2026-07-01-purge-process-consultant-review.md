# Purge-Process Consultant Review — the canonical doc-purge, audited from outside

**STATUS:** PUSHBACK MEMORANDUM / CONSULTANT REVIEW — awaiting Matt ruling on §9 (Q6 process revision; Q5 slate).
**Author:** gandalf, 2026-07-01 — written under an explicit Matt mandate to review the team's purge work *"with the lens of hired contractor… sufficiently unbiased."* This memo judges machinery my own prior sessions built (`⚠ SWITCH: SPEC-AUTHOR → DRIFT-CRITIC`).
**Method:** session-start ritual per OP §1; full read of the fold-map ledger, both trackers, both spec-folder indexes, the decision queue, the prior-session handoff; plus three corpus-wide scans run this session — (i) live inbound-reference scan of all 71 `canonical/story/` docs + 14 numbered docs against 655 live surfaces (specs, trackers, OPs, skills, CLAUDE.md, engine `src/`+`design/`, godot repo), (ii) STATUS census, (iii) Matt-ruling-line density scan.
**Standing order under review (Matt, unrescinded):** *"I am 100% committed to the purge and I'm prioritizing it until completed."* End-state: no loose `canonical/NN-*.md` except a thin router; `canonical/story/` retired to zero files; three surviving homes.

---

## 1. Credit first — what the prior work got right

A fair audit starts here, because the fix in §5 keeps these:

1. **The three-home target structure is correct.** END-STATE specs (`reap-die-rise-{story,engine}/`) / DELTA trackers (`current-to-end-state/`) / decision queue (`matt_decision_needed/`) is a clean separation, already standing, already routing new work correctly.
2. **Tranche 1 was clean and fast** — 13 live kills + 98 already-demoted swept in one pass, zero regrets since.
3. **The season-archive HALT was a genuine catch.** Live engine code (`kit_space_emitter.py`, `kit_space_skill_naming.py`, `ws1a4_lite_flavor_judgment.py`, `data/kit_space/`, `CHRONICLE_SCHEMA.md`) cites that doc's §3.2–§3.4 as the canonical commitment behind a live subsystem. Deleting it blind would have orphaned real architecture. The halt was right.
4. **The fit-audit slate's design verdicts are sound** (§6 endorses all seven rows).
5. **The descent-trio and anchor folds were genuine, lossless consolidations.**

The problem is not that the team did bad work. The problem is that the *process* the good work spawned now optimizes for preservation while calling itself a purge.

---

## 2. Core finding — the purge has inverted into a preservation program

| # | Finding | Evidence |
|---|---|---|
| **F1** | **Trajectory misses the mandate by an order of magnitude.** | End-state = 0 loose docs. Current = 71 story docs (30,203 L) + 14 numbered (9,911 L) ≈ **40k lines**. Tranche-3 net removal: **10 docs across ~3 sessions.** At observed pace with per-doc capture-checks: **15–25 more sessions.** |
| **F2** | **The corpus is 100% self-certified load-bearing.** | STATUS census: **71/71** survivors stamp themselves CURRENT / CANONICAL / RATIFIED (1 partial-superseded banner). Every stamp was issued *by the doc's author, at authoring time, never re-audited.* 22 stamps read "load-bearing as of **2026-05-23**" — five weeks, one retitle, one genre-frame replacement, and one release-model retirement ago. Self-certification is not audit. |
| **F3** | **The prune engine's first live run deleted nothing.** | verify-then-prune first run: 153 candidate notes → **113 declared "evidentiary" (74%), 33 routed to ratification, 0 deleted.** A purge instrument that returns 0% delete on first firing is a preservation instrument. |
| **F4** | **Process mass now outgrows purge mass.** | Tranche-3 window shipped: doc-lifecycle governance §6 + a 14-scenario stress-test + a standing hygiene Routine (blocked on environment) + per-doc capture-check protocol + a cross-seam handoff brief — while removing 10 docs. The season-archive banner commit (`5043890`): **6 files changed, +55/−7, zero files removed.** The halt was correct; the *shape* of a session's throughput — ledger-tending — is the tell. |
| **F5** | **One doc's disposition updates 5–6 bookkeeping surfaces.** | fold-map §6.5 + engine 00-index + story 00-index + story-tracker PART C + engine-tracker PART II + the session handoff all mirror per-doc state. Overhead per doc ≈ the doc. |
| **F6** | **Ratification round-trips have become the deferral mechanism.** | Matt has ruled the strategic question repeatedly — *"100% committed"*; *"all v1 isekai gone"*; *"(b) heavyweight-fold… Please begin."* Yet finer-grained approval requests keep queuing (fit-audit slate, cut-line confirm, 33-note ratification list) — and the slate was **never filed in `matt_decision_needed/`**, the queue Matt built for exactly this. Each round-trip costs a session and re-arms every bias in §3. |
| **F7** | **The purge's own bookkeeping has drifted.** | Both spec-folder 00-indexes + handoff §7 Step 8 state the authoritative spec "still lives in `canonical/reap-die-rise/`" — a folder **dissolved in commit `6b9d6d1`** (verified via `git log --follow`). Five mirrored ledgers produce exactly this failure. |

---

## 3. Bias audit — why a 100%-committed team cannot delete

- **B1 — Endowment.** The authors are purging their own corpus. Every STATUS: CURRENT is the author grading the author. No third-party re-audit has ever fired.
- **B2 — Mispriced loss-asymmetry (the load-bearing bias).** Every guardrail prices a wrong DELETE as catastrophic and a wrong KEEP as free. **Under git, the prices are inverted:** a wrong delete costs one `git show` (seconds, lossless); a wrong keep costs a perpetual attention tax on every future session, drift risk (F7 is the proof), and the exact pain Matt named. The machinery's own motto is "git holds all lineage" — but it behaves as if version control doesn't exist. This is the single deepest defect.
- **B3 — Over-generalized halt.** One correct catch (a code-cited doc) was generalized into per-doc archaeology across all 85 units. The correct generalization was narrow: *grep for live citers before rm* — and it batches. This session's corpus-wide scan ran in ~30 seconds and produced what the current process buys one doc per session.
- **B4 — Fold-scope inflation.** Strategy (b) as practiced makes every deletion hostage to authoring the complete v2 engine spec first. "Clean the tree" became "write the spec, then clean the tree" — so neither happens.
- **B5 — Approval-seeking as deferral.** Fine-grained ratification slates feel like diligence and function as postponement.

Diablo III shipped its auction house because everyone kept ratifying the sunk work instead of pricing what players actually paid. Same failure, smaller theater: the team keeps ratifying the archive's self-worth instead of pricing the attention it costs.

---

## 4. Scan evidence (the data the fix stands on)

Scan artifacts: `/tmp/story_names.txt`, `/tmp/live_surfaces.txt` (655 files), `/tmp/story_hits.txt`. Reproducible in one command; should be re-run at each batch head.

- **16 / 71 story docs have ZERO live-surface citations by filename** — mechanically safe now: the 5 marginal-lineage dispositions, `variant-cluster-policy-assignments`, `ab-comparison-protocol-cycle-14-close`, `autonomous-fire-prompt-template`, `weapon-substrate-conclusion-declaration`, `designer-writes-substrate-…-principle`¹, `v1-1-plus-design-discipline-recognitions`¹, `stat-derivation-from-bc-convergence`, `seasonal-hero-h-5-hybrid-spec`, `arpg-physical-magical-ratio-baseline`, `engine-architecture-canonical-synthesis`, `gear-spec-element-flavor-manifest-design-half`. *(¹ = principle docs: harvest to jack-ryan disciplines per fold-map B5 routing, then delete.)*
- **Genuinely embedded docs (move / re-point — NOT archaeology):** `qd-engine-bc-axes-lock` (**25 live citers**: 5 engine code files, decisions-log, 12+ math docs, the substrate-vector-cheatsheet skill) · `gauntlet-metrics-as-provisional-hypotheses` (engineering-disciplines + decisions-log + `phase7_verdict.py`) · `style-register` (14, session-start read) · `2026-06-02-season-archive-…` (bannered, held on the kit-space engine question — correctly) · `autonomous-run-plan-v2` (13 citers, but ALL are MIGRATION/AGENT_STATE/math-lineage surfaces — historical-record class; confirm run spent → delete).
- **The sole-carrier risk is bounded and greppable:** **45/71 docs carry ≥1 Matt-ruling line; 173 ruling-flavored lines corpus-wide.** The feared "we'll lose a Matt ruling" scenario lives in 173 lines, not 30,203. One harvest session, deduped against `decisions-log.md` (rulings' canonical home) and story-tracker PART A. **No new ledger instrument needed.**

---

## 5. Recommendation — (b′) pull-based fold *(supersedes strict-(b) practice; Q6, needs Matt)*

**The rule inverts the burden of proof: DEFAULT-DELETE.** A doc earns survival only through one of three exemptions:

| Exemption | Meaning | Disposition |
|---|---|---|
| **E1 — ruling-carrier** | sole carrier of a Matt ruling still in force | harvest the line → decisions-log (engine) / tracker PART A (story) → delete |
| **E2 — live-cited** | cited by live code / OP / skill / spec | move-whole into the spec folder + re-point citers (or re-point to git where the citer already embodies the content) |
| **E3 — spec-member** | already lives in a spec folder | keep; distill in place |

**Mechanics:**
1. **Batch inbound-ref scan replaces per-doc capture-checks.** The tooling now exists; re-run per batch head.
2. **Move-whole is a legitimate fold** for run-invariant load-bearing docs — their distill ratio approaches 1.0, and re-transcribing 400KB of balance math invites transcription error (the exact hazard Disciplines #1/#8 exist for). **Distillation becomes PULL-based:** a moved doc is tightened when engine work next touches it — not as a pre-deletion authoring program.
3. **Specialist confirmation inverts.** Each seam owner receives ONE list — *"these docs claiming your seam delete next batch; name any constraint your live code does not already embody."* Silence within a session = consent. This replaces the B4/B5 per-doc cross-seam capture-check briefs.
4. **Bookkeeping collapses to ONE ledger** (the fold-map note) + the decision queue. The 00-indexes stop mirroring per-doc state (F7 is what mirroring buys).

**The honest cost:** `reap-die-rise-engine/` lands at ~20 docs, not the aspirational 7–10, converging to tight over time. **What it buys:** the end-state tree in **~3–4 sessions instead of 15–25**, with both real risks (E1/E2) guarded by cheap mechanized checks instead of ceremony. The tight-spec aesthetic was (b)'s means; the clean tree is the mandate's end. (b′) trades the means to hit the end.

---

## 6. The fit-audit slate (Q5) — independent design read: **endorse all seven rows**

| Row | Verdict + consultant rationale |
|---|---|
| Projection: kill remote-avatar, keep transition ritual | **Endorse.** Remote-avatar mediation dilutes the title's second word — if you're projecting, dying is disconnection, not death. You ARE the reaper who descends. |
| Hall of Heroes → merge into Grimoire | **Endorse.** Two collections of claimed souls is one collection with a redundancy bug. §11's book-of-claimed-souls already IS the death-faith Hall. (Hades earns Codex+Mirror by splitting *function*; these two don't split.) |
| Cosmograph: kill content-browse, park night-sky presentation | **Endorse.** A browsable possibility-sky is a menu wearing fiction's clothes, and it fights the descent compulsion loop — PoE's Atlas works because it IS the run-selector, not a gallery beside it. The patron's night-sky-of-reaped-souls as *presentation* of the Grimoire keeps the mood at zero systems cost. |
| Molting: keep-reskin | **Endorse — strongest fit on the slate.** Molt is die/rise enacted at the form level; it's the title as mechanic. |
| Temporal dyad: keep companion, kill past/present/future framing | **Endorse.** The future corner was the retired spirit guide; a grimoire-summoned claimed soul is cleaner and already spec'd (§13). |
| Creation moment → dark sacrament | **Endorse.** Cheap reskin, high atmosphere; the contract-moment that a later manufactured-rebellion reveal recontextualizes (Bloodborne's blood ministration is the working precedent). |
| Engine §3.2/§3.3/§3.4: keep, pending engine call | **Endorse** — correct routing; the open question is star-lord/rocket's, not a fit question. |

**One refinement:** the Hall→Grimoire merge resolves only B1's *collection* half; the run-persistence core of B1 (what survives a run) stays OPEN — the tracker holds it correctly. Ruling the slate does not close B1.

---

## 7. Batch plan under (b′)

- **Batch 1** *(fires on Q6 ratification; ~1 session):* delete the 16 zero-ref docs (principles harvested to jack-ryan routing first) + Cluster E remainder (minus `atomic-substrate-registry`; flag elrond re: MIGRATION.md lines 385/413/565) + Cluster F non-keepers + the 4 held-back Cluster-B docs after citer-checks (`autonomous-run-plan-v2` confirmed spent) · run the **173-line rulings harvest** diffed against decisions-log. **≈ 30–35 deletions.**
- **Batch 2** *(~1–2 sessions):* numbered spine — **move-whole** {38, 39, 40, 42, 46, 47, 50, 51} → `reap-die-rise-engine/` with re-points; **verify-delete** {41 after 40 moves, 43, 44, 45 vs code, 49} ; **harvest-delete** 37 (zero refs; 1-page two-products essence → engine 00-index preamble). Cluster D: move-whole the code-cited, delete the v1-superseded per the fold-map's own three-way split; **ONE confirmation list** to rocket/gamora/star-lord via KR.
- **Batch 3** *(~1 session):* Cluster C per the Q5 ruling + `story-expansion.md` §12 revision · style-register → spec folder + re-points · CLAUDE.md "Where to find things" rewrite (B6) · final sweep. If the kit-space engine question is still open, the bannered season-archive doc **moves to `reap-die-rise-engine/` as a bannered annex** so `canonical/story/` still retires on schedule.
- **Exit test:** `canonical/` = router + 4 folders; `canonical/story/` absent; every deletion one `git show` from recovery.

---

## 8. Self-audit

This review judges machinery my own prior sessions built. Two temptations, named: *defend it* (continuity bias) and *raze it for effect* (decisiveness theater). The guards: every finding above is scan-derived, not vibes-derived; and the fix retains hard protection for the only two loss modes that are real (E1 ruling-carriers, E2 live-citers) — as thirty-second batch checks instead of multi-session rites. The season-archive halt stays honored; its lesson is a grep, not a liturgy.

---

## 9. What needs Matt (filed as Q5/Q6 in `canonical/matt_decision_needed/`)

1. **Q5 — rule the fit-audit slate** (§6; gates 4 story docs + the §12 revision).
2. **Q6 — ratify (b′)** (§5; supersedes strict-(b) *practice* — same end-state, same three homes, ~10% of the effort). On yes, Batch 1 fires same-session.
3. **Push-auth** when batches land (commits auto-fire in scope; push stays Matt-gated).

---

**Signed:** gandalf, 2026-07-01 — story-and-design steward, wearing the contractor's plain grey. A tree that needs five ledgers to delete one file has built a shrine around its own attic. Git already keeps every road we ever walked; the working tree only owes the traveler the road ahead.
