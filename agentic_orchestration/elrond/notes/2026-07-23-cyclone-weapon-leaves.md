# Cyclone Weapon Leaves — KFL-13(d) elrond micro-lane — 2026-07-23

**Run:** KIT-FIDELITY (conductor: gandalf `RUN-CONDUCTOR`). **Ledger anchor:** KFL-13.
**Purpose:** store the conductor-verified-ANCHORED 3.15 Cyclone Slayer build-point WEAPON as verbatim
corpus leaves, so gamora's queued weapon-composition rule step can flip the one RED KF-4 acceptance
assert (`poe1-cyclone` `has_damage_base`) → GREEN. Leaves ONLY — no derivation (that is gamora's step).

**Source note (conductor-verified ANCHORED, commit `8abfeed5`):**
`agentic_orchestration/legolas/notes/2026-07-23-cyclone-weapon-dps-anchor.md`
**Migrations committed:**
- `research/scripts/catalogue_migrations/corpus_poe1_cyclone_weapon_leaves.sql` (12 kit_numeric leaves)
- `research/scripts/catalogue_migrations/corpus_poe1_cyclone_weapon_citations.sql` (3 citations + Berserker quarantine)

---

## Task 1 — 12 weapon leaf rows added to `kit_numeric` (kit_id=`poe1-cyclone`)

Dual-column law held: `source_value` = verbatim number, `source_anchor` = verbatim quote it came from,
`rdr_value` = NULL, `rule_id` = NULL (gamora's normalization-rule step derives + assigns). Build-point rows
carry the compiler's `_bp` selector suffix; damage-shaping weapon scales carry the `_v315` build-point marker
(matching `effectiveness_pct_gem20_bp`'s `poe1_effectiveness_pct_v315`) so the future weapon-composition rule
selects them as the 3.15 build point and never confuses them with the `_v327_context` fence.

| # | numeric_key | source_value | source_scale | anchor quote (source) |
|---|---|---|---|---|
| 1 | `weapon_identity_ilvl` | 83 | `poe1_level` | "Blood Razor" rare Exquisite Blade, iLvl 83, Q44, Weapon 1 — PoB `Sf8AYHkK` XML 1618-1634 / slot 1840 [WEAPON IDENTITY / gear-stage] |
| 2 | `weapon_base_phys_min_bp` | 67 | `poe1_weapon_base_phys_v315` | "Physical Damage 67-112" (min) — poedb.tw/us/Exquisite_Blade |
| 3 | `weapon_base_phys_max_bp` | 112 | `poe1_weapon_base_phys_v315` | "Physical Damage 67-112" (max) — poedb.tw/us/Exquisite_Blade |
| 4 | `weapon_base_aps_bp` | 1.35 | `poe1_weapon_aps_v315` | "Attacks per Second 1.35" — poedb.tw/us/Exquisite_Blade |
| 5 | `weapon_base_crit_chance_pct_bp` | 5.7 | `poe1_pct` | "Critical Strike Chance 5.7%" — poedb.tw/us/Exquisite_Blade |
| 6 | `weapon_mod_inc_phys_pct_bp` | 156 | `poe1_pct` | "156% increased Physical Damage" — PoB `Sf8AYHkK` XML line 1629 |
| 7 | `weapon_mod_flat_phys_min_bp` | 23 | `poe1_weapon_flat_phys_v315` | "Adds 23 to 49 Physical Damage" (min) — PoB XML line 1630 |
| 8 | `weapon_mod_flat_phys_max_bp` | 49 | `poe1_weapon_flat_phys_v315` | "Adds 23 to 49 Physical Damage" (max) — PoB XML line 1630 |
| 9 | `weapon_mod_inc_attack_speed_pct_bp` | 21 | `poe1_pct` | "21% increased Attack Speed" — PoB XML line 1631 |
| 10 | `weapon_quality_pct_bp` | 44 | `poe1_pct` | "Quality: 44" (incl. {crafted}+14% to Quality) — PoB XML lines 1624 + 1633 |
| 11 | `weapon_implicit_global_crit_multi_pct_bp` | 50 | `poe1_pct` | "+50% to Global Critical Strike Multiplier" (implicit) — PoB XML line 1628 |
| 12 | `weapon_crafted_inc_crit_chance_pct_bp` | 25 | `poe1_pct` | "{crafted}25% increased Critical Strike Chance" — PoB XML line 1632 |

Covers the full required damage-composition surface: base phys min/max, base APS, base crit%, increased
phys%, flat added phys min/max, increased attack-speed%, quality%, implicit global crit-multi%, crafted
increased crit-chance%. Weapon identity/gear-stage recorded (row 1 + carried in every anchor as "Blood Razor").

**Conductor KFL-13(b) defects — recorded, cannot leak here.** The note's DERIVED ~570 pDPS is arithmetically
wrong twice: (i) invents "+0.5% inc phys per 1% quality for two-handers" (the PoE local-weapon quality rule is
1:1, Q44 → +44%); (ii) the per-hit sketch (570×0.59/3.0) conflates attack cadence with per-hit magnitude.
NEITHER touches these rows — every leaf is a pure verbatim number; the COMPOSITION that would have consumed
that arithmetic is gamora's normalization rule, to be pinned against a citable source (PoB CalcOffence),
jack-ryan-checked. Flagged in both migration headers so the note's arithmetic cannot enter the rule.

## Task 2 — 3 citation rows added to `kit_citations` + Berserker disposition

New rows (accessed_date 2026-07-23, rank_class `recovered`):

| id | url | site | cite_class | q |
|---|---|---|---|---|
| 1294 | pathofexile.com/forum/view-thread/3033867 | pathofexile.com/forum | communal | 0 |
| 1295 | pastebin.com/Sf8AYHkK (PoB export, primary weapon anchor) | pastebin.com | dataset | 0 |
| 1296 | poedb.tw/us/Exquisite_Blade (base item) | poedb.tw | dataset | 0 |

**Berserker-thread disposition — QUARANTINE (`quarantined=1`), NOT deleted.** Rationale: existing citation
id 64 = `pathofexile.com/forum/view-thread/3078559` is a 3.15 Cyclone **Berserker** build; this kit is
Slayer-documented (KFL-2/KFL-5) and legolas decoded that thread's PoB (`iXrZh2pY`) and rejected it as the wrong
ascendancy. I quarantine rather than delete because provenance is never silently destroyed — the schema's
`quarantined` flag exists exactly for "recorded, never citable"; the row stays queryable as the documented
reason the wrong build was ruled out. The Slayer thread 3033867 (id 1294) is now the primary build citation.
**Load-bearing note:** this does NOT weaken the two `59% effectiveness` build-point leaves whose `source_anchor`
still cites thread 3078559 — Cyclone's gem effectiveness (59% at gem 20, 3.15) is a property of the SKILL GEM,
ascendancy-independent (Slayer and Berserker share the identical gem); the effectiveness quote is true
regardless of build. The quarantine narrows the citation's ROLE (not a build endorsement); it changes no leaf.

## Discipline proofs

- **Idempotency:** first apply → cyclone `kit_numeric` 20→32 (+12), `kit_citations` 3→6 (+3), quarantined 0→1.
  Re-apply both `.sql` → **32 / 6 / 1 stable** (no drift). Migrations use `INSERT OR IGNORE` + a
  quarantined=0-guarded `UPDATE` → safe re-run by construction.
- **Immutability:** SHA of all 20 pre-existing rows' `numeric_key=source_value` = `bb22132a59691e7662757288fd7a4463d360ba91`
  BEFORE apply and BYTE-IDENTICAL AFTER two applies. `weapon_dps_target=650` (R-CTX-GEO overgear floor)
  untouched. Zero existing `source_value` mutated. Only NEW rows + the one Berserker citation flag changed.
- **Dual-column law:** my 12 new rows = 12 with `rdr_value` NULL AND 12 with `rule_id` NULL (isolated query).
- **Byte-rebuildability:** applied both migrations to a fresh copy of corpus.db → cyclone state matched live
  exactly (32/6/1). DB stays rebuildable from the committed `.sql` files.
- **RED-flip surface present:** the kit now carries 2 `poe1_weapon_base_phys_v315` rows (67/112) — the weapon
  damage base the `has_damage_base` assert needs. gamora's queued rule step derives + re-asserts RED→GREEN.

## Deviation logged (not silent)

The sibling file `corpus_kf23_kit_poe1_cyclone.sql` uses `INSERT OR REPLACE`; this micro-lane uses
`INSERT OR IGNORE` instead — because the mandate is to NEVER overwrite an existing row (immutability made
STRUCTURAL: a re-run against a populated DB is a no-op on every prior row, incl. `weapon_dps_target=650`).
Strictly more preserving; all new keys are collision-free (`weapon_*` namespace verified absent), so nothing
is skipped on first apply. Documented in both migration headers.

## Handoff to gamora (queued behind KF-5)

The weapon-composition normalization rule consumes the `_bp` + `_v315` weapon leaves above to derive per-hit
physical `rdr_value`, pinned to a citable composition source (PoB CalcOffence path), and must NOT import the
note's ~570/112 arithmetic (defects above). On derivation, stamp `rule_id` + `rule_version_applied` on these
12 rows and re-run the `has_damage_base` assert. Existing `weapon_dps_target=650` remains context-fenced under
R-CTX-GEO (aspirational floor, never the build point).
