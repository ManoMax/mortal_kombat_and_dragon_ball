#!/usr/bin/env python3
"""Run the previous X11 regressions and record real Sprint 5 gameplay sequentially.

Focuses IKEMEN and injects keys; run on an unlocked desktop without other work.
"""
from pathlib import Path
import argparse
import subprocess
import sys
ROOT=Path(__file__).resolve().parents[1]
if __name__ == '__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--capture-only',action='store_true',help='Repeat the capture/Ki stage after a harness failure')
    args=parser.parse_args()
    checks=[] if args.capture_only else [('sprint4_smoke.py',[]),('keyboard_smoke.py',[]),
                                        ('match_smoke.py',[]),('match_smoke.py',['--audio'])]
    for script, extra in checks:
        print('RUN',script,*extra,flush=True)
        subprocess.run([sys.executable,str(ROOT/'tests'/script),*extra],cwd=ROOT,check=True,timeout=120)
    print('RUN real demo, Ki regression and resource measurement',flush=True)
    report=ROOT/'tests/sprint5-performance.txt'
    subprocess.run(['/usr/bin/time','-v','-o',str(report),sys.executable,str(ROOT/'scripts/capture_demo.py')],cwd=ROOT,check=True,timeout=120)
    subprocess.run([sys.executable,str(ROOT/'tests/performance_smoke.py'),'--report',str(report)],cwd=ROOT,check=True)
