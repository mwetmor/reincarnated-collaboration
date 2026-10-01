set -x
I="blender -b -noaudio --python scripts/07_isolate2.py --"
$I builds/nocape.glb builds/wl_rigged.glb pieces/helm_iso.glb --region helm --hratio 1.0254 --yaw -90 --seed "(zf>0.90)&(dist>0.02)" --grow "(zf>0.80)&(dist>0.008)" 2>&1 | grep -E "noise|region|grown|components|rror"
$I builds/nocape.glb builds/wl_rigged.glb pieces/pauldrons_iso.glb --region shoulders --hratio 1.0254 --yaw -90 --seed "(zf>0.72)&(zf<0.86)&(ax>0.14)&(dist>0.03)" --grow "(zf>0.64)&(zf<0.89)&(ax>0.09)&(dist>0.010)" --minfrac 0.15 2>&1 | grep -E "noise|region|grown|components|rror"
$I builds/nocape.glb builds/wl_rigged.glb pieces/chest_iso.glb --region chest --hratio 1.0254 --yaw -90 --seed "(zf>0.60)&(zf<0.80)&(ax<0.16)&(dist>0.015)" --grow "(zf>0.56)&(zf<0.84)&(ax<0.21)&(dist>0.006)" 2>&1 | grep -E "noise|region|grown|components|rror"
$I builds/full_A1.glb builds/wl_rigged.glb pieces/cape_iso.glb --region cape --hratio 1.0254 --yaw -90 --seed "(y>0.12)&(dist>0.05)&(zf<0.75)" --grow "(y>0.02)&(dist>0.012)&(zf<0.86)" 2>&1 | grep -E "noise|region|grown|components|rror"
