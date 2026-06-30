# Verify-then-prune — FIRST RUN on gandalf/notes — result + Matt ratification surface

> **STATUS:** WORKING-MEMORY (ratification request). This note is itself prunable once Matt rules on the prune-list below — at which point its content is spent (the rulings land in git history + the standing § 6.6 routine inherits the finding). Authored as the durable record of the first manual verify-then-prune.

**Authored:** 2026-06-30
**Author:** gandalf
**Authority:** Matt 2026-06-30 — *"…and run the verify-then-prune"* (item 4 of the 4-part execution authorization). Implements `canonical-doc-format.md § 6.3` (the 4-predicate prune-safe rule) + § 6.6 (the sweep), applied manually as the first run.
**Companion:** `2026-06-30-doc-lifecycle-governance-stress-test.md` (the system this exercises); `canonical-hygiene-audit-routine.md` (the standing routine this first-run validates).

---

## 0. Headline — the SAFE TIER IS EMPTY. Nothing was auto-pruned. Nothing was deleted.

The 4-predicate prune-safe rule, applied honestly with a cross-repo reference check **and a read-verify step**, found **zero** notes that clear the auto-prune bar. Per § 6.6 ("if the safe tier is empty, commit nothing"), **no `git rm` fired.** Every candidate surfaces below for your ratification.

**This is not the routine failing — it is the routine working, and it surfaced a real finding** (§ 5): gandalf's "coordination" notes embed load-bearing design reasoning, so the filename-class heuristic ("brief / prompt / request / pointer = ephemeral working-memory") **failed on 9 of 9** notes I read to verify. The auto-prune ceiling (ambiguity → surface, never auto-fire) held exactly as the stress-test (S1/S2) predicted.

---

## 1. Method + the partition (153 notes → 33 judgment candidates)

| Step | Filter | Count |
|---|---|---|
| Start | all notes in `agentic_orchestration/gandalf/notes/` | **153** |
| Predicate 4 — **path-cited** across BOTH repos (`reincarnated-collaboration` + `reincarnated-engine`; decisions-log lives in the engine repo) → **evidentiary, protected** | −109 | 44 |
| Predicate 1 — **non-markdown** (`.html`/`.json`/`.py`) → out of § 6 scope (seam-owner lifecycle) | −7 | 37 |
| Predicate 4 — **basename-cited** (second pass; caught the resist/proxy/path-b cluster) → protected | −4 | **33** |
| **Judgment candidates** (markdown, uncited, not-never-prune) → read-verified, classified below | | **33** |

The 109 path-cited + 4 basename-cited = **113 notes are evidentiary** (cited by decisions-log, a canonical doc, a skill, an active dispatch, or a downstream math-note). Per ruling (c) they are never auto-pruned. They are the working spine of the design record — the citation graph voted to keep them.

---

## 2. The safe-tier-empty finding — filename-class failed 9/9

I provisionally classed 9 notes as "pure coordination ephemera" (briefs/prompts/requests/pointers/winddowns) → the only plausible safe tier. Per the stress-test discipline (**never fire on appearance**), I read all 9 before any `git rm`. **All 9 carried design substance:**

| Note | What it actually carries |
|---|---|
| `descent-round4-establish-recompose-brief` | the **katabasis / withhold-the-destination** design recognition (magenta sanctum revealed on arrival, not at the threshold) |
| `combined-run-winddown` | **live** battle-sim + content-emission closure criteria + the **proxy/summoner door** (Path-B-active) |
| `gamora-brief-perception-asymmetry-sim-wiring` | a **LIVE GAP**: perception-asymmetry is designed+built+demo-wired+telemetry-schema'd but **not wired into `spatial_engine.py`**; `AOECastEvent` has no producer. Locked constants. A registered prediction. |
| `kr-session-opener-dot-investigation` | the **DoT-as-boss-bridge** hypothesis + the 3-question falsifiable diagnostic + sequencing |
| `kr-autonomous-run-kickoff-prompt` | the **three-tier authority envelope** — and its cited charter (`canonical/story/2026-06-16-engine-state-and-autonomous-run-plan.md`) **is MISSING**, so this may be the last surviving record |
| `descent-round3-galadriel-rescore-request` | the **dressed-vs-stark SHF calibration** (later codified into the scorer as the kind-aware gate) |
| `descent-round4-galadriel-establish-rescore-request` | the kind-aware-gate spec + the blue-slab-mass diagnostic |
| `spell-vfx-round1-drax-brief` | the **emanate-from-caster** spell lifecycle design (charge→release→impact→fade) |
| `seasonal-descent-session-pointer` | points at the **current active game vision** (infinite reincarnating descent) + forward-looking capacity moves |

**Filename class did not predict content class — 9/9.** A design steward's coordination *is* design transmission; the reasoning rides in the brief. The safe tier is therefore empty.

---

## 3. Judgment-tier prune-list (33 notes) — your ratification

Nothing here was touched. Lean = my recommendation; you rule.

> **⟹ RATIFICATION LANDED (Matt 2026-06-30) — the rulings below now govern; the original
> recommendation text in 3a–3f is retained as lineage (reconcile, don't amputate).**
>
> - **RAVINE ×9 (§ 3c) → PRUNED.** Matt: *"Ratify the ravine ×9."* Reference check came back
>   **clean** (all citations intra-cluster or in the two governance docs; zero external
>   evidentiary homes). Executed: `git rm` of all 9 + commit (NO push).
> - **CRYPT-VAULT ×5 → PRUNED.** Matt: *"The crypt/vault learnings can be added to the ravine
>   learnings, but the scene was cancelled."* This **moves 3 crypt notes out of KEEP** —
>   `crypt-vault-gate3-verdict-1-calibration` (was § 3d), `crypt-vault-phase1-verification-and-
>   preread` + `crypt-vault-rebuild-brief-camera-committed` (were § 3e) — **plus** the 2
>   previously citation-protected crypt notes (`crypt-vault-node-poc-brief`, `crypt-vault-node-
>   gate3-coherence-capture`). Learnings folded into the carry-forward note § 6 first. The
>   phase1 note's uncommitted `M` (the § 3e ⚠) was already committed earlier this session →
>   clean to prune. **Surfaced caveat (not silent):** `node-poc-brief` is cited by a frozen
>   2026-06-19 dispatch + that day's skill_handoff — historical point-in-time records (not
>   pruned); their refs become intentional git-lineage pointers.
> - **KING-RIG (§ 3f) → KEEP, confirmed LIVE.** Matt: *"another scene which is not cancelled…
>   a small square room with a king character. This is the live game being built, so do not
>   prune that one."* `2026-06-22-king-rig-mcp-alignment-brief.md` STAYS. (Verified it cites
>   zero crypt notes, so the crypt prune does not orphan it.)
> - **The open crypt-vault question in § 3c is RESOLVED** — Matt ruled the crypt scene
>   cancelled, so the "stays KEEP until you rule" hedge is now spent.
> - **Still awaiting:** the S15 governance refinement (§ 5a) — Matt asked to talk it through
>   in more detail (Pattern-B), so it is NOT yet entered in the stress-test record.
> - **Open recommendations untouched by this ruling:** 3a (descent-rescore ×3), 3b (spell-vfx),
>   3f remainder (orphan/handoff ×4) still await Matt's confirmation of their substance-homes.

### 3a. RECOMMEND PRUNE — descent run-to-green per-round children (3 notes) — confidence medium-high
Workstream **CLOSED** (6/6 chambers green, establish closed). All three explicitly cite the **intact** parent `2026-06-17-descent-runtogreen-log.md` as "the authority," and the calibration they carry was **codified into the scorer** (kind-aware gate). Substance is preserved upstream; these are per-round process residue.
- `2026-06-17-descent-round3-galadriel-rescore-request.md`
- `2026-06-17-descent-round4-establish-recompose-brief.md`
- `2026-06-17-descent-round4-galadriel-establish-rescore-request.md`
- **Gate on your confirmation** that the runtogreen-log + the scorer code are the retained homes (I assert they are).

### 3b. LEAN PRUNE — but closure unconfirmed (1 note)
- `2026-06-17-spell-vfx-round1-drax-brief.md` — round-1 SLICE brief; parent `2026-06-17-spell-vfx-runtogreen-log.md` (intact) holds the direction. But this is a *slice-first* brief implying a rollout; I have **not confirmed the spell-vfx rollout closed.** If complete → prune; if mid-rollout → keep. Your call.

### 3c. RECOMMEND PRUNE — Godot ravine (9 notes) — workstream CANCELLED + learnings PROMOTED — confidence high
**REVISED (Matt 2026-06-30: *"the ravine work was cancelled. But there may be some learnings there."*).** My original read here ("r3 awaiting the Matt Gate; workstream OPEN; do not prune") is **VOID** — the workstream is cancelled, not awaiting a gate. Predicate 3 (workstream-closed) now holds.

Per **promote-then-prune** (§ 5b): I extracted the load-bearing learnings — the edge-socket snap-by-construction primitive, the exemplar→seed-vary→assemble carry chain, the generate→gate→graduate loop, WFC-as-scale-path, the two-footprint rule, the 28×28 vestigial-removal category-error, the R1–R14 + NV-1…5 no-void ruleset, the tripod-gate + eye-overrides-hard-gate process, the depth-toward-the-climax beat, and the Synty/Godot asset gotchas — into a durable lineage home:
→ **`2026-06-30-ravine-cancelled-learnings-carry-forward.md`** (organized for the active seasonal-descent procgen work, gate G3, to consume).

With the substance promoted, all 9 raw iteration notes clear predicate 3. **Prune-recommended, one commit, NO push, on your word + a clean reference check** (the only remaining gate — confirm none is cited by an evidentiary home across both repos). NOT auto-rm'd: you are in live dialogue, surface-for-ratification is correct.
- `2026-06-20-enchanted-forest-ravine-plan-and-floor-sizing-research.md` · `2026-06-20-ravine-atgrade-matt-gate-package.md` · `2026-06-20-ravine-cutout-pattern-spec.md` · `2026-06-20-ravine-tripod-autonomous-run-verdict.md` · `2026-06-20-ravine-vignette-generator-spec.md` · `2026-06-21-ravine-carve-and-sculpt-spec.md` · `2026-06-21-ravine-carved-r1-matt-gate-package.md` · `2026-06-21-ravine-carved-r2-matt-gate-package.md` · `2026-06-21-ravine-carved-r3-matt-gate-package.md`
- **Open question flagged, NOT assumed:** the ravine generalized its node-schema + Gate-1 from the **crypt-vault PoC**. You cancelled *"the ravine work"* — not, explicitly, the crypt-vault prototype. The crypt notes stay **KEEP** (§ 3d/§ 3e) until you rule on whether the crypt-vault Godot prototype is also retired. The promoted methodology transfers regardless of which prototype proved it.

### 3d. RECOMMEND KEEP — verdict-class (uncited, but NO established supersession) (8 notes)
Per ruling (c), verdict/recognition notes prune only on **total-supersession + zero citations**. They are uncited, but I have **not** established total supersession for any — and one is recent + active.
- `2026-06-18-bc-coordinate-cutover-stage2-envelope-escalation-ruling.md` (connects to live engine `bc-coordinate-cutover` math-notes) · `2026-06-18-vfx-register-test-verdict-binbun-backbone.md` · `2026-06-19-boss-numbers-pre-registered-interpretation.md` · `2026-06-19-crypt-vault-gate3-verdict-1-calibration.md` · `2026-06-19-session-close-vfx-register-to-v1-incontext.md` (records a register→v1 decision) · `2026-06-19-v1-warhall-incontext-adjudication.md` · `2026-06-20-signature-ailment-emission-breadth-design-fit.md` · `2026-06-29-path-b-classification-report.md` (**recent, Path-B-active — definitely keep**)

### 3e. RECOMMEND KEEP — live status / active vision / missing-substance-home (7 notes)
- `2026-06-15-gamora-brief-perception-asymmetry-sim-wiring.md` — **a LIVE BUILD-TO-SPEC GAP** (see § 5b), not process residue
- `2026-06-21-combined-run-winddown.md` — live proxy-door + closure criteria (Path-B-active)
- `2026-06-22-seasonal-descent-session-pointer.md` — points at the current vision; recognition record intact but forward G1/G3 moves may not be
- `2026-06-16-kr-autonomous-run-kickoff-prompt.md` — **its charter is MISSING**; may be the last record of the three-tier envelope
- `2026-06-15-kr-session-opener-dot-investigation.md` — DoT-boss-bridge hypothesis; investigation ran downstream
- `2026-06-19-crypt-vault-phase1-verification-and-preread.md` — **⚠ has UNCOMMITTED modifications** (in `git status` as `M`); never prune a file being actively edited
- `2026-06-19-crypt-vault-rebuild-brief-camera-committed.md` — encodes a camera commitment

### 3f. RECOMMEND KEEP — orphan/handoff/spec (verify-then-rule) (5 notes)
Lower-confidence keeps; each needs a one-line check before any prune.
- `2026-06-09-3-kit-to-star-sign-canonical-mappings.md` — mapping data; check if it landed in the engine (if so → superseded → prunable)
- `2026-06-10-fable-5-handoff-fidelity-test-design.md` — a test-design spec
- `2026-06-15-end-to-end-pipeline-handoff-where-we-are.md` — a 2026-06-15 status snapshot (stale; lean-prunable but verify nothing unique)
- `2026-06-16-companion-gen-conformance.md` — a conformance report
- `2026-06-22-king-rig-mcp-alignment-brief.md` — king-rig MCP work; the seasonal-descent pointer says it was committed+pushed (`c205c76`) → likely spent, verify

---

## 4. Out of § 6 scope — non-markdown artifacts in the notes dir (7) — flag only

Predicate 1 excludes these (data/code/binary live under seam-owner lifecycle, not § 6). They are **clutter in gandalf's notes dir** and can be cleaned under a separate disposition if you want — but the doc-lifecycle routine does not touch them.
- `2026-05-23-geography-vs-culture-substrate-analysis.html` · `2026-05-27-cycle-13-character-analysis.html` · `2026-05-29-community-substrate-axis-expansion-and-t4-capstone-design-implications.html` · `2026-05-30-engine-state-season-003-flow-diagram.html` · `2026-05-30-physical-infrastructure-implementation-plan.html` · `2026-06-01-ia-2-phase-2-anchors-batch.json` · `generate_cycle13_character_analysis.py`

---

## 5. Governance finding — and the real lever for "tons of notes"

### 5a. Finding (S15-class — validates the system, refines the expectation)
**Design-steward "coordination" notes embed load-bearing design reasoning, so the filename-class heuristic that predicts "coordination artifact = ephemeral" FAILS for this author class.** Read-verification nearly always surfaces substance → judgment tier. Operational consequence: **for gandalf-authored notes the safe tier is effectively empty**; the standing § 6.6 routine should not expect filename-based auto-prunes from gandalf — it must read-verify, and read-verification will route to judgment tier almost every time.

This **validates** the system (the auto-prune ceiling + the read-verify step caught it; nothing was wrongly deleted) and **refines** the operational expectation. Proposed as a new stress-test scenario **S15** and a § 6.6 note. *Per the system's own discipline, I do not unilaterally amend ratified § 6 — surfaced for your ruling.*

### 5b. The real lever — promote-then-prune, not a bigger broom
The notes accumulate because **design recognitions live in notes instead of being promoted to canon.** Auto-prune can't fix that (the substance is load-bearing → it can't be deleted). The two real fixes:
1. **System A (propagation) is the cleanup engine.** When a recognition lands in `canonical/` (or a tracker delta), the note becomes a redundant pointer — and *then* it clears predicate 3 (totally-superseded) and becomes prunable. The `seasonal-descent-session-pointer` is the model: its substance IS canonized (the recognition record), so once you confirm the forward-moves are captured, it prunes cleanly. **Prune follows promotion.**
2. **Authoring discipline.** Prefer a canonical update or a `Tracker-delta:` over a fresh coordination note where the content is design-substance. Fewer notes that carry load-bearing reasoning = fewer judgment-tier residues later.
3. **One concrete build-to-spec item surfaced by this sweep:** `gamora-brief-perception-asymmetry-sim-wiring` documents a designed+built mechanic **not wired into the spatial sim** — that is a GAP-TO-CLOSE (no-deferral directive), and belongs as a row in the engine tracker, not as a prune candidate.

---

## 6. What fired vs what awaits you

- **PRUNED on Matt's 2026-06-30 ratification (`git rm` + commit, NO push):** **14 notes** —
  the Godot ravine ×9 (§ 3c) + the crypt-vault ×5 (cancelled scene; learnings promoted to
  `2026-06-30-ravine-cancelled-learnings-carry-forward.md` § 6 first). Reference checks clean
  (ravine: all intra-cluster/governance; crypt: intra-cluster + one surfaced historical-
  dispatch caveat on `node-poc-brief`). **KING-RIG kept (LIVE).**
- **Auto-pruned without ratification (git rm):** still **NOTHING** — the 14 above fired on
  Matt's explicit word, not the auto-prune path. The safe-tier-empty finding stands.
- **Awaiting Matt's confirmation of substance-homes (NOT yet pruned):**
  - **3a — descent-rescore ×3** (workstream closed; calibration codified into the scorer).
  - **3b — spell-vfx round-1 brief** (confirm the rollout closed).
  - **3f — orphan/handoff ×4** (one-line check each).
- **Awaiting Matt's ruling (Pattern-B dialogue):** the **S15 governance refinement** (§ 5a) —
  Matt asked to talk it through before it enters the stress-test record.
- **Pushed:** nothing. The prune commit is local; 14 notes deleted from the tree, learnings
  banked in the carry-forward note, king-rig retained.

---

**Tracker-delta:** ENGINE tracker — add a build-vs-spec GAP row: *perception-asymmetry (player-favoring near-miss, two-layer model) is designed + foundation-built + demo-wired + telemetry-schema'd but NOT wired into `spatial_engine.py`; `AOECastEvent` has no producer* (source: `gandalf/notes/2026-06-15-gamora-brief-perception-asymmetry-sim-wiring.md`). I will consolidate this into `current-to-end-state-engine.md` in the #12 tracker-delta pass.

**Signed:** gandalf, 2026-06-30. First verify-then-prune: safe tier empty (filename-class failed 9/9 on read), nothing deleted, the citation graph protected 113 notes, 33 surface for ratification with the descent-rescore trio as the one confident prune-lean — and the real finding is that prune follows promotion, not a bigger broom.
