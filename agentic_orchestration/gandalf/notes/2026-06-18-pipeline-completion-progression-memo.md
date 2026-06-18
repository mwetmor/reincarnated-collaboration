# Wind-down memo — progression toward battle-sim + gen-pipeline completion

**STATUS:** MEMO (gandalf wind-down survey + progression diagram + autonomous-run-eligibility classification)
**Date:** 2026-06-18
**Author:** gandalf (story-and-design steward)
**Purpose:** map the steps remaining toward (A) **battle-sim completion** and (B) **engine gen-pipeline completion**; classify each step blocked vs unblocked; identify which steps a **pre-authorization note converts to autonomous-run-eligible** (Matt's "overnight run" question).
**Method:** reconciled against disk — two Explore surveys of `reincarnated-engine/` (simulation seam + generation seam) + the gear-spec §7 architecture record + the catalogue substrate. Cited file:line throughout. NOT from session memory.
**Survey-mode discipline:** §1–§4 report **what EXISTS** (descriptive). §5–§6 are the forward classification Matt asked for (the "what unblocks" judgment) — kept separate from the state survey per the cross-cutting rule.

---

## 0. The shape in one line

**Each pipeline is blocked at exactly ONE gandalf chokepoint — battle-sim at the Stage-2c band ruling, gen-pipeline at the §7.1 manifest design-owned half — and both chokepoints are mine to clear.** Clear those two (a focused gandalf work-item each, authorable from on-disk substrate, neither needs Matt), add the already-given "flip all 3" + one push pre-authorization, and a single unattended run can take **both pipelines most of the way to completion.** The only items that genuinely cannot ride an unattended run are the push gate (ADR-006), two design calls (keystone-ceiling, caster-coverage) whose *investigations* can run while the *calls* park, and the procgen-tool adoption (Tier-3, off both critical paths).

---

## 0.5 — CORRECTION (2026-06-18, post-Matt-reframe + reconcile-against-disk; GOVERNS where it conflicts with §0–§6)

Three corrections landed after the first draft — two reconcile-against-disk catches, one Matt reframe of what "gen-pipeline completion" means. The original §1–§7 are preserved as the first-draft record; **where they conflict with this block, this block governs.**

### C1 — "Gen-pipeline" traced the WRONG pipeline (Matt's reframe)

The original §2(B)/§3/§4-gen-rows/§5–§6 traced the **gear-spec VISUAL asset path** (emitted gear item → renderable spec: manifest → master ShaderMaterial → constrained-LLM fill → L4 adapter → render). That is a real pipeline — but it is **downstream, visual-only, and deferred behind the Synty catalogue.** It is NOT what Matt meant.

**What Matt meant (verbatim):** "the end-to-end serial content-creation pipeline which results in a season of kits/factions/monsters/npcs/gear/weapons/flavortext (the full JSON emission that Godot will need for the replica of the battle sim to run)." That is the **content-emission** pipeline — the MECHANICAL + NARRATIVE content the SIM consumes, not the visual render-specs. The gear-spec visual path (original §3) is a *downstream RENDER sub-pipeline of the "gear/weapons" leg*, not the emission spine. Corrected picture below.

### C-PIPE — The real content-emission pipeline (completion state, from disk)

```
CONTENT-EMISSION PIPELINE (Matt's "gen pipeline") — what produces a season's sim-ready JSON
═══════════════════════════════════════════════════════════════════════════════════════════
 NO single end-to-end driver. TWO emit tracks that do NOT meet:

 TRACK NEW (cycle-14 wave5) — kit+faction-rich, emits to the LOADOUT app:
   run_season_production.py → wave5_season_orchestrator.run_season_production()
     P2 kit-candidates → 2.5 variant-enum → 3 gauntlet+PM1-cluster
       → 4 mechanical-archive (kit_archive.db) → 4.5 PM1-rerun
       → 5 cohesion-judge LLM (faction identity / season name / inter-faction rel / per-kit names)
       → 7 joint-gate
     → cycle14_wave5_emitter.emit_season() ──▶ reincarnated-loadout/data/.../classes/*.json
        (KIT-ONLY: no monsters; skill flavor_text NULL; main_weapon NULL)

 TRACK OLD (season_exporter) — produces the SIM-READY bundle, but driver DELETED + kit/monster/gear-only:
   [generate-season CLI — DELETED, b6-stack deletion] → season_exporter.export_season()
     ──▶ exports/<id>/{metadata, classes, monsters, gear_pool, gauntlet_recipe}.json
        (monsters ✓+flavor, gear ✓+flavor, kits ✓+flavor; factions ABSENT, npcs ABSENT, weapon=null)

 THE GAP ◄══ THE REAL CHOKEPOINT: the two tracks don't meet. NO pipeline emits all 7 content
   types into the sim-ready bundle. cycle-14 content never reaches season_exporter; season_exporter
   never gets factions / npcs / weapon-descriptors / cycle-14 kits. "Completion" = a single driver
   that emits ALL 7 types into one Godot-consumable bundle.
```

**Per-content-type completion (the honest 7-row state):**

| Content type | State | Evidence (file) |
|---|---|---|
| **kits** | WORKING | `exports/season_001010/classes.json` — full `stat_distribution` + skills + LLM names; cycle-14 54 kits w/ 12 skills |
| **factions** | PARTIAL — generated, NOT in sim-ready bundle | Phase-5 Wave-A LLM live; `ExportSeason.faction_clusters` schema exists (`schemas.py:1174`) but `_export_season_inner()` never writes it |
| **monsters** | WORKING (old) / MISSING (cycle-14) | `monsters.json` 44 w/ stats+flavor (`monster_generator.py:389`); cycle-14 P2–7 is **kit-only** |
| **npcs** | MISSING | no `ExportNPC` schema, no npc generator anywhere |
| **gear** | WORKING | `gear_pool.json` 200 items + stats + rolled_effects + LLM names |
| **weapons** | PARTIAL — substrate binding in-kit, not emitted as descriptor | `main_weapon=None` in every export; no `weapons.json`; weapon identity lives in `substrate_weapon_binding` (phase2 intermediate) |
| **flavortext** | WORKING (class/monster/gear) / GAP (cycle-14 skill flavor NULL) | `naming.py` live Anthropic calls; cycle-14 skill `flavor_text` null |

**The single biggest blocker:** the **split emit path** — the kit/faction-rich cycle-14 pipeline emits to the loadout app, not the sim-ready `exports/<id>/` bundle; the bundle-producing `season_exporter` path is kit/monster/gear-only with its driver deleted. Reaching a complete season JSON for the Godot sim replica needs: (a) a single driver that routes cycle-14 content through (or replaces) `season_exporter`, (b) **monster generation wired into the cycle-14 track** (it's kit-only today), (c) **faction_clusters actually written** to the bundle (schema present, writer absent), (d) the **weapon descriptor** wired through from `substrate_weapon_binding` → `main_weapon`, (e) an **NPC emitter built from zero** (no schema, no generator). This is a real, scoped engineering map — and it is mostly **rocket + star-lord seam work**, not a gandalf chokepoint. My role here is design-spec'ing the missing emitters' CONTENT (what an NPC IS, what faction JSON carries to the sim, what flavortext the sim needs) — not building them.

### C2 — Stage-2c was ALREADY done (NOT a gandalf chokepoint)

§0/§2/§4(row)/§5–§6 treated Stage-2c (KPM-band ruling) as "blocked-on-gandalf." **Falsified by disk:** Stage-2c was ruled + wired (Stage-2d, `92c040f`, MIGRATION v1.76) + Gate-2-closed (`2b8b502`, interim guard LIFTED) on **2026-06-16**. The bands are live in `gauntlet_sim.py` `ENCOUNTER_COHORT_KPM_BAND`, matching the n=3078 empirical distribution exactly. The "READY FOR GANDALF" in `AGENT_STATE.md:4269` is a **stale checkpoint** never back-edited after 2c/2d landed (flag for gamora). My independent re-derivation from the raw n=3078 data CONFIRMS the asymmetric-band logic. **Stage-2c needs confirmation, not re-ruling — it is closed.**

### C3 — The two "lower-confidence" items (§2 diagram L64–65), traced + dispositioned

- **BC-coordinate cutover Stage-2 Unit-2+** — this was the REAL battle-sim gandalf chokepoint (Stage-2c being already-done). "BC" = Battle-Coordinate, the 8-axis bin tuple replacing the archetype LABEL as the pipeline's structural hub. Stage-1 (rocket/gen) complete; Stage-2 (gamora/sim) implementation landed per MIGRATION v1.70; the equivalence run (`output/stage-2-bc-keying-equivalence-2026-06-14.txt`, N=1120/arm/archetype) passed **16/16 archetypes at `0.00/0.00/0.000`** but escalated ONE WARN-1a envelope-width flag (`damage_long_collapse` water/earth/holy/shadow, W_ttk=24.42% > cap) to gandalf. **RULED THIS SESSION → ACCEPT** (the over-wide envelope is element-intrinsic flavor spread the cutover preserves exactly, not ordering-driven differentiation the collapse would flatten; A1 earth_caster case=2 re-confirmed). See `2026-06-18-bc-coordinate-cutover-stage2-envelope-escalation-ruling.md`. This **clears the genuine battle-sim gandalf gate**; jack-ryan Gate-2 on the implementation + Stage-3 prove-then-delete are the downstream gated steps.
- **open-shell floor residual** — a Stage-2c sub-question, **already RESOLVED**: gandalf ruled **option (a) empirical central mass** (open_arena band `[9.90, 15.53]`, unimodal p10/p90), accepting that realized spatial throughput sits ~0.63× the RESOLVE theoretical floor because RESOLVE's `A/√R` assumes pure-TMPM with no spatial overhead (travel/telegraph/approach). Wired in Stage-2d, ratified in decisions-log. **Closed.** (Another over-flag by the first draft — it read as open but disk shows it ruled.)

**Net correction to §0's headline:** the battle-sim gandalf chokepoint was NOT Stage-2c (already done) — it was the **BC-coordinate Stage-2 envelope gate, now ruled this session.** The "gen-pipeline" gandalf chokepoint (§7.1) is real but is the **VISUAL** path; Matt's **content-emission** pipeline is a separate, mostly-rocket/star-lord engineering map (C-PIPE) whose gandalf surface is design-spec'ing the missing emitters' content, not a single ruling.

---

## 1. What "completion" means (the two targets)

- **(A) Battle-sim complete** = the measurement apparatus is **honest** (geometry-aware spatial resolution [#1], faithful-loadout kit power [#3], MOB_HP-anchored [✓ locked 1.5x]) AND the mobs/min bands are **ruled + wired** (Stage-2c→2d) AND the open balance questions are **dispositioned** (W-F adoption live; keystone-ceiling + caster-coverage either fixed or explicitly parked with a criterion). "Done" for a gauntlet run is empirically defined: 18 SC-6 endgame encounters, terminal pass-floor 9-of-18 in-band per cohort per kit (`gauntlet_sim.py:109,158`).
- **(B) Gen-pipeline complete** = the gear-spec asset path runs **end-to-end** (manifest → master ShaderMaterial → constrained-LLM fill → L4 adapter → render), the catalogue substrate feeds it, and the six-profile emission apex lands. Procgen-assembly tooling is **off this path** (Tier-3, deferred — nothing depends on it).

---

## 2. Battle-sim progression diagram

```
BATTLE-SIM COMPLETION
═════════════════════
 ✓ MOB_HP 1.5x LOCKED (arena.py:49) ─────────────┐ (composes with #3)
                                                  ▼
 #1 geometry-fix ──▶ #2 proxy-track ON ──▶ #3 keystone-faithful ON
 (104bfbc)            (af5c8b2,+remeasure)   (gamora/v-keystone…-2,+remeasure)
 [PRE-AUTH:           [PRE-AUTH]              [PRE-AUTH]
  "flip all 3"]                                   │
      │                                           ▼
      │                                    archive re-measure
      │                                           │
      │                                           ▼
      │                              band-refit?  ⟵ GANDALF Tier-2
      │                              (pre-specifiable drift threshold;
      │                               under→bands hold, over→PARK)
      ▼
 spatial-proxy ─┐
  mechanic port │      ┌── Stage-2c BAND RULING  ◄══ GANDALF CHOKEPOINT #1
 [additive build]│     │   (AGENT_STATE:4269 "READY FOR GANDALF";
      │          │     │    n=3078 data on disk — I can clear now)
      │          │     ▼
      │          │  Stage-2d band wiring  [additive, gated on 2c]
      │          │
      └──────────┴────────────┐
                              ▼
                      W-F ADOPTION  ──▶ measurement apparatus HONEST + LIVE
                  (gated on #1 + proxy-port + Stage-2c)

 OPEN — design judgment, NOT on the additive path:
   • keystone-ceiling "over-tuned" ticket  (1.000 zero-variance ceiling;
       investigation autonomous, the CALL parks)
   • caster coverage-bound failure  (session-13: 3.3× HP move = ΔWR ~0.02;
       spatial/timeout limit, independent of mob HP; needs gandalf scenario-
       design spec BEFORE implementation is eligible)

 LOWER-CONFIDENCE / further-out (surfaced, not fully traced):
   • BC-coordinate cutover Stage-2 Unit-2+ (deferred pending a gandalf review)
   • open-shell floor residual (Stage-2c sub-question)
```

## 3. Gen-pipeline progression diagram

```
GEN-PIPELINE COMPLETION
═══════════════════════
 ✓ §7.6 StyleProfile ruling (DONE — styleprofile-output-shape-ruling-2026-06-17)
 ✓ catalogue substrate (157 packs / 62,281 assets; 5-axis tagged;
                         Option-A consumption rule: bind iff mode ∈ {A,B})
 ✓ §7.2 restyle-leaf build (rocket 5f85014; Gate-2 869c31b; conformance ENDORSED)
        │
        ▼
 §7.1 MANIFEST  ◄══ GANDALF CHOKEPOINT #2
   = design-owned half (GANDALF — element-flavor tint/finish menu +
                        provisional metal/leather labels + intent)
   + substrate slice  (ELROND — per-mesh mode + zone-count + sockets;
                       IN-FLIGHT, dispatched 837dd7f)
   [design-half: I can clear now │ elrond-slice: additive, already moving]
        │
        ▼
 §7.2 master ShaderMaterial (rocket)  [additive, gated on §7.1]
        │
        ├──▶ §7.3 star-lord constrained-LLM fill  [additive, gated]
        ├──▶ §7.5 drax L4 adapter → Godot .tres   [additive, gated]
        │
        ▼
   end-to-end GEAR-SPEC GEN COMPLETE ──▶ six-profile set apex (emission aura)

 PARALLEL / DEFERRED — off the critical path:
   • §7.4 galadriel render pass — locks provisional metal/leather labels
       (additive; one import render; fires once any mesh imports)
   • procgen-assembly tool — Tier-3, Matt-gated; NOTHING depends on it
   • B0 descent render run-to-green — gandalf-driven, in-flight (separate sub-pipeline)
```

---

## 4. Node-by-node — blocked vs unblocked

| Node | Pipeline | State | Blocked on |
|---|---|---|---|
| MOB_HP 1.5x anchor | sim | ✓ DONE (locked this session) | — |
| #1 geometry-fix flip | sim | in-flight (run prompt authored) | Matt's "flip all 3" given → only PUSH |
| #2 proxy-track flip + re-measure | sim | in-flight | same |
| #3 keystone-faithful flip + re-measure | sim | in-flight | same |
| **Stage-2c band ruling** | sim | **blocked-on-gandalf** | **gandalf (CHOKEPOINT #1)** |
| Stage-2d band wiring | sim | gated | Stage-2c |
| band-refit-after-#3 | sim | gated | #3 re-measure (pre-specifiable) |
| spatial-proxy mechanic port | sim | gated | additive build |
| W-F adoption | sim | gated | #1 + proxy-port + Stage-2c |
| keystone-ceiling ticket | sim | OPEN | design call (gandalf+Matt) |
| caster coverage-bound | sim | OPEN | gandalf scenario-design spec |
| §7.6 ruling | gen | ✓ DONE | — |
| catalogue substrate | gen | ✓ DONE | — |
| §7.2 restyle-leaf | gen | ✓ BUILT (unpushed) | — |
| **§7.1 manifest design-half** | gen | **blocked-on-gandalf** | **gandalf (CHOKEPOINT #2)** |
| §7.1 elrond substrate slice | gen | in-flight (837dd7f) | additive dispatch |
| §7.2 master ShaderMaterial | gen | gated | §7.1 |
| §7.3 star-lord LLM-fill | gen | gated | §7.1 + §7.2 |
| §7.5 drax L4 adapter | gen | gated | §7.2 |
| §7.4 galadriel render pass | gen | DEFERRED (additive) | mesh import (parallel-able) |
| procgen tool adoption | gen | DEFERRED | Matt Tier-3 (off-path) |
| PUSH (both pipelines) | — | standing gate | Matt (ADR-006) |

---

## 5. Autonomous-run eligibility — what a pre-authorization note unblocks

Three classes (this is the answer to Matt's "which can be unblocked with a pre-authorization note for an overnight run"):

**Class (i) — ALREADY pre-authorized (the note exists or is trivial):**
- **The three flag-flips (#1/#2/#3).** Matt said "flip all 3"; the run prompt (`requests/2026-06-17-kr-flag-flip-run-prompt.md`) is the note. Unattended-safe because the one design hinge — the band-refit-after-#3 — **parks** rather than auto-fires (pre-registered drift threshold; under→bands hold, over→PARK for gandalf). Residual Matt-gate: the PUSH only.

**Class (ii) — UNBLOCKABLE by a gandalf pre-clear (the high-leverage move):**
The two chokepoints are mine. Clearing them is a focused gandalf work-item each (authorable from on-disk substrate — the n=3078 characterization for Stage-2c; the §7.6 ruling + six-profile architecture for the §7.1 design-half), **neither needs Matt.** Clearing them converts a large downstream from blocked → autonomous-eligible additive builds:
- **Stage-2c band ruling cleared** → unblocks Stage-2d band wiring + (with proxy-port) W-F adoption.
- **§7.1 manifest design-half cleared** (+ elrond's in-flight slice) → unblocks §7.2 master ShaderMaterial → §7.3 LLM-fill + §7.5 L4 adapter → **end-to-end gear-spec gen.**
- Plus the always-additive items that ride alongside: spatial-proxy mechanic port, §7.4 galadriel render pass.

**Class (iii) — genuinely CANNOT ride an unattended run (Matt or live-design):**
- **The PUSH gate** (ADR-006) — unless Matt pre-authorizes a push-pattern for the run ("push at run-close"), as the charter convention allows.
- **keystone-ceiling "over-tuned" CALL** — the *investigation* (loss-variance under varied keystone magnitudes) is autonomous-eligible; the *design call* parks for Matt/gandalf.
- **caster coverage-bound failure** — needs a gandalf **scenario-design spec** before any implementation is eligible (it's a spatial/coverage/timeout fix, independent of mob HP — the flip run does NOT touch it). I can author that spec; then implementation becomes eligible.
- **procgen-assembly tool adoption** — Tier-3 cost/tooling, Matt's call. Off both critical paths, so it blocks nothing.

---

## 6. The pre-authorization note — what it would take to maximally advance both pipelines unattended

If Matt wants a single unattended autonomous run that takes both pipelines as far as they can go, the charter needs exactly three inputs:

1. **Two gandalf pre-clears (mine — next gandalf session, not Matt's):**
   - Stage-2c band ruling (from the on-disk n=3078 data) — a genuine ruling, not a rubber-stamp; it's the highest-leverage single gandalf item in the battle-sim pipeline.
   - §7.1 manifest design-owned half (element-flavor tint/finish menu + provisional labels) — the highest-leverage single gandalf item in the gen pipeline.
   - *(Optional third, lower-leverage: the caster-coverage scenario-design spec — converts that OPEN item to eligible. Worth doing if the run has headroom.)*

2. **The "flip all 3" run** (already authorized) folded into the same charter, with the band-refit-after-#3 set to **PARK on drift** (pre-registered threshold) so it's unattended-safe.

3. **One Matt input: a push pre-authorization** ("push at run-close," per the standing charter convention) — otherwise every commit accumulates unpushed and the run's value sits on disk until the next Matt session.

**Decision envelope for the run (the 2026-06-17 three-tier pattern):**
- **Tier 1 (autonomous):** all additive builds (§7.2 master shader, §7.3, §7.5, §7.4 render, spatial-proxy port, Stage-2d wiring) close via the jack-ryan Gate-2 critique-pair + my pre-registered endorse-criteria.
- **Tier 2 (PARK for gandalf — do NOT decide):** band-refit if #3 re-measure drifts past threshold; any keystone-ceiling interaction; any schema contradiction.
- **Tier 3 (PARK for Matt):** push (unless pre-authorized); keystone-ceiling design call; procgen adoption; any locked-decision re-open (MOB_HP 1.5x / band fit beyond mechanical refit).

**What the run would deliver if all three inputs are in place:** battle-sim measurement apparatus honest + live (flips ratified, bands ruled+wired, W-F adopted); gen-pipeline end-to-end gear-spec generation (manifest→shader→fill→adapter→render). That is the bulk of BOTH completion targets in one unattended pass — bounded by the two design calls that correctly park (keystone-ceiling, caster-coverage) and the push gate.

---

## 7. Sign-off

The two pipelines are not blocked on Matt and they are not blocked on engineering capacity — they are each blocked on **one gandalf ruling I have not yet authored.** That is the actionable finding: the next gandalf session's highest-leverage work is clearing Stage-2c (band ruling) and §7.1 (manifest design-half), because those two pre-clears are what convert "blocked" into "an unattended run can finish it." The flip run is authorized and routed; the push and the two design calls are the named residual.

**Signed:** gandalf, 2026-06-18.
