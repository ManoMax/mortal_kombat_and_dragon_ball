"""Resolve AIR collision defaults and one-frame overrides (including empty sets)."""
import re

def frames(text):
    defaults = {1: [], 2: []}
    pending = {}
    target = None
    action = None
    expected = None
    def check_count():
        if target is not None and len(target) != expected:
            raise ValueError('Collision count does not match declaration')
    for index, line in enumerate(text.splitlines()):
        code = line.split(';')[0].strip()
        match = re.match(r'\[Begin Action\s+(\d+)\]', code, re.I)
        if match:
            check_count()
            action = int(match[1]); defaults = {1: [], 2: []}; pending = {}; target = None
        match = re.match(r'Clsn([12])(Default)?:\s*(\d+)', code, re.I)
        if match:
            check_count()
            expected = int(match[3])
            kind = int(match[1])
            target = []
            (defaults if match[2] else pending)[kind] = target
        match = re.match(r'Clsn[12]\[\d+\]\s*=\s*(-?\d+)\s*,\s*(-?\d+)\s*,\s*(-?\d+)\s*,\s*(-?\d+)', code, re.I)
        if match:
            x,y,r,b = map(int, match.groups())
            if target is None: raise ValueError('Collision without declaration')
            target.append((min(x,r), min(y,b), max(x,r), max(y,b)))
        match = re.match(r'(-?\d+)\s*,\s*(-?\d+)\s*,\s*(-?\d+)\s*,\s*(-?\d+)\s*,\s*(-?\d+)(.*)', code)
        if match:
            check_count()
            yield index, action, tuple(map(int, match.groups()[:5])), match[6], {k: list(pending.get(k, defaults[k])) for k in (1,2)}
            pending = {}; target = None
    check_count()


def apply_hurtboxes(text, overrides):
    """Replace Clsn2 for explicit sprite contexts without changing AIR timing/hits."""
    lines = text.splitlines()
    for line, action, values, flags, boxes in frames(text):
        key = values[:2]
        if key in overrides:
            body = overrides[key]
            declaration = [f'Clsn2: {len(body)}'] + [f'Clsn2[{i}] = '+', '.join(map(str, box)) for i, box in enumerate(body)]
            lines[line] = '\n'.join(declaration + [lines[line]])
    return '\n'.join(lines)+'\n'
