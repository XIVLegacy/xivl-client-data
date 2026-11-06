# Parley message widget declarations

The supplied `NegotiationWidget.form` and `NegotiationMessageWidget.form`
declare SQWT Window roots named `Window_NegotiationWidget` and
`Window_NegotiationMessageWidget`. Their selected root declarations contain
no script or class discriminator. These two files therefore do not choose
between the two script modules with the `negotiationmessagewidget.lua`
basename.

## Source identities and decoding

These are `client_extraction` findings from the supplied retail 1.23b install.
The inspected `game.ver` marker contained `2012.09.19.0001`. Paths below are
relative to `client/sqwt/widget/`. The marker identifies the supplied install;
the exact input pins identify the files. Inputs and decoded XML are not
distributed here.

| File | Input bytes | Input SHA-256 | Decoded XML bytes | Decoded XML SHA-256 |
| --- | ---: | --- | ---: | --- |
| `NegotiationWidget.form` | 9254 | `0328f3b103658af4b91bd0f3a47112db8ceb2042acde5c970c9d5f8bf77f836d` | 9246 | `ab6eadae80c17253b3f98aeec8ac740e3f8e2e77ea24be2620a87847680715ce` |
| `NegotiationMessageWidget.form` | 3383 | `edce5467cb7b8008fbb0febec9418a22a719dc94fa2ae0b2ba38440e8a59ecd3` | 3375 | `549a281a5d98299a228bbc80dc61a8e54be8d3c192a06a3a95e549f2e587153e` |

Both inputs have the full SQEX signature `5351455800000000`. Decode using
the ASCII basename, including case and suffix, as the Blowfish key. The
[Ask reproduction recipe](sqwt-ask-structure.md#reproduction-recipe) owns
the pinned decoder and little-endian block/partial-tail rule. For these
inputs, strict UTF-8 decoding, standard-library ElementTree parsing and
byte-exact re-encryption passed. Selected declarations were checked
independently of the roundtrip.

## Selected roots and name boundary

Both roots have local element type `Window` in namespace
`http://namespace.square-enix.com/sqwt`. The default namespace is that URI,
and prefix `x` binds `http://namespace.square-enix.com/sqwt/x`. These are XML
namespace declarations, without a Lua module-path discriminator.

| File | Raw root `Name` |
| --- | --- |
| `NegotiationWidget.form` | `Window_NegotiationWidget` |
| `NegotiationMessageWidget.form` | `Window_NegotiationMessageWidget` |

Neither root has an attribute whose local name contains `Script`, `Class`,
`Namespace` or `Type`, ignoring case. Neither has a direct property element
with such a local name. These are scoped absences, without an inferred
default or runtime binding.

In `NegotiationWidget.form`, no element has a raw `Name` containing the exact
case-sensitive string `NegotiationMessageWidget`, or local element type
`NegotiationMessageWidget`. In `NegotiationMessageWidget.form`, the only
element matching either criterion is its own root. In particular, neither
file declares a node with exact raw `Name="NegotiationMessageWidget"`.
The prefixed root name is a literal declaration, not proof of a name alias,
loaded child, parent relationship or native lookup hit.

## Direct template references and selection boundary

The selected root resource and template property declarations carry these
raw strings:

| File | `ResourceDictionary/@Source` under root resources | `StaticResource/@ResourceKey` under root template |
| --- | --- | --- |
| `NegotiationWidget.form` | `widget/NegotiationWidget.tpl` | `ControlTemplate_Window_WINBasis` |
| `NegotiationMessageWidget.form` | `common/WINBasisLight_noGrayout.tpl` | `ControlTemplate_Window_WINBasisLight` |

Each listed field occurs once in its selected property. The references do
not establish successful resolution or application. Neither referenced
template body is part of this finding.

`xivl-client-scripts:docs/parley-child-initialization-request.md`, Conditional
Parley composition, owns the request using child-name operand
`"NegotiationMessageWidget"`. Its manifest distinguishes
`widget/ask/negotiationmessagewidget.lua` from
`widget/negotiationmessagewidget.lua`. Literal name compatibility with these
two forms supplies no choice between those script modules. Actual selected
class, form, namespace-to-class binding, initialization delivery and applied
properties remain unresolved. This finding interprets no other controls'
text, layout or timing and establishes no rendered or historical behavior.
