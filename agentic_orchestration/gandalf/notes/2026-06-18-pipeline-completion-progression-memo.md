# Wind-down memo — progression toward battle-sim + gen-pipeline completion

> **⚠ SUPERSEDED 2026-06-23 → `canonical/story/current-to-end-state.md`** (the LIVING consolidated tracker that absorbs this memo's progression map + the disk-verified spine + the v2 gameplay-loop design + the horde-gap finding). This memo remains as lineage; **where it conflicts with the living doc, the living doc governs.** Do not update this file — update the living doc.

**STATUS:** SUPERSEDED (was: MEMO — gandalf wind-down survey + progression diagram + autonomous-run-eligibility classification)
**Date:** 2026-06-18
**Author:** gandalf (story-and-design steward)
**Purpose:** map the steps remaining toward (A) **battle-sim completion** and (B) **engine gen-pipeline completion**; classify each step blocked vs unblocked; identify which steps a **pre-authorization note converts to autonomous-run-eligible** (Matt's "overnight run" question).
**Method:** reconciled against disk — two Explore surveys of `reincarnated-engine/` (simulation seam + generation seam) + the gear-spec §7 architecture record + the catalogue substrate. Cited file:line throughout. NOT from session memory.
**Survey-mode discipline:** §1–§4 report **what EXISTS** (descriptive). §5–§6 are the forward classification Matt asked for (the "what unblocks" judgment) — kept separate from the state survey per the cross-cutting rule.

---

## SESSION-DELTA 2026-06-21 — LATEST LAYER (GOVERNS ALL BELOW, including the 2026-06-20 delta + §0.5)

The 2026-06-20/21 session closed the boss-half of the instrument-validity workstream and launched a combined autonomous run that closes the rest of the solo battle-sim instrument and brings the proxy/summoner question to the edge of an architecture decision. **Where this block conflicts with the 06-20 delta or §0–§8, this block governs.**

### BATTLE-SIM PROGRESS — what changed (the honest-apparatus criterion, 06-20 D1, is now CLOSED for boss shells)

- **The §6 boss-gate doctrine is BUILT + Gate-2 PASS + canonical-written** (`d5b7ac2`). Boss shells leave the KPM band onto **survive-and-kill within the 240s enrage timer** (binary; DPS/TTK measured-never-gating; no over-performance ceiling). This is the win-condition split Matt ADOPTED 2026-06-19.
- **The STR "inversion" resolved as HONEST substrate drift, not a bug.** §5 predicted STR fails boss shells (timeout=1.000); the composed instrument measured STR PASSING (1.000) — STR was starved (mana-default + T1-only) and is now funded by the Phase R economy + Phase 2 rotation. Gate-only diff; fight path byte-unchanged (jack-ryan verified). STR ships boss shells via the rotation/economy lever, NOT via DoT.
- **The `mini_boss` caster-wipe diagnosed as a stale-calibration DEFECT** (same class as the four workstream targets): 100% timeouts / 0% deaths, caused by a 150s `soft_timeout` (calibrated to a ~3s-TTK regime) + a `mini_boss` HP roll ABOVE the full boss. Fixed recompose-first (soft_timeout→None; HP floored ≤ boss). **The inversion is GONE** (int 0.000→0.681, wis 0.000→0.563, dex 0.667, str 1.000). Matt **ratified the "smaller boss" identity**.
- **Both boss shells BANKED** (un-escrow draft `2b80306`, awaiting Matt disposition approval). → **The boss-half of the single tail-refit is COMPLETE.**
- **06-20 D1 (instrument bias) status:** the armor/resist asymmetry that re-opened the honest-apparatus criterion is the **Phase 4** target — symmetrized + Gate-2 PASS (`d2d3dde` / `8dde097`, "boundary 4 of 4"). All four instrument-validity defects (economy/rotation/DoT/armor) are addressed. **The boss shells are banked on the honest composed instrument** → the honest-apparatus criterion is CLOSED for boss shells; clear shells still need the magnitude pass + re-band (now in-flight, below).
- **IN-FLIGHT — the combined autonomous run (LAUNCHED 2026-06-21):** Track 1 closes the **solo Profile-A instrument**: T1.1 magnitude pass (clear-shell timing-floor) → T1.2 absolute-magnitude-constant sweep (task #11: the live-upstream `mini_boss` HP-factor range + V5 >1.0 artifact) → T1.3 clear-shell re-band (the deferred half of the single tail-refit) → T1.4 Phase 6 reads (STR encounter-segregated + mixed-pack focus-fire). Run plan: `gandalf/requests/2026-06-21-track1-track2-combined-autonomous-run-plan.md`.

### CONTENT-EMISSION PROGRESS — spine UNCHANGED; the "kits" leg gains an asterisk (summoner/proxy)

- **The emit-spine is structurally UNCHANGED since 06-18:** still two emit tracks that do not meet (TRACK NEW → loadout; TRACK OLD `season_exporter` → sim-ready bundle, driver deleted); the join is rocket/star-lord plumbing, NOT a gandalf chokepoint. The combined run does NOT touch the emit-spine (it is battle-sim + proxy, not the join). **Zero movement on the plumbing this session.**
- **NEW refinement to the "kits" leg (the 7-row/6-type table's `kits WORKING`):** the kits leg is incomplete in a newly-surfaced way — **it excludes the genre's ~25% summoner/proxy archetype.** The ~25% reservation IS encoded (`bc_target_cell_sampler.py` curated roster = 5/25 proxy-heavy + 3/25 proxy-light; intent doc `v1-bc-target-intent-2026-05-24.md` line 101: none ~75% / light ~10% / heavy ~15%) but **DEFERRED at composition** (`bc_target_composer.py:318` `_DEFERRED_PROXY_BINS`, "sim is solo-only; proxy-creation mechanics absent"). Cycle-14 shipped **0 proxy-heavy, 3 sub-threshold proxy-light INT** (familiar-augment, which track INT-solo exactly). So **season-1 kits currently ship with zero real summoners.** Read the table row as **kits-WORKING-for-solo / summoner-DEFERRED.**
- **Why the proxy "sim extension" does not close this:** what landed (`gamora/v-proxy-add-sim-1`, 2026-06-17) is a CONTRIBUTION-CLASSIFIER (potential-integral for the 0.5 membership selector + Set #6 calibration), flag-gated OFF. In the spatial fight proxies **deal NO spatial damage and take NO position** (the COUNT≠CONTRIBUTION cut). The boss-killing measurement for summoners is UNBUILT — it is net-new spatial-combat architecture.
- **Track 2 of the combined run** brings this to the edge of decision (does NOT build/emit): T2.1 spatial-proxy-combat math note → T2.2 Gate-1 design review (pre-registered gandalf design-fit) → T2.3 throwaway de-risk spike (*does a summoner clear the boss when the army actually fights?*) → HARD-STOP with an architecture decision packet for Matt. Lifting `_DEFERRED_PROXY_BINS` + emitting the 25% are the two reserved Matt decisions (§5a content-gate).
- **Reporting gap flagged (small star-lord/rocket add):** the proxy deferral is tracked per-cell (`is_deferred=True`) but not rolled into the season summary; surface "N proxy cells reserved, M deferred" so the unfilled 25% is VISIBLE season-over-season, not silent.

### What did NOT move

- **Content-emission plumbing (the two-tracks-don't-meet join):** zero movement — still the rocket/star-lord engineering map (§7.1 (a)–(e)). The combined run does not advance it.
- **The §7.2 design pre-clears (faction/weapon shapes, keystone-ceiling, endorse-criteria):** stationary. The **caster-coverage spec (item 4)** is now sharpened by the proxy finding (the caster single-target residual int 0.681/wis 0.563 is measured on a proxy-EXCLUDED roster — so it cannot yet be judged honest-texture vs measurement-gap) but is not yet authored.

**Signed:** gandalf, 2026-06-21.

---

## SESSION-DELTA 2026-06-20 — (GOVERNED BY THE 2026-06-21 DELTA ABOVE; GOVERNS §0.5 + below)

The 2026-06-19/20 battle-sim session opened a sublayer the 06-18 memo did not see. **Where this block conflicts with §0–§8 (incl. §0.5 C2 and §7.4), this block governs.** It deliberately does NOT re-resolve the in-flight DoT/ailment fix run — those items are marked in-flight with their empirical criteria, to be closed on data in a second pass once Arm C + the band refit land.

### What the 06-18 memo got WRONG (now-false, corrected here)

- **(D1) Target-A's "honest apparatus" criterion (§1) was ASSUMED met — it was NOT.** The spatial-regime measurement instrument is biased: synthetic endgame mobs carry nonzero `armor` but EMPTY `elemental_resistances` (`t4_sim_cycling.py:1007-1015` `_synthetic_mob_dict_for_spatial` emits no resist key; `spatial_resolver_adapter.py:227-228` defaults empty). Physical eats armor mitigation (8.1% swarm → 92.7% boss by tier); elemental eats ZERO. **Every spatial-regime band-fit ever done was contaminated** — casters were OVER-credited (zero resist → inflated KPM → inflated bands). The real game does NOT carry this bias (`monster_generator.py:486-498` rolls resistances); it is a SYNTHETIC-instrument artifact. **Target-A's "honest" gate is RE-OPENED.**
- **(D2) §0.5 C2 + §7.4 "Stage-2c ALREADY DONE / do not re-rule" is REVERSED → REOPENED-FOR-REFIT.** The n=3078 distribution those bands matched was itself caster-over-credit-inflated. Bands require a refit pass. The production gate (`gauntlet_sim.py:1032`) inherits the mitigation-symmetry fix's default → UNTRUSTWORTHY-pending-refit. The 06-18 "confirm, do not re-rule" instruction is void.

### What this session SETTLED (new, record-worthy)

- **(D3) Boss/mini-boss mitigation too high in ABSOLUTE terms.** Under symmetric mitigation (Arm B), boss survive+kill = 0.000 for ALL FOUR attributes — not an STR problem. The boss/mini-boss (90%+ tiers) nerf folds into the ONE refit pass; hold elite (66%).
- **(D4) Two latent mechanism bugs, not balance.** DoT inert in the spatial sim (`ActiveEffect` appended, never ticked — no `tick_effects` advance) + physical bleed scaled on int/wis (`damage_resolver.py:987-988`). Both silently in the shipping regime. Fix run (F1 activate / F2 re-route tick-scaling to originating skill's attribute / F4 mitigation symmetry) in flight.
- **(D5) Ailment-emission ruling: `is_control != hard` cut.** Emit 5 safe now (burn/bleed/drain/consecrate=`none`, chill=`soft`); defer 3 hard-locks (root/knockback/shock=`hard`) to a DR-guarded fast-follow. Rocket implements chain_A-only (`f5ae509`).
- **(D6) The "caster problem" is TWO problems sharing a name.** This session's thread = the MEASUREMENT confound (caster over-credit, D1) — diagnosed. **§7.2 item (4) caster-coverage** (spatial/timeout swarm; ΔWR ~0.02 on a 3.3× HP move) is DISTINCT, untouched, STILL OPEN. Do not read D1's resolution as closing item (4).

### What did NOT move (06-18 plan vs what happened)

- **(D7) §7's next-session pickup was NOT executed.** The §7.2 pre-clears (items 2/4/5) are STATIONARY since 06-18; item (3) keystone still PARKED. The session went entirely into this battle-sim sublayer. **Target B (gen-pipeline) gandalf surface: zero movement this session.**
- **(D8) Net on-track read:** direction UNCHANGED, and this is NOT Discipline-#13 drift — the STATED target-A "honest apparatus" goal is exactly what pulled the session deeper (you cannot declare A done on a biased instrument). But target-A's finish line moved OUT (a latent defect surfaced, not a regression), and target-B made no progress — a deliberate depth-on-A vs breadth-toward-B trade, recorded so it is visible.

### IN-FLIGHT — marked, NOT pre-resolved (close on data, second pass)

- **DoT/ailment fix run (F1/F2/F4)** → gamora implement + jack-ryan Gate-2 → **Arm C bleed-lever disposition**: does activating bleed close STR's elite_pack below-floor + boss-0.000 gap? gandalf rules on return.
- **The ONE band-refit pass** — absorbs caster-over-credit correction + D3 boss/mini-boss nerf + D5 ailment band-shift TOGETHER. Not yet run.
- **DR guardrail + chain_A-vs-chain_C hard-control placement** — open design follow-on.
- **decisions-log entry** — the `is_control != hard` boundary + deferred-hard-locks fast-follow + placement question.

**Signed:** gandalf, 2026-06-20.

---

## 0. The shape in one line

**Each pipeline is blocked at exactly ONE gandalf chokepoint — battle-sim at the Stage-2c band ruling, gen-pipeline at the §7.1 manifest design-owned half — and both chokepoints are mine to clear.** Clear those two (a focused gandalf work-item each, authorable from on-disk substrate, neither needs Matt), add the already-given "flip all 3" + one push pre-authorization, and a single unattended run can take **both pipelines most of the way to completion.** The only items that genuinely cannot ride an unattended run are the push gate (ADR-006), two design calls (keystone-ceiling, caster-coverage) whose *investigations* can run while the *calls* park, and the procgen-tool adoption (Tier-3, off both critical paths).

---

## 0.5 — CORRECTION (2026-06-18, post-Matt-reframe + reconcile-against-disk; GOVERNS where it conflicts with §0–§6)

Three corrections landed after the first draft — two reconcile-against-disk catches, one Matt reframe of what "gen-pipeline completion" means. The original §1–§7 are preserved as the first-draft record; **where they conflict with this block, this block governs.**

> **C4 — NPC SCOPING ERROR STRUCK (Matt-confirmed 2026-06-18).** A FOURTH correction: every "NPC content spec — from zero / headline gandalf item / highest-leverage" claim in this memo (§0, §7.1 line 67, §7.2(1), §7.4 line 258/260, §8 line 310) is **WRONG and STRUCK.** There is no season-1 "npc" content type — "npc" = the companion/mercenary ally (season-2), or townsfolk (future Engine-2 hub). The season-1 bundle is **SIX types** (kits/monsters/factions/gear/weapons/flavortext). Full reasoning + replacement at the §7.2 correction banner and in `canonical/story/2026-06-18-current-to-end-state-battlesim-and-pipeline.md` (the disk-verified successor, which governs). Do not re-impose the phantom NPC requirement.

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

§0/§2/§4(row)/§5–§6 treated Stage-2c (KPM-band ruling) as "blocked-on-gandalf." **Falsified by disk:** Stage-2c was ruled + wired (Stage-2d, `92c040f`, MIGRATION v1.76) + Gate-2-closed (`2b8b502`, interim guard LIFTED) on **2026-06-16**. The bands are live in `gauntlet_sim.py` `ENCOUNTER_COHORT_KPM_BAND`, matching the n=3078 empirical distribution exactly. The "READY FOR GANDALF" in `AGENT_STATE.md:4269` is a **stale checkpoint** never back-edited after 2c/2d landed (flag for gamora). My independent re-derivation from the raw n=3078 data CONFIRMS the asymmetric-band logic. **Stage-2c needs confirmation, not re-ruling — it is closed.** *(⚠ REVERSED 2026-06-20: REOPENED-FOR-REFIT — the n=3078 bands were caster-over-credit-inflated; see top SESSION-DELTA D2.)*

### C3 — The two "lower-confidence" items (§2 diagram L64–65), traced + dispositioned

- **BC-coordinate cutover Stage-2 Unit-2+** — this was the REAL battle-sim gandalf chokepoint (Stage-2c being already-done). "BC" = Battle-Coordinate, the 8-axis bin tuple replacing the archetype LABEL as the pipeline's structural hub. Stage-1 (rocket/gen) complete; Stage-2 (gamora/sim) implementation landed per MIGRATION v1.70; the equivalence run (`output/stage-2-bc-keying-equivalence-2026-06-14.txt`, N=1120/arm/archetype) passed **16/16 archetypes at `0.00/0.00/0.000`** but escalated ONE WARN-1a envelope-width flag (`damage_long_collapse` water/earth/holy/shadow, W_ttk=24.42% > cap) to gandalf. **RULED THIS SESSION → ACCEPT** (the over-wide envelope is element-intrinsic flavor spread the cutover preserves exactly, not ordering-driven differentiation the collapse would flatten; A1 earth_caster case=2 re-confirmed). See `2026-06-18-bc-coordinate-cutover-stage2-envelope-escalation-ruling.md`. This **clears the genuine battle-sim gandalf gate**; jack-ryan Gate-2 on the implementation + Stage-3 prove-then-delete are the downstream gated steps.
- **open-shell floor residual** — a Stage-2c sub-question, **already RESOLVED**: gandalf ruled **option (a) empirical central mass** (open_arena band `[9.90, 15.53]`, unimodal p10/p90), accepting that realized spatial throughput sits ~0.63× the RESOLVE theoretical floor because RESOLVE's `A/√R` assumes pure-TMPM with no spatial overhead (travel/telegraph/approach). Wired in Stage-2d, ratified in decisions-log. **Closed.** (Another over-flag by the first draft — it read as open but disk shows it ruled.)

**Net correction to §0's headline:** the battle-sim gandalf chokepoint was NOT Stage-2c (already done) — it was the **BC-coordinate Stage-2 envelope gate, now ruled this session.** The "gen-pipeline" gandalf chokepoint (§7.1) is real but is the **VISUAL** path; Matt's **content-emission** pipeline is a separate, mostly-rocket/star-lord engineering map (C-PIPE) whose gandalf surface is design-spec'ing the missing emitters' content, not a single ruling.

---

## 1. What "completion" means (the two targets)

- **(A) Battle-sim complete** = the measurement apparatus is **honest** *(⚠ 2026-06-20: this criterion was ASSUMED met but is NOT — armor/resist instrument bias re-opened it; see top SESSION-DELTA D1)* (geometry-aware spatial resolution [#1], faithful-loadout kit power [#3], MOB_HP-anchored [✓ locked 1.5x]) AND the mobs/min bands are **ruled + wired** (Stage-2c→2d) AND the open balance questions are **dispositioned** (W-F adoption live; keystone-ceiling + caster-coverage either fixed or explicitly parked with a criterion). "Done" for a gauntlet run is empirically defined: 18 SC-6 endgame encounters, terminal pass-floor 9-of-18 in-band per cohort per kit (`gauntlet_sim.py:109,158`).
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

## 7. NEXT-SESSION PICKUP — consolidated forward queue (GOVERNS §1–§6 where it conflicts)

Cold-start-safe pickup. **This session closed four things** (see §7.4) and leaves the content-emission spine + five gandalf design pre-clears for the next session. Everything needed to resume without re-deriving is captured here.

### 7.1 The full content-emission path (Matt's "gen pipeline") — the forward picture

The target is **one driver that emits all seven content types into a single Godot-consumable sim-ready bundle.** Today there is none — **two emit tracks that do not meet** (full diagram: §0.5 C-PIPE):

- **TRACK NEW** (cycle-14 wave5): `run_season_production.py` → P2 kit-candidates → 2.5 variant-enum → 3 gauntlet+PM1 → 4 mechanical-archive (`kit_archive.db`) → 4.5 PM1-rerun → 5 cohesion-judge LLM (faction identity / season name / inter-faction rel / per-kit names) → 7 joint-gate → `cycle14_wave5_emitter.emit_season()` → **loadout app** JSON. **Kit-only — no monsters, no npcs; skill `flavor_text` NULL; `main_weapon` NULL.**
- **TRACK OLD** (`season_exporter.export_season()`): emits the genuinely sim-ready bundle `exports/<id>/{metadata,classes,monsters,gear_pool,gauntlet_recipe}.json` — **but kit/monster/gear-only (factions + npcs ABSENT, weapon=null), and its `generate-season` CLI driver was DELETED.**

**The 7-row honest state** (evidence in §0.5 C-PIPE table): kits WORKING · gear WORKING · monsters WORKING-old / MISSING-cycle-14 · factions PARTIAL (generated, schema at `schemas.py:1174`, never written) · weapons PARTIAL (identity in `substrate_weapon_binding`, never emitted as descriptor; `main_weapon=None`) · flavortext WORKING-class/monster/gear / GAP-cycle-14-skill-NULL · **npcs MISSING (no schema, no generator).**

**The five-part engineering map to a complete bundle** (mostly rocket + star-lord plumbing — NOT gandalf, except where flagged):
- (a) a **single driver** that routes cycle-14 content through (or replaces) `season_exporter` — *star-lord/rocket plumbing*
- (b) **monster generation wired into the cycle-14 track** (kit-only today) — *rocket/star-lord plumbing*
- (c) **`faction_clusters` actually written** to the bundle (schema present, writer absent) — *star-lord plumbing, gated on the §7.2(below) faction-shape design-spec*
- (d) **weapon descriptor wired** `substrate_weapon_binding` → `main_weapon` — *star-lord plumbing, gated on the weapon-shape design-spec*
- (e) **NPC emitter built from zero** — *rocket/star-lord build, gated on the NPC design-spec (the headline gandalf item)*

**The gandalf surface on this spine is design-spec'ing the missing emitters' CONTENT — items §7.2(1)(2) below. The plumbing (a)(b) is not mine.**

### 7.2 The gandalf design pre-clears (priority order)

> **CORRECTION 2026-06-18 (Matt-confirmed) — item (1) STRUCK. This block governs §7.2 and every NPC reference in this memo (incl. §0.5, lines 67/258/260/310 below).**
> Matt caught the scoping error: "Why do we need NPCs right now? Are they the mercenaries?" — they are. **There is NO season-1 "npc" content type.** "npc" in this project's vocabulary IS the companion/mercenary ally (`COMPANION_KIND_NPC="npc"`, `balance_loop.py:128`; `investment_profile.py:9` buckets "npc/mercenary" disjoint from player+monster), and it is ruled **season-2** (`MIN_COMPANION_SEASON=2`). The other reading — townsfolk vendors/quest-givers — is Engine-2/hub, future and non-combat. **Under every reading, NPCs are NOT season-1.** The season-1 bundle is **SIX content types**: kits (incl. summoner kits, which carry their summons) + monsters + factions + gear + weapons + flavortext. The phantom "world-population NPC" type below was my invention; do not re-impose it. The disk-verified replacement is `canonical/story/2026-06-18-current-to-end-state-battlesim-and-pipeline.md` (governs). The pre-clears that REMAIN are the (re-lettered) items (2)–(5) below: faction/weapon content-shapes, keystone-ceiling investigation, caster-coverage scenario spec, pre-registered endorse-criteria. **NEW season-2 item surfaced by Matt the same session:** the companion creates a season-boundary difficulty-inversion risk (season-2-with-ally easier than solo season-1); mitigation design (enemy-HP scaling for the companion + a spirit-guide solo-fallback combat contribution until first-form ascension) is a gandalf item once season-2 planning opens — captured in the companion-difficulty recognition note.

**~~(1) NPC content spec — from zero~~ — STRUCK (see correction banner above). Not a season-1 content type.**

**(2) Faction + weapon content-shape specs [HIGH; gandalf].**
- *Faction:* generated + schema-present (`schemas.py:1174`) but `_export_season_inner()` never writes it. Design question — does the Godot sim consume factions **mechanically** (faction-modifiers on encounter composition / monster / kit, alliance-hostility affecting encounter-gen via the cohesion-judge inter-faction relationships) or **narratively** (identity/flavor only)? Which `faction_clusters` fields are sim-load-bearing vs presentation-only. *Produces:* the faction JSON shape the sim reads + which cohesion-judge outputs route to the bundle (gates plumbing (c)).
- *Weapon:* `main_weapon=None` everywhere; identity lives in `substrate_weapon_binding` (phase2 intermediate), never emitted. Design question — is a weapon a separate content type or a gear-subtype? What does the sim need from a weapon descriptor distinct from its gear entry? *Produces:* the weapon descriptor shape + binding→descriptor mapping intent (gates plumbing (d)). Lighter design than NPC/faction — the substrate binding already exists; this is wiring-shape.

**(3) Keystone-ceiling "over-tuned" investigation [HIGH for autonomous-run value; my parked Tier-2b ticket].**
- *Scope:* open_arena AFTER `mean_wr=1.000`, `spearman_degenerate`, `max_rank_shift=23`. 1.000 WR with zero loss-variance is a **ceiling, not a measurement** — it degrades any balance run that leans on it. Distinct from the MOB_HP anchor (locked 1.5×) and from FLIP #3 (faithful default) — both correctly did NOT absorb this.
- *Design question:* is the keystone over-tuned? *Investigation:* a keystone-magnitude sweep at fixed MOB_HP 1.5× — does any magnitude produce sub-1.000 WR with measurable variance, restoring rank-discrimination? *Produces:* an empirical characterization (ceiling keystone-driven vs scenario-driven) feeding the design CALL.
- *Autonomous-eligibility:* INVESTIGATION autonomous-eligible (it's a sweep); the design CALL parks for Matt+gandalf (Tier-2/3).

**(4) Caster-coverage scenario-design spec [MEDIUM-HIGH; gandalf; off the additive critical path].**
- *Scope:* session-13 AGENT_STATE finding — a 3.3× HP reduction moved fire_mage swarm WR only ~0.02 (0.467→0.483). Casters fail on a **spatial/coverage/timeout limit INDEPENDENT of mob HP**, in the swarm/open-arena GROUP-clear scenario. The flip run does NOT touch this.
- *Design question:* scenario-design artifact (the swarm encounter over-punishes the caster spatial/coverage profile) vs genuine kit-power gap? The fix is a scenario-design call — adjust the swarm cohort's spatial/timeout parameters (telegraph windows, arena geometry, timeout calibration) to fairly measure caster coverage — NOT a MOB_HP or kit-stat change.
- *Substrate:* the session-13 finding + the spatial-proxy mechanic-port (the geometry-aware spatial resolution #1 brought online). *Produces:* the swarm/open-arena scenario-design spec; implementation becomes eligible once it lands.

**(5) Pre-registered endorse-criteria [META pre-clear — the lever that converts the queue to unattended].**
- *Scope:* for an autonomous run to close additive builds (Tier-1) without round-tripping to a live gandalf turn, the run needs gandalf-authored criteria it self-checks against (2026-06-17 three-tier envelope pattern).
- *Produces:* per-build acceptance criteria (what makes §7.2 shader / §7.3 fill / §7.5 adapter / Stage-2d wiring / spatial-proxy port "gandalf-endorsed" without a live turn) + the PARK triggers (Tier-2: band-drift past pre-registered threshold, any keystone-ceiling interaction, any schema contradiction; Tier-3: push, keystone-ceiling design call, procgen adoption, any locked-decision re-open). The criteria encode the design-intent fidelity each build must preserve — that's why it's gandalf. Author **after** the content specs exist (so there's something to write criteria against), but it's what makes the whole downstream autonomous-eligible.

### 7.3 Other follow-up items (routing + gates — NOT gandalf design-authoring)

- **BC-coordinate decisions-log entry** — ratifies this session's Stage-2 ACCEPT ruling; routes Matt-approve → KR-draft → jack-ryan-review. Awaits Matt-approve.
- **jack-ryan Gate-2 on the BC implementation** — separate downstream QA gate (MIGRATION v1.70 already landed; the §3.3 INFO-4 table + JSON companion are the Gate-2 evidence). My design gate ≠ jack-ryan's QA gate.
- **Stage-3 BC prove-then-delete** — gated-but-unblocked by this session's ruling; its own future gate (deletes `ARCHETYPE_ROLE_PRIORITY` / `_PLAYER_CONTROLLER_ARCHETYPES` / `ARCHETYPE_TEMPLATES` / `legacy_archetype_shim`). The tri-state must NOT collapse before it (FALLBACK + LOUD-DEFAULT survive per Disc #12/#39).
- **`AGENT_STATE.md:4269` stale "READY FOR GANDALF"** — never back-edited after Stage-2c/2d landed 2026-06-16; flag for gamora to clear (it is NOT a live ask).
- **elrond §7.1 substrate slice** — in-flight (`837dd7f`), additive; the remaining half of the gen-pipeline VISUAL §7.1 node (my design-half closed this session).
- **Push gates (ADR-006, Matt-ask):** collab ahead by 3 (`01a0d53` + two prior); engine ahead by 4 (the three flips + jack-ryan's declaration). Unattended-run value sits on disk until a push-pre-authorization or a Matt push.

### 7.4 Closed THIS session — do NOT re-open next session

- **BC-coordinate cutover Stage-2 envelope escalation → RULED ACCEPT** + A1 earth_caster case=2 re-confirmed (the genuine battle-sim gandalf gate; ruling note `2026-06-18-bc-coordinate-cutover-stage2-envelope-escalation-ruling.md`).
- **Gear-spec §7.1 manifest VISUAL design-half → AUTHORED** (element-flavor tint menu + aura colors + finish-leans + zone guidance + emission placement; `canonical/story/gear-spec-element-flavor-manifest-design-half-2026-06-18.md`). This closes gen-pipeline VISUAL chokepoint #2 (§1–§6 still show it open — superseded).
- **Stage-2c band ruling → ALREADY DONE** (2026-06-16; confirm, do NOT re-rule — §0–§6 treating it as blocked-on-gandalf are superseded by §0.5 C2). *(⚠ REVERSED 2026-06-20: REOPENED-FOR-REFIT — see top SESSION-DELTA D2.)*
- **open-shell floor residual → RESOLVED** option (a) empirical central mass (§0.5 C3).
- **3-flips KR run → COMPLETE** — all flipped + jack-ryan-declared (`f32e48a`); FLIP #3 band-drift byte-identical `|delta|=0.00` confirming the @max-profile coherence prediction; keystone-ceiling correctly parked (→ §7.2(3)); regression clean; only PUSH pending.

---

## 8. Sign-off

The two pipelines are not blocked on Matt and they are not blocked on engineering capacity. **The battle-sim gandalf gate cleared this session** (BC-coordinate ACCEPT; Stage-2c was already done). **The gen-pipeline VISUAL gandalf chokepoint cleared this session** (§7.1 design-half authored). What remains is the **content-emission spine** — Matt's actual "gen pipeline" — whose gandalf surface is the five design pre-clears in §7.2, headed by the **NPC content spec (from zero).** The plumbing that joins the two emit tracks is rocket/star-lord seam work, not a gandalf chokepoint. Next-session highest-leverage work: author the NPC spec, then the faction/weapon shapes, then pre-registered endorse-criteria — the sequence that converts the content-emission map from "blocked" into "an unattended run can build it."

**Signed:** gandalf, 2026-06-18.
