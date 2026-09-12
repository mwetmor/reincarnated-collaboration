from oracles.figure_ground import separation
from oracles_helpers import *
class Tests(unittest.TestCase):
    def test_contrast_reverse_and_empty(self):
        light=separation(sprite((200,200,200)),(20,20,20),min_delta=50)
        dark=separation(sprite((10,10,10)),(200,200,200),min_delta=50,display_scale=.5)
        self.assertTrue(light['passed']);self.assertFalse(dark['passed'])
        self.assertEqual(metrics(dark)['sign'],-1);assert_envelope(self,dark)
        self.assertIsNone(separation(np.zeros((8,8,4),np.uint8),(20,20,20))['passed'])
