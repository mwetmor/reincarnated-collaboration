"""Set the cliffside3d project's stretch so both apps show the planned 16:9 view on any screen:
window/stretch/mode = canvas_items, window/stretch/aspect = keep, base 1920x1080.

Surgical: only the [display] section is touched, and only these keys. It REFUSES if the section
is not what it was when this was written (only the two base-size keys, 1920 and 1080) -- a key
someone else set is reported, not overwritten. Prints the before and after values.
    python3 display_stretch.py <project.godot> [--check]"""
import re, sys
p = sys.argv[1]
check_only = "--check" in sys.argv
t = open(p).read()
m = re.search(r"(?ms)^\[display\]\n(.*?)(?=^\[|\Z)", t)
assert m, "no [display] section"
body = m.group(1)
keys = dict(re.findall(r'(?m)^([A-Za-z0-9_/]+)=(.*)$', body))
print("BEFORE [display]: %s" % (keys or "{}"))
for k, v in (("window/stretch/mode", "disabled (Godot default: key absent)"), ("window/stretch/aspect", "keep (Godot default: key absent)")):
    print("   %-26s %s" % (k, keys.get(k, v)))
expected = {"window/size/viewport_width": "1920", "window/size/viewport_height": "1080"}
if keys != expected:
    print("REFUSED: [display] is not what the change was written against; expected exactly %s" % expected)
    sys.exit(2)
if check_only:
    print("check only: unchanged since planned, would apply")
    sys.exit(0)
new_body = body.rstrip("\n") + '\nwindow/stretch/mode="canvas_items"\nwindow/stretch/aspect="keep"\n\n'
t2 = t[:m.start(1)] + new_body + t[m.end(1):]
open(p + ".tmp_stretch", "w").write(t2)
import os
os.replace(p + ".tmp_stretch", p)
keys2 = dict(re.findall(r'(?m)^([A-Za-z0-9_/]+)=(.*)$', re.search(r"(?ms)^\[display\]\n(.*?)(?=^\[|\Z)", open(p).read()).group(1)))
print("AFTER  [display]: %s" % keys2)
