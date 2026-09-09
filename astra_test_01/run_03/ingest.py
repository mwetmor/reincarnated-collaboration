"""Persist built-in generation results without changing original files."""
from pathlib import Path
import json, shutil, sys
ROOT=Path(__file__).resolve().parent
def ingest(record):
    e=json.loads(Path(record).read_text());name=e['name'];source=Path(e['source'])
    shutil.copyfile(source,ROOT/'source'/f'{name}.png')
    (ROOT/'prompts'/f'{name}.txt').write_text(e['prompt']+'\n')
    f=ROOT/'generation_log.json';log=json.loads(f.read_text()) if f.exists() else []
    if not any(row['name']==name for row in log):log.append(e)
    f.write_text(json.dumps(log,indent=2)+'\n')
    state=json.loads((ROOT/'STATE.json').read_text());state['generated_calls']=len(log);(ROOT/'STATE.json').write_text(json.dumps(state,indent=2)+'\n')
if __name__=='__main__':ingest(sys.argv[1])
