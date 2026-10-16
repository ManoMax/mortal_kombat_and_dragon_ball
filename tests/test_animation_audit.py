"""Essential coverage and non-static animation checks reject broken evidence."""
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch
from PIL import Image
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
import audit_animations as audit


class AnimationAudit(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup)
        self.root=Path(self.tmp.name);self.folder=self.root/'assets-source/sprites/goku'
        (self.folder/'idle').mkdir(parents=True)
        engine=self.root/'engine/chars/goku';engine.mkdir(parents=True)
        (engine/'kfm.air').write_text('[Begin Action 0]\n30000,0,0,0,10\n30000,1,0,0,10\n30000,2,0,0,10\n30000,3,0,0,10\n')
        self.manifest=dict(frames=[dict(sprite=[30000,i],organic=True) for i in range(4)])
        self.plan=dict(sheets=[dict(animation='idle',file='idle/000.png',grounded=True,anchors=[[0,0]]*4)])
        for i in range(4):
            image=Image.new('RGBA',(320,320));image.putpixel((160,239),(100+i,80,60,255));image.save(self.folder/'idle'/f'{i:03}.png')
        self.write()

    def write(self):
        (self.folder/'manifest.json').write_text(json.dumps(self.manifest))
        (self.folder/'production.json').write_text(json.dumps(self.plan))

    def inspect(self):
        with patch.object(audit,'ROOT',self.root),patch.object(audit,'ESSENTIAL',(0,)):
            return audit.inspect('goku')

    def test_missing_organic_binding_rejected(self):
        self.inspect();self.manifest['frames'].pop();self.write()
        with self.assertRaisesRegex(ValueError,'placeholder'):self.inspect()

    def test_static_sequence_rejected(self):
        data=(self.folder/'idle/000.png').read_bytes()
        for i in range(4):(self.folder/'idle'/f'{i:03}.png').write_bytes(data)
        with self.assertRaisesRegex(ValueError,'distinct'):self.inspect()

    def test_foot_drift_rejected(self):
        image=Image.new('RGBA',(320,320));image.putpixel((160,238),(100,80,60,255));image.save(self.folder/'idle/000.png')
        with self.assertRaisesRegex(ValueError,'baseline'):self.inspect()
