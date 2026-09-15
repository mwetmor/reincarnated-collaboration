"""Run the required unchanged suite with output/temp relocation only.

Existing test source, fixtures and other runs stay read-only. Python report writes
under tests/ and historical runs/ are diverted to this burst's suite_artifacts/.
TemporaryDirectory/mkdtemp use tests/tmp. No test assertions or results change.
"""
import json
import os
from pathlib import Path
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parents[4]
OUT = Path(__file__).resolve().parent
GUARD = ROOT/'tests/tmp/t4d_suite_guard'
GUARD.mkdir(parents=True,exist_ok=True)
CODE = r'''
import builtins, io, os, pathlib, tempfile
ROOT = pathlib.Path(os.environ['T4D_ROOT'])
OUT = pathlib.Path(os.environ['T4D_OUT'])
TMP = ROOT/'tests/tmp'
raw_open, raw_io, raw_mkdir = builtins.open, io.open, os.mkdir
raw_stat, raw_unlink, raw_rmdir = os.stat, os.unlink, os.rmdir

def candidate(path):
    if not isinstance(path,(str,bytes,os.PathLike)): return None
    p = pathlib.Path(os.path.abspath(os.fsdecode(path)))
    if p.is_relative_to(TMP) or p.is_relative_to(OUT): return None
    if p.is_relative_to(ROOT/'runs') or p.is_relative_to(ROOT/'tests'):
        if p.suffix == '.py': return None
        return OUT/'suite_artifacts'/p.relative_to(ROOT)
    return None

def mapped(path, write=False):
    dest = candidate(path)
    if dest is None: return path
    if write:
        dest.parent.mkdir(parents=True,exist_ok=True)
        return dest
    try: raw_stat(dest)
    except (FileNotFoundError,NotADirectoryError): return path
    return dest

def fopen(original):
    def wrapped(file,mode='r',*args,**kwargs):
        return original(mapped(file,any(c in mode for c in 'wax+')),mode,*args,**kwargs)
    return wrapped
builtins.open = fopen(raw_open)
io.open = fopen(raw_io)

def mkdir(path,*args,**kwargs):
    if kwargs.get('dir_fd') is not None: return raw_mkdir(path,*args,**kwargs)
    target = candidate(path)
    if target is not None:
        target.parent.mkdir(parents=True,exist_ok=True)
        return raw_mkdir(target,*args,**kwargs)
    return raw_mkdir(path,*args,**kwargs)
os.mkdir = mkdir

def stat(path,*args,**kwargs): return raw_stat(path if kwargs.get('dir_fd') is not None else mapped(path),*args,**kwargs)
os.stat = stat

def unlink(path,*args,**kwargs): return raw_unlink(path if kwargs.get('dir_fd') is not None else mapped(path),*args,**kwargs)
os.unlink = unlink

def rmdir(path,*args,**kwargs): return raw_rmdir(path if kwargs.get('dir_fd') is not None else mapped(path),*args,**kwargs)
os.rmdir = rmdir
old_mkdtemp = tempfile.mkdtemp
def mkdtemp(suffix=None,prefix=None,dir=None):
    return old_mkdtemp(suffix=suffix,prefix=prefix,dir=str(TMP))
tempfile.mkdtemp = mkdtemp
'''
(GUARD/'sitecustomize.py').write_text(CODE)
env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1', PYTHONPATH=str(GUARD),
           TMPDIR=str(ROOT/'tests/tmp'),T4D_ROOT=str(ROOT),T4D_OUT=str(OUT))
started = time.monotonic()
with (OUT/'full_suite_process.log').open('w') as stream:
    result = subprocess.run([sys.executable,'-B','tests/run_t0c.py'],cwd=ROOT,
                            env=env,stdout=stream,stderr=subprocess.STDOUT)
source = OUT/'suite_artifacts/tests/t0c_summary.json'
report = {'returncode':result.returncode,'wall_s':time.monotonic()-started,
          'command':'PYTHONDONTWRITEBYTECODE=1 python3 -B tests/run_t0c.py',
          'relocation':'sitecustomize redirects report writes and temporary directories only'}
if source.exists():
    data = json.loads(source.read_text())
    report.update(tests_run=data['tests_run'],successful=data['successful_tests'],
                  elapsed_s=data['elapsed_s'],reds=data['failures']+data['errors'],
                  skipped=data['skipped'],regression=data['regression'])
(OUT/'full_suite_summary.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({k:v for k,v in report.items() if k not in ('reds','regression','skipped')}))
for row in report.get('reds',[]): print(row['test'])
