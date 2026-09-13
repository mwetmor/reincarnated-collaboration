# Conductor brief generator: P4 TRANSCRIBE (motion questions by eye, separate instance) + PACK (cell packet). usage: mk_p4_tr_pack.py <check_bid> [...]
import json, pathlib, sys
S = pathlib.Path('/private/tmp/claude-501/-Users-admin-Games-reincarnated-collaboration/423f7949-3b86-43e3-82bd-845c71630541/scratchpad')
B = pathlib.Path('/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst'); A = B/'runs/C-3/artifacts'
Q = json.load(open(B/'runs/C-3/matrix_questions.json'))['sets']
FACE = {'S':'toward the camera','SW':"toward the screen's lower-left",'W':'screen-left (left profile)','NW':"away from the camera toward the upper-left",'N':'directly away from the camera','NE':"away from the camera toward the upper-right",'E':'screen-right (right profile)','SE':"toward the screen's lower-right"}
for cb in sys.argv[1:]:
    _, D, a = cb.split('-')[:3]; a = a.split('-')[0]; suffix = cb[len(f'P4c-{D}-{a}'):]
    art = A/cb; n = {'idle':16,'walk':12,'run':8,'jump':8,'cast':8}[a]
    items = list(Q[a]['items']) + [{'id':'first_second_head_down','question':'In the t=0.0, t=0.5 and t=1.0 panels of the second image, is the head tilted DOWN so her gaze points at the ground or her feet in ANY of the three panels?','expected':'no','class':'motion'}]
    refs = []
    if (art/'grid.png').exists(): refs.append({'path': str(art/'grid.png'), 'role': f'the {n} registered animation frames of ONE {a} cycle/one-shot, numbered 0…{n-1}, read left-to-right, top-to-bottom'})
    refs.append({'path': str(art/'first_second.png'), 'role': 'the first second of the source clip: three panels t=0.0, t=0.5, t=1.0'})
    tb = f'P4t-{D}-{a}{suffix}'
    qtxt = '\n'.join(f"{i+1}. [{it['id']}] {it['question']}" for i, it in enumerate(items))
    text = (f"TRANSCRIBE BURST {tb} — answer closed YES/NO questions about ONE animation of a painted 2D character (a young woman with a staff), by looking. task_id \"{tb}\". You are a separate instance: you have not seen any prompt, receipt, measurement or prior answer and must not look for one. The character should face {FACE[D]} and perform: {a}.\n"
      + ('' if (art/'grid.png').exists() else 'NOTE: the frame grid could not be produced for this cell; answer only the questions you can answer from the first-second image and answer "cannot tell" for the rest.\n')
      + f"Answer every question with exactly one of: \"yes\", \"no\", \"cannot tell\" — presence/absence only, never coordinates, never free vocabulary — plus one short line of visible evidence (name frame numbers).\n{qtxt}\n\n"
      f"Write out/answers.json: {{\"task_id\":\"{tb}\",\"answers\":[{{\"id\":\"…\",\"answer\":\"yes|no|cannot tell\",\"evidence\":\"…\"}}, …]}} with one entry per question in order. No image_gen. No code. No web. No files outside out/. calls_used must be 0.\n"
      f"RETURN: receipt task_id \"{tb}\"; images []; files [out/answers.json + sha256]; status DELIVERED / DELIVERED_WITH_CONCERNS; concerns for anything you could not assess. Never PASS/FAIL.")
    json.dump({"text": text, "references": refs, "image_cap": 0, "minutes_cap": 15, "tool_call_cap": 20, "outputs": ["out/answers.json"], "effort": "high", "add_dirs": [], "experiment": "C3-P4", "questions": items}, open(S/'briefs_stage'/f'{tb}.task.json','w'), indent=1, ensure_ascii=False)
    pb = f'P4p-{D}-{a}{suffix}'
    oracle = f" --oracle {B}/fixtures/muybridge/plate13_lateral --oracle-fps 8.33" if (a == 'walk' and D in ('E','W')) else ''
    text = (f"PACK BURST {pb} — review packet for Run C-3 matrix cell {a.upper()} × {D} with the FROZEN packet builder. task_id \"{pb}\".\n\n"
      f"Inputs (read-only): the cut {art}/cut (frames + registration.json) and its checks {art}/checks.json. Run exactly once: `cd {B} && python3 -B -m review.cell_packet --cell {art}/cut --checks {art}/checks.json --out $PWD/out/packet{oracle}` (use the absolute path of this burst's out/ directory). If the cut has no frames (a cell whose cut recorded no cycle/detection), do not run the builder: write out/packet/summary.txt with the cell name and the reason copied from checks.json and out/packet/review.html (self-contained, no external references) showing that reason and first_second.png copied into out/packet/img/.\n"
      f"No image_gen. No code beyond that page. No writes outside out/. No web. calls_used 0. BUDGET: under 5 minutes.\n"
      f"RETURN: receipt task_id \"{pb}\"; images []; files: every out/packet/** file with sha256; status DELIVERED / DELIVERED_WITH_CONCERNS; concerns for anything missing. Never PASS/FAIL.")
    json.dump({"text": text, "references": [], "image_cap": 0, "minutes_cap": 15, "tool_call_cap": 20, "outputs": ["out/packet/review.html"], "effort": "high", "add_dirs": [], "experiment": "C3-P4"}, open(S/'briefs_stage'/f'{pb}.task.json','w'), indent=1, ensure_ascii=False)
    print(tb, pb, len(refs))
