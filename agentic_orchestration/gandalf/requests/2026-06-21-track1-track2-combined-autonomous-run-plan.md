# Combined autonomous run plan — Track 1 (close the solo instrument) → Track 2 (proxy spec + gate + spike)

**Type:** gandalf-authored autonomous-run plan → **knight-rider sequences + executes**; gamora/rocket build + measure; jack-ryan Gate-1 (DESIGN-MODE) + Gate-2 (DEV-MODE, BLOCK authority); star-lord if a field crosses the sim→telemetry seam.
**Author:** gandalf
**Date:** 2026-06-21
**Run shape:** a single combined autonomous run. **Track 1 runs end-to-end. Track 2 runs spec + design-gate + de-risk spike ONLY, then HARD-STOPS.** Both tracks stack their genuine decisions as a batch of ready-to-approve drafts at run-end — the run does NOT block mid-stream on Matt, and does NOT take either of the two reserved decisions (band acceptance; proxy-combat architecture + emission).

**Composes with / read IN FULL before executing:**
- `agentic_orchestration/2026-06-20-miniboss-unescrow-decisions-log-draft.md` (the boss-half bank pattern this run mirrors — DRAFT banked "pending Matt disposition approval," measurement continued past it).
- `agentic_orchestration/gandalf/requests/2026-06-20-instrument-validity-workstream-KR-brief.md` (parent workstream; measure-isolated + single-tail-refit disciplines; task #11 the absolute-magnitude-constant sweep).
- `agentic_orchestration/gandalf/requests/2026-06-20-boss-gate-implementation-spec.md` (the boss-half tail-refit; this run does the CLEAR-half + the reads).
- Track 2 prior art: `canonical/story/proxy-add-design-spec-2026-06-16.md`, `proxy-commander-set-6-capstone-spec-2026-06-16.md`, `src/reincarnated/simulation/math/proxy-contribution-measure-and-set6-calibration-2026-06-17.md` (the COUNT≠CONTRIBUTION cut — proxies deal NO spatial damage, take NO position TODAY), `src/reincarnated/simulation/math/wc-derisk-spike-oracle-first-run-2026-06-13.md` (K5 proxy/summoner: IN @ open_arena, **LOW-EDGE @ boss** — the open question).
- `canonical/story/v1-bc-target-intent-2026-05-24.md` §line 101 (the documented ~25% proxy reservation: none ~75% / light ~10% / heavy ~15%).

---

## 0. Why this run exists (one paragraph)

The instrument-validity workstream's boss-half tail-refit is banked (un-escrow draft awaiting Matt disposition approval). Two things remain to CLOSE the solo Profile-A instrument (Track 1): the clear-shell half of the single tail-refit (magnitude pass → clear re-band), the absolute-magnitude-constant sweep (task #11), and the Phase 6 reads. Separately, the genre's primary single-target caster path — proxy/summoner — is reserved at ~25% in the BC cell roster (`bc_target_cell_sampler.py`) but DEFERRED at composition (`bc_target_composer.py:318-322`, "sim is solo-only; proxy-creation mechanics absent") because the spatial sim measures proxy *contribution-for-classification* only and gives proxies NO spatial damage / NO position. Closing that gap is a net-new combat-architecture build (Track 2). This run advances BOTH as far as is honest in one pass: Track 1 to completion; Track 2 to a ready-for-architecture-decision packet.

---

## 1. THE PRE-REGISTERED DECISION TREE (the safety core — read first)

Every stage routes to exactly one of three dispositions. This is what makes the run safe to leave running.

- **AUTO-PROCEED** — the stage's pre-registered ENDORSE criteria hold; the run banks its work-product as a DRAFT (KR-authored, jack-ryan-reviewed) and continues to the next stage WITHOUT waking Matt or gandalf. (Same pattern as the A2 wave's §2.2 ENDORSE and the boss-half "banked pending approval.")
- **STACK-FOR-MATT** — the stage produced a DISPOSITION that changes what ships (a re-band; an architecture commit; a content emission). The run drafts it, stacks it in the run-end decision batch (§5), and CONTINUES any downstream work that does not depend on the approval. It does NOT block.
- **HALT-AND-FLAG-GANDALF** — a pre-registered PARK trigger fired (an inversion, a zero-clear, a scope explosion, a design-fit failure). The run stops the affected stage, writes the flag, and continues other independent stages if any remain; the flagged item waits for gandalf.

**Discipline anchors (all auto-fire, no re-ask):** Discipline #1 math-before-code (every build stage authors a falsifiable math note first); #3 seed hygiene (fresh disjoint bases — used bases listed in the workstream brief); #11 empirical inspection; #12 semantic-shift declaration across any meaning change; recompose-first (no hand-tuning to a pass); §5/§5a anti-pattern (never bless an artifact as texture just because a gate is sound). jack-ryan Gate-2 BLOCK authority is absolute on any production-gate change.

---

## 2. PRE-APPROVALS (fire without re-ask) vs MATT-HALTS (stack for the batch)

**PRE-APPROVED — these fire autonomously:**
1. gamora + rocket recompose-first builds + re-measures for every Track 1 stage (in-seam, Gate-2-covered).
2. jack-ryan Gate-2 reviews (with BLOCK authority) on each production-gate change.
3. The run BANKS Track 1 dispositions as DRAFTS (KR-authored, jack-ryan-reviewed) — decisions-log DRAFTS, not canonical writes.
4. Track 2 math-note authoring + the THROWAWAY de-risk spike (no production touch; throwaway branch/harness).
5. gandalf design-fit on Track 2's spec is PRE-REGISTERED in §4 (the run self-assesses against my criteria; it does not need to wake me unless a PARK trigger fires).
6. star-lord MIGRATION authoring if a Track 1 field newly crosses the sim→telemetry seam (ADR-004).

**MATT-HALTS — these stack as drafts; the run does NOT take them:**
1. **Acceptance of the re-banded CLEAR-shell dispositions** (clear-half of the Phase-5 band-approval halt) — drafted, banked pending approval, downstream reads continue.
2. **Acceptance of the boss-half un-escrow draft** (already drafted 2026-06-20) — folded into the same batch.
3. **The proxy-combat ARCHITECTURE commit** (crossing the COUNT≠CONTRIBUTION boundary) — the run produces the math note + Gate-1 verdict + spike findings as a decision packet; it does NOT build the subsystem.
4. **The composer un-defer + 25% proxy emission** (`_DEFERRED_PROXY_BINS` lift) — the §5a content-emission gate; reserved to Matt absolutely.
5. **Push to remote** — stays held (ADR-006). The run is fully local; Matt reviews the batch and pushes as the final act. Push is NOT needed for the run to complete.

---

## 3. TRACK 1 — close the solo Profile-A instrument (runs end-to-end)

### T1.1 — Magnitude pass (clear-shell timing-floor)
- **Work (gamora, recompose-first):** resolve the 600@0.3s timing-floor artifact on clear shells (the sub-second caster cells). Math-note-first: state the expected clear-shell KPM shift for caster cells once the timing floor is corrected, falsifiable against the current cratered/72×-spread rows.
- **AUTO-PROCEED if:** caster sub-second cells calibrate (no sub-second guillotine artifact remains), no clear-shell archetype inverts, no zero-clears introduced, recompose-first held. → jack-ryan Gate-2.
- **HALT-AND-FLAG-GANDALF if:** the magnitude fix requires a new mechanic (not a constant re-scale), or a clear-shell archetype inverts, or it perturbs boss shells (which are out of scope — boss-half is banked).

### T1.2 — Absolute-magnitude-constant sweep (task #11)
- **Work (gamora sim constants + rocket gen HP-factor range — KR routes cross-seam):** systematically resolve the dead-absolute / stale-calibration constants surfaced across the workstream: the `mini_boss` HP-factor range `(9.50, 14.50)` still live upstream in rocket's generation (the config inversion the boss-half consumption-clamp worked around), the V5 >1.0 attribution artifact, and any sibling constants of the same class. Each gets a math note (same dead-absolute-constant class as the four workstream targets).
- **AUTO-PROCEED if:** each constant resolves recompose-first, the boss-half consumption-clamp becomes redundant-but-harmless (generation-source now correct), no banked column moves. → jack-ryan Gate-2 per change.
- **STACK-FOR-MATT if:** any constant resolution changes a banked disposition (then it joins the band batch).

### T1.3 — Clear-shell re-band (the clear-half of the single tail-refit)
- **Work (gamora):** with T1.1 + T1.2 landed, re-fit the clear-shell KPM bands ONCE (the deferred half of the single tail-refit). Math-note-first: pre-register the expected re-banded clear-shell disposition by attribute.
- **STACK-FOR-MATT (always — this changes what ships):** draft the re-banded clear-shell disposition; bank pending Matt approval; CONTINUE to T1.4 (the reads do not need the approval, only the measured numbers).
- **HALT-AND-FLAG-GANDALF if:** the re-band produces an inversion, a zero-clear, or a floor breach (a band that lets a kit ship with no viable clear cell) — that is a design-fit failure, not a refit.

### T1.4 — Phase 6 reads (solo)
- **Read-1 (gamora):** STR encounter-segregated read — STR's honest disposition with the lever as it fires today (ships clear-room floor; boss shells via survive-and-kill). Pure analysis on measured data. AUTO-PROCEED to draft.
- **Read-2 (gamora):** the mixed-pack focus-fire read (the definitive (A)-vs-(B) read) — this REQUIRES gamora's anchor-predicate rescale first (G3b ruling §2.4). The rescale is a Phase-6-internal gamora build (math-note-first, Gate-2). AUTO-PROCEED through the rescale + read; **HALT-AND-FLAG-GANDALF** if the anchor-predicate rescale changes a banked clear/boss disposition (cross-contamination with the tail-refit).
- **Output:** both reads drafted as findings; any disposition consequence joins the batch.

**Track 1 end-state:** solo Profile-A instrument closed — clear + boss shells both refit, constants swept, reads in hand. Drafts stacked: boss-half un-escrow (pre-existing) + clear-half re-band + any constant-driven disposition shifts.

---

## 4. TRACK 2 — proxy: spec + design-gate + de-risk spike ONLY (HARD-STOP before build)

> **The hard rule:** Track 2 in THIS run produces a DECISION PACKET, not a combat subsystem. It does NOT write production spatial-combat code. It does NOT lift `_DEFERRED_PROXY_BINS`. It does NOT emit proxy kits. Those are Matt's two reserved decisions (§2 Matt-halts 3 + 4).

### T2.1 — Spatial-proxy-combat math note (gamora lead + rocket gen-interface input)
- **Work:** design-spec-as-math for crossing the COUNT≠CONTRIBUTION cut — how a proxy, in the SPATIAL fight, (a) spawns + takes a position, (b) selects a target, (c) deals spatial damage on the realized event stream (not a potential-integral), (d) becomes targetable / tanks / dies, (e) how the existing `proxy_population.py` lifetime/attrition model (D2-dominance wall, D3-evaporate) feeds the spatial fight. State the scope honestly: how many seams, how many waves, what the `proxy_max_active` count wall means for a single-boss fight.
- **AUTO-PROCEED to T2.2** on math-note authored. (Authoring a spec is always safe.)

### T2.2 — Gate-1 design review (jack-ryan DESIGN-MODE + PRE-REGISTERED gandalf design-fit)
- **jack-ryan DESIGN-MODE:** structural soundness of the proposed combat model (does it compose with the existing fight engine; is the COUNT≠CONTRIBUTION boundary crossed cleanly or smeared).
- **gandalf design-fit — PRE-REGISTERED ENDORSE criteria (the run self-assesses; does not wake me unless a PARK trigger fires):**
  - **ENDORSE if** the spec (1) preserves solo-fight behavior byte-identically when `proxy_bin=solo` (no regression to the closed Track-1 instrument); (2) makes proxy boss-kill a REAL graded outcome (a summoner is a fight you mostly-but-not-always win — like the smaller-boss texture — NOT a free clear and NOT an auto-fail); (3) keeps the player relevant (`s < 1` inheritance discipline holds — the army amplifies, never replaces, the caster); (4) routes proxy through the SAME survive-and-kill boss gate as solo (one instrument, not a special-cased proxy gate).
  - **PARK-and-flag-gandalf if** the spec gives proxies full autonomous spatial AI that forks the fight model; OR proposes a separate proxy-only ship gate (instrument fragmentation); OR the scope reads as a multi-month rewrite rather than an extension (that is a roadmap decision, not a wave).
- **Output:** Gate-1 verdict appended to the decision packet.

### T2.3 — Throwaway de-risk spike (no production touch)
- **Work (gamora, throwaway branch/harness):** the single highest-value unknown — *does a summoner clear the boss shell when the army actually fights?* Give proxies spatial damage in a SPIKE harness (not production), run a genuine proxy-commander caster fixture against `boss_with_adds` + `mini_boss`, and read survive-and-kill. Prior art: `wc-derisk-spike-oracle-first-run-2026-06-13.md` (K5 proxy was IN @ open_arena, LOW-EDGE @ boss with synthetic density — this spike replaces synthetic density with actual fighting proxies).
- **Findings feed the architecture call:** if summoners clear boss shells gradedly → the build is worth it and bounded; if they trivially faceroll → the inheritance/count wall needs design work before build; if proxies can't be made to fight without a fight-engine rewrite → scope is a roadmap item, not a wave. ALL THREE are valuable findings, not failures.
- **AUTO-PROCEED to HARD-STOP** on spike findings written.

### T2 HARD-STOP — assemble the decision packet
The run stops Track 2 here and writes the **proxy-combat decision packet**: T2.1 math note + T2.2 Gate-1 verdict (with gandalf design-fit disposition) + T2.3 spike findings + a bounded scope estimate. This packet is what Matt needs to make the architecture call (§2 Matt-halt 3). The build, the un-defer, and the 25% emission are NOT in this run.

---

## 5. RUN-END STATE — what Matt finds (a batch of ready decisions, nothing half-built)

1. **Decisions-log DRAFT batch** (KR-authored, jack-ryan-reviewed, awaiting Matt disposition approval): boss-half un-escrow (pre-existing) + clear-half re-band + any constant-sweep disposition shifts. Approve → jack-ryan canonical-writes.
2. **Phase 6 reads** (Read-1 + Read-2 findings) — the STR/lever disposition in hand.
3. **Closed solo Profile-A instrument** — clear + boss shells refit, constants swept. The battle-sim track is closeable on Matt's approval of the band batch.
4. **Proxy-combat decision packet** — math note + Gate-1 verdict + spike findings + scope estimate. Matt's architecture call (build Track 2 proper / re-scope / park) is a clean, evidenced decision.
5. **Everything local; push held** — Matt reviews + pushes as the final act.

No subsystem is left half-built; no band is silently accepted; no content is silently emitted. The run advanced everything that could advance autonomously and stopped exactly at the decisions that are yours.

---

## 6. THE LAUNCH PROMPT (hand to knight-rider)

```
Execute the combined autonomous run per
agentic_orchestration/gandalf/requests/2026-06-21-track1-track2-combined-autonomous-run-plan.md.

Run Track 1 end-to-end (T1.1 magnitude pass → T1.2 constant sweep → T1.3 clear re-band →
T1.4 Phase 6 reads), then Track 2 spec+gate+spike only (T2.1 math note → T2.2 Gate-1 →
T2.3 throwaway spike → HARD-STOP).

Honor the §1 decision tree exactly: AUTO-PROCEED on pre-registered ENDORSE; STACK-FOR-MATT
(draft + continue, do not block) on any disposition that changes what ships; HALT-AND-FLAG-
GANDALF only on a pre-registered PARK trigger. Fire the §2 pre-approvals without re-ask.
Do NOT take the §2 Matt-halts (band acceptance; proxy architecture; proxy un-defer/emit; push).

Sequence the specialists (gamora, rocket, jack-ryan, star-lord) per stage. jack-ryan Gate-2
BLOCK authority is absolute on production-gate changes. Math-note-first + recompose-first +
seed hygiene + semantic-shift declaration on every build. Assemble the §5 run-end batch.
Leave everything local (push held). Surface the batch when the run completes.
```

---
**Signed:** gandalf, 2026-06-21. Close the solo instrument the workstream was scoped to close; bring the proxy question to the edge of decision with real evidence — the spec, the gate, and the spike that answers whether the army can kill the boss. Stop at the two doors that are Matt's: which bands ship, and whether the summoner crosses the COUNT≠CONTRIBUTION line into the fight.
