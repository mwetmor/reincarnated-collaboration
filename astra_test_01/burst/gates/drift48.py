"""48px LANCZOS RGBA canvas reduction, same composite/comparator as G5."""
from PIL import Image
from .common import rgba
from .g5_drift import evaluate as drift

def evaluate(frames, cast05=None, subject=''):
    small=lambda im:rgba(im).resize((48,48),Image.Resampling.LANCZOS)
    r=drift([small(f) for f in frames],None if cast05 is None else small(cast05),subject)
    r['id']='drift48';r['notes']='48px LANCZOS, then dark-background composite; '+r['notes']
    return r
