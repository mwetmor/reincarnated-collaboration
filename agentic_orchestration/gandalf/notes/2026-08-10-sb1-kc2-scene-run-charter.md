# SB-1 — SCENE-BUILD 1: the KC2 baton scene · the factory's founding run

**Date:** 2026-08-10 · **Conductor:** gandalf (`RUN-CONDUCTOR` — charter author conducts; intent
residency per `desirable-run-pattern.md` § 2 el. 3)
**Status:** CHARTERED, **NOT LAUNCHED** — launch gate at § 11. Veto window opens at this commit.
**Pattern compliance:** charter lands as its OWN COMMIT before any build cell fires (CL-8).
**Law:** `operating-procedures/run-minted-law.md` binds throughout — GL (drax cells), FG (gates),
CL (conduct), EL (the fence). Cited by ID below, not restated.

---

## 0 · Intent sentence

> Build the Godot scene that **faithfully reproduces run `E-s09-cp150` from the baton alone** —
> reproduce first, perturb never (this run) — with the factory spine absorbing the run's
> mechanical cells as its founding workload; judged by the gate wall for coverage and semantics,
> and by **Matt's eye at three pre-registered checkpoints** for whether it reads right.

Dual mission, one primary: **the scene is the deliverable; the factory absorption is the rider.**
If the rider fails, the scene does not die with it (§ 4 fallback).

## 1 · Substrate (bounded, frozen at launch — F1 ✓)

| Item | Pin |
|---|---|
| **The baton** | `reincarnated-engine/src/reincarnated/output/kc2-baton-v1-E-s09-cp150-20260809_052836.json` @ SHA-256 `d7ecd866ac45ec9647ca3d4f7850c41f6a7654e718451d9e5c38ccdb59b8d5aa` — verify before load (GL-6/FG-7); 344 actors · 20 waves · 1,900 event rows · 3,732 track samples · 1,003 path knots |
| **The handoff** | `gandalf/notes/2026-08-09-kc2-godot-handoff.md` — Rider-1 verbatim + ten consumer semantics (now law: GL-6…GL-12) |
| **Reference loader** | `export/baton_v1_stub_consumer.py` — the executable reading; the scene loader is judged differentially against it |
| **The law** | `run-minted-law.md` GL-1…19 · FG catalogue · CL · EL |
| **Locked grammar** | `current-to-end-state-game.md` PART A (Matt-signed constants live THERE — pointed at, never copied) |
| **Godot repo** | `~/Games/reincarnated-godot/` at the HEAD recorded in ledger row L-0 at launch |
| **EXCLUDED** | Threat-grammar companions (Rider-2 territory) · engine tree (read-only, FG-17 protected) · any perturbation of the specified run |

Substrate cannot move mid-run (CL-6): the baton is an emitted artifact, digest-pinned.

## 2 · Target-state (decidable — F2 ✓) and the rubric diff

Pre-registered predicate, in gate order (**coverage before accuracy** — pattern § 6 obs. 1,
KIT-FIDELITY's paid-for lesson):

| Gate | Predicate | Decider |
|---|---|---|
| **G-COV** | Watched-surface coverage: 344/344 actors instantiated · 20/20 waves · player track driven from all 3,732 samples · 1,003 knots interpolated per GL-7 · every event row consumed or explicitly binned (FG-13 need-list from the baton's own event vocabulary) · summons present with DECLARED-UNDEFINED motion (GL-12) | mechanical |
| **G-SEM** | The ten semantics hold in the loader, differentially vs the stub consumer: digest-verify (GL-6) · no hit-test at `path[0]` (GL-8) · BOX scatter (GL-9) · wire constants used, never re-derived (GL-10/11) · absences declared, never filled (GL-12) | mechanical |
| **G-DET** | Scene-sim replay determinism: two runs of the identical scene config produce identical event/position digests (FG-10), layer DECLARED. **Render-pixel determinism NOT claimed** — the N3 term is open (§ 10); the assertion states the layer it covers, per FG-10's rider | mechanical |
| **G-WATCH** | Promoted watch artifact(s): temp-name render → ffprobe-verify → promote (FG-9); digest recorded; frames pruned (FG-12) | mechanical |
| **G-EYE-A/B/C** | Three owner-eye checkpoints (§ 6) at Matt's word | **Matt** |
| **G-FACT** (rider) | ≥3 mechanical cell classes (digest / media / test-wall) executed via `factory run` with receipts + a generated run report | mechanical, **honorable-fail permitted** |

**Rubric diff (pattern § 6 obs. 3 — what the predicate set does NOT capture, said out loud):**
(1) *"does it read right"* is NOT in the mechanical gates — it lives ONLY at G-EYE, which is why
G-EYE is a gate and not a briefing (EL-1); (2) **playtest-readiness is explicitly OUT** — a
milestone at Matt's hands later, never this run's predicate (EL-4); (3) *combat FEEL* is
structurally incomplete under Rider-1 (no attack-timing grammar) — the divergence is DECLARED,
and judging feel-completeness against this run is pre-registered as unfair until Rider-2 lands.

## 3 · Fit test (F1–F4 walked)

- **F1 enumerable ✓** — § 1 table: countable, listable, diffable.
- **F2 decidable ✓** — § 2: mechanical gates + judgment converted to named Matt checkpoints.
- **F3 pre-drainable ✓** — § 5 fork table: five forks drained to leans; residuals are
  reasoning-boundaries (presentation grammar against locked PART A + GL-law).
- **F4 authority-resident ✓** — presentation grammar is the conductor's SCENEWRIGHT seam;
  commitment items (§ 6, § 8) HALT.

## 4 · The factory-founding rider and its honorable fallback

The spine (`agentic_orchestration/factory/`) runs SB-1's mechanical cells: digest gate, ffprobe
promotion, headless test wall — CL-1's split cell in factory form (*the mechanical leg is a spine
phase, not an agent turn*). This discharges Spec A § 11 acceptance **on real work**, and SB-1's
receipts become the first of the two workflows Spec B's Tier-2 build gate counts.

**Serviceability precondition:** the spine is used only after (a) the Gate-2 ladder closes and
(b) the conductor's DRIFT-CRITIC re-verdict on the final state (folding the v1 FAITHFUL-WITH-DRIFT
verdict + all rounds) passes. **Honorable fallback (pre-registered):** if either fails at launch
— or the spine faults mid-run — SB-1 **decouples and proceeds conductor-run** (BR-2 practice:
agent edits, conductor renders, CL-1 classic form); the factory port converts to a post-hoc lap.
G-FACT then closes as a FINDING, not a failure of SB-1. The scene never waits on its own tooling.

## 5 · Pre-drained forks — rulings-at-launch, ALL veto-open (F3)

| # | Fork | Ruling-at-launch (lean) |
|---|---|---|
| **K-1** | **Melee/attack presentation under Rider-1 absence** (the BR-3 §3 design call, inherited) | Impact-anchored only: attack anims key to the damage-emission tick (GL-19), arriving-damage channel dresses the hit (GL-15). **No wind-up, telegraph, or cadence is fabricated** — back-timing a wind-up from an impact IS fabricating timing grammar (GL-12). The abruptness is the honest declared state; Rider-2 exists to fix it. |
| **K-2** | **Arena dressing** (geometry is baton-truth; dress is scene-side) | Crucible-adjacent arena register per the 2026-08-01 render-exhibit ruling; dress from the Synty set under GL-17 (reference governs frame/layout/ornament/palette — never copy). Floor-mesh footprint clips telegraph-class ground FX (GL-13). |
| **K-3** | **Player spin presentation** (heading `0`, DECLARED-NON-SEMANTIC; EoR is a spin channel) | Conductor rules the channel→heading mapping at the cell; locomotion from kinematics (GL-19); spin rate reads as continuous at watch scale (GL-16 discipline: judge at watch distance). |
| **K-4** | **Summons presentation** (no path — R-L53-2 absence, not gap) | Literal GL-12: visible at spawn point, DECLARED-UNDEFINED motion state (no fabricated wander), filed in the run ledger. |
| **K-5** | **Spawn drip** (`tick`/`t_s` ≤1-tick disagreement) | Rendered as measured (GL-8): the drip is data, not jitter — do not snap. |

Residual forks discovered mid-run: reasoning-boundaries ruled in-run veto-open (§ 8); anything
touching locked PART A grammar or story register HALTs.

## 6 · Matt interface (declared pre-launch — element 5; checkpoints per pattern § 6 obs. 2)

**Owner-eye checkpoints are pre-registered MID-RUN gates, not end-of-run briefings** (the
KIT-FIDELITY lesson: both catches were his, mid-stream, unprompted):

- **CP-A — statics:** arena + roster stand-up (dressed arena, 344 actors placeable, spawn
  markers under the BOX rule). One framed still-set + framing sentence. *Before* motion work
  builds on it.
- **CP-B — motion:** locomotion watch (paths, dwells, straight walks, spawn drip, player sweep).
  One short clip. *Before* combat presentation builds on it.
- **CP-C — the run watch:** full E-s09-cp150 candidate watch (waves 151–170), divergence ledger
  beside it (GL-12: read `informative_rows` before judging feel).

Each CP is a HALT: the run does not proceed past an unviewed checkpoint. Matt's other declared
surfaces: this charter's veto window (open now → launch); fork vetoes (§ 5, one word); G-FACT
fallback notification (informational, not a halt). Red-flag pings only between checkpoints.

## 7 · Lanes and routing (element 7 — seams execute; conductor writes no production code)

| Seam | Work |
|---|---|
| **drax** | ALL Godot cells (loader, arena, actors, watch). **Cell 0 (precondition): the two owed countersigns** — board-boundary rule + BOX shape declaration (CL-11; `export/MIGRATION.md [2026-08-09b]`) + OBJ-1 signature disposition. Split-cell form per CL-1; commit-per-item per CL-2. |
| **galadriel** | Screenshot/watch verification cells; noise-floor statements on any presence verdict (FG-11/FL-6). |
| **star-lord** | Factory-side: SB-1 workflow YAML + receipts; engine tree untouched otherwise. |
| **conductor** | Course only (§ 2.1 economics): sequencing, rulings, renders in fallback mode, ledger. Gandalf-seam pieces → named `gandalf` sub-agent. |
| **jack-ryan** | Gate-2 on the loader landing + any in-run reclassification (safety #2). |

## 8 · Halt taxonomy (instantiated)

**Commitment HALTs (correct, keep):** G-EYE checkpoints · locked-PART-A grammar conflicts ·
style-register or story-frame implications · charter amendment · Gate-2 BLOCK · any temptation
to cross Rider-1 (fabricating absent grammar) — that one is a REFUSAL, not a fork.
**Reasoning-boundaries (ruled in-run, veto-open, ledgered):** presentation choices within GL-law
+ PART A · fork residuals of § 5 · gate-failure diagnosis → finding (Gate-B precedent).

## 9 · Ledger and laws

- Ruling ledger: `gandalf/notes/2026-08-10-sb1-scene-run-ledger.md`, created at launch (L-0 =
  pins: godot HEAD, spine commit or fallback declaration, charter commit).
- Per-landing law CL-3 at every landing; trust-but-verify every hop (CL-10); value-change sweeps
  per Discipline #72 (mechanical enumeration, pasted).
- Deploy surfaces: none (local godot repo, never pushed) — red-main tripwire (§ 6 obs. 4)
  N/A, declared.

## 10 · Known instrument state and debts (declared, not blocking)

- **N3 OPEN** (BR-2 wind-down): unidentified render-nondeterminism term, up to 2,305 lit px from
  ~frame 100 — why G-DET claims the scene-sim layer only (FG-10 rider). Identifying N3 stays
  BR-3-inherited work; any SB-1 presence gate states its floor at verdict frames (FL-6).
- **R-BR-17 (three-layer VFX law) NOT-HARVESTED** (`run-minted-law.md` § 5.3) — if a VFX cell
  needs it, harvest-first, never restate from recollection (CL-4).
- **Engine full-suite red tree** (63 F / 21 E) is the L-74(d) NON-GATING baseline — SB-1's test
  walls target factory + scene suites, never the engine baseline.
- **Addendum-19 Class-C re-derivation** (BR-3 item 2) — carried, surfaces only if a BR-2-lineage
  gate is reused.

## 11 · Launch gate

SB-1 launches when ALL of: **(1)** spine Gate-2 ladder closed + conductor DRIFT-CRITIC re-verdict
PASS — **or** fallback § 4 invoked in writing in the ledger; **(2)** charter veto window closed
by Matt's word (or his silence past his next engagement, per the KC2 pick-discharge precedent —
named here so silence is a defined signal, not an assumption); **(3)** Cell 0 countersigns
dispositioned. Launch is recorded as ledger L-0.

**Signed:** gandalf (`RUN-CONDUCTOR`), 2026-08-10. Reproduce, then let the divergence ledger say
where reproduction was impossible or ruled away.

---

## Amendment 2026-08-12 — retention law rider (Matt: "LAW")

The R2-rider retention law is ADOPTED and binds every capture-producing lane of this run:
artifact classes **O / D / E**, `captures/` hard ceiling **10 G**, floor-check-before-render
(breach = housekeeping HALT). Full text: run ledger **PL-5**
(`2026-08-10-sb1-scene-run-ledger.md`). Graduates toward run-minted-law (FG-12 extension) at
SB-1 close. — gandalf, `RUN-CONDUCTOR`
