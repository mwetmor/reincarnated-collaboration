# 2026-05-18 — rocket — RESEED: new-season regen 002017 at canonical-6 (seed-variance test)

**Authority:** Matt L3 2026-05-18 morning verbatim "fire reseed 2017. Sensible." Authorization for re-seed per knight-rider L3-3 recommendation (re-seed before lowering modifier floor or applying archetype DPS cap).
**Type:** Pattern A re-seed — identical to `2026-05-18-rocket-new-season-regen-002016-RE-FIRE.md` with `SEASON_SEED = 2017` swap. ~30-60 min wall-clock.
**Predecessor:** `2026-05-18-rocket-new-season-regen-002016-RE-FIRE.md` HALTED at convergence drift gate (3/10 = 30%; seed-variance hypothesis or structural).
**Status:** 🟢 **ACTIVE — fire immediately. Rocket idle pending Matt L3.**

---

## Why this matters — hypothesis test framing

**Hypothesis A (seed-variance):** Seed 2016 was a statistical outlier; the canonical-6 generation pool is sound; floor-pinning is incidental to this seed's kit rolls. Confirmed if seed 2017 converges ≥70%.

**Hypothesis B (structural):** Post-canonical-6 class pool genuinely has insufficient range below `BALANCE_MODIFIER_FLOOR=0.055`; floor-pinning is systemic. Confirmed if seed 2017 ALSO fails at <70%.

Evidence for A (which the hive bets on):
- Hunter archetype has 1.82 modifier range across seeds (B14.5 sidecar finding)
- ~75% expected failure rate is canonical (jack-ryan twin entry)
- earth_caster + wind_controller + experimental converged FINE on seed 2016 — argues against systemic kit-shape issues
- D11 hybrid_mage was ARCHETYPE-specific structural; that pattern hasn't reproduced cross-archetype here

If hypothesis A confirmed: ship season 002017 for Suno music workflow + drax SEASON_IDS update.

If hypothesis A falsified: knight-rider authorizes seed 2018 as third data point; if 002018 also fails, escalate to Option 2 (lower modifier floor with gamora math note + jack-ryan Gate-1).

**Do not iterate beyond 3 seeds without escalation.** Three data points → structural conclusion → stop empirical iteration → do the math note.

---

## Root cause of detach-pattern (and how to avoid)

Same as 002016 RE-FIRE dispatch: detached subprocess survives agent wrapper exit. Three-layer defense unchanged:

1. **`nohup`** (macOS has no `setsid` — verified in 002016 RE-FIRE; nohup alone with shell wrapper achieved ppid=1 detachment)
2. **Explicit log file** at `/tmp/regen_002017.log`
3. **Sentinel files** — `REGEN_STARTING.json` at script start + `REGEN_COMPLETE.json` (status=SUCCESS or status=HALTED) at exit

Sentinel pattern validated end-to-end on 002016 run (PID 17673 ran ~50min detached, wrote HALTED sentinel cleanly). Reuse without modification.

---

## Launch protocol

```bash
# From engine repo root, with venv active:
cd /Users/admin/Games/reincarnated-engine
source .venv/bin/activate  # or however the engine env activates

# Detached launch — survives any agent session ending:
nohup python3 scripts/regen_002017_canonical_6.py \
  > /tmp/regen_002017.log 2>&1 < /dev/null &

# Capture PID for later reference:
echo $! > /tmp/regen_002017.pid

# Verify it's detached (parent should be PID 1 within a few seconds):
sleep 2 && ps -o pid,ppid,pgid,sid,comm -p $(cat /tmp/regen_002017.pid)
# Expected: ppid=1 (init) — proves detachment.
```

**Then return immediately.** Do NOT wait or sleep-poll inside the agent session. Do NOT use a Monitor on the agent side — the monitor itself dies with the agent. The script will run for ~30-60 min independently.

Before exiting the agent session, write a single-line status to this dispatch (under "## Detach record") with:
- Launch timestamp
- PID at `/tmp/regen_002017.pid`
- Log path `/tmp/regen_002017.log`
- Sentinel path `output/standard-demo-regen-2026-05-18/REGEN_COMPLETE.json` (same staging dir as 002016 — see Required script amendment below for collision-avoidance)

Then exit cleanly. Knight-rider picks up the sentinel + log in the next session.

---

## Required script: clone + reseed

Author `scripts/regen_002017_canonical_6.py` as a copy of `scripts/regen_002016_canonical_6.py` with the following changes:

1. `SEASON_SEED = 2017` (was 2016)
2. `SEASON_ID = "002017"` (was "002016") — applied to all output paths + metadata
3. Output staging dir: `output/standard-demo-regen-2026-05-18/season_002017/` (parallel to season_002016/)
4. Sentinel paths:
   - `output/standard-demo-regen-2026-05-18/REGEN_STARTING_002017.json` (suffixed to avoid collision with 002016 sentinel)
   - `output/standard-demo-regen-2026-05-18/REGEN_COMPLETE_002017.json` (suffixed)
5. Demo sync target: `~/Games/reincarnated-demo/public/seasons/season_002017/`
6. Loadout sync target: `~/Games/reincarnated-loadout/data/season_002017/`

Everything else (canonical-6 archetype pool enforcement, D10 substrate-coherent generation, D11.1 element-coverage tax α=0.08, Discipline #17 gear_catalog environment fidelity, gauntlet_recipe.json emission, convergence drift gate at <20% any-archetype HALT) stays identical.

---

## Convergence drift gate (UNCHANGED from 002016)

If any archetype shows <20% convergence → HALT and write `REGEN_COMPLETE_002017.json` with `status=HALTED` + per-archetype diagnostic dict. Don't sync to demo/loadout on HALT.

Expected convergence per design canon: ~75-85%. Gate failure threshold: any one archetype below 20%.

---

## Required reading

1. **Predecessor RE-FIRE dispatch:** `agentic_orchestration/dispatches/2026-05-18-rocket-new-season-regen-002016-RE-FIRE.md` — full launch protocol + sentinel pattern (validated end-to-end on 002016)
2. **002016 HALT diagnostic:** `output/standard-demo-regen-2026-05-18/convergence_drift_diagnostic.json` — the data we're comparing against
3. **MIGRATION.md v1.14:** appended after 002016 HALT; 002017 will append v1.15 on completion
4. **D11 hybrid_mage pattern (memory):** `~/.claude/projects/-Users-admin-Games-reincarnated-collaboration/memory/MEMORY.md` "B14.5 sidecar analyses" entry (hunter 1.82 modifier range; seed variance well-documented)
5. **Reincarnated engine engineering disciplines:** `reincarnated-engine/design/working-agreement/engineering-disciplines.md` (Discipline #17 environment fidelity in particular)

---

## Acceptance criteria

- [ ] `scripts/regen_002017_canonical_6.py` authored as 002016 clone + reseed
- [ ] Subprocess launched detached per protocol above (ppid=1 verified at t+3s)
- [ ] `/tmp/regen_002017.pid` written
- [ ] Detach record appended to this dispatch (path + PID + log path + sentinel path)
- [ ] Agent exits cleanly without waiting on subprocess
- [ ] (Out-of-session) `REGEN_COMPLETE_002017.json` appears within ~60 min
- [ ] (Post-completion) tag `rocket/v1.19-new-season-regen-canonical-6-002017-1` applied
- [ ] (Post-completion) MIGRATION.md v1.15 entry appended
- [ ] (If HALT) status=HALTED sentinel + diagnostic captured — surface to knight-rider for L3-3-followup escalation
- [ ] (If SUCCESS) demo public/seasons/season_002017 + loadout data/season_002017 synced; tag applied

---

## Out of scope (DO NOT)

- ❌ DO NOT use `run_in_background=true` from inside the agent session for the regen script (002016 lesson: kills subprocess on agent exit)
- ❌ DO NOT sleep-poll the subprocess inside the agent — exit and let it run
- ❌ DO NOT use a Monitor inside the agent
- ❌ DO NOT exceed $10 LLM cost (HALT if cost-tracking shows runaway)
- ❌ DO NOT generate hybrid_mage classes (canonical-6 enforced)
- ❌ DO NOT modify `BALANCE_MODIFIER_FLOOR` or any tuning constant — this is a SEED CHANGE ONLY, not a structural fix attempt
- ❌ DO NOT iterate to seed 2018 without knight-rider authorization (need to see 002017 result first)
- ❌ DO NOT push tag (ADR-006)
- ❌ DO NOT pre-empt drax v1.20.2 / chest-replacement / v1.22 camera zoom or any sprint Track work (parallel-safe; different repo)

---

## Coordination

- **Predecessor:** 002016 RE-FIRE HALT — sentinel + diagnostic + MIGRATION.md v1.14 staged
- **Triggers downstream (if SUCCESS):**
  - Knight-rider reads sentinel → surfaces convergence stats + season metadata (002017 anchor + theme + elements + cosmological vocab) to Matt
  - Matt manual Suno music workflow (pick season name + flavor → Suno → audio drop → drax SEASON_IDS update)
  - Drax SEASON_IDS pointer update for 002017 (separate dispatch knight-rider fires post-completion)
  - Star-lord telemetry validation (task #177 still pending)
- **Triggers downstream (if HALT):**
  - Knight-rider escalates L3-3-followup to Matt: "002017 also failed; recommend seed 2018 as 3rd data point OR escalate to Option 2 (lower modifier floor)"
- **Parallel-safe with:** All overnight sprint specialist work (Track A/B/C dispatches in queue); drax demo work; loadout work; star-lord any analytics manifests
- **PRE-SIGNAL § 14.1.1** before hive-log appends

---

*Dispatched 2026-05-18 morning by knight-rider per Matt L3 re-seed authorization. ~30-60 min subprocess wall-clock; ~5-10 min agent-session work. Sentinel-based completion detection (no agent-side polling).*

---

## Detach record

- Launch timestamp: 2026-05-18T10:19:29Z
- PID: 22486 (written to `/tmp/regen_002017.pid`)
- ppid=1 verified at t+3s — detachment confirmed
- Log path: `/tmp/regen_002017.log`
- Start sentinel written: `output/standard-demo-regen-2026-05-18/REGEN_STARTING_002017.json`
- Completion sentinel path: `output/standard-demo-regen-2026-05-18/REGEN_COMPLETE_002017.json`
- Script: `scripts/regen_002017_canonical_6.py` (seed=2017, season_002017 paths, suffixed sentinels)
- Launched by rocket agent session; script running independently (~30-60 min wall-clock)

---

## Completion record

*(rocket-next-session or knight-rider appends here AFTER `REGEN_COMPLETE_002017.json` sentinel is observed)*
