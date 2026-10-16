# PNG sources (art production pending)

Install pinned Pillow with `python3 -m pip install -r requirements-assets.txt`.
Build with `python3 scripts/build_characters.py`. No Blender required.

Optional per-character `manifest.json`:

```json
{"version":1,"facing":"right","frames":[{"sprite":[30000,0],"file":"idle/000.png","origin":[160,240],"scale":1}]}
```

Use original/licensed RGBA PNG sequences with binary alpha (SFF v1 cannot
preserve partial alpha), <=2048 source pixels per dimension. Scale uses nearest
neighbor. Origin is in source pixels; output is 320x320 with origin 160,240.
Source files cannot escape the character directory. IDs refer to the generated
AIR context, not the KFM shared sprite ID. Every context can have unique art.
AIR offsets/flips still apply; render right facing and compensate the existing
AIR transform. Timing, hitboxes and hurtboxes remain unchanged. Run validate.py
for every import. No manual edits to generated AIR/SFF.

Current strict validator requires complete occupancy of collision unions, so
organic artwork is deliberately NOT approved by this first importer. Replace
that policy with artist-reviewed per-frame collision envelopes before shipping
final sprites; do not simply remove collision validation. This sprint delivers
an import foundation and improved collision placeholders, not final character
art. Idle/walk/crouch/jump/normals/guard/hit/fall/charge/special/win animation
contexts already run through the existing AIR. All require artist production
and human review in both facings. No Super Saiyan transformations.
