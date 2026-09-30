# Write the scene's clip-selection rules into the manifest (gandalf, W1 item 3).
#
#   python3 scripts/34_manifest_rules.py <assemble_report.json>
#
# The rules are DATA, not prose in a commit message, because the scene drax
# reads the manifest and nobody reads a commit message twice.
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
rep = json.load(open(sys.argv[1])) if len(sys.argv) > 1 else {}
MP = os.path.join(ROOT, "export", "manifest.json")
m = json.load(open(MP))
clips = rep.get("lint", {}).get("clips", [])
m["clip_selection"] = dict(
    rule=("ARMED is the default for this character: he ships with an axe and a "
          "shield. The unarmed clips stay because the body has no gear welded to "
          "it and an unarmed barbarian is a real state, not a fallback."),
    armed=dict(
        idle="idle_armed", walk="walk_armed", run="run_armed",
        attack=["attack", "attack_chop"],
        block="block",
        left_arm_layer=("shield_guard_L while the shield is equipped -- on idle, "
                        "walk, run and block. NOT on the attacks: the attack "
                        "clips move the whole body and a static left-arm layer "
                        "fights them."),
        morphs="grip_R while the axe is equipped, grip_L while the shield is"),
    unarmed=dict(idle="idle", walk="walk", run="run", attack="attack",
                 left_arm_layer=None, morphs=None),
    superseded=dict(
        shield_carry_L=("kept for the scene already wired to it, but "
                        "shield_guard_L replaces it: carry only kept the disc "
                        "off his chest, guard holds it in front facing the "
                        "enemy, which is what a shield is for.")),
    available=clips)
if rep.get("shield"):
    m["shield_centre_grip"] = rep["shield"]
if rep.get("hygiene"):
    m["clip_hygiene_on_merge"] = rep["hygiene"]
json.dump(m, open(MP, "w"), indent=1)
print("manifest clip_selection written; clips: %s" % clips)

# THE MANIFEST LINT RUNS ON EVERY WRITE. The scene reads speeds from this file
# at load, so a stale number here is a shipped defect. One survived a
# correction because the fix was written into a new block and the old block was
# left saying something else.
import subprocess
_g = os.path.join(ROOT, "export", "nb-body.glb")
if os.path.exists(_g):
    _r = subprocess.run([sys.executable,
                         os.path.join(HERE, "48_manifest_lint.py"), MP, _g],
                        capture_output=True, text=True)
    print(_r.stdout.rstrip())
    assert _r.returncode == 0, "manifest disagrees with the GLB -- see above"
