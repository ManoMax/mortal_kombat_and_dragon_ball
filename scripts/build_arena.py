#!/usr/bin/env python3
"""Original procedural Obsidian Rift arena; no commercial source assets."""
import math
import struct
from pathlib import Path
from PIL import Image, ImageDraw
from build_characters import pcx
ROOT = Path(__file__).resolve().parents[1]


def main():
    chunks = []
    offset = 512
    for layer in range(2):
        image = Image.new('RGB', (640, 240), (12, 10, 26))
        draw = ImageDraw.Draw(image)
        if layer == 0:
            for y in range(240):
                draw.line((0,y,639,y), fill=(14+y//12,10+y//20,30+y//8))
            draw.ellipse((430,20,487,77), fill=(188,104,65))
            for ridge, color in ((0,(34,27,49)),(1,(48,32,50)),(2,(61,38,49))):
                points = [(0,240)] + [(x,100+ridge*22+int(22*math.sin(x*.026+ridge*2)+13*math.cos(x*.053))) for x in range(0,641,8)] + [(640,240)]
                draw.polygon(points,fill=color)
            for x in (80,180,460,560):
                draw.polygon([(x,185),(x+7,94),(x+18,78),(x+29,94),(x+36,185)],fill=(22,18,30))
                draw.line((x+18,95,x+18,161),fill=(212,85,50),width=2)
        else:
            image = Image.new('RGB',(640,56),(34,28,38)); draw=ImageDraw.Draw(image)
            for y in range(56):
                draw.line((0,y,639,y), fill=(57-y//2,46-y//3,48-y//3))
            for y in (0,6,17,35,55): draw.line((0,y,639,y),fill=(112,72,62))
            for x in range(-320,961,64): draw.line((320+(x-320)//3,0,x,55),fill=(15,15,23),width=2)
            draw.line((0,3,639,3), fill=(230,115,64))
        indexed=image.quantize(colors=255,dither=Image.NONE)
        palette=list(zip(*[iter(indexed.getpalette()[:768])]*3))
        data=pcx(bytes(indexed.getdata()),palette,image.width,image.height)
        nxt=offset+32+len(data) if layer==0 else 0
        chunks.append(struct.pack('<IIhhHHHB',nxt,len(data),320,0,0,layer,0,0)+bytes(13)+data)
        offset+=32+len(data)
    header=b'ElecbyteSpr\0'+bytes((0,1,0,1))+struct.pack('<IIII',1,2,512,32)+bytes(480)
    (ROOT/'engine/stages/obsidian.sff').write_bytes(header+b''.join(chunks))
    source=(ROOT/'assets-source/obsidian.def').read_text()
    (ROOT/'engine/stages/obsidian.def').write_text(source)


if __name__ == '__main__': main()
