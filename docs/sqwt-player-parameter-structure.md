# PlayerParameter form and template declarations

## Source and extraction

This finding records static client-asset extraction metadata
(`client_extraction`) for supplied build `2012.09.19.0001`. It covers only
`client/sqwt/widget/PlayerParameterWidget.form` and
`client/sqwt/widget/PlayerParameterWidget.tpl`. The build is supplied
provenance. The identified inputs and decoded XML are not distributed here.
Public metadata alone cannot reproduce the extraction.

| Artifact | Bytes | SHA-256 |
|---|---:|---|
| Form input | 5987 | `602cefe3489630240466d9d3dab9484bd59f3dbefaa33a50534f7b65ea5c5b2a` |
| Form decoded strict UTF-8 XML | 5979 | `88c37e2cc1b7ac5e83f24349dfeeedbdd148a44beaefc41015296ad24a5a8237` |
| Template input | 2514 | `81155d689fc5dfe64c348487b9e63470a19e342ba25bf00a6db433672a454c91` |
| Template decoded strict UTF-8 XML | 2506 | `ca8698a204a642943db9cb6f8757e387bc29c664ff7779734b6fa2e405fcafce` |

Both inputs carry the exact eight-byte signature `5351455800000000`.
The extraction checked strict UTF-8 decoding, XML parsing and byte-exact
re-encryption for both inputs.

## Reproduction recipe

Use the basename-key SQEX format in
[xivl-tools:docs/formats/sqex.md, container and key sections](https://github.com/XIVLegacy/xivl-tools/blob/e33378e5f2b429f49ff21a9450e787664227adca/docs/formats/sqex.md#L17-L42)
and the existing
[xivl-tools:tools/blowfish.py, Blowfish](https://github.com/XIVLegacy/xivl-tools/blob/e33378e5f2b429f49ff21a9450e787664227adca/tools/blowfish.py#L60-L125).
The decoder is 4324 bytes, SHA-256
`7c4208f5d3b7acf20bfb67ddcba706cbb10bf4d1c6c1677b4b11d8685774f90e`.

1. Require each input's byte size, SHA-256 and complete signature above.
2. Initialize `Blowfish` separately with the ASCII basename including its
   suffix, `b"PlayerParameterWidget.form"` or `b"PlayerParameterWidget.tpl"`.
   Decrypt after the signature. The decoder uses little-endian block halves
   and preserves a final partial block.
3. Require the decoded identities above. Decode with strict UTF-8 and parse
   with Python's standard-library `xml.etree.ElementTree`.
4. Re-encrypt the decoded bytes, prepend the original signature and require
   byte-for-byte equality with the input.
5. Select namespace-qualified elements and exact attributes below. Preserve
   raw strings without evaluating bindings, resolving resources or using defaults.

## Selected form containment and attributes

The element namespace is `http://namespace.square-enix.com/sqwt`.
The form root is `Window`, with raw `Name="Window_PlayerParameterWidget"`.
Exactly one form element has each primary `ProgressBar/@Name` below.
Each primary has a distinct immediate parent `Grid`. Each selected parent
has no `Name` or `Visibility` attribute and exactly five direct children:
one unnamed `Border`, two named `ProgressBar` elements and two named
`TextBlock` elements. The table lists those named children in document order.

| Primary `ProgressBar` | Other `ProgressBar` | `TextBlock` names |
|---|---|---|
| `ProgressBar_Hp` | `ProgressBar_actionCost_Hp` | `TextBlock_Hp`, `TextBlock_CurrentHp` |
| `ProgressBar_Mp` | `ProgressBar_actionCost_Mp` | `TextBlock_Mp`, `TextBlock_CurrentMp` |
| `ProgressBar_Tp` | `ProgressBar_actionCost_Tp` | `TextBlock_Tp`, `TextBlock_CurrentTp` |

Each primary declares literal `Maximum="999"` and `Value="999"`.
Each has no `Minimum` or `Visibility` attribute. Those absences establish
no defaults or visibility behavior. Each declares
`Template="{StaticResource ControlTemplate_ProgressBar}"`.

Each selected current-caption name occurs exactly once in the form.
Its `Text` attribute is the complete raw string below:

| `TextBlock/@Name` | Raw `Text` |
|---|---|
| `TextBlock_CurrentHp` | `{Binding Path=Value Mode=OneWay ElementName=ProgressBar_Hp:StatusBar ConverterParameter=%.f}` |
| `TextBlock_CurrentMp` | `{Binding Path=Value Mode=OneWay ElementName=ProgressBar_Mp:StatusBar ConverterParameter=%.f}` |
| `TextBlock_CurrentTp` | `{Binding Path=Value Mode=OneWay ElementName=ProgressBar_Tp:StatusBar ConverterParameter=%.f}` |

The primary-name substrings match the selected owners exactly. `StatusBar`
matches the selected template inner name below. These are raw string joins.
The markup does not establish native addressability or binding execution.

## Resources and selected template

The form declares `ResourceDictionary/@Source` values
`common/WINBasisLight_noGrayout.tpl` and `widget/PlayerParameterWidget.tpl`,
in document order. The latter matches the identified template input path
relative to `client/sqwt/`. The form declares
`SqwtStyleFile="common/default.style"`. The primary `SqwtStyle` strings are
`PRB_parameter_hpLargeH`, `PRB_parameter_mpLargeH` and
`PRB_parameter_tpLargeH`, respectively. Dependency contents beyond the two
identified inputs remain unread.

The template root is `ResourceDictionary`. Exactly one `ControlTemplate`
has `x:Key="ControlTemplate_ProgressBar"`, matching the primary resource-key
string. Here `x` denotes `http://namespace.square-enix.com/sqwt/x`.
Its raw `TargetType` is `{x:Type ProgressBar}`.
The selected template contains exactly one inner `ProgressBar`, with
`Name="StatusBar"`, empty `Value=""` and raw
`Maximum="{Binding RelativeSource={RelativeSource TemplatedParent},Path=Maximum}"`.
That inner node has no `Minimum` or `Visibility` attribute.

The selected `ControlTemplate.Triggers` contains one `EventTrigger` with
`RoutedEvent="ValueChanged"` and raw
`SourceName="{Binding RelativeSource={RelativeSource TemplatedParent},Path=Name,Mode=OneWay}"`.
Its nested `BeginStoryboard/Storyboard` contains one `DoubleAnimation` with
`Storyboard.TargetName="StatusBar"`, `Storyboard.TargetProperty="Value"`
and raw `To="{Binding RelativeSource={RelativeSource TemplatedParent},Path=Value}"`.
These declarations establish no event delivery, final applied value or animation
execution.

## Claim boundary

This finding establishes selected static containment, attribute presence and
absence, literal versus binding-shaped values, and exact string equality.
It does not establish runtime defaults, native ownership or addressability,
row visibility semantics, style or resource resolution, computed bindings,
update order, animation timing, rendered layout, visual parity or gameplay.
No live-client result is claimed. No XML body, complete hierarchy or client
bytes are distributed.
