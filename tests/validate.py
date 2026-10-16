#!/usr/bin/env python3
"""Validate SFF/PCX, AIR semantics, and visible collision alignment without X11."""
from pathlib import Path
import re
import struct
import sys
import hashlib
import json
sys.path.insert(0, str(Path(__file__).resolve().parents[1]/'scripts'))
from air_geometry import frames
from sff_rgba import read_sff
from png_pipeline import load_overrides
import dbz_combat as dbz
root=Path(__file__).resolve().parents[1]

def require(condition, message):
    if not condition: raise ValueError(message)

def decode(data):
    require(data[:4]==bytes((10,5,1,8)), 'Unsupported PCX')
    x,y,r,b=struct.unpack_from('<HHHH',data,4)
    width,height=r-x+1,b-y+1
    stride=struct.unpack_from('<H',data,66)[0]
    require(data[65]==1 and stride>=width, 'Invalid PCX layout')
    require(data[-769]==12, 'Missing PCX palette')
    pixels=bytearray(); pos=128
    while pos<len(data)-769:
        value=data[pos]; pos+=1
        if value>=192:
            count=value&63
            require(count>0 and pos<len(data)-769, 'Invalid PCX RLE')
            pixels.extend([data[pos]]*count); pos+=1
        else: pixels.append(value)
    require(len(pixels)==stride*height, 'Incorrect decoded PCX length')
    return width,height,stride,pixels

def validate(folder, source_name=None):
    data=(folder/'fighter.sff').read_bytes()
    require(data[:12]==b'ElecbyteSpr\0', 'SFF signature')
    if data[15] == 2:
        entries = read_sff(data)
        count = len(entries)
    else:
        groups,count,offset,size=struct.unpack_from('<IIII',data,16)
        require(size==32 and offset==512 and count>0, 'SFF header')
        entries={}; end=512
        for i in range(count):
            require(offset==end and offset+32<=len(data), 'SFF chain outside file')
            nxt,length,x,y,g,n,linked,pal=struct.unpack_from('<IIhhHHHB',data,offset)
            end=offset+32+length
            require(end<=len(data) and length>897 and linked==0, 'SFF payload')
            require((g,n) not in entries, 'Duplicate sprite')
            entries[g,n]=(x,y,decode(data[offset+32:end]))
            require(nxt==(end if i<count-1 else 0), 'SFF next offset')
            offset=nxt
        require(end==len(data) and groups==len({g for g,n in entries}), 'SFF count/trailing bytes')
    actual=list(frames((folder/'kfm.air').read_text(encoding='utf-8-sig')))
    inherited=list(frames((root/'engine/chars/kfm/kfm.air').read_text(encoding='utf-8-sig')))
    original=[frame for frame in actual if frame[1] < 7000]
    require(len(original)==len(inherited), 'Inherited animation frame count changed')
    name = source_name or folder.name
    manifest = root/'assets-source/sprites'/name/'manifest.json'
    organic = {}
    if manifest.exists():
        organic = {tuple(f['sprite']): f for f in json.loads(manifest.read_text())['frames'] if f.get('organic')}
    if organic:
        sources = load_overrides(root, name)
        for key in organic:
            require(key in entries, 'Organic frame missing from SFF')
            ox, oy, (w, h, stride, alpha) = entries[key]
            require((ox, oy, w, h, stride) == (160, 240, 320, 320, 320), 'Organic origin/canvas mismatch')
            require(bytes(alpha) == sources[key].getchannel('A').tobytes(), 'Organic alpha/frame integrity mismatch')
    aligned=0
    for current,base in zip(original,inherited):
        _,action,(g,n,dx,dy,duration),flags,boxes=current
        expected_boxes = base[4].copy()
        if (g,n) in organic and 'hurtboxes' in organic[g,n]:
            expected_boxes[2] = [tuple(box) for box in organic[g,n]['hurtboxes']]
        require(current[1]==base[1] and current[2][2:]==base[2][2:] and flags==base[3] and boxes==expected_boxes, 'Combat timing/geometry changed')
        if g<0: continue
        require((g,n) in entries, f'Missing sprite {g},{n}')
        if not boxes[2]: continue
        require(g==30000, f'Unadapted body frame {action}')
        ox,oy,(width,height,stride,pixels)=entries[g,n]
        require((ox, oy) == (160, 240), 'Incorrect normalized sprite origin')
        def visible(x,y):
            x=x-dx; y=y-dy
            if 'H' in flags.upper(): x=-x
            if 'V' in flags.upper(): y=-y
            x+=ox; y+=oy
            return 0<=x<width and 0<=y<height and pixels[y*stride+x]!=0
        if (g,n) in organic:
            occupied=[(i%stride-ox,i//stride-oy) for i,v in enumerate(pixels) if v]
            require(bool(occupied), 'Empty organic frame')
            bounds=[min(x for x,y in occupied),min(y for x,y in occupied),max(x for x,y in occupied)+1,max(y for x,y in occupied)+1]
            require(bounds == organic[g,n]['normalized_bounds'], 'Organic frame bounds/scale/alignment changed')
            for kind in (1, 2):
                for l,t,r,b in boxes[kind]:
                    require(any(visible(x,y) for y in range(t,b+1) for x in range(l,r+1)), f'Organic sprite misses collision box kind {kind}')
            aligned+=1
            continue
        for kind in (1,2):
            for l,t,r,b in boxes[kind]:
                hits=sum(visible(x,y) for y in range(t,b+1) for x in range(l,r+1))
                require(hits==(r-l+1)*(b-t+1), f'Collision coverage: action {action}, sprite {g},{n}, kind {kind}')
        union={(x,y) for l,t,r,b in boxes[1]+boxes[2] for y in range(t,b+1) for x in range(l,r+1)}
        require(sum(value!=0 for value in pixels)==len(union), 'Artwork outside collision silhouette')
        aligned+=1
    specials = [frame for frame in actual if frame[1] >= 7000]
    expected_specials = list(frames(dbz.animations(name == 'vegeta')))
    require(len(specials) == len(expected_specials), 'DBZ animation count changed')
    for current, base in zip(specials, expected_specials):
        _, action, (g,n,dx,dy,duration), flags, boxes = current
        require((g,n) in entries, f'Missing DBZ sprite {g},{n}')
        expected_boxes = base[4].copy()
        if (g,n) in organic and 'hurtboxes' in organic[g,n]:
            expected_boxes[2] = [tuple(box) for box in organic[g,n]['hurtboxes']]
        require(current[1:4] == base[1:4] and boxes == expected_boxes, 'DBZ timing/geometry changed')
        if (g,n) in organic:
            ox,oy,(width,height,stride,pixels) = entries[g,n]
            for kind in (1, 2):
                for l,t,r,b in boxes[kind]:
                    require(any(pixels[(y-dy+oy)*stride+x-dx+ox] for y in range(t,b+1) for x in range(l,r+1)
                                if 0 <= x-dx+ox < width and 0 <= y-dy+oy < height), 'Organic DBZ sprite misses collision box')
    print(f'PASS {folder.name}: {count} sprites, {len(actual)} AIR frames, {aligned} inherited body frames aligned')

if __name__=='__main__':
    for name in ('goku','vegeta'): validate(root/'engine/chars'/name)
    require((root/'engine/Ikemen_GO_Linux').is_file(), 'Engine missing')
    lock=json.loads((root/'docs/engine-lock.json').read_text())
    require(lock['version']=='v1.0.0', 'Engine version lock changed')
    require(hashlib.sha256((root/'engine/Ikemen_GO_Linux').read_bytes()).hexdigest()==lock['executable_sha256'], 'Engine binary hash mismatch')
    print('PASS engine v1.0.0 binary matches pinned SHA256')
