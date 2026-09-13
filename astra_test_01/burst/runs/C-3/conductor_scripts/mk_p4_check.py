# Conductor brief generator: Run C-3 P4 per-cell CHECK (cut + report-only measures + transcriber sheets). Data, not lane code.
import json, pathlib, sys
S = pathlib.Path('/private/tmp/claude-501/-Users-admin-Games-reincarnated-collaboration/423f7949-3b86-43e3-82bd-845c71630541/scratchpad')
B = pathlib.Path('/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst'); XV = B/'runs/C-3/xvideo/in'
W = pathlib.Path('/Users/admin/astra-burst/runs/C-3')
SPEC = {'idle': (16, 8, '--prompted-period-s 2.0'), 'walk': (12, 12, ''), 'run': (8, 12, ''), 'jump': (8, 12, '--t-max-s 6.0'), 'cast': (8, 20, '--t-max-s 6.0')}
ROW = {'E': 'walk_E_video', 'SE': 'walk_E_video', 'NE': 'walk_E_video', 'W': 'walk_W_video', 'SW': 'walk_W_video', 'NW': 'walk_W_video', 'N': 'walk_N_proposal', 'S': 'walk_S_proposal'}
overrides = json.loads(sys.argv[1]) if len(sys.argv) > 1 else {}   # {"<D>_<a>": {"min_start_s": 1.0, "suffix": "-r1", "flag": "..."}}
out = []
for D in ['S', 'SW', 'W', 'NW', 'N', 'NE', 'E', 'SE']:
    for a in ['idle', 'walk', 'run', 'jump', 'cast']:
        cell = f'{D}_{a}'; o = overrides.get(cell, {})
        flags = list(o.get('flags', []))
        clip = XV/f'{cell}.mp4'; ver = 'v1'
        if a in ('jump', 'cast'):
            if (XV/f'{cell}_v2.mp4').exists(): clip, ver = XV/f'{cell}_v2.mp4', 'v2'
            else: flags.append('v2 not generated (H-C3-1 Grok balance) — cut from the full-height v1 clip (R-C3-9)')
        n, fps, extra = SPEC[a]
        if o.get('min_start_s'): extra += f" --min-start-s {o['min_start_s']}"
        bid = f"P4c-{D}-{a}{o.get('suffix', '')}"
        if a == 'idle': row, rowtxt = 'idle_relaxed_video', "score against oracle/bands_proposed.json row 'idle_relaxed_video' (proposed)"
        elif a == 'walk': row, rowtxt = ROW[D], f"score against oracle/bands_proposed.json row '{ROW[D]}' (proposed; for a diagonal this is the NEAREST profile row — label it 'nearest proposal'; a row with no quantities → measure only)"
        elif a == 'run': row, rowtxt = None, "measure as kind 'walk' (report only; there is NO run band — score nothing)"
        else: row, rowtxt = None, 'no measure() kind exists for one-shots — skip a)'
        wd = W/bid/'out'
        text = (f"CHECK BURST {bid} — Run C-3 matrix cell {a.upper()} × {D}: cut ONE registered {'cycle' if a in ('idle','walk','run') else 'one-shot'} from its Grok clip with the FROZEN cut tool, then measure it with FROZEN gates — REPORT ONLY (no verdicts; every band here is a proposal). task_id \"{bid}\".\n\n"
 f"Inputs (read-only): the clip {clip} ({ver}; 768×1168, 24 fps, 145 frames, #00ff00 plate). Frozen tools under {B}/ — read the docstrings, run them, never modify them: oracle/video_cut.py (CLI), oracle/bands_from_exemplar.py (measure, score), oracle/bands_proposed.json, gates/g6_seam.py (evaluate, g6c), gates/g1_height.py, gates/head_pitch.py (evaluate), gates/coherence.py (evaluate(frames_dir, None)), gates/matte_quality.py (rim_luma_excess). `python3 - <<'PY'` glue that imports these modules (sys.path.insert(0, '{B}')) is fine; no new tool files; PIL + numpy + scipy only; ffmpeg at /opt/homebrew/bin/ffmpeg.\n\n"
 f"STEP 1 — cut (exactly this command, once): `cd {B} && python3 -B -m oracle.video_cut --clip {clip} --kind {a} --direction {D} --n {n} --fps-out {fps} --out {wd}/cut --edge-mode clamp {extra}`. If it reports no cycle / no detection or writes no frames, do NOT retry with other parameters and do NOT choose frames yourself: record that in checks.json and go to STEP 3 (first_second.png only).\n"
 f"STEP 2 — measure (report only) into out/checks.json = {{\"cell\":\"{cell}\",\"clip\":\"{clip.name}\",\"clip_version\":\"{ver}\",\"flags\":{json.dumps(flags)},\"cut\":<the registration.json blocks: period, selection or detection (key poses + confidence), splice (incl. suspect_inside_selected), transform, wall_seconds>,\"results\":[result envelopes]}}. Frames = out/cut/frames/{a}/{D}/{a}_{D}_NN.png; rest = out/cut/frames/rest/{D}/rest_{D}.png. Each item below is one or more envelopes; if a call raises, append an envelope with value null, passed null and notes = the exception text, and continue:\n"
 f"  a) values, diagnostic = bands_from_exemplar.measure(...) — {rowtxt}; every scored envelope must carry passed = null.\n"
 f"  b) g6_seam.evaluate(frames) (G6 literal / G6b){' and g6_seam.g6c(frames, animation=\"walk\")' if a in ('walk','run') else ''}.\n"
 f"  c) G1 size stability: g1_height.evaluate(frame_i, rest) for every frame → one envelope with value = the max fraction and the per-frame list in notes.\n"
 f"  d) head_pitch.evaluate(frames, rest, fps={fps}) — report.\n  e) coherence.evaluate(frames_dir, None) — report.\n  f) matte_quality.rim_luma_excess(frame) per frame → one envelope, value = mean.\n"
 f"  g) closure: alpha-weighted mean |RGB| between frame 0 and frame {n-1}, and between frame {n-1} and the rest frame (two envelopes, unit rgb_mad).\n"
 f"STEP 3 — sheets for the separate transcriber: out/grid.png = the {n} registered frames in a grid of 4 columns, 256-px cells on #3a3f4a, each numbered 0…{n-1} in its top-left corner; out/first_second.png = the clip's native frames at t = 0.0, 0.5 and 1.0 s (ffmpeg select, no matte) side by side, each scaled to 384 px tall, labelled t=0.0 / t=0.5 / t=1.0.\n"
 f"No image_gen. No writes outside out/. No web. calls_used must be 0. BUDGET: the cut takes ~30 s; everything else is quick — deliver within 12 minutes.\n"
 f"RETURN: receipt task_id \"{bid}\"; images []; files: out/checks.json, out/grid.png, out/first_second.png, out/cut/registration.json, out/cut/series.json, every out/cut/frames/** PNG and the strip, each with sha256; status DELIVERED / DELIVERED_WITH_CONCERNS / FAILED; concerns naming anything not computed. Never PASS/FAIL.")
        task = {"text": text, "references": [], "image_cap": 0, "minutes_cap": 15, "tool_call_cap": 20, "outputs": ["out/checks.json", "out/grid.png", "out/first_second.png"], "effort": "high", "add_dirs": [], "experiment": "C3-P4"}
        json.dump(task, open(S/'briefs_stage'/f'{bid}.task.json', 'w'), indent=1, ensure_ascii=False); out.append(bid)
print(len(out), out[:3])
