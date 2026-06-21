# Combined autonomous run — wind-down: what to expect, and where it leaves battle-sim + content-emission

**Type:** gandalf wind-down note for the combined Track 1 + Track 2 autonomous run (launched by Matt 2026-06-21).
**Date:** 2026-06-21
**Author:** gandalf
**Companions:** the run plan `gandalf/requests/2026-06-21-track1-track2-combined-autonomous-run-plan.md`; the T1.1 halt ruling `gandalf/notes/2026-06-21-T1.1-magnitude-halt-ruling-metric-domain-not-magnitude.md`; the progress memo `gandalf/notes/2026-06-18-pipeline-completion-progression-memo.md` (2026-06-21 session-delta).

---

## 0. The headline — the run halted on its first stage, flagged me, and I've ruled

The run reached **T1.1 (the clear-shell magnitude pass) within ~1 minute of launch and HALTED there** (engine `bcc52b2`, collab `58e9539`). This is the run plan working, not failing: gamora authored a math-note-first falsifiable prediction, swept the only in-scope constant levers, **empirically falsified the recompose-first hypothesis** (the caster cohort is bimodal in burst — any mob-HP increase large enough to de-saturate the high-burst tail first inverts the caster median below the build-spend floor AND craters elite_pack into a mass zero-clear), and HALT-AND-FLAG-GANDALF rather than improvise a new mechanic or hand-tune to a pass. Two pre-registered PARK triggers fired exactly as designed.

**I have ruled** (`2026-06-21-T1.1-magnitude-halt-ruling...`): the 600@0.4s is a **metric out of its domain of validity, not a magnitude defect**. A caster deleting a blue trash pack sub-second is the ARPG caster fantasy (D3 Tal Rasha/Archon; PoE Arc/Spark off-screen clears) — inflating trash HP to slow it is the D4-launch damage-sponge anti-pattern and is REJECTED. The resolution is a **metric domain-of-validity GUARD at the band layer (T1.3)**: sub-`T_min` clears are out-of-domain for KPM, gated on clear-COMPLETION (did the pack die, fast) and excluded from the band fit; the band + ceiling apply to in-domain cells only. **T1.1 collapses into T1.3.** This falsifies the *mechanism* of my own 2026-06-20 three-fork ruling (Fork-2/3a "magnitude-tune it in") while preserving its destination ("exclude the artifacts, band the honest cells") — the substrate spoke and the ruling updated.

**Net effect on the run:** the one parked dependency (T1.1 → T1.3) is now un-parked by the ruling. Everything else was always independent and proceeds.

---

## 1. What to expect from the run (run-end state)

Per the run plan §1 decision tree, a HALT parks the affected stage and **continues all independent stages**. Independent of T1.1, and expected to complete:

- **T1.2 — absolute-magnitude-constant sweep (task #11):** the dead-absolute / stale-calibration constants (rocket's `mini_boss` HP-factor range `(9.50, 14.50)` still live upstream; the V5 >1.0 attribution artifact; siblings). Each math-note-first, recompose-first, jack-ryan Gate-2. STACK-FOR-MATT only if a constant moves a banked column.
- **T1.4 Read-1 — STR encounter-segregated read:** pure analysis on measured data (STR ships clear-room floor; boss shells via survive-and-kill). Drafts a finding.
- **T1.4 Read-2 — mixed-pack focus-fire read:** requires gamora's anchor-predicate rescale first (a Phase-6-internal build, math-note-first, Gate-2); independent of the T1.1 clear-shell question. Drafts the definitive (A)-vs-(B) focus-fire finding.
- **Track 2 — the full proxy decision packet:** T2.1 spatial-proxy-combat math note → T2.2 Gate-1 (jack-ryan DESIGN-MODE + the pre-registered gandalf design-fit self-assessment) → T2.3 the throwaway de-risk spike ("does a summoner clear the boss when the army actually fights?") → HARD-STOP. No production code, no `_DEFERRED_PROXY_BINS` lift, no proxy emission.

- **T1.3 — clear re-band (un-parked by the ruling):** with the domain-guard principle as input, gamora derives `T_min`, implements the guard (recompose-first, math-note-first, Discipline #12 semantic-shift declared, Gate-2), re-fits the clear-shell bands over in-domain cells, and **STACKS-FOR-MATT** (unchanged — the band acceptance was always Matt's). Two outcomes are both fine:
  - if the run re-consults gandalf state mid-flight, it consumes the ruling and **T1.3 completes inside the run**;
  - if not, T1.3 **parks to the run-end batch as "awaiting gandalf ruling"** — and the ruling is already written and sitting ready, so it closes in a short follow-up.

**Observed as of this writing:** the run had not committed past the T1.1 halt in ~7 minutes — either mid-stage on the next independent work (T1.2 / Track 2, which is normal — stages commit at checkpoints) or parked at the flag. Both are healthy. Nothing is corrupted; every work-product so far is committed locally.

---

## 2. Where this leaves BATTLE-SIM completion

The battle-sim track is the instrument-validity workstream: make the damage equation honest, then re-fit the bands ONCE at the tail.

- **Boss-half: DONE, banked.** Boss-gate built + Gate-2 PASS + canonical-written (`d5b7ac2`); both boss shells banked (the `mini_boss` un-escrow draft `2b80306` awaits Matt disposition approval). STR boss inversion ruled honest substrate drift; the `mini_boss` caster-wipe ruled a stale-calibration DEFECT and fixed recompose-first (inversion gone).
- **Clear-half: in hand, design-unobstructed.** The one design input that gated the clear re-band — the 600@0.4s question — is now **resolved by my ruling** (domain guard, T1.3). gamora's domain-guard build + clear re-band proceed; the re-banded clear-shell instrument STACKS-FOR-MATT.
- **Constants: swept (T1.2).** The dead-absolute constants get resolved at the source; the boss-half consumption-clamp becomes redundant-but-harmless.
- **Reads: in hand (T1.4).** STR segregated + mixed-pack focus-fire.

**Closure criterion:** the solo Profile-A instrument is **closeable on Matt's approval of the band batch** (boss-half un-escrow + clear-half re-band + any constant-driven shift). The run removes every *technical and design* obstacle to that closure; what remains is the one decision reserved to Matt — which bands ship. The instrument is honest; the question left is acceptance, not validity.

---

## 3. Where this leaves CONTENT-EMISSION completion

The content-emission pipeline (the full kit→world→player content spine) is **structurally unchanged by this run** — and that is correct, because its remaining work is not battle-sim work.

- **The spine plumbing is rocket/star-lord, not this run.** The "two tracks don't meet" gap (generation produces kits; the emission/assembly path that turns them into player-facing content) is unchanged. This run touches the *measurement instrument*, not the *emission plumbing*.
- **The kits leg keeps its asterisk: kits WORK for solo, summoner is DEFERRED.** The ~25% proxy reservation is encoded in the BC cell roster (`bc_target_cell_sampler.py`) but BLOCKED at composition (`bc_target_composer.py` `_DEFERRED_PROXY_BINS`) because the spatial sim gives proxies NO spatial damage and NO position — the genre's primary single-target caster path (summoner/proxy) emits nothing today.
- **Track 2 brings that to the edge of decision.** At run-end, Matt has a **proxy-combat decision packet**: the spatial-combat math note (what crossing the COUNT≠CONTRIBUTION cut costs), the Gate-1 verdict (structural + design-fit), and the spike findings (does the army actually kill the boss). That is what he needs to make the architecture call.

**Closure criterion:** content-emission completion has **two distinct doors still ahead, neither closed by this run** (by design): (1) the spine plumbing build (rocket/star-lord — a separate workstream), and (2) the proxy/summoner architecture decision (Matt's call on the Track 2 packet), which gates the 25% proxy emission. This run advances door (2) to a clean, evidenced decision; door (1) is untouched and remains the larger content-emission lift.

---

## 4. The batch Matt finds at run-end (the decisions reserved to you)

1. **Decisions-log DRAFT batch** (KR-authored, jack-ryan-reviewed, awaiting your disposition approval): boss-half un-escrow (pre-existing `2b80306`) + clear-half re-band & domain-guard (T1.3) + any constant-sweep disposition shifts (T1.2). Approve → jack-ryan canonical-writes.
2. **Phase 6 reads** (Read-1 STR-segregated + Read-2 mixed-pack focus-fire) — the STR/lever disposition in hand.
3. **Proxy-combat decision packet** (Track 2) — math note + Gate-1 verdict + spike findings + scope estimate. Your architecture call: build proxy combat proper / re-scope / park. This is the door to the 25% proxy emission.
4. **The T1.1 ruling** (`2026-06-21-T1.1-magnitude-halt-ruling...`) — already written; if T1.3 parked, relay/approve it and T1.3 closes.
5. **Push — held** (ADR-006 + run plan §2 Matt-halt 5). The run is fully local; push is your final act after reviewing the batch. Push is NOT needed for the run to complete.

No subsystem is left half-built; no band is silently accepted; no content is silently emitted. The run advanced everything that could advance and stopped at the doors that are yours.

---

## 5. Session / process notes (separate from the decisions)

- **The terminal/process running the KR autonomous loop must stay alive** for the run to keep grinding the independent stages. If that process is closed, the run stops where it is — **safely**: all work-products are committed locally, nothing is corrupted, and it resumes/completes in a follow-up session. Closing it is not destructive; it just pauses progress.
- **Other interactive sessions are safe to close** at any time.
- **A separate gandalf/drax Godot ravine-carve workstream is also active** in the git log (collab `3dc3372`, `479d55c`) — unrelated to the combined battle-sim run; noted only so the interleaved commits aren't mistaken for run output.

---

**Signed:** gandalf, 2026-06-21. The run halted clean on its first stage, flagged the one call that was mine, and I made it — so the path is unobstructed in front of it. Battle-sim closes on your band-batch approval; content-emission's proxy door opens on your read of the Track 2 packet; the larger emission plumbing stays the separate lift it always was. Everything is local; the batch will be waiting.
