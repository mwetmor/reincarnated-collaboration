B="blender -b -noaudio --python scripts/e13_gear.py -- export/wl_body.glb"
COMMON="--pieces cape --flare 0.20 --side 0.10 --thigh 0.65 --ramp hem"
mkdir -p export/gear_i/v0 export/gear_i/v1 export/gear_i/v2 export/gear_i/v3
$B export/gear_i/v0 $COMMON --json work/gear_cape_i0.json 2>&1 | grep -c "^GEAR"
$B export/gear_i/v1 $COMMON --shin 0.4 --json work/gear_cape_i1.json 2>&1 | grep -c "^GEAR"
$B export/gear_i/v2 $COMMON --shin 0.4 --gap 0.03 --json work/gear_cape_i2.json 2>&1 | grep -c "^GEAR"
$B export/gear_i/v3 $COMMON --shin 0.7 --gap 0.03 --json work/gear_cape_i3.json 2>&1 | grep -c "^GEAR"
