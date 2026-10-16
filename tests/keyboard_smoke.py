#!/usr/bin/env python3
"""X11 integration test. Requires an unlocked desktop; focuses only Ikemen."""
import ctypes as C
from pathlib import Path
import subprocess, time, re, tempfile, os
root=Path(__file__).resolve().parents[1]
x=C.CDLL('libX11.so.6'); xt=C.CDLL('libXtst.so.6')
x.XOpenDisplay.restype=C.c_void_p
x.XOpenDisplay.argtypes=[C.c_char_p]
x.XStringToKeysym.argtypes=[C.c_char_p]; x.XStringToKeysym.restype=C.c_ulong
x.XKeysymToKeycode.argtypes=[C.c_void_p,C.c_ulong]
x.XSetInputFocus.argtypes=[C.c_void_p,C.c_ulong,C.c_int,C.c_ulong]
x.XFlush.argtypes=[C.c_void_p]
xt.XTestFakeKeyEvent.argtypes=[C.c_void_p,C.c_uint,C.c_int,C.c_ulong]
d=x.XOpenDisplay(None)
if not d: raise SystemExit('No X11 display available')
def key(name,down):
    code=x.XKeysymToKeycode(d,x.XStringToKeysym(name.encode()))
    xt.XTestFakeKeyEvent(d,code,int(down),0); x.XFlush(d)
def hold(names, seconds):
    for name in names: key(name,True)
    time.sleep(seconds)
    for name in names: key(name,False)
temporary=tempfile.TemporaryDirectory(prefix='dbz-keyboard-')
fresh_log=Path(temporary.name)/'match.log'
proc=subprocess.Popen([str(root/'scripts/play.sh'),'-nosound','-p1.life','900','-time','20','-rounds','1','-log',str(fresh_log)],cwd=root)
try:
    time.sleep(4)
    tree=subprocess.check_output(['xwininfo','-root','-tree'],text=True)
    window=re.search(r'(0x[0-9a-f]+) "Ikemen GO"',tree)
    if not window: raise RuntimeError('Game window not found')
    wid=int(window[1],16)
    x.XSetInputFocus(d,wid,1,0); x.XFlush(d)
    time.sleep(2)
    hold(['Right','j'],0.65)
    for i in range(12):
        hold(['a','r'] if i%2==0 else ['s','t'],0.08); time.sleep(.18)
    hold(['Up','i'],.15); time.sleep(.7)
    hold(['Down','k'],.4)
    for i in range(10):
        hold(['z','f'] if i%2==0 else ['x','g'],.08); time.sleep(.18)
    subprocess.run(['ffmpeg','-y','-loglevel','error','-f','x11grab','-window_id',str(wid),'-i',os.environ['DISPLAY'],'-frames:v','1',str(root/'tests/gameplay.png')],check=True)
    proc.wait(timeout=40)
    if proc.returncode: raise RuntimeError(f'Game exited {proc.returncode}')
    log=fresh_log.read_text()
    lives=[int(v) for v in re.findall(r'\["Life"\] => (\d+)',log)]
    if not (len(lives)==2 and 0<=lives[0]<900 and 0<=lives[1]<1000): raise RuntimeError(f'Invalid damage results: {lives}')
    if log.count('["AILevel"] => 0')!=2: raise RuntimeError('Fighters are not both human controlled')
    (root/'tests/keyboard-match.log').write_text(log)
    print('PASS: both keyboard-controlled fighters dealt damage:', lives)
finally:
    for name in ['Right','j','a','r','s','t','Up','i','Down','k','z','f','x','g']: key(name,False)
    if proc.poll() is None:
        proc.terminate()
        try: proc.wait(timeout=5)
        except subprocess.TimeoutExpired: proc.kill(); proc.wait()
    temporary.cleanup()
