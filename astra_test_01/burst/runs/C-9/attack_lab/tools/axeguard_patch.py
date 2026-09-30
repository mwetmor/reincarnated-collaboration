"""THE AXE ARM'S GUARD LAYER for knight.gd -- the shield's recipe for the right arm.

`arm_layer_armed_R` in character.json names the clip (axe_guard_R: the right arm's guard pose,
authored by IK), the bones it owns and the WEIGHT it is laid on with. A filtered Blend2 ABOVE the
block and BELOW the strikes: it holds the axe arm over the idle, the locomotion, the strafes and
the block (where the shield arm blocks and the axe arm stays at guard), and a slash, chop or bash
owns the arm outright while it runs, fading back to the guard on its own fade-out. At a weight
below 1 the arm keeps part of its own motion; weapon_r (keyed per clip) finishes the angle.
No `arm_layer_armed_R` block -> the layer runs at zero and nothing changes.

    python3 axeguard_patch.py <knight.gd in> <knight.gd out>

Refusing: every anchor must match exactly once."""
import sys

src, dst = sys.argv[1], sys.argv[2]
t = open(src).read()

EDITS = [
    ('\t\t_tree.set("parameters/blk/blend_amount", _block_w)\n',
     '\t\t_tree.set("parameters/blk/blend_amount", _block_w)\n'
     '\t\t_tree.set("parameters/gsel/blend_amount", clampf(_block_w, 0.0, 1.0))\n'
     '\t\t_tree.set("parameters/blend_r/blend_amount", _axe_guard_weight())\n'),
    ('\tvar prev := "blk"\n',
     '\t# THE AXE ARM\'S GUARD: above the block, below the strikes (see _apply_axe_guard)\n'
     '\tvar guard_r := AnimationNodeAnimation.new()\n'
     '\tguard_r.animation = action\n'
     '\t# the BLOCK has its own guard: it turns his torso ~50 deg to present the shield, and a pose\n'
     '\t# held relative to the chest would turn the axe out of guard with it. gsel follows the block.\n'
     '\tvar guard_rb := AnimationNodeAnimation.new()\n'
     '\tguard_rb.animation = action\n'
     '\tvar gsel := AnimationNodeBlend2.new()\n'
     '\tvar blend_r := AnimationNodeBlend2.new()\n'
     '\tblend_r.filter_enabled = true\n'
     '\tbt.add_node("guard_r", guard_r, Vector2(900, 300))\n'
     '\tbt.add_node("guard_rb", guard_rb, Vector2(900, 380))\n'
     '\tbt.add_node("gsel", gsel, Vector2(940, 260))\n'
     '\tbt.add_node("blend_r", blend_r, Vector2(960, 100))\n'
     '\tbt.connect_node("gsel", 0, "guard_r")\n'
     '\tbt.connect_node("gsel", 1, "guard_rb")\n'
     '\tbt.connect_node("blend_r", 0, "blk")\n'
     '\tbt.connect_node("blend_r", 1, "gsel")\n'
     '\tvar prev := "blend_r"\n'),
    ('\t_apply_upper()\n',
     '\t_apply_upper()\n'
     '\t_apply_axe_guard()\n'),
    ('\tif armed() != was:\n\t\t_apply_clip_set()\n\tif _tree != null:\n\t\t_tree.set("parameters/blend/blend_amount", _layer_weight(_clip))\n',
     '\tif armed() != was:\n\t\t_apply_clip_set()\n\tif _tree != null:\n\t\t_tree.set("parameters/blend/blend_amount", _layer_weight(_clip))\n'
     '\t\t_tree.set("parameters/blend_r/blend_amount", _axe_guard_weight())\n'),
    ('func _upper_spec() -> Dictionary:\n',
     'func _axe_guard_spec() -> Dictionary:\n'
     '\tvar s = cfg.get("arm_layer_armed_R", {})\n'
     '\treturn s if s is Dictionary else {}\n'
     '\n'
     '\n'
     'func _axe_guard_weight() -> float:\n'
     '\t"""The layer\'s weight while the axe is carried, blended toward `weight_block` by the block\n'
     '\tweight -- data, swept in the lab -- else 0."""\n'
     '\tvar spec := _axe_guard_spec()\n'
     '\tif not _armed or not _clip_len.has(String(spec.get("action", ""))):\n'
     '\t\treturn 0.0\n'
     '\tvar w: float = clampf(float(spec.get("weight", 1.0)), 0.0, 1.0)\n'
     '\tvar wb: float = clampf(float(spec.get("weight_block", w)), 0.0, 1.0)\n'
     '\treturn lerpf(w, wb, clampf(_block_w, 0.0, 1.0))\n'
     '\n'
     '\n'
     'func _apply_axe_guard() -> void:\n'
     '\t"""Point the layer at its clip and filter it to the spec\'s bones, the paths taken from the\n'
     '\tclip\'s OWN tracks (a bone the clip does not key cannot be filtered by accident)."""\n'
     '\tif _tree == null or _anim == null:\n'
     '\t\treturn\n'
     '\tvar bt := _tree.tree_root as AnimationTreeBlendTreeCast if false else _tree.tree_root as AnimationNodeBlendTree\n'
     '\tif bt == null or not bt.has_node("blend_r"):\n'
     '\t\treturn\n'
     '\tvar spec := _axe_guard_spec()\n'
     '\tvar action := String(spec.get("action", ""))\n'
     '\tvar b2 := bt.get_node("blend_r") as AnimationNodeBlend2\n'
     '\tvar filtered := 0\n'
     '\tif _clip_len.has(action):\n'
     '\t\tvar ab := String(spec.get("action_block", ""))\n'
     '\t\tif not _clip_len.has(ab):\n'
     '\t\t\tab = action\n'
     '\t\t(bt.get_node("guard_r") as AnimationNodeAnimation).animation = action\n'
     '\t\t(bt.get_node("guard_rb") as AnimationNodeAnimation).animation = ab\n'
     '\t\tvar want: Array = spec.get("bones", [])\n'
     '\t\tfor c in [action, ab]:\n'
     '\t\t\tvar ca := _anim.get_animation(c)\n'
     '\t\t\tfor i in ca.get_track_count():\n'
     '\t\t\t\tvar pth: NodePath = ca.track_get_path(i)\n'
     '\t\t\t\tvar on: bool = want.has(String(pth.get_concatenated_subnames()))\n'
     '\t\t\t\tb2.set_filter_path(pth, on)\n'
     '\t\t\t\tif on and c == action:\n'
     '\t\t\t\t\tfiltered += 1\n'
     '\t_tree.set("parameters/blend_r/blend_amount", _axe_guard_weight())\n'
     '\tprint("axe guard layer: \'%s\' at weight %.2f, %d tracks" % [action, _axe_guard_weight(), filtered])\n'
     '\n'
     '\n'
     'func _upper_spec() -> Dictionary:\n'),
]
for old, new in EDITS:
    n = t.count(old)
    if n != 1:
        sys.exit("REFUSED: anchor found %d times, want exactly 1:\n%s" % (n, old))
    t = t.replace(old, new)
t = t.replace('\tvar bt := _tree.tree_root as AnimationTreeBlendTreeCast if false else _tree.tree_root as AnimationNodeBlendTree\n',
              '\tvar bt := _tree.tree_root as AnimationNodeBlendTree\n')
open(dst, "w").write(t)
print("wrote %s (%d edits)" % (dst, len(EDITS)))
