"""Reproducible RGBA PNG import for SFF v1; AIR remains the collision authority."""
import json
from pathlib import Path
from PIL import Image


def load_overrides(root, name, encode):
    manifest = root / 'assets-source' / 'sprites' / name / 'manifest.json'
    if not manifest.exists():
        return {}
    spec = json.loads(manifest.read_text())
    if spec['version'] != 1 or spec['facing'] != 'right':
        raise ValueError('Expected manifest v1, right-facing artwork')
    result = {}
    for frame in spec['frames']:
        key = tuple(frame['sprite'])
        if len(key) != 2 or key in result or not all(isinstance(v, int) and 0 <= v <= 65535 for v in key):
            raise ValueError('Invalid or duplicate sprite ID')
        source = (manifest.parent / frame['file']).resolve()
        if not source.is_relative_to(manifest.parent.resolve()):
            raise ValueError('PNG must stay inside character source directory')
        with Image.open(source) as image:
            if image.format != 'PNG' or image.mode != 'RGBA':
                raise ValueError('Source must be RGBA PNG')
            if not (1 <= image.width <= 2048 and 1 <= image.height <= 2048):
                raise ValueError('Invalid source resolution')
            image.load()
            alpha = image.getchannel('A')
            if alpha.getextrema() != (0, 255) or set(alpha.getdata()) - {0, 255}:
                raise ValueError('SFF v1 requires binary transparency and visible pixels')
            scale = frame.get('scale', 1)
            if not isinstance(scale, (float, int)) or not 0 < scale <= 8:
                raise ValueError('Invalid scale')
            origin = frame['origin']
            if len(origin) != 2 or not all(isinstance(v, int) for v in origin):
                raise ValueError('Invalid origin')
            width, height = round(image.width * scale), round(image.height * scale)
            if min(width, height) < 1 or max(width, height) > 1024:
                raise ValueError('Invalid normalized resolution')
            image = image.resize((width, height), Image.NEAREST)
            canvas = Image.new('RGBA', (320, 320))
            x, y = 160-round(origin[0]*scale), 240-round(origin[1]*scale)
            bounds = image.getbbox()
            if bounds is None or x+bounds[0] < 0 or y+bounds[1] < 0 or x+bounds[2] > 320 or y+bounds[3] > 320:
                raise ValueError('Normalized artwork clips canvas')
            canvas.paste(image, (x, y))
            # Reserve index zero for alpha; each PCX carries its own palette.
            indexed = canvas.convert('RGB').quantize(colors=255, dither=Image.NONE)
            palette = [(0, 0, 0)] + list(zip(*[iter(indexed.getpalette()[:765])]*3))
            pixels = bytes(v+1 if a else 0 for v, a in zip(indexed.getdata(), canvas.getchannel('A').getdata()))
            result[key] = encode(pixels, palette, 320, 320)
    return result
