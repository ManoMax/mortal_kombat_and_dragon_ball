#!/usr/bin/env python3
"""Build original RGBA sprites and noncommercial KFM-derived fighters."""
from pathlib import Path
import re, struct, shutil, json
from io import BytesIO
from PIL import Image
from sff_rgba import write_sff
from air_geometry import frames, apply_hurtboxes
import dbz_combat as dbz
from png_pipeline import load_overrides
ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / 'engine/chars/kfm'
W,H=160,120

def pcx(pixels, palette, width=W, height=H):
    header=bytearray(128)
    struct.pack_into('<BBBBHHHHHH',header,0,10,5,1,8,0,0,width-1,height-1,width,height)
    header[65]=1
    struct.pack_into('<HH',header,66,width,1)
    data=bytearray(header)
    # PCX runs may not cross scanlines; compress transparent padding too.
    for row in range(height):
        scan=pixels[row*width:(row+1)*width]
        i=0
        while i<width:
            value=scan[i]; run=1
            while i+run<width and run<63 and scan[i+run]==value: run+=1
            if run>1 or value>=192: data.append(192|run)
            data.append(value); i+=run
    return bytes(data)+b'\x0c'+bytes(sum(palette,()))+bytes(768-3*len(palette))

def sprite(group, frame, vegeta, geometry=None):
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
        # Base artwork at (44,110); frame geometry is applied below.
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
    palette=dbz.palette(vegeta)
    if geometry:
        # Fit each frame independently: sprite IDs alone do not identify a pose.
        boxes, dx, dy, flip, _, _ = geometry
        body = boxes[2]
        if body:
            left=min(b[0] for b in body); top=min(b[1] for b in body)
            right=max(b[2] for b in body); bottom=max(b[3] for b in body)
            occupied=[(i%W,i//W) for i,v in enumerate(p) if v]
            sx=min(x for x,y in occupied); sy=min(y for x,y in occupied)
            sw=max(x for x,y in occupied)-sx+1; sh=max(y for x,y in occupied)-sy+1
            old=p; p=bytearray(320*320)
            def paint(x,y,c):
                # AIR flip transforms artwork; collision coordinates stay local.
                x = -(x-dx) if 'H' in flip.upper() else x-dx
                y = -(y-dy) if 'V' in flip.upper() else y-dy
                xx=x+160; yy=y+240
                if not (0<=xx<320 and 0<=yy<320):
                    raise ValueError(f'Pose outside canvas: {group}, {frame}, {xx}, {yy}')
                p[yy*320+xx]=c
            for y in range(top,bottom+1):
                for x in range(left,right+1):
                    c=old[(sy+(y-top)*sh//(bottom-top+1))*W+sx+(x-left)*sw//(right-left+1)]
                    if any(l<=x<=r and t<=y<=b for l,t,r,b in body):
                        paint(x,y, (5 if vegeta else 3) if x == left or y == top else c or 2)
            # Original placeholder fists/feet follow active attack reach.
            for l,t,r,b in boxes[1]:
                for y in range(t,b+1):
                    for x in range(l,r+1): paint(x,y,1)
    return pcx(p,palette,320,320) if geometry else pcx(p,palette)

def sff(path, entries, vegeta, poses, overrides=None):
    overrides = overrides or {}
    sprites = []
    for g, i in entries:
        pose = poses.get((g, i))
        if (g, i) in overrides:
            image = overrides[g, i]
        else:
            data = dbz.effect(g, i, vegeta, pcx) if (g, i) in dbz.ENTRIES else sprite(pose[4] if pose else g, pose[5] if pose else i, vegeta, pose)
            with Image.open(BytesIO(data)) as indexed:
                image = indexed.convert('RGBA')
                image.putalpha(Image.frombytes('L', indexed.size, bytes(255 if v else 0 for v in indexed.getdata())))
        origin = (160, 240) if pose or (g, i) in overrides else (80, 110) if (g, i) in dbz.ENTRIES else (44, 110)
        sprites.append(((g, i), origin, image))
    write_sff(path, sprites)

def main():
    air=(BASE/'kfm.air').read_text(encoding='utf-8-sig')
    entries=sorted({tuple(map(int,m)) for m in re.findall(r'^\s*(\d+)\s*,\s*(\d+)\s*,',air,re.M)}|{(9000,0),(9000,1)})
    lines=air.splitlines(); poses={}
    for number, (line, action, values, flags, boxes) in enumerate(frames(air)):
        g,i,dx,dy,duration=values
        if g < 0 or not boxes[2]: continue
        key=(30000,number)
        poses[key]=(boxes,dx,dy,flags,g,i)
        lines[line]=f'{key[0]},{key[1]}, {dx},{dy}, {duration}{flags}'
    adapted='\n'.join(lines)+'\n'
    entries=sorted(set(entries)|set(poses)|set(dbz.ENTRIES))
    for name in ('goku','vegeta'):
        dest=ROOT/'engine/chars'/name; dest.mkdir(exist_ok=True)
        for f in ('kfm.cmd','kfm.cns','kfm.air','kfm.snd','readme.txt','movelist.dat'):
            shutil.copy2(BASE/f,dest/f)
        overrides = load_overrides(ROOT, name)
        manifest = ROOT/'assets-source/sprites'/name/'manifest.json'
        spec = json.loads(manifest.read_text()) if manifest.exists() else {'frames': []}
        hurtboxes = {tuple(f['sprite']): f['hurtboxes'] for f in spec['frames'] if 'hurtboxes' in f}
        (dest/'kfm.air').write_text(apply_hurtboxes(adapted+dbz.animations(name=='vegeta'), hurtboxes))
        (dest/'kfm.cmd').write_text(dbz.command_layer((dest/'kfm.cmd').read_text(encoding='utf-8-sig')))
        cns=(dest/'kfm.cns').read_text(encoding='utf-8-sig')
        cns=cns.replace('type = PosFreeze\ntrigger1 = 1\nx = 1\ny = 1','type = PosFreeze\ntrigger1 = 1')
        cns=cns.replace('walk.fwd  = 2.4','walk.fwd  = 2.8').replace('walk.back = -2.2','walk.back = -2.5')
        (dest/'kfm.cns').write_text(cns+dbz.states(name))
        definition=(BASE/'kfm.def').read_text()
        definition=definition.replace('"Kung Fu Man"',f'"{name.title()} (Prototype)"').replace('sprite  = kfm.sff','sprite  = fighter.sff')
        definition=definition.split('; Arcade mode')[0]
        definition=definition.replace('author = "Elecbyte"','author = "DBZ-MK; combat derived from Elecbyte KFM"')
        (dest/f'{name}.def').write_text(definition)
        if set(overrides) - (set(poses) | set(dbz.ENTRIES)):
            raise ValueError('PNG overrides must target known AIR context/effect IDs')
        sff(dest/'fighter.sff',entries,name=='vegeta',poses,overrides)
    print(f'Built 2 fighters, {len(entries)} original sprite entries each.')
if __name__=='__main__': main()
