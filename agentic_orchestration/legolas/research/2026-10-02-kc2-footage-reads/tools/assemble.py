"""Assemble referent_lineup_by_wave.csv from the fingerprint census + hover-name binds.
Each row = one identity. keys = the max-HP fingerprints (one per level) that carry it."""
import json, csv, collections
M=json.load(open('lineup_matched.json')); B=json.load(open('bodies.json'))
S9=json.load(open('seed9.json'))
def fp(w,mx): 
    for r in M[str(w)]:
        if r['max']==mx: return r
    raise KeyError((w,mx))
# (wave, keys, point, record(s), display, summoned_by, identification basis, confidence, label, note)
R=[
(151,[136975,139400],'p01/p04','wraith_a01','Wraith','', 'HP-exact unique pool-legal; name read 690.9 (L104)','HIGH','FOOTAGE+DATAMINED',''),
(151,[221351,225874,230020],'p01/p04','wraith_b01','Spiteful Wraith','', 'HP-exact unique pool-legal (L104/105/106)','HIGH','FOOTAGE+DATAMINED','three levels = at least three bodies'),
(151,[373665,381272],'p01/p04','wraith_c01','Ancient Wraith','', 'HP-exact; name read 685.8/686.9 (L104)','HIGH','FOOTAGE+DATAMINED',''),
(151,[453064],'p02','wraith_h03 + wraith_h01','Tildoom ~ Timewarped + Arcanom the Soulthief','', 'both names read (L108) and both carry 453,064; 2 simultaneous','HIGH','FOOTAGE+DATAMINED','p02 rolled the WRAITH-hero alternative (seed 9: wendigo heroes)'),
(151,[442747],'p02 or p03','one of wraith_h02/h04/h05 or swampgolem_h02','(hero, L107)','', 'HP class shared by 6 pool-legal heroes; not named','LOW','FOOTAGE+DATAMINED+INFERRED','a third p02 wraith hero, or a p03 golem hero'),
(151,[569330,582590],'p03','swampgolem_h01/h03/h04/h05 (one or two)','Ugdenbog golem hero (L107, L108)','', 'HP class (golem heroes or wendigo heroes); p02 is taken by the wraith-hero alternative, so the golem-hero alternative at p03; plant summons (below) need a golem-hero owner','MEDIUM','FOOTAGE+DATAMINED+INFERRED','same alternative as seed 9 (swampgolem_h01/h02/h05)'),
(151,[272948,278543],'p05','livingplant_a01','Carnivorous Plant','', 'HP-exact unique; name read 692.1 (L103), 696.5/697.5 (L104)','HIGH','FOOTAGE+DATAMINED','no swampgolem_a01 fingerprint in w151 (seed 9 has 2 golems at p05)'),
(151,[295984,302387],'(summon)','livingplant_a01_summon','Carnivorous Plant (summoned)','swampgolem_h0x', 'HP-exact unique summon record (L107/L108)','HIGH','FOOTAGE+DATAMINED','summoned, not a pool body'),
(152,[443554,453883],'p02 + p01 + p05','basilisk_h05 + basilisk_h02 named; rest crab heroes (p01) and aetherialcorruption heroes (p05)','Chillslither ~ Arctic, Rotmouth (+ unnamed heroes)','', 'hero HP class L107/L108; two names read (L107); galadriel read Vanallius the Voracious (aetherialcorruption_h02) at p05 (KP-203)','MEDIUM','FOOTAGE+DATAMINED+INFERRED','class cannot separate p01/p02/p05 heroes; crabling summons prove crab heroes at p01'),
(152,[91696,93599],'p03','basilisk_a01','Juvenile Basilisk','', 'HP-exact; name read 707.3 (L102)','HIGH','FOOTAGE+DATAMINED','p03 rolled BASILISK trash (seed 9: thornedhorrorfrost trash)'),
(152,[237258,242124],'p03','basilisk_b01','Venomgaze Basilisk','', 'HP-exact; name read 710.0 (L103)','HIGH','FOOTAGE+DATAMINED',''),
(152,[369770],'p03','basilisk_c01','Stonegaze Basilisk','', 'HP-exact unique pool-legal (L106)','HIGH','FOOTAGE+DATAMINED',''),
(152,[2050807],'p04','aetherialfleshshaper_haraxis','Fleshweaver Haraxis','', 'name read 706.6 (L108, boss) + HP-exact','HIGH','FOOTAGE+DATAMINED','seed 9: Carraxus (swampcrab_ugdenbog_01)'),
(152,[472732],'(summon)','aetherialcorruption_c01_summon','Fleshwarped Aberration (summoned)','aetherialfleshshaper_haraxis', 'HP-exact unique summon (L108)','HIGH','FOOTAGE+DATAMINED',''),
(152,[42798,43548],'(summon)','swampcrab_a00_summon or springscrab_a00_summon','Ugdenbog / Calcified Crabling (summoned)','p01 crab hero', 'HP-exact; the two crabling records share HP','MEDIUM','FOOTAGE+DATAMINED','species (and so the p01 crab-hero alternative) unresolved'),
(153,[203039,207203],'p01','wendigo_a01','Wendigo','', 'HP-exact; name read 719.1 (L104)','HIGH','FOOTAGE+DATAMINED','same p01 alternative as seed 9 (wendigo_t3)'),
(153,[297609,303657],'p01','wendigo_b01 or wendigo_b02','Wendigo ~ Flayer / ~ Marroweater','', 'HP-exact, two sibling records share HP','MEDIUM','FOOTAGE+DATAMINED',''),
(153,[476173],'p01','wendigo_c01','Wendigo ~ Ancient','', 'HP-exact unique pool-legal (L106)','HIGH','FOOTAGE+DATAMINED',''),
(153,[260786,266082,271687],'p03','skeleton_c01/c02/c03 (Frost Revenant named)','Flame/Frost/Storm Revenant','', 'HP-exact class of 3 siblings; Frost Revenant read 721.9 (L104)','MEDIUM','FOOTAGE+DATAMINED','p03 rolled the REVENANT alternative (seed 9: giants)'),
(153,[425285],'p03','skeleton_d01','Death Revenant','', 'HP-exact unique (L105)','HIGH','FOOTAGE+DATAMINED',''),
(153,[37840],'(summon)','skeleton_a02_summon (+ possibly skeleton_a01_summon)','Skeletal Archer (summoned)','skeleton_d01 / odv_bounty13', 'HP-exact; Skeletal Archer read 722.9 (L105); warrior shares HP','HIGH','FOOTAGE+DATAMINED',''),
(153,[273975],'p05','livingplant_a01','Carnivorous Plant','', 'HP-exact unique (L103)','HIGH','FOOTAGE+DATAMINED',''),
(153,[417957,427128],'p05','swampgolem_a01','Ugdenbog Golem','', 'HP-exact unique pool-legal (L104/L105)','HIGH','FOOTAGE+DATAMINED',''),
(153,[584695],'p02 or p04','kc_bounty13','Chthonian Unraveler','', 'name read 728.2/729.5 (L108) + HP class','HIGH','FOOTAGE+DATAMINED',''),
(153,[275518],'p02 or p04','dc_bounty08 or ku_bounty_06','Slathra, the Plagued / Holvir the Crimson Blade','', 'HP-exact, 2 pool-legal records','MEDIUM','FOOTAGE+DATAMINED',''),
(153,[638564],'p02/p04 (or p06)','kc_bounty09 or ro_bounty12 (or chthonianfiend_h01 at p06)',"Vom'Zul / Mortallis ~ Charger",'', 'HP-exact, 3 legal records','MEDIUM','FOOTAGE+DATAMINED',''),
(153,[444361],'p02 or p04','bounty hero (L107 class)','(bounty hero)','', 'HP class shared by ~33 bounty records','LOW','FOOTAGE+DATAMINED',''),
(153,[447994],'?','UNKNOWN','UNKNOWN','', 'no record reproduces 447,994; nearest dc_bounty17 L107 448,801 (-0.18%)','UNKNOWN','FOOTAGE','6 readings only'),
(154,[2373673],'p01','fatherkymon','Father Kymon, Avatar of Korvaak','', 'name read 733.7 (L108) + HP-exact','HIGH','FOOTAGE+DATAMINED','seed 9: Bloodlord (cultist_cultleader_01)'),
(154,[2058204],'p02','chthonianrylok_gabalthunn',"Gabal'Thunn, the Visage of Madness",'', 'name read 742.0/743.0 (L108) + HP class','HIGH','FOOTAGE+DATAMINED','same as seed 9'),
(154,[2924379],'p03','nemesis_beast_01_p1','Kubacabra, the Endless Menace','', 'name read 733.0-738.8 (L109) + HP-exact unique','HIGH','FOOTAGE+DATAMINED','same as seed 9'),
(154,[92151,94059],'p04','wendigocannibal_a01','Ugdenbog Wretch','', 'HP-exact unique (L102/L103)','HIGH','FOOTAGE+DATAMINED','p04 rolled WENDIGOCANNIBAL trash (seed 9: eldritcharmor fire trash)'),
(154,[202027,205597],'p04','wendigocannibal_b01','Ugdenbog Turned','', 'HP-exact; name read 734.9 (L104)','HIGH','FOOTAGE+DATAMINED',''),
(155,[1476963],'p01 + p02','aetherialcorruption_intro + humanascendant_mindthief_01','Dralgar + Allostria, the Mindthief','', 'two simultaneous bodies of one HP class; Allostria read 750.3 (L108)','HIGH','FOOTAGE+DATAMINED','same as seed 9'),
(155,[138013,140452],'p03 or p04','eldritchwraith_a01','Eldritch Spirit','', 'HP-exact; name read 751.7 (L103)','HIGH','FOOTAGE+DATAMINED','one ring point rolled ELDRITCHWRAITH (seed 9: imps at p03)'),
(155,[227566],'p03 or p04','eldritchwraith_b01','Eldritch Spirit ~ Haunt','', 'HP-exact; name read 752.2 (L105)','HIGH','FOOTAGE+DATAMINED',''),
(155,[384096],'p03 or p04','eldritchwraith_c01','Eldritch Spirit ~ Ancient','', 'HP-exact; name read 753.5 (L105)','HIGH','FOOTAGE+DATAMINED',''),
(155,[429073,437859],'p03 or p04','aetherialcorruption_c01','Fleshwarped Aberration','', 'HP-exact; name read 748.1/749.1 (L103)','HIGH','FOOTAGE+DATAMINED','same pool as seed 9 p04'),
(155,[2061902],'?','UNKNOWN (boss-class L108)','UNKNOWN','', "boss HP class; the only w155-legal member is Ishtal (p02), which cannot co-roll with Allostria at p02",'UNKNOWN','FOOTAGE+DATAMINED','8 readings in 759.3-760.0, at the wave seam'),
(156,[2022317],'p01','witch_janaxia','Janaxia, the Betrayer','', 'name read 778.9 (L107); the HP is NOT reproduced by the Lap D model (2,018,819, -0.17%)','HIGH','FOOTAGE (+DATAMINED residual)','HP residual routed'),
(156,[2065601],'p02 + p03','(basilisk_witchritual or direwolf_frozenwastes_01) + witch_larria','Stone Basilisk / Siff Icehowl + Larria, the Hexxer','', '2 simultaneous bodies of the L108 boss class whose legal members are p02 (2) and p03 Larria; Janaxia is bound separately','MEDIUM','FOOTAGE+DATAMINED+INFERRED','p03 = Larria, not the Kurn shaman (seed 9: shaman, chaosorb 24 % of seed-9 w156 damage)'),
(156,[1976276],'?','UNKNOWN 4th boss-class body (L106)','UNKNOWN','', 'same boss HP class at L106; all three boss points are already accounted for','UNKNOWN','FOOTAGE+DATAMINED','summoned clone or mis-assigned level; not resolved'),
(156,[274977,280601],'p05','aetherialcorruption_b01','Fleshwarped Chilled One','', 'HP class of 3 element siblings; name read 765.2/766.2 (L104) and 769.9 (L103)','HIGH','FOOTAGE+DATAMINED','same pool as seed 9 (ice)'),
(156,[425124,426076],'p04','statue_a01 or statue_a02','Animated Keeper','', 'name read 762.6 (L104); HP not reproduced by the model (420,287; residual about +1.1%)','MEDIUM','FOOTAGE','p04 rolled STATUES (seed 9: chthonian heralds, 29 % of seed-9 w156 damage)'),
(156,[710131,722616],'p04','statue_b01 or statue_b02','Animated Watcher','', 'name read 763.3 (L104), 767.5/769.0 (L105); HP not reproduced (702,448 / 717,842)','MEDIUM','FOOTAGE',''),
(156,[236810],'(summon)','wraith_b01_summon','Spiteful Wraith (summoned)','witch_janaxia', 'HP-exact unique summon (L107)','HIGH','FOOTAGE+DATAMINED',''),
(156,[444150],'?','UNKNOWN','UNKNOWN','', 'nearest aetherialbloater_b01_summon L107 445,209 (-0.24%)','UNKNOWN','FOOTAGE','6 readings'),
(157,[2069299],'p01','aetherialbloater_malmouthdocks_01','Blugrug the Living Plague','', 'name read 787.8/792.0 (L108) + HP class','HIGH','FOOTAGE+DATAMINED','same as seed 9'),
(157,[447590],'p02','rhino_h02','Starhorn ~ Celestial','', 'name read 786.2/787.1 (L107); 2 simultaneous bodies of this class','HIGH','FOOTAGE+DATAMINED','same alternative as seed 9 (devotion_heroes01 #2), different heroes'),
(157,[588905],'p02','chthonianherald_h02',"Arum'Zoth ~ Burning",'', 'name read 793.0/795.0 (L108)','HIGH','FOOTAGE+DATAMINED','seed 9: chthonianherald_h01, rhino_h04, rhino_h01'),
(157,[398226,414837],'p03','chthonianservitor_b01','Chthonian Servitor','', 'HP-exact unique; name read 797.6/798.6 (L104)','HIGH','FOOTAGE+DATAMINED','p03 rolled SERVITORS (seed 9: chthonian leeches)'),
(157,[406243],'p03','chthonianservitor_b02','Chthonian Harvester','', 'HP-exact unique (L105)','HIGH','FOOTAGE+DATAMINED',''),
(157,[547007],'p03','chthonianservitor_c01','Chthonian Bloodkeeper','', 'name read 789.0 (L106) + HP-exact','HIGH','FOOTAGE+DATAMINED',''),
(157,[226525],'p03','chthonianservitor_a01','Chthonian Drone','', 'HP-exact unique (L104)','HIGH','FOOTAGE+DATAMINED',''),
(157,[233250,238068],'p04','yetidire_a01','Diremane Brute','', 'HP-exact; name read 783.2/784.3 (L103)','HIGH','FOOTAGE+DATAMINED','p04 rolled DIREMANE trash (seed 9: skeletal golems + revenants)'),
(157,[411440,419839],'p04','yetidire_b01 or yetidire_b02','Diremane Rager / Icebreaker','', 'HP-exact siblings (419,839 also fits aetherialbloater_b01 L104)','MEDIUM','FOOTAGE+DATAMINED',''),
(157,[504193],'p04','yetidire_c01 (or aetherialbloater_c01)','Diremane Alpha','', 'HP-exact, 2 legal records; yetidire alternative favoured','MEDIUM','FOOTAGE+DATAMINED+INFERRED',''),
(157,[457975],'p05','aetherialimp_h01 + 2 more imp heroes','Phigillius Stormbile (+2)','', 'name read 796.1 (L108); 3 simultaneous bodies of the class','HIGH (Phigillius) / MEDIUM (the other two)','FOOTAGE+DATAMINED+INFERRED','p05 rolled the IMP-hero pool (seed 9: corruption heroes)'),
(157,[304994],'(summon)','aetherialworm_b0x_summon','Aetherial worm (summoned)','aetherialbloater_malmouthdocks_01', 'HP-exact, 4 sibling summon records','HIGH','FOOTAGE+DATAMINED',''),
(158,[199111,203230],'p01','sandlizard_a01','Sandclaw','', 'name read 807.4 (L103); plain Sandclaw is legal only at p01','HIGH','FOOTAGE+DATAMINED','p01 rolled SANDLIZARD (seed 9: devourers)'),
(158,[294361,300375],'p01','sandlizard_b01','Sandclaw ~ Flayer','', 'name read 805.0 (L104)','HIGH','FOOTAGE+DATAMINED',''),
(158,[480530],'p01','sandlizard_c01','Sandclaw ~ Matriarch','', 'HP class of 3 element siblings; p01 plain alternative favoured','MEDIUM','FOOTAGE+DATAMINED+INFERRED',''),
(158,[448397],'p02 + p05','skeleton_h04 named (+2 heroes)','Everon ~ Burning (+2)','', 'name read 808.1 (L107); 3 simultaneous bodies of the class (p02 heroes and p05 wraith/hypporaven heroes share it)','HIGH (Everon) / LOW (others)','FOOTAGE+DATAMINED',''),
(158,[589958],'p02','skeletalgolem_h03','Flamegore ~ Burning','', 'name read 810.3/811.7 (L108)','HIGH','FOOTAGE+DATAMINED','same alternative as seed 9 (devotion_heroes04), different heroes; seed 9 had skeleton_h08/h09 (66 % of seed-9 w158 damage)'),
(158,[39311],'p03 or p04','chthoniandevourer_a01','Chthonian Hungerer','', 'HP-exact unique (L102)','HIGH','FOOTAGE+DATAMINED',''),
(158,[98986,100948],'p03 or p04','chthoniandevourer_b01 / b02','Chthonian Devourer / Gorger','', 'HP siblings; Chthonian Gorger read 801.8 (L104)','MEDIUM','FOOTAGE+DATAMINED',''),
(158,[94715,96385],'p03 or p04','swampcrab_a01','Ugdenbog Crab','', 'name read 803.8 (L104) + HP-exact','HIGH','FOOTAGE+DATAMINED',''),
(158,[171897],'p03 or p04','swampcrab_b01','Ugdenbog Spikeshell','', 'HP-exact unique pool-legal (L103)','HIGH','FOOTAGE+DATAMINED',''),
(158,[293482],'p03 or p04','swampcrab_c01','Ugdenbog Stoneshell','', 'HP-exact unique pool-legal (L106)','HIGH','FOOTAGE+DATAMINED',''),
(158,[42446],'(summon)','swampcrab_a00_summon','Ugdenbog Crabling (summoned)','swampcrab_c01', 'HP-exact (L106)','HIGH','FOOTAGE+DATAMINED',''),
(159,[2029761],'p04 (+ p01?)','beetle_maggot01 (+ chthonianservitor_lunalvalgoth?)','Margul the Rotting (+ Lunal\'Valgoth?)','', 'Margul read 815.6-821.0 (L107); Lunal\'Valgoth shares the class and his Drone summons are present','HIGH (Margul) / MEDIUM (Lunal\'Valgoth)','FOOTAGE+DATAMINED+INFERRED','seed 9 p04: Rimehorn'),
(159,[1599856],'p02','aetherial_fleshhulk_mine','Venarius, the Backbreaker','', 'name read 833.5 (L106) + HP-exact unique','HIGH','FOOTAGE+DATAMINED','seed 9 p02: Avinnia (rokwind_01)'),
(159,[2025309],'p03','witchgod_finalboss','The Sentinel','', 'name read 819.3/829.7/838.3 (L107) + HP-exact','HIGH','FOOTAGE+DATAMINED','same as seed 9'),
(159,[2340860],'p05','chthonianrylok_ekketzul',"Ekket'Zul, Progenitor of Darkness",'', 'name read 831.5 (L107) + HP class','HIGH','FOOTAGE+DATAMINED','seed 9 p05: Okaloth (korvaakmessenger_02b)'),
(159,[102327],'(summon)','beetle_maggot01_maggotsummon','Korvan Maggot (summoned)','beetle_maggot01', 'HP-exact unique (L107)','HIGH','FOOTAGE+DATAMINED',''),
(159,[241531],'(summon)','chthonianservitor_a01_summon','Chthonian Drone (summoned)','chthonianservitor_lunalvalgoth', 'HP-exact unique (L107)','HIGH','FOOTAGE+DATAMINED','implies Lunal\'Valgoth at p01'),
(159,[403232],'(summon)','hellhound_witchgod_b01_summon','(hellhound, summoned)','owner not in the roster packet; The Sentinel INFERRED', 'HP-exact unique (L107)','MEDIUM','FOOTAGE+DATAMINED+INFERRED',''),
(160,[3722896],'p01 + p03','nemesis_orderdeathsvigil_01 + nemesis_aetherialvanguard_01','Zantarin, the Immortal + Archmage Aleksander','', 'both names read (L109); exactly 2 simultaneous bodies (galadriel 73 frames)','HIGH','FOOTAGE+DATAMINED','seed 9 p01: Kymon nemesis'),
(160,[2955796],'p02','nemesis_beast_01_p1','Kubacabra, the Endless Menace','', 'name read + HP-exact unique (L109)','HIGH','FOOTAGE+DATAMINED','seed 9 p02: nemesis_wendigo_01'),
(160,[2295755],'p04','aetherialcolossus_galakros','Galakros, the Mountain','', 'name read (L106) + HP','HIGH','FOOTAGE+DATAMINED','seed 9 p04: The Steward'),
(160,[103912],'(summon)','aetherialvanguard_crystal',"Aleksander's Shard (summoned)",'nemesis_aetherialvanguard_01', 'name read 861.6 (L109) + HP','HIGH','FOOTAGE+DATAMINED',''),
(160,[468504],'(summon)','nemesis_orderdeathsvigil_01_revenantsummon','Death Revenant (summoned)','nemesis_orderdeathsvigil_01', 'name read 863.2 + HP-exact unique','HIGH','FOOTAGE+DATAMINED',''),
(160,[41237],'(summon)','skeleton_a02_summon','Skeletal Archer (summoned)','nemesis_orderdeathsvigil_01', 'HP-exact (L109); name read by galadriel 862.8','HIGH','FOOTAGE+DATAMINED',''),
(160,[484095],'(summon?)','UNKNOWN (galadriel: probable Aetherial Bileeater, L112)','Aetherial Bileeater (probable)','aetherialcolossus_galakros (INFERRED)', 'no level row at L112 in the life table','LOW','FOOTAGE',''),
]
rows=[]
for w,keys,pt,rec,disp,owner,basis,conf,lab,note in R:
    rs=[fp(w,k) for k in keys]
    levels=sorted({x[1] for r in rs for x in r['legal']+r['summon'] if x[0].replace('.dbr','') in rec} ) or sorted({x[1] for r in rs for x in r['legal']+r['summon']})
    s9=collections.Counter()
    for sp,v in S9[str(w)].items():
        for r_ in v: s9[r_.split('/')[-1].replace('.dbr','')]+=1
    s9n=sum(c for k,c in s9.items() if k in rec.replace('(','').replace(')','').replace('+',' ').replace('/',' ').replace(',',' ').split())
    rows.append(dict(wave=w,spawn_point=pt,record=rec,display_name=disp,summoned_by=owner,
        max_hp_fingerprints=' '.join(f'{k:,}'.replace(',','_') for k in keys),levels=' '.join(map(str,levels)),
        n_readouts=sum(r['n'] for r in rs),count_min=sum(r['simul'] for r in rs),
        count_tracker_upper=sum(B[str(w)].get(str(k),{}).get('tracks2',0) for k in keys),
        first_s=min(r['first'] for r in rs),last_s=max(r['last'] for r in rs),
        seed9_count=s9n,identification=basis,confidence=conf,label=lab,note=note))
with open('referent_lineup_by_wave.csv','w',newline='') as f:
    w_=csv.DictWriter(f,fieldnames=list(rows[0].keys())); w_.writeheader(); w_.writerows(rows)
print(len(rows))
# per-wave summary
for w in range(151,161):
    rr=[r for r in rows if r['wave']==w]
    pool=sum(r['count_min'] for r in rr if not r['spawn_point'].startswith('(summon'))
    summ=sum(r['count_min'] for r in rr if r['spawn_point'].startswith('(summon'))
    s9tot=sum(len(v) for v in S9[str(w)].values())
    print(w,'pool bodies >=',pool,'summoned >=',summ,'seed9 bodies',s9tot)
