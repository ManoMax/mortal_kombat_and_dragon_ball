#!/usr/bin/env python3
"""Export AIR-space comparisons and sequences. Asset previews, never gameplay."""
import argparse
import csv
import re
from collections import defaultdict
import hashlib
import json
from pathlib import Path
from PIL import Image, ImageDraw, ImageChops
from air_geometry import frames

ROOT = Path(__file__).resolve().parents[1]


def placed(image, origin, values, flags, facing=1):
    """Apply AIR flips/offsets and facing to RGBA pixels around the player axis."""
    result = Image.new('RGBA', (320, 320))
    bounds = image.getchannel('A').getbbox()
    if bounds is None:
        raise ValueError('Empty body frame')
    crop = image.crop(bounds)
    x = bounds[0]-origin[0]
    y = bounds[1]-origin[1]
    if 'H' in flags.upper():
        x = origin[0]-(bounds[2]-1)
        crop = crop.transpose(Image.FLIP_LEFT_RIGHT)
    if 'V' in flags.upper():
        y = origin[1]-(bounds[3]-1)
        crop = crop.transpose(Image.FLIP_TOP_BOTTOM)
    x += values[2]
    y += values[3]
    if facing == -1:
        x = -(x+crop.width-1)
        crop = crop.transpose(Image.FLIP_LEFT_RIGHT)
    tx,ty = 160+x,240+y
    if tx < 0 or ty < 0 or tx+crop.width > 320 or ty+crop.height > 320:
        raise ValueError('Preview clips transformed artwork')
    result.paste(crop,(tx,ty))
    return result


def metrics(image):
    alpha = image.getchannel('A').point(lambda a: 255 if a >= 32 else 0)
    bounds = alpha.getbbox()
    if bounds is None:
        raise ValueError('Empty body frame')
    # Contact band is a measurement, not a semantic identification of either foot.
    band = alpha.crop((0, bounds[3]-3, 320, bounds[3])).getbbox()
    return dict(bounds=list(bounds), bottom=bounds[3]-240,
                contact_center=(band[0]+band[2])/2-160,
                alpha_sha256=hashlib.sha256(alpha.tobytes()).hexdigest())


def inspect(name, output, selected, boxes=False):
    folder = ROOT/'assets-source/sprites'/name
    manifest = json.loads((folder/'manifest.json').read_text())
    entries = {tuple(f['sprite']): f for f in manifest['frames'] if f.get('organic')}
    plan = json.loads((folder/'production.json').read_text())
    families = {tuple(key): s['animation'] for s in plan['sheets'] for key, index in s['bindings']}
    actions = defaultdict(list)
    for _, action, values, flags, collision in frames((ROOT/'engine/chars'/name/'kfm.air').read_text()):
        actions[action].append((values, flags, collision))
    report = dict(character=name, human_acceptance='pending', actions={})
    cache = {}
    for action, sequence in actions.items():
        records, previews = [], []
        previous_alpha = None
        for index, (values, flags, collision) in enumerate(sequence):
            entry = entries.get(values[:2])
            record = dict(frame=index, sprite=list(values[:2]), ticks=values[4],
                          hitboxes=collision[1], hurtboxes=collision[2],
                          source_family=families.get(values[:2]), organic=entry is not None)
            if entry:
                key = (entry['file'], tuple(entry['origin']), values[2:4], flags)
                if key not in cache:
                    with Image.open(folder/entry['file']) as image:
                        cache[key] = (placed(image, entry['origin'], values, flags),
                                      placed(image, entry['origin'], values, flags, -1))
                right, left = cache[key]
                record.update(metrics(right))
                record['left_bounds'] = metrics(left)['bounds']
                if previous_alpha is not None:
                    record['alpha_change_pixels'] = sum(v != 0 for v in ImageChops.difference(right.getchannel('A'), previous_alpha).getdata())
                previous_alpha = right.getchannel('A')
                previews.append((right, left, collision, values[4]))
            records.append(record)
        active = [i for i, r in enumerate(records) if r['hitboxes']]
        report['actions'][str(action)] = dict(frames=records,
            active_frame_indices=active,
            air_box_startup_ticks=sum(r['ticks'] for r in records[:active[0]]) if active else None,
            air_box_recovery_ticks=sum(r['ticks'] for r in records[active[-1]+1:]) if active else None,
            indefinite=any(r['ticks'] < 0 for r in records),
            choreography='inherited KFM contract; source families do not certify matching motion')
        if action not in selected or not previews:
            continue
        rendered = []
        for index, (right, left, collision, ticks) in enumerate(previews):
            canvas = Image.new('RGB', (640, 320), (30, 30, 38))
            draw = ImageDraw.Draw(canvas)
            for side, image in enumerate((right, left)):
                canvas.paste(image, (side*320, 0), image)
                draw.line((side*320, 240, side*320+319, 240), fill='green')
                draw.line((side*320+160, 0, side*320+160, 319), fill=(70,70,90))
                if boxes:
                    facing = 1 if side == 0 else -1
                    for kind in (2, 1):
                        for x,y,r,b in collision[kind]:
                            a,c = sorted((160+facing*x,160+facing*r))
                            draw.rectangle((side*320+a,240+y,side*320+c,240+b), outline='red' if kind == 1 else 'cyan')
            draw.text((5,5), f'{name} AIR {action} frame {index} ticks {ticks}; asset preview', fill='white')
            rendered.append(canvas)
        sheet = Image.new('RGB', (640*min(4,len(rendered)),320*((len(rendered)+3)//4)))
        for i, image in enumerate(rendered):
            sheet.paste(image, ((i%4)*640,(i//4)*320))
        sheet.save(output/f'{name}-{action}-frames.png')
        rendered[0].save(output/f'{name}-{action}.gif', save_all=True, append_images=rendered[1:],
                         duration=[round(max(1,p[3])*1000/60) if p[3]>=0 else 1000 for p in previews], loop=0)
    # Preserve expressions and triggers: AIR boxes alone do not establish HitDef timing.
    contracts = {}
    for filename in ('kfm.cns','kfm.cmd'):
        text = (ROOT/'engine/chars'/name/filename).read_text(encoding='utf-8-sig')
        blocks = re.split(r'(?=^\[)', text, flags=re.M)
        contracts[filename] = [b for b in blocks if re.search(
            r'type\s*=\s*(HitDef|Projectile|TargetBind|TargetState|TargetVelSet|ChangeState|HitOverride)\b', b, re.I)]
    report['state_contracts'] = contracts
    original = (ROOT/'engine/chars/kfm/kfm.cns').read_text(encoding='utf-8-sig')
    inherited = set(re.findall(r'^\[Statedef\s+(-?\d+)\]',original,re.I|re.M))
    text = (ROOT/'engine/chars'/name/'kfm.cns').read_text(encoding='utf-8-sig')
    report['state_inventory'] = []
    for block in re.split(r'(?=^\[Statedef)',text,flags=re.I|re.M):
        match = re.match(r'\[Statedef\s+(-?\d+)\]',block,re.I)
        if not match: continue
        anim = re.search(r'^anim\s*=\s*([^;\n]+)',block,re.I|re.M)
        expression = anim[1].strip() if anim else None
        action = report['actions'].get(expression,{})
        report['state_inventory'].append(dict(state=int(match[1]),
            origin='inherited KFM' if match[1] in inherited else 'DBZ layer',
            animation_expression=expression,
            source_families=sorted({f['source_family'] for f in action.get('frames',[]) if f['source_family']})))
    common = ROOT/'engine/data/common1.cns.zss'
    report['common_states'] = dict(file=str(common.relative_to(ROOT)),
        sha256=hashlib.sha256(common.read_bytes()).hexdigest(),
        note='Engine default common states; dynamic animation selection is not resolved by this static tool')
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, default=ROOT/'evidence/sprint6/assets')
    parser.add_argument('--actions', default='0,20,21,40,47,200,210,230,240,5100,5120,7100')
    parser.add_argument('--hitboxes', action='store_true')
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    reports = [inspect(n,args.output,set(map(int,args.actions.split(','))),args.hitboxes) for n in ('goku','vegeta')]
    (args.output/'inspection.json').write_text(json.dumps(reports,indent=2)+'\n')
    with (args.output/'feet.csv').open('w', newline='') as stream:
        writer = csv.writer(stream)
        writer.writerow(('character','action','frame','source_family','bottom_y','contact_center_x','alpha_change_pixels'))
        for report in reports:
            for action, data in report['actions'].items():
                for frame in data['frames']:
                    if 'bottom' in frame:
                        writer.writerow((report['character'],action,frame['frame'],frame['source_family'],frame['bottom'],frame['contact_center'],frame.get('alpha_change_pixels','')))
    with (args.output/'kfm-state-inventory.csv').open('w', newline='') as stream:
        writer = csv.writer(stream)
        writer.writerow(('character','state','origin','animation_expression','source_families'))
        for report in reports:
            for state in report['state_inventory']:
                writer.writerow((report['character'],state['state'],state['origin'],state['animation_expression'],'|'.join(state['source_families'])))
    print('Exported AIR previews and measurements; human acceptance pending')

if __name__ == '__main__':
    main()
