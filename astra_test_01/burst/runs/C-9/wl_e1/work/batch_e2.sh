I="blender -b -noaudio --python scripts/07_isolate2.py --"
$I builds/nocape.glb builds/wl_rigged.glb pieces/helm_iso.glb --region helm --hratio 1.0254 --yaw -90 --seed "(zf>0.90)" --grow "(zf>0.845)" 2>&1 | grep -E "region|grown|components|rror"
$I builds/nocape.glb builds/wl_rigged.glb pieces/chest_iso.glb --region chest --hratio 1.0254 --yaw -90 --seed "(zf>0.62)&(zf<0.80)&(ax<0.14)&(dist>0.010)" --grow "(zf>0.565)&(zf<0.835)&(ax<0.19)&~((ax>0.13)&(zf>0.74))" 2>&1 | grep -E "region|grown|components|rror"
$I builds/full_A1.glb builds/wl_rigged.glb pieces/cape_iso.glb --region cape --hratio 1.0254 --yaw -90 --alignz 0.05 --seed "(y>0.12)&(dist>0.05)&(zf<0.75)" --grow "(y>0.02)&(dist>0.012)&(zf<0.82)&~((ax>0.13)&(zf>0.72))" 2>&1 | grep -E "region|grown|components|rror"
for p in helm chest cape; do blender -b -noaudio --python scripts/e03_render_views.py -- pieces/${p}_iso.glb look/iso_$p --n 4 --res 400 2>&1 | grep -c bbox; done
