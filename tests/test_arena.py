"""Check generated arena SFF payloads, camera, and floor contact."""
import struct
import json
import re
import unittest
from pathlib import Path
from validate import decode
ROOT=Path(__file__).resolve().parents[1]


class ArenaTests(unittest.TestCase):
    def test_sff_layers_and_stage_bounds(self):
        data=(ROOT/'engine/stages/obsidian.sff').read_bytes()
        self.assertEqual(data[:12],b'ElecbyteSpr\0')
        groups,count,offset,size=struct.unpack_from('<IIII',data,16)
        self.assertEqual((groups,count,offset,size),(1,2,512,32))
        for frame,height in enumerate((240,56)):
            nxt,length,x,y,g,n,linked,pal=struct.unpack_from('<IIhhHHHB',data,offset)
            self.assertEqual((x,y,g,n,linked,pal),(320,0,0,frame,0,0))
            w,h,stride,pixels=decode(data[offset+32:offset+32+length])
            self.assertEqual((w,h),(640,height))
            end=offset+32+length
            self.assertEqual(nxt,end if frame==0 else 0)
            offset=end
        self.assertEqual(offset,len(data))
        stage=(ROOT/'engine/stages/obsidian.def').read_text()
        for expected in ('zoffset = 190','boundleft = -100','boundright = 100','delta = .35,.2','start = 0,184','autoturn = 1'):
            self.assertIn(expected,stage)
        # The outward side is negative local X for either facing. Keep actual
        # idle/walk/guard silhouettes inside the viewport, rather than checking
        # an arbitrary camera constant that could still clip new artwork.
        outward=0
        for name in ('goku','vegeta'):
            manifest=json.loads((ROOT/f'assets-source/sprites/{name}/manifest.json').read_text())
            for frame in manifest['frames']:
                if frame.get('organic') and frame['file'].split('/')[0] in ('idle','walk','guard'):
                    outward=max(outward,-frame['normalized_bounds'][0])
        for side in ('screenleft','screenright'):
            margin=int(re.search(r'^'+side+r'\s*=\s*(\d+)',stage,re.M)[1])
            self.assertGreaterEqual(margin,outward)

if __name__=='__main__': unittest.main()
