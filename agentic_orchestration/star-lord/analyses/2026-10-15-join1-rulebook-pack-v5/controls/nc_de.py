import glob, importlib.util, pathlib, shutil, subprocess, sys
S = pathlib.Path(sys.argv[1]); T = "/Users/admin/Games/reincarnated-engine/src/reincarnated/export/kc2_rulebook_pack_v5.py"
spec = importlib.util.spec_from_file_location("v5", T); M = importlib.util.module_from_spec(spec); sys.modules["v5"] = M; spec.loader.exec_module(M)
clean = pathlib.Path(glob.glob(str(S / "dry3" / "kc2-rulebook-pack-v5-*"))[0]); print("clean dry pack:", clean)
n = 0
for cfg in ("ORACLE", "PLAY", "join", "", None):
    for name, fn in (("load_operands", lambda c: M.V0.load_operands(clean, config=c)),
                     ("load_layer KIT", lambda c: M.load_layer(clean, M.KIT, config=c)),
                     ("load_layer WORLD", lambda c: M.load_layer(clean, M.WORLD, config=c))):
        try:
            fn(cfg); print(f"NC-V5-e {name} {cfg!r} OPENED (FAIL)")
        except M.RulebookPackRefused as e:
            n += 1; print(f"NC-V5-e {name} {cfg!r} REFUSED: {e}")
print("NC-V5-e refused", n, "/ 15")
W = M.load_layer(clean, M.WORLD, config="JOIN"); K = M.load_layer(clean, M.KIT, config="JOIN")
print("NC-V5-e JOIN l21_length_frames", W["l21_length_frames"]["value"], "stamina_max", K["stamina_max"]["value"], "kit_id", K["kit_id"]["value"])
d = S / "nc_d_pack"
shutil.copytree(clean, d)
f = d / "tables" / "physical_contact_table.json"; b = bytearray(f.read_bytes()); i = b.index(b"1"); b[i] = ord("2"); f.write_bytes(bytes(b))
r = subprocess.run([sys.executable, T, "verify", str(d)], capture_output=True, text=True)
print(r.stdout[-1200:]); print("NC-V5-d verify rc", r.returncode)
try:
    M.load_layer(d, M.WORLD, config="JOIN"); print("NC-V5-d load_layer OPENED (FAIL)")
except M.RulebookPackRefused as e:
    print("NC-V5-d load_layer REFUSED:", e)
