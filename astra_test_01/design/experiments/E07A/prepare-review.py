from pathlib import Path
from PIL import Image,ImageDraw
import subprocess,json
p=Path(__file__).resolve().parent;b=p/'evidence/batch-03';probes=[]
for video in sorted(b.glob('*.webm')):
 meta=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(video)]));probes.append({'path':str(video.relative_to(p)),'width':meta['streams'][0]['width'],'height':meta['streams'][0]['height'],'duration_s':float(meta['format']['duration'])});clip=video.stem.split('-')[0];duration={'idle':1.6,'walk':.8,'cast':1.2}[clip];sheet=Image.new('RGB',(1200,240),'#303940')
 for j,k in enumerate([0,.25,.5,.75,1]):
  t=.2+duration*k;file=b/f'{video.stem}-sample{j}.png';subprocess.run(['ffmpeg','-v','error','-ss',str(t),'-i',str(video),'-frames:v','1',str(file)],check=True);im=Image.open(file);cell=im.crop((410,220,650,420));sheet.paste(cell,(j*240,35));ImageDraw.Draw(sheet).text((j*240+5,8),f'{clip} t={duration*k:.2f}s native crop',fill='white')
 sheet.save(b/f'{video.stem}-sequence.png')
(b/'video-probe.json').write_text(json.dumps(probes,indent=2)+'\n')
