# Post-Mortem — the 1800-Candidate Emission Fire (Mis-Instrumented; Matt-Killed)

**Author:** gandalf (DRIFT-CRITIC on my own run-authorization — the conflict seam is the point)
**Date:** 2026-07-08
**Incident window:** 13:28:58 → 14:56:27 (~88 min; Matt kill on PID 43779)
**Consumes:** live-run log + source verification (this session); four-family pilot verdicts;
`2026-07-08-s4-inverted-surface-acceptance-reframe.md` §6 (the chain the fire violated).
**Routing:** Matt (record) · KR (pilot sequencing) · star-lord (driver re-point investigation) ·
jack-ryan (companion amendment proposal — separate doc, same date).
**Disciplines:** #2 (smoke-before-full-regen — the violated one), #11 (empirical inspection),
#12 (semantic-shift honesty), #23 framing-audit (OP §4.1 — the un-run checklist).

> **⚠ CORRECTED SAME-DAY — read §8 before citing §2/§3/§6.** star-lord's forensic refuted this
> note's mechanism claim ("legacy gate instead of family-cert"); gandalf source re-verification
> confirms the refutation AND confirms the conclusion (season_emit = 0 by construction) via the
> true mechanism: the fought encounter catalog contains **zero escape_lane rooms** — the F4
> criterion was registered in the judge, the room was never added to the rotation. §8 carries
> the retraction, the corrected diagnosis, the dedup-contract finding, and the revised pilot.

---

## TL;DR

- The 1800-candidate emission run (`w3_emission_driver --dry-run-flavor --seed 57000000`) was
  **mis-instrumented**: its step-4 gauntlet is the **legacy 18-encounter catalog** (survivor
  criterion ≥9/18), not the four-family certification. **F4's only member shell (`escape_lane`)
  was absent from the encounter set — the four-family conjunction was unsatisfiable by
  construction**, regardless of kit quality.
- Pace was ~1.67 min/candidate → **~50 h projected**, not "a few more hours." Matt killed it at
  ~88 min (~50 candidates processed; nothing downstream consumes the partial log).
- **Root cause is my transmission, not the architecture and not a misread.** The (B) rider named
  a verdict criterion but named no instrument and gated on no pilot result. The executor ran
  exactly what was written.
- Remedies: Discipline #2 amendment proposal (companion doc) · driver re-point gap on the engine
  tracker (star-lord) · **stratified pilot re-fire queued** behind five named gates (§6).

---

## §1 — Incident record

- **Command:** `python -u -m reincarnated.export.w3_emission_driver --dry-run-flavor --seed 57000000 --log-level INFO` (PID 43779, started 13:28:58).
- **Log:** `src/reincarnated/output/f4_realcand_season_emit/f4_realcand_run_20260708_132858.log`
  (2.95 MB at kill; final line 14:56:27).
- **Measured pace:** 46 distinct candidates in 77 min = **1.674 min/candidate** → 1800 ≈ **50.2 h**.
- **Kill:** Matt, in-session, on my recommendation after verification. Confirmed dead; partial
  log has no downstream consumer; the ~50 processed candidates are discarded at zero cost.
- **Prior state the fire ignored:** the four-family pilots had NOT passed —
  F1 healthy (25/40 martial + 2/2 caster) · F2 8/40 with 32 over-band ceiling misses
  (flag-pass ruling OPEN) · F3 BLOCKED (boss_damage_scale rank-deficiency STOP) ·
  F4 martial wholesale FAIL (median 23.7 vs floor 60; casters 71.8 pass).

## §2 — Verification evidence (Discipline #11)

1. **Log scenario inventory (complete):** `chokepoint_corridor` ×1086 · `open_arena` ×1175 ·
   `escape_lane` / `dense_cell` / `boss_with_adds` / `elite_pack` / `mini_boss` / `magic_pack`
   **×0**. All warnings were WR=1.000 ceiling-saturation (WP-R2-A-2 class).
2. **Source (structural, not sampling):** driver step-4 → `run_gauntlet_sim` →
   `w5g0_gauntlet_setup` → legacy catalog, `GAUNTLET_ENCOUNTER_COUNT_EXPECTED = 18`
   (`gauntlet_sim.py:109`); survivor criterion "≥9/18 per kit" (`w3_emission_driver.py:505`).
3. **The family machinery exists and is bypassed:** `_FAMILY_SHELLS` (`gauntlet_sim.py:264-269`)
   defines F1 {dense_cell, chokepoint_corridor, magic_pack} · F2 {open_arena, elite_pack} ·
   F3 {boss_with_adds, mini_boss} · F4 {escape_lane}; certification = ≥1 passing member per
   family, all four families. The driver never invokes this pass. The run touched *members* of
   F1/F2 but under legacy judging; **F4 had zero coverage.**

## §3 — Five-layer diagnosis

| Layer | Verdict |
|---|---|
| Four-family cert architecture | **Sound — it worked.** F4 caught a real martial-mobility gap, F3's STOP caught genuine rank-deficiency, F2's ceiling misses caught a live band question. The design discriminated as intended. |
| Emission driver build | **Lagging spec.** Step-4 never re-pointed to family-cert when the family work landed. Real gap; benign until stepped on. (star-lord seam — no blame; built before the family pass existed.) |
| My (B) transmission | **PROXIMATE CAUSE.** Verdict criterion without instrument identity; no pilot gate. Half a rider. |
| Execution | **Faithful.** No misread; the driver did what the driver does; command matched transmission. |
| Discipline #2 | **Skipped by omission** — the amplifier turning a benign build gap into a would-be 50 h incident. |

## §4 — Mechanism (three compounding misses, all mine at authoring)

1. **Unverified load-bearing assumption.** I assumed the emission driver's gauntlet *was* the
   four-family cert because the family work is the current certification architecture and the
   driver is the emission path. One grep (`escape_lane` vs the driver — zero hits) falsified it
   in ten seconds, post-hoc. The framing-audit checklist (OP §4.1 Q1/Q2) exists for exactly
   this; I run it on design verdicts and did not run it on a **run authorization** — where it is
   cheapest and matters most.
2. **Sequencing violation against my own chain.** The reframe note's §6 puts emission
   DOWNSTREAM of certification closure. With F2's ruling open, F3 stopped, and F4
   wholesale-failed, no 1800-fire should have been authorable at all.
3. **Flag-name false-cheapness.** `--dry-run-flavor` is dry **only for LLM flavor spend**; the
   simulation is full-cost. The name lulled the sizing instinct, mine included.

## §5 — What the architecture is NOT guilty of

The four-family design is unimplicated and unamended by this incident. Its pilots produced
exactly the discrimination it was built for. The incident is purely: *a big run fired on the OLD
instrument while the NEW instrument's verdicts sat open, authorized by a rider that checked
neither.* No design surface moves in response.

## §6 — The stratified pilot re-fire (queued; what it now seeks to test)

**The target inverted.** The 1800 was a **harvest** run — collect certified survivors, assuming
the instrument settled and the driver pointed at it. Both assumptions were false. The pilot is a
**measurement** run seeking three verdicts, in order:

1. **PIPE verdict — instrument identity, end-to-end.** The re-pointed driver demonstrably runs
   the four-family cert: log scenario inventory contains all seven family shells (escape_lane
   and dense_cell are the tells — they exist ONLY in the family set); per-family verdicts
   emitted; survivor gate = four-family conjunction, not legacy ≥9/18. This is the check my
   rider missed, promoted to a deliverable.
2. **YIELD verdict — per-cell × per-family pass-rate map** under the RESOLVED instrument
   (post F2 ruling / F3 unblock / F4 disposition). Includes **chargen survival per cell**
   (leg3 precedent: 6/18 cells composed zero kits — compound yield = chargen-survival ×
   cert-pass is the real number).
3. **SIZING verdict — the yield map sizes or cancels the full fire.** Denominator = One-Realm
   roster need. If certified yield per 100 candidates covers roster need at N ≤ 1800, size the
   fire to need (possibly ≪ 1800). **If any roster-required stratum yields ~0 (martial × F4
   as of the pilots), NO N fixes it** — the remedy is upstream (generation or instrument), and
   the full fire stays cancelled until that closes. You cannot population-size your way out of
   a zero-yield stratum.

**Gates (all five, before the pilot fires):**

| # | Gate | Owner |
|---|---|---|
| 1 | F2 flag-pass ruling (32 over-band ceiling misses) | Matt |
| 2 | F3 boss_damage_scale rank-deficiency fix | gamora |
| 3 | F4-martial disposition (content vs instrument vs band fork) | Matt (my design read feeds it) |
| 4 | §4 acceptance-layer reframe ratification | Matt + jack-ryan review |
| 5 | Driver re-point: step-4 → family-cert OR standalone family-cert driver | star-lord |

**Sizing:** 18 generation cells × 6 = **108 candidates ≈ 3 h** at measured pace — verdict-grade
signal at 6% of the killed run's cost. **Optional split (KR's call):** if gate 5 lands before
gates 1–4, an early PIPE-smoke (18 × 2 = 36 kits ≈ 1 h) can verify the re-point alone.

**Out of scope for the pilot:** flavor (Beat B closed 35/35), resource_model (range-determined),
Glance (jack-ryan ratification lane).

## §7 — Routing

- **Companion amendment:** `2026-07-08-discipline-2-amendment-full-fire-rider-proposal.md`
  (this date, gandalf → jack-ryan ratification).
- **Engine tracker:** SESSION-DELTA prepended this session (driver re-point gap + pilot queue).
- **star-lord (via KR):** re-point investigation (gate 5) + optional hardening: a start-banner
  printing instrument identity, projected fight count, and wall-clock projection at driver
  launch — would have surfaced both defects in the first log line.
- **KR transmission:** *"1800 run killed (Matt, 14:56). Post-mortem filed. Queue: (a) star-lord
  driver re-point investigation; (b) stratified pilot 18×6 gated on F2 ruling + F3 fix + F4
  disposition + §4 ratification + re-point; (c) jack-ryan ratification pass on the Discipline #2
  amendment. No emission fire of any size until the pilot's three verdicts land."*

---

## §8 — SAME-DAY CORRECTION (star-lord forensic + gandalf source re-verification)

**Trigger:** star-lord's read-only forensic (KR-relayed) contradicted §2/§3's mechanism claim.
Re-verified everything against source before reconciling. He was right about the gate; I was
wrong about the mechanism; the conclusion survives one layer down. The critique pair worked.

### §8.1 — RETRACTED (two claims, both mine)

1. **"The survivor criterion is legacy ≥9/18" — FALSE.** `gauntlet_pass()` returns
   `family_certification_pass(cohort)` (`gauntlet_sim.py:1023`; R4 flip FIRED 2026-07-07;
   `season_emit` = any-cohort conjunction at `:1026`). I cited a **stale docstring**
   (`w3_emission_driver.py:505`) over live code — a Discipline #11 violation inside my own
   forensics, the exact failure the discipline names.
2. **"Log scenario inventory (complete)" — SAMPLING-FRAME ERROR.** The WP-R2-A-2 ceiling
   warnings are code-scoped to `MOB_HP_DIFFICULTY_SCENARIOS` = {open_arena, chokepoint_corridor}
   only (`spatial_engine.py:3590`). Four of the six fought shell types log **silently**.
   Log-absence was never evidence of not-fought. My "complete inventory" was complete only over
   warning-instrumented scenarios.

### §8.2 — CONFIRMED (the conclusion, corrected mechanism)

**season_emit = 0 by construction STANDS — via the catalog, not the gate.** Complete shell
inventory of `generation/endgame_encounter_catalog.py` (the 18 encounters actually fought):
`boss_with_adds ×3 · chokepoint_corridor ×3 · elite_pack ×4 · magic_pack ×3 · mini_boss ×1 ·
open_arena ×4`. **ZERO escape_lane. ZERO dense_cell.** `family_passed()` iterates *fought
results* for a member-shell match (`gauntlet_sim.py:903-916`); no fought result can ever carry
`scenario_shell_id="escape_lane"` → F4 = False for every kit → the four-family conjunction =
False for every kit → season_emit ≡ 0. **The F4-a registration (2026-07-08) armed the JUDGE;
nobody added the ROOM.** The registration docstring's claim that the flip made
`family_certification_pass()` "REACHABLE-True" is true at the criterion layer and false at the
system layer — reachability requires a room that exists in the rotation.

**Three-seam hole:** criterion registered (gamora seam) · driver wired (star-lord seam) ·
catalog rooms (rocket seam) — **the conjunction across seams had no owner.** Also resolved:
KR's mapping worry — chokepoint→F1 is correct (`F1 = {dense_cell, chokepoint_corridor,
magic_pack}`); the gauntlet runs a **subset** of the family space, not a superset. F1 is
satisfiable via 2-of-3 members, but note the **rigor mismatch**: emission judges F1 without
dense_cell while the pilot-instrument F1 standard included it — F1 is easier in emission than
in pilots. Design question for the catalog-extension spec.

### §8.3 — The volume finding (star-lord's, confirmed + sharpened)

The feed (`season_generation_pipeline.py:1717-1726`) submits **2,422 legendary configs** from
the 1,800 candidates (log line 13:29:00) with `all_configs.append(cfg)` **unconditional** —
while `config_to_kits` dedups by `legendary_id`. But `legendary_id` is **cell-derived**
(`{bc_cell_id}_t4_null` / `{bc_cell_id}_{chain_id}`, `:1331/:1383`), and the code's own contract
comment (`:1710-1714`) states: *"The gauntlet result is cell-level: all submissions sharing a
legendary_id receive identical season_emit (PlayerClass shape is cell-derived, not
sample-derived)."* **Certification is ALREADY cell-grain by documented design. The sim
re-fights the same cell-config ~100×.** Star-lord's dedup is therefore NOT a
certification-grain change — it enforces the existing contract. His Discipline-#1 find (the
5.32h math-note estimate never re-derived against the current instrument) also stands.

### §8.4 — Corrected layer table (supersedes §3's driver row)

| Layer | Corrected verdict |
|---|---|
| Four-family gate | LIVE and correct (R4 flip 2026-07-07) — star-lord right, my §2/§3 wrong |
| Encounter catalog (rocket seam) | **THE instrument gap**: F4 room absent (fatal — conjunction unsatisfiable), dense_cell absent (rigor mismatch) |
| Candidate feed | **Volume regression**: unconditional config submission vs cell-grain contract — ~100× redundant fights |
| My (B) transmission | Unchanged — proximate cause; and my post-hoc forensics ALSO mis-fired (§8.1), which **strengthens** #2-FF clause (a): pre-registered verification commands exist because ad-hoc grepping under confirmation pressure fails. New exhibits: a stale docstring (:505) and a contract comment the code half-honors (:1710) — comments lie; halt-loud asserts don't. |

### §8.5 — Revised pilot + gates (supersedes §6's gate table and sizing)

The pilot splits into **two cheap legs** on two harnesses:

- **Leg i — emission-path, cell-grain (PIPE + YIELD):** after dedup + catalog extension, the
  emission gauntlet fights only **distinct legendary configs (~20-70)** — near-free. PIPE
  verdict re-mechanized: fought rotation contains ≥1 escape_lane room; per-family verdicts emit;
  conjunction reachable. YIELD: per-cell × per-family pass map = the season_emit yield **by
  construction** (emission stamps at cell grain).
- **Leg ii — kit-grain spatial sample (GRAIN, new fourth verdict):** 18 cells × ~6 kits through
  gamora's spatial harness. Measures **within-cell verdict heterogeneity** — is the cell-grain
  stamp leaky? (F1 pilot's 25/40 kit-grain split is prima facie evidence it may be.) If
  same-cell kits diverge on family verdicts, the **demo-roster kits get individual kit-grain
  certification** (roster-sized ≈ dozens — cheap) while population certification stays
  cell-grain. SIZING falls out of both legs.

**Pilot preconditions (REVISED — instrument-validity only):** (1) rocket catalog extension
(escape_lane mandatory; dense_cell recommended; band tables + 18-count assertions updated);
(2) dedup fix with a **halt-loud byte-identity assert** (same-lid configs must be identical —
if `_build_legendary_config` leaks sample-derived fields, the :1710 comment lies and we want to
know loudly); (3) gamora F3 boss_damage_scale fix (F3 leg validity). **Matt's three rulings
(F2 flag-pass · F4-martial disposition · §4 reframe) gate verdict-INTERPRETATION and any
emission re-fire — NOT the pilot's firing.** They can land in parallel.

**Sign-off (§8):** gandalf, 2026-07-08 (same-day correction unit). Anchors:
`gauntlet_sim.py:903-1026` (live gate), `generation/endgame_encounter_catalog.py` shell
inventory, `season_generation_pipeline.py:1710-1726` (cell-grain contract + unconditional
submission), `spatial_engine.py:3590` (warning scope), run-log line 13:29:00 (2,422 configs).

---

**Sign-off:** gandalf, 2026-07-08. Anchors: kill-state log (final line 14:56:27),
`w3_emission_driver.py:505`, `gauntlet_sim.py:109` + `:264-269`, four-family pilot verdicts,
reframe note §6 chain. **Superseded in part by §8 (same day) — §8 governs where they conflict.**
