import json,sys
B='/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst'; R=B+'/runs/C-3'
tid=sys.argv[1]; DIR=sys.argv[2]
t=(f"PACK BURST {tid} — export the playable CLIFFSIDE SCENE (bare foreground + four parallax layers + follow camera) with the FROZEN exporter (Run C-3, Matt R-C3-42/48). task_id \"{tid}\".\n\n"
 f"Run exactly once, substituting OUT = the absolute path of this burst's out/ directory: cd {B} && python3 -B -m export.godot_import --cells {R}/cells --out OUT/godot --parallax {DIR} --vfx-kit {R}/vfx_scene --sockets {R}/sockets.json\n"
 "Do NOT pass --scene, --vfx or --gear-variant. Do NOT run Godot (the conductor runs the headless proof outside this sandbox). Paste the command's JSON stdout (or its stderr on failure — do not work around a failure) into out/exporter.json. Then write out/README_scene.txt (≤ 15 lines): how to open it (Godot 4.6 → Import → out/godot/project.godot → Run Project), controls (arrows/WASD move, Shift run, Space jump, E or left click cast), what is in the scene (painted cliffside foreground, parallax layers sky 0.12 / far_ruins 0.25 / forest_valley 0.45 / mist 0.70, follow camera at 12.5 % figure height, collision from the walkable data, contact shadow, directional frost bolt) and the VFX credit line from vfx_scene/CREDITS.txt.\n"
 "No image_gen. No code. No writes outside out/. No web. calls_used 0. BUDGET under 10 minutes.\n"
 f"RETURN: receipt task_id \"{tid}\"; images []; files: out/exporter.json, out/README_scene.txt, out/godot/project.godot, out/godot/scenes/*.tscn, out/godot/scripts/*.gd with sha256 (PNG copies may be omitted); status; concerns. Never PASS/FAIL.")
json.dump({"text":t,"references":[],"image_cap":0,"minutes_cap":15,"tool_call_cap":20,"outputs":["out/exporter.json"],"effort":"high","add_dirs":[],"experiment":"C3-cliffside-v3"},open(f'{B}/briefs/C-3/{tid}.task.json','w'),indent=1,ensure_ascii=False)
print('ok',tid)
