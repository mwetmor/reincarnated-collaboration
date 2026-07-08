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

**Sign-off:** gandalf, 2026-07-08. Anchors: kill-state log (final line 14:56:27),
`w3_emission_driver.py:505`, `gauntlet_sim.py:109` + `:264-269`, four-family pilot verdicts,
reframe note §6 chain.
