# Bounded decoded form dependency structure

## Source and method

This is decoded static client-asset metadata (`client_extraction`) for two
identified dependency files. The identified form input is
`client/sqwt/widget/ItemHelpWidget.form`, 45183 bytes, SHA-256
`9108081affa967b9946ebc6ac9d90d0944e3193abc73111b5e8310c377b5fb54`.
Its decoded XML is 45175 bytes, SHA-256
`58f996c347be731f52c10ad728dbd64cb827b327f77bdd2fd94770bdc65b30ef`.
The form's two direct filename references match the two dependency inputs
by exact install-relative path comparison.

`client/sqwt/common/default.style` input is 353783 bytes, SHA-256
`632b314cb2257fcbee42d4b002989a58dfeb42e64af864c1f5356336dc233dc0`. Its decoded UTF-8 XML is
353775 bytes, SHA-256
`33bb178c3b172c62eeb65e8bcaf94f701a0ec3921564e27a619516900896d9f6`. Its extraction manifest is
2707 bytes, SHA-256
`dfaa770638b392bdee31d1096ebd5779083ffb292de831c47b2d6905270fdea7`.

`client/sqwt/common/WINBasis.tpl` input is 6278 bytes, SHA-256
`27d03aca012d1554a3cf8ecd1b5e8da22cc7c815c6f92a1d6d0557dad3bcc5aa`. Its decoded UTF-8 XML is
6270 bytes, SHA-256
`d3227d9200d301ba715250e393d8e09c0ca2d39080754e1ed517692fa7d50700`. Its extraction manifest is
4347 bytes, SHA-256
`8a5e2a3dcf1a2b75e55d925ef795dd1a315b839e0b60740d6d3ea3ea1ca66c13`.

The supplied export provenance records `xivl` version `0.1.0`,
`commit: null`, source revision
`f2a9a2b5a6a4c450458db7a493c25fcdcd70aca0`, and producing executable
23251960 bytes, SHA-256
`4d5ea720fc09073694d4c1864f5844867a41311d72658f8ad267a3fa9948773b`.
That producer identity is reported provenance only. The observation parsed
existing strict UTF-8 XML with Python's standard-library ElementTree. It
did not inspect or execute the producing tool or client.

## Style property carriers

The style tree has 4794 nodes and maximum depth 5, with root
`StyleResources`. Its structural tags are 24 `Widget`, 543 `SqwtStyle`,
711 `Parts` and 3515 `Property` elements. The root carries `Name`,
`Source` and `Version` attributes.

There is one `Widget` element with declared Label type syntax. Its
subtree contains 52 `SqwtStyle`, 52 `Parts` and 416 `Property` elements.
The selected content and font-related Property attribute names are:

- `FontColor`: 101 occurrences.
- `FontEdgeColor`: 101 occurrences.

These counts describe attribute carriers only. `Content`, `FontSize` and
`FontStyle` attributes are absent from these Property elements.

The form's 126 Label elements use four distinct style-key strings. Of
those four strings, 1 matches a named SqwtStyle in the declared Label
Widget subtree, covering 41 form Label elements. This is exact XML
string membership only. It establishes no sentinel, fallback or style
resolution behavior for any key.

## Template structure and limits

The template tree has 83 nodes and maximum depth 8. Its root
is `ResourceDictionary`, with one direct `ControlTemplate` and one
`ContentPresenter` within that template. The form's template resource-key
string matches the ControlTemplate key attribute by exact string equality.
This does not establish Native resource resolution or content forwarding.

The style root has one direct unread filename reference in `Source`.
No further dependency was read. No XML body, Name values, style-key values,
client text or unread dependency filename values are reproduced here.

`FontColor` presence does not establish font selection. Native property
semantics, FontSize and FontStyle semantics, defaults, resource producers,
font attachment, computed layout, rendering and live behavior remain
unverified. This observation supplies structural data for a separately
scoped question only.
