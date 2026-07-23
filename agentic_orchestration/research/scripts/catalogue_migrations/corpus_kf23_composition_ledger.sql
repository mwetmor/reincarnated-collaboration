-- corpus_kf23_composition_ledger.sql
-- KF-2 composition ledgers (KFL-7 fold) — per pilot kit, per direction (dealt/received).
-- Author: elrond | 2026-07-23
-- Factor chain: base x skill/mastery modifiers x hit-chance x crit-EV x (1 - target mitigation).
-- Every factor labeled ANCHORED (verbatim source) / PINNED (charter ruling) / GAP-EXCLUDED (named, never estimated).
-- ref = anchor citation OR PIN id OR GAP id. Idempotent: DELETE the run's rows first, then re-insert (comp_id is
-- AUTOINCREMENT so INSERT OR REPLACE can't key on it; a scoped DELETE by kit_id keeps this rebuildable).
-- Gauge basis (charter §9): per-hit / per-tick, never DPS.

DELETE FROM kit_composition WHERE kit_id IN
  ('d2-firewall-sorc','d2-fire-sorc','gd-flames-of-ignaffar-purifier','poe2-bonestorm','poe1-cyclone');

-- =====================================================================================================
-- d2-firewall-sorc
-- =====================================================================================================
-- DEALT: Fire Wall sustained fire DoT. Gauge basis = per-tick; expected-per-cast = dmg/sec x 3.6s duration.
INSERT INTO kit_composition (kit_id, direction, factor_key, factor_role, status, factor_value, ref, notes) VALUES
('d2-firewall-sorc','dealt','base_dps','base','anchored','1296-1320 fire dmg/sec at slvl 20','rankedboost.com/diablo-2/sorceress/fire-wall/ (2026-07-23); kit_numeric firewall_dps_min/max_lvl20','Fire damage per second; DoT. Non-crit mean roll (Pin A).'),
('d2-firewall-sorc','dealt','fire_mastery_mult','modifier','anchored','+163% at FM slvl 20 (x2.63 multiplicative)','rankedboost.com/diablo-2/sorceress/fire-mastery/ (2026-07-23); kit_numeric firemastery_bonus_pct_lvl20','Multiplicative on base. Does NOT grant crit.'),
('d2-firewall-sorc','dealt','duration_to_percast','modifier','anchored','x 3.6 sec duration','diablo2.wiki.fextralife.com/Fire+Wall (2026-07-23); kit_numeric firewall_duration_sec','Expected-per-cast = dps x duration (stationary pass-through).'),
('d2-firewall-sorc','dealt','tick_rate','modifier','gap_excluded',NULL,'GAP-C5','Per-tick value = dps / tick_rate; tick rate un-anchored in any public source. Charter-registered GAP; per-cast gauge computes over dps x duration, tick granularity excluded + named (charter §9).'),
('d2-firewall-sorc','dealt','hit_chance','hit_chance','pinned','1.0','PIN-C2','D2 fire-skill hit-chance = 1 (spells bypass AR check; blanket verbatim unfindable, GAP-C2). PINNED not anchored.'),
('d2-firewall-sorc','dealt','crit_ev','crit_ev','pinned','1.0 (no crit)','Pin A / CONDUCTOR PIN #2','D2 spells have no crit; expected = non-crit mean. Crit factor = 1.'),
('d2-firewall-sorc','dealt','target_fire_resist','mitigation','anchored','target fire_resist_pct (0% for Act-1 Normal mobs, inferred)','monster_numeric *.fire_resist_pct (gap_flag=normal_resist_inferred)','Fire Wall is fire damage; mitigation = target fire resist. Sorc has no native -enemy resist (Lower Resist not native).');
-- RECEIVED: mob melee vs sorc. Sorc defensive sheet GAP -> received-% renders pre-mitigation + says so (charter §9 ladder).
INSERT INTO kit_composition (kit_id, direction, factor_key, factor_role, status, factor_value, ref, notes) VALUES
('d2-firewall-sorc','received','base_mob_damage','base','anchored','mob melee dmg (e.g. Fallen 1-2, Zombie 1-3)','monster_numeric d2-*.melee_dmg* (2026-07-23)','Per-hit physical mob damage, Act-1 Normal.'),
('d2-firewall-sorc','received','hit_chance','hit_chance','anchored','min(max(200%*(AR/(AR+Dr))*(ALVL/(ALVL+TLVL)),5%),95%)','maxroll.gg/d2/resources/hit-chance-mechanics (2026-07-23), formulas note C1; mob AR in monster_numeric ar_attack*','D2 chance-to-hit. Mob AR anchored (Fallen/Zombie=8); sorc Defense (Dr) at build point = GAP.'),
('d2-firewall-sorc','received','sorc_defense','hit_chance','gap_excluded',NULL,'GAP (d2 note: armor/defense rating not stated in any reachable source)','Sorc Defense rating (Dr term) un-anchored at build point. Hit-chance computes with Dr as a gap; received-% falls back pre-mitigation ladder (charter §9).'),
('d2-firewall-sorc','received','crit_ev','crit_ev','pinned','1.0 (mobs, no crit modeled)','Pin A / CONDUCTOR PIN #2','D2 Normal mobs; no crit-EV term curated.'),
('d2-firewall-sorc','received','sorc_mitigation','mitigation','gap_excluded',NULL,'GAP (d2 note: fire/cold/lightning/poison resist + armor at build point GAP)','Sorc resists/armor at build point un-anchored. Received-% renders pre-mitigation and says so (charter §9 fallback ladder).');

-- =====================================================================================================
-- d2-fire-sorc (Fire Ball + Meteor)
-- =====================================================================================================
-- DEALT: two skills. Fire Ball single-hit; Meteor impact-hit + ground-burn DoT. Gauge basis per-hit / per-tick.
INSERT INTO kit_composition (kit_id, direction, factor_key, factor_role, status, factor_value, ref, notes) VALUES
('d2-fire-sorc','dealt','base_fireball','base','anchored','227-258 fire per cast at slvl 20','rankedboost.com/diablo-2/sorceress/fire-ball/ (2026-07-23); kit_numeric fireball_dmg_min/max_lvl20','Single-hit fire projectile. Non-crit mean (Pin A).'),
('d2-fire-sorc','dealt','base_meteor_impact','base','anchored','955-1019 impact fire at slvl 20','rankedboost.com/diablo-2/sorceress/meteor/ (2026-07-23); kit_numeric meteor_impact_min/max_lvl20','Meteor impact single-hit component.'),
('d2-fire-sorc','dealt','base_meteor_burn','base','anchored','257-281 fire dmg/sec ground burn at slvl 20','rankedboost.com/diablo-2/sorceress/meteor/ (2026-07-23); kit_numeric meteor_burn_min/max_lvl20','Meteor ground-burn DoT component; burn duration + tick rate = GAP (see below).'),
('d2-fire-sorc','dealt','meteor_burn_duration','modifier','gap_excluded',NULL,'GAP (d2-fire-sorc note: ground burn duration not stated verbatim)','Ground-burn per-cast total needs duration; un-anchored. Excluded + named.'),
('d2-fire-sorc','dealt','fire_mastery_mult','modifier','anchored','+163% at FM slvl 20 (x2.63)','rankedboost.com/diablo-2/sorceress/fire-mastery/ (2026-07-23); kit_numeric firemastery_bonus_pct_lvl20','Applies to both Fire Ball and Meteor (both fire type). Multiplicative.'),
('d2-fire-sorc','dealt','hit_chance','hit_chance','pinned','1.0','PIN-C2','D2 fire-skill hit-chance = 1.'),
('d2-fire-sorc','dealt','crit_ev','crit_ev','pinned','1.0 (no crit)','Pin A / CONDUCTOR PIN #2','No spell crit; non-crit mean.'),
('d2-fire-sorc','dealt','target_fire_resist','mitigation','anchored','target fire_resist_pct (0% Act-1 Normal, inferred)','monster_numeric *.fire_resist_pct (gap_flag=normal_resist_inferred)','Both skills fire; mitigation = target fire resist.');
INSERT INTO kit_composition (kit_id, direction, factor_key, factor_role, status, factor_value, ref, notes) VALUES
('d2-fire-sorc','received','base_mob_damage','base','anchored','mob melee dmg (Act-1 Normal)','monster_numeric d2-*.melee_dmg* (2026-07-23)','Same shared d2 mob set as firewall-sorc.'),
('d2-fire-sorc','received','hit_chance','hit_chance','anchored','min(max(200%*(AR/(AR+Dr))*(ALVL/(ALVL+TLVL)),5%),95%)','maxroll.gg/d2/resources/hit-chance-mechanics (2026-07-23), formulas note C1','Mob AR anchored; sorc Defense = GAP (below).'),
('d2-fire-sorc','received','sorc_defense','hit_chance','gap_excluded',NULL,'GAP (build-point Defense un-anchored)','Dr term un-anchored; hit-chance gap.'),
('d2-fire-sorc','received','crit_ev','crit_ev','pinned','1.0 (mobs)','Pin A / CONDUCTOR PIN #2','No crit-EV term.'),
('d2-fire-sorc','received','sorc_mitigation','mitigation','gap_excluded',NULL,'GAP (build-point resists/armor un-anchored)','Received-% pre-mitigation, says so (charter §9 ladder).');

-- =====================================================================================================
-- poe1-cyclone (3.15 build point, weapon-dependent, physical)
-- =====================================================================================================
-- DEALT: Cyclone deals weapon damage x effectiveness per hit in radius; channel-move. Gauge basis per-hit.
INSERT INTO kit_composition (kit_id, direction, factor_key, factor_role, status, factor_value, ref, notes) VALUES
('poe1-cyclone','dealt','base_weapon_dps','base','gap_excluded',NULL,'PARTIAL/GAP (overgear "650+ dps" target only; no stat-sheet weapon DPS at build point)','Cyclone is weapon-dependent; base = weapon physical DPS x weapon damage range. Exact build-point weapon DPS un-anchored (only a target floor). Excluded + named.'),
('poe1-cyclone','dealt','effectiveness','modifier','anchored','59% effectiveness of added damage at gem 20 (3.15 era)','pathofexile.com/forum/view-thread/3078559 (2026-07-23), CONDUCTOR PIN #1; kit_numeric effectiveness_pct_gem20_bp','THE documented build point (3.15). poedb 150% is context-only, NOT used here.'),
('poe1-cyclone','dealt','attack_speed_mult','modifier','anchored','300% of base attack speed (x3.0)','poedb.tw/us/Cyclone (2026-07-23); kit_numeric attack_speed_pct_of_base','Shapes per-hit cadence, not per-hit magnitude; noted for tempo not join-key denominator (per-hit gauge).'),
('poe1-cyclone','dealt','hit_chance','hit_chance','anchored','poe1 chance-to-hit vs monster evasion (accuracy entropy system)','poecurrency.com/news/path-of-exile-evasion-entropy-system (2026-07-23), formulas note A2; monster_numeric *.evasion_rating','Cyclone is an ATTACK (evasion applies; "Evasion only works against attacks"). Formula expression is image-only (GAP-A2) — see below.'),
('poe1-cyclone','dealt','hit_chance_formula_expr','hit_chance','gap_excluded',NULL,'GAP-A2','poe1 evasion/accuracy chance-to-hit formula EXPRESSION un-anchored (image-only on source). Player accuracy at build point also GAP. Excluded + named; entropy mechanic + evasion-applies rule ARE anchored.'),
('poe1-cyclone','dealt','crit_ev','crit_ev','anchored','~96% crit chance top-gear; crit multi = GAP','poe-vault.com [3.20] (2026-07-23); kit_numeric crit_chance_pct_topgear','Crit-weighted mean (Pin A). Crit chance anchored (top-gear ~96%); crit MULTIPLIER un-anchored (GAP) — crit-EV partial.'),
('poe1-cyclone','dealt','target_armour_dr','mitigation','anchored','ArmourRed = Armour/(Armour + 10*PhysRawDmg), cap 90%','pathofexile.com/forum/view-thread/1468738 (2026-07-23), formulas note A1; monster_numeric *.armour','Cyclone is PHYSICAL; mitigation = target armour DR. Target armour anchored (28,790-35,988 verbatim). THE KFL-7 loud case — now formalized.');
-- RECEIVED: monster attack vs player. Player defensive sheet GAP.
INSERT INTO kit_composition (kit_id, direction, factor_key, factor_role, status, factor_value, ref, notes) VALUES
('poe1-cyclone','received','base_monster_damage','base','anchored','monster Damage (e.g. Goatman 616, range 493-740)','monster_numeric poe1-*.damage / damage_range* (2026-07-23)','Per-hit monster damage, zone-68.'),
('poe1-cyclone','received','hit_chance','hit_chance','anchored','monster accuracy vs player evasion (entropy); evasion vs attacks only','poecurrency.com evasion-entropy (2026-07-23), formulas note A2','Player evasion applies to monster ATTACKS. Player evasion at build point = GAP.'),
('poe1-cyclone','received','player_evasion','hit_chance','gap_excluded',NULL,'GAP (poe1 note: player Armor/Evasion GAP)','Player evasion un-anchored at build point. Hit-chance gap.'),
('poe1-cyclone','received','crit_ev','crit_ev','anchored','monster crit chance 5%','monster_numeric poe1-*.crit_chance_pct (2026-07-23)','Monster base crit 5% anchored; monster crit multi not separately anchored (default assumed by engine, not curated).'),
('poe1-cyclone','received','player_mitigation','mitigation','gap_excluded',NULL,'GAP (poe1 note: player armor/evasion/resist exact = GAP; only 75% resist cap)','Player mitigation sheet un-anchored (only resist cap target). Received-% pre-mitigation, says so (charter §9).');

-- =====================================================================================================
-- poe2-bonestorm (physical spell, projectile + explosion, channel)
-- =====================================================================================================
-- DEALT: two components per shard. N_shards=10 pinned. projectile=evadable; explosion=AoE-exempt (PIN #6). Gauge per-hit.
INSERT INTO kit_composition (kit_id, direction, factor_key, factor_role, status, factor_value, ref, notes) VALUES
('poe2-bonestorm','dealt','base_projectile','base','anchored','116-175 physical at gem 20 (projectile)','poe2db.tw/us/Bonestorm (2026-07-23); kit_numeric bonestorm_proj_min/max_gem20','Physical spell damage (not weapon-dependent). Projectile component.'),
('poe2-bonestorm','dealt','base_explosion','base','anchored','89-134 physical at gem 20 (explosion)','poe2db.tw/us/Bonestorm (2026-07-23); kit_numeric bonestorm_expl_min/max_gem20','Explosion component; AoE-exempt from evasion (PIN #6).'),
('poe2-bonestorm','dealt','n_shards','modifier','pinned','10 (max 20)','PIN-N10 / CONDUCTOR PIN #5; kit_numeric n_shards_expected_pin','Expected-per-release = N_shards x (proj + explosion). Documented-build midpoint.'),
('poe2-bonestorm','dealt','hit_chance_projectile','hit_chance','anchored','projectile EVADABLE (monster accuracy vs player evasion in reverse; here vs monster evasion)','poecurrency.com poe2 evasion (2026-07-23), formulas note B2; monster_numeric poe2 evasion','PIN #6: Bonestorm projectile IS evadable (LOAD-BEARING correction to spells-always-hit). vs poe2 monster evasion (formula-level).'),
('poe2-bonestorm','dealt','hit_chance_explosion','hit_chance','anchored','explosion AoE-EXEMPT (cannot be evaded)','poecurrency.com poe2 evasion (2026-07-23), formulas note B2','PIN #6: explosion (AoE) exempt; hit_chance = 1 for the explosion component.'),
('poe2-bonestorm','dealt','crit_ev','crit_ev','anchored','base crit 15%; crit multi = GAP','poe2db.tw/us/Bonestorm (2026-07-23); kit_numeric crit_chance_pct_base','Crit-weighted mean (Pin A). Base 15% anchored; total crit chance + multi with gear/passives = GAP -> crit-EV partial.'),
('poe2-bonestorm','dealt','target_armour','mitigation','gap_excluded',NULL,'GAP-B1 / CONDUCTOR PIN #6','poe2 armour damage-reduction formula un-anchored (sources blocked). Dealt-% renders PRE-ARMOUR, named (charter §9).');
INSERT INTO kit_composition (kit_id, direction, factor_key, factor_role, status, factor_value, ref, notes) VALUES
('poe2-bonestorm','received','base_monster_damage','base','anchored','levelscale[monster_level] x creature_mult','monster_numeric poe2-levelscale-* / creature-mult (2026-07-23)','Formula-level anchor (per-named mob GAP). base = level-scale damage x creature multiplier.'),
('poe2-bonestorm','received','monster_damage_permob','base','gap_excluded',NULL,'GAP (poe2 note: per-named Act-1 mob stats FULL GAP, SPA-blocked)','Per-named-mob verbatim un-fetchable; formula-level composition only. Excluded + named; next-lap admission.'),
('poe2-bonestorm','received','hit_chance','hit_chance','anchored','monster accuracy vs player evasion (poe2 evade any projectile/strike)','poecurrency.com poe2 evasion (2026-07-23), formulas note B2; monster_numeric accuracy','Player evasion applies vs monster attacks AND spell projectiles in poe2. Player evasion at build point = GAP.'),
('poe2-bonestorm','received','player_evasion','hit_chance','gap_excluded',NULL,'GAP (poe2 note: player Armor/Evasion GAP)','Player evasion un-anchored. Hit-chance gap.'),
('poe2-bonestorm','received','crit_ev','crit_ev','gap_excluded',NULL,'GAP (poe2 monster crit not anchored at level-scale)','Monster crit-EV not anchored for level-scale rows. Excluded + named.'),
('poe2-bonestorm','received','player_mitigation','mitigation','gap_excluded',NULL,'GAP (poe2 note: player ES/armor/resist = GAP) + GAP-B1 armour formula','Player mitigation sheet + armour formula un-anchored. Received-% pre-mitigation, says so (charter §9).');

-- =====================================================================================================
-- gd-flames-of-ignaffar-purifier (KIT HELD; FoI rank table GAP; monster side FULL GAP)
-- =====================================================================================================
-- DEALT: FoI channeled fire+burn cone, tick every 0.3s. Rank-table damage = GAP (kit HELD). Character formulas anchored.
INSERT INTO kit_composition (kit_id, direction, factor_key, factor_role, status, factor_value, ref, notes) VALUES
('gd-flames-of-ignaffar-purifier','dealt','base_foi_damage','base','gap_excluded',NULL,'GAP-D1 / CONDUCTOR PIN #8 (kit HELD)','FoI per-rank fire/burn damage table = FULL GAP (grimtools JS-rendered, fandom 402). KIT HELD; base un-anchorable. Matt fork queued (KFL-8c). Excluded + named; NEVER estimated.'),
('gd-flames-of-ignaffar-purifier','dealt','tick_interval','modifier','anchored','every 0.3 sec at 100% cast speed','steamcommunity.com/app/219990/discussions/0/1620599015872291805/ (2026-07-23); kit_numeric foi_tick_interval_sec','Channel tick cadence anchored (structural), though per-tick DAMAGE is GAP. Gauge basis per-tick.'),
('gd-flames-of-ignaffar-purifier','dealt','hit_chance','hit_chance','anchored','PTH = ((((OA/((DA/3.5)+OA))*300)*0.3)+(((((OA*3.25)+10000)-(DA*3.25))/100)*0.7))-50; floor 55','grimdawn.com/guide/gameplay/combat/ (2026-07-23); kit_numeric pth_floor','GD PTH formula ANCHORED verbatim (formula expression carried here as ref; scalar floor=55 in kit_numeric). Build-point OA/DA totals = GAP.'),
('gd-flames-of-ignaffar-purifier','dealt','oa_at_buildpoint','hit_chance','gap_excluded',NULL,'GAP (gd note: OA/DA totals at build point un-anchored; formula anchored, inputs not)','OA = (115+12*Level+0.4*Cunning+bonuses)*(1+%OA/100); formula anchored, but Cunning total + gear bonuses + level = GAP. Excluded + named.'),
('gd-flames-of-ignaffar-purifier','dealt','crit_ev','crit_ev','anchored','crit chance = PTH-90; crit multi tiers 1.0-1.5x (official)','grimdawn.com/guide/gameplay/combat/ (2026-07-23); kit_numeric crit_mult_pth*','Crit-weighted mean (Pin A). Crit-chance formula + tier table ANCHORED (Source E official, 1.5x max). PTH inputs GAP so realized crit-EV partial.'),
('gd-flames-of-ignaffar-purifier','dealt','target_resist','mitigation','gap_excluded',NULL,'GAP-D2 (gd monster side FULL GAP)','FoI is fire+burn; target fire resist = mitigation. GD Act-1 monster resists FULL GAP (grimtools JS-rendered, fandom 402). Excluded + named.');
-- RECEIVED: gd monster attacks vs Purifier. Monster side FULL GAP; Purifier armor-absorption anchored (70% default).
INSERT INTO kit_composition (kit_id, direction, factor_key, factor_role, status, factor_value, ref, notes) VALUES
('gd-flames-of-ignaffar-purifier','received','base_monster_damage','base','gap_excluded',NULL,'GAP-D2','GD Act-1 Normal mob damage = FULL GAP (all monster fields un-anchorable). Excluded + named; monster harvest = FULL GAP, Matt fork queued.'),
('gd-flames-of-ignaffar-purifier','received','hit_chance','hit_chance','anchored','GD PTH formula (mob OA vs Purifier DA); floor 55','grimdawn.com/guide/gameplay/combat/ (2026-07-23)','PTH formula anchored (symmetric); mob OA = GAP (monster side), Purifier DA = GAP (build point). Formula anchored, inputs gap.'),
('gd-flames-of-ignaffar-purifier','received','purifier_da','hit_chance','gap_excluded',NULL,'GAP (build-point DA un-anchored)','DA = (115+12*Level+0.4*Spirit+bonuses)*(1+%DA/100); Spirit=0 invested anchored but level+gear+flat-Physique-DA totals GAP.'),
('gd-flames-of-ignaffar-purifier','received','crit_ev','crit_ev','gap_excluded',NULL,'GAP-D2 (mob OA un-anchored)','Mob crit via PTH needs mob OA = GAP. Excluded + named.'),
('gd-flames-of-ignaffar-purifier','received','armor_absorption','mitigation','anchored','70% default armor absorption; 30% always through','grimdawn.com/guide/gameplay/combat/ (2026-07-23); kit_numeric armor_absorption_default_pct','Armor absorption 70% ANCHORED (default). Actual armor RATING at build point = GAP (partial mitigation anchor).');
