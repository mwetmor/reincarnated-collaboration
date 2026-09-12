"""G3: stable brightest-5% centroid must lie above and left of bbox centre."""
import json
from .common import rgba, measure, result

def evaluate(image, subject=''):
    m=measure(rgba(image))
    if not m['valid']: return result('g3_light',subject,notes='Empty alpha subject')
    offsets=[x-y for x,y in zip(m['light_centroid'],m['silhouette_center'])]
    return result('g3_light',subject,max(offsets),0,op='<',unit='px',notes=json.dumps(m))
