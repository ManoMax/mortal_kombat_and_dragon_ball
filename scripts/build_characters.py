#!/usr/bin/env python3
"""Build original indexed sprites and noncommercial KFM-derived fighters."""
from pathlib import Path
import re, struct, shutil
ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / 'engine/chars/kfm'
W,H=160,120

def pcx(pixels, palette):
    header=bytearray(128)
    struct.pack_into('<BBBBHHHHHH',header,0,10,5,1,8,0,0,W-1,H-1,W,H)
    header[65]=1
    struct.pack_into('<HH',header,66,W,1)
    data=bytearray(header)
    for value in pixels:
        if value>=192: data.append(193)
        data.append(value)
    return bytes(data)+b'\x0c'+bytes(sum(palette,()))+bytes(768-3*len(palette))

def sprite(group, frame, vegeta):
    p=bytearray(W*H)
    def rect(x,y,w,h,c):
        for yy in range(max(0,y),min(H,y+h)):
            for xx in range(max(0,x),min(W,x+w)): p[yy*W+xx]=c
    def limb(x,y,x2,y2,width,c):
        steps=max(abs(x2-x),abs(y2-y),1)
        for i in range(steps+1): rect(round(x+(x2-x)*i/steps),round(y+(y2-y)*i/steps),width,width,c)
    crouch=group in (11,400,410,430,440)
    dy=24 if crouch else (frame%3 if group in (0,20,21) else 0)
    if group in (5100,5110,5120,5170):
        rect(20,98,64,12,2); rect(75,94,15,16,1)
    else:
        # Origin is (44,110); silhouette matches the inherited 90px hurtboxes.
        y=22+dy
        rect(35,y,19,20,1)
        rect(33,y-7,23,9,4)
        for i in range(5): limb(33+i*5,y-4,30+i*5,y-15-(i%2)*5,4,4)
        rect(51,y+7,4,3,4)
        rect(30,y+21,29,30,2)
        if vegeta: rect(33,y+22,22,19,5)
        rect(29,y+48,31,5,3)
        kick=group in (230,240,430,440,630,640) and frame>0
        walk=6 if group in (20,21,100) and frame%2 else 0
        limb(32,y+52,25-walk,101,9,2)
        limb(49,y+52,86 if kick else 54+walk, y+48 if kick else 101,9,2)
        rect(22-walk,103,18,7,3)
        if kick: rect(86,y+47,15,9,3)
        else: rect(52+walk,103,18,7,3)
        punch=group in (200,210,400,410,600,610,1000,1010,1020) and frame>0
        guard=120<=group<=152
        limb(30,y+24,24,y+43,7,1)
        limb(53,y+24,96 if punch else 60,y+26 if punch else y+12 if guard else y+38,7,1)
        rect(25,y+39,10,8,3)
        rect(95 if punch else 59,y+24 if punch else y+10 if guard else y+36,10,9,1)
    palette=((0,0,0),(245,183,125),(43,76,172) if vegeta else (239,112,26),(231,231,220) if vegeta else (27,52,122),(21,22,31),(220,199,133))
    return pcx(p,palette)

def sff(path, entries, vegeta):
    chunks=[]; offset=512
    for n,(g,i) in enumerate(entries):
        data=sprite(g,i,vegeta)
        next_offset=offset+32+len(data) if n<len(entries)-1 else 0
        chunks.append(struct.pack('<IIhhHHHB',next_offset,len(data),44,110,g,i,0,0)+bytes(13)+data)
        offset+=32+len(data)
    header=b'ElecbyteSpr\0'+bytes((0,1,0,1))+struct.pack('<IIII',len(set(g for g,i in entries)),len(entries),512,32)+bytes(480)
    path.write_bytes(header+b''.join(chunks))

def main():
    air=(BASE/'kfm.air').read_text(encoding='utf-8-sig')
    entries=sorted({tuple(map(int,m)) for m in re.findall(r'^\s*(\d+)\s*,\s*(\d+)\s*,',air,re.M)}|{(9000,0),(9000,1)})
    for name in ('goku','vegeta'):
        dest=ROOT/'engine/chars'/name; dest.mkdir(exist_ok=True)
        for f in ('kfm.cmd','kfm.cns','kfm.air','kfm.snd','readme.txt','movelist.dat'):
            shutil.copy2(BASE/f,dest/f)
        cns=(dest/'kfm.cns').read_text(encoding='utf-8-sig')
        cns=cns.replace('type = PosFreeze\ntrigger1 = 1\nx = 1\ny = 1','type = PosFreeze\ntrigger1 = 1')
        (dest/'kfm.cns').write_text(cns)
        definition=(BASE/'kfm.def').read_text()
        definition=definition.replace('"Kung Fu Man"',f'"{name.title()} (Prototype)"').replace('sprite  = kfm.sff','sprite  = fighter.sff')
        definition=definition.split('; Arcade mode')[0]
        definition=definition.replace('author = "Elecbyte"','author = "DBZ-MK; combat derived from Elecbyte KFM"')
        (dest/f'{name}.def').write_text(definition)
        sff(dest/'fighter.sff',entries,name=='vegeta')
    print(f'Built 2 fighters, {len(entries)} original sprite entries each.')
if __name__=='__main__': main()
