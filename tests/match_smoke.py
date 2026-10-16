#!/usr/bin/env python3
"""Fresh-process best-of-three test; requires X11 (does not simulate keys)."""
import argparse
from pathlib import Path
import re
import subprocess
import tempfile
import time

ROOT = Path(__file__).resolve().parents[1]

def verify(log, require_ko=False):
    def number(key):
        match = re.search(r'\["'+key+r'"\] => (\d+)', log)
        if not match: raise ValueError(f'Missing {key}')
        return int(match[1])
    rounds = number('LastRound')
    if rounds not in (2, 3): raise ValueError(f'Invalid best-of-three length: {rounds}')
    if re.findall(r'\["Index"\] => (\d+)', log) != [str(i) for i in range(1, rounds+1)]:
        raise ValueError('Missing or unordered round results')
    wins = re.search(r'\["Wins"\] => table:[^{]+\{\s*\[1\] => (\d+)\s*\[2\] => (\d+)', log)
    if not wins: raise ValueError('Missing match scores')
    scores = list(map(int, wins.groups()))
    winner = number('WinSide') # engine uses zero-based side in this field
    if winner not in (0,1) or scores[winner] != 2 or scores[1-winner] >= 2:
        raise ValueError(f'Invalid winner/scores: {winner}, {scores}')
    if sum(scores) != rounds or number('Draws') != 0: raise ValueError('Unexpected draw')
    per_round = re.findall(r'\["Win"\] => (true|false)', log)
    if len(per_round) != rounds*2: raise ValueError('Missing fighter results')
    accumulated = [0,0]
    for i in range(rounds):
        result = per_round[i*2:i*2+2]
        if result.count('true') != 1: raise ValueError('No unique round winner')
        accumulated[result.index('true')] += 1
        if i < rounds-1 and max(accumulated) == 2: raise ValueError('Match continued after second win')
    if accumulated != scores: raise ValueError('Round wins disagree with match scores')
    if require_ko:
        kos=re.findall(r'\["WinKO"\] => (true|false)',log)
        lives=[int(value) for value in re.findall(r'\["Life"\] => (\d+)',log)]
        if kos!=per_round or len(lives)!=rounds*2:
            raise ValueError('Missing KO/life evidence')
        for i,won in enumerate(per_round):
            if (won=='false' and lives[i]!=0) or (won=='true' and lives[i]<=0):
                raise ValueError('KO inconsistent with life')
    return rounds, scores

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--audio', action='store_true')
    parser.add_argument('--timeout', type=int, default=90)
    args=parser.parse_args()
    with tempfile.TemporaryDirectory(prefix='dbz-match-') as directory:
        log=Path(directory)/'match.log'
        command=[str(ROOT/'scripts/play.sh'), '-p1.life','1','-p1.lifeMax','1','-p2.life','1000','-p2.ai','8', '-time','30','-rounds','2','-log',str(log)]
        if not args.audio: command.append('-nosound')
        started=time.monotonic()
        try:
            result=subprocess.run(command, capture_output=True, text=True, timeout=args.timeout)
        except subprocess.TimeoutExpired as exc:
            raise SystemExit(f'FAIL timeout after {args.timeout}s; no completion evidence. stdout={exc.stdout!r} stderr={exc.stderr!r}')
        if result.returncode: raise SystemExit(f'FAIL exit {result.returncode}: {result.stdout}\n{result.stderr}')
        if not log.is_file(): raise SystemExit('FAIL no fresh final log')
        destination=ROOT/'tests'/('rounds-audio.log' if args.audio else 'rounds-nosound.log')
        destination.write_text(log.read_text())
        rounds,scores=verify(log.read_text(), require_ko=True)
        print(f'PASS audio={args.audio}, rounds={rounds}, scores={scores}, elapsed={time.monotonic()-started:.2f}s; {destination.name}')
if __name__ == '__main__': main()
