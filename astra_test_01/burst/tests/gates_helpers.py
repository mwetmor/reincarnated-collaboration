from pathlib import Path
import tempfile
import unittest
import numpy as np
from PIL import Image,ImageDraw

ROOT=Path(__file__).resolve().parents[1]
FIXTURE_ROOT=ROOT.parent/'run_03/character/frames'

def sprite(shift=0,bag=0,wrong_light=False):
    im=Image.new('RGBA',(128,128));d=ImageDraw.Draw(im)
    d.rectangle((45+shift,20,75+shift,85),fill=(70,60,55,255))
    d.rectangle((40+shift,80,53+shift,109),fill=(40,35,30,255))
    d.rectangle((68+shift,80,82+shift,114),fill=(40,35,30,255))
    d.rectangle((74+shift,50,82+shift+bag,70),fill=(80,65,45,255))
    x=66 if wrong_light else 46
    d.rectangle((x+shift,22,x+8+shift,40),fill=(250,240,230,255))
    return im

class TemporaryTest(unittest.TestCase):
    def setUp(self):
        (ROOT/'tests/tmp').mkdir(exist_ok=True)
        self.temp=tempfile.TemporaryDirectory(dir=ROOT/'tests/tmp')
        self.addCleanup(self.temp.cleanup)
        self.base=Path(self.temp.name)
