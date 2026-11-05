# Normal tutorial form declarations

The supplied `TutorialWidgetK2`, `TutorialWidgetP2`, `TutorialWidgetK5` and
`TutorialWidgetP5` forms each declare the two named text blocks, confirmation
button and button grid requested by the selected normal tutorial Lua methods.
Their `Button_OK` declarations carry `Command="UILuaCommands.Operate"` and
`Content="@9095"`. This is static declaration compatibility, conditional on
selection and resolution of one of these supplied files.

## Source identities and decoding

These are `client_extraction` findings from the supplied retail 1.23b install,
build `2012.09.19.0001`. Paths below are relative to `client/sqwt/widget/`.
Neither encrypted inputs nor decoded XML are distributed here.

| File | Input bytes | Input SHA-256 | Decoded XML bytes | Decoded XML SHA-256 |
| --- | ---: | --- | ---: | --- |
| `TutorialWidgetK2.form` | 3255 | `e991224e68f485d0956d731ba13d42072bb2756d8afe326ead157704b60e0049` | 3247 | `4f310a8b12204f9e939476f91fd20a772bf7a7adb7da1f8277c7cddc685f29f4` |
| `TutorialWidgetP2.form` | 3334 | `a96c62886a84cb877f76503eac19fd06dba00fc06a9e30b988b08c2282a0e628` | 3326 | `8addd6199e6a71f2a250517e4c826d559159fa4ec85e5657ae280202446b8e6b` |
| `TutorialWidgetK5.form` | 3373 | `7f88a4649d5dea8ab44c4ff748aa161b34bb117037dc12ef3d07e7da81c0195d` | 3365 | `ec065c7605eec27edc0572e9930fb4461f9764a817e31c9fba7eb2131ab9d49e` |
| `TutorialWidgetP5.form` | 3337 | `c8fdc01229a382d902d8041614002ce8aada624111639e9ec093cfce497e39c2` | 3329 | `18cb1d7eb78f8d056031d938dc26fd5e594763bcdbbf1b006a0837b65aaf2468` |
| `TutorialBase.tpl` | 4075 | `55c96560f085df23fa302819c6841e51145fd787c99a89a6f59ce4f2fa4535b7` | 4067 | `760a4246d87218bd6923556530df8872dd35705e01a50a0ea9685389d184d860` |

All five inputs have the complete SQEX signature `5351455800000000`.
Decode with the basename, including case and suffix, as the ASCII Blowfish
key. The existing [Ask extraction recipe](sqwt-ask-structure.md#reproduction-recipe)
owns the decoder identity and little-endian block/partial-tail rule.
For every input, strict UTF-8 decoding, standard-library ElementTree parsing
and byte-exact re-encryption passed. Reproduction also requires the selected
raw declarations below. Roundtrip equality alone does not validate them.

## Selected declarations

All selected element tags use namespace
`http://namespace.square-enix.com/sqwt`. Each form root is `Window`, with raw
`Name="Window_"` followed by that file's stem. Each form contains exactly one
element with each raw `Name` below, with these types and declarations:

| Raw `Name` | Element type | Present selected attributes |
| --- | --- | --- |
| `TextBlock_Text_1` | `TextBlock` | `Focusable="False"`, `IsTabStop="False"`, `IsHitTestVisible="False"` |
| `TextBlock_Text_2` | `TextBlock` | `Focusable="False"`, `IsTabStop="False"`, `IsHitTestVisible="False"` |
| `Button_OK` | `Button` | `Command="UILuaCommands.Operate"`, `Content="@9095"` |
| `Grid_Button` | `Grid` | None of the selected attributes below. |

The selected attributes are `Command`, `Text`, `Content`, `Focusable`,
`IsTabStop`, `IsHitTestVisible`, `IsEnabled` and `Visibility`. Every unlisted
attribute in this set is absent on the corresponding node. In particular,
neither text block has `Text` or `Content`, and the button has no `Text`,
explicit focus, hit-test, enabled or visibility attribute. Both text blocks
and the button have no child elements. The grid has no child property element
for any selected attribute. These absences imply no default or computed value.

The four roots have none of those selected attributes. The roots and selected
nodes have no `Source`, `DataContext` or attribute whose name contains
`TextSource`, `TextDataSource` or `Context`, and no direct property element
with those source/context names. This does not identify the text-data provider,
its table, locale or the meaning of the raw `@9095` content string.

## Template reference and source ceiling

Each form has exactly one `ResourceDictionary` carrying `Source`, with raw
value `widget/TutorialBase.tpl`. Each has one `StaticResource` carrying
`ResourceKey="ControlTemplate_Window_TutorialBase"`. The directly named
template was inspected only for that matching declaration and selected
source/context declarations. Its root is `ResourceDictionary`. Exactly one
direct `ControlTemplate` has `x:Key="ControlTemplate_Window_TutorialBase"`
and raw `TargetType="{x:Type Window}"`, where `x` binds
`http://namespace.square-enix.com/sqwt/x`. Neither root nor selected template
has a `Name`, any selected attribute from the set above, or the selected
source/context attributes or direct property elements. The selected template
contains no text/source/context Setter declaration or text/source/context
attribute, excluding event `SourceType`. None of the four selected control
names occurs in this template input.

Each form root declares `SqwtStyleFile="common/default.style"`. That is the
first unread dependency; its body and further dependencies were not inspected.
Template/style application, inherited values and text-provider resolution
therefore remain unresolved. Matching the template key is string equality,
without a claim that the resource was resolved or applied.

The published resolver in
`xivl-decomp:docs/resource/sqwt-form-locale-resolution.md`, Lua entry,
Directory modes and The opener, owns the conditional directory and language
search. Its Other resource kinds section qualifies direct `Source` handling.
`xivl-decomp:docs/resource/sqwt-name-lookup-cache.md`, Lookup and Rule for a UI
runtime, owns the conditional named-control cache and explicitly excludes
binding resolution. Neither publication establishes a loaded record or lookup
hit for these files.

`xivl-client-scripts:docs/normal-tutorial-panel-completion.md`, Form-name and
declaration boundary, owns the inherited getter/load contract and the missing
alias-to-name argument edge. These declarations establish no active form,
receiver, locale/root, applied text/property/binding, accepted input, rendering,
focus, closure or historical/tutorial progression. No client was activated.
