exec((__import__('pathlib').Path(__file__).parent/'prepare.py').read_text().split("im=Image.new")[0])
base=(-2,-1.5);corners=[(-2.5,-2),(-1.5,-2),(-1.5,-1),(-2.5,-1)];root=project(base);top=project(base,3);scale=540/(root[1]-top[1])
def pos(w,h=0):
 q=project(w,h);return(512+(q[0]-root[0])*scale,800+(q[1]-root[1])*scale)
im=Image.new('RGBA',(1024,1024),(0,0,0,0));draw=ImageDraw.Draw(im)
for ids,col in [([0,1],(91,105,112,255)),([1,2],(113,125,132,255)),([2,3],(74,87,95,255))]:
 i,j=ids;draw.polygon([pos(corners[i]),pos(corners[j]),pos(corners[j],3),pos(corners[i],3)],fill=col)
draw.polygon([pos(w,3) for w in corners],fill=(156,166,171,255));im.save(p/'guides/pillar-volume.png')
(p/'guides/pillar-registration.json').write_text(json.dumps({'root_source':[512,800],'axis_height_source':540,'height_m':3,'world':base,'footprint':corners,'source_corners':[[pos(w),pos(w,3)] for w in corners]},indent=2)+'\n')
