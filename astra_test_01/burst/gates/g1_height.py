"""G1: alpha>=128 bbox height, relative to S master, literal +/-3%."""
from .common import measure, rgba, result

def evaluate(image, master, subject='', tolerance=.03):
    a,b=measure(rgba(image)),measure(rgba(master))
    if not a['valid'] or not b['valid']:
        return result('g1_height',subject,notes='Empty alpha subject or master')
    return result('g1_height',subject,abs(a['height']/b['height']-1),tolerance,
                  unit='fraction',notes=f"height_px={a['height']}; master_height_px={b['height']}")
