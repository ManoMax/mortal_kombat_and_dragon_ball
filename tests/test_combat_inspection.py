"""Known-coordinate fixtures: these validate measurements, never art quality."""
import sys
from pathlib import Path
import unittest
import tempfile
from PIL import Image
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from inspect_combat import placed, metrics, inspect
import animation_polish
from air_geometry import frames


class CombatInspection(unittest.TestCase):
    def test_offsets_flips_and_both_facings(self):
        image = Image.new('RGBA',(12,12))
        image.putpixel((7,8),(255,100,50,255))
        for flags, facing, expected in (('',1,(164,244)),('H',1,(160,244)),('V',1,(164,236)),('HV',-1,(160,236))):
            result = placed(image,(5,4),(0,0,2,0,3),flags,facing)
            self.assertEqual(result.getchannel('A').getbbox(),(*expected,expected[0]+1,expected[1]+1))

    def test_ground_contact_and_lift_are_distinguished(self):
        image=Image.new('RGBA',(320,320))
        image.putpixel((155,239),(255,255,255,255))
        self.assertEqual(metrics(image)['bottom'],0)
        self.assertEqual(metrics(image)['contact_center'],-4.5)
        shifted=placed(image,(160,240),(0,0,0,-5,1),'')
        self.assertEqual(metrics(shifted)['bottom'],-5)
        self.assertNotEqual(metrics(image)['alpha_sha256'],metrics(shifted)['alpha_sha256'])

    def test_empty_and_clipped_art_rejected(self):
        image=Image.new('RGBA',(320,320))
        with self.assertRaises(ValueError): metrics(image)
        image.putpixel((319,100),(255,255,255,255))
        with self.assertRaises(ValueError): placed(image,(160,240),(0,0,3,0,1),'')


class IdlePolish(unittest.TestCase):
    def test_only_idle_durations_change(self):
        root=Path(__file__).resolve().parents[1]
        source=(root/'engine/chars/kfm/kfm.air').read_text(encoding='utf-8-sig')
        before=list(frames(source)); after=list(frames(animation_polish.apply(source)))
        self.assertEqual(len(before),len(after))
        changes=0
        for old,new in zip(before,after):
            if old[1] == 0:
                self.assertEqual(old[2][:4],new[2][:4])
                self.assertEqual(old[3:],new[3:])
                self.assertLessEqual(new[2][4],15)
                changes += old[2][4] != new[2][4]
            else:
                self.assertEqual(old,new)
        self.assertGreater(changes,0)


class ProductionInspection(unittest.TestCase):
    def test_all_organic_contexts_have_mirrored_bounds_and_state_inventory(self):
        with tempfile.TemporaryDirectory() as folder:
            for name in ('goku','vegeta'):
                report=inspect(name,Path(folder),set())
                self.assertTrue(any(s['state']==810 and s['origin']=='inherited KFM' for s in report['state_inventory']))
                self.assertTrue(any(s['state']==7100 and s['origin']=='DBZ layer' for s in report['state_inventory']))
                self.assertEqual(len(report['common_states']['sha256']),64)
                for action in report['actions'].values():
                    for frame in action['frames']:
                        if not frame['organic']: continue
                        x,y,r,b=frame['bounds']
                        self.assertEqual(frame['left_bounds'],[321-r,y,321-x,b])
                self.assertEqual([f['ticks'] for f in report['actions']['0']['frames']],animation_polish.idle_ticks())
