from pathlib import Path
from PIL import Image,ImageDraw
import json,subprocess
p=Path(__file__).resolve().parent;b=p/'evidence/batch-03';rows=[]
for video in sorted(b.glob('*.webm')):
 r=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(video)]));rows.append({'path':str(video.relative_to(p)),'width':r['streams'][0]['width'],'height':r['streams'][0]['height'],'duration_s':float(r['format']['duration']),'codec':r['streams'][0]['codec_name']})
 cells=[]
 for j,t in enumerate([.2,.4,.6,.8,1.05]):
  f=b/f'{video.stem}-t{j}.png';subprocess.run(['ffmpeg','-v','error','-ss',str(t),'-i',str(video),'-frames:v','1',str(f)],check=True)
  im=Image.open(f);cell=Image.new('RGB',(600,380),'#182331');cell.paste(im.crop((900,150,1200,500)),(0,30));cell.paste(im.crop((2100,150,2400,500)),(300,30));ImageDraw.Draw(cell).text((8,8),f'{video.stem} video t={t:.2f}s | views 135 / 315',(255,255,255));cells.append(cell)
 sheet=Image.new('RGB',(3000,380),'#182331')
 for j,c in enumerate(cells):sheet.paste(c,(j*600,0))
 sheet.save(b/f'{video.stem}-sequence.png')
(b/'video-probe.json').write_text(json.dumps(rows,indent=2)+'\n')
