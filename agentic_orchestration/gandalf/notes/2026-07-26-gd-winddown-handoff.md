# WIND-DOWN / HAND-OFF — 2026-07-26 — GD play-test v1 cycle → the join-key decision

**Author:** gandalf (steady-state, Pattern-B session with Matt)
**Role:** `ELICITOR` — framing next session's ruling over `DRIFT-CRITIC` evidence (the efficacy verdict)
**Readers:** next-session gandalf + Matt. Secondary: knight-rider, gamora, elrond, galadriel.
**Purpose:** next session rules two decisions. This doc is the complete substrate for both.

> **D-A** — Is **Grim Dawn the right game** to serve as (1) the **primary engine/sim join key** — the
> external reference distribution the battle sim calibrates against — and (2) the reference for
> **monster/NPC combatant AI**?
>
> **D-B** — If yes: what **gaps are outstanding** to complete the push of GD gameplay into the battle
> sim and to **generate + test kits representing GD builds**?

**Evidence grade of everything cited:** MEASURED unless marked otherwise. Primary artifacts:
`gandalf/notes/2026-07-26-gd-playtest-v1-efficacy-verdict.md` (CONDITIONAL PASS) ·
`…-artifact-verification.md` §§1–9.13 · `galadriel/captures/2026-07-26-gd-playtest-v1*/` ·
protocol `…-gd-general-play-run-protocol.md`.

---

## 0. State at wind-down (one screen)

- **Run `GP-gd-2026-07-26-s1`:** 113 min, levels 1–12, Soldier→werewolf, no potions, no devotion
  procs, one character. Verdict: **CONDITIONAL PASS** (commit `83ad0a2b`).
- **Extraction:** full-run T-A ledger DONE (13,633 samples @0.5 s, two-method closure, zero gate
  rejections on kills/deaths). Screenshot arm 313/313. **Damage-intake NOT extracted** (0.85%
  coverage) — one bounded 19,305-frame pass converts the verdict to PASS.
- **Nothing is running.** All processes down; chain scaffolding preserved.
- **Storage:** Pi = archive of record (13 GB: 12 GB video + 1.1 GB screenshots). Mac local copy at
  `/Users/admin/gd-scratch/` is the working copy — keep until T-B closes. Screenshots recommended
  local-permanent. **Single-Pi-disk risk flagged to Matt** (unrepeatable artifact, one disk).
- **Reproducibility verified, not assumed:** all chain scripts committed at
  `galadriel/pipeline/gd-playtest-v1/`; the fitted panel model is byte-identical to committed
  `panel-ocr-model.json`. `/tmp/gal-p0/` (1.4 GB) is disposable.

---

## 1. What this cycle PROVED (the case FOR Grim Dawn)

1. **Zero-cost telemetry works, at closure-grade.** GD's native UI is a machine-readable ledger:
   kills, deaths, `play_time`, per-skill use counts, `life_healed`, rolling dps, HP-globe numerals —
   all OCR'd at 2 fps with **two-method closure** (13,633-sample series terminating exactly on
   independently human-read totals; no shared failure mode). No instrumentation was written into the
   game; none is possible; none was needed.
2. **The game tolerates experimental protocol.** No-potion and no-devotion controls held for 113
   minutes and are *verifiable from the footage* (potions 0/0 in all 313 stills; zero devotion procs).
   A game you can run controls on is a game you can calibrate against.
3. **Oracle-grade micro-measurement is achievable from video alone.** The incoming poison DoT
   resolved to **−10 HP / 1.000 s period (sd 0.072 s)** — 57 identical ticks proving a single
   continuously-refreshed source. In-combat healing 1.580 HP/s with potions and dps pinned at zero.
   Hazard ≈ 6.3× regen. GD's internals are regular enough to reverse-engineer to sim-grade precision.
4. **One cheap run bought a real fixture.** 113 min of play + one afternoon of rig-fitting + 16 min
   of extraction compute → a **647-kill / 77-engagement distribution (R2)** plus a usable second
   (R3: 190/16). The economics of GD-as-substrate are excellent.
5. **The clock is solvable.** Piecewise slope-1 model confirmed out-of-sample at 13,633 points;
   80.0 s divergence decomposed into 12 located breaks + honestly-declared 39 s residual; loading
   screens self-identify (>2 s unreadable runs) and independently find the fitted breaks.
6. **Mechanically genre-canonical.** GD is D2-lineage in exactly the dimensions RDR's combat model
   targets: flat+% damage layering, resist/ailment architecture, gear-gated DoT, pack-based
   encounters, transformation builds. Matt's werewolf run even yielded a form-identity design finding
   (verification note §10) — the substrate speaks RDR's language.
7. **The AI half already has a positive rung — from a different lineage.** TSF6-Track-A (2026-07-24,
   tracker delta): GD AI *parameters* were pushed into the sim once — **leash parameter-faithful at
   +0.15%** (return-to-spawn 120.17 vs K·`MaxPursuitDistance` 120.0), pre-registered K=1.60 melee
   unit-pin, K-nonlinearity finding queued for Track-B. GD's monster AI is **data-parameterized**,
   which gives the join BOTH ends: declared parameters *and* observable behavior. That is a rare
   property among candidates.

## 2. What this cycle DISPROVED or bounded (the case AGAINST, honestly)

1. **Per-kill attack cost is NOT recoverable from GD video.** The protocol's own structural insight
   (§1.1) partly failed: the named counter covers 4.9% of kills, and the live substitutes alias —
   39% of kill increments are multi-kill (up to 7 at once). Attacks-per-kill survives only on
   single-kill events, which are conditioned on being single-target. **GD video delivers
   ENGAGEMENT-grain, not kill-grain.** (Q47 is solved at engagement level for R2/R3; not per-kill.)
2. **Outgoing damage cannot be typed at the pixel layer.** FCT is colorless — direct vs DoT
   inseparable. The dummy-side outgoing-DoT measurement failed this cycle (self-inflicted debug-
   overlay confound); recoverable only via the v2 overlay-off dummy segment.
3. **Intake is bounded-expensive.** The only intake instrument is the HP globe (proven 98.2% coverage
   at 60 fps over the death window); run-wide it needs the 19,305-frame T-B pass per run.
4. **Regime non-stationarity taxes everything.** Build churn fragmented v1 into three regimes and
   destroyed R1 as a distribution (43 kills = anecdote). Fixture cost scales with build stability
   discipline; kills/engagement 3.3 → 8.4 → 11.9 proves pack size rides build power, so pooling is
   never legal.
5. **Monster-side video instrumentation is UNPROVEN.** This run instrumented the *player* ledger.
   S3 per-entity segmentation was defined and never exercised — zero extraction of aggro radii, pack
   cohesion, attack cadence, or kiting response from footage. (The parameter path — item 1.7 — is
   proven; the video-behavioral path is not.)
6. **Single-sitting constraint unresolved.** Whether `skill_use_count` survives save/reload is
   unknown; Matt's ~60 s test is pending. Until then a run is bounded by one sitting.
7. **Off-video channels are UNEXPLORED, not dead.** `character.LogData` yields no file (probed).
   Save-file parsing (`.gdc`) and game-database extraction (`.arz` records) were NOT probed this
   cycle — flagged UNEXPLORED. If either works, caveats 1–2 may dissolve without CV work.
8. **No comparative baseline exists.** No alternative (D2R, Last Epoch, PoE, Torchlight) has been
   tested with this rig. "Right game" currently means "the proven game vs unknown alternatives." The
   rig itself is GD-fitted (panel model, digit templates); porting it to another game re-pays the
   model-fitting afternoon.

## 3. What the evidence CANNOT say

- **Representativeness:** one character, one difficulty, levels 1–12, controls on. Controls trade
  representativeness for cleanliness *deliberately* — but a Normal-difficulty levelling arc is not
  endgame density.
- **The devotion stronger claim** (zero points assigned) stays UNVERIFIED; only "no proc fired" is
  proven.
- **Restore-on-load vs Constitution regen** — unresolved; 30 s v2 trial settles it; the DoT number
  stands either way.

---

## 4. The forks Matt rules next session (ELICITOR — my lean stated; Matt rules)

**F-1 — Join grain: engagement or kill?**
GD video gives engagement-grain (TTK, kills/engagement, pack size) and cannot give kill-grain.
*Option (a)*: ratify **engagement as the canonical join grain**. *Option (b)*: require kill-grain →
forces the off-video channel probe (§2.7) or a different game.
**Lean: (a).** The sim's own gauntlet fights are engagement-shaped; the genre balances on clear-speed
and pack economics (D3 GR timers, PoE pack-size investment), not per-monster swing counts; and §1 of
our own protocol asked for engagement shape before §1.1 romanticized the per-kill counter.

**F-2 — Monster-AI reference path.**
*(a)* parameters-primary: GD database records → sim params (TSF6-Track-A lineage; exact, cheap,
proven at +0.15%; tests *declared* behavior). *(b)* video-behavioral: S3 entity tracking (measures
what the player experiences; unproven, expensive). *(c)* both — parameters primary, video
spot-verification where parameters underdetermine behavior (e.g. target-selection, repositioning).
**Lean: (c)**, sequenced parameters-first. Track-A already carries the lineage; the sim's **missing
aggro-onset concept** is the named headline gap there and doesn't need video to close.

**F-3 — Commit depth: one game deep, or survey first?**
*(a)* GD as THE join key; invest in T-B + fixtures + kit mapping now. *(b)* port the rig to 1–2
alternatives for a shallow comparison first.
**Lean: (a).** The rig passed hard, the genre-fit is canonical, TSF6 lineage compounds, and Matt's
stated intent ("kits representing Grim Dawn builds") already names the game. A second reference game
is a later luxury; it costs a rig re-fit and buys mostly reassurance.

**F-4 — Sequencing of the T-B intake pass.**
**Lean: fire it BEFORE the D-A ruling if compute allows** — it runs on existing footage, converts
CONDITIONAL PASS → PASS, and delivers the intake distribution that the ruling would otherwise have
to assume. It sharpens the decision for free.

*(Parked by Matt this session, not for next session: the §10.1.c kit-power fork and §10.1.d
grimoire record-vs-currency tension — "forget the story fork. it's not important now.")*

---

## 5. If D-A = YES: the gap inventory (D-B), ordered

### Tier 1 — close v1 on existing footage (no new recording, no ruling dependency)

| # | Gap | Owner | Note |
|---|---|---|---|
| G-1 | **T-B intake pass** — 15 fps globe OCR over 106 engagement windows +3 s pad = 19,305 frames | galadriel | Converts verdict to PASS. Digit templates exist. ~5× the death-window work. |
| G-2 | **Damage-per-regime derivation** — integrate the captured `dps` column; mean damage-spent-per-kill per regime (overkill-inflated monster-EHP bound) | galadriel/gandalf | Cheap; from existing CSV. Kernel caveat: per-ENGAGEMENT damage only valid for engagements ≫ 6 s (rolling-mean width). |
| G-3 | **Fixture ingestion** — regime-partitioned, never pooled; DoT boundary `play_time` **6052** (not 6816); `life_healed` 3.1% rejection rate as a column; **every reader emits coverage** | elrond | Schema: fixture rows still need `fixture_character`/`fixture_set`/`fixture_trial` identity input. |

### Tier 2 — the join itself (design + sim work; F-1/F-2 rulings feed these)

| # | Gap | Owner | Note |
|---|---|---|---|
| G-4 | **GD-build → RDR-kit mapping spec** — first kit = the R2 werewolf: 2 actives (claws 358 / charge 175 uses) + auto + gear-DoT; cadence from the use-count series; form-commitment maps to the form library | gandalf `SPEC-AUTHOR` (+gamora) | The spec must state what the kit is ACCOUNTABLE to: R2's engagement-TTK + kills/engagement + (post-G-1) intake distributions. |
| G-5 | **Sim comparison harness** — run a kit against pack-size-distributed encounters; emit engagement-grain TTK + kills/engagement; compare to R2 fixture under pre-registered acceptance bands | gamora | This is the join key made operational. Bands pre-registered BEFORE the first comparison run (standing discipline). |
| G-6 | **Monster-side acquisition per F-2** — parameters path continues TSF6-Track-B (K-nonlinearity; aggro-onset concept missing from sim); video path (if ruled in) starts with S3 feasibility on existing footage | gamora (params) / galadriel (video) | Sim's missing aggro-onset is already the named headline gap from Track-A. |
| G-7 | **Off-video channel probe** — `.gdc` save parse + `.arz` database read (UNEXPLORED) | legolas (Mode A) | If the database yields monster stats + skill data directly, G-2's EHP bound becomes exact and F-1(b) becomes cheap. One bounded research commission. |

### Tier 3 — v2 recording (only after Tiers 1–2 shape it)

| # | Gap | Owner |
|---|---|---|
| G-8 | Protocol v2 amendments (ranked in verdict §8): overlay-OFF dummy segment · **~2× engagements via combat-weighted play** · stable-or-announced build · audio callouts for deaths/gear/zones · loading-screen = segment boundary · coverage rule mechanical · ≥25 Mbps | gandalf (protocol) / Matt (play) |
| G-9 | Matt's ~60 s save-identity test (menu-return, reload, re-read counters) — decides the single-sitting constraint | **Matt** |
| G-10 | 30 s non-DoT 50%-HP out-of-combat stand — settles restore-on-load vs regen | Matt (in v2) |

### Carried debts (not gating, not forgettable)

- Coverage retrofit on the panel readers (D-1 instances 1–2 were undetectable because readers
  couldn't report their own coverage; **five instances this cycle, one mine**).
- Protocol §1.1 rewrite around engagement-grain kills-per-swing; drop the `defaultweaponattack`
  premise; save identity into §2.1; quest-tracker/anger-overlay collapse into §2.0.
- Elrond labeling: "in-combat healing, all sources," never "regen"; devotion as two separate flags.
- Storage: delete the Mac 13 GB working copy after G-1; copy screenshots local-permanent; Matt to
  disposition the single-Pi-disk exposure.

---

## 6. Artifact map

| Artifact | Path |
|---|---|
| Efficacy verdict (CONDITIONAL PASS) | `gandalf/notes/2026-07-26-gd-playtest-v1-efficacy-verdict.md` |
| Verification note (§§1–10.1, incl. §9.13 extraction fold) | `gandalf/notes/2026-07-26-gd-playtest-v1-artifact-verification.md` |
| Run protocol under test | `gandalf/notes/2026-07-26-gd-general-play-run-protocol.md` |
| T-A ledger (13,633 gated) + shots arm (313) + panel model | `galadriel/captures/2026-07-26-gd-playtest-v1/` |
| Death-window / DoT / anomaly evidence | `…-gd-playtest-v1-r2/`, `…-r3/` |
| Chain scripts (all committed) | `galadriel/pipeline/gd-playtest-v1/` |
| Raw footage — archive of record | `/Volumes/reincarnated/visual-artifacts/GD-matt-test/play-test-v1/` |
| Raw footage — working copy (delete after G-1) | `/Users/admin/gd-scratch/play_test_2026-07-26.mp4` |
| TSF6-Track-A precedent (AI-parameter join) | tracker delta 2026-07-24 + `gandalf/notes/2026-07-24-tsf6-track-a-run-charter.md` |
| Key commits this cycle | `83ad0a2b` (verdict + §9.13), `23e3e25f` (r3 evidence), plus capture/pipeline commits |

## 7. First moves next session

1. Read this doc, then the efficacy verdict. (The verification note is reference depth, not
   re-read depth.)
2. **Rule F-1 → F-4** (§4). F-3 effectively decides D-A.
3. If GO: fire **G-1** (galadriel, backgroundable) and **G-4** (kit-mapping spec) in parallel;
   commission **G-7** (legolas probe) cheap and early — its result can upgrade the whole join.
4. Knight-rider sequences Tier-2 once G-1 returns.

**Signed:** gandalf, 2026-07-26, session wind-down.
