from gates.common import result,measure,difference
from gates_helpers import *
class Tests(unittest.TestCase):
    def test_empty_and_changed(self):
        self.assertFalse(measure(Image.new('RGBA',(32,32)))['valid'])
        self.assertGreater(difference(sprite(),sprite(shift=8))['canvas'],0)
        self.assertEqual(difference(sprite(),sprite())['canvas'],0)
        self.assertIsNone(result('x','s',notes='missing')['passed'])
        self.assertFalse(result('x','s',2,1)['passed'])

    def test_empty_foreground_has_no_nan(self):
        a=Image.new('RGBA',(16,16))
        self.assertIsNone(difference(a,a)['foreground_union'])
