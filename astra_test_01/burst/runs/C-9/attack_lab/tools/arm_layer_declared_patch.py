"""THE DECLARED-SET FILTER for knight.gd's SHIELD ARM LAYER (T12_11) -- the same rule as the axe guard
(declared_filter_patch.py, T12_10): a layer's filter is the bone set it DECLARES; a bone its pose clip
does not key blends to rest.

The arm layer (character.json arm_layer_armed -> shield_guard_L in the running scene; arm_layer ->
shield_carry_L, retired: _layer_spec says it must not be in the running scene, and it is only selected
if a character file carries no arm_layer_armed) took its filter paths from the layer action's OWN
tracks, at two sites: the tree build (the Blend2 made once) and _apply (re-pointed at the live spec).
shield_carry_L keys LeftShoulder and LeftHand AT REST, so a runtime glTF import (GLTFDocument: the
JOIN renderer's path) drops those two tracks and the filter would leave them to the base clip.
shield_guard_L keys all four arm bones away from rest, so it keeps them either way -- which is why
nothing changes on screen today. This makes the filter independent of which tracks an import keeps.

    python3 arm_layer_declared_patch.py <knight.gd in> <knight.gd out>

Refusing: every anchor must match once."""
import sys

src, dst = sys.argv[1], sys.argv[2]
s = open(src).read()
REP = [
    # the build site
    ('''	var b2 := AnimationNodeBlend2.new()
	b2.filter_enabled = true
	var filtered := 0
	for i in ca.get_track_count():
		var pth: NodePath = ca.track_get_path(i)
		if want.has(String(pth.get_concatenated_subnames())):
			b2.set_filter_path(pth, true)
			filtered += 1
''',
     '''	var b2 := AnimationNodeBlend2.new()
	b2.filter_enabled = true
	var filtered := 0
	# THE DECLARED SET (T12_11): the paths for the spec's bones from ANY clip that keys them -- an
	# import may drop a pose's rest-valued track (shield_carry_L's shoulder and wrist); filtered, a
	# bone the pose does not key blends to its rest, which is what the pose means
	var seen_l := {}
	for cn in _anim.get_animation_list():
		var cl := _anim.get_animation(cn)
		for i in cl.get_track_count():
			var pth: NodePath = cl.track_get_path(i)
			if want.has(String(pth.get_concatenated_subnames())) and not seen_l.has(String(pth)):
				seen_l[String(pth)] = true
				b2.set_filter_path(pth, true)
				filtered += 1
'''),
    # the apply site
    ('''		var want: Array = spec.get("bones", [])
		var ca := _anim.get_animation(action)
		for i in ca.get_track_count():
			var pth: NodePath = ca.track_get_path(i)
			b2.set_filter_path(pth, want.has(String(pth.get_concatenated_subnames())))
''',
     '''		var want: Array = spec.get("bones", [])
		# THE DECLARED SET (T12_11), as at the build: every clip's paths, on for the spec's bones only
		for cn in _anim.get_animation_list():
			var cl := _anim.get_animation(cn)
			for i in cl.get_track_count():
				var pth: NodePath = cl.track_get_path(i)
				b2.set_filter_path(pth, want.has(String(pth.get_concatenated_subnames())))
'''),
]
for a, b in REP:
    n = s.count(a)
    if n != 1:
        sys.exit("REFUSED: anchor matched %d times: %r" % (n, a[:80]))
    s = s.replace(a, b)
open(dst, 'w').write(s)
print("patched %s -> %s" % (src, dst))
