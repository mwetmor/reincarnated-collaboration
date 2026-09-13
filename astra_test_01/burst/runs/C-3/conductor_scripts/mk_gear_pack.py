import json
B='/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst'; A=B+'/runs/C-3/artifacts'
jobs={'P5p-gear-idle-S-r1':('K1p-paintchk-idle-S-r2', B+'/runs/C-1/artifacts/K3p-xv-idle-cut-01/frames/idle/S', 8),
      'P5p-gear-walk-E-r1':('K1p-paintchk-walk-E-r2', A+'/P4c-E-walk/cut/frames/walk/E', 12)}
for bid,(chk,base,fps) in jobs.items():
    cmd = f"cd {B} && python3 -B -m review.cell_packet --cell {A}/{chk}/advanced --checks {A}/{chk}/checks.json --out <ABSOLUTE PATH OF THIS BURST'S out/>/packet --oracle {base} --oracle-fps {fps}"
    text=(f"PACK BURST {bid} — review packet for the Keeper ADVANCED gear set (Run C-3 P5, fork C) with the FROZEN packet builder; the STARTER frames play beside it as the comparison. task_id \"{bid}\".\n\n"
      f"Run exactly once (substitute the absolute path of this burst's out/ directory): {cmd}\n"
      f"Then copy into out/packet/img/ these read-only evidence images and append a section to out/packet/review.html (self-contained, relative paths only) titled 'Gear layer evidence', each with a one-line caption: {A}/{chk}/regions_overlay.png ('regions: staff head + pauldron; base | edited sheet cell | composited'), {A}/{chk}/gear_layer_strip.png ('pixels taken from the edit'), {A}/K1p-adv-01/adv_2.png ('the advanced still, judge-selected'), {A}/K1p-sig-01/glyph_A.png ('provenance mark: glyph A, judge pick; Matt ratifies'). Label the oracle video 'STARTER (same motion)'.\n"
      "No image_gen. No code beyond that HTML edit. No writes outside out/. No web. calls_used 0. BUDGET under 6 minutes.\n"
      f"RETURN: receipt task_id \"{bid}\"; images []; files: every out/packet/** file with sha256; status DELIVERED / DELIVERED_WITH_CONCERNS; concerns. Never PASS/FAIL.")
    json.dump({"text":text,"references":[],"image_cap":0,"minutes_cap":15,"tool_call_cap":20,"outputs":["out/packet/review.html"],"effort":"high","add_dirs":[],"experiment":"C3-P5"},open(B+f'/briefs/C-3/{bid}.task.json','w'),indent=1,ensure_ascii=False)
    print(bid, 'cell_packet' in text)
