import unittest
import numpy as np
from PIL import Image,ImageDraw
from composite_motion import composite

class CompositeTests(unittest.TestCase):
    def test_locked_pixels_exact_and_full_mask_replaces(self):
        base=Image.new('RGBA',(16,16),(11,22,33,77));variant=Image.new('RGBA',(16,16),(100,170,210,150));mask=Image.new('L',(16,16));ImageDraw.Draw(mask).rectangle((4,4,8,8),fill=255)
        result,evidence=composite(base,variant,mask);a=np.array(result)
        np.testing.assert_array_equal(a[0,0],np.array(base)[0,0]);np.testing.assert_array_equal(a[5,5],np.array(variant)[5,5]);self.assertTrue(evidence['locked_pixels_identical'])

    def test_feather_uses_premultiplied_alpha(self):
        result,_=composite(Image.new('RGBA',(1,1),(255,0,0,0)),Image.new('RGBA',(1,1),(0,0,255,255)),Image.new('L',(1,1),128))
        self.assertEqual(result.getpixel((0,0)),(0,0,255,128))

if __name__=='__main__':unittest.main()
