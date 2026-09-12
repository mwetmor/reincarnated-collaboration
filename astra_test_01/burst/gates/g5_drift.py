"""G5: every adjacent pair INCLUDING closure < frame zero versus cast 05."""
import json
from .common import difference, pair_differences, result

def evaluate(frames, cast05=None, subject=''):
    if len(frames)<2 or cast05 is None:
        return result('g5_drift',subject,notes='UNEVALUABLE: at least two frames and cast05 required')
    pairs=pair_differences(frames); cross=difference(frames[0],cast05)
    return result('g5_drift',subject,max(p['canvas'] for p in pairs),cross['canvas'],op='<',unit='rgb_mad',
                  notes=json.dumps({'adjacent_and_seam':pairs,'cross_cast_05':cross}))
