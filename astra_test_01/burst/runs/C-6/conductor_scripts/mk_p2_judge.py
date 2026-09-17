# Conductor JUDGE brief generator for Run C-6 P2 (data, not lane code) — C-3 mk_p2_judge.py shape, scythe geometry axis.
# usage: mk_p2_judge.py <bid> <dirs csv> <ctrl_src dir> <ctrl_claim dir> [D=relpath ...]   (candidates default runs/C-6/artifacts/N5-turn-<d>/n5_<d>.png)
import json, pathlib, sys
from PIL import Image, ImageOps
B = pathlib.Path('/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst'); A = B/'runs/C-6/artifacts'
T = json.load(open(B/'runs/C-6/n5_facing_table.json'))['table']
bid = sys.argv[1]; dirs = sys.argv[2].split(','); ctrl_src = sys.argv[3]; ctrl_claim = sys.argv[4]; srcs = dict(a.split('=') for a in sys.argv[5:]) if len(sys.argv) > 5 else {}
(A/'N5-control').mkdir(parents=True, exist_ok=True)
cp = A/'N5-control'/f'{bid}_control_mirror.png'
ImageOps.mirror(Image.open(A/srcs.get(ctrl_src, f'N5-turn-{ctrl_src}/n5_{ctrl_src}.png'))).save(cp)
cands = [(d, A/srcs.get(d, f'N5-turn-{d}/n5_{d}.png')) for d in dirs]
cands.insert(len(cands)//2, (ctrl_claim, cp))   # hidden control, mid-batch
refs = [{"path": str(A/'N3-final-cam-01/necro_master_S_512.png'), "role": "APPROVED MASTER (direction S)"}]
lines = []
for i, (d, p) in enumerate(cands, 2):
    refs.append({"path": str(p), "role": f"candidate, claimed direction {d}"})
    lines.append(f"Image {i} claims {d}. EXPECTED for {d}: {T[d]}")
text = (f"JUDGE BURST {bid} — the Necromancer's 8-direction turnaround (Run C-6 P2): equipment GEOMETRY verified by occlusion and anatomy, not by claim. task_id \"{bid}\". You are a separate instance: you have not seen any prompt, receipt, check or prior judgment, and must not look for one.\n\n"
 "Image 1 = the APPROVED MASTER (direction S, facing the camera): a two-handed WAR SCYTHE — the haft runs from low at his LEFT hip (screen-right) up past his RIGHT shoulder (screen-left), and the great crescent BLADE stands above and screen-LEFT of his head, i.e. over his anatomical RIGHT; ONE great bone HORN rises from his LEFT shoulder (screen-right); a small dark TOME hangs at his LEFT hip (screen-right). THE RULE you verify for every view: a figure turned toward screen-RIGHT shows his RIGHT side (the BLADE side) to the camera — the blade is over the near shoulder; turned toward screen-LEFT he shows his LEFT side (the HORN + TOME side) and the blade rises behind the far shoulder. In back views (N/NE/NW) the blade is on the SCREEN-RIGHT of his head and the horn on the SCREEN-LEFT. A figure whose blade and horn sit on the wrong sides for its claim is a MIRRORED body. Judge each candidate independently against ITS claimed direction; do not assume any candidate is a control and do not assume any candidate is correct.\n\n"
 + "\n".join(lines) +
 "\n\nFor EACH candidate write, each with one line of visible evidence: seen_facing (one of S SW W NW N NE E SE); blade_side = \"near\" | \"far\" | \"screen-left\" | \"screen-right\" (back views) | \"cannot tell\" + the occlusion evidence (is the blade over the shoulder nearer the camera or behind the far one; which shoulder the haft top passes); horn = \"near-shoulder\" | \"far-shoulder\" | \"screen-left\" | \"screen-right\" | \"absent\"; tome = \"near-hip\" | \"far-hip\" | \"hidden\" | \"absent\"; both_hands_on_haft true|false; face_visible true|false; head_level true|false (false if looking down or turned against the body); mirrored true|false (anatomical right/left swapped relative to Image 1); back_details_wrong true|false (a FRONT ribcage relief or skull buckle drawn on the BACK in N/NE/NW); then axes 1–5 (integers, one-line reasons): 1 register fidelity to Image 1 (hand-drawn tapered contour, painted planes, no glow) · 2 identity fidelity (face where visible, white hair mass, bone-plate armour, horn, tome, scythe design and its size relative to the body) · 3 light (key from screen upper-left in every direction; lit from upper-right ≤ 2) · 4 equipment geometry vs the EXPECTED text for its claim (blade side, horn side, tome side, haft crossing, face visibility — all correct = 5; each error −1; a mirrored body = 1) · 5 direction read (the claimed facing is unmistakable at 64 px tall).\n"
 "Write out/judgment.json: {\"candidates\":[{\"image\":n,\"claimed\":\"…\",\"seen_facing\":\"…\",\"blade_side\":\"…\",\"blade_evidence\":\"…\",\"horn\":\"…\",\"tome\":\"…\",\"both_hands_on_haft\":bool,\"face_visible\":bool,\"head_level\":bool,\"mirrored\":bool,\"back_details_wrong\":bool,\"axes\":{\"1\":n,\"2\":n,\"3\":n,\"4\":n,\"5\":n},\"reasons\":{\"1\":\"…\",…}}, …]}. No image_gen. No code. No web. No files outside out/. calls_used must be 0.\n"
 f"RETURN: receipt task_id \"{bid}\"; images []; files [out/judgment.json + sha256]; status DELIVERED / DELIVERED_WITH_CONCERNS; concerns for anything you could not assess. Never PASS/FAIL — scores only.")
task = {"text": text, "references": refs, "image_cap": 0, "minutes_cap": 15, "tool_call_cap": 20, "outputs": ["out/judgment.json"], "effort": "high", "add_dirs": [], "experiment": "C6-P2"}
json.dump(task, open(B/f'briefs/C-6/{bid}.task.json', 'w'), indent=1, ensure_ascii=False)
print(bid, 'control = mirror of', ctrl_src, 'claimed', ctrl_claim, 'at image', [i for i,(d,p) in enumerate(cands,2) if p==cp][0], '| chars', len(text))
