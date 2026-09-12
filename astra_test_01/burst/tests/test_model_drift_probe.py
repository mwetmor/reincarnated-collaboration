import hashlib
import tempfile
from oracles.model_drift_probe import freeze,distance
from oracles_helpers import *
class Tests(unittest.TestCase):
    def setUp(self):
        td=tempfile.TemporaryDirectory(dir=ROOT/'tests/tmp');self.addCleanup(td.cleanup);self.root=Path(td.name)
    def test_freeze_reference_hash_and_strict_schema(self):
        ref=self.root/'ref.png';Image.fromarray(sprite()).save(ref)
        manifest=dict(probes=[dict(id='synthetic',prompt='Synthetic unit-test placeholder only.',
            references=[dict(path='ref.png',sha256=hashlib.sha256(ref.read_bytes()).hexdigest())],expected_canvas=[64,64])])
        path=self.root/'probe.json';path.write_text(json.dumps(manifest))
        self.assertEqual(freeze(path),hashlib.sha256(path.read_bytes()).hexdigest())
        ref.write_bytes(b'changed')
        with self.assertRaisesRegex(ValueError,'hash mismatch'):freeze(path)
        manifest['probes'][0]['extra']=1;path.write_text(json.dumps(manifest))
        with self.assertRaises(ValueError):freeze(path)
    def test_identical_mirror_palette_and_missing(self):
        approved=self.root/'approved';out=self.root/'outputs';approved.mkdir();out.mkdir()
        a=np.zeros((96,96,4),np.uint8);a[10:85,30:60]=(50,90,140,255);a[15:50,60:85]=(60,110,150,255)
        Image.fromarray(a).save(approved/'one.png');Image.fromarray(a).save(out/'one.png')
        same=distance(out,approved);self.assertEqual(same['value'],0);self.assertIsNone(same['passed'])
        Image.fromarray(a[:,::-1]).save(out/'one.png');mirror=distance(out,approved)
        self.assertGreater(mirror['value'],0);self.assertGreater(metrics(mirror)['aggregate']['O5'],0)
        b=a.copy();b[b[...,3]>0,:3]=(200,30,40);Image.fromarray(b).save(out/'one.png')
        shifted=distance(out,approved);self.assertGreater(metrics(shifted)['aggregate']['O1'],0)
        self.assertFalse(distance(out,approved,alarm_threshold=0)['passed'])
        (out/'one.png').unlink();self.assertIsNone(distance(out,approved)['passed'])
