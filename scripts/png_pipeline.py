"""Reproducible RGBA normalization; AIR remains the collision authority."""
import json
import math
import hashlib
from pathlib import Path
from PIL import Image


def load_overrides(root, name, encode=None):
    manifest = root / 'assets-source' / 'sprites' / name / 'manifest.json'
    if not manifest.exists():
        return {}
    spec = json.loads(manifest.read_text())
    if spec['version'] != 1 or spec['facing'] != 'right':
        raise ValueError('Expected manifest v1, right-facing artwork')
    result = {}
    for frame in spec['frames']:
        key = tuple(frame['sprite'])
        if len(key) != 2 or key in result or not all(type(v) is int and 0 <= v <= 65535 for v in key):
            raise ValueError('Invalid or duplicate sprite ID')
        source = (manifest.parent / frame['file']).resolve()
        if not source.is_relative_to(manifest.parent.resolve()):
            raise ValueError('PNG must stay inside character source directory')
        if frame.get('sha256') and hashlib.sha256(source.read_bytes()).hexdigest() != frame['sha256']:
            raise ValueError('Frame SHA256 mismatch')
        with Image.open(source) as image:
            if image.format != 'PNG' or image.mode != 'RGBA':
                raise ValueError('Source must be RGBA PNG')
            if not (1 <= image.width <= 2048 and 1 <= image.height <= 2048):
                raise ValueError('Invalid source resolution')
            image.load()
            alpha = image.getchannel('A')
            if alpha.getbbox() is None:
                raise ValueError('Empty frame')
            scale = frame.get('scale', 1)
            if type(scale) not in (float, int) or not math.isfinite(scale) or not 0 < scale <= 8:
                raise ValueError('Invalid scale')
            origin = frame['origin']
            if len(origin) != 2 or not all(type(v) is int for v in origin) or not (0 <= origin[0] <= image.width and 0 <= origin[1] <= image.height):
                raise ValueError('Invalid origin')
            width, height = round(image.width * scale), round(image.height * scale)
            if min(width, height) < 1 or max(width, height) > 1024:
                raise ValueError('Invalid normalized resolution')
            if frame.get('resample', 'nearest') not in ('nearest', 'lanczos'):
                raise ValueError('Unknown resampler')
            image = image.resize((width, height), Image.LANCZOS if frame.get('resample') == 'lanczos' else Image.NEAREST)
            canvas = Image.new('RGBA', (320, 320))
            x, y = 160-round(origin[0]*scale), 240-round(origin[1]*scale)
            bounds = image.getchannel('A').getbbox()
            if frame.get('organic', False) and (bounds is None or bounds[0] == 0 or bounds[1] == 0 or bounds[2] == width or bounds[3] == height):
                raise ValueError('Organic frame touches source edge; possible crop')
            if bounds is None or x+bounds[0] < 0 or y+bounds[1] < 0 or x+bounds[2] > 320 or y+bounds[3] > 320:
                raise ValueError('Normalized artwork clips canvas')
            canvas.paste(image, (x, y))
            if frame.get('organic'):
                bbox = canvas.getchannel('A').getbbox()
                actual = [bbox[0]-160, bbox[1]-240, bbox[2]-160, bbox[3]-240]
                if frame.get('normalized_bounds') != actual:
                    raise ValueError('Organic frame bounds/scale/origin mismatch')
                if frame.get('facing', spec['facing']) != 'right':
                    raise ValueError('Artwork must face right')
            if 'hurtboxes' in frame:
                boxes = frame['hurtboxes']
                if not isinstance(boxes, list) or not 1 <= len(boxes) <= 10:
                    raise ValueError('Invalid hurtboxes')
                for box in boxes:
                    if len(box) != 4 or any(type(v) is not int or abs(v) > 320 for v in box) or box[0] >= box[2] or box[1] >= box[3]:
                        raise ValueError('Invalid hurtbox coordinates')
            if encode is None:
                result[key] = canvas
                continue
            if set(canvas.getchannel('A').getdata()) - {0, 255}:
                raise ValueError('Legacy PCX cannot preserve partial alpha; use SFF v2')
            # Reserve index zero for alpha; each PCX carries its own palette.
            indexed = canvas.convert('RGB').quantize(colors=255, dither=Image.NONE)
            palette = [(0, 0, 0)] + list(zip(*[iter(indexed.getpalette()[:765])]*3))
            pixels = bytes(v+1 if a else 0 for v, a in zip(indexed.getdata(), canvas.getchannel('A').getdata()))
            result[key] = encode(pixels, palette, 320, 320)
    return result
