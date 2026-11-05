# Normal tutorial selected style declarations

The four [supplied normal tutorial forms](tutorial-normal-form-declarations.md)
name three local style entries for their roots, text blocks and confirmation
buttons. Those entries contain no text, command, focus, hit-test, enabled,
visibility or source/context declaration in the property scope below.
`Grid_Button` has no local style key. Computed defaults and actual style
application remain unresolved.

## Source and selection

These are `client_extraction` findings for the supplied retail 1.23b build
`2012.09.19.0001`. The [form identities](tutorial-normal-form-declarations.md#source-identities-and-decoding)
pin `TutorialWidgetK2.form`, `TutorialWidgetP2.form`, `TutorialWidgetK5.form`
and `TutorialWidgetP5.form`. The [Ask extraction](sqwt-ask-structure.md#source-and-extraction)
pins the sole style input, `client/sqwt/common/default.style`, and its decoded
XML. No additional form, template, style or skin body was inspected here.

All five exact inputs passed the complete signature, size and SHA-256 checks,
strict UTF-8/XML parsing and byte-exact re-encryption using the pinned
[decoder recipe](sqwt-ask-structure.md#reproduction-recipe).
The following raw declarations were checked independently of roundtrip
success. Neither input bytes nor decoded XML are distributed here.

Each form's root and the four named controls have the namespace-qualified
types recorded in the form finding. Their unqualified `SqwtStyle` attributes
have these exact strings in every form:

| Selected node | Element type | Raw `SqwtStyle` |
| --- | --- | --- |
| Root `Window_` plus the form stem | `Window` | `WIN_tutorial` |
| `TextBlock_Text_1` | `TextBlock` | `TBL_null` |
| `TextBlock_Text_2` | `TextBlock` | `TBL_null` |
| `Button_OK` | `Button` | `BTN_basis` |
| `Grid_Button` | `Grid` | Absent |

Absent means there is no such attribute, including a namespace-qualified
attribute of that local name. It does not mean an empty string. Every other
row has exactly one unqualified, nonempty key. No class default was selected
for the unkeyed grid.

The style document has unqualified `StyleResources`, `Widget` and `SqwtStyle`
elements. Each selected key occurs exactly once as `SqwtStyle/@Name`, directly
under one `Widget`, whose raw `Type` string is respectively `Window`,
`TextBlock` or `Button`. These strings equal the selected form element types.
This is local key/type equality, without proof of native selection or
resource resolution.

## Local property scope and remaining resolution

The property check selects the exact, case-sensitive names `Text`, `Content`,
`Command`, `ConsumedCommand`, `Focusable`, `IsTabStop`, `IsHitTestVisible`,
`IsEnabled`, `Visibility`, `Source` and `DataContext`, plus names containing
`TextSource`, `TextDataSource` or `Context`. It checks element and attribute
local names throughout only the three selected entries, and property names
carried by `Name` or `Property` attributes. This includes direct attributes,
property elements and Setter-style property declarations. Namespace-qualified
spellings remain distinct and are not silently substituted for unqualified
ones.

No declaration in that set occurs in the selected entries. In particular,
they supply no local value for the text blocks' missing text/content or the
button's missing focus, hit-test, enabled and visibility attributes. Each
entry has one `Parts` child with raw `Name="Frame"`, containing `Property`
elements. Raw `Condition="SkinFocused"` and `Condition="SkinDisabled"` each
occur once per entry. These are condition strings, not declarations of
`Focusable` or `IsEnabled`, and their evaluation is unproved. No typed or
computed value is inferred from an identifier.

The style root's raw `Source` is `common/default.skin`. That dependency was
not decoded or followed. The local negative above says nothing about its
contents, inherited or transitive values, precedence, or class defaults.
The [form finding's resolver and name-cache qualifications](tutorial-normal-form-declarations.md#template-reference-and-source-ceiling)
still apply. This study identifies no physical text provider, native property
or binding effect, active form, accepted input, actual focus, rendering or
tutorial progression.
