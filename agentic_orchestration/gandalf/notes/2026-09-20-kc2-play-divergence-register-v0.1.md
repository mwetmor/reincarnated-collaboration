# KC2-PLAY · THE DIVERGENCE REGISTER — **v0.1**

> **STATUS:** CURRENT — **v0.1, 2026-09-20. SUPERSEDES v0 FORWARD.**
> **v0 (`1f5489af`, sha256 `3da22dfa0421…`) is NOT edited.** Superseded readings named in place at § A. **No T-B recording exists under v0** (§ F), so this amendment pools nothing.
> **Occasioned by:** **KP-5** (the v0 open questions ruled) · **KP-6** (galadriel: `u`, the T-B reference corrections, the denominator law) · **KP-7** (gamora: two corrections to the charter, both the conductor's own — the Banner's magnitude and the known-bad limbs) · **KP-9** (coverage denominator 89) · **KP-10** (Type-B σ = 48 ms).
> **Companion:** `2026-09-20-kc2-play-ta-prereg-v1.1.md` — **no `DIV` row below is graded by T-A, by construction.**
> **Sources cross-pinned by sha256:** gamora band widths **`a7984b7926324edf…`** · galadriel W1 T-B + `u` rider **`0411e6b805e2baa9…`**.
> **Author:** gandalf (named sub-agent, `SPEC-AUTHOR`), Wave 1.

---

## § A · CHANGE TABLE — v0 → v0.1

| row | v0 | **v0.1** | reason | ledger |
|---|---|---|---|---|
| **DIV-07 Banner** | *"a positional **×2.0** on outgoing damage"*; player sentence *"doubles your damage"* | ⚑ **×1.0319, ADDITIVE.** `banner_additive=True` is of record: the `+100 %` lands on a sheet **already carrying +3036 % physical**. Radius 8 m, per-tick, no hysteresis, MODEL-BOUND status and the probe row **all stand**. The feel case shrinks to **≈ 3 %** | the charter's R-KP-0f magnitude was relayed to Matt as fact before it was checked against the driver. **drax must not build ×2.0** | **KP-7 (i)** |
| **DIV-14 potion** | ORACLE auto-fires at **θ 0.49** (`I4_EXCURSION_MAX`, measured-falsified 5/9) | ⚑ **ORACLE auto-fires at θ 0.22972972972972974** (`PotionLimb.TRACE_CONSISTENT`). PLAY: **manual key, auto-fire OFF** (KP-5(6) stands, number corrected) | `I4_EXCURSION_MAX` is a `load_kit()` **default the driver OVERRIDES**. ⚑ *A divergence row written against 0.49 would describe a divergence from a configuration nobody graded* | **KP-7 (ii)** |
| **ND-04 known-bad limbs** | ⚑ **"THREE, not two"** — a correction *I* raised against charter L4 | ⚑ **ONE.** Only `LifeMonitorLimb.POLL_AT_SLOT` survives. **War Cry `I8_LEGACY` and Potion `I4_EXCURSION_MAX` are STRUCK AS FALSE-OF-THE-ORACLE** — the cell of record runs `WarCryLimb.COOLDOWN` (7.5 s) and `PotionLimb.TRACE_CONSISTENT` | ⚑ **My own correction was wrong in the same way as the thing it corrected.** v0 read census (c-4), which read **module defaults**; `V0` is the row-set whose entire purpose is that `MODULE-DEFAULT` and `DRIVER-OF-RECORD` are different claims about the same value. Recorded loudly rather than quietly fixed | **KP-7 (ii)**; widths A5 |
| **DIV-09 `u`** | *"registered runtime choice inside `[0.22277, 0.3663]`"*, no value | ⚑ **`u = 0.285`** (galadriel's `DR-u`), window `[0.22277, 0.3663]`, ⚑ **operative sub-window `[0.246, 0.324]` — 1.32×, the tightest defensible statement in the corpus.** Arena **57.3 × 76.7 m**, max chord **77.0 m** vs the sim's 87.5 m — **12 % tighter** | ⚑ **`u` is UNPINNABLE-FROM-COMMITTED-DATA**: every route reduces to `u = s/g` and the corpus holds two committed ground scales 2.3–2.4× apart; the spawn-points↔green-zones registration was **tested and REJECTED** (invariant differs 29×). **A CHOICE, never a pin.** R-KP-0c's declared expectation arrives as a number | **KP-6 (a)**, **KP-9 (2)** ratified against the wave |
| **DIV-13 entry state** | UNRESOLVED | ⚑ **RULED (veto-open): PLAY resumes the `cp150` fixture and OPENS AT WAVE 151.** A played wave 150 is a **labelled pre-roll excluded from every statistic**; `entry_state_source` in the recorder header | ⚠ touches Matt's F6 wording (*"waves 150–160"*) — **surfaced to him at the G-IMG checkpoint** | **KP-5 (5)** |
| **DIV-15** | *(absent)* | ⚑ **NEW — bar-slot skill NAMES are `DECLARED-not-decoded`.** T-B interrupt rows ship **SLOT-INDEXED**; the names on slots are a presentation-side declaration, given the same treatment R-KP-0f gives the Banner's placement | the measuring lap forbids naming. ⚑ **The flag VALUES stay model-grade** (Blitz `true` / Vire's `true` / War Cry `false`) and **D-CP2-2 is untouched**; only the *skill attachment* is declared | **KP-6 (b)** |
| **DIV-03 test reference** | footage vectors at cast rate **0.290 /s, n = 53** | ⚑ **0.2957 /s, n = 54, one per 3.383 s — and it is a FLOOR, not an estimate** (slots 7 and R blind; re-fire mid-cooldown undetectable in principle; 3 OCR-blind dim gaps carried) | the 2c lap eye-adjudicated a 7.20 s slot-L dim run against that slot's 3.60 s modal cooldown and split it into **two** casts (`eor_attrib.MERGED`); slot L 12 → 13, total 53 → 54. **The correction cost that lap its own hypothesis** (slot-L rate 0.417 → 0.385) — the tell that it was not a convenience | **KP-6 (b)** |
| **DIV-04 authority** | Type-B range 0.53–0.67 s, n = 8; σ ≈ 49 ms inferred | ⚑ **σ = 48 ms, MEASURED** — confirming Gate-1 WARN-17's strike. **KP-1 rests on the WITHIN-SUBJECT CONTRAST, not on an impossibility claim** | all five release reproductions check exactly | **KP-10** |
| **ND-08 (c-2)** | **PENDING-W1** — both candidate values carried | ⚑ **RESOLVED: the PACK row is stale, the oracle is right.** `ehp = base_life × (1 + (G + ultimate + life_passive)/100)`, **790/790 within 1.0 hp**, **no armour or resist term inside eHP** (232 records at identical `base_life` with armour 991 vs 1308 carry **byte-identical** eHP). Mitigation is applied per body **on top**. `mitigation_note` **retired**; `stat="ehp"` a declared semantic shift (MIGRATION rides) | a pack-following builder kills armoured bodies **up to 1.902× too fast** (median 1.098×; exactly **1.000× on a zero-armour body — the positive control**) | **KP-7** |
| **§ 5 INSTRUMENT class** | founding case B-8 (`frac_moving` 1.41× across three instruments) | ⚑ **adds the LIVE-MAX denominator law and the two windows** (§ E.1) | **42.84 % requires `LIVE-MAX`; NOMINAL gives 39.76 % — a 3.08 pp gap with no fight in it** | **KP-6 (c)** |
| coverage denominator | 72 | **89 enumerated row ids** | *a gate must count things it can list* | **KP-9 (1)** |
| ND-06 scatter trap | *"falsified by E-7a/E-7b"* — indirectly, W1 arms only | **now directly closed by prereg `TA-X-17` + `TA-X-18`**, every arm | E-7b reported a spawn-law defect **as a wall statistic** | prereg § E |

---

## § B · INDEX

| id | switch | class | status |
|---|---|---|---|
| **DIV-01** | arena wall — circle `R = 43.758…` m vs the video-measured ring at `u = 0.285` | DIVERGENCE | ACTIVE |
| **DIV-02** | spawn-pool DoT — `0.0` vs D-LIFT-1/2 | DIVERGENCE | ACTIVE |
| **DIV-03** | cast-interrupt — uniform 0.15 cancellation vs the per-skill flag | DIVERGENCE | ACTIVE |
| **DIV-04** | Type-B auto-resume under held RMB | DIVERGENCE | ACTIVE (Matt-accepted, KP-2 L5) |
| **DIV-05** | pilot — `DRIVE_TO_PACK` vs Matt's hands | DIVERGENCE | ACTIVE |
| **DIV-06** | bound-skill additions OFF vs ON; riders `PLACEHOLDER-INERT` | DIVERGENCE | ACTIVE |
| **DIV-07** | ⚑ Banner **placement** (magnitude ×1.0319 is MODEL-BOUND, not a divergence) | DIVERGENCE | ACTIVE — **magnitude corrected** |
| **DIV-08** | summons presentation — no health bar, no view-side `hp` | DIVERGENCE | ACTIVE |
| **DIV-09** | ⚑ `u = 0.285` (galadriel's `DR-u`) — the metre scale the oracle does not have | DIVERGENCE | ACTIVE — **value landed** |
| **DIV-10** | zoom register — `ZOOM-GD` 75.668 px/m default, `ZOOM-HOUSE` 160.394 toggle | DIVERGENCE | ACTIVE |
| **DIV-11** | player kinematics at render rate, sampled per tick | DIVERGENCE | ACTIVE |
| **DIV-12** | one life · restart key · scope window | DIVERGENCE | ACTIVE |
| **DIV-13** | ⚑ entry state — **resumes `cp150`, opens at 151** | DIVERGENCE | **RULED, veto-open (Matt at G-IMG)** |
| **DIV-14** | ⚑ potion agency — ORACLE auto-fires at **θ 0.2297**; PLAY manual | DIVERGENCE | **RULED, veto-open (the KEY is F3 = Matt's)** |
| **DIV-15** | ⚑ bar-slot skill **names** `DECLARED-not-decoded`; T-B rows slot-indexed | DIVERGENCE | **NEW** |
| **ND-01** | fire-time resolution — strafing does not dodge | ND + confound | CARRIED |
| **ND-02** | no player crit | ND + confound | CARRIED |
| **ND-03** | base cooldowns; CDR not recovered | ND + confound | CARRIED |
| **ND-04** | ⚑ **ONE** known-bad live limb (`LifeMonitorLimb.POLL_AT_SLOT`) | ND + confound | **CORRECTED 3 → 1** |
| **ND-05** | `health_max` constancy (`D-Q1` / B-18) | ND + known model gap | CARRIED |
| **ND-06** | spawn scatter — polar disc in both; the pack says box | ND + pack trap | CARRIED — **trap now closed in T-A** |
| **ND-07** | `hit_test_model` — pack says `"point"`; both run the 3.0 m disc | ND + pack trap | CARRIED — **half-closed by `TA-X-20`** |
| **ND-08** | monster-side mitigation | ND + **RESOLVED** | **RESOLVED — moves the hash (§ F)** |

*Rows unchanged from v0 in substance (DIV-01…06, 08, 10…12; ND-01…03, 05) keep v0's text, tests, directions and handoff sentences; only what the change table names has moved.*

---

## § C · THE ROWS THAT MOVED

### DIV-07 · VANGUARD BANNER — magnitude corrected, placement still the divergence

| | |
|---|---|
| **ORACLE = PLAY (MODEL-BOUND, not a divergence)** | `offensiveTotalDamageModifier = +100 %`, **`banner_additive = True`** ⇒ the realised multiplier on player outgoing damage is **×1.0319**, because the `+100 %` is one additive term on a sheet already carrying **+3036 % physical**. Radius **8 m**, evaluated from the player's own position **every tick, no hysteresis, no grace period**. |
| **THE DIVERGENCE** | **placement only.** `D-1`: no coordinate is minted; the four defences sit on the sim's own `PatrolPoint_Attack` anchors, greedy ascending radius, separation floor = the 8 m aura. The runner-up anchor sits **2.27 m outside** the aura. PLAY draws the aura at true radius with a HUD icon that drops the instant you leave, and emits occupancy against **all eleven anchors**. |
| **How it is tested** | geometry-true probe asserts **8.0 m** against the census figure (`defenses.py:10-14`) until V14 lifts it into the pack (the provenance is named because the Banner is **in no pack member**); unit probe: stepping 7.9 → 8.1 m changes outgoing damage **on the next tick**, by **×1.0319 ÷ 1**, with no hysteresis. |
| **Expected direction on T-B** | ⚑ **Small, and this is the correction that matters most to the build.** At ×2.0 the Banner was the single most feel-bearing Crucible term; at **×1.0319** the whole effect is **≈ 3 %**, well inside every band, and the placement's knife-edge stops being a T-B hazard and becomes a presentation detail. **Damage rows no longer require banner-occupancy beside them to be interpretable** — they are simply better with it. |
| **Handoff sentence** | ⚑ *(rewritten — v0's "doubles your damage" is false)* **"The banner's ring gives you about 3 % more damage inside 8 metres, instantly, with no grace period. It was described to you as double; it is not — the +100 % is one additive line on a sheet that already carries +3036 %. We still draw the ring, because it is the only Crucible term you can act on."* |

### DIV-14 · POTION AGENCY — θ corrected

| | |
|---|---|
| **ORACLE** | `defaulthealthpotion.dbr` + HoT — **800 flat + 25 % instant + 25 % HoT, cd 12.0 s, 1 charge** — auto-fired by the policy at ⚑ **θ = 0.22972972972972974** (`PotionLimb.TRACE_CONSISTENT`, the cell of record). The potion is `RequestUseItem`, **decoded PERMITTED in every control state**. |
| **PLAY** | **bound to a key; auto-fire OFF.** ⚠ **The key itself is F3's surface and therefore Matt's** — asked at the G-IMG checkpoint. |
| **How it is tested** | unit probe on magnitude / cooldown / charge against the census values; recorder emits `potion_use` with `trigger ∈ {"auto_theta","player_input"}`; ORACLE asserts `trigger == "auto_theta"` on 100 % of uses. **V13 (Tier 2) carries the potion's PARAMETERS cleanly separable from its θ POLICY**, which is what makes the manual bind a one-line configuration rather than a fork. |
| **Expected direction on T-B** | lands squarely on the HP trace — **B-11…B-18**, the richest T-B family. Moves *time at full health* (**42.84 %**), *time below 50 %* (**3.46 %**) and *HP min* (**5,360 of 20,005 = 26.79 %**) together. |
| **Handoff sentence** | *"The health potion is yours to press. The simulation drank automatically whenever it dropped below about 23 % health; you will not, and the health graph is where that shows."* |

### DIV-09 · `u` — the value landed (galadriel's `DR-u`)

**ORACLE:** *not applicable* — the oracle runs on an unbounded open plane with a derived `R_wall = 43.758 m` and **never consults `u`**.
**PLAY:** **`u = 0.285` m per native minimap px** — a **registered runtime CHOICE, not a pin, not a measurement**. Window `[0.22277, 0.3663]` (R-L3-2); ⚑ **operative sub-window `[0.246, 0.324]` — 1.32×**, the intersection of the window with the character chain at the **measured** θ = 43.95° (B1 lap G-e fit, n = 1,275).
**Why a choice and not a pin:** `u` is **UNPINNABLE-FROM-COMMITTED-DATA** — every route reduces to `u = s/g`, the corpus holds two committed ground scales **2.3–2.4× apart**, the spawn-points↔green-zones registration was **tested and REJECTED** (invariant differs **29×**), and the traced arena's identity among 20 decoded Crucible maps is undetermined. Its warrant is narrow and stated: it is the **only committed route whose every term is measured rather than assumed in the direction that matters**, and it lands inside a window derived by a **completely independent argument**. *Two independent lines converging inside a 1.64× window is the strongest thing on the table; it is not a pin.*
**What it makes the arena:** ring extent **57.3 × 76.7 m**, max chord **77.0 m** — against the sealed sim's 87.5 m across, **12 % tighter**. ⚑ **R-KP-0c's declared expectation arriving as a number, not a surprise.** *(And at the window floor the ring's 60.2 m chord could not contain the 65.72 m spawn spread — an independent nudge away from the low end.)*
**How it is tested:** `u` read from **exactly one symbol**; the plate authored in **native px**, so a later pin is a one-line change and a camera re-gate, never a re-authoring; any metre readout drawn from the ring **displays `u` and its window beside it**. **Claim class: `PRESENTATION-CHOICE-NOT-MODEL-TRUTH`.**
**Handoff sentence:** *"The arena is about 77 metres across, and that number is a choice inside a range we could not close — the map's scale is not recoverable from anything we have committed. It is 12 % tighter than the simulation's arena, which is expected, and if distances feel wrong this is the first thing to suspect."*

### DIV-13 · ENTRY STATE — ruled

**PLAY resumes the `cp150` fixture and opens at wave 151.** A played wave 150 is a **labelled pre-roll excluded from every statistic**, with `entry_state_source ∈ {"cp150_fixture","played_150"}` in the recorder header and a grader that **refuses to pool the two**. *Reason:* otherwise the first graded wave's entry conditions (energy, cooldown phase, potion charge, breaker cooldowns, HP) are pilot-determined, and the whole 151–160 comparison inherits the **cold-start confound sibling S6 exists to measure — which is out of scope.** ⚠ **Veto-open and it touches Matt's own F6 wording; surfaced at G-IMG.**

### DIV-15 · BAR-SLOT SKILL NAMES — `DECLARED-not-decoded` *(new)*

**ORACLE:** the sim casts no bar skill by name; there is no naming surface.
**PLAY:** the HUD needs tooltips, so slots carry names — **and the measuring lap forbids naming them.** T-B interrupt rows therefore ship **SLOT-INDEXED** (slot L / 2 / 3 / 7 / R), and the names are a **presentation-side declaration**, the same treatment R-KP-0f gives the Banner's placement.
⚑ **What this does NOT touch:** the `interrupts_channel` **flag values** are model-grade and **D-CP2-2 stands** — *the values are model-grade while the skill attachment is a declaration.* Blitz `true` / Vire's `true` / War Cry `false` / Rune of Rush `UNDETERMINED` are unchanged.
**Tested:** every T-B row emits a slot index; a name never appears in a graded row, only in a tooltip.
**Handoff sentence:** *"The names on your keys are our best reading of the footage, not a measurement. Everything we grade is graded by slot, so a wrong name cannot make a wrong number."*

### ND-04 · KNOWN-BAD LIVE LIMBS — **ONE**, not three

| limb | what v0 (and charter L4) claimed | **the cell of record** |
|---|---|---|
| War Cry | `I8_LEGACY`, duration 5.0 — the retired invented literal that priced 19.43 % of incoming damage | ⚑ **`WarCryLimb.COOLDOWN`, 7.5 s — NOT-IN-CELL-OF-RECORD** |
| Potion | `I4_EXCURSION_MAX`, θ 0.49, measured-falsified 5/9 | ⚑ **`PotionLimb.TRACE_CONSISTENT`, θ 0.2297 — NOT-IN-CELL-OF-RECORD** |
| LifeMonitor | `POLL_AT_SLOT` | ⚑ **LIVE — the one survivor.** `sustain_procs_fold` not passed ⇒ the repair limb is not installed. The breakers poll a **post-lift** HP value and measurably miss floor ticks: **Turtle 51 vs 41 seen, Menhir 13 vs 10**; in waves 151/153 the censored tick was the only sub-threshold tick — **the breaker was off entirely there** |

⚑ **This is my own correction corrected.** v0 raised *"three, not two"* against charter L4; the measurement says **one**. v0 read census (c-4), which read **module defaults** — the identical defect v0 itself catalogued at ND-06 and ND-07 (*the pack steers the builder wrong*), committed by the register against the sim. **All three are carried in `V0` as `V0-KB-*` rows with their status, so the record is correct rather than merely three-long.**
**Handoff sentence:** ⚑ *(rewritten)* **"One of the simulation's settings is known to be wrong and was kept anyway: the two emergency heals check your health slightly late and sometimes miss the moment they were built for. Two others were reported to you as wrong and are not — they were settings in a file the simulation overrides."**

### ND-08 · MONSTER-SIDE MITIGATION — **RESOLVED**

`ehp = base_life × (1 + (G + ultimate + life_passive)/100)` — **790/790 records within 1.0 hp, no armour or resist term inside eHP**; 232 records at identical `base_life` with armour 991 vs 1308 carry **byte-identical** eHP. **Mitigation is applied per body on top, and the oracle is right.** `mitigation_note` retired; `stat="ehp"` is a declared semantic shift and a MIGRATION rides with it. **A pack-following builder kills armoured bodies up to 1.902× too fast** (median 1.098×; **exactly 1.000× on a zero-armour body — the positive control that makes the result a measurement rather than a story**).

---

## § D · WHAT IS NOT A REGISTER ROW

Unchanged from v0: the 43-state AI graph (*the oracle never ran it*) · loot / levelling / meta / shop (F6) · Web / phone (F3) · pets (`L-83 D-3`) · celestial blessings (**a measured zero, both sittings** — the module *refuses* to read the counterfactual) · the three Crucible beacons' output (**they do not fire** in either config; cadence UNREAD; signed bias **away** from reaching 160, closable by one read of `skillCooldownTime` on three `turret*.dbr` records).

---

## § E · THE FIVE ATTRIBUTION CLASSES AND THE DECISION PROCEDURE

### E.1 · The five classes *(unchanged; `placeholder` folds into declared divergence, `instrument` takes the slot — WARN-2 discharged, adopted verbatim at KP-5(8))*

**1 PORT** (bounded, not eliminated, by T-A) · **2 DECLARED DIVERGENCE** (a `DIV-nn` row; **includes `PLACEHOLDER-INERT` riders**) · **3 MODEL GAP** (the `ND` confounds) · **4 PILOT** (Matt's hands, plus what he can see and what he chooses) · **5 INSTRUMENT** (same-named statistic, different denominator or window).

⚑ **Class 5's founding cases, both now named:**
- **B-8 `frac_moving`** reads **0.883 / 0.705 / 0.6265** across three footage instruments — a **1.41×** spread. Ratios ship regardless (D-MPOL2-2); *an absolute movement figure in a green report is a defect in the report.*
- ⚑ **The LIVE-MAX denominator law.** HP occupancy is computed against `hp_max` **as read at that frame** — **this is what reproduces 42.84 %**. The NOMINAL 20,005 denominator gives **39.76 %**: a **3.08 pp gap with no fight in it.** And the **HP window is 181.0 s** while **energy / motion / release / cast is 182.65 s** (0.90 % apart). **A grader that picks the wrong one manufactures a port defect.** *(This is also why per-wave durations from the two instruments agree to ≤ 0.19 s on waves 152–159 and disagree by 0.68 s and 0.88 s on w151 and w160 — not boundary error; different windows.)*

### E.2 · The procedure — cheapest-falsifier-first, stop at the first hit

**Step 0 · INSTRUMENT** — does the row's denominator and window match the footage instrument's, as the row's own definition states? *Test:* recompute the twin side on the footage instrument's construction; if the miss closes, confirmed.
**Step 1 · DECLARED DIVERGENCE** — is there a `DIV-nn` row whose **pre-registered direction matches the sign of the miss**? *Test:* **re-run the same fight under `ORACLE`** — buildable only because there is ONE runtime with two configurations.
**Step 2 · PORT vs MODEL GAP** — does the miss **survive under `ORACLE` with the scripted pilot**? Then: **T-A row red → PORT · T-A row green → MODEL GAP · no T-A row covering it → `UNATTRIBUTABLE-PENDING`**, named as a finding, ⚑ **never assigned to PORT by default.** *(The prereg's § E now lists exactly which surfaces have no covering row — the board roll above all.)*
**Step 3 · PILOT** — appears only with Matt at the controls and vanishes under the scripted pilot in the same config.
**Step 4 · none of the above** → **a defect in this register.** File a row, re-hash, record why it was missed.
**Tie-break:** assign the class whose OFF-state test is **cheapest to run**, run it, record the result. **Never by narrative plausibility** — that is how a port bug becomes a "model gap" and stops being fixed.

> ⚑ **The sentence this whole instrument exists to license:** *a green T-A row plus a T-B miss that survives under `ORACLE` with the scripted pilot is a **MODEL GAP**, not a port bug.*

---

## § F · THE REGISTER HASH, AND THE EPOCH STATEMENT

**Mechanics unchanged from v0 § 6.** The runtime **emits** the machine form from its own configuration tables (#72); this document is the **labelled expectation checked against it**, and a mismatch is a **COVERAGE FAIL** at prereg **P-1** (now 89/89). Machine form = a JSON array of `{"id","class","switch","oracle","play","authority","test","direction","status"}` rows; canonicalisation = rows sorted by `id`, keys sorted, UTF-8 NFC, whitespace collapsed, no insignificant JSON whitespace, no trailing newline; `register_sha256 = sha256(canonical_bytes)`, **derived at use, never retyped**; full 64 hex in the telemetry header, 12-char prefix in prose. A recording whose header hash does not match the register in force at grading time **is not comparable and the grader says so.**

### ⚑ THE EPOCH STATEMENT — asked for at KP-5(10), answered here

1. **(c-2) HAS resolved** (ND-08, KP-7). Its `status` moves `PENDING-W1 → RESOLVED`, the eHP semantic shift lands in **V6**, and **therefore the register hash HAS moved.**
2. ⚑ **EPOCH 1 begins at v3.2** — the lift complete at KP-8 (`kc2-lifted-rows-KC2PLAY-W1-v3p2-full-20260920_163932.json`, sha256 `e0117429…`). Every recording made from this point carries the **v0.1** hash.
3. ⚑ **EPOCH 0 PRODUCED ZERO RECORDINGS.** No runtime has yet written a telemetry file; the two-epoch rule therefore has nothing to un-pool and **fires forward only**. Recorded explicitly, because *"the rule was pre-declared and never needed"* is a disposition and silence is not.
4. **Forward:** any later `status` change re-hashes. Recordings under different hashes are **reported separately, never pooled**, and the W1 seal records the hash before and after.

---

## § G · OPEN QUESTIONS — one lean each

**OQ-1 · The Banner's correction changes a feel argument, not just a number.** → **Tell Matt the ×2.0 was wrong before he plays, in the same breath as the ring.** R-KP-0f's whole feel case (*"a human who drifts 8 m loses half his DPS with no feedback"*) is now false; the honest version (*"about 3 %"*) is less exciting and is the one that survives. A correction he meets at the controls costs more than one he reads.

**OQ-2 · DIV-14's key is F3's surface, and F3 is Matt-ruled.** → **Ask for one key at the G-IMG checkpoint and default to `1` if he does not care.** The potion's binding is the only thing standing between a ruled divergence and a buildable one.

**OQ-3 · DIV-13 contradicts the literal wording of Matt's own F6 (*"waves 150–160"*).** → **Surface it as a wording clarification, not a re-ruling** — *"you'll start at 151 from the simulation's own save point; 150 is available as a warm-up that we don't count."* His intent (*exactly the referent's window*) is satisfied by the ruling; only the sentence moves.

**OQ-4 · ND-04's correction is the second time a census module-default reading reached Matt as fact.** → **Adopt a standing rule for the handoff page: every claim about the oracle's configuration cites a `V0-*` row id or it does not ship.** Both errors were caught by V0 within one wave; a citation requirement makes the catch structural instead of lucky.

**OQ-5 · `u = 0.285` is a choice that will read to a player as a measurement.** → **Print `u` and its operative window `[0.246, 0.324]` on the how-to-play page, not only beside a metre readout.** The register calls it `PRESENTATION-CHOICE-NOT-MODEL-TRUTH`; the person most likely to mistake it for truth is the one holding the mouse.

---

*Filed 2026-09-20 by gandalf (named sub-agent, `SPEC-AUTHOR`), Wave 1, Run KC2-PLAY. **v0 not edited; superseded readings named in place at § A** — including my own ND-04 correction, corrected. **Law 3 held; GL-12 held; K-7 held.** No production code, no dispatch, no push.*
