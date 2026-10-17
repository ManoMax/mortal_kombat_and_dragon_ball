#!/usr/bin/env python3
"""Sequential real-engine regressions; preserve historical evidence and controls.

Focuses IKEMEN and injects keys on unlocked X11. No manual-play claim.
"""
import argparse
import json
from pathlib import Path
import subprocess
import sys
import time
ROOT=Path(__file__).resolve().parents[1]
LEGACY = ('gameplay.png','keyboard-match.log','rounds-audio.log','rounds-nosound.log',
          'sprint4-facings.png','sprint4-sprites.csv','sprint5-facings.png',
          'sprint5-sprites.csv','sprint5-reversed-facings.png','sprint5-reversed-sprites.csv',
          'sprint5-gameplay.mp4','sprint5-performance.txt','sprint2-effects.png','sprint2-trace.csv')


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path,default=ROOT/'evidence/sprint6/runtime')
    args=parser.parse_args(); args.output.mkdir(parents=True,exist_ok=True)
    originals={name:(ROOT/'tests'/name).read_bytes() if (ROOT/'tests'/name).exists() else None for name in LEGACY}
    started=time.time(); result={'automated':True,'human_acceptance':'pending','status':'failed'}
    try:
        subprocess.run([sys.executable,str(ROOT/'tests/sprint5_graphics.py')],cwd=ROOT,check=True,timeout=300)
        for name in LEGACY:
            source=ROOT/'tests'/name
            if source.stat().st_mtime < started:
                raise RuntimeError('Stale evidence: '+name)
            (args.output/name).write_bytes(source.read_bytes())
        subprocess.run(['/usr/bin/time','-v','-o',str(args.output/'reversed-performance.txt'),
            sys.executable,str(ROOT/'tests/sprint2_smoke.py'),'--reverse-fighters',
            '--output',str(args.output/'reversed'),'--record',str(args.output/'reversed-gameplay.mp4')],cwd=ROOT,check=True,timeout=100)
        subprocess.run([sys.executable,str(ROOT/'tests/performance_smoke.py'),'--report',str(args.output/'reversed-performance.txt')],check=True)
        result['status']='pass'
    finally:
        result['elapsed_seconds']=round(time.time()-started,2)
        (args.output/'result.json').write_text(json.dumps(result,indent=2)+'\n')
        for name,data in originals.items():
            if data is not None: (ROOT/'tests'/name).write_bytes(data)
            else: (ROOT/'tests'/name).unlink(missing_ok=True)
    print('PASS Sprint 6 real-engine regressions and both fighter orders; human review pending')

if __name__=='__main__': main()
