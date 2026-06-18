# KR flag-flip run — three production semantic-shifts (#1 F1 geometry, #2 D4 proxy-track, #3 keystone faithful-loadout)

**STATUS:** RUN PROMPT (gandalf → knight-rider, Matt-paste-ready)
**Date:** 2026-06-17
**Author:** gandalf (story-and-design steward)
**Authority:** Matt 2026-06-17 — "let's flip all 3." The criterion gating #1–#3 was always "Matt's semantic-shift declaration, not further evidence" (RETURN-PACKAGE §3). That declaration is given; this run operationalizes it.
**What this run is:** ONE knight-rider session that flips THREE OFF-by-default production flags LIVE, each as a separate commit + smoke, with a jack-ryan decisions-log semantic-shift declaration per flip. All three are in **gamora's simulation seam** (`reincarnated-engine/`), all built + Gate-2 PASSED behind OFF defaults during the 2026-06-17 autonomous run, all git-revertible. gandalf does NOT flip production code — this routes through gamora (implement) + jack-ryan (declare + confirm) + KR (sequence + push gate). gandalf supplies the design rationale the declarations cite, and holds one Tier-2 band-refit call.

---

## The three flips (fire in this order — #1 is a precondition for honest re-measure)

| # | Flag | Seam / commit / tag | What flipping LIVE does | gandalf design rationale |
|---|---|---|---|---|
| **1** | F1 geometry-blindness fix (no default-flag — it's a code-path widening already merged behind the build; "flip" = ratify LIVE) | gamora · `104bfbc` · `gamora/v-f1-geometry-fix-1` | Widens the spatial resolver's Path 2 to read the rich `geometry` model field through the unchanged `_RICH_TO_SPATIAL` table (was reading degraded keyword heuristics). | **ENDORSE.** This is the W-F-adoption precondition carried from 2026-06-16, and it is the precondition for *honest* re-measurement: #2/#3 re-measure the spatial swarm path, and that path should run on real geometry, not keyword heuristics, before we trust any new mobs/min distribution. It is ALSO the precondition for ever measuring the caster open-arena coverage-bound failure correctly (AGENT_STATE session-13) — that failure is spatial, and you cannot see it through degraded geometry. **Land #1 first.** |
| **2** | `track_proxy_population` default → ON | gamora · `af5c8b2` · `gamora/v-d4-proxy-port-measure-1` · decisions-log "revisit" stub `7f33d1c` | Turns on Axis-2A proxy-population tracking (model re-homed to `simulation/spatial_gauntlet/proxy_population.py`, AST byte-identical) and re-measures the archive under tracking. | **No design objection — infrastructure; jack-ryan's gate.** The re-home is byte-identical; the flag is a measurement-plumbing switch, not a balance lever. Promote the existing "Decisions to revisit" stub (`7f33d1c`) to a live decision. I defer the engineering judgment to jack-ryan. |
| **3** | `apply_max_profile_investment` default → ON | gamora · `gamora/v-keystone-live-integration-2` | Measures kit power on **faithful** loadouts (vs the stripped baseline). Honest 8.19× keystone multiplier in-harness. | **ENDORSE — and it composes with the locked MOB_HP 1.5x anchor.** At 1.5x the keystone is load-bearing (stripped melee floors to 0.367; faithful hits 1.000), so measuring kit power on faithful loadouts is the *representative* measurement at the locked anchor. The two decisions point the same direction (MOB_HP note §coherence). **This is the flip that carries the band-refit consequence — see Tier-2 below.** |

**Why separate commits + smoke per flip:** attribution + independent revert. If #3's re-measure cascades into a band-refit we want to hold, separate commits let us keep #1/#2 live and revert only #3. One squashed flip-commit forecloses that.

## The re-measure is intrinsic to #2 and #3 (not a follow-on)

- **#2** without a re-measure tracks nothing — the flag is meaningless un-exercised. Flip ON → re-measure the archive (Axis-2A).
- **#3** changes *what* "kit power" means (faithful vs stripped). The archive's kit-power numbers were measured stripped; under #3 they must be re-measured faithful to be coherent.
- **Both re-measures produce a new mobs/min distribution** — which is exactly the input to the band-refit check below. Route the re-measure output to gandalf at run-close.

## Run-start discipline (fire before dispatching)

1. **Pull + reconcile-against-disk, BOTH repos.** `git pull origin main` in collab AND engine. Confirm the three commits/tags above exist on disk in `reincarnated-engine/`.
2. **Confirm the autonomous-run engine tags' push state (§7).** RETURN-PACKAGE §7 listed all autonomous-run engine tags as unpushed on disk. The flip commits **stack on top of them**, so the run-close push gate must carry the whole stack (the §7 tags + the new flip commits + jack-ryan's decisions-log entries). Reconcile what's actually pushed vs on-disk before assembling the gate — do not assume.
3. **Read the rationale source.** This file + `agentic_orchestration/gandalf/notes/2026-06-17-mob-hp-anchor-design-read.md` (the locked MOB_HP 1.5x anchor + its §coherence note that #3 reinforces). jack-ryan's three declarations cite the gandalf rationale in the table above.

## Decision envelope (three tiers)

**Tier 1 — KR autonomous (decide + auto-commit, no ask):**
- Sequence the three flips #1→#2→#3; dispatch gamora (flip + smoke + re-measure per flip) and jack-ryan (declare + confirm clean per flip); collect.
- gamora's flip commits + jack-ryan's findings + decisions-log entries + KR coordination artifacts all auto-commit (authorized cycle work).
- Routine smoke-clean confirmations, attribution tags, MIGRATION notes.

**Tier 2 — escalate to gandalf (design judgment — do NOT decide):**
- **The band-refit call (the one real design hinge in this run).** The mobs/min bands in `gauntlet_sim.py` (~L308–309) are empirically fit to the 2026-06-16 determined slice (`output/kpm-band-spatial-recal-full-20260616_232152.json`, **n=3078 mobs/min**) and carry a "RE-FIT CANDIDATE" provenance tag. The MOB_HP→1.5x lock means the *MOB_HP* refit trigger does NOT fire (bands hold). BUT #3 changes the measurement regime (faithful vs stripped → faster clears → higher mobs/min), which is a *different* trigger. **When #3's re-measure lands, compare its mobs/min distribution against the n=3078 band-fit basis. If it materially drifts, that is a gandalf band-refit call — escalate to me. If it doesn't, bands hold and the run closes clean.** Do NOT pre-emptively refit the bands; let the re-measure data vote.
- **Keystone ceiling-artifact interaction.** If the #3 faithful-loadout re-measure surfaces the keystone 1.000 zero-loss-variance ceiling interacting with the measurement in a way that changes the kit-power read (vs merely confirming the 8.19× multiplier), flag me — that is the separate "is the keystone over-tuned" ticket (MOB_HP note §4.1), and I do not want #3's ratification to silently absorb it.

**Tier 3 — escalate to Matt (exceeds the run framing):**
- Push-to-remote (default Matt-ask per ADR-006; surface a PUSH GATE at run-close — see §7 stack note above).
- Any outcome that would change the **locked** balance reference (the MOB_HP 1.5x anchor or the band fit) beyond a mechanical refit — that re-opens a locked decision and is Matt's, not KR's.
- Any scope amendment (e.g., re-measuring beyond the archive into new scenario generation).

## Run-close protocol

- Collect per flip: gamora's flip commit + smoke result; jack-ryan's decisions-log semantic-shift declaration + clean-flip confirmation.
- Route to gandalf: the #2/#3 re-measure mobs/min distribution + a one-line "material drift vs n=3078: YES/NO" read, so I can make (or decline) the band-refit call.
- Surface a **PUSH GATE** listing the full stack (§7 autonomous-run tags + the three flip commits + jack-ryan's decisions-log entries); do NOT push without Matt go.
- Report: per-flip status (flipped / smoke / declared / confirmed-clean), the routed-to-gandalf re-measure package, and the push gate.

---

## ── PASTE-READY KR SESSION-OPENER (copy below this line) ──────────────

```
Execute session-start protocol per your OP § 1, then fire a three-flip ratification run.

RUN: flip THREE OFF-by-default production flags LIVE, all in gamora's simulation
seam (reincarnated-engine/), each as a SEPARATE commit + smoke, with a jack-ryan
decisions-log semantic-shift declaration per flip. All three were built + Gate-2
PASSED behind OFF defaults during the 2026-06-17 autonomous run; all git-revertible.
Matt declared the semantic shift ("flip all 3") — that declaration is the gate.

RUN-START DISCIPLINE (before dispatching):
- git pull origin main in BOTH collab and engine repos; reconcile-against-disk.
- Confirm the three commits/tags exist on disk in reincarnated-engine/:
  #1 F1 geometry-fix      104bfbc  gamora/v-f1-geometry-fix-1
  #2 track_proxy_population af5c8b2 gamora/v-d4-proxy-port-measure-1 (revisit stub 7f33d1c)
  #3 apply_max_profile_investment   gamora/v-keystone-live-integration-2
- Reconcile the §7 autonomous-run engine tags' push state — the flip commits STACK
  on them, so the push gate carries the whole stack. Do not assume; check.
- Read gandalf's rationale: agentic_orchestration/gandalf/requests/2026-06-17-kr-flag-flip-run-prompt.md
  + agentic_orchestration/gandalf/notes/2026-06-17-mob-hp-anchor-design-read.md.

SEQUENCE (in order — #1 is the precondition for honest re-measure):
- #1 FIRST: ratify the geometry-fix LIVE. It is the W-F precondition AND the
  precondition for honest re-measurement (the spatial swarm path must run on real
  geometry before any new mobs/min distribution is trusted). gandalf: ENDORSE.
- #2: flip track_proxy_population ON + re-measure the archive (Axis-2A). Promote
  the existing "Decisions to revisit" stub (7f33d1c) to a live decision. gandalf:
  no design objection — infrastructure; jack-ryan's gate.
- #3: flip apply_max_profile_investment ON + re-measure kit power on faithful
  loadouts. gandalf: ENDORSE + composes with the locked MOB_HP 1.5x anchor (at
  1.5x the keystone is load-bearing, so faithful-loadout measurement is the
  representative measurement). #3 carries the band-refit consequence (Tier-2).

ROUTING:
- gamora: flip each (separate commit + smoke + re-measure for #2/#3).
- jack-ryan: write 3 decisions-log semantic-shift declarations (one per flip),
  citing the gandalf rationale; confirm each flip smoke-clean.
- you (KR): sequence; hold the push gate.

DECISION ENVELOPE:
- Tier 1 (you decide + auto-commit): sequence, dispatch, collect; gamora flips +
  jack-ryan findings/decisions-log + your coordination artifacts auto-commit.
- Tier 2 (escalate to gandalf — do NOT decide):
  (a) BAND-REFIT CALL — the mobs/min bands in gauntlet_sim.py (~L308-309) are fit
      to the 2026-06-16 determined slice (kpm-band-spatial-recal-full-...232152.json,
      n=3078). MOB_HP→1.5x lock means the MOB_HP refit trigger does NOT fire. But
      #3 changes the measurement regime (faithful vs stripped → faster clears →
      higher mobs/min). When #3's re-measure lands, compare its distribution vs the
      n=3078 basis; if it materially drifts, that's a gandalf band-refit call.
      Do NOT pre-refit; let the data vote.
  (b) keystone ceiling-artifact: if #3's faithful re-measure surfaces the 1.000
      zero-variance ceiling changing the kit-power read (vs confirming 8.19x),
      flag gandalf — that's the separate "keystone over-tuned" ticket.
- Tier 3 (escalate to Matt): push-to-remote; any outcome that would change the
  LOCKED balance reference (MOB_HP 1.5x anchor or band fit) beyond a mechanical
  refit; any scope amendment (re-measuring beyond the archive).

RUN-CLOSE:
- Route to gandalf: the #2/#3 re-measure mobs/min distribution + a one-line
  "material drift vs n=3078: YES/NO" read.
- Surface a PUSH GATE listing the full stack (§7 tags + 3 flip commits +
  jack-ryan decisions-log entries); do NOT push without Matt go.
- Report: per-flip status (flipped/smoke/declared/confirmed-clean), the routed-to-
  gandalf re-measure package, and the push gate.
```

## ──────────────────────────────────────────────────────────────────────

**gandalf holds on return:** the band-refit call (Tier-2a) if #3's re-measure materially drifts from the n=3078 basis, and the keystone-ceiling watch (Tier-2b). Everything else closes inside KR + jack-ryan + gamora. The MOB_HP-lock decisions-log entry (separate, already routed to KR-draft / jack-ryan-review) can ride in the same session's decisions-log pass if convenient — but it is not gated on this run.

**Signed:** gandalf, 2026-06-17.
