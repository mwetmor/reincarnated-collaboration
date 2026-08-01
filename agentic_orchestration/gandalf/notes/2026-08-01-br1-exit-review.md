# BR-1 (BATON-RENDER) — EXIT REVIEW

> **STATUS: RUN COMPLETE 2026-08-01.** Both target-states delivered. Zero cells lost.
> **Conductor:** gandalf (`RUN-CONDUCTOR`). **Charter:** `2026-07-31-baton-render-run-charter.md`.
> **Ledger of record:** `2026-07-30-ambient-refit-fold-in.md` (Scopes 1–39, rulings R-BR-1…R-BR-23,
> every cell landing) — this doc is the single review surface, not a restatement of the ledger.
> **Matt's return page** (watch order + veto surfaces): `2026-08-01-br1-matt-return-review.md`.
> **M-EYE holds:** every acceptance surface named below is MOTION. No still is offered as evidence
> of look.

**Matt's charter sentence, verbatim:** *"take the phase2c baton and complete the run ending at the
fully godot rendered battle sim (including lighting, shadows, VFX, characters (player and enemy)?
Full combat sim render in a beautiful corner"*

---

## §1 — Target-state scorecard (charter §2)

| Target | State |
|---|---|
| **T-1** — one integrated watch: a full phase-1 fight, start→death, in the crypt corner at the GD camera, carrying cone-beams + cold pools, unified shadow grammar, warm-carried-light werewolf, cast boss, real-nova telegraph decals, crit-RED numerals, element-mapped VFX, death resolution | **✓ DELIVERED 2026-07-31** — `tmp/lap1watch/clips/LAP1_WATCH_full_fight_CAMLOCK.mp4` (27.80 s) + highlights. **G-4 PASS: 11 PRESENT / 1 PARTIAL**, every row frame-stamped. Boss-ID triple-verified (max-HP ∧ id-prefix ∧ roster-tier): **PRIMORDIAN, THE FORGOTTEN ONE**, 14,812 HP — the same boss whose Grim Dawn fight is the run-family's acceptance fixture (R-KC1-22). `is_boss` reads FALSE on the correct actor, exactly as R-BR-1 predicted |
| **T-2** — the scene re-rendered on rider-bearing traces, the three Lap-2 channels visibly consumed, diff named | **✓ DELIVERED 2026-08-01** — `tmp/restage/clips/LAP2C_WATCH.mp4`, 1600×900, 1,264 frames, **42.13 s**, h264+AAC, decode-verified, plus the JUICE camera arm. **G-6: 20 rows, 0 silently missing.** G-VFX PASS. **70/70 audio beats on their own frames. 3,441 position writes, 0 displacement violations.** Hit-stop drift **1.11 %** against a ~3.7 % budget |

**Rider census (T-2's own predicate, censused before being claimed):** `icearmor` **YES** (120/361
boss ticks → ward annulus at 2.05× body radius — readable on the boss for the first time) ·
`family` **YES 9/9** · `attack_id` **PARTIAL** (9/9 telegraph, 4/57 damage) — **consumed** for the
boss-ultimate hit-stop class and **refused** for T-2's "`attack_id`-keyed attack anims," because
keying three slices off a rider that is null on 53 of 57 events *"would be a mapping wearing a
rider's clothes."* An absent referent, named rather than dressed. That refusal is the single
cleanest instance in the run of the substrate voting against its own charter clause and winning.

## §2 — The cells (17 write + 2 measurement; single-writer godot chain, zero collisions after F-BR-1)

`BEAM-FIX` → `BEAM-CONE` → `RIVAL-CAST` → `SHADOW-UNIFY` → `TELL-DRESS` → `ROOM-DRESS` →
**`LAP-1 WATCH` (T-1)** → `MOB-CAST` → `BEAM-PIN2` → `VFX-BAKEOFF` → `BEAM-V3` → `ARSENAL-HARVEST` →
`WARMTH` → `HUD-BUILD` → `BEAM-SLITS` → `BODY-PROBE` → **`LAP-2C RESTAGE` (T-2)**
— godot `65cafec` … `69264c5`, every cell opened at the previous head clean, every landing banked
and pushed to the meta-repo as it occurred. Read-only measurement in parallel: **`GD-PARITY`**
(galadriel — overturned the conductor's camera-only ruling) and **`VFX-SCOUT`** (legolas — the
Unity→Godot translation path that made D-VFX-1 usable).

The charter's §3 sequence was eight cells. It ran to seventeen because Matt's post-T-1 review opened
Scopes 24–39 — **eleven Matt scopes, each folded into the ledger as a bound scope before any cell
consumed it.** No cell moved its own goalposts; the goalposts moved by ruling, in writing, upstream
of the work. That distinction is the whole of standing safety §5.1.

## §3 — Findings that outrank their cells

1. **★ The werewolf had never been given a strike to play.** Zero attack-named clips exist in
   **24,576 FBX**. Every attack in every render anyone has ever watched played
   `A_MOD_GBL_Idle_Fidget_Swipe_Neut` — **an idle fidget from a goblin locomotion pack.** Not a weak
   attack animation: *not an attack animation.* The tree's one authored melee take
   (`Animations_Melee.fbx`, hand-reach span 1.3671 m) was not missing — it was **unreachable at 0/21
   shared bone names**, so no search anyone ran could ever have surfaced it. Bridged through
   `SkeletonProfileHumanoid` + a hand-authored `sf_melee_bone_map.tres` (13 slots left **empty**,
   not guessed), it binds **16/18** on every candidate body against the incumbent's 21/95, and
   crosses **24.5 % deeper** into the target hull. This finding retro-invalidates the strike read of
   every clip cut before BODY-PROBE.
2. **★ Four of Matt's observations were RIGHT with the cause WRONG** — cold dust (not beam particles:
   shader-discarded outside the shaft since SKY-2; the AMB-HUE ramps did it) · sheen mechanism (the
   sconces rake the film; the carried lamp's own contribution *falls*) · beam glow (~80 % was fog,
   already removed by `--fogunlit` fired for another reason) · the werewolf strike (finding 1). The
   pattern is worth more than any of the four: **the owner's eye located four real defects and the
   team's explanation was wrong every time.** Eye as instrument, explanation as hypothesis.
3. **★ Knight ↔ werewolf are a 49/49 identical animation family** — so the body choice costs a flag,
   not a cell. R-BR-21's reversal of Matt's stated lean is therefore *cheap to veto*, which is the
   only reason a conductor should ever reverse a stated lean in the owner's absence.
4. **A stale constant is more dangerous than an agent's assumption.** My nova wind-up of **2.32 s**
   was wrong; measured, 9/9 telegraphs sit at 0.8333–0.8519 s (nova **0.8500**). I had carried it
   into the SFX beat table, G-6 row 6, **and the charter itself**. Truncating the charge sample to
   2.32 s would have made audio outrun every tell by **1.47 s** — the exact lie R-BR-16's truncation
   clause was written to prevent, arriving through a number that came *with a provenance.*
5. **A gate can measure the right criterion for the wrong reason and still be a good gate.** The
   Binbun shell does not work by additive bloom as R-BR-17 claimed; it is an alpha-blended grey puff
   that **occludes** core light (~6 % of core lit pixels pushed below threshold; law/core lit-px
   ratio median 0.944). G-VFX passed on component count, which was the right thing to protect. The
   ruling's *mechanism* is amended by measurement; the ruling stands.
6. **R-BR-22's disrepair clause dissolved under G-7: 0.0000 m interpenetration** along the boss's
   alive path. The "2.40 m beam base" I ruled against was **stale by two cells** (BEAM-PIN2 retired
   it to −0.60 m; the room has no ceiling mesh at all). I resolved a collision with a number, not
   with geometry. **The consequence outlives the ruling** — see §10.4.
7. **~30.9 % of damage taken emits no event** (F-HB-7). A third of the punishment the player absorbs
   is invisible to any consumer of the trace. Presentation cannot fix this; it can only fail to show
   it. Routed to the engine seam — the largest thing this presentation run found that presentation
   does not own.
8. **Instrument corpus grew by eight standing guards**, every one caught pre-verdict, none smoothed:
   F-AH-3 (`--import` strips `project.godot [rendering]`) · F-AH-6 (ffmpeg emits corrupt H.264 while
   exiting 0 → decode-verify every clip) · F-BS-2 (the exit-top gate had only ever run on one
   topology — it was never testing what we thought) · F-RS-2 (Binbun asset case-mismatch survives
   only on macOS's case-insensitive filesystem) · F-BR-1 (single-writer collision → worktree-per-cell)
   · F-BV-1 · F-AH-1 · F-AH-2.

## §4 — Owner-eye ledger (desirable-run-pattern §6.2, fired six times)

The pattern says: *when the run's output is a watched surface, the owner's eye is not a briefing
recipient; it is an instrument of record.* BR-1 scheduled it that way and it paid six times —
**twice as a PASS that unblocked a chain** (BEAM-REAL smoke frame: *"exactly what I want"*; BEAM-V3:
*"Beams and shadows are great now"*), **once as a verdict that reshaped a spec** (VFX interim →
the three-source COMBINE law), **once as praise that survived its own refutation** (*"the water
splotches look AMAZING"* — the effect real, the mechanism wrong), **once as a scope** (the
ARSENAL_BEATS gap list → R-BR-17/18 owners), and **once as the run's largest catch** (the werewolf
attack).

⚑ **That last one is a gate defect, not a lucky catch.** G-4 passed 11/1 on a watch in which every
strike was a goblin idle fidget, because the gate asked *did an animation play on the attack frame?*
— not *is the clip an attack?* **A presence gate cannot catch a wrong referent.** See §9.1.

## §5 — Rulings ledger (R-BR-1…R-BR-23; all veto-open unless Matt-signed)

**Discharged clean:** R-BR-1 boss-ID heuristic (triple-verified at T-1) · R-BR-2 animation mapping
(superseded in substance by BODY-PROBE's real melee take) · R-BR-3 no-invented-travel (held through
R-BR-18 and through the `attack_id` refusal) · R-BR-4 fight selection (seed 74000806, logged) ·
R-BR-5 casting (ElementalGolem lean; drax's rig-quality say honored) · R-BR-6 substrate re-pin ·
R-BR-7 Arm-A default flip (a standing Matt ruling implemented, not a new lighting decision) ·
**R-BR-8 shadow depth 3.50 — MATT-SIGNED** · R-BR-9 sticky target.

**Made in Matt's absence, alternate preserved on every one:** R-BR-10 warmth via `--fogunlit` + dust
ramp · R-BR-11 graded lamp bump for the sheen rake · R-BR-12 dust/beam coupling at a pre-registered
~80 % threshold · R-BR-13 numerals grade **C** (C′ one flag away) · R-BR-14 charge-glow authorship
split *(carries a correction of my own claim: `commit_skill_idx` is −1 on 361/361 ticks — the trace
has no player cast window)* · **R-BR-15 beams A3 / dust FULL — the threshold measured 76.7 % and did
not trigger; the run did not move its goalpost after seeing the result** · R-BR-16 licence-cleared
SFX only *(+ standing amendment: **restricted audio is restricted in every container**)* · R-BR-17
three-layer VFX law *(mechanism amended, §3.5)* · R-BR-18 muzzle-flash + impact, nothing between ·
R-BR-19 hit-stop budgeted, **trace clock inviolate, knockback forbidden** · R-BR-20 camera impulse
as a second arm so CAM-LOCK stays clean · **R-BR-21 werewolf ships, knight one flag away** (reverses
Matt's stated lean on the condition he attached; pre-committed FAIL registered — §10.1) · R-BR-22
parity ×1.29 *(disrepair clause dissolved, §3.6)* · **R-BR-23 HOLD on the boss/player ratio "fix."**

⚑ **R-BR-23 deserves its own line, because the HOLD was right for a wrong reason.** I called 1.5278
and 1.46 "two measurements of the same number." They are different quantities — a ratio of two
*constants* versus a *rendered* ratio (this render measures the rendered mean at **1.4571**) — and
GD-PARITY's own note had already published both in one row. **But had the hold not held, the cell
would have edited `RIG_BOSS_H` to "fix" 1.5278 and pushed the ratio an eye actually sees *away* from
GD-correct.** A hold that is right for an imprecise reason still beats an edit that is wrong for a
confident one. No `RIG_BOSS_H` edit was made.

## §6 — Gates, and how each resolved

| Gate | Resolution |
|---|---|
| **G-1** beam base-radius == pool-radius | PASS in BEAM-CONE; later re-pinned by BEAM-PIN2 (base −0.60 m) |
| **G-2** boss rig imports/retargets/animates without inversion | PASS on the Fantasy Rivals lean; the L6 `remove_tracks/unmapped_bones` law never needed to fire as a rescue |
| **G-3** ρ within ~10 % bright-vs-dim, one directional author, pools survive | PASS in SHADOW-UNIFY on **both** cast bodies |
| **G-4** T-1 completeness | **PASS 11 PRESENT / 1 PARTIAL** — the PARTIAL (werewolf in-motion readability 1.288× vs 1.540× static) declared, not hidden. **See §4: this gate passed a fight with no attack animation in it** |
| **G-5** Lap-2 open-gate | **FIRED ITS FALLBACK, THEN OPENED.** At T-1 the newest on-disk batteries carried `attack_id` and **zero** files with `family`/`icearmor` → Lap 1 declared the deliverable, Lap 2 **parked armed**. Matt then handed the 2c baton, the traces existed, the census re-ran, and G-5 opened on its own stated terms |
| **G-6** T-2 completeness (20 rows, pre-registered before the cell ran) | **PASS — 20 rows, 0 silently missing.** The gate's own law: *"absence is a PASS if it is named; a row silently missing is a FAIL"* |
| **G-VFX** component count must not collapse | **PASS** — 17 beats, 0 collapse, components median 32 vs 32 |
| **G-7** interpenetration along the boss path | **0.0000 m** — and the cell's run-1 report of 0.1849 m was self-caught as 81/84 offending frames being the floor slab |

**Every gate FAIL in this run was processed as a finding. None was terminal.**

## §7 — Honorable-fallback audit

One fallback was **declared, armed, and then dissolved by substrate arriving** — G-5. That is the
best possible outcome for a fallback clause: it was written pre-launch, it fired without drama when
the rider traces did not exist, it converted "the run is blocked" into "Lap 1 IS the deliverable and
Lap 2 parks armed," and when Matt handed over the 2c baton the gate re-checked on **its own
pre-registered terms** rather than on the conductor's appetite to continue. R-BR-5's fallback chain
(FortGolem → SpiritDemon → DarkLord) was never needed. R-BR-21 carries a **pre-committed FAIL
condition** into Matt's review rather than out of it, which is the same discipline pointed forward.

## §8 — Rubric-law self-check (desirable-run-pattern §6.3 — diff the predicates against the intent)

Matt's intent sentence asks for a **fully rendered battle sim in a beautiful corner.** The predicate
set (G-4, G-6, G-VFX, G-7, drift, displacement, audio-frame alignment) measures **presence,
integrity, and honesty**. Naming what fell out, out loud:

- **"Beautiful" is not in any predicate, and could not be.** The run can certify that every element
  is present, that no clock lies, that no body slides, that no layer collapsed — and it **cannot**
  certify the corner is beautiful. That is why M-EYE was standing from the first cell and why the
  watch, not the checklist, is the acceptance surface. This is a declared proxy, not a leak.
- **"Player and enemy characters" leaked once and was caught by the owner, not by us** (§4). The
  predicate read *animated*; the intent read *fighting*. That gap is the run's one genuine instance
  of intent leak, it was caught mid-run, and it is now the §9.1 amendment proposal.
- **Coverage before accuracy (§6.1) was obeyed:** G-4 and G-6 are coverage gates over the watched
  surface, run *before* any fidelity claim. No sliver was certified as a whole.
- **Red-main tripwire (§6.4): not applicable** — BR-1 pushed to no CI- or deploy-gated surface. The
  godot tree is local-plus-meta-bank by charter. The one shipping constraint the run *did* discover
  it owned is the licence containment in §10.5.

## §9 — Pattern-observations proposed for `desirable-run-pattern.md` §6

*(Proposals, not writes — `CANON-STEWARD` proposes, jack-ryan ratifies per `canonical-doc-format.md`
§ 6.7.)*

1. **Presence gates cannot catch wrong referents.** A completeness row must name the **referent it
   expects**, not merely non-emptiness. G-4 asked *"did an animation play?"* and passed a fight in
   which every strike was a goblin idle fidget. The generalized form: for each coverage row, write
   the row as *"X is present AND X is the kind of thing X is supposed to be,"* and state how the
   second clause is checked. Where it cannot be checked mechanically, **that row is an owner-eye
   checkpoint by construction** — which is exactly what it turned out to be here.
2. **The conductor's inherited constants carry an agent's assumption risk, at higher rank.** The
   2.32 s wind-up entered the charter *with a provenance* and propagated into a spec, a gate row and
   an asset instruction. Proposal: any numeric constant a charter asserts about the substrate must
   be **re-measured against the frozen substrate at launch**, not inherited from a prior battery.
   Cheap, and it would have caught this before it reached three artifacts.
3. **Restricted inputs are restricted in every container.** A WAV mixed from restricted samples, and
   an MP4 carrying that WAV in its AAC track, are the same licence object as the source directory.
   Banked as a standing amendment to R-BR-16; generalizes to any run that muxes vendored material.

## §10 — Decisions routed to Matt at exit

| # | Decision | Shape |
|---|---|---|
| 1 | **The body (R-BR-21).** I reversed your stated lean, on the condition you attached to it — the sword-vs-claw fork **has no referent in the asset** (21-bone rig, no fingers, pack ships `SF_Wep_Claws_01` against it), so your *"if not, select another character"* never fires. Counter-evidence not buried: the knight out-reaches it ×1.51 vs ×1.19 and you named a preference out loud. **Pre-committed FAIL: if the strike still reads weaker than the jump on the watch, the knight ships without further argument** | one word; the swap is a re-render, not a cell |
| 2 | **Parity grade** — ×1.29 shipped, ×1.00 and ×1.15 rendered beside it | eye |
| 3 | **Beam glow, re-judged against the current frame** — ~80 % of what you objected to was fog and is already gone. This is the one item where your eye may reasonably land elsewhere than it did when you wrote the note | eye |
| 4 | ⚑ **The slits have no cause in frame.** You asked for *"slits of light shining through cracks in the crypt's ceiling."* **There is no ceiling mesh.** The light is correct and its origin is unexplained. The disrepair edit I ruled would have supplied that cause as a side effect and is **not** being made (§3.6). A crypt whose light has no visible origin reads **stylised** rather than ruined — that is a register choice nobody has made on purpose yet, and it is yours | a register ruling, not a defect |
| 5 | **The two watch clips are LOCAL-ONLY** — restricted audio in another container. Silent evidence clips commit normally; `bash tmp/restage/run_all.sh` rebuilds both from committed instruments in one command | acknowledge, or rule the audio out |
| 6 | **Music on/off** · **camera-impulse arm** (both rendered) · **F-BR-5 principle** (`polygon-simple-fantasy` is SIMPLE-line; what was consumed is **rotation curves only** — no SIMPLE mesh, material, texture or rig instantiated. The naming-convention gate defect routes to jack-ryan regardless of how you rule) | taste ×2 + one principle |
| 7 | **Push authorization** for the godot tree (17 cells of local commits) | one word |

## §11 — Debts leaving the run (named, owned, not smoothed)

- **Engine seam (knight-rider sequences):** F-HB-7 (~30.9 % of damage taken emits no event) ·
  F-HB-8 + the `ReplicaFrameSink.telegraph()` family-drop — **one join-key repair closes both** ·
  F-RS-3 (F-HB-4 is too strong: a real telegraph→damage join key exists on 4/57; the HUD heuristic
  mis-read nova #5 because `telegraph.damage_amount` is **pre**-mitigation and `delivered` is
  **post**) · F-RS-1 (**G-5's rider-census amendment can be un-amended** — `family` is populated 9/9
  and the seam is fixed).
- **jack-ryan:** the §9 pattern-observations for ratification; the F-BR-5 naming-convention gate
  defect; F-BS-2's single-topology gate.
- **Presentation debt, declared:** foot-slide/moonwalk mitigations landed but the strafe family is
  still partial · F-AH-2's trail class is now **exercised on a swinging bone (50 attachments) and
  still not measured there** — downgraded, not paid.
- **Housekeeping:** `reincarnated-godot/AGENT_STATE.md` is eleven cells behind · `tmp/vfxbakeoff/`
  ~8 GB and `tmp/restage/` 567 MB await Matt's prune hand (`rm -rf` on directories remains
  sandbox-denied to every agent; file-level prune only) · SFX provenance drift (`_licenses` covers
  7 of 20 dirs; two notes read *NOT YET ACQUIRED* for packs that are staged, one under a different
  name).

---

**The one-sentence verdict on the run itself:** BR-1 delivered both target-states with every gate
resolved and every fallback honored, and its most valuable output was not the watch — it was the
discovery that for the entire history of this project the player character had never once been given
a strike to play, found only because the owner's eye was scheduled as an instrument and the run was
willing to print the finding at full volume against its own prior gates.

**Signed:** gandalf (`RUN-CONDUCTOR`), 2026-08-01.
