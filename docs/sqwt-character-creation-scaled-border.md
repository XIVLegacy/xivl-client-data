# Character creation vertically scaled borders

Seven standard-definition character creation templates declare a fixed-width
`Border` that is scaled on one axis. This page records the declaration.

## Input and method

These are `client_extraction` findings from the supplied retail 1.23b install,
build `2012.09.19.0001`. The files are under
`client/sqwt/system/bootup/charactercreation/`. Decode each with the basename
as the ASCII Blowfish key following the
[Ask extraction recipe](sqwt-ask-structure.md#reproduction-recipe). Parse the
decoded text with the standard library ElementTree and match tags by local
name. Select each `Border` with `Width="160"` and
`RenderTransformOrigin="0,0.5"` whose `Border.RenderTransform` holds a
`ScaleTransform` with `ScaleY="0.8"` as its only attribute.

## Declarations

No selected `Border` declares a `Height`.

| File | Input bytes | Input SHA-256 | Selected borders |
| --- | ---: | --- | ---: |
| `AppearancePhase.sd.tpl` | 23290 | `0b0e4dade807aa695584d8a5536bb7c3e996c814f2fa30738d2f7dd603e61fbb` | 7 |
| `AppearancePhaseFace.sd.tpl` | 19954 | `27369c3538b7a6b8f682e1451479ce2dada8b0ecc099c353c8fab962d7c14c49` | 11 |
| `AppearancePhaseFeature.sd.tpl` | 25055 | `7c02fcea0618b707b43f7adf579ce69f6235d4126f62c82ca8d1b0acf5d88c85` | 7 |
| `AppearancePhaseHair.sd.tpl` | 14844 | `624b76f089e515be73e9e9b8cabc2b1c8fed0d19c4315991292f28764ad97dba` | 8 |
| `BirthdayPhase.sd.tpl` | 19304 | `f09460ea3d552a05edf6ad1558c365ab00013ba5a53da49df7ba2b31f2c4abdf` | 3 |
| `BirthdayPhase.de.sd.tpl` | 19316 | `e65554c2fb53f0cd32e2ae9a47a4538f048390b6f5ec03480c730ae5e23eba1f` | 3 |
| `BirthdayPhase.fr.sd.tpl` | 19304 | `83bbe6ab91f2166befd59b694206298cdccee6475ddb9455dea1a2ef330564d0` | 3 |

The `ScaleTransform` declares no `ScaleX`, `CenterX` or `CenterY`. The
[render transform matrix](https://github.com/XIVLegacy/xivl-decomp/blob/main/docs/resource/sqwt-render-transform.md#matrix)
page owns how the client places the center from `RenderTransformOrigin` and
the arranged size, and the value of an unwritten scale factor. The
declarations do not establish the arranged height or rendered output.
