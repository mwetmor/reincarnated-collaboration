# Tier-3 PREREG-beat — RE-JOIN + NEUTRAL-ARENA BASELINES — REPORT

**PREREG-beat of the Tier-3 Encounter-Geometry Run** · conductor gandalf `RUN-CONDUCTOR` · ruling L-13(d)
**Author:** named-gamora sub-agent · 2026-07-22
**Two-part wave:** Part 1 fit RE-JOIN on the membership sidecar · Part 2 NEUTRAL-ARENA BASELINES (the prereg's empirical input)

**Engine HEAD:** `b34a14b` at open. **MOVED mid-session to `a3671d4`** (star-lord commit:
`W3 bundle flavor wiring + encounters reserved key + 9 tests`). The `b34a14b..a3671d4`
delta touched ONLY `export/` + `output/` + `tests/` — **NOTHING in
`simulation/spatial_gauntlet/` or `generation/`** (the harness + builders I invoke).
Baseline runs are stable at `a3671d4`; both JSON artifacts stamp both HEADs. HEAD
re-verified `a3671d4` post-run (no further movement). Lane-2's Gate-2 is elsewhere in the
engine repo; my invocation is read/import-only, zero engine-repo writes.

**Substrate:** corpus.db md5 `d091881d` (READ-ONLY, md5-checked in both scripts) + membership
sidecar `2026-07-22-tier3-family-membership-sidecar.json` (READ-ONLY, commit `6dd43161`,
declares corpus md5 `d091881d` — matches).

**Artifacts (all in `agentic_orchestration/gamora/notes/`):**
- `2026-07-22-tier3-w2-fit-layer-v2.py` — Part 1 RE-JOIN compute + delta census
- `2026-07-22-tier3-w2-fit-output-v2.json` — 1068 fit records (+ `membership_tier` per row) + DELTA census
- `2026-07-22-tier3-prereg-baselines-math.md` — Part 2 math note (Discipline #1, math-before-code)
- `2026-07-22-tier3-prereg-baselines.py` — Part 2 baseline harness (real fighting PlayerClass path)
- `2026-07-22-tier3-prereg-baselines.json` — 131 per-kit baselines + per-era variance + feasibility
- this report

**v1 output preserved unmodified** (`2026-07-22-tier3-w2-fit-output.json` — audit trail; verified untouched by git).

---

## PART 1 — RE-JOIN DELTA CENSUS

Re-ran the W2 fit layer sourcing family resolution from the sidecar (ACTIVE rows only =
falsy `shadowed_by`; `on_spine` resolves the record-267 spine). Weights FROZEN per L-13(a)
(0.50 verb / 0.30 topology / 0.20 shelf — not re-derived). `membership_tier` added per fit
row per L-13(c). Resolution fallback unchanged: family → kit-level → era. **Totality
preserved: 1068/1068 rows, 0 errors.**

**Resolution delta (the headline):**

| | v1 (gateA RATIFIED-only) | v2 (sidecar, all tiers) |
|---|---|---|
| spine kits family-resolved | 46 | **131** (+85 newly) |
| membership tiers | RATIFIED only | RATIFIED 46 / PROPAGATED 31 / DOCKET 54 |
| families covered | 5 | **9** (adds MELEE-STRIKE, DOT-AILMENT, MULTI-PROJECTILE-VOLLEY, SHAPESHIFT) |
| zero family CHANGES for the 46 overlap kits | — | confirmed (sidecar RATIFIED ≡ gateA byte-identical) |

**scoring_basis distribution — before → after:**
`{full 184, era_only 884}` → **`{full 524, era_only 544}`** (+340 full = 85 newly-resolved kits × 4 eras).

**Per-era resolution mix (v2):** family resolution is era-independent (full=131 in every
era); present/hole shifts per deck:

| Era | full | era_only | present | hole | unresolved |
|---|---|---|---|---|---|
| I | 131 | 136 | 125 | 6 | 136 |
| II | 131 | 136 | 111 | 20 | 136 |
| III | 131 | 136 | 111 | 20 | 136 |
| IV | 131 | 136 | 131 | 0 | 136 |

(Era IV has 0 holes — all 9 resolved families are IV-present; Eras II/III have 20 holes =
resolved families whose deck omits them. Correct determinate-join behavior.)

**fit_score spread for the 85 newly-resolved kits (v1 era_only → v2 full):**
- v1 (era_only neutral degradation): min 0.5, max 0.6, mean 0.525, **stdev 0.043** (flat band)
- v2 (full family-keyed scoring): min 0.1, max 1.0, mean 0.658, **stdev 0.265**

→ a **6.1× variance expansion**. Family resolution genuinely differentiates the newly-resolved
kits — they were collapsed to a neutral era-band in v1 and now spread across the full
showcase↔stress range, which is what W3's argmax/argmin selection needs.

**Per-family spine counts (v2):** TOTEM-SENTRY 32 · TRAP-MINE 26 · DOT-AILMENT 20 ·
MELEE-STRIKE 15 · MULTI-PROJECTILE-VOLLEY 14 · WHIRLWIND 7 · AURA 6 · CHANNELED-BEAM 6 ·
SHAPESHIFT 5. (TOTEM+TRAP = 58, the reported skew.)

---

## PART 2 — NEUTRAL-ARENA BASELINES

### Baseline design + budget

**Neutral scenario:** `open_arena` (open 36×36 field; verified neutral — `choke_zones=[]`,
`has_boss=False`, `has_mini_boss=False`, `continuous_spawn=None`, `timed_add_waves=()`,
`win_condition=all_mobs_killed`; 40 mobs = 3 elite + 37 swarm). No formation shaping, no
choke, no wave injection. The mob roster is held byte-identical across ALL kits (neutrality);
only the player varies.

**CRITICAL design finding (Discipline #11, verified before spending budget):** a raw
hand-rolled `class_dict` (skill dicts) produces a **PASSIVE player** — `player_damage_total=0.0,
mobs_killed=0` even with a 50m-reach circle at `damage_modifier=20`. The player only issues
attacks when a real `PlayerClass` is threaded via the `player_class=` kwarg (the PRODUCTION
PATH). The W2 scenario driver floored at WR=0.0 for exactly this reason (it never asserted
player kills, only engagement). **Fix:** map each kit's BC vector to the nearest materialized
endgame BC-cell and build that cell's real fighting PlayerClass via the production martial
builder (`_build_martial_player_class`, 0.22s/build, LLM-free, 12 real skills). The kit is
still the variable — its BC vector `(range, tempo, amp, attr)` selects the fighter.

**HONEST LIMITATION (declared, not buried):** with nearest-cell mapping, between-kit variance
is **between-CELL** (16 distinct fighters), not between-131-kits. Kits sharing a cell share a
fighter → their pairwise fighter-variance is 0, and the reported within-kit(seed) stdev is a
LOWER bound on the true per-kit noise floor (kits-in-a-cell differ only by metadata, not
fighter shape). This is the correct trade: 16 REAL fighting players (valid metrics) beats 131
PASSIVE non-fighters (zero metrics). A finer baseline (one KitCandidate per corpus kit) is a
**rocket-seam generation task** — flagged, not undertaken (I only CALL the existing martial
builder; zero generation-seam patching). Cell-assignment coverage: 29 exact / 80 dist-1 / 20
dist-2 / 2 dist-3; 16 of 17 cells used; no coverage holes.

**Calibration:** `damage_modifier=1.0` (the metrology driver's native operating point — no
dead-wall dmod), applied UNIFORMLY. Yields a non-degenerate graded band. Instrument-comparable
to the Lane-3 four-family metrology run.

**Budget (Discipline #2 smoke-scale):** 4 seeds/kit × 131 kits = **524 fights**, paired seed
set {20260722–25} shared across all kits (between-kit signal not confounded by seed draw).
Discipline #3 honored (single sequential process, one seed set, no parallel same-seed).
Wall: **8.9s** (16 cached builds ~0.3s + 524 fights). **0 errors.**

### Variance findings (statistical OBSERVATION — the conductor declares X + the metric subset)

Pool band non-degenerate: `mobs_killed` per-kit means span [0.0, 40.0], stdev 12.8 (NOT a
floor/ceiling artifact). Pool WR mean 0.107 (most fights time-out as winner=monster in the
~5s smoke — WR is NOT the deliverable; the graded per-metric variance is).

**Pool signal-to-noise (between-cell stdev / mean within-kit(seed) stdev), ranked:**

| metric | S/N | between-cell sd | within-seed sd | pool range |
|---|---|---|---|---|
| `player_damage_total` | **389** | 6370.0 | 16.4 | [0, 19575] |
| `total_aoe_hits` | **185** | 12.82 | 0.069 | [0, 40] |
| `mobs_killed` | **176** | 12.82 | 0.073 | [0, 40] |
| `max_flanking_count` | 54 | 5.51 | 0.103 | [10.75, 38] |
| `total_flanking_ticks` | 34 | 10.34 | 0.307 | [4, 31] |
| `elapsed_s` | 9.4 | 0.373 | 0.040 | [4.03, 5.3] |

**Stable enough to gate on (observation):** `player_damage_total`, `total_aoe_hits`,
`mobs_killed` carry overwhelming between-cell signal vs seed noise (S/N > 170) — the
strongest candidates for an effect-size gate. `max_flanking_count` / `total_flanking_ticks`
are secondary (S/N 34–54). `elapsed_s` is the tightest band (S/N 9.4) — usable but low
dynamic range in a smoke.

**Null/constant on this path (NOT gate-eligible from this baseline):** `total_mob_count`
(fixed 40), `damage_taken_while_committed`, `completion_rate`, `whiff_rate`, `sustain_uptime`,
`total_displacement`, `cone/line/circle_hit_fraction`, `forced_break_count`, `move_cancel_count`,
`drain_exhaustion_events` — these fields are not populated by the open_arena smoke config.

**CAVEAT on the noise floor:** the within-kit(seed) stdev is unusually low (0.07 for
mobs_killed) because the fighter is deterministic and a 5s open-arena outcome is barely
seed-perturbed. Two consequences the conductor should weigh when deriving X: (1) the true
per-kit noise floor is likely HIGHER than reported (cell-sharing hides per-kit shape noise);
(2) an X set purely off this within-seed floor would be very tight — a longer-fight or
win-condition-reaching baseline would give a more conservative noise estimate. This is a
smoke-scale variance estimate, explicitly bounded.

### Per-era W3 feasibility (sample rule n≥8 + courts)

| Era | n (resolved kits) | n≥8 | courts represented | TOTEM+TRAP | verdict |
|---|---|---|---|---|---|
| I | 27 | yes | 6 (physical 14, fire 5, chaos-poison 4, lightning 2, cold 1, +1 null) | 9/27 (0.33) | **FEASIBLE** |
| II | 53 | yes | 6 (chaos-poison 17, physical 12, fire 11, lightning 6, cold 6, +1 null) | 26/53 (0.49) | **FEASIBLE** |
| III | 20 | yes | 5 (physical 6, chaos-poison 5, fire 5, lightning 3, cold 1) | 8/20 (0.40) | **FEASIBLE** |
| IV | 31 | yes | 5 (physical 14, fire 7, chaos-poison 6, lightning 3, cold 1) | 15/31 (0.48) | **FEASIBLE** |

All four eras satisfy n≥8 AND element-court representation (5–6 courts each). W3's per-era
sample rule is feasible across the board.

### TOTEM/TRAP skew note (sampling)

58 of the 131 resolved kits (44%) are TOTEM-SENTRY (32) or TRAP-MINE (26). Per-era the skew
concentrates in the middle eras: **Era II 49% (26/53)** and **Era IV 48% (15/31)** are nearly
half emplacement-family; Era III 40% (8/20); **Era I is the lightest at 33% (9/27)**. A naive
uniform per-era sample would over-represent emplacement play in II/IV. For a family-balanced
W3 sample the conductor may want per-era family stratification — Era II especially, where
TOTEM-SENTRY alone is 14/53 (26%). Era I offers the most family-diverse pool
(MELEE-STRIKE 8, TRAP-MINE 6, TOTEM/WHIRLWIND/MPV 3 each).

---

## Discipline compliance

- **#1 math-before-code:** math note (`…-baselines-math.md`) written BEFORE the harness; the
  §2-probe finding (raw class_dict = passive player) DROVE a documented design correction
  (synth-kit → real-PlayerClass) captured in the note before the full run.
- **#2 smoke-test:** Part 2 is a smoke (524 fights, 8.9s wall, single arena); Part 1 re-join
  is deterministic and re-ran clean (its own smoke). No full regen.
- **#3 no parallel same-seed:** single sequential process, one shared seed set.
- **#11 empirical inspection over assumption:** the passive-player pathology was CAUGHT by a
  3-kit smoke before committing the 524-fight budget; every metric's gate-eligibility is
  grounded in measured S/N, not assumed.
- **External-system rule (ADR-006):** corpus.db + sidecar READ-ONLY (md5-checked, `mode=ro`);
  zero telemetry writes; zero engine-repo writes (harness invoked by path).
- **Generation-seam boundary:** the finer-grained per-corpus-kit baseline is flagged as a
  rocket-seam task, NOT patched here.
- **No prereg authoring:** X (effect-size threshold) + metric-subset declaration are the
  CONDUCTOR's per L-13. I deliver variance data + statistical observations only.
- **No scoring-weight changes:** Part 1 weights FROZEN per L-13(a).
- **Working labels:** all family values are working labels (charter §5 / T3-V2), rename-safe.

## What the conductor owns from here

1. **Derive X** (effect-size threshold) from the Part-2 variance data — candidates by S/N:
   `player_damage_total` / `total_aoe_hits` / `mobs_killed`. Weigh the noise-floor caveat
   (cell-sharing understates per-kit noise; a longer-fight baseline would be more conservative).
2. **Declare the metric subset** the W3 showcase/stress contrast is measured on.
3. **Decide per-era family stratification** for the W3 sample given the TOTEM/TRAP skew
   (II/IV ~48–49% emplacement).
4. **(optional) commission a finer baseline** — one real fighter per corpus kit — as a
   rocket-seam generation task if between-131-kit (not between-16-cell) variance is needed.
