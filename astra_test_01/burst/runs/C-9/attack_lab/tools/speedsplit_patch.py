"""THE ARMED-SPEED SPLIT for knight.gd (Matt: "even the run speed slows way down when I put on the
axe/shield"). The legs, hips and root come from the gait clips the ROLES name -- which for the
armed set become the UNARMED walk and run, so ground speed does not change with the gear -- and
the spine and both arms come from an armed UPPER layer: `upper_armed` in character.json names the
armed gait clips and the bones. The upper clips run on the SAME locked cycle length as the legs'
(the sync group's time scales) and are phase-aligned at left-toe contact while weightless, the
way the run is already aligned to the walk. A filtered Blend2 between the gait blend and the
strafe: the strafe, the shield guard, the block and the strikes still own what they own.
No `upper_armed` block -> the layer runs at zero and nothing changes.

    python3 speedsplit_patch.py <knight.gd in> <knight.gd out>

Surgical and refusing: each anchor must match exactly once, or nothing is written."""
import sys

src, dst = sys.argv[1], sys.argv[2]
t = open(src).read()

EDITS = [
    # ---- state -------------------------------------------------------------------------
    ("var _prev_w := 0.0\n",
     "var _prev_w := 0.0\n"
     "## THE ARMED UPPER LAYER (armed-speed split) -- see _upper_spec\n"
     "var _upper_on := false\n"
     "var _walk_len_u := 1.0\n"
     "var _run_len_u := 1.0\n"
     "var _walk_contact_u := 0.0\n"
     "var _run_contact_u := 0.0\n"
     "var _prev_a := 0.0\n"),
    # ---- the upper chain, built beside the gait chain ----------------------------------
    ("\tbt.connect_node(\"bl_wr\", 1, \"seek_run\")\n",
     "\tbt.connect_node(\"bl_wr\", 1, \"seek_run\")\n"
     "\t# THE ARMED UPPER BODY: the same idle/walk/run blend, on the armed gait clips, locked to\n"
     "\t# the legs' cycle by its own time scales and seeks. `up` takes the spine and arms from it.\n"
     "\tvar a_idle_u := AnimationNodeAnimation.new()\n"
     "\ta_idle_u.animation = a_idle.animation\n"
     "\tvar a_walk_u := AnimationNodeAnimation.new()\n"
     "\ta_walk_u.animation = a_walk.animation\n"
     "\tvar a_run_u := AnimationNodeAnimation.new()\n"
     "\ta_run_u.animation = a_run.animation\n"
     "\tvar ts_walk_u := AnimationNodeTimeScale.new()\n"
     "\tvar ts_run_u := AnimationNodeTimeScale.new()\n"
     "\tvar seek_walk_u := AnimationNodeTimeSeek.new()\n"
     "\tvar seek_run_u := AnimationNodeTimeSeek.new()\n"
     "\tvar bl_iw_u := AnimationNodeBlend2.new()\n"
     "\tvar bl_wr_u := AnimationNodeBlend2.new()\n"
     "\tbl_iw_u.sync = true\n"
     "\tbl_wr_u.sync = true\n"
     "\tvar up := AnimationNodeBlend2.new()\n"
     "\tup.filter_enabled = true\n"
     "\t# SYNCED: the upper chain advances even at zero weight, so its idle keeps the legs' idle's\n"
     "\t# time. idle_armed is NOT a seamless loop (its wrap snaps Spine02 34.6 deg, LeftArm 78) and\n"
     "\t# two copies wrapping at different moments would pop twice per loop instead of once.\n"
     "\tup.sync = true\n"
     "\tbt.add_node(\"a_idle_u\", a_idle_u, Vector2(0, -420))\n"
     "\tbt.add_node(\"a_walk_u\", a_walk_u, Vector2(0, -340))\n"
     "\tbt.add_node(\"a_run_u\", a_run_u, Vector2(0, -260))\n"
     "\tbt.add_node(\"ts_walk_u\", ts_walk_u, Vector2(180, -340))\n"
     "\tbt.add_node(\"ts_run_u\", ts_run_u, Vector2(180, -260))\n"
     "\tbt.add_node(\"seek_walk_u\", seek_walk_u, Vector2(300, -340))\n"
     "\tbt.add_node(\"seek_run_u\", seek_run_u, Vector2(300, -260))\n"
     "\tbt.add_node(\"bl_iw_u\", bl_iw_u, Vector2(430, -380))\n"
     "\tbt.add_node(\"bl_wr_u\", bl_wr_u, Vector2(560, -320))\n"
     "\tbt.add_node(\"up\", up, Vector2(620, -120))\n"
     "\tbt.connect_node(\"ts_walk_u\", 0, \"a_walk_u\")\n"
     "\tbt.connect_node(\"seek_walk_u\", 0, \"ts_walk_u\")\n"
     "\tbt.connect_node(\"ts_run_u\", 0, \"a_run_u\")\n"
     "\tbt.connect_node(\"seek_run_u\", 0, \"ts_run_u\")\n"
     "\tbt.connect_node(\"bl_iw_u\", 0, \"a_idle_u\")\n"
     "\tbt.connect_node(\"bl_iw_u\", 1, \"seek_walk_u\")\n"
     "\tbt.connect_node(\"bl_wr_u\", 0, \"bl_iw_u\")\n"
     "\tbt.connect_node(\"bl_wr_u\", 1, \"seek_run_u\")\n"
     "\tbt.connect_node(\"up\", 0, \"bl_wr\")\n"
     "\tbt.connect_node(\"up\", 1, \"bl_wr_u\")\n"),
    ("\tbt.connect_node(\"strf\", 0, \"bl_wr\")\n",
     "\tbt.connect_node(\"strf\", 0, \"up\")\n"),
    # ---- per frame: the same weights, the same cycle, alignment only while weightless ----
    ("\t_tree.set(\"parameters/bl_wr/blend_amount\", w)\n",
     "\t_tree.set(\"parameters/bl_wr/blend_amount\", w)\n"
     "\t_tree.set(\"parameters/bl_iw_u/blend_amount\", a)\n"
     "\t_tree.set(\"parameters/bl_wr_u/blend_amount\", w)\n"
     "\t_tree.set(\"parameters/up/blend_amount\", 1.0 if _upper_on else 0.0)\n"
     "\t# the upper walk is aligned to the legs' walk only while it is weightless (standing), the\n"
     "\t# upper run only while the run is (as the legs' run is): a seek under weight is a teleport\n"
     "\tif _upper_on and sync_group and a <= 0.0 and _prev_a <= 0.0:\n"
     "\t\t_align_upper(\"walk\")\n"
     "\t_prev_a = a\n"),
    ("\tif w <= 0.0 and _prev_w <= 0.0 and sync_group:\n\t\talign_phase()\n",
     "\tif w <= 0.0 and _prev_w <= 0.0 and sync_group:\n\t\talign_phase()\n"
     "\t\tif _upper_on:\n"
     "\t\t\t_align_upper(\"run\")\n"),
    ("\t\t_tree.set(\"parameters/ts_run/scale\", 1.0)\n\t\treturn\n",
     "\t\t_tree.set(\"parameters/ts_run/scale\", 1.0)\n"
     "\t\t_tree.set(\"parameters/ts_walk_u/scale\", 1.0)\n"
     "\t\t_tree.set(\"parameters/ts_run_u/scale\", 1.0)\n"
     "\t\treturn\n"),
    ("\t_tree.set(\"parameters/ts_run/scale\", _run_len / maxf(blended, 1e-6))\n",
     "\t_tree.set(\"parameters/ts_run/scale\", _run_len / maxf(blended, 1e-6))\n"
     "\t# THE UPPER CLIPS ON THE LEGS' CYCLE: each completes one cycle in the same `blended`\n"
     "\t# seconds, so their phase against the legs is constant once aligned\n"
     "\t_tree.set(\"parameters/ts_walk_u/scale\", _walk_len_u / maxf(blended, 1e-6))\n"
     "\t_tree.set(\"parameters/ts_run_u/scale\", _run_len_u / maxf(blended, 1e-6))\n"),
    # ---- the clip set: point the upper chain, filter it, measure it --------------------
    ("\t_point_strafe()\n\t_block_marks()\n\talign_phase()\n",
     "\t_point_strafe()\n\t_block_marks()\n\talign_phase()\n"
     "\t_apply_upper()\n"),
    # ---- helpers ----------------------------------------------------------------------
    ("func speed_px_s() -> float:\n",
     "func _upper_spec() -> Dictionary:\n"
     "\t\"\"\"`upper_armed` in character.json: the ARMED gait clips whose spine and arms ride over the\n"
     "\tunarmed legs, and the bones they own. Absent, or unarmed -> the layer runs at zero.\"\"\"\n"
     "\tif not _armed:\n"
     "\t\treturn {}\n"
     "\tvar s = cfg.get(\"upper_armed\", {})\n"
     "\treturn s if s is Dictionary else {}\n"
     "\n"
     "\n"
     "func _apply_upper() -> void:\n"
     "\t\"\"\"Point the upper chain at the armed gait clips, filter `up` to the spec's bones (paths\n"
     "\ttaken from the clips' OWN tracks), and derive the lengths and contact phases the per-frame\n"
     "\tcode locks and aligns against. Unarmed, the chain mirrors the legs' clips at weight zero.\"\"\"\n"
     "\tif _tree == null or _anim == null:\n"
     "\t\treturn\n"
     "\tvar bt := _tree.tree_root as AnimationNodeBlendTree\n"
     "\tif bt == null or not bt.has_node(\"up\"):\n"
     "\t\treturn\n"
     "\tvar spec := _upper_spec()\n"
     "\tvar uw := String(spec.get(\"walk\", \"\"))\n"
     "\tvar ur := String(spec.get(\"run\", \"\"))\n"
     "\t_upper_on = _clip_len.has(uw) and _clip_len.has(ur)\n"
     "\tvar idle_c := String(_roles.get(\"idle\", \"idle\"))\n"
     "\tvar walk_c := uw if _upper_on else String(_roles.get(\"walk\", \"walk\"))\n"
     "\tvar run_c := ur if _upper_on else String(_roles.get(\"run\", \"run\"))\n"
     "\t(bt.get_node(\"a_idle_u\") as AnimationNodeAnimation).animation = idle_c\n"
     "\t(bt.get_node(\"a_walk_u\") as AnimationNodeAnimation).animation = walk_c\n"
     "\t(bt.get_node(\"a_run_u\") as AnimationNodeAnimation).animation = run_c\n"
     "\tfor c in [walk_c, run_c]:\n"
     "\t\tif _clip_len.has(c):\n"
     "\t\t\t_anim.get_animation(c).loop_mode = Animation.LOOP_LINEAR\n"
     "\tvar want: Array = spec.get(\"bones\", [])\n"
     "\tvar up := bt.get_node(\"up\") as AnimationNodeBlend2\n"
     "\tvar filtered := 0\n"
     "\tfor c in [idle_c, walk_c, run_c]:\n"
     "\t\tif not _clip_len.has(c):\n"
     "\t\t\tcontinue\n"
     "\t\tvar an := _anim.get_animation(c)\n"
     "\t\tfor i in an.get_track_count():\n"
     "\t\t\tvar pth: NodePath = an.track_get_path(i)\n"
     "\t\t\tvar on: bool = _upper_on and want.has(String(pth.get_concatenated_subnames()))\n"
     "\t\t\tup.set_filter_path(pth, on)\n"
     "\t\t\tif on and c == walk_c:\n"
     "\t\t\t\tfiltered += 1\n"
     "\t_walk_len_u = float(_clip_len.get(walk_c, 1.0))\n"
     "\t_run_len_u = float(_clip_len.get(run_c, 1.0))\n"
     "\t_walk_contact_u = _contact_phase(walk_c)\n"
     "\t_run_contact_u = _contact_phase(run_c)\n"
     "\t_tree.set(\"parameters/up/blend_amount\", 1.0 if _upper_on else 0.0)\n"
     "\tif _upper_on:\n"
     "\t\t_align_upper(\"walk\")\n"
     "\t\t_align_upper(\"run\")\n"
     "\tprint(\"upper layer: %s | walk '%s' (%.4f s, contact %.3f) run '%s' (%.4f s, contact %.3f) | %d tracks on %d bones\"\n"
     "\t\t% [\"ON\" if _upper_on else \"off\", walk_c, _walk_len_u, _walk_contact_u, run_c, _run_len_u,\n"
     "\t\t   _run_contact_u, filtered, want.size()])\n"
     "\n"
     "\n"
     "func _align_upper(which: String) -> void:\n"
     "\t\"\"\"Seek an upper clip so its left-toe contact lands on the LEGS' walk contact -- the same\n"
     "\trule align_phase uses for the legs' run, so all four clips share one contact instant.\"\"\"\n"
     "\tif _tree == null:\n"
     "\t\treturn\n"
     "\tvar wl: float = maxf(_walk_len, 1e-6)\n"
     "\tvar wp: float = fmod(maxf(float(_tree.get(\"parameters/a_walk/current_position\")), 0.0), wl) / wl\n"
     "\tif which == \"walk\":\n"
     "\t\t_tree.set(\"parameters/seek_walk_u/seek_request\", fposmod(wp - _walk_contact + _walk_contact_u, 1.0) * _walk_len_u)\n"
     "\telse:\n"
     "\t\t_tree.set(\"parameters/seek_run_u/seek_request\", fposmod(wp - _walk_contact + _run_contact_u, 1.0) * _run_len_u)\n"
     "\n"
     "\n"
     "func speed_px_s() -> float:\n"),
]
for old, new in EDITS:
    n = t.count(old)
    if n != 1:
        sys.exit("REFUSED: anchor found %d times, want exactly 1:\n%s" % (n, old))
    t = t.replace(old, new)
open(dst, "w").write(t)
print("wrote %s (%d edits)" % (dst, len(EDITS)))
