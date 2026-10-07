import hashlib, json, os
SP = "/private/tmp/claude-501/-Users-admin-Games-reincarnated-collaboration/df21e264-6571-4d04-96ee-b8e2bd6d97fa/scratchpad"
O = "/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst/runs/C-9/barrow_full"
PC = "/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst/runs/C-9/barrow_v2/fid/pc"
sha = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest()
res = {"_what": "BV2F R-C9-210 (3): positive control T1-T3 re-measured at the Phase-0 pin f1aa715ac and at current barrow_full HEAD, each in its own APFS clone; v1 tools run unmodified in the clone; barrow_full untouched (control_shas_phase2pp.json).",
       "pin_clone": "HEAD working tree with the paths added after f1aa715ac moved out (godot/data/bv2f, godot/scripts/bv2f, godot/tools/bv2f, godot/scenes/bv2f_barrow_v2.tscn); git diff f1aa715ac..HEAD on barrow_full = additions only (all under bv2f roots), no v1 file modified",
       "head_commit_barrow_full": "3686cea98", "runs": {}}
for tag in ("pin", "head"):
    BF = "%s/pc6_%s/C-9/barrow_full" % (SP, tag); OUT = "%s/pc6_%s/out" % (SP, tag)
    r = {}
    ic = json.load(open(BF + "/take/ids/ids.json"))["instrument_check"]
    r["T1"] = {"worst_px": ic["worst_px_camera_vs_formula"], "placements_checked": ic["placements_checked"],
               "ids_png_ident_v1": sha(BF + "/take/ids/ids.png") == sha(BF + "/take/ids_v1orig/ids.png"),
               "ids_json_ident_v1": sha(BF + "/take/ids/ids.json") == sha(O + "/take/ids/ids.json"),
               "take_outputs_ident_v1": {f: sha(BF + "/take/" + f) == sha(O + "/take/" + f) for f in ("take_report.json", "plates/plates.json", "masks/tufts.json", "masks/density_uv.png", "ground/ground_uv.png", "ground/splat_world.png")}}
    m = json.load(open(BF + "/take/build/mini_overlay.json"))
    r["T2"] = {"unlit_mean_abs": m["summary"]["unlit_mean_abs"], "lit_mean_abs_informational": m["summary"]["lit_mean_abs"],
               "per_piece_unlit": {k: v["unlit"]["mean_abs"] for k, v in m["pieces"].items()}}
    oc = json.load(open(OUT + "/overlay_check.json"))["variants"]["as_painted"]
    tw = oc["whole_window"]["heather + shrub tufts"]
    pp = json.load(open(BF + "/take/build/painted_prep.json"))["heather"]["placement"]
    ndiff = sum(1 for dp, _, fs in os.walk(O + "/godot/data/painted") for f in fs if sha(os.path.join(dp, f)) != sha(os.path.join(dp, f).replace(O, BF)))
    r["T3"] = {"precision_drawn_on_painted": tw["precision_drawn_on_painted"], "coverage": tw["coverage"],
               "per_chunk_precision": {k: v["heather + shrub tufts"]["precision_drawn_on_painted"] for k, v in oc["per_chunk"].items()},
               "painted_prep_heather_share": pp["heather"]["tuft_cells_covered_share"], "painted_prep_shrub_share": pp["shrub"]["tuft_cells_covered_share"],
               "painted_data_files_differing_from_v1": ndiff}
    res["runs"][tag] = r
P0 = json.load(open(PC + "/results.json"))
rec = {"T1_worst": 0.004, "T2_unlit": 15.5, "T3_precision": 0.5221, "T3_coverage": 0.3407, "T3_share": 0.4379}
v = {}
for tag, r in res["runs"].items():
    ok = (r["T1"]["worst_px"] <= 0.005 and r["T1"]["placements_checked"] == 86 and r["T1"]["ids_png_ident_v1"] and r["T1"]["ids_json_ident_v1"] and all(r["T1"]["take_outputs_ident_v1"].values())
          and abs(r["T2"]["unlit_mean_abs"] - 15.5) <= 0.5
          and abs(r["T3"]["precision_drawn_on_painted"] - 0.5221) <= 0.0005 and abs(r["T3"]["coverage"] - 0.3407) <= 0.0005
          and r["T3"]["painted_prep_heather_share"] == 0.4379 and r["T3"]["painted_data_files_differing_from_v1"] == 0)
    v[tag] = "PASS" if ok else "MISS"
same = json.dumps(res["runs"]["pin"], sort_keys=True) == json.dumps(res["runs"]["head"], sort_keys=True)
res["verdict"] = {"pin": v["pin"], "head": v["head"], "pin_vs_head_identical": same,
                  "halt": (not same) or v["pin"] != "PASS" or v["head"] != "PASS"}
json.dump(res, open(PC + "/results_phase2pp.json", "w"), indent=1)
print(json.dumps(res["verdict"]), {t: (r["T1"]["worst_px"], r["T2"]["unlit_mean_abs"], r["T2"]["lit_mean_abs_informational"], r["T3"]["precision_drawn_on_painted"], r["T3"]["painted_prep_heather_share"]) for t, r in res["runs"].items()})
