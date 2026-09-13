import json,sys
src='/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst/runs/C-3/artifacts/CS-guides-v3/walkable.json'
w=json.load(open(src))
r=lambda p:[round(p[0],2),round(p[1],2)]
walk=[[r(p) for p in x['polygon_px']] for x in w['walkable']+w['walkable_flagged']]
blk=[[r(p) for p in x['footprint_px']] for x in w['blocked']]
out={'canvas_size':[5376,4096],'walkable':walk,'blocked':blk,'spawn':r(w['spawn_feet_px']),'bounds':[0,0,5376,4096],'figure_height_px':130}
json.dump(out,open(sys.argv[1],'w'))
print(len(walk),[len(p) for p in walk],len(blk))
