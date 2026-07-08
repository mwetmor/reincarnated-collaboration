# Decisions-log entry PROPOSAL — §6 spatial-difficulty fork ruling (A / YES / YES)

> **✅ FOLDED / AUTHORED 2026-07-08 (jack-ryan).** This proposal was authored into the decisions-log as the entry **"2026-07-08 — Endgame-BC gauntlet un-stacks MOB_HP_DIFFICULTY_MULTIPLIER (Option A); serial-engagement pass authorized"**, batched + cross-linked with the F4 registration + R4 cert-contract + §4-reframe Lane-3 entries. The two parked-workstream Status edits (log 4240 + 5223 → SCOPE-RETIRED) were applied per format skill §5. Finding: `qa/findings/2026-07-08-jackryan-f4-registration-gate2-lane3.md`. This file is retained as the KR draft-of-record; no longer pending.

**Proposer:** knight-rider (capture obligation per batch2-run-state line 837)
**For authoring by:** jack-ryan (sole decisions-log authoring authority per decision-log-format skill §1)
**Routing:** KR-drafted → jack-ryan reviews + authors into `~/Games/reincarnated-engine/design/decisions/decisions-log.md` → Matt already approved the underlying ruling (2026-07-08, verbatim "I agree with the 1-2 asks (A/yes/yes)")
**Batch with:** R3a Gate-2 reviews (Option-A un-stack + serial-engagement math-notes) — this proposal can be authored alongside those since it documents the ruling those changes implement.

---

## Proposed entry (canonical format — jack-ryan edits as needed)

### 2026-07-08: Endgame-BC gauntlet un-stacks MOB_HP_DIFFICULTY_MULTIPLIER (Option A); serial-engagement pass authorized

**Decision**: The endgame-BC spatial-gauntlet path stops applying `MOB_HP_DIFFICULTY_MULTIPLIER` (Option A, "un-stack"). The constant itself stays `1.5`, untouched, for the legacy convergence instrument it was ruled for (2026-05-19). The parked, Matt-scheduling-pending multiplier-recalibration workstream (decisions-log 4240 + 5223) is thereby **resolved as SCOPE-RETIREMENT — no constant moves.** Separately, a serial-engagement (pack-local activation) design pass is authorized for `open_arena` + `magic_pack` so open rooms engage in proximity waves rather than total-field alpha-strike.

**Reasoning**: The endgame-BC WR surface is saturated at both rails (323 floor / 278 ceiling events, every extreme exactly 0.000 or 1.000, no mid-band mass) — a step function, not a gradient: the definition of an uncalibrated difficulty instrument (gandalf design read §1). Three difficulty dials moved independently since the last joint calibration and were never re-ruled together: per-mob HP regime (~2,019→26,500, ~13×, 2026-05-28 endgame profile), the legacy ×1.5 runtime multiplier (ruled 2026-05-19 for the OLD regime + 8-mob rooms, still stacking in 2 of 3 rooms), and room density+geometry (open_arena 8→~40, magic_pack 4→~24, 2026-07-07 F1/F2 re-population). The 2026-05-28 endgame profile explicitly bakes durability into the stat spec *"rather than applying a runtime multiplier"* and declares it "DOES NOT modify arena.py"; the gauntlet path applied the legacy multiplier on top anyway — two difficulty systems from two eras stacking. Option A resolves which ruling governs endgame difficulty in favor of the one that already claimed that ground; it is NOT Goodhart-softening (gamora's rider-5 refusal to move a parked constant to green a gate stands — no constant moves). The `1.5→1.25` remedy the v3 log suggested was wrong in KIND: `MOB_HP_DIFFICULTY_SCENARIOS={open_arena, chokepoint_corridor}` excludes magic_pack, yet magic_pack accounts for 111 of 323 floor events, and everyone walls the corridor at the HIGHEST per-mob HP while casters floor magic_pack at the LOWEST — so HP is not the discriminant; engagement geometry is. Serial-engagement restores both the rooms' stated certification intent ("repositioning cost" presumes engagements to reposition between) and genre open-field grammar (D2 pack-local aggro, D3 density pulls, PoE pack spacing).

**Alternatives considered**:
- **Option B — extend + re-rule the multiplier** (add magic_pack to scope, re-derive per-scenario values). Rejected: doubles down on the runtime-multiplier pattern the endgame profile explicitly retired, proliferates parked constants, and §1 shows HP is not the discriminant.
- **Option C — per-scenario difficulty spec block** (HP factor + density + clock as one governed structure per scenario). Not rejected but deferred: the right EVENTUAL shape if the scenario family keeps growing; more machinery than the current unblock needs; a compatible follow-on to A, not an alternative.

**Status**: Active

**Related**:
- Design read: `agentic_orchestration/gandalf/notes/2026-07-08-spatial-difficulty-levers-design-read.md` (§§1-6)
- Design finding (source): `agentic_orchestration/gamora/notes/2026-07-08-spatial-floor-saturation-g1-g2-design-finding.md` (G1/G2)
- Dispatch: `agentic_orchestration/dispatches/2026-07-08-gamora-starlord-spatial-floor-diagnosis.md`
- Run-state ruling block: `agentic_orchestration/batch2-run-state-2026-07-06.md` (Matt ruling 2026-07-08, lines 817-841)
- Prior decisions superseded/annotated: decisions-log 4240 + 5223 (parked multiplier-recalibration workstream → now SCOPE-RETIRED; jack-ryan: edit those entries' Status to reference this ruling per format skill §5)
- Endgame profile ruling: engine `endgame_mob_stat_profile.py:8-16` (2026-05-28, "rather than applying a runtime multiplier")
- Legacy multiplier origin: `spatial_gauntlet/arena.py:49` (commit `24cdc7e`, 2026-05-19 R2 recalibration) + application site `spatial_engine.py:3441`
- Riders 1/4/5 of the gandalf Lane-C verdict

---

## Notes for jack-ryan (not part of the entry)

- Per format skill §5: the two parked-workstream references (decisions-log 4240 + 5223) should get their Status edited to point at this new entry (SCOPE-RETIRED, not moved). KR flags but leaves the append-only status-edit to your authoring authority.
- The serial-engagement radii + the un-stack application-site change land as gamora math-notes with their own Gate-2s in R3a; this entry documents the RULING, not the implementation values (those are captured in the math-notes + commits).
- The conditional Lever-4 certification-criterion ruling is NOT captured here — it fires (or doesn't) later, with data, and gets its own entry if ruled.
