# PlayerParameter form and template declarations

## Source and extraction

This finding records static client-asset extraction metadata
(`client_extraction`) for supplied build `2012.09.19.0001`. It covers exactly these three inputs under `client/sqwt/`:

| Input path | Read boundary |
|---|---|
| `widget/PlayerParameterWidget.form` | Selected form declarations |
| `widget/PlayerParameterWidget.tpl` | Selected progress-bar and label templates |
| `common/WINBasisLight_noGrayout.tpl` | Selected Window template declarations |

The build is supplied
provenance. The identified inputs and decoded XML are not distributed here.
Public metadata alone cannot reproduce the extraction.

| Artifact | Bytes | SHA-256 |
|---|---:|---|
| Form input | 5987 | `602cefe3489630240466d9d3dab9484bd59f3dbefaa33a50534f7b65ea5c5b2a` |
| Form decoded strict UTF-8 XML | 5979 | `88c37e2cc1b7ac5e83f24349dfeeedbdd148a44beaefc41015296ad24a5a8237` |
| Template input | 2514 | `81155d689fc5dfe64c348487b9e63470a19e342ba25bf00a6db433672a454c91` |
| Template decoded strict UTF-8 XML | 2506 | `ca8698a204a642943db9cb6f8757e387bc29c664ff7779734b6fa2e405fcafce` |
| Window template input | 4303 | `be271e92c52765dd1cfd8c786c0f77144440520b84239f08db5b0c21c97c8949` |
| Window template decoded strict UTF-8 XML | 4295 | `47271a67f14e47e0fb458e1a211de9366b17c112576e951668bd519e116ee6d8` |

All three inputs carry the exact eight-byte signature `5351455800000000`.
The extraction checked strict UTF-8 decoding, XML parsing and byte-exact
re-encryption for all three inputs.

## Reproduction recipe

Use the basename-key SQEX format in
[xivl-tools:docs/formats/sqex.md, container and key sections](https://github.com/XIVLegacy/xivl-tools/blob/e33378e5f2b429f49ff21a9450e787664227adca/docs/formats/sqex.md#L17-L42)
and the existing
[xivl-tools:tools/blowfish.py, Blowfish](https://github.com/XIVLegacy/xivl-tools/blob/e33378e5f2b429f49ff21a9450e787664227adca/tools/blowfish.py#L60-L125).
The decoder is 4324 bytes, SHA-256
`7c4208f5d3b7acf20bfb67ddcba706cbb10bf4d1c6c1677b4b11d8685774f90e`.

1. Require each input's byte size, SHA-256 and complete signature above.
2. Initialize `Blowfish` separately with the ASCII basename including its
   suffix: `b"PlayerParameterWidget.form"`, `b"PlayerParameterWidget.tpl"`
   or `b"WINBasisLight_noGrayout.tpl"`.
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

## Selected ancestors and sibling declarations

Each selected primary has this kind/name chain from the form root:
`Window/Window_PlayerParameterWidget -> Grid/unnamed ->
Button/Button_PlayerParameter -> Grid/unnamed -> Grid/unnamed ->
ProgressBar/ProgressBar_Hp|Mp|Tp`. The final unnamed-grid position denotes three
separate elements, one per primary. The two earlier unnamed grids are shared.

The outer shared grid has exactly two direct children, in document order:
`Label/Label_TargetingMember` and `Button/Button_PlayerParameter`.
The button has one direct child, the inner shared grid. Its direct children
are `Grid.ColumnDefinitions`, the three selected row grids in Hp, Mp, Tp
order, `IconControl/IconControl_LeaderIcon` and
`IconControl/IconControl_MoveMode`. Its column-definition container declares
four `ColumnDefinition` elements. The form contains five `Grid` elements,
four `ColumnDefinition` elements and no `RowDefinition` elements.

Each named candidate above occurs exactly once. The root window and button
each contain all three selected primaries. The label and both icons contain
none. The icons share the row grids' immediate parent. The label is the
button's sibling, outside the button's containing chain for the primaries.
These are XML containment facts only.

The button declares literal `Command="UILuaCommands.Operate"` and
`CommandTarget="Button_PlayerParameter"`. The latter exactly matches its
`Name`. It has no `CommandParameter` or `Target` attribute. The root,
five selected ancestor grids, three primaries, label and two icons have no
`Command`, `CommandParameter`, `CommandTarget` or `Target` attribute.
The form has no trigger element. Its only command-bearing element is this
button. These absences do not establish command routing or input behavior.

## Resources and selected template

The form declares `ResourceDictionary/@Source` values
`common/WINBasisLight_noGrayout.tpl` and `widget/PlayerParameterWidget.tpl`,
in document order. Both match the identified template input paths
relative to `client/sqwt/`. The form declares
`SqwtStyleFile="common/default.style"`. The primary `SqwtStyle` strings are
`PRB_parameter_hpLargeH`, `PRB_parameter_mpLargeH` and
`PRB_parameter_tpLargeH`, respectively. Only the three identified inputs
were decoded. The declared style file and other dependency contents remain unread.

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

## Widget template trigger and action inventory

Across the form and widget template inputs there are three trigger elements,
all in the widget template input. Each belongs to `ControlTemplate.Triggers`. The selected progress-bar
template owns the `EventTrigger` described above. Its event name is literal
and its `SourceName` and animation `To` are binding-shaped strings. The
animation also declares literal `Duration="0.7"`,
`FromAccelType="SpeedUp"`, `ToAccelType="SlowDown"`,
`FromAccelValue="1"` and `ToAccelValue="1"`. The two inputs contain no
element whose kind includes `Condition`.

The other owner is the unique `ControlTemplate` with
`x:Key="ControlTemplate_Label_TargetEffect"` and
`TargetType="{x:Type Label}"`. Its key exactly matches
`Label_TargetingMember/@Template`'s static-resource key. The label declares
literal `VisualOpacity="0"`. The template has one direct `Setter`, with
`Property="RenderTransform"` and `Value="ScaleTransform"`.

| Trigger kind | Raw literal command | Direct action declarations |
|---|---|---|
| `CommandTrigger` | `SQWTDesignCommands.TargetEffectOn` | `StopStoryboard BeginStoryboardName="TargetEffectOff"`, then `BeginStoryboard Name="TargetEffectOn"` |
| `CommandTrigger` | `SQWTDesignCommands.TargetEffectOff` | `StopStoryboard BeginStoryboardName="TargetEffectOn"`, then `BeginStoryboard Name="TargetEffectOff"` |

Each `BeginStoryboard` contains one `Storyboard`. Each storyboard contains
one `PropertyAnimationUsingKeyFrames` with
`Storyboard.TargetProperty="RenderTransformOrigin"` and
`BeginTime="0:0:0"`, containing one `DiscreteValueKeyFrame Value="0.5,0.5"`.
Each also contains one `DoubleAnimation` with
`Storyboard.TargetProperty="VisualOpacity"`, `Duration="0:0:0.2"` and
`BeginTime="0:0:0"`. The On command's raw `To` is `1`, and the Off
command's is `0`. These label-trigger descendants have no `TargetName`,
`Storyboard.TargetName` or `SourceName` attribute. Both command triggers
have only their `Command` attribute. Their stop-action strings exactly match
the opposite begin-action names. These literal joins do not resolve an
implicit target or establish event delivery, animation execution or timing.

## Selected Window template declarations

The form's `Window.Template` contains one `StaticResource`, with literal
`ResourceKey="ControlTemplate_Window_WINBasisLight"`. The identified common
template input contains exactly one `ControlTemplate` with that exact
`x:Key` and `TargetType="{x:Type Window}"`. This is a raw resource-key join.
The common template input declares no `ResourceDictionary/@Source`.

The selected template's direct element kinds are `Grid`, `Setter`, `Setter`
and `ControlTemplate.Triggers`, in document order. Its structural root is
`Grid Name="Grid_Content"`. That grid directly contains the template's one
`ContentPresenter`, which has no `Name` attribute and declares literal
`ClipToBounds="False"`. The direct setters declare `Property="SqwtTopOffset"`
and then `Property="SqwtLeftOffset"`, each with literal `Value="5"`.

Its one `ControlTemplate.Triggers` contains these ten triggers in document
order. All event, name, command and action values in this section are literal
strings. The action column lists direct actions in document order.

| Kind | Trigger attributes | Direct action declarations |
|---|---|---|
| `EventTrigger` | `RoutedEvent="Shown" Name="WindowOpen"` | `StopStoryboard BeginStoryboardName="ClosingAnimation"`, `StopStoryboard BeginStoryboardName="HidingAnimation"`, `BeginStoryboard Name="OpeningAnimation"` |
| `EventTrigger` | `RoutedEvent="Closing" Name="WindowClose"` | `StopStoryboard BeginStoryboardName="OpeningAnimation"`, `StopStoryboard BeginStoryboardName="HidingAnimation"`, `BeginStoryboard Name="ClosingAnimation"` |
| `EventTrigger` | `RoutedEvent="Hiding" Name="WindowHide"` | `StopStoryboard BeginStoryboardName="OpeningAnimation"`, `StopStoryboard BeginStoryboardName="ClosingAnimation"`, `BeginStoryboard Name="HidingAnimation"` |
| `EventTrigger` | `RoutedEvent="Activated" SourceType="Window"` | `ExecuteCommandAction Command="UILuaCommands.Activated"` |
| `EventTrigger` | `RoutedEvent="Deactivated" SourceType="Window"` | `ExecuteCommandAction Command="UILuaCommands.Deactivated"` |
| `EventTrigger` | `RoutedEvent="MouseEnter"` | `SoundPlayerAction FileNumber="3"` |
| `EventTrigger` | `RoutedEvent="GotKeyboardFocus"` | `SoundPlayerAction FileNumber="3"` |
| `EventTrigger` | `RoutedEvent="Click"` | `SoundPlayerAction FileNumber="4"` |
| `CommandTrigger` | `Command="ApplicationCommands.Operate"` | `SoundPlayerAction FileNumber="4"` |
| `CommandTrigger` | `Command="UILuaCommands.Cancel"` | `SoundPlayerAction FileNumber="1"` |

There are eight `EventTrigger` and two `CommandTrigger` elements. Direct
action counts are six `StopStoryboard`, three `BeginStoryboard`, two
`ExecuteCommandAction` and five `SoundPlayerAction`. Each stop-action string
matches a begin-action name in this same selected template.

Each begin action contains one `Storyboard`. Each storyboard declares these
children in document order: one `PropertyAnimationUsingKeyFrames`, then
three `DoubleAnimation` elements. The property animation declares
`Storyboard.TargetProperty="RenderTransformOrigin"` and contains one
`DiscreteValueKeyFrame Value="0.5,0.5"`. The double animations declare
`Duration="0:0:0.2"` and `BeginTime="0:0:0"`. Their property and value
attributes are listed below. An absent attribute is marked absent.

| Begin-action name | Storyboard `CompletedCommand` | `VisualOpacity` `From` / `To` | `SqwtTopOffset` `From` / `To` | `SqwtLeftOffset` `From` / `To` |
|---|---|---|---|---|
| `OpeningAnimation` | absent | `0` / `1` | absent / `0` | absent / `0` |
| `ClosingAnimation` | `ApplicationCommands.DestroyWindow` | `1` / `0` | absent / `5` | absent / `5` |
| `HidingAnimation` | `ApplicationCommands.InvisibleWindow` | `1` / `0` | absent / `5` | absent / `5` |

The property columns denote exact `Storyboard.TargetProperty` strings.
No selected Window trigger or its descendants declares `SourceName`,
`TargetName`, `Storyboard.TargetName`, `CommandTarget`, `CommandParameter`
or `Target`. None has a binding-shaped attribute value. The selected
Window template contains no element whose kind includes `Condition`.
These absences do not resolve implicit sources or targets. The declarations
establish no command or event delivery, audio playback, animation execution,
window lifecycle, applied property value or elapsed duration.

## Claim boundary

This finding establishes selected static containment, attribute presence and
absence, literal versus binding-shaped values, and exact string equality.
It does not establish runtime defaults, native ownership or addressability,
row visibility semantics, suppression policy, input or event routing,
style or resource resolution, computed bindings,
update order, animation timing, rendered layout, visual parity or gameplay.
No live-client result is claimed. No XML body, complete hierarchy or client
bytes are distributed.
