from gates.guides import DEFAULT_PROJECTION,PROJECTION_C,RUN_02,constants
from gates_helpers import *
class Tests(unittest.TestCase):
    def test_numeric_C_and_legacy(self):
        self.assertEqual(DEFAULT_PROJECTION,PROJECTION_C)
        self.assertEqual(PROJECTION_C['type'],'pinhole')
        self.assertAlmostEqual(PROJECTION_C['distance_m'],23.869291234544452)
        self.assertEqual(constants(),PROJECTION_C)
        legacy=constants('run_02');self.assertEqual(legacy['scale'],510)
        legacy['anchor'][0]=0;self.assertEqual(RUN_02['anchor'][0],512)
        with self.assertRaises(ValueError):constants('unknown')
