# Revised asset process

This run is stopped after two failed turnaround checkpoints. These instructions
describe the implemented preparation tools and the remaining production sequence;
they do not authorize a third checkpoint or claim animation qualification.

1. Declare tool availability and controls. Preserve source artwork, prompts, source
   hashes and actual image modes. Use one qualified S master for all directions.
2. Fix camera geometry in `guides.py`. Guides condition pose and camera only; their
   procedural geometry must never appear as painted deliverables.
3. Qualify alpha before further generation. `pipeline.extract` preserves native
   alpha or keys an explicitly requested green plate. Inspect dark, light and blue
   composites. Its largest-component cleanup is character-specific and must not be
   reused for detached VFX shards or particles.
4. Establish one scale per direction. Reject upscaling. Annotate two source sole
   regions, then use `registration_preflight.measured_anchor` to derive the source
   midpoint. Do not manually estimate a midpoint from a thumbnail.
5. Inspect separately selected output sole regions with `preflight` before freezing
   a checkpoint. A region touching the lowest contact pixels at its lower or side
   boundary is invalid. An occluded sole needs explicit visual annotation and
   uncertainty; never crop another leg to manufacture a foot position.
6. Run the complete eight-direction checkpoint only after preparation is finished.
   Count full evaluations honestly, preserve failures, and repair all identified
   defects as a set. Exact register, alpha and literal light tests still govern.
7. After turnaround PASS, generate direction-specific animation key poses using the
   master and approved direction as references. Lock direction scale and root
   registration. Do not independently resize each pose to conceal breathing or
   drift. Validate source resolution before commissioning a multi-frame sheet.
8. Verify actual counts (8 idle, 8 walk, 12 cast per direction), unique motion,
   support-foot/root behavior, screen-fixed light, and spawn index 5. Compare each
   loop's consecutive differences to the predeclared cast frame 5; compare the loop
   seam against the minimum internal adjacent difference. Preserve literal failures.
9. Generate frost modules separately; qualify native alpha or a particle-safe
   extraction method before the full 8/6/10-frame modules. Compare brushwork to the
   actual character release frame. Character failure is not a VFX style verdict.
10. Pack only actual frames, create exact atlas metadata, inspect the browser's S/E
    cast-to-travel-to-impact sequence, and state any missing verification explicitly.

Run the instrument tests from the repository root:

```sh
python3 -m unittest discover -s astra_test_01/run_02 -p 'test_*.py' -v
```

`evidence/checkpoint_checker_v1.py` records the permissive ROI checker used for the
two frozen checkpoints (its imports require the run directory on PYTHONPATH).
Current `check.py` uses the stricter preflight and refuses to overwrite either
checkpoint. `evidence/instrument_audit.json` documents the resulting uncertainty.
