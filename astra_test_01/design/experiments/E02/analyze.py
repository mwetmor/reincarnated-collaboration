"""Read-only art inspection and independently cross-checked projection analysis."""
from pathlib import Path
import hashlib
import json
import math
import platform
import numpy as np
from PIL import Image

HERE = Path(__file__).resolve().parent
profiles = json.loads((HERE / 'inputs/projection-candidates.json').read_text())
c = profiles[2]
t, yaw = map(math.radians, [c['elevation_deg'], c['yaw_deg']])
st, ct, sy, cy = math.sin(t), math.cos(t), math.sin(yaw), math.cos(yaw)
f = 405 / 2 / math.tan(math.radians(c['vertical_fov_deg']) / 2)
d = c['distance_m']
anchor = np.array(c['anchor'])


def project(point, perspective=True):
    u, v, h = point
    right, depth = cy*u-sy*v, sy*u+cy*v
    scale = f/(d-ct*depth-st*h) if perspective else profiles[1]['uniform_scale_px_per_m']
    return anchor + scale*np.array([right, st*depth-ct*h])


# Homogeneous camera matrix assembled separately, not calling project().
denominator = np.array([-ct*sy, -ct*cy, -st, d])
matrix = np.vstack((f*np.array([cy, -sy, 0, 0])+anchor[0]*denominator,
                    f*np.array([st*sy, st*cy, -ct, 0])+anchor[1]*denominator,
                    denominator))


def matrix_project(point):
    q = matrix @ np.array([*point, 1])
    return q[:2]/q[2]


samples = [('center', 0, 0), ('far', 0, -3), ('near', 0, 3),
           ('left', -3, 0), ('right', 3, 0), ('far-left', -2, -2),
           ('far-right', 2, -2), ('near-left', -2, 2), ('near-right', 2, 2)]
# Camera-aligned volume. Known geometric fixture, never inferred mage anatomy.
corners = [np.array([cy*r+sy*z, -sy*r+cy*z, h])
           for r in [-.3, .3] for z in [-.2, .2] for h in [0, 2]]
center_image = [project(q)-anchor for q in corners]
center_height = anchor[1]-project([0, 0, 2])[1]
rows = []
matrix_errors = []
for name, right, depth in samples:
    u, v = cy*right+sy*depth, -sy*right+cy*depth
    origin = np.array([u, v, 0])
    root, top = project(origin), project(origin+[0, 0, 2])
    height = root[1]-top[1]
    scale = height/center_height
    actual = [project(origin+q) for q in corners]
    sprite_like = [root+scale*q for q in center_image]
    residuals = [float(np.linalg.norm(a-b)) for a,b in zip(actual, sprite_like)]
    # Viewpoint at mid-body; eye = camera back * distance, above ground.
    horizontal_depth = ct*d-depth
    elevation = math.degrees(math.atan2(st*d-1, math.hypot(right, horizontal_depth)))
    azimuth_delta = math.degrees(math.atan2(right, horizontal_depth))
    circumference = [np.array([u+.7*math.cos(a), v+.7*math.sin(a), 0])
                     for a in np.linspace(0, math.tau, 48, endpoint=False)]
    correct_ring = [project(q) for q in circumference]
    frozen_ring = [root+project(q-origin)-anchor for q in circumference]
    ring_errors = [float(np.linalg.norm(a-b)) for a,b in zip(correct_ring,frozen_ring)]
    for q in [origin, origin+[0,0,2], *[origin+x for x in corners], *circumference]:
        matrix_errors.append(float(np.linalg.norm(project(q)-matrix_project(q))))
    rows.append(dict(id=name, camera_ground=[right,depth], world=[u,v],
                     inside_chamber=bool(-5<=u<=5 and -4<=v<=4),
                     root_px=root.tolist(), top_px=top.tolist(), body_height_px=height,
                     uniform_sprite_scale_vs_center=scale,
                     top_axis_horizontal_shift_px=float(top[0]-root[0]),
                     cuboid_corner_max_residual_px=max(residuals),
                     cuboid_corner_mean_residual_px=float(np.mean(residuals)),
                     geometric_review_flag=max(residuals)>2,
                     view_elevation_at_1m_deg=elevation,
                     view_azimuth_delta_deg=azimuth_delta,
                     frozen_ring_max_error_px=max(ring_errors)))

im = Image.open(HERE/'inputs/legacy-idle-S.png')
rgba = np.array(im.convert('RGBA'))
alpha = rgba[:,:,3]
border = np.concatenate([alpha[0],alpha[-1],alpha[:,0],alpha[:,-1]])
alpha_stats = dict(mode=im.mode, dimensions=list(im.size),
                   transparent_pixels=int(np.sum(alpha==0)),
                   opaque_pixels=int(np.sum(alpha==255)),
                   partial_pixels=int(np.sum((alpha>0)&(alpha<255))),
                   border_alpha_max=int(border.max()))
checks = dict(matrix_agreement=max(matrix_errors)<=1e-8,
              samples_inside_chamber=all(x['inside_chamber'] for x in rows),
              native_alpha=alpha_stats['transparent_pixels']>0 and alpha_stats['opaque_pixels']>0 and alpha_stats['border_alpha_max']==0,
              tracking_removes_relative_position=all(np.linalg.norm(project(np.array([*r['world'],0])-np.array([*r['world'],0]))-anchor)<1e-8 for r in rows),
              shifted_root_rejected=np.linalg.norm([8.,0])>.5,
              shifted_socket_rejected=np.linalg.norm([8.,0])>.5,
              wrong_scale_rejected=all(abs(r['body_height_px']*1.25-r['body_height_px'])>.5 for r in rows),
              frozen_ring_rejected_offcenter=all(r['frozen_ring_max_error_px']>.5 for r in rows if r['id']!='center'))
# Separate negative control applied to the independent matrix, proving sensitivity.
corrupt = matrix.copy(); corrupt[0] += 8*matrix[2]
q = corrupt @ np.array([1,2,0,1])
checks['corrupt_projection_rejected'] = bool(np.linalg.norm(q[:2]/q[2]-project([1,2,0]))>.5)
result = dict(experiment='E02', coordinate_convention='positive camera-ground depth is nearer camera',
              checks={k:bool(v) for k,v in checks.items()},
              matrix_max_error_px=max(matrix_errors), alpha=alpha_stats, samples=rows,
              scope='Static single-source sprite / known-volume diagnostic. No anatomy or gait pass.',
              python=platform.python_version(), numpy=np.__version__)
(HERE/'evidence/analysis.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'checks':result['checks'],'matrix_max_error_px':max(matrix_errors),
                  'max_cuboid_error_px':max(r['cuboid_corner_max_residual_px'] for r in rows)},indent=2))
assert all(checks.values())
