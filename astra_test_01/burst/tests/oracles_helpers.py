import json
from pathlib import Path
import unittest
import numpy as np
from PIL import Image
from scipy import ndimage
ROOT=Path(__file__).resolve().parents[1]
FIXTURES=ROOT/'fixtures'
FRAME=ROOT.parent/'run_03/character/frames'
def metrics(row):return json.loads(row['notes'])['metrics']
def fixture_params():
    manifest=json.loads((FIXTURES/'manifest.json').read_text())
    return manifest,{k:v for k,v in manifest['motif_parameters'].items() if k in ['scales','rotations_deg','thresh','nms_iou']}
def stub():return json.loads((ROOT/'bible/f04-keepers.stub.json').read_text())
def sprite(color=(50,70,90)):
    a=np.zeros((64,64,4),np.uint8);a[8:56,8:56]=[*color,255];return a

def assert_envelope(case,row):
    case.assertEqual(set(row),{'id','subject','passed','value','threshold','op','unit','evidence','notes'})
    json.dumps(row,allow_nan=False)
