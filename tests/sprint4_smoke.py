#!/usr/bin/env python3
"""Real Goku mirror match: AIR sprite progression and screenshots in both facings.

Requires unlocked X11; focuses Ikemen and injects keys. No manual-play claim.
"""
import ctypes as C
import argparse
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile
import time

ROOT = Path(__file__).resolve().parents[1]


def verify(rows):
    if not rows:
        raise ValueError('No fresh sprite telemetry')
    for player in (1, 2):
        samples = [r for r in rows if r[1] == player]
        idle = {r[4] for r in samples if r[2] == 0 and r[3] == 30000}
        if not set(range(4)) <= idle:
            raise ValueError(f'P{player}: idle frames missing')
        for action in (20, 21, 200):
            if not any(r[2] == action and r[3] == 30000 for r in samples):
                raise ValueError(f'P{player}: action {action} missing')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--fighter', choices=('goku', 'vegeta'), default='goku')
    parser.add_argument('--opponent', choices=('goku', 'vegeta'), default='goku')
    parser.add_argument('--prefix', default='sprint4')
    parser.add_argument('--organic', action='store_true', help='Require observed body sprites to be organic on both sides')
    args = parser.parse_args()
    if not re.fullmatch(r'[a-zA-Z0-9_-]+', args.prefix):
        raise ValueError('Invalid evidence prefix')
    x = C.CDLL('libX11.so.6'); xt = C.CDLL('libXtst.so.6')
    x.XOpenDisplay.restype = C.c_void_p; x.XOpenDisplay.argtypes = [C.c_char_p]
    x.XStringToKeysym.argtypes = [C.c_char_p]; x.XStringToKeysym.restype = C.c_ulong
    x.XKeysymToKeycode.argtypes = [C.c_void_p, C.c_ulong]
    x.XSetInputFocus.argtypes = [C.c_void_p, C.c_ulong, C.c_int, C.c_ulong]
    x.XFlush.argtypes = [C.c_void_p]
    xt.XTestFakeKeyEvent.argtypes = [C.c_void_p, C.c_uint, C.c_int, C.c_ulong]
    display = x.XOpenDisplay(None)
    if not display: raise RuntimeError('No X11 display')
    pressed = set()
    def key(name, down):
        code = x.XKeysymToKeycode(display, x.XStringToKeysym(name.encode()))
        xt.XTestFakeKeyEvent(display, code, int(down), 0); x.XFlush(display)
        (pressed.add if down else pressed.discard)(name)
    def hold(keys, seconds):
        for name in keys: key(name, True)
        time.sleep(seconds)
        for name in keys: key(name, False)
    with tempfile.TemporaryDirectory(prefix='dbz-art-') as td:
        td = Path(td); trace = td/'trace.csv'; probe = td/'probe.lua'; config = td/'config.ini'
        probe.write_text('''
if not artTrace then artTrace = assert(io.open(assert(os.getenv('DBZ_ART_TRACE')), 'w')); artTick = 0 end
local old = id()
artTick = artTick + 1
for p = 1, 2 do
    if player(p) then
        artTrace:write(string.format('%d,%d,%d,%d,%d\\n', artTick, p, anim(), spriteVar('group'), spriteVar('image')))
    end
end
artTrace:flush()
playerId(old)
loop()
''')
        config.write_text(re.sub(r'^Lua\s*=.*$', f"Lua = dofile('{probe}')", (ROOT/'engine/save/config.ini').read_text(), flags=re.M))
        env = dict(os.environ, DBZ_ART_TRACE=str(trace))
        with (td/'engine.log').open('w+') as output:
            proc = subprocess.Popen([str(ROOT/'scripts/play.sh'), '-p1', args.fighter, '-p2', args.opponent, '-config', str(config), '-nosound', '-time', '99'], cwd=ROOT, env=env, stdout=output, stderr=subprocess.STDOUT)
            def rows():
                return [list(map(int, line.split(','))) for line in trace.read_text().splitlines() if line.count(',') == 4]
            try:
                deadline = time.monotonic()+20
                window = None
                while time.monotonic() < deadline:
                    if proc.poll() is not None:
                        output.seek(0); raise RuntimeError(output.read())
                    tree = subprocess.check_output(['xwininfo', '-root', '-tree'], text=True)
                    window = re.search(r'(0x[0-9a-f]+) "Ikemen GO"', tree)
                    if window:
                        info=subprocess.run(['xwininfo','-id',window[1]],capture_output=True,text=True)
                        if info.returncode==0 and 'Map State: IsViewable' in info.stdout:
                            x.XSetInputFocus(display, int(window[1], 16), 1, 0); x.XFlush(display)
                        else: window=None
                    if window and trace.exists() and len(rows()) > 600: break
                    time.sleep(.2)
                if not window or not trace.exists(): raise RuntimeError('No fresh game window/trace')
                subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'x11grab', '-window_id', window[1], '-i', os.environ['DISPLAY'], '-frames:v', '1', str(ROOT/f'tests/{args.prefix}-facings.png')], check=True)
                hold(['Right', 'j'], .2)
                hold(['Left', 'l'], .35)
                hold(['a', 'r'], .1); time.sleep(.6)
                evidence = rows(); verify(evidence)
                if args.organic:
                    for player, name in ((1,args.fighter),(2,args.opponent)):
                        manifest=json.loads((ROOT/f'assets-source/sprites/{name}/manifest.json').read_text())
                        organic={tuple(f['sprite']) for f in manifest['frames'] if f.get('organic')}
                        if any((r[3],r[4]) not in organic for r in evidence if r[1]==player and r[2] in (0,20,21,200)):
                            raise ValueError(f'P{player}: observed placeholder in essential action')
                x.XSetInputFocus(display,int(window[1],16),1,0); x.XFlush(display)
                time.sleep(.1)
                hold(['Escape'], .2); proc.wait(timeout=10)
                if proc.returncode: raise RuntimeError(f'Engine exited {proc.returncode}')
                (ROOT/f'tests/{args.prefix}-sprites.csv').write_text('\n'.join(','.join(map(str, r)) for r in evidence)+'\n')
                print(f'PASS real {args.fighter} vs {args.opponent}: idle progression, forward/back walk, punch; both players; fresh capture')
            finally:
                for name in list(pressed): key(name, False)
                if proc.poll() is None:
                    proc.terminate()
                    try: proc.wait(timeout=5)
                    except subprocess.TimeoutExpired: proc.kill(); proc.wait()


if __name__ == '__main__': main()
