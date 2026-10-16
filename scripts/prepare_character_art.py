#!/usr/bin/env python3
"""Extract reviewed sheets using explicit foot anchors, shared by fighters.

This is deterministic slicing/scaling of supplied artwork, not an art generator.
Keep source sheets and production.json; build_characters consumes manifest.json.
"""
import argparse
import hashlib
import json
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]


def prepare(name):
    folder = ROOT/'assets-source/sprites'/name
    plan = json.loads((folder/'production.json').read_text())
    if not plan['sheets']:
        print(f'{name}: awaiting artist sheets; existing preview retained')
        return
    records = []
    for sheet in plan['sheets']:
        path = (folder/sheet['file']).resolve()
        if not path.is_relative_to(folder.resolve()):
            raise ValueError('Sheet escapes character folder')
        with Image.open(path) as source:
            if source.mode != 'RGBA':
                raise ValueError('Sheet must be RGBA')
            columns = sheet['columns']
            for index, anchor in enumerate(sheet['anchors']):
                rectangle = sheet.get('rectangles', [
                    [round(i*source.width/columns), 0, round((i+1)*source.width/columns), source.height]
                    for i in range(columns)])[index]
                cell = source.crop(rectangle)
                core = cell.getchannel('A').point(lambda alpha: 255 if alpha >= 32 else 0).getbbox()
                if core is None or core[0] == 0 or core[1] == 0 or core[2] == cell.width or core[3] == cell.height:
                    raise ValueError('Source cell cuts visible artwork; review extraction rectangles')
                scale = sheet['scale']
                image = cell.resize((round(cell.width*scale), round(cell.height*scale)), Image.LANCZOS)
                canvas = Image.new('RGBA', (320, 320))
                x, y = 160-round(anchor[0]*scale), 240-round(anchor[1]*scale)
                bounds = image.getchannel('A').getbbox()
                if bounds is not None and sheet.get('grounded', False):
                    y = 240 - bounds[3]
                if bounds is None or min(x+bounds[0], y+bounds[1]) < 1 or max(x+bounds[2], y+bounds[3]) > 319:
                    raise ValueError('Sheet clips normalized canvas')
                canvas.paste(image, (x, y))
                destination = folder/sheet['animation']/f'{index:03}.png'
                destination.parent.mkdir(parents=True, exist_ok=True)
                canvas.save(destination)
                bbox = canvas.getchannel('A').getbbox()
                for key, frame in sheet['bindings']:
                    if frame == index:
                        records.append(dict(sprite=key, file=str(destination.relative_to(folder)),
                                            origin=[160, 240], scale=1, organic=True,
                                            normalized_bounds=[bbox[0]-160, bbox[1]-240, bbox[2]-160, bbox[3]-240],
                                            sha256=hashlib.sha256(destination.read_bytes()).hexdigest()))
    (folder/'manifest.json').write_text(json.dumps(dict(version=1, facing='right', frames=records), indent=2)+'\n')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('name', choices=('goku', 'vegeta'))
    prepare(parser.parse_args().name)
