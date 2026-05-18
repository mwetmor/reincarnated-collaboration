# 2026-05-18 — rocket — New-season regen at canonical-6 (season 002016) — Matt L3 AUTHORIZED

**Authority:** Matt L3 verdict 2026-05-18 — "New-season regen authorization — canonical-6 chain locked; ready to fire whenever you greenlight." Greenlit.

**Type:** Pattern B — full LLM-generated season + balance loop + gauntlet + monsters + gear + recipe; ~30-60 min wall-clock + ~$2-5 LLM cost.

**Predecessor chain (all complete):**
- ✅ Canonical-6 transition (gandalf v1.11 + jack-ryan v1.6/v1.7/v1.8 + rocket v1.17 + drax v1.17 is_retired filter)
- ✅ D11 cycle CLOSED + Discipline #17 environment-fidelity amendment in place
- ✅ All 4 VS2a JSON-parity invariants closed (drax v1.16/v1.16.1/v1.16.2/v1.17)
- ✅ Audio + visual demo experience-blockers cleared (drax v1.16.2 + v1.17; drax v1.18 WSP wire-in in flight)
- ✅ rocket v1.17 generation pipeline smoke confirmed canonical-6 (5/5 clean; 44/44 balance_loop tests pass)

**Status:** 🟢 **ACTIVE — fire immediately. Matt L3 authorized.**

---

## Why this matters

This is Matt's stated milestone: *"develop a completely new LLM generated season once we feel those issues are resolved and converge many classes from it."* The engine has been stabilized through D10 + D11.2 cycle; hybrid_mage retired; canonical-6 locked; demo + loadout consume cleanly. A fresh new-season regen at canonical-6 validates that the engine is end-to-end healthy on never-before-seen content — and provides the season that gets the manual Suno music workflow + full playtest.

---

## Required reading

1. **Your v1.17 completion record** — `agentic_orchestration/dispatches/2026-05-18-rocket-canonical-6-archetype-removal-plus-is-retired-flag.md` § completion (your generation pipeline state; smoke verdict; MIGRATION.md v1.13)
2. **Gandalf canonical-6 doc** — `canonical/story/canonical-6-transition-retire-hybrid-mage-2026-05-18.md` (archetype list § 4; identity-DNA redistribution § 5)
3. **D11.2 advisory** — `canonical/story/d11-2-structural-redesign-advisory-2026-05-17.md` (lever rationale; if any archetype lags in new regen, Lever B retained for potential reuse per gandalf doc)
4. **Discipline #17** — `reincarnated-engine/design/working-agreement/engineering-disciplines.md` (smoke gate with environment fidelity amendment; apply if any post-regen archetype shows convergence drift)
5. **Your standard regen pipeline** — wherever the standard-demo-regen entry point lives (`scripts/` or main season_orchestrator); you've run this before (002011-015 batch)

---

## Scope — six deliverables

### Deliverable 1 — Single new season at canonical-6 (season_002016)

Fire the standard regen pipeline targeting **season_002016**:
- 6 archetypes (no hybrid_mage)
- ~50 classes total per typical season distribution
- All 7 substrates active (canonical-7 → canonical-6 affects archetype list, not substrate list)
- D10 substrate-coherent generation rules
- Element-coverage tax (D11 alpha=0.08 from D11.1) — apply consistently
- Standard gauntlet emission + monster pool generation + gear pool generation
- Gauntlet recipe emission (star-lord v1.7 schema; auto-emitted now)

Output destinations:
- Engine staged: `reincarnated-engine/output/standard-demo-regen-<date>/season_002016/`
- Demo: `reincarnated-demo/public/seasons/season_002016/`
- Loadout: `reincarnated-loadout/data/season_002016/`

Use your existing v1.13.2 / v1.14-d11.1-demo-sync + v1.14-d11.1-loadout-sync patterns for the sync.

### Deliverable 2 — Convergence stats + telemetry

After regen completes, report convergence stats:
- Total classes generated: <N>
- Converged (interior modifier > 0.055): <X>/<N>
- Floor-pinned (modifier <= 0.055): <Y>/<N>
- Convergence rate: <X/N as %>
- Per-archetype convergence breakdown (6 archetypes)
- Per-substrate convergence breakdown (7 substrates)
- Flag any archetype with convergence rate < 50% (potential D-series-style sprint candidate post-VS2a)

Expected per design constant: ~75-85% convergence rate (75% expected failure rate canonical per jack-ryan twin entry; surviving classes filter through).

### Deliverable 3 — Convergence drift detection

Per Discipline #17 environment-fidelity amendment, ensure:
- Smoke environment dimensions matched production (gear_catalog + monster_pool present during balance computation)
- No archetype shows D11-style floor-pinning at 0-6% convergence
- If any archetype shows < 20% convergence: HALT regen; surface to Matt + knight-rider with diagnostic (which archetype, what WR distribution, suspected cause)
- If all archetypes converge ≥ 50%: proceed to sync; healthy regen

### Deliverable 4 — Engine + demo + loadout sync

If convergence is acceptable:
- Sync engine output → demo public/seasons/season_002016/classes.json + monsters.json + gear_pool.json + metadata.json + gauntlet_recipe.json
- Sync engine output → loadout data/season_002016/classes/<id>.json per-class files
- Verify drax SEASON_IDS pointer can be flipped (knight-rider will fire drax SEASON_IDS update dispatch post-regen)

### Deliverable 5 — Telemetry capture

Star-lord seam (per v1.5 orchestrator wiring + pending v1.10 columns from gamora D11.2):
- Ensure ClassBalanceResult rows captured for all 50 classes
- Note: gamora v1.11 added hybrid_mage_dps_scale_factor + composite_d_active columns; these stay default (no hybrid_mage in regen) — verify schema doesn't error on the new columns

### Deliverable 6 — MIGRATION.md v1.14 entry + completion record

Append v1.14 to MIGRATION.md:
- Description: first new-season regen at canonical-6; season 002016 shipped
- Convergence rate vs canonical 75% expected
- Per-archetype breakdown
- Any flags / follow-on dispatches needed

Completion record in this dispatch with:
- Final convergence stats
- Cost breakdown (LLM tokens, $ estimate)
- Wall-clock time
- Any anomalies surfaced
- New-season metadata (season name, theme, flavor text — for Matt's Suno music workflow)

---

## Acceptance criteria

- [ ] Season 002016 fully generated (classes + monsters + gear_pool + metadata + gauntlet_recipe)
- [ ] Convergence stats reported with per-archetype + per-substrate breakdown
- [ ] No archetype < 20% convergence (HALT + escalate if so)
- [ ] Demo + loadout sync completed
- [ ] Telemetry rows captured for all classes
- [ ] MIGRATION.md v1.14 entry appended
- [ ] LLM cost reported (≤$5 expected)
- [ ] Wall-clock time reported
- [ ] PRE-SIGNAL § 14.1.1 before hive-log append
- [ ] AGENT_STATE STATE entry
- [ ] Tag `rocket/v1.18-new-season-regen-canonical-6-002016-1`

---

## Out of scope (DO NOT)

- ❌ DO NOT generate multiple seasons (single 002016; Matt iterates after playtest)
- ❌ DO NOT exceed $10 LLM cost (~$5 typical; HALT + surface if budget overrun)
- ❌ DO NOT generate hybrid_mage classes (canonical-6 enforced; if generation slips, that's a regression to flag)
- ❌ DO NOT modify Lever B code (retained with retirement comment per v1.17)
- ❌ DO NOT pre-empt mobile chain (drax v1.18 in flight; v1.19 mobile audit + Tier 1.5 queued)
- ❌ DO NOT fire drax SEASON_IDS update (separate dispatch knight-rider fires post-your-completion)
- ❌ DO NOT push tag (ADR-006)
- ❌ DO NOT touch hybrid_mage staged classes (canonical-6 chain locked them is_retired; preserve)

---

## Coordination

- **Predecessors:** entire canonical-6 chain (5 agents) + VS2a JSON-parity chain
- **Triggers downstream:**
  - drax SEASON_IDS pointer update (knight-rider fires post-completion)
  - Matt manual Suno music workflow (Matt picks season name + flavor → Suno → audio library update → drax Layer 5 manifest swap)
  - Matt full playtest of season 002016
  - Star-lord telemetry analysis (post-playtest convergence analysis)
  - Possible D12+ archetype-specific sprint (only if a new laggard archetype surfaces; expected NOT to fire)
- **Parallel-safe with:** drax v1.18 WSP wire-in (in flight; different repo); elrond chierit mapping (in flight; different repo)
- **PRE-SIGNAL § 14.1.1** before hive-log appends

---

## Post-regen path forward (informational; not your work)

1. Knight-rider surfaces convergence stats + season metadata to Matt
2. Matt loads season name + flavor text into Suno → generates music → drops tracks at audio library path
3. Drax SEASON_IDS update dispatch fires (point demo at 002016)
4. Matt full playtest of canonical-6 season 002016
5. Star-lord telemetry analysis post-playtest
6. If convergence + playtest are both healthy → VS2a CRITICAL PATH SUBSTANTIALLY COMPLETE → mobile polish + remaining Tier 5.1/5.2 elrond + chierit monsters become the final lap

---

*Dispatched 2026-05-18 by knight-rider per Matt L3 authorization. ~30-60 min wall-clock + ~$5 LLM. Append completion record with convergence stats + season metadata when done.*
