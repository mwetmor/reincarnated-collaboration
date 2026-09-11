# E07F — compiler-gated shared-shadow integration

Compiler gate PASS; shared floor/vertical mechanism PARTIAL; remaining native pilot samples FAIL. E07C remains the working chamber. Godot is the shipping target; Pixi is the test harness.

The single consumer build applies the prepared GLSL reserved-identifier rename to an owned E07E copy. All A/B/faction shader paths pass console and GL checks before scene captures. E07E's two failures remain; cumulative shared-shadow builds are three. No geometry, simulation, encoding, bias, light definition or art source changed.

The first integrated matrix acquires 1,336 independent source witnesses and fails 29. Depth probes at 464 independent 4×4 subpixel positions find actual GPU map depth within 0.049 mm of source map-texel ray intersections. None exceeds 1 mm. This rules out gross depth encoding or map projection error for those probes. The grid is not claimed to reproduce the driver's MSAA sample locations.

The original edge guard checked receiver group and shadow state, allowing a pixel neighborhood to cross between objects or vertical face normals. Its failure evidence is preserved. The repaired instrument additionally requires the same object over nine neighboring pixels plus a 4×4 subpixel grid; vertical normals must agree to dot >0.9999. All 29 original failing samples are rejected by that stricter source-only guard. No RGB tolerance or consumer code changed.

The repaired matrix contains 1,302 available source witnesses:
- All 576 floor and 288 vertical witnesses pass.
- Of 438 pilot samples, 436 pass and two fail. Both are the same native cast/sleeve location, repeated across factions: expected unshadowed, actual green diagnostic 64, with a material difference of 6–7 levels. These are retained failures, not waived because the receiver group lacks six shadowed samples.
- Reversed caster order preserves every observed diagnostic result.
- Missing scene, missing pilot and stale-root controls each produce detected failures on source-selected sensitive samples.
- All 24 states render without browser/GL errors.

Profile A's camera-visible vertical faces face away from the directional key, so their direct-key witness groups are unavailable. Profile B proves vertical receivers. Several native pilot groups lack enough separate lit/shadow samples after strict edge guarding; their partial samples do not qualify a full group or general self-shadow behavior. The source packet explicitly lists unavailable groups.

A read-only diagnostic evaluates receiver-plane depth at the selected map texel center. On the earlier 464-position probe set, raw lookups disagree with continuous source rays at 14 positions; plane-corrected predictions disagree at ten. It is a hypothesis for the next test, not a demonstrated complete repair. The observed two current native failures remain unresolved by this experiment.

No actual interaction or playback expansion follows the failed pilot prerequisite. Saved images show the working hard-shadow mechanism and its limitations; no final light/style choice is made. Stronger local glow, soft shadows, NPC/monster casters, full actor visibility and richer faction construction remain open.

Next E07G: verify derivative support, then test a receiver-plane lookup at the actual shadow texel center with the same 5 mm compare bias, source evidence, tolerance and negative controls. One bounded consumer build, preserving E07F. No generation or paid-service call occurred.
