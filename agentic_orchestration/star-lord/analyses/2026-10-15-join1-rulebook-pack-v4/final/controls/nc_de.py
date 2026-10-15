import glob, importlib.util, pathlib, shutil, subprocess, sys
S = pathlib.Path(sys.argv[1]); T = "/Users/admin/Games/reincarnated-engine/src/reincarnated/export/kc2_rulebook_pack_v4_final.py"
spec = importlib.util.spec_from_file_location("v4f", T); M = importlib.util.module_from_spec(spec); sys.modules["v4f"] = M; spec.loader.exec_module(M)
clean = pathlib.Path(glob.glob(str(S / "dry1" / "kc2-rulebook-pack-v4-*"))[0]); print("clean dry pack:", clean)
for cfg in ("ORACLE", "PLAY", "join", "", None):
    for name, fn in (("load_operands", lambda c: M.V0.load_operands(clean, config=c)),
                     ("load_layer", lambda c: M.load_layer(clean, M.KIT, config=c))):
        try:
            fn(cfg); print(f"NC-V4F-e {name} {cfg!r} OPENED (FAIL)")
        except M.RulebookPackRefused as e:
            print(f"NC-V4F-e {name} {cfg!r} REFUSED: {e}")
a = M.load_layer(clean, M.ANCHOR, config="JOIN")["anchor_m_per_yd"]
print("NC-V4F-e JOIN anchor_m_per_yd:", a["value"], a["grade"], "beside:", a["printed_beside"])
print("NC-V4F-e JOIN kit rows:", len(M.load_layer(clean, M.KIT, config="JOIN")))
d = S / "nc_d_pack"
shutil.copytree(clean, d)
f = d / "tables" / "physical_contact_table.json"; b = bytearray(f.read_bytes()); i = b.index(b"1"); b[i] = ord("2"); f.write_bytes(bytes(b))
r = subprocess.run([sys.executable, T, "verify", str(d)], capture_output=True, text=True)
print(r.stdout[-1500:]); print("NC-V4F-d verify rc", r.returncode)
try:
    M.load_layer(d, M.ANCHOR, config="JOIN"); print("NC-V4F-d load_layer OPENED (FAIL)")
except M.RulebookPackRefused as e:
    print("NC-V4F-d load_layer REFUSED:", e)
