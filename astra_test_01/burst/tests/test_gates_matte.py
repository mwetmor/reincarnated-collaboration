from gates.matte import extract,remove_chroma_key
from gates_helpers import *
class Tests(unittest.TestCase):
    def test_checkerboard_rejection(self):
        a=np.indices((128,128)).sum(0)%2*100+100
        with self.assertRaises(ValueError):extract(Image.fromarray(np.repeat(a[...,None],3,2).astype('uint8')))
    def test_native_alpha_dark_interiors(self):
        im=sprite();a=np.array(im);a[40:65,50:70,:3]=0
        out,info=extract(Image.fromarray(a))
        self.assertTrue(info['native_input_alpha'])
        self.assertEqual(out.getpixel((55,50)),(0,0,0,255))
    def test_particle_safe_opt_in_and_green_plate(self):
        im=sprite();ImageDraw.Draw(im).rectangle((10,10,13,13),fill=(80,80,150,255))
        self.assertEqual(extract(im)[0].getpixel((11,11))[3],0)
        self.assertEqual(extract(im,preserve_particles=True)[0].getpixel((11,11))[3],255)
        plate=Image.new('RGBA',im.size,(0,255,0,255));plate.alpha_composite(im)
        out=remove_chroma_key(plate.convert('RGB'),preserve_particles=True)
        self.assertEqual(out.getpixel((0,0))[3],0)
        self.assertGreater(out.getpixel((11,11))[3],200)
