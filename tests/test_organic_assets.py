"""RGBA fidelity, malformed manifests, crop/origin guards and SFF corruption."""
import hashlib
import json
from pathlib import Path
import sys
import tempfile
import unittest
from PIL import Image

sys.path.insert(0, str(Path(__file__).resolve().parents[1]/'scripts'))
from png_pipeline import load_overrides
from sff_rgba import write_sff, read_sff


class OrganicAssets(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.folder = self.root/'assets-source/sprites/goku'
        self.folder.mkdir(parents=True)
        self.image = Image.new('RGBA', (8, 8))
        self.image.putpixel((3, 4), (200, 70, 10, 128))
        self.image.save(self.folder/'frame.png')
        self.frame = dict(sprite=[30000, 0], file='frame.png', origin=[3, 4])
        self.spec = dict(version=1, facing='right', frames=[self.frame])

    def load(self):
        (self.folder/'manifest.json').write_text(json.dumps(self.spec))
        return load_overrides(self.root, 'goku')

    def test_partial_alpha_roundtrip_and_determinism(self):
        image = self.load()[30000, 0]
        sprites = [((30000, 0), (160, 240), image)]
        first, second = self.root/'a.sff', self.root/'b.sff'
        write_sff(first, sprites)
        write_sff(second, sprites)
        self.assertEqual(first.read_bytes(), second.read_bytes())
        x, y, (w, h, stride, alpha) = read_sff(first.read_bytes())[30000, 0]
        self.assertEqual((x, y, w, h), (160, 240, 320, 320))
        self.assertEqual(alpha[240*stride+160], 128)
        self.assertEqual(sum(bool(a) for a in alpha), 1)
        for broken in (first.read_bytes()[:-1], first.read_bytes()+b'x'):
            with self.assertRaises(ValueError): read_sff(broken)

    def test_identical_frames_use_safe_backward_links(self):
        import struct
        image = self.load()[30000, 0]
        path = self.root/'linked.sff'
        sprites = [((30000, i), (160, 240), image) for i in range(4)]
        write_sff(path, sprites)
        original = path.read_bytes()
        self.assertEqual(struct.unpack_from('<I', original, 512+28+20)[0], 0)
        self.assertEqual(len(read_sff(original)), 4)
        write_sff(path, list(reversed(sprites)))
        self.assertEqual(path.read_bytes(), original)
        broken = bytearray(original)
        struct.pack_into('<H', broken, 512+28+12, 1)
        with self.assertRaisesRegex(ValueError, 'link'): read_sff(broken)

    def test_invalid_scales_origins_and_facing(self):
        for scale in (0, -1, True, float('nan'), float('inf'), 9):
            self.frame['scale'] = scale
            with self.subTest(scale=scale), self.assertRaises(ValueError): self.load()
        self.frame.pop('scale')
        for origin in ([-1, 0], [9, 0], [1.5, 0]):
            self.frame['origin'] = origin
            with self.subTest(origin=origin), self.assertRaises(ValueError): self.load()
        self.frame['origin'] = [3, 4]
        self.spec['facing'] = 'left'
        with self.assertRaises(ValueError): self.load()

    def test_organic_bounds_scale_and_crop(self):
        self.frame.update(organic=True, normalized_bounds=[0, 0, 1, 1])
        self.load()
        self.frame['scale'] = 2
        with self.assertRaises(ValueError): self.load()
        self.frame['scale'] = 1
        self.image.putpixel((0, 0), (255, 255, 255, 255))
        self.image.save(self.folder/'frame.png')
        with self.assertRaises(ValueError): self.load()

    def test_extractor_rejects_cut_source_and_pins_ground(self):
        import prepare_character_art as extractor
        from unittest.mock import patch
        sheet = dict(file='frame.png', animation='idle', columns=1, anchors=[[3, 4]], scale=1,
                     grounded=True, bindings=[[[30000, 0], 0]])
        plan = self.folder/'production.json'
        plan.write_text(json.dumps(dict(sheets=[sheet])))
        with patch.object(extractor, 'ROOT', self.root):
            extractor.prepare('goku')
            manifest = json.loads((self.folder/'manifest.json').read_text())
            self.assertEqual(manifest['frames'][0]['normalized_bounds'][3], 0)
            sheet['rectangles'] = [[3, 4, 5, 6]]
            plan.write_text(json.dumps(dict(sheets=[sheet])))
            with self.assertRaisesRegex(ValueError, 'cuts visible artwork'): extractor.prepare('goku')

    def test_empty_duplicate_and_integrity(self):
        self.frame['sha256'] = hashlib.sha256((self.folder/'frame.png').read_bytes()).hexdigest()
        self.load()
        self.image.putpixel((3, 4), (20, 20, 20, 128))
        self.image.save(self.folder/'frame.png')
        with self.assertRaises(ValueError): self.load()
        self.frame.pop('sha256')
        self.spec['frames'].append(self.frame.copy())
        with self.assertRaises(ValueError): self.load()
        self.spec['frames'].pop()
        Image.new('RGBA', (8, 8)).save(self.folder/'frame.png')
        with self.assertRaises(ValueError): self.load()

    def test_air_hurtbox_override_preserves_other_frames_and_hits(self):
        from air_geometry import frames, apply_hurtboxes
        source = '[Begin Action 7100]\nClsn1Default: 1\nClsn1[0] = 16,-80,61,-71\nClsn2Default: 1\nClsn2[0] = -12,-80,12,0\n7100,0,0,0,10\n7100,1,0,0,10\n'
        before = list(frames(source))
        after = list(frames(apply_hurtboxes(source, {(7100, 0): [[-20, -90, 20, 0]]})))
        self.assertEqual(after[0][2:4], before[0][2:4])
        self.assertEqual(after[0][4][1], before[0][4][1])
        self.assertEqual(after[0][4][2], [(-20, -90, 20, 0)])
        self.assertEqual(after[1][2:], before[1][2:])

    def test_hurtboxes_are_independent_but_ordered(self):
        self.frame.update(organic=True, normalized_bounds=[0, 0, 1, 1], hurtboxes=[[-10, -90, 10, 0]])
        self.load()  # No pixel-by-pixel box coverage requirement.
        self.frame['hurtboxes'] = [[10, 0, -10, -90]]
        with self.assertRaises(ValueError): self.load()


class RuntimeEvidence(unittest.TestCase):
    def test_missing_side_or_idle_frame_is_rejected(self):
        from sprint4_smoke import verify
        valid = [[i, p, 0, 30000, i] for p in (1, 2) for i in range(4)]
        valid += [[5, p, action, 30000, 20] for p in (1, 2) for action in (20, 21, 200)]
        verify(valid)
        for broken in ([], [r for r in valid if r[1] == 1], [r for r in valid if r[4] != 3], [r for r in valid if r[2] != 200]):
            with self.assertRaises(ValueError): verify(broken)


if __name__ == '__main__': unittest.main()
