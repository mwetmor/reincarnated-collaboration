# Next-session start — the path to the Periodic Table of Kits + first emission

> **STATUS:** RESUME PLAN — authored gandalf 2026-07-11 at wind-down. Companion to
> `2026-07-11-project-wind-down.md` (the state of record; read it first if anything below
> surprises you). This doc is ORDERED and PASTE-READY: a fresh session with zero context can
> drive the whole resume from here. **Fire prompts in this doc carry the new one-session +
> slot-claim discipline** (collision post-mortem: wind-down §2).

---

## §0 The two north stars (Matt, verbatim intent, 2026-07-11)

> *"…our goals of the periodic table of kits and the emit our first pipeline so that I can
> begin selecting kits and using them to build out the demo."*

1. **The Periodic Table of Kits** — the atlas chart, emitted from measurement, rendered on Glance.
2. **The first emission pipeline run** — sim-certified kit bundles on disk, so **Matt selects kits → demo build-out** (the point of everything below).

**The chain (memorize this shape):**

```
E4 Gate-2 ──► ninth-axis measurement (ii) ──► emission primitive ──► atlas harness ──► PROMPT 5 (atlas.json + SVG) ──► PROMPT 6 (Glance /table)
   │                                              │                                        ▲
   │                                              └──► FIRST EMISSION RUN ──► kit bundles  │ plane-lock ruling (Matt, §3 below)
   │                                                        │
F5 note ► Gate-1 ► F5 build ──► K26–K29 land (roster 35) ───┴──► MATT SELECTS KITS ──► DEMO BUILD-OUT
```

Machinery lane (top) builds the table; content lane (bottom) fills its dots. Both start immediately and in parallel — they touch disjoint gates.

## §1 STEP 1 — E4 Gate-2, collision-aware (fires FIRST, unblocks the machinery lane)

**Paste into exactly ONE fresh KR session:**

```
KR — PASTE INTO EXACTLY ONE SESSION. One job: fire jack-ryan Gate-2 on engine commit 785956c
(E4 PHASE-2, tag gamora/v1.5-commitment-axis-4) with a COLLISION-AWARE mandate. Context: this
build survived a two-writer collision resolved by race (full record:
agentic_orchestration/gandalf/notes/2026-07-11-project-wind-down.md §2); it is self-verified
(byte-identity 12/12, smoke GREEN, perf −2.5%) but UNGATED and UNPUSHED, and its provenance
may include absorbed second-author code. Before firing, append "SLOT CLAIMED — E4-Gate-2,
this session, <timestamp>" to agentic_orchestration/dispatches/2026-07-10-gamora-commitment-axis-E4.md
and COMMIT. jack-ryan's mandate, in addition to standard Gate-2 scope:
(a) line-trace the full E4 surface (spatial_engine.py +469, spatial_telemetry.py +29,
    commitment_state_machine.py) against the PHASE-1 math note (56e1eb4) + the sim-consumer
    math note in the commit — every mechanism traces to spec or gets flagged;
(b) hunt the interleave bug-class explicitly — double-inits (the :1929 _e4_blind pattern,
    already gone from HEAD), orphaned attributes, dead branches, duplicate wiring — using
    agentic_orchestration/dispatches/2026-07-11-e4-phase2-collision-harvest.diff (2,277
    lines) as the provenance reference;
(c) EMPIRICAL criterion-18 check: RUN the blind-arm vs competent-arm A/B and demand a
    distributional difference — byte-identity 12/12 proves only the no-E4 path untouched,
    NOT that the E4 path is right;
(d) on PASS: engine push unblocks per the E3 v1-whole pattern (Matt's go in-session);
    downstream note: ninth-axis measurement half (ii) unblocks — signal gandalf for
    PROMPT 2b. On BLOCK: the held Option-2 fallback (revert 785956c, rebuild in isolated
    worktree) is the pre-agreed disposition — nothing was lost by gating first.
```

## §2 STEP 2 — F5 math-note RE-FIRE (parallel-safe; content lane opens)

The mid-run cancellation cost nothing (wind-down §1: no partial artifacts, $0). Dispatch is FIRE-READY as authored. **Paste into exactly ONE fresh KR session** (may run concurrently with STEP 1 — disjoint seams, and the F5 unit is notes-only):

```
KR — PASTE INTO EXACTLY ONE SESSION. One job: dispatch gamora on the F5 cost-TYPE math note.
The dispatch is FIRE-READY as authored:
agentic_orchestration/dispatches/2026-07-11-gamora-f5-cost-type-math-note.md (four §8 pins:
HP-floor shared-branch mirroring combatant.py:409 · damage-taken event grain · charge-pool
arity + active-spender law · byte-guard scope; all design forks Matt-ruled 2026-07-11; roster
K26–K29; denominator 35). A prior fire was cancelled mid-run with zero artifacts — this is a
clean re-fire, NOT a resume. Before firing, append "SLOT CLAIMED — F5-math-note, this
session, <timestamp>" to that dispatch file and COMMIT. Notes-only, $0, NO sim code, NO runs.
On landing: Gate-1 critique pair (jack-ryan + gandalf — cost-model semantics are
class-fantasy surface), then signal gandalf for PROMPT 3b (the F5 build fire).
```

## §3 STEP 3 — plane-lock ruling (Matt + gandalf; gates PROMPT 5)

**gandalf's first task next session:** read **Matt's own mock** —
`matt_notes_handoff_docs/reap-die-rise-atlas-chart-mock.svg` (committed at wind-down) —
against renderer-spec §2 (`agentic_orchestration/gandalf/notes/2026-07-11-atlas-chart-renderer-spec.md`),
and present Matt the mock-vs-spec delta. The mock is likely the ruling input.

**What Matt rules (§2.7):** lock the 15-cell frame — rows = `bc_commitment`
(instant / wind-up / channel, ordered `commitment-weight-v1`) × columns = damage-geometry
Axis 2 (single / small-AOE / large-AOE / chain / multi-spawn, ordered `dispersion-v1`), with
`isotope-seq-v1` sub-ordering. **Lock the rule, not the raster** — badges/dots/annotations
stay per-version payload; addresses are permanent. Matt's pre-stated lock criteria
(purposeful, sensible axes for search/exploration) are argued met in spec §2. Queue row
**Q19** carries this.

## §4 STEPS 4–7 — the drafted-on-signal chain (gandalf authors, Matt relays)

| Step | Prompt | gandalf drafts WHEN | Fires WHEN |
|---|---|---|---|
| 4 | **PROMPT 2b** — ninth-axis measurement half (ii): commitment-axis measurement over the population (the table's row-axis data) | Gate-2 finding lands (its conditions shape the prompt) | immediately after drafting |
| 5 | **PROMPT 3b** — F5 build fire (K26–K29 into generation + sim; Gate-1 conditions carried verbatim) | F5 Gate-1 disposition lands | after 3b drafting; slot-claimed |
| 6 | **PROMPT 5** — star-lord: atlas.json emission harness + deterministic SVG renderer (renderer spec §4–§5, acceptance §7) | may draft early; fires only when THREE gates green: ninth-axis (ii) landed · emission-primitive verify · plane-lock ruled (Q19) | gate-checked in the prompt |
| 7 | **PROMPT 6** — drax: Glance v1.10 `/table` page consuming atlas.json (v1.9 relay pattern) | after first validated atlas.json + SVG + gandalf DRIFT-CRITIC pass | same-day as its gate |

**Then the goal events:** first full emission run (kit bundles on disk, sim-certified) →
**Matt's kit-selection session** (the periodic table is the selection instrument — that's why
the machinery lane matters) → **demo build-out** (drax, Godot, selected kits).

## §5 Standing discipline to INSTITUTE this session (from the collision)

KR executes, jack-ryan ratifies as governance (wind-down §2 has the full rationale):
1. `PASTE INTO EXACTLY ONE SESSION` header on every relay prompt (already applied above).
2. Commit-as-mutex slot claim before any shared-tree subagent fires.
3. Worktree-by-default for shared-tree builds; merge back via single KR commit.

## §6 Parked (non-blocking — do not let these preempt §1–§4)

- Engine push of `785956c` — gated on Gate-2 PASS (STEP 1d).
- Batch-2 re-fire — rests at Matt's 2026-07-08 lock (four preconditions + driver re-point + stratified mandate).
- star-lord `output/`-tree hygiene sweep; stale W0.1 worktree removal (`agent-ad557ae39574ea548`).
- `bigork_specs.png` + business-platform-strategy copy (Matt drops, committed at wind-down) — Matt introduces when ready.
- B12 re-cert + star-lord telemetry follow-on flagged in E4 completion record — sequence after Gate-2.

## §7 Session-start reads (fresh gandalf)

1. `canonical/00-ground-state.md` → 2. this doc + wind-down companion → 3. serial-content-emission tracker (twelfth delta governs) → 4. `matt_decision_needed/README.md` (Q19) → 5. renderer spec §2 + **Matt's mock SVG** (STEP 3 is yours first).

**Signed:** gandalf, 2026-07-11. Nothing above requires re-derivation — every gate, hash, and path was verified at wind-down. Pick up STEP 1 + STEP 2 in parallel, STEP 3 the moment Matt engages.
