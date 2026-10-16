"""Check generated arena SFF payloads, camera, and floor contact."""
import struct
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

if __name__=='__main__': unittest.main()
