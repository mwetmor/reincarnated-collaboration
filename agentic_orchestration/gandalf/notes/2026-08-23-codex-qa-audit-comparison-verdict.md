# Codex QA Audit vs Project State — Comparison Verdict + Recommendation (2026-08-23)

> **STATUS:** VERDICT OF RECORD — gandalf, DRIFT-CRITIC (comparison) → CANON-STEWARD (curation).
> **Mandate (Matt, verbatim intent):** compare the two Codex Mac QA audit docs against the entire RDR work tree as of 2026-08-23; examine the ongoing gandalf session; then "do an ultra think to provide your own recommendation" toward "updating/upgrading/improving our working process/plan/scope/efficiency."
> **Audit docs:** `/Users/admin/Games/codex-project-review/PROJECT_END_TO_END_SUMMARY_2026-08-16.md` + `PROJECT_STRATEGIC_RECOMMENDATIONS_2026-08-16.md` (both read in full).
> **Method:** house discipline — every load-bearing Codex claim verified against the machine (files, git heads, greps), never trusted as prose. Both repo heads (engine `c77934a3`, godot `d252d0c`) are UNMOVED since Codex's 2026-08-16 snapshot → its build-state reads are CURRENT, not stale; its *ruling-lattice* reads are partial (it audited the workspace, not the governance layer).

---

## §1 — Verdict in one paragraph

The Codex audit is a competent outside-in read whose gap list almost perfectly REPRODUCES our own trackers — which is independent confirmation that the tracker discipline is honest, and simultaneously means most of its findings buy us nothing new. It lands **one genuinely new catch** (Synty July-2026 license/AI-terms exposure — nothing in canon tracks pack-level entitlements while the ensemble pipeline plans a third-party image→3D vendor call), **one real strategic tension** (its "validated player loop first" restructure collides with three standing Matt rulings it never saw — the FULL-RUN PIVOT, GATE1, zero-hand-authored-content — but the underlying risk it names is true and our own canon names the same test), and **one same-day internal convergence** (its "when does reference replication stop paying" question = Q59, filed from the inside on the identical date). Its stop/continue framework is largely convergent with work the other gandalf session curated into `workflow-upgrades.md` U-1..U-8 the same day. Recommendation register at §5.

## §2 — Classification of findings

### Class 1 — CONFIRMED, and we already knew (tracker mirrors)
Codex END_TO_END §11.3 runtime gaps ≈ game tracker PART B rows nearly 1:1 — B1 (camera ratification caveat = our F-5), B2 (first floor not authored), B4 (style-register unapplied), B5 (Binding-Rite-LITE absent). §23's "product proof lags infrastructure" ≈ one-realm-mvp-scope §8's own "§20d parametric-verb condition — THE test." **Audit value: confirmation, not discovery.** An external auditor with full workspace access could not find a build gap our trackers had not already named.

### Class 2 — CONFIRMED, already queued (convergences)
- **Hardware blind spot / Windows export** (Codex P0) → `matt_to_do/` **T2** (2026-07-02) + drax proxy Gate A (`reincarnated-godot/MINSPEC_CADENCE.md`, `scripts/run_minspec.sh`). Codex adds "Steam Next Fest is one-shot" urgency framing — real, already gated (D10 Gate B "must run before Next Fest").
- **Storage / observability / artifact sprawl** → U-1 (flight recorder + board) + U-2 (retrospective mining), curated the SAME DAY by the parallel gandalf session. Two independent audits, same levers.
- **Automation caution / test strategy** → software-factory delta GL-1…GL-19 + EL-1…EL-5 never-automate rows (2026-08-10) already codify the boundary Codex gestures at.
- **Untracked-file counts** (164/277/230 — verified accurate): mostly galadriel evidence-capture pattern; minor hygiene, folds into U-1/U-2 rather than meriting its own item.

### Class 3 — GENUINELY NEW (the audit's catches)
1. **Synty July-2026 license terms as an AI/editor stop-gate — THE catch.** Verified against canon 2026-08-23: `business-platform-strategy.md:52` is the ONLY license-shape sentence in the whole canon (strategy-level: shipped-game use vs redistribution — predates any AI-terms question); `ensemble-asset-pipeline-spec.md` contains ZERO license/EULA/clearance/entitlement rows while its Stage-4 plans an image→3D vendor call (Tripo slot) on Synty-derived captures. No pack-level ledger, no entitlement classes, no written clarification anywhere. Codex's required-actions (pack ledger; written clarification request; entitlement classes `game_only` / `ai_input_allowed` / …) adopt nearly as-written. → **U-9** + **T18**. *Caveat carried into the item: Codex's July-2026 EULA-revision claim itself needs primary-source verification (legolas) — we adopt the exposure, not the unverified citation.*
2. **Contract proliferation as a NAMED pattern** (Codex §23 → §7 single-versioned-bundle-contract). Partially new: our contracts are individually strong (baton v1 + GL-6..GL-12 law, export bundle, atlas manifest, receipts schema) but there is no versioned INDEX. → **U-10**, gated on star-lord/KR concurrence.

### Class 4 — WRONG or STALE in Codex
- **Market title:** both docs use "Reap. Die. Rise." as the product title — RETIRED 2026-07-21 (story tracker A1; successor gated at Q37; "RDR" internal codename only). Cosmetic, but an **import guard** is warranted: nobody copies Codex prose into canon carrying the dead title.
- **"Doc drift" risk:** aimed at a shape the 2026-07-01 canon reorg + §4.8 sync-walk already answered. Residual truth is the next line:
- **Identity-surface staleness — factually right, inferentially wrong:** `project.godot` main_scene = `sidekick_test.tscn` (verified line 15) + README "throwaway Phase 0 spike" (verified). The build is far beyond both; a cold reader (as Codex was) mis-infers repo maturity from them. Cheap drax fix. The finding is really "identity surfaces lie about the build," not "the build is a spike."
- **Governance blindness (structural, not a specific error):** Codex never mentions GATE1, the FULL-RUN PIVOT, the Matt queues, the roster-of-record, or the ruling lattice. Its recommendations are computed against a project WITHOUT its own law. This is why Class-5 exists.

### Class 5 — THE STRATEGIC FORK (the tension worth Matt's ruling) → Q60
Codex headline: *"Validated player loop first; enabling engine second; scale third"* → Route A Golden Path Slice (8–12 min handcrafted, 4 kits, 6 weeks, Windows export, 10 blind playtests, 30/60/90 gates). This collides with three standing rulings Codex never saw: **(i)** FULL-RUN PIVOT 2026-07-08 — "sprint-to-demo" RETIRED as scope license; **(ii)** surface-ledger **GATE1 CLOSED at 12✓/20** — demo assembly is gated and Matt closes rows; **(iii)** zero hand-authored SHIPPED content + the One-Realm 25–27 min denominator.

**DRIFT-CRITIC verdict:** Route A as written = REJECT — it re-litigates a settled Matt ruling on a stale premise, and the pivot's own rationale (slice-first produces *unrepresentative* proof) stands unrefuted. **BUT the underlying risk is TRUE and internally attested:** no human has played the loop end-to-end; the proof-of-fun evidence class is empty; EL-5 already names playtest-readiness as a Matt-hands milestone gate with no scheduled position. The honest synthesis is *"the risk is real; the remedy is wrong; define the fun-proof INSIDE the full-emission architecture."* → filed as **Q60** (options A/B/C, lean B — an explicit named GATE-FUN whose proof artifact is emission output only, with GATE1's remaining rows sequenced by fun-proof criticality). Decision-shaped per ELICIT-don't-IMPOSE; Matt rules.

### Class 6 — Internal-mirror findings (the ongoing-session exam, per Matt's directive)
Transcript `5bd7f4ca…` mined (background Explore, §4.10 recon exception, evidence-only):
- **State:** LIVE; awaiting Matt's ruling on the VFX referent-corpus proposal (Grim Dawn oracle-video screenshots as Judge-To targets). One commit: `f34ff83f` = `workflow-upgrades.md` (U-1..U-8).
- **Convergence signal:** its U-1..U-8 and Codex's §17/§19 overlap heavily (observability, cost attribution, cross-vendor judge). Two independent same-day upgrade passes converging on the same levers = the levers are real.
- **Gap flagged (not repaired — its lane):** `workflow-upgrades.md` session-lineage line cites *"Verdicts of record: `gandalf/notes/` this date"* — **no such notes exist.** The session said "I'll bank this verdict as a note" and did not. Repair path: that session writes its two banked notes (Codex seam-substitution review; Godot AI-tooling review) OR amends the lineage line to cite the doc's own items (U-4/U-7 ARE the verdicts). Not fabricated here; this note records the flag. *Process moral for U-5: promised-artifact tracking is precisely what a flight recorder catches.*
- **Q59 ripeness:** Codex (outside-in, §24) and the SIM-ARC handoff (inside-out, same date 2026-08-16) both arrive at "when does reference-replication stop paying marginal value." Two vantage points, one question, one open row. Q59 is ripe for ruling; the handoff already carries the conductor lean ((ii) parallel-PROVISIONAL, pinned to sibling digest `20b05cb4…`).

## §3 — Recommendation register (what was filed, where)

| # | Item | Filed |
|---|---|---|
| R1 | **Synty pack-level license ledger + clearance stop-gate** (+ primary-source verification of the July-2026 terms) | `workflow-upgrades.md` **U-9** |
| R2 | **Synty written clarification request** (account-holder correspondence — Matt's hands) | `matt_to_do/` **T18** |
| R3 | **Fun-proof placement fork** (A hold / B named GATE-FUN inside full-emission, lean / C Codex Route A, lean-against) | `matt_decision_needed/` **Q60** |
| R4 | **Identity-surface staleness fix** — `project.godot` main_scene + godot README | drax-seam one-liner; KR sequences (recorded here; no dispatch authored by gandalf) |
| R5 | **Q59 ripeness nudge** — external+internal convergence noted on the open row | this note §2 Class 6 (no new artifact; Q59 row already carries the fork) |
| R6 | **Contract-index consolidation candidate** | `workflow-upgrades.md` **U-10** (gated on star-lord/KR concurrence) |
| R7 | **Import guard** — Codex docs carry the retired title; quote with care | this note §2 Class 4 |
| R8 | **Dangling verdicts-of-record flag** → live session repairs (write notes or amend lineage) | this note §2 Class 6 |

## §4 — What was NOT adopted, and why
- **Codex Route A restructure** (Golden Path Slice as program-of-record): rejected at Class 5 — surfaced instead as Q60 option C with lean-against, because retiring it silently would hide a real fork from Matt.
- **DSH / third-party router:** already REJECTED on machine evidence by the parallel session (U-4: not installed, misidentified, duplicates the factory harness); the seam-substitution doc's G-S0–G-S6 gates were adopted, the router was not. Nothing in the Codex QA docs re-opens that.
- **30/60/90-day calendar gates:** calendar-relative framing; this project runs workstream-relative gates (GATE1 rows, ledger closures, empirical criteria). The *content* of those gates is absorbed into Q60/U-9; the calendar shape is not.

---

**Signed:** gandalf — DRIFT-CRITIC (comparison, §2) · CANON-STEWARD (curation, §3) · ELICITOR (Q60 shape). 2026-08-23.
