import glob, importlib.util, pathlib, shutil, subprocess, sys
S = pathlib.Path(sys.argv[1]); T = "/Users/admin/Games/reincarnated-engine/src/reincarnated/export/kc2_rulebook_pack_v5p1.py"
spec = importlib.util.spec_from_file_location("v51", T); M = importlib.util.module_from_spec(spec); sys.modules["v51"] = M; spec.loader.exec_module(M)
clean = pathlib.Path(glob.glob(str(S / "dry2" / "kc2-rulebook-pack-v5.1-*"))[0]); print("clean dry pack:", clean)
n = 0
for cfg in ("ORACLE", "PLAY", "join", "", None):
    fns = [("load_operands", lambda c: M.V0.load_operands(clean, config=c))] + \
          [(f"load_layer {mm}", (lambda mm_: (lambda c: M.load_layer(clean, mm_, config=c)))(mm)) for mm in (M.ANCHOR, M.KIT, M.HOOKS, M.WORLD)]
    for name, fn in fns:
        try:
            fn(cfg); print(f"NC-V51-e {name} {cfg!r} OPENED (FAIL)")
        except M.RulebookPackRefused as e:
            n += 1; print(f"NC-V51-e {name} {cfg!r} REFUSED: {e}")
print("NC-V51-e refused", n, "/ 25")
print("NC-V51-e JOIN physical_contact_table", M.load_layer(clean, M.ANCHOR, config="JOIN")["physical_contact_table"]["value"])
d = S / "nc_d_pack"
shutil.copytree(clean, d)
f = d / "tables" / "physical_contact_table.json"; b = bytearray(f.read_bytes()); i = b.index(b"1"); b[i] = ord("2"); f.write_bytes(bytes(b))
r = subprocess.run([sys.executable, T, "verify", str(d)], capture_output=True, text=True)
print(r.stdout[-1200:]); print("NC-V51-d verify rc", r.returncode)
try:
    M.load_layer(d, M.ANCHOR, config="JOIN"); print("NC-V51-d load_layer OPENED (FAIL)")
except M.RulebookPackRefused as e:
    print("NC-V51-d load_layer REFUSED:", e)
