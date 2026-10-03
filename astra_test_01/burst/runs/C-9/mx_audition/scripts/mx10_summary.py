# MX audition (R-C9-149): the SUMMARY -- one recommendation per body with the measurements behind it -- as summary.json
# (committed) and sheets/mx_audition_summary.png (a table sheet). Reads work/meas_<tag>.json (mx03 + mx09) and work/lint_<tag>.json
# (nb_join j_joint_lint, ref = the body's own hit of record). Nothing here touches a kit, manifest or pack root.
#   python3 scripts/mx10_summary.py
import json, os
from PIL import Image, ImageDraw, ImageFont
B = {'fleshhulk': 'en-fleshhulk', 'colossus': 'en-colossus', 'revenant': 'en-revenant', 'wretch': 'en-wretch', 'golem': 'en-golem'}
S = {t: json.load(open('specs/%s.json' % t)) for t in ['fleshhulk', 'colossus', 'revenant', 'wretch', 'revenant_em', 'golem_em']}
M = {t: json.load(open('work/meas_%s.json' % t))['clips'] for t in B}
LT = {t: json.load(open('work/lint_%s.json' % t))['moves'] for t in B}
NAT = {}   # natural FBX lengths (last key, s) of the emerge candidates, from the rig-named GLBs
import sys; sys.path.insert(0, '../en_e2/scripts'); L = __import__('21_lint_export')
for k, f in [('zombie stand up', 'nsz__zombie_stand_up'), ('zombie stand up (2)', 'nsz__zombie_stand_up_2'), ('zombie stand up (3)', 'nsz__zombie_stand_up_3'),
             ('zombie crawl', 'sz__zombie_crawl'), ('running crawl', 'sz__running_crawl')]:
    js, _ = L.load_glb('mxglb/%s.glb' % f); an = js['animations'][0]
    NAT[k] = round(max(js['accessors'][s['input']]['max'][0] for s in an['samplers']), 4)
def row(t, c):
    r = M[t][c]; lt = LT[t].get(c, {})
    d = dict(clip=c, source=S[t if t in S else t]['sources'].get(c, '') if t in S else '', length_s=r['length_s'],
             lint='%s %d/%d' % (lt.get('verdict', '?'), lt.get('failing_frames', 0), lt.get('frames', 0)),
             arm_elev_mean_LR=[r['arm_L']['mean'], r['arm_R']['mean']], arm_elev_max_LR=[r['arm_L']['max'], r['arm_R']['max']],
             hips_excursion_m=r.get('hips_excursion_m'), top_m=r['top_m'], lowest_m=r['low_min_m'], t0=r['t0'])
    if 'slide_pct' in r: d.update(drive_m_s=r['drive_m_s'], stance_foot_m_s=r['foot_m_s'], slide_pct=r['slide_pct'], seam_m=r.get('seam_m'))
    else: d.update(foot_creep_m=r['foot_creep_m'])
    if 'seam_m' in r: d['seam_m'] = r['seam_m']
    return d
out = dict(_what='MX audition (R-C9-149, C-9 Phase 2 lane MX): Mixamo Creature / Zombie packs grafted onto COPIES of shipped bodies next to the '
                 'clips of record; measures per clip; ONE recommendation per body. No pack root, kit or manifest changed; Matt picks from the sheets.',
           method=dict(graft='en_e2 e40a (FBX -> rig-named GLB) + e40b (55_clip_graft world-space transfer + T->A rest alignment), window [1/30 s, end], '
                             'loops +loop+deroot, one-shots +deroot -- the EN-E2 convention; self-check: re-grafting axe_unarmed_walk_forward onto final_d '
                             'reproduces the shipped walk to 0.0000 m',
                       joint_lint='nb_join/scripts/j_joint_lint.py, ref = the body\'s own hit of record; FAIL = any frame past elbow/knee -5 deg '
                                  'hyperextension or wrist flex 80 / dev 40 deg (EN-E2 fixes such frames with 63_joint_fix --dev-max 38)',
                       foot_slide='en_e2 s6 estimator (planted ankle = bottom 25 % of its height range, median backward speed, 60 Hz) vs the drive '
                                  'speed (record: manifest locomotion_in_place; graft: source root travel / length); foot_creep = a planted ankle\'s '
                                  'largest horizontal travel in one contact (non-locomotion)',
                       arm_elevation='upper arm from hanging straight down (deg), mean / max over every key (en56_arm_calm, world up)',
                       camera='stills + films: play camera ortho, pitch 52.9535 deg, yaw 47 deg, 100.617 px/m (en_e2 film_rt copy)'),
           bodies={})
REC = {
 'fleshhulk': dict(recommend='HYBRID: Creature Pack locomotion + idle + punch; keep the record slam / lob / hit / death',
   map={'idle': 'mx_idle_breath (mutant breathing idle)', 'walk': 'mx_walk (mutant walking)', 'run': 'mx_run (mutant run)',
        'attack': 'mx_punch (mutant punch)', 'slam': 'KEEP record', 'lob': 'KEEP record', 'hit': 'KEEP record', 'death': 'KEEP record'},
   why=['idle: breathing idle holds the arms out at 40/42 deg (record 15/16) with the head at 0.92 of rest (record 1.02): a hunched, wide, heavy stance; lint PASS, seam 0.000, creep 0.003 m',
        'walk: slide 5.0 % vs 8.8 %; lint PASS; own speed 1.87 m/s (record 1.45: 0.78x playback at the record speed); seam 0.019 m (EN-E2 58 loop blend closes it)',
        'run: slide 16.6 % vs 18.8 %; lint PASS; 3.39 m/s own (record 3.90)',
        'attack: punch lint PASS 0/34, creep 0.17 m vs the record swing 0.53 m, stays on the anchor (hips 0.24 m); swipe FAILS 7/73 (wrist dev 50) and lunges 1.05 m off the anchor',
        'slam: mutant jump attack FAILS 34/112, leaves the anchor 1.38 m and peaks at 5.61 m (1.87x its standing 3.0 m, so a max-fit kit would shrink the whole body to fit the leap): reject; record slam PASS',
        'death: mutant dying FAILS 2/105 and sinks 0.37 m under the floor (record 0.21): keep the record']),
 'colossus': dict(recommend='HYBRID: the fleshhulk set (Creature Pack idle / walk / run / punch) + mutant roaring for roar; keep record slam / lob / hit / death',
   map={'idle': 'mx_idle_breath', 'walk': 'mx_walk', 'run': 'mx_run', 'attack': 'mx_punch', 'roar': 'mx_roar (mutant roaring)',
        'slam': 'KEEP record', 'lob': 'KEEP record', 'hit': 'KEEP record', 'death': 'KEEP record'},
   why=['same graft geometry as the fleshhulk (one rig family): walk slide 4.6 % vs 6.0 %, run 21.1 % vs 19.7 % (a wash), every pick lint PASS',
        'roar: mutant roaring lint PASS 0/162, creep 0.08 m, reads as a creature roar (record = axe battlecry); natural 5.37 s vs record 2.83 s -- KC2 warps one-shots, so it compresses ~1.9x into the same window',
        'flex FAILS 1/133; swipe FAILS 6/73 and lunges 1.09 m; jump attack FAILS 23/112, 5.77 m tall']),
 'revenant': dict(recommend='KEEP the record set; adopt ONLY Scary Zombie "zombie idle" for idle',
   map={'idle': 'mx_idle_sz (zombie idle)', 'walk': 'KEEP record', 'run': 'KEEP record', 'cast_bolt': 'KEEP record', 'cast_area': 'KEEP record', 'hit': 'KEEP record', 'death': 'KEEP record'},
   why=['idle: zombie idle lint PASS, arms 26/14 deg (record 34/62: the caster idle\'s raised right arm), creep 0.004 m, seam 0.001 m, 4.27 s',
        'walk: the zombie walks carry their own 0.33 m/s (Scary) / 0.54 m/s (Not So Scary); the record drives at 1.61 m/s, so they need 4.9x / 3.0x playback or skate; stumbling travels SIDEWAYS 2.75 m (slide 86 %, lint FAIL 5/116)',
        'run: zombie run is a wash (slide 18.6 % vs 22.9 %, own 2.98 vs 3.78 m/s), no read gain on a caster',
        'attack/death: zombie attack FAILS 7/76, zombie death FAILS 3/85; zombie dying PASSES here but FAILS 11/100 on the wretch -- not adopted; the revenant is a caster (cast_bolt / cast_area) and no zombie clip casts']),
 'wretch': dict(recommend='HYBRID: zombie idle + zombie attack + zombie reaction hit; keep the record walk / run / throw / buff / death',
   map={'idle': 'mx_idle_sz (zombie idle)', 'swipe': 'mx_attack_sz (Scary zombie attack)', 'hit': 'mx_hit (zombie reaction hit)',
        'walk': 'KEEP record', 'run': 'KEEP record', 'throw': 'KEEP record', 'buff': 'KEEP record', 'death': 'KEEP record'},
   why=['attack: Scary zombie attack lint PASS 0/76 on this body, creep 0.05 m vs the record backhand 0.21 m, stays on the anchor (hips 0.11 m vs 0.67 m), 2.50 s vs 3.17 s, strike R hand at 1.00 s',
        'idle: zombie idle PASS, natively hunched (head 0.94 of rest) without the en31 hunch edit; creep 0.004 m',
        'hit: zombie reaction hit PASS 0/46, creep 0.03 m',
        'walk: Not So Scary "walking" grips best (slide 1.1 %) but its own speed is 0.52 m/s vs the record 0.947 -> 1.8x playback or 82 % slide at the record speed: NOT adopted unless the record speed drops (engine side)',
        'death: zombie death FAILS 4/85, zombie dying FAILS 11/100: keep the record']),
 'emerge': dict(recommend='Not So Scary "zombie stand up" (the first, 3.10 s) for BOTH the golem p05 emerge and the revenant barrow-door rise',
   map={'en-golem emerge': 'mx_standup1 (replaces the en29 crouch-hold + crouch-to-stand, which never touches the ground)', 'en-revenant emerge (new state)': 'mx_standup1'},
   why=['starts LYING at the snow line: t0 head at 0.12 (revenant) / 0.18 (golem) of standing, lowest point +0.06 / -0.20 m -- on or under the ground, never floating',
        'lint: golem PASS 0/94, revenant FAIL 2/94 (wrist, the EN-E2 63_joint_fix class); stand up (2) FAILS 2-8/175, stand up (3) 37-72/181, crawl 42-85/155',
        'length: natural 3.133 s (3.100 s windowed) vs am3 window D 3.533 s (golem) / 3.467 s (voidlord): a 1.12-1.14x stretch, the least of the three (stand up (2) 5.833 s / (3) 6.033 s need ~0.6x)',
        'zombie crawl is locomotion on the belly (slide 91-93 % in place), not a rise: reject as an emerge']),
}
for t in B:
    clips = [c for c in M[t]]
    out['bodies'][B[t]] = dict(height_m={'fleshhulk': 3.0, 'colossus': 3.2, 'revenant': 1.8, 'wretch': 1.8, 'golem': 2.3}[t],
                               sheet='sheets/%s_stills8_current_vs_mixamo.png' % t if t != 'golem' else 'sheets/golem_emerge_stills8_current_vs_mixamo.png',
                               film='film/%s_sbs_1x.mp4' % t if t != 'golem' else 'film/golem_em_sbs_1x.mp4',
                               recommendation=REC[t] if t in REC else REC['emerge'], clips={c: row(t, c) for c in clips})
out['bodies']['en-revenant']['emerge_sheet'] = 'sheets/revenant_emerge_stills8_mixamo.png'; out['bodies']['en-revenant']['emerge_film'] = 'film/revenant_em_sbs_1x.mp4'
out['emerge'] = dict(recommendation=REC['emerge'], natural_length_s=NAT,
                     windowed_length_s={'zombie stand up': 3.1, 'zombie stand up (2)': 5.8, 'zombie stand up (3)': 6.0, 'zombie crawl': 5.1333},
                     am3_window_D_s={'en-golem': 3.5333, 'en-voidlord': 3.4667})
json.dump(out, open('summary.json', 'w'), indent=1, ensure_ascii=False); open('summary.json', 'a').write('\n')
# ---- the summary sheet (PNG)
Fm = ImageFont.truetype('/System/Library/Fonts/Menlo.ttc', 17); Fb = ImageFont.truetype('/System/Library/Fonts/Menlo.ttc', 22); Ft = ImageFont.truetype('/System/Library/Fonts/Menlo.ttc', 30)
lines = [('T', 'MX AUDITION (R-C9-149) -- Mixamo Creature / Zombie packs vs the clips of record. ONE recommendation per body. Nothing re-rendered; no kit touched.'),
         ('m', 'graft = en_e2 e40a+e40b onto a COPY of the shipped body (self-check 0.0000 m) | lint = j_joint_lint ref hit | slide = s6 stance ankle vs drive speed | arm = upper-arm elevation from hanging'), ('', '')]
hdr = '%-16s %-34s %6s %-12s %11s %11s %-22s %6s %6s %6s' % ('clip', 'source', 'len s', 'joint lint', 'arm mean', 'arm max', 'foot (slide%/creep m)', 'hipsX', 'top', 'low')
for t in ['fleshhulk', 'colossus', 'revenant', 'wretch', 'golem']:
    b = out['bodies'][B[t]]; R = b['recommendation']
    lines.append(('B', '%s  (%.2f m)  ->  %s' % (B[t], b['height_m'], R['recommend'])))
    for w in R['why']: lines.append(('w', '   - ' + w))
    lines.append(('h', hdr))
    for c, r in b['clips'].items():
        foot = ('slide %5.1f%% @%.2f' % (r['slide_pct'], r['drive_m_s'])) if 'slide_pct' in r else ('creep %.3f' % r['foot_creep_m'])
        src = S['golem_em' if t == 'golem' else t]['sources'].get(c, '')
        lines.append(('r' if c.startswith('mx_') else 'c', '%-16s %-34s %6.2f %-12s %5.0f/%-5.0f %5.0f/%-5.0f %-22s %6.2f %6.2f %6.2f' % (
            c, src[:34], r['length_s'], r['lint'], r['arm_elev_mean_LR'][0], r['arm_elev_mean_LR'][1], r['arm_elev_max_LR'][0], r['arm_elev_max_LR'][1],
            foot, r['hips_excursion_m'], r['top_m'], r['lowest_m'])))
    lines.append(('', ''))
E = out['emerge']
lines.append(('B', 'EMERGE  ->  ' + E['recommendation']['recommend']))
for w in E['recommendation']['why']: lines.append(('w', '   - ' + w))
lines.append(('w', '   natural lengths (s): ' + ', '.join('%s %.3f' % kv for kv in NAT.items())))
for t in ['revenant', 'golem']:
    for c in ['mx_standup1', 'mx_standup2', 'mx_standup3', 'mx_crawl'] + (['emerge'] if t == 'golem' else []):
        r = M[t][c]; lt = LT[t][c]
        lines.append(('r', '   %-9s %-12s t0: lowest %+.2f m, head %.2f / hips %.2f of standing | lint %s %d/%d | creep %.2f m | len %.2f s' % (
            t, c, r['t0']['low_m'], r['t0']['head_ratio'], r['t0']['hips_ratio'], lt['verdict'], lt['failing_frames'], lt['frames'], r.get('foot_creep_m', 0), r['length_s'])))
LH = 26; W = 2700; im = Image.new('RGB', (W, 40 + LH * len(lines)), (246, 243, 236)); dr = ImageDraw.Draw(im)
col = dict(T=(0, 0, 0), m=(70, 70, 70), B=(20, 20, 120), w=(30, 30, 30), h=(110, 110, 110), r=(150, 40, 20), c=(20, 60, 20))
y = 20
for k, s in lines:
    dr.text((20, y), s, fill=col.get(k, (0, 0, 0)), font=Ft if k == 'T' else Fb if k == 'B' else Fm); y += LH + (10 if k == 'T' else 0)
im.save('sheets/mx_audition_summary.png'); print('wrote summary.json + sheets/mx_audition_summary.png', im.size)
