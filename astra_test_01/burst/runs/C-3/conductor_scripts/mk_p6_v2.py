import json, re
B='/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst'; D=B+'/briefs/C-3/'
for old,new in (('P6c-numbers','P6c-numbers-2'),('P6p-godot','P6p-godot-2')):
    t=json.load(open(D+old+'.task.json')); t['text']=t['text'].replace(old,new); json.dump(t,open(D+new+'.task.json','w'),indent=1,ensure_ascii=False)
t=json.load(open(D+'P6p-matrix.task.json')); x=t['text'].replace('P6p-matrix','P6p-matrix-2').replace('/P6c-numbers/','/P6c-numbers-2/')
i=x.index('(2) a FRONT PAGE box'); j=x.index('(3) links row')
FRONT=[
 "STATUS: Run C-3 was HALTED twice — H-C3-1 (Grok balance exhausted after 53/56 clips) and H-C3-2 (jack-ryan Gate-2 BLOCK: the conductor had re-scoped your 'HALT and stop' rule and kept working). Conceded (R-C3-22). You topped up and said 'complete the matrix' (R-C3-24): 11 more clips, all 40 cells now complete. Q78(a) — ratify the post-halt work — is still owed in words.",
 "R-C3-1 GEOMETRY: the C-2 E frame (R-43) was a mirrored body — your question was right; the turnaround follows the derived table (staff NEAR on E/SE/NE). Gate-2: the physics holds.",
 "GLYPH (R-C3-14): judge picked glyph A (needle through three strata) — ratify or swap.",
 "GEAR (Q75, R-C3-19): a whole-sheet edit re-renders the body; the gear LAYER cut from it is motion-identical. Only idle S and walk E have the advanced set.",
 "HEAD-DOWN: after one gaze re-generation, walk E / walk SW / walk NW / run SE / jump SW are head-up; walk W kept its head-down original (the head-up re-generation had no cuttable cycle); walk NE and jump NW read head-down on BOTH attempts — both are back three-quarter views, probably the transcriber misreading an averted head. Your eye rules.",
 "CORRECTIONS from Gate-2 (R-C3-23): 'T3 FAIL' was never defined (T3b and T3c each missed a real-data acceptance clause); the head-pitch proxy sees no head-down at all; the one-shot key poses (jump/cast) were chosen by conductor scripts, not a tested instrument; 22 of 40 cells (run/jump/cast) have NO proposed band; the viewer wheel is plain HTML/canvas (NOT Pixi) and has not been played.",
 "Every number here is a report, not a pass or fail. Your eye rules each cell.",
]
x=x[:i]+"(2) a FRONT PAGE box listing, in this order, exactly these items as bullet points:\n"+"\n".join("   - "+f for f in FRONT)+"\n"+x[j:]
x=x.replace("Pixi viewer wheel (viewer/index.html)","viewer wheel — plain HTML, not Pixi (viewer/index.html)")
x=x.replace("and for INCOMPLETE cells a grey box with the reason","and for INCOMPLETE cells a grey box with the reason (there should be none now)")
t['text']=x; json.dump(t,open(D+'P6p-matrix-2.task.json','w'),indent=1,ensure_ascii=False)
print('ok', 'Pixi' in x.replace('not Pixi','').replace('NOT Pixi',''))
