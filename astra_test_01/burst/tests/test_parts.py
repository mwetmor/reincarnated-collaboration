from parts.part_masks import classify_by_bins
from parts import part_metrics
from oracles.common import lab
from oracles_helpers import *
class Tests(unittest.TestCase):
    def fixture(self):
        a=np.zeros((96,96,4),np.uint8);truth={};bins={}
        for name,color,box in [('red',(210,30,50),(5,5,35,40)),('green',(40,190,50),(50,8,87,45)),('blue',(40,50,210),(20,55,65,90))]:
            x0,y0,x1,y1=box;m=np.zeros((96,96),bool);m[y0:y1,x0:x1]=True
            border=ndimage.binary_dilation(m)&~m;a[border]=[*color,64];a[m]=[*color,255]
            truth[name]=ndimage.binary_erosion(m,iterations=1)
            c=lab(np.array(color));bins[name]={'a':[float(c[1]-2),float(c[1]+2)],'b':[float(c[2]-2),float(c[2]+2)]}
        return a,truth,bins
    def test_three_part_antialiased_iou_and_health(self):
        a,truth,bins=self.fixture();r=classify_by_bins(a,bins,max_unclassified=.2);scores={}
        for part,expected in truth.items():
            got=r['masks'][part];scores[part]=float((got&expected).sum()/(got|expected).sum());self.assertGreaterEqual(scores[part],.95)
        self.assertGreater(r['unclassified_frac'],0);self.assertTrue(r['result']['passed'])
        (ROOT/'tests/parts_measurements.json').write_text(json.dumps({'iou':scores,'unclassified_frac':r['unclassified_frac']},indent=2)+'\n')
        a[a[...,3]>0,:3]=128;bad=classify_by_bins(a,bins,max_unclassified=.2)
        self.assertIsNone(bad['result']['passed']);self.assertEqual(bad['unclassified_frac'],1)
        assert_envelope(self,bad['result'])
    def test_ambiguous_bins_empty_and_display(self):
        a,truth,bins=self.fixture();bins['duplicate']=bins['red'];r=classify_by_bins(a,bins,max_unclassified=.1)
        self.assertFalse(r['masks']['red'].any());self.assertIsNone(r['result']['passed'])
        self.assertIsNone(classify_by_bins(np.zeros_like(a),bins)['result']['passed'])
        self.assertEqual(classify_by_bins(a,bins,display_scale=.5)['masks']['red'].shape,(48,48))
    def test_metrics_and_known_bad(self):
        a,truth,bins=self.fixture();m=truth['red'];mirrored=m[:,::-1]
        self.assertEqual(part_metrics.area(m)['value'],int(m.sum()))
        self.assertEqual(part_metrics.centroid_rel(m,m)['value'],[0,0])
        self.assertEqual(part_metrics.mirror_symmetry(m,mirrored,threshold=.1)['value'],0)
        self.assertFalse(part_metrics.mirror_symmetry(m,m,threshold=.1)['passed'])
        self.assertAlmostEqual(part_metrics.palette_distance(a,m,['#d21e32'])['value'],0)
        self.assertIsNone(part_metrics.area(np.zeros_like(m))['passed'])
