"""THE DECLARED-SET FILTER for knight.gd's axe guard layer -- a layer's filter is the bone set it
DECLARES, and a bone its pose clip does not key blends to REST (coordinator ruling 2026-09-30).

Godot's glTF importer drops a track whose every key equals the bone's rest (remove_immutable_tracks).
The guard poses key the wrist AT REST on purpose -- RightHand neutral, so the haft stays in the fist's
channel -- so axe_guard_R (and its block, bash and chop variants) arrive with three tracks, not four.
_apply_axe_guard took its filter paths from the pose clip's OWN tracks, so the Blend2 never filtered
RightHand: under the guard layer the wrist followed the base clip (walk_armed's, a strafe's, the
block's). The D2 JOIN lane found it in its renderer (sword tilt 11-32 deg where 40-58 was designed).

The fix takes the filter paths for the declared bones from ANY clip that keys them -- the way
_apply_strike_release already builds its release filter -- so every declared bone is filtered, and a
bone the pose lacks goes to its rest, which is what the pose means. knight.gd's shield_carry_L layer
has the same drop (LeftShoulder and LeftHand at rest) and is NOT changed here: this patch is the axe
guard only, the layer the T12 gate measures.

    python3 declared_filter_patch.py <knight.gd in> <knight.gd out>

Refusing: every anchor must match once."""
import sys

src, dst = sys.argv[1], sys.argv[2]
s = open(src).read()
REP = [
    ('''	"""Point the layer at its clip and filter it to the spec's bones, the paths taken from the
	clip's OWN tracks (a bone the clip does not key cannot be filtered by accident)."""''',
     '''	"""Point the layer at its clip and filter it to the spec's DECLARED bones, the paths taken from
	any clip that keys them (T12_10, the coordinator's ruling: a layer's filter is its declared set).
	The importer drops a track equal to the rest pose -- the guard's neutral wrist -- so a filter taken
	from the pose clip's own tracks left RightHand to the base clip; filtered, a bone the pose does not
	key blends to its rest, which is the pose's intent."""'''),
    ('''		var want: Array = spec.get("bones", [])
		for c in [action, ab]:
			var ca := _anim.get_animation(c)
			for i in ca.get_track_count():
				var pth: NodePath = ca.track_get_path(i)
				var on: bool = want.has(String(pth.get_concatenated_subnames()))
				b2.set_filter_path(pth, on)
				if on and c == action:
					filtered += 1''',
     '''		var want: Array = spec.get("bones", [])
		var seen := {}
		for c in _anim.get_animation_list():
			var ca := _anim.get_animation(c)
			for i in ca.get_track_count():
				var pth: NodePath = ca.track_get_path(i)
				if want.has(String(pth.get_concatenated_subnames())) and not seen.has(String(pth)):
					seen[String(pth)] = true
					b2.set_filter_path(pth, true)
					filtered += 1'''),
]
for a, b in REP:
    n = s.count(a)
    if n != 1:
        sys.exit("REFUSED: anchor matched %d times: %r" % (n, a[:80]))
    s = s.replace(a, b)
open(dst, 'w').write(s)
print("patched %s -> %s" % (src, dst))
