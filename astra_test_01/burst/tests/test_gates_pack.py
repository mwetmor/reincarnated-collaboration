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

class VfxPixels(TemporaryTest):
    def test_internal_packing_energy_and_bad_size(self):
        from gates.pack import pack_vfx
        p=self.base/'frames/travel';p.mkdir(parents=True)
        a=np.zeros((8,12,4),np.uint8);a[2,3]=[200,100,50,128];a[3,4]=[255,255,255,0]
        Image.fromarray(a).save(p/'travel_00.png')
        data=vfx_atlas({'travel':(12,8)},{'travel':1},frames_dir=self.base/'frames',out_dir=self.base/'packed')
        with Image.open(self.base/'packed/sheets/travel.png') as im:np.testing.assert_array_equal(np.array(im),a)
        expected=(a[...,:3].astype(float)*(a[...,3,None]/255))@np.array([.2126,.7152,.0722])
        with Image.open(self.base/'packed/sheets/travel_emissive.png') as im:np.testing.assert_array_equal(np.array(im),expected.clip(0,255).astype('uint8'))
        self.assertEqual(data['modules']['travel']['count'],1)
        with self.assertRaises(ValueError):pack_vfx('travel',self.base/'frames',self.base/'bad')
