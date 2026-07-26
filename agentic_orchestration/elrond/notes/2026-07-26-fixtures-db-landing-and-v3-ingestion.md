# `fixtures.db` landed · rounds 1–2 backfilled · round 3 certified

**Agent:** elrond (data steward) · **Commissioner:** gandalf (GD program, gap 5)
**Date:** 2026-07-26 · **Store:** `agentic_orchestration/research/curated/fixtures.db`, schema `fixtures-v0.1`
**Ledger:** `research/curated/MIGRATION-fixtures.md`
**Governing:** `elrond/notes/2026-07-25-l0-fixture-schema-draft.md` · `gandalf/notes/2026-07-25-l0-fixture-schema-review.md` (rulings O-1…O-10)

---

## 1. What is in the store

| Table | Rows | Note |
|---|---:|---|
| `fixture_session` | 3 | rounds 1, 2, 3 |
| `capture` | 28 | 10 (r1+r2) + 18 (r3) |
| `fixture_character` | 4 | r1 ×1, r2 ×2 (the level-up), r3 ×1 **full-sheet** |
| `character_stat` | 175 | exhaustive VAUGHT sheet — the G-5 key's input document |
| `fixture_set` | 4 | r1 baseline, r2 set1/set2, r3 set1 |
| `fixture_set_constraint` | 34 | incl. the O-9 expired no-CC row on every fought set |
| `fixture_trial` | 7 | 1 baseline + 3 (r2) + 3 (r3) |
| `trial_measurement` | 179 | every number a reading, with per-field provenance |
| `trial_trace` | 17 | 10 session-scoped, 7 trial-scoped (all r3) |
| `measure_dict` | 17 | 3 `oracle-only` |

Rebuild is three commands (MIGRATION doc § top). The `.db` is gitignored; the scripts are the record.

---

## 2. Certification verdict — per trial

`v_fixture_bank_certified` predicate: identity attested by spawn command or nameplate · monster's
own level attested · character snapshot is `full-sheet` · no mid-set level-up · not a baseline row.

| Trial | Identity | Monster lvl | Char sheet | Level-up | **Verdict** |
|---|---|---|---|---|---|
| `L0-gd-s2-set1/t1` | `assumed-unverified` | — | level-only | — | **FAIL** |
| `L0-gd-s2-set2/t1` | `assumed-unverified` | — | level+HP only | — | **FAIL** |
| `L0-gd-s2-set2/t2` | `assumed-unverified` | — | level+HP only | — | **FAIL** |
| `L0-gd-s3-set1/t1` | nameplate "Walking Dead" | 6 (nameplate) | full-sheet | none | **CERTIFIED** |
| `L0-gd-s3-set1/t2` | nameplate "Walking Dead" | 6 (nameplate) | full-sheet | none | **CERTIFIED** (contaminated upstream) |
| `L0-gd-s3-set1/t3` | nameplate "Walking Dead" | 6 (nameplate) | full-sheet | none | **CERTIFIED** |

The round-2 failures are O-8 working as ruled, not a defect. Round 3 certifies because the v3 sheet
asked for the two things that were missing: a nameplate and a character sheet.

`monster_record` is still NULL even on the certified rows. Nothing in `corpus.db` maps the display
name "Walking Dead" to a `.dbr` path, so the join to the `.arz` remains a pending gap. The
certification predicate does not require it — deliberately (O-8) — because level plus name is enough
to *identify the fixture*, while the record path is what you need to *predict* it.

---

## 3. Q47 — evaluated against the certified view only

Spread over the three certified trials (`v_trial_delta` ⋈ `v_fixture_bank_certified`):

| Measure | values | mean | range | range/mean | instrument uncertainty |
|---|---|---:|---:|---:|---|
| `kills` Δ | 1, 1, 1 | 1.00 | 0 | **0.0 %** | exact (counter) |
| `skill_use_count` [defaultweaponattack] Δ | **2, 2, 3** | 2.33 | 1 | **42.9 %** | exact (counter) |
| `play_time` Δ (capture interval) | 5, 5, 4 s | 4.67 | 1 | **21.4 %** | exact |
| `fight_seconds` (hand) | 5, 5, 4 s | 4.67 | 1 | 21.4 % | **±2 s each** (addendum) |
| `life_healed` Δ (damage-taken proxy) | 0.00, 16.04, 0.95 | 5.66 | 16.04 | **283.2 %** | exact |
| `hp_cost_abs` (hand) | 0, 0, 13 | 4.33 | 13 | 300.0 % | globe glance |
| `dps_field` Δ | 22.88, 26.96, — | 24.47 | 4.08 | 16.7 % | oracle colour only (O-6) |

### Verdict: **PARTIAL FIRE.** Enough to strike one row of Q47's own table; not enough to rule it.

**What fires.** The `±5 % on time-to-kill, per fight` tier is **empirically unreachable at L0**, and
the reason is not instrument coarseness. The cleanest number in the entire bank — an integer counter,
zero read uncertainty, same monster type, same monster level, same character, same difficulty, same
area, three consecutive fights — is **2, 2, 3 basic attacks**. That is a 42.9 % spread on the
quantity the fixture is *most* controlled for. A discrete, small kill cost cannot support a ±5 %
per-fight bar no matter how good the capture rig gets. Buying a frame-accurate instrument to chase
±5 % per fight would be buying precision the phenomenon does not have.

**What does not fire.** Everything else. n = 3, one fixture set, one monster, one character, one
build. Choosing among *±15 % in aggregate* / *rank-ordering preserved* / *nothing obviously wrong*
is Matt's call and the bank cannot size it yet — the rank-ordering tier in particular is untestable
in principle until a **second build** exists to be ranked against the first. **Q47 stays open.**

**Corollary worth having before the ruling:** the panel `play_time` delta does **not** independently
corroborate Matt's stopwatch. Both instruments measure the same capture interval and both carry the
same ~1 s/screenshot overhead the addendum describes — which is exactly why they agree to the second
(5/5/4 both ways). Two instruments that agree because they share a bias are one instrument.

---

## 4. Anomalies, honestly

**A1 — "Aether Corruption". The biggest one.** The target frame reads three lines: `Walking Dead` /
level `6` / **`Aether Corruption`**. The first two are what certified the set. The third is
unexplained. If it denotes an affix, aura or corruption modifier on the creature, then these are
**not vanilla zombie statlines**, and any per-hit damage inference drawn against a vanilla `.dbr`
would be silently wrong — wrong in the specific way certification is supposed to prevent. The
certification predicate passes and the fixture may still be a variant. **One line on the next sheet
closes it: hover the monster and screenshot the full tooltip.**

**A2 — the player is not a melee character.** The equipment doll shows a two-handed firearm; the only
skill counter that moves is `defaultweaponattack`; `Chance to Block` is 0 % and the round-3 panel has
no `Shield block chance` line at all. Every round-3 TTK therefore includes projectile travel and
standoff distance. Banked as constraint `player-melee-only` = **violated** (new key). This does not
invalidate the fixtures — it renames what they measure.

**A3 — T1/T2 cost zero HP, and one of those zeroes is false.** Trial 1: `life_healed` Δ = 0.00 and
globe 282/282 — a genuine no-cost kill, both instruments agreeing. Trial 2: globe **also** 282/282
and Matt's note says HP cost 0, but `life_healed` accrued **+16.04** across the 5 s window. Both
readings stand (O-7) and they are not actually contradictory: the globe is a snapshot taken after
regeneration ran, `life_healed` integrates over the window. Read together they say trial 2 cost ~16
HP that was regenerated before the shutter. This is the strongest argument in the bank for keeping
the panel counters rather than trusting the globe alone — and it is a warning that "HP cost 0" from
a post-kill glance means "recovered by the time I looked", not "took no damage".

**A4 — fight-time uncertainty.** 5/5/4 s hand-noted, banked with `uncertainty_abs = 2.0` and a
`validity_note` citing `matt-addendum-timing-uncertainty.md`. Real engagement is plausibly 2–3 s;
the bias is systematic and **upward**. The observed 1 s spread is entirely inside the per-reading
uncertainty, so per-fight TTK variance is not measurable at L0 at all.

**A5 — ledger discontinuities.** Round 2: +1 kill, +2 attacks, +18.51 HP healed between T2-after and
T3-before. Round 3: +1 kill, +2 attacks between T1-after and T2-before. Both trials carry
`contaminated = 1`, `ledger-discontinuity`. Visible only because before(n+1) and after(n) are both
stored as readings.

**A6 — the panel mixes two clocks.** `play_time`, `kills`, `deaths`, potions and `max_level_achieved`
run **continuous** from round 2 into round 3 (8563 → 8735 s; 165 → 172 kills). `skill_use_count` and
`life_healed` **reset** (435 → 22; 2311.37 → 0.00). The panel is part save-cumulative and part
session-cumulative, and nothing on it says which is which. Cross-session deltas are valid for the
first group and meaningless for the second. Recorded in `fixture_session.notes`.

**A7 — the character sheet's own clock disagrees with the panel.** Sheet: `Elapsed Time 0:2:21`
(141 min), `Monsters Killed 162`. Panel during the trials: 145–149 min, 172–176 kills. Either the
sheet was shot before the trials or the two counters are differently defined. Recorded, not
reconciled. It does not affect the sheet's use as a character description: its `Health 282/282` and
`Level 6` match the trial globes and panels exactly.

**A8 — a coverage gap in the sheet.** The tab-III scroll jumps from `Energy Absorption` (end of S20)
to `Constitution Bonus` (start of S21). Any lines between were never captured.

---

## 5. Findings that are not anomalies

**F1 — `Pursue` is live-attested.** Census row 4 (`Pursue`, DATA-ATTESTED, 100 % of the bestiary,
IN-both) is observed live on the start frames of trials 1 and 3. Unlike round 2's `Fidget`, this
token **is** a census row and does confirm one.

**F2 — the overlay hands us the gap-9 mapping table for free.** With both console flags on, every
entity renders *two* lines: a controller-state line above an `[entityId] Action State: X` line. Round
2 could only see the channels separately, which is why the draft had to keep `trace_token` and
`controller_state` apart. Round 3 supplies live **(controller, action) pairs with an entity id
attached** — `(Pursue, Move)` ×3 and `(LongIdle, Fidget)` ×1 — from the game rather than from
inference. `LongIdle` is absent from the 40-state table and is banked unmapped; its entity is
screen-centred and is most likely the player, so it may not be a `ControllerMonster` observation at
all.

**F3 — round 2's `Moving` may have been a formatting artefact.** The on-screen overlay prints
**`Move`**, matching 40-state-table row 18 exactly, where round 2's console printed `Moving`. The
near-miss the draft flagged may be console formatting, not a distinct token.

**F4 — three distinct entity ids (68957 / 75289 / 77775)** prove three separate monsters, one per
trial — the cleanest evidence the bank has for the `single-monster` constraint.

---

## 6. Corrections filed against my own draft

- **C10.** Draft § 7.2 attributes a "2–3 s (close)" `AlertBeforePursue` beat to round 1. The round-1
  raw notes carry no such number — Matt wrote that he had too few instances to tell. Banked with
  `duration_s` NULL. Raw evidence governs.
- **O-6 seed correction.** Draft § 6.1 listed `dps_field` as `lane_availability = both`; gandalf
  ruled it out of the comparable set. Seeded `oracle-only`.
- **O-10's own lesson.** The round-1 panel read `Max. level achieved: 1` at a wide, lightly-upscaled
  crop and `2` at a tight 4× crop. Only the 4× reading is banked.

---

## 7. Recommended for `fixtures-v0.2` (not applied)

1. **`measure_dict.off_trial_semantics`.** `v_ledger_continuity` currently flags `life_healed` as
   DISCONTINUOUS between every trial pair — correctly, and uselessly, because regeneration legitimately
   accrues off-trial. The view needs to distinguish counters that *must not* advance between trials
   (`kills`, `skill_use_count`) from counters that *may* (`life_healed`). Today the analyst supplies
   that judgment; it belongs in the dictionary.
2. **A `monster_display_name → record_path` bridge**, once legolas can source GD's display-name table.
   That is the last link between a certified fixture and the `.arz` statline it is supposed to predict.
3. **`fixture_set.monster_affix` / `monster_variant`** — A1 is the reason.

---

**Signed:** elrond, 2026-07-26. Three trials certified; one nameplate line still unexplained. The
schema did the job it was built for twice today — it refused to certify round 2, and it kept two
disagreeing HP readings side by side long enough for the disagreement to turn out to be the finding.
