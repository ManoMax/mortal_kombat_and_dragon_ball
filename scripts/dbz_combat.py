"""Deterministic original DBZ combat layer; KFM source remains untouched."""
import json
from pathlib import Path

CONFIG = json.loads((Path(__file__).resolve().parents[1]/'assets-source/combat.json').read_text())
if not (isinstance(CONFIG['initial_ki'], int) and 0 <= CONFIG['initial_ki'] <= 3000):
    raise ValueError('initial_ki must be an integer in 0..3000')
if not (isinstance(CONFIG['charge_per_tick'], int) and 1 <= CONFIG['charge_per_tick'] <= 3000):
    raise ValueError('charge_per_tick must be an integer in 1..3000')
for fighter in ('goku', 'vegeta'):
    for key in ('damage', 'speed', 'startup', 'recovery'):
        if not isinstance(CONFIG[fighter][key], int) or CONFIG[fighter][key] <= 0:
            raise ValueError(f'{fighter}.{key} must be a positive integer')


def command_layer(cmd):
    # Remove only the competing dispatch, retaining state 1010 and dependencies.
    import re
    cmd = re.sub(r'\[State -1, Strong Kung Fu Palm\].*?(?=\[State -1,)', '', cmd, flags=re.S)
    definitions = '''[Command]
name = "ki_charge_a"
command = /a
time = 1

[Command]
name = "ki_charge_b"
command = /b
time = 1

'''
    dispatch = '''
[State -1, DBZ beam]
type = ChangeState
triggerall = roundstate = 2
triggerall = command = "QCF_y"
triggerall = var(20) >= 1000
triggerall = statetype != A
triggerall = numprojID(7100) = 0
trigger1 = ctrl
trigger2 = stateno = [200, 429]
trigger2 = movecontact
value = 7100

[State -1, Ki charge]
type = ChangeState
triggerall = roundstate = 2
triggerall = command = "ki_charge_a"
triggerall = command = "ki_charge_b"
triggerall = statetype != A
trigger1 = ctrl
value = 7000
'''
    return cmd.replace('[Statedef -1]', definitions+'[Statedef -1]\n'+dispatch)


def states(name):
    c = CONFIG[name]
    return f'''
; DBZ: var(20) is Ki, independent of KFM power and vars 1/2.
[Statedef -2]
[State -2, Reset Ki each round]
type = VarSet
trigger1 = roundstate < 2
var(20) = {CONFIG['initial_ki']}
ignorehitpause = 1

[State -2, Ki background]
type = Explod
trigger1 = numexplod(7201) = 0
anim = 7201
ID = 7201
postype = left
pos = ifelse(teamside = 1, 12, 208), 40
bindtime = -1
removetime = -1
sprpriority = 10
ownpal = 1
ignorehitpause = 1

[State -2, Stop aura on interruption]
type = RemoveExplod
trigger1 = stateno != 7000
ID = 7020
ignorehitpause = 1

[State -2, Ki meter]
type = Explod
trigger1 = numexplod(7200) = 0
anim = 7200
ID = 7200
postype = left
pos = ifelse(teamside = 1, 12, 208), 40
bindtime = -1
removetime = -1
sprpriority = 11
ownpal = 1
ignorehitpause = 1

[State -2, Ki meter fill]
type = ModifyExplod
trigger1 = 1
ID = 7200
scale = var(20) / 3000.0, 1
ignorehitpause = 1

[Statedef 7000]
type = S
movetype = I
physics = S
anim = 7000
ctrl = 0
velset = 0, 0

[State 7000, Charge]
type = VarSet
trigger1 = roundstate = 2
var(20) = min(3000, var(20) + {CONFIG['charge_per_tick']})

[State 7000, Aura]
type = Explod
trigger1 = time % 12 = 0
anim = 7020
ID = 7020
pos = 0, 0
postype = p1
bindtime = -1
removetime = 12
sprpriority = -1
ownpal = 1

[State 7000, Release]
type = ChangeState
trigger1 = command != "ki_charge_a"
trigger2 = command != "ki_charge_b"
trigger3 = roundstate != 2
value = 0
ctrl = 1

[Statedef 7100]
type = S
movetype = A
physics = S
anim = 7100
ctrl = 0
velset = 0, 0

[State 7100, Pay once on entry]
type = VarAdd
trigger1 = time = 0
v = 20
value = -1000

[State 7100, Original beam]
type = Projectile
trigger1 = time = {c['startup']}
ProjID = 7100
projanim = 7110
projhitanim = 7120
projremanim = 7120
projcancelanim = 7120
projremove = 1
projremovetime = 90
projhits = 1
projpriority = 1
offset = 35, -55
velocity = {c['speed']}, 0
attr = S, SP
hitflag = MAF
guardflag = MA
animtype = Heavy
priority = 4, Hit
damage = {c['damage']}, 0
pausetime = 0, 10
guard.pausetime = 0, 8
sparkno = -1
guard.sparkno = -1
getpower = 0, 0
givepower = 0, 0
ground.type = High
ground.slidetime = 18
ground.hittime = 24
guard.hittime = 14
ground.velocity = -6, 0
guard.velocity = -3
air.velocity = -4, -3
air.hittime = 24
fall = 0

[State 7100, Recovery]
type = ChangeState
trigger1 = time >= {c['startup'] + c['recovery']}
value = 0
ctrl = 1
'''


def animations(vegeta):
    # New body poses preserve the established standing hurtbox dimensions.
    out = ''
    for action, frames in ((7000, [(7000,0,8),(7000,1,8)]),
                           (7100, [(7100,0,10),(7100,1,10),(7100,2,-1)])):
        out += f'\n[Begin Action {action}]\nClsn2Default: 1\n Clsn2[0] = -12,-80,12,0\n'
        for g,i,t in frames: out += f'{g},{i},0,0,{t}\n'
    out += '''
[Begin Action 7110]
Clsn1Default: 1
 Clsn1[0] = -24,-9,24,9
Clsn2Default: 1
 Clsn2[0] = -24,-9,24,9
7110,0,0,0,3
7110,1,0,0,3
[Begin Action 7120]
7120,0,0,0,4
7120,1,0,0,4
7120,2,0,0,4
[Begin Action 7020]
7020,0,0,0,4
7020,1,0,0,4
7020,2,0,0,4
[Begin Action 7200]
7200,0,0,0,-1
[Begin Action 7201]
7201,0,0,0,-1
'''
    return out


def palette(vegeta):
    # One shared SFF v1 palette: effects must never reinterpret skin as beam color.
    return ((0,0,0),(245,183,125),(43,76,172) if vegeta else (239,112,26),
            (231,231,220) if vegeta else (27,52,122),(21,22,31),(220,199,133),
            (180,75,255) if vegeta else (40,170,255),(240,245,255),(60,65,80))


def effect(g, i, vegeta, pcx):
    w=h=160; p=bytearray(w*h)
    for y in range(h):
        for x in range(w):
            xx=x-80; yy=y-110; v=0
            if g in (7000,7100):
                # Original charge/preparation/release silhouettes and hand positions.
                if -10<=xx<=10 and -78<=yy<=-60: v=4
                if -12<=xx<=12 and -59<=yy<=-27: v=5
                if (-12<=xx<=-4 or 4<=xx<=12) and -26<=yy<=0: v=5
                if -11<=xx<=11 and -84<=yy<=-79: v=6
                hx = (16 if vegeta else -18) if i==0 else (20 if i==1 else 29)
                hy = -66 if vegeta and i<2 else -48
                if min(8,hx)<=xx<=max(8,hx)+6 and hy<=yy<=hy+7: v=4
            elif g==7110:
                if (xx/25)**2+(yy/(10-i))**2<=1: v=2 if abs(yy)<4 else 1
            elif g==7120:
                r=10+i*7
                if r-5<=abs(xx)+abs(yy)<=r: v=2 if i==0 else 1
            elif g==7020:
                if .65<=(xx/(23+i*3))**2+((yy+40)/(48+i*2))**2<=1: v=1
            elif g in (7200,7201):
                if 0<=xx<72 and 0<=yy<5: v=1 if g==7200 else 3
            p[y*w+x]=(0,6,7,8,1,2,4)[v]
    return pcx(p,palette(vegeta),w,h)

ENTRIES = [(7000,i) for i in range(2)]+[(7100,i) for i in range(3)]+[(7110,i) for i in range(2)]+[(7120,i) for i in range(3)]+[(7020,i) for i in range(3)]+[(7200,0),(7201,0)]
