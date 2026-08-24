"""VALIDATION — reproduce Lap K's certified trace on eor-test-2 with the new reader."""
import csv
from d4_ocr import stream, FPS
from d4_reader import read
V2='/Volumes/reincarnated/visual-artifacts/GD-matt-test/eor-test-2/video/eor-warlord-wave-150-160-2026-08-05 21-37-25.mp4'
LAPK='/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/legolas/notes/2026-08-14-kc2-pm4-lap-k-death-anchor/pm4k_full_trace.csv'
lab={}
for r in csv.DictReader(open(LAPK)):
    if r['hp_cur'] and r['hp_max']:
        lab[round(float(r['t_s'])*FPS)]=(int(r['hp_cur']),int(r['hp_max']))
agree=dis=0; mine_only=0; theirs_only=0; both_blank=0
dis_ex=[]
for i,img in stream(V2,675.0,885.0):
    f=round(675.0*FPS)+i
    mine=read(img); theirs=lab.get(f)
    if mine and theirs:
        if mine==theirs: agree+=1
        else:
            dis+=1
            if len(dis_ex)<12: dis_ex.append((f/FPS,mine,theirs))
    elif mine and not theirs: mine_only+=1
    elif theirs and not mine: theirs_only+=1
    else: both_blank+=1
tot=agree+dis
print(f'both read : {tot}   AGREE {agree} ({100*agree/max(tot,1):.4f}%)   DISAGREE {dis}')
print(f'mine-only (Lap K rejected, I read) : {mine_only}')
print(f'theirs-only (I rejected, Lap K read): {theirs_only}')
print(f'both blank: {both_blank}')
for e in dis_ex: print('   disagree', e)
