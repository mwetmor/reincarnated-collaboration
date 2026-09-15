# T4d measurement delivery

## Instruments

- `oracle.vfx_measure.measure(frames_dir, fps_or_durations, body_h_px=130, plate='alpha')`: existing metrics now serialize with VO names. VO3 is the fraction of effect pixels with V > 0.85 and S >= 0.25 (integer comparison preserves the inclusive saturation boundary). Original white-core numbers remain under VO3_white_legacy. Deprecated Python lookups remain readable without adding serialized legacy keys. Legacy comparison bands target the legacy white measure rather than the new population.
- `oracle.white_gate.measure(plate, frames, impact_xy, subject='white')`: a native 960x540 crop, centred by floor(coordinate + 0.5). Out-of-bounds crops and nonopaque captures are rejected. White is exactly V > 0.95 and S < 0.20. Attribution is effect-white AND NOT plate-white at the same pixel. Peak means first maximum attributable-white frame; total and baseline are reported at that same frame. Mean includes every frame. Percent denominator is always 518,400 pixels.
- `white_gate.measure_cases(cases)` accepts separately captured flash-on/off and single/synchronised/staggered four-cast cases. Each named case contains plate, frames, impact_xy, plus optional flash, cast_pattern and cast_count metadata. Missing runs are not synthesized. `white_gate.baseline(plate, impact_xy, subject='empty_crop')` measures the clean crop.
- `event_gates.field_boundary(boundary_xy, centre_xy, radius_px)` reports signed radius errors; `activation_expiry(trace, events, activation_event='contact', expiry_event='expire')` reports observed minus stamped frame differences; `aura_attachment(aura_xy, attachment_xy, offset_xy=(0,0))` measures pointwise attachment drift; `interval_cv(event_frames)` reports population SD / mean interval. `evaluate(...)` separates effect-age clocks by effect_id/cast_id and accepts native G1 age_frames events. Missing evidence yields null quantities, never a fabricated zero. No event or white-budget tolerance was invented.

## Export fixes

Grey export removed body material uses but retained unused external-resource declarations. It now removes only declarations with no remaining use and updates load_steps; shared light/glow declarations survive. The T4f fixture exports with 653 validated references, 131 grey body frames, 10,077,144 compared pixels, zero changed alpha pixels and zero non-mid-grey body pixels.

The replay probe formerly created and replaced ImageTextures during frame_pre_draw, without image validation. It now loads/validates all native RGBA images before drawing, retains strong texture references, and only selects an existing texture during drawing. The native crop pivot is explicitly at viewport centre (the effect origin). Absolute external PNG loading was verified headless: three textures loaded on each of three backgrounds. Texture lifetime/upload timing is the diagnosed candidate mechanism; renderer confirmation remains required.

Run `python3 -B tests/probe_t4d_flipbook.py --render --out runs/C-5/t3/T4d/flipbook_probe` outside the sandbox for production-probe pixel comparisons on black, white and coloured ground. Expected source-over error is <=2 byte levels and output must contain nonwhite pixels. This sandbox's graphics process aborted with exit -6 on all three grounds, so no viewport pixel result is claimed.

## Acceptance and limitations

`frozen_orb_comparison.json` compares pre-edit and post-edit metrics on the five supplied Frozen Orb v3 impact frames at 60 fps. All ten retained quantities have identical canonical JSON bytes; VO3 is newly defined and is 0.0 in all five frames. The historical R-C3-112 report itself was not within the allowed read set.

`measurement_acceptance.json`: synthetic peak 4.000% (criterion 4.0 +/-0.2%); late expiry 12 frames (expected 12). Both 960x540 baselines and their source crop origins are in `baselines/white_baseline.json`. Dirt origin (1806,2137), foliage origin (1920,3230). They are native source-plate composites at authored layer offsets over the source project's declared clear colour, not engine captures with camera parallax and props. Baseline white: dirt 0.0719521605%, foliage 0.1612654321%.

The required `runs/C-5/baselines/white_baseline.json` location conflicts with the later explicit prohibition on writes outside `runs/C-5/t3/T4d/`. The measured baselines are staged here; the required final path is not populated by this burst.

Focused tests: `PYTHONPATH=tests PYTHONDONTWRITEBYTECODE=1 python3 -B -m unittest test_vfx_measure test_white_gate test_event_gates test_t4d_export -v`.

`run_full_suite.py` invokes the unchanged `PYTHONDONTWRITEBYTECODE=1 python3 -B tests/run_t0c.py`, with Python report writes and temporary directories redirected into permitted locations. No assertions are modified. Exact final counts, every red ID/trace, and the 1,880-value regression comparison are in `full_suite_summary.json`; complete test output is retained in `full_suite_output.txt`. Godot environment errors are reported without weakening engine assertions.
