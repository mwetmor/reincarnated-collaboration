import json, pathlib, hashlib, sys
from PIL import Image, ImageOps
B = pathlib.Path('/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst'); A = B/'runs/C-3/artifacts'
T = json.load(open(B/'runs/C-3/k2c_facing_table.json'))['table']
bid = sys.argv[1]; dirs = sys.argv[2].split(','); ctrl_src = sys.argv[3]; ctrl_claim = sys.argv[4]; srcs = dict(a.split('=') for a in sys.argv[5:]) if len(sys.argv) > 5 else {}
(A/'K2c-control').mkdir(parents=True, exist_ok=True)
cp = A/'K2c-control'/f'{bid}_control_mirror.png'
ImageOps.mirror(Image.open(A/srcs.get(ctrl_src, f'K2c-gen-{ctrl_src}/k2c_{ctrl_src}.png'))).save(cp)
cands = [(d, A/srcs.get(d, f'K2c-gen-{d}/k2c_{d}.png')) for d in dirs]
cands.insert(len(cands)//2, (ctrl_claim, cp))   # hidden control, mid-batch
refs = [{"path": str(B/'runs/C-1/artifacts/K1p-gen-01/k1p_master_C.png'), "role": "APPROVED MASTER (direction S)"}]
lines = []
for i, (d, p) in enumerate(cands, 2):
    refs.append({"path": str(p), "role": f"candidate, claimed direction {d}"})
    r = T[d]; lines.append(f"Image {i} claims {d}. EXPECTED for {d}: {r['text']}")
text = (f"JUDGE BURST {bid} — the Keeper's H1 8-direction turnaround (Run C-3 P2): equipment GEOMETRY verified by occlusion and anatomy, not by claim. task_id \"{bid}\". You are a separate instance: you have not seen any prompt, receipt, check or prior judgment, and must not look for one.\n\n"
 "Image 1 = the APPROVED MASTER (direction S, facing the camera): the staff is in her RIGHT hand (on SCREEN-LEFT when she faces you); ONE strap runs from her RIGHT shoulder across the chest front to an olive satchel AT HER SIDE on her LEFT hip (screen-right). THE RULE you verify for every view: a figure turned toward screen-RIGHT shows her RIGHT side (the staff side) to the camera; turned toward screen-LEFT she shows her LEFT side (the satchel side). A figure whose visible near arm is EMPTY while the staff is held by the far arm, when the rule says the staff side is near, is a MIRRORED body (and vice-versa). Judge each candidate independently against ITS claimed direction; do not assume any candidate is a control and do not assume any candidate is correct.\n\n"
 + "\n".join(lines) +
 "\n\nFor EACH candidate write, each with one line of visible evidence: seen_facing (one of S SW W NW N NE E SE); staff_side = \"near\" | \"far\" | \"screen-left\" | \"screen-right\" (back views) | \"cannot tell\" + the occlusion evidence (which arm's shoulder/forearm is in front of the torso); satchel = \"near-side\" | \"far-side\" | \"front-of-body\" | \"absent\"; strap = where it runs (over which visible shoulder; chest front or back); face_visible true|false; head_level true|false (false if looking down or turned against the body); mirrored true|false (anatomical right/left swapped relative to Image 1); then axes 1–5 (integers, one-line reasons): 1 register fidelity to Image 1 (hand-drawn tapered contour, painted planes) · 2 identity fidelity (face where visible, hair mass, costume, colours, plain surfaces) · 3 light (key from screen upper-left in every direction; lit from upper-right ≤ 2) · 4 equipment geometry vs the EXPECTED text for its claim (staff side, satchel side, strap path, face visibility — all correct = 5; each error −1; a mirrored body = 1) · 5 direction read (the claimed facing is unmistakable at 64 px tall).\n"
 "Write out/judgment.json: {\"candidates\":[{\"image\":n,\"claimed\":\"…\",\"seen_facing\":\"…\",\"staff_side\":\"…\",\"staff_evidence\":\"…\",\"satchel\":\"…\",\"strap\":\"…\",\"face_visible\":bool,\"head_level\":bool,\"mirrored\":bool,\"axes\":{\"1\":n,\"2\":n,\"3\":n,\"4\":n,\"5\":n},\"reasons\":{\"1\":\"…\",…}}, …]}. No image_gen. No code. No web. No files outside out/. calls_used must be 0.\n"
 f"RETURN: receipt task_id \"{bid}\"; images []; files [out/judgment.json + sha256]; status DELIVERED / DELIVERED_WITH_CONCERNS; concerns for anything you could not assess. Never PASS/FAIL — scores only.")
task = {"text": text, "references": refs, "image_cap": 0, "minutes_cap": 15, "tool_call_cap": 20, "outputs": ["out/judgment.json"], "effort": "high", "add_dirs": [], "experiment": "C3-P2"}
json.dump(task, open(B/f'briefs/C-3/{bid}.task.json', 'w'), indent=1, ensure_ascii=False)
print(bid, 'control = mirror of', ctrl_src, 'claimed', ctrl_claim, 'at image', len(cands)//2 + 2 if False else [i for i,(d,p) in enumerate(cands,2) if p==cp][0], '| chars', len(text))
