"""THE RELEASE FROM THE SWING END (T12_11) for knight.gd's recovery release.

The recovery release (strike_release_patch.py) blends the axe arm from the STRIKE CLIP, which keeps
playing, to the guard: from at_s[clip] over over_s, smoothstep. That is right while the clip's
follow-through is harmless. The slash re-cut on its source's own keys (nbt_attack.glb) is not: its
follow-through drives the axe into his head and left shoulder 11 ms after the swing's last frame
(0.719 s at a 1/96 s step, 0.1 m deep by 0.74 s) -- faster than any eased release can take the arm
out of it (at_s 0.708, over 0.08: 228 axe points inside his head at 0.75 s).

A clip listed in strike_release.from_swing_end ({clip: over_s}) is released from its swing-end pose
HELD instead: the release clip (g_<key>) holds the strike's own pose at at_s for the release bones
and eases from it to the guard over that clip's over_s (smoothstep, keyed every 1/120 s); the
release weight is a step at the swing end. The clip's follow-through never reaches the arm. Every
other clip releases exactly as before (the chop, the bash: unchanged).

    python3 strike_hold_release_patch.py <knight.gd in> <knight.gd out>

Refusing: every anchor must match once."""
import sys

src, dst = sys.argv[1], sys.argv[2]
s = open(src).read()
REP = [
    # 1. _apply_strike_release: a from-swing-end clip gets the held-and-eased release clip
    ('''		var held := _release_pose_for(clip, String((spec.get("pose_for", {}) as Dictionary).get(clip, pose)))
		(bt.get_node("g_" + key) as AnimationNodeAnimation).animation = held if held != "" else clip
''',
     '''		var held := _release_pose_for(clip, String((spec.get("pose_for", {}) as Dictionary).get(clip, pose)))
		# FROM THE SWING END (T12_11): the release starts from the pose the swing ENDED in, held,
		# not from the clip's follow-through (see _release_hold_for)
		var fse: Dictionary = spec.get("from_swing_end", {})
		if held != "" and fse.has(clip) and (spec.get("at_s", {}) as Dictionary).has(clip):
			held = _release_hold_for(clip, held, float((spec["at_s"] as Dictionary)[clip]), float(fse[clip]), want)
			print("strike release: '%s' from its swing end HELD (%.3f s), eased to the guard over %.2f s" % [clip, float((spec["at_s"] as Dictionary)[clip]), float(fse[clip])])
		(bt.get_node("g_" + key) as AnimationNodeAnimation).animation = held if held != "" else clip
'''),
    # 2. the held-and-eased release clip, after _release_pose_for
    ('''func _release_tick(dt: float) -> void:
''',
     '''func _release_hold_for(clip: String, guard_nm: String, at_s: float, over: float, bones: Array) -> String:
	"""THE RELEASE FROM THE SWING END (T12_11): a clip of the strike's length whose release bones HOLD
	the strike's own pose at `at_s` (its swing's last frame) and ease from it to the guard over `over`
	(smoothstep, keyed every 1/120 s). With the release weight a step at the swing end, the arm shows
	the swing's last pose, then the ease: the clip's follow-through never reaches it. A bone the guard
	does not key (weapon_r: the channel keys it, the pose does not) eases to its rest, the mount, as
	the release Blend2 would take it."""
	var nm := "%s__from_%d_%d" % [guard_nm, int(round(at_s * 10000.0)), int(round(over * 10000.0))]
	if _clip_len.has(nm):
		return nm
	var sa := _anim.get_animation(clip)
	var ga := _anim.get_animation(guard_nm)
	var a := Animation.new()
	a.length = float(_clip_len[clip])
	a.loop_mode = Animation.LOOP_NONE
	var n_ease: int = maxi(2, int(ceil(over * 120.0)))
	for bn in bones:
		var bi := _skel.find_bone(String(bn))
		if bi < 0:
			continue
		var path := NodePath("")
		var ts := -1
		for i in sa.get_track_count():
			if sa.track_get_type(i) == Animation.TYPE_ROTATION_3D and String(sa.track_get_path(i).get_concatenated_subnames()) == String(bn):
				ts = i; path = sa.track_get_path(i)
		var tg := -1
		for i in ga.get_track_count():
			if ga.track_get_type(i) == Animation.TYPE_ROTATION_3D and String(ga.track_get_path(i).get_concatenated_subnames()) == String(bn):
				tg = i; path = ga.track_get_path(i) if path.is_empty() else path
		if ts < 0 and tg < 0:
			continue
		var rest_q: Quaternion = _skel.get_bone_rest(bi).basis.orthonormalized().get_rotation_quaternion()
		var p0: Quaternion = sa.rotation_track_interpolate(ts, at_s) if ts >= 0 else rest_q
		var g: Quaternion = ga.rotation_track_interpolate(tg, 0.0) if tg >= 0 else rest_q
		var ti := a.add_track(Animation.TYPE_ROTATION_3D)
		a.track_set_path(ti, path)
		a.track_set_interpolation_type(ti, Animation.INTERPOLATION_LINEAR)
		a.rotation_track_insert_key(ti, 0.0, p0)
		a.rotation_track_insert_key(ti, at_s, p0)
		for j in range(1, n_ease + 1):
			var u := float(j) / float(n_ease)
			var tj: float = minf(at_s + over * u, a.length)
			a.rotation_track_insert_key(ti, tj, p0.slerp(g, u * u * (3.0 - 2.0 * u)))
		if at_s + over < a.length:
			a.rotation_track_insert_key(ti, a.length, g)
	_anim.get_animation_library("").add_animation(nm, a)
	_clip_len[nm] = a.length
	return nm


func _release_tick(dt: float) -> void:
'''),
    # 3. _release_tick: the weight of a from-swing-end clip is a step (the ease is in its clip)
    ('''			if pos >= 0.0:
				var a0 := float(at_map[clip])
				r = smoothstep(a0, a0 + over, pos + dt)
''',
     '''			if pos >= 0.0:
				var a0 := float(at_map[clip])
				if (spec.get("from_swing_end", {}) as Dictionary).has(clip):
					# from the swing end (T12_11): the ease is in the release clip; the weight steps
					r = 1.0 if pos + dt >= a0 - 1e-4 else 0.0
				else:
					r = smoothstep(a0, a0 + over, pos + dt)
'''),
]
for a, b in REP:
    n = s.count(a)
    if n != 1:
        sys.exit("REFUSED: anchor matched %d times: %r" % (n, a[:80]))
    s = s.replace(a, b)
open(dst, 'w').write(s)
print("patched %s -> %s" % (src, dst))
