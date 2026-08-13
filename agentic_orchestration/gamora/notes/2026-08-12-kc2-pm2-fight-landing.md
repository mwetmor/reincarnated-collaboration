# KC2-PM2 — landing note: it is a fight now, and the player dies in wave 156

> **Cell:** KC2-PM2 · **Conductor:** gandalf (`RUN-CONDUCTOR`) · **Author:** gamora (simulation seam)
> **Date:** 2026-08-12 · **Charter:** `agentic_orchestration/gandalf/notes/2026-08-12-kc2-pm2-run-charter.md`
> **Math note (Discipline #1, written BEFORE the code):**
> `reincarnated-engine/src/reincarnated/simulation/math/kc2-pm2-incoming-damage-2026-08-12.md`
> **Status:** COMPLETE — four sibling batons, determinism ×2 masked-EXACT each, gate wall 66/66 each,
> assert wall 9/9. **No HALT was hit.**

---

## 0 — The one-paragraph answer

Monsters attack now, and so do their pets. The player has a measured defensive sheet, measured
sustain, and **dies in all four cells at wave 156, between 412.65 s and 415.35 s.** Matt survived
the real run; the frozen baseline clears twenty waves in 304.65 s with the player never touched.
So the sim player now outlives the *baseline's whole runtime* by 1.35× and still only reaches
**6 of 20 waves.** The four cells are separated by **2.70 s — 0.65 %** — which falsifies my
pre-registered ordering and is the lap's most useful negative. And the death mechanism is not the
one I predicted: the player floats at **97.7 % mean HP** all run, spends **0.4 % of ticks below
half**, and dies inside eight seconds of a **kill drought** — **182 of the final 200 ticks carried
no player damage output at all**, so 21 % ADCtH had nothing to leech from. **This build is not
tanky. It is one dry spell from death, permanently.** That is § 5.

---

## 1 — What landed

| # | artifact | where | digest |
|---|---|---|---|
| 1 | **math note** (+ § K amendments, appended after the run) | `simulation/math/kc2-pm2-incoming-damage-2026-08-12.md` | commit `e85c07ea` |
| 2 | **threat engine** | `simulation/kc2/threat.py` | `e85c07ea` |
| 3 | **avoidance AI** | `simulation/kc2/dodge.py` | `e85c07ea` |
| 4 | **tick-loop wiring** | `simulation/kc2/run.py` | `e85c07ea` |
| 5 | **pinned substrate** (8 files, digest-verified) | `data/kc2/pm2_*` | `e85c07ea` |
| 6 | **driver + assert wall + calibration** | `simulation/scripts/gamora_kc2_pm2_fight_2026_08_12.py` | `e85c07ea` |
| 7 | **export: 4 specs + 9 wire declarations** | `export/kc2_run_adapter.py` | `271679cc` / `c2b4d716` |
| 8 | **validator refinements + MIGRATION ×2** | `export/baton_v1_{validator,stub_consumer}.py`, both `MIGRATION.md` | `c2b4d716` |
| 9 | **4 knots supplies** | `simulation/output/kc2-pm2-actor-paths-*-20260813_012249.json` | `22e9d199` |
| 10 | **findings artifact** | `simulation/output/kc2-pm2-findings-20260813_012249.json` | `e16d97bb…` |

### ★ THE FOUR SIBLING BATONS

All emitted at **FULL** grade from a **clean** tree at engine `c2b4d71`, each through the **same
66/66** gate wall.

| cell | file (`src/reincarnated/output/`) | sha256 |
|---|---|---|
| **CAMP** | `kc2-baton-v1-E-s09-cp150-pm2-camp-20260813_013102.json` | `d24f13fb21ac60b7d0572f86a49d77d52f646cc9b5f8e077108928165d0a8a0b` |
| **DRIVE** | `kc2-baton-v1-E-s09-cp150-pm2-drive-20260813_013105.json` | `d6b6f211c2dbb836715d7a20c3ffe1f3fa11fae8eba57a1b63c771f58ec8f998` |
| **DRIVE+DODGE** | `kc2-baton-v1-E-s09-cp150-pm2-drive-dodge-20260813_013107.json` | `d4a20f708384b13c06c336a4aaa19ab7a5ac94e25dbe79183c1365da1ccac230` |
| **CAMP+DODGE** | `kc2-baton-v1-E-s09-cp150-pm2-camp-dodge-20260813_013110.json` | `ca5c094d2c60109d5cfe5d6b794313026699ea2a90eba54ca7a636c1f4bd12c1` |

**Both frozen batons** (`d7ecd866…`, `4585eeb8…`) were **verified from bytes** at the top of the
driver and of every emission, read read-only, and **never written**. Both still emit byte-identically
and both **re-validate at 66/66 after the two validator refinements** — which is the *evidence* that
those refinements are strict, not the claim.

---

## 2 — Determinism ×2 (charter law), per cell

Two FULL-grade emissions per cell into `/tmp` (so neither perturbs the tree — PM-1's
`tree_state_untracked_entries_excluded` hazard), then the record. Mask = **the emitter's own
`PROVENANCE_VOLATILE_KEYS`**, imported, not restated: `['_emitted_at', 'baton_run_id']`.

| cell | masked A / B / record | verdict |
|---|---|---|
| CAMP | `3ab72d1d075eec647989645b84b3c194…` ×3 | **EXACT** |
| DRIVE | `4d2f3383ae2ac9b4ec8346fbb0fcd4df…` ×3 | **EXACT** |
| DRIVE+DODGE | `d42a167d5219d021e99c28dd281e1005…` ×3 | **EXACT** |
| CAMP+DODGE | `3dc75b2cdef1bdd0beb05c1bec7752a3…` ×3 | **EXACT** |

**Sim-layer** determinism (each cell replayed twice, full emitted surface deep-compared): **EXACT**,
0 differences, 144,438 / 150,823 / 154,887 / 144,173 leaves.

---

## 3 — THE SURVIVAL HEADLINE vs REFERENCE TRUTH

> **Reference truth: Matt SURVIVED the real run.** The frozen baseline runs **3,732 ticks /
> 304.65 s / 20 waves / 344 kills with the player never hit.**

| cell | ticks | time of death | wave | waves cleared | kills | intake | healed | pets |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| **CAMP** | 5,055 | **412.65 s** | 156 | 6 / 20 | 217 | 95,358 | 74,918 | 139 |
| **CAMP+DODGE** | 5,055 | **412.65 s** | 156 | 6 / 20 | 218 | 97,671 | 77,231 | 140 |
| **DRIVE+DODGE** | 5,087 | **415.27 s** | 156 | 6 / 20 | 214 | 112,201 | 91,630 | 130 |
| **DRIVE** | 5,088 | **415.35 s** | 156 | 6 / 20 | 213 | 114,059 | 93,487 | 129 |

**The divergence from reference truth is total and it is the headline: the sim player dies where
Matt lived.** Nothing was tuned toward survival (charter Law 3) and nothing will be.

**The four cells are separated by 2.70 s = 0.65 %.** CAMP and CAMP+DODGE are **identical to the
tick**; DRIVE and DRIVE+DODGE differ by **one tick**. On this substrate **neither main effect nor
the interaction is measurable** — the 2×2 collapses.

---

## 4 — Damage composition, sustain, reach

| cell | %-current-life | direct | DoT | leech | hits/misses | land rate | crits |
|---|---:|---:|---:|---:|---:|---:|---:|
| CAMP | 26.1 % | 64.9 % | 7.5 % | 1.6 % | 184 / 52 | 78.0 % | 0 |
| DRIVE | 33.4 % | 59.1 % | 6.2 % | 1.3 % | 190 / 59 | 76.3 % | 0 |
| DRIVE+DODGE | 32.4 % | 60.2 % | 6.2 % | 1.2 % | 184 / 59 | 75.7 % | 0 |
| CAMP+DODGE | 26.5 % | 64.5 % | 7.4 % | 1.6 % | 185 / 53 | 77.7 % | 0 |

**Zero crits in ~950 resolved attacks**, and that is *correct*, not a bug: folded per R-PM2-3 the
roster's PTH runs **66.3 / 77.8 / 84.6** (min/median/max) against DA 2,591, and `pthThreshold2` is
**90**. Nothing on this board can reach the first crit band. The PTH **floor of 55 never binds**
either — the floor and the crit ladder are both inert here, and that is a measurement about this
matchup.

**Reach dominates opportunity: 71–74 % of all attack opportunities are OUT OF REACH.** ~1,300
opportunities per cell yield only ~240 resolutions.

### Sustain — and § G.5 is badly wrong

| cell | regen offered | **ADCtH offered** | landed | overheal | landed / intake |
|---|---:|---:|---:|---:|---:|
| CAMP | 53,378 | **2,317,895** | 74,918 | 2,296,355 | **78.6 %** |
| DRIVE | 53,727 | **2,184,246** | 93,487 | 2,144,486 | **82.0 %** |

I predicted healing would be **< 15 %** of intake. It is **78.6–82.0 %**, and ADCtH *offers* **24×
the total damage taken** while **96 % of it overheals**. Sustain is not a rounding error; it is the
entire defence.

---

## 5 — ⚑ WHAT ACTUALLY KILLS THE PLAYER (the finding I did not predict at all)

| | CAMP | DRIVE |
|---|---:|---:|
| mean HP across the run | **19,546 / 20,005 (97.7 %)** | 19,487 (97.4 %) |
| ticks below 50 % HP | **18 of 5,055 (0.4 %)** | 54 of 5,088 (1.1 %) |
| ticks below 25 % HP | 10 (0.2 %) | 18 (0.4 %) |
| **of the FINAL 200 ticks, how many had NO player damage output** | **182** | **180** |
| killer | `w156_a010`, 20 bodies live | `w156_a004`, 14 bodies live |

The camp cell's last hundred ticks, sampled every tenth:
`16047 → 12996 → 19585 → 20005 → 18489 → 18271 → 16928 → 15585 → 11816 → 4388 → dead`.

**Read it:** the bar is *full* four samples before death. The player is not ground down over a
wave — the player is **snapped from full to zero inside about eight seconds**, and the thing that
changed was not incoming damage but **outgoing** damage. 21 % ADCtH on a kill term that one-shots
makes the player effectively immortal *while there is something inside the disc*, and makes them a
20,005-HP bag with 129 hp/s of regen the moment there is not. **91 % of the final two hundred ticks
were dry.** Wave 156 arrives with the board thinned, the drip spread out, and ranged attackers
(reach out to 90 m) still firing from outside the 3.0 m disc.

**So the survival mechanism this build actually runs on is kill throughput, not the defensive
sheet** — and the defensive sheet is exactly what F-1 went and measured. The cell that would test
this is not in the F-5c matrix: it is *the same fight with leech switched off*, which would separate
"tanky" from "sustained". **Not run; not in scope; named here.**

Top incoming skills (CAMP): `aetherialcorruption_rotskin` 12,992 · `livingplant_venomousseed`
12,877 · `chthonianherald_chaosblast` 8,266 · `witch_necroticmissiles` 7,328 ·
`thornedhorrorfrost_icethornfield` 6,346. By slot: **`initial` 77 rows, `basic` 47, specials 22,
`dying` 10, pets 4.** The **`initial` slot — the opening attack — is the single largest incoming
family**, which is a spawn-timing consequence worth someone's attention.

---

## 6 — PRE-REGISTERED PREDICTIONS vs OUTCOME

| # | prediction (written before the run) | outcome |
|---|---|---|
| **G.1** | player dies in all four cells, **inside the first two waves** | **HALF RIGHT.** Dies in all four — in **wave 156, the 6th**, at 412–415 s. Direction right, magnitude wrong by 3×; the § K.2 correction is why |
| **G.2** | ordering `CAMP < CAMP+DODGE < DRIVE < DRIVE+DODGE` | **FALSIFIED.** Actual `CAMP = CAMP+DODGE (412.65) < DRIVE+DODGE (415.27) < DRIVE (415.35)`. Spread **0.65 %**; the ordering is noise, and the two camp cells are identical to the tick |
| **G.3** | dodge changes time-of-death by **< 10 %** | **CONFIRMED, and then some.** 0.00 % on camp, **−0.02 %** on drive |
| **G.4** | **< 100** pets ever spawn | **FALSIFIED, narrowly.** 129–140 spawn (vs a 1,117-body declared worst case) |
| **G.5** | healing is **< 15 %** of damage taken | **FALSIFIED, badly.** **78.6–82.0 %**, with 24× that offered and 96 % overhealed. This is § 5 |

**Three of five falsified.** Per PM-1's precedent that is the lap working, not the lap failing.

---

## 7 — ⚑ FOUR DEFECTS IN MY OWN MODEL, found by empirical inspection (Discipline #11)

Math note § K carries these in full; they are **appended** to the note, not folded back into it — a
math note edited to look prescient has stopped being evidence.

| # | defect | how found | effect |
|---|---|---|---|
| **K.1** | `tg2_attack_damage.csv`'s grain is the **(owner→pet) contract**; mine is the **body**. A pet reachable from four summoners had its slot summed **four times** | reading **one** `damage_taken` row and seeing 64 % of the bar from a table whose max is 35 % | 132 rows, 13 of 68 pet bodies. Death **3.92 → 5.22 s** |
| **K.2** | **`delay_s` — measured data I had and did not use.** Populated on **482/482** special slots and **ZERO** basic/initial/dying. Median 6–9 s vs swing periods 0.42–1.98 s: I over-fired every special by **5×–15×** | looking at the column's population by slot | Death **5.22 → 412.65 s.** **79× on the headline number** |
| **K.3** | the telegraph centre is **measured** (`projectileExplosionRadius` = player-centred; `skillRadius` = caster-centred). I centred every telegraph on the player, making novas unescapable *by construction* | reading the names in the escapable set — they were all novas | escapable slots **25/135 → 45/135** |
| **K.4** | **the dodge calibration is degenerate** | running the bracket ends before bisecting | § 8 |

Plus two the assert wall caught: `damage_applied` on a killing blow was the *computed* swing, not
the actual reduction (event sum vs HP track disagreed by up to 323 hp on 4 rows — the exact class
of defect L-27 exists to prevent); and **the wall's own check 11 read a per-second step against a
per-tick path** and reported 82 of 83 steps as partial. The wall catching its own defect is the only
kind of wall worth having.

**K.2 is the one that matters.** A single unused measured column was worth 79× on the answer. If
this cell had shipped its first result — *"the player dies in 3.9 seconds"* — it would have been a
confident, well-documented, fully-declared, **wrong** finding.

---

## 8 — DODGE: calibration outcome (⚑ DEGENERATE, reported not fudged)

| cell | telegraphs | inside-ticks | attempts | successes | **dodge-driven** | incidental | failures | rate | suppressed by refractory |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| DRIVE+DODGE | 50 | 304 | 4 | 1 | **0** | 1 | 3 | 0.25 | 260 |
| CAMP+DODGE | 44 | 246 | 4 | 2 | **2** | 0 | 2 | 0.50 | 183 |

**The one calibrated constant could not be calibrated.** Success is **0.375 (3/8) and IDENTICAL at
`L0 = 0.01 s` and `L0 = 4.00 s`** — flat across a **400×** bracket. Reaction latency is **never the
binding constraint**, so bisection has nothing to bisect and **no value of `L0` reaches Matt's
~50 %**. The calibrator detects this and says so; `L0` stays at its module default **0.400 s** and
the achieved rate is reported **as a measurement, not as a fit**.

**The ceiling is geometric.** At *zero* latency only **45 of 135** telegraph slots (**33.3 %**) can
be escaped at all: measured wind-ups (median **0.70 s**, max 2.20 s) are shorter than a 5.4 m/s
player needs to clear measured extents (median **7.0 m**). **Matt's ~50 % is unreachable on this
substrate**, and producing a number that *looked* calibrated would have been the single most
dishonest thing available in this lap.

The **attribution split earns its keep**: of DRIVE+DODGE's one success, **zero were dodge-driven** —
the drive policy happened to carry the player clear. Without that column the avoidance AI would have
been credited with someone else's work.

Matt's favour-criteria **emerge** as designed: "nearer the edge" from an argmin over remaining
escape distance, "inside longer" from per-tick trigger evaluation. **No coefficient encodes either,
and `dodge.py` contains ZERO RNG tokens** (asserted by check 8 against the module source).

---

## 9 — PET LOAD (F-6(a))

| | |
|---|---|
| substrate | **47 summoners → 68 pet profiles → 149 contracts**, Lap B gate CLEAN |
| **declared worst case** | **1,117 bodies** — ⚑ **not the charter's 960.** Applying R-PM2-4's petLimit-12 to the **36 cap-less contracts** adds 157. Sized for 1,117; **no silent truncation** |
| actually spawned | **129–140** per cell (11.6–12.5 % of worst case) |
| pet attacks landed | 26–30 per cell |
| **caps that bound** | **16 distinct (owner, pet) contracts** per cell — declared, per R-PM2-7 |
| **`pet_special_slots_ungated`** | **51** — see below |

⚑ **A declared under-read.** `tg2_attack_slots.csv` is roster-only: **0 of 56 pet records appear in
it**, so **no pet special carries a measured `delay_s`**, and only **13 of 58** pet special skills
declare their own `skillCooldownTime`. Borrowing the roster's delay distribution would be inventing
a quantity (GL-12); firing them ungated would repeat K.2's 5×–15× over-fire. **So a pet special with
no measured reuse gate does not fire — 51 slots, counted on the wire.**

---

## 10 — DECLARED ASSUMPTIONS + GAPS (every one on the wire)

**Folds where the corpus is silent and I chose** (all in `threat.declared_constants()` and in the
`PM2-DECLARED-FOLDS` informative row): OA fold order per `combatformulas` with **`dexterityDV`
ABSENT → zero** · mitigation order **resistance then armour** (the lower reading) ·
**SEM-1 = total-over-duration** (R-PM2-1, the lower reading) · `percent_current_life` **unmitigated
and floored so it cannot kill alone** (R-PM2-5) · pet cap **`petLimit`=12 on 36 cap-less contracts**
(R-PM2-4) · pet locomotion **straight-line pursuit** (no spawn point, no patrol node) · telegraph
extent from **every** AOE carrier (R-PM2-6) · telegraph **centre from the extent carrier** (K.3) ·
special-slot `delay_s` as **both** initial gate and reuse cooldown (the lower of two semantics).

**Threat this model does NOT carry, named rather than shown as a measured zero:**
**286 of 4,692 MEASURED rows** are control/debuff/modifier families (stun, freeze, fumble, sunder,
resistance reduction) — real, and needing a player control-state PM-2 lacks · **191 tree-only
buff/other rows** · **30 rows** at non-`MEASURED` rank (R-PM2-2) · **2** unresolved-in-arz ·
**51 ungated pet specials** · **1,860 tree rows deduplicated against their slot twin** and **132
path-duplicates** (K.1) — those two are corrections, not exclusions.

**L-0 played-save cross-check** — § 12.

---

## 11 — SEAM WORK (star-lord: two rulings + one real schema request)

Both filed in `export/MIGRATION.md [2026-08-12]` and `simulation/MIGRATION.md [2026-08-12]`.

1. **⚑ SCHEMA REQUEST — `actors[].threat_tier` is `Literal["trash","hero","boss","nemesis"]` and has
   no member for a SUMMONED body.** Up to 1,117 pet bodies cannot be actors. **I did not retype a
   countersigned Literal from the simulation seam.** Interim, all declared: pets ride
   `waves[].pets`; **a pet's damage is attributed to its SUMMONER** with the pet id preserved on
   `damage_source_tag`; pet-*targeted* rows and the two off-enum families (`pet_spawn`,
   `dodge_attempt`) are withheld and counted (494 withheld / 21 re-attributed on the camp cell).
   ⚑ Withholding pet-*sourced* rows **broke the wire's HP chain and AC-11.7e caught it immediately
   and correctly** — the re-attribution is what keeps the player HP series exactly reconstructible.
2. **VALIDATOR REFINEMENT — `AC-11.7b` / `M-26` key gains `source_id` + `damage_source_tag`.** The
   invariant is unchanged; the old key omitted two fields that were *constants until incoming damage
   existed*. **Strictly stronger**, byte-identical on player-sourced rows, and both frozen batons
   re-validate at 66/66.
3. Incoming damage rides **`damage_dealt` with `target_id="player"`**, not a new family — the closed
   enum already carries direction on `target_id` (R-25). The charter's suggested `damage_taken` was
   **not** minted. `player_death` was already in the enum and had simply never been emittable.

Also moved: `monster_attack_model` → **`geometric`** (the Literal already had the member; this lap
makes it true) · `player_hp_increase_sources` off `[]` (M-17 reads the empty list as a declaration) ·
`mitigation_model` / `damage_semantic` (**incoming rows read `damage_raw` as PRE-mitigation**) ·
outcome/termination enums gain `player_death` / `player_died`, versions → 2.

**drax / any scene consumer:** the nine `PM2-*` wire declarations are the read-this list; the three
semantic shifts (player HP is a curve · attack model is geometric · R-L53-2 retired) are the ones
that cost money if ignored. **rocket:** nothing. **jack-ryan:** Discipline #1, #2, #11, #12 all
exercised and named.

---

## 12 — L-0 PINS AND THE PLAYED-SAVE CROSS-CHECK (a real finding)

**L-0 at launch:** engine HEAD `6c4a7472` · **porcelain 2,789 = the FG-17 baseline exactly** ·
both frozen baton digests **verified from bytes** · all 8 substrate files digest-verified.
**At landing:** HEAD `c2b4d716`, porcelain **2,793** = baseline + the four new batons.

⚑ **A scope error I made and corrected:** my first export commit used `git add -A` on the simulation
tree and swept in **2,649 pre-existing untracked artifacts** under `simulation/output/` belonging to
earlier laps. Caught by re-reading the porcelain count against the L-0 pin (2,789 → 140 is not a
plausible delta for fifteen files). Soft-reset, re-staged by explicit path, nothing left the
worktree, and the re-commit says so.

### The played-save cross-check — Lap A's cliff C-3 BINDS, and I got past it far enough to matter

`gd_gdc_parse.py` **fails outright** on the played save: it handles only the plaintext case
(`seed == 0x55555555`, which zeroes the cipher table). **The played save's seed is `0x5298565B`, so
it is encrypted** — Lap A's documented cliff C-3, firing exactly where it said it would.

I solved the cipher rather than shrug at it, by **known-plaintext against the `GDCX` magic**, then
confirmed it on the next two `u32`s. The schedule: `key₀ = seed ^ 0x55555555`; table entries
`k = rotr(k,1); k = (k × 39916801) mod 2³²`; a `u32` read is `plain = cipher ^ key` followed by
`key ^= table[b]` for each of the four **cipher** bytes. Verified by the first three `u32`s decoding
to `GDCX`, `2`, `11`.

**Result — the header identity block decodes EXACT and matches the pristine save three ways:**
name `EoRWarlGuts` · `class_tag` `tagSkillClassName0109` (Soldier + Oathkeeper) · `level_header`
**100** · sex 1 · hardcore 0 · file_version 2.

**Residual, bounded and handed back:** the block walk desyncs immediately after `hardcore`, where
GD's read granularity (byte vs `u32`) stops matching Lap A's field order. Chasing it further is
**legolas's instrument, not mine**, and it is **non-blocking**: F-1 ranks screenshots PRIMARY and
**every** input this sim consumes (HP, OA/DA, armour, resistances, ADCtH, regen) comes from
screenshots. Size delta pristine → played is +10,281 B (87,820 → 98,101), unexplained but consistent
with post-play state.

**No pristine-vs-played contradiction was found in anything the sim consumes.**

---

## 13 — SELF-ATTACK SURFACES (what I would want a second pair of eyes on)

1. **`percent_current_life` is 26–33 % of intake and I cannot check its player-facing semantics.**
   R-PM2-5 ruled INCLUDE and I did, unmitigated, floored so it cannot kill alone. If GD reduces
   monster %-current-life against players — plausible, and **not measurable from this corpus** —
   every survival number here is conservative by a quarter. **Most consequential unverifiable term.**
2. **The special-slot `delay_s` semantics are inferred from a distribution, not from a definition.**
   482/482 specials, 0/482 weapon swings is a very loud signal, and it is still my reading of an
   undocumented field. I apply it as *both* gate and cooldown because that is the lower reading —
   but if it is initial-delay-only, incoming damage rises again.
3. **`E* = 4.0 m` for "large telegraphed AOE" is anchored to the disc radius, which is a *choice of
   anchor*.** It selects 135 of 304 AOE-bearing slots. A different threshold moves the dodge
   population, though § 8's geometric ceiling suggests not the conclusion.
4. **The attention-load `κ = 0.02` is untested by anything** — § 8 proves latency is not binding, so
   κ has no measured consequence in this run at all. It is a declared constant doing no work.
5. **Attributing a pet's damage to its summoner is an indirection I invented** to keep the HP chain
   whole. It is declared and reversible, and it is still a fiction about who hit the player.
6. **I wrote in star-lord's seam again** — four export files, two of them *validator predicates*.
   Minimal, MIGRATION-filed, both frozen batons re-validating. Still: a sim agent loosened-then-
   tightened a countersigned check, and § 11.2 is the sentence to argue with.
7. **The four cells being indistinguishable may be a property of the death mechanism, not of the
   policies.** If § 5 is right — death comes from a kill drought — then seek policy and dodge are
   both irrelevant *because neither changes kill throughput at wave 156*. That is a hypothesis this
   lap did not test.

---

## 14 — QUESTIONS FOR THE CONDUCTOR / MATT (all veto-open, none blocking)

1. **§ 5 — should the next cell switch ADCtH OFF?** It is the one variable that separates "this
   build is tanky" from "this build is sustained", and everything in § 5 says it is the second.
2. **§ 8 — Matt's ~50 % dodge target is geometrically unreachable here (ceiling 33.3 %).** Re-aim
   the directive, or accept the measured rate as the answer?
3. **§ 11.1 — star-lord: add `"summon"` to `threat_tier`, or rule pets permanently off `actors[]`?**
4. **§ 13.1 — does anyone have a way to check monster %-current-life against players?** It is the
   largest unverifiable term in the model.
5. **The `initial` slot is the biggest incoming family (77 of ~170 rows).** Spawn-timing consequence
   or model artifact? I lean artifact-adjacent and did not chase it.

**No HALT was hit.** Nothing required inventing an unmeasured quantity — every silence was either
declared with the lower reading or refused outright. Nothing was tuned toward survival; the only
fitted constant in the lap turned out not to be fittable, and that is reported rather than papered
over.
