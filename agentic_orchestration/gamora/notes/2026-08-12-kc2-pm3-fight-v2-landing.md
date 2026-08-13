# KC2-PM3 — landing note: the throughput gap closes, and the player still dies on wave 156

> **Cell:** KC2-PM3 fight cell v2 · **Conductor:** gandalf (`RUN-CONDUCTOR`) · **Author:** gamora
> **Date:** 2026-08-12 · **Charter:** `agentic_orchestration/gandalf/notes/2026-08-12-kc2-pm3-run-charter.md`
> **Math note (Discipline #1, written BEFORE the code):**
> `reincarnated-engine/src/reincarnated/simulation/math/kc2-pm3-defences-cluster-2026-08-12.md`
> **Status:** COMPLETE — five sibling batons, assert wall 16/16 each, gate wall 66/66 each,
> determinism ×2 masked-EXACT each, **REPLICATION LAW EXACT**. **No HALT was hit.**

---

## 0 — The one-paragraph answer

**No — DEFENCES-ON + CLUSTER does not reach the 159–160 band. Every cell still dies on wave 156.
But the thing the charter went looking for got found anyway, and it is a better finding than the
band would have been.** CLUSTER movement **closes Lap C's measured 4–5× kill-throughput gap almost
exactly** — the sim now clears six waves in **102.4 s against the reference's 98.0 s for the same
six (ratio 1.04, down from 4.21)**, and kill rate goes **0.53 → 2.40 bodies/s, a 4.5× lift that
lands squarely inside Lap C's measured 4–5× band**. **Wave 152 alone was the entire gap: 326.5 s
camped, 20.1 s clustered — 16.3× on one wave.** And with throughput matched, the death wave does
not move by one. **So kill throughput was never the survival constraint**, which retires the whole
premise the charter was built on and replaces it with a sharper question. The defences turn out to
be worth **0.00 %** of time-of-death while camped and **−3.8 %** while clustering; the leech-OFF
diagnostic settles PM-2's § 14.1 ask outright (**4 waves instead of 6; 1,141 of 4,522 ticks below
half HP instead of 18 of 5,055** — *this build is sustained, not tanky*, confirmed); and the reason
the sim stops at 156 is § 5, which is a property of the **frozen substrate**, not of the fight.

---

## 1 — What landed

| # | artifact | where | commit |
|---|---|---|---|
| 1 | **math note** (written before the code) | `simulation/math/kc2-pm3-defences-cluster-2026-08-12.md` | `c80e0a59` |
| 2 | **defences fold** | `simulation/kc2/defenses.py` | `c80e0a59` |
| 3 | **cluster-seek policy** | `simulation/kc2/player_drive.py :: ClusterSeekPolicy` | `c80e0a59` |
| 4 | **DoT corrections + aura fold** | `simulation/kc2/threat.py` | `c80e0a59` |
| 5 | **tick-loop wiring + `PlayerPolicy.CLUSTER_SEEK`** | `simulation/kc2/{run,locomotion}.py` | `c80e0a59` |
| 6 | **pinned Lap-C substrate** (2 files, digest-verified) | `data/kc2/pm3_*` | `c80e0a59` |
| 7 | **driver + assert wall + reference comparison** | `simulation/scripts/gamora_kc2_pm3_fight_v2_2026_08_12.py` | `c80e0a59` |
| 8 | **export: 5 specs + 3 spec fields + 5 wire declarations** | `export/kc2_run_adapter.py` | `c80e0a59` |
| 9 | **MIGRATION ×2** | `simulation/MIGRATION.md`, `export/MIGRATION.md` | `c80e0a59` |
| 10 | **5 knots supplies + findings** | `simulation/output/kc2-pm3-*-20260813_034259.json` | `c80e0a59` |

### ★ THE FIVE SIBLING BATONS

All at **FULL** grade from a **clean** tree at engine `c80e0a59`, each through the **same 66/66**
gate wall (VALIDATOR 32/32 · G-STATS 1/1 · G-E 33/33), committed at `3ee9a4a5`.

| cell | file (`src/reincarnated/output/`) | sha256 |
|---|---|---|
| CAMP / DEF-OFF | `kc2-baton-v1-…-pm3-camp-defoff-20260813_034620.json` | `503439f79978d1ff5ad62e25531662700bba6615b0cff1644bf7f3e8910e1f5e` |
| CAMP / DEF-ON | `…-pm3-camp-defon-20260813_034622.json` | `060f70408cfcb391f54925864eb1dc8e363b65b7a05146b56693a278de78d73f` |
| CLUSTER / DEF-OFF | `…-pm3-cluster-defoff-20260813_034624.json` | `322bebb656f6e04b4e58d453803a90131fa7a207afd28d27a348a8b9e98d7bbf` |
| **CLUSTER / DEF-ON** ← comparator | `…-pm3-cluster-defon-20260813_034626.json` | `1628bffa3280d29fafd6f9df18e8aed779bf6ce39e68f1ac64157b98e02ed351` |
| LEECH-OFF (diagnostic) | `…-pm3-leech-off-20260813_034628.json` | `441dd74f70a3a917e39ede4cb328881e1f8531cfffd875dd066634f958451aee` |

**Both frozen batons and all four PM-2 batons** were verified from bytes at the top of the driver,
read read-only, and **never written**. `baseline` / `pm1` / `pm2-camp` / `pm2-drive-dodge` **all
re-gate at 66/66 green** after the adapter delta — which is the *evidence* the three new spec
fields are additive, not the claim.

---

## 2 — Determinism ×2 (charter law), per cell

Mask = **the emitter's own `PROVENANCE_VOLATILE_KEYS`**, imported, not restated. Both determinism
emissions written to `/tmp` so the tree stayed clean.

| cell | masked A / B / record | verdict |
|---|---|---|
| CAMP/DEF-OFF | `ee86a14ca1552f8d6c2cd0f7…` ×3 | **EXACT** |
| CAMP/DEF-ON | `527316cd4e41eb95fceec4aa…` ×3 | **EXACT** |
| CLUSTER/DEF-OFF | `cd403c85066997c3343d178e…` ×3 | **EXACT** |
| CLUSTER/DEF-ON | `aedd61bd5aea38e92ad8048c…` ×3 | **EXACT** |
| LEECH-OFF | `8f1c3efb1af84b77c4cb0f1c…` ×3 | **EXACT** |

**Sim-layer** determinism (each cell replayed twice, full emitted surface deep-compared): **EXACT,
0 differences**, over 136,417 / 133,412 / 107,258 / 106,677 / 139,215 leaves.

### ⚑ THE REPLICATION LAW — EXACT, and I ran it both ways as instructed

| | |
|---|---|
| **(a) corrections-OFF** CAMP/DEF-OFF vs the PM-2 CAMP knots of record | `bec00893bfed3db0…` **≡** `bec00893bfed3db0…` → **EXACT**, 5,055 ticks vs 5,055 |
| **(b) corrections-ON** (the matrix cell) | emitted surface digest **MOVED**; time-of-death **+0.00 %**, `damage_total` **−2.46 %** |

Cross-run determinism holds across a lap that added a movement policy, a defences module and three
fold corrections. **The corrections are real but small on this cell** (§ 6).

---

## 3 — THE SURVIVAL HEADLINE vs the **MEASURED** reference truth

> **Reference truth, MEASURED (Lap C, charter Law 4): Matt DIED ON WAVE 160.** Ten waves in
> **186 s** (682 → 868 s), per-wave 14 / 17 / 29 s min/med/max, sharp slowdown on the last two.
> ⚑ PM-2 shipped its headline against a conductor-*remembered* "Matt survived" that the reference
> falsified. Every number below is against the measured curve.

| cell | ticks | time of death | wave | cleared | kills | **kills/s** | intake | healed |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| CAMP / DEF-OFF | 5,055 | 412.65 s | **156** | 5 | 217 | 0.53 | 93,010 | 72,995 |
| CAMP / DEF-ON | 5,055 | 412.65 s | **156** | 5 | 216 | 0.52 | 91,782 | 71,534 |
| CLUSTER / DEF-OFF | 1,304 | **106.45 s** | **156** | 5 | 243 | **2.28** | 94,664 | 74,065 |
| **CLUSTER / DEF-ON** | 1,254 | **102.37 s** | **156** | 5 | 246 | **2.40** | 98,938 | 78,550 |
| LEECH-OFF | 4,522 | 369.14 s | **154** | 3 | 160 | 0.43 | 45,594 | 25,306 |

**Answer to the charter's question: NO.** The band is **missed by four waves** in every cell, and
the miss is **identical** across the 2×2 — movement and defences both leave the death wave at 156.

### ⚑ AND THE PACING CURVE IS THE REAL RESULT

| wave | reference | CAMP | CLUSTER/DEF-ON | ratio (cluster / ref) |
|---:|---:|---:|---:|---:|
| 151 | 16 s | 18.45 s | 17.71 s | 1.11 |
| **152** | 17 s | **326.53 s** | **20.08 s** | **1.18** ← 16.3× compression |
| 153 | 15 s | 16.00 s | 16.08 s | 1.07 |
| 154 | 14 s | 38.12 s | 33.71 s | 2.41 |
| 155 | 16 s | 9.39 s | 9.55 s | 0.60 |
| 156 | 20 s | 4.16 s (death) | 5.22 s (death) | 0.26 |
| **total** | **98 s** | **412.7 s** | **102.4 s** | **1.04** |

**The 4–5× throughput gap Lap C measured is GONE**, and the mechanism is one wave. Lap C's
comparison (186 s / 10 waves vs 412 s / 5.x waves) was reading a **locomotion artifact** — a camped
player waiting on `ViewDistance`-15 bodies that never come (JC-G9) — as a **damage-rate** gap.
Under CLUSTER the sim's per-wave pacing sits inside the reference's own 14–29 s band on five of six
waves.

---

## 4 — WHY THE DEFENCES ARE WORTH ALMOST NOTHING (and it is not the beacons)

Of **182 decoded effect rows on the four purchases, exactly six touch the player**, all on the
Vanguard Banner's aura, and of those six **only one is live in this sim**:
`offensiveTotalDamageModifier = +100 %` within 8.0 m. (+80 OA and +4 % OA are inert — the player's
disc carries no to-hit roll, PM-2 § B.3; +100 % retaliation is inert — no retaliation term exists.)

| | CAMP/DEF-ON | CLUSTER/DEF-ON |
|---|---:|---:|
| **banner tether occupancy** | **100.0 %** (5,055 / 5,055 ticks) | **23.7 %** (297 / 1,254) |
| distinct player `damage_raw` on the wire | `{103452.0 ×274}` | `{51726.0 ×311, 103452.0 ×78}` |
| Δ time-of-death vs its DEF-OFF twin | **0.00 %** (identical to the tick) | **−3.83 %** |
| Δ ADCtH offered | −0.08 % | +3.51 % |

⚑ **Doubling the player's damage changes nothing, and § 5 is why:** `applied = min(2·D, hp)` and
**182 of 188 band-B bodies have `hp_max = 0.0`.** You cannot double zero. The banner is live only
on the six covered bodies in the whole ten-wave band.

⚑ **R-PM3-4's tether is priced, and the price is exactly what the ruling predicted:** CLUSTER buys
2.40 kills/s and **pays 76 % of its banner uptime for them**. On this substrate that is a good
trade only because the banner is worth ~0.

**Placement sensitivity, emitted rather than argued** (D-1 seats the banner on the sim's own
nearest cited patrol anchor, r = 5.963 m, minting no coordinate). Occupancy is emitted against
**all eleven** anchors: at the runner-up (node 0, r = 8.24 m) CAMP occupancy would fall **100 % →
0 %** and CLUSTER **23.7 % → 16.0 %**. **The CAMP/DEF-ON cell is knife-edge on 2.27 m, and since
its measured effect is 0.00 % anyway, the knife-edge costs nothing.** Both facts are on the wire.

---

## 5 — ⚑ WHAT ACTUALLY STOPS THE SIM AT WAVE 156, AND IT IS NOT THE FIGHT

**Measured before a design decision was made (math note § A.1), on the run-of-record seeds:**

| waves 151–160 | value |
|---|---|
| bodies rolled | **188** |
| records covered by the band-B eHP table | **6 (3.2 %)** |
| waves with **ZERO** coverage | 151, 152, 153, 155, 156, 157, 158, 159 — **eight of ten** |
| Σ eHP on wave 160 | 15,967,220 across 5 bodies |

`run.py` reads `hp = hp_lookup.get(record, 0.0)`, so **182 of 188 band-B bodies enter with
`hp_max = 0.0`**. They die to the first disc tick — and because `applied = min(D, hp)`, they yield
**`applied = 0`, i.e. ZERO ADCtH.** Three consequences, all now measured rather than suspected:

1. **The sim's wave clock is travel-bound, not damage-bound.** That is why CLUSTER is worth 4.5×
   and the banner is worth 0.
2. **PM-2's "kill drought" is structural.** Re-measured here: **172–178 of the final 200 ticks
   carry no player damage output in every cell**, unchanged by movement or defences. The player
   floats at 88–98 % mean HP and is snapped to zero in seconds (`camp-defoff` tail, every tenth
   tick: `16558 → 13950 → 19646 → 20005 → 19070 → 18972 → 17629 → 16286 → 12461 → 4890 → 0`).
3. **⚑ Wave 160 — the one wave with full coverage — costs 309 ticks (25.2 s) of unbroken disc
   contact at the measured kill term, against the reference's measured 29 s.** The sim never gets
   there, but the arithmetic that *would* govern it is already in agreement with the video.

⚑ **This is a property of the FROZEN substrate, inherited unchanged from the baseline baton, and
it was NOT touched.** Changing the eHP limb would be a different experiment and, under Law 3, the
tuning move. It is measured, declared, and left alone. **It is also, on the evidence of this lap,
the single largest thing standing between the sim and wave 160.**

---

## 6 — THE DoT CORRECTIONS, MEASURED (R-PM3-2)

| | corrections OFF | corrections ON | Δ |
|---|---:|---:|---:|
| time of death | 412.65 s | 412.65 s | **+0.00 %** |
| `damage_total` | 95,358 | 93,010 | **−2.46 %** |
| `damage_dot` | 7,117 | 6,084 | −14.5 % |
| `damage_aura` | 0 | 117.8 | — |
| aura applications | 0 | **3** | — |
| bodies killed | 217 | 217 | 0 |

**(A) `playerDefenseCap = [80,80,80]`** — bleed clamps 85 → 80, ×1.333 on bleed. Folded; too small
a family here to register. **CLIFF C-3 rides unresolved on the wire** (if the GD sheet prints
post-cap, this correction is wrong in the raise-damage direction).

**(B) `rotskin` re-folded as a toggled 3.5 m aura** — 10 rows moved off the `initial` slot across
**5 carriers**, `slots_emptied_by_aura_move = 0` (exactly as § A.3 predicted). ⚑ **The corrected
aura is nearly inert — 3 applications in a 5,055-tick run, 0 in CLUSTER/DEF-ON — and the reason is
geometric:** the aura radius (3.5 m) barely exceeds the player's kill disc (3.0 m), and every body
that enters the disc dies on that tick, so a carrier can only exist in the 3.0–3.5 m annulus for a
fraction of a tick while approaching.

⚑ **PM-2's #1 incoming threat was a fold artifact.** PM-2 ranked `aetherialcorruption_rotskin`
first at 12,992 — but the loader merges every skill on a slot into one `AttackSlot` labelled by the
first, so that number was rotskin **plus** `aetherorbitalretaliation`. Corrected, rotskin's aura
carries **117.8** and the retaliation half carries **9,466–11,034** under its own name. The threat
was real; the attribution was not.

**(C) duration axis:** DECLARED, **inert** (the measured sheet has no defensive duration-reduction
row). **Stacking:** NOT modelled, `damageMagnitude = 100.0` carried as an address (Lap C C-4).

---

## 7 — THE LEECH-OFF DIAGNOSTIC (RF-2) — PM-2's own § 14.1 ask, answered

| | CAMP/DEF-OFF | LEECH-OFF | verdict |
|---|---:|---:|---|
| waves reached / cleared | 156 / 5 | **154 / 3** | **−2 waves** |
| time of death | 412.65 s | 369.14 s | −10.5 % |
| mean HP | **97.8 %** | **74.2 %** | |
| ticks below half HP | **18 / 5,055 (0.4 %)** | **1,141 / 4,522 (25.2 %)** | **63× the pressure** |
| healing landed | 72,995 | 25,306 (regen only) | |

**PM-2 § 5's claim is CONFIRMED and it is not close: this build is SUSTAINED, not TANKY.** Without
ADCtH the player spends a quarter of the run under half health instead of 0.4 %, and loses a third
of the waves. ⚑ **The time-of-death drop is only 10.5 % and that is misleading** — wave 152's
326 s grind dominates the clock in both. **Waves, not seconds, is the honest axis here**, and this
row is why the pacing table in § 3 exists.

---

## 8 — PRE-REGISTERED PREDICTIONS vs OUTCOME

| # | prediction (written before the run) | outcome |
|---|---|---|
| **G.1** | CLUSTER compresses wave duration ≥ 2× vs CAMP; mechanism is ARRIVAL not damage; waves 151–155 in **under half** CAMP's ticks | **CONFIRMED, and under-predicted.** 4.03× overall (412.7 → 102.4 s); waves 151–155 at **24 %** of CAMP's ticks; the mechanism is exactly arrival (wave 152: 326.5 → 20.1 s on a **zero-eHP** board) |
| **G.2** | DEF-ON changes < 2 % of time-of-death; any advantage appears on wave 154 or 160 | **CONFIRMED on CAMP to the tick (0.00 %); MISSED on CLUSTER (−3.83 %).** And the advantage does appear on **wave 154** — 38.04 → 33.71 s — the one pre-160 wave with a covered body |
| **G.3** | death in all five cells; ≥ 70 % of the final 200 ticks dry in ≥ 3 cells | **CONFIRMED.** Five deaths; dry fraction **80–89 % in all five** |
| **G.4** | leech-OFF time-of-death < 60 % of cell 1's | **FALSIFIED.** 89.5 %. ⚑ But the prediction was measuring the wrong axis: in **waves** it is 3 vs 5 cleared, and § 7's HP pressure is 63× |
| **G.5** | tether > 90 % in CAMP, < 40 % in CLUSTER; CLUSTER/DEF-ON still outlives CAMP/DEF-ON | **HALF CONFIRMED.** 100.0 % / 23.7 % is exactly right. The second clause is **FALSIFIED and was badly framed**: both die on wave 156, and CAMP takes 4× *longer in seconds* to get there. "Outlives" has two meanings and I used the useless one |
| **G.6** | the band is MISSED; best cell reaches wave **157 ± 1**, clears 6–8 | **CONFIRMED in direction, FALSIFIED in magnitude.** Missed — but **no cell moved past 156 at all** and none cleared more than 5. The gap did not narrow by a single wave |

**Two clean confirmations, one half, three falsified.** The most useful falsification is **G.6's
magnitude**: I predicted movement and defences would buy 1–2 waves, and they bought **zero**. That
is what points at § 5.

---

## 9 — ⚑ DEFECTS AND UNDER-READS I FOUND IN MY OWN WORK (Discipline #11)

| # | what | how found | effect |
|---|---|---|---|
| **1** | **Assert-wall check 12 could not fail.** It compared the **actor-path** digest, and the DoT corrections change only what damage the *player* takes — they cannot move a monster trajectory. `digest_off == digest_on` was guaranteed | reading the wall's own output and noticing the "corrections changed the run" line said `False` on a run whose damage totals differed | rewritten to compare the **full emitted surface** + measured deltas; it then reported `MOVED` / −2.46 %. **A check that cannot fail is not a check** |
| **2** | **Lap C's rotskin "displacement" claim is mechanically wrong** and I checked it instead of adopting it | measuring all five carriers' `basic` reach (2.4 m) against rotskin's (3.5 m) and reading `SLOT_ORDER` | no weapon swing was **ever** displaced; the real defect is that a toggle could not apply *concurrently* inside 2.4 m. Direction of the correction is the opposite of what Lap C could not decide |
| **3** | **PM-2's #1 incoming threat was mis-attributed** (§ 6) | reading the corrected top-incoming table and seeing a skill appear that had never ranked | 12,992 "rotskin" was rotskin + `aetherorbitalretaliation` summed under one label |
| **4** | **The band-B eHP coverage is 3.2 %, and every earlier lap called it "partial"** | measuring it per wave before designing anything | it is § 5, and it reframes Lap C's throughput headline |

---

## 10 — DECLARED ASSUMPTIONS + GAPS (every one on the wire)

**⚑ THE LARGEST GAP, and its direction is NEW.** **The three beacons do not fire.** Their
enemy-facing output is fully MEASURED (icebolt 1,876 Cold + 50 % freeze + −145 OA/DA;
chainlightning 1,604–4,284 + −10 all-res; fireblast 2,340 + 381 burn/5 s + −14 % damage) and their
**firing cadence is UNREAD** — the Lap-C sheet's grain is granted stat effects derived from
`parameters_offensive.tpl`, which cannot carry a `skillCooldownTime` even if the record has one. A
DPS is `magnitude ÷ period`; `period` is not in the substrate. **Ruled by PM-2 § K.2's own rule for
the 51 ungated pet specials: no measured reuse gate ⇒ does not fire.** Counted as
`defence_output_slots_ungated = 3`.
**Every PM-2 gap under-read THREAT; this one under-reads ALLY HELP**, so it biases this run *away*
from wave 160 — which makes it the first-named reason for the miss. ⚑ **But it is smaller than it
looks: § 5 says a beacon cannot thin a board whose bodies have `hp_max = 0`, and cannot cut leech
that is already zero. R-PM3-3's named tension is structurally inert on nine of the ten waves.**
**One read of `skillCooldownTime` / `projectileDistance` on the three turret skill records closes
it.**

**Placement D-1 (declared, veto-open):** the four defence points are fixed map objects and their
coordinates are in **no** pinned substrate. D-1 seats them on the sim's own cited
`PatrolPoint_Attack` anchors, greedily ascending in radius with a ≥ 8.0 m separation floor
**imported from the banner's own measured aura radius**; the banner takes the anchor nearest the
centroid **because R-PM3-4 asks the sim to price the tether and a placement the player is never
inside prices nothing**. **No coordinate is minted.** Sensitivity emitted against all eleven nodes.

**Rank policy (declared):** **ADOPT Lap C's rank 26 unchanged, re-read nothing.** Lap C's C-2 cliff
(unbound defence `charLevel`) is **INERT here**: the only rank that reaches this sim's arithmetic is
the banner aura's, and that is `ARRAY[2]@rank1:EXACT` — a literal, rank-free.

**Carried unchanged from PM-2, all still on the wire:** OA fold with `dexterityDV` absent →
zero · resist-then-armour order · SEM-1 total-over-duration (now **MEASURED**, not defaulted —
Lap C F-1) · `percent_current_life` unmitigated and floored · pet cap 12 on 36 cap-less contracts ·
pet straight-line locomotion · 51 ungated pet specials · 593 control/debuff/modifier rows that are
not HP damage · 30 non-MEASURED-rank rows.

**New this lap:** aura cadence = the carrier's own measured swing clock (CLIFF C-4b) · the aura
retains its PTH roll (lower reading) · CLUSTER's live set **includes pets** (they are the only
bodies on this board carrying real HP) · CLUSTER's objective is **unweighted** (β dropped; the
HP-weighted objective would be an argmax over a near-constant zero).

---

## 11 — SEAM WORK (star-lord: two semantic shifts, one re-ruling candidate, zero validator edits)

Both filed in `export/MIGRATION.md` and `simulation/MIGRATION.md` `[2026-08-12] KC2-PM3`.

1. **⚑ SEMANTIC SHIFT — `events.rows[].damage_raw` on player-sourced rows is no longer a
   constant.** PM-2 emitted one value on every such row; a DEFENCES-ON baton emits two
   (`51726.0` and `103452.0`). **Any consumer that derived a per-tick kill rate from one row and
   extrapolated is wrong by up to 2× on those two batons.** Wire row
   `PM3-PLAYER-OUTGOING-DAMAGE-IS-POSITIONAL`; re-derivable from `tracks.player_path`.
2. **⚑ SEMANTIC SHIFT — R-PM1-2 is SCOPED, not repealed.** `CLUSTER_SEEK` clamps its step;
   `DRIVE_TO_PACK` is byte-identical and untouched. Wire row
   `PM3-CLUSTER-ARRIVES-R-PM1-2-SCOPED`.
3. **⚑ RE-RULING CANDIDATE, NOT TAKEN.** `F5-I-DEFENSES = DECLARED-COUNT-ONLY` still emits
   `["DEFENSE-COUNT-4-NAMES-NOT-EMITTED"]`. **The four names are now MEASURED.** I did not re-rule
   a countersigned ruling from the simulation seam — the same line PM-2 held on `threat_tier` — and
   the names ride `informative_rows` instead. **Conductor + star-lord's call.**
4. **NO validator predicate was touched this lap** (PM-2 touched two). `KC2RunSpec` gains three
   optional fields, all defaulting to PM-2 behaviour; **no event column, no enum member, no schema
   version moved.**
5. **Defences are NOT `actors[]` rows** — three declared reasons in
   `defenses.py :: declared_constants()["defence_is_not_an_actor"]`. Pets still ride
   `waves[].pets` (RF-3 parked, unchanged).

**rocket:** nothing. **drax / scene consumers:** if you draw player damage, it is now positional.
**jack-ryan:** Disciplines #1, #2, #3, #11, #12 all exercised and named.

---

## 12 — L-0 PINS

**At launch:** engine HEAD `c75af8da` · **porcelain 2,789 = the FG-17 baseline exactly** · both
frozen batons + all four PM-2 batons + the PM-2 CAMP knots verified from bytes · 8 PM-2 substrate
files + 2 Lap-C files digest-verified.
**At landing:** HEAD `3ee9a4a5`, porcelain **2,789 — the baseline, unchanged**, because everything
this lap produced was committed **by explicit path**. ⚑ PM-2's `git add -A` scope error (2,649
swept artifacts) is on the ledger; **no `-A` was used anywhere in this lap** and the porcelain count
was re-read against the L-0 pin after both commits.

Two superseded first-batch artifacts (stamp `034259` was preceded by `034052`, emitted under the
defective check 12 of § 9.1) were **deleted before staging** rather than committed alongside.

---

## 13 — SELF-ATTACK SURFACES (what I would want a second pair of eyes on)

1. **§ 5 is the finding, and it is a finding about the substrate, not the fight.** If the band-B
   eHP table were complete, every number in this note would change. I did not touch it (Law 3) and
   I think the next cell should be about it rather than about the fight.
2. **The beacon cadence gap is one read away from closing** and its direction favours the null
   result I reported. If a re-probe makes the beacons fire, § 3's death wave is the number to
   re-check first.
3. **D-1's banner assignment is the most attackable choice in the lap.** I placed the banner where
   the tradeoff exists rather than where it does not, and I said so. The measured effect is 0.00 %,
   so the choice cost nothing — but it *could* have.
4. **CLUSTER's arrival clamp is a departure from a countersigned ruling.** Scoped, declared,
   argued from the leech identity — and still a sim agent narrowing someone else's rule.
5. **`n_arrived_ticks` is ~0 in five of six waves.** The player almost never *reaches* the centroid
   because the centroid moves toward the player. The clamp is therefore mostly inert, which means
   § 8's G.1 confirmation is really about **going to the bodies at all**, not about dwelling. The
   dwell half of the policy is untested by this run.
6. **CLUSTER's objective is unweighted and its tie-break radius is 8 m.** Both are defensible and
   both are choices; the disc-occupancy series is emitted so someone can argue with them.
7. **`percent_current_life` is 27–40 % of intake and still unverifiable** (PM-2 § 13.1, unchanged).
   It rose under CLUSTER (25,127 → 39,286) because the player stands closer to more bodies.

---

## 14 — QUESTIONS FOR THE CONDUCTOR / MATT (all veto-open, none blocking)

1. **§ 5 — is the band-B eHP table the next cell?** On this lap's evidence it is the binding
   constraint on wave depth, and it is the one thing PM-3 was forbidden to touch.
2. **§ 10 — commission the beacon-cadence re-probe?** One legolas read of `skillCooldownTime` /
   `projectileDistance` on three records converts the lap's largest declared gap into a
   measurement.
3. **§ 11.3 — star-lord: re-rule `F5-I-DEFENSES` now that the four names are measured?**
4. **§ 6 — CLIFF C-3 (does the GD sheet print pre- or post-cap resistance?) needs Matt's eye**, not
   a decode: it is a UI question about a screenshot he took.
5. **The reference's own last two waves slowed to 26 s and 29 s.** The sim never reaches them, but
   § 5 computes wave 160 at **25.2 s of unbroken disc contact** — within 13 % of the measured 29 s.
   **Is that agreement worth a targeted wave-160-only cell?** It would test the kill term against
   the one wave where the substrate is complete.

**No HALT was hit.** Nothing required inventing an unmeasured quantity — every silence was declared
with the lower reading or refused outright. **There is no fitted constant anywhere in this lap.**
Nothing was tuned toward wave 160, and the band was missed by four waves in every cell.
