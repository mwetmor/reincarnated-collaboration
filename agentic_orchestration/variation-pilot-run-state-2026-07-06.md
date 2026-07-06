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

## Calibration-note Gate-1 disposition (2026-07-06) — RATIFY-WITH-CONDITIONS

Critique-pair on `simulation/notes/proxy-magnitude-calibration-math-2026-07-06.md` (gamora `066ba37`). Both critics RATIFY-WITH-CONDITIONS. Math verified sound; NO Matt decision at this Gate; NO BLOCK; no MIGRATION.md (decl shape unchanged, ADR-004 untriggered).

- **jack-ryan** (technical, `cb040b0`): every load-bearing number verified first-hand (KPM bands `gauntlet_sim.py:393-398`; WR-1.0 anchors + gravecaller quote `proxy-fight-calibration:302-304`; `None or 0.0` coalesce + `damage_modifier=1.0` default `spatial_engine.py:1741-1742,1773`; `SPATIAL_DAMAGE_SCALE=0.6` `:326`).
- **gandalf** (design, per Matt's design-eyes requirement): endorses marginal-value frame ("the only frame that refuses to ship a lie"); proxy-dominant ceiling is a *design gate*, not a balance clamp.

**The crux resolved — ranged/melee caveat does NOT block the re-fight.** jack-ryan: the re-fight runs CLEAR shells (packs), not boss shells; gravecaller's WR 0.0 was a BOSS-specific nav evaporate; on a dense pack field the nearest-enemy nav gap is far less binding. So the pack re-fight IS the honest empirical test of whether the melee-derived anchor transfers to a ranged proxy — **the primitive question is answered BY the fight, not before it.** The ranged/melee tier split, if needed, is a rocket-seam generation primitive (ADR-002) escalated to knight-rider WITH re-fight evidence — not a sim patch, not masked by a magnitude bump (gandalf concurs, structural).

**Binding conditions on the calibrated re-emit + caster re-fight:**
1. **(jack-ryan #1, non-optional)** Engagement gate BEFORE reading KPM — a nav evaporate must not be misread as a magnitude shortfall. **This operationalizes Matt's "does the emitted thing FIGHT?" run-boundary check.**
2. **(jack-ryan #2)** State the 0.6-vs-1.0 `damage_modifier` regime as an explicit harness parameter (silent 1.67× otherwise).
3. **(jack-ryan #3)** No DPS lever on above-ceiling pack shells — survivability only.
4. **(jack-ryan #4 + gandalf #2)** Ranged-primitive escalation to knight-rider carries re-fight evidence; ranged-nav-evaporate is STRUCTURAL — do NOT mask with magnitude.
5. **(gandalf #1)** Grade `[0.15, ~0.30)` f_army share as "balance-passing / fantasy-marginal" on the read — no silent PASS. Ranged floor likely higher than melee floor.
6. **(gandalf #3, emission-time)** When rocket emits varied summoners, summons must READ as the summoner's own (thematic coherence with element/name/weapon), not generic proxies.

**Sequencing:** pilot solo baseline fills gamora's open slot → rocket calibrated re-emit (chassis-coordinate magnitudes + engagement-gate hook) → gamora caster-cell-only re-fight (~20 min) under conditions 1-5 → ranged-primitive question surfaces to KR/Matt only IF the pack re-fight shows the melee anchor doesn't transfer.
