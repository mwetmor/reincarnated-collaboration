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

    def test_floor_and_particles(self):
        a=np.zeros((100,100,4),np.uint8);a[30:70,30:70]=(70,80,100,255)
        for x,y,v in [(5,5,30),(10,10,200),(80,80,100)]:a[y,x]=(20,50,80,v)
        legacy=np.array(extract(Image.fromarray(a),preserve_particles=True)[0])
        self.assertTrue(np.array_equal(a,legacy))
        floored=np.array(extract(Image.fromarray(a),preserve_particles=True,alpha_floor=40)[0])
        self.assertEqual(floored[5,5,3],0);self.assertEqual(floored[10,10,3],200)
        self.assertEqual(floored[80,80,3],100)

    def test_x1_floor_border_zero(self):
        from x1_helpers import X1_GENERATED,PROPS
        from gates.g9_alpha import evaluate
        for name in PROPS:
            with self.subTest(prop=name), Image.open(X1_GENERATED/f'x1_{name}.png') as im:
                out=extract(im,preserve_particles=True,alpha_floor=40)[0]
                self.assertEqual(evaluate(out)[0]['value'],0)
