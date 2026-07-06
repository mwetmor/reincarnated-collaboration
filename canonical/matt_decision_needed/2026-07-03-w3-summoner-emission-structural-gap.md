# MATT DECISION NEEDED — W3 summoner emission: structural gap (criterion C unsatisfiable as written)

> **✓ RESOLVED 2026-07-06 — Matt ruled OPTION 1** (build the summon gen-path, re-fire as registered batch 2). Ruling record at the bottom of this file. Decisions-log: `2026-07-06: W3 summoner emission — Matt rules Option 1`. History below preserved.

> **Raised:** 2026-07-03, mid-flight in the DEMO-READINESS UNATTENDED RUN (W3 Phase A halt-loud, first §7 invocation of the run).
> **Finding:** `reincarnated-engine/src/reincarnated/generation/notes/w3-ungate-refutation-fired-2026-07-03.md` (rocket, engine `0a1706c`).
> **Adjudication:** critique pair (jack-ryan + gandalf, parallel read-only) — verdicts folded below with attribution.
> **Run disposition while you rule:** W3 fires as **solo full-spectrum BATCH 1** (spec §4 batch mechanism; criterion C PARKED loudly, NOT amended). Nothing below pre-commits your ruling.

## What happened

The run-spec criterion C un-gate ("lift `_DEFERRED_PROXY_BINS` + `ProxySpawn`; emission fires with proxy bins live") is **structurally unsatisfiable** — the generation-side summon-skill composition path does not exist:

1. Phase 4d of `bc_target_composer.py` (`:756-757`) is a no-op stub assuming `proxy_bin=="solo"` — verified verbatim by jack-ryan.
2. The `multi-spawn` geometry maps to `multi_projectile`/`chain`/`fork` (`:380-384`) — projectile multiplicity, no summon taxonomy.
3. `PoolMechanic` carries no summon discriminator; `build_proxies_surface` (`proxy_vocabulary_bridge.py:298-299`) documents "every exported kit gets `[]`."

Lifting the gate composes proxy-heavy targets with **zero summon skills** → hollow kits that would fake criteria B/C. Rocket performed no lift, no tag — halt-loud per §7 (both critics: correct and disciplined). Additionally: `ProxySpawn` at `mechanic_alteration.py:46` is a docstring reference to the register you RETIRED 2026-07-02 — nothing to lift; the spec's "2026-06-24 ratification" reference has no provenance in the engine tree. Spec v1.2 should correct both.

## Process finding riding along (jack-ryan [AMEND])

W0 deliverable #2 ("2-type decl check — PASS (not a gap)") validated the **fixture/classifier layer**, not the composer→kit production path the check was written to guard (Disc #2/#11 finding). The gap existed at W0 and was masked. Bounded — classifier/F-f/singleton-smoke PASSes are self-contained and unaffected; gamora's W2 cert is honest *as a fixture cert*. But no PASS in W0–W2 established emission-viable proxy content.

## The authority conflict your ruling resolves (the load-bearing part)

- **jack-ryan** concurs with rocket's Option 2 (curated certified summoners fill the demo roster's summoner seats, flagged `curated-not-emitted` in the registry), citing One Realm §5.2 "hand-authored acceptable at demo scope" + the III.1b launch-track split already in the tree.
- **gandalf [CONTEST]:** §5.2's hand-authored language is **struck through** — your 2026-07-02 ruling (one-realm-mvp-scope.md line 16, verbatim: *"they need to be balanced and pipeline emitted… we can pick from a seasonal emission… of battle-sim passed kits"*) repurposed the hand-authored decls to calibration fixtures only, zero hand-authored content ships. Option 2 would re-install exactly what you struck. jack-ryan's citation is to the pre-ruling text.
- **Both agree** the distinction is invisible to the player at demo scope (minute-one "raise the dead" promise is satisfiable either way); the emitted-vs-curated question is a *product-integrity* promise — which is precisely why it is yours, not ours.
- **gandalf on G4:** the ~25% is two promises wearing one number — the player experiences *curated-roster share* (2-3 of 8-10, achievable either way); the *emitted share* is an engine-capability goal (currently 0%, structurally).

## Options (rocket's three, critique-pair assessed)

| # | Option | Assessment |
|---|---|---|
| 1 | **Build the missing gen-path** (summon-skill composition + Phase-4d population + PoolMechanic summon discriminator + bridge derivation) as a scoped follow-on — math-first + Gate-1 — then re-fire summoner emission as **registered batch 2** | Both critics: highest integrity; the only path to generation-emitted summoners at the G4 share; the only path consistent with your 2026-07-02 ruling as written. Cannot ride the unattended run (needs a Gate-1 it can't supervise). |
| 2 | Curated certified summoners fill the demo summoner seats now, registry-flagged `curated-not-emitted`; criterion C + G4 formally amended (decisions-log + spec v1.2, not a header edit) | jack-ryan: process-honest with the flag, on-schedule. gandalf: contradicts your struck-through ruling — choose it only knowing you're reversing 2026-07-02. |
| 3 | Minimal Phase-4d stub → undifferentiated summoners emit | **Both critics reject.** False abundance poisoning the §8 shortlist; the D3-vanilla decoration-pet failure; ships the hollow-kit failure mode without Option 2's honesty. |

## What is being asked of you

1. **Rule the summoner path:** Option 1 (batch-2 re-fire after the gen-path build — consistent with 2026-07-02) vs Option 2 (curated seats + formal C/G4 amendment — a knowing reversal). Option 3 is not recommended by anyone.
2. **If Option 1:** authorize the gen-path build dispatch (math-first + Gate-1 critique-pair; new cross-seam `proxies` emission contract → ADR-004 MIGRATION).
3. **If Option 2:** the C/G4 amendment lands as a decisions-log entry + spec v1.2 fold (jack-ryan seam), and jack-ryan asks that the registry schema gain a per-content-type provenance field (`emitted`/`curated`) — G9 fast-pass ratification.
4. **Spec v1.2 hygiene either way:** strike the `ProxySpawn` lift + the 2026-06-24 reference from criterion C.

## What proceeded without you (no pre-commitment)

- **W3 BATCH 1 — solo full-spectrum emission** — fired under spec §4's batch mechanism: pilot beat → thousands of candidates → gauntlet → flavor (survivors-only kits; membership-keyed monster/gear/faction) → assemble + register. Banks curation-from-abundance for the ~7-8 non-summoner roster seats (gandalf Q4: intact). Criterion C recorded as PARKED in the registry/board, not satisfied, not amended.
- **Step-0 registry writer** (#8b, criterion F) — ruling-independent under all options; both critics endorsed the carve-out.
- Empirical criterion that re-engages the summoner leg: **your ruling on this file** (not time-passage).

**References:** finding note (path above) · blockers `bc_target_composer.py:97,318,380-384,756-757` · bridge `proxy_vocabulary_bridge.py:295-311` · W0 smoke `generation/notes/w0_prereqs_smoke_2026_07_03.py:98-131` · struck §5.2 `canonical/reap-die-rise-game/one-realm-mvp-scope.md` lines 16, 50, 67 · run spec v1.1 §1-C, §4, §5, §7 · state board `agentic_orchestration/demo-readiness-run-state-2026-07-03.md`.

---

## ADDENDUM (2026-07-03, post-W4-close) — gandalf: new evidence; the gap is empirically WIDER than "summoner emission"

The §5 glyph-gate pre-run over the true 700-kit bundle (`gandalf/notes/2026-07-03-glyph-s5-pre-run-findings.md`) surfaced population facts material to this ruling:

1. **Caster wipeout.** The catalog fielded 18 cells — STR 4 / DEX 4 / **INT 5 / WIS 5**. Survivors: STR 4/4, DEX 3/4, **INT 0/5, WIS 0/5**. The "11 failed cells" = all 10 caster-attribute cells + 1 melee-DEX. Zero mana-economy kits survive (doc-48: INT/WIS → mana). This includes the 9 INT/WIS cells designed at `proxy_density="none"` — i.e., the caster cells that were *meant* to be solo-viable also died.
2. **No cross-kit role variety.** Skill-role composition is invariant 4/4/2/2 (ST-dmg/AoE/control/support) across all 700 — no controller- or warden-leaning kits were emitted.

**Bearing on the options (evidence, not re-argument — my CONTEST verdict above stands unchanged):**

- **Option 1:** the gen-path build as scoped fixes SUMMON composition; it does not by itself explain or recover the 9 solo-caster cells. If caster viability is proxy-dependent (W2: caster-alone WR 0.000), a proxy-live batch-2 may recover them; if the failure is calibration/composition, batch-2 fires blind without the autopsy. **Attached recommendation: the batch-2 dispatch opens with a failed-cell autopsy as its first beat** — runnable from the existing canonical JSON (93MB, all 1,800 candidates' fight data on disk; capture + classify by failure mode, no re-fight).
- **Option 2, sharpened:** curated seats fill the *summoner* slots only — the batch-1 roster remains **martial-only** (STR/DEX chassis, non-mana economies). Element + geometry pips can fake an artillery-mage *read* (fire/shadow ranged-spiky), but the kit underneath is martial in resource-feel. Ruling Option 2 = accepting a demo roster with zero caster-fantasy kits, not merely zero emitted summoners.
- **Net asymmetry this evidence adds:** one batch-2 re-fire is now the recovery vehicle for THREE absences — summoners, casters, role-varied kits.

*Correction riding along:* the closeout phrase "role_orientation derivable-but-unpopulated" is wrong for that field specifically — it is **phantom** (hard-coded `"damage"` population-wide, `season_generation_pipeline.py:1557`; nothing exists to derive it from). `archetype_tag`/`dominant_element` are genuinely derivable — bridge specced in the findings note (F1), rides the glyph-stamp beat.

**Signed:** gandalf, 2026-07-03 (addendum; evidence from the §5 pre-run).

---

## FAILED-CELL AUTOPSY (2026-07-03) — gamora: 11-cell failure-mode classification (ZERO fights simulated)

> **Dispatch:** `dispatches/2026-07-03-gamora-failed-cell-autopsy.md` (Matt-approved, ruling-independent).
> **Method:** read-only forensic over the W3 canonical `src/reincarnated/simulation/output/cycle-13-gauntlet-sim-results-2026-05-27.json` (the `--recover-from-canonical` file; 2,200 `kit_results`, 125,400 `encounter_results`). **ZERO FIGHTS SIMULATED** — on-disk data only. Reproducible script: `reincarnated-engine/src/reincarnated/simulation/notes/w3_failed_cell_autopsy_2026_07_03.py`.
> **Evidence leg only** — this classifies the failure; it does NOT recommend Option 1 vs 2 (Matt's call).

### The gate the autopsy reads (framing-audit correction — Discipline #23, the F2 phantom-axis lesson)

`in_band`, `sg_overall`, and encounter-level `gauntlet_pass` are **FALSE/BLOCK across the ENTIRE 125,400-encounter population — survivors included** (`in_band` False ×125,400; `sg_overall` BLOCK ×125,400). They do **not** discriminate survivor from failure; reading them as the failure axis is a phantom-axis trap. The **live emission gate** is `kit_results.per_cohort[cohort].eligible_encounters_passed >= eligible_pass_floor (9)`, aggregated to emit via `season_emit = any(gauntlet_pass(c) for c in cohorts)` (`gauntlet_sim.py:715,725`). **Correction (jack-ryan Gate-2, verified against `gauntlet_sim.py:615-667`): `eligible_encounters_passed` counts a `tier_2`-based pass, NOT `tier_1_outcome=="PROVISIONAL_PASS"`.** Per shell branch (`:619-625,646-666`): CLEAR shells (open_arena, chokepoint_corridor, magic_pack, elite_pack) pass iff `tier_2_kpm` ∈ `ENCOUNTER_COHORT_KPM_BAND[shell][cohort]` (floor **and** ceiling); BOSS shells (boss_with_adds, mini_boss) pass iff `tier_2_survival_rate >= SURVIVAL_FLOOR_BY_COHORT[cohort]` (survive+kill within the 240s enrage timer) — verbatim `:624-625`, "The KPM band is NEVER consulted for boss shells." The boss-gate move (2026-06-19 doctrine, `:167-179`) retired the `tier_1` boss-KPM-REJECT so boss shells route to `tier_2` unconditionally. All 18 encounters are eligible; survivors clear **11.0–18.0** on `eligible_encounters_passed`, every composed failure clears **3.6–6.0** — a sharp, unambiguous separation at floor 9. (The dispatch's "tier-1 REJECT-count bimodal" is a real description but is NOT the survivor axis — survivor cells span `tier_1` REJECT 2→5,100 too; the discriminator is the `tier_2`-based `eligible_encounters_passed` count, not any `tier_1` field.)

### The 11-cell classification (each: file `cycle-13-gauntlet-sim-results-2026-05-27.json`)

| # | Cell | Attr | **Primary mode** | Secondary | One-line evidence (field:value) |
|---|---|---|---|---|---|
| 1 | `mid_low_spiky_int_none` | INT | **STRUCTURAL** | — | `kit_results` rows = **0**; `legendary_id` for this stem absent from BOTH tables → generator composed ZERO candidates |
| 2 | `ranged_low_spiky_int_none` | INT | **STRUCTURAL** | — | `kit_results` rows = **0**; no `legendary_id` anywhere → zero candidates |
| 3 | `ranged_medium_variable_int_none` | INT | **STRUCTURAL** | — | `kit_results` rows = **0**; no `legendary_id` → zero candidates |
| 4 | `ranged_medium_variable_int_light` | INT | **STRUCTURAL** | — | `kit_results` rows = **0**; no `legendary_id` → zero candidates (the one proxy-`light` INT cell — see Q3) |
| 5 | `melee_high_flat_int_none` | INT | **CALIBRATION** (clear-shell) | — | composed (100 kit rows, all `season_emit=False`); `Balanced elig_passed=3.6/9`; **PASSES boss shells** (`tier_2_survival_rate`≈1.0); FAILS clear shells (corridor/open timeout, pack `tier_2_kpm` above ceiling) |
| 6 | `melee_high_variable_wis_none` | WIS | **CALIBRATION** (clear-shell) | — | `Balanced elig_passed=3.6/9`; boss survive-kill PASS (≈1.0); packs FAIL by exceeding band CEILING; corridor/open timeout |
| 7 | `melee_medium_variable_wis_none` | WIS | **CALIBRATION** (clear-shell) | — | `Balanced elig_passed=3.8/9`; boss survive-kill PASS; clear shells FAIL (corridor/open timeout + pack overkill above ceiling) |
| 8 | `mid_medium_variable_wis_none` | WIS | **CALIBRATION** (clear-shell) | — | `Balanced elig_passed=3.9/9`; boss survive-kill PASS; clear shells FAIL; **see Q2** (the `tier_1` REJECT=0 lead is a home-shell artifact) |
| 9 | `ranged_low_spiky_wis_none` | WIS | **CALIBRATION** (clear-shell) | — | `Balanced elig_passed=3.8/9`; boss survive-kill PASS; clear shells FAIL (corridor/open timeout + pack above ceiling) |
| 10 | `ranged_medium_variable_wis_none` | WIS | **CALIBRATION** (clear-shell) | — | `Balanced elig_passed=3.7/9`; boss survive-kill PASS; clear shells FAIL (corridor/open timeout + pack above ceiling) |
| 11 | `melee_high_flat_dex_none` | DEX | **CALIBRATION** (pure) | — | composed; `Balanced elig_passed=6.0/9` (closest to floor); on the live gate PASSES `boss_with_adds` (100%) but FAILS `mini_boss` (0%) and both non-boss clear shells (corridor/open above upper band edge). NO ST-sustain collapse → the cleanest pure-calibration case |

### Bimodal split resolved → it is actually TRIMODAL

> **Re-grounded per jack-ryan Gate-2 (2026-07-03), verified against `gauntlet_sim.py:615-667`.** The prior version of this section attributed cohort (B) to a "single-target-sustain collapse" read off `tier_1_kpm` — a field the live gate does NOT consult for boss shells. That secondary is **WITHDRAWN**. On the actual `tier_2` gate the composed casters PASS boss shells and FAIL clear shells; cohort (B) is clear-shell CALIBRATION, not ST-sustain structural.

The one "FAIL" label hides **three** mechanisms, not two:

- **(A) Generation gap (STRUCTURAL) — 4 INT cells (#1–#4):** the composer emitted **zero kits**. No fight ever ran under their `legendary_id`. This is a missing-generation-capability signature by the dispatch's own taxonomy — not fixable by any number.
- **(B) Clear-shell calibration (CALIBRATION, pure) — 6 composed caster cells (#5–#10):** these DO fight and DO deal damage. On the live gate they **PASS the boss survive-kill shells** (`tier_2_survival_rate`≈1.0; `boss_with_adds`/`mini_boss` survive-kill 83–95%) — casters survive and kill the single-target boss. They FAIL the **CLEAR** shells: `chokepoint_corridor` + `open_arena` time out (`tier_2_kpm`=0), and `elite_pack` + `magic_pack` exceed the band **CEILING** (band `(8.26,28.13)`/`(18.61,100.0)` vs caster `tier_2_kpm` at/above 450–600 → overkill above the ceiling, NOT undershoot). Net `elig_passed ~3.6–3.9 << 9`. *(The "600" is a documented tick-floor discretization artifact — `t4_sim_cycling.py:720-723`; `gauntlet_sim.py:211` — not a real throughput; it signals only that the clear was faster than the 1.0s domain floor.)*
- **(C) Corridor overkill (CALIBRATION, pure) — `melee_high_flat_dex` (#11):** on the live gate PASSES `boss_with_adds` (100%) but FAILS `mini_boss` (0%) and both non-boss clear shells (amplitude above the corridor/open upper band edge). No caster mechanism; a martial-DEX kit tuned too hot for the clear shells.

### Load-bearing answer: is the caster wipeout (10 INT/WIS cells) predominantly STRUCTURAL or CALIBRATION?

**HALF structural, HALF calibration** (re-grounded per jack-ryan Gate-2 — the prior "predominantly structural + ST-sustain economy gap" framing is WITHDRAWN). Decomposition of the 10 caster cells:

- **4/10 are STRUCTURAL** (no kit composed at all — a generation gap; #1–#4). No fight-side lever touches these; a proxy-live batch-2 re-fire recovers them **only if the gen-path first composes candidates for these cells**. This half is the load-bearing Option-1 caution: **a batch-2 cannot fight what was never composed.**
- **6/10 are CALIBRATION on the live gate** — clear-shell band mismatch (corridor/open timeout + pack `tier_2_kpm` above ceiling), with the boss survive-kill gate **already PASSED**. There is no ST-sustain collapse: casters clear the single-target boss. Whether these 6 recover on a proxy-live batch-2 is a **calibration/geometry** question (do proxies move clear-shell tempo enough to bring `tier_2_kpm` into band on corridors/open and off the ceiling on packs), NOT a resource-economy-loop question. Materially more tractable than "the mana economy has no single-target loop."

**Net for the ruling:** a proxy-live batch-2 re-fire *without* a gen-path fix fires **partially blind on the 4 zero-composed INT cells** (this caution survives and is the load-bearing one) — it cannot compose those cells at all. The 6 composed casters are a **calibration/geometry** recovery candidate with the boss already cleared. The caster absence is therefore **half structural (generation gap, 4 cells) and half calibration (clear-shell band, 6 cells)** — NOT "majority-structural + ST-sustain economy gap."

### Cheapest refuting test per verdict (Discipline #19.1)

- **STRUCTURAL (4 INT cells):** SQL/JSON count — if a `legendary_id` for these 4 stems appears in `kit_results` or `encounter_results` of a re-run, the "zero candidates" verdict flips to calibration. (Current count: **0**, both tables.)
- **CALIBRATION (clear-shell) on the 6 composed casters (re-grounded per jack-ryan Gate-2):** the boss survive-kill gate is already PASSED on-disk (`tier_2_survival_rate`≈1.0), so the prior "widen the boss band" test is moot — the boss is not their blocker. The correct refuting test is the CLEAR-shell one: re-run with the clear-shell tempo altered (e.g. proxy-live composition, or corridor/open band widened + pack ceiling raised). If `tier_2_kpm` then lands in-band on corridors/open (currently timeout=0) and off the ceiling on packs → `elig_passed≥9`, calibration confirmed. *(Re-fight; flagged as the refuting test, NOT executed — dispatch forbids simulation.)*
- **CALIBRATION (pure) on `melee_high_flat_dex`:** re-run with the `mini_boss` + corridor/open clear-shell band edges raised. If it clears `elig_passed≥9`, pure-calibration confirmed. Its `boss_with_adds` survive-kill PASS (100%) already rules out an ST-sustain gap.

### The three dispatch open questions — answered

1. **Defensive-cohort confound (`gauntlet_pass_by_cohort.Defensive=0`): ORTHOGONAL, not a confound.** Defensive's `eligible_encounters_total` is fixed at **6**, structurally below `eligible_pass_floor=9` → it can *never* pass, for **every** cell including all 7 survivors. Proof: **1,000/1,000** emit-kits have Defensive `gauntlet_pass=False` yet still `season_emit=True`. Defensive pass is not a precondition for emission; it is a fixture artifact (a cohort that runs too few eligible encounters to clear the floor) and does not touch the caster read.
2. **`mid_medium_variable_wis` (REJECT=0, yet failed): NOT a clean band/survival-only failure — the REJECT=0 is a home-shell projection artifact.** Filtered by `encounter_id` (its home shell = `magic_pack`) it is 100% PROVISIONAL_PASS → REJECT=0 (the dispatch's lead). But the live gate reads **all 18 shells** (`tier_2`-based per `gauntlet_sim.py:615-667`): `Balanced elig_passed=3.9<<9`. Its mechanism is the **same clear-shell calibration** as the other 5 composed WIS cells (boss survive-kill PASSED; corridor/open timeout + pack above ceiling) — it is an ordinary member of cohort (B), neither the cleanest "calibration-not-structural" candidate nor its counter. The `tier_1` REJECT=0 headline was reading the home-shell `tier_1_outcome`, not the cross-shell `tier_2` gate input.
3. **`ranged_medium_variable_int_light` vs the `_none` INT cells: NO difference — proxy-density did not change caster viability at composition.** Both `_light` and `_none` INT variable cells have **zero composed kits** (identical structural absence). The one proxy-`light` INT cell composed exactly as many candidates as its `_none` siblings: **none**. So the closest on-disk proxy-density signal says proxy-`light` did **not** rescue the INT caster at the composition stage — the gap is upstream of proxy density. (This is the on-disk signal that bears on Option 1: proxy density alone, at the `light` level present here, did not move caster composition. Whether a heavier proxy tier would is not answerable from this data without new generation + fights.)

### Assertions

- **ZERO fights simulated.** All findings derive from on-disk `kit_results` + `encounter_results` in the cited canonical JSON. No re-simulation, no new fights, no gauntlet re-run.
- No cross-seam contract change (read JSON, wrote this markdown section). Round-trip: not applicable.
- Analysis artifact only; no production code touched; throwaway script under `simulation/notes/` (not tagged).

**Signed:** gamora, 2026-07-03 (failed-cell autopsy; evidence leg for the summoner ruling). Awaiting jack-ryan DEV-MODE review of the classification method + evidence.

> **CORRECTIONS LANDED (gamora, 2026-07-03, post-jack-ryan Gate-2):** the four required doc-only corrections from the REVIEW VERDICT below are now folded above (gate description at "The gate the autopsy reads"; cohort-(B) rows #5–#10 + trimodal-split (B) + load-bearing answer + Q2 re-grounded to clear-shell calibration; `melee_high_flat_dex` #11 evidence tightened; headline re-stated as HALF structural / HALF calibration). ZERO fights — all four are derivable from fields already on disk (`gauntlet_sim.py:615-667` gate semantics + on-disk `tier_2_survival_rate`/`tier_2_kpm`). The withdrawn plank: the "single-target-sustain collapse / band re-tune can't fix" secondary is retracted — the composed casters PASS the boss survive-kill gate; their blocker is the CLEAR shells. **Net effect on the headline: caster absence is HALF structural (4 zero-composed INT cells) + HALF calibration (6 composed cells, boss already cleared) — NOT majority-structural + ST-sustain economy gap.** Script docstring `w3_failed_cell_autopsy_2026_07_03.py:17-23` corrected to match.

---

## REVIEW VERDICT (2026-07-03) — jack-ryan, DEV-MODE (Gate 2, BLOCK authority)

> **Dispatch:** `dispatches/2026-07-03-gamora-failed-cell-autopsy.md` § "Review leg". Scope: review the CLASSIFICATION METHOD AND EVIDENCE, not just conclusions. **ZERO fights simulated by this review** (read-only JSON queries + engine source read only).
> **Principles applied:** Review Principles #1 (math-before-code / evidence-cited), #4 (decisions-log/gate-as-truth), #5 (severity). Disciplines #1, #12 (semantic shift), #19.1, #23 (framing-audit).

### Verdict: **PASS-with-notes — but ONE load-bearing plank is BLOCKed and must be corrected before this informs the ruling.**

The autopsy's **structural skeleton is sound and its top-line labels survive** (4 INT cells structural; `melee_high_flat_dex` pure-calibration; the floor-9 separation; the phantom-axis catch; Defensive orthogonality; int_light==int_none). But the narrative mechanism gamora attached to the 6 composed caster cells — the **"single-target-sustain collapse / boss-kpm 0.25–1.14 / a band re-tune cannot fix"** structural-secondary — is read off a **field the live emission gate does not use**, and is **contradicted by the field it does use**. Because Matt's Option-1-vs-2 ruling turns specifically on whether casters are structurally boss-broken, that plank must be corrected before it informs the ruling. Everything else PASSES.

### CONFIRMED (verified by direct JSON query + engine source):

1. **The 4-INT-cell STRUCTURAL verdict HOLDS — not a parsing artifact.** The apparent KR-vs-gamora conflict is resolved: `encounter_id` carries the ENCOUNTER-side (environment) cell; `legendary_id` carries the KIT's home cell. Query — raw substring (bypassing the regex) across `kit_results` for `mid_low_spiky_int`, `ranged_low_spiky_int`, `ranged_medium_variable_int_none`, `ranged_medium_variable_int_light`: **0 kit rows each** (only `int` kit ever composed is `melee_high_flat_int_none`, 100 rows). Same 4 stems on the ENCOUNTER side (`encounter_id`): **6,600 rows each**, with tier-1 REJECT = 6,300 / 5,100 / 5,100 — **exactly KR's bimodal lead.** KR counted kits-rejecting-INSIDE those cells' encounter shells; gamora counted kits FROM those cells (zero). Both internally correct; different axes. gamora's verdict stands; KR's "all 18 cells present" is true at the encounter-shell level but only 14 cells composed kits.
2. **Floor-9 separation is real and gate-authoritative.** Read straight from `kit_results.per_cohort.Balanced.eligible_encounters_passed`: survivors **11.0–18.0**, composed failures **3.65–3.87**, `melee_high_flat_dex` **6.00** — all << floor 9. `eligible_encounters_passed` IS a live varying coordinate (survivors clear it). Matches gamora's cited numbers.
3. **Phantom-axis catch is correct.** `in_band` (False ×125,400) and `sg_overall` (BLOCK ×125,400) are population-wide constants; reading them as the failure axis is the trap gamora correctly flagged (Discipline #23).
4. **Defensive orthogonality — exact.** `eligible_encounters_total`=6 (min=max) < floor 9 for every kit; **1,000/1,000** emit-kits have Defensive `gauntlet_pass=False`. Orthogonal, confirmed.
5. **int_light == int_none:** both zero composed. Proxy-`light` did not rescue INT composition; gap is upstream of proxy density. Confirmed.
6. **ZERO fights:** gamora's script (`w3_failed_cell_autopsy_2026_07_03.py`) contains only `json.load` + reads — no `simulate`/`run_gauntlet`/`subprocess`/fight-execution. Assertion honest.

### BLOCK (the load-bearing plank — cohort (B) mechanism is mis-attributed):

**The live ship gate reads `tier_2`, not `tier_1`.** Per `gauntlet_sim.py:615-667` (`eligible_encounters_passed`): CLEAR shells pass iff **`tier_2_kpm`** in `ENCOUNTER_COHORT_KPM_BAND[shell][cohort]`; BOSS shells (`boss_with_adds`, `mini_boss`) pass iff **`tier_2_survival_rate >= SURVIVAL_FLOOR_BY_COHORT[cohort]`** — and (verbatim `:624-625`) *"The KPM band is NEVER consulted for boss shells."* The boss-gate move (`:167-179`, Matt-adopted 2026-06-19) explicitly **retired the tier_1 boss-KPM-REJECT** so boss shells route to tier_2 unconditionally. gamora's method (decision-file line 81 + script docstring `:21-23`) describes the gate as counting **`tier_1_outcome=='PROVISIONAL_PASS'`**. That is the wrong field family — and it drives the wrong mechanism story:

- **Applying the ACTUAL gate per shell (Balanced), the 6 composed casters PASS the boss shells:** `boss_with_adds` survive-kill 94–95%, `mini_boss` 83–92% (`tier_2_survival_rate` median = **1.000**). **Casters DO survive and kill the single-target boss on the live gate.** gamora's "boss kpm 0.25–1.14 → ST-sustain collapse a band re-tune can't fix" reads the **retired tier_1 boss-KPM path** (`tier_1_kpm` med ~0.7), a field the gate abandoned for exactly the reason it manufactured a fake STR boss-crater (`:171-173`).
- **Where the casters ACTUALLY fail the gate: the CLEAR shells.** `chokepoint_corridor` + `open_arena` fail on timeout (`tier_2_kpm`=0, `tier_2_survival_rate`=0); `elite_pack` + `magic_pack` fail by exceeding the band **CEILING** (band `(8.26, 28.13)` / `(18.61, 100.0)` but caster `tier_2_kpm` = 450 / 600 → **overkill above the ceiling**, not undershoot). The "600" gamora reads as pack throughput is a **documented tick-floor discretization artifact** (`t4_sim_cycling.py:720-723`; `gauntlet_sim.py:211`), not a real KPM.

**Consequence for the mechanism, not the label:** cohort (B)'s failure on the live gate is **clear-shell calibration/geometry** — corridor/open timeout + pack-overkill-above-ceiling — **not a single-target-boss-sustain collapse.** The specific claim that a band re-tune "would relabel the same collapsed kpm without creating single-target sustain" is refuted: the casters already clear the boss survive-kill gate; the boss is not their blocker. This does **not** flip the four **primary-mode labels** (the 4 INT cells are still zero-composed = structural; the 6 casters still fail the floor; dex still pure-calibration). It **does** dissolve the *structural-secondary* that the "predominantly STRUCTURAL" caster headline leans on for the composed subset.

### Does the "PREDOMINANTLY STRUCTURAL" headline survive for Matt's ruling? — **PARTIALLY. Re-state it as:**

- **4/10 caster cells are unambiguously STRUCTURAL** (generation gap — zero kits composed). This half is rock-solid and is the part that actually bears on Option 1: a proxy-live batch-2 **cannot fight what was never composed.** The gen-path must compose INT candidates first.
- **6/10 caster cells are CALIBRATION on the live gate** — clear-shell band mismatch (corridor/open timeout + pack overkill), with the boss survive-kill gate already PASSED. The prior "structural ST-sustain secondary" is **not supported by the gate field** and should be withdrawn or re-grounded. Whether these 6 recover on a proxy-live batch-2 is now a **calibration/geometry** question (do proxies change clear-shell tempo enough to bring `tier_2_kpm` into band on corridors/open, and off the ceiling on packs), not a resource-economy-loop question.

**Net for the ruling:** the caster absence is **half structural (generation gap, 4 cells) and half calibration (clear-shell band, 6 cells)** — NOT "majority-structural + ST-sustain economy gap." A proxy-live batch-2 without a gen-path still fires **partially blind on the 4 zero-composed INT cells** (gamora's core Option-1 caution survives, and is the load-bearing one). But the 6 composed casters are a **calibration/geometry** recovery candidate, materially more tractable than "the mana economy has no single-target loop." Matt should rule with that corrected decomposition.

### Required corrections (gamora — before this informs the ruling; ADR-002: doc-only, within jack-ryan approval once fixed):

- [ ] **Correct the gate description** (decision-file line 81 + script docstring `:21-23`): the live gate counts `tier_2`-based pass (`tier_2_kpm` in-band for clear shells; `tier_2_survival_rate >= floor` for boss shells), **not** `tier_1_outcome=='PROVISIONAL_PASS'`. (`gauntlet_sim.py:615-667`.)
- [ ] **Re-ground cohort (B)** (decision-file rows #5–#10 + "Bimodal split (B)" + the load-bearing answer): the composed casters PASS the boss survive-kill gate (`tier_2_survival_rate`≈1.0, boss-pass 94–95%); they FAIL the CLEAR shells (corridor/open timeout + pack `tier_2_kpm` **above ceiling**). Withdraw or re-evidence the "single-target-sustain collapse / band re-tune can't fix" secondary. The "kpm→600 pack overkill" phrasing reads a discretization artifact — drop or footnote it.
- [ ] **Re-state the headline** as the corrected half-structural / half-calibration decomposition above.
- [ ] **`melee_high_flat_dex` #19.1 note:** on the live gate it PASSES `boss_with_adds` (100%) but FAILS `mini_boss` (0%) and both non-boss clear shells — its "boss PROV=100%" is `boss_with_adds` tier_1 only. Primary-mode label (pure calibration) still holds; tighten the evidence line.

### For Matt (this verdict gates whether the autopsy informs the Option-1-vs-2 ruling):

- [ ] The autopsy is **usable for the ruling AFTER the four corrections land** (they are doc-only and do not require re-fight — every correction above is derivable from fields already on disk). The corrected takeaway — **4 caster cells structurally un-composable, 6 caster cells clear-shell-calibration with the boss already cleared** — is the honest input. If Matt is ruling on cadence before gamora re-grounds, use THIS block's corrected decomposition, not the "predominantly structural / ST-sustain" framing above it.

### References
- Canonical JSON: `reincarnated-engine/src/reincarnated/simulation/output/cycle-13-gauntlet-sim-results-2026-05-27.json` (read-only; kit_results 2,200, encounter_results 125,400).
- Gate semantics: `reincarnated-engine/src/reincarnated/simulation/gauntlet_sim.py:158,167-186,615-667,690-715` (eligible_encounters_passed reads tier_2; boss survive-kill; floor 9); `ENCOUNTER_COHORT_KPM_BAND` bands (boss_with_adds `(2.49,3.78)`, elite_pack `(8.26,28.13)`, magic_pack `(18.61,100.0)`), `SURVIVAL_FLOOR_BY_COHORT` (Balanced 0.8).
- 600 = discretization artifact: `t4_sim_cycling.py:100,720-723,748-756`; `gauntlet_sim.py:188-211`.
- gamora's script: `reincarnated-engine/src/reincarnated/simulation/notes/w3_failed_cell_autopsy_2026_07_03.py` (read-only confirmed).

**Signed:** jack-ryan, 2026-07-03 (DEV-MODE Gate-2 review of the failed-cell autopsy classification method + evidence). PASS-with-notes; cohort-(B) mechanism BLOCKed pending the four doc-only corrections above.

---

## GATE-2 RE-REVIEW — BLOCK LIFTED (2026-07-06) — jack-ryan, DEV-MODE

> **Scope:** verify gamora's four doc-only corrections (CORRECTIONS LANDED note above) are correct + complete. **ZERO fights** — verified against on-disk fields + engine source only. **Principles applied:** #4 (gate-as-truth), #5 (severity). **Disciplines:** #11 (empirical inspection over assumption), #12 (semantic shift), #23 (framing-audit).

**Verdict: BLOCK LIFTED. All four corrections land correctly and completely; no residual.**

Verified against `gauntlet_sim.py:640-692` (the actual `eligible_encounters_passed` body): boss shells gate on `tier_2_survival_rate >= SURVIVAL_FLOOR_BY_COHORT[cohort]` (`:671-677`, "the KPM band is NEVER consulted for boss shells" `:649`); clear shells gate on `tier_2_kpm` in `ENCOUNTER_COHORT_KPM_BAND` (`:680-691`). This is exactly what the four corrections now assert.

1. **Gate reads `tier_2` not `tier_1`** — CORRECT. Decision-file line 81 + script docstring `w3_failed_cell_autopsy_2026_07_03.py:25-40` now describe the gate as `tier_2`-based (survive-kill for boss, KPM-in-band for clear), with the `tier_1`/PROVISIONAL_PASS fields explicitly demoted to descriptive-context-only. Matches source.
2. **Cohort (B) re-grounded** — CORRECT + complete. Rows #5–#10 now read "boss survive-kill PASS / clear shells FAIL (corridor/open timeout + pack `tier_2_kpm` above ceiling)"; the ST-sustain secondary is WITHDRAWN (line 101); the "600" is footnoted as a documented tick-floor discretization artifact (line 106, `t4_sim_cycling.py:720-723`), not real throughput. Q2 (`mid_medium_variable_wis`) re-grounded to ordinary clear-shell calibration.
3. **Headline re-stated HALF-structural / HALF-calibration** — CORRECT. Line 111 + the load-bearing answer now read "4/10 STRUCTURAL (zero-composed) + 6/10 CALIBRATION (clear-shell, boss already cleared)," replacing "predominantly structural + ST-sustain economy gap." The load-bearing Option-1 caution (batch-2 cannot fight the 4 zero-composed INT cells) is preserved and correctly foregrounded.
4. **`melee_high_flat_dex` #19.1 evidence tightened** — CORRECT. Rows #11 + trimodal (C) now state PASSES `boss_with_adds` (100%), FAILS `mini_boss` (0%) + both clear shells; the refuting-test line names the `mini_boss` + corridor/open band-edge raise. Primary-mode label (pure calibration) holds.

**No residual.** All four are derivable from fields already on disk — no re-fight was needed or performed. The corrected decomposition is the honest ruling input, and Matt's Option-1 ruling used it.

## RULING RECORD (2026-07-06) — Matt: OPTION 1

**Ruled:** OPTION 1 — build the missing summon-skill generation path (math-first + Gate-1 critique-pair), then re-fire summoner + recovered-caster + role-varied emission as **registered batch 2**. Consistent with Matt's 2026-07-02 "balanced and pipeline emitted" ruling (one-realm-mvp-scope.md line 16). Option 2 (curated seats) NOT taken; Option 3 (undifferentiated stub) rejected.

- **Criterion C un-PARKs**, with **batch 2 as its satisfaction path**. Run spec folded to **v1.2** (jack-ryan): the `ProxySpawn` lift + "2026-06-24 ratification" refs STRUCK from §1-C + §3 W3 step 1.
- **Landed:** Leg 0 (INT-cell zero-composition root-cause, engine `2980182`); Leg 2; gamora's four Gate-2 autopsy corrections (BLOCK LIFTED, above). **In flight:** Leg 1 (summon gen-path build).
- **Decisions-log entry:** `2026-07-06: W3 summoner emission — Matt rules Option 1 (build the summon gen-path, re-fire as batch 2); criterion C un-PARKs` (`reincarnated-engine/design/decisions/decisions-log.md`).
- **Empirical close criterion for C:** a registered batch-2 bundle whose summoner + recovered-caster kits pass the `tier_2` ship gate (`eligible_encounters_passed >= 9`) — NOT time-passage.

**Signed:** jack-ryan, 2026-07-06 (Gate-2 re-review BLOCK LIFT + ruling record; decision file RESOLVED, history preserved).
