#!/usr/bin/env python3
"""Compare preserved Sprint 6 drawings with integrated walk candidates.

These are source previews, not engine footage or artistic acceptance.
"""
import hashlib
import json
from pathlib import Path
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'evidence/sprint7'


def cell(path):
    with Image.open(path) as source:
        return source.crop((96, 124, 224, 244)).resize((256, 240), Image.NEAREST)


def main():
    output = OUT / 'assets'
    output.mkdir(parents=True, exist_ok=True)
    records = {}
    for name in ('goku', 'vegeta'):
        folder = ROOT / 'assets-source/sprites' / name
        comparison = Image.new('RGB', (1024, 540), (29, 29, 37))
        draw = ImageDraw.Draw(comparison)
        frames = []
        for phase in range(4):
            old = OUT / 'baseline' / f'{name}-walk-{phase:03}.png'
            new = folder / 'walk_sprint7' / f'{phase:03}.png'
            for row, path in enumerate((old, new)):
                pose = cell(path)
                comparison.paste(pose, (phase * 256, row * 270 + 24), pose)
                draw.line((phase*256, row*270+256, phase*256+255, row*270+256), fill=(75, 155, 85))
            draw.text((phase*256+8, 6), f'{name} Sprint 6 / {phase}', fill='white')
            draw.text((phase*256+8, 276), f'Sprint 7 candidate / {phase}', fill='white')
            gif = Image.new('RGB', (256, 270), (29, 29, 37))
            pose = cell(new)
            gif.paste(pose, (0, 24), pose)
            ImageDraw.Draw(gif).text((8, 6), f'{name} source preview {phase}', fill='white')
            frames.append(gif)
        comparison.save(output / f'{name}-walk-before-after.png')
        # Four drawings, each held for 12 ticks by the unchanged AIR contract.
        frames[0].save(output / f'{name}-walk-source.gif', save_all=True,
                       append_images=frames[1:], duration=200, loop=0)
        records[name] = {'new_drawings': 4, 'artistic_acceptance': 'blocked',
                         'sha256': {f'{i:03}.png': hashlib.sha256(
                             (folder / 'walk_sprint7' / f'{i:03}.png').read_bytes()).hexdigest()
                             for i in range(4)}}
    contracts = json.loads((OUT / 'baseline/contracts.json').read_text())
    for path, expected in contracts['combat_sha256'].items():
        if hashlib.sha256((ROOT / path).read_bytes()).hexdigest() != expected:
            raise ValueError(f'Combat/AIR contract changed: {path}')
    (OUT / 'drawings.json').write_text(json.dumps(records, indent=2) + '\n')
    print('Exported before/after source previews; CNS/CMD/AIR hashes preserved')


if __name__ == '__main__':
    main()
