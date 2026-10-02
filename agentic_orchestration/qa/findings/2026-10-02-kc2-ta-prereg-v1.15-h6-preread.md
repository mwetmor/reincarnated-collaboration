# Finding — 2026-10-02 — KC2-PLAY H-6: pre-read of T-A prereg v1.14 + v1.15 (Q104's successor)

**Reviewer:** jack-ryan (DEV-MODE, gatekeeper)
**Severity / verdict:** **PASS-WITH-FINDINGS.** No BLOCK. 3 WARN, 6 INFO. **All 28 EXACT rows pass law (a) on the oracle of record.** Three WARNs are owed **before H-7**, the 28-row pre-attempt read.
**Target:** prereg v1.14, collab `4d64316d`, FILE `5bbe7ae5f0c3f73c77ee7cc3e21870ed8523b6d19fa1eae977dff451ef6b2d92`, instruments `cbe174fe`. Prereg v1.15, collab `d84010f2`, FILE `d1c4a75ae2d35b2c27ddd127b18ef0066664eb54926e8466f2fe522a1ca34593`, instruments `be44edd1`. Both files are unmodified since their commits (porcelain clean). D4 held: each prereg commit touches one file.
**Oracle of record:** engine `969fbd8d`, `scripts/gamora_kc2_play_v3p11_oracle_2026_10_02.py` (FILE `dc39d8b6…`, verified), `run_one("V311-FULL")` + `v3p8.graded_arm`. The engine HEAD moved during this read (`acba3ac5` → `6c9f988f`, JOIN-1 commits). `git diff 969fbd8d HEAD -- simulation/kc2 <oracle scripts>` is empty, and all 150 modules the derivation imports are byte-identical to their `969fbd8d` blobs. Pack v3.11: model `99711727…`, reference `af58ef40…`. Shared OBS-1 guard: engine `9c756081`, FILE `5f3f4f1e29d147e528709ef317b20ae226edc04c60534d9d506e987d5a3b54d2`.
**Developer:** gamora. **Conductor:** gandalf (KP-238 … KP-244).
**Principles applied:** REVIEW_PROCESS 1 (math before code), 2 (reproduction), 3 (cross-seam: drax's H-4 harness), 4 (committed truth: Matt Q104/KP-240, Q98/KP-207, Q99/KP-212, KP-137, KP-178), 5 (severity matters). Discipline #12 (semantic shift named) and #73 (the record follows the state).
**Instruments:** the sibling folder `2026-10-02-kc2-ta-prereg-v1.15-h6-preread/`, committed with this file (FILE digests in § 9). Disk stayed at 26–27 GiB free throughout, above the 20 GiB HALT.
**Out of scope, not run:** H-2, H-3, H-5 and H-7. They need the attempt digest, which does not exist yet.

---

## 1 · Law (a) on all 28 EXACT rows: what I re-ran and what I recomputed myself

I read every instrument before running it: `oracle_trace_v3p11.py`, `check_v1p14.py`, `derive_v1p14.py`, `audit_v1p15.py` and `check_v1p15.py`. Then I did two separate things.

**(A) RE-RAN gamora's instruments** from scratch copies. That was 36 oracle traces (hooked ×5, bare ×5, single ×25, repeat ×1), 5 v1.15 audits, both checkers and the static derivation. The comparison is in `h6_rerun_compare.json`:
- **36/36 traces and 5/5 audits are byte-equal to the committed outputs** once `wall_s` is excluded.
- `results_v1p14.json` and `results_v1p15.json` are equal, excluding only the gz FILE digests, which embed `wall_s`.
- `derive_v1p14.json` is equal except for `engine.HEAD`. Its one self-check failure is "engine HEAD is the oracle rev", which is expected because HEAD moved. The modules differing from `969fbd8d` are none.

**(B) RECOMPUTED INDEPENDENTLY** with `h6_gate_probe.py`, `h6_gate_check.py` and `h6_crit_probe.py`. These are my own hooks and rules and import nothing from gamora's instruments. Each runs the same oracle composition, 5 arms × salts 0–4, leg A.

| row | how the gate checked it | oracle passes? |
|---|---|---|
| `TA-X-01` | (A) repeat run byte-identical; single == batch 25/25 | **PASS** |
| `TA-X-02` | cited (census 89/89); § L.1 disposition read | PASS (structural) |
| `TA-X-03` / `04` / `05` | **(B)** my per-cell digest covers every event row, the ring ledger, the actors and pets, and the tick range of every wave. `M-POL-2-NULL ≡ M0` 5/5; `W1-NULL ≡ M-POL-2` 5/5; `M-POL-2 ≢ M0` 5/5 | **PASS** |
| `TA-X-06` (declared) | (B) `W1 ≡ M-POL-2` on salts 0, 1, 4 | printed, as v1.14 states |
| `TA-X-07` | cited; § L.4 read; (L2) is owed at the attempt digest (H-2) | PASS (structural) |
| `TA-X-08` | (A) | **PASS 25/25** |
| `TA-X-09`, `18`, `26`, `27(d)`, `29(a)`, `29(d)`, `29(e)` | (A) re-derivation equal: ROWSET `0e826ee0…`, bits `c00fffffffffffde`/`be9777a5cf72cec6`, 139/97, (e) `3.197066`/`4.935649` | **PASS** |
| `TA-X-10` | **(B)** W1 max body 43.29880530043161 m, max spawn 43.54625981277354 m. The oracle's own `ArenaFold.r_wall_m` is 43.71638147965161 m, equal to the prereg bound | **PASS** |
| `TA-X-11` | **(B)** 0 player and 0 body wall clamps on all 10 W1 / W1-NULL cells | **PASS** |
| `TA-X-12` | (B) no `pool` damage tag on any row | **PASS 25/25** |
| `TA-X-13` | **(B)** 0 crit rows sourced by `player` on 25 cells. ⚑ **The printed basis is wrong; see WARN-2** | **PASS** (narrow reading) |
| `TA-X-14`, `17`, `22`, `27(c)`, `29(c)` | (A) | **PASS** |
| `TA-X-15(a)` | (B) p01–p04 spawn at 0.0 s and p05 at 4.0 s, every body | **PASS 25/25** |
| `TA-X-16` | **(B)** I derived `LU-KEYS = [5,5,5,4,4,5,5,5,5,4]` from `referent_lineup.REFERENT_LINEUP` myself. Every wave is played, there is no key 6, bonus spawns are off, and fought points ⊆ fold keys | **PASS 25/25** |
| `TA-X-19` | source read: `c11` passes `monster_deferred_arrival=None` and no `a8` row names a deferred arrival | PASS-vacuous (as stated) |
| `TA-X-20`, `28` | cited; kit and `player_sustain.py` unchanged | PASS (structural) |
| `TA-X-21` | **(B)** liveness of every `round(` line in every `simulation/kc2` module, measured with a `sys.monitoring` LINE probe that does not perturb the run (digest equal). ⚑ **Its site list is stale; see WARN-3** | PASS in rule (every live site is `int(round(`, half-to-even) |
| `TA-X-24` | (B) `PhaseModel.ENGAGE` on every wave; no actor hash anywhere in the v3.8–v3.11 fold modules | **PASS** |
| `TA-X-25` | (B) every fought record ∈ POOL-466 (466); `can_swing` via (A) | **PASS 25/25** |
| `TA-X-29(b′)` | (A) 104,945 composed rows bit-equal; (B) divisor reachability (INFO-3) | **PASS 25/25** |
| `TA-X-30(a′)` | **(B)** I checked the travel law myself on all 830,069 roster player-argument steps (776,181 unclipped and law-exact; 53,888 held at zero). Operand by **pack membership**, not by `halt_for`'s return: Attack (op = distance) 253,753 · waypoint (op 0) 572,104 · ring halt (op 2.4) 4,212 · non-waypoint Pursue **0** · none outside the pack set. Pets via (A): 672,931 steps exact | **PASS 25/25** |
| `TA-X-30(b′)` | **(B)** every `clamp_body` call and every call that **returned a stop** | **PASS 25/25**, ⚑ **vacuous on 25/25; see WARN-1** |

**Result: the v3.11 oracle passes all 28 EXACT rows of v1.14 + v1.15 under law (a).** gamora's 26 + 2 PASS is reproduced. No row fails. The findings below concern what three of those passes *mean*, not whether they pass.

## 2 · § B.0 completeness (OBS-1) on the 25 graded cells

- I applied the **shared guard** (`gamora_join1_obs1_guard_2026_10_02.cell_check`) to `run_one`'s own result on every arm. **G1** (10 rows w151…w160, raw outcome cleared or player_death), **G2** (w160 not at the tick cap: cap 4,000 ticks = 326.531 s; the longest wave on any cell is **968 ticks**) and **G3** (9N rows) all hold on **25/25**.
- **G4** is N/A. `run_one` returns no summary layer (keys `config`, `fold_reports`, `fold_telemetry`, `salts`). This is the same disposition as the J0-F re-freeze.
- My own innermost `simulate_wave` observer agrees on every cell: every wave is `cleared/board_empty` or `player_death/player_died`, no exception escaped, `raised` is None, and leg A matches the first death. That gives 20 clears in w160 and 5 deaths in w160.
- **Inertness:** hooked == bare 25/25 and single == batch 25/25, both reproduced under (A).
- **§ B.0 holds: 25/25 complete, no STOP cell.** INFO-4 notes a wording gap.

## 3 · § L (law (b)): rows whose regime changed and were not re-opened

I read the 13 dispositions against the source. L.1–L.13 are correct as far as they go. **One row was missed: `TA-X-21`** (WARN-3). v1.14 treated it as a CITATION. It re-cited four `threat.py` sites, but the v3.9/v3.10 GD folds changed **which quantisation sites are live**. Two of the four cited sites never execute under `V311-FULL`, and ten new sites do. KP-178 law (b) applies to exactly that: the fold made a state reachable, and the row that reads it was not re-opened.

Rows I checked and found adequately covered or unaffected:
- `TA-X-14`: cells run ≈ 4× longer, but 0 energy dry-outs were measured on 25/25.
- `TA-X-19`: no arrival limb is configured.
- `TA-X-20`: kit unchanged.
- `TA-X-24`: no actor hashing in any new module.
- `TA-X-26`: pack additive.
- `TA-X-28`: covered by L.7.

## 4 · v1.15 against Matt's KP-240 ruling

- **Only the two Q104 rows are restated.** The prereg commit touches one file. § 0 lists `TA-X-30` and `TA-X-29(b)`, and nothing else moves. v1.14 is carried by FILE `5bbe7ae5…`, and I recomputed that digest myself. The budget (a fresh 2), § G.1a and § F.5 rules 1–15 are carried.
- **`TA-X-30` follows Q104(1).** The FORM `min(v·dt, max(0, dist − op))` is unchanged and only the operand moves. The operand table matches the code at `969fbd8d`. I checked `run.py:2369–2385`: `halt_for`, then `waypoint` with op 0. For pets I checked `run.py:1996–2003`: 2.4 on the incumbent walk, `pet_target`'s halt otherwise. (b′) is under R-G4-V311 with its vacuity printed. ⚑ The printed vacuity is incomplete; see WARN-1.
- **`TA-X-29` follows Q104(2).** (b′) matches `gd_composition.py` term for term: `P = om − 1`, the LO limb, the clamped and unclamped physical legs, DoT, leech-type DoT and untouched PCL. (a), (c) and (d) are carried, and (e) is carried at `3.197066`/`4.935649` with its static-supply definition stated. Two text gaps are noted in INFO-3.
- The added emission fields and GREEN conditions implement the ruling, not a widening. They are operand provenance, non-vacuity (`n_player_arg_steps > 0`), NaN and position checks. **Faithful.**

## 5 · The conductor's KP-244 divisor ruling (int/200 + 1)

**Consistent with Q98, Q99 and the pack. Upheld.**
- **Pack.** Every fight job and `WALK` constructs the composing fold with an explicit `chaos_aether_dot_divisor=True` (`IC7-A-V311-0017`, `-0179`, `-0334`, `-0490`, `-0647`, `-0792`). `math_rules ⚑ v3p11_rows.dc1 V39-DC1-2` reads *"replaces the declared 1.0 (KP-207)"*. The oracle's own `report()` text is `int/200 + 1 (decoded, KP-212 fold 3b)`.
- **Matt authority.** Q98 (KP-207) declared 1.0 *because the divisor was undecoded*. Q99's oracle-pass-2 scope (KP-212) names *"the decoded constants (… SlowChaos/SlowAether int/200 …)"*. The decoded value therefore stands on Matt's ruling, not on the conductor's.
- **Law (a).** Only the `True` reading is passable by the oracle if such a row is ever composed, because every one of the 105,045 composing instances on the 25 cells has `divisor=True`. Binding 1.0 would plant a row the oracle fails.
- The vacuity is **stronger than printed**; see INFO-3.

## 6 · Vacuity and discriminating power

| item | presented as | measured | finding |
|---|---|---|---|
| `TA-X-30(b′)` on the 20 unwalled cells | vacuous (printed) | vacuous | — |
| ⚑ `TA-X-30(b′)` on **W1** | **"tested"** (v1.15 § K′ table) | 171,478 clamp calls, **0 returned a stop** | **WARN-1** |
| divisor clause | "unexercised on the 25 cells" | **unreachable**: 0 SlowChaos/SlowAether DoT rows on any of 507 roster + 68 pet profiles, 0 in the pack's offense members | INFO-3 |
| `TA-X-30(a′)` non-waypoint Pursue operand (`reach·(1−1e-9)`) | a table row, emitted as `n_pursue_reach` | **0 steps**: every Pursue approach runs through a waypoint (agrees with KP-244 and J0-F NC-3b) | INFO-2 |
| `TA-X-30(a′)` clip limb | an allowed exception ("unless the non-penetration clip shortens it") | **0 calls** to `geometry.max_admissible_travel` on 25 cells: the solver is off under `V311-FULL` | INFO-2 |
| ⚑ **25 cells** | "PASS 25/25", "20/25 clear w160" | **12 distinct trajectories** (9 clearing, 3 dying) | INFO-1 |

**The 12-trajectory collapse, assessed.** I re-derived it independently: `M0 ≡ M-POL-2-NULL` and `M-POL-2 ≡ W1-NULL` on 5/5 salts, and `W1` departs only on salts 2 and 3. Here is what it does and does not cost.
- **The arm-relation rows stay discriminating.** `TA-X-03`/`04` assert the duplication, so a port whose null arms are not inert fails them. `TA-X-05` assert a difference, and it holds 5/5.
- **Per-cell rows carry about half the independent evidence their count suggests.** "25/25" is 12/12 distinct fights. `TA-X-08`'s lethal-tick clause is exercised on **3** distinct dying trajectories, not 5.
- **W1's armed wall contributes nothing.** It makes 0 stops (`TA-X-11`, WARN-1). W1's only distinct behaviour is avoidance on two salts, so the walled-arena evidence on the reference is effectively nil. `TA-X-11` already says this in words: *"the port never needed to clamp"*.
- **Disclosure.** v1.14 discloses the collapse once, inside law-(b) row § L.3 (*"12 distinct realisations"*). It is absent from v1.14's headline counts, from the § F.5 cl. 14 residual sentence ("20/25 clear w160") and from all of v1.15, whose § K′ prints 25 rows with duplicates and "PASS 25/25". The JOIN-1 J0-F Gate-2 (collab `608eaef56`, WARN-B) found the same omission on the fixture face. **It is one shape across both runs.**

---

## 7 · Findings

### WARN-1 · `TA-X-30(b′)` is vacuous on **all 25** reference cells, not 20; the face's vacuity predicate would print "tested" on W1
- **What:** v1.15 § F.2i′.1 and § K′ say (b′) is *"tested only on W1 (5 of 25)"*, and the § K′ table marks W1 "tested". On W1, `ArenaFold.clamp_body` was called 171,478 times and **returned a stop 0 times**, so `n_wall_clamps_body = 0` (consistent with `TA-X-11`). (b′)'s antecedent, *"a step that `clamp_body` stopped"*, never occurs on any cell. Structurally, a step toward an in-disc target from an in-disc position cannot leave a convex disc. The max spawn radius is 43.546 m against a 43.716 m wall, and `travel ≤ dist − op` never overshoots. So (b′) can turn non-zero only if a port spawns outside the wall or overshoots its target.
- **Why it matters:** Matt's Q104(1) ruling premised the vacuity print on W1 being the tested arm (*"its vacuity outside W1 printed on the face"*). The emission's `pursuit.r_g4_vacuous == not arena_armed` would print **"tested"** on W1, which presents a vacuous clause as discriminating. This is the § F.5 cl. 6 / `TA-X-11` shape.
- **Cite:** KP-178 law (a) (what the oracle exercises); REVIEW_PROCESS 5; Discipline #12.
- **Fix owed (before H-7):**
  - **conductor:** rule a report-face amendment. The face prints, per cell, `n_clamp_stops` (clamp calls that returned True) beside `arena_armed`. "(b′) vacuous" prints where `n_clamp_stops == 0`, not only where no wall is armed. The face also states *"vacuous on 25/25 reference cells, W1 included (0 stops in 171,478 clamp calls)"*. No criterion, operand or expected value changes. **Relay to Matt as INFO, veto-open**, because his ruling's stated premise was W1.
  - **drax (H-4):** emit `pursuit.n_clamp_calls` and `pursuit.n_clamp_stops`.

### WARN-2 · `TA-X-13`: v1.14's law-(a) evidence is false as printed, and gamora's checker has a dead clause
- **What:** v1.14 § 0.2 prints *"PASS 25/25 (every crit row is monster-sourced)"*. On the 25 cells there are **4,281 crit rows sourced by player summons** (`ps_…`, `summons.py:706 SUMMON_ID_PREFIX = "ps_"`, *"the player-summon id space"*; `damage_source_tag = "summon"`, targets roster bodies; 127–206 per cell). There are 132 monster-side crit rows and **0** rows sourced by `player`. The summon crit is the decoded PTH tier from `summon_offense.swing` (`th.resolve_hit`, draw site `V9-SITE-17`), a legitimate oracle mechanism. `check_v1p14.py:258` *intends* to fail on player-summon crits (`crit.get("player_summon", 0) == 0`), but its classifier keys on `startswith("summon")` / `"player_"` and never sees `ps_`. The clause is dead, and the PASS it reports does not answer the question the checker itself asks.
- **Gate reading:** the row's text is *"count of player rows with `is_crit == true` is 0"* and its basis is `V0 · CritLimb LO`, the player-kit crit limb. Under that text the player's own rows are in scope and the PTH summon tier is not, so **the oracle passes**. The port's emission (`n_player_crits`) uses the same reading. Under the inclusive reading the instrument's author evidently intended, the oracle **fails** `TA-X-13` by construction on 25/25 cells. That would be the `TA-X-16` shape, a faithful port failing the row.
- **Cite:** KP-178 law (a); KP-137 (a restatement is Matt's); REVIEW_PROCESS 4.
- **Fix owed (before H-7):**
  - **conductor:** rule the scope in the ledger: *"player rows = `source_id == "player"`; player-summon PTH crit tiers are out of scope."* That is the gate's reading. If the conductor holds the inclusive reading instead, law (a) fails and it is a **HALT to Matt** (a restatement, KP-137).
  - **gamora:** correct the classifier (`ps_` → `player_summon`), drop or re-scope the dead clause per the ruling, and file a corrigendum line for v1.14 § 0.2's printed basis. No prereg edit and no expected-value change.

### WARN-3 · `TA-X-21`: law (b) miss; the cited live-site list is stale under `V311-FULL`
- **What:** these are line-level liveness counts on M-POL-2, salts 0–4, from every `round(` line in every `simulation/kc2` module. The probe run's trajectory digest equals the unprobed run.
  - Of v1.14's four cited sites, `threat.py:1613` (519 hits) and `:1774` (1,461) are live. **`:1813` (the cooldown write) and `:2182` (the DoT expiry) never execute.** `:1813` is superseded by v3.9 GD engagement's `choose_slot`. `:2182` is bypassed because the DoT timeline is active and quantises at `dot_timeline.py:380`, live 2,888 times.
  - **Ten live `int(round(` sites are uncited**, all minted by the v3.9/v3.10 folds that now govern the threat path's slot timing:
    - `gd_engagement.py:121` (delay gate, 1,790 hits) and `:187` (cooldown, 2,218);
    - `gd_reposition.py:364`, `:365`, `:519`, `:530`, `:554`, `:726`, `:731`, `:739` (WaitToAttack poll and roam, RFA timer; 48–60,022 hits each).
  - Every live site is `int(round(…))`, half-to-even, so **the rule passes**. What is stale is the site list.
- **Why it matters:** the port's `ta_x_21` emission and H-7 grade against the cited list. A port that quantised GD cooldowns or RFA timers differently would pass `TA-X-21`, and only G3 would catch it. The row's own text says *"Re-verify the live site list at emission; the site list is a property of the code"*, and v1.14 re-cited line numbers without re-verifying liveness.
- **Cite:** KP-178 law (b); Discipline #73; the row's own clause.
- **Fix owed (before H-7):**
  - **gamora:** file the measured live list at `969fbd8d` (all arms) as a dated note, not a prereg edit, under the row's own "re-verify at emission" clause. Also state the row's module scope: whether the pre-v3.8 live sites in `dot_timeline`, `channel_policy`, `control_application`, `summons` and `summon_offense` are "threat path".
  - **conductor:** confirm this falls within the row's clause (a citation, not a restatement). If not, **HALT to Matt**.
  - **drax (H-4):** re-point `ta_x_21` to the live list.

### INFO-1 · 25 cells = 12 distinct trajectories; the face does not say so (§ 6)
- **Fix (conductor, report face, before the attempt):** every per-cell count on the face prints *"25 cells / 12 distinct trajectories (9 clear, 3 die)"* beside it, and § F.5 cl. 14's residual (2) reads "20/25 cells (9 distinct clearing trajectories)". No criterion changes.

### INFO-2 · `TA-X-30(a′)`'s two partial vacuities
- **Non-waypoint Pursue operand.** The class `op = reach(S)·(1−1e-9)` has **0 steps**. A Pursue approach always runs through a waypoint (op 0), and `reach(S)` enters only through the waypoint's stop point. The travel law does not grade that stop point; only `n_reach_ne_pack`, a load-time equality, touches it.
- **Clip limb.** The non-penetration solver is **never called** under `V311-FULL`: 0 calls on 25 cells. Yet (a′) admits any clipped step that is "strictly shorter, on the ray". A port with a live clip passes (a′) where the oracle has none; only G3 catches it.
- v1.15 § F.2i′.1 ("What the row now proves …") scopes the state questions to G3, which covers this in principle, but neither item is printed as a vacuity.
- **Fix (conductor, report face):** print both as UNEXERCISED-ON-REFERENT, and flag any port `n_clipped > 0` on the face as a G3-attention item. No criterion changes.

### INFO-3 · The divisor clause is **unreachable**, not merely unexercised; and two text gaps
- **Unreachable.** There are 0 SlowChaos/SlowAether DoT rows on any of the 507 roster and 68 pet profiles the graded loader builds, 0 in the pack's `monster_offense.json` / `monsters.json`, and 0 under `data/kc2`. `V39-DC1-2` itself records `population_on_the_v3p8_oracle: 0`. v1.15's *"if the port's realisation composes such a row, the row grades it"* can therefore occur only if the port fabricates a row. Print it as **UNREACHABLE-IN-PACK**.
- **Text gap 1.** Each `a8` fight job also constructs a **default-`False` sibling** `CompositionFold` (`-0018`, `-0180`, `-0333`, `-0491`, `-0648`, `-0793`; the v3.8 base `Folds`), which v3.9 replaces before the fight. A harness "configured from `a8`" must take the explicit `True` row. v1.15 does not mention the sibling.
- **Text gap 2.** v1.15's (b′) states `a_dur = int/200 + 1` but omits the code's fallback `intelligence is None → 1.0` (`gd_composition.py`).
- **Fix (gamora, a note line; drax, H-4 awareness):** no value moves.

### INFO-4 · § B.0's completeness predicate does not name the shared guard's G2 (w160 tick cap)
- It is harmless here. B.0 requires `termination_reason ∈ {board_empty, player_died}`, which excludes a tick-cap stall, and the shared module re-run gives 25/25 complete (longest wave 968 of 4,000 ticks).
- **Fix (gamora):** cite the shared module (`9c756081`, FILE `5f3f4f1e…`) as the guard of record in the next note, as the J0-F re-freeze did.

### INFO-5 · Forward note for H-7 (port; not graded here)
- At godot HEAD `1e914c2`, `kc2rt_fight.gd :: n_player_crits` is declared (`:382`) and reset (`:6393`) but **never incremented**. The port's `TA-X-13` emission is a constant zero. That is consistent with v1.8's "config identity" class (`crit_mult = 1.0`), but H-7 should read it as structural, not measured.
- godot HEAD has also moved since v1.15 cited `a07f7f5`.

### INFO-6 · Process self-report (gate hygiene)
- **(a)** The session scratchpad is shared across sessions. While setting up I moved gamora's existing `v114/` and `v115/` scratch folders and overwrote four instrument copies in them with the committed bytes (verified `cmp`-identical to the commits). I restored their location within a minute. No committed artifact was touched.
- **(b)** The probe's first run wrote five `probe_*.json` files into the engine's `src/` because the oracle requires that cwd and I had not made the output path absolute first. I removed them at once, and the committed probe now resolves the output path before the `chdir`. No tracked engine file changed.

---

## 8 · Action

- [ ] **conductor (gandalf):** WARN-1 report-face amendment + relay to Matt (INFO, veto-open). WARN-2 scope ruling (or HALT to Matt). WARN-3 confirm citation-class (or HALT to Matt). INFO-1/INFO-2 report-face prints. **All before H-7.**
- [ ] **gamora:** WARN-2 classifier + corrigendum line. WARN-3 measured live-site list (all arms) as a dated note. INFO-3/INFO-4 note lines. No prereg edit.
- [ ] **drax (H-4):** emit `pursuit.n_clamp_calls` / `n_clamp_stops` (WARN-1); re-point `ta_x_21` to the live list (WARN-3); configure `CompositionFold` from the explicit `True` `a8` row (INFO-3).
- [ ] **Matt:** nothing is owed unless the conductor routes WARN-2 or WARN-3 as a restatement. WARN-1 is for your information: your Q104(1) premise that W1 tests (b′) does not hold on the reference.

## 9 · References

- Preregs: `agentic_orchestration/gandalf/notes/2026-09-20-kc2-play-ta-prereg-v1.14.md`, `…-v1.15.md`. Ledger: `agentic_orchestration/gandalf/notes/2026-09-20-kc2-play-run-charter.md` (KP-137, KP-178, KP-207, KP-212, KP-238 … KP-244).
- gamora's instruments: `agentic_orchestration/gamora/analyses/2026-10-02-kc2-play-prereg-v1.14/`, `…-v1.15/` (every FILE digest re-verified against both preregs' § Z tables).
- Engine: `src/reincarnated/simulation/kc2/{run.py,locomotion.py,gd_engagement.py,gd_reposition.py,gd_composition.py,arena_fold.py,threat.py,dot_timeline.py,summons.py,summon_offense.py,c11a_corrections.py,referent_lineup.py}`; `scripts/gamora_kc2_play_v3p{8,9,11}_oracle_2026_10_02.py`; `scripts/gamora_join1_obs1_guard_2026_10_02.py`. Godot: `kc2_runtime/sim/kc2rt_fight.gd`.
- Related gate: JOIN-1 J0-F Gate-2, `agentic_orchestration/qa/findings/2026-10-02-join1-j0f-oracle-half-gate2.md` (collab `608eaef56`).
- **Instruments of this finding** (`2026-10-02-kc2-ta-prereg-v1.15-h6-preread/`, sha256):

| file | sha256 |
|---|---|
| `h6_gate_probe.py` | `37a4a562a00d4dc1b623c4c382887440ca4529f5df1a4270d31a18adfc4ef730` |
| `h6_gate_check.py` | `c1917844ee785d99c7cf7729080b6957420d34fdefcce5e051b14a0dfa789c5d` |
| `h6_crit_probe.py` | `3f82fdc696c05ef115b47065afd8ad7d205fdac7038519151df5428e84ef6b9b` |
| `h6_rerun_gamora_instruments.sh` | `bd26a83e3af8079871f3841a0e9f3d4f180186ddfa392420c5c6f89f00aa55e9` |
| `h6_rerun_compare.py` | `d9f55f78d3dab8bbf897fc3ef494577604333b77d33cc87efd19e91949f623f0` |
| `h6_gate_results.json` | `8c84a887485fcd8a7b28cae861c06ed7a9234cc22ddda57588289de01a138a03` |
| `h6_rerun_compare.json` | `b7410b771c3a75fba43532b4f1db92dd332c660e50b380b3222d3432e2ec3c9f` |
| `probe_M0.json` | `0b1cb8773fccc3cb6427102c603ade74bd355c6e0080bf64aa81daec20032993` |
| `probe_M-POL-2.json` | `0de82d05bae19a16ff8dd8d2b28178c82102b4e6f2258c547b20f662e812cf6f` |
| `probe_M-POL-2-NULL.json` | `adf31209d93211f526af945fb5e96e9b7cfb6171a35117f68a6ee8fbd3300d0e` |
| `probe_W1.json` | `fb37cf1bf9cbd27092cbaf827e81ec90177641816ec57bf09aeca6a59b479c39` |
| `probe_W1-NULL.json` | `ddfd2ed332767ab5ea9e52e6737434fa3360acf121ff9efbb4d161a395065fd9` |
| `probe_round_M-POL-2.json` | `59d2f78f7f4f6fad85ef81eeeb920097a15d1942626f5272e74775a01971f745` |
| `crit_M-POL-2.json` | `87d1a220fc2ce0c7446a4e212bf8ee3b85b61f54794a67df03aadbc9d22ca0b3` |
| `crit_W1.json` | `97c3f94cbb4ed962f557f91d9ff7f1869351dedaa1298cf2bd1fc4bbf4054f6c` |

*Filed 2026-10-02 by **jack-ryan**, H-6, Run KC2-PLAY; conductor gandalf. Neither prereg was edited. No production code. No push.*
