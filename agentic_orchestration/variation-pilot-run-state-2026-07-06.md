# Variation Pilot — run state (2026-07-06)

> Authored by knight-rider at Leg-3 launch. Records Matt's FORK RULING (Option 1 — fire the inert pilot now) and its four riders, so Leg-4 analysis and batch-2 sequencing honor them. Live ledger.

## Launch record

- **Fired:** 2026-07-06 ~14:54 local, detached (`nohup`, PID 11337) from persistent KR session per Discipline #19 (NOT a sub-agent).
- **Driver:** `star-lord/v-pilot-leg3-driver-1` (engine `2ac1ee6`), `reincarnated.export.variation_pilot_driver`.
- **Log:** `reincarnated-engine/src/reincarnated/output/variation_pilot_run.log`.
- **Checkpoints:** generation → `output/variation_pilot_generation_checkpoint.json`; gauntlet → `simulation/output/pilot/…`. Recovery: `--recover-from-canonical <path>`.
- **Completion sentinel:** `VARIATION PILOT COMPLETE`. Registry: `emission_runs WHERE season_id LIKE 'variation-pilot%'`.
- **Expected wall:** ~35–40 min. **Cells:** one physical-melee (full variation), one caster (G4 proxy knob live ~0.25).
- **PROXIES INERT BY DESIGN this run:** emitted proxy magnitudes = `None` → `_spawn_one_ally` resolves `None or 0.0 = 0.0` → `_is_fighting_decl=False`. Summoned allies do not fight. This is expected and is the reason for the four riders below.

## Matt's four riders (FORK RULING — binding on Leg 4 + batch 2)

### Rider 1 — Roster trigger DISARMED for this run, BOTH directions
- **No summoner seat fills from an inert-proxy fight.** A fail-artifact (~0 survivors) is NOT "summoners fail." A pass-artifact is WORSE: a proxy-dominant kit that clears on its non-summon remainder is NOT a validated summoner — seating it ships the F1 hazard as a demo kit whose skeletons stand there doing nothing.
- **Summoner seats fill ONLY from a live-proxy fight** (post-calibration re-fight).
- **Plain-caster survivors (~75) KEEP caster-seat candidacy** — their read is clean (no proxy dependence).

### Rider 2 — Leg-4 attribution PRE-REGISTERED (before data lands)
- Proxy-dominant results report as **"solo-baseline, summons inert by design"** — NEVER as summoner viability, in either direction.
- Emitted-vs-curated SIM comparison is DEFERRED to the re-fight.
- Take the FREE STATIC version now: emitted proxy-dominant tree shape / skill composition / offer-table vs the 2 curated summoners' structure — **no sim** — feeds calibration.

### Rider 3 — Calibration fires as its own gated task, IN PARALLEL (LAUNCHED)
- gamora math-note on proxy-magnitude architecture. Frame = **marginal value** (required summon contribution = clear-shell bar − solo baseline; baseline arrives from this run within the hour). Empirical anchors = the 2 certified curated summoners' known-good magnitudes (WR 1.0 both shells) scaled to chassis coordinates.
- **Gate-1 critique-pair on the note** (design eyes REQUIRED: summon strength is class-fantasy surface, not just a balance constant).
- Then calibrated re-emit + re-fight of the **CASTER CELL ONLY** (~20 min).
- **Status:** gamora math-note dispatched as background task at Leg-3 launch. Gate-1 (jack-ryan + gandalf) fires when note lands.

### Rider 4 — Batch-2 gains a NAMED GATE
- **Gates-on:** `proxy-magnitude-calibration` · `calibrated-caster-re-fight`.
- Leg-4 go/no-go is a **CONDITIONAL go** (all learnings EXCEPT summoner survival); the re-fight finalizes it.
- Firing batch-2 before calibration would reproduce inert summons at 18-cell scale. DO NOT fire batch-2 full-spectrum until both gate items clear.

## Process lesson (Matt-flagged — for critique-pair run-boundary checklist)
- Holding the launch was CORRECT — the inert-proxy finding was a **premise-change to Leg-4 outputs, not a seam call**.
- rocket's `magnitudes=None` is a **legitimate layer-handoff** (named owner, named task), correctly caught at shell-prep.
- BUT the Gate-1 pass should have PRICED its Leg-4 consequence. **New checklist question: "does the emitted thing FIGHT?" joins the run-boundary checklist.** Route to jack-ryan + gandalf for the critique-pair operating-procedure / engineering-disciplines record.

## Leg-4 deliverables (pending pilot completion)
1. Solo caster baseline (KPM) → feeds gamora calibration note's open slot.
2. Melee-cell variation report (distinct t4/geometry/chains/role-split/resource — mechanics not palette per Ruling 2).
3. Caster-cell variation report + static emitted-vs-curated summoner structural comparison (Rider 2).
4. Conditional go/no-go framed per Rider 4.
