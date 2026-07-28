#!/usr/bin/env python3
"""M8 part 4 -- the fixture identity, the accountability contract, the declared
conditions, and the evidence grades (G-3 / KC1-2026-07-27 P-1).

Everything a consumer would otherwise have to REMEMBER from a prose document becomes
a row here, scoped to what it conditions. The three consumer views join them in, so a
figure cannot leave this store without the conditions that qualify it.
"""

import os
import sqlite3

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
DB = os.path.join(ROOT, "agentic_orchestration/research/curated/fixtures.db")

S = "GP-gd-2026-07-26-s1"
SEG = f"{S}/S1-gap5s-v1"
R1, R2, R3 = f"{S}/R1", f"{S}/R2", f"{S}/R3"
V = "gandalf/notes/2026-07-26-gd-playtest-v1-efficacy-verdict.md"
F = "galadriel/notes/2026-07-27-gd-playtest-v1-tb-intake-findings.md"
C = "gandalf/notes/2026-07-27-kit-cal-1-run-charter.md"
DATE = "2026-07-28"


def log(m):
    print(f"[m8d] {m}", flush=True)


FIXTURES = [
    # fixture_id, regime, kit_id, role, naming_status, ruling, grade, notes
    ("GD-R2-werewolf", R2, "gd-werewolf-kitcal-1", "primary", "matt-ratified", "R-KC1-1",
     "MEASURED",
     "THE fixture. 647 kills over 77 engagements, play_time 1134-6052, two-skill werewolf "
     "(claws + charge), potions 0/0, no devotion proc, levels ~5-11. Carries both halves of "
     "protocol sec 1: TTK shape AND intake distribution. The first measured external "
     "gameplay fixture the project has banked."),
    ("GD-R3-werewolf-poison", R3, "gd-werewolf-kitcal-1", "secondary",
     "elrond-provisional", "R-KC1-2", "MEASURED",
     "Secondary fixture with its own error bars AND a declared coverage hole "
     "(C-R3-COV-HOLE). Report-only as an accountability target per R-KC1-2. NAME NOT "
     "RATIFIED -- only GD-R2-werewolf was named at grill item 1."),
    ("GD-R1-pretransform", R1, "gd-werewolf-kitcal-1", "report-only",
     "elrond-provisional", "R-KC1-2", "MEASURED",
     "13 engagements is an anecdote, not a distribution (verdict sec 3). Report it; do not "
     "fit it. NAME NOT RATIFIED."),
]

TARGETS = [
    # fixture_id, target_key, tier, measure_key, stat_family, rationale, gate_ref
    ("GD-R2-werewolf", "ttk_shape", "primary", "engagement_seconds", "totals",
     "Engagement-level TTK shape -- one of the two sec-1 protocol quantities. The run "
     "delivers it; per-kill TTK it does not (C-ATTACKCOST-DEAD).",
     "bands ratified at HALT H-2 before the first G-5 comparison executes"),
    ("GD-R2-werewolf", "damage_intake_total", "primary", "intake_hp", "totals",
     "Damage-intake distribution per engagement. Heavily zero-inflated (median 17 HP "
     "against a 366-759 HP pool, mean 67.7). FIT THE TAIL, NOT THE MEAN.",
     "HALT H-2"),
    ("GD-R2-werewolf", "damage_intake_rate", "primary", "intake_hp_per_s", "rates",
     "Intake per COVERED second. Reported beside totals and never mixed with them.",
     "HALT H-2"),
    ("GD-R2-werewolf", "hazard_tail", "primary", "hp_drop_count_ge_10pc_ehp", "drops",
     "27 drops at or above 10% EHP carry 46.8% of R2 intake; the largest removed 72.4% of "
     "the pool in a single frame. R2 is the run's only dangerous regime. Tune against "
     "those 27; the other 305 are weather.", "HALT H-2"),
    ("GD-R2-werewolf", "kills_per_engagement", "provisional", "kills_per_engagement",
     "totals",
     "PROVISIONAL per Matt ruling R-KC1-2. The 3.3 -> 8.4 -> 11.9 progression confounds "
     "pack size, dash-chaining and AoE proficiency. Banding it would band a measurement "
     "artifact. NOT the fixture's headline stat.",
     "T-1: G-2b causal decomposition separates the three signatures; then H-1 grain ruling"),
    ("GD-R2-werewolf", "damage_per_kill", "report-only", "damage_per_kill_merged", "damage",
     "An overkill-inflated UPPER BOUND on monster EHP, not a monster health figure. "
     "Usable as a ceiling, never as a target.", None),
    ("GD-R2-werewolf", "per_kill_attack_cost", "report-only", None, None,
     "Considered and EXCLUDED. The named instrument is dead for 95% of the run and 39% of "
     "kill-increment samples are multi-kill. Not recoverable by reprocessing. "
     "See C-ATTACKCOST-DEAD.", "v2 recording with the sec-8 requirements met"),
    ("GD-R3-werewolf-poison", "ttk_shape", "report-only", "engagement_seconds", "totals",
     "R1/R3 report-only per R-KC1-2.", None),
    ("GD-R3-werewolf-poison", "damage_intake_total", "report-only", "intake_hp", "totals",
     "Report-only per R-KC1-2, AND conditioned on the readable remainder: 4 of 16 "
     "engagements (33 kills) at literally zero coverage. See C-R3-COV-HOLE.", None),
    ("GD-R1-pretransform", "ttk_shape", "report-only", "engagement_seconds", "totals",
     "13 engagements. Report, do not fit.", None),
    ("GD-R1-pretransform", "damage_intake_total", "report-only", "intake_hp", "totals",
     "13 engagements, median engagement takes nothing at all.", None),
]

INTAKE_KEYS = ("intake_hp,healed_hp,hp_drop_count,hp_drop_max,hp_drop_p50,hp_drop_size,"
               "hp_drop_pc_ehp,intake_pc_ehp,intake_hp_per_s,intake_pc_ehp_per_s,"
               "healed_hp_per_s,intake_per_kill,intake_per_kill_pc_ehp,hp_max_observed,"
               "hp_min_observed,hp_drop_count_ge_10pc_ehp,"
               "frac_intake_from_drops_ge_10pc_ehp,drop_events_per_covered_s")

CONDITIONS = [
    # id, scope_kind, scope_ref, kind, severity, headline, detail, measures, engs, kills,
    # cause, cause_grade, recoverable, remedy, evidence
    ("C-R3-COV-HOLE", "regime", R3, "coverage-hole", "high",
     "R3 intake travels with a DECLARED HOLE: 4 of 16 engagements at literally zero coverage.",
     "Engagements 90, 91, 92, 93 -- 33 kills -- returned no readable globe numeral at all. "
     "R3 frame coverage is 75.89% against R1's 99.95% and R2's 90.11%. Totals are computed "
     "over 9 of 16 engagements (129 of 190 kills); rates over 12 of 16. A calibration sweep "
     "over five brightness and four chroma thresholds plus a blue-channel variant recovers "
     "nothing: best case is an 8-row glyph band at IoU 0.25-0.47 against a 0.72 floor. "
     "The information is gone at the pixel layer.",
     INTAKE_KEYS, "90,91,92,93", 33,
     "The bright gold horizontal HUD band (the experience bar) crosses the health globe at "
     "exactly the screen rows the numerals occupy. When it blooms it saturates the upper "
     "rows of every glyph and the 12-row numeral band collapses to 6-8 rows.",
     "INFERRED", 0,
     "v2 recording: raise UI scale, move the readout, or read HP from a second surface. "
     "Costs nothing at record time; the difference between R3 at 76% and R3 at ~99%.",
     F + " sec 5; " + V + " addendum 2026-07-28"),
    ("C-R3-COV-NONRANDOM", "regime", R3, "confound", "high",
     "R3's coverage loss is NOT RANDOM -- it is correlated with the moments just after a kill.",
     "The gold band blooms after kills, so the FLASH refusal class (719 frames run-wide) "
     "clusters immediately post-kill. R3 loses 24% of its frames this way, R2 1.2%. Any R3 "
     "intake figure is conditioned on the readable remainder, and the remainder is "
     "systematically the quieter part of each engagement.",
     INTAKE_KEYS, None, None, "as C-R3-COV-HOLE", "INFERRED", 0,
     "as C-R3-COV-HOLE", F + " sec 5"),
    ("C-R2-COV-ENG39", "engagement", f"{SEG}/e039", "coverage-hole", "moderate",
     "One R2 engagement (eng_id 39) read at zero coverage.",
     "Same gold-band confound as C-R3-COV-HOLE, at 1.2% incidence in R2 rather than 24%. "
     "Excluded from R2 totals and rates.",
     INTAKE_KEYS, "39", None, "as C-R3-COV-HOLE", "INFERRED", 0, "as C-R3-COV-HOLE",
     F + " sec 5"),
    ("C-R2-TOTALS-INCLUSION", "regime", R2, "coverage-hole", "moderate",
     "R2 totals are computed over 62 of 77 engagements (479 of 647 kills).",
     "The >=0.80 frame-coverage gate excludes 15 engagements: a fragment is not a total. "
     "Rates use a different, wider inclusion (73 of 77, >=2 s of admissible pair-time) and "
     "the two families are never mixed. Filtering trial_measurement.coverage >= 0.80 "
     "reproduces the totals set exactly.",
     INTAKE_KEYS, None, 168, "coverage gate, by design", "MEASURED", 1,
     "v2 recording at R1-grade coverage", F + " sec 6"),
    ("C-R3-TOTALS-INCLUSION", "regime", R3, "coverage-hole", "high",
     "R3 totals are computed over 9 of 16 engagements (129 of 190 kills).",
     "Thin to begin with (16 engagements), thinner after the coverage gate. Every R3 "
     "distribution statistic rests on nine numbers.",
     INTAKE_KEYS, None, 61, "coverage gate + C-R3-COV-HOLE", "MEASURED", 0,
     "v2 recording", F + " sec 6"),
    ("C-R1-NOT-A-DISTRIBUTION", "regime", R1, "sample-size", "high",
     "R1 is an anecdote, not a distribution. 43 kills over 13 engagements.",
     "13 engagements describes the opening nineteen minutes of one run. Report it; do not "
     "fit it. R-KC1-2 grades it report-only.",
     "", None, 43, "run structure", "MEASURED", 0,
     "v2 recording with a longer stable opening build", V + " sec 3"),
    ("C-SEG-GRAIN-UNRULED", "session", S, "provisional-ruling", "high",
     "The engagement GRAIN is not yet ruled. Every engagement-grain figure is provisional on it.",
     "The gap>5 s cut is the most permissive defensible threshold, chosen because it is the "
     "only one that reaches the sec-1 target band. gap>8 s gives 75 engagements, gap>10 s "
     "gives 67. Charter HALT H-1 places the grain ruling with Matt, WITH the G-2b "
     "decomposition in hand, before any band is drafted. A re-cut lands as a new "
     "segmentation_run; these rows are not edited.",
     "engagement_seconds,kills_per_engagement," + INTAKE_KEYS, None, None,
     "the ruling has not been made yet", "MEASURED", 1,
     "HALT H-1: Matt rules the grain with G-2b evidence on the table",
     C + " sec 5; " + V + " sec 4"),
    ("C-ENG-COUNT-AT-FLOOR", "session", S, "sample-size", "moderate",
     "106 engagements sits AT the floor of the 100-250 target band, not inside it.",
     "Reached only at the most permissive defensible threshold; below the band at any "
     "conservative one. PASS on the criterion with no margin. v2 should target roughly "
     "double, which at this run's density is ~2 hours of COMBAT-WEIGHTED play rather than "
     "2 hours of general play.",
     "", None, None, "run length and density", "MEASURED", 0,
     "v2: roughly double the engagements", V + " sec 4, sec 8 item 2"),
    ("C-TTK-QUANTISATION", "session", S, "resolution-limit", "moderate",
     "Engagement TTK carries ~11% quantisation.",
     "A 4.5 s median engagement sampled at 0.5 s is nine samples. Usable, not tight. Every "
     "engagement_seconds row carries uncertainty_abs = 0.5 s.",
     "engagement_seconds", None, None, "0.5 s panel sampling rate", "MEASURED", 0,
     "v2 at a higher panel sampling rate", V + " sec 4"),
    ("C-KPE-PROVISIONAL", "fixture", "GD-R2-werewolf", "provisional-ruling", "high",
     "kills/engagement is PROVISIONAL as an accountability target and is not the headline stat.",
     "The 3.3 -> 8.4 -> 11.9 progression across regimes is a real finding but a confounded "
     "one: it mixes pack size, dash-chaining and AoE proficiency, which G-2b is separating. "
     "Matt ruling R-KC1-2 keeps it out of the primary set until that decomposition lands. "
     "Banding it now would band a measurement artifact.",
     "kills_per_engagement", None, None, "causal confound, undecomposed", "MEASURED", 1,
     "T-1: G-2b files the causal decomposition; the tier is then re-ruled",
     C + " sec 8 R-KC1-2; " + V + " sec 3"),
    ("C-EHP-LOWER-BOUND", "session", S, "normalisation-caveat", "moderate",
     "Every %EHP figure is normalised by a LOWER BOUND on max HP.",
     "The denominator is each window's OBSERVED max HP, which is whatever the reader saw. "
     "Max HP moves 250 -> 1600 across the run, so absolute HP is not comparable between "
     "regimes and %EHP figures are, if anything, overstated.",
     "intake_pc_ehp,intake_pc_ehp_per_s,hp_drop_pc_ehp,intake_per_kill_pc_ehp,"
     "hp_drop_count_ge_10pc_ehp,frac_intake_from_drops_ge_10pc_ehp,hp_max_observed",
     None, None, "instrument reads the current sheet, not the true maximum", "MEASURED", 1,
     "read max HP from the character sheet per regime in v2", F + " sec 6"),
    ("C-DAMAGE-UPPER-BOUND", "measure", "damage_spent", "normalisation-caveat", "high",
     "damage_spent and damage_per_kill are OVERKILL-INFLATED UPPER BOUNDS on monster EHP.",
     "Inflated by overkill, by damage dealt to monsters that die outside the window, and by "
     "anything that misses. Read 494.2 as 'no more than 494, probably meaningfully less' -- "
     "never as 'an R2 monster has 494 health'. Per-engagement attribution below 12 s is not "
     "supported at all: the dps field is a 5.0 s rolling mean (measured over 22 clean "
     "falling edges), so a 4.5 s engagement's integral leaks into its neighbour's. The "
     "merged-interval aggregate is the ceiling of what this field supports.",
     "damage_spent,damage_per_kill,damage_per_kill_merged", None, None,
     "the instrument is a rolling-mean gauge, not an event log", "MEASURED", 0,
     "a damage instrument that is not a 5 s rolling mean", F + " sec 7"),
    ("C-ATTACKCOST-DEAD", "session", S, "instrument-dead", "high",
     "Per-kill attack cost is NOT RECOVERABLE from this run, by two independent failures.",
     "(1) The named instrument is dead for 95% of the run: defaultweaponattack covers "
     "play_time 358-1134 only -- 11.5% of elapsed time and 43 of 882 kills (4.9%). "
     "(2) The live substitute aliases: of 514 samples carrying a kill increment, 201 (39%) "
     "are multi-kill (113 doubles, 38 triples, 31 quads, 12 fives, 6 sixes, one seven). At "
     "0.5 s, attacks cannot be attributed to kills inside those, and the 313 single-kill "
     "events are conditioned on being single-target -- the non-AoE tail, not the "
     "distribution. Not recoverable by reprocessing. Q47 is solved at the ENGAGEMENT level "
     "for R2 and R3, and unsolved at the per-kill level.",
     "skill_use_count", None, None, "instrument coverage + sampling-rate aliasing",
     "MEASURED", 0, "v2 recording per verdict sec 8", V + " sec 5"),
    ("C-ONSLAUGHT-UI-MASKED", "measure", "skill_use_count", "confound", "high",
     "The onslaught counter freezes in werewolf form. The freeze is UI behaviour, not player behaviour.",
     "The counter reads 54 across 11,486 consecutive samples from play_time ~1145 onward. "
     "Matt's testimony (2026-07-28): 'Onslaught skill use is hidden by the game because I "
     "was in werewolf form; the skill that impacted the enemies was the werewolf claw.' The "
     "OPEN sub-question: did Onslaught function as a claws-damage AUGMENT while transformed, "
     "or was the press REPLACED by a claw swing? T-2's empirical check still runs; testimony "
     "and series must agree or the disagreement is itself a finding.",
     "skill_use_count", None, None, "GD transform skill-exclusion / conversion machinery",
     "ATTESTED", 1,
     "G-4 reads the Fangs-of-Asterkarn werewolf-transform records in the Edition-II .arz "
     "for skill-exclusion / skill-conversion behaviour; T-2 checks whether the counter ever "
     "increments in R2/R3", C + " sec 8 testimony amendment 1; R-KC1-3"),
    ("C-RESTORE-ON-LOAD", "regime", R2, "anomaly", "moderate",
     "One unexplained full restore: 66 -> 759 HP inside a single frame, with life_healed +14.51.",
     "At pts 5514.87 the player goes from 66 HP to full in 67 ms while the panel healing "
     "counter records 14.5. Max HP is verified constant at 759 across the jump, so this is "
     "not a werewolf-form rescale. Measured regen in the same window runs ~1.7 HP/frame. "
     "Potions are 0/0 and no devotion proc fired. Two further single-frame jumps >=50% max "
     "HP exist (pts 1843.67 R2; pts 6425.40 R3). Evidence toward restore-on-load, NOT proof: "
     "there is no clock break at 5514.87 in the fitted 12-break list and only one frame is "
     "unreadable, whereas a loading screen blanks the HUD for ~2 s. AFFECTS THE HEALING "
     "COLUMN ONLY -- intake is a strictly negative-delta quantity and is untouched.",
     "healed_hp,healed_hp_per_s", None, None,
     "restore-on-load vs Constitution regen, unresolved", "UNVERIFIED", 1,
     "G-10: a 30 s v2 stand distinguishes restore-on-load from Constitution regen",
     F + " sec 8-A; " + V + " sec 9 + addendum"),
    ("C-OCR-EXCURSION-6425", "regime", R3, "anomaly", "low",
     "One residual OCR excursion survives both guards: +1,116 phantom heal at pts 6425.40.",
     "A '121' read whose preceding flank was a LOWCONF refusal rather than an accepted read, "
     "so neither the truncation guard nor the run-aware spike test saw it. Contributes zero "
     "intake (the feeding pair exceeded the adjacency tolerance). One unresolved excursion "
     "in 17,183 accepted reads. DECLARED, NOT REPAIRED -- a repaired sample is an invented "
     "measurement.",
     "healed_hp,healed_hp_per_s", None, None, "OCR glyph loss beside a refusal flank",
     "MEASURED", 1, "a guard that treats a refusal flank as a spike boundary", F + " sec 8-B"),
    ("C-LIFEHEALED-NOISIEST", "measure", "life_healed", "confound", "moderate",
     "life_healed is the noisiest T-A series: 413 non-monotonic rejections.",
     "413 rejections against 12,913 present reads and 13,633 samples. THE RATE DEPENDS ON "
     "THE DENOMINATOR and this store does not choose one for you: 3.198% of present reads, "
     "3.029% of samples. The verdict's headline 3.1% sits between the two. Rejected reads "
     "are banked with read_status='rejected-nonmonotonic' and their raw value preserved in "
     "panel_series_reading.value_raw, at engagement, regime and session grain in "
     "series_field_quality. No rejection was smoothed away.",
     "life_healed", None, None, "OCR instability on a six-character decimal field",
     "MEASURED", 1, "a v2 read at higher bitrate / larger UI scale", V + " sec 1"),
    ("C-COUNTERS-NONZERO", "session", S, "control-violation", "low",
     "The counters did NOT start at zero: the run's head frame already reads 2 kills.",
     "Protocol control counters-start-at-zero is VIOLATED. Panel kills endpoint is 882; the "
     "segmentation attributes 880. The two agree exactly once the 2 pre-run kills are "
     "subtracted, which is the closure check on the whole kills series.",
     "kills,life_healed,skill_use_count", None, 2, "session not started from a fresh save",
     "MEASURED", 1, "v2: perform the smoke gate on a fresh save", V + " sec 1"),
    ("C-PLAYTIME-UNLOCATED", "session", S, "resolution-limit", "low",
     "209 of 13,633 panel samples (1.53%) cannot be located to a regime.",
     "206 play_time refusals plus 3 non-monotonic rejections. Their regime_id is NULL rather "
     "than carried forward from a neighbour: a forward-fill would be an interpolation, and "
     "this store does not interpolate. They are absent from regime-scope quality counts and "
     "present in session-scope ones, which is why the two do not sum.",
     "", None, None, "OCR refusal on the play_time field", "MEASURED", 1,
     "recoverable in principle by pts-interval inference from the fitted clock map; NOT "
     "done, because that is an inference dressed as a measurement", V + " sec 1"),
]

CLAIMS = [
    # id, subject_kind, subject_ref, text, grade, method, source, upgrade_criterion, gate
    ("EC-TA-SERIES", "series", "T-A-panel",
     "The 13,633-sample panel-counter series is a faithful reading of the run.",
     "MEASURED",
     "Two-method closure: every series terminates exactly on the independently human-read "
     "sec-6b totals (882 kills / 74 weaponattack / 54 onslaught / 358 claws / 175 charge / "
     "12468.06 healed), reached by OCR down a fully independent path. Two methods, one "
     "number, no shared failure mode. Screenshot arm 313/313 with zero rejections. Clock "
     "model confirmed out-of-sample: divergence falls 80.0 s, reproduced at 13,633 points.",
     V + " sec 1", None, None),
    ("EC-TB-SERIES", "series", "T-B-globe",
     "The 19,348-frame health-globe series is a faithful reading of damage intake.",
     "MEASURED",
     "Validated against the committed 60 fps death-window series over the same footage: "
     "939 co-read frames, 97.55% agreement, all 23 disagreements +/-1 HP from sub-frame "
     "sampling phase against a 1 HP/frame decay. Independent closure: round 2 measured 57 "
     "identical -10 HP ticks; T-B at a quarter the frame rate through a different code path "
     "returns intake 570, 57 drop events, drop median = drop max = 10. 570 = 57 x 10.",
     F + " sec 2", None, None),
    ("EC-DEVOTION-ZERO-ASSIGNED", "control", "no-devotion-assigned",
     "Zero devotion points were ASSIGNED during the run.", "ATTESTED",
     "Player testimony. The verdict explicitly declined this stronger claim on 2026-07-26 "
     "(it certified only that no devotion PROC fired) and left it UNVERIFIED; Matt's "
     "testimony at launch upgraded it to ATTESTED.",
     "Matt verbatim, charter launch record 2026-07-28: 'I definitely did not utilize any "
     "devotion points.'",
     "The R-KC1-4 .gdc save-file probe parses the save and returns a devotion allocation of "
     "zero. That upgrades this claim ATTESTED -> MEASURED.", "R-KC1-4 (legolas, in flight)"),
    ("EC-DEVOTION-NO-PROC", "control", "no-devotion-proc-fired",
     "No devotion proc fired at any point in the run.", "MEASURED",
     "313 native screenshots inspected; no proc visual in any of them. This is the control "
     "that protected the oracle, and it is a WEAKER claim than EC-DEVOTION-ZERO-ASSIGNED.",
     V + " sec 1, sec 9", None, None),
    ("EC-POTIONS-ZERO", "control", "no-potions",
     "Zero health and zero mana potions were consumed across the run.", "MEASURED",
     "Both panel counters read 0 across all 13,633 samples, and Matt's stated intent agrees.",
     V + " sec 1; Matt verbatim 2026-07-26", None, None),
    ("EC-BUILD-BREAK-1134", "boundary", R2,
     "The R1/R2 build break sits at play_time 1134.", "MEASURED",
     "defaultweaponattack climbs one at a time 61 -> 74 between 1019 and 1134; onslaught "
     "bursts 47 -> 54 by 1145; then 11,486 consecutive samples read exactly 74. Verified a "
     "clean climb, not an OCR jump. Supersedes the spot-sampled 1757: a spot-sampled "
     "boundary is an upper bound, not a location.",
     V + " sec 2 (C-2)", None, None),
    ("EC-DOT-BOUNDARY-6052", "boundary", R3,
     "The R2/R3 poison-DoT boundary sits at play_time 6052.", "DERIVED",
     "The DoT is gear-gated, not level-gated. The gear equip BRACKETS to play_time "
     "6052-6282 (level 11) -- a 230 s band -- and the boundary is banked at the band's LOWER "
     "edge. That choice is a derivation, not a measurement, and it moves up to 230 s of "
     "engagements between R2 and R3. The bracket itself is MEASURED; its collapse to a point "
     "is not.",
     V + " sec 2 (C-1)",
     "Locate the gear-equip event inside the 6052-6282 bracket -- from the .gdc save probe, "
     "from an inventory-panel read, or from the first poison-DoT tick in the globe series.",
     "R-KC1-4 .gdc probe; or a targeted T-B pass over pts covering play_time 6052-6282"),
    ("EC-ONSLAUGHT-UI-MASK", "measurement", "skill_use_count/onslaught",
     "The frozen onslaught counter reflects UI masking in werewolf form, not player behaviour.",
     "ATTESTED",
     "Player testimony, pre-confirming the frozen-counter reading. Branch (b) of the "
     "pre-pinned R-KC1-3 disposition rule.",
     "Matt verbatim, charter launch record 2026-07-28",
     "G-4 reads the Fangs-of-Asterkarn werewolf-transform records in the Edition-II .arz for "
     "skill-exclusion / skill-conversion behaviour, AND T-2 confirms the counter never "
     "increments in R2/R3. Agreement upgrades to MEASURED; disagreement is a finding.",
     "T-2 + G-4 (charter sec 8 testimony amendment 1)"),
    ("EC-XPBAR-CAUSE", "instrument", "T-B-globe/FLASH",
     "The FLASH refusal class is caused by the experience bar blooming across the globe numerals.",
     "INFERRED",
     "The EFFECT is MEASURED -- 719 frames, glyph band collapsing 12 rows to 6-8, and a "
     "calibration sweep over five brightness and four chroma thresholds plus a blue-channel "
     "variant recovers nothing. The IDENTIFICATION of the gold band as the experience bar is "
     "an inference from screen geometry.",
     F + " sec 5",
     "A v2 recording with UI scale raised or the readout moved either removes the FLASH class "
     "or does not. Either outcome settles the identification.",
     "v2 recording requirement"),
    ("EC-DAMAGE-UPPER-BOUND", "measurement", "damage_spent",
     "Damage spent per kill is an overkill-inflated upper bound on monster effective HP.",
     "DERIVED",
     "Integral of the trailing rolling-mean dps field. Kernel width MEASURED, not assumed: "
     "5.0 s p50 over 22 clean falling edges (p90 6.5, max 7.5). Kernel sensitivity K = 5.0 "
     "-> 7.5 s moves the R2 merged figure by 1.9%. The merged-interval estimator covers 612 "
     "of R2's 647 kills and is immune to the attribution problem.",
     F + " sec 7",
     "A damage instrument that is an event log rather than a 5 s rolling mean would make "
     "monster EHP measurable rather than bounded.", "v2 instrument change"),
    ("EC-RESTORE-ON-LOAD", "anomaly", "C-RESTORE-ON-LOAD",
     "The three single-frame full-restore events are restore-on-load rather than Constitution regen.",
     "UNVERIFIED",
     "Evidence in favour: 693 HP recovered in 67 ms against ~1.7 HP/frame measured regen, "
     "with life_healed recording only 14.5. Evidence against: no clock break at pts 5514.87 "
     "in the fitted 12-break list, and only one unreadable frame where a loading screen "
     "blanks the HUD for ~2 s. Handed up as a finding, not a resolution.",
     F + " sec 8-A; " + V + " sec 9",
     "G-10: a 30 s v2 stand that loads a save and watches the globe distinguishes the two "
     "mechanisms directly.", "G-10 v2 trial"),
    ("EC-SEGMENTATION-GRAIN", "fixture", SEG,
     "The gap>5 s inter-kill-event rule is the correct definition of 'an engagement'.",
     "UNVERIFIED",
     "The cut reproduces exactly and the arithmetic is sound; what is unestablished is that "
     "this grain is the RIGHT grain. It was chosen as the most permissive defensible "
     "threshold, which is also the only one that reaches the target engagement band -- a "
     "selection pressure worth naming out loud.",
     V + " sec 4",
     "HALT H-1: Matt rules the grain WITH the G-2b causal decomposition in hand "
     "(engagement-duration trend, intra-engagement kill-gap structure, charge-per-engagement, "
     "multi-kill fraction per regime), before any acceptance band is drafted.",
     "HALT H-1 (charter sec 5)"),
    ("EC-DIFFICULTY", "control", "difficulty-declared",
     "The run's difficulty setting is unrecorded.", "UNVERIFIED",
     "Protocol sec 3.5's notes.md was not delivered, so difficulty, starting area, "
     "per-boundary play_time jots and per-transition area names are all ABSENT rather than "
     "inferred. fixture_session.difficulty is NULL for this session.",
     V + " sec 1; M6 ingest note",
     "Matt states the difficulty, or the R-KC1-4 .gdc save probe reads it.",
     "R-KC1-4 .gdc probe"),
    ("EC-FIXTURE-IDENTITY", "fixture", "GD-R2-werewolf",
     "R2 is THE fixture and is named GD-R2-werewolf, kit gd-werewolf-kitcal-1.", "ATTESTED",
     "Matt ratified the charter's grill-item-1 lean verbatim at launch ('Agreed on all five "
     "leans'). Naming governs canon. R1/R3 fixture names in this store are elrond-provisional "
     "-- only GD-R2-werewolf was ratified.",
     C + " sec 8 ruling R-KC1-1", None, None),
]

# session_control grading rule, applied uniformly and recorded here so it is auditable.
GRADE_RULE = [
    ("Matt verbatim", "ATTESTED"),
    ("elrond tight-crop read", "MEASURED"),
    ("gandalf/notes/2026-07-26-gd-playtest-v1-artifact-verification", "MEASURED"),
    ("ABSENT", "UNVERIFIED"),
]


def main():
    cx = sqlite3.connect(DB)
    cx.execute("PRAGMA foreign_keys = ON")
    try:
        cx.execute("BEGIN")

        cx.execute("DELETE FROM fixture_target")
        cx.execute("DELETE FROM measured_fixture WHERE session_id=?", (S,))
        for fid, rid, kit, role, naming, ruling, grade, notes in FIXTURES:
            cx.execute("""INSERT INTO measured_fixture
                (fixture_id, session_id, regime_id, segmentation_id, kit_id, run_id,
                 calibration_run, fixture_role, naming_status, ruling_ref, charter_ref,
                 verdict_ref, evidence_grade, notes)
                VALUES (?,?,?,?,?,?, 'KC1-2026-07-27', ?,?,?,?,?,?,?)""",
                (fid, S, rid, SEG, kit, S, role, naming, ruling, C, V, grade, notes))
        log(f"measured_fixture: {len(FIXTURES)} rows")

        for fid, tk, tier, mk, fam, rationale, gate in TARGETS:
            cx.execute("""INSERT INTO fixture_target
                (fixture_id, target_key, tier, measure_key, stat_family, rationale,
                 gate_ref, ruling_ref, band_status)
                VALUES (?,?,?,?,?,?,?, 'R-KC1-2', ?)""",
                (fid, tk, tier, mk, fam, rationale, gate,
                 "waived" if tier == "report-only" else "unratified"))
        log(f"fixture_target: {len(TARGETS)} rows (bands UNRATIFIED until HALT H-2)")

        cx.execute("DELETE FROM fixture_condition")
        for (cid, sk, sr, kind, sev, head, detail, measures, engs, kills, cause, cg,
             rec, remedy, ev) in CONDITIONS:
            cx.execute("""INSERT INTO fixture_condition
                (condition_id, scope_kind, scope_ref, condition_kind, severity, headline,
                 detail, affects_measure_keys, affected_engagement_ids, affected_kills,
                 cause, cause_grade, recoverable_from_this_footage, remedy, evidence_ref,
                 status, raised_by, raised_date)
                VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?, 'open', 'elrond (M8 ingest)', ?)""",
                (cid, sk, sr, kind, sev, head, detail, measures, engs, kills, cause, cg,
                 rec, remedy, ev, DATE))
        log(f"fixture_condition: {len(CONDITIONS)} rows")

        cx.execute("DELETE FROM evidence_claim WHERE session_id=?", (S,))
        for cid, kind, ref, text, grade, method, source, upg, gate in CLAIMS:
            cx.execute("""INSERT INTO evidence_claim
                (claim_id, session_id, subject_kind, subject_ref, claim_text, grade,
                 method, source, source_date, upgrade_criterion, upgrade_gate_ref, status)
                VALUES (?,?,?,?,?,?,?,?,?,?,?, 'current')""",
                (cid, S, kind, ref, text, grade, method, source, DATE, upg, gate))
        log(f"evidence_claim: {len(CLAIMS)} rows")

        # the two devotion controls the session_control table never carried
        for key, held, grade, claim, ev in (
                ("no-devotion-assigned", "held", "ATTESTED", "EC-DEVOTION-ZERO-ASSIGNED",
                 "Matt verbatim 2026-07-28: 'I definitely did not utilize any devotion "
                 "points.' Verdict sec 9 had left this UNVERIFIED."),
                ("no-devotion-proc-fired", "held", "MEASURED", "EC-DEVOTION-NO-PROC",
                 "No devotion proc visual in any of 313 native screenshots (verdict sec 1).")):
            cx.execute("""INSERT OR REPLACE INTO session_control
                (session_id, control_key, held, intent, affects_measure_key,
                 effect_on_measure, effect_note, evidence, evidence_grade,
                 upgrade_criterion, claim_id, ruled_by, ruled_date)
                VALUES (?,?,?, 'deliberate-control', '', 'confound-retired', ?,?,?,?,?,
                        'Matt', ?)""",
                (S, key, held,
                 "Protects the oracle: a devotion proc would inject damage and healing the "
                 "kit spec cannot model.", ev, grade,
                 "R-KC1-4 .gdc save probe returns devotion allocation" if grade == "ATTESTED"
                 else None, claim, DATE))

        # grade the 17 pre-existing controls by a uniform, auditable rule
        n = 0
        for sid, key, amk, evid in cx.execute(
                "SELECT session_id, control_key, affects_measure_key, evidence "
                "FROM session_control WHERE session_id LIKE 'GP-gd-%' "
                "AND evidence_grade IS NULL"):
            grade = "UNVERIFIED"
            for needle, g in GRADE_RULE:
                if evid and needle in evid:
                    grade = g
                    break
            cx.execute("UPDATE session_control SET evidence_grade=? WHERE session_id=? "
                       "AND control_key=? AND affects_measure_key=?", (grade, sid, key, amk))
            n += 1
        log(f"session_control: 2 devotion rows added, {n} pre-existing rows graded")

        cx.commit()
    except Exception:
        cx.rollback()
        raise
    fk = list(cx.execute("PRAGMA foreign_key_check"))
    log(f"foreign_key_check: {'CLEAN' if not fk else fk[:5]}")
    cx.close()


if __name__ == "__main__":
    main()
