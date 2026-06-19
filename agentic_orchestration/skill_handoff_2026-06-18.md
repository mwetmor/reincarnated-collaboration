# Skill Handoff — 2026-06-18

**Author:** knight-rider
**Session:** three-flip ratification run (gandalf-authored, Matt-declared)
**Driving directive:** Matt 2026-06-17 "let's flip all 3" — operationalizing parking-lot items #1/#2/#3 from the 2026-06-17 autonomous run. The declaration was the gate; this session executed it.

---

## Headline: three OFF-by-default production flags flipped LIVE — run closes clean both sides

All three flips landed as separate, git-revertible commits in gamora's simulation seam, each smoke-clean, each with a jack-ryan decisions-log semantic-shift declaration, both gandalf Tier-2 calls resolved. **No BLOCK. No locked reference changed. Nothing pushed** — the push gate is held for Matt (Tier-3).

### Per-flip status

| # | Flip | gamora commit / tag | Smoke | jack-ryan declaration | gandalf |
|---|---|---|---|---|---|
| **1** | F1 geometry-fix RATIFIED LIVE (no flag — code-path widening already merged at `104bfbc`; "flip" = ratify the shipped spatial measurement basis) | `6f3d689` / `gamora/v-f1-geometry-ratify-live-1` | 18/18 PASS | decisions-log L4277 | ENDORSE (precondition for honest re-measure) |
| **2** | `track_proxy_population` default OFF→ON (Axis-2A proxy COUNT instrument goes live) | `62f0f2d` / `gamora/v-d4-proxy-default-on-1` | 6/6 PASS | decisions-log L4302 (+ promoted the "Decisions to revisit" stub `7f33d1c` to live) | no design objection — infrastructure |
| **3** | `apply_max_profile_investment` default OFF→ON (4-site chain; "kit power" now means FAITHFUL/geared, not the stripped ablation floor) | `424c83e` / `gamora/v-keystone-faithful-default-on-1` | 242/242 seam PASS | decisions-log L4329 | ENDORSE — composes with locked MOB_HP 1.5x anchor |

jack-ryan's three declarations are in one commit: **`f32e48a`** (engine decisions-log). Each cites the gandalf rationale; supersession edits applied (2026-06-16 Axis-2A entry → production-default Superseded; revisit-stub struck + promoted).

### Re-measure package (routed to gandalf, resolved)

- **#2 re-measure:** mobs/min **INERT** — byte-identical OFF vs ON (same seed; COUNT≠CONTRIBUTION). 34/34 archive kits declare zero proxies → uniform honest measured-zero `solo` floor. No band consequence.
- **#3 re-measure:** `output/kpm-band-spatial-recal-full-20260618_002503.json` (n=3078). Pooled mean 8.523. **8.19× keystone multiplier CONFIRMED** (mean-of-ratios on kpm throughput metric, not ceilinged).
- **Material drift vs n=3078 basis: NO** — byte-identical (|Δ|=0.00) across all 6 shells + pooled. Mechanism: the band-fit harness already applied max-profile investment (`_patch_kits_profile(profile="max")`), so the bands were *already* fit on faithful loadouts; #3 only aligns the runtime default to the regime the bands assumed.

### gandalf Tier-2 calls (both made; ruling `f4bb895` in collab)

1. **Band-refit: HOLD (no refit).** Same measurement regime → byte-identical Δ is the same-regime fingerprint, not coincidence. `gauntlet_sim.py` bands UNCHANGED. This is the clean-close branch gandalf's run-prompt pre-stated.
2. **Keystone-ceiling: stays a SEPARATE parked ticket** — #3 ratifies cleanly. The 8.19× reads *throughput*; the 1.000 zero-variance ceiling lives on *win-rate* (different metric — the ceiling cannot corrupt a multiplier it doesn't touch). Parking pointer: `gandalf/notes/2026-06-17-mob-hp-anchor-design-read.md` §4.1. **Empirical re-engagement criterion (not time):** when the open_arena reference de-saturates off the 1.000 WR ceiling (loss-variance > 0, `spearman_degenerate` false) — until then there is nothing to rank.

---

## ⚠️ PUSH GATE — held for Matt (Tier-3, ADR-006)

The §7 autonomous-run feature commits (`104bfbc`/`af5c8b2`/`c1e07a0`) and their 3 tags are ALREADY on remote (pushed since the 06-17 handoff). The unpushed delta is purely this run's new stack:

**ENGINE repo (`~/Games/reincarnated-engine/`):**
- `git push origin main` → 4 commits: `6f3d689` (#1) · `62f0f2d` (#2) · `424c83e` (#3) · `f32e48a` (decisions-log)
- 3 new tags (`git push origin <tag>`): `gamora/v-f1-geometry-ratify-live-1` · `gamora/v-d4-proxy-default-on-1` · `gamora/v-keystone-faithful-default-on-1`

**COLLAB repo (`~/Games/reincarnated-collaboration/`):**
- `git push origin main` → `f4bb895` (gandalf run-close ruling) + this handoff commit

**Awareness (NOT part of this gate):** several pre-existing local-only intermediate seam tags from earlier work are unpushed (`gamora/v-keystone-live-integration-1`, `v-d4-proxy-port-axis2a-1`, `v-keystone-node-wire-1`, `rocket/v-companion-gen-1`, `rocket/v-keystone-gear-materialization-1`, `star-lord/v-wd-export-1`). Intermediate seam tags don't normally need remote; flagging only so the picture is complete.

---

## Pending Matt-decisions queue

1. **PUSH GATE above** — the only decision gating this run's close. Two-repo push.
2. **Keystone-over-tuned standing ticket** (visibility, not action) — parked with the de-saturation empirical criterion above; nothing to act on until open_arena reference comes off the 1.000 ceiling.

## Carried-forward open items (from 06-17, not this run)

- **Cloud backup of full Synty corpus** — PENDING, Matt-gated (external write). Corpus safe on Mac disk. Only remaining open item in the acquisition workstream.
- **`canonical/story/styleprofile-output-shape-ruling-2026-06-17.md`** — was untracked at 06-17 close; verify gandalf committed it.
- **EULA confirmation** + per-zone semantic labels (galadriel render pass) — Matt/tooling open items.
- **rocket §7.2 restyle-leaf build** — gate now satisfied; eligible to dispatch next cycle.

## Next-session pickup

If Matt authorizes the push: execute the two-repo push above, then the three-flip run is fully closed. Otherwise the stack sits clean and revertible on disk.

---

# ADDENDUM — FOLDED season-1 completion run (sim + pipeline-spine, one sequence)

**Session 2 (same date):** knight-rider executed the gandalf-authored folded completion run (`gandalf/requests/2026-06-18-kr-folded-completion-run-prompt.md`). Fired autonomously per its sequence (diagnostics → additive/calibration → BC-Stage-3-destructive-LAST), joint-gated each Tier-1 close with jack-ryan Gate-2 + the gandalf endorse-criteria. **Push was PRE-AUTHORIZED (run-close push-pattern) — executed.**

## Per-item status (8 items)

| # | Item | Workstream | Status | Gate composition |
|---|---|---|---|---|
| 1 | Caster-Lever-C probe | A (diag) | **PARK Tier-2** | blocked pre-sim; no verdict forced (§2.1 trigger) |
| 2 | Keystone-ceiling sweep | cross (diag) | **CLOSED** (investigation); CALL **PARK Tier-3** | K-1, M_desat=g=0.55 |
| 3 | P2 faction writer | B | **Tier-1 CLOSED** | JR PASS-WITH-INFO + endorse §3.1 |
| 4 | P3 monster wiring | B | **Tier-1 CLOSED** | JR PASS-WITH-INFO + endorse §3.2 |
| 5 | P5 weapon emission | B | **Tier-1 CLOSED** | JR PASS-WITH-INFO + endorse §3.3 |
| 6 | P1 emitter scaffolding | B | per-type **CLOSED**; assembly **PARK Tier-3** | endorse §3.4 (no route-vs-replace baked) |
| 7 | B4 summon-construct calibration | A | **PARK Tier-2** (HONEST_FAIL §2.3(ii)) | no value committed; discipline held |
| 8 | BC Stage-3 prove-then-delete | A (destructive LAST) | **Tier-1 CLOSED as NO-OP** | JR PASS-WITH-INFO + endorse §2.2; tri-state survives |

## Commits + push

- **Engine** `eb69419..2e4033f` (8): `2c252d5` star-lord emitters · `64e26d8` B4 park note · `5b529d2` BC Stage-3 NO-OP + diag math notes · `2e4033f` diagnostic-record (harnesses+outputs) · PLUS the 4 carried three-flip ratification commits (`f32e48a`/`424c83e`/`62f0f2d`/`6f3d689`) annotated "carried in the run-close PUSH GATE" — this folded run was that gate.
- **Collab** `ce2e5c3..528f3ed` (20): `2c0592f` + `528f3ed` JR Gate-2 findings (this run) + 18 carried prior gandalf/galadriel/run-prompt work-products.

## Park-stack (for re-engagement)

**Tier-2 (gandalf):**
- **Caster probe** — blocked on the BC-cutover-deleted caster kit-build path; needs a rocket post-cutover caster→`PlayerClass` construction path. Harness complete (`scripts/caster_lever_c_probe_2026_06_18.py`), ~near-zero marginal work once the rocket path lands. The caster boss-bridge CALL stays blocked behind it.
- **B4 summon-construct calibration** — §7 proxy budget math (contribution-shaped) vs gauntlet KPM pass-floor (direct-damage-shaped) in structural tension; proxy damage invisible to KPM by the COUNT≠CONTRIBUTION cut. §5 re-engagement criterion: choose the instrument (seat summoners on the contribution instrument Set #6 used / refit the KPM band / wire proxy budget into KPM as a Tier-3 build). No value moved (correct — no fake green).
- **BC §2.2 doc-reconcile NOTE** — the prove-gate references the deleted `simulate_fight` 1D instrument (removed 2026-06-16); reconcile the criteria wording to the 2D-spatial-gauntlet-sole-sim reality. No behavioral risk (equivalence already proven 16/16-at-0.00 at Stage-2).

**Tier-3 (Matt):**
- **Keystone-ceiling CALL** — K-1: keystone WAS holding the ceiling; M_desat=g=0.55 (above the g=0.25 power-fantasy floor, so over-tuned is genuinely measurable, not a feel-vs-measure tension). How far to reduce magnitude, if at all. Evidence durable at `output/keystone-ceiling-magnitude-sweep-20260618.json`.
- **P1 route-through-vs-replace architecture** — does the single driver route cycle-14 content THROUGH `season_exporter` or REPLACE it? Per-type emitters built driver-agnostically and waiting; only the top-level stitch parks.
- **Boss-bridge family calls** — rogue (a) composer-efficacy-fix vs (b) accept-and-route-via-b6; caster analog blocked behind the parked probe. gandalf's lean (one doctrine, three instances) is framed, not decided.

**INFO routed (non-blocking):**
- 33 `test_cycle12_layer4_convergence.py` failures — rocket seam, pre-existing/out-of-seam (`SkillTreeGenerator.generate()` retired G10 2026-06-16). Standing rocket cleanup.
- 7 `test_cycle13_wave5_gauntlet_sim.py::TestGauntletKitResult` failures — gamora seam, boundary-independent cohort-accounting; separate ticket.

## Next-session pickup

drax cutover (loadout reads factions from the embedded bundle block, then retire the `*-faction-clusters.json` sidecar) is sequenced behind the P1 architecture call. Sidecar NOT deleted this run.
