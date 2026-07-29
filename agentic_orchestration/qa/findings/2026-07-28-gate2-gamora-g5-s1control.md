# Finding — 2026-07-28 — G-5 S-1 control arm (KIT-CAL-1 / KC1-2026-07-27)

**Reviewer:** jack-ryan (DEV-MODE, Gate 2)
**Severity:** **CONDITIONAL PASS** on the landing · **BLOCK** on the `g5_r3arm/` banked artifact
**Target:** `ee5930a` / tag `gamora/v-g5-s1control-1` (engine) · plus `g5_r3arm/` output banked at `f54c547`
**Developer:** gamora (simulation seam)
**Principles applied:** #1 math-before-code · #2 smoke-gate · #4 decisions-log-as-truth · #5 severity
**Disciplines cited:** #1, #2, #6 (right tool for the validation question), #8 (schema validation at boundaries), #10 (empirical inspection over assumption), #12 (semantic-shift naming)
**Verification stance:** every claim below was re-derived independently from the banked traces and by live instrumentation. Gamora's notes were read but not trusted as evidence.

---

## §1 — What I found (descriptive)

### 1.1 The control arm's code is correct, and the value-identity claim verifies

Independent leaf-level diff of `fixture_class_dict(s1_control=False)` vs `(s1_control=True)` across all **12** kit variants (pool ∈ {759, 1607} × with_dot ∈ {F,T} × leech ∈ {0.0, 0.05, 0.08}) returns **exactly 7 differing leaves in every variant**, all geometry:

```
.skills[0].geometry_type            ('cone', 'single_target')
.skills[0].geometry_params.arc_degrees          (150.0, <ABSENT>)
.skills[0].geometry_params.max_targets          (5,     <ABSENT>)
.skills[1].geometry_type            ('line', 'single_target')
.skills[1].geometry_params.path_length_m        (14.0,  <ABSENT>)
.skills[1].geometry_params.path_radius_m        (2.5,   <ABSENT>)
.skills[1].geometry_params.terminal_radius_multiplier (1.5, <ABSENT>)
```

Zero divergence in `damage_multiplier`, `cooldown_seconds`, `energy_cost`, `range_m`, `effects`, `canonical_element`, `role`, or the `_calibration_overrides` door block. **Claim verified by diff, not by note.**

Flag threading is sound and cannot masquerade: report body `s1_control: true`, report filename `kitcal_g5_g5_s1control_report.json`, output dir `g5_s1control/`, trace filenames `<tier>__<arm>__s1control__seed<n>.jsonl`, and `fight_key` all carry the marker. `FightRecord.arm` correctly keeps the plain value so arm assertions are unaffected. Canonical battery emits `s1_control: false` and a `None` summary.

Pins hold and are non-vacuous. 27/27 tests pass (0.37 s). A-S1C-1's injection test patches `fixture_class_dict` in both directions (control-that-did-not-neutralize; flag-leaked-into-canonical) plus a half-controlled scenario set, all three raising `A-S1C-1`. A-S1C-2's injection raises at runtime. `assert_static_pins` correctly went 8 → 9.

Engine-hash concern cleared: the canonical battery ran at `bef1f55`, the control at `f54c547`. I diffed the two. **The entire `src/` delta between them is comments and docstrings** — `spatial_engine.py`, `calibration_overrides.py`, `spatial_resolver_adapter.py` show no non-comment line changes. The arms are like-for-like. Her "no code behavior change" claim holds.

### 1.2 The coincidence-floor finding is TRUE, and I reproduced it

Re-derived hits/press from the banked traces with my own grouping (`press = (t_s, skill_idx)` over player-sourced `damage` events), across all 300 fights:

| tier | control pooled | control per-seed min/max | canonical pooled | canonical hits-per-press distribution |
|---|---|---|---|---|
| trash | **1995→ 262/262 = 1.0000** | 1.0000 / 1.0000 | **253/98 = 2.5816** | `{1:8, 2:55, 3:5, 4:30}` |
| champion | 249/249 = 1.0000 | 1.0000 / 1.0000 | 245/155 = 1.5806 | `{1:65, 2:90}` |
| mixed_pack | 896/896 = 1.0000 | 1.0000 / 1.0000 | 876/756 = 1.1587 | `{1:696, 3:60}` |
| boss (A) | 1995/1995 = 1.0000 | 1.0000 / 1.0000 | 2175/2082 = 1.0447 | `{1:1989, 2:93}` |

**"Exactly 1.0000 on every tier and every seed" is TRUE.** Every control press hit exactly one body; the distribution is a single bucket. Geometry in the control traces reads `point` on both skills; canonical reads `cone`/`line`. The neutralization fired and did not leak.

The bin-coincidence mechanism is the correct explanation, and I confirmed it at the event level. Control trash seed 74000800:

```
kill t=0.00 bin=0   | kill t=4.00 bin=8  kill t=4.20 bin=8  kill t=4.30 bin=8  kill t=4.40 bin=8
                    | kill t=4.50 bin=9  kill t=4.60 bin=9  kill t=4.70 bin=9
→ kills=8  kill_events=3  A=2.6667
```

One kill per 0.1 s tick. `compute_abc` is not buggy — I recomputed A independently with my own binning and matched to 4 dp on every tier. The excess is temporal, not spatial. **No alternative explanation survives**: an event-binning defect would have to produce hits/press > 1 or an A/B/C identity violation, and neither is present.

Root cause is correctly identified as claws compiling at `cooldown_seconds = 0.0` (no player attack-speed model), and correctly declined as out of scope for a control arm.

### 1.3 The `.arz` geometry is not in the sim at all — a fact neither document states

`arc_degrees`, `max_targets`, `path_length_m`, `path_radius_m`, and `terminal_radius_multiplier` appear **nowhere in `src/reincarnated/` outside the `kitcal_g5_*` harness files.** They are carried into `_ResolverSkill.geometry_params` and never read. The engine's cone and line are hardcoded:

```python
# spatial_engine.py:185-189
CONE_RANGE_M       = 5.0
CONE_HALF_ANGLE_RAD = math.pi / 4   # 45° half-angle = 90° full cone
LINE_RANGE_M       = 20.0
LINE_WIDTH_M       = 1.5
```

`_compute_cone_hits` reads only `CONE_RANGE_M` and `CONE_HALF_ANGLE_RAD`; `_compute_line_hits` reads only `LINE_RANGE_M` and `LINE_WIDTH_M`. So every hits/press number in this run — gamora's and the verdict's alike — measures a **hardcoded 90° / 5.0 m cone and a 20.0 m × 1.5 m line against a fixed ring formation**, not the pinned 150° / cap-5 arc or the 14.0 m × 2.5 m path.

`geometry_type` *is* read (it routes cone vs. the `point` branch at `spatial_engine.py:1529`), so **the control arm itself is valid**. Only the params are inert.

### 1.4 THE DoT PATH IS INERT — a contract with no writer, at a second site

Across all 300 banked fights (150 W-c + 150 R3), the traces contain **zero `dot` events**. Event counts are byte-equivalent between the two arms: `damage(player)=5724`, `damage(mob)=2314`, `death=720`, `leech=4350` — identical in both.

I confirmed by live instrumentation, not inference. A frame-sink probe on a boss fight (27.8 s, 3 kills, 95 player hits, charge pressing ~7 times with its 810/3.0 s bleed, and in the R3 arm a poison DoT on every one of those 95 claws hits):

```
r3=False with_dot=False  winner=player elapsed=27.8 kills=3 | on_hit=95  DOT_TICKS=0  dot_total=0.0
r3=True  with_dot=True   winner=player elapsed=27.8 kills=3 | on_hit=95  DOT_TICKS=0  dot_total=0.0
```

The seam is named in the adapter's own docstring: `resolve_spatial_hit` states *"Only the returned damage float is carried back to the spatial entity by the caller"* and enumerates the discarded kernel side effects (`heal`, `lifesteal`, `heal_over_time`, `reflect`) — **but does not name DoT application**. The kernel writes the DoT into the defender's scratch `CombatantState.active_effects`; that scratch is discarded; the spatial entity's `combatant_state.active_effects` therefore stays empty; and `_tick_effects` at `spatial_engine.py:5299` is gated on exactly that set being non-empty, so it never runs.

This is the **third instance of the same architectural pattern** — kernel side effect discarded at the projection seam. The first two were the leech carry-back (O-d, repaired inside the door) and the received-side mirror (assembly note §2, caught by gamora at the smoke gate). It was not caught this time because no test asserts a DoT event exists.

### 1.5 Consequences in the banked r3_arm output

`g5_r3arm/g5/kitcal_g5_g5_report.json`, aggregated against the canonical W-c report:

| tier | A W-c | A R3 | B W-c | B R3 | **B lift** | C W-c | C R3 |
|---|---|---|---|---|---|---|---|
| trash | 4.0000 | 4.0000 | 1.0000 | 1.0000 | **1.000** | 2.000 | 2.000 |
| champion | 2.0000 | 2.0000 | 1.0000 | 1.0000 | **1.000** | 2.000 | 2.000 |
| mixed_pack | 1.5000 | 1.5000 | 1.2778 | 1.2778 | **1.000** | 3.167 | 3.167 |
| boss | 1.0000 | 1.0000 | 1.0000 | 1.0000 | **1.000** | 3.000 | 3.000 |

A, B and C are **bit-identical at every tier**. The only quantity that moved is normalized intake, and it moved by exactly the pool ratio (`worst_drop` 5.994 → 2.831; 759/1607 = 0.472; 5.994 × 0.472 = 2.83). The R3 arm changed the player's HP denominator and nothing else.

### 1.6 Two divergences in the banked control output that the landing does not report

**(a) Boss-tier win-rate divergence.** Control boss: **player 50 / monster 10** of 60. Canonical boss: **player 60 / monster 0** of 60. Losses kill 2 of 3; wins kill 3 of 3. Control elapsed is systematically longer at every tier (trash 4.7–4.9 vs 4.2–4.3; mixed 11.0–14.0 vs 10.1–11.5; boss 28.5–32.5 vs 27.3–30.3). The boss tier is the only tier where the control PASSES the band, and it is the tier where the control dies 17 % of the time. (A reads 1.0000 on both wins and losses, so the pass is not manufactured by the truncation — but the divergence is undisclosed.)

**(b) Zero variance on A.** A is identical to 4 dp across all 30 seeds on every tier in **both** arms, while hits/press does vary per seed (canonical trash 2.25–3.00). Effective n on A is ~1, not 30. The report emits `n: 30` and `all_seeds_in_band`.

### 1.7 Two instrument properties that bound the numbers

**Press denominator excludes zero-hit presses.** `compute_breadth`'s key is built inside `on_hit`, so a press that lands no hit leaves no trace event and is structurally invisible. The fixture's 680 is a press-ledger count of *activations*. The sim's denominator is therefore *presses that connected*, which biases sim hits/press **upward** relative to §1.1p's definition.

**A's bins are absolute, not gap-clustered.** `compute_abc` uses `floor(t / 0.5)`. In the control trash trace above, kills at 4.40 and 4.50 fall in different bins despite being 0.1 s apart; a gap-clusterer at the same 0.5 s tolerance would merge bins 8 and 9 and return **A = 4.0, not 2.667**. The reported coincidence floor is a **lower bound**, and it is anchor-dependent. The fixture-side `S1-gap5s-v1` anchoring is not established in this landing.

### 1.8 r3_arm artifact hygiene

The r3 report filename is `kitcal_g5_g5_report.json` — **byte-identical to the canonical battery's filename** — and its traces are `boss__A__seed74000800.jsonl`, also byte-identical to canonical. Only the conductor-chosen parent directory distinguishes them. The report body is distinguishable (`r3_arm: true`, `player_pool_max_hp: 1607.0`), and the r3 report carries no `breadth` block (it predates `compute_breadth`).

---

## §2 — Adjudication of the 1.36-vs-2.58 contradiction

**Ruling: there is no computational divergence. The divergence is aggregation scope, and neither number is a valid §1.1p comparator.**

Both documents use the identical per-press definition and both are arithmetically correct. Their per-tier tables agree to 4 dp, and my independent re-derivation reproduces both:

| tier | verdict §4.3 | gamora math note §6a | jack-ryan (independent) |
|---|---|---|---|
| trash | 2.582 | 2.5816 | **253/98 = 2.5816** |
| champion | 1.581 | 1.5806 | **245/155 = 1.5806** |
| mixed_pack | 1.159 | 1.1587 | **876/756 = 1.1587** |
| boss | 1.045 | 1.0447 | **2175/2082 = 1.0447** |

- The **verdict's 1.3617** is a press-weighted pool over three pack tiers with boss **excluded**: `(253+245+876) / (98+155+756) = 1374/1009 = 1.36175`.
- **Gamora's 2.5816** is the **trash tier alone**.

**The divergence, named: aggregation scope — pooled-over-three-tiers-excluding-boss vs single-densest-tier.** Not definition, not computation, not DoT semantics, not binning.

**Neither number is citable against the fixture's 2.362.** §1.1p is a *session-pooled* ratio over the fixture's own encounter-density mix. The sim battery ran three arbitrary fixed densities plus a boss, and:

- the verdict's pool is **75 % mixed_pack** (756 of 1009 presses), the sparsest pack tier;
- including boss's 2,082 presses drops the pooled figure to **1.1485** — a choice the spec does not adjudicate, and a 19 % swing on an inclusion decision;
- gamora's single tier cannot represent a session-pooled ratio at all;
- the sim's denominator omits zero-hit presses (§1.7), biasing both numbers upward;
- the fixture's `hitsInflicted` DoT semantics are graded **UNCERTAIN** by the spec, which is why §6.2 calls it a diagnostic and not a band;
- the catch-count distributions are **degenerate** — mixed_pack produces only 1s and 3s (never 2), champion only 1s and 2s (never 3) — which is a fixed-ring-formation artifact, not a geometry measurement.

This is the **same tier-weighting defect the verdict itself already flagged at §7.3** for §6.3's bands. It applies to §1.1p equally and was not carried across.

**Of the two, gamora's is the weaker claim and must not be banked.** "Trash within 9 % of the fixture, the arc looks RIGHT" reads a single densest-tier number as a session statistic, in the direction that flatters the sim, on an upward-biased denominator. The verdict's pooled number is the better-scoped of the two but must be restated as density-conditional rather than as a single figure.

### Does keeper (3) survive?

**YES — the operational conclusion SURVIVES, on stronger evidence than the number it was argued from. The stated premise must be AMENDED.**

Keeper (3)'s load-bearing conclusion is *"tightening the target cap would move the sim backwards; re-scope BQ-1/BQ-2 toward geometry-vs-spacing."* Three findings sustain it, none of which depend on the aggregation dispute:

1. **`max_targets` is not read anywhere in the engine** (§1.3). There is no cap to tighten. "Tightening the target cap" is not a change the sim can currently express — it is a no-op, which is a stronger statement than "backwards."
2. **The cap never binds even as declared.** Maximum hits/press anywhere in the 150-fight canonical battery is **4** (trash), against a declared cap of 5. Not one press in the entire battery reached it.
3. **The under-catch is now source-located.** `CONE_HALF_ANGLE_RAD = π/4` gives a **90° full cone** against the fixture's 150°, at a hardcoded 5.0 m reach. That is precisely "the cone under-catches at realistic spacing," and it confirms **A2** at the source rather than by inference — which is what kit-spec §6.2's honorable-fallback category **(iv)** requires G-5 to *state, not infer*.

The premise must be amended from *"the sim's arc hits 1.36 per press vs the fixture's 2.36, so breadth is under-delivered"* to:

> The sim's cone is a hardcoded 90° / 5.0 m primitive; the kit's declared 150° arc and cap-5 are inert. Measured breadth is density-conditional: it **matches or slightly exceeds** the fixture diagnostic at 8-mob density (2.5816 vs 2.362, on an upward-biased denominator) and falls **below** it at 4- and 6-mob spacing (1.5806, 1.1587). No single pooled figure is comparable to §1.1p without a density-composition weighting rule the spec does not supply.

Note the irony worth banking: **gamora's control arm independently confirms keeper (3)'s conclusion by a cleaner route than the number that appeared to contradict it.** hits/press = exactly 1.0000 with A = 2.667 proves breadth is not the A driver, without needing any fixture comparison at all. Her landing is keeper (3)'s best evidence even though her headline number superficially opposes it.

---

## §3 — Rationale

**On the CONDITIONAL PASS.** Discipline #1 is met — the math note preceded the code and named its design choice, its residual (§4), and its declined repair. The control-arm design call (neutralize both actives, hold throughput exactly) is the correct conservative reading and I endorse it. Discipline #10 is met — she measured rather than assumed, and built the second instrument that made her own failure legible. Principle #2 (smoke-gate) is met. The pins are non-vacuous by injection, which is the standard her own door suites set.

**On the BLOCK.** Kit-spec §6.2 grades S-2 as a PRIMARY structural target. An arm whose lever is provably disconnected cannot return a MISS on S-2 — it returns nothing. Reporting `B lift = 1.000` as an S-2 result would bank a **null instrument as a negative finding**, which is the identical defect class gamora herself caught at the smoke gate for the received-side mirror (assembly note §2: *"numbers produced, asserts passed, the comparison never actually run"*). Discipline #8 (schema validation at boundaries) and #10 apply. This is a BLOCK, not a WARN, because the terminal verdict amendment is being written now and would consume the artifact.

**On the math-note corrections.** §3 argues the control's conservatism partly from holding "the charge bleed (810 / 3.0 s)" at canonical value, and §5 lists it among what does not change. The bleed contributes zero damage in either arm. The argument's *conclusion* survives (throughput was held; the field is identical), but a load-bearing component of its *reasoning* is fictional, and a reader will otherwise carry that fiction forward. Discipline #12 requires the semantic shift be named where it lives.

**On the boss-tier losses.** The math note §4 pre-names the conceptual residual ("the control cannot separate breadth-removed from the kill-rate reduction removing breadth causes"). It does not report that the residual materialized as a **10/60 player-death divergence in the one tier that carries the landing's only PASS**. Descriptively that is a material omission from a control-arm landing; prescriptively it must be disclosed before the PASS is cited.

---

## §4 — Action

### BLOCK — must clear before the amendment treats this as evidence

- [ ] **Matt / conductor:** **quarantine `src/reincarnated/simulation/output/kitcal_g5/g5_r3arm/`.** Nothing in it may be cited for **S-2** (DoT-tail lift confined to B) or for any DoT-dependent half of **S-3**. Its `B lift = 1.000` is a null instrument, not a MISS. The S-3 gear-step half (pool 759 → 1607, hazard-shape) is unaffected by this finding and remains readable.
- [ ] **gamora:** amend `simulation/math/g5-s1-control-arm-2026-07-28.md` §3 and §5 — the charge bleed contributes **zero** in this engine; the throughput-identity claim must rest on the direct-damage fields alone.
- [ ] **gamora:** disclose the boss-tier **50/10 vs 60/0** win-rate divergence and the per-tier elapsed-time divergence in the landing record. The S-1 boss PASS may be cited only alongside it.

### WARN — fix advisable before the next lap

- [ ] **gamora:** amend §6a — the sim's press denominator excludes zero-hit presses and is therefore not the fixture's `680`-activation denominator. Name the direction of the bias (sim reads high).
- [ ] **gamora:** name A's absolute-bin anchoring in §4. State the reported coincidence floor as a **lower bound** and establish whether the fixture's `S1-gap5s-v1` clusters by gap or by absolute bin. If the latter differs, the like-for-like claim needs a note.
- [ ] **gamora:** report effective-n on A. Zero variance across 30 seeds means `all_seeds_in_band` is one observation restated 30 times.
- [ ] **gamora:** apply the §7 output-labelling fix to `--r3-arm` (one line in `label`, the same fix already written for `--s1-control`). The r3 report and traces are filename-identical to canonical.
- [ ] **gandalf:** amend efficacy-verdict §4.3 and keeper (3) per §2 above — conclusion stands, premise restated as density-conditional, `max_targets`-is-inert substituted for the pooled-number argument.
- [ ] **gandalf:** carry the verdict's own §7.3 tier-weighting amendment across to **§1.1p**, not just §6.3. Until a density-composition rule exists, no pooled sim hits/press is citable against 2.362.

### ESCALATE to Matt

- [ ] **Architectural:** the DoT-application discard at the `resolve_spatial_hit` projection seam is the **third** instance of the kernel-side-effect-discarded pattern (after O-d leech and the received-side mirror). It is cross-seam (rocket owns generation-side skill effects; gamora owns simulation) and it silently voids `dot` on **every** kit the spatial engine has ever run, not just this fixture. Needs a scoped decision: repair, or document-and-pin as a named engine limitation. Not a one-line edit — the O-d precedent shows a carry-back can double-count.
- [ ] **Decisions-log:** I will file an entry once Matt rules on the above. Candidate title: *"Spatial-engine DoT effects are inert at the projection seam (KIT-CAL-1 G-5 Gate 2)."*

### APPROVED under my ADR-002 authority (no Matt needed)

- The **S-1 control-arm build itself** — within-seam, no consumer API change, tests added, pins non-vacuous. `gamora/v-g5-s1control-1` stands as a tag.
- The **coincidence-floor finding** — independently reproduced and correct. It may be cited by the amendment as-is.
- The **A-S1C-1 / A-S1C-2 pins** — sound, with the §1.3 caveat that A-S1C-1's non-vacuity half asserts on `arc_degrees` / `max_targets`, which are dict fields the engine never reads. The pin still does real work (it blocks flag leakage into the canonical dict); it is not the behavioral guarantee §6's wording implies. Recommend a one-line comment, not a code change.

---

## §5 — References

**Engine (`/Users/admin/Games/reincarnated-engine/`):**
- `src/reincarnated/simulation/math/g5-s1-control-arm-2026-07-28.md` — the math note under review
- `src/reincarnated/simulation/spatial_gauntlet/kitcal_g5_scenarios.py` — `fixture_class_dict`, the `s1_control` mutation
- `src/reincarnated/simulation/spatial_gauntlet/kitcal_g5_harness.py` — `compute_breadth`, `compute_abc`, `assert_s1_control_pins`, `_assert_fight_invariants`
- `src/reincarnated/simulation/spatial_gauntlet/spatial_engine.py:185-189` — the hardcoded geometry constants
- `src/reincarnated/simulation/spatial_gauntlet/spatial_engine.py:1463-1513` — `_compute_cone_hits` / `_compute_line_hits`
- `src/reincarnated/simulation/spatial_gauntlet/spatial_engine.py:5290-5342` — the `_tick_effects` DoT site, gated on `active_effects`
- `src/reincarnated/simulation/spatial_gauntlet/spatial_resolver_adapter.py:388-404` — the side-effect discard seam
- `tests/test_kitcal_g5_harness.py` — 27/27 pass
- `src/reincarnated/simulation/output/kitcal_g5/g5/` — canonical W-c battery (`bef1f55`)
- `src/reincarnated/simulation/output/kitcal_g5/g5_s1control/` — the control battery (`f54c547`)
- `src/reincarnated/simulation/output/kitcal_g5/g5_r3arm/` — **BLOCKED artifact** (`f54c547`)

**Meta-repo (`/Users/admin/Games/reincarnated-collaboration/`):**
- `agentic_orchestration/gandalf/notes/2026-07-28-kitcal1-g5-efficacy-verdict.md` §4.3, §7.2 keeper (3)
- `agentic_orchestration/gandalf/notes/2026-07-28-kitcal1-g4-kit-spec-v2.md` §1.1p, §6.2 (S-1, S-2, S-3)
- `agentic_orchestration/gandalf/notes/2026-07-27-kit-cal-1-run-charter.md` §14.27

**Signed:** jack-ryan, 2026-07-28. Every number in §1 and §2 re-derived independently from the banked traces or by live instrumentation.
