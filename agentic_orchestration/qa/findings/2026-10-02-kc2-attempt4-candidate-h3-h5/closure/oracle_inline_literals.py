"""jack-ryan H-5: AST census of INLINE numeric literals (not module-level bindings) in the v3.8-v3.11 fold modules of
the oracle of record — the class the closure law cannot see (prereg 92cc5350 § 1.6). Trivial values excluded."""
import ast, sys, os
K = sys.argv[1]
MODS = ["gd_engagement", "gd_reposition", "swing_pause", "pilot_move", "mutators", "referent_lineup", "gd_composition",
        "initial_self_cast", "p05_emergence", "gd_fire_range", "stationary", "global_magnitude", "hunt_pilot"]
TRIV = {0, 1, 2, -1, 0.0, 1.0, 2.0, 0.5, -1.0}
for m in MODS:
    p = os.path.join(K, m + ".py")
    if not os.path.exists(p): continue
    src = open(p, encoding="utf-8").read(); tree = ast.parse(src)
    top = {id(n) for n in tree.body}
    mod_level_lines = set()
    for n in tree.body:
        if isinstance(n, (ast.Assign, ast.AnnAssign)):
            mod_level_lines.update(range(n.lineno, (n.end_lineno or n.lineno) + 1))
    lines = src.split("\n")
    for node in ast.walk(tree):
        if isinstance(node, ast.Constant) and type(node.value) in (int, float) and not isinstance(node.value, bool):
            v = node.value
            if v in TRIV or node.lineno in mod_level_lines: continue
            print(f"{m}.py:{node.lineno}\t{v!r}\t{lines[node.lineno-1].strip()[:140]}")
