from gates.pack import package,vfx_atlas,composite_sockets
from gates_helpers import *
class Tests(TemporaryTest):
    def test_sparse_atlas_layout_and_invalid_canvas(self):
        source=self.base/'frames/idle/S';source.mkdir(parents=True)
        Image.new('RGBA',(512,512),(100,50,20,255)).save(source/'idle_S_00.png')
        atlas=package(self.base/'frames',self.base/'character')
        self.assertEqual(atlas['available_frames'],1)
        self.assertEqual(atlas['animations']['idle']['frames'][0]['rect'],[0,0,512,512])
        with Image.open(self.base/'character/contact/idle.png') as im:self.assertEqual(im.size,(1024,1024))
        sprite().save(source/'idle_S_01.png')
        with self.assertRaises(ValueError):package(self.base/'frames',self.base/'bad')
    def test_vfx_metadata(self):
        calls=[];a=vfx_atlas({'travel':(256,128)},{'travel':6},calls.append)
        self.assertEqual(calls,['travel']);self.assertEqual(a['modules']['travel']['pivot'],[170,64])
