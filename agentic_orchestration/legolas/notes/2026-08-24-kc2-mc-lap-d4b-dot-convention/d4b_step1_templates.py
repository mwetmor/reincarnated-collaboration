"""STEP 1 — locate offensiveSlow* variable definitions in the DEVELOPER-AUTHORED template schema
(templates.arc :: *.tpl). These .tpl files are the authoring schema the GD DBREditor consumes;
each Variable carries a developer 'description'. This is primary substrate, not a wiki."""
import sys, re, collections; sys.path.insert(0,'.')
from d4b_lib import *

a = ArcArchive(VENDOR_E3/'database'/'templates.arc')
hits = collections.defaultdict(list)
for n in a.names():
    try: txt = a.read_file(n).decode('utf-8-sig', errors='replace')
    except Exception as e: print('SKIP', n, e); continue
    if 'offensiveSlow' in txt:
        hits[n].append(len(re.findall(r'offensiveSlow', txt)))
print('templates mentioning offensiveSlow:', len(hits))
for n,c in sorted(hits.items()): print(f'  {n}  ({c[0]} mentions)')
