#!/usr/bin/env python3
"""Check essential organic coverage and report remaining inherited placeholders.

This certifies asset integrity and measurable alignment, never art approval.
"""
import argparse
from collections import defaultdict
import hashlib
import json
from pathlib import Path
from PIL import Image
from air_geometry import frames

ROOT = Path(__file__).resolve().parents[1]
ESSENTIAL = (0,10,11,12,20,21,40,41,42,43,47,120,121,122,130,131,132,
             140,141,142,150,151,152,181,200,210,230,240,400,410,430,440,
             600,610,630,640,5000,5010,5030,5035,5040,5050,5080,5100,5110,5120,7000,7100)


def inspect(name, complete=False):
    folder = ROOT/'assets-source/sprites'/name
    manifest = json.loads((folder/'manifest.json').read_text())
    organic = {tuple(f['sprite']): f for f in manifest['frames'] if f.get('organic')}
    actions = defaultdict(list)
    for _, action, values, flags, boxes in frames((ROOT/'engine/chars'/name/'kfm.air').read_text()):
        if values[0] >= 0 and (values[0] == 30000 or action in (170,230,810,820,7000,7100)):
            actions[action].append(tuple(values[:2]))
    missing = {str(a): [list(k) for k in keys if k not in organic]
               for a, keys in actions.items() if any(k not in organic for k in keys)}
    for action in ESSENTIAL:
        if action not in actions or str(action) in missing:
            raise ValueError(f'{name}: essential action {action} contains missing/placeholder sprites')
    if complete and missing:
        raise ValueError(f'{name}: inherited body placeholders remain: {sorted(missing)}')
    plan = json.loads((folder/'production.json').read_text())
    for sheet in plan['sheets']:
        hashes, heights = set(), []
        for index in range(len(sheet['anchors'])):
            path = folder/sheet['animation']/f'{index:03}.png'
            with Image.open(path) as image:
                if image.mode != 'RGBA' or image.size != (320,320):
                    raise ValueError('Invalid normalized RGBA frame')
                bounds = image.getchannel('A').getbbox()
                if bounds is None or min(bounds[:2]) < 1 or max(bounds[2:]) > 319:
                    raise ValueError('Empty or clipped normalized frame')
                if sheet.get('grounded') and bounds[3] != 240:
                    raise ValueError('Grounded feet are not on origin baseline')
                hashes.add(hashlib.sha256(image.tobytes()).hexdigest())
                heights.append(bounds[3]-bounds[1])
        if len(hashes) < 3:
            raise ValueError(f'{name}/{sheet["animation"]}: insufficient distinct drawings')
        if sheet['animation'] in ('idle','walk') and max(heights)-min(heights) > 8:
            raise ValueError('Locomotion scale drift exceeds 8 pixels')
    return dict(character=name, organic_bindings=len(organic),
                essential_actions=list(ESSENTIAL), remaining_placeholders=missing,
                human_art_acceptance='pending',
                source_sha256={s['file']: hashlib.sha256((folder/s['file']).read_bytes()).hexdigest()
                               for s in plan['sheets']})


if __name__ == '__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--report', type=Path)
    parser.add_argument('--complete', action='store_true', help='Reject placeholders in every inherited body action')
    args=parser.parse_args()
    report={n:inspect(n,args.complete) for n in ('goku','vegeta')}
    if args.report: args.report.write_text(json.dumps(report,indent=2)+'\n')
    for name, data in report.items():
        print(f'PASS {name}: {data["organic_bindings"]} organic bindings; all essential actions; '
              f'{len(data["remaining_placeholders"])} inherited actions still need art; human acceptance pending')
