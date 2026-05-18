# 2026-05-18 — rocket — RE-FIRE: new-season regen 002016 at canonical-6 (HARDENED)

**Authority:** Matt L3 re-fire authorization 2026-05-18 (verbatim: "re-fire rocket regen").
**Type:** Pattern A re-fire — same scope as prior dispatch `2026-05-18-rocket-new-season-regen-canonical-6-002016.md` with **subprocess-survival hardening**.
**Predecessor (FAILED):** prior dispatch's `python regen_002016_canonical_6.py` was launched via `run_in_background=true` inside rocket's agent session. When the agent session ended (context exhaustion / wrapper completion), the subprocess was killed. No `season_002016` directory exists; no tag; ~$0 LLM spent (regen never finished the balance loop). Forensics: `scripts/regen_002016_canonical_6.py` survives on disk (573 lines, untracked); `output/standard-demo-regen-2026-05-18/` is empty; no python process running for regen.
**Status:** 🟢 **ACTIVE — fire immediately. Rocket idle.**

---

## Root cause of prior failure (and how to avoid this time)

**Cause:** `run_in_background=true` from inside an agent session ties the subprocess lifetime to the agent process. When the agent exits (any cause — context exhaustion, wrapper completion, normal session end), all background children die with SIGTERM.

**Fix pattern (this dispatch):** detach the subprocess from the agent session entirely. Three layered defenses:

1. **`nohup` + `setsid`** — detach from controlling terminal and process group so SIGHUP / SIGTERM from the agent shell does not propagate.
2. **Explicit log file at a stable path** — `/tmp/regen_002016.log` — so the next session (or you) can verify progress without depending on the agent's session-scoped output buffer.
3. **Script self-reports completion** — the regen script writes a sentinel file `output/standard-demo-regen-2026-05-18/REGEN_COMPLETE.json` at successful exit. Knight-rider or rocket-next-session can poll for that file rather than relying on the agent's notification.

---

## Launch protocol (DO THIS EXACTLY)

```bash
# From engine repo root, with venv active:
cd /Users/admin/Games/reincarnated-engine
source .venv/bin/activate  # or however the engine env activates

# Detached launch — survives any agent session ending:
nohup setsid python scripts/regen_002016_canonical_6.py \
  > /tmp/regen_002016.log 2>&1 < /dev/null &

# Capture PID for later reference:
echo $! > /tmp/regen_002016.pid

# Verify it's detached (parent should be PID 1 within a few seconds):
sleep 2 && ps -o pid,ppid,pgid,sid,comm -p $(cat /tmp/regen_002016.pid)
# Expected: ppid=1 (init), pgid != shell pgid, sid different — proves detachment.
```

**Then return immediately.** Do NOT wait or sleep-poll inside the agent session. Do NOT use a Monitor on the agent side — the monitor itself dies with the agent. The script will run for ~30-60 min independently.

Before exiting the agent session, write a single-line status to `agentic_orchestration/dispatches/2026-05-18-rocket-new-season-regen-002016-RE-FIRE.md` (under "## Detach record") with:
- Launch timestamp
- PID at `/tmp/regen_002016.pid`
- Log path `/tmp/regen_002016.log`
- Sentinel path `output/standard-demo-regen-2026-05-18/REGEN_COMPLETE.json`

Then exit cleanly. Knight-rider will pick up the sentinel + log in the next session.

---

## Required script amendment (small but essential)

Before launching, amend `scripts/regen_002016_canonical_6.py` to write the completion sentinel at successful exit (so we can detect completion without relying on the agent):

```python
# At the very end of main(), AFTER successful demo + loadout sync:
import json as _json
sentinel_path = Path("output/standard-demo-regen-2026-05-18/REGEN_COMPLETE.json")
sentinel_path.parent.mkdir(parents=True, exist_ok=True)
sentinel_path.write_text(_json.dumps({
    "completed_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    "season_id": "002016",
    "convergence_rate_pct": <computed>,
    "per_archetype_convergence": <dict>,
    "wall_clock_min": <computed>,
    "llm_cost_usd_estimate": <computed>,
    "status": "SUCCESS",
}, indent=2))

# At any HALT path (e.g., if any archetype < 20% convergence), write status="HALTED" sentinel
# with diagnostic dict, so post-mortem doesn't require reading the full log.
```

Also at the very start of `main()`, write a `REGEN_STARTING.json` sentinel with `started_at` + `pid` so post-mortem can confirm the script entered execution.

---

## Required reading

1. Prior dispatch: `agentic_orchestration/dispatches/2026-05-18-rocket-new-season-regen-canonical-6-002016.md` — scope is unchanged; this dispatch is purely about subprocess survival
2. `scripts/regen_002016_canonical_6.py` — already authored; only sentinel additions needed
3. `reincarnated-engine/MIGRATION.md` (simulation) — v1.13 tail; v1.14 entry to be appended on completion

---

## Scope (UNCHANGED from prior dispatch)

Single full new-season regen at canonical-6:
- D10 substrate-coherent generation (canonical-7 substrates; gen pool is 6 archetypes since rocket/v1.17 retire)
- D11.1 element-coverage tax (alpha=0.08)
- Discipline #17 environment fidelity — gear_catalog present during balance computation
- gauntlet_recipe.json emitted (star-lord v1.7 schema)
- Engine staged output → demo public/seasons → loadout data/season_002016 sync
- MIGRATION.md v1.14 entry on success
- Tag `rocket/v1.18-new-season-regen-canonical-6-002016-1`

Expected convergence: ~75-85% canonical (gate at < 20% any archetype → HALT-and-flag).

LLM budget: ~$2-5 (≤ $10 hard cap).

---

## Acceptance criteria

- [ ] `scripts/regen_002016_canonical_6.py` amended with sentinel-write logic (start + end)
- [ ] Subprocess launched detached per protocol above (ppid=1 verified)
- [ ] `/tmp/regen_002016.pid` written
- [ ] Detach record appended to this dispatch (path + PID + log path + sentinel path)
- [ ] Agent exits cleanly without waiting on subprocess
- [ ] (Out-of-session) `output/standard-demo-regen-2026-05-18/REGEN_COMPLETE.json` appears within ~60 min
- [ ] (Post-completion) tag `rocket/v1.18-new-season-regen-canonical-6-002016-1` applied
- [ ] (Post-completion) MIGRATION.md v1.14 entry appended

---

## Out of scope (DO NOT)

- ❌ DO NOT use `run_in_background=true` from inside the agent session for the regen script (that's what killed it last time)
- ❌ DO NOT sleep-poll the subprocess inside the agent — exit and let it run
- ❌ DO NOT use a Monitor inside the agent (the monitor will die with the session)
- ❌ DO NOT exceed $10 LLM cost (HALT if cost-tracking shows runaway)
- ❌ DO NOT generate hybrid_mage classes (canonical-6 enforced)
- ❌ DO NOT push tag (ADR-006)
- ❌ DO NOT pre-empt drax v1.20 (parallel-safe; different repo)

---

## Coordination

- **Predecessor:** prior dispatch died at balance-loop stage; sentinel re-fire is hardened replacement
- **Triggers downstream (post-completion):**
  - Knight-rider reads sentinel → surfaces convergence stats + season metadata to Matt
  - Matt manual Suno music workflow (pick season name + flavor → Suno → audio drop → drax SEASON_IDS update)
  - Drax SEASON_IDS pointer update (separate dispatch knight-rider fires)
  - Star-lord telemetry validation (task #177)
- **Parallel-safe with:** drax v1.20 mobile + bug fix dispatch (different repo; no conflict)

---

*Dispatched 2026-05-18 by knight-rider per Matt L3 re-fire authorization. ~30-60 min subprocess wall-clock; ~5-10 min agent-session work (amend script, launch detached, write detach record, exit). Append completion record to this dispatch AFTER sentinel observed.*

---

## Detach record

*(rocket appends here at launch — agent-session work; do NOT include completion data here)*

---

## Completion record

*(rocket-next-session or knight-rider appends here AFTER `REGEN_COMPLETE.json` sentinel is observed)*
