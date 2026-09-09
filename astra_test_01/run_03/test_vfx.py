import unittest
import numpy as np
from PIL import Image
from vfx import emission_matte
from character_matte import refine_blue_edges

class MatteTests(unittest.TestCase):
    def test_black_emission_reconstruction_preserves_detached_particles(self):
        source=np.zeros((32,32,3),dtype='uint8');source[8:12,8:12]=[40,90,180];source[24,25]=[4,12,30]
        out,info=emission_matte(Image.fromarray(source));a=np.array(out).astype(float);emission=a[...,:3]*a[...,3,None]/255
        self.assertLessEqual(np.abs(emission-source).max(),.5);self.assertGreater(a[24,25,3],0)

    def test_terminal_black_frame_is_zero_rgba(self):
        out,_=emission_matte(Image.new('RGB',(32,32)))
        self.assertFalse(np.array(out).any())

    def test_known_blue_chroma_edge(self):
        # Known foreground obeys the explicitly documented frost prior.
        rgb=np.array([20.,119.,200.]);alpha=.4;raw=np.round(rgb*alpha+np.array([0,255,0])*(1-alpha)).astype('uint8')
        source=Image.fromarray(np.tile(raw,(8,8,1)));base=Image.new('RGBA',(8,8),(20,200,200,100));out,_=refine_blue_edges(source,base);a=np.array(out)[0,0]
        self.assertLessEqual(abs(int(a[3])-102),1);self.assertLessEqual(abs(int(a[1])-119),2)

if __name__=='__main__':unittest.main()
