"""THE RECOVERY RELEASE for knight.gd -- every strike gives the axe arm back at its swing end.

A strike is a one-shot that owns every bone for the clip's whole length. After its ACTIVE SWING
(the frames contiguous with the axe head's peak speed at >= 50% of it -- the weapon gate's
definition) the clip's follow-through keeps driving the arm, and with the axe seated in the fist
that follow-through is where the haft goes through his own body (the slash: his shield arm at
0.79-0.83 s). The rule: from the end of the swing, the arm blends to the GUARD over `over_s`,
eased, inside the one-shot -- so the one-shot's own fade-out that follows starts from a strike
whose arm is already at guard.

`strike_release` in character.json names the pose (axe_guard_R), the bones it takes back (the
right arm and weapon_r; a filtered bone the pose does not key blends to its rest, which for
weapon_r is the mount) and, per CLIP, the swing end `at_s` -- measured on the clip by
tools/guard_accept.gd, the gate's own instrument. A clip in `guard_throughout` never takes the
axe arm at all (the shield bash: its swing is the shield's). A strike whose clip is in neither
keeps its arm throughout; no `strike_release` block -> nothing changes.

THE POSE IS PLAYED AS A CLIP OF THE STRIKE'S OWN LENGTH, synced. A Blend2 reports the time left
of whichever input weighs more than half, and the one-shot ends when that runs out: with the
pose's own 1-frame clip the slash's one-shot ended the moment the release passed 0.5 (measured:
at 0.79 s of 1.50). So each strike gets a copy of the pose held for its length, and the release
Blend2 is synced so the two advance together from the fire.

    python3 strike_release_patch.py <knight.gd in> <knight.gd out>

Applied over the axe-guard patch (axeguard_patch.py). Refusing: every anchor must match once."""
import sys

src, dst = sys.argv[1], sys.argv[2]
t = open(src).read()

EDITS = [
    # the fire flag
    ('var _strike_out_sent := false\n',
     'var _strike_out_sent := false\n'
     'var _rel_fire := {}             # strike key -> fired this frame (the clip position is stale until the tree runs)\n'),
    ('\t\t_tree.set("parameters/%s/request" % node, AnimationNodeOneShot.ONE_SHOT_REQUEST_FIRE)\n',
     '\t\t_tree.set("parameters/%s/request" % node, AnimationNodeOneShot.ONE_SHOT_REQUEST_FIRE)\n'
     '\t\t_rel_fire[which] = true\n'),
    # the nodes: rel_<key> between the strike clip and its one-shot
    ('\t\tvar an := AnimationNodeAnimation.new()\n'
     '\t\tan.animation = clip\n'
     '\t\tvar os_n := AnimationNodeOneShot.new()\n'
     '\t\tos_n.fadein_time = fin\n'
     '\t\tos_n.fadeout_time = fout\n'
     '\t\tbt.add_node("a_" + key, an, Vector2(x, 280))\n'
     '\t\tbt.add_node("os_" + key, os_n, Vector2(x, 100))\n'
     '\t\tbt.connect_node("os_" + key, 0, prev)\n'
     '\t\tbt.connect_node("os_" + key, 1, "a_" + key)\n',
     '\t\tvar an := AnimationNodeAnimation.new()\n'
     '\t\tan.animation = clip\n'
     '\t\t# THE RECOVERY RELEASE (see _release_tick): rel_<key> hands the axe arm back to the guard\n'
     '\t\t# after the strike\'s active swing. It sits INSIDE the one-shot, so the fade-out that\n'
     '\t\t# follows starts from a strike whose arm is already at guard.\n'
     '\t\tvar g_n := AnimationNodeAnimation.new()\n'
     '\t\tvar rp := String(_release_spec().get("pose", ""))\n'
     '\t\tg_n.animation = rp if _clip_len.has(rp) else clip\n'
     '\t\tvar rel := AnimationNodeBlend2.new()\n'
     '\t\trel.filter_enabled = true\n'
     '\t\t# SYNCED: the held pose advances with the strike, so its time left is the strike\'s\n'
     '\t\trel.sync = true\n'
     '\t\tvar os_n := AnimationNodeOneShot.new()\n'
     '\t\tos_n.fadein_time = fin\n'
     '\t\tos_n.fadeout_time = fout\n'
     '\t\tbt.add_node("a_" + key, an, Vector2(x, 280))\n'
     '\t\tbt.add_node("g_" + key, g_n, Vector2(x, 400))\n'
     '\t\tbt.add_node("rel_" + key, rel, Vector2(x, 190))\n'
     '\t\tbt.add_node("os_" + key, os_n, Vector2(x, 100))\n'
     '\t\tbt.connect_node("rel_" + key, 0, "a_" + key)\n'
     '\t\tbt.connect_node("rel_" + key, 1, "g_" + key)\n'
     '\t\tbt.connect_node("os_" + key, 0, prev)\n'
     '\t\tbt.connect_node("os_" + key, 1, "rel_" + key)\n'),
    # the filters, whenever the clip set is applied
    ('\t_apply_axe_guard()\n',
     '\t_apply_axe_guard()\n'
     '\t_apply_strike_release()\n'),
    # the per-frame weight
    ('\t\t_tree.set("parameters/strf/blend_amount", _strafe_w)\n',
     '\t\t_tree.set("parameters/strf/blend_amount", _strafe_w)\n'
     '\t\t_release_tick(dt)\n'),
    ('func _axe_guard_spec() -> Dictionary:\n',
     'func _release_spec() -> Dictionary:\n'
     '\tvar s = cfg.get("strike_release", {})\n'
     '\treturn s if s is Dictionary else {}\n'
     '\n'
     '\n'
     'func _apply_strike_release() -> void:\n'
     '\t"""Point each strike\'s release at the guard pose and filter it to the spec\'s bones, the paths\n'
     '\ttaken from whichever clips key them (weapon_r is keyed by the channel, not by the pose)."""\n'
     '\tif _tree == null or _anim == null:\n'
     '\t\treturn\n'
     '\tvar bt := _tree.tree_root as AnimationNodeBlendTree\n'
     '\tif bt == null:\n'
     '\t\treturn\n'
     '\tvar spec := _release_spec()\n'
     '\tvar pose := String(spec.get("pose", ""))\n'
     '\tvar want: Array = spec.get("bones", [])\n'
     '\tvar paths := {}\n'
     '\tfor an_name in _anim.get_animation_list():\n'
     '\t\tvar a := _anim.get_animation(an_name)\n'
     '\t\tfor i in a.get_track_count():\n'
     '\t\t\tvar pth: NodePath = a.track_get_path(i)\n'
     '\t\t\tif want.has(String(pth.get_concatenated_subnames())):\n'
     '\t\t\t\tpaths[String(pth)] = pth\n'
     '\tvar n_on := 0\n'
     '\tfor key in ["slash", "chop", "bash"]:\n'
     '\t\tif not bt.has_node("rel_" + key):\n'
     '\t\t\tcontinue\n'
     '\t\tvar clip := String((bt.get_node("a_" + key) as AnimationNodeAnimation).animation)\n'
     '\t\tvar held := _release_pose_for(clip, pose)\n'
     '\t\t(bt.get_node("g_" + key) as AnimationNodeAnimation).animation = held if held != "" else clip\n'
     '\t\tvar b2 := bt.get_node("rel_" + key) as AnimationNodeBlend2\n'
     '\t\tfor p in paths.values():\n'
     '\t\t\tb2.set_filter_path(p, _clip_len.has(pose))\n'
     '\t\t_tree.set("parameters/rel_%s/blend_amount" % key, 0.0)\n'
     '\t\tn_on += 1\n'
     '\tprint("strike release: pose \'%s\', %d bone paths, %d strikes, swing ends %s, over %.2f s, guard throughout %s"\n'
     '\t\t% [pose, paths.size(), n_on, JSON.stringify(spec.get("at_s", {})), float(spec.get("over_s", 0.08)),\n'
     '\t\t   JSON.stringify(spec.get("guard_throughout", []))])\n'
     '\n'
     '\n'
     'func _release_pose_for(clip: String, pose: String) -> String:\n'
     '\t"""The guard pose as a clip of the STRIKE\'s length (keys unchanged, so it holds the pose for\n'
     '\tthe whole strike): the release Blend2 then reports the strike\'s own time left."""\n'
     '\tif not _clip_len.has(pose) or not _clip_len.has(clip):\n'
     '\t\treturn ""\n'
     '\tvar nm := "%s__%s" % [pose, clip]\n'
     '\tif not _clip_len.has(nm):\n'
     '\t\tvar a := (_anim.get_animation(pose) as Animation).duplicate(true) as Animation\n'
     '\t\ta.length = float(_clip_len[clip])\n'
     '\t\ta.loop_mode = Animation.LOOP_NONE\n'
     '\t\t_anim.get_animation_library("").add_animation(nm, a)\n'
     '\t\t_clip_len[nm] = a.length\n'
     '\treturn nm\n'
     '\n'
     '\n'
     'func _release_tick(dt: float) -> void:\n'
     '\t"""THE RECOVERY RELEASE, per frame: each strike hands the axe arm back to the guard from the end\n'
     '\tof its active swing (`strike_release.at_s[clip]`) over `over_s`, eased. The weight is taken at\n'
     '\tthe position the clip WILL show after this step (current + dt): a release one frame late is an\n'
     '\tarm one frame late, and the slash\'s first penetrating frame is the first after its swing."""\n'
     '\tvar bt := _tree.tree_root as AnimationNodeBlendTree\n'
     '\tif bt == null:\n'
     '\t\treturn\n'
     '\tvar spec := _release_spec()\n'
     '\tvar at_map: Dictionary = spec.get("at_s", {})\n'
     '\tvar over: float = maxf(float(spec.get("over_s", 0.08)), 1e-3)\n'
     '\tfor key in ["slash", "chop", "bash"]:\n'
     '\t\tif not bt.has_node("rel_" + key):\n'
     '\t\t\tcontinue\n'
     '\t\tvar r := 0.0\n'
     '\t\tvar clip := String((bt.get_node("a_" + key) as AnimationNodeAnimation).animation)\n'
     '\t\tvar held: bool = (spec.get("guard_throughout", []) as Array).has(clip)\n'
     '\t\tif held and (bool(_rel_fire.get(key, false)) or bool(_tree.get("parameters/os_%s/active" % key))):\n'
     '\t\t\t_rel_fire[key] = false\n'
     '\t\t\tr = 1.0\n'
     '\t\telif at_map.has(clip):\n'
     '\t\t\tvar pos := -1.0\n'
     '\t\t\tif bool(_rel_fire.get(key, false)):\n'
     '\t\t\t\tpos = 0.0\n'
     '\t\t\t\t_rel_fire[key] = false\n'
     '\t\t\telif bool(_tree.get("parameters/os_%s/active" % key)):\n'
     '\t\t\t\tpos = float(_tree.get("parameters/a_%s/current_position" % key))\n'
     '\t\t\tif pos >= 0.0:\n'
     '\t\t\t\tvar a0 := float(at_map[clip])\n'
     '\t\t\t\tr = smoothstep(a0, a0 + over, pos + dt)\n'
     '\t\t_tree.set("parameters/rel_%s/blend_amount" % key, r)\n'
     '\n'
     '\n'
     'func _axe_guard_spec() -> Dictionary:\n'),
]
for old, new in EDITS:
    n = t.count(old)
    if n != 1:
        sys.exit("REFUSED: anchor found %d times, want exactly 1:\n%s" % (n, old))
    t = t.replace(old, new)
open(dst, "w").write(t)
print("wrote %s (%d edits)" % (dst, len(EDITS)))
