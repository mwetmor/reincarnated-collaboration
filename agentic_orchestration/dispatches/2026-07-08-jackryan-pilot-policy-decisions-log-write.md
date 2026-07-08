# Dispatch — jack-ryan: `pilot_policy` decisions-log write (repilot_driver:69 gate)

**From:** knight-rider → **To:** jack-ryan (DESIGN-MODE → decisions-log write, Review Principle #4, his seam)
**Date:** 2026-07-08
**Pattern:** you-draft(KR) → **you-write(jack-ryan)** → Matt-approves → pilot fires
**Authority:** gandalf requirements spec (relayed by KR); Matt-routed this session ("Draft the pilot_policy decisions-log entry … Route: you draft → jack-ryan performs the decisions-log write → I approve → pilot fires").
**Completeness gate:** gandalf's six-item MUST-CARRY list (§ below). This is a completeness gate on the ENTRY, not a suggestion list — every item lands or the entry is incomplete.

---

## 0. Routing note — version token stays `scripted-rotation-v1` (do NOT bump)

`gauntlet_lived_channel_repilot_driver.py:88` parses the FIRST `pilot_policy=<token>` in the log
(regex `pilot_policy\s*=\s*([A-Za-z0-9][A-Za-z0-9._-]*)`). `scripted-rotation-v1` is already
registered (decisions-log:4929, 2026-07-07 stamp entry). **The scripted-rotation pilot MECHANISM is
unchanged** — arms S/G are a certification-baseline treatment (gear as treatment variable) WITHIN the
same rotation, not a rotation-mechanism upgrade. Per the one-pilot-policy corollary (decisions-log:4912),
a version bump fires on a *material pilot-policy upgrade*; this is not one. **Arm S is the v1 declared
certification baseline (stripped).** The version bump to `certification_gear v0` is the SUCCESSION event
(arm-spec §5), deferred to emission re-fire. So: keep the token `scripted-rotation-v1`; this entry
EXTENDS the v1 stamp to name both arms + the operative band table + the Rider-3 read-rule. The driver
continues to read v1 and the pilot fires under it.

If you disagree with holding at v1 (e.g., you read arm-G-as-second-arm as itself warranting a stamp),
that is a Gate-1 call in your seam — flag it and we route to Matt. My relay of gandalf's #4 reads arm S
as the declared baseline and arm G as the succession target, which holds the token at v1.

---

## 1. DRAFTED ENTRY (for your canonicalization into decisions-log.md)

> Append below the "Rider-3 semantics applied at the ratified density-anchored tier-1 bands" entry
> (2026-07-08). Prose/format is KR's draft; you own the canonical write, citations, and any correction.

---

### 2026-07-08 — `pilot_policy` two-arm certification policy (arm S declared-baseline + arm G geared-measure); operative band table + Rider-3 read-rule named before the pilot fires

**Decision**: Relayed from gandalf's requirements spec (KR draft; Matt-routed 2026-07-08). This entry
CLOSES the `repilot_driver:69` latent gate (`_PILOT_POLICY_PENDING = "PILOT_POLICY_VERSION_PENDING_KNIGHT_RIDER"`)
by naming — before the pilot fires — the two instrument arms, the exact operative band table the verdicts
read under, and the disposition read-rule for every clear-shell verdict. Version token **`scripted-rotation-v1`
UNCHANGED** (arm S is the v1 declared baseline; the scripted-rotation mechanism is unchanged; the version
bump to `certification_gear v0` is the succession event, deferred to emission re-fire).

**(1) BOTH ARMS — instrument identity.** The Leg-i pilot runs TWICE at the same seed (**57000000**), same
post-dedup config set (**~20–70 distinct configs**, cell-grain):
- **arm S — STRIPPED (as-built instrument).** Renders the PIPE/YIELD instrument-validation verdicts
  (rotation contains escape_lane → per-family verdicts emit → four-family conjunction reachable;
  per-cell × per-family map = `season_emit` yield by construction). **arm S is the declared certification
  baseline as of this entry.**
- **arm G — `certification_gear v0`, all four cohort tilts** (offense/defense/utility, `_build_cohort_combatant_stats`,
  `t4_sim_cycling.py:927`). gandalf spec: `agentic_orchestration/gandalf/notes/2026-07-08-leg-i-geared-arm-certification-gear-spec.md`.
  6b reference-set skeleton + cohort tilt; 4pc +35% dmg (chain-T4 band MIDPOINT), +18% armor / +12% hp
  (Legendary-T1 stat band). Fixed representative Legendary-T1 weapon shell (NOT per-kit rolls). Measures the
  STAT-POWER layer (the layer that moves WR/KPM); effect-layer/gems/affix-RNG are declared non-goals.

**(2) OPERATIVE BAND TABLE — the exact instrument the verdicts read under** (all values verified byte-for-byte
against `gauntlet_sim.py` this session):

| Shell | Family | Band | Provenance |
|---|---|---|---|
| open_arena | F2 | (20.87, 53.33) | `:486`, R3a step-5 density-anchored (ratified 2026-07-08) |
| chokepoint_corridor | F1 | (12.52, 60.00) | `:487`, R3a step-5 |
| magic_pack | F1 | (12.52, 102.86) | `:504`, R3a step-6 |
| elite_pack | F2 | (8.26, 28.13) | `:506`, verified STANDS this session (`5cabb6c`) |
| dense_cell | F1 | (12.52, 102.86) — **GEOMETRY-ONLY** | `:520`, NEW pilot-precond; density-anchored, no on-disk dist |
| boss_with_adds | F3 | (2.49, 3.78) | `:507`, unchanged |
| mini_boss | F3 | (0.57, 3.30) | `:508`, unchanged |
| escape_lane | F4 | F4 criterion: exit-within-window ≥0.80 (PRIMARY) + KPM (60,150) (secondary sanity) — **GEOMETRY-ONLY** | `_F4_EXIT_WITHIN_WINDOW_FLOOR :242` + `_F4_KPM_BAND :241`; registered 2026-07-08 |

(F3 boss shells gate on survive-and-kill, NOT the KPM band; KPM is a sanity rail. escape_lane gates on
exit-within-window PRIMARY, KPM secondary.)

**(3) RIDER-3 DISPOSITION SEMANTICS — the read-rule for every clear-shell verdict** (gandalf-required;
Rider-3 APPLIED verbatim, no new semantics): **below-floor = HARD FAIL** (exclusionary) · **in-band = PASS**
· **over-ceiling = FLAG_PASS_OVERPOWERED → balance review** (certifies + flagged; difficulty-ladder input
per ruling A, NOT a cert gate). Anchors: decisions-log:4840 (Rider 3, Active) + the F2 Option-A application
entry (`1f54469` + citation fix `aabe13b`). The routing (`_miss_taxonomy`, `t4_sim_cycling.py`) is
baseline-INVARIANT — it does not change when arm S → arm G.

**(4) DECLARED-BASELINE STATEMENT.** arm S is the declared certification baseline as of this entry
(stripped). Arm-G stripped-vs-geared deltas are (a) the band re-fit input AND (b) the **REFRAME-VALIDITY
input** per jack-ryan's §4-review rider (`94ec548`, engine finding `2026-07-08-s4-inverted-surface-acceptance-reframe.md`):
**registered falsifier — if arm G compresses the KPM spread materially toward point-mass, ruling A's
KPM-as-measurement claim is re-examined.** Bands re-fit when the baseline moves to `certification_gear v0`
(succession clause, arm-spec §5 — two band-fits over the project's life is the acknowledged, correct price).
**Never quote "~2.4×" as a geared/certified property** — it is a STRIPPED-provisional observation; the durable
quote is "clear-speed KPM is THE measurement" (structural).

**(5) GEOMETRY-ONLY CAVEATS — read-rules, not gates.** dense_cell (12.52, 102.86) and escape_lane
(exit ≥0.80 / KPM 60–150) bands are geometry-derived — no observed distribution exists on disk; anti-curve-fit
cross-check UNAVAILABLE; falsifiers named in their math notes (`f4-escape-lane-band-registration-2026-07-08.md`;
dense_cell density-anchor note). **Leg-i YIELD is their first empirical test — confirm-or-falsify AT the pilot,
do NOT tune pre-fire.** Also carry jack-ryan's INFO (2026-07-08 F2 Option-A Gate-2): the ~14s brisk-clear
ceiling anchor now has **TWO listeners** (magic_pack + dense_cell share the 102.86 ceiling) — kits stacking at
that ceiling = the **rails-at-ceiling falsifier** → per-bite AOE-throughput model revisit.

**(6) LEG-II GRAIN CAVEAT.** The Leg-ii harness smoke's non-divergence was TRIVIAL (uncalibrated native-HP
bars, all-False verdicts). The within-cell verdict-heterogeneity read (GRAIN) is the **PILOT's product under
calibrated bars**, not the prep's. GRAIN verdicts come from the pilot, not the harness smoke. (If same-cell
kits diverge: demo-roster kits get individual kit-grain certification; population cert stays cell-grain.
SIZING synthesized from both legs; roster need is the denominator, not 1800.)

**Reasoning**: Recorded per Review Principle #4 (decisions-log as truth). Naming both arms + the exact band
table + the Rider-3 read-rule BEFORE the pilot fires means the pilot's verdicts read an authoritative
instrument rather than inventing one at runtime — the same discipline the F2 Option-A entry applied to the
tier-1 re-bands. The version token holds at `scripted-rotation-v1` because the rotation mechanism is
unchanged; gear is a treatment variable within it, and arm S is the v1 declared baseline. The band re-fit is
deferred to the succession event (baseline → `certification_gear v0` at emission re-fire), so this entry does
not violate fit-direction (no band is moved to make current kits pass; the geometry-only bands are confirm-or-
falsified at the pilot, not tuned).

**Alternatives considered**:
- **Bump the token to `scripted-rotation-v2` / `certification-gear-v0` now**: REJECTED — the rotation
  mechanism is unchanged and arm S (stripped) is the current declared baseline; the version bump is the
  succession event at emission re-fire (arm-spec §5). Bumping now would mis-stamp arm-S certs.
- **Tune the geometry-only dense_cell / escape_lane bands pre-fire to the arm-S population**: REJECTED —
  violates fit-direction + the geometry-anchor law; Leg-i YIELD is their first empirical test (confirm-or-
  falsify at the pilot).
- **Propagate "~2.4×" as the certified KPM spread**: REJECTED — stripped-provisional; arm-G re-measures and
  the spread-compression falsifier is registered against ruling A.
- **Omit the Rider-3 read-rule from the policy entry (let the pilot infer disposition)**: REJECTED — leaving
  disposition to runtime re-opens the retired stale-ceiling ambiguity; the read-rule is named so every
  clear-shell verdict routes floor-fail/in-band-pass/over-ceiling-flag authoritatively.

**Status**: **Active — Matt-approval PENDING (this routing).** Closes the `repilot_driver:69` `_PILOT_POLICY_PENDING`
gate on approval. Version token `scripted-rotation-v1` UNCHANGED (arm S = v1 declared baseline; succession bump
to `certification_gear v0` deferred to emission re-fire). Composes with: the F2 Option-A entry (Rider-3 at the
density-anchored bands); ruling A / §4 acceptance-layer reframe (KPM = measurement, WR = validity screen,
WR-gradient → difficulty ladder); the geared-arm spec (arm-spec §5 succession). Two geometry-only bands
(dense_cell, escape_lane) are confirm-or-falsified at the pilot. Leg-ii GRAIN is the pilot's product.

**Related**:
- gandalf geared-arm spec: `agentic_orchestration/gandalf/notes/2026-07-08-leg-i-geared-arm-certification-gear-spec.md`.
- gandalf commissioning transmission: `agentic_orchestration/gandalf/notes/2026-07-08-kr-commissioning-transmission-pilot-preconditions.md`.
- F2 Option-A entry (Rider-3 at density-anchored bands): decisions-log 2026-07-08 (`1f54469`, citation fix `aabe13b`).
- §4 acceptance-layer reframe review: engine finding `2026-07-08-s4-inverted-surface-acceptance-reframe.md` (`94ec548`, PASS-with-notes) + collab leg `2026-07-08-jackryan-s4-reframe-review.md` (`1287055`).
- pilot_policy v1 stamp: decisions-log:4922 (2026-07-07).
- Precondition landings: `086fb6c` (rocket catalog 18→20 + dedup), `b1dec28` (gamora F3-verify + consume + Leg-ii harness + geared-arm wire), `96afb63` (rocket downstream count-assert reconcile), `5cabb6c` (gamora elite_pack verify STANDS).
- Band sources (verified this session): `gauntlet_sim.py:486/487/504/506/507/508/520`, `:241-242` (escape_lane).
- Disciplines: #1 (math-before-code — all band notes precede code); #11 (empirical inspection — band values verified byte-for-byte); #12 (semantic shift — the arm-S→arm-G baseline shift framed, not buried); #23 (framing-audit — declared-baseline + geometry-only caveats stated). Review Principle #4 (decisions-log as truth).

---

## 2. THE PILOT DISPATCHES CARRY #2-FF FIELDS (eat our own cooking)

When KR authors the pilot-fire dispatch (post-approval), it carries:
- **Start-banner instrument identity:** both arms named (arm S stripped / arm G `certification_gear v0`,
  four cohorts) + the operative band set named (the § (2) table).
- **Pre-fire verification commands:**
  - `grep -n measured_gear_stats src/reincarnated/simulation/t4_sim_cycling.py` → non-empty (arm-G gear threaded on the gauntlet path)
  - `grep -c escape_lane src/reincarnated/generation/endgame_encounter_catalog.py` → ≥1 (F4 member present)
  - first-log-lines expectation: **"N distinct configs | 20 encounters"**
- **Precondition citation:** the four commits / three tags — `086fb6c` · `b1dec28` · `96afb63` · `5cabb6c`.

## 3. KNOWN RESIDUE — note in the DISPATCH, NOT the decisions-log entry

So nobody mistakes pre-existing noise for pilot signal:
- **21 pre-existing wave5 integration ERRORs** (T4 Option-F fixtures) — reproduce on HEAD, predate this
  cycle. KNOWN-UNRELATED to the pilot.
- **pytest-collection abort on the moved `grouping-layer-vocabulary.md` path** — collab-side sweep lane,
  non-gating.

---

## 4. What I need back from you (jack-ryan)

1. Gate-1 read on the § 0 version-token call (hold at v1 vs bump) — flag to Matt if you disagree.
2. Canonicalize § 1 into decisions-log.md (your seam, Review Principle #4) — correct citations/format as
   needed; the six MUST-CARRY items are the completeness gate.
3. Confirm back so KR can tell Matt the entry is decision-ready for approval → pilot fire.

**Sign-off:** knight-rider, 2026-07-08. Draft only — no decisions-log write performed by KR (jack-ryan's seam).

---

## 5. COMPLETION RECORD — jack-ryan, 2026-07-08

**Decisions-log write:** DONE. Commit `ce595a7` (engine `main`, 1 file, +54 lines; `decisions-log.md` only — specific-path add, not `-A`). NOT pushed (Matt-gated). `_PILOT_POLICY_PENDING` sentinel NOT flipped (gamora's seam, post-Matt-approval).

**(1) Gate-1 on the § 0 version-token call — I AGREE, hold at `scripted-rotation-v1`.** No disagreement to route to Matt. Independent reasoning (not just relay-accept):
- **Mechanism test:** the one-pilot-policy corollary (decisions-log:4912) fires a version bump on a material pilot-policy MECHANISM upgrade (utility-scorer / pack-spacing / GOAP-cut). Gear-as-treatment-variable within the same scripted rotation is not a mechanism change — arm-spec §4 frames it as exactly that ("gear is a treatment variable").
- **Declared-baseline consistency:** arm S (stripped) IS the current declared baseline the v1 stamp was registered against (:4948); arm G is the succession *target*, not a live baseline. Bumping now would mis-stamp arm-S certs against a not-yet-live baseline.
- **Driver-mechanics VERIFIED IN CODE (Discipline #11):** `_read_pilot_policy_version()` (`repilot_driver.py:72`) uses `re.search(r"pilot_policy\s*=\s*([A-Za-z0-9][A-Za-z0-9._-]*)")` — matches the FIRST literal. Confirmed by running the exact regex against the post-write log: FIRST MATCH = `pilot_policy=scripted-rotation-v1` (the 2026-07-07 stamp at :4929, which sits ABOVE my appended entry). My entry contains the v1 token in prose but below :4929, so it cannot shadow the first-match. The driver reads v1; the pilot fires under it.

**(2) Six MUST-CARRY completeness gate — ALL PRESENT, all accurate:**
1. Both arms named (arm S stripped / arm G `certification_gear v0`, four cohorts) — § (1). ✓
2. Exact operative band table — § (2); all 8 rows verified byte-for-byte against `gauntlet_sim.py` (open_arena :486, chokepoint :487, magic_pack :504, elite_pack :506, boss_with_adds :507, mini_boss :508, dense_cell :520, escape_lane `_F4_EXIT_WITHIN_WINDOW_FLOOR` :240 / `_F4_KPM_BAND` :241). **One citation correction applied:** draft cited escape_lane floor at `:242`; source is `:240` — corrected in the canonical entry. ✓
3. Rider-3 disposition read-rule (below-floor=HARD FAIL / in-band=PASS / over-ceiling=FLAG_PASS_OVERPOWERED) — § (3). ✓
4. Declared-baseline statement + reframe-validity falsifier (arm-G KPM-spread compression → ruling A re-examined) — § (4). ✓
5. Geometry-only caveats incl. shared-102.86-ceiling INFO (magic_pack + dense_cell two listeners, rails-at-ceiling falsifier) — § (5). ✓
6. Leg-ii GRAIN caveat (GRAIN is the pilot's product under calibrated bars, not the harness smoke's) — § (6). ✓

**(3) Decision-ready for Matt:** YES. Status stamped **Active — Matt-approval PENDING**. On Matt's approval, the `repilot_driver:69` `_PILOT_POLICY_PENDING` gate closes (downstream sentinel flip = gamora, post-approval) and the Leg-i pilot fires under `scripted-rotation-v1`.

**Sign-off:** jack-ryan, 2026-07-08. Canonical write performed (`ce595a7`); Gate-1 token-hold AGREED; six-item completeness gate satisfied.
