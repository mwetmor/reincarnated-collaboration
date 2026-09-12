from gates.g2_pivot import root_anchor,visible_midpoint,planted_trajectory
from gates_helpers import *
class Tests(unittest.TestCase):
    def test_independent_root_and_shifted_mask(self):
        self.assertIsNone(root_anchor()['passed'])
        self.assertTrue(root_anchor([256,400])['passed'])
        self.assertFalse(root_anchor([261,400])['passed'])
        self.assertFalse(visible_midpoint(sprite())['passed'])
    def test_planted_slide_and_repeated_lead(self):
        points=[[[0,10],[10,8]],[[8,10],[10,8]],[[0,8],[10,10]],[[0,8],[10,10]]]
        planted=[[True,False],[True,False],[False,True],[False,True]]
        rows=planted_trajectory(points,planted,tolerance=4,expected_leads=[0,0,1,1])
        self.assertFalse(rows[0]['passed']);self.assertTrue(rows[1]['passed'])
        repeated=[[True,False]]*4
        self.assertFalse(planted_trajectory(points,repeated,expected_leads=[0,0,1,1])[1]['passed'])
        self.assertIsNone(planted_trajectory()['passed'])
