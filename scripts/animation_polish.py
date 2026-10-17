"""Explicit idle-only cadence override; combat contracts are immutable here."""
import json
from pathlib import Path
from air_geometry import frames
ROOT = Path(__file__).resolve().parents[1]


def idle_ticks():
    ticks = json.loads((ROOT/'assets-source/animation-polish.json').read_text())['idle_ticks']
    if len(ticks) != 11 or any(type(t) is not int or not 1 <= t <= 15 for t in ticks):
        raise ValueError('Idle cadence requires eleven positive holds of at most 15 ticks')
    return ticks


def apply(text):
    lines = text.splitlines()
    idle = [f for f in frames(text) if f[1] == 0]
    ticks = idle_ticks()
    if len(idle) != len(ticks):
        raise ValueError('Unexpected idle contract')
    for (line, action, values, flags, boxes), duration in zip(idle, ticks):
        g,n,x,y,_ = values
        lines[line] = f'{g},{n}, {x},{y}, {duration}{flags}'
    return '\n'.join(lines)+'\n'
