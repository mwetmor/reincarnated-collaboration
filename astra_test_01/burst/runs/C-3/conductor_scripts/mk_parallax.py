import json,sys
D=sys.argv[1]; ys=dict(zip(['sky','far_ruins','forest_valley','mist'],map(float,sys.argv[2:6])))
sc={'sky':0.12,'far_ruins':0.25,'forest_valley':0.45,'mist':0.70}
L=[{'name':n,'file':f'layers/{n}.png','scroll_scale':sc[n],'position':[0,ys[n]],'z':-40+10*i} for i,n in enumerate(sc)]
json.dump({'layers':L,'camera':{'anchor':[962,595],'view':[1920,1080],'limits':[2,55,5378,4151]}},open(D+'/parallax.json','w'),indent=1)
print(ys)
