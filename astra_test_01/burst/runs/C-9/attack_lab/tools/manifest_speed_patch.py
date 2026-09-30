"""THE MANIFEST SPEED UNIT for knight.gd (T12_10) -- a manifest speed drives the body at the speed it states.

Every locomotion speed in knight.gd ends up as canvas px/s AT THE REFERENCE SCALE
(character.json speed_measured_at_scale, 1.25178) and is then multiplied by
_figure_scale / reference: walk_px_s and run_px_s were measured at 1.25178, and so was the
clip_px_s fallback table. _read_manifest_speeds converted the export manifest's metres per
second with PPM alone -- canvas px/s at figure scale 1.0 -- and handed that to the same
rescale, so every manifest-priced clip was driven at 1/1.25178 = 0.799 of its stated speed.

Measured (tools/strafe_probe.gd, 2026-09-30, across-screen, figure scale 1.0): the T12_9
strafe_L was asked 0.844 m/s by the manifest and moved at 0.674; with T12_10's foot-lock speed
0.724 it moved at 0.578 while its planted feet moved 0.731 relative to the body -- feet sliding
backward at 26%. The old stepping speed had been overstated by about the same factor, so the two
errors had hidden each other. The fix states manifest speeds at the reference scale (x the
reference) so the rescale that follows lands on m/s x PPM x figure scale -- the unit the rest
of the file already uses for de-rooted clips (_root_speeds x PPM x _figure_scale).

knight.gd moves at a fixed CANVAS speed by design (canvas_velocity_to_world: the 2D route's
feel), so a ground speed stated in m/s is exact across the screen and up to 1/sin(pitch) =
1.25x more up the screen -- the same as the walk and the run. Pinned feet are defined across
the screen.

    python3 manifest_speed_patch.py <knight.gd in> <knight.gd out>

Applied over strike_release_patch.py's knight (ea761ba8). Refusing: every anchor must match once."""
import sys

src, dst = sys.argv[1], sys.argv[2]
s = open(src).read()
REP = [
    ('''	STEPPING, where the manifest offers it. Net displacement over a whole clip is the wrong
	number for a blend space whenever the clip has stationary portions: strafe_R's net is
	0.340 m/s against a stepping 0.536, because it stands still for part of the clip, and a
	blend space drives the body only while he is travelling. Where there is no stepping
	figure, `speed_m_s` over one gait cycle is the same quantity."""
''',
     '''	THE FOOT-LOCK SPEED (T12_10, coordinator ruling 2026-09-30): speed_m_s is the ground speed
	that pins a planted foot, measured on the clip's own keys (nb_d2/scripts/57_footlock.py). The
	NET / STEPPING pair it replaced is still read if an older manifest carries it (stepping first)."""
'''),
    ('''		var v = (e as Dictionary).get("stepping_speed_m_s", (e as Dictionary).get("speed_m_s", null))
		if v == null:
			continue
		out[String(name)] = float(v) * PPM
''',
     '''		var v = (e as Dictionary).get("stepping_speed_m_s", (e as Dictionary).get("speed_m_s", null))
		if v == null:
			continue
		# STATED AT THE REFERENCE SCALE, like every other px/s here (walk_px_s, run_px_s, clip_px_s):
		# clip_px_s() rescales by _figure_scale / speed_measured_at_scale. PPM alone is figure scale 1.0,
		# which drove every manifest-priced clip at 0.799 of its speed (T12_10, tools/strafe_probe.gd).
		var at_ref: float = float(cfg.get("speed_measured_at_scale", 1.0))
		out[String(name)] = float(v) * PPM * (at_ref if at_ref > 0.0 else 1.0)
'''),
]
for a, b in REP:
    n = s.count(a)
    if n != 1:
        sys.exit("REFUSED: anchor matched %d times: %r" % (n, a[:80]))
    s = s.replace(a, b)
open(dst, 'w').write(s)
print("patched %s -> %s" % (src, dst))
