"""Offline integrity/routing checks. Does not evaluate artwork or gameplay motion."""
import ast,hashlib,json,re
from pathlib import Path
from urllib.parse import unquote,urlparse
from html.parser import HTMLParser
from PIL import Image
P=Path(__file__).resolve().parent;repo=P.parents[3]
rows=json.loads((P/'sources.json').read_text());assert len(rows)==28
assert len({r['id'] for r in rows})==28
for r in rows:
 f=P/r['path'];assert hashlib.sha256(f.read_bytes()).hexdigest()==r['sha256'],r['id']
 with Image.open(f) as im:assert list(im.size)==r['dimensions']
 assert r['inspection']=='VISUALLY_INSPECTED_FULL_FRAME'
 for previous in r['byte_identical_existing_files']:
  assert hashlib.sha256(Path(previous).read_bytes()).hexdigest()==r['sha256']
assert sum(bool(r['byte_identical_existing_files']) for r in rows)==7
for r in rows:
 if r['id'].startswith('LE-'):assert r['camera_eligibility'].startswith('EXCLUDED')
 if r['id']=='REPLICA-01':assert 'PROJECT REPLICA' in r['edition']
assert all(r['motion_verdict'].startswith('UNVERIFIED') for r in rows)
for f in P.glob('*.py'):ast.parse(f.read_text(),filename=str(f))
for f in P.rglob('*.json'):json.loads(f.read_text())
receipt=json.loads((P/'RECEIPT.json').read_text())
for file,sha in receipt['dependency_hashes'].items():assert hashlib.sha256((P/file).read_bytes()).hexdigest()==sha,file
progress=json.loads((P.parents[1]/'PROGRESS.json').read_text());assert progress['gates']['G1']=='INDETERMINATE';assert not progress['running_jobs'];assert progress['gates']['G2']=='NOT_RUN'
paths=[]
def local_link(raw,base):
 if raw.startswith(('http:','https:','data:','#','mailto:')):return
 raw=unquote(raw).split('#')[0]
 if not raw:return
 # Optional local source code line suffix is renderer syntax.
 raw=re.sub(r':\d+$','',raw)
 target=Path(raw) if raw.startswith('/') else base/raw
 assert target.exists(),str(target)
 paths.append(str(target))
for f in [P/'REPORT.md',P/'PREPARATION.md',P.parents[1]/'START_HERE.md',P.parents[1]/'SOURCE_INTAKE.md',repo/'.agents/skills/painted-character-vfx/references/measured-lessons.md']:
 for raw in re.findall(r'\]\(([^)]+)\)',f.read_text()):local_link(raw,f.parent)
class Links(HTMLParser):
 def handle_starttag(self,tag,attrs):
  for k,v in attrs:
   if k in ('src','href'):local_link(v,P)
parser=Links();parser.feed((P/'comparison.html').read_text())
for file in progress['completed_artifacts']:assert (P.parents[1]/file).exists(),file
for m in json.loads((P/'measurements.json').read_text()):
 r=next(r for r in rows if r['id']==m['id']);w,h=r['dimensions']
 if m['body_bbox']:
  a,b,c,d=m['body_bbox'];assert 0<=a<c<=w and 0<=b<d<=h
  assert m['body_height_px']==d-b
 assert 0<=m['foot'][0]<=w and 0<=m['foot'][1]<=h
result={'verdict':'PASS','scope':'Integrity, declared eligibility, syntax and local links only; browser/Canvas rendering remains unverified','source_hashes':28,'exact_prior_matches':7,'local_links_checked':len(paths),'json_and_python_syntax':'PASS','progress_gate_consistency':'PASS'}
(P/'validation.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
