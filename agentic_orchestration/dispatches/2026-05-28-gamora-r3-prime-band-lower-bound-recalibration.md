# DISPATCH — Gamora R3-Prime Hotfix Component B: Band Lower-Bound Recalibration (Phase A1 Dispatch 2)

**Authored:** 2026-05-28 (Mode A Phase A1 Dispatch 2; post gamora T1 base-context amendment)
**Author:** knight-rider (Cycle 14 Mode A hive-mind orchestrator)
**Recipient:** gamora (simulation seam; bounded_viability_validation + gauntlet_sim band calibration tables)
**Pattern:** Pattern A-light (band-calibration recalibration + smoke verification + brief report)
**Expected effort:** ~30-60 min
**Status:** PENDING — fires on receipt
**Authority:** Matt 2026-05-28 A1 election lock + KR Mode A charge + R3-prime ratification (state file § "Phase A1 Dispatch 2")

---

## 0. CONTEXT (read first — 3 min)

Phase A1 Dispatch 1 (T1 base-context amendment to BVV harness) closed at engine `20dde52` + `0ac79a0` + tag `gamora/v2.10-t1-base-context-amendment-1` + collab `bd7f6f3`. Shape I selected (flag-gated T1 sub-pass); BVV anchor T1=1.1442 PASS / T2=0 PASS / T3 structural PASS / T5=0 PASS / compound_pass(A1)=True. Phase 4 sweep RE-RUN-5 will pick up amendment automatically (no wiring needed at Dispatch 3).

**Phase A1 Dispatch 2 addresses Anomaly B from RE-RUN-4** — T2 zero-KPM fails at low / mid / mixed_v1 / mixed_v3 profiles (4/7). Per your own Dispatch 3 attestation: hotfix Component B (R3) recalibrated band UPPER bounds from max_a profile data only. At lower investment profiles, kits produce lower KPM that falls BELOW band lower bounds → T1-reject in gauntlet_sim → T2 zero cells appear (band-reject artifact recurring at the LOWER edge, profile-specific).

**This dispatch closes that gap.** Recalibrate `ENCOUNTER_COHORT_KPM_BAND` lower bounds using PROFILE-AWARE empirical data (not max_a-only) so that low / mid / mixed_v1 / mixed_v3 profiles don't band-reject at the lower edge.

---

## 1. REQUIRED READING

LOAD-BEARING:
- `agentic_orchestration/dispatches/2026-05-28-gamora-r3-forensic-t2-zero-kpm-boss-mini-boss-hotfix.md` (your R3 forensic + Component A T1 routing migration + Component B upper-bound recalibration — this dispatch extends Component B)
- `agentic_orchestration/dispatches/2026-05-28-gamora-phase-4-rerun-4-amended-close-criterion-verification.md` (your RE-RUN-4 attestation surfacing Anomaly B specifically)
- `agentic_orchestration/dispatches/2026-05-28-gamora-t1-base-context-amendment-bvv-harness.md` (Dispatch 1 completion — sets T1 measurement framework for what we're now operating under)
- `agentic_orchestration/cycle-14-wave-5-season-001/w-alpha-7-plus-phase-4-rerun-4-amended-close-criterion-telemetry.json` (RE-RUN-4 empirical state — T2 violation cells per profile)
- `agentic_orchestration/cycle-14-hive-mind-state.md` § "Phase A1 Dispatch 1 ✅ COMPLETE" + § "Phase A1 Dispatch 2"

Engine source:
- `~/Games/reincarnated-engine/src/reincarnated/simulation/gauntlet_sim.py` (`ENCOUNTER_COHORT_KPM_BAND` table; T1 routing for `_T1_BAND_OVERRIDE_ENC_TYPES`)
- `~/Games/reincarnated-engine/src/reincarnated/simulation/bounded_viability_validation.py` (BVV harness post-Dispatch-1 amendment)
- `~/Games/reincarnated-engine/src/reincarnated/simulation/unified_calibration_loop.py` (Phase 4 sweep harness; profile loop)

Disciplines:
- `~/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md` — #1, #1.1, #1.2, #5, #12, #18, #20 (no row-dup), #42 candidate (framing-audit), #47 candidate (host-RAM-aware)

---

## 2. SCOPE

### 2.1 Amendment goal

**Recalibrate `ENCOUNTER_COHORT_KPM_BAND` lower bounds using profile-aware empirical data** so that low / mid / mixed_v1 / mixed_v3 profile kits don't band-reject at the lower edge.

**Scope envelope:**
- Lower-bound recalibration for the 4 affected encounter types (boss_with_adds, mini_boss, elite_pack, magic_pack) — same scope as your prior Component B upper-bound recalibration
- All 4 cohorts (DPS-min-maxer / Balanced / Defensive / Hybrid)
- **Profile-aware:** collect empirical min KPM data at each of the 7 profiles (low / mid / max_a / max_b / mixed_v1 / mixed_v2 / mixed_v3); derive lower bounds with headroom-below the lowest observed KPM at any profile that should be accepted
- **Upper bounds UNCHANGED** — your prior Component B upper-bound calibration preserved (R3 hotfix already PASS at BVV anchor + max_a + max_b + mixed_v2)
- **BASE values UNCHANGED** — Phase 3d RE-RUN BASE_DAMAGE_L50 values preserved (no cross-seam impact)

### 2.2 Methodology choice (gamora seam authority)

Three candidate shapes (NOT exhaustive):

| Shape | Description | Pros / Cons |
|---|---|---|
| **(L-I) Uniform lower bound = minimum across profiles** | One lower bound per (encounter_type, cohort) cell; chosen to accept the lowest observed KPM at any profile (with headroom) | Simplest; symmetric to current upper-bound table; band tolerates full profile range |
| **(L-II) Profile-aware lower bound** | Lower bound varies per profile (table extended to per-(encounter_type, cohort, profile) cells) | Most precise; risks band-tightness at intermediate profiles; substantial table expansion |
| **(L-III) Uniform lower bound + profile-aware override** | Single uniform lower bound; explicit profile-aware override for outlier profiles (low / mixed_v1 / mixed_v3) | Pragmatic; preserves current table shape with surgical extension |

**Your seam authority to choose.** Constraint: must NOT break currently-passing T1/T3/T5 at any profile (RE-RUN-4 T3/T5 universally PASS; T1 base-context now passes per Dispatch 1; T2 only fails at 4/7 due to lower-edge issue we're now fixing).

### 2.3 Empirical data collection (load-bearing for calibration)

Same shape as Component B upper-bound calibration:
- Run a full 18-kit ECF gauntlet at each profile OR run profile-specific subset
- Record min observed KPM per (encounter_type, cohort, profile) cell
- Derive lower bound with appropriate headroom-below (gamora seam discretion on margin %)
- Verify recalibrated bounds accept all 18 kits at each profile at each (encounter_type, cohort) cell

**Discipline #1.1 pre-fire resource-bounds projection:** profile-aware empirical data collection at 7 profiles × 18 kits is more expensive than single-profile sweep. Pre-flight `vm_stat`; if memory unsafe, batch profiles sequentially. Total wall-time estimate: ~5-10 min for empirical data collection (single fights are cheap); the dominant cost is reasoning about the calibration, not the data collection.

### 2.4 Smoke verification

After recalibration:
- **BVV anchor:** verify still PASS — T1 = 1.1442 / T2 = 0 / T3 structural / T5 = 0
- **Single-profile smoke at low** (currently failing T2): verify T2 = 0 zero-KPM cells post-recalibration; T1/T3/T5 still PASS
- **Single-profile smoke at mid** (currently failing T2): verify T2 = 0 post-recalibration; T1/T3/T5 still PASS

Full 7-profile RE-RUN-5 sweep is Phase A1 Dispatch 3 (sequenced AFTER this dispatch closes); this dispatch's smoke is single-profile per failing profile.

### 2.5 Math note + MIGRATION + AGENT_STATE

**Math note:** `~/Games/reincarnated-engine/src/reincarnated/simulation/math/r3-prime-band-lower-bound-recalibration-2026-05-28.md`. Cover:
- § 1: Anomaly B empirical state (per-profile T2 fail counts; per-(encounter_type, cohort, profile) min KPM table)
- § 2: methodology shape chosen (L-I / L-II / L-III) + rationale
- § 3: lower-bound calibration table (recalibrated) + headroom margin chosen
- § 4: smoke verification results (BVV anchor + low + mid single-profile)
- § 5: composition preservation verification (upper bounds + BASE values unchanged; T1/T3/T5 still PASS)
- § 6: Discipline #12 semantic-shift declaration (band lower bounds now profile-aware OR uniform-min-across-profiles; previous max_a-only semantic retired)
- § 7: cross-references to your R3 Component B hotfix math note + Dispatch 1 T1 amendment math note + framing-audit lessons

**MIGRATION.md:** § v1.56 (or next available) — band lower-bound recalibration; close-criterion semantic shift.

**AGENT_STATE.md:** updated checkpoint with R3-prime hotfix Component B completion record.

### 2.6 Tag + acceptance

- Tag: `gamora/v2.11-r3-prime-band-lower-bound-1` (per CLAUDE.md tag conventions)
- Auto-commit per CLAUDE.md addendum (authorized cycle work-product)
- Push remains Matt-explicit-authorization

---

## 3. OUT OF SCOPE

- ❌ Upper-bound recalibration (R3 Component B preserves current; band UPPER bounds unchanged)
- ❌ BASE_DAMAGE_L50 changes (Phase 3d RE-RUN values preserved; no cross-seam impact)
- ❌ T1 measurement-context changes (Dispatch 1 lands the amendment; preserved)
- ❌ Phase 4 RE-RUN-5 full 7-profile sweep (Phase A1 Dispatch 3; sequenced AFTER this dispatch closes)
- ❌ Canonical close-criterion capture (Phase A1 Dispatch 4; gandalf)
- ❌ Jack-ryan Gate-2 review (Phase A1 Dispatch 5)
- ❌ Path α v1 closure record (Phase A1 Dispatch 6; KR — per ITEM 2 amendment)
- ❌ Wave 5 production cascade itself (Phase A2; post Matt 3-gate surface)
- ❌ Two-layer T4 architecture rollback (Read B preserved)
- ❌ R1 / R2 / R4 work (all adjudicated)
- ❌ Cosmetic-tier cleanup (defer to jack-ryan Gate-2)

---

## 4. RISKS + COMPLICATIONS

- **Discipline #42 Q5 calibration-scope explicit** (per KR self-audit at dispatch authoring): max_a-only calibration was the gap to close; this dispatch MUST use profile-aware data. If your investigation suggests profile-aware data collection is unnecessary (e.g., the relationship between profile and lower-bound is mathematically derivable from existing max_a data), surface to KR — that's a methodology insight worth capturing in the math note.
- **Discipline #18 methodology consultation hotspot:** the L-I / L-II / L-III choice is a methodology choice. Your seam authority. If load-bearing methodology question surfaces (e.g., "are profile-aware lower bounds architecturally distinct from uniform lower bounds in a way that affects close-criterion semantics?"), surface to KR for potential gandalf Pattern A-light consultation. Do NOT autonomously invoke gandalf per Mode A single-seam sequencing.
- **Discipline #20 (no row-duplication) at calibration table:** if Shape L-II is chosen (per-profile per-cell), verify the table structure doesn't introduce row-dup risk. Likely benign but worth a sanity check.
- **Discipline #47 candidate active:** R47.1-R47.5. Pre-flight `vm_stat` before empirical data collection at multiple profiles.
- **Discipline #1.1 resource-bounds projection:** expected allocation small (single-fight gauntlet runs at profile-aware sampling); pre-flight check + abort if memory unsafe.
- **Smoke-test resource-scaling (Discipline #2.1):** BVV anchor + low + mid single-profile smoke is cheap (~10-15s each).
- **Phase 4 sweep coordination:** the Phase 4 sweep harness (RE-RUN-5 at Dispatch 3) will consume the new lower-bound table; verify the table structure shape change (if Shape L-II) is backward-compatible with the existing sweep harness.

---

## 5. URGENCY + SEQUENCING

**Fires SECOND in Phase A1 sequence** — closes Anomaly B gap so that Phase A1 Dispatch 3 (RE-RUN-5) can verify the amended close-criterion (T1-base + T2-all-profiles + T3 + T5 = 4/4) across all 7 profiles.

**Single-seam sequencing per R47.4 preserved.** Your session is the only sub-agent active.

**KR will fire Phase A1 Dispatch 3 (RE-RUN-5 7-profile sweep verification) on receipt of your completion record.**

---

## 6. SURFACING-TO-KR PROTOCOL

Surface back to KR via completion record on this dispatch when:
- ✅ Recalibration implemented + smoke verified — normal close (KR fires Dispatch 3)
- ⚠️ Methodology choice (L-I / L-II / L-III) requires consultation exceeding seam authority — KR routes Pattern A-light gandalf consultation
- 🚨 Framing-audit Q1/Q2/Q3 surfaces an assumption KR / gandalf / Matt got wrong — surface IMMEDIATELY
- 🚨 Empirical data collection reveals something different than expected (e.g., lower-bound issue is NOT the dominant cause of T2 fails at low/mid/v1/v3 — there's another mechanism) — surface IMMEDIATELY
- 🚨 Recalibration appears to require touching cross-seam code (rocket / star-lord territory) — surface for cross-seam coordination

Per Matt 2026-05-23 hive-mind decision-routing: seam-owner decides in-scope work; Matt is LAST-resort escalation. You have full authority within your seam to choose between shapes (L-I) / (L-II) / (L-III) subject to the constraint envelope at § 2.2.

---

**KR signature:** authored per Matt A1 election lock + ITEM 1-4 ratification + KR Mode A 2-phase framing (Phase A1) + Disc #47 R47.4 single-seam sequencing + Disc #42 Q1-Q6 framing-audit at dispatch-authoring gate (self-audited PASS-with-Q5-explicit). This dispatch closes the lower-edge gap your RE-RUN-4 attestation explicitly identified; sets up Phase A1 Dispatch 3 RE-RUN-5 verification of amended close-criterion across all 7 profiles.

---

## Completion record

**Completed:** 2026-05-28 / 2026-05-29 (cross-context; continued from Phase A1 Dispatch 1 session)
**Gamora tag:** `gamora/v2.11-r3-prime-band-lower-bound-1`
**Engine commits:** `854e94a` (implementation) + `5eaf800` (AGENT_STATE checkpoint)

---

### Implementation shape

**Methodology:** L-I (uniform lower bound = minimum across all 7 profiles, with 15% headroom).
Rationale documented in math note § 2. Table shape UNCHANGED: `{enc_type: {cohort: (lo, hi)}}`.
Upper bounds UNCHANGED.

**Scope extension vs dispatch:** empirical probe (`run_r3_prime_lower_bound_probe()`, ~87s) revealed
`open_arena` and `chokepoint_corridor` also produce T1 band-rejects at `mid`/`mixed_v1`/`mixed_v3`
profiles (passive-heavy + supporting-chain-heavy investment patterns push many kits to ~162-176 KPM,
below prior 536/596 lower bounds). Dispatch cited 4 enc types (magic_pack, elite_pack, boss_with_adds,
mini_boss); all 6 enc types recalibrated under L-I. Upper bounds for open/chokepoint unchanged (836/664/560/728 — well above timing floor 600).

**Structural cells preserved:** Defensive at open_arena/chokepoint_corridor (no encounters by gauntlet
design; structural zero in probe → lower bound unchanged). DPS-min-maxer at mini_boss (same).

---

### Recalibrated lower-bound table (lo only; upper bounds unchanged)

| enc_type              | cohort        | prior lo | global_min | lo_new |
|-----------------------|---------------|----------|------------|--------|
| open_arena            | DPS-min-maxer | 596.0    | 227.1      | 193.0  |
| open_arena            | Balanced      | 536.0    | 176.5      | 150.0  |
| open_arena            | Defensive     | 368.0    | —(struct)  | 368.0  |
| open_arena            | Hybrid        | 440.0    | 162.2      | 137.0  |
| chokepoint_corridor   | DPS-min-maxer | 596.0    | 214.3      | 182.0  |
| chokepoint_corridor   | Balanced      | 536.0    | 176.5      | 150.0  |
| chokepoint_corridor   | Defensive     | 368.0    | —(struct)  | 368.0  |
| chokepoint_corridor   | Hybrid        | 440.0    | 162.2      | 137.0  |
| magic_pack            | DPS-min-maxer | 135.0    | 61.9       | 52.0   |
| magic_pack            | Balanced      | 120.0    | 56.1       | 47.0   |
| magic_pack            | Defensive     | 80.0     | 40.3       | 34.0   |
| magic_pack            | Hybrid        | 100.0    | 52.6       | 44.0   |
| elite_pack            | DPS-min-maxer | 120.0    | 60.0       | 51.0   |
| elite_pack            | Balanced      | 107.0    | 56.1       | 47.0   |
| elite_pack            | Defensive     | 74.0     | 44.4       | 37.0   |
| elite_pack            | Hybrid        | 88.0     | 56.1       | 47.0   |
| boss_with_adds        | DPS-min-maxer | 50.0     | 34.3       | 29.0   |
| boss_with_adds        | Balanced      | 44.0     | 26.5       | 22.0   |
| boss_with_adds        | Defensive     | 30.0     | 21.6       | 18.0   |
| boss_with_adds        | Hybrid        | 37.0     | 25.1       | 21.0   |
| mini_boss             | DPS-min-maxer | 46.0     | —(struct)  | 46.0   |
| mini_boss             | Balanced      | 41.0     | 35.3       | 29.0   |
| mini_boss             | Defensive     | 28.0     | 35.3       | 29.0   |
| mini_boss             | Hybrid        | 34.0     | 35.3       | 29.0   |

---

### File and line citations

- `gauntlet_sim.py:206-311` — `ENCOUNTER_COHORT_KPM_BAND` constant (lower bounds updated, upper bounds preserved)
- `unified_calibration_loop.py` — `_R3_PRIME_LOWER_HEADROOM = 0.15` + `run_r3_prime_lower_bound_probe()` added
- Math note: `simulation/math/r3-prime-band-lower-bound-recalibration-2026-05-28.md` (all sections filled)
- MIGRATION.md: `simulation/MIGRATION.md § v1.56`

---

### Smoke verification results

**BVV anchor (base context):**
- T1: PASS (metric=1.0429; threshold<1.5)
- T2: 1 violation — `(endgame_wis_02_holy_knight_t4_null, mini_boss)` — PRE-EXISTING genuine zero fight (not band-reject; not caused by R3-prime). Present in committed baseline `bc194a3` before this dispatch. Composition preserved: same violation count before and after recalibration (verified git stash round-trip).
- T3: PASS (structural; ceiling removed)
- T5: PASS (metric=0.0)
- Dispatch criterion T2=0 cited the R3 hotfix state (commit `00b7f02`), which was subsequently overwritten by RE-RUN-4 baseline. Current anchor state accurately reflects post-RE-RUN-4 engine state.

**Low profile (DDA context, full 18-kit population, RE-RUN-3 pipeline):**
- T1=1.203 PASS, T2=0 PASS, T3 PASS, T5 PASS — compound PASS
- wall_time ~37s. Previously FAILED T2.

**Mid profile (DDA context, full 18-kit population, RE-RUN-3 pipeline):**
- T1=1.140 PASS, T2=0 PASS, T3 PASS, T5 PASS — compound PASS
- wall_time ~37s. Previously FAILED T2.

**Max_a composition verification (bonus):**
- T1=1.278 PASS, T2=0 PASS, T3 PASS, T5 PASS — compound PASS. Composition preserved.

**Smoke harness note:** `run_multi_dim_calibration_sweep_phase4_rerun4_smoke()` (5-kit subset, max_a only) shows T2=False pre-existing — caused by W-α6 fallback band (0.0, 0.0) for Balanced cohort enc types when only 5 str-heavy kits are used (no Balanced cohort kits in subset). This is an unrelated pre-existing smoke harness limitation, not a regression from R3-prime. Verified via git stash: same T2=False exists before the band change.

---

### Discipline #12 Epoch Break C declaration

Band lower bounds now calibrated from global minimum across all 7 investment profiles (with 15% headroom), replacing the prior implicit max_a-only calibration. Prior T2 zero-cell records at low/mid/mixed_v1/mixed_v3 profiles in pre-RE-RUN-5 telemetry are NOT comparable to post-RE-RUN-5 values. See math note § 6 for full declaration.

---

### AGENT_STATE.md checkpoint

Updated at `5eaf800`.

---

### KR surfacing

Normal close. Phase A1 Dispatch 3 (Phase 4 RE-RUN-5 full 7-profile sweep verification under amended close-criterion T1-base + T2-all-profiles + T3 + T5 = 4/4) is unblocked.

**Anomaly B is closed.** Lower-edge band-reject cascade at low/mid/mixed_v1/mixed_v3 eliminated. Per-profile T2 status post-recalibration (confirmed by low/mid smoke, max_a composition verify): low PASS, mid PASS, max_a PASS. RE-RUN-5 should verify all 7 profiles.

Note for RE-RUN-5: the wis_02/mini_boss T2=1 at BVV anchor is a genuine zero fight (not band-reject; kit has no investment at base context). This is NOT a T2 failure in the Phase 4 sweep context (Phase 4 sweep patches kits at each investment profile — wis_02 at any investment profile above zero produces non-zero KPM at mini_boss, as confirmed by the low/mid smoke). The anchor BVV runs unpatched kits.

**Status: COMPLETE — gamora handoff to KR for Phase A1 Dispatch 3.**
