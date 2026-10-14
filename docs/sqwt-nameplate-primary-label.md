# Nameplate primary-label form attributes

## Source and extraction

This finding records supplied static client-asset extraction metadata
(`client_extraction`) for build `2012.09.19.0001`. It covers only
`client/sqwt/system/ingame/NamePlateWidget.form`.
The input and decoded XML are not distributed with this repository.
Their identities and the extraction results below are declared metadata,
not independent reproduction results from the public tree.

| Artifact | Bytes | SHA-256 |
|---|---:|---|
| Named form input | 4048 | `9ac30efaee82d7045a5dfda9f0044d6090cb16b092415ff88ce3b1dee64d5c81` |
| Decoded strict UTF-8 XML | 4040 | `de6ca8942674c3d8a8e66e442b4237b2d317dcff47cbe57caedf690505c2649f` |

The input carries the exact eight-byte SQEX signature
`5351455800000000`. The supplied extraction reports byte-exact
re-encryption of the decoded body to the identified input.

## Reproduction recipe

Use the existing basename-key SQEX decoder described in
[xivl-tools:docs/formats/sqex.md, container and key sections](https://github.com/XIVLegacy/xivl-tools/blob/c364f4cc8d8d85f7bc900b7f5d5e44687ac66f06/docs/formats/sqex.md#L17-L42).
The decoder is
[xivl-tools:tools/blowfish.py, Blowfish](https://github.com/XIVLegacy/xivl-tools/blob/c364f4cc8d8d85f7bc900b7f5d5e44687ac66f06/tools/blowfish.py#L60-L125),
4324 bytes, SHA-256
`7c4208f5d3b7acf20bfb67ddcba706cbb10bf4d1c6c1677b4b11d8685774f90e`.

1. Check the supplied file's size and SHA-256 against the input identity.
   Require all eight signature bytes before decoding.
2. Initialize `Blowfish` with `b"NamePlateWidget.form"`. Decrypt the bytes
   after the signature using `Blowfish.decrypt`. The existing decoder maps
   whole eight-byte blocks with little-endian halves and preserves a final
   partial block.
3. Check the decoded bytes against the XML identity. Decode with strict
   UTF-8 and parse with Python's standard-library `xml.etree.ElementTree`.
4. Re-encrypt those decoded bytes with `Blowfish.encrypt`, prepend the
   unchanged signature, and require byte-for-byte equality with the input.
5. Select the element by the namespace-qualified `TextBlock` tag and the
   exact `Name` attribute below. Record its attributes as strings without
   resolving styles, converting values, or applying defaults.

This recipe reproduces the declared extraction from a separately supplied
identified input. The public metadata alone cannot execute that reproduction.

## Raw XML selection

The explicit XML namespace is `http://namespace.square-enix.com/sqwt`.
Exactly one element has local name `TextBlock` and raw `Name` value
`TextBlock_PrimaryLabel`. The named element is a `TextBlock`, not a `Label`.
It carries exactly these ten attributes:

| Attribute | Raw string value |
|---|---|
| FontSize | `24` |
| FontStyle | `Italic` |
| FontHeightSpacing | `0` |
| IsTabStop | `False` |
| VerticalContentAlignment | `Center` |
| FontEdgeColor | `#ff262626` |
| SqwtStyle | `TBL_namePlate` |
| Name | `TextBlock_PrimaryLabel` |
| Margin | `4,0,4,0` |
| Height | `36` |

The selected element has no child elements and no `Text`, `Content`, or
`FontFamily` attribute. These are absence observations on this element only.
The raw `Window/@SqwtStyleFile` value is `common/default.style`.
This records a filename attribute without resolving or loading its target.

## Claim boundary

The values above are raw XML strings. They establish no runtime property
meaning, default, font asset or font pair, style precedence, computed layout,
loading behavior, text measurement, or rendering result. The referenced style,
template, and transitive files are outside this finding. No XML body or client
bytes are reproduced here, and no live-client result is claimed.
