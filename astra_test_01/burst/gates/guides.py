"""Projection constants as data; C is the E01 numeric pinhole candidate.
No geometry artwork is generated. Callers choose a projection explicitly.
"""
from copy import deepcopy

RUN_02 = dict(type='affine', screen=[1024,1024], anchor=[512,800],
              scale=510, y_coeff=-0.5, z_coeff=-0.5, elevation_deg=45,
              vertical_image_compression=2**-.5, light_world_vector=[-.6,-.35,.8])
PROJECTION_C = {'id': 'C', 'title': 'Godot-informed perspective', 'type': 'pinhole', 'elevation_deg': 52.9535411256, 'yaw_deg': 47, 'q': 0.7981472596262743, 'screen': [720, 405], 'anchor': [360.74984436000005, 223.12467497699998], 'body_height_fraction': 0.095, 'uniform_scale_px_per_m': None, 'vertical_fov_deg': 31.7861018306, 'distance_m': 23.869291234544452, 'probe_heights_far_center_near_px': [39.98375830082445, 38.474999999999994, 35.85215776763948], 'ground_roundtrip_max_m': 2.2644195468014703e-15, 'note': 'C matches recovered angle/lens but recalibrates distance to equal body size; not exact recovered Godot camera. Ground field and all volumetric proxies use same projection; no painted asset is tested.'}
DEFAULT_PROJECTION = PROJECTION_C


def constants(name='C'):
    """Return independent caller-editable constants; never infer camera geometry."""
    if name not in ('C','run_02'): raise ValueError('Unknown projection constant set')
    return deepcopy(PROJECTION_C if name=='C' else RUN_02)
