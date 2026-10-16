#!/usr/bin/env python3
"""Ubuntu resource budget for the real Ki/projectile smoke; no FPS claim."""
import argparse
from pathlib import Path
import re
import subprocess
import sys
ROOT=Path(__file__).resolve().parents[1]


def verify(report):
    def field(label):
        match=re.search(re.escape(label)+r':\s*([^\n]+)',report)
        if not match: raise ValueError('Missing performance field: '+label)
        return match[1].strip()
    if field('Exit status') != '0': raise ValueError('Combat smoke failed')
    rss=int(field('Maximum resident set size (kbytes)'))
    parts=field('Elapsed (wall clock) time (h:mm:ss or m:ss)').split(':')
    elapsed=0
    for part in parts: elapsed=elapsed*60+float(part)
    if rss<=0 or rss>1048576 or elapsed<=0 or elapsed>90:
        raise ValueError(f'Resource budget exceeded: {rss} KiB, {elapsed}s')
    print(f'PASS resource budget: {rss} KiB peak RSS, {elapsed:.2f}s; limits 1 GiB / 90s')


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--report', type=Path, help='Validate an existing GNU time report without running the game')
    args=parser.parse_args()
    report=args.report or ROOT/'tests/sprint3-performance.txt'
    if args.report is None:
        subprocess.run(['/usr/bin/time','-v','-o',str(report),sys.executable,str(ROOT/'tests/sprint2_smoke.py')],check=True,timeout=100)
    verify(report.read_text())

if __name__=='__main__': main()
