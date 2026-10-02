import json, collections
exec(open('analyse.py').read().split("frames=[]")[0])
raw=json.load(open('lineup_raw.json'))
def legal(w,rec):
    pts=[]
    for sp,alts in P[str(w)].items():
        for a in alts:
            if rec in a['recs'] or rec in a['crecs']: pts.append(sp)
    return sorted(set(pts))
HOV=[(151,685.8,'Ancient Wraith',104),(151,687.8,'Tildoom ~ Timewarped',108),(151,689.3,'Arcanom the Soulthief',108),(151,690.9,'Wraith',104),
(151,692.1,'Carnivorous Plant',103),(151,696.5,'Carnivorous Plant',104),
(152,703.5,'Chillslither ~ Arctic',107),(152,704.6,'Rotmouth',107),(152,706.6,'Fleshweaver Haraxis',108),(152,707.3,'Juvenile Basilisk',102),(152,710.0,'Venomgaze Basilisk',103),
(153,719.1,'Wendigo',104),(153,721.9,'Frost Revenant',104),(153,722.9,'Skeletal Archer',105),(153,728.2,'Chthonian Unraveler',108),
(154,733.0,'Kubacabra, the Endless Menace',109),(154,733.7,'Father Kymon, Avatar of Korvaak',108),(154,734.9,'Ugdenbog Turned',104),(154,742.0,"Gabal'Thunn, the Visage of Madness",108),
(155,748.1,'Fleshwarped Aberration',103),(155,750.3,'Allostria, the Mindthief',108),(155,751.7,'Eldritch Spirit',103),(155,752.2,'Eldritch Spirit ~ Haunt',105),(155,753.5,'Eldritch Spirit ~ Ancient',105),
(156,762.6,'Animated Keeper',104),(156,763.3,'Animated Watcher',104),(156,765.2,'Fleshwarped Chilled One',104),(156,767.5,'Animated Watcher',105),(156,769.9,'Fleshwarped Chilled One',103),(156,778.9,'Janaxia, the Betrayer',107),
(157,783.2,'Diremane Brute',103),(157,786.2,'Starhorn ~ Celestial',107),(157,787.8,'Blugrug the Living Plague',108),(157,789.0,'Chthonian Bloodkeeper',106),(157,793.0,"Arum'Zoth ~ Burning",108),(157,796.1,'Phigillius Stormbile',108),(157,797.6,'Chthonian Servitor',104),
(158,801.8,'Chthonian Gorger',104),(158,803.8,'Ugdenbog Crab',104),(158,805.0,'Sandclaw ~ Flayer',104),(158,807.4,'Sandclaw',103),(158,808.1,'Everon ~ Burning',107),(158,810.3,'Flamegore ~ Burning',108),
(159,815.6,'Margul the Rotting',107),(159,819.3,'The Sentinel',107),(159,831.5,"Ekket'Zul, Progenitor of Darkness",107),(159,833.5,'Venarius, the Backbreaker',106),
(160,842.0,'Galakros, the Mountain',106),(160,847.0,'Archmage Aleksander',109),(160,852.0,'Kubacabra, the Endless Menace',109),(160,861.6,"Aleksander's Shard",109),(160,863.2,'Death Revenant',109),(160,864.3,'Zantarin, the Immortal',109)]
REV=collections.defaultdict(set)
for r,n in NAME.items(): REV[n].add(r)
# also scan all pools display names
fpd={(rec,L,w):e for rec,L,w,e in fp}
seen={w:{r['max']:r['n'] for r in raw[str(w)]} for w in range(151,161)}
out=[]
for w,t,nm,L in HOV:
    recs=sorted(REV.get(nm,[]))
    hits=[]
    for rec in recs:
        e=fpd.get((rec,L,w))
        if e is None: hits.append((rec.split('/')[-1],None,'no-level-row',legal(w,rec))); continue
        n=max(seen[w].get(e,0),seen[w].get(e+1,0),seen[w].get(e-1,0))
        hits.append((rec.split('/')[-1],e,n,legal(w,rec)))
    out.append(dict(wave=w,t=t,name=nm,level=L,records=hits))
    print(w,t,nm,L,hits)
json.dump(out,open('hover_bind.json','w'),indent=1)
