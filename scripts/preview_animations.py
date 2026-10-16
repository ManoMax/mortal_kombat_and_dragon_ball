#!/usr/bin/env python3
"""Build a labelled art contact sheet; this is an asset preview, not gameplay."""
import json
from pathlib import Path
from PIL import Image, ImageDraw
ROOT=Path(__file__).resolve().parents[1]
for name in ('goku','vegeta'):
    folder=ROOT/'assets-source/sprites'/name
    sheets=json.loads((folder/'production.json').read_text())['sheets']
    result=Image.new('RGB',(640,160*len(sheets)),(35,35,40));draw=ImageDraw.Draw(result)
    for row,sheet in enumerate(sheets):
        for i in range(4):
            with Image.open(folder/sheet['animation']/f'{i:03}.png') as image:
                cell=image.crop((80,90,240,250))
                result.paste(cell,(i*160,row*160),cell)
            draw.line((i*160,row*160+150,(i+1)*160-1,row*160+150),fill=(80,160,80))
        draw.text((4,row*160+2),sheet['animation'],fill=(255,255,255))
    result.save(ROOT/'tests'/f'sprint5-{name}-contact.png')
