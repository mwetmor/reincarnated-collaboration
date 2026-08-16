# KC2-PM4 · LAP V — THE ROSTER DECODE · PRE-REGISTRATION

**Agent:** legolas (UNKNOWN-RESEARCHER) · **Conductor:** gandalf (RUN-CONDUCTOR)
**Authority:** `R-PM4-56 part 2`, ledger rows `L-47` + `R-PM4-56`. Matt's word (2026-08-15, Q58,
verbatim): ***"fix the bonus spawn system and count-model holes now."*** **Date:** 2026-08-15.

**Discipline in force:** GL-6 (full 64-hex on every input and output; no truncated handles —
`R-PM4-55 part 2`) · GL-12 (DECODE-NEVER-ESTIMATE; UNREACHED honest per limb) · NOTE-9 (no repair
outside my own seam; carried constants named with their emitting lap) · Law-3 (I decode what the
game DOES; the referent's 19–36 is a GRADE, never an input) · **L-46 carry (NEW, and the reason
this file exists alone): THIS FILE COMMITS BY ITSELF, IN ITS OWN COMMIT, BEFORE ANY INSTRUMENT OF
THIS LAP RUNS.** Priority is git-attested, not self-attested.

---

## § 0 — RECONNAISSANCE PRECEDING THE HASH (declared in full, per CL-10)

Everything below was read or run **before** this file was written. **None of it is a result of this
lap.** It is orientation, and it is named so the reader can discount it. If any statement here
later appears in `pm4v_findings.md` as a finding, it is a defect and I will label it one.

**Documents read:**

1. Run charter rows `L-42`…`L-47` and `R-PM4-56` (verbatim), plus the Q58 row in
   `canonical/matt_decision_needed/README.md`.
2. gamora's I-21 landing note §§ 4.1–4.3, 5, 11.2, 11.3 — in particular the `C-12` / `C-13` pricing
   table and the two-branch `EMPTY_ROSTER_DISPOSITION` naming.
3. My own `2026-08-07-u9-spawnmin-operator-order.md` §§ 5.2–5.5, 6, 7 — the count model I myself
   authored, including the Lua excerpt that first named `bonusSpawnStatus`.
4. My own Lap S findings § `UNREACHED-S7`; my own Lap U findings §§ 2.1–2.5 (method standard),
   § 6 (UNREACHED census), § 8 (hand-off DO-NOTs).
5. The sim's `src/reincarnated/simulation/kc2/wave_engine.py` — `count_bounds`, `roll_wave`,
   `_weighted_pick`, `expected_counts`, `count_model_provenance`, and the `P06_*` /
   `EMPTY_ROSTER_*` constant block. Read so that the hand-off can name the exact call site each
   decoded term lands on, and so that "what the sim currently does" is stated from its source
   rather than from a summary.

**Shell reconnaissance run before the hash — six facts, each of which shapes a hypothesis below and
is therefore declared here rather than presented later as a finding:**

- **R-0.1** The corpus of record is `vendor/grim-dawn-edition-III-20260808` (base `database.arz`
  = `2ad6d379…83bfd`, matching Lap U's pinned digest exactly). The binaries of record are
  `vendor/grim-dawn/{Game.dll,Engine.dll}`, digests byte-identical to Lap U's.
- **R-0.2** **`bonusSpawnStatus` is NOT a `.dbr` field name.** A string-table sweep for `bonus` over
  all eight archives returns no such field. It is a **Lua local** (my own U9 § 5.4), assigned from
  `gd.survival.rewards.checkBonusStatus()`. Limb (a) is therefore a **script + record + text**
  decode, not a `.dbr` field decode. This reframes the target and I say so up front.
- **R-0.3** `mods/survivalmode/resources/Scripts.arc` exists (`47e6426d…b009`) and is the expected
  home of `game/events/survivalevent.lua` and `game/survival/rewards.lua`.
- **R-0.4** The survival mod's own string table carries `Complete Event - Ultimate + Bonus Spawns`,
  i.e. bonus spawns are a **named, shipped Crucible concept** with UI/achievement surface — not an
  inference of mine.
- **R-0.5** The sim's roster path is: `pools_for(wave, bonus_spawns_enabled)` → per spawn point
  `_weighted_pick` (exactly ONE alternative) → `count_bounds` → `rng.randint(n_min, n_max)` for
  regulars → a HARD gate `rng.random() < champion_chance/100` → `rng.randint(c_min, c_max)` for
  champions. `EMPTY_ROSTER_DISPOSITION = "NO_OP_ON_EMPTY"` zeroes `n_min = n_max = 0` when the
  alternative's regular roster is empty. `P06_BONUS_SPAWNS`/`P06_OPERATIVE_LIMB = False`;
  **`P06_CODE_DEFAULT = True`, i.e. the sim's own code default already disagrees with its operative
  limb and says so.**
- **R-0.6** `pe6_crucible_wave_pools_v2.csv` (`bbdc18f1…5587`, 1,998 data rows) is the DB-CITED
  composition sidecar the sim reads, and carries `spawn_min`, `spawn_max`, `champion_chance`,
  `champion_min`, `champion_max`, `roster_n`, `champ_roster_n`, `pool_weight`, `spawn_point`,
  `ignore_game_balance` per alternative row.

**I have NOT looked at, at the instant of this hash:** any Lua body inside `Scripts.arc`; any
disassembly of any spawn/proxy/count symbol; any per-wave p06 row for waves 150–160; any count
arithmetic for any wave of the band; any grade against 19–36. **Every number this lap reports is
unobserved right now.**

---

## § 1 — INPUTS, PINNED (full 64 hex; re-hashed at instrument start, HALT on mismatch)

| input | expected sha256 |
|---|---|
| `edition-III/database/database.arz` | `2ad6d379285cfb745462316949e8d59e9450cb58a13f9ffa2fdeb70193183bfd` |
| `edition-III/gdx1/database/GDX1.arz` | `431e64e1d372e4ebee5d1048d3aca458923e1df8c97844274636f5373a01e292` |
| `edition-III/gdx2/database/GDX2.arz` | `13fa0b93be15835958968ad672b9efa5159d7221a279aca791590390dd81a072` |
| `edition-III/gdx3/database/GDX3.arz` | `e990e1265f14ff2ee241658433d4d666d399a5b0be27543ae9481fc97d6a2ae4` |
| `edition-III/mods/survivalmode/database/SurvivalMode.arz` | `e9f6e2213eada8f5ffcc4fc430395b43c95384b745b629def096dbb2e7da29b6` |
| `edition-III/survivalmode1/database/SurvivalMode1.arz` | `6ac10d6180bfa8491edfc89946d1cfbf166c5ca6442c5862ecf6947290021252` |
| `edition-III/survivalmode2/database/SurvivalMode2.arz` | `940e40344e9dde53bfac8ff6576940d52ebfece600adeabe3774f9f0c3071e95` |
| `edition-III/survivalmode3/database/SurvivalMode3.arz` | `e848791e4b15496670e4c78832075d9868e7b502e6eed93715c24e894902e12a` |
| `edition-III/mods/survivalmode/resources/Scripts.arc` | `47e6426d9534e0ddd5f867ca4d2640e5aa42cc8ffd68baa1db7e8870a61fb009` |
| `edition-III/resources/Scripts.arc` | `323b46deb08abfe41f3b86d3652777fc1f3f6f586b7579fde46d50d8270df672` |
| `edition-III/survivalmode3/resources/Scripts.arc` | `2c376262c0969eb247af46fb88047a02ac1e24447d291f7d3a3e438934c0ed6b` |
| `edition-III/mods/survivalmode/resources/Text_EN.arc` | `fa0689778ef0badb4472213684733e958edfbeeebb45086830939c9693b3d06e` |
| `edition-III/database/templates.arc` | `679db83f019020ef7d4d27be8e61203006ee94e5c582dd8a59642f3fddd54602` |
| `vendor/grim-dawn/Game.dll` | `4876d6bdb69cca71cfa987652cbd7a42cf6d5578564d02d09aaf9b55c078ab02` |
| `vendor/grim-dawn/Engine.dll` | `7141b51ae61b396fd0743da9e51471043329c51b3bb61d0037b2ce934864c87c` |
| `engine/data/kc2/pe6_crucible_wave_pools_v2.csv` | `bbdc18f12aab8e3788eac229ed1871a88ed7790dc3d1786c509cd26c076e5587` |
| `engine/data/kc2/pe6_pool_ignoregamebalance.csv` | `40182de26b64cc03e936d9504274e9135f10373979e73eccc224ec732aff77d3` |
| `engine/src/reincarnated/simulation/kc2/wave_engine.py` (read-only, comparator) | `d5c232d7f7e09c7e47b3782afe28b0d14a9e0ac0f43b4781f1d8c53767e320ba` |

**Carried constants, each with its emitting lap named (NOTE-9), used unchanged and never
re-derived:** Gladiator `spawnMinModifier = 120 %`, `BASE_ADDITIVE = +1`, `spawnMinAdj/spawnMaxAdj
= 0` over the band, `spawnChampionMinAdj/MaxAdj = +1` over the band (all U9 §§ 2.1/2.3/5.3) ·
array-lookup law "fighting wave `w` reads the cell LABELED `w`" (`L-33`) · the referent's peak
living inside 11.64 m = **19–36, median 25, a LOWER bound** (Lap U `B-1`, via I-21 § 4.1) · the
as-run sim roster 151→160 = `28,18,24,13,18,19,21,33,9,5` (I-21 § 4.2, comparator only).

---

## § 2 — BOUND DIRECTIONS AND KNOWN CENSORING (fixed before any measurement)

Stated first because two of them **kill** grades I would otherwise be tempted to claim.

* **B-1 (carried, Lap U).** A nameplate proves a living body; its absence proves nothing. The
  referent's 19–36 is a **LOWER** bound on living bodies inside the window. A decode that lands at
  19 has not "matched" it.
* **B-2.** `roster(w) ≥ living(w, t)` for every `t`, always, because bodies die and never
  un-die. Therefore **roster size is a CEILING on the concurrency functional**, and the only
  honest grade a roster decode can earn is a **necessary-condition** grade: *could* the decoded
  board ever hold 19–36 at once. A roster decode **cannot** demonstrate sufficiency; claiming it
  does would be the defect.
* **B-3.** Under I-21's pursue-all fold, 100 % of the board reaches the player, so the ceiling in
  B-2 is tight in the arrival sense and loose in the survival sense (kill throughput depresses
  concurrency). I will not adjust for kill throughput — that is gamora's seam (NOTE-9), and any
  such adjustment from me would be modelling, not decoding.
* **B-4.** The referent-side *value* of `bonusSpawnStatus` in Matt's own sitting is a **fixture
  fact**, not a records fact. If the decode shows the flag is player-chosen, then no amount of
  binary reading can tell me what Matt chose. That outcome is a legitimate landing and is
  pre-declared here as such (see `V-a4`).

---

## § 3 — LIMB (a): `bonusSpawnStatus` — HYPOTHESES AND VERDICT RULES

**`DECODED` means:** a named artefact (Lua function body, `.dbr` field, `.arc` text entry, or an
exported symbol at an address) whose content I can **read**, and whose consequence I can state
without interpolation. Anything less is `INFERRED-WITH-EVIDENCE` or `UNREACHED`. Nothing else earns
the word (GL-12).

| id | hypothesis | verdict rule |
|---|---|---|
| **V-a1** | `gd.survival.rewards.checkBonusStatus()` has a readable body in the shipped Lua, and its return is decided by a namable set of inputs. | **DECODED** iff I can quote the body and name every input. Otherwise **UNREACHED-V1**. |
| **V-a2** | The gate `id < waveEvent.numSpawns \|\| bonusSpawnStatus == true` is the ONLY place p06 is suppressed — i.e. there is no second, independent p06 gate. | **DECODED** iff a full sweep of the survival Lua for `numSpawns` / `entity[6]` / spawn-point-06 identifiers returns exactly this one gate. A second gate = a **third mechanism** → § 6 HALT report. |
| **V-a3** | Every wave in **150–160** that declares a p06 proxy is enumerable from the record corpus, with its pool alternatives, weights, and count fields. | **DECODED** iff the enumeration is a direct record read for all 11 waves. |
| **V-a4** | The referent-side value of the flag in Matt's sitting is decidable from records + binary. | **My prior is NO.** Verdict **DECODED** only if the Lua shows the flag is *forced* (e.g. by difficulty or wave index) rather than chosen. If chosen → `UNREACHED-S7` **stays open on the referent side**, is re-scoped to a *fixture* question, and is routed to the conductor for a one-line Matt question. **I will not guess it, and I will not pick the limb that grades better** (Law-3). |
| **V-a5** | The per-wave arithmetic: bodies added by p06 over 151–160 under `status = TRUE`, expected + `[min, max]` envelope, per wave, from the decoded recipe. | **DECODED** iff every term traces to a cited record field; the deliverable is `pm4v_roster_arithmetic.csv`. |

**Falsifier for the limb:** if `Scripts.arc` does not contain `game/survival/rewards.lua`, or the
function is engine-side rather than script-side, limb (a) fails as written and I report
`UNREACHED-V1` with the search path enumerated. I will **not** substitute a plausible reconstruction.

---

## § 4 — LIMB (b): THE COUNT-MODEL RESOLUTION — HYPOTHESES AND VERDICT RULES

| id | hypothesis | verdict rule |
|---|---|---|
| **V-b1** | The engine's regular-count draw over `[spawnMin', spawnMax']` is a **uniform inclusive integer** draw. | **DECODED** iff I can read the arithmetic at a named symbol/address (the `min + rand % (max-min+1)` shape, or whatever it actually is). If the symbol is virtual-dispatched and unreachable, **UNREACHED-V2** and the sim's `randint` stays **DECLARED**. |
| **V-b2** | The count resolves **once per spawn point per wave** (after exactly one weighted pool-alternative pick), not once per wave and not once per roster entry. | **DECODED** iff the Lua spawn loop + the proxy record structure jointly force it. Divergence between Lua and binary readings = a fork → § 6. |
| **V-b3** | `championChance` is a **per-pool-instance hard gate** applied **after** (or independently of) the regular draw, and champions **ADD** rather than **CONVERT**. | **DECODED** iff the gate and the add/convert question are both readable. Crate's modding-guide statement is **secondary**; a record/binary reading outranks it, and if they disagree I report the disagreement rather than averaging it. |
| **V-b4** | Of `NO_OP_ON_EMPTY` / `CONJURE_FROM_TEMPLATE` / `PROMOTE_TO_CHAMPION_DRAW`, the engine implements exactly one. | **DECODED** iff a readable code path or a template/record constraint adjudicates it. **Explicit anti-fit clause: `CONJURE_FROM_TEMPLATE` is the branch that grades better (+11 bodies, and it lands AC-10.4 inside T-2). If my evidence for it is anything weaker than my evidence would need to be for `NO_OP_ON_EMPTY`, I have fitted, and I will say so and rule UNREACHED instead.** |
| **V-b5** | The draw is seeded such that the same wave index reproduces the same roster within a sitting. | **My prior is that this is UNREACHED** — a global-RNG question I expect not to reach. Declared so it cannot be claimed later. |
| **V-b6** | The `spawnMin` **operator order** residual `U9-1` (`(base+add)×mod` vs `⌊base×mod⌋+add`) is **out of scope** for this lap and stays as U9 left it. | Declared, not tested. If the disassembly answers it for free, I report it as a **bonus finding**, not as a scope expansion. |

---

## § 5 — LIMB (c): THE PREDICTION AND THE GRADING PLAN — FIXED NOW

**The order of operations is fixed here and is not negotiable afterwards:**

1. Decode limbs (a) and (b). **No grade is computed during this step.**
2. From the decoded recipe alone, compute the per-wave roster for waves **151–160**: expected value
   and `[min, max]` envelope, plus the champion split. Emit as `pm4v_prediction.json` **and hash
   it**. The hash is recorded in `pm4v_digests.json` under `prediction_before_grade`.
3. **Only then** compare against the referent's 19–36 / median 25.

**The grade is defined now, in full, so it cannot be redefined to flatter the result:**

* **G-1 (the necessary-condition grade, PRIMARY).** For each wave `w ∈ 151…160`: does the decoded
  roster **envelope maximum** reach the referent floor of **19**? Report the count of waves that do
  (`k/10`) and the per-wave table. Under B-2 this is the only grade a roster decode can earn.
* **G-2 (the central grade).** Decoded **median expected roster** over 151–160 vs the referent
  median **25**, reported as a ratio and a difference, with the explicit reminder that 25 is a
  LOWER bound so a ratio of 1.0 is a **floor**, not a match.
* **G-3 (the wave-160 grade).** Decoded wave-160 roster (expected + envelope) vs **19**. This is the
  wave the run died on and the wave the sim fields 5 bodies at.
* **G-4 (the delta grade).** Decoded roster vs the as-run `28,18,24,13,18,19,21,33,9,5`, per wave
  and in total — so the conductor can see what the amendment actually buys, separately from whether
  it is enough.

**PRE-REGISTERED PRIOR (mine, stated so it can fail).** From gamora's pricing (`C-12` +25, `C-13`
+11 over the band) I expect, *before decoding anything*:

* **PRIOR-1** — decoded median expected roster over 151–160 lands in **[20, 26]**.
* **PRIOR-2** — **at least 3 of 10** waves still have an expected roster **below 19**.
* **PRIOR-3** — wave 160's expected roster lands **below 19** (my point guess: 8–12).
* **PRIOR-4** — G-1 returns **k ≤ 7** of 10.

If the decode contradicts these, the decode wins and I report the prior as **failed**, loudly. A
prior that is never allowed to fail is decoration.

---

## § 6 — HALT AND FORK RULES (binding, from `R-PM4-56 part 4`)

* **Third-mechanism HALT.** If a roster-relevant mechanism beyond the two named holes surfaces —
  any additional spawn point, any wave-level cap, any concurrency limiter, any respawn/reinforcement
  path, any difficulty-conditional multiplier not already in the U9 model — I **do not decode it**
  and I **do not price it**. I report it as a named finding `F-3M-*` for the conductor, flagged as a
  **run-level HALT trigger**. Scope does not expand inside this lap.
* **Verdict-divergent fork (Law-3 tripwire).** If two readings of the same mechanism are both
  defensible and I notice myself weighing them by which lands nearer 19–36, I **stop**, publish both
  readings with their evidence, and label the item **VERDICT-DIVERGENT — conductor's call**. I do
  not break the tie.
* **Read-only.** Nothing is written outside
  `agentic_orchestration/legolas/notes/2026-08-15-kc2-pm4-lap-v-roster-decode/` and
  `agentic_orchestration/research/scripts/` (instrument sources). The vendor tree and the engine
  repo are never written.

---

## § 7 — DELIVERABLES DECLARED

| file | contents |
|---|---|
| `PREREGISTRATION.md` | this file — **committed alone, before any instrument runs** |
| `pm4v_findings.md` | headline findings `F-*`, per-limb decode with evidence at named record fields / Lua lines / binary addresses, the graded prediction, UNREACHED table, defect table `D-V-*`, § hand-off with DO-NOTs |
| `pm4v_prediction.json` | the decoded per-wave roster prediction, **hashed before any grade is computed** |
| `pm4v_roster_arithmetic.csv` | per wave × spawn point × pool alternative: cited count fields, decoded bounds, expected contribution |
| `pm4v_bonusspawn.json` | limb (a) machine artefact — the Lua decode, the p06 wave/pool enumeration |
| `pm4v_countmodel.json` | limb (b) machine artefact — the decoded draw semantics with addresses |
| `pm4v_digests.json` | full-64 sha256 of every input, every instrument, every output, plus this file's own hash and its UTC hashing instant |

---

*Hashed and committed alone by legolas (UNKNOWN-RESEARCHER), 2026-08-15, before instrument I-V1.*
