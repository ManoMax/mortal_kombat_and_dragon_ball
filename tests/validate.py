#!/usr/bin/env python3
"""Validate generated SFF chain and all animation sprite references."""
from pathlib import Path
import re, struct
root=Path(__file__).resolve().parents[1]
for name in ('goku','vegeta'):
    folder=root/'engine/chars'/name
    data=(folder/'fighter.sff').read_bytes()
    assert data[:12]==b'ElecbyteSpr\0'
    groups,count,offset,size=struct.unpack_from('<IIII',data,16)
    assert size==32
    entries=set()
    for i in range(count):
        nxt,length,x,y,g,n,linked,pal=struct.unpack_from('<IIhhHHHB',data,offset)
        assert offset+32+length<=len(data) and length>128
        assert data[offset+32]==10
        assert (g,n) not in entries
        entries.add((g,n))
        if i<count-1: assert nxt==offset+32+length
        else: assert nxt==0
        offset=nxt
    air=(folder/'kfm.air').read_text(encoding='utf-8-sig')
    required={tuple(map(int,m)) for m in re.findall(r'^\s*(\d+)\s*,\s*(\d+)\s*,',air,re.M)}
    assert required<=entries
    print(f'PASS {name}: {count} sprites, all animation references resolved')
assert (root/'engine/Ikemen_GO_Linux').is_file()
print('PASS engine present')
