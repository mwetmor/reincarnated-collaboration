# Re-key prep — ECON slot (design session #5) + mechanics-gap census

**Date:** 2026-07-12 · gandalf (mechanical prep; **elicits, does not rule**) · Spec: `corpus-rekey-spec-v1.md` §2 — econ (15 codes) RETIRES → raw descriptor; engine targets = `_ENERGY_CONFIGS` · doc-48 assigner · Axis-5 cost-TYPE bins · T4 doors. **Unmappable residue = the mechanics-gap census → feeds pause-2 / V3.**

## 1. Corpus code frequency (v3 CSV canon positives, n=478)

| code | meaning | count | % | | code | meaning | count | % |
|---|---|---|---|---|---|---|---|---|
| SP | spend | 267 | 56% | | RS | reserve | 13 | 3% |
| CD | cooldown | 40 | 8% | | SW | stat-weapon | 9 | 2% |
| MT | meter | 39 | 8% | | DW | dot-walk | 6 | 1% |
| SU | summon | 32 | 7% | | LC | leech | 6 | 1% |
| AM | ammo | 26 | 5% | | DR | draft | 5 | 1% |
| PC | proc | 19 | 4% | | HV | harvest | 2 | 0% |
| RC | recipe | 13 | 3% | | SC | self-cost | 1 | 0% |

**14 live codes** (decoded via `ECON_CODE`/`econ_bucket`).

## 2. Engine vocabulary of record

- **`_ENERGY_CONFIGS`** (`combatant.py:430`): `rage(100,empty,0)` · `combo(5,empty,0)` · `focus(100,full,-5)` · `stamina-as-resource(150,full,+20)` · `charge-stack(10,empty,0)` + **mana-default** branch.
- **Resource models** (substrate registry §1.11): `cooldown · energy · mana · stamina · ki`.
- **Axis-5 cost-TYPE bins** (F5): `resource_target {pool, hp}` × `builder_source {on_cast, on_hit, on_damage_taken}`.
- **T4 doors** (`t4_category_schema.py`, 8 strategies): **`RESOURCE_CONVERSION`** (HP-for-power) + `TRADE_OFF` are the econ-relevant ones.

## 3. PROPOSED mapping (corpus → engine) + residue

| corpus | → engine | confidence | note |
|---|---|---|---|
| SP spend | mana/energy pool · `resource_target=pool` · `builder=on_cast` | HIGH | the default economy |
| CD cooldown | resource-model `cooldown` | HIGH | 1:1 |
| SC self-cost | `resource_target=hp` → T4 `RESOURCE_CONVERSION` | HIGH | **native** (K26/K29) |
| MT meter | `rage`/`combo`/`focus`/`charge-stack`; `builder=on_hit` | MED | 1:many family |
| SW stat-weapon | Axis-5 `on_damage_taken` builder (thorns) | MED | K27 (`MT`→`SW` per V4-r2 F6) |
| DW dot-walk | element-application dot-stacking | PARTIAL | rider, not a pool |
| LC leech | leech/life-feed → `RESOURCE_CONVERSION`-adjacent | PARTIAL | sustain economy |
| RS reserve | reservation/aura toggle (GX-05) | PARTIAL | engine has no first-class reserve pool |
| SU summon | *(no engine econ)* | **GAP** | GX-19 |
| AM ammo | *(no engine econ)* | **GAP** | GX-14 |
| PC proc | *(no first-class proc econ)* | **GAP** | partial via on_hit |
| RC recipe | *(no engine econ)* | **GAP** | GX union/pair-grain |
| DR draft | *(no engine econ)* | **GAP** | roguelite offer-pool |
| HV harvest | *(no engine econ)* | **GAP** | pickup/magnet |

## 4. Mechanics-gap census (unmappable econ → candidate engine mechanics; feeds pause-2 / V3)

Ordered by corpus weight — these are the econ codes with **no engine mechanism**, i.e. candidate mechanics-adds:

| gap econ | kits | GX ref | candidate mechanic | genre precedent |
|---|---|---|---|---|
| **SU summon** | **32** | GX-19 | summon-uptime / troop economy | universal (D2 skele, PoE spectre, GD pet) — pairs with unoccupied summoner basins IRMFHI/IMMFHI |
| **AM ammo** | 26 | GX-14 | finite-ammo / consumable / reload | PoE flasks, GD ammo, D-quiver — 10 games |
| **PC proc** | 19 | — | proc/cascade/trigger economy | PoE CoC/trigger-wands, D3 procs |
| **RC recipe** | 13 | union | union/evolution/relic-gated authoring | VS evolutions, HoT, Undecember runes |
| **RS reserve** | 13 | GX-05 | reservation / aura / seal toggle | PoE auras (partial engine coverage) |
| **DR draft** | 5 | — | roguelite draft / banish / reroll offer-pool | Hades, VS, roguelite layer |
| **HV harvest** | 2 | — | pickup / magnet / greed economy | VS/HoT survivor loot-magnet |

**SU (summon) is the largest gap and the highest-leverage** — 32 kits, GX-19, and it directly gates the two biggest unoccupied genre basins (summoner IRMFHI + minion IMMFHI, census §2). A summon-economy add is the single most coverage-unlocking mechanic in the corpus.

## 5. Open forks (UNRESOLVED — Matt rules)

- **Fork E1 — "all mechanics if I can": which gaps clear the bar?** The census hands Matt a ranked mechanics-add menu. SU (summoner economy) is the clear #1 by coverage-unlock. AM (ammo) and RC (recipe/union) are structurally large but genre-tier-split (AM = ARPG-core; RC/DR/HV = roguelite/survivor tier T3). **Genre precedent:** adding summon-economy is a well-trodden ARPG spine (every T1 game has it); adding draft/harvest pulls toward the survivor sub-genre (VS/HoT). **Lean:** SU first (ARPG-core, huge unlock); RC/DR/HV are a *survivor-tier bundle* decision, separable. This is the pause-2 surface — Matt rules per gap.
- **Fork E2 — meter (MT) family split.** Corpus `meter` collapses rage/combo/focus/charge-stack. Re-key needs to assign each MT kit to one `_ENERGY_CONFIGS` type — a per-kit disambiguation (39 kits). **Lean:** doc-48 assigner already does this at generation; re-key MT→`meter-family` descriptor and let the assigner resolve. Verify on a sample.
