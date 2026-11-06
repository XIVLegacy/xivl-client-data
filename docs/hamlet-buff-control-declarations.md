# Hamlet buff control declarations

For ordinary string operands and numeric slots 1-3 whose `tostring` results
are `"1"`, `"2"` and `"3"`, the inspected naming helpers produce six label
names matching `HamletDefenseWidget.form`. Each label references the template
containing `IconControl_Buff` and the two requested buff-command triggers.
This establishes conditional string equality and declaration containment.
It does not establish native control lookup, resource resolution or delivery.

## Sources and reproduction

The two static client inputs have supplied-build provenance
`2012.09.19.0001` and evidence class `client_extraction`. The build identifier
is supplied provenance, rather than a runtime version measurement.

| Artifact | Bytes | SHA-256 |
| --- | ---: | --- |
| `client/sqwt/widget/HamletDefenseWidget.form` | 9849 | `5bc2fba70027b914334b69e9220ac4f103426c9bb989c40bf57ee5806ebdf6b3` |
| Form decoded strict UTF-8 XML | 9841 | `08acba33aca46fa94be7cf9a8214684ae417209f09d4d266a4ae6148c052c282` |
| `client/sqwt/widget/HamletDefenseWidget.tpl` | 32684 | `0f9e675a2dde33975e0fc9b34a86c8aac49c5831946061db1e5bbc4e3b2ad4de` |
| Template decoded strict UTF-8 XML | 32676 | `91fc6d5370b814144002762503c795442496eb49a9dc1eca60fe194033853a28` |

Both inputs carry the exact eight-byte SQEX signature `5351455800000000`.
The decoding contract is
[xivl-tools:docs/formats/sqex.md, container and key sections](https://github.com/XIVLegacy/xivl-tools/blob/604210657f4858fb69744a3a92c90f3369040057/docs/formats/sqex.md#what-the-container-is).
At that revision, the format page is 9412 bytes, SHA-256
`72fb258459edbf256402255180812f8529ddf16aceaf6d2e46bd76acbd2fa3d0`.
The existing
[xivl-tools:tools/blowfish.py, Blowfish](https://github.com/XIVLegacy/xivl-tools/blob/604210657f4858fb69744a3a92c90f3369040057/tools/blowfish.py#L60)
is 4324 bytes, SHA-256
`7c4208f5d3b7acf20bfb67ddcba706cbb10bf4d1c6c1677b4b11d8685774f90e`.

1. Authenticate each complete input against its byte count, SHA-256 and
   signature. Use its case-sensitive ASCII basename, including `.form` or
   `.tpl`, as the Blowfish key.
2. Decrypt after the signature in memory. Use little-endian block halves and
   retain the clear partial-block tail. Require the decoded identities above.
3. Decode strict UTF-8 and parse with Python's `xml.etree.ElementTree`.
   Re-encrypt, prepend the signature and require byte-for-byte input equality.
4. Select only the names, namespace-qualified template key and command
   subtrees below. Preserve raw attributes, order, multiplicity and absence.
   Do not flatten templates or resolve external references.

Both documents passed these checks. Their bodies remain undistributed.
The input files are required to reproduce the extraction.

The Lua identity and adopted caller frames come from
[xivl-client-scripts:docs/hamlet-buff-hud-contract.md, sources, guard and control selection](https://github.com/XIVLegacy/xivl-client-scripts/blob/9d9f70f2a39f16bad27fab50f4e6f6c54370d82f/docs/hamlet-buff-hud-contract.md#guard-and-control-selection).
That published finding is 17938 bytes, SHA-256
`5407a331fb820db096cd0a4cedc9a19e0c2d438fa4b49dc4ad2b07168eb544be`.
Its caller, initializer and reset bodies are adopted findings here, rather
than additional raw-body analysis.

| Lua artifact | Bytes | SHA-256 |
| --- | ---: | --- |
| `lua.zip`, member source archive | 14385427 | `0e8f902f7a2f592fc1220d41b89a3f35ec395cfb261806d4bd590a530099ae31` |
| `widget/hamletdefensewidget.lua`, canonical archive member | 22816 | `1d2eee659669adc83b82b8d7ba58cf799756194de89cd100aea09bb8a1f9a440` |
| `client/script/n1635q/29xy5q6545wr5n1635q.le.lpb` | 10206 | `882b2b249b3de84a593e4084e8cb7e49fbb00b3bf4cbd0fc911d1a2814964286` |
| Decoded original Lua 5.1 payload | 10193 | `a564717080911218c718ea28f4a8b604a9850b3f2db27bcd73ed9cec93715d9e` |

The canonical decoded path is `lua/scripts/widget/hamletdefensewidget.lua`.
The archive's declared source revision is
`40006d5d716583d78690a6f3ef50ca1bc41dddee`; the adopted finding's source
section identifies its manifest and coverage rows. The complete archive,
selected member, original LPB and decoded payload were authenticated.
Original decoding used
[xivl-client-scripts:tools/retail_script.py, decode_lpb](https://github.com/XIVLegacy/xivl-client-scripts/blob/9d9f70f2a39f16bad27fab50f4e6f6c54370d82f/tools/retail_script.py#L24).
Structural reads and instruction fields used
[xivl-client-scripts:tools/build_quest_contracts.py, ChunkReader and instruction](https://github.com/XIVLegacy/xivl-client-scripts/blob/9d9f70f2a39f16bad27fab50f4e6f6c54370d82f/tools/build_quest_contracts.py#L67).
Only the following two helpers and their necessary header/root bindings were
interpreted. Required modules and other method bodies were not interpreted.

| Helper | Original prototype | Code offset | Words | Canonical lines | Root closure / binding PCs |
| --- | --- | ---: | ---: | --- | --- |
| `getTemplateControlName` | `root/proto31` | 10048 | 6 | 1118-1127 | 101 / 102 |
| `getIndexControlName` | `root/proto32` | 10119 | 7 | 1130-1140 | 104 / 105 |

Offsets are decoded-payload byte offsets and PCs are zero-based. Both helpers
have three fixed parameters, including `self`, and zero vararg flags,
upvalues and child prototypes. Root PCs 100 and 103 read the global
`HamletDefenseWidget` before their respective closure/binding pairs.
The canonical header at lines 1-9 requires `/Widget/WidgetBaseClass` and
declares that base. These are dependency names, without a construction claim.

## Naming behavior and conditional caller composition

`getTemplateControlName(self, label, part)` returns exactly one value from
concatenating `label`, the literal colon `":"`, and `part`, in that order.
It does not read `self`, resolve a member or call another function.

`getIndexControlName(self, prefix, index)` resolves the global `tostring`
afresh, calls it with `index` as its only argument, retains exactly one
result and concatenates `prefix` with that result. It returns exactly one
value. It does not pass `self` to the call, add padding, subtract from the
index or perform a member lookup. The binding named `tostring` is dynamic.
An arbitrary replacement is not guaranteed to behave like the standard
library. Concatenation remains subject to original Lua 5.1 semantics.

Neither helper guards the operands or catches a lookup, call or
concatenation error. Each original prototype also has an unreachable final
zero-value return after the one-value return. Neither has a tail call.
The unmodified canonical statements and original instruction semantics agree
on these operations and result widths. Focused comparisons used authored
string operands and callable bindings, without treating a newer Lua library
as evidence for original behavior on other types.

The adopted callers first request the index name, retaining one result, then
the template name with part `"IconControl_Buff"`, retaining one result.
Conditioned on those dynamic method bindings selecting the helpers above,
ordinary concatenation and `tostring(1..3)` producing the decimal strings
`"1"`, `"2"`, `"3"`, the exact outputs are:

| Prefix and numeric slot | Label result / command target | Icon control string |
| --- | --- | --- |
| Army, 1 | `Label_ArmyBuff_1` | `Label_ArmyBuff_1:IconControl_Buff` |
| Army, 2 | `Label_ArmyBuff_2` | `Label_ArmyBuff_2:IconControl_Buff` |
| Army, 3 | `Label_ArmyBuff_3` | `Label_ArmyBuff_3:IconControl_Buff` |
| Enemy, 1 | `Label_EnemyBuff_1` | `Label_EnemyBuff_1:IconControl_Buff` |
| Enemy, 2 | `Label_EnemyBuff_2` | `Label_EnemyBuff_2:IconControl_Buff` |
| Enemy, 3 | `Label_EnemyBuff_3` | `Label_EnemyBuff_3:IconControl_Buff` |

Army uses the literal prefix `"Label_ArmyBuff_"`; enemy uses
`"Label_EnemyBuff_"`. As recorded by the adopted caller, selected commands
are sent to the label string, while icon/visibility requests use the colon
string. Numeric slots 1 and 2 can request `UILuaCommands.BuffUp` or
`UILuaCommands.BuffDown` on their selected value branches. Slot 3 requests no
control command in that contract. Declaration of a trigger below does not
add a slot-3 command request.

## Selected form and template declarations

Both documents use element namespace
`http://namespace.square-enix.com/sqwt`. The form root is `Window`; the
template root is `ResourceDictionary`. Here `x:Key` means the attribute in
`http://namespace.square-enix.com/sqwt/x`, not an unqualified `Key` or `Name`.

Each of the six label results above occurs exactly once as a `Label/@Name`
in the form. All six declare raw
`Template="{StaticResource ControlTemplate_Label_Buff}"`,
`Margin="0,0,0,2"`, `HorizontalAlignment="Center"`, `Width="32"`,
`Height="32"` and `IsHitTestVisible="False"`. They have no child elements.
There is no form control whose `Name` is the full colon string in the table;
the composition relates a label name and a template-contained name.

Exactly one namespace-qualified `ControlTemplate` has
`x:Key="ControlTemplate_Label_Buff"`. Its raw `TargetType` is `"Label"`.
Within that selected template, exactly one `IconControl` has
`Name="IconControl_Buff"`. It declares `IconDatas="0"`,
`HorizontalAlignment="Center"`, `VerticalAlignment="Center"`,
`Width="32"`, `Height="32"`, `IsHitTestVisible="False"` and
`Visibility="Visible"`, with no child elements. `IconDatas="0"` is an
authored raw attribute, rather than identification of a requested icon.
The separator's native interpretation and template instantiation remain unverified.

The form's `ResourceDictionary/@Source` declarations are
`common/WINBasisLight_noGrayout.tpl` and `widget/HamletDefenseWidget.tpl`,
in document order. The second dependency name matches the selected template
file. The first dependency, styles and other external references remain unread.
Names and containment do not prove that these resources resolved.

Within `ControlTemplate_Label_Buff`, exactly one `CommandTrigger` declares
each selected command. The `UILuaCommands.BuffUp` trigger directly contains
one `BeginStoryboard` with `Name="BuffUp"`; the `UILuaCommands.BuffDown`
trigger directly contains one with `Name="BuffDown"`. Each contains one
attribute-free `Storyboard`. Its direct `DoubleAnimation` declarations are
listed below in their original order, preserving both Up target groups.
All nine declare raw `Duration="0:0:0.4"` and have no child elements.

| Command suffix | Ordinal | Raw `Storyboard.TargetName` | Raw `Storyboard.TargetProperty` | `From` | `To` | `BeginTime` |
| --- | ---: | --- | --- | --- | --- | --- |
| `BuffUp` | 1 | `Label_BuffEffect_Up_1` | `VisualOpacity` | `1` | `0` | absent |
| `BuffUp` | 2 | `Label_BuffEffect_Up_1` | `RenderTransform.ScaleX` | `1` | `3` | absent |
| `BuffUp` | 3 | `Label_BuffEffect_Up_1` | `RenderTransform.ScaleY` | `1` | `3` | absent |
| `BuffUp` | 4 | `Label_BuffEffect_Up_2` | `VisualOpacity` | `1` | `0` | `0:0:0.2` |
| `BuffUp` | 5 | `Label_BuffEffect_Up_2` | `RenderTransform.ScaleX` | `1` | `3` | `0:0:0.2` |
| `BuffUp` | 6 | `Label_BuffEffect_Up_2` | `RenderTransform.ScaleY` | `1` | `3` | `0:0:0.2` |
| `BuffDown` | 1 | `Label_BuffEffect_Down_1` | `VisualOpacity` | `1` | `0` | absent |
| `BuffDown` | 2 | `Label_BuffEffect_Down_1` | `RenderTransform.ScaleX` | `3` | `1` | absent |
| `BuffDown` | 3 | `Label_BuffEffect_Down_1` | `RenderTransform.ScaleY` | `3` | `1` | absent |

Each of those three distinct target strings equals exactly one `Label/@Name`
within the same selected template. Each target label declares
`HorizontalAlignment="Center"`, `VerticalAlignment="Center"`,
`RenderTransformOrigin="0.5,0.5"`, `IsHitTestVisible="False"` and
`VisualOpacity="0"`. Each has a `Label.RenderTransform/ScaleTransform`
declaration with raw `CenterX="0.5"` and `CenterY="0.5"`.
Neither `ScaleX` nor `ScaleY` is an attribute on those selected transforms.
Absence supplies no default value. The animation table records authored
property paths and time strings, without evaluating them or asserting timing.

## Verification and remaining boundary

Literal assertions covered both complete helper contracts, six unpadded
names and colon strings, selected namespace/key/name containment, two
commands, three effect targets and all nine ordered animation declarations.
Rejecting controls covered separator, argument/index and result-width
changes, dynamic conversion, zero padding, zero-based indices, Name/key and
namespace mixups, template flattening, command/target/property confusion,
lost target groups, absent attributes, input/key mismatch and roundtrip error.

The first unresolved edge is the actual dynamic method/global binding at
invocation. Even with the inspected helpers and ordinary conversion, exact
string matches do not prove template/resource/native-part resolution,
successful icon or visibility assignment, command delivery, animation
execution or timing, rendered icon/status identity, historical gameplay state,
or a director-to-HUD argument join. No renderer, native implementation or live
client result is claimed. Other controls/templates, command bodies, style
defaults and transitive dependencies remain outside this finding.
