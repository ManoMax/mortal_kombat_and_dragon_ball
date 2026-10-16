#!/usr/bin/env python3
"""Capture real Goku vs Vegeta input/animations and specials, sequentially on X11.

Focuses IKEMEN and injects keys. Requires libX11/libXtst, xwininfo, ffmpeg.
The video records the live game window; it is never used as game content.
"""
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
if __name__ == '__main__':
    subprocess.run([sys.executable, str(ROOT/'tests/sprint4_smoke.py'), '--opponent', 'vegeta', '--prefix', 'sprint5', '--organic'], cwd=ROOT, check=True)
    subprocess.run([sys.executable, str(ROOT/'tests/sprint4_smoke.py'), '--fighter', 'vegeta', '--opponent', 'goku', '--prefix', 'sprint5-reversed', '--organic'], cwd=ROOT, check=True)
    subprocess.run([sys.executable, str(ROOT/'tests/sprint2_smoke.py'), '--record', str(ROOT/'tests/sprint5-gameplay.mp4')], cwd=ROOT, check=True)
