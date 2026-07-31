#!/usr/bin/env python3
"""V5 - template variable declarations + descriptions for the spawn/champion/gameadjustment
families, read from templates.arc. READ-ONLY."""
import sys, pathlib, re
sys.path.insert(0,"/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/research/scripts")
from gd_arc_reader_2026_07_26 import ArcArchive
P=pathlib.Path("/Users/admin/Games/vendor/grim-dawn/database/templates.arc")
arc=ArcArchive(P)
names=arc.names()
want=[n for n in names if any(t in n.lower() for t in
      ("proxypool","proxy.tpl","gameadjustment","attributepak","gameengine","setpiece","gameascendant"))]
print("matching templates:", want)
NEEDLE=re.compile(r'(spawn|champion|hero|experience|challenge|mutator|adjust)',re.I)
for w in want:
    data=arc.read_file(w)
    try: txt=data.decode("utf-8","replace")
    except Exception: continue
    print("\n"+"="*100); print(w); print("="*100)
    # tpl files are brace-structured Variable { ... } blocks
    blocks=re.findall(r'Variable\s*\{(.*?)\}', txt, re.S)
    for b in blocks:
        nm=re.search(r'name\s*=\s*"([^"]*)"',b)
        if not nm or not NEEDLE.search(nm.group(1)): continue
        ty=re.search(r'type\s*=\s*"([^"]*)"',b)
        cl=re.search(r'class\s*=\s*"([^"]*)"',b)
        de=re.search(r'description\s*=\s*"([^"]*)"',b)
        df=re.search(r'defaultValue\s*=\s*"([^"]*)"',b)
        print(f"  {nm.group(1):36s} type={ty.group(1) if ty else '?':10s} class={cl.group(1) if cl else '?':10s} "
              f"def={df.group(1) if df else '':6s} :: {de.group(1) if de else ''}")
