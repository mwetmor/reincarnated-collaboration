# JOIN-1 RUN — charter v0.2 (DRAFT, NOT LAUNCHED)

> **STATUS:** v0.2 DRAFT, 2026-09-29, gandalf (`ARCHITECT` → prospective `RUN-CONDUCTOR`). **NOT LAUNCHED.** v0.2 is the **Gate-1 DISCHARGE** of v0.1 (file sha256 `b8c2cb92…`, commit of record in git): jack-ryan Gate-1 `qa/findings/2026-09-29-run-JOIN-1-charter-gate1.md` (`570251ee4`), **BLOCK-narrow, 7 BLOCK / 10 WARN / 7 INFO**, every item dispositioned at **§ 9**. Launch awaits: (1) jack-ryan Gate-1 **re-check**, (2) precondition **J-P2** (the golden-master instrument note), (3) **J-P1** (the REFERENT-v1 seal), (4) Matt's launch sheet (§ 6) and launch word. Paper-only prep authorized by Matt at seal-lap **L3** (KC2-PLAY ledger KP-84).
> **Course of record:** `2026-09-28-join-key-architect-pass.md` **§ 8 governs** (Q85–Q89 + E-1, KP-83). **Canon:** `canonical/reap-die-rise-engine/era-substrate-architecture-2026-07-25.md` (three layers · fidelity-grade LAW § 4 · E-1 RULED · E-2 open).
> **P0 input (landed):** elrond `elrond/notes/2026-09-28-join1-p0-internal-boundary-census.md` (`78797db4b`; KP-85). **Predecessor:** Run KC2-PLAY (closes at the REFERENT-v1 seal, Q89).

---

## § 0 — Intent (whose words, what outcome)

**Matt, 2026-09-28:** *"finish making this as a join key to being in other kits from other ARPGs by first testing out its viability as an arena replica and then tweaking the replica until it sits in between our games and contains what is needed to join the other kits in."* · R-J1: *"Between grim dawn and the other games.. then we leave levers open specifically to be tweaked as we go to reach our own version of fun."* · Q86: *"Is there any reason not to simply add all of the mechanisms into the game? … we will run everything through the battle sim and tune the kits to the game's balance thresholds."*

**Terminal artifact:** the EoR arena running **three configurations of one runtime**: `ORACLE` and `PLAY`, **invariant by assertion (§ 4.7), not by prose**, and **`JOIN`**. `JOIN` hosts kits from other games: their kit-internal mechanisms enter **natively**; the kit↔world boundary is adjudicated by **ONE rulebook** (Grim Dawn's rules as default, widened only by **lever**). **D2 Whirlwind Barbarian** runs in it beside the Warlord (**"runs" is defined at § 4.5**), and the **golden master** (§ 4.3) stays green throughout. The run **ENDS at the handoff**. Everything past § 4.5's mechanical definition, including whether the Barbarian *feels* right, is the post-run HITL's.

## § 1 — Bounded substrate (frozen at launch; **digests DERIVED at launch and labelled FILE vs ROWSET**, per KP-101)

| # | Substrate | Pin |
|---|---|---|
| J-S1 | **REFERENT-v1**: the sealed pack (baton v3.4.2; both pack digests are **ROWSET-shaped**: computed over member lists under the manifest's own law), runtime digest, register hash, T-A grade, Matt's T-C word | the seal record; digests derived at launch, never carried from this text |
| J-S2 | **The P0 census**: **46 classed rows + 3 cross-cutting misfits (census § 7.3–7.5) = 49** · 15 INTERNAL / 25 BOUNDARY (8 AS-IS · 14 WIDEN · 3 GD-EMPTY) / 5 OUT-OF-ARENA / 1 HELD · 16 candidate levers · boundary list extended by target multiplicity, movement↔engagement coupling and the damage-family registry. **D2 WW Barb: 14 rows, 9 BOUNDARY (the § 4.5 coverage denominator).** | `78797db4b` |
| J-S3 | **The kit** `d2-ww-barb`: `Skills.txt` rows 151 + 149 (D2 1.13 classic, `fabd/diablo2 @ 45112569…`, DATAMINED) + the D2 formula set (MODEL-VERIFIED) + `kits-export/d2-ww-barb.json` | derived at launch |
| J-S4 | The corpus EoR kit `kits-export/gd-eor-warlord.json` (**APPROX**) + the kit compiler (`simulation/kit_compiler/`) | derived at launch |
| J-S5 | The seal lap's instruments: U-P-N-3/4 bodies-in-disc census, the heal-ratio probe, the T-A harness | commits of record |
| **J-S6** | **The SEALED ORACLE AND PORT**, preserved: the oracle at its seal commit (git tag `kc2/referent-v1-oracle`) and the runtime at its sealed digest (tag `kc2/referent-v1-runtime`), so every replay runs against **the sealed code, not its successor** | tags cut at the seal; digests derived |
| **J-S7** | **The D2 frontier TABLES:** `MonStats.txt`, `MonLvl.txt`, `Levels.txt` from the same `fabd/diablo2 @ 45112569…` commit (DATAMINED; on disk at `research/datamine-acquisition/d2/raw/`). ⚑ The tables are pinned; **the frontier POINT (which area/difficulty is the WW Barb's home frontier) is NOT** (see § 4.5 and commission C-12) | derived at launch |
| **J-S8** | **The REFERENT-v1 NUMERIC FIXTURE:** the sealed run's emitted, boundary-determined quantities under `ORACLE`, for oracle and port, frozen per the J-P2 instrument note | frozen at the seal; FILE digest labelled |

**Named out-of-scope, pre-declared:** the house profile (Phase C) · any lever moved off its GD setting without a ruling · era profiles (E-2 beyond GD's own checklist) · PoE lanes beyond paper · the OUT-OF-ARENA rows · allies and party scope (dockets 2/12, ruled) · loot and progression · **kit #3 / non-physical kits (JOIN-2, J-L2)**.

## § 2 — The central design

1. **Union + one boundary rulebook** (Q86). A foreign kit's resources, skills, leech, accumulators and procs are **INTERNAL**: ported natively with their home data at their lane's grade. Hit resolution, damage-family vs resistance, mitigation order, CC/status on monsters, the tick clock, target multiplicity, movement↔engagement coupling and the damage-family registry are **BOUNDARY**: one rulebook adjudicates them for every kit.
2. **The rulebook starts as Grim Dawn's, extracted.** Today it is welded to one character's operands (P0 finding 5). **J2 separates FORM from OPERAND.**
3. **Levers.** Every WIDEN row becomes a lever: `id · primitive · gd_referent_value ∈ {value | NONE — no GD rule} · per-game settings + grades · range · load class · status OPEN`. ⚑ **A registry that cannot say "GD is silent here" launders silence into a default** (census § 7.1). **Two GD-EMPTY rows have no mechanism to parameterise: L-14 (player projectiles) and L-15 (monster debuff lane). They are BUILD ITEMS, not levers.** **L-16 `agency_model` is a settable lever** ({player-driven (GD default) | autonomous}).
4. **Golden master: the line in the sand, as a DIFF, not a re-grade.** See § 4.3. **A lever change that breaks it is a regression, not a design choice.**
5. **The ablation map (the bridge).** Before any lever moves, each mechanism is switched off alone under the scripted pilot, and the move in the feel metrics is recorded (HP occupancy, energy excursion + ceiling duty, wave durations, frac-moving, terminal wave, heal:intake, bodies-in-disc). This classes every mechanism **LOAD-BEARING / INCIDENTAL** and yields **GD's E-2 checklist by measurement**, **under independent gate (§ 5 J0).**
6. **E-1 (ruled): tune toward our balance thresholds; home margin measured and recorded.** In JOIN-1, **record only** (J-L3). **The fidelity-cost table prints on its own face any margin that could not be measured, with the reason.**

## § 3 — Fit test

- **F1 Enumerable? YES:** J-S1..S8; 49 census items (46 + 3), 16 levers, one kit.
- **F2 Decidable? YES as of v0.2.** Every § 4 row now has a pass rule a run can check. The feel verdict, and anything past § 4.5's mechanical "runs", is converted to the post-run HITL boundary.
- **F3 Pre-drainable? YES:** five forks drained on the launch sheet (§ 6). The residual forks are lever *forms* (reasoning-boundaries).
- **F4 Authority-resident? YES** for the rulebook, levers and golden master. ⚠ `SPEC-AUTHOR → DRIFT-CRITIC` at every fold against the conductor's own ARCHITECT pass; jack-ryan Gate-2 at J0, J1, J2 and J5 is the independent check.

## § 4 — Decidable target-state (DONE when every row evaluates, without Matt)

1. **Ablation map filed and GATED:** every INTERNAL/BOUNDARY mechanism of the Warlord classed LOAD-BEARING / INCIDENTAL with its measured deltas; GD's E-2 checklist derived; **jack-ryan Gate-2 PASS on the classification and the checklist** before either is quoted.
2. **Self-join (B0) with a PASS RULE:** `gd-eor-warlord.json` → kit compiler → the arena, compared against REFERENT-v1 on the **`EXECUTES-THE-BOUNDARY-RULEBOOK` set** (J-P2). **B0 PASSES** when the corpus path reproduces the referent on that set, **or** when every divergence carries a disposition in {`closes-in-J2` · `schema-change-owed` (→ J-L4) · `permanent, recorded`}. **A gap list with an undisposed row is a B0 FAIL and a finding, not a deliverable.** ⚑ **Deconfound first:** the APPROX kit JSON is re-graded against the sealed pack before B0 is graded, and **the APPROX ceiling prints on every B0 figure's face.** jack-ryan Gate-2 on the schema-gap list before it is quoted at J-L4 or against TL.
3. **Rulebook v0 + GOLDEN MASTER GREEN,** where the golden master is **a numeric diff against the J-S8 fixture on the J-P2 `EXECUTES-THE-BOUNDARY-RULEBOOK` set** (boundary-determined quantities: per-tick hit/miss and crit tier, applied damage per packet after mitigation, per-wave intake/heal, bodies-in-disc, death tick/wave; the exact grain, tolerance law and negative control are those of J-P2). **The golden master's verdict is over that set;** `ABSENCE-SATISFIED` and `DOES-NOT-TOUCH-THE-JOIN-PATH` rows are reported, **never quoted as the gate.** ⚑ **If J-P2 finds set 1 empty, the charter states that finding and the golden master is the J-S8 fixture diff alone.**
4. **Lever registry v0:** 14 settable levers + 2 build items (L-14, L-15) registered. Every lever is **OPEN at GD's setting, or, where GD is silent, at a DECLARED-INVENTED default carrying its author and reason**; the named instances are **L-03 `max_hp_change_policy`, L-08 `proportional_damage_mitigable`, L-11 `generic_damage_taken_mult`**. **Negative controls for the 8 lever ids whose alternate setting this run implements** (`crit_model` + the D2 set: `tick_quantisation`, `packets_per_tick`, `max_hp_change_policy`, `pth_floor_pct`, `pth_ceiling_pct`, `proportional_damage_offense`, `proportional_damage_mitigable`): flipping it off-default moves **the named metric, in the predicted direction, by a recorded magnitude** (the round-trip back to the golden master is reported beside it, never in place of it). **The other 6 are `REGISTERED-UNEXERCISED` and say so in the registry.**
5. **Kit #2 joined.** **Coverage denominator = J-S2's frozen 14 D2 rows.** Any addition, removal or reclassification after launch, **`OUT-OF-ARENA` especially**, is a named finding carrying its reason, never a silent re-map. **Two fractions print side by side:** (a) rows mapped / 14; (b) **of the D2 BOUNDARY/WIDEN rows, how many have their D2 setting implemented and ACTIVE in the kit's `JOIN` profile** vs left at GD's default. *(Only (b) says whether a kit joined or merely compiled.)* **"Runs" means:** the kit loads from `kits-export`, binds, and executes to a terminal state without exception across the scripted pilot, emitting its arena margin. **Arena margin RECORDED. Home margin: J-S7 pins the tables; the frontier POINT is sourced by commission C-12 in J4; if C-12 returns searched-unlocated, home margin is `DEFERRED` with the re-entry criterion printed on the fidelity-cost table's own face.**
6. **Handoff packet:** build + how-to-run for the Barbarian + the lever registry + the ablation map + the fidelity-cost table + findings. jack-ryan Gate-2 on the whole.
7. **`ORACLE` / `PLAY` INVARIANCE:** the `ORACLE` and `PLAY` configurations emit **byte-identical output before and after every commit on the join path**, checked against the **preserved** sealed oracle and runtime (J-S6) by the J-P2 invariance command. **A change in `ORACLE` behaviour is a HALT to Matt (§ 6), never a lever and never a J2 finding.**

## § 5 — Waves (seams execute; the conductor writes no production code)

| Wave | Seat | Piece | Gate |
|---|---|---|---|
| **pre-launch** | gamora | **J-P2, the golden-master instrument note** (the 29-row classification · the J-S8 fixture spec · tolerance law + negative control · the invariance command) | jack-ryan re-check |
| **J0** | gamora (oracle) · drax (port) | **Ablation map** under `ORACLE` + scripted pilot; print-only, never a T-A artifact | § 4.1 · **jack-ryan Gate-2** |
| J0 | elrond | **Docket-disposition sweep under J-L1's rule** (P0 misfit d; dockets 1, 3, 4, 5, 7, 8 + family rows 9–19), with further hits returned to Matt as ONE batch · GD-SLICE freeze-not-drop + `boundary_class` / `vocab_scope` (**mechanically derived from the key prefix, therefore auditable**) / `mechanism_grade` / `magnitude_grade` (J-L4) | findings + MIGRATION |
| J0 | jack-ryan | **GV:** the 675 `exact_skill` rows graded MEASURED where the era-substrate LAW says DATAMINED (his seam; separate finding) | his finding |
| **J1** | elrond + gamora | **Self-join (B0)**, deconfounded first | § 4.2 · **jack-ryan Gate-2** |
| **J2** | gamora (oracle) → star-lord (pack rows for the rulebook's law + operands) → drax (port) | **Rulebook v0**, FORM/OPERAND split; golden master (§ 4.3); invariance (§ 4.7) | **jack-ryan Gate-2** |
| **J3** | drax + gamora | **Levers v0**: first `crit_model` (three witnesses; GD `pth-tiered` default), then the D2 set (7 more ids) | § 4.4 |
| ⛔ **J3 → J4** | **MATT** | **OWNER-EYE CHECKPOINT** (pattern § 6.2): after `crit_model` lands and before J4 builds the D2 kit on it, because every downstream kit inherits it. A short capture + the lever's metric deltas; red-flag rulings land as class `matt` | Matt |
| **J4** | legolas (D2 formulas + primary rows + **commission C-12: the WW Barb's home frontier point**) → gamora (adapter / conversion key) → star-lord (kit rows) → drax (build) | **D2 WW Barb joined** + arena margin (+ home margin if C-12 sources the point) | § 4.5 |
| **J5** | conductor · jack-ryan | handoff packet · Gate-2 | § 4.6 |

## § 6 — Matt interface (LAUNCH SHEET — one word each; one recommendation each)

| # | Fork | Recommendation |
|---|---|---|
| **J-L1** | **THE RULE, not only the instance:** does Q86 ("add everything natively") supersede **every** pre-union docket disposition that closed a kit-internal mechanism as `permanent-gap-record`? Docket **5** (life-cost casting) is the first application; the census names dockets **1, 3, 4, 7, 8** and family rows **9–19** as the same collision | **YES, as a rule.** Q86 supersedes any pre-union `permanent-gap-record` that closed a **kit-internal** mechanism; docket 5 is re-dispositioned SUPERSEDED-BY-Q86 first; the J0 sweep re-dispositions the rest under the same rule and **returns them to you as one batch, never silently.** Boundary or world-shape dockets (e.g. 2 and 12, allies) are untouched |
| **J-L2** | Does kit #3 (non-physical, KP-85) ride in JOIN-1, or open JOIN-2? | **JOIN-2** (candidate: D2 Fire Sorceress; 294 DATAMINED numeric rows banked; same D2 adapter), **with one clause:** rulebook v0 declares the damage-family registry **`UNEXERCISED-IN-JOIN-1`** on its own face, and `mitigate`'s `KeyError`-on-unmapped-family is **preserved, never defaulted** (GL-12; the oracle's refuse-loudly precedent). L-12 `control_family_registry` is likewise registered-unexercised |
| **J-L3** | "Our balance thresholds" (E-1): tune kit #2 in JOIN-1, or record only? | **Record only.** Arena margin measured (home margin as § 4.5), the fidelity cost filed; **tuning waits until the thresholds are pinned as numbers** (an ELICITOR sitting on doc 50's band) |
| **J-L4** | Cross-seam schema change on `corpus.db`: freeze GD-SLICE `is_core`; add `boundary_class` / `vocab_scope` / `mechanism_grade` / `magnitude_grade` (ADR-002) | **Approve,** additive, nothing dropped (le-park / `source_urls` precedent); `vocab_scope` carried as a DERIVED column, which makes it a check rather than a label |
| **J-L5** | Push posture | **Push-as-work-lands on collaboration + engine + godot** for the run's duration. **Folded into `CLAUDE.md`'s push-pattern section on landing** (its own recording mandate), not only here; loadout/demo untouched |

**HALT-to-Matt boundaries:** **any change in `ORACLE` behaviour (§ 4.7)** · **a C-11 disposition that would alter REFERENT-v1** · a golden-master RED that the conductor cannot attribute to a named defect · jack-ryan BLOCK · committed-truth conflict · free disk < 40 GiB by `df -h` (unit stated, per KP-91; **59 GiB measured at Gate-1**; the KC2 seal lap lost 4 GiB in a single session) · any lever moved off its GD setting (or its declared-invented default) outside kit #2's own profile · a write outside a seat's named tree · two failed attempts at one gate by one seat.
**Conductor continuity:** on conductor session loss or compaction, the successor re-reads this charter and its ledger **before any fold** and records a freshness line (the gandalf OP's charter-freshness gate).

## § 7 — Standing laws carried in

KC2 lineage (K-7 · Law 3 · D4 prereg-alone · digests derived, never retyped, **and labelled FILE vs ROWSET**, KP-101, **applied in § 1 of this document** · corrigenda-forward · § 4.11 value-set sweep) · **the Commission Rule** · `--only` commits with explicit FILE lists · `git status --porcelain` pre / `git show --stat HEAD` post · the heavy lock · captures encoded straight to video · **derive, don't relay** (KP-65, KP-86, KP-95, KP-100: four relay defects in two laps, three of them the conductor's).

## § 8 — Open-questions gate (ARCHITECT)

| Question | State |
|---|---|
| Where the middle sits; union + one rulebook; E-1 target | **RESOLVED** (R-J1, Q86, E-1; KP-82/83) |
| J-L1 … J-L5 | **OPEN — Matt** (launch sheet) |
| **J-P1: REFERENT-v1 sealed** | **GATED:** T-A under prereg v1.6 + Q83(b) + Matt's T-C yes |
| **J-P2: the golden-master instrument note** | **GATED:** gamora (in flight) → jack-ryan re-check |
| **TL** (GD-SLICE template lock) | **GATED:** B1 already said *"not ready to lock"*; the other half of its criterion is **B0 at § 4.2** |
| **GV** (grade-vocabulary unification; 675 rows MEASURED → DATAMINED) | **OPEN — jack-ryan**, opens at J0 |
| **E-2** (per-era signature-feel checklist) | **DERIVED AT § 4.1** for GD; other eras out of scope |
| **C-11** (the oracle's ~×1.9 over-lethality; deaths at 151–156 vs 160) | **GATED+TRACKED:** issued if Matt's T-C says "too deadly", else at J0 as research only; **a disposition that would alter REFERENT-v1 HALTs to Matt** |
| **C-12** (the D2 WW Barb's home frontier point) | **ISSUED AT J4** under the Commission Rule; a negative result DEFERS home margin, printed on the table's face |
| `ABS-C-I14-2-SOURCED-UNFOLDED` (≤ 2.2 %) | **GATED+TRACKED:** folded at the next forward revision of the reference, **which is itself a J-S1 change and so a HALT to Matt inside this run** |
| Lever *settings* for the house profile | **Out of scope** (Phase C) |

## § 9 — Gate-1 discharge (v0.1 `b8c2cb92…` → v0.2), finding by finding

| Finding | Disposition in v0.2 |
|---|---|
| **BLOCK-A** golden master unfalsifiable | § 4.3 rewritten as a **numeric diff against the J-S8 fixture over the `EXECUTES-THE-BOUNDARY-RULEBOOK` set**; the 29-row classification, fixture spec, tolerance law and negative control are **J-P2**, a pre-launch precondition under jack-ryan re-check; the empty-set case is stated |
| **BLOCK-B** ORACLE invariance was prose | **J-S6** preserves the sealed oracle and runtime (tags); **§ 4.7** byte-identical `ORACLE`/`PLAY` across every join-path commit; **§ 6 HALT** on any `ORACLE` behaviour change |
| **BLOCK-C** B0 cannot fail; confounded | **§ 4.2 pass rule** + per-gap disposition set; APPROX deconfounded first and its ceiling printed on every figure; TL row restored in § 8 |
| **BLOCK-D** lever row cannot evaluate | `gd_referent_value ∈ {value \| NONE — no GD rule}`; DECLARED-INVENTED defaults named (L-03, L-08, L-11); negative controls scoped to the 8 implemented ids, 6 REGISTERED-UNEXERCISED; § 2.3 names L-14/L-15 as the build items; L-16 settable |
| **BLOCK-E** coverage gameable | denominator frozen at J-S2's 14 D2 rows; reclassification (OUT-OF-ARENA especially) is a named finding; **second fraction: implemented-and-ACTIVE D2 settings** |
| **BLOCK-F** home margin unsourced | **J-S7** pins the D2 frontier TABLES; the frontier POINT is commission **C-12** at J4; a negative result DEFERS home margin **on the table's face** |
| **BLOCK-G** no gate at J0/J1 | jack-ryan Gate-2 seated at **J0** (ablation classes + E-2) and **J1** (schema-gap list) |
| WARN-1 46 vs 49 | J-S2 reads **46 + 3 = 49** |
| WARN-2 FILE/ROWSET unapplied | § 1 header + J-S1 label the pack digests ROWSET-shaped and derive them at launch |
| WARN-3 TL / GV / E-2 carriers | restored as § 8 rows |
| WARN-4 J-L1 is the instance, not the rule | J-L1 asks for **the rule**; the sweep's hits return to Matt as one batch |
| WARN-5 C-11 a commitment boundary | § 6 HALT + § 8 row |
| WARN-6 "playable" undefined | § 4.5 defines "runs" mechanically; the rest is HITL (§ 0) |
| WARN-7 damage-family registry unexercised | J-L2 clause: `UNEXERCISED-IN-JOIN-1` + `KeyError` preserved; L-12 likewise |
| WARN-8 round-trip ≠ liveness | § 4.4: named metric, predicted direction, recorded magnitude; round-trip reported beside |
| WARN-9 no compaction clause | § 6 conductor-continuity clause |
| WARN-10 no mid-run owner-eye | ⛔ owner-eye checkpoint between J3 and J4 |
| INFO-2 disk headroom | carried on the HALT line (59 GiB at Gate-1) |
| INFO-4 fold J-L5 into CLAUDE.md | J-L5 says so |
| INFO-5 `vocab_scope` derivability | J-L4 + J0 carry it as a DERIVED column |
| INFO-1/3/6/7 | recorded; no edit owed |

---

**Signed:** gandalf (`ARCHITECT`), 2026-09-29. *The replica earned the right to be moved by being proved first; JOIN-1 earns the right to tune by measuring first; and the golden master earns the right to be called a line in the sand only when it can be shown to move.*
