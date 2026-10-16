#!/usr/bin/env python3
"""Extract reviewed sheets using explicit foot anchors, shared by fighters.

This is deterministic slicing/scaling of supplied artwork, not an art generator.
Keep source sheets and production.json; build_characters consumes manifest.json.
"""
import argparse
import hashlib
import json
from pathlib import Path
from PIL import Image, ImageFilter, ImageChops

ROOT = Path(__file__).resolve().parents[1]


def isolate(source, seed):
    """Slice one connected RGBA drawing; keep its original partial alpha.

    Explicit source seeds disambiguate staggered sheets whose rectangular
    cells overlap. This never synthesizes, stretches or repaints a pose.
    """
    width, height = source.size
    x, y = seed
    if not (0 <= x < width and 0 <= y < height):
        raise ValueError('Component seed outside source')
    alpha = source.getchannel('A').tobytes()
    start = y*width+x
    if alpha[start] < 32:
        raise ValueError('Component seed is transparent')
    pending = [start]
    visited = {start}
    mask = bytearray(width*height)
    while pending:
        index = pending.pop()
        mask[index] = 255
        x, y = index % width, index // width
        neighbors = ([index-1] if x else []) + ([index+1] if x+1 < width else [])
        neighbors += ([index-width] if y else []) + ([index+width] if y+1 < height else [])
        for neighbor in neighbors:
            if alpha[neighbor] >= 32 and neighbor not in visited:
                visited.add(neighbor)
                pending.append(neighbor)
    result = source.copy()
    # Retain the two-pixel antialiased fringe, exclude disconnected sheet debris.
    region = Image.frombytes('L', source.size, bytes(mask)).filter(ImageFilter.MaxFilter(5))
    result.putalpha(ImageChops.multiply(source.getchannel('A'), region))
    return result


def compensate(canvas, dx, dy, flags):
    """Inverse AIR offsets/flips around the normalized origin, without scaling."""
    result = Image.new('RGBA', canvas.size)
    source, target = canvas.load(), result.load()
    for y in range(canvas.height):
        for x in range(canvas.width):
            if not source[x, y][3]:
                continue
            tx, ty = x-160-dx, y-240-dy
            if 'H' in flags.upper(): tx = -tx
            if 'V' in flags.upper(): ty = -ty
            tx, ty = tx+160, ty+240
            if not (1 <= tx < 319 and 1 <= ty < 319):
                raise ValueError('AIR compensation clips artwork')
            target[tx, ty] = source[x, y]
    return result


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
                drawing = isolate(source, sheet['seeds'][index]) if 'seeds' in sheet else source
                # A crop must contain the entire visible connected drawing.
                if 'seeds' in sheet:
                    full = drawing.getchannel('A').point(lambda a: 255 if a >= 32 else 0).getbbox()
                    if full is None or not (rectangle[0] < full[0] and rectangle[1] < full[1]
                                            and rectangle[2] > full[2] and rectangle[3] > full[3]):
                        raise ValueError('Source rectangle cuts isolated artwork')
                cell = drawing.crop(rectangle)
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
                        asset = destination
                        adjustment = sheet.get('context_adjustments', {}).get(','.join(map(str, key)))
                        final = canvas
                        placement = sheet.get('binding_placements', {}).get(','.join(map(str, key)))
                        if placement:
                            final = compensate(final, -placement[0], -placement[1], '')
                        if adjustment:
                            final = compensate(final, *adjustment)
                        if adjustment or placement:
                            asset = destination.with_name(f'{index:03}-{key[0]}-{key[1]}.png')
                            final.save(asset)
                        bbox = final.getchannel('A').getbbox()
                        records.append(dict(sprite=key, file=str(asset.relative_to(folder)),
                                            origin=[160, 240], scale=1, organic=True,
                                            normalized_bounds=[bbox[0]-160, bbox[1]-240, bbox[2]-160, bbox[3]-240],
                                            sha256=hashlib.sha256(asset.read_bytes()).hexdigest()))
                        hurtboxes = sheet.get('hurtbox_overrides', {}).get(','.join(map(str, key)))
                        if hurtboxes is not None:
                            records[-1]['hurtboxes'] = hurtboxes
    (folder/'manifest.json').write_text(json.dumps(dict(version=1, facing='right', frames=records), indent=2)+'\n')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('name', choices=('goku', 'vegeta'))
    prepare(parser.parse_args().name)
