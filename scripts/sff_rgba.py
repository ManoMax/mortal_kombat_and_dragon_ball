"""Deterministic SFF 2.0.1 PNG32 subset; straight RGBA, no palette quantization."""
from io import BytesIO
import struct
from PIL import Image


def write_sff(path, sprites):
    nodes = bytearray()
    payload = bytearray()
    keys = set()
    images = {}
    for (group, number), (x, y), image in sorted(sprites, key=lambda item: item[0]):
        if (group, number) in keys:
            raise ValueError('Duplicate sprite')
        keys.add((group, number))
        stream = BytesIO()
        image.convert('RGBA').save(stream, format='PNG', compress_level=9)
        blob = struct.pack('<I', image.width * image.height * 4) + stream.getvalue()
        identity = (x, y, blob)
        if identity in images:
            link, offset, length = images[identity], 0, 0
        else:
            link, offset, length = 0, len(payload), len(blob)
            images[identity] = len(keys)-1
            payload.extend(blob)
        nodes.extend(struct.pack('<HHHHhhHBBIIHH', group, number, image.width,
                                 image.height, x, y, link, 12, 32,
                                 offset, length, 0, 0))
    header = bytearray(512)
    header[:16] = b'ElecbyteSpr\0' + bytes((0, 1, 0, 2))
    start = 512 + len(nodes)
    struct.pack_into('<8I', header, 36, 512, len(keys), start, 0,
                     start, len(payload), start + len(payload), 0)
    path.write_bytes(header + nodes + payload)


def read_sff(data):
    """Validate our deliberately narrow writer subset and decode exact alpha."""
    if len(data) < 512 or data[:16] != b'ElecbyteSpr\0' + bytes((0, 1, 0, 2)):
        raise ValueError('Unsupported SFF v2 header')
    nodes, count, palettes, npal, start, size, translated, tsize = struct.unpack_from('<8I', data, 36)
    if not count or nodes != 512 or palettes != start or npal or start != 512 + 28 * count or translated != start + size or tsize or translated != len(data):
        raise ValueError('Invalid SFF sections')
    result = {}
    end = 0
    decoded = []
    for index in range(count):
        g, n, w, h, x, y, link, fmt, depth, offset, length, pal, flags = struct.unpack_from('<HHHHhhHBBIIHH', data, nodes + 28 * index)
        if length == 0:
            if (g, n) in result or link >= index or offset or fmt != 12 or depth != 32 or pal or flags:
                raise ValueError('Invalid SFF sprite link')
            sx, sy, pixels = decoded[link]
            if (w, h, x, y) != (pixels[0], pixels[1], sx, sy):
                raise ValueError('Linked sprite origin/geometry mismatch')
            result[g, n] = decoded[link]
            decoded.append(result[g, n])
            continue
        if (g, n) in result or link or fmt != 12 or depth != 32 or pal or flags or offset != end or length < 4 or offset + length > size:
            raise ValueError('Invalid SFF sprite node')
        blob = data[start + offset:start + offset + length]
        if struct.unpack_from('<I', blob)[0] != w * h * 4:
            raise ValueError('Invalid decoded length')
        with Image.open(BytesIO(blob[4:])) as check:
            check.verify()
        with Image.open(BytesIO(blob[4:])) as image:
            if image.format != 'PNG' or image.mode != 'RGBA' or image.size != (w, h):
                raise ValueError('Invalid PNG32 payload')
            image.load()
            result[g, n] = (x, y, (w, h, w, image.getchannel('A').tobytes()))
        decoded.append(result[g, n])
        end += length
    if end != size:
        raise ValueError('Trailing SFF payload')
    return result
