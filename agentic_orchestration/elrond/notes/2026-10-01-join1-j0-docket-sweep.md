# JOIN-1 J0: the docket-disposition sweep under J-L1, and the GD-SLICE field derivation

> **STATUS:** CURRENT. J0 deliverable, seat elrond, Run JOIN-1 (charter `gandalf/notes/2026-09-29-join-1-run-charter.md` v0.5, § 5 J0 elrond row; gate: "findings + MIGRATION").
> **Date:** 2026-10-01 · **Author:** elrond · **Conductor:** gandalf.
> **The rule being applied (J-L1, Matt, 2026-09-29, KC2-PLAY KP-110, "YES as a rule"):** *Q86 supersedes any pre-union `permanent-gap-record` that closed a **kit-internal** mechanism. Docket 5 is re-dispositioned SUPERSEDED-BY-Q86 first. The sweep re-dispositions the rest under the same rule and returns them to Matt as ONE batch, never silently. Boundary or world-shape dockets (e.g. 2 and 12) are untouched.*
> **Companion:** the census `elrond/notes/2026-10-01-join1-j0-sorceress-census.md`. MIGRATION entry `join1-j0-2026-10-01` in `research/curated/MIGRATION.md`.
> ⚑ **Write state (amended forward): APPLIED 2026-10-01T05:04Z** on gandalf's word (KP-162), once disk was back above 40 GiB. `corpus.db` FILE sha256 → `dffad643547a73068e2b8e39ddb6c7cb26dfef0fdea5453efdb96e2c18b8d473`; every post-apply assert PASS (see the `MIGRATION.md` entry). The staging line follows, kept as written.
> **Write state (as staged): STAGED, NOT APPLIED.** Free disk measured **39.72 GiB, then 36.30 GiB** (`df -k`, GiB = 2³⁰ bytes), below the charter § 6 HALT line of 40 GiB. The `corpus.db` writes are fully scripted and **dry-run PASS in memory, with zero bytes written**. Applying them takes one command once the conductor clears the HALT (§ 5).

---

## 1 · Method

**Two tests per docket.**
- **T1:** is the disposition a pre-union `permanent-gap-record`?
- **T2:** is the mechanism kit-internal? This uses the P0 method: the kit decides it, even when the boundary reads its output.

T1 and T2 together make a hit. The sweep screened **every row of `mechanic_gap_docket` (63)**, not only the 17 the charter names (1, 3, 4, 5, 7, 8 and 9–19), so that "no further hits" is a measured statement. Only four rows carry `permanent-gap-record` (2, 3, 5, 12). Three are inside the named list; docket 2 is outside it, but J-L1 itself names it untouched. The other 44 rows (`docket_id` 90–176) are `open` or carry non-closing dispositions, so the rule has nothing to supersede there.

**"P0 misfit (d)".** The P0 census does not letter its misfits. Read in order, § 7.1–7.5 = (a)–(e), so **(d) = § 7.4, world-shape** (Battle Orders projecting to allies, dockets 2/12). Under J-L1 it is **untouched**, as the rule says. If "(d)" meant § 7.5 (the docket-5 collision), that collision is **discharged** by J-L1's own instance ruling. Both readings land in the same place.

**Corrigendum to my P0 note (§ 7.5).** It listed docket 3 among "1, 3, 4, 7, 8 (all `engine-design-intake`)". **Docket 3 is `permanent-gap-record`.** That is why it is the one further hit below.

## 2 · Results, docket by docket

| Docket | Mechanism (short) | Prior disposition | T1 | T2 | Verdict |
|---|---|---|---|---|---|
| **5** | self-damage cast cost redirected to a proxy life pool | permanent-gap-record | ✓ | kit-internal | **SUPERSEDED-BY-Q86** (Matt-ruled instance). **Staged write:** disposition → `superseded-by-q86`, prior value kept in `provenance_json.q86_supersession` |
| **3** | RNG-element-pool identity (per-hit random element from a fixed pool) | permanent-gap-record | ✓ | kit-internal (the kit picks the element; the boundary only reads the family tag, as for any packet) | **PROPOSED SUPERSEDED-BY-Q86 → Matt batch M-1** |
| 2 | ally-buff projection (party scope, solo engine) | permanent-gap-record | ✓ | world shape | **Untouched** (named by J-L1). ⚑ Its *secondary* clause (reservation ~100% vs the LOCKED 0.75 cap) → **M-3** |
| 12 | [§5.2] support-party-scope | permanent-gap-record | ✓ | world shape | **Untouched** (named by J-L1); P0 § 7.4 consistent |
| 15 | [§5.2] roguelite-idiom (hades1) | **permanent-genre-law-record** ("no engine action") | ✗ (literal) / closing in effect | split | **SCOPE QUESTION → M-2** |
| 6 *(not named)* | closed-loop self-damage trigger economy | **working-as-intended** (vs `MAX_CHAIN_DEPTH=1` LOCKED) | ✗ | ambiguous | **SCOPE QUESTION → M-3** |
| 13 | [§5.2] loot-economy-identity | permanent-out-of-scope | ✗ | out of arena | Untouched; agrees with P0 § 7.2 |
| 4 | stun magnitude as damage + perma-stunlock | engine-design-intake (declare half) · working-as-intended (collision half) | ✗ | mixed; the anti-stunlock floor is **CC on monsters = BOUNDARY** | Untouched. When a stun kit joins, the floor is a monster-CC lever question (P0 § 7.1), not a docket re-disposition |
| 1, 7, 8 | entity-as-pool · world-entity capture · stat-as-army | engine-design-intake | ✗ | mixed · mixed · kit-internal | Untouched (open, not closed). ⚑ *Consequence (info, no write):* Q86 forecloses the "declare permanently approximated" branch of each D-4.2 mint-or-declare fork for the **kit-internal** sub-shapes, from the moment a member kit joins |
| 9, 10, 11 | [§5.2] summoner-deferral · stat-as-damage-substrate · spatial resource node | engine-design-intake | ✗ | kit-internal / mixed | Untouched; Q86-consistent |
| 14, 19 | [§5.2] mode-swap-identity · held-singletons | hold | ✗ | kit-internal / mixed | Untouched (a hold is not a closure). Docket 19's member "utility-transport teleport-sorc" is the Teleport row J-S3b excludes |
| 16, 17, 18 | [§5.2] standing families | standing-family-record | ✗ | kit-internal | Untouched: a record that names an evidenced family does not close it |

**Tally over the charter's named list (17 rows) plus dockets 2 and 6 (19 rows):**

| Outcome | Dockets |
|---|---|
| Superseded, ruled | 5 |
| Proposed superseded | 3 |
| Scope questions | 15, 6 |
| Untouched, world shape | 2, 12 |
| Untouched, out of arena | 13 |
| Untouched, not closed | 1, 4, 7, 8, 9, 10, 11, 14, 16, 17, 18, 19 |

Screened outside the named list and not a pre-union closure: 44 rows (63 − 19).

## 3 · ⚑ THE ONE BATCH FOR MATT (J-L1: "returned to you as one batch, never silently")

**None of these touches JOIN-1's three kits, the REFERENT-v1 pack or the ORACLE.** Every member kit is PoE1, hades1 or LA, so each answer is **record-only in JOIN-1**: no build is owed. They are asked now because the lever registry is seeded after the sweep (charter § 4.4, RC-I5) and would otherwise inherit whichever answer is read first.

| # | Question | Steward's lean |
|---|---|---|
| **M-1** | **Docket 3 (RNG-element-pool identity: per-hit / per-entity random element from a fixed pool; PoE1 elemental-hit, skeleton-mages, wild-strike), `permanent-gap-record` → SUPERSEDED-BY-Q86?** | **YES.** It has the same shape as docket 5: a pre-union gap record over a mechanism the kit decides. Two conditions travel with it. The docket's own prunable = build / unprunable = trap distinction survives. Each emitted family must map in the damage-family registry when a member kit joins (`KeyError` preserved) |
| **M-2** | **Does J-L1 reach `permanent-genre-law-record` (docket 15, hades1 roguelite idioms, "no engine action")?** It closes kit-internal mechanisms in effect, but it is not literally a `permanent-gap-record` | **YES for its kit-internal members** (self-cost contract, finite-ammo burst, duo-boon pair). **Untouched for its boundary members** (delayed-detonation Doom and per-arrow status are status on monsters; deflect is hit resolution) |
| **M-3** | **Does Q86 reach LOCKED engine guards dispositioned `working-as-intended` or clamped in-map?** Two instances: **docket 6** (`MAX_CHAIN_DEPTH=1` vs a closed-loop trigger economy) and **docket 2's secondary clause** (a reserving kit clamped to the LOCKED `reservation_percent` 0.75) | **Split them.** *Reservation* is kit-internal by Q86's own list ("…energy shield, **reservation**…"), so the 0.75 clamp does not bind a joined kit's reservation (lean YES). *Trigger-chain depth* is applied to every kit alike, which makes it a shared, boundary-shaped rule: **not superseded; register it as a lever candidate when a member kit joins** (lean NO) |

## 4 · GD-SLICE: freeze, don't drop, and the four columns (J-L4)

`exact_skill_field` (7,250 rows, 285 keys) gains `vocab_scope`, `boundary_class` (plus `boundary_class_rule`, the rule that fired), `mechanism_grade` and `magnitude_grade`. **Nothing is dropped and no existing value is rewritten.** `is_core` is **frozen by a trigger** (`BEFORE UPDATE OF is_core` → ABORT, tested in memory). The precedent is `le-park` and the frozen `source_urls`.

### 4.1 · The derivation rules: mechanical, therefore auditable

**`vocab_scope`, one rule:** `game_named` iff `canon_key` begins with `<g>_` for some `g` in the corpus's own game codes (`SELECT DISTINCT game FROM canon_corpus`: 21 codes); otherwise `neutral`. Nothing is hand-listed, and there are 0 prefix collisions among the 285 keys.
- **Independent cross-check:** the result agrees with `canon_key_provenance` on **every row**. `game_named` = `mechanical` (251 keys / 4,883 rows) and `neutral` = `curated` (34 keys / 2,367 rows).
- **The P0 drift, now a query rather than a claim:** within `is_core = 1` at the devotion version, 169 keys / 3,232 rows are `game_named`.

**`boundary_class`:** the **first** rule (by `rule_order`) whose GLOB matches `canon_key`, taken from the committed rule table `research/curated/gd-slice-boundary-class-rules-2026-10-01.csv`. The table has 34 rules over 84 patterns, FILE sha256 `882ef1244991291f0f0770a00685cbf29133dddd7ff06512216496327aea8ef4`, and is loaded verbatim into `corpus.db` as `boundary_class_rule`.
- The values are {`internal`, `boundary`, `out_of_arena`, **`unresolved`**}. `unresolved` is the honest fourth value, by the census § 7.1 law: a sort that cannot say "the key does not decide" launders silence into a class.
- An unmatched key falls through to `R99-fallback` → `unresolved`. It is never silently classed.
- An `AFTER INSERT` trigger derives both columns for new rows.
- The view **`v_exact_skill_field_class_audit`** returns every row whose stored values disagree with a fresh derivation. **Dry-run: 0 rows.**

The rule spine, in P0's terms:

| Class | Key families (rules) | Rows (keys) |
|---|---|---|
| **boundary** | `gd_defensive_*` (resist, armour, block, CC resist, leech resist) · `gd_damage_absorption*` · OA/DA · dodge/deflect/block-recovery · attack/cast/total speed · run speed · `cast_cadence_ms` · `gd_instant_cast` · monster CC (`gd_offensive_{stun,freeze,petrify,knockdown,confusion,fumble,projectile_fumble,taunt,slow_run_speed,slow_attack_speed,slow_total_speed}*`, `ailment_*`) · monster debuffs (`*resistance_reduction*`, `physical_reduction*`, `total_damage_reduction*`, `slow_{defensive,offensive}_ability*`, `gd_debuf_skill`) · crit damage · retaliation fear/petrify · DoT dispel · racial defense · targeting/geometry (projectile, wave, drop, cone, range, target, contagion, spark, expansion time) · `gd_*_damage_qualifier` | **2,483 (153)** |
| **internal** | `damage_*` · `weapon_damage_pct` · the remaining `gd_offensive_*` (flat damage, +%, DoT magnitudes and durations, damage mult, mana drain) · `leech_*` · the remaining `gd_retaliation_*` · conversion · racial damage · the remaining `gd_skill_*` (cost, sustain, cooldown reduction) · `cost_*` · `cooldown_*` · refresh time · burn duration · the remaining `gd_character_*` (attributes, pools, regen) · pets/spawns | **4,474 (111)** |
| **out_of_arena** | equipment requirement reductions · weapon-type restriction flags | **108 (20)** |
| **unresolved** | `effect_duration_sec` (`skillActiveDuration` covers self-buffs AND monster debuffs; the key cannot tell them apart) | **185 (1)** |

**Rules carrying a FLAG for Gate-2:**

| Rule | Keys | Question |
|---|---|---|
| R14 | `gd_character_total_speed_modifier` | Two boundary items in one key (the class is unambiguous) |
| R17 | `gd_instant_cast` | Tick clock, or a skill property? |
| R22 | `gd_offensive_crit_damage_modifier` | Boundary because GD welds crit to the hit roll (P0 finding 3) |
| R25 | `gd_racial_bonus_percent_defense` | Classed as an intake multiplier (the L-11 shape) |
| R26 | `gd_expansion_time` | Family label says "cadence"; classed B6 |
| R42 | `gd_offensive_slow_mana_leach_*` | Classed as leech |
| R50 | `gd_refresh_time` | Classed by the cooldown precedent |
| R60 | `effect_duration_sec` | Unresolved (see above) |

**What the derivation shows about `is_core`:** `is_core` does not track the Q86 sort at all.

| `boundary_class` | `is_core = 1` | `is_core = 0` |
|---|---|---|
| boundary | 1,811 rows | 672 rows |
| internal | 3,574 rows | 900 rows |

The flag was measuring something else before the union ruling. This is P0 § 8.2 restated as a query.

### 4.2 · `mechanism_grade` / `magnitude_grade`

**Rule:** both **inherit the header's `exact_skill.fidelity_grade`.** Every `exact_skill_field` row is a decoded value of its header's `.arz` record, so mechanism and magnitude share one source, and on this table P0 § 7.3's split is structurally degenerate. The split earns its keep at the kit and census layer, as in the Sorceress census.
- **Precondition:** jack-ryan's GV remedy has landed. The migration **aborts** if any header still reads `MEASURED`, rather than copy the defect into two new columns.
- **Dry-run** (with GV applied in memory first): **7,250 / 7,250 `DATAMINED` / `DATAMINED`.**

## 5 · Apply sequence (staged; one command each, in this order, once the disk HALT clears)

```
cd ~/Games/reincarnated-collaboration/agentic_orchestration/research/scripts
python3 join1_j0_gv_relabel_2026_10_01.py      --mode apply   # GV first (precondition)
python3 join1_j0_corpus_migration_2026_10_01.py --mode apply   # then M1 GD-SLICE + M2 docket sweep
```

Both scripts **refuse to apply below 40 GiB free** and write a file backup first. Both re-run their audits after the write and print PASS or FAIL.

**Signed:** elrond, 2026-10-01.
