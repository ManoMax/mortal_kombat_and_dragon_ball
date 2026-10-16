"""Importer acceptance and rejection using real RGBA files."""
import json
import sys
import tempfile
import unittest
from pathlib import Path
from PIL import Image
sys.path.insert(0, str(Path(__file__).resolve().parents[1]/'scripts'))
from png_pipeline import load_overrides
from build_characters import pcx
from validate import decode


class PNGPipeline(unittest.TestCase):
    def test_origin_transparency_and_palette(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp); folder=root/'assets-source/sprites/goku'; folder.mkdir(parents=True)
            image=Image.new('RGBA',(4,4)); image.putpixel((1,2),(255,60,10,255)); image.save(folder/'000.png')
            spec={'version':1,'facing':'right','frames':[{'sprite':[30000,0],'file':'000.png','origin':[1,2]}]}
            (folder/'manifest.json').write_text(json.dumps(spec))
            result=load_overrides(root,'goku',pcx)
            w,h,stride,pixels=decode(result[30000,0])
            self.assertEqual((w,h),(320,320))
            self.assertNotEqual(pixels[240*stride+160],0)
            self.assertEqual(sum(bool(p) for p in pixels),1)
            image.putpixel((1,2),(255,60,10,128)); image.save(folder/'000.png')
            with self.assertRaises(ValueError): load_overrides(root,'goku',pcx)
            spec['frames'][0]['file']='../escape.png'
            (folder/'manifest.json').write_text(json.dumps(spec))
            with self.assertRaises(ValueError): load_overrides(root,'goku',pcx)

if __name__ == '__main__': unittest.main()
