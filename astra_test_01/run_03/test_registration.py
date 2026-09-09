"""Synthetic measurement fixtures, never production artwork."""
import unittest
from PIL import Image,ImageDraw
from turnaround import contacts
from head_registration import fit_scale

class RegistrationTests(unittest.TestCase):
    def test_crop_does_not_create_ground_contour(self):
        im=Image.new('RGBA',(100,100));ImageDraw.Draw(im).rectangle((20,10,40,90),fill='white')
        with self.assertRaisesRegex(ValueError,'No visible'):
            contacts(im,[[10,20,50,80],[10,20,50,80]])

    def test_two_actual_sole_contours(self):
        im=Image.new('RGBA',(100,100));d=ImageDraw.Draw(im)
        d.rectangle((20,10,40,80),fill='white');d.rectangle((60,10,80,90),fill='white')
        self.assertEqual(contacts(im,[[10,60,50,88],[50,60,90,98]])['midpoint'],[50.,85.])

    def test_hood_fit_recovers_global_scale(self):
        source=Image.new('RGBA',(500,500));d=ImageDraw.Draw(source)
        d.polygon([(250,30),(300,100),(285,155),(215,155),(200,100)],fill='white')
        d.rectangle((180,155,320,420),fill='white');d.rectangle((205,420,235,460),fill='white');d.rectangle((265,420,295,460),fill='white')
        ref=source.resize((250,250),Image.Resampling.LANCZOS)
        scale,info=fit_scale(source,ref)
        self.assertLess(abs(scale-.5),.02)
        self.assertLess(info['hood_width_rmse_px'],2)

if __name__=='__main__':unittest.main()
