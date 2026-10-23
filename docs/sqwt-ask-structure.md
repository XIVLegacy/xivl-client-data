# Ask form, template and style declarations

## Source and extraction

This finding records static client-asset extraction metadata
(`client_extraction`) for supplied build `2012.09.19.0001`. It covers only
`client/sqwt/widget/AskWidget.form`, `client/sqwt/widget/AskWidget.tpl`,
`client/sqwt/common/WINBasis.tpl` and `client/sqwt/common/default.style`.
The build is supplied provenance. The inputs and decoded XML are not
distributed here. Public metadata alone cannot reproduce the extraction.

| Artifact | Bytes | SHA-256 |
|---|---:|---|
| Form input | 2619 | `e56d47f2d5a27f99f2d13a9763d960dd471b456868001f657f515c5230bcc92a` |
| Form decoded strict UTF-8 XML | 2611 | `227990f424902da69814b3de7bcc78ed3143435bbe5030192f14b9ac45a17af7` |
| Ask template input | 535 | `e9ffd9acfb89498efd2ffac3e346e0f826082443cba64c6fc91e6b931e9189ad` |
| Ask template decoded strict UTF-8 XML | 527 | `2cbe61b006602d9451419b64fa39abfc4bad908061e2d47cf82c225f67bd0e6f` |
| WINBasis input | 6278 | `27d03aca012d1554a3cf8ecd1b5e8da22cc7c815c6f92a1d6d0557dad3bcc5aa` |
| WINBasis decoded strict UTF-8 XML | 6270 | `d3227d9200d301ba715250e393d8e09c0ca2d39080754e1ed517692fa7d50700` |
| Style input | 353783 | `632b314cb2257fcbee42d4b002989a58dfeb42e64af864c1f5356336dc233dc0` |
| Style decoded strict UTF-8 XML | 353775 | `33bb178c3b172c62eeb65e8bcaf94f701a0ec3921564e27a619516900896d9f6` |

All four inputs carry the exact eight-byte signature `5351455800000000`.
The supplied extraction reports strict UTF-8 decoding, XML parsing and
byte-exact re-encryption for all four inputs.

## Reproduction recipe

Use the basename-key SQEX format in
[xivl-tools:docs/formats/sqex.md, container and key sections](https://github.com/XIVLegacy/xivl-tools/blob/e33378e5f2b429f49ff21a9450e787664227adca/docs/formats/sqex.md#L17-L42)
and the existing
[xivl-tools:tools/blowfish.py, Blowfish](https://github.com/XIVLegacy/xivl-tools/blob/e33378e5f2b429f49ff21a9450e787664227adca/tools/blowfish.py#L60-L125).
The decoder is 4324 bytes, SHA-256
`7c4208f5d3b7acf20bfb67ddcba706cbb10bf4d1c6c1677b4b11d8685774f90e`.

1. Require each input's byte size, SHA-256 and complete signature above.
2. Initialize `Blowfish` with the ASCII basename including its suffix,
   `b"AskWidget.form"`, `b"AskWidget.tpl"`, `b"WINBasis.tpl"` or
   `b"default.style"`, and decrypt after the signature.
   The decoder uses little-endian block halves and preserves a partial tail.
3. Require the decoded identities above. Decode with strict UTF-8 and parse
   with Python's standard-library `xml.etree.ElementTree`.
4. Re-encrypt, prepend the original signature and require exact input equality.
5. Select namespace-qualified tags and exact attributes below. Record raw
   strings without resolving references, evaluating bindings or using defaults.

## Selected controls and template

The Ask form and both templates use the element namespace
`http://namespace.square-enix.com/sqwt`.
The form root is `Window`. Exactly one form element has each selected raw
`Name` below, and its tag matches the listed type:

| Element tag | Raw `Name` |
|---|---|
| `Window` | `Window_AskWidget` |
| `TextBlock` | `TextBlock_Question` |
| `ListBox` | `ListBox_Answers` |
| `Button` | `Button_Previous` |
| `Button` | `Button_Next` |

The selected question node has no `Text` or `Content` attribute and no child
elements. The selected answers node has no `Template` or `ItemTemplate`
attribute and no child elements. These are bounded observations on those
nodes. Question and answer roles follow their names. Runtime text/item
assignment and binding remain unresolved.

The Ask template root is `ResourceDictionary`, containing exactly one
`ControlTemplate` with raw `TargetType="{x:Type ListBoxItem}"` and
`x:Key="ControlTemplate_ListBoxItem"`. Here `x` denotes
`http://namespace.square-enix.com/sqwt/x`. That template has no `Name`
attribute. Its direct child `Button` has the unique template
`Name="TemplateButton_Answer"` and raw `Command="UILuaCommands.Operate"`.
This selected button has no `Owner`, `Part`, `Text` or `Content` attribute.
Target type and containment establish no runtime ownership or native-part
contract. A direct `Setter` declares `Property="IsTabStop"`, `Value="False"`.

## References and commands

The form declares `ResourceDictionary/@Source` values
`common/WINBasis.tpl` and `widget/AskWidget.tpl`, in document order.
Its `Window.Template/StaticResource/@ResourceKey` is
`ControlTemplate_Window_WINBasis`. The form root declares
`SqwtStyleFile="common/default.style"`. The selected answers node declares
`SqwtStyle="LIB_basis"`. The selected template button declares
`SqwtStyle="BTN_basis_listboxSelect"`.

`WINBasis.tpl` has root `ResourceDictionary`. Exactly one namespace-qualified
`ControlTemplate` has `x:Key="ControlTemplate_Window_WINBasis"`, matching the
form's resource-key string. Its raw `TargetType` is `{x:Type Window}`.

`default.style` uses unqualified `StyleResources`, `Widget` and `SqwtStyle`
tags for the following selected declarations. Each style name occurs exactly
once among `SqwtStyle/@Name` values and has one containing `Widget`:

| Raw `SqwtStyle/@Name` | Containing `Widget/@Type` |
|---|---|
| `LIB_basis` | `ListBox` |
| `BTN_basis_listboxSelect` | `Button` |

These names match the selected controls' style-key strings, and the type
strings match their element tags. This records declaration containment and
string equality. Successful style or resource resolution is unverified.
The four inputs do not establish the runtime association from
`ListBox_Answers` to `ControlTemplate_ListBoxItem`. The style root declares
another `Source` dependency outside these four inputs. It remains unread,
and transitive resource closure is unresolved.

| Selected form node | Attribute | Raw value |
|---|---|---|
| `Window_AskWidget` | `ConsumedCommand` | `UILuaCommands.Cancel` |
| `Button_Previous` | `Command` | `UILuaCommands.PagePrevious` |
| `Button_Next` | `Command` | `UILuaCommands.PageNext` |

Neither `AskWidget.form` nor `AskWidget.tpl` contains a namespace-qualified
`CommandTrigger` or `EventTrigger` element. This absence is bounded to those
two documents.
Command attributes do not establish delivery or input behavior.

## Claim boundary

These static declarations identify a possible choice-panel surface.
They do not establish native host APIs, selection base or index, click/key
behavior, computed bindings, text assignment, style/font resolution, computed
layout, command delivery, animation execution/timing/reuse or retail visual
or gameplay parity. No live-client result is claimed. No XML body, complete
hierarchy or client bytes are distributed.
