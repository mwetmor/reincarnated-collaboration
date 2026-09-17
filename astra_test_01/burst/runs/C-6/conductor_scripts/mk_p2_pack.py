# Conductor PACK brief for the C-6 turnaround packet (C-3 P2p-turnaround shape). usage: mk_p2_pack.py <bid> <packet_no> <judgment relpaths csv> [D=relpath ...]
import json, pathlib, sys
B = pathlib.Path('/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst'); A = B/'runs/C-6/artifacts'
bid, pno, judg = sys.argv[1], sys.argv[2], sys.argv[3].split(','); over = dict(a.split('=') for a in sys.argv[4:])
src = {'S': A/'N3-final-cam-01/necro_master_S_512.png', **{d: A/f'N5-turn-{d}/n5_{d}.png' for d in ['SW','W','NW','N','NE','E','SE']}}
for d, rel in over.items(): src[d] = B/rel
order = ['S','SE','E','NE','N','NW','W','SW']
inputs = '; '.join(f'{d} = {src[d]}' for d in order)
text = (f"PACK BURST {bid} — packet {pno}: the Necromancer's 8-direction turnaround (Run C-6 P2). task_id \"{bid}\".\n\n"
 f"Inputs (read-only): {inputs}; judgments {', '.join(str(B/j) for j in judg)} (in N5-jdg-01 image 5 was the hidden MIRRORED control claiming SW — say so and report it was caught: mirrored=true, axis 4 = 1); the conductor's facing table {B/'runs/C-6/n5_facing_table.json'}; the selection note {B/'runs/C-6/p2_selection.json'} (which attempt stands per direction and why).\n"
 "With PIL: out/turnaround_strip.png (S SE E NE N NW W SW left→right, each still cropped to its figure bbox with a 40-px margin and scaled to 600 px tall, labelled, on #3a3f4a) and out/wheel.png (the 8 stills arranged on a compass: N top, E right, S bottom, W left, diagonals between, labelled). out/review.html (self-contained, relative out/ paths): title; a FLAG box quoting the selection note's flags verbatim (any direction that stands with a known deduction); the strip; the wheel; a table per direction: claimed, seen_facing, blade_side, horn, tome, both_hands_on_haft, head_level, mirrored, back_details_wrong, axes 1–5 and the axis-4 reason, from the judgment rows of the attempt that STANDS (skip the control row but report it caught); the facing-table text per direction. out/summary.txt ≤ 12 lines. No image_gen. No code beyond the page and the two PIL images. No writes outside out/. No web. calls_used 0.\n"
 f"RETURN: receipt task_id \"{bid}\"; images []; files: every out/ file with sha256; status DELIVERED / DELIVERED_WITH_CONCERNS; concerns. Never PASS/FAIL.")
task = {"text": text, "references": [], "image_cap": 0, "minutes_cap": 15, "tool_call_cap": 20, "outputs": ["out/review.html","out/turnaround_strip.png","out/wheel.png","out/summary.txt"], "effort": "high", "add_dirs": [], "experiment": "C6-P2"}
json.dump(task, open(B/f'briefs/C-6/{bid}.task.json', 'w'), indent=1, ensure_ascii=False); print(bid, len(text))
