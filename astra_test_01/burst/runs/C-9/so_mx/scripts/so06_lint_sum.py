# so_mx: summarise a j_joint_lint json per clip from its WORST values against the lint's own limits (elbow -5..150, knee
# -5..155, wrist |flex| <= 80, |dev| <= 40): every joint measure out of range, with its worst degree and time.  so06_lint_sum.py <json>
import json, sys
d = json.load(open(sys.argv[1]))
for k, v in list(d['moves'].items()) + list(d.get('control_library', {}).items()):
    w = v['worst']; out = []
    for j in ('elbow_R', 'elbow_L', 'knee_R', 'knee_L'):
        lo, hi = (-5, 150) if j.startswith('elbow') else (-5, 155)
        if w[j]['flex_min']['deg'] < lo: out.append("%s hyperext %.1f@%.2f" % (j, w[j]['flex_min']['deg'], w[j]['flex_min']['t']))
        if w[j]['flex_max']['deg'] > hi: out.append("%s overbend %.1f" % (j, w[j]['flex_max']['deg']))
    for j in ('wrist_R', 'wrist_L'):
        if abs(w[j]['flex_worst']['deg']) > 80: out.append("%s flex %.1f@%.2f" % (j, w[j]['flex_worst']['deg'], w[j]['flex_worst']['t']))
        if abs(w[j]['dev_worst']['deg']) > 40: out.append("%s dev %.1f@%.2f" % (j, w[j]['dev_worst']['deg'], w[j]['dev_worst']['t']))
    print("%-16s %-4s %s" % (k, v['verdict'], "; ".join(out) or "-"))
