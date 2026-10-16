"""Negative controls for validators: invalid evidence must fail."""
import unittest
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from air_geometry import frames
from match_smoke import verify
from validate import decode

class RegressionTests(unittest.TestCase):
    def test_air_default_override_reset_and_empty(self):
        air='''[Begin Action 0]
Clsn2Default: 1
Clsn2[0] = 10, 0, -10, -90
0,0, 0,0, 1
Clsn2: 0
0,1, 0,0, 1
0,2, 0,0, 1
[Begin Action 1]
0,0, 0,0, 1
'''
        result=list(frames(air))
        self.assertEqual([v[4][2] for v in result], [[(-10,-90,10,0)],[],[(-10,-90,10,0)],[]])

    def test_air_rejects_missing_boxes(self):
        with self.assertRaises(ValueError):
            list(frames('[Begin Action 0]\nClsn2: 1\n0,0, 0,0, 1'))

    def test_offset_and_both_flips_have_known_pixel_bounds(self):
        from build_characters import sprite
        pcx=sprite(41,4,False,({1:[],2:[(-10,-90,10,0)]},5,-120,', VH',41,4))
        width,height,stride,pixels=decode(pcx)
        occupied=[(i%stride,i//stride) for i,v in enumerate(pixels) if v]
        self.assertEqual((min(x for x,y in occupied),max(x for x,y in occupied),
                          min(y for x,y in occupied),max(y for x,y in occupied)),(155,175,120,210))

    def test_match_scores_and_reject_incomplete(self):
        log='''["LastRound"] => 2
["WinSide"] => 1
["Draws"] => 0
["Wins"] => table: 0x1 { [1] => 0 [2] => 2 }
["Index"] => 1
["Win"] => false
["Win"] => true
["Index"] => 2
["Win"] => false
["Win"] => true
'''
        self.assertEqual(verify(log),(2,[0,2]))
        with self.assertRaises(ValueError): verify(log,require_ko=True)
        for invalid in ('', log.replace('[2] => 2','[2] => 1'),
                        log.replace('["Index"] => 2','["Index"] => 3'),
                        log.replace('["WinSide"] => 1','["WinSide"] => 0'),
                        log.replace('["Win"] => true','["Win"] => false'),
                        log.replace('["LastRound"] => 2','["LastRound"] => 1')):
            with self.subTest(invalid=invalid), self.assertRaises(ValueError): verify(invalid)

    def test_sff_rejects_bad_chain_and_misaligned_origin(self):
        import tempfile, struct
        from validate import validate
        folder=Path(__file__).resolve().parents[1]/'engine/chars/goku'
        original=(folder/'fighter.sff').read_bytes()
        with tempfile.TemporaryDirectory() as directory:
            destination=Path(directory)
            (destination/'kfm.air').write_bytes((folder/'kfm.air').read_bytes())
            broken=bytearray(original)
            struct.pack_into('<I',broken,52,513)
            (destination/'fighter.sff').write_bytes(broken)
            with self.assertRaisesRegex(ValueError, 'Invalid SFF sections'): validate(destination, 'goku')
            broken=bytearray(original); offset=512
            while struct.unpack_from('<H',broken,offset)[0]!=30000:
                offset+=28
            struct.pack_into('<h',broken,offset+8,0)
            (destination/'fighter.sff').write_bytes(broken)
            with self.assertRaisesRegex(ValueError, 'origin'): validate(destination, 'goku')

    def test_pcx_rejects_truncation(self):
        from build_characters import sprite
        valid=sprite(0,0,False)
        self.assertEqual(decode(valid)[:2],(160,120))
        for broken in (valid[:128],valid[:-1],valid[:128]+valid[129:]):
            with self.assertRaises((ValueError,IndexError)): decode(broken)

if __name__=='__main__': unittest.main()
