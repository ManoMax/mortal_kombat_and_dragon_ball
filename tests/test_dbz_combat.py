"""Regression checks for command ownership, resources and telemetry rejection."""
from pathlib import Path
import sys
import unittest

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
import dbz_combat
from air_geometry import frames
from validate import decode
from build_characters import pcx
from sprint2_smoke import verify


class DBZTests(unittest.TestCase):
    def test_quarter_circle_has_single_owner_and_no_power_dependency(self):
        for name in ('goku','vegeta'):
            cmd=(ROOT/f'engine/chars/{name}/kfm.cmd').read_text()
            self.assertEqual(cmd.count('triggerall = command = "QCF_y"'),1)
            self.assertNotIn('[State -1, Strong Kung Fu Palm]',cmd)
            layer=cmd.split('[State -1, DBZ beam]')[1].split(';===========================================================================')[0]
            self.assertIn('var(20) >= 1000',layer)
            self.assertNotIn('power >=',layer)
            cns=(ROOT/f'engine/chars/{name}/kfm.cns').read_text()
            self.assertIn('[Statedef 1010]',cns) # retained legacy dependencies
            self.assertIn('[Statedef 3000]',cns)
            self.assertNotIn('poweradd',dbz_combat.states(name).lower())

    def test_original_effects_have_distinct_palettes_and_hitbox_coverage(self):
        colors=[]
        for vegeta in (False,True):
            data=dbz_combat.effect(7110,0,vegeta,pcx)
            colors.append(data[-750:-747])
            w,h,stride,pixels=decode(data)
            # Elliptical artwork reaches the center and cardinal collision edges.
            self.assertNotEqual(pixels[110*stride+80],0)
            self.assertNotEqual(pixels[110*stride+104],0)
            self.assertNotEqual(pixels[101*stride+80],0)
        self.assertNotEqual(*colors)
        beam=[f for f in frames(dbz_combat.animations(False)) if f[1]==7110]
        self.assertTrue(all(f[4][1] and f[4][2] for f in beam))

    def test_reject_empty_or_missing_fighter_telemetry(self):
        for rows in ([], [[1,1,1,2,0,1000,0,0,-1,-1,1]]):
            with self.assertRaises(RuntimeError): verify(rows)

    def test_reject_invalid_cost_guard_or_round_evidence(self):
        # Known telemetry fixture: entry costs exactly 1000, then round two resets.
        rows=[]
        for p in (1,2):
            rows.extend([[1,p,1,2,7000,1000,3000,0,-1,-1,1],
                         [2,p,1,2,7100,850,2000,1,0,0,1],
                         [3,p,2,2,0,1000,0,0,-1,-1,1]])
        verify(rows)
        for column,value in ((6,2100),(8,-1),(9,-1),(10,0)):
            bad=[r[:] for r in rows]; bad[1][column]=value
            with self.assertRaises(RuntimeError): verify(bad)
        bad=[r for r in rows if r[2]!=2]
        with self.assertRaises(RuntimeError): verify(bad)

if __name__=='__main__': unittest.main()
