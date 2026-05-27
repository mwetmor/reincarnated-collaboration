# Wave 1.5 Stage 1 — Class-Roster Substrate-Evidence Audit (Cycle 14)

> **STATUS:** CURRENT — audit deliverable for Wave 1.5 Stage 2 (gandalf class-roster design call). EVIDENCE only; does NOT select the final roster or lock per-class chain counts. Per dispatch Out-of-scope clauses, all design selection is gandalf Stage 2 territory.

**Authored:** 2026-05-27 (Cycle 14 Wave 1.5 Stage 1)
**Author:** elrond (data steward — catalogue DB + abstraction-analysis seam)
**Authority:** Matt 2026-05-27 ratified Option C (substrate-evidence audit → gandalf design call) per `agentic_orchestration/gandalf/notes/2026-05-27-scaffold-drift-recognition-and-corrective-package.md` § 3.5
**Dispatch:** `agentic_orchestration/dispatches/2026-05-27-elrond-cycle-14-wave-1-5-stage-1-class-roster-substrate-audit.md`
**Companion docs:**
- `agentic_orchestration/elrond/notes/2026-05-27-cycle-14-sc-6-substrate-weapon-audit.md` (SC-6 substrate composition; 2,293 v1_scope rows; 5-family weapon_type_family taxonomy; primary_stat distribution)
- `agentic_orchestration/elrond/notes/2026-05-27-cycle-14-sc-6b-substrate-enrichment-implementation.md` (SC-6b enrichment values; per-family L50 baselines)
- `canonical/40-gear-balance-guide-architecture-2026-05-26.md` § 8.3 (variable 3-or-4 chains; T4 = chains − 1) + § 6.6.1 (supporting chain Option C; class-intrinsic)
- `canonical/46-concentration-architecture-2026-05-27.md` (Wave 1 architectural foundation)
- `.claude/skills/reincarnated-substrate-vector-cheatsheet` (BC axes)

---

## 0. TL;DR

- **Substrate evidence pool: 969 named_template + unique + 1,139 category rows = 2,108 archetype-anchoring rows** (after hygiene filter excluding ammo/shield-as-main/banner/horn/talisman from PRIMARY weapon role — but these reappear as SUPPORT-archetype evidence in § 2.5)
- **34 candidate archetype seeds surfaced** (per Q-W15-S1-1 elrond call: tighter side of dispatch's 30-50 range — substrate evidence has natural clustering ~30, padding to 50 would manufacture archetypes without substrate vote)
- **Three structural findings load-bearing for Stage 2:**
  1. **Form-vocabulary signal is rich; mythological-character signal is sparse.** Only 34/969 named+unique have `named_mythological_match` populated. Archetype-vocabulary is FORM-derived (greatsword, dagger, staff, mace, bow, gun), NOT character-mythos derived (Beowulf, Gilgamesh, Arthur appear but at low density). **Per Q-W15-S1-3: lineage-balanced filtering not feasible against this substrate** (95% of named+unique tag `fantasy_generic`/`fantasy`); lineage signal lives in CATEGORY rows instead (823 european, 119 east_asian — viable for lineage-conscious gandalf curation at Stage 2 if desired)
  2. **STR-martial-heavy substrate is 2.7× over-saturated relative to other primary_stat × weapon_type_family cells** (363 named+unique rows vs ~125 average in other cells). Multiple internal archetype distinctions warranted (greatsword vs hammer vs polearm vs lance vs unarmed). DEX-ranged has internal multi-archetype (precision-shooter 100 guns + 88 rifles vs scatter 45 shotguns vs javelin 53 thrown). INT and WIS are smaller pools (125 + 99) with more limited internal differentiation.
  3. **BC-axis cell coverage from substrate's proxy classifications:** STR-heavy substrate votes `single` (346) + `cleave` (314) + `AoE` (78) — three damage-geometry surfaces. DEX votes `single` (773) + `cleave` (136) + `multi-hit` (50) + `scatter` (45) + `AoE` (33). INT votes `single` (149) + `AoE` (6) — virtually no AoE-caster substrate. WIS votes `single` (103) + `AoE` (42) — strong AoE-faith-support substrate. **INT-AoE cell is empirically empty; gandalf Stage 2 must either commission substrate enrichment OR design INT classes around `single` damage-geometry exclusively.**
- **Per Q-W15-S1-2 (BC-cell prioritization):** elrond votes COMPREHENSIVE coverage with explicit notation of cells where Cycle 13 cohort FAILED — comprehensiveness gives gandalf the wider surface to curate from. Cycle 13 cohort-failure pattern noted in § 3.4 below.
- **Per Q-W15-S1-4 (named_template vs category prioritization):** elrond votes BOTH — named_template primary (form-vocabulary identity); category supporting (lineage signal + form-coverage validation). Architecture: each candidate archetype seed cites primary substrate-evidence rows (named) + supporting evidence rows (category) where applicable.

---

## 1. Substrate evidence overview

### 1.1 v1_scope row distribution (per SC-6 audit § 1.2 baseline)

| Population | n | % of v1_scope |
|---|---|---|
| Total v1_scope rows | 2,293 | 100% |
| named_template | 927 | 40.4% |
| category | 1,139 | 49.7% |
| unique | 42 | 1.8% |
| ammo_or_consumable | 148 | 6.5% |
| shield | 17 | 0.7% |
| talisman | 11 | 0.5% |
| banner | 7 | 0.3% |
| horn | 1 | 0.04% |
| unknown | 1 | 0.04% |

**Archetype-anchoring rows (primary weapon role):** named_template + unique + category = 2,108. Per substrate-sidecar Fix A hygiene filter, this is the curation-clean pool.

**Support-archetype-anchoring rows (off-hand / aura / consumable):** ammo + shield + talisman + banner + horn = 184. These are NOT main-weapon candidates but DO carry support-archetype evidence (shield-blocker, banner-rally-aura, talisman-AoE) — see § 2.5.

### 1.2 primary_stat × weapon_type_family distribution (named+unique only, the form-vocabulary signal)

Per dispatch Scope Item 1; cluster-key for archetype seeding:

| primary_stat | weapon_type_family | n (named+unique) | % of named+unique |
|---|---|---|---|
| STR | martial-heavy | 363 | 37.5% |
| DEX | martial-light | 195 | 20.1% |
| DEX | ranged | 151 | 15.6% |
| INT | caster-arcane | 125 | 12.9% |
| WIS | caster-faith | 99 | 10.2% |
| STR | ranged | 36 | 3.7% |

**Total named+unique anchoring archetype identity:** 969 rows.

**Empirical observation:** STR-martial-heavy is 2.7× over-saturated relative to other cells (363 vs ~125 average). Multiple internal archetype distinctions warranted within STR-heavy. INT-caster and WIS-caster cells are tightest (125 + 99); fewer internal archetype distinctions empirically supported.

### 1.3 Lineage / register signal (audit Q-W15-S1-3 grounding)

**named+unique rows (969):**

| cultural_lineage_canonical × register_canonical | n | % |
|---|---|---|
| fantasy_generic × fantasy | 921 | 95.0% |
| european × mythological | 18 | 1.9% |
| european × historical | 9 | 0.9% |
| european × fantasy | 5 | 0.5% |
| south_asian × mythological | 5 | 0.5% |
| mesoamerican × mythological | 3 | 0.3% |
| east_asian × historical | 2 | 0.2% |
| east_asian × mythological | 2 | 0.2% |
| middle_eastern × mythological | 2 | 0.2% |
| east_asian × fantasy | 1 | 0.1% |
| mesoamerican × historical | 1 | 0.1% |

**Empirical finding:** the named_template pool is overwhelmingly `fantasy_generic`/`fantasy`. Lineage-balanced filtering against named rows is NOT feasible — there are only ~48 non-`fantasy_generic` named rows total. Per Q-W15-S1-3, **elrond's recommendation: substrate-natural distribution (do not impose lineage balance at Stage 1).** Gandalf Stage 2 can refine the curation question if lineage diversification is a design priority.

**category rows (1,139) — DIFFERENT signal:**

| cultural_lineage_canonical | n |
|---|---|
| european | 823 |
| east_asian | 119 |
| fantasy_generic | 82 |
| south_asian | 52 |
| middle_eastern | 29 |
| southeast_asian | 23 |
| mesoamerican | 5 |
| african | 2 |
| south_american_indigenous | 1 |

**Architectural finding:** **category rows carry lineage signal; named_template rows do not.** If Stage 2 design wants lineage-conscious archetypes (e.g., "katana-wielding samurai" vs "claymore-wielding highlander"), the SUPPORTING evidence lives in the category-row pool, not the named-row pool. Audit defers to gandalf on whether to surface lineage as a Stage 2 archetype dimension.

**register_canonical for category rows:** 1,017 historical / 83 fantasy / 32 military_modern / 7 mythological. Historical/military substrate provides realistic-weapon coverage; fantasy substrate is the named_template surface.

**historical_period for category rows:** 410 early_modern + 325 industrial + 130 modern + 79 fictional + 73 contemporary + 62 medieval + 28 classical + 17 unknown + 15 pre_classical. **The substrate skews EARLY-MODERN through MODERN (~76% of category rows = 1600s-2020s firearms + military hardware).** This is the source of the DEX-ranged "gun/pistol/rifle" form vocabulary surfaced in § 2.

### 1.4 Per-attribute proxy_geometry_class distribution (BC damage-geometry axis)

Per substrate-vector cheatsheet § 2 (Axis 2 damage geometry: single-target / small-AOE / large-AOE / chain / multi-spawn) — substrate's `proxy_geometry_class` enum maps loosely:

| primary_stat | single | cleave | multi-hit | scatter | AoE | banner_rally_aura | shield_blocker |
|---|---|---|---|---|---|---|---|
| STR | 346 | 314 | 23 | 1 | 78 | 0 | 0 |
| DEX | 773 | 136 | 50 | 45 | 33 | 0 | 17 |
| INT | 149 | 1 | 0 | 0 | 6 | 0 | 0 |
| WIS | 103 | 6 | 0 | 0 | 42 | 7 | 0 |

**Substrate-vote findings (load-bearing for Stage 2):**

- **STR:** strong single+cleave duality (single 346 ~= cleave 314); modest AoE (78 — siege/mortar/large-blast cluster); negligible multi-hit. STR substrate VOTES dual-archetype (single-target heavy + cleave sweep) on damage-geometry axis.
- **DEX:** dominantly single (773 = 80% of DEX), with modest cleave (light blades), small multi-hit (machine-gun-like), scatter (shotgun-like), and very small AoE. DEX substrate VOTES precision/sniper-class single-target dominance.
- **INT:** essentially single-only (149 single + 6 AoE — and the AoE rows are sparse: powder magazines, pyromantic_ember_staff, conflagration_tome). **INT-AoE cell is empirically near-empty.** If Stage 2 wants AoE-INT classes (e.g., elementalist mage with fireball-AoE), substrate enrichment commission needed OR the AoE-INT archetype designs against very thin substrate.
- **WIS:** strong single+AoE duality (single 103, AoE 42); plus banner_rally_aura (7) for support-archetype. WIS substrate VOTES support/healer-class with AoE-buff/AoE-aura signature.

### 1.5 Per-attribute proxy_tempo_class distribution (BC damage-tempo axis)

| primary_stat | low | medium | high |
|---|---|---|---|
| STR | 321 | 408 | 33 |
| DEX | 246 | 398 | 397 |
| INT | 17 | 140 | 0 |
| WIS | 41 | 103 | 0 |

**Substrate-vote findings:**

- **STR:** balanced low+medium with sparse high (33 — likely flail/whip-like rapid strikes). STR substrate VOTES slow+measured tempo.
- **DEX:** balanced across all three tempo bins; **DEX is the only attribute with substantial `high` tempo substrate (397).** DEX substrate VOTES rapid-strike archetypes prominent.
- **INT:** medium-dominant, no `high` substrate. INT substrate VOTES measured-cast tempo.
- **WIS:** medium-dominant with low secondary, no `high`. WIS substrate VOTES measured-channel tempo.

### 1.6 Per-attribute range distribution (BC engagement axis)

| weapon_type_family | r_min_avg | r_max_avg | r_min_min | r_max_max |
|---|---|---|---|---|
| martial-heavy | 1.1 | 3.9 | 0.5 | 18.0 |
| martial-light | 0.5 | 2.5 | 0.5 | 3.0 |
| ranged | 4.5 | 15.2 | 2.5 | 18.0 |
| caster-arcane | 3.8 | 12.9 | 0.5 | 18.0 |
| caster-faith | 1.6 | 5.9 | 0.5 | 18.0 |

**Substrate-vote findings:** caster-faith is RANGE-BIFURCATED (avg max 5.9, max-of-max 18.0) — both close-range melee implementations (mace, scepter) AND ranged implements (horn, banner-aura). caster-arcane is purely ranged-dominant (3.8-12.9 avg). martial-heavy r_max_max=18 reflects the siege-weapon outliers (cannon, ballista). martial-light is the tightest cluster (0.5-3.0 — knife-fight territory).

---

## 2. Candidate archetype seeds (~34 surfaced)

> **Per dispatch Out-of-scope:** these are SEEDS for gandalf Stage 2 curation, NOT a recommended class roster. Per Q-W15-S1-1: 34 seeds (tighter side of 30-50 range) per substrate evidence — substrate's natural clustering produces ~30 distinct archetype anchors; padding to 50 would manufacture archetypes without empirical vote.
>
> **Format per seed:** `**[Stat-Family] — [Archetype name]** — substrate evidence: [n] named+unique rows on form keyword [X]; supporting category rows: [n] on lineage [Y]; BC-axis coverage: [engagement / geometry / tempo].`

### 2.1 STR × martial-heavy (10 archetype seeds; over-saturated cell warrants internal differentiation)

1. **STR-Heavy-Sword Bruiser** — substrate evidence: 119 named+unique rows on `sword` form (Astora Greatsword, Migration Period sword, Tizona, Joyeuse, Hauteclere, Excalibur, Carnwennan, Galatine, Sword of Freyr, etc.) + 35 on `greatsword` form. Mythological match: Beowulf (Hrunting, Nægling), Arthurian (Excalibur, Galatine), Charlemagne (Joyeuse), El Cid (Tizona, Colada). Supporting category rows: bulk of european-historical sword corpus. BC-coverage: melee / cleave-or-single / medium-tempo.
2. **STR-Heavy-Hammer Crusher** — substrate evidence: 46 named+unique rows on `hammer` form + 10 on `maul` (Astral Grandhammer, Black Steel Greathammer, War Hammer, Aethermight Hammer, Angharad's Warhammer, Baleglyph Maul, Drakebite Maul). Mythological: Thor-adjacent (Mjölnir family absent from substrate named pool — surprising sparseness). BC-coverage: melee / cleave / low-tempo.
3. **STR-Heavy-Axe Berserker** — substrate evidence: 44 named+unique rows on `axe` form (Bandit Greataxe, Black Knight Greataxe, Berzerker Broadaxe, Black Dragon Warpick) + 19 on `club` form (primitive/savage variants). BC-coverage: melee / cleave / medium-tempo. Substrate anchors a "Norse-flavored brutality" register even without explicit lineage tagging.
4. **STR-Heavy-Polearm Soldier** — substrate evidence: 62 named+unique rows on `glaive` form + 48 on `halberd` + 30 on `lance` + 6 on `pike` + 5 on `polearm`. Reach + cleave. Lineage: european-medieval pole-weapon corpus (Beastskewer Glaive, Black Knight Glaive, Barrow Lance, Ancestral Lance). BC-coverage: mid / cleave / measured-tempo.
5. **STR-Heavy-Spear Lancer** — substrate evidence: 7 named+unique on `spear` form (Mistilteinn, gilgamesh_cedar_forest_spear) + plus the lance subset above. Distinct from polearm in single-target precision vs cleave. Mythological anchors: Mistilteinn (Norse), Gilgamesh's cedar-forest-spear, Gáe Bolg (absent — substrate gap). BC-coverage: mid / single / measured-tempo.
6. **STR-Heavy-Unarmed Brawler** — substrate evidence: 13 named+unique on `knuckle` form (Abyssal Bane Knuckle Duster, Abyssal Bane Spiked Knuckle Duster variants). Distinct kit identity (handheld brawler vs weapon-wielder). BC-coverage: melee / single+multi-hit / medium-tempo. Cycle 13 cohort had no monk-equivalent on STR side — substrate vote supports.
7. **STR-Heavy-Flail Chain-Wielder** — substrate evidence: 9 named+unique on `flail` form (Barbarian Flail) + 2 on `morningstar`. Smaller cluster but distinct mechanic identity (reach-extend + cleave + chain-physics potential). BC-coverage: melee / cleave / medium-tempo with substrate's only `high` tempo signal on STR-side.
8. **STR-Heavy-Pick Crusher** — substrate evidence: 7 named+unique on `pick` (Black Dragon Warpick subset). Distinct from hammer in armor-penetration register. Smaller substrate base; possibly fold into hammer archetype at Stage 2.
9. **STR-Heavy-Mace Smasher** — substrate evidence: 3 named+unique on `mace` form (STR cell — most mace forms are WIS-routed; STR-mace is the heavier-warhammer variant). Small substrate cluster — possibly fold into hammer at Stage 2 OR distinct register if "war-priest-with-mace" intended.
10. **STR-Heavy-Cleave-AoE Sweeper** — substrate evidence: 78 named+unique on STR `proxy_geometry_class='AoE'` (siege cluster: 10in mortar, 105mm howitzer, ballista, catapult, cannon variants) + Dread Catapult — Cauldron of Torment / Cursed Stele / Necrotic Skulls (fantasy-flavor catapult). Distinct archetype (siege-soldier / artillery-master) — modern register but mythologically extensible to "battle-mage-with-engines." BC-coverage: ranged / AoE / low-tempo. Substrate-supports a STR-ranged-AoE class (Cycle 13 cohort had none).

### 2.2 STR × ranged (3 archetype seeds; smaller cell — 36 named+unique rows)

11. **STR-Ranged-Cannon Artillerist** — substrate evidence: 24 named+unique on `cannon` form + 6 on `catapult` + 5 on `ballista` + 36 siege_vehicle category rows. Overlaps STR-Cleave-AoE Sweeper (§ 2.1 #10) — substrate-evidence supports treating them as one archetype OR splitting cannon/catapult into "modern artillery" vs "fantasy siege engine" registers.
12. **STR-Ranged-Thrown Spear** — substrate evidence: 0 explicit `javelin`/`throw` keyword hits on STR cell; substrate-supports as a Stage 2 design-call against thin evidence (or commission substrate enrichment for STR-thrown). Listed for completeness; substrate vote is LOW.
13. **STR-Ranged-Heavy-Crossbow** — substrate evidence: 1 explicit `crossbow` on STR cell. Almost no substrate; would require enrichment. Listed for completeness.

### 2.3 DEX × martial-light (7 archetype seeds)

14. **DEX-Light-Dagger Assassin** — substrate evidence: 41 named+unique on `dagger` form + 13 on `kris` (curved/wave-blade dagger variant). Mythological match: Carnwennan (Arthur's dagger). BC-coverage: melee / single / high-tempo (DEX substrate's high-tempo lives heavily on dagger forms).
15. **DEX-Light-Sword Fencer** — substrate evidence: 13 named+unique on `sword` form (Swiss sabre, etc.) + 2 on `shortsword`. Distinct from dagger in reach + parry potential. BC-coverage: melee / single / medium-tempo.
16. **DEX-Light-Curved-Blade Saberist** — substrate evidence: 4 named+unique on `sabre`/`saber` + 3 on `scimitar` + 3 on `kukri`. Lineage-diverse cluster (Swiss sabre, Kukri, scimitars). BC-coverage: melee / single+cleave-hybrid / medium-high tempo.
17. **DEX-Light-Claw Wildhunter** — substrate evidence: 12 named+unique on `claw` form (Claw of the Black Drake, Claw of the Watcher, Crushing Claw and Gilded Weapon). Distinct kit identity (multi-hit signature; DEX's `multi-hit=50` cluster anchors here). BC-coverage: melee / multi-hit / high-tempo.
18. **DEX-Light-Rapier Duelist** — substrate evidence: 2 named+unique on `rapier` form. Small substrate base; possibly fold into Fencer at Stage 2.
19. **DEX-Light-Katana Iaijutsu** — substrate evidence: 1 named+unique on `katana` form (Kogarasu Maru — Amakuni, east_asian, tier_2). Very thin substrate; if east_asian register is wanted, enrichment needed.
20. **DEX-Light-Shield-Skirmisher** — substrate evidence: 17 shield rows routed to DEX-martial-light via `melee_close_or_grapple` proxy_range (Pavise, Rondache, Targe, Dhàl, Shield of Saint George, Rhos Rydd Shield). Distinct from STR-tank — DEX-shield is "mobile-blocker" register. BC-coverage: melee / single+shield_blocker / medium-tempo. **Substrate supports a dedicated shield-archetype OR shield-as-support-chain-evidence per § 4** (see § 2.5 + § 4).

### 2.4 DEX × ranged (5 archetype seeds; rich form-vocabulary)

21. **DEX-Ranged-Bow Archer** — substrate evidence: 15 named+unique on `bow` form (Gandiva — Arjuna/vedic, mythological tier_1; Bowstring Bow; Horn Bow variants). Substrate is thin on bow vs gun — substrate skews early-modern-firearm-heavy per § 1.3 historical_period. BC-coverage: ranged / single / medium-tempo.
22. **DEX-Ranged-Crossbow Sniper** — substrate evidence: 7 named+unique on `crossbow` form. BC-coverage: ranged / single / low-tempo (slow but high-impact register).
23. **DEX-Ranged-Firearm Gunslinger** — substrate evidence: 100 named+unique on `gun` form + 94 on `pistol` + 88 on `rifle` + 16 on `musket` — the largest single form-vocabulary cluster in the substrate. Lineage: european + middle_eastern + east_asian (industrial period dominant). **Substrate strongly supports a modern-firearm class archetype** (Cycle 13 cohort had no equivalent — sniper was the closest, but pistol/dual-wield gunslinger archetype absent). BC-coverage: ranged / single / medium-high tempo.
24. **DEX-Ranged-Shotgun Scatter-Shooter** — substrate evidence: 45 `proxy_geometry_class='scatter'` rows (Centrefire breech-loading double-barrelled shotgun variants, Flintlock blunderbuss, Grenade Launching Blunderbuss). Distinct kit identity (close-range AoE-cone). BC-coverage: mid+ranged / scatter (cone_aoe analog) / medium-tempo.
25. **DEX-Ranged-Machine-Gun Rapid-Striker** — substrate evidence: 50 `proxy_geometry_class='multi-hit'` rows (Centrefire automatic belt-fed machine gun variants, sub-machine guns). Distinct kit identity (high-rate-of-fire sustained). BC-coverage: ranged / multi-hit / high-tempo. Modern-register; gandalf Stage 2 design-call on fictional analog if fantasy-register preferred.
26. **DEX-Ranged-Thrown Javelin** — substrate evidence: 53 named+unique on `javelin` form (per § 2 query). Distinct from bow in reach + single-target heavy-impact register. BC-coverage: mid+ranged / single / medium-tempo.

### 2.5 INT × caster-arcane (4 archetype seeds; smaller cell)

27. **INT-Arcane-Staff Wizard** — substrate evidence: 64 named+unique on `staff` form. Anchors the canonical "wizard" register. BC-coverage: mid+ranged / single / medium-tempo.
28. **INT-Arcane-Wand Magus** — substrate evidence: 4 named+unique on `wand` form. Surprisingly small substrate vs canonical-genre expectation. Possibly fold into Wizard at Stage 2.
29. **INT-Arcane-Rod Channeler** — substrate evidence: 54 named+unique on `rod` form (Rod of Icicles, Elk Horn Rod, Rod of the Pact Keeper). Distinct from staff in single-hand wieldability. BC-coverage: mid+ranged / single / medium-tempo.
30. **INT-Arcane-Crystal Familiar** — substrate evidence: 27 named+unique on `crystal` form. Distinct kit identity (focus-implement; possibly summoner-adjacent given "Crystal Familiar" Cycle 13 cohort name). BC-coverage: mid / single / low-tempo. **INT-AoE substrate is empirically empty (6 thin rows only)** — see § 3.2 gap analysis.

### 2.6 WIS × caster-faith (4 archetype seeds)

31. **WIS-Faith-Mace Crusader** — substrate evidence: 90 named+unique on `mace` form (largest WIS cluster). Anchors the canonical "holy knight / war-priest" register. BC-coverage: melee+mid / single+cleave / measured-tempo.
32. **WIS-Faith-Staff Cleric** — substrate evidence: 5 named+unique on `staff` form (WIS-routed). Distinct from INT-staff in healing/support register vs damage. Substrate is thin — folding into Channeler more likely.
33. **WIS-Faith-Horn Caller** — substrate evidence: 21 named+unique on `horn` form (Envoy's Horn, Faun's Horn, Goat's Horn, Herculean Horn, Hunting Horn, Demon's Horn, Elk Horn Rod). Distinct kit identity (AoE-buff aura / rally / call-to-arms). BC-coverage: ranged / AoE / low-tempo. Substrate STRONGLY supports a horn-caller / war-bard / huntsman-rally archetype.
34. **WIS-Faith-Talisman Holy-Channeler** — substrate evidence: 11 talisman rows + 7 banner rows + 42 generic AoE rows (Aegis, Censer of Righteousness, Holy Water Sprinkler, Devotee's Censer, Great Plague Censer, Darkmoon Talisman, Sunlight Talisman, Thorolund Talisman, Canvas Talisman variants). Anchors AoE-buff / heal-aura / banner-rally support archetype. BC-coverage: ranged / AoE / low-tempo. Per dispatch Item 3 supporting-chain candidate evidence — § 4.

### 2.7 Support-archetype substrate (off-hand evidence; not main-weapon archetypes)

Per § 1.1, these 184 rows are excluded from main-weapon role by Fix A hygiene filter, but they DO provide substrate evidence for SUPPORTING-CHAIN identity per doc 40 § 6.6.1 Option C — class-intrinsic passives absorbing into a T3-cap supporting chain.

- **Shield substrate (17 rows; DEX-routed):** supports "shield-skirmisher" supporting-chain identity for tank-flavored DEX classes
- **Banner substrate (7 rows; WIS-routed):** supports "rally-aura / banner-call" supporting-chain identity for WIS leader-flavored classes
- **Talisman/horn substrate (12 rows; WIS-routed):** supports "blessing-aura / channel-prayer" supporting-chain identity for WIS holy classes
- **Tome/focus (rare; INT-routed):** supports "lore-recall / spell-mastery" supporting-chain identity for INT mage classes (substrate thin; possible enrichment commission)

These rows REAPPEAR in § 4 as supporting-chain candidate evidence per archetype.

---

## 3. BC-axis coverage cross-reference

Per dispatch Item 2 + substrate-vector cheatsheet § 1 (8 BC axes).

### 3.1 Coverage matrix (substrate vote per archetype seed × BC axis)

Per cheatsheet § 2 operational definitions, mapping the 34 seeds to BC-axis cells. Engagement profile = composite range × mobility (mobility undetermined at substrate; range derived from § 1.6); damage geometry = proxy_geometry_class mapping; damage tempo = proxy_tempo_class.

| Seed # | Archetype | Engagement (range) | Damage Geometry | Damage Tempo | Stat Affinity | Notes |
|---|---|---|---|---|---|---|
| 1 | STR-Sword Bruiser | melee | cleave+single | medium | STR | Mythological-anchored |
| 2 | STR-Hammer Crusher | melee | cleave | low | STR | |
| 3 | STR-Axe Berserker | melee | cleave | medium | STR | |
| 4 | STR-Polearm Soldier | mid | cleave | medium | STR | reach |
| 5 | STR-Spear Lancer | mid | single | medium | STR | |
| 6 | STR-Unarmed Brawler | melee | single+multi-hit | medium | STR | distinct from weapon-wielders |
| 7 | STR-Flail Chain-Wielder | melee | cleave | medium-high | STR | rare high-tempo STR |
| 8 | STR-Pick Crusher | melee | single | low | STR | thin substrate |
| 9 | STR-Mace Smasher | melee | single | low | STR | thin substrate; fold candidate |
| 10 | STR-Cleave-AoE Sweeper | ranged | AoE | low | STR | siege/artillery |
| 11 | STR-Cannon Artillerist | ranged | AoE | low | STR | overlaps #10 |
| 12 | STR-Thrown Spear | mid | single | medium | STR | thin substrate |
| 13 | STR-Heavy-Crossbow | ranged | single | low | STR | thin substrate |
| 14 | DEX-Dagger Assassin | melee | single | high | DEX | |
| 15 | DEX-Sword Fencer | melee | single | medium | DEX | |
| 16 | DEX-Saberist | melee | single+cleave | medium-high | DEX | lineage-diverse |
| 17 | DEX-Claw Wildhunter | melee | multi-hit | high | DEX | distinct multi-hit signature |
| 18 | DEX-Rapier Duelist | melee | single | medium | DEX | thin; fold candidate |
| 19 | DEX-Katana Iaijutsu | melee | single+cleave | medium | DEX | thin; lineage-specific |
| 20 | DEX-Shield-Skirmisher | melee | single+shield_blocker | medium | DEX | tank-flavored DEX |
| 21 | DEX-Bow Archer | ranged | single | medium | DEX | |
| 22 | DEX-Crossbow Sniper | ranged | single | low | DEX | |
| 23 | DEX-Firearm Gunslinger | ranged | single | medium-high | DEX | largest substrate cluster |
| 24 | DEX-Shotgun Scatter | mid+ranged | scatter (cone_aoe) | medium | DEX | |
| 25 | DEX-MG Rapid-Striker | ranged | multi-hit | high | DEX | modern register |
| 26 | DEX-Javelin Thrower | mid+ranged | single | medium | DEX | |
| 27 | INT-Staff Wizard | mid+ranged | single | medium | INT | canonical wizard |
| 28 | INT-Wand Magus | mid+ranged | single | medium | INT | thin; fold candidate |
| 29 | INT-Rod Channeler | mid+ranged | single | medium | INT | |
| 30 | INT-Crystal Familiar | mid | single | low | INT | summoner-adjacent |
| 31 | WIS-Mace Crusader | melee+mid | single+cleave | measured | WIS | holy knight |
| 32 | WIS-Staff Cleric | mid | single | measured | WIS | thin; fold candidate |
| 33 | WIS-Horn Caller | ranged | AoE | low | WIS | rally/buff aura |
| 34 | WIS-Talisman Channeler | ranged | AoE | low | WIS | heal/aura/banner |

### 3.2 BC-cell gaps (substrate-empty cells; gandalf design-call territory)

Per dispatch Item 2 — surfacing cells with NO candidate archetype OR thin substrate:

| Gap | Substrate state | Stage 2 implication |
|---|---|---|
| **INT × AoE damage-geometry** | 6 thin rows (powder magazine, conflagration_tome, pyromantic_ember_staff) | Stage 2 must EITHER commission substrate enrichment for AoE-INT (fireball / chain-lightning canonical mage forms surprisingly absent from substrate) OR design INT classes around `single`-only damage-geometry (more "arcane single-target striker" than "elemental AoE blaster") |
| **INT × high-tempo** | 0 rows | INT cannot have rapid-cast archetypes from substrate; design call: accept measured/slow-cast as INT identity OR enrichment |
| **WIS × high-tempo** | 0 rows | Same as INT — WIS substrate votes measured tempo only |
| **WIS × close-melee dagger/martial-light** | 0 named+unique rows | WIS-monk-style close-combat archetype has no substrate vote (Cycle 13's wis_05_monk had to draw from generic mace/staff substrate) |
| **STR × ranged general** | 36 named+unique rows (siege-dominant) | STR-ranged archetypes confined to siege/cannon/heavy-crossbow registers — no STR-thrown-spear / STR-javelin substrate; if "barbarian thrower" desired, enrichment needed |
| **STR × high-tempo** | 33 rows (mostly flail-related) | STR-rapid-strike confined to flail/whip archetype; STR-monk (rapid unarmed) has 13 knuckle-form rows only |
| **DEX × AoE** | 33 rows | Thin substrate for DEX-AoE; DEX-shotgun (#24 scatter) is the closest substrate-supported AoE archetype |

### 3.3 BC-cell over-saturation (cells with many competing candidates)

Per dispatch Item 2:

| Over-saturated cell | Candidate archetype seeds | Stage 2 implication |
|---|---|---|
| **STR-melee-cleave-medium-tempo** | Seeds #1, #2, #3, #4, #7 (sword/hammer/axe/polearm/flail bruisers) | 5 candidates for one BC cell — gandalf Stage 2 must collapse or differentiate via secondary signal (lineage, mythological anchor, ranged-or-not, supporting chain identity) |
| **DEX-melee-single-high-tempo** | Seeds #14 (dagger), partially #15 (fencer sword), #16 (saber subset) | 3 candidates clustering; differentiate via reach (dagger close vs fencer mid-melee) or single-target-vs-cleave-secondary |
| **DEX-ranged-single-medium** | Seeds #21 (bow), #22 (crossbow), #23 (firearm), #26 (javelin) | 4 candidates competing on the canonical "ranged single-target precision" cell — gandalf differentiates via tempo (low vs medium vs high) + reload-mechanic + register (medieval vs modern vs primitive) |
| **INT-mid-ranged-single-medium** | Seeds #27 (staff), #28 (wand), #29 (rod) | 3 candidates clustering; fold into 1-2 archetypes or differentiate via 1-hand vs 2-hand + supporting-chain identity |

### 3.4 Cycle 13 cohort BC-axis coverage (INFORMATIONAL — Q9 disregarded)

Per dispatch reading-list reference: Cycle 13's 16 characters cover this BC profile (substrate-derived; INFORMATIONAL only):

| Cycle 13 character | Substrate-derived archetype seed | Notes |
|---|---|---|
| S1_endgame_dex_01_dagger_assassin | Seed #14 (DEX-Dagger Assassin) | covered |
| S1_endgame_dex_02_archer | Seed #21 (DEX-Bow Archer) | covered |
| S1_endgame_dex_03_crossbow_sniper | Seed #22 (DEX-Crossbow Sniper) | covered |
| S1_endgame_dex_04_twin_blade_fencer | Seed #15+#18 (DEX-Sword Fencer + Rapier Duelist hybrid) | partial — substrate thin on twin-blade specifically |
| S1_endgame_int_01_standard_wizard | Seed #27 (INT-Staff Wizard) | covered |
| S1_endgame_int_03_pyromantic_caster | NO clean seed — INT-AoE substrate empty per § 3.2 | substrate-gap exposed |
| S1_endgame_int_04_red_mage_spellsword | NO clean seed — INT+martial hybrid substrate empty | substrate-gap exposed |
| S1_endgame_int_05_arcane_familiar_mage | Seed #30 (INT-Crystal Familiar) | covered |
| S1_endgame_str_01_heavy_barbarian | Seed #1 or #3 (STR-Sword/Axe Bruiser) | covered |
| S1_endgame_str_02_light_fighter | NO clean seed — STR-light substrate thin | substrate-gap exposed |
| S1_endgame_str_03_polearm_soldier | Seed #4 (STR-Polearm Soldier) | covered |
| S1_endgame_wis_01_channeling_cleric | Seed #34 (WIS-Talisman Channeler) | covered |
| S1_endgame_wis_02_holy_knight | Seed #31 (WIS-Mace Crusader) | covered |
| S1_endgame_wis_03_ritual_mage | Seed #34 (WIS-Talisman Channeler variant) | overlap |
| S1_endgame_wis_04_storm_caller | NO clean seed — WIS-high-tempo substrate empty | substrate-gap exposed |
| S1_endgame_wis_05_monk | NO clean seed — WIS-melee-light substrate empty | substrate-gap exposed |

**Cycle 13 substrate-gap pattern:** 5 of 16 Cycle 13 characters (31%) operate against substrate-empty BC cells (red_mage_spellsword, pyromantic_caster, str_light_fighter, wis_storm_caller, wis_05_monk). This is INFORMATIONAL data for Stage 2 — gandalf can either close these gaps via substrate enrichment commissions OR design the Cycle 14 roster around substrate-supported archetypes.

**Substrate-unrepresented archetype seeds (Cycle 14 NEW candidates beyond Cycle 13):**

- #6 STR-Unarmed Brawler (Cycle 13 had no STR-monk)
- #7 STR-Flail Chain-Wielder
- #10/#11 STR-Cleave-AoE Sweeper / Cannon Artillerist (Cycle 13 had no STR-ranged)
- #17 DEX-Claw Wildhunter
- #20 DEX-Shield-Skirmisher
- #23 DEX-Firearm Gunslinger (Cycle 13 had crossbow sniper, no pistol/MG variant)
- #24 DEX-Shotgun Scatter
- #25 DEX-MG Rapid-Striker
- #33 WIS-Horn Caller (Cycle 13 had no banner/rally archetype)

---

## 4. Chain-count + supporting-chain candidate evidence per archetype

> **Per dispatch Out-of-scope:** EVIDENCE only; does NOT lock per-class chain counts OR identify final supporting-chain identities. Gandalf Stage 2 design-call territory.
>
> **Doc 40 § 8.3 chain-count rule:** 3-chain class = 2 T4 + 1 supporting; 4-chain class = 3 T4 + 1 supporting. T4 count = chain count − 1.
>
> **Substrate evidence for chain count:** does the archetype's substrate naturally suggest 3 OR 4 chains? Evidence comes from (a) weapon-kind variety within the seed's substrate cluster + (b) damage-geometry diversity (single/cleave/AoE) + (c) tier coverage at substrate row level.
>
> **Substrate evidence for supporting chain:** what class-intrinsic passive theme absorbs (per doc 40 § 6.6.1 Option C)? Substrate evidence: shared aesthetic / tone / register / off-hand utility across the archetype's row cluster.

### 4.1 STR archetype seeds — chain-count + supporting-chain evidence

| Seed # | Chain-count substrate vote | Supporting-chain candidate evidence |
|---|---|---|
| 1 STR-Sword Bruiser | **3 or 4** — substrate has single+cleave+AoE (siege-adjacent) coverage AND mythological lineage diversity (Norse/Arthurian/Charlemagne). Could be 3-chain "concentrated bruiser" OR 4-chain "versatile veteran" | **Substrate evidence for supporting chain:** mythological-anchor passives ("blessed-weapon" / "named-blade-mastery" — drawn from 18 european-mythological named rows). Class-intrinsic theme: "weapon-mastery / blade-lore" passive surface |
| 2 STR-Hammer Crusher | **3** — substrate is cleave-heavy single-geometry-dominant; less internal variety than #1; 3-chain "concentrated" architecture votes | **Supporting:** "earth-shaking / siege-impact" passives — composes with #10 STR-Cleave-AoE if hybrid. Substrate thin on hammer-mythos (no Mjölnir in substrate); supporting-chain theme more elemental/physical-impact than character-mythos |
| 3 STR-Axe Berserker | **3** — cleave-dominant single archetype identity; substrate clean on axe form alone | **Supporting:** "rage / battle-fury / berserker-trance" passives — substrate skews savage/primitive (Bandit Greataxe, Berzerker Broadaxe). Class-intrinsic theme: rage-on-hit, battle-trance |
| 4 STR-Polearm Soldier | **4** — substrate carries reach (glaive/halberd) + thrust (lance/pike) + cleave (polearm) variety; 4-chain "soldier-versatility" votes | **Supporting:** "formation-discipline / military-drill" passives — substrate skews european-medieval drill (Beastskewer Glaive, Black Knight Glaive, Barrow Lance). Class-intrinsic theme: armor-piercing, formation-bonus |
| 5 STR-Spear Lancer | **3** — single-target dominant; thin variety; 3-chain "concentrated spear-mastery" | **Supporting:** "thrust-precision / mounted-charge" passives. Composes with #4 polearm OR distinct if mythological (Mistilteinn) |
| 6 STR-Unarmed Brawler | **3** — 13 substrate rows is thin; 3-chain "concentrated unarmed-master" | **Supporting:** "ki-strike / body-as-weapon" passives — substrate skews abyssal/savage register (Abyssal Bane Knuckle Duster). Class-intrinsic theme: critical-strike, multi-hit chain |
| 7 STR-Flail Chain-Wielder | **3** — 9 rows; very thin; 3-chain concentrated | **Supporting:** "reach-extend / disarm" passives — distinct flail-mechanic-anchored. Substrate has Barbarian Flail; theme could be "chain-and-spike control" |
| 8/9 STR-Pick/Mace | **3** — thin substrate; likely fold into Hammer at Stage 2 | — (likely folded) |
| 10 STR-Cleave-AoE Sweeper | **3 or 4** — substrate diverse (siege-mortar + dread-catapult + cannon — modern + fantasy registers split) | **Supporting:** "siege-engine-mastery / artillery-tactics" passives. Could pair with #11 if not folded |
| 11 STR-Cannon Artillerist | **3** — substrate overlaps #10; likely 3-chain concentrated artillery | **Supporting:** "loader-rhythm / ammunition-craft" passives |
| 12/13 STR-Thrown/Crossbow | **3** — thin; possibly fold | — |

### 4.2 DEX archetype seeds — chain-count + supporting-chain evidence

| Seed # | Chain-count substrate vote | Supporting-chain candidate evidence |
|---|---|---|
| 14 DEX-Dagger Assassin | **3** — single+high-tempo concentrated archetype; 3-chain "concentrated assassination" | **Supporting:** "stealth-strike / poison-craft / shadow-step" passives — substrate has mythological-shadow anchor (Carnwennan). Class-intrinsic theme: critical-from-stealth, status-application |
| 15 DEX-Sword Fencer | **3** — single-dominant; smaller substrate; 3-chain "concentrated fencing" | **Supporting:** "parry-mastery / riposte-stance" passives |
| 16 DEX-Saberist | **4** — lineage-diverse (european saber + kukri + scimitar) + single+cleave dual-geometry signal; 4-chain "versatile curved-blade" votes | **Supporting:** "draw-cut / iaijutsu / sweep-recovery" passives — substrate skews east_asian/middle_eastern lineage even at thin substrate |
| 17 DEX-Claw Wildhunter | **3** — distinct multi-hit signature; concentrated; 3-chain | **Supporting:** "feral-instinct / pack-coordination / track-prey" passives — substrate has fantasy-savage register (Claw of the Black Drake, Claw of the Watcher) |
| 18 DEX-Rapier Duelist | thin — fold into #15 | — (likely folded) |
| 19 DEX-Katana Iaijutsu | thin — substrate cannot vote 3 vs 4; design call needed | — (substrate enrichment commission would unlock) |
| 20 DEX-Shield-Skirmisher | **3** — substrate has shield + light-blade hybrid evidence (17 shield rows); 3-chain "concentrated mobile-defender" | **Supporting:** "shield-bash / bulwark-stance / mobile-block" passives — substrate has explicit shield_blocker proxy_geometry signal AND lineage-diverse shields (Pavise, Rondache, Dhàl, Targe). Class-intrinsic theme: defensive-conversion (per doc 40 § 8.4 algorithm strategy DEFENSIVE_CONVERSION). **This is the cleanest substrate-evidenced supporting-chain candidate in the audit** |
| 21 DEX-Bow Archer | **3** — single-dominant; concentrated; 3-chain | **Supporting:** "arrow-craft / wind-reading / quiver-mastery" passives |
| 22 DEX-Crossbow Sniper | **3** — single+low-tempo concentrated | **Supporting:** "reload-rhythm / heavy-bolt-impact / cover-discipline" passives |
| 23 DEX-Firearm Gunslinger | **4** — substrate is the largest (288 named+unique on gun+pistol+rifle+musket) AND geometry-diverse (single + multi-hit + scatter all in DEX-ranged); 4-chain "versatile gunslinger" votes — multiple firearm-form chains (pistol vs rifle vs shotgun vs MG) | **Supporting:** "reload-mastery / quick-draw / aim-precision" passives — distinct from #24 and #25 if those are separate classes; fold into one super-class if not |
| 24 DEX-Shotgun Scatter | **3** — substrate distinct (45 scatter rows); concentrated cone-AoE archetype | **Supporting:** "spread-control / close-quarters-discipline" passives. Could fold into #23 as a chain |
| 25 DEX-MG Rapid-Striker | **3** — substrate distinct (50 multi-hit rows); concentrated suppression archetype | **Supporting:** "sustained-fire / barrel-cooling / ammo-belt-mastery" passives. Could fold into #23 as a chain |
| 26 DEX-Javelin Thrower | **3** — single+mid-range concentrated; 3-chain | **Supporting:** "throw-precision / spear-retrieve" passives |

### 4.3 INT archetype seeds — chain-count + supporting-chain evidence

| Seed # | Chain-count substrate vote | Supporting-chain candidate evidence |
|---|---|---|
| 27 INT-Staff Wizard | **4** — staff is the largest INT cluster (64 rows) AND substrate carries some range/tempo variety; 4-chain "versatile mage" votes IF elemental sub-chains are accepted (despite AoE-substrate empty per § 3.2 — sub-chain identity comes from element, not geometry) | **Supporting:** "spell-lore / mana-channel / arcane-recall" passives — substrate has lineage signal (Pact Keeper, Ember Staff, Conflagration Tome) at thin density. Class-intrinsic theme: knowledge-mastery, spell-efficiency |
| 28 INT-Wand Magus | thin — fold into #27 | — (likely folded) |
| 29 INT-Rod Channeler | **3** — single-hand wieldability + 54 rows = distinct from staff; 3-chain "concentrated channeler" | **Supporting:** "rod-channel / focus-rite / spell-bind" passives |
| 30 INT-Crystal Familiar | **3** — 27 rows distinct; possibly summoner-adjacent if proxy-density substrate enrichment commissioned; 3-chain | **Supporting:** "familiar-bond / crystal-attunement / summon-discipline" passives. Per substrate-vector cheatsheet § 3, this archetype touches Axis 2A proxy_density (proxy-light cluster); substrate currently has no proxy-count metadata — Stage 2 design-call territory |

### 4.4 WIS archetype seeds — chain-count + supporting-chain evidence

| Seed # | Chain-count substrate vote | Supporting-chain candidate evidence |
|---|---|---|
| 31 WIS-Mace Crusader | **3 or 4** — substrate has melee+mid-range mace + holy-aura adjacent (cross-cell with #34) potential; 3-chain concentrated OR 4-chain hybrid-holy-knight | **Supporting:** "blessing-aura / divine-protection / consecrated-ground" passives — substrate has the AoE evidence (Aegis, Censer of Righteousness, Holy Water Sprinkler) anchoring the holy-knight-as-AoE-aura-bearer supporting chain. **Cross-cell composition: WIS-Mace-Crusader supporting chain CAN absorb the WIS-Talisman-Channeler AoE substrate as class-intrinsic** |
| 32 WIS-Staff Cleric | thin — fold into #34 likely | — |
| 33 WIS-Horn Caller | **3** — 21 horn rows distinct; concentrated rally archetype; 3-chain "concentrated caller" | **Supporting:** "rally-call / banner-presence / hunt-coordination" passives — substrate has the banner subset (7 rows) anchoring "leader-flag-bearer" class-intrinsic theme. Distinct register from #31 (martial-rally vs holy-aura) |
| 34 WIS-Talisman Channeler | **3 or 4** — substrate has talisman + censer + sprinkler + horn variety; 3-chain concentrated OR 4-chain versatile holy-channeler. Substrate vote ambiguous; depends on design intent | **Supporting:** "consecration / litany / divine-channel" passives — substrate is uniformly AoE-low-tempo (no high-tempo cast support; substrate vote against rapid-cleric); class-intrinsic theme: aura-stacking, channel-uninterrupted |

### 4.5 Aggregate chain-count substrate vote across 34 seeds

| Substrate vote | Seed count | % |
|---|---|---|
| 3-chain (concentrated archetype) | 22 | 65% |
| 4-chain (versatile archetype) | 5 | 15% |
| 3 or 4 (ambiguous; design call) | 4 | 12% |
| Thin substrate (fold candidate) | 3 | 9% |

**Substrate-natural distribution: ~2/3 of archetype seeds vote 3-chain (concentrated identity).** This is INFORMATIONAL for Stage 2; gandalf design-call territory on whether per-class chain counts should follow substrate vote OR be set per design intent independent of substrate.

---

## 5. Recommended Stage 2 design-call agenda (questions for gandalf)

Per dispatch Item 4 § 5; questions for gandalf to answer in Stage 2 class-roster design call.

### 5.1 Roster-selection questions

- **Q-S2-1 (Roster cardinality):** the substrate surfaces 34 candidate archetype seeds; gandalf curates to N classes. What N is target? Composes with season-cardinality decision (n_kits=40 default per consolidated package § 3.4). Roster N << 40 (multiple kits per class via BC-cell variation); plausible roster sizes: 8 (one per primary_stat × 2 archetypes/stat) to 20 (substrate-natural plus differentiation)
- **Q-S2-2 (Fold-vs-distinct):** several seeds are fold candidates (thin substrate; overlap with larger archetype). Specifically: #8 Pick, #9 Mace (STR), #18 Rapier, #19 Katana, #28 Wand, #32 WIS-Staff. Fold per gandalf design call OR keep distinct OR commission substrate enrichment?
- **Q-S2-3 (Substrate-gap closure):** Cycle 13 cohort exposed 5 substrate-gap archetypes (red_mage_spellsword, pyromantic_caster, str_light_fighter, wis_storm_caller, wis_05_monk). Per Q-W15-S1-2 (comprehensive coverage vote): does Cycle 14 close these gaps via substrate enrichment commissions to elrond OR design around substrate-supported archetypes only?
- **Q-S2-4 (Lineage architecture):** named+unique substrate is 95% `fantasy_generic`; category substrate has rich lineage signal (823 european / 119 east_asian / 52 south_asian / etc.). Should lineage be a Stage 2 archetype-discrimination axis (e.g., "katana-samurai" vs "claymore-highlander" both as DEX-saberist variants)? If yes, substrate-evidence anchoring shifts from named pool to category pool

### 5.2 Chain-count + supporting-chain questions

- **Q-S2-5 (Per-class chain count assignment):** substrate-natural vote is ~2/3 3-chain. Does gandalf accept substrate-natural distribution OR set per-class chain count by design intent (e.g., "all classes 4-chain for versatility" OR "all classes 3-chain for concentration")?
- **Q-S2-6 (Supporting chain identity):** § 4 surfaces supporting-chain candidate themes per archetype. Some have STRONG substrate evidence (e.g., #20 DEX-Shield-Skirmisher → defensive-conversion supporting chain from 17 shield rows). Others are gandalf-design-derived (e.g., #1 STR-Sword Bruiser → "blessed-weapon mastery" — substrate is thin on mythological-name anchors but the inferred theme is coherent). Does Stage 2 prioritize substrate-evidenced supporting chains OR design-coherent supporting chains?
- **Q-S2-7 (Supporting-chain cross-class sharing):** Several archetype seeds share substrate evidence for similar supporting chains (e.g., #1 + #2 + #3 + #4 + #5 all STR-martial — could share a "weapon-mastery" supporting-chain pattern). Does Stage 2 design unique supporting chains per class (more variety; more design surface) OR shared supporting-chain templates across class families (less surface; more cohesion)?

### 5.3 BC-cell coverage questions

- **Q-S2-8 (INT-AoE substrate gap):** INT-AoE substrate is empirically near-empty (6 rows). Cycle 13's `int_03_pyromantic_caster` exposes this gap. Stage 2 options: (a) design INT classes around `single`-only damage-geometry (substrate-natural; aligns with "arcane sniper" register over "elemental blaster"); (b) commission substrate enrichment for AoE-INT spell-implement library; (c) accept design-spec-as-math-derived INT-AoE without substrate vote. Recommend?
- **Q-S2-9 (DEX-firearm class architecture):** substrate's largest single form-vocabulary cluster (288 named+unique on gun+pistol+rifle+musket) supports either ONE versatile 4-chain "gunslinger" class OR MULTIPLE 3-chain firearm specialists (sniper / shotgunner / MG / pistolero). Substrate vote is ambiguous; depends on roster cardinality and modern-register design intent
- **Q-S2-10 (Over-saturated STR-melee cell):** 5 archetype seeds compete for the STR-melee-cleave-medium-tempo cell (sword/hammer/axe/polearm/flail bruisers). Stage 2 must collapse or differentiate. Differentiation axes available from substrate: lineage (Norse-axe vs European-sword vs etc.); supporting chain theme (rage vs blade-lore vs siege); weapon-kind variety (single-handed vs two-handed vs polearm)
- **Q-S2-11 (Cross-attribute hybrid classes):** Cycle 13's `int_04_red_mage_spellsword` exposed a hybrid INT+martial archetype gap. Substrate's `secondary_stat` is uniformly `'none'` (no dual-attribute scaling); Cycle 14 hybrid classes would need design-spec-as-math derivation without substrate vote OR a fresh substrate-enrichment commission for hybrid weapons

### 5.4 Substrate-enrichment commission questions (elrond-bounce-back)

If Stage 2 surfaces substrate gaps that warrant enrichment, elrond can commission:

- **Q-S2-12 (INT-AoE enrichment):** commission a 30-50 row enrichment pass for AoE-INT spell-implement forms (canonical fireball-staff, chain-lightning-rod, blizzard-orb, meteor-tome) per existing substrate enrichment patterns (SC-6b precedent). Effort: ~3-5 hours elrond + cross-seam rocket sanity-check
- **Q-S2-13 (Cultural-lineage anchored named pool):** the named-template pool's 95% `fantasy_generic` tagging is a substrate gap if lineage-conscious archetypes are wanted. Commission a re-tagging pass on the named pool against the category-pool's lineage signal (823 european, etc.). Effort: ~6-10 hours elrond curation + LLM-assisted name parsing
- **Q-S2-14 (Hybrid-attribute substrate):** commission a hybrid-weapon substrate enrichment for cross-attribute classes (red mage's spellsword, paladin's holy-warrior). Architectural decision: extend `secondary_stat` enum coverage at substrate OR maintain hybrid as design-time-only derivation. Effort: ~5-8 hours + cross-seam rocket coordination on damage-routing implications per doc 47

---

## 6. Sign-off

**Author:** elrond (data steward — catalogue DB + abstraction-analysis seam)
**Status:** CURRENT — Wave 1.5 Stage 1 substrate-evidence audit complete; gandalf Stage 2 design-call ready

**Audit deliverables per dispatch acceptance criteria:**

- [x] Audit report filed at specified path with all 5 sections
- [x] 34 candidate archetype seeds surfaced with substrate-evidence anchoring per archetype (per Q-W15-S1-1: tighter side of dispatch's 30-50 range; substrate evidence does not support padding to 50 without manufacturing archetypes)
- [x] BC-axis coverage cross-reference complete; gaps + over-saturation identified per § 3.2 + § 3.3
- [x] Chain-count + supporting-chain candidate evidence surfaced per archetype per § 4
- [x] Stage 2 design-call agenda recommended (14 questions for gandalf to answer per § 5)
- [x] No DB schema changes; no canonical doc amendments
- [x] Cross-referenced SC-6 + SC-6b + doc 40 § 8.3 + § 6.6.1 + doc 46

**Out-of-scope adherence (per dispatch § Out of scope):**

- [x] Did NOT select the final class roster (gandalf Stage 2 territory)
- [x] Did NOT lock per-class chain counts (gandalf Stage 2 territory)
- [x] Did NOT identify final supporting-chain identities (gandalf Stage 2 design call territory)
- [x] Did NOT amend doc 40 / doc 46 / doc 47
- [x] Did NOT touch substrate library DB (audit only; all queries read-only)
- [x] Did NOT touch character JSON output schema
- [x] Did NOT enter Wave 1.5 implementation scope
- [x] Did NOT reproduce Cycle 13 16-archetype roster as the candidate pool (Q9 DISREGARD honored; Cycle 13 cohort referenced informationally only in § 3.4)

**Key structural findings load-bearing for Stage 2:**

1. **Substrate's archetype-vocabulary signal is FORM-derived, not character-mythos-derived.** Only 34/969 named+unique rows have `named_mythological_match` populated. Stage 2 archetype design should anchor on weapon-form (greatsword, dagger, staff, mace, bow, gun) as primary identity, with mythological-character anchors as secondary flavor where substrate supports
2. **STR-martial-heavy is 2.7× over-saturated relative to other primary_stat × weapon_type_family cells.** Multiple internal archetype differentiations warranted (10 seeds in this single cell). DEX-ranged has rich form-vocabulary diversity (5 seeds: bow / crossbow / firearm / shotgun / MG / javelin). INT and WIS cells are tighter (4 seeds each)
3. **INT-AoE substrate is empirically near-empty (6 thin rows).** Stage 2 must explicitly decide INT design direction: design around `single` damage-geometry OR commission substrate enrichment
4. **Lineage signal lives in CATEGORY rows (1,139), not NAMED rows (969 — 95% fantasy_generic).** If Stage 2 wants lineage-conscious archetypes, substrate-evidence shifts from named pool to category pool; OR commission a re-tagging pass on the named pool
5. **Substrate's natural chain-count vote is ~65% 3-chain (concentrated identity), 15% 4-chain (versatile), 12% ambiguous, 9% thin.** Gandalf Stage 2 decides whether to follow substrate-natural distribution OR impose design-uniform chain count

**For Wave 1.5 Stage 2:** this audit unblocks gandalf's class-roster design call. Substrate evidence is the curation input; gandalf curates the roster + locks per-class chain counts + identifies supporting-chain identities; rocket Wave 1.5 Stage 3 implements per Stage 2 spec.

**Cross-seam impact:** no immediate cross-seam impact from this audit (read-only). Stage 2 may surface substrate-enrichment commissions back to elrond (per § 5.4 Q-S2-12 through Q-S2-14) — those would be small additive enrichment passes following SC-6b pattern, not architectural schema changes.

**Signed:** elrond (data steward — catalogue DB + abstraction-analysis seam)
