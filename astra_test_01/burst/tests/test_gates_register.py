from gates.register import registration,measured_anchor,sole_contacts,contacts,register_reviewed
from gates_helpers import *
class Tests(unittest.TestCase):
    def test_upscaling_rejection(self):
        with self.assertRaises(ValueError):registration(sprite(),{'body_height':100,'anchor':[64,112]})
    def test_clipped_sole_rejection(self):
        for fn in (sole_contacts,contacts):
            with self.assertRaises(ValueError):fn(sprite(),[[35,90,60,110],[65,90,90,115]])
    def test_measured_registration_and_shifted_mask(self):
        rois=[[35,90,60,120],[65,90,90,120]]
        anchor=measured_anchor(sprite(),rois)
        self.assertEqual(anchor,[60.75,111.5])
        frame,info=register_reviewed(sprite(),rois,240)
        # Re-read output contacts using independently translated reviewed windows.
        dx,dy=info['translation'];moved=[[round(x0+dx),round(y0+dy),round(x1+dx),round(y1+dy)] for x0,y0,x1,y1 in rois]
        self.assertLessEqual(max(abs(np.array(measured_anchor(frame,moved))-[256,400])),1)
        with self.assertRaises(ValueError):measured_anchor(sprite(shift=20),rois)

    def test_reviewed_region_bounds(self):
        with self.assertRaises(ValueError):contacts(sprite(),[[-1,90,60,120],[65,90,90,120]])
