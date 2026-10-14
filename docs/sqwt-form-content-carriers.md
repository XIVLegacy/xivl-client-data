# Bounded decoded form Content carriers

## Source and method

One Original named-form input is identified by its 45183-byte size and
SHA-256 `9108081affa967b9946ebc6ac9d90d0944e3193abc73111b5e8310c377b5fb54`.
The install-relative source is `client/sqwt/widget/ItemHelpWidget.form`.
This is decoded static client-asset metadata (`client_extraction`) for one
identified file only.
Its existing decoded UTF-8 XML is 45175 bytes with SHA-256
`58f996c347be731f52c10ad728dbd64cb827b327f77bdd2fd94770bdc65b30ef`.
The extraction manifest is 5774 bytes with SHA-256
`31093be45e16c8776c87fa2696ea3378deb0d7cd5875c9f3e13ec217a36b9fa0`.

The export provenance records `xivl` version `0.1.0`, `commit: null` and
`source_revision: f2a9a2b5a6a4c450458db7a493c25fcdcd70aca0`. It identifies
the producing executable as 23251960 bytes with SHA-256
`4d5ea720fc09073694d4c1864f5844867a41311d72658f8ad267a3fa9948773b`.
This observation parsed the existing decoded data with Python's
standard-library `xml.etree.ElementTree`. It did not inspect the decoder
executable or Source, repeat the export or execute the client.

The one parsed tree has 403 nodes and maximum depth 9. Its root local tag
is `Window`. No DOCTYPE or entity declaration appears in this payload.

## Retained installation labels

The retained installation label `game.ver` is 15 bytes with SHA-256
`3dbeed87ae1f2805bec69d63137e3deca9dd444ad5caa3ea5dedb68b8a50bfef`.
Its ASCII value is `2012.09.19.0001`. The retained `patch.ver` label is 5
bytes with SHA-256
`cbe2f3b81d7b70aafe1eeca3ccbfc573f4b5156245bf697fc9dafd82527df9b6`
and ASCII value `1.23b`.

These two labels provide retained installation context. They do not prove
per-file delivery of the observed form, active configuration, resource or
font selection, or live rendering.

## Literal Content carrier

The tree has 126 `Label` elements. Of these, 111 have a `Content` string
attribute and 15 lack a Content carrier. All 111 present values classify
as plain literals under the syntax rule below. Their lengths range from 1
to 16 Unicode code points. No present Content value is empty,
markup-shaped or binding-looking, and no `Label.Content` property element
appears.

The classifier treats whitespace-only values as empty, strings enclosed
in braces as binding-looking, child elements or tag-shaped text as markup,
and the remainder as plain literals. This is an XML-data classification,
not a Native property type or text interpretation.

There is no `TextBlock` tag, `Text` attribute or Text property-element
carrier in this document. Its literal-data carrier is `Label/@Content`.
There are 210 `Name` attributes, all unique, each matching
`[A-Za-z_][A-Za-z0-9_]*`. No Native name-resolution rule follows from that
syntax observation.

## Layout and references

| Attribute on Label | Count |
|---|---:|
| Margin | 42 |
| HorizontalAlignment | 99 |
| VerticalAlignment | 31 |
| Width | 29 |
| Height | 120 |
| VerticalContentAlignment | 94 |
| HorizontalContentAlignment | 47 |
| Grid.Column | 38 |
| Grid.Row | 10 |

These counts record XML attribute associations. They do not establish
computed layout or pixel bounds.

`Window.Resources` contains one `ResourceDictionary` with a `Source`
attribute. `Window.Template` contains one `StaticResource` with a
`ResourceKey` attribute. `Window/@SqwtStyleFile` and
`ResourceDictionary/@Source` carry two explicit dependency filenames.
There are three `Binding` elements with `ElementName`, `Path`, `Mode` and
`ConverterParameter` attributes. All 126 Label elements carry `SqwtStyle`.

The referenced dependency files and transitive resources were not read.
Resource, style-key and binding resolution remain unobserved. No default
font, FontStyle meaning, resource selection, Native class behavior,
font attachment, text measurement or live drawing is established.

This finding supplies counts and property carriers without Name values,
Content strings, dependency filename values or the XML body. Literal data
is present for a separately scoped attachment question. Attachment and
rendering support remain outside this data observation.
