from pathlib import Path
p=Path(__file__).resolve().parent
source_text=(p/'author.py').read_text();exec(compile(source_text[:source_text.index("results={'source_file'")],str(p/'author.py'),'exec'))
records=[]
for phase in [0,24]:
 previous=None
 for frame in range(37):
  stop_pose(frame/60,phase);now={pb.name:rig.matrix_world@pb.head for pb in rig.pose.bones}
  if previous is not None:
   name=max(now,key=lambda n:(now[n]-previous[n]).length);error=(now[name]-previous[name]).length
   if error>.05:records.append({'phase':phase,'frame':frame,'joint':name,'step_m':error,'before':list(previous[name]),'after':list(now[name])})
  previous=now
(HERE/'evidence/pole-diagnosis.json').write_text(json.dumps({'jumps':records},indent=2)+'\n');print(records)
