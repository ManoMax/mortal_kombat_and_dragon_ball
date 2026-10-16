#!/usr/bin/env python3
"""Real CMD/input and state/result checks. Requires unlocked X11. Focuses Ikemen."""
import ctypes as C
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile
import time

ROOT = Path(__file__).resolve().parents[1]

def require(ok, message):
    if not ok: raise RuntimeError(message)

def verify(rows):
    require(rows, 'No fresh telemetry')
    for p in (1,2):
        samples=[r for r in rows if r[1]==p]
        require(samples, f'Missing P{p}')
        require(all(0<=r[6]<=3000 for r in samples), 'Ki outside bounds')
        require(any(r[6]==3000 for r in samples), f'P{p} never reached cap')
        require(any(r[4]==7000 for r in samples), f'P{p} never charged')
        beams=[r for r in samples if r[4]==7100]
        require(beams, f'P{p} never cast')
        require(any(r[7]>0 for r in samples), f'P{p} missing projectile')
        require(any(r[8]>=0 for r in samples), f'P{p} projectile never hit')
        require(any(r[9]>=0 for r in samples), f'P{p} projectile never guarded')
        entries=[(a,b) for a,b in zip(samples,samples[1:]) if a[4]!=7100 and b[4]==7100]
        require(entries and all(a[6]-b[6]==1000 for a,b in entries), f'P{p} incorrect cost')
        require(all(r[10]==1 for r in samples if r[3]==2), f'P{p} missing meter')
        require(any(r[2]>=2 and r[3]==2 and r[6]==0 for r in samples), f'P{p} round reset missing')

def main():
    x=C.CDLL('libX11.so.6'); xt=C.CDLL('libXtst.so.6')
    x.XOpenDisplay.restype=C.c_void_p; x.XOpenDisplay.argtypes=[C.c_char_p]
    x.XStringToKeysym.argtypes=[C.c_char_p]; x.XStringToKeysym.restype=C.c_ulong
    x.XKeysymToKeycode.argtypes=[C.c_void_p,C.c_ulong]
    x.XSetInputFocus.argtypes=[C.c_void_p,C.c_ulong,C.c_int,C.c_ulong]
    x.XFlush.argtypes=[C.c_void_p]
    xt.XTestFakeKeyEvent.argtypes=[C.c_void_p,C.c_uint,C.c_int,C.c_ulong]
    display=x.XOpenDisplay(None); require(display, 'No X11 display')
    pressed=set()
    def key(k,down):
        code=x.XKeysymToKeycode(display,x.XStringToKeysym(k.encode()))
        xt.XTestFakeKeyEvent(display,code,int(down),0); x.XFlush(display)
        (pressed.add if down else pressed.discard)(k)
    def hold(keys,seconds):
        for k in keys: key(k,True)
        time.sleep(seconds)
        for k in keys: key(k,False)
    def beam(p):
        down,forward,punch=('Down','Right','s') if p==1 else ('k','j','t')
        hold([down],.08)
        hold([down,forward],.08)
        hold([forward,punch],.08)
    with tempfile.TemporaryDirectory(prefix='dbz-sprint2-') as td:
        trace=Path(td)/'trace.csv'; config=Path(td)/'config.ini'
        config.write_text(re.sub(r'^Lua\s*=.*$', "Lua = dofile('external/mods/-dbz-probe.lua')", (ROOT/'engine/save/config.ini').read_text(), flags=re.M))
        env=dict(os.environ, DBZ_TRACE=str(trace))
        output=open(Path(td)/'output.log','w+')
        proc=subprocess.Popen([str(ROOT/'scripts/play.sh'),'-config',str(config),'-nosound','-time','25','-rounds','2'],cwd=ROOT,env=env,stdout=output,stderr=subprocess.STDOUT)
        def rows():
            return [list(map(int,line.split(','))) for line in trace.read_text().splitlines() if line.count(',')==10]
        def snap(p): return [r for r in rows() if r[1]==p][-1]
        try:
            deadline=time.monotonic()+20
            while time.monotonic()<deadline:
                if proc.poll() is not None:
                    output.seek(0); raise RuntimeError(output.read())
                tree=subprocess.check_output(['xwininfo','-root','-tree'],text=True)
                window=re.search(r'(0x[0-9a-f]+) "Ikemen GO"',tree)
                if window:
                    x.XSetInputFocus(display,int(window[1],16),1,0); x.XFlush(display)
                if trace.exists() and rows() and snap(1)[3]==2: break
                time.sleep(.2)
            require(trace.exists() and snap(1)[3]==2, 'Fight did not start')
            # No Ki: actual quarter-circle must not dispatch to beam or Palm 1010.
            for p in (1,2):
                start=len(rows()); beam(p); time.sleep(.8)
                require(not any(r[1]==p and r[4] in (7100,1010) for r in rows()[start:]), 'Cast without Ki / KFM conflict')
            for k in ('z','x','f','g'): key(k,True)
            time.sleep(2.7)
            subprocess.run(['ffmpeg','-y','-loglevel','error','-f','x11grab','-window_id',window[1],'-i',os.environ['DISPLAY'],'-frames:v','1',str(ROOT/'tests/sprint2-effects.png')],check=True)
            for k in ('z','x','f','g'): key(k,False)
            time.sleep(.3)
            require(snap(1)[6]==snap(2)[6]==3000, 'Charge failed to saturate')
            # Hit idle opponent, then repeat into directional guard.
            for p,guard in ((1,'l'),(2,'Left')):
                before=snap(3-p)[5]
                beam(p); time.sleep(1.5)
                nominal=json.loads((ROOT/'assets-source/combat.json').read_text())['goku' if p==1 else 'vegeta']['damage']
                require(before-snap(3-p)[5]==nominal, f'P{p} unexpected beam damage')
                before=snap(3-p)[5]; key(guard,True)
                beam(p); time.sleep(1.5); key(guard,False)
                require(snap(3-p)[5]==before, f'P{p} guard failed')
            # Charging opponent must be hittable and stop gaining Ki on impact.
            key('f',True); key('g',True)
            beam(1); time.sleep(1.5); key('f',False); key('g',False)
            samples=[r for r in rows() if r[1]==2]
            require(any(a[4]==7000 and b[4]>=5000 and b[4]<6000 for a,b in zip(samples,samples[1:])), 'Charge not interrupted by hit')
            # Natural timeout with unequal life ends a real round (no debug reset).
            deadline=time.monotonic()+25
            while time.monotonic()<deadline and not (snap(1)[2]>=2 and snap(1)[3]==2): time.sleep(.2)
            verify(rows())
            print('PASS real motor: charge/cap/cost/projectiles/hit/guard/meters/round reset, both fighters')
            hold(['Escape'],.1); proc.wait(timeout=10)
            require(proc.returncode==0, 'Engine exited with error')
            (ROOT/'tests/sprint2-trace.csv').write_text(trace.read_text())
        except Exception:
            if trace.exists(): (ROOT/'tests/sprint2-failed.csv').write_text(trace.read_text())
            output.flush(); output.seek(0)
            print(output.read())
            raise
        finally:
            for k in list(pressed): key(k,False)
            if proc.poll() is None:
                proc.terminate()
                try: proc.wait(timeout=5)
                except subprocess.TimeoutExpired: proc.kill(); proc.wait()
            output.close()

if __name__=='__main__': main()
