import subprocess, os
ON={151:682.10,152:698.42,153:714.68,157:780.32}
procs=[]
for w,t in ON.items():
    a=round(t+3.0,2)
    os.makedirs(f'p05b/f{w}',exist_ok=True)
    procs.append(subprocess.Popen(['python3','census.py','../ref.mp4',str(a),str(round(t+9.5,2)),'30',f'p05b/cen_{w}.json'],stdout=open(f'p05b/cen_{w}.log','w'),stderr=subprocess.STDOUT))
    procs.append(subprocess.Popen(['ffmpeg','-v','error','-ss',str(a),'-t','6.5','-i','../ref.mp4','-vf','fps=30,scale=960:540','-q:v','4',f'p05b/f{w}/f_%04d.jpg']))
for p in procs: p.wait()
