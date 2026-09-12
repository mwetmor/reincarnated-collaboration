"""G9: literal edge mean, green spill, border clipping; explicit dark-fringe policy.
The allowed source contains a visual dark-fringe judgment, no numeric threshold.
Supply dark_threshold (edge mean RGB) to enable a numeric screening verdict.
This screen cannot establish visual absence of a localized black halo.
"""
from .common import rgba, measure, result

def evaluate(image, subject='', dark_threshold=None):
    m=measure(rgba(image))
    if not m['valid']: return [result('g9_alpha',subject,notes='Empty alpha subject')]
    return [result('g9_alpha',subject,m['border_alpha_max'],0,unit='alpha',notes='Canvas-border clipping'),
            result('g9_green',subject,m['green_contaminated_pixels'],0,unit='pixels',notes='Partial alpha and green excess >20'),
            result('g9_edge_mean',subject,m['edge_mean_rgb_value'],unit='rgb',notes='Mean RGB over 0<alpha<255; measurement only'),
            result('g9_dark_fringe',subject,m['edge_mean_rgb_value'],dark_threshold,op='>=',unit='rgb',
                   notes='UNEVALUABLE: source defines visual inspection, no numeric threshold' if dark_threshold is None else 'Caller-calibrated edge-mean screen; visual review still required')]
