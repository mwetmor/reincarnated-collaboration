# Painted-2D Art Pipeline — SYSTEM DESCRIPTION (human-readable)

> **STATUS:** CURRENT (load-bearing as of 2026-09-11) — see `canonical/00-ground-state.md`. **LIVING:** this is Matt's cross-session view of the Astra burst lane; it is kept in sync with the executable sources by the § 7 SYNC table (hash-stamped, same-commit rule).

**Date:** 2026-09-11
**Author:** gandalf (CANON-STEWARD / RUN-CONDUCTOR)
**Status:** v1.0 — describes Run C-1 as chartered; amend the SYNC table on every source change
**Authority:** Matt 2026-09-11 — *"add this section into canonical so that yourself and other agents can reference it … a system description with links and pipeline flow which is all human readable so that I can stay in sync and track the architecture across sessions in case there is agentic drift"*; rulings F1–F10 (charter § 10)
**Companion docs:**
- `canonical/reap-die-rise-game/painted-2d-pipeline/mechanical-process.md` — the agent-facing twin (what executes; enforcement)
- `agentic_orchestration/gandalf/notes/2026-09-11-astra-burst-lane-run-charter.md` — Run C-1 charter (register card, burst rules, rubric, slate, HALT rules, ARCHITECT gate)
- `astra_test_01/burst/SPEC.md` — the software build contract (T0 modules, oracles O1–O9, bible schema, T1–T5 roadmap)
- `agentic_orchestration/gandalf/notes/2026-09-11-astra-burst-lane-review-and-architecture.md` — why this exists (the TEST-02 verdict) + the rulings ledger
- `agentic_orchestration/gandalf/notes/2026-09-11-painted-2d-pipeline-scope-map.md` — the full scope map (~70 scopes)
- `agentic_orchestration/legolas/research/2026-09-11-ai-tells-bibles-oracles/findings.md` — R6–R8 (tells, bibles, oracles)

---

## 0. TL;DR

- **What it is:** a lane that runs `gpt-6-astra` (OpenAI Codex, built-in `image_gen`, ChatGPT subscription) in **short, fresh-context bursts** to produce painted-2D game art — sprite sheets, gear layers, VFX, scene plates — judged by **deterministic oracles + an independent Astra instance**, against a **faction bible** that is data, not prose.
- **Why bursts:** the 22-hour autonomous run (Sep 10–11) kept its goal sentence through 14 compactions and still drifted into a Blender rig, because intent lived only in documents it wrote itself. Here **intent lives outside the generator**: register card + bible + ledger are conductor-owned; a burst gets one bounded task and cannot grade itself.
- **Who:** gandalf conducts; **Astra does all labour** (tooling, generation, checking, judging, packing — Matt's F7); Matt rules at milestones. No other team agents are in the loop during the testing phase.
- **Where it is now:** § 6 (and the live ledger it points to).

---

## FLOW

1. **Bible + charter** ← S1
2. **Brief** ← S2
3. **Generate** ← S3
4. **Check** ← S4
5. **Judge + transcribe** ← S5
6. **Compare + ledger** ← S6
7. **HITL milestone** ← S7
8. **Pack + import** ← S8

---

## 1. Purpose and boundaries

Test — then, if it passes, produce — *beautiful, thematically scoped painted-2D characters, VFX and scene plates* for **Reap. Die. Rise.**, 100 % via Astra under strict guidelines (Matt F6a), with the 3D Synty/Godot register (`reap-die-rise-story/style-register.md`) **still the locked register** until one character passes X2–X5 and one plate passes X6. Scenes follow the **finite plate library + procedural assembly** model (Hades / Diablo II tiles; Matt F6). The non-Astra generation path is discussed only if Astra is ruled out.

```
  bible.json ──► render brief ──► [Astra GENERATE burst] ──► PNGs + receipt
      │                                                          │
      │            ┌──────────── deterministic oracles O1–O8 ◄────┤ CHECK burst (frozen tools)
      │            │                                             │
      └────► compare_to_bible ◄─── inventory.json ◄──────────────┤ TRANSCRIBE burst (separate Astra instance)
                   │                    (presence + counts only) │ JUDGE burst (taste residue + known-bad control)
                   ▼
              ledger.json ──► milestone packet (review.html + MP4) ──► Matt rules ──► PACK/import (Godot 2D)
```

## S1 Bible and charter

The **charter** fixes the run (register card § 2, typed-burst rules § 4, rubric § 6, slate § 7, HALT rules § 8) and is ARCHITECT-gated before launch. The **faction bible** (`astra_test_01/burst/bible/`, schema v0.1) is the declared truth every oracle compares against: rules with `scope`, `placements[]`, `exclusions[]`, an `oracle{}` or `JUDGE-only`, a `known_bad`; faction tables PILLARS / PALETTE / PARTS / CONSTRUCTION / LIGHT / SCALE. Vocabulary rows are **Matt's rulings**; oracle catches re-enter as rules with `source: oracle-feedback` (the bible ↔ oracle loop).

## S2 Brief

`lane/render_brief.py` renders REGISTER_CARD + the type's BURST_RULES row + TASK + REFERENCES (labelled by role) + RETURN (the strict receipt schema). Deterministic; the brief's hash is in the ledger. Prompts are generated artifacts, never hand-written.

## S3 Generate

`lane/run_burst.py` invokes `codex exec` **in a fresh, ephemeral process with a workdir outside the repo** (no charter text loads; ≈19K-token boot), hard caps (≤15 min, ≤20 tool calls, ≤12 images; TOOLING ≤40/≤60), reference images via `-i`, output forced to the receipt schema. GENERATE bursts may not write code or touch anything outside `out/`. Green plate + deterministic matting (transparency is unreliable under reference conditioning).

## S4 Check

CHECK bursts run **frozen** tools (hash-pinned in `MANIFEST.sha256`) — the brief's gates G1–G9 (ported from runs 02/03), plus O1 palette, O2 figure/ground, O3 **motif-instance count** (the astrolabe defect as a number), O4 plain-surface budget, O5 silhouette at 64 px, O6 per-part metrics via disjoint palette bins, O7 key-light azimuth, O8 brush-grain energy. Every result is a number + threshold + evidence; `null` when unclassifiable.

## S5 Judge and transcribe

A **separate Astra instance** (never the generating context) does two things: **TRANSCRIBE** — answer DSG-shaped questions generated from the bible (presence/absence + per-part counts against a closed part list; never coordinates), with a **declared-absent control** in every set — the only instrument that reaches *functional implausibility* (straps carrying nothing), the most prevalent and least-caught tell class; and **JUDGE** — the taste residue on a 1–5 rubric, with a hidden known-bad control per batch; a judge that passes its control voids the batch.

## S6 Compare and ledger

`compare/compare_to_bible.py` scores gate results + inventory against the bible's declarations and emits the diff. The conductor-owned `runs/C-1/ledger.json` records every burst (type, brief hash, images, audit, receipt hash, artifacts, exit), experiments, milestones, HALTs and veto-open conductor rulings. **No burst ever writes the ledger; no receipt may say PASS.**

## S7 HITL milestone

Matt sees: identity masters (picks 1 of 3) · the turnaround · the first loop (rules G6b as shipping bar) · the first VFX composite · the first plate + derived mask — each as a standalone `review.html` + Chrome-playable MP4 in `~/Desktop/Astra Burst Review - <date>/` — plus any experiment-level FAIL and any HALT (two consecutive FAILs; VOIDs; cap; rate-limit streak). A planned **HITL review console** turns approve/reject into JSON clicks (scope map 8.2).

## S8 Pack and import

PACK bursts write sheets, `atlas.json`, the engine-neutral manifest (frames, fps, pivot, direction, layer stack + slot, hitbox, emissive — `E04/NEUTRAL_CONTRACT.md`), `review.html`, MP4, and Godot port notes; `godot_import.py` (T2) emits SpriteFrames. Pixi is a **viewer only** (no runtime) during testing; Godot 2D is the target.

---

## 3. Components and links

| Component | Path | Owner | Class |
|---|---|---|---|
| Run charter (rules, slate, gate) | `agentic_orchestration/gandalf/notes/2026-09-11-astra-burst-lane-run-charter.md` | gandalf | doc (source) |
| Software build contract | `astra_test_01/burst/SPEC.md` | gandalf (Astra builds) | doc (source) |
| Executable rules (extracted verbatim) | `astra_test_01/burst/{REGISTER_CARD,BURST_RULES,JUDGE_RUBRIC}.md` | gandalf | data (Astra reads) |
| Lane runtime | `astra_test_01/burst/lane/` (`run_burst.py`, `audit.py`, `render_brief.py`, `ledger.py`, `schema_check.py`) | Astra-built, conductor-frozen | code |
| Gates / oracles / parts / comparator | `astra_test_01/burst/{gates,oracles,parts,compare,transcribe,review}/` (T0-b/T0-c) | Astra-built, conductor-frozen | code |
| Bible | `astra_test_01/burst/bible/` | Matt rules vocabulary; gandalf authors | data |
| Ledger + artifacts | `astra_test_01/burst/runs/C-1/` | conductor | data |
| Freeze manifest | `astra_test_01/burst/MANIFEST.sha256` | conductor | data |
| Codex profile | `~/.codex/astra-burst.config.toml` | conductor | config |
| Burst workdirs (outside repo) | `~/astra-burst/runs/C-1/<burst>/` | wrapper | scratch |
| Research | `agentic_orchestration/legolas/research/2026-09-11-ai-tells-bibles-oracles/` (R6–R8) · `…/2026-09-11-r9-pipeline-scope-discovery/` (R9, in flight) | legolas | evidence |
| Scope map | `agentic_orchestration/gandalf/notes/2026-09-11-painted-2d-pipeline-scope-map.md` | gandalf | doc |
| Historical | `astra_test_01/design/` (TEST-02 suite, HISTORICAL — Matt F8), `astra_test_01/run_0{1,2,3}/` (the guided runs; tooling harvested) | — | lineage |

## 4. Roles and the human interface

| Role | Who | Does |
|---|---|---|
| Conductor | gandalf (foreground) | charter, briefs, ledger, milestones, design judgment; **writes no code** |
| Labour | Astra via typed bursts | TOOLING (once, then frozen) · GENERATE · CHECK · JUDGE · TRANSCRIBE · LABEL · ANNOTATE · PACK |
| Ruler | Matt | vocabulary (bible), milestones, HALTs, medium changes, the GO word |
| Outside the run | star-lord, galadriel, drax, legolas (research only), jack-ryan Gate-2 at close-out | per Matt: *"bulky agentic team infrastructure … may slow us down"* |

## 5. Enforcement (how the process is made to hold, not hoped)

1. **The wrapper audit** — every burst's event stream is censused (image calls, tool names, write paths vs a pre-burst snapshot, caps); any violation → **VOID** (rerun once, then HALT). This is the real enforcement for bursts.
2. **Fresh context by construction** — workdir outside the repo → no AGENTS.md/CLAUDE.md, no session memory, no compaction possible.
3. **Root `AGENTS.md` routing** — any interactive Codex session in this repo is pointed at `mechanical-process.md` and forbidden from generating painted assets outside the lane or resuming `astra_test_01/design/`.
4. **The profile** — `astra-burst.config.toml`: no plugins, no MCP servers, sandbox workspace-write.
5. **Freeze manifest** — tools are hash-pinned; any change is a new TOOLING burst + re-freeze + ledger entry.
6. **Receipts with no PASS vocabulary; controls in every judgment batch.**
7. **Open (research R2):** Codex `hooks.json` (session_start) as a fourth routing surface — unverified API in this Codex build.

## 6. Current state

Live truth: `astra_test_01/burst/runs/C-1/ledger.json`. As of this doc's authoring: T0-a/b/c DELIVERED and frozen (lane runtime; gate library; oracles O1–O9 + parts + comparator + transcription contract — 69 tests, 2 named-red acceptance cases: O3 template mode cannot see primitive-family bleed → O3b owed in T0-d, with two audit fixes); X1 smoke next (oracles + comparator); X1 smoke next; K1 (pilot identity) **paused** on Faction Bible v0 + Matt's vocabulary rulings; legolas R9 in flight. Rulings F1–F10: charter § 10.

## 7. SYNC — the two process documents and their sources (same-commit rule)

**Rule:** this doc and `mechanical-process.md` are views over the executable sources below. **Any commit that changes a listed source updates that row's hash + date in THIS table in the same commit (`mechanical-process.md` carries no table; it points here)** (the OP↔skill twin rule, `canonical-doc-format § 6.8`, applied here). Drift is detected by comparing the stamped hash to `shasum -a 256` of the source (a `check_sync.py` lands with T0-c; until then the check is the conductor's session-start act). A stale row is a **drift alarm**, never silently corrected.

| Source | Role | sha256[:12] | Reconciled |
|---|---|---|---|
| `agentic_orchestration/gandalf/notes/2026-09-11-astra-burst-lane-run-charter.md` | rules of the run | bbb1a1b9fbfe | 2026-09-11 |
| `astra_test_01/burst/SPEC.md` | build contract | 05d48f86b245 | 2026-09-11 |
| `astra_test_01/burst/BURST_RULES.md` | executable burst rules | 1a96e8aa0ad6 | 2026-09-11 |
| `astra_test_01/burst/REGISTER_CARD.md` | executable register | bc3ce44dee71 | 2026-09-11 |
| `astra_test_01/burst/JUDGE_RUBRIC.md` | executable rubric | 67b1e22ca361 | 2026-09-11 |
| `astra_test_01/burst/receipt.schema.json` | receipt contract | e2afcbc22e8d | 2026-09-11 |
| `astra_test_01/burst/lane/run_burst.py` | the invocation | 5a2df9e8381d | 2026-09-11 |
| `astra_test_01/burst/MANIFEST.sha256` | freeze state | ac2f9820407d | 2026-09-11 |
| `AGENTS.md` (repo root, § Painted 2D) | Codex routing | 190e17eb10a1 | 2026-09-11 |

---

## 8. Cross-references

- Router: `canonical/00-ground-state.md` · Game spec index: `canonical/reap-die-rise-game/00-index.md` · Game tracker: `canonical/current-to-end-state/current-to-end-state-game.md` (SESSION-DELTA 2026-09-11)
- Register lock (unchanged): `canonical/reap-die-rise-story/style-register.md` · Visual target: `astra_test_01/design/VISUAL_TARGET.md` · Doorway rule: `astra_test_01/design/experiments/E07V/FEEDBACK_2026-09-11.md` · Portability: `astra_test_01/design/experiments/E04/NEUTRAL_CONTRACT.md`
- Matt queues: Q70/Q71 RESOLVED 2026-09-11 (`canonical/matt_decision_needed/README.md`)

Tracker-delta: new canon home registered → game tracker SESSION-DELTA 2026-09-11 (this doc + mechanical-process.md); PART B open decision unchanged (register fork stays evidence-gated).

---

**Signed:** gandalf (CANON-STEWARD)
**For:** Matt's human-readable, hash-synced view of the painted-2D art pipeline so the architecture survives sessions and agentic drift is visible.
